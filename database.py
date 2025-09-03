
import os
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from supabase import create_client, Client


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def register_user(username, password):
    existing = client.table("users").select("id").eq("username", username).execute()
    if existing.data:
        return False
    res = client.table("users").insert({"username": username, "password": password}).execute()
    return True if res.data else False

def login_user(username, password):
    res = client.table("users").select("id").eq("username", username).eq("password", password).single().execute()
    if res.data:
        return res.data["id"]
    return None

def save_message(role, message, user_id):
    client.table("chat_logs").insert({
        "user_id": user_id,
        "role": role,
        "message": message
    }).execute()

def get_recent_messages(user_id, limit=100):
    res = client.table("chat_logs").select("role", "message", "timestamp") \
        .eq("user_id", user_id).order("id", desc=True).limit(limit).execute()
    return res.data if res.data else []

def save_emotion_log(emotion, note, user_id):
    client.table("emotion_logs").insert({
        "user_id": user_id,
        "emotion": emotion,
        "note": note
    }).execute()

def get_chat_emotion_logs(user_id, days=30):
    since = (datetime.utcnow() - timedelta(days=days)).isoformat()
    res = client.table("emotion_logs").select("emotion", "note", "timestamp") \
        .eq("user_id", user_id).gte("timestamp", since).execute()
    return pd.DataFrame(res.data) if res.data else pd.DataFrame()

### --- GPT emotional detection and event detection --- ###

def detect_event(text):
    prompt = f"""
你是一个心理健康事件识别模型。请阅读下面的用户输入，判断是否包含下列三类事件：工作压力，感情冲突，学业烦恼，并返回标签或 "无"：\n\n输入：\"{text}\"\n\n请只返回下列四个之一：\n- 工作压力\n- 感情冲突\n- 学业烦恼\n- 无
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        return result if result in ["工作压力", "感情冲突", "学业烦恼"] else "无"
    except Exception:
        return "无"

def detect_emotion(text):
    prompt = f"""
你是一个敏感度极高的情绪识别模型，善于理解用户在中文输入中**隐藏或表达的情绪信号**。

请判断以下文本的主要情绪类别，输出以下五个标签之一：
- 😊 开心
- 😣 难过
- 😐 平静
- 😡 生气
- 🥶 焦虑

请特别注意：
- 如果文本中表达了焦虑、崩溃、疲惫、无助等情绪，请优先考虑“🥶 焦虑”或“😣 难过”；
- 只有在完全看不出情绪波动、语气客观理性时，才能使用“😐 平静”；
- 如情绪混合，请以“最强烈或最频繁出现的情绪”为主导；

请仅返回标签（例如：🥶 焦虑），不要添加其他内容。

文本如下："{text}"
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        valid = ["😊 开心", "😣 难过", "😐 平静", "😡 生气", "🥶 焦虑"]
        return result if result in valid else "😐 平静"
    except Exception:
        return "😐 平静"
