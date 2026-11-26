# -*- coding: utf-8 -*-
"""Mapas de «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (25-nov-2026; mismo origen que wow_errores_60 y wow_ruta_forever).
- Mapas de zona de FOREVER en Wowhead: wow.zamimg.com/images/wow/classicplus/maps/<eses|enus>/original/<id de zona>.jpg (1 % = 1 coordenada).
  Claros del Río (16591) y Shen'dralas (16651) solo existen en enus.
- Monte Hyjal: el de zamimg (616) es un borrador → File:WorldMap-Hyjal-forever.jpg de warcraft.wiki.gg (mapa del juego de Forever, rótulos en inglés).
- Recortes de las TESELAS del mapa mundial de Wowhead Forever (classicplus/world-map/v3), sin rótulos, con su rect del lienzo en
  mapas/_rects.json para pasar coordenadas de zona → % del recorte (_coords_check.py):
    ventormenta / orgrimmar = rect de la CAPITAL (campo places): 1 % del recorte = 1 coordenada del mapa de ciudad de FOREVER
      (Ventormenta de Forever no es la de Classic: Georgio Bolero 53.3, 81.5)
    forjaz = mapa de ciudad de zamimg (1537): en las teselas Forjaz es solo la nieve de la montaña (la ciudad está bajo tierra)
    peste_este = rect de la zona (el 139 de zamimg tiene el encuadre de Classic y no cuadra con Forever)
    mundo = Kalimdor + Zephras + Reinos del Este en 16:9, de Teldrassil a Bahía del Botín (rutas por tramos y campamentos de Favor)
python _mapas.py [nombre…] → mapas/*.jpg + mapas/_fuentes.txt + mapas/_rects.json"""
import io
import json
import os
import re
import urllib.request

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
MAP = os.path.join(D, "mapas")
os.makedirs(MAP, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
BASE = "https://wow.zamimg.com/images/wow/classicplus/world-map/v3"
# nombre: (id de zona en zamimg, idioma)
ZONAS = {
    "durotar": (14, "eses"), "mulgore": (215, "eses"), "teldrassil": (141, "eses"), "elwynn": (12, "eses"),
    "humedales": (11, "eses"), "argenteos": (130, "eses"), "laderas": (267, "eses"), "arathi": (45, "eses"),
    "mil_agujas": (400, "eses"), "riverglades": (16591, "enus"), "interior": (47, "eses"), "tanaris": (440, "eses"),
    "ungoro": (490, "eses"), "frondavil": (361, "eses"), "cuna_invierno": (618, "eses"), "estepas": (46, "eses"),
    "tuercespina": (33, "eses"), "baldios": (17, "eses"), "crestagrana": (44, "eses"), "alterac": (36, "eses"),
    "feralas": (357, "eses"), "pantano": (8, "eses"), "sierra_espolon": (406, "eses"), "inhospitas": (3, "eses"),
    "desolace": (405, "eses"), "vallefresno": (331, "eses"), "marjal": (15, "eses"), "azshara": (16, "eses"),
    "shendralas": (16651, "enus"), "loch_modan": (38, "eses"), "bosque_ocaso": (10, "eses"), "paramos": (40, "eses"),
    "forjaz": (1537, "eses"),   # ciudad subterránea: las teselas solo muestran la nieve de encima → mapa de ciudad de zamimg
}
HYJAL = "https://warcraft.wiki.gg/images/WorldMap-Hyjal-forever.jpg"
# recortes: nombre: (rect [[x0,y0],[x1,y1]] del lienzo del mapa mundial, zoom de teselas, ancho final, nota)
RECORTES = {
    "ventormenta": ([[35722, 22012], [37390, 23124]], 7, 1920, "rect de Stormwind City (capital, places): mapa de ciudad de Forever"),
    "orgrimmar": ([[19917.4, 14201.1], [21263.9, 15099.1]], 7, 1920, "rect de Orgrimmar (capital, places)"),
    "peste_este": ([[39542, 10792], [43672, 13544]], 6, 2048, "rect de Eastern Plaguelands (zona, places): encuadre de Forever"),
    "mundo": ([[6000, 4700], [49600, 29225]], 4, 3200, "mundo entero en 16:9 (Kalimdor + Zephras + Reinos del Este, de Teldrassil a Bahía del Botín)"),
}


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=60) as r:
        return r.read()


