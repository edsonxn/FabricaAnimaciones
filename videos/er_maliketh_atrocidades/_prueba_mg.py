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
    ("retal", E.retal(remate="Y Maliketh los cosió a su servicio"), [0.4, 1.6, 4.4, 6.0], 8, 3.0),
    ("recambio", E.recambio(iconos=(_P("gurranq"), _P("d_cazador"), None)), [0.3, 2.4, 4.6], 8, 3.4),
    ("nombre_bestia", E.nombre_bestia(), [0.3, 2.0, 3.6, 6.4], 9, 2.8),
    ("jaula_orden", E.jaula_orden(), [0.3, 1.8, 3.6, 5.6], 8, 2.6),
    ("pruebas", E.pruebas(objetos=(("Aojo de puñal negro", "oculta la verdad de la conspiración", _P("cuchillo_negro")),
                                  ("Armadura de Cuchillo Negro", "númenes vinculadas a la propia Márika", _P("armadura_cuchillo")),
                                  ("Recuerdo de la Hoja Negra", "Aun así, ella lo traicionó", _P("recuerdo_espada_negra")))),
     [0.3, 1.3, 2.3, 3.6, 5.2], 8, 2.0),
    ("dos_muertes", E.dos_muertes(), [0.3, 2.2, 4.4], 7, 2.6),
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
