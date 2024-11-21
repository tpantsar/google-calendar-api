import json

from flask import Response, request
from flask_restful import Resource

from constants import JSON, MASON
from logger_config import logger
from utils import create_error_response, get_calendar_list, write_to_file


class CalendarCollection(Resource):
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


class CalendarIdCollection(Resource):
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
