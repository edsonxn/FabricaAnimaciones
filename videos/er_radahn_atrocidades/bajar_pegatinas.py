# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_radahn_atrocidades (28-oct-2026; archivos comprobados en investigacion.md §4): eldenring.fandom.com (API imageinfo por archivo y
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

ARCHIVOS = {   # slug: archivo de la wiki
    "radahn_render": "Starscourge Radahn model.png", "radahn_retrato": "Starscourge Radahn portrait.jpg",
    "radahn_general": "ER General Radahn.jpg", "radahn_concepto": "ER Concept Art Radahn1.jpg",
    "leonard": "ER Leonard.png", "gato": "Talisman longtail cat talisman.png",
    "recuerdo_azote": "ER Icon Remembrance of the Starscourge.png", "recuerdo_dios2": "ER Icon Remembrance of a God and a Lord.png",
    "runa_radahn2": "ER Icon Key Item Great Rune Radahn's.png", "espadon_azote": "ER Icon weapon Starscourge Greatsword.png",
    "arco_leon": "ER Icon weapon Lion Greatbow.png", "lanza_radahn": "ER Icon ammo Radahn's Spear.png",
    "espadon_radahn": "ER Icon Weapon Greatsword of Radahn.png", "espadon_luz": "ER Icon Weapon Greatsword of Radahn (Light).png",
    "espadon_senor": "ER Icon Weapon Greatsword of Radahn (Lord).png", "yelmo_melena": "ER Icon Armor Radahn's Redmane Helm.png",
    "armadura_leon": "ER Icon Armor Radahn's Lion Armor.png", "armadura_joven": "ER Icon Armor Young Lion's Armor.png",
    "pozo_gravedad": "ER Icon Spell Gravity Well.png", "estrellas_colapso": "ER Icon Spell Collapsing Stars.png",
    "hojas_piedra": "ER Icon Spell Blades of Stone.png", "reliquia_azote": "ER Icon Talisman Starscourge Heirloom.png",
    "capucha_jerren": "ER Icon Armor Eccentric's Hood.png", "armadura_jerren": "ER Icon Armor Eccentric's Armor.png",
    "armadura_melena": "ER Icon Armor Redmane Knight Armor.png", "sobreveste_melena": "ER Icon Armor Redmane Surcoat.png",
    "cenizas_soldado": "ER Icon Ash Radahn Soldier Ashes.png", "ogha": "ER Icon Ash Redmane Knight Ogha.png",
    "armadura_freyja": "ER Icon Armor Freyja's Armor.png", "pergamino2": "ER Icon Key Item Secret Rite Scroll.png",
    "diadema_luz": "ER Icon Armor Circlet of Light.png", "runa_miquella2": "ER Icon Tool Miquella's Great Rune.png",
    "aeonia_escarlata": "ER Icon Spell Scarlet Aeonia.png", "recuerdo_gaius": "MENU Knowledge 00732.png",
    "jerren_npc": "ER NPC Closeup Jerren.png", "blaidd_cara": "ER NPC Closeup Blaidd.png", "iji_cara": "ER NPC Closeup Iji.png",
    "sellen": "ER NPC Closeup Sellen.png", "ranni_cuadro": "ER Ranni (square portrait).png", "freyja_render": "ER Render Redmane Freyja.png",
    "ansbach_npc": "ER NPC Ansbach.png", "miquella_perfil": "Miquella Appearance Profile.jpg",
}
PANTALLAS = {
    "radahn_dunas": "ER Starscourge Radahn.png", "radahn_festival": "Starscourge Radahn Cutscene.jpg",
    "radahn_arte": "Starscourge Radahn concept art.jpg", "consorte": "Promised Consort Boss.jpg",
    "consorte_miquella": "Consort of Miquella Boss.jpg", "consorte_cara": "Promised Consort Radahn CloseUp.jpg",
    "consorte_puerta": "Promised Consort Radahn Gate.jpg", "cuernos": "Radahn Omen Horns.jpg",
    "consorte_arte": "Consort Radahn Concept.jpg", "miquella_sobre": "Miquella Appearance.jpg",
    "aeonia_trailer": "Malenia vs Radahn (story trailer).jpg", "aeonia_preparan": "Malenia and Radahn preparing to battle each other.jpg",
    "aeonia_duelo": "Malenia the Severed vs General Radahn.jpg", "aeonia_arte": "ER Concept Art Battle of Aeonia.png",
    "aeonia_t01": "ER Promo Trailer Battle of Aeonia01.png", "aeonia_t09": "ER Promo Trailer Battle of Aeonia09.png",
    "aeonia_t16": "ER Promo Trailer Battle of Aeonia16.png", "aeonia_t23": "ER Promo Trailer Battle of Aeonia23.png",
    "morgott_radahn": "Morgott the Omen King fighting Radahn.jpg", "leonard_grande": "ER Leonard.png",
    "castillo": "ER Redmane Castle.png", "dunas": "ER Ancient Ruins Wailing Dunes.png", "gracia_radahn": "ER Starscourge Radahn Grace.png",
    "fuerte_gael": "ER Fort Gael.png", "pantano": "ER Swamp of Aeonia.png", "aeonia_interior": "ER Site of Grace Inner Aeonia.png",
    "calle_sabios": "ER Street of Sages Ruins.png", "gran_puente": "ER Smouldering Wall Impassable Greatbridge 2.png",
    "catacumbas": "ER War-Dead Catacombs.png", "sellia": "ER Sellia, Town of Sorcery.png", "enir_ilim": "ER location Enir-Ilim.png",
    "puerta_divinidad": "Gate of Divinity Shadow of the Erdtree.png", "caelid_panorama": "ER Caelid Gael Panorama.png",
    "gaius": "ER Boss Commander Gaius.png", "mohg_jefe": "ER Mohg Phase 1.png", "rennala_reina": "Queen Rennala.webp",
    "radagon_jefe": "ER Radagon Boss.png", "malenia_f2": "ER Malenia Phase 2.png",
}
PAGINAS = {   # slug: página (su imagen principal)
    "nokron": "Nokron, Eternal City", "crater": "Starfall Crater", "torre_ranni": "Ranni's Rise", "fortaleza_sombria": "Shadow Keep",
    "ruinas_bruja": "Witchbane Ruins", "palacio_mohgwyn": "Mohgwyn Palace", "almacen": "Specimen Storehouse",
    "godfrey_jefe": "Godfrey, First Elden Lord", "leda": "Needle Knight Leda", "gaius_peg": "Commander Gaius",
    "velo_tormentoso": "Stormveil Castle",
}
COPIAS = {   # slug: (video, slug allí)
    "radahn": ("er_ranni_atrocidades", "radahn_estelar"), "radahn_icono": ("er_malenia_atrocidades", "radahn"),
    "runa_radahn": ("er_malenia_atrocidades", "runa_radahn"), "jerren": ("er_malenia_atrocidades", "jerren"),
    "gideon": ("er_malenia_atrocidades", "gideon"), "millicent": ("er_malenia_atrocidades", "millicent"),
    "finlay": ("er_malenia_atrocidades", "cenizas_finlay"), "cleanrot": ("er_malenia_atrocidades", "cleanrot"),
    "malenia": ("er_malenia_atrocidades", "malenia_icono"), "malenia_jefa": ("er_malenia_atrocidades", "malenia_jefa"),
    "aeonia": ("er_malenia_atrocidades", "aeonia"), "godfrey": ("er_malenia_atrocidades", "godfrey"),
    "godrick": ("er_malenia_atrocidades", "godrick"), "marika": ("er_malenia_atrocidades", "marika"),
    "radagon": ("er_malenia_atrocidades", "radagon"), "ranni": ("er_ranni_atrocidades", "ranni"),
    "blaidd": ("er_ranni_atrocidades", "blaidd"), "iji": ("er_ranni_atrocidades", "iji"), "rennala": ("er_ranni_atrocidades", "rennala"),
    "miquella": ("er_miquella_atrocidades", "miquella"), "miquella_nino": ("er_miquella_atrocidades", "miquella_nino"),
    "mohg": ("er_miquella_atrocidades", "mohg"), "ansbach": ("er_miquella_atrocidades", "ansbach"),
    "freyja": ("er_miquella_atrocidades", "freyja"), "pergamino": ("er_miquella_atrocidades", "pergamino"),
    "recuerdo_dios": ("er_miquella_atrocidades", "recuerdo_dios"), "yelmo_leon": ("er_miquella_atrocidades", "yelmo_leon"),
    "luz_miquella": ("er_miquella_atrocidades", "luz_miquella"), "runa_miquella": ("er_miquella_atrocidades", "runa_miquella"),
    "messmer": ("er_miquella_atrocidades", "messmer"), "leda_peg": ("er_miquella_atrocidades", "leda"),
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
