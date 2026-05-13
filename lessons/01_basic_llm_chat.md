# Lesson 01  -  Talking to a Model

# 第 01 课 —— 与模型对话

## What Question Are We Answering?

## 我们在回答什么问题？

**"How do I talk to a language model at all?"**

**"我该如何与语言模型对话？"**

This is the absolute foundation. Before we can build agents, we need to understand the simplest possible interaction: text in, text out.

这是绝对的基础。在构建智能体之前，我们需要理解最简单的交互方式：文本输入，文本输出。

## What You Will Build

## 你将构建什么

A minimal interaction that:
- Loads a local LLM
- Sends text to it
- Receives text back

一个最简交互，它能：
- 加载本地 LLM
- 向其发送文本
- 接收返回的文本

That's it. No magic. No frameworks. Just the basics.

就这些。没有魔法，没有框架，只有基础知识。

## New Concepts Introduced

## 引入的新概念

### 1. Prompts

### 1. 提示词（Prompts）

A **prompt** is just text you send to the model. It can be a question like "What is an AI agent?", an instruction like "Explain quantum computing", or a request like "Write a poem about the ocean". The model completes or responds to this text based on patterns it learned during training.

**提示词**就是你发送给模型的文本。它可以是一个问题，如"什么是 AI 智能体？"，一个指令，如"解释量子计算"，或者一个请求，如"写一首关于海洋的诗"。模型根据训练时学到的模式来完成或响应这段文本。

### 2. Tokens

### 2. 词元（Tokens）

Models don't see text as words - they see **tokens**. Tokens are pieces of text (often words or subwords). For example, "Hello world" might be 2 tokens, while "artificial intelligence" could be 2-4 tokens depending on the model.

模型看到的不是单词，而是**词元**。词元是文本片段（通常是单词或子词）。例如，"Hello world"可能是 2 个词元，而"artificial intelligence"根据模型不同可能是 2-4 个词元。

This matters because models have token limits (context windows), generation is measured in tokens per second, and longer prompts use more tokens, leaving less room for responses.

这很重要，因为模型有词元限制（上下文窗口），生成速度以每秒词元数衡量，较长的提示词会使用更多词元，从而为响应留下更少空间。

### 3. Context

### 3. 上下文（Context）

The **context** is everything the model can "see" at once. It includes your prompt, any previous conversation, and system instructions. Models have a **context window** (e.g., 2048 tokens). If you exceed it, the model can't see the earlier text.

**上下文**是模型能够一次"看到"的所有内容。它包括你的提示词、任何之前的对话以及系统指令。模型有一个**上下文窗口**（例如 2048 个词元）。如果超出它，模型就看不到之前的文本了。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No system prompts ([Lesson 02](02_system_prompt.md))
- No structured outputs ([Lesson 03](03_structured_output.md))
- No tools ([Lesson 05](05_tools.md))
- No agents ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))

- 无系统提示词（[第 02 课](02_system_prompt.md)）
- 无结构化输出（[第 03 课](03_structured_output.md)）
- 无工具（[第 05 课](05_tools.md)）
- 无智能体（[第 06 课](06_agent_loop.md)）
- 无记忆（[第 07 课](07_memory.md)）

This lesson is intentionally minimal.

本课有意保持最简。

## The Code

## 代码

Look at `agent/agent.py`, see `simple_generate()` method:

查看 `agent/agent.py`，参见 `simple_generate()` 方法：

```python
def simple_generate(self, user_input: str) -> str:
    """
    Simplest possible interaction - just pass text to the LLM.
    """
    return self.llm.generate(user_input)
```

That's it. One line. No complexity.

就这些。一行代码。没有复杂性。

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_01_basic_chat()` method:

查看 `complete_example.py`，参见 `lesson_01_basic_chat()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

response = agent.simple_generate("What is an AI agent?")
print(response)
```

## What's Happening Internally?

## 内部发生了什么？

1. Your text is converted to tokens
2. Tokens are sent to the model
3. The model predicts the next token
4. Repeat until a stop condition (end token, max length, etc.)
5. Tokens are converted back to text
6. Text is returned to you

1. 你的文本被转换为词元
2. 词元被发送给模型
3. 模型预测下一个词元
4. 重复，直到满足停止条件（结束词元、最大长度等）
5. 词元被转换回文本
6. 文本返回给你

## Key Insights

## 关键见解

### There is No "Understanding"

### 没有"理解"

The model doesn't "understand" your question. Instead, it recognizes patterns in the tokens, predicts likely continuations, and generates probabilistic text. This is important: **models are pattern matchers, not minds.**

模型不"理解"你的问题。相反，它识别词元中的模式，预测可能的延续，并生成概率性文本。这很重要：**模型是模式匹配器，而不是思维。**

### It's Probabilistic

### 它是概率性的

Run the same prompt twice and you might get different responses. This happens because models use randomness (temperature) in generation, and multiple plausible continuations exist. There's no single "correct" answer - just probabilistic outputs.

用同一个提示词运行两次可能会得到不同的响应。这是因为模型在生成时使用了随机性（temperature），并且存在多种合理的延续。没有单一的"正确"答案——只有概率性输出。

### Text In = Text Out

### 文本输入 = 文本输出

That's all this is. Everything else we build (agents, tools, memory) is built on top of this simple foundation.

这就是全部。我们构建的其他一切（智能体、工具、记忆）都建立在这个简单的基础之上。

## Common Issues

## 常见问题

**"The response is cut off"**
- Increase `max_tokens` in `shared/llm.py`

**"响应被截断了"**
- 增加 `shared/llm.py` 中的 `max_tokens`

**"The model repeats itself"**
- This is normal for completion models
- We'll fix it with better prompting in [Lesson 02](02_system_prompt.md)

**"模型在重复自己"**
- 这对于补全模型来说是正常现象
- 我们将在[第 02 课](02_system_prompt.md)中通过更好的提示词来解决这个问题

**"The response doesn't match the prompt"**
- Some models need specific formatting
- We'll add structure in [Lesson 02](02_system_prompt.md) and [Lesson 03](03_structured_output.md)

**"响应与提示词不匹配"**
- 某些模型需要特定的格式
- 我们将在[第 02 课](02_system_prompt.md)和[第 03 课](03_structured_output.md)中添加结构

## Exercises

## 练习

1. Try different prompts and observe the responses
2. Change the `temperature` in `shared/llm.py` (0.0 = deterministic, 1.0 = creative)
3. Use `max_tokens` to control response length

1. 尝试不同的提示词并观察响应
2. 修改 `shared/llm.py` 中的 `temperature`（0.0 = 确定性，1.0 = 创造性）
3. 使用 `max_tokens` 控制响应长度

## What's Next?

## 下一步是什么？

In [Lesson 02](02_system_prompt.md), we'll add a **system prompt** to shape the model's behavior. This turns random completions into consistent, useful responses.

在[第 02 课](02_system_prompt.md)中，我们将添加一个**系统提示词**来塑造模型的行为。这将把随机的补全变成一致的、有用的响应。

---

**Key Takeaway:** An LLM is just a text completion engine. Everything we build is structured interaction with this simple mechanism.

**关键要点：** LLM 只是一个文本补全引擎。我们构建的一切都是与这个简单机制的结构化交互。