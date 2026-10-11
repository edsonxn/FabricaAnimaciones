# -*- coding: utf-8 -*-
"""Escena 1 · gancho (0:00-0:24): mapa que baja al cañón, la flor de xúchitl que brota, el nombre «lugar de flores nobles» como ecuación,
el valle tranquilo que se oscurece, la multitud que se borra en pétalos y el cierre dividido entre flores y guerra."""
import math

import numpy as np

import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import kz_pers2d as K2
import kz_abstracto as AB
import plano as P
import lugares  # noqa: F401  (registra los lugares del video)
import paisajes as PA
import mundos_a as MA
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01
from reg import shot, snd
from util import *  # noqa: F401,F403

E1 = "gancho"
t_pueblo, t_zac, t_nombre, t_flor = T(E1, "pueblo", frase=0), T(E1, "zacatecas", frase=0), T(E1, "nombre", frase=0), T(E1, "flor", frase=0)
t_llama, t_juch, t_nah, t_quiere = T(E1, "llama", frase=0), T(E1, "juchipila", frase=0), T(E1, "nahuatl", frase=0), T(E1, "quiere", frase=0)
t_lugar, t_flores, t_nobles = T(E1, "lugar", frase=0), T(E1, "flores", frase=0), T(E1, "nobles", frase=0)
t_pero, t_casi, t_quin, t_valle, t_trang = T(E1, "pero", frase=1), T(E1, "casi", frase=1), T(E1, "quinientos", frase=1), T(E1, "valle", frase=1), T(E1, "tranquilo", frase=1)
t_rebel, t_grandes, t_conq = T(E1, "rebeliones", frase=1), T(E1, "grandes", frase=1), T(E1, "conquista", frase=1)
t_guerra, t_borrar, t_pueblo2, t_caxc = T(E1, "guerra", frase=2), T(E1, "borrar", frase=2), T(E1, "pueblo", frase=2), T(E1, "caxcanes", frase=2)
t_hist, t_juch2, t_flores2, t_guerra2 = T(E1, "historia", frase=3), T(E1, "juchipila", frase=3), T(E1, "flores", frase=3), T(E1, "guerra", frase=3)
MP = KM.MAPA
BG0 = np.zeros((H, W, 3), np.float32)
BG_VIOLETA = lambda t: bg_grad((78, 32, 140), (18, 8, 46), mid=(44, 18, 96), ym=0.5)
T_A = T0(E1)
T_B = t_nombre + 0.05          # corte del mapa a la flor
T_D = t_pero - 0.05            # valle tranquilo
T_E = t_rebel - 0.35           # el cielo se vuelve rojo
T_F = t_guerra - 0.1           # multitud
T_G = t_hist - 0.1             # cierre


def acabado(img, t):
    return AB.grano(U.gradacion(img, luces=(1.03, 1.0, 0.95), sombras=(0.96, 0.97, 1.05), contraste=1.05, saturacion=1.08), t)


# ------------------------------------------------------------------------------------------------ A. el mapa baja al cañón
def cam_mapa(t):
    return Klog(t, [(T_A, (-101.3, 22.9, 0.62)), (t_zac, (-102.4, 22.2, 1.4)), (T_B, (-103.12, 21.50, 3.4))])


