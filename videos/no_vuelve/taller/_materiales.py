# -*- coding: utf-8 -*-
"""Copia a taller/ lo que usa la presentación «Bájate de la rueda» (21-oct-2026): fondos de Flow (con nombre SIN variante: la
elegida está en FONDOS), pegatinas recortadas, la rueda y sus góndolas, el la canción de cuna de Lyria para la carta (diap. 9) y las fuentes del corto.
    python taller/_materiales.py        (desde videos/no_vuelve, con PYTHONPATH="<video>;C:\\FabricaAnimaciones\\nucleo")"""
import os
import shutil
import subprocess
import sys

import numpy as np
from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
VID = os.path.dirname(AQUI)
os.chdir(VID)
sys.path.insert(0, VID)
IMG = os.path.join(AQUI, "img")
for d in ("img", "fonts", "audio", "video"):
    os.makedirs(os.path.join(AQUI, d), exist_ok=True)

FONDOS = {"cocina_noche": "cocina_noche_a", "feria_noche": "feria_noche_a", "corredor_secu": "corredor_secu_a",
          "jardin_tarde": "jardin_tarde_a", "bajo_mesa": "bajo_mesa_a", "patio_noche": "patio_noche_a",
          "cocina_manana": "cocina_manana_a", "casa_fer": "casa_fer_a", "orientacion": "orientacion_a",
          "feria_atardecer": "feria_atardecer_a", "calle_amanecer": "calle_amanecer_a",
          "feria_alta_atardecer": "feria_alta_atardecer_a",
          "cocina_tarde": "cocina_tarde_a", "recamara_noche": "recamara_noche_a", "feria_alta_noche": "feria_alta_noche_a"}
PIEZAS = ["rueda/00", "utileria_feria/00", "utileria_feria/01", "utileria_feria/02", "utileria_feria/03", "utileria_feria/04",
          "utileria_feria/05", "utileria_feria/06", "utileria_feria/09", "utileria_casa/05", "utileria_casa/06",
          "gente_hoja/01", "gente_hoja/02", "fer_hoja/03", "fer_hoja/05", "diego14b_hoja/03",
          "diego14b_hoja/04", "duo_mesa_hoja/02", "abrazo_hoja/00", "lupe_b_hoja/01", "xime9_hoja/02", "gondolas_hoja/03",
          # la historia de Diego en láminas (21-oct: sin video)
          "gondolas_hoja/00", "papa_hoja/00", "papa_hoja/03", "diego8_hoja/00", "diego8_hoja/01", "diego8_hoja/02", "xime3_hoja/00",
          "lupe_hoja/01", "lupe_hoja/04", "duo_mesa_hoja/00", "duo_mesa_hoja/01", "utileria_casa/04", "utileria_casa/13",
          "utileria_casa/15", "diego14_hoja/01", "diego14_hoja/03", "diego14_hoja/04", "fer_hoja/02", "extra/diego_golpe",
          "xime9_hoja/00", "xime9_hoja/04", "diego14b_hoja/00", "abrazo_hoja/01", "abrazo_hoja/02"]
CICLOS = ["diego14_camina"]
GRANDES = {"rueda/00": 1400, "gondolas_hoja/00": 1200, "utileria_feria/04": 1200}     # 04 = patas en A (mapa real tras recortar, 21-oct)     # la rueda se ve grande en el título y en la diap. 11

for k, f in FONDOS.items():
    Image.open(f"imagenes/{f}.jpg").convert("RGB").save(os.path.join(IMG, k + ".jpg"), quality=86)
for p in PIEZAS:
    im = Image.open(f"piezas/{p}.png").convert("RGBA")
    lado = GRANDES.get(p, 900)
    im.thumbnail((lado, lado), Image.LANCZOS)
    im.save(os.path.join(IMG, "p_" + p.replace("/", "_") + ".png"), optimize=True)
for c in CICLOS:
    i = 0
    while os.path.exists(f"piezas/{c}/ciclo_{i:02d}.png"):
        im = Image.open(f"piezas/{c}/ciclo_{i:02d}.png").convert("RGBA")
        im.thumbnail((700, 700), Image.LANCZOS)
        im.save(os.path.join(IMG, f"c_{c}_{i:02d}.png"), optimize=True)
        i += 1

import escenas as S  # noqa: E402  (solo para los tiempos de la canción de cuna)

# la canción de cuna (las muñecas + el patio: lo más tierno del corto) para la carta de la diap. 9
if os.path.exists("audio/musica.wav"):
    a0, a1 = S._ESC["munecas"]["t0"], S._ESC["patio"]["t1"]
    subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a0:.2f}", "-to", f"{a1:.2f}", "-i", "audio/musica.wav",
                    "-af", f"afade=t=in:d=2,afade=t=out:st={a1 - a0 - 3:.2f}:d=3", "-c:a", "libmp3lame", "-b:a", "128k",
                    os.path.join(AQUI, "audio", "musica_cuna.mp3")], check=True)

# fuentes y logos: los mismos del taller «Antes de decir que sí» (la_sena)
LS = os.path.join(VID, "..", "la_sena", "taller")
for f in os.listdir(os.path.join(LS, "fonts")):
    shutil.copy(os.path.join(LS, "fonts", f), os.path.join(AQUI, "fonts", f))
for f in os.listdir(os.path.join(LS, "img")):
    if f.startswith("logo_"):
        shutil.copy(os.path.join(LS, "img", f), os.path.join(IMG, f))

tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(AQUI) for f in fs if not f.endswith(".html"))
print(f"taller/: {tot / 1e6:.1f} MB")
