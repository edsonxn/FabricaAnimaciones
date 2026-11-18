# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_villanos (17-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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
    "c_cod4": "Call of Duty 4: Modern Warfare", "c_waw": "Call of Duty: World at War", "c_mw2": "Call of Duty: Modern Warfare 2",
    "c_mw3": "Call of Duty: Modern Warfare 3", "c_bo1": "Call of Duty: Black Ops", "c_bo2": "Call of Duty: Black Ops II",
    "c_gh": "Call of Duty: Ghosts", "c_aw": "Call of Duty: Advanced Warfare", "c_iw": "Call of Duty: Infinite Warfare",
    "c_ww2": "Call of Duty: WWII", "c_mw19": "Call of Duty: Modern Warfare (2019 video game)",
    "c_cw": "Call of Duty: Black Ops Cold War", "c_mw22": "Call of Duty: Modern Warfare II (2022 video game)",
    "c_mw23": "Call of Duty: Modern Warfare III (2023 video game)", "c_bo6": "Call of Duty: Black Ops 6",
    "kevin_spacey": "Kevin Spacey", "kit_harington": "Kit Harington",
}
# slug: página de callofduty.fandom.com (17-nov-2026; IDENTIDAD comprobada en previews/pegatinas_check.jpg)
FANDOM = {
    # villanos
    "zakhaev": "Imran Zakhaev", "alasad": "Khaled Al-Asad", "victor": "Victor Zakhaev", "shepherd": "Shepherd",
    "makarov": "Vladimir Makarov", "dragovich": "Nikita Dragovich", "kravchenko": "Lev Kravchenko", "steiner": "Friedrich Steiner",
    "menendez": "Raul Menendez", "rorke": "Gabriel Rorke", "irons": "Jonathan Irons", "kotch": "Salen Kotch",
    "heinrich": "Heinrich", "barkov": "Roman Barkov", "wolf": "Omar \"The Wolf\" Sulaman", "hassan": "Hassan Zyani", "graves": "Phillip Graves",
    "makarov_r": "Vladimir Makarov (Reboot)", "perseus": "Perseus (Cold War)", "harrow": "Jane Harrow", "amsel": "Heinrich Amsel",
    "richtofen": "Edward Richtofen (Ultimis)",
    # héroes y testigos
    "price": "John Price", "soap": "John \"Soap\" MacTavish", "gaz": "Gaz", "griggs": "Griggs", "kamarov": "Sergeant Kamarov",
    "yuri": "Yuri (Modern Warfare)", "roach": "Gary \"Roach\" Sanderson", "ghost": "Simon \"Ghost\" Riley", "nikolai": "Nikolai",
    "mason": "Alex Mason", "woods": "Frank Woods", "reznov": "Viktor Reznov", "hudson": "Jason Hudson", "weaver": "Grigori Weaver",
    "david_mason": "David Mason", "harper": "Mike Harper", "farid": "Farid Ali", "chloe": "Chloe Lynch", "logan": "Logan Walker",
    "hesh": "Hesh", "elias": "Elias Walker", "mitchell": "Jack Mitchell", "gideon": "Gideon", "reyes": "Nick Reyes",
    "salter": "Nora Salter", "ethan": "E3N", "daniels": "Ronald Daniels", "zussman": "Robert Zussman", "farah": "Farah Karim",
    "kyle": "Kyle Garrick", "hadir": "Hadir Karim", "alejandro": "Alejandro Vargas", "laswell": "Kate Laswell", "adler": "Russell Adler",
    "bell": "Bell (Cold War)", "case": "William \"Case\" Calderon", "marshall": "Troy Marshall", "petrenko": "Dimitri Petrenko", "dempsey": "\"Tank\" Dempsey",
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
