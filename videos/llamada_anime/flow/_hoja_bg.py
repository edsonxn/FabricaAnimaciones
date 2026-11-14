import os
from PIL import Image, ImageDraw
A = {}
for ln in open('flow/_asig_bg.txt'):
    r, k, s, *_ = ln.split()
    if float(s) > 0.6: A.setdefault(k, []).append(r)
ks = sorted(A); W, H = 320, 179
for parte in range(2):
    sub = ks[parte*12:(parte+1)*12]
    hoja = Image.new('RGB', (W*5, H*len(sub)), 'black'); d = ImageDraw.Draw(hoja)
    for i, k in enumerate(sub):
        hoja.paste(Image.open(f'../llamada_domingo/flow/bg/{k}.jpg').resize((W, H)), (0, i*H)); d.text((4, i*H+4), k, fill='yellow')
        for j, r in enumerate(A[k]):
            hoja.paste(Image.open(f'flow/bg_raw/{r}.jpg').resize((W, H)), ((j+1)*W, i*H)); d.text(((j+1)*W+4, i*H+4), r, fill='cyan')
    hoja.save(f'flow/_hojas/bg_anime_{parte}.jpg', quality=85)
