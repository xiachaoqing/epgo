#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
英语陪跑GO - Favicon 生成器
将PNG图片转换为favicon.ico，自动去除黑色背景

用法：
  python3 create_favicon.py <input.png> [output.ico]
  python3 create_favicon.py /path/to/logo.png        # 输出为favicon.ico
  python3 create_favicon.py /path/to/logo.png my-icon.ico
"""

import sys
from PIL import Image
from io import BytesIO

def remove_black_background(image_path, black_threshold=30):
    """
    从图片中去除黑色背景，转为透明

    Args:
        image_path: 输入图片路径
        black_threshold: 黑色阈值（RGB值小于此值认为是黑色）

    Returns:
        PIL Image 对象
    """
    try:
        # 打开图片
        img = Image.open(image_path)
        print('✓ 图片已加载: {}x{}'.format(img.width, img.height))

        # 转换为RGBA（支持透明）
        if img.mode != 'RGBA':
            img = img.convert('RGBA')

        # 获取像素数据
        data = img.getdata()

        # 处理每个像素
        new_data = []
        black_count = 0

        for item in data:
            # 支持RGB和RGBA
            if len(item) == 4:
                r, g, b, a = item
            else:
                r, g, b = item[:3]
                a = 255

            # 检查是否为黑色或深色
            if r < black_threshold and g < black_threshold and b < black_threshold:
                # 转为透明
                new_data.append((r, g, b, 0))
                black_count += 1
            else:
                # 保持原样
                new_data.append((r, g, b, a))

        img.putdata(new_data)
        print('✓ 已移除 {} 个黑色像素，转为透明'.format(black_count))

        return img

    except Exception as e:
        print('✗ 处理失败: {}'.format(e))
        return None


def create_favicon(image, output_path='favicon.ico'):
    """
    创建favicon.ico

    Args:
        image: PIL Image 对象
        output_path: 输出路径
    """
    try:
        # favicon 通常是 16x16, 32x32, 64x64 的组合
        # 为了最佳兼容性，创建多个尺寸

        sizes = [(16, 16), (32, 32), (64, 64)]
        icons = []

        for size in sizes:
            # 调整大小
            resized = image.resize(size, Image.Resampling.LANCZOS)
            icons.append(resized)

        # 保存为ICO（多尺寸）
        icons[0].save(output_path, sizes=[(16, 16), (32, 32), (64, 64)])

        print('✓ 已创建favicon: {}'.format(output_path))
        print('  - 包含尺寸: 16x16, 32x32, 64x64')
        return True

    except Exception as e:
        print('✗ 创建失败: {}'.format(e))
        return False


def main():
    if len(sys.argv) < 2:
        print('用法: python3 create_favicon.py <input.png> [output.ico]')
        print('示例: python3 create_favicon.py logo.png')
        print('      python3 create_favicon.py logo.png my-favicon.ico')
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2] if len(sys.argv) > 2 else 'favicon.ico'

    print('='*60)
    print('Favicon 生成器')
    print('='*60)
    print('输入: {}'.format(input_path))
    print('输出: {}'.format(output_path))
    print('-'*60)

    # 移除黑色背景
    img = remove_black_background(input_path)
    if not img:
        sys.exit(1)

    # 创建favicon
    if create_favicon(img, output_path):
        print('-'*60)
        print('✓ Favicon 创建成功！')
        print('现在可以上传到服务器根目录')
        print('='*60)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
