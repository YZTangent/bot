from datetime import datetime
from connection.exceptions import InvalidDatetimeError


def past_future_check(date: datetime) -> str:
    now = datetime.now()

    if date < now:
        return "past"
    elif date > now:
        return "future"
    else:
        return "now"


def datetime_validation(year: int, month: int, day: int, hour: int = 0, minute: int = 0, second: int = 0) -> datetime:
    try:
        return datetime(int(year), int(month), int(day), hour, minute, second)
    except ValueError:
        raise InvalidDatetimeError
