from collections import Counter
from datetime import datetime, timedelta

from gcalcli.utils import get_time_from_str
from gcalcli.validators import parsable_date_validator
from googleapiclient.errors import HttpError

from src.error import APIError, ParameterError, ServiceBuildError
from src.logger_config import logger
from src.utils import build_service, format_event_time_from_iso, write_to_output_file


def get_event(calendar_id, event_id):
    """Fetches a single calendar event by ID."""
    if calendar_id is None or event_id is None:
        raise ParameterError('Calendar ID or event ID is missing')

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        # Add computed properties to the event
        event = update_event_properties(event)

        logger.info('Found event with ID %s', event_id)
        return event
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to fetch the event. {error}',
        )
    except KeyError as e:
        raise APIError(
            500,
            'Event Properties Error',
            f'Failed to update computed event properties. {str(e)}',
        )


def get_events(
    calendar_id, start_date: datetime, end_date: datetime, search_query: str = None
):
    """
    Fetches Google Calendar events for the specified time range.
    Reference: https://developers.google.com/calendar/api/v3/reference/events/list

    start_date: The start date of the time range (RFC3339 timestamp).
    end_date: The end date of the time range (RFC3339 timestamp).
    RFC3339 timestamp must have mandatory time zone offset, for example:
    2011-06-03, 2011-06-03T10:00:00-07:00, 2011-06-03T10:00:00Z.

    search_query: Optional search query to filter events by title or description.
    """
    logger.info(
        'Fetching events from %s between %s and %s',
        calendar_id,
        start_date,
        end_date,
    )

    if calendar_id is None:
        raise ParameterError('Calendar ID is missing')
    if start_date is None or end_date is None:
        raise ParameterError('Start date or end date is missing')
    if (
        get_time_from_str(start_date).timestamp()
        > get_time_from_str(end_date).timestamp()
    ):
        raise ParameterError('Start date is after the end date')

    # Validate and parse the start_date and end_date
    try:
        start_date = parsable_date_validator(start_date)
        end_date = parsable_date_validator(end_date)
    except ValueError as e:
        raise ParameterError(f'Invalid date format: {str(e)}')

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,  # Default is 'primary'
                timeMin=start_date,  # RFC3339 timestamp, 2011-06-03T10:00:00Z
                timeMax=end_date,  # RFC3339 timestamp, 2011-06-03T10:00:00Z
                q=search_query,  # Optional search query
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])
        calendar_summary = (
            service.calendars().get(calendarId=calendar_id).execute().get('summary')
        )
        logger.info(
            'Found %d events from %s between %s and %s with search query "%s"',
            len(events),
            calendar_summary,
            start_date,
            end_date,
            search_query,
        )
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to fetch the calendar events. {error}',
        )

    # Sort events by start time in descending order (newest first)
    events.reverse()

    try:
        # Add computed properties to each event
        for event in events:
            event = update_event_properties(event)
    except (KeyError, AttributeError) as e:
        raise APIError(
            500,
            'Event Properties Error',
            f'Failed to update computed event properties. {str(e)}',
        )

    write_to_output_file('events.json', events)
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
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        # Fetch all events from the calendar
        now = datetime.now()
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=(now - timedelta(days=365)).isoformat() + 'Z',
                timeMax=now.isoformat() + 'Z',
                maxResults=1000,  # Fetch a larger dataset for frequency analysis
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])
        logger.info('Found %d events in the calendar', len(events))
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to fetch events from the calendar. {error}',
        )

    # Analyze and find the top 10 most frequent event summaries
    try:
        # Count the frequency of each event summary
        summaries = [event.get('summary', 'Untitled Event') for event in events]
        summary_counts = Counter(summaries)

        # Get the top 10 most common summaries and their frequencies
        top_summary_counts = summary_counts.most_common(10)
        logger.info('Top 10 popular events with counts: %s', top_summary_counts)
    except KeyError as e:
        raise APIError(
            500,
            'Event Analysis Error',
            f'Failed to analyze event frequencies. {str(e)}',
        )

    # Write detailed events to a file (optional for debugging)
    write_to_output_file('popular_events.json', events)

    # Return a dictionary of the top 10 summaries with their counts
    return {summary: count for summary, count in top_summary_counts}


