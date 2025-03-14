import os
import sqlite3
import asyncio
from datetime import datetime, timedelta

import logging

logger = logging.getLogger(__name__)  # 获取当前模块的 logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前模块所在目录
DB_PATH = os.path.join(BASE_DIR, "memory.db")  # 让数据库文件存储在模块目录下

def get_user_character(user_id) -> str:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT character FROM user_characters WHERE user_id=?", (user_id,))
    result = cursor.fetchone()
    conn.close()
    logger.info(f"查询用户 {user_id} 角色数据完成")
    return result[0] if result else None 

def modify_user_character(user_id, character) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE user_characters SET character=? WHERE user_id=?", (character, user_id))
    conn.commit()
    conn.close()
    logger.info(f"修改用户 {user_id} 角色数据 { character}完成")
    
def insert_user_character(user_id, character) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO user_characters (user_id, character) VALUES (?, ?)", (user_id, character))
    conn.commit()
    conn.close()
    logger.info(f"插入用户 {user_id} 角色数据{character}]完成")
    
def upsert_user_character(user_id, character) -> None:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # 使用 INSERT OR REPLACE 语句
    cursor.execute("""
        INSERT OR REPLACE INTO user_characters (user_id, character) 
        VALUES (?, ?)
    """, (user_id, character))
    conn.commit()
    conn.close()
    logger.info(f"插入或更新用户 {user_id} 角色数据 {character} 完成")
