"""Urgency rules for Tesla Service fault triage.

Everything the service team decided lives here, so the schema, the prompt and
the scripts all read the same values:

* the three urgency tags
* the four fix paths and which tag each one may serve
* the safety alert list (vehicle_alert_code values that always mean safety_urgent)
* the hidden-safety guard: brake, pedal, stability and steering symptoms in the
  message text that force safety_urgent whatever the tone or alert code
"""

from __future__ import annotations

import re
from enum import Enum


class Urgency(str, Enum):
    SAFETY_URGENT = "safety_urgent"
    SOON = "soon"
    ROUTINE = "routine"


# Queue order: safety_urgent first, then soon, then routine.
URGENCY_RANK: dict[Urgency, int] = {
    Urgency.SAFETY_URGENT: 0,
    Urgency.SOON: 1,
    Urgency.ROUTINE: 2,
}


class FixPath(str, Enum):
    # Owner stops driving and the car is towed in. Only path for safety_urgent.
    TOW_IN = "tow_in"
    # Owner drives the car to a service center.
    SERVICE_CENTER_VISIT = "service_center_visit"
    # Mobile technician visit, or remote support (app, software, over-the-air).
    MOBILE_REMOTE_SUPPORT = "mobile_remote_support"
    # Fourth path: a part has to be ordered before the job can be done, so the
    # booking lands on the first slot after the part is expected
    # (e.g. a wiper arm or charge-port door swap "at my next visit").
    PARTS_ORDER_THEN_VISIT = "parts_order_then_visit"


FIX_PATH_LABELS: dict[FixPath, str] = {
    FixPath.TOW_IN: "Owner stops driving & car is towed in",
    FixPath.SERVICE_CENTER_VISIT: "Service center visit",
    FixPath.MOBILE_REMOTE_SUPPORT: "Mobile service / remote support",
    FixPath.PARTS_ORDER_THEN_VISIT: "Order part, then service visit",
}

# Which fix paths each urgency tag may use. A tag/path pair outside this
# table fails validation.
ALLOWED_FIX_PATHS: dict[Urgency, frozenset[FixPath]] = {
    Urgency.SAFETY_URGENT: frozenset({FixPath.TOW_IN}),
    Urgency.SOON: frozenset({FixPath.SERVICE_CENTER_VISIT, FixPath.PARTS_ORDER_THEN_VISIT}),
    Urgency.ROUTINE: frozenset({FixPath.MOBILE_REMOTE_SUPPORT, FixPath.PARTS_ORDER_THEN_VISIT}),
}

# The 11 distinct vehicle_alert_code values in the 16 Nov 2026 batch.
# Any other value is a wrong field and the record is rejected.
KNOWN_ALERT_CODES: frozenset[str] = frozenset({
    "NONE",
    "BRK_a001", "BRK_w003",   # brake system
    "ABS_w002",               # anti-lock braking
    "ESP_w003",               # stability / traction control
    "EPAS_a191", "EPAS_w202", # electric power steering assist
    "HVAC_w003",              # climate
    "UI_a004",                # touchscreen / infotainment
    "WIP_w001",               # wipers
    "CP_a004",                # charge port
})

# Safety alert list: these codes always mean safety_urgent.
SAFETY_ALERT_CODES: frozenset[str] = frozenset({
    "BRK_a001", "BRK_w003", "ABS_w002", "ESP_w003", "EPAS_a191", "EPAS_w202",
})


# --- Hidden-safety guard ----------------------------------------------------
# Deterministic backstop for the model. Each pattern describes a *symptom*
# (something going wrong), not just a mention of brakes or steering, so
# "brakes feel normal" or "steers fine" do not fire. Patterns stop at a full
# stop so they stay inside one sentence.

_S = r"[^.!?]"  # any character inside the same sentence

