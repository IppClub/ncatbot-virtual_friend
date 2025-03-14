from .user_state import USER_CHARACTERS,USER_INPUTS, USER_TASKS
from ..ai_utils.ai_helper import ai_message
from .task_manager import schedule_task
from ..config.config_loader import get_character ,get_all_characters_names
from ..memory.user_manager import get_user_character, insert_user_character, modify_user_character,upsert_user_character
import logging

logger = logging.getLogger(__name__)  # 获取当前模块的 logger

# 直接接收私聊消息部分
async def handle_private_message(msg, api):

    user_id = msg.user_id

    # 测试
    if msg.raw_message == "测试":
        await api.post_private_msg(user_id, text="Ncatbot 插件测试成功喵")
        return
    
    # 帮助
    if msg.raw_message == "帮助":
        return_msg="可用命令：1.设置角色 角色名；2.切换角色 角色名；3.查看当前角色；4.查看所有角色（直接输入原始文本）"
        await api.post_private_msg(user_id, text=return_msg)
        return 
    
    # 设置角色
    if msg.raw_message.startswith("设置角色"): 
        # 判断输入格式   
        character = msg.raw_message.split(maxsplit=1)[1] if len(msg.raw_message.split()) > 1 else None
        if not character:
            await api.post_private_msg(user_id, "正确格式：设置角色 角色名")
            return

        if character not in get_character(""):
            await api.post_private_msg(user_id, "未知角色")
            return

        USER_CHARACTERS[user_id]=character # 更新缓存
        upsert_user_character(user_id, character) # 更新数据库
        await api.post_private_msg(user_id, f"已设置成 {character} 人格")
        return
        
    # 切换角色
    if msg.raw_message.startswith("切换角色"): 
        # 判断输入格式   
        character = msg.raw_message.split(maxsplit=1)[1] if len(msg.raw_message.split()) > 1 else None
        if not character:
            await api.post_private_msg(user_id, "正确格式：切换角色 角色名")
            return

        if character not in get_character(""):
            await api.post_private_msg(user_id, "未知角色")
            return

        USER_CHARACTERS[user_id]=character # 更新缓存
        upsert_user_character(user_id, character) # 更新数据库
        await api.post_private_msg(user_id, f"已切换至 {character} 人格")
        return

    # 查看所有角色
    if msg.raw_message == "查看所有角色":
        all_characters = get_all_characters_names()
        await api.post_private_msg(user_id, f"全部角色有：{all_characters}")
        return 
    
    cur_character = get_cur_character(user_id)
    
    # 查看当前角色
    if msg.raw_message == "查看当前角色":
        if(cur_character == ""):
            await api.post_private_msg(user_id, "请先设置角色喵~（输入：设置角色 角色名）")
            return 
        else:
            await api.post_private_msg(user_id, f"当前角色为：{cur_character}")
            return
    
    #判断有没有该用户的记录
    if(cur_character == ""):
        await api.post_private_msg(user_id, "请先设置角色喵~（输入：切换角色 角色名）")
        return 
    
    # 处理用户输入
    if user_id in USER_INPUTS:
        USER_INPUTS[user_id] += " " + msg.raw_message
    else:
        USER_INPUTS[user_id] = msg.raw_message

    # 取消旧任务，启动新任务
    await schedule_task(user_id, api, cur_character)


def get_cur_character(user_id) -> str:
    # 首先检查缓存
    if user_id in USER_CHARACTERS:
        return USER_CHARACTERS[user_id]
    else:
        logger.info(f"把用户 {user_id} 的角色数据从数据库加载到缓存...")
        # 从数据库查询(如果没有数据是返回None)
        db = get_user_character(user_id)
        if db is not None:
            USER_CHARACTERS[user_id] = db  # 更新缓存
            logger.info(f"用户 {user_id} 的角色数据从数据库加载到缓存完成,是 {db}")
            return db  # 返回角色名（字符串）
        logger.info(f"数据库没有用户 {user_id} 的角色数据")
        return ""  # 如果没有查询到角色，则返回空字符串
