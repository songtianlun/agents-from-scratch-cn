# Lesson 12 - Telemetry (Runtime Observability)

# 第 12 课 —— 遥测（运行时可观测性）

## What Question Are We Answering?

## 我们在回答什么问题？

**"What is my agent actually doing at runtime?"**

**"我的智能体在运行时实际上在做什么？"**

Evals tell you if the agent works before deployment. Telemetry tells you what's happening during deployment. Without telemetry, debugging is guesswork.

评估告诉你智能体在部署前是否正常工作。遥测告诉你在部署过程中发生了什么。没有遥测，调试就是猜测。

## What You Will Build

## 你将构建什么

A telemetry system that:
- Logs every LLM call with inputs and outputs
- Tracks tool call success/failure rates
- Measures latency and retry counts
- Enables post-hoc debugging with traces

一个遥测系统，它能：
- 记录每次 LLM 调用的输入和输出
- 跟踪工具调用的成功/失败率
- 测量延迟和重试次数
- 通过追踪实现事后调试

## New Concepts Introduced

## 引入的新概念

### 1. Structured Logging

### 1. 结构化日志

**Structured logging** means JSON logs, not print statements. Every log entry has a consistent schema: timestamp, event type, data, error.

**结构化日志**意味着 JSON 日志，而不是 print 语句。每条日志条目都有一致的模式：时间戳、事件类型、数据、错误。

```json
{"event_type": "llm_call", "timestamp": "2024-01-15T10:30:00", "duration_ms": 1523, "success": true}
```

This is searchable, parseable, and machine-readable.

这是可搜索、可解析且机器可读的。

### 2. Spans and Traces

### 2. 跨度与追踪

A **span** is one operation - a single LLM call, one tool execution, one memory access.

**跨度**是一次操作——单次 LLM 调用、一次工具执行、一次内存访问。

A **trace** is a full agent interaction - multiple spans linked together by a trace ID.

**追踪**是完整的智能体交互——通过追踪 ID 链接在一起的多个跨度。

When something fails, you find the trace and see exactly what happened step by step.

当某些东西失败时，你找到追踪并逐步查看确切发生了什么。

### 3. Metrics

### 3. 指标

**Metrics** are aggregated numbers:
- `llm_success_rate` - How often does JSON parse correctly?
- `avg_latency_ms` - How long do LLM calls take?
- `tool_failure_rate` - How often do tool calls fail?

**指标**是聚合数字：
- `llm_success_rate` - JSON 解析正确的频率？
- `avg_latency_ms` - LLM 调用需要多长时间？
- `tool_failure_rate` - 工具调用失败的频率？

Metrics tell you the health of your agent at a glance.

指标让你一眼就能了解智能体的健康状况。

## What We Are NOT Doing (Yet)

## 我们（暂时）不做什么

- No distributed tracing (single machine only)
- No production dashboards (file-based logging)
- No alerting (manual inspection)
- No OpenTelemetry (keeping it simple)

- 无分布式追踪（仅单机）
- 无生产仪表板（基于文件的日志）
- 无告警（手动检查）
- 无 OpenTelemetry（保持简单）

## The Code

## 代码

Look at `agent/telemetry.py`:

查看 `agent/telemetry.py`：

```python
import json
import time
from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass, asdict
from typing import Optional


@dataclass
class Span:
    """A single operation in a trace."""
    span_id: str
    trace_id: str
    event_type: str
    timestamp: str
    duration_ms: Optional[float] = None
    data: Optional[dict] = None
    error: Optional[str] = None


@dataclass
class Metrics:
    """Aggregated metrics for the agent."""
    llm_calls: int = 0
    llm_failures: int = 0
    llm_retries: int = 0
    tool_calls: int = 0
    tool_failures: int = 0
    total_latency_ms: float = 0.0
    
    @property
    def avg_latency_ms(self) -> float:
        return self.total_latency_ms / self.llm_calls if self.llm_calls > 0 else 0.0
    
    @property
    def llm_success_rate(self) -> float:
        return 1 - (self.llm_failures / self.llm_calls) if self.llm_calls > 0 else 0.0


class Telemetry:
    """Simple telemetry for agent observability."""
    
    def __init__(self, log_file: str = "agent_telemetry.jsonl"):
        self.log_file = log_file
        self.current_trace_id = None
        self.metrics = Metrics()
    
    def start_trace(self) -> str:
        """Start a new trace (one full agent interaction)."""
        self.current_trace_id = str(uuid4())[:8]
        return self.current_trace_id
    
    def log_llm_call(self, prompt_length: int, response_length: int, 
                     duration_ms: float, success: bool = True, error: str = None):
        """Log an LLM call."""
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="llm_call",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2),
            data={"prompt_length": prompt_length, "response_length": response_length},
            error=error
        )
        
        # Write to log file
        # 写入日志文件
        with open(self.log_file, "a") as f:
            f.write(json.dumps(asdict(span)) + "\n")
        
        # Update metrics
        # 更新指标
        self.metrics.llm_calls += 1
        self.metrics.total_latency_ms += duration_ms
        if not success:
            self.metrics.llm_failures += 1
```

