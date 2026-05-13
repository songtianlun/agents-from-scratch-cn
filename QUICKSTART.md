# Quick Start Guide

# 快速入门指南

Get up and running with AI Agents from Scratch in 10 minutes.

10 分钟内启动并运行《从零开始构建 AI 智能体》。

## Prerequisites

## 前置条件

- Python 3.10 or higher
- 8GB+ RAM (for running local models)
- ~5-10GB free disk space (for model files)

- Python 3.10 或更高版本
- 8GB+ 内存（用于运行本地模型）
- 约 5-10GB 可用磁盘空间（用于模型文件）

## Step 1: Install Dependencies

## 第一步：安装依赖

```bash
pip install llama-cpp-python
```

**Optional but recommended:**
```bash
# Create a virtual environment first
# 建议先创建虚拟环境
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install llama-cpp-python
```

**可选但推荐：**
```bash
# Create a virtual environment first
# 建议先创建虚拟环境
python -m venv venv
source venv/bin/activate  # Windows 系统：venv\Scripts\activate
pip install llama-cpp-python
```

## Step 2: Download a Model

## 第二步：下载模型

You need a GGUF model file. Here's the easiest way:

你需要一个 GGUF 格式的模型文件。最简单的方式如下：

1. Go to https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF
2. Download `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf` (~5GB)
3. Place it in the `models/` directory
4. Rename it to `llama-3-8b-instruct.gguf` (optional, for simplicity)

1. 访问 https://huggingface.co/bartowski/Meta-Llama-3-8B-Instruct-GGUF
2. 下载 `Meta-Llama-3-8B-Instruct-Q4_K_M.gguf`（约 5GB）
3. 将其放入 `models/` 目录
4. 将其重命名为 `llama-3-8b-instruct.gguf`（可选，为了简洁）

**Alternative models:**
- Mistral 7B: https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.2-GGUF
- Gemma 7B: https://huggingface.co/bartowski/gemma-7b-it-GGUF

**备选模型：**
- Mistral 7B：https://huggingface.co/bartowski/Mistral-7B-Instruct-v0.2-GGUF
- Gemma 7B：https://huggingface.co/bartowski/gemma-7b-it-GGUF

## Step 3: Verify Setup

## 第三步：验证安装

```bash
python setup_check.py
```

This checks:
- Python version
- Dependencies
- Models directory
- Repository structure

此脚本将检查：
- Python 版本
- 依赖项
- 模型目录
- 仓库结构

## Step 4: Run Examples

## 第四步：运行示例

```bash
python complete_example.py
```

This will run examples from all 10 lessons. You can also open `complete_example.py` and modify the model path or comment out lessons you want to skip.

这将运行全部 10 节课的示例。你也可以打开 `complete_example.py`，修改模型路径，或注释掉你想跳过的课节。

## Step 6: Start Learning

## 第六步：开始学习

Now read the lessons in order:

现在按顺序阅读各节课：

1. `lessons/01_basic_llm_chat.md` - Understanding the basics
2. `lessons/02_system_prompt.md` - Adding behavior
3. `lessons/03_structured_output.md` - Making it reliable
4. ... and so on through lesson 10

1. `lessons/01_basic_llm_chat.md` - 理解基础知识
2. `lessons/02_system_prompt.md` - 添加行为
3. `lessons/03_structured_output.md` - 提高可靠性
4. ...以此类推，直到第 10 课

Each lesson builds on the previous one.

每节课都在前一节的基础上构建。

## Troubleshooting

## 故障排除

### "Module 'llama_cpp' not found"

### "找不到模块 'llama_cpp'"

```bash
pip install llama-cpp-python
```

### "Model file not found"

### "找不到模型文件"

Check that:
1. The model file is in `models/` directory
2. The path in `complete_example.py` matches the actual filename
3. The file has a `.gguf` extension

请检查：
1. 模型文件是否在 `models/` 目录中
2. `complete_example.py` 中的路径是否与实际文件名匹配
3. 文件是否具有 `.gguf` 扩展名

### "Out of memory" error

### "内存不足"错误

Try a smaller model or smaller quantization:
- Q4_K_M: ~5GB RAM
- Q5_K_M: ~6GB RAM  
- Q8_0: ~8GB RAM

尝试使用更小的模型或更低的量化精度：
- Q4_K_M：约 5GB 内存
- Q5_K_M：约 6GB 内存
- Q8_0：约 8GB 内存

### Slow responses

### 响应缓慢

This is normal for CPU inference. Each response takes 10-30 seconds depending on:
- Your CPU speed
- Model size
- Response length

这是 CPU 推理的正常现象。每次响应需要 10-30 秒，具体取决于：
- 你的 CPU 速度
- 模型大小
- 响应长度

## Next Steps

## 后续步骤

- **Read philosophy.md** to understand the approach
- **Work through lessons** one at a time
- **Modify the agent** to experiment
- **Check examples/** for complete code examples

- **阅读 philosophy.md** 以理解本仓库的方法论
- **逐节学习课程**
- **修改智能体**进行实验
- **查看 examples/** 获取完整代码示例

## Getting Help

## 获取帮助

- Check existing [GitHub Issues](https://github.com/your-repo/issues)
- Read the lesson markdown files carefully
- Ask questions in [GitHub Discussions](https://github.com/your-repo/discussions)

- 查看现有的 [GitHub Issues](https://github.com/your-repo/issues)
- 仔细阅读课程 Markdown 文件
- 在 [GitHub Discussions](https://github.com/your-repo/discussions) 中提问

## Tips for Success

## 成功学习的建议

1. **Don't skip lessons** - they build on each other
2. **Run the code** - reading isn't enough
3. **Experiment** - modify examples and see what happens
4. **Be patient** - local inference is slow but worth it
5. **Read comments** - the code explains the "why"

1. **不要跳过课节** - 它们相互依赖
2. **运行代码** - 仅仅阅读是不够的
3. **动手实验** - 修改示例，观察结果
4. **保持耐心** - 本地推理速度较慢，但值得等待
5. **阅读注释** - 代码解释了"为什么"

Happy learning! 🚀

祝学习愉快！🚀