"""Load the Fault Message Batch CSV into validated FaultMessage records."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

from pydantic import ValidationError

from .schema import FaultMessage

DEFAULT_BATCH = Path(__file__).resolve().parent.parent / "data" / "Overnight Fault Message Batch (16 November 2026).csv"


@dataclass(frozen=True)
class RejectedRow:
    line: int            # line number in the CSV (header is line 1)
    message_id: str      # as written in the row, may be blank
    errors: list[str]


def load_batch(path: Path = DEFAULT_BATCH) -> tuple[list[FaultMessage], list[RejectedRow]]:
    """Return (valid messages, rejected rows). Bad rows are rejected, never repaired."""
    accepted: list[FaultMessage] = []
    rejected: list[RejectedRow] = []
    seen: set[str] = set()

    with open(path, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        for line, row in enumerate(reader, start=2):
            raw_id = (row.get("message_id") or "").strip()
            # csv puts surplus cells under the key None; a short row gives None values.
            if None in row:
                rejected.append(RejectedRow(line, raw_id, ["row has more cells than the header"]))
                continue
            data = {k: v for k, v in row.items() if v is not None}
            try:
                msg = FaultMessage.model_validate(data)
            except ValidationError as e:
                errs = [f"{'.'.join(map(str, err['loc'])) or 'row'}: {err['msg']}" for err in e.errors()]
                rejected.append(RejectedRow(line, raw_id, errs))
                continue
            if msg.message_id in seen:
                rejected.append(RejectedRow(line, raw_id, ["duplicate message_id"]))
                continue
            seen.add(msg.message_id)
            accepted.append(msg)
    return accepted, rejected
