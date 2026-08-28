"""
生成微信分享卡片图 600×600
蓝色渐变背景 + 功能介绍截图 + logo + 文字
"""
from PIL import Image, ImageDraw, ImageFont
import os
from pathlib import Path

OUT = Path('/Users/xiachaoqing/projects/epgo/jiazhangtong/share.jpg')
W = H = 600

# ── 背景渐变（蓝色）─────────────────────────────────────
img = Image.new('RGB', (W, H))
draw = ImageDraw.Draw(img)
for y in range(H):
    r = int(18  + (10  - 18)  * y / H)
    g = int(90  + (55  - 90)  * y / H)
    b = int(210 + (155 - 210) * y / H)
    draw.line([(0, y), (W, y)], fill=(r, g, b))

# ── 装饰圆 ───────────────────────────────────────────────
for cx, cy, cr, a in [(520,60,130,15),(80,520,100,12),(300,300,220,6)]:
    ov = Image.new('RGBA',(W,H),(0,0,0,0))
    od = ImageDraw.Draw(ov)
    od.ellipse([cx-cr,cy-cr,cx+cr,cy+cr], fill=(255,255,255,a))
    img = Image.alpha_composite(img.convert('RGBA'), ov).convert('RGB')
draw = ImageDraw.Draw(img)

# ── 嵌入功能介绍截图（右侧，带圆角白色卡片）────────────────
feat_path = '/Users/xiachaoqing/projects/doc/英语陪跑go/功能介绍.png'
if os.path.exists(feat_path):
    feat = Image.open(feat_path).convert('RGBA')
    # 缩放到合适大小，右侧展示
    feat_w, feat_h = feat.size
    target_h = 320
    target_w = int(feat_w * target_h / feat_h)
    feat = feat.resize((target_w, target_h), Image.LANCZOS)
    # 白色圆角卡片背景
    card_pad = 8
    card = Image.new('RGBA', (target_w + card_pad*2, target_h + card_pad*2), (255,255,255,230))
    card_x = W - target_w - card_pad*2 - 20
    card_y = (H - target_h - card_pad*2) // 2 + 30
    img.paste(Image.new('RGB', card.size, (255,255,255)),
              (card_x, card_y),
              Image.new('L', card.size, 200))
    img.paste(feat, (card_x + card_pad, card_y + card_pad), feat)
    draw = ImageDraw.Draw(img)

# ── 字体 ─────────────────────────────────────────────────
font_candidates = [
    '/System/Library/Fonts/STHeiti Medium.ttc',
    '/System/Library/Fonts/PingFang.ttc',
    '/Library/Fonts/Arial Unicode MS.ttf',
]
def load_font(size):
    for p in font_candidates:
        if os.path.exists(p):
            try: return ImageFont.truetype(p, size)
            except: pass
    return ImageFont.load_default()

# ── Logo（左上角）─────────────────────────────────────────
logo_path = '/Users/xiachaoqing/projects/doc/英语陪跑go/logo.png'
if os.path.exists(logo_path):
    logo = Image.open(logo_path).convert('RGBA')
    logo = logo.resize((72, 72), Image.LANCZOS)
    img.paste(logo, (28, 28), logo)
    draw = ImageDraw.Draw(img)

# ── 品牌名 ───────────────────────────────────────────────
draw.text((112, 35), '英语陪跑GO', font=load_font(36), fill=(255,255,255))
draw.text((114, 76), 'AI英语智能学习', font=load_font(20), fill=(180,225,255))

# ── 分隔线 ───────────────────────────────────────────────
draw.rectangle([28, 118, 260, 121], fill=(255,255,255,80))

# ── 主口号 ───────────────────────────────────────────────
draw.text((28, 136), '为孩子打造', font=load_font(44), fill=(255,255,255))
draw.text((28, 190), '有温度的英语', font=load_font(44), fill=(255, 230, 100))
draw.text((28, 244), '智能学习乐园', font=load_font(44), fill=(255,255,255))

# ── 特点标签 ─────────────────────────────────────────────
tags = [('🤖 AI口语测评', (60,190,255)),
        ('📚 10万+绘本',  (60,220,140)),
        ('🎯 同步教材',   (255,190,60))]
ty = 316
for label, color in tags:
    bbox = draw.textbbox((28, ty), label, font=load_font(22))
    pw = bbox[2]-bbox[0]+18; ph = bbox[3]-bbox[1]+10
    draw.rounded_rectangle([26, ty-2, 26+pw, ty+ph], radius=6, fill=(*color, 200))
    draw.text((34, ty+2), label, font=load_font(22), fill=(255,255,255))
    ty += ph + 10

# ── 底部价格提示 ─────────────────────────────────────────
draw.rounded_rectangle([26, 520, 300, 570], radius=8, fill=(255,255,255,30))
draw.text((38, 526), '下载免费  · 7天体验 ¥4.9', font=load_font(22), fill=(255,255,255))

# ── 底部域名 ─────────────────────────────────────────────
draw.text((28, 576), 'go.xiachaoqing.com/jiazhangtong', font=load_font(17), fill=(160,210,255))

img.save(str(OUT), 'JPEG', quality=94)
print(f'生成完成: {OUT}  {W}x{H}')
