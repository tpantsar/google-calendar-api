from datetime import datetime, timedelta, timezone

import pytz
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, ValidationError, Validator

from constants import TIME_FORMAT_PROMPT, TIMEZONE
from logger_config import logger
from services.calendar import get_calendar_list
from services.event import create_event, get_recent_unique_events
from utils import print_event_details, round_to_nearest_interval


class DateTimeValidator(Validator):
    def __init__(
        self, message: str = "Invalid date format. Use YYYY-MM-DD HH:MM"
    ) -> None:
        self._message = message

    def validate(self, document) -> None:
        try:
            datetime.strptime(document.text, TIME_FORMAT_PROMPT)
        except ValueError:
            raise ValidationError(
                message=self._message, cursor_position=document.cursor_position
            )


def format_datetime(datetime_str, timezone_str):
    local_timezone = pytz.timezone(timezone_str)
    dt = datetime.strptime(datetime_str, TIME_FORMAT_PROMPT)
    dt = local_timezone.localize(dt)
    return dt.isoformat()


def main():
    # Fetch calendar list
    calendars = get_calendar_list()
    calendar_choices = [
        {"name": calendar["summary"], "value": calendar["id"]} for calendar in calendars
    ]

    menu_choices = ["Fast", "Custom"]
    menu = inquirer.select(
        message="Method:",
        choices=menu_choices,
        default="Fast",  # Optional: Set a default choice
        validate=EmptyInputValidator(),
    )

    # Display calendar menu with filtering enabled
    selected_calendar_id = inquirer.fuzzy(
        message="Select calendar:",
        choices=calendar_choices,
        default=None,  # Optional: Set a default choice
        validate=EmptyInputValidator(),
    ).execute()

    print(f"Using calendar: {selected_calendar_id}")

    if menu.execute() == "Fast":
        fast(selected_calendar_id)
    else:
        custom(selected_calendar_id)


def fast(selected_calendar_id: str):
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
    logger.debug(f"Start: {start}, End: {end}")

    start_formatted = start.isoformat()
    end_formatted = end.isoformat()

    event_body = {
        "start": {"dateTime": start_formatted, "timeZone": TIMEZONE},
        "end": {"dateTime": end_formatted, "timeZone": TIMEZONE},
        "summary": summary,
        "description": description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(event, float(duration), start, end)


def custom(selected_calendar_id: str):
    events = get_recent_unique_events(selected_calendar_id)
    for event in events:
        print(event)
    popular_events_summaries = {event: None for event in events}
    duration = 1

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

    start = inquirer.text(
        message="Start time",
        default=start.strftime(TIME_FORMAT_PROMPT),
        validate=DateTimeValidator(),
    ).execute()

    end = inquirer.text(
        message="End time",
        default=end.strftime(TIME_FORMAT_PROMPT),
        validate=DateTimeValidator(),
    ).execute()

    start_formatted = format_datetime(start, TIMEZONE)
    print(start_formatted)

    end_formatted = format_datetime(end, TIMEZONE)
    print(end_formatted)

    event_body = {
        "start": {"dateTime": start_formatted, "timeZone": TIMEZONE},
        "end": {"dateTime": end_formatted, "timeZone": TIMEZONE},
        "summary": summary,
        "description": description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(
        event,
        duration,
        datetime.strptime(start, TIME_FORMAT_PROMPT),
        datetime.strptime(end, TIME_FORMAT_PROMPT),
    )


if __name__ == "__main__":
    main()
