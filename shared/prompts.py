"""
Prompt templates for the agent.

智能体的提示词模板。

These functions build prompts that evolve across lessons:
- Lesson 01: base_prompt (just text)
- Lesson 02: system_prompt (add role)
- Lesson 03: json_contract (add structure)
- Lesson 04+: specialized prompts for decisions, tools, planning

这些函数构建了在各课程中演进的提示词：
- 第 01 课：base_prompt（纯文本）
- 第 02 课：system_prompt（添加角色）
- 第 03 课：json_contract（添加结构）
- 第 04 课+：用于决策、工具、规划的专用提示词

Prompts are first-class citizens in agent systems.

提示词在智能体系统中是一等公民。
"""


def base_prompt(user_input: str) -> str:
    """
    The simplest possible prompt - just the user's text.
    
    最简单的提示词——只是用户的文本。
    
    Used in: Lesson 01
    
    Args:
        user_input: The user's question or request
                    用户的问题或请求
        
    Returns:
        Unmodified user input
        
        返回：
        未修改的用户输入
    """
    return user_input


def system_prompt(role: str, user_input: str) -> str:
    """
    Add a system role to shape behavior.
    
    添加系统角色以塑造行为。
    
    Used in: Lesson 02
    
    Args:
        role: Description of the assistant's role and behavior
              助手角色和行为的描述
        user_input: The user's question or request
                    用户的问题或请求
        
    Returns:
        Formatted prompt with system and user sections
        
        返回：
        包含系统和用户部分的格式化提示词
    """
    return f"""<SYSTEM>
{role}
</SYSTEM>

<USER>
{user_input}
</USER>"""


def json_contract(schema: str, content: str) -> str:
    """
    Enforce structured JSON output.
    
    强制执行结构化 JSON 输出。
    
    Used in: Lesson 03
    
    Args:
        schema: JSON schema description
                JSON 模式描述
        content: The content to process
                 要处理的内容
        
    Returns:
        Prompt that enforces JSON output
        
        返回：
        强制 JSON 输出的提示词
    """
    return f"""Return ONLY valid JSON.
No explanations. No markdown. No extra text.

Schema:
{schema}

Content:
{content}"""


def decision_prompt(choices: list[str], user_input: str) -> str:
    """
    Make the model choose from a finite set of options.
    
    使模型从有限的选项集中选择。
    
    Used in: Lesson 04
    
    Args:
        choices: List of possible actions/decisions
                 可能的行动/决策列表
        user_input: The input to make a decision about
                    要做出决策的输入
        
    Returns:
        Prompt that enforces decision-making
        
        返回：
        强制决策的提示词
    """
    options = "\n".join(f"- {choice}" for choice in choices)
    
    return f"""You must choose ONE of the following options.
Return ONLY valid JSON.

Available choices:
{options}

Schema:
{{ "decision": string }}

Input:
{user_input}"""


def tool_call_prompt(tools: dict, user_input: str) -> str:
    """
    Request a tool call from the model.
    
    从模型请求工具调用。
    
    Used in: Lesson 05
    
    Args:
        tools: Dictionary of available tools and their schemas
               可用工具及其模式的字典
        user_input: The user's request
                    用户的请求
        
    Returns:
        Prompt that requests a tool call
        
        返回：
        请求工具调用的提示词
    """
    return f"""You may request ONE tool call.

Available tools:
{tools}

Return ONLY valid JSON.

Schema:
{{
  "tool": string,
  "arguments": object
}}

User request:
{user_input}"""


def agent_step_prompt(state: dict, user_input: str) -> str:
    """
    Generate the next agent action based on current state.
    
    基于当前状态生成下一个智能体行动。
    
    Used in: Lesson 06
    
    Args:
        state: Current agent state
               当前智能体状态
        user_input: User's input or system observation
                    用户输入或系统观察
        
    Returns:
        Prompt for agent step execution
        
        返回：
        用于智能体步骤执行的提示词
    """
    return f"""You are an agent.

Current state:
{state}

Decide the next action.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "reason": string
}}

User input:
{user_input}"""


def memory_prompt(state: dict, memory: list, user_input: str) -> str:
    """
    Agent prompt with memory context.
    
    带有记忆上下文的智能体提示词。
    
    Used in: Lesson 07
    
    Args:
        state: Current agent state
               当前智能体状态
        memory: List of relevant memories
                相关记忆列表
        user_input: User's input
                    用户输入
        
    Returns:
        Prompt with memory context
        
        返回：
        带有记忆上下文的提示词
    """
    return f"""You are an agent with memory.

Current state:
{state}

Relevant memory:
{memory}

Decide what to do next.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "save_to_memory": string | null
}}

User input:
{user_input}"""


def planning_prompt(goal: str) -> str:
    """
    Generate a plan to achieve a goal.
    
    生成实现目标的计划。
    
    Used in: Lesson 08
    
    Args:
        goal: The goal to achieve
              要实现的目标
        
    Returns:
        Prompt for plan generation
        
        返回：
        用于计划生成的提示词
    """
    return f"""Create a step-by-step plan to achieve the goal.

Return ONLY valid JSON.

Schema:
{{
  "steps": [string]
}}

Goal:
{goal}"""


def atomic_action_prompt(step: str) -> str:
    """
    Convert a plan step into an atomic action.
    
    将计划步骤转换为原子动作。
    
    Used in: Lesson 09
    
    Args:
        step: A step from a plan
              计划中的一个步骤
        
    Returns:
        Prompt to generate atomic action
        
        返回：
        用于生成原子动作的提示词
    """
    return f"""Convert this step into an atomic action.

Return ONLY valid JSON.

Schema:
{{
  "action": string,
  "inputs": object
}}

Step:
{step}"""


def aot_prompt(goal: str) -> str:
    """
    Generate an Atom of Thought execution graph.
    
    生成思维原子执行图。
    
    Used in: Lesson 10
    
    Args:
        goal: The goal to achieve
              要实现的目标
        
    Returns:
        Prompt for AoT graph generation
        
        返回：
        用于 AoT 图生成的提示词
    """
    return f"""Create an atomic execution graph for the goal.

Return ONLY valid JSON.

Schema:
{{
  "nodes": [
    {{
      "id": string,
      "action": string,
      "depends_on": [string]
    }}
  ]
}}

Goal:
{goal}"""