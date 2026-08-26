# Lightweight_Agent_memory

给你写了一个标准、干净、适合 GitHub 展示的 README.md，中英文混排风格偏技术文档，直接复制到项目根目录即可：

markdown
# 🧠 Agent Structured Memory System — MVP Demo


![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-green)
![License](https://img.shields.io/badge/license-MIT-yellow)

---

## ✨ 核心特性

- **双层记忆架构**：短期记忆（最近 5-6 轮对话，存内存）+ 长期记忆（SQLite 持久化）
- **LLM 事实抽取**：自动从对话中提取用户偏好、计划、身份等关键事实
- **规则评估器**：基于关键词加权 + 字符重叠去重，决定是否写入长期记忆（无模型依赖，零额外开销）
- **关键词召回**：字符级重叠匹配，从长期记忆中检索最相关的 Top-3 条
- **记忆注入回答**：LLM 生成回答时同时感知短期上下文和长期用户画像
- **Live Demo 就绪**：极简前端实时展示每一步记忆变化，演讲可直接用

---

## 🏗️ 系统架构

用户输入

│

▼

┌────────────────────────────────────────────┐

│            FastAPI 后端                     │

│                                            │

│  1. 短期记忆：最近 5-6 轮对话（列表存内存）│

│  2. 事实抽取器：LLM 从最新对话抽取事实     │

│  3. 记忆评估器：规则判断是否写入长期记忆   │

│  4. 长期记忆库：SQLite（id, fact, time）  │

│  5. 记忆召回：关键词匹配检索相关长期记忆   │

│  6. 回答生成：LLM + 短期记忆 + 召回的长期 │

└────────────────────────────────────────────┘

│

▼

返回回答 + 记忆面板更新数据（JSON）

纯文本
---

## 📁 项目结构

agent_memory_demo/

├── main.py              # FastAPI 入口，串联所有模块

├── config.py            # LLM API 配置（兼容 OpenAI 格式）

├── requirements.txt     # Python 依赖

├── memory.db            # 运行时自动生成（SQLite）

│

├── memory/

│   ├── init.py

│   ├── extractor.py     # 事实抽取（调用 LLM）

│   ├── evaluator.py     # 记忆评估（纯规则）

│   ├── store.py         # SQLite 读写

│   └── retriever.py     # 记忆召回（关键词匹配）

│

├── agent/

│   ├── init.py

│   └── responder.py     # 回答生成（LLM + 记忆注入）

│

└── static/

├── index.html       # 前端页面

├── style.css        # 样式（白底黑字极简风）

└── app.js           # 前后端交互逻辑

纯文本
---

## 🛠️ 技术栈

| 组件 | 选型 | 理由 |
|------|------|------|
| 后端框架 | FastAPI | 轻量、热重载、自带 API 文档 |
| 数据库 | SQLite | 零配置，单文件，不需要额外服务 |
| LLM 接口 | OpenAI 兼容格式 | 可切换 DeepSeek / Qwen / 智谱 GLM 等 |
| 前端 | 单页 HTML + CSS + 原生 JS | 一个文件搞定，无构建工具 |
| 记忆检索 | 关键词重叠匹配 | 简单有效，后续可升级为向量搜索 |

---

## 🚀 快速开始

### 1. 克隆项目

bash

git clone https://github.com/your-username/agent-memory-demo.git

cd agent-memory-demo

纯文本
### 2. 安装依赖

bash

pip install -r requirements.txt

纯文本
### 3. 配置 LLM API

编辑 `config.py`，填入你的 API Key 和对应服务地址：

python

DeepSeek（默认）

API_KEY = "sk-你的deepseek_key"

BASE_URL = "https://api.deepseek.com
"

MODEL_NAME = "deepseek-chat"

或 智谱 GLM
API_KEY = "你的智谱_key"
BASE_URL = "https://open.bigmodel.cn/api/paas/v4
"
MODEL_NAME = "glm-4-flash"
或 Qwen
BASE_URL = "https://dashscope.aliyuncs.com/compatible-mode/v1
"
MODEL_NAME = "qwen-turbo"
纯文本
> 也支持通过环境变量传入，避免硬编码：
> ```bash
> export DEEPSEEK_API_KEY="sk-你的key"
> ```

### 4. 启动服务

bash

uvicorn main:app --reload

纯文本
浏览器打开 **http://localhost:8000** 即可看到 Demo 界面。

API 文档地址：**http://localhost:8000/docs**

---

## 🎬 Demo 剧本（演讲用）

| 轮次 | 用户输入               | 预期系统行为 |
|------|--------------------|-------------|
| 1 | *"我叫an，20岁，喜欢学习AI变成，休闲的程序员穿搭。"* | 抽取事实 → 写入长期记忆 |
| 2 | *"我周五要去xx参加演讲。"*   | 抽取事实 → 写入长期记忆 |
| 3 | *"那我该穿什么？"*        | 召回"喜欢港风穿搭" + "周五深圳演讲" → 建议穿港风米白针织衫 |

> 💡 演讲前可点击前端"清空记忆"按钮重置所有状态。

---

## 📡 API 端点

| 方法 | 路径 | 说明 |
|------|------|------|
| `POST` | `/chat` | 发送消息，执行完整记忆流程，返回回答 + 记忆状态 |
| `GET` | `/memories` | 获取所有长期记忆列表 |
| `DELETE` | `/memories` | 清空所有长期记忆 + 短期记忆 |
| `GET` | `/` | 返回前端页面 |
| `GET` | `/docs` | 自动生成的 Swagger API 文档 |

### `/chat` 请求/响应示例

**请求：**

json

{ "message": "我叫an，20岁，喜欢小狗" }

纯文本
**响应：**

json

{

"reply": "你好an！喜欢小狗很可爱呢 ， 以后我会记住你的喜好的。",

"extracted_facts": ["用户叫an", "an20岁", "an喜欢小狗"],

"new_memories": ["用户叫an", "an20岁", "an喜欢小狗"],

"retrieved_memories": [],

"short_term": ["User: 我叫an，20岁，喜欢小狗", "Assistant: 你好an！..."]

}

纯文本
---

## ⚠️ 设计约束

本项目是一个 **MVP 演示原型**，刻意做了以下简化：

- ✅ **不使用** JEPA / 预测误差 / 世界模型等算法（那是后续研究方向）
- ✅ **不使用** 向量数据库、LangChain 等重框架
- ✅ **不使用** 任何前端构建工具（Node.js/npm）
- ✅ 记忆评估完全基于**规则**（关键词 + 字符重叠），保证可解释性和演讲效果
- ✅ 检索采用字符级重叠匹配，后续可平滑升级为 Embedding + 向量检索

---

## 🗺️ 后续扩展方向

- [ ] 用 Embedding 向量替换关键词匹配，提升召回质量
- [ ] 增加记忆遗忘机制（时间衰减 / 重要性衰减）
- [ ] 记忆冲突检测与合并（如用户改了名字）
- [ ] 多用户隔离（Session 管理）
- [ ] 记忆可视化时间线

---

## 📝 License

[MIT](LICENSE)

---

## 运行main.py后,访问http://localhost:8000
