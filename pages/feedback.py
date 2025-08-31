# import streamlit as st
# import pandas as pd
# from datetime import datetime
# import os

# st.set_page_config(page_title="📋 Feedback", layout="centered")
# st.title("💬 MSPSS Feedback Survey")
# st.markdown("We'd love to understand how supported you feel after using our chatbot. Please fill out this short questionnaire based on your recent experience.")

# # 12 MSPSS items
# questions = {
#     1: " 1.The chatbot is available when I feel emotionally distressed.",
#     2: " 2.I can share my joys and sorrows with the chatbot.",
#     3: " 3.The chatbot makes an effort to support me emotionally.",
#     4: " 4.I receive the emotional help and support I need from the chatbot.",
#     5: " 5.The chatbot is a genuine source of comfort for me.",
#     6: " 6.The chatbot actively tries to help me manage my emotions.",
#     7: " 7.I can count on the chatbot when things go wrong.",
#     8: " 8.I can talk about my problems with the chatbot.",
#     9: " 9.The chatbot allows me to share both joyful and painful feelings.",
#     10: "10.The chatbot care about my feelings during our conversation.",
#     11: "11.The chatbot supports me in thinking through my emotional challenges.",
#     12: "12.I feel comfortable discussing my problems with the chatbot."
# }

# responses = {}
# st.markdown("### 📝 Please rate the following statements (1 = Strongly Disagree, 7 = Strongly Agree)")

# for i in range(1, 13):
#     st.markdown(f"<div style='font-size:18px; font-weight:500;'>{questions[i]}</div>", unsafe_allow_html=True)
#     responses[i] = st.slider("", 1, 7, 4, key=f"q{i}")

# if st.button("📨 Submit Feedback"):
#     feedback_df = pd.DataFrame([responses])
#     feedback_df["timestamp"] = datetime.now()
#     # 保存为 CSV（可扩展为写入数据库）
#     feedback_df.to_csv("data/mspss_feedback.csv", mode="a", index=False, header=not os.path.exists("data/mspss_feedback.csv"))
#     st.success("Thank you for your feedback! 🎉")

#     # 可视化平均得分
#     st.markdown("### 📊 Your Feedback Summary")
#     family = [responses[i] for i in [3, 4, 8, 11]]
#     friends = [responses[i] for i in [6, 7, 9, 12]]
#     significant = [responses[i] for i in [1, 2, 5, 10]]

#     summary = pd.DataFrame({
#         "Family Support": [sum(family) / 4],
#         "Friend Support": [sum(friends) / 4],
#         "Significant Other Support": [sum(significant) / 4]
#     })

#     st.bar_chart(summary.T)
# The chatbot is available when I feel emotionally distressed.
# I can share my joys and sorrows with the chatbot.
# The chatbot makes an effort to support me emotionally.
# I receive the emotional help and support I need from the chatbot
# The chatbot is a genuine source of comfort for me.
# The chatbot actively tries to help me manage my emotions.
# I can count on the chatbot when I encounter emotional difficulties.
# I can talk about my problems with the chatbot.

# The chatbot allows me to share both joyful and painful feelings.
# The chatbot care about my feelings during our conversation
# The chatbot supports me in thinking through my emotional challenges.
# I feel comfortable discussing my problems with the chatbot
import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
    # ✅ 将 responses 转为 DataFrame
    feedback_df = pd.DataFrame([responses])

    # ✅ 添加时间戳
    feedback_df["timestamp"] = datetime.now()

    # ✅ 计算平均得分
    total_score = sum(responses.values())
    avg_score = total_score / 12
    feedback_df["average_score"] = round(avg_score, 2)

    # ✅ 判断支持水平
    if avg_score < 3.0:
        level = "Low"
    elif avg_score <= 5.0:
        level = "Moderate"
    else:
        level = "High"
    feedback_df["support_level"] = level

    # ✅ 创建 data 文件夹
    os.makedirs("data", exist_ok=True)

    # ✅ 保存 CSV 文件
    file_path = "data/mspss_feedback.csv"
    feedback_df.to_csv(file_path, mode="a", index=False, header=not os.path.exists(file_path))

    # ✅ 用户反馈显示
    st.success("Thank you for your feedback! 🎉")
    st.markdown("### 🧠 Overall Support Evaluation")
    st.metric("Average MSPSS Score", f"{avg_score:.2f}")
    st.success(f"Your Support Level: **{level}**")

