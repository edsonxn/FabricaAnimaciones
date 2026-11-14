# regenera flow/v3/cola.json (prompt + ingredientes en versión ligera JPG <=1280 px en flow/ingred/)
import sys, json, os; sys.path.insert(0, 'flow/v3'); import prompts as p
from PIL import Image
def lite(f):
    if f.startswith('pegatinas/'): n = 'flow/ingred/peg_' + os.path.splitext(os.path.basename(f))[0] + '.jpg'
    elif os.path.getsize(f) < 700000: return f
    else: n = os.path.splitext(f)[0] + '_l.jpg'
    if not os.path.exists(n):
        im = Image.open(f)
        if im.mode in ('RGBA', 'LA', 'P'):
            im = im.convert('RGBA'); bg = Image.new('RGB', im.size, (40, 40, 40)); bg.paste(im, mask=im.split()[3]); im = bg
        im = im.convert('RGB'); im.thumbnail((1280, 1280), Image.LANCZOS); im.save(n, quality=88)
    return n
c = {i: {'p': p.prompt(i)[0], 'ing': [lite(x) for x in p.prompt(i)[1]]} for i in p.E}
json.dump(c, open('flow/v3/cola.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=0); print(len(c))