@shot(T_A, bg=lambda t: MP.base(cam_mapa(t), t, exag=12.0, rios_umbral=0.7), post=[acabado], ent=("fundido", 0.01))
def a_mapa(lz, t):
    cam = cam_mapa(t)
    MD.mar_vivo(lz, cam, t, seed=2)
    MD.montes(lz, cam)
    MD.region(lz, cam, "ZACATECAS", (-102.45, 23.35), px=54, alfa=0.80, z_max=2.6)
    MD.region(lz, cam, "SIERRA MADRE OCCIDENTAL", (-105.6, 24.2), px=26, rot=-1.1, alfa=0.55, z_max=1.2)
    MD.region(lz, cam, "JALISCO", (-103.2, 20.3), px=34, alfa=0.55, z_max=2.2)
    MD.ciudad(lz, cam, "zacatecas", t, t_zac - 0.2, tam=0.8, tipo="ciudad", nombre="Zacatecas", px=26)
    MD.ciudad(lz, cam, "guadalajara", t, t_zac + 0.2, tam=0.8, tipo="ciudad", nombre="Guadalajara", px=26)
    MD.onda(lz, cam, "juchipila", t, t_pueblo + 0.1, dur=2.0, r_deg=1.0, n=3, ancho=5.0, periodo=0.4, alfa=0.9, color=(255, 214, 90))
    MD.ciudad(lz, cam, "juchipila", t, t_pueblo, tam=1.15, tipo="pueblo", semilla=3)
    k = U.pop(t, t_pueblo + 0.15) * U.salida(t, T_B - 0.05, 0.15)
    sx, sy = MP.proy(cam, *MD.CIUDADES["juchipila"])
    if k > 0.01:
        U.llamada(lz, float(sx), float(sy) - 70, "un pueblo", color=U.COL["naranja"], px=40, k=k, cola="abajo")


# ------------------------------------------------------------------------------------------------ B. la flor brota y el nombre
def bg_flor(t):
    return BG_VIOLETA(t)


@shot(T_B, bg=bg_flor, post=[acabado], ent=("zoom", 0.55))
def b_flor(lz, t):
    AB_ = AB
    U.bokeh(lz, t, seed=4, n=16, colores=((255, 150, 44), (236, 70, 140), (122, 90, 255), (255, 214, 90)), alfa=0.45)
    U.chispas(lz, t, n=14, seed=2)
    # la flor brota en el centro y, al decir «Juchipila», se desplaza a la izquierda
    u = prog(t, t_flor - 0.05, t_flor + 1.1)
    m = e_inout(prog(t, t_juch - 0.2, t_juch + 0.8))
    fx, fy, fr = lerp(W / 2, 480, m), lerp(540, 590, m), lerp(300, 235, m)
    MA.flor_xuchitl(lz, fx, fy, fr, t, u=u)
    AB.petalos(lz, t, t_flor + 0.25, (fx, fy), n=18, dur=2.2, spread=(-math.pi, 0.0), seed=3)
    # título con textura de flores
    a = U.pop(t, t_juch) * U.salida(t, T_D - 0.25, 0.2)
    sub = e_inout(prog(t, t_quiere - 0.2, t_quiere + 0.5))
    AB.titulo_textura(lz, "JUCHIPILA", lerp(1330, 1330, sub), lerp(380, 215, sub), 190 if sub < 0.5 else 190, t, k=lerp(1.0, 0.62, sub), alfa=min(1.0, a * 1.5))
    # etimología como ecuación
    k = U.pop(t, t_nah - 0.1) * U.salida(t, T_D - 0.25, 0.2)
    if k > 0.01:
        U.llamada(lz, 1330, lerp(530, 330, sub), "en náhuatl: Xochipillan", color=U.COL["teal"], px=40, k=k, cola=None)
    k1 = U.pop(t, t_flores) * U.salida(t, T_D - 0.25, 0.2)
    if k1 > 0.01:
        MA.flor_xuchitl(lz, 1030, 660, 100 * k1, t, u=1.0, sombra=False)
        U.llamada(lz, 1030, 800, "xóchitl = flor", color=U.COL["naranja"], px=44, k=k1, cola="arriba")
    k2 = U.pop(t, t_nobles) * U.salida(t, T_D - 0.25, 0.2)
    if k2 > 0.01:
        MD.corona(lz, 1500, 690, 3.6 * k2, 1.0, t)
        U.llamada(lz, 1500, 800, "pilli = noble", color=U.COL["magenta"], px=44, k=k2, cola="arriba")
        P.rotulo(lz, 1265, 660, "+", px=120, alfa=min(1.0, k2 * 1.5))
    k3 = U.pop(t, t_nobles + 0.45) * U.salida(t, T_D - 0.25, 0.2)
    if k3 > 0.01:
        U.llamada(lz, 1260, 955, "lugar de flores nobles", color=U.COL["morado"], px=72, k=k3 * U.repop(t, t_nobles + 0.9), cola=None)
    for tt in (t_flor + 0.2, t_juch, t_flores, t_nobles):
        snd(tt, "pop", 0.35)


