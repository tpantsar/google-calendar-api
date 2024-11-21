import json
from datetime import datetime

from flask import Response, request
from flask_restful import Resource

from constants import JSON, MASON
from services.event import (
    create_calendar_event,
    delete_calendar_event,
    get_calendar_event,
    get_calendar_events,
    update_calendar_event,
)
from utils import create_error_response


class EventList(Resource):
    def get(self, calendar_id):
        """Returns the calendar events for the current year."""
        if calendar_id is None:
            return create_error_response(400, "Bad Request", "Calendar ID is missing")

        current_year = datetime.now().year
        events = get_calendar_events(calendar_id, current_year)

        if events is None:
            return create_error_response(
                500,
                "Internal Server Error",
                f"Failed to fetch the calendar events for {current_year}",
            )

        return Response(json.dumps(events), status=200, mimetype=MASON)

    def post(self, calendar_id):
        """
        Creates a new calendar event.
        """
        if request.content_type != JSON:
            return create_error_response(
                415, "Unsupported Media Type", "Request type must be JSON"
            )

        return create_calendar_event(calendar_id, event_body=request.get_json())


class EventItem(Resource):
    def get(self, calendar_id, event_id):
        """Returns a single calendar event by ID."""
        if calendar_id is None or event_id is None:
            return create_error_response(
                400, "Bad Request", "Calendar ID or event ID is missing"
            )

        event = get_calendar_event(calendar_id, event_id)

        if event is None:
            return create_error_response(
                500, "Internal Server Error", "Failed to fetch the calendar event"
            )

        return Response(json.dumps(event), status=200, mimetype=MASON)

    def put(self, calendar_id, event_id):
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

        return update_calendar_event(
            calendar_id, event_id, event_body=request.get_json()
        )

    def delete(self, calendar_id, event_id):
        """
        Deletes a single calendar event by ID.
        Returns: Response object
        """
        if calendar_id is None or event_id is None:
            return create_error_response(
                400, "Bad Request", "Calendar ID or event ID is missing"
            )

        return delete_calendar_event(calendar_id, event_id)
