# from datetime import datetime, timedelta
# import pandas as pd
# import os
# import sqlite3
#
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
# os.makedirs(DATA_DIR, exist_ok=True)
#
# DB_PATH = os.path.join(DATA_DIR, "chat_logs.sql")
#
# # # 设置数据库文件路径（确保 data 文件夹存在）
# # DB_PATH = os.path.join(os.path.dirname(__file__), "data", "chat_logs.sql")
#
# def init_db():
#     """初始化数据库，创建 chat_logs 表（如果尚未存在）"""
#     os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS chat_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             role TEXT NOT NULL,
#             message TEXT NOT NULL,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         );
#     """)
#     conn.commit()
#     conn.close()
#
# def create_chat_table():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS chat_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             role TEXT NOT NULL,
#             message TEXT NOT NULL,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
# def save_message(role, message):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('INSERT INTO chat_logs (role, message) VALUES (?, ?)', (role, message))
#     conn.commit()
#     conn.close()
# def get_recent_messages(limit=100):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('''
#         SELECT role, message, timestamp
#         FROM chat_logs
#         ORDER BY id DESC
#         LIMIT ?
#     ''', (limit,))
#     rows = c.fetchall()
#     conn.close()
#     return rows
# def create_emotion_table():
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         CREATE TABLE IF NOT EXISTS emotion_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             emotion TEXT NOT NULL,
#             note TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     """)
#     conn.commit()
#     conn.close()
#
# def save_emotion_log(emotion, note):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     cursor.execute("""
#         INSERT INTO emotion_logs (emotion, note)
#         VALUES (?, ?)
#     """, (emotion, note))
#     conn.commit()
#     conn.close()
#
# def get_emotion_logs(days=30):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     query = f"""
#         SELECT emotion, note, timestamp
#         FROM emotion_logs
#         WHERE timestamp >= datetime('now', '-{days} days')
#     """
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df
#
# def get_chat_emotion_logs(days=30):
#     conn = sqlite3.connect(DB_PATH)
#     cursor = conn.cursor()
#     since = datetime.now() - timedelta(days=days)
#     query = "SELECT role, message, timestamp FROM chat_logs WHERE timestamp >= ?"
#     df = pd.read_sql_query(query, conn, params=[since.strftime('%Y-%m-%d %H:%M:%S')])
#     conn.close()
#     return df
#
# # def detect_emotion(text):
# #     # 简化的情绪识别逻辑，可换成更复杂模型
# #     if any(word in text for word in ["开心", "高兴", "快乐", "幸福"]):
# #         return "😊 开心"
# #     elif any(word in text for word in ["难过", "伤心", "沮丧"]):
# #         return "😣 难过"
# #     elif any(word in text for word in ["焦虑", "紧张", "担心"]):
# #         return "🥶 焦虑"
# #     elif any(word in text for word in ["生气", "愤怒", "恼火"]):
# #         return "😡 生气"
# #     else:
# #         return "😐 平静"
#
# # event_analysis.py
# import os
# from openai import OpenAI
# from dotenv import load_dotenv
#
# # 加载 API Key
# load_dotenv()
# api_key = os.getenv("OPENAI_API_KEY")
# client = OpenAI(api_key=api_key)
#
# def detect_event(text):
#     """
#     使用 GPT 模型分析用户输入中是否包含生活事件（如工作压力、感情冲突、学业焦虑等）
#     """
#     prompt = f"""
# 你是一个心理健康事件识别模型。请阅读下面的用户输入，判断其中是否包含以下三类事件之一，并返回事件标签（工作压力、感情冲突、学业焦虑）或无：
#
# 输入："{text}"
#
# 请只返回以下四种之一：
# - 工作压力
# - 感情冲突
# - 学业焦虑
# - 无
# """
#
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
#         return result if result in ["工作压力", "感情冲突", "学业焦虑"] else None
#     except Exception as e:
#         return None
#
# DB_PATH = "chat_logs.db"
#
# def create_user_table():
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()
#
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
#
# def login_user(username, password):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
#     user = c.fetchone()
#     conn.close()
#     return user[0] if user else None
import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# 设置数据库文件路径
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "chat_logs.db")

# 初始化数据库

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            emotion TEXT NOT NULL,
            note TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()
def create_user_table():
    """创建用户表（如果尚未存在）"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()
def create_chat_table():
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS chat_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                message TEXT NOT NULL,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        conn.commit()
        conn.close()
# chat 相关

def save_message(role, message):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO chat_logs (role, message) VALUES (?, ?)', (role, message))
    conn.commit()
    conn.close()

def get_recent_messages(limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT role, message, timestamp FROM chat_logs ORDER BY id DESC LIMIT ?
    ''', (limit,))
    rows = c.fetchall()
    conn.close()
    return rows

def get_chat_emotion_logs(days=30):
    conn = sqlite3.connect(DB_PATH)
    since = datetime.now() - timedelta(days=days)
    df = pd.read_sql_query("SELECT role, message, timestamp FROM chat_logs WHERE timestamp >= ?",
                           conn, params=[since.strftime('%Y-%m-%d %H:%M:%S')])
    conn.close()
    return df

# 情绪分析

def save_emotion_log(emotion, note):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO emotion_logs (emotion, note) VALUES (?, ?)", (emotion, note))
    conn.commit()
    conn.close()

def get_emotion_logs(days=30):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT emotion, note, timestamp
        FROM emotion_logs
        WHERE timestamp >= datetime('now', '-{days} days')
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 用户登录


def register_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
        return True
    except:
        return False
    finally:
        conn.close()

def login_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()
    return user[0] if user else None

# 生活事件分析

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def detect_event(text):
    prompt = f"""
    你是一个心理健康事件识别模型。请阅读下面的用户输入，判断是否包含下列三类事件：工作压力，感情冲突，学业烦恼，并返回标签或 "无"：\n\n输入：\"{text}\"\n\n请只返回下列四个之一：\n- 工作压力\n- 感情冲突\n- 学业烦恼\n- 无
    """
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            max_tokens=10
        )
        result = response.choices[0].message.content.strip()
        return result if result in ["工作压力", "感情冲突", "学业烦恼"] else None
    except Exception:
        return None
def detect_emotion(text):
    """
    使用 GPT 模型分析用户输入文本，返回五种标准情绪之一。
    """
    prompt = f"""
你是一个情绪识别模型，请根据以下用户的一段文本，判断其主要情绪类别，并仅返回以下五个标签之一：
- 😊 Happy
- 😣 Sad
- 😐 Peace
- 😡 Angry
- 🥶 Anxiety

用户输入："{text}"

请只返回对应的情绪标签（例如：😊 开心），不要添加解释。
    """

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=10,
        )
        result = response.choices[0].message.content.strip()
        # 只接受五种合法标签
        valid_emotions = ["😊 开心", "😣 难过", "😐 平静", "😡 生气", "🥶 焦虑"]
        return result if result in valid_emotions else "😐 平静"
    except Exception as e:
        return "😐 平静"
