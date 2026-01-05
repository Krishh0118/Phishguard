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
    page_title="PhishGuard",
    page_icon="🚨",
    layout="centered"
)

# ================= CUSTOM UI STYLING ==============
st.markdown("""
<style>
body {
    background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
}
.main {
    background-color: transparent;
}
h1, h2, h3, h4, h5, h6 {
    color: #ffffff;
}
p, label, span {
    color: #cfd8dc;
}
.card {
    background: rgba(255,255,255,0.06);
    padding: 25px;
    border-radius: 16px;
    box-shadow: 0 0 25px rgba(0,0,0,0.4);
    margin-top: 20px;
}
.safe {
    background: #1b5e20;
    padding: 14px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}
.warning {
    background: #f9a825;
    padding: 14px;
    border-radius: 10px;
    color: black;
    font-weight: bold;
}
.danger {
    background: #b71c1c;
    padding: 14px;
    border-radius: 10px;
    color: white;
    font-weight: bold;
}
footer {
    visibility: hidden;
}
</style>
""", unsafe_allow_html=True)

# ================= HEADER =========================
st.markdown("<h1 style='text-align:center;'>🚨 PhishGuard</h1>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; font-size:18px;'>"
    "AI-Powered Cyber Safety Assistant for Phishing Detection"
    "</p>",
    unsafe_allow_html=True
)

# ================= MODE SELECT ====================
st.markdown("<div class='card'>", unsafe_allow_html=True)
option = st.radio("🔍 What do you want to check?", ["Message", "URL"])
st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# ================= MESSAGE ANALYSIS ===============
# =================================================
if option == "Message":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    msg = st.text_area("📩 Paste the message here")
    analyze_msg = st.button("🧠 Analyze Message")
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_msg:

        if not msg.strip():
            st.warning("Please enter a message.")
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

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if score < 30:
            st.markdown("<div class='safe'>✅ SAFE MESSAGE</div>", unsafe_allow_html=True)
        elif score < 60:
            st.markdown("<div class='warning'>⚠️ SUSPICIOUS MESSAGE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='danger'>🚨 HIGH RISK MESSAGE</div>", unsafe_allow_html=True)

        st.subheader("📊 Analysis Summary")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Risk Score:** {score}")
        st.write(f"**AI Confidence:** {confidence:.2f}%")

        if found_words:
            st.subheader("🔎 Suspicious Keywords")
            st.write(", ".join(found_words))

        st.markdown("</div>", unsafe_allow_html=True)

# =================================================
# ================= URL ANALYSIS ===================
# =================================================
else:

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    url = st.text_input("🌐 Paste the URL here")
    analyze_url = st.button("🔎 Analyze URL")
    st.markdown("</div>", unsafe_allow_html=True)

    if analyze_url:

        if not url.strip():
            st.warning("Please enter a URL.")
            st.stop()

        base_score, url_reasons = url_check(url)
        base_score = int(base_score)

        domain_score = 0
        domain_reasons = []
        domain_result = domain_intel(url)

        if isinstance(domain_result, tuple):
            domain_score = int(domain_result[0])
            domain_reasons = domain_result[1] or []

        link_score = 0
        link_reasons = []
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

        st.markdown("<div class='card'>", unsafe_allow_html=True)

        if score < 30:
            st.markdown("<div class='safe'>✅ SAFE WEBSITE</div>", unsafe_allow_html=True)
        elif score < 60:
            st.markdown("<div class='warning'>⚠️ SUSPICIOUS WEBSITE</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div class='danger'>🚨 HIGH RISK – POSSIBLE PHISHING</div>", unsafe_allow_html=True)

        st.subheader("🔐 Risk Assessment")
        st.write(f"**Risk Level:** {level}")
        st.write(f"**Total Risk Score:** {score}")

        if url_reasons:
            st.subheader("🔍 URL Pattern Findings")
            for r in url_reasons:
                st.write(f"- {r}")

        if domain_reasons:
            st.subheader("🌐 Domain Intelligence")
            for r in domain_reasons:
                st.write(f"- {r}")

        if link_reasons:
            st.subheader("🔗 Link Intelligence")
            for r in link_reasons:
                st.write(f"- {r}")

        st.markdown("</div>", unsafe_allow_html=True)

# ================= FOOTER =========================
st.markdown(
    "<p style='text-align:center; color:#90a4ae; margin-top:30px;'>"
    "Software Engineering Project • Incremental Development Model • PhishGuard"
    "</p>",
    unsafe_allow_html=True
)
