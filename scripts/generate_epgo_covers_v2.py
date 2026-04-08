from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

out = Path('/Users/xiachaoqing/projects/epgo/public/uploads/epgo-covers-v2')
out.mkdir(parents=True, exist_ok=True)

configs = {
    'ket':    {'bg1':'#1D4ED8','bg2':'#2563EB','accent':'#DBEAFE','title':'KET Exam','sub':'Vocabulary · Writing · Listening'},
    'pet':    {'bg1':'#15803D','bg2':'#16A34A','accent':'#DCFCE7','title':'PET Exam','sub':'Reading · Writing · Practice'},
    'reading':{'bg1':'#C2410C','bg2':'#EA580C','accent':'#FFEDD5','title':'English Reading','sub':'Intensive Reading · Skills'},
    'speech': {'bg1':'#6D28D9','bg2':'#7C3AED','accent':'#EDE9FE','title':'English Speech','sub':'Speaking · Structure · Ideas'},
    'daily':  {'bg1':'#0F766E','bg2':'#0EA5A4','accent':'#CCFBF1','title':'Daily English','sub':'Useful Phrases · Daily Input'},
    'download': {'bg1':'#7C2D12','bg2':'#C2410C','accent':'#FED7AA','title':'Free Downloads','sub':'PDF · Worksheets · Study Packs'},
    'about': {'bg1':'#1E293B','bg2':'#334155','accent':'#E2E8F0','title':'About EPGO','sub':'Platform · Method · Learning Path'},
}

try:
    font_title = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 72)
    font_sub = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf', 28)
    font_brand = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 24)
except Exception:
    font_title = ImageFont.load_default()
    font_sub = ImageFont.load_default()
    font_brand = ImageFont.load_default()

for key, cfg in configs.items():
    img = Image.new('RGB', (1200, 720), cfg['bg1'])
    draw = ImageDraw.Draw(img)

    r1,g1,b1 = int(cfg['bg1'][1:3],16), int(cfg['bg1'][3:5],16), int(cfg['bg1'][5:7],16)
    r2,g2,b2 = int(cfg['bg2'][1:3],16), int(cfg['bg2'][3:5],16), int(cfg['bg2'][5:7],16)
    for y in range(720):
        t = y / 719
        color = (int(r1*(1-t)+r2*t), int(g1*(1-t)+g2*t), int(b1*(1-t)+b2*t))
        draw.line((0,y,1200,y), fill=color)

    draw.rounded_rectangle((70,70,1130,650), radius=36, outline=(255,255,255,40), width=2)
    draw.rounded_rectangle((90,90,1110,630), radius=28, outline=(255,255,255,22), width=1)

    draw.ellipse((760,-80,1280,440), fill=(255,255,255,22))
    draw.ellipse((880,360,1320,800), fill=(255,255,255,16))
    draw.ellipse((-120,520,220,860), fill=(255,255,255,12))

    for i in range(5):
        x = 760 + i*56
        draw.rounded_rectangle((x,155,x+36,280), radius=12, fill=(255,255,255,28))
    for i in range(4):
        x = 820 + i*70
        draw.ellipse((x,470,x+42,512), fill=(255,255,255,30))

    draw.rounded_rectangle((105,120,245,165), radius=22, fill=cfg['accent'])
    draw.text((132,129), '英语陪跑GO', font=font_brand, fill=cfg['bg1'])

    draw.text((105,240), cfg['title'], font=font_title, fill='white')
    draw.text((108,335), cfg['sub'], font=font_sub, fill=(245,248,255))
    draw.line((108,390,330,390), fill=(255,255,255,170), width=4)

    card_y = 470
    labels = ['Focused Content', 'Clear Structure', 'Daily Growth']
    for i, text in enumerate(labels):
        x = 108 + i*235
        draw.rounded_rectangle((x, card_y, x+205, card_y+92), radius=18, fill=(255,255,255,26))
        draw.text((x+18, card_y+18), text, font=font_sub, fill='white')

    draw.text((108,600), 'Learn steadily. Build real progress.', font=font_sub, fill=(250,250,255))
    img.save(out / f'{key}.png')

print(out)
