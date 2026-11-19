# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_mandela3 (19-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
personas de Wikipedia. Receta de videos/n64_secretos/bajar_pegatinas.py. Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py            baja lo que falte (no repite lo que ya existe)
"""
import json
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones/1.0 (pegatinas)"}

# slug: título de en.wikipedia (pageimages = imagen del infobox: carátula, logo o retrato)
WIKI = {
    "c_cod1": "Call of Duty (video game)", "c_cod2": "Call of Duty 2", "c_cod4": "Call of Duty 4: Modern Warfare",
    "c_waw": "Call of Duty: World at War", "c_mw2": "Call of Duty: Modern Warfare 2", "c_bo1": "Call of Duty: Black Ops",
    "c_bo2": "Call of Duty: Black Ops II", "c_bo3": "Call of Duty: Black Ops III", "c_bo4": "Call of Duty: Black Ops 4",
    "c_gh": "Call of Duty: Ghosts", "c_mw19": "Call of Duty: Modern Warfare (2019 video game)", "c_cw": "Call of Duty: Black Ops Cold War",
    "c_mwr": "Call of Duty: Modern Warfare Remastered", "c_mw2r": "Call of Duty: Modern Warfare 2 Campaign Remastered",
    "c_bo7": "Call of Duty: Black Ops 7", "c_bf4": "Battlefield 4", "tirpitz": "German battleship Tirpitz",
    "pripyat": "Pripyat", "piccadilly_circus": "Piccadilly Circus",
}
# slug: página de callofduty.fandom.com (19-nov-2026; IDENTIDAD comprobada en previews/pegatinas_check.jpg)
FANDOM = {
    "gaz": "Gaz", "gaz19": "Kyle Garrick", "zakhaev": "Imran Zakhaev", "price": "John Price", "price_ww2": "Price (World War II)",
    "soap": "John \"Soap\" MacTavish", "ghost": "Simon \"Ghost\" Riley", "macmillan": "MacMillan", "makarov": "Vladimir Makarov",
    "jackson": "Paul Jackson", "volker": "Volker", "seaknight": "CH-46 Sea Knight", "reznov": "Viktor Reznov", "petrenko": "Dimitri Petrenko",
    "menendez": "Raul Menendez", "david_mason": "David Mason", "alex_mason": "Alex Mason", "chloe": "Chloe Lynch", "kagan": "Emma Kagan",
    "hudson": "Jason Hudson", "allen": "Joseph Allen",
    "max_ammo": "Max Ammo", "nuke": "Tactical Nuke", "uav": "UAV", "airstrike": "Airstrike", "heli": "Attack Helicopter",
    "speed_cola": "Speed Cola", "double_tap": "Double Tap Root Beer", "mule_kick": "Mule Kick", "zombie_flesh": "Zombie Flesh",
    "monkey_bomb": "Cymbal Monkey", "raygun": "Ray Gun", "raygun2": "Ray Gun Mark II", "cryptid": "Cryptid", "extinction": "Extinction",
    "oitc": "One in the Chamber", "m1911": "M1911", "mannequin": "Mannequin", "adam": "A.D.A.M.",
    "nacht": "Nacht der Untoten", "tranzit": "TranZit", "farm": "Farm", "grief": "Grief", "buried": "Buried", "vengeance": "Vengeance",
    "nuketown": "Nuketown", "nuketown_z": "Nuketown Zombies", "alpha_omega": "Alpha Omega", "nuk3town": "Nuk3town",
    "outbreak": "Outbreak", "golova": "Golova", "piccadilly": "Piccadilly (map)", "all_ghillied": "All Ghillied Up",
    "no_russian": "No Russian", "shock_awe": "Shock and Awe", "judgment_day": "Judgment Day", "vendetta": "Vendetta",
    "their_land": "Their Land, Their Blood", "loose_ends": "Loose Ends", "game_over": "Game Over", "tf141": "Task Force 141",
}
# slug: archivo concreto de la wiki de CoD (se llena tras mirar la hoja si una página trae la imagen equivocada)
ARCHIVO = {}


def _abrir(url, timeout):
    for i in range(5):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=timeout)
        except urllib.error.HTTPError as e:
            if e.code != 429 or i == 4:
                raise
            time.sleep(20 * (i + 1))


def _json(url):
    return json.load(_abrir(url, 40))


def _bajar(url, ruta):
    with _abrir(url, 60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def imagen(base, titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageprops|pageimages", piprop="name|original", format="json",
                                    redirects=1))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        if "missing" in p:
            return None
        pp = p.get("pageprops") or {}
        nombre = pp.get("page_image") or pp.get("page_image_free") or p.get("pageimage")
        if nombre:
            return archivo(base, nombre)
        return (p.get("original") or {}).get("source")


def archivo(base, nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", iiurlwidth=1200, format="json"))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        u = ii.get("url")
        return ii.get("thumburl") if u and u.lower().split("?")[0].endswith(".svg") else u


def _existe(slug):
    return next((f for f in os.listdir(PEG) if os.path.splitext(f)[0] == slug), None)


def main():
    os.makedirs(PEG, exist_ok=True)
    solo = set(sys.argv[1:])
    reg_ruta = os.path.join(PEG, "_fuentes.txt")
    reg = open(reg_ruta, encoding="utf-8").read().splitlines() if os.path.exists(reg_ruta) else []
    tareas = [(s, "https://en.wikipedia.org/w/api.php", "Wikipedia", t, 3) for s, t in WIKI.items()]
    tareas += [(s, "https://callofduty.fandom.com/api.php", "callofduty.fandom.com", t, .5) for s, t in FANDOM.items()]
    tareas += [(s, "https://callofduty.fandom.com/api.php", "callofduty.fandom.com", "File:" + t, .5) for s, t in ARCHIVO.items()]
    sin = []
    for slug, base, org, tit, pausa in tareas:
        if (solo and slug not in solo) or _existe(slug):
            continue
        try:
            u = archivo(base, tit[5:]) if tit.startswith("File:") else imagen(base, tit)
            if not u:
                print("SIN", slug, tit)
                sin.append(slug)
                continue
            ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower()
            if ".png" in u.lower() and ext not in (".png", ".jpg", ".jpeg", ".webp"):
                ext = ".png"
            ext = {".jpeg": ".jpg"}.get(ext, ext if ext in (".png", ".jpg", ".webp") else ".jpg")
            r = os.path.join(PEG, slug + ext)
            _bajar(u, r)
            reg = [x for x in reg if not x.startswith(slug + ":")] + [f"{slug}: {org} «{tit}» {u}"]
            print("ok", slug, ext, os.path.getsize(r) // 1024, "KB")
        except Exception as e:
            print("ERR", slug, e)
            sin.append(slug)
        time.sleep(pausa)
    with open(reg_ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(reg))
    print(f"\nsin imagen: {', '.join(sin) or '-'}")


if __name__ == "__main__":
    main()
