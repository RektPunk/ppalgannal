from datetime import date, datetime, timedelta
from functools import lru_cache

from ppalgannal.holidays.constant import (
    KST,
    LUNAR_HOLIDAYS,
    SOLAR_HOLIDAYS,
    SPECIAL_HOLIDAYS,
    Holiday,
    SubstituteRule,
)
from ppalgannal.holidays.substitute import add_substitute_holidays
from ppalgannal.lunar import lunar_to_solar


def _add_holiday(
    holidays: dict[date, Holiday],
    holiday: Holiday,
) -> None:
    holidays.setdefault(holiday.date, holiday)


def _build_holidays(
    year: int,
) -> tuple[
    dict[date, Holiday],
    dict[date, SubstituteRule],
    list[tuple[date, ...]],
    set[date],
]:
    holidays: dict[date, Holiday] = {}
    rules: dict[date, SubstituteRule] = {}
    three_day_groups: list[tuple[date, ...]] = []
    overlapping_dates: set[date] = set()

    for definition in SOLAR_HOLIDAYS:
        holiday_date = date(year, definition.month, definition.day)
        _add_holiday(holidays, Holiday(date=holiday_date, name=definition.name))
        rules[holiday_date] = definition.substitute

    for definition in LUNAR_HOLIDAYS:
        center = lunar_to_solar(year, definition.month, definition.day)
        if definition.three_day:
            dates = (center - timedelta(days=1), center, center + timedelta(days=1))
            three_day_groups.append(dates)
            names = (
                f"{definition.name} 전날",
                definition.name,
                f"{definition.name} 다음날",
            )
            overlapping_dates.update(day for day in dates if day in holidays)
        else:
            dates = (center,)
            names = (definition.name,)

        for holiday_date, name in zip(dates, names, strict=True):
            _add_holiday(holidays, Holiday(date=holiday_date, name=name))
            rules[holiday_date] = definition.substitute

    for definition in SPECIAL_HOLIDAYS.get(year, ()):
        holiday_date = date(year, definition.month, definition.day)
        _add_holiday(
            holidays,
            Holiday(date=holiday_date, name=definition.name, is_substitute=False),
        )
        rules[holiday_date] = definition.substitute

    return holidays, rules, three_day_groups, overlapping_dates


@lru_cache(maxsize=16)
def _get_holidays(year: int) -> tuple[Holiday, ...]:
    holidays, rules, three_day_groups, overlapping_dates = _build_holidays(year)
    add_substitute_holidays(holidays, rules, three_day_groups, overlapping_dates)

    return tuple(
        sorted(
            holidays.values(),
            key=lambda holiday: holiday.date,
        ),
    )


@lru_cache(maxsize=16)
def _get_holiday_dates(year: int) -> frozenset[date]:
    return frozenset(holiday.date for holiday in _get_holidays(year))


def get_holidays(year: int) -> list[Holiday]:
    """Return named public holidays for the given year."""
    return list(_get_holidays(year))


def is_holiday(value: date | str) -> bool:
    """Return whether value is a named public or substitute holiday."""
    if isinstance(value, str):
        value = date.fromisoformat(value)

    return value in _get_holiday_dates(value.year)


def is_holiday_today() -> bool:
    """Return whether today is a named public or substitute holiday in Korea."""
    return is_holiday(datetime.now(KST).date())
