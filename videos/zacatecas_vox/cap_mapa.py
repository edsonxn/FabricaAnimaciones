# -*- coding: utf-8 -*-
"""Capítulo 1 (escena `mapa`): mapa de papel de la Nueva España en 1546 y la Gran Chichimeca."""
import math

import numpy as np

import geo as G
import mapa_dib as M
import ui_vox as U
import vox as V
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, smooth, clamp01, h01

A = dict(
    mil=T("mapa", "Mil"), seis=T("mapa", "seis"), nueva=T("mapa", "Nueva"), ninguna=T("mapa", "ninguna"),
    cerros=T("mapa", "cerros"), nopales=T("mapa", "nopales"), nomadas=T("mapa", "nómadas"),
    siglos=T("mapa", "siglos"), zacatecos=T("mapa", "Zacatecos"), huachi=T("mapa", "huachichiles"),
    conq=T("mapa", "conquistadores"), chichi=T("mapa", "chichimecas"),
)
A["fin"] = FIN("mapa")


def alfa_mapa(z):
    """El mapa se desvanece cuando la cámara se acerca a Zacatecas (z de mundo entre 1.5 y 9)."""
    u = clamp01((math.log(max(z, 1e-6)) - math.log(1.6)) / (math.log(5.0) - math.log(1.6)))
    return 1.0 - smooth(u)


def _pop(t, t0, dur=0.32):
    return 0.0 if t < t0 else e_back(prog(t, t0, t0 + dur), 1.8)


def etiqueta(lz, t, t0, x, y, txt, z, px=27, fondo=V.CREMA, color=V.TINTA, a=1.0):
    k = _pop(t, t0)
    if k > 0.01:
        V.pastilla(lz, x, y, txt, px, k=k / z, fondo=fondo, color=color, alfa=a)


