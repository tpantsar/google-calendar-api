import json
from datetime import datetime

from flask import Response, request
from flask_restful import Resource

from constants import JSON, MASON
from error import APIError, ParameterError, create_error_response
from logger_config import logger
from services.event import (
    create_event,
    delete_event,
    get_event,
    get_events,
    update_event,
)


class EventList(Resource):
    """Resource for a list of calendar events."""

    def get(self, calendar_id) -> Response:
        """Returns the calendar events for the current year."""
        if calendar_id is None:
            return create_error_response(400, "Bad Request", "Calendar ID is missing")

        current_year = datetime.now().year

        try:
            events = get_events(calendar_id, current_year)
            return Response(json.dumps(events), status=200, mimetype=MASON)
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"An unhandled error occurred: {e}")
            return create_error_response(500, "Internal Server Error", str(e))

    def post(self, calendar_id) -> Response:
        """
        Creates a new calendar event.
        """
        if request.content_type != JSON:
            return create_error_response(
                415, "Unsupported Media Type", "Request type must be JSON"
            )

        try:
            return create_event(calendar_id, event_body=request.get_json())
        except APIError as e:
            return e.to_response()
        except ParameterError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"An unhandled error occurred: {e}")
            return create_error_response(500, "Internal Server Error", str(e))


class EventItem(Resource):
    """Resource for a single calendar event."""

    def get(self, calendar_id, event_id) -> Response:
        """Returns a single calendar event by ID."""
        try:
            event = get_event(calendar_id, event_id)
            return Response(json.dumps(event), status=200, mimetype=MASON)
        except ParameterError as e:
            return e.to_response()
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"An unhandled error occurred: {e}")
            return create_error_response(500, "Internal Server Error", str(e))

    def put(self, calendar_id, event_id) -> Response:
        """
        Updates a calendar event.
        https://developers.google.com/calendar/api/v3/reference/events/update#python
        PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId

        Returns: Response object
        """
        if request.content_type != JSON:
            return create_error_response(
                415, "Unsupported Media Type", "Request type must be JSON"
            )

        try:
            return update_event(calendar_id, event_id, event_body=request.get_json())
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"An unhandled error occurred: {e}")
            return create_error_response(500, "Internal Server Error", str(e))

    def delete(self, calendar_id, event_id) -> Response:
        """
        Deletes a single calendar event by ID.
        Returns: Response object
        """
        if calendar_id is None or event_id is None:
            return create_error_response(
                400, "Bad Request", "Calendar ID or event ID is missing"
            )

        try:
            delete_event(calendar_id, event_id)
            return Response("Event deleted successfully", status=200)
        except APIError as e:
            return e.to_response()
        except Exception as e:
            return create_error_response(500, "Internal Server Error", str(e))
