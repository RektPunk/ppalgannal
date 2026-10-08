from datetime import date, timedelta

from ppalgannal.holidays.constant import Holiday, SubstituteRule


def _is_substitute_triggered(
    holiday_date: date,
    rule: SubstituteRule,
) -> bool:
    if rule == SubstituteRule.WEEKEND:
        return holiday_date.weekday() >= 5

    if rule == SubstituteRule.SUNDAY:
        return holiday_date.weekday() == 6

    return False


def _next_non_holiday(start: date, holidays: set[date]) -> date:
    candidate = start + timedelta(days=1)
    while candidate.weekday() in (5, 6) or candidate in holidays:
        candidate += timedelta(days=1)

    return candidate


def add_substitute_holidays(
    holidays: dict[date, Holiday],
    rules: dict[date, SubstituteRule],
    three_day_groups: list[tuple[date, ...]],
    overlapping_dates: set[date],
) -> None:
    holiday_dates = set(holidays)

    for group in three_day_groups:
        overlaps_sunday = any(day.weekday() == 6 for day in group)
        overlaps_holiday = any(day in overlapping_dates for day in group)

        if not (overlaps_sunday or overlaps_holiday):
            continue

        substitute_date = _next_non_holiday(group[-1], holiday_dates)
        holidays[substitute_date] = Holiday(
            date=substitute_date,
            name=f"{holidays[group[1]].name} 대체공휴일",
            is_substitute=True,
        )
        holiday_dates.add(substitute_date)

    for holiday_date, rule in rules.items():
        if any(holiday_date in group for group in three_day_groups):
            continue

        if not _is_substitute_triggered(holiday_date, rule):
            continue

        substitute_date = _next_non_holiday(holiday_date, holiday_dates)
        holidays[substitute_date] = Holiday(
            date=substitute_date,
            name=f"{holidays[holiday_date].name} 대체공휴일",
            is_substitute=True,
        )
        holiday_dates.add(substitute_date)
