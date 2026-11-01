# -*- coding: utf-8 -*-
"""Coreografía (2/4): el Reino Nuevo (Ahmose expulsa a los hicsos, el imperio hasta el Éufrates, Hatshepsut y la expedición a Punt,
Tutmosis III y Megido), la revolución de Akenatón (Atón, Amarna, Nefertiti, el nombre borrado, Tutankamón y su tesoro), Ramsés II
(Kadesh contra los hititas, el primer tratado de paz, colosos y Abu Simbel) y la decadencia (Pueblos del Mar, nubios, asirios, persas).
Capas: 0 = Egipto, 1 = hititas / Kush, 2 = Asiria / Persia."""
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


def cortes(R):
    pass


def construir(R):
    _reino_nuevo(R)
    _revolucion(R)
    _ramses(R)
    _decadencia(R)


# ------------------------------------------------------------------ REINO NUEVO
def _reino_nuevo(R):
    e = "reino_nuevo"
    i0 = INI(e)
    t_ado, t_cab, t_car, t_exp, t_fun, t_rei = T(e, "adoptan"), T(e, "caballos"), T(e, "carros"), T(e, "expulsar"), T(e, "fundan"), T(e, "reino")
    t_eg, t_imp, t_mil, t_lle, t_euf = T(e, "egipto", frase=1), T(e, "imperio", frase=1), T(e, "militar"), T(e, "llega"), T(e, "eufrates")
    t_rei2, t_hat, t_far, t_env, t_exped, t_mar = T(e, "reina"), T(e, "hatshepsut"), T(e, "faraon", frase=2), T(e, "enviando"), T(e, "expediciones"), T(e, "mar")
    t_suc, t_tut, t_expa, t_fron, t_estr = T(e, "sucesor"), T(e, "tutmosis"), T(e, "expande"), T(e, "fronteras"), T(e, "estratega")
    # cámara
    R.camara(i0 - 0.2, 32.0, 28.6, 2.2)
    R.camara(t_exp, 32.2, 29.3, 2.3)
    R.camara(t_rei, 32.4, 29.5, 2.2)
    R.camara(t_imp, 34.8, 31.6, 1.0)
    R.camara(t_euf + 0.6, 35.0, 32.0, 1.02)
    R.camara(t_rei2, 36.0, 20.3, 1.25)
    R.camara(t_mar + 0.4, 36.2, 19.9, 1.28)
    R.camara(t_tut, 35.9, 32.6, 2.3)
    R.camara(FIN(e) + 0.6, 36.1, 33.2, 2.2)
    # años
    R.anio(i0 + 0.1, -1550)
    R.anio(t_eg, -1504)
    R.anio(t_rei2, -1479)
    R.anio(t_suc, -1458)
    # caballos + carro: los egipcios adoptan el arma de los hicsos
    R.morf(E3.caballo(0), E3.carro(0, "ahmose"), t_car - 0.1, 0.6, (1470, 1010, 0.62), sem=110, salida=t_fun, t_a=t_cab - 0.1)
    R.texto(t_cab + 0.1, t_car - 0.2, "CABALLOS", (1470, 640), px=48, d=0.4)
    R.texto(t_car + 0.5, t_fun - 0.1, "CARROS DE GUERRA", (1470, 640), px=48, d=0.5)
    R.snd(t_cab, "galope", 0.4, dur=0.8)
    # Ahmose expulsa a los hicsos
    P_up = tramo(nilo("damieta"), CI["tebas"], (31.8, 30.8), 24)
    andar(R, lambda p: E3.carro(p, "ahmose"), P_up, t_exp - 0.6, 2.6, t1=t_rei + 0.4, s=0.3, sem=111, zs=0.4, z=3, fps=9)
    andar(R, lambda p: E3.carro(p + 1, "egipcio"), P_up, t_exp - 0.3, 2.6, t1=t_rei + 0.4, s=0.27, sem=112, zs=0.4, z=3, fps=9, off=(110, 40))
    R.snd(t_exp - 0.5, "galope", 0.5, dur=2.4)
    for k in range(2):
        andar(R, lambda p, k=k: E3.carro(p, "hicso", (170, 120, 160)), M.RUTAS["hicsos_fuera"], t_exp + 0.6 + 0.2 * k, 2.2, t1=t_rei + 0.4, s=0.27,
              sem=113 + k, zs=0.4, z=2, fps=9, off=formacion(k, 2, 150))
    titulo(R, t_exp, t_fun + 0.2, "¡FUERA LOS HICSOS!", px=78)
    R.terreno(t_exp + 0.6, None, COL["hicsos"], 1.2, capa=1)
    R.terreno(t_exp + 0.6, "reino_antiguo", COL["reino_nuevo"], 1.2)
    R.texto(t_exp + 1.4, t_rei + 0.4, "AHMOSE", (560, 520), px=52, d=0.4)
    R.sello(t_rei + 0.1, "ojo", "REINO NUEVO", color=(196, 60, 50))
    # un imperio hasta el Éufrates y Nubia
    R.terreno(t_imp - 0.2, "imp_1350", COL["reino_nuevo"], 1.6)
    R.texto(t_imp, t_rei2 - 0.2, "UN IMPERIO", (520, 930), px=84, d=0.6)
    R.ruta(M.RUTAS["tutmosis"], t_imp - 0.2, 2.8, ancho=5.0, t1=t_rei2 - 0.1, flecha=True)
    grupo(R, lambda p: E1.soldado_eg(p % 2, "serio"), M.RUTAS["tutmosis"], t_imp, 3.2, n=3, ancho=110, t1=t_rei2 - 0.1, s=0.42, sem=115, fps=6)
    andar(R, lambda p: E3.carro(p, "egipcio"), M.RUTAS["tutmosis"], t_imp - 0.3, 3.0, t1=t_rei2 - 0.1, s=0.36, sem=118, zs=0.4, z=3, fps=9, off=(0, 50))
    R.snd(t_mil, "tambor", 0.45)
    R.snd(t_mil + 0.4, "pasos", 0.4, dur=2.0)
    R.terreno(t_euf - 0.3, "reino_nuevo", COL["reino_nuevo"], 1.0)
    ciudad(R, t_euf - 0.2, t_rei2 - 0.6, "carquemis", "CARQUÉMIS", "izq", 40)
    lugar(R, t_euf, t_rei2 - 0.6, "RÍO ÉUFRATES", (40.8, 35.4), off=(0, 0), px=46)
    R.snd(t_euf, "ding", 0.4)
    # Hatshepsut y la expedición al país de Punt
    pa(R, E1.hatshepsut(0, "feliz"), 330, 1010, 1.15, t_hat - 0.2, t_suc + 0.1, sem=121, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_hat + 0.1, t_suc, "HATSHEPSUT", (330, 610), px=54, d=0.5)
    R.texto(t_far + 0.1, t_suc, "MUJER FARAÓN", (330, 540), px=38, d=0.4)
    R.ruta(M.RUTAS["punt"], t_env, 2.6, ancho=5.0, t1=t_suc + 0.1, flecha=True)
    andar(R, lambda p: E3.barco_punt(p), M.RUTAS["punt"], t_env + 0.1, 3.2, t1=t_mar + 0.6, s=0.42, sem=123, zs=0.4, z=2, fps=4)
    R.snd(t_env + 0.3, "ola", 0.4, dur=1.2)
    andar(R, lambda p: E3.barco_punt(p), M.RUTAS["punt_vuelta"], t_mar + 0.5, 1.6, t1=t_suc + 0.1, s=0.42, sem=124, zs=0.4, z=2, fps=4, entra="fija")
    ciudad(R, t_exped + 0.4, t_suc - 0.4, "punt", "PUNT", "der", 50)
    for k, (dib, dx, dy) in enumerate(((E3.jirafa(), -150, -10), (E3.babuino(), 120, 40), (E3.arbol_incienso(), 210, 20), (E3.arbol_incienso(), -60, 50))):
        ga(R, dib, CI["punt"], t_exped + 0.7 + 0.15 * k, t_suc + 0.1, s=0.3 if k == 0 else 0.32, off=(dx, dy), sem=125 + k, zs=0.4, z=2)
    lugar(R, t_exped + 1.0, t_suc - 0.4, "INCIENSO, ORO, ÉBANO", CI["punt"], off=(-60, -230), px=40)
    lugar(R, t_mar - 0.1, t_suc - 0.4, "MAR ROJO", (38.4, 19.6), off=(0, 0), px=52)
    # Tutmosis III: Megido y diecisiete campañas
    P_tut = [(31.88, 30.98), (32.57, 31.04), (34.45, 31.5), (35.18, 32.58)]
    andar(R, lambda p: E3.carro(p, "tutmosis"), P_tut, t_tut - 0.3, 2.0, t1=FIN(e) + 0.4, s=0.4, sem=129, zs=0.4, z=3, fps=9)
    grupo(R, lambda p: E1.soldado_eg(p % 2, "serio"), [(31.88, 30.85), (32.7, 30.75), (34.55, 31.05)], t_tut - 0.1, 2.0, n=3, ancho=100, t1=FIN(e) + 0.4, s=0.34, sem=130, fps=6)
    R.snd(t_tut - 0.2, "galope", 0.45, dur=1.8)
    lugar(R, t_tut + 0.3, FIN(e) + 0.3, "TUTMOSIS III", CI["megido"], off=(-60, -200), px=48)
    ciudad(R, t_expa, FIN(e) + 0.4, "megido", "MEGIDO", "der", 44)
    ga(R, A.espadas(), CI["megido"], t_expa + 0.2, FIN(e) + 0.4, s=0.32, off=(170, -60), sem=133, zs=0.3, z=3, extra=[(0.05, "espada", 0.5)])
    R.contador(t_fron, t_fron + 1.0, 1, 17, (960, 196), px=84, formato="{} CAMPAÑAS", hasta_t=FIN(e) + 0.3)
    R.snd(t_fron, "tambor", 0.35)
    pa(R, E1.tutmosis(0, "serio"), 1620, 1010, 1.05, t_estr - 0.4, FIN(e) + 0.4, sem=134)
    R.texto(t_estr, FIN(e) + 0.3, "GRAN ESTRATEGA", (1620, 640), px=42, d=0.4)


