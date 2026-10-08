from datetime import date

import pytest

from ppalgannal.lunar import lunar_to_solar
from ppalgannal.lunar.constant import LUNAR_MAX_YEAR, LUNAR_MIN_YEAR


class TestLunarToSolar:
    @pytest.mark.parametrize(
        "lunar_year, lunar_month, lunar_day, expected_solar_date",
        [
            (2027, 1, 1, date(2027, 2, 7)),  # Seollal
            (2027, 4, 8, date(2027, 5, 13)),  # Buddha's Birthday
            (2027, 8, 15, date(2027, 9, 15)),  # Chuseok
        ],
    )
    def test_known_lunar_dates(
        self, lunar_year, lunar_month, lunar_day, expected_solar_date
    ):
        assert lunar_to_solar(lunar_year, lunar_month, lunar_day) == expected_solar_date

    def test_invalid_types(self):
        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2027.0, 1, 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2027, "1", 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            # bool is subclass of int in Python, should be rejected
            lunar_to_solar(True, 1, 1)  # type: ignore

        with pytest.raises(TypeError, match="must be integers"):
            lunar_to_solar(2027, False, 1)  # type: ignore

    def test_year_out_of_range(self):
        with pytest.raises(ValueError, match="lunar year must be between"):
            lunar_to_solar(LUNAR_MIN_YEAR - 1, 1, 1)

        with pytest.raises(ValueError, match="lunar year must be between"):
            lunar_to_solar(LUNAR_MAX_YEAR + 1, 1, 1)

    def test_invalid_month(self):
        with pytest.raises(ValueError, match="lunar month must be between 1 and 12"):
            lunar_to_solar(2027, 0, 1)

        with pytest.raises(ValueError, match="lunar month must be between 1 and 12"):
            lunar_to_solar(2027, 13, 1)

    def test_invalid_day(self):
        with pytest.raises(ValueError, match="invalid lunar day"):
            lunar_to_solar(2027, 1, 0)

        with pytest.raises(ValueError, match="invalid lunar day"):
            # January 2027 has 30 lunar days, so day 31 is invalid
            lunar_to_solar(2027, 1, 31)

    def test_boundary_years(self):
        min_solar = lunar_to_solar(LUNAR_MIN_YEAR, 1, 1)
        assert isinstance(min_solar, date)
        assert min_solar.year == LUNAR_MIN_YEAR

        max_solar = lunar_to_solar(LUNAR_MAX_YEAR, 12, 1)
        assert isinstance(max_solar, date)
        assert max_solar.year >= LUNAR_MAX_YEAR
