# PDF Thumbnail Grid Tool

A lightweight Python tool that transforms PDF pages into organized thumbnail grids. Perfect for creating document previews, proofreading layouts, or compact document summaries.

## Features

- 🚀 **Smart Layout**: Automatically calculates optimal page size to minimize whitespace
- 🎛️ **Flexible Configuration**: Customizable grid dimensions (rows × columns)
- 🎨 **Quality Control**: Adjustable DPI for clear or compact thumbnails
- 🖥️ **User-Friendly GUI**: Intuitive interface with drag-and-drop support
- ⚡ **Quick Presets**: Pre-configured layouts for common use cases
- 📦 **Standalone Executable**: Windows .exe file requires no installation

## Quick Start

### For Windows Users (Recommended)

Download and run the standalone executable:

1. Navigate to `dist/PDF Thumbnail Grid Tool.exe` after building
2. Double-click to launch the GUI
3. Select your PDF file and configure your grid layout
4. Click "Start Processing" to generate thumbnails

### For Developers

#### Prerequisites
- Python 3.12 or higher
- [uv](https://docs.astral.sh/uv/) package manager

#### Installation

```bash
# Clone the repository
git clone <repository-url>
cd concat_pdf

# Install dependencies
uv sync

# Optional: Install GUI dependencies for packaging
uv sync --extra gui
```

#### Running the Application

```bash
# GUI version
uv run src/gui.py

# Command-line version
uv run python -m concat_pdf input.pdf output.pdf -n 3
```

## Building the Executable

### Windows Executable

```bash
# Install packaging dependencies
uv sync --extra gui

# Build the .exe file
uv run pyinstaller --name "PDF Thumbnail Grid Tool" --onefile --windowed --add-data "src;src" src/gui.py

# The executable will be in the dist/ directory
```

### Portable Version

For a complete portable package with documentation:

```bash
# Run the build script (Windows only)
python build.py

# This creates:
# - dist/PDF Thumbnail Grid Tool.exe
# - PDF Thumbnail Grid Tool_Portable/ (with README and launcher)
```

## Usage Guide

### GUI Interface

1. **File Selection**
   - Use "Browse..." buttons or drag-and-drop PDF files
   - Output filename is auto-generated from input

2. **Grid Configuration**
   - **Columns**: Number of thumbnails per row (1-10)
   - **Rows**: Number of thumbnails per column (1-10)
   - **Auto Calculate Rows**: Automatically determine rows based on page count

3. **Quality Settings**
   - **DPI**: Resolution (50-600, recommended 150-300)
   - **Spacing**: Gap between thumbnails (0-20 points)
   - **Margin**: Page edge whitespace (0-50 points)

4. **Quick Presets**
   - A4 Landscape 3×2: Standard layout for A4 pages
   - A4 Landscape 4×3: Denser layout for more content
   - A3 Landscape 5×3: Large format for high detail
   - Auto Layout: Intelligent layout based on content

### Command Line Interface

```bash
# Basic usage
uv run python -m concat_pdf input.pdf output.pdf -n 3

# Advanced options
uv run python -m concat_pdf input.pdf output.pdf \
    -n 4 \          # 4 columns
    -m 3 \          # 3 rows
    --dpi 200 \     # High quality
    --gap 2 \       # Small gaps
    --padding 5     # Minimal margins
```

## File Structure

```
concat_pdf/
├── src/
│   ├── gui.py              # GUI application
│   └── concat_pdf/
│       └── __init__.py     # Core processing logic
├── concat_pdf.py           # CLI entry point
├── build.py                # Build script for Windows
├── pyproject.toml          # Project configuration
├── README.md               # This file
├── .gitignore             # Git ignore rules
└── dist/                  # Build output directory
    └── PDF Thumbnail Grid Tool.exe
```

## Dependencies

- **PyMuPDF**: PDF processing and rendering
- **Pillow**: Image manipulation
- **NumPy**: Numerical operations
- **tkinter**: GUI framework (included with Python)

## Troubleshooting

### Common Issues

1. **"Cannot read PDF file"**
   - Ensure the PDF is not password-protected
   - Check if the file is corrupted

2. **Executable won't run**
   - Windows Defender may flag it - click "More info" → "Run anyway"
   - Ensure you're running on Windows 7/8/10/11 (64-bit)

3. **Large output file size**
   - Reduce DPI setting
   - Increase spacing between thumbnails

## License

This project is open source. See LICENSE file for details.

---

# PDF缩略图网格工具

一个轻量级的Python工具，可以将PDF页面转换为有组织的缩略图网格。非常适合用于创建文档预览、校对布局或生成紧凑的文档摘要。

## 主要功能

- 🚀 **智能布局**：自动计算最佳页面大小，最小化空白区域
- 🎛️ **灵活配置**：可自定义网格维度（行×列）
- 🎨 **质量控制**：可调节DPI以获得清晰或紧凑的缩略图
- 🖥️ **用户友好界面**：直观的图形界面，支持拖放操作
- ⚡ **快速预设**：预配置常用布局
- 📦 **独立可执行文件**：Windows .exe文件无需安装

## 快速开始

### Windows用户（推荐）

直接下载并运行独立可执行文件：

1. 构建后进入 `dist/PDF Thumbnail Grid Tool.exe` 目录
2. 双击启动GUI界面
3. 选择PDF文件并配置网格布局
4. 点击"开始处理"生成缩略图

### 开发者

#### 系统要求
- Python 3.12 或更高版本
- [uv](https://docs.astral.sh/uv/) 包管理器

#### 安装

```bash
# 克隆仓库
git clone <repository-url>
cd concat_pdf

# 安装依赖
uv sync

# 可选：安装GUI打包依赖
uv sync --extra gui
```

#### 运行程序

```bash
# GUI版本
uv run src/gui.py

# 命令行版本
uv run python -m concat_pdf input.pdf output.pdf -n 3
```

## 构建可执行文件

### Windows可执行文件

```bash
# 安装打包依赖
uv sync --extra gui

# 构建.exe文件
uv run pyinstaller --name "PDF Thumbnail Grid Tool" --onefile --windowed --add-data "src;src" src/gui.py

# 可执行文件将位于 dist/ 目录中
```

### 便携版

创建包含说明文档的完整便携包：

```bash
# 运行构建脚本（仅Windows）
python build.py

# 这将创建：
# - dist/PDF Thumbnail Grid Tool.exe
# - PDF Thumbnail Grid Tool_Portable/（包含说明文档和启动器）
```

## 使用指南

### 图形界面

1. **文件选择**
   - 使用"浏览..."按钮或直接拖放PDF文件
   - 输出文件名会根据输入自动生成

2. **网格配置**
   - **列数**：每行的缩略图数量（1-10）
   - **行数**：每列的缩略图数量（1-10）
   - **自动计算行数**：根据页数自动确定所需的行数

3. **质量设置**
   - **DPI**：分辨率（50-600，推荐150-300）
   - **间距**：缩略图之间的间隙（0-20点）
   - **边距**：页面边缘的留白（0-50点）

4. **快速预设**
   - A4横向 3×2：A4页面的标准布局
   - A4横向 4×3：更密集的布局
   - A3横向 5×3：大格式高细节布局
   - 自动布局：基于内容的智能布局

### 命令行界面

```bash
# 基本用法
uv run python -m concat_pdf input.pdf output.pdf -n 3

# 高级选项
uv run python -m concat_pdf input.pdf output.pdf \
    -n 4 \          # 4列
    -m 3 \          # 3行
    --dpi 200 \     # 高质量
    --gap 2 \       # 小间距
    --padding 5     # 最小边距
```

## 文件结构

```
concat_pdf/
├── src/
│   ├── gui.py              # GUI应用程序
│   └── concat_pdf/
│       └── __init__.py     # 核心处理逻辑
├── concat_pdf.py           # 命令行入口
├── build.py                # Windows构建脚本
├── pyproject.toml          # 项目配置
├── README.md               # 本文件
├── .gitignore             # Git忽略规则
└── dist/                  # 构建输出目录
    └── PDF Thumbnail Grid Tool.exe
```

## 依赖项

- **PyMuPDF**：PDF处理和渲染
- **Pillow**：图像处理
- **NumPy**：数值计算
- **tkinter**：GUI框架（Python自带）

## 故障排除

### 常见问题

1. **"无法读取PDF文件"**
   - 确保PDF没有密码保护
   - 检查文件是否损坏

2. **可执行文件无法运行**
   - Windows Defender可能拦截，点击"更多信息"→"仍要运行"
   - 确保在Windows 7/8/10/11（64位）系统上运行

3. **输出文件过大**
   - 降低DPI设置
   - 增加缩略图间距

## 许可证

本项目是开源的。详情请参阅LICENSE文件。