# -*- coding: utf-8 -*-
"""Escena 9 · La captura (4:56-5:32): la huida al norte, la emboscada en el desierto, los prisioneros a Chihuahua, el final de los jefes (sin mostrar el momento), Hidalgo degradado y las cabezas en la Alhóndiga."""
import datetime
import math

import numpy as np

import kz_iso as I
from kz_iso import tint
import kz_iso_obj as O
import kz_iso_obj2 as O2
import kz_iso_arq as A
import kz_iso_arq2 as B
import kz_iso_int as N
import kz_gente_iso as G
import kz_iso_deco as DC
import kz_retrato as RT
import kz_ui as U
import kz_mapa as KM
import kz_mapa_dib as MD
import plano as P
from motor import W, H, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, elipse, rect_red, h01, catmull
from reg import shot, snd
from util import *  # noqa: F401,F403
import mundos_g as mg
import mundos_j as mj

E9 = "captura"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
GRIS = lambda img, t: U.gradacion(img, luces=(1.0, 0.98, 0.98), sombras=(0.94, 0.95, 1.02), saturacion=0.72)
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
DES = mj.Desierto()
GTO = mg.GuanajuatoCiudad()

# ------------------------------------------------------------------ anclas
t_jefes, t_insu, t_huy, t_hacia, t_norte, t_esp, t_lleg, t_eeuu = [T(E9, w, frase=0) for w in ("jefes", "insurgentes", "huyeron", "hacia", "norte", "esperanza", "llegar", "estados")]
t_pero, t_marzo, t_trai, t_espero, t_cam, t_des, t_fuer, t_capt = [T(E9, w, frase=1) for w in ("pero", "marzo", "traidor", "espero", "camino", "desierto", "fueron", "capturados")]
t_llev, t_enc, t_chi, t_alle, t_alda, t_jime, t_fus, t_jun = [T(E9, w, frase=2) for w in ("llevaron", "encadenados", "chihuahua", "allende", "aldama", "jimenez", "fusilados", "junio")]
t_hid3, t_sac, t_prim, t_degr, t_fus2, t_trein, t_jul, t_once = [T(E9, w, frase=3) for w in ("hidalgo", "sacerdote", "primero", "degradaron", "fusilaron", "treinta", "julio", "once")]
t_cab, t_colg, t_esq, t_alh, t_gdit, t_gua = [T(E9, w, frase=4) for w in ("cabezas", "colgadas", "esquinas", "alhondiga", "granaditas", "guanajuato")]
t_ahi, t_perm, t_diez, t_anos, t_adv, t_pero2, t_rev, t_muer = [T(E9, w, frase=5) for w in ("ahi", "permanecieron", "diez", "anos", "advertencia", "pero", "revolucion", "muerto")]
T_A, T_B, T_C, T_C2, T_D, T_D2, T_E, T_F = T0(E9), t_pero - 0.2, t_llev - 0.15, t_alle - 0.2, t_hid3 - 0.2, t_fus2 - 0.55, t_cab - 0.2, t_ahi - 0.2


# ------------------------------------------------------------------------------------------------ 1. HUIDA AL NORTE (mapa)
RUTA_N = [(-102.8, 20.6), (-102.57, 22.77), (-101.0, 25.42), (-101.1, 26.9)]
RUTA_N2 = [(-101.1, 26.9), (-100.5, 28.7)]


def cam_n(t):
    return Klog(t, [(T_A, (-102.0, 22.6, 1.3)), (t_hacia, (-101.7, 24.6, 1.3)), (T_B, (-101.4, 26.0, 1.5))])


