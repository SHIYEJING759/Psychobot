# import streamlit as st
# from database import get_recent_messages

# st.set_page_config(page_title="📜 Chat History", layout="centered")
# st.title("🕘 Past Chat Records")
# st.markdown("This page shows your recent conversation history.")

# # ✅ 获取当前用户 ID
# user_id = st.session_state.get("user_id", None)
# if user_id is None:
#     st.warning("⚠️ 请先登录以查看聊天记录。")
#     st.stop()

# # ✅ 获取当前用户的聊天记录
# messages = get_recent_messages(user_id=user_id, limit=50)

# if messages:
#     for role, message, timestamp in reversed(messages):
#         with st.chat_message("user" if role == "user" else "ai"):
#             st.markdown(f"**{timestamp}**  \n{message}")
# else:
#     st.info("No chat records found.")
import streamlit as st
from database import get_recent_messages

st.set_page_config(page_title="📜 Chat History", layout="centered")
st.title("🕘 Past Chat Records")
st.markdown("This page shows your recent conversation history.")

# ✅ 获取当前用户 ID
user_id = st.session_state.get("user_id", None)
if user_id is None:
    st.warning("⚠️ 请先登录以查看聊天记录。")
    st.stop()

# ✅ 获取当前用户的聊天记录
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
