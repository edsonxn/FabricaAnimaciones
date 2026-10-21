# -*- coding: utf-8 -*-
"""Copia a taller/ lo que usa la presentación «Antes de decir que sí» (21-oct-2026): fondos de Flow, pegatinas recortadas, el primer
y el último cuadro del corto (las costuras de las diapositivas 8 y 10), un tramo de la música de Lyria y las fuentes del corto.
    python taller/_materiales.py        (desde videos/la_sena, con PYTHONPATH="<video>;C:\\FabricaAnimaciones\\nucleo")"""
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
os.makedirs(IMG, exist_ok=True)
os.makedirs(os.path.join(AQUI, "fonts"), exist_ok=True)
os.makedirs(os.path.join(AQUI, "audio"), exist_ok=True)
os.makedirs(os.path.join(AQUI, "video"), exist_ok=True)

FONDOS = ["jalpa_panorama_a", "jalpa_panorama_b", "plaza_jalpa_a", "secundaria_patio_a", "salon_a", "huerta_guayaba_a",
          "azotea_noche_b", "cocina_dia_a", "cocina_noche_lluvia_a", "puerta_noche_a", "cuesta_tarde_b_a"]
PIEZAS = ["angel14_hoja/04", "angel14_hoja/02", "angel14_hoja/05", "tono19b_hoja/00", "tono19b_hoja/03", "tono19b_hoja/02",
          "rosa_hoja/04", "tono13_hoja/04", "angel8_hoja/04", "gente_hoja/02", "gente_hoja/03", "gente_hoja/05", "gente_hoja/06",
          "graduacion_gente_hoja/06", "utileria_casa/00", "utileria_casa/02", "utileria_casa/03", "utileria_casa/05",
          "utileria_casa/09", "utileria_fiesta/00", "utileria_fiesta/01", "naturaleza/08", "naturaleza/05", "naturaleza/01",
          "zanate_vuelo/00", "zanate_vuelo/02", "zanate_vuelo/04"]
CICLOS = ["angel14_camina"]

for f in FONDOS:
    Image.open(f"imagenes/{f}.jpg").convert("RGB").save(os.path.join(IMG, f + ".jpg"), quality=86)
for p in PIEZAS:
    im = Image.open(f"piezas/{p}.png").convert("RGBA")
    im.thumbnail((900, 900), Image.LANCZOS)
    im.save(os.path.join(IMG, "p_" + p.replace("/", "_") + ".png"), optimize=True)
for c in CICLOS:
    i = 0
    while os.path.exists(f"piezas/{c}/ciclo_{i:02d}.png"):
        im = Image.open(f"piezas/{c}/ciclo_{i:02d}.png").convert("RGBA")
        im.thumbnail((700, 700), Image.LANCZOS)
        im.save(os.path.join(IMG, f"c_{c}_{i:02d}.png"), optimize=True)
        i += 1

# las costuras con el corto: primer cuadro (diap. 8) y último (diap. 10)
import escenas as S  # noqa: E402
for nombre, t in (("corto_inicio", 1.0), ("corto_fin", S.TOTAL - 1.6)):
    a = (np.clip(S.render_mundo(t), 0, 1) * 255).round().astype(np.uint8)
    Image.fromarray(a).save(os.path.join(IMG, nombre + ".jpg"), quality=88)

# la música de la azotea (lo más cálido del corto) para la escritura privada de la diap. 11
a0, a1 = S._ESC["azotea"]["t0"], S._ESC["azotea"]["t1"]
subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-ss", f"{a0:.2f}", "-to", f"{a1:.2f}", "-i", "audio/musica.wav",
                "-af", f"afade=t=in:d=2,afade=t=out:st={a1 - a0 - 3:.2f}:d=3", "-c:a", "libmp3lame", "-b:a", "128k",
                os.path.join(AQUI, "audio", "musica_azotea.mp3")], check=True)

# fuentes: Poppins de «Hablemos» + Baskervville de los rótulos del corto
for f in ("poppins-400.woff2", "poppins-600.woff2", "poppins-800.woff2", "poppins-900.woff2"):
    shutil.copy(os.path.join(r"C:\googleimagenes\scratch\taller_hablemos\fonts", f), os.path.join(AQUI, "fonts", f))
FD = os.path.expanduser("~/AppData/Local/Microsoft/Windows/Fonts")
for f in ("Baskervville-Bold.ttf", "Baskervville-BoldItalic.ttf"):
    shutil.copy(os.path.join(FD, f), os.path.join(AQUI, "fonts", f.lower()))
for f in os.listdir(r"C:\googleimagenes\scratch\taller_hablemos\logos"):
    shutil.copy(os.path.join(r"C:\googleimagenes\scratch\taller_hablemos\logos", f), os.path.join(IMG, "logo_" + f))

tot = sum(os.path.getsize(os.path.join(r, f)) for r, _, fs in os.walk(AQUI) for f in fs)
print(f"taller/: {tot / 1e6:.1f} MB")
