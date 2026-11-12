# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_godrick_atrocidades (11-nov-2026; nombres en _investigacion/dossier.md § 4): eldenring.fandom.com (API imageinfo por archivo y
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

ARCHIVOS = {   # slug: archivo de la wiki (_investigacion/dossier.md § 4, comprobados por API el 11-nov-2026)
    "godrick_arte": "ER Godrick the Grafted.jpg", "godrick_f1": "ER Godrick Phase 1.png", "godrick_f2": "ER Godrick Phase 2.png",
    "godrick_modelo": "Godrick the Grafted model.png", "brazo_dragon": "ER Render Godrick Grafted Dragon.png",
    "dragon_empalado": "ER Render Impaled Dragon.png", "godefroy": "ER Godefroy the Grafted.png",
    "vastago": "ER Render Grafted Scion.png", "vastago2": "ER Render Grafted Scion01.png",
    "hacha": "ER Icon weapon Axe of Godrick.png", "dragon_arma": "ER Icon weapon Grafted Dragon.png",
    "runa_godrick": "ER Icon Key Item Great Rune Godrick's.png", "recuerdo_injertado": "ER Icon Remembrance of the Grafted.png",
    "recuerdo_crisalidas": "ER Icon Key Item Chrysalids' Memento.png", "velo_imitador": "ER Icon Tool Mimic's Veil.png",
    "icono_godfrey": "ER Icon Talisman Godfrey Icon.png", "margit": "ER Margit Boss.png", "nepheli": "ER NPC Closeup Nepheli.png",
    "kenneth": "ER NPC Closeup Kenneth.png", "gostoc": "ER NPC Closeup Gostoc.png", "edgar": "ER NPC Closeup Edgar.png",
    "irina": "ER NPC Closeup Irina.png", "roderika": "ER NPC Closeup Roderika.png", "varre": "ER NPC Closeup Varre.png",
    "rogier": "ER NPC Closeup Rogier.png", "enia": "ER NPC Closeup Enia.png", "gideon": "ER NPC Closeup Gideon.png",
    "godfrey": "ER Godfrey, First Elden Lord.png", "leonino": "ER Boss Leonine Misbegotten (1.1).png",
    "latigo": "ER Icon weapon Whip.png", "espadon_injertado": "ER Icon weapon Grafted Blade Greatsword.png",
    "halcon": "ER Icon Ash Warhawk Ashes.png", "escudo_cuero": "ER Icon shield Marred Leather Shield.png",
    "espada_ornamental": "ER Icon weapon Ornamental Straight Sword.png", "escudo_bestia": "ER Icon shield Golden Beast Crest Shield.png",
    "cenizas_soldado": "ER Icon Ash Godrick Soldier Ashes.png", "kristoff": "ER Icon Ash Ancient Dragon Knight Kristoff Ashes.png",
    "caballero_godrick": "ER Godrick Knight w Partisan.png", "comandante_haight": "ER Blood Obsessed Godrick Knight.png",
    "kenneth_cara": "ER Character Face Kenneth Haight, Limgrave Heir.png", "irina_cara": "ER Character Face Irina of Morne.png",
}
PANTALLAS = {   # imágenes grandes para pant()
    "velo_carga": "ER loading screen stormveil castle.png", "morne": "Eldenringcastlemorne.jpeg",
    "monumento": "20230222174027_1.jpg", "dragon_estatua": "ER Godrick's Dragon.png", "vastago_foto": "ER Grafted Scion.png",
    "edgar_irina": "ER Edgar Mourning Irinia.jpg", "edgar_vengador": "ER Edgar the Revenger.png",
    "gostoc_foto": "Elden ring gostoc screenshot.jpg", "godrick_concepto": "Godrick the Grafted Concept Art.jpg",
}
PAGINAS = {}
COPIAS = {   # slug: (video, slug allí) — misma imagen real ya bajada en videos anteriores
    "malenia": ("er_malenia_atrocidades", "malenia_icono"), "radahn": ("er_ranni_atrocidades", "radahn_estelar"),
    "mohg": ("er_miquella_atrocidades", "mohg"), "miquella": ("er_miquella_atrocidades", "miquella"),
    "ranni": ("er_ranni_atrocidades", "ranni"), "godwyn": ("er_melina_atrocidades", "godwyn"), "godrick": ("er_malenia_atrocidades", "godrick"),
    "marika": ("er_malenia_atrocidades", "marika"), "exaltacion": ("er_mohg_atrocidades", "exaltacion"),
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
