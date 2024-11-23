from googleapiclient.errors import HttpError

from error import APIError, ServiceBuildError
from logger_config import logger
from utils import build_service, write_to_file


def get_calendar_list():
    """Fetches the list of calendars from the Google Calendar API."""
    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
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
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to fetch the calendar list. {error}",
        )
    except Exception as e:
        raise APIError(
            500,
            "Internal Server Error",
            f"Unexpected error occurred while fetching the calendar list. {e}",
        )
