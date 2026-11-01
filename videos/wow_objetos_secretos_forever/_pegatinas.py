# -*- coding: utf-8 -*-
"""Baja las pegatinas: íconos de Forever (API de tooltips de Wowhead) e imágenes de personajes/lugares (Wowpedia en Fandom).
python _pegatinas.py   → pegatinas/<slug>.png + pantallas/<slug>.jpg + previews/_hoja_peg.jpg (MIRARLA)"""
import io
import json
import os
import shutil
import urllib.parse
import urllib.request

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
os.makedirs(PEG, exist_ok=True)
os.makedirs(PAN, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}

ITEMS = {  # slug: (id, api)
    "delicia": 251525, "saltavientos": 268109, "babosa": 275682, "fango": 278265, "cria_croco": 282047, "banana": 270226,
    "crisalida": 276895, "cercenarrocas": 872, "contramaestre": 284715, "media_naranja": 284716, "galope": 271871,
    "loto": 13468, "riendas": 13335, "pagina": 281356, "fragmento": 281350, "llave": 281358,
}
WIKI = {  # slug: título de Wowpedia
    "murloc": "Murloc", "ogro": "Ogre", "crocolisco": "Crocolisk", "rhahkzor": "Rhahk'Zor", "smite": "Mr. Smite",
    "rivendare": "Baron Rivendare", "destrero": "Deathcharger", "graphed": "Goblin", "onyxia": "Onyxia", "ragnaros": "Ragnaros",
    "archimonde": "Archimonde", "cenarius": "Cenarius", "quelserrar": "Quel'Serrar", "orco": "Orc", "gruñido": "Grunt",
    "aggrend": "Josh Greenfield", "sátiro": "Satyr", "zanahoria": "Carrot on a Stick", "stratholme": "Stratholme",
    "roca_negra": "Blackrock Mountain", "portal": "Dark Portal", "ungoro": "Un'Goro Crater", "thoradin": "Thoradin's Wall",
    "entranas": "Undercity", "ventormenta": "Stormwind City", "hyjal": "Hyjal Summit", "pozo": "Moonwell", "nordrassil": "Nordrassil",
    "claro": "Moonglade", "cenarion": "Cenarion Circle", "nucleo": "Molten Core", "minas": "Deadmines", "skyborne": "Skyborne",
}
REUSA = {"bolsa_dormir": "wow_primera_semana", "kazzak": "wow_jugadores_rompieron"}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=25) as r:
        return r.read()


def icono(slug, i):
    j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/item/{i}?locale=11"))
    im = Image.open(io.BytesIO(get(f"https://wow.zamimg.com/images/wow/icons/large/{j['icon']}.jpg"))).convert("RGBA")
    im.resize((320, 320), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
    return j.get("name"), j["icon"]


def wiki(titulos):
    q = urllib.parse.urlencode(dict(action="query", prop="pageimages", piprop="original", redirects=1, format="json",
                                    titles="|".join(titulos)))
    return json.loads(get("https://wowpedia.fandom.com/api.php?" + q))["query"]


res = {}
for slug, i in ITEMS.items():
    try:
        res[slug] = icono(slug, i)
    except Exception as e:
        res[slug] = f"FALLO {e}"
    print(slug, res[slug], flush=True)

t = list(WIKI.items())
for k in range(0, len(t), 40):
    q = wiki([v for _, v in t[k:k + 40]])
    nombres = {x["from"]: x["to"] for x in q.get("redirects", [])}
    norm = {x["from"]: x["to"] for x in q.get("normalized", [])}
    pags = {p["title"]: p for p in q["pages"].values()}
    for slug, titulo in t[k:k + 40]:
        n = norm.get(titulo, titulo)
        n = nombres.get(n, n)
        p = pags.get(n, {})
        url = p.get("original", {}).get("source")
        if not url:
            print("SIN IMAGEN", slug, titulo, flush=True)
            continue
        try:
            im = Image.open(io.BytesIO(get(url))).convert("RGBA")
            print(slug, im.size, url[:90], flush=True)
            grande = im.copy()
            grande.thumbnail((1920, 1920))
            if max(im.size) >= 1000:
                grande.convert("RGB").save(os.path.join(PAN, slug + ".jpg"), quality=92)
            im.thumbnail((700, 700))
            im.save(os.path.join(PEG, slug + ".png"))
        except Exception as e:
            print("FALLO", slug, e, flush=True)

for slug, v in REUSA.items():
    src = os.path.join(D, "..", v, "pegatinas", slug + ".png")
    if os.path.exists(src):
        shutil.copy(src, PEG)

fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png") and not f.startswith("com_"))
col = 10
hoja = Image.new("RGB", (col * 180, (len(fs) // col + 1) * 200), (40, 40, 40))
from PIL import ImageDraw
d = ImageDraw.Draw(hoja)
for n, f in enumerate(fs):
    im = Image.open(os.path.join(PEG, f)).convert("RGBA")
    im.thumbnail((170, 170))
    x, y = (n % col) * 180 + 5, (n // col) * 200 + 5
    hoja.paste(im, (x, y), im)
    d.text((x, y + 175), f[:-4][:24], fill="white")
hoja.save(os.path.join(D, "previews", "_hoja_peg.jpg"), quality=85)
print("hoja lista:", len(fs))
