from datetime import date, datetime

from triage.booking import QueueItem, queue_order
from triage.load import load_batch
from triage.rules import FixPath, Urgency
from triage.safety_check import load_tags
from triage.queue_view import (
    build_queue, filter_queue, load_schedule, open_slots_after, pasted_message, position_for_new,
)
from triage.booking import BookingTool, load_slots

from .test_booking import slot


def qi(mid, urgency, ts):
    return QueueItem(mid, ts, urgency, FixPath.MOBILE_REMOTE_SUPPORT, "NONE")


def test_same_urgency_earliest_first_message_id_breaks_ties():
    t1, t2 = datetime(2026, 11, 15, 18, 0), datetime(2026, 11, 15, 19, 0)
    items = [
        qi("MSG-10009", Urgency.ROUTINE, t2),
        qi("MSG-10005", Urgency.ROUTINE, t1),
        qi("MSG-10003", Urgency.ROUTINE, t1),   # same time as 10005: lower id first
        qi("MSG-10001", Urgency.ROUTINE, t2),   # same time as 10009: lower id first
        qi("MSG-10099", Urgency.SAFETY_URGENT, t2),
    ]
    assert [i.message_id for i in queue_order(items)] == [
        "MSG-10099", "MSG-10003", "MSG-10005", "MSG-10001", "MSG-10009"]


def real_queue():
    messages, _ = load_batch()
    return build_queue(messages, load_tags(), load_schedule())


def test_real_queue_order_and_booking_match():
    rows = real_queue()
    assert len(rows) == 300 and all(r.booked for r in rows)
    assert [r.position for r in rows] == list(range(1, 301))
    rank = {"safety_urgent": 0, "soon": 1, "routine": 2}
    for a, b in zip(rows, rows[1:]):
        assert rank[a.urgency.value] <= rank[b.urgency.value]
        if a.urgency is b.urgency:  # submitted time never goes backwards inside a tag
            assert (a.received_at, a.message_id) < (b.received_at, b.message_id)
    sched = load_schedule()
    assert all(int(sched[r.message_id]["queue_position"]) == r.position for r in rows)


def test_filter_keeps_order_and_queue_numbers():
    rows = real_queue()
    out = filter_queue(rows, urgencies={"soon"})
    assert len(out) == 9 and [r.position for r in out] == sorted(r.position for r in out)
    assert out[0].position == 106  # numbers come from the full queue
    assert all("pedal" in (r.message_text + r.subject).lower() for r in filter_queue(rows, search="PEDAL"))
    assert {r.slot_type for r in filter_queue(rows, slot_types={"support_callback"})} == {"support_callback"}


def test_position_for_new_goes_last_in_its_tag():
    rows = real_queue()
    assert position_for_new(rows, Urgency.SAFETY_URGENT) == (106, 106)
    assert position_for_new(rows, Urgency.SOON) == (115, 10)
    assert position_for_new(rows, Urgency.ROUTINE) == (301, 187)


def test_pasted_message_validates_and_gets_a_free_id():
    msg = pasted_message("The brake pedal feels soft, no rush.", "", {"MSG-10001", "MSG-10002"},
                         now=datetime(2026, 11, 17, 9, 30))
    assert msg.message_id == "MSG-10003" and msg.vehicle_alert_code == "NONE"
    assert msg.received_at == datetime(2026, 11, 17, 9, 30)


def test_open_slots_after_and_preview_booking():
    slots = [slot(1, 16, 9), slot(2, 17, 9), slot(3, 18, 9)]
    left = open_slots_after(slots, {"SLOT-0001"})
    assert [s.slot_id for s in left] == ["SLOT-0002", "SLOT-0003"]
    tool = BookingTool(left, booking_day=date(2026, 11, 16))
    b = tool.book(qi("MSG-10301", Urgency.SAFETY_URGENT, datetime(2026, 11, 16, 8)))
    assert b.slot_id == "SLOT-0002" and b.same_day is False
    real, _ = load_slots()
    assert len(open_slots_after(real, {r["slot_id"] for r in load_schedule().values()})) == 20
