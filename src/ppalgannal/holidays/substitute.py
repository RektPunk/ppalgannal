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
) -> None:
    for group in three_day_groups:
        if not any(day.weekday() == 6 for day in group):
            continue

        substitute_date = _next_non_holiday(group[-1], set(holidays.keys()))
        holidays[substitute_date] = Holiday(
            substitute_date,
            f"{holidays[group[1]].name} 대체공휴일",
            True,
        )

    for holiday_date, rule in rules.items():
        if any(holiday_date in group for group in three_day_groups):
            continue

        if not _is_substitute_triggered(holiday_date, rule):
            continue

        substitute_date = _next_non_holiday(holiday_date, set(holidays.keys()))
        holidays[substitute_date] = Holiday(
            substitute_date,
            f"{holidays[holiday_date].name} 대체공휴일",
            True,
        )
