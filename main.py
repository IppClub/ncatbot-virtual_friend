import configparser
import datetime
import json
import os
import asyncio
import logging
import random
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

class virtual_friend(BasePlugin):
    name = "virtual_friend"  # 插件名称
    version = "0.1.0"  # 插件版本

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

        # 试验功能：机器人启动时主动向指定主用户发送消息（但是在测试环境频繁重启机器人时候可能导致记忆混乱）
        # 主用户id放在配置文件中
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))  
        CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH,encoding="utf-8")

        USER_ID = config.get("host", "USER_ID")

        message_data = {'message_id': '284041315', 
                        'user_id': USER_ID, 
                        'message_seq': '284041315', 
                        'real_id': '284041315', 
                        'message_type': 'private', 
                        "sender": {"user_id": USER_ID, "nickname": "夜愿", "card": ""},
                        'raw_message': '', 
                        'font': '14', 
                        'sub_type': 'friend', 
                        "message": json.loads('[{"type": "text", "data": {"text": ""}}]'),  # 这里改为列表 
                        'message_format': 'array', 
                        'target_id': USER_ID}
        private_msg = PrivateMessage(message_data)
        await handle_private_message(private_msg, self.api)

        # 试验功能：定时任务发送消息
        # 启动后台定时任务
        asyncio.create_task(self.start_sending_messages())
    
    # 随机时间间隔发送消息
    # TODO: 现在是后台进程死循环，是否会影响性能？
    async def start_sending_messages(self):
        # 从配置文件读取参数
        BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))  
        CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

        config = configparser.ConfigParser()
        config.read(CONFIG_FILE_PATH,encoding="utf-8")
        max_reply_interval = int(config.get("active-send", "max_reply_interval"))
        min_reply_interval = int(config.get("active-send", "min_reply_interval"))
        silent_start = config.get("active-send", "silent_start")
        silent_end = config.get("active-send", "silent_end")
        user_id = config.get("host", "USER_ID")

        # 解析静默时间段的开始和结束时间
        silent_start_hour, silent_start_minute = map(int, silent_start.split(":"))
        silent_end_hour, silent_end_minute = map(int, silent_end.split(":"))

        """开始发送消息的死循环"""
        while True:
            current_time = datetime.datetime.now()
            current_hour = current_time.hour
            current_minute = current_time.minute

            # 检查是否在静默时间段内
            if self.is_in_silent_period(current_hour, current_minute, silent_start_hour, silent_start_minute, 
                                        silent_end_hour, silent_end_minute):
                reply_interval = random.randint(min_reply_interval, max_reply_interval)
                logger.info(f"当前在静默时间段，不发送消息，将在{reply_interval}秒后再次尝试")
                await asyncio.sleep(reply_interval)

            else:
                # 随机生成回复间隔
                reply_interval = random.randint(min_reply_interval, max_reply_interval)
                logger.info(f"将在 {reply_interval} 秒后发送消息")
                
                # 等待一段时间
                await asyncio.sleep(reply_interval)
                
                # 发送消息
                message_data = {'message_id': '284041315', 
                                'user_id': user_id, 
                                'message_seq': '284041315', 
                                'real_id': '284041315', 
                                'message_type': 'private', 
                                "sender": {"user_id": user_id, "nickname": "夜愿", "card": ""}, 
                                'raw_message': '', 
                                'font': '14', 
                                'sub_type': 'friend', 
                                "message": [{"type": "text", "data": {"text": ""}}], 
                                'message_format': 'array', 
                                'target_id': user_id}
                private_msg = PrivateMessage(message_data)
                await handle_private_message(private_msg, self.api)

    def is_in_silent_period(self, current_hour, current_minute, silent_start_hour, silent_start_minute, silent_end_hour, silent_end_minute):
        """检查当前时间是否在静默时间段内"""
        start_time = datetime.time(silent_start_hour, silent_start_minute)
        end_time = datetime.time(silent_end_hour, silent_end_minute)
        current_time = datetime.time(current_hour, current_minute)

        # 处理跨午夜的静默时间段
        if silent_end_hour < silent_start_hour or (silent_end_hour == silent_start_hour and silent_end_minute < silent_start_minute):
            return current_time >= start_time or current_time <= end_time
        else:
            return start_time <= current_time <= end_time