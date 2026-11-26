# -*- coding: utf-8 -*-
"""Hoja «CADA IMAGEN ES DE LO QUE SE NOMBRA» (regla 6-nov-2026; copiado de wow_ruta_forever/_peg_check.py).
Con efectos.py: cada pegatina usada con la(s) frase(s) de la voz que la llaman (la primera cadena de su línea).
Sin efectos.py todavía (25-nov): cada pegatina con su escena y su identidad de pegatinas/_creditos.json (qué es y de dónde sale).
previews/pegatinas_check_NN.jpg (24 por hoja; las tarjetas com_* van al final).
    python _peg_check.py"""
import json
import os
import re
import textwrap

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
slugs = {f[:-4] for f in os.listdir(PEG) if f.endswith(".png")}
usos = {}
EF = os.path.join(AQUI, "efectos.py")
if os.path.isfile(EF) and os.environ.get("PEG_EFECTOS"):   # 25-nov: efectos.py aún sin pegatinas → por créditos
    for ln in open(EF, encoding="utf-8"):
        if ln.lstrip().startswith("#"):
            continue
        cads = re.findall(r'"([^"]+)"', ln)
        hits = [c for c in cads if c in slugs or "com_" + c in slugs]
        if not hits:
            continue
        frase = next((c for c in cads if c not in slugs and " " in c), cads[0])
        for h in hits:
            h = h if h in slugs else "com_" + h
            usos.setdefault(h, [])
            if frase not in usos[h]:
                usos[h].append(frase)
if not usos:   # efectos.py sin pegatinas todavía
    cred = json.load(open(os.path.join(PEG, "_creditos.json"), encoding="utf-8"))
    for s, c in cred.items():
        usos[s] = [f"[{c.get('escena', '?')}] {c.get('identidad', '')}"]
    for ln in open(os.path.join(PEG, "_comentarios.txt"), encoding="utf-8"):
        if ln.startswith("com_"):
            p = ln.split(" → ")
            usos[p[0][:-4]] = [f"[{p[3]}] {p[1]} · " + ln.split(" · ", 1)[-1].strip()]
F = ImageFont.truetype("arial.ttf", 17)
FB = ImageFont.truetype("arialbd.ttf", 19)
CW, CH, COLS, POR = 400, 330, 6, 24
items = sorted(usos.items(), key=lambda kv: (kv[0].startswith("com_"), kv[0]))
for k in range(0, len(items), POR):
    lote = items[k:k + POR]
    filas = (len(lote) + COLS - 1) // COLS
    hoja = Image.new("RGB", (CW * COLS, CH * filas), (25, 25, 25))
    d = ImageDraw.Draw(hoja)
    for i, (s, frases) in enumerate(lote):
        x, y = (i % COLS) * CW, (i // COLS) * CH
        im = Image.open(os.path.join(PEG, s + ".png")).convert("RGBA")
        im.thumbnail((CW - 20, 200))
        fondo = Image.new("RGBA", im.size, (70, 70, 70, 255))
        fondo.alpha_composite(im)
        hoja.paste(fondo.convert("RGB"), (x + (CW - im.width) // 2, y + 6))
        d.text((x + 8, y + 210), s, font=FB, fill=(255, 220, 80))
        t = " | ".join(frases)
        for j, l in enumerate(textwrap.wrap(t, 40)[:4]):
            d.text((x + 8, y + 236 + j * 21), l, font=F, fill=(230, 230, 230))
    out = os.path.join(AQUI, "previews", f"pegatinas_check_{k // POR + 1:02d}.jpg")
    hoja.save(out, quality=82)
    print(out)
print(len(items), "imágenes")
