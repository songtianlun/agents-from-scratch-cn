"""
Tool definitions for the agent.

智能体的工具定义。

Tools are APIs, not abilities.
The agent requests tools; the system executes them.

工具是 API，而非能力。
智能体请求工具；系统执行它们。
"""

from typing import Any


def calculator(a: float, b: float, operation: str = "add") -> float:
    """
    Simple calculator tool.
    
    简单的计算器工具。
    
    Args:
        a: First number
           第一个数字
        b: Second number
           第二个数字
        operation: One of "add", "subtract", "multiply", "divide"
                   "add"、"subtract"、"multiply"、"divide" 之一
        
    Returns:
        Result of the operation
        
        返回：
        操作的结果
    """
    operations = {
        "add": lambda x, y: x + y,
        "subtract": lambda x, y: x - y,
        "multiply": lambda x, y: x * y,
        "divide": lambda x, y: x / y if y != 0 else float('inf'),
    }
    
    if operation not in operations:
        raise ValueError(f"Unknown operation: {operation}")
    
    return operations[operation](a, b)


def get_tool_schema() -> dict:
    """
    Get the schema for available tools.
    
    获取可用工具的模式。
    
    This is what the agent sees when deciding which tool to call.
    
    这是智能体在决定调用哪个工具时看到的内容。
    
    Returns:
        Dictionary of tool names to their schemas
        
        返回：
        工具名称到其模式的字典
    """
    return {
        "calculator": {
            "description": "Perform basic arithmetic operations",
            "parameters": {
                "a": {"type": "number", "description": "First number"},
                "b": {"type": "number", "description": "Second number"},
                "operation": {
                    "type": "string",
                    "enum": ["add", "subtract", "multiply", "divide"],
                    "description": "The operation to perform"
                }
            },
            "required": ["a", "b"]
        }
    }


def execute_tool(tool_name: str, arguments: dict) -> Any:
    """
    Execute a tool by name with given arguments.
    
    用给定参数按名称执行工具。
    
    Args:
        tool_name: Name of the tool to execute
                   要执行的工具名称
        arguments: Dictionary of arguments for the tool
                   工具参数的字典
        
    Returns:
        Result of the tool execution
        
        返回：
        工具执行的结果
        
    Raises:
        ValueError: If tool doesn't exist
        
    异常：
        ValueError: 如果工具不存在
    """
    tools = {
        "calculator": calculator,
    }
    
    if tool_name not in tools:
        raise ValueError(f"Unknown tool: {tool_name}")
    
    return tools[tool_name](**arguments)