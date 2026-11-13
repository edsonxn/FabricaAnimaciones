# -*- coding: utf-8 -*-
"""Familia Septim para el árbol genealógico (mg_tes.arbol). Lo importa efectos.py; `python _arbol.py` saca la prueba
previews/arbol_prueba.jpg con todos a la vista."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import mg_tes as T  # noqa: E402


def _p(s):
    return os.path.join(AQUI, "pegatinas", s + ".png")


ALTO = (.5, .33, 2.4)        # retrato vertical de Flow (1024x1371): la cara en el tercio de arriba
PERSONAS = {
    "pelagio2": dict(n="Pelagio II", s="Emperador", img=_p("pelagio_ii"), x=.50, fila=0, foco=ALTO),
    "quintila": dict(n="Quintila", s="Hechicera de Camlorn", img=_p("quintila"), x=.72, fila=0, foco=ALTO),
    "antioco": dict(n="Antíoco", s="Medio hermano · emperador", img=_p("antioco"), x=.07, fila=1, foco=ALTO),
    "mantiarco": dict(n="Mantiarco", s="Rey de Soledad", img=_p("mantiarco"), x=.27, fila=1, foco=ALTO),
    "potema": dict(n="Potema", s="La Reina Loba", img=_p("potema_reina_joven"), x=.45, fila=1, foco=(.585, .29, 4.0)),
    "cefor": dict(n="Céforo", s="Rey de Gilane", img=_p("cefor_i"), x=.68, fila=1, foco=ALTO),
    "magnus": dict(n="Magnus", s="Rey de Lilmoth", img=_p("magnus"), x=.88, fila=1, foco=ALTO),
    "kintyra": dict(n="Kintyra II", s="Emperatriz a los 15", img=_p("kintyra_ii"), x=.07, fila=2, foco=(.5, .24, 2.2)),
    "bathorgh": dict(n="Bathorgh", s="Hijastro desterrado", img=_p("bathorgh"), x=.21, fila=2, foco=(.5, .34, 2.6)),
    "uriel": dict(n="Uriel III", s="El hijo de Potema", img=_p("uriel_iii_ob"), x=.36, fila=2, foco=(.52, .26, 3.2)),
    "pelagio3": dict(n="Pelagio III", s="El Loco", img=_p("pelagio_iii"), x=.78, fila=2, foco=(.5, .27, 1.8)),
    "katariah": dict(n="Katariah", s="Emperatriz dunmer", img=_p("katariah"), x=.95, fila=2, foco=(.56, .15, 2.0)),
}
LAZOS = [
    dict(t="pareja", a="pelagio2", b="quintila"),
    dict(t="hijos", de=["pelagio2"], a=["antioco"], punteado=True, lado=True, nota="de su primera esposa"),
    dict(t="hijos", de=["pelagio2", "quintila"], a=["potema", "cefor", "magnus"]),
    dict(t="pareja", a="mantiarco", b="potema"),
    dict(t="hijos", de=["mantiarco", "potema"], a=["uriel"]),
    dict(t="hijos", de=["mantiarco"], a=["bathorgh"], punteado=True),
    dict(t="hijos", de=["antioco"], a=["kintyra"]),
    dict(t="hijos", de=["magnus"], a=["pelagio3"]),
    dict(t="pareja", a="pelagio3", b="katariah"),
]
TITULO = "La familia Septim"


def arbol(pasos):
    return T.arbol(TITULO, PERSONAS, LAZOS, pasos)


if __name__ == "__main__":
    import numpy as np
    from PIL import Image
    fn = arbol([dict(ver=list(PERSONAS), tacha=["antioco", "kintyra"], foco=["potema", "uriel"], nota="Prueba: todos a la vista")])
    a = np.asarray(fn(3.0, 6.0, [0.2]))
    im = Image.fromarray(a[..., [2, 1, 0, 3]])
    bg = Image.new("RGBA", (1920, 1080), (60, 80, 60, 255))
    bg.alpha_composite(im, ((1920 - im.width) // 2, (1080 - im.height) // 2))
    bg.convert("RGB").save(os.path.join(AQUI, "previews", "arbol_prueba.jpg"), quality=90)
    print(im.size)
