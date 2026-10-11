# -*- coding: utf-8 -*-
"""Coreografía (2/3): revolución amarniense, Ramsés II, decadencia y Alejandro Magno."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402

COL = M.COL
CIU = M.CIUDADES


def lugar(R, t0, t1, txt, geo, off=(0, -60), px=52, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _revolucion(R)
    _ramses(R)
    _decadencia(R)
    _alejandro(R)


# ------------------------------------------------------------------ 6. REVOLUCIÓN (Akenatón, Nefertiti y Tutankamón)
def _revolucion(R):
    e = "revolucion"
    i0 = INI(e)
    t_cincuenta = T(e, "cincuenta")
    t_akenaton = T(e, "akenaton")
    t_prohibe = T(e, "prohibe")
    t_aton = T(e, "aton")
    t_capital = T(e, "capital")
    t_nefertiti = T(e, "nefertiti")
    t_sacerdotes = T(e, "sacerdotes")
    t_borran = T(e, "borran")
    t_tutankamon = T(e, "tutankamon")
    t_oro = T(e, "oro")

    R.terreno(i0 - 0.2, "reino_nuevo", COL["amarna"], 1.3)
    R.camara(i0 - 0.2, 30.9, 27.50, 4.4) # Amarna (Akhetaten)
    R.camara(t_aton - 0.2, 30.9, 27.50, 4.4)
    R.camara(t_sacerdotes - 0.2, 32.64, 25.68, 4.4) # Retorno a Tebas
    R.camara(t_tutankamon - 0.2, 32.64, 25.68, 4.8) # Valle de los Reyes

    R.anio(i0, -1353)
    R.anio(t_tutankamon, -1332)

    # Sello de dinastía: Herejía de Amarna
    R.sello(t_akenaton, "ATÓN", "CULTO SOLAR", COL["amarna"])

    # El disco solar de Atón descendiendo con rayos y manos de vida
    R.act(Bb.disco_aton(), geo=CIU["amarna"], off=(0, -40), s=0.52,
          t_in=t_aton - 0.3, d_in=0.6, entra="pop", sem=150,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.6)], t_out=t_sacerdotes - 0.2, sale="encoger", z=1)
    lugar(R, t_aton, t_nefertiti - 0.2, "ATÓN: EL CULTO SOLAR", CIU["amarna"], off=(0, 140), px=50)

    # Akenatón y la reina Nefertiti con su célebre corona azul alta
    R.act(personaje_egipcio("faraon", corona="khepresh", mirada=1.0), geo=CIU["amarna"], off=(-80, 50), s=0.48,
          t_in=t_akenaton - 0.2, d_in=0.5, entra="pop", sem=151,
          sfx=[(0, "pop", 0.5)], t_out=t_sacerdotes - 0.2, sale="encoger", z=2)
    R.act(personaje_egipcio("reina", corona="nefertiti", piel=PIEL_CL, mirada=-1.0), geo=CIU["amarna"], off=(80, 50), s=0.48,
          t_in=t_nefertiti - 0.2, d_in=0.5, entra="pop", sem=152,
          sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.4)], t_out=t_sacerdotes - 0.2, sale="encoger", z=2)
    lugar(R, t_nefertiti, t_sacerdotes - 0.3, "AKENATÓN Y NEFERTITI", CIU["amarna"], off=(0, 160), px=48)

    # La deslumbrante máscara de oro de Tutankamón
    R.act(Bb.mascara_tutankamon(), geo=CIU["tebas"], off=(0, 30), s=0.58,
          t_in=t_tutankamon - 0.3, d_in=0.7, entra="pop", sem=153,
          sfx=[(0, "pop", 0.5), (0.2, "brillo", 0.7)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_tutankamon, FIN(e), "MÁSCARA DE TUTANKAMÓN (ORO MACIZO)", CIU["tebas"], off=(0, -180), px=52)


# ------------------------------------------------------------------ 7. RAMSÉS II (Kadesh y Abu Simbel)
def _ramses(R):
    e = "ramses"
    i0 = INI(e)
    t_sube = T(e, "sube")
    t_ramses = T(e, "ramses")
    t_setenta = T(e, "setenta")
    t_combate = T(e, "combate")
    t_kadesh = T(e, "kadesh")
    t_tratado = T(e, "tratado")
    t_paz = T(e, "paz")
    t_colosos = T(e, "colosos")
    t_abu = T(e, "abu")
    t_sesenta = T(e, "sesenta")

    R.terreno(i0 - 0.2, "reino_nuevo", COL["ramses"], 1.4)
    R.camara(i0 - 0.2, 32.5, 28.5, 3.2)
    R.camara(t_combate - 0.3, 36.52, 34.56, 4.2) # Kadesh en Siria
    R.camara(t_tratado - 0.2, 35.5, 33.5, 3.8)
    R.camara(t_abu - 0.3, 31.62, 22.34, 4.4)    # Abu Simbel en Nubia
    R.camara(FIN(e), 31.62, 22.34, 3.8)

    R.anio(i0, -1279)
    R.anio(t_kadesh, -1274)
    R.anio(t_sesenta, -1213)

    # Sello de dinastía: Dinastía XIX / Ramsés el Grande
    R.sello(t_ramses, "XIX", "RAMSÉS II EL GRANDE", COL["ramses"])

    # Ramsés II montado en su carro de guerra real hacia Kadesh
    R.act(Bb.carro_faraon(), geo=CIU["kadesh"], off=(0, 20), s=0.55,
          t_in=t_combate - 0.2, d_in=0.6, entra="pop", sem=160,
          sfx=[(0, "pop", 0.5), (0.2, "fanfarria", 0.6)], t_out=t_tratado - 0.2, sale="encoger", z=2)
    lugar(R, t_combate, t_tratado - 0.3, "BATALLA DE KADESH (1274 a.C.)", CIU["kadesh"], off=(0, -170), px=52)

    # La tablilla del Tratado de Paz de Kadesh
    R.act(Bb.tratado_paz_kadesh(), geo=(35.5, 33.5), off=(0, 20), s=0.52,
          t_in=t_tratado - 0.2, d_in=0.5, entra="pop", sem=161,
          sfx=[(0, "pop", 0.5), (0.1, "escribir", 0.5)], t_out=t_abu - 0.2, sale="encoger", z=2)
    lugar(R, t_paz, t_abu - 0.3, "PRIMER TRATADO DE PAZ DE LA HISTORIA", (35.5, 33.5), off=(0, -160), px=50)

    # Los colosos de Abu Simbel excavados en la roca nubia
    R.act(Bb.abu_simbel_fachada(), geo=CIU["abu_simbel"], off=(0, 20), s=0.58,
          t_in=t_abu - 0.3, d_in=0.7, entra="pop", sem=162,
          sfx=[(0, "pop", 0.5), (0.2, "tambor", 0.6)], t_out=FIN(e), sale="encoger", z=1)
    lugar(R, t_abu, FIN(e), "TEMPLO DE ABU SIMBEL (66 AÑOS DE REINADO)", CIU["abu_simbel"], off=(0, -180), px=50)


# ------------------------------------------------------------------ 8. DECADENCIA (Invasiones y conquista persa)
def _decadencia(R):
    e = "decadencia"
    i0 = INI(e)
    t_siglos = T(e, "siglos")
    t_fragmenta = T(e, "fragmenta")
    t_invasiones = T(e, "invasiones")
    t_nubios = T(e, "nubios")
    t_asirios = T(e, "asirios")
    t_quinientos = T(e, "quinientos")
    t_persas = T(e, "persas")
    t_apagan = T(e, "apagan")

    # Fragmentación y conquista persa
    R.terreno(i0 - 0.2, "unificado", COL["tardio"], 1.3)
    R.camara(i0 - 0.2, 32.0, 28.5, 2.7)
    R.camara(t_invasiones - 0.2, 32.0, 28.2, 2.7)
    R.camara(t_persas - 0.2, 31.25, 29.85, 4.2) # Menfis tomada por Cambises II

    R.anio(i0, -1069)
    R.anio(t_quinientos, -525)

    # Soldado egipcio defensor con escudo y lanza
    R.act(personaje_egipcio("guerrero", corona=None, mirada=1.0, cetro=False), geo=(31.8, 30.2), off=(-60, 40), s=0.50,
          t_in=t_invasiones - 0.2, d_in=0.5, entra="pop", sem=170,
          sfx=[(0, "pop", 0.5), (0.1, "golpe_suave", 0.4)], t_out=t_persas - 0.2, sale="encoger", z=2)
    lugar(R, t_invasiones, t_persas - 0.3, "PUEBLOS DEL MAR Y ASIRIOS", (31.8, 30.2), off=(-180, 40), px=44)

    # Faraón nubio de la Dinastía XXV con corona de dos uraeus
    R.act(personaje_egipcio("faraon", corona="hedjet", piel=(140, 85, 60), mirada=-1.0), geo=CIU["tebas"], off=(70, 30), s=0.48,
          t_in=t_nubios - 0.2, d_in=0.5, entra="pop", sem=171,
          sfx=[(0, "pop", 0.5)], t_out=t_persas - 0.2, sale="encoger", z=2)
    lugar(R, t_nubios, t_persas - 0.3, "DINASTÍA XXV NUBIA", CIU["tebas"], off=(-200, 30), px=44)

    # Guerrero persa aqueménida con lanza y tiara almenada
    R.act(personaje_egipcio("guerrero", corona="turbante", piel=PIEL_CL, mirada=-1.0, cetro=False),
          geo=CIU["menfis"], off=(0, 40), s=0.54,
          t_in=t_persas - 0.2, d_in=0.5, entra="pop", sem=172,
          sfx=[(0, "cuerno", 0.5), (0.1, "tambor", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_persas, FIN(e), "CONQUISTA PERSA (CAMBISES II, 525 a.C.)", CIU["menfis"], off=(0, -160), px=52)


# ------------------------------------------------------------------ 9. ALEJANDRO MAGNO Y PTOLOMEO
def _alejandro(R):
    e = "alejandro"
    i0 = INI(e)
    t_trescientos = T(e, "trescientos")
    t_alejandro = T(e, "alejandro")
    t_coronan = T(e, "coronan")
    t_alejandria = T(e, "alejandria")
    t_faro = T(e, "faro")
    t_biblioteca = T(e, "biblioteca")
    t_ptolomeo = T(e, "ptolomeo")
    t_griegos = T(e, "griegos")

    R.terreno(i0 - 0.2, "ptolomeo", COL["ptolomeo"], 1.4)
    R.camara(i0 - 0.2, 30.5, 30.5, 3.2)
    R.camara(t_alejandro - 0.2, 29.92, 31.15, 4.4) # Alejandría
    R.camara(t_faro - 0.2, 29.92, 31.15, 4.4)      # Puerto y Faro
    R.camara(t_biblioteca - 0.2, 29.92, 31.15, 4.4)# Gran Biblioteca
    R.camara(t_ptolomeo - 0.2, 29.92, 31.15, 4.2)

    R.anio(i0, -332)
    R.anio(t_alejandria, -331)
    R.anio(t_ptolomeo, -305)

    # Sello de dinastía: Dinastía Ptolemaica
    R.sello(t_ptolomeo, "PTO", "DINASTÍA PTOLEMAICA", COL["ptolomeo"])

    # Alejandro Magno con casco griego y clámide macedonia
    R.act(personaje_egipcio("faraon", corona="casco_griego", piel=PIEL_CL, mirada=1.0),
          geo=CIU["alejandria"], off=(-90, 40), s=0.52,
          t_in=t_alejandro - 0.2, d_in=0.5, entra="pop", sem=180,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.6)], t_out=t_faro - 0.2, sale="encoger", z=2)
    lugar(R, t_alejandro, t_faro - 0.3, "ALEJANDRO MAGNO ENTRA EN EGIPTO (332 a.C.)", CIU["alejandria"], off=(-50, -170), px=52)

    # El Faro de Alejandría alzándose sobre las olas del Mediterráneo
    R.act(C.faro_alejandria(), geo=CIU["alejandria"], off=(-150, 40), s=0.52,
          t_in=t_faro - 0.3, d_in=0.6, entra="pop", sem=181,
          sfx=[(0, "pop", 0.5), (0.2, "brillo", 0.6)], t_out=t_ptolomeo - 0.2, sale="encoger", z=1)
    lugar(R, t_faro, t_ptolomeo - 0.3, "EL FARO DE ALEJANDRÍA", CIU["alejandria"], off=(-150, -170), px=46)

    # La Gran Biblioteca de Alejandría
    R.act(C.biblioteca_alejandria(), geo=CIU["alejandria"], off=(150, 40), s=0.48,
          t_in=t_biblioteca - 0.2, d_in=0.6, entra="pop", sem=182,
          sfx=[(0, "pop", 0.5)], t_out=t_ptolomeo - 0.2, sale="encoger", z=1)
    lugar(R, t_biblioteca, t_ptolomeo - 0.3, "LA GRAN BIBLIOTECA", CIU["alejandria"], off=(150, 150), px=46)

    # Dinastía de los Ptolomeos: faraón griego con corona doble
    R.act(personaje_egipcio("faraon", corona="pschent", piel=PIEL_CL, mirada=1.0),
          geo=CIU["alejandria"], off=(0, 40), s=0.54,
          t_in=t_ptolomeo - 0.2, d_in=0.5, entra="pop", sem=183,
          sfx=[(0, "pop", 0.5), (0.1, "fanfarria", 0.5)], t_out=FIN(e), sale="encoger", z=2)
    lugar(R, t_ptolomeo, FIN(e), "DINASTÍA PTOLEMAICA", CIU["alejandria"], off=(0, -160), px=52)
