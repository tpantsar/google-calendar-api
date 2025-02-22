from datetime import datetime

from gcalcli.exceptions import ValidationError
from InquirerPy.validator import Validator

from .constants import TIME_FORMAT_PROMPT


class DateTimeValidator(Validator):
    """Legacy validator for datetime input."""

    def __init__(
        self, message: str = 'Invalid date format. Use YYYY-MM-DD HH:MM'
    ) -> None:
        self._message = message

    def validate(self, document) -> None:
        try:
            datetime.strptime(document.text, TIME_FORMAT_PROMPT)
        except ValueError:
            raise ValidationError(message=self._message)
