from PIL import Image, ImageDraw
import glob, os
fs = sorted(glob.glob('pegatinas/*.png')); W = 240
S = Image.new('RGB', (W * 9, (W + 20) * ((len(fs) + 8) // 9)), (60, 60, 60))
for i, f in enumerate(fs):
    im = Image.open(f); im.thumbnail((W, W)); x, y = (i % 9) * W, (i // 9) * (W + 20)
    S.paste(im, (x, y), im); ImageDraw.Draw(S).text((x + 3, y + W + 3), os.path.basename(f)[:30], fill='yellow')
S.save('previews/pegatinas_hoja.jpg')
