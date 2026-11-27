# -*- coding: utf-8 -*-
"""Planos 3: Hera, lo que vio, lo que sigue, por qué importa, cierre."""
import math

import numpy as np

from comun import (H, W, L3, Cam, E, ap, cabecera, clamp, contador, e_inout, e_out, etiqueta3d, F0, F1, foto, globo, lerp, pr,
                   real, smooth, T0, T1, vacio, vent, ww, a_img, _Img, circulo3d, nrm, R_T, curva_suave)
from p3d import (O, X, Y, Z, SOL, R_DID, R_DIM, R_ORB, P_ANTES, P_DESPUES, cam_orb, pos_dim, didymos, dimorphos, orbita,
                 flecha3d, reloj, orbita_planeta, pos_planeta, sol)
from planos1 import rp, con_foto, ang_dim
from _seg import SEG


# ------------------------------------------------------------------ HERA
def h_modelo(t):
    """Hera: despliega sus alas; rótulos de lo que lleva."""
    t0 = F0("hera", 1) - 0.3
    k = pr(t, t0, F0("hera", 3))
    alas = e_inout(pr(t, t0, t0 + 2.5))
    lz = L3(cam_orb(np.array([0, 0, 0.3]), lerp(15, 19, k), lerp(-35, -12, k), 22, centro=(W * 0.44, H * 0.52), cerca=0.1))
    E.estrellas(lz)
    E.hera(lz, O, np.eye(3), alas=max(alas, 0.02))
    etiqueta3d(lz, np.array([0, 5.0, 0.4]) * min(1, alas * 1.2), "ALAS SOLARES", None, dx=150, dy=-170,
               op=ap(t, ww("hera", 1, "alas") - 0.1) * smooth(pr(alas, 0.5, 0.8)), px=30)
    etiqueta3d(lz, np.array([0.82, 0, 0.3]), "CÁMARAS", None, dx=-170, dy=-140, op=ap(t, ww("hera", 2, "cámaras") - 0.1), px=30)
    etiqueta3d(lz, np.array([0.82, 0.4, -0.2]), "CÁMARA DE CALOR", "JAPÓN", dx=-200, dy=110, op=ap(t, ww("hera", 2, "calor") - 0.1), px=30)
    o_l = ap(t, ww("hera", 2, "láser") - 0.1)
    if o_l > 0:
        P0 = np.array([0.85, -0.3, 0.0])
        lz.linea(np.array([P0, P0 + np.array([30, 0, -2])]), o_l * 0.8, 1.4, guion=4)
        etiqueta3d(lz, np.array([0.85, -0.3, 0.0]), "LÁSER", "MIDE DISTANCIAS", dx=170, dy=150, op=o_l, px=30)
    cabecera(lz, "HERA · AGENCIA ESPACIAL EUROPEA")
    return lz


# órbitas (UA) para el plano del viaje: Tierra, Marte y Didymos (a, e, perihelio)
A_DID, E_DID, W_DID = 1.64, 0.38, math.radians(-40)
A_MAR, E_MAR = 1.52, 0.09


