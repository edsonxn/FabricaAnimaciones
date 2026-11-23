# -*- coding: utf-8 -*-
"""Mapas de «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (22-nov-2026; mismo origen que wow_ruta_forever/mapas).
- Mapas de zona de FOREVER en Wowhead: wow.zamimg.com/images/wow/classicplus/maps/eses/original/<id de zona>.jpg (1 % = 1 coordenada).
- Monte Hyjal: el de zamimg (616) es un borrador → File:WorldMap-Hyjal-forever.jpg de warcraft.wiki.gg (mapa del juego, rótulos en inglés).
- Recortes de las TESELAS del mapa mundial de Wowhead Forever (classicplus/world-map/v3), sin rótulos, con su rect del lienzo en
  mapas/_rects.json para pasar coordenadas de zona → % del recorte (_coords_check.py):
    ungoro_norte  = Un'Goro con un 22 % más al norte (el pin del Bancal del Creador cae ENCIMA del mapa de zona)
    peste_forever = Tierras de la Peste del Oeste + del Este juntas (Scholomance y Stratholme en un solo mapa; encuadre de Forever)
    kalimdor_bandas = norte y este de Kalimdor en 16:9 (Hyjal, Cuna del Invierno, Azshara, Marjal): las tres puertas de banda
    mundo_bandas = mundo entero de Forever en 16:9 (ruta de la cadena del conjunto 0.5: Forjaz/Orgrimmar → … → Cumbre)
python _mapas.py → mapas/*.jpg + mapas/_fuentes.txt + mapas/_rects.json"""
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
ZONAS = {"estepas": 46, "marjal": 15, "cuna_invierno": 618, "azshara": 16, "ungoro": 490, "tanaris": 440}
HYJAL = "https://warcraft.wiki.gg/images/WorldMap-Hyjal-forever.jpg"
# recortes: nombre: (rect [[x0,y0],[x1,y1]] del lienzo del mapa mundial, zoom de teselas, ancho final, nota)
RECORTES = {
    "ungoro_norte": ([[15872, 21591], [19424, 24480]], 6, 1600, "Un'Goro (rect de zona) + 22 % al norte"),
    "peste_forever": ([[36976, 10200], [43400, 13856]], 6, 2400, "rect de WPL ∪ EPL, con 600 más al norte (Stratholme no queda en el borde)"),
    "cavernas_puertas": ([[16900, 9000], [24400, 13219]], 5, 2400, "Hyjal + Cuna del Invierno + norte de Azshara en 16:9 (puertas de las Cavernas del Túmulo)"),
    "kalimdor_bandas": ([[6500, 7600], [32100, 22000]], 4, 3200, "norte/este de Kalimdor en 16:9"),
    "mundo_bandas": ([[8000, 3000], [50000, 26625]], 4, 3200, "mundo entero en 16:9 (Kalimdor + Zephras + Reinos del Este)"),
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
    fuentes = [l for l in open(os.path.join(MAP, "_fuentes.txt"), encoding="utf-8").read().splitlines()
               if solo and l.split()[0][:-4] not in solo] if solo else []
    for n, z in ZONAS.items():
        if solo:
            break
        url = f"https://wow.zamimg.com/images/wow/classicplus/maps/eses/original/{z}.jpg"
        im = Image.open(io.BytesIO(get(url))).convert("RGB")
        im.save(os.path.join(MAP, n + ".jpg"), quality=92)
        fuentes.append(f"{n}.jpg  zamimg classicplus/maps/eses/original/{z}.jpg (Forever) {im.size[0]}x{im.size[1]}")
        print(n, im.size)
    if not solo:
        im = Image.open(io.BytesIO(get(HYJAL))).convert("RGB")
        im.save(os.path.join(MAP, "hyjal.jpg"), quality=92)
        fuentes.append(f"hyjal.jpg  warcraft.wiki.gg File:WorldMap-Hyjal-forever.jpg (mapa del juego de Forever, rótulos en inglés; "
                       f"el de zamimg 616 es un borrador) {im.size[0]}x{im.size[1]}")
    cfg, man = config()
    rf = os.path.join(MAP, "_rects.json")
    rects = json.load(open(rf)) if solo and os.path.isfile(rf) else {}
    for n, (rect, z, ancho, nota) in RECORTES.items():
        if solo and n not in solo:
            continue
        im = recorte(cfg, man, rect, z, ancho)
        im.save(os.path.join(MAP, n + ".jpg"), quality=92)
        rects[n] = dict(rect=rect, zoom=z, tam=list(im.size), nota=nota)
        fuentes.append(f"{n}.jpg  teselas del mapa mundial de Wowhead Forever (classicplus/world-map/v3, zoom {z}), rect {rect} "
                       f"del lienzo ({nota}); sin rótulos {im.size[0]}x{im.size[1]}")
        print(n, im.size)
    json.dump(rects, open(os.path.join(MAP, "_rects.json"), "w"), indent=1)
    open(os.path.join(MAP, "_fuentes.txt"), "w", encoding="utf-8").write("\n".join(fuentes) + "\n")


if __name__ == "__main__":
    import sys
    main(set(sys.argv[1:]) or None)
