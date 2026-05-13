# Lesson 04  -  Decision Making with LLMs

# 第 04 课 —— 用 LLM 进行决策

## What Question Are We Answering?

## 我们在回答什么问题？

**"Can the model decide what to do, not just answer?"**

**"模型能决定要做什么，而不仅仅是回答问题吗？"**

This is the first moment of **agency**. Instead of responding with generated text, the model chooses actions from a finite set of options.

这是**智能体性**的第一个时刻。模型不再用生成的文本来响应，而是从有限的选项集中选择行动。

## What You Will Build

## 你将构建什么

A decision-making system that:
- Presents the model with a finite set of choices
- Forces the model to pick exactly one option
- Validates the decision and retries on failure
- Uses the decision to route execution

一个决策系统，它能：
- 向模型呈现一组有限的选择
- 强制模型选择其中一个选项
- 验证决策并在失败时重试
- 使用决策来路由执行

## New Concepts Introduced

## 引入的新概念

### 1. Decision Schemas

### 1. 决策模式（Decision Schemas）

A **decision schema** is a finite set of choices the model must pick from. Instead of generating free text, the model selects from predefined actions like "answer_question", "summarize_text", or "translate".

**决策模式**是模型必须从中选择的有限选项集。模型不再生成自由文本，而是从预定义的行动中选择，如"answer_question"、"summarize_text"或"translate"。

This constrains the output space dramatically - instead of infinite possible responses, there are only a few valid options.

这大大约束了输出空间——不再是无限可能的响应，而是只有几个有效选项。

### 2. Routing Logic

### 2. 路由逻辑

Once a decision is made, your code can **route** execution based on it. If the model chooses "summarize_text", you call the summarization function. If it chooses "translate", you call the translation function.

一旦做出决策，你的代码就可以基于它进行**路由**执行。如果模型选择"summarize_text"，你调用摘要函数。如果它选择"translate"，你调用翻译函数。

This is how agents take different paths based on what they "decide" to do.

这就是智能体如何根据它们"决定"做什么来走不同的路径。

### 3. Intent Detection

### 3. 意图检测

By framing user input as a decision problem, you're doing **intent detection**. The model analyzes what the user wants and maps it to one of your available actions.

通过将用户输入框架化为决策问题，你在进行**意图检测**。模型分析用户想要什么，并将其映射到你可用的行动之一。

This is simpler than trying to parse free text to understand intent.

这比尝试解析自由文本来理解意图要简单得多。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No tools ([Lesson 05](05_tools.md))
- No agent loop ([Lesson 06](06_agent_loop.md))
- No memory ([Lesson 07](07_memory.md))
- No planning ([Lesson 08](08_planning.md))

- 无工具（[第 05 课](05_tools.md)）
- 无智能体循环（[第 06 课](06_agent_loop.md)）
- 无记忆（[第 07 课](07_memory.md)）
- 无规划（[第 08 课](08_planning.md)）

## The Code

## 代码

Look at `agent/agent.py`, see `decide()` method:

查看 `agent/agent.py`，参见 `decide()` 方法：

```python
def decide(self, user_input: str, choices: list[str]) -> str | None:
    """
    Make the model choose from a finite set of options.
    
    Lesson 04 version.
    
    Args:
        user_input: The input to make a decision about
        choices: List of possible actions/decisions
        
    Returns:
        The chosen action or None if decision failed
    """
    options = "\n".join(f"- {choice}" for choice in choices)
    
    prompt = f"""{self.system_prompt}

You must choose ONE of the following options. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Available choices:
{options}

Required JSON format:
{{"decision": "one_of_the_choices_above"}}

User request: {user_input}

Response (JSON only):"""
    
    for attempt in range(3):
        response = self.llm.generate(prompt, temperature=0.0)
        parsed = extract_json_from_text(response)
        
        if parsed and "decision" in parsed:
            decision = parsed["decision"]
            if decision in choices:
                return decision
    
    return None
```

Notice we've added:
- **Finite choice space** - The model must pick from a predefined list, not generate anything
- **Validation** - We check that the decision is actually in the list of choices
- **Structured output** - Using the same JSON extraction pattern from Lesson 03
- **Retry logic** - Up to 3 attempts to get a valid decision

注意我们添加了：
- **有限选择空间** - 模型必须从预定义列表中选择，而不是生成任何内容
- **验证** - 我们检查决策是否实际在选择列表中
- **结构化输出** - 使用与第 03 课相同的 JSON 提取模式
- **重试逻辑** - 最多 3 次尝试获取有效决策

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_04_decisions()` method:

查看 `complete_example.py`，参见 `lesson_04_decisions()` 方法：

```python
from agent.agent import Agent

