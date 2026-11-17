"""Pydantic models for the fault triage pipeline.

Two models, two jobs:

* FaultMessage  - one row of the Fault Message Batch CSV. A row with a missing,
                  empty, extra or wrong-typed field is rejected, never patched.
* TriageResult  - the language model's answer for one message. It must match
                  the schema exactly, and it is checked against the urgency
                  rules: an answer that tags a safety fault soon/routine is
                  rejected so the caller retries or flags it.
"""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Literal

from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    StrictBool,
    StringConstraints,
    ValidationInfo,
    field_validator,
    model_validator,
)

from .rules import (
    ALLOWED_FIX_PATHS,
    KNOWN_ALERT_CODES,
    FixPath,
    Urgency,
    required_urgency,
)

NonEmptyStr = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
MessageId = Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^MSG-\d{5}$")]


class FaultMessage(BaseModel):
    """One owner fault message, exactly as it arrives in the batch CSV."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    message_id: MessageId
    received_at: datetime
    channel: Literal["mobile_app", "email", "phone", "service_center_walk_in"]
    customer_name: NonEmptyStr
    vehicle_model: Literal["Model 3", "Model Y", "Model S", "Model X"]
    model_year: int = Field(ge=2012, le=2027)
    vin_last6: Annotated[str, StringConstraints(strip_whitespace=True, pattern=r"^[A-Z0-9]{6}$")]
    odometer_km: int = Field(ge=0, le=2_000_000)
    service_center: NonEmptyStr
    vehicle_alert_code: NonEmptyStr
    message_subject: NonEmptyStr
    message_text: NonEmptyStr
    hand_checked: bool
    hand_checked_safety_fault: bool

    @field_validator("vehicle_alert_code")
    @classmethod
    def _known_alert_code(cls, v: str) -> str:
        if v not in KNOWN_ALERT_CODES:
            raise ValueError(f"unknown vehicle_alert_code {v!r}")
        return v

    @model_validator(mode="after")
    def _hand_check_consistent(self) -> "FaultMessage":
        if self.hand_checked_safety_fault and not self.hand_checked:
            raise ValueError("hand_checked_safety_fault is TRUE but hand_checked is FALSE")
        return self

    @property
    def full_text(self) -> str:
        """Subject and body together; the guard and the model both read this."""
        return f"{self.message_subject}. {self.message_text}"


class TriageResult(BaseModel):
    """The model's answer for one message. Strict: no extra keys, no coercion."""

    model_config = ConfigDict(extra="forbid", frozen=True)

    message_id: MessageId
    urgency: Urgency
    fix_path: FixPath
    hidden_safety_symptom: StrictBool = Field(
        description="True if the text describes a brake, pedal, stability or steering symptom."
    )
    reason: Annotated[str, StringConstraints(strip_whitespace=True, min_length=10, max_length=300)]

    @model_validator(mode="after")
    def _apply_urgency_rules(self, info: ValidationInfo) -> "TriageResult":
        # Rule 1: the fix path must be one the urgency tag is allowed to use.
        allowed = ALLOWED_FIX_PATHS[self.urgency]
        if self.fix_path not in allowed:
            names = ", ".join(sorted(p.value for p in allowed))
            raise ValueError(
                f"fix_path {self.fix_path.value!r} not allowed for {self.urgency.value}; use {names}"
            )

        # Rule 2: if the model itself saw a safety symptom, the tag must be safety_urgent.
        if self.hidden_safety_symptom and self.urgency is not Urgency.SAFETY_URGENT:
            raise ValueError("hidden_safety_symptom is true, so urgency must be safety_urgent")

        # Rules 3 and 4 need the source message (pass it as context={"message": msg}).
        msg: FaultMessage | None = (info.context or {}).get("message")
        if msg is not None:
            if self.message_id != msg.message_id:
                raise ValueError(f"message_id {self.message_id} does not match {msg.message_id}")
            must, why = required_urgency(msg.vehicle_alert_code, msg.full_text)
            if must is not None and self.urgency is not must:
                raise ValueError(f"urgency must be {must.value}: {why}")
        return self


def validate_triage(raw_json: str | bytes, message: FaultMessage) -> TriageResult:
    """Parse and check one model answer. Raises pydantic.ValidationError if invalid."""
    return TriageResult.model_validate_json(raw_json, context={"message": message})
