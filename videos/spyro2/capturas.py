# -*- coding: utf-8 -*-
"""Capturas REALES del juego a 1080p para pegatinas y MG (mundos, pantallas_negras, discos): ffmpeg contra la URL directa del video.
ModernXP L9ePJJp1P8E y Jiggylookback qNBm6CYfAQs (segundos en verificacion_clips.md). Hoja de control: pegatinas/_capturas.jpg.
    python capturas.py
"""
import os
import subprocess
import sys
import time

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
MXP, JIG, CTR = "L9ePJJp1P8E", "qNBm6CYfAQs", "jtOfpZqVhok"
LISTA = [
    ("cap_summer", MXP, 1000), ("cap_autumn", MXP, 6110), ("cap_winter", MXP, 13850), ("cap_glimmer", MXP, 300), ("cap_idol", MXP, 1300),
    ("cap_colossus", MXP, 2110), ("cap_hurricos", MXP, 3050), ("cap_sunny", MXP, 3960), ("cap_aquaria", MXP, 4500), ("cap_skelos", MXP, 7150),
    ("cap_crystal", MXP, 7900), ("cap_breeze", MXP, 8560), ("cap_zephyr", MXP, 9260), ("cap_scorch", MXP, 10340), ("cap_fracture", MXP, 11220),
    ("cap_magma", MXP, 11580), ("cap_shady", MXP, 12360), ("cap_marsh", MXP, 15180), ("cap_cloud", MXP, 15990), ("cap_robotica", MXP, 16660),
    ("cap_metropolis", MXP, 17340), ("cap_canyon", MXP, 17880), ("cap_arena", MXP, 18230), ("cap_shores", MXP, 18830), ("cap_ned", MXP, 2243.5),
    ("cap_fisher", MXP, 8880), ("cap_murgen", MXP, 16445), ("cap_widgie", MXP, 7855), ("cap_hunter22", MXP, 5669.5), ("cap_cetro", MXP, 190),
    ("cap_moneda", JIG, 70), ("cap_dan", JIG, 77), ("cap_ctr", CTR, 200),
]


def url(vid):
    r = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height=1080][vcodec^=avc1]/bv*[height<=2160][height>=1080][vcodec^=avc1]/bv*[height>=720]",
                        "https://youtu.be/" + vid, "--no-warnings"], capture_output=True, text=True)
    return r.stdout.strip().split("\n")[0]


if __name__ == "__main__":
    pedidos = set(sys.argv[1:])
    urls = {}
    for slug, vid, s in LISTA:
        if pedidos and slug not in pedidos:
            continue
        ruta = os.path.join(PEG, slug + ".jpg")
        if os.path.exists(ruta) and not pedidos:
            continue
        urls.setdefault(vid, url(vid))
        for _ in range(4):     # el primer pedido a una URL recién firmada suele dar 403
            time.sleep(2)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "quiet", "-ss", str(s), "-i", urls[vid], "-frames:v", "1", "-q:v", "2", ruta], timeout=120)
            if os.path.exists(ruta):
                break
        print(slug, os.path.exists(ruta), flush=True)
    n = len(LISTA)
    cols = 7
    hoja = Image.new("RGB", (cols * 270, ((n + cols - 1) // cols) * 152), "black")
    for i, (slug, _, _) in enumerate(LISTA):
        ruta = os.path.join(PEG, slug + ".jpg")
        if os.path.exists(ruta):
            c = Image.open(ruta).convert("RGB").resize((270, 152))
            ImageDraw.Draw(c).text((4, 4), slug[4:], fill=(255, 255, 0))
            hoja.paste(c, ((i % cols) * 270, (i // cols) * 152))
    hoja.save(os.path.join(PEG, "_capturas.jpg"), quality=80)
