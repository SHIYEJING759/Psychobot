
# import streamlit as st
# from database import create_user_table, register_user, login_user

# # 创建用户表（确保表存在）
# create_user_table()

# st.set_page_config(page_title="🔐 Login/Register", layout="centered")
# st.title("🔐 User Login / Register")

# # 初始化 session_state（防止错误）
# if "user_id" not in st.session_state:
#     st.session_state["user_id"] = None
# if "username" not in st.session_state:
#     st.session_state["username"] = ""

# # 页面表单选择
# menu = st.selectbox("Choose your operation", ["Login", "Register"])
# username = st.text_input("Username")
# password = st.text_input("Password", type="password")

# # 登录功能
# if menu == "Login":
#     if st.button("Login"):
#         if username and password:
#             user_id = login_user(username, password)
#             if user_id:
#                 st.session_state["user_id"] = user_id
#                 st.session_state["username"] = username
#                 st.success(f"Welcome back, {username}!")
#                 st.switch_page("pages/chat_interface.py")
#             else:
#                 st.error("❌ Username or password is incorrect.")
#         else:
#             st.warning("Please enter both username and password.")

# # 注册功能
# else:
#     if st.button("Register"):
#         if username and password:
#             success = register_user(username, password)
#             if success:
#                 st.success("✅ Register successfully! Please login.")
#             else:
#                 st.error("⚠️ Fail to register. The username may already exist.")
#         else:
#             st.warning("Please fill in both username and password.")
import streamlit as st
from database import create_user_table, register_user, login_user

# 创建用户表（确保表存在）
create_user_table()

st.set_page_config(page_title="🔐 Login/Register", layout="centered")
st.title("🔐 User Login / Register")

# 初始化 session_state（防止错误）
if "user_id" not in st.session_state:
    st.session_state["user_id"] = None
if "username" not in st.session_state:
    st.session_state["username"] = ""

# 页面表单选择
menu = st.selectbox("Choose your operation", ["Login", "Register"])
username = st.text_input("Username")
password = st.text_input("Password", type="password")

# 登录功能
if menu == "Login":
    if st.button("Login"):
        if username and password:
            user_id = login_user(username, password)
            if user_id:
                # ✅ 登录成功后写入 session_state
                st.session_state["user_id"] = user_id
                st.session_state["username"] = username
                st.success(f"Welcome back, {username}!")

                # ✅ 把 user_id 写入 URL 参数，实现持久化
                st.experimental_set_query_params(user_id=user_id)

                # ✅ 登录成功跳转首页或你想跳转的页面
                st.switch_page("app.py")
            else:
                st.error("❌ Username or password is incorrect.")
        else:
            st.warning("Please enter both username and password.")

# 注册功能
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