def h_ruta(t):
    """El viaje de Hera: Tierra (oct-2024) → Marte (mar-2025) → Didymos (nov-2026). ESQUEMÁTICO."""
    t0 = F0("hera", 3) - 0.3
    t1 = F1("hera", 4) + 0.4
    k = pr(t, t0, t1)
    lz = L3(cam_orb(np.array([0.2, 0.1, 0]), 6.2, 15 + 10 * k, 55, fov=36, centro=(W * 0.5, H * 0.53), cerca=0.01))
    E.estrellas(lz, op=0.3)
    sol(lz)
    orbita_planeta(lz, 1.0, 0.45)
    orbita_planeta(lz, A_MAR, 0.45, e=E_MAR)
    orbita_planeta(lz, A_DID, 0.35, e=E_DID, varpi=W_DID, guion=3)
    Pt = pos_planeta(1.0, 200)
    Pm = pos_planeta(A_MAR, 95, E_MAR)
    Pd = pos_planeta(A_DID, -20, E_DID, W_DID)
    # trayectoria (curva suave por los tres puntos, saliendo de la Tierra hacia fuera)
    ctrl = np.array([Pt, pos_planeta(1.18, 150), Pm, pos_planeta(1.75, 40), Pd])
    from scipy.interpolate import CubicSpline  # noqa: E402
    cs = CubicSpline(np.arange(len(ctrl)), ctrl, axis=0)
    u = np.linspace(0, len(ctrl) - 1, 300)
    tray = cs(u)
    kt = e_inout(pr(t, t0 + 0.6, t1 - 0.5))
    n = max(2, int(300 * kt))
    lz.linea(tray[:n], 0.9, 1.6)
    if n > 2:
        E.hera(lz, tray[n - 1], E.rot_ypr(0, 0, 0), esc=0.03)
        lz.puntos(tray[n - 1], r=4, op=1.0)
    for P, txt, sub, ta, dx, dy in ((Pt, "TIERRA", "DESPEGUE · OCT-2024", t0, -150, 110),
                                     (Pm, "MARTE", "SOBREVUELO · MAR-2025", ww("hera", 3, "marte") - 0.2, 140, -120),
                                     (Pd, "DIDYMOS", "LLEGADA · NOV-2026", F0("hera", 4) + 1.5, 150, 100)):
        lz.puntos(P, r=5, op=ap(t, ta))
        etiqueta3d(lz, P, txt, sub, dx=dx, dy=dy, op=ap(t, ta), px=28)
    o = ap(t, ww("hera", 4, "gratis") - 0.2)
    lz.texto("ASISTENCIA GRAVITATORIA", 120, 900, 40, "Bold Condensed", o, "lm", esp=0.06)
    lz.texto("MARTE LA ACELERA Y LA DESVÍA SIN GASTAR COMBUSTIBLE", 122, 945, 22, "SemiBold Condensed", o * 0.9, "lm", esp=0.14)
    lz.texto("TRAYECTORIA ESQUEMÁTICA", W - 80, 1010, 18, "SemiBold Condensed", ap(t, t0) * 0.6, "rm", esp=0.16)
    cabecera(lz, "EL VIAJE DE HERA")
    return lz


# ------------------------------------------------------------------ LO QUE VIO
def m_forma(t, ta, tb):
    """Dimorphos antes y ahora, lado a lado; ahora con la cara aplanada, el cráter y dando tumbos."""
    k = pr(t, ta, tb)
    lz = L3(cam_orb(np.array([0, 0, 0]), 640, 0, 12, fov=40, centro=(W * 0.5, H * 0.46)))
    E.estrellas(lz, op=0.35)
    ant = np.array([-230.0, 0, 0])
    aho = np.array([230.0, 0, 0])
    dimorphos(lz, ant, yaw=-30 + 10 * k, rocas=160)
    s = t - ta
    dimorphos(lz, aho, despues=True, yaw=-20 + 25 * math.sin(s * 0.5), pitch=15 * math.sin(s * 0.37), roll=12 * math.sin(s * 0.61),
              rocas=160)
    lz.texto("ANTES · DART 2022", 960 - 420, 860, 30, "Bold Condensed", ap(t, ta), "mm", esp=0.1)
    lz.texto("AHORA · HERA 2026", 960 + 420, 860, 30, "Bold Condensed", ap(t, ta + 0.3), "mm", esp=0.1)
    lz.texto("RECREACIÓN 3D", 960, 1010, 18, "SemiBold Condensed", ap(t, ta) * 0.6, "mm", esp=0.2)
    return lz


