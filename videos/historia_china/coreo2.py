# -*- coding: utf-8 -*-
"""Coreografía (2/3): Qin, Han, Tang, Song, Yuan y Ming."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf, recortar, punto_en  # noqa: E402
from coreo1 import pop

COL = M.COL


def construir(R):
    _qin(R)
    _han(R)
    _tang(R)
    _song(R)
    _yuan(R)
    _ming(R)


def torres_en(R, P, t0, dur, s=0.34, cada=3, sem=60):
    """Torres que van brotando a lo largo de una muralla (P en lon/lat) mientras se construye."""
    n = len(P)
    for k in range(0, n, cada):
        u = k / max(1, n - 1)
        R.act(A.torre_muralla(), geo=tuple(P[k]), off=(0, 6), s=s, t_in=t0 + dur * e_inout(u) * 0.92, d_in=0.35, entra="pop", sem=sem + k,
              sfx=[(0, "bonk", 0.3, {"tono": 1.2})], zs=0.45)


# ------------------------------------------------------------------ QIN
def _qin(R):
    e = "qin"
    i0 = INI(e)
    t_conq, t_todos = T(e, "conquista"), T(e, "todos")
    t_antes, t_primer, t_empera = T(e, "antes", frase=1), T(e, "primer"), T(e, "emperador")
    t_unif, t_escr, t_mon, t_ejes, t_carros = T(e, "unifica"), T(e, "escritura"), T(e, "moneda"), T(e, "ejes"), T(e, "carros")
    t_une, t_murallas, t_norte, t_enterrar, t_barro = T(e, "une"), T(e, "murallas"), T(e, "norte"), T(e, "enterrar"), T(e, "barro")
    t_pero, t_apenas, t_cuatro = T(e, "pero"), T(e, "apenas"), T(e, "cuatro")
    t_parte = T("zhou", "parte")
    # los siete estados se reparten el mapa (desde Zhou) y Qin los conquista uno a uno
    orden = [0, 3, 1, 2, 4, 5, 6]
    qin_c = COL["qin"]
    pal = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60)]

    def colores(t, i):
        k = orden.index(i)
        ta = t_conq + 0.16 * k
        u = e_inout(prog(t, ta, ta + 0.45))
        if i == 0:
            u = 1.0 if t > t_parte + 1.0 else u
        return tuple(lerp(a, b, u) for a, b in zip(pal[i], qin_c))
    R.romper("estados", t_parte - 0.1, t_parte + 0.7, t_conq + 0.45, t_todos + 0.55, colores=colores, gap=12, deriva=24)
    R.snd(t_parte, "crujido", 0.9, dur=0.9)
    R.snd(t_conq, "cuerno", 0.5)
    for k in range(5):
        R.snd(t_conq + 0.2 + 0.2 * k, "impacto", 0.35, tono=0.9 + 0.05 * k)
    R.snd(t_todos + 0.4, "boing", 0.7)
    R.terreno(t_conq, "estados", COL["qin"], 0.4)
    R.terreno(t_antes + 0.1, "qin", COL["qin"], 1.4)
    # cámara
    R.camara(i0, 109.5, 34.6, 1.6)
    R.camara(t_antes, 108.5, 35.0, 1.85)
    R.camara(t_murallas - 0.3, 110.5, 38.5, 1.9)
    R.camara(t_enterrar - 0.2, 109.5, 36.5, 2.0)
    R.camara(t_pero, 108.5, 35.0, 1.55)
    R.camara(FIN(e), 108.0, 35.0, 1.45)
    # emperador
    R.sello(t_antes + 0.25, "秦", "Qin")
    R.anio(t_antes + 0.2, -221)
    R.anio(t_apenas, -210)
    R.anio(t_cuatro + 0.45, -206)
    tr = R.act(A.trono(), pos=(1560, 880, 1.05), t_in=t_primer, d_in=0.45, entra="pop", sem=70, sfx=[(0, "pop", 0.6)], z=-1, t_out=t_apenas + 0.2, sale="encoger")
    emp = R.act(persona(qin_c, PIEL, "mianguan", "serio", (20, 110), 0, traje="tunica", faja=ORO, cuello=ROJO_OSC, bigote=True), pos=(1560, 860, 1.05), t_in=t_primer + 0.05, d_in=0.45,
                entra="pop", sem=71, t_out=t_apenas + 0.15, sale="caer", d_out=0.9, z=1)
    R.act(A.estallido(14, 60, 170), pos=(1560, 640, 1.0), t_in=t_empera, d_in=0.35, entra="pop", sem=72, z=-2, t_out=t_empera + 0.9, sale="encoger", sfx=[(0, "brillo", 0.6)])
    R.texto(t_empera + 0.1, t_une - 0.2, "Qin Shi Huang", (1420, 560), px=62, d=0.8) if False else None
    # estandarización: escritura, moneda y ejes
    R.act(A.rollo_escritura(1), pos=(470, 700, 0.95), t_in=t_escr, d_in=0.45, entra="pop", sem=73, sfx=[(0, "papel", 0.7)], t_out=t_une - 0.1, sale="encoger")
    R.act(A.moneda(), pos=lambda t: (850, 690, 1.0, 5.0 * max(0.0, t - t_mon)), t_in=t_mon, d_in=0.45, entra="pop", sem=74, sfx=[(0, "clink", 0.8)], t_out=t_une - 0.1, sale="encoger")
    R.act(A.rueda(), pos=(1200, 720, 0.95), t_in=t_ejes, d_in=0.45, entra="pop", sem=75, sfx=[(0, "pop", 0.6), (0.15, "tick", 0.5)], t_out=t_une - 0.1, sale="encoger")
    # murallas del norte + ejército de barro
    P = M.suavizar = None
    from core import suavizar
    Pq = R.rio(M.MURALLA_QIN, t_murallas - 0.1, 1.9, (178, 168, 150), ancho=9)
    torres_en(R, Pq, t_murallas - 0.1, 1.9, 0.3, 9, 80)
    R.snd(t_murallas, "pincel", 0.55, dur=1.8)
    R.act(A.foso_guerreros(), pos=(820, 900, 1.25), t_in=t_enterrar, d_in=0.5, entra="pop", sem=76, sfx=[(0, "pop", 0.5)], z=-1, t_out=t_pero - 0.1, sale="encoger")
    for k in range(7):
        R.act(A.soldado_barro(k), pos=(440 + 122 * k, 905, 0.5), t_in=t_barro - 0.3 + 0.16 * k, d_in=0.35, entra="pop", sem=90 + k, sfx=[(0, "tick", 0.5, {"tono": 0.9 + 0.04 * k})],
              t_out=t_pero - 0.1, sale="encoger")
    # cuatro años
    R.act(A.arena_reloj(), pos=(900, 760, 1.0), t_in=t_apenas - 0.1, d_in=0.45, entra="pop", sem=77, sfx=[(0, "pop", 0.6), (0.1, "arena", 0.5, {"dur": 1.3})], t_out=FIN(e) + 0.3, sale="encoger")
    for k in range(4):
        R.snd(t_cuatro - 0.3 + 0.35 * k, "tick", 0.5, tono=0.8)


# ------------------------------------------------------------------ HAN
def _han(R):
    e = "han"
    i0 = INI(e)
    t_han, t_abre, t_mundo = T(e, "han"), T(e, "abre"), T(e, "mundo")
    t_ruta, t_seda, t_camellos, t_roma = T(e, "ruta"), T(e, "seda", frase=1), T(e, "camellos"), T(e, "roma")
    t_corr, t_rebel, t_rompe, t_reinos = T(e, "corrupcion"), T(e, "rebeliones"), T(e, "rompe"), T(e, "reinos")
    R.terreno(t_han - 0.1, "han", COL["han"], 1.5)
    R.sello(t_han + 0.05, "汉", "Han")
    R.anio(t_han, -206)
    R.anio(t_camellos + 0.3, -130)
    R.anio(t_corr, -130)
    R.anio(t_reinos + 0.5, 220)
    R.camara(i0, 106.0, 36.0, 1.4)
    R.camara(t_abre, 105.0, 37.0, 1.5)
    R.camara(t_ruta, 98.0, 38.5, 1.55)
    R.camara(t_camellos + 0.6, 84.0, 39.5, 1.6)
    R.camara(t_roma + 0.6, 82.0, 39.5, 1.5)
    R.camara(t_corr - 0.2, 106.0, 34.5, 1.65)
    R.camara(FIN(e), 108.0, 33.5, 1.6)
    # la puerta del mundo se abre
    R.act(lambda t: Bb.puerta(0.0) if False else A.puerta(e_inout(prog(t, t_abre, t_abre + 0.9))), pos=(1530, 800, 0.85), t_in=t_abre - 0.15, d_in=0.45, entra="pop", sem=100,
          sfx=[(0, "pop", 0.6), (0.2, "persianas", 0.5)], t_out=t_camellos + 0.6, sale="encoger")
    # la Ruta de la Seda
    P = R.ruta(M.RUTA_SEDA, t_ruta - 0.1, 2.6, ancho=6, dash=30, hueco=22)
    f0 = R.camino_pos(P, t_ruta + 0.05, 5.0, ease=lambda u: u)
    for k in range(3):
        R.act(lambda t, k=k: A.camello(int(t * 4) + k), pos_geo=R.camino_pos(P, t_ruta + 0.05 + 0.75 * k, 5.6 - 0.4 * k, ease=lambda u: u), off=lambda t: (0, 10 + 3 * math.sin(t * 6)),
              s=0.55, t_in=t_camellos - 0.35 + 0.3 * k, d_in=0.4, entra="pop", flip=True, sem=101 + k, sfx=[(0, "pop", 0.5)], t_out=t_roma + 1.4, sale="encoger", zs=0.5)
    R.snd(t_camellos, "pasos", 0.45, dur=2.4)
    R.act(A.rollo_seda(), pos=(540, 760, 1.0), t_in=t_seda, d_in=0.45, entra="pop", sem=104, sfx=[(0, "papel", 0.7)], t_out=t_roma + 1.6, sale="encoger", z=1)
    R.texto(t_roma, t_roma + 1.8, "a Roma", (470, 560), px=82, d=0.6)
    R.snd(t_roma, "escribir", 0.5, dur=0.6)
    # corrupción, rebeliones y tres reinos
    R.act(persona(AZUL_IMP, PIEL, "funcionario", "guiño", (30, 120), 0, traje="tunica", faja=ORO, acc_d="saco"), pos=(520, 830, 1.0), t_in=t_corr, d_in=0.45, entra="pop", sem=105, sfx=[(0, "pop", 0.6), (0.2, "monedas", 0.6)],
          t_out=t_rompe + 0.3, sale="encoger")
    R.act(A.bolsa_dinero(), pos=(780, 850, 0.8), t_in=t_corr + 0.25, d_in=0.4, entra="cae", dy=500, sem=106, sfx=[(0.3, "clink", 0.6)], t_out=t_rompe + 0.3, sale="encoger")
    R.act(A.multitud(9, 2), pos=(1250, 850, 1.25), t_in=t_rebel, d_in=0.4, entra="pop", sem=107, sfx=[(0, "pop", 0.6), (0.1, "rugido", 0.4)], t_out=t_rompe + 0.3, sale="encoger")
    for k in range(3):
        R.act(A.horquilla(), pos=(1130 + 120 * k, 850, 0.7, 0.12 * (k - 1)), t_in=t_rebel + 0.12 * k, d_in=0.3, entra="pop", sem=108 + k, t_out=t_rompe + 0.3, sale="encoger", z=2)
    R.terreno(t_rompe - 0.1, "tres", COL["tres"], 1.0)
    t_unir = T("tang", "unirse")
    R.romper("tres", t_rompe - 0.05, t_rompe + 0.6, t_unir - 0.25, t_unir + 0.7, colores=[(96, 134, 184), (104, 168, 136), (214, 90, 76)], gap=14, deriva=40)
    R.snd(t_rompe, "crujido", 0.9, dur=0.9)
    R.snd(t_reinos, "gong", 0.5)


# ------------------------------------------------------------------ TANG
def _tang(R):
    e = "tang"
    i0 = INI(e)
    t_casi, t_cuatro, t_unirse = T(e, "casi"), T(e, "cuatrocientos"), T(e, "unirse")
    t_tang, t_edad, t_poetas, t_baila, t_millon = T(e, "tang"), T(e, "edad"), T(e, "poetas"), T(e, "bailarinas"), T(e, "millon")
    t_alq, t_vida, t_inv, t_pol = T(e, "alquimistas"), T(e, "eterna"), T(e, "inventan"), T(e, "polvora")
    R.terreno(t_unirse - 0.35, "tang", COL["tang"], 1.5)
    R.sello(t_tang, "唐", "Tang")
    R.anio(t_casi, 220)
    R.anio(t_cuatro + 0.2, 220)
    R.anio(t_unirse, 618)
    R.camara(i0, 108.0, 33.5, 1.6)
    R.camara(t_unirse, 109.5, 34.5, 1.5)
    R.camara(t_edad, 109.0, 35.0, 2.5)
    R.camara(t_alq, 110.0, 35.2, 2.3)
    R.camara(FIN(e), 110.0, 35.0, 2.2)
    R.snd(t_cuatro, "reloj_rapido", 0.5, dur=1.5)
    R.snd(t_unirse, "boing", 0.7)
    # edad de oro: pagoda, poeta, bailarina y una ciudad enorme
    R.act(A.pagoda(5), geo=(108.9, 34.3), off=(-60, 10), s=0.8, t_in=t_edad, d_in=1.1, entra="pluma", sem=110, sfx=[(0, "crece", 0.6, {"dur": 0.8}), (1.0, "campana", 0.6)], t_out=t_alq - 0.15, sale="encoger")
    R.act(Bb.poeta(0), pos=(1560, 830, 1.0), t_in=t_poetas, d_in=0.45, entra="pop", sem=111, sfx=[(0, "pop", 0.6), (0.1, "pluck", 0.6)], t_out=t_alq - 0.15, sale="encoger", z=1)
    R.act(lambda t: Bb.bailarina(int(t * 4) % 3), pos=(1180, 840, 1.0), t_in=t_baila, d_in=0.45, entra="pop", sem=112, sfx=[(0, "pop", 0.6), (0.1, "pluck", 0.6, {"tono": 1.26})], t_out=t_alq - 0.15,
          sale="encoger", z=1)
    for k in range(6):
        R.act(A.multitud(8, 10 + k), pos=(300 + 190 * k, 800 + 12 * (k % 2), 0.8), t_in=t_millon - 0.6 + 0.12 * k, d_in=0.3, entra="pop", sem=120 + k, t_out=t_alq - 0.15, sale="encoger",
              sfx=[(0, "tick", 0.3, {"tono": 1 + 0.05 * k})])
    R.contador(t_millon - 0.4, t_millon + 0.9, 0, 1000000, (560, 330), px=110)
    R.snd(t_millon, "escribir", 0.4, dur=0.8)
    # alquimistas: vida eterna... y pólvora
    R.act(lambda t: Bb.frasco_burbujas(int(t * 5)), pos=(1050, 820, 1.25), t_in=t_alq, d_in=0.45, entra="pop", sem=113, sfx=[(0, "pop", 0.6), (0.1, "burbujas", 0.6, {"dur": 1.0})], t_out=t_pol, sale="cortar", z=1)
    R.act(Bb.alquimista(0), pos=(1560, 840, 1.0), t_in=t_alq + 0.1, d_in=0.45, entra="pop", sem=114, sfx=[(0, "pop", 0.6)], t_out=t_pol, sale="cortar", z=1)
    R.act(Bb.alquimista(1), pos=(1590, 830, 1.0, 0.0), t_in=t_pol, d_in=0.01, entra="fija", sem=115, t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.texto(t_vida - 0.3, t_pol - 0.1, "¿vida eterna?", (900, 300), px=86, d=0.7)
    R.act(A.estallido(14, 80, 240), pos=(1050, 700, 1.6), t_in=t_pol, d_in=0.3, entra="pop", sem=116, z=3, t_out=t_pol + 0.8, sale="encoger", sfx=[(0, "explosion", 1.0)])
    R.act(Bb.chispas(16, 260), pos=(1050, 700, 1.5), t_in=t_pol + 0.05, d_in=0.5, entra="pop", sem=117, z=2, t_out=FIN(e) + 0.4, sale="encoger")
    R.act(lambda t: Bb.cohete(), pos=lambda t: (1330, 880 - 620 * e_in(prog(t, t_pol + 0.5, t_pol + 1.6)), 0.8), t_in=t_pol + 0.4, d_in=0.2, entra="fija", sem=118, z=2, t_out=t_pol + 1.6, sale="cortar",
          sfx=[(0.1, "whoosh", 0.5, {"dur": 1.0})])
    R.act(Bb.chispas(18, 300), pos=(1330, 260, 1.3), t_in=t_pol + 1.6, d_in=0.4, entra="pop", sem=119, z=2, t_out=FIN(e) + 0.4, sale="encoger", sfx=[(0, "explosion", 0.8, {"tono": 1.3})])


# ------------------------------------------------------------------ SONG
def _song(R):
    e = "song"
    i0 = INI(e)
    t_song, t_avanz, t_planeta = T(e, "song"), T(e, "avanzada"), T(e, "planeta")
    t_inv, t_papelm, t_imp, t_bruj, t_nav = T(e, "inventa"), T(e, "moneda"), T(e, "imprenta"), T(e, "brujula"), T(e, "navega")
    R.terreno(t_song - 0.1, "song", COL["song"], 1.5)
    R.sello(t_song + 0.05, "宋", "Song")
    R.anio(t_song, 960)
    R.anio(t_imp, 1040)
    R.camara(i0, 110.0, 33.0, 1.6)
    R.camara(t_inv, 114.0, 32.0, 1.75)
    R.camara(t_nav, 118.0, 29.0, 1.95)
    R.camara(FIN(e), 119.5, 28.5, 2.0)
    R.act(A.pagoda(4), geo=(114.3, 34.8), off=(0, -6), s=0.7, t_in=t_avanz - 0.3, d_in=0.9, entra="pluma", sem=130, sfx=[(0, "crece", 0.5, {"dur": 0.7})], t_out=t_inv - 0.1, sale="encoger")
    for k, (x, y) in enumerate(((1100, 400), (1330, 330), (1560, 420))):
        R.act(A.estrella5(46), pos=(x, y, 1.0, 0.3 * (k - 1)), t_in=t_avanz + 0.1 * k, d_in=0.35, entra="pop", sem=131 + k, sfx=[(0, "bling", 0.5)], t_out=t_inv - 0.1, sale="encoger")
    R.texto(t_avanz, t_inv - 0.1, "la más avanzada", (1330, 520), px=70, d=0.8)
    # papel moneda, imprenta, brújula
    R.act(Bb.billete(), pos=(470, 720, 1.0), t_in=t_papelm - 0.2, d_in=0.45, entra="pop", sem=134, sfx=[(0, "papel", 0.7)], t_out=FIN(e) + 0.3, sale="encoger")
    R.act(A.papel_hoja(), pos=(900, 790, 0.85), t_in=t_imp - 0.35, d_in=0.45, entra="pop", sem=135, sfx=[(0, "papel", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", z=0)
    R.act(Bb.tipo_movil(), pos=lambda t: (900 + 10 * math.sin(t * 7), 560 + 110 * abs(math.sin((t - t_imp) * 4.0)) if t > t_imp - 0.2 else 560, 1.1), t_in=t_imp - 0.2, d_in=0.3, entra="pop", sem=136,
          t_out=FIN(e) + 0.3, sale="encoger", z=1)
    for k in range(4):
        R.snd(t_imp + 0.18 + 0.52 * k, "bonk", 0.5, tono=1.0 + 0.08 * k)
    R.act(lambda t: Bb.brujula(0.9 * math.sin((t - t_bruj) * 5.0) * math.exp(-(t - t_bruj) * 0.9)), pos=(1400, 700, 1.05), t_in=t_bruj - 0.1, d_in=0.45, entra="pop", sem=137,
          sfx=[(0, "pop", 0.6), (0.2, "ding", 0.6)], t_out=FIN(e) + 0.3, sale="encoger")
    R.act(Bb.junco(1.0, 3), pos_geo=R.camino_pos([(121.3, 30.6), (122.6, 29.0), (121.9, 26.6), (120.0, 24.8)], t_nav, 3.4), off=lambda t: (0, 8 * math.sin(t * 4)), s=0.46, t_in=t_nav - 0.2, d_in=0.4,
          entra="pop", sem=138, sfx=[(0, "chapuzon", 0.4)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.5)


# ------------------------------------------------------------------ YUAN
def _yuan(R):
    e = "yuan"
    i0 = INI(e)
    t_norte, t_torm, t_jin, t_mong = T(e, "norte"), T(e, "tormenta"), T(e, "jinetes"), T(e, "mongoles")
    t_nieto, t_gengis, t_conq, t_yuan = T(e, "nieto"), T(e, "gengis"), T(e, "conquista"), T(e, "yuan")
    R.terreno(t_jin - 0.3, "yuan", COL["yuan"], 3.0)
    R.sello(t_yuan - 0.05, "元", "Yuan")
    R.anio(t_norte, 1206)
    R.anio(t_nieto, 1206)
    R.anio(t_conq + 0.3, 1279)
    R.camara(i0, 106.0, 41.0, 1.3)
    R.camara(t_jin, 105.0, 44.0, 1.35)
    R.camara(t_nieto, 104.0, 40.0, 1.2)
    R.camara(FIN(e), 104.0, 38.0, 1.15)
    R.act(Bb.tormenta(), pos=(960, 230, 1.6), t_in=t_torm - 0.3, d_in=0.5, entra="pop", sem=140, sfx=[(0, "trueno", 0.8)], t_out=t_nieto - 0.2, sale="sube_fuera", d_out=0.6, z=2)
    R.snd(t_jin - 0.2, "galope", 0.7, dur=3.0)
    R.snd(t_jin - 0.3, "tambor", 0.6)
    for k in range(6):
        ini = (92 + 7 * k, 53.5 - 1.5 * (k % 2))
        fin_ = (102 + 5 * k, 37 - 1.2 * (k % 3))
        R.act(lambda t, k=k: Bb.jinete(int(t * 6) + k, ROJO_OSC, "gorro", True, False, "enojo"), pos_geo=R.camino_pos([ini, ((ini[0] + fin_[0]) / 2 + 3, (ini[1] + fin_[1]) / 2), fin_], t_jin - 0.2 + 0.18 * k, 3.4, ease=e_inout),
              off=lambda t, k=k: (0, 4 * math.sin(t * 12 + k)), s=0.42, t_in=t_jin - 0.3 + 0.12 * k, d_in=0.3, entra="pop", sem=141 + k, flip=False, t_out=t_nieto - 0.3, sale="encoger", zs=0.5, z=1)
    # el nieto de Gengis Kan
    R.act(persona(ROJO_OSC, PIEL_OSC, "gorro", "serio", (30, 60), 0, traje="tunica", barba=(200, 200, 204), bigote=True, cuello=ORO), pos=(560, 830, 1.05), t_in=t_gengis - 0.1, d_in=0.45, entra="pop", sem=150,
          sfx=[(0, "pop", 0.6), (0.1, "cuerno", 0.4)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.act(C.tribuna() if False else Bb.arbol_familia(), pos=(930, 640, 1.0), t_in=t_nieto, d_in=0.7, entra="pluma", sem=151, peg=False, t_out=FIN(e) + 0.4, sale="cortar", z=0)
    R.act(persona(AZUL_OSC, PIEL, "gorro", "feliz", (30, 130), 1, traje="tunica", cuello=ORO, faja=ORO), pos=(1300, 830, 1.05), t_in=t_nieto + 0.25, d_in=0.45, entra="pop", sem=152,
          sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.texto(t_gengis, FIN(e) + 0.2, "Gengis Kan", (560, 420), px=62, d=0.7)
    R.texto(t_nieto + 0.3, FIN(e) + 0.2, "su nieto", (1300, 420), px=62, d=0.7)


# ------------------------------------------------------------------ MING
def _ming(R):
    e = "ming"
    i0 = INI(e)
    t_camp, t_huer, t_expulsa, t_ming = T(e, "campesino"), T(e, "huerfano"), T(e, "expulsa"), T(e, "ming")
    t_lev, t_ciudad, t_muralla, t_ladr = T(e, "levantan"), T(e, "ciudad"), T(e, "muralla"), T(e, "ladrillo")
    t_almi, t_zarpa, t_barcos, t_colon = T(e, "almirante"), T(e, "zarpa"), T(e, "barcos"), T(e, "colon")
    t_pronto, t_espalda, t_mar = T(e, "pronto"), T(e, "espalda"), T(e, "mar")
    R.terreno(t_expulsa, "ming", COL["ming"], 1.6)
    R.sello(t_ming, "明", "Ming")
    R.anio(t_camp, 1368)
    R.anio(t_zarpa, 1405)
    R.anio(t_colon + 0.4, 1492)
    R.anio(t_pronto, 1433)
    R.camara(i0, 108.0, 37.0, 1.35)
    R.camara(t_expulsa, 108.0, 34.5, 1.5)
    R.camara(t_lev, 115.0, 40.0, 2.3)
    R.camara(t_muralla + 0.5, 112.0, 39.5, 2.0)
    R.camara(t_almi + 0.5, 118.0, 30.0, 1.7)
    R.camara(t_zarpa + 2.0, 112.0, 20.0, 1.45)
    R.camara(t_colon, 106.0, 14.0, 1.3)
    R.camara(t_pronto, 112.0, 26.0, 1.5)
    R.camara(FIN(e), 112.0, 30.0, 1.4)
    # campesino huérfano -> emperador (transformación)
    R.morf(Bb.huerfano(0), Bb.emperador(0), t_expulsa - 0.05, 0.6, (820, 830, 1.05), sem=161, salida=t_ciudad + 0.3, t_a=t_camp - 0.1)
    for k in range(4):
        ini = (104 + 3 * k, 38.5 - 0.8 * k)
        R.act(lambda t, k=k: Bb.jinete(int(t * 6) + k, ROJO_OSC, "gorro", True), pos_geo=R.camino_pos([ini, (104 + 3 * k, 46 + k), (108 + 3 * k, 54)], t_expulsa, 2.4, ease=e_in), s=0.42, flip=True, t_in=t_expulsa - 0.1,
              d_in=0.2, entra="fija", sem=165 + k, off=(0, 0), t_out=t_expulsa + 2.5, sale="cortar", zs=0.5)
    R.snd(t_expulsa, "galope", 0.6, dur=2.0)
    # Ciudad Prohibida y Gran Muralla
    R.act(Bb.palacio(), geo=(116.4, 39.9), off=(0, 30), s=0.85, t_in=t_ciudad - 0.4, d_in=0.5, entra="pop", sem=170, sfx=[(0, "pop", 0.7), (0.15, "gong", 0.5)], t_out=t_almi - 0.2, sale="encoger", zs=0.5)
    Pm = R.rio(M.MURALLA_MING, t_muralla - 0.3, 1.5, (188, 120, 100), ancho=10)
    torres_en(R, Pm, t_muralla - 0.3, 1.5, 0.26, 9, 180)
    R.snd(t_muralla, "pincel", 0.55, dur=1.7)
    # flota del tesoro
    Pz = R.ruta(M.RUTA_ZHENG, t_zarpa - 0.1, 3.6, ancho=6, dash=28, hueco=22, t1=t_pronto - 0.3)
    R.act(Bb.nave_tesoro(), geo=(118.8, 32.0), off=(0, 10), s=0.4, t_in=t_almi - 0.1, d_in=0.45, entra="pop", sem=171, sfx=[(0, "pop", 0.6)], t_out=t_zarpa + 0.05, sale="cortar", zs=0.5)
    for k in range(7):
        R.act(lambda t, k=k: Bb.junco(1.0, 3 if k % 2 == 0 else 2), pos_geo=R.camino_pos(Pz, t_zarpa + 0.18 * k, 4.2 - 0.05 * k, ease=lambda u: u), off=lambda t, k=k: (0, 6 * math.sin(t * 3 + k)),
              s=0.30 if k else 0.4, t_in=t_zarpa + 0.18 * k - 0.05, d_in=0.3, entra="pop", sem=172 + k, sfx=[(0, "chapuzon", 0.3)] if k % 3 == 0 else [], t_out=t_pronto - 0.4, sale="encoger", zs=0.5, z=1)
    R.snd(t_zarpa, "campana", 0.6)
    R.snd(t_zarpa + 0.2, "viento", 0.45, dur=2.6)
    # comparación con Colón
    R.act(Bb.nave_tesoro(), pos=(640, 760, 0.6), t_in=t_barcos, d_in=0.5, entra="pop", sem=180, sfx=[(0, "pop", 0.6)], t_out=t_pronto - 0.4, sale="encoger", z=2)
    R.act(Bb.carabela(), pos=(1380, 830, 0.42), t_in=t_colon - 0.1, d_in=0.45, entra="pop", sem=181, sfx=[(0, "pop", 0.6), (0.1, "bocinazo", 0.3)], t_out=t_pronto - 0.4, sale="encoger", z=2)
    R.texto(t_barcos + 0.1, t_pronto - 0.5, "1405", (640, 560), px=84, d=0.6)
    R.texto(t_colon, t_pronto - 0.5, "Colón 1492", (1380, 690), px=64, d=0.7)
    # China le da la espalda al mar
    R.act(lambda t: Bb.gran_puerta_cerrada(e_inout(prog(t, t_espalda, t_espalda + 0.9))), pos=(1450, 820, 0.85), t_in=t_pronto, d_in=0.5, entra="pop", sem=185,
          sfx=[(0, "pop", 0.6), (0.9, "impacto", 0.9)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.texto(t_espalda + 0.6, FIN(e) + 0.2, "CERRADO", (1450, 480), px=90, d=0.6)
    R.snd(t_espalda, "persianas", 0.5)
