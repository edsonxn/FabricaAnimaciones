# -*- coding: utf-8 -*-
"""Hoja de prueba de los MG nuevos de este video: cada MG a MITAD (izq.) y en su CUADRO FINAL con todas las marcas
disparadas (der.), sobre fondo rojizo → previews/mg_prueba_hoja.jpg (y previews/mg_<nombre>.jpg sueltas).
    python _prueba_mg.py [nombre ...]
"""
import os
import sys

from PIL import Image, ImageDraw

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import mg_er as E


def _P(s):
    return os.path.join(AQUI, "pegatinas", s + ".png")


PRUEBAS = [   # (nombre, fn, marcas, dur, t_mitad)
    ("inquisicion", E.inquisicion([("Candelabro de inquisidor", _P("candelabro")), ("Rueda de Ghiza", _P("rueda_ghiza")),
                                   ("Máscara ensangrentada", _P("mascara_ensangrentada")),
                                   ("Atuendo de oficial", _P("atuendo_oficial"))]),
     [0.4, 1.6, 2.8, 4.0, 5.4], 8, 3.2),
    ("red_secuestro", E.red_secuestro(["Academia de Raya Lucaria", "Mansión de los Caria", "Monte Gelmir",
                                       "Afueras de la capital", "Leyndell"], destino="Cámara de la inquisición",
                                      sub_destino="Mansión del Volcán", remate="Una red de punta a punta del mapa",
                                      titulo="Las vírgenes raptoras"),
     [0.4, 1.4, 2.4, 3.4, 4.4, 5.6], 9, 2.9),
    ("estandarte_caido", E.estandarte_caido(emblema="Caballeros de Gelmir",
                                            quien="un señor que empezó con nobles ambiciones",
                                            remate="Un emblema que ya nadie usa"),
     [0.8, 2.6, 3.8], 7, 1.9),
    ("incubadora", E.incubadora(), [0.5, 2.0, 4.2], 7, 2.6),
    ("recibo", E.recibo(concepto="la noche del complot", pagador="Ranni", cobrador="pretor Rykard",
                        pago="restos de la Runa de la Muerte"),
     [0.5, 1.6, 2.7, 3.9, 5.4], 8, 3.2),
]
ANCHO = 900


def cuadro(f, t, dur, mk):
    a = f(t, dur, mk)
    im = Image.fromarray(a[..., [2, 1, 0, 3]])
    bg = Image.new("RGBA", im.size, (60, 40, 40, 255))
    bg.alpha_composite(im)
    bg = bg.convert("RGB")
    return bg.resize((ANCHO, int(bg.height * ANCHO / bg.width)), Image.LANCZOS)


sel = sys.argv[1:]
filas = []
for nom, f, mk, dur, tm in PRUEBAS:
    if sel and nom not in sel:
        continue
    a, b = cuadro(f, tm, dur, mk), cuadro(f, dur - .45, dur, mk)
    fila = Image.new("RGB", (ANCHO * 2 + 10, a.height + 34), (24, 20, 18))
    fila.paste(a, (0, 34))
    fila.paste(b, (ANCHO + 10, 34))
    ImageDraw.Draw(fila).text((10, 8), f"{nom}  ·  mitad (t={tm})  |  final (t={dur - .45:.2f}, {len(mk)} marcas)",
                              fill=(230, 220, 190), font=E.fuente("r", 24))
    fila.save(os.path.join(AQUI, "previews", f"mg_{nom}.jpg"), quality=85)
    filas.append(fila)
if filas:
    H = sum(x.height for x in filas) + 8 * len(filas)
    hoja = Image.new("RGB", (filas[0].width, H), (12, 10, 9))
    y = 0
    for x in filas:
        hoja.paste(x, (0, y))
        y += x.height + 8
    hoja.save(os.path.join(AQUI, "previews", "mg_prueba_hoja.jpg"), quality=85)
print("ok", len(filas))
