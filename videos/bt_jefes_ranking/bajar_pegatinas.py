# -*- coding: utf-8 -*-
"""Pegatinas de bt_50_secretos (las de bt_mundos_ranking ya copiadas): baja las nuevas de banjokazooie.fandom.com por la API (la página
da 402 a bots; la API responde). Busca por nombre de personaje en el espacio Archivo y prefiere los renders .png.
    python bajar_pegatinas.py          pegatinas/<slug>.png + _fuentes.txt
"""
import json
import os
import shutil
import time
import urllib.parse as p
import urllib.request as u

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
H = {"User-Agent": "Mozilla/5.0"}
NUEVAS = {"speccy": "Speccy", "goggles": "Goggles", "heggy": "Heggy", "trotty": "Trotty", "minjo": "Minjo", "hag1": "Hag 1",
          "jingaling": "King Jingaling", "clockwork": "Clockwork Kazooie", "warp_pad": "Warp Pad", "mumbo_pad": "Mumbo Pad",
          "bottles_ghost": "Bottles ghost", "jiggywiggy_temple": "Jiggywiggy's Temple", "shack_pack": "Shack Pack", "taxi_pack": "Taxi Pack",
          "breegull_bash": "Breegull Bash", "isla": "Isle o' Hags", "cauldron_keep": "Cauldron Keep", "tower_tragedy": "Tower of Tragedy",
          "gatehouse": "The Gatehouse", "bt_na": "Banjo-Tooie North American box", "bt_jp": "Banjo to Kazooie no Daibouken 2",
          "bt_eu": "Banjo-Tooie PAL box", "bt_xbla": "Banjo-Tooie Xbox Live Arcade", "dkr": "Diddy Kong Racing", "dk64": "Donkey Kong 64",
          "perfect_dark": "Perfect Dark", "jfg": "Jet Force Gemini", "juno": "Juno", "vela": "Vela", "nuts_bolts": "Nuts & Bolts",
          "hero_klungo": "Hero Klungo Sssavesss Teh World", "smash_banjo": "Banjo Kazooie Smash Ultimate", "alphette": "Alphette",
          "kirkhope": "Grant Kirkhope", "gregg_mayles": "Gregg Mayles", "castle_world": "Castle World", "cockeye": "Captain Cockeye",
          "dream": "Dream Land of Giants", "edson_dream": "Project Dream", "dk_plush": "Donkey Kong doll", "grunty_head": "Gruntilda head",
          "jamjars_silo": "Silo", "egg_pink": "Pink Mystery Egg", "egg_blue": "Blue Mystery Egg", "egg_yellow": "Yellow Mystery Egg"}
def api(**q):
    q.update(format="json")
    return json.load(u.urlopen(u.Request("https://banjokazooie.fandom.com/api.php?" + p.urlencode(q), headers=H), timeout=30))


def info(titulo):
    d = api(action="query", prop="imageinfo", iiprop="url|size", titles=titulo)
    for x in d["query"]["pages"].values():
        i = x.get("imageinfo")
        if i:
            return i[0]
    return None


def buscar(n):
    d = api(action="query", list="search", srnamespace=6, srlimit=10, srsearch=n)
    return [x["title"] for x in d["query"]["search"] if x["title"].lower().endswith((".png", ".jpg", ".jpeg"))]


def bajar(titulo, slug, log):
    i = info(titulo)
    if not i or i.get("width", 0) < 120:
        return False
    s = os.path.join(PEG, slug + ".png")
    data = u.urlopen(u.Request(i["url"], headers=H), timeout=40).read()
    open(s, "wb").write(data)
    log.write(f"{slug}: {titulo} ({i['width']}x{i['height']}) {i['url']}\n")
    print(slug, titulo, i["width"], i["height"], flush=True)
    return True


def main():
    os.makedirs(PEG, exist_ok=True)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as log:
        for slug, n in NUEVAS.items():
            if os.path.exists(os.path.join(PEG, slug + ".png")):
                continue
            ok = False
            for t in buscar(n):
                if bajar(t, slug, log):
                    ok = True
                    break
            if not ok:
                print("NADA", slug, n, flush=True)
            time.sleep(.3)


if __name__ == "__main__":
    main()