def config():
    t = get("https://nether.wowhead.com/forever/data/world-map").decode("utf-8")
    cfg = json.loads(re.search(r'classicplus\.config",(\{.*?\})\);', t).group(1))
    i = t.find('classicplus.manifest",') + len('classicplus.manifest",')
    return cfg, json.JSONDecoder().raw_decode(t[i:])[0]


def recorte(cfg, man, rect, z, ancho):
    """Pega las teselas de TODOS los continentes que tocan el rect (zoom z) y recorta."""
    esc = 2 ** (7 - z)
    (x0, y0), (x1, y1) = rect
    W, H = int((x1 - x0) / esc), int((y1 - y0) / esc)
    im = Image.new("RGB", (W, H), (22, 52, 78))
    for c in cfg["continents"]:
        k = c["key"]
        filas = man["continents"][k]["zooms"][str(z)]["rows"]
        filas = filas if isinstance(filas, dict) else {str(n): r for n, r in enumerate(filas)}
        for fila, rangos in filas.items():
            for a, b in rangos:
                for col in range(a, b + 1):
                    tx, ty = c["canvasX"] + col * 256 * esc, c["canvasY"] + int(fila) * 256 * esc
                    if tx + 256 * esc < x0 or tx > x1 or ty + 256 * esc < y0 or ty > y1:
                        continue
                    try:
                        t_ = Image.open(io.BytesIO(get(f"{BASE}/{k}/{z}/{fila}/{col}.webp"))).convert("RGBA")
                    except Exception as e:
                        print("falta", k, z, fila, col, e)
                        continue
                    im.paste(t_, (int((tx - x0) / esc), int((ty - y0) / esc)), t_)
    return im.resize((ancho, round(ancho * H / W)), Image.LANCZOS)


def main(solo=None):
    ff = os.path.join(MAP, "_fuentes.txt")
    fuentes = [l for l in open(ff, encoding="utf-8").read().splitlines()
               if l.strip() and l.split()[0][:-4] not in solo] if solo and os.path.isfile(ff) else []
    for n, (z, idioma) in ZONAS.items():
        if solo and n not in solo:
            continue
        url = f"https://wow.zamimg.com/images/wow/classicplus/maps/{idioma}/original/{z}.jpg"
        im = Image.open(io.BytesIO(get(url))).convert("RGB")
        im.save(os.path.join(MAP, n + ".jpg"), quality=92)
        fuentes.append(f"{n}.jpg  zamimg classicplus/maps/{idioma}/original/{z}.jpg (Forever) {im.size[0]}x{im.size[1]}")
        print(n, im.size)
    if not solo or "hyjal" in solo:
        im = Image.open(io.BytesIO(get(HYJAL))).convert("RGB")
        im.save(os.path.join(MAP, "hyjal.jpg"), quality=92)
        fuentes.append(f"hyjal.jpg  warcraft.wiki.gg File:WorldMap-Hyjal-forever.jpg (mapa del juego de Forever, rótulos en inglés; "
                       f"el de zamimg 616 es un borrador) {im.size[0]}x{im.size[1]}")
    rf = os.path.join(MAP, "_rects.json")
    rects = json.load(open(rf)) if solo and os.path.isfile(rf) else {}
    if not solo or any(n in solo for n in RECORTES):
        cfg, man = config()
        for n, (rect, z, ancho, nota) in RECORTES.items():
            if solo and n not in solo:
                continue
            im = recorte(cfg, man, rect, z, ancho)
            im.save(os.path.join(MAP, n + ".jpg"), quality=92)
            rects[n] = dict(rect=rect, zoom=z, tam=list(im.size), nota=nota)
            fuentes.append(f"{n}.jpg  teselas del mapa mundial de Wowhead Forever (classicplus/world-map/v3, zoom {z}), rect {rect} "
                           f"del lienzo ({nota}); sin rótulos {im.size[0]}x{im.size[1]}")
            print(n, im.size)
    json.dump(rects, open(rf, "w"), indent=1)
    open(ff, "w", encoding="utf-8").write("\n".join(sorted(fuentes)) + "\n")


if __name__ == "__main__":
    import sys
    main(set(sys.argv[1:]) or None)
