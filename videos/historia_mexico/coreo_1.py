# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (pirámides en la selva, Tenochtitlan sobre el lago, el choque de dos mundos, maíz, cacao y plata),
orígenes (domesticación del maíz hace 7.000 años, los olmecas en La Venta y San Lorenzo, cabezas colosales, los zapotecas en Monte Albán),
el Periodo Clásico (Teotihuacán y la Calzada de los Muertos, las ciudades-estado mayas de Palenque, Calakmul y Chichén Itzá, el cero maya,
el colapso clásico) y el ascenso de los mexicas (Tula tolteca, la migración náhuatl, el águila sobre el nopal en 1325, Tenochtitlan,
las chinampas y la Triple Alianza).
Capas de territorio: 0 = cultura principal en el centro/golfo, 1 = zapotecas / mayas / Tlaxcala, 50 = lago de Texcoco (agua)."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_mx1 as M1
import obj_mx2 as M2
import obj_mx3 as M3
from core import FIN, INI, T, kf, linea_punteada
from coreo_util import CI, COL, andar, ciudad, formacion, ga, grupo, lugar, mece, pa, titulo
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog

ARENA_TXT = (146, 110, 72)
SELVA_TXT = (76, 118, 82)
MAR_TXT = (58, 108, 148)


def cortes(R):
    pass


def construir(R):
    _mares(R)
    _gancho(R)
    _origenes(R)
    _clasico(R)
    _mexicas(R)


