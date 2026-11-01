# -*- coding: utf-8 -*-
"""Personajes del paisaje: la protagonista («tú»), la gente del parque y del pueblo, el perro, Kuri (mascota del canal)
y los aviones (el jumbo que planea, el que vuelve a encender motores y los lejanos con estela)."""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from plano import mezcla
from motor import prog, clamp01, lerp, e_in, e_out, e_inout, circulo, rect_red, h01
from mundo_comun import kf, pop, ventana, campana
from anclas import A, B0, PORTAL_IN, PORTAL_OUT, Z4
from estado import T_FUEGO, T_O2_FUERA
import kit_oxi as KO
import ui_base as UB
import mundo_paisaje as MP

X_PROTA = -800.0
S_PERS = 28.0          # px por unidad del personaje a k = 1 (≈ 230 de alto)


def _base(X, est):
    return float(MP.suelo_h(X, 1.0, est.get("hundir", 0.0))) - 6


# ======================================================================== Kuri
# (t, X) — entre claves Kuri va dando saltitos
_KURI = [(0.0, -640.0), (84.6, -640.0), (88.2, 250.0), (109.6, 250.0), (113.0, 1240.0), (128.9, 1240.0),
         (128.95, -650.0), (190.5, -650.0), (214.0, 540.0), (254.0, 540.0), (254.05, -650.0)]


def pos_kuri(t):
    X = float(kf(t, _KURI, ease=lambda u: u))
    for (a, xa), (b, xb) in zip(_KURI[:-1], _KURI[1:]):
        if a < t < b and abs(xb - xa) > 5 and b - a > 0.2:
            n = max(1, int(abs(xb - xa) / 110))
            u = (t - a) / (b - a)
            salto = 46 * abs(math.sin(math.pi * u * n))
            return X, salto, 1 if xb > xa else -1
    return X, 0.0, 0


def kuri(lz, t, S, est):
    X, salto, d = pos_kuri(t)
    if not S.vis(X - 120, X + 120, -50, 260):
        return
    base = _base(X, est)
    mirar = (0.0, 0.0)
    aleteo = 0.0
    tirit = 0.0
    feliz = 0.0
    boca = 0.0
    s = 0.95
    voltear = d < 0
    if t < A.imagina + 0.4:                         # aguanta la respiración con la protagonista
        s *= 1 + 0.12 * e_out(prog(t, A.respira, A.respira + 0.9))
        mirar = (-0.8, -0.2)
    elif t < A.esfuma:
        mirar = (-0.6, -0.4)
    elif t < A.oidos - 0.2:
        tirit = 0.6 * ventana(t, A.esfuma, A.ligero, 0.1, 0.6)
        mirar = (-0.5, -0.8)
    elif t < A.demasiado + 1.0:
        aleteo = 1.0                                # se tapa los oídos (brazos arriba)
        tirit = 0.4
        mirar = (-0.6, 0.0)
    elif t < A.uno_f:
        mirar = (0.2, -1.0)                         # mira el cielo
    elif t < A.aviones - 0.5:
        mirar = (0.8, -0.2)
    elif t < A.centrales:
        mirar = (0.3, -1.0)
    elif t < 129:
        mirar = (0.6, -0.6) if t < A.sol_f else (0.0, -1.0)
        tirit = 0.5 * ventana(t, A.seguridad, A.apagones + 1.2, 0.2, 0.4)
    elif t < A.vuelve_ra:
        mirar = (-0.7, 0.0)
        tirit = 0.3 * est.get("mareo", 0.0)
    elif t < A.version_facil:
        feliz = 1.0 if t > A.sobreviviriamos else 0.0
        mirar = (-0.6, 0.0)
        aleteo = 0.6 * ventana(t, A.sobreviviriamos, A.version_facil, 0.2, 0.3)
    elif t < A.piezas - 0.4:
        mirar = (0.5, 0.3)
        tirit = 0.4 * ventana(t, A.edificios, A.hunde + 1.5, 0.2, 0.5)
    elif t < A.invento:
        aleteo = 1.0                                # aplaude y las manos se le quedan pegadas
        tirit = 0.7 if t > A.pegar else 0.0
        mirar = (0.0, -0.8)
    elif t < 255:
        mirar = (0.6, -0.3)
    elif t < A.cinco_rb:
        mirar = (-0.8, 0.2)
        tirit = 0.3 if t > A.ser_vivo else 0.0
        boca = 0.0
    elif t < Z4[0]:
        mirar = (0.3, -0.8)
    else:
        feliz = 1.0 if t > A.regala else 0.0
        s *= 1 + 0.1 * campana(t, A.proxima, A.proxima + 2.2)
        mirar = (-0.8, -0.2)
    with S.en(lz, X, base + salto):
        P.kuri(lz, 0, 0, s, t, mirar=mirar, aleteo=aleteo, tiritar=tirit, feliz=feliz, boca=boca, voltear=voltear)
        if A.piezas - 0.4 < t < A.invento + 0.6 and t > A.tocan - 0.2:   # chispa de soldadura en frío entre las manos
            a = ventana(t, A.tocan - 0.1, A.invento, 0.1, 0.5)
            lz.halo(0, -205 * s, 60, (255, 236, 170), alfa=0.8 * a * (0.7 + 0.3 * math.sin(t * 20)))
            for k in range(6):
                ang = k / 6 * 2 * math.pi + t * 4
                lz.relleno(circulo(34 * math.cos(ang), -205 * s + 34 * math.sin(ang), 4, 8), (255, 240, 190), alfa=a)


