# 定义一个 OllamaClient 类
import configparser
import os
import requests

class OllamaClient:
    def __init__(self, base_url='http://127.0.0.1:11434'):
        self.base_url = base_url
        self.session = requests.Session()  # 创建一个 Session 来复用连接

    def get_embedding(self, text, model='bge-m3'):
        # 构造请求数据
        data = {
            "model": model,
            "input": text
        }
        # 向 Ollama 服务器发送请求
        response = self.session.post(f'{self.base_url}/api/embed', json=data)
        response.raise_for_status()  # 如果请求失败，抛出异常
        return response.json()['embeddings'][0]
    
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH,encoding="utf-8")

OLLAMA_BASE_URL = config.get("RAG_memory", "OLLAMA_BASE_URL")
ollama_client=OllamaClient(OLLAMA_BASE_URL)