import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib
from database import  get_recent_messages, detect_emotion, detect_event
from openai import OpenAI
import os
from dotenv import load_dotenv

user_id = st.session_state.get("user_id", None)
if user_id is None:
    st.warning("⚠️ 请先登录后查看情绪记录")
    st.stop()

# 初始化
matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

# 加载 OpenAI API key
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(page_title="My Emotional Record", layout="centered")
st.title("📘 My Emotional Forecast & Trend Record")
st.markdown("Analyze emotional trends based on your chat history, and receive GPT-generated forecasts & suggestions.")

st.markdown("---")
st.subheader("📈 Emotion Fluctuation Over Time")

# 获取聊天记录
data = get_recent_messages(user_id, limit=100)
data = pd.DataFrame(data, columns=["role", "message", "timestamp"])

if not data.empty:
    user_data = data[data["role"] == "user"].copy()
    user_data["date"] = pd.to_datetime(user_data["timestamp"]).dt.date
    user_data["emotion"] = user_data["message"].apply(detect_emotion)
    user_data["event"] = user_data["message"].apply(detect_event)

    # 生成主导情绪得分趋势
    trend_df = user_data.groupby("date")["emotion"].apply(lambda x: x.value_counts().idxmax()).reset_index()
    trend_df.columns = ["date", "main_emotion"]

    emotion_map = {"😊 开心": 3, "😐 平静": 2, "😣 难过": 1, "🥶 焦虑": 0, "😡 生气": -1}
    trend_df["emotion_score"] = trend_df["main_emotion"].map(emotion_map)

    # 折线图可视化
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.plot(trend_df["date"], trend_df["emotion_score"], marker='o')
    ax.set_title("Daily Dominant Emotion Trend")
    ax.set_ylabel("Emotion Score")
    ax.set_xlabel("Date")
    ax.set_xticks(trend_df["date"])
    ax.set_xticklabels(trend_df["date"], rotation=45)
    st.pyplot(fig)

    # 显示情绪数据表格
    st.subheader("📊 Past 14-Day Emotion Summary")
    st.dataframe(trend_df[["date", "main_emotion"]])

    # GPT情绪预测与建议
    st.subheader("🔮 Chat history Based Emotion Forecast")

    history_text = "\n".join([f"{row['date']}：{row['main_emotion']}" for _, row in trend_df.iterrows()])

    prompt = f"""
    You are an AI emotional support expert. Below is the user's dominant emotion trend over the past 14 days:
    {history_text}

    Based on this history, please forecast the user's emotional state for the next 7 days and provide specific mental health advice to support them.

    Please respond in the following format:
    [Emotion Forecast]:
    [Advice]:
    """

    with st.spinner("🧠 Chatbot is analyzing..."):
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.6,
                max_tokens=1000,
            )
            forecast = response.choices[0].message.content.strip()
            st.markdown(f"📌 Result of the analysis：\n\n{forecast}")
        except Exception as e:
            st.error(f"❗ 无法获取 GPT 预测：{e}")

else:
    st.info("暂无聊天记录，无法分析情绪趋势。")
