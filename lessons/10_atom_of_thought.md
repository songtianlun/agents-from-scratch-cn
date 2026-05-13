# Lesson 10  -  AoT (Atom of Thought)  -  Now It Makes Sense

# 第 10 课 —— AoT（思维原子） —— 现在一切都说得通了

## What Question Are We Answering?

## 我们在回答什么问题？

**"How do I scale planning without losing control?"**

**"我如何在不失去控制的情况下扩展规划？"**

Complex tasks need many actions with dependencies. Some actions can run in parallel, others must wait. AoT (Atom of Thought) creates dependency graphs that enable safe, efficient execution of complex workflows.

复杂的任务需要许多带有依赖关系的行动。有些行动可以并行运行，其他的必须等待。AoT（思维原子）创建依赖图，使复杂工作流程的安全、高效执行成为可能。

## What You Will Build

## 你将构建什么

An AoT system that:
- Creates dependency graphs with nodes and dependencies
- Validates graph structure before execution
- Executes actions respecting dependencies
- Enables parallel execution of independent actions

一个 AoT 系统，它能：
- 创建带有节点和依赖关系的依赖图
- 在执行前验证图结构
- 遵守依赖关系执行行动
- 实现独立行动的并行执行

## New Concepts Introduced

## 引入的新概念

### 1. Atomic Planning

### 1. 原子规划

**Atomic planning** means creating plans as dependency graphs where each node is an atomic action. Nodes can depend on other nodes, creating an explicit execution order.

**原子规划**意味着将计划创建为依赖图，其中每个节点是一个原子动作。节点可以依赖其他节点，创建明确的执行顺序。

This is the natural combination of Lesson 08's planning and Lesson 09's atomic actions, with added dependency tracking.

这是第 08 课规划和第 09 课原子动作的自然结合，加上了依赖跟踪。

### 2. Dependency Resolution

### 2. 依赖解析

**Dependency resolution** determines the correct execution order. Actions with no dependencies can run immediately. Actions with dependencies wait for their dependencies to complete.

**依赖解析**确定正确的执行顺序。没有依赖的行动可以立即运行。有依赖的行动等待其依赖完成。

This enables parallel execution of independent actions while respecting ordering constraints.

这在遵守排序约束的同时，实现了独立行动的并行执行。

### 3. Validated Execution

### 3. 经过验证的执行

**Validated execution** means checking the graph structure before running it. Are all dependencies valid? Is there a circular dependency? Are all required nodes present?

**经过验证的执行**意味着在运行图之前检查图结构。所有依赖都有效吗？有循环依赖吗？所有必需的节点都存在吗？

Validation catches structural errors before execution begins.

验证在执行开始前捕获结构性错误。

## The Code

## 代码

Look at `agent/planner.py`, see `create_aot_graph()` function:

查看 `agent/planner.py`，参见 `create_aot_graph()` 函数：

```python
def create_aot_graph(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate an AoT execution graph.
    
    Used in: Lesson 10
    
    Args:
        llm: The language model to use
        goal: The goal to achieve
        
    Returns:
        AoT graph with nodes and dependencies, or None if generation failed
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create an execution graph to achieve the goal. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{
  "nodes": [
    {{"id": "1", "action": "action_name", "depends_on": []}},
    {{"id": "2", "action": "action_name", "depends_on": ["1"]}}
  ]
}}

Each node must have:
- "id": unique identifier (string)
- "action": what to do (string)
- "depends_on": list of node IDs that must complete first (list of strings)

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        graph = extract_json_from_text(response)
        
        if graph and "nodes" in graph and isinstance(graph["nodes"], list):
            # Validate node structure
            # 验证节点结构
            node_ids = set()
            for node in graph["nodes"]:
                if "id" not in node or "action" not in node or "depends_on" not in node:
                    break
                node_ids.add(node["id"])
            else:
                # All nodes valid, check dependencies reference valid nodes
                # 所有节点有效，检查依赖是否引用有效节点
                for node in graph["nodes"]:
                    for dep in node.get("depends_on", []):
                        if dep not in node_ids:
                            break
                    else:
                        continue
                    break
                else:
                    return graph
    
    return None
```

