# -*- coding: utf-8 -*-
"""Fotos REALES de cada animal para las pegatinas (regla de Wild Next Door, 18-oct-2026): imagen principal del artículo de
Wikipedia en inglés (Wikimedia Commons, licencia libre) a 1280 px -> pegatinas/<slug>.jpg + pegatinas/CREDITOS.md.
Uso: python _fotos.py [slug=Articulo ...]   (sin argumentos baja todas las de ESPECIES; con slug=Articulo cambia una)."""
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "FabricaAnimaciones/1.0 (wild next door educational video; contact via YouTube channel)"}
ESPECIES = {
    "possum": "Virginia_opossum", "lizard": "Western_fence_lizard", "bat": "Little_brown_bat",
    "snake": "Common_garter_snake", "toad": "American_toad", "bumble": "Bombus_impatiens",
    "dragon": "Anax_junius", "garden": "Argiope_aurantia", "beetle": "Ground_beetle", "hover": "Hoverfly",
    "milli": "Narceus_americanus", "lady": "Coccinella_septempunctata", "lantern": "Spotted_lanternfly",
    "tick": "Ixodes_scapularis",
}


def api(url, **p):
    q = url + "?" + urllib.parse.urlencode(dict(p, format="json", formatversion=2))
    for intento in range(8):            # la API también da 429 en ráfagas: esperar y reintentar
        try:
            return json.load(urllib.request.urlopen(urllib.request.Request(q, headers=UA), timeout=30))
        except urllib.error.HTTPError as e:
            if e.code != 429 or intento == 7:
                raise
            time.sleep(30 * (intento + 1))


def limpiar(html):
    return re.sub(r"<[^>]+>", "", html or "").strip()


def una(slug, art):
    pag = api("https://en.wikipedia.org/w/api.php", action="query", titles=art, prop="pageimages", piprop="name",
              redirects=1)["query"]["pages"][0]
    nombre = pag.get("pageimage")
    if not nombre:
        return f"| {slug} | {art} | SIN IMAGEN | | |"
    info = api("https://commons.wikimedia.org/w/api.php", action="query", titles="File:" + nombre, prop="imageinfo",
               iiprop="url|extmetadata", iiurlwidth=1280)["query"]["pages"][0]
    if "imageinfo" not in info:        # imagen local de Wikipedia (no libre): no se usa
        return f"| {slug} | {art} | NO ESTÁ EN COMMONS ({nombre}) | | |"
    ii = info["imageinfo"][0]
    md = ii.get("extmetadata", {})
    url = ii.get("thumburl") or ii["url"]
    for intento in range(6):            # upload.wikimedia.org responde 429 si se piden seguidas: esperar y reintentar
        try:
            datos = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
            break
        except urllib.error.HTTPError as e:
            if e.code != 429 or intento == 5:
                raise
            time.sleep(20 * (intento + 1))
    time.sleep(5)
    ext = ".png" if url.lower().endswith(".png") else ".jpg"
    open(os.path.join(DEST, slug + ext), "wb").write(datos)
    autor = limpiar(md.get("Artist", {}).get("value"))
    lic = limpiar(md.get("LicenseShortName", {}).get("value"))
    return f"| {slug} | {art} | {nombre} | {autor} | {lic} |"


if __name__ == "__main__":
    os.makedirs(DEST, exist_ok=True)
    cambios = dict(a.split("=", 1) for a in sys.argv[1:])
    especies = {**ESPECIES, **cambios} if not cambios else cambios
    ruta_cred = os.path.join(DEST, "CREDITOS.md")
    filas = {}
    if os.path.exists(ruta_cred):
        for l in open(ruta_cred, encoding="utf-8"):
            if l.startswith("| ") and not l.startswith("| slug"):
                filas[l.split("|")[1].strip()] = l.rstrip("\n")
    for slug, art in especies.items():
        try:
            filas[slug] = una(slug, art)
        except Exception as e:
            filas[slug] = f"| {slug} | {art} | ERROR {e} | | |"
        print(filas[slug])
    with open(ruta_cred, "w", encoding="utf-8") as f:
        f.write("# Fotos reales de las pegatinas (Wikimedia Commons)\n\n| slug | artículo | archivo | autor | licencia |\n|---|---|---|---|---|\n")
        f.write("\n".join(filas[k] for k in sorted(filas)) + "\n")
