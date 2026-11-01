# -*- coding: utf-8 -*-
"""PROFUNDIDAD del kit «grabado de peste» (docs/estilo_grabado_peste.md § «Profundidad»; 14-oct-2026). Lo que evita que una
lámina parezca «página web» (paneles planos sobre un fondo): un ESPACIO 3D real dibujado a buril.

  cam = Camara(x, y, z, guinada, cabeceo, f, foco, apertura, bruma, lejos)    mundo: x derecha, y ABAJO (suelo y=0), z fondo
  plano(g, cam, O, U, V, au, av, tono, familias, patron, luces)  suelo / muro / techo con trama EN PERSPECTIVA (las líneas
        convergen al punto de fuga, se afinan con la distancia y se funden en tono antes de hacer moiré); losas y sillares
        procedurales; charcos de luz 3D (velas, fraguas, luna) sobre la superficie.
  sx, sy, zc = cam.pt(X, Y, Z); k = cam.k(zc)     poner una figura del kit en el mundo (tamaño = tamaño_mundo * k)
  with capa_prof(g, cam, zc) as c: ...            capa con profundidad de campo (desenfoque) y bruma de lejanía por distancia
  sombra_contacto · sombra_capa (sombra proyectada de una figura por una luz) · trazo3d (rejas, vigas, telarañas)
  iluminar (claroscuro grabado: lo que no toca la luz se hunde en trama) · haz (haz de luz con polvo) · particulas · humo
  estampar (pega un lienzo transparente en perspectiva sobre un cuadrilátero, con sombra arrojada: cuadros, pergaminos)
  pegatina (WoW REAL: render o recorte PNG como recorte de papel de pie en el mundo, pasado a la estampa; 15-oct-2026)
"""
import functools
import math

import cv2
import numpy as np

import grabado as GR
from grabado import (G, H, ORO, PAPEL, TINTA, W, _lineas, _rejilla, capa, clamp, componer, grabar_imagen, lerp,  # noqa: F401
                     rnd, smooth, tramado)


# ------------------------------------------------------------------ cámara
class Camara:
    """Cámara de perspectiva. `guinada` (grados, + mira a la derecha), `cabeceo` (grados, + mira hacia abajo), `f` = focal en
    px (1500 ≈ 65° de campo horizontal), `foco` = distancia nítida, `apertura` = cuánto se desenfoca lo que está lejos del foco
    (0 = todo nítido; 6-14 = cine), `bruma` 0..1 y `lejos` = distancia a la que la bruma llega a ~63 %."""

    def __init__(self, x=0.0, y=-160.0, z=0.0, guinada=0.0, cabeceo=0.0, f=1500.0, foco=900.0, apertura=0.0, bruma=0.0,
                 lejos=3000.0, cerca=8.0):
        self.C = np.float32((x, y, z))
        self.f, self.foco, self.apertura, self.bruma, self.lejos, self.cerca = f, foco, apertura, bruma, lejos, cerca
        yw, pt = math.radians(guinada), math.radians(cabeceo)
        self.F = np.float32((math.sin(yw) * math.cos(pt), math.sin(pt), math.cos(yw) * math.cos(pt)))
        self.R = np.float32((math.cos(yw), 0.0, -math.sin(yw)))
        self.D = np.cross(self.F, self.R).astype(np.float32)
        self.cx, self.cy = W / 2, H / 2

    def cam(self, P):
        d = np.asarray(P, np.float32) - self.C
        return np.stack([d @ self.R, d @ self.D, d @ self.F], -1)

    def pt(self, x, y, z):
        """Punto del mundo -> (x, y) de pantalla y profundidad zc."""
        c = self.cam((x, y, z))
        zc = max(float(c[2]), 1e-3)
        return self.cx + self.f * float(c[0]) / zc, self.cy + self.f * float(c[1]) / zc, float(c[2])

    def k(self, zc):
        """Escala de pantalla a esa profundidad (px por unidad del mundo)."""
        return self.f / max(zc, 1e-3)

    def sigma(self, zc):
        return float(min(18.0, self.apertura * abs(1.0 / max(zc, 1.0) - 1.0 / self.foco) * self.foco))

    def niebla(self, zc):
        return float(clamp(self.bruma * (1.0 - math.exp(-max(zc, 0.0) / self.lejos))))

    def horizonte(self):
        return self.cy - self.f * self.F[1] / max(math.hypot(self.F[0], self.F[2]), 1e-3)


