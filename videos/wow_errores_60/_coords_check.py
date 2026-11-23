# -*- coding: utf-8 -*-
"""Coordenadas de «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (22-nov-2026; adaptado de wow_ruta_forever/_coords_check.py).
Fuentes: WHF = mapa mundial de Wowhead Forever (nether.wowhead.com/forever/data/world-map: pines de PNJ/mazmorra/banda, leídos el 22-nov);
WHF-lugar = rótulo de subzona del mismo archivo (campo places), pasado a % de la zona con el rect de la zona;
INV = videos/_investigacion_wow_errores_60.md (guías de Forever: Conquest Capped…). Mapas de zona: 1 % de la imagen = 1 de coordenada.
Mapas de teselas (ungoro_norte, peste_forever, kalimdor_bandas, mundo_bandas): coordenada de zona → lienzo (rect de la zona) → % del
recorte (rect en mapas/_rects.json). Los % que salen aquí son los que van a P(x, y, …) de efectos.py.
    python _coords_check.py      → previews/_coords_check_N.jpg (4 mapas por hoja, MIRARLAS)
    python _coords_check.py md   → imprime la tabla de _coords.md
Tipos: C = centro (pueblo/vuelo) · R = punto de ruta/lugar · M = entrada de mazmorra/banda · P = PNJ o referencia."""
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

D = os.path.dirname(os.path.abspath(__file__))
W_, WL, INV = "WHF", "WHF-lugar", "INV"
# rect de cada zona en el lienzo del mapa mundial de Wowhead Forever (campo places, kind=zone)
ZR = {
    "hyjal": [[17270, 10332], [20604, 12554]], "cuna": [[16688, 8192], [23504, 12736]], "azshara": [[19530, 11256], [24398, 14502]],
    "ungoro": [[15872, 22112], [19424, 24480]], "marjal": [[17320, 18336], [22360, 21696]], "estepas": [[37632, 21086], [40444, 22960]],
    "epl": [[39542, 10792], [43672, 13544]], "wpl": [[36976, 11104], [41104, 13856]], "tanaris": [[16594, 22024], [23218, 26440]],
}
RECTS = json.load(open(os.path.join(D, "mapas", "_rects.json")))


def lienzo(zona, x, y):
    (x0, y0), (x1, y1) = ZR[zona]
    return x0 + x / 100 * (x1 - x0), y0 + y / 100 * (y1 - y0)


def L(mapa, cx, cy):
    """punto del lienzo → % del recorte de teselas «mapa»"""
    (x0, y0), (x1, y1) = RECTS[mapa]["rect"]
    return round(100 * (cx - x0) / (x1 - x0), 1), round(100 * (cy - y0) / (y1 - y0), 1)


def Z(mapa, zona, x, y):
    return L(mapa, *lienzo(zona, x, y))