agent = Agent("models/llama-3-8b-instruct.gguf")

decision = agent.decide(
    "Can you summarize this article for me?",
    choices=["answer_question", "summarize_text", "translate"]
)

print(decision)
# Output: "summarize_text"
```

## Compare to Lesson 03

## 与第 03 课的对比

**Lesson 03 (Structured Output):**
```
Input: "What is AI?"
Output: {"answer": "AI is...", "confidence": "high"}
```
The model generates structured data with values it creates.

**第 03 课（结构化输出）：**
```
输入："What is AI?"
输出：{"answer": "AI is...", "confidence": "high"}
```
模型生成带有它自己创建的值的结构化数据。

**Lesson 04 (Decision Making):**
```
Input: "Summarize this article"
Choices: ["answer_question", "summarize_text", "translate"]
Output: "summarize_text"
```
The model selects from predefined options - no generation, just selection.

**第 04 课（决策制定）：**
```
输入："Summarize this article"
选择：["answer_question", "summarize_text", "translate"]
输出："summarize_text"
```
模型从预定义选项中选择——不是生成，而是选择。

## Key Insights

## 关键见解

### Selection vs Generation

### 选择与生成

The model is no longer generating content - it's **selecting from a finite action space**. This is fundamentally different and much more predictable than free-text generation.

模型不再生成内容——它在**从有限动作空间中选择**。这与自由文本生成有本质区别，并且更可预测。

### Agency Begins Here

### 智能体性从这里开始

This is where the agent starts to feel "agent-like". It's not just responding - it's choosing what to do. The choices might be simple, but the pattern is important.

这是智能体开始感觉"像智能体"的地方。它不只是在响应——它在选择要做什么。选择可能很简单，但这个模式很重要。

### Constrained = Reliable

### 约束 = 可靠

By limiting choices to a small, well-defined set, you make the system more reliable. The model can't hallucinate new actions - it must pick from your list.

通过将选择限制在一个小的、定义良好的集合中，你使系统更可靠。模型无法幻觉出新的行动——它必须从你的列表中选择。

### Validation is Critical

### 验证至关重要

Always validate that the decision is actually in your choices list. The model might return something that looks like a decision but isn't in your allowed set.

始终验证决策是否实际在你的选择列表中。模型可能会返回看起来像决策但不在你允许集合中的内容。

## Common Issues

## 常见问题

**"The model returns a choice not in my list"**
- Validate against the choices list (the code does this)
- Make your choice names clear and unambiguous
- Consider adding a retry with more explicit instructions

**"模型返回了一个不在我列表中的选择"**
- 针对选择列表进行验证（代码已经这样做了）
- 使你的选择名称清晰明确
- 考虑添加带有更明确指令的重试

**"All decisions seem random"**
- Check that your choices are semantically distinct
- Make sure the user input actually relates to the choices
- Lower temperature further for more deterministic selection

**"所有决策似乎都是随机的"**
- 检查你的选择在语义上是否不同
- 确保用户输入实际上与选择相关
- 进一步降低温度以获得更确定性的选择

**"The model adds explanations"**
- The `extract_json_from_text()` helper handles this
- Stronger instructions help (already in the code)
- Consider rejecting responses with extra text

**"模型添加了解释"**
- `extract_json_from_text()` 辅助函数处理了这个问题
- 更强烈的指令有帮助（代码中已有）
- 考虑拒绝带有额外文本的响应

## Exercises

## 练习

1. Create a decision with 5+ choices and test different inputs
2. Try ambiguous inputs and see which choice the model picks
3. Add a "none_of_the_above" choice and see when it's selected
4. Compare decisions with temperature 0.0 vs 0.5

1. 创建一个有 5 个以上选择的决策，并测试不同的输入
2. 尝试模糊的输入，看看模型选择哪个选项
3. 添加一个"none_of_the_above"（以上都不是）选项，看看它何时被选中
4. 比较温度 0.0 与 0.5 的决策结果

## What's Next?

## 下一步是什么？

In [Lesson 05](05_tools.md), we'll introduce **tools** - capabilities the agent can request to extend beyond text generation.

在[第 05 课](05_tools.md)中，我们将介绍**工具** —— 智能体可以请求的、超越文本生成的能力。

---

**Key Takeaway:** Decisions = agency. Agents choose, not just respond. Constraining choices makes behavior predictable.

**关键要点：** 决策 = 智能体性。智能体会选择，而不仅仅是响应。约束选择使行为可预测。