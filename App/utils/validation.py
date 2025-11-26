import re
from datetime import datetime

def validate_username(username):
    """Validates that the username is alphanumeric and between 3-20 characters."""
    if not username or not isinstance(username, str):
        return False
    return bool(re.match(r'^[a-zA-Z0-9]{3,20}$', username))

def validate_password(password):
    """Validates that the password is at least 8 characters long."""
    if not password or not isinstance(password, str):
        return False
    return len(password) >= 8

def validate_date(date_str):
    """Validates that the date string is in YYYY-MM-DD format."""
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

def validate_time(time_str):
    """Validates that the time string is in HH:MM format."""
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False

def validate_required_fields(data, required_fields):
    """Validates that all required fields are present in the data dictionary."""
    if not data:
        return False
    for field in required_fields:
        if field not in data or not data[field]:
            return False
    return True
