from datetime import datetime, date
from typing import Tuple

def get_age(date_of_birth_str: str) -> Tuple[int, int, int]:
    # Convert the string to a date object
    date_of_birth = datetime.strptime(date_of_birth_str, "%d-%m-%Y").date()
    
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

# Example usage
dob_str = "13-03-1991"
age_years, age_months, age_days = get_age(dob_str)
print(f"{age_years} years, {age_months} months, and {age_days} days")
