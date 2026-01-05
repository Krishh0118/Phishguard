import streamlit as st

# ================= ENGINE IMPORTS =================
from engine.rules import rule_check
from engine.url_check import url_check
from engine.ai_model import ai_predict
from engine.risk_engine import calculate_risk
from engine.domain_intel import domain_intel
from engine.link_intel import check_link_intel

# ================= PAGE CONFIG ====================
st.set_page_config(
    page_title="PhishGuard – AI Phishing Detection",
    page_icon="🚨",
    layout="centered"
)

# ================= CUSTOM CSS =====================
st.markdown(
    """
    <style>
    body {
        background: radial-gradient(circle at top, #0f2027, #000000);
        color: #ffffff;
    }

    .main {
        background: transparent;
    }

    h1 {
        text-align: center;
        color: #00f2ff;
        font-weight: 800;
    }

    h2, h3 {
        color: #00d4ff;
    }

    .stButton button {
        background: linear-gradient(135deg, #00f2ff, #0077ff);
        color: black;
        font-weight: bold;
        border-radius: 12px;
        padding: 0.6em 1.2em;
        border: none;
        box-shadow: 0 0 15px rgba(0, 242, 255, 0.6);
    }

    .stButton button:hover {
        background: linear-gradient(135deg, #0077ff, #00f2ff);
        box-shadow: 0 0 25px rgba(0, 242, 255, 0.9);
        transform: scale(1.03);
    }

    .result-box {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(0, 242, 255, 0.3);
        padding: 20px;
        border-radius: 16px;
        margin-top: 20px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ================= HEADER =========================
st.markdown("<h1>🚨 PhishGuard</h1>", unsafe_allow_html=True)
st.markdown(
    "<h3 style='text-align:center;'>AI-Powered Phishing & Scam Detection System</h3>",
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align:center; color:#cfd8dc;'>
    Analyze suspicious <b>messages</b> and <b>URLs</b> using AI models,
    security rules, and cyber-threat intelligence.
    </p>
    """,
    unsafe_allow_html=True
)

st.divider()

# ================= MODE SELECT ====================
option = st.radio(
    "🔍 What do you want to analyze?",
    ["Message", "URL"],
    horizontal=True
)

# =================================================
# ================= MESSAGE ANALYSIS ===============
# =================================================
if option == "Message":

    msg = st.text_area(
        "📩 Paste the message here",
        height=160,
        placeholder="Example: Your account is suspended. Click here to verify..."
    )

    if st.button("🚀 Analyze Message"):

        if not msg.strip():
            st.warning("⚠️ Please enter a message.")
            st.stop()

        rule_score, found_words = rule_check(msg)
        _, confidence = ai_predict(msg)

        risk = calculate_risk(
            rule_score=int(rule_score),
            ai_confidence=float(confidence),
            intel_score=0
        )

        label = risk.get("label", "UNKNOWN RISK")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.markdown("<div class='result-box'>", unsafe_allow_html=True)

        st.subheader(f"⚠️ {label}")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Risk Score:** {score}")
        st.write(f"**AI Confidence:** {confidence:.2f}%")

        if found_words:
            st.subheader("🔎 Suspicious Keywords Detected")
            st.write(", ".join(found_words))

        st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# ================= URL ANALYSIS ===================
# =================================================
else:

    url = st.text_input(
        "🌐 Paste the URL here",
        placeholder="https://example.com/login"
    )

    if st.button("🚀 Analyze URL"):

        if not url.strip():
            st.warning("⚠️ Please enter a URL.")
            st.stop()

        base_score, url_reasons = url_check(url)
        base_score = int(base_score)

        domain_score, domain_reasons = 0, []
        domain_result = domain_intel(url)
        if isinstance(domain_result, tuple):
            domain_score = int(domain_result[0])
            domain_reasons = domain_result[1] or []

        link_score, link_reasons = 0, []
        link_result = check_link_intel(url)
        if isinstance(link_result, tuple):
            link_score = int(link_result[0])
            link_reasons = link_result[1] or []

        intel_score = domain_score + link_score

        risk = calculate_risk(
            rule_score=base_score,
            ai_confidence=0.0,
            intel_score=intel_score
        )

        label = risk.get("label", "UNKNOWN RISK")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.markdown("<div class='result-box'>", unsafe_allow_html=True)

        st.subheader(f"🚨 {label}")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Total Risk Score:** {score}")

        if url_reasons:
            st.subheader("🔍 URL Pattern Findings")
            for r in url_reasons:
                st.write(f"• {r}")

        if domain_reasons:
            st.subheader("🌐 Domain Intelligence")
            for r in domain_reasons:
                st.write(f"• {r}")

        if link_reasons:
            st.subheader("🔗 Link Intelligence")
            for r in link_reasons:
                st.write(f"• {r}")

        st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =========================
st.divider()
st.markdown(
    "<p style='text-align:center; color:#90a4ae;'>© 2026 PhishGuard | Software Engineering Project</p>",
    unsafe_allow_html=True
)
