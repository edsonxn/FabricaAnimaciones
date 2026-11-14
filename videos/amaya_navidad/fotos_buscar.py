# -*- coding: utf-8 -*-
"""Fotos reales con licencia libre (Wikimedia Commons, sin clave): python fotos_buscar.py → fotos/cand/<clave>_<k>.jpg + fotos/cand.json
y la hoja previews/fotos_cand.jpg (clave_k sobre cada miniatura) para elegir a ojo, por identidad."""
import json
import os
import urllib.parse
import urllib.request
import urllib.error

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "FabricaAnimaciones/1.0 (video escolar; contacto no disponible)"}
BUSCA = {
    "tintec": "hair dye bowl brush", "tinted": "colorful hair extensions",
}
N = 3


def leer(url, intentos=6):
    import time
    for i in range(intentos):
        try:
            time.sleep(1.2)
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code != 429:
                raise
            time.sleep(6 * (i + 1))
    raise RuntimeError("429 persistente")


def api(params):
    url = "https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(params)
    return json.loads(leer(url))


def main():
    os.makedirs(os.path.join(AQUI, "fotos", "cand"), exist_ok=True)
    meta, tiles = {}, []
    for clave, q in BUSCA.items():
        r = api(dict(action="query", format="json", generator="search", gsrsearch=f"filetype:bitmap {q}", gsrnamespace=6,
                     gsrlimit=12, prop="imageinfo", iiprop="url|extmetadata|size", iiurlwidth=900))
        pags = sorted(r.get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        k = 0
        for p in pags:
            ii = (p.get("imageinfo") or [{}])[0]
            if not ii.get("thumburl") or ii.get("width", 0) < 500:
                continue
            em = ii.get("extmetadata", {})
            lic = em.get("LicenseShortName", {}).get("value", "")
            if not any(x in lic for x in ("CC", "Public domain", "PD")):
                continue
            dst = os.path.join(AQUI, "fotos", "cand", f"{clave}_{k}.jpg")
            try:
                data = leer(ii["thumburl"])
            except Exception:
                continue
            open(dst, "wb").write(data)
            autor = em.get("Artist", {}).get("value", "")
            import re
            autor = re.sub("<[^>]+>", "", autor).strip()
            meta[f"{clave}_{k}"] = dict(titulo=p["title"], pagina=ii.get("descriptionurl"), licencia=lic, autor=autor)
            im = cv2.imdecode(np.frombuffer(data, np.uint8), cv2.IMREAD_COLOR)
            if im is None:
                continue
            im = cv2.resize(im, (300, int(300 * im.shape[0] / im.shape[1])))[:220]
            im = cv2.copyMakeBorder(im, 0, 220 - im.shape[0], 0, 0, cv2.BORDER_CONSTANT)
            cv2.putText(im, f"{clave}_{k}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
            cv2.putText(im, f"{clave}_{k}", (6, 22), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            tiles.append(im)
            k += 1
            if k >= N:
                break
        print(clave, k)
    json.dump(meta, open(os.path.join(AQUI, "fotos", "cand_3.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    while len(tiles) % 6:
        tiles.append(np.zeros_like(tiles[0]))
    filas = [np.hstack(tiles[i:i + 6]) for i in range(0, len(tiles), 6)]
    cv2.imwrite(os.path.join(AQUI, "previews", "fotos_cand_3.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])


if __name__ == "__main__":
    main()
