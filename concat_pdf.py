#!/usr/bin/env python3
"""PDF缩略图拼接工具的便捷入口脚本"""

import sys
from pathlib import Path

# 添加src目录到Python路径
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

from concat_pdf import main

if __name__ == "__main__":
    main()