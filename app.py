import os
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# Use Streamlit secrets in production, .env locally
api_key = st.secrets.get("GROQ_API_KEY", None) if hasattr(st, "secrets") else None
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)

SYSTEM_PROMPT = """You are an expert Facebook and Instagram ad copywriter.
When given a product, target audience, and key benefit — write exactly 5 ad copy variations.

Each variation must use a different angle:
1. Curiosity Hook
2. Problem → Solution
3. Social Proof
4. Urgency / Scarcity
5. Direct Benefit

Format your response EXACTLY like this for each variation:

### 1. Curiosity Hook
**Headline:** [headline here]
**Body:** [body copy here]

### 2. Problem → Solution
**Headline:** [headline here]
**Body:** [body copy here]

### 3. Social Proof
**Headline:** [headline here]
**Body:** [body copy here]

### 4. Urgency / Scarcity
**Headline:** [headline here]
**Body:** [body copy here]

### 5. Direct Benefit
**Headline:** [headline here]
**Body:** [body copy here]

Keep headlines under 10 words. Keep body under 30 words. Be punchy, direct, and conversion-focused."""

EXAMPLE_OUTPUT = """### 1. Curiosity Hook
**Headline:** Why Are 12,000 Sellers Switching to This?
**Body:** It's not luck. It's not budget. It's the one tool writing ads that actually convert.

### 2. Problem → Solution
**Headline:** Stop Wasting Hours Writing Ads That Flop
**Body:** AdCopy AI generates 5 tested angles in seconds. No copywriter. No guesswork. Just results.

### 3. Social Proof
**Headline:** 500+ Sellers Use This Every Single Day
**Body:** From dropshippers to 7-figure brands — everyone needs fresh ad copy. Now it takes 15 seconds.

### 4. Urgency / Scarcity
**Headline:** Free While We're in Beta — Not for Long
**Body:** We're adding paid plans soon. Get unlimited ad copy now before the price goes up.

### 5. Direct Benefit
**Headline:** 5 Ready-to-Run Ads. Any Product. 15 Seconds.
**Body:** Type your product, audience, and benefit. Get 5 Facebook and Instagram ad variations instantly."""

WAITLIST_URL = "https://docs.google.com/forms/d/1Zj8PQTNE3eI_rkjJKqu7gXtFN8kYcx1Whpera81b4PY/viewform"

st.set_page_config(
    page_title="AdCopy AI — Ad Generator for Ecom Sellers",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0d0d14; }
.block-container { padding: 2.5rem 2rem 4rem 2rem; max-width: 780px; }

.hero-badge {
    display: inline-block;
    background: rgba(99,102,241,0.12);
    color: #818cf8;
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    padding: 4px 14px;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    margin-bottom: 1.2rem;
}

.hero-title {
    font-size: 2.9rem;
    font-weight: 800;
    color: #f1f5f9;
    line-height: 1.15;
    margin-bottom: 1rem;
}

