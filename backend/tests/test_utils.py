from datetime import datetime

import pytest
from typeguard import TypeCheckError

from src.utils import print_event_details


def test_print_event_details_success():
    event = {
        "summary": "Test Event",
        "description": "This is a test event",
        "htmlLink": "http://example.com",
    }
    duration = 2
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 20, 0)

    try:
        print_event_details(event, duration, start, end)
    except Exception:
        pytest.fail("print_event_details raised an exception unexpectedly!")


def test_print_event_details_partial_data_success():
    event = {"summary": "Test Event", "description": "This is a test event"}
    duration = 2
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 20, 0)

    try:
        print_event_details(event, duration, start, end)
    except Exception:
        pytest.fail("print_event_details raised an exception unexpectedly!")


def test_print_event_details_missing_event_data():
    event = {"summary": "Test Event"}
    duration = 2
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 20, 0)

    with pytest.raises(ValueError):
        print_event_details(event, duration, start, end)


def test_print_event_details_valid_datetime():
    test_event = {
        "summary": "Test Event",
        "description": "Test Description",
        "htmlLink": "http://example.com",
    }

    try:
        start = datetime(2025, 1, 8, 11, 15, 0)
        end = datetime(2025, 1, 8, 12, 15, 0)
        print_event_details(test_event, 1.5, start, end)
    except Exception:
        pytest.fail("print_event_details raised an exception unexpectedly!")


def test_print_event_details_invalid_datetime1():
    test_event = {
        "summary": "Test Event",
        "description": "Test Description",
        "htmlLink": "http://example.com",
    }

    with pytest.raises(TypeCheckError):
        print_event_details(
            test_event, 1.5, "2025-01-08 11:15:00+02:00", "2025-01-08 12:15:00+02:00"
        )


def test_print_event_details_invalid_datetime2():
    test_event = {
        "summary": "Test Event",
        "description": "Test Description",
        "htmlLink": "http://example.com",
    }

    with pytest.raises(TypeCheckError):
        print_event_details(test_event, 1.5, "2023-10-10 10:15", "2023-10-10 11:15")
