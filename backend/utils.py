import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from logger_config import logger


def get_calendar_events(calendar_id, year):
    """Fetches Google Calendar events for the specified year."""
    creds = get_credentials()
    service = build_service(creds)

    if service is None:
        logger.error("Failed to build the Calendar API service")
        return []

    # Define the time range for the year
    start_date = datetime.datetime(year, 1, 1).isoformat() + "Z"
    end_date = datetime.datetime(year, 12, 31, 23, 59, 59).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId=calendar_id,  # Default is 'primary'
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])
    calendar = service.calendars().get(calendarId=calendar_id).execute().get("summary")
    logger.info(f"Found {len(events)} events from {calendar} for the year {year}")

    # Sort events by start time in descending order (newest first)
    events.reverse()

    # Format the start and end times of each event
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        event["formatted_start"] = format_event_time(start)
        event["formatted_end"] = format_event_time(end)

    return events


def get_calendar_list(creds):
    """Fetches the list of calendars from the Google Calendar API."""
    service = build_service(creds)
    calendar_list = service.calendarList().list().execute()

    calendars = calendar_list.get("items", [])
    logger.info(f"Found {len(calendars)} calendars")
    logger.debug(f"Calendars: {calendars}")

    for calendar in calendars:
        logger.info(f"Calendar: {calendar['summary']}")

    return calendars


def build_service(creds):
    """
    Build the Calendar API service and return it.
    creds is the credentials object to use for building the service.
    """
    try:
        service = build("calendar", "v3", credentials=creds)
    except HttpError as error:
        logger.error(f"An error occurred with building the service: {error}")
        return None
    return service


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
