from datetime import datetime
from dateutil.relativedelta import relativedelta

def calculate_age(date_of_birth):
    """
    Calculate the age of a person given their date of birth.

    Args:
        date_of_birth (datetime.date): The date of birth.

    Returns:
        int: The age in years.
    """
    if not date_of_birth:
        raise ValueError("The date_of_birth is required")
    
    today = datetime.today().date()
    age = relativedelta(today, date_of_birth)
    return age.years

