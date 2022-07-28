class UserNotRegisteredError(Exception):
    """Raised when the user who calls the method is not registered with the bot."""
    pass


class InvalidDatetimeError(Exception):
    """Raised when input date and/or time is invalid."""
    pass