@shot(T_A, bg=lambda t: BASE(cam_n(t), t), post=[GRAD], ent=("fundido", 0.5))
def cp_huida(lz, t):
    cam = cam_n(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.pais(lz, cam, "United States of America", (90, 130, 230), alfa=0.16, borde=(120, 160, 255), ancho=4.0)
    for j, (lug, tp, nm, dx, dy, lado) in enumerate((("guadalajara", "ciudad", "", 0, 0, "izq"), ("zacatecas", "ciudad", "Zacatecas", 130, 4, "izq"), ((-101.0, 25.42), "ciudad", "Saltillo", 120, 4, "izq"), ("acatita", "pueblo", "Acatita de Baján", 160, 4, "izq"))):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1 * j, tam=1.3, tipo=tp, bando="ins", semilla=j + 61)
        if nm:
            MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    f = e_inout(prog(t, T_A + 0.2, T_B - 0.2))
    MD.ruta(lz, cam, RUTA_N, color=(255, 214, 84), frac=f, t=t, ancho=8.0, flecha=True)
    MD.ruta(lz, cam, RUTA_N2, color=(255, 255, 255), frac=prog(t, t_lleg, T_B), t=t, ancho=7.0, flecha=True)
    for i in range(7):
        u = max(0.0, min(0.999, f - 0.045 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_N, u)
            MD.ejercito(lz, float(x), float(y), 12, bando="ins", t=t + i * 0.2, s=1.6, dir=1, semilla=i, bandera=(i == 0), polvo=(i % 2 == 0))
    k = U.pop(t, t_jefes - 0.05) * U.salida(t, t_huy - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los jefes insurgentes", color=U.COL["naranja"], px=74, k=k, cola=None)
    k = U.pop(t, t_huy - 0.05) * U.salida(t, t_esp - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "huyen hacia el norte", color=U.COL["azul"], px=80, k=k * U.repop(t, t_norte + 0.1), cola=None)
    k = U.pop(t, t_esp - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "con la esperanza de llegar a Estados Unidos", color=U.COL["verde"], px=58, k=k * U.repop(t, t_eeuu + 0.1), cola=None)
        sx, sy = MP.proy(cam, -100.5, 28.7)
        U.llamada(lz, float(sx), float(sy) + 170, "Estados Unidos", color=(90, 130, 230), px=40, k=k, cola="arriba")
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. LA EMBOSCADA EN EL DESIERTO
def cam_b(t):
    return K(t, [(T_B, (-10, 275, 30, 2.3)), (t_trai, (140, 245, 34, 2.7)), (t_des, (225, 210, 36, 3.0)), (t_fuer, (255, 195, 36, 3.3)), (T_C, (258, 192, 36, 3.4))])


CIRCULO_C = (258.0, 196.0)


def _emboscada(m, t):
    # caravana: jinetes (Hidalgo, Allende, Aldama, Jiménez), carretas con familias y tropa a pie
    base = 150 + (t - T_B) * 16.0
    hasta = 262.0
    s_stop = 340.0
    s = min(base, s_stop)
    mov = base < s_stop
    for k, (tp, off, sd) in enumerate((("cura", 0, 1), ("oficial", -26, 2), ("dragon", -52, 3), ("oficial", -78, 4))):
        x, y, d = mj.pos_camino_d(s + off)
        m.add(x - 8, y - 8, x + 8, y + 8, 50, (lambda x, y, d, tp, sd: (lambda lz, iso: G.caballo(lz, iso, x, y, t, dir=1, seed=sd, vel=1.0 if mov else 0.0, jinete=tp, s=1.3)))(x, y, d, tp, sd), fijo=False, clave=x + y + 10)
    for k in range(3):
        x, y, d = mj.pos_camino_d(s - 110 - 46 * k)
        m.add(x - 12, y - 8, x + 12, y + 8, 30, (lambda x, y, k: (lambda lz, iso: O.carreta(lz, iso, x, y, t, mov=1.0 if mov else 0.0, carga=(214, 180, 96), s=1.2, bultos=True)))(x, y, k), fijo=False, clave=x + y + 4)
    for i in range(16):
        x, y, d = mj.pos_camino_d(s - 30 - 14 * (i // 2) - 90 * (i % 2 == 1) * 0)
        ox, oy = 12 * ((i % 2) - 0.5), 12 * (((i * 7) % 3) - 1)
        m.add(x + ox - 4, y + oy - 4, x + ox + 4, y + oy + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("insurgente", "insurgente_lanza", "campesino", "indigena")[i % 4], dir=(1, -0.3), vel=1.3 if mov else 0.0, seed=9000 + i, h=42, cara="miedo" if not mov else None)))(x + ox, y + oy, i), fijo=False, clave=x + y + 5)
    # el traidor: un oficial a caballo con un pañuelo blanco, esperando junto a las rocas; los emboscados agazapados
    tx, ty = 330.0, 170.0
    m.add(tx - 8, ty - 8, tx + 8, ty + 8, 50, lambda lz, iso: G.caballo(lz, iso, tx, ty, t, dir=-1, seed=9, vel=0.0, jinete="oficial", s=1.3), fijo=False, clave=tx + ty + 10)
    surge = e_out(prog(t, t_fuer - 0.2, t_capt + 0.4))
    for i, (rx, ry) in enumerate(mj.ROCAS_D):
        for j in range(3):
            x0, y0 = rx + 14 * (j - 1), ry + 12 + 4 * j
            a = 2 * math.pi * (i * 3 + j) / 24
            x1, y1 = CIRCULO_C[0] + 70 * math.cos(a), CIRCULO_C[1] + 46 * math.sin(a)
            x, y = lerp(x0, x1, surge), lerp(y0, y1, surge)
            h = lerp(26.0, 46.0, surge)
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, h, i, j, sg: (lambda lz, iso: G.persona(lz, iso, x, y, t, "realista", dir=(CIRCULO_C[0] - x, CIRCULO_C[1] - y) if sg > 0 else (0, 1), vel=1.8 if 0 < sg < 1 else 0.0, seed=9100 + i * 3 + j, h=h, cara="enojo", accion="pelea" if sg >= 1 and j == 0 else None)))(x, y, h, i, j, surge), fijo=False, clave=x + y + 3)


