# -*- coding: utf-8 -*-
"""Coreografía (1/3): gancho, río amarillo (Shang) y Zhou."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402  (después del * para que T sea el tiempo, no el trazo)

COL = M.COL


def pop(R, dib, t, pos=None, geo=None, off=(0, 0), s=1.0, snd="pop", vol=0.6, **k):
    sfx = [(0.0, snd, vol)] if snd else []
    if pos is not None:
        return R.act(dib, pos=pos, t_in=t, sfx=sfx, **k)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t, sfx=sfx, **k)


def construir(R):
    _gancho(R)
    _rio(R)
    _zhou(R)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    t_imperio, t_rompio, t_otra = T(e, "imperio"), T(e, "rompio"), T(e, "otra")
    t_volvio, t_unirse = T(e, "volvio"), T(e, "unirse")
    t_historia, t_china, t_tres, t_min = T(e, "historia"), T(e, "china"), T(e, "tres"), T(e, "minutos")
    # cámara: toda China, deriva lenta y luego vuelo al río
    R.camara(0.0, 103.5, 36.0, 1.12)
    R.camara(t_rompio, 103.5, 36.0, 1.2)
    R.camara(t_unirse, 104.0, 36.5, 1.3)
    R.camara(t_min + 0.4, 105.0, 36.0, 1.25)
    # el imperio aparece (pincelada que crece) y se rompe dos veces
    R.terreno(t_imperio - 0.1, "prc", COL["prc"], 1.2)
    R.romper("caudillos", t_rompio - 0.05, t_rompio + 0.45, t_rompio + 0.72, t_rompio + 1.15, colores=None, gap=12, deriva=34)
    R.romper("caudillos", t_otra - 0.12, t_otra + 0.45, t_volvio - 0.05, t_unirse + 0.4, colores=None, gap=14, deriva=52, nervio=1.6)
    R.snd(t_imperio, "brillo", 0.5)
    R.snd(t_rompio - 0.05, "crujido", 0.9, dur=0.7)
    R.snd(t_rompio + 0.72, "boing", 0.6, tono=1.1)
    R.snd(t_otra - 0.12, "crujido", 0.95, dur=0.9)
    R.snd(t_otra + 0.1, "impacto", 0.5)
    R.snd(t_volvio - 0.05, "whoosh", 0.5, dur=0.8, tono=1.2)
    R.snd(t_unirse + 0.22, "boing", 0.8)
    R.snd(t_unirse + 0.3, "ding", 0.6)
    # título y cronómetro
    R.texto(t_historia - 0.05, FIN(e) + 1.0, "LA HISTORIA DE CHINA", (960, 150), px=118, d=0.9)
    R.texto(t_tres - 0.05, FIN(e) + 1.0, "en 3 minutos", (960, 262), px=84, d=0.6)
    R.snd(t_historia, "escribir", 0.6, dur=0.9)
    R.snd(t_tres, "escribir", 0.5, dur=0.6)
    pop(R, lambda t: C.cronometro((t - t_tres) * 2.0 * math.pi / max(0.6, FIN(e) - t_tres + 0.6)), t_tres + 0.15, pos=(1660, 520, 1.15), t_out=FIN(e) + 0.6, sale="encoger",
        d_in=0.5, snd="pop", vol=0.7, sem=2)
    R.snd(t_tres + 0.3, "reloj_rapido", 0.45, dur=1.6)


# ------------------------------------------------------------------ RÍO AMARILLO / SHANG
def _rio(R):
    e = "rio"
    i0 = INI(e)
    t_empieza, t_rio, t_amar, t_hace, t_cuatro = T(e, "empieza"), T(e, "rio"), T(e, "amarillo"), T(e, "hace"), T(e, "cuatro")
    t_aldeas, t_agri, t_mijo, t_arroz = T(e, "aldeas"), T(e, "agricultores"), T(e, "mijo"), T(e, "arroz")
    t_nacen, t_reyes, t_shang = T(e, "nacen"), T(e, "reyes"), T(e, "shang")
    t_adiv, t_grab, t_huesos, t_fuego, t_escr, t_antig = T(e, "adivinos"), T(e, "graban"), T(e, "huesos"), T(e, "fuego"), T(e, "escritura"), T(e, "antigua")
    # el imperio moderno se desvanece y la cámara vuela al río
    R.terreno(i0 - 0.6, None, COL["prc"], 1.0)
    R.camara(i0 - 0.5, 105.0, 36.0, 1.25)
    R.camara(t_rio + 0.3, 111.0, 35.8, 2.5)
    R.camara(t_nacen, 111.5, 35.2, 2.4)
    R.camara(t_adiv, 112.0, 34.8, 2.25)
    R.camara(FIN(e), 112.0, 34.6, 2.1)
    R.snd(i0 - 0.5, "zoom_whoosh", 0.6, dur=1.0)
    # contador de años: de hoy a hace cuatro mil años, y luego Shang
    R.anio(t_hace - 0.4, 2026)
    R.anio(t_hace, 2026)
    R.anio(t_cuatro + 0.35, -2000)
    R.anio(t_nacen, -2000)
    R.anio(t_shang + 0.2, -1600)
    R.snd(t_hace, "reloj_rapido", 0.5, dur=1.4)
    # el río amarillo se pinta
    R.rio(M.RIO_AMARILLO, t_rio - 0.25, 1.9, (214, 172, 72), ancho=21)
    R.snd(t_rio - 0.2, "pincel", 0.6, dur=1.8)
    # amanecer sobre el río: sol, barca y pájaros (la escena nunca está vacía)
    R.act(A.sol_brillo(58), pos=(1580, 250, 1.0), t_in=t_empieza - 0.1, d_in=0.6, entra="pop", sem=1, sfx=[(0, "brillo", 0.5)], z=-1, t_out=t_aldeas - 0.1, sale="sube_fuera", d_out=0.6)
    P_rio = R.camino_pos(M.RIO_AMARILLO, t_rio + 0.8, 3.6, ease=lambda u: u)
    R.act(Bb.junco(1.0, 1), pos_geo=P_rio, off=lambda t: (0, -8 + 5 * math.sin(t * 4)), s=0.3, t_in=t_rio + 0.8, d_in=0.4, entra="pop", sem=2, sfx=[(0, "chapuzon", 0.4)], t_out=t_nacen, sale="encoger", zs=0.5, z=1)
    for k in range(3):
        R.act(lambda t, k=k: Bb.pajaro(int(t * 5) + k), pos=lambda t, k=k: (1850 - 220 * (t - t_hace) + 70 * k, 300 + 55 * k + 18 * math.sin(t * 3 + k), 0.6), t_in=t_hace + 0.15 * k, d_in=0.3, entra="pop", sem=3 + k,
              t_out=t_aldeas - 0.2, sale="encoger", peg=False, z=2)
    # aldeas y cultivos
    pop(R, A.casa(), t_aldeas, geo=(112.4, 35.0), off=(-40, -40), s=0.9, sem=3)
    pop(R, A.casa(), t_aldeas + 0.28, geo=(109.6, 35.6), off=(-10, 10), s=0.75, sem=4)
    pop(R, A.casa(), t_aldeas + 0.5, geo=(114.4, 35.4), off=(0, -20), s=0.8, sem=5)
    pop(R, persona(VERDE_OSC, PIEL, "paja", "feliz", (25, 80), 0, traje="corta", acc_d="azada"), t_agri, geo=(111.0, 34.3), off=(0, 110), s=0.72, sem=6)
    pop(R, persona(ROJO_OSC, PIEL, "moño", "feliz", (30, 60), 1, traje="corta", acc_d="mijo"), t_agri + 0.25, geo=(113.4, 34.0), off=(0, 120), s=0.68, sem=7)
    for k in range(3):
        pop(R, A.mijo_planta(), t_mijo + 0.12 * k, geo=(110.2 + 1.5 * k, 37.4), off=(0, 80), s=0.75, sem=8 + k, snd="pop" if k == 0 else None)
    pop(R, A.arrozal(), t_arroz, geo=(113.2, 31.6), off=(0, 80), s=1.0, sem=12, entra="lt")
    pop(R, A.arrozal(), t_arroz + 0.3, geo=(115.6, 30.6), off=(0, 70), s=0.8, sem=13, entra="lt")
    # salida de lo anterior: todo se encoge al hablar de los reyes
    for a in R.actores:
        if a.t_in >= t_aldeas - 0.01 and a.t_out is None and a.t_in < t_nacen:
            a.t_out, a.d_out, a.sale = t_nacen + 0.05, 0.35, "encoger"
    # los primeros reyes: nace Shang
    R.terreno(t_nacen, "shang", COL["shang"], 1.4)
    R.sello(t_shang - 0.1, "商", "Shang")
    trono = pop(R, A.trono(), t_reyes, pos=(1330, 800, 1.05), z=-1, sem=14, snd=None, t_out=t_adiv - 0.15, sale="encoger")
    rey = pop(R, persona(ROJO_CH, PIEL, "corona", "feliz", (25, 120), 0, traje="tunica", faja=ORO, cuello=ORO_OSC, bigote=True), t_reyes + 0.05, pos=(1330, 780, 1.0),
              sem=15, vida=1.0, t_out=t_adiv - 0.15, sale="encoger")
    ding = pop(R, A.ding(), t_shang + 0.05, pos=(1640, 820, 0.9), sem=16, t_out=t_adiv - 0.1, sale="encoger")
    R.snd(t_shang + 0.05, "gong", 0.45, tono=1.1)
    # huesos oraculares
    hue = R.act(A.hueso(), pos=(520, 520, 1.45), t_in=t_adiv, d_in=0.5, entra="pop", sem=17, sfx=[(0, "pop", 0.7)], t_out=FIN(e) + 0.4, sale="encoger")
    R.act(A.hueso(), pos=(520, 520, 1.45), t_in=t_adiv, d_in=0.01, entra="fija", sem=17, peg=False, z=1, t_out=t_adiv + 0.01, sale="cortar")
    for f in range(3):
        R.act(lambda t, f=f: A.llama(int(t * 9) + f), pos=(470 + 55 * f, 960, 0.75 + 0.1 * (f % 2)), t_in=t_fuego + 0.08 * f, d_in=0.3, entra="pop", sem=18 + f, z=2,
              sfx=[(0, "siseo", 0.5, {"dur": 1.4})] if f == 0 else [], t_out=FIN(e) + 0.4, sale="encoger")
    R.act(A.grietas_hueso(), pos=(520, 520, 1.45), t_in=t_fuego + 0.45, d_in=0.8, entra="pluma", sem=22, z=3, peg=False, t_out=FIN(e) + 0.4, sale="cortar")
    R.snd(t_grab, "garabato", 0.6, dur=1.3)
    R.snd(t_fuego + 0.5, "crujido", 0.8, dur=0.6)
    R.texto(t_escr, FIN(e) + 0.2, "la escritura más antigua", (900, 260), px=66, d=0.9)
    R.snd(t_escr, "escribir", 0.5, dur=0.9)


# ------------------------------------------------------------------ ZHOU
def _zhou(R):
    e = "zhou"
    t_zhou, t_idea, t_mand, t_cielo = T(e, "zhou"), T(e, "idea"), T(e, "mandato"), T(e, "cielo")
    t_rey, t_apru, t_mal, t_cae = T(e, "rey", frase=1), T(e, "apruebe"), T(e, "mal"), T(e, "cae", frase=1)
    t_cae2, t_parte, t_siete, t_pelean, t_siglos = T(e, "cae", frase=2), T(e, "parte"), T(e, "siete"), T(e, "pelean"), T(e, "siglos")
    i0 = INI(e)
    R.terreno(t_zhou - 0.1, "zhou", COL["zhou"], 1.5)
    R.sello(t_zhou + 0.05, "周", "Zhou")
    R.camara(i0, 111.5, 34.6, 2.1)
    R.camara(t_mand, 111.0, 34.5, 1.95)
    R.camara(t_parte, 110.5, 34.5, 1.75)
    R.camara(t_siglos, 110.0, 33.8, 1.65)
    R.camara(FIN(e), 109.5, 34.6, 1.6)
    R.anio(t_zhou, -1046)
    R.anio(t_siete, -475)
    R.anio(t_siglos + 0.4, -221)
    R.snd(t_zhou + 0.2, "whoosh", 0.4, dur=0.7)
    # Mandato del Cielo: nube con sol, rollo que baja
    nube = pop(R, A.nube_cielo(), t_mand - 0.1, pos=(1290, 300, 1.05), sem=30, t_out=t_parte - 0.2, sale="sube_fuera", d_out=0.6)
    sol = pop(R, A.sol_brillo(44), t_cielo - 0.1, pos=(1290, 240, 0.9), sem=31, snd="brillo", t_out=t_parte - 0.2, sale="sube_fuera", d_out=0.6, z=-1)
    R.act(A.rollo_escritura(3), pos=(1290, 560, 0.85), t_in=t_cielo + 0.1, d_in=0.7, entra="baja_entra", dy=500, sem=32, sfx=[(0.5, "papel", 0.7)], t_out=t_parte - 0.25, sale="sube_fuera",
          d_out=0.5)
    # el rey sobre su trono: el cielo lo aprueba... y lo castiga
    tr = R.act(A.trono(), pos=(1500, 860, 1.0), t_in=t_rey - 0.05, d_in=0.45, entra="pop", sem=33, sfx=[(0, "pop", 0.6)], z=-1, t_out=t_cae + 0.7, sale="encoger", d_out=0.3)
    rey = R.act(persona(ROJO_CH, PIEL, "corona", "feliz", (25, 120), 0, traje="tunica", faja=ORO, cuello=ORO_OSC, bigote=True), pos=(1500, 840, 0.95), t_in=t_rey, d_in=0.45,
                entra="pop", sem=34, t_out=t_cae + 0.25, sale="caer", d_out=0.9)
    pul1 = pop(R, A.pulgar(True), t_apru, pos=(1130, 430, 0.75), sem=35, t_out=t_mal, sale="encoger", d_out=0.25)
    pul2 = pop(R, A.pulgar(False), t_mal, pos=(1130, 430, 0.75), sem=36, t_out=t_cae + 0.9, sale="encoger", snd="bocinazo", vol=0.35)
    R.act(A.rayo(), pos=(1500, 560, 1.15), t_in=t_cae - 0.05, d_in=0.12, entra="fija", sem=37, z=4, t_out=t_cae + 0.22, sale="cortar", sfx=[(0, "trueno", 0.8), (0, "zap", 0.6)])
    # el reino se parte en siete estados (la fractura continúa en la escena de Qin)
    R.terreno(t_parte - 0.2, "estados", COL["zhou"], 1.2)
    # espadas entre los estados
    for k, (lon, lat) in enumerate(((109.5, 36.5), (114.5, 37.2), (113.0, 32.4))):
        pop(R, A.espadas(), t_pelean + 0.22 * k, geo=(lon, lat), off=(0, 0), s=0.75, sem=40 + k, snd="impacto", vol=0.5, t_out=t_siglos + 0.4, sale="encoger")
