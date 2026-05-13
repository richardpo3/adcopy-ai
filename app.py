import os
import stripe
import streamlit as st
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = st.secrets.get("GROQ_API_KEY", None) if hasattr(st, "secrets") else None
if not api_key:
    api_key = os.getenv("GROQ_API_KEY")

stripe_key = st.secrets.get("STRIPE_SECRET_KEY", None) if hasattr(st, "secrets") else None
if not stripe_key:
    stripe_key = os.getenv("STRIPE_SECRET_KEY")

stripe_price_id = st.secrets.get("STRIPE_PRICE_ID", None) if hasattr(st, "secrets") else None
if not stripe_price_id:
    stripe_price_id = os.getenv("STRIPE_PRICE_ID")

stripe.api_key = stripe_key
client = Groq(api_key=api_key)

FREE_LIMIT = 3
APP_URL = "https://adcopy-ai.streamlit.app"

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

[body copy here — 2-3 punchy sentences that expand on the headline, create desire, and end with a soft call to action]

### 2. Problem → Solution
**Headline:** [headline here]

[body copy here]

### 3. Social Proof
**Headline:** [headline here]

[body copy here]

### 4. Urgency / Scarcity
**Headline:** [headline here]

[body copy here]

### 5. Direct Benefit
**Headline:** [headline here]

[body copy here]

