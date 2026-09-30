# -*- coding: utf-8 -*-
"""Coreografía (3/3): safávidas, Nader Sha y los qayares, petróleo y Pahlavi, revolución y hoy, cierre y cambios de escena."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_p as P
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402
from coreo_i1 import campo_extra, lugar, pop
from trans import SFX, Transicion
from boceto import T as TRAZO

COL = M.COL
PURPURA = P.PURPURA


def construir(R):
    _safavidas(R)
    _qayar(R)
    _pahlavi(R)
    _moderna(R)
    _cierre(R)
    _transiciones(R)


def _tachon():
    return Dib([TRAZO(linea((-150, 30), (150, -30)), 12, peso=0.05), TRAZO(linea((-150, -30), (150, 30)), 12, peso=0.05)])


# ------------------------------------------------------------------ SAFÁVIDAS
def _safavidas(R):
    e = "safavidas"
    i0 = INI(e)
    t_1501, t_adol, t_14, t_procl, t_ismail, t_safa = T(e, "quinientos"), T(e, "adolescente"), T(e, "catorce"), T(e, "proclama"), T(e, "ismail"), T(e, "safavida")
    t_conv, t_chii, t_relig, t_unir, t_iran = T(e, "impone"), T(e, "rama"), T(e, "religion"), T(e, "unir"), T(e, "iran")
    t_abas, t_isf, t_mezq, t_azul, t_jard, t_baz = T(e, "abas"), T(e, "isfahan", frase=2), T(e, "mezquitas"), T(e, "azulejos"), T(e, "jardines"), T(e, "bazares")
    t_mitad, t_mundo, t_alf, t_vend, t_eur = T(e, "mitad"), T(e, "mundo"), T(e, "alfombras"), T(e, "venden"), T(e, "europa")
    R.terreno(t_procl - 0.3, "safavidas", COL["safavidas"], 1.7)
    R.sello(t_safa + 0.05, "ص", "Safávidas", color=(40, 100, 150))
    R.camara(i0 - 0.3, 52.0, 34.0, 1.9)
    R.camara(t_procl, 51.0, 33.5, 2.0)
    R.camara(t_conv, 48.0, 36.5, 2.4)
    R.camara(t_abas - 0.3, 51.7, 32.8, 2.8)
    R.camara(t_mitad, 51.7, 32.8, 3.0)
    R.camara(t_alf, 44.0, 36.0, 1.6)
    R.camara(FIN(e), 38.0, 38.0, 1.65)
    R.anio(i0, 1258)
    R.anio(t_1501 - 0.3, 1258)
    R.anio(t_1501 + 0.8, 1501)
    R.anio(t_abas, 1501)
    R.anio(t_abas + 0.8, 1598)
    # un adolescente de catorce años
    R.act(persona(P.AZUL_TILE, PIEL_OSC, "taj", "feliz", (30, 110), 0, bigote=True, traje="tunica", faja=ORO, cuello=ORO), pos=(1400, 800, 0.85), t_in=t_adol - 0.1, d_in=0.45,
          entra="pop", sem=200, sfx=[(0, "pop", 0.6)], t_out=t_conv - 0.2, sale="encoger", z=1)
    R.texto(t_ismail - 0.05, t_conv - 0.3, "ISMAIL I", (1400, 490), px=80, d=0.6)
    R.contador(t_14 - 0.3, t_14 + 0.7, 0, 14, (700, 330), px=130, formato="{} años")
    R.snd(t_14 - 0.2, "reloj_rapido", 0.45, dur=1.0)
    # chiismo: religión oficial; vuelve a unir Irán
    R.act(P.mezquita(), geo=(46.3, 38.08), off=(0, 40), s=0.42, t_in=t_chii - 0.1, d_in=0.6, entra="pluma", sem=201, sfx=[(0, "crece", 0.45, {"dur": 0.7})], t_out=t_abas - 0.2, sale="encoger", zs=0.5)
    lugar(R, t_chii, t_abas - 0.3, "TABRIZ", (46.3, 38.08), off=(0, -230), px=54)
    R.texto(t_chii, t_abas - 0.3, "CHIISMO", (960, 190), px=96, d=0.7)
    R.act(A.estrella5(36), geo=(51.7, 32.6), off=lambda t: (0, -60 + 8 * math.sin(t * 4)), s=1.0, t_in=t_unir, d_in=0.4, entra="pop", sem=202, sfx=[(0, "bling", 0.5)], t_out=t_abas - 0.2, sale="encoger", zs=0.5, z=2)
    # Isfahán con el sha Abás
    R.act(P.mezquita(), geo=(51.67, 32.65), off=(0, 80), s=0.6, t_in=t_abas + 0.2, d_in=0.7, entra="pluma", sem=203, sfx=[(0, "crece", 0.5, {"dur": 0.8})], t_out=t_alf - 0.2, sale="encoger", zs=0.5, z=1)
    R.act(persona(ROJO_CH, PIEL_OSC, "taj", "feliz", (30, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), geo=(51.67, 32.65), off=(330, 120), s=0.66, t_in=t_abas - 0.1, d_in=0.45, entra="pop",
          sem=204, sfx=[(0, "pop", 0.6)], t_out=t_alf - 0.2, sale="encoger", zs=0.4, z=2)
    R.texto(t_abas, t_alf - 0.3, "SHA ABÁS", (1500, 300), px=76, d=0.6)
    lugar(R, t_isf, t_alf - 0.3, "ISFAHÁN", (51.67, 32.65), off=(0, -330), px=86)
    for k in range(5):
        R.act(A.estrella5(20), geo=(51.67, 32.65), off=(-260 + 130 * k, 130 + 10 * (k % 2)), s=0.9, t_in=t_azul + 0.1 * k, d_in=0.3, entra="pop", sem=205 + k, sfx=[(0, "tick", 0.4, {"tono": 1.0 + 0.1 * k})],
              t_out=t_alf - 0.2, sale="encoger", zs=0.4, z=2)
    R.texto(t_azul, t_jard - 0.1, "AZULEJOS", (500, 760), px=64, d=0.6)
    for k, (dx, c) in enumerate(((-330, VERDE_OSC), (-250, VERDE_CL), (-170, VERDE_OSC))):
        R.act(A.mijo_planta(), geo=(51.67, 32.65), off=(dx, 200), s=0.9, t_in=t_jard + 0.12 * k, d_in=0.4, entra="pop", sem=210 + k, sfx=[(0, "pop", 0.4)] if k == 0 else [], t_out=t_alf - 0.2, sale="encoger", zs=0.4)
    R.texto(t_baz - 0.1, t_mitad - 0.2, "BAZARES", (1500, 780), px=64, d=0.6)
    R.act(P.alfombra(), pos=(1500, 960, 0.5), t_in=t_baz, d_in=0.45, entra="pop", sem=213, sfx=[(0, "pop", 0.5)], t_out=t_alf - 0.2, sale="encoger", z=2)
    # la mitad del mundo y las alfombras viajan a Europa
    R.texto(t_mitad - 0.1, t_alf - 0.3, "LA MITAD DEL MUNDO", (960, 190), px=86, d=1.0)
    R.snd(t_mitad, "escribir", 0.5, dur=1.0)
    Pe = R.ruta([(51.7, 32.6), (44.0, 36.0), (34.0, 39.5), (26.0, 41.0), (22.0, 44.0)], t_alf - 0.1, 2.0, ancho=6.0)
    for k in range(2):
        R.act(P.alfombra(), pos_geo=R.camino_pos(Pe, t_vend + 0.25 * k, 2.4, ease=lambda u: u), off=(0, -20 - 14 * k), s=0.3, t_in=t_vend - 0.05 + 0.25 * k, d_in=0.3, entra="pop", sem=214 + k,
              sfx=[(0, "whoosh", 0.4, {"dur": 1.4})] if k == 0 else [], t_out=FIN(e) + 0.3, sale="encoger", zs=0.5, z=2)
    lugar(R, t_eur, FIN(e), "EUROPA", (23.5, 44.0), off=(0, 40), px=64)


# ------------------------------------------------------------------ NADER SHA Y LOS QAYARES, PETRÓLEO
def _qayar(R):
    e = "qayar"
    i0 = INI(e)
    t_nader, t_conq, t_delhi, t_trono, t_pavo = T(e, "nader"), T(e, "conquista"), T(e, "delhi"), T(e, "trono"), T(e, "pavo")
    t_suc, t_qay, t_pier, t_terr, t_rusia, t_imp, t_brit = T(e, "sucesores"), T(e, "qayares"), T(e, "pierden"), T(e, "terreno"), T(e, "rusia"), T(e, "imperio"), T(e, "britanico")
    t_1906, t_revo, t_obl, t_const, t_parl = T(e, "novecientos", frase=2), T(e, "revolucion"), T(e, "obliga"), T(e, "constitucion"), T(e, "parlamento")
    t_1908, t_brota, t_petr, t_des = T(e, "novecientos", frase=3), T(e, "brota"), T(e, "petroleo"), T(e, "desierto")
    R.camara(i0 - 0.3, 51.0, 33.5, 2.0)
    R.camara(t_conq - 0.2, 62.0, 33.5, 1.9)
    R.camara(t_delhi, 72.0, 30.5, 2.2)
    R.camara(t_trono, 68.0, 31.5, 1.8)
    R.camara(t_suc - 0.2, 53.0, 36.0, 1.55)
    R.camara(t_rusia, 50.0, 38.0, 1.6)
    R.camara(t_1906 - 0.3, 51.4, 35.7, 2.4)
    R.camara(t_1908 - 0.3, 50.0, 32.0, 2.6)
    R.camara(t_brota + 0.4, 49.3, 32.0, 3.6)
    R.camara(FIN(e), 49.3, 32.0, 3.5)
    R.anio(i0, 1598)
    R.anio(t_nader - 0.2, 1598)
    R.anio(t_nader + 0.9, 1736)
    R.anio(t_delhi - 0.3, 1736)
    R.anio(t_delhi + 0.6, 1739)
    R.anio(t_suc, 1739)
    R.anio(t_suc + 1.0, 1813)
    R.anio(t_1906 - 0.3, 1813)
    R.anio(t_1906 + 0.6, 1906)
    R.anio(t_1908 - 0.3, 1906)
    R.anio(t_1908 + 0.6, 1908)
    # Nader Sha llega a Delhi y trae el Trono del Pavo Real
    R.act(persona((96, 100, 116), PIEL_OSC, "kolah", "enojo", (20, 140), 0, barba=NEGRO, traje="armadura", acc_d="espada"), pos=(1400, 820, 0.8), t_in=t_nader - 0.1, d_in=0.45, entra="pop", sem=220,
          sfx=[(0, "pop", 0.6)], t_out=t_conq + 0.3, sale="encoger", z=1)
    R.texto(t_nader, t_conq + 0.2, "NADER SHA", (1400, 500), px=76, d=0.6)
    R.rio(M.RUTA_NADER, t_conq - 0.1, 2.4, (170, 70, 70), ancho=12, t1=t_trono + 0.5)
    R.snd(t_conq, "pincel", 0.5, dur=2.0)
    R.act(lambda t: Bb.jinete(int(t * 8), (96, 100, 116), "kolah", True, False, "enojo"), pos_geo=R.camino_pos(M.RUTA_NADER, t_conq + 0.1, 2.4, ease=lambda u: u), off=(0, -18), s=0.3,
          t_in=t_conq, d_in=0.3, entra="pop", sem=221, sfx=[(0, "galope", 0.4, {"dur": 2.4})], t_out=t_delhi + 0.3, sale="encoger", zs=0.6, z=2)
    lugar(R, t_delhi - 0.1, t_trono + 0.4, "DELHI", (77.2, 28.6), off=(0, -60), px=64)
    R.act(A.estallido(12, 30, 100), geo=(77.2, 28.6), off=(0, -20), s=0.7, t_in=t_delhi, d_in=0.12, entra="fija", sem=222, sfx=[(0, "explosion", 0.5)], t_out=t_delhi + 0.4, sale="cortar", z=3, zs=0.5)
    R.act(P.trono_pavo(), geo=(77.2, 28.6), off=(0, 20), s=0.65, t_in=t_trono - 0.05, d_in=0.5, entra="pop", sem=223, sfx=[(0, "pop", 0.6), (0.1, "bling", 0.6)], t_out=t_trono + 0.8, sale="encoger", zs=0.5, z=1)
    Rv = [(77.2, 28.6), (75.0, 31.6), (72.0, 33.8), (69.2, 34.5), (68.0, 33.0), (65.7, 31.6), (63.0, 34.6), (59.6, 36.3)]
    R.act(P.trono_pavo(), pos_geo=R.camino_pos(Rv, t_pavo + 0.2, 2.2, ease=lambda u: u), off=(0, 20), s=0.35, t_in=t_trono + 0.8, d_in=0.3, entra="pop", sem=224, sfx=[(0, "whoosh", 0.4, {"dur": 1.6})],
          t_out=t_suc - 0.1, sale="encoger", zs=0.5, z=2)
    R.texto(t_pavo, t_suc - 0.2, "TRONO DEL PAVO REAL", (960, 190), px=84, d=1.0)
    R.snd(t_pavo, "escribir", 0.5, dur=1.0)
    # los qayares pierden terreno ante Rusia y el Imperio británico
    R.terreno(t_pier - 0.2, "qayar", COL["qayar"], 1.8)
    R.sello(t_qay + 0.05, "ق", "Qayares", color=(170, 70, 60))
    R.act(persona(PURPURA, PIEL_OSC, "kolah", "normal", (30, 30), 0, bigote=True, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1500, 820, 0.85), t_in=t_suc - 0.1, d_in=0.45, entra="pop", sem=225,
          sfx=[(0, "pop", 0.6)], t_out=t_1906 - 0.2, sale="encoger", z=1)
    R.ruta([(47.0, 50.0), (46.0, 45.0), (46.5, 40.5)], t_rusia - 0.3, 1.0, ancho=7.0, t1=t_1906 - 0.3)
    lugar(R, t_rusia, t_1906 - 0.3, "RUSIA", (47.0, 47.5), off=(0, 0), px=70)
    R.ruta([(72.0, 22.0), (66.0, 25.0), (59.0, 26.5)], t_brit - 0.4, 1.2, ancho=7.0, t1=t_1906 - 0.3)
    R.act(C.ingles(0), geo=(66.0, 25.5), off=(0, 40), s=0.55, t_in=t_brit - 0.2, d_in=0.45, entra="pop", sem=226, sfx=[(0, "pop", 0.5)], t_out=t_1906 - 0.2, sale="encoger", zs=0.5, z=1)
    lugar(R, t_brit - 0.1, t_1906 - 0.3, "IMPERIO BRITÁNICO", (68.0, 23.0), off=(0, 0), px=54)
    # 1906: constitución y parlamento
    R.act(P.parlamento(), pos=(1000, 840, 1.15), t_in=t_parl - 0.3, d_in=0.6, entra="pop", sem=227, sfx=[(0, "pop", 0.6), (0.2, "bling", 0.5)], t_out=t_1908 - 0.3, sale="encoger", z=1)
    R.act(A.rollo_escritura(3), pos=(520, 780, 0.9), t_in=t_const - 0.1, d_in=0.5, entra="pop", sem=228, sfx=[(0, "pop", 0.6), (0.2, "papel", 0.6)], t_out=t_1908 - 0.3, sale="encoger", z=2)
    R.texto(t_const - 0.1, t_1908 - 0.3, "CONSTITUCIÓN", (960, 190), px=90, d=0.9)
    R.snd(t_const, "escribir", 0.5, dur=0.9)
    # 1908: brota petróleo
    R.act(lambda t: P.torre_petroleo(int(t * 8)), geo=(49.3, 32.0), off=(0, 120), s=1.0, t_in=t_brota - 0.3, d_in=0.6, entra="pluma", sem=229, sfx=[(0, "crece", 0.5, {"dur": 0.6}), (0.5, "chorro", 0.6, {"dur": 2.4})],
          t_out=FIN(e) + 0.4, sale="encoger", zs=0.5, z=1)
    R.texto(t_petr - 0.1, FIN(e) + 0.2, "PETRÓLEO", (960, 200), px=110, d=0.8)
    R.snd(t_petr, "escribir", 0.5, dur=0.8)
    for k in range(3):
        R.act(P.barril(), geo=(49.3, 32.0), off=(-240 + 110 * k, 140), s=0.9, t_in=t_des + 0.15 * k, d_in=0.4, entra="pop", sem=230 + k, sfx=[(0, "pop", 0.5)] if k == 0 else [], t_out=FIN(e) + 0.4, sale="encoger", zs=0.4)
    lugar(R, t_des, FIN(e), "MASYED SOLEIMÁN", (49.3, 32.0), off=(0, 230), px=50)


# ------------------------------------------------------------------ PAHLAVI
def _pahlavi(R):
    e = "pahlavi"
    i0 = INI(e)
    t_petr, t_pot, t_disp = T(e, "petroleo"), T(e, "potencias"), T(e, "disputan")
    t_1925, t_ofi, t_cor, t_pahl = T(e, "novecientos", frase=1), T(e, "oficial"), T(e, "corona"), T(e, "pahlavi")
    t_1935, t_pide, t_pers, t_nombre, t_iran = T(e, "novecientos", frase=2), T(e, "pide"), T(e, "persia"), T(e, "nombre"), T(e, "iran")
    t_1951, t_nac = T(e, "novecientos", frase=3), T(e, "nacionaliza")
    t_dos, t_golpe, t_eeuu, t_reino, t_derr = T(e, "dos"), T(e, "golpe"), T(e, "estados"), T(e, "reino"), T(e, "derriba")
    R.terreno(t_petr - 0.4, "pahlavi", COL["pahlavi"], 1.5)
    R.camara(i0 - 0.3, 49.3, 32.0, 3.4)
    R.camara(t_pot, 52.0, 33.5, 2.3)
    R.camara(t_1925 - 0.2, 51.39, 35.69, 2.6)
    R.camara(t_1935, 53.0, 33.5, 2.1)
    R.camara(t_1951 - 0.2, 50.0, 32.0, 2.4)
    R.camara(t_golpe - 0.3, 51.39, 35.69, 2.6)
    R.camara(FIN(e), 51.39, 35.69, 2.5)
    R.anio(i0, 1908)
    R.anio(t_1925 - 0.3, 1908)
    R.anio(t_1925 + 0.8, 1925)
    R.anio(t_1935 - 0.2, 1925)
    R.anio(t_1935 + 0.8, 1935)
    R.anio(t_1951 - 0.2, 1935)
    R.anio(t_1951 + 0.7, 1951)
    R.anio(t_golpe - 0.3, 1951)
    R.anio(t_golpe + 0.6, 1953)
    # las potencias se disputan el petróleo
    R.act(P.barril(), pos=(960, 830, 1.2), t_in=t_petr - 0.1, d_in=0.45, entra="pop", sem=240, sfx=[(0, "pop", 0.6)], t_out=t_1925 - 0.2, sale="encoger", z=1)
    R.act(lambda t: C.ingles(int(t * 3)), pos=lambda t: (lerp(-200, 560, e_out(prog(t, t_pot - 0.2, t_pot + 0.6))), 830, 0.85), t_in=t_pot - 0.2, d_in=0.01, entra="fija", sem=241, sfx=[(0.3, "pasos", 0.3, {"dur": 0.6})],
          t_out=t_1925 - 0.2, sale="encoger", z=1)
    R.act(persona(ROJO_OSC, PIEL_OSC, "gorro", "enojo", (30, 30), 1, traje="corta", bigote=True), pos=lambda t: (lerp(2100, 1360, e_out(prog(t, t_pot - 0.1, t_pot + 0.7))), 830, 0.85),
          t_in=t_pot - 0.1, d_in=0.01, entra="fija", sem=242, t_out=t_1925 - 0.2, sale="encoger", z=1, flip=True)
    R.texto(t_pot - 0.1, t_1925 - 0.3, "¿DE QUIÉN ES?", (960, 200), px=90, d=0.9)
    R.snd(t_disp, "bocinazo", 0.3)
    # 1925: un oficial se corona
    R.act(persona((150, 140, 108), PIEL_OSC, "gorra_oficial", "serio", (20, 20), 0, bigote=True, traje="corta", faja=ORO), pos=(960, 830, 0.95), t_in=t_ofi - 0.1, d_in=0.45, entra="pop", sem=243,
          sfx=[(0, "pop", 0.6)], t_out=t_1935 - 0.2, sale="encoger", z=1)
    R.act(A.cetro_corona(1.0), pos=lambda t: (960, lerp(250, 480, e_out(prog(t, t_cor, t_cor + 0.8))), 1.0), t_in=t_cor - 0.05, d_in=0.3, entra="pop", sem=244, sfx=[(0, "bling", 0.6)],
          t_out=t_1935 - 0.2, sale="encoger", z=2)
    R.sello(t_pahl + 0.05, "پ", "Pahlavi", color=(130, 90, 140))
    R.texto(t_pahl - 0.1, t_1935 - 0.3, "DINASTÍA PAHLAVI", (960, 190), px=86, d=1.0)
    R.snd(t_pahl, "escribir", 0.5, dur=1.0)
    # 1935: Persia -> Irán
    R.texto(t_pers - 0.1, t_nombre + 1.5, "PERSIA", (620, 380), px=120, d=0.6)
    R.act(_tachon(), pos=(620, 395, 1.0), t_in=t_nombre - 0.3, d_in=0.4, entra="pluma", sem=245, sfx=[(0, "garabato", 0.6, {"dur": 0.6})], t_out=t_1951 - 0.3, sale="encoger", z=3)
    R.texto(t_iran - 0.05, t_1951 - 0.3, "IRÁN", (1260, 500), px=190, d=0.7)
    R.snd(t_iran, "escribir", 0.6, dur=0.7)
    R.act(A.estrella5(40), pos=lambda t: (1560, 330 + 10 * math.sin(t * 4), 1.2), t_in=t_iran + 0.6, d_in=0.4, entra="pop", sem=246, sfx=[(0, "bling", 0.5)], t_out=t_1951 - 0.3, sale="encoger", z=2)
    # 1951: nacionalización; 1953: golpe
    R.act(persona(AZUL_IMP, PIEL_OSC, "pelo", "feliz", (30, 110), 0, traje="tunica", faja=ORO, bigote=True), pos=(700, 830, 0.85), t_in=t_1951 - 0.1, d_in=0.45, entra="pop", sem=247,
          sfx=[(0, "pop", 0.6)], t_out=t_dos + 0.2, sale="encoger", z=1)
    R.act(P.barril(), pos=(1250, 840, 1.1), t_in=t_nac - 0.1, d_in=0.4, entra="pop", sem=248, sfx=[(0, "pop", 0.6), (0.1, "sello", 0.6)], t_out=t_dos + 0.2, sale="encoger", z=1)
    R.texto(t_nac - 0.1, t_dos + 0.2, "PETRÓLEO NACIONAL", (960, 200), px=86, d=1.0)
    R.snd(t_nac, "escribir", 0.5, dur=1.0)
    for k, x in enumerate((420, 640, 1280, 1500)):
        R.act(lambda t, k=k: C.soldado_fusil(int(t * 3) + k), pos=lambda t, x=x, k=k: (lerp(x + (900 if x > 960 else -900), x, e_out(prog(t, t_golpe - 0.3, t_golpe + 0.5))), 850, 0.7),
              t_in=t_golpe - 0.3, d_in=0.01, entra="fija", sem=250 + k, sfx=[(0, "pasos", 0.3, {"dur": 0.8})] if k == 0 else [], t_out=FIN(e) + 0.4, sale="encoger", z=1, flip=x > 960)
    R.act(A.estallido(14, 40, 120), pos=(960, 640, 1.2), t_in=t_derr - 0.05, d_in=0.15, entra="fija", sem=254, sfx=[(0, "explosion", 0.6)], t_out=t_derr + 0.5, sale="cortar", z=3)
    R.texto(t_golpe - 0.1, FIN(e) + 0.3, "GOLPE DE ESTADO · 1953", (960, 190), px=80, d=1.2)
    R.snd(t_golpe, "escribir", 0.5, dur=1.0)
    R.texto(t_eeuu - 0.1, FIN(e) + 0.3, "EE. UU. + REINO UNIDO", (960, 290), px=56, d=1.1)


# ------------------------------------------------------------------ REVOLUCIÓN Y HOY
def _moderna(R):
    e = "moderna"
    i0 = INI(e)
    t_desc, t_crece, t_1979, t_revo, t_derr = T(e, "descontento"), T(e, "crece"), T(e, "setenta"), T(e, "revolucion"), T(e, "derroca")
    t_procl, t_rep, t_isl, t_ayat, t_jom = T(e, "proclama"), T(e, "republica"), T(e, "islamica"), T(e, "ayatola"), T(e, "jomeini")
    t_est, t_guerra, t_ocho, t_irak, t_muer = T(e, "estalla"), T(e, "guerra"), T(e, "ocho"), T(e, "irak"), T(e, "muertos")
    t_hoy, t_nov, t_mill, t_pers = T(e, "hoy"), T(e, "noventa"), T(e, "millones"), T(e, "personas")
    t_prim, t_now, t_ano, t_fiesta, t_tres = T(e, "primavera"), T(e, "nouruz"), T(e, "ano"), T(e, "fiesta"), T(e, "tres", frase=4)
    R.terreno(t_1979 - 0.2, "iran", COL["iran"], 1.6)
    R.camara(i0 - 0.3, 51.39, 35.69, 2.5)
    R.camara(t_1979, 51.39, 35.69, 2.7)
    R.camara(t_procl, 52.5, 34.0, 2.3)
    R.camara(t_est - 0.3, 49.0, 33.5, 2.4)
    R.camara(t_ocho, 47.8, 33.3, 2.8)
    R.camara(t_hoy - 0.3, 53.5, 32.5, 2.0)
    R.camara(t_prim - 0.3, 53.0, 33.0, 2.3)
    R.camara(FIN(e), 53.0, 33.0, 2.25)
    R.anio(i0, 1953)
    R.anio(t_1979 - 0.3, 1953)
    R.anio(t_1979 + 0.6, 1979)
    R.anio(t_est - 0.2, 1979)
    R.anio(t_est + 0.6, 1980)
    R.anio(t_ocho + 1.0, 1988)
    R.anio(t_hoy - 0.2, 1988)
    R.anio(t_hoy + 0.8, 2026)
    # descontento creciente: multitudes con pancartas
    for k, x in enumerate((360, 660, 960, 1260, 1560)):
        R.act(P.pancarta(), pos=(x, 880 - 20 * (k % 2), 0.75), t_in=t_crece - 0.6 + 0.12 * k, d_in=0.45, entra="sube", dy=300, sem=260 + k, sfx=[(0, "pop", 0.4)] if k == 0 else [], t_out=t_procl - 0.2, sale="encoger", z=1)
        R.act(A.multitud(6, 10 + k), pos=(x, 950, 0.75), t_in=t_crece - 0.5 + 0.12 * k, d_in=0.45, entra="pop", sem=270 + k, t_out=t_procl - 0.2, sale="encoger", z=2)
    R.snd(t_crece, "tambor", 0.5, dur=1.2)
    R.act(C.avion(), pos=lambda t: (lerp(400, 2300, e_in(prog(t, t_derr - 0.1, t_derr + 1.6))), lerp(520, 300, prog(t, t_derr - 0.1, t_derr + 1.6)), 0.8, -0.18), t_in=t_derr - 0.1, d_in=0.01,
          entra="fija", sem=280, sfx=[(0, "whoosh", 0.5, {"dur": 1.8})], t_out=t_derr + 1.7, sale="cortar", z=3)
    R.texto(t_revo - 0.1, t_procl - 0.3, "REVOLUCIÓN", (960, 190), px=100, d=0.8)
    R.snd(t_revo, "escribir", 0.5, dur=0.8)
    # República Islámica
    R.act(persona(NEGRO, PIEL_CL, "turbante_negro", "serio", (20, 20), 0, barba=(236, 236, 240), traje="tunica", faja=None, cuello=CREMA), pos=(1450, 820, 0.9), t_in=t_ayat - 0.1, d_in=0.45, entra="pop", sem=281,
          sfx=[(0, "pop", 0.6)], t_out=t_est - 0.2, sale="encoger", z=1)
    R.texto(t_rep - 0.1, t_est - 0.3, "REPÚBLICA ISLÁMICA", (960, 190), px=84, d=1.0)
    R.snd(t_rep, "escribir", 0.5, dur=1.0)
    R.texto(t_jom, t_est - 0.3, "JOMEINI", (1450, 490), px=70, d=0.6)
    # guerra con Irak
    campo_extra(R, "irak", (196, 98, 82), t_irak - 0.3, d=0.9, alfa=0.9)
    R.act(A.espadas(), geo=(47.8, 33.3), off=(0, 0), s=1.0, t_in=t_est, d_in=0.3, entra="pop", sem=282, sfx=[(0, "impacto", 0.7)], t_out=t_hoy - 0.3, sale="encoger", zs=0.5, z=2)
    for k, (lon, lat) in enumerate(((46.6, 33.9), (48.6, 32.4), (47.2, 31.0))):
        R.act(lambda t, k=k: C.humo(int(t * 6) + k), geo=(lon, lat), off=(0, -30), s=1.0, t_in=t_guerra + 0.15 * k, d_in=0.3, entra="pop", sem=283 + k, peg=False, sfx=[(0, "canonazo", 0.4)] if k != 1 else [],
              t_out=t_hoy - 0.3, sale="encoger", zs=0.5, z=2)
    lugar(R, t_irak, t_hoy - 0.3, "IRAK", (43.6, 33.0), off=(0, 0), px=70)
    R.texto(t_ocho - 0.1, t_hoy - 0.3, "8 AÑOS", (960, 190), px=110, d=0.7)
    # hoy: noventa millones; Nowruz
    R.terreno(t_hoy - 0.2, "iran", COL["iran"], 1.0)
    R.contador(t_nov - 0.4, t_nov + 1.3, 0, 89000000, (960, 240), px=110)
    R.snd(t_nov - 0.3, "reloj_rapido", 0.45, dur=1.6)
    R.texto(t_mill + 0.2, t_prim - 0.3, "habitantes", (960, 340), px=64, d=0.5)
    R.act(A.multitud(10, 3), pos=(960, 900, 1.4), t_in=t_pers - 0.2, d_in=0.5, entra="pop", sem=290, sfx=[(0, "pop", 0.5)], t_out=t_prim - 0.25, sale="encoger", z=1)
    R.act(P.haft_sin(), pos=(960, 850, 1.45), t_in=t_now - 0.2, d_in=0.6, entra="pop", sem=291, sfx=[(0, "pop", 0.7), (0.15, "bling", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.texto(t_now - 0.1, FIN(e) + 0.2, "NOWRUZ", (960, 190), px=120, d=0.8)
    R.snd(t_now, "escribir", 0.5, dur=0.8)
    for k in range(5):
        R.act(A.estrella5(26), pos=lambda t, k=k: (360 + 300 * k, 470 + 14 * math.sin(t * 3 + k), 1.0), t_in=t_ano + 0.12 * k, d_in=0.3, entra="pop", sem=292 + k, sfx=[(0, "tick", 0.4, {"tono": 1.0 + 0.12 * k})],
              t_out=FIN(e) + 0.4, sale="encoger", z=2)
    R.texto(t_fiesta - 0.1, FIN(e) + 0.2, "más de 3.000 años", (960, 330), px=84, d=1.0)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_cay, t_camb, t_relig, t_cult, t_viva = T(e, "cayeron"), T(e, "cambiaron"), T(e, "religiones"), T(e, "cultura"), T(e, "viva")
    t_pais, t_cinco, t_min, t_coment = T(e, "pais"), T(e, "cinco"), T(e, "minutos"), T(e, "comentarios")
    R.terreno(i0 - 0.2, "iran", COL["iran"], 0.6)
    R.romper("cierre", t_cay - 0.05, t_cay + 0.4, t_camb + 0.3, t_relig + 0.5, colores=None, gap=12, deriva=34)
    R.romper("cierre", t_cult - 0.4, t_cult - 0.05, t_viva - 0.3, t_viva + 0.3, colores=None, gap=14, deriva=44, nervio=1.4)
    R.snd(t_cay - 0.05, "crujido", 0.9, dur=0.7)
    R.snd(t_relig + 0.5, "boing", 0.7)
    R.snd(t_cult - 0.4, "crujido", 0.9, dur=0.7)
    R.snd(t_viva + 0.1, "gong", 0.6)
    R.camara(i0, 53.0, 33.0, 2.1)
    R.camara(t_viva, 53.0, 33.0, 2.0)
    R.camara(t_pais, 50.0, 33.0, 1.6)
    R.camara(FIN(e), 48.0, 33.0, 1.45)
    R.anio(t_cay, 2026)
    R.texto(t_cult - 0.1, t_pais - 0.2, "CULTURA PERSA", (960, 200), px=104, d=1.0)
    R.snd(t_cult, "escribir", 0.5, dur=0.9)
    paises = [(30.5, 27.0), (34.0, 39.0), (22.8, 39.3), (77.0, 24.0), (44.0, 24.0), (69.5, 30.0), (68.0, 47.0)]
    for k, (lon, lat) in enumerate(paises):
        R.act(A.signo_pregunta(), geo=(lon, lat), off=lambda t, k=k: (0, -16 + 12 * math.sin(t * 4 + k)), s=0.72, t_in=t_pais + 0.14 * k, d_in=0.4, entra="pop", sem=300 + k,
              sfx=[(0, "pluck", 0.5, {"tono": (1.0, 1.125, 1.26, 1.5, 1.68, 2.0, 2.25)[k]})], zs=0.3, z=1)
    R.texto(t_min, FIN(e) + 1.0, "¿cuál sigue?", (960, 200), px=112, d=0.9)
    R.act(C.boton_suscribir(), pos=lambda t: (960, 800 + 4 * math.sin(t * 5), 1.0), t_in=t_coment - 0.6, d_in=0.5, entra="pop", sem=310, sfx=[(0, "pop", 0.7), (0.1, "bling", 0.6)], z=2)
    R.texto(t_coment - 0.4, FIN(e) + 1.0, "SUSCRÍBETE", (960, 800), px=76, d=0.7)
    R.act(C.campana(), pos=lambda t: (1270, 790, 0.8, 0.35 * math.sin((t - t_coment) * 9) * math.exp(-(t - t_coment) * 0.4)), t_in=t_coment - 0.3, d_in=0.4, entra="pop", sem=311,
          sfx=[(0, "pop", 0.6), (0.1, "campana", 0.6)], z=2)
    R.act(C.globo_dialogo(), pos=(1470, 520, 1.1), t_in=t_coment - 0.1, d_in=0.45, entra="pop", sem=312, sfx=[(0, "pop", 0.6)], z=2)
    R.texto(t_coment, FIN(e) + 1.0, "...", (1470, 500), px=92, d=0.4)


# ------------------------------------------------------------------ CAMBIOS DE ESCENA (procedurales, sin cortes)
def _transiciones(R):
    ids = ["gancho", "meseta", "ciro", "dario", "alejandro", "partos", "sasanidas", "islam", "mongoles", "safavidas", "qayar", "pahlavi", "moderna", "cierre"]
    spec = [
        ("tinta", COL["meseta"], (960, 170), (1000, 620)),
        ("puntos", COL["medos"], (960, 540), (960, 540)),
        ("pincel", COL["aquemenida"], (960, 540), (960, 540)),
        ("portal", COL["alejandro"], (1640, 800), (520, 820)),
        ("rollo", COL["partos"], (960, 540), (960, 540)),
        ("papel", COL["sasanidas"], (960, 540), (960, 540)),
        ("ola", COL["califato"], (960, 540), (960, 540)),
        ("portal", COL["mongol"], (1000, 800), (700, 820)),
        ("persianas", COL["safavidas"], (960, 540), (960, 540)),
        ("tinta", (62, 56, 74), (1000, 700), (960, 540)),
        ("pincel", COL["qayar"], (960, 540), (960, 540)),
        ("papel", COL["pahlavi"], (960, 540), (960, 540)),
        ("ola", (186, 214, 216), (960, 540), (960, 540)),
    ]
    for k, (tipo, color, a, b) in enumerate(spec):
        tc = (FIN(ids[k]) + INI(ids[k + 1])) / 2
        R.trans.append(Transicion(tc, tipo, color, a, b, dur=0.8, seed=k + 1))
        R.snd(tc - 0.36, SFX[tipo], 0.55, dur=0.8) if SFX[tipo] in ("pincel", "zoom_whoosh", "ola") else R.snd(tc - 0.36, SFX[tipo], 0.55)
