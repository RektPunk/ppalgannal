import ppalgannal
from ppalgannal import get_holidays, is_holiday, is_holiday_today


def test_package_exports():
    assert ppalgannal.get_holidays is get_holidays
    assert ppalgannal.is_holiday is is_holiday
    assert ppalgannal.is_holiday_today is is_holiday_today
    assert set(ppalgannal.__all__) == {
        "get_holidays",
        "is_holiday",
        "is_holiday_today",
    }