# ------------------------------------------------------------------ AKENATÓN, ATÓN Y TUTANKAMÓN
def _revolucion(R):
    e = "revolucion"
    i0 = INI(e)
    t_mil, t_far, t_reb, t_con, t_ake = T(e, "mil"), T(e, "faraon"), T(e, "rebelde"), T(e, "conmociona"), T(e, "akenaton")
    t_pro, t_dio, t_imp, t_sol, t_aton = T(e, "prohibe"), T(e, "dioses"), T(e, "impone"), T(e, "sol"), T(e, "aton")
    t_fun, t_cap, t_des, t_rei, t_nef, t_tra, t_arte = (T(e, "funda"), T(e, "capital"), T(e, "desierto"), T(e, "reina"), T(e, "nefertiti"), T(e, "transforma"),
                                                        T(e, "arte"))
    t_mue, t_sac, t_res, t_vie, t_bor, t_nom = T(e, "muerte"), T(e, "sacerdotes"), T(e, "restauran"), T(e, "viejas"), T(e, "borran"), T(e, "nombre")
    t_jov, t_tut, t_rest, t_sep, t_tes, t_oro = T(e, "joven"), T(e, "tutankamon"), T(e, "restablece"), T(e, "sepultado"), T(e, "tesoro"), T(e, "oro")
    # cámara
    R.camara(i0 - 0.2, 31.4, 27.3, 2.6)
    R.camara(t_pro, 31.2, 27.5, 3.0)
    R.camara(t_fun + 0.1, 30.95, 27.68, 7.0)
    R.camara(t_arte + 0.6, 30.92, 27.66, 7.6)
    R.camara(t_sac, 31.5, 26.9, 3.2)
    R.camara(t_jov, 32.56, 25.76, 8.4)
    R.camara(FIN(e) + 0.6, 32.58, 25.75, 9.0)
    # años
    R.anio(t_mil, -1353)
    R.anio(t_fun, -1346)
    R.anio(t_mue, -1336)
    R.anio(t_jov, -1332)
    # territorio: el imperio se tiñe del oro de Atón y vuelve al rojo con los sacerdotes
    R.terreno(i0 - 0.6, "imp_1350", COL["reino_nuevo"], 0.5)
    R.terreno(t_imp, "imp_1350", COL["aton"], 1.2)
    R.terreno(t_res, "imp_1350", COL["reino_nuevo"], 1.0)
    # el faraón rebelde
    ga(R, E2.templo_karnak(), CI["karnak"], i0, t_reb + 0.3, s=0.42, off=(0, 20), sem=140, zs=0.4, z=1)
    for k in range(3):
        ga(R, E1.sacerdote(k % 2, "feliz"), CI["karnak"], i0 + 0.3 + 0.15 * k, t_reb + 0.3, s=0.36, off=(-170 + 110 * k, 110), sem=141 + k, zs=0.4, z=2)
    lugar(R, i0 + 0.2, t_reb + 0.2, "TEMPLO DE AMÓN", CI["karnak"], off=(0, -200), px=42)
    pa(R, E1.akenaton(0, "enojo"), 330, 1010, 1.15, t_far - 0.1, t_mue + 0.2, sem=144, sale="caer", extra=[(0.05, "impacto", 0.4)])
    titulo(R, t_reb - 0.1, t_pro - 0.1, "UN FARAÓN REBELDE", px=74)
    R.texto(t_ake, t_fun - 0.2, "AKENATÓN", (330, 600), px=54, d=0.4)
    # fuera los dioses: solo Atón
    X = [780, 960, 1140, 1320, 1500]
    dioses = ("amon", "ra", "anubis", "osiris", "bastet")
    for k, q in enumerate(dioses):
        pa(R, E2.dios(q), X[k], 1010, 0.6, t_dio - 0.2 + 0.12 * k, t_imp + 0.9, sem=145 + k, sale="caer", d_out=0.6)
        pa(R, E2.tachar(), X[k], 1000, 0.6, t_imp - 0.2 + 0.1 * k, t_imp + 0.9, sem=150 + k, entra="pluma", d_in=0.25, sale="caer", d_out=0.6, z=3)
    R.snd(t_dio - 0.2, "pluck", 0.35)
    R.snd(t_imp - 0.2, "borrar", 0.5, dur=0.6)
    R.texto(t_dio + 0.3, t_imp + 0.8, "LOS DIOSES DE SIEMPRE", (1140, 660), px=44, d=0.5)
    pa(R, E2.disco_aton(), 1140, 900, 1.0, t_sol - 0.4, t_fun - 0.1, sem=155, entra="sube", dy=600, extra=[(0.05, "amanecer", 0.45, {"dur": 2.0})])
    R.sello(t_aton, "aton", "CULTO A ATÓN", color=(222, 160, 40))
    # Ajetatón (Amarna) y Nefertiti
    ciudad(R, t_cap - 0.1, t_mue + 0.2, "amarna", "AJETATÓN (AMARNA)", "der", 44)
    ga(R, E2.ciudad_antigua(), CI["amarna"], t_cap, t_mue + 0.2, s=0.42, off=(-40, -30), sem=156, zs=0.5, z=1, entra="sube", dy=300,
       extra=[(0.05, "crece", 0.45)])
    ga(R, E2.disco_aton(n=9), CI["amarna"], t_cap + 0.4, t_mue + 0.2, s=0.24, off=(-40, -150), sem=157, zs=0.5, z=1)
    lugar(R, t_des, t_rei, "EN MEDIO DEL DESIERTO", CI["amarna"], off=(0, 110), px=40)
    pa(R, E1.nefertiti(0, "feliz"), 1600, 1010, 1.1, t_nef - 0.2, t_mue + 0.2, sem=158, extra=[(0.05, "brillo", 0.4)])
    R.texto(t_nef + 0.1, t_mue, "NEFERTITI", (1600, 590), px=54, d=0.4)
    pa(R, E2.busto_nefertiti(), 960, 1010, 0.82, t_arte - 0.3, t_mue + 0.2, sem=159, entra="pluma", d_in=1.0, extra=[(0.05, "pincel", 0.4, {"dur": 0.9})])
    R.texto(t_arte + 0.3, t_mue, "UN ARTE NUEVO", (960, 640), px=42, d=0.4)
    # los sacerdotes restauran a los dioses y borran su nombre
    for k in range(3):
        pa(R, E1.sacerdote(k % 2, "enojo" if k == 1 else "serio"), 260 + 230 * k, 1010, 0.92, t_sac - 0.1 + 0.15 * k, t_jov - 0.1, sem=160 + k)
    for k, q in enumerate(dioses):
        pa(R, E2.dios(q), 1000 + 165 * k, 1010, 0.55, t_vie - 0.3 + 0.12 * k, t_jov - 0.1, sem=163 + k, entra="cae", dy=500)
    R.snd(t_vie - 0.2, "ding", 0.35)
    titulo(R, t_res, t_jov - 0.2, "VUELVEN LOS DIOSES", px=72)
    R.morf(E2.cartucho(("sol", "pajaro", "anj")), E2.cartucho(("sol", "pajaro", "anj"), True), t_bor + 0.1, 0.6, (1330, 600, 0.95), sem=168,
           salida=t_jov - 0.1, t_a=t_bor - 0.6)
    R.snd(t_bor + 0.1, "borrar", 0.55, dur=0.6)
    R.texto(t_nom + 0.4, t_jov - 0.2, "NOMBRE BORRADO", (1330, 330), px=44, d=0.4)
    # Tutankamón y su tesoro
    pa(R, E1.tutankamon(0, "feliz"), 330, 1010, 0.95, t_tut - 0.2, FIN(e) + 0.4, sem=170, extra=[(0.05, "pluck", 0.4)])
    R.texto(t_tut + 0.1, FIN(e) + 0.3, "TUTANKAMÓN", (330, 650), px=52, d=0.4)
    R.texto(t_tut + 0.4, FIN(e) + 0.3, "REY A LOS 9 AÑOS", (330, 590), px=34, d=0.4)
    pa(R, E2.dios("amon"), 590, 1010, 0.62, t_rest - 0.1, FIN(e) + 0.4, sem=171, entra="cae", dy=500)
    ga(R, E2.tumba_valle(), CI["valle_reyes"], t_sep - 0.3, FIN(e) + 0.4, s=0.42, off=(-40, 10), sem=172, zs=0.5, z=1, entra="sube", dy=300)
    lugar(R, t_sep, FIN(e) + 0.3, "VALLE DE LOS REYES", CI["valle_reyes"], off=(-40, 60), px=40)
    pa(R, E2.sarcofago(), 880, 1010, 0.62, t_sep + 0.3, FIN(e) + 0.4, sem=173)
    pa(R, E2.tesoro(), 1230, 1010, 0.82, t_tes - 0.1, FIN(e) + 0.4, sem=174, extra=[(0.05, "monedas", 0.45)])
    pa(R, E2.mascara_tut(), 1620, 1010, 0.72, t_oro - 0.4, FIN(e) + 0.4, sem=175, extra=[(0.05, "bling", 0.5)])
    R.texto(t_oro, FIN(e) + 0.3, "HALLADA EN 1922", (1620, 720), px=36, d=0.4)