Notice:
- **Dataclasses** - Clean, typed structures
- **JSONL format** - One JSON object per line, easy to parse
- **Metrics accumulation** - Track aggregates as we go
- **Trace linking** - All spans share a trace ID

注意：
- **数据类** - 干净、类型化的结构
- **JSONL 格式** - 每行一个 JSON 对象，易于解析
- **指标累积** - 随着进行跟踪聚合
- **追踪链接** - 所有跨度共享一个追踪 ID

## How to Run

## 如何运行

Look at `complete_example.py`, see `lesson_12_telemetry()` method:

查看 `complete_example.py`，参见 `lesson_12_telemetry()` 方法：

```python
from agent.agent import Agent
from agent.telemetry import Telemetry

agent = Agent("models/llama-3-8b-instruct.gguf")
telemetry = Telemetry()

# Start a trace
# 开始一次追踪
trace_id = telemetry.start_trace()
print(f"Trace ID: {trace_id}")

# Simulate some operations (in real usage, these come from instrumented agent)
# 模拟一些操作（在实际使用中，这些来自已插桩的智能体）
import time

start = time.time()
result = agent.generate_structured("What is Python?", '{"answer": string}')
duration = (time.time() - start) * 1000

telemetry.log_llm_call(
    prompt_length=100,
    response_length=len(str(result)),
    duration_ms=duration,
    success=result is not None
)

# Check metrics
# 检查指标
telemetry.print_summary()
```

Example output:

示例输出：

```
========================================
TELEMETRY SUMMARY
========================================
LLM Calls:      3
  Success Rate: 100.00%
  Avg Latency:  1245ms
  Retries:      0
Tool Calls:     2
  Success Rate: 100.00%
Memory Ops:     1
========================================
```

## Viewing the Log File

## 查看日志文件

The telemetry logs to `agent_telemetry.jsonl`:

遥测日志记录到 `agent_telemetry.jsonl`：

```jsonl
{"span_id": "a1b2c3d4", "trace_id": "x9y8z7w6", "event_type": "llm_call", "timestamp": "2024-01-15T10:30:00.123456", "duration_ms": 1523.45, "data": {"prompt_length": 256, "response_length": 89, "success": true}}
{"span_id": "e5f6g7h8", "trace_id": "x9y8z7w6", "event_type": "tool_call", "timestamp": "2024-01-15T10:30:02.456789", "duration_ms": 5.23, "data": {"tool": "calculator", "arguments": {"a": 42, "b": 7, "operation": "multiply"}}}
```

To debug a specific interaction, filter by trace_id:

要调试特定交互，按 trace_id 过滤：
```bash
grep "x9y8z7w6" agent_telemetry.jsonl
```

## What to Log

## 记录什么

| Event | Data to Capture | Why |
|-------|-----------------|-----|
| LLM call | prompt_length, response_length, duration_ms, success | Track latency, identify slow/failing calls |
| Tool request | tool_name, arguments | Debug wrong tool selection |
| Tool execution | tool_name, result, error | Debug tool failures |
| Memory operation | operation, data | Track what's being stored/retrieved |
| Decision | choices, selected | Debug routing issues |

| 事件 | 需要捕获的数据 | 原因 |
|------|--------------|------|
| LLM 调用 | prompt_length, response_length, duration_ms, success | 跟踪延迟，识别慢速/失败的调用 |
| 工具请求 | tool_name, arguments | 调试错误的工具选择 |
| 工具执行 | tool_name, result, error | 调试工具失败 |
| 记忆操作 | operation, data | 跟踪正在存储/检索的内容 |
| 决策 | choices, selected | 调试路由问题 |

## Compare to Lesson 11

## 与第 11 课的对比

**Lesson 11 (Evals):**
- Run before deployment
- Known inputs, expected outputs
- Binary pass/fail
- Catches regressions

**第 11 课（评估）：**
- 在部署前运行
- 已知输入，预期输出
- 二进制通过/失败
- 捕获回归问题

**Lesson 12 (Telemetry):**
- Run during deployment
- Unknown inputs, observed outputs
- Continuous monitoring
- Enables debugging

**第 12 课（遥测）：**
- 在部署期间运行
- 未知输入，观察到的输出
- 持续监控
- 实现调试

