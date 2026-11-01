# -*- coding: utf-8 -*-
"""Pegatinas REALES de n64_secretos (31-oct-2026): fotos de personas, consolas, accesorios y carátulas de Wikipedia (API pageimages),
personajes de mariowiki.com y Pokémon de Bulbapedia. Receta de spyro2/bajar_pegatinas.py. Fuentes en pegatinas/_fuentes.txt.
    python bajar_pegatinas.py            baja lo que falte (no repite lo que ya existe)
"""
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas; jairedson5 at gmail)"}

# slug: título de en.wikipedia (pageimages = la imagen del infobox: retrato, foto del aparato o carátula)
WIKI = {
    # personas
    "jim_clark": "James H. Clark", "yamauchi": "Hiroshi Yamauchi", "miyamoto": "Shigeru Miyamoto", "iwata": "Satoru Iwata",
    "sakurai": "Masahiro Sakurai", "sakaguchi": "Hironobu Sakaguchi", "itoi": "Shigesato Itoi", "eguchi": "Katsuya Eguchi",
    "sakamoto": "Yoshio Sakamoto", "ken_lobb": "Ken Lobb", "eric_caen": "Titus Interactive",
    # consola, rivales y hardware
    "n64": "Nintendo 64", "saturn": "Sega Saturn", "playstation": "PlayStation (console)", "gamecube": "GameCube",
    "mando_n64": "Nintendo 64 controller", "rumble_pak": "Rumble Pak", "transfer_pak": "Transfer Pak",
    "expansion_pak": "Nintendo 64 accessories", "dd64": "64DD", "ique": "iQue Player", "gb_camera": "Game Boy Camera",
    "game_boy": "Game Boy", "sgi_onyx": "SGI Onyx", "sgi": "Silicon Graphics", "vitality": "Wii Vitality Sensor",
    "switch2": "Nintendo Switch 2", "randnet": "Randnet", "lodgenet": "LodgeNet", "blockbuster": "Blockbuster (retailer)",
    "cd": "Compact disc", "ultra64_arcade": "Killer Instinct (1994 video game)", "cruisn": "Cruis'n USA",
    # carátulas
    "c_mario64": "Super Mario 64", "c_pilotwings": "Pilotwings 64", "c_shogi": "Saikyō Habu Shōgi", "c_mariokart": "Mario Kart 64",
    "c_goldeneye": "GoldenEye 007 (1997 video game)", "c_mariotennis": "Mario Tennis (2000 video game)", "c_excitebike": "Excitebike 64",
    "c_excitebike_nes": "Excitebike", "c_starfox": "Star Fox 64", "c_stadium": "Pokémon Stadium (1999 video game)",
    "c_pokered": "Pokémon Red and Blue", "c_clayfighter": "ClayFighter 63⅓", "c_superman": "Superman 64",
    "c_ki_gold": "Killer Instinct Gold", "c_snap": "Pokémon Snap", "c_perfectdark": "Perfect Dark", "c_dk64": "Donkey Kong 64",
    "c_bodyharvest": "Body Harvest", "c_gta3": "Grand Theft Auto III", "c_animalforest": "Animal Crossing (video game)",
    "c_re2": "Resident Evil 2 (1998 video game)", "c_marioparty": "Mario Party (video game)", "c_tetris64": "Tetris 64",
    "c_ff6": "Final Fantasy VI", "c_ff7": "Final Fantasy VII", "c_dq7": "Dragon Quest VII", "c_earthbound64": "EarthBound 64",
    "c_mother3": "Mother 3", "c_polygon": "Mario Artist", "c_warioware": "WarioWare, Inc.: Mega Microgames!",
    "c_smash": "Super Smash Bros. (video game)", "c_oot_remake": "The Legend of Zelda: Ocarina of Time", "c_majora": "The Legend of Zelda: Majora's Mask",
    # estudios
    "dma": "DMA Design", "rockstar_north": "Rockstar North", "rare": "Rare (company)", "angel_studios": "Rockstar San Diego",
    "square": "Square (video game company)", "hal": "HAL Laboratory", "paradigm": "Paradigm Simulation", "gamefan": "GameFan",
    "heritage": "Heritage Auctions", "digital_foundry": "Digital Foundry",
}
# slug: página de mariowiki.com (renders oficiales de personajes)
MARIO = {"waluigi": "Waluigi", "wario": "Wario", "mario": "Mario", "luigi": "Luigi", "donkey_kong": "Donkey Kong",
         "yoshi": "Yoshi", "bowser": "Bowser", "peach": "Princess Peach"}
