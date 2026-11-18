"""Stage 4: urgency-sorted fault queue page.

    streamlit run app.py

Reads the Stage 2 and 3 outputs; all rules, tagging and booking logic comes from
triage/. The page loads without an API key; only the paste box needs one.
"""

from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from pydantic import ValidationError

from triage.booking import SLOT_TYPE_LABELS, BookingTool, QueueItem, load_slots
from triage.llm import DailyLimitReached, openrouter_chat, tag_message
from triage.load import load_batch
from triage.queue_view import (
    build_queue, filter_queue, load_schedule, open_slots_after, pasted_message, position_for_new,
)
from triage.rules import FIX_PATH_LABELS, KNOWN_ALERT_CODES, SAFETY_ALERT_CODES, Urgency, required_urgency
from triage.safety_check import load_tags, run_check

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")

st.set_page_config(page_title="Brake the Line: Fault Queue", page_icon="🛠️", layout="wide")

URGENCY_STYLE = {
    "safety_urgent": "background-color: rgba(220, 38, 38, 0.18); color: #b91c1c; font-weight: 600",
    "soon": "background-color: rgba(217, 119, 6, 0.18); color: #b45309; font-weight: 600",
    "routine": "background-color: rgba(37, 99, 235, 0.12); color: #1d4ed8",
}


# ---- data (cached) -----------------------------------------------------------

@st.cache_data
def load_all():
    messages, rejected = load_batch()
    tags = load_tags()
    schedule = load_schedule()
    rows = build_queue(messages, tags, schedule)
    safety = run_check(messages, tags)
    slots, _ = load_slots()
    return messages, rejected, tags, schedule, rows, safety, slots


@st.cache_resource
def chat_client():
    return openrouter_chat()


messages, rejected, tags, schedule, rows, safety, slots = load_all()
booking_day = min(s.slot_date for s in slots)
api_key = os.environ.get("OPENROUTER_API_KEY", "").strip()

st.title("Brake the Line: urgency-sorted fault queue")
st.caption(
    f"Overnight batch of {len(messages)} owner fault messages, booked into open slots for the week of "
    f"16–21 Nov 2026. Queue order: safety_urgent, then soon, then routine; earliest submitted first "
    f"within each tag."
)

# ---- 1. count bar ------------------------------------------------------------

n_total = len(messages) + len(rejected)
count = {u: sum(1 for r in rows if r.urgency is u) for u in Urgency}
n_booked = sum(1 for r in rows if r.booked)
n_missed, n_hand = len(safety.misses), len(safety.rows)

c = st.columns(6)
c[0].metric("Total processed", f"{len(rows)} of {n_total}", border=True)
c[1].metric("safety_urgent", count[Urgency.SAFETY_URGENT], border=True)
c[2].metric("soon", count[Urgency.SOON], border=True)
c[3].metric("routine", count[Urgency.ROUTINE], border=True)
c[4].metric("Booked", f"{n_booked} of {n_total}", border=True)
miss_colour = "#dc2626" if n_missed else "#16a34a"
c[5].markdown(
    f"""<div style="border:1px solid rgba(128,128,128,.3);border-radius:.5rem;padding:.75rem 1rem;
    height:100%;background:{miss_colour}1a">
    <div style="font-size:.875rem;opacity:.8">Safety faults missed</div>
    <div style="font-size:2.25rem;font-weight:600;color:{miss_colour};line-height:1.3">{n_missed} of {n_hand}</div>
    </div>""",
    unsafe_allow_html=True,
)

# ---- 2. queue ----------------------------------------------------------------

st.subheader("Fault queue")
f1, f2, f3 = st.columns([1, 1, 2])
pick_urg = f1.multiselect("Tag", [u.value for u in Urgency])
pick_slot = f2.multiselect("Slot type", list(SLOT_TYPE_LABELS), format_func=SLOT_TYPE_LABELS.get)
search = f3.text_input("Search message text", placeholder="e.g. pedal, steering, wiper")
shown = filter_queue(rows, set(pick_urg), set(pick_slot), search)

df = pd.DataFrame([{
    "Queue #": r.position,
    "Message": r.message_id,
    "Submitted": r.received_at.strftime("%a %d %b %H:%M"),
    "Time slot": (f"{r.slot_date:%a %d %b} {r.slot_start_time:%H:%M} ({r.duration_minutes} min)"
                  if r.booked else "not booked"),
    "Slot type": SLOT_TYPE_LABELS.get(r.slot_type, "-"),
    "Issue type (alert code)": r.vehicle_alert_code,
    "Tag": r.urgency.value,
    "Fix path": r.fix_path_label,
    "Reason": r.reason,
} for r in shown])

st.caption(f"Showing {len(shown)} of {len(rows)}. Select a row to read the full message.")
if df.empty:
    st.info("No messages match these filters.")
else:
    event = st.dataframe(
        df.style.map(lambda v: URGENCY_STYLE.get(v, ""), subset=["Tag"]),
        hide_index=True,
        height=420,
        on_select="rerun",
        selection_mode="single-row",
        key="queue",
        column_config={
            "Queue #": st.column_config.NumberColumn(width="small"),
            "Reason": st.column_config.TextColumn(width="large"),
        },
    )
    picked = event.selection.rows if event and event.selection else []
    if picked:
        r = shown[picked[0]]
        with st.expander(f"#{r.position} · {r.message_id} · {r.subject}", expanded=True):
            st.write(r.message_text)
            st.caption(f"Submitted {r.received_at:%a %d %b %Y %H:%M} · alert code {r.vehicle_alert_code} · "
                       f"{r.urgency.value} → {r.fix_path_label} · slot {r.slot_id or '-'}")

