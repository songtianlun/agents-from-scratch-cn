# Lesson 09  -  Atomic Steps & Safe Execution

# 第 09 课 —— 原子步骤与安全执行

## What Question Are We Answering?

## 我们在回答什么问题？

**"How do I make plans safe and predictable?"**

**"我如何使计划安全且可预测？"**

Plan steps like "Write article" are vague and hard to validate. Atomic actions break steps into the smallest possible, well-defined operations that can be validated and executed safely.

像"写文章"这样的计划步骤是模糊的，很难验证。原子动作将步骤分解为可以安全验证和执行的最小、定义明确的操作。

## What You Will Build

## 你将构建什么

An atomic action system that:
- Converts vague plan steps into specific, typed actions
- Validates actions before execution
- Uses schemas to ensure correct parameters
- Makes execution predictable and debuggable

一个原子动作系统，它能：
- 将模糊的计划步骤转换为具体的、类型化的行动
- 在执行前验证行动
- 使用模式确保正确的参数
- 使执行可预测且可调试

## New Concepts Introduced

## 引入的新概念

### 1. Atomicity

### 1. 原子性

**Atomicity** means breaking actions into the smallest possible units. Instead of "Write article," you get "generate_text" with specific parameters like topic and length.

**原子性**意味着将行动分解为尽可能小的单元。不是"写文章"，而是"generate_text"，带有诸如主题和长度的具体参数。

Atomic actions are indivisible - they either succeed completely or fail completely, with no partial states.

原子动作是不可分割的——它们要么完全成功，要么完全失败，没有部分状态。

### 2. Determinism

### 2. 确定性

**Determinism** means predictable outcomes. Given the same atomic action with the same inputs, you should get similar results (accounting for LLM randomness).

**确定性**意味着可预测的结果。给定相同的原子动作和相同的输入，你应该得到类似的结果（考虑到 LLM 的随机性）。

Atomic actions make execution deterministic by removing ambiguity.

原子动作通过消除歧义使执行具有确定性。

### 3. Typed Execution

### 3. 类型化执行

**Typed execution** means actions have validated schemas. Each action specifies:
- Action name (e.g., "generate_text")
- Required inputs (e.g., {"topic": string, "length": string})
- Validation rules

**类型化执行**意味着行动具有经过验证的模式。每个行动指定：
- 行动名称（例如，"generate_text"）
- 必需的输入（例如，{"topic": string, "length": string}）
- 验证规则

This catches errors before execution.

这在执行之前捕获错误。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No dependency handling between actions ([Lesson 10](10_atom_of_thought.md))
- No parallel execution
- No action execution implementation - just conversion and validation

- 无行动间依赖处理（[第 10 课](10_atom_of_thought.md)）
- 无并行执行
- 无行动执行实现——只是转换和验证

## The Code

## 代码

Look at `agent/planner.py`, see `create_atomic_action()` function:

查看 `agent/planner.py`，参见 `create_atomic_action()` 函数：

```python
def create_atomic_action(llm: LocalLLM, step: str) -> dict | None:
    """
    Convert a plan step into an atomic action.
    
    Used in: Lesson 09
    
    Args:
        llm: The language model to use
        step: A step from a plan
        
    Returns:
        Atomic action as a dictionary, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Convert this step into an atomic action. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{
  "action": "action_name",
  "inputs": {{"key": "value"}}
}}

The action should be a simple, atomic operation name.
The inputs should be a dictionary with the parameters needed for this action.

Step to convert:
{step}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        action = extract_json_from_text(response)
        
        if action and "action" in action:
            return action
    
    return None
```

And in `agent/agent.py`:

以及 `agent/agent.py` 中：

```python
def create_atomic_action(self, step: str) -> dict | None:
    """
    Convert a plan step into an atomic action.
    
    Lesson 09 version.
    
    Args:
        step: A step from a plan (e.g., "Write an explanation of AI agents")
        
    Returns:
        Atomic action dictionary with "action" and "inputs", or None if generation failed
    """
    return create_atomic_action(self.llm, step)
```

Notice:
- **Step conversion** - Vague steps become specific actions with parameters
- **Schema validation** - Actions must have "action" and "inputs" fields
- **Structured output** - Uses the same JSON pattern from previous lessons
- **Retry logic** - Multiple attempts to get valid atomic actions

注意：
- **步骤转换** - 模糊的步骤变成带参数的具体行动
- **模式验证** - 行动必须有"action"和"inputs"字段
- **结构化输出** - 使用与前面课程相同的 JSON 模式
- **重试逻辑** - 多次尝试获取有效的原子动作

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_09_atomic_actions()` method:

查看 `complete_example.py`，参见 `lesson_09_atomic_actions()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

# Convert a plan step into an atomic action
# 将计划步骤转换为原子动作
step = "Write an explanation of AI agents"
atomic_action = agent.create_atomic_action(step)
print(f"Step: {step}")
print(f"Atomic action: {atomic_action}")

