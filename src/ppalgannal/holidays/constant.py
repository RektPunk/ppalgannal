from datetime import date, timedelta, timezone
from enum import StrEnum
from typing import NamedTuple

KST = timezone(timedelta(hours=9))


class SubstituteRule(StrEnum):
    NONE = "none"
    WEEKEND = "weekend"
    SUNDAY = "sunday"


class SolarHoliday(NamedTuple):
    month: int
    day: int
    name: str
    substitute: SubstituteRule = SubstituteRule.NONE


class LunarHoliday(NamedTuple):
    month: int
    day: int
    name: str
    three_day: bool = False
    substitute: SubstituteRule = SubstituteRule.NONE


class Holiday(NamedTuple):
    date: date
    name: str
    is_substitute: bool = False


SOLAR_HOLIDAYS = (
    SolarHoliday(1, 1, "신정"),
    SolarHoliday(3, 1, "삼일절", SubstituteRule.WEEKEND),
    SolarHoliday(5, 1, "노동절", SubstituteRule.WEEKEND),
    SolarHoliday(5, 5, "어린이날", SubstituteRule.WEEKEND),
    SolarHoliday(6, 6, "현충일"),
    SolarHoliday(7, 17, "제헌절", SubstituteRule.WEEKEND),
    SolarHoliday(8, 15, "광복절", SubstituteRule.WEEKEND),
    SolarHoliday(10, 3, "개천절", SubstituteRule.WEEKEND),
    SolarHoliday(10, 9, "한글날", SubstituteRule.WEEKEND),
    SolarHoliday(12, 25, "기독탄신일", SubstituteRule.WEEKEND),
)

LUNAR_HOLIDAYS = (
    LunarHoliday(1, 1, "설날", three_day=True, substitute=SubstituteRule.SUNDAY),
    LunarHoliday(4, 8, "부처님오신날", substitute=SubstituteRule.WEEKEND),
    LunarHoliday(8, 15, "추석", three_day=True, substitute=SubstituteRule.SUNDAY),
)

SPECIAL_HOLIDAYS: dict[int, tuple[SolarHoliday, ...]] = {
    2024: (SolarHoliday(4, 10, "제22대 국회의원 선거일"),),
    2025: (SolarHoliday(6, 3, "제21대 대통령 선거일"),),
    2026: (SolarHoliday(6, 3, "제9회 전국동시지방선거"),),
    2028: (SolarHoliday(4, 12, "제23대 국회의원 선거일"),),
    2030: (SolarHoliday(3, 27, "제22대 대통령 선거일"),),
    2035: (SolarHoliday(3, 28, "제23대 대통령 선거일"),),
}
