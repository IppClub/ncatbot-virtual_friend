import os
import asyncio
import configparser 
from .img_handler import read_img
from openai import AsyncOpenAI, OpenAIError
from ..config.config_loader import get_character
from datetime import datetime
import pytz

import logging

logger = logging.getLogger(__name__)  # 获取当前模块的 logger

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

API_KEY = config.get("deepseek", "API_KEY")
BASE_URL = config.get("deepseek", "BASE_URL")

client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL) # 只创建一个客户端
# 直接和ai发请求的接口
async def use_ai(prompt, content) -> str:
    response = await client.chat.completions.create(  # 确保这里是 await
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": content},
        ],
        stream=False,
        frequency_penalty=1.0,
        presence_penalty=1,
        temperature=1.3
    )
    return response.choices[0].message.content

# 处理速率限制的错误
async def handle_rate_limit():
    await asyncio.sleep(1)
    return char_config["error_msg"]

# 格式化响应文本
def format_response(text):
    return text.strip() if text else "出错了，稍后再试喵~"

# 处理用户和AI对话内容
async def ai_message(user_input: str, url_list ,character="魈", user_id=None) -> str:
    """ 处理 AI 对话请求 """
    try:
        # 获取角色配置
        char_config = get_character(character)
        if not char_config or "system_prompt" not in char_config:
            return "角色设定未找到，喵~"
        
        # 获取图片读取数据
        if url_list:
            img_text = await read_img(url_list)
            user_input += "\n\n" + "同时用户发送图片：" + img_text

        from ..memory.memory_manager import get_temp_memory_string,get_cur_mid_memory,get_long_memory #  用于处理循环导入
        # 获取用户的记忆
        short_term_memory = get_temp_memory_string(user_id)  # 短期记忆
        mid_term_memory = get_cur_mid_memory(user_id)  # 最近的中期记忆
        long_term_memory = get_long_memory(user_id)  # 长期记忆

        # 构建系统提示信息，加入记忆内容
        prompt = (
            "这是你的身份："
            +char_config["system_prompt"]
            + "\n\n"  # 分隔角色设定和记忆部分
            + "你正在和用户聊天，你是bot"
            + "短期记忆: " + short_term_memory + "\n\n" 
            + "最近的中期记忆: " + mid_term_memory + "\n\n" 
            + "长期记忆: " + long_term_memory + "\n\n"
            + "现在的时间是：" + get_current_time() + "\n\n"
            + "请你结合对话和时间信息继续聊天，返回近似于人类聊天的多条消息，不要重复之前的对话"
            + "保持自然节奏，以括号形式保留语气和动作。"
            + "每条最好不超过25字，每一条用'。'隔开，中间不要有额外的换行"
        )

        logger.info(f"发送给ai的prompt: {prompt}")

        # 调用 AI 生成回复
        response = await use_ai(prompt, user_input)
        
        # 格式化并返回回复
        return format_response(response)

    except OpenAIError as e:
        # 处理 rate limit 错误yong
        if "rate limit" in str(e).lower():
            return await handle_rate_limit()
        
        logger.error(f"API 调用失败: {str(e)}")
        return char_config["error_msg"]


# 使用llm拆分回答（暂时没用）
async def split_response_with_llm(text):
    """借助 LLM 将长文本拆成多条自然的短消息"""
    prompt = f"请将以下文本拆分成适合人类聊天的多条消息，保持自然节奏，每条最好不超过25字, 每一条用'。'隔开，中间不要有额外的换行：\n\n{text}"

    try:
        response = await client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "system", "content": "你是一个智能分段助手"},
                {"role": "user", "content": prompt},
            ],
            stream=False
        )

        return format_response(response.choices[0].message.content)
        
    except OpenAIError as e:  # 捕获所有 OpenAI 相关错误
        logger.info(f"API 调用失败: {str(e)}")
        return text  # 如果拆分失败，返回原文本


# 获取当前时间
def get_current_time() -> str:
    # 设置时区为北京时间
    beijing_tz = pytz.timezone('Asia/Shanghai')
    now = datetime.now(beijing_tz)

    # 格式化字符串（示例格式："2025-03-14 星期五 15:30:45"）
    time_str = now.strftime("%Y-%m-%d %A %H:%M:%S")
    return time_str
