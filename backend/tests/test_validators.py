import re
from datetime import datetime
from unittest.mock import patch

from src.printer import Printer
from src.utils import get_time_from_str, get_timedelta_from_str
from src.validators import PARSABLE_DATE, get_input

PRINTER = Printer()

# ISO 8601 format regex pattern
iso8601_pattern = (
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:\.\d+)?(?:Z|[+-]\d{2}:\d{2})?$"
)


@patch("builtins.input", lambda: "15:00")
def test_get_input():
    start_input = get_input(PRINTER, "When: ", PARSABLE_DATE).strip()
    start_time = get_time_from_str(start_input)
    end_time = start_time + get_timedelta_from_str(60)  # 60 minutes

    assert end_time > start_time, "End time must be after start time."

    now = datetime.now()

    assert start_time.date() == now.date(), "Start time must be today."
    assert start_input == "15:00", "Input should be '15:00'."

    start_formatted = start_time.isoformat()
    end_formatted = end_time.isoformat()

    assert re.match(
        iso8601_pattern, start_formatted
    ), "start_formatted does not follow ISO 8601 format."

    assert re.match(
        iso8601_pattern, end_formatted
    ), "end_formatted does not follow ISO 8601 format."
