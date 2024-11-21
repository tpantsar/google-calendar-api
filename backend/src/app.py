import datetime

from flask import Flask, Response, request

from api import api_bp
from constants import JSON, MASON
from utils import (
    create_error_response,
    delete_calendar_event,
    get_calendar_events,
    update_calendar_event,
)

app = Flask(__name__)
app.register_blueprint(api_bp)

# Set Google API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


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
