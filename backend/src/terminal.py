from datetime import datetime, timedelta, timezone

import pytz
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from constants import TIMEZONE
from services.calendar import get_calendar_list
from services.event import create_event, get_recent_unique_events
from utils import round_to_nearest_interval


def main():
    # Fetch calendar list
    calendars = get_calendar_list()
    choices = [
        {"name": calendar["summary"], "value": calendar["id"]} for calendar in calendars
    ]

    # Display calendar menu with filtering enabled
    selected_calendar_id = inquirer.fuzzy(
        message="Select calendar:",
        choices=choices,
        default=None,  # Optional: Set a default choice
        validate=EmptyInputValidator(),
    ).execute()

    # Print the selected calendar ID
    print(f"Using calendar: {selected_calendar_id}")

    # Duration of the event in hours
    duration = inquirer.number(
        message="Duration in hours",
        min_allowed=0,
        max_allowed=24,
        float_allowed=True,
        default=None,
        replace_mode=True,
        validate=EmptyInputValidator(),
    ).execute()

    events = get_recent_unique_events(selected_calendar_id)
    for event in events:
        print(event)
    popular_events_summaries = {event: None for event in events}

    # Event summary with auto-complete from popular events
    # https://inquirerpy.readthedocs.io/en/latest/pages/prompts/input.html#auto-completion
    summary = inquirer.text(
        message="Summary",
        completer=popular_events_summaries,
        validate=EmptyInputValidator(),
    ).execute()

    # Event description
    description = inquirer.text(
        message="Description",
        validate=EmptyInputValidator(),
    ).execute()

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)
    current_utc_time = datetime.now(timezone.utc)
    current_local_time = current_utc_time.astimezone(local_timezone)

    end = round_to_nearest_interval(current_local_time, 15)
    start = end - timedelta(hours=float(duration))

    start_formatted = start.isoformat()
    end_formatted = end.isoformat()

    event_body = {
        "start": {"dateTime": start_formatted, "timeZone": TIMEZONE},
        "end": {"dateTime": end_formatted, "timeZone": TIMEZONE},
        "summary": summary,
        "description": description,
    }

    event = create_event(selected_calendar_id, event_body)

    TIME_FORMAT = "%d.%m.%Y %H.%M"

    print("\nEvent created successfully:")
    print("{:<12}{:<}".format("Summary:", event["summary"]))
    print("{:<12}{:<}".format("Desc:", event["description"]))
    print("{:<12}{:<}".format("Duration:", str(duration) + " hours"))
    print("{:<12}{:<}".format("Start:", start.strftime(TIME_FORMAT)))
    print("{:<12}{:<}".format("End:", end.strftime(TIME_FORMAT)))
    print(event.get("htmlLink"))


if __name__ == "__main__":
    main()
