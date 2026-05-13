# Lesson 11 - Evals (Regression Testing for Agents)

# 第 11 课 —— 评估（智能体的回归测试）

## What Question Are We Answering?

## 我们在回答什么问题？

**"How do I know if my agent still works after I change something?"**

**"在我修改某些东西之后，我如何知道我的智能体是否仍然正常工作？"**

Once you have tools, memory, and structured outputs, changing a prompt becomes risky. A small wording change can break JSON parsing. An "improvement" can make tool calls less reliable. Without evals, quality degrades silently.

一旦你有了工具、记忆和结构化输出，修改提示词就变得有风险了。一个小的措辞改变可能会破坏 JSON 解析。一个"改进"可能会使工具调用变得不那么可靠。没有评估，质量会悄悄下降。

An eval suite is just a Python file that runs your agent and asserts things didn't break.

评估套件只是一个运行你的智能体并断言事情没有损坏的 Python 文件。

## What You Will Build

## 你将构建什么

An evaluation system that:
- Tests prompt and JSON parsing reliability
- Validates tool call accuracy
- Checks memory storage and retrieval cycles
- Catches regressions before deployment

一个评估系统，它能：
- 测试提示词和 JSON 解析的可靠性
- 验证工具调用的准确性
- 检查记忆存储和检索循环
- 在部署前捕获回归问题

## New Concepts Introduced

## 引入的新概念

### 1. Eval Suites

### 1. 评估套件

An **eval suite** is a collection of test cases that validate agent behavior. Each case has an input and an expected outcome. You run the suite after every prompt change.

**评估套件**是验证智能体行为的测试用例集合。每个用例都有一个输入和一个预期结果。每次提示词更改后你都要运行套件。

This isn't magic - it's just running your agent with known inputs and checking the outputs.

这没有魔法——只是用已知输入运行你的智能体并检查输出。

### 2. Golden Datasets

### 2. 黄金数据集

A **golden dataset** is your source of truth - known-good examples that must always pass. If a golden case fails, the agent is broken (not the test).

**黄金数据集**是你的真相来源——必须始终通过的已知正确示例。如果一个黄金用例失败，那是智能体出了问题（不是测试）。

Golden datasets are version controlled alongside your prompts. When you change a prompt, you run the golden dataset to verify nothing broke.

黄金数据集与你的提示词一起进行版本控制。当你更改提示词时，运行黄金数据集以验证没有任何内容损坏。

### 3. Hard vs Soft Assertions

### 3. 硬断言与软断言

**Hard assertions** must always pass:
- JSON must be valid
- Required fields must be present
- Tool names must match available tools

**硬断言**必须始终通过：
- JSON 必须有效
- 必填字段必须存在
- 工具名称必须与可用工具匹配

**Soft assertions** should usually pass:
- The answer is semantically correct
- The phrasing is appropriate
- The tool arguments are optimal

**软断言**通常应该通过：
- 答案在语义上是正确的
- 措辞是合适的
- 工具参数是最优的

Start with hard assertions. Add soft ones later.

从硬断言开始。之后再添加软断言。

## Why This Fails in the Real World

## 为什么这在现实世界中会失败

A prompt change that improves phrasing can:
- Increase verbosity
- Push JSON out of context window
- Break parsing
- ...without changing correctness

一个改善措辞的提示词更改可能会：
- 增加冗长度
- 将 JSON 推出上下文窗口
- 破坏解析
- ……而不改变正确性

This is why evals exist. They catch these silent failures.

这就是评估存在的原因。它们捕获这些无声的失败。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No runtime monitoring ([Lesson 12](12_telemetry.md))
- No A/B testing
- No production observability
- No LLM-as-judge evals (too complex for now)

- 无运行时监控（[第 12 课](12_telemetry.md)）
- 无 A/B 测试
- 无生产可观测性
- 无 LLM 作为评判的评估（目前太复杂）

## The Code

## 代码

Look at `agent/evals.py`:

查看 `agent/evals.py`：

