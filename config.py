import os
from openai import OpenAI
from dotenv import load_dotenv

# 从 .env 文件加载环境变量（可选，方便本地开发）
load_dotenv()

# 用户需设置环境变量 DEEPSEEK_API_KEY 或在下方直接填写
# 获取方式：export DEEPSEEK_API_KEY="sk-你的key" 或在下方硬编码
API_KEY = os.getenv("DEEPSEEK_API_KEY", "sk-你的key")
BASE_URL = ""  # 智谱 GLM 兼容 OpenAI 格式，openai SDK 会自动拼接 /chat/completions
MODEL_NAME = ""  # 或 qwen-turbo

# 创建 OpenAI 兼容客户端
client = OpenAI(api_key=API_KEY, base_url=BASE_URL)