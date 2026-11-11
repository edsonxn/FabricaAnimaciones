# -*- coding: utf-8 -*-
"""Pegatinas de «25 SECRETOS de los primeros niveles de WoW Forever» (10-nov-2026).
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

ITEMS = {  # slug: id de objeto en Wowhead Forever (nombre en el buscador = el que dice la voz)
    "o_anillo": 264908,        # Ancient Heirloom
    "o_antorcha": 280612,      # Night Watchman's Torch
    "o_eluviana": 276188,      # Eluvi'ana
    "o_empunadura": 282315,    # Ancient Hilt
    "o_hoja": 264501,          # Ancient Skyborne Blade
    "o_pala": 273817,          # Graverobber's Shovel
    "o_tomo_negro": 276561,    # Black Tome
    "o_tomo_dalaran": 275989,  # Tome of Dalaran
    "o_munequera": 281256,     # Repurposed Hair Band
    "o_idolo": 263411,         # Idol of Shifting Tides
    "o_totem": 263412,         # Totem of Charged Flames
    "o_pienso": 11109,         # Special Chicken Feed
    "o_porra": 16114,          # Foreman's Blackjack
    "o_llave": 4882,           # Benedict's Key
    "o_bombay": 8485,          # Cat Carrier (Bombay)
    "o_carne": 287505,         # Tender Strider Meat
    "o_cuchara": 5198,         # Cookie's Stirring Rod
    "o_huevo": 11110,          # Chicken Egg
}
WIKI = {  # slug: título exacto de Wowpedia (comprobado: es ESE personaje/lugar de Classic)
    "kyle": "Kyle", "ahab": "Ahab Wheathoof", "ezra": "Ezra Chatterton", "donni": "Donni Anthania", "blanchy": "Old Blanchy",
    "saldean": "Farmer Saldean", "benedict": "Lieutenant Benedict", "tiragarde": "Tiragarde Keep", "cookie": "Cookie",
    "eitrigg": "Eitrigg", "thazzril": "Foreman Thazz'ril", "peones": "Lazy Peon", "khara": "Khara Deepwater",
    "humar": "Humar the Pridelord", "swiftmane": "Swiftmane", "takk": "Takk the Leaper", "rake": "The Rake",
    "arugal": "Archmage Arugal", "tortheldrin": "Prince Tortheldrin", "muro": "Greymane Wall", "genn": "Genn Greymane",
    "ruinas_lordaeron": "Ruins of Lordaeron", "colmillo": "Shadowfang Keep", "minas": "Deadmines", "colina_cuervo": "Raven Hill Cemetery",
    "valle_retos": "Valley of Trials", "pezuna": "Bloodhoof Village", "molino_ambar": "Ambermill", "pollo": "Westfall Chicken",
    "rex": "Cornish Rex", "naranja": "Orange Tabby", "plateado": "Silver Tabby", "shendralar": "Shen'dralar",
    "mazmorras": "Stormwind Stockade", "tirion": "Tirion Fordring", "thrall": "Thrall", "lordaeron_trono": "Terenas Menethil II",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=30) as r:
        return r.read()


def icono(slug, i):
    j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/item/{i}?locale=0"))
    im = Image.open(io.BytesIO(get(f"https://wow.zamimg.com/images/wow/icons/large/{j['icon']}.jpg"))).convert("RGBA")
    im.resize((320, 320), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
    return j.get("name")


def wiki(titulos):
    q = urllib.parse.urlencode(dict(action="query", prop="pageimages", piprop="original", redirects=1, format="json",
                                    titles="|".join(titulos)))
    return json.loads(get("https://wowpedia.fandom.com/api.php?" + q))["query"]


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
