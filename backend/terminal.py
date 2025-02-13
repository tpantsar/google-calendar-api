from datetime import datetime, timezone

import pytz
from gcalcli.utils import get_time_from_str
from InquirerPy import inquirer
from InquirerPy.validator import EmptyInputValidator

from src.constants import TIMEZONE
from src.logger_config import logger
from src.printer import Printer
from src.services.calendar import get_calendar_list
from src.services.event import create_event, get_recent_unique_events
from src.utils import (
    get_timedelta_from_str,
    print_event_details,
    round_to_nearest_interval,
)
from src.validators import PARSABLE_DATE, PARSABLE_DURATION, get_input

PRINTER = Printer()


def main():
    # Fetch calendar list
    calendars = get_calendar_list()
    calendar_choices = [
        {'name': calendar['summary'], 'value': calendar['id']} for calendar in calendars
    ]

    menu_choices = ['Fast', 'Custom']
    menu = inquirer.select(
        message='Method:',
        choices=menu_choices,
        default='Fast',  # Optional: Set a default choice
        validate=EmptyInputValidator(),
    )

    # Display calendar menu with filtering enabled
    selected_calendar_id = inquirer.fuzzy(
        message='Select calendar:',
        choices=calendar_choices,
        default=None,  # Optional: Set a default choice
        validate=EmptyInputValidator(),
    ).execute()

    print(f'Using calendar: {selected_calendar_id}')

    if menu.execute() == 'Fast':
        fast(selected_calendar_id)
    else:
        custom(selected_calendar_id)


def get_duration_legacy() -> int:
    return inquirer.number(
        message='Duration in minutes',
        min_allowed=0,
        max_allowed=1440,
        float_allowed=False,
        default=None,
        replace_mode=True,
        validate=EmptyInputValidator(),
    ).execute()


def get_duration():
    return get_input(PRINTER, 'Duration (human readable): ', PARSABLE_DURATION)


def fast(selected_calendar_id: str):
    duration = get_duration()

    events = get_recent_unique_events(selected_calendar_id)
    for event in events:
        print(event)
    popular_events_summaries = {event: None for event in events}

    # Event summary with auto-complete from popular events
    # https://inquirerpy.readthedocs.io/en/latest/pages/prompts/input.html#auto-completion
    summary = inquirer.text(
        message='Summary',
        completer=popular_events_summaries,
        validate=EmptyInputValidator(),
    ).execute()

    # Event description
    description = inquirer.text(
        message='Description',
        validate=EmptyInputValidator(),
    ).execute()

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)
    current_utc_time = datetime.now(timezone.utc)
    current_local_time = current_utc_time.astimezone(local_timezone)

    end = round_to_nearest_interval(current_local_time, 15)
    start = end - get_timedelta_from_str(duration)
    logger.debug('Start: %s, End: %s', str(start), str(end))

    start_formatted = start.isoformat()
    end_formatted = end.isoformat()

    event_body = {
        'start': {'dateTime': start_formatted, 'timeZone': TIMEZONE},
        'end': {'dateTime': end_formatted, 'timeZone': TIMEZONE},
        'summary': summary,
        'description': description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(event, duration, start, end)


def custom(selected_calendar_id: str):
    events = get_recent_unique_events(selected_calendar_id)
    for event in events:
        print(event)
    popular_events_summaries = {event: None for event in events}

    # Event summary with auto-complete from popular events
    # https://inquirerpy.readthedocs.io/en/latest/pages/prompts/input.html#auto-completion
    summary = inquirer.text(
        message='Summary',
        completer=popular_events_summaries,
        validate=EmptyInputValidator(),
    ).execute()

    # Event description
    description = inquirer.text(
        message='Description',
        validate=EmptyInputValidator(),
    ).execute()

    start_input = get_input(PRINTER, 'When: ', PARSABLE_DATE).strip()
    duration = get_duration()

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)
    start_time = get_time_from_str(start_input).astimezone(local_timezone)
    end_time = start_time + get_timedelta_from_str(duration)

    start_formatted = start_time.isoformat()
    end_formatted = end_time.isoformat()

    print(start_formatted)
    print(end_formatted)

    event_body = {
        'start': {'dateTime': start_formatted, 'timeZone': TIMEZONE},
        'end': {'dateTime': end_formatted, 'timeZone': TIMEZONE},
        'summary': summary,
        'description': description,
    }

    event = create_event(selected_calendar_id, event_body)
    print_event_details(event, duration, start_time, end_time)


if __name__ == '__main__':
    main()
