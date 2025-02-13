import logging
from datetime import datetime, timedelta

import pytest
import pytz
from typeguard import TypeCheckError

from src.utils import (
    format_event_time_from_iso,
    fuzzy_datetime_parse,
    get_duration_str,
    get_time_from_str,
    get_timedelta_from_str,
    print_event_details,
)

logger = logging.getLogger(__name__)


def test_print_event_details_success():
    event = {
        'summary': 'Test Event',
        'description': 'This is a test event',
        'htmlLink': 'http://example.com',
    }
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 19, 0)

    try:
        print_event_details(event, end - start, start, end)
    except Exception:
        pytest.fail('print_event_details raised an exception unexpectedly!')


def test_print_event_details_get_time_from_str_success():
    event = {
        'summary': 'Test Event',
        'description': 'This is a test event',
        'htmlLink': 'http://example.com',
    }
    start = get_time_from_str('2024-10-04 18:00')  # "2024-10-04 18:00"
    end = start + get_timedelta_from_str(60)  # "2024-10-04 19:00"
    assert end > start, 'End time must be after start time.'

    duration = end - start
    assert duration == timedelta(minutes=60), 'Duration must be 60 minutes.'

    try:
        print_event_details(event, duration, start, end)
    except Exception:
        pytest.fail('print_event_details raised an exception unexpectedly!')


def test_print_event_details_partial_data_success():
    event = {'summary': 'Test Event', 'description': 'This is a test event'}
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 19, 0)

    try:
        print_event_details(event, end - start, start, end)
    except Exception:
        pytest.fail('print_event_details raised an exception unexpectedly!')


def test_print_event_details_missing_event_data():
    event = {'summary': 'Test Event'}
    start = datetime(2024, 10, 4, 18, 0)
    end = datetime(2024, 10, 4, 19, 0)

    with pytest.raises(ValueError):
        print_event_details(event, end - start, start, end)


def test_print_event_details_valid_datetime():
    test_event = {
        'summary': 'Test Event',
        'description': 'Test Description',
        'htmlLink': 'http://example.com',
    }

    try:
        start = datetime(2025, 1, 8, 11, 15, 0)
        end = datetime(2025, 1, 8, 12, 15, 0)
        duration = end - start
        print_event_details(event=test_event, duration=duration, start=start, end=end)
    except Exception:
        pytest.fail('print_event_details raised an exception unexpectedly!')


def test_print_event_details_invalid_datetime1():
    test_event = {
        'summary': 'Test Event',
        'description': 'Test Description',
        'htmlLink': 'http://example.com',
    }

    with pytest.raises(TypeCheckError):
        print_event_details(
            test_event, 1.5, '2025-01-08 11:15:00+02:00', '2025-01-08 12:15:00+02:00'
        )


def test_print_event_details_invalid_datetime2():
    test_event = {
        'summary': 'Test Event',
        'description': 'Test Description',
        'htmlLink': 'http://example.com',
    }

    with pytest.raises(TypeCheckError):
        print_event_details(test_event, 1.5, '2023-10-10 10:15', '2023-10-10 11:15')


def test_get_time_from_str_non_dayfirst_locale():
    TIMEZONE = 'Europe/Helsinki'
    when = '2025-01-26 11:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    # Localize the expected datetime to the specified timezone
    expected = local_timezone.localize(datetime(2025, 1, 26, 11, 0))
    result = get_time_from_str(when).astimezone(local_timezone)
    logger.info(result)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_valid_fuzzy_parse1():
    when = 'next Friday at 6pm'
    current_year = datetime.now().year

    result = get_time_from_str(when)
    logger.info(result)
    assert result.year == current_year, f'Expected {current_year}, but got {result.year}'
    assert result.weekday() == 4, f'Expected Friday, but got {result.strftime("%A")}'
    assert result.hour == 18, f'Expected 18:00, but got {result.strftime("%H:%M")}'


def test_get_time_from_str_valid_fuzzy_parse2():
    when = 'Today at 3pm'

    current_year = datetime.now().year

    result = get_time_from_str(when)
    logger.info(result)
    assert result.year == current_year, f'Expected {current_year}, but got {result.year}'
    assert result.weekday() == datetime.now().weekday(), (
        f'Expected today, but got {result.strftime("%A")}'
    )
    assert result.hour == 15, f'Expected 15:00, but got {result.strftime("%H:%M")}'


