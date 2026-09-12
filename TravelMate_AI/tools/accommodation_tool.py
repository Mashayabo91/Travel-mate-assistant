from datetime import date


def search_accommodation(
    destination: str,
    start_date: date,
    days: int,
    context: dict,
) -> list:
    """
    Returns a list of available accommodation options.

    Demo mode: returns safe mock data — no external API calls, no charges.
    Live mode: replace this function body with your Booking.com, Hotels.ng,
               or similar API call.
               The agent only reads: name, area, total_ngn, rating.
    """
    nightly_rates = [18_000, 22_500, 35_000, 55_000]
    hotels = [
        ("Protea Hotel by Marriott", "Victoria Island", 4.6, nightly_rates[3]),
        ("Best Western Plus Elegante", "Central district", 4.3, nightly_rates[2]),
        ("Ibis Budget", "Airport district", 3.9, nightly_rates[1]),
        ("TravelMate Guesthouse", "Mainland", 4.1, nightly_rates[0]),
    ]

    return [
        {
            "name": name,
            "area": area,
            "rating": rating,
            "total_ngn": rate * days,
        }
        for name, area, rating, rate in hotels
    ]
