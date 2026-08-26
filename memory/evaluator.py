from memory.store import get_all_facts

# 关键词加权列表（包含这些词的事实直接存储）
PRIORITY_KEYWORDS = ["喜欢", "讨厌", "计划", "叫", "岁", "去", "参加", "名字", "开心", "快乐", "痛"]


def _similarity_check(new_fact: str, existing_fact: str) -> bool:
    """
    简单的关键词重叠去重（字符级）。
    如果重叠字符数 / 新事实字符数 > 80%，认为语义相似。
    """
    new_chars = set(new_fact.replace(" ", ""))
    exist_chars = set(existing_fact.replace(" ", ""))

    if not new_chars or not exist_chars:
        return False

    overlap = new_chars.intersection(exist_chars)
    overlap_ratio = len(overlap) / len(new_chars)
    return overlap_ratio > 0.8


def should_store_fact(fact: str) -> bool:
    """
    根据规则判断是否将事实存入长期记忆。

    规则：
    1. 长度过滤：< 2 个字符不存（中文事实通常很短，"16岁""喜欢编程"等应入库）
    2. 关键词加权：包含优先词直接存储
    3. 去重：与已有记忆重叠 > 80% 不存
    4. 其他情况默认存储
    """
    # 规则 1：长度过滤
    if len(fact) < 2:
        return False

    # 规则 2：关键词加权（直接存储）
    for kw in PRIORITY_KEYWORDS:
        if kw in fact:
            return True

    # 规则 3：去重检查
    existing_facts = get_all_facts()
    for exist_fact in existing_facts:
        if _similarity_check(fact, exist_fact):
            return False  # 相似，丢弃

    # 规则 4：默认存储
    return True