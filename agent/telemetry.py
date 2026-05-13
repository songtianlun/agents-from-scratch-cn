"""
Agent Telemetry - Runtime Observability.

智能体遥测 - 运行时可观测性。

Telemetry is structured logging, not magic.
It's data you can inspect to understand what your agent did.

遥测是结构化日志，而非魔法。
它是你可以检查以了解智能体做了什么的数据。

This module provides:
- Structured JSON logging (not print statements)
- Spans and traces for linking related operations
- Metrics aggregation (latency, success rates, retries)

此模块提供：
- 结构化 JSON 日志（而非 print 语句）
- 用于链接相关操作的跨度和追踪
- 指标聚合（延迟、成功率、重试次数）
"""

import json
import time
from datetime import datetime
from uuid import uuid4
from dataclasses import dataclass, asdict, field
from typing import Any, Callable, Optional
from pathlib import Path


@dataclass
class Span:
    """
    A single operation in a trace.
    
    追踪中的单次操作。
    
    A span captures one discrete action: an LLM call, a tool execution,
    a memory operation, etc.
    
    跨度捕获一个离散的行动：LLM 调用、工具执行、
    记忆操作等。
    """
    span_id: str
    trace_id: str
    event_type: str
    timestamp: str
    duration_ms: Optional[float] = None
    data: Optional[dict] = None
    error: Optional[str] = None
    
    def to_dict(self) -> dict:
        """Convert to dictionary, excluding None values.
        
        转换为字典，排除 None 值。
        """
        return {k: v for k, v in asdict(self).items() if v is not None}


@dataclass
class Metrics:
    """Aggregated metrics for the agent.
    
    智能体的聚合指标。
    """
    llm_calls: int = 0
    llm_failures: int = 0
    llm_retries: int = 0
    tool_calls: int = 0
    tool_failures: int = 0
    memory_operations: int = 0
    total_tokens: int = 0
    total_latency_ms: float = 0.0
    
    @property
    def avg_latency_ms(self) -> float:
        """Average LLM call latency.
        
        LLM 调用的平均延迟。
        """
        return self.total_latency_ms / self.llm_calls if self.llm_calls > 0 else 0.0
    
    @property
    def llm_success_rate(self) -> float:
        """LLM call success rate (0.0 to 1.0).
        
        LLM 调用成功率（0.0 到 1.0）。
        """
        return 1 - (self.llm_failures / self.llm_calls) if self.llm_calls > 0 else 0.0
    
    @property
    def tool_success_rate(self) -> float:
        """Tool call success rate (0.0 to 1.0).
        
        工具调用成功率（0.0 到 1.0）。
        """
        return 1 - (self.tool_failures / self.tool_calls) if self.tool_calls > 0 else 0.0
    
    def to_dict(self) -> dict:
        """Export metrics as dictionary.
        
        将指标导出为字典。
        """
        return {
            "llm_calls": self.llm_calls,
            "llm_failures": self.llm_failures,
            "llm_retries": self.llm_retries,
            "llm_success_rate": f"{self.llm_success_rate:.2%}",
            "avg_latency_ms": round(self.avg_latency_ms, 1),
            "tool_calls": self.tool_calls,
            "tool_failures": self.tool_failures,
            "tool_success_rate": f"{self.tool_success_rate:.2%}",
            "memory_operations": self.memory_operations,
        }


