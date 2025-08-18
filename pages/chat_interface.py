import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime
from database import get_recent_messages  # 这个函数你之前已经写在 database.py 里了
import html

from database import create_chat_table, save_message

# 引入上级目录中的 chat_engine
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chat_engine import get_ai_response

# 页面基本设置
st.set_page_config(page_title="AI Emotional support chatbot", layout="centered")

# 🔐 登录检查
if "user_id" not in st.session_state:
    st.warning("⚠️ 请先登录后使用本功能。")
    st.stop()

user_id = st.session_state["user_id"]
username = st.session_state.get("username", "你")

#初始化聊天表
create_chat_table()

st.title("💬 AI Emotional support chatbot")
st.markdown("Welcome to AI Emotional support chatbot! I'm here to talk with you! 🌱")

# 初始化对话历史
if "messages" not in st.session_state:
    st.session_state.messages = []

# 注入 CSS 样式（气泡 + 头像 + 固定聊天区域）
st.markdown("""
<style>
.chat-container {
    max-height: 70vh;
    overflow-y: auto;
    padding: 10px;
    margin-bottom: 10px;
    border-radius: 12px;
    background-color: #ffffff;
}
.message-row {
    display: flex;
    margin-bottom: 10px;
    align-items: flex-start;
}
.message-content {
    max-width: 70%;
    padding: 12px 16px;
    border-radius: 18px;
    font-size: 16px;
    line-height: 1.6;
    white-space: pre-wrap;
    overflow-wrap: break-word;
}
.user-row {
    flex-direction: row-reverse;
}
.user-message {
    background-color: #DCF8C6;
    margin-right: 8px;
}
.ai-message {
    background-color: #F1F0F0;
    margin-left: 8px;
}
.avatar {
    width: 36px;
    height: 36px;
    border-radius: 50%;
    background-color: #888;
    color: white;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# 聊天展示区域
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, content in st.session_state.messages:
    # 转义 HTML 特殊字符，并保留换行格式
    safe_content = html.escape(content).replace("\n", "<br>")

    if role == "user":
        st.markdown(f"""
        <div class="message-row user-row">
            <div class="avatar">你</div>
            <div class="message-content user-message">{safe_content}</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown(f"""
        <div class="message-row">
            <div class="avatar">AI</div>
            <div class="message-content ai-message">{safe_content}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)

with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("Say something:", key="input_field", label_visibility="collapsed")
    submitted = st.form_submit_button("Send")
    if submitted and user_input:
        st.session_state.messages.append(("user", user_input))
        save_message("user", user_input)

        with st.spinner("AI is thinking..."):
            ai_reply = get_ai_response(user_input)

        st.session_state.messages.append(("ai", ai_reply))
        save_message("ai", ai_reply)

        st.rerun()

st.markdown("---")

if st.button("📥 Export chat history as CSV"):
    messages = get_recent_messages(limit=1000)
    if messages:
        df = pd.DataFrame(messages, columns=["Role", "Message", "Timestamp"])
        filename = f"chat_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        df.to_csv(filename, index=False)
        with open(filename, "rb") as f:
            st.download_button(
                label="📄 点击下载 CSV 文件",
                data=f,
                file_name=filename,
                mime="text/csv"
            )
    else:
        st.info("暂无聊天记录可导出。")
