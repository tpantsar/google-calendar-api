import csv
import json
from datetime import datetime

from flask import Response, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from constants import ERROR_PROFILE, MASON
from logger_config import logger
from mason import MasonBuilder


def write_to_file(file_name, data):
    """Writes the data to a file depending on the file format."""
    if file_name.endswith(".json"):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
        logger.info(f"Data written to {file_name}")
    elif file_name.endswith(".csv"):
        with open(file_name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        logger.info(f"Data written to {file_name}")
    elif file_name.endswith(".txt"):
        with open(file_name, "w", encoding="utf-8") as file:
            for item in data:
                file.write(f"{item}\n", encoding="utf-8")
        logger.info(f"Data written to {file_name}")
    else:
        logger.error("Unsupported file format")


def get_calendar_event(calendar_id, event_id):
    """Fetches a single calendar event by ID."""
    service = build_service()

    if service is None:
        logger.error("Failed to build the Calendar API service")
        return None

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Found event with ID {event_id}")
        return event
    except HttpError as error:
        logger.error(f"An error occurred with fetching the event: {error}")
        return None


def get_calendar_events(calendar_id, year):
    """Fetches Google Calendar events for the specified year."""
    service = build_service()

    if service is None:
        logger.error("Failed to build the Calendar API service")
        return None

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
    return events


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


def get_calendar_list():
    """Fetches the list of calendars from the Google Calendar API."""
    service = build_service()

    try:
        calendar_list = service.calendarList().list().execute()

        calendars = calendar_list.get("items", [])
        calendar_summaries = [calendar["summary"] for calendar in calendars]

        logger.info(f"Found {len(calendars)} calendars")
        logger.debug(f"Calendars: {calendar_summaries}")

        return calendars
    except HttpError as error:
        logger.error(f"An error occurred with fetching the calendar list: {error}")
        return None


def create_error_response(status_code, title, message=None) -> Response:
    """
    Create an error response with the given status code and title.

    Parameters:
    - status_code: The HTTP status code.
    - title: The title of the error.
    - message: An optional message describing the error.

    Returns:
    - A dictionary containing the error response.
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


def build_service() -> build:
    """
    Build the Calendar API service and return it.
    creds is the credentials object used for building the service.
    """
    try:
        creds = get_credentials()
        if creds is None:
            logger.error("Failed to get the credentials")
            return None

        service = build("calendar", "v3", credentials=creds)
        if service is None:
            logger.error("Failed to build the Calendar API service")
            return None

        return service
    except HttpError as error:
        logger.error(f"An error occurred with building the service: {error}")
        return None


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