# Example with a step from a plan
# 使用计划中步骤的示例
plan = agent.create_plan("Create a tutorial about Python")
if plan and "steps" in plan and plan["steps"]:
    first_step = plan["steps"][0]
    atomic_action_from_plan = agent.create_atomic_action(first_step)
    print(f"\nPlan step: {first_step}")
    print(f"Atomic action from plan step: {atomic_action_from_plan}")
```

## Compare to Lesson 08

## 与第 08 课的对比

**Lesson 08 (Planning):**
```
Goal -> Plan: ["Research topic", "Create outline", "Write draft"]
```
Plans are lists of vague step descriptions.

**第 08 课（规划）：**
```
目标 -> 计划：["研究主题", "创建大纲", "撰写草稿"]
```
计划是模糊步骤描述的列表。

**Lesson 09 (Atomic Actions):**
```
Step: "Write draft" -> Atomic: {"action": "generate_text", "inputs": {"topic": "...", "length": "..."}}
```
Steps become specific, typed actions with validated parameters.

**第 09 课（原子动作）：**
```
步骤："撰写草稿" -> 原子：{"action": "generate_text", "inputs": {"topic": "...", "length": "..."}}
```
步骤变成具体的、类型化的行动，带有经过验证的参数。

## Key Insights

## 关键见解

### Small Steps = Safe Systems

### 小步骤 = 安全系统

The smaller the action, the safer the system. Atomic actions are:
- Easier to validate - you can check parameters before execution
- Easier to test - each action can be tested independently
- Easier to debug - failures are isolated to specific actions
- Harder to fail catastrophically - small actions have limited blast radius

行动越小，系统越安全。原子动作是：
- 更容易验证——你可以在执行前检查参数
- 更容易测试——每个行动都可以独立测试
- 更容易调试——失败被隔离到特定行动
- 更难灾难性失败——小行动的影响范围有限

### Vague vs Specific

### 模糊与具体

"Write article" is vague. "generate_text(topic='AI agents', length='1000 words')" is specific. Specificity enables validation and predictable execution.

"写文章"是模糊的。"generate_text(topic='AI agents', length='1000 words')"是具体的。具体性使验证和可预测的执行成为可能。

### Validation Happens Early

### 验证尽早发生

By validating actions before execution, you catch errors early. A plan with invalid actions can be rejected before any work is done.

通过在执行前验证行动，你可以尽早捕获错误。带有无效行动的计划可以在任何工作完成之前被拒绝。

### Building Blocks

### 构建模块

Atomic actions are building blocks. Complex workflows are built from many simple atomic actions, each validated and safe.

原子动作是构建模块。复杂的工作流程由许多简单的原子动作构建，每个都经过验证且安全。

## Common Issues

## 常见问题

**"Atomic action is still vague"**
- Provide clearer instructions in the prompt
- Give examples of good atomic actions
- Consider constraining the action names to a predefined set

**"原子动作仍然模糊"**
- 在提示词中提供更清晰的指令
- 提供好的原子动作示例
- 考虑将行动名称限制为预定义集合

**"Validation fails"**
- Check that the action has both "action" and "inputs" fields
- Verify the JSON structure is correct
- Consider adding schema validation for inputs

**"验证失败"**
- 检查行动是否同时具有"action"和"inputs"字段
- 验证 JSON 结构是否正确
- 考虑为输入添加模式验证

**"Conversion fails"**
- Some steps might not map cleanly to atomic actions
- Consider multiple retry attempts (already implemented)
- Provide more context about what makes a good atomic action

**"转换失败"**
- 某些步骤可能无法清晰地映射到原子动作
- 考虑多次重试（已实现）
- 提供更多关于什么是好的原子动作的上下文

## Exercises

## 练习

1. Convert different types of plan steps to atomic actions
2. Compare atomic actions for similar steps
3. Try to validate atomic actions before execution
4. Experiment with different input parameter structures

1. 将不同类型的计划步骤转换为原子动作
2. 比较类似步骤的原子动作
3. 尝试在执行前验证原子动作
4. 实验不同的输入参数结构

## What's Next?

## 下一步是什么？

In [Lesson 10](10_atom_of_thought.md), we'll combine planning, atomic actions, and **dependencies** to create execution graphs that can run actions in the correct order and even in parallel.

在[第 10 课](10_atom_of_thought.md)中，我们将结合规划、原子动作和**依赖关系**，创建可以按正确顺序甚至并行运行行动的执行图。

---

**Key Takeaway:** Small steps = safe systems. Atomic actions make execution predictable, debuggable, and safe by breaking vague plans into specific, validated operations.

**关键要点：** 小步骤 = 安全系统。原子动作通过将模糊的计划分解为具体的、经过验证的操作，使执行可预测、可调试且安全。
