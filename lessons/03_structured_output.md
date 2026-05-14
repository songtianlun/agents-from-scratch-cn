# Lesson 03  -  Making Output Reliable

# 第 03 课 —— 让输出变得可靠

## What Question Are We Answering?

## 我们在回答什么问题？

**"How do I stop parsing free-text?"**

**"我如何摆脱解析自由文本的困境？"**

Free-text responses are unpredictable. Sometimes the model adds explanations, sometimes it uses different formats, sometimes it hallucinates. We need **structure**.

自由文本响应是不可预测的。有时模型会添加解释，有时使用不同的格式，有时会出现幻觉。我们需要**结构**。

## What You Will Build

## 你将构建什么

A system that:
- Forces JSON output
- Validates the response
- Retries on failure

一个能够：
- 强制输出 JSON
- 验证响应
- 失败时重试

的系统。

## New Concepts Introduced

## 引入的新概念

### 1. Output Contracts

### 1. 输出契约（Output Contracts）

An **output contract** is a specification for what the model must return. Instead of "answer the question," we say "return JSON matching this schema."

**输出契约**是对模型必须返回内容的规范。我们不说"回答问题"，而是说"返回符合此模式的 JSON"。

```json
{
  "answer": string,
  "confidence": "high" | "medium" | "low"
}
```

### 2. Trust Boundaries

### 2. 信任边界

Never trust LLM output directly. Always:
1. Parse it
2. Validate it
3. Handle failures

永远不要直接信任 LLM 的输出。始终：
1. 解析它
2. 验证它
3. 处理失败情况

This is the first "engineering" moment - treating the LLM as a fallible component.

这是第一个"工程化"时刻——将 LLM 视为一个可能出错的组件。

### 3. Validation

### 3. 验证

Validation ensures the output matches your contract:
- Is it valid JSON?
- Does it have required fields?
- Are the values the right type?

验证确保输出符合你的契约：
- 它是有效的 JSON 吗？
- 它有必填字段吗？
- 值的类型正确吗？

## The Code

## 代码

Look at `agent/agent.py`, see `generate_structured()` method:

查看 `agent/agent.py`，参见 `generate_structured()` 方法：

```python
def generate_structured(self, user_input: str, schema: str) -> dict | None:
    """
    Generate structured JSON output with validation and retries.
    
    Lesson 03 version.
    
    Args:
        user_input: The user's question or request
        schema: JSON schema description
        
    Returns:
        Parsed JSON dictionary or None if all retries failed
    """
    prompt = f"""{self.system_prompt}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no extra text before or after the JSON
3. Start your response with {{ and end with }}

Schema you must follow:
{schema}

User request: {user_input}

Response (JSON only):"""
    
    # Try up to 3 times
    # 最多尝试 3 次
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed is not None:
            return parsed
    
    return None
```

Notice we've added:
- **Strong instructions** - "CRITICAL INSTRUCTIONS" with explicit JSON-only requirements
- **Temperature control** - `temperature=0.0` for more deterministic, consistent output
- **JSON extraction** - `extract_json_from_text()` handles cases where the model adds extra text
- **Retry logic** - Up to 3 attempts to get valid JSON, turning probabilistic behavior into reliable results

注意我们添加了：
- **强指令** - 带有明确仅限 JSON 要求的"CRITICAL INSTRUCTIONS"
- **温度控制** - `temperature=0.0` 获得更确定性、更一致的输出
- **JSON 提取** - `extract_json_from_text()` 处理模型添加额外文本的情况
- **重试逻辑** - 最多 3 次尝试获取有效 JSON，将概率性行为转变为可靠结果

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_03_structured()` method:

查看 `complete_example.py`，参见 `lesson_03_structured()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

schema = '''
{
  "topic": string,
  "difficulty": "beginner" | "intermediate" | "advanced"
}
'''

result = agent.generate_structured(
    "Explain quantum computing",
    schema
)

print(result)
# {"topic": "'quantum computing", "difficulty": "advanced"}
```

## Why This Matters

## 为什么这很重要

### Before (Free Text)

### 之前（自由文本）

```
Output: "Okay! This task is medium difficulty. I'd suggest building..."
```
- Can't parse
- Inconsistent
- Unreliable

- 无法解析
- 不一致
- 不可靠

### After (Structured)

### 之后（结构化）

```
Output: {'topic': 'quantum computing', 'difficulty': 'advanced'}
```
- Parseable
- Predictable
- Validated

- 可解析
- 可预测
- 经过验证

## Key Insights

## 关键见解

### LLMs Are Probabilistic

### LLM 是概率性的

They don't always output valid JSON on the first try. Retries turn probabilistic behavior into reliable behavior.

它们不总是在第一次尝试时输出有效的 JSON。重试将概率性行为转变为可靠行为。

### Structure Beats Cleverness

### 结构胜过巧妙

A simple prompt with validation beats a clever prompt without it.

带有验证的简单提示词胜过没有验证的巧妙提示词。

### This is Engineering

### 这是工程化

You're treating the LLM as a component in a system:
- Input: prompt + schema
- Output: validated data or error
- Retry: if validation fails

你将 LLM 视为系统中的一个组件：
- 输入：提示词 + 模式
- 输出：验证后的数据或错误
- 重试：如果验证失败

## Common Issues

## 常见问题

**"The model adds explanations before JSON"**
- Use `extract_json_from_text()` helper (finds JSON in text)
- Emphasize "ONLY valid JSON" in prompt

**"模型在 JSON 前添加了解释"**
- 使用 `extract_json_from_text()` 辅助函数（在文本中查找 JSON）
- 在提示词中强调"仅限有效 JSON"

**"Still getting invalid responses"**
- Lower temperature for more deterministic output
- Be more specific about the schema
- Use models trained for structured output

**"仍然收到无效响应"**
- 降低温度以获得更确定性的输出
- 更具体地描述模式
- 使用为结构化输出训练的模型

**"Retries use too many tokens"**
- 3 retries is usually enough
- Track retry counts to monitor model quality

**"重试使用了太多词元"**
- 3 次重试通常已足够
- 跟踪重试次数以监控模型质量

## What's Next?

## 下一步是什么？

In [Lesson 04](04_decision_making.md), we add **decision making** - the model chooses actions, not just answers questions.

在[第 04 课](04_decision_making.md)中，我们添加**决策制定** —— 模型选择行动，而不仅仅是回答问题。

---

**Key Takeaway:** Structured outputs + validation = reliable agents.

**关键要点：** 结构化输出 + 验证 = 可靠的智能体。