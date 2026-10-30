# -*- coding: utf-8 -*-
"""Pegatinas de bt_mundos_ranking: copia las de bt_jiggies_crueles y baja las nuevas de banjokazooie.fandom.com por la API (la página
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
VIEJAS = os.path.join(AQUI, "..", "bt_jiggies_crueles", "pegatinas")
H = {"User-Agent": "Mozilla/5.0"}
NUEVAS = {"blackeye": "Captain Blackeye", "tooty": "Tooty", "mr_pants": "Mr. Pants", "boggy_tooie": "Boggy", "george": "George Ice Cube",
          "mildred": "Mildred Ice Cube", "loggo": "Loggo", "dilberta": "Dilberta", "merry_maggie": "Merry Maggie Malpass", "pawno": "Pawno",
          "chompa": "Chompa", "stony_t": "Stony Transformation", "van": "Van Banjo", "snowball": "Snowball Banjo", "t_rex": "Daddy T-Rex",
          "detonator": "Detonator Banjo", "stomponadon": "Stomponadon", "dippy": "Dippy", "guffo": "Guffo", "golden_goliath": "Golden Goliath",
          "gobi": "Gobi", "mega_glowbo": "Mega Glowbo", "dragon_kazooie": "Dragon Kazooie", "kazooie_blaster": "Breegull Blaster",
          "skivvy": "Skivvy", "ssslumber": "Ssslumber", "lord_woo": "Lord Woo Fak Fak", "old_king_coal2": "Old King Coal",
          "gruntilda_bt": "Gruntilda Banjo-Tooie", "chilli_billi2": "Chilli Billi", "merry_christmas": "Boggy's Igloo"}
MUNDOS = {"mt": "Mayahem Temple", "ggm": "Glitter Gulch Mine", "ww": "Witchyworld", "jrl": "Jolly Roger's Lagoon", "tdl": "Terrydactyland",
          "gi": "Grunty Industries", "hfp": "Hailfire Peaks", "ccl": "Cloud Cuckooland"}


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
    for f in os.listdir(VIEJAS):
        if f.endswith(".png") and not os.path.exists(os.path.join(PEG, f)):
            shutil.copy(os.path.join(VIEJAS, f), PEG)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as log:
        for k, n in MUNDOS.items():
            if not bajar(f"File:{n} Title Card.png", "titulo_" + k, log):
                print("SIN TITULO", n)
            time.sleep(.3)
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
