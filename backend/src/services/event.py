from collections import Counter
from datetime import datetime, timedelta

from googleapiclient.errors import HttpError

from error import APIError, ParameterError, ServiceBuildError
from logger_config import logger
from utils import build_service, format_event_time, write_to_file


def get_event(calendar_id, event_id):
    """Fetches a single calendar event by ID."""
    if calendar_id is None or event_id is None:
        raise ParameterError("Calendar ID or event ID is missing")

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        # Add computed properties to the event
        event = update_event_properties(event)

        logger.info(f"Found event with ID {event_id}")
        return event
    except HttpError as error:
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to fetch the event. {error}",
        )
    except KeyError as e:
        raise APIError(
            500,
            "Event Properties Error",
            f"Failed to update computed event properties. {str(e)}",
        )


def get_events(calendar_id, year):
    """Fetches Google Calendar events for the specified year."""
    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

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
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to fetch the calendar events. {error}",
        )

    # Sort events by start time in descending order (newest first)
    events.reverse()

    try:
        # Add computed properties to each event
        for event in events:
            event = update_event_properties(event)
    except KeyError as e:
        raise APIError(
            500,
            "Event Properties Error",
            f"Failed to update computed event properties. {str(e)}",
        )

    write_to_file("events.json", events)
    return events


def get_popular_events(calendar_id):
    """
    Fetches the summaries and counts of the maximum of 10 most frequently occurring events
    from the past in selected calendar.
    """
    try:
        service = build_service()
    except Exception as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

    try:
        # Fetch all events from the calendar
        now = datetime.now()
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=(now - timedelta(days=365)).isoformat() + "Z",
                timeMax=now.isoformat() + "Z",
                maxResults=1000,  # Fetch a larger dataset for frequency analysis
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])
        logger.info(f"Found {len(events)} events in the calendar")
    except HttpError as error:
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to fetch events from the calendar. {error}",
        )

    # Analyze and find the top 10 most frequent event summaries
    try:
        # Count the frequency of each event summary
        summaries = [event.get("summary", "Untitled Event") for event in events]
        summary_counts = Counter(summaries)

        # Get the top 10 most common summaries and their frequencies
        top_summary_counts = summary_counts.most_common(10)
        logger.info(f"Top 10 popular events with counts: {top_summary_counts}")
    except KeyError as e:
        raise APIError(
            500,
            "Event Analysis Error",
            f"Failed to analyze event frequencies. {str(e)}",
        )

    # Write detailed events to a file (optional for debugging)
    write_to_file("popular_events.json", events)

    # Return a dictionary of the top 10 summaries with their counts
    return {summary: count for summary, count in top_summary_counts}


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

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

    try:
        event = (
            service.events().insert(calendarId=calendar_id, body=event_body).execute()
        )

        # Add computed properties to the event
        event = update_event_properties(event)

        logger.info(f"Event created successfully: {event['id']}")
        return event
    except HttpError as error:
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to create the event. {error}",
        )
    except KeyError as e:
        raise APIError(
            500,
            "Event Properties Error",
            f"Failed to update computed event properties. {str(e)}",
        )


def delete_event(calendar_id, event_id):
    """
    Deletes a single calendar event.
    DELETE https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None:
        raise ParameterError("Calendar ID or event ID is missing")

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        logger.info(f"Event with ID {event_id} deleted successfully")
    except HttpError as error:
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to delete the event. {error}",
        )


def update_event(calendar_id, event_id, event_body):
    """
    Updates a calendar event.
    PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    https://developers.google.com/calendar/api/v3/reference/events/update
    """
    if calendar_id is None or event_id is None or event_body is None:
        raise ParameterError("Calendar ID or event ID or event body is missing")

    logger.debug(f"Calendar ID: {calendar_id}")
    logger.debug(f"Event ID: {event_id}")
    logger.debug(f"Event body: {event_body}")

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, "Service Build Error", f"Failed to build the service: {str(e)}"
        )

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

        updated_event = update_event_properties(updated_event)

        logger.info(f"Event with ID {event_id} updated successfully")
        logger.info(f"Event body: {event_body}")
        return updated_event
    except HttpError as error:
        raise APIError(
            500,
            "Google Calendar API Error",
            f"Failed to update computed event properties. {error}",
        )
    except KeyError as e:
        raise APIError(
            500,
            "Event Properties Error",
            f"Failed to update computed event properties. {str(e)}",
        )


def update_event_properties(event: dict):
    """Updates the properties of a single calendar event."""
    start = event["start"].get("dateTime", event["start"].get("date"))
    end = event["end"].get("dateTime", event["end"].get("date"))
    event["formatted_start"] = format_event_time(start)
    event["formatted_end"] = format_event_time(end)

    # Calculate the duration of the event in hours
    time_difference = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    event["duration"] = time_difference.total_seconds() / 3600

    return event