# ------------------------------------------------------------------------------------------------ D. el valle tranquilo
def amb_t(t):
    return float(smooth(prog(t, T_E, t_grandes + 0.2)))


def paisaje(lz, t, cx, amb, personas=True, entre=None):
    PA.sol(lz, 1380, 300, 70, t, amb)
    PA.sierras(lz, t, cx, amb, y0=640)
    if entre is not None:                    # lo que va entre las sierras y el valle (guerreros en las crestas)
        entre(lz, t)
    PA.rio(lz, t, amb)
    PA.aldea(lz, t, amb)
    PA.pared_canon(lz, t, -1, amb, ancho=430, seed=2)
    PA.pared_canon(lz, t, 1, amb, ancho=430, seed=5)
    PA.aves(lz, t, n=7, seed=3, vel=1.0)
    PA.flores_frente(lz, t, cx, amb=amb)


@shot(T_D, bg=lambda t: PA.cielo(round(amb_t(t), 1)), post=[acabado], ent=("fundido", 0.5))
def d_valle(lz, t):
    cx = 36.0 * (t - T_D)
    amb = amb_t(t)
    paisaje(lz, t, cx, amb)
    # personajes del valle caminando por la orilla (cuerpo completo)
    for i, (tipo, x0, v, y, s_) in enumerate((("caxcana", -200, 1.0, 905, 26), ("caxcan", -520, 0.9, 930, 28), ("anciano_caxcan", -860, 0.7, 915, 25))):
        x = min(x0 + v * 140 * (t - T_D + 3.0) * 0.9, PA.rio_borde(y)[0] - 70)      # caminan por la orilla, nunca dentro del río
        K2.cuerpo(lz, x, y, s_, tipo, t, piernas="camina", brazos="balanceo", mirar=1, vista="perfil", seed=i + 3)
    # cuenta atrás del tiempo: de 2026 a 1541
    c = lerp(2026, 1541, e_inout(prog(t, t_casi - 0.1, t_quin + 0.9)))
    kc = U.pop(t, t_casi - 0.1) * U.salida(t, t_valle - 0.1, 0.25)
    if kc > 0.01:
        AB.contador_atras(lz, W / 2, 230, c, px=190, k=kc)
    kq = U.pop(t, t_quin) * U.salida(t, t_valle - 0.1, 0.25)
    if kq > 0.01:
        U.llamada(lz, W / 2, 360, "casi 500 años", color=U.COL["naranja"], px=44, k=kq, cola="arriba")
    kv = U.pop(t, t_trang) * U.salida(t, T_E, 0.2)
    if kv > 0.01:
        U.llamada(lz, 1500, 470, "un valle tranquilo", color=U.COL["teal"], px=40, k=kv, cola=None)


# ------------------------------------------------------------------------------------------------ E. el cielo se vuelve rojo; guerreros en las crestas
def _guerreros_crestas(lz, t):
    """Siluetas escalonadas sobre las crestas de las sierras: se dibujan DETRÁS del río y del pueblo (nunca de pie sobre los techos)."""
    for i in range(16):
        k = pk(t, t_rebel + 0.05 + 0.085 * i, 0.35)
        if k <= 0.01:
            continue
        x = 140 + 1640 * h01(8, i, 1)
        y = 600 + 26 * h01(8, i, 2) + (i % 3) * 10
        MA.silueta_guerrero(lz, x, y, 13 + 4 * h01(8, i, 3), (36, 12, 44), t, seed=i, alfa=0.95, escala=k)


