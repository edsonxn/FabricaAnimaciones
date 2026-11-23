# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_mandela_zombies (22-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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
    "c_waw": "Call of Duty: World at War", "c_bo1": "Call of Duty: Black Ops", "c_bo2": "Call of Duty: Black Ops II",
    "c_bo3": "Call of Duty: Black Ops III", "c_bo4": "Call of Duty: Black Ops 4", "c_cw": "Call of Duty: Black Ops Cold War",
    "c_mw3_23": "Call of Duty: Modern Warfare III (2023 video game)", "c_wz": "Call of Duty: Warzone", "c_aw": "Call of Duty: Advanced Warfare",
    "peleliu": "Peleliu", "shisa": "Shisa", "kowloon": "Kowloon Walled City", "hue": "Huế", "aral": "Vozrozhdeniya",
    "alcatraz": "Alcatraz Island", "b17": "Boeing B-17 Flying Fortress",
}
# slug: página de callofduty.fandom.com (22-nov-2026; IDENTIDAD comprobada en previews/pegatinas_check.jpg)
FANDOM = {
    "thundergun": "Thundergun", "little_resistance": "Little Resistance", "numbers": "Numbers",
    "nova6": "Nova 6", "gknova6": "GKNOVA6", "clarke": "Clarke", "five": "\"Five\"", "nixon": "Richard Nixon", "jfk": "John F. Kennedy/Zombies",
    "castro": "Fidel Castro/Zombies", "mcnamara": "Robert McNamara/Zombies", "hs10": "HS-10", "gorod": "Gorod Krovi", "nikolai": "Nikolai Belinski (Ultimis)",
    "nikolai_p": "Nikolai Belinski (Primis)", "the_defector": "The Defector", "mason": "Alex Mason", "woods": "Frank Woods",
    "verruckt": "Verrückt", "town": "Town", "speed_cola": "Speed Cola", "rem870": "Remington 870 MCS", "tranzit": "TranZit",
    "farm": "Farm", "bus_depot": "Bus Depot", "quick_revive": "Quick Revive", "type100": "Type 100", "shi_no_numa": "Shi No Numa",
    "der_riese": "Der Riese", "origins": "Origins", "shield": "Zombie Shield", "richtofen": "Edward Richtofen (Ultimis)", "kino": "Kino der Toten",
    "perk_cola": "Perk-a-Cola", "juggernog": "Juggernog", "moon": "Moon", "ascension": "Ascension", "nacht": "Nacht der Untoten",
    "hard_landing": "Hard Landing", "rebirth": "Rebirth", "rebirth_island": "Rebirth Island (Warzone)", "dead_ops": "Dead Ops Arcade",
    "tombstone": "Tombstone Soda", "mob": "Mob of the Dead", "blundergat": "Blundergat", "acid_gat": "Acid Gat", "magmagat": "Magmagat",
    "blood_dead": "Blood of the Dead", "electric_cherry": "Electric Cherry", "pap": "Pack-a-Punch", "bus": "Bus",
    "tedd": "T.E.D.D.", "jesse": "Jesse Snyder", "mystery_box": "Mystery Box", "zombie_royale": "Zombie Royale",
    "dempsey": "Tank Dempsey", "takeo": "Takeo Masaki", "teddy": "Teddy Bear",
}
ARCHIVO = {"raygun": "Ray Gun models BO.png"}   # la página «Ray Gun» trae la Mark II (hoja 22-nov)


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
        return ii.get("thumburl") or u   # miniatura de 1200 px: Wikimedia da 429 con los originales (22-nov)


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