def kf_camara(t, kfs, **fijos):
    """Cámara interpolada (suave) entre fotogramas clave [(t, dict(x=, y=, z=, guinada=, cabeceo=, f=, foco=)), ...]."""
    if t <= kfs[0][0]:
        p = dict(kfs[0][1])
    elif t >= kfs[-1][0]:
        p = dict(kfs[-1][1])
    else:
        for (t0, a), (t1, b) in zip(kfs, kfs[1:]):
            if t0 <= t <= t1:
                u = smooth((t - t0) / max(t1 - t0, 1e-6))
                p = {k: lerp(a[k], b.get(k, a[k]), u) for k in a}
                break
    p.update(fijos)
    return Camara(**p)


def firma_lejos(cam, paralaje=0.3):
    """Firma (px) de lo que depende del FONDO LEJANO (cielo, luna, nubes, colinas del horizonte) para GR.fondo: horizonte,
    giro y el paralaje en pantalla (`paralaje` px por unidad que se mueve la cámara de lado)."""
    return (cam.horizonte(), cam.f * math.atan2(float(cam.F[0]), float(cam.F[2])), paralaje * float(cam.C[0]))


def firma_cerca(cam, zmin=400.0):
    """Firma (px) de superficies 3D cuyo punto más cercano está a `zmin` (suelo, muros) para GR.fondo: cuánto se mueve en
    pantalla al trasladar o girar la cámara. Con cámara quieta no cambia: muros y suelos se dibujan una vez por tick."""
    e = GR.FONDO_TOL / 0.75                              # lo cercano solo tolera ~0,75 px (los pies no resbalan)
    k = cam.f / zmin * e
    return tuple(float(v) * k for v in cam.C) + tuple(float(v) * cam.f * e for v in cam.F) + (cam.f * e,)


# ------------------------------------------------------------------ proyección con recorte en el plano cercano
def _recorte_cerca(Pc, cerca, cerrado=True):
    out = []
    n = len(Pc)
    for i in range(n if cerrado else n - 1):
        A, B = Pc[i], Pc[(i + 1) % n]
        ia, ib = A[2] >= cerca, B[2] >= cerca
        if ia:
            out.append(A)
        if ia != ib:
            u = (cerca - A[2]) / (B[2] - A[2])
            out.append(A + (B - A) * u)
    if not cerrado and Pc[-1][2] >= cerca:
        out.append(Pc[-1])
    return np.float32(out) if len(out) >= (3 if cerrado else 2) else None


def proyectar(cam, P3, cerrado=True):
    """Polígono (o polilínea) 3D -> pantalla, recortado en el plano cercano. Devuelve (pts Nx2, zc N) o (None, None)."""
    Pc = _recorte_cerca(cam.cam(np.asarray(P3, np.float32)), cam.cerca, cerrado)
    if Pc is None:
        return None, None
    z = np.maximum(Pc[:, 2], 1e-3)
    return np.stack([cam.cx + cam.f * Pc[:, 0] / z, cam.cy + cam.f * Pc[:, 1] / z], 1).astype(np.float32), z


def _hash(a, b):
    x = np.sin(a * 127.1 + b * 311.7) * 43758.5453
    return x - np.floor(x)


