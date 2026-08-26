def retrieve_relevant_memories(query: str, all_memories: list[str], top_k: int = 3) -> list[str]:
    """
    基于关键词重叠匹配检索最相关的记忆。

    方法：将查询和每条记忆按字符分词，计算重叠字符数量，排序返回 top_k。
    """
    if not all_memories:
        return []

    # 查询分词（字符级，适合中文）
    query_chars = set(list(query.replace(" ", "")))

    scored_memories = []
    for mem in all_memories:
        mem_chars = set(list(mem.replace(" ", "")))
        overlap = len(query_chars.intersection(mem_chars))
        scored_memories.append((overlap, mem))

    # 按重叠数降序排序
    scored_memories.sort(key=lambda x: x[0], reverse=True)

    # 提取 top_k 条（只取有重叠的）
    top_memories = [mem for score, mem in scored_memories[:top_k] if score > 0]

    # 如果不足 top_k 条，用无重叠的记忆补齐（保证返回数量）
    if len(top_memories) < top_k:
        remaining = [mem for _, mem in scored_memories if mem not in top_memories]
        top_memories.extend(remaining[:top_k - len(top_memories)])

    return top_memories