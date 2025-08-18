# import os
# import sqlite3
# import pandas as pd
# from datetime import datetime, timedelta
# from openai import OpenAI
# from dotenv import load_dotenv

# # 设置数据库文件路径
# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# DATA_DIR = os.path.join(BASE_DIR, "data")
# os.makedirs(DATA_DIR, exist_ok=True)
# DB_PATH = os.path.join(DATA_DIR, "chat_logs.db")

# # 初始化数据库

# def init_db():
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
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS emotion_logs (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             emotion TEXT NOT NULL,
#             note TEXT,
#             timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
#         )
#     ''')
#     c.execute('''
#         CREATE TABLE IF NOT EXISTS users (
#             id INTEGER PRIMARY KEY AUTOINCREMENT,
#             username TEXT UNIQUE NOT NULL,
#             password TEXT NOT NULL
#         )
#     ''')
#     conn.commit()
#     conn.close()
# def create_user_table():
#     """创建用户表（如果尚未存在）"""
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
# # chat 相关

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
#         SELECT role, message, timestamp FROM chat_logs ORDER BY id DESC LIMIT ?
#     ''', (limit,))
#     rows = c.fetchall()
#     conn.close()
#     return rows

# def get_chat_emotion_logs(days=30):
#     conn = sqlite3.connect(DB_PATH)
#     since = datetime.now() - timedelta(days=days)
#     df = pd.read_sql_query("SELECT role, message, timestamp FROM chat_logs WHERE timestamp >= ?",
#                            conn, params=[since.strftime('%Y-%m-%d %H:%M:%S')])
#     conn.close()
#     return df

# # 情绪分析

# def save_emotion_log(emotion, note):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("INSERT INTO emotion_logs (emotion, note) VALUES (?, ?)", (emotion, note))
#     conn.commit()
#     conn.close()

# def get_emotion_logs(days=30):
#     conn = sqlite3.connect(DB_PATH)
#     query = f"""
#         SELECT emotion, note, timestamp
#         FROM emotion_logs
#         WHERE timestamp >= datetime('now', '-{days} days')
#     """
#     df = pd.read_sql_query(query, conn)
#     conn.close()
#     return df

# # 用户登录


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

# def login_user(username, password):
#     conn = sqlite3.connect(DB_PATH)
#     c = conn.cursor()
#     c.execute("SELECT id FROM users WHERE username=? AND password=?", (username, password))
#     user = c.fetchone()
#     conn.close()
#     return user[0] if user else None
# database.py

import os
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
from openai import OpenAI
from dotenv import load_dotenv

# 数据库路径设置
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)
DB_PATH = os.path.join(DATA_DIR, "chat_logs.db")

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 用户表
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    ''')

    # 聊天记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS chat_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            role TEXT NOT NULL,
            message TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    # 情绪记录表
    c.execute('''
        CREATE TABLE IF NOT EXISTS emotion_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            emotion TEXT NOT NULL,
            note TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')

    conn.commit()
    conn.close()


### --- 多用户支持的核心函数 --- ###

# 保存消息
def save_message(role, message, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO chat_logs (user_id, role, message) VALUES (?, ?, ?)', (user_id, role, message))
    conn.commit()
    conn.close()

# 读取用户的聊天记录
def get_recent_messages(user_id, limit=100):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        SELECT role, message, timestamp
        FROM chat_logs
        WHERE user_id = ?
        ORDER BY id DESC LIMIT ?
    ''', (user_id, limit))
    rows = c.fetchall()
    conn.close()
    return rows

# 保存情绪记录
def save_emotion_log(emotion, note, user_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO emotion_logs (user_id, emotion, note) VALUES (?, ?, ?)", (user_id, emotion, note))
    conn.commit()
    conn.close()

# 获取用户情绪记录
def get_emotion_logs(user_id, days=30):
    conn = sqlite3.connect(DB_PATH)
    query = f"""
        SELECT emotion, note, timestamp
        FROM emotion_logs
        WHERE user_id = ? AND timestamp >= datetime('now', '-{days} days')
    """
    df = pd.read_sql_query(query, conn, params=(user_id,))
    conn.close()
    return df

# 用户注册
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

# 用户登录
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