# ------------------------------------------------------------------ RAMSÉS II
def _ramses(R):
    e = "ramses"
    i0 = INI(e)
    t_sub, t_tro, t_far, t_ram, t_seg = T(e, "sube"), T(e, "trono"), T(e, "faraon"), T(e, "ramses", frase=0), T(e, "segundo")
    t_mil, t_comb, t_imp, t_hit, t_gig, t_bat, t_kad = (T(e, "mil"), T(e, "combate"), T(e, "imperio"), T(e, "hitita"), T(e, "gigantesca"), T(e, "batalla"),
                                                        T(e, "kadesh"))
    t_tras, t_fir, t_tra, t_paz, t_hist = T(e, "tras"), T(e, "firma"), T(e, "tratado"), T(e, "paz"), T(e, "historia")
    t_ram2, t_col, t_tem, t_roca, t_abu, t_rei, t_ses = (T(e, "ramses", frase=3), T(e, "colosos"), T(e, "templos"), T(e, "roca"), T(e, "abu"), T(e, "reina"),
                                                         T(e, "sesenta"))
    # cámara
    R.camara(i0 - 0.2, 31.6, 27.4, 2.3)
    R.camara(t_seg, 31.7, 27.8, 2.25)
    R.camara(t_comb, 35.2, 35.6, 1.45)
    R.camara(t_gig, 35.6, 35.3, 1.7)
    R.camara(t_kad - 0.1, 36.3, 34.9, 3.0)
    R.camara(t_hist + 0.2, 36.0, 34.4, 2.9)
    R.camara(t_ram2 + 0.1, 31.8, 28.1, 2.0)
    R.camara(t_roca, 31.9, 26.0, 2.2)
    R.camara(t_abu - 0.1, 31.75, 22.7, 5.3)
    R.camara(FIN(e) + 0.6, 31.7, 22.55, 5.0)
    # años
    R.anio(i0 + 0.2, -1279)
    R.anio(t_mil, -1274)
    R.anio(t_tras, -1259)
    R.anio(t_ram2, -1265)
    R.anio(t_rei, -1213)
    # Ramsés sube al trono
    pa(R, E2.trono_eg(), 1290, 1010, 0.82, t_sub - 0.2, t_mil, sem=180, entra="sube", dy=400)
    pa(R, E1.ramses(0, "serio", "pschent"), 1060, 1010, 1.1, t_far - 0.2, t_mil, sem=181, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_ram, t_mil - 0.1, "RAMSÉS II", (1060, 600), px=58, d=0.4)
    titulo(R, t_far, t_mil - 0.1, "EL MÁS CÉLEBRE", px=74)
    for k in range(4):
        pa(R, A.estrella5(), 800 + 520 * (k % 2), 560 + 160 * (k // 2), 0.5, t_ram + 0.1 * k, t_mil, sem=182 + k, extra=[(0.0, "estrellitas", 0.3)] if k == 0 else ())
    R.sello(t_seg - 0.1, "cartucho", "RAMSÉS II", color=(196, 68, 56))
    # Kadesh: egipcios contra hititas, la mayor batalla de carros
    R.terreno(t_mil, "ramses", COL["ramses"], 1.0)
    R.terreno(t_imp - 0.2, "hititas", COL["hititas"], 1.0, capa=1)
    lugar(R, t_hit, t_gig, "IMPERIO HITITA", (34.0, 38.6), off=(0, 0), px=52)
    ga(R, E1.rey_hitita(0, "enojo"), CI["hattusa"], t_hit - 0.1, t_gig, s=0.42, off=(0, 120), sem=187, zs=0.4, z=2)
    ciudad(R, t_hit, t_gig, "hattusa", "HATTUSA", "der", 38)
    for k in range(3):
        andar(R, lambda p, k=k: E3.carro(p + k, "ramses" if k == 0 else "egipcio"), M.RUTAS["kadesh_eg"], t_comb - 0.4 + 0.15 * k, t_kad - t_comb + 0.3,
              t1=t_tras + 0.2, s=0.24, sem=188 + k, zs=0.5, z=3, fps=9, off=formacion(k, 3, 130))
        andar(R, lambda p, k=k: E3.carro(p + k, "hitita", (150, 160, 200), (120, 100, 90), (110, 120, 170)), M.RUTAS["kadesh_hit"][1:], t_comb - 0.2 + 0.15 * k,
              t_kad - t_comb + 0.1, t1=t_tras + 0.2, s=0.24, sem=191 + k, zs=0.5, z=3, fps=9, off=formacion(k, 3, 130))
    R.snd(t_comb - 0.3, "galope", 0.55, dur=3.6)
    titulo(R, t_gig - 0.1, t_tras, "BATALLA DE KADESH", px=76)
    ciudad(R, t_kad - 0.3, t_hist, "kadesh", "KADESH", "abajo", 46)
    ga(R, A.estallido(14, 50, 150), CI["kadesh"], t_kad - 0.1, t_kad + 0.6, s=0.7, off=(0, -60), entra="fija", sale="cortar", sem=194, zs=0.3, z=4,
       extra=[(0.0, "explosion", 0.4)])
    ga(R, A.espadas(), CI["kadesh"], t_kad + 0.2, t_tras + 0.2, s=0.4, off=(0, -70), sem=195, zs=0.3, z=4, extra=[(0.05, "espada", 0.55)])
    # el primer tratado de paz
    pa(R, E2.tratado(), 960, 1000, 0.95, t_fir - 0.2, t_ram2 - 0.1, sem=196, extra=[(0.05, "sello", 0.5)])
    titulo(R, t_tra - 0.1, t_ram2 - 0.2, "PRIMER TRATADO DE PAZ", px=72)
    pa(R, lambda t: E3.paloma(int(t * 5) % 2), lambda t: lerp(380, 1560, prog(t, t_paz, t_hist + 1.2)), lambda t: 560 - 90 * math.sin(prog(t, t_paz, t_hist + 1.2) * math.pi), 0.9,
       t_paz, t_ram2 - 0.1, sem=197, extra=[(0.05, "pio", 0.4)])
    R.terreno(t_hist, None, COL["hititas"], 1.0, capa=1)
    # colosos, templos y Abu Simbel
    for k, (g, dx) in enumerate(((CI["tebas"], -90), (CI["abidos"], -90), (CI["menfis"], -90))):
        ga(R, E2.coloso(), g, t_col - 0.2 + 0.18 * k, t_abu - 0.8, s=0.26, off=(dx, 20), sem=198 + k, zs=0.4, z=2, entra="sube", dy=300)
    R.snd(t_col - 0.2, "crece", 0.45, dur=0.9)
    for k, (g, dx) in enumerate(((CI["karnak"], 110), (CI["abidos"], 110))):
        ga(R, E2.templo_karnak(), g, t_tem - 0.2 + 0.2 * k, t_abu - 0.8, s=0.22, off=(dx, 20), sem=201 + k, zs=0.4, z=1, entra="sube", dy=300)
    lugar(R, t_col, t_abu - 0.9, "LUXOR", CI["tebas"], off=(-90, 60), px=36)
    lugar(R, t_tem, t_abu - 0.9, "ABIDOS", CI["abidos"], off=(-90, 60), px=36)
    ga(R, E2.abu_simbel(), CI["abu_simbel"], t_roca - 0.4, FIN(e) + 0.4, s=0.48, off=(-60, 30), sem=203, zs=0.5, z=1, entra="pluma", d_in=1.3,
       extra=[(0.05, "crece", 0.5, {"dur": 1.2})])
    ciudad(R, t_abu - 0.1, FIN(e) + 0.4, "abu_simbel", "ABU SIMBEL", "abajo", 50)
    R.contador(t_ses - 0.2, t_ses + 0.8, 0, 66, (960, 196), px=84, formato="{} AÑOS DE REINADO", hasta_t=FIN(e) + 0.3)
    pa(R, A.arena_reloj(), 1600, 1010, 0.7, t_rei, FIN(e) + 0.4, sem=204, extra=[(0.05, "reloj_rapido", 0.35, {"dur": 1.0})])
    pa(R, E1.ramses(0, "feliz", "pschent"), 320, 1010, 1.05, t_ram2 - 0.1, FIN(e) + 0.4, sem=205)


# ------------------------------------------------------------------ DECADENCIA: Pueblos del Mar, nubios, asirios y persas
def _decadencia(R):
    e = "decadencia"
    i0 = INI(e)
    t_sig, t_pod, t_fra = T(e, "siglos"), T(e, "poder"), T(e, "fragmenta")
    t_eg, t_inv, t_pue, t_nub, t_asi = T(e, "egipto"), T(e, "invasiones"), T(e, "pueblos"), T(e, "nubios"), T(e, "asirios")
    t_qui, t_ejer, t_per, t_conq, t_nilo, t_prov = T(e, "quinientos"), T(e, "ejercitos"), T(e, "persas"), T(e, "conquistan"), T(e, "nilo"), T(e, "provincia")
    t_din, t_rey, t_apa = T(e, "dinastias"), T(e, "reyes"), T(e, "apagan")
    # cámara
    R.camara(i0 - 0.2, 31.5, 27.6, 2.2)
    R.camara(t_eg, 33.6, 28.3, 1.05)
    R.camara(t_asi + 0.4, 34.0, 29.0, 1.0)
    R.camara(t_per + 0.6, 34.0, 29.6, 1.0)
    R.camara(t_nilo, 31.8, 28.0, 1.7)
    R.camara(t_din, 31.5, 27.6, 2.0)
    R.camara(FIN(e) + 0.6, 31.4, 27.6, 2.1)
    # años
    R.anio(t_sig, -1069)
    R.anio(t_nub, -728)
    R.anio(t_asi, -671)
    R.anio(t_qui, -525)
    # el poder se fragmenta
    R.terreno(i0 - 0.4, "reino_antiguo", COL["reino_nuevo"], 1.2)
    R.terreno(i0 - 0.4, None, COL["hititas"], 0.4, capa=1)
    R.romper("tercer", t_fra - 0.2, t_fra + 0.5, t_asi - 0.3, t_qui, capa=0, gap=14.0, deriva=26.0)
    pa(R, E2.corona_doble(), 960, 820, 0.95, t_pod - 0.5, t_eg, sem=210, sale="caer", d_out=0.6)
    pa(R, A.grietas_hueso(), 960, 700, 1.3, t_fra - 0.1, t_eg, sem=211, entra="pluma", d_in=0.3, sale="caer", d_out=0.6, z=3)
    R.snd(t_fra - 0.1, "crujido", 0.55, dur=0.8)
    titulo(R, t_sig, t_eg - 0.1, "EL PODER SE ROMPE", px=74)
    # Pueblos del Mar
    for k in range(2):
        andar(R, lambda p, k=k: E3.barco_pueblos_mar(p), M.RUTAS["pueblos_mar"], t_inv - 0.3 + 0.3 * k, 2.6, t1=t_ejer, s=0.24, sem=212 + k, zs=0.4, z=2,
              fps=4, off=formacion(k, 2, 170))
    R.snd(t_inv - 0.2, "ola", 0.45, dur=1.0)
    lugar(R, t_pue, t_ejer - 0.2, "PUEBLOS DEL MAR", (27.6, 33.6), off=(0, 0), px=46)
    # los faraones nubios de Kush
    R.terreno(t_nub - 0.3, "kush_egipto", COL["kush"], 1.2, capa=1)
    andar(R, lambda p: E1.faraon_nubio(p % 2, "serio"), M.RUTAS["nubios"], t_nub - 0.3, 2.2, t1=t_ejer, s=0.32, sem=214, zs=0.4, z=3, fps=5)
    lugar(R, t_nub + 0.3, t_ejer - 0.2, "FARAONES NUBIOS", (34.3, 22.6), off=(0, 0), px=44)
    R.snd(t_nub, "tambor", 0.4)
    # los asirios
    R.terreno(t_asi - 0.3, "asiria", COL["asiria"], 1.2, capa=2)
    R.terreno(t_asi + 0.6, "kush", COL["kush"], 1.0, capa=1)
    grupo(R, lambda p: E1.asirio(p % 2, "enojo"), M.RUTAS["asirios"][1:], t_asi - 0.4, 2.6, n=3, ancho=80, t1=t_ejer, s=0.22, sem=215, fps=6)
    lugar(R, t_asi + 0.1, t_ejer - 0.2, "ASIRIOS", (40.2, 33.2), off=(0, 0), px=50)
    R.snd(t_asi - 0.3, "cuerno", 0.45)
    # los persas: Egipto, provincia del Imperio aqueménida
    R.terreno(t_ejer - 0.3, "persia", COL["persia"], 1.6, capa=2)
    R.ruta(M.RUTAS["persas"], t_ejer - 0.3, 2.4, ancho=5.0, t1=t_din, flecha=True)
    grupo(R, lambda p: E1.persa(p % 2, "serio"), M.RUTAS["persas"], t_ejer - 0.2, 3.0, n=3, ancho=80, t1=t_din, s=0.22, sem=218, fps=6)
    R.snd(t_ejer - 0.2, "pasos", 0.45, dur=2.4)
    pa(R, E1.persa(0, "serio", True), 330, 1010, 1.05, t_per - 0.2, t_din, sem=221, extra=[(0.05, "cuerno", 0.35)])
    R.texto(t_per + 0.2, t_din - 0.1, "CAMBISES II", (330, 610), px=50, d=0.4)
    lugar(R, t_per, t_nilo - 0.3, "PERSAS", (44.0, 31.8), off=(0, 0), px=52)
    R.terreno(t_conq + 0.6, None, COL["reino_nuevo"], 1.0)
    R.sello(t_prov - 0.6, "alas", "EGIPTO PERSA", color=(110, 96, 170))
    lugar(R, t_prov, FIN(e) + 0.3, "PROVINCIA PERSA", (28.6, 28.6), off=(0, 0), px=50)
    # se apagan las dinastías nativas
    pa(R, E1.faraon(0, "pschent", "lloron", acc_d=None, acc_i=None, brazos=(10, 10)), 760, 1010, 1.05, t_din - 0.1, t_apa + 0.6, sem=222, sale="borrar",
       d_out=0.8)
    pa(R, C.vela(), 1160, 1010, 0.85, t_din, t_apa, sem=223, sale="cortar")
    pa(R, C.humo(), 1160, 860, 0.9, t_apa, FIN(e) + 0.4, sem=224, entra="sube", dy=60, extra=[(0.0, "puf", 0.45)])
    titulo(R, t_rey - 0.2, FIN(e) + 0.3, "FIN DE LOS FARAONES EGIPCIOS", px=64)
