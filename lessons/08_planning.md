# Lesson 08  -  Planning as Data (Not Thoughts)

# 第 08 课 —— 规划即数据（而非思维）

## What Question Are We Answering?

## 我们在回答什么问题？

**"How can an agent solve multi-step tasks?"**

**"智能体如何解决多步骤任务？"**

Complex tasks require multiple steps. Planning breaks down a goal into a sequence of actions that can be executed step by step.

复杂的任务需要多个步骤。规划将目标分解为一系列可以逐步执行的行动。

## What You Will Build

## 你将构建什么

A planning system that:
- Generates a step-by-step plan from a goal
- Separates planning from execution
- Stores plans as data structures
- Executes plans sequentially

一个规划系统，它能：
- 从目标生成逐步计划
- 将规划与执行分离
- 将计划存储为数据结构
- 按顺序执行计划

## New Concepts Introduced

## 引入的新概念

### 1. Planning vs Execution

### 1. 规划与执行

**Planning** is generating the steps needed to achieve a goal. **Execution** is actually doing those steps. By separating them, you can:
- Inspect the plan before executing
- Modify the plan if needed
- Debug planning separately from execution

**规划**是生成实现目标所需的步骤。**执行**是实际完成这些步骤。通过将它们分离，你可以：
- 在执行前检查计划
- 在需要时修改计划
- 将规划与执行分开调试

This separation is powerful - you can see what the agent "thinks" it should do before it does it.

这种分离很强大——在智能体行动之前，你可以看到它"认为"应该做什么。

### 2. Step Ordering

### 2. 步骤排序

