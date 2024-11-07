from flask import Flask, render_template

from auth import get_credentials
from logger_config import logger
from utils import build_service, get_calendar_events, get_calendar_list

app = Flask(__name__)

# Set Google API scopes
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]


@app.route("/year/<int:year>/<calendar_id>")
def year_view(year, calendar_id):
    """Displays the year view with calendar events."""
    events = get_calendar_events(calendar_id, year)
    creds = get_credentials()
    service = build_service(creds=creds)

    calendar = service.calendars().get(calendarId=calendar_id).execute()
    calendar_name = calendar.get("summary")
    logger.info(f"Displaying the year view for {calendar_name} for the year {year}")

    # Pass events to the template
    return render_template(
        "calendar_view.html", calendar=calendar_name, events=events, year=year
    )


@app.route("/calendars")
def calendars_view():
    """Displays the list of calendars."""
    creds = get_credentials()
    calendars = get_calendar_list(creds)

    # Pass calendars to the template
    return render_template("calendar_list.html", calendars=calendars)


if __name__ == "__main__":
    app.run(debug=True)
