import os
import asyncio
import configparser
from openai import AsyncOpenAI, OpenAIError
from ..config.config_loader import get_character
import logging

logger = logging.getLogger(__name__)  # 获取当前模块的 logger

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH, encoding="utf-8")

DEFAULT_API_KEY = "<input_your_key>"
DEFAULT_BASE_URL = "https://ark.cn-beijing.volces.com/api/v3"

API_KEY = config.get("doubao", "API_KEY", fallback=DEFAULT_API_KEY)
BASE_URL = config.get("doubao", "BASE_URL", fallback=DEFAULT_BASE_URL)

# 如果配置为默认值，则不启用识图功能
if API_KEY == DEFAULT_API_KEY or BASE_URL == DEFAULT_BASE_URL:
    client = None
else:
    client = AsyncOpenAI(api_key=API_KEY, base_url=BASE_URL)  # 只创建一个客户端

# 识图，传入一个图片列表，返回图片描述
async def read_img(image_urls: list) -> str:
    """
    传入图片 URL 列表，调用 Doubao API 进行识别，返回图片描述
    """
    if not client:
        logger.info("识图功能未启用，返回'图片'。")
        return "图片"

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "详细说明这些图片中的内容"},
            ] + [{"type": "image_url", "image_url": {"url": url}} for url in image_urls]
        }
    ]

    try:
        response = await client.chat.completions.create(
            model="doubao-1.5-vision-pro-32k-250115",  # 确保模型名称正确
            messages=messages
        )
        result = response.choices[0].message.content
        logger.info(f"API 调用成功: {result}")
        return result
    except OpenAIError as e:
        logger.error(f"API 调用失败: {e}")
        return "图片识别失败，请稍后再试"
