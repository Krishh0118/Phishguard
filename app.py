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

        # Rule-based analysis
        rule_score, found_words = rule_check(msg)

        # AI-based analysis
        ai_pred, confidence = ai_predict(msg)

        # Final decision logic (HYBRID)
        total = rule_score + ai_pred

        if total >= 2 or confidence >= 70:
            st.error("⚠ PHISHING DETECTED")
        else:
            st.success("✅ MESSAGE IS SAFE")

        # -------- Explanation Section --------
        st.subheader("📊 Analysis Details")

        st.write("**Decision Logic:**")
        st.write(f"- Rule Score: {rule_score}")
        st.write(f"- AI Confidence: {confidence:.2f}%")

        if found_words:
            st.write("**Suspicious words found:**", ", ".join(found_words))
        else:
            st.write("**Suspicious words found:** None")

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
        st.write("URL Risk Score:", url_score)

        if reasons:
            st.write("**Reasons:**")
            for reason in reasons:
                st.write("-", reason)
        else:
            st.write("No suspicious patterns found")
