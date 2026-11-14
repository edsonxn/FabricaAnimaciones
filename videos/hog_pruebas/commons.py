# -*- coding: utf-8 -*-
"""Wikimedia Commons: buscar (con licencia y autor) y bajar.
   python commons.py buscar "texto" [n]
   python commons.py bajar <nombre_local> "File:Titulo.jpg" [ancho]
"""
import json, sys, urllib.parse, urllib.request
from pathlib import Path

AQUI = Path(__file__).parent
IMG = AQUI / "img"
API = "https://commons.wikimedia.org/w/api.php"
UA = {"User-Agent": "video-editor-script/1.0 (image lookup)"}


def api(**p):
    p.update(format="json")
    with urllib.request.urlopen(urllib.request.Request(API + "?" + urllib.parse.urlencode(p), headers=UA), timeout=40) as r:
        return json.load(r)


def info(titulos, ancho=1600):
    d = api(action="query", titles="|".join(titulos), prop="imageinfo", iiprop="url|size|extmetadata", iiurlwidth=ancho)
    sal = {}
    for p in d["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        m = ii.get("extmetadata", {})
        sal[p["title"]] = dict(url=ii.get("thumburl") or ii.get("url"), w=ii.get("width"), h=ii.get("height"),
                               lic=m.get("LicenseShortName", {}).get("value", "?"),
                               autor=__import__("re").sub("<[^>]+>", "", m.get("Artist", {}).get("value", "?"))[:70],
                               desc=__import__("re").sub("<[^>]+>", "", m.get("ImageDescription", {}).get("value", ""))[:110])
    return sal


def buscar(q, n=8):
    d = api(action="query", list="search", srsearch=q + " filetype:bitmap|drawing", srnamespace=6, srlimit=n)
    ts = [x["title"] for x in d["query"]["search"]]
    if not ts:
        print("nada"); return
    inf = info(ts)
    for t in ts:
        i = inf.get(t, {})
        print(f"{t}\n   {i.get('w')}x{i.get('h')} · {i.get('lic')} · {i.get('autor')} · {i.get('desc')}")


def bajar(nombre, titulo, ancho=1600):
    IMG.mkdir(exist_ok=True)
    i = info([titulo], ancho)[titulo]
    ext = ".png" if i["url"].lower().endswith(".png") else ".jpg"
    with urllib.request.urlopen(urllib.request.Request(i["url"], headers=UA), timeout=90) as r:
        (IMG / (nombre + ext)).write_bytes(r.read())
    cr = IMG / "creditos.json"
    c = json.loads(cr.read_text(encoding="utf-8")) if cr.exists() else {}
    c[nombre] = dict(titulo=titulo, lic=i["lic"], autor=i["autor"], desc=i["desc"])
    cr.write_text(json.dumps(c, ensure_ascii=False, indent=1), encoding="utf-8")
    print(nombre + ext, i["lic"], i["autor"])


if __name__ == "__main__":
    if sys.argv[1] == "buscar":
        buscar(sys.argv[2], int(sys.argv[3]) if len(sys.argv) > 3 else 8)
    else:
        bajar(sys.argv[2], sys.argv[3], int(sys.argv[4]) if len(sys.argv) > 4 else 1600)
