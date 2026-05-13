# Lesson 02  -  Giving the Model a Role

# 第 02 课 —— 赋予模型一个角色

## What Question Are We Answering?

## 我们在回答什么问题？

**"Why does the same model behave differently?"**

**"为什么同一个模型会表现出不同的行为？"**

You've probably noticed that LLMs can act like different personas - technical expert, creative writer, helpful assistant. How does that work?

你可能已经注意到，LLM 可以扮演不同的角色——技术专家、创意写手、贴心助理。这是如何做到的？

## What You Will Build

## 你将构建什么

A script that uses **system prompts** to:
- Assign the model a specific role
- Stabilize its behavior
- Control tone and format

一个使用**系统提示词**的脚本，用于：
- 为模型指定一个特定角色
- 稳定其行为
- 控制语气和格式

## New Concepts Introduced

## 引入的新概念

### 1. System Prompts

### 1. 系统提示词（System Prompts）

A **system prompt** is an instruction that shapes how the model responds. It's like giving someone a role before a conversation.

**系统提示词**是一条指令，用于塑造模型的响应方式。就像在对话前给某人指定一个角色。

Example system prompts:
```
"You are a calm, precise teacher who explains concepts simply."
```

```
"You are a creative writer who uses vivid imagery."
```

```
"You are a code reviewer who finds bugs and suggests improvements."
```

示例系统提示词：
```
"You are a calm, precise teacher who explains concepts simply."
（你是一位冷静、精确的老师，能用简单的语言解释概念。）
```

```
"You are a creative writer who uses vivid imagery."
（你是一位使用生动意象的创意写手。）
```

```
"You are a code reviewer who finds bugs and suggests improvements."
（你是一位能发现缺陷并提出改进建议的代码审查者。）
```

### 2. Instruction Hierarchy

### 2. 指令层级

Most models understand this hierarchy:
1. **System prompt** - Overall behavior and role
2. **User prompt** - The actual question or request

大多数模型理解以下层级：
1. **系统提示词** - 整体行为和角色
2. **用户提示词** - 实际的问题或请求

The system prompt has higher "priority" - it guides how the model interprets the user prompt.

系统提示词具有更高的"优先级"——它指导模型如何解释用户提示词。

### 3. Behavior Shaping

### 3. 行为塑造

Behavior ≠ intelligence. Behavior = instructions.

行为 ≠ 智能。行为 = 指令。

The same model can:
- Be technical or casual (tone)
- Be verbose or concise (length)
- Be creative or factual (style)

同一个模型可以：
- 技术性的或随意的（语气）
- 详细的或简洁的（长度）
- 创造性的或基于事实的（风格）

All based on the system prompt.

这一切都基于系统提示词。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No structured outputs ([Lesson 03](03_structured_output.md))
- No decisions ([Lesson 04](04_decision_making.md))
- No tools ([Lesson 05](05_tools.md))
- No memory ([Lesson 07](07_memory.md))

- 无结构化输出（[第 03 课](03_structured_output.md)）
- 无决策（[第 04 课](04_decision_making.md)）
- 无工具（[第 05 课](05_tools.md)）
- 无记忆（[第 07 课](07_memory.md)）

## The Code

## 代码

Look at `agent/agent.py`, see `generate_with_role()` method:

查看 `agent/agent.py`，参见 `generate_with_role()` 方法：

```python
def generate_with_role(self, user_input: str) -> str:
    """
    Generate with a system prompt to shape behavior.
    """
    # Use a format that doesn't confuse the model
    # 使用不会让模型困惑的格式
    prompt = f"""{self.system_prompt}

User: {user_input}
Assistant:"""
    
    response = self.llm.generate(prompt)
    # Clean up any potential tag artifacts
    # 清除可能出现的标签残留
    response = response.replace('<SYSTEM>', '').replace('</SYSTEM>', '')
    response = response.replace('<USER>', '').replace('</USER>', '')
    return response.strip()
```

Notice we've added:
- The system prompt at the beginning
- A simple "User:" / "Assistant:" format for the conversation
- Cleanup code to remove any tag artifacts that might appear

注意我们添加了：
- 开头的系统提示词
- 对话的简单 "User:" / "Assistant:" 格式
- 用于删除可能出现的标签残留的清理代码

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_02_with_role()` method:

查看 `complete_example.py`，参见 `lesson_02_with_role()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# The agent has a default system prompt:
# "You are a calm, precise, and helpful AI assistant..."
# 智能体有一个默认的系统提示词：
# "你是一个冷静、精确且有帮助的 AI 助手..."

