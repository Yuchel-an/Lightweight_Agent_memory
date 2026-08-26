from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse, FileResponse
import uvicorn
import os
import sys
from pathlib import Path

# 项目根目录（基于本文件定位，保证从任何目录运行都能正常工作）
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR))

# 导入记忆和 Agent 模块
from memory.store import init_db, add_fact, get_all_facts
from memory.extractor import extract_facts
from memory.evaluator import should_store_fact
from memory.retriever import retrieve_relevant_memories
from agent.responder import generate_response

# 初始化 FastAPI 应用
app = FastAPI(title="Agent 记忆系统 MVP")

# 挂载静态文件目录（前端 HTML/CSS/JS）
STATIC_DIR = BASE_DIR / "static"
if not STATIC_DIR.exists():
    STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


# ==================== 启动事件 ====================
@app.on_event("startup")
async def startup_event():
    """服务启动时初始化数据库"""
    init_db()
    print("轻量  Agent 记忆系统启动完成！")
    print("访问http://localhost:8000")


# ==================== 全局状态 ====================
# 短期记忆：最近 6 条消息（3轮对话），重启即清空
short_term_memory = []
MAX_SHORT_TERM = 6


# ==================== API 路由 ====================
@app.post("/chat")
async def chat_endpoint(request: Request):
    """
    核心聊天接口：执行完整流程（抽取 → 评估 → 存储 → 召回 → 回答）
    """
    global short_term_memory

    data = await request.json()
    user_message = data.get("message", "")

    if not user_message:
        return JSONResponse(content={"error": "消息不能为空"}, status_code=400)

    # 1. 将用户消息加入短期记忆
    short_term_memory.append(f"User: {user_message}")

    # 2. 事实抽取（传入最近 4 条对话作为上下文）
    context = short_term_memory[-4:] if len(short_term_memory) >= 4 else short_term_memory
    extracted_facts = extract_facts(context)

    # 3. 记忆评估与存储
    new_memories = []
    for fact in extracted_facts:
        if should_store_fact(fact):
            add_fact(fact)
            new_memories.append(fact)

    # 4. 记忆召回（从所有长期记忆中检索 top 3）
    all_facts = get_all_facts()
    retrieved_memories = retrieve_relevant_memories(user_message, all_facts, top_k=3)

    # 5. 回答生成（LLM + 短期记忆 + 召回的长期记忆）
    reply = generate_response(user_message, short_term_memory, retrieved_memories)

    # 6. 将助手回答加入短期记忆
    short_term_memory.append(f"Assistant: {reply}")

    # 7. 修剪短期记忆（保持最多 6 条）
    if len(short_term_memory) > MAX_SHORT_TERM:
        short_term_memory = short_term_memory[-MAX_SHORT_TERM:]

    # 8. 返回 JSON 结果（前端用于更新面板）
    return JSONResponse(content={
        "reply": reply,
        "extracted_facts": extracted_facts,
        "new_memories": new_memories,
        "retrieved_memories": retrieved_memories,
        "short_term": short_term_memory
    })


@app.get("/memories")
async def get_memories():
    """返回所有长期记忆（用于前端展示）"""
    facts = get_all_facts()
    return JSONResponse(content={"memories": facts})


@app.delete("/memories")
async def clear_memories():
    """清空所有长期记忆 + 短期记忆（演讲前重置用）"""
    from memory.store import get_db_connection
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM long_term_memory")
    conn.commit()
    conn.close()

    # 同时清空短期记忆
    global short_term_memory
    short_term_memory.clear()

    return JSONResponse(content={"message": "记忆已清空，可以重新开始 Demo！"})


@app.get("/")
async def read_root():
    """根路径返回前端页面"""
    return FileResponse(str(STATIC_DIR / "index.html"))


# ==================== 本地运行入口 ====================
if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)