import ppalgannal
from ppalgannal import get_holidays, is_holiday, is_today_holiday


def test_package_exports():
    assert ppalgannal.get_holidays is get_holidays
    assert ppalgannal.is_holiday is is_holiday
    assert ppalgannal.is_today_holiday is is_today_holiday
    assert set(ppalgannal.__all__) == {
        "get_holidays",
        "is_holiday",
        "is_today_holiday",
    }
