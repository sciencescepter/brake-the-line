from datetime import date, datetime, time

import pytest
from pydantic import ValidationError

from triage.booking import Booking, QueueItem, Slot, book_all, load_slots
from triage.rules import FixPath, Urgency

PATH = {Urgency.SAFETY_URGENT: FixPath.TOW_IN, Urgency.SOON: FixPath.SERVICE_CENTER_VISIT,
        Urgency.ROUTINE: FixPath.MOBILE_REMOTE_SUPPORT}


def slot(n, day, hour, kind="service_center_bay"):
    return Slot(slot_id=f"SLOT-{n:04d}", slot_date=date(2026, 11, day), slot_start_time=time(hour),
                duration_minutes=60, slot_type=kind, bay_id="BAY-01", technician_id="TECH-01", status="open")


def item(n, urgency, minute=0):
    return QueueItem(f"MSG-{n:05d}", datetime(2026, 11, 15, 18, minute), urgency, PATH[urgency], "NONE")


def test_safety_books_same_day_then_carries_over():
    slots = [slot(1, 16, 9), slot(2, 16, 10), slot(3, 17, 8), slot(4, 17, 9)]
    items = [item(i, Urgency.SAFETY_URGENT, i) for i in range(1, 4)]
    bookings, wait = book_all(items, slots)
    assert [b.slot_id for b in bookings] == ["SLOT-0001", "SLOT-0002", "SLOT-0003"]
    assert [b.same_day for b in bookings] == [True, True, False]
    assert wait == []


def test_safety_books_before_older_soon_and_routine():
    slots = [slot(1, 16, 9), slot(2, 16, 10)]
    items = [item(1, Urgency.SOON, 0), item(2, Urgency.ROUTINE, 1), item(3, Urgency.SAFETY_URGENT, 59)]
    bookings, wait = book_all(items, slots)
    assert [(b.message_id, b.slot_id) for b in bookings] == [("MSG-00003", "SLOT-0001"), ("MSG-00001", "SLOT-0002")]
    assert [w.message_id for w in wait] == ["MSG-00002"]


def test_safety_and_soon_only_take_bays():
    slots = [slot(1, 16, 9, "mobile_service_visit"), slot(2, 16, 10, "support_callback")]
    bookings, wait = book_all([item(1, Urgency.SAFETY_URGENT), item(2, Urgency.SOON)], slots)
    assert bookings == [] and len(wait) == 2


def test_routine_prefers_remote_then_mobile_then_bay():
    slots = [slot(1, 16, 8), slot(2, 16, 9, "mobile_service_visit"),
             slot(3, 21, 17, "support_callback"), slot(4, 20, 9, "remote_ota_or_diagnostic")]
    items = [item(i, Urgency.ROUTINE, i) for i in range(1, 5)]
    bookings, _ = book_all(items, slots)
    assert [b.slot_type for b in bookings] == [
        "remote_ota_or_diagnostic", "support_callback", "mobile_service_visit", "service_center_bay"]


def test_each_slot_holds_one_message():
    bookings, wait = book_all([item(i, Urgency.SAFETY_URGENT, i) for i in range(5)], [slot(1, 16, 9)])
    assert len(bookings) == 1 and len(wait) == 4


def test_booking_rejects_wrong_slot_type_for_tag():
    with pytest.raises(ValidationError):
        Booking(message_id="MSG-00001", urgency="safety_urgent", fix_path="tow_in", vehicle_alert_code="NONE",
                slot_id="SLOT-0001", slot_date=date(2026, 11, 16), slot_start_time=time(9), duration_minutes=60,
                slot_type="support_callback", bay_id="REMOTE-DESK", technician_id="TECH-01", same_day=True)


def test_slot_file_loads_clean_and_bad_rows_rejected(tmp_path):
    slots, rejected = load_slots()
    assert len(slots) == 320 and rejected == []
    p = tmp_path / "slots.csv"
    p.write_text(
        "slot_id,slot_date,slot_start_time,duration_minutes,slot_type,bay_id,technician_id,status\n"
        "SLOT-0001,2026-11-16,07:00,60,service_center_bay,BAY-02,TECH-03,open\n"
        "SLOT-0002,2026-11-16,,60,service_center_bay,BAY-02,TECH-03,open\n"
        "SLOT-0003,2026-11-16,08:00,60,car_wash,BAY-02,TECH-03,open\n"
        "SLOT-0001,2026-11-16,09:00,60,service_center_bay,BAY-02,TECH-03,open\n"
    )
    slots, rejected = load_slots(p)
    assert [s.slot_id for s in slots] == ["SLOT-0001"] and [r.line for r in rejected] == [3, 4, 5]
