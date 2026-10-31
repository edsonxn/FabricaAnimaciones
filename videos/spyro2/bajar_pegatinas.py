# -*- coding: utf-8 -*-
"""Pegatinas REALES de spyro2 (30-oct-2026): artes de spyro.fandom.com (API pageimages por página) y fotos de personas de Wikipedia.
Fuentes en pegatinas/_fuentes.txt. Receta de mario64_secretos/bajar_pegatinas.py.
    python bajar_pegatinas.py
"""
import json
import os
import time
import urllib.parse
import urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
FANDOM = {"spyro": "Spyro", "sparx": "Sparx", "ripto": "Ripto", "crush": "Crush", "gulp": "Gulp", "hunter": "Hunter", "elora": "Elora",
          "moneybags": "Moneybags", "profesor": "The Professor", "zoe": "Zoe", "gnasty": "Gnasty Gnorc", "bianca": "Bianca",
          "juego1": "Spyro the Dragon (1998 video game)", "juego2": "Spyro 2: Ripto's Rage!", "juego3": "Spyro: Year of the Dragon",
          "reignited": "Spyro Reignited Trilogy", "realm": "Spyro: A Realm Beyond", "gear_grab": "Gear Grab", "cowlek": "Cowlek Corral",
          "landblubber": "Land Blubber", "breeze_builder": "Breeze Builder", "electroll": "Electroll", "water_worker": "Water Worker",
          "faunus": "Epilogue/Faunus Mortas", "basil": "Basil the Explorer", "avalar": "Avalar", "insomniac": "Insomniac Games",
          "toysforbob": "Toys for Bob"}
WIKI = {"copeland": "Stewart Copeland", "kenny": "Tom Kenny", "alazraqui": "Carlos Alazraqui", "ps1": "PlayStation (console)", "pocketstation": "PocketStation", "berger": "Gregg Berger", "kurzweil": "Kurzweil K2000"}


ARCHIVOS = {"spyro": "Spyro 2 Spyro render.png", "spyro2_logo": "Spyro2.png", "caja2": "Spyro2-riptos-rage-cover.jpg", "faunus_libro": "Faunus Mortas.jpg",
            "f_catabatus": "Catabatus.jpg", "f_armapillow": "Armapillow.jpg", "f_fistus": "Mister Fistus.jpg", "f_wuss": "Wuss.jpg",
            "f_farmae": "Farmae Robotum.jpg", "f_varmintum": "Varmintum.jpg", "f_guardus": "Guardus Fioritum.jpg", "f_druidus": "Druidus Schnikum.jpg",
            "f_lizardum": "Lizardum Fat Slobae.jpg", "f_tickus": "Nervous Tickus.jpg", "orbe": "Orb.png", "gema": "Gem.png", "gemas": "Gems.jpg",
            "engrane": "Gear.jpg", "gear_reto": "GearGrabChallenge.jpg", "sparx2": "Sparx Mugshot AotR.png", "arena_diff": "Ripto's Arena entrance differences.jpg"}


def _json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def _bajar(url, ruta):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def imagen(base, titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="original", format="json", redirects=1))
    for p in _json(base + "?" + q)["query"]["pages"].values():
        return (p.get("original") or {}).get("source")


def archivo(nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", format="json"))
    for p in _json("https://spyro.fandom.com/api.php?" + q)["query"]["pages"].values():
        return (p.get("imageinfo") or [{}])[0].get("url")


def main():
    os.makedirs(PEG, exist_ok=True)
    reg = []
    for slug, nom in ARCHIVOS.items():
        u = archivo(nom)
        if not u:
            print("SIN", slug, nom)
            continue
        ext = os.path.splitext(nom)[1].lower()
        r = os.path.join(PEG, slug + ext)
        if not os.path.exists(r):
            _bajar(u, r)
        reg.append(f"{slug}: spyro.fandom.com «{nom}» {u}")
        print("ok", slug, os.path.getsize(r) // 1024, "KB")
        time.sleep(.3)
    for dic, base, org in ((FANDOM, "https://spyro.fandom.com/api.php", "spyro.fandom.com"), (WIKI, "https://en.wikipedia.org/w/api.php", "Wikipedia")):
        for slug, tit in dic.items():
            try:
                u = imagen(base, tit)
                if not u:
                    print("SIN", slug, tit)
                    continue
                ext = os.path.splitext(urllib.parse.urlparse(u).path)[1].lower() or ".png"
                if ext == ".svg":
                    print("SVG", slug, u)
                    continue
                r = os.path.join(PEG, slug + ext)
                if not os.path.exists(r):
                    _bajar(u, r)
                reg.append(f"{slug}: {org} «{tit}» {u}")
                print("ok", slug, ext, os.path.getsize(r) // 1024, "KB")
            except Exception as e:
                print("ERR", slug, e)
            time.sleep(3 if dic is WIKI else .3)
    with open(os.path.join(PEG, "_fuentes.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(reg))


if __name__ == "__main__":
    main()