# mapa: [(escena, x, y, rótulo, tipo, fuente, confianza)]
PTS = {
    "estepas": [("c11 c04", 33.0, 25.2, "Cumbre de Roca Negra (entrada)", "M", W_, "ALTA (pin de mazmorra)"),
                ("c01", 32.2, 25.8, "Bodley (fantasma, cadena 0.5)", "P", W_, "ALTA"),
                ("c01", 74.0, 66.0, "Ejecutor Asharell (~74, 66)", "P", INV, "MEDIA (guía; «sur de Las Estepas»; sin pin en WHF)"),
                ("c01", 85.9, 67.6, "Vigilia de Morgan", "C", WL, "ALTA (referencia)")],
    "marjal": [("c23 c10 c09 c08", 52.9, 77.7, "Guarida de Onyxia", "M", W_, "ALTA (pin de banda)"),
               ("c04", 56.6, 87.6, "Brasaliza (Ciénaga de Fuego)", "P", W_, "ALTA"),
               ("c21 c08", 65.0, 47.1, "Isla Theramore", "C", WL, "ALTA (referencia)"),
               ("c21 c08", 36.3, 31.4, "Poblado Murohelecho", "C", WL, "ALTA (referencia)")],
    "hyjal": [("c18 c06", 78.5, 36.9, "Cima de la Eternidad", "R", WL, "ALTA"),
              ("c18", 68.6, 44.0, "vuelo (Fayran Elthas)", "C", W_, "ALTA"),
              ("c06", 68.8, 50.4, "Tiala Melenablanca", "P", W_, "ALTA"),
              ("c06", 70.6, 51.2, "Rhylin Espinapiedra (intendente)", "P", W_, "ALTA"),
              ("c18 c08", 85.0, 33.0, "portal de la Cima Hyjal (~85, 33)", "M", INV, "MEDIA (investigación; WHF no tiene pin propio)"),
              ("c17 c08", 70.0, 62.0, "Cavernas del Túmulo, entrada (~70, 62)", "M", INV, "MEDIA (investigación «según los archivos»)"),
              ("—", 58.4, 57.1, "pin WHF de las 2 bandas (genérico)", "P", W_, "BAJA: el mismo pin para Cima y Cavernas; NO usar en pantalla"),
              ("c18", 59.3, 74.3, "Laderas Maculadas", "R", WL, "ALTA (referencia)")],
    "cuna_invierno": [("c17", 61.2, 38.2, "Vista Eterna", "C", WL, "ALTA"),
                      ("c17", 58.2, 85.6, "Garganta Negro Rumor (a Hyjal)", "R", WL, "ALTA"),
                      ("c17 c16", 70.0, 90.5, "Bastión Faucenegra (lado de Cuna)", "M", WL, "ALTA (rótulo de subzona)")],
    "azshara": [("c16 c12 c17", 38.4, 32.6, "Bastión Faucenegra: piedra de encuentro", "M", INV, "ALTA (guía; WHF 39.6, 32.3)"),
                ("c17 c16", 35.0, 23.4, "Bastión Faucenegra: portal", "M", INV, "ALTA (guía; junto a Cuna del Invierno)"),
                ("c16", 21.8, 50.0, "Valormok (vuelo H)", "C", WL, "ALTA"),
                ("c16", 11.7, 77.9, "Punta Talrendis (vuelo A)", "C", WL, "ALTA"),
                ("c16", 47.5, 26.4, "Ursolan", "R", WL, "ALTA"),
                ("c16", 33.6, 56.9, "Ruinas de Eldarath", "R", WL, "ALTA")],
    "ungoro": [("c15", 43.6, 7.2, "Refugio de los Mariscales", "C", WL, "ALTA"),
               ("c15", 45.2, 5.8, "vuelo (Gryfe)", "C", W_, "ALTA"),
               ("c15", 48.1, 6.1, "Bancal del Creador (guía)", "M", INV, "MEDIA: guía 48.1, 6.1; el pin WHF cae 8,8 % por ENCIMA del mapa")],
    "ungoro_norte": [("c15",) + Z("ungoro_norte", "ungoro", 43.6, 7.2) + ("Refugio de los Mariscales", "C", WL, "ALTA"),
                     ("c15",) + Z("ungoro_norte", "ungoro", 45.2, 5.8) + ("vuelo (Gryfe)", "C", W_, "ALTA"),
                     ("c15",) + Z("ungoro_norte", "ungoro", 48.1, 6.1) + ("Bancal del Creador (guía 48.1, 6.1)", "M", INV, "MEDIA"),
                     ("c15",) + L("ungoro_norte", 17552, 21904) + ("Bancal del Creador (pin WHF)", "M", W_, "ALTA el dato (pin de mazmorra)")],
    "tanaris": [("c01", 52.4, 27.2, "Mux Malamaná (Gadgetzan)", "P", W_, "ALTA"),
                ("c01", 51.2, 27.5, "Gadgetzan", "C", WL, "ALTA")],
    "peste_forever": [("c05 c01", ) + L("peste_forever", 40619.4, 11079.4) + ("Stratholme (entrada)", "M", W_, "ALTA (pin)"),
                      ("c01",) + Z("peste_forever", "epl", 21.7, 6.7) + ("Anthion Harmon", "P", W_, "ALTA"),
                      ("c05 c01",) + L("peste_forever", 39826.5, 13112.2) + ("Scholomance (entrada)", "M", W_, "ALTA (pin)"),
                      ("c05 c01",) + Z("peste_forever", "wpl", 69.0, 75.0) + ("Castel Darrow", "R", WL, "ALTA"),
                      ("c01",) + Z("peste_forever", "epl", 71.9, 49.1) + ("Capilla Esperanza de la Luz (Alba Argenta)", "C", WL, "ALTA")],
    "kalimdor_bandas": [("c17 c08",) + Z("kalimdor_bandas", "hyjal", 70.0, 62.0) + ("Cavernas del Túmulo · puerta de Hyjal", "M", INV, "MEDIA"),
                        ("c18 c08",) + Z("kalimdor_bandas", "hyjal", 85.0, 33.0) + ("Cima Hyjal", "M", INV, "MEDIA"),
                        ("c17 c08",) + Z("kalimdor_bandas", "azshara", 35.0, 23.4) + ("Cavernas · puerta del Bastión Faucenegra", "M", INV, "ALTA"),
                        ("c17 c08",) + Z("kalimdor_bandas", "cuna", 61.2, 38.2) + ("Cuna del Invierno (puerta sin coordenada)", "R", WL, "BAJA: marca la ZONA (Vista Eterna), no la puerta"),
                        ("c08 c23",) + L("kalimdor_bandas", 19986.3, 20947.2) + ("Guarida de Onyxia", "M", W_, "ALTA (pin)")],
    "cavernas_puertas": [("c17",) + Z("cavernas_puertas", "hyjal", 70.0, 62.0) + ("Cavernas · puerta del Monte Hyjal (~70, 62)", "M", INV, "MEDIA"),
                         ("c17",) + Z("cavernas_puertas", "azshara", 35.0, 23.4) + ("Cavernas · puerta del Bastión Faucenegra", "M", INV, "ALTA"),
                         ("c17 c16",) + Z("cavernas_puertas", "azshara", 38.4, 32.6) + ("Bastión Faucenegra (entrada)", "M", INV, "ALTA"),
                         ("c17",) + Z("cavernas_puertas", "cuna", 61.2, 38.2) + ("Cuna del Invierno · Vista Eterna (puerta sin coordenada)", "R", WL, "BAJA: zona, no puerta"),
                         ("c18",) + Z("cavernas_puertas", "hyjal", 85.0, 33.0) + ("Cima Hyjal (~85, 33)", "M", INV, "MEDIA"),
                         ("c18 c06",) + Z("cavernas_puertas", "hyjal", 78.5, 36.9) + ("Cima de la Eternidad", "R", WL, "ALTA")],
    "mundo_bandas": [("c01",) + L("mundo_bandas", 38390.5, 18986.9) + ("Forjaz · Deliana (A)", "P", W_, "ALTA"),
                     ("c01",) + L("mundo_bandas", 20386, 14542.3) + ("Orgrimmar · Mokvar (H)", "P", W_, "ALTA"),
                     ("c01",) + Z("mundo_bandas", "tanaris", 52.4, 27.2) + ("Tanaris · Mux", "P", W_, "ALTA"),
                     ("c01",) + L("mundo_bandas", 40619.4, 11079.4) + ("Stratholme", "M", W_, "ALTA"),
                     ("c01",) + L("mundo_bandas", 15299.2, 20135.7) + ("La Masacre", "M", W_, "ALTA"),
                     ("c01",) + Z("mundo_bandas", "estepas", 32.2, 25.8) + ("Roca Negra · Bodley", "P", W_, "ALTA"),
                     ("c01",) + Z("mundo_bandas", "estepas", 74.0, 66.0) + ("Estepas · Ejecutor Asharell", "P", INV, "MEDIA"),
                     ("c01",) + L("mundo_bandas", 38559.7, 21557.6) + ("Cumbre superior · Valthalak", "M", W_, "ALTA (pin de Cumbre de Roca Negra)")],
}
COLOR = {"C": (255, 60, 60), "R": (255, 230, 0), "M": (80, 200, 255), "P": (255, 140, 255)}


