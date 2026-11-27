# -*- coding: utf-8 -*-
"""Kit LÍNEA 3D — espacio profundo (26-nov-2026, video `hera_dart_crater` de T Menos Cero).
Asteroides de alambre con cara oculta, luz del Sol en las líneas, cráteres, cara aplanada y rocas; naves DART y Hera;
cielo de estrellas; nube de eyección. Unidades libres (metros en los planos cercanos).

    import linea3d_espacio as E
    E.asteroide(lz, C, R, ejes=(1, 1, .66), rot=Rm, sol=(1, 0, 0), forma="huevo"|"trompo", crater=dir, aplanar=0.0, rocas=120)
    E.dart(lz, C, Rm, esc=1.0, rosa=1.0)      E.hera(lz, C, Rm, esc=1.0, alas=1.0)
    E.estrellas(lz, n=500)                     E.eyeccion(lz, P, dir, t, largo, ancho)
"""
import math

import cv2
import numpy as np

from linea3d import SS, base_de, circulo3d, clamp, nrm, rnd, rot_eje
from motor import H, W


def rot_ypr(yaw=0.0, pitch=0.0, roll=0.0):
    """Matriz de rotación (grados): z (yaw), luego y (pitch), luego x (roll)."""
    return rot_eje((0, 0, 1), math.radians(yaw)) @ rot_eje((0, 1, 0), math.radians(pitch)) @ rot_eje((1, 0, 0), math.radians(roll))


def _fill2d(lz, pts2, val=0.0):
    pts = np.round(np.asarray(pts2, np.float64) * SS * 16).astype(np.int32)
    cv2.fillPoly(lz.b, [pts], int(255 * val), cv2.LINE_AA, shift=4)


def _hull(lz, P):
    x, y, z = lz.cam.proy(np.asarray(P, np.float64).reshape(-1, 3))
    ok = np.isfinite(x) & np.isfinite(y)
    if ok.sum() < 3:
        return None
    pts = np.stack([x[ok], y[ok]], -1).astype(np.float32)
    pts = np.clip(pts, -4 * W, 5 * W)
    return cv2.convexHull(pts)[:, 0, :]


# ------------------------------------------------------------------ superficie de asteroide
_MALLAS = {}


def _malla(forma, ejes, semilla, crater, aplanar, nf, nl, crater_r=0.42, crater_prof=0.10):
    key = (forma, tuple(ejes), semilla, None if crater is None else tuple(np.round(crater, 3)), round(aplanar, 3), nf, nl,
           crater_r, crater_prof)
    if key in _MALLAS:
        return _MALLAS[key]
    phi = np.radians(np.linspace(-88, 88, nf))[:, None]
    lam = np.radians(np.linspace(-180, 180, nl))[None, :]
    U = np.stack([np.cos(phi) * np.cos(lam), np.cos(phi) * np.sin(lam), np.sin(phi) * np.ones_like(lam)], -1)
    if forma == "trompo":                              # Didymos: trompo con cresta ecuatorial (superelipse p < 2)
        p = 1.45
        c, s = np.abs(np.cos(phi)), np.abs(np.sin(phi))
        r = 1.0 / (c ** p + (s / 0.86) ** p) ** (1.0 / p)
        r = r * np.ones_like(lam)
    else:
        r = np.ones(U.shape[:2])
    # relieve: abolladuras suaves al azar (cráteres viejos) + ondulación
    rng = np.random.default_rng(semilla)
    for i in range(22):
        d = nrm(rng.normal(size=3))
        s = rng.uniform(0.03, 0.35)
        a = rng.uniform(0.02, 0.07) * (1 if i % 3 else -0.8)
        r = r - a * np.exp(-(1 - U @ d) / s)
    r = r * (1 + 0.025 * np.sin(3 * lam + semilla) * np.cos(2 * phi))
    P = U * r[..., None] * np.asarray(ejes, np.float64)
    if crater is not None:
        dc = nrm(crater)
        if aplanar > 0:                                # cara aplanada: se recorta contra un plano
            h = P @ dc
            hmax = h.max()
            lim = hmax - aplanar * hmax
            exc = np.clip(h - lim, 0, None)
            P = P - exc[..., None] * dc
        k = np.exp(-(1 - U @ dc) / (crater_r * crater_r * 0.5))   # hueco del cráter
        P = P - (k * crater_prof)[..., None] * dc * np.linalg.norm(ejes) / 1.7
    _MALLAS[key] = P
    return P


