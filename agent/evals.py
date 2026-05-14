"""
Agent Evaluation Framework.

智能体评估框架。

Evals are regression tests for agents.
An eval suite is just a Python file that runs your agent and asserts things didn't break.

评估是智能体的回归测试。
评估套件只是一个运行智能体并断言事情没有损坏的 Python 文件。

This module provides:
- Structured output validation
- Tool call accuracy testing
- Memory store/retrieve cycle testing
- Decision routing validation

此模块提供：
- 结构化输出验证
- 工具调用准确性测试
- 记忆存储/检索循环测试
- 决策路由验证
"""

from typing import Any, Callable
from dataclasses import dataclass, field


@dataclass
class EvalResult:
    """Result of a single eval case.
    
    单个评估用例的结果。
    """
    passed: bool
    input: str
    expected: Any = None
    actual: Any = None
    error: str | None = None


@dataclass 
class EvalSuiteResult:
    """Result of running an eval suite.
    
    运行评估套件的结果。
    """
    name: str
    passed: int = 0
    failed: int = 0
    results: list[EvalResult] = field(default_factory=list)
    
    @property
    def total(self) -> int:
        return self.passed + self.failed
    
    @property
    def pass_rate(self) -> float:
        return self.passed / self.total if self.total > 0 else 0.0
    
    def add_result(self, result: EvalResult):
        """Add a result and update counts.
        
        添加结果并更新计数。
        """
        self.results.append(result)
        if result.passed:
            self.passed += 1
        else:
            self.failed += 1
    
    def summary(self) -> str:
        """Generate a human-readable summary.
        
        生成人类可读的摘要。
        """
        status = "✓ PASSED" if self.failed == 0 else "✗ FAILED"
        return f"{self.name}: {status} ({self.passed}/{self.total})"