And in `agent/agent.py`:

以及 `agent/agent.py` 中：

```python
def create_aot_plan(self, goal: str) -> dict | None:
    """
    Generate an AoT execution graph.
    
    Lesson 10 version.
    
    Args:
        goal: The goal to achieve
        
    Returns:
        AoT graph with atomic nodes and dependencies
    """
    return create_aot_graph(self.llm, goal)

def execute_aot_plan(self, graph: dict) -> list:
    """
    Execute an AoT graph respecting dependencies.
    
    Args:
        graph: AoT graph
        
    Returns:
        List of execution results
    """
    def execute_action(action: str):
        # Placeholder for actual action execution
        # 实际行动执行的占位符
        return f"Executed: {action}"
    
    return execute_graph(graph, execute_action)
```

Notice:
- **Graph structure** - Nodes with IDs, actions, and dependencies
- **Validation** - Checks that all dependencies reference valid nodes
- **Dependency resolution** - The execute_graph function handles ordering
- **Extensibility** - Easy to add parallel execution later

注意：
- **图结构** - 带有 ID、行动和依赖的节点
- **验证** - 检查所有依赖是否引用有效节点
- **依赖解析** - execute_graph 函数处理排序
- **可扩展性** - 之后容易添加并行执行

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_10_aot()` method:

查看 `complete_example.py`，参见 `lesson_10_aot()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

graph = agent.create_aot_plan("Research and write article")
print(f"AoT graph: {graph}")

if graph:
    results = agent.execute_aot_plan(graph)
    print(f"Execution results: {results}")