def m_tumbos(t):
    """Antes: siempre la misma cara hacia Didymos (como la Luna). Ahora: tumbos."""
    t0 = F0("imagenes", 7) - 0.3
    tt = ww("imagenes", 8, "tumbos") - 0.5
    lz = L3(cam_orb(np.array([R_ORB * 0.5, 0, 0]), 2600, -15, 22, centro=(W * 0.4, H * 0.5)))
    E.estrellas(lz)
    orbita(lz, 0.4)
    didymos(lz, t)
    s = t - t0
    ang = -65 + s * 6
    P = pos_dim(ang)
    q = max(0.0, t - tt)
    kq = min(1.0, q / 1.5)
    dimorphos(lz, P, despues=True, yaw=ang + 270 + q * 45, pitch=30 * math.sin(q * 0.9) * kq, roll=25 * math.sin(q * 1.3) * kq,
              esc=1.5)
    oa = vent(t, t0 + 0.3, tt)
    lz.linea(np.array([P, P * 0.15]), oa * 0.5, 1.0, guion=3)
    lz.texto("ANTES: SIEMPRE LA MISMA CARA", 1500, 820, 46, "Bold Condensed", oa, "mm", esp=0.05)
    lz.texto("COMO LA LUNA CON LA TIERRA", 1500, 872, 22, "SemiBold Condensed", oa * 0.9, "mm", esp=0.16)
    o = ap(t, tt + 0.4)
    lz.texto("AHORA: DA TUMBOS", 1500, 820, 64, "Bold Condensed", o, "mm", esp=0.05)
    lz.texto("GIRO CAÓTICO · RECREACIÓN 3D", 1500, 880, 22, "SemiBold Condensed", o * 0.9, "mm", esp=0.16)
    cabecera(lz, "DIMORPHOS · ANTES Y AHORA")
    return lz


# ------------------------------------------------------------------ LO QUE SIGUE
def n_acerca(t):
    """Hera se acerca de ~30 km a ~13 km y suelta a Milani y Juventas."""
    t0 = F0("sigue", 1) - 0.3
    k = e_inout(pr(t, t0, F0("sigue", 2)))
    r = lerp(30000, 13000, k)
    lz = L3(cam_orb(np.array([0, 0, 0]), lerp(80000, 42000, k), 25, 35, fov=36, centro=(W * 0.45, H * 0.5)))
    E.estrellas(lz)
    lz.linea(circulo3d(O, Z, r, 180), 0.5, 1.0, guion=3)
    x, y = lz.cam.px(O)
    lz.c2(x, y, 6, 1.0, lleno=True)
    etiqueta3d(lz, O, "DIDYMOS + DIMORPHOS", None, dx=-160, dy=-120, op=ap(t, t0), px=26)
    a = math.radians(30 + 40 * pr(t, t0, T1("sigue")))
    Ph = np.array([r * math.cos(a), r * math.sin(a), 0])
    E.hera(lz, Ph, E.rot_ypr(math.degrees(a) + 180, 0, 0), esc=700)
    lz.texto(f"{r / 1000:.0f} KM", 1550, 300, 96, "Bold Condensed", ap(t, t0), "mm", esp=0.03)
    lz.texto("DISTANCIA DE HERA", 1550, 365, 22, "SemiBold Condensed", ap(t, t0) * 0.9, "mm", esp=0.18)
    # CubeSats
    oc = ap(t, ww("sigue", 2, "enero") - 0.2)
    if oc > 0:
        kc = e_out(pr(t, ww("sigue", 2, "enero"), ww("sigue", 2, "enero") + 4))
        for i, (nom, dd) in enumerate((("MILANI", np.array([-1, 0.4, 0.2])), ("JUVENTAS", np.array([-1, -0.5, -0.1])))):
            Pc = Ph + nrm(dd - Ph / np.linalg.norm(Ph) * 0.6) * 9000 * kc
            E.caja(lz, Pc, np.eye(3), (900, 600, 300))
            etiqueta3d(lz, Pc, nom, ("ESTUDIA EL POLVO" if i == 0 else "RADAR: VE POR DENTRO"), dx=-150 if i == 0 else 150,
                       dy=-120 if i == 0 else 120, op=oc * ap(t, ww("sigue", 2, nom.lower()) - 0.2), px=28)
    cabecera(lz, "LO QUE SIGUE")
    return lz


