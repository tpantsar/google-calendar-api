import logging
from unittest.mock import MagicMock, patch

from src.services.event import get_popular_events

logger = logging.getLogger(__name__)


class TestServicesEvent(object):
    """Tests for src.services.event"""

    @patch('src.services.event.build_service')
    def test_get_popular_events_multiple_events(self, mock_build_service):
        # Mock the service object and its methods
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the events returned by the API
        mock_events = {
            'items': [
                {'summary': 'Event A'},
                {'summary': 'Event B'},
                {'summary': 'Event A'},
                {'summary': 'Event C'},
                {'summary': 'Event B'},
                {'summary': 'Event A'},
            ]
        }
        mock_service.events().list().execute.return_value = mock_events

        # Call the function
        result = get_popular_events('test_calendar_id')
        logger.debug(result)

        # Assert the result
        assert result == {'Event A': 3, 'Event B': 2, 'Event C': 1}

    @patch('src.services.event.build_service')
    def test_get_popular_events_no_events(self, mock_build_service):
        # Mock the service and its methods
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the events returned by the API to be empty
        mock_service.events().list().execute.return_value = {'items': []}

        result = get_popular_events('test_calendar_id')
        logger.debug(result)

        # Assert the result
        assert result == {}

    @patch('src.services.event.build_service')
    def test_get_popular_events_single_event(self, mock_build_service):
        # Mock the service and its methods
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the events returned by the API with a single event
        mock_events = {
            'items': [
                {'summary': 'Event A'},
            ]
        }
        mock_service.events().list().execute.return_value = mock_events

        # Call the function
        result = get_popular_events('test_calendar_id')
        logger.debug(result)

        # Assert the result
        assert result == {'Event A': 1}

    @patch('src.services.event.build_service')
    def test_get_popular_events_more_than_ten_unique_events(self, mock_build_service):
        # Mock the service and its methods
        mock_service = MagicMock()
        mock_build_service.return_value = mock_service

        # Mock the events returned by the API with more than ten unique events
        mock_events = {'items': [{'summary': f'Event {chr(65 + i)}'} for i in range(15)]}
        mock_service.events().list().execute.return_value = mock_events

        # Call the function
        result = get_popular_events('test_calendar_id')
        logger.debug(result)

        # Assert the result contains only 10 most recent events
        assert len(result) == 10
