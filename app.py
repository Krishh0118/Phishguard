import streamlit as st

# ================= ENGINE IMPORTS =================
from main.engine.rules import rule_check
from main.engine.url_check import url_check
from main.engine.ai_model import ai_predict
from main.engine.risk_engine import calculate_risk
from main.engine.domain_intel import domain_intel
from main.engine.link_intel import check_link_intel



# ================= PAGE CONFIG ====================
st.set_page_config(
    page_title="PhishGuard",
    page_icon="🚨",
    layout="centered"
)

# ================= CUSTOM CSS =====================
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background-color: transparent;
}
.card {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0px 0px 25px rgba(0,0,0,0.3);
    margin-top: 20px;
}
.title {
    text-align: center;
    font-size: 42px;
    font-weight: bold;
    color: #ffffff;
}
.subtitle {
    text-align: center;
    color: #cfd8dc;
    font-size: 16px;
    margin-bottom: 30px;
}
.result-box {
    background: rgba(0,0,0,0.5);
    padding: 20px;
    border-radius: 12px;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =========================
st.markdown("<div class='title'>🚨 PhishGuard</div>", unsafe_allow_html=True)
st.markdown(
    "<div class='subtitle'>AI-Powered Phishing & Scam Detection System</div>",
    unsafe_allow_html=True
)

# ================= MODE SELECT ====================
option = st.radio(
    "🔍 What do you want to analyze?",
    ["Message", "URL"],
    horizontal=True
)

st.markdown("<div class='card'>", unsafe_allow_html=True)

# =================================================
# ================= MESSAGE ANALYSIS ===============
# =================================================
if option == "Message":

    msg = st.text_area("📩 Paste the suspicious message here")

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

        label = risk.get("label", "UNKNOWN")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.error(f"⚠️ {label}")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Risk Score:** {score}")
        st.write(f"**AI Confidence:** {confidence:.2f}%")

        if found_words:
            st.write("🔎 **Suspicious Keywords Detected:**")
            st.write(", ".join(found_words))

        st.markdown("</div>", unsafe_allow_html=True)


# =================================================
# ================= URL ANALYSIS ===================
# =================================================
else:

    url = st.text_input("🌐 Paste the URL here")

    if st.button("🚀 Analyze URL"):

        if not url.strip():
            st.warning("⚠️ Please enter a URL.")
            st.stop()

        base_score, url_reasons = url_check(url)
        domain_score, domain_reasons = domain_intel(url)
        link_score, link_reasons = check_link_intel(url)

        intel_score = int(domain_score) + int(link_score)

        risk = calculate_risk(
            rule_score=int(base_score),
            ai_confidence=0.0,
            intel_score=intel_score
        )

        label = risk.get("label", "UNKNOWN")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.markdown("<div class='result-box'>", unsafe_allow_html=True)
        st.error(f"⚠️ {label}")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Total Risk Score:** {score}")

        if url_reasons:
            st.write("🔍 **URL Pattern Findings:**")
            for r in url_reasons:
                st.write(f"- {r}")

        if domain_reasons:
            st.write("🌐 **Domain Intelligence:**")
            for r in domain_reasons:
                st.write(f"- {r}")

        if link_reasons:
            st.write("🔗 **Link Intelligence:**")
            for r in link_reasons:
                st.write(f"- {r}")

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)
