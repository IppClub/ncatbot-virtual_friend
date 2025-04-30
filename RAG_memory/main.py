import configparser
import os
from .em_doubao import em_client
from .qdrant_for_doubao import store_vector_in_qdrant,query_vector_in_qdrant,query_all_vectors_for_user,update_vector_in_qdrant,delete_all_vectors_for_user
from ..ai_utils.ai_helper import use_ai_raw_reasoner,use_ai_raw_chat
from .prompt import CUSTOM_DUAL_FACT_PROMPT,QUERY_PROMPT

from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

OPEN = config.get("RAG_memory", "OPEN")
SIMILARITY_THRESHOLD = config.getfloat("RAG_memory", "SIMILARITY_THRESHOLD")

# 接收原始的多轮聊天记录，然后llm总结得到事实，事实向量化后存储到向量数据库
# TODO:考虑之后改成并发操作，提高速度
async def store_memory(messages, user_id):
    if OPEN != "true":
        return
    # ai总结
    prompt=CUSTOM_DUAL_FACT_PROMPT
    fact=await use_ai_raw_reasoner(prompt,messages)
    print(f"ai总结得到的事实原始格式为：{fact}")

    # 把输出结果按"。"分割变成一个list
    fact_list = [s for s in fact.split("。") if s]

    for f in fact_list:
        embedder_fact=em_client.get_embedding(f)
        # 找到最相符的一条数据（是否合理）
        similar_fact=query_vector_in_qdrant(embedder_fact,user_id=user_id,top_k=1)
        print(f"最相符的数据为：{similar_fact}")
        if not similar_fact or len(similar_fact) == 0 or similar_fact[0].score < SIMILARITY_THRESHOLD:
            store_vector_in_qdrant(embedder_fact, f, user_id=user_id)
        
        else:
          prompt = f"""你是一个智能记忆管理系统，请判断用户的新记忆应该执行何种操作（ADD/UPDATE/NONE）：

            - 如果新记忆和旧记忆描述的是相同事实，但有补充或更准确内容，则选择 UPDATE。
            - 如果新记忆和旧记忆无关，则选择 ADD。
            - 如果内容重复或没有新信息，则选择 NONE。

            请严格只返回一个词：ADD、UPDATE 或 NONE。不要解释。

            最相似的旧记忆：{similar_fact[0].payload.get("content")}
            新记忆：{f}
            """
          
          action=await use_ai_raw_chat(prompt,"")
          print(f"ai决定的操作为：{action}")

          if(action=="ADD"):
              store_vector_in_qdrant(embedder_fact,f,user_id=user_id)
          elif(action=="UPDATE"):
              vector_id=similar_fact[0].id
              update_vector_in_qdrant(vector_id,embedder_fact,f,user_id=user_id)
          else:
              pass

# 使用一句话和用户id查询相关的向量数据库中数据
async def query_memory(query, user_id,number_of_results=5):
    # ai转换时间
    prompt=QUERY_PROMPT
    query=await use_ai_raw_chat(prompt,query)
    print(f"ai转换的查询语句为：{query}")
    # 向量查询
    query_vector=em_client.get_embedding(query)
    result=query_vector_in_qdrant(query_vector,user_id=user_id,top_k=number_of_results)
    return result

# 查询某一个用户的所有数据
async def query_all_memory(user_id):
    result=query_all_vectors_for_user(user_id)
    return result

# 删除某一个用户的所有数据
async def delete_all_memory(user_id):
    delete_all_vectors_for_user(user_id)