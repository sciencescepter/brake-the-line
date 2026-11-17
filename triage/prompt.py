"""Prompt for the tagging model.

The model sees the message text, subject and alert code only. The hand_checked
columns are the answer key for the safety check, so they are never sent.
"""

from __future__ import annotations

import json

from .rules import FIX_PATH_LABELS, SAFETY_ALERT_CODES, FixPath
from .schema import FaultMessage

# The hidden-safety rule. Quoted word for word in README.md.
HIDDEN_SAFETY_RULE = (
    "Any message pertaining to the pedal/brake feel, stability, or steering must be "
    "tagged safety_urgent, whatever the tone and whatever the vehicle_alert_code. "
    "Calm, polite or apologetic wording does not lower the urgency: \"no rush\", "
    "\"probably nothing\" or \"happy to wait\" next to a soft pedal, a grinding brake, "
    "a pull to one side, heavy or shaky steering, or an unsettled or sliding car is "
    "still safety_urgent. When in doubt between safety_urgent and anything else, "
    "choose safety_urgent."
)

SYSTEM_PROMPT = f"""You triage Tesla owner fault messages for Tesla Service.
Read one message and return a JSON object that matches the schema exactly. No other text.

Urgency tags:
- safety_urgent: a brake, pedal, stability or steering fault. The owner should stop driving.
- soon: a fault that affects use of the car and needs a service visit, but is not a safety fault.
- routine: comfort, cosmetic, app, screen or convenience issues.

Fix paths (each tag may only use its own paths):
- "{FixPath.TOW_IN.value}" ({FIX_PATH_LABELS[FixPath.TOW_IN]}): safety_urgent only.
- "{FixPath.SERVICE_CENTER_VISIT.value}" ({FIX_PATH_LABELS[FixPath.SERVICE_CENTER_VISIT]}): soon.
- "{FixPath.MOBILE_REMOTE_SUPPORT.value}" ({FIX_PATH_LABELS[FixPath.MOBILE_REMOTE_SUPPORT]}): routine.
- "{FixPath.PARTS_ORDER_THEN_VISIT.value}" ({FIX_PATH_LABELS[FixPath.PARTS_ORDER_THEN_VISIT]}): soon or routine,
  when a part must be ordered before the job (e.g. "swap the wiper arm at my next visit").

Safety alert codes. If vehicle_alert_code is one of these, the tag is safety_urgent:
{", ".join(sorted(SAFETY_ALERT_CODES))}

Hidden-safety rule:
{HIDDEN_SAFETY_RULE}
Set hidden_safety_symptom to true whenever the text itself describes such a symptom.
Words like "brakes feel normal" or "steers fine" are not symptoms.

Return exactly these keys:
{{"message_id": "<copy from input>", "urgency": "safety_urgent|soon|routine",
  "fix_path": "<one fix path>", "hidden_safety_symptom": true|false,
  "reason": "<one sentence, 10-300 characters, naming the symptom that decided the tag>"}}"""


def user_prompt(msg: FaultMessage) -> str:
    """The per-message input. Only the fields the model needs; no answer key."""
    return json.dumps(
        {
            "message_id": msg.message_id,
            "vehicle_alert_code": msg.vehicle_alert_code,
            "message_subject": msg.message_subject,
            "message_text": msg.message_text,
        },
        ensure_ascii=False,
    )


def retry_prompt(error_text: str) -> str:
    """Sent back to the model when its answer failed validation."""
    return (
        "Your answer failed validation:\n"
        f"{error_text}\n"
        "Return a corrected JSON object only."
    )
