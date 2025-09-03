from openai import OpenAI
import streamlit as st


def _build_client() -> OpenAI:
    api_key = st.secrets["OPENAI_API_KEY"].strip()  
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is empty. Please set it in Streamlit Cloud → Secrets.")
    return OpenAI(api_key=api_key)

_client = None
def client() -> OpenAI:
    global _client
    if _client is None:
        _client = _build_client()
    return _client
#prompt of the ai and invoke functional code
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


def health_check() -> str:
    try:
        _ = client().models.list()
        return "ok"
    except Exception as e:
        return f"error: {e}"

if __name__ == "__main__":
    print(get_ai_response("你好，我有点焦虑，想聊聊。"))


