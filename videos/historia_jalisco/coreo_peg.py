# -*- coding: utf-8 -*-
"""Atajos de coreografía con PEGATINAS DE FLOW (historia_jalisco): piezas por hoja y caminantes con ciclo real de Flow."""
import numpy as np

import mapa as M
from coreo_util import formacion
from motor import e_inout
from pegflow import P, Peg, ciclo

# hojas (número de pieza = el de piezas/<hoja>/_indice.jpg)
OC = lambda n, **k: P("01_occidente_hoja", n, **k)       # 0 pirámide redonda, 1 tumba de tiro, 2 figurilla mujer, 3 figurilla guerrero, 4 maqueta de aldea, 5 volcán, 6 agave, 7 sal y cestas
PU = lambda n, **k: P("02_pueblos_hoja", n, **k)         # 0 caxcán, 1 tecuexe, 2 coca, 3 wixárika, 4 purépecha, 5 mujer en el metate, 6 cihuapilli, 7 Tenamaxtli
CQ = lambda n, **k: P("03_conquista_hoja", n, **k)       # 0 Nuño de Guzmán, 1 Alvarado, 2 virrey Mendoza, 3 ballestero, 4 arcabucero, 5 tlaxcalteca, 6 choza en llamas, 7 hierro y cadenas
CO = lambda n, **k: P("04_colonia_hoja", n, **k)         # 0 catedral, 1 Hospicio Cabañas, 2 universidad, 3 hacienda, 4 mula con plata, 5 barril, 6 jarra, 7 cédula real, 8 rey
IN = lambda n, **k: P("05_independencia_hoja", n, **k)   # 0 Hidalgo, 1 Amo Torres, 2 Calleja, 3 insurgente, 10/11 cadena rota, 12 cañón, 13 puente con humo (2K)
XI = lambda n, **k: P("06_xix_hoja", n, **k)             # 0 Prisciliano Sánchez, 1 Juárez, 2 Guillermo Prieto, 3 niño, 4 soldado apuntando, 5 palacio, 6 libro, 7 pluma, 8 tren, 9 tranvía
XX = lambda n, **k: P("07_xx_hoja", n, **k)              # 0 cristero, 1 federal, 2 templo cerrado, 3 mariachi guitarrón, 4 mariachi trompeta, 5 charro a caballo, 6 cámara de cine, 7 estadio
HO = lambda n, **k: P("08_hoy_hoja", n, **k)             # 0 explosión, 1-4 edificios, 5 laptop, 6 chip, 7 futbolista con balón, 8 aficionado, 9 agaves, 10 Arcos, 11 joven (2K)
SI = lambda n, **k: P("09_simbolos_hoja", n, **k)        # 0 sombrero, 1 botella de tequila, 2 caballito, 3 jimador, 4 agave, 5 bailarina, 6 tortillas y olla, 7 casa de adobe, 8 cruz, 9 barca de Chapala

PERIODICO = Peg("05_independencia_hoja/periodico.png")   # del 1K: en 2K el papel blanco se parte
BALON = Peg("08_hoy_hoja/balon.png")                 # del 1K: en 2K queda pegado al futbolista
C_SOLDADO = ciclo("10_soldado_marcha")
C_CAXCAN = ciclo("11_caxcan_corre")
C_INSURG = ciclo("12_insurgente_marcha")
C_CRISTERO = ciclo("13_cristero_galope")


def andar_ciclo(R, frames, P_, t0, dur, t1=None, s=0.4, sem=0, z=1, zs=0.4, fps=9.0, flip=None, off=(0, 0), entra="pop", ease=e_inout,
                extra=(), sale="encoger"):
    """Caminante con el ciclo de Flow sobre el camino geográfico P_ (los cuadros miran a la derecha; flip si va al oeste)."""
    if flip is None:
        a, b = P_[0], P_[-1]
        flip = float(b[0]) < float(a[0])
    n = len(frames)
    return R.act(lambda t, k=sem: frames[int(t * fps + k * 3) % n], pos_geo=R.camino_pos(P_, t0, dur, ease=ease), off=off, s=s, t_in=t0,
                 d_in=0.4, entra=entra, sem=sem, sfx=list(extra), t_out=t1, sale=sale, zs=zs, z=z, flip=flip)


def grupo_ciclo(R, frames, P_, t0, dur, n=3, ancho=90, t1=None, s=0.4, sem=0, z=1, fps=9.0, desfase=0.12, flip=None, extra=()):
    return [andar_ciclo(R, frames, P_, t0 + desfase * k, dur, t1=t1, s=s, sem=sem + k, z=z, fps=fps, off=formacion(k, n, ancho), flip=flip,
                        extra=extra if k == 0 else ()) for k in range(n)]


def ciclo_pant(R, frames, x0, x1, y, t0, dur, t1=None, s=0.9, sem=0, z=3, fps=9.0):
    """Ciclo que cruza la pantalla (coordenadas de pantalla)."""
    n = len(frames)

    def pos(t):
        u = min(1.0, max(0.0, (t - t0) / dur))
        return (x0 + (x1 - x0) * u, y, s)
    return R.act(lambda t, k=sem: frames[int(t * fps + k * 3) % n], pos=pos, t_in=t0, d_in=0.3, entra="pop", sem=sem, t_out=t1, z=z,
                 flip=x1 < x0)
