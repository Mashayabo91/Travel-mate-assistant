from datetime import date


def search_flights(
    origin: str,
    destination: str,
    start_date: date,
    days: int,
    context: dict,
) -> list:
    """
    Returns a list of available flight options.

    Demo mode: returns safe mock data — no external API calls, no charges.
    Live mode: replace this function body with your Duffel or Amadeus API call.
               The agent only reads: airline, departure, arrival, duration, stops, price_ngn.
    """
    cabin = context.get("cabin", "Economy")

    # Cabin price multiplier
    multiplier = {"Economy": 1.0, "Premium Economy": 1.6, "Business": 2.8}.get(cabin, 1.0)

    return [
        {
            "airline": "Air Peace",
            "departure": "07:00",
            "arrival": "08:15",
            "duration": "1h 15m",
            "stops": 0,
            "price_ngn": int(85_000 * multiplier),
        },
        {
            "airline": "Ibom Air",
            "departure": "12:30",
            "arrival": "13:50",
            "duration": "1h 20m",
            "stops": 0,
            "price_ngn": int(78_000 * multiplier),
        },
        {
            "airline": "United Nigeria Airlines",
            "departure": "17:45",
            "arrival": "19:10",
            "duration": "1h 25m",
            "stops": 0,
            "price_ngn": int(72_000 * multiplier),
        },
    ]