# ======================================================================== la protagonista y la gente
def _fantasma_persona(lz, S, X, base, a, t, s=1.0):
    if a <= 0.01:
        return
    with S.en(lz, X, base, s):
        KO.fantasma(lz, 0, -185, 30, (255, 255, 255), alfa=0.7 * a, fase=t * 12, ancho=3)
        pts = np.array([[-30, -150], [30, -150], [34, -60], [20, 0], [-20, 0], [-34, -60]], float)
        P.discontinua(lz, np.vstack([pts, pts[:1]]), (255, 255, 255, int(180 * a)), 3, 12, 9, fase=t * 12)


def _dispersion(lz, S, X, base, t, t0, a=1.0, n=26, seed=0, alto=220):
    """Los átomos de O que se van del cuerpo: puntitos rojos que salen y se desvanecen."""
    u = t - t0
    if u <= 0 or u > 2.0:
        return
    for i in range(n):
        ang = h01(i, seed) * 2 * math.pi
        r = 30 + 160 * u * (0.5 + h01(i, seed + 3))
        X_ = X + math.cos(ang) * r
        H_ = base + alto * h01(i, seed + 5) + math.sin(ang) * r * 0.6
        x, y = S.pt(X_, H_)
        lz.relleno(circulo(x, y, 6 * S.k, 10), (255, 90, 100), alfa=a * (1 - u / 2.0))


def protagonista(lz, t, S, est):
    X = X_PROTA
    if not S.vis(X - 150, X + 150, -50, 300):
        return
    base = _base(X, est)
    brazos, piernas, emo = "idle", "idle", "neutro"
    lean = 0.0
    if t < A.imagina:
        brazos = "pecho"
        emo = "alegre"
    elif t < A.esfuma:
        emo = "neutro"
    elif t < A.oidos - 0.3:
        emo = "sorpresa"
    elif t < A.demasiado + 0.9:
        emo = "dolor"
        brazos = "defensa"
    elif t < A.uno_f:
        emo = "pensativo"
    elif t < A.dentro:
        emo = "sorpresa" if t > T_FUEGO else "neutro"
    elif t < A.vuelve_ra:
        emo = "cansado"
        lean = 0.1 * math.sin(t * 2.2) * est.get("mareo", 0.0)
    elif t < A.contrario + 0.6:
        emo = "dolor"
        brazos = "defensa"
    elif t < A.version_facil:
        emo = "alegre" if t > A.sobreviviriamos else "sorpresa"
    elif t < Z4[0]:
        emo = "sorpresa"
    else:
        emo = "alegre"
        brazos = "pecho" if A.proxima < t < A.miles else "idle"
    vida = est.get("vida", 1.0)
    if vida > 0.01:
        with S.en(lz, X, base):
            K2.cuerpo(lz, 0, 0, S_PERS, "mujer", t, piernas=piernas, brazos=brazos, mirar=1, vista="frente",
                      emocion=emo, seed=1, alfa=vida, lean=lean)
    if vida < 0.99:
        _fantasma_persona(lz, S, X, base, 1 - vida, t)
        _dispersion(lz, S, X, base, t, A.terceras_n - 0.2, seed=3)


def _ping(t, x0, x1, v, fase=0.0):
    L = x1 - x0
    u = (t * v / L + fase) % 2
    if u < 1:
        return x0 + L * u, 1
    return x1 - L * (u - 1), -1


