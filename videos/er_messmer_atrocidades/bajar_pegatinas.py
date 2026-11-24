# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_messmer_atrocidades (24-nov-2026; nombres en _investigacion/dossier.md):
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

ARCHIVOS = {}
PANTALLAS = {}
PAGINAS_NUEVAS = {}
PANT_NUEVAS = {"fortaleza_wiki": "Shadow Keep", "belurat_wiki": "Belurat, Tower Settlement", "rauh_wiki": "Ancient Ruins of Rauh",
               "llanura_wiki": "Gravesite Plain", "ruinas_calcinadas": "Scorched Ruins", "almacen_wiki": "Specimen Storehouse",
               "iglesia_brote": "Church of the Bud", "reino_sombras": "Realm of Shadow"}
PAGINAS = {   # slug: página de la wiki inglesa (pageimages = imagen del infobox; MIRAR en pegatinas_check)
    "messmer_jefe": "Messmer the Impaler", "messmer_serpiente": "Base Serpent Messmer", "anciana": "Hornsent Grandam",
    "cornamentado": "Hornsent", "leda": "Needle Knight Leda", "queelign": "Fire Knight Queelign", "leon": "Divine Beast Dancing Lion",
    "romina": "Romina, Saint of the Bud", "rellana": "Rellana, Twin Moon Knight", "gaius": "Commander Gaius",
    "caballero_fuego": "Fire Knight", "caballero_negro": "Black Knight", "soldado_messmer": "Messmer Soldier",
    "recuerdo_empalador": "Remembrance of the Impaler", "yesca": "Messmer's Kindling", "lanza_empalador": "Spear of the Impaler",
    "casco_messmer": "Messmer's Helm", "armadura_messmer": "Messmer's Armor", "casco_serpiente_alada": "Winged Serpent Helm",
    "escudo_serpiente": "Serpent Crest Shield", "insignia": "Crusade Insignia", "mayal": "Serpent Flail",
    "tornado_bestia": "Divine Beast Tornado", "recuerdo_leon": "Remembrance of the Dancing Lion", "cabeza_bestia": "Divine Beast Head",
    "potaje": "Scorpion Stew", "potaje_gourmet": "Gourmet Scorpion Stew", "tunica_cordon": "Braided Cord Robe",
    "cenizas_andreas": "Black Knight Commander Andreas", "cenizas_huw": "Black Knight Captain Huw",
    "cenizas_soldado": "Messmer Soldier Ashes", "armadura_soldado": "Messmer Soldier Armor", "casco_negro": "Black Knight Helm",
    "casco_fuego": "Fire Knight Helm", "armadura_fuego": "Fire Knight Armor", "capucha_salza": "Salza's Hood",
    "lluvia_fuego": "Rain of Fire", "hilde": "Fire Knight Hilde", "chispa_aromatica": "Firespark Perfume Bottle",
    "grasa_messmer": "Messmerfire Grease", "espadon_queelign": "Queelign's Greatsword", "iris_gracia": "Iris of Grace",
    "bendicion_marika": "Blessing of Marika", "runa_marika": "Marika's Rune", "hoja_brote": "Poleblade of the Bud",
    "recuerdo_brote": "Remembrance of the Saint of the Bud", "orbe_messmer": "Messmer's Orb", "botella_perfume": "Firespark Perfume Bottle",
}
PAGINAS_PANT = {}
COPIAS = {   # slug: (video, slug allí)
    **{s: ("er_rykard_atrocidades", s) for s in ("marika", "miquella", "messmer", "radagon", "godfrey", "rykard", "ranni", "radahn",
                                                  "malenia", "mohg", "morgott", "godrick", "melina", "rennala", "maliketh", "bayle",
                                                  "parches", "zampaheces", "gideon")},
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
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda t=t: url_pagina(t), False) for s, t in PAGINAS_PANT.items()]
    trabajos += [(s, os.path.join(PEG, s + ".png"), lambda t=t: url_pagina(t), True) for s, t in PAGINAS_NUEVAS.items()]
    trabajos += [(s, os.path.join(PAN, s + ".jpg"), lambda t=t: url_pagina(t), False) for s, t in PANT_NUEVAS.items()]
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
