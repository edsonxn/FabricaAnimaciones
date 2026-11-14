# hojas de contacto previews/flow3_hoja_N.jpg (12 por hoja, id + frase debajo) con las ELEGIDAS
import sys, json, glob, os, textwrap
sys.path.insert(0, 'flow/v3'); import prompts as p
from PIL import Image, ImageDraw, ImageFont
B = {x['id'][-3:]: x['texto'] for x in json.load(open('beats.json', encoding='utf-8'))}
ids = [i for i in sorted(p.E) if os.path.exists(f'pegatinas/flow3_{i}.png')]
try: F = ImageFont.truetype('arial.ttf', 17); FB = ImageFont.truetype('arialbd.ttf', 22)
except Exception: F = FB = ImageFont.load_default()
tw, th, tx = 620, 346, 92; W = 3
for h in range(0, len(ids), 12):
    grp = ids[h:h+12]; rows = (len(grp) + W - 1) // W
    s = Image.new('RGB', (W * (tw + 10) + 10, rows * (th + tx + 10) + 10), (18, 18, 18)); d = ImageDraw.Draw(s)
    for k, i in enumerate(grp):
        x = 10 + (k % W) * (tw + 10); y = 10 + (k // W) * (th + tx + 10)
        im = Image.open(f'pegatinas/flow3_{i}.png').convert('RGB').resize((tw, th)); s.paste(im, (x, y))
        d.text((x, y + th + 4), i + ' · ' + p.E[i][0], font=FB, fill=(255, 210, 60))
        for n, l in enumerate(textwrap.wrap(B.get(i, ''), 70)[:3]): d.text((x, y + th + 30 + n * 20), l, font=F, fill=(230, 230, 230))
    out = f'previews/flow3_hoja_{h // 12 + 1}.jpg'; s.save(out, quality=85); print(out, grp)
