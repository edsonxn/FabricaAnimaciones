# -*- coding: utf-8 -*-
"""Pegatinas NUEVAS de oot_mitos_reales (26-nov-2026; antes oot_remake_anadido). Las ya verificadas se copiaron de zelda_oot/ y oot_remake_cambios/.
zelda.fandom.com: búsqueda de archivos (namespace 6) con prefijo OoT; Wikipedia: pageimages. Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py
"""
import json, os, urllib.parse, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
ZELDA = {  # slug -> búsqueda (primer archivo que empiece por el prefijo) — 26-nov, oot_mitos_reales
    "locha": ("OoT Hylian Loach", "OoT"), "pescador": ("OoT Fishing Pond Owner Artwork", "OoT"),
    "corredor": ("OoT Running Man Artwork", "OoT"), "stalchild": ("OoT Stalchild Artwork", "OoT"),
    "fado": ("OoT Fado Artwork", "OoT"), "grog": ("OoT Grog Artwork", "OoT"), "stalfos": ("OoT Stalfos Artwork", "OoT"),
    "ganon": ("OoT Ganon Artwork", "OoT"), "escudo_espejo": ("OoT Mirror Shield Icon", "OoT"),
    "dampe": ("OoT Dampé Artwork", "OoT"), "malon": ("OoT Malon Artwork", "OoT"), "templo_sombras": ("OoT Shadow Temple", "OoT"),
    "sheik_ico": ("OoT Sheikah Symbol", "OoT"), "simbolo_gerudo": ("Gerudo Symbol", "Gerudo"), "potranca": ("OoT Epona Artwork", "OoT"),
}
WIKI = {"dd64": "64DD", "hyrule_historia": "Hyrule Historia", "kondo": "Koji Kondo", "tasbot": "TASBot",
        "gdq": "Games Done Quick", "cartucho": "The Legend of Zelda: Ocarina of Time", "majora_caja": "The Legend of Zelda: Majora's Mask",
        "gamecube_mq": "The Legend of Zelda: Ocarina of Time Master Quest"}


def _json(u): return json.load(urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=40))
def _bajar(u, r):
    with urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=60) as x, open(r, "wb") as f: f.write(x.read())

def zelda(q, pre):
    s = _json("https://zelda.fandom.com/api.php?" + urllib.parse.urlencode(dict(action="query", list="search", srsearch=q,
              srnamespace=6, srlimit=10, format="json")))["query"]["search"]
    for h in s:
        t = h["title"]
        if t.split(":", 1)[1].startswith(pre + "_") or t.split(":", 1)[1].startswith(pre + " "):
            p = _json("https://zelda.fandom.com/api.php?" + urllib.parse.urlencode(dict(action="query", titles=t, prop="imageinfo",
                      iiprop="url", format="json")))["query"]["pages"]
            for v in p.values():
                if "imageinfo" in v: return v["imageinfo"][0]["url"], t
    return None, None

def wiki(t):
    p = _json("https://en.wikipedia.org/w/api.php?" + urllib.parse.urlencode(dict(action="query", titles=t, prop="pageimages",
              piprop="original", redirects=1, format="json")))["query"]["pages"]
    for v in p.values():
        if "original" in v: return v["original"]["source"], t
    return None, None

fuentes = []
for slug, f in [(s, lambda q=q, p=p: zelda(q, p)) for s, (q, p) in ZELDA.items()] + [(s, lambda t=t: wiki(t)) for s, t in WIKI.items()]:
    if any(os.path.exists(os.path.join(PEG, slug + e)) for e in (".png", ".jpg", ".svg")): continue
    try:
        u, t = f()
        if not u: print("SIN IMAGEN", slug); continue
        e = ".png" if ".png" in u.lower() else (".svg" if ".svg" in u.lower() else ".jpg")
        _bajar(u, os.path.join(PEG, slug + e)); fuentes.append(f"{slug}\t{t}\t{u}"); print("ok", slug, t)
    except Exception as ex: print("ERROR", slug, ex)
open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8").write("\n".join(fuentes) + "\n")
