# Lesson 07  -  Memory (Short and Long)

# 第 07 课 —— 记忆（短期与长期）

## What Question Are We Answering?

## 我们在回答什么问题？

**"How does an agent remember things?"**

**"智能体如何记住事物？"**

Agents need to remember information across multiple interactions. Without memory, each conversation starts from scratch. Memory lets agents build on previous conversations and maintain context.

智能体需要跨多次交互记住信息。没有记忆，每次对话都从零开始。记忆让智能体能够在之前的对话基础上构建并保持上下文。

## What You Will Build

## 你将构建什么

A memory system that:
- Stores facts across interactions
- Retrieves relevant memories when needed
- Integrates memory into the agent's context
- Allows explicit memory management

一个记忆系统，它能：
- 跨交互存储事实
- 在需要时检索相关记忆
- 将记忆整合到智能体的上下文中
- 允许显式记忆管理

## New Concepts Introduced

## 引入的新概念

### 1. Context vs Memory

### 1. 上下文与记忆

**Context** is what's in the current prompt - everything the model can see right now. **Memory** is persistent storage that survives across interactions.

**上下文**是当前提示词中的内容——模型现在能看到的一切。**记忆**是跨交互保持存在的持久化存储。

Context is temporary. Memory persists. Memory gets loaded into context when needed.

上下文是临时的。记忆会持久存在。记忆在需要时被加载到上下文中。

### 2. Persistence

### 2. 持久性

**Persistence** means saving facts across turns. When a user says "My name is Alice," that fact should be stored and available in future interactions.

**持久性**意味着在多轮交互中保存事实。当用户说"我的名字是 Alice"时，这个事实应该被存储，并在未来的交互中可用。

Without persistence, the agent forgets everything after each interaction.

没有持久性，智能体在每次交互后都会遗忘一切。

### 3. Retrieval

### 3. 检索

**Retrieval** is getting relevant memories when needed. When the user asks "What's my name?", the agent retrieves "User's name is Alice" from memory and uses it to respond.

**检索**是在需要时获取相关记忆。当用户问"我叫什么名字？"时，智能体从记忆中检索"用户的名字是 Alice"并用它来响应。

Simple retrieval might mean "get all memories." More sophisticated retrieval finds relevant memories based on the current query.

简单的检索可能意味着"获取所有记忆"。更复杂的检索则根据当前查询找到相关记忆。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No planning ([Lesson 08](08_planning.md))
- No sophisticated memory retrieval - just simple "get all" retrieval
- No memory decay or prioritization

- 无规划（[第 08 课](08_planning.md)）
- 无复杂的记忆检索——只是简单的"获取全部"检索
- 无记忆衰减或优先级排序

## The Code

## 代码

Look at `agent/agent.py`, see `run_with_memory()` method:

查看 `agent/agent.py`，参见 `run_with_memory()` 方法：

```python
def run_with_memory(self, user_input: str) -> dict | None:
    """
    Run agent with memory context.
    
    Lesson 07 version.
    
    Args:
        user_input: User's input
        
    Returns:
        Response with potential memory update
    """
    memory_context = self.memory.get_all()
    
    # Build memory context string
    # 构建记忆上下文字符串
    if memory_context:
        memory_str = "You remember the following:\n" + "\n".join(f"- {item}" for item in memory_context)
    else:
        memory_str = "You have no memories yet."
    
    prompt = f"""{self.system_prompt}

You are an agent with memory. You must respond with ONLY valid JSON.

{memory_str}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}
4. If the user tells you information (like their name), save it to memory
5. If the user asks about something you remember, USE YOUR MEMORY to answer

Required JSON format:
{{"reply": "your response text", "save_to_memory": "fact to remember" or null}}

Examples:
- User says "My name is Alice" -> {{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}}
- User asks "What's my name?" and you remember "User's name is Alice" -> {{"reply": "Your name is Alice", "save_to_memory": null}}

User input: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "reply" in parsed:
            # Save to memory if requested
            # 如果需要，保存到记忆
            if parsed.get("save_to_memory"):
                self.memory.add(parsed["save_to_memory"])
            
            self.state.increment_step()
            return parsed
    
    return None
```

Notice:
- **Memory retrieval** - `memory.get_all()` loads all stored memories
- **Context integration** - Memories are included in the prompt
- **Explicit storage** - The agent explicitly says what to save via JSON
- **Automatic persistence** - When `save_to_memory` is provided, it's automatically stored

注意：
- **记忆检索** - `memory.get_all()` 加载所有存储的记忆
- **上下文集成** - 记忆被包含在提示词中
- **显式存储** - 智能体通过 JSON 明确说明要保存什么
- **自动持久化** - 当提供 `save_to_memory` 时，它会自动存储

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_07_memory()` method:

查看 `complete_example.py`，参见 `lesson_07_memory()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# First interaction - store name
# 第一次交互——存储名字
response1 = agent.run_with_memory("My name is Alice")
if response1 and "reply" in response1:
    print(f"Response 1: {response1['reply']}")

