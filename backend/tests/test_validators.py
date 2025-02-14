import re
from datetime import datetime
from unittest.mock import MagicMock, patch

import pytest
from gcalcli.utils import get_time_from_str

from src.exceptions import ValidationError
from src.printer import Printer
from src.utils import get_timedelta_from_str
from src.validators import PARSABLE_DATE, DateTimeValidator, get_input

PRINTER = Printer()

# ISO 8601 format regex pattern
iso8601_pattern = r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$'


@patch('builtins.input', lambda: '15:00')
def test_get_input():
    start_input = get_input(PRINTER, 'When: ', PARSABLE_DATE).strip()
    start_time = get_time_from_str(start_input)
    end_time = start_time + get_timedelta_from_str(60)  # 60 minutes

    assert end_time > start_time, 'End time must be after start time.'

    now = datetime.now()

    assert start_time.date() == now.date(), 'Start time must be today.'
    assert start_input == '15:00', "Input should be '15:00'."

    start_formatted = start_time.isoformat()
    end_formatted = end_time.isoformat()

    assert re.match(iso8601_pattern, start_formatted), (
        'start_formatted does not follow ISO 8601 format.'
    )

    assert re.match(iso8601_pattern, end_formatted), (
        'end_formatted does not follow ISO 8601 format.'
    )


# Parametrized test for DateTimeValidator
@pytest.mark.parametrize(
    'datetime_str',
    [
        ('2023-10-10 10:10'),
        ('2023-12-31 23:59'),
        ('2023-01-01 00:00'),
        ('2023-1-1 9:00'),
        ('2023-01-1 9:00'),
        ('2023-1-01 9:00'),
        ('2023-1-1 9:0'),
    ],
)
def test_datetime_validator_valid(datetime_str):
    validator = DateTimeValidator()
    document = MagicMock()
    document.text = datetime_str
    try:
        validator.validate(document)
    except ValidationError:
        pytest.fail('ValidationError raised unexpectedly!')