@shot(T_B, bg=lambda t: bg_grad((250, 190, 120), (254, 232, 190), mid=(246, 150, 130), ym=0.5), post=[GRAD], ent=("fundido", 0.5))
def cp_emboscada(lz, t):
    cx, cy, cz, zm = cam_b(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(1.06, 0.98, 0.90), mix=(255, 170, 100), k=0.12)
    DES.suelo(lz, iso, t)
    m = DES.objetos(t)
    _emboscada(m, t)
    m.dibujar(lz, iso)
    DC.aves(lz, t, n=6, seed=81, y0=60, y1=200, color=(60, 40, 60))
    DC.polvo_luz(lz, t, n=24, seed=82, color=(240, 214, 160), alfa=0.45)
    k = U.pop(t, t_pero - 0.05) * U.salida(t, t_trai - 0.15, 0.2)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_B + 0.1, t_des, "Acatita de Baján, Coahuila", "21 de marzo de 1811", y=70)
    k = U.pop(t, t_trai - 0.05) * U.salida(t, t_des - 0.1, 0.2)
    if k > 0.01:
        qx, qy = iso.P(330, 170, 66)
        U.llamada(lz, float(qx), float(qy) - 10, "un traidor", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_trai + 0.3), cola="abajo")
    k = U.pop(t, t_des - 0.05) * U.salida(t, t_fuer - 0.1, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los espera en el desierto", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_fuer - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "¡capturados!", color=U.COL["rojo"], px=100, k=k * U.repop(t, t_capt + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. ENCADENADOS A CHIHUAHUA (mapa)
RUTA_CH = [(-101.1, 26.9), (-102.5, 27.3), (-104.0, 28.0), (-106.09, 28.63)]


def cam_c(t):
    return Klog(t, [(T_C, (-103.2, 27.4, 1.7)), (t_chi, (-104.0, 27.9, 1.9)), (T_C2, (-104.8, 28.2, 2.2))])


@shot(T_C, bg=lambda t: BASE(cam_c(t), t), post=[GRAD], ent=("zoom", 0.5))
def cp_chihuahua(lz, t):
    cam = cam_c(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.10, borde=(255, 220, 90), ancho=4.0, t=t, latido=1.0)
    MD.pais(lz, cam, "United States of America", (90, 130, 230), alfa=0.14, borde=(120, 160, 255), ancho=4.0)
    MD.ciudad(lz, cam, "acatita", t, T_C, tam=1.4, tipo="pueblo", bando="real", semilla=3)
    MD.etiqueta(lz, cam, "acatita", "Acatita de Baján", t, T_C + 0.1, px=22, dy=4, dx=150, lado="izq")
    MD.ciudad(lz, cam, "chihuahua", t, t_enc, tam=2.4, tipo="ciudad", bando="real", semilla=9)
    f = e_inout(prog(t, T_C + 0.2, T_C2 - 0.2))
    MD.ruta(lz, cam, RUTA_CH, color=(220, 220, 236), frac=f, t=t, ancho=7.0, flecha=False)
    for i in range(6):
        u = max(0.0, min(0.999, f - 0.06 * i))
        if u > 0.01:
            x, y, v = MD.punto_ruta(cam, RUTA_CH, u)
            MD.ejercito(lz, float(x), float(y), 8, bando=(200, 200, 216) if i else (60, 60, 80), t=t + i * 0.2, s=1.5, dir=-1, semilla=i, bandera=False, polvo=(i % 2 == 0))
            if i < 5:                                         # cadena entre los prisioneros
                x2, y2, v2 = MD.punto_ruta(cam, RUTA_CH, max(0.0, min(0.999, f - 0.06 * (i + 1))))
                lz.trazo(np.array([[float(x), float(y) - 10], [float(x2), float(y2) - 10]]), (90, 90, 110), 4, afinar=False, temblor=0.0, capa=2)
    k = U.pop(t, t_llev - 0.05) * U.salida(t, t_chi - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los llevan encadenados", color=U.COL["rojo"], px=76, k=k * U.repop(t, t_enc + 0.1), cola=None)
    k = U.pop(t, t_chi - 0.05)
    if k > 0.01:
        sx, sy = MP.proy(cam, -106.09, 28.63)
        U.llamada(lz, float(sx), float(sy) - 120, "Chihuahua", color=U.COL["morado"], px=72, k=k * U.repop(t, t_chi + 0.3), cola="abajo")
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 4. ALLENDE, ALDAMA Y JIMÉNEZ (sobrio)
def _fusileros(lz, t, y, k):
    """Fila de soldados de espaldas con fusiles en alto (siluetas), sin mostrar a los fusilados."""
    for i in range(9):
        x = 360 + 150 * i
        s = 1.7
        lz.relleno(rect_red(x - 14 * s, y - 40 * s, 28 * s, 44 * s, 6), (44, 52, 100), capa=2)
        lz.relleno(circulo(x, y - 52 * s, 12 * s, 14), (200, 160, 130), capa=2)
        lz.relleno(rect_red(x - 12 * s, y - 80 * s, 24 * s, 24 * s, 4), (30, 30, 50), capa=2)
        lz.trazo(np.array([[x + 18 * s, y - 14 * s], [x + 60 * s, y - 96 * s * k - 8 * s * (1 - k)]]), (60, 50, 50), 5 * s, afinar=False, temblor=0.0, capa=2)


@shot(T_C2, bg=lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55), post=[GRIS], ent=("fundido", 0.6))
def cp_jefes(lz, t):
    U.haces_luz(lz, W / 2, 380, t, n=7, largo=1300, color=(220, 200, 255), alfa=0.08, ancho=0.09)
    nom = (("allende", "Ignacio Allende", t_alle, 360, U.COL["azul"]), ("aldama", "Juan Aldama", t_alda, 960, U.COL["naranja"]), ("jimenez", "Mariano Jiménez", t_jime, 1560, U.COL["morado"]))
    fus = e_out(prog(t, t_fus, t_fus + 0.6))
    for (q, lab, tt_, x, col) in nom:
        k = U.pop(t, tt_ - 0.05, 1.2)
        if k > 0.01:
            RT.retrato(lz, x, 720, 150 * (0.94 + 0.06 * k), q, t, emocion="serio", habla=0.0, mirar=0.0, seed=3, alfa=min(1.0, k) * (1 - 0.55 * fus), luz_borde=(220, 200, 255))
            U.llamada(lz, x, 110, lab, color=col, px=46, k=k, cola=None)
            if fus > 0.01:                                       # crespón negro
                lz.relleno(np.array([[x - 160, 560], [x - 120, 540], [x + 160, 760], [x + 120, 790]]), (14, 12, 22), alfa=0.85 * fus, capa=2)
    t_v = t_fus + 0.35
    kv = U.pop(t, t_fus - 0.3, 1.2) * U.salida(t, T_D - 0.2, 0.3)
    if kv > 0.01:
        _fusileros(lz, t, 1040, 1.0 if t > t_fus + 0.1 else 0.0)
        if t_v - 0.05 < t < t_v + 0.6:
            for i in range(9):
                u = (t - t_v) / 0.6
                lz.halo(360 + 150 * i + 90, 760 - 40 * u, 60 + 40 * u, (255, 220, 150), alfa=0.5 * (1 - u), capa=2)
    k = U.pop(t, t_fus - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 920, "fusilados en junio de 1811", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_jun + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 5. HIDALGO: DEGRADADO Y FUSILADO
def _altar(lz, iso, t):
    I.caja(lz, iso, 150, 8, 100, 26, 24, (206, 202, 214))
    I.caja(lz, iso, 152, 10, 96, 22, 3, (252, 250, 255), z0=24)
    B.candelabro(lz, iso, 170, 22, 27, t, n=3)
    B.candelabro(lz, iso, 232, 22, 27, t + 0.6, n=3)
    I.caja(lz, iso, 198, 18, 4, 4, 30, (240, 214, 120), z0=27)
    I.caja(lz, iso, 190, 18, 20, 4, 4, (240, 214, 120), z0=48)
    sx, sy = iso.P(200, 20, 50)
    lz.halo(float(sx), float(sy), 90 * iso.z / 3.0, (255, 220, 150), alfa=0.30, capa=2)


def _sacristia(lz, iso, t):
    c = I.habitacion(lz, iso, 0, 0, 280, 230, 140, piso=(150, 142, 150), pared_a=(206, 198, 206), pared_b=(190, 182, 194), friso=(100, 92, 106))
    N.ventana_vista(lz, iso, c, "yi", 100, 176, 40, 120, t=t, cielo=(120, 140, 200), marco=(200, 192, 200), cortinas=(80, 70, 110), vista="cielo")
    I.cara_rect(lz, iso, c, "xi", 40, 46, 60, 112, (84, 70, 70))
    I.cara_rect(lz, iso, c, "xi", 30, 56, 94, 100, (84, 70, 70))
    I.cara_arco(lz, iso, c, "xi", 150, 204, 0, 98, (84, 66, 62))
    return c


@shot(T_D, bg=lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55), post=[GRIS], ent=("fundido", 0.6))
def cp_degradacion(lz, t):
    I.luz(mul=(0.92, 0.92, 1.0), mix=(60, 50, 100), k=0.12)
    iso = I.Iso(140, 118, 44, 4.2 + 0.05 * (t - T_D), sx0=930, sy0=650)
    _sacristia(lz, iso, t)
    m = I.Mundo()
    m.add(150, 8, 250, 34, 60, lambda lz, iso: _altar(lz, iso, t), clave=170)
    for (x, y) in ((40, 90), (40, 130), (210, 190), (60, 200)):
        m.add(x, y, x + 10, y + 10, 12, (lambda x, y: (lambda lz, iso: B.silla(lz, iso, x, y, 12, (84, 70, 76))))(x, y), clave=x + y + 2)
    deg = t > t_degr
    m.add(120, 100, 140, 120, 50, lambda lz, iso: G.persona(lz, iso, 130, 112, t, "campesino" if deg else "cura", dir=(0, 1), seed=9200, h=60, cara="triste" if deg else "serio"), fijo=False, clave=250)
    for i, (x, y) in enumerate(((90, 100), (170, 100), (80, 150), (180, 150))):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, "cura" if i < 2 else "noble", dir=(1 if x < 130 else -1, 0.3), seed=9210 + i, h=54, accion="habla" if t_prim < t < t_degr + 1.0 and i % 2 == 0 else None, cara="serio")))(x, y, i), fijo=False, clave=x + y + 4)
    m.dibujar(lz, iso)
    if deg:                                                   # la ropa clerical sale volando (cuello y estola)
        u = prog(t, t_degr, t_degr + 1.2)
        qx, qy = iso.P(130, 112, 56)
        lz.relleno(rect_red(float(qx) - 20 + 200 * u, float(qy) - 40 - 220 * u, 40, 14, 4), (240, 240, 244), alfa=1 - u, capa=2)
        lz.relleno(rect_red(float(qx) - 30 - 180 * u, float(qy) - 20 - 260 * u, 60, 20, 6), (36, 32, 48), alfa=1 - u, capa=2)
    U.fecha_lugar(lz, t, T_D, T_D2 - 0.3, "Chihuahua", "Julio de 1811", y=70)
    k = U.pop(t, t_sac - 0.05) * U.salida(t, t_prim - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "por ser sacerdote…", color=U.COL["morado"], px=76, k=k, cola=None)
    k = U.pop(t, t_prim - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "primero lo degradaron", color=U.COL["rojo"], px=80, k=k * U.repop(t, t_degr + 0.1), cola=None)


