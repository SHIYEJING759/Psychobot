import streamlit as st
import sys
import os
import pandas as pd
from datetime import datetime
from database import get_recent_messages  
import html

from database import(
    register_user,
    login_user,
    save_message,
    get_recent_messages,
    save_emotion_log,
    get_chat_emotion_logs,
    detect_event,
    detect_emotion
)

# import chat_engine from parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from chat_engine import get_ai_response

# Basic page settings
st.set_page_config(page_title="AI Emotional support chatbot", layout="centered")

#  check login state
if "user_id" not in st.session_state:
    st.warning("⚠️ Please login first then use the function")
    st.stop()

user_id = st.session_state["user_id"]
username = st.session_state.get("username", "你")


st.title("💬 AI Emotional support chatbot")
st.markdown("Welcome to AI Emotional support chatbot! I'm here to talk with you! 🌱")

# intialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Inject CSS style
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

# chat space
st.markdown('<div class="chat-container">', unsafe_allow_html=True)

for role, content in st.session_state.messages:
    
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
        save_message("user", user_input, st.session_state["user_id"])

        with st.spinner("AI is thinking..."):
            ai_reply = get_ai_response(user_input)

        st.session_state.messages.append(("ai", ai_reply))
        save_message("ai", ai_reply, st.session_state["user_id"])

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
                label="📄 Download CSV File of chat history",
                data=f,
                file_name=filename,
                mime="text/csv"
            )
    else:
        st.info("No chat history can be export")
