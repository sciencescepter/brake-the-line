# Service Booking Report: week of 16 to 21 November 2026

Generated 17 Nov 2026 18:38 by `scripts/book_queue.py`. Booking day: **Mon 16 Nov 2026** (first day in the slot list).

| Processed | safety_urgent | soon | routine | Booked | Waitlist | Safety faults missed |
|---|---|---|---|---|---|---|
| 300 of 300 | 105 | 9 | 186 | 300 of 300 | 0 | **0 of 60** |

## Safety check: tags vs the 60 hand-checked safety messages

The service team hand-checked 60 messages and marked all of them as safety faults. A hand-checked message tagged `soon` or `routine` counts as a miss.

| Result | Count |
|---|---|
| Hand-checked safety faults | 60 |
| Tagged `safety_urgent` | 60 |
| **Missed (tagged soon / routine / untagged)** | **0** |
| Caught with a safety alert code | 23 |
| Caught with no safety code (calm or hidden symptom in the text) | 37 |
| Tagged `safety_urgent` outside the hand-checked set | 45 |

**No misses.** Every hand-checked safety fault is tagged `safety_urgent`, including the calm, friendly messages with a brake or steering symptom and no alert code.

The 45 extra `safety_urgent` messages either carry a safety alert code or describe a brake, pedal, stability or steering symptom. They weren't in the hand-checked sample, so they can't count as misses or false alarms.

<details><summary>All 60 hand-checked messages</summary>

