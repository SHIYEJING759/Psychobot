# chat_engine.py
import os
from dotenv import load_dotenv
from openai import OpenAI
import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

# 加载 .env 文件中的 API 密钥
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# 初始化 OpenAI 客户端
client = OpenAI(api_key=api_key)

def get_ai_response(user_input):
    """
    调用 OpenAI Chat Completions API 获取 AI 回复
    """
    try:
        response = client.chat.completions.create(
            model="gpt-4o",  # 可替换为 "gpt-4" 或 "gpt-4o"
            messages=[
                {"role": "system", "content": "你是一位温暖、理解人的心理支持型AI机器人，善于倾听和安慰用户,在共情用户时你最好不要显得很假，要有真实的温度和情感。"},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"❗错误：{e}"

# 测试函数（可选）
def test_api():
    test_input = "你好，我感觉最近有点焦虑。"
    return get_ai_response(test_input)

if __name__ == "__main__":
    print("测试结果：", test_api())
