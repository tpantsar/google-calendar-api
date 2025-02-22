import json
import logging
from typing import Generator
from unittest.mock import MagicMock, patch

import pytest
from flask import Flask
from flask.testing import FlaskClient

from src.resources.event import EventList

logger = logging.getLogger(__name__)

app = Flask(__name__)

# Register the EventList resource with the Flask application
app.add_url_rule(
    '/events/<string:calendar_id>', view_func=EventList.as_view('event_list')
)


@pytest.fixture
def client() -> Generator[FlaskClient, None, None]:
    """Create a Flask test client for testing the API."""
    with app.test_client() as client:
        yield client


# Mock the events returned by the API
mock_events = {
    'items': [
        {
            'id': 'test-id-1',
            'start': '2025-02-01T10:00:00Z',
            'end': '2025-02-01T15:00:00Z',
        },
        {
            'id': 'test-id-2',
            'start': '2025-02-15T10:00:00Z',
            'end': '2025-02-15T12:00:00Z',
        },
    ]
}


class TestEventList(object):
    """Tests for src.resources.event"""

    @patch('src.services.event.build_service')
    @patch('src.services.event.update_event_properties')
    def test_get_with_query_parameters(
        self, mock_build_service, mock_update_event_properties, client: FlaskClient
    ):
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service
        mock_update_event_properties.return_value = mock_service
        mock_service.events().list().execute.return_value = mock_events

        query_params = {
            'start_date': '2025-02-01T00:00:00Z',
            'end_date': '2025-02-28T00:00:00Z',
        }

        # Send a GET request to the /events/<calendar_id> endpoint with query parameters
        response = client.get('/events/test_calendar_id', query_string=query_params)

        # Assert the response status code and content
        assert response.status_code == 200
        data = json.loads(response.data)

        # Additional assertions based on the expected response content
        # For example, check if the events have the expected start and end dates
        for event in data:
            assert 'start' in event
            assert 'end' in event

    @patch('src.services.event.build_service')
    @patch('src.services.event.update_event_properties')
    def test_get_with_invalid_query_parameters(
        self, mock_build_service, mock_update_event_properties, client: FlaskClient
    ):
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service
        mock_update_event_properties.return_value = mock_service
        mock_service.events().list().execute.return_value = mock_events

        query_params = {
            'start_date': '32.13.2025',  # Invalid date format
            'end_date': '2025-02-28T00:00:00Z',
            'search_query': 123,
        }

        # Send a GET request to the /events/<calendar_id> endpoint with query parameters
        response = client.get('/events/test_calendar_id', query_string=query_params)

        # Assert the response status code and content
        assert response.status_code == 400
        data = json.loads(response.data)
        assert data['@error']['@message'] == 'Invalid query parameters'
        assert data['@error']['@messages'][0] == 'Date and time is invalid: 32.13.2025'
