# Shared Code

# 共享代码

This folder contains small, boring helpers used by the agent.

这个文件夹包含智能体使用的小型、朴实的辅助工具。

## Files

## 文件

- **llm.py** - Minimal wrapper around llama-cpp-python
- **utils.py** - JSON parsing and text formatting helpers
- **prompts.py** - Prompt templates that evolve across lessons

- **llm.py** - 对 llama-cpp-python 的最小封装
- **utils.py** - JSON 解析和文本格式化辅助函数
- **prompts.py** - 在各课程中持续演进的提示词模板

## Philosophy

## 设计理念

Nothing clever lives here.

这里没有任何炫技的东西。

If something feels complex, it doesn't belong in this folder.

如果某件事感觉复杂，它就不属于这个文件夹。

These utilities exist to:
1. Reduce repetition
2. Keep lesson code focused
3. Maintain consistency

这些工具函数的存在是为了：
1. 减少重复
2. 保持课程代码的专注性
3. 维护一致性

They are intentionally simple and well-documented.

它们是有意保持简单并有完整文档的。