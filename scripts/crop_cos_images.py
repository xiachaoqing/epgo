#!/usr/bin/env python3
"""
COS图片裁剪工具 - 英语陪跑GO宣传素材处理
功能: 从COS下载指定图片，裁掉底部机构名称/二维码区域，保存为新文件
用法: python3 crop_cos_images.py
依赖: pip install Pillow requests
"""

import os
import io
import urllib.request
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("请先安装Pillow: pip install Pillow")
    exit(1)

# ── COS 配置 ──────────────────────────────────────────────
COS_BASE = "https://art-nine-1252921383.cos.ap-beijing.myqcloud.com/yingyupeipao"

# 需要裁剪的图片配置
# crop_ratio: 保留顶部的比例 (0.0~1.0)，例如0.82表示裁掉底部18%
IMAGES = [
    {
        "filename": "ai对话.png",
        "encoded":  "ai%E5%AF%B9%E8%AF%9D.png",
        "crop_ratio": 0.80,   # 保留顶部80%，裁掉底部20%（去掉机构名称）
        "save_as": "ai对话_crop.png",
    },
    {
        "filename": "C端APP宣传海报.png",
        "encoded":  "C%E7%AB%AFAPP%E5%AE%A3%E4%BC%A0%E6%B5%B7%E6%8A%A5.png",
        "crop_ratio": 0.85,   # 保留顶部85%，裁掉底部15%（去掉二维码和机构区域）
        "save_as": "C端APP宣传海报_crop.png",
    },
    {
        "filename": "下载方式.png",
        "encoded":  "%E4%B8%8B%E8%BD%BD%E6%96%B9%E5%BC%8F.png",
        "crop_ratio": 0.82,   # 保留顶部82%，裁掉底部18%
        "save_as": "下载方式_crop.png",
    },
]

OUTPUT_DIR = Path(__file__).parent.parent / "jiazhangtong" / "cropped"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def download_image(url: str) -> Image.Image:
    """从URL下载图片"""
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"}
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=30) as resp:
        data = resp.read()
    return Image.open(io.BytesIO(data))


def crop_bottom(img: Image.Image, keep_ratio: float) -> Image.Image:
    """裁掉底部，保留顶部 keep_ratio 比例"""
    w, h = img.size
    new_h = int(h * keep_ratio)
    return img.crop((0, 0, w, new_h))


def main():
    print(f"输出目录: {OUTPUT_DIR}\n")

    for cfg in IMAGES:
        url = f"{COS_BASE}/{cfg['encoded']}"
        out_path = OUTPUT_DIR / cfg["save_as"]

        print(f"处理: {cfg['filename']}")
        print(f"  URL: {url}")

        try:
            img = download_image(url)
            w, h = img.size
            print(f"  原始尺寸: {w} x {h}")

            cropped = crop_bottom(img, cfg["crop_ratio"])
            cw, ch = cropped.size
            print(f"  裁剪后: {cw} x {ch}  (保留 {cfg['crop_ratio']*100:.0f}%)")

            # 保存为PNG（带透明通道时保持，否则转RGB节省空间）
            if img.mode in ("RGBA", "LA"):
                cropped.save(out_path, "PNG", optimize=True)
            else:
                cropped = cropped.convert("RGB")
                cropped.save(out_path, "PNG", optimize=True)

            print(f"  已保存: {out_path}")

        except Exception as e:
            print(f"  [ERROR] {e}")

        print()

    print("=" * 50)
    print("完成！请将以下文件上传到COS的 yingyupeipao/ 目录：")
    for cfg in IMAGES:
        print(f"  {OUTPUT_DIR / cfg['save_as']}")
    print()
    print("上传后对应的COS URL（页面已自动引用）：")
    for cfg in IMAGES:
        name_encoded = urllib.request.pathname2url(cfg["save_as"])
        print(f"  {COS_BASE}/{name_encoded}")


if __name__ == "__main__":
    main()
