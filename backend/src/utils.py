import calendar
import csv
import json
from datetime import datetime

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from error import ServiceBuildError
from logger_config import logger


def write_to_file(file_name, data):
    """Writes the data to a file depending on the file format."""
    if file_name.endswith(".json"):
        with open(file_name, "w", encoding="utf-8") as file:
            file.write(json.dumps(data, indent=2, ensure_ascii=False))
        logger.info(f"Data written to {file_name}")
    elif file_name.endswith(".csv"):
        with open(file_name, "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            for row in data:
                writer.writerow(row)
        logger.info(f"Data written to {file_name}")
    elif file_name.endswith(".txt"):
        with open(file_name, "w", encoding="utf-8") as file:
            for item in data:
                file.write(f"{item}\n", encoding="utf-8")
        logger.info(f"Data written to {file_name}")
    else:
        logger.error("Unsupported file format")


def build_service() -> build:
    """
    Build and return the Google Calendar API service.
    Raises:
        ServiceBuildError: If credentials are missing or the service cannot be built.
    """
    try:
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
        logger.error(f"HTTP Error while building the service: {e}")
        raise ServiceBuildError(f"Failed to build service due to an HTTP error: {e}")
    except Exception as e:
        logger.error(f"Unexpected error during service build: {e}")
        raise ServiceBuildError(
            f"An unexpected error occurred while building the service: {e}"
        )


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


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
