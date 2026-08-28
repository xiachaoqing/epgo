from PIL import Image

src = '/Users/xiachaoqing/projects/doc/英语陪跑go/同步天天练.png'
img = Image.open(src)
w, h = img.size
print(f'原始尺寸: {w}x{h}')

# 截取上部 900px：标题 + 跑步插画，去掉底部课程亮点列表
crop_h = 900
cropped = img.crop((0, 0, w, crop_h))

# 转 RGB（去透明通道），白底
bg = Image.new('RGB', (w, crop_h), (255, 255, 255))
if img.mode == 'RGBA':
    bg.paste(cropped, mask=cropped.split()[3])
else:
    bg.paste(cropped)

out = '/Users/xiachaoqing/projects/epgo/jiazhangtong/thumbs/tongbu_crop.jpg'
bg.save(out, 'JPEG', quality=90)
print(f'裁剪完成: {w}x{crop_h} -> {out}')
