# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_mandela (3-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas; jairedson5 at gmail)"}

# slug: título de en.wikipedia (pageimages = imagen del infobox: carátula, logo o retrato)
WIKI = {
    "c_cod4": "Call of Duty 4: Modern Warfare", "c_mw2_2009": "Call of Duty: Modern Warfare 2", "c_mw2019": "Call of Duty: Modern Warfare (2019 video game)",
    "c_mw3_2011": "Call of Duty: Modern Warfare 3", "c_aw": "Call of Duty: Advanced Warfare", "c_waw": "Call of Duty: World at War",
    "c_bo1": "Call of Duty: Black Ops", "c_bo2": "Call of Duty: Black Ops II", "c_bo3": "Call of Duty: Black Ops III",
    "c_bocw": "Call of Duty: Black Ops Cold War", "c_finalfronts": "Call of Duty: World at War – Final Fronts",
    "wii": "Wii", "wii_zapper": "Wii Zapper", "ps2": "PlayStation 2", "evanescence": "Evanescence", "romero": "George A. Romero",
    "mandela": "Nelson Mandela", "okinawa": "Battle of Okinawa", "shuri": "Shuri Castle", "pripyat": "Pripyat", "virginia": "Virginia",
    "elena_siegman": "Elena Siegman", "teclado_f": "Press F to pay respects", "luna": "Moon", "knowyourmeme": "Know Your Meme",
}
# slug: página de callofduty.fandom.com
FANDOM = {
    "price_mw2019": "John Price", "gaz": "Kyle Garrick", "barkov": "Roman Barkov", "zakhaev": "Imran Zakhaev", "macmillan": "MacMillan",
    "soap": "John MacTavish", "ghost": "Simon Riley", "roach": "Gary Sanderson", "shepherd": "Herschel Shepherd", "makarov": "Vladimir Makarov",
    "foley": "Foley", "ramirez": "James Ramirez", "burger_town": "Burger Town", "irons": "Will Irons", "mitchell": "Jack Mitchell",
    "mason": "Alex Mason", "hudson": "Jason Hudson", "weaver": "Grigori Weaver", "reznov": "Viktor Reznov", "dragovich": "Nikita Dragovich",
    "menendez": "Raul Menendez", "josefina": "Josefina Menendez", "roebuck": "Roebuck", "polonsky": "Polonsky",
    "juggernog": "Juggernog", "pap": "Pack-a-Punch Machine", "double_tap": "Double Tap Root Beer", "wunderfizz": "Der Wunderfizz",
    "staminup": "Stamin-Up", "phd": "PhD Flopper", "caja": "Mystery Box", "qed": "Quantum Entanglement Device",
    "verruckt": "Verrückt", "der_riese": "Der Riese", "origins": "Origins", "revelations": "Revelations", "kino": "Kino der Toten",
    "cotd": "Call of the Dead", "moon": "Moon", "soe": "Shadows of Evil", "shadowman": "Shadowman", "nacht": "Nacht der Untoten",
    "standoff": "Standoff", "pala_dorada": "Golden Shovel", "casco_dorado": "Golden Helmet", "m1911": "M1911",
    "loose_ends": "Loose Ends", "one_shot": "One Shot, One Kill", "game_over": "Game Over", "breaking_point": "Breaking Point",
    "clean_house": "Clean House", "going_dark": "Going Dark", "wolverines": "Wolverines!", "numbers": "Numbers", "suffer": "Suffer With Me",
    "kino_115": "115 (song)", "robot_origins": "Giant Robot", "magnum44": ".44 Magnum", "raid": "Raid",
}


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
    sin = []
    for slug, base, org, tit, pausa in tareas:
        if (solo and slug not in solo) or _existe(slug):
            continue
        try:
            u = imagen(base, tit)
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
