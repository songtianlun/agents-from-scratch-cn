"""
LocalLLM - A simple wrapper around llama-cpp-python.

LocalLLM - 对 llama-cpp-python 的简单封装。

This class provides a minimal interface to interact with local language models.
It intentionally has no magic:
- No retries (added in lesson 03)
- No tool calling (added in lesson 05)
- No memory (added in lesson 07)

此类提供与本地语言模型交互的最小接口。
它有意不包含任何魔法：
- 无重试（在第 03 课中添加）
- 无工具调用（在第 05 课中添加）
- 无记忆（在第 07 课中添加）

Just text in, text out.

只是文本输入，文本输出。
"""

from shared.llama_logging import disable_llama_logging
from llama_cpp import Llama

disable_llama_logging()

class LocalLLM:
    """
    A minimal wrapper for local LLM inference using llama.cpp.
    
    一个用于使用 llama.cpp 进行本地 LLM 推理的最小封装器。
    
    This class is intentionally simple and grows throughout the lessons.
    
    此类有意保持简单，并在各课程中不断成长。
    """
    
    def __init__(
        self,
        model_path: str,
        temperature: float = 0.2,
        max_tokens: int = 512,
        n_ctx: int = 2048
    ):
        """
        Initialize the local LLM.
        
        初始化本地 LLM。
        
        Args:
            model_path: Path to the GGUF model file
                        GGUF 模型文件的路径
            temperature: Sampling temperature (0.0 = deterministic, 1.0 = creative)
                         采样温度（0.0 = 确定性，1.0 = 创造性）
            max_tokens: Maximum tokens to generate per response
                        每次响应生成的最大词元数
            n_ctx: Context window size
                   上下文窗口大小
        """
        self.llm = Llama(
            model_path=model_path,
            temperature=temperature,
            n_ctx=n_ctx,
            verbose=False,
        )
        self.max_tokens = max_tokens
    
    def generate(self, prompt: str, temperature: float = None, stop: list[str] = None) -> str:
        """
        Generate text from a prompt.
        
        从提示词生成文本。
        
        Args:
            prompt: The input text prompt
                    输入文本提示词
            temperature: Optional temperature override
                         可选的温度覆盖值
            stop: Optional list of stop sequences
                  可选的停止序列列表
                
        Returns:
            Generated text as a string
            
            返回：
            作为字符串的生成文本
        """
        kwargs = {
            "prompt": prompt,
            "max_tokens": self.max_tokens,
            "stop": stop if stop is not None else ["</s>", "\n\n", "User:", "Assistant:"],
        }
        
        if temperature is not None:
            kwargs["temperature"] = temperature
        
        response = self.llm(**kwargs)
        return response["choices"][0]["text"].strip()