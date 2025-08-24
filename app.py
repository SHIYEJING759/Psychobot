# import streamlit as st
# from database import init_db
# init_db()
#
#
# st.set_page_config(
#     page_title="AI心理支持机器人",
#     layout="centered",
#     page_icon="🧠"
# )
#
# # 设置标题与欢迎语
# st.title("💬 Welcome to the AI Emotional Support Space")
# st.markdown("👋 **Hello！**\n\nI am your AI chat partner, ready to listen to what you want to say at any time, and I can also help you record your emotions and organize your thoughts.")
#
# st.divider()
#
# # 主功能入口
# st.subheader("📌 Function Navigation")
#
# st.page_link("pages/chat_interface.py", label="🗣️ Start chat", icon="💬")
# st.page_link("pages/my_emotional_record.py", label="📈 Check my emotional record", icon="📊")
# st.page_link("pages/feedback.py", label="📝 Submit the survey questionnaire", icon="🧾")
#
# st.divider()
#
# # 温馨提示
# st.markdown(
#     """
#     <style>
#     #custom-footer {
#         position: fixed;
#         bottom: 0;
#         left: 0;
#         width: 100%;
#         background-color: white;
#         text-align: center;
#         padding: 8px;
#         font-size: 0.9em;
#         color: gray;
#         z-index: 9999;
#     }
#     </style>
#     <div id="custom-footer">
#         💡 All the information will be stroed locally ,your privacy will be respected.
#     </div>
#     """,
#     unsafe_allow_html=True
# )
import streamlit as st
from database import init_db

# 初始化数据库
init_db()

# 页面基本配置
st.set_page_config(
    page_title="AI心理支持机器人",
    layout="centered",
    page_icon="🧠"
)
# 👉 从 URL 参数中恢复登录状态 保存用户的账户信息
# params = st.experimental_get_query_params()
# if "user_id" in params and "user_id" not in st.session_state:
#     st.session_state["user_id"] = int(params["user_id"][0])
params = st.query_params
if "user_id" in params and "user_id" not in st.session_state:
    st.session_state["user_id"] = int(params["user_id"][0])


# 标题与欢迎语
st.title("💬 Welcome to the AI Emotional Support Space")
st.markdown("👋 **Hello！**\n\nI am your AI chat partner, ready to listen to what you want to say at any time, and I can also help you record your emotions and organize your thoughts.")
st.divider()

# 📌 主功能导航（带权限判断跳转）
st.subheader("📌 Function Navigation")

# 判断是否登录
is_logged_in = "user_id" in st.session_state

# 🗣️ 聊天功能跳转：需要登录
if st.button("🗣️ Start chat 💬"):
    if is_logged_in:
        st.switch_page("pages/chat_interface.py")
    else:
        st.warning("⚠️ Please login first.")
        st.switch_page("pages/login.py")

# 📈 情绪记录
if st.button("📈 Check my emotional record"):
    st.switch_page("pages/my_emotional_record.py")

# 📝 问卷反馈
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



