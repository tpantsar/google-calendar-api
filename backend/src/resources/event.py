import json

from flask import Response, jsonify, make_response, request
from flask_restful import Resource
from gcalcli.utils import get_time_from_str

from src.constants import JSON, MASON
from src.error import APIError, ParameterError, create_error_response
from src.logger_config import logger
from src.services.event import (
    create_event,
    delete_event,
    get_event,
    get_events,
    update_event,
)


def _build_cors_preflight_response() -> Response:
    response = make_response()
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', '*')
    response.headers.add('Access-Control-Allow-Methods', '*')
    return response


def _corsify_actual_response(response: Response) -> Response:
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


class EventList(Resource):
    """Resource for a list of calendar events."""

    def get(self, calendar_id) -> Response:
        """Returns the calendar events for the specified time range."""
        # Retrieve query parameters from the URL
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        if calendar_id is None:
            return create_error_response(400, 'Bad Request', 'Calendar ID is missing')

        if start_date is None:
            return create_error_response(
                400, 'Bad Request', 'Start date is required for event retrieval'
            )

        if end_date is None:
            return create_error_response(
                400, 'Bad Request', 'End date is required for event retrieval'
            )

        start_date = get_time_from_str(start_date).replace(tzinfo=None).isoformat() + 'Z'
        end_date = get_time_from_str(end_date).replace(tzinfo=None).isoformat() + 'Z'

        try:
            events = get_events(calendar_id, start_date=start_date, end_date=end_date)
            return Response(json.dumps(events), status=200, mimetype=MASON)
        except APIError as e:
            return e.to_response()
        except ParameterError as e:
            return e.to_response()
        except Exception as e:
            logger.error('An unhandled error occurred: %s', e)
            return create_error_response(500, 'Internal Server Error', str(e))

    def post(self, calendar_id) -> Response:
        """
        Creates a new calendar event.
        """
        # https://stackoverflow.com/questions/25594893/how-to-enable-cors-in-flask
        if request.method == 'OPTIONS':  # CORS preflight
            return _build_cors_preflight_response()
        if request.content_type != JSON:
            return create_error_response(
                415, 'Unsupported Media Type', 'Request type must be JSON'
            )

        try:
            response = jsonify(create_event(calendar_id, event_body=request.get_json()))
            return _corsify_actual_response(response)
            # return create_event(calendar_id, event_body=request.get_json())
        except APIError as e:
            return e.to_response()
        except ParameterError as e:
            return e.to_response()
        except Exception as e:
            logger.error('An unhandled error occurred: %s', e)
            return create_error_response(500, 'Internal Server Error', str(e))


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
            logger.error('An unhandled error occurred: %s', e)
            return create_error_response(500, 'Internal Server Error', str(e))

    def put(self, calendar_id, event_id) -> Response:
        """
        Updates a calendar event.
        https://developers.google.com/calendar/api/v3/reference/events/update#python
        PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId

        Returns: Response object
        """
        if request.content_type != JSON:
            return create_error_response(
                415, 'Unsupported Media Type', 'Request type must be JSON'
            )

        try:
            return update_event(calendar_id, event_id, event_body=request.get_json())
        except ParameterError as e:
            return e.to_response()
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error('An unhandled error occurred: %s', e)
            return create_error_response(500, 'Internal Server Error', str(e))

    def delete(self, calendar_id, event_id) -> Response:
        """
        Deletes a single calendar event by ID.
        Returns: Response object
        """
        if calendar_id is None or event_id is None:
            return create_error_response(
                400, 'Bad Request', 'Calendar ID or event ID is missing'
            )

        try:
            delete_event(calendar_id, event_id)
            return Response('Event deleted successfully', status=200)
        except APIError as e:
            return e.to_response()
        except Exception as e:
            return create_error_response(500, 'Internal Server Error', str(e))
