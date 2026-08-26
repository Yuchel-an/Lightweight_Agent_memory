from config import client, MODEL_NAME


def generate_response(user_input: str, short_term_history: list[str], long_term_memories: list[str]) -> str:
    """
    调用 LLM 生成回答，注入短期记忆和长期记忆。
    """
    # 格式化长期记忆
    long_term_text = "\n".join([f"- {m}" for m in long_term_memories]) if long_term_memories else "（无）"

    # 格式化短期记忆
    short_term_text = "\n".join(short_term_history) if short_term_history else "（无）"

    # 构建 Prompt（严格按照手册模板）
    prompt = f"""你是一个有记忆的助手。

长期记忆（关于用户的事实）：
{long_term_text}

近期对话：
{short_term_text}

用户：{user_input}
回答："""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system",
                 "content": "你是一个有记忆的助手。根据提供的长期记忆和近期对话，自然地回答用户的问题。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        print(f"回答生成出错: {e}")
        return "抱歉，我暂时无法回答，请稍后再试。"