def n_radar(t):
    """Juventas mira por dentro: ondas de radar que atraviesan el asteroide (corte)."""
    t0 = F0("sigue", 3) - 0.3
    lz = L3(cam_orb(np.array([0, 0, 0]), 520, 20, 15, centro=(W * 0.45, H * 0.5)))
    E.estrellas(lz)
    dimorphos(lz, O, despues=True, yaw=10 + 5 * pr(t, t0, T1("sigue")))
    s = t - t0
    for i in range(6):
        f = ((s * 0.6 + i / 6) % 1.0)
        rr = 40 + f * 260
        lz.linea(circulo3d(np.array([0, -300, 40]), nrm(np.array([0, 1, -0.1])), rr * 0.4, 64), (1 - f) * 0.6, 1.0)
        lz.linea(circulo3d(np.array([0, 0, 0]), Y, rr * 0.35, 64), (1 - f) * 0.35 * ap(t, t0 + 0.8), 0.8)
    E.caja(lz, np.array([0, -320, 45]), np.eye(3), (14, 9, 5))
    o = ap(t, t0)
    lz.texto("POR DENTRO", 1520, 800, 72, "Bold Condensed", o, "mm", esp=0.05)
    lz.texto("PRIMERA VEZ EN UN ASTEROIDE", 1520, 860, 22, "SemiBold Condensed", o * 0.9, "mm", esp=0.16)
    cabecera(lz, "JUVENTAS · RADAR · RECREACIÓN 3D")
    return lz


# ------------------------------------------------------------------ POR QUÉ IMPORTA
def p_desvio(t):
    """Un empujón pequeño años antes = miles de km de diferencia: la Tierra y dos trayectorias que se separan."""
    t0 = F0("importa", 6) - 0.3
    k = pr(t, t0, T1("importa") + 0.5)
    C = np.array([0.0, 0, 0])
    lz = L3(cam_orb(C, lerp(60000, 52000, k), -60, 18, fov=40, centro=(W * 0.62, H * 0.5), cerca=10))
    E.estrellas(lz)
    globo(lz, C, R_T, op=0.9, paso=20)
    s = np.linspace(0, 1, 200)
    A = np.array([-90000.0, 30000, 0])
    B = C + np.array([0, 0, 0.0])
    d1 = A[None] + (B - A)[None] * s[:, None]
    kd = e_inout(pr(t, t0 + 0.6, t0 + 4.0))
    lz.linea(d1, 0.35, 1.0, guion=4)
    off = np.array([0, 0, 1.0])[None] * ((s ** 2) * 18000 * kd)[:, None]
    d2 = d1 + off
    n = max(2, int(200 * e_out(pr(t, t0, t0 + 3.0))))
    lz.linea(d2[:n], 1.0, 1.6)
    lz.puntos(d2[n - 1], r=4, op=1.0)
    o1 = ap(t, t0 + 0.4)
    lz.texto("PUNTEADA · SIN EMPUJÓN: CHOQUE", 120, 860, 34, "Bold Condensed", o1 * 0.85, "lm", esp=0.06)
    o2 = ap(t, t0 + 3.0)
    lz.texto("CONTINUA · CON UN EMPUJÓN AÑOS ANTES: PASA DE LARGO", 120, 920, 34, "Bold Condensed", o2, "lm", esp=0.06)
    o3 = ap(t, ww("importa", 7, "minutos") - 0.2)
    lz.texto("MINUTOS HOY = MILES DE KM DESPUÉS", 120, 200, 46, "Bold Condensed", o3, "lm", esp=0.05)
    lz.texto("ESQUEMA · NO A ESCALA", W - 80, 1010, 18, "SemiBold Condensed", ap(t, t0) * 0.6, "rm", esp=0.16)
    cabecera(lz, "DEFENSA PLANETARIA")
    return lz


