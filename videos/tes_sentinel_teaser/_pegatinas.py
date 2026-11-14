# -*- coding: utf-8 -*-
"""Baja las pegatinas (imagen REAL de la wiki de Fandom, elderscrolls.fandom.com) de pegatinas/_lista.json y arma el
mosaico previews/pegatinas.jpg para revisarlas (pageimages a veces trae otra cosa: MIRAR el mosaico).
_lista.json = {"slug": "Título de página (Skyrim)"} o {"slug": {"archivo": "Nombre.png"}}
    python _pegatinas.py            baja las que falten        python _pegatinas.py --rehacer slug1,slug2
"""
import io
import json
import os
import sys
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
API = "https://elderscrolls.fandom.com/api.php?"
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones; pegatinas)"}


def _api(**k):
    k.update(format="json")
    req = urllib.request.Request(API + urllib.parse.urlencode(k), headers=UA)
    return json.load(urllib.request.urlopen(req, timeout=40))


def url_de(entrada):
    if isinstance(entrada, dict) and "url" in entrada:      # imagen directa (p. ej. UESP cuando Fandom solo tiene el genérico)
        return entrada["url"], entrada["url"]
    if isinstance(entrada, dict):
        r = _api(action="query", prop="imageinfo", iiprop="url", iiurlwidth=800, titles="File:" + entrada["archivo"])
        p = next(iter(r["query"]["pages"].values()))
        ii = p.get("imageinfo", [{}])[0]
        return ii.get("thumburl") or ii.get("url"), "File:" + entrada["archivo"]
    r = _api(action="query", prop="pageimages", pithumbsize=800, titles=entrada, redirects=1)
    p = next(iter(r["query"]["pages"].values()))
    return p.get("thumbnail", {}).get("source"), entrada


def bajar(slug, entrada):
    url, de = url_de(entrada)
    if not url:
        print(f"  ✗ {slug}: sin imagen ({de})")
        return None
    req = urllib.request.Request(url, headers=UA)
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGBA")
    im.save(os.path.join(PEG, slug + ".png"))
    print(f"  ✓ {slug}: {im.size} ← {de}")
    return f"{slug}: {de} — {url}"


def mosaico():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png"))
    c, t = 8, 220
    filas = (len(fs) + c - 1) // c
    lien = Image.new("RGB", (c * t, filas * (t + 26)), (90, 90, 90))
    d = ImageDraw.Draw(lien)
    try:
        f = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        f = ImageFont.load_default()
    for i, n in enumerate(fs):
        im = Image.open(os.path.join(PEG, n)).convert("RGBA")
        im.thumbnail((t - 10, t - 10))
        x, y = (i % c) * t, (i // c) * (t + 26)
        lien.paste(im, (x + (t - im.width) // 2, y + (t - im.height) // 2), im)
        d.text((x + 6, y + t + 3), n[:-4], fill=(255, 255, 255), font=f)
    os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)
    lien.save(os.path.join(AQUI, "previews", "pegatinas.jpg"), quality=88)
    print(f"mosaico previews/pegatinas.jpg ({len(fs)} imágenes)")


def main():
    lista = json.load(open(os.path.join(PEG, "_lista.json"), encoding="utf-8-sig"))
    rehacer = set(sys.argv[sys.argv.index("--rehacer") + 1].split(",")) if "--rehacer" in sys.argv else set()
    fuentes_p = os.path.join(PEG, "_fuentes.txt")
    fuentes = dict(l.split(": ", 1) for l in open(fuentes_p, encoding="utf-8").read().splitlines() if ": " in l) \
        if os.path.exists(fuentes_p) else {}
    for slug, entrada in lista.items():
        if os.path.exists(os.path.join(PEG, slug + ".png")) and slug not in rehacer:
            continue
        try:
            r = bajar(slug, entrada)
            if r:
                fuentes[slug] = r.split(": ", 1)[1]
        except Exception as e:      # una que falle no tumba las demás
            print(f"  ✗ {slug}: {e}")
    with open(fuentes_p, "w", encoding="utf-8") as fo:
        fo.write("\n".join(f"{k}: {v}" for k, v in sorted(fuentes.items())) + "\n")
    mosaico()


if __name__ == "__main__":
    main()
