from datetime import timedelta


def date_shift(date_val):
    """
    test
    """
    if date_val and date_val.isoweekday() == 5:
        additional_days = 3
    elif date_val and date_val.isoweekday() == 6:
        additional_days = 2
    elif date_val and date_val.isoweekday() == 7:
        additional_days = 1
    else:
        additional_days = 1

    return date_val + timedelta(days=additional_days)
