from datetime import datetime

from googleapiclient.errors import HttpError

from error import ParameterError, raise_api_error
from logger_config import logger
from utils import (
    build_service,
    create_error_response,
    format_event_time,
    handle_service_build,
    write_to_file,
)


def get_event(calendar_id, event_id):
    """Fetches a single calendar event by ID."""
    if calendar_id is None or event_id is None:
        raise ParameterError("Calendar ID or event ID is missing")

    service = handle_service_build(build_service)

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Found event with ID {event_id}")
        return event
    except HttpError as error:
        logger.error(f"An error occurred with fetching the event: {error}")
        raise_api_error(500, "Google API Error", str(error))


def get_events(calendar_id, year):
    """Fetches Google Calendar events for the specified year."""
    service = handle_service_build(build_service)

    # Define the time range for the year
    start_date = datetime(year, 1, 1).isoformat() + "Z"
    end_date = datetime(year, 12, 31, 23, 59, 59).isoformat() + "Z"

    try:
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
        calendar_summary = (
            service.calendars().get(calendarId=calendar_id).execute().get("summary")
        )
        logger.info(
            f"Found {len(events)} events from {calendar_summary} for the year {year}"
        )
    except HttpError as error:
        logger.error(f"An error occurred with fetching the events: {error}")
        raise_api_error(
            500,
            "Google Calendar Error",
            f"Failed to fetch the calendar events. {error}",
        )

    # Sort events by start time in descending order (newest first)
    events.reverse()

    # Add formatted start and end times to the events
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        event["formatted_start"] = format_event_time(start)
        event["formatted_end"] = format_event_time(end)

        # Convert the time difference to hours
        time_difference = datetime.fromisoformat(end) - datetime.fromisoformat(start)
        event["duration"] = time_difference.total_seconds() / 3600

    write_to_file("events.json", events)
    return events


def create_event(calendar_id, event_body):
    """
    Creates a new calendar event.
    POST https://www.googleapis.com/calendar/v3/calendars/calendarId/events
    https://developers.google.com/calendar/api/v3/reference/events/insert

    Required properties in the event body:
    - end: The end time of the event.
    - start: The start time of the event.
    """
    if calendar_id is None or event_body is None:
        raise ParameterError("Calendar ID or event body is missing")

    logger.debug(f"Calendar ID: {calendar_id}")
    logger.debug(f"Event body: {event_body}")

    service = handle_service_build(build_service)

    try:
        event = (
            service.events().insert(calendarId=calendar_id, body=event_body).execute()
        )
        logger.info(f"Event created successfully: {event['id']}")
        return event
    except HttpError as error:
        logger.error(f"An error occurred with creating the event: {error}")
        raise_api_error(500, "Calendar API error", str(error))


def delete_event(calendar_id, event_id):
    """
    Deletes a single calendar event.
    DELETE https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None:
        raise ParameterError("Calendar ID or event ID is missing")

    service = handle_service_build(build_service)

    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Event with ID {event_id} deleted successfully")
    except HttpError as error:
        logger.error(f"An error occurred with deleting the event: {error}")
        raise_api_error(500, "Google API Error", str(error))


def update_event(calendar_id, event_id, event_body):
    """
    Updates a calendar event.
    PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None or event_body is None:
        logger.error("Calendar ID or event ID or event body is missing")
        raise create_error_response(
            400, "Bad Request", "Calendar ID or event ID or event body is missing"
        )

    logger.debug(f"Calendar ID: {calendar_id}")
    logger.debug(f"Event ID: {event_id}")
    logger.debug(f"Event body: {event_body}")

    service = handle_service_build(build_service)

    try:
        # First retrieve the event from the API
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        # Update the event with the new body
        event["summary"] = event_body["summary"]

        # Update the event with the new body
        updated_event = (
            service.events()
            .update(calendarId=calendar_id, eventId=event["id"], body=event)
            .execute()
        )
        logger.info(f"Event with ID {event_id} updated successfully")
        logger.info(f"Event body: {event_body}")
        return updated_event
    except HttpError as error:
        logger.error(f"An error occurred with updating the event: {error}")
        raise create_error_response(500, "Internal Server Error", str(error))
