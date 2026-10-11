# -*- coding: utf-8 -*-
"""Coreografía parte 3/3: Máxima Extensión, Crisis del Siglo III, División y Caída/Legado."""
import math
import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_roma as RO
from obj_roma import *
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402

COL = M.COL


def pop(R, dib, t, pos=None, geo=None, off=(0, 0), s=1.0, snd="pop", vol=0.6, **k):
    sfx = [(0.0, snd, vol)] if snd else []
    if pos is not None:
        return R.act(dib, pos=pos, t_in=t, sfx=sfx, s=s, **k)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t, sfx=sfx, **k)


def lugar(R, t0, t1, txt, geo, off=(0, -55), px=52, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _maxima(R)
    _crisis(R)
    _division(R)
    _caida(R)


# ------------------------------------------------------------------ 9. MÁXIMA EXTENSIÓN (Trajano 117 d.C.)
def _maxima(R):
    e = "maxima"
    i0 = INI(e)
    t_117 = T(e, "ciento")
    t_trajano = T(e, "trajano")
    t_imperio = T(e, "imperio")
    t_gloria = T(e, "gloria")
    t_extiende = T(e, "extiende")
    t_britania = T(e, "britania")
    t_arabia = T(e, "arabia")
    t_atlantico = T(e, "atlántico")
    t_eufrates = T(e, "éufrates")

    R.camara(i0, 13.8, 41.2, 1.55)
    R.camara(t_trajano, 14.5, 42.0, 1.35)
    R.camara(t_britania, -1.5, 52.5, 1.45)
    R.camara(t_eufrates, 38.0, 35.5, 1.45)
    R.camara(FIN(e), 17.5, 41.5, 1.2)

    # Año 117 d.C.
    R.anio(t_117 - 0.2, 117)
    R.terreno(t_trajano - 0.2, "maxima", COL["maxima"], 2.2)
    R.snd(t_trajano, "fanfarria", 0.75)

    # El emperador Trajano con armadura dorada y cetro
    pop(R, RO.cesar_emperador, t_trajano, pos=(360, 720), s=0.98, sem=90, snd="pop", t_out=FIN(e) + 0.5, sale="encoger")

    # Etiquetas de los extremos del Imperio
    lugar(R, t_britania - 0.1, FIN(e) + 0.4, "BRITANIA", (-1.5, 52.5), off=(0, -35), px=52)
    pop(R, RO.castrum_fort, t_britania + 0.2, geo=(-1.5, 51.5), off=(0, 20), s=0.48, sem=91, snd="pop", t_out=FIN(e) + 0.4, sale="encoger")

    lugar(R, t_arabia - 0.1, FIN(e) + 0.4, "ARABIA PÉTREA", (36.0, 29.5), off=(0, 40), px=50)
    lugar(R, t_eufrates - 0.1, FIN(e) + 0.4, "MESOPOTAMIA (Río Éufrates)", (42.0, 34.5), off=(0, -35), px=52)
    pop(R, RO.anfora_vino, t_eufrates + 0.2, geo=(40.0, 34.0), off=(0, 20), s=0.55, sem=93, snd="ding", t_out=FIN(e) + 0.4, sale="encoger")

    # Patrulla de caballería custodiando el limes
    pop(R, lambda t: RO.jinete_romano(int(t * 5)), t_extiende + 0.2, pos=(1560, 680), s=0.78, sem=94, snd="galope", t_out=FIN(e) + 0.4, sale="encoger")

    # Corona triunfal de laurel en lo alto
    pop(R, RO.corona_laurel, t_gloria - 0.1, pos=(1020, 225), s=0.72, sem=95, snd="brillo", t_out=FIN(e) + 0.5, sale="encoger")
    R.texto(t_117, FIN(e) + 0.5, "MÁXIMA EXTENSIÓN (117 d. C.)", (1020, 95), px=66, d=0.8)
    R.texto(t_extiende, FIN(e) + 0.5, "Desde Britania hasta el Éufrates y Arabia", (1020, 155), px=46, d=0.6)


# ------------------------------------------------------------------ 10. CRISIS DEL SIGLO III
def _crisis(R):
    e = "crisis"
    i0 = INI(e)
    t_territorio = T(e, "territorio")
    t_defender = T(e, "defender")
    t_tercero = T(e, "tercero")
    t_peste = T(e, "peste")
    t_guerras = T(e, "guerras")
    t_emperadores = T(e, "emperadores")
    t_colapso = T(e, "colapso")
    t_germanos = T(e, "germánicos")
    t_fronteras = T(e, "fronteras")
    t_rin = T(e, "rin")
    t_danubio = T(e, "danubio")

    R.camara(i0, 17.5, 41.5, 1.2)
    R.camara(t_tercero, 14.0, 44.0, 1.35)
    R.camara(t_rin, 10.5, 48.0, 1.6)
    R.camara(t_danubio, 18.0, 46.0, 1.5)
    R.camara(FIN(e), 15.0, 43.0, 1.3)

    # Año 235-284 d.C.
    R.anio(t_tercero - 0.2, 235)
    R.anio(t_colapso + 0.4, 284)

    # Los ríos frontera se tiñen de rojo amenaza
    R.rio(M.RIO_RIN, t_rin - 0.3, 1.8, color=(180, 50, 50), ancho=20)
    R.rio(M.RIO_DANUBIO, t_danubio - 0.3, 2.2, color=(180, 50, 50), ancho=20)
    lugar(R, t_rin, FIN(e) + 0.4, "Limes del Rin", (7.8, 50.0), off=(-55, -25), px=44)
    lugar(R, t_danubio, FIN(e) + 0.4, "Limes del Danubio", (19.5, 46.5), off=(0, -25), px=44)

    # Guerreros bárbaros atacando las fronteras
    pop(R, RO.barbaro_german, t_germanos - 0.2, geo=(8.5, 51.5), off=(0, 20), s=0.72, sem=100, snd="impacto", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.barbaro_german, t_germanos + 0.2, geo=(16.5, 48.5), off=(0, 20), s=0.68, sem=101, snd="impacto", t_out=FIN(e) + 0.4, sale="encoger")
    pop(R, RO.barbaro_german, t_germanos + 0.5, geo=(22.5, 47.0), off=(0, 20), s=0.65, sem=102, snd="impacto", t_out=FIN(e) + 0.4, sale="encoger")

    # Voronoi: el imperio se agrieta en caudillos y provincias rebeldes
    R.romper("barbaros", t_tercero, t_tercero + 0.8, t_colapso + 0.5, t_colapso + 1.8, gap=18, deriva=40, nervio=1.5)
    R.snd(t_tercero, "crujido", 0.9, dur=1.2)
    R.snd(t_guerras, "espada", 0.8)
    R.snd(t_colapso, "impacto", 0.8)

    # Caudillos militares y anarquía
    R.texto(t_tercero, FIN(e) + 0.4, "CRISIS DEL SIGLO III (235-284 d. C.)", (960, 95), px=72, d=0.7)
    R.texto(t_emperadores, FIN(e) + 0.4, "Más de 20 emperadores en 50 años", (960, 155), px=52, d=0.6)


# ------------------------------------------------------------------ 11. DIVISIÓN (Diocleciano y Constantino)
def _division(R):
    e = "division"
    i0 = INI(e)
    t_salvar = T(e, "gobernar")
    t_dividir = T(e, "dividirlo")
    t_mitades = T(e, "mitades")
    t_occidente = T(e, "occidente")
    t_oriente = T(e, "oriente")
    t_constantino = T(e, "constantino")
    t_capital = T(e, "capital")
    t_este = T(e, "este")
    t_constantinopla = T(e, "constantinopla")
    t_enriquece = T(e, "enriquece")
    t_desangra = T(e, "desangra")

    R.camara(i0, 15.0, 43.0, 1.3)
    R.camara(t_dividir, 18.0, 40.0, 1.32)
    R.camara(t_constantino, 28.5, 41.2, 1.7)
    R.camara(t_constantinopla, 29.0, 41.0, 1.85)
    R.camara(FIN(e), 20.0, 39.5, 1.25)

    # Año 330 (Constantinopla) y 395 (División formal)
    R.anio(t_constantino - 0.2, 330)
    R.anio(t_enriquece, 395)

    # División del mapa: Occidente en rojo vino, Oriente en azul bizantino
    R.terreno(t_dividir - 0.2, "occidente", COL["occidente"], 1.8)
    R.snd(t_dividir, "crujido", 0.7, dur=0.9)

    # Constantinopla en el Bósforo
    lugar(R, t_constantinopla - 0.2, FIN(e) + 0.5, "CONSTANTINOPLA", (28.98, 41.01), off=(0, -35), px=42)
    pop(R, RO.templo_romano, t_constantinopla, geo=(28.98, 41.01), off=(0, 20), s=0.48, sem=110, snd="brillo", t_out=FIN(e) + 0.5, sale="encoger")
    pop(R, lambda t: RO.galera_romana(int(t * 4)), t_constantinopla + 0.3, geo=(29.5, 40.5), off=(30, 20), s=0.42, sem=111, t_out=FIN(e) + 0.5, sale="encoger")

    # Emperador Constantino
    pop(R, RO.cesar_emperador, t_constantino, pos=(1560, 720), s=0.94, sem=112, snd="fanfarria", t_out=FIN(e) + 0.5, sale="encoger")

    # Rótulos de las dos mitades
    R.texto(t_occidente - 0.1, FIN(e) + 0.5, "IMPERIO DE OCCIDENTE", (450, 310), px=48, d=0.7)
    R.texto(t_occidente + 0.3, FIN(e) + 0.5, "(Capital: Roma / Rávena)", (450, 360), px=34, d=0.5)

    R.texto(t_oriente - 0.1, FIN(e) + 0.5, "IMPERIO DE ORIENTE", (1480, 310), px=48, d=0.7)
    R.texto(t_oriente + 0.3, FIN(e) + 0.5, "(Capital: Constantinopla)", (1480, 360), px=34, d=0.5)
    R.snd(t_oriente, "escribir", 0.6)


# ------------------------------------------------------------------ 12. CAÍDA Y LEGADO ETERNO
def _caida(R):
    e = "caida"
    i0 = INI(e)
    t_476 = T(e, "cuatrocientos")
    t_ultimo = T(e, "último")
    t_depuesto = T(e, "depuesto")
    t_colapsa = T(e, "colapsa")
    t_sobrevivira = T(e, "sobrevivirá")
    t_bizantino = T(e, "bizantino")
    t_murió = T(e, "murió")
    t_leyes = T(e, "leyes")
    t_arte = T(e, "arte")
    t_vivos = T(e, "vivos")

    R.camara(i0, 20.0, 39.5, 1.25)
    R.camara(t_476, 15.0, 41.5, 1.35)
    R.camara(t_colapsa, 16.0, 40.0, 1.25)
    R.camara(t_bizantino, 22.0, 38.5, 1.3)
    R.camara(t_vivos - 0.2, 16.0, 40.0, 1.15)
    R.camara(FIN(e), 16.0, 40.0, 1.15)

    # Año 476 d.C.: deposición del último emperador
    R.anio(t_476 - 0.2, 476)
    R.snd(t_476, "reloj_rapido", 0.55, dur=1.2)

    # Caída del emperador Rómulo Augústulo: cae de su trono
    emperador_cae = R.act(persona(ROJO_ROMA, PIEL, "corona", "asombro", (20, 140), 0, traje="tunica"),
                          pos=(520, 720), s=0.92, t_in=t_ultimo - 0.1, d_in=0.4, entra="pop", sem=120, snd=[(0, "pop", 0.5)],
                          t_out=t_depuesto + 0.2, sale="caer", d_out=1.0)
    R.snd(t_depuesto, "impacto", 0.75)

    # Caudillo bárbaro (Odoacro) tomando Roma
    pop(R, RO.barbaro_german, t_depuesto + 0.1, pos=(360, 720), s=0.94, sem=121, snd="impacto", t_out=t_murió, sale="encoger")

    # Occidente se desvanece, Oriente permanece azul y dorado por 1000 años
    R.terreno(t_colapsa - 0.2, "oriente", COL["oriente"], 2.2)
    R.texto(t_bizantino - 0.2, FIN(e) + 0.5, "IMPERIO BIZANTINO", (1420, 370), px=52, d=0.6)
    R.texto(t_bizantino + 0.1, FIN(e) + 0.5, "(Oriente sobrevive +1000 años)", (1420, 425), px=36, d=0.5)
    pop(R, RO.templo_romano, t_bizantino, geo=(28.98, 41.01), off=(0, 20), s=0.55, sem=123, snd="brillo", t_out=FIN(e) + 0.5)

    # El legado eterno de Roma: el Coliseo, las calzadas, las leyes y el águila SPQR
    pop(R, RO.coliseo, t_murió, pos=(420, 720), s=0.82, sem=124, snd="pop", t_out=FIN(e) + 1.2)
    pop(R, RO.arco_triunfo, t_leyes, pos=(740, 720), s=0.78, sem=125, snd="pop", t_out=FIN(e) + 1.2)
    pop(R, RO.estandarte_spqr, t_arte, pos=(1200, 720), s=0.88, sem=126, snd="impacto", t_out=FIN(e) + 1.2)
    pop(R, RO.corona_laurel, t_vivos - 0.2, pos=(1520, 680), s=0.95, sem=127, snd="brillo", t_out=FIN(e) + 1.2)

    # Título final glorioso
    R.texto(t_vivos - 0.2, FIN(e) + 1.2, "EL LEGADO ETERNO DE ROMA", (960, 160), px=84, d=0.9)
    R.texto(t_vivos + 0.4, FIN(e) + 1.2, "Leyes · Idiomas · Arquitectura · Civilización", (960, 245), px=66, d=0.7)
    R.snd(t_vivos, "fanfarria", 0.8)
