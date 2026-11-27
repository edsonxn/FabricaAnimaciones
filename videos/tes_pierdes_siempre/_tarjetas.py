# -*- coding: utf-8 -*-
"""Barre TODO cada clip de medios/ (3 cuadros/s) buscando TARJETAS de youtuber a mitad del clip: fondo plano (blanco, negro
o de un color) con texto, como «#8 Skeleton Dinner Party / Top 10 Slo-Mo Bow Kills» que salió en el 2:07 de la v3
(el usuario, 12-nov-2026). `_ultimos.py` solo mira el primer y el último cuadro: este mira todos.
  python _tarjetas.py [ids]   → lista de sospechosos + previews/_tarjetas_NN.jpg (cada sospechoso con su clip y segundo)"""
import glob, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw

os.chdir(os.path.dirname(os.path.abspath(__file__)))
FF = r"C:\ffmpeg\bin\ffmpeg"
W, H, FPS = 160, 90, 3
clips = sorted(glob.glob("medios/scene-*.mp4"))
if len(sys.argv) > 1:
    q = {f"scene-{int(x):03d}" for x in sys.argv[1].split(",")}
    clips = [c for c in clips if os.path.basename(c)[:-4] in q]


def cuadros(f):
    r = subprocess.run([FF, "-loglevel", "error", "-i", f, "-vf", f"fps={FPS},scale={W}:{H}", "-f", "rawvideo",
                        "-pix_fmt", "rgb24", "-"], capture_output=True)
    a = np.frombuffer(r.stdout, np.uint8)
    n = a.size // (W * H * 3)
    return a[:n * W * H * 3].reshape(n, H, W, 3)


def sospecha(im):
    """(motivo, valor) si el cuadro parece tarjeta: fondo plano dominante (un color cuantizado > 55 % del cuadro, sin contar
    el negro de una escena oscura salvo si es negro PURO con texto) o blanco dominante."""
    x = im.astype(np.float32) / 255
    lum = x.mean(2)
    sat = x.max(2) - x.min(2)
    blanco = ((lum > .85) & (sat < .12)).mean()
    if blanco > .40:
        return "blanco", blanco
    qz = (im // 32).reshape(-1, 3)
    cod = qz[:, 0] * 64 + qz[:, 1] * 8 + qz[:, 2]
    cuenta = np.bincount(cod, minlength=512)
    k = cuenta.argmax()
    dom = cuenta[k] / cod.size
    if k == 0:                                   # negro: solo si es negro puro con algo de texto claro encima
        puro = (lum < .03).mean()
        texto = ((lum > .7)).mean()
        if puro > .80 and .003 < texto < .15:
            return "negro+texto", puro
        # recorte vertical (o foto pequeña) sobre negro puro: columnas laterales enteras en negro (scene-113, 12-nov)
        lados = np.concatenate([lum[:, :W // 4], lum[:, -W // 4:]], 1)
        if (lados < .03).mean() > .97 and (lum[:, W // 3:2 * W // 3] > .08).mean() > .3:
            return "negro+recorte", puro
        return None
    if dom > .55:
        return "plano", dom
    return None


hallados = []
for c in clips:
    fr = cuadros(c)
    for i, im in enumerate(fr):
        s = sospecha(im)
        if s:
            hallados.append((os.path.basename(c)[:-4], i / FPS, s[0], s[1], im))
print(f"{len(clips)} clips barridos · {len(hallados)} cuadros sospechosos")
vistos = {}
for b, t, m, v, _ in hallados:
    vistos.setdefault(b, []).append(f"{t:.1f}s {m} {v:.2f}")
for b, l in vistos.items():
    print(f"  {b}: {len(l)} → {', '.join(l[:6])}{' …' if len(l) > 6 else ''}")
# hoja: como mucho 3 cuadros por clip (el primero, el del medio y el último sospechoso)
sel = []
for b in vistos:
    hs = [h for h in hallados if h[0] == b]
    for h in {id(x): x for x in (hs[0], hs[len(hs) // 2], hs[-1])}.values():
        sel.append(h)
por, cols = 30, 6
for k in range(0, len(sel), por):
    lote = sel[k:k + por]
    filas = (len(lote) + cols - 1) // cols
    hoja = Image.new("RGB", (cols * 320, filas * 200), (30, 30, 30))
    d = ImageDraw.Draw(hoja)
    for j, (b, t, m, v, im) in enumerate(lote):
        x, y = (j % cols) * 320, (j // cols) * 200
        hoja.paste(Image.fromarray(im).resize((320, 180)), (x, y))
        d.text((x + 4, y + 182), f"{b} {t:.1f}s {m} {v:.2f}", fill=(255, 220, 0))
    os.makedirs("previews", exist_ok=True)
    hoja.save(f"previews/_tarjetas_{k // por + 1:02d}.jpg", quality=85)
    print(f"previews/_tarjetas_{k // por + 1:02d}.jpg")