def dibujar(lz, t, z):
    """Dibuja el mapa en coordenadas de mundo. Llamar solo si alfa_mapa(z) > 0."""
    a = alfa_mapa(z)
    if a <= 0.01:
        return
    kt = e_back(prog(t, 0.0, 0.9), 1.5)
    M.mar(lz, alfa=a * smooth(prog(t, 0.0, 0.5)), z=z)
    M.tierra(lz, alfa=a * smooth(prog(t, 0.1, 0.7)))
    # Gran Chichimeca (se rellena al hablar de los nómadas)
    M.chichimeca(lz, alfa=a, frac=smooth(prog(t, A["nomadas"] - 0.2, A["nomadas"] + 0.9)))
    rotulos = z < 1.0
    reposo = t > A["fin"] + 1.0        # tras la primera vez, el mapa se muestra limpio (sin rótulos)
    M.sierras(lz, alfa=a, esc=1.0 / max(0.5, z) * 0.62, aparece=lambda i: _pop(t, A["cerros"] + i * 0.04, 0.3))
    M.nopales(lz, alfa=a, esc=1.0 / max(0.5, z) * 0.62, aparece=lambda i: _pop(t, A["nopales"] + i * 0.05, 0.3))
    # Ciudad de México (única ciudad grande) y "ninguna ciudad" al norte
    mx, my = G.xy(*G.CIUDADES["mexico"])
    if reposo:
        zx, zy = G.xy(*G.CIUDADES["zacatecas"])
        M.edificio_mexico(lz, mx, my + 4, 0.55 / max(z, 0.3) * 1.1, alfa=a)
        M.estrella(lz, zx, zy, 30 / max(z, 0.3), alfa=a, color=V.ROJO)
        return
    kn = _pop(t, A["nueva"] + 0.1)
    if kn > 0.01:
        M.edificio_mexico(lz, mx, my + 4, 0.55 / z * 1.1 * kn, alfa=a)
        etiqueta(lz, t, A["nueva"] + 0.5, mx + 40, my + 70 / z, "CIUDAD DE MÉXICO", z, px=24, a=a)
    # estrella de Zacatecas
    zx, zy = G.xy(*G.CIUDADES["zacatecas"])
    ke = _pop(t, A["chichi"] + 0.4, 0.45)
    if ke > 0.01:
        pulso = 1 + 0.14 * math.sin(t * 6)
        M.estrella(lz, zx, zy, 30 / z * ke * pulso, alfa=a, color=V.ROJO)
        etiqueta(lz, t, A["chichi"] + 0.9, zx, zy - 110 / z, "ZACATECAS", z, px=27, fondo=V.ROJO, color=V.CREMA, a=a)
    # anotación a mano: círculo alrededor del norte vacío + signos de pregunta
    fc = smooth(prog(t, A["ninguna"], A["ninguna"] + 1.2))
    if fc > 0.01:
        cx, cy = G.xy(-103.0, 25.0)
        V.circulo_mano(lz, cx, cy, 300, 340, fc, V.ROJO, 9 / z, seed=4)
        for i, (lon, lat) in enumerate([(-104.5, 26.6), (-102.0, 25.6), (-103.6, 23.9)]):
            k = _pop(t, A["ninguna"] + 0.5 + i * 0.2)
            if k > 0.01:
                qx, qy = G.xy(lon, lat)
                V.rotulo(lz, "?", qx, qy, 96, color=V.ROJO, k=k / z, sombra=0.0, fuente="vox_x")
    # los pueblos: pastillas con línea de llamada
    if t >= A["zacatecos"] and rotulos:
        px_, py_ = G.xy(-104.6, 24.3)
        k = _pop(t, A["zacatecos"])
        lz.trazo(np.array([[px_, py_], [px_ - 300, py_ - 80 / z]]), V.CREMA, 3 / z, afinar=False, temblor=0.0, capa=2)
        etiqueta(lz, t, A["zacatecos"], px_ - 300, py_ - 80 / z, "ZACATECOS", z, px=25, fondo=V.AMARILLO)
    if t >= A["huachi"] and rotulos:
        px_, py_ = G.xy(-100.9, 24.0)
        lz.trazo(np.array([[px_, py_], [px_ + 320, py_ + 20 / z]]), V.CREMA, 3 / z, afinar=False, temblor=0.0, capa=2)
        etiqueta(lz, t, A["huachi"], px_ + 320, py_ + 20 / z, "HUACHICHILES", z, px=25, fondo=V.AMARILLO)
    if t >= A["chichi"]:
        k = _pop(t, A["chichi"], 0.4)
        cx, cy = G.xy(-103.0, 22.6)
        V.marcador(lz, cx - 250, cy - 6, 500, 70 / z * 0.62, smooth(prog(t, A["chichi"] + 0.1, A["chichi"] + 0.7)) * k,
                   V.AMARILLO, seed=3)
        V.rotulo(lz, "CHICHIMECAS", cx, cy, 44, color=V.TINTA, k=k / z * 0.62 * 1.0, fuente="vox_x", sombra=0.0)


def ui(lz, t):
    """Titulares de pantalla (espacio de pantalla)."""
    cx = W / 2
    # titulares que se suceden sobre el mapa
    heads = [(A["nueva"] - 0.2, A["ninguna"] - 0.3, ["NUEVA ESPAÑA"]),
             (A["ninguna"] - 0.1, A["cerros"] - 0.2, ["AL NORTE:", "NINGUNA CIUDAD"]),
             (A["cerros"] - 0.1, A["nomadas"] - 0.3, ["CERROS SECOS", "Y NOPALES"]),
             (A["nomadas"] - 0.1, A["zacatecos"] - 0.2, ["PUEBLOS NÓMADAS"]),
             (A["zacatecos"] - 0.1, A["fin"] + 0.6, ["LOS “CHICHIMECAS”"])]
    for (t0, t1, lin) in heads:
        if t0 <= t < t1 + 0.3:
            k = e_back(prog(t, t0, t0 + 0.35), 1.6) * (1 - smooth(prog(t, t1, t1 + 0.3)))
            if k > 0.01:
                U.frase_grande(lz, lin, cx, 470, px=78, k=k, alfa=1.0, color=V.TINTA, marcador=len(lin) - 1 if len(lin) > 1 else 0)
