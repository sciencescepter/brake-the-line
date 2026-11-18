"""Plain helpers behind the Streamlit page (app.py). No Streamlit imports here,
so everything can be tested.

Queue order everywhere: urgency (safety_urgent, soon, routine), then
received_at earliest first, then message_id. It comes from
triage.booking.queue_order, the same function the booking tool uses.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path

from .booking import QueueItem, Slot, queue_order
from .rules import FIX_PATH_LABELS, URGENCY_RANK, FixPath, Urgency
from .schema import FaultMessage

ROOT = Path(__file__).resolve().parent.parent
SCHEDULE = ROOT / "output" / "service_schedule.csv"


@dataclass(frozen=True)
class QueueRow:
    position: int                 # queue #, fixed: filters never renumber it
    message_id: str
    received_at: datetime
    urgency: Urgency
    fix_path: FixPath
    vehicle_alert_code: str
    reason: str
    subject: str
    message_text: str
    slot_id: str = ""
    slot_date: date | None = None
    slot_start_time: time | None = None
    duration_minutes: int | None = None
    slot_type: str = ""

    @property
    def fix_path_label(self) -> str:
        return FIX_PATH_LABELS[self.fix_path]

    @property
    def booked(self) -> bool:
        return bool(self.slot_id)


def load_schedule(path: Path = SCHEDULE) -> dict[str, dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return {r["message_id"]: r for r in csv.DictReader(f)}


def build_queue(messages: list[FaultMessage], tags: dict[str, dict], schedule: dict[str, dict]) -> list[QueueRow]:
    """Tagged messages in queue order, joined to their booked slot (if any)."""
    by_id = {m.message_id: m for m in messages}
    items = [
        QueueItem(mid, by_id[mid].received_at, Urgency(t["urgency"]), FixPath(t["fix_path"]),
                  by_id[mid].vehicle_alert_code)
        for mid, t in tags.items() if mid in by_id
    ]
    rows = []
    for pos, it in enumerate(queue_order(items), start=1):
        m, t, s = by_id[it.message_id], tags[it.message_id], schedule.get(it.message_id)
        rows.append(QueueRow(
            position=pos,
            message_id=it.message_id,
            received_at=it.received_at,
            urgency=it.urgency,
            fix_path=it.fix_path,
            vehicle_alert_code=it.vehicle_alert_code,
            reason=t.get("reason", ""),
            subject=m.message_subject,
            message_text=m.message_text,
            slot_id=s["slot_id"] if s else "",
            slot_date=date.fromisoformat(s["slot_date"]) if s else None,
            slot_start_time=time.fromisoformat(s["slot_start_time"]) if s else None,
            duration_minutes=int(s["duration_minutes"]) if s else None,
            slot_type=s["slot_type"] if s else "",
        ))
    return rows


def filter_queue(rows: list[QueueRow], urgencies: set[str] | None = None,
                 slot_types: set[str] | None = None, search: str = "") -> list[QueueRow]:
    """Keep rows that match. Order and queue # stay as they were."""
    q = search.strip().lower()
    return [
        r for r in rows
        if (not urgencies or r.urgency.value in urgencies)
        and (not slot_types or r.slot_type in slot_types)
        and (not q or q in r.message_text.lower() or q in r.subject.lower() or q in r.message_id.lower())
    ]


def open_slots_after(slots: list[Slot], booked_slot_ids: set[str]) -> list[Slot]:
    """Slots nobody has booked yet."""
    return [s for s in slots if s.slot_id not in booked_slot_ids]


def position_for_new(rows: list[QueueRow], urgency: Urgency) -> tuple[int, int]:
    """Where a message submitted now would sit: after every message with the same
    or higher urgency, because it is the most recent. Returns (queue #, its rank
    within its own tag)."""
    rank = URGENCY_RANK[urgency]
    ahead = sum(1 for r in rows if URGENCY_RANK[r.urgency] <= rank)
    same = sum(1 for r in rows if r.urgency is urgency)
    return ahead + 1, same + 1


def pasted_message(text: str, alert_code: str, existing_ids: set[str], now: datetime | None = None) -> FaultMessage:
    """Wrap pasted text in a FaultMessage so it goes through the same validation
    as a batch row. Fields the owner didn't give get neutral placeholders."""
    n = 10001
    while f"MSG-{n:05d}" in existing_ids:
        n += 1
    return FaultMessage.model_validate({
        "message_id": f"MSG-{n:05d}",
        "received_at": (now or datetime.now()).replace(microsecond=0),
        "channel": "mobile_app",
        "customer_name": "Pasted message",
        "vehicle_model": "Model 3",
        "model_year": 2024,
        "vin_last6": "000000",
        "odometer_km": 0,
        "service_center": "Not specified",
        "vehicle_alert_code": alert_code or "NONE",
        "message_subject": "pasted message",
        "message_text": text,
        "hand_checked": False,
        "hand_checked_safety_fault": False,
    })
