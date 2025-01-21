from datetime import datetime, timezone

import pytz

from src.constants import TIMEZONE
from src.printer import Printer
from src.utils import (
    get_time_from_str,
    get_timedelta_from_str,
)
from src.validators import PARSABLE_DATE, get_input

PRINTER = Printer()

duration = 60  # minutes

# Convert UTC datetime to local datetime
local_timezone = pytz.timezone(TIMEZONE)
current_utc_time = datetime.now(timezone.utc)
current_local_time = current_utc_time.astimezone(local_timezone)

# start_default = round_to_nearest_interval(current_local_time, 15)
start_input = get_input(PRINTER, "When: ", PARSABLE_DATE).strip()

start_time = get_time_from_str(start_input)
end_time = start_time + get_timedelta_from_str(duration)

assert end_time > start_time, "End time must be after start time."

print(f"Start: {start_time}")
print(f"End: {end_time}")
