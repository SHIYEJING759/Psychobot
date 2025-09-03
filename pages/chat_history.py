import streamlit as st
from database import get_recent_messages

st.set_page_config(page_title="📜 Chat History", layout="centered")
st.title("🕘 Past Chat Records")
st.markdown("This page shows your recent conversation history.")

# obtain present user ID
user_id = st.session_state.get("user_id", None)
if user_id is None:
    st.warning("⚠️ Please login to check the chat history.")
    st.stop()

# obtain present user chat history
messages = get_recent_messages(user_id=user_id, limit=50)

if messages:
    for msg in reversed(messages):
        role = msg["role"]
        message = msg["message"]
        timestamp = msg["timestamp"]

        with st.chat_message("user" if role == "user" else "ai"):
            st.markdown(f"**{timestamp}**  \n{message}")
else:
    st.info("No chat records found.")
