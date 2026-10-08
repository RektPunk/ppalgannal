<div style="text-align: center;">
  <img src="https://capsule-render.vercel.app/api?type=transparent&fontColor=0047AB&text=ppalgannal&height=120&fontSize=90">
</div>

Korean holidays, aka the red days. A lightweight, zero-dependency Python library for South Korean public and substitute holidays.

## Installation

Requires Python 3.10+.

```bash
pip install ppalgannal
```

## Quick Start

```python
from datetime import date

from ppalgannal import get_holidays, is_holiday, is_today_holiday

# 1. Get all holidays for a year
for holiday in get_holidays(2026):
    print(
        holiday.date,
        holiday.name,
        "(Substitute)" if holiday.is_substitute else "",
    )

# 2. Check if a date is a holiday (accepts date or ISO string)
print(is_holiday("2027-01-01"))  # True (New Year's Day)
print(is_holiday("2027-02-09"))  # True (Seollal Substitute Holiday)
print(is_holiday(date(2027, 5, 5)))  # True (Children's Day)
print(is_holiday("2027-05-03"))  # True (Labor Day)

# 3. Check if today is a holiday in Korea (KST)
if is_today_holiday():
    print("Today is a holiday!")
```
