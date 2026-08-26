from config import client, MODEL_NAME


def extract_facts(conversation_history: list[str]) -> list[str]:
    """
    从对话历史中（最近 2-3 轮）抽取事实。

    输入：对话历史字符串列表，如 ["User: ...", "Assistant: ..."]
    输出：事实字符串列表，每条事实是一句简短的话
    """
    if not conversation_history:
        return []

    # 将对话历史拼接为文本
    history_text = "\n".join(conversation_history)

    # 构建 Prompt（严格按照手册要求）
    prompt = f"""从以下对话中抽取用户提到的事实（偏好、姓名、年龄、计划、重要事件）。
每条事实用一句话描述。
如果没有新事实，返回空列表。
输出格式：每行一条事实，不要编号，不要其他废话。

对话历史：
{history_text}

抽取的事实："""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "你是一个事实抽取助手。只输出抽取的事实，每行一条，不要编号。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,  # 低温度保证格式稳定
            max_tokens=200
        )

        content = response.choices[0].message.content.strip()
        if not content:
            return []

        # 按行分割，过滤空行，清理可能的列表符号
        facts = [line.strip().lstrip("- •") for line in content.split("\n") if line.strip()]
        return facts

    except Exception as e:
        print(f"❌ 事实抽取出错: {e}")
        return []