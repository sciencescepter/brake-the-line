"""Stage 3: book every tagged message into a service slot and write the report.

Reads   data/Overnight Fault Message Batch (16 November 2026).csv
        data/Open Service Slots, Week of 16-21 November 2026.csv
        output/tagged_messages.csv   (from scripts.tag_batch)
Writes  output/service_schedule.csv  one row per booked message, in queue order
        output/waitlist.csv          messages with no slot left (should be empty)
        output/booking_report.md     the booking page plus the safety check report

    python -m scripts.book_queue
"""

from __future__ import annotations

import csv
from collections import Counter
from datetime import datetime
from pathlib import Path

from triage.booking import SLOT_TYPE_LABELS, Booking, QueueItem, book_all, load_slots
from triage.load import load_batch
from triage.rules import FIX_PATH_LABELS, FixPath, Urgency
from triage.safety_check import load_tags, run_check

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"


def slot_text(b: Booking) -> str:
    return f"{b.slot_date:%a %d %b} {b.slot_start_time:%H:%M} ({b.duration_minutes} min)"


def main() -> int:
    messages, rejected_msgs = load_batch()
    slots, rejected_slots = load_slots()
    tags = load_tags()
    by_id = {m.message_id: m for m in messages}

    untagged = [m.message_id for m in messages if m.message_id not in tags]
    items = [
        QueueItem(
            message_id=mid,
            received_at=by_id[mid].received_at,
            urgency=Urgency(t["urgency"]),
            fix_path=FixPath(t["fix_path"]),
            vehicle_alert_code=by_id[mid].vehicle_alert_code,
        )
        for mid, t in tags.items() if mid in by_id
    ]
    bookings, waitlist = book_all(items, slots)
    safety = run_check(messages, tags)

    OUT.mkdir(exist_ok=True)
    with open(OUT / "service_schedule.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["queue_position", "message_id", "urgency", "fix_path", "vehicle_alert_code", "slot_id",
                    "slot_date", "slot_start_time", "duration_minutes", "slot_type", "bay_id",
                    "technician_id", "same_day"])
        for i, b in enumerate(bookings, start=1):
            w.writerow([i, b.message_id, b.urgency.value, b.fix_path.value, b.vehicle_alert_code, b.slot_id,
                        b.slot_date.isoformat(), b.slot_start_time.strftime("%H:%M"), b.duration_minutes,
                        b.slot_type, b.bay_id, b.technician_id, b.same_day])
    with open(OUT / "waitlist.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["message_id", "urgency", "fix_path", "vehicle_alert_code"])
        for q in waitlist:
            w.writerow([q.message_id, q.urgency.value, q.fix_path.value, q.vehicle_alert_code])

    # ---- report -------------------------------------------------------------
    urg = Counter(b.urgency for b in items)
    booked_urg = Counter(b.urgency for b in bookings)
    safety_b = [b for b in bookings if b.urgency is Urgency.SAFETY_URGENT]
    booking_day = min(s.slot_date for s in slots)
    by_day = Counter(b.slot_date for b in safety_b)
    routine_types = Counter(b.slot_type for b in bookings if b.urgency is Urgency.ROUTINE)
    n_hand = len(safety.rows)
    caught = Counter(r.caught_by for r in safety.rows)

    L: list[str] = []
    L += ["# Service Booking Report: week of 16 to 21 November 2026", ""]
    L += [f"Generated {datetime.now():%d %b %Y %H:%M} by `scripts/book_queue.py`. Booking day: "
          f"**{booking_day:%a %d %b %Y}** (first day in the slot list).", ""]
    L += ["| Processed | safety_urgent | soon | routine | Booked | Waitlist | Safety faults missed |",
          "|---|---|---|---|---|---|---|",
          f"| {len(items)} of {len(messages)} | {urg[Urgency.SAFETY_URGENT]} | {urg[Urgency.SOON]} | "
          f"{urg[Urgency.ROUTINE]} | {len(bookings)} of {len(messages)} | {len(waitlist)} | "
          f"**{len(safety.misses)} of {n_hand}** |", ""]

    # Safety check
    L += ["## Safety check: tags vs the 60 hand-checked safety messages", ""]
    L += [f"The service team hand-checked {n_hand} messages and marked all of them as safety faults. "
          f"A hand-checked message tagged `soon` or `routine` counts as a miss.", ""]
    L += ["| Result | Count |", "|---|---|",
          f"| Hand-checked safety faults | {n_hand} |",
          f"| Tagged `safety_urgent` | {n_hand - len(safety.misses)} |",
          f"| **Missed (tagged soon / routine / untagged)** | **{len(safety.misses)}** |",
          f"| Caught with a safety alert code | {caught['alert code']} |",
          f"| Caught with no safety code (calm or hidden symptom in the text) | "
          f"{caught['hidden-safety text'] + caught['model only']} |",
          f"| Tagged `safety_urgent` outside the hand-checked set | {len(safety.extra_safety)} |", ""]
    if safety.misses:
        L += ["**Misses:**", ""] + [f"- {r.message_id} [{r.vehicle_alert_code}] tagged {r.tag or 'nothing'}: "
                                     f"{r.subject}" for r in safety.misses] + [""]
    else:
        L += ["**No misses.** Every hand-checked safety fault is tagged `safety_urgent`, including the calm, "
              "friendly messages with a brake or steering symptom and no alert code.", ""]
    L += [f"The {len(safety.extra_safety)} extra `safety_urgent` messages either carry a safety alert code "
          "or describe a brake, pedal, stability or steering symptom. They weren't in the hand-checked "
          "sample, so they can't count as misses or false alarms.", ""]
    L += ["<details><summary>All 60 hand-checked messages</summary>", "",
          "| Message | Alert code | Tag given | Caught by | Subject |", "|---|---|---|---|---|"]
    L += [f"| {r.message_id} | {r.vehicle_alert_code} | {r.tag or '-'} | {r.caught_by} | {r.subject} |"
          for r in safety.rows]
    L += ["", "</details>", ""]

    # Booking checks
    L += ["## Booking checks", ""]
    L += [f"- **No slot booked twice:** {len(bookings)} bookings use {len({b.slot_id for b in bookings})} "
          f"different slots."]
    L += [f"- **safety_urgent same day:** {by_day.get(booking_day, 0)} of {len(safety_b)} booked on "
          f"{booking_day:%a %d %b}. The service center bays ran out, so the rest carried over to the "
          "earliest bays on the following days: "
          + ", ".join(f"{d:%a %d %b} {n}" for d, n in sorted(by_day.items()) if d != booking_day) + "."
          if len(by_day) > 1 else
          f"- **safety_urgent same day:** all {len(safety_b)} booked on {booking_day:%a %d %b}."]
    L += [f"- **Order:** every safety_urgent booking comes before soon and routine. soon took the "
          f"{booked_urg[Urgency.SOON]} next bays. routine filled remote/OTA and callback slots, then mobile "
          f"visits, then spare bays: "
          + ", ".join(f"{SLOT_TYPE_LABELS[t]} {n}" for t, n in routine_types.most_common()) + "."]
    L += [f"- **Rejected input rows:** {len(rejected_msgs)} messages, {len(rejected_slots)} slots. "
          f"**Untagged messages:** {len(untagged)}. **Waitlist:** {len(waitlist)}.", ""]

    # Booking page
    L += ["## Booking page", "",
          "In queue order: safety_urgent first, then soon, then routine. Oldest message first within each tag.", "",
          "| # | Message | Time slot | Slot type | Issue type (alert code) | Tag | Fix path |",
          "|---|---|---|---|---|---|---|"]
    for i, b in enumerate(bookings, start=1):
        L.append(f"| {i} | {b.message_id} | {slot_text(b)} | {SLOT_TYPE_LABELS[b.slot_type]} | "
                 f"{b.vehicle_alert_code} | {b.urgency.value} | {FIX_PATH_LABELS[b.fix_path]} |")
    if waitlist:
        L += ["", "### Waitlist (no slot left this week)", "", "| Message | Tag | Alert code |", "|---|---|---|"]
        L += [f"| {q.message_id} | {q.urgency.value} | {q.vehicle_alert_code} |" for q in waitlist]
    (OUT / "booking_report.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    print(f"Booked {len(bookings)} of {len(messages)}  waitlist {len(waitlist)}  untagged {len(untagged)}")
    print(f"safety_urgent same day ({booking_day}): {by_day.get(booking_day, 0)} of {len(safety_b)}; "
          f"by day {dict(sorted((str(d), n) for d, n in by_day.items()))}")
    print(f"routine slot types: {dict(routine_types)}")
    print(f"Safety check: {len(safety.misses)} of {n_hand} missed")
    print("Saved output/service_schedule.csv, output/waitlist.csv, output/booking_report.md")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