def fuente(n):
    for f in ("arialbd.ttf", "arial.ttf"):
        try:
            return ImageFont.truetype(f, n)
        except OSError:
            pass
    return ImageFont.load_default()


def hojas():
    F = fuente(15)
    minis = []
    for m, pts in PTS.items():
        im = Image.open(os.path.join(D, "mapas", m + ".jpg")).convert("RGB")
        im = im.resize((1024, round(1024 * im.height / im.width)))
        W, H = im.size
        d = ImageDraw.Draw(im)
        for e, x, y, r, t, *_ in pts:
            px, py = x / 100 * W, y / 100 * H
            d.ellipse((px - 6, py - 6, px + 6, py + 6), outline=COLOR[t], width=3)
            d.text((px + 8, py - 8), f"{r} [{x:.1f},{y:.1f}]", fill=COLOR[t], font=F, stroke_width=2, stroke_fill=(0, 0, 0))
        d.text((8, H - 24), m, fill=(0, 255, 255), font=fuente(20), stroke_width=2, stroke_fill=(0, 0, 0))
        minis.append(im.resize((960, round(960 * H / W))))
    por = 4
    for k in range(0, len(minis), por):
        lote = minis[k:k + por]
        alto = max(mi.height for mi in lote)
        g = Image.new("RGB", (2 * 960, ((len(lote) + 1) // 2) * alto), (20, 20, 20))
        for i, mi in enumerate(lote):
            g.paste(mi, ((i % 2) * 960, (i // 2) * alto))
        g.save(os.path.join(D, "previews", f"_coords_check_{k // por + 1}.jpg"), quality=85)
    print(len(minis), "mapas;", (len(minis) + por - 1) // por, "hojas")


def md():
    print("| Mapa | Escena | Punto | Tipo | x, y (% del mapa) | Fuente | Confianza |\n|---|---|---|---|---|---|---|")
    for m, pts in PTS.items():
        for e, x, y, r, t, f, c in pts:
            print(f"| `{m}` | {e} | {r} | {t} | {x:.1f}, {y:.1f} | {f} | {c} |")


if __name__ == "__main__":
    md() if sys.argv[1:] == ["md"] else hojas()