# Second interaction - recall name
# 第二次交互——回忆名字
response2 = agent.run_with_memory("What's my name?")
if response2 and "reply" in response2:
    print(f"Response 2: {response2['reply']}")

print(f"Memory contents: {agent.memory.get_all()}")
```

![Memory System](diagrams/lesson-07-memory.png)

## Compare to Lesson 06

## 与第 06 课的对比

**Lesson 06 (Agent Loop):**
```
Loop -> Step 1 -> Step 2 -> Step 3 -> Done
         |         |        |
       Action   Action   Action
```
State persists within the loop but resets when the loop ends.

**第 06 课（智能体循环）：**
```
循环 -> 步骤 1 -> 步骤 2 -> 步骤 3 -> 完成
          |           |          |
        行动         行动        行动
```
状态在循环内持续存在，但在循环结束时重置。

**Lesson 07 (Memory):**
```
Interaction 1 -> Save "name is Alice" -> Memory stores it
Interaction 2 -> Load memory -> "Your name is Alice"
```
Memory persists across completely separate interactions.

**第 07 课（记忆）：**
```
交互 1 -> 保存"名字是 Alice" -> 记忆存储它
交互 2 -> 加载记忆 -> "你的名字是 Alice"
```
记忆跨完全独立的交互持续存在。

## Key Insights

## 关键见解

### Memory is Explicit Storage

### 记忆是显式存储

Memory is **explicit storage**, not consciousness. It's data you can inspect, modify, and delete. There's no hidden reasoning - just stored facts.

记忆是**显式存储**，而不是意识。它是你可以检查、修改和删除的数据。没有隐藏的推理——只是存储的事实。

### Simple is Powerful

### 简单即强大

This memory system is simple: store strings, retrieve all of them. Yet it's incredibly useful. More sophisticated retrieval can come later, but this foundation works.

这个记忆系统很简单：存储字符串，检索所有字符串。然而它非常有用。更复杂的检索可以在之后加入，但这个基础是有效的。

### The Agent Controls Storage

### 智能体控制存储

The agent decides what to save via the `save_to_memory` field. You could automate this, but explicit control keeps things predictable.

智能体通过 `save_to_memory` 字段决定保存什么。你可以自动化这个过程，但显式控制使事情保持可预测。

### Context Loading

### 上下文加载

Memories are loaded into the prompt context. The model doesn't have direct access to memory - it only sees what you include in the prompt.

记忆被加载到提示词上下文中。模型没有直接访问记忆的权限——它只看到你在提示词中包含的内容。

## Common Issues

## 常见问题

**"The agent doesn't save information"**
- Check that the response includes `save_to_memory`
- Verify the memory.add() is being called
- Make sure the prompt clearly explains when to save

**"智能体不保存信息"**
- 检查响应是否包含 `save_to_memory`
- 验证 memory.add() 是否被调用
- 确保提示词清楚地解释了何时保存

**"The agent forgets things"**
- Verify memory is being loaded into the prompt
- Check that memory persists across calls
- Ensure the memory context string is being included

**"智能体忘记了事情"**
- 验证记忆是否被加载到提示词中
- 检查记忆是否在调用之间持续存在
- 确保记忆上下文字符串被包含

**"Memory gets too large"**
- This simple system stores all memories forever
- Consider adding memory limits or deletion
- More sophisticated systems can prioritize or summarize memories

**"记忆变得太大"**
- 这个简单系统永久存储所有记忆
- 考虑添加记忆限制或删除功能
- 更复杂的系统可以对记忆进行优先级排序或总结

## Exercises

## 练习

1. Save multiple facts and see how they accumulate
2. Try asking about something not in memory
3. Manually inspect `agent.memory.get_all()` to see stored data
4. Modify the memory format and see how it affects behavior

1. 保存多个事实并查看它们如何累积
2. 尝试询问不在记忆中的事物
3. 手动检查 `agent.memory.get_all()` 以查看存储的数据
4. 修改记忆格式并查看它如何影响行为

## What's Next?

## 下一步是什么？

In [Lesson 08](08_planning.md), we'll add **planning** - the ability to break down complex goals into a sequence of steps.

在[第 08 课](08_planning.md)中，我们将添加**规划** —— 将复杂目标分解为一系列步骤的能力。

---

**Key Takeaway:** Memory = data storage, not thoughts. It's explicit, inspectable, and gives agents continuity across interactions.

**关键要点：** 记忆 = 数据存储，而非思想。它是显式的、可检查的，并赋予智能体跨交互的连续性。
