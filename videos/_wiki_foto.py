# -*- coding: utf-8 -*-
"""Baja una foto de Wikimedia Commons (miniatura de 1280 px) y escribe su línea de créditos.
Uso: python videos/_wiki_foto.py <v> <slug> "<File title sin File:>" "<qué es, para CREDITOS.md>"
Deja videos/<v>/pegatinas/_orig/<slug>.jpg y añade la línea a videos/<v>/pegatinas/CREDITOS.md."""
import json
import os
import re
import sys
import urllib.parse
import urllib.request

v, slug, titulo, que = sys.argv[1:5]
AQUI = os.path.dirname(os.path.abspath(__file__))
dest = os.path.join(AQUI, v, "pegatinas")
os.makedirs(os.path.join(dest, "_orig"), exist_ok=True)
UA = {"User-Agent": "FabricaAnimaciones/1.0 (jairedson5@gmail.com)"}
api = ("https://commons.wikimedia.org/w/api.php?action=query&prop=imageinfo&iiprop=url|extmetadata&iiurlwidth=1280"
       "&format=json&titles=" + urllib.parse.quote("File:" + titulo))
p = list(json.load(urllib.request.urlopen(urllib.request.Request(api, headers=UA)))["query"]["pages"].values())[0]
ii = p["imageinfo"][0]
m = ii["extmetadata"]
autor = re.sub("<[^>]+>", "", m.get("Artist", {}).get("value", "")).strip()
lic = m.get("LicenseShortName", {}).get("value", "")
datos = urllib.request.urlopen(urllib.request.Request(ii.get("thumburl") or ii["url"], headers=UA)).read()
open(os.path.join(dest, "_orig", slug + ".jpg"), "wb").write(datos)
cred = os.path.join(dest, "CREDITOS.md")
if not os.path.exists(cred):
    open(cred, "w", encoding="utf-8").write("# Fotos reales (Wikimedia Commons)\n")
open(cred, "a", encoding="utf-8").write(f"- {slug}.jpg — {que}, {autor}, {lic} — {ii['descriptionurl']}\n")
print(slug, "|", autor, "|", lic)
