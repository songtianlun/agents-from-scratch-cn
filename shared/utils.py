"""
Utility functions for the agent.

智能体的工具函数。

These are boring, predictable helpers that do exactly what they say.
Nothing clever lives here.

这些是无聊、可预测的辅助函数，它们完全按照其名称所示工作。
这里没有任何炫技的东西。
"""

import json


def safe_json_parse(text: str) -> dict | None:
    """
    Safely parse JSON text, returning None on failure.
    
    Args:
        text: String that might be valid JSON
        
    Returns:
        Parsed JSON as a dictionary, or None if parsing fails
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None


def extract_json_from_text(text: str) -> dict | None:
    """
    Try to extract JSON from text that might have extra content.
    
    This handles cases where the model adds explanations before/after JSON.
    
    Args:
        text: Text that might contain JSON
        
    Returns:
        Parsed JSON if found, None otherwise
    """
    if not text:
        return None
    
    # Clean up the text - remove common markdown code blocks
    # 清理文本——删除常见的 Markdown 代码块
    text = text.strip()
    if text.startswith('```json'):
        text = text[7:]
    elif text.startswith('```'):
        text = text[3:]
    if text.endswith('```'):
        text = text[:-3]
    text = text.strip()
    
    # Remove common prefixes that models sometimes add
    # 删除模型有时会添加的常见前缀
    prefixes = ["JSON:", "Response:", "Answer:", "Here's the JSON:", "The JSON is:"]
    for prefix in prefixes:
        if text.startswith(prefix):
            text = text[len(prefix):].strip()
    
    # Try direct parsing first
    # 首先尝试直接解析
    result = safe_json_parse(text)
    if result is not None:
        return result
    
    # Try to find JSON between curly braces (most common case)
    # 尝试在花括号之间找到 JSON（最常见的情况）
    start = text.find('{')
    end = text.rfind('}')
    
    if start != -1 and end != -1 and end > start:
        json_text = text[start:end+1]
        result = safe_json_parse(json_text)
        if result is not None:
            return result
        
        # Try to fix common issues: unclosed strings, missing quotes
        # 尝试修复常见问题：未闭合的字符串、缺失引号
        # This is a simple heuristic - if we're close, try to fix it
        # 这是一个简单的启发式方法——如果我们接近了，尝试修复它
        if json_text.count('"') % 2 != 0:
            # Odd number of quotes - try to close the last string
            # 奇数个引号——尝试关闭最后一个字符串
            last_quote = json_text.rfind('"')
            if last_quote > 0:
                # Check if it's an opening quote
                # 检查它是否是开头引号
                before = json_text[:last_quote]
                if before.count('"') % 2 == 0:
                    # This might be an unclosed string, try adding a closing quote
                    # 这可能是一个未闭合的字符串，尝试添加结束引号
                    try_fix = json_text[:last_quote+1] + '"' + json_text[last_quote+1:] + '}'
                    result = safe_json_parse(try_fix)
                    if result is not None:
                        return result
    
    # Try to find JSON between square brackets (for arrays)
    # 尝试在方括号之间找到 JSON（对于数组）
    start = text.find('[')
    end = text.rfind(']')
    
    if start != -1 and end != -1 and end > start:
        json_text = text[start:end+1]
        result = safe_json_parse(json_text)
        if result is not None:
            return result
    
    # Last resort: try to extract key-value pairs from text
    # 最后手段：尝试从文本中提取键值对
    # This is very heuristic and may not work well
    # 这是非常启发式的，可能效果不佳
    if '{' in text or '[' in text:
        # Try to find any JSON-like structure
        # 尝试找到任何类似 JSON 的结构
        lines = text.split('\n')
        for line in lines:
            line = line.strip()
            if line.startswith('{') or line.startswith('['):
                result = safe_json_parse(line)
                if result is not None:
                    return result
    
    return None


def format_messages(messages: list[dict]) -> str:
    """
    Format a list of messages into a readable string.
    
    Args:
        messages: List of message dictionaries with 'role' and 'content' keys
        
    Returns:
        Formatted string representation
    """
    formatted = []
    for msg in messages:
        role = msg.get('role', 'unknown').upper()
        content = msg.get('content', '')
        formatted.append(f"[{role}]\n{content}\n")
    
    return "\n".join(formatted)