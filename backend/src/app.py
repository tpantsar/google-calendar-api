import datetime

from flask import Flask, Response, request

from constants import JSON, MASON
from logger_config import logger
from utils import (
    build_service,
    create_error_response,
    delete_calendar_event,
    get_calendar_events,
    get_calendar_list,
    update_calendar_event,
    write_to_file,
)

app = Flask(__name__)

# Set Google API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@app.get("/api/calendars")
def get_calendars_list():
    """Returns the list of calendars."""
    calendars = get_calendar_list()

    # Return the list of calendars
    return calendars


@app.get("/api/calendars/id")
def get_calendars_id_list():
    """Returns the list of calendar IDs."""
    service = build_service()

    calendar_list = service.calendarList().list().execute()
    calendars = calendar_list.get("items", [])
    write_to_file("data.json", calendars)

    logger.info(f"Found {len(calendars)} calendars")
    calendar_summaries = [calendar["summary"] for calendar in calendars]
    logger.debug(f"Calendars: {calendar_summaries}")

    result = [
        {"summary": calendar["summary"], "id": calendar["id"]} for calendar in calendars
    ]
    write_to_file("calendars.json", result)

    # Return the list of calendar IDs
    return result


@app.get("/api/events/<calendar_id>")
def get_events_for_current_year(calendar_id):
    """Returns the calendar events for the current year."""
    current_year = datetime.datetime.now().year
    events = get_calendar_events(calendar_id, current_year)
    return events


@app.get("/api/events/<int:year>/<calendar_id>")
def get_events_for_year(year, calendar_id):
    """Returns the calendar events for the specified year."""
    events = get_calendar_events(calendar_id, year)
    return events


@app.delete("/api/events/delete/<calendar_id>/<event_id>")
def delete_event(calendar_id, event_id):
    delete_calendar_event(calendar_id, event_id)

    response = {"message": "Event deleted successfully"}
    return Response(response=response, status=204, mimetype=MASON)


@app.put("/api/events/update/<calendar_id>/<event_id>")
def update_event(calendar_id, event_id):
    """
    Updates a calendar event.
    https://developers.google.com/calendar/api/v3/reference/events/update#python
    PUT https://www.googleapis.com/calendar/v3/calendars/calendarId/events/eventId
    """
    if request.content_type != JSON:
        return create_error_response(
            415, "Unsupported Media Type", "Request type must be JSON"
        )

    event_body = request.get_json()
    update_calendar_event(calendar_id, event_id, event_body)
    response = {"message": "Event updated successfully"}
    return Response(response=response, status=200, mimetype=MASON)


if __name__ == "__main__":
    app.run(debug=True)
