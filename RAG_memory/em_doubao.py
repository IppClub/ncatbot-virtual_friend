import configparser
import os
import requests
from volcenginesdkarkruntime import Ark
from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct

class DoubaoClient:
    def __init__(self, API_KEY):
        self.client=Ark(api_key=API_KEY)

    def get_embedding(self, text):
        # 请求 Volcengine API 获取嵌入向量
        resp = self.client.multimodal_embeddings.create(
            model="doubao-embedding-vision-241215",
            encoding_format="float",
            input=[{"text": text, "type": "text"}]
        )

        if hasattr(resp, "data") and resp.data:
            # 获取嵌入向量数据
            embedding = resp.data["embedding"]
            print("豆包正确返回向量")
            return embedding  # 假设返回第一个嵌入向量
        else:
            print("错误：未接收到嵌入数据")
            return None

# 配置文件读取
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH, encoding="utf-8")

DOUBAO_API_KEY = config.get("doubao", "API_KEY")

em_client=DoubaoClient(DOUBAO_API_KEY)
