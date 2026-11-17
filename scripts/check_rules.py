"""Stage 1 check: load the batch, reject bad rows, and test the hard urgency rules
against the 60 hand-checked safety messages.

    python -m scripts.check_rules [path/to/batch.csv]
"""

from __future__ import annotations

import sys
from collections import Counter
from pathlib import Path

from triage.load import DEFAULT_BATCH, load_batch
from triage.rules import SAFETY_ALERT_CODES, Urgency, required_urgency


def main() -> int:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_BATCH
    messages, rejected = load_batch(path)

    print(f"Batch: {path.name}")
    print(f"  rows accepted: {len(messages)}")
    print(f"  rows rejected: {len(rejected)}")
    for r in rejected:
        print(f"    line {r.line} {r.message_id or '(no id)'}: {'; '.join(r.errors)}")

    codes = Counter(m.vehicle_alert_code for m in messages)
    print(f"\nDistinct vehicle_alert_code values: {len(codes)}")
    for code, n in sorted(codes.items()):
        flag = "  <- safety alert list" if code in SAFETY_ALERT_CODES else ""
        print(f"  {code:10} {n:4}{flag}")

    by_code = by_text = 0
    misses = []
    for m in messages:
        must, why = required_urgency(m.vehicle_alert_code, m.full_text)
        if must is Urgency.SAFETY_URGENT:
            if m.vehicle_alert_code in SAFETY_ALERT_CODES:
                by_code += 1
            else:
                by_text += 1
        if m.hand_checked_safety_fault and must is not Urgency.SAFETY_URGENT:
            misses.append(m)

    hand = [m for m in messages if m.hand_checked]
    print("\nHard rules (before the model runs):")
    print(f"  forced safety_urgent by alert code: {by_code}")
    print(f"  forced safety_urgent by hidden-safety text guard: {by_text}")
    print(f"  hand-checked safety messages missed by the rules: {len(misses)} of {len(hand)}")
    for m in misses:
        print(f"    {m.message_id}: {m.message_text[:100]}")

    return 1 if (misses or rejected) else 0


if __name__ == "__main__":
    raise SystemExit(main())