| Message | Alert code | Tag given | Caught by | Subject |
|---|---|---|---|---|
| MSG-10002 | NONE | safety_urgent | hidden-safety text | pedal feels soft lately |
| MSG-10003 | ABS_w002 | safety_urgent | alert code | ABS light came on this morning |
| MSG-10012 | BRK_w003 | safety_urgent | alert code | brake warning light on dash |
| MSG-10013 | NONE | safety_urgent | hidden-safety text | grinding when I stop at lights |
| MSG-10024 | BRK_w003 | safety_urgent | alert code | brake warning and pedal feel off |
| MSG-10027 | ABS_w002 | safety_urgent | alert code | ABS light and stability warning came on at speed |
| MSG-10032 | NONE | safety_urgent | hidden-safety text | quick question about a pull |
| MSG-10036 | NONE | safety_urgent | hidden-safety text | grinding at the lights |
| MSG-10039 | EPAS_w202 | safety_urgent | alert code | steering wheel feels heavy then light on ramps |
| MSG-10045 | BRK_w003 | safety_urgent | alert code | brake pedal sinks and brake warning on dash |
| MSG-10050 | NONE | safety_urgent | hidden-safety text | soft pedal since this afternoon |
| MSG-10057 | ABS_w002 | safety_urgent | alert code | ABS light came on this morning |
| MSG-10062 | NONE | safety_urgent | hidden-safety text | pulls to the left when stopping |
| MSG-10069 | NONE | safety_urgent | hidden-safety text | grinding at the lights |
| MSG-10076 | NONE | safety_urgent | hidden-safety text | soft pedal on the way to work |
| MSG-10082 | BRK_w003 | safety_urgent | alert code | brake warning came on at the lights |
| MSG-10083 | NONE | safety_urgent | hidden-safety text | quick question about the car pulling |
| MSG-10091 | NONE | safety_urgent | hidden-safety text | steering pulls when braking |
| MSG-10093 | BRK_a001 | safety_urgent | alert code | brake fluid level warning |
| MSG-10101 | NONE | safety_urgent | hidden-safety text | steering feels odd at low speed |
| MSG-10103 | ESP_w003 | safety_urgent | alert code | stability light flashing on the motorway |
| MSG-10107 | EPAS_a191 | safety_urgent | alert code | steering assist fault shown at desk |
| MSG-10124 | BRK_w003 | safety_urgent | alert code | brake warning light on after the freeway |
| MSG-10127 | NONE | safety_urgent | hidden-safety text | pedal feels soft this evening |
| MSG-10132 | NONE | safety_urgent | hidden-safety text | car pulls to the left when stopping |
| MSG-10135 | ABS_w002 | safety_urgent | alert code | ABS light came on this morning |
| MSG-10140 | NONE | safety_urgent | hidden-safety text | grinding at the lights |
| MSG-10149 | NONE | safety_urgent | hidden-safety text | soft pedal since last Tuesday |
| MSG-10153 | NONE | safety_urgent | hidden-safety text | steering pulls a bit |
| MSG-10157 | BRK_w003 | safety_urgent | alert code | brake warning light |
| MSG-10160 | EPAS_w202 | safety_urgent | alert code | steering wheel feels heavy |
| MSG-10163 | ABS_w002 | safety_urgent | alert code | ABS and brake light together |
| MSG-10165 | NONE | safety_urgent | hidden-safety text | quick question about a noise |
| MSG-10169 | BRK_a001 | safety_urgent | alert code | brake pedal soft |
| MSG-10170 | NONE | safety_urgent | hidden-safety text | steering a bit off |
| MSG-10174 | NONE | safety_urgent | hidden-safety text | soft pedal on the way down from Skyline |
| MSG-10187 | EPAS_w202 | safety_urgent | alert code | steering wheel warning on the screen |
| MSG-10189 | NONE | safety_urgent | hidden-safety text | pedal goes soft after a long drive |
| MSG-10196 | BRK_a001 | safety_urgent | alert code | brake pedal went to floor once |
| MSG-10198 | NONE | safety_urgent | hidden-safety text | pedal feels a bit soft lately |
| MSG-10202 | BRK_w003 | safety_urgent | alert code | brake warning and spongy pedal |
| MSG-10205 | EPAS_w202 | safety_urgent | alert code | steering heavy at parking speed |
| MSG-10208 | NONE | safety_urgent | hidden-safety text | grinding at the lights |
| MSG-10219 | NONE | safety_urgent | hidden-safety text | wheel shimmy at highway speed |
| MSG-10223 | NONE | safety_urgent | hidden-safety text | soft pedal since yesterday |
| MSG-10226 | NONE | safety_urgent | hidden-safety text | advisor note car pulls left |
| MSG-10230 | NONE | safety_urgent | hidden-safety text | stiff steering at low speed |
| MSG-10234 | BRK_a001 | safety_urgent | alert code | brake pedal fault message |
| MSG-10240 | NONE | safety_urgent | hidden-safety text | pedal feels odd lately |
| MSG-10245 | NONE | safety_urgent | hidden-safety text | car drifts when braking hard |
| MSG-10248 | NONE | safety_urgent | hidden-safety text | pedal feels soft this week |
| MSG-10253 | NONE | safety_urgent | hidden-safety text | car tugs left when I stop |
| MSG-10265 | EPAS_a191 | safety_urgent | alert code | steering stiff at low speed |
| MSG-10269 | NONE | safety_urgent | hidden-safety text | drifts right when braking downhill |
| MSG-10274 | NONE | safety_urgent | hidden-safety text | pulling on stops |
| MSG-10278 | NONE | safety_urgent | hidden-safety text | steering feels loose |
| MSG-10286 | NONE | safety_urgent | hidden-safety text | polite note about pedal |
| MSG-10292 | NONE | safety_urgent | hidden-safety text | sorry for the delay |
| MSG-10296 | NONE | safety_urgent | hidden-safety text | pedal feels a bit soft lately |
| MSG-10299 | NONE | safety_urgent | hidden-safety text | wheel tugging at stops |

</details>

## Booking checks

- **No slot booked twice:** 300 bookings use 300 different slots.
- **safety_urgent same day:** 24 of 105 booked on Mon 16 Nov. The service center bays ran out, so the rest carried over to the earliest bays on the following days: Tue 17 Nov 34, Wed 18 Nov 42, Thu 19 Nov 5.
- **Order:** every safety_urgent booking comes before soon and routine. soon took the 9 next bays. routine filled remote/OTA and callback slots, then mobile visits, then spare bays: Mobile service visit 64, Service center bay 60, Remote / OTA diagnostic 38, Support callback 24.
- **Rejected input rows:** 0 messages, 0 slots. **Untagged messages:** 0. **Waitlist:** 0.

