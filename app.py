import streamlit as st
from engine.rules import rule_check
from engine.url_check import url_check
from engine.ai_model import ai_predict

# Page config
st.set_page_config(page_title="PhishGuard", page_icon="🚨")
st.title("🚨 PhishGuard – AI Phishing Detection")

option = st.radio("What do you want to check?", ["Message", "URL"])

# ---------------- MESSAGE CHECK ----------------
if option == "Message":
    msg = st.text_area("Paste the message here")

    if st.button("Check Message"):
        if not msg.strip():
            st.warning("Please enter a message to analyze.")
            st.stop()

        rule_score, found_words = rule_check(msg)
        ai_pred, confidence = ai_predict(msg)
        total = rule_score + ai_pred

        if total >= 2:
            st.error("⚠ PHISHING DETECTED")
        else:
            st.success("✅ MESSAGE IS SAFE")

        st.subheader("📊 Analysis")
        st.write("AI Confidence:", f"{confidence:.2f}%")
        st.write("Rule score:", rule_score)

        if found_words:
            st.write("Suspicious words found:", ", ".join(found_words))
        else:
            st.write("No suspicious keywords found")

# ---------------- URL CHECK ----------------
else:
    url = st.text_input("Paste the URL here")

    if st.button("Check URL"):
        if not url.strip():
            st.warning("Please enter a URL to analyze.")
            st.stop()

        url_score, reasons = url_check(url)

        if url_score >= 2:
            st.error("⚠ PHISHING URL")
        else:
            st.success("✅ URL IS SAFE")

        st.subheader("🔍 URL Analysis")
        st.write("URL risk score:", url_score)

        if reasons:
            st.write("Reasons:")
            for reason in reasons:
                st.write("-", reason)
        else:
            st.write("No suspicious patterns found")