# ---- 3. safety check ---------------------------------------------------------

st.subheader("Safety check: tags vs the 60 hand-checked safety messages")
s1, s2, s3 = st.columns(3)
s1.metric("Hand-checked safety faults", n_hand, border=True)
s2.metric("Tagged safety_urgent", n_hand - n_missed, border=True)
s3.metric("Extra safety_urgent outside the hand-checked set", len(safety.extra_safety), border=True)

if safety.misses:
    st.error("Missed safety faults (tagged soon, routine or not tagged):\n\n" + "\n".join(
        f"- **{m.message_id}** [{m.vehicle_alert_code}] tagged {m.tag or 'nothing'}: {m.subject}"
        for m in safety.misses))
else:
    st.success(f"0 of {n_hand} missed. Every hand-checked safety fault is tagged safety_urgent, "
               f"including the calm messages with no safety alert code.")

caught_label = {"alert code": "Alert code", "hidden-safety text": "Hidden-safety text", "model only": "Model"}
safety_df = pd.DataFrame([{
    "Message": r.message_id, "Alert code": r.vehicle_alert_code, "Tag given": r.tag or "not tagged",
    "Caught by": caught_label[r.caught_by], "Subject": r.subject,
} for r in safety.rows])
st.dataframe(
    safety_df.style.map(lambda v: URGENCY_STYLE.get(v, "color: #dc2626; font-weight: 600")
                        if v != "safety_urgent" else URGENCY_STYLE[v], subset=["Tag given"]),
    hide_index=True, height=300,
)

# ---- 4. paste box ------------------------------------------------------------

st.subheader("Tag a new message")
if not api_key:
    st.info("The paste box needs OPENROUTER_API_KEY in .env (or the environment). "
            "The rest of the page works without it.")

codes = ["NONE"] + sorted(c for c in KNOWN_ALERT_CODES if c != "NONE")
with st.form("paste"):
    text = st.text_area("Owner message", height=120, disabled=not api_key,
                        placeholder="Paste an owner fault message here")
    code = st.selectbox("Vehicle alert code (optional)", codes, disabled=not api_key,
                        format_func=lambda c: "None shown" if c == "NONE" else
                        f"{c}  (safety alert)" if c in SAFETY_ALERT_CODES else c)
    submitted = st.form_submit_button("Tag and preview booking", disabled=not api_key, type="primary")

if submitted:
    try:
        msg = pasted_message(text, code, {m.message_id for m in messages})
    except ValidationError as e:
        st.error("This message can't be tagged: " + "; ".join(err["msg"] for err in e.errors()))
        st.stop()

    with st.spinner("Asking the model and checking its answer against the schema…"):
        try:
            outcome = tag_message(msg, chat_client())
        except DailyLimitReached:
            st.error("The model's daily request limit is used up. Try again later.")
            st.stop()
        except Exception as e:
            st.error(f"Could not reach the model: {type(e).__name__}")
            st.stop()

    if outcome.flagged:
        st.error(f"Flagged for review: the model's answer failed validation {outcome.attempts} times, "
                 "so it was not accepted.")
        for err in outcome.errors:
            st.caption(err)
        st.stop()

    res = outcome.result
    must, why = required_urgency(msg.vehicle_alert_code, msg.full_text)
    pos, within = position_for_new(rows, res.urgency)

    a, b, d = st.columns(3)
    a.markdown(f"**Urgency**<br><span style='{URGENCY_STYLE[res.urgency.value]};padding:.15rem .5rem;"
               f"border-radius:.3rem'>{res.urgency.value}</span>", unsafe_allow_html=True)
    b.markdown(f"**Fix path**<br>{FIX_PATH_LABELS[res.fix_path]}", unsafe_allow_html=True)
    d.markdown(f"**Hidden safety symptom**<br>{'Yes' if res.hidden_safety_symptom else 'No'}",
               unsafe_allow_html=True)
    st.markdown(f"**Reason:** {res.reason}")
    st.caption(f"Validated by Pydantic on attempt {outcome.attempts}"
               + (f" · hard rule: {why}" if must else " · no hard rule applied; the model's tag stands"))

    st.markdown(f"**Queue position:** would be **#{pos}**, last of the {res.urgency.value} messages "
                f"({within} of {within}), because it was submitted most recently.")

    booked_ids = {r["slot_id"] for r in schedule.values()}
    tool = BookingTool(open_slots_after(slots, booked_ids), booking_day=booking_day)
    preview = tool.book(QueueItem(msg.message_id, msg.received_at, res.urgency, res.fix_path,
                                  msg.vehicle_alert_code))
    if preview:
        st.markdown(f"**Slot preview:** {preview.slot_id}, {preview.slot_date:%a %d %b} "
                    f"{preview.slot_start_time:%H:%M} ({preview.duration_minutes} min), "
                    f"{SLOT_TYPE_LABELS[preview.slot_type]}"
                    + ("" if preview.same_day or res.urgency is not Urgency.SAFETY_URGENT else
                       f". Not same day: no bays left on {booking_day:%a %d %b}."))
    else:
        st.warning("No open slot this week fits this tag. It would go on the waitlist.")
    st.caption("Preview only. The schedule files are not changed.")
