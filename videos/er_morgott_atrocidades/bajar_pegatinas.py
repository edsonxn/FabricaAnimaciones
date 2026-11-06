# -*- coding: utf-8 -*-
"""Pegatinas y pantallas REALES de er_morgott_atrocidades (5-nov-2026; archivos comprobados en investigacion.md §4): eldenring.fandom.com (API imageinfo por archivo y
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

ARCHIVOS = {   # slug: archivo de la wiki (investigacion.md §6, comprobados el 5-nov-2026)
    "morgott_icono": "Morgott Icon.png", "margit_render": "Margit, the Fell Omen model.png", "margit_cara": "ER Boss Margit (Stormveil) Closeup.png",
    "runa_morgott": "ER Icon Key Item Great Rune Morgott's.png", "runa_mohg": "ER Icon Key Item Great Rune Mohg's.png",
    "recuerdo_morgott": "ER Icon Remembrance of the Omen King.png", "espada_maldita": "ER Icon weapon Morgott's Cursed Sword.png",
    "grillete_margit": "ER Icon Tool margit's shackle.png", "grillete_mohg": "ER Icon Tool Mohg's Shackle.png",
    "sigilo_grillete": "ER Spell Sigil Margit & Mogh's Shackle (Color).png",
    "parvulo_realeza": "ER Icon Tool Regal Omen Bairn.png", "parvulo": "ER Icon Tool Omen Bairn.png", "parvulo_cornudo": "ER Icon Tool Horned Bairn.png",
    "capa_augurio": "ER Icon Armor Fell Omen Cloak.png", "casco_noche": "ER Icon Armor Night's Cavalry Helm.png",
    "armadura_noche": "ER Icon Armor Night's Cavalry Armor.png", "guanteletes_noche": "ER Icon Armor Night's Cavalry Gauntlets.png",
    "machete_asesino": "ER Icon weapon Great Omenkiller Cleaver.png", "mascara_sonriente": "ER Icon Armor Omensmirk Mask.png",
    "tunica_asesino": "ER Icon Armor Omenkiller Robe.png", "rollo": "ER Icon Ash Omenkiller Rollo.png", "machete_augurio": "ER Icon weapon Omen Cleaver.png",
    "plebeyo": "ER Commoner.png", "augurio_machete": "ER Omen w Omen Cleaver.jpg", "asesino_augurios": "ER Enemy Omenkiller.png",
    "gemelo_caido": "ER Fell Twin w Cleaver.jpg", "mohg_icono": "Mohg Icon.png", "parches": "ER NPC Closeup Patches.png",
    "gideon_cara": "ER NPC Closeup Gideon.png", "enia": "ER NPC Closeup Enia.png", "kenneth": "ER NPC Closeup Kenneth.png",
    "glaive_noche": "Night's Cavalry Glaive.png", "pluma_crisol": "ER Icon Talisman Crucible Teather Talisman.png",
}
PANTALLAS = {
    "morgott_jefe": "ER Morgott Boss.png", "morgott_render": "ER Render Morgott.png", "morgott_render1": "ER Render Morgott01.png",
    "morgott_boca": "ER Render Morgott02.png", "margit_jefe": "ER Margit Boss.png", "margit_fell": "ER margit the fell.png",
    "margit_radahn": "Margit the Fell Omen vs. Starscourge Radahn.jpg", "morgott_radahn": "Morgott the Omen King fighting Radahn.jpg",
    "trono_trailer": "ER trailer throne.jpg", "godfrey_llora": "Eldenringgodfrey1.jpg", "godfrey_llora2": "Eldenringgodfrey2.jpg",
    "godfrey_serosh": "ER Godfrey and Serosh Mourn.png", "monumento2": "Second_Defense_Leyndell_Sword_Monument.jpg",
    "gracia_margit": "ER Site of Grace Margit, the Fell Omen.png", "gracia_tunel": "ER Site of Grace Castleward Tunnel.png",
    "puerta_tormentosa": "Eldenringstormgate.jpeg", "velo_carga": "ER loading screen stormveil castle.png", "agualobrega": "Eldenringmurkwaterc.jpeg",
    "afueras": "ER Capital Outskirts.png", "gracia_muro": "ER Site of Grace Outer Wall Battleground.png", "leyndell": "ER Leyndell, Royal Capital.png",
    "gracia_iglesia": "ER Site of Grace Lower Capital Church.png", "gracia_alcoba": "ER Site of Grace Queen's Bedchamber.png",
    "gracia_trono": "ER Site of Grace Elden Throne.png", "espinas": "ER Erdtree Thorns.png", "muro_espinas": "ER Erdtree Wall of Thorns.png",
    "subsuelo": "ER Subterranean Shunning-Grounds.png", "gracia_camino_sub": "ER Site of Grace Underground Roadside.png",
    "gracia_abismo": "ER Site of Grace Forsaken Depths.png", "gracia_catedral": "ER Site of Grace Cathedral of the Forsaken.png",
    "gracia_llama": "ER Site of Grace Frenzied Flame Proscription.png", "perfumeria": "ER Perfumer's Ruins.png",
    "ceniza": "ER Leyndell, Ashen Capital.png", "parvulo_omen": "ER Omen Bairn Omen.png", "campamento_augurios": "Omen Camp Altus1.jpg",
    "mohg_jefe": "ER Mohg, the Omen.png", "godfrey_jefe": "ER Godfrey, First Elden Lord.png", "godrick_jefe": "ER Godrick the Grafted.jpg",
    "rykard": "Eldenringrykardcutscene1.jpg", "godwyn": "Elden ring godwyn.png", "parches_grande": "ER NPC Patches (Murkwater Cave) (1.1).png",
    "omenkiller_arte": "Omenkiller concept art.jpg",
}
PAGINAS = {}
COPIAS = {   # slug: (video, slug allí) — misma imagen real ya bajada en videos anteriores
    "radahn": ("er_ranni_atrocidades", "radahn_estelar"), "godfrey": ("er_malenia_atrocidades", "godfrey"),
    "godrick": ("er_malenia_atrocidades", "godrick"), "marika": ("er_malenia_atrocidades", "marika"),
    "radagon": ("er_malenia_atrocidades", "radagon"), "ranni": ("er_ranni_atrocidades", "ranni"), "malenia": ("er_malenia_atrocidades", "malenia_icono"),
    "miquella": ("er_miquella_atrocidades", "miquella"), "mohg": ("er_miquella_atrocidades", "mohg"), "gideon": ("er_malenia_atrocidades", "gideon"),
    "blaidd": ("er_ranni_atrocidades", "blaidd"), "rennala": ("er_ranni_atrocidades", "rennala"), "melina": ("er_melina_atrocidades", "melina"),
    "godwyn_peg": ("er_melina_atrocidades", "godwyn"),
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
