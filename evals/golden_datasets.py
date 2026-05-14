"""
Golden Datasets for Agent Evals.

智能体评估的黄金数据集。

Golden datasets are known-good test cases that must always pass.
They are version controlled alongside prompts - when you change a prompt,
you run the golden dataset to make sure you didn't break anything.

黄金数据集是必须始终通过的已知正确测试用例。
它们与提示词一起进行版本控制——当你更改提示词时，
运行黄金数据集以确保你没有破坏任何内容。

Why "golden"?
- These are your source of truth
- If a golden case fails, the agent is broken (not the test)
- They cover both happy paths AND edge cases

为什么叫"黄金"？
- 这些是你的真相来源
- 如果一个黄金用例失败，那是智能体出了问题（不是测试）
- 它们覆盖了快乐路径和边缘情况
"""

# ============================================================
# STRUCTURED OUTPUT GOLDEN DATASET
# 结构化输出黄金数据集
# Tests: JSON parsing, schema compliance
# 测试：JSON 解析、模式合规性
# 
# NOTE: Schemas use multi-line format with examples for clarity.
# Single-line schemas often confuse models.
# 注意：模式使用带示例的多行格式以增加清晰度。
# 单行模式通常会使模型感到困惑。
# ============================================================

STRUCTURED_OUTPUT_GOLDEN = [
    # Happy path: standard question
    # 快乐路径：标准问题
    {
        "input": "Explain quantum computing in one sentence",
        "schema": """{
  "topic": "the topic name as a string",
  "difficulty": "beginner" or "intermediate" or "advanced"
}

Example: {"topic": "machine learning", "difficulty": "intermediate"}""",
        "must_have_fields": ["topic", "difficulty"]
    },
    # Happy path: simple question
    # 快乐路径：简单问题
    {
        "input": "What is Python in one sentence?",
        "schema": """{
  "topic": "the topic name as a string",
  "difficulty": "beginner" or "intermediate" or "advanced"
}

Example: {"topic": "web development", "difficulty": "beginner"}""",
        "must_have_fields": ["topic", "difficulty"]
    },
    # Edge case: question with numbers
    # 边缘情况：含数字的问题
    {
        "input": "What is the significance of 42?",
        "schema": """{
  "answer": "your answer as a string"
}

Example: {"answer": "It is the meaning of life"}""",
        "must_have_fields": ["answer"]
    },
    # Edge case: question with special characters
    # 边缘情况：含特殊字符的问题
    {
        "input": "What does hello world mean in programming?",
        "schema": """{
  "explanation": "your explanation as a string"
}

Example: {"explanation": "It is a simple test program"}""",
        "must_have_fields": ["explanation"]
    },
]


# ============================================================
# TOOL CALL GOLDEN DATASET
# 工具调用黄金数据集
# Tests: Correct tool selection, valid arguments
# 测试：正确的工具选择、有效的参数
# ============================================================

TOOL_CALL_GOLDEN = [
    # Happy path: multiplication
    # 快乐路径：乘法
    {
        "input": "What is 42 * 7?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "multiply"}
    },
    # Happy path: addition
    # 快乐路径：加法
    {
        "input": "Calculate 100 + 50",
        "expected_tool": "calculator",
        "expected_args": {"operation": "add"}
    },
    # Happy path: division
    # 快乐路径：除法
    {
        "input": "What is 100 / 5?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "divide"}
    },
    # Happy path: subtraction
    # 快乐路径：减法
    {
        "input": "What's 50 minus 25?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "subtract"}
    },
    # Edge case: word problem
    # 边缘情况：文字应用题
    {
        "input": "If I have 15 apples and buy 27 more, how many do I have?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "add"}
    },
]


# ============================================================
# DECISION GOLDEN DATASET
# 决策黄金数据集
# Tests: Correct routing based on input
# 测试：基于输入的正确路由
# ============================================================

DECISION_GOLDEN = [
    # Clear summarization request
    # 明确的摘要请求
    {
        "input": "Can you summarize this article for me?",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "summarize_text"
    },
    # Clear translation request
    # 明确的翻译请求
    {
        "input": "Translate 'hello' to Spanish",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "translate"
    },
    # Clear question
    # 明确的问题
    {
        "input": "What is the capital of France?",
        "choices": ["answer_question", "summarize_text", "translate"],
        "expected": "answer_question"
    },
    # Calculate vs answer
    # 计算与回答
    {
        "input": "What is 5 + 5?",
        "choices": ["answer_question", "calculate", "search"],
        "expected": "calculate"
    },
]


# ============================================================
# MEMORY GOLDEN DATASET
# 记忆黄金数据集
# Tests: Store → Retrieve cycle
# 测试：存储 → 检索循环
# ============================================================

MEMORY_GOLDEN = [
    # Name storage and recall
    # 姓名存储和回忆
    {
        "store_input": "My name is Alice",
        "query_input": "What's my name?",
        "expected_in_response": "Alice"
    },
    # Preference storage and recall
    # 偏好存储和回忆
    {
        "store_input": "I prefer dark mode",
        "query_input": "What's my preference for display mode?",
        "expected_in_response": "dark"
    },
    # Location storage and recall
    # 位置存储和回忆
    {
        "store_input": "I live in New York",
        "query_input": "Where do I live?",
        "expected_in_response": "New York"
    },
]


# ============================================================
# EDGE CASES GOLDEN DATASET
# 边缘情况黄金数据集
# Tests: Boundary conditions that often break prompts
# 测试：经常破坏提示词的边界条件
# ============================================================

EDGE_CASES_GOLDEN = {
    "empty_input": {
        "structured": {
            "input": "Respond with a greeting",
            "schema": '{"response": "your response"}\n\nExample: {"response": "Hello!"}',
            "must_have_fields": ["response"]
        }
    },
    "very_long_input": {
        "structured": {
            "input": "Summarize: " + "very " * 20 + "complex topic",
            "schema": '{"summary": "brief summary"}\n\nExample: {"summary": "A complex topic"}',
            "must_have_fields": ["summary"]
        }
    },
    "unicode_input": {
        "structured": {
            "input": "What does hello mean in Chinese?",
            "schema": '{"translation": "the translation"}\n\nExample: {"translation": "你好"}',
            "must_have_fields": ["translation"]
        }
    },
    "json_in_input": {
        "structured": {
            "input": "What format is this: key value pairs?",
            "schema": '{"parsed": "your answer"}\n\nExample: {"parsed": "dictionary"}',
            "must_have_fields": ["parsed"]
        }
    },
}
