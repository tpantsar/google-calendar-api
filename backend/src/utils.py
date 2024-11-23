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


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
