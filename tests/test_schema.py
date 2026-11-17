import json

import pytest
from pydantic import ValidationError

from triage.load import load_batch
from triage.rules import Urgency, hidden_safety_hits
from triage.schema import FaultMessage, validate_triage

ROW = {
    "message_id": "MSG-10002",
    "received_at": "2026-11-15T18:19:00",
    "channel": "email",
    "customer_name": "Test Owner",
    "vehicle_model": "Model 3",
    "model_year": "2021",
    "vin_last6": "9KD013",
    "odometer_km": "61280",
    "service_center": "San Jose Service Center",
    "vehicle_alert_code": "NONE",
    "message_subject": "pedal feels soft lately",
    "message_text": (
        "Hello, no rush at all, the car is generally lovely. Only thing is the brake pedal "
        "feels a bit softer than it used to, and on the off-ramp it sinks a little further "
        "before it bites. Happy to wait for whatever slot suits you. Thanks."
    ),
    "hand_checked": "TRUE",
    "hand_checked_safety_fault": "TRUE",
}


def answer(**over):
    base = {
        "message_id": "MSG-10002",
        "urgency": "safety_urgent",
        "fix_path": "tow_in",
        "hidden_safety_symptom": True,
        "reason": "Soft brake pedal that sinks further before biting.",
    }
    base.update(over)
    return json.dumps(base)


# --- input records ---------------------------------------------------------

def test_valid_row_loads():
    assert FaultMessage.model_validate(ROW).hand_checked_safety_fault is True


@pytest.mark.parametrize("field", ["message_id", "message_text", "vehicle_alert_code"])
def test_missing_field_rejected(field):
    row = {k: v for k, v in ROW.items() if k != field}
    with pytest.raises(ValidationError):
        FaultMessage.model_validate(row)


@pytest.mark.parametrize(
    "field,value",
    [
        ("message_text", "   "),
        ("message_id", "10002"),
        ("vehicle_alert_code", "BRK_x999"),
        ("vehicle_model", "Cybertruck"),
        ("odometer_km", "lots"),
        ("vin_last6", "abc"),
    ],
)
def test_wrong_field_rejected(field, value):
    with pytest.raises(ValidationError):
        FaultMessage.model_validate({**ROW, field: value})


def test_extra_field_rejected():
    with pytest.raises(ValidationError):
        FaultMessage.model_validate({**ROW, "priority": "high"})


def test_whole_batch_loads_clean():
    messages, rejected = load_batch()
    assert rejected == []
    assert len({m.message_id for m in messages}) == len(messages)


# --- model answers -----------------------------------------------------------

MSG = FaultMessage.model_validate(ROW)


def test_correct_answer_passes():
    assert validate_triage(answer(), MSG).urgency is Urgency.SAFETY_URGENT


def test_calm_brake_message_cannot_be_routine():
    # The primary risk: a friendly message with a soft pedal tagged routine.
    bad = answer(urgency="routine", fix_path="mobile_remote_support", hidden_safety_symptom=False)
    with pytest.raises(ValidationError, match="must be safety_urgent"):
        validate_triage(bad, MSG)


def test_safety_alert_code_forces_safety_urgent():
    msg = FaultMessage.model_validate(
        {**ROW, "vehicle_alert_code": "EPAS_w202", "message_text": "A warning chime went off once."}
    )
    with pytest.raises(ValidationError, match="safety alert list"):
        validate_triage(answer(urgency="soon", fix_path="service_center_visit", hidden_safety_symptom=False), msg)


def test_fix_path_must_match_urgency():
    with pytest.raises(ValidationError, match="not allowed"):
        validate_triage(answer(fix_path="service_center_visit"), MSG)


def test_extra_key_and_bad_enum_rejected():
    with pytest.raises(ValidationError):
        validate_triage(json.dumps({**json.loads(answer()), "confidence": 0.9}), MSG)
    with pytest.raises(ValidationError):
        validate_triage(answer(urgency="urgent"), MSG)


def test_hidden_safety_flag_must_be_strict_bool():
    with pytest.raises(ValidationError):
        validate_triage(answer(hidden_safety_symptom="yes"), MSG)


def test_wrong_message_id_rejected():
    with pytest.raises(ValidationError, match="does not match"):
        validate_triage(answer(message_id="MSG-10003"), MSG)


# --- hidden-safety guard -----------------------------------------------------

@pytest.mark.parametrize(
    "text",
    [
        "The wiper arm makes a horrible grinding noise every time it parks.",
        "There is a clunk over bumps but the brakes feel normal and it steers fine.",
        "Tyre pressure light came on. Pedal and steering feel completely normal.",
        "The rear door handle sticks and needs two pulls to open.",
    ],
)
def test_guard_ignores_non_symptoms(text):
    assert hidden_safety_hits(text) == []


@pytest.mark.parametrize(
    "text",
    [
        "No rush, but the brake pedal sinks a little further before it bites.",
        "Every time I stop at a red light I feel a grinding through the brake pedal.",
        "The car tugs to the left when stopping at lights.",
        "The steering wheel starts to shimmy in my hands at 110 km/h.",
        "There's a grinding noise from the front wheels when I'm stopped at the lights.",
    ],
)
def test_guard_catches_calm_symptoms(text):
    assert hidden_safety_hits(text)


def test_broken_csv_rows_rejected(tmp_path):
    header = ",".join(ROW)
    good = ",".join(f'"{v}"' for v in ROW.values())
    blank_text = ",".join('""' if k == "message_text" else f'"{v}"' for k, v in ROW.items())
    extra_cell = good + ',"surplus"'
    dup = good
    p = tmp_path / "batch.csv"
    p.write_text("\n".join([header, good, blank_text.replace("MSG-10002", "MSG-10009"), extra_cell, dup]) + "\n")
    messages, rejected = load_batch(p)
    assert [m.message_id for m in messages] == ["MSG-10002"]
    assert [r.line for r in rejected] == [3, 4, 5]
