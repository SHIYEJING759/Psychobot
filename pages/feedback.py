import streamlit as st
import pandas as pd
from datetime import datetime
import os
import io

st.set_page_config(page_title="📋 Feedback", layout="centered")
st.title("💬 MSPSS Feedback Survey")
st.markdown("We'd love to understand how supported you feel after using our chatbot. Please fill out this short questionnaire based on your recent experience.")

# 12 MSPSS items
questions = {
    1: " 1. The chatbot is available when I feel emotionally distressed.",
    2: " 2. I can share my joys and sorrows with the chatbot.",
    3: " 3. The chatbot makes an effort to support me emotionally.",
    4: " 4. I receive the emotional help and support I need from the chatbot.",
    5: " 5. The chatbot is a genuine source of comfort for me.",
    6: " 6. The chatbot actively tries to help me manage my emotions.",
    7: " 7. I can count on the chatbot when things go wrong.",
    8: " 8. I can talk about my problems with the chatbot.",
    9: " 9. The chatbot allows me to share both joyful and painful feelings.",
    10: "10. The chatbot cares about my feelings during our conversation.",
    11: "11. The chatbot supports me in thinking through my emotional challenges.",
    12: "12. I feel comfortable discussing my problems with the chatbot."
}

responses = {}
st.markdown("### 📝 Please rate the following statements (1 = Strongly Disagree, 7 = Strongly Agree)")

for i in range(1, 13):
    st.markdown(f"<div style='font-size:18px; font-weight:500;'>{questions[i]}</div>", unsafe_allow_html=True)
    responses[i] = st.slider("", 1, 7, 4, key=f"q{i}")


if st.button("📨 Submit Feedback"):
   
    question_columns = {f"Question{i}": responses[i] for i in range(1, 13)}
    feedback_df = pd.DataFrame([question_columns])

    # Sum average score and perceived emotional support level
    total_score = sum(responses.values())
    avg_score = total_score / 12
    feedback_df["average_score"] = round(avg_score, 2)

    if avg_score < 3.0:
        level = "Low"
    elif avg_score <= 5.0:
        level = "Moderate"
    else:
        level = "High"
    feedback_df["support_level"] = level

    
    os.makedirs("data", exist_ok=True)
    file_path = "data/mspss_feedback.csv"
    feedback_df.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path))

    # show score and support level
    st.success("Thank you for your feedback! 🎉")
    st.metric("Average MSPSS Score", f"{avg_score:.2f}")
    st.success(f"Your Support Level: **{level}**")

    # build download link
    csv_buffer = io.StringIO()
    feedback_df.to_csv(csv_buffer, index=False)
    st.download_button(
        label="⬇️ Download your feedback as CSV",
        data=csv_buffer.getvalue(),
        file_name="mspss_feedback.csv",
        mime="text/csv"
    )
