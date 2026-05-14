# Lesson 05  -  Introducing Tools 

# 第 05 课 —— 引入工具

## What Question Are We Answering?

## 我们在回答什么问题？

**"Can the model ask me to do something?"**

**"模型能请求我去做某事吗？"**

Tools extend the agent's capabilities beyond text generation. Instead of only generating text, the agent can request actions like calculations, API calls, or file operations.

工具将智能体的能力扩展到文本生成之外。智能体不再只是生成文本，还可以请求执行计算、API 调用或文件操作等行动。

## What You Will Build

## 你将构建什么

A tool-calling system that:
- Lets the agent request specific tools with structured parameters
- Validates tool requests before execution
- Separates tool requests from tool execution
- Extends agent capabilities without retraining the model

一个工具调用系统，它能：
- 让智能体使用结构化参数请求特定工具
- 在执行前验证工具请求
- 将工具请求与工具执行分离
- 无需重新训练模型就能扩展智能体能力

## New Concepts Introduced

## 引入的新概念

### 1. Tool Interfaces

### 1. 工具接口

A **tool interface** is a defined API the agent can request. Tools have names and parameters, like `calculator(a, b, operation)`. The agent requests the tool, but the system executes it.

**工具接口**是智能体可以请求的定义好的 API。工具有名称和参数，如 `calculator(a, b, operation)`。智能体请求工具，但由系统执行它。

This separation is critical - the agent **describes** what it needs, but you **control** what actually happens.

这种分离至关重要——智能体**描述**它需要什么，但你**控制**实际发生的事情。

### 2. Structured Tool Calls

### 2. 结构化工具调用

Tool calls are **structured JSON specifications** for function calls. The model outputs JSON like `{"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}`, and your code validates and executes it.

工具调用是函数调用的**结构化 JSON 规范**。模型输出 JSON 如 `{"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}`，你的代码验证并执行它。

This is similar to Lesson 04's decision making, but instead of choosing an action, the agent is specifying a function call.

这类似于第 04 课的决策制定，但智能体不是选择一个行动，而是指定一个函数调用。

### 3. Model-Chosen Actions

### 3. 模型选择的行动

The agent decides **which tool to use** and **what parameters to pass**. You define available tools, but the agent chooses which one fits the situation.

智能体决定**使用哪个工具**以及**传递什么参数**。你定义可用的工具，但智能体选择哪个适合当前情况。

This is agency at work - the agent is selecting and configuring actions.

这就是智能体性的体现——智能体在选择和配置行动。

## Important Rule

## 重要规则

The model **requests** tools. The system **executes** them. No autonomy yet. This separation gives you control and safety.

模型**请求**工具。系统**执行**它们。目前还没有自主性。这种分离给了你控制权和安全性。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No agent loop ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))
- No automatic tool execution - you still manually execute tool calls

- 无智能体循环（[第 06 课](06_agent_loop.md)）
- 无记忆（[第 07 课](07_memory.md)）
- 无自动工具执行——你仍然手动执行工具调用

## The Code

## 代码

Look at `agent/agent.py`, see `request_tool()` method:

查看 `agent/agent.py`，参见 `request_tool()` 方法：

```python
def request_tool(self, user_input: str) -> dict | None:
    """
    Have the model request a tool call.
    
    Lesson 05 version.
    
    Args:
        user_input: The user's request
        
    Returns:
        Tool call specification or None if request failed
    """
    prompt = f"""{self.system_prompt}

You are a tool-calling assistant. When asked a math question, you must respond with ONLY valid JSON.

Available tool: calculator
- Parameters: a (number), b (number), operation ("add", "subtract", "multiply", or "divide")

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Example format:
{{"tool": "calculator", "arguments": {{"a": 42, "b": 7, "operation": "multiply"}}}}

User request: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "tool" in parsed and "arguments" in parsed:
            return parsed
    
    return None

def execute_tool_call(self, tool_call: dict) -> Any:
    """
    Execute a tool call requested by the model.
    
    Args:
        tool_call: Dictionary with "tool" and "arguments"
        
    Returns:
        Result of the tool execution
    """
    return execute_tool(tool_call["tool"], tool_call["arguments"])
```

Notice:
- **Structured output** - The tool call is validated JSON, similar to Lesson 03
- **Validation** - We check that both "tool" and "arguments" are present
- **Separation of concerns** - Request and execution are separate methods
- **Extensibility** - Easy to add new tools without changing the model

注意：
- **结构化输出** - 工具调用是经过验证的 JSON，类似于第 03 课
- **验证** - 我们检查"tool"和"arguments"是否都存在
- **关注点分离** - 请求和执行是独立的方法
- **可扩展性** - 无需更改模型即可轻松添加新工具

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_05_tools()` method:

查看 `complete_example.py`，参见 `lesson_05_tools()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

