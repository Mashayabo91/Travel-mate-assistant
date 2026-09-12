import json
import os
import re
from datetime import datetime, timedelta

from tools.calendar_tool import check_calendar
from tools.flight_tool import search_flights
from tools.accommodation_tool import search_accommodation

SYSTEM_PROMPT = """You are TravelMate AI, a friendly and concise travel-planning assistant.
Your job is to understand the user's travel request and build a practical, budget-aware itinerary.

Rules:
- Never claim a real booking happened unless a booking tool confirmed it.
- In demo mode, clearly label all results as simulated.
- Always require explicit user confirmation before any real booking.
- Respect the user's origin, cabin class, passenger count, and budget.
- If destination or trip length is missing, ask one clear question — never invent details.
- Return structured replies with: dates, flight details, accommodation, and an estimated total in ₦.
"""


class TravelAgent:
    def __init__(self):
        self.groq_key = os.getenv("GROQ_API_KEY")
        self.groq_model = os.getenv("GROQ_MODEL", "llama3-70b-8192")
        self.client = None

        if self.groq_key:
            try:
                from groq import Groq
                self.client = Groq(api_key=self.groq_key)
            except ImportError:
                pass  # Groq not installed — demo mode only

    # ── Public entry point ────────────────────────────────────────────
    def run(self, user_request: str, context: dict) -> str:
        if context.get("demo_mode", True):
            return self._demo_plan(user_request, context)
        if not self.client:
            return (
                "⚠️ **Live mode is on but GROQ_API_KEY is not set.**\n\n"
                "Either add your Groq API key to the environment, or switch back to "
                "**Demo mode** in the sidebar to explore with safe mock data."
            )
        return self._llm_plan(user_request, context)

    # ── Demo plan (no external calls) ────────────────────────────────
    def _demo_plan(self, request: str, context: dict) -> str:
        destination = self._extract_destination(request)
        days = self._extract_days(request) or 4
        passengers = context.get("passengers", 1)
        cabin = context.get("cabin", "Economy")
        budget = context.get("budget_ngn", 300_000)

        start = datetime.now().date() + timedelta(days=10)
        windows = check_calendar(start, days)
        chosen_date = windows[0]

        flights = search_flights(
            context["origin"], destination, chosen_date, days, context
        )
        hotels = search_accommodation(destination, chosen_date, days, context)

        flight = flights[0]
        hotel = hotels[0]

        flight_total = flight["price_ngn"] * passengers
        hotel_total = hotel["total_ngn"]
        grand_total = flight_total + hotel_total

        end_date = chosen_date + timedelta(days=days)
        over_budget = grand_total > budget

        budget_line = (
            f"⚠️ ₦{grand_total:,} exceeds your budget of ₦{budget:,} by ₦{grand_total - budget:,}."
            if over_budget
            else f"✅ Within your ₦{budget:,} budget."
        )

        return f"""### ✨ Recommended trip — {context['origin']} → {destination}

**📅 Dates:** {chosen_date.strftime('%d %b %Y')} – {end_date.strftime('%d %b %Y')} ({days} nights)  
**👤 Passengers:** {passengers} · **Cabin:** {cabin}

---

#### ✈️ Flight
**{flight['airline']}**  
Departure {flight['departure']} → Arrival {flight['arrival']} · {flight['duration']} · {flight['stops']} stop(s)  
₦{flight['price_ngn']:,} per person × {passengers} = **₦{flight_total:,}**

---

#### 🏨 Accommodation
**{hotel['name']}** — {hotel['area']}  
{days} nights · Rating: {'⭐' * int(hotel['rating'])}  
**₦{hotel_total:,}**

---

#### 💰 Estimated total
**₦{grand_total:,}**  
{budget_line}

---

> 🧪 **Demo mode — no real bookings or charges.**  
> To go live, add your `GROQ_API_KEY` and disable Demo mode in the sidebar.

**Next step:** type *"confirm"* to proceed, or ask me to compare other options."""

    # ── Live Groq plan ─────────────────────────────────────────────────
    def _llm_plan(self, request: str, context: dict) -> str:
        prompt = (
            f"User request: {request}\n"
            f"Preferences: {json.dumps(context)}\n"
            f"Today: {datetime.now().date()}\n\n"
            "Provide a concise travel plan with dates, flight summary, accommodation summary, "
            "and estimated total cost in Nigerian Naira (₦). "
            "If destination or trip length is missing, ask one question instead of guessing."
        )

        response = self.client.chat.completions.create(
            model=self.groq_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=600,
        )
        return response.choices[0].message.content

    # ── Helpers ────────────────────────────────────────────────────────
    @staticmethod
    def _extract_destination(request: str) -> str:
        low = request.lower()
        destinations = {
            "lagos": "Lagos (LOS)",
            "abuja": "Abuja (ABV)",
            "kano": "Kano (KAN)",
            "port harcourt": "Port Harcourt (PHC)",
            "enugu": "Enugu (ENU)",
            "accra": "Accra (ACC)",
            "nairobi": "Nairobi (NBO)",
            "london": "London (LHR)",
            "dubai": "Dubai (DXB)",
            "rome": "Rome (FCO)",
            "paris": "Paris (CDG)",
        }
        for key, value in destinations.items():
            if key in low:
                return value
        return "Lagos (LOS)"

    @staticmethod
    def _extract_days(request: str):
        m = re.search(r"(\d+)\s*(?:day|days|night|nights)", request.lower())
        return int(m.group(1)) if m else None