def asteroide(lz, C, R, ejes=(1, 1, 1), rot=None, sol=(1, 0.3, 0.2), forma="huevo", semilla=3, crater=None, aplanar=0.0,
              rocas=0, op=1.0, w=1.1, nf=31, nl=56, op_rej=0.6, ambiente=0.1, rellenar=True, crater_r=0.42, crater_prof=0.10,
              silueta=0.95):
    """Asteroide de alambre: rejilla deformada con cara oculta y la luz del Sol modulando las líneas (cara de noche tenue).
    `crater` = dirección LOCAL del cráter (dibuja borde); `aplanar` 0..0.3 = cara aplanada en esa dirección;
    `rocas` = nº de rocas (puntos) sobre la superficie. Devuelve la función local→mundo."""
    C = np.asarray(C, np.float64)
    Rm = np.eye(3) if rot is None else np.asarray(rot, np.float64)
    Pl = _malla(forma, ejes, semilla, crater, aplanar, nf, nl, crater_r, crater_prof)
    P = C + (Pl @ Rm.T) * R
    # normales por diferencias
    dphi = np.gradient(P, axis=0)
    dlam = np.gradient(P, axis=1)
    N = np.cross(dlam, dphi)
    out = np.sign(np.sum(N * (P - C), -1, keepdims=True))
    out[out == 0] = 1
    N = N * out
    N /= np.linalg.norm(N, axis=-1, keepdims=True) + 1e-12
    V = lz.cam.pos - P
    V /= np.linalg.norm(V, axis=-1, keepdims=True) + 1e-12
    vis = np.clip((np.sum(N * V, -1) + 0.02) / 0.12, 0, 1)
    luz = np.clip(N @ nrm(sol), 0, 1)
    brillo = ambiente + (1 - ambiente) * luz ** 0.8
    o = vis * brillo * op * op_rej
    hull = _hull(lz, P)
    if hull is None:
        return lambda q: C + (np.asarray(q) @ Rm.T) * R
    if rellenar:
        _fill2d(lz, hull, 0.0)
    lineas, ops = [], []
    for i in range(1, P.shape[0] - 1, 2):
        lineas.append(P[i]), ops.append(o[i])
    for i in range(2, P.shape[0] - 1, 2):
        lineas.append(P[i]), ops.append(o[i] * 0.35)
    for j in range(0, P.shape[1] - 1, 2):
        lineas.append(P[:, j]), ops.append(o[:, j])
    lz.lineas(lineas, ops, w=w * 0.8)
    # silueta (limbo) con brillo según el lado iluminado
    if silueta:
        lz.l2(np.vstack([hull, hull[:1]]), op * silueta * 0.9, w * 1.25)
    f = lambda q: C + (np.asarray(q, np.float64) @ Rm.T) * R
    if crater is not None:                              # borde del cráter: dos anillos en la cara aplanada
        dc = nrm(crater)
        h = Pl @ dc
        hmax = float(h.max())
        Uu = Pl / (np.linalg.norm(Pl, axis=-1, keepdims=True) + 1e-12)
        near = (Uu @ dc) > math.cos(crater_r * 1.1)
        rad = float(np.median(np.linalg.norm(Pl[near] - (Pl[near] @ dc)[:, None] * dc, axis=-1))) if near.any() else 0.5
        Nr = nrm(Rm @ dc)
        for k, (fr, prof, oo) in enumerate(((0.95, 0.0, 1.0), (0.55, crater_prof * 0.9, 0.6))):
            ring = f(circulo3d(dc * (hmax + 0.005 - prof * np.linalg.norm(ejes) / 1.7), dc, rad * fr, 72))
            cc = f(dc * hmax)
            vr = np.clip(((lz.cam.pos - cc) @ Nr) / (np.linalg.norm(lz.cam.pos - cc) + 1e-9) / 0.2 + 0.25, 0, 1)
            lz.linea(ring, vr * op * oo, w * (1.3 if k == 0 else 0.9), cerrada=True)
    if rocas:
        rr = np.random.default_rng(semilla + 99)
        ii = rr.integers(1, P.shape[0] - 1, rocas)
        jj = rr.integers(0, P.shape[1] - 1, rocas)
        sz = rr.uniform(0.6, 2.2, rocas)
        oo = o[ii, jj] / max(op_rej, 1e-6)
        for k in range(rocas):
            if oo[k] > 0.05:
                lz.puntos(P[ii[k], jj[k]] + N[ii[k], jj[k]] * R * 0.004, r=sz[k], op=min(1.0, oo[k] * 1.1))
    return f


