import streamlit as st
from database import get_recent_messages

st.set_page_config(page_title="📜 Chat History", layout="centered")
st.title("🕘 Past Chat Records")
st.markdown("This page shows your recent conversation history.")

# 获取并展示聊天记录
messages = get_recent_messages(limit=50)

if messages:
    for role, message, timestamp in reversed(messages):
        with st.chat_message("user" if role == "user" else "ai"):
            st.markdown(f"**{timestamp}**  \n{message}")
else:
    st.info("No chat records found.")