.hero-title span {
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

.hero-sub {
    color: #94a3b8;
    font-size: 1.05rem;
    line-height: 1.65;
    margin-bottom: 2rem;
}

.social-proof-bar {
    display: flex;
    align-items: center;
    gap: 1.5rem;
    background: #16171f;
    border: 1px solid #2a2b36;
    border-radius: 12px;
    padding: 1rem 1.5rem;
    margin-bottom: 2rem;
}

.sp-item {
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.85rem;
    color: #94a3b8;
}

.sp-dot { color: #6366f1; font-size: 1.1rem; }
.sp-bold { color: #f1f5f9; font-weight: 700; }

.stats-row {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.stat-item {
    background: #16171f;
    border: 1px solid #2a2b36;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    flex: 1;
    text-align: center;
}

.stat-number { font-size: 1.6rem; font-weight: 800; color: #6366f1; }
.stat-label { font-size: 0.75rem; color: #64748b; margin-top: 2px; }

.divider { border: none; border-top: 1px solid #1e1f2b; margin: 2rem 0; }

.section-label {
    font-size: 0.72rem;
    font-weight: 700;
    color: #64748b;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.example-box {
    background: #16171f;
    border: 1px solid #2a2b36;
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.example-box::before {
    content: 'LIVE EXAMPLE';
    position: absolute;
    top: 14px;
    right: 14px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    color: #6366f1;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    padding: 2px 10px;
}

.example-product {
    font-size: 0.8rem;
    color: #64748b;
    margin-bottom: 1rem;
}

.stTextInput > label {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.stTextInput > div > div > input {
    background-color: #16171f !important;
    color: #f1f5f9 !important;
    border: 1px solid #2a2b36 !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
}

.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
}

.stTextInput > div > div > input::placeholder { color: #3f4151 !important; }

.stFormSubmitButton > button, .stButton > button {
    background: linear-gradient(135deg, #6366f1, #7c3aed) !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem 2rem !important;
    border: none !important;
    border-radius: 10px !important;
    width: 100% !important;
    letter-spacing: 0.02em;
}

.stFormSubmitButton > button:hover, .stButton > button:hover { opacity: 0.9 !important; }

.email-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(124,58,237,0.08));
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 12px;
    padding: 1.5rem;
    margin-top: 2rem;
}

.email-title { font-size: 1rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.3rem; }
.email-sub { font-size: 0.85rem; color: #94a3b8; margin-bottom: 1rem; }

.footer { text-align: center; color: #3f4151; font-size: 0.78rem; margin-top: 3rem; }

.stAlert { background-color: #1e1f2b !important; border: 1px solid #2a2b36 !important; color: #94a3b8 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-badge">AI-Powered Ad Copy</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-title">Write <span>converting ads</span><br>in seconds.</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Generate 5 Facebook & Instagram ad variations for any product instantly. Built for dropshippers and ecom sellers who want better ads without hiring a copywriter.</div>', unsafe_allow_html=True)

# ── Social proof bar ──────────────────────────────────────────────────────────
st.markdown("""
<div class="social-proof-bar">
    <div class="sp-item"><span class="sp-dot">●</span><span><span class="sp-bold">Free</span> while in beta</span></div>
    <div class="sp-item"><span class="sp-dot">●</span><span>No signup needed</span></div>
    <div class="sp-item"><span class="sp-dot">●</span><span>Works for any product</span></div>
</div>
""", unsafe_allow_html=True)

# ── Stats ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-item"><div class="stat-number">5</div><div class="stat-label">Ad angles per run</div></div>
    <div class="stat-item"><div class="stat-number">&lt;15s</div><div class="stat-label">Generation time</div></div>
    <div class="stat-item"><div class="stat-number">∞</div><div class="stat-label">Products supported</div></div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Live example ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">See it in action</div>', unsafe_allow_html=True)
st.markdown('<div class="example-box"><div class="example-product">Product: AdCopy AI &nbsp;|&nbsp; Audience: Shopify sellers &nbsp;|&nbsp; Benefit: 5 ad variations in 15 seconds</div>', unsafe_allow_html=True)
st.markdown(EXAMPLE_OUTPUT)
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<hr class="divider">', unsafe_allow_html=True)

# ── Generate form ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Generate your ads</div>', unsafe_allow_html=True)

with st.form("ad_form"):
    product = st.text_input("Product name", placeholder="e.g. PeelEase 3-in-1 Peeler Set")
    audience = st.text_input("Target audience", placeholder="e.g. home cooks who hate meal prep")
    benefit = st.text_input("Key benefit", placeholder="e.g. peels faster with no hand strain")
    submitted = st.form_submit_button("Generate 5 Ad Variations")

if submitted:
    if not product or not audience or not benefit:
        st.warning("Please fill in all three fields.")
    else:
        with st.spinner("Writing your ads..."):
            prompt = f"Product: {product}\nTarget audience: {audience}\nKey benefit: {benefit}\n\nWrite 5 ad copy variations."
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                max_tokens=1024,
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ],
            )
            result = response.choices[0].message.content
            st.session_state["last_result"] = result

if "last_result" in st.session_state:
    st.markdown('<hr class="divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-label">Your 5 ad variations</div>', unsafe_allow_html=True)
    st.markdown(st.session_state["last_result"])

# ── Email capture ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="email-box">
    <div class="email-title">Get early access updates</div>
    <div class="email-sub">We're building image generation, saved history, and more. Join the waitlist to be first in line — free forever for early users.</div>
</div>
""", unsafe_allow_html=True)

st.markdown(f'<a href="{WAITLIST_URL}" target="_blank"><button style="background:linear-gradient(135deg,#6366f1,#7c3aed);color:white;font-weight:700;font-size:1rem;padding:0.75rem 2rem;border:none;border-radius:10px;width:100%;cursor:pointer;margin-top:1rem;">Join the Waitlist</button></a>', unsafe_allow_html=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<div class="footer">AdCopy AI — Built for ecom sellers who move fast.</div>', unsafe_allow_html=True)
