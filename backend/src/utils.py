import calendar
import csv
import json
import re
import time
from datetime import datetime, timedelta

import babel
import pytz
from dateutil.parser import parse as dateutil_parse
from dateutil.tz import tzlocal
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from parsedatetime.parsedatetime import Calendar
from typeguard import typechecked

from src.auth import get_credentials
from src.constants import TIME_FORMAT_PROMPT
from src.error import ServiceBuildError
from src.logger_config import logger

fuzzy_date_parse = Calendar().parse
fuzzy_datetime_parse = Calendar().parseDT

# Regular expression to parse duration strings like "1d 2h 3m" or "1.5h"
# Based on https://stackoverflow.com/a/51916936/12880
DURATION_REGEX = re.compile(
    r"^((?P<days>[\.\d]+?)(?:d|day|days))?[ :]*"
    r"((?P<hours>[\.\d]+?)(?:h|hour|hours))?[ :]*"
    r"((?P<minutes>[\.\d]+?)(?:m|min|mins|minute|minutes))?[ :]*"
    r"((?P<seconds>[\.\d]+?)(?:s|sec|secs|second|seconds))?$"
)


def write_to_output_file(file_name, data):
    """Writes the data to /output directory, file extension determines the format."""
    path = "src/output/" + file_name

    if file_name.endswith(".json"):
        with open(path, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
        logger.info("Data written to %s", file_name)
    elif file_name.endswith(".csv"):
        with open(path, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        logger.info("Data written to %s", file_name)
    elif file_name.endswith(".txt"):
        with open(path, "w", encoding="utf-8") as file:
            for item in data:
                file.write(f"{item}\n", encoding="utf-8")
        logger.info("Data written to %s", file_name)
    else:
        logger.error("Unsupported file format")


def build_service() -> build:
    """
    Build and return the Google Calendar API service.
    Raises:
        ServiceBuildError: If credentials are missing or the service cannot be built.
    """
    try:
        logger.debug("Building the Google Calendar API service.")
        creds = get_credentials()
        if not creds:
            logger.error("Credentials not found for building the service.")
            raise ServiceBuildError(
                "Missing credentials for building the Calendar API service."
            )

        logger.info("Building the Google Calendar API service.")
        service = build("calendar", "v3", credentials=creds)
        return service
    except HttpError as e:
        logger.error("HTTP Error while building the service: %s", e)
        raise ServiceBuildError(f"Failed to build service due to an HTTP error: {e}")
    except Exception as e:
        logger.error("Unexpected error during service build: %s", e)
        raise ServiceBuildError(f"Unexpected error during service build: {e}")


def round_to_nearest_interval(
    timestamp: datetime, interval_minutes: int = 15
) -> datetime:
    """
    Round the timestamp to the nearest interval, default 15 minutes.
    Handle cases where the hour or day needs to be increased due to rounding.
    For example: 11:58 -> 12:00 or 11:49 -> 11:45 or 23:58 -> 00:00 next day.
    """
    # Extract components from the timestamp
    year = timestamp.year
    month = timestamp.month
    day = timestamp.day
    hour = timestamp.hour
    minute = timestamp.minute

    # Calculate the nearest interval based on the provided interval_minutes
    nearest_interval_minute = round(minute / interval_minutes) * interval_minutes

    # Increase the hour if the nearest interval exceeds 59
    if nearest_interval_minute >= 60:
        nearest_interval_minute = 0  # Reset to 0 if it exceeds 59
        hour += 1  # Increase the hour by 1 if the minute exceeds 59
        if hour >= 24:
            hour = 0  # Reset to 0 if hour exceeds 23
            day += 1  # Increase the day by 1 if the hour exceeds 23
            # Check if day needs to be increased to the next month (e.g. 31st day of the month)
            _, last_day = calendar.monthrange(year, month)
            if day > last_day:
                day = 1
                month += 1
                # Increase the year if the month exceeds 12
                if month > 12:
                    month = 1
                    year += 1

    # Construct a new timestamp with the rounded minute
    rounded_timestamp = timestamp.replace(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=nearest_interval_minute,
        second=0,
        microsecond=0,
    )
    return rounded_timestamp


@typechecked
def print_event_details(event: dict, duration: int, start: datetime, end: datetime):
    """Prints the created event details to the console."""
    if not all(key in event for key in ("summary", "description")):
        raise ValueError("Event details are missing required fields.")

    if duration < 0:
        raise ValueError("Duration cannot be negative.")

    try:
        print("\nEvent created successfully:")
        print("{:<12}{:<}".format("Summary:", event["summary"]))
        print("{:<12}{:<}".format("Desc:", event["description"]))
        print("{:<12}{:<}".format("Duration:", str(duration) + " minutes"))
        print("{:<12}{:<}".format("Start:", start.strftime("%Y-%m-%d %H:%M:%S")))
        print("{:<12}{:<}".format("End:", end.strftime("%Y-%m-%d %H:%M:%S")))
        print(event.get("htmlLink"))
    except Exception as e:
        print("Failed to print event details.", str(e))


def format_event_time_from_iso(event_time):
    """Formats the event time from ISO format to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")


def format_str_datetime_to_iso(dt_str: str, timezone: str):
    """Formats the datetime string to ISO format."""
    local_timezone = pytz.timezone(timezone)
    dt = datetime.strptime(dt_str, TIME_FORMAT_PROMPT)
    dt = local_timezone.localize(dt)
    return dt.isoformat()


def _is_dayfirst_locale():
    """Detect whether system locale date format has day first.

    Examples:
     - M/d/yy -> False
     - dd/MM/yy -> True
     - (UnknownLocaleError) -> False

    Pattern syntax is documented at
    https://babel.pocoo.org/en/latest/dates.html#pattern-syntax.
    """
    try:
        locale = babel.Locale(babel.default_locale("LC_TIME"))
    except babel.UnknownLocaleError:
        # Couldn't detect locale, assume non-dayfirst.
        return False
    m = re.search(r"M|d|$", locale.date_formats["short"].pattern)
    return m and m.group(0) == "d"


def get_time_from_str(when):
    """Convert a string to a time: first uses the dateutil parser, falls back
    on fuzzy matching with parsedatetime
    """
    zero_oclock_today = datetime.now(tzlocal()).replace(
        hour=0, minute=0, second=0, microsecond=0
    )

    # Only apply dayfirst=True if date actually starts with "XX-XX-".
    # Other forms like YYYY-MM-DD shouldn't rely on locale by default (#792).
    # dayfirst = _is_dayfirst_locale() if re.match(r"^\d{1,2}-\d{1,2}-", when) else None
    dayfirst = (
        True if re.match(r"^\d{1,2}[-.]\d{1,2}[-.]", when) else _is_dayfirst_locale()
    )
    try:
        event_time = dateutil_parse(when, default=zero_oclock_today, dayfirst=dayfirst)
    except ValueError:
        struct, result = fuzzy_date_parse(when)
        if not result:
            raise ValueError("Date and time is invalid: %s" % (when))
        event_time = datetime.fromtimestamp(time.mktime(struct), tzlocal())

    return event_time


def get_timedelta_from_str(delta):
    """
    Parse a time string into a timedelta object.
    Formats:
      - number -> duration in minutes
      - "1:10" -> hour and minutes
      - "1d 1h 1m" -> days, hours, minutes
    Based on https://stackoverflow.com/a/51916936/12880
    """
    parsed_delta = None
    try:
        parsed_delta = timedelta(minutes=float(delta))
    except ValueError:
        pass
    if parsed_delta is None:
        parts = DURATION_REGEX.match(delta)
        if parts is not None:
            try:
                time_params = {
                    name: float(param)
                    for name, param in parts.groupdict().items()
                    if param
                }
                parsed_delta = timedelta(**time_params)
            except ValueError:
                pass
    if parsed_delta is None:
        dt, result = fuzzy_datetime_parse(delta, sourceTime=datetime.min)
        if result:
            parsed_delta = dt - datetime.min
    if parsed_delta is None:
        raise ValueError("Duration is invalid: %s" % (delta))
    return parsed_delta