def get_recent_unique_events(calendar_id) -> list[str]:
    """
    Fetches the summaries of the 10 most recent unique events (by summary)
    from the selected calendar.
    Prioritizes recency while filtering out duplicate summaries.
    """
    try:
        service = build_service()
    except Exception as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        # Fetch events ordered by start time, descending
        now = datetime.now()
        events_result = (
            service.events()
            .list(
                calendarId=calendar_id,
                timeMin=(now - timedelta(days=365)).isoformat() + 'Z',
                timeMax=now.isoformat() + 'Z',
                maxResults=1000,  # Fetch a larger dataset to ensure uniqueness
                singleEvents=True,
                orderBy='startTime',
            )
            .execute()
        )
        events = events_result.get('items', [])
        logger.info('Found %d events in the calendar', len(events))
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to fetch events from the calendar. {error}',
        )

    # Extract and filter unique summaries by recency
    try:
        unique_events = {}
        recent_events = []

        # Reverse to prioritize more recent events (descending)
        for event in reversed(events):
            summary = event.get('summary', 'Untitled Event')
            if summary not in unique_events:
                unique_events[summary] = event
                recent_events.append(event)

            if len(recent_events) == 10:  # Stop once we have 10 unique events
                break

        logger.info('Found %d unique recent events', len(recent_events))
    except KeyError as e:
        raise APIError(
            500,
            'Event Processing Error',
            f'Failed to process unique events. {str(e)}',
        )

    # Write detailed events to a file (optional for debugging)
    write_to_output_file('recent_unique_events.json', recent_events)

    # Return the summaries of the 10 most recent unique events
    return [event.get('summary', 'Untitled Event') for event in recent_events]


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
        raise ParameterError('Calendar ID or event body is missing')

    logger.debug('Calendar ID: %s', calendar_id)
    logger.debug('Event body: %s', event_body)

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        event = service.events().insert(calendarId=calendar_id, body=event_body).execute()

        # Add computed properties to the event
        event = update_event_properties(event)

        logger.info('Event created successfully: %s', event.get('id'))
        return event
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to create the event. {error}',
        )
    except KeyError as e:
        raise APIError(
            500,
            'Event Properties Error',
            f'Failed to update computed event properties. {str(e)}',
        )


def delete_event(calendar_id, event_id):
    """
    Deletes a single calendar event.
    DELETE https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if calendar_id is None or event_id is None:
        raise ParameterError('Calendar ID or event ID is missing')

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        service.events().delete(calendarId=calendar_id, eventId=event_id).execute()
        logger.info('Event with ID %s deleted successfully', event_id)
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to delete the event. {error}',
        )


def update_event(calendar_id, event_id, event_body):
    """
    Updates a calendar event.
    PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    https://developers.google.com/calendar/api/v3/reference/events/update
    """
    if calendar_id is None or event_id is None or event_body is None:
        raise ParameterError('Calendar ID or event ID or event body is missing')

    logger.debug('Calendar ID: %s', calendar_id)
    logger.debug('Event ID: %s', event_id)
    logger.debug('Event body: %s', event_body)

    try:
        service = build_service()
    except ServiceBuildError as e:
        raise APIError(
            500, 'Service Build Error', f'Failed to build the service: {str(e)}'
        )

    try:
        # First retrieve the event from the API
        event = service.events().get(calendarId=calendar_id, eventId=event_id).execute()

        # Update the event with the new body
        event['summary'] = event_body['summary']

        # Update the event with the new body
        updated_event = (
            service.events()
            .update(calendarId=calendar_id, eventId=event['id'], body=event)
            .execute()
        )

        updated_event = update_event_properties(updated_event)

        logger.info('Event with ID %s updated successfully', event_id)
        logger.info('Event body: %s', event_body)
        return updated_event
    except HttpError as error:
        raise APIError(
            500,
            'Google Calendar API Error',
            f'Failed to update computed event properties. {error}',
        )
    except KeyError as e:
        raise APIError(
            500,
            'Event Properties Error',
            f'Failed to update computed event properties. {str(e)}',
        )


def update_event_properties(event: dict):
    """Updates the properties of a single calendar event."""
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['end'].get('date'))
    event['formatted_start'] = format_event_time_from_iso(start)
    event['formatted_end'] = format_event_time_from_iso(end)

    # Calculate the duration of the event in hours
    time_difference = datetime.fromisoformat(end) - datetime.fromisoformat(start)
    event['duration'] = time_difference.total_seconds() / 3600

    return event
