#!/usr/bin/env python3
"""
🚀 Playform AI - 超快启动脚本 (3秒吸睛!)
最快方式启动系统
"""

import subprocess
import sys
import os

def main():
    print("\n" + "="*60)
    print("🎯 Playform AI - 3秒启动")
    print("="*60)
    
    # 检查环境
    print("\n✅ 检查环境...")
    
    # 安装必要包
    packages = ["langchain", "langchain-openai", "rich", "python-dotenv"]
    
    try:
        for pkg in packages:
            __import__(pkg.replace("-", "_"))
    except ImportError:
        print("\n📦 安装必需包...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-q"] + packages)
    
    print("✅ 环境就绪！\n")
    
    # 显示3秒吸睛仪表板
    print("🎨 加载 3 秒吸睛仪表板...\n")
    subprocess.run([sys.executable, "dashboard.py"])


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n👋 已中断")
        sys.exit(0)