```python
from dataclasses import dataclass, field
from typing import Any


@dataclass
class EvalResult:
    """Result of a single eval case."""
    passed: bool
    input: str
    expected: Any = None
    actual: Any = None
    error: str | None = None


@dataclass 
class EvalSuiteResult:
    """Result of running an eval suite."""
    name: str
    passed: int = 0
    failed: int = 0
    results: list[EvalResult] = field(default_factory=list)
    
    @property
    def pass_rate(self) -> float:
        return self.passed / (self.passed + self.failed) if (self.passed + self.failed) > 0 else 0.0
    
    def summary(self) -> str:
        status = "✓ PASSED" if self.failed == 0 else "✗ FAILED"
        return f"{self.name}: {status} ({self.passed}/{self.passed + self.failed})"


class AgentEval:
    """Regression testing for agent capabilities."""
    
    def __init__(self, agent):
        self.agent = agent
    
    def test_structured_output(self, cases: list[dict]) -> EvalSuiteResult:
        """Test that structured output parses correctly and matches schema."""
        suite = EvalSuiteResult(name="Structured Output")
        
        for case in cases:
            result = self.agent.generate_structured(case["input"], case["schema"])
            
            # Check 1: Did we get valid JSON?
            # 检查 1：我们得到有效的 JSON 了吗？
            if result is None:
                suite.add_result(EvalResult(
                    passed=False,
                    input=case["input"],
                    error="Failed to parse JSON"
                ))
                continue
            
            # Check 2: Are required fields present?
            # 检查 2：必填字段是否存在？
            missing = [f for f in case.get("must_have_fields", []) if f not in result]
            if missing:
                suite.add_result(EvalResult(
                    passed=False,
                    input=case["input"],
                    error=f"Missing fields: {missing}"
                ))
                continue
            
            suite.add_result(EvalResult(passed=True, input=case["input"], actual=result))
        
        return suite
```

Notice:
- **Plain Python** - No testing framework needed
- **Structured results** - Each result captures input, expected, actual, error
- **Composable** - Run one suite or many
- **Actionable** - Failures tell you exactly what went wrong

注意：
- **纯 Python** - 不需要测试框架
- **结构化结果** - 每个结果捕获输入、预期、实际和错误
- **可组合** - 运行一个或多个套件
- **可操作** - 失败告诉你确切出了什么问题

## The Golden Dataset

## 黄金数据集

Look at `evals/golden_datasets.py`:

查看 `evals/golden_datasets.py`：

```python
STRUCTURED_OUTPUT_GOLDEN = [
    {
        "input": "Explain quantum computing in one sentence",
        "schema": """{
  "topic": "the topic name as a string",
  "difficulty": "beginner" or "intermediate" or "advanced"
}

Example: {"topic": "machine learning", "difficulty": "intermediate"}""",
        "must_have_fields": ["topic", "difficulty"]
    },
]

TOOL_CALL_GOLDEN = [
    {
        "input": "What is 42 * 7?",
        "expected_tool": "calculator",
        "expected_args": {"operation": "multiply"}
    },
]

MEMORY_GOLDEN = [
    {
        "store_input": "My name is Alice",
        "query_input": "What's my name?",
        "expected_in_response": "Alice"
    },
]
```

Notice:
- **Multi-line schemas with examples** - Single-line schemas often confuse models
- **Version controlled** - These live in your repo
- **Cover edge cases** - Special characters, numbers, etc.
- **Specific assertions** - Not "it works" but "this field exists"

注意：
- **带有示例的多行模式** - 单行模式通常会使模型感到困惑
- **版本控制** - 这些文件存在于你的仓库中
- **覆盖边缘情况** - 特殊字符、数字等
- **具体断言** - 不是"它有效"，而是"这个字段存在"

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_11_evals()` method:

查看 `complete_example.py`，参见 `lesson_11_evals()` 方法：

```python
from agent.agent import Agent
from agent.evals import AgentEval, print_eval_report
from evals.golden_datasets import (
    STRUCTURED_OUTPUT_GOLDEN,
    TOOL_CALL_GOLDEN,
    MEMORY_GOLDEN
)

agent = Agent("models/llama-3-8b-instruct.gguf")
evaluator = AgentEval(agent)

# Run all evals
# 运行所有评估
results = evaluator.run_all(
    structured_cases=STRUCTURED_OUTPUT_GOLDEN,
    tool_cases=TOOL_CALL_GOLDEN,
    memory_cases=MEMORY_GOLDEN
)

# Print report
# 打印报告
print_eval_report(results)
```

Example output:

示例输出：

```
==================================================
EVAL REPORT
==================================================

Structured Output: ✓ PASSED (4/4)
Tool Calls: ✓ PASSED (5/5)
Memory Cycle: ✓ PASSED (3/3)

--------------------------------------------------
Overall: ✓ ALL PASSED (12/12)
==================================================
```

Or when something breaks:

或者当某些东西损坏时：

```
==================================================
EVAL REPORT
==================================================

Structured Output: ✗ FAILED (3/4)
  ✗ Input: What does 'hello world' mean in progra...
    Expected: Fields: ['explanation']
    Actual: Missing: ['explanation']
    Error: Schema contract violated

