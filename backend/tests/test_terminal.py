from unittest.mock import patch

import pytest

from src.utils import format_str_datetime_to_iso
from terminal import custom, fast


# Mock constants and services
@pytest.fixture
def mock_constants():
    with patch('terminal.TIMEZONE', 'UTC'):
        yield


@pytest.fixture
def mock_services():
    with (
        patch('terminal.get_calendar_list') as mock_get_calendar_list,
        patch('terminal.get_recent_unique_events') as mock_get_recent_unique_events,
        patch('terminal.create_event') as mock_create_event,
    ):
        yield mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event


# Test format_datetime
def test_format_datetime():
    datetime_str = '2023-10-10 10:10'
    timezone_str = 'UTC'
    expected = '2023-10-10T10:10:00+00:00'
    assert format_str_datetime_to_iso(datetime_str, timezone_str) == expected


def test_fast(mock_services):
    """Test fast function with print_event_details"""
    mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event = (
        mock_services
    )
    mock_get_recent_unique_events.return_value = [
        'Summary1',
        'Summary2',
        'Summary3',
    ]
    mock_create_event.return_value = {
        'summary': 'Test Event',
        'description': 'Test Description',
        'htmlLink': 'http://example.com',
    }

    # Mock inquirer prompt values
    with (
        patch('terminal.get_duration') as mock_duration,
        patch('InquirerPy.inquirer.text') as mock_title_desc,
        patch('terminal.print_event_details') as mock_print_event_details,
    ):
        mock_duration.return_value = '60 minutes'
        mock_title_desc.return_value.execute.side_effect = [
            'Test Summary',
            'Test Description',
        ]

        fast('test_calendar_id')

        mock_create_event.assert_called_once()
        try:
            mock_print_event_details.assert_called_once()
        except Exception as e:
            pytest.fail(f'print_event_details raised an exception: {e}')


@patch('builtins.input', lambda: '10:15')  # Mock start time input
def test_custom(mock_services):
    """Test custom function with print_event_details."""
    mock_get_calendar_list, mock_get_recent_unique_events, mock_create_event = (
        mock_services
    )
    mock_get_recent_unique_events.return_value = [
        'Summary1',
        'Summary2',
        'Summary3',
    ]
    mock_create_event.return_value = {
        'summary': 'Test Event',
        'description': 'Test Description',
        'htmlLink': 'http://example.com',
    }

    # Mock inquirer prompt values
    with (
        patch('terminal.get_duration') as mock_duration,
        patch('InquirerPy.inquirer.text') as mock_text,
        patch('terminal.print_event_details') as mock_print_event_details,
    ):
        mock_duration.return_value = '60 minutes'
        mock_text.return_value.execute.side_effect = [
            'Test Summary',
            'Test Description',
            '2023-10-10 10:15',  # Start time
        ]

        custom('test_calendar_id')

        mock_create_event.assert_called_once()
        try:
            mock_print_event_details.assert_called_once()
        except Exception as e:
            pytest.fail(f'print_event_details raised an exception: {e}')
