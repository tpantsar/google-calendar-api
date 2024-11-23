import json

from flask import Response
from flask_restful import Resource

from constants import MASON
from error import APIError, create_error_response
from logger_config import logger
from services.calendar import get_calendar_list


class CalendarList(Resource):
    def get(self) -> Response:
        """
        Returns the list of calendars.
        """
        try:
            calendars = get_calendar_list()
            return Response(json.dumps(calendars), status=200, mimetype=MASON)
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"Unhandled Error in get_calendars: {e}")
            return create_error_response(500, "Internal Server Error", str(e))


class CalendarListId(Resource):
    def get(self) -> Response:
        """
        Returns the list of calendar IDs: /api/calendars/id
        """
        try:
            calendars = get_calendar_list()
            calendar_ids = [
                {"summary": calendar["summary"], "id": calendar["id"]}
                for calendar in calendars
            ]
            return Response(json.dumps(calendar_ids), status=200, mimetype=MASON)
        except APIError as e:
            return e.to_response()
        except Exception as e:
            logger.error(f"Unhandled Error in get_calendars: {e}")
            return create_error_response(500, "Internal Server Error", str(e))
