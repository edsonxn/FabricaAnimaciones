# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_maliketh_atrocidades (27-nov-2026; nombres en _investigacion/dossier.md):
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
PANT_NUEVAS = {"farum_wiki": "Crumbling Farum Azula", "santuario_bestial": "Bestial Sanctum", "nokron_wiki": "Nokron, Eternal City",
               "nokstella_wiki": "Nokstella, Eternal City", "catacumbas_cuchillo": "Black Knife Catacombs",
               "leyndell_wiki": "Leyndell, Royal Capital", "caelid_wiki": "Caelid", "mesa_redonda": "Roundtable Hold"}
PAGINAS = {
    "maliketh_jefe": "Maliketh, the Black Blade", "clerigo": "Beast Clergyman", "gurranq": "Gurranq, Beast Clergyman",
    "recuerdo_espada_negra": "Remembrance of the Black Blade", "espada_maliketh": "Maliketh's Black Blade",
    "hoja_negra": "Black Blade (Incantation)", "cuchillo_negro": "Black Knife", "asesina_cuchillo": "Black Knife Assassin",
    "tiche": "Black Knife Tiche", "armadura_cuchillo": "Black Knife Armor", "capucha_cuchillo": "Black Knife Hood",
    "raiz_muerte": "Deathroot", "ojo_bestia": "Beast Eye", "sello_garra": "Clawmark Seal", "garra_bestia": "Beast Claw",
    "garra_gurranq": "Gurranq's Beast Claw", "vitalidad_bestial": "Bestial Vitality", "honda_bestial": "Bestial Sling",
    "piedra_gurranq": "Stone of Gurranq", "placidusax": "Dragonlord Placidusax", "pielesdivinas": "Godskin Apostle",
    "godwyn": "Godwyn the Golden", "fia": "Fia", "d_cazador": "D, Hunter of the Dead", "pajaro_muerte": "Death Rite Bird",
    "ave_muerte": "Deathbird", "lansseax": "Ancient Dragon Lansseax", "garra_maliketh": "Maliketh's Black Blade",
    "armadura_maliketh": "Maliketh's Armor", "casco_maliketh": "Maliketh's Helm", "rito_muerte": "Rite of Death",
    "runa_muerte": "Rune of Death", "llama_negra": "Black Flame", "cuchillas_negras": "Black Knives",
    "marca_muerte": "Mark of the Black Blade", "pigmeo": "Fingercreeper", "mano_cuchilla": "Godslayer's Greatsword",
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
