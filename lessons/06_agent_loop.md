# Lesson 06  -  The Agent Loop

# 第 06 课 —— 智能体循环

## What Question Are We Answering?

## 我们在回答什么问题？

**"How does this become an agent instead of a chatbot?"**

**"这如何变成智能体而不是聊天机器人？"**

Answer: When it can **observe, decide, act, and repeat**, with state. A chatbot responds once and stops. An agent takes multiple steps toward a goal.

回答：当它能够**带着状态地观察、决策、行动并重复**时。聊天机器人响应一次就停止了。智能体会向目标迈出多个步骤。

## What You Will Build

## 你将构建什么

An agent loop that:
- Runs multiple steps in sequence
- Maintains state across steps
- Decides actions based on current state
- Terminates when the goal is reached or max steps exceeded

一个能够：
- 按顺序运行多个步骤
- 在步骤间保持状态
- 根据当前状态决定行动
- 在达到目标或超过最大步骤数时终止

的智能体循环。

## New Concepts Introduced

## 引入的新概念

### 1. Agent Loop

### 1. 智能体循环

The **agent loop** is the repeating cycle: observe, decide, act. Each iteration, the agent looks at the current situation, decides what to do, takes that action, and repeats until done.

**智能体循环**是重复的循环：观察、决策、行动。每次迭代，智能体查看当前情况，决定要做什么，采取该行动，然后重复，直到完成。

This is what separates agents from simple chatbots - agents don't stop after one response.

这就是智能体与简单聊天机器人的区别——智能体不会在一次响应后就停止。

### 2. State Transitions

### 2. 状态转换

**State transitions** track how the agent's state changes with each step. The state might include step count, completion status, accumulated results, or other tracking information.

**状态转换**跟踪智能体的状态如何随着每个步骤而变化。状态可能包括步骤计数、完成状态、累积结果或其他跟踪信息。

State makes the loop aware of its progress and history.

状态使循环了解其进度和历史。

### 3. Termination Conditions

### 3. 终止条件

**Termination conditions** determine when the loop stops. Common conditions include:
- The agent decides it's "done"
- Maximum steps reached
- A goal is achieved
- An error occurs

**终止条件**决定循环何时停止。常见条件包括：
- 智能体决定它已"完成"
- 达到最大步骤数
- 实现了目标
- 发生了错误

Without termination, the loop would run forever.

没有终止条件，循环将永远运行。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No memory across loops ([Lesson 07](07_memory.md))
- No planning ([Lesson 08](08_planning.md))
- No sophisticated reasoning - just simple step-by-step decisions

- 无跨循环记忆（[第 07 课](07_memory.md)）
- 无规划（[第 08 课](08_planning.md)）
- 无复杂推理——只是简单的逐步决策

## The Code

## 代码

Look at `agent/agent.py`, see `agent_step()` and `run_loop()` methods:

查看 `agent/agent.py`，参见 `agent_step()` 和 `run_loop()` 方法：

```python
def agent_step(self, user_input: str) -> dict | None:
    """
    Execute one step of the agent loop: observe, decide, act.
    
    Lesson 06 version.
    
    Args:
        user_input: User's input or system observation
        
    Returns:
        Action decision or None if step failed
    """
    state_dict = self.state.to_dict()
    
    prompt = f"""{self.system_prompt}

You are an agent. You must decide the next action and respond with ONLY valid JSON.

Current state: steps={state_dict.get('steps', 0)}, done={state_dict.get('done', False)}

Available actions: analyze, research, summarize, answer, done

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"action": "action_name", "reason": "explanation"}}

User input: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "action" in parsed:
            if "reason" not in parsed:
                parsed["reason"] = f"Taking action: {parsed['action']}"
            self.state.increment_step()
            return parsed
    
    return None

def run_loop(self, user_input: str, max_steps: int = 5):
    """
    Run the agent loop for multiple steps.
    
    Args:
        user_input: Initial user input
        max_steps: Maximum number of steps to execute
        
    Returns:
        List of action results
    """
    self.state.reset()
    results = []
    
    while not self.state.done and self.state.steps < max_steps:
        action = self.agent_step(user_input)
        
        if action:
            results.append(action)
            
            # Simple termination condition
            # 简单的终止条件
            if action.get("action") == "done":
                self.state.mark_done()
        else:
            break
    
    return results
```

Notice:
- **State tracking** - Each step increments the step counter and checks completion
- **Loop structure** - `while not done` continues until termination
- **Action accumulation** - Results are collected across steps
- **Safety limits** - `max_steps` prevents infinite loops

注意：
- **状态跟踪** - 每个步骤递增步骤计数器并检查完成状态
- **循环结构** - `while not done` 持续到终止
- **行动累积** - 结果在各步骤中被收集
- **安全限制** - `max_steps` 防止无限循环

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_06_agent_loop()` method:

查看 `complete_example.py`，参见 `lesson_06_agent_loop()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

