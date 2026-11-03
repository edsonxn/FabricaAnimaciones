# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_mw4_secretos (2-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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
    "c_mw4": "Call of Duty: Modern Warfare 4", "c_mw2019": "Call of Duty: Modern Warfare (2019 video game)",
    "c_cod4": "Call of Duty 4: Modern Warfare", "c_mw2_2009": "Call of Duty: Modern Warfare 2",
    "c_mw3_2011": "Call of Duty: Modern Warfare 3", "c_aw": "Call of Duty: Advanced Warfare", "c_ghosts": "Call of Duty: Ghosts",
    "c_iw": "Call of Duty: Infinite Warfare", "c_mw2r": "Call of Duty: Modern Warfare 2 Campaign Remastered",
    "infinity_ward": "Infinity Ward", "activision": "Activision",
    "stephen_barton": "Stephen Barton", "gregson_williams": "Harry Gregson-Williams", "mads": "Mads Mikkelsen",
    "invader": "Invader (artist)",
    # 3-nov-2026: más pegatinas para llenar los tramos vacíos (el usuario: «faltan animaciones y pegatinas»)
    "gta6": "Grand Theft Auto VI", "pitfall": "Pitfall!", "famas": "FAMAS", "pripyat": "Pripyat", "impresora3d": "3D printing",
    "fideos": "Instant noodles", "pato_goma": "Rubber duck", "spiderman": "Spider-Man", "reddit": "Reddit", "mumbai": "Mumbai",
    "nueva_york": "New York City", "paris": "Paris", "pyongyang": "Pyongyang", "corea_norte_mapa": "North Korea",
    "matrix": "The Matrix", "humo": "Smoke grenade", "zombies_cod": "Call of Duty: Zombies",
}
# slug: página de callofduty.fandom.com
FANDOM = {
    "makarov": "Vladimir Makarov", "price": "John Price", "gaz": "Kyle Garrick", "ghost": "Simon Riley", "soap": "John MacTavish",
    "graves": "Phillip Graves", "laswell": "Kate Laswell", "shepherd": "Herschel Shepherd", "zakhaev": "Imran Zakhaev",
    "macmillan": "MacMillan", "riley_perro": "Riley", "griffin": "Griffin", "wallcroft": "Wallcroft",
    "mystery_box": "Mystery Box", "press_f": "Press F to Pay Respects", "war_pig": "War Pig",
    # 3-nov-2026: pantallas de misión de MW4 (pageimage = SelectScreen), personajes, armas y mapas
    "m_atrapados": "Stranded", "m_huida": "Escape (Modern Warfare 4)", "m_trafico": "Traffic (Modern Warfare 4)",
    "m_ordenes": "Following Orders", "m_contraataque": "Counter Attack", "m_hiredgun": "Hired Gun", "m_decap": "Decapitation",
    "m_final": "Greater Good", "m_nuevayork": "Out in the Cold", "m_bombay": "Gone Dark", "m_mayhem": "Mayhem (level)",
    "dunn": "Joseph Dunn", "ri": "Ri Ju-Young", "lider": "Ri Seung-Ho", "chow": "Cho \"Chow\" Han", "arquero": "The Archer",
    "patriot": "Patriot XMR", "cachette": "Cachette", "hajin_logo": "Hajin (map)", "dmz": "DMZ/Modern Warfare 4",
    "mw4_key": "Call of Duty: Modern Warfare 4", "war_pig_tanque": "War Pig (tank)", "jackson": "Paul Jackson", "ak74u": "AK-74u",
    "chapas": "Dog Tags", "ost_cod4": "War Pig (soundtrack)", "park": "Park Hyun-Jun", "shaw": "Shaw (Modern Warfare 4)",
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