response = agent.generate_with_role("What is an AI agent?")
print(response)
```

## Compare to Lesson 01

## 与第 01 课的对比

**Without system prompt ([Lesson 01](01_basic_llm_chat.md)):**
```
Input: "What is an AI agent?"
Output: "An AI agent is a system that perceives its environment and acts autonomously to achieve specified goals. It processes information, makes decisions, and can adapt to changing conditions using machine learning algorithms..."
```

**不使用系统提示词（[第 01 课](01_basic_llm_chat.md)）：**
```
输入："What is an AI agent?"
输出："An AI agent is a system that perceives its environment and acts autonomously to achieve specified goals. It processes information, makes decisions, and can adapt to changing conditions using machine learning algorithms..."
（AI 智能体是一个能感知环境并自主行动以实现特定目标的系统。它处理信息、做出决策，并能使用机器学习算法适应变化的条件……）
```

**With system prompt:**
```
Input: "What is an AI agent?"
Output: "Think of an AI agent as a helpful assistant that can observe what's happening around it and take actions to help you accomplish tasks. Like how a thermostat watches the temperature and adjusts heating automatically - but much more sophisticated."
```

**使用系统提示词：**
```
输入："What is an AI agent?"
输出："Think of an AI agent as a helpful assistant that can observe what's happening around it and take actions to help you accomplish tasks. Like how a thermostat watches the temperature and adjusts heating automatically - but much more sophisticated."
（把 AI 智能体想象成一个有帮助的助手，它可以观察周围发生的事情并采取行动帮助你完成任务。就像温控器监测温度并自动调节暖气一样——但要复杂得多。）
```

Same question. Same model. Different behavior.

相同的问题。相同的模型。不同的行为。

## The Power of System Prompts

## 系统提示词的力量

### Example 1: Technical Expert
```python
agent.system_prompt = "You are a senior software engineer who explains concepts with code examples."
```

### 示例 1：技术专家
```python
agent.system_prompt = "You are a senior software engineer who explains concepts with code examples."
# 你是一位用代码示例解释概念的高级软件工程师。
```

### Example 2: ELI5 (Explain Like I'm 5)
```python
agent.system_prompt = "You explain complex topics using simple words and everyday analogies."
```

### 示例 2：用孩子能懂的方式解释
```python
agent.system_prompt = "You explain complex topics using simple words and everyday analogies."
# 你用简单的词汇和日常类比来解释复杂的话题。
```

### Example 3: Concise Responder
```python
agent.system_prompt = "You give accurate answers in 1-2 sentences maximum. No elaboration unless asked."
```

### 示例 3：简洁回答者
```python
agent.system_prompt = "You give accurate answers in 1-2 sentences maximum. No elaboration unless asked."
# 你用最多 1-2 句话给出准确的答案。除非被要求，否则不做详细阐述。
```

## Key Insights

## 关键见解

### Behavior is Configurable

### 行为是可配置的

You're not changing the model - you're changing the **constraints** on its output. The model still predicts tokens; the system prompt just shifts probabilities.

你没有改变模型——你在改变其输出的**约束条件**。模型仍然在预测词元；系统提示词只是改变了概率分布。

### Consistency Improves

### 一致性提升

Without a system prompt, the model might be:
- Formal one response, casual the next
- Verbose sometimes, terse other times
- Inconsistent in tone

没有系统提示词，模型可能会：
- 一次正式，下次随意
- 有时详细，有时简短
- 语气不一致

A system prompt creates **behavioral consistency**.

系统提示词创造了**行为一致性**。

### Still Probabilistic

### 仍然是概率性的

Even with a system prompt, responses vary. But they vary **within the constraints** you set.

即使有了系统提示词，响应仍然会变化。但它们会在你设定的**约束范围内**变化。

## Common System Prompt Patterns

## 常见系统提示词模式

### 1. Role Definition
```
You are a [role] who [behavior].
```

### 1. 角色定义
```
你是一个 [角色]，具有 [行为] 特征。
```

### 2. Constraint Setting
```
You must [requirement]. You never [prohibition].
```

### 2. 约束设定
```
你必须 [要求]。你永远不 [禁止事项]。
```

### 3. Output Format
```
Always respond with [format]. Use [style].
```

### 3. 输出格式
```
始终以 [格式] 响应。使用 [风格]。
```

### 4. Combination
```
You are a helpful assistant. 
You explain concepts clearly using examples.
You keep responses under 100 words unless asked to elaborate.
```

### 4. 组合
```
你是一个有帮助的助手。
你用示例清晰地解释概念。
你的回答保持在 100 字以内，除非被要求详细阐述。
```

## Common Issues

## 常见问题

**"The model ignores my system prompt"**
- Some models follow system prompts better than others
- Try being more explicit and specific
- Use stronger language ("You MUST..." instead of "Try to...")

**"模型忽略了我的系统提示词"**
- 某些模型比其他模型更好地遵循系统提示词
- 尝试更明确和具体
- 使用更强烈的语言（用"You MUST..."而不是"Try to..."）

**"Responses are still inconsistent"**
- This is normal - LLMs are probabilistic
- Lower the `temperature` for more consistency
- We'll add validation in [Lesson 03](03_structured_output.md)

**"响应仍然不一致"**
- 这是正常的——LLM 是概率性的
- 降低 `temperature` 以获得更高的一致性
- 我们将在[第 03 课](03_structured_output.md)中添加验证

**"The system prompt is too long"**
- Keep it under 100-200 words
- More tokens = less room for user input + response

**"系统提示词太长了"**
- 保持在 100-200 字以内
- 词元越多 = 用户输入 + 响应的空间越少

## Exercises

## 练习

1. Try different system prompts and observe behavior changes
2. Create a system prompt that makes responses extremely concise
3. Create a system prompt that makes responses highly detailed
4. Experiment with conflicting instructions (what wins?)

1. 尝试不同的系统提示词并观察行为变化
2. 创建一个使响应极其简洁的系统提示词
3. 创建一个使响应非常详细的系统提示词
4. 用冲突的指令进行实验（谁赢了？）

## What's Next?

## 下一步是什么？

In [Lesson 03](03_structured_output.md), we'll add **structured outputs** to make responses reliable and parseable. Instead of free text, we'll get validated JSON.

在[第 03 课](03_structured_output.md)中，我们将添加**结构化输出**，使响应可靠且可解析。我们将得到经过验证的 JSON，而不是自由文本。

---

**Key Takeaway:** Behavior is not intelligence. It's constraints. System prompts turn a general model into a specific assistant.

**关键要点：** 行为不是智能。它是约束。系统提示词将通用模型变成特定的助手。