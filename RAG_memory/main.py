import configparser
import os
from .em_ollama import ollama_client
from .qdrant import store_vector_in_qdrant,query_vector_in_qdrant,query_all_vectors_for_user,update_vector_in_qdrant,delete_all_vectors_for_user
from ..ai_utils.ai_helper import use_ai_raw,use_ai_output_json

from datetime import datetime

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

OPEN = config.get("RAG_memory", "OPEN")
SIMILARITY_THRESHOLD = config.getfloat("RAG_memory", "SIMILARITY_THRESHOLD")

CUSTOM_DUAL_FACT_PROMPT = f"""
# 角色定义
您是多角色对话分析专家，需要同时提取对话双方的事实信息，并自动将时间描述转换为ISO 8601格式日期。
注意不要遗漏任何时间相关描述，尤其是"昨天"、"今天"、"下周三"等模糊描述！！！

# 提取规则
## 核心要求
1. 每个事实条目必须包含：角色标识（user/bot）+事实描述，如果事实和时间相关才需要携带时间，否则不用
2. 时间优先参考每一条记忆携带的time，比如“you: 昨晚调试代码到凌晨三点，time:2025-04-07 10:14:07”，需要参考时间为2025-04-07 10:14:07
3. 时间格式统一为YYYY-MM-DD（含时间段时使用YYYY-MM-DD HH:MM格式）

## 时间处理策略
**当前基准日期**：{datetime.now().strftime("%Y-%m-%d")}
- 转换优先级：
  1. 绝对时间（如"2025年4月2日"）→ 2025-04-02
  2. 相对时间（如"下周三"）→ 根据记忆日期时间推算
  3. 模糊时间（如"三个月后"）→ 推算具体日期
  4. 时间段（如"下午三点到五点"）→ 15:00-17:00

# 输出规范
```json
{{
  "facts": [
    "user:在 2025-04-02 准备去爬山",
    "bot:在2025-04-02 建议用户多穿衣服" ,
    "user:喜欢吃蛋糕"
  ]
}}
"""

QUERY_PROMPT=f"""
请严格按以下步骤处理用户输入：
1. **时间检测**：识别所有时间表达式（绝对/相对/模糊）
2. **时间转换**：
   - 绝对时间 → 转为ISO 8601格式（YYYY-MM-DD[THH:mm]）
   - 相对时间 → 基于当前基准时间计算（当前：{datetime.now().strftime("%Y-%m-%d")}）
   - 时间段 → 转为ISO区间格式（HH:mm-HH:mm）
3. **语义保留**：保持原句结构，仅替换时间表达式
4. 如果原句没有时间描述直接返回原句内容

## 转换优先级
1. 精确时间点（如"下午3点半" → 15:30）
2. 日期范围（如"4-5月" → 2024-04-01~2024-05-31）
3. 模糊时段（如"明年初" → 2025-Q1）

直接返回转化完的字符串即可
"""

# 接收原始的多轮聊天记录，然后llm总结得到事实，事实向量化后存储到向量数据库
# TODO:考虑之后改成并发操作，提高速度
async def store_memory(messages, user_id):
    if OPEN != "true":
        return
    # ai总结
    prompt=CUSTOM_DUAL_FACT_PROMPT
    fact=await use_ai_output_json(prompt,messages)
    print(f"ai总结得到的事实原始格式为：{fact}")

    fact_list=fact["facts"]
    for f in fact_list:
        embedder_fact=ollama_client.get_embedding(f)
        # 找到最相符的一条数据（是否合理）
        similar_fact=query_vector_in_qdrant(embedder_fact,user_id=user_id,top_k=1)
        print(f"最相符的数据为：{similar_fact}")
        if similar_fact==[] or similar_fact[0].score<SIMILARITY_THRESHOLD:
            store_vector_in_qdrant(embedder_fact,f,user_id=user_id)
        
        else:
          prompt = f"""你是一个智能记忆管理系统，请判断用户的新记忆应该执行何种操作（ADD/UPDATE/NONE）：

            - 如果新记忆和旧记忆描述的是相同事实，但有补充或更准确内容，则选择 UPDATE。
            - 如果新记忆和旧记忆无关，则选择 ADD。
            - 如果内容重复或没有新信息，则选择 NONE。

            请严格只返回一个词：ADD、UPDATE 或 NONE。不要解释。

            最相似的旧记忆：{similar_fact[0].payload.get("content")}
            新记忆：{f}
            """
          
          action=await use_ai_raw(prompt,"")
          print(f"ai决定的操作为：{action}")

          if(action=="ADD"):
              store_vector_in_qdrant(embedder_fact,f,user_id=user_id)
          elif(action=="UPDATE"):
              vector_id=similar_fact[0].id
              update_vector_in_qdrant(vector_id,embedder_fact,f,user_id=user_id)
          else:
              pass

# 使用一句话和用户id查询相关的向量数据库中数据
async def query_memory(query, user_id):
    # ai转换时间
    prompt=QUERY_PROMPT
    query=await use_ai_raw(prompt,query)
    print(f"ai转换的查询语句为：{query}")
    # 向量查询
    query_vector=ollama_client.get_embedding(query)
    result=query_vector_in_qdrant(query_vector,user_id=user_id)
    return result

# 查询某一个用户的所有数据
async def query_all_memory(user_id):
    result=query_all_vectors_for_user(user_id)
    return result

# 删除某一个用户的所有数据
async def delete_all_memory(user_id):
    delete_all_vectors_for_user(user_id)