class Telemetry:
    """
    Simple telemetry for agent observability.
    
    用于智能体可观测性的简单遥测。
    
    Usage:
        telemetry = Telemetry()
        telemetry.start_trace()
        
        # Log operations
        # 记录操作
        telemetry.log_llm_call(prompt, response, duration_ms)
        telemetry.log_tool_call(tool_name, args, result)
        
        # Check metrics
        # 检查指标
        print(telemetry.get_metrics())
    """
    
    def __init__(self, log_file: str = "agent_telemetry.jsonl"):
        """
        Initialize telemetry.
        
        初始化遥测。
        
        Args:
            log_file: Path to JSONL log file (None to disable file logging)
                      JSONL 日志文件的路径（None 禁用文件日志）
        """
        self.log_file = log_file
        self.current_trace_id: Optional[str] = None
        self.metrics = Metrics()
        self._spans: list[Span] = []  # In-memory span buffer / 内存中的跨度缓冲区
    
    def start_trace(self) -> str:
        """
        Start a new trace (one full agent interaction).
        
        开始一次新的追踪（一次完整的智能体交互）。
        
        Returns:
            The trace ID
            
            返回：
            追踪 ID
        """
        self.current_trace_id = str(uuid4())[:8]
        return self.current_trace_id
    
    def _log_span(self, span: Span):
        """Write span to log file and memory buffer.
        
        将跨度写入日志文件和内存缓冲区。
        """
        self._spans.append(span)
        
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(json.dumps(span.to_dict()) + "\n")
    
    def log_llm_call(self, 
                     prompt_length: int,
                     response_length: int,
                     duration_ms: float,
                     success: bool = True,
                     attempt: int = 1,
                     error: str = None):
        """
        Log an LLM call.
        
        记录 LLM 调用。
        
        Args:
            prompt_length: Length of prompt in characters
                           提示词的字符长度
            response_length: Length of response in characters
                             响应的字符长度
            duration_ms: Time taken in milliseconds
                         以毫秒为单位的耗时
            success: Whether the call succeeded (JSON parsed, etc.)
                     调用是否成功（JSON 已解析等）
            attempt: Retry attempt number (1 = first try)
                     重试尝试次数（1 = 第一次尝试）
            error: Error message if failed
                   失败时的错误消息
        """
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="llm_call",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2),
            data={
                "prompt_length": prompt_length,
                "response_length": response_length,
                "attempt": attempt,
                "success": success
            },
            error=error
        )
        
        self._log_span(span)
        
        # Update metrics
        # 更新指标
        self.metrics.llm_calls += 1
        self.metrics.total_latency_ms += duration_ms
        if not success:
            self.metrics.llm_failures += 1
        if attempt > 1:
            self.metrics.llm_retries += 1
    
    def log_tool_call(self,
                      tool_name: str,
                      arguments: dict,
                      result: Any = None,
                      duration_ms: float = None,
                      error: str = None):
        """
        Log a tool call.
        
        记录工具调用。
        
        Args:
            tool_name: Name of the tool called
                       被调用工具的名称
            arguments: Arguments passed to the tool
                       传递给工具的参数
            result: Result of the tool execution
                    工具执行的结果
            duration_ms: Time taken in milliseconds
                         以毫秒为单位的耗时
            error: Error message if failed
                   失败时的错误消息
        """
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="tool_call",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2) if duration_ms else None,
            data={
                "tool": tool_name,
                "arguments": arguments,
                "result": str(result)[:200] if result else None  # Truncate long results / 截断长结果
            },
            error=error
        )
        
        self._log_span(span)
        
        # Update metrics
        # 更新指标
        self.metrics.tool_calls += 1
        if error:
            self.metrics.tool_failures += 1
    
    def log_memory_operation(self,
                             operation: str,
                             data: str = None):
        """
        Log a memory operation.
        
        记录记忆操作。
        
        Args:
            operation: Type of operation (add, get, clear)
                       操作类型（add、get、clear）
            data: Data involved (truncated for storage)
                  涉及的数据（为存储截断）
        """
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="memory",
            timestamp=datetime.now().isoformat(),
            data={
                "operation": operation,
                "data": data[:100] if data else None  # Truncate / 截断
            }
        )
        
        self._log_span(span)
        self.metrics.memory_operations += 1
    
    def log_decision(self,
                     choices: list[str],
                     selected: str,
                     duration_ms: float = None):
        """
        Log a decision.
        
        记录决策。
        
        Args:
            choices: Available choices
                     可用选项
            selected: The choice made
                      所做的选择
            duration_ms: Time taken in milliseconds
                         以毫秒为单位的耗时
        """
        span = Span(
            span_id=str(uuid4())[:8],
            trace_id=self.current_trace_id or "no-trace",
            event_type="decision",
            timestamp=datetime.now().isoformat(),
            duration_ms=round(duration_ms, 2) if duration_ms else None,
            data={
                "choices": choices,
                "selected": selected
            }
        )
        
        self._log_span(span)
    
    def get_metrics(self) -> dict:
        """Get aggregated metrics as dictionary.
        
        以字典形式获取聚合指标。
        """
        return self.metrics.to_dict()
    
    def get_recent_spans(self, n: int = 10) -> list[dict]:
        """
        Get the n most recent spans.
        
        获取 n 个最近的跨度。
        
        Args:
            n: Number of spans to return
               要返回的跨度数
            
        Returns:
            List of span dictionaries
            
            返回：
            跨度字典列表
        """
        return [s.to_dict() for s in self._spans[-n:]]
    
    def get_trace_spans(self, trace_id: str) -> list[dict]:
        """
        Get all spans for a specific trace.
        
        获取特定追踪的所有跨度。
        
        Args:
            trace_id: The trace ID to filter by
                      要过滤的追踪 ID
            
        Returns:
            List of span dictionaries for that trace
            
            返回：
            该追踪的跨度字典列表
        """
        return [s.to_dict() for s in self._spans if s.trace_id == trace_id]
    
    def clear(self):
        """Clear all spans and reset metrics.
        
        清除所有跨度并重置指标。
        """
        self._spans = []
        self.metrics = Metrics()
        if self.log_file and Path(self.log_file).exists():
            Path(self.log_file).unlink()
    
    def print_summary(self):
        """Print a human-readable summary of metrics.
        
        打印人类可读的指标摘要。
        """
        m = self.get_metrics()
        print("\n" + "="*40)
        print("TELEMETRY SUMMARY")
        print("="*40)
        print(f"LLM Calls:      {m['llm_calls']}")
        print(f"  Success Rate: {m['llm_success_rate']}")
        print(f"  Avg Latency:  {m['avg_latency_ms']}ms")
        print(f"  Retries:      {m['llm_retries']}")
        print(f"Tool Calls:     {m['tool_calls']}")
        print(f"  Success Rate: {m['tool_success_rate']}")
        print(f"Memory Ops:     {m['memory_operations']}")
        print("="*40)


def traced(telemetry: Telemetry, event_type: str):
    """
    Decorator to add telemetry to any function.
    
    向任何函数添加遥测的装饰器。
    
    Usage:
        @traced(telemetry, "my_operation")
        def my_function():
            ...
    
    Args:
        telemetry: Telemetry instance to log to
                   要记录到的遥测实例
        event_type: Type of event to log
                    要记录的事件类型
        
    Returns:
        Decorated function
        
        返回：
        装饰后的函数
    """
    def decorator(func: Callable):
        def wrapper(*args, **kwargs):
            start = time.time()
            error = None
            result = None
            
            try:
                result = func(*args, **kwargs)
                return result
            except Exception as e:
                error = str(e)
                raise
            finally:
                duration_ms = (time.time() - start) * 1000
                span = Span(
                    span_id=str(uuid4())[:8],
                    trace_id=telemetry.current_trace_id or "no-trace",
                    event_type=event_type,
                    timestamp=datetime.now().isoformat(),
                    duration_ms=round(duration_ms, 2),
                    data={"function": func.__name__},
                    error=error
                )
                telemetry._log_span(span)
        
        return wrapper
    return decorator