They're complementary. Evals prevent bad code from shipping. Telemetry helps you understand what shipped code is doing.

它们是互补的。评估防止坏代码被发布。遥测帮助你理解已发布代码在做什么。

## Key Insights

## 关键见解

### Telemetry is Just Structured Logging

### 遥测只是结构化日志

No magic. You're writing JSON to a file. The power is in:
- Consistent schema
- Trace IDs linking related events
- Aggregated metrics

没有魔法。你在将 JSON 写入文件。力量在于：
- 一致的模式
- 将相关事件链接起来的追踪 ID
- 聚合指标

### Traces Are Your Debugging Superpower

### 追踪是你的调试超能力

When a user reports "the agent gave a weird answer", you:
1. Get the trace ID
2. Find all spans for that trace
3. See exactly what happened

当用户报告"智能体给出了奇怪的答案"时，你：
1. 获取追踪 ID
2. 找到该追踪的所有跨度
3. 确切地看到发生了什么

Without traces, you're guessing.

没有追踪，你只能猜测。

### Metrics Tell You System Health

### 指标告诉你系统健康状况

Glance at metrics to know if something's wrong:
- Success rate dropping? Check for prompt issues
- Latency increasing? Check model/hardware
- Retries increasing? Check JSON parsing

一眼看指标就知道是否有问题：
- 成功率下降？检查提示词问题
- 延迟增加？检查模型/硬件
- 重试次数增加？检查 JSON 解析

### Start Simple, Add More Later

### 从简单开始，之后再添加更多

This implementation logs to a file. That's enough to start. Later you might add:
- Database storage
- Real-time dashboards
- Alerting on thresholds

这个实现记录到文件。这已经足够开始了。之后你可能会添加：
- 数据库存储
- 实时仪表板
- 阈值告警

But start with a file.

但从文件开始。

## Common Issues

## 常见问题

**"The log file is too big"**
- Rotate logs (new file per day/hour)
- Only log failures in production
- Truncate long data fields

**"日志文件太大了"**
- 轮换日志（每天/每小时新文件）
- 在生产中只记录失败
- 截断长数据字段

**"I can't find the trace I need"**
- Add trace IDs to user-facing errors
- Log trace IDs in your application logs
- Consider adding user IDs to traces

**"我找不到需要的追踪"**
- 将追踪 ID 添加到面向用户的错误中
- 在应用程序日志中记录追踪 ID
- 考虑向追踪添加用户 ID

**"Telemetry is slowing down my agent"**
- Log asynchronously (buffer, then write)
- Reduce data captured per span
- Sample instead of logging everything

**"遥测减慢了我的智能体"**
- 异步记录（缓冲，然后写入）
- 减少每个跨度捕获的数据
- 采样而不是记录所有内容

## Exercises

## 练习

1. Add telemetry to the agent loop and trace a full multi-step interaction
2. Calculate JSON parse success rate across 20 structured output calls
3. Compare latency between different prompt lengths
4. Find a failing span in the logs and debug what went wrong

---

1. 向智能体循环添加遥测并追踪完整的多步骤交互
2. 计算 20 次结构化输出调用中 JSON 解析的成功率
3. 比较不同提示词长度之间的延迟
4. 在日志中找到失败的跨度并调试出了什么问题

## What's Next?

## 下一步是什么？

Congratulations! You've completed the core curriculum.

恭喜！你已经完成了核心课程。

You now have an agent with:
- Structured outputs (Lesson 03)
- Decision making (Lesson 04)
- Tool calling (Lesson 05)
- Agent loop (Lesson 06)
- Memory (Lesson 07)
- Planning (Lesson 08)
- Atomic actions (Lesson 09)
- Dependency graphs (Lesson 10)
- Regression testing (Lesson 11)
- Runtime observability (Lesson 12)

你现在拥有一个具有以下能力的智能体：
- 结构化输出（第 03 课）
- 决策制定（第 04 课）
- 工具调用（第 05 课）
- 智能体循环（第 06 课）
- 记忆（第 07 课）
- 规划（第 08 课）
- 原子动作（第 09 课）
- 依赖图（第 10 课）
- 回归测试（第 11 课）
- 运行时可观测性（第 12 课）

This is a complete, observable, testable agent built from first principles.

这是一个从第一性原理构建的完整、可观测、可测试的智能体。

---

**Key Takeaway:** Telemetry = structured logging + traces + metrics. It turns "something's wrong" into "here's exactly what happened."

**关键要点：** 遥测 = 结构化日志 + 追踪 + 指标。它将"有什么东西出了问题"变成"这就是确切发生的事情"。
