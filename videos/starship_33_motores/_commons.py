"""Fotos de Wikimedia Commons con User-Agent genérico.
  python _commons.py buscar "consulta" [n]      → títulos candidatos con licencia y tamaño
  python _commons.py bajar nombre "File:Título.jpg"   → imagenes/<nombre>.jpg (1600 px) + imagenes/creditos.json
"""
import json
import os
import sys
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "FabricaAnimaciones/1.0 (python-urllib)"}
API = "https://commons.wikimedia.org/w/api.php?"


def api(**kw):
    kw.update(format="json")
    req = urllib.request.Request(API + urllib.parse.urlencode(kw), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=40))


def info(titulos):
    d = api(action="query", titles="|".join(titulos), prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=1600)
    out = []
    for p in d["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        em = ii.get("extmetadata", {})
        out.append(dict(titulo=p["title"], url=ii.get("thumburl") or ii.get("url"), w=ii.get("width"), h=ii.get("height"),
                        licencia=em.get("LicenseShortName", {}).get("value", "?"),
                        autor=em.get("Artist", {}).get("value", "?")[:80]))
    return out


if sys.argv[1] == "buscar":
    time.sleep(6)
    n = int(sys.argv[3]) if len(sys.argv) > 3 else 8
    d = api(action="query", list="search", srsearch=sys.argv[2], srnamespace=6, srlimit=n)
    tit = [x["title"] for x in d["query"]["search"]]
    for x in info(tit) if tit else []:
        print(f'{x["w"]}x{x["h"]} | {x["licencia"]} | {x["titulo"]}')
elif sys.argv[1] == "bajar":
    nom, tit = sys.argv[2], sys.argv[3]
    x = info([tit])[0]
    os.makedirs(os.path.join(AQUI, "imagenes"), exist_ok=True)
    dest = os.path.join(AQUI, "imagenes", nom + ".jpg")
    req = urllib.request.Request(x["url"], headers=UA)
    data = urllib.request.urlopen(req, timeout=60).read()
    if not x["url"].lower().endswith((".jpg", ".jpeg")):
        import cv2
        import numpy as np
        im = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
        cv2.imwrite(dest, im, [cv2.IMWRITE_JPEG_QUALITY, 92])
    else:
        open(dest, "wb").write(data)
    cj = os.path.join(AQUI, "imagenes", "creditos.json")
    cr = json.load(open(cj, encoding="utf-8")) if os.path.exists(cj) else {}
    cr[nom] = dict(titulo=tit, licencia=x["licencia"], autor=x["autor"])
    json.dump(cr, open(cj, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(nom, "OK", x["licencia"])
    time.sleep(2)