```

![Atom of Thought Graph](diagrams/lesson-10-atom-of-thoght.png)

## Compare to Lesson 09

## 与第 09 课的对比

**Lesson 09 (Atomic Actions):**
```
Step -> Atomic action: {"action": "...", "inputs": {...}}
```
Single step converted to atomic action.

**第 09 课（原子动作）：**
```
步骤 -> 原子动作：{"action": "...", "inputs": {...}}
```
单个步骤转换为原子动作。

**Lesson 10 (AoT):**
```
Goal -> Graph: {
  nodes: [
    {id: "1", action: "...", depends_on: []},
    {id: "2", action: "...", depends_on: ["1"]}
  ]
}
```
Multiple atomic actions with explicit dependencies.

**第 10 课（AoT）：**
```
目标 -> 图：{
  nodes: [
    {id: "1", action: "...", depends_on: []},
    {id: "2", action: "...", depends_on: ["1"]}
  ]
}
```
具有明确依赖关系的多个原子动作。

## Key Insights

## 关键见解

### AoT is Inevitable

### AoT 是必然的

At this point, AoT feels **inevitable**, not advanced. It's the natural evolution of planning (Lesson 08), atomic actions (Lesson 09), and adding dependencies. Once you understand the pieces, the graph structure makes perfect sense.

到这一点，AoT 感觉是**必然的**，而不是高级的。它是规划（第 08 课）、原子动作（第 09 课）的自然演进，加上了依赖关系。一旦你理解了各个部分，图结构就完全说得通了。

### It's Not Advanced Reasoning

### 这不是高级推理

AoT isn't smarter thinking - it's **better structure**:
- Each node is validated (from Lesson 09)
- Dependencies are explicit (new in this lesson)
- Execution is deterministic (respecting order)
- Failures are contained (to individual nodes)

AoT 不是更聪明的思考——它是**更好的结构**：
- 每个节点都经过验证（来自第 09 课）
- 依赖关系是显式的（本课新内容）
- 执行是确定性的（遵守顺序）
- 失败被隔离（到单个节点）

### Structure Enables Scale

### 结构实现扩展

By adding dependencies, you can handle complex workflows with many actions. Dependencies enable:
- Parallel execution of independent actions
- Clear execution order
- Easier debugging (know what depends on what)

通过添加依赖关系，你可以处理包含许多行动的复杂工作流程。依赖关系使以下成为可能：
- 独立行动的并行执行
- 清晰的执行顺序
- 更容易调试（知道什么依赖什么）

### Validation is Key

### 验证是关键

The graph structure must be validated before execution. Circular dependencies, missing nodes, or invalid references must be caught early.

图结构必须在执行前进行验证。循环依赖、缺失节点或无效引用必须尽早捕获。

## Common Issues

## 常见问题

**"Circular dependencies"**
- The validation should catch this
- Check that dependencies form a directed acyclic graph (DAG)
- Consider adding cycle detection to validation

**"循环依赖"**
- 验证应该捕获这个问题
- 检查依赖是否形成有向无环图（DAG）
- 考虑向验证添加循环检测

**"Dependencies reference non-existent nodes"**
- Validation checks for this
- Ensure all node IDs in dependencies exist in the graph
- Consider generating IDs more systematically

**"依赖引用了不存在的节点"**
- 验证会检查这一点
- 确保依赖中的所有节点 ID 都存在于图中
- 考虑更系统地生成 ID

**"Execution order seems wrong"**
- Verify dependencies are correctly specified
- Check that execute_graph respects dependencies
- Consider adding execution logging to see order

**"执行顺序似乎不对"**
- 验证依赖是否正确指定
- 检查 execute_graph 是否遵守依赖关系
- 考虑添加执行日志以查看顺序

## Exercises

## 练习

1. Create graphs with different dependency structures
2. Try to create a circular dependency and see if validation catches it
3. Compare execution order with and without dependencies
4. Experiment with parallel vs sequential execution

---

1. 创建具有不同依赖结构的图
2. 尝试创建循环依赖，看看验证是否能捕获它
3. 比较有和没有依赖的执行顺序
4. 实验并行与顺序执行

## Final Insight

## 最终见解

You've now built an agent that:
1. Talks to an LLM ([Lesson 01](01_basic_llm_chat.md))
2. Has consistent behavior ([Lesson 02](02_system_prompt.md))
3. Produces validated outputs ([Lesson 03](03_structured_output.md))
4. Makes decisions ([Lesson 04](04_decision_making.md))
5. Uses tools ([Lesson 05](05_tools.md))
6. Runs in a loop ([Lesson 06](06_agent_loop.md))
7. Remembers things ([Lesson 07](07_memory.md))
8. Plans actions ([Lesson 08](08_planning.md))
9. Executes safely ([Lesson 09](09_atomic_actions.md))
10. Scales with dependencies ([Lesson 10](10_atom_of_thought.md))

你现在已经构建了一个能够：
1. 与 LLM 对话（[第 01 课](01_basic_llm_chat.md)）
2. 具有一致行为（[第 02 课](02_system_prompt.md)）
3. 产生经过验证的输出（[第 03 课](03_structured_output.md)）
4. 做出决策（[第 04 课](04_decision_making.md)）
5. 使用工具（[第 05 课](05_tools.md)）
6. 在循环中运行（[第 06 课](06_agent_loop.md)）
7. 记住事物（[第 07 课](07_memory.md)）
8. 规划行动（[第 08 课](08_planning.md)）
9. 安全执行（[第 09 课](09_atomic_actions.md)）
10. 通过依赖关系扩展（[第 10 课](10_atom_of_thought.md)）

的智能体。

And you understand **exactly how it all works**. No magic, no hidden reasoning - just structure, validation, and explicit execution.

而且你**完全理解了这一切是如何工作的**。没有魔法，没有隐藏推理——只是结构、验证和显式执行。

---

**Key Takeaway:** AoT is structure, not magic. Agents are systems, not minds. Dependency graphs enable complex workflows while maintaining control and predictability.

**关键要点：** AoT 是结构，而非魔法。智能体是系统，而非思维。依赖图在保持控制和可预测性的同时，实现了复杂工作流程。
