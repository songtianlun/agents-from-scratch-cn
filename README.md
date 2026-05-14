# AI Agents from Scratch

# 从零开始构建 AI 智能体

A gentle, local-first introduction to AI agents.

一份循序渐进、以本地运行为核心的 AI 智能体入门教程。

This repository teaches how AI agents actually work by building **one agent** step by step from a single local LLM call.

本仓库通过从单次本地 LLM 调用出发，逐步构建**同一个智能体**，来教你 AI 智能体究竟是如何工作的。

**No frameworks. No cloud APIs. No hidden reasoning. No magic.**

**无框架。无云端 API。无隐藏推理。无魔法。**


## Related Projects

## 相关项目

### [AI Product from Scratch](https://github.com/pguso/ai-product-from-scratch)

[![TypeScript](https://img.shields.io/badge/TypeScript-007ACC?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-20232A?logo=react&logoColor=61DAFB)](https://reactjs.org/)
[![Node.js](https://img.shields.io/badge/Node.js-339933?logo=node.js&logoColor=white)](https://nodejs.org/)

Learn AI product development fundamentals with local LLMs. Covers prompt engineering, structured output, multi-step reasoning, API design, and frontend integration through 10 comprehensive lessons with visual diagrams.

使用本地 LLM 学习 AI 产品开发基础。通过 10 节配有可视化图表的综合课程，涵盖提示词工程、结构化输出、多步骤推理、API 设计以及前端集成。

### [AI Agents from Scratch in JavaScript](https://github.com/pguso/ai-agents-from-scratch) 

![Python](https://img.shields.io/badge/JavaScript-3776AB?logo=javascript&logoColor=yellow)

![Agent Architecture](diagrams/agent-architecture.png)

## Philosophy

## 设计理念

Agents are not personalities. They are loops, state, and constraints.

智能体不是有个性的存在，而是由循环、状态和约束构成的系统。

If something feels like magic, open the file — there is no hidden logic in this repo.

如果某件事感觉像魔法，打开文件看看——本仓库没有任何隐藏逻辑。

## What You Will Learn

## 你将学到什么

This repository builds one continuously evolving agent across 12 lessons:

本仓库通过 12 节课，构建一个持续演进的智能体：

| Lesson | Capability Added | Link |
|--------|------------------|------|
| 01 | Text in / text out | [lessons/01_basic_llm_chat.md](lessons/01_basic_llm_chat.md) |
| 02 | Roles and behavior (system prompts) | [lessons/02_system_prompt.md](lessons/02_system_prompt.md) |
| 03 | Structured output (JSON contracts) | [lessons/03_structured_output.md](lessons/03_structured_output.md) |
| 04 | Decisions (routing logic) | [lessons/04_decision_making.md](lessons/04_decision_making.md) |
| 05 | Tools (external capabilities) | [lessons/05_tools.md](lessons/05_tools.md) |
| 06 | Agent loop (observe → decide → act) | [lessons/06_agent_loop.md](lessons/06_agent_loop.md) |
| 07 | Memory (short and long-term) | [lessons/07_memory.md](lessons/07_memory.md) |
| 08 | Planning (as data, not thoughts) | [lessons/08_planning.md](lessons/08_planning.md) |
| 09 | Atomic actions (safe execution) | [lessons/09_atomic_actions.md](lessons/09_atomic_actions.md) |
| 10 | AoT - Atom of Thought (dependency graphs) | [lessons/10_atom_of_thought.md](lessons/10_atom_of_thought.md) |
| 11 | Evals (regression testing) | [lessons/11_evals.md](lessons/11_evals.md) |
| 12 | Telemetry (runtime observability) | [lessons/12_telemetry.md](lessons/12_telemetry.md) |

| 课节 | 新增能力 | 链接 |
|------|---------|------|
| 01 | 文本输入 / 文本输出 | [lessons/01_basic_llm_chat.md](lessons/01_basic_llm_chat.md) |
| 02 | 角色与行为（系统提示词） | [lessons/02_system_prompt.md](lessons/02_system_prompt.md) |
| 03 | 结构化输出（JSON 契约） | [lessons/03_structured_output.md](lessons/03_structured_output.md) |
| 04 | 决策（路由逻辑） | [lessons/04_decision_making.md](lessons/04_decision_making.md) |
| 05 | 工具（外部能力） | [lessons/05_tools.md](lessons/05_tools.md) |
| 06 | 智能体循环（观察 → 决策 → 行动） | [lessons/06_agent_loop.md](lessons/06_agent_loop.md) |
| 07 | 记忆（短期与长期） | [lessons/07_memory.md](lessons/07_memory.md) |
| 08 | 规划（数据形式，而非思维） | [lessons/08_planning.md](lessons/08_planning.md) |
| 09 | 原子动作（安全执行） | [lessons/09_atomic_actions.md](lessons/09_atomic_actions.md) |
| 10 | AoT - 思维原子（依赖图） | [lessons/10_atom_of_thought.md](lessons/10_atom_of_thought.md) |
| 11 | 评估（回归测试） | [lessons/11_evals.md](lessons/11_evals.md) |
| 12 | 遥测（运行时可观测性） | [lessons/12_telemetry.md](lessons/12_telemetry.md) |

## Who This Is For

## 适合谁学习

**This repo is for:**
- Developers who can code but feel lost with agents
- People tired of "just use LangChain"
- Learners who want local models
- Engineers who want mechanical understanding
- Educators looking for a clean mental model

**本仓库适合：**
- 会写代码但对智能体感到困惑的开发者
- 厌倦了"直接用 LangChain"的人
- 希望使用本地模型的学习者
- 追求机械化理解的工程师
- 寻求清晰思维模型的教育者

**This repo is NOT for:**
- People looking for the fastest demo
- People who want a SaaS starter kit
- People who believe agents "think"
- People who want hidden chain-of-thought

**本仓库不适合：**
- 寻求最快演示效果的人
- 想要 SaaS 启动套件的人
- 相信智能体会"思考"的人
- 希望使用隐藏思维链的人

## Quick Start

## 快速开始

**For detailed setup instructions, see [QUICKSTART.md](QUICKSTART.md)**

**详细安装说明请参见 [QUICKSTART.md](QUICKSTART.md)**

In short:
1. Install dependencies: `pip install -r requirements.txt`
2. Download a GGUF model to the `models/` folder
3. Run: `python complete_example.py`

简而言之：
1. 安装依赖：`pip install -r requirements.txt`
2. 下载一个 GGUF 模型到 `models/` 目录
3. 运行：`python complete_example.py`

**Note:** The `complete_example.py` file contains executable code examples demonstrating all 12 lessons. You can use it as a reference to see how all the concepts fit together.

**注意：** `complete_example.py` 文件包含演示全部 12 节课的可运行代码示例，可作为参考，了解所有概念如何融合在一起。

## Repository Structure

## 仓库结构

```
ai-agents-from-scratch/
├─ README.md              # You are here
├─ philosophy.md          # Why this repo exists
├─ QUICKSTART.md          # Detailed setup guide
├─ complete_example.py    # Demonstrations of all 12 lessons
├─ requirements.txt       # Python dependencies
│
├─ models/                # Place GGUF models here
├─ shared/                # Reusable utilities (LLM, prompts, utils)
├─ agent/                 # The evolving agent implementation
│  ├─ agent.py             # Main agent class 
│  ├─ memory.py            # Memory system
│  ├─ planner.py           # Planning and atomic actions
│  ├─ state.py             # Agent state management
│  ├─ tools.py             # Tool definitions
│  ├─ evals.py             # Evaluation framework (Lesson 11)
│  └─ telemetry.py         # Telemetry system (Lesson 12)
├─ evals/                 # Golden datasets for testing
│  └─ golden_datasets.py   # Known-good test cases
└─ lessons/               # Step-by-step explanations (01-12)
```

```
ai-agents-from-scratch/
├─ README.md              # 你在这里 / You are here
├─ philosophy.md          # 本仓库存在的原因 / Why this repo exists
├─ QUICKSTART.md          # 详细安装指南 / Detailed setup guide
├─ complete_example.py    # 全部 12 节课的演示 / Demonstrations of all 12 lessons
├─ requirements.txt       # Python 依赖 / Python dependencies
│
├─ models/                # 放置 GGUF 模型 / Place GGUF models here
├─ shared/                # 可复用工具（LLM、提示词、工具函数） / Reusable utilities
├─ agent/                 # 持续演进的智能体实现 / The evolving agent implementation
│  ├─ agent.py             # 主智能体类 / Main agent class 
│  ├─ memory.py            # 记忆系统 / Memory system
│  ├─ planner.py           # 规划与原子动作 / Planning and atomic actions
│  ├─ state.py             # 智能体状态管理 / Agent state management
│  ├─ tools.py             # 工具定义 / Tool definitions
│  ├─ evals.py             # 评估框架（第11课） / Evaluation framework (Lesson 11)
│  └─ telemetry.py         # 遥测系统（第12课） / Telemetry system (Lesson 12)
├─ evals/                 # 测试用黄金数据集 / Golden datasets for testing
│  └─ golden_datasets.py   # 已知正确的测试用例 / Known-good test cases
└─ lessons/               # 逐步讲解（01-12） / Step-by-step explanations (01-12)
```

### Key Files Explained

### 关键文件说明

**`agent/agent.py`** - The heart of the repository
- Contains the `Agent` class that evolves across all 12 lessons
- Each lesson adds new methods and capabilities to this same class
- This is what you study and modify as you learn

**`agent/agent.py`** - 仓库的核心
- 包含在全部 12 节课中持续演进的 `Agent` 类
- 每节课都为该类添加新的方法和能力
- 学习过程中，你将研究并修改这个文件

**`complete_example.py`** - Learning reference
- Contains 12 separate functions, one for each lesson
- Each function demonstrates that lesson's concepts in isolation
- Use this to see how individual lessons work before combining them
- Run: `python complete_example.py`

**`complete_example.py`** - 学习参考
- 包含 12 个独立函数，每节课对应一个
- 每个函数单独演示该节课的概念
- 在组合使用之前，用它来了解各节课如何运作
- 运行：`python complete_example.py`

**`agent/evals.py`** - Regression testing (Lesson 11)
- Test your agent against known-good cases
- Catch prompt regressions before deployment

**`agent/evals.py`** - 回归测试（第 11 课）
- 用已知正确用例测试你的智能体
- 在部署前捕获提示词退化

**`agent/telemetry.py`** - Runtime observability (Lesson 12)
- Structured logging for debugging
- Track latency, success rates, and traces

**`agent/telemetry.py`** - 运行时可观测性（第 12 课）
- 用于调试的结构化日志
- 追踪延迟、成功率和调用链

**Relationship**: 
- `agent/agent.py` = the code you're learning (the implementation)
- `complete_example.py` = isolated examples of each lesson (for learning and experimentation)

**关系说明**：
- `agent/agent.py` = 你正在学习的代码（实现部分）
- `complete_example.py` = 每节课的独立示例（用于学习和实验）

## What This Repo Is Not

## 本仓库不是什么

- This is **not a framework**
- This is **not a chatbot demo**
- This does **not claim models think**
- This does **not expose chain-of-thought**
- This does **not require OpenAI or cloud APIs**

- 这**不是一个框架**
- 这**不是一个聊天机器人演示**
- 这**不声称模型会思考**
- 这**不暴露思维链**
- 这**不需要 OpenAI 或云端 API**

## Core Principles

## 核心原则

1. **One agent, many stages** - The same `agent.py` file grows across lessons
2. **Explicit over implicit** - No hidden logic, no magic abstractions
3. **Structure over prompting** - Reliability comes from constraints, not clever wording
4. **Local-first** - No API keys, no rate limits, no cloud dependency
5. **Educational, not production** - This teaches fundamentals, not best practices

1. **一个智能体，多个阶段** - 同一个 `agent.py` 文件在各课中不断成长
2. **显式优于隐式** - 没有隐藏逻辑，没有魔法抽象
3. **结构优于提示** - 可靠性来自约束，而非巧妙的措辞
4. **本地优先** - 无需 API 密钥，无速率限制，无云端依赖
5. **教育性，非生产性** - 教授基本原理，而非最佳实践

## Learning Path

## 学习路径

Each lesson builds on the previous one. **Do not skip ahead.**

每节课都在前一节的基础上构建。**不要跳跃前进。**

The curriculum is designed to build understanding gradually:
- Lessons 1-3: Foundation (LLM basics)
- Lessons 4-6: Agency (decisions, tools, loops)
- Lessons 7-10: Intelligence (memory, planning, execution)
- Lessons 11-12: Observability (evals, telemetry)

课程设计旨在逐步建立理解：
- 第 1-3 课：基础（LLM 基础知识）
- 第 4-6 课：智能体行为（决策、工具、循环）
- 第 7-10 课：智能化（记忆、规划、执行）
- 第 11-12 课：可观测性（评估、遥测）

## Contributing

## 贡献

This is an educational repository. Contributions should:
- Maintain the gentle, progressive learning style
- Keep code readable over clever
- Add explanations, not just features
- Preserve the "no framework" philosophy

这是一个教育性仓库。贡献内容应该：
- 保持循序渐进的学习风格
- 保持代码的可读性而非炫技
- 添加解释，而不仅仅是功能
- 维护"无框架"的理念

## License

## 许可证

MIT License - see LICENSE file

MIT 许可证 - 详见 LICENSE 文件

## Acknowledgments

## 致谢

This repository synthesizes best practices from modern agent development while deliberately avoiding complexity that obscures understanding.

本仓库汇总了现代智能体开发的最佳实践，同时有意规避了那些会掩盖理解的复杂性。

---

**If you find this useful, please star the repository and share it with others learning about AI agents.**

**如果你觉得本仓库有用，请点个 Star 并分享给其他正在学习 AI 智能体的人。**
