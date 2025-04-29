import os
import sqlite3
import asyncio
import configparser 
from datetime import datetime, timedelta
from ..ai_utils.check_memory import check_temp_memory, check_mid_memory, check_long_memory  # 调用你的记忆函数
from ..RAG_memory.main import store_memory

import logging

logger = logging.getLogger(__name__)  # 获取当前模块的 logger

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # 当前模块所在目录
DB_PATH = os.path.join(BASE_DIR, "memory.db")  # 让数据库文件存储在模块目录下

BASE_DIR2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR2, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

TEMP_GROUP_SIZE=config.getint("memory", "TEMP_GROUP_SIZE") # 每一组处理的临时记忆条数
MID_GROUP_SIZE=config.getint("memory", "MID_GROUP_SIZE") # 每一组处理的中期记忆条数

def init_db():
    """检查数据库是否存在，不存在则创建并初始化"""
    if not os.path.exists(DB_PATH):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS temp_memory (
                user_id TEXT NOT NULL,
                content TEXT NOT NULL,
                role TEXT NOT NULL,  -- "user" 或 "bot"
                timestamp TIMESTAMP DEFAULT datetime('now', 'localtime')
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS mid_memory (
                user_id TEXT NOT NULL,
                content TEXT NOT NULL UNIQUE,
                timestamp TIMESTAMP DEFAULT datetime('now', 'localtime')
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS long_memory (
                user_id TEXT NOT NULL,
                content TEXT NOT NULL UNIQUE,
                timestamp TIMESTAMP DEFAULT datetime('now', 'localtime')
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_characters (
                user_id TEXT PRIMARY KEY UNIQUE,
                character TEXT
            );
        """)

        conn.commit()
        conn.close()
        logger.info("数据库初始化完成！")
    else:
        logger.info("数据库已存在，无需初始化。")

# 管理短期记忆
async def manage_temp_memory(user_id):
    logger.info(f"正在处理{user_id}短期记忆")
    # 获取短期记忆条数
    temp_memory_data = get_temp_memory(user_id) 
    temp_count = len(temp_memory_data)

    if temp_count < TEMP_GROUP_SIZE*2:
        logger.info(f"短期记忆条数为：{str(temp_count)},不需要处理")
        # 如果短期记忆条数小于10，则不做处理，返回

    else:
        logger.info(f"短期记忆条数为：{str(temp_count)},需要处理")
        # 获取早期短期记忆，转化成字符串格式
        temp_memory_last=get_temp_memory_last(user_id)

        temp_memory_last_str="\n".join([f"{m['role']}: {m['content']},time:{'timestamp'}" for m in temp_memory_last])
        
        # 使用 check_temp_memory 来总结这些短期记忆
        summary = await check_mid_memory(user_id, temp_memory_last_str)

        logger.info( f"总结结果为：{summary}" )            
        if summary != "无重要内容":
            # 存入中期记忆
            insert_mid_memory(user_id, summary)
        
        # 存入向量数据库
        await store_memory(temp_memory_last_str, user_id)

        # 清空短期记忆
        clear_temp_memory(user_id)
    logger.info("短期记忆处理完成")

# 管理中期记忆
async def manage_mid_memory(user_id):
    logger.info(f"正在处理{user_id}中期记忆")
    mid_memory_data = get_mid_memory(user_id)
    mid_count = len(mid_memory_data)

    if mid_count < MID_GROUP_SIZE:
        # 如果长期记忆条数小于50，则不做处理，返回
        logger.info (f"中期记忆条数为：{str(mid_count)} 不需要处理")

    else:
        logger.info (f"中期记忆条数为：{str(mid_count)} 需要处理")
        formatted_content=""
        for entry in mid_memory_data:
            formatted_content += entry['content']
        
        # 使用 check_long_memory 来总结这些长期记忆
        summary = await check_long_memory(user_id, formatted_content)
        logger.info(f"总结结果为：{summary}" )
        if summary != "无重要内容":
            insert_long_memory(user_id, summary)
        clear_mid_memory(user_id)
    logger.info("中期记忆处理完成")

# 管理长期记忆（当长期记忆过多的时候，自己总结重复存入）
async def manage_long_memory(user_id):
    logger.info(f"正在处理{user_id}长期记忆")
    long_memory_data = get_long_memory_raw(user_id)
    long_count = len(long_memory_data)

    if long_count < 10:
        # 如果长期记忆条数小于10，则不做处理，返回
        logger.info (f"长期记忆条数为：{str(long_count)} 不需要处理")

    else:
        logger.info (f"长期记忆条数为：{str(long_count)} 需要处理")
        formatted_content = "\n".join(long_memory_data)
        summary = await check_long_memory(user_id, formatted_content)

        if summary != "无重要内容":
            clear_long_memory(user_id)
            insert_long_memory(user_id, summary)
        else:
            clear_long_memory(user_id)

# 删除临时记忆（时间最早的一组）
def clear_temp_memory(user_id):
    logger.info(f"删除{user_id}最早的临时记忆")
    """ 清空用户的临时记忆 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM temp_memory WHERE timestamp IN ( SELECT timestamp FROM temp_memory WHERE user_id = ? ORDER BY timestamp LIMIT ?);", (user_id,TEMP_GROUP_SIZE))
    conn.commit()
    conn.close()

# 删除中期记忆（只留下最近的一条）
def clear_mid_memory(user_id):
    logger.info(f"删除{user_id}的中期记忆")
    """ 清空用户的中期记忆 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM mid_memory WHERE timestamp IN ( SELECT timestamp FROM mid_memory WHERE user_id = ? ORDER BY timestamp LIMIT ?);", (user_id,MID_GROUP_SIZE-1))
    conn.commit()
    conn.close()


# 删除用户所有的长期记忆
def clear_long_memory(user_id):
    logger.info(f"删除{user_id}的长期记忆")
    """ 清空用户的长期记忆 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM long_memory WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()

# 插入临时记忆
def insert_temp_memory(user_id, content, role):
    logger.info(f"正在插入一条临时数据:{role}:{content}")
    """ 插入临时记忆 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO temp_memory (user_id, content, role) VALUES (?, ?, ?)", (user_id, content, role))
    conn.commit()
    conn.close()
    logger.info("插入一条临时数据完成")

# 插入中期记忆
def insert_mid_memory(user_id, content):
    logger.info(f"正在插入一条中期数据:{content}")
    """ 插入中期记忆，避免重复存储 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO mid_memory (user_id, content) VALUES (?, ?)", (user_id, content))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # 忽略重复内容
    conn.close()
    logger.info("插入一条中期数据完成")

# 插入长期记忆
def insert_long_memory(user_id, content):
    logger.info(f"正在插入一条长期数据:{content}")
    """ 插入长期记忆，避免重复存储 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO long_memory (user_id, content) VALUES (?, ?)", (user_id, content))
        conn.commit()
    except sqlite3.IntegrityError:
        pass  # 忽略重复内容
    conn.close()
    logger.info("插入一条长期数据完成")

# 获取全部临时记忆（拼接格式）（返回加上时间）
def get_temp_memory_string(user_id):
    logger.info(f"正在获取用户 {user_id} 的拼接临时记忆...")
    """ 获取用户的临时记忆 """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, role, timestamp FROM temp_memory WHERE user_id = ?", (user_id,))
    
    memories = [{"content": row[0], "role": row[1],"timestamp": row[2]} for row in cursor.fetchall()]
    conn.close()

    # 如果没有临时记忆，返回空字符串
    if not memories:
        logger.info(f"用户 {user_id} 没有临时记忆。")
        return ""

    # 拼接记忆内容
    formatted_content = ""
    for entry in memories:
        if entry["role"] == "bot":
            formatted_content += f"bot: {entry['content']}，time:{entry['timestamp']};"
        else:
            formatted_content += f"user: {entry['content']}，time:{entry['timestamp']};"
    
    logger.info(f"拼接临时记忆内容：{formatted_content}")
    return formatted_content.strip("，")  # 去掉最后的逗号


# 获取全部临时记忆（原始格式）
def get_temp_memory(user_id):
    logger.info(f"正在获取用户 {user_id} 的全部临时记忆原始格式...")
    
    # 获取用户的临时记忆
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, role, timestamp FROM temp_memory WHERE user_id = ?", (user_id,))
    
    memories = [{"content": row[0], "role": row[1], "timestamp": row[2]} for row in cursor.fetchall()]
    conn.close()

    if not memories:
        logger.info(f"用户 {user_id} 没有临时记忆。")
    else:
        logger.info(f"获取用户 {user_id} 的全部临时记忆原始格式：{memories}")
    return memories  # 返回所有的临时记忆


# 获取最近20条临时记忆（原始格式）
def get_temp_memory_recent(user_id):
    logger.info(f"正在获取用户 {user_id} 的全部临时记忆原始格式...")
    
    # 获取用户的临时记忆
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, role, timestamp FROM temp_memory WHERE user_id = ? ORDER BY timestamp DESC LIMIT ?", (user_id, TEMP_GROUP_SIZE))
    
    # 使用 reversed 反转查询结果顺序（保持最新记录在前）
    memories = [{"content": row[0], "role": row[1], "timestamp": row[2]} for row in reversed(cursor.fetchall())]
    conn.close()

    if not memories:
        logger.info(f"用户 {user_id} 没有临时记忆。")
    else:
        logger.info(f"获取用户 {user_id} 的最近20条临时记忆原始格式：{memories}")
    return memories  # 返回所有的临时记忆


# 获取最早20条临时记忆（原始格式）
def get_temp_memory_last(user_id):
    logger.info(f"正在获取用户 {user_id} 的最早临时记忆原始格式...")
    
    # 获取用户的临时记忆
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content, role,timestamp FROM temp_memory WHERE user_id = ? ORDER BY timestamp ASC LIMIT ?", (user_id,TEMP_GROUP_SIZE))
    
    memories = [{"content": row[0], "role": row[1] ,"timestamp": row[2]} for row in cursor.fetchall()]
    conn.close()

    if not memories:
        logger.info(f"用户 {user_id} 没有临时记忆。")
    else:
        logger.info(f"获取用户 {user_id} 的最早的20条临时记忆原始格式：{memories}")
    return memories  # 返回所有的临时记忆

# 获取最新的中期记忆（纯content文本）
def get_cur_mid_memory(user_id):
    logger.info(f"正在获取用户 {user_id} 的最新中期记忆文本...")
    # 获取用户的最新中期记忆
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM mid_memory WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", (user_id,))
    memory = cursor.fetchone()
    conn.close()
    
    if memory:
        logger.info(f"获取用户 {user_id} 的最新中期记忆：{memory[0]}")
        return memory[0]
    else:
        logger.info(f"用户 {user_id} 没有最新的中期记忆。")
        return ""  # 如果没有记录，返回空字符串


# 获取全部中期记忆（原始格式）
def get_mid_memory(user_id):
    logger.info(f"正在获取用户 {user_id} 的全部中期记忆原始格式...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 构造 SQL 语句并打印
    sql = "SELECT content FROM mid_memory WHERE user_id = ?"

    cursor.execute(sql, (user_id,))
    memories = [{"content": row[0]} for row in cursor.fetchall()]

    conn.close()
    logger.info(f"获取到的中期记忆：{memories}") 
    return memories  # 统一返回列表

# 获取用户的全部长期记忆（拼接成一段话）
def get_long_memory(user_id):
    logger.info(f"正在获取用户 {user_id} 的全部长期记忆...")
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("SELECT content FROM long_memory WHERE user_id = ?", (user_id,))
    memories = [row[0] for row in cursor.fetchall()]
    
    conn.close()
    
    if not memories:  # 如果没有长期记忆
        logger.info(f"用户 {user_id} 没有长期记忆。")
        return ""  # 返回空字符串
    
    # 将记忆内容用 \n 拼接成一段话
    long_memory_text = "\n".join(memories)
    
    logger.info(f"拼接长期记忆内容：{long_memory_text}")
    return long_memory_text

# 获取用户的全部长期记忆（原始格式）
def get_long_memory_raw(user_id):
    logger.info(f"正在获取用户 {user_id} 的全部长期记忆...")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT content FROM long_memory WHERE user_id = ?", (user_id,))
    memories = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not memories:
        logger.info(f"用户 {user_id} 没有长期记忆。")
    else:
        logger.info(f"获取到长期记忆：{memories}")
    return memories
