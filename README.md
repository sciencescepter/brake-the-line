# Brake the Line: Tesla Service Fault Triage

Tesla Service currently answers owner fault messages in arrival order, so a soft brake pedal can wait days behind wiper and app-login questions. This project replaces that with an urgency-sorted queue. A language model tags each message, a strict Pydantic schema checks every answer, and a booking tool assigns a service slot. Brake and steering faults go to the front.

Project owner: Leilani Oyelaran, Senior Machine Learning Lead, Autopilot Perception.

## Key prompt

The rule that stops a calm, friendly message from hiding a brake or steering fault. It is sent to the model word for word ([triage/prompt.py](triage/prompt.py)):

> "Any message pertaining to the pedal/brake feel, stability, or steering must be tagged safety_urgent, whatever the tone and whatever the vehicle_alert_code. Calm, polite or apologetic wording does not lower the urgency: "no rush", "probably nothing" or "happy to wait" next to a soft pedal, a grinding brake, a pull to one side, heavy or shaky steering, or an unsettled or sliding car is still safety_urgent. When in doubt between safety_urgent and anything else, choose safety_urgent."

The schema enforces the same rule in code, so the prompt is not the only safeguard. If the model tags a brake or steering message `soon` or `routine`, its answer fails validation and goes back for a retry or gets flagged. It is never accepted as it is.

## Urgency rules (Stage 1)

| Urgency tag | Fix path(s) allowed |
|---|---|
| `safety_urgent` | `tow_in`: owner stops driving and the car is towed in |
| `soon` | `service_center_visit`: owner drives the car to a service center |
| `routine` | `mobile_remote_support`: mobile service or remote support |

**Change (17 Nov 2026):** I dropped the fourth fix path, `parts_order_then_visit`, for now, so each tag has exactly one fix path. A fourth path may be added again in a later stage.

**Safety alert list.** These `vehicle_alert_code` values always mean `safety_urgent`: `BRK_a001`, `BRK_w003`, `ABS_w002`, `ESP_w003`, `EPAS_a191`, `EPAS_w202`. The other five codes in the batch (`HVAC_w003`, `UI_a004`, `WIP_w001`, `CP_a004`, `NONE`) are left to the model and the text guard.

**Hidden-safety guard.** [triage/rules.py](triage/rules.py) also has pattern checks for symptoms such as a soft or sinking pedal, grinding through the pedal or wheels when stopping, pulling or tugging to one side, heavy, light or shimmying steering, and an unsettled or sliding car. If the text matches, the message must be `safety_urgent`. The patterns look for symptoms, not keywords, so "brakes feel normal" and wiper grinding do not trigger them.

**Bad records are rejected.** An input row with a missing, blank, extra or wrong-typed field (unknown alert code, bad `message_id`, non-numeric odometer and so on) is rejected and listed. It is never patched. The same goes for duplicate `message_id`s. A model answer with extra keys, an unknown tag, a fix path that doesn't fit its tag, or a non-boolean flag is rejected too.

## Current results

```
rows accepted: 300   rows rejected: 0
forced safety_urgent by alert code: 64
forced safety_urgent by hidden-safety text guard: 41
hand-checked safety messages missed by the rules: 0 of 60
```

## Run it

```bash
python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
.venv/bin/python -m scripts.check_rules   # load batch, check rules against the 60 hand-checked messages
.venv/bin/python -m pytest -q             # schema and guard tests
```

## Layout

```
data/       Overnight Fault Message Batch (16 November 2026).csv
triage/     rules.py (tags, fix paths, safety codes, guard) · schema.py (Pydantic) · prompt.py · load.py
scripts/    check_rules.py
tests/      test_schema.py
```

## Stages

1. Pydantic urgency rules (done)
2. Tagging script and tagged output for every message (free OpenRouter model)
3. Booking tool, service schedule and safety check script
4. Streamlit page
5. Slides and presentation

## Data notes

- The batch has **300** messages (`MSG-10001` to `MSG-10300`), not the 400 in the brief.
- The 60 hand-checked messages are the `hand_checked` / `hand_checked_safety_fault` columns in the batch, not a separate file. All 60 are safety faults. The model never sees these columns.
- There is no Open Service Slots CSV yet. Stage 3 needs one, and its `fix_path` values must match the three paths above.
- The text guard was tuned while looking at the hand-checked set, so 0 of 60 is the best case. The model is the main classifier, and the guard is a backstop.
