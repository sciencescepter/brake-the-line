"""Safety check: compare the model's tags with the 60 hand-checked safety messages.

Ground truth is the hand_checked_safety_fault column in the Fault Message Batch.
Any hand-checked safety fault tagged soon or routine (or not tagged at all) is a miss.
"""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from .rules import SAFETY_ALERT_CODES, Urgency, hidden_safety_hits
from .schema import FaultMessage

ROOT = Path(__file__).resolve().parent.parent
TAGGED = ROOT / "output" / "tagged_messages.csv"


@dataclass(frozen=True)
class CheckRow:
    message_id: str
    vehicle_alert_code: str
    tag: str            # urgency given, or "" if the message was never tagged
    caught_by: str      # "alert code", "hidden-safety text", or "model only"
    subject: str

    @property
    def missed(self) -> bool:
        return self.tag != Urgency.SAFETY_URGENT.value


@dataclass(frozen=True)
class SafetyReport:
    rows: list[CheckRow]                 # one per hand-checked safety message
    extra_safety: list[str]              # tagged safety_urgent but not in the hand-checked set

    @property
    def misses(self) -> list[CheckRow]:
        return [r for r in self.rows if r.missed]


def load_tags(path: Path = TAGGED) -> dict[str, dict]:
    with open(path, newline="", encoding="utf-8") as f:
        return {r["message_id"]: r for r in csv.DictReader(f)}


def run_check(messages: list[FaultMessage], tags: dict[str, dict]) -> SafetyReport:
    rows = []
    for m in messages:
        if not m.hand_checked_safety_fault:
            continue
        if m.vehicle_alert_code in SAFETY_ALERT_CODES:
            caught = "alert code"
        elif hidden_safety_hits(m.full_text):
            caught = "hidden-safety text"
        else:
            caught = "model only"
        rows.append(CheckRow(m.message_id, m.vehicle_alert_code,
                             tags.get(m.message_id, {}).get("urgency", ""), caught, m.message_subject))
    hand_ids = {m.message_id for m in messages if m.hand_checked_safety_fault}
    extra = sorted(mid for mid, t in tags.items()
                   if t["urgency"] == Urgency.SAFETY_URGENT.value and mid not in hand_ids)
    return SafetyReport(rows, extra)