@shot(T_D2, bg=lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55), post=[GRIS], ent=("fundido", 0.5))
def cp_patio(lz, t):
    I.luz(mul=(0.92, 0.92, 1.0), mix=(60, 50, 100), k=0.14)
    iso = I.Iso(150, 110, 40, 3.7, sx0=960, sy0=640)
    mj.patio_ejecucion(lz, iso, t)
    m = mj.objetos_patio(t)
    for i in range(16):                                         # testigos de pie, en silencio, a los lados
        x = (-10 + 20 * i) if i < 8 else (250 + 14 * (i - 8))
        y = 230 + 10 * (i % 3) - 60 * (i >= 8)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ('campesino', 'campesina', 'regidor', 'dama', 'indigena', 'indigena_f', 'mestizo', 'nino')[i % 8], dir=(1 if x < 150 else -1, -0.4), seed=9400 + i, h=44 if i % 8 != 7 else 30, cara='triste')))(x, y, i), fijo=False, clave=x + y + 3)
    m.add(146, 36, 156, 46, 60, lambda lz, iso: G.persona(lz, iso, 150, 42, t, "campesino", dir=(0, 1), seed=9300, h=60, cara="serio") if t < t_fus2 + 0.45 else None, fijo=False, clave=160)
    for i in range(7):
        x = 90 + 18 * i
        m.add(x - 4, 190, x + 4, 198, 50, (lambda x, i: (lambda lz, iso: G.persona(lz, iso, x, 194, t, "granadero", dir=(0, -1), seed=9310 + i, h=56, cara="serio", accion=None)))(x, i), fijo=False, clave=x + 194)
    m.dibujar(lz, iso)
    if t_fus2 + 0.35 < t < t_fus2 + 1.2:                      # destello local de la descarga (sin mostrar el momento)
        u = (t - t_fus2 - 0.35) / 0.85
        qx, qy = iso.P(150, 150, 50)
        lz.halo(float(qx), float(qy), 200 + 140 * u, (255, 230, 170), alfa=0.5 * (1 - u), capa=2)
    if t > t_fus2 + 0.6:                                      # una paloma sube donde estaba
        u = prog(t, t_fus2 + 0.6, t_fus2 + 3.0)
        qx, qy = iso.P(150, 42, 60)
        x, y = float(qx) + 120 * u, float(qy) - 40 - 380 * u
        al = math.sin(t * 10) * 12
        lz.relleno(np.array([[x - 40, y - al], [x, y + 4], [x + 40, y - al], [x, y - 6]]), (250, 250, 255), alfa=1 - 0.5 * u, capa=2)
    k = U.pop(t, t_fus2 - 0.05, 1.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 190, "30 de julio de 1811", px=int(104 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    k = U.pop(t, t_trein - 0.05) * U.salida(t, T_E - 0.3, 0.3)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "Miguel Hidalgo es fusilado", color=U.COL["rojo"], px=60, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 6. LAS CABEZAS EN LA ALHÓNDIGA (sobrio)
def _jaula(lz, iso, x, y, z, t, lado=1):
    sx, sy = iso.P(x, y, z)
    sx, sy = float(sx), float(sy)
    k = iso.z * 1.6
    sw = math.sin(t * 1.3 + x) * 2 * k
    lz.trazo(np.array([[sx - lado * 14 * k, sy], [sx, sy + 16 * k]]), (50, 46, 60), 2.4 * k, afinar=False, temblor=0.0, capa=2)
    lz.trazo(np.array([[sx, sy + 16 * k], [sx + sw, sy + 40 * k]]), (110, 106, 120), 1.6 * k, afinar=False, temblor=0.0, capa=2)
    cx_, cy_ = sx + sw, sy + 40 * k
    lz.relleno(rect_red(cx_ - 9 * k, cy_, 18 * k, 26 * k, 5 * k), (46, 44, 58), capa=2)
    lz.relleno(rect_red(cx_ - 9 * k, cy_ - 1 * k, 18 * k, 3 * k, 1 * k), (90, 88, 102), capa=2)
    for j in range(5):
        lz.trazo(np.array([[cx_ - 7 * k + 3.5 * k * j, cy_ + 2 * k], [cx_ - 7 * k + 3.5 * k * j, cy_ + 24 * k]]), (126, 122, 138), 1.2 * k, afinar=False, temblor=0.0, capa=2)


def cam_e(t):
    return K(t, [(T_E, (315, 60, 56, 2.3)), (t_colg, (315, 60, 60, 2.8)), (t_alh, (315, 70, 56, 2.6)), (T_F, (315, 90, 50, 2.4))])


@shot(T_E, bg=lambda t: bg_grad((70, 60, 110), (170, 120, 130), mid=(110, 84, 120), ym=0.5), post=[GRIS], ent=("fundido", 0.6))
def cp_cabezas(lz, t):
    cx, cy, cz, zm = cam_e(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.9, 0.9, 1.0), mix=(60, 50, 100), k=0.16)
    mg.cerros(lz, cx, cy, t, tonos=((100, 100, 130), (84, 84, 116), (70, 70, 102)))
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t, gente=0.0)
    m.dibujar(lz, iso)
    for k_, (jx, jy) in enumerate(((236, 118), (396, 118), (236, -2), (396, -2))):
        kk = U.pop(t, t_colg - 0.2 + 0.18 * k_)
        if kk > 0.01:
            qx, qy = iso.P(jx, jy, 84)
            with lz.grupo(float(qx) * 0, 0, 1.0):
                _jaula(lz, iso, jx, jy, 84, t, 1 if k_ % 2 == 0 else -1)
    DC.aves(lz, t, n=6, seed=83, y0=60, y1=220, color=(50, 44, 64))
    for k_, (q, lab, x) in enumerate((("hidalgo", "Hidalgo", 300), ("allende", "Allende", 800), ("aldama", "Aldama", 1300), ("jimenez", "Jiménez", 1700))):
        kk = U.pop(t, t_cab + 0.25 * k_, 1.2) * U.salida(t, T_F - 0.1, 0.25)
        if kk > 0.01:
            MD.medallon(lz, x, 880, 86, q, t, emocion="serio", k=kk, seed=k_ + 2, fondo=(40, 34, 70), borde=(190, 186, 210))
    k = U.pop(t, t_cab - 0.05) * U.salida(t, t_alh - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "sus cabezas, colgadas", color=U.COL["rojo"], px=78, k=k * U.repop(t, t_colg + 0.1), cola=None)
    k = U.pop(t, t_alh - 0.05)
    if k > 0.01:
        qx, qy = iso.P(315, 60, 110)
        U.llamada(lz, float(qx), float(qy) - 30, "Alhóndiga de Granaditas", color=U.COL["morado"], px=58, k=k * U.repop(t, t_gua + 0.1), cola="abajo")


