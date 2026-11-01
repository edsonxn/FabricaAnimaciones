# -*- coding: utf-8 -*-
"""Coreografía (4/4): la Edad Moderna (Egipto otomano, Napoleón y sus sabios, la Piedra de Rosetta, Champollion descifra los jeroglíficos,
Mehmet Alí y el algodón, el Canal de Suez), el siglo XX (protectorado británico, independencia de 1922, la República de 1953, Nasser y el
canal, la presa de Asuán y el lago Nasser, 105 millones de egipcios, las pirámides de hoy), el cierre (desfile de cinco mil años a orillas
del Nilo y la pregunta) y los cambios de escena procedurales.
Capas: 0 = el poder que gobierna Egipto, 1 = Francia, 50 = el lago Nasser (agua)."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_eg1 as E1
import obj_eg2 as E2
import obj_eg3 as E3
from core import FIN, INI, T, kf
from coreo_util import CI, COL, andar, ciudad, formacion, ga, grupo, lugar, mece, nilo, pa, titulo, tramo
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog
from trans import SFX, Transicion

CANAL = (110, 170, 210)


def cortes(R):
    pass


def construir(R):
    _modernidad(R)
    _siglo20(R)
    _cierre(R)
    _transiciones(R)


# ------------------------------------------------------------------ NAPOLEÓN, ROSETTA, MEHMET ALÍ Y SUEZ
def _modernidad(R):
    e = "modernidad"
    i0 = INI(e)
    t_ocho, t_nap, t_des, t_tro, t_cie, t_hal, t_pie = (T(e, "ocho"), T(e, "napoleon"), T(e, "desembarca"), T(e, "tropas"), T(e, "cientificos"), T(e, "hallan"),
                                                        T(e, "piedra"))
    t_gra, t_sab, t_desc, t_jer, t_casi, t_mil, t_sil = (T(e, "gracias"), T(e, "sabios"), T(e, "descifrar"), T(e, "jeroglificos"), T(e, "casi"), T(e, "mil", frase=1),
                                                         T(e, "silencio"))
    t_gob, t_meh, t_mod, t_ins, t_agr, t_bas, t_con = (T(e, "gobernante"), T(e, "mehmet"), T(e, "moderniza"), T(e, "instituciones"), T(e, "agricultura"),
                                                       T(e, "bases"), T(e, "contemporaneo"))
    t_mil3, t_ina, t_can, t_suez, t_uni, t_med, t_oce, t_ind, t_tra, t_rut = (T(e, "mil", frase=3), T(e, "inaugura"), T(e, "canal"), T(e, "suez"), T(e, "uniendo"),
                                                                              T(e, "mediterraneo"), T(e, "oceano"), T(e, "indico"), T(e, "transformando"),
                                                                              T(e, "rutas"))
    # cámara
    R.camara(i0 - 0.2, 30.4, 30.4, 1.6)
    R.camara(t_nap - 0.2, 29.4, 31.8, 1.4)
    R.camara(t_des + 0.6, 30.6, 30.7, 3.0)
    R.camara(t_pie - 0.4, 30.45, 31.22, 6.8)
    R.camara(t_gra, 30.6, 31.0, 5.6)
    R.camara(t_gob, 31.5, 24.8, 1.2)
    R.camara(t_agr + 0.4, 31.2, 26.5, 1.45)
    R.camara(t_con + 0.3, 31.25, 26.7, 1.5)
    R.camara(t_mil3 + 0.3, 32.4, 30.6, 5.2)
    R.camara(t_suez + 0.8, 32.45, 30.5, 4.8)
    R.camara(t_oce, 38.0, 17.0, 1.25)
    R.camara(t_rut, 38.6, 15.0, 1.3)
    R.camara(FIN(e) + 0.6, 38.6, 15.0, 1.3)
    # años
    R.anio(i0, 1517)
    R.anio(t_ocho, 1798)
    R.anio(t_gra, 1822)
    R.anio(t_gob, 1830)
    R.anio(t_mil3, 1869)
    # el Egipto otomano y la llegada de los franceses
    R.terreno(i0 - 0.6, "otomano", COL["otomano"], 0.5)
    R.terreno(i0 - 0.6, None, COL["mongoles"], 0.4, capa=3)
    ga(R, E2.bandera("otomana"), CI["cairo"], i0, t_nap, s=0.32, off=(0, -10), sem=320, zs=0.4, z=2)
    lugar(R, i0, t_nap, "EGIPTO OTOMANO (1517)", (28.6, 29.0), off=(0, 0), px=46)
    for k in range(3):
        andar(R, lambda p, k=k: E3.navio(p + k), M.RUTAS["napoleon"][1:4], t_ocho - 0.3 + 0.2 * k, 1.9, t1=t_cie, s=0.3, sem=321 + k, zs=0.4, z=2, fps=4,
              off=formacion(k, 3, 140), ease=e_out)
    R.snd(t_nap, "canonazo", 0.4)
    pa(R, E1.napoleon(0, "serio"), 330, 1010, 1.15, t_nap - 0.2, t_gra - 0.2, sem=324, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_nap + 0.1, t_gra - 0.3, "NAPOLEÓN", (330, 600), px=54, d=0.4)
    R.terreno(t_des, "francia", COL["francia"], 1.4, capa=1)
    P_fr = [(29.92, 31.2), (30.4, 30.9), (30.8, 30.5), (31.13, 30.05)]
    grupo(R, lambda p: E1.soldado_fr(p % 2, "serio"), P_fr, t_des, 2.2, n=3, ancho=90, t1=t_pie, s=0.36, sem=325, fps=6)
    R.snd(t_des + 0.2, "pasos", 0.4, dur=2.0)
    titulo(R, t_des, t_cie - 0.1, "LA EXPEDICIÓN FRANCESA", px=70)
    ga(R, E2.piramides_guiza(), CI["guiza"], t_tro, t_pie, s=0.26, off=(-60, 10), sem=328, zs=0.4, z=1)
    pa(R, E1.sabio_fr(0, "asombro"), 1420, 1010, 0.92, t_cie - 0.1, t_gra - 0.2, sem=329)
    pa(R, E1.sabio_fr(1, "feliz", "lupa"), 1650, 1010, 0.92, t_cie + 0.1, t_gra - 0.2, sem=330, flip=True)
    R.texto(t_cie + 0.2, t_gra - 0.3, "SABIOS Y CIENTÍFICOS", (1535, 630), px=44, d=0.5)
    ciudad(R, t_pie - 0.3, t_gra, "rosetta", "ROSETTA (RASHID)", "der", 46)
    ga(R, E2.piedra_rosetta(), CI["rosetta"], t_pie - 0.3, t_gra, s=0.42, off=(-170, 40), sem=331, zs=0.5, z=3, entra="sube", dy=400,
       extra=[(0.05, "brillo", 0.5)])
    # Champollion descifra los jeroglíficos
    R.terreno(t_gra, None, COL["francia"], 0.8, capa=1)
    pa(R, E1.champollion(0, "asombro"), 330, 1010, 1.15, t_gra - 0.1, t_gob - 0.2, sem=332, extra=[(0.05, "pluck", 0.4)])
    R.texto(t_gra + 0.1, t_gob - 0.3, "CHAMPOLLION (1822)", (330, 600), px=46, d=0.5)
    pa(R, E2.piedra_rosetta(), 880, 1000, 0.95, t_gra, t_gob - 0.2, sem=333)
    pa(R, E2.cartucho(("pan", "buho", "cana")), 1460, 1000, 1.05, t_desc - 0.2, t_gob - 0.2, sem=334, extra=[(0.05, "bling", 0.35)])
    pa(R, Bb.flecha(), 1170, 860, 0.7, t_desc, t_gob - 0.2, sem=339)
    R.texto(t_desc + 0.3, t_gob - 0.3, "= PTOLOMEO", (1500, 700), px=46, d=0.5)
    R.snd(t_desc + 0.3, "tick", 0.35)
    R.snd(t_jer, "ding", 0.5)
    titulo(R, t_desc, t_casi - 0.1, "¡DESCIFRADOS!", px=84)
    R.contador(t_casi, t_mil + 0.8, 0, 1428, (960, 196), px=78, formato="{:,} AÑOS DE SILENCIO", hasta_t=t_gob - 0.2)
    R.snd(t_casi, "reloj_rapido", 0.35, dur=1.0)
    # Mehmet Alí: el Egipto moderno (y el algodón)
    R.terreno(t_gob - 0.2, "mehmet", COL["mehmet"], 1.2)
    pa(R, E1.mehmet_ali(0, "serio"), 330, 1010, 1.15, t_gob - 0.1, t_mil3 - 0.2, sem=335, extra=[(0.05, "cuerno", 0.3)])
    R.texto(t_meh, t_mil3 - 0.3, "MEHMET ALÍ", (330, 600), px=54, d=0.4)
    lugar(R, t_meh + 0.3, t_mil3 - 0.2, "EGIPTO Y SUDÁN", (35.4, 21.4), off=(0, 0), px=46)
    pa(R, C.fabrica(), 900, 1010, 0.55, t_ins - 0.1, t_mil3 - 0.2, sem=336, extra=[(0.05, "crece", 0.4)])
    R.texto(t_ins + 0.1, t_mil3 - 0.3, "FÁBRICAS Y ESCUELAS", (900, 790), px=40, d=0.5)
    for k, x in enumerate((1380, 1520, 1660)):
        pa(R, E3.algodon(), x, 1010, 0.62, t_agr - 0.1 + 0.12 * k, t_mil3 - 0.2, sem=337 + k, entra="sube", dy=300)
    R.texto(t_agr + 0.1, t_mil3 - 0.3, "ALGODÓN", (1520, 780), px=48, d=0.4)
    R.rio([(29.92, 31.18), (30.2, 31.15), (30.48, 31.12)], t_agr, 1.0, CANAL, ancho=8, tinta=True, t1=t_mil3 - 0.2)
    ga(R, lambda t: E3.buey(int(t * 4) % 4), (30.9, 30.6), t_agr + 0.2, t_mil3 - 0.2, s=0.3, off=(0, 0), sem=340, zs=0.4, z=2)
    R.snd(t_agr, "pluck", 0.35)
    # el Canal de Suez
    R.rio(M.RUTAS["suez"], t_ina - 0.4, 1.4, CANAL, ancho=12, tinta=True)
    R.snd(t_ina - 0.4, "chorro", 0.4, dur=1.2)
    pa(R, E1.lesseps(0, "feliz"), 330, 1010, 1.12, t_mil3 - 0.1, t_med, sem=341)
    R.texto(t_ina, t_med - 0.1, "FERDINAND DE LESSEPS", (330, 600), px=40, d=0.5)
    ciudad(R, t_can - 0.2, t_med, "port_said", "PORT SAID", "der", 40)
    ciudad(R, t_suez - 0.1, t_med, "suez", "SUEZ", "der", 40)
    andar(R, lambda p: E3.vapor_suez(p), M.RUTAS["suez"], t_ina - 0.1, t_med - t_ina + 0.4, t1=t_oce, s=0.3, sem=342, zs=0.4, z=3, fps=4,
          ease=lambda u: u)
    for k, (dx, dy) in enumerate(((-300, -30), (280, -50), (420, 120))):
        ga(R, lambda t, k=k: Bb.chispas(), CI["port_said"], t_ina + 0.15 * k, t_uni, s=0.3, off=(dx, dy), sem=343 + k, zs=0.3, z=4,
           extra=[(0.0, "estrellitas", 0.4)] if k == 0 else ())
    R.sello(t_suez, "ancla", "CANAL DE SUEZ", color=(70, 120, 180))
    titulo(R, t_can - 0.1, t_med - 0.1, "CANAL DE SUEZ: 164 km", px=70)
    # una nueva ruta entre el Mediterráneo y el Índico
    R.ruta(M.RUTAS["ruta_india"], t_uni - 0.2, 3.4, ancho=5.0, flecha=True)
    for k in range(3):
        andar(R, lambda p, k=k: E3.vapor_suez(p + k), M.RUTAS["ruta_india"][3:], t_uni + 0.5 * k, 4.4, s=0.36, sem=346 + k, zs=0.4, z=3, fps=4,
              ease=lambda u: u)
    lugar(R, t_oce, FIN(e) + 0.3, "OCÉANO ÍNDICO", (45.4, 12.2), off=(0, 0), px=54)
    lugar(R, t_med - 0.1, t_oce, "MAR ROJO", (38.2, 19.6), off=(0, 0), px=48)
    titulo(R, t_tra - 0.1, FIN(e) + 0.3, "UN ATAJO ENTRE EUROPA Y ASIA", px=66)


# ------------------------------------------------------------------ EL SIGLO XX Y HOY
def _siglo20(R):
    e = "siglo20"
    i0 = INI(e)
    t_tras, t_pro, t_bri, t_egi, t_procl, t_ind, t_mil, t_rep = (T(e, "tras"), T(e, "protectorado"), T(e, "britanico"), T(e, "egipto"), T(e, "proclama"),
                                                                 T(e, "independencia"), T(e, "mil"), T(e, "republica"))
    t_pais, t_nac, t_can, t_cons, t_pre, t_asu, t_dom, t_cre, t_nilo = (T(e, "pais"), T(e, "nacionaliza"), T(e, "canal"), T(e, "construye"), T(e, "presa"),
                                                                        T(e, "asuan"), T(e, "domesticando"), T(e, "crecidas"), T(e, "nilo"))
    t_hoy, t_cien, t_mill, t_per, t_viv, t_pue, t_afr, t_ori = (T(e, "hoy"), T(e, "ciento"), T(e, "millones"), T(e, "personas"), T(e, "viven"), T(e, "puente"),
                                                                T(e, "africa"), T(e, "oriente"))
    t_pir, t_sig, t_des, t_cinco, t_hist = T(e, "piramides"), T(e, "siguen"), T(e, "desierto"), T(e, "cinco", frase=3), T(e, "historia")
    # cámara
    R.camara(i0 - 0.2, 31.0, 28.0, 1.9)
    R.camara(t_rep + 0.4, 31.1, 28.4, 2.0)
    R.camara(t_pais, 32.3, 30.85, 5.0)
    R.camara(t_cons - 0.6, 32.35, 30.8, 4.8)
    R.camara(t_cons + 0.4, 32.4, 27.3, 2.4)
    R.camara(t_pre, 32.6, 23.75, 4.4)
    R.camara(t_nilo + 0.2, 32.4, 23.5, 3.9)
    R.camara(t_hoy + 0.2, 33.8, 27.2, 1.0)
    R.camara(t_ori + 0.6, 34.0, 27.6, 1.05)
    R.camara(t_pir, 31.17, 29.975, 8.6)
    R.camara(FIN(e) + 0.6, 31.17, 29.97, 9.4)
    # años
    R.anio(t_tras, 1882)
    R.anio(t_procl, 1922)
    R.anio(t_mil, 1953)
    R.anio(t_nac, 1956)
    R.anio(t_pre, 1970)
    R.anio(t_hoy, 2026)
    # el protectorado británico y la independencia
    R.terreno(t_tras, "britanico", COL["britanico"], 1.0)
    pa(R, E1.soldado_brit(0, "serio"), 330, 1010, 1.12, t_pro - 0.2, t_procl, sem=351, sale="izq_fuera", d_out=0.5)
    titulo(R, t_pro, t_procl - 0.1, "PROTECTORADO BRITÁNICO", px=70)
    R.morf(E2.bandera("uk"), E2.bandera_reino(), t_procl, 0.7, (1000, 1010, 0.82), sem=352, salida=t_pais, t_a=t_bri - 0.1)
    R.terreno(t_procl, "egipto_mod", COL["egipto_mod"], 1.0)
    titulo(R, t_ind - 0.1, t_mil - 0.1, "INDEPENDENCIA (1922)", px=72)
    R.snd(t_ind, "fanfarria", 0.4)
    for k in range(4):
        pa(R, lambda t, k=k: E1.egipcio_hoy(k, int(t * 3) % 2), 220 + 190 * k, 1010, 0.8, t_mil + 0.15 * k, t_pais, sem=353 + k, entra="sube", dy=300)
    titulo(R, t_mil + 0.1, t_pais - 0.1, "LA REPÚBLICA (1953)", px=72)
    R.sello(t_rep, "aguila", "REPÚBLICA", color=(200, 60, 54))
    # Nasser nacionaliza el canal
    R.rio(M.RUTAS["suez"], t_pais - 0.6, 0.3, CANAL, ancho=12, tinta=True)
    ciudad(R, t_pais, t_cons - 0.6, "port_said", "PORT SAID", "izq", 40)
    ciudad(R, t_pais + 0.1, t_cons, "suez", "SUEZ", "der", 40)
    pa(R, E1.nasser(0, "feliz"), 330, 1010, 1.15, t_pais - 0.1, t_nilo + 0.3, sem=357, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_nac, t_nilo + 0.2, "NASSER (1956)", (330, 600), px=50, d=0.4)
    andar(R, lambda p: E3.vapor_suez(p), M.RUTAS["suez"], t_pais, 2.4, t1=t_cons, s=0.32, sem=358, zs=0.4, z=3, fps=4, ease=lambda u: u)
    titulo(R, t_nac, t_cons - 0.1, "EL CANAL ES EGIPCIO", px=74)
    # la Gran Presa de Asuán y el lago Nasser
    ga(R, E2.presa_asuan(), CI["presa"], t_pre - 0.3, FIN(e, 1) + 0.3, s=0.4, off=(0, 30), sem=359, zs=0.5, z=2, entra="pluma", d_in=1.1,
       extra=[(0.05, "crece", 0.5, {"dur": 1.0})])
    ciudad(R, t_asu - 0.1, FIN(e, 1) + 0.3, "asuan", None)
    lugar(R, t_asu, FIN(e, 1) + 0.2, "ASUÁN", CI["asuan"], off=(0, 150), px=46)
    titulo(R, t_pre, FIN(e, 1) + 0.2, "LA GRAN PRESA DE ASUÁN", px=70)
    R.terreno(t_dom - 0.3, "nasser", M.AGUA_LAGO, 2.2, capa=50)
    R.snd(t_dom - 0.2, "chorro", 0.45, dur=1.8)
    lugar(R, t_dom + 0.6, FIN(e, 1) + 0.2, "LAGO NASSER", (31.7, 22.6), off=(0, 0), px=48)
    pa(R, E2.crecida(), 1500, 1010, 0.6, t_dom, FIN(e, 1) + 0.3, sem=360)
    pa(R, E2.tachar(), 1500, 1000, 0.62, t_cre - 0.1, FIN(e, 1) + 0.3, sem=361, entra="pluma", d_in=0.3, z=3, extra=[(0.0, "borrar", 0.45)])
    pa(R, E1.ingeniero(0, "feliz"), 1000, 1010, 0.95, t_pre + 0.3, FIN(e, 1) + 0.3, sem=362)
    # hoy: más de 105 millones, puente entre África y Oriente Medio
    R.contador(t_cien - 0.4, t_mill + 0.6, 0, 105_000_000, (960, 196), px=88, hasta_t=FIN(e, 2) + 0.2)
    R.texto(t_per, FIN(e, 2) + 0.1, "PERSONAS", (960, 300), px=56, d=0.4)
    R.snd(t_cien - 0.4, "reloj_rapido", 0.4, dur=1.2)
    for k in range(6):
        pa(R, lambda t, k=k: E1.egipcio_hoy(k, int(t * 3 + k) % 2), 250 + 284 * k, 1010, 0.7, t_hoy + 0.4 + 0.12 * k, FIN(e, 2) + 0.2, sem=363 + k,
           entra="sube", dy=300, flip=k % 2 == 1)
    ga(R, E2.rascacielos_eg(4), CI["cairo"], t_hoy + 0.2, FIN(e, 2) + 0.2, s=0.24, off=(40, 0), sem=369, zs=0.4, z=1)
    lugar(R, t_afr - 0.2, FIN(e, 2) - 0.3, "ÁFRICA", (24.6, 26.2), off=(0, 0), px=62)
    lugar(R, t_ori - 0.1, FIN(e, 2) - 0.3, "ORIENTE MEDIO", (42.0, 29.0), off=(0, 0), px=58)
    R.ruta([(27.5, 24.0), (31.0, 28.5), (33.8, 30.0), (37.0, 30.6), (40.0, 30.4)], t_pue - 0.1, 1.4, ancho=6.0, t1=FIN(e, 2) + 0.2, flecha=True)
    R.ruta([(40.0, 29.4), (37.0, 29.6), (33.8, 29.2), (31.4, 27.4), (28.0, 23.2)], t_pue + 0.3, 1.4, ancho=6.0, t1=FIN(e, 2) + 0.2, flecha=True)
    # las pirámides siguen ahí
    ga(R, E2.piramides_guiza(), CI["guiza"], t_pir - 0.3, FIN(e) + 0.4, s=0.62, off=(-380, 60), sem=370, zs=0.5, z=1, entra="sube", dy=400,
       extra=[(0.05, "crece", 0.4)])
    ga(R, E2.esfinge(), CI["guiza"], t_pir, FIN(e) + 0.4, s=0.34, off=(-40, 140), sem=371, zs=0.5, z=2, entra="sube", dy=300)
    ga(R, E2.rascacielos_eg(5), CI["cairo"], t_sig - 0.2, FIN(e) + 0.4, s=0.34, off=(300, -40), sem=372, zs=0.5, z=1, entra="sube", dy=300)
    ga(R, E2.torre_cairo(), CI["cairo"], t_sig, FIN(e) + 0.4, s=0.3, off=(560, -10), sem=373, zs=0.5, z=1, entra="sube", dy=300)
    pa(R, lambda t: E3.camello(int(t * 2) % 4, carga=False), 1430, 1010, 0.5, t_des - 0.2, FIN(e) + 0.4, sem=374)
    pa(R, E1.turista(0, "feliz"), 1690, 1010, 0.9, t_des, FIN(e) + 0.4, sem=375, extra=[(0.05, "obturador", 0.45)])
    R.contador(t_cinco - 0.3, t_hist + 0.3, 0, 5000, (960, 196), px=86, formato="{:,} AÑOS", hasta_t=FIN(e) + 0.4)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_tie, t_far, t_nac, t_civ, t_nun, t_rei, t_ori, t_rio = (T(e, "tierra"), T(e, "faraones"), T(e, "nacer"), T(e, "civilizacion"), T(e, "nunca"),
                                                              T(e, "reinventarse"), T(e, "orillas"), T(e, "rio"))
    t_que, t_pais, t_imp, t_dim, t_com = T(e, "que", frase=1), T(e, "pais"), T(e, "imperio"), T(e, "dimelo"), T(e, "comentarios")
    R.camara(i0 - 0.2, 31.5, 27.3, 2.4)
    R.camara(t_rio, 31.4, 27.6, 2.05)
    R.camara(FIN(e) + 1.4, 31.35, 27.7, 1.85)
    R.terreno(i0 - 0.5, None, COL["egipto_mod"], 0.4)
    # el desfile de cinco mil años a orillas del Nilo
    P = tramo(nilo(), (32.9, 24.15), (31.26, 29.9), 40)
    gente = [lambda p: E1.keops(p % 2, "feliz"), lambda p: E1.nefertiti(p % 2, "feliz"), lambda p: E1.ramses(p % 2, "feliz"),
             lambda p: E1.cleopatra(p % 2, "feliz"), lambda p: E1.saladino(p % 2, "feliz"), lambda p: E1.mehmet_ali(p % 2, "feliz"),
             lambda p: E1.nasser(p % 2, "feliz", (16, 30)), lambda p: E1.egipcio_hoy(4, p % 2)]
    for k, fn in enumerate(gente):
        andar(R, fn, P, i0 - 0.6 + 0.75 * k, 7.0, t1=t_que + 0.3, s=0.58, sem=380 + k, zs=0.4, z=3, fps=5, off=(-150 if k % 2 else 150, 10),
              ease=lambda u: u)
    R.snd(t_tie, "pasos", 0.35, dur=4.0)
    andar(R, lambda p: E3.falua(p), tramo(nilo(), (31.3, 29.6), (32.6, 25.8), 20), i0 - 0.4, 7.0, t1=t_que + 0.3, s=0.36, sem=390, zs=0.3, z=2, fps=4,
          ease=lambda u: u)
    R.texto(t_far - 0.3, t_que - 0.1, "LA TIERRA DE LOS FARAONES", (1480, 900), px=60, d=1.0)
    R.rio(tramo(nilo(), (32.9, 24.1), (31.24, 30.1), 40), t_rio - 0.3, 1.6, (150, 200, 232), ancho=16, tinta=False, t1=FIN(e) + 1.0)
    lugar(R, t_rio, t_que - 0.1, "EL NILO", (29.4, 26.4), off=(0, 0), px=60)
    R.snd(t_rio, "brillo", 0.4)
    # la pregunta
    titulo(R, t_que, FIN(e) + 1.4, "¿QUÉ PAÍS O IMPERIO SIGUE?", px=78)
    pa(R, C.globo_dialogo(), 1560, 640, 0.85, t_dim - 0.2, FIN(e) + 1.4, sem=391)
    R.texto(t_dim, FIN(e) + 1.3, "¡DÍMELO!", (1560, 610), px=56, d=0.4)
    R.texto(t_com - 0.2, FIN(e) + 1.3, "SUSCRÍBETE", (880, 960), px=72, d=0.6)
    pa(R, C.campana(), 1250, 950, 0.9, t_com - 0.4, FIN(e) + 1.4, sem=392, extra=[(0.1, "campana", 0.5)])
    pa(R, E1.egipcio_hoy(4, 0), 330, 1010, 1.05, t_pais - 0.2, FIN(e) + 1.4, sem=393)
    pa(R, E1.keops(0, "feliz"), 1520, 1010, 0.82, t_que + 0.2, FIN(e) + 1.4, sem=394, entra="sube", dy=400)
    pa(R, E1.cleopatra(0, "guiño"), 1760, 1010, 0.82, t_que + 0.4, FIN(e) + 1.4, sem=395, entra="sube", dy=400)
    for k, (g, dx) in enumerate((((31.0, 28.1), -90), ((31.5, 27.0), 100), ((32.3, 26.0), -90), ((32.75, 25.3), 90))):
        ga(R, E3.palmera(240), g, t_que + 0.1 * k, FIN(e) + 1.4, s=0.5, off=(dx, 10), sem=396 + k, zs=0.4, z=1)
    andar(R, lambda p: E3.falua(p), tramo(nilo(), (32.7, 25.4), (31.4, 28.6), 20), t_que, 5.5, s=0.38, sem=400, zs=0.3, z=2, fps=4, ease=lambda u: u)


# ------------------------------------------------------------------ cambios de escena procedurales
def _transiciones(R):
    tipos = ["tinta", "pincel", "papel", "portal", "rollo", "puntos", "ola", "pincel", "tinta", "papel", "persianas", "portal", "rollo"]
    colores = [(206, 146, 44), (198, 52, 52), (60, 140, 120), (204, 74, 58), (240, 196, 72), (196, 68, 56), (110, 96, 170), (70, 120, 186),
               (186, 52, 46), (70, 140, 96), (74, 108, 180), (204, 64, 56), (226, 170, 62)]
    ids = [e["id"] for e in __import__("escena_base").TL["escenas"]]
    centros = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]
    for k, tc in enumerate(centros):
        tipo, color = tipos[k % len(tipos)], colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.45, dur=0.8)