def p_apophis(t):
    """Apophis, 13-abr-2029: pasa por dentro del anillo de los satélites geoestacionarios. ESQUEMA."""
    t0 = T0("cierre")
    k = pr(t, t0, F1("cierre", 0) + 0.3)
    C = np.array([0.0, 0, 0])
    lz = L3(cam_orb(C, lerp(140000, 120000, k), -50 + 20 * k, 42, fov=40, centro=(W * 0.38, H * 0.5), cerca=10))
    E.estrellas(lz)
    globo(lz, C, R_T, op=0.9, paso=20)
    rg = 42164.0
    lz.linea(circulo3d(C, Z, rg, 200), 0.5, 1.0, guion=3)
    for i in range(10):
        a = math.radians(i * 36 + t * 2)
        lz.puntos(np.array([rg * math.cos(a), rg * math.sin(a), 0]), r=3, op=0.8)
    etiqueta3d(lz, np.array([rg * math.cos(math.radians(115)), rg * math.sin(math.radians(115)), 0]), "SATÉLITES", "36 000 KM DE ALTURA",
               dx=150, dy=-110, op=ap(t, t0 + 0.4) * 0.9, px=24)
    s = np.linspace(-1, 1, 200)
    d0 = 32000.0 + R_T
    tray = np.stack([s * 160000, np.full_like(s, -d0), s * s * 4000], -1)
    ka = e_inout(pr(t, t0 + 0.3, F1("cierre", 0)))
    n = max(2, int(101 * ka))
    lz.linea(tray[:n], 1.0, 1.6)
    E.asteroide(lz, tray[n - 1], 1800, forma="huevo", rot=E.rot_ypr(t * 40, 20, 0), sol=SOL, rocas=40, semilla=11)
    etiqueta3d(lz, tray[n - 1], "APOPHIS", "A MENOS DE 32 000 KM", dx=150, dy=-130, op=ap(t, t0 + 1.0), px=30)
    o = ap(t, ww("cierre", 0, "trece") - 0.2)
    lz.texto("13 · ABRIL · 2029", 1520, 300, 72, "Bold Condensed", o, "mm", esp=0.04)
    o2 = ap(t, ww("cierre", 0, "telescopio") - 0.3)
    lz.texto("SE VERÁ A SIMPLE VISTA", 1520, 370, 28, "SemiBold Condensed", o2, "mm", esp=0.16)
    lz.texto("ESQUEMA · NO A ESCALA", W - 80, 1010, 18, "SemiBold Condensed", ap(t, t0) * 0.6, "rm", esp=0.16)
    cabecera(lz, "LA PRÓXIMA CITA")
    return lz


def c_cierre(t):
    t0 = F0("cierre", 1) - 0.3
    k = pr(t, t0, T1("cierre"))
    foco = np.array([R_ORB * 0.45, 0, 0])
    lz = L3(cam_orb(foco, lerp(3800, 4600, k), lerp(-20, 10, k), 22, centro=(W * 0.32, H * 0.5)))
    E.estrellas(lz)
    orbita(lz, 0.35)
    didymos(lz, t)
    P = pos_dim(ang_dim(t))
    dimorphos(lz, P, despues=True, yaw=t * 20, pitch=10 * math.sin(t))
    a = t * 0.15
    E.hera(lz, foco + np.array([1800 * math.cos(a), 1800 * math.sin(a), 500]), E.rot_ypr(math.degrees(a), 0, 0), esc=40)
    o = ap(t, t0 + 0.3)
    lz.texto("T MENOS CERO", 1180, 430, 110, "Bold Condensed", o, "lm", esp=0.04)
    lz.texto("CADA MISIÓN, EXPLICADA EN 3D", 1186, 515, 30, "SemiBold Condensed", o * 0.9, "lm", esp=0.2)
    o2 = ap(t, ww("cierre", 1, "suscríbete") - 0.1)
    lz.l2([(1186, 600), (1600, 600), (1600, 668), (1186, 668)], o2, 1.8, cerrada=True)
    lz.texto("SUSCRÍBETE", 1393, 634, 40, "Bold Condensed", o2, "mm", esp=0.1)
    o3 = ap(t, F0("cierre", 2) - 0.1)
    lz.texto("¿QUÉ MISIÓN SIGUE?", 1186, 760, 44, "Bold Condensed", o3, "lm", esp=0.05)
    lz.texto("DÍNOSLO EN LOS COMENTARIOS", 1188, 806, 22, "SemiBold Condensed", o3 * 0.9, "lm", esp=0.18)
    return lz


