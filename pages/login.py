import streamlit as st
from database import create_user_table, register_user, login_user

create_user_table()

st.title("🔐 User Register / Login")

menu = st.selectbox("Choose your operation", ["Login", "Register"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

if menu == "Login":
    if st.button("Login"):
        user_id = login_user(username, password)
        if user_id:
            st.success(f"Welcome to the chatbot，{username}！")
            st.session_state["user_id"] = user_id
            st.session_state["username"] = username
            st.switch_page("pages/chat_interface.py")
        else:
            st.error("Username or password is incorrect")
else:
    if st.button("Register"):
        success = register_user(username, password)
        if success:
            st.success("Register successfully ! Please login.")

        else:
            st.error("Fail to register ! The username may existed.")