HIDDEN_SAFETY_PATTERNS: dict[str, re.Pattern[str]] = {
    name: re.compile(p, re.IGNORECASE)
    for name, p in {
        # Pedal feel: soft, spongy, sinks, goes long, drops to the floor, pulses
        "pedal_feel": (
            rf"\bpedal\b{_S}{{0,60}}?\b(soft|softer|spongy|sinks?|sinking|sank|floor|"
            rf"long|further|pulses?|pulsed|pulsing|drop(s|ped)?|odd|different|firm and then)\b"
        ),
        "soft_pedal": r"\b(soft|spongy|long|sinking)\s+(brake\s+)?pedal\b",
        # Brakes feel wrong
        "brake_feel": (
            rf"\bbrak\w*{_S}{{0,40}}?\b(feel|feels|felt)\s+(a\s+bit\s+|a\s+little\s+)?"
            rf"(different|grabby|odd|soft|spongy|weak|strange|funny|off)\b"
        ),
        # Grinding / scraping while braking or stopping (not wiper parking noise)
        "brake_noise": (
            rf"\b(grind\w*|scrap\w*|squeal\w*)\b{_S}{{0,40}}?\b(when|while|as)\s+"
            rf"(i\s+|i'?m\s+|i\s+am\s+)?(brak\w*|stop\w*)"
        ),
        # Grinding / rubbing felt through the pedal, or heard from the wheels
        "pedal_grind": (
            rf"(\b(grind\w*|rub\w*|scrap\w*)\b{_S}{{0,40}}?\bpedal\b)|"
            rf"(\bpedal\b{_S}{{0,40}}?\b(grind\w*|rub\w*|scrap\w*)\b)"
        ),
        "wheel_grind": rf"\b(grind\w*|scrap\w*)\b{_S}{{0,30}}?\bwheels?\b",
        # Car pulls / tugs / jerks to one side
        "pull_to_side": (
            rf"\b(pull(s|ed|ing)?|tug(s|ged|ging)?|drift(s|ed|ing)?|jerk(s|ed|ing)?|veer(s|ed|ing)?)\b"
            rf"{_S}{{0,30}}?\b(left|right|one side)\b"
        ),
        "pull_on_wheel": r"\bpull on the (steering\s+)?wheel\b",
        "tugs": r"\btug(s|ging)?\b",
        # Steering heavy, light, loose, jerky
        "steering_feel": (
            rf"\bsteering\b{_S}{{0,40}}?\b(heavy|heavier|light|loose|stiff|jerk\w*|"
            rf"vibrat\w*|shak\w*|wobbl\w*|shimm\w*|notchy|stuck)\b"
        ),
        "wheel_feel": (
            r"\bwheel\s+(went|goes|felt|feels|got)\s+(really\s+|very\s+)?(heavy|light|loose|stiff)\b"
        ),
        # Stability: unsettled, loose, sliding, wheels locking
        "unsettled": r"\b(felt|feels|feel)\s+(a\s+bit\s+|a\s+little\s+)?(unsettled|loose)\b",
        "slide": r"\b(slid|skid\w*|fishtail\w*|spun)\b",
        "wheel_lock": rf"\bwheels?\b{_S}{{0,25}}?\block(s|ed|ing)?\b",
    }.items()
}


def hidden_safety_hits(text: str) -> list[str]:
    """Names of the hidden-safety patterns that match the text (empty if none)."""
    return [name for name, pat in HIDDEN_SAFETY_PATTERNS.items() if pat.search(text)]


def required_urgency(alert_code: str, text: str) -> tuple[Urgency | None, str]:
    """The urgency a message *must* get, if a hard rule decides it.

    Returns (Urgency.SAFETY_URGENT, reason) when the alert code is on the safety
    list or the text shows a brake/pedal/stability/steering symptom, otherwise
    (None, "") and the model's tag stands.
    """
    if alert_code in SAFETY_ALERT_CODES:
        return Urgency.SAFETY_URGENT, f"alert code {alert_code} is on the safety alert list"
    hits = hidden_safety_hits(text)
    if hits:
        return Urgency.SAFETY_URGENT, f"hidden safety symptom in text ({', '.join(hits)})"
    return None, ""
