import configparser
import os
import requests

class OllamaClient:
    def __init__(self, base_url='http://127.0.0.1:11434'):
        self.base_url = base_url
        self.session = requests.Session()

    def _model_exists(self, model_name):
        """检查模型是否已下载"""
        try:
            response = self.session.get(f'{self.base_url}/api/tags')
            response.raise_for_status()
            models = response.json().get("models", [])
            return any(model['name'] == model_name or model['name'] == model_name + ":latest"for model in models)
        except Exception as e:
            print(f"[模型检查失败] {e}")
            return False

    def _pull_model(self, model_name):
        """下载模型"""
        print(f"[拉取模型] 正在下载模型 '{model_name}'，请稍候...")
        response = self.session.post(f'{self.base_url}/api/pull', json={"name": model_name})
        for line in response.iter_lines(decode_unicode=True):
            if line:
                print(line)

    def ensure_model_ready(self, model_name):
        """确保模型已准备好，没有则自动拉取"""
        if not self._model_exists(model_name):
            self._pull_model(model_name)

    def get_embedding(self, text, model='bge-m3'):
        self.ensure_model_ready(model)

        data = {
            "model": model,
            "input": text
        }
        response = self.session.post(f'{self.base_url}/api/embed', json=data)
        response.raise_for_status()
        return response.json()['embeddings'][0]

# 配置文件读取
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))  
CONFIG_FILE_PATH = os.path.join(BASE_DIR, "settings.ini")

config = configparser.ConfigParser()
config.read(CONFIG_FILE_PATH, encoding="utf-8")

OLLAMA_BASE_URL = config.get("RAG_memory", "OLLAMA_BASE_URL")

# 创建 Ollama 客户端
ollama_client = OllamaClient(OLLAMA_BASE_URL)
