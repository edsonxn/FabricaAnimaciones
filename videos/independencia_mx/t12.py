# -*- coding: utf-8 -*-
"""Escena 12 · La caída de Morelos (6:49-7:24): el cerco realista, el círculo de Morelos que cae, el Congreso que huye, la captura, el juicio y el final de Morelos (sobrio, sin mostrar el momento) y las luces de la insurgencia que se apagan."""
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
import mundos_f as mf
import mundos_j as mj
import t09 as T9
import t10 as T10

E12 = "fusilamiento"
MP = KM.MAPA
GRAD = lambda img, t: U.gradacion(img)
GRIS = T9.GRIS
BASE = lambda cam, t: MP.base(cam, t, exag=13.0, rios_umbral=0.7)
PURPG = lambda t: bg_grad((40, 34, 70), (96, 70, 100), mid=(64, 50, 84), ym=0.55)
MARCHA = mf.CaminoMarcha()

# ------------------------------------------------------------------ anclas
t_pero, t_ejer, t_real, t_camb, t_estr, t_vir, t_call, t_mismo, t_venc, t_hid, t_pers, t_desc = [T(E12, w, frase=0) for w in ("pero", "ejercito", "realista", "cambio", "estrategia", "virrey", "calleja", "mismo", "vencido", "hidalgo", "persiguio", "descanso")]
t_uno, t_cay, t_circ, t_mor, t_mat, t_capt, t_fus, t_gal, t_murio, t_comb = [T(E12, w, frase=1) for w in ("uno", "cayendo", "circulo", "morelos", "matamoros", "capturado", "fusilado", "galeana", "murio", "combate")]
t_cong, t_huir, t_pueblo, t_carg, t_pap, t_mor2, t_ofrec, t_prot = [T(E12, w, frase=2) for w in ("congreso", "huir", "pueblo", "cargando", "papeles", "morelos", "ofrecio", "proteger")]
t_nov, t_cayo, t_pris, t_juz, t_degr, t_fusi, t_dic = [T(E12, w, frase=3) for w in ("noviembre", "cayo", "prisionero", "juzgaron", "degradaron", "fusilaron", "diciembre")]
t_con, t_par, t_insu, t_term = [T(E12, w, frase=4) for w in ("con", "parecia", "insurgencia", "terminado")]
T_A, T_B, T_C, T_D1, T_D2, T_D3, T_E = T0(E12), t_uno - 0.2, t_cong - 0.2, t_nov - 0.2, t_juz - 0.15, t_fusi - 0.55, t_con - 0.1


# ------------------------------------------------------------------------------------------------ 1. EL CERCO REALISTA SE CIERRA (mapa)
def cam_a(t):
    return Klog(t, [(T_A, (-98.9, 18.4, 1.7)), (T_B, (-98.9, 18.2, 1.9))])


def _flecha(lz, a, b, ancho, color, frac=1.0, alfa=1.0):
    d = b - a
    L = float(np.hypot(*d))
    if L < 1 or frac < 0.01:
        return
    u = d / L
    n = np.array([-u[1], u[0]])
    f = min(1.0, frac)
    p1 = a + d * f
    cab = min(ancho * 1.5, L * f)
    base = p1 - u * cab
    w = ancho / 2
    pts = np.array([a + n * w * 0.55, base + n * w * 0.55, base + n * w * 1.5, p1, base - n * w * 1.5, base - n * w * 0.55, a - n * w * 0.55])
    lz.relleno(pts + np.array([6.0, 8.0]), (20, 10, 50), alfa=0.25 * alfa, capa=2)
    lz.relleno(pts, color, alfa=alfa, capa=2)


