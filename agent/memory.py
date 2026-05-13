"""
Agent memory system.

智能体记忆系统。

Memory is explicit storage, not consciousness.
It's data that persists across agent steps and can be queried.

记忆是显式存储，而非意识。
它是跨智能体步骤持久存在并可被查询的数据。
"""


class Memory:
    """
    Simple memory storage for the agent.
    
    智能体的简单记忆存储。
    
    This is intentionally basic and grows in lessons:
    - Lesson 07: Basic list-based memory
    - Future: Add semantic search, persistence, etc.
    
    这是有意保持基础的，并在课程中成长：
    - 第 07 课：基于列表的基础记忆
    - 未来：添加语义搜索、持久化等
    """
    
    def __init__(self):
        """Initialize empty memory.
        
        初始化空记忆。
        """
        self.items = []
    
    def add(self, item: str):
        """
        Add an item to memory.
        
        向记忆中添加一项。
        
        Args:
            item: String to remember
                  要记住的字符串
        """
        if item and item not in self.items:
            self.items.append(item)
    
    def get_all(self) -> list[str]:
        """
        Retrieve all memory items.
        
        检索所有记忆项。
        
        Returns:
            List of all stored items
            
            返回：
            所有存储项的列表
        """
        return self.items.copy()
    
    def get_recent(self, n: int = 5) -> list[str]:
        """
        Get the n most recent memory items.
        
        获取 n 个最近的记忆项。
        
        Args:
            n: Number of recent items to retrieve
               要检索的最近项数
            
        Returns:
            List of recent items
            
            返回：
            最近项的列表
        """
        return self.items[-n:] if self.items else []
    
    def search(self, query: str) -> list[str]:
        """
        Simple search through memory items.
        
        简单地搜索记忆项。
        
        Args:
            query: String to search for
                   要搜索的字符串
            
        Returns:
            List of items containing the query
            
            返回：
            包含查询的项的列表
        """
        query_lower = query.lower()
        return [item for item in self.items if query_lower in item.lower()]
    
    def clear(self):
        """Clear all memory.
        
        清除所有记忆。
        """
        self.items = []
    
    def __len__(self) -> int:
        """Return the number of items in memory.
        
        返回记忆中的项目数。
        """
        return len(self.items)
    
    def __repr__(self) -> str:
        """String representation of memory.
        
        记忆的字符串表示。
        """
        return f"Memory({len(self.items)} items)"