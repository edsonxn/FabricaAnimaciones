# -*- coding: utf-8 -*-
"""Pegatinas de «30 cosas para vivir la experiencia REAL de WoW Forever» (12-nov-2026; copiado de wow_errores_30_60).
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
    "o_hogar": 6948, "o_cana": 6256, "o_fragmento": 6265, "o_flecha": 2512, "o_agua": 5350, "o_bolsa": 4238,
    "o_pez": 6291, "o_garra": 1931, "o_cebo": 6530, "o_pan": 4540,
}
SPELLS = {  # slug: id de hechizo (icono)
    "h_fogata": 818, "h_domesticar": 1515, "h_sucubo": 712, "h_oso": 5487, "h_invocar": 698, "h_conjurar_agua": 5504,
    "h_pesca": 7620, "h_gato": 768, "h_resurreccion": 2006, "h_totem": 8071,
}
WIKI = {  # slug: título exacto de Wowpedia (comprobar identidad en la hoja)
    "hogger": "Hogger", "mankrik": "Mankrik", "vancleef": "Edwin VanCleef", "stalvan": "Stalvan Mistmantle",
    "morladim": "Mor'Ladim", "sucubo": "Succubus", "espiritu_oso": "Great Bear Spirit", "angel": "Spirit Healer",
    "elwynn": "Elwynn Forest", "villadorada": "Goldshire", "villa_lago": "Lakeshire", "crestagrana": "Redridge Mountains",
    "villa_oscura": "Darkshire", "ocaso": "Duskwood", "colina_cuervo": "Raven Hill Cemetery", "paramos": "Westfall",
    "minas": "Deadmines", "lamentos": "Wailing Caverns", "cima_trueno": "Thunder Bluff", "forjaz": "Ironforge",
    "ventormenta": "Stormwind City", "orgrimmar": "Orgrimmar", "entranas": "Undercity", "molino_tarren": "Tarren Mill",
    "costasur": "Southshore", "baldios": "The Barrens", "cruce": "The Crossroads", "claro_luna": "Moonglade",
    "menethil": "Menethil Harbor", "theramore": "Theramore Isle", "auberdine": "Auberdine", "dun_morogh": "Dun Morogh",
    "teldrassil": "Teldrassil", "durotar": "Durotar", "tuercespina": "Stranglethorn Vale", "bahia": "Booty Bay",
    "zepelin": "Zeppelin", "darnassus": "Darnassus", "defias": "Defias Brotherhood", "nesingwary": "Nesingwary's Expedition",
    "trabalomas": "Hillsbrad Foothills", "grifo": "Gryphon", "posadero": "Innkeeper", "mor_tanaris": "Mulgore",
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


def icono_spell(slug, i):
    j = json.loads(get(f"https://nether.wowhead.com/classic/tooltip/spell/{i}?locale=0"))
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
    for slug, i in SPELLS.items():
        try:
            log.append(f"{slug}: {icono_spell(slug, i)}")
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