@shot(T_E, bg=lambda t: PA.cielo(round(amb_t(t), 1)), post=[acabado], ent=("fundido", 0.01))
def e_rojo(lz, t):
    cx = 36.0 * (t - T_D)
    amb = amb_t(t)
    paisaje(lz, t, cx, amb, entre=_guerreros_crestas)
    for i, (tipo, x0, v, y, s_) in enumerate((("caxcana", -200, 1.0, 905, 26), ("caxcan", -520, 0.9, 930, 28), ("anciano_caxcan", -860, 0.7, 915, 25))):
        x = min(x0 + v * 140 * (t - T_D + 3.0) * 0.9, PA.rio_borde(y)[0] - 70)      # caminan por la orilla, nunca dentro del río
        K2.cuerpo(lz, x, y, s_, tipo, t, piernas="idle" if t > t_rebel + 0.4 else "camina", brazos="idle" if t > t_rebel + 0.4 else "balanceo", mirar=1, vista="perfil", seed=i + 3)
    kg = U.pop(t, t_grandes - 0.1) * U.salida(t, t_conq + 1.6, 0.25)
    if kg > 0.01:
        U.llamada(lz, W / 2, 210, "una de las rebeliones más grandes", color=U.COL["rojo"], px=50, k=kg, cola=None)
    kc = U.pop(t, t_conq) * U.salida(t, T_F - 0.1, 0.2)
    if kc > 0.01:
        U.llamada(lz, W / 2, 310, "de la Conquista", color=U.COL["oscuro"], px=50, k=kc, cola=None)
        U.ondas_sonoras(lz, W / 2, 640, t, t_conq, dur=1.4, r1=520, n=2, color=(255, 120, 100), ancho=5.0, periodo=0.35, alfa=0.55)
    snd(t_rebel, "tambor", 0.5)
    snd(t_conq, "gong", 0.6)


# ------------------------------------------------------------------------------------------------ F. un pueblo entero, a punto de borrarse
FIG = [(r, c) for r in range(2) for c in range(8)]


def _pos_fig(i):
    r, c = FIG[i]
    return 290 + 190 * c + 55 * (r % 2) + 12 * h01(9, i, 1), 760 + 210 * r


def borra_u(i):
    """Instante en que la figura i se disuelve (tres sobreviven, repartidas)."""
    if i in (2, 9, 13):
        return 1e9
    return t_borrar + 0.05 + 0.5 * h01(9, i, 2)


@shot(T_F, bg=lambda t: bg_grad((40, 14, 76), (16, 6, 40), mid=(86, 26, 110), ym=0.6), post=[acabado], ent=("tinta", 0.6))
def f_pueblo(lz, t):
    U.bokeh(lz, t, seed=7, n=12, colores=((236, 70, 140), (122, 90, 255), (255, 150, 44)), alfa=0.35)
    lz.relleno(rect_red(0, 930, W, 160, 0), (22, 8, 48), alfa=0.85, capa=0)
    for i in range(len(FIG)):
        x, y = _pos_fig(i)
        te = borra_u(i)
        k = pk(t, t_guerra + 0.02 + 0.02 * i, 0.3)
        if t > te:
            k *= 1 - smooth(prog(t, te, te + 0.22))
        if k <= 0.01:
            continue
        spec = K2.variar("caxcana" if i % 3 == 1 else "caxcan" if i % 3 == 0 else "hombre", i + 11)
        K2.cuerpo(lz, x, y, 30 * k, spec, t, piernas="idle", brazos="idle", mirar=1 if i % 2 else -1, vista="frente", seed=i, cara="ninguna")
    # los pétalos de los que desaparecen
    for i in range(len(FIG)):
        te = borra_u(i)
        if te < 1e8 and t > te:
            x, y = _pos_fig(i)
            AB.petalos(lz, t, te, (x, y - 140), n=7, dur=2.4, spread=(-math.pi * 0.95, -math.pi * 0.05), seed=i + 20, tam=(18, 34), vel=(80, 260))
    # barrido rojo que «borra»
    AB.barrido(lz, t, t_borrar - 0.05, dur=0.8, color=(236, 70, 90), ang=0.2, alfa=0.7)
    kp = U.pop(t, t_guerra + 0.2) * U.salida(t, t_caxc - 0.1, 0.2)
    if kp > 0.01:
        U.llamada(lz, W / 2, 230, "un pueblo entero", color=U.COL["morado"], px=64, k=kp, cola=None)
    # el busto de un caxcán entra al decir «los caxcanes»
    kb = pk(t, t_caxc - 0.1, 0.5)
    if kb > 0.01:
        x_b = lerp(W + 380, 1380, e_out(prog(t, t_caxc - 0.1, t_caxc + 0.6)))
        K2.busto(lz, x_b, 1110, 150 * kb, "caxcan", t, yaw=-0.55, emocion="serio", ojos="abiertos", mano=None)
        U.llamada(lz, x_b, 540, "los caxcanes", color=U.COL["naranja"], px=64, k=kb, cola="abajo")
    snd(t_borrar, "whoosh", 0.45)


