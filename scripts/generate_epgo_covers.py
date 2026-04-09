from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path('/Users/xiachaoqing/projects/epgo/public/uploads/epgo-covers')
out.mkdir(parents=True, exist_ok=True)
colors = {
    'ket': ('#2563EB', '#1D4ED8'),
    'pet': ('#16A34A', '#15803D'),
    'reading': ('#EA580C', '#C2410C'),
    'speech': ('#7C3AED', '#6D28D9'),
    'daily': ('#0891B2', '#0E7490'),
}
labels = {
    'ket': 'KET\nPractice',
    'pet': 'PET\nPractice',
    'reading': 'English\nReading',
    'speech': 'English\nSpeech',
    'daily': 'Daily\nEnglish',
}

for key, (c1, c2) in colors.items():
    img = Image.new('RGB', (1200, 720), c1)
    draw = ImageDraw.Draw(img)
    r1, g1, b1 = int(c1[1:3], 16), int(c1[3:5], 16), int(c1[5:7], 16)
    r2, g2, b2 = int(c2[1:3], 16), int(c2[3:5], 16), int(c2[5:7], 16)
    for y in range(720):
        t = y / 719
        color = (
            int(r1 * (1 - t) + r2 * t),
            int(g1 * (1 - t) + g2 * t),
            int(b1 * (1 - t) + b2 * t),
        )
        draw.line((0, y, 1200, y), fill=color)
    for i in range(8):
        x = 80 + i * 130
        draw.rounded_rectangle((x, 90, x + 90, 180), 18, outline=(255, 255, 255, 45), width=3)
    for i in range(5):
        x = 140 + i * 180
        draw.ellipse((x, 450, x + 160, 610), outline=(255, 255, 255, 40), width=4)
    try:
        font_big = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 84)
        font_small = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 30)
    except Exception:
        font_big = ImageFont.load_default()
        font_small = ImageFont.load_default()
    draw.text((90, 240), labels[key], font=font_big, fill='white', spacing=10)
    draw.text((92, 430), '英语陪跑GO · Learning Cover', font=font_small, fill=(235, 245, 255))
    img.save(out / f'{key}.png')

print(out)
