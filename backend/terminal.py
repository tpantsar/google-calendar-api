from datetime import datetime, timedelta, timezone

import pytz
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator, ValidationError, Validator

from src.constants import TIME_FORMAT_PROMPT, TIMEZONE
from src.logger_config import logger
from src.printer import Printer
from src.services.calendar import get_calendar_list
from src.services.event import create_event, get_recent_unique_events
from src.utils import (
    get_time_from_str,
    get_timedelta_from_str,
    print_event_details,
    round_to_nearest_interval,
)
from src.validators import PARSABLE_DATE, get_input

PRINTER = Printer()


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


def get_duration() -> int:
    return inquirer.number(
        message="Duration in minutes",
        min_allowed=0,
        max_allowed=1440,
        float_allowed=False,
        default=None,
        replace_mode=True,
        validate=EmptyInputValidator(),
    ).execute()


def fast(selected_calendar_id: str):
    duration = get_duration()

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
    start = end - timedelta(minutes=int(duration))
    logger.debug("Start: %s, End: %s", str(start), str(end))

    start_formatted = start.isoformat()
    end_formatted = end.isoformat()

    event_body = {
        "start": {"dateTime": start_formatted, "timeZone": TIMEZONE},
        "end": {"dateTime": end_formatted, "timeZone": TIMEZONE},
        "summary": summary,
        "description": description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(event, int(duration), start, end)


def custom(selected_calendar_id: str):
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

    start_input = get_input(PRINTER, "Start: ", PARSABLE_DATE).strip()
    duration = get_duration()

    start_time = get_time_from_str(start_input)
    end_time = start_time + get_timedelta_from_str(duration)

    start_formatted = start_time.isoformat()
    end_formatted = end_time.isoformat()

    print(start_formatted)
    print(end_formatted)

    event_body = {
        "start": {"dateTime": start_formatted, "timeZone": TIMEZONE},
        "end": {"dateTime": end_formatted, "timeZone": TIMEZONE},
        "summary": summary,
        "description": description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(event, int(duration), start_time, end_time)


if __name__ == "__main__":
    main()
