# -*- coding: utf-8 -*-
"""Pegatinas REALES de mario64_secretos (29-oct-2026): artes y modelos oficiales de Super Mario Wiki (mariowiki.com, API
imageinfo por nombre de archivo; la lista completa de archivos de Mario 64 está en pegatinas/_mariowiki_lista.txt) y fotos de
personas/hardware de Wikipedia. Fuentes en pegatinas/_fuentes.txt. Receta de majora_mask/bajar_pegatinas.py.
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

MARIOWIKI = {        # slug: nombre de archivo en mariowiki.com
    "mario": "SM64_Artwork_Mario_(Jump).png", "mario_bobomb": "SM64_Artwork_Mario_and_Bob-omb.png",
    "mario_bowser": "Mario and Bowser Fire Artwork - Super Mario 64.png",
    "estrella": "SM64_Artwork_Power_Star.png", "lakitu": "SM64_Artwork_Lakitu_Bro.png", "camara": "SM64_Artwork_Camera.png",
    "mips": "SM64_Asset_Model_MIPS.png", "unagi": "Unagi SM64.png", "pinguino": "SM64_Artwork_Penguin_(Big).png",
    "pinguinos": "SM3DAS_SM64_Penguins.png", "yoshi": "SM64_Artwork_Yoshi.png", "yoshi_msg": "SM3DAS_SM64_Yoshi_message.jpg",
    "peach": "SM64_Asset_Model_Princess_Peach.png", "toad": "SM64_Asset_Model_Toad.png", "boo": "SM64_Asset_Model_Boo.png",
    "chomp": "SM64_Asset_Model_Chain_Chomp.png", "bully": "SM64_Asset_Model_Bully.png", "chill_bully": "SM64_Asset_Model_Chill_Bully.png",
    "hoot": "SM64_Asset_Model_Hoot.png", "blargg": "SM64 Blargg Model.png", "motos": "SM64 Motos left.png",
    "luigi_modelo": "SuperMario64LuigiModel.jpg", "cabeza": "Mario's Head Model SM64.png",
    "caja_jp": "SM64 Box Art Artwork Japan.jpg", "caja_pal": "Super Mario 64 PAL box art.png", "caja_ds": "SM64DS Box CAN.jpg",
    "caja_3das": "Box NA-Super Mario 3D All-Stars.png", "castillo": "SM64_Artwork_Mushroom_Castle.jpg",
    "placa": "SM64_Screenshot_Courtyard_Statue_Plaque.jpg", "reloj": "SM64_Screenshot_Clock.png",
    "cuadro_ttc": "SM3DAS-Tick_Tock_Clock_Painting.png", "cuadro_wdw": "SM3DAS-Wet_Dry_World_painting.png",
    "cuadro_jrb": "SM3DAS-Jolly_Roger_Bay_Painting.png", "cuadro_ccm": "SM3DAS-Cool_Cool_Mountain_painting.png",
    "cuadro_peach": "SM3DAS-Peach_Painting.png", "cuadro_bowser": "SM3DAS-Bowser_painting_SM64.png",
    "escalera": "NM SM64 The Endless Stairs.jpg", "gorro_invisible": "SM64_Vanish_Cap.png", "wiggler": "SM64_Asset_Model_Wiggler.png",
    "plano": "SM64_Artwork_Floor_Layout.jpg", "bobomb_rey": "SM64_Artwork_King_Bob-omb.png", "whomp_fort": "SM64_Artwork_Whomp's_Fortress.jpg",
    "mando": "Nintendo Sixty Four Controller.jpg", "martinet": "Charles Martinet portrait.jpg", "miyamoto": "Shigeru Miyamoto 2019.jpg",
    "kondo": "Koji Kondo.jpg", "koizumi": "Yoshiaki Koizumi.jpg", "panfleto": "SM64_Early_Pamphlet.jpg",
    "pinguino_beta": "SM64_Early_Penguin_Model.png", "yoshi_proto": "SM64_Prototype_Yoshi_Model.png",
}
WIKI = {             # slug: título de página de Wikipedia en inglés (imagen principal)
    "n64": "Nintendo 64", "snes": "Super Nintendo Entertainment System", "star_fox": "Star Fox (1993 video game)",
    "superfx": "Super FX", "sgi_indy": "SGI Indy", "tres_do": "3DO Interactive Multiplayer", "n3ds": "Nintendo 3DS",
    "nds": "Nintendo DS", "switch": "Nintendo Switch", "arale": "Dr. Slump", "smw": "Super Mario World",
    "max_planck": "Max Planck Institute for Human Development", "ign": "IGN", "cuthbert": "Dylan Cuthbert",
    "lincoln": "Howard Lincoln", "tezuka": "Takashi Tezuka", "shepard": "Shepard tone",
}
COMMONS = {}         # slug: nombre de archivo en Wikimedia Commons


def _json(url):
    return json.load(urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40))


def _bajar(url, ruta):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r, open(ruta, "wb") as f:
        f.write(r.read())


def mw_url(nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", format="json"))
    for p in _json("https://www.mariowiki.com/api.php?" + q)["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]
    return None


def wiki_url(titulo):
    q = urllib.parse.urlencode(dict(action="query", titles=titulo, prop="pageimages", piprop="thumbnail", pithumbsize=960,
                                    redirects=1, format="json"))
    for p in _json("https://en.wikipedia.org/w/api.php?" + q)["query"]["pages"].values():
        if "thumbnail" in p:
            return p["thumbnail"]["source"]
    return None


def commons_url(nombre):
    q = urllib.parse.urlencode(dict(action="query", titles="File:" + nombre, prop="imageinfo", iiprop="url", iiurlwidth=960,
                                    format="json"))
    for p in _json("https://commons.wikimedia.org/w/api.php?" + q)["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0].get("thumburl") or p["imageinfo"][0]["url"]
    return None


def main():
    os.makedirs(PEG, exist_ok=True)
    fuentes = []
    trabajos = [(s, os.path.splitext(n)[1].lower(), lambda n=n: mw_url(n)) for s, n in MARIOWIKI.items()]
    trabajos += [(s, ".jpg", lambda t=t: wiki_url(t)) for s, t in WIKI.items()]
    trabajos += [(s, os.path.splitext(n)[1].lower(), lambda n=n: commons_url(n)) for s, n in COMMONS.items()]
    for slug, ext, buscar in trabajos:
        if any(os.path.exists(os.path.join(PEG, slug + e)) for e in (".png", ".jpg", ".jpeg", ".gif")):
            continue
        try:
            url = buscar()
            if not url:
                print("SIN IMAGEN", slug)
                continue
            e = os.path.splitext(url.split("?")[0])[1].lower() or ext
            _bajar(url, os.path.join(PEG, slug + (".jpg" if e == ".jpeg" else e)))
            fuentes.append(f"{slug}\t{url}")
            print("ok", slug, flush=True)
            time.sleep(2.5)
        except Exception as e:                       # noqa: BLE001
            print("ERROR", slug, e)
    with open(os.path.join(PEG, "_fuentes.txt"), "a", encoding="utf-8") as f:
        f.write("\n".join(fuentes) + ("\n" if fuentes else ""))


if __name__ == "__main__":
    main()
