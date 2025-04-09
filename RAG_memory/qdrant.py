import configparser
import os
import time
import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from qdrant_client.http.models import Filter, FieldCondition, MatchValue

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

QDRANT_HOST = config.get("RAG_memory", "QDRANT_HOST")
QDRANT_PORT = config.get("RAG_memory", "QDRANT_PORT")

# 创建一个 QdrantClient 实例
qdrant_client = QdrantClient(host=QDRANT_HOST, port=QDRANT_PORT)
# 默认集合名
COLLECTION_NAME = "ollama_bge_my"

# 存储向量和对应文本内容
def store_vector_in_qdrant(vector, content, user_id):

    # 确保集合存在
    create_collection_if_not_exists()

    # 创建UUID
    vector_id = str(uuid.uuid4())
    
    # 创建 PointStruct 对象
    point = PointStruct(id=vector_id, vector=vector,payload={"user_id":user_id,"content":content})  # 确保向量是列表类型
    # 将向量存储到 Qdrant
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point],

    )


# 使用向量查询文本内容（带 user_id 过滤）
def query_vector_in_qdrant(query_vector, user_id, top_k=5):
    create_collection_if_not_exists()

    query_result = qdrant_client.search(
        collection_name=COLLECTION_NAME,
        query_vector=query_vector,
        limit=top_k,
        with_payload=True,
        query_filter=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )
    )
    return query_result


# 查询某个 user_id 的所有向量数据（不使用向量查询）
def query_all_vectors_for_user(user_id):
    create_collection_if_not_exists()
    # 使用 scroll 而不是 search，可以拿到所有满足条件的数据
    all_points = []
    scroll_offset = None

    while True:
        result, scroll_offset = qdrant_client.scroll(
            collection_name=COLLECTION_NAME,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="user_id",
                        match=MatchValue(value=user_id)
                    )
                ]
            ),
            with_payload=True,
            with_vectors=False,
            offset=scroll_offset,
            limit=100  # 一次最多返回 100 个，可以调大调小
        )

        all_points.extend(result)

        if scroll_offset is None:
            break  # 没有更多了

    return all_points

# 检查集合是否存在，如果不存在就创建
def create_collection_if_not_exists(collection_name=COLLECTION_NAME):
    collections = qdrant_client.get_collections()
    existing_names = {col.name.lower(): col.name for col in collections.collections}
    if collection_name not in existing_names:
        # 设置向量参数
        vectors_config = VectorParams(
            size=1024,  # 根据你的嵌入向量的大小选择合适的尺寸
            distance=Distance.COSINE  # 使用余弦相似度作为距离度量
        )

        # 创建集合
        qdrant_client.create_collection(
            collection_name=collection_name,
            vectors_config=vectors_config  # 传递向量配置
        )
    else:
        pass

# 使用向量id更新已有记忆
def update_vector_in_qdrant(vector_id, vector, content, user_id):
    point = PointStruct(
        id=vector_id,
        vector=vector,
        payload={
            "user_id": user_id,
            "content": content
        }
    )

    # 使用 upsert：更新或插入向量
    qdrant_client.upsert(
        collection_name=COLLECTION_NAME,
        points=[point]
    )

# 删除某一个user_id的所有向量数据
def delete_all_vectors_for_user(user_id):
    qdrant_client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="user_id",
                    match=MatchValue(value=user_id)
                )
            ]
        )
    )