from datetime import date, timedelta


def previous_week_monday() -> date:
    today = date.today()
    return today + timedelta(days=-today.weekday(), weeks=-1)


def previous_week_friday() -> date:
    return previous_week_monday() + timedelta(days=5)