--------------------------------------------------
Overall: ✗ 1 FAILED (11/12)
==================================================
```

## What to Test

## 测试什么

| Component | What to Eval | Example Assertion |
| --------- | ------------ | ----------------- |
| Structured output | JSON validity + schema contract | `parse_json(output) is not None and matches schema` |
| Decisions | Correct routing | `decision in valid_choices` |
| Tool calls | Correct tool + args | `tool_call["tool"] == "calculator"` |
| Memory | Store/retrieve cycle | `agent.memory.get_all()` contains saved fact |

| 组件 | 评估什么 | 示例断言 |
| ---- | -------- | -------- |
| 结构化输出 | JSON 有效性 + 模式契约 | `parse_json(output) is not None and matches schema` |
| 决策 | 正确路由 | `decision in valid_choices` |
| 工具调用 | 正确的工具 + 参数 | `tool_call["tool"] == "calculator"` |
| 记忆 | 存储/检索循环 | `agent.memory.get_all()` 包含已保存的事实 |

## Compare to Lesson 03

## 与第 03 课的对比

**Lesson 03 (Structured Output):**
- One-off validation during generation
- Retry if JSON fails
- No history

**第 03 课（结构化输出）：**
- 生成过程中的一次性验证
- JSON 失败时重试
- 没有历史记录

**Lesson 11 (Evals):**
- Systematic testing across many cases
- Track success rates over time
- Catch regressions before deployment

**第 11 课（评估）：**
- 跨多个用例的系统测试
- 随时间跟踪成功率
- 在部署前捕获回归问题

## Key Insights

## 关键见解

### Evals Are Just Assertions

### 评估只是断言

There's no magic here. You run the agent, check the output, report pass/fail. The power is in doing this systematically.

这里没有魔法。你运行智能体，检查输出，报告通过/失败。力量在于系统地做这件事。

### Golden Datasets Are Your Contract

### 黄金数据集是你的契约

When someone asks "does the agent work?", you point to the golden dataset. 100% pass rate = it works. Anything less = specific failures to fix.

当有人问"智能体能用吗？"时，你指向黄金数据集。100% 通过率 = 它有效。低于此 = 需要修复的具体失败。

### Run Evals Before Every Change

### 每次更改前运行评估

The workflow:
1. Make prompt change
2. Run evals
3. If any fail, fix or revert
4. Commit

工作流程：
1. 做提示词更改
2. 运行评估
3. 如果有任何失败，修复或回滚
4. 提交

This is how you prevent quality degradation.

这是你防止质量下降的方式。

### Start Simple

### 从简单开始

You don't need 1000 test cases. Start with 5-10 golden cases per capability. Add more as you find edge cases in production.

你不需要 1000 个测试用例。每个能力从 5-10 个黄金用例开始。随着在生产中发现边缘情况，再添加更多。

## Common Issues

## 常见问题

**"Evals are too slow"**
- Run a smaller subset for quick checks
- Run full suite before commits
- Consider caching model loads

**"评估太慢了"**
- 运行更小的子集进行快速检查
- 在提交前运行完整套件
- 考虑缓存模型加载

**"Soft assertions are flaky"**
- Start with hard assertions only
- Add soft ones when you have enough data
- Consider using exact match before semantic match

**"软断言不稳定"**
- 只从硬断言开始
- 当你有足够数据时再添加软断言
- 考虑在语义匹配之前使用精确匹配

**"I don't know what to test"**
- Start with the happy path
- Add cases that broke in production
- Cover edge cases (empty input, special chars, etc.)

**"我不知道要测试什么"**
- 从快乐路径开始
- 添加在生产中损坏的用例
- 覆盖边缘情况（空输入、特殊字符等）

## Exercises

## 练习

1. Add a new golden case that currently fails, then fix the prompt
2. Break a prompt intentionally and verify evals catch the regression
3. Add an edge case (empty input, very long input, unicode)
4. Create golden dataset for planning (Lesson 08)

1. 添加一个目前失败的新黄金用例，然后修复提示词
2. 有意破坏一个提示词并验证评估是否能捕获回归问题
3. 添加边缘情况（空输入、非常长的输入、Unicode）
4. 为规划创建黄金数据集（第 08 课）

## What's Next?

## 下一步是什么？

In [Lesson 12](12_telemetry.md), we'll add **telemetry** - understanding what your agent is doing at runtime, not just in tests.

在[第 12 课](12_telemetry.md)中，我们将添加**遥测** —— 了解你的智能体在运行时做什么，而不仅仅是在测试中。

---

**Key Takeaway:** Evals = systematic testing. Golden datasets = your contract. Run them before every prompt change.

**关键要点：** 评估 = 系统测试。黄金数据集 = 你的契约。每次提示词更改前都要运行它们。
