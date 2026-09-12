from datetime import date, timedelta


def check_calendar(start_date: date, trip_days: int):
    """
    Returns a list of available start dates for the trip.

    Demo mode: deterministic mock — no external API calls.
    Live mode: replace the body of this function with your Google Calendar
               OAuth integration. The rest of the agent does not need to change.
    """
    # Mock: three candidate windows spaced a week apart
    return [
        start_date,
        start_date + timedelta(days=7),
        start_date + timedelta(days=14),
    ]
