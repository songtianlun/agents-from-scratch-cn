# Contributing to AI Agents from Scratch

# 为《从零开始构建 AI 智能体》做贡献

Thank you for your interest in contributing! This repository has a specific educational philosophy, so please read this guide carefully before contributing.

感谢你有兴趣为本项目做贡献！本仓库有特定的教育理念，请在贡献之前仔细阅读本指南。

## Philosophy First

## 理念优先

This repository prioritizes:
1. **Clarity over cleverness**
2. **Progressive complexity**
3. **Mechanical understanding**
4. **No magic, no hype**

本仓库优先考虑：
1. **清晰胜过巧妙**
2. **渐进式复杂性**
3. **机械化理解**
4. **无魔法，无炒作**

Every contribution should make the learning experience **better**, not just add features.

每次贡献都应该让学习体验**更好**，而不仅仅是添加功能。

## What We Welcome

## 我们欢迎的贡献

### ✅ Good Contributions

### ✅ 好的贡献

- **Bug fixes** in existing code
- **Clarifications** in lesson explanations
- **Better examples** that illustrate concepts
- **Additional exercises** at the end of lessons
- **Documentation improvements**
- **Typo fixes and grammar improvements**
- **Translation** of lessons to other languages

- 现有代码中的**缺陷修复**
- 课程解释中的**澄清说明**
- 能更好说明概念的**更好示例**
- 课程末尾的**附加练习**
- **文档改进**
- **错别字和语法修正**
- 课程的**翻译**

### ⚠️ Needs Discussion First

### ⚠️ 需要先讨论

These might be good ideas, but need careful thought:
- **New lessons** - must fit the progression
- **Alternative approaches** - must preserve simplicity
- **Framework integrations** - goes against the philosophy
- **Advanced features** - might break the learning flow

这些可能是好主意，但需要仔细考虑：
- **新课节** - 必须符合课程进度
- **替代方案** - 必须保持简洁性
- **框架集成** - 违背了本仓库的理念
- **高级功能** - 可能破坏学习流程

### ❌ We Will Not Accept

### ❌ 我们不会接受

- Additions that require external APIs
- Framework dependencies (LangChain, CrewAI, etc.)
- "Smart" abstractions that hide mechanisms
- Chain-of-thought or hidden reasoning
- Anthropomorphic language ("the agent thinks...")
- Hype-driven features without pedagogical value

- 需要外部 API 的添加内容
- 框架依赖（LangChain、CrewAI 等）
- 隐藏机制的"智能"抽象
- 思维链或隐藏推理
- 拟人化语言（"智能体认为..."）
- 没有教学价值的炒作功能

## Contribution Guidelines

## 贡献指南

### 1. Code Style

### 1. 代码风格

**Python Code:**
- Follow PEP 8
- Use type hints
- Write docstrings for all functions
- Prefer readability over brevity
- Comment "why," not "what"

**Python 代码：**
- 遵循 PEP 8
- 使用类型注解
- 为所有函数编写文档字符串
- 可读性优先，简洁性次之
- 注释"为什么"，而不是"是什么"

**Example:**
```python
def safe_json_parse(text: str) -> dict | None:
    """
    Safely parse JSON text, returning None on failure.
    
    This handles the common case where LLMs add extra text
    around JSON, making direct parsing fail.
    """
    try:
        return json.loads(text)
    except (json.JSONDecodeError, TypeError):
        return None
```

### 2. Lesson Writing Style

### 2. 课程写作风格

**Principles:**
- Start with the question being answered
- Introduce one concept at a time
- Use concrete examples
- Avoid jargon without explanation
- End with key takeaways

**原则：**
- 从要回答的问题开始
- 一次介绍一个概念
- 使用具体示例
- 避免未解释的术语
- 以关键要点结束

**Structure:**
```markdown
# Lesson XX  -  Title

## What Question Are We Answering?

## What You Will Build

## New Concepts Introduced

## What We Are NOT Doing (Yet)

## The Code

## How to Run

## Key Insights

## Common Issues

## Exercises

## What's Next?

---

**Key Takeaway:**
```

**结构：**
```markdown
# 第 XX 课  -  标题

## 我们在回答什么问题？

## 你将构建什么

## 引入的新概念

## 我们（暂时）不做什么

## 代码

## 如何运行

## 关键见解

## 常见问题

## 练习

## 下一步是什么？

---

**关键要点：**
```

### 3. Commit Messages

### 3. 提交信息

Use clear, descriptive commit messages:

使用清晰、描述性的提交信息：

```
Good:
- "Fix JSON parsing in lesson 03 example"
- "Clarify memory explanation in lesson 07"
- "Add exercise for testing different temperatures"

Bad:
- "Update"
- "Fix bug"
- "Changes"
```

```
好的：
- "修复第 03 课示例中的 JSON 解析问题"
- "澄清第 07 课中的记忆解释"
- "添加测试不同温度的练习"

不好的：
- "更新"
- "修复缺陷"
- "改动"
```

## How to Contribute

## 如何贡献

### 1. Small Changes (Typos, Small Fixes)

### 1. 小改动（错别字、小修复）

For small changes:
1. Fork the repository
2. Make your changes
3. Submit a pull request with a clear description

对于小改动：
1. Fork 本仓库
2. 进行你的更改
3. 提交一个有清晰描述的 pull request

### 2. Larger Changes (New Examples, Lessons)

### 2. 较大改动（新示例、新课程）

For larger contributions:
1. **Open an issue first** to discuss the idea
2. Wait for maintainer feedback
3. If approved, fork and implement
4. Submit a pull request

对于较大的贡献：
1. **首先开一个 issue** 讨论想法
2. 等待维护者的反馈
3. 获批后，Fork 并实现
4. 提交 pull request

### 3. Testing Your Changes

### 3. 测试你的更改

Before submitting:
- Test all code examples work
- Verify markdown renders correctly
- Check that changes don't break the lesson progression
- Run through the lessons as a learner would

提交之前：
- 测试所有代码示例是否正常工作
- 验证 Markdown 渲染是否正确
- 检查更改是否不会破坏课程进度
- 像学习者一样过一遍课程

## Code Review Process

## 代码审查流程

We will review for:
1. **Pedagogical value** - Does this help learning?
2. **Simplicity** - Is it as simple as possible?
3. **Consistency** - Does it fit the existing style?
4. **Correctness** - Does the code work?

我们将审查：
1. **教学价值** - 这有助于学习吗？
2. **简洁性** - 它尽可能简单吗？
3. **一致性** - 它符合现有风格吗？
4. **正确性** - 代码能正常工作吗？

## Questions?

## 有问题？

- **For bugs:** Open an issue with steps to reproduce
- **For features:** Open an issue to discuss first
- **For questions:** Use GitHub Discussions

- **关于缺陷：** 开一个 issue，附上复现步骤
- **关于功能：** 先开一个 issue 讨论
- **关于问题：** 使用 GitHub Discussions

## Recognition

## 致谢

Contributors will be:
- Added to CONTRIBUTORS.md
- Mentioned in release notes
- Credited in the repository

贡献者将会：
- 被添加到 CONTRIBUTORS.md
- 在发布说明中被提及
- 在仓库中获得致谢

Thank you for helping make AI agent education better!

感谢你帮助改善 AI 智能体教育！