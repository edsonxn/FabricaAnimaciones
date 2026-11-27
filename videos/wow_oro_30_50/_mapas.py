# -*- coding: utf-8 -*-
"""Mapas de «15 FARMEOS de ORO del 30 al 50 en WoW Forever» (25-nov-2026; adaptado de wow_ruta_profesiones/_mapas.py).
MAPAS = SIEMPRE EL ORIGINAL A TODO COLOR (cambio del usuario al kit, 25-nov): el mapa de zona del juego, sin teñir.
- Mapas de zona de FOREVER en Wowhead: wow.zamimg.com/images/wow/classicplus/maps/<eses|enus>/original/<id de zona>.jpg (1 % = 1 coordenada).
  Claros del Río (16591) solo existe en enus. Las Tierras Devastadas = zona 4 (MIRAR: el 4 es zona, no continente).
- «mundo» = recorte de las TESELAS del mapa mundial de Wowhead Forever (classicplus/world-map/v3), sin rótulos, en 16:9, de Feralas a
  Claros del Río y de Alterac a Bahía del Botín (las 11 zonas del video); rect del lienzo en mapas/_rects.json para pasar coordenadas de
  zona → % del recorte (M() de _coords_check.py).
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
    "desolace": (405, "eses"), "marjal": (15, "eses"), "tuercespina": (33, "eses"), "mil_agujas": (400, "eses"),
    "riverglades": (16591, "enus"), "inhospitas": (3, "eses"), "pantano": (8, "eses"), "tanaris": (440, "eses"),
    "feralas": (357, "eses"), "alterac": (36, "eses"), "devastadas": (4, "eses"),
}
# recortes: nombre: (rect [[x0,y0],[x1,y1]] del lienzo del mapa mundial, zoom de teselas, ancho final, nota)
RECORTES = {
    "mundo": ([[10400, 11300], [44600, 30538]], 4, 3200, "Kalimdor + Reinos del Este en 16:9, de Feralas a Claros del Río y de Alterac a Bahía del Botín (las 11 zonas del video)"),
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
