"""Compare the tags in output/tagged_messages.csv with the 60 hand-checked
safety messages and list any misses. Exit code 1 if anything was missed.

    python -m scripts.safety_check
"""

from __future__ import annotations

from triage.load import load_batch
from triage.safety_check import load_tags, run_check


def main() -> int:
    messages, _ = load_batch()
    report = run_check(messages, load_tags())
    n = len(report.rows)
    print(f"Hand-checked safety messages: {n}")
    print(f"Tagged safety_urgent:         {n - len(report.misses)}")
    print(f"Missed (soon/routine/untagged): {len(report.misses)} of {n}")
    for r in report.misses:
        print(f"  MISS {r.message_id} [{r.vehicle_alert_code}] tagged {r.tag or 'nothing'}: {r.subject}")
    print(f"Also tagged safety_urgent outside the hand-checked set: {len(report.extra_safety)}")
    return 1 if report.misses else 0


if __name__ == "__main__":
    raise SystemExit(main())