# ------------------------------------------------------------------ superficies en perspectiva
def plano(g, cam, O, U, V, au, av, tono=0.5, familias=((0.0, 9.0),), patron=None, luces=(), oscuro=0.0, op=1.0,
          color=TINTA, papel=True, vibra=1.0, niebla=True, junta=3.0, var=0.12, contorno=0.0, quiebre=0.0, tramo=40.0):
    """Superficie rectangular del mundo (origen O, ejes unitarios U, V; medidas au x av) con trama en perspectiva.
    tono: número o f(a, b, zc) -> array (a, b = coordenadas sobre el plano). familias: [(ángulo en el plano, periodo en
    unidades del mundo), ...] (la 1.ª carga el tono; las demás cruzan las sombras). `quiebre` 0..1 corta las líneas en
    tramos de `tramo` unidades (piedra tallada, tierra: sin él, un muro parece persiana). patron: None · ("losas", lado) ·
    ("sillares", largo, alto) -> juntas en perspectiva + tono distinto por pieza (`var`). luces: [(x, y, z, radio, fuerza)]
    aclaran la superficie con caída 3D; `oscuro` = tono que se suma donde NO llega la luz."""
    O, U, V = np.float32(O), np.float32(U), np.float32(V)
    esq = np.float32([O, O + U * au, O + U * au + V * av, O + V * av])
    scr, _ = proyectar(cam, esq)
    if scr is None:
        return
    m, bb = (g.papel(scr, op) if papel else g._mascara(scr))
    if m is None:
        return
    x0, y0, x1, y1 = bb
    if x1 - x0 < 3 or y1 - y0 < 3:                       # superficie vista de canto (tira de 1-2 px): ya quedó el papel
        return
    gx, gy = _rejilla(x1 - x0, y1 - y0)
    xs = (gx + (x0 - cam.cx)) / cam.f
    ys = (gy + (y0 - cam.cy)) / cam.f
    N = np.cross(U, V)
    CO = cam.C - O

    def dot3(v):
        return float(cam.R @ v) * xs + float(cam.D @ v) * ys + float(cam.F @ v)
    dn = dot3(N)
    dn = np.where(np.abs(dn) < 1e-6, 1e-6, dn)
    tt = float(-(CO @ N)) / dn
    tt = np.where(tt > 0, tt, 1e6).astype(np.float32)
    a = float(CO @ U) + tt * dot3(U)
    b = float(CO @ V) + tt * dot3(V)
    T = tono(a, b, tt) if callable(tono) else np.full(a.shape, float(tono), np.float32)
    T = np.asarray(T, np.float32)
    jun = None
    if patron:
        if patron[0] == "losas":
            L = float(patron[1])
            ua, ub = a / L, b / L
            T = T + var * (_hash(np.floor(ua), np.floor(ub)) - 0.5)
        else:
            L, h = float(patron[1]), float(patron[2])
            ub = b / h
            fila = np.floor(ub)
            ua = (a + (fila % 2) * L * 0.5) / L
            T = T + var * (_hash(np.floor(ua), fila) - 0.5)
        jun = []
        for u in (ua, ub):
            gy_, gx_ = np.gradient(u)
            pp = 1.0 / np.maximum(np.sqrt(gx_ * gx_ + gy_ * gy_), 1e-4)
            per_w = L if u is ua else (float(patron[2]) if patron[0] == "sillares" else L)
            anc = np.float32(junta / per_w)
            c = _lineas(u, pp, anc)
            jun.append(c * np.clip((pp - 3.0) / 3.0, 0, 1) + anc * (1 - np.clip((pp - 3.0) / 3.0, 0, 1)))
    if luces:
        dx_, dy_, dz_ = [cam.R[i] * xs + cam.D[i] * ys + cam.F[i] for i in range(3)]
        hx, hy, hz = cam.C[0] + tt * dx_, cam.C[1] + tt * dy_, cam.C[2] + tt * dz_
        Lz = np.zeros_like(T)
        for (lx, ly, lz, rad, fz) in luces:
            d = np.sqrt((hx - lx) ** 2 + (hy - ly) ** 2 + (hz - lz) ** 2) / rad
            Lz += fz * np.clip(1 - d, 0, 1) ** 1.5
        Lz = np.clip(Lz, 0, 1)
        T = T * (1 - 0.85 * Lz) + oscuro * (1 - Lz)
    if niebla and cam.bruma > 0:
        T = T * (1 - cam.bruma * (1 - np.exp(-tt / cam.lejos)))
    T = np.clip(T, 0, 1)
    ph1, ph2 = rnd(int(O[0] + 3 * O[2]), 11) * 6.2832, rnd(int(O[1]), 12) * 6.2832   # fijas: la superficie NO hierve
    cov = np.zeros_like(T)
    for i, (ang, per) in enumerate(familias):
        r = math.radians(ang)
        u = (a * math.cos(r + math.pi / 2) + b * math.sin(r + math.pi / 2)) / per
        v = (-a * math.sin(r + math.pi / 2) + b * math.cos(r + math.pi / 2)) / per
        u = u + vibra * (0.06 * np.sin(v / 10.0 + ph1 + i) + 0.028 * np.sin(v / 2.7 + ph2))
        gy_, gx_ = np.gradient(u)
        pp = 1.0 / np.maximum(np.sqrt(gx_ * gx_ + gy_ * gy_), 1e-4)
        if len(familias) == 1:
            anc = T * 0.94
        elif i == 0:
            anc = np.clip(T / 0.62, 0, 1) * 0.62
        elif i == 1:
            anc = np.clip((T - 0.60) / 0.35, 0, 1) * 0.26
        else:
            anc = np.clip((T - 0.78) / 0.18, 0, 1) * 0.45
        nit = np.clip((pp - 3.0) / 3.0, 0, 1)                    # a lo lejos: tono plano en vez de moiré
        if quiebre > 0:                                          # trazo QUEBRADO (piedra tallada): cortes al azar, y cada
            lid = np.floor(u + 0.5)                              # tramo se afila en punta como un golpe de buril
            w_ = v * per / tramo + 0.37 * lid
            fr = w_ - np.floor(w_)
            vivo = (_hash(lid + 17.0 * i, np.floor(w_)) > quiebre * (1.0 - 0.6 * T)).astype(np.float32)
            anc = anc * vivo * np.clip(np.minimum(fr, 1.0 - fr) * 5.0, 0.0, 1.0) ** 0.6
        c = _lineas(u, pp, anc) * nit + anc * (1 - nit)
        cov = 1 - (1 - cov) * (1 - c)
    cov = np.maximum(cov, np.clip((T - 0.95) / 0.05, 0, 1))
    if jun is not None:
        for c in jun:
            cov = 1 - (1 - cov) * (1 - c)
    cov = cov * (tt < 1e5)
    g._blend(m.astype(np.float32) * cov, x0, y0, color, op)
    if contorno:
        g.trazo(scr, contorno, cerrado=True, afilado=0.0, op=op)


