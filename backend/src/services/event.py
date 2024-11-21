import json
from datetime import datetime

from flask import Response
from googleapiclient.errors import HttpError

from constants import MASON
from logger_config import logger
from utils import build_service, create_error_response, format_event_time, write_to_file


def get_calendar_event(calendar_id, event_id) -> Response:
    """Fetches a single calendar event by ID."""
    service = build_service()

    if service is None:
        logger.error("Failed to build the Calendar API service")
        return create_error_response(
            500, "Internal Server Error", "Failed to build the Calendar API service"
        )

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Found event with ID {event_id}")
        return Response(json.dumps(event), status=200, mimetype=MASON)
    except HttpError as error:
        logger.error(f"An error occurred with fetching the event: {error}")
        return create_error_response(500, "Internal Server Error", str(error))


def get_calendar_events(calendar_id, year) -> Response:
    """Fetches Google Calendar events for the specified year."""
    service = build_service()

    if service is None:
        logger.error("Failed to build the Calendar API service")
        return create_error_response(
            500, "Internal Server Error", "Failed to build the Calendar API service"
        )

    # Define the time range for the year
    start_date = datetime(year, 1, 1).isoformat() + "Z"
    end_date = datetime(year, 12, 31, 23, 59, 59).isoformat() + "Z"

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
    return Response(json.dumps(events), status=200, mimetype=MASON)


def create_calendar_event(calendar_id, event_body) -> Response:
    """
    Creates a new calendar event.
    POST https://www.googleapis.com/calendar/v3/calendars/calendarId/events
    https://developers.google.com/calendar/api/v3/reference/events/insert

    Required properties in the event body:
    - end: The end time of the event.
    - start: The start time of the event.
    """
    if calendar_id is None or event_body is None:
        logger.error("Calendar ID or event body is missing")
        return create_error_response(
            400, "Bad Request", "Calendar ID or event body is missing"
        )

    logger.debug(f"Calendar ID: {calendar_id}")
    logger.debug(f"Event body: {event_body}")

    service = build_service()

    try:
        event = (
            service.events().insert(calendarId=calendar_id, body=event_body).execute()
        )
        logger.info(f"Event created successfully: {event['id']}")

        # Return a response with 201 (created) status code
        return Response(json.dumps(event), status=201, mimetype=MASON)
    except HttpError as error:
        logger.error(f"An error occurred with creating the event: {error}")
        return create_error_response(500, "Internal Server Error", str(error))


def delete_calendar_event(calendar_id, event_id) -> Response:
    """
    Deletes a single calendar event.
    DELETE https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None:
        logger.error("Calendar ID or event ID is missing")
        return create_error_response(
            400, "Bad Request", "Calendar ID or event ID is missing"
        )

    service = build_service()

    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Event with ID {event_id} deleted successfully")

        # Return a response with 200 (content) or 204 (no content) status code
        return Response(
            response="Event deleted successfully",
            status=200,
            mimetype=MASON,
        )
    except HttpError as error:
        logger.error(f"An error occurred with deleting the event: {error}")
        return create_error_response(500, "Internal Server Error", str(error))


def update_calendar_event(calendar_id, event_id, event_body) -> Response:
    """
    Updates a calendar event.
    PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None or event_body is None:
        logger.error("Calendar ID or event ID or event body is missing")
        return create_error_response(
            400, "Bad Request", "Calendar ID or event ID or event body is missing"
        )

    logger.debug(f"Calendar ID: {calendar_id}")
    logger.debug(f"Event ID: {event_id}")
    logger.debug(f"Event body: {event_body}")
    service = build_service()

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
        return Response(json.dumps(updated_event), status=200, mimetype=MASON)
    except HttpError as error:
        logger.error(f"An error occurred with updating the event: {error}")
        return create_error_response(500, "Internal Server Error", str(error))
