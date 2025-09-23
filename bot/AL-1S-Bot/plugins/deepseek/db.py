import sqlite3
import json
from datetime import datetime
from contextlib import closing
from .tools import short
import os

def init_db():
    with closing(sqlite3.connect('deepseek.db')) as conn:
        with conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS chat_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    message TEXT NOT NULL,
                    answer TEXT NOT NULL,
                    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id TEXT NOT NULL,
                    intro TEXT,
                    description TEXT
                )
            ''')
            conn.commit()

def save_message(user_id: str, message: str, answer: str):
    with closing(sqlite3.connect('deepseek.db')) as conn:
        with conn:
            conn.execute(
                'INSERT INTO chat_history (user_id, message, answer) VALUES (?, ?, ?)', 
                (user_id, message, answer)
            )
            conn.commit()

def get_user_intro(user_id: str) -> str:
    with closing(sqlite3.connect('deepseek.db')) as conn:
        cursor = conn.execute(
            'SELECT intro FROM users WHERE user_id = ?', 
            (user_id)
        )
        row = cursor.fetchone()
        return row[0] if row else ""

def get_user_description(user_id: str) -> str:
    with closing(sqlite3.connect('deepseek.db')) as conn:
        cursor = conn.execute(
            'SELECT description FROM users WHERE user_id = ?', 
            (user_id)
        )
        row = cursor.fetchone()
        return row[0] if row else ""
    
def get_user_message(user_id: str) -> str:
    with closing(sqlite3.connect('deepseek.db')) as conn:
        cursor = conn.execute(
            'SELECT message, timestamp, answer FROM chat_history WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20', 
            (user_id)
        )
        rows = cursor.fetchall()
        messages = []
        for message, timestamp, answer in reversed(rows):
            dt = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            messages.append({"时间": dt, "用户": message, "AI": answer})
        return json.dumps(messages, ensure_ascii=False)

def update_user_intro(user_id: str, intro: str):
    with closing(sqlite3.connect('deepseek.db')) as conn:
        with conn:
            cursor = conn.execute(
                'SELECT id FROM users WHERE user_id = ?', 
                (user_id,)
            )
            if cursor.fetchone():
                conn.execute(
                    'UPDATE users SET intro = ? WHERE user_id = ?', 
                    (intro, user_id)
                )
            else:
                conn.execute(
                    'INSERT INTO users (user_id, intro) VALUES (?, ?)', 
                    (user_id, intro)
                )
            conn.commit()

def show_db():
    with closing(sqlite3.connect('deepseek.db')) as conn:
        cursor = conn.execute('SELECT user_id, message, answer, timestamp FROM chat_history ORDER BY timestamp DESC LIMIT 10')
        rows = cursor.fetchall()
        return os.path.abspath('deepseek.db') + "\n".join([f'user: {short(row[0])} \nmessage: {short(row[1])} \nanswer: {short(row[2])} \ntimastamp: {row[3]}' for row in rows])

def clear_db():
    with closing(sqlite3.connect('deepseek.db')) as conn:
        with conn:
            conn.execute('DELETE FROM chat_history')
            conn.execute('DELETE FROM users')
            conn.commit()