import json

from flask import Response
from flask_restful import Resource

from constants import MASON
from logger_config import logger
from utils import create_error_response, get_calendar_list, write_to_file


class CalendarList(Resource):
    def get(self):
        """
        Returns the list of calendars: /api/calendars/
        """
        calendars = get_calendar_list()

        if calendars is None:
            return create_error_response(
                500, "Internal Server Error", "Failed to fetch the calendar list"
            )

        return Response(json.dumps(calendars), status=200, mimetype=MASON)


class CalendarListId(Resource):
    def get(self):
        """
        Returns the list of calendar IDs: /api/calendars/id
        """
        calendars = get_calendar_list()

        if calendars is None:
            return create_error_response(
                500, "Internal Server Error", "Failed to fetch the calendar list"
            )

        write_to_file("data.json", calendars)
        logger.info(f"Found {len(calendars)} calendars")

        calendar_ids = [
            {"summary": calendar["summary"], "id": calendar["id"]}
            for calendar in calendars
        ]

        return Response(json.dumps(calendar_ids), status=200, mimetype=MASON)