def _mares(R):
    R.mar("mx", "GOLFO DE MÉXICO", -90.5, 25.0, 42, 0.44, color=MAR_TXT)
    R.mar("mx", "OCÉANO PACÍFICO", -111.5, 18.2, 46, 0.44, rot=-0.38, color=MAR_TXT)
    R.mar("mx", "MAR CARIBE", -83.2, 18.2, 36, 0.42, color=MAR_TXT)
    R.mar("mx", "GOLFO DE CALIFORNIA", -111.8, 27.6, 22, 0.40, rot=-0.92, color=MAR_TXT)
    R.mar("mx", "PENÍNSULA DE YUCATÁN", -89.2, 19.6, 22, 0.34, color=SELVA_TXT)
    R.mar("mx", "SIERRA MADRE OCCIDENTAL", -105.8, 25.4, 24, 0.32, rot=-0.88, color=ARENA_TXT)
    R.mar("mx", "SIERRA MADRE ORIENTAL", -99.6, 24.4, 22, 0.30, rot=-0.85, color=ARENA_TXT)
    R.mar("mx", "ALTIPLANO CENTRAL", -100.2, 20.6, 22, 0.32, color=ARENA_TXT)
    R.mar("mx", "DESIERTO DE SONORA", -112.5, 31.2, 26, 0.32, color=ARENA_TXT)
    R.mar("mx", "DESIERTO DE CHIHUAHUA", -104.8, 29.5, 26, 0.32, color=ARENA_TXT)
    R.mar("mx", "MESOAMÉRICA", -94.5, 16.5, 30, 0.32, color=SELVA_TXT)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    t_pir, t_sel, t_ciu, t_lag, t_cho, t_dos, t_mun = (T(e, "piramides"), T(e, "selva"), T(e, "ciudades"), T(e, "lago"),
                                                       T(e, "choque"), T(e, "dos"), T(e, "mundos"))
    t_sal, t_maiz, t_cac, t_pla, t_com, t_nac, t_cie, t_per = (T(e, "salieron"), T(e, "maiz"), T(e, "cacao"), T(e, "plata"),
                                                               T(e, "comercio"), T(e, "nacion"), T(e, "ciento"), T(e, "personas"))
    t_esta, t_hist, t_mex, t_cinco, t_min = T(e, "esta"), T(e, "historia"), T(e, "mexico"), T(e, "cinco"), T(e, "minutos")

    # cámara: península maya y selva -> Valle de México y lago -> vista general de México
    R.camara(0.0, -90.4, 18.8, 3.6)
    R.camara(t_ciu - 0.1, -90.8, 18.9, 3.5)
    R.camara(t_lag, -98.9, 19.48, 5.4)
    R.camara(t_cho + 0.3, -97.6, 19.35, 3.8)
    R.camara(t_maiz + 0.2, -99.5, 20.8, 2.3)
    R.camara(t_mex, -101.8, 23.6, 1.55)
    R.camara(FIN(e) + 0.6, -101.5, 23.4, 1.50)

    # el lago de Texcoco brilla desde el inicio en el Valle de México
    R.terreno(0.0, "lago_texcoco", M.AGUA_LAGO, 0.2, capa=50)

    # frase 0: pirámides entre la selva, ciudades sobre un lago y el choque de dos mundos
    ga(R, M2.piramide_kukulcan(), CI["chichen_itza"], 0.0, t_sal, s=0.46, off=(0, 20), sem=1, zs=0.45, z=2, entra="sube", dy=320,
       extra=[(0.05, "crece", 0.45, {"dur": 0.9})])
    ga(R, M2.piramide_kukulcan(), CI["palenque"], 0.18, t_sal, s=0.38, off=(-40, 20), sem=2, zs=0.45, z=1, entra="sube", dy=280)
    for k, (g, dx, dy) in enumerate(((CI["chichen_itza"], -150, 30), (CI["chichen_itza"], 150, 25), (CI["palenque"], 110, 30), (CI["calakmul"], 0, 20))):
        ga(R, M3.palmera_selva(210 + 20 * (k % 2)), g, 0.05 + 0.08 * k, t_sal, s=0.34, off=(dx, dy), sem=3 + k, zs=0.4, z=1)
    ga(R, lambda t: M3.jaguar(int(t * 4) % 4), CI["calakmul"], t_sel - 0.1, t_sal, s=0.32, off=(-90, 40), sem=7, zs=0.4, z=2)
    lugar(R, t_sel, t_ciu - 0.15, "LA SELVA MAYA", CI["palenque"], off=(0, 95), px=44)

    # Tenochtitlan sobre el lago + canoas
    ga(R, M2.templo_mayor(), CI["tenochtitlan"], t_ciu - 0.1, t_sal, s=0.48, off=(0, -10), sem=8, zs=0.5, z=2, entra="sube", dy=340,
       extra=[(0.05, "crece", 0.45)])
    ga(R, M2.chinampa(), CI["tenochtitlan"], t_lag - 0.1, t_sal, s=0.36, off=(-190, 55), sem=9, zs=0.45, z=1)
    andar(R, lambda p: M3.canoa_mexica(p), [(-99.35, 19.35), (-98.95, 19.48)], t_ciu, 3.2, t1=t_sal, s=0.34, sem=10, zs=0.4, z=3, fps=4)
    lugar(R, t_lag, t_sal - 0.2, "LAGO DE TEXCOCO", CI["tenochtitlan"], off=(0, 105), px=44)
    R.snd(t_lag, "ola", 0.35, dur=1.2)

    # el choque de dos mundos: guerrero águila vs conquistador y galeón en Veracruz
    andar(R, lambda p: M3.galeon(p), [(-94.2, 19.6), (-96.0, 19.2)], t_cho - 0.2, 2.2, t1=t_sal + 0.2, s=0.36, sem=11, zs=0.4, z=2, fps=4, flip=True)
    pa(R, M1.guerrero_aguila(0, "enojo"), 320, 1010, 1.05, t_cho - 0.1, t_sal + 0.1, sem=12, z=3)
    pa(R, M1.cortes(0, "serio"), 1600, 1010, 1.05, t_dos - 0.1, t_sal + 0.1, sem=13, z=3, flip=True)
    ga(R, A.espadas(), CI["tlaxcala"], t_cho + 0.1, t_sal + 0.1, s=0.44, off=(0, -20), sem=14, zs=0.35, z=4, extra=[(0.05, "espada", 0.5)])
    titulo(R, t_cho, t_sal - 0.1, "CHOQUE DE DOS MUNDOS", px=74)

    # frase 1: maíz, cacao, plata y 130 millones de personas
    pa(R, M2.planta_maiz(), 300, 1010, 0.92, t_maiz - 0.15, t_esta + 0.1, sem=15, entra="sube", dy=320, extra=[(0.05, "pluck", 0.4)])
    R.texto(t_maiz, t_esta, "MAÍZ", (300, 690), px=48, d=0.35)
    pa(R, M2.cacao(), 610, 1010, 0.92, t_cac - 0.15, t_esta + 0.1, sem=16, entra="sube", dy=300, extra=[(0.05, "pluck", 0.4)])
    R.texto(t_cac, t_esta, "CACAO", (610, 740), px=48, d=0.35)
    pa(R, M2.real_de_a_ocho(), 960, 1010, 0.92, t_pla - 0.15, t_esta + 0.1, sem=17, entra="sube", dy=300, extra=[(0.05, "monedas", 0.45)])
    R.texto(t_pla, t_esta, "PLATA MUNDIAL", (960, 720), px=46, d=0.4)
    ga(R, M2.cerro_mina_plata(), CI["zacatecas"], t_pla, t_esta, s=0.36, off=(0, 10), sem=18, zs=0.4, z=1)
    pa(R, M1.ciudadano_hoy(0, "feliz"), 1360, 1010, 0.95, t_nac - 0.1, t_esta + 0.1, sem=19)
    pa(R, M1.ingeniera_hoy(0, "feliz"), 1610, 1010, 0.95, t_nac + 0.1, t_esta + 0.1, sem=20, flip=True)
    R.contador(t_cie - 0.2, t_per + 0.3, 0, 130, (960, 196), px=84, formato="{} MILLONES", hasta_t=t_esta - 0.1)
    R.snd(t_cie - 0.2, "reloj_rapido", 0.35, dur=0.9)

    # frase 2: título y territorio de México
    R.terreno(t_mex - 0.2, "mexico_mod", COL["mexico_mod"], 0.8)
    R.terreno(FIN(e) + 0.4, None, COL["mexico_mod"], 0.3)
    R.snd(t_mex - 0.2, "whoosh", 0.45, dur=0.8)
    R.texto(t_hist - 0.2, FIN(e) + 0.6, "LA HISTORIA DE MÉXICO", (960, 178), px=96, d=0.9)
    R.texto(t_cinco - 0.1, FIN(e) + 0.6, "en 5 minutos", (960, 296), px=74, d=0.6)
    R.snd(t_hist - 0.2, "escribir", 0.45, dur=0.9)
    pa(R, lambda t: C.cronometro(round(kf(t, [(t_cinco, 0.0), (FIN(e) + 0.8, 0.9)], ease=lambda u: u), 2)), 1640, 860, 0.85, t_cinco - 0.1,
       FIN(e) + 0.6, sem=21, extra=[(0.08, "reloj_rapido", 0.4, {"dur": 1.1})])