def trazo3d(g, cam, P3, w=3.0, color=TINTA, op=1.0, cerrado=False, afilado=0.5, temblor=1.0, sem=0, densidad=12):
    """Polilínea del mundo (reja, viga, telaraña) con ancho en unidades del mundo: engorda al acercarse."""
    P3 = np.asarray(P3, np.float32)
    if cerrado:
        P3 = np.vstack([P3, P3[:1]])
    sub = [P3[0]]
    for A, B in zip(P3, P3[1:]):
        for u in np.linspace(0, 1, densidad + 1)[1:]:
            sub.append(A + (B - A) * u)
    scr, z = proyectar(cam, np.float32(sub), cerrado=False)
    if scr is None:
        return
    g.trazo(scr, anchos=w * cam.f / z, color=color, op=op, afilado=afilado, temblor=temblor, sem=sem)


def capa_prof(g, cam, zc, extra=0.0, bruma=True, op=1.0):
    """Capa para figuras a profundidad zc: desenfoque de cámara + bruma de lejanía."""
    return capa(g, desenfoque=cam.sigma(zc) + extra, bruma=cam.niebla(zc) if bruma else 0.0, op=op)


def sombra_contacto(g, cam, X, Z, rx, rz=None, op=0.85, tono=0.85, Y=0.0):
    """Sombra de contacto en el suelo bajo una figura (asienta los pies: nada flota)."""
    rz = rz or rx * 0.6
    for f, tn, o in ((1.35, tono * 0.55, 0.7), (1.0, tono, 1.0)):
        a = np.linspace(0, 2 * np.pi, 28, endpoint=False)
        P3 = np.stack([X + rx * f * np.cos(a), np.full_like(a, Y), Z + rz * f * np.sin(a)], 1)
        scr, _ = proyectar(cam, P3)
        if scr is not None:
            g.trama(scr, tn, ang=8, per=4.2, cruz=False, op=op * o)


def nueva_capa(g):
    """Capa transparente manual (para sombra_capa + componer)."""
    c = G(g.t, g.W, g.H, g.fondo_papel, alfa=True, k=g.k)
    c.s, c.ox, c.oy, c.rec = g.s, g.ox, g.oy, g.rec
    return c


def sombra_capa(g, c, pie, dirx=0.0, diry=0.5, largo=1.0, op=0.75, tono=0.9, desenfoque=1.5, ang=12.0, per=4.6):
    """Sombra PROYECTADA de lo dibujado en la capa `c` sobre el suelo de `g`: la silueta se tumba desde `pie` (x, y de
    pantalla) en la dirección (dirx, diry) — alejándose de la luz — y se graba como trama. Llamar ANTES de componer `c`."""
    px, py = pie
    L = largo
    M = np.float32([[1.0, -dirx * L, dirx * L * py], [0.0, -diry * L, py * (1 + diry * L)]])
    S = cv2.warpAffine(c.alfa, M, (g.W, g.H), flags=cv2.INTER_LINEAR, borderValue=0)
    if desenfoque > 0.3:
        S = cv2.GaussianBlur(S, (0, 0), desenfoque)
    ys, xs = np.nonzero(S > 0.02)
    if len(ys) == 0:
        return
    y0, y1, x0, x1 = ys.min(), ys.max() + 1, xs.min(), xs.max() + 1
    s = S[y0:y1, x0:x1]
    gx, gy = _rejilla(x1 - x0, y1 - y0)
    cov = tramado(s * tono, gx + x0, gy + y0, 1.0, ang, per, "lineal", False, g.k)
    g._blend(cov * 255.0, x0, y0, TINTA, op)


