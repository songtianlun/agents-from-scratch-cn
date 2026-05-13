#!/usr/bin/env python3
"""
Setup verification script

设置验证脚本

Run this after installing dependencies to verify your setup is correct.

安装依赖项后运行此脚本以验证你的设置是否正确。
"""

import sys
import os


def check_python_version():
    """Check Python version is 3.10+
    
    检查 Python 版本是否为 3.10+
    """
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_dependencies():
    """Check if required packages are installed
    
    检查是否安装了所需的包
    """
    try:
        import llama_cpp
        print("✅ llama-cpp-python installed")
        return True
    except ImportError:
        print("❌ llama-cpp-python not found")
        print("   Install with: pip install llama-cpp-python")
        return False


def check_model_directory():
    """Check if models directory exists
    
    检查 models 目录是否存在
    """
    if os.path.isdir("models"):
        print("✅ models/ directory exists")
        
        # Check for GGUF files
        # 检查 GGUF 文件
        files = [f for f in os.listdir("models") if f.endswith(".gguf")]
        if files:
            print(f"✅ Found {len(files)} GGUF model(s):")
            for f in files:
                size_mb = os.path.getsize(f"models/{f}") / (1024**2)
                print(f"   - {f} ({size_mb:.1f} MB)")
        else:
            print("⚠️  No GGUF models found in models/")
            print("   Download a model and place it in models/")
        return True
    else:
        print("❌ models/ directory not found")
        return False


def check_structure():
    """Check repository structure
    
    检查仓库结构
    """
    required_dirs = ["shared", "agent", "lessons"]
    all_exist = True
    
    for dir_name in required_dirs:
        if os.path.isdir(dir_name):
            print(f"✅ {dir_name}/ directory exists")
        else:
            print(f"❌ {dir_name}/ directory not found")
            all_exist = False
    
    return all_exist


def main():
    """Run all checks
    
    运行所有检查
    """
    print("="*50)
    print("AI Agents from Scratch - Setup Verification")
    print("="*50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Models Directory", check_model_directory),
        ("Repository Structure", check_structure),
    ]
    
    results = []
    
    for name, check_func in checks:
        print(f"\n{name}:")
        results.append(check_func())
    
    print("\n" + "="*50)
    if all(results):
        print("✅ All checks passed! You're ready to start learning.")
        print("\nNext steps:")
        print("1. Read lessons/01_basic_llm_chat.md")
        print("2. Run: python complete_example.py")
    else:
        print("⚠️  Some checks failed. Please fix the issues above.")
    print("="*50)


if __name__ == "__main__":
    main()