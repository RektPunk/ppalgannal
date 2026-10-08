from datetime import date, datetime
from unittest.mock import patch

import pytest

from ppalgannal.holidays import (
    get_holidays,
    is_holiday,
    is_holiday_today,
)
from ppalgannal.holidays.constant import KST, SPECIAL_HOLIDAYS, Holiday


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
        holidays = {h.date: h.name for h in get_holidays(2027)}
        target_date = date(2027, month, day)

        assert target_date in holidays
        assert holidays[target_date] == expected_name


class TestLunarHolidays:
    def test_lunar_holidays_2027(self):
        holidays = {h.date: h.name for h in get_holidays(2027)}

        # Seollal
        assert holidays[date(2027, 2, 6)] == "설날 전날"
        assert holidays[date(2027, 2, 7)] == "설날"
        assert holidays[date(2027, 2, 8)] == "설날 다음날"

        # Buddha's Birthday
        assert holidays[date(2027, 5, 13)] == "부처님오신날"

        # Chuseok
        assert holidays[date(2027, 9, 14)] == "추석 전날"
        assert holidays[date(2027, 9, 15)] == "추석"
        assert holidays[date(2027, 9, 16)] == "추석 다음날"


class TestSpecialHolidays:
    def test_election_days(self):
        holidays_2024 = {h.date: h.name for h in get_holidays(2024)}
        assert date(2024, 4, 10) in holidays_2024
        assert holidays_2024[date(2024, 4, 10)] == "제22대 국회의원 선거일"

        holidays_2025 = {h.date: h.name for h in get_holidays(2025)}
        assert date(2025, 6, 3) in holidays_2025
        assert holidays_2025[date(2025, 6, 3)] == "대통령 선거일"

        holidays_2026 = {h.date: h.name for h in get_holidays(2026)}
        assert date(2026, 6, 3) in holidays_2026
        assert holidays_2026[date(2026, 6, 3)] == "제9회 전국동시지방선거"

        assert 2027 not in SPECIAL_HOLIDAYS


class TestSubstituteHolidays:
    def test_lunar_three_day_substitute(self):
        holidays = {h.date: h for h in get_holidays(2027)}
        sub_date = date(2027, 2, 9)

        assert sub_date in holidays
        assert holidays[sub_date].name == "설날 대체공휴일"
        assert holidays[sub_date].is_substitute is True

    def test_solar_weekend_substitutes(self):
        holidays = {h.date: h for h in get_holidays(2027)}

        assert date(2027, 5, 3) in holidays
        assert holidays[date(2027, 5, 3)].name == "노동절 대체공휴일"
        assert holidays[date(2027, 5, 3)].is_substitute is True

        assert date(2027, 7, 19) in holidays
        assert holidays[date(2027, 7, 19)].name == "제헌절 대체공휴일"
        assert holidays[date(2027, 7, 19)].is_substitute is True

        assert date(2027, 8, 16) in holidays
        assert holidays[date(2027, 8, 16)].name == "광복절 대체공휴일"
        assert holidays[date(2027, 8, 16)].is_substitute is True

        assert date(2027, 10, 4) in holidays
        assert holidays[date(2027, 10, 4)].name == "개천절 대체공휴일"
        assert holidays[date(2027, 10, 4)].is_substitute is True

        assert date(2027, 10, 11) in holidays
        assert holidays[date(2027, 10, 11)].name == "한글날 대체공휴일"
        assert holidays[date(2027, 10, 11)].is_substitute is True

        assert date(2027, 12, 27) in holidays
        assert holidays[date(2027, 12, 27)].name == "기독탄신일 대체공휴일"
        assert holidays[date(2027, 12, 27)].is_substitute is True

    def test_lunar_three_day_without_sunday(self):
        holidays = {h.date: h for h in get_holidays(2027)}
        sub_names = [h.name for h in holidays.values() if "추석 대체공휴일" in h.name]
        assert len(sub_names) == 0

    def test_no_substitute_for_none_rule(self):
        holidays = {h.date: h for h in get_holidays(2027)}
        assert date(2027, 6, 6) in holidays
        assert date(2027, 6, 7) not in holidays


class TestGetHolidays:
    def test_sorted_by_date(self):
        holidays = get_holidays(2027)
        dates = [h.date for h in holidays]
        assert dates == sorted(dates)

    def test_return_type_and_structure(self):
        holidays = get_holidays(2027)
        assert isinstance(holidays, list)
        for h in holidays:
            assert isinstance(h, Holiday)
            assert isinstance(h.date, date)
            assert isinstance(h.name, str)
            assert isinstance(h.is_substitute, bool)

    def test_cache_immutability(self):
        first_call = get_holidays(2027)
        original_len = len(first_call)

        first_call.pop()
        assert len(first_call) == original_len - 1

        second_call = get_holidays(2027)
        assert len(second_call) == original_len
        assert first_call != second_call


class TestIsHoliday:
    @pytest.mark.parametrize(
        "test_input, expected",
        [
            (date(2027, 1, 1), True),
            ("2027-01-01", True),
            (date(2027, 2, 7), True),
            ("2027-02-09", True),
            (date(2027, 5, 1), True),
            ("2027-05-03", True),
            ("2027-09-15", True),
            ("2027-01-04", False),
            (date(2027, 1, 2), False),
            (date(2027, 1, 3), False),
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
        mock_now = datetime(2027, 1, 1, 10, 0, 0, tzinfo=KST)
        mock_datetime.now.return_value = mock_now

        assert is_holiday_today() is True

    @patch("ppalgannal.holidays.calc.datetime")
    def test_today_is_not_holiday(self, mock_datetime):
        mock_now = datetime(2027, 1, 4, 10, 0, 0, tzinfo=KST)
        mock_datetime.now.return_value = mock_now

        assert is_holiday_today() is False
