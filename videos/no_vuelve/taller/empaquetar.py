# -*- coding: utf-8 -*-
"""Empaqueta la presentación «Bájate de la rueda» en UN solo archivo (se abre sin internet en la compu del salón):
index.html + fonts + img + audio → Bajate_de_la_rueda.html. SIN el corto (21-oct, decisión del usuario): la historia de Diego
va en láminas dentro de la presentación.
    python taller/empaquetar.py      (desde videos/no_vuelve)"""
import base64
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
MIME = {".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2", ".ttf": "font/ttf", ".mp3": "audio/mpeg"}


def uri(p):
    return f"data:{MIME[os.path.splitext(p)[1]]};base64,{base64.b64encode(open(p, 'rb').read()).decode()}"


s = open("index.html", encoding="utf-8").read()
s = re.sub(r'url\(((?:fonts|img)/[\w\-.]+)\)', lambda m: f"url({uri(m.group(1))})", s)
s = re.sub(r'src="((?:img|audio)/[\w\-.]+)"', lambda m: f'src="{uri(m.group(1))}"', s)
dinamicos = sorted(f for f in os.listdir("img") if f.startswith(("c_diego14_camina_", "p_rueda_", "p_utileria_feria_", "p_utileria_casa_06")))
s = s.replace("<script>\n(()=>{", "<script>window.IMG={%s};</script>\n<script>\n(()=>{"
              % ",".join(f'"{f}":"{uri(os.path.join("img", f))}"' for f in dinamicos), 1)

open("Bajate_de_la_rueda.html", "w", encoding="utf-8").write(s)
print(round(os.path.getsize("Bajate_de_la_rueda.html") / 1e6, 1), "MB → taller/Bajate_de_la_rueda.html")