# ------------------------------------------------------------------------------------------------ 7. DIEZ AÑOS DESPUÉS: LA SEMILLA
def cam_f(t):
    return K(t, [(T_F, (315, 110, 50, 2.5)), (t_adv, (315, 130, 50, 2.2)), (t_pero2, (315, 150, 50, 2.4)), (T1(E9), (315, 160, 50, 2.6))])


def _cielo_tiempo(t):
    u = prog(t, t_perm, t_pero2 - 0.2)
    a = math.sin(u * 20.0) * 0.5 + 0.5                         # días y noches que pasan rápido
    if u <= 0 or u >= 1:
        a = 0.5 if u <= 0 else 0.75
    c = lambda x0, x1: int(x0 + (x1 - x0) * a)
    return bg_grad((c(30, 130), c(30, 190), c(80, 240)), (c(110, 254), c(80, 232), c(130, 200)), mid=None)


@shot(T_F, bg=_cielo_tiempo, post=[GRIS], ent=("fundido", 0.5))
def cp_semilla(lz, t):
    cx, cy, cz, zm = cam_f(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    verde = smooth(prog(t, t_pero2, t_rev + 0.8))
    I.luz(mul=(0.90 + 0.12 * verde, 0.90 + 0.12 * verde, 1.0), mix=(60, 50, 100), k=0.14 * (1 - verde))
    mg.cerros(lz, cx, cy, t, tonos=((100, 100, 130), (84, 84, 116), (70, 70, 102)))
    GTO.suelo(lz, iso, t)
    m = GTO.objetos(t, gente=0.0)
    m.dibujar(lz, iso)
    for (jx, jy) in ((236, 118), (396, 118), (236, -2), (396, -2)):
        _jaula(lz, iso, jx, jy, 84, t, 1)
    # los años pasan: calendario que cuenta de 1811 a 1821
    uy = prog(t, t_perm, t_pero2 - 0.2)
    if 0 < uy < 1 or t > t_perm:
        anio = int(1811 + 10 * min(1.0, uy))
        k = U.pop(t, t_perm - 0.05) * U.salida(t, t_pero2 - 0.1, 0.25)
        if k > 0.01:
            P.rotulo(lz, W / 2, 190, str(anio), px=190, k=k, color=(255, 255, 255))
            U.llamada(lz, W / 2, 330, "diez años", color=U.COL["naranja"], px=64, k=k * U.repop(t, t_diez + 0.2), cola=None)
    k = U.pop(t, t_adv - 0.05) * U.salida(t, t_pero2 - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "como una advertencia", color=U.COL["rojo"], px=62, k=k, cola=None)
    # y entre las lajas de la plaza brota una planta con una flor roja: la revolución no ha muerto
    if verde > 0.01:
        O2.brote(lz, iso, 315, 170, u=verde, t=t, enojo=False, s=1.6)
        qx, qy = iso.P(315, 170, 30)
        lz.halo(float(qx), float(qy), 260 * verde, (150, 255, 160), alfa=0.30 * verde, capa=2)
        for i in range(8):
            U.chispa4(lz, float(qx) + 200 * math.cos(i * 0.8 + t), float(qy) - 60 + 120 * math.sin(i * 0.8 + t), 10 + 6 * (i % 3), color=(200, 255, 200), alfa=0.9 * verde)
    k = U.pop(t, t_pero2 - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "pero la revolución no había muerto", color=U.COL["verde"], px=70, k=k * U.repop(t, t_rev + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_huy, "galope", 0.4, dur=2.0)
snd(t_esp, "pluck", 0.4)
snd(T_B, "amanecer", 0.2, dur=1.6)
snd(t_trai, "gong", 0.5)
snd(t_fuer - 0.2, "tambor", 0.5)
snd(t_capt, "pop", 0.5)
snd(T_C, "whoosh", 0.3, dur=0.9)
snd(t_enc, "crujido", 0.4)
snd(t_chi, "pop", 0.4)
snd(T_C2, "gong", 0.4)
snd(t_fus + 0.35, "canonazo", 0.4)
snd(T_D, "gong", 0.4)
snd(t_degr, "crujido", 0.5)
snd(T_D2, "pluck", 0.4)
snd(t_fus2 + 0.35, "canonazo", 0.5)
snd(T_E, "gong", 0.4)
snd(t_alh, "pop", 0.4)
snd(T_F, "whoosh", 0.3, dur=1.0)
snd(t_pero2, "amanecer", 0.4, dur=2.0)
snd(t_rev, "bling", 0.5)
