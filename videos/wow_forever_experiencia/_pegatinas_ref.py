# -*- coding: utf-8 -*-
"""Pegatinas de «Los 20 ERRORES del 30 al 60 en WoW Forever» (10-nov-2026; copiado de wow_secretos_primeros_niveles).
- Íconos de objetos: API de tooltips de Wowhead FOREVER (id comprobado con su buscador: nombre exacto del objeto).
- PNJ, criaturas y lugares de Classic: imagen principal de su página de Wowpedia (identidad = título exacto de la página).
- PNJ nuevos de Forever (sin página en la wiki): cuadro del video de guía cuyo título nombra a ese PNJ (_capturas.py).
python _pegatinas.py → pegatinas/<slug>.png + pantallas/<slug>.jpg + previews/_hoja_peg.jpg (MIRARLA)"""
import io
import json
import os
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
for c in (PEG, PAN, os.path.join(D, "previews")):
    os.makedirs(c, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}

ITEMS = {  # slug: id de objeto (Wowhead Forever; si falla, Classic). Nombre = el que dice la voz
    "o_pagina": 2725, "o_hogar": 6948, "o_tuberculo": 11951, "o_aliento": 11952, "o_unguento": 11516, "o_manoplas": 14551,
    "o_pocion": 13446, "o_panomagico": 4338, "o_seda": 4306, "o_mitril": 3858, "o_cuero": 4304, "o_devastador": 7717,
    "o_sombrero": 7720, "o_llave_escarlata": 7146, "o_llave_sombra": 11000, "o_llave_creciente": 18249, "o_marra": 9240,
    "o_zanahoria": 11122, "o_espada_linken": 11902, "o_bumeran": 11905, "o_pluma": 21377, "o_cuentas": 21383,
    "o_comision": 12846, "o_piedra_plaga": 12840, "o_muestra": 12844, "o_llave_esqueleto": 13704, "o_torio": 12359,
    "o_amuleto": 16309, "o_lacre": 12219, "o_fragmento": 13705,
}
WIKI = {  # slug: título exacto de Wowpedia (comprobar identidad en la hoja)
    "barnil": "Barnil Stonepot", "nesingwary": "Hemet Nesingwary", "expedicion": "Nesingwary's Expedition", "bahia": "Booty Bay",
    "angel": "Spirit Healer", "gadgetzan": "Gadgetzan", "vista_eterna": "Everlook", "capilla": "Light's Hope Chapel",
    "gromgol": "Grom'gol Base Camp", "frondavil": "Felwood", "santuario": "Emerald Sanctuary", "gregory": "Doctor Gregory Victor",
    "gustaf": "Doctor Gustaf VanHowzen", "theramore": "Theramore Isle", "sentencia": "Hammerfall", "herod": "Herod",
    "melenablanca": "Sally Whitemane", "monasterio": "Scarlet Monastery", "doan": "Arcanist Doan", "franclorn": "Franclorn Forgewright",
    "brd": "Blackrock Depths", "gahzrilla": "Gahz'rilla", "zulfarrak": "Zul'Farrak", "jinthaalor": "Jintha'Alor", "linken": "Linken",
    "jdcollie": "J.D. Collie", "ungoro": "Un'Goro Crater", "timbermaw": "Timbermaw Hold", "grazle": "Grazle", "nafien": "Nafien",
    "zverenhoff": "Nicholas Zverenhoff", "stratholme": "Stratholme", "scholomance": "Scholomance", "templo": "Temple of Atal'Hakkar",
    "xylem": "Archmage Xylem", "ogtinc": "Ogtinc", "diblis": "Impsy", "heroe": "Fallen Hero of the Horde", "montana": "Blackrock Mountain",
    "krinkle": "Krinkle Goodsteel", "araj": "Araj the Summoner", "andorhal": "Andorhal", "caer_darrow": "Caer Darrow",
    "riverglades": "Riverglades", "onyxia": "Onyxia", "guarida": "Onyxia's Lair", "dientegore": "Warlord Goretooth",
    "windsor": "Reginald Windsor", "drakkisath": "General Drakkisath", "helendis": "Helendis Riverhorn", "rexxar": "Rexxar",
    "brasaliza": "Emberstrife", "bolvar": "Bolvar Fordragon", "thrall": "Thrall", "barrow": "Barrow Deeps", "hyjal": "Mount Hyjal",
    "ashlam": "Commander Ashlam Valorfist", "baluarte": "The Bulwark", "kargath": "Kargath", "tuercespina": "Stranglethorn Vale",
    "desolace": "Desolace", "tanaris": "Tanaris", "cuna": "Winterspring", "peste_oeste": "Western Plaguelands", "azshara": "Azshara",
    "kroldok": "Krol'dok Stronghold", "drowned": "The Drowned City", "alcaz": "Alcaz Island", "blackmaw": "Blackmaw Hold",
    "shendralas": "Shen'dralas", "muertobosque": "Deadwood tribe", "nevada": "Winterfall tribe", "jokerd": "Jokerd",
}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def icono(slug, i):
    try:
        j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/item/{i}?locale=0"))
        assert j.get("icon")
    except Exception:
        j = json.loads(get(f"https://nether.wowhead.com/classic/tooltip/item/{i}?locale=0"))
    im = Image.open(io.BytesIO(get(f"https://wow.zamimg.com/images/wow/icons/large/{j['icon']}.jpg"))).convert("RGBA")
    im.resize((320, 320), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
    return j.get("name")


def wiki(titulos):
    out = dict(pages={}, redirects=[], normalized=[])
    for k in range(0, len(titulos), 40):
        q = urllib.parse.urlencode(dict(action="query", prop="pageimages", piprop="original", redirects=1, format="json",
                                        titles="|".join(titulos[k:k + 40])))
        r = json.loads(get("https://wowpedia.fandom.com/api.php?" + q))["query"]
        out["pages"].update(r.get("pages", {}))
        out["redirects"] += r.get("redirects", [])
        out["normalized"] += r.get("normalized", [])
    return out


def main():
    log = []
    for slug, i in ITEMS.items():
        try:
            log.append(f"{slug}: {icono(slug, i)}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    t = list(WIKI.items())
    q = wiki([v for _, v in t])
    red = {x["from"]: x["to"] for x in q.get("redirects", [])}
    nor = {x["from"]: x["to"] for x in q.get("normalized", [])}
    pags = {p["title"]: p for p in q["pages"].values()}
    for slug, titulo in t:
        n = red.get(nor.get(titulo, titulo), nor.get(titulo, titulo))
        url = pags.get(n, {}).get("original", {}).get("source")
        if not url:
            log.append(f"SIN IMAGEN {slug} {titulo}")
            continue
        try:
            im = Image.open(io.BytesIO(get(url))).convert("RGBA")
            if max(im.size) >= 1000:
                g = im.copy()
                g.thumbnail((1920, 1920))
                g.convert("RGB").save(os.path.join(PAN, slug + ".jpg"), quality=92)
            im.thumbnail((700, 700))
            im.save(os.path.join(PEG, slug + ".png"))
            log.append(f"{slug}: {titulo} {im.size} {url.split('/images/')[-1][:60]}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    open(os.path.join(D, "pegatinas", "_fuentes.txt"), "w", encoding="utf-8").write("\n".join(log))
    print("\n".join(log))
    hoja()


def hoja():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png"))
    col = 10
    h = Image.new("RGB", (col * 180, (len(fs) // col + 1) * 200), (40, 40, 40))
    d = ImageDraw.Draw(h)
    for n, f in enumerate(fs):
        im = Image.open(os.path.join(PEG, f)).convert("RGBA")
        im.thumbnail((170, 170))
        x, y = (n % col) * 180 + 5, (n // col) * 200 + 5
        h.paste(im, (x, y), im)
        d.text((x, y + 175), f[:-4][:24], fill="white")
    h.save(os.path.join(D, "previews", "_hoja_peg.jpg"), quality=85)
    print("hoja:", len(fs))


if __name__ == "__main__":
    main()
