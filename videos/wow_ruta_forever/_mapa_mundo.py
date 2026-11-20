# -*- coding: utf-8 -*-
"""Mapa del mundo de WoW FOREVER (Kalimdor + Isla Zephras + Reinos del Este) cosido con las teselas del mapa mundial
interactivo de Wowhead Forever (wow.zamimg.com/images/wow/classicplus/world-map/v3/<continente>/<zoom>/<fila>/<col>.webp;
manifiesto en nether.wowhead.com/forever/data/world-map). Sin rótulos: los nombres los ponemos nosotros.
Coordenadas: lienzo del mapa mundial (el mismo de los «rect» de las zonas) / 2**(7-Z). python _mapa_mundo.py → mapas/mundo_forever.jpg
"""
import io
import json
import os
import re
import urllib.request

from PIL import Image

D = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "Mozilla/5.0 (FabricaAnimaciones)"}
Z = 4
BASE = "https://wow.zamimg.com/images/wow/classicplus/world-map/v3"


def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()


def main():
    t = get("https://nether.wowhead.com/forever/data/world-map").decode("utf-8")
    cfg = json.loads(re.search(r'classicplus\.config",(\{.*?\})\);', t).group(1))
    i = t.find('classicplus.manifest",') + len('classicplus.manifest",')
    man = json.JSONDecoder().raw_decode(t[i:])[0]
    esc = 2 ** (7 - Z)
    W, H = cfg["canvasWidth"] // esc, cfg["canvasHeight"] // esc
    lienzo = Image.new("RGB", (W, H), (22, 52, 78))
    for c in cfg["continents"]:
        k = c["key"]
        filas = man["continents"][k]["zooms"][str(Z)]["rows"]
        filas = filas if isinstance(filas, dict) else {str(n): r for n, r in enumerate(filas)}
        for fila, rangos in filas.items():
            for a, b in rangos:
                for col in range(a, b + 1):
                    try:
                        im = Image.open(io.BytesIO(get(f"{BASE}/{k}/{Z}/{fila}/{col}.webp"))).convert("RGBA")
                    except Exception as e:
                        print("falta", k, fila, col, e)
                        continue
                    x = c["canvasX"] // esc + col * 256
                    y = c["canvasY"] // esc + int(fila) * 256
                    lienzo.paste(im, (x, y), im)
        print(k, "ok")
    lienzo.save(os.path.join(D, "mapas", "mundo_forever_lienzo.jpg"), quality=92)
    # recorte a la tierra, medido a mano sobre el lienzo (el mar de las teselas no es de un solo color)
    caja = (1476, 542, 5556, 3729)
    lienzo.crop(caja).save(os.path.join(D, "mapas", "mundo_forever.jpg"), quality=92)
    json.dump({"zoom": Z, "escala": esc, "recorte": caja, "nota": "px = (lienzo_x/escala - recorte[0], lienzo_y/escala - recorte[1])"},
              open(os.path.join(D, "mapas", "mundo_forever.json"), "w"), indent=1)
    print(W, H, caja)


def recorte(cont_key, rect, z, salida, ancho=1600):
    """Recorta del mapa mundial (teselas de zoom z) el rectángulo rect=[[x0,y0],[x1,y1]] del lienzo → mapas/<salida>.jpg"""
    t = get("https://nether.wowhead.com/forever/data/world-map").decode("utf-8")
    cfg = json.loads(re.search(r'classicplus\.config",(\{.*?\})\);', t).group(1))
    c = next(c for c in cfg["continents"] if c["key"] == cont_key)
    esc = 2 ** (7 - z)
    (x0, y0), (x1, y1) = rect
    lx0, ly0, lx1, ly1 = [(v - o) / esc for v, o in ((x0, c["canvasX"]), (y0, c["canvasY"]), (x1, c["canvasX"]), (y1, c["canvasY"]))]
    c0, c1, f0, f1 = int(lx0 // 256), int(lx1 // 256), int(ly0 // 256), int(ly1 // 256)
    im = Image.new("RGB", ((c1 - c0 + 1) * 256, (f1 - f0 + 1) * 256), (22, 52, 78))
    for f in range(f0, f1 + 1):
        for col in range(c0, c1 + 1):
            try:
                t_ = Image.open(io.BytesIO(get(f"{BASE}/{cont_key}/{z}/{f}/{col}.webp"))).convert("RGBA")
                im.paste(t_, ((col - c0) * 256, (f - f0) * 256), t_)
            except Exception:
                pass
    im = im.crop((int(lx0 - c0 * 256), int(ly0 - f0 * 256), int(lx1 - c0 * 256), int(ly1 - f0 * 256)))
    im = im.resize((ancho, round(ancho * im.height / im.width)), Image.LANCZOS)
    im.save(os.path.join(D, "mapas", salida + ".jpg"), quality=92)
    print(salida, im.size)


RECORTES = {  # salida: (continente, rect del lienzo, zoom)
    # La Vega con un 30 % más de mar al oeste para la Ciudad Anegada (x -15.6 del mapa de zona).
    # Conversión: X_oeste = (x_zona + 30) / 130 * 100 ; Y igual que el mapa de zona.
    "tuercespina_oeste": ("eastern-kingdoms", [[35244 - 0.30 * 6126, 25058], [41370, 29142]], 6),
    # La isla de la Ciudad Anegada de cerca (x_zona -8.4, y 50.6 de la Vega = centro del recorte)
    "ciudad_anegada_isla": ("eastern-kingdoms", [[34729 - 700, 27125 - 450], [34729 + 700, 27125 + 450]], 7),
    # Tierras de la Peste del Este con el encuadre de FOREVER (el mapa de zamimg 139 usa el de Classic y no cuadra)
    "peste_este_forever": ("eastern-kingdoms", [[39542, 10792], [43672, 13544]], 6),
    # La isla de la Prisión de Alcaz con el aspecto de Forever: x 64-86 %, y 8-30 % del Marjal (X_marjal = 64 + X*0.22; Y = 8 + Y*0.22)
    "alcaz_isla": ("kalimdor", [[17320 + 0.64 * 5040, 18336 + 0.08 * 3360], [17320 + 0.86 * 5040, 18336 + 0.30 * 3360]], 7),
}

if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["recortes"]:
        for k, (cont, r, z) in RECORTES.items():
            recorte(cont, r, z, k)
    else:
        main()