tool_call = agent.request_tool("What is 42 * 7?")
print(f"Tool request: {tool_call}")

if tool_call:
    result = agent.execute_tool_call(tool_call)
    print(f"Tool result: {result}")
```

![Tool Calling Flow](diagrams/lesson-05-tool-calling.png)

## Compare to Lesson 04

## 与第 04 课的对比

**Lesson 04 (Decision Making):**
```
Input: "What should I do?"
Choices: ["answer", "calculate", "translate"]
Output: "calculate"
```
The agent picks from a list of actions.

**第 04 课（决策制定）：**
```
输入："What should I do?"
选择：["answer", "calculate", "translate"]
输出："calculate"
```
智能体从行动列表中选择。

**Lesson 05 (Tool Calling):**
```
Input: "What is 42 * 7?"
Tool: calculator
Arguments: {"a": 42, "b": 7, "operation": "multiply"}
Result: 294
```
The agent specifies a tool call with parameters and gets a result.

**第 05 课（工具调用）：**
```
输入："What is 42 * 7?"
工具：calculator
参数：{"a": 42, "b": 7, "operation": "multiply"}
结果：294
```
智能体指定带参数的工具调用并获得结果。

## Key Insights

## 关键见解

### Tools Are Interfaces, Not Abilities

### 工具是接口，不是能力

The agent doesn't have the ability - you do. The agent describes what it needs through a structured interface, and you provide the implementation. This keeps you in control.

智能体没有这种能力——你有。智能体通过结构化接口描述它需要什么，你提供实现。这让你保持控制权。

### No Retraining Required

### 无需重新训练

To add new capabilities, you add new tools. The model doesn't need retraining - it just needs to understand the tool interface. This is powerful.

要添加新能力，你添加新工具。模型不需要重新训练——它只需要理解工具接口。这很强大。

### Safety Through Separation

### 通过分离实现安全

By separating tool requests from execution, you can validate, log, and control what actually happens. The agent can't execute dangerous operations without your code allowing it.

通过将工具请求与执行分离，你可以验证、记录和控制实际发生的事情。没有你的代码允许，智能体就无法执行危险操作。

### Structured = Reliable

### 结构化 = 可靠

Using the same structured JSON pattern from Lessons 03 and 04 makes tool calls reliable and parseable. The model outputs structured data, you validate it, then execute.

使用与第 03 课和第 04 课相同的结构化 JSON 模式使工具调用可靠且可解析。模型输出结构化数据，你验证它，然后执行。

## Common Issues

## 常见问题

**"The model requests a tool that doesn't exist"**
- Validate the tool name against your available tools
- Provide clear examples of available tools in the prompt
- Handle invalid tool names gracefully

**"模型请求了一个不存在的工具"**
- 针对你可用的工具验证工具名称
- 在提示词中提供可用工具的清晰示例
- 优雅地处理无效工具名称

**"The arguments are the wrong type"**
- Validate argument types before execution
- Make the expected types clear in the tool description
- Consider using schema validation for complex tools

**"参数类型不对"**
- 在执行前验证参数类型
- 在工具描述中明确预期类型
- 考虑对复杂工具使用模式验证

**"The model doesn't request a tool when it should"**
- Make it clear when tools should be used
- Provide examples in the prompt
- Consider making tool use mandatory for certain request types

**"模型在应该请求工具的时候没有请求"**
- 明确说明工具应该在什么时候使用
- 在提示词中提供示例
- 考虑对某些请求类型强制使用工具

## Exercises

## 练习

1. Add a new tool (e.g., "weather" or "search") and test it
2. Try invalid tool calls and see how validation handles them
3. Modify the tool interface and see how the model adapts
4. Create tools with different parameter types (strings, numbers, booleans)

---

1. 添加一个新工具（例如"weather"或"search"）并测试它
2. 尝试无效的工具调用，看看验证如何处理它们
3. 修改工具接口，看看模型如何适应
4. 创建具有不同参数类型（字符串、数字、布尔值）的工具

## What's Next?

## 下一步是什么？

In [Lesson 06](06_agent_loop.md), we'll create the **agent loop** - putting decision making and tool calling together into a repeating cycle.

在[第 06 课](06_agent_loop.md)中，我们将创建**智能体循环** —— 将决策制定和工具调用放入一个重复循环中。

---

**Key Takeaway:** Tool calling = expanding capabilities without retraining. Tools are interfaces you control, not abilities the agent has.

**关键要点：** 工具调用 = 无需重新训练即可扩展能力。工具是你控制的接口，而不是智能体拥有的能力。