# ------------------------------------------------------------------ ORÍGENES: Maíz, Olmecas y Zapotecas
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_siete, t_pue, t_dom, t_pla, t_maiz = T(e, "siete"), T(e, "pueblos"), T(e, "domestican"), T(e, "planta"), T(e, "maiz")
    t_mil, t_cos, t_gol, t_flo, t_mad, t_mes, t_olm = (T(e, "mil", frase=1), T(e, "costas"), T(e, "golfo"), T(e, "florece"),
                                                       T(e, "madre"), T(e, "mesoamerica"), T(e, "olmecas"))
    t_tal, t_col, t_cab, t_vein, t_lev, t_cen, t_ven = (T(e, "tallan"), T(e, "colosales"), T(e, "cabezas"), T(e, "veinte"),
                                                        T(e, "levantan"), T(e, "centros"), T(e, "venta"))
    t_mie, t_val, t_oax, t_zap, t_niv, t_mon, t_cal = (T(e, "mientras"), T(e, "valles"), T(e, "oaxaca"), T(e, "zapotecas"),
                                                       T(e, "nivelan"), T(e, "monte"), T(e, "calendarios"))

    # cámara: valle de Tehuacán / Balsas -> costa del Golfo (La Venta / San Lorenzo) -> valles de Oaxaca (Monte Albán)
    R.camara(i0 - 0.2, -97.8, 18.5, 4.4)
    R.camara(t_maiz + 0.4, -97.4, 18.4, 4.6)
    R.camara(t_mil + 0.2, -94.4, 18.0, 5.2)
    R.camara(t_mie - 0.1, -94.2, 18.05, 5.6)
    R.camara(t_oax + 0.2, -96.75, 17.05, 5.6)
    R.camara(FIN(e) + 0.4, -96.75, 17.15, 5.2)

    # años
    R.anio(i0 + 0.1, -5000)
    R.anio(t_mil, -1200)
    R.anio(t_mie + 0.2, -500)

    # frase 0: domesticación del maíz en Tehuacán y el Balsas
    ciudad(R, i0 + 0.2, t_mil - 0.2, "tehuacan", "VALLE DE TEHUACÁN", "arriba", 44)
    for k, (dx, dy) in enumerate(((-160, 20), (-70, 35), (70, 30), (160, 15))):
        ga(R, M2.planta_maiz(), CI["tehuacan"], t_dom - 0.2 + 0.12 * k, t_mil - 0.1, s=0.42, off=(dx, dy), sem=30 + k, zs=0.45, z=2,
           entra="sube", dy=240)
    R.snd(t_dom, "crece", 0.4, dur=0.8)
    pa(R, lambda t: M1.campesino_pre(int(t * 3) % 2, "feliz"), 320, 1010, 1.0, t_pue - 0.1, t_mil - 0.1, sem=34)
    pa(R, lambda t: M1.campesina_pre(int(t * 3) % 2, "feliz"), 580, 1010, 0.96, t_pue + 0.15, t_mil - 0.1, sem=35, flip=True)
    pa(R, M2.planta_maiz(), 1180, 1010, 1.15, t_pla - 0.1, t_mil - 0.1, sem=36, entra="sube", dy=360, extra=[(0.05, "brillo", 0.45)])
    titulo(R, t_maiz - 0.2, t_mil - 0.2, "EL MAÍZ SAGRADO", px=80)
    R.sello(t_maiz, "maiz", "EL MAÍZ", color=(212, 152, 44))

    # frase 1 y 2: los olmecas en San Lorenzo y La Venta + cabezas colosales de 20 toneladas
    R.terreno(t_gol - 0.1, "olmeca", COL["olmeca"], 1.0)
    R.snd(t_gol, "whoosh", 0.4, dur=0.7)
    lugar(R, t_mad, t_mie - 0.3, "CULTURA MADRE", (-94.5, 18.85), off=(0, 0), px=48)
    ciudad(R, t_olm - 0.1, t_mie - 0.2, "san_lorenzo", "SAN LORENZO", "abajo", 42)
    ciudad(R, t_ven - 0.3, t_mie - 0.2, "la_venta", "LA VENTA", "abajo", 46)
    R.sello(t_olm + 0.1, "olmeca", "OLMECAS", color=(68, 148, 122))

    ga(R, M2.cabeza_olmeca(), CI["san_lorenzo"], t_cab - 0.2, t_mie - 0.2, s=0.44, off=(-135, -20), sem=37, zs=0.5, z=2, entra="cae", dy=380,
       extra=[(0.05, "golpe_suave", 0.55)])
    ga(R, M2.cabeza_olmeca(), CI["la_venta"], t_cab + 0.1, t_mie - 0.2, s=0.48, off=(135, -20), sem=38, zs=0.5, z=2, entra="cae", dy=380)
    pa(R, M1.escultor_olmeca(0, "serio"), 310, 1010, 1.05, t_tal - 0.1, t_mie - 0.1, sem=39)
    pa(R, M2.cabeza_olmeca(), 660, 1010, 0.95, t_col - 0.1, t_mie - 0.1, sem=40, entra="sube", dy=340)
    R.contador(t_vein - 0.2, t_vein + 0.7, 1, 20, (960, 196), px=82, formato="{} TONELADAS", hasta_t=t_mie - 0.2)
    for k, dx in enumerate((-230, 260)):
        ga(R, M3.palmera_selva(220), CI["la_venta"], t_flo + 0.15 * k, t_mie - 0.2, s=0.35, off=(dx, -10), sem=41 + k, zs=0.4, z=1)
    ga(R, lambda t: M3.jaguar(int(t * 4) % 4), CI["san_lorenzo"], t_cen, t_mie - 0.2, s=0.32, off=(0, -90), sem=43, zs=0.4, z=2)

    # frase 3: los zapotecas en Oaxaca y Monte Albán
    R.terreno(t_oax - 0.1, "zapoteca", COL["zapoteca"], 1.0, capa=1)
    R.snd(t_oax, "whoosh", 0.4, dur=0.7)
    ciudad(R, t_mon - 0.3, FIN(e) + 0.3, "monte_alban", "MONTE ALBÁN", "abajo", 48)
    ga(R, M2.monte_alban(), CI["monte_alban"], t_niv - 0.1, FIN(e) + 0.3, s=0.56, off=(0, -15), sem=44, zs=0.5, z=2, entra="pluma", d_in=1.1,
       extra=[(0.05, "crece", 0.5, {"dur": 1.0})])
    titulo(R, t_zap - 0.1, FIN(e) + 0.2, "LOS ZAPOTECAS", px=78)
    pa(R, M1.sabio_zapoteca(0, "feliz"), 320, 1010, 1.08, t_zap - 0.1, FIN(e) + 0.3, sem=45)
    R.texto(t_zap + 0.1, FIN(e) + 0.2, "VALLES DE OAXACA", (320, 600), px=42, d=0.4)
    pa(R, M2.glifo_cero(), 1560, 1010, 0.92, t_cal - 0.3, FIN(e) + 0.3, sem=46, entra="sube", dy=300, extra=[(0.05, "escribir", 0.45, {"dur": 0.8})])
    R.texto(t_cal - 0.1, FIN(e) + 0.2, "PRIMEROS CALENDARIOS", (1560, 680), px=42, d=0.4)