Rules:
- Headlines under 10 words, bold and punchy
- Body is 2-3 sentences, conversational, no corporate speak
- Each variation must feel completely different in tone and angle
- End every body with a soft CTA like "Try it today", "Shop now", or "Get yours"
- Write like a human, not a robot"""

WAITLIST_URL = "https://docs.google.com/forms/d/1Zj8PQTNE3eI_rkjJKqu7gXtFN8kYcx1Whpera81b4PY/viewform"

st.set_page_config(
    page_title="AdCopy AI — Ad Generator for Ecom Sellers",
    page_icon="⚡",
    layout="centered"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
.stApp { background-color: #0a0a0f; }
.block-container { padding: 0 2rem 4rem 2rem; max-width: 1000px; }

/* Nav */
.nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 1.2rem 0;
    margin-bottom: 1rem;
    border-bottom: 1px solid #1a1b26;
}
.nav-logo { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.nav-logo span { color: #6366f1; }
.nav-badge {
    font-size: 0.72rem;
    font-weight: 600;
    color: #818cf8;
    background: rgba(99,102,241,0.12);
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 999px;
    padding: 3px 12px;
}

/* Hero */
.hero {
    text-align: center;
    padding: 4rem 1rem 3rem 1rem;
}
.hero-tag {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    color: #6366f1;
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 999px;
    padding: 4px 14px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 1.5rem;
}
.hero-title {
    font-size: 4rem;
    font-weight: 900;
    color: #f1f5f9;
    line-height: 1.1;
    margin-bottom: 1.2rem;
    letter-spacing: -0.02em;
}
.hero-title span {
    background: linear-gradient(135deg, #6366f1, #a78bfa);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
.hero-sub {
    font-size: 1.2rem;
    color: #64748b;
    line-height: 1.7;
    max-width: 620px;
    margin: 0 auto 2.5rem auto;
}

/* How it works */
.how-section { padding: 3rem 0; }
.how-title {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 2rem;
}
.steps-row {
    display: flex;
    gap: 1rem;
}
.step {
    flex: 1;
    background: #13141e;
    border: 1px solid #1e1f2e;
    border-radius: 14px;
    padding: 1.5rem;
    text-align: center;
}
.step-num {
    width: 36px;
    height: 36px;
    background: rgba(99,102,241,0.15);
    border: 1px solid rgba(99,102,241,0.3);
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 0.85rem;
    font-weight: 700;
    color: #818cf8;
    margin: 0 auto 1rem auto;
}
.step-title { font-size: 0.95rem; font-weight: 700; color: #f1f5f9; margin-bottom: 0.4rem; }
.step-desc { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

/* Pricing */
.pricing-section { padding: 3rem 0; }
.pricing-title {
    text-align: center;
    font-size: 1.6rem;
    font-weight: 800;
    color: #f1f5f9;
    margin-bottom: 2rem;
}
.pricing-row { display: flex; gap: 1rem; }
.plan {
    flex: 1;
    background: #13141e;
    border: 1px solid #1e1f2e;
    border-radius: 14px;
    padding: 1.8rem;
}
.plan.pro {
    border-color: rgba(99,102,241,0.4);
    background: linear-gradient(135deg, rgba(99,102,241,0.06), rgba(124,58,237,0.06));
}
.plan-name { font-size: 0.78rem; font-weight: 700; color: #64748b; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.8rem; }
.plan-price { font-size: 2.2rem; font-weight: 900; color: #f1f5f9; margin-bottom: 0.2rem; }
.plan-price span { font-size: 1rem; font-weight: 500; color: #64748b; }
.plan-desc { font-size: 0.82rem; color: #64748b; margin-bottom: 1.2rem; }
.plan-features { list-style: none; padding: 0; margin: 0; }
.plan-features li { font-size: 0.85rem; color: #94a3b8; padding: 0.3rem 0; }
.plan-features li::before { content: "✓  "; color: #6366f1; font-weight: 700; }

/* Generator page */
.gen-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 1.2rem 0;
    margin-bottom: 2rem;
    border-bottom: 1px solid #1a1b26;
}
.gen-logo { font-size: 1.1rem; font-weight: 800; color: #f1f5f9; }
.gen-logo span { color: #6366f1; }
.gen-counter {
    font-size: 0.8rem;
    color: #64748b;
    background: #13141e;
    border: 1px solid #1e1f2e;
    border-radius: 999px;
    padding: 4px 14px;
}
.gen-counter.pro { color: #818cf8; border-color: rgba(99,102,241,0.3); }

.result-card {
    background: #13141e;
    border: 1px solid #1e1f2e;
    border-radius: 14px;
    padding: 1.8rem;
    margin-top: 2rem;
}

/* Shared */
.divider { border: none; border-top: 1px solid #1a1b26; margin: 1rem 0; }

.stTextInput > label { color: #64748b !important; font-size: 0.82rem !important; font-weight: 600 !important; letter-spacing: 0.04em; text-transform: uppercase; }
.stTextInput > div > div > input {
    background-color: #13141e !important;
    color: #f1f5f9 !important;
    border: 1px solid #1e1f2e !important;
    border-radius: 10px !important;
    padding: 0.75rem 1rem !important;
    font-size: 0.95rem !important;
    font-family: 'Inter', sans-serif !important;
}
.stTextInput > div > div > input:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 3px rgba(99,102,241,0.1) !important;
}
.stTextInput > div > div > input::placeholder { color: #2a2b36 !important; }

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
    transition: opacity 0.2s;
}
.stFormSubmitButton > button:hover, .stButton > button:hover { opacity: 0.88 !important; }

.upgrade-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.08), rgba(124,58,237,0.08));
    border: 1px solid rgba(99,102,241,0.25);
    border-radius: 14px;
    padding: 2rem;
    text-align: center;
    margin: 2rem 0;
}
.upgrade-title { font-size: 1.15rem; font-weight: 800; color: #f1f5f9; margin-bottom: 0.4rem; }
.upgrade-sub { font-size: 0.88rem; color: #64748b; margin-bottom: 1.2rem; }
.upgrade-price { font-size: 2rem; font-weight: 900; color: #6366f1; }

.stAlert { background-color: #13141e !important; border: 1px solid #1e1f2e !important; color: #94a3b8 !important; border-radius: 10px !important; }

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stToolbar"] {display: none;}
[data-testid="stDecoration"] {display: none;}
[data-testid="stStatusWidget"] {display: none;}
.stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "landing"
if "generations_used" not in st.session_state:
    st.session_state["generations_used"] = 0
if "pro" not in st.session_state:
    st.session_state["pro"] = False
if "last_result" not in st.session_state:
    st.session_state["last_result"] = None

# ── Check for Stripe payment return ───────────────────────────────────────────
params = st.query_params
session_id = params.get("session_id")
if session_id and not st.session_state["pro"]:
    try:
        checkout_session = stripe.checkout.Session.retrieve(session_id)
        if checkout_session.payment_status == "paid":
            st.session_state["pro"] = True
            st.session_state["page"] = "generator"
    except Exception:
        pass

def start_checkout():
    try:
        checkout_session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": stripe_price_id, "quantity": 1}],
            mode="subscription",
            success_url=f"{APP_URL}/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=APP_URL,
        )
        st.markdown(f'<meta http-equiv="refresh" content="0; url={checkout_session.url}">', unsafe_allow_html=True)
        st.markdown(f'[Click here if not redirected]({checkout_session.url})')
    except Exception as e:
        st.error(f"Could not start checkout: {e}")


# ════════════════════════════════════════════════════════════════════════════════
# LANDING PAGE
# ════════════════════════════════════════════════════════════════════════════════
if st.session_state["page"] == "landing":

    st.markdown("""
    <div class="nav">
        <div class="nav-logo">AdCopy<span>AI</span></div>
        <div class="nav-badge">Free to try</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="hero">
        <div class="hero-tag">Built for ecom sellers</div>
        <div class="hero-title">Stop writing ads.<br>Start <span>running</span> them.</div>
        <div class="hero-sub">Type your product, audience, and key benefit. Get 5 ready-to-run Facebook and Instagram ad variations in under 15 seconds.</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Generate My Ads — It's Free"):
        st.session_state["page"] = "generator"
        st.rerun()

    st.markdown('<hr class="divider" style="margin: 2rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div class="how-section">
        <div class="how-title">How it works</div>
        <div class="steps-row">
            <div class="step">
                <div class="step-num">1</div>
                <div class="step-title">Describe your product</div>
                <div class="step-desc">Enter your product name, who it's for, and the main benefit it delivers.</div>
            </div>
            <div class="step">
                <div class="step-num">2</div>
                <div class="step-title">AI writes 5 variations</div>
                <div class="step-desc">Get 5 different ad angles — curiosity, social proof, urgency, and more.</div>
            </div>
            <div class="step">
                <div class="step-num">3</div>
                <div class="step-title">Copy and run</div>
                <div class="step-desc">Paste straight into Facebook Ads Manager. No editing needed.</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<hr class="divider" style="margin: 1rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div class="pricing-section">
        <div class="pricing-title">Simple pricing</div>
        <div class="pricing-row">
            <div class="plan">
                <div class="plan-name">Free</div>
                <div class="plan-price">$0</div>
                <div class="plan-desc">Try it out, no signup needed</div>
                <ul class="plan-features">
                    <li>3 ad generations</li>
                    <li>5 angles per generation</li>
                    <li>Facebook + Instagram copy</li>
                </ul>
            </div>
            <div class="plan pro">
                <div class="plan-name">Pro — Most Popular</div>
                <div class="plan-price">$9<span>/month</span></div>
                <div class="plan-desc">For sellers who run ads every week</div>
                <ul class="plan-features">
                    <li>Unlimited generations</li>
                    <li>5 angles per generation</li>
                    <li>Facebook + Instagram copy</li>
                    <li>Cancel anytime</li>
                </ul>
            </div>
            <div class="plan">
                <div class="plan-name">Agency</div>
                <div class="plan-price">$29<span>/month</span></div>
                <div class="plan-desc">For teams and multi-brand sellers</div>
                <ul class="plan-features">
                    <li>Everything in Pro</li>
                    <li>Bulk generation (5 products at once)</li>
                    <li>Copy history — save past ads</li>
                    <li>Up to 5 users</li>
                    <li>Priority support</li>
                </ul>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Get Started Free"):
        st.session_state["page"] = "generator"
        st.rerun()

    st.markdown('<hr class="divider" style="margin: 1rem 0;">', unsafe_allow_html=True)

    st.markdown("""
    <div class="how-section">
        <div class="how-title">Common questions</div>
        <div class="step" style="text-align:left; margin-bottom: 1rem;">
            <div class="step-title">Will this work for my product?</div>
            <div class="step-desc" style="margin-top:0.4rem;">Yes. It works for any physical or digital product. Skincare, kitchen tools, clothing, courses, software — if you can describe it in one sentence, we can write ads for it.</div>
        </div>
        <div class="step" style="text-align:left; margin-bottom: 1rem;">
            <div class="step-title">Is this just ChatGPT?</div>
            <div class="step-desc" style="margin-top:0.4rem;">No. The AI is trained specifically on direct-response ad copy. It writes in 5 proven angles that are tested to convert — not generic marketing fluff. You get copy that sounds human and is ready to run.</div>
        </div>
        <div class="step" style="text-align:left; margin-bottom: 1rem;">
            <div class="step-title">Do I need to edit the ads before using them?</div>
            <div class="step-desc" style="margin-top:0.4rem;">Usually not. Most users copy straight into Ads Manager. You can tweak if you want, but they're written to be ready out of the box.</div>
        </div>
        <div class="step" style="text-align:left; margin-bottom: 1rem;">
            <div class="step-title">Can I cancel my subscription?</div>
            <div class="step-desc" style="margin-top:0.4rem;">Yes, anytime. No contracts, no questions asked. Cancel from your billing portal in one click.</div>
        </div>
        <div class="step" style="text-align:left;">
            <div class="step-title">Why not just use a freelance copywriter?</div>
            <div class="step-desc" style="margin-top:0.4rem;">A good copywriter charges $50-200 per ad. We give you 5 variations in 15 seconds for $9 a month. Use us for first drafts and volume — hire a copywriter when you're scaling a winner.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════════════════
# GENERATOR PAGE
# ════════════════════════════════════════════════════════════════════════════════
elif st.session_state["page"] == "generator":

    gens_used = st.session_state["generations_used"]
    is_pro = st.session_state["pro"]
    remaining = max(0, FREE_LIMIT - gens_used)
    can_generate = is_pro or gens_used < FREE_LIMIT

    if is_pro:
        counter_label = "Pro — unlimited"
        counter_class = "gen-counter pro"
    else:
        counter_label = f"{remaining} free generation{'s' if remaining != 1 else ''} left"
        counter_class = "gen-counter"

    st.markdown(f"""
    <div class="gen-header">
        <div class="gen-logo">AdCopy<span>AI</span></div>
        <div class="{counter_class}">{counter_label}</div>
    </div>
    """, unsafe_allow_html=True)

    if st.button("Back to home"):
        st.session_state["page"] = "landing"
        st.rerun()

    if can_generate:
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
                    if not is_pro:
                        st.session_state["generations_used"] += 1
                    st.rerun()

    else:
        st.markdown("""
        <div class="upgrade-box">
            <div class="upgrade-title">You've used your 3 free generations</div>
            <div class="upgrade-sub">Upgrade to Pro for unlimited ad copy — any product, any time.</div>
            <div class="upgrade-price">$9<span style="font-size:1rem;font-weight:500;color:#64748b">/month</span></div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("Upgrade to Pro"):
            start_checkout()

    if st.session_state["last_result"]:
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(st.session_state["last_result"])
        st.markdown('</div>', unsafe_allow_html=True)

        if not is_pro and gens_used >= FREE_LIMIT:
            st.markdown('<hr class="divider">', unsafe_allow_html=True)
            if st.button("Upgrade to Pro — $9/month"):
                start_checkout()
