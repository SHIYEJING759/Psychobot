
# import os
# import sqlite3
# import pandas as pd
# from datetime import datetime, timedelta
# from openai import OpenAI
# from dotenv import load_dotenv

# # 数据库路径设置
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
# os.makedirs(DATA_DIR, exist_ok=True)
# DB_PATH = os.path.join(DATA_DIR, "chat_logs.db")

# def init_db():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()

#     # 用户表
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')

#     # 聊天记录表
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS chat_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             role TEXT NOT NULL,
#             message TEXT NOT NULL,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY(user_id) REFERENCES users(id)
#         )
#     ''')

#     # 情绪记录表
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS emotion_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             user_id INTEGER,
#             emotion TEXT NOT NULL,
#             note TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
#             FOREIGN KEY(user_id) REFERENCES users(id)
#         )
#     ''')

#     conn.commit()
#     conn.close()

# def create_user_table():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         );
#     """)
#     conn.commit()
#     conn.close()
# def create_chat_table():
#         conn = sqlite3.connect(DB_PATH)
#         c = conn.cursor()
#         c.execute('''
#             CREATE TABLE IF NOT EXISTS chat_logs (
#                 id INTEGER PRIMARY KEY AUTOINCREMENT,
#                 role TEXT NOT NULL,
#                 message TEXT NOT NULL,
#                 timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#             )
#         ''')
#         conn.commit()
#         conn.close()
# ### --- 多用户支持的核心函数 --- ###

# # 保存消息
# def save_message(role, message, user_id):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('INSERT INTO chat_logs (user_id, role, message) VALUES (?, ?, ?)', (user_id, role, message))
#     conn.commit()
#     conn.close()

# # 读取用户的聊天记录
# def get_recent_messages(user_id, limit=100):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('''
#         SELECT role, message, timestamp
#         FROM chat_logs
#         WHERE user_id = ?
#         ORDER BY id DESC LIMIT ?
#     ''', (user_id, limit))
#     rows = c.fetchall()
#     conn.close()
#     return rows

# # 保存情绪记录
# def save_emotion_log(emotion, note, user_id):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("INSERT INTO emotion_logs (user_id, emotion, note) VALUES (?, ?, ?)", (user_id, emotion, note))
#     conn.commit()
#     conn.close()

# # 获取用户情绪记录
# def get_chat_emotion_logs(user_id, days=30):
#     conn = sqlite3.connect(DB_PATH)
#     query = f"""
#         SELECT emotion, note, timestamp
#         FROM emotion_logs
#         WHERE user_id = ? AND timestamp >= datetime('now', '-{days} days')
#     """
#     df = pd.read_sql_query(query, conn, params=(user_id,))
#     conn.close()
#     return df

# # 用户注册
# def register_user(username, password):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     try:
#         c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
#         conn.commit()
#         return True
#     except:
#         return False
#     finally:
#         conn.close()

# # 用户登录
# def login_user(username, password):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
#     user = c.fetchone()
#     conn.close()
#     return user[0] if user else None

# # 生活事件分析

# load_dotenv()
# client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# def detect_event(text):
#     prompt = f"""
#     你是一个心理健康事件识别模型。请阅读下面的用户输入，判断是否包含下列三类事件：工作压力，感情冲突，学业烦恼，并返回标签或 "无"：\n\n输入：\"{text}\"\n\n请只返回下列四个之一：\n- 工作压力\n- 感情冲突\n- 学业烦恼\n- 无
#     """
#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             temperature=0.3,
#             max_tokens=10
#         )
#         result = response.choices[0].message.content.strip()
#         return result if result in ["工作压力", "感情冲突", "学业烦恼"] else None
#     except Exception:
#         return None
# def detect_emotion(text):
#     """
#     使用 GPT 模型分析用户输入文本，返回五种标准情绪之一。
#     """
#     prompt = f"""
# 你是一个敏感度极高的情绪识别模型，善于理解用户在中文输入中**隐藏或表达的情绪信号**。

# 请判断以下文本的主要情绪类别，输出以下五个标签之一：
# - 😊 开心
# - 😣 难过
# - 😐 平静
# - 😡 生气
# - 🥶 焦虑

# 请特别注意：
# - 如果文本中表达了焦虑、崩溃、疲惫、无助等情绪，请优先考虑“🥶 焦虑”或“😣 难过”；
# - 只有在完全看不出情绪波动、语气客观理性时，才能使用“😐 平静”；
# - 如情绪混合，请以“最强烈或最频繁出现的情绪”为主导；

# 请仅返回标签（例如：🥶 焦虑），不要添加其他内容。

# 文本如下："{text}"

#     """

#     try:
#         response = client.chat.completions.create(
#             model="gpt-3.5-turbo",
#             messages=[
#                 {"role": "user", "content": prompt}
#             ],
#             temperature=0.3,
#             max_tokens=10,
#         )
#         result = response.choices[0].message.content.strip()
#         # 只接受五种合法标签
#         valid_emotions = ["😊 开心", "😣 难过", "😐 平静", "😡 生气", "🥶 焦虑"]
#         return result if result in valid_emotions else "😐 平静"
#     except Exception as e:
#         return "😐 平静"

import os
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv
from supabase import create_client, Client

# 载入环境变量
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
client: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# OpenAI
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

### --- 多用户支持的核心函数 --- ###

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

### --- GPT 情绪识别与事件识别 --- ###

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
