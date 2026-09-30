# -*- coding: utf-8 -*-
"""Coreografía (2/3): Alejandro, partos, sasánidas, conquista árabe y edad de oro, mongoles."""
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

COL = M.COL
PURPURA = P.PURPURA


def construir(R):
    _alejandro(R)
    _partos(R)
    _sasanidas(R)
    _islam(R)
    _mongoles(R)


# ------------------------------------------------------------------ ALEJANDRO
def _alejandro(R):
    e = "alejandro"
    i0 = INI(e)
    t_330, t_llega, t_joven, t_mac, t_alej = T(e, "trescientos"), T(e, "llega"), T(e, "joven"), T(e, "macedonio"), T(e, "alejandro", frase=0)
    t_derr, t_rey, t_ejer, t_inc, t_pers = T(e, "derrota"), T(e, "rey"), T(e, "ejercito"), T(e, "incendia"), T(e, "persepolis")
    t_muere, t_32, t_imp, t_rep = T(e, "muere"), T(e, "treinta", frase=2), T(e, "imperio"), T(e, "reparte")
    R.terreno(i0 - 0.2, "dario", COL["aquemenida"], 0.6)
    R.camara(i0 - 0.3, 32.0, 37.0, 1.6)
    R.camara(t_mac, 30.0, 38.0, 1.9)
    R.camara(t_derr, 42.0, 35.5, 1.9)
    R.camara(t_inc - 0.3, 50.0, 31.5, 2.3)
    R.camara(t_pers + 0.3, 52.9, 30.0, 3.0)
    R.camara(t_muere - 0.3, 52.0, 31.0, 2.4)
    R.camara(t_imp, 47.5, 31.5, 1.45)
    R.camara(FIN(e), 47.5, 31.5, 1.47)
    R.anio(i0, -480)
    R.anio(t_330 - 0.3, -480)
    R.anio(t_330 + 0.6, -330)
    R.anio(t_muere, -330)
    R.anio(t_muere + 0.8, -323)
    # el joven macedonio llega a caballo y avanza por todo el imperio
    Pa = R.rio(M.RUTA_ALEJANDRO, t_llega, 4.2, (206, 70, 70), ancho=14, t1=t_inc - 0.4)
    R.snd(t_llega, "pincel", 0.5, dur=3.0)
    R.act(lambda t: Bb.jinete(int(t * 8), ROJO_CH, "casco_griego", False, False, "enojo"), pos_geo=R.camino_pos(M.RUTA_ALEJANDRO, t_llega + 0.2, 4.0, ease=lambda u: u), off=(0, -18), s=0.34,
          t_in=t_llega + 0.1, d_in=0.4, entra="pop", sem=110, sfx=[(0, "galope", 0.45, {"dur": 4.0})], t_out=t_inc - 0.2, sale="encoger", zs=0.6, z=2)
    R.texto(t_alej - 0.1, t_derr, "ALEJANDRO MAGNO", (960, 190), px=86, d=0.9)
    R.snd(t_alej, "escribir", 0.5, dur=0.9)
    lugar(R, t_mac, t_derr, "MACEDONIA", (22.6, 40.6), off=(0, -20), px=46)
    # derrota al rey: el imperio cambia de color
    R.terreno(t_derr + 0.2, "alejandro", COL["alejandro"], 1.8)
    R.act(persona(PURPURA, PIEL_OSC, "tiara", "miedo", (60, 60), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), geo=(43.4, 36.6), off=(0, 40), s=0.6, t_in=t_rey - 0.1, d_in=0.45, entra="pop", sem=111,
          sfx=[(0, "pop", 0.5)], t_out=t_ejer + 0.2, sale="caer", d_out=0.9, zs=0.5, z=1)
    R.act(A.espadas(), geo=(43.4, 36.3), off=(0, 0), s=0.8, t_in=t_derr, d_in=0.3, entra="pop", sem=112, sfx=[(0, "impacto", 0.7)], t_out=t_ejer, sale="encoger", zs=0.5, z=2)
    # incendia Persépolis
    for k, (dx, h) in enumerate(((-90, 0.9), (0, 1.1), (90, 0.85))):
        R.act(P.columna(0.5), geo=(52.9, 29.9), off=(dx * 1.2, 90), s=0.7, t_in=t_inc - 0.6 + 0.1 * k, d_in=0.45, entra="pop", sem=113 + k, sfx=[], t_out=t_muere - 0.2, sale="encoger", zs=0.5)
        R.act(lambda t, k=k: A.llama(int(t * 9) + k), geo=(52.9, 29.9), off=(dx * 1.2, 10), s=h * 0.9, t_in=t_inc + 0.12 * k, d_in=0.3, entra="pop", sem=116 + k, z=3,
              sfx=[(0, "fuego", 0.5, {"dur": 2.4})] if k == 1 else [], t_out=t_muere - 0.2, sale="encoger", zs=0.5)
    R.texto(t_pers - 0.1, t_muere - 0.3, "PERSÉPOLIS EN LLAMAS", (960, 200), px=84, d=0.9)
    R.snd(t_inc, "crujido", 0.7, dur=0.8)
    # muere joven: 32 años, el imperio se reparte
    R.act(persona(ROJO_CH, PIEL_OSC, "casco_griego", "dormido", (20, 20), 0, traje="armadura", faja=ORO), pos=(960, 830, 0.85), t_in=t_muere - 0.1, d_in=0.45, entra="pop", sem=119,
          sfx=[(0, "pop", 0.5), (0.3, "suspiro", 0.5)], t_out=t_imp - 0.1, sale="encoger", z=2)
    R.contador(t_32 - 0.3, t_32 + 0.7, 0, 32, (960, 300), px=120, formato="{} años")
    R.snd(t_32 - 0.2, "reloj_rapido", 0.45, dur=1.0)
    R.romper("diadocos", t_rep - 0.2, t_rep + 0.5, FIN(e) + 0.2, FIN(e) + 0.8, colores=None, gap=16, deriva=30)
    R.snd(t_rep - 0.2, "crujido", 0.9, dur=0.8)


