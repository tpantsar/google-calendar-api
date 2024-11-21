import csv
import json
from datetime import datetime

from flask import Response, request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from auth import get_credentials
from constants import ERROR_PROFILE, MASON
from logger_config import logger
from mason import MasonBuilder


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


def create_error_response(status_code, title, message=None) -> Response:
    """
    Create an error response with the given status code and title.

    Parameters:
    - status_code: The HTTP status code.
    - title: The title of the error.
    - message: An optional message describing the error.

    Returns:
    - A Response object with the error message.
    """
    resource_url = request.path
    body = MasonBuilder(resource_url=resource_url)
    body.add_error(title, message)
    body.add_control("profile", href=ERROR_PROFILE)
    return Response(json.dumps(body), status_code, mimetype=MASON)


def build_service() -> build:
    """
    Build the Calendar API service and return it.
    creds is the credentials object used for building the service.
    """
    try:
        creds = get_credentials()
        if creds is None:
            logger.error("Failed to get the credentials")
            return None

        service = build("calendar", "v3", credentials=creds)
        if service is None:
            logger.error("Failed to build the Calendar API service")
            return None

        return service
    except HttpError as error:
        logger.error(f"An error occurred with building the service: {error}")
        return None


def format_event_time(event_time):
    """Formats the event time to 'pe 4.10.2024 18:00'."""
    date = datetime.fromisoformat(event_time)
    return date.strftime("%a %d.%m.%Y %H:%M")