# ------------------------------------------------------------------ PERIODO CLÁSICO: Teotihuacán y los Mayas
def _clasico(R):
    e = "clasico"
    i0 = INI(e)
    t_alt, t_met, t_teo, t_ciu, t_dios = T(e, "altiplano"), T(e, "metropolis"), T(e, "teotihuacan"), T(e, "ciudad"), T(e, "dioses")
    t_calz, t_sol, t_luna, t_cien, t_hab = T(e, "calzadas"), T(e, "sol"), T(e, "luna"), T(e, "cien"), T(e, "habitantes")
    t_sel, t_yuc, t_bri, t_may = T(e, "selvas"), T(e, "yucatan"), T(e, "brillan"), T(e, "mayas")
    t_pal, t_cala, t_chi, t_sab, t_ecl, t_cero, t_jer = (T(e, "palenque"), T(e, "calakmul"), T(e, "chichen"), T(e, "sabios"),
                                                         T(e, "eclipses"), T(e, "cero"), T(e, "jeroglifica"))
    t_pero, t_sig, t_seq, t_gue, t_aba, t_cap = (T(e, "pero"), T(e, "siglos"), T(e, "sequias"), T(e, "guerras"),
                                                 T(e, "abandono"), T(e, "capitales"))

    # cámara: Teotihuacán de cerca -> vuelo al área maya (Palenque, Calakmul, Chichén Itzá) -> plano abierto del colapso
    R.camara(i0 - 0.2, -98.84, 19.69, 6.2)
    R.camara(t_sel - 0.2, -98.84, 19.69, 6.4)
    R.camara(t_may, -90.8, 19.3, 3.1)
    R.camara(t_pero - 0.2, -90.5, 19.4, 3.1)
    R.camara(t_seq + 0.2, -93.8, 18.8, 2.4)
    R.camara(FIN(e) + 0.4, -94.2, 19.0, 2.3)

    # años
    R.anio(i0 + 0.1, 200)
    R.anio(t_cien, 450)
    R.anio(t_sel, 650)
    R.anio(t_pero, 800)

    # limpiamos capa olmeca y pintamos Teotihuacán
    R.terreno(i0 - 0.3, "teotihuacan", COL["teotihuacan"], 0.9)
    R.terreno(i0 - 0.3, None, COL["zapoteca"], 0.6, capa=1)
    R.sello(t_teo, "piramide_mx", "PERIODO CLÁSICO", color=(204, 74, 56))

    # frase 0 y 1: Teotihuacán, Pirámide del Sol y de la Luna, > 100.000 habitantes
    ciudad(R, t_teo - 0.2, t_sel - 0.3, "teotihuacan", "TEOTIHUACÁN", "abajo", 50)
    ga(R, M2.piramide_sol(), CI["teotihuacan"], t_met - 0.1, t_sel - 0.3, s=0.58, off=(0, -15), sem=50, zs=0.5, z=2, entra="pluma", d_in=1.2,
       extra=[(0.05, "crece", 0.5, {"dur": 1.1})])
    ga(R, M2.monte_alban(), CI["teotihuacan"], t_luna - 0.2, t_sel - 0.3, s=0.40, off=(-290, -45), sem=51, zs=0.5, z=1, entra="sube", dy=280)
    lugar(R, t_sol, t_sel - 0.3, "PIRÁMIDE DEL SOL", CI["teotihuacan"], off=(350, -60), px=38)
    lugar(R, t_luna, t_sel - 0.3, "PIRÁMIDE DE LA LUNA", CI["teotihuacan"], off=(-350, -195), px=38)
    pa(R, M1.sacerdote_teotihuacan(0, "serio"), 310, 1010, 1.1, t_dios - 0.2, t_sel - 0.2, sem=52, extra=[(0.05, "fanfarria", 0.32)])
    R.texto(t_dios, t_calz + 0.3, "CIUDAD DE LOS DIOSES", (310, 590), px=40, d=0.45)
    R.contador(t_cien - 0.2, t_hab + 0.3, 0, 100_000, (960, 196), px=82, formato="+{:,} HABITANTES", hasta_t=t_sel - 0.3)
    R.snd(t_cien - 0.2, "reloj_rapido", 0.35, dur=0.9)

    # frase 2 y 3: las ciudades-estado mayas (Palenque, Calakmul, Chichén Itzá), eclipses, el cero y jeroglíficos
    R.terreno(t_sel - 0.1, "maya", COL["maya"], 1.1, capa=1)
    R.snd(t_sel, "whoosh", 0.4, dur=0.8)
    titulo(R, t_may - 0.2, t_pal - 0.1, "CIUDADES-ESTADO MAYAS", px=76)
    ciudad(R, t_pal - 0.1, t_pero - 0.3, "palenque", "PALENQUE", "abajo", 42)
    ciudad(R, t_cala - 0.1, t_jer - 0.2, "calakmul", "CALAKMUL", "abajo", 42)
    ciudad(R, t_chi - 0.1, t_pero - 0.3, "chichen_itza", "CHICHÉN ITZÁ", "abajo", 44)
    ga(R, M2.piramide_kukulcan(), CI["palenque"], t_pal - 0.1, t_pero - 0.2, s=0.40, off=(0, -15), sem=53, zs=0.45, z=2, entra="sube", dy=280)
    ga(R, M2.piramide_kukulcan(), CI["calakmul"], t_cala - 0.1, t_pero - 0.2, s=0.40, off=(0, -15), sem=54, zs=0.45, z=2, entra="sube", dy=280)
    ga(R, M2.piramide_kukulcan(), CI["chichen_itza"], t_chi - 0.1, t_pero - 0.2, s=0.48, off=(0, -15), sem=55, zs=0.45, z=2, entra="pluma", d_in=1.0,
       extra=[(0.05, "crece", 0.45)])
    pa(R, M1.rey_maya(0, "serio"), 240, 1010, 1.04, t_may - 0.1, t_pero - 0.2, sem=56)
    pa(R, M1.astronomo_maya(0, "feliz"), 490, 1010, 1.0, t_sab - 0.1, t_pero - 0.2, sem=57, flip=True)
    pa(R, A.sol_brillo(), 1580, 420, 0.76, t_ecl - 0.1, t_pero - 0.2, sem=58, extra=[(0.05, "brillo", 0.4)])
    R.texto(t_ecl, t_cero - 0.2, "ECLIPSES", (1580, 260), px=44, d=0.35)
    pa(R, M2.glifo_cero(), 1640, 1010, 0.94, t_cero - 0.15, t_pero - 0.2, sem=59, entra="sube", dy=320, extra=[(0.05, "ding", 0.45)])
    R.texto(t_cero, t_pero - 0.2, "EL CERO MAYA", (1640, 680), px=42, d=0.4)
    pa(R, A.rollo_escritura(), 1320, 1010, 0.65, t_jer - 0.2, t_pero - 0.2, sem=60, extra=[(0.05, "escribir", 0.4, {"dur": 0.7})])
    R.texto(t_jer - 0.1, t_pero - 0.2, "JEROGLÍFICOS", (1320, 810), px=40, d=0.4)

    # frase 4: sequías, guerras y abandono de las grandes capitales clásicas (fractura Voronoi)
    R.romper("clasico_colapso", t_seq - 0.1, t_seq + 0.6, FIN(e) - 0.2, FIN(e) + 0.4, capa=0, gap=14.0, deriva=28.0)
    R.romper("clasico_colapso", t_seq, t_seq + 0.7, FIN(e) - 0.2, FIN(e) + 0.4, capa=1, gap=14.0, deriva=28.0)
    R.snd(t_seq, "crujido", 0.5, dur=0.9)
    titulo(R, t_seq - 0.1, FIN(e) + 0.2, "COLAPSO DEL CLÁSICO (S. VII-IX)", px=72)
    ga(R, A.espadas(), (-92.0, 18.2), t_gue - 0.1, FIN(e) + 0.2, s=0.42, off=(0, 0), sem=61, zs=0.35, z=3, extra=[(0.05, "espada", 0.5)])
    ga(R, A.grietas_hueso(), CI["teotihuacan"], t_aba - 0.2, FIN(e) + 0.2, s=0.5, off=(0, 0), sem=62, zs=0.35, z=3)
    pa(R, A.sol_brillo(), 1580, 440, 0.85, t_seq - 0.1, FIN(e) + 0.2, sem=63, extra=[(0.05, "viento", 0.4, {"dur": 1.6})])
    R.texto(t_seq + 0.1, FIN(e) + 0.2, "SEQUÍAS Y GUERRAS", (1580, 640), px=44, d=0.4)


