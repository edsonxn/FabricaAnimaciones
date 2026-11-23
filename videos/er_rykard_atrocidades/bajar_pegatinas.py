# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_rykard_atrocidades (22-nov-2026; nombres en _investigacion/dossier.md):
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
PANT_NUEVAS = {"mansion_wiki": "Volcano Manor", "gelmir": "Mt. Gelmir", "raya_lucaria": "Academy of Raya Lucaria",
               "eiglay": "Temple of Eiglay", "camara_wiki": "Subterranean Inquisition Chamber", "farum_wiki": "Crumbling Farum Azula"}
PAGINAS = {   # slug: página de la wiki inglesa (pageimages = imagen del infobox; MIRAR en pegatinas_check)
    "bernahl": "Knight Bernahl", "parches": "Patches", "ghiza": "Inquisitor Ghiza", "virgen_raptora": "Abductor Virgin",
    "hombre_serpiente": "Man-Serpent", "noble_sacrodermo": "Godskin Noble", "rogier": "Sorcerer Rogier",
    "rykard_jefe": "Rykard, Lord of Blasphemy", "serpiente_jefe": "God-Devouring Serpent",
    "candelabro": "Inquisitor's Girandole", "rueda_ghiza": "Ghiza's Wheel", "mascara_ensangrentada": "Bloodsoaked Mask",
    "atuendo_oficial": "Official's Attire", "casco_gelmir": "Gelmir Knight Helm", "armadura_gelmir": "Gelmir Knight Armor",
    "cazador_serpientes": "Serpent-Hunter", "hoja_blasfema": "Blasphemous Blade", "sobretodo_ocular": "Eye Surcoat",
    "cenizas_hombre_serpiente": "Man-Serpent Ashes", "espada_dios_serpiente": "Serpent-God's Curved Sword",
    "amnios": "Serpent's Amnion", "carta_zorayas": "Zorayas's Letter", "ira_gelmir": "Gelmir's Fury",
    "garra_blasfema": "Blasphemous Claw", "cetro_devorador": "Devourer's Scepter", "dedo_recusante": "Recusant Finger",
    "gideon_npc": "Sir Gideon Ofnir, the All-Knowing", "tanith_npc": "Tanith, Volcano Manor Proprietress",
}
PAGINAS_PANT = {}
COPIAS = {   # slug: (video, slug allí)
    **{s: ("er_sinluz_atrocidades", s) for s in ("rykard", "tanith", "rya", "serpiente", "recuerdo_blasfemo", "runa_rykard",
                                                  "caballero_tanith", "gideon", "ranni", "radahn", "rennala", "maliketh", "godwyn",
                                                  "disparo_magma", "farum_azula", "mesa_redonda", "miquella", "messmer", "marika",
                                                  "zampaheces", "melina", "radagon")},
    "godfrey": ("er_godfrey_atrocidades", "godfrey"), "corona_senor": ("er_godfrey_atrocidades", "corona_senor"),
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
