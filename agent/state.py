"""
Agent state management.

智能体状态管理。

State is explicit, inspectable, and modifiable.
It's not hidden in conversation history or mysterious context.

状态是显式的、可检查的、可修改的。
它不隐藏在对话历史或神秘的上下文中。
"""


class AgentState:
    """
    Represents the current state of the agent.
    
    代表智能体的当前状态。
    
    This grows throughout the lessons as we add capabilities:
    - Lesson 06: Basic state (steps, done)
    - Lesson 07: Add memory tracking
    - Lesson 08: Add planning state
    - Lesson 09: Add execution state
    - Lesson 10: Add dependency tracking
    
    随着我们添加能力，这在整个课程中成长：
    - 第 06 课：基础状态（步骤、完成）
    - 第 07 课：添加记忆跟踪
    - 第 08 课：添加规划状态
    - 第 09 课：添加执行状态
    - 第 10 课：添加依赖跟踪
    """
    
    def __init__(self):
        """Initialize a new agent state.
        
        初始化新的智能体状态。
        """
        self.steps = 0
        self.done = False
        self.current_plan = None
        self.last_action = None
    
    def increment_step(self):
        """Increment the step counter.
        
        递增步骤计数器。
        """
        self.steps += 1
    
    def mark_done(self):
        """Mark the agent's task as complete.
        
        将智能体的任务标记为已完成。
        """
        self.done = True
    
    def reset(self):
        """Reset the state for a new task.
        
        为新任务重置状态。
        """
        self.steps = 0
        self.done = False
        self.current_plan = None
        self.last_action = None
    
    def to_dict(self) -> dict:
        """
        Convert state to a dictionary for serialization or prompts.
        
        将状态转换为字典以进行序列化或提示。
        
        Returns:
            Dictionary representation of the state
            
            返回：
            状态的字典表示
        """
        return {
            "steps": self.steps,
            "done": self.done,
            "current_plan": self.current_plan,
            "last_action": self.last_action,
        }
    
    def __repr__(self) -> str:
        """String representation of the state.
        
        状态的字符串表示。
        """
        return f"AgentState(steps={self.steps}, done={self.done})"