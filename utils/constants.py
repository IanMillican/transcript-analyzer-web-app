MONTH_TO_INT = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}

MONTH_ABBR_MAP = {
    "Jan": 1, "Feb": 2, "Mar": 3, "Apr": 4,
    "May": 5, "Jun": 6, "Jul": 7, "Aug": 8,
    "Sep": 9, "Oct": 10, "Nov": 11, "Dec": 12
}

INT_TO_MONTH = {v: k for k, v in MONTH_TO_INT.items()}

def month_int_converter(input: str | int) -> int | str:
    """A function that accepts a month as the nume, the abbreviation, or the number corresponding to that month, and reuturns the other.

    Args:
        input (str | int): The name/abbreviation of the month, or the number 1-12 corresponding to that month.

    Raises:
        ValueError: Raised if the input doesn't correspond to any month string or is a number outiside of 1-12 or is not an int datatype

    Returns:
        int | str: The corresponding month to the given input. Either The full written month (not abbreviated) or the integer corresponding to the input.
    """
    error_msg = f"Invalid input '{input}'. Expected a month name or an integer from 1 to 12."
    if isinstance(input, str):
        if input in MONTH_TO_INT:
            return MONTH_TO_INT[input]
        elif input in MONTH_ABBR_MAP:
            return MONTH_ABBR_MAP[input]
        else:
            raise ValueError(error_msg)
    elif isinstance(input, int):
        if input < 1 or input > 12:
            raise ValueError(error_msg)
        return INT_TO_MONTH[input]
    else:
        raise ValueError(error_msg)