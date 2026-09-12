import streamlit as st
from agent.travel_agent import TravelAgent

st.set_page_config(
    page_title="TravelMate AI",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Page background */
.stApp {
    background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 100%);
    min-height: 100vh;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: #0f172a !important;
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] * {
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stSelectbox select {
    background: #1e293b !important;
    color: #f1f5f9 !important;
    border: 1px solid rgba(255,255,255,0.1) !important;
    border-radius: 8px !important;
}

/* Hero */
.hero-wrap {
    padding: 2.5rem 2rem 1.2rem 2rem;
    text-align: left;
}
.hero-eyebrow {
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.12em;
    color: #60a5fa;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.hero-title {
    font-size: 2.8rem;
    font-weight: 700;
    color: #f8fafc;
    margin: 0 0 0.4rem 0;
    line-height: 1.1;
}
.hero-sub {
    font-size: 1rem;
    color: #94a3b8;
    margin: 0;
}

/* Chat messages */
.msg-user {
    background: #1e40af;
    color: #f0f9ff;
    border-radius: 18px 18px 4px 18px;
    padding: 0.85rem 1.1rem;
    margin: 0.4rem 0;
    max-width: 80%;
    margin-left: auto;
    font-size: 0.95rem;
    line-height: 1.55;
}
.msg-agent {
    background: #1e293b;
    color: #e2e8f0;
    border-radius: 18px 18px 18px 4px;
    padding: 0.85rem 1.1rem;
    margin: 0.4rem 0;
    max-width: 86%;
    font-size: 0.95rem;
    line-height: 1.6;
    border: 1px solid rgba(255,255,255,0.06);
}
.msg-agent h3 {
    color: #f1f5f9;
    font-size: 1.05rem;
    margin-top: 0.6rem;
}
.msg-agent strong { color: #93c5fd; }
.msg-agent blockquote {
    border-left: 3px solid #3b82f6;
    padding-left: 0.75rem;
    color: #94a3b8;
    font-size: 0.88rem;
    margin: 0.5rem 0 0 0;
}

/* Welcome card */
.welcome-card {
    background: rgba(30, 41, 59, 0.7);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 1.8rem 2rem;
    margin: 1rem 2rem;
    color: #cbd5e1;
}
.welcome-card h3 { color: #f1f5f9; margin-top: 0; }
.welcome-card .example {
    background: rgba(59,130,246,0.15);
    border: 1px solid rgba(59,130,246,0.3);
    border-radius: 10px;
    padding: 0.6rem 1rem;
    margin: 0.4rem 0;
    font-size: 0.9rem;
    color: #93c5fd;
    cursor: pointer;
}

/* Demo badge */
.demo-badge {
    display: inline-block;
    background: rgba(234,179,8,0.15);
    border: 1px solid rgba(234,179,8,0.4);
    color: #fbbf24;
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.25rem 0.65rem;
    border-radius: 999px;
    margin-bottom: 1rem;
}

/* Input area */
[data-testid="stChatInput"] {
    border-radius: 14px !important;
}
</style>
""", unsafe_allow_html=True)

# ── State ──────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "agent" not in st.session_state:
    st.session_state.agent = TravelAgent()

# ── Sidebar ────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### ✈️ TravelMate AI")
    st.markdown("---")
    st.markdown("**Trip preferences**")
    st.caption("Optional — the agent asks for anything missing.")

    origin = st.text_input("Departure city / airport", "Abuja (ABV)")
    passengers = st.number_input("Passengers", min_value=1, max_value=9, value=1)
    cabin = st.selectbox("Cabin class", ["Economy", "Premium Economy", "Business"])
    budget = st.number_input("Max budget (₦)", min_value=0, value=300_000, step=25_000)
    demo_mode = st.toggle("Demo mode (safe mock data)", value=True)

    if demo_mode:
        st.markdown('<div style="margin-top:0.5rem"><span style="background:rgba(234,179,8,0.15);border:1px solid rgba(234,179,8,0.35);color:#fbbf24;font-size:0.75rem;font-weight:600;padding:0.2rem 0.6rem;border-radius:999px;">DEMO</span> No real bookings or charges.</div>', unsafe_allow_html=True)
    else:
        st.warning("Live mode: requires GROQ_API_KEY in your environment.", icon="⚠️")

    st.markdown("---")
    if st.button("🗑️ Clear chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("Built for the AFX Academy agentic AI assignment.")

# ── Hero ───────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-wrap">
  <div class="hero-eyebrow">Agentic AI Travel Planner</div>
  <h1 class="hero-title">Where to next?</h1>
  <p class="hero-sub">Tell me your destination and dates — I'll handle flights, hotels, and the itinerary.</p>
</div>
""", unsafe_allow_html=True)

# ── Welcome screen (no messages yet) ──────────────────────────────────
if not st.session_state.messages:
    st.markdown("""
<div class="welcome-card">
  <h3>Try one of these</h3>
  <div class="example">✈️ "I want to travel to Lagos for 4 days next month."</div>
  <div class="example">🏖️ "Plan a 7-day trip to Accra for 2 people under ₦500,000."</div>
  <div class="example">🏙️ "Weekend trip to Kano, economy class, just me."</div>
  <br/>
  <p style="font-size:0.85rem;color:#64748b;margin:0;">
    TravelMate checks your calendar window, finds the best flight and hotel,
    and gives you a full cost breakdown — before asking for any confirmation.
  </p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ───────────────────────────────────────────────────────
for role, text in st.session_state.messages:
    if role == "user":
        st.markdown(f'<div class="msg-user">{text}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="msg-agent">{text}</div>', unsafe_allow_html=True)

# ── Chat input ─────────────────────────────────────────────────────────
prompt = st.chat_input("Where would you like to go?")

if prompt:
    st.session_state.messages.append(("user", prompt))

    context = {
        "origin": origin,
        "passengers": passengers,
        "cabin": cabin,
        "budget_ngn": budget,
        "demo_mode": demo_mode,
    }

    with st.spinner("Planning your trip…"):
        reply = st.session_state.agent.run(prompt, context)

    st.session_state.messages.append(("assistant", reply))
    st.rerun()
