from unittest.mock import MagicMock, patch

import pytest
from InquirerPy.validator import ValidationError

from src.utils import format_str_datetime_to_iso
from terminal import DateTimeValidator, custom, fast


# Mock constants and services
@pytest.fixture
def mock_constants():
    with patch("terminal.TIMEZONE", "UTC"):
        yield


@pytest.fixture
def mock_services():
    with patch("terminal.get_calendar_list") as mock_get_calendar_list, patch(
        "terminal.get_recent_unique_events"
    ) as mock_get_recent_unique_events, patch(
        "terminal.create_event"
    ) as mock_create_event:
        yield mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event


# Parametrized test for DateTimeValidator
@pytest.mark.parametrize(
    "datetime_str",
    [
        ("2023-10-10 10:10"),
        ("2023-12-31 23:59"),
        ("2023-01-01 00:00"),
        ("2023-1-1 9:00"),
        ("2023-01-1 9:00"),
        ("2023-1-01 9:00"),
        ("2023-1-1 9:0"),
    ],
)
def test_datetime_validator_valid(datetime_str):
    validator = DateTimeValidator()
    document = MagicMock()
    document.text = datetime_str
    try:
        validator.validate(document)
    except ValidationError:
        pytest.fail("ValidationError raised unexpectedly!")


@pytest.mark.parametrize(
    "datetime_str",
    [
        ("invalid-date"),
        ("2023-13-01 10:10"),
        ("2023-10-32 10:10"),
        ("2023-10-10 25:00"),
        ("2023-10-10 10:61"),
    ],
)
def test_datetime_validator_invalid(datetime_str):
    validator = DateTimeValidator()
    document = MagicMock()
    document.text = datetime_str
    with pytest.raises(ValidationError):
        validator.validate(document)


# Test format_datetime
def test_format_datetime():
    datetime_str = "2023-10-10 10:10"
    timezone_str = "UTC"
    expected = "2023-10-10T10:10:00+00:00"
    assert format_str_datetime_to_iso(datetime_str, timezone_str) == expected


# Test fast function with print_event_details
def test_fast(mock_constants, mock_services):
    mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event = (
        mock_services
    )
    mock_get_recent_unique_events.return_value = [
        "Summary1",
        "Summary2",
        "Summary3",
    ]
    mock_create_event.return_value = {
        "summary": "Test Event",
        "description": "Test Description",
        "htmlLink": "http://example.com",
    }

    # Mock inquirer prompt values
    with patch("InquirerPy.inquirer.number") as mock_number, patch(
        "InquirerPy.inquirer.text"
    ) as mock_text, patch("terminal.print_event_details") as mock_print_event_details:
        mock_number.return_value.execute.return_value = 60
        mock_text.return_value.execute.side_effect = [
            "Test Summary",
            "Test Description",
        ]

        fast("test_calendar_id")

        mock_create_event.assert_called_once()
        try:
            mock_print_event_details.assert_called_once()
        except Exception as e:
            pytest.fail(f"print_event_details raised an exception: {e}")


# Test custom function with print_event_details
def test_custom(mock_constants, mock_services):
    mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event = (
        mock_services
    )
    mock_get_recent_unique_events.return_value = [
        "Summary1",
        "Summary2",
        "Summary3",
    ]
    mock_create_event.return_value = {
        "summary": "Test Event",
        "description": "Test Description",
        "htmlLink": "http://example.com",
    }

    with patch("InquirerPy.inquirer.text") as mock_text, patch(
        "terminal.print_event_details"
    ) as mock_print_event_details:
        mock_text.return_value.execute.side_effect = [
            "Test Summary",
            "Test Description",
            "2023-10-10 10:15",
            "2023-10-10 11:15",
        ]

        custom("test_calendar_id")

        mock_create_event.assert_called_once()
        mock_print_event_details.assert_called_once()
        try:
            mock_print_event_details.assert_called_once()
        except Exception as e:
            pytest.fail(f"print_event_details raised an exception: {e}")