# ------------------------------------------------------------------ luz y atmósfera
def iluminar(g, luces, amb=0.2, fuerza=0.8, acento=0.0, engorde=2, lavado=0.5):
    """CLAROSCURO sobre el cuadro entero: lo que no toca ninguna luz se oscurece ENGORDANDO la tinta que ya hay (filtro de
    mínimo) y con un lavado de tono (aguatinta). NO añade líneas nuevas: una trama fija en pantalla encima de superficies en
    perspectiva hace moiré que «nada» con la cámara y marea (el usuario, 14-oct-2026).
    luces: [(x, y, radio, fuerza[, color])] en pantalla (proyecta las 3D con cam.pt). `acento` > 0 tiñe el halo de cada luz
    con su color en la plancha de color."""
    gx, gy = _rejilla(g.W, g.H)
    L = np.full((g.H, g.W), amb, np.float32)
    for lz in luces:
        x, y, r, k = lz[:4]
        d = np.sqrt((gx - x) ** 2 + ((gy - y) * 1.15) ** 2) / r
        L += k * np.clip(1 - d, 0, 1) ** 1.6
        if acento > 0 and len(lz) > 4:
            g.acento_luz(x, y, r * 0.7, lz[4], acento * k)
    D = (fuerza * (1 - np.clip(L, 0, 1)))[..., None]
    er = g.im
    for _ in range(engorde):
        er = cv2.erode(er, np.ones((3, 3), np.uint8))
    g.im = g.im * (1 - D) + er * D
    g.im *= 1 - lavado * D


def haz(g, x, y, ang, abertura, largo, t, op=0.35, n=170, color=None, polvo=True):
    """Haz de luz grabado (luna por una ventana, fragua por un arco): rayos finos de papel que se abren desde (x, y) en la
    dirección `ang` (grados), con bandas que respiran y polvo que pasa."""
    a0 = math.radians(ang)
    ab = math.radians(abertura)
    pts = [(x, y)] + [(x + largo * math.cos(a0 + u), y + largo * math.sin(a0 + u)) for u in np.linspace(-ab / 2, ab / 2, 9)]
    bb = g._bb(np.float32(pts), pad=4)
    if bb is None or op <= 0.004:
        return
    x0, y0, x1, y1 = bb
    gx, gy = _rejilla(x1 - x0, y1 - y0)
    dx, dy = gx + (x0 - x), gy + (y0 - y)
    rho = np.sqrt(dx * dx + dy * dy)
    th = np.arctan2(dy, dx) - a0
    th = (th + np.pi) % (2 * np.pi) - np.pi
    cono = np.clip((ab / 2 - np.abs(th)) / (ab * 0.3), 0, 1) * np.clip(1 - rho / largo, 0, 1) ** 1.2 * np.clip(rho / 40, 0, 1)
    u = th * (n / 6.2832) + 0.12 * np.sin(rho / 80.0 - t * 0.9)
    pp = np.maximum(rho * 6.2832 / n, 1.5)
    banda = 0.55 + 0.45 * np.sin(th * 9 + t * 0.5) * np.sin(th * 4.3 - t * 0.33)
    ray = _lineas(u, pp, np.clip(0.25 + 0.35 * banda, 0, 1))
    A = cono * (0.30 + 0.70 * ray) * op
    reg = g.im[y0:y1, x0:x1]
    col = np.float32(color or g.fondo_papel)
    reg *= 1 - A[..., None]
    reg += A[..., None] * col
    if polvo:
        for i in range(int(40 * op / 0.35)):
            r = largo * (0.1 + 0.85 * ((rnd(i, 300) + t * (0.02 + 0.03 * rnd(i, 301))) % 1.0))
            aa = a0 + (rnd(i, 302) - 0.5) * ab * 0.9 + 0.05 * math.sin(t * 0.7 + i)
            px, py = x + r * math.cos(aa), y + r * math.sin(aa)
            tw = 0.5 + 0.5 * math.sin(t * (1.5 + rnd(i, 303) * 3) + i)
            g.circ(px, py, 0.8 + 1.8 * rnd(i, 304), col, op * 1.6 * tw * (1 - r / largo))


