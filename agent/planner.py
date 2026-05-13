"""
Planning functionality for the agent.

智能体的规划功能。

Planning is data generation, not reasoning.
Plans are inspectable, modifiable data structures.

规划是数据生成，而非推理。
计划是可检查、可修改的数据结构。
"""

from shared.llm import LocalLLM


def create_plan(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate a plan to achieve a goal.
    
    生成实现目标的计划。
    
    Used in: Lesson 08
    
    Args:
        llm: The language model to use
             要使用的语言模型
        goal: The goal to achieve
              要实现的目标
        
    Returns:
        Plan as a dictionary with a "steps" list, or None if generation failed
        
        返回：
        包含 "steps" 列表的计划字典，或如果生成失败则返回 None
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


def create_atomic_action(llm: LocalLLM, step: str) -> dict | None:
    """
    Convert a plan step into an atomic action.
    
    将计划步骤转换为原子动作。
    
    Used in: Lesson 09
    
    Args:
        llm: The language model to use
             要使用的语言模型
        step: A step from a plan
              计划中的一个步骤
        
    Returns:
        Atomic action as a dictionary, or None if generation failed
        
        返回：
        作为字典的原子动作，或如果生成失败则返回 None
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


def create_aot_graph(llm: LocalLLM, goal: str) -> dict | None:
    """
    Generate an Atom of Thought (AoT) execution graph.
    
    生成思维原子（AoT）执行图。
    
    Used in: Lesson 10
    
    Args:
        llm: The language model to use
             要使用的语言模型
        goal: The goal to achieve
              要实现的目标
        
    Returns:
        AoT graph with nodes and dependencies, or None if generation failed
        
        返回：
        带有节点和依赖关系的 AoT 图，或如果生成失败则返回 None
    """
    from shared.utils import extract_json_from_text
    
    prompt = f"""Create an atomic execution graph for the goal. Each node is a single action. Dependencies are node IDs. Respond with ONLY valid JSON.

CRITICAL INSTRUCTIONS:
1. Respond with ONLY valid JSON
2. No explanations, no markdown, no other text
3. Start your response with {{ and end with }}

Required JSON format:
{{"nodes": [{{"id": "1", "action": "research", "depends_on": []}}, {{"id": "2", "action": "write", "depends_on": ["1"]}}]}}

Each node must have:
- id: unique string like "1", "2", "3"
- action: what to do (e.g., "research", "write", "review")
- depends_on: list of node IDs that must complete first (empty [] for first step)

Goal: {goal}

Response (JSON only):"""
    
    for attempt in range(3):
        response = llm.generate(prompt, temperature=0.0)
        graph = extract_json_from_text(response)
        
        if graph and "nodes" in graph and isinstance(graph["nodes"], list):
            # Validate graph structure
            # 验证图结构
            valid_nodes = []
            for node in graph["nodes"]:
                if isinstance(node, dict) and "id" in node and "action" in node and "depends_on" in node:
                    # Ensure depends_on is a list
                    # 确保 depends_on 是一个列表
                    if not isinstance(node["depends_on"], list):
                        continue
                    valid_nodes.append(node)
            
            if valid_nodes:
                return {"nodes": valid_nodes}
    
    return None


def execute_graph(graph: dict, executor_func) -> list:
    """
    Execute an AoT graph respecting dependencies.
    
    遵守依赖关系执行 AoT 图。
    
    Args:
        graph: AoT graph with nodes and dependencies
               带有节点和依赖关系的 AoT 图
        executor_func: Function to execute each action (takes action string)
                       用于执行每个行动的函数（接受行动字符串）
        
    Returns:
        List of execution results in order
        
        返回：
        按顺序排列的执行结果列表
    """
    if not graph or "nodes" not in graph:
        return []
    
    nodes = graph["nodes"]
    executed = set()
    results = []
    
    # Simple topological execution
    # 简单的拓扑执行
    # In a real implementation, this would be more sophisticated
    # 在实际实现中，这会更复杂
    max_iterations = len(nodes) * 2
    iteration = 0
    
    while len(executed) < len(nodes) and iteration < max_iterations:
        iteration += 1
        
        for node in nodes:
            node_id = node["id"]
            
            # Skip if already executed
            # 如果已经执行则跳过
            if node_id in executed:
                continue
            
            # Check if all dependencies are met
            # 检查是否满足所有依赖关系
            dependencies = node.get("depends_on", [])
            if all(dep in executed for dep in dependencies):
                # Execute the node
                # 执行节点
                try:
                    result = executor_func(node["action"])
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "result": result,
                        "success": True
                    })
                    executed.add(node_id)
                except Exception as e:
                    results.append({
                        "node_id": node_id,
                        "action": node["action"],
                        "error": str(e),
                        "success": False
                    })
                    # Mark as executed even on failure to avoid infinite loops
                    # 即使失败也标记为已执行，以避免无限循环
                    executed.add(node_id)
    
    return results