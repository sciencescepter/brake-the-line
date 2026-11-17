"""Stage 2: tag every message in the Fault Message Batch.

Reads the batch, rejects bad rows, asks the model for an urgency tag and fix
path for each message, validates each answer with Pydantic (retry, then flag),
and saves:

    output/tagged_messages.csv    one row per message: urgency, fix path, reason, status
    output/flagged_messages.csv   messages whose answer never passed validation
    output/rejected_rows.csv      input rows rejected for missing or wrong fields
    output/tagging_cache.jsonl    progress log; a rerun skips messages already tagged

    python -m scripts.tag_batch              # tag everything not yet tagged
    python -m scripts.tag_batch --limit 5    # try a few first
    python -m scripts.tag_batch --redo       # ignore the cache and tag everything again
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import threading
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

from dotenv import load_dotenv
from pydantic import ValidationError

from triage.llm import DailyLimitReached, TagOutcome, openrouter_chat, tag_message
from triage.load import DEFAULT_BATCH, load_batch
from triage.rules import FIX_PATH_LABELS, SAFETY_ALERT_CODES, URGENCY_RANK, Urgency, hidden_safety_hits
from triage.schema import FaultMessage, TriageResult

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "output"
CACHE = OUT / "tagging_cache.jsonl"


def rule_source(msg: FaultMessage) -> str:
    """Which hard rule (if any) required safety_urgent for this message."""
    if msg.vehicle_alert_code in SAFETY_ALERT_CODES:
        return "alert_code"
    if hidden_safety_hits(msg.full_text):
        return "text_guard"
    return ""


def load_cache(by_id: dict[str, FaultMessage]) -> dict[str, dict]:
    """Latest cached entry per message. Cached results are re-validated, so a rule
    change since the last run sends the message back to the model."""
    done: dict[str, dict] = {}
    if not CACHE.exists():
        return done
    for line in CACHE.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        entry = json.loads(line)
        msg = by_id.get(entry["message_id"])
        if msg is None or entry["status"] != "ok":
            continue
        try:
            TriageResult.model_validate_json(json.dumps(entry["result"]), context={"message": msg})
        except ValidationError:
            continue
        done[entry["message_id"]] = entry
    return done


def to_entry(o: TagOutcome, model: str) -> dict:
    return {
        "message_id": o.message.message_id,
        "status": "flagged" if o.flagged else "ok",
        "result": o.result.model_dump(mode="json") if o.result else None,
        "attempts": o.attempts,
        "errors": o.errors,
        "model": model,
    }


def write_outputs(messages: list[FaultMessage], entries: dict[str, dict], rejected) -> None:
    OUT.mkdir(exist_ok=True)
    tagged, flagged = [], []
    for m in messages:
        e = entries.get(m.message_id)
        if e is None:
            continue
        if e["status"] == "ok":
            r = e["result"]
            tagged.append({
                "message_id": m.message_id,
                "received_at": m.received_at.isoformat(),
                "service_center": m.service_center,
                "vehicle_alert_code": m.vehicle_alert_code,
                "urgency": r["urgency"],
                "fix_path": r["fix_path"],
                "fix_path_label": FIX_PATH_LABELS[next(p for p in FIX_PATH_LABELS if p.value == r["fix_path"])],
                "hidden_safety_symptom": r["hidden_safety_symptom"],
                "rule_required_safety": rule_source(m),
                "attempts": e["attempts"],
                "reason": r["reason"],
                "message_subject": m.message_subject,
            })
        else:
            flagged.append({
                "message_id": m.message_id,
                "vehicle_alert_code": m.vehicle_alert_code,
                "rule_required_safety": rule_source(m),
                "attempts": e["attempts"],
                "errors": " | ".join(e["errors"]),
                "message_text": m.message_text,
            })

    # Urgency order: safety_urgent, soon, routine; oldest message first inside each tag.
    tagged.sort(key=lambda r: (URGENCY_RANK[Urgency(r["urgency"])], r["received_at"], r["message_id"]))

    def dump(path: Path, rows: list[dict], fields: list[str]) -> None:
        with open(path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=fields)
            w.writeheader()
            w.writerows(rows)

    dump(OUT / "tagged_messages.csv", tagged, [
        "message_id", "received_at", "service_center", "vehicle_alert_code", "urgency", "fix_path",
        "fix_path_label", "hidden_safety_symptom", "rule_required_safety", "attempts", "reason",
        "message_subject",
    ])
    dump(OUT / "flagged_messages.csv", flagged, [
        "message_id", "vehicle_alert_code", "rule_required_safety", "attempts", "errors", "message_text",
    ])
    dump(OUT / "rejected_rows.csv", [
        {"line": r.line, "message_id": r.message_id, "errors": "; ".join(r.errors)} for r in rejected
    ], ["line", "message_id", "errors"])

    # Summary
    urg = Counter(r["urgency"] for r in tagged)
    paths = Counter(r["fix_path_label"] for r in tagged)
    retried = sum(1 for r in tagged if int(r["attempts"]) > 1)
    hand = [m for m in messages if m.hand_checked_safety_fault]
    tag_of = {r["message_id"]: r["urgency"] for r in tagged}
    missed = [m.message_id for m in hand if tag_of.get(m.message_id) != Urgency.SAFETY_URGENT.value]

    print(f"\nRows in batch: {len(messages) + len(rejected)}  rejected: {len(rejected)}")
    print(f"Tagged and validated: {len(tagged)} of {len(messages)}   flagged: {len(flagged)}"
          f"   needed a retry: {retried}")
    print("By urgency:  " + ", ".join(f"{u.value} {urg.get(u.value, 0)}" for u in Urgency))
    print("By fix path: " + ", ".join(f"{k} {v}" for k, v in paths.most_common()))
    print(f"Hand-checked safety messages not tagged safety_urgent: {len(missed)} of {len(hand)}"
          + (f"  {missed}" if missed else ""))
    print(f"Saved to {OUT.relative_to(ROOT)}/")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--batch", type=Path, default=DEFAULT_BATCH)
    ap.add_argument("--limit", type=int, help="only tag this many new messages")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--redo", action="store_true", help="ignore the cache and tag everything again")
    args = ap.parse_args()

    load_dotenv(ROOT / ".env")
    messages, rejected = load_batch(args.batch)
    by_id = {m.message_id: m for m in messages}
    OUT.mkdir(exist_ok=True)
    if args.redo and CACHE.exists():
        CACHE.unlink()

    entries = load_cache(by_id)
    todo = [m for m in messages if m.message_id not in entries]
    if args.limit is not None:
        todo = todo[: args.limit]

    if todo:
        chat = openrouter_chat()
        model = getattr(chat, "model", "")
        print(f"Tagging {len(todo)} messages with {model} ({len(entries)} already done)")
        lock = threading.Lock()
        stopped = False
        with ThreadPoolExecutor(max_workers=args.workers) as pool, open(CACHE, "a", encoding="utf-8") as log:
            futures = {pool.submit(tag_message, m, chat): m for m in todo}
            for i, fut in enumerate(as_completed(futures), start=1):
                try:
                    outcome = fut.result()
                except DailyLimitReached:
                    if not stopped:
                        print("  Daily request limit reached. Progress is saved; run again later to continue.")
                        stopped = True
                        for f in futures:
                            f.cancel()
                    continue
                entry = to_entry(outcome, model)
                with lock:
                    log.write(json.dumps(entry) + "\n")
                    log.flush()
                    entries[entry["message_id"]] = entry
                mark = "ok" if entry["status"] == "ok" else "FLAGGED"
                tag = entry["result"]["urgency"] if entry["result"] else "-"
                print(f"  [{i}/{len(todo)}] {entry['message_id']} {mark} {tag} (attempts {entry['attempts']})",
                      flush=True)

    write_outputs(messages, entries, rejected)
    return 0


if __name__ == "__main__":
    sys.exit(main())