def S(k, d=0.0):
    return SEG.get(k, d)


FE = "FOTO: ESA · CC BY-SA 3.0 IGO"


def _base(cab):
    def f(t):
        lz = vacio()
        E.estrellas(lz, op=0.35)
        cabecera(lz, cab)
        return lz
    return f


def _importa(t):
    lz = _base("HACE 66 MILLONES DE AÑOS")(t)
    o = vent(t, T0("importa") + 0.1, F0("importa", 1) - 0.1)
    lz.texto("¿POR QUÉ IMPORTA?", 960, 540, 140, "Bold Condensed", o, "mm", esp=0.03)
    return lz


def _forma(t):
    return m_forma(t, ww("imagenes", 5, "cráter") - 0.3, F1("imagenes", 5) + 0.5)


PLANOS = [
    # ---------------- HERA
    (T0("hera"), rp("hera_lanz", S("hera_lanz", 60.0), T0("hera"), "HERA · 7-OCT-2024", "FALCON 9 · CABO CAÑAVERAL, FLORIDA")),
    (F0("hera", 1) - 0.3, h_modelo),
    (F0("hera", 3) - 0.3, h_ruta),
    (ww("hera", 3, "aprovechó") - 0.2, rp("hera_marte", S("marte", 40.0), ww("hera", 3, "aprovechó") - 0.2, "MARTE Y DEIMOS",
                                          "FOTOS REALES DE HERA · MARZO 2025")),
    (F0("hera", 4) - 0.3, h_ruta),
    (F0("hera", 5) - 0.3, rp("hera_llegada", S("llegada", 0.0), F0("hera", 5) - 0.3, "LA LLEGADA",
                             "DE 270 000 KM A 52 KM · FOTOS DE HERA", vel=S("llegada_vel", 5.0), tfin=S("llegada_fin", 66.0))),
    (F0("hera", 6) - 0.3, rp("hera_norte", S("norte", 0.0), F0("hera", 6) - 0.3, "DIDYMOS Y DIMORPHOS", "VISTOS POR HERA DESDE EL NORTE")),
    # ---------------- LO QUE VIO
    (T0("imagenes"), con_foto(rp("esa_intro", S("berlin", 137.6), T0("imagenes"), "ESA · 25-NOV-2026", "LA PRESENTACIÓN, EN BERLÍN"),
                              dict(nombre="museo_dino", cx=1420, cy=520, ancho=640, t0=ww("imagenes", 0, "dinosaurios") - 0.4,
                                   t1=F0("imagenes", 1) - 0.2, rotulo="LA SALA DE LOS DINOSAURIOS",
                                   sub="FOTO: MUSEO DE HISTORIA NATURAL DE BERLÍN · COMMONS · CC BY 2.0", estilo=2, asp=1.5))),
    (F0("imagenes", 1) - 0.3, con_foto(_base("FOTO REAL DE HERA · NOVIEMBRE 2026"),
                                       dict(nombre="esa_dimorphos", cx=960, cy=520, ancho=780, t0=F0("imagenes", 1) - 0.3,
                                            t1=F0("imagenes", 3) - 0.2, rotulo="DIMORPHOS HOY", sub=FE, estilo=0, asp=420 / 360))),
    (F0("imagenes", 3) - 0.3, rp("esa_10m", S("diez", 10.0), F0("imagenes", 3) - 0.3, "«NOS DIJERON: UNOS 10 METROS»",
                                 "TRANSMISIÓN DE LA ESA")),
    (F0("imagenes", 4) - 0.3, rp("esa_puro", S("puro", 18.0), F0("imagenes", 4) - 0.3, "UNA ESTRUCTURA RARA",
                                 "EN EL CENTRO DEL CRÁTER · AÚN SIN EXPLICACIÓN")),
    (F0("imagenes", 5) - 0.3, con_foto(_base("ANTES Y DESPUÉS · FOTOS DE HERA"),
                                       dict(nombre="esa_antes_despues", cx=960, cy=520, ancho=1500, t0=F0("imagenes", 5) - 0.3,
                                            t1=ww("imagenes", 5, "cráter") - 0.3, rotulo="LAS TRES COSAS A LA VEZ", sub=FE, estilo=0,
                                            asp=850 / 478))),
    (ww("imagenes", 5, "cráter") - 0.3, _forma),
    (F0("imagenes", 6) - 0.3, con_foto(_base("FUERA DEL CRÁTER · TODO IGUAL QUE EN 2022"),
                                       dict(nombre="esa_dimorphos", cx=560, cy=530, ancho=640, t0=F0("imagenes", 6) - 0.3,
                                            t1=F1("imagenes", 6) + 0.5, rotulo="HERA · 2026", sub=FE, estilo=0, asp=420 / 360),
                                       dict(nombre="dart_penultima", cx=1360, cy=530, ancho=560, t0=F0("imagenes", 6) + 0.2,
                                            t1=F1("imagenes", 6) + 0.5, rotulo="DART · 2022", sub="FOTO: NASA / JOHNS HOPKINS APL",
                                            estilo=1, asp=1.0))),
    (F0("imagenes", 7) - 0.3, m_tumbos),
    (ww("imagenes", 8, "objeto") - 0.2, rp("hera_sur", S("sur", 0.0), ww("imagenes", 8, "objeto") - 0.2, "DIMORPHOS DA TUMBOS",
                                           "VIDEO REAL DE HERA · DESDE EL SUR")),
    (F0("imagenes", 9) - 0.3, rp("esa_rocas", S("rocas", 11.5), F0("imagenes", 9) - 0.3, "CIENTOS DE ROCAS",
                                 "DE UNOS POCOS METROS · NADIE LAS HABÍA VISTO")),
    (F0("imagenes", 10) - 0.3, rp("esa_10m", 32.0, F0("imagenes", 10) - 0.3, "«UNA AVENTURA DE INDIANA JONES»",
                                  "HABRÁ QUE ESQUIVAR LAS ROCAS · TRANSMISIÓN DE LA ESA")),
    # ---------------- LO QUE SIGUE
    (T0("sigue"), rp("esa_estafeta", S("estafeta", 5.0), T0("sigue"), "HERA", "FASE DE CARACTERIZACIÓN")),
    (F0("sigue", 1) - 0.3, n_acerca),
    (F0("sigue", 3) - 0.3, n_radar),
    (F0("sigue", 4) - 0.3, con_foto(_base("¿CUÁNTO EMPUJÓ DART? · LA CUENTA FINAL"),
                                    dict(nombre="esa_tiri", cx=960, cy=520, ancho=1500, t0=F0("sigue", 4) - 0.3, t1=T1("sigue") + 0.5,
                                         rotulo="HERA: CÁMARA NORMAL Y CÁMARA DE CALOR", sub=FE, estilo=0, asp=820 / 421))),
    # ---------------- POR QUÉ IMPORTA
    (T0("importa"), con_foto(_importa,
                             dict(nombre="chicxulub", cx=960, cy=530, ancho=560, t0=F0("importa", 1) - 0.3,
                                  t1=F0("importa", 2) - 0.2, rotulo="CHICXULUB · YUCATÁN, MÉXICO", sub="IMAGEN: NASA · DOMINIO PÚBLICO",
                                  estilo=0, asp=1233 / 1400),
                             dict(nombre="museo_dino", cx=960, cy=520, ancho=1100, t0=F0("importa", 2) - 0.3,
                                  t1=F0("importa", 3) - 0.2, rotulo="EL FIN DE LOS DINOSAURIOS",
                                  sub="FOTO: MUSEO DE HISTORIA NATURAL DE BERLÍN · CC BY 2.0", estilo=2, asp=1.5))),
    (F0("importa", 3) - 0.3, rp("esa_intro", S("dino", 95.0), F0("importa", 3) - 0.3, "«LOS DINOSAURIOS NO TENÍAN AGENCIA ESPACIAL»",
                                "TRANSMISIÓN DE LA ESA · BERLÍN")),
    (F0("importa", 4) - 0.3, con_foto(_base("TUNGUSKA · SIBERIA · 1908"),
                                      dict(nombre="tunguska", cx=960, cy=520, ancho=1100, t0=F0("importa", 4) - 0.3,
                                           t1=F0("importa", 5) - 0.1, rotulo="EL BOSQUE DERRIBADO", sub="FOTO: EXPEDICIÓN KULIK · DOMINIO PÚBLICO",
                                           estilo=2, asp=1.47))),
    (F0("importa", 5) - 0.3, rp("chel_dash", S("chel", 5.0), F0("importa", 5) - 0.3, "CHELIÁBINSK, RUSIA · 2013",
                                "CASI 1 500 HERIDOS")),
    (F0("importa", 6) - 0.3, p_desvio),
    # ---------------- CIERRE
    (T0("cierre"), p_apophis),
    (F0("cierre", 1) - 0.3, c_cierre),
]