def particulas(g, t, tipo="polvo", n=60, caja=(0, 0, W, H), sem=0, op=1.0, escala=1.0, color=None):
    """Partículas con profundidad (cada una con su z: tamaño, velocidad y opacidad): polvo (motas de papel que flotan),
    ceniza (copos de tinta que caen), brasas (chispas de color que suben), nieve, esporas (de la plaga)."""
    x0, y0, x1, y1 = caja
    w, h = x1 - x0, y1 - y0
    for i in range(n):
        z = 0.35 + 0.65 * rnd(i, sem + 400)
        tw = 0.6 + 0.4 * math.sin(t * (1 + 2 * rnd(i, sem + 401)) + i)
        if tipo in ("nieve", "ceniza"):
            vy, vx = (22 + 50 * z) * (1 if tipo == "nieve" else 0.6), 8 * math.sin(t * 0.7 + i)
        elif tipo in ("brasas", "esporas"):
            vy, vx = -(30 + 70 * z) * (1 if tipo == "brasas" else 0.35), 12 * math.sin(t * 1.3 + i * 0.7)
        else:
            vy, vx = -4 * z, 6 * math.sin(t * 0.3 + i)
        px = x0 + (rnd(i, sem + 402) * w + vx + t * (3 + 9 * z) * (1 if i % 2 else -1)) % w
        py = y0 + (rnd(i, sem + 403) * h + vy * t) % h
        r = escala * (0.7 + 2.6 * z * rnd(i, sem + 404))
        if tipo == "ceniza":
            g.elip(px, py, r * 1.6, r * 0.7, color or TINTA, op * 0.8 * tw, ang=(t * 40 + i * 37) % 180)
        elif tipo == "brasas":
            vida = 1 - ((py - y0) / h) ** 2 if vy < 0 else 1
            g.circ(px, py, r * 0.9, g.fondo_papel, op * tw * (1 - vida * 0.3))
            g.acento_luz(px, py, r * 4, color or ORO, 0.9 * op * tw)
        elif tipo == "esporas":
            g.circ(px, py, r, color or (0.47, 0.62, 0.12), 0.75 * op * tw)
        else:
            g.circ(px, py, r, color or g.fondo_papel, op * 0.85 * tw)


def humo(g, x, y, s, t, sem=0, op=0.7, color=TINTA, alto=260, hebras=3):
    """Humo grabado (vela, incienso, ruinas): hebras que suben ondulando, se rizan y se desvanecen."""
    for j in range(hebras):
        pts = []
        for i in range(30):
            u = i / 29
            yy = y - u * alto * s
            amp = s * (6 + 34 * u ** 1.2)
            xx = x + s * 10 * u * (j - 1) + amp * math.sin(u * 7.5 - t * 1.7 + j * 2.1 + sem)
            pts.append((xx, yy))
        pts = np.float32(pts)
        for q, (i0, i1) in enumerate(((0, 12), (11, 21), (20, 30))):
            g.trazo(pts[i0:i1], (2.0 - 0.4 * q) * s ** 0.5, color=color, op=op * (1 - 0.32 * q), afilado=0.7, temblor=0.6,
                    sem=j * 3 + q)
        cx, cy = pts[22]
        a = np.linspace(0, 4.5, 14) + t * 0.8 + j
        rr = s * np.linspace(10, 2, 14)
        g.trazo(np.stack([cx + rr * np.cos(a), cy + rr * np.sin(a)], 1), 1.3 * s ** 0.5, color=color, op=op * 0.5,
                afilado=0.8)


def estampar(g, sub, quad, sombra=0.45, off=(14, 20), desenfoque_sombra=12.0, op=1.0):
    """Pega el lienzo transparente `sub` (G con alfa) sobre el cuadrilátero `quad` de pantalla (sup-izq, sup-der, inf-der,
    inf-izq), en perspectiva, con sombra arrojada: un cuadro colgado, un pergamino clavado, un cartel."""
    h, w = sub.H, sub.W
    dst = np.float32(quad)
    pad = int(abs(off[0]) + abs(off[1]) + 3 * desenfoque_sombra) + 4
    x0, y0 = max(0, int(dst[:, 0].min()) - pad), max(0, int(dst[:, 1].min()) - pad)
    x1, y1 = min(g.W, int(dst[:, 0].max()) + pad), min(g.H, int(dst[:, 1].max()) + pad)
    if x1 - x0 < 4 or y1 - y0 < 4:
        return
    M = cv2.getPerspectiveTransform(np.float32([(0, 0), (w, 0), (w, h), (0, h)]), dst - np.float32((x0, y0)))
    sz = (x1 - x0, y1 - y0)
    im = cv2.warpPerspective(sub.im, M, sz, flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0))
    A = cv2.warpPerspective(sub.alfa, M, sz, flags=cv2.INTER_LINEAR, borderValue=0) * op
    ac = cv2.warpPerspective(sub.ac, M, sz, flags=cv2.INTER_LINEAR, borderValue=(1, 1, 1))
    reg = g.im[y0:y1, x0:x1]
    if sombra > 0:
        S = cv2.GaussianBlur(A, (0, 0), desenfoque_sombra)
        S = np.roll(S, (int(off[1]), int(off[0])), axis=(0, 1))
        reg *= 1 - (sombra * S)[..., None]
    reg *= 1 - A[..., None]
    reg += im * op
    rac = g.ac[y0:y1, x0:x1]
    rac *= 1 - A[..., None]
    rac += ac * A[..., None]
    if g.alfa is not None:
        ra = g.alfa[y0:y1, x0:x1]
        ra *= 1 - A
        ra += A


