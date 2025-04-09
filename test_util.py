'''
RAG_memory 测试工具
'''
import asyncio
import configparser
import json
import os
import time
from .RAG_memory.main import query_memory, store_memory,query_all_memory,delete_all_memory

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "./"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

user_id = config.getint("host", "USER_ID")
async def search_all_data():
    """查询全部用户数据"""
    results = await query_all_memory(user_id)
    print("\n[查询结果]:", results)


async def insert_data(text):
    """插入用户数据"""
    await store_memory(text, user_id)
    print("\n[插入成功]:", text)

async def search_data(text):
    """查询匹配的用户数据"""
    results = await query_memory(text, user_id)
    print("\n[查询结果]:", results)

async def delete_data():
    """删除用户数据"""
    await delete_all_memory(user_id)
    print("\n[删除成功]")

async def main():
    while True:
        print("\n===== RAG_memory 测试工具 =====")
        print("1. 查询全部用户数据")
        print("2. 插入用户数据")
        print("3. 查询用户数据")
        print("4. 删除用户全部数据")
        print("5. 退出程序")
        choice = input("请选择操作: ")

        if choice == "1":
            await search_all_data()
        elif choice == "2":
            text = input("请输入要插入的文本: ")
            await insert_data(text)
        elif choice == "3":
            text = input("请输入查询关键词: ")
            await search_data(text)
        elif choice == "4":
            await delete_data()
        elif choice == "5":
            print("退出程序...")
            break
        else:
            print("无效输入，请重新选择！")

if __name__ == "__main__":
    # 运行异步 main 函数
    asyncio.run(main())