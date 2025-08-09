import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="📋 Feedback", layout="centered")
st.title("💬 MSPSS Feedback Survey")
st.markdown("We'd love to understand how supported you feel after using our chatbot. Please fill out this short questionnaire based on your recent experience.")

# 12 MSPSS items
questions = {
    1: " 1. There is a special person who is around when I am in need.",
    2: " 2. There is a special person with whom I can share my joys and sorrows.",
    3: " 3. My family really tries to help me.",
    4: " 4. I get the emotional help and support I need from my family.",
    5: " 5. I have a special person who is a real source of comfort to me.",
    6: " 6. My friends really try to help me.",
    7: " 7. I can count on my friends when things go wrong.",
    8: " 8. I can talk about my problems with my family.",
    9: " 9. I have friends with whom I can share my joys and sorrows.",
    10: "10. There is a special person in my life who cares about my feelings.",
    11: "11. My family is willing to help me make decisions.",
    12: "12. I can talk about my problems with my friends."
}

responses = {}
st.markdown("### 📝 Please rate the following statements (1 = Strongly Disagree, 7 = Strongly Agree)")

for i in range(1, 13):
    st.markdown(f"<div style='font-size:18px; font-weight:500;'>{questions[i]}</div>", unsafe_allow_html=True)
    responses[i] = st.slider("", 1, 7, 4, key=f"q{i}")

if st.button("📨 Submit Feedback"):
    feedback_df = pd.DataFrame([responses])
    feedback_df["timestamp"] = datetime.now()
    # 保存为 CSV（可扩展为写入数据库）
    feedback_df.to_csv("data/mspss_feedback.csv", mode="a", index=False, header=not os.path.exists("data/mspss_feedback.csv"))
    st.success("Thank you for your feedback! 🎉")

    # 可视化平均得分
    st.markdown("### 📊 Your Feedback Summary")
    family = [responses[i] for i in [3, 4, 8, 11]]
    friends = [responses[i] for i in [6, 7, 9, 12]]
    significant = [responses[i] for i in [1, 2, 5, 10]]

    summary = pd.DataFrame({
        "Family Support": [sum(family) / 4],
        "Friend Support": [sum(friends) / 4],
        "Significant Other Support": [sum(significant) / 4]
    })

    st.bar_chart(summary.T)

