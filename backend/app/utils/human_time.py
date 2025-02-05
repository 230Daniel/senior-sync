from datetime import datetime


def to_human_time(timestamp: datetime):
    """
    Convert a DateTime to a lovely string.
    Example: 'Thursday the 23rd of January 2025 at 9:32 PM'
    """
    day_suffix = { 1 : "st", 2 : "nd", 3 : "rd" }.get(timestamp.day % 10, "th")
    hour = timestamp.strftime("%I").lstrip("0")
    return timestamp.strftime(f"%A the {timestamp.day}{day_suffix} of %B %Y at {hour}:%M %p")
