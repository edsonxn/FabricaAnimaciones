# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_mohg_atrocidades (10-nov-2026; nombres en _investigacion/pegatinas_wiki.txt): eldenring.fandom.com (API imageinfo por archivo y
pageimages por página) a pegatinas/<slug>.png (≤ 700 px) y pantallas/<slug>.jpg (≥ 1000 px); fuentes en */_fuentes.txt.
Las que ya bajaron Malenia/Ranni/Miquella se copian de sus carpetas (misma imagen real, no es una escena).
    python bajar_pegatinas.py
"""
import io
import json
import os
import shutil
import urllib.parse
import urllib.request

from PIL import Image

AQUI = os.path.dirname(os.path.abspath(__file__))
PEG = os.path.join(AQUI, "pegatinas")
PAN = os.path.join(AQUI, "pantallas")
VID = os.path.dirname(AQUI)
UA = {"User-Agent": "Mozilla/5.0 FabricaAnimaciones (pegatinas)"}
API = "https://eldenring.fandom.com/api.php?"

ARCHIVOS = {   # slug: archivo de la wiki (_investigacion/pegatinas_wiki.txt, búsqueda del 10-nov-2026)
    "varre": "ER NPC Closeup Varre.png", "varre_cara": "ER Character Face White Mask Varre.png", "varre_ramo": "ER Icon weapon Varre's Bouquet.png",
    "dedo_infestado": "ER Icon Tool Festering Bloody Finger.png", "icono_dedos": "ER Custom Icon Bloody Fingers.png",
    "icono_mohgwyn": "ER Custom Icon Mohgwyn.png", "icono_pureblood": "ER Custom Icon Pureblood Knights.png",
    "pano_limpio": "ER Icon Key Item Lord of Blood's Favor (Clean).png", "pano_rojo": "ER Icon Key Item Lord of Blood's Favor (Soaked).png",
    "medalla": "ER Icon Key Item Pureblood Knight's Medal.png", "rios": "ER Icon weapon Rivers of Blood.png",
    "okina": "ER Character Face Okina.png", "mascara_okina": "ER Icon Armor Okina Mask.png", "yura": "ER NPC Closeup Yura.png",
    "nerijus": "ER Character Face Bloody Finger Nerijus.png", "eleonora": "ER Character Face Eleonora, Violet Bloody Finger.png",
    "guja_eleonora": "ER Icon weapon Eleonora's Poleblade.png", "magnus": "ER Magnus Beast Claw.png",
    "mascara_blanca": "ER Icon Armor White Mask.png", "mascara_sin_nombre": "ER Character Face Nameless White Mask.png",
    "tunica_cirujano": "ER Icon Armor War Surgeon Gown.png", "albinaurico_rojo": "ER Enemy Blood Albinauric w Great Curved Club.png",
    "albinaurico": "ER Enemy Albinauric w Club.png", "noble": "ER Enemy Sanguine Noble.png", "tunica_noble": "ER Icon Armor Sanguine Noble Robe.png",
    "helice": "ER Icon weapon Bloody Helice.png", "blood_tax": "ER Icon ash of war Blood Tax.png", "esgar": "ER Esgar, Priests of Blood.png",
    "moscas": "ER Icon Spell Swarm of Flies.png", "excremento": "ER Icon material blood-tainted excrement.png",
    "recuerdo_mohg": "ER Icon Remembrance of the Blood Lord.png", "exaltacion": "ER Icon Talisman Lord of Blood's Exultation.png",
    "bloodboon": "ER Icon Spell Bloodboon.png", "lanza": "ER Icon weapon Mohgwyn's Sacred Spear.png", "lagrima": "ER Icon tear Purifying Crystal.png",
    "garras": "ER Icon Spell Bloodflame Talons.png", "hoja_hemofuego": "ER Icon Spell Bloodflame Blade.png",
    "grillete_mohg": "ER Icon Tool Mohg's Shackle.png", "runa_mohg": "ER Icon Key Item Great Rune Mohg's.png",
    "dios_exterior": "ER Icon Talisman Outer God Heirloom.png", "irina": "ER NPC Closeup Irina.png", "carta_irina": "ER Icon Key Item Irina's Letter.png",
    "hyetta": "ER NPC Closeup Hyetta.png", "doncella_vyke": "ER Character Face Vyke's Finger Maiden.png", "vyke": "ER Character Face Festering Fingerprint Vyke.png",
    "dos_dedos": "ER Render Two Fingers.png", "ansbach": "ER NPC Ansbach.png", "gideon_cara": "ER NPC Closeup Gideon.png",
    "mohg_icono": "Mohg Icon.png", "mohg_modelo": "Mohg, Lord of Blood model.png", "torrentera": "ER RE Torrent.png",
}
PANTALLAS = {
    "mohg_miquella": "Mohg carrying Miquella .webp", "capullo_arte": "ER Concept Art Cocoon of the Empyrean.png",
    "estatua": "ER Statue Ancient Dynasty Mohgwyn.png", "palacio": "ER Mohgwyn Palace.png", "varre_invasion": "ER Varre invasion.png",
    "rykard": "ER Rykard, Lord of Blasphemy.png", "maliketh": "ER Maliketh, the Black Blade.png", "albinaurico_rojo2": "ER Red Albinauric w Curved Great Club.jpg",
    "noble_ruinas": "ER Sanguine Noble Writheblood Ruins.png", "nerijus_full": "ER Nerijus Full.png", "okina_rios": "Okina Rivers of Blood.png",
}
PAGINAS = {}
COPIAS = {   # slug: (video, slug allí) — misma imagen real ya bajada en videos anteriores
    "mohg": ("er_miquella_atrocidades", "mohg"), "miquella": ("er_miquella_atrocidades", "miquella"),
    "malenia": ("er_malenia_atrocidades", "malenia_icono"), "radahn": ("er_ranni_atrocidades", "radahn_estelar"),
    "morgott_icono": ("er_morgott_atrocidades", "morgott_icono"), "marika": ("er_malenia_atrocidades", "marika"),
    "radagon": ("er_malenia_atrocidades", "radagon"), "ranni": ("er_ranni_atrocidades", "ranni"), "melina": ("er_melina_atrocidades", "melina"),
    "godwyn": ("er_melina_atrocidades", "godwyn"), "godrick": ("er_malenia_atrocidades", "godrick"),
}


def _json(q):
    return json.load(urllib.request.urlopen(urllib.request.Request(API + urllib.parse.urlencode(q), headers=UA), timeout=40))


def url_archivo(n):
    for p in _json(dict(action="query", titles="File:" + n, prop="imageinfo", iiprop="url", format="json"))["query"]["pages"].values():
        if "imageinfo" in p:
            return p["imageinfo"][0]["url"]


def url_pagina(t):
    for p in _json(dict(action="query", titles=t, prop="pageimages", piprop="original", redirects=1, format="json"))["query"]["pages"].values():
        if "original" in p:
            return p["original"]["source"]


def guardar(url, ruta, peg):
    data = urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
    im = Image.open(io.BytesIO(data))   # vienen en WebP aunque digan .png: reabrir y guardar con PIL
    if peg:
        im = im.convert("RGBA")
        im.thumbnail((700, 700), Image.LANCZOS)
        im.save(ruta)
    else:
        im = im.convert("RGB")
        if im.width > 2400:
            im = im.resize((2400, round(im.height * 2400 / im.width)), Image.LANCZOS)
        im.save(ruta, quality=92)
    return im.size


def main():
    os.makedirs(PEG, exist_ok=True)
    os.makedirs(PAN, exist_ok=True)
    fuentes = {PEG: [], PAN: []}
    for s, (v, o) in COPIAS.items():
        src = os.path.join(VID, v, "pegatinas", o + ".png")
        dst = os.path.join(PEG, s + ".png")
        if os.path.exists(src) and not os.path.exists(dst):
            shutil.copy2(src, dst)
            fuentes[PEG].append(f"{s}\tcopia de videos/{v}/pegatinas/{o}.png")
    trabajos = [(s, os.path.join(PEG, s + ".png"), lambda n=n: url_archivo(n), True) for s, n in ARCHIVOS.items()]
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda n=n: url_archivo(n), False) for s, n in PANTALLAS.items()]
    trabajos += [(s, os.path.join(PEG, s + ".png"), lambda t=t: url_pagina(t), True) for s, t in PAGINAS.items()]
    for slug, ruta, buscar, peg in trabajos:
        if os.path.exists(ruta):
            continue
        try:
            url = buscar()
            if not url:
                print("SIN IMAGEN", slug)
                continue
            tam = guardar(url, ruta, peg)
            fuentes[PEG if peg else PAN].append(f"{slug}\t{url}")
            print("ok", slug, tam)
        except Exception as e:                       # noqa: BLE001
            print("ERROR", slug, e)
    for d, fs in fuentes.items():
        with open(os.path.join(d, "_fuentes.txt"), "a", encoding="utf-8") as f:
            f.write("\n".join(fs) + ("\n" if fs else ""))


if __name__ == "__main__":
    main()
