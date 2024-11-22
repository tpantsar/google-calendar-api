import json

from flask import Response, request

from constants import ERROR_PROFILE, MASON
from logger_config import logger
from mason import MasonBuilder


class ServiceBuildError(Exception):
    """Custom exception for service build errors."""



class CalendarServiceError(Exception):
    """Custom exception for CalendarService errors."""



class ParameterError(Exception):
    """Custom exception for parameter errors."""

    def __init__(self, message):
        self.message = message
        logger.error(message)
        super().__init__(self.message)

    def to_response(self):
        resource_url = request.path
        body = MasonBuilder(resource_url=resource_url)
        body.add_error("Bad Request", self.message)
        body.add_control("profile", href=ERROR_PROFILE)
        return Response(json.dumps(body), status=400, mimetype=MASON)


class APIError(Exception):
    """Custom exception for API errors."""

    def __init__(self, status_code, title, message=None):
        self.status_code = status_code
        self.title = title
        self.message = message
        super().__init__(self.message)

    def to_response(self):
        resource_url = request.path
        body = MasonBuilder(resource_url=resource_url)
        body.add_error(self.title, self.message)
        body.add_control("profile", href=ERROR_PROFILE)
        return Response(json.dumps(body), status=self.status_code, mimetype=MASON)


def raise_api_error(status_code, title, message=None) -> APIError:
    """
    Create an error response with the given status code and title.

    Parameters:
    - status_code: The HTTP status code.
    - title: The title of the error.
    - message: An optional message describing the error.

    Returns:
    - Raises an APIError exception with the error details.
    """
    raise APIError(status_code, title, message)


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
