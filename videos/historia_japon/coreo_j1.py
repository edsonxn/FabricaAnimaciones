# -*- coding: utf-8 -*-
"""Coreografía (1/3): gancho, orígenes, imperio Yamato, Heian y el nacimiento del shogunato."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_j as J
import obj_p as P
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402  (después del * para que T sea el tiempo, no el trazo)

COL = M.COL


def lugar(R, t0, t1, txt, geo, off=(0, -60), px=54, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _gancho(R)
    _origenes(R)
    _imperio(R)
    _heian(R)
    _shogun(R)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_arch, t_sam, t_sig, t_emp, t_trono = T(e, "archipielago"), T(e, "samurais"), T(e, "siglos"), T(e, "emperador"), T(e, "trono")
    t_cerro, t_puertas, t_abrio, t_golpe, t_rev = T(e, "cerro"), T(e, "puertas"), T(e, "abrio"), T(e, "golpe"), T(e, "revolucion")
    t_hist, t_jap, t_cinco, t_min = T(e, "historia"), T(e, "japon"), T(e, "cinco"), T(e, "minutos")
    R.terreno(t_arch - 0.1, "japon", COL["japon"], 1.3)
    R.camara(0.0, 136.5, 36.5, 2.2)
    R.camara(t_sam, 135.0, 35.0, 3.2)
    R.camara(t_trono, 135.5, 35.2, 3.6)
    R.camara(t_cerro, 134.0, 35.5, 2.4)
    R.camara(t_rev, 137.0, 36.5, 2.6)
    R.camara(t_jap, 138.0, 37.0, 2.7)
    R.camara(t_min + 0.4, 138.5, 37.0, 2.9)
    R.anio(t_sam - 0.3, 1200)
    R.anio(t_sam + 0.8, 1200)
    R.anio(t_rev - 0.2, 1853)
    R.anio(t_rev + 1.0, 1868)
    # samuráis (con el código del guerrero) y emperador en su trono
    for k, (lon, lat) in enumerate(((139.6, 35.6), (131.0, 33.4), (141.0, 38.3))):
        R.act(lambda t, k=k: J.samurai(int(t * 6) + k), geo=(lon, lat), off=lambda t, k=k: (0, -16 + 6 * math.sin(t * 3 + k)), s=0.5, t_in=t_sam + 0.12 * k, d_in=0.4, entra="pop", sem=500 + k,
              sfx=[(0, "pop", 0.5), (0.05, "clink", 0.4)], t_out=t_cerro - 0.2, sale="encoger", zs=0.6, z=1)
    lugar(R, t_sam, t_sig + 0.4, "SAMURÁIS", (139.6, 35.6), off=(0, -200), px=58)
    R.act(J.emperador_jp(0), geo=(135.77, 35.01), off=(0, 30), s=0.6, t_in=t_emp - 0.1, d_in=0.45, entra="pop", sem=505, sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.4)],
          t_out=t_cerro - 0.2, sale="encoger", zs=0.6, z=1)
    R.act(A.trono(1.0), geo=(135.77, 35.01), off=(0, 60), s=0.5, t_in=t_emp - 0.3, d_in=0.4, entra="pop", sem=506, t_out=t_cerro - 0.2, sale="encoger", zs=0.6, z=0)
    lugar(R, t_emp, t_cerro - 0.3, "EMPERADOR", (135.77, 35.01), off=(0, -200), px=58)
    R.act(J.sol_naciente(), geo=(135.77, 35.01), off=(0, -90), s=0.55, t_in=t_trono - 0.3, d_in=0.5, entra="pop", sem=507, sfx=[(0, "brillo", 0.5)], t_out=t_cerro - 0.2, sale="encoger", zs=0.6, z=0)
    # cierra sus puertas
    R.act(lambda t: Bb.gran_puerta_cerrada(round(kf(t, [(t_cerro, 0.0), (t_puertas + 0.7, 1.0), (t_abrio - 0.2, 1.0), (t_abrio + 0.6, 0.0)]), 1)),
          pos=(960, 820, 1.05), t_in=t_cerro - 0.05, d_in=0.45, entra="pop", sem=508, sfx=[(0, "pop", 0.5), (0.4, "golpe_suave", 0.6)], t_out=t_golpe - 0.1, sale="encoger", z=2)
    R.texto(t_puertas - 0.1, t_abrio - 0.1, "PUERTAS CERRADAS", (960, 230), px=84, d=0.9)
    R.snd(t_puertas, "escribir", 0.5, dur=0.9)
    R.snd(t_abrio, "crujido", 0.8, dur=0.8)
    # ... y las abre de golpe
    R.act(A.estallido(16, 50, 160), pos=(960, 640, 1.5), t_in=t_golpe, d_in=0.15, entra="fija", sem=509, sfx=[(0, "explosion", 0.6)], t_out=t_golpe + 0.5, sale="cortar", z=3)
    R.act(J.barco_negro(0), pos=lambda t: (lerp(2100, 1450, e_out(prog(t, t_golpe, t_rev + 0.8))), 850 + 10 * math.sin(t * 3), 0.6), t_in=t_golpe, d_in=0.3, entra="fija", sem=510,
          sfx=[(0, "cuerno", 0.5)], t_out=t_hist - 0.1, sale="izq_fuera", d_out=0.8, z=1)
    R.texto(t_rev - 0.1, t_hist - 0.2, "¡REVOLUCIÓN!", (960, 230), px=100, d=0.8)
    R.snd(t_rev, "escribir", 0.5, dur=0.8)
    # título
    R.texto(t_jap - 0.3, FIN(e) + 1.0, "JAPÓN", (960, 210), px=150, d=0.9)
    R.texto(t_cinco - 0.1, FIN(e) + 1.0, "EN 5 MINUTOS", (960, 380), px=88, d=0.8)
    R.snd(t_jap, "escribir", 0.5, dur=0.9)
    R.snd(t_cinco, "pluck", 0.5)
    R.act(J.cerezo(0), geo=(140.5, 36.0), off=(0, 0), s=0.6, t_in=t_min - 0.2, d_in=0.6, entra="pluma", sem=511, sfx=[(0, "brillo", 0.4)], zs=0.5, z=1)


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_todo, t_islas, t_volc, t_bosq, t_16 = T(e, "todo"), T(e, "islas"), T(e, "volcanes"), T(e, "bosques"), T(e, "dieciseis")
    t_jomon, t_fab, t_cer = T(e, "jomon"), T(e, "fabrica"), T(e, "ceramicas")
    t_300, t_arroz, t_metal, t_agri = T(e, "trescientos"), T(e, "arroz"), T(e, "metal"), T(e, "agricultores")
    t_jefes, t_tumbas, t_ojo, t_estadio = T(e, "jefes"), T(e, "tumbas"), T(e, "ojo"), T(e, "estadio")
    t_ley, t_660, t_jimmu, t_funda, t_diosa, t_sol = T(e, "leyenda"), T(e, "seiscientos"), T(e, "jimmu"), T(e, "funda"), T(e, "diosa"), T(e, "sol")
    R.terreno(i0 - 0.2, "japon", COL["jomon"], 0.8)
    R.terreno(t_300 - 0.1, "yayoi", COL["yayoi"], 1.4)
    R.camara(i0 - 0.3, 138.0, 37.0, 2.9)
    R.camara(t_todo, 137.5, 36.5, 3.4)
    R.camara(t_jomon - 0.3, 138.5, 36.0, 4.2)
    R.camara(t_300 - 0.3, 131.5, 33.3, 5.2)
    R.camara(t_jefes - 0.3, 135.2, 34.6, 6.0)
    R.camara(t_ojo, 135.49, 34.56, 9.0)
    R.camara(t_ley - 0.2, 135.8, 34.6, 5.0)
    R.camara(t_sol + 0.3, 135.6, 34.8, 4.4)
    R.camara(FIN(e), 135.8, 35.0, 4.0)
    R.anio(i0, -14000)
    R.anio(t_16 + 0.5, -14000)
    R.anio(t_300 - 0.3, -14000)
    R.anio(t_300 + 0.8, -300)
    R.anio(t_ley, -300)
    R.anio(t_660 + 0.9, -660)
    # islas de volcanes y bosques
    R.act(J.monte_fuji(), geo=(138.73, 35.36), off=(0, 50), s=0.42, t_in=t_volc - 0.1, d_in=0.5, entra="pluma", sem=520, sfx=[(0, "crece", 0.5, {"dur": 0.6})], t_out=t_jomon + 0.4, sale="encoger", zs=0.5, z=1)
    for k, (lon, lat) in enumerate(((140.6, 37.6), (137.4, 36.9), (132.6, 35.0))):
        R.act(lambda t, k=k: A.nube_cielo(), geo=(lon, lat + 2.0), off=lambda t, k=k: (12 * math.sin(t * 0.8 + k), 0), s=0.5, t_in=t_islas + 0.1 * k, d_in=0.4, entra="pop", sem=524 + k, t_out=t_jomon, sale="encoger", zs=0.4)
    R.texto(t_todo - 0.1, t_jomon - 0.4, "HACE 16.000 AÑOS", (960, 200), px=86, d=1.0)
    R.snd(t_todo, "escribir", 0.5, dur=1.0)
    # el pueblo jomon y su cerámica
    R.act(J.vasija_jomon(), geo=(139.0, 36.5), off=(0, 40), s=0.8, t_in=t_fab, d_in=0.5, entra="pop", sem=527, sfx=[(0, "pop", 0.6), (0.1, "plop", 0.5)], t_out=t_300 - 0.3, sale="encoger", zs=0.5, z=1)
    R.act(J.vasija_jomon(), geo=(140.4, 38.0), off=(0, 30), s=0.6, t_in=t_cer, d_in=0.5, entra="pop", sem=528, sfx=[(0, "pop", 0.5)], t_out=t_300 - 0.3, sale="encoger", zs=0.5, z=1, flip=True)
    R.act(J.campesino_jp(0), geo=(137.6, 37.0), off=(0, 30), s=0.46, t_in=t_jomon - 0.1, d_in=0.45, entra="pop", sem=529, sfx=[(0, "pop", 0.5)], t_out=t_300 - 0.3, sale="encoger", zs=0.5, z=1)
    lugar(R, t_jomon, t_300 - 0.4, "JOMON", (139.0, 36.5), off=(0, -170), px=64)
    # llegan el arroz y el metal (Yayoi)
    R.sello(t_300 + 0.3, "弥", "Yayoi", color=(206, 140, 40))
    for k, dx in enumerate((-120, 0, 120)):
        R.act(lambda t, k=k: J.arroz_planta(int(t * 6) + k), geo=(130.6, 33.3), off=(dx, 20), s=0.55, t_in=t_arroz + 0.12 * k, d_in=0.45, entra="pop", sem=530 + k, sfx=[(0, "pop", 0.4)],
              t_out=t_jefes - 0.2, sale="encoger", zs=0.5, z=1)
    R.act(A.espadas(), geo=(131.5, 33.2), off=(120, -20), s=0.5, t_in=t_metal, d_in=0.4, entra="pop", sem=533, sfx=[(0, "clink", 0.6)], t_out=t_jefes - 0.2, sale="encoger", zs=0.5, z=2)
    lugar(R, t_arroz, t_jefes - 0.3, "ARROZ Y METAL", (130.8, 33.3), off=(0, -160), px=58)
    # tumbas con forma de ojo de cerradura
    R.act(J.kofun(), geo=(135.49, 34.56), off=(0, 0), s=0.6, t_in=t_tumbas, d_in=0.7, entra="pluma", sem=534, sfx=[(0, "crece", 0.5, {"dur": 0.7})], t_out=t_ley - 0.3, sale="encoger", zs=0.9, z=1)
    R.act(J.samurai_paz(0, "serio"), geo=(135.49, 34.56), off=(380, -80), s=0.85, t_in=t_estadio - 0.2, d_in=0.45, entra="pop", sem=535, sfx=[(0, "pop", 0.5)], t_out=t_ley - 0.3, sale="encoger", zs=0.7, z=2)
    R.texto(t_ojo - 0.1, t_ley - 0.3, "TUMBA EN FORMA DE OJO DE CERRADURA", (960, 190), px=64, d=1.3)
    R.snd(t_ojo, "escribir", 0.5, dur=1.2)
    # la leyenda del primer emperador
    R.act(J.emperador_jp(0), geo=(135.8, 34.5), off=(0, 40), s=0.72, t_in=t_jimmu - 0.1, d_in=0.45, entra="pop", sem=537, sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.5)], zs=0.6, z=1)
    R.act(J.sol_naciente(), geo=(135.8, 34.5), off=(0, -250), s=0.62, t_in=t_diosa - 0.2, d_in=0.5, entra="pop", sem=538, sfx=[(0, "brillo", 0.6)], zs=0.6, z=0)
    R.texto(t_jimmu - 0.1, FIN(e) + 0.3, "JIMMU, SEGÚN LA LEYENDA", (960, 190), px=74, d=1.1)
    R.snd(t_jimmu, "escribir", 0.5, dur=1.0)
    R.snd(t_diosa, "campana", 0.4)


# ------------------------------------------------------------------ IMPERIO YAMATO
def _imperio(R):
    e = "imperio"
    i0 = INI(e)
    t_tiempo, t_yam, t_unif, t_islas, t_jefes, t_emps = T(e, "tiempo"), T(e, "yamato"), T(e, "unifica"), T(e, "islas"), T(e, "jefes"), T(e, "emperadores")
    t_corea, t_china, t_escr, t_budi, t_gob = T(e, "corea"), T(e, "china"), T(e, "escritura"), T(e, "budismo"), T(e, "gobernar")
    t_604, t_princ, t_sho, t_const, t_17 = T(e, "seiscientos"), T(e, "principe"), T(e, "shotoku"), T(e, "constitucion"), T(e, "diecisiete")
    t_cap, t_nara, t_desp, t_794, t_kioto = T(e, "capital"), T(e, "nara"), T(e, "despues"), T(e, "setecientos"), T(e, "kioto")
    R.terreno(t_yam - 0.3, "kinai", COL["yamato"], 0.9)
    R.terreno(t_unif - 0.1, "yamato_exp", COL["yamato"], 1.6)
    R.sello(t_yam + 0.1, "和", "Yamato", color=(186, 60, 60))
    R.camara(i0 - 0.3, 135.8, 35.0, 4.0)
    R.camara(t_yam, 135.4, 34.8, 5.2)
    R.camara(t_unif, 133.4, 34.4, 3.6)
    R.camara(t_corea - 0.2, 131.0, 35.2, 3.2)
    R.camara(t_budi, 135.0, 34.6, 4.2)
    R.camara(t_604 - 0.2, 135.3, 34.7, 5.6)
    R.camara(t_nara - 0.3, 135.8, 34.8, 6.4)
    R.camara(t_kioto - 0.6, 135.8, 34.9, 6.2)
    R.camara(FIN(e), 135.8, 35.0, 5.6)
    R.anio(i0, -660)
    R.anio(t_tiempo + 0.2, 300)
    R.anio(t_604 - 0.3, 300)
    R.anio(t_604 + 0.5, 604)
    R.anio(t_nara - 0.2, 604)
    R.anio(t_nara + 0.5, 710)
    R.anio(t_794 - 0.1, 710)
    R.anio(t_794 + 0.9, 794)
    # el clan Yamato unifica las islas
    R.act(J.emperador_jp(1), geo=(135.5, 34.6), off=(0, 40), s=0.64, t_in=t_emps - 0.1, d_in=0.45, entra="pop", sem=540, sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.5)], t_out=t_corea - 0.2, sale="encoger", zs=0.6, z=1)
    for k, (lon, lat) in enumerate(((131.2, 33.4), (133.4, 34.6), (135.2, 35.5))):
        R.act(lambda t, k=k: J.samurai(int(t * 7) + k, (14, 120), "enojo"), geo=(lon, lat), off=(0, 10), s=0.4, t_in=t_unif + 0.2 * k, d_in=0.4, entra="pop", sem=541 + k, sfx=[(0, "pop", 0.4)],
              t_out=t_corea - 0.2, sale="encoger", zs=0.6, z=1)
    lugar(R, t_yam, t_unif - 0.2, "YAMATO", (135.4, 34.8), off=(0, -170), px=62)
    R.snd(t_unif, "whoosh", 0.5, dur=0.8)
    # de Corea y China llegan la escritura, el budismo y el gobierno
    Pr = R.ruta(M.RUTA_COREA, t_corea - 0.1, 2.0, ancho=6.0, t1=t_gob + 0.4)
    R.act(A.rollo_escritura(1), pos_geo=R.camino_pos(M.RUTA_COREA, t_corea, 2.2, ease=lambda u: u), off=(0, -30), s=0.6, t_in=t_corea, d_in=0.4, entra="pop", sem=544, sfx=[(0, "papel", 0.5)],
          t_out=t_budi + 0.2, sale="encoger", zs=0.6, z=2)
    lugar(R, t_corea, t_escr, "COREA", (127.0, 37.5), off=(0, -80), px=52)
    R.act(J.templo(), geo=(135.8, 34.68), off=(0, 40), s=0.75, t_in=t_budi - 0.1, d_in=0.6, entra="pluma", sem=545, sfx=[(0, "crece", 0.5, {"dur": 0.6}), (0.4, "campana", 0.5)], t_out=t_604 - 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_escr, t_gob + 0.3, "ESCRITURA", (133.0, 34.5), off=(0, -120), px=50)
    lugar(R, t_budi, t_gob + 0.3, "BUDISMO", (135.8, 34.68), off=(0, -210), px=56)
    R.snd(t_china, "pluck", 0.5)
    # el príncipe Shotoku y su constitución
    R.act(J.emperador_jp(0, "feliz"), pos=(700, 790, 0.92), t_in=t_princ - 0.1, d_in=0.45, entra="pop", sem=546, sfx=[(0, "pop", 0.5)], t_out=t_nara - 0.4, sale="encoger", z=1)
    R.act(J.tablilla_ley(), pos=(1250, 760, 1.25), t_in=t_const - 0.1, d_in=0.5, entra="pop", sem=547, sfx=[(0, "pop", 0.5), (0.1, "escribir", 0.4)], t_out=t_nara - 0.4, sale="encoger", z=1)
    R.texto(t_sho - 0.1, t_nara - 0.4, "PRÍNCIPE SHOTOKU", (700, 450), px=64, d=0.9)
    R.contador(t_17 - 0.3, t_17 + 0.7, 0, 17, (1250, 450), px=96, formato="{} artículos")
    R.snd(t_17 - 0.2, "reloj_rapido", 0.45, dur=1.0)
    # la capital se traslada: Nara y luego Kioto
    Pn = [(135.8, 34.68), (135.78, 34.85), (135.77, 35.01)]
    R.act(Bb.palacio(), pos_geo=R.camino_pos(Pn, t_desp, 1.4), off=(0, 30), s=0.55, t_in=t_cap - 0.1, d_in=0.5, entra="pop", sem=548, sfx=[(0, "pop", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_nara - 0.1, t_desp, "NARA", (135.8, 34.68), off=(0, -130), px=64)
    lugar(R, t_kioto - 0.1, FIN(e) + 0.3, "KIOTO", (135.77, 35.01), off=(0, -130), px=72)
    R.snd(t_desp, "whoosh", 0.5, dur=0.6)
    R.snd(t_kioto, "gong", 0.6)


# ------------------------------------------------------------------ HEIAN
def _heian(R):
    e = "heian"
    i0 = INI(e)
    t_emp, t_edad, t_corte, t_poe, t_pint, t_nob = T(e, "empieza"), T(e, "edad"), T(e, "corte"), T(e, "poetas"), T(e, "pintores"), T(e, "nobles")
    t_mil, t_dama, t_mur, t_genji = T(e, "mil"), T(e, "dama"), T(e, "murasaki"), T(e, "genji")
    t_mucho, t_prim, t_nov = T(e, "muchos"), T(e, "primera"), T(e, "novela")
    t_pero, t_poem, t_prov, t_guer = T(e, "pero"), T(e, "poemas"), T(e, "provincias"), T(e, "guerreros")
    R.terreno(t_emp - 0.2, "heian", COL["heian"], 1.6)
    R.sello(t_edad + 0.1, "安", "Heian", color=(140, 90, 150))
    R.camara(i0 - 0.3, 135.8, 35.0, 5.6)
    R.camara(t_corte, 135.77, 35.05, 7.0)
    R.camara(t_mil - 0.2, 135.77, 35.05, 8.0)
    R.camara(t_mucho - 0.2, 135.77, 35.05, 8.6)
    R.camara(t_pero, 136.4, 35.2, 5.0)
    R.camara(t_guer - 0.2, 139.0, 36.0, 4.0)
    R.camara(FIN(e), 139.4, 35.8, 4.0)
    R.anio(i0, 794)
    R.anio(t_emp + 0.3, 794)
    R.anio(t_mil - 0.3, 794)
    R.anio(t_mil + 0.5, 1000)
    R.anio(t_pero - 0.2, 1000)
    R.anio(t_pero + 1.0, 1185)
    # la corte: emperador, poetas y nobles
    R.act(Bb.palacio(), geo=(135.77, 35.01), off=(0, 40), s=0.5, t_in=t_emp, d_in=0.5, entra="pluma", sem=550, sfx=[(0, "crece", 0.5, {"dur": 0.6})], t_out=t_mil - 0.2, sale="encoger", zs=0.6, z=0)
    R.act(J.emperador_jp(0, "feliz"), geo=(135.77, 35.01), off=(-240, 80), s=0.62, t_in=t_corte, d_in=0.45, entra="pop", sem=551, sfx=[(0, "pop", 0.5)], t_out=t_mil - 0.2, sale="encoger", zs=0.6, z=1)
    R.act(J.dama_heian(0), geo=(135.77, 35.01), off=(260, 80), s=0.62, t_in=t_nob, d_in=0.45, entra="pop", sem=552, sfx=[(0, "pop", 0.5)], t_out=t_mil - 0.2, sale="encoger", zs=0.6, z=1)
    R.act(Bb.poeta(0), geo=(135.77, 35.01), off=(20, 110), s=0.56, t_in=t_poe, d_in=0.45, entra="pop", sem=553, sfx=[(0, "pop", 0.5), (0.15, "pluck", 0.4)], t_out=t_mil - 0.2, sale="encoger", zs=0.6, z=1)
    R.act(P.libro(True), geo=(135.77, 35.01), off=(-60, -200), s=0.5, t_in=t_pint, d_in=0.45, entra="pop", sem=554, sfx=[(0, "papel", 0.5)], t_out=t_mil - 0.2, sale="encoger", zs=0.6, z=2)
    R.texto(t_edad - 0.1, t_mil - 0.3, "EDAD DE ORO DE LA CORTE", (960, 190), px=78, d=1.1)
    R.snd(t_edad, "escribir", 0.5, dur=1.0)
    # Murasaki Shikibu y el Genji
    R.act(J.dama_heian(1), pos=(700, 790, 1.0), t_in=t_dama - 0.1, d_in=0.45, entra="pop", sem=555, sfx=[(0, "pop", 0.6)], t_out=t_pero - 0.2, sale="encoger", z=1)
    R.act(P.libro(True), pos=lambda t: (1260, 760 + 6 * math.sin(t * 2), 1.5), t_in=t_genji - 0.2, d_in=0.5, entra="pop", sem=556, sfx=[(0, "pop", 0.6), (0.15, "brillo", 0.4)], t_out=t_pero - 0.2, sale="encoger", z=1)
    R.texto(t_mur - 0.1, t_pero - 0.3, "MURASAKI SHIKIBU", (700, 440), px=66, d=0.9)
    R.texto(t_genji - 0.1, t_pero - 0.3, "EL GENJI", (1260, 440), px=84, d=0.6)
    R.act(A.estrella5(44), pos=lambda t: (1340, 560 + 8 * math.sin(t * 3), 1.3), t_in=t_prim, d_in=0.4, entra="pop", sem=557, sfx=[(0, "bling", 0.6)], t_out=t_pero - 0.2, sale="encoger", z=2)
    R.texto(t_nov - 0.1, t_pero - 0.3, "¿PRIMERA NOVELA?", (960, 200), px=82, d=0.9)
    R.snd(t_nov, "escribir", 0.5, dur=0.8)
    # mientras tanto, en las provincias, crecen los guerreros
    Pg = [(135.77, 35.0), (137.5, 35.4), (139.4, 35.7)]
    R.ruta(Pg, t_prov - 0.1, 1.6, ancho=6.0, t1=FIN(e))
    for k, (dx, dy) in enumerate(((-130, 20), (0, 60), (130, 10))):
        R.act(lambda t, k=k: J.samurai(int(t * 6) + k, (40, 110), "enojo"), geo=(139.4, 35.7), off=(dx, dy), s=0.5, t_in=t_guer + 0.12 * k, d_in=0.4, entra="pop", sem=558 + k,
              sfx=[(0, "pop", 0.4), (0.05, "clink", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_prov, FIN(e), "PROVINCIAS", (139.4, 35.7), off=(0, -190), px=58)
    R.snd(t_guer, "tambor", 0.6)


# ------------------------------------------------------------------ SHOGUN
def _shogun(R):
    e = "shogun"
    i0 = INI(e)
    t_sam, t_clan, t_disp, t_poder = T(e, "samurais"), T(e, "clanes"), T(e, "disputan"), T(e, "poder")
    t_1192, t_mina, t_yori, t_vence, t_emp, t_tit, t_shog, t_gen, t_sup = T(e, "ciento"), T(e, "minamoto"), T(e, "yoritomo"), T(e, "vence"), T(e, "emperador", frase=1), T(e, "titulo"), T(e, "shogun", frase=1), T(e, "general"), T(e, "supremo")
    t_desde, t_manda, t_verd, t_reina, t_gobi = T(e, "desde"), T(e, "manda"), T(e, "verdad"), T(e, "reina"), T(e, "gobierna")
    t_y, t_cod, t_honor, t_leal, t_disc = T(e, "imponen"), T(e, "codigo"), T(e, "honor"), T(e, "lealtad"), T(e, "disciplina")
    R.camara(i0 - 0.3, 139.4, 35.8, 4.0)
    R.camara(t_clan - 0.2, 136.4, 35.4, 3.3)
    R.camara(t_poder, 136.0, 35.3, 3.4)
    R.camara(t_1192 - 0.3, 139.5, 35.3, 6.0)
    R.camara(t_desde - 0.3, 137.6, 35.3, 3.8)
    R.camara(t_cod - 0.3, 137.6, 35.3, 3.8)
    R.camara(FIN(e), 138.0, 35.5, 3.5)
    R.anio(i0, 1185)
    R.anio(t_1192 - 0.2, 1185)
    R.anio(t_1192 + 0.6, 1192)
    R.anio(t_cod - 0.2, 1192)
    R.anio(t_cod + 1.0, 1600)
    # clanes que se pelean por el poder (el territorio se fractura)
    colores = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146)]
    R.romper("clanes", t_clan - 0.2, t_clan + 0.6, t_poder + 0.6, t_poder + 1.3, colores=colores, gap=18, deriva=34)
    R.snd(t_clan - 0.2, "crujido", 0.8, dur=0.8)
    for k, (lon, lat) in enumerate(((131.0, 33.0), (133.5, 34.4), (135.5, 35.2), (138.5, 35.5), (140.5, 37.5), (140.6, 35.8))):
        R.act(lambda t, k=k: J.samurai(int(t * 8) + k, (40, 130), "enojo", (170, 60, 60) if k % 2 else (60, 100, 160)), geo=(lon, lat), off=lambda t, k=k: (8 * math.sin(t * 2 + k), 0), s=0.4,
              t_in=t_sam + 0.1 * k, d_in=0.35, entra="pop", sem=560 + k, sfx=[(0, "pop", 0.35)] + ([(0.1, "clink", 0.5)] if k % 2 == 0 else []),
              t_out=t_1192 - 0.3, sale="encoger", zs=0.6, z=1)
    R.texto(t_disp - 0.1, t_1192 - 0.4, "GUERRA DE CLANES", (960, 190), px=84, d=0.9)
    R.snd(t_disp, "escribir", 0.5, dur=0.8)
    R.snd(t_poder, "tambor", 0.7)
    # Yoritomo vence y recibe el título de shogun en Kamakura
    R.terreno(t_vence, "sin_hokkaido", COL["shogun"], 1.6)
    R.sello(t_shog + 0.2, "将", "Shogun", color=(52, 120, 124))
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "serio", (60, 100, 160)), geo=(139.55, 35.32), off=(0, 40), s=0.75, t_in=t_yori - 0.1, d_in=0.45, entra="pop", sem=570,
          sfx=[(0, "pop", 0.6), (0.1, "clink", 0.6)], t_out=t_desde - 0.2, sale="encoger", zs=0.5, z=1)
    R.act(J.emperador_jp(0), pos=(520, 800, 0.85), t_in=t_emp - 0.1, d_in=0.45, entra="pop", sem=571, sfx=[(0, "pop", 0.5)], t_out=t_desde - 0.2, sale="encoger", z=1)
    R.act(A.rollo_escritura(1), pos=lambda t: (lerp(640, 1260, e_inout(prog(t, t_tit, t_shog))), 730 - 60 * math.sin(math.pi * prog(t, t_tit, t_shog)), 1.0), t_in=t_tit - 0.1, d_in=0.3, entra="pop", sem=572,
          sfx=[(0, "papel", 0.5)], t_out=t_gen, sale="encoger", z=2)
    lugar(R, t_mina, t_vence, "MINAMOTO NO YORITOMO", (139.55, 35.32), off=(0, -210), px=56)
    lugar(R, t_1192, t_desde - 0.3, "KAMAKURA", (139.55, 35.32), off=(0, 120), px=58)
    R.texto(t_shog - 0.1, t_desde - 0.3, "SHOGUN = GENERAL SUPREMO", (960, 210), px=76, d=1.2)
    R.snd(t_shog, "gong", 0.6)
    R.snd(t_shog + 0.05, "escribir", 0.5, dur=1.0)
    # el shogun manda; el emperador reina pero no gobierna
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "serio", (60, 100, 160)), pos=(1380, 800, 1.0), t_in=t_manda - 0.2, d_in=0.45, entra="pop", sem=573, sfx=[(0, "pop", 0.6)], t_out=t_cod - 0.3, sale="encoger", z=1)
    R.act(A.cetro_corona(1.0), pos=(1560, 690, 0.9), t_in=t_manda, d_in=0.4, entra="pop", sem=574, sfx=[(0, "bling", 0.5)], t_out=t_cod - 0.3, sale="encoger", z=2)
    R.act(J.emperador_jp(0, "normal"), pos=(540, 800, 1.0), t_in=t_reina - 0.3, d_in=0.45, entra="pop", sem=575, sfx=[(0, "pop", 0.5)], t_out=t_cod - 0.3, sale="encoger", z=1)
    R.texto(t_manda - 0.1, t_cod - 0.4, "SHOGUN: MANDA", (1380, 470), px=64, d=0.7)
    R.texto(t_reina - 0.2, t_cod - 0.4, "EMPERADOR: REINA", (540, 470), px=64, d=0.7)
    R.act(A.signo_pregunta(), pos=lambda t: (540, 330 + 10 * math.sin(t * 4), 0.8), t_in=t_gobi, d_in=0.4, entra="pop", sem=576, sfx=[(0, "hmm", 0.5)], t_out=t_cod - 0.3, sale="encoger", z=2)
    # el código del samurái
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "serio"), pos=(960, 800, 1.1), t_in=t_cod - 0.1, d_in=0.45, entra="pop", sem=577, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", z=1)
    for k, (t0, txt, x) in enumerate(((t_honor, "HONOR", 420), (t_leal, "LEALTAD", 960), (t_disc, "DISCIPLINA", 1500))):
        R.texto(t0 - 0.1, FIN(e) + 0.2, txt, (x, 420), px=84, d=0.6)
        R.snd(t0, "escribir", 0.5, dur=0.6)
        R.act(A.estrella5(34), pos=lambda t, x=x, k=k: (x, 330 + 8 * math.sin(t * 4 + k), 1.0), t_in=t0, d_in=0.4, entra="pop", sem=578 + k, sfx=[(0, "bling", 0.5, {"tono": 1.0 + 0.25 * k})],
              t_out=FIN(e) + 0.3, sale="encoger", z=2)
