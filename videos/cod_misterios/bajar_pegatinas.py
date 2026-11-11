# -*- coding: utf-8 -*-
"""Pegatinas REALES de cod_misterios (9-nov-2026): personajes de la wiki de Call of Duty (Fandom), carátulas, estudios y
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
    "c_cod3": "Call of Duty 3", "c_cod4": "Call of Duty 4: Modern Warfare", "c_mw3_2011": "Call of Duty: Modern Warfare 3",
    "c_mw2019": "Call of Duty: Modern Warfare (2019 video game)", "c_bo1": "Call of Duty: Black Ops", "c_bo2": "Call of Duty: Black Ops II",
    "c_bo3": "Call of Duty: Black Ops III", "c_bo4": "Call of Duty: Black Ops 4", "c_bo6": "Call of Duty: Black Ops 6",
    "c_bo7": "Call of Duty: Black Ops 7", "c_ghosts": "Call of Duty: Ghosts", "c_finesthour": "Call of Duty: Finest Hour",
    "c_warzone": "Call of Duty: Warzone", "c_bocw": "Call of Duty: Black Ops Cold War", "xbox360": "Xbox 360",
    "drdisrespect": "Dr Disrespect", "lovecraft": "H. P. Lovecraft", "jfk": "John F. Kennedy", "dealey": "Dealey Plaza",
    "foo_fighter": "Foo fighter", "zork": "Zork", "area51": "Area 51", "sr71": "Lockheed SR-71 Blackbird", "adfgvx": "ADFGVX cipher",
    "morse": "Morse code", "vhs": "VHS", "sledgehammer": "Sledgehammer Games", "treyarch": "Treyarch", "infinityward": "Infinity Ward",
    "alcatraz": "Alcatraz Island", "golden_gate": "Golden Gate Bridge", "cthulhu": "Cthulhu", "proyector": "Slide projector",
    "reddit": "Reddit",
}
# slug: página de callofduty.fandom.com
FANDOM = {
    "gobblegum": "GobbleGum", "private_eye": "GobbleGum/Black Ops III", "perkaholic": "Perk-a-Holic", "taylor": "John Taylor", "corvus": "Corvus",
    "frozen_forest": "Frozen Forest", "russman": "Russman", "misty": "Abigail \"Misty\" Briarton", "marlton": "Marlton Johnson",
    "stuhlinger": "Samuel Stuhlinger", "tranzit": "TranZit", "bus": "Bus", "dotn": "Dead of the Night", "alistair": "Alistair's Folly",
    "kino": "Kino der Toten", "dempsey": "Thomas \"Tank\" Dempsey", "nikolai": "Nikolai Belinski (Ultimis)", "takeo": "Takeo Masaki (Ultimis)",
    "richtofen": "Edward Richtofen", "motd": "Mob of the Dead", "dead_ops": "Dead Ops Arcade", "shadowman": "Shadowman",
    "soe": "Shadows of Evil", "nero": "Nero Blackstone", "jessica": "Jessica Rose", "jack": "Jack Vincent", "floyd": "Floyd Campbell",
    "apothicon": "Apothicon", "wmd": "WMD (mission)", "hangar18": "Hangar 18", "rorke": "Gabriel Rorke", "logan": "Logan Walker", "hesh": "David Walker",
    "riley": "Riley (Ghosts)", "reznov": "Viktor Reznov", "mason": "Alex Mason", "hudson": "Jason Hudson", "dragovich": "Nikita Dragovich",
    "vorkuta": "Vorkuta (level)", "ix": "IX", "der_eisendrache": "Der Eisendrache", "rk5": "RK5", "shiva": "Sheiva", "spectre": "Spectre (Specialist)",
    "ripper": "Ripper", "sanctuary": "Sanctuary", "davis": "Davis Family Vacation", "ironclad": "Ironclad", "vacant": "Vacant",
    "backlot": "Backlot", "origins": "Origins", "robot_origins": "Giant Robot", "samantha": "Samantha Maxis", "mp7": "MP7",
    "verdansk": "Verdansk", "bunker11": "Verdansk (map)", "alex": "Alex Keller", "ghost_mw19": "Simon Riley", "farah": "Farah Karim",
    "price": "John Price", "makarov": "Vladimir Makarov", "scorched_earth": "Scorched Earth (mission)", "the_giant": "The Giant", "kn44": "KN-44",
    "blundell": "Jason Blundell", "zombie_shield": "Zombie Shield", "chaos_theory": "Chaos Theory", "hotel_oasis": "Dust to Dust",
    "pawn": "Pawn Takes Pawn", "dragon": "Dragon (Enemy)", "wrath": "Wrath of the Ancients", "elemento115": "Element 115", "cia": "Central Intelligence Agency Data System", "c_warzone": "Call of Duty: Warzone",
    "sarah": "Sarah Davis", "jumpscare_motd": "Mob of the Dead/Easter Eggs", "summit": "Summit",
}
# slug: archivo concreto de la wiki de CoD (capturas que no son la imagen principal de su página)
ARCHIVO = {
    "adfgx_pantalla": "ADFGX Cipher LoadingScreen MOTD BO2.png", "cara_motd": "Man Face Jumpscare MOTD BO2.png",
    "ironclad_mapa": "Ironclad Map CoD3.png",
    # 10-nov: los 3 que no salieron por página (Richtofen era desambiguación; Warzone y Treyarch sin imagen en Wikipedia)
    "richtofen": "WWII Richtofen Laughing Closeup BO3.png", "c_warzone": "Warzone Logo Transparent WZ.png",
    "treyarch": "Treyarch logo.png", "infinityward": "Infinity Ward Logo.png", "xbox360": "Xbox360.png",
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
