import argparse
import io
import math
import sys
from pathlib import Path
from typing import Tuple, Optional

import fitz
import numpy as np
from PIL import Image

# 设置控制台编码为UTF-8
if sys.platform == 'win32':
    import locale
    try:
        locale.setlocale(locale.LC_ALL, 'zh_CN.UTF-8')
    except:
        try:
            locale.setlocale(locale.LC_ALL, 'Chinese_China.65001')
        except:
            pass


def calculate_grid_size(total_pages: int, n: int, m: Optional[int] = None) -> Tuple[int, int]:
    """计算网格大小"""
    if m is None:
        m = math.ceil(total_pages / n)
    return n, m


def process_pdf(
    input_path: Path,
    output_path: Path,
    n: int,
    m: Optional[int] = None,
    page_size: Optional[Tuple[float, float]] = None,  # None表示自动计算
    orientation: str = "landscape",  # 默认横向以更好地展示多页面
    dpi: int = 150,
    gap: float = 3,  # 缩略图之间的间距 (points)，改小以节省空间
    padding: float = 10,  # 页面边缘的留白
) -> None:
    """
    处理PDF文件，生成N×M网格拼接的缩略图PDF

    Args:
        input_path: 输入PDF文件路径
        output_path: 输出PDF文件路径
        n: 网格列数
        m: 网格行数（可选，如果不提供则自动计算）
        page_size: 输出PDF页面大小 (width, height) in points，None表示自动计算
        orientation: 页面方向 "portrait" 或 "landscape"
        dpi: 缩略图DPI
        gap: 缩略图之间的间距 (points)
        padding: 页面边缘的留白 (points)
    """
    # 打开输入PDF
    doc = fitz.open(input_path)
    total_pages = len(doc)

    # 计算网格大小
    n, m = calculate_grid_size(total_pages, n, m)

    # 计算总页数（需要多少个输出页面）
    thumbnails_per_page = n * m
    output_pages = math.ceil(total_pages / thumbnails_per_page)

    # 如果没有指定页面大小，根据内容和布局自动计算最适合的页面大小
    if page_size is None:
        # 获取第一页的宽高比作为参考
        first_page = doc[0]
        src_rect = first_page.rect
        aspect_ratio = src_rect.width / src_rect.height

        # 设定一个合适的缩略图高度（根据DPI）
        # 使用更大的尺寸以便更好查看，但避免过大造成浪费
        base_thumb_height = 300  # 基础缩略图高度
        base_thumb_width = base_thumb_height * aspect_ratio

        # 计算页面大小 - 使用紧凑布局以减少空白
        # 减小间距和边距以更好地利用空间
        effective_gap = gap * 0.5  # 使用更小的间距
        effective_padding = padding * 0.8  # 使用更小的边距

        page_width = n * base_thumb_width + (n - 1) * effective_gap + 2 * effective_padding
        page_height = m * base_thumb_height + (m - 1) * effective_gap + 2 * effective_padding

        page_size = (page_width, page_height)
        print(f"Auto-calculated page size: {page_width:.2f} x {page_height:.2f} points")
        print(f"In inches: {page_width/72:.2f} x {page_height/72:.2f} inches")
    else:
        print(f"Using specified page size: {page_size}")
        # 调整页面方向
        if orientation == "landscape":
            page_size = (page_size[1], page_size[0])

    # 计算每个缩略图的可用空间
    # 如果是自动计算页面大小，使用实际的有效间距
    if page_size is None:
        effective_gap = gap * 0.5
        effective_padding = padding * 0.8
    else:
        effective_gap = gap
        effective_padding = padding

    available_width = page_size[0] - 2 * effective_padding - (n - 1) * effective_gap
    available_height = page_size[1] - 2 * effective_padding - (m - 1) * effective_gap
    thumbnail_width = available_width / n
    thumbnail_height = available_height / m

    # 创建输出PDF
    output_doc = fitz.open()

    for page_idx in range(output_pages):
        # 创建新页面
        page = output_doc.new_page(width=page_size[0], height=page_size[1])

        # 计算当前页面的缩略图范围
        start_idx = page_idx * thumbnails_per_page
        end_idx = min(start_idx + thumbnails_per_page, total_pages)

        for idx in range(start_idx, end_idx):
            # 计算在网格中的位置
            grid_idx = idx - start_idx
            row = grid_idx // n
            col = grid_idx % n

            # 计算缩略图在页面上的位置
            x = effective_padding + col * (thumbnail_width + effective_gap)
            y = effective_padding + row * (thumbnail_height + effective_gap)

            # 获取原页面
            src_page = doc[idx]

            # 获取原页面的宽高比
            src_rect = src_page.rect
            aspect_ratio = src_rect.width / src_rect.height

            # 计算缩略图矩形，保持宽高比
            if aspect_ratio > thumbnail_width / thumbnail_height:
                # 宽度受限
                thumb_width_final = thumbnail_width
                thumb_height_final = thumbnail_width / aspect_ratio
                # 居中对齐
                y_offset = (thumbnail_height - thumb_height_final) / 2
                img_rect = fitz.Rect(x, y + y_offset, x + thumb_width_final, y + y_offset + thumb_height_final)
            else:
                # 高度受限
                thumb_height_final = thumbnail_height
                thumb_width_final = thumbnail_height * aspect_ratio
                # 居中对齐
                x_offset = (thumbnail_width - thumb_width_final) / 2
                img_rect = fitz.Rect(x + x_offset, y, x + x_offset + thumb_width_final, y + thumb_height_final)

            # 将页面直接绘制到新位置（更高效且保持质量）
            page.show_pdf_page(img_rect, doc, idx)

            # 绘制黑色边框
            page.draw_rect(img_rect, color=fitz.utils.getColor("black"), width=0.5)

    # 保存输出PDF
    output_doc.save(output_path, garbage=4, deflate=True)
    output_doc.close()
    doc.close()


def main():
    parser = argparse.ArgumentParser(description="PDF缩略图拼接工具 - 优化空间利用版本")
    parser.add_argument("input", type=Path, help="输入PDF文件路径")
    parser.add_argument("output", type=Path, help="输出PDF文件路径")
    parser.add_argument("-n", "--columns", type=int, required=True, help="网格列数")
    parser.add_argument("-m", "--rows", type=int, help="网格行数（可选，自动计算）")
    parser.add_argument("--page-size", type=str, default="auto",
                       choices=["auto", "A4", "A3", "A5", "Letter"],
                       help="输出页面大小，'auto'表示根据内容自动计算")
    parser.add_argument("--orientation", type=str, default="landscape",
                       choices=["portrait", "landscape"],
                       help="页面方向（默认landscape）")
    parser.add_argument("--dpi", type=int, default=150, help="缩略图DPI")
    parser.add_argument("--gap", type=float, default=3, help="缩略图之间的间距（点）")
    parser.add_argument("--padding", type=float, default=10, help="页面边缘留白（点）")

    args = parser.parse_args()

    # 页面大小映射
    page_sizes = {
        "auto": None,
        "A4": (595.276, 841.890),
        "A3": (841.890, 1190.551),
        "A5": (419.528, 595.276),
        "Letter": (612, 792)
    }

    process_pdf(
        input_path=args.input,
        output_path=args.output,
        n=args.columns,
        m=args.rows,
        page_size=page_sizes[args.page_size],
        orientation=args.orientation,
        dpi=args.dpi,
        gap=args.gap,
        padding=args.padding
    )

    print(f"Successfully generated thumbnail PDF: {args.output}")


if __name__ == "__main__":
    import io
    main()