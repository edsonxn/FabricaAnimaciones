# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_godfrey_atrocidades (19-nov-2026; nombres en _investigacion/dossier.md):
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
PANT_NUEVAS = {"velo": "Stormveil Castle", "morne": "Castle Morne", "picos": "Mountaintops of the Giants",
               "leyndell": "Leyndell, Royal Capital", "leyndell_ceniza": "Leyndell, Ashen Capital",
               "subsuelo_wiki": "Subterranean Shunning-Grounds", "zamor": "Ruins of Zamor"}
PAGINAS = {   # slug: página de la wiki inglesa (pageimages = imagen del infobox; MIRAR en pegatinas_check)
    "hoarah_loux": "Hoarah Loux, Warrior", "serosh": "Serosh", "morgott": "Morgott, the Omen King", "godefroy": "Godefroy the Grafted",
    "gigante_fuego": "Fire Giant", "bastardo_leonino": "Leonine Misbegotten", "troll": "Troll", "melina": "Melina",
    "gurranq": "Gurranq, Beast Clergyman",
    "corona_senor": "Elden Lord Crown", "armadura_senor": "Elden Lord Armor", "icono_godfrey_t": "Godfrey Icon",
    "recuerdo_hoarah": "Remembrance of Hoarah Loux", "cinta_campeon": "Champion Headband", "espadon_injertado": "Grafted Blade Greatsword",
    "talisman_hacha": "Axe Talisman", "ancla_oxidada": "Rusted Anchor", "hacha_godfrey": "Axe of Godfrey",
    "parvulo": "Omen Bairn", "parvulo_realeza": "Regal Omen Bairn", "grillete_mohg": "Mohg's Shackle",
    "recuerdo_augurios": "Remembrance of the Omen King", "runa_mohg": "Mohg's Great Rune", "medallon_rugido": "Roar Medallion",
    "aplastagigantes": "Giant-Crusher", "escudo_rostro": "Visage Shield", "recuerdo_gigante": "Remembrance of the Fire Giant",
    "espada_trol": "Troll's Golden Sword", "martillo_garras": "Beastclaw Greathammer", "escudo_apuntado": "Beast Crest Heater Shield",
    "armadura_leonina": "Lion Greatbow", "armadura_radahn": "Radahn's Lion Armor", "talisman_dadiva": "Talisman of Lord's Bestowal",
    "aguja_miquella": "Miquella's Needle", "armadura_zamor": "Zamor Armor", "carne_excelsa": "Exalted Flesh",
    "atuendo_altiplanos": "Highland Attire", "cenizas_halcon_rey": "The Stormhawk King", "gran_hacha": "Greataxe",
    "ceniza_sacudida": "Ash of War: Hoarah Loux's Earthshaker",
}
PAGINAS_PANT = {}
COPIAS = {   # slug: (video, slug allí)
    "godfrey": ("er_godrick_atrocidades", "godfrey"), "godwyn": ("er_godrick_atrocidades", "godwyn"),
    "margit": ("er_godrick_atrocidades", "margit"), "marika": ("er_godrick_atrocidades", "marika"),
    "mohg": ("er_godrick_atrocidades", "mohg"), "godrick": ("er_godrick_atrocidades", "godrick"),
    "radahn": ("er_godrick_atrocidades", "radahn"), "icono_godfrey": ("er_godrick_atrocidades", "icono_godfrey"),
    "miquella": ("er_godrick_atrocidades", "miquella"), "gideon": ("er_godrick_atrocidades", "gideon"),
    "nepheli": ("er_godrick_atrocidades", "nepheli"), "malenia": ("er_godrick_atrocidades", "malenia"),
    "ranni": ("er_godrick_atrocidades", "ranni"), "messmer": ("er_godrick_atrocidades", "messmer"),
    "rennala": ("er_godrick_atrocidades", "rennala"),
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