class AgentEval:
    """
    Regression testing for agent capabilities.
    
    智能体能力的回归测试。
    
    Usage:
        evaluator = AgentEval(agent)
        results = evaluator.test_structured_output(golden_cases)
        print(results.summary())
    """
    
    def __init__(self, agent):
        """
        Initialize evaluator with an agent instance.
        
        使用智能体实例初始化评估器。
        
        Args:
            agent: The Agent instance to test
                   要测试的智能体实例
        """
        self.agent = agent
    
    def test_structured_output(self, cases: list[dict]) -> EvalSuiteResult:
        """
        Test that structured output parses correctly and matches schema.
        
        测试结构化输出是否正确解析并匹配模式。
        
        This is a HARD assertion - JSON must always be valid.
        
        这是一个硬断言——JSON 必须始终有效。
        
        Args:
            cases: List of {"input": str, "schema": str, "must_have_fields": list[str]}
                   {"input": str, "schema": str, "must_have_fields": list[str]} 的列表
            
        Returns:
            EvalSuiteResult with pass/fail counts and details
            
            返回：
            包含通过/失败计数和详细信息的 EvalSuiteResult
        """
        suite = EvalSuiteResult(name="Structured Output")
        
        for case in cases:
            input_text = case["input"]
            schema = case["schema"]
            required_fields = case.get("must_have_fields", [])
            
            try:
                result = self.agent.generate_structured(input_text, schema)
                
                # Check 1: Did we get valid JSON?
                # 检查 1：我们得到有效的 JSON 了吗？
                if result is None:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected="Valid JSON",
                        actual=None,
                        error="Failed to parse JSON after retries"
                    ))
                    continue
                
                # Check 2: Are required fields present?
                # 检查 2：必填字段是否存在？
                missing_fields = [f for f in required_fields if f not in result]
                if missing_fields:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected=f"Fields: {required_fields}",
                        actual=f"Missing: {missing_fields}",
                        error="Schema contract violated"
                    ))
                    continue
                
                # Passed all checks
                # 通过了所有检查
                suite.add_result(EvalResult(
                    passed=True,
                    input=input_text,
                    actual=result
                ))
                
            except Exception as e:
                suite.add_result(EvalResult(
                    passed=False,
                    input=input_text,
                    error=str(e)
                ))
        
        return suite
    
    def test_tool_calls(self, cases: list[dict]) -> EvalSuiteResult:
        """
        Test tool call accuracy - correct tool selected with valid arguments.
        
        测试工具调用准确性——使用有效参数选择了正确的工具。
        
        Args:
            cases: List of {"input": str, "expected_tool": str, "expected_args": dict (optional)}
                   {"input": str, "expected_tool": str, "expected_args": dict（可选）} 的列表
            
        Returns:
            EvalSuiteResult with pass/fail counts
            
            返回：
            包含通过/失败计数的 EvalSuiteResult
        """
        suite = EvalSuiteResult(name="Tool Calls")
        
        for case in cases:
            input_text = case["input"]
            expected_tool = case["expected_tool"]
            expected_args = case.get("expected_args")
            
            try:
                tool_call = self.agent.request_tool(input_text)
                
                # Check 1: Did we get a tool call?
                # 检查 1：我们得到工具调用了吗？
                if tool_call is None:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected=expected_tool,
                        actual=None,
                        error="No tool call generated"
                    ))
                    continue
                
                # Check 2: Is it the right tool?
                # 检查 2：是正确的工具吗？
                actual_tool = tool_call.get("tool")
                if actual_tool != expected_tool:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected=expected_tool,
                        actual=actual_tool,
                        error="Wrong tool selected"
                    ))
                    continue
                
                # Check 3: Are arguments valid? (if specified)
                # 检查 3：参数是否有效？（如果已指定）
                if expected_args:
                    actual_args = tool_call.get("arguments", {})
                    for key, expected_val in expected_args.items():
                        if actual_args.get(key) != expected_val:
                            suite.add_result(EvalResult(
                                passed=False,
                                input=input_text,
                                expected=expected_args,
                                actual=actual_args,
                                error=f"Wrong argument: {key}"
                            ))
                            continue
                
                # Passed
                # 通过
                suite.add_result(EvalResult(
                    passed=True,
                    input=input_text,
                    expected=expected_tool,
                    actual=tool_call
                ))
                
            except Exception as e:
                suite.add_result(EvalResult(
                    passed=False,
                    input=input_text,
                    error=str(e)
                ))
        
        return suite
    
    def test_decisions(self, cases: list[dict]) -> EvalSuiteResult:
        """
        Test decision routing - agent picks correct action from choices.
        
        测试决策路由——智能体从选项中选择正确的行动。
        
        Args:
            cases: List of {"input": str, "choices": list[str], "expected": str}
                   {"input": str, "choices": list[str], "expected": str} 的列表
            
        Returns:
            EvalSuiteResult with pass/fail counts
            
            返回：
            包含通过/失败计数的 EvalSuiteResult
        """
        suite = EvalSuiteResult(name="Decisions")
        
        for case in cases:
            input_text = case["input"]
            choices = case["choices"]
            expected = case["expected"]
            
            try:
                decision = self.agent.decide(input_text, choices)
                
                if decision is None:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected=expected,
                        actual=None,
                        error="No decision made"
                    ))
                elif decision != expected:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=input_text,
                        expected=expected,
                        actual=decision,
                        error="Wrong decision"
                    ))
                else:
                    suite.add_result(EvalResult(
                        passed=True,
                        input=input_text,
                        expected=expected,
                        actual=decision
                    ))
                    
            except Exception as e:
                suite.add_result(EvalResult(
                    passed=False,
                    input=input_text,
                    error=str(e)
                ))
        
        return suite
    
    def test_memory_cycle(self, cases: list[dict]) -> EvalSuiteResult:
        """
        Test memory store → retrieve cycle.
        
        测试记忆存储 → 检索循环。
        
        Args:
            cases: List of {"store_input": str, "query_input": str, "expected_in_response": str}
                   {"store_input": str, "query_input": str, "expected_in_response": str} 的列表
            
        Returns:
            EvalSuiteResult with pass/fail counts
            
            返回：
            包含通过/失败计数的 EvalSuiteResult
        """
        suite = EvalSuiteResult(name="Memory Cycle")
        
        for case in cases:
            store_input = case["store_input"]
            query_input = case["query_input"]
            expected_substring = case.get("expected_in_response", "")
            
            try:
                # Clear memory for clean test
                # 清除记忆以进行干净的测试
                self.agent.memory.clear()
                
                # Step 1: Store
                # 步骤 1：存储
                store_response = self.agent.run_with_memory(store_input)
                if store_response is None:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=store_input,
                        error="Failed to store to memory"
                    ))
                    continue
                
                # Step 2: Query
                # 步骤 2：查询
                query_response = self.agent.run_with_memory(query_input)
                if query_response is None:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=query_input,
                        error="Failed to query memory"
                    ))
                    continue
                
                # Step 3: Check response contains expected info
                # 步骤 3：检查响应是否包含预期信息
                reply = query_response.get("reply", "")
                if expected_substring.lower() in reply.lower():
                    suite.add_result(EvalResult(
                        passed=True,
                        input=f"{store_input} → {query_input}",
                        expected=expected_substring,
                        actual=reply
                    ))
                else:
                    suite.add_result(EvalResult(
                        passed=False,
                        input=f"{store_input} → {query_input}",
                        expected=expected_substring,
                        actual=reply,
                        error="Expected content not in response"
                    ))
                    
            except Exception as e:
                suite.add_result(EvalResult(
                    passed=False,
                    input=store_input,
                    error=str(e)
                ))
        
        return suite
    
    def run_all(self, 
                structured_cases: list[dict] = None,
                tool_cases: list[dict] = None,
                decision_cases: list[dict] = None,
                memory_cases: list[dict] = None) -> list[EvalSuiteResult]:
        """
        Run all eval suites.
        
        运行所有评估套件。
        
        Args:
            structured_cases: Cases for structured output testing
                              用于结构化输出测试的用例
            tool_cases: Cases for tool call testing
                        用于工具调用测试的用例
            decision_cases: Cases for decision testing
                            用于决策测试的用例
            memory_cases: Cases for memory testing
                          用于记忆测试的用例
            
        Returns:
            List of all EvalSuiteResults
            
            返回：
            所有 EvalSuiteResult 的列表
        """
        results = []
        
        if structured_cases:
            results.append(self.test_structured_output(structured_cases))
        
        if tool_cases:
            results.append(self.test_tool_calls(tool_cases))
        
        if decision_cases:
            results.append(self.test_decisions(decision_cases))
        
        if memory_cases:
            results.append(self.test_memory_cycle(memory_cases))
        
        return results


def print_eval_report(results: list[EvalSuiteResult]):
    """
    Print a formatted eval report.
    
    打印格式化的评估报告。
    
    Args:
        results: List of EvalSuiteResults to report
                 要报告的 EvalSuiteResult 列表
    """
    print("\n" + "="*50)
    print("EVAL REPORT")
    print("="*50)
    
    total_passed = 0
    total_failed = 0
    
    for suite in results:
        print(f"\n{suite.summary()}")
        
        # Show failures
        # 显示失败
        for result in suite.results:
            if not result.passed:
                print(f"  ✗ Input: {result.input[:50]}...")
                if result.expected:
                    print(f"    Expected: {result.expected}")
                if result.actual:
                    print(f"    Actual: {result.actual}")
                if result.error:
                    print(f"    Error: {result.error}")
        
        total_passed += suite.passed
        total_failed += suite.failed
    
    print("\n" + "-"*50)
    overall = "✓ ALL PASSED" if total_failed == 0 else f"✗ {total_failed} FAILED"
    print(f"Overall: {overall} ({total_passed}/{total_passed + total_failed})")
    print("="*50)
