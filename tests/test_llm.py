import json

from triage.llm import tag_message
from triage.rules import Urgency
from triage.schema import FaultMessage

from .test_schema import ROW

MSG = FaultMessage.model_validate(ROW)  # calm message with a soft brake pedal

GOOD = json.dumps({
    "message_id": "MSG-10002", "urgency": "safety_urgent", "fix_path": "tow_in",
    "hidden_safety_symptom": True, "reason": "Soft brake pedal that sinks before biting.",
})
ROUTINE = json.dumps({
    "message_id": "MSG-10002", "urgency": "routine", "fix_path": "mobile_remote_support",
    "hidden_safety_symptom": False, "reason": "Owner says there is no rush at all.",
})


def scripted(*answers):
    calls = []

    def chat(messages):
        calls.append(messages)
        return answers[len(calls) - 1]

    return chat, calls


def test_valid_first_answer_accepted():
    chat, calls = scripted(GOOD)
    out = tag_message(MSG, chat)
    assert out.result.urgency is Urgency.SAFETY_URGENT and out.attempts == 1 and len(calls) == 1


def test_wrong_tag_is_retried_with_the_error():
    chat, calls = scripted(ROUTINE, GOOD)
    out = tag_message(MSG, chat)
    assert out.result.urgency is Urgency.SAFETY_URGENT and out.attempts == 2
    assert "must be safety_urgent" in calls[1][-1]["content"]


def test_never_valid_is_flagged_not_accepted():
    chat, _ = scripted(ROUTINE, "not json", ROUTINE)
    out = tag_message(MSG, chat)
    assert out.flagged and out.result is None and len(out.errors) == 3


def test_api_error_counts_as_attempt(monkeypatch):
    monkeypatch.setattr("triage.llm.time.sleep", lambda s: None)
    n = {"i": 0}

    def chat(messages):
        n["i"] += 1
        if n["i"] == 1:
            raise TimeoutError("slow")
        return GOOD

    out = tag_message(MSG, chat)
    assert out.result is not None and out.attempts == 2


def test_code_fences_are_tolerated():
    chat, _ = scripted(f"```json\n{GOOD}\n```")
    assert tag_message(MSG, chat).result is not None


def test_daily_limit_stops_instead_of_flagging():
    import pytest
    from triage.llm import DailyLimitReached

    def chat(messages):
        raise RuntimeError("Error code: 429 - Rate limit exceeded: free-models-per-day")

    with pytest.raises(DailyLimitReached):
        tag_message(MSG, chat)