def sfx():
    return [(T0("hera"), "rugido", 0.7, 0.0, None), (F0("hera", 1) - 0.1, "despliegue", 0.6, 0.0, None),
            (ww("hera", 2, "cámaras"), "hud", 0.5, -0.2, None), (ww("hera", 2, "calor"), "hud", 0.5, 0.0, None),
            (ww("hera", 2, "láser"), "radar", 0.5, 0.2, None), (F0("hera", 3) - 0.3, "whoosh", 0.6, 0.0, None),
            (ww("hera", 3, "aprovechó"), "foto", 0.6, 0.0, None), (F0("hera", 5), "foto", 0.5, 0.0, None),
            (T0("imagenes"), "whoosh", 0.5, 0.0, None), (F0("imagenes", 1) - 0.2, "pulso", 0.9, 0.0, None),
            (F0("imagenes", 4), "radar", 0.5, 0.0, None), (F0("imagenes", 8), "rocas", 0.5, 0.0, None),
            (F0("imagenes", 9) - 0.2, "hud", 0.6, 0.0, None), (F0("imagenes", 10), "alarma", 0.45, 0.0, None),
            (T0("sigue"), "whoosh", 0.5, 0.0, None), (ww("sigue", 2, "milani"), "despliegue", 0.5, -0.2, None),
            (ww("sigue", 2, "juventas"), "despliegue", 0.5, 0.2, None), (F0("sigue", 3), "radar", 0.6, 0.0, None),
            (ww("importa", 1, "yucatán"), "impacto", 0.7, 0.0, None), (F0("importa", 4), "rocas", 0.5, 0.0, None),
            (F0("importa", 5) + 0.3, "cristales", 0.6, 0.0, None), (F0("importa", 6) - 0.3, "whoosh", 0.5, 0.0, None),
            (F0("importa", 8), "sello", 0.7, 0.0, None), (T0("cierre"), "whoosh", 0.6, 0.0, None),
            (F0("cierre", 1) - 0.2, "pulso", 0.8, 0.0, None)]
