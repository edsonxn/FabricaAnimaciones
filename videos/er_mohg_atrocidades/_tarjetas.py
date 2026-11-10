# -*- coding: utf-8 -*-
"""Tarjetas de comentarios REALES desde los .info.json de yt-dlp (la API da 403: token sin force-ssl, 10-nov-2026).
Mismas reglas que `yt comentario`: ≤ 10 días y nunca un id ya enseñado en otro video.
    python _tarjetas.py
"""
import datetime as dt
import glob
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import comentarios as C

IDS = ["UgzQzkzQm8Hgtqtjn4V4AaABAg", "UgwZNOqIbIepAyMYwcF4AaABAg", "Ugwwr2Qj8QL7rlGZMfd4AaABAg", "Ugx8DJiYZSnW7fEi4FZ4AaABAg",
       "Ugw1bm9aV6wukwm3RZZ4AaABAg", "UgzvfipRMhMbWKhpEa14AaABAg", "UgwYiYKsYsRQ1IFZUp14AaABAg", "Ugz8dOeV0BvZ8fzrW5x4AaABAg",
       "UgztGOwx19tTZK-XWsV4AaABAg", "Ugxbkmo3yYrzzhvuEdh4AaABAg", "Ugy3J9g_I8ZqBY_rauV4AaABAg"]
todos = {}
for f in glob.glob("_investigacion/*.info.json"):
    for c in json.load(open(f, encoding="utf-8")).get("comments", []):
        todos[c["id"]] = c
VID = os.path.dirname(os.path.abspath(__file__))
for i in IDS:
    c = todos[i]
    fecha = dt.date.fromtimestamp(c["timestamp"])
    if (dt.date.today() - fecha).days > 10:
        print("VIEJO", i)
        continue
    ya = [d for d in os.listdir(os.path.dirname(VID)) if d != os.path.basename(VID)
          and os.path.isfile(os.path.join(os.path.dirname(VID), d, "pegatinas", f"com_{i}.png"))]
    if ya:
        print("YA USADO", i, ya)
        continue
    d = dict(id=i, autor=c["author"], avatar=c.get("author_thumbnail"), fecha=fecha.isoformat(), likes=c.get("like_count", 0),
             texto=c["text"])
    print("ok", C.tarjeta(d, os.path.join(VID, "pegatinas", f"com_{i}.png")))
