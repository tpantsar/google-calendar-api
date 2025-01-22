from typing import Optional

from .exceptions import ValidationError
from .utils import get_time_from_str

DATE_INPUT_DESCRIPTION = "\
a date (e.g. 2019-12-31, tomorrow 10am, 2nd Jan, Jan 4th, etc) or valid time \
if today"


def get_input(printer, prompt, validator_func, help: Optional[str] = None):
    printer.msg(prompt, "magenta")
    while True:
        try:
            answer = input()
            if answer.strip() == "?" and help:
                printer.msg(f"{help}\n")
                printer.msg(prompt, "magenta")
                continue
            output = validator_func(answer)
            return output
        except ValidationError as e:
            printer.msg(e.message, "red")
            printer.msg(prompt, "magenta")


def parsable_date_validator(input_str):
    """
    A filter allowing any string which can be parsed
    by dateutil.
    Raises ValidationError otherwise.
    """
    try:
        get_time_from_str(input_str)
        return input_str
    except ValueError:
        raise ValidationError(
            f"Expected format: {DATE_INPUT_DESCRIPTION}. " "(Ctrl-C to exit)\n"
        )


PARSABLE_DATE = parsable_date_validator
