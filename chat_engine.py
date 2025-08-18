# # chat_engine.py
# # import os
# # from dotenv import load_dotenv
# # from openai import OpenAI
# # import streamlit as st

# # openai.api_key = st.secrets["OPENAI_API_KEY"]

# # # 加载 .env 文件中的 API 密钥
# # load_dotenv()
# # api_key = os.getenv("OPENAI_API_KEY")

# # # 初始化 OpenAI 客户端
# # client = OpenAI(api_key=api_key)

# def get_ai_response(user_input):
#     """
#     调用 OpenAI Chat Completions API 获取 AI 回复
#     """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-4o",  # 可替换为 "gpt-4" 或 "gpt-4o"
#             messages=[
#                 {"role": "system", "content": "你是一位温暖、理解人的心理支持型AI机器人，善于倾听和安慰用户,在共情用户时你最好不要显得很假，要有真实的温度和情感。"},
#                 {"role": "user", "content": user_input}
#             ],
#             temperature=0.7,
#             max_tokens=1000,
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"❗错误：{e}"

# # 测试函数（可选）
# def test_api():
#     test_input = "你好，我感觉最近有点焦虑。"
#     return get_ai_response(test_input)

# if __name__ == "__main__":
#     print("测试结果：", test_api())
# chat_engine.py
from openai import OpenAI
import streamlit as st

# ---- 只用 st.secrets 读取 Key，避免被其他方式覆盖 ----
def _build_client() -> OpenAI:
    api_key = st.secrets["OPENAI_API_KEY"].strip()  # 防止隐藏空格/换行
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is empty. Please set it in Streamlit Cloud → Secrets.")
    return OpenAI(api_key=api_key)

_client = None
def client() -> OpenAI:
    global _client
    if _client is None:
        _client = _build_client()
    return _client

SYSTEM_PROMPT = (
    "你是一位温暖、理解人的心理支持型AI，善于倾听和安慰用户；"
    "避免医疗诊断；语言自然真诚，有温度。"
)

def get_ai_response(user_input: str) -> str:
    """
    调用 OpenAI Chat Completions API 获取 AI 回复（新 SDK）
    """
    try:
        resp = client().chat.completions.create(
            # 建议先用 gpt-4o-mini 或 gpt-3.5-turbo（更通用、更省钱）；若你账号有 4o 权限可换成 "gpt-4o"
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_input},
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return resp.choices[0].message.content.strip()
    except Exception as e:
        return f"❗错误：{e}"

# 可选：连通性自检（侧边栏按钮里调用）
def health_check() -> str:
    try:
        _ = client().models.list()
        return "ok"
    except Exception as e:
        return f"error: {e}"

# 本地快速测试
if __name__ == "__main__":
    print(get_ai_response("你好，我有点焦虑，想聊聊。"))