# ------------------------------------------------------------------ cajas y naves
def caja(lz, C, Rm, dims, op=1.0, w=1.2, rellenar=True, op_atras=0.25):
    C = np.asarray(C, np.float64)
    dx, dy, dz = (np.asarray(dims, np.float64) / 2)
    sig = np.array([[sx, sy, sz] for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)], np.float64)
    V = C + (sig * [dx, dy, dz]) @ np.asarray(Rm).T
    if rellenar:
        hull = _hull(lz, V)
        if hull is not None:
            _fill2d(lz, hull, 0.0)
    # aristas: atrás tenues (la arista es trasera si sus dos caras miran lejos)
    caras = {}
    for ax in range(3):
        for s in (-1, 1):
            n = np.asarray(Rm)[:, ax] * s
            ctr = C + n * [dx, dy, dz][ax]
            caras[(ax, s)] = ((lz.cam.pos - ctr) @ n) > 0
    for i in range(8):
        for j in range(i + 1, 8):
            d = sig[i] != sig[j]
            if d.sum() != 1:
                continue
            ax_l = [k for k in range(3) if not d[k]]
            vis = any(caras[(k, int(sig[i][k]))] for k in ax_l)
            lz.linea(np.array([V[i], V[j]]), op if vis else op * op_atras, w)
    return V


def _panel(lz, P0, u, v, L, Wd, n_tiras, op, w):
    """Panel solar rectangular desde P0 a lo largo de u (largo L) y v (ancho Wd), con tiras."""
    A = P0 - v * Wd / 2
    pts = np.array([A, A + u * L, A + u * L + v * Wd, A + v * Wd])
    x, y, _ = lz.cam.proy(pts)
    if np.all(np.isfinite(x)):
        _fill2d(lz, np.stack([x, y], -1), 0.0)
    lz.linea(pts, op, w, cerrada=True)
    for k in range(1, n_tiras):
        f = k / n_tiras
        lz.linea(np.array([A + u * L * f, A + u * L * f + v * Wd]), op * 0.55, w * 0.7)
    lz.linea(np.array([A + v * Wd / 2, A + u * L + v * Wd / 2]), op * 0.35, w * 0.6)


def dart(lz, C, Rm, esc=1.0, rosa=1.0, op=1.0, w=1.2):
    """DART: cuerpo ~1,2 × 1,3 × 1,3 m, dos paneles ROSA que se desenrollan (8,5 m cada uno, `rosa` 0..1), antena plana,
    cámara DRACO al frente (+x) y motor iónico atrás. Frente = eje x local."""
    C = np.asarray(C, np.float64)
    Rm = np.asarray(Rm, np.float64)
    ex, ey, ez = Rm[:, 0], Rm[:, 1], Rm[:, 2]
    caja(lz, C, Rm, (1.25 * esc, 1.3 * esc, 1.3 * esc), op, w)
    # DRACO: tubo hacia +x
    tubo0 = C + ex * 0.62 * esc + ez * 0.25 * esc
    for k in range(2):
        lz.linea(circulo3d(tubo0 + ex * 0.45 * esc * k, ex, 0.17 * esc, 32), op * 0.9, w * 0.9, cerrada=True)
    for a in range(4):
        u, v = base_de(ex)
        d = (math.cos(a * math.pi / 2) * u + math.sin(a * math.pi / 2) * v) * 0.17 * esc
        lz.linea(np.array([tubo0 + d, tubo0 + d + ex * 0.45 * esc]), op * 0.6, w * 0.8)
    # antena plana (disco) en -z... en la cara -y? se pone en la cara +z inclinada
    lz.linea(circulo3d(C - ex * 0.1 * esc + ez * 0.66 * esc, ez, 0.45 * esc, 40), op * 0.8, w, cerrada=True)
    # motor iónico atrás
    lz.linea(circulo3d(C - ex * 0.66 * esc, ex, 0.22 * esc, 32), op * 0.8, w, cerrada=True)
    # ROSA: dos rollos a ±y
    for s in (-1, 1):
        base = C + ey * s * 0.68 * esc
        lz.linea(np.array([base, base + ey * s * 0.35 * esc]), op, w)
        L = max(0.05, 8.5 * rosa) * esc
        _panel(lz, base + ey * s * 0.35 * esc, ey * s, ex, L, 2.3 * esc, max(2, int(10 * rosa)), op, w * 0.9)
        # el rollo (cilindro) en la punta
        tip = base + ey * s * (0.35 * esc + L)
        lz.linea(np.array([tip - ex * 1.15 * esc, tip + ex * 1.15 * esc]), op, w * 2.2)
    return C


