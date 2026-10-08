from datetime import date

from ppalgannal.lunar.constant import (
    LUNAR_BIG_MONTH_DAYS,
    LUNAR_DATA,
    LUNAR_MAX_YEAR,
    LUNAR_MIN_YEAR,
    LUNAR_SMALL_MONTH_DAYS,
    SOLAR_LUNAR_DAY_DIFF,
)


def _lunar_data(year: int) -> int:
    return LUNAR_DATA[year - LUNAR_MIN_YEAR]


def _leap_month(lunar_data: int) -> int:
    return (lunar_data >> 12) & 0x0F


def _lunar_month_days(year: int, month: int) -> int:
    lunar_data = _lunar_data(year)
    return (
        LUNAR_BIG_MONTH_DAYS
        if (lunar_data >> (12 - month)) & 1
        else LUNAR_SMALL_MONTH_DAYS
    )


def _lunar_year_days(year: int) -> int:
    return (_lunar_data(year) >> 17) & 0x01FF


def _lunar_days_before_year(year: int) -> int:
    return sum(_lunar_year_days(y) for y in range(LUNAR_MIN_YEAR, year + 1))


def _lunar_days_before_month(year: int, month: int) -> int:
    days = sum(_lunar_month_days(year, m) for m in range(1, month + 1))
    leap_month = _leap_month(_lunar_data(year))
    if leap_month and leap_month < month + 1:
        days += (
            LUNAR_BIG_MONTH_DAYS
            if (_lunar_data(year) >> 16) & 1
            else LUNAR_SMALL_MONTH_DAYS
        )
    return days


def _lunar_abs_days(year: int, month: int, day: int) -> int:
    return (
        _lunar_days_before_year(year - 1)
        + _lunar_days_before_month(year, month - 1)
        + day
    )


def _is_solar_leap_year(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _solar_month_days(year: int, month: int) -> int:
    if month == 2 and _is_solar_leap_year(year):
        return 29
    return (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)[month - 1]


def _solar_year_days(year: int) -> int:
    return 366 if _is_solar_leap_year(year) else 365


def _solar_days_before_year(year: int) -> int:
    return sum(_solar_year_days(y) for y in range(LUNAR_MIN_YEAR, year + 1))


def _solar_days_before_month(year: int, month: int) -> int:
    return sum(_solar_month_days(year, m) for m in range(1, month + 1))


def _solar_abs_days(year: int, month: int, day: int) -> int:
    return (
        _solar_days_before_year(year - 1)
        + _solar_days_before_month(year, month - 1)
        + day
        - SOLAR_LUNAR_DAY_DIFF
    )


def lunar_to_solar(year: int, month: int, day: int) -> date:
    """Convert a regular Korean lunar date to a Gregorian date."""
    if not all(
        isinstance(value, int) and not isinstance(value, bool)
        for value in (year, month, day)
    ):
        raise TypeError("year, month, and day must be integers")

    if not LUNAR_MIN_YEAR <= year <= LUNAR_MAX_YEAR:
        raise ValueError(
            f"lunar year must be between {LUNAR_MIN_YEAR} and {LUNAR_MAX_YEAR}",
        )

    if not 1 <= month <= 12:
        raise ValueError("lunar month must be between 1 and 12")

    if not 1 <= day <= _lunar_month_days(year, month):
        raise ValueError("invalid lunar day")

    abs_days = _lunar_abs_days(year, month, day)
    solar_year = year if abs_days < _solar_abs_days(year + 1, 1, 1) else year + 1

    for solar_month in range(12, 0, -1):
        abs_days_by_month = _solar_abs_days(solar_year, solar_month, 1)
        if abs_days >= abs_days_by_month:
            solar_day = abs_days - abs_days_by_month + 1
            return date(solar_year, solar_month, solar_day)

    raise ValueError("failed to convert lunar date")
