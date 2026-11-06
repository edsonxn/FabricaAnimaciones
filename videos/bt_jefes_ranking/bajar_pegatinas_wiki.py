# -*- coding: utf-8 -*-
"""Pegatinas de bt_50_secretos que no están en la wiki de Banjo: fotos libres de Commons (hardware, Kirkhope) y portadas de
Wikipedia en inglés (archivos de cada artículo). Wikimedia da 429 si se va rápido: 3 s entre pedidos y reintento.
    python bajar_pegatinas_wiki.py      pegatinas/<slug>.<ext> + _fuentes.txt; imprime los archivos de cada artículo
"""
import json
import os
import time
import urllib.error
import urllib.parse as p
import urllib.request as u

AQUI = os.path.dirname(os.path.abspath(__file__))
H = {"User-Agent": "FabricaAnimaciones/1.0 (video research; contact via youtube)"}
W = "https://en.wikipedia.org/w/api.php"
C = "https://commons.wikimedia.org/w/api.php"


def pedir(url, binario=False):
    for k in range(5):
        try:
            time.sleep(3)
            r = u.urlopen(u.Request(url, headers=H), timeout=60).read()
            return r if binario else json.loads(r)
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(20 * (k + 1))
    raise RuntimeError("429 sin fin: " + url)


def api(base, **q):
    q.update(format="json")
    return pedir(base + "?" + p.urlencode(q))


def url(base, f):
    d = api(base, action="query", prop="imageinfo", iiprop="url|size", titles=f)
    for x in d["query"]["pages"].values():
        if x.get("imageinfo"):
            i = x["imageinfo"][0]
            return i["url"], i["width"], i["height"]


def get(slug, base, f, log):
    r = url(base, f)
    if not r:
        print("NADA", slug, f, flush=True)
        return
    ext = os.path.splitext(r[0].split("?")[0])[1].lower()
    open(os.path.join(AQUI, "pegatinas", slug + ext), "wb").write(pedir(r[0], True))
    log.write(f"{slug}: {f} {r[1]}x{r[2]} {r[0]}\n")
    print(slug, f, r[1], r[2], flush=True)


COMMONS = {"kirkhope": "File:Grant Kirkhope by Gage Skidmore.jpg", "gamecube": "File:GameCube-Console-Set.png",
           "n64": "File:Nintendo-64-wController-L.jpg", "n64_mando": "File:Nintendo-64-Controller-Gray-Flat.jpg",
           "expansion": "File:Nintendo-64-Memory-Expansion-Pak.jpg", "agdq": "File:Games Done Quick logo 2018.png"}
ARTICULOS = {"bt_na": "Banjo-Tooie", "dkr": "Diddy Kong Racing", "dk64": "Donkey Kong 64", "perfect_dark": "Perfect Dark",
             "jfg": "Jet Force Gemini", "xbox360": "Xbox 360", "smash": "Super Smash Bros. Ultimate"}

if __name__ == "__main__":
    with open(os.path.join(AQUI, "pegatinas", "_fuentes.txt"), "a", encoding="utf-8") as log:
        for slug, f in COMMONS.items():
            if not any(os.path.exists(os.path.join(AQUI, "pegatinas", slug + e)) for e in (".jpg", ".png")):
                get(slug, C, f, log)
        for slug, t in ARTICULOS.items():
            d = api(W, action="query", prop="images", titles=t, imlimit=50, redirects=1)
            fs = [i["title"] for x in d["query"]["pages"].values() for i in x.get("images", [])
                  if i["title"].lower().endswith((".jpg", ".png", ".jpeg"))]
            print(slug, t, fs, flush=True)
            portada = [f for f in fs if any(k in f.lower() for k in ("cover", "box", "art", "boxart"))]
            if portada:
                get(slug, W, portada[0], log)