# ------------------------------------------------------------------ MEXICAS: Tula, migración náhuatl, Tenochtitlan y la Triple Alianza
def _mexicas(R):
    e = "mexicas"
    i0 = INI(e)
    t_tol, t_tula, t_pue, t_nah, t_cam, t_nor, t_val = (T(e, "tolteca"), T(e, "tula"), T(e, "pueblos", frase=0), T(e, "nahuatl"),
                                                        T(e, "caminan"), T(e, "norte"), T(e, "valle"))
    t_mil, t_mex, t_sen, t_isl, t_tex, t_agu, t_nop = (T(e, "mil"), T(e, "mexicas", frase=1), T(e, "senal"), T(e, "islote"),
                                                       T(e, "texcoco"), T(e, "aguila"), T(e, "nopal"))
    t_fun, t_ten, t_flo, t_calz, t_isl2, t_chi = (T(e, "fundan"), T(e, "tenochtitlan"), T(e, "flotante"), T(e, "calzadas"),
                                                  T(e, "islas"), T(e, "chinampas"))
    t_tri, t_ali, t_imp, t_ext, t_cos, t_trib = (T(e, "triple"), T(e, "alianza"), T(e, "imperio"), T(e, "extiende"),
                                                 T(e, "costa"), T(e, "tributo"))

    # cámara: norte / Tula -> acercamiento al lago de Texcoco -> vista imperial de costa a costa
    R.camara(i0 - 0.2, -100.8, 20.5, 3.8)
    R.camara(t_val, -100.4, 20.3, 4.0)
    R.camara(t_isl, -99.05, 19.45, 7.2)
    R.camara(t_tri - 0.2, -99.08, 19.44, 7.2)
    R.camara(t_imp + 0.2, -98.2, 18.8, 3.8)
    R.camara(FIN(e) + 0.4, -98.0, 18.7, 3.6)

    # años
    R.anio(i0 + 0.1, 950)
    R.anio(t_mil, 1325)
    R.anio(t_tri, 1428)

    # frase 0: esplendor tolteca en Tula y migración náhuatl desde el norte
    R.terreno(i0 - 0.3, "tolteca", COL["tolteca"], 0.8)
    R.terreno(i0 - 0.3, None, COL["maya"], 0.6, capa=1)
    ciudad(R, t_tula - 0.2, t_cam + 0.2, "tula", "TULA", "der", 46)
    ga(R, M2.atlante_tula(), CI["tula"], i0 + 0.1, t_val, s=0.46, off=(-110, -15), sem=70, zs=0.45, z=2, entra="sube", dy=280,
       extra=[(0.05, "crece", 0.4)])
    ga(R, M2.atlante_tula(), CI["tula"], i0 + 0.25, t_val, s=0.46, off=(110, -15), sem=71, zs=0.45, z=2, entra="sube", dy=280)
    pa(R, M1.guerrero_tolteca(0, "serio"), 310, 1010, 1.05, i0 + 0.1, t_mil - 0.1, sem=72)
    R.texto(t_tol, t_mil - 0.2, "LOS TOLTECAS", (310, 610), px=44, d=0.4)

    R.ruta(M.RUTAS["migracion_mexica"], t_cam - 0.3, 2.2, ancho=5.0, t1=t_mil + 0.3, flecha=True)
    grupo(R, lambda p: M1.campesino_pre(p % 2, "serio"), M.RUTAS["migracion_mexica"][:3], t_cam - 0.2, 2.0, n=3, ancho=90, t1=t_val,
          s=0.38, sem=73, fps=6)
    R.snd(t_cam - 0.1, "pasos", 0.4, dur=1.8)
    lugar(R, t_nah, t_val - 0.1, "PUEBLOS NÁHUATL", (-102.2, 21.8), off=(0, 0), px=44)

    # frase 1: 1325, el águila sobre el nopal en el lago de Texcoco
    lugar(R, t_tex - 0.1, t_fun + 0.3, "LAGO DE TEXCOCO", CI["texcoco"], off=(120, -40), px=44)
    pa(R, M2.aguila_nopal(), 960, 960, 1.18, t_sen - 0.1, t_fun + 0.2, sem=76, entra="sube", dy=380, extra=[(0.05, "fanfarria", 0.4)])
    titulo(R, t_agu - 0.1, t_fun, "EL ÁGUILA SOBRE EL NOPAL (1325)", px=74)
    R.sello(t_nop - 0.2, "aguila_nopal", "TENOCHTITLAN", color=(198, 56, 52))

    # frase 2: México-Tenochtitlan, calzadas y chinampas
    ciudad(R, t_ten - 0.2, t_tri - 0.2, "tenochtitlan", "MÉXICO-TENOCHTITLAN", "abajo", 46)
    ga(R, M2.templo_mayor(), CI["tenochtitlan"], t_fun, FIN(e) + 0.3, s=0.56, off=(0, -15), sem=77, zs=0.5, z=2, entra="pluma", d_in=1.1,
       extra=[(0.05, "crece", 0.5, {"dur": 1.0})])

    def calzadas_lago(h, cam, t, fs, te):
        if not (t_calz - 0.2 <= t <= t_tri + 0.1):
            return
        x0, y0 = cam.pant(*CI["tenochtitlan"])
        u = e_inout(prog(t, t_calz - 0.2, t_calz + 0.7)) * (1 - prog(t, t_tri - 0.2, t_tri + 0.1))
        for k, (dx, dy) in enumerate(((0, -180), (-210, 20), (0, 190), (160, -40))):
            linea_punteada(h, np.array([(x0, y0), (x0 + dx, y0 + dy)]), t, 18, 12, 4.2, 700 + k, fs, u)
    R.frente.append(R._acot(calzadas_lago, t_calz - 0.2))

    for k, (dx, dy) in enumerate(((-240, -10), (230, -10))):
        ga(R, M2.chinampa(), CI["tenochtitlan"], t_isl2 - 0.1 + 0.15 * k, t_tri - 0.1, s=0.40, off=(dx, dy), sem=78 + k, zs=0.45, z=2,
           entra="sube", dy=240)
    andar(R, lambda p: M3.canoa_mexica(p), [(-99.32, 19.30), (-98.90, 19.32)], t_flo, 3.0, t1=t_tri - 0.1, s=0.34, sem=80, zs=0.4, z=3, fps=4)
    pa(R, M2.chinampa(), 1520, 990, 0.92, t_chi - 0.2, t_tri + 0.1, sem=81, entra="sube", dy=280, extra=[(0.05, "ola", 0.35)])
    R.texto(t_chi, t_tri, "LAS CHINAMPAS", (1520, 780), px=46, d=0.4)

    # frase 3: Triple Alianza, Imperio mexica de costa a costa y tributos
    R.terreno(t_tri - 0.1, "mexica", COL["mexica"], 1.1)
    R.terreno(t_tri + 0.2, "tlaxcala", COL["tlaxcala"], 0.9, capa=1)
    R.snd(t_tri, "tambor", 0.45)
    titulo(R, t_tri, FIN(e) + 0.2, "EL IMPERIO MEXICA (TRIPLE ALIANZA)", px=72)
    ciudad(R, t_ext, FIN(e) + 0.2, "tlaxcala", "TLAXCALA", "der", 42)
    pa(R, M1.moctezuma(0, "serio"), 290, 1010, 1.12, t_imp - 0.1, FIN(e) + 0.3, sem=82, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_imp + 0.1, FIN(e) + 0.2, "HUEY TLATOANI", (290, 580), px=42, d=0.4)
    pa(R, M1.guerrero_aguila(0, "enojo"), 600, 1010, 1.02, t_ext - 0.1, FIN(e) + 0.3, sem=83)
    pa(R, M1.guerrero_jaguar(0, "enojo"), 860, 1010, 1.02, t_ext + 0.1, FIN(e) + 0.3, sem=84, flip=True)
    pa(R, M2.cacao(), 1380, 1010, 0.72, t_trib - 0.1, FIN(e) + 0.3, sem=85, extra=[(0.05, "monedas", 0.4)])
    pa(R, A.bolsa_dinero(), 1600, 1010, 0.65, t_trib + 0.1, FIN(e) + 0.3, sem=86)
    R.texto(t_trib, FIN(e) + 0.2, "TRIBUTO DE LOS PUEBLOS", (1490, 740), px=42, d=0.4)
