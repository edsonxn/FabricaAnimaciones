# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_protagonistas (24-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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

# slug: título de en.wikipedia (pageimages = imagen del infobox: carátula, logo o retrato) — cod_protagonistas 24-nov-2026
WIKI = {
    "c_cod1": "Call of Duty (video game)", "c_cod4": "Call of Duty 4: Modern Warfare", "c_mw2": "Call of Duty: Modern Warfare 2",
    "c_mw3": "Call of Duty: Modern Warfare 3", "c_waw": "Call of Duty: World at War", "c_bo1": "Call of Duty: Black Ops",
    "c_bo2": "Call of Duty: Black Ops II", "c_bo3": "Call of Duty: Black Ops III", "c_cw": "Call of Duty: Black Ops Cold War",
    "c_bo6": "Call of Duty: Black Ops 6", "c_bo7": "Call of Duty: Black Ops 7", "c_gh": "Call of Duty: Ghosts",
    "c_iw": "Call of Duty: Infinite Warfare", "c_mw19": "Call of Duty: Modern Warfare (2019 video game)",
    "c_mw22": "Call of Duty: Modern Warfare II (2022 video game)", "c_mw23": "Call of Duty: Modern Warfare III (2023 video game)",
    "c_mw4": "Call of Duty: Modern Warfare 4", "c_aw": "Call of Duty: Advanced Warfare",
    "vorkuta": "Vorkuta", "pripyat": "Pripyat", "praga": "Prague", "arlington": "Arlington National Cemetery",
    "miraflores": "Panama Canal", "eurotunel": "Channel Tunnel", "tirpitz": "German battleship Tirpitz",
    "solovetsky": "Solovetsky Islands", "kumsusan": "Kumsusan Palace of the Sun", "highlands": "Glen Coe", "m1911": "M1911 pistol",
    "marte": "Mars", "titan": "Titan (moon)", "mar_negro": "Black Sea", "borjomi": "Borjomi", "noriega_real": "Manuel Noriega",
}
# slug: página de callofduty.fandom.com (IDENTIDAD comprobada en previews/pegatinas_check.jpg)
FANDOM = {
    "reyes": "Nick Reyes", "salter": "Nora Salter", "retribution": "UNSA Retribution", "ethan": "E3N",
    "logan": "Logan Walker", "hesh": "David \"Hesh\" Walker", "rorke": "Gabriel Rorke", "riley_gh": "Riley",
    "keller": "Alex Keller", "farah": "Farah Karim", "barkov": "Roman Barkov",
    "jackson": "Paul Jackson", "pelayo": "Pelayo", "alfulani": "Yasir Al-Fulani", "alasad": "Khaled Al-Asad",
    "victor": "Victor Zakhaev", "zakhaev": "Imran Zakhaev", "makarov": "Vladimir Makarov",
    "makarov_r": "Vladimir Makarov (Reboot)", "yuri": "Yuri (Modern Warfare)", "case": "William \"Case\" Calderon",
    "harrow": "Jane Harrow", "marshall": "Troy Marshall", "section": "David \"Section\" Mason", "harper": "Mike Harper",
    "karma": "Chloe \"Karma\" Lynch", "roach": "Gary \"Roach\" Sanderson", "ghost": "Simon \"Ghost\" Riley", "shepherd": "Shepherd",
    "ghost_r": "Simon \"Ghost\" Riley (Reboot)", "laswell": "Kate Laswell", "reznov": "Viktor Reznov", "mason": "Alex Mason",
    "hudson": "Jason Hudson", "dragovich": "Nikita Dragovich", "kravchenko": "Lev Kravchenko", "steiner": "Friedrich Steiner",
    "soap": "John \"Soap\" MacTavish", "price": "John Price", "woods": "Frank Woods", "menendez": "Raul Menendez",
    "bell": "Bell (Cold War)", "adler": "Russell Adler", "noriega": "Manuel Noriega", "player_bo3": "Player (Black Ops III)",
    "taylor": "John Taylor", "corvus": "Corvus", "hendricks": "Jacob Hendricks", "gaz_r": "Kyle \"Gaz\" Garrick", "gaz": "Gaz",
    "archer": "The Archer", "soap_r": "Johnny \"Soap\" MacTavish", "price_r": "John Price (Reboot)", "price_ww2": "Price (World War II)",
    "petrenko": "Dimitri Petrenko", "mitchell": "Jack Mitchell", "valeria": "Valeria Garza", "graves": "Phillip Graves",
    "dsm": "DSM", "tf141": "Task Force 141 (Reboot)", "konni": "Konni Group", "cradle": "Cradle",
    "m_blood_storm": "Operation Blood Storm", "m_ghost_killer": "The Ghost Killer", "m_furnace": "Into the Furnace",
    "m_shock": "Shock and Awe", "m_coup": "The Coup", "m_norussian": "No Russian", "m_blood_brothers": "Blood Brothers",
    "m_dust": "Dust to Dust", "m_checkmate": "Checkmate (level)", "m_judgment": "Judgment Day", "m_loose": "Loose Ends",
    "m_greater": "Greater Good", "m_vorkuta": "Vorkuta (level)", "m_payback": "Payback", "m_countdown": "The Final Countdown",
    "m_suffer": "Suffer With Me", "m_newworld": "New World", "m_life": "Life", "m_counter": "Counter Attack", "m_gameover": "Game Over",
    "m_trojan": "Trojan Horse", "m_tirpitz": "Battleship Tirpitz", "dmz": "DMZ",
}
ARCHIVO = {"allen": "Alexei Borodin MW3.png"}


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