def hera(lz, C, Rm, esc=1.0, alas=1.0, op=1.0, w=1.2):
    """Hera: cuerpo ~1,6 × 1,6 × 1,7 m, dos alas solares de 3 paneles (`alas` 0..1 despliegue), antena parabólica arriba."""
    C = np.asarray(C, np.float64)
    Rm = np.asarray(Rm, np.float64)
    ex, ey, ez = Rm[:, 0], Rm[:, 1], Rm[:, 2]
    caja(lz, C, Rm, (1.6 * esc, 1.6 * esc, 1.7 * esc), op, w)
    # antena parabólica en +z
    c0 = C + ez * 0.85 * esc
    for k, (rr, hh) in enumerate(((0.56, 0.32), (0.4, 0.17), (0.2, 0.05))):
        lz.linea(circulo3d(c0 + ez * hh * esc, ez, rr * esc, 48), op * (1 if k == 0 else 0.5), w, cerrada=True)
    lz.linea(np.array([c0, c0 + ez * 0.55 * esc]), op * 0.7, w)
    # cámaras al frente (+x)
    lz.linea(circulo3d(C + ex * 0.82 * esc + ez * 0.3 * esc, ex, 0.12 * esc, 24), op * 0.9, w, cerrada=True)
    lz.linea(circulo3d(C + ex * 0.82 * esc - ez * 0.2 * esc + ey * 0.4 * esc, ex, 0.09 * esc, 24), op * 0.7, w, cerrada=True)
    for s in (-1, 1):
        base = C + ey * s * 0.8 * esc
        lz.linea(np.array([base, base + ey * s * 0.5 * esc]), op, w)
        x = 0.5 * esc
        for k in range(3):
            fk = clamp(alas * 3 - k)
            if fk <= 0:
                break
            _panel(lz, base + ey * s * (x), ey * s, ez, 1.55 * esc * fk, 1.25 * esc, 4, op, w * 0.9)
            x += 1.6 * esc
    return C


# ------------------------------------------------------------------ cielo y eyección
_EST = {}


def estrellas(lz, n=500, semilla=1, op=0.55, r=1.0):
    """Estrellas en direcciones fijas (sin paralaje): giran con la cámara."""
    if (n, semilla) not in _EST:
        rr = np.random.default_rng(semilla)
        U = rr.normal(size=(n, 3))
        U /= np.linalg.norm(U, axis=1, keepdims=True)
        _EST[(n, semilla)] = (U, rr.uniform(0.25, 1.0, n) ** 2, rr.uniform(0.5, 1.4, n))
    U, b, s = _EST[(n, semilla)]
    cam = lz.cam
    D = 1e7
    x, y, z = cam.proy(cam.pos + U * D)
    for xi, yi, bi, si in zip(x, y, b, s):
        if np.isfinite(xi) and 0 <= xi < W and 0 <= yi < H:
            cv2.circle(lz.b, (int(xi * SS * 16), int(yi * SS * 16)), max(1, int(r * si * SS * 16)), int(255 * clamp(op * bi)), -1,
                       cv2.LINE_AA, shift=4)


def eyeccion(lz, P, d, t, largo, ancho, n=260, op=1.0, semilla=5, w=1.0, abre=2.2, puntos=True, ritmo=1.2):
    """Nube de material expulsado: partículas que salen de P en un cono alrededor de d y se frenan (t en s desde el impacto)."""
    P = np.asarray(P, np.float64)
    d = nrm(d)
    u, v = base_de(d)
    for i in range(n):
        ang = rnd(i, semilla) * 2 * math.pi
        apert = (0.15 + abre * rnd(i, semilla + 1) ** 1.5) * 0.5
        dirp = nrm(d + (math.cos(ang) * u + math.sin(ang) * v) * apert)
        vel = 0.04 + 0.96 * rnd(i, semilla + 2) ** 1.6
        s = largo * vel * (1 - math.exp(-t * ritmo))
        p = P + dirp * s
        o = op * (0.35 + 0.65 * rnd(i, semilla + 3)) * clamp(1.2 - s / (largo * 1.1))
        if o <= 0.02:
            continue
        if puntos:
            lz.puntos(p, r=0.8 + 1.4 * rnd(i, semilla + 4), op=o)
        else:
            lz.linea(np.array([p, p - dirp * largo * 0.04]), o, w)
