from datetime import date
from typing import Tuple



def get_age_3(date_of_birth: date) -> Tuple[int, int, int]:
    today = date.today()
    birth_date = date_of_birth
    
    # Calculate the difference in years
    years = today.year - birth_date.year
    
    # Calculate the difference in months and days
    if (today.month, today.day) < (birth_date.month, birth_date.day):
        years -= 1
        months = today.month - birth_date.month + 12
        days = today.day - birth_date.day + (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days
        if days >= (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days:
            days -= (date(today.year, today.month, 1) - date(today.year, today.month - 1, 1)).days
            months += 1
        if months >= 12:
            months -= 12
            years += 1
    else:
        months = today.month - birth_date.month
        days = today.day - birth_date.day
        if days < 0:
            months -= 1
            previous_month = today.month - 1 if today.month > 1 else 12
            days += (date(today.year, today.month, 1) - date(today.year, previous_month, 1)).days

    return years, months, days