## Booking page

In queue order: safety_urgent first, then soon, then routine. Oldest message first within each tag.

| # | Message | Time slot | Slot type | Issue type (alert code) | Tag | Fix path |
|---|---|---|---|---|---|---|
| 1 | MSG-10198 | Mon 16 Nov 07:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 2 | MSG-10050 | Mon 16 Nov 08:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 3 | MSG-10002 | Mon 16 Nov 09:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 4 | MSG-10100 | Mon 16 Nov 10:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 5 | MSG-10101 | Mon 16 Nov 10:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 6 | MSG-10003 | Mon 16 Nov 11:00 (120 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 7 | MSG-10200 | Mon 16 Nov 11:00 (90 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 8 | MSG-10296 | Mon 16 Nov 13:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 9 | MSG-10103 | Mon 16 Nov 13:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 10 | MSG-10297 | Mon 16 Nov 13:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 11 | MSG-10202 | Mon 16 Nov 14:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 12 | MSG-10006 | Mon 16 Nov 14:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 13 | MSG-10027 | Mon 16 Nov 14:00 (90 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 14 | MSG-10299 | Mon 16 Nov 15:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 15 | MSG-10107 | Mon 16 Nov 15:00 (60 min) | Service center bay | EPAS_a191 | safety_urgent | Owner stops driving & car is towed in |
| 16 | MSG-10057 | Mon 16 Nov 15:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 17 | MSG-10205 | Mon 16 Nov 15:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 18 | MSG-10009 | Mon 16 Nov 16:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 19 | MSG-10032 | Mon 16 Nov 16:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 20 | MSG-10110 | Mon 16 Nov 16:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 21 | MSG-10062 | Mon 16 Nov 17:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 22 | MSG-10036 | Mon 16 Nov 17:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 23 | MSG-10112 | Mon 16 Nov 17:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 24 | MSG-10208 | Mon 16 Nov 17:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 25 | MSG-10012 | Tue 17 Nov 07:00 (120 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 26 | MSG-10114 | Tue 17 Nov 08:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 27 | MSG-10013 | Tue 17 Nov 08:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 28 | MSG-10039 | Tue 17 Nov 09:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 29 | MSG-10066 | Tue 17 Nov 09:00 (90 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 30 | MSG-10124 | Tue 17 Nov 10:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 31 | MSG-10211 | Tue 17 Nov 10:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 32 | MSG-10076 | Tue 17 Nov 10:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 33 | MSG-10127 | Tue 17 Nov 11:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 34 | MSG-10079 | Tue 17 Nov 11:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 35 | MSG-10117 | Tue 17 Nov 11:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 36 | MSG-10069 | Tue 17 Nov 13:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 37 | MSG-10016 | Tue 17 Nov 13:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 38 | MSG-10082 | Tue 17 Nov 13:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 39 | MSG-10132 | Tue 17 Nov 13:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 40 | MSG-10083 | Tue 17 Nov 14:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 41 | MSG-10119 | Tue 17 Nov 14:00 (60 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 42 | MSG-10149 | Tue 17 Nov 14:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 43 | MSG-10135 | Tue 17 Nov 14:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 44 | MSG-10018 | Tue 17 Nov 14:00 (60 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 45 | MSG-10045 | Tue 17 Nov 15:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 46 | MSG-10151 | Tue 17 Nov 15:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 47 | MSG-10087 | Tue 17 Nov 15:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 48 | MSG-10140 | Tue 17 Nov 15:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 49 | MSG-10153 | Tue 17 Nov 15:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 50 | MSG-10073 | Tue 17 Nov 16:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 51 | MSG-10154 | Tue 17 Nov 16:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 52 | MSG-10091 | Tue 17 Nov 16:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 53 | MSG-10048 | Tue 17 Nov 16:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 54 | MSG-10093 | Tue 17 Nov 16:00 (60 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 55 | MSG-10144 | Tue 17 Nov 17:00 (120 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 56 | MSG-10157 | Tue 17 Nov 17:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 57 | MSG-10218 | Tue 17 Nov 17:00 (90 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 58 | MSG-10223 | Tue 17 Nov 17:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 59 | MSG-10096 | Wed 18 Nov 07:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 60 | MSG-10174 | Wed 18 Nov 07:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 61 | MSG-10224 | Wed 18 Nov 08:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 62 | MSG-10022 | Wed 18 Nov 08:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 63 | MSG-10160 | Wed 18 Nov 08:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 64 | MSG-10176 | Wed 18 Nov 09:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 65 | MSG-10219 | Wed 18 Nov 09:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 66 | MSG-10226 | Wed 18 Nov 09:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 67 | MSG-10163 | Wed 18 Nov 09:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 68 | MSG-10178 | Wed 18 Nov 10:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 69 | MSG-10165 | Wed 18 Nov 10:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 70 | MSG-10180 | Wed 18 Nov 10:00 (90 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 71 | MSG-10229 | Wed 18 Nov 10:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 72 | MSG-10248 | Wed 18 Nov 11:00 (120 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 73 | MSG-10230 | Wed 18 Nov 11:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 74 | MSG-10024 | Wed 18 Nov 11:00 (60 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 75 | MSG-10249 | Wed 18 Nov 11:00 (120 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 76 | MSG-10183 | Wed 18 Nov 13:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 77 | MSG-10169 | Wed 18 Nov 13:00 (60 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 78 | MSG-10185 | Wed 18 Nov 13:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 79 | MSG-10233 | Wed 18 Nov 13:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 80 | MSG-10170 | Wed 18 Nov 13:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 81 | MSG-10234 | Wed 18 Nov 14:00 (60 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 82 | MSG-10253 | Wed 18 Nov 14:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 83 | MSG-10187 | Wed 18 Nov 14:00 (60 min) | Service center bay | EPAS_w202 | safety_urgent | Owner stops driving & car is towed in |
| 84 | MSG-10172 | Wed 18 Nov 14:00 (60 min) | Service center bay | EPAS_a191 | safety_urgent | Owner stops driving & car is towed in |
| 85 | MSG-10189 | Wed 18 Nov 14:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 86 | MSG-10237 | Wed 18 Nov 15:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 87 | MSG-10259 | Wed 18 Nov 15:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 88 | MSG-10240 | Wed 18 Nov 15:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 89 | MSG-10193 | Wed 18 Nov 15:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 90 | MSG-10262 | Wed 18 Nov 15:00 (60 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 91 | MSG-10243 | Wed 18 Nov 16:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 92 | MSG-10196 | Wed 18 Nov 16:00 (90 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 93 | MSG-10245 | Wed 18 Nov 16:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 94 | MSG-10265 | Wed 18 Nov 16:00 (60 min) | Service center bay | EPAS_a191 | safety_urgent | Owner stops driving & car is towed in |
| 95 | MSG-10274 | Wed 18 Nov 16:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 96 | MSG-10247 | Wed 18 Nov 17:00 (120 min) | Service center bay | EPAS_a191 | safety_urgent | Owner stops driving & car is towed in |
| 97 | MSG-10269 | Wed 18 Nov 17:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 98 | MSG-10276 | Wed 18 Nov 17:00 (120 min) | Service center bay | BRK_w003 | safety_urgent | Owner stops driving & car is towed in |
| 99 | MSG-10278 | Wed 18 Nov 17:00 (90 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 100 | MSG-10280 | Wed 18 Nov 17:00 (60 min) | Service center bay | ABS_w002 | safety_urgent | Owner stops driving & car is towed in |
| 101 | MSG-10282 | Thu 19 Nov 07:00 (60 min) | Service center bay | EPAS_a191 | safety_urgent | Owner stops driving & car is towed in |
| 102 | MSG-10284 | Thu 19 Nov 07:00 (90 min) | Service center bay | ESP_w003 | safety_urgent | Owner stops driving & car is towed in |
| 103 | MSG-10286 | Thu 19 Nov 08:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 104 | MSG-10289 | Thu 19 Nov 08:00 (120 min) | Service center bay | BRK_a001 | safety_urgent | Owner stops driving & car is towed in |
| 105 | MSG-10292 | Thu 19 Nov 08:00 (60 min) | Service center bay | NONE | safety_urgent | Owner stops driving & car is towed in |
| 106 | MSG-10204 | Thu 19 Nov 09:00 (90 min) | Service center bay | NONE | soon | Service center visit |
| 107 | MSG-10059 | Thu 19 Nov 09:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 108 | MSG-10126 | Thu 19 Nov 09:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 109 | MSG-10095 | Thu 19 Nov 09:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 110 | MSG-10191 | Thu 19 Nov 10:00 (60 min) | Service center bay | CP_a004 | soon | Service center visit |
| 111 | MSG-10192 | Thu 19 Nov 10:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 112 | MSG-10268 | Thu 19 Nov 10:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 113 | MSG-10277 | Thu 19 Nov 10:00 (60 min) | Service center bay | NONE | soon | Service center visit |
| 114 | MSG-10283 | Thu 19 Nov 11:00 (120 min) | Service center bay | NONE | soon | Service center visit |
| 115 | MSG-10001 | Mon 16 Nov 08:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 116 | MSG-10294 | Mon 16 Nov 09:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 117 | MSG-10099 | Mon 16 Nov 09:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 118 | MSG-10199 | Mon 16 Nov 10:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 119 | MSG-10295 | Mon 16 Nov 10:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 120 | MSG-10051 | Mon 16 Nov 11:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 121 | MSG-10102 | Mon 16 Nov 13:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 122 | MSG-10052 | Mon 16 Nov 13:00 (60 min) | Remote / OTA diagnostic | HVAC_w003 | routine | Mobile service / remote support |
| 123 | MSG-10004 | Mon 16 Nov 13:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 124 | MSG-10201 | Mon 16 Nov 14:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 125 | MSG-10053 | Mon 16 Nov 14:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 126 | MSG-10026 | Mon 16 Nov 14:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 127 | MSG-10104 | Mon 16 Nov 15:00 (60 min) | Remote / OTA diagnostic | HVAC_w003 | routine | Mobile service / remote support |
| 128 | MSG-10005 | Mon 16 Nov 15:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 129 | MSG-10054 | Mon 16 Nov 16:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 130 | MSG-10298 | Mon 16 Nov 17:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 131 | MSG-10055 | Tue 17 Nov 07:00 (60 min) | Remote / OTA diagnostic | CP_a004 | routine | Mobile service / remote support |
| 132 | MSG-10105 | Tue 17 Nov 08:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 133 | MSG-10203 | Tue 17 Nov 08:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 134 | MSG-10028 | Tue 17 Nov 09:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 135 | MSG-10056 | Tue 17 Nov 09:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 136 | MSG-10106 | Tue 17 Nov 10:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 137 | MSG-10007 | Tue 17 Nov 10:00 (60 min) | Support callback | CP_a004 | routine | Mobile service / remote support |
| 138 | MSG-10029 | Tue 17 Nov 11:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 139 | MSG-10300 | Tue 17 Nov 13:00 (60 min) | Remote / OTA diagnostic | HVAC_w003 | routine | Mobile service / remote support |
| 140 | MSG-10030 | Tue 17 Nov 13:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 141 | MSG-10008 | Tue 17 Nov 14:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 142 | MSG-10058 | Tue 17 Nov 14:00 (60 min) | Support callback | WIP_w001 | routine | Mobile service / remote support |
| 143 | MSG-10031 | Tue 17 Nov 15:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 144 | MSG-10108 | Tue 17 Nov 16:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 145 | MSG-10109 | Tue 17 Nov 16:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 146 | MSG-10060 | Tue 17 Nov 17:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 147 | MSG-10033 | Wed 18 Nov 07:00 (60 min) | Remote / OTA diagnostic | CP_a004 | routine | Mobile service / remote support |
| 148 | MSG-10206 | Wed 18 Nov 08:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 149 | MSG-10010 | Wed 18 Nov 09:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 150 | MSG-10034 | Wed 18 Nov 10:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 151 | MSG-10061 | Wed 18 Nov 11:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 152 | MSG-10207 | Wed 18 Nov 13:00 (60 min) | Remote / OTA diagnostic | CP_a004 | routine | Mobile service / remote support |
| 153 | MSG-10035 | Wed 18 Nov 14:00 (60 min) | Support callback | WIP_w001 | routine | Mobile service / remote support |
| 154 | MSG-10111 | Wed 18 Nov 15:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 155 | MSG-10011 | Wed 18 Nov 16:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 156 | MSG-10063 | Wed 18 Nov 17:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 157 | MSG-10037 | Thu 19 Nov 08:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 158 | MSG-10113 | Thu 19 Nov 09:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 159 | MSG-10209 | Thu 19 Nov 10:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 160 | MSG-10064 | Thu 19 Nov 11:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 161 | MSG-10038 | Thu 19 Nov 13:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 162 | MSG-10065 | Thu 19 Nov 14:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 163 | MSG-10210 | Thu 19 Nov 15:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 164 | MSG-10040 | Thu 19 Nov 16:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 165 | MSG-10115 | Fri 20 Nov 07:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 166 | MSG-10014 | Fri 20 Nov 08:00 (60 min) | Support callback | HVAC_w003 | routine | Mobile service / remote support |
| 167 | MSG-10041 | Fri 20 Nov 09:00 (60 min) | Remote / OTA diagnostic | NONE | routine | Mobile service / remote support |
| 168 | MSG-10075 | Fri 20 Nov 10:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 169 | MSG-10067 | Fri 20 Nov 11:00 (60 min) | Support callback | NONE | routine | Mobile service / remote support |
| 170 | MSG-10125 | Fri 20 Nov 13:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 171 | MSG-10116 | Fri 20 Nov 14:00 (60 min) | Support callback | WIP_w001 | routine | Mobile service / remote support |
| 172 | MSG-10077 | Fri 20 Nov 15:00 (60 min) | Remote / OTA diagnostic | HVAC_w003 | routine | Mobile service / remote support |
| 173 | MSG-10015 | Sat 21 Nov 07:00 (60 min) | Remote / OTA diagnostic | WIP_w001 | routine | Mobile service / remote support |
| 174 | MSG-10042 | Sat 21 Nov 08:00 (60 min) | Support callback | WIP_w001 | routine | Mobile service / remote support |
| 175 | MSG-10078 | Sat 21 Nov 09:00 (60 min) | Remote / OTA diagnostic | UI_a004 | routine | Mobile service / remote support |
| 176 | MSG-10068 | Sat 21 Nov 10:00 (60 min) | Support callback | WIP_w001 | routine | Mobile service / remote support |
| 177 | MSG-10212 | Mon 16 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 178 | MSG-10128 | Mon 16 Nov 11:00 (90 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 179 | MSG-10080 | Mon 16 Nov 11:00 (120 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 180 | MSG-10129 | Mon 16 Nov 14:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 181 | MSG-10081 | Mon 16 Nov 15:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 182 | MSG-10213 | Mon 16 Nov 16:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 183 | MSG-10130 | Mon 16 Nov 16:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 184 | MSG-10131 | Mon 16 Nov 17:00 (90 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 185 | MSG-10070 | Tue 17 Nov 09:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 186 | MSG-10118 | Tue 17 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 187 | MSG-10043 | Tue 17 Nov 11:00 (90 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 188 | MSG-10017 | Tue 17 Nov 11:00 (120 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 189 | MSG-10214 | Tue 17 Nov 13:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 190 | MSG-10133 | Tue 17 Nov 13:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 191 | MSG-10071 | Tue 17 Nov 14:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 192 | MSG-10084 | Tue 17 Nov 15:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 193 | MSG-10134 | Tue 17 Nov 15:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 194 | MSG-10044 | Tue 17 Nov 16:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 195 | MSG-10085 | Tue 17 Nov 17:00 (90 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 196 | MSG-10150 | Tue 17 Nov 17:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 197 | MSG-10136 | Wed 18 Nov 08:00 (90 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 198 | MSG-10215 | Wed 18 Nov 09:00 (60 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 199 | MSG-10086 | Wed 18 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 200 | MSG-10072 | Wed 18 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 201 | MSG-10137 | Wed 18 Nov 11:00 (90 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 202 | MSG-10138 | Wed 18 Nov 11:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 203 | MSG-10046 | Wed 18 Nov 13:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 204 | MSG-10088 | Wed 18 Nov 13:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 205 | MSG-10139 | Wed 18 Nov 14:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 206 | MSG-10019 | Wed 18 Nov 14:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 207 | MSG-10152 | Wed 18 Nov 15:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 208 | MSG-10216 | Wed 18 Nov 15:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 209 | MSG-10089 | Wed 18 Nov 16:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 210 | MSG-10120 | Wed 18 Nov 17:00 (90 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 211 | MSG-10047 | Thu 19 Nov 08:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 212 | MSG-10090 | Thu 19 Nov 09:00 (60 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 213 | MSG-10141 | Thu 19 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 214 | MSG-10142 | Thu 19 Nov 10:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 215 | MSG-10020 | Thu 19 Nov 11:00 (90 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 216 | MSG-10155 | Thu 19 Nov 11:00 (60 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 217 | MSG-10217 | Thu 19 Nov 13:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 218 | MSG-10143 | Thu 19 Nov 13:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 219 | MSG-10092 | Thu 19 Nov 14:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 220 | MSG-10074 | Thu 19 Nov 14:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 221 | MSG-10156 | Thu 19 Nov 15:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 222 | MSG-10094 | Thu 19 Nov 15:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 223 | MSG-10021 | Thu 19 Nov 16:00 (90 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 224 | MSG-10049 | Thu 19 Nov 17:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 225 | MSG-10145 | Fri 20 Nov 08:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 226 | MSG-10121 | Fri 20 Nov 09:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 227 | MSG-10158 | Fri 20 Nov 09:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 228 | MSG-10159 | Fri 20 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 229 | MSG-10146 | Fri 20 Nov 10:00 (60 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 230 | MSG-10097 | Fri 20 Nov 11:00 (90 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 231 | MSG-10175 | Fri 20 Nov 11:00 (60 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 232 | MSG-10225 | Fri 20 Nov 13:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 233 | MSG-10161 | Fri 20 Nov 14:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 234 | MSG-10098 | Fri 20 Nov 15:00 (60 min) | Mobile service visit | CP_a004 | routine | Mobile service / remote support |
| 235 | MSG-10147 | Fri 20 Nov 16:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 236 | MSG-10162 | Fri 20 Nov 17:00 (60 min) | Mobile service visit | WIP_w001 | routine | Mobile service / remote support |
| 237 | MSG-10177 | Sat 21 Nov 09:00 (60 min) | Mobile service visit | UI_a004 | routine | Mobile service / remote support |
| 238 | MSG-10148 | Sat 21 Nov 10:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 239 | MSG-10227 | Sat 21 Nov 11:00 (90 min) | Mobile service visit | HVAC_w003 | routine | Mobile service / remote support |
| 240 | MSG-10023 | Sat 21 Nov 11:00 (60 min) | Mobile service visit | NONE | routine | Mobile service / remote support |
| 241 | MSG-10164 | Thu 19 Nov 11:00 (90 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 242 | MSG-10179 | Thu 19 Nov 11:00 (60 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 243 | MSG-10228 | Thu 19 Nov 11:00 (120 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 244 | MSG-10166 | Thu 19 Nov 11:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 245 | MSG-10181 | Thu 19 Nov 13:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 246 | MSG-10167 | Thu 19 Nov 13:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 247 | MSG-10182 | Thu 19 Nov 13:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 248 | MSG-10220 | Thu 19 Nov 13:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 249 | MSG-10231 | Thu 19 Nov 13:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 250 | MSG-10168 | Thu 19 Nov 14:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 251 | MSG-10250 | Thu 19 Nov 14:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 252 | MSG-10232 | Thu 19 Nov 14:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 253 | MSG-10184 | Thu 19 Nov 14:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 254 | MSG-10122 | Thu 19 Nov 14:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 255 | MSG-10251 | Thu 19 Nov 15:00 (60 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 256 | MSG-10252 | Thu 19 Nov 15:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 257 | MSG-10186 | Thu 19 Nov 15:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 258 | MSG-10171 | Thu 19 Nov 15:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 259 | MSG-10235 | Thu 19 Nov 15:00 (60 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 260 | MSG-10254 | Thu 19 Nov 16:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 261 | MSG-10188 | Thu 19 Nov 16:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 262 | MSG-10236 | Thu 19 Nov 16:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 263 | MSG-10255 | Thu 19 Nov 16:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 264 | MSG-10256 | Thu 19 Nov 16:00 (60 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 265 | MSG-10173 | Thu 19 Nov 17:00 (120 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 266 | MSG-10190 | Thu 19 Nov 17:00 (60 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 267 | MSG-10257 | Thu 19 Nov 17:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 268 | MSG-10238 | Thu 19 Nov 17:00 (120 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 269 | MSG-10258 | Thu 19 Nov 17:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 270 | MSG-10239 | Thu 19 Nov 17:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 271 | MSG-10260 | Fri 20 Nov 07:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 272 | MSG-10241 | Fri 20 Nov 07:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 273 | MSG-10261 | Fri 20 Nov 08:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 274 | MSG-10194 | Fri 20 Nov 08:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 275 | MSG-10221 | Fri 20 Nov 08:00 (90 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 276 | MSG-10242 | Fri 20 Nov 09:00 (60 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 277 | MSG-10195 | Fri 20 Nov 09:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 278 | MSG-10263 | Fri 20 Nov 09:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 279 | MSG-10244 | Fri 20 Nov 09:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 280 | MSG-10264 | Fri 20 Nov 10:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 281 | MSG-10197 | Fri 20 Nov 10:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 282 | MSG-10273 | Fri 20 Nov 10:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 283 | MSG-10266 | Fri 20 Nov 10:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 284 | MSG-10246 | Fri 20 Nov 10:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 285 | MSG-10267 | Fri 20 Nov 11:00 (120 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 286 | MSG-10275 | Fri 20 Nov 11:00 (90 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 287 | MSG-10270 | Fri 20 Nov 11:00 (60 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 288 | MSG-10271 | Fri 20 Nov 11:00 (120 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 289 | MSG-10279 | Fri 20 Nov 11:00 (90 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 290 | MSG-10281 | Fri 20 Nov 13:00 (60 min) | Service center bay | HVAC_w003 | routine | Mobile service / remote support |
| 291 | MSG-10123 | Fri 20 Nov 13:00 (90 min) | Service center bay | CP_a004 | routine | Mobile service / remote support |
| 292 | MSG-10222 | Fri 20 Nov 13:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 293 | MSG-10285 | Fri 20 Nov 13:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 294 | MSG-10025 | Fri 20 Nov 13:00 (60 min) | Service center bay | UI_a004 | routine | Mobile service / remote support |
| 295 | MSG-10287 | Fri 20 Nov 14:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 296 | MSG-10288 | Fri 20 Nov 14:00 (60 min) | Service center bay | WIP_w001 | routine | Mobile service / remote support |
| 297 | MSG-10272 | Fri 20 Nov 14:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 298 | MSG-10290 | Fri 20 Nov 14:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 299 | MSG-10291 | Fri 20 Nov 15:00 (90 min) | Service center bay | NONE | routine | Mobile service / remote support |
| 300 | MSG-10293 | Fri 20 Nov 15:00 (60 min) | Service center bay | NONE | routine | Mobile service / remote support |
