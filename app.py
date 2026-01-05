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

st.title("🚨 PhishGuard – AI Cyber Safety Assistant")
st.write(
    "PhishGuard analyzes messages and URLs using **AI + security intelligence** "
    "to detect phishing and online scams."
)

# ================= MODE SELECT ====================
option = st.radio("What do you want to check?", ["Message", "URL"])


# =================================================
# ================= MESSAGE ANALYSIS ===============
# =================================================
if option == "Message":

    msg = st.text_area("Paste the message here")

    if st.button("Analyze Message"):

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

        # ---- SAFE EXTRACTION ----
        label = risk.get("label", "UNKNOWN RISK")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.warning(f"⚠️ {label}")
        st.subheader("📊 Analysis")

        st.write(f"**Risk Level:** {level}")
        st.write(f"**Risk Score:** {score}")
        st.write(f"**AI Confidence:** {confidence:.2f}%")

        if found_words:
            st.subheader("🔎 Suspicious Keywords Found")
            st.write(", ".join(found_words))


# =================================================
# ================= URL ANALYSIS ===================
# =================================================
else:

    url = st.text_input("Paste the URL here")

    if st.button("Analyze URL"):

        if not url.strip():
            st.warning("Please enter a URL.")
            st.stop()

        # ---------- URL RULES ----------
        base_score, url_reasons = url_check(url)
        base_score = int(base_score)

        # ---------- DOMAIN INTEL ----------
        domain_score = 0
        domain_reasons = []
        domain_result = domain_intel(url)

        if isinstance(domain_result, tuple):
            domain_score = int(domain_result[0])
            domain_reasons = domain_result[1] or []

        # ---------- LINK INTEL ----------
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

        # ---- SAFE EXTRACTION ----
        label = risk.get("label", "UNKNOWN RISK")
        score = risk.get("score", 0)
        level = risk.get("level", label)

        st.warning(f"⚠️ {label}")
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
