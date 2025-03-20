import os
import asyncio
import logging
from ncatbot.plugin import BasePlugin, CompatibleEnrollment

from ncatbot.core.message import GroupMessage, PrivateMessage
from .handlers.private_handler import handle_private_message
from .memory.memory_manager import init_db

# 用于单元测试引入
from .ai_utils.img_handler import read_img

bot = CompatibleEnrollment  # 兼容回调函数注册器

# 全局配置日志
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

# **定义 logger 变量**
logger = logging.getLogger(__name__)

class MyPlugin(BasePlugin):
    name = "virtual_friend"  # 插件名称
    version = "0.0.1"  # 插件版本

    @bot.group_event() # 暂时不考虑开发群聊功能
    async def on_group_event(self, msg: GroupMessage):
        # 定义的回调函数
        if msg.raw_message == "测试":
            await self.api.post_group_msg(msg.group_id, text="Ncatbot 插件测试成功喵")

    @bot.private_event()
    async def on_private_message(self, msg: PrivateMessage):    
        # logger.info(f"收到私聊消息: {msg.message}")    
        # logger.info(f"纯文本消息{msg.raw_message}")
        # for segment in msg.message:
        #     if segment["type"] == "image":  # 确保是图片消息
        #         image_url = segment["data"]["url"]
        #         logger.info(f"收到图片消息，URL: {image_url}")
        #         urls= [image_url]
        #         await read_img(urls)

        
        await handle_private_message(msg, self.api) # 转到处理函数

    async def on_load(self):
        """插件加载时执行的操作"""
        print(f"{self.name} 插件已加载")
        print(f"插件版本: {self.version}")
        init_db() # 初始化数据库        
    
