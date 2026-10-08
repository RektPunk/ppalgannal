from datetime import date, datetime
from unittest.mock import patch

import pytest

from ppalgannal.holidays import (
    get_holidays,
    is_holiday,
    is_today_holiday,
)
from ppalgannal.holidays.constant import KST, Holiday


class TestSolarHolidays:
    @pytest.mark.parametrize(
        "expected_month_day, expected_name",
        [
            ((1, 1), "신정"),
            ((3, 1), "삼일절"),
            ((5, 1), "노동절"),
            ((5, 5), "어린이날"),
            ((6, 6), "현충일"),
            ((7, 17), "제헌절"),
            ((8, 15), "광복절"),
            ((10, 3), "개천절"),
            ((10, 9), "한글날"),
            ((12, 25), "기독탄신일"),
        ],
    )
    def test_fixed_solar_holidays(self, expected_month_day, expected_name):
        month, day = expected_month_day
        holidays = {h.date: h.name for h in get_holidays(2024)}
        target_date = date(2024, month, day)

        assert target_date in holidays
        assert holidays[target_date] == expected_name


class TestLunarHolidays:
    def test_lunar_holidays_2024(self):
        holidays = {h.date: h.name for h in get_holidays(2024)}

        # 2024년 설날 연휴 (2/9 ~ 2/11)
        assert holidays[date(2024, 2, 9)] == "설날 전날"
        assert holidays[date(2024, 2, 10)] == "설날"
        assert holidays[date(2024, 2, 11)] == "설날 다음날"

        # 2024년 부처님오신날 (5/15)
        assert holidays[date(2024, 5, 15)] == "부처님오신날"

        # 2024년 추석 연휴 (9/16 ~ 9/18)
        assert holidays[date(2024, 9, 16)] == "추석 전날"
        assert holidays[date(2024, 9, 17)] == "추석"
        assert holidays[date(2024, 9, 18)] == "추석 다음날"


class TestSpecialHolidays:
    def test_election_days(self):
        # 2024년 제22대 국회의원 선거일 (4/10)
        holidays_2024 = {h.date: h.name for h in get_holidays(2024)}
        assert date(2024, 4, 10) in holidays_2024
        assert holidays_2024[date(2024, 4, 10)] == "제22대 국회의원 선거일"

        # 2025년 대통령 선거일 (6/3)
        holidays_2025 = {h.date: h.name for h in get_holidays(2025)}
        assert date(2025, 6, 3) in holidays_2025
        assert holidays_2025[date(2025, 6, 3)] == "대통령 선거일"

        # 2026년 제9회 전국동시지방선거 (6/3)
        holidays_2026 = {h.date: h.name for h in get_holidays(2026)}
        assert date(2026, 6, 3) in holidays_2026
        assert holidays_2026[date(2026, 6, 3)] == "제9회 전국동시지방선거"


class TestSubstituteHolidays:
    def test_lunar_three_day_substitute(self):
        # 2024년 설날 연휴 (2/9 금, 2/10 토, 2/11 일) -> 2/11이 일요일이므로 2/12 월요일이 대체공휴일
        holidays = {h.date: h for h in get_holidays(2024)}
        sub_date = date(2024, 2, 12)

        assert sub_date in holidays
        assert holidays[sub_date].name == "설날 대체공휴일"
        assert holidays[sub_date].is_substitute is True

    def test_solar_weekend_substitute(self):
        # 2024년 어린이날 (5/5 일) -> 5/6 월요일이 대체공휴일
        holidays = {h.date: h for h in get_holidays(2024)}
        sub_date = date(2024, 5, 6)

        assert sub_date in holidays
        assert holidays[sub_date].name == "어린이날 대체공휴일"
        assert holidays[sub_date].is_substitute is True

    def test_buddha_birthday_weekend_substitute(self):
        # 2023년 부처님오신날 (5/27 토) -> 5/29 월요일이 대체공휴일
        holidays = {h.date: h for h in get_holidays(2023)}
        sub_date = date(2023, 5, 29)

        assert sub_date in holidays
        assert holidays[sub_date].name == "부처님오신날 대체공휴일"
        assert holidays[sub_date].is_substitute is True

    def test_lunar_three_day_without_sunday(self):
        # 2025년 설날 연휴 (1/28 화, 1/29 수, 1/30 목) -> 일요일이 포함되지 않으므로 대체공휴일 없음
        holidays = {h.date: h for h in get_holidays(2025)}
        sub_names = [h.name for h in holidays.values() if "설날 대체공휴일" in h.name]
        assert len(sub_names) == 0

    def test_no_substitute_for_none_rule(self):
        # 현충일 (6/6)은 substitute rule이 NONE -> 일요일이더라도 대체공휴일 없음
        # 2021년 6월 6일은 일요일
        holidays_2021 = {h.date: h for h in get_holidays(2021)}
        assert date(2021, 6, 6) in holidays_2021
        assert date(2021, 6, 7) not in holidays_2021


class TestGetHolidays:
    def test_sorted_by_date(self):
        holidays = get_holidays(2024)
        dates = [h.date for h in holidays]
        assert dates == sorted(dates)

    def test_return_type_and_structure(self):
        holidays = get_holidays(2024)
        assert isinstance(holidays, list)
        for h in holidays:
            assert isinstance(h, Holiday)
            assert isinstance(h.date, date)
            assert isinstance(h.name, str)
            assert isinstance(h.is_substitute, bool)

    def test_cache_immutability(self):
        first_call = get_holidays(2024)
        original_len = len(first_call)

        first_call.pop()
        assert len(first_call) == original_len - 1

        second_call = get_holidays(2024)
        assert len(second_call) == original_len
        assert first_call != second_call


class TestIsHoliday:
    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (date(2024, 1, 1), True),  # 신정 (date 객체)
            ("2024-01-01", True),  # 신정 (문자열)
            (date(2024, 2, 10), True),  # 설날 당일
            ("2024-02-12", True),  # 설날 대체공휴일
            ("2024-04-10", True),  # 국회의원 선거일
            ("2024-01-02", False),  # 일반 평일
            (date(2024, 1, 6), False),  # 공휴일이 아닌 일반 토요일
            (date(2024, 1, 7), False),  # 공휴일이 아닌 일반 일요일
        ],
    )
    def test_is_holiday_inputs(self, test_input, expected):
        assert is_holiday(test_input) is expected

    def test_is_holiday_invalid_string(self):
        with pytest.raises(ValueError):
            is_holiday("invalid-date")


class TestIsTodayHoliday:
    @patch("ppalgannal.holidays.calc.datetime")
    def test_today_is_holiday(self, mock_datetime):
        mock_now = datetime(2024, 1, 1, 10, 0, 0, tzinfo=KST)
        mock_datetime.now.return_value = mock_now

        assert is_today_holiday() is True

    @patch("ppalgannal.holidays.calc.datetime")
    def test_today_is_not_holiday(self, mock_datetime):
        mock_now = datetime(2024, 1, 2, 10, 0, 0, tzinfo=KST)
        mock_datetime.now.return_value = mock_now

        assert is_today_holiday() is False
