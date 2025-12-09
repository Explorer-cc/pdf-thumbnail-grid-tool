#!/usr/bin/env python3
"""GUI 启动脚本"""

import sys
from pathlib import Path

# 添加 src 目录到 Python 路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from gui import main

if __name__ == "__main__":
    main()