def gente(lz, t, S, est):
    vr = est.get("vida_resto", 1.0)
    hund = est.get("hundir", 0.0)
    susto = ventana(t, A.choques, A.sobreviviriamos, 0.2, 0.3) if not est.get("normal") else 0.0
    ok = ventana(t, A.sobreviviriamos, A.version_facil + 1.0, 0.2, 0.4) if not est.get("normal") else 0.0
    # banco: hombre sentado (se desmaya un momento con el mareo)
    if S.vis(MP.X_BANCO - 120, MP.X_BANCO + 120, 0, 260):
        b = _base(MP.X_BANCO, est)
        des = 0.0 if est.get("normal") else ventana(t, A.desmayarse - 0.4, A.vuelve_ra + 0.6, 0.6, 0.8)
        if vr > 0.01:
            with S.en(lz, MP.X_BANCO - 10, b + 4):
                K2.cuerpo(lz, 0, 0, S_PERS * 0.95, "hombre", t, piernas="sentado", brazos="idle", mirar=1, vista="perfil",
                          emocion="cansado" if des > 0.3 else ("sorpresa" if susto > 0.3 else "neutro"), seed=4, alfa=vr,
                          lean=-0.55 * des)
        _fantasma_persona(lz, S, MP.X_BANCO - 10, b + 20, 1 - vr, t, 0.9)
    # quien cuida el asador
    Xa = MP.X_ASADOR - 110
    if S.vis(Xa - 120, Xa + 120, 0, 260):
        b = _base(Xa, est)
        if vr > 0.01:
            with S.en(lz, Xa, b):
                K2.cuerpo(lz, 0, 0, S_PERS, "senora", t, piernas="idle", brazos="carga" if t < T_FUEGO else "idle",
                          mirar=1, vista="perfil", emocion="sorpresa" if T_FUEGO < t < A.coches else "alegre", seed=6, alfa=vr)
        _fantasma_persona(lz, S, Xa, b, 1 - vr, t)
    # niño con perro junto al estanque
    Xn = -1290.0 + 30 * math.sin(t * 0.4)
    if S.vis(Xn - 300, Xn + 200, 0, 260):
        b = _base(Xn, est)
        if vr > 0.01:
            with S.en(lz, Xn, b):
                K2.cuerpo(lz, 0, 0, S_PERS * 0.75, "nino", t, piernas="idle", brazos="saluda" if (t % 7) < 2.5 else "idle",
                          mirar=-1, vista="frente", emocion="alegre", seed=8, alfa=vr)
            xp = Xn - 150 + 70 * math.sin(t * 0.9)
            with S.en(lz, xp, _base(xp, est)):
                KO.perro(lz, 0, 0, 0.9, t, dir=1 if math.cos(t * 0.9) > 0 else -1, corre=abs(math.cos(t * 0.9)))
        _fantasma_persona(lz, S, Xn, b, 1 - vr, t, 0.75)
    # corredor que va y viene por el parque
    xc, dc = _ping(t, -2250.0, -1050.0, 95.0, 0.3)
    if S.vis(xc - 100, xc + 100, 0, 260) and vr > 0.01:
        with S.en(lz, xc, _base(xc, est)):
            K2.cuerpo(lz, 0, 0, S_PERS, K2.variar("hombre", 5), t, piernas="corre", brazos="balanceo", mirar=dc,
                      vista="perfil", seed=5, alfa=vr, vel=0.9)
    # peatones del pueblo
    for i, (x0, x1, v, f, tipo) in enumerate(((20.0, 560.0, 70.0, 0.1, "mujer"), (420.0, 1300.0, 62.0, 0.6, "hombre"))):
        xp, dp = _ping(t, x0, x1, v, f)
        para = clamp01(prog(t, A.choques - 0.4, A.choques) * (1 - prog(t, A.version_facil, A.version_facil + 0.5)))
        if A.choques - 0.4 < t < Z4[0]:
            xp, dp = _ping(A.choques - 0.4, x0, x1, v, f)
        if not S.vis(xp - 100, xp + 100, 0, 260) or vr <= 0.01 or est.get("polvo", 0.0) > 0.4:
            continue
        with S.en(lz, xp, -10 - hund * 70):
            K2.cuerpo(lz, 0, 0, S_PERS * 0.95, K2.variar(tipo, 11 + i), t,
                      piernas="camina" if para < 0.5 else "idle", brazos="balanceo" if para < 0.5 else "arriba",
                      mirar=dp, vista="perfil", seed=11 + i, alfa=vr,
                      emocion="sorpresa" if susto > 0.3 else ("alegre" if ok > 0.3 else "neutro"))
        if susto > 0.02:
            x_, y_ = S.pt(xp, 300)
            P.pastilla(lz, x_, y_, "!", 46, k=pop(t, A.choques + 0.1 * i) * S.k * 1.2, fondo=(255, 236, 120),
                       color=(150, 40, 40), alfa=susto)
        if ok > 0.02:
            x_, y_ = S.pt(xp, 300)
            kk = pop(t, A.sobreviviriamos + 0.1 * i) * S.k * 1.2
            with lz.capa(2):
                lz.relleno(circulo(x_, y_, 34 * kk, 24), (110, 210, 140), alfa=ok)
                UB.check(lz, x_, y_ + 2 * kk, 16 * kk, (255, 255, 255), ok)
    protagonista(lz, t, S, est)
    kuri(lz, t, S, est)


# ======================================================================== aviones
def pos_jumbo(t):
    X = -1150 + 78 * (t - 80)
    Hh = 990 + 8 * math.sin(t * 0.7)
    if t > T_FUEGO:
        Hh -= 13 * (t - T_FUEGO)
    return X, Hh


def pos_avion2(t):
    X = -1750 + 84 * (t - 176)
    Hh = 820 - 10 * (t - 176)
    if t > A.motores_ra:
        Hh = 820 - 10 * (A.motores_ra - 176) + 14 * (t - A.motores_ra) ** 1.2
    return X, Hh


def avion_grande(lz, t, S, est):
    if est.get("normal") or t > B0:
        return
    X, Hh = pos_jumbo(t)
    if S.vis(X - 300, X + 300, Hh - 120, Hh + 120):
        rot = -0.02 if t < T_FUEGO else 0.06
        with S.en(lz, X, Hh, 0.8):
            KO.avion(lz, 0, 0, 1.0, t, motores=1.0 if t < T_FUEGO else 0.0, rot=rot, dir=1, estela=1.0 if t < T_FUEGO else 0.0,
                     luz=1.0)
    if A.brasas - 2 < t < B0:
        X, Hh = pos_avion2(t)
        if S.vis(X - 300, X + 300, Hh - 120, Hh + 120):
            m = e_out(prog(t, A.motores_ra - 0.2, A.motores_ra + 0.6))
            with S.en(lz, X, Hh, 0.7):
                KO.avion(lz, 0, 0, 1.0, t, motores=m, rot=0.06 - 0.12 * m, dir=1, estela=m, col=(250, 250, 255),
                         franja=(230, 90, 90), luz=1.0)
                if m > 0.01 and t < A.motores_ra + 1.2:
                    for ex, ey in ((-6, 30), (-48, 54)):
                        lz.halo(ex - 34, ey, 60, (255, 200, 120), alfa=0.9 * (1 - prog(t, A.motores_ra, A.motores_ra + 1.2)))


_LEJANOS = [(-3000, 3000, 160, 0.0), (-500, 3300, 140, 0.3), (2200, 2850, 180, 0.6), (5200, 3150, 150, 0.2), (-6000, 2900, 170, 0.8),
            (8000, 3200, 150, 0.5)]


def aviones_lejanos(lz, t, S, est):
    if est.get("b", 0.0) > 0.5 and not est.get("normal"):
        return
    Sl = S.par(0.35)
    apag = (not est.get("normal")) and t > T_FUEGO
    for i, (x0, h0, v, f) in enumerate(_LEJANOS):
        X = x0 + v * t
        Hh = h0 - (40 * (t - T_FUEGO) if apag else 0.0)
        x, y = Sl.pt(X, Hh)
        if not (-200 < x < 2120 and -100 < y < 1180):
            continue
        with Sl.en(lz, X, Hh, 0.9):
            KO.avion(lz, 0, 0, 1.0, t, motores=0.0 if apag else 1.0, rot=0.08 if apag else 0.0, col=(240, 244, 255),
                     franja=(120, 150, 210))
        # estela: si los motores se apagaron, la estela queda atrás y se deshace
        if not apag:
            xs_, ys_ = Sl.p(np.linspace(X - 1400, X - 260, 20), np.full(20, Hh + 30))
            lz.trazo(np.stack([xs_, ys_], 1), (255, 255, 255, 170), 9 * Sl.k, afinar=False)
        else:
            Xa = x0 + v * T_FUEGO
            a = 1 - prog(t, T_FUEGO, T_FUEGO + 14)
            xs_, ys_ = Sl.p(np.linspace(Xa - 1400, Xa - 260, 20), np.full(20, h0 + 30))
            lz.trazo(np.stack([xs_, ys_], 1), (255, 255, 255, int(170 * a)), 9 * Sl.k * (1 + 0.5 * (1 - a)), afinar=False)
