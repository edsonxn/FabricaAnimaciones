# -*- coding: utf-8 -*-
"""Pegatinas de «30 trucos para NUNCA quedarte sin ORO en WoW Forever» (15-nov-2026; copiado de wow_forever_experiencia).
- Íconos de objetos: API de tooltips de Wowhead FOREVER (id comprobado por NOMBRE en el tooltip; nombre es-ES en _iconos.md).
  Prefijo o_ = ícono de 56 px ampliado (va en ficha/tarjeta, no a pantalla completa).
- PNJ, criaturas y lugares: imagen principal de su página de warcraft.wiki.gg (identidad = título exacto de la página;
  WIKI_FILE fuerza un archivo concreto cuando la imagen principal no es la de Classic/Forever).
python _pegatinas.py → pegatinas/<slug>.png + pantallas/<slug>.jpg (si es grande) + previews/_hoja_peg.jpg (MIRARLA)
NO toca los com_*.png (tarjetas de comentarios)."""
import io
import json
import os
import urllib.parse
import urllib.request

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
PEG, PAN = os.path.join(D, "pegatinas"), os.path.join(D, "pantallas")
for c in (PEG, PAN, os.path.join(D, "previews")):
    os.makedirs(c, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
WIKI_API = "https://warcraft.wiki.gg/api.php"

ITEMS = {  # slug: id de objeto (Wowhead Forever; nombre comprobado en el tooltip, ver _iconos.md)
    "o_bolsa_roja": 10051, "o_seda": 4306, "o_venda": 6451, "o_pagina": 2725, "o_cana_hierro": 6367,
    "o_receta_lobo": 12227, "o_filete": 12209, "o_tal_ardiente": 4479, "o_tal_trueno": 4480, "o_tal_blasonado": 4481,
    "o_perla_azul": 4611, "o_huevo": 12207, "o_pico": 5829, "o_hueso": 11418, "o_perla_oro": 13926, "o_tortuga": 3712,
    "o_cardopresto": 2452, "o_fuego": 7068, "o_adornos": 6532, "o_runico": 14047, "o_vil": 14256, "o_cristal": 12363,
    "o_torio": 10620, "o_loto": 13468, "o_cuero_ligero": 2318, "o_cuero_medio": 2319, "o_caja_feria": 19291,
    "o_tejido_magico": 4338,
}
WIKI = {  # slug: título exacto de warcraft.wiki.gg
    "strahad": "Strahad Farsan", "randal": "Randal Hunter", "kildar": "Kildar", "cholaruk": "Chol'aruk",
    "gelvas": "Gelvas Grimegate", "supervendedor": "Super-Seller 680", "exiliado_trueno_wiki": "Thundering Exile",
    "exiliado_ardiente": "Burning Exile", "exiliado_blasonado": "Cresting Exile",  # «Roc» de la wiki = Irewing (otro roc): los rocs de Tanaris van en URLS
    "planeador": "Surf Glider", "onyxia_guarida": "Onyxia", "heming": "Old Man Heming", "nat_pagle": "Nat Pagle",
    "satiro_jadefire": "Jadefire Satyr", "satiro_legashi": "Legashi Satyr", "almeja": "Giant Clam",
    "hyjal": "Mount Hyjal (Forever)", "frayfeather": "Frayfeather Skystormer", "dirge": "Dirge Quikcleave",
}
WIKI_FILE = {  # slug: archivo concreto (la imagen principal de la página no servía; revisado en la hoja del 15-nov)
    "strahad": "Strahad Farsan.jpg",      # la principal era el edificio del aquelarre de Trinquete
    "nat_pagle": "Nat Pagle.jpg",         # la principal era arte de Hearthstone
    "onyxia_guarida": "Onyxia.jpg",       # la principal era arte de Hearthstone; esta = en su guarida, en el juego
    "gelvas": "Gelvas Grimegate old.jpg", # modelo viejo (Classic/Forever)
}
URLS = {  # slug: imagen directa de la fuente. webthumbs = modelo de Wowhead FOREVER (classicplus), fondo transparente
    "roc": "https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/176/3248.webp",          # wowhead.com/forever/npc=5428 «Roc» (Tanaris)
    "roc_fuego": "https://wow.zamimg.com/uploads/screenshots/normal/897358.jpg",                 # captura en wowhead.com/classic/npc=5429 Fire Roc (Tanaris)
    "onyxia": "https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/122/8570.webp",       # wowhead.com/forever/npc=10184
    "exiliado_trueno": "https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/114/5490.webp",  # wowhead.com/forever/npc=2762
    "veta_torio": "https://wow.zamimg.com/uploads/screenshots/normal/46433.jpg",       # captura en wowhead.com/classic/object=175404
    "veta_torio_mina": "https://wow.zamimg.com/uploads/screenshots/normal/13681.jpg",  # misma página: minero picando la veta (1222×995 → pantallas/)
    "mister_graphed": "https://wow.zamimg.com/modelviewer/classicplus/webthumbs/npc/72/143688.webp",  # wowhead.com/forever/npc=263384 (displayId 143688)
    "auctionator_logo": "https://media.forgecdn.net/avatars/1403/232/638909541952729618.png",  # curseforge.com/wow/addons/auctionator
    "auctionator_vender": "https://media.forgecdn.net/attachments/721/366/2023-screenshot-classic-selling-1.png",
    "auctionator_compras": "https://media.forgecdn.net/attachments/721/368/2023-screenshot-classic-shopping-1.png",
    "auctionator_tooltip": "https://media.forgecdn.net/attachments/721/369/2023-screenshot-classic-tooltip-1.png",
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()


def icono(slug, i):
    try:
        j = json.loads(get(f"https://nether.wowhead.com/forever/tooltip/item/{i}?locale=0"))
        assert j.get("icon")
    except Exception:
        j = json.loads(get(f"https://nether.wowhead.com/classic/tooltip/item/{i}?locale=0"))
    im = Image.open(io.BytesIO(get(f"https://wow.zamimg.com/images/wow/icons/large/{j['icon']}.jpg"))).convert("RGBA")
    im.resize((320, 320), Image.LANCZOS).save(os.path.join(PEG, slug + ".png"))
    return f"{j.get('name')} [{j['icon']}]"


def wiki_q(**kw):
    q = urllib.parse.urlencode(dict(format="json", **kw))
    return json.loads(get(WIKI_API + "?" + q))["query"]


def url_archivo(nombre):
    p = list(wiki_q(action="query", prop="imageinfo", iiprop="url", titles="File:" + nombre)["pages"].values())[0]
    return p["imageinfo"][0]["url"]


def guardar(slug, url):
    im = Image.open(io.BytesIO(get(url))).convert("RGBA")
    caja = im.getchannel("A").point(lambda a: 255 if a > 8 else 0).getbbox()
    if caja and caja != (0, 0) + im.size:  # webthumbs con mucho margen transparente: recortar al modelo (+4 %)
        m = int(0.04 * max(im.size))
        im = im.crop((max(0, caja[0] - m), max(0, caja[1] - m), min(im.width, caja[2] + m), min(im.height, caja[3] + m)))
        im = im.resize((im.width * 2, im.height * 2), Image.LANCZOS) if max(im.size) < 350 else im
    if max(im.size) >= 1000:
        g = im.copy()
        g.thumbnail((1920, 1920))
        g.convert("RGB").save(os.path.join(PAN, slug + ".jpg"), quality=92)
    im.thumbnail((700, 700))
    im.save(os.path.join(PEG, slug + ".png"))
    return im.size


def main():
    log = []
    for slug, i in ITEMS.items():
        try:
            log.append(f"{slug}: {icono(slug, i)}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    for slug, url in URLS.items():
        try:
            log.append(f"{slug}: {guardar(slug, url)} {url}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    t = list(WIKI.items())
    q = wiki_q(action="query", prop="pageimages", piprop="original", redirects=1, titles="|".join(v for _, v in t))
    red = {x["from"]: x["to"] for x in q.get("redirects", [])}
    nor = {x["from"]: x["to"] for x in q.get("normalized", [])}
    pags = {p["title"]: p for p in q["pages"].values()}
    for slug, titulo in t:
        try:
            if slug in WIKI_FILE:
                url = url_archivo(WIKI_FILE[slug])
            else:
                n = red.get(nor.get(titulo, titulo), nor.get(titulo, titulo))
                url = pags.get(n, {}).get("original", {}).get("source")
            if not url:
                log.append(f"SIN IMAGEN {slug} {titulo}")
                continue
            log.append(f"{slug}: {titulo} {guardar(slug, url)} {url.split('/images/')[-1][:70]}")
        except Exception as e:
            log.append(f"FALLO {slug} {e}")
    open(os.path.join(PEG, "_fuentes.txt"), "w", encoding="utf-8").write("\n".join(log))
    print("\n".join(log))
    hoja()


def hoja():
    fs = sorted(f for f in os.listdir(PEG) if f.endswith(".png") and not f.startswith("com_"))
    col, cw, ch = 8, 230, 260
    h = Image.new("RGB", (col * cw, ((len(fs) + col - 1) // col) * ch), (40, 40, 40))
    d = ImageDraw.Draw(h)
    try:
        fnt = ImageFont.truetype("arial.ttf", 16)
    except OSError:
        fnt = None
    for n, f in enumerate(fs):
        im = Image.open(os.path.join(PEG, f)).convert("RGBA")
        im.thumbnail((cw - 10, ch - 40))
        x, y = (n % col) * cw + 5, (n // col) * ch + 5
        h.paste(im, (x, y), im)
        d.text((x, y + ch - 32), f[:-4][:26], fill="white", font=fnt)
    h.save(os.path.join(D, "previews", "_hoja_peg.jpg"), quality=85)
    print("hoja:", len(fs))


if __name__ == "__main__":
    main()
