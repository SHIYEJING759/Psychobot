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



st.set_page_config(page_title="🔐 Login/Register", layout="centered")
st.title("🔐 User Login / Register")

# initialize session_state
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = ""

# page form choice
menu = st.selectbox("Choose your operation", ["Login", "Register"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# login function
if menu == "Login":
    if st.button("Login"):
        if username and password:
            user_id = login_user(username, password)
            if user_id:
                # Write session_state after successful login
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
                st.success(f"Welcome back, {username}!")

                #  Write user_id into URL parameters to achieve persistence
                st.query_params = {"user_id": user_id}

                # After successful login, you will be redirected to the homepage or the page you want to jump to.
                st.switch_page("app.py")
            else:
                st.error("❌ Username or password is incorrect.")
        else:
            st.warning("Please enter both username and password.")

# register function
else:
    if st.button("Register"):
        if username and password:
            success = register_user(username, password)
            if success:
                st.success("✅ Register successfully! Please login.")
            else:
                st.error("⚠️ Fail to register. The username may already exist.")
        else:
            st.warning("Please fill in both username and password.")

