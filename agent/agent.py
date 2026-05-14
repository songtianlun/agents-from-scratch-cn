"""
The Agent - This file grows across all 10 lessons.

智能体 - 此文件在所有 10 课中持续成长。

This is the heart of the repository. Each lesson adds exactly one capability
to this agent, building understanding progressively.

这是仓库的核心。每课向此智能体添加恰好一个能力，
逐步构建理解。

Lesson progression:
01: Basic LLM chat
02: System prompts (roles)
03: Structured outputs (JSON)
04: Decision-making
05: Tool calling
06: Agent loop
07: Memory
08: Planning
09: Atomic actions
10: AoT (Atom of Thought)

课程进展：
01：基础 LLM 对话
02：系统提示词（角色）
03：结构化输出（JSON）
04：决策制定
05：工具调用
06：智能体循环
07：记忆
08：规划
09：原子动作
10：AoT（思维原子）
"""

from typing import Any

from shared.llm import LocalLLM
from shared.utils import extract_json_from_text
from agent.state import AgentState
from agent.memory import Memory
from agent.tools import get_tool_schema, execute_tool
from agent.planner import create_plan, create_atomic_action, create_aot_graph, execute_graph


class Agent:
    """
    An AI agent that grows in capability across lessons.
    
    一个在各课程中能力不断增长的 AI 智能体。
    
    This is the same agent throughout the repository - it just gains
    new methods and capabilities as lessons progress.
    
    这是整个仓库中同一个智能体——它只是随着课程进展获得
    新方法和能力。
    """
    
    def __init__(self, model_path: str):
        """
        Initialize the agent.
        
        初始化智能体。
        
        Args:
            model_path: Path to the GGUF model file
                        GGUF 模型文件的路径
        """
        # Lesson 01: Basic LLM interaction
        # 第 01 课：基础 LLM 交互
        self.llm = LocalLLM(model_path)
        
        # Lesson 02: System prompt for consistent behavior
        # 第 02 课：用于一致行为的系统提示词
        self.system_prompt = (
            "You are a calm, precise, and helpful AI assistant. "
            "You explain concepts simply and avoid unnecessary jargon. "
            "You are honest about what you know and don't know."
        )
        
        # Lesson 06: Agent state
        # 第 06 课：智能体状态
        self.state = AgentState()
        
        # Lesson 07: Memory system
        # 第 07 课：记忆系统
        self.memory = Memory()
    
    # ============================================================
    # LESSON 01: Basic LLM Chat
    # ============================================================
    
    def simple_generate(self, user_input: str) -> str:
        """
        Simplest possible interaction - just pass text to the LLM.
        
        最简单的交互——只是将文本传递给 LLM。
        
        Lesson 01 version.
        
        Args:
            user_input: The user's question or request
                        用户的问题或请求
            
        Returns:
            The model's response
            
            返回：
            模型的响应
        """
        return self.llm.generate(user_input)
    
    # ============================================================
    # LESSON 02: System Prompts (Roles)
    # ============================================================
    
    def generate_with_role(self, user_input: str) -> str:
        """
        Generate with a system prompt to shape behavior.
        
        使用系统提示词来塑造行为进行生成。
        
        Lesson 02 version.
        
        Args:
            user_input: The user's question or request
                        用户的问题或请求
            
        Returns:
            The model's response with role-based behavior
            
            返回：
            带有基于角色行为的模型响应
        """
        # Use a format that doesn't confuse the model
        # 使用不会让模型困惑的格式
        prompt = f"""{self.system_prompt}

User: {user_input}
Assistant:"""
        
        response = self.llm.generate(prompt)
        # Clean up any potential tag artifacts
        # 清除可能出现的标签残留
        response = response.replace('<SYSTEM>', '').replace('</SYSTEM>', '')
        response = response.replace('<USER>', '').replace('</USER>', '')
        return response.strip()
    
    # ============================================================
    # LESSON 03: Structured Outputs
    # ============================================================
    
    def generate_structured(self, user_input: str, schema: str) -> dict | None:
        """
        Generate structured JSON output with validation and retries.
        
        生成带有验证和重试的结构化 JSON 输出。
        
        Lesson 03 version.
        
        Args:
            user_input: The user's question or request
                        用户的问题或请求
            schema: JSON schema description
                    JSON 模式描述
            
        Returns:
            Parsed JSON dictionary or None if all retries failed
            
            返回：
            解析后的 JSON 字典，或如果所有重试均失败则返回 None
        """
        prompt = f"""{self.system_prompt}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no extra text before or after the JSON
3. Start your response with {{ and end with }}

Schema you must follow:
{schema}

User request: {user_input}

Response (JSON only):"""
        
        # Try up to 3 times
        # 最多尝试 3 次
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)
            
            if parsed is not None:
                return parsed
        
        return None
    
    # ============================================================
    # LESSON 04: Decision Making
    # ============================================================
    
    def decide(self, user_input: str, choices: list[str]) -> str | None:
        """
        Make the model choose from a finite set of options.
        
        使模型从有限的选项集中选择。
        
        Lesson 04 version.
        
        Args:
            user_input: The input to make a decision about
                        要做出决策的输入
            choices: List of possible actions/decisions
                     可能的行动/决策列表
            
        Returns:
            The chosen action or None if decision failed
            
            返回：
            所选行动，或如果决策失败则返回 None
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
    
    # ============================================================
    # LESSON 05: Tools
    # ============================================================
    
    def request_tool(self, user_input: str) -> dict | None:
        """
        Have the model request a tool call.
        
        让模型请求工具调用。
        
        Lesson 05 version.
        
        Args:
            user_input: The user's request
                        用户的请求
            
        Returns:
            Tool call specification or None if request failed
            
            返回：
            工具调用规范，或如果请求失败则返回 None
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
        
        执行模型请求的工具调用。
        
        Args:
            tool_call: Dictionary with "tool" and "arguments"
                       包含 "tool" 和 "arguments" 的字典
            
        Returns:
            Result of the tool execution
            
            返回：
            工具执行的结果
        """
        return execute_tool(tool_call["tool"], tool_call["arguments"])
    
    # ============================================================
    # LESSON 06: Agent Loop
    # ============================================================
    
    def agent_step(self, user_input: str) -> dict | None:
        """
        Execute one step of the agent loop: observe → decide → act.
        
        执行智能体循环的一个步骤：观察 → 决策 → 行动。
        
        Lesson 06 version.
        
        Args:
            user_input: User's input or system observation
                        用户输入或系统观察
            
        Returns:
            Action decision or None if step failed
            
            返回：
            行动决策，或如果步骤失败则返回 None
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
        
        运行智能体循环多个步骤。
        
        Args:
            user_input: Initial user input
                        初始用户输入
            max_steps: Maximum number of steps to execute
                       要执行的最大步骤数
            
        Returns:
            List of action results
            
            返回：
            行动结果列表
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
    
    # ============================================================
    # LESSON 07: Memory
    # ============================================================
    
    def run_with_memory(self, user_input: str) -> dict | None:
        """
        Run agent with memory context.
        
        带记忆上下文运行智能体。
        
        Lesson 07 version.
        
        Args:
            user_input: User's input
                        用户输入
            
        Returns:
            Response with potential memory update
            
            返回：
            带有潜在记忆更新的响应
        """
        memory_context = self.memory.get_all()
        
        # Build memory context string
        # 构建记忆上下文字符串
        if memory_context:
            memory_str = "You remember the following:\n" + "\n".join(f"- {item}" for item in memory_context)
        else:
            memory_str = "You have no memories yet."
        
        prompt = f"""{self.system_prompt}

You are an agent with memory. You must respond with ONLY valid JSON.

{memory_str}

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}
4. If the user tells you information (like their name), save it to memory
5. If the user asks about something you remember, USE YOUR MEMORY to answer

Required JSON format:
{{"reply": "your response text", "save_to_memory": "fact to remember" or null}}

Examples:
- User says "My name is Alice" → {{"reply": "Nice to meet you, Alice!", "save_to_memory": "User's name is Alice"}}
- User asks "What's my name?" and you remember "User's name is Alice" → {{"reply": "Your name is Alice", "save_to_memory": null}}

User input: {user_input}

Response (JSON only):"""
        
        for attempt in range(3):
            response = self.llm.generate(prompt, temperature=0.0)
            parsed = extract_json_from_text(response)
            
            if parsed and "reply" in parsed:
                # Save to memory if requested
                # 如果需要，保存到记忆
                if parsed.get("save_to_memory"):
                    self.memory.add(parsed["save_to_memory"])
                
                self.state.increment_step()
                return parsed
        
        return None
    
    # ============================================================
    # LESSON 08: Planning
    # ============================================================
    
    def create_plan(self, goal: str) -> dict | None:
        """
        Generate a plan to achieve a goal.
        
        生成实现目标的计划。
        
        Lesson 08 version.
        
        Args:
            goal: The goal to achieve
                  要实现的目标
            
        Returns:
            Plan with steps
            
            返回：
            包含步骤的计划
        """
        plan = create_plan(self.llm, goal)
        
        if plan:
            self.state.current_plan = plan
        
        return plan
    
    def execute_plan(self, plan: dict) -> list:
        """
        Execute a plan step by step.
        
        逐步执行计划。
        
        Args:
            plan: Plan dictionary with "steps" list
                  包含 "steps" 列表的计划字典
            
        Returns:
            List of execution results
            
            返回：
            执行结果列表
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
    
    # ============================================================
    # LESSON 09: Atomic Actions
    # ============================================================
    
    def create_atomic_action(self, step: str) -> dict | None:
        """
        Convert a plan step into an atomic action.
        
        将计划步骤转换为原子动作。
        
        Lesson 09 version.
        
        Atomic actions are the smallest possible actions that can be:
        - Validated independently
        - Tested in isolation
        - Executed safely
        - Rolled back if needed
        
        原子动作是可以被：
        - 独立验证
        - 隔离测试
        - 安全执行
        - 如有需要可回滚
        
        的最小可能行动。
        
        Args:
            step: A step from a plan (e.g., "Write an explanation of AI agents")
                  计划中的一个步骤（例如，"Write an explanation of AI agents"）
            
        Returns:
            Atomic action dictionary with "action" and "inputs", or None if generation failed
            
            返回：
            包含 "action" 和 "inputs" 的原子动作字典，或如果生成失败则返回 None
        """
        return create_atomic_action(self.llm, step)
    
    # ============================================================
    # LESSON 10: Atom of Thought (AoT)
    # ============================================================
    
    def create_aot_plan(self, goal: str) -> dict | None:
        """
        Generate an AoT execution graph.
        
        生成 AoT 执行图。
        
        Lesson 10 version.
        
        Args:
            goal: The goal to achieve
                  要实现的目标
            
        Returns:
            AoT graph with atomic nodes and dependencies
            
            返回：
            带有原子节点和依赖关系的 AoT 图
        """
        return create_aot_graph(self.llm, goal)
    
    def execute_aot_plan(self, graph: dict) -> list:
        """
        Execute an AoT graph respecting dependencies.
        
        遵守依赖关系执行 AoT 图。
        
        Args:
            graph: AoT graph
                   AoT 图
            
        Returns:
            List of execution results
            
            返回：
            执行结果列表
        """
        def execute_action(action: str):
            # Placeholder for actual action execution
            # 实际行动执行的占位符
            return f"Executed: {action}"
        
        return execute_graph(graph, execute_action)
    
    # ============================================================
    # MAIN RUN METHOD (evolves across lessons)
    # ============================================================
    
    def run(self, user_input: str) -> str:
        """
        Main entry point for the agent.
        
        This method evolves across lessons to use different capabilities.
        Currently, at: Lesson 07 (with memory)
        
        Args:
            user_input: The user's question or request
            
        Returns:
            The agent's response
        """
        result = self.run_with_memory(user_input)
        
        if result and "reply" in result:
            return result["reply"]
        
        # Fallback to simple generation
        return self.generate_with_role(user_input)