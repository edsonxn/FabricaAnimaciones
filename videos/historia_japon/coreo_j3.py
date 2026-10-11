# -*- coding: utf-8 -*-
"""Coreografía (3/3): Meiji, imperialismo, guerra, Japón moderno, cierre y cambios de escena procedurales."""
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
from obj_base import T as TRAZO
from core import INI, FIN, T, kf  # noqa: E402
from coreo_j1 import lugar
from trans import SFX, Transicion

COL = M.COL


def construir(R):
    _meiji(R)
    _imperialismo(R)
    _guerra(R)
    _moderna(R)
    _cierre(R)
    _transiciones(R)


def _tachon():
    return Dib([TRAZO(linea((-150, 30), (150, -30)), 12, peso=0.05), TRAZO(linea((-150, -30), (150, 30)), 12, peso=0.05)])


# ------------------------------------------------------------------ MEIJI
def _meiji(R):
    e = "meiji"
    i0 = INI(e)
    t_1868, t_reb, t_derr, t_shog, t_col, t_trono, t_emp, t_15, t_meiji = T(e, "ochocientos"), T(e, "rebeldes"), T(e, "derrocan"), T(e, "shogun"), T(e, "colocan"), T(e, "trono"), T(e, "emperador"), T(e, "quince"), T(e, "meiji")
    t_com, t_mod, t_vel, t_asom = T(e, "comienza"), T(e, "modernizacion"), T(e, "velocidad"), T(e, "asombrosa")
    t_jap, t_estud, t_occ, t_tren, t_fab, t_esc, t_ejer, t_const = T(e, "japon"), T(e, "estudia"), T(e, "occidente"), T(e, "trenes"), T(e, "fabricas"), T(e, "escuelas"), T(e, "ejercito"), T(e, "constitucion")
    t_sam, t_pierd, t_priv, t_prohibe, t_llevar, t_esp = T(e, "samurais", frase=3), T(e, "pierden"), T(e, "privilegios"), T(e, "prohibe"), T(e, "llevar"), T(e, "espada")
    t_solo, t_30, t_pais, t_aisl, t_pot = T(e, "solo"), T(e, "treinta"), T(e, "pais"), T(e, "aislado"), T(e, "potencia")
    R.terreno(t_1868 - 0.1, "japon", COL["meiji"], 1.2)
    R.sello(t_meiji + 0.2, "明", "Meiji", color=(198, 72, 60))
    R.camara(i0 - 0.3, 137.0, 35.5, 3.8)
    R.camara(t_reb, 135.77, 35.01, 6.0)
    R.camara(t_trono - 0.2, 139.69, 35.69, 7.0)
    R.camara(t_com, 139.6, 35.5, 7.6)
    R.camara(t_jap - 0.3, 139.4, 35.5, 5.2)
    R.camara(t_ejer, 138.5, 35.7, 4.4)
    R.camara(t_sam - 0.2, 139.69, 35.69, 6.4)
    R.camara(t_solo - 0.3, 137.5, 36.5, 3.4)
    R.camara(FIN(e), 138.0, 37.0, 3.0)
    R.anio(i0, 1853)
    R.anio(t_1868 - 0.2, 1853)
    R.anio(t_1868 + 0.9, 1868)
    R.anio(t_solo - 0.2, 1868)
    R.anio(t_solo + 1.6, 1898)
    # samuráis rebeldes derrocan al shogun; sube el joven emperador
    for k, (dx, dy) in enumerate(((-200, 60), (-90, 90), (200, 60))):
        R.act(lambda t, k=k: J.samurai(int(t * 7) + k, (40, 130), "enojo", (200, 70, 70)), geo=(139.69, 35.69), off=(dx, dy), s=0.5, t_in=t_reb + 0.12 * k, d_in=0.4, entra="pop", sem=800 + k,
              sfx=[(0, "pop", 0.4), (0.05, "clink", 0.5)], t_out=t_trono, sale="encoger", zs=0.6, z=1)
    R.act(lambda t: J.samurai(0, (20, 20), "lloron", (60, 100, 160)), geo=(139.69, 35.69), off=(120, 70), s=0.6, t_in=t_shog - 0.3, d_in=0.45, entra="pop", sem=803, sfx=[(0, "pop", 0.4)],
          t_out=t_derr + 0.5, sale="caer", d_out=0.8, zs=0.6, z=1)
    lugar(R, t_derr - 0.2, t_col, "FIN DEL SHOGUNATO", (139.69, 35.69), off=(0, -260), px=62)
    R.act(J.emperador_meiji(0), geo=(139.69, 35.69), off=(0, 50), s=0.6, t_in=t_trono - 0.2, d_in=0.5, entra="pop", sem=804, sfx=[(0, "pop", 0.6), (0.1, "brillo", 0.6)], zs=0.6, z=2)
    R.act(A.trono(1.0), geo=(139.69, 35.69), off=(0, 80), s=0.6, t_in=t_trono - 0.3, d_in=0.4, entra="pop", sem=805, zs=0.6, z=0)
    R.contador(t_15 - 0.3, t_15 + 0.6, 0, 15, (960, 300), px=110, formato="{} años")
    R.snd(t_15 - 0.2, "reloj_rapido", 0.45, dur=0.9)
    R.texto(t_meiji - 0.1, t_com - 0.2, "EMPERADOR MEIJI", (960, 190), px=86, d=0.9)
    R.snd(t_meiji, "escribir", 0.5, dur=0.9)
    # modernización a toda velocidad: el tren Tokio–Yokohama
    Pt = [(139.69, 35.69), (139.66, 35.56), (139.64, 35.44)]
    R.ruta(Pt, t_com, 1.2, ancho=6.0, t1=t_ejer)
    R.act(lambda t: J.locomotora(int(t * 12)), pos_geo=R.camino_pos(Pt, t_vel - 0.3, 1.6, ease=lambda u: u), off=(0, -10), s=0.42, t_in=t_com, d_in=0.4, entra="pop", sem=806,
          sfx=[(0, "pop", 0.5), (0.1, "tren", 0.6, {"dur": 2.0})], t_out=t_jap, sale="encoger", zs=0.7, z=1)
    R.texto(t_mod - 0.1, t_jap - 0.3, "MODERNIZACIÓN", (960, 190), px=96, d=1.0)
    R.snd(t_mod, "escribir", 0.5, dur=1.0)
    # estudia Occidente: trenes, fábricas, escuelas, ejército, constitución
    R.act(lambda t: J.locomotora(int(t * 12)), pos=(480, 840, 0.72), t_in=t_tren - 0.1, d_in=0.4, entra="pop", sem=807, sfx=[(0, "pop", 0.5), (0.1, "tren", 0.5, {"dur": 1.2})], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.act(C.fabrica(), pos=(960, 830, 0.8), t_in=t_fab - 0.1, d_in=0.4, entra="pop", sem=808, sfx=[(0, "pop", 0.5), (0.1, "golpe_suave", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.act(J.obrero_jp(0), pos=(1260, 830, 0.8), t_in=t_esc - 0.1, d_in=0.4, entra="pop", sem=809, sfx=[(0, "pop", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.act(P.libro(True), pos=(1260, 640, 0.9), t_in=t_esc, d_in=0.4, entra="pop", sem=810, sfx=[(0, "papel", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=2)
    R.act(C.soldado_fusil(0, (44, 54, 92)), pos=(1560, 830, 0.85), t_in=t_ejer - 0.1, d_in=0.4, entra="pop", sem=811, sfx=[(0, "pop", 0.5), (0.1, "tambor", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.act(A.rollo_escritura(1), pos=lambda t: (1560, 640 + 6 * math.sin(t * 3), 1.0), t_in=t_const - 0.1, d_in=0.4, entra="pop", sem=812, sfx=[(0, "papel", 0.5), (0.1, "sello", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=2)
    R.texto(t_estud - 0.1, t_sam - 0.3, "JAPÓN ESTUDIA A OCCIDENTE", (960, 190), px=74, d=1.2)
    R.snd(t_estud, "escribir", 0.5, dur=1.0)
    # los samuráis pierden la espada
    R.act(lambda t: J.samurai_paz(int(t * 2), "lloron"), pos=(760, 810, 1.0), t_in=t_sam - 0.1, d_in=0.45, entra="pop", sem=813, sfx=[(0, "pop", 0.5)], t_out=t_solo - 0.3, sale="encoger", z=1)
    R.act(A.espadas(), pos=lambda t: (900 + 160 * prog(t, t_llevar, t_esp + 0.5), 640 + 300 * e_in(prog(t, t_llevar, t_esp + 0.5)), 0.7, 1.6 * prog(t, t_llevar, t_esp + 0.5)), t_in=t_priv, d_in=0.3, entra="pop", sem=814,
          sfx=[(0, "pop", 0.4)], t_out=t_esp + 0.6, sale="cortar", z=2)
    R.act(_tachon(), pos=(1000, 660, 1.4), t_in=t_prohibe + 0.1, d_in=0.25, entra="pop", sem=815, sfx=[(0, "impacto", 0.6)], t_out=t_solo - 0.3, sale="encoger", z=3)
    R.texto(t_pierd - 0.1, t_solo - 0.3, "SIN PRIVILEGIOS", (960, 190), px=86, d=0.9)
    # en treinta años: de país aislado a potencia
    R.contador(t_30 - 0.3, t_30 + 0.7, 0, 30, (960, 300), px=120, formato="{} años")
    R.snd(t_30 - 0.2, "reloj_rapido", 0.45, dur=1.0)
    R.act(J.bandera_japon(), pos=lambda t: (960, 830, 1.1), t_in=t_pais - 0.1, d_in=0.45, entra="pop", sem=816, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", z=1)
    R.act(J.sol_naciente(), pos=lambda t: (1420, 700 + 6 * math.sin(t * 3), 0.85), t_in=t_pot - 0.2, d_in=0.5, entra="pop", sem=817, sfx=[(0, "brillo", 0.6), (0.1, "bling", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", z=1)
    R.texto(t_pot - 0.1, FIN(e) + 0.3, "¡POTENCIA!", (960, 190), px=120, d=0.7)
    R.snd(t_pot, "escribir", 0.5, dur=0.7)


# ------------------------------------------------------------------ IMPERIALISMO
def _imperialismo(R):
    e = "imperialismo"
    i0 = INI(e)
    t_y, t_pot, t_eur, t_jap, t_lanza, t_conq = T(e, "potencias"), T(e, "potencias"), T(e, "europeas"), T(e, "japon"), T(e, "lanza"), T(e, "conquistar")
    t_1905, t_cinco, t_derr, t_rusia, t_ning, t_asia, t_europ = T(e, "novecientos"), T(e, "cinco"), T(e, "derrota"), T(e, "rusia"), T(e, "ningun"), T(e, "asiatico"), T(e, "europeo")
    t_anexa, t_corea, t_invade, t_manch, t_37, t_china = T(e, "anexa"), T(e, "corea"), T(e, "invade"), T(e, "manchuria"), T(e, "siete"), T(e, "china")
    t_41, t_ataca, t_base, t_pearl, t_entra, t_seg, t_guerra = T(e, "cuarenta"), T(e, "ataca"), T(e, "base"), T(e, "pearl"), T(e, "entra"), T(e, "segunda"), T(e, "mundial")
    R.camara(i0 - 0.3, 136.0, 35.5, 3.0)
    R.camara(t_lanza, 131.0, 37.0, 3.3)
    R.camara(t_1905 - 0.2, 127.0, 39.0, 3.8)
    R.camara(t_anexa - 0.3, 126.0, 38.0, 3.6)
    R.camara(t_manch, 126.5, 42.0, 3.6)
    R.camara(t_41 - 0.3, 138.0, 34.0, 3.0)
    R.camara(t_pearl, 141.5, 32.5, 3.2)
    R.camara(FIN(e), 142.0, 32.0, 3.0)
    R.anio(i0, 1898)
    R.anio(t_1905 - 0.2, 1898)
    R.anio(t_1905 + 1.0, 1905)
    R.anio(t_anexa - 0.2, 1905)
    R.anio(t_anexa + 0.8, 1910)
    R.anio(t_37 - 0.3, 1910)
    R.anio(t_37 + 0.3, 1937)
    R.anio(t_41 - 0.3, 1937)
    R.anio(t_41 + 1.0, 1941)
    # como las potencias europeas, Japón se lanza a conquistar
    R.act(Bb.carabela(), pos=(480, 830, 0.42), t_in=t_eur - 0.1, d_in=0.4, entra="pop", sem=830, sfx=[(0, "pop", 0.5)], t_out=t_jap, sale="encoger", z=1)
    R.act(J.barco_negro(0), pos=(1480, 830, 0.36), t_in=t_jap - 0.2, d_in=0.4, entra="pop", sem=831, sfx=[(0, "pop", 0.5), (0.1, "cuerno", 0.5)], t_out=t_conq + 0.5, sale="izq_fuera", d_out=0.8, z=1)
    R.texto(t_lanza - 0.1, t_1905 - 0.3, "¡A CONQUISTAR!", (960, 190), px=108, d=0.8)
    R.snd(t_lanza, "escribir", 0.5, dur=0.8)
    R.snd(t_conq, "tambor", 0.6)
    # 1905: derrota a Rusia
    R.act(persona((150, 100, 100), PIEL_ROSA, "gorro", "miedo", (60, 60), 0, traje="armadura"), pos=(520, 810, 0.95), t_in=t_rusia - 0.1, d_in=0.45, entra="pop", sem=832, sfx=[(0, "pop", 0.5)],
          t_out=t_ning - 0.1, sale="caer", d_out=0.8, z=1)
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "feliz", (44, 54, 92)), pos=(1400, 810, 1.0), t_in=t_derr - 0.2, d_in=0.45, entra="pop", sem=833, sfx=[(0, "pop", 0.5), (0.2, "bling", 0.5)], t_out=FIN(e) - 4.0, sale="encoger", z=1)
    R.act(A.estallido(14, 40, 120), pos=(960, 640, 1.3), t_in=t_derr + 0.1, d_in=0.12, entra="fija", sem=834, sfx=[(0, "explosion", 0.6)], t_out=t_derr + 0.5, sale="cortar", z=3)
    R.texto(t_derr - 0.1, t_ning - 0.2, "¡DERROTA A RUSIA!", (960, 190), px=90, d=0.8)
    R.act(A.signo_pregunta(), pos=lambda t: (960, 560 + 8 * math.sin(t * 4), 0.9), t_in=t_asia - 0.2, d_in=0.4, entra="pop", sem=835, sfx=[(0, "bling", 0.5)], t_out=t_europ + 0.5, sale="encoger", z=2)
    R.texto(t_asia - 0.3, t_europ + 0.6, "ASIA > EUROPA", (960, 330), px=88, d=0.9)
    # anexa Corea, invade Manchuria y China: el imperio crece
    R.terreno(t_anexa - 0.3, "imperio", COL["imperio"], 2.6)
    R.ruta(M.RUTA_COREA[::-1], t_anexa - 0.2, 1.5, ancho=6.0, t1=t_41)
    R.act(lambda t: J.samurai(int(t * 6), (40, 130), "enojo", (44, 54, 92)), geo=(127.0, 37.5), off=(0, 40), s=0.5, t_in=t_corea - 0.1, d_in=0.45, entra="pop", sem=836, sfx=[(0, "pop", 0.5)], t_out=t_41 - 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_corea, t_invade, "COREA", (127.2, 37.5), off=(0, -130), px=64)
    R.act(lambda t: J.samurai(int(t * 6), (40, 130), "enojo", (44, 54, 92)), geo=(125.0, 43.5), off=(0, 40), s=0.5, t_in=t_invade - 0.1, d_in=0.45, entra="pop", sem=837, sfx=[(0, "pop", 0.5), (0.1, "canonazo", 0.4)], t_out=t_41 - 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_manch, t_37, "MANCHURIA", (125.0, 43.5), off=(0, -130), px=64)
    R.act(lambda t: J.samurai(int(t * 6), (40, 130), "enojo", (44, 54, 92)), geo=(121.5, 39.0), off=(0, 40), s=0.5, t_in=t_china - 0.1, d_in=0.45, entra="pop", sem=838, sfx=[(0, "pop", 0.5), (0.1, "canonazo", 0.4)], t_out=t_41 - 0.3, sale="encoger", zs=0.6, z=1)
    lugar(R, t_china, t_41 - 0.3, "CHINA", (121.5, 39.0), off=(0, -130), px=64)
    R.snd(t_anexa, "crujido", 0.6, dur=0.6)
    # Pearl Harbor: ataque con aviones hacia el Pacífico
    R.ruta(M.RUTA_PACIFICO, t_ataca - 0.3, 2.0, ancho=7.0, t1=FIN(e))
    for k in range(3):
        R.act(lambda t, k=k: J.avion_zero(int(t * 10) + k), pos_geo=R.camino_pos(M.RUTA_PACIFICO, t_ataca + 0.15 * k, 2.4), off=(0, -30 - 40 * k), s=0.3, t_in=t_ataca + 0.15 * k, d_in=0.35, entra="pop", sem=839 + k,
              sfx=[(0, "pop", 0.4), (0.05, "whoosh", 0.4, {"dur": 1.6, "tono": 0.8})], t_out=t_pearl + 0.6, sale="encoger", zs=0.7, z=2)
    lugar(R, t_pearl - 0.1, FIN(e), "PEARL HARBOR →", (148.6, 29.0), off=(0, -90), px=60)
    R.act(J.bandera_japon(), geo=(139.7, 35.2), off=(0, 60), s=0.65, t_in=t_entra, d_in=0.4, entra="pop", sem=842, sfx=[(0, "pop", 0.5)], zs=0.7, z=1)
    R.texto(t_seg - 0.1, FIN(e) + 0.3, "SEGUNDA GUERRA MUNDIAL", (960, 190), px=74, d=1.3)
    R.snd(t_seg, "escribir", 0.5, dur=1.2)
    R.snd(t_pearl, "gong", 0.6)


# ------------------------------------------------------------------ GUERRA
def _guerra(R):
    e = "guerra"
    i0 = INI(e)
    t_prin, t_conq, t_pac, t_pero, t_eeuu, t_contra, t_isla = T(e, "principio"), T(e, "conquista"), T(e, "pacifico"), T(e, "pero"), T(e, "estados"), T(e, "contraataca"), T(e, "isla")
    t_ciud, t_jps, t_bomb = T(e, "ciudades"), T(e, "japonesas"), T(e, "bombardeadas")
    t_ago, t_45, t_dos, t_bombas, t_atom, t_destr, t_hiro, t_naga = T(e, "agosto"), T(e, "cuarenta"), T(e, "dos"), T(e, "bombas"), T(e, "atomicas"), T(e, "destruyen"), T(e, "hiroshima"), T(e, "nagasaki")
    t_emp, t_habla, t_radio, t_prim, t_vez, t_anun, t_rend = T(e, "emperador"), T(e, "habla"), T(e, "radio"), T(e, "primera"), T(e, "vez"), T(e, "anuncia"), T(e, "rendicion")
    t_jap, t_queda, t_arr, t_ocup, t_eeuu2 = T(e, "japon", frase=4), T(e, "queda"), T(e, "arrasado"), T(e, "ocupado"), T(e, "estadounidenses")
    R.camara(i0 - 0.3, 142.0, 32.0, 3.0)
    R.camara(t_conq, 136.0, 34.0, 2.3)
    R.camara(t_pero - 0.2, 142.0, 33.0, 2.7)
    R.camara(t_ciud - 0.2, 138.5, 35.5, 4.0)
    R.camara(t_ago - 0.3, 132.0, 34.0, 6.0)
    R.camara(t_hiro, 132.4, 34.2, 7.0)
    R.camara(t_naga - 0.2, 130.5, 33.4, 7.2)
    R.camara(t_emp - 0.3, 137.0, 35.5, 4.0)
    R.camara(t_queda - 0.2, 137.5, 36.0, 3.5)
    R.camara(FIN(e), 138.0, 36.5, 3.0)
    R.anio(i0, 1941)
    R.anio(t_ago - 0.3, 1941)
    R.anio(t_ago + 1.0, 1945)
    # al principio conquista medio Pacífico; luego EE. UU. contraataca isla por isla
    R.act(lambda t: J.avion_zero(int(t * 10)), pos=lambda t: (lerp(-200, 2100, prog(t, t_prin, t_pero)), 400 + 40 * math.sin(t * 2), 0.4), t_in=t_prin, d_in=0.2, entra="fija", sem=850,
          sfx=[(0, "whoosh", 0.4, {"dur": 2.0, "tono": 0.8})], t_out=t_pero, sale="cortar", z=2)
    R.texto(t_conq - 0.1, t_pero - 0.3, "MEDIO PACÍFICO", (960, 200), px=92, d=0.9)
    R.snd(t_conq, "escribir", 0.5, dur=0.9)
    Pi = [(151.0, 29.0), (147.0, 31.0), (143.0, 33.0), (140.0, 34.8)]
    R.ruta(Pi, t_eeuu - 0.3, 2.0, ancho=7.0, t1=t_ciud)
    R.act(J.marino_yanqui(0), pos=(520, 810, 1.0), t_in=t_eeuu - 0.1, d_in=0.45, entra="pop", sem=851, sfx=[(0, "pop", 0.5)], t_out=t_ciud - 0.2, sale="encoger", z=1)
    for k, (lon, lat) in enumerate(((151.0, 29.0), (147.0, 31.0), (143.0, 33.0))):
        R.act(C.isla_trozo(40), geo=(lon, lat), off=(0, 20), s=0.55, t_in=t_isla + 0.25 * k, d_in=0.4, entra="pop", sem=852 + k, sfx=[(0, "pop", 0.4), (0.1, "pluck", 0.5, {"tono": 1.0 + 0.25 * k})], t_out=t_ciud - 0.2, sale="encoger", zs=0.7, z=1)
    R.texto(t_contra - 0.1, t_ciud - 0.3, "ISLA POR ISLA", (960, 200), px=92, d=0.9)
    # ciudades bombardeadas
    R.terreno(t_ciud, "japon", (170, 136, 170), 1.6)
    for k, (lon, lat) in enumerate(((139.69, 35.69), (135.5, 34.69), (136.9, 35.18))):
        R.act(lambda t, k=k: A.llama(int(t * 9) + k), geo=(lon, lat), off=(0, -10), s=0.45, t_in=t_bomb + 0.2 * k - 0.4, d_in=0.3, entra="pop", sem=855 + k, z=3, zs=0.7,
              sfx=[(0, "fuego", 0.4, {"dur": 2.0})] if k == 0 else [])
    R.texto(t_ciud - 0.1, t_ago - 0.4, "CIUDADES BOMBARDEADAS", (960, 200), px=76, d=1.2)
    R.snd(t_ciud, "escribir", 0.5, dur=1.0)
    R.snd(t_bomb, "siseo", 0.4, dur=1.0)
    # 1945: Hiroshima y Nagasaki
    R.act(J.hongo(0), geo=(132.46, 34.39), off=(0, 40), s=0.5, t_in=t_hiro - 0.1, d_in=0.7, entra="pluma", sem=858, sfx=[(0, "explosion", 0.7), (0.2, "trueno", 0.6)], zs=0.8, z=2)
    lugar(R, t_hiro, t_emp - 0.3, "HIROSHIMA", (132.46, 34.39), off=(0, -330), px=70)
    R.act(J.hongo(0), geo=(129.87, 32.75), off=(0, 40), s=0.5, t_in=t_naga - 0.1, d_in=0.7, entra="pluma", sem=859, sfx=[(0, "explosion", 0.7), (0.2, "trueno", 0.6)], zs=0.8, z=2)
    lugar(R, t_naga, t_emp - 0.3, "NAGASAKI", (129.87, 32.75), off=(0, -330), px=70)
    R.contador(t_dos - 0.3, t_dos + 0.4, 0, 2, (960, 300), px=130, formato="{} bombas")
    # el emperador habla por radio por primera vez
    R.act(J.radio(), pos=(1400, 830, 1.5), t_in=t_radio - 0.1, d_in=0.5, entra="pop", sem=860, sfx=[(0, "pop", 0.5), (0.2, "tick", 0.4)], t_out=t_jap - 0.3, sale="encoger", z=1)
    R.act(J.emperador_jp(0, "serio"), pos=(620, 810, 1.0), t_in=t_emp - 0.1, d_in=0.45, entra="pop", sem=861, sfx=[(0, "pop", 0.5)], t_out=t_jap - 0.3, sale="encoger", z=1)
    R.texto(t_prim - 0.1, t_jap - 0.4, "¡PRIMERA VEZ POR RADIO!", (960, 200), px=72, d=1.2)
    R.texto(t_rend - 0.1, t_jap - 0.4, "RENDICIÓN", (960, 340), px=92, d=0.7)
    R.snd(t_rend, "suspiro", 0.5)
    # arrasado y ocupado
    R.terreno(t_ocup - 0.3, "japon", (150, 140, 150), 1.6)
    R.act(J.marino_yanqui(0), geo=(139.7, 35.6), off=(0, 40), s=0.6, t_in=t_ocup - 0.1, d_in=0.45, entra="pop", sem=862, sfx=[(0, "pop", 0.5)], zs=0.7, z=1)
    R.texto(t_arr - 0.1, FIN(e) + 0.3, "ARRASADO Y OCUPADO", (960, 200), px=82, d=1.2)
    R.snd(t_arr, "escribir", 0.5, dur=1.0)


# ------------------------------------------------------------------ MODERNA
def _moderna(R):
    e = "moderna"
    i0 = INI(e)
    t_pero, t_lev, t_nuevo = T(e, "pero"), T(e, "levanta"), T(e, "nuevo")
    t_47, t_aprueba, t_const, t_renun, t_siempre, t_guerra = T(e, "cuarenta"), T(e, "aprueba"), T(e, "constitucion"), T(e, "renuncia"), T(e, "siempre"), T(e, "guerra")
    t_64, t_org, t_juegos, t_tokio, t_estrena, t_tren, t_bala = T(e, "sesenta"), T(e, "organiza"), T(e, "juegos"), T(e, "tokio"), T(e, "estrena"), T(e, "tren"), T(e, "bala")
    t_pocas, t_dec, t_conv, t_mayores, t_econ, t_plan = T(e, "pocas"), T(e, "decadas"), T(e, "convierte"), T(e, "mayores"), T(e, "economias"), T(e, "planeta")
    t_hoy, t_viven, t_ciento, t_mill, t_pers, t_pob, t_env = T(e, "hoy"), T(e, "viven"), T(e, "ciento"), T(e, "millones"), T(e, "personas"), T(e, "poblaciones"), T(e, "envejecidas")
    t_cer, t_flor, t_prim, t_mil = T(e, "cerezos"), T(e, "florecen"), T(e, "primavera"), T(e, "mil", frase=5)
    R.terreno(t_lev - 0.2, "japon", COL["japon"], 2.0)
    R.camara(i0 - 0.3, 138.0, 36.5, 3.0)
    R.camara(t_47 - 0.3, 139.69, 35.69, 6.0)
    R.camara(t_64 - 0.3, 138.5, 35.3, 5.0)
    R.camara(t_bala, 137.0, 35.0, 4.2)
    R.camara(t_pocas - 0.2, 138.5, 36.0, 3.6)
    R.camara(t_hoy - 0.2, 138.0, 36.5, 3.0)
    R.camara(t_cer - 0.3, 138.5, 36.0, 4.2)
    R.camara(t_prim, 138.0, 37.0, 3.0)
    R.camara(FIN(e), 138.0, 37.0, 2.6)
    R.anio(i0, 1945)
    R.anio(t_47 - 0.3, 1945)
    R.anio(t_47 + 0.8, 1947)
    R.anio(t_64 - 0.3, 1947)
    R.anio(t_64 + 0.8, 1964)
    R.anio(t_hoy - 0.4, 1964)
    R.anio(t_hoy + 1.2, 2026)
    # se levanta: brota un cerezo entre las ruinas
    R.act(J.cerezo(0, 0.0), pos=(960, 830, 1.0), t_in=t_pero - 0.1, d_in=0.6, entra="pluma", sem=870, sfx=[(0, "crece", 0.5, {"dur": 0.7})], t_out=t_47 - 0.3, sale="encoger", z=1)
    R.texto(t_lev - 0.1, t_47 - 0.4, "SE LEVANTA", (960, 200), px=110, d=0.9)
    R.snd(t_lev, "escribir", 0.5, dur=0.9)
    R.snd(t_nuevo, "bling", 0.6)
    # constitución que renuncia a la guerra
    R.act(P.libro(True), pos=(720, 800, 1.6), t_in=t_const - 0.2, d_in=0.5, entra="pop", sem=871, sfx=[(0, "pop", 0.5), (0.1, "papel", 0.5)], t_out=t_64 - 0.3, sale="encoger", z=1)
    R.act(A.espadas(), pos=(1300, 800, 1.3), t_in=t_renun - 0.1, d_in=0.4, entra="pop", sem=872, sfx=[(0, "clink", 0.5)], t_out=t_64 - 0.3, sale="encoger", z=1)
    R.act(_tachon(), pos=(1300, 790, 1.7), t_in=t_siempre, d_in=0.25, entra="pop", sem=873, sfx=[(0, "impacto", 0.6)], t_out=t_64 - 0.3, sale="encoger", z=2)
    R.texto(t_const - 0.1, t_64 - 0.4, "NUNCA MÁS LA GUERRA", (960, 200), px=82, d=1.2)
    R.snd(t_const, "escribir", 0.5, dur=1.0)
    # Juegos Olímpicos y tren bala
    R.act(J.aros_olimpicos(), pos=lambda t: (620, 740 + 8 * math.sin(t * 3), 2.0), t_in=t_juegos - 0.1, d_in=0.5, entra="pop", sem=874, sfx=[(0, "pop", 0.6), (0.1, "bling", 0.6)], t_out=t_pocas - 0.3, sale="encoger", z=1)
    lugar(R, t_tokio - 0.1, t_pocas - 0.4, "TOKIO 1964", (139.69, 35.69), off=(0, -130), px=64)
    Pb = [(139.69, 35.69), (137.0, 35.1), (135.5, 34.69)]
    R.ruta(Pb, t_estrena - 0.1, 1.6, ancho=7.0, t1=t_pocas)
    R.act(C.tren_bala(), pos_geo=R.camino_pos(Pb, t_tren, 1.8, ease=lambda u: u), off=(0, -30), s=0.4, t_in=t_estrena, d_in=0.4, entra="pop", sem=875, sfx=[(0, "pop", 0.5), (0.1, "tren", 0.6, {"dur": 2.0, "tono": 1.4})],
          t_out=t_pocas - 0.2, sale="encoger", zs=0.7, z=2)
    R.texto(t_bala - 0.1, t_pocas - 0.4, "¡TREN BALA!", (960, 200), px=100, d=0.7)
    # una de las mayores economías del planeta
    R.act(C.rascacielos(300, 90, (120, 150, 190)), pos=(560, 810, 1.0), t_in=t_dec - 0.1, d_in=0.45, entra="pop", sem=876, sfx=[(0, "pop", 0.5)], t_out=t_hoy - 0.3, sale="encoger", z=1)
    R.act(C.rascacielos(400, 100, (150, 130, 190)), pos=(700, 810, 1.0), t_in=t_conv - 0.1, d_in=0.45, entra="pop", sem=877, sfx=[(0, "pop", 0.5)], t_out=t_hoy - 0.3, sale="encoger", z=1)
    R.act(C.fabrica(), pos=(1000, 830, 0.85), t_in=t_mayores - 0.1, d_in=0.45, entra="pop", sem=878, sfx=[(0, "pop", 0.5)], t_out=t_hoy - 0.3, sale="encoger", z=1)
    R.act(A.bolsa_dinero(), pos=(1380, 830, 1.0), t_in=t_econ - 0.1, d_in=0.45, entra="pop", sem=879, sfx=[(0, "pop", 0.5), (0.1, "monedas", 0.6)], t_out=t_hoy - 0.3, sale="encoger", z=1)
    R.act(A.moneda(62), pos=lambda t: (1560, 700 + 20 * math.sin(t * 4), 1.0), t_in=t_plan - 0.2, d_in=0.4, entra="pop", sem=880, sfx=[(0, "bling", 0.5)], t_out=t_hoy - 0.3, sale="encoger", z=2)
    R.texto(t_econ - 0.1, t_hoy - 0.4, "GRAN ECONOMÍA", (960, 200), px=90, d=0.9)
    # hoy: 124 millones de personas, muy envejecidos
    R.contador(t_ciento - 0.3, t_mill + 0.2, 0, 124, (960, 300), px=130, formato="{} millones")
    R.snd(t_ciento - 0.2, "reloj_rapido", 0.45, dur=1.6)
    R.act(A.multitud(8, 3), pos=(960, 830, 1.15), t_in=t_pers - 0.1, d_in=0.5, entra="pop", sem=881, sfx=[(0, "pop", 0.5)], t_out=t_cer - 0.3, sale="encoger", z=1)
    R.texto(t_pob - 0.1, t_cer - 0.4, "DE LAS MÁS ENVEJECIDAS", (960, 430), px=70, d=1.2)
    R.snd(t_env, "hmm", 0.5)
    # los cerezos florecen
    for k, (x, s) in enumerate(((420, 1.0), (960, 1.25), (1500, 1.0))):
        R.act(lambda t, k=k: J.cerezo(0, 1.0), pos=(x, 850, s), t_in=t_cer + 0.25 * k, d_in=0.6, entra="pluma", sem=882 + k, sfx=[(0, "crece", 0.5, {"dur": 0.6}), (0.4, "brillo", 0.4)], z=1)
    for k in range(5):
        R.act(J.nube_petalos(8), pos=lambda t, k=k: (300 + 330 * k + 30 * math.sin(t * 1.3 + k), 300 + 220 * ((t * 0.3 + 0.2 * k) % 1.0), 1.2, 0.6 * math.sin(t + k)), t_in=t_flor + 0.1 * k, d_in=0.4, entra="fija", sem=885 + k, z=3)
    R.texto(t_flor - 0.1, FIN(e) + 0.3, "CADA PRIMAVERA", (960, 200), px=96, d=0.9)
    R.snd(t_flor, "escribir", 0.5, dur=0.9)
    R.sello_libre(t_mil - 0.2, FIN(e) + 0.4, "桜", 1660, 360, px=150)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_pais, t_aisl, t_abrio, t_cayo, t_reinv, t_ident = T(e, "pais"), T(e, "aislo"), T(e, "abrio"), T(e, "cayo"), T(e, "reinvento"), T(e, "identidad")
    t_que, t_quieres, t_cinco, t_min, t_dimelo, t_coment = T(e, "que", frase=1), T(e, "quieres"), T(e, "cinco"), T(e, "minutos"), T(e, "dimelo"), T(e, "comentarios")
    R.camara(i0 - 0.3, 138.0, 37.0, 2.6)
    R.camara(t_abrio, 137.0, 36.0, 2.4)
    R.camara(t_reinv - 0.3, 138.0, 36.0, 3.0)
    R.camara(t_ident, 138.0, 36.5, 2.8)
    R.camara(FIN(e), 138.0, 36.5, 2.5)
    R.anio(i0, 2026)
    # aislado, abierto, caído, reinventado
    R.act(lambda t: Bb.gran_puerta_cerrada(round(kf(t, [(t_aisl - 0.2, 0.0), (t_aisl + 0.6, 1.0), (t_abrio - 0.1, 1.0), (t_abrio + 0.5, 0.0)]), 1)), pos=(560, 790, 1.2), t_in=t_aisl - 0.2, d_in=0.45, entra="pop", sem=890,
          sfx=[(0, "pop", 0.5), (0.5, "golpe_suave", 0.6)], t_out=t_cayo - 0.1, sale="encoger", z=1)
    R.texto(t_aisl - 0.1, t_cayo - 0.2, "SE AISLÓ", (560, 480), px=68, d=0.6)
    R.texto(t_abrio - 0.1, t_cayo - 0.2, "SE ABRIÓ", (560, 560), px=68, d=0.6)
    R.snd(t_abrio, "crujido", 0.7, dur=0.6)
    R.act(J.hongo(0), pos=(1000, 830, 0.75), t_in=t_cayo - 0.1, d_in=0.5, entra="pop", sem=891, sfx=[(0, "pop", 0.5), (0.1, "trueno", 0.5)], t_out=t_reinv - 0.1, sale="encoger", z=1)
    R.texto(t_cayo - 0.1, t_reinv - 0.2, "CAYÓ", (1000, 470), px=76, d=0.6)
    R.act(J.cerezo(0, 1.0), pos=(1400, 850, 1.0), t_in=t_reinv - 0.1, d_in=0.6, entra="pluma", sem=892, sfx=[(0, "crece", 0.5, {"dur": 0.6}), (0.3, "brillo", 0.5)], z=1)
    R.texto(t_reinv - 0.1, t_que - 0.2, "SE REINVENTÓ", (1400, 470), px=68, d=0.8)
    R.act(J.sol_naciente(), pos=lambda t: (960, 330 + 6 * math.sin(t * 3), 0.9), t_in=t_ident - 0.2, d_in=0.5, entra="pop", sem=893, sfx=[(0, "brillo", 0.6), (0.1, "bling", 0.6)], t_out=t_que - 0.2, sale="encoger", z=0)
    # pregunta al público
    paises = [(260, 620), (560, 420), (860, 640), (1160, 430), (1460, 650), (1720, 440)]
    for k, (x, y) in enumerate(paises):
        R.act(A.signo_pregunta(), pos=lambda t, k=k, x=x, y=y: (x, y + 12 * math.sin(t * 4 + k), 0.72), t_in=t_quieres + 0.13 * k, d_in=0.4, entra="pop", sem=895 + k,
              sfx=[(0, "pluck", 0.5, {"tono": (1.0, 1.125, 1.26, 1.5, 1.68, 2.0)[k]})], z=1)
    R.texto(t_min, FIN(e) + 1.0, "¿cuál sigue?", (960, 200), px=112, d=0.9)
    R.act(C.boton_suscribir(), pos=lambda t: (960, 800 + 4 * math.sin(t * 5), 1.0), t_in=t_coment - 0.6, d_in=0.5, entra="pop", sem=910, sfx=[(0, "pop", 0.7), (0.1, "bling", 0.6)], z=2)
    R.texto(t_coment - 0.4, FIN(e) + 1.0, "SUSCRÍBETE", (960, 800), px=76, d=0.7)
    R.act(C.campana(), pos=lambda t: (1270, 790, 0.8, 0.35 * math.sin((t - t_coment) * 9) * math.exp(-(t - t_coment) * 0.4)), t_in=t_coment - 0.3, d_in=0.4, entra="pop", sem=911,
          sfx=[(0, "pop", 0.6), (0.1, "campana", 0.6)], z=2)
    R.act(C.globo_dialogo(), pos=(1470, 520, 1.1), t_in=t_coment - 0.1, d_in=0.45, entra="pop", sem=912, sfx=[(0, "pop", 0.6)], z=2)
    R.texto(t_coment, FIN(e) + 1.0, "...", (1470, 500), px=92, d=0.4)


# ------------------------------------------------------------------ CAMBIOS DE ESCENA (procedurales, sin cortes)
def _transiciones(R):
    ids = ["gancho", "origenes", "imperio", "heian", "shogun", "mongoles", "sengoku", "unificacion", "edo", "perry", "meiji", "imperialismo", "guerra", "moderna", "cierre"]
    spec = [
        ("tinta", COL["jomon"], (960, 170), (1000, 620)),
        ("pincel", COL["yayoi"], (960, 540), (960, 540)),
        ("papel", COL["yamato"], (960, 540), (960, 540)),
        ("portal", COL["heian"], (1000, 800), (700, 820)),
        ("puntos", COL["shogun"], (960, 540), (960, 540)),
        ("ola", COL["mongol"], (960, 540), (960, 540)),
        ("persianas", COL["sengoku"], (960, 540), (960, 540)),
        ("tinta", (62, 56, 74), (1000, 700), (960, 540)),
        ("rollo", COL["tokugawa"], (960, 540), (960, 540)),
        ("pincel", (44, 44, 52), (960, 540), (960, 540)),
        ("portal", COL["meiji"], (1640, 800), (520, 820)),
        ("papel", COL["imperio"], (960, 540), (960, 540)),
        ("ola", (150, 140, 150), (960, 540), (960, 540)),
        ("puntos", (186, 214, 216), (960, 540), (960, 540)),
    ]
    for k, (tipo, color, a, b) in enumerate(spec):
        tc = (FIN(ids[k]) + INI(ids[k + 1])) / 2
        R.trans.append(Transicion(tc, tipo, color, a, b, dur=0.8, seed=k + 1))
        R.snd(tc - 0.36, SFX[tipo], 0.55, dur=0.8) if SFX[tipo] in ("pincel", "zoom_whoosh", "ola") else R.snd(tc - 0.36, SFX[tipo], 0.55)
