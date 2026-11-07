# -*- coding: utf-8 -*-
"""Pegatinas NUEVAS de oot_remake_eliminado (6-nov-2026). Las ya verificadas se copiaron de zelda_oot/ y oot_remake_cambios/.
zelda.fandom.com: búsqueda de archivos (namespace 6) con prefijo OoT; Wikipedia: pageimages. Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py
"""
import json, os, urllib.parse, urllib.request
AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
ZELDA = {  # slug -> búsqueda (se toma el primer archivo que empiece por el prefijo)
    "kaepora": ("OoT Kaepora Gaebora Artwork", "OoT"), "lupa": ("OoT Lens of Truth Icon", "OoT"),
    "piedra_agonia": ("OoT Stone of Agony Icon", "OoT"), "gran_hada": ("OoT Great Fairy Artwork", "OoT"),
    "rupia_roja": ("OoT Red Rupee Model", "OoT"), "bomba": ("OoT Bomb Icon", "OoT"),
    "skulltula_dorada": ("OoT Gold Skulltula Model", "OoT"), "espada_kokiri": ("OoT Kokiri Sword Icon", "OoT"),
    "escudo_deku": ("OoT Deku Shield Icon", "OoT"), "mido": ("OoT Mido Artwork", "OoT"),
}
WIKI = {"fujibayashi": "Hidemaro Fujibayashi", "gamecube": "GameCube", "skyward_sword": "The Legend of Zelda: Skyward Sword",
        "rumble_pak": "Rumble Pak", "game_informer": "Game Informer", "ign": "IGN", "wind_waker": "The Legend of Zelda: The Wind Waker"}

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
