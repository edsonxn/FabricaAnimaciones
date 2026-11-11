# -*- coding: utf-8 -*-
"""Pegatinas de los puestos NUEVOS de la lista v3 (10-nov-2026, sesión 3). Misma receta que _pegatinas.py:
íconos por id de Wowhead Forever; PNJ/lugares de Classic = imagen principal de su página de Wowpedia (título exacto);
personas y referencias reales = su página de Wikipedia / wiki de su juego (identidad = título exacto).
python _pegatinas_v3.py → pegatinas/<slug>.png (+ pantallas/) y vuelve a hacer previews/_hoja_peg.jpg (MIRARLA)."""
import io
import json
import os
import urllib.parse

from PIL import Image

import _pegatinas as P

ITEMS = {"o_carta": 4432}   # Sully Balloo's Letter
WIKI = {
    "pebblebitty": "Mountaineer Pebblebitty", "bombay_npc": "Bom'bay", "gadrin": "Master Gadrin", "zalazane": "Zalazane",
    "senjin": "Sen'jin Village", "mankrik": "Mankrik", "olgra": "Olgra", "cruce": "The Crossroads",
    "santuario": "Shrine of the Fallen Warrior", "koiter_npc": "Koiter", "michel": "Michel Koiter",
    "pirolena": "Pyrewood Village", "faerleia": "Deathstalker Faerleia", "morrison": "Lord Mayor Morrison",
    "moonrage": "Moonrage Watcher", "pyre_vigia": "Pyrewood Watcher", "sara": "Sara Balloo", "thandol": "Thandol Span",
    "dun_modr": "Dun Modr", "valle_reyes": "Valley of Kings", "zendraas": "Brother Zendraas", "silverlaine": "Baron Silverlaine",
}
OTRAS = {  # slug: (api, título exacto)
    "sullivan": ("https://en.wikipedia.org/w/api.php", "Sullivan Ballou"),
    "mumbo": ("https://banjokazooie.fandom.com/api.php", "Mumbo Jumbo"),
}


def una(api, titulo):
    q = urllib.parse.urlencode(dict(action="query", prop="pageimages", piprop="original", redirects=1, format="json", titles=titulo))
    r = json.loads(P.get(api + "?" + q))["query"]
    return next(iter(r["pages"].values())).get("original", {}).get("source")


def guarda(slug, url, log, txt):
    im = Image.open(io.BytesIO(P.get(url))).convert("RGBA")
    if max(im.size) >= 1000:
        g = im.copy()
        g.thumbnail((1920, 1920))
        g.convert("RGB").save(os.path.join(P.PAN, slug + ".jpg"), quality=92)
    im.thumbnail((700, 700))
    im.save(os.path.join(P.PEG, slug + ".png"))
    log.append(f"{slug}: {txt} {im.size} {url.split('/')[-1][:60]}")


def main():
    log = []
    for slug, i in ITEMS.items():
        try:
            log.append(f"{slug}: {P.icono(slug, i)}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    for slug, titulo in WIKI.items():
        try:
            url = una("https://wowpedia.fandom.com/api.php", titulo)
            if url:
                guarda(slug, url, log, titulo)
            else:
                log.append(f"SIN IMAGEN {slug} {titulo}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    for slug, (api, titulo) in OTRAS.items():
        try:
            url = una(api, titulo)
            guarda(slug, url, log, titulo) if url else log.append(f"SIN IMAGEN {slug} {titulo}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    with open(os.path.join(P.PEG, "_fuentes.txt"), "a", encoding="utf-8") as f:
        f.write("\n# v3\n" + "\n".join(log))
    print("\n".join(log))
    P.hoja()


if __name__ == "__main__":
    main()