@shot(T_A, bg=lambda t: BASE(cam_a(t), t), post=[GRAD], ent=("fundido", 0.5))
def fu_cerco(lz, t):
    cam = cam_a(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    g = 1.0 - 0.62 * smooth(prog(t, t_camb, t_desc + 0.8))                # el territorio insurgente se encoge
    c0 = np.array([float(v) for v in MP.proy(cam, -98.94, 18.81)])
    pts = np.array([[float(v) for v in MP.proy(cam, lo, la)] for lo, la in T10.SUR_POLI])
    pts = c0 + (pts - c0) * g
    lz.relleno(pts, (70, 200, 120), alfa=0.26, capa=2)
    lz.trazo(np.vstack([pts, pts[:1]]), (140, 255, 170), 6.0, afinar=False, temblor=0.0, capa=2)
    for j, (lug, tp, nm, dx, dy, lado, bd) in enumerate((("mexico", "ciudad", "Ciudad de México", 0, -100, "abajo", "real"), ("puebla", "ciudad", "Puebla", 100, 4, "izq", "real"), ("oaxaca", "ciudad", "Oaxaca", 110, 4, "izq", "ins"), ("cuautla", "pueblo", "", 0, 0, "izq", "ins"), ("chilpancingo", "ciudad", "Chilpancingo", -130, 4, "der", "ins"))):
        MD.ciudad(lz, cam, lug, t, T_A + 0.1 * j, tam=1.4, tipo=tp, bando=bd, semilla=j + 111)
        if nm:
            MD.etiqueta(lz, cam, lug, nm, t, T_A + 0.1 * j + 0.1, px=22, dy=dy, dx=dx, lado=lado)
    # columnas realistas (flechas rojas) que se cierran sobre el sur desde varios lados
    centro = c0
    for j, (ox, oy) in enumerate(((-520, -300), (520, -260), (560, 120), (-460, 260), (0, -380))):
        u = e_inout(prog(t, t_camb - 0.1 + 0.15 * j, t_desc + 0.6))
        a = centro + np.array([ox, oy], float)
        b = centro + np.array([ox, oy], float) * 0.34
        _flecha(lz, a, b, 60, (232, 70, 80), u)
        if u > 0.05:
            p = a + (b - a) * u
            MD.ejercito(lz, float(p[0]), float(p[1]) + 4, 10, bando="real", t=t + j * 0.2, s=1.4, dir=1 if ox < 0 else -1, semilla=j, bandera=(j == 0), polvo=True)
    kc = U.pop(t, t_vir - 0.1)
    if kc > 0.01:
        MD.medallon(lz, 300, 470, 150, "calleja", t, emocion="serio", k=kc, seed=9)
        U.llamada(lz, 300, 650, "virrey Calleja", color=U.COL["rojo"], px=44, k=kc, cola="arriba")
    k = U.pop(t, t_pero - 0.05) * U.salida(t, t_vir - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el ejército realista cambia de estrategia", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_estr + 0.1), cola=None)
    k = U.pop(t, t_mismo - 0.1) * U.salida(t, t_pers - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el mismo que venció a Hidalgo", color=U.COL["naranja"], px=62, k=k, cola=None)
    k = U.pop(t, t_pers - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "los persigue sin descanso", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_desc + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 2. EL CÍRCULO DE MORELOS CAE
@shot(T_B, bg=lambda t: bg_grad((54, 30, 112), (130, 64, 120), mid=(92, 44, 120), ym=0.5), post=[GRIS], ent=("fundido", 0.5))
def fu_circulo(lz, t):
    U.bokeh(lz, t, seed=71, n=12, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.18)
    cx, cy, R = W / 2, 610, 640
    pers = (("matamoros", "Matamoros", t_mat, 0.0), ("galeana", "Galeana", t_gal, 1.256), ("guerrero", "Guerrero", None, 2.513), ("victoria", "Victoria", None, 3.77), ("leona", "Leona Vicario", None, 5.03))
    # anillo del círculo (se va quebrando)
    nrompe = (t > t_mat + 0.5) + (t > t_gal + 0.9)
    for i in range(5):
        a0, a1 = -1.57 + i * 1.2566, -1.57 + (i + 1) * 1.2566
        u = np.linspace(a0 + 0.12, a1 - 0.12, 24)
        rota = (i == 0 and t > t_mat + 0.5) or (i == 1 and t > t_gal + 0.9)
        if rota:
            continue
        lz.trazo(np.stack([cx + R * np.cos(u), cy + R * 0.5 * np.sin(u)], 1), (255, 214, 84), 8, afinar=False, temblor=0.0, capa=2)
    k0 = U.pop(t, T_B + 0.05, 1.3)
    RT.retrato(lz, cx, cy + 215, 105 * (0.94 + 0.06 * k0), "morelos", t, emocion="serio", mirar=0.0, seed=3, alfa=min(1.0, k0))
    for q, lab, tt_, ang in pers:
        a = ang - 1.57
        x, y = cx + R * math.cos(a), cy + R * 0.5 * math.sin(a)
        ka = U.pop(t, T_B + 0.2 + 0.1 * (ang / 1.256), 1.2)
        caido = tt_ is not None and t > tt_ + 0.8
        if ka > 0.01:
            RT.retrato(lz, x, y + 95, 62 * (0.94 + 0.06 * ka), q, t, emocion="serio", alfa=min(1.0, ka) * (0.38 if caido else 1.0), mirar=-math.cos(a) * 0.4, seed=5)
            U.llamada(lz, x, y - 90, lab, color=U.COL["rojo"] if caido else U.COL["morado"], px=34, k=ka, cola=None, alfa=0.7 if caido else 1.0)
            if caido:
                lz.relleno(np.array([[x - 80, y - 10], [x - 50, y - 30], [x + 80, y + 70], [x + 50, y + 90]]), (14, 12, 22), alfa=0.85, capa=2)
    k = U.pop(t, t_uno - 0.05) * U.salida(t, t_mat - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 110, "uno por uno cae el círculo de Morelos", color=U.COL["naranja"], px=58, k=k * U.repop(t, t_circ + 0.1), cola=None)
    k = U.pop(t, t_mat - 0.05) * U.salida(t, t_gal - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 110, "Matamoros, capturado y fusilado", color=U.COL["rojo"], px=62, k=k * U.repop(t, t_fus + 0.1), cola=None)
    k = U.pop(t, t_gal - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 110, "Galeana, muerto en combate", color=U.COL["rojo"], px=62, k=k * U.repop(t, t_murio + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 3. EL CONGRESO HUYE
def cam_c(t):
    sc = 150 + (t - T_C) * 22
    x, y = mf.pos_camino(sc)
    return (x + 4, y - 4, 24, 4.8)


@shot(T_C, bg=lambda t: bg_grad((90, 100, 140), (170, 170, 190), mid=(130, 134, 164), ym=0.5), post=[GRIS], ent=("fundido", 0.5))
def fu_huida(lz, t):
    cx, cy, cz, zm = cam_c(t)
    iso = I.Iso(float(cx), float(cy), float(cz), float(zm))
    I.luz(mul=(0.86, 0.9, 1.0), mix=(80, 90, 130), k=0.18)
    MARCHA.suelo(lz, iso, t)
    m = MARCHA.objetos(t)
    tipos = ("regidor", "noble", "cura", "escribano", "comerciante", "regidor")
    for i in range(34):                                     # diputados que caminan encorvados con papeles y cofres
        s0 = 100 + 80 * h01(231, i)
        x, y = mf.pos_camino(s0 + (t - T_C) * 22.0)
        ox, oy = -16 + 32 * h01(232, i), -12 + 24 * h01(233, i)
        m.add(x + ox - 4, y + oy - 4, x + ox + 4, y + oy + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, tipos[i % 6], dir=(1, -0.35), vel=1.3, seed=10000 + i, h=44, accion="carga" if i % 2 == 0 else None, cara="miedo")))(x + ox, y + oy, i), fijo=False, clave=x + y + 3)
    for i in range(3):                                      # mulas con baúles de papeles
        x, y = mf.pos_camino(150 + 40 * i + (t - T_C) * 22.0)
        m.add(x - 6, y - 4, x + 6, y + 4, 20, (lambda x, y, i: (lambda lz, iso: G.burro(lz, iso, x + 14, y + 10, t, dir=1, seed=i, carga=True)))(x, y, i), fijo=False, clave=x + y + 12)
    # Morelos con su escolta cubre la retaguardia cuando se ofrece a protegerlos
    k = e_inout(prog(t, t_ofrec - 0.4, t_prot + 0.5))
    sx_, sy_ = mf.pos_camino(60 + (t - T_C) * 22.0)
    if k > 0.01:
        m.add(sx_ - 8, sy_ - 8, sx_ + 8, sy_ + 8, 50, lambda lz, iso: G.caballo(lz, iso, sx_, sy_, t, dir=1, seed=7, vel=1.0, jinete="cura", s=1.3), fijo=False, clave=sx_ + sy_ + 10)
        for j in range(6):
            x2, y2 = mf.pos_camino(30 + 18 * j + (t - T_C) * 22.0)
            m.add(x2 - 4, y2 - 4, x2 + 4, y2 + 4, 40, (lambda x2, y2, j: (lambda lz, iso: G.persona(lz, iso, x2, y2 + 8, t, "insurgente_lanza", dir=(1, -0.3), vel=1.3, seed=10100 + j, h=44, accion="pelea" if j % 2 else None, cara="enojo")))(x2, y2, j), fijo=False, clave=x2 + y2 + 5)
    m.dibujar(lz, iso)
    O2.lluvia(lz, t, dens=1.2, alfa=0.5)
    k = U.pop(t, t_huir - 0.1) * U.salida(t, t_carg - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "el Congreso huye de pueblo en pueblo", color=U.COL["rojo"], px=66, k=k * U.repop(t, t_pueblo + 0.1), cola=None)
    k = U.pop(t, t_carg - 0.05) * U.salida(t, t_mor2 - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "cargando sus papeles", color=U.COL["naranja"], px=76, k=k * U.repop(t, t_pap + 0.1), cola=None)
    k = U.pop(t, t_mor2 - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "Morelos se ofrece a protegerlo", color=U.COL["azul"], px=70, k=k * U.repop(t, t_prot + 0.1), cola=None)


# ------------------------------------------------------------------------------------------------ 4. CAPTURA (mapa)
def cam_d1(t):
    return Klog(t, [(T_D1, (-99.4, 18.6, 2.2)), (T_D2, (-99.3, 18.7, 3.0))])


@shot(T_D1, bg=lambda t: BASE(cam_d1(t), t), post=[GRIS], ent=("zoom", 0.5))
def fu_captura(lz, t):
    cam = cam_d1(t)
    I.luz()
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.08, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    MD.ciudad(lz, cam, "temalaca", t, T_D1, tam=2.0, tipo="pueblo", bando="ins", nombre="Temalaca", px=26, semilla=3)
    MD.ciudad(lz, cam, "mexico", t, T_D1 + 0.1, tam=1.6, tipo="ciudad", bando="real", nombre="Ciudad de México", px=24, semilla=5)
    pm = np.array([float(v) for v in MP.proy(cam, -99.13, 19.43)])
    pt = np.array([float(v) for v in MP.proy(cam, -99.33, 18.80)])
    f = e_inout(prog(t, t_pris - 0.1, T_D2 - 0.1))
    for j in range(5):                                       # soldados que rodean al prisionero y lo llevan a la capital
        p = pt + (pm - pt) * f + np.array([40 * math.cos(j * 1.26), 26 * math.sin(j * 1.26)])
        MD.ejercito(lz, float(p[0]), float(p[1]), 4, bando="real", t=t + j * 0.2, s=1.4, dir=1, semilla=j, bandera=False, polvo=False)
    k = U.pop(t, t_nov - 0.05)
    if k > 0.01:
        U.fecha_lugar(lz, t, T_D1, T_D2 - 0.1, "Temalaca", "Noviembre de 1815", y=70)
    k = U.pop(t, t_cayo - 0.05) * U.salida(t, T_D2 - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "cae prisionero", color=U.COL["rojo"], px=92, k=k * U.repop(t, t_pris + 0.1), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ 5. JUICIO Y DEGRADACIÓN
@shot(T_D2, bg=PURPG, post=[GRIS], ent=("fundido", 0.6))
def fu_juicio(lz, t):
    I.luz(mul=(0.92, 0.92, 1.0), mix=(60, 50, 100), k=0.12)
    iso = I.Iso(140, 118, 44, 4.0 + 0.04 * (t - T_D2), sx0=930, sy0=650)
    T9._sacristia(lz, iso, t)
    m = I.Mundo()
    m.add(60, 20, 220, 56, 30, lambda lz, iso: B.mesa(lz, iso, 60, 20, 160, 34, 22, color=(90, 70, 70), mantel=(40, 36, 60)), clave=140)
    for i, (x, tp) in enumerate(((84, "cura"), (118, "regidor"), (152, "noble"), (186, "cura"))):
        m.add(x - 4, 58, x + 4, 66, 40, (lambda x, tp, i: (lambda lz, iso: G.persona(lz, iso, x, 62, t, tp, dir=(0, 1), seed=10200 + i, h=54, cara="serio", accion="habla" if (t_juz < t < t_degr and i % 2 == 0) else None)))(x, tp, i), fijo=False, clave=x + 62)
    deg = t > t_degr
    m.add(126, 120, 142, 136, 50, lambda lz, iso: G.persona(lz, iso, 134, 128, t, "campesino" if deg else "cura", dir=(0, -1), seed=10210, h=60, cara="triste" if deg else "serio"), fijo=False, clave=270)
    for (x, y) in ((100, 180), (170, 180)):
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y: (lambda lz, iso: G.persona(lz, iso, x, y, t, "realista", dir=(0, -1), seed=10220 + int(x), h=52, cara="serio")))(x, y), fijo=False, clave=x + y)
    m.dibujar(lz, iso)
    if deg:
        u = prog(t, t_degr, t_degr + 1.2)
        qx, qy = iso.P(134, 128, 56)
        lz.relleno(rect_red(float(qx) - 20 + 200 * u, float(qy) - 40 - 220 * u, 40, 14, 4), (240, 240, 244), alfa=1 - u, capa=2)
        lz.relleno(rect_red(float(qx) - 30 - 180 * u, float(qy) - 20 - 260 * u, 60, 20, 6), (36, 32, 48), alfa=1 - u, capa=2)
    U.fecha_lugar(lz, t, T_D2, T_D3 - 0.2, "Ciudad de México", "Diciembre de 1815", y=70)
    k = U.pop(t, t_juz - 0.05) * U.salida(t, t_degr - 0.15, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "lo juzgaron", color=U.COL["morado"], px=92, k=k * U.repop(t, t_juz + 0.2), cola=None)
    k = U.pop(t, t_degr - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "lo degradaron como sacerdote", color=U.COL["rojo"], px=70, k=k * U.repop(t, t_degr + 0.2), cola=None)


# ------------------------------------------------------------------------------------------------ 6. PATIO DE SAN CRISTÓBAL ECATEPEC
@shot(T_D3, bg=PURPG, post=[GRIS], ent=("fundido", 0.5))
def fu_patio(lz, t):
    I.luz(mul=(0.92, 0.92, 1.0), mix=(60, 50, 100), k=0.14)
    iso = I.Iso(150, 110, 40, 3.7, sx0=960, sy0=640)
    mj.patio_ejecucion(lz, iso, t)
    m = mj.objetos_patio(t)
    for i in range(16):
        x = (-10 + 20 * i) if i < 8 else (250 + 14 * (i - 8))
        y = 230 + 10 * (i % 3) - 60 * (i >= 8)
        m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, ("campesino", "campesina", "regidor", "dama", "indigena", "indigena_f", "mestizo", "nino")[i % 8], dir=(1 if x < 150 else -1, -0.4), seed=10300 + i, h=44 if i % 8 != 7 else 30, cara="triste")))(x, y, i), fijo=False, clave=x + y + 3)
    m.add(146, 36, 156, 46, 60, lambda lz, iso: G.persona(lz, iso, 150, 42, t, "campesino", dir=(0, 1), seed=10310, h=60, cara="serio") if t < t_fusi + 0.45 else None, fijo=False, clave=160)
    for i in range(7):
        x = 90 + 18 * i
        m.add(x - 4, 190, x + 4, 198, 50, (lambda x, i: (lambda lz, iso: G.persona(lz, iso, x, 194, t, "granadero", dir=(0, -1), seed=10320 + i, h=56, cara="serio")))(x, i), fijo=False, clave=x + 194)
    m.dibujar(lz, iso)
    if t_fusi + 0.35 < t < t_fusi + 1.2:
        u = (t - t_fusi - 0.35) / 0.85
        qx, qy = iso.P(150, 150, 50)
        lz.halo(float(qx), float(qy), 200 + 140 * u, (255, 230, 170), alfa=0.5 * (1 - u), capa=2)
    if t > t_fusi + 0.6:
        u = prog(t, t_fusi + 0.6, t_fusi + 3.0)
        qx, qy = iso.P(150, 42, 60)
        x, y = float(qx) + 120 * u, float(qy) - 40 - 380 * u
        al = math.sin(t * 10) * 12
        lz.relleno(np.array([[x - 40, y - al], [x, y + 4], [x + 40, y - al], [x, y - 6]]), (250, 250, 255), alfa=1 - 0.5 * u, capa=2)
    k = U.pop(t, t_fusi - 0.1, 1.3)
    if k > 0.01:
        P.rotulo(lz, W / 2, 190, "22 de diciembre de 1815", px=int(96 * (0.94 + 0.06 * k)), k=k, color=(255, 255, 255))
    k = U.pop(t, t_dic - 0.05) * U.salida(t, T_E - 0.3, 0.3)
    if k > 0.01:
        U.llamada(lz, W / 2, 960, "José María Morelos es fusilado", color=U.COL["rojo"], px=58, k=k, cola=None)


