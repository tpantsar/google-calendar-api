
from googleapiclient.errors import HttpError

from error import raise_api_error
from logger_config import logger
from utils import build_service, handle_service_build, write_to_file


def get_calendar_list():
    """Fetches the list of calendars from the Google Calendar API."""
    service = handle_service_build(build_service)

    try:
        calendar_list = service.calendarList().list().execute()
        calendars = calendar_list.get("items", [])
        calendar_summaries = [calendar["summary"] for calendar in calendars]

        write_to_file("data.json", calendars)
        logger.info(f"Found {len(calendars)} calendars")
        logger.debug(f"Calendars: {calendar_summaries}")

        return calendars
    except HttpError as error:
        logger.error(f"Google API Error: {error}")
        raise_api_error(
            500, "Google Calendar Error", f"Failed to fetch the calendar list. {error}"
        )
    except Exception as e:
        logger.error(f"Unexpected Error in get_calendar_list: {e}")
        raise_api_error(
            500,
            "Internal Server Error",
            f"An error occurred while fetching the calendar list. {error}",
        )
