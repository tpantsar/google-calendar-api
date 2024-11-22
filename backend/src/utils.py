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


def handle_service_build(build_function):
    """Handles service building logic."""
    try:
        return build_function()
    except ServiceBuildError as e:
        logger.error(f"Service Build Error: {str(e)}")
        raise ServiceBuildError("Failed to build the service")
    except Exception as e:
        logger.error(f"Unhandled Service Error: {str(e)}")
        raise ServiceBuildError("An unexpected error occurred")


def build_service() -> build:
    """
    Build the Calendar API service and return it.
    creds is the credentials object used for building the service.
    Raises:
        ServiceBuildError: If an error occurs while building the service.
    """
    try:
        creds = get_credentials()
        if creds is None:
            raise ServiceBuildError("Failed to get the credentials")

        service = build("calendar", "v3", credentials=creds)
        if service is None:
            raise ServiceBuildError("Failed to build the Calendar API service.")

        return service
    except HttpError as error:
        raise ServiceBuildError(
            f"An HTTP error occurred while building the service: {error}"
        )
    except Exception as error:
        raise ServiceBuildError(f"An unexpected error occurred: {error}")


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