# ------------------------------------------------------------------------------------------------ 7. LAS LUCES SE APAGAN
FOCOS = [(-99.5, 17.55), (-98.94, 18.81), (-96.7, 17.06), (-99.89, 16.85), (-101.2, 20.0), (-100.9, 21.16), (-101.26, 21.02), (-102.35, 19.08), (-97.0, 19.2), (-96.1, 18.4), (-99.2, 19.4), (-103.35, 20.67)]


def cam_e(t):
    return Klog(t, [(T_E, (-99.5, 19.5, 1.5)), (T1(E12), (-99.5, 19.4, 1.4))])


@shot(T_E, bg=lambda t: BASE(cam_e(t), t), post=[lambda img, t: U.gradacion(img, luces=(0.96, 0.96, 1.0), sombras=(0.9, 0.92, 1.05), saturacion=0.55 + 0.4 * (1 - smooth(prog(t, t_insu, T1(E12) - 0.6))))], ent=("fundido", 0.6))
def fu_apagon(lz, t):
    cam = cam_e(t)
    I.luz(mul=(0.9, 0.92, 1.0), mix=(30, 34, 90), k=0.18 * smooth(prog(t, T_E, T1(E12) - 0.5)))
    MD.montes(lz, cam, min_alt=2200)
    MD.pais(lz, cam, "Mexico", (255, 96, 70), alfa=0.06, borde=(255, 220, 90), ancho=4.0, t=t, latido=0.0)
    for i, (lo, la) in enumerate(FOCOS):
        t_off = t_par + 0.3 + (T1(E12) - 0.6 - t_par) * (i / (len(FOCOS) - 1))
        a = 1.0 - smooth(prog(t, t_off, t_off + 0.5))
        sx, sy = MP.proy(cam, lo, la)
        if a > 0.01:
            lz.halo(float(sx), float(sy), 220, (140, 255, 170), alfa=0.6 * a, capa=2)
            lz.relleno(circulo(float(sx), float(sy), 24, 16), (200, 255, 210), alfa=a, capa=2)
            MD.bandera_mapa(lz, float(sx), float(sy) - 20, (70, 190, 110), t + i, 1.0 * a)
        else:
            lz.relleno(circulo(float(sx), float(sy), 10, 12), (60, 60, 80), alfa=0.8, capa=2)
    k = U.pop(t, t_con - 0.05) * U.salida(t, t_insu - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "con él…", color=U.COL["morado"], px=96, k=k, cola=None)
    k = U.pop(t, t_par - 0.05) * U.salida(t, t_term - 0.2, 0.2)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "parecía que la insurgencia…", color=U.COL["naranja"], px=70, k=k, cola=None)
    k = U.pop(t, t_term - 0.05)
    if k > 0.01:
        U.llamada(lz, W / 2, 130, "…se había terminado", color=U.COL["rojo"], px=88, k=k * U.repop(t, t_term + 0.2), cola=None)
    MD.brujula(lz, W - 110, H - 120, 1.0)


# ------------------------------------------------------------------------------------------------ sonido
snd(T_A + 0.2, "whoosh", 0.3, dur=1.0)
snd(t_vir, "pop", 0.4)
snd(t_pers, "tambor", 0.4)
snd(T_B, "gong", 0.4)
snd(t_mat + 0.6, "gong", 0.5)
snd(t_gal + 0.9, "gong", 0.5)
snd(T_C, "trueno", 0.3)
snd(t_prot, "galope", 0.4, dur=1.5)
snd(T_D1, "whoosh", 0.3, dur=0.9)
snd(t_pris, "gong", 0.5)
snd(T_D2, "pluck", 0.4)
snd(t_degr, "crujido", 0.5)
snd(T_D3, "pluck", 0.4)
snd(t_fusi + 0.35, "canonazo", 0.5)
snd(T_E, "gong", 0.4)
for _i in range(6):
    snd(t_par + 0.5 + 0.4 * _i, "pop", 0.2)