# ------------------------------------------------------------------------------------------------ G. flores y guerra
@shot(T_G, bg=lambda t: BG0, post=[acabado, lambda img, t: post_fundido_negro(img, t, T1(E1) - 0.9, T1(E1) - 0.05)], ent=("destello", 0.7))
def g_cierre(lz, t):
    xm = W / 2
    izq = [(0, 0), (xm + 60, 0), (xm - 60, H), (0, H)]
    der = [(xm + 60, 0), (W, 0), (W, H), (xm - 60, H)]
    c_amb = lerp(0.0, 1.0, 0.0)
    with lz.recorte(izq):
        lz.degradado(izq, (255, 190, 110), (250, 110, 120), (0, 0), (0, H), capa=0)
        U.bokeh(lz, t, seed=9, n=10, colores=((255, 214, 90), (255, 150, 44), (236, 110, 150)), alfa=0.4, area=(0, 0, xm, H))
        kf = pk(t, t_flores2 - 0.2, 0.6)
        MA.flor_xuchitl(lz, 470, 600, 290 * kf, t, u=max(0.0, min(1.0, kf)), seed=2)
        AB.petalos(lz, t, t_flores2 - 0.1, (470, 600), n=16, dur=2.4, spread=(-math.pi, 0.0), seed=5)
    with lz.recorte(der):
        lz.degradado(der, (24, 8, 46), (150, 30, 70), (0, 0), (0, H), capa=0)
        PA.sierras(lz, t, 0.0, 1.0, y0=760, capas=3)
        kg = pk(t, t_guerra2 - 0.2, 0.5)
        for i in range(9):
            if kg <= 0.01:
                break
            MA.silueta_guerrero(lz, 1100 + 95 * i, 800 + 22 * (i % 3), 20, (30, 10, 40), t, seed=i, escala=kg)
    # muesca de flecha en el corte
    lz.relleno(np.array([[xm - 60, H], [xm + 60, 0], [xm + 78, 0], [xm - 42, H]]), (255, 255, 255), alfa=0.55, capa=2)
    # título y rótulos
    ka = U.pop(t, t_juch2 - 0.1)
    AB.titulo_textura(lz, "JUCHIPILA", W / 2, 150, 170, t, k=0.7, alfa=min(1.0, ka * 1.5))
    k1 = U.pop(t, t_flores2)
    if k1 > 0.01:
        U.llamada(lz, 470, 960, "las flores", color=U.COL["naranja"], px=64, k=k1, cola=None)
    k2 = U.pop(t, t_guerra2)
    if k2 > 0.01:
        U.llamada(lz, 1450, 960, "la guerra", color=U.COL["rojo"], px=64, k=k2, cola=None)
