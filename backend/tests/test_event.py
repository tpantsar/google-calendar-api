from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from googleapiclient.errors import HttpError

from services.event import get_popular_events

from ..src.error import APIError


@patch("services.event.build_service")
@patch("services.event.datetime")
def test_get_popular_events_success(mock_datetime, mock_build_service):
    # Mock the current datetime
    mock_datetime.now.return_value = datetime(2023, 10, 10)

    # Mock the service and its methods
    mock_service = MagicMock()
    mock_build_service.return_value = mock_service

    # Mock the events returned by the API
    mock_events = {
        "items": [
            {"summary": "Event A"},
            {"summary": "Event B"},
            {"summary": "Event A"},
            {"summary": "Event C"},
            {"summary": "Event B"},
            {"summary": "Event A"},
        ]
    }
    mock_service.events().list().execute.return_value = mock_events

    # Call the function
    calendar_id = "test_calendar_id"
    result = get_popular_events(calendar_id)

    # Assert the result
    assert result == ["Event A", "Event B", "Event C"]


@patch("services.event.build_service")
def test_get_popular_events_service_build_error(mock_build_service):
    # Mock the service build to raise an exception
    mock_build_service.side_effect = Exception("Service build error")

    # Call the function and assert it raises an APIError
    calendar_id = "test_calendar_id"
    with pytest.raises(APIError) as excinfo:
        get_popular_events(calendar_id)
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Service Build Error"


@patch("services.event.build_service")
@patch("services.event.datetime")
def test_get_popular_events_http_error(mock_datetime, mock_build_service):
    # Mock the current datetime
    mock_datetime.now.return_value = datetime(2023, 10, 10)

    # Mock the service and its methods
    mock_service = MagicMock()
    mock_build_service.return_value = mock_service

    # Mock the events list method to raise an HttpError
    mock_service.events().list().execute.side_effect = HttpError(
        resp=MagicMock(status=500), content=b"Internal Server Error"
    )

    # Call the function and assert it raises an APIError
    calendar_id = "test_calendar_id"
    with pytest.raises(APIError) as excinfo:
        get_popular_events(calendar_id)
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Google Calendar API Error"


@patch("services.event.build_service")
@patch("services.event.datetime")
def test_get_popular_events_key_error(mock_datetime, mock_build_service):
    # Mock the current datetime
    mock_datetime.now.return_value = datetime(2023, 10, 10)

    # Mock the service and its methods
    mock_service = MagicMock()
    mock_build_service.return_value = mock_service

    # Mock the events returned by the API with a missing summary
    mock_events = {
        "items": [
            {"summary": "Event A"},
            {"summary": "Event B"},
            {"summary": "Event A"},
            {"summary": "Event C"},
            {"summary": "Event B"},
            {"summary": "Event A"},
            {},
        ]
    }
    mock_service.events().list().execute.return_value = mock_events

    # Call the function and assert it raises an APIError
    calendar_id = "test_calendar_id"
    with pytest.raises(APIError) as excinfo:
        get_popular_events(calendar_id)
    assert excinfo.value.status_code == 500
    assert excinfo.value.message == "Event Analysis Error"
