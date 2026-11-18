"""Booking tool: assign every tagged message one open service slot.

Rules
1. safety_urgent books first, into service center bays, starting on the booking
   day (the first day in the slot list). When that day's bays run out it carries
   into the earliest bay on the following day.
2. soon books next, into the service center bays left after safety_urgent.
3. routine books last. It fills remote/OTA and support callback slots first,
   then mobile service visits, then any service center bays still free.
4. A slot holds one message only. No slot_id is booked twice.

Inside each tag, older messages book first (received_at, then message_id).
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from datetime import date, datetime, time
from pathlib import Path
from typing import Annotated, Literal

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, ValidationError, model_validator

from .load import RejectedRow
from .rules import URGENCY_RANK, FixPath, Urgency

DATA = Path(__file__).resolve().parent.parent / "data"
DEFAULT_SLOTS = DATA / "Open Service Slots, Week of 16-21 November 2026.csv"

SlotType = Literal["service_center_bay", "mobile_service_visit", "remote_ota_or_diagnostic", "support_callback"]

SLOT_TYPE_LABELS: dict[str, str] = {
    "service_center_bay": "Service center bay",
    "mobile_service_visit": "Mobile service visit",
    "remote_ota_or_diagnostic": "Remote / OTA diagnostic",
    "support_callback": "Support callback",
}

# Slot types each tag may take, in order of preference. Each inner tuple is one
# tier: the earliest open slot in the first tier with space wins.
SLOT_TIERS: dict[Urgency, tuple[tuple[str, ...], ...]] = {
    Urgency.SAFETY_URGENT: (("service_center_bay",),),
    Urgency.SOON: (("service_center_bay",),),
    Urgency.ROUTINE: (
        ("remote_ota_or_diagnostic", "support_callback"),
        ("mobile_service_visit",),
        ("service_center_bay",),
    ),
}


class Slot(BaseModel):
    """One row of the Open Service Slots CSV. Bad rows are rejected."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    slot_id: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^SLOT-\d{4}$")]
    slot_date: date
    slot_start_time: time
    duration_minutes: int = Field(gt=0, le=480)
    slot_type: SlotType
    bay_id: Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
    technician_id: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^TECH-\d{2}$")]
    status: Literal["open"]

    @property
    def start(self) -> datetime:
        return datetime.combine(self.slot_date, self.slot_start_time)


class Booking(BaseModel):
    """One message booked into one slot. Checks the slot type fits the tag."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    message_id: str
    urgency: Urgency
    fix_path: FixPath
    vehicle_alert_code: str
    slot_id: str
    slot_date: date
    slot_start_time: time
    duration_minutes: int
    slot_type: SlotType
    bay_id: str
    technician_id: str
    same_day: bool  # booked on the booking day

    @model_validator(mode="after")
    def _slot_fits_tag(self) -> "Booking":
        allowed = {t for tier in SLOT_TIERS[self.urgency] for t in tier}
        if self.slot_type not in allowed:
            raise ValueError(f"{self.urgency.value} cannot take a {self.slot_type} slot")
        return self


@dataclass(frozen=True)
class QueueItem:
    """What the booking tool needs to know about one tagged message."""

    message_id: str
    received_at: datetime
    urgency: Urgency
    fix_path: FixPath
    vehicle_alert_code: str


def load_slots(path: Path = DEFAULT_SLOTS) -> tuple[list[Slot], list[RejectedRow]]:
    slots: list[Slot] = []
    rejected: list[RejectedRow] = []
    seen: set[str] = set()
    with open(path, newline="", encoding="utf-8-sig") as f:
        for line, row in enumerate(csv.DictReader(f), start=2):
            raw_id = (row.get("slot_id") or "").strip()
            if None in row:
                rejected.append(RejectedRow(line, raw_id, ["row has more cells than the header"]))
                continue
            try:
                slot = Slot.model_validate({k: v for k, v in row.items() if v is not None})
            except ValidationError as e:
                errs = [f"{'.'.join(map(str, err['loc'])) or 'row'}: {err['msg']}" for err in e.errors()]
                rejected.append(RejectedRow(line, raw_id, errs))
                continue
            if slot.slot_id in seen:
                rejected.append(RejectedRow(line, raw_id, ["duplicate slot_id"]))
                continue
            seen.add(slot.slot_id)
            slots.append(slot)
    return slots, rejected


class BookingTool:
    """Holds the open slots and books one message per call."""

    def __init__(self, slots: list[Slot], booking_day: date | None = None):
        self._open: list[Slot] = sorted(slots, key=lambda s: (s.start, s.slot_id))
        self._taken: set[str] = set()
        # The day safety_urgent should book on. Defaults to the first day in the slot list.
        self.booking_day: date | None = booking_day or (self._open[0].slot_date if self._open else None)

    def remaining(self, slot_type: str | None = None) -> int:
        return sum(1 for s in self._open if s.slot_id not in self._taken
                   and (slot_type is None or s.slot_type == slot_type))

    def book(self, item: QueueItem) -> Booking | None:
        """Book the earliest open slot this message's tag may use, or None if none left."""
        for tier in SLOT_TIERS[item.urgency]:
            slot = next((s for s in self._open if s.slot_id not in self._taken and s.slot_type in tier), None)
            if slot is None:
                continue
            self._taken.add(slot.slot_id)
            return Booking(
                message_id=item.message_id,
                urgency=item.urgency,
                fix_path=item.fix_path,
                vehicle_alert_code=item.vehicle_alert_code,
                slot_id=slot.slot_id,
                slot_date=slot.slot_date,
                slot_start_time=slot.slot_start_time,
                duration_minutes=slot.duration_minutes,
                slot_type=slot.slot_type,
                bay_id=slot.bay_id,
                technician_id=slot.technician_id,
                same_day=slot.slot_date == self.booking_day,
            )
        return None


def queue_order(items: list[QueueItem]) -> list[QueueItem]:
    """safety_urgent, then soon, then routine; oldest first inside each tag."""
    return sorted(items, key=lambda i: (URGENCY_RANK[i.urgency], i.received_at, i.message_id))


def book_all(items: list[QueueItem], slots: list[Slot]) -> tuple[list[Booking], list[QueueItem]]:
    """Book every message in queue order. Returns (bookings, waitlist)."""
    tool = BookingTool(slots)
    bookings: list[Booking] = []
    waitlist: list[QueueItem] = []
    for item in queue_order(items):
        b = tool.book(item)
        (bookings.append(b) if b else waitlist.append(item))
    ids = [b.slot_id for b in bookings]
    assert len(ids) == len(set(ids)), "a slot was booked twice"
    return bookings, waitlist
