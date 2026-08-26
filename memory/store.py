import sqlite3
from datetime import datetime
from pathlib import Path

# 数据库固定放在项目根目录，避免因工作目录不同而建错位置
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "memory.db"

def get_db_connection():
    """创建并返回数据库连接"""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """
    初始化数据库，创建长期记忆表。
    表结构：id, fact, created_at
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS long_term_memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fact TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # 为 fact 字段创建索引，加速去重查询
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_fact ON long_term_memory (fact)")
    conn.commit()
    conn.close()
    print("数据库初始化完成。")

def add_fact(fact: str):
    """插入一条事实到长期记忆库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO long_term_memory (fact, created_at) VALUES (?, ?)",
                   (fact, datetime.now()))
    conn.commit()
    conn.close()

def get_all_facts():
    """返回所有事实列表（按时间倒序）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT fact FROM long_term_memory ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [row["fact"] for row in rows]

def fact_exists(fact: str):
    """检查事实是否已存在（精确匹配）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM long_term_memory WHERE fact = ? LIMIT 1", (fact,))
    result = cursor.fetchone()
    conn.close()
    return result is not None