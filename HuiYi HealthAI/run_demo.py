#!/usr/bin/env python3
"""
慧医小助 - MiniMind医疗问答系统
主启动脚本 - 调用scripts目录下的实际启动程序
"""

import os
import sys
import subprocess

def main():
    """主函数 - 切换到正确目录并调用启动脚本"""
    # 确保在正确的目录
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # 调用scripts目录下的启动脚本
    try:
        subprocess.run([sys.executable, "scripts/run_demo.py"], check=True)
    except subprocess.CalledProcessError as e:
        print(f"启动失败: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n👋 程序已退出")

if __name__ == "__main__":
    main() 