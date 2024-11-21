import json

from flask import Response
from googleapiclient.errors import HttpError

from constants import MASON
from logger_config import logger
from utils import build_service, create_error_response, write_to_file


class CalendarServiceError(Exception):
    """Custom exception for CalendarService errors."""

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


def get_calendar_list():
    """Fetches the list of calendars from the Google Calendar API."""
    service = build_service()

    if service is None:
        logger.error("Failed to build the Calendar API service")
        raise create_error_response(
            500, "Internal Server Error", "Failed to build the Calendar API service"
        )

    try:
        calendar_list = service.calendarList().list().execute()

        calendars = calendar_list.get("items", [])
        calendar_summaries = [calendar["summary"] for calendar in calendars]

        write_to_file("data.json", calendars)
        logger.info(f"Found {len(calendars)} calendars")
        logger.debug(f"Calendars: {calendar_summaries}")

        return calendars
    except HttpError as error:
        logger.error(f"An error occurred with fetching the calendar list: {error}")
        raise create_error_response(500, "Internal Server Error", str(error))
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        raise CalendarServiceError(f"Failed to fetch calendar list: {str(e)}")