# slug: archivo exacto de mariowiki.com (cuando la imagen de la página no es la de N64)
MARIO_ARCH = {"waluigi_tennis": "Waluigi MT64.png", "mario_tennis_art": "MarioTennisN64Artwork.png"}
# slug: página de Bulbapedia
BULBA = {"pikachu": "Pikachu (Pokémon)", "magikarp": "Magikarp (Pokémon)", "doduo": "Doduo (Pokémon)", "dodrio": "Dodrio (Pokémon)"}
# slug: página de una wiki de Fandom (personajes sin página en las otras)
FANDOM = {"samus": ("metroid", "Samus Aran"), "fox": ("starfox", "Fox McCloud"), "superman": ("dc", "Superman (Kal-El)"),
          "lex_luthor": ("dc", "Alexander Luthor (Prime Earth)")}


def _abrir(url, timeout):
    for i in range(5):                                      # Wikimedia corta con 429 si se va rápido: espera y reintenta
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
    """Archivo principal de la página: `page_image` de pageprops (incluye carátulas no libres, que pageimages no da)."""
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageprops|pageimages", piprop="name", format="json", redirects=1))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        pp = p.get("pageprops") or {}
        nombre = pp.get("page_image") or pp.get("page_image_free") or p.get("pageimage")
        return archivo(base, nombre) if nombre else None


def archivo(base, nombre):
    """URL del archivo; si es SVG, su PNG de 1200 px."""
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", iiurlwidth=1200, format="json"))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        ii = (p.get("imageinfo") or [{}])[0]
        u = ii.get("url")
        return ii.get("thumburl") if u and u.lower().split("?")[0].endswith(".svg") else u


def _existe(slug):
    return next((f for f in os.listdir(PEG) if os.path.splitext(f)[0] == slug), None)


def main():
    os.makedirs(PEG, exist_ok=True)
    reg_ruta = os.path.join(PEG, "_fuentes.txt")
    reg = open(reg_ruta, encoding="utf-8").read().splitlines() if os.path.exists(reg_ruta) else []
    hechos = {r.split(":", 1)[0] for r in reg}
    tareas = [(s, "https://en.wikipedia.org/w/api.php", "Wikipedia", t, False, 5) for s, t in WIKI.items()]
    tareas += [(s, "https://www.mariowiki.com/api.php", "mariowiki.com", t, False, .5) for s, t in MARIO.items()]
    tareas += [(s, "https://www.mariowiki.com/api.php", "mariowiki.com", t, True, .5) for s, t in MARIO_ARCH.items()]
    tareas += [(s, "https://bulbapedia.bulbagarden.net/w/api.php", "Bulbapedia", t, False, 1) for s, t in BULBA.items()]
    tareas += [(s, f"https://{w}.fandom.com/api.php", f"{w}.fandom.com", t, False, .5) for s, (w, t) in FANDOM.items()]
    sin = []
    for slug, base, org, tit, es_archivo, pausa in tareas:
        if _existe(slug) and slug in hechos:
            continue
        try:
            u = archivo(base, tit) if es_archivo else imagen(base, tit)
            if not u:
                print("SIN", slug, tit)
                sin.append(slug)
                continue
            ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower() or ".png"
            if ext not in (".png", ".jpg", ".jpeg", ".webp"):
                print("FORMATO", slug, u)
                sin.append(slug)
                continue
            ext = ".jpg" if ext == ".jpeg" else ext
            r = os.path.join(PEG, slug + ext)
            if not os.path.exists(r):
                _bajar(u, r)
            reg = [x for x in reg if not x.startswith(slug + ":")] + [f"{slug}: {org} «{tit}» {u}"]
            print("ok", slug, ext, os.path.getsize(r) // 1024, "KB")
        except Exception as e:
            print("ERR", slug, e)
            sin.append(slug)
        time.sleep(pausa)
    with open(reg_ruta, "w", encoding="utf-8") as f:
        f.write("\n".join(reg))
    print(f"\n{len(tareas) - len(sin)}/{len(tareas)} · sin imagen: {', '.join(sin) or '-'}")


if __name__ == "__main__":
    main()
