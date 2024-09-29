from flask import Flask, render_template
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import datetime

app = Flask(__name__)

# Set Google API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")


def get_calendar_events(year):
    """Fetches Google Calendar events for the specified year."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    service = build("calendar", "v3", credentials=creds)

    # Define the time range for the year
    start_date = datetime.datetime(year, 1, 1).isoformat() + "Z"
    end_date = datetime.datetime(year, 12, 31, 23, 59, 59).isoformat() + "Z"

    events_result = (
        service.events()
        .list(
            calendarId="primary",
            timeMin=start_date,
            timeMax=end_date,
            singleEvents=True,
            orderBy="startTime",
        )
        .execute()
    )

    events = events_result.get("items", [])

    # Sort events by start time in descending order (newest first)
    events.reverse()

    # Format the start and end times of each event
    for event in events:
        start = event["start"].get("dateTime", event["start"].get("date"))
        end = event["end"].get("dateTime", event["end"].get("date"))
        event["formatted_start"] = format_event_time(start)
        event["formatted_end"] = format_event_time(end)

    return events


@app.route("/year/<int:year>")
def year_view(year):
    """Displays the year view with calendar events."""
    events = get_calendar_events(year)
    # Pass events to the template
    return render_template("calendar_view.html", events=events, year=year)


if __name__ == "__main__":
    app.run(debug=True)