# ------------------------------------------------------------------ WoW REAL: pegatinas de papel de pie en el mundo
_RGBA = {}


def _rgba(fuente):
    """Ruta de PNG (o array RGBA uint8) -> float32 RGBA 0..1, cacheado por ruta."""
    if not isinstance(fuente, str):
        return np.asarray(fuente, np.float32) / 255.0
    if fuente not in _RGBA:
        from PIL import Image
        _RGBA[fuente] = np.asarray(Image.open(fuente).convert("RGBA"), np.float32) / 255.0
    return _RGBA[fuente]


@functools.lru_cache(maxsize=256)
def _estampa_png(fuente, alto_px, tinta, color, borde, k, espejo, sem):
    rgba = _rgba(fuente)
    h, w = rgba.shape[:2]
    s = alto_px / float(h)
    nw, nh = max(4, int(round(w * s))), max(4, int(round(h * s)))
    im = cv2.resize(rgba, (nw, nh), interpolation=cv2.INTER_AREA if s < 1 else cv2.INTER_CUBIC)
    if espejo:
        im = im[:, ::-1]
    pad = int(borde) + 4
    im = np.pad(np.clip(im, 0, 1), ((pad, pad), (pad, pad), (0, 0)))
    H2, W2 = im.shape[:2]
    a = im[..., 3]
    rgb = im[..., :3]
    fig = (a > 0.45).astype(np.uint8)
    # ---- figura pasada a la estampa: duotono al centro y grabado de líneas hacia su contorno (como los «recuerdos»)
    lum = rgb.mean(2)
    dentro = lum[a > 0.5]
    lo, hi = (float(np.percentile(dentro, 2)), float(np.percentile(dentro, 96))) if dentro.size > 20 else (0.0, 1.0)
    sobre = rgb * a[..., None] + np.float32(PAPEL) * (1 - a[..., None])
    dist = cv2.distanceTransform(fig, cv2.DIST_L2, 5)
    mapa = np.clip(tinta + (1 - tinta) * (1 - np.clip(dist / max(0.10 * nh, 4.0), 0, 1)) ** 1.4, 0, 1)
    est = grabar_imagen((sobre * 255).astype(np.uint8), W2, H2, lo, hi, mapa, per=4.2 if nh > 260 else 3.6, ang=30.0, k=k,
                        gamma=0.62, contornos=0.8)
    # ---- contorno de buril alrededor de la silueta
    wl = max(1.2, nh / 200.0)
    ker = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * int(wl) + 1, 2 * int(wl) + 1))
    aa = np.clip(cv2.GaussianBlur(a, (0, 0), 0.6), 0, 1)
    linea = np.clip(cv2.dilate(aa, ker) - cv2.erode(aa, ker), 0, 1) * 0.9
    # ---- recorte de papel (borde con filo irregular, como cortado a tijera) y su filo de tinta
    if borde > 0:
        fuera = cv2.distanceTransform(1 - fig, cv2.DIST_L2, 5)
        rng = np.random.default_rng(700 + sem)
        ru = cv2.resize(rng.random((max(2, H2 // 40), max(2, W2 // 40))).astype(np.float32), (W2, H2),
                        interpolation=cv2.INTER_CUBIC)
        lim = borde * (0.75 + 0.5 * ru)
        pap = np.clip(lim - fuera + 0.5, 0, 1)
        pap = cv2.GaussianBlur(pap, (0, 0), 0.7)
        filo = np.clip(1 - np.abs(lim - fuera) / 1.1, 0, 1) * (fuera > 0.5) * 0.8
    else:
        pap = np.zeros_like(a)
        filo = pap
    A = np.maximum(pap, aa)
    col = np.float32(PAPEL) * 1.03 * (1 - aa[..., None]) + est * aa[..., None]
    col = col * (1 - linea[..., None]) + np.float32(TINTA) * linea[..., None]
    col = col * (1 - filo[..., None]) + np.float32(TINTA) * filo[..., None]
    A = np.maximum(A, filo)
    # ---- plancha de color «iluminada a mano»: solo el TONO real (el rojo de Hakkar, el verde de un troll), sin su valor
    mx = np.maximum(rgb.max(2, keepdims=True), 1e-3)
    tono = np.clip(rgb / mx, 0, 1)
    sat = np.clip((mx[..., 0] - rgb.min(2)) / mx[..., 0] * 1.6, 0, 1)
    f = cv2.GaussianBlur((color * sat * aa).astype(np.float32), (0, 0), 1.5)[..., None]
    ac = 1.0 - f * (1.0 - cv2.GaussianBlur(tono, (0, 0), 1.5))
    return (col * A[..., None]).astype(np.float32), A.astype(np.float32), ac.astype(np.float32)


def pegatina(g, cam, fuente, X, Z, alto, t, Y=0.0, tinta=0.35, color=0.8, borde=None, alza=1.0, giro=0.0, aleteo=1.0,
             sombra=0.35, contacto=0.8, op=1.0, sem=0, espejo=False):
    """Personaje u objeto REAL de WoW (render oficial o recorte de un clip, PNG con alfa) como RECORTE DE PAPEL DE PIE en
    el mundo, a su profundidad: mira a la cámara, se mece un poco (`aleteo`), lleva sombra de contacto en el suelo y su
    sombra de cartón. La imagen se pasa a la estampa (duotono + líneas hacia el contorno + buril) y conserva su tono real en
    la plancha de color (`color` 0..1). `borde` px de papel recortado (None = automático; 0 = sin borde: elemento del
    decorado integrado). `alza` 0..1 = se levanta del suelo como un libro desplegable (0 = tumbado, 1 = de pie).
    `alto` = alto de la figura en unidades del mundo (un humano ≈ 180; un enano ≈ 140; Hakkar ≈ 600)."""
    if op <= 0.01 or alza <= 0.001:
        return
    dx, dz = float(cam.C[0]) - X, float(cam.C[2]) - Z
    n = math.hypot(dx, dz) or 1.0
    dx, dz = dx / n, dz / n
    th = math.radians(giro + aleteo * (3.5 * math.sin(t * 0.9 + sem * 1.7) + 1.5 * math.sin(t * 2.3 + sem)))
    ux, uz = -dz, dx
    U = (ux * math.cos(th) - uz * math.sin(th), 0.0, ux * math.sin(th) + uz * math.cos(th))
    phi = (1.0 - clamp(alza)) * math.pi / 2 * 0.97
    up = np.float32((-dx * math.sin(phi), -math.cos(phi), -dz * math.sin(phi)))
    sx, sy, zc = cam.pt(X, Y, Z)
    if zc < cam.cerca + 20:
        return
    px = alto * cam.k(zc)
    if px < 6:
        return
    alto_px = int(clamp(px, 24, 1100) // 8 * 8 + 8)
    b = int(round(max(4.0, alto_px * 0.035))) if borde is None else int(borde)
    im, A, ac = _estampa_png(fuente, alto_px, round(tinta, 2), round(color, 2), b, int(g.k) % 3, bool(espejo), sem)
    sub = G(g.t, im.shape[1], im.shape[0], alfa=True)
    sub.im, sub.alfa, sub.ac = im, A, ac
    pad = b + 4
    a_mundo = alto * im.shape[0] / float(alto_px)
    w_mundo = a_mundo * im.shape[1] / float(im.shape[0])
    base = np.float32((X, Y, Z)) - up * (alto * pad / float(alto_px))
    centro = base + up * (a_mundo / 2)
    if contacto > 0 and alza > 0.5:
        sombra_contacto(g, cam, X, Z, w_mundo * 0.32, w_mundo * 0.14, op=contacto * op * smooth((alza - 0.5) / 0.5), Y=Y)
    q = quad_mundo(cam, centro, U, tuple(-up), w_mundo, a_mundo)
    if q is not None:
        k = cam.k(zc)
        estampar(g, sub, q, sombra=sombra, off=(5 * k ** 0.5 + 3, 8 * k ** 0.5 + 4), desenfoque_sombra=4 + 3 * k ** 0.5,
                 op=op)


def quad_mundo(cam, centro, U, V, ancho, alto, giro=0.0):
    """Cuadrilátero de pantalla de un rectángulo del mundo (centro, ejes U, V; `giro` en grados dentro del plano), para
    `estampar`. Devuelve None si queda detrás de la cámara."""
    c, U, V = np.float32(centro), np.float32(U), np.float32(V)
    r = math.radians(giro)
    U2, V2 = U * math.cos(r) + V * math.sin(r), -U * math.sin(r) + V * math.cos(r)
    esq = [c - U2 * ancho / 2 - V2 * alto / 2, c + U2 * ancho / 2 - V2 * alto / 2, c + U2 * ancho / 2 + V2 * alto / 2,
           c - U2 * ancho / 2 + V2 * alto / 2]
    out = []
    for p in esq:
        sx, sy, zc = cam.pt(*p)
        if zc < cam.cerca:
            return None
        out.append((sx, sy))
    return np.float32(out)