**Step ordering** determines the sequence of actions. Steps might depend on each other (step 2 needs step 1's output), or they might be independent.

**步骤排序**决定行动的顺序。步骤可能相互依赖（步骤 2 需要步骤 1 的输出），也可能是独立的。

For now, we execute steps in order. Later lessons will handle dependencies more explicitly.

目前，我们按顺序执行步骤。后面的课程将更明确地处理依赖关系。

### 3. Validation

### 3. 验证

**Validation** checks plans before execution. Is the plan valid JSON? Does it have the required structure? Are the steps reasonable?

**验证**在执行前检查计划。计划是有效的 JSON 吗？它有所需的结构吗？步骤合理吗？

Validating plans catches errors before wasting time on execution.

验证计划可以在浪费时间执行之前捕获错误。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No dependency handling ([Lesson 10](10_atom_of_thought.md))
- No atomic action validation ([Lesson 09](09_atomic_actions.md))
- No parallel execution - steps run sequentially

- 无依赖处理（[第 10 课](10_atom_of_thought.md)）
- 无原子动作验证（[第 09 课](09_atomic_actions.md)）
- 无并行执行——步骤按顺序运行

## The Code

## 代码

Look at `agent/agent.py`, see `create_plan()` and `execute_plan()` methods:

查看 `agent/agent.py`，参见 `create_plan()` 和 `execute_plan()` 方法：

```python
def create_plan(self, goal: str) -> dict | None:
    """
    Generate a plan to achieve a goal.
    
    Lesson 08 version.
    
    Args:
        goal: The goal to achieve
        
    Returns:
        Plan with steps
    """
    plan = create_plan(self.llm, goal)
    
    if plan:
        self.state.current_plan = plan
    
    return plan

def execute_plan(self, plan: dict) -> list:
    """
    Execute a plan step by step.
    
    Args:
        plan: Plan dictionary with "steps" list
        
    Returns:
        List of execution results
    """
    if not plan or "steps" not in plan:
        return []
    
    results = []
    
    for step in plan["steps"]:
        # Simple execution - in reality you'd call tools, etc.
        # 简单执行——实际上你会调用工具等
        result = {
            "step": step,
            "executed": True
        }
        results.append(result)
        self.state.increment_step()
    
    return results
```

And the planner implementation in `agent/planner.py`:

以及 `agent/planner.py` 中的规划器实现：

```python
def create_plan(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate a plan to achieve a goal.
    
    Used in: Lesson 08
    
    Args:
        llm: The language model to use
        goal: The goal to achieve
        
    Returns:
        Plan as a dictionary with a "steps" list, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create a step-by-step plan to achieve the goal. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"steps": ["step1", "step2", "step3"]}}

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        plan = extract_json_from_text(response)
        
        if plan and "steps" in plan and isinstance(plan["steps"], list):
            return plan
    
    return None
```

Notice:
- **Structured output** - Plans are JSON data structures
- **Validation** - We check that plans have the expected structure
- **Retry logic** - Multiple attempts to get a valid plan
- **Simple execution** - Steps are executed in order (actual execution logic comes later)

注意：
- **结构化输出** - 计划是 JSON 数据结构
- **验证** - 我们检查计划是否有预期的结构
- **重试逻辑** - 多次尝试获取有效计划
- **简单执行** - 步骤按顺序执行（实际执行逻辑在后面出现）

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_08_planning()` method:

查看 `complete_example.py`，参见 `lesson_08_planning()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

plan = agent.create_plan("Write a blog post about AI agents")
print(f"Plan: {plan}")

if plan:
    results = agent.execute_plan(plan)
    print(f"Execution results: {results}")
```

## Compare to Lesson 07

## 与第 07 课的对比

**Lesson 07 (Memory):**
```
User: "My name is Alice" -> Save to memory
User: "What's my name?" -> Retrieve from memory
```
Stores and retrieves facts.

**第 07 课（记忆）：**
```
用户："我的名字是 Alice" -> 保存到记忆
用户："我叫什么名字？" -> 从记忆中检索
```
存储和检索事实。

**Lesson 08 (Planning):**
```
Goal: "Write article" -> Plan: ["Research", "Outline", "Write", "Review"]
Plan -> Execute each step -> Results
```
Generates and executes a sequence of steps.

**第 08 课（规划）：**
```
目标："写文章" -> 计划：["研究", "概述", "写作", "审查"]
计划 -> 执行每个步骤 -> 结果
```
生成并执行一系列步骤。

![Planning Flow](diagrams/lesson-08-planning.png)

## Key Insights

## 关键见解

### Plans Aren't Thoughts

### 计划不是思维

Plans aren't thoughts - they're **data structures**. This makes them inspectable, modifiable, and safe. You can see, edit, and validate them before execution.

计划不是思维——它们是**数据结构**。这使它们可检查、可修改且安全。在执行之前，你可以查看、编辑和验证它们。

### Planning = Data Generation

### 规划 = 数据生成

Planning is not sophisticated reasoning - it's structured data generation. The model generates a list of steps, just like it generates any other structured output.

规划不是复杂的推理——它是结构化数据生成。模型生成步骤列表，就像生成其他任何结构化输出一样。

### Separate Phases

### 分离阶段

Separating planning from execution lets you:
- Debug plans without executing
- Modify plans before running
- Reuse plans for similar goals
- Test planning independently

将规划与执行分离让你可以：
- 在不执行的情况下调试计划
- 在运行前修改计划
- 为类似目标重用计划
- 独立测试规划

### Simple Execution

### 简单执行

For now, execution is simple - just iterate through steps. Later lessons will add more sophisticated execution with dependencies and validation.

目前，执行很简单——只是遍历步骤。后面的课程将添加带有依赖关系和验证的更复杂执行。

## Common Issues

## 常见问题

**"The plan is too vague"**
- Make the goal more specific
- Provide examples of good plans in the prompt
- Consider breaking down very general goals

**"计划太模糊了"**
- 使目标更具体
- 在提示词中提供好计划的示例
- 考虑分解非常笼统的目标

**"Steps are in wrong order"**
- The model determines order - validate if needed
- Consider adding dependency information
- Review and reorder steps before execution if necessary

**"步骤顺序错误"**
- 模型决定顺序——如有需要可进行验证
- 考虑添加依赖信息
- 如有必要，在执行前审查并重新排序步骤

**"Execution doesn't do anything"**
- This lesson's execution is a placeholder
- In practice, you'd call tools or other functions
- The pattern is more important than the implementation

**"执行什么都没做"**
- 本课的执行是一个占位符
- 在实践中，你会调用工具或其他函数
- 模式比实现更重要

## Exercises

## 练习

1. Generate plans for different types of goals
2. Modify plans manually before executing
3. Compare plans for the same goal across multiple runs
4. Try to validate plans for completeness

---

1. 为不同类型的目标生成计划
2. 在执行前手动修改计划
3. 比较多次运行中相同目标的计划
4. 尝试验证计划的完整性

## What's Next?

## 下一步是什么？

In [Lesson 09](09_atomic_actions.md), we'll make execution safer by converting plan steps into **atomic actions** with validated schemas.

在[第 09 课](09_atomic_actions.md)中，我们将通过将计划步骤转换为带有验证模式的**原子动作**来使执行更安全。

---

**Key Takeaway:** Planning = data generation, not reasoning. Plans are inspectable data structures that enable multi-step execution.

**关键要点：** 规划 = 数据生成，而非推理。计划是可检查的数据结构，支持多步骤执行。