# ------------------------------------------------------------------ PARTOS
def _partos(R):
    e = "partos"
    i0 = INI(e)
    t_sig, t_partos, t_jin, t_arq = T(e, "siglos"), T(e, "partos"), T(e, "jinetes"), T(e, "arqueros")
    t_fing, t_huir, t_disp, t_flecha = T(e, "fingen"), T(e, "huir"), T(e, "disparan"), T(e, "flecha")
    t_aplast, t_romano, t_carras = T(e, "aplastan"), T(e, "romano"), T(e, "carras")
    t_cinco, t_partia, t_roma, t_mundo = T(e, "cinco"), T(e, "partia"), T(e, "roma", frase=3), T(e, "mundo")
    R.terreno(t_partos - 0.3, "partos", COL["partos"], 1.6)
    R.sello(t_partos + 0.05, "ا", "Partos", color=(206, 110, 50))
    R.camara(i0 - 0.3, 47.5, 31.5, 1.47)
    R.camara(t_partos, 50.0, 34.0, 1.9)
    R.camara(t_fing - 0.3, 46.0, 35.5, 2.2)
    R.camara(t_aplast - 0.3, 40.5, 36.8, 2.7)
    R.camara(t_cinco - 0.2, 44.0, 35.0, 1.9)
    R.camara(FIN(e), 43.0, 35.0, 1.55)
    R.anio(i0, -323)
    R.anio(t_partos, -323)
    R.anio(t_partos + 0.9, -247)
    R.anio(t_carras - 0.2, -247)
    R.anio(t_carras + 0.8, -53)
    # jinetes arqueros
    for k, (lon, lat) in enumerate(((52.0, 35.4), (55.0, 33.6), (53.6, 31.6))):
        R.act(lambda t, k=k: Bb.jinete(int(t * 8) + k, (214, 130, 70), "gorro", True, False, "feliz"), geo=(lon, lat), off=lambda t, k=k: (40 * math.sin(t * 1.3 + k * 2), 10 * math.sin(t * 2 + k)),
              s=0.36, t_in=t_jin + 0.15 * k, d_in=0.4, entra="pop", sem=120 + k, sfx=[(0, "galope", 0.4, {"dur": 2.2})] if k == 0 else [], t_out=t_fing - 0.25, sale="encoger", zs=0.6, z=1)
    lugar(R, t_partos, t_fing - 0.3, "PARTIA", (54.0, 37.0), off=(0, -20), px=64)
    # fingen huir y disparan hacia atrás
    for k, y in enumerate((-40, 20)):
        R.act(lambda t, k=k: Bb.jinete(int(t * 9) + k, (214, 130, 70), "gorro", True, False, "feliz"), pos=lambda t, y=y, k=k: (lerp(700, 1500, prog(t, t_fing, t_disp + 1.2)), 720 + y * 3 + 8 * math.sin(t * 9), 0.52),
              t_in=t_fing - 0.15, d_in=0.3, entra="pop", sem=125 + k, sfx=[(0, "galope", 0.45, {"dur": 2.4})] if k == 0 else [], t_out=t_aplast + 0.5, sale="encoger", z=1)
    for k in range(4):
        tt = t_disp + 0.22 * k
        R.act(Bb.flecha(), pos=lambda t, tt=tt, k=k: (lerp(1150 + 25 * k, 330, e_in(prog(t, tt, tt + 0.7))), 640 + 40 * (k % 2), 0.9, math.pi), t_in=tt, d_in=0.05, entra="fija", sem=128 + k,
              sfx=[(0, "whoosh", 0.4, {"dur": 0.5, "tono": 1.4})], t_out=tt + 0.75, sale="cortar", z=2)
    R.texto(t_flecha - 0.1, t_aplast - 0.2, "LA FLECHA PARTA", (960, 190), px=86, d=0.9)
    R.snd(t_flecha, "escribir", 0.5, dur=0.9)
    # Carras: los romanos caen
    Pr = R.ruta([(32.0, 37.6), (36.0, 37.2), (39.0, 36.9)], t_romano - 0.4, 1.0, ancho=6.0, t1=t_cinco - 0.3)
    for k, (dx, dy) in enumerate(((-90, 20), (0, 50), (90, 10))):
        R.act(persona(ROJO_CH, PIEL_OSC, "casco_griego", "miedo", (60, 60), k % 2, traje="armadura", acc_d="lanza"), geo=(39.0, 36.9), off=(dx, dy), s=0.52, t_in=t_romano + 0.1 * k, d_in=0.4, entra="pop", sem=132 + k,
              sfx=[(0, "pop", 0.4)], t_out=t_aplast + 0.4 + 0.15 * k, sale="caer", d_out=0.8, zs=0.5, z=1)
    R.act(A.estallido(14, 40, 120), geo=(39.0, 36.9), off=(0, -30), s=0.8, t_in=t_aplast, d_in=0.15, entra="fija", sem=135, sfx=[(0, "explosion", 0.6)], t_out=t_aplast + 0.45, sale="cortar", z=3, zs=0.5)
    lugar(R, t_carras - 0.1, t_cinco - 0.3, "CARRAS", (39.0, 36.9), off=(0, -150), px=66)
    # cinco siglos de rivalidad Partia – Roma
    R.act(persona((214, 130, 70), PIEL_OSC, "tiara", "serio", (30, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1460, 800, 0.85), t_in=t_partia - 0.1, d_in=0.45, entra="pop", sem=136,
          sfx=[(0, "pop", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", z=1)
    R.act(persona(ROJO_CH, PIEL_OSC, "casco_griego", "serio", (110, 30), 1, traje="armadura", acc_i="espada"), pos=(460, 800, 0.85), flip=True, t_in=t_roma - 0.1, d_in=0.45, entra="pop", sem=137,
          sfx=[(0, "pop", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", z=1)
    R.texto(t_partia, FIN(e) + 0.2, "PARTIA", (1460, 520), px=74, d=0.6)
    R.texto(t_roma, FIN(e) + 0.2, "ROMA", (460, 520), px=74, d=0.6)
    R.texto(t_cinco - 0.1, FIN(e) + 0.2, "CASI 500 AÑOS", (960, 200), px=86, d=0.9)
    R.snd(t_cinco, "escribir", 0.5, dur=0.9)
    R.act(A.espadas(), pos=(960, 700, 1.0), t_in=t_mundo - 0.2, d_in=0.4, entra="pop", sem=138, sfx=[(0, "impacto", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", z=2)


# ------------------------------------------------------------------ SASÁNIDAS
def _sasanidas(R):
    e = "sasanidas"
    i0 = INI(e)
    t_224, t_nace, t_sasa = T(e, "doscientos"), T(e, "nace"), T(e, "sasanidas")
    t_shapur, t_capt, t_valer, t_jamas = T(e, "shapur"), T(e, "captura"), T(e, "valeriano"), T(e, "jamas")
    t_relig, t_zoro, t_bien, t_mal, t_fuego, t_sag = T(e, "religion"), T(e, "zoroastrismo"), T(e, "bien"), T(e, "mal"), T(e, "fuego"), T(e, "sagrado")
    t_india, t_juego, t_perf, t_ajedrez = T(e, "india"), T(e, "juego"), T(e, "perfeccionan"), T(e, "ajedrez")
    t_sigl, t_bizan, t_agot = T(e, "siglos"), T(e, "bizancio"), T(e, "agotado")
    R.terreno(t_nace - 0.3, "sasanidas", COL["sasanidas"], 1.6)
    R.sello(t_sasa + 0.1, "س", "Sasánidas", color=(52, 120, 124))
    R.camara(i0 - 0.3, 43.0, 35.0, 1.55)
    R.camara(t_nace, 46.0, 33.5, 2.0)
    R.camara(t_shapur, 44.6, 33.6, 2.4)
    R.camara(t_relig - 0.2, 50.0, 32.5, 2.2)
    R.camara(t_india - 0.2, 62.0, 31.0, 1.7)
    R.camara(t_juego + 0.5, 56.0, 32.5, 1.9)
    R.camara(t_sigl - 0.2, 44.0, 35.0, 2.0)
    R.camara(FIN(e), 43.5, 35.0, 1.9)
    R.anio(i0, -53)
    R.anio(t_224 - 0.2, -53)
    R.anio(t_224 + 0.8, 224)
    R.anio(t_capt, 224)
    R.anio(t_capt + 0.8, 260)
    R.anio(t_sigl, 260)
    R.anio(t_sigl + 1.4, 602)
    # nace el imperio, con el gran arco de Ctesifonte
    R.act(P.arco_ctesifonte(), geo=(44.6, 33.1), off=(0, 40), s=0.5, t_in=t_sasa, d_in=0.7, entra="pluma", sem=140, sfx=[(0, "crece", 0.5, {"dur": 0.7})], t_out=t_shapur - 0.2, sale="encoger", zs=0.5)
    lugar(R, t_sasa, t_shapur - 0.3, "CTESIFONTE", (44.6, 33.1), off=(0, -140), px=56)
    # Shapur captura a Valeriano
    R.act(persona(ROJO_CH, PIEL_OSC, "corona_sasanida", "serio", (20, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1300, 800, 1.0), t_in=t_shapur - 0.1, d_in=0.45, entra="pop",
          sem=141, sfx=[(0, "pop", 0.6)], t_out=t_relig - 0.2, sale="encoger", z=1)
    R.act(persona(ROJO_OSC, PIEL_OSC, "casco_griego", "miedo", (150, 150), 0, traje="armadura"), pos=(760, 860, 0.72), t_in=t_valer - 0.1, d_in=0.45, entra="pop", sem=142,
          sfx=[(0, "pop", 0.5), (0.2, "clink", 0.5)], t_out=t_relig - 0.2, sale="encoger", z=1)
    R.texto(t_shapur, t_relig - 0.3, "SHAPUR I", (1300, 470), px=76, d=0.6)
    R.texto(t_valer, t_relig - 0.3, "VALERIANO", (760, 560), px=62, d=0.7)
    R.texto(t_jamas - 0.1, t_relig - 0.3, "¡UN EMPERADOR ROMANO PRISIONERO!", (960, 200), px=70, d=1.1)
    R.snd(t_capt, "impacto", 0.6)
    # zoroastrismo: fuego sagrado, bien y mal
    R.act(lambda t: P.altar_fuego(int(t * 8)), pos=(960, 820, 1.25), t_in=t_zoro - 0.1, d_in=0.5, entra="pop", sem=143, sfx=[(0, "pop", 0.6), (0.1, "fuego", 0.4, {"dur": 3.0})], t_out=t_india - 0.2, sale="encoger", z=1)
    R.act(A.sol_brillo(46), pos=lambda t: (520, 440 + 8 * math.sin(t * 3), 1.0), t_in=t_bien - 0.1, d_in=0.45, entra="pop", sem=144, sfx=[(0, "brillo", 0.5)], t_out=t_india - 0.2, sale="encoger", z=2)
    R.act(Bb.tormenta(), pos=lambda t: (1400, 450 + 8 * math.sin(t * 3 + 1), 0.7), t_in=t_mal - 0.1, d_in=0.45, entra="pop", sem=145, sfx=[(0, "trueno", 0.5)], t_out=t_india - 0.2, sale="encoger", z=2)
    R.texto(t_bien, t_india - 0.3, "BIEN", (520, 590), px=74, d=0.5)
    R.texto(t_mal, t_india - 0.3, "MAL", (1400, 590), px=74, d=0.5)
    # ajedrez: llega de la India
    R.ruta([(77.0, 27.0), (68.0, 30.5), (58.0, 33.0), (50.5, 33.5)], t_india - 0.2, 1.6, ancho=6.0, t1=t_sigl - 0.3)
    lugar(R, t_india, t_juego + 1.0, "INDIA", (76.0, 24.8), off=(0, 0), px=58)
    R.act(P.tablero_ajedrez(), pos=(1420, 740, 1.15), t_in=t_juego - 0.1, d_in=0.5, entra="pop", sem=146, sfx=[(0, "pop", 0.6), (0.2, "tick", 0.5)], t_out=t_sigl - 0.25, sale="encoger", z=2)
    R.texto(t_ajedrez - 0.1, t_sigl - 0.3, "AJEDREZ", (1420, 440), px=90, d=0.8)
    R.snd(t_ajedrez, "escribir", 0.5, dur=0.8)
    # siglos de guerra contra Bizancio: el imperio se agota
    R.terreno(t_sigl + 0.3, "sasanidas", (58, 104, 108), 2.0)
    Pb = R.ruta([(38.0, 36.0), (41.0, 36.0), (44.0, 35.0)], t_bizan - 0.3, 1.2, ancho=6.0)
    R.act(A.espadas(), geo=(39.0, 36.6), off=(0, 0), s=0.8, t_in=t_bizan, d_in=0.3, entra="pop", sem=147, sfx=[(0, "impacto", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.5, z=2)
    lugar(R, t_bizan, FIN(e), "BIZANCIO", (36.0, 38.6), off=(0, -10), px=62)
    R.act(persona(ROJO_CH, PIEL_OSC, "corona_sasanida", "lloron", (40, 40), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1500, 830, 0.85), t_in=t_agot - 0.4, d_in=0.45, entra="pop", sem=148,
          sfx=[(0, "pop", 0.5), (0.3, "suspiro", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", z=1)


# ------------------------------------------------------------------ ISLAM Y EDAD DE ORO
def _islam(R):
    e = "islam"
    i0 = INI(e)
    t_ejer, t_arabia, t_651, t_muere, t_rey, t_islam = T(e, "ejercitos"), T(e, "arabia"), T(e, "seiscientos"), T(e, "muere"), T(e, "rey"), T(e, "islam", frase=1)
    t_persia, t_lengua, t_ident = T(e, "persia"), T(e, "lengua"), T(e, "identidad")
    t_sabios, t_edad, t_avi, t_manual, t_medic, t_europa = T(e, "sabios"), T(e, "edad"), T(e, "avicena"), T(e, "manual"), T(e, "medicina"), T(e, "europa")
    t_juar, t_algo, t_ferd, t_idioma, t_poema, t_cinc, t_versos = T(e, "juarismi"), T(e, "algoritmos"), T(e, "ferdousi"), T(e, "idioma"), T(e, "poema"), T(e, "cincuenta", frase=4), T(e, "versos")
    R.camara(i0 - 0.3, 43.5, 35.0, 1.9)
    R.camara(t_ejer, 43.0, 28.0, 1.7)
    R.camara(t_651 - 0.2, 47.0, 32.5, 1.75)
    R.camara(t_persia - 0.2, 52.0, 32.5, 2.1)
    R.camara(t_sabios - 0.3, 47.0, 33.5, 1.9)
    R.camara(t_avi, 47.0, 33.8, 2.3)
    R.camara(t_juar - 0.2, 50.0, 33.5, 2.0)
    R.camara(FIN(e), 53.0, 34.0, 2.0)
    R.anio(i0, 602)
    R.anio(t_ejer - 0.1, 602)
    R.anio(t_ejer + 0.6, 636)
    R.anio(t_651, 636)
    R.anio(t_651 + 0.9, 651)
    R.anio(t_persia, 651)
    R.anio(t_sabios + 0.4, 1000)
    # ejércitos desde Arabia
    R.rio(M.RUTA_ARABE, t_ejer - 0.1, 3.0, (96, 150, 100), ancho=13, t1=t_651 - 0.3)
    R.snd(t_ejer, "pincel", 0.5, dur=2.6)
    for k in range(3):
        R.act(lambda t, k=k: Bb.jinete(int(t * 8) + k, CREMA, "kufiya", False, False, "enojo"), pos_geo=R.camino_pos(M.RUTA_ARABE, t_ejer + 0.2 + 0.25 * k, 2.8, ease=lambda u: u), off=(0, -18),
              s=0.28, t_in=t_ejer + 0.15 + 0.25 * k, d_in=0.3, entra="pop", sem=150 + k, sfx=[(0, "galope", 0.4, {"dur": 2.8})] if k == 0 else [], t_out=t_651, sale="encoger", zs=0.6, z=1)
    lugar(R, t_arabia, t_651 - 0.2, "ARABIA", (42.0, 26.0), off=(0, 40), px=62)
    # 651: muere el último rey sasánida; llega el islam
    R.terreno(t_muere - 0.1, "califato", COL["califato"], 1.8)
    R.act(persona(ROJO_CH, PIEL_OSC, "corona_sasanida", "miedo", (60, 60), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1400, 800, 0.85), t_in=t_651 - 0.2, d_in=0.45, entra="pop", sem=153,
          sfx=[(0, "pop", 0.5)], t_out=t_rey + 0.5, sale="caer", d_out=0.9, z=1)
    R.texto(t_651 - 0.1, t_persia - 0.3, "651", (960, 200), px=130, d=0.6)
    R.act(P.mezquita(), geo=(44.4, 33.3), off=(0, 40), s=0.36, t_in=t_islam - 0.1, d_in=0.6, entra="pluma", sem=154, sfx=[(0, "crece", 0.45, {"dur": 0.7})], t_out=t_persia - 0.15, sale="encoger", zs=0.5)
    # Persia no desaparece
    campo_extra(R, "iran", COL["safavidas"], t_persia - 0.1, d=0.9, alfa=0.9)
    R.act(P.libro(), pos=(600, 790, 1.2), t_in=t_lengua - 0.1, d_in=0.5, entra="pop", sem=155, sfx=[(0, "pop", 0.6), (0.1, "papel", 0.6)], t_out=t_sabios - 0.2, sale="encoger", z=2)
    R.texto(t_lengua - 0.1, t_sabios - 0.3, "LENGUA PERSA", (960, 190), px=90, d=0.9)
    R.snd(t_lengua, "escribir", 0.5, dur=0.9)
    R.act(A.estrella5(40), pos=lambda t: (1360, 780 + 10 * math.sin(t * 4), 1.0), t_in=t_ident, d_in=0.4, entra="pop", sem=156, sfx=[(0, "bling", 0.5)], t_out=t_sabios - 0.2, sale="encoger", z=2)
    # edad de oro
    R.act(persona(MORADO, PIEL_OSC, "turbante_blanco", "feliz", (30, 110), 0, barba=(236, 236, 240), traje="tunica", faja=ORO, acc_d="frasco"), pos=(520, 800, 0.85), t_in=t_avi - 0.1, d_in=0.45, entra="pop",
          sem=157, sfx=[(0, "pop", 0.6)], t_out=t_juar - 0.2, sale="encoger", z=1)
    R.texto(t_avi, t_juar - 0.3, "AVICENA", (520, 470), px=72, d=0.6)
    R.act(P.libro(), pos=(980, 820, 0.9), t_in=t_manual, d_in=0.45, entra="pop", sem=158, sfx=[(0, "pop", 0.6), (0.1, "papel", 0.5)], t_out=t_juar - 0.2, sale="encoger", z=2)
    R.texto(t_medic - 0.1, t_juar - 0.3, "MEDICINA", (980, 650), px=62, d=0.6)
    Pe = R.ruta([(47.0, 34.0), (38.0, 38.0), (28.0, 42.0), (22.0, 44.5)], t_europa - 0.2, 1.4, ancho=6.0, t1=t_juar - 0.3)
    R.act(P.libro(), pos_geo=R.camino_pos(Pe, t_europa, 2.2, ease=lambda u: u), off=(0, -10), s=0.3, t_in=t_europa - 0.05, d_in=0.3, entra="pop", sem=159, sfx=[(0, "whoosh", 0.4, {"dur": 1.4})],
          t_out=t_juar - 0.25, sale="encoger", zs=0.5, z=2)
    lugar(R, t_europa, t_juar - 0.3, "EUROPA", (22.0, 44.5), off=(0, 40), px=62)
    R.act(persona(AZUL_IMP, PIEL_OSC, "turbante_blanco", "feliz", (30, 100), 1, traje="tunica", faja=ORO, acc_d="rollo"), pos=(520, 800, 0.85), t_in=t_juar - 0.1, d_in=0.45, entra="pop", sem=160,
          sfx=[(0, "pop", 0.6)], t_out=t_ferd - 0.15, sale="encoger", z=1)
    R.texto(t_algo - 0.1, t_ferd - 0.2, "ALGORITMO", (520, 480), px=76, d=0.7)
    R.snd(t_algo, "escribir", 0.5, dur=0.7)
    R.act(persona(VERDE_OSC, PIEL_OSC, "turbante_blanco", "feliz", (30, 110), 0, barba=(60, 50, 50), traje="tunica", faja=ORO, acc_d="pincel"), pos=(1000, 800, 0.85), t_in=t_ferd - 0.1, d_in=0.45, entra="pop",
          sem=161, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.texto(t_ferd, FIN(e) + 0.2, "FERDOUSÍ", (1000, 470), px=72, d=0.6)
    R.act(A.rollo_escritura(3), pos=(1480, 800, 0.95), t_in=t_poema - 0.1, d_in=0.5, entra="pop", sem=162, sfx=[(0, "pop", 0.6), (0.2, "papel", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=2)
    R.contador(t_cinc - 0.3, t_cinc + 1.0, 0, 50000, (1480, 600), px=84)
    R.snd(t_cinc - 0.2, "reloj_rapido", 0.45, dur=1.3)
    R.texto(t_versos - 0.1, FIN(e) + 0.2, "versos", (1480, 670), px=56, d=0.5)


# ------------------------------------------------------------------ MONGOLES
def _mongoles(R):
    e = "mongoles"
    i0 = INI(e)
    t_1219, t_front, t_torm, t_mong, t_gengis = T(e, "diecinueve"), T(e, "frontera"), T(e, "tormenta"), T(e, "mongoles"), T(e, "gengis")
    t_arras, t_ciud, t_nieto, t_bagdad = T(e, "arrasan"), T(e, "ciudades"), T(e, "nieto"), T(e, "bagdad")
    t_siglo, t_tamer, t_conq, t_ruinas = T(e, "siglo"), T(e, "tamerlan"), T(e, "conquistador"), T(e, "ruinas")
    t_inv, t_persa, t_cultura = T(e, "invasores"), T(e, "persa"), T(e, "cultura")
    R.terreno(t_front - 0.3, "mongol", COL["mongol"], 1.6)
    R.camara(i0 - 0.3, 53.0, 34.0, 2.0)
    R.camara(t_front, 66.0, 38.0, 1.7)
    R.camara(t_arras - 0.2, 58.0, 36.5, 1.75)
    R.camara(t_nieto, 50.0, 35.0, 1.8)
    R.camara(t_bagdad, 45.5, 33.6, 2.6)
    R.camara(t_siglo, 58.0, 36.0, 1.7)
    R.camara(t_tamer + 0.3, 64.0, 38.5, 2.2)
    R.camara(t_inv, 52.0, 35.0, 2.1)
    R.camara(FIN(e), 52.0, 34.5, 2.0)
    R.anio(i0, 1000)
    R.anio(t_1219 - 0.5, 1000)
    R.anio(t_1219 + 0.6, 1219)
    R.anio(t_bagdad, 1219)
    R.anio(t_bagdad + 0.8, 1258)
    R.anio(t_siglo, 1258)
    R.anio(t_tamer + 0.8, 1380)
    # la tormenta cruza la frontera
    R.act(Bb.tormenta(), geo=(74.0, 41.0), off=lambda t: (0, -40 + 8 * math.sin(t * 3)), s=0.9, t_in=t_torm - 0.1, d_in=0.45, entra="pop", sem=170, sfx=[(0, "trueno", 0.6)], t_out=t_arras, sale="encoger", zs=0.5, z=3)
    R.rio(M.RUTA_MONGOL, t_mong - 0.1, 3.2, (96, 134, 184), ancho=14, t1=t_nieto - 0.2)
    R.snd(t_mong, "pincel", 0.5, dur=2.8)
    for k in range(4):
        R.act(lambda t, k=k: Bb.jinete(int(t * 9) + k, ROJO_OSC, "gorro", True, False, "enojo"), pos_geo=R.camino_pos(M.RUTA_MONGOL, t_mong + 0.1 + 0.2 * k, 3.0, ease=lambda u: u), off=(0, -14),
              s=0.3, t_in=t_mong + 0.05 + 0.2 * k, d_in=0.3, entra="pop", sem=171 + k, sfx=[(0, "galope", 0.4, {"dur": 3.0})] if k == 0 else [], t_out=t_nieto + 0.2, sale="encoger", zs=0.6, z=1)
    R.texto(t_gengis - 0.1, t_arras - 0.2, "GENGIS KAN", (960, 190), px=90, d=0.9)
    R.snd(t_gengis, "escribir", 0.5, dur=0.9)
    # arrasan ciudades
    for k, (lon, lat) in enumerate(((66.96, 39.65), (62.2, 37.6), (58.8, 36.2), (52.5, 36.0))):
        R.act(lambda t, k=k: C.humo(int(t * 6) + k), geo=(lon, lat), off=(0, -30), s=0.9, t_in=t_ciud + 0.18 * k - 0.2, d_in=0.3, entra="pop", sem=176 + k, peg=False, sfx=[(0, "fuego", 0.35, {"dur": 1.6})] if k == 0 else [],
              t_out=t_bagdad - 0.2, sale="encoger", zs=0.5, z=2)
        R.act(A.estallido(12, 30, 90), geo=(lon, lat), off=(0, -10), s=0.6, t_in=t_ciud + 0.18 * k - 0.2, d_in=0.12, entra="fija", sem=180 + k, sfx=[(0, "explosion", 0.4)], t_out=t_ciud + 0.18 * k, sale="cortar", z=3, zs=0.5)
    # el nieto llega a Bagdad
    R.terreno(t_nieto - 0.1, "ilkanato", COL["mongol"], 1.6)
    R.act(A.estallido(14, 40, 130), geo=(44.36, 33.3), off=(0, -30), s=0.9, t_in=t_bagdad - 0.05, d_in=0.15, entra="fija", sem=184, sfx=[(0, "explosion", 0.7)], t_out=t_bagdad + 0.5, sale="cortar", z=3, zs=0.5)
    R.act(lambda t: C.humo(int(t * 6)), geo=(44.36, 33.3), off=(0, -30), s=1.0, t_in=t_bagdad + 0.2, d_in=0.3, entra="pop", sem=185, peg=False, t_out=t_siglo - 0.2, sale="encoger", zs=0.5, z=2)
    lugar(R, t_bagdad - 0.1, t_siglo - 0.3, "BAGDAD", (44.36, 33.3), off=(0, 50), px=64)
    # Tamerlán
    R.act(lambda t: Bb.jinete(int(t * 9), MORADO, "gorro", True, False, "enojo"), geo=(66.96, 39.65), off=lambda t: (30 * math.sin(t * 1.2), 10), s=0.4, t_in=t_tamer, d_in=0.4, entra="pop", sem=186,
          sfx=[(0, "pop", 0.5), (0.1, "galope", 0.4, {"dur": 2.0})], t_out=t_inv - 0.2, sale="encoger", zs=0.6, z=1)
    lugar(R, t_tamer, t_inv - 0.3, "TAMERLÁN", (66.96, 39.65), off=(0, -130), px=70)
    for k, (lon, lat) in enumerate(((62.0, 36.6), (69.0, 37.0), (65.0, 35.2))):
        R.act(lambda t, k=k: C.humo(int(t * 6) + k), geo=(lon, lat), off=(0, -20), s=0.8, t_in=t_ruinas + 0.15 * k - 0.1, d_in=0.3, entra="pop", sem=187 + k, peg=False, t_out=t_inv - 0.2, sale="encoger", zs=0.5, z=2)
    # los invasores se vuelven persas
    R.terreno(t_persa - 0.1, "ilkanato", COL["iran"], 1.6)
    R.act(persona(ROJO_OSC, PIEL_OSC, "gorro", "feliz", (30, 110), 0, traje="corta", acc_d="rollo"), pos=(700, 820, 0.85), t_in=t_inv - 0.1, d_in=0.45, entra="pop", sem=190, sfx=[(0, "pop", 0.6)],
          t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.act(C.globo_dialogo(), pos=(1000, 560, 1.1), t_in=t_persa - 0.1, d_in=0.45, entra="pop", sem=191, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=2)
    R.texto(t_persa, FIN(e) + 0.2, "PERSA", (1000, 540), px=84, d=0.6)
    R.act(P.libro(), pos=(1440, 830, 1.0), t_in=t_cultura - 0.1, d_in=0.45, entra="pop", sem=192, sfx=[(0, "pop", 0.6), (0.1, "papel", 0.5)], t_out=FIN(e) + 0.4, sale="encoger", z=2)
