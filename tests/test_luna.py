from datetime import date

import pytest

from ppalgannal.luna import lunar_to_solar
from ppalgannal.luna.constant import LUNAR_MAX_YEAR, LUNAR_MIN_YEAR


class TestLunarToSolar:
    @pytest.mark.parametrize(
        "lunar_year, lunar_month, lunar_day, expected_solar_date",
        [
            # 2024년 설날 (음력 1월 1일)
            (2024, 1, 1, date(2024, 2, 10)),
            # 2024년 부처님오신날 (음력 4월 8일)
            (2024, 4, 8, date(2024, 5, 15)),
            # 2024년 추석 (음력 8월 15일)
            (2024, 8, 15, date(2024, 9, 17)),
            # 2025년 설날
            (2025, 1, 1, date(2025, 1, 29)),
            # 2025년 추석
            (2025, 8, 15, date(2025, 10, 6)),
            # 2026년 설날
            (2026, 1, 1, date(2026, 2, 17)),
            # 2026년 추석
            (2026, 8, 15, date(2026, 9, 25)),
        ],
    )
    def test_known_lunar_dates(
        self, lunar_year, lunar_month, lunar_day, expected_solar_date
    ):
        assert lunar_to_solar(lunar_year, lunar_month, lunar_day) == expected_solar_date

    def test_invalid_types(self):
        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2024.0, 1, 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2024, "1", 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            # bool is subclass of int in Python, should be rejected
            lunar_to_solar(True, 1, 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2024, False, 1)  # type: ignore

    def test_year_out_of_range(self):
        with pytest.raises(ValueError, match="lunar year must be between"):
            lunar_to_solar(LUNAR_MIN_YEAR - 1, 1, 1)

        with pytest.raises(ValueError, match="lunar year must be between"):
            lunar_to_solar(LUNAR_MAX_YEAR + 1, 1, 1)

    def test_invalid_month(self):
        with pytest.raises(ValueError, match="lunar month must be between 1 and 12"):
            lunar_to_solar(2024, 0, 1)

        with pytest.raises(ValueError, match="lunar month must be between 1 and 12"):
            lunar_to_solar(2024, 13, 1)

    def test_invalid_day(self):
        with pytest.raises(ValueError, match="invalid lunar day"):
            lunar_to_solar(2024, 1, 0)

        with pytest.raises(ValueError, match="invalid lunar day"):
            # 음력 한 달은 29일 1또는 30일
            lunar_to_solar(2024, 1, 31)
