import streamlit as st
from database import (
    register_user,
    login_user,
    save_message,
    get_recent_messages,
    save_emotion_log,
    get_chat_emotion_logs,
    detect_event,
    detect_emotion
)


# Page basic settings
st.set_page_config(
    page_title="AI心理支持机器人",
    layout="centered",
    page_icon="🧠"
)
# Restore the login state from URL parameters Save the user's account information
# params = st.experimental_get_query_params()
# if "user_id" in params and "user_id" not in st.session_state:
#     st.session_state["user_id"] = int(params["user_id"][0])
params = st.query_params
if "user_id" in params and "user_id" not in st.session_state:
    st.session_state["user_id"] = int(params["user_id"][0])


# Title and welcome message
st.title("💬 Welcome to the AI Emotional Support Space")
st.markdown("👋 **Hello！**\n\nI am your AI chat partner, ready to listen to what you want to say at any time, and I can also help you record your emotions and organize your thoughts.")
st.divider()

#  Main function navigation (with permission judgment jump)
st.subheader("📌 Function Navigation")

# Check the login state
is_logged_in = "user_id" in st.session_state

# Chat function jump: need to log in
if st.button("🗣️ Start chat 💬"):
    if is_logged_in:
        st.switch_page("pages/chat_interface.py")
    else:
        st.warning("⚠️ Please login first.")
        st.switch_page("pages/login.py")

# Emotional record
if st.button("📈 Check my emotional record"):
    st.switch_page("pages/my_emotional_record.py")

# MSPSS questionnaire feedback
if st.button("📝 Submit the survey questionnaire"):
    st.switch_page("pages/feedback.py")

# Footer
st.divider()
st.markdown(
    """
    <style>
    #custom-footer {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        background-color: white;
        text-align: center;
        padding: 8px;
        font-size: 0.9em;
        color: gray;
        z-index: 9999;
    }
    </style>
    <div id="custom-footer">
        💡 All the information will be stored locally, your privacy will be respected.
    </div>
    """,
    unsafe_allow_html=True
)