print("\nNote: Repetition in early iterations is expected.")
print("The agent refines its understanding step by step and may repeat analysis")
print("before converging on a clearer explanation.\n")

results = agent.run_loop("Help me understand loops", max_steps=3)

for i, result in enumerate(results, 1):
    print(f"Iteration {i}:")
    action = result.get("action", "unknown")
    reason = result.get("reason", "No reason provided")
    print(f"  Action: {action}")
    print(f"  Reason: {reason}")
    if i < len(results):
        print()
```

The output shows each iteration with the action taken and reason. Note that repetition in early iterations is expected - the agent refines its understanding step by step.

输出显示每次迭代所采取的行动和原因。注意，早期迭代中的重复是预期的——智能体逐步完善其理解。

## Compare to Lesson 05

## 与第 05 课的对比

**Lesson 05 (Tool Calling):**
```
Request -> Tool call -> Result -> Done
```
Single interaction: request, execute, return.

**第 05 课（工具调用）：**
```
请求 -> 工具调用 -> 结果 -> 完成
```
单次交互：请求、执行、返回。

**Lesson 06 (Agent Loop):**
```
Input -> Step 1 -> Step 2 -> Step 3 -> Done
          |        |        |
        Action   Action   Action
```
Multiple steps in sequence, each deciding what to do next.

**第 06 课（智能体循环）：**
```
输入 -> 步骤 1 -> 步骤 2 -> 步骤 3 -> 完成
         |          |          |
       行动        行动        行动
```
按顺序执行多个步骤，每个步骤决定下一步要做什么。

![Agent Loop Flow](diagrams/lesson-06-agent-loop.png)

## Key Insights

## 关键见解

### An Agent is Not a Clever Prompt

### 智能体不是一个巧妙的提示词

An agent is not a clever prompt. It's a **loop with state**. The magic isn't in the prompt - it's in the repeated cycle of observation, decision, and action.

智能体不是一个巧妙的提示词。它是一个**带有状态的循环**。魔法不在于提示词——而在于观察、决策和行动的重复循环。

### State Enables Continuity

### 状态实现连续性

Without state, each step would be independent. With state, steps can build on each other and track progress toward a goal.

没有状态，每个步骤都将是独立的。有了状态，步骤可以相互构建并跟踪朝向目标的进度。

### Termination is Critical

### 终止至关重要

Always have termination conditions. Without them, loops can run forever or consume resources unnecessarily. `max_steps` is a simple but essential safety mechanism.

始终要有终止条件。没有它们，循环可能永远运行或不必要地消耗资源。`max_steps` 是一个简单但必不可少的安全机制。

### Simple is Better

### 简单更好

This loop is intentionally simple. Complex reasoning can come later - first, establish the pattern of repeated action.

这个循环是有意保持简单的。复杂的推理可以在之后加入——首先，建立重复行动的模式。

## Common Issues

## 常见问题

**"The loop runs forever"**
- Check that termination conditions are properly set
- Verify `max_steps` is being enforced
- Make sure the agent can signal "done"

**"循环永远运行"**
- 检查终止条件是否正确设置
- 验证 `max_steps` 是否被执行
- 确保智能体能够发出"完成"信号

**"Each step seems independent"**
- Include state information in the prompt
- Pass accumulated results to subsequent steps
- Make the state visible to the decision-making process

**"每个步骤似乎都是独立的"**
- 在提示词中包含状态信息
- 将累积结果传递给后续步骤
- 使状态对决策过程可见

**"The agent doesn't make progress"**
- Check that actions actually change something
- Verify state is being updated correctly
- Ensure the agent sees relevant state information

**"智能体没有取得进展"**
- 检查行动是否实际上改变了某些东西
- 验证状态是否正确更新
- 确保智能体看到了相关的状态信息

## Exercises

## 练习

1. Modify the available actions and see how the loop adapts
2. Change `max_steps` and observe how it affects behavior
3. Add state variables beyond step count
4. Experiment with different termination conditions

---

1. 修改可用行动，看看循环如何适应
2. 更改 `max_steps` 并观察它如何影响行为
3. 添加步骤计数之外的状态变量
4. 实验不同的终止条件

## What's Next?

## 下一步是什么？

In [Lesson 07](07_memory.md), we'll add **memory** so the agent can remember information across multiple interactions, not just within a single loop.

在[第 07 课](07_memory.md)中，我们将添加**记忆**，使智能体能够跨多次交互记住信息，而不仅仅是在单个循环内。

---

**Key Takeaway:** Agent = loop + state. That's it. The loop enables multi-step behavior, state enables continuity.

**关键要点：** 智能体 = 循环 + 状态。就这些。循环实现多步骤行为，状态实现连续性。