def test_get_time_from_str_invalid_date():
    when = 'invalid date string'
    with pytest.raises(ValueError, match='Date and time is invalid'):
        get_time_from_str(when)


def test_get_time_from_str_invalid_date2():
    when = ''
    with pytest.raises(ValueError, match='Date and time is invalid'):
        get_time_from_str(when)


def test_get_time_from_str_dayfirst_locale1():
    TIMEZONE = 'Europe/Helsinki'
    when = '04-10-2024 18:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 10, 4, 18, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_dayfirst_locale_leading_zeroes():
    TIMEZONE = 'Europe/Helsinki'
    when = '04.09.2024 18:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 9, 4, 18, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_time_from_str_dayfirst_locale_non_leading_zeroes():
    TIMEZONE = 'Europe/Helsinki'
    when = '4.5.2024 9:00'

    # Convert UTC datetime to local datetime
    local_timezone = pytz.timezone(TIMEZONE)

    expected = local_timezone.localize(datetime(2024, 5, 4, 9, 0))
    result = get_time_from_str(when).astimezone(local_timezone)

    assert result == expected, f'Expected {expected}, but got {result}'


def test_format_event_time_from_iso_valid_date():
    event_time = '2024-10-04T18:00:00Z'
    expected = 'Fri 04.10.2024 18:00'
    result = format_event_time_from_iso(event_time)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_format_event_time_from_iso_invalid_date():
    event_time = 'invalid-date'
    with pytest.raises(ValueError):
        format_event_time_from_iso(event_time)


def test_format_event_time_from_iso_edge_case():
    event_time = '2024-02-29T23:59:59'  # Leap year date
    expected = 'Thu 29.02.2024 23:59'
    result = format_event_time_from_iso(event_time)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_format_event_time_from_iso_different_time():
    event_time = '2024-10-04T09:30:00'
    expected = 'Fri 04.10.2024 09:30'
    result = format_event_time_from_iso(event_time)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_minutes():
    delta = '90'
    expected = timedelta(minutes=90)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_hours_minutes():
    delta = '1:30'
    expected = timedelta(hours=1, minutes=30)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_days_hours_minutes():
    delta = '1d 2h 30m'
    expected = timedelta(days=1, hours=2, minutes=30)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_hours():
    delta = '2h'
    expected = timedelta(hours=2)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_days():
    delta = '3d'
    expected = timedelta(days=3)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_timedelta_from_str_invalid_format():
    delta = 'invalid'
    with pytest.raises(ValueError, match='Duration is invalid'):
        get_timedelta_from_str(delta)


def test_get_timedelta_from_str_fuzzy_parse():
    delta = 'next Friday at 6pm'
    result = get_timedelta_from_str(delta)
    logger.info(result)
    expected = fuzzy_datetime_parse(delta, sourceTime=datetime.min)[0] - datetime.min
    assert result == expected, f'Expected {expected}, but got {result}'
    assert result.days >= 0, 'Expected a positive timedelta'


def test_get_timedelta_from_str_edge_case():
    delta = '0.5h'
    expected = timedelta(minutes=30)
    result = get_timedelta_from_str(delta)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_minutes():
    duration = '90'
    expected = '1 h 30 min'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_hours():
    duration = '120'
    expected = '2 h'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_hours_minutes():
    duration = '150'
    expected = '2 h 30 min'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_days_hours_minutes():
    duration = '1d 2h 30m'
    expected = '26 h 30 min'  # 1 day = 24 hours + 2 hours = 26 hours
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_invalid_format():
    duration = 'invalid'
    with pytest.raises(ValueError, match='Duration is invalid'):
        get_duration_str(duration)


def test_get_duration_str_edge_case():
    duration = '0.5h'
    expected = '30 min'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'


def test_get_duration_str_none_zero():
    duration = None
    expected = '0 min'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'

    duration = 0
    expected = '0 min'
    result = get_duration_str(duration)
    logger.info(result)
    assert result == expected, f'Expected {expected}, but got {result}'
