import os
import asyncio
import configparser 
from ..ai_utils.ai_helper import ai_message
from .user_state import USER_IMGS, USER_INPUTS, USER_TASKS,USER_TASKS_QUEUES,USER_TASKS_MANAGER
from .user_state import USER_DATA_LOCK,USER_TASKS_MANAGER_LOCK,USER_TASKS_LOCK
from ..memory.memory_manager import insert_temp_memory, manage_temp_memory, manage_mid_memory


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

WAIT_TIME= config.getfloat("task", "WAIT_TIME") # 等待用户输入的时间

# 任务管理器：串行执行某个 user_id 的任务
async def user_task_manager(user_id):
    while True:
        task_data = await USER_TASKS_QUEUES[user_id].get()
        try:
            await core_send(task_data["final_message"], task_data["url_list"], task_data["api"], task_data["character"], task_data["user_id"])
        except Exception as e:
            print(f"Error processing task for user {user_id}: {e}")
        finally:
            USER_TASKS_QUEUES[user_id].task_done()

async def send_delayed_message(user_id, api, character):
    """ 等待用户输入结束后，再发送完整消息 """
    await asyncio.sleep(WAIT_TIME)

    # 等待结束
    # 把任务从字典中移除，独立运行，不会被新任务打断取消

    if user_id in USER_TASKS:
        USER_TASKS.pop(user_id, None)

    # 立即取出这部分应该处理的数据（加锁防止同时修改）
    async with USER_DATA_LOCK:
        if user_id in USER_INPUTS or user_id in USER_IMGS:
            final_message=""
            url_list=[]
            if user_id in USER_INPUTS:
                final_message=USER_INPUTS.pop(user_id)

            if user_id in USER_IMGS:
                url_list=USER_IMGS.pop(user_id)

            try:
                if(final_message!=""):
                    insert_temp_memory(user_id, final_message, "user")
            except Exception as e:
                print(f"Error inserting temp memory: {e}")

    # 初始化该用户的任务队列
    if user_id not in USER_TASKS_QUEUES:
        USER_TASKS_QUEUES[user_id] = asyncio.Queue()

    # 初始化任务管理器（加锁控制）
    async with USER_TASKS_MANAGER_LOCK:
        if user_id not in USER_TASKS_MANAGER:
            USER_TASKS_MANAGER[user_id] = asyncio.create_task(user_task_manager(user_id))

    # 将需要执行的数据放进待执行队列
    await USER_TASKS_QUEUES[user_id].put({"final_message":final_message,"url_list":url_list,"api":api,"character":character,"user_id":user_id})

async def core_send(final_message, url_list,api, character,user_id):
    # 获取ai回复
    ai_response = await ai_message(final_message,url_list, character,user_id)

    # 拆分分段回复
    for sentence in ai_response.split("。"):
        if sentence.strip():
            await api.post_private_msg(user_id, sentence.strip())
            try:
                insert_temp_memory(user_id, sentence.strip(), "bot")
            except Exception as e:
                print(f"Error inserting temp memory: {e}")
            await asyncio.sleep(1.5)  # 模拟打字间隔
    await manage_temp_memory(user_id)
    await manage_mid_memory(user_id)
async def schedule_task(user_id, api, character):
    """ 取消旧任务并启动新任务 """
    async with USER_TASKS_LOCK:
        if user_id in USER_TASKS:
            USER_TASKS[user_id].cancel()  # 取消旧任务
        task = asyncio.create_task(send_delayed_message(user_id, api, character))
        USER_TASKS[user_id] = task
