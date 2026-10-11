# -*- coding: utf-8 -*-
"""Personajes 2D expresivos del estilo Kurzgesagt (referencia: «This Woman Cured Her Cancer…», primeros planos y multitudes).

  busto(lz, x, y, s, spec, t, yaw=-0.5, bajar=0.0, roll=0.0, emocion='neutro', ojos=None, mirar=(0, 0), habla=0.0, mano=None, ...)
      Primer plano en 3/4: cabeza grande con cuello, pelo en bloque de 2 tonos, cejas sueltas, rubor, gafas/pendientes/tocados, hombros,
      manga con degradado y mano opcional. (x, y) = base del cuello; s = px por unidad (la cabeza mide ~2,4 unidades de alto).
      yaw: giro de la cabeza (rad, + = mira a la derecha; ±0.5 = 3/4); bajar 0..1 = cabeza inclinada hacia delante; roll = ladeo (rad).
  spec: dict o nombre de TIPOS (ver TIPOS; `variar(tipo, seed)` crea variantes para multitudes).

Sin contornos negros; sombras de 2 tonos (base + sombra rojiza-violeta); luz desde arriba-izquierda; idle siempre (respiración, balanceo, parpadeo).
"""
import math

import numpy as np

import plano as P
from motor import elipse, h01, catmull, smooth, ruido1
from kz_retrato import _emocion

# ---------------------------------------------------------------- paleta
PIEL2D = dict(clara=(247, 204, 168), trigueña=(232, 168, 118), canela=(214, 146, 98), morena=(196, 124, 84), oscura=(150, 94, 66))
SOMBRA_P = (112, 44, 84)           # la sombra de la piel tira a rojo-violeta, como en el original
CEJA_OSC = (70, 30, 70)

TIPOS = {
    # --- caxcanes
    "caxcan": dict(piel="morena", pelo=(40, 28, 44), peinado="largo", cejas_g=1.2, torso="capa_plumas", ropa=(214, 84, 70), ropa2=(250, 200, 84), tocado="plumas", pintura=True, collar=(80, 200, 190)),
    "caxcana": dict(piel="canela", pelo=(36, 26, 42), peinado="trenzas", cejas_g=1.0, torso="huipil", ropa=(236, 232, 214), ropa2=(222, 70, 120), tocado="cinta", pesta=True, rubor=0.4, collar=(250, 200, 84)),
    "anciano_caxcan": dict(piel="morena", pelo=(220, 214, 226), peinado="largo", cejas_g=1.3, torso="huipil", ropa=(190, 150, 110), ropa2=(222, 70, 120), tocado="cinta", arrugas=True),
    "jefe_caxcan": dict(piel="morena", pelo=(30, 22, 36), peinado="largo", cejas_g=1.4, torso="capa_plumas", ropa=(72, 150, 190), ropa2=(250, 200, 84), tocado="plumas_grande", pintura=True, collar=(250, 200, 84)),
    "sacerdote": dict(piel="canela", pelo=(30, 22, 36), peinado="largo", cejas_g=1.2, torso="capa_plumas", ropa=(120, 70, 190), ropa2=(80, 220, 200), tocado="plumas_grande", pintura=True, collar=(250, 200, 84)),
    # --- españoles y mundo colonial
    "soldado": dict(piel="clara", pelo=(90, 56, 44), peinado="corto", cejas_g=1.2, torso="coraza", ropa=(150, 160, 190), ropa2=(214, 70, 70), tocado="morrion", barba="corta"),
    "capitan": dict(piel="clara", pelo=(70, 42, 36), peinado="corto", cejas_g=1.3, torso="coraza", ropa=(190, 190, 214), ropa2=(214, 70, 70), tocado="morrion_plumas", barba="puntiaguda", bigote=True),
    "fraile": dict(piel="trigueña", pelo=(60, 40, 40), peinado="tonsura", cejas_g=1.1, torso="habito", ropa=(150, 118, 96), ropa2=(240, 232, 214), barba="corta"),
    "encomendero": dict(piel="clara", pelo=(60, 44, 40), peinado="corto", cejas_g=1.3, torso="levita", ropa=(60, 52, 96), ropa2=(250, 244, 230), bigote=True, barba="corta", tocado="sombrero_ala"),
    # --- siglo XX
    "revolucionario": dict(piel="trigueña", pelo=(36, 28, 32), peinado="corto", cejas_g=1.3, torso="bandolera", ropa=(240, 232, 208), ropa2=(150, 90, 60), tocado="sombrero_palma", bigote=True, cejas_gr=True),
    "comerciante": dict(piel="trigueña", pelo=(44, 32, 36), peinado="corto", cejas_g=1.1, torso="levita", ropa=(70, 100, 130), ropa2=(250, 244, 230), bigote=True),
    # --- hoy
    "mujer": dict(piel="canela", pelo=(110, 40, 96), peinado="corto", cejas_g=1.0, torso="camiseta", ropa=(140, 108, 200), ropa2=(200, 170, 230), gafas=(176, 50, 164), pendientes=(40, 160, 150), pesta=True, rubor=0.55),
    "senora": dict(piel="morena", pelo=(200, 196, 210), peinado="chongo", cejas_g=1.0, torso="rebozo", ropa=(70, 140, 170), ropa2=(240, 190, 80), arrugas=True, pendientes=(250, 200, 84), pesta=True),
    "xochipilli": dict(piel="morena", pelo=(30, 22, 36), peinado="largo", cejas_g=1.3, torso="capa_plumas", ropa=(236, 112, 60), ropa2=(255, 206, 80), tocado="flores_plumas", pintura=True, collar=(255, 206, 80), rubor=0.2),
    "danzante": dict(piel="canela", pelo=(36, 26, 42), peinado="trenzas", cejas_g=1.0, torso="huipil", ropa=(250, 240, 220), ropa2=(222, 60, 110), tocado="flores", pesta=True, rubor=0.5, collar=(250, 200, 84)),
    "danzante_h": dict(piel="trigueña", pelo=(36, 28, 32), peinado="corto", cejas_g=1.2, torso="camiseta", ropa=(250, 240, 220), ropa2=(222, 60, 70), tocado="flores", bigote=False),
    "hombre": dict(piel="trigueña", pelo=(44, 32, 38), peinado="corto", cejas_g=1.2, torso="camiseta", ropa=(220, 120, 70), ropa2=(250, 200, 120), bigote=False),
    "nino": dict(piel="canela", pelo=(36, 26, 42), peinado="corto", cejas_g=0.9, torso="camiseta", ropa=(80, 180, 150), ropa2=(250, 220, 120), rubor=0.6, escala_cabeza=1.12),
    "tastoan": dict(piel="morena", pelo=(40, 28, 44), peinado="corto", cejas_g=1.2, torso="camiseta", ropa=(214, 84, 70), ropa2=(250, 200, 84), tocado="mascara_tastoan"),
}


def variar(tipo, seed):
    """Variante de un tipo para multitudes: piel, pelo y ropa distintos con la misma silueta."""
    R = dict(TIPOS[tipo] if isinstance(tipo, str) else tipo)
    pieles = list(PIEL2D)
    R["piel"] = pieles[int(h01(seed, 3) * len(pieles)) % len(pieles)] if R.get("piel") in pieles else R.get("piel", "canela")
    paleta = [(214, 84, 70), (80, 160, 210), (120, 90, 200), (240, 170, 60), (80, 190, 140), (222, 80, 140), (236, 232, 214), (60, 52, 96)]
    R["ropa"] = paleta[int(h01(seed, 5) * len(paleta)) % len(paleta)]
    R["ropa2"] = paleta[int(h01(seed, 7) * len(paleta)) % len(paleta)]
    R["pelo"] = [(40, 28, 44), (70, 40, 40), (30, 22, 36), (110, 50, 90), (60, 40, 30)][int(h01(seed, 9) * 5) % 5]
    return R


# ---------------------------------------------------------------- utilidades de dibujo
class _D:
    """Dibuja en coordenadas locales de la cabeza/torso (unidades de s) con alfa global."""

    def __init__(self, lz, x, y, s, flip, A):
        self.lz, self.x, self.y, self.s, self.flip, self.A = lz, x, y, s, flip, A

    def pts(self, pts):
        a = np.asarray(pts, float)
        return np.stack([self.x + a[:, 0] * self.s * self.flip, self.y + a[:, 1] * self.s], 1)

    def poly(self, pts, color, a=1.0, capa=None):
        self.lz.relleno(self.pts(pts), color, alfa=a * self.A, capa=capa)

    def cat(self, pts, color, a=1.0, n=6, cerrado=True):
        self.lz.relleno(self.pts(catmull(np.array(pts, float), n, cerrado)), color, alfa=a * self.A)

    def ell(self, cx, cy, rx, ry, color, a=1.0, rot=0.0):
        self.lz.relleno(elipse(self.x + cx * self.s * self.flip, self.y + cy * self.s, rx * self.s, ry * self.s, rot * self.flip, 28), color, alfa=a * self.A)

    def grad(self, pts, c0, c1, p0, p1, a=1.0):
        q = self.pts(pts)
        self.lz.degradado(q, c0, c1, self.pts([p0])[0], self.pts([p1])[0], alfa=a * self.A)


def _sombreado(D, pts, base, sombra, luz=(-0.09, -0.07), n=8, a=1.0):
    """Forma con 2 tonos: relleno de sombra y, recortado a la silueta, el tono base desplazado hacia la luz."""
    c = catmull(np.array(pts, float), n, True)
    D.poly(c, sombra, a)
    with D.lz.recorte(D.pts(c)):
        D.poly(c + np.array(luz), base, a)


def _yaw_x(px, py, a, W=1.0):
    """Mapa de un punto frontal de la superficie de la cabeza (px, py) a x con la cabeza girada a rad."""
    r = px / max(1e-6, W)
    if abs(r) <= 1.0:
        x = math.sin(math.asin(r) + a)
    else:
        x = math.cos(a) * r
    cuello = smooth(min(1.0, max(0.0, (py + 1.55) / 1.1)))          # mandíbula y barbilla se desplazan más hacia donde mira
    return W * x + math.sin(a) * 0.20 * cuello


# ---------------------------------------------------------------- busto
# La cabeza se dibuja SIEMPRE «mirando a la derecha» con dos siluetas hechas a mano (frontal y 3/4) que se mezclan según |yaw|;
# si yaw < 0 se refleja entera (D con flip invertido). Mismo número y orden de puntos en las dos siluetas.
FRONT = np.array([(0.0, -2.78), (0.62, -2.62), (0.98, -2.10), (1.02, -1.50), (0.96, -1.18), (0.82, -0.92), (0.52, -0.50), (0.0, -0.36),
                  (-0.52, -0.50), (-0.82, -0.92), (-0.96, -1.18), (-1.02, -1.50), (-0.98, -2.10), (-0.62, -2.62)], float)
TRES4 = np.array([(-0.02, -2.80), (0.58, -2.66), (0.96, -2.25), (1.04, -1.78), (1.27, -1.40), (1.05, -1.08), (0.82, -0.72), (0.34, -0.40),
                  (-0.20, -0.52), (-0.62, -0.88), (-0.92, -1.20), (-1.08, -1.60), (-1.06, -2.10), (-0.72, -2.60)], float)


def _mt(a):
    return min(1.0, abs(a) / 0.95)


def _lerp(a, b, t):
    return a + (b - a) * t


def _sil(t, fw):
    p = FRONT * (1 - t) + TRES4 * t
    p = p.copy()
    p[:, 0] *= fw
    return p


def busto(lz, x, y, s, spec="mujer", t=0.0, yaw=-0.5, bajar=0.0, roll=0.0, emocion="neutro", ojos=None, mirar=(0.0, 0.0), habla=0.0, mano=None,
          seed=0, alfa=1.0, flip=1, luz_borde=None, temblor=0.0, brazo=True, torso_inc=0.0):
    R = TIPOS[spec] if isinstance(spec, str) else spec
    base_em = emocion if emocion in ("neutro", "alegre", "serio", "sorpresa", "miedo", "enojo", "triste", "pensativo", "grito") else \
        {"dolor": "triste", "cansado": "triste", "preocupado": "pensativo"}.get(emocion, "neutro")
    inc_b, alt_b, ab_ojo, curva_b, ab_b = _emocion(base_em)
    if emocion in ("dolor", "cansado"):
        ab_ojo, inc_b = 0.55, -0.42
    piel = PIEL2D[R.get("piel", "canela")]
    sombra = P.mezcla(piel, SOMBRA_P, 0.42)
    luzp = P.aclarar(piel, 0.20)
    resp = math.sin(t * 1.9 + seed)
    sway = math.sin(t * 0.8 + seed * 2.0)
    if temblor > 0:
        x += ruido1(t * 22 + seed, 3, 1) * temblor * s * 0.02
        y += ruido1(t * 22 + seed, 4, 2) * temblor * s * 0.02
    y += resp * s * 0.12
    x += sway * s * 0.05
    per = 3.4 + 2.4 * h01(seed, 17)                                       # parpadeo cada 3-6 s, ~0,14 s cerrado
    ciclo = (t + seed * 1.7) % per
    cierre = max(0.0, 1.0 - abs(ciclo - (per - 0.1)) / 0.07) if ciclo > per - 0.2 else 0.0
    tipo_ojo = ojos or ("cerrados" if emocion == "dormido" else "abiertos")
    ab = ab_ojo * (1 - 0.92 * cierre)
    D = _D(lz, x, y, s, flip, alfa)
    alto = mano in ("frente", "boca", "alzada")
    Dt = _D(lz, x, y - 0.32 * s, s, flip, alfa)
    _torso(Dt, R, yaw, t, seed, resp, mano, brazo and not alto, torso_inc)
    sg = 1 if yaw >= 0 else -1
    with lz.grupo(x, y, 1.0, roll * flip):
        Dh = _D(lz, 0.0, 0.0, s, flip * sg, alfa)
        _cabeza(Dh, R, abs(yaw), piel, sombra, luzp, bajar, inc_b, alt_b, ab, curva_b, ab_b, habla, t, seed, tipo_ojo, mirar, luz_borde)
    if alto and brazo:
        ropa = R.get("ropa", (140, 108, 200))
        _brazo(Dt, R, yaw, 1 if yaw < 0 else -1, 2.3, ropa, P.oscurecer(ropa, 0.30), piel, mano, t, seed)


def _cuello(D, piel, sombra, tt):
    c = -0.16 * tt
    D.cat([(-0.50 + c, -0.9), (0.50 + c, -0.9), (0.55 + c, -0.3), (0.58, 0.02), (-0.58, 0.02), (-0.55 + c, -0.3)], sombra, n=4)
    D.cat([(-0.50 + c, -0.9), (0.30 + c, -0.9), (0.34 + c, -0.3), (0.40, 0.02), (-0.58, 0.02), (-0.55 + c, -0.3)], P.mezcla(piel, sombra, 0.30), n=4)


def _cabeza(D, R, aa, piel, sombra, luzp, bajar, inc_b, alt_b, ab, curva_b, ab_b, habla, t, seed, tipo_ojo, mirar, luz_borde):
    tt = _mt(aa)
    fw = R.get("fw", 1.0) * R.get("escala_cabeza", 1.0) ** 0.5
    by = 0.17 * bajar
    sil = _sil(tt, fw)
    _pelo_atras(D, R, sil, tt, fw)
    _cuello(D, piel, sombra, tt)
    # ---- cara
    if luz_borde is not None:
        D.cat([(px + 0.06, py) for px, py in sil], luz_borde, 0.40)
    _sombreado(D, [tuple(p) for p in sil], piel, sombra, luz=(-0.07, -0.05))
    D.ell(_lerp(0.0, 0.5, tt) - 0.3, -2.0 + by * 0.3, 0.30, 0.15, luzp, 0.0)
    cc = D.pts(catmull(sil, 8, True))
    ef = (_lerp(0.43 * fw, 0.84, tt), _lerp(1.0, 0.5, tt))               # ojo del lado al que mira: (x, ancho relativo)
    eb = (_lerp(-0.43 * fw, 0.30, tt), _lerp(1.0, 0.92, tt))              # ojo del lado de atrás
    nx = _lerp(0.0, 1.02, tt)
    mx, mw = _lerp(0.0, 0.64, tt), _lerp(1.0, 0.62, tt)
    rub = R.get("rubor", 0.3)
    with D.lz.recorte(cc):
        for (cx_, w_) in ((_lerp(-0.66 * fw, 0.12, tt), _lerp(1.0, 0.9, tt)), (_lerp(0.66 * fw, 0.92, tt), _lerp(1.0, 0.35, tt))):
            D.ell(cx_, -1.12 + by, 0.27 * w_, 0.16, (240, 96, 96), rub)
        if R.get("pintura"):
            for (cx_, w_) in ((eb[0] + 0.02, eb[1]), (ef[0] + 0.02, ef[1])):
                for k in range(2):
                    D.poly([(cx_ - 0.25 * w_, -1.38 + k * 0.13 + by), (cx_ + 0.25 * w_, -1.42 + k * 0.13 + by), (cx_ + 0.25 * w_, -1.33 + k * 0.13 + by), (cx_ - 0.25 * w_, -1.29 + k * 0.13 + by)],
                           (250, 220, 120) if k == 0 else (80, 200, 190), 0.9)
    # ---- oreja (del lado de atrás) y pendiente
    ox = _lerp(-1.02 * fw, -0.42, tt)
    oy = -1.50 + 0.12 * bajar
    D.ell(ox, oy, 0.21, 0.34, P.mezcla(piel, sombra, 0.10), 1.0)
    D.ell(ox - 0.04, oy - 0.08, 0.10, 0.17, luzp, 0.35)
    D.ell(ox + 0.02, oy + 0.01, 0.10, 0.21, P.mezcla(sombra, (80, 24, 60), 0.30), 0.85)
    if R.get("pendientes"):
        D.ell(ox, oy + 0.42, 0.105, 0.105, R["pendientes"], 1.0)
    if tt < 0.45:                                                         # la otra oreja, mientras no la tape la cabeza
        D.ell(_lerp(1.02 * fw, 0.98, tt), oy, 0.21, 0.34, P.mezcla(piel, sombra, 0.4), 1.0 - tt * 2.2)
        if R.get("pendientes"):
            D.ell(_lerp(1.02 * fw, 0.98, tt), oy + 0.42, 0.105, 0.105, R["pendientes"], 1.0 - tt * 2.2)
    # ---- nariz
    n = R.get("nariz", 1.0)
    sc = 1.0 - 0.45 * tt
    D.cat([(nx + 0.02, -1.58 + by), (nx + 0.20 * n * sc, -1.30 + by), (nx + 0.16 * n * sc, -1.12 + by), (nx - 0.02, -1.07 + by), (nx - 0.14 * n * sc, -1.14 + by), (nx - 0.10 * n * sc, -1.32 + by)],
          sombra, 0.45 if tt < 0.6 else 0.0, n=5)
    D.ell(nx - 0.02 * tt, -1.20 + by, 0.16 * n * sc, 0.13 * n, piel, 1.0 if tt < 0.85 else 0.0)
    D.ell(nx - 0.04, -1.26 + by, 0.06 * n, 0.045 * n, luzp, 0.7 if tt < 0.85 else 0.0)
    if tt >= 0.5:                                                          # en 3/4 fuerte la nariz es solo un bulto del perfil con su sombra
        D.poly([(nx - 0.30, -1.62 + by), (nx - 0.10, -1.52 + by), (nx - 0.06, -1.15 + by), (nx - 0.22, -1.12 + by)], sombra, 0.55 * min(1.0, (tt - 0.45) * 3))
        D.ell(nx - 0.08, -1.10 + by, 0.04, 0.03, (90, 30, 64), 0.9)
    # ---- ojos y cejas
    dx, dy = mirar[0] * 0.07, mirar[1] * 0.05
    for (ex, wc, sd) in ((eb[0], eb[1], -1), (ef[0], ef[1], 1)):
        ey = -1.66 + by
        _ojo(D, ex, ey, wc, ab, tipo_ojo, R, dx, dy, sombra, sd)
        k = 0.7 + 0.45 * (R.get("cejas_g", 1.0) - 1)
        ang = inc_b * sd * (-1)
        cby = -2.0 - alt_b + by * 0.8
        w = 0.32 * wc
        col_c = R.get("cejas", P.mezcla(R["pelo"], CEJA_OSC, 0.45) if sum(R["pelo"]) < 560 else P.oscurecer(R["pelo"], 0.12))
        D.poly([(ex - w, cby + 0.05 - ang * w), (ex - w * 0.85, cby - 0.04 * k - ang * w * 0.85), (ex + w * 0.9, cby - 0.055 * k + ang * w * 0.9), (ex + w, cby + 0.02 + ang * w),
                (ex + w * 0.9, cby + 0.04 * k + ang * w * 0.9), (ex - w * 0.85, cby + 0.065 * k - ang * w * 0.85)], col_c, 1.0)
    if R.get("arrugas"):
        for (cx_, w_) in ((eb[0] + 0.1, eb[1]), (ef[0] - 0.05, ef[1])):
            D.poly([(cx_, -1.30 + by), (cx_ + 0.05, -1.05 + by), (cx_, -0.86 + by), (cx_ - 0.04, -1.05 + by)], sombra, 0.4)
        for yy in (-2.34, -2.24):
            D.poly([(-0.4, yy), (0.7, yy), (0.7, yy + 0.03), (-0.4, yy + 0.03)], sombra, 0.35)
    if R.get("gafas"):
        _gafas(D, R, eb, ef, by, ox)
    _boca(D, mx, mw, by, curva_b, ab_b, habla, t, seed, tt)
    _vello(D, R, sil, mx, mw, tt, by)
    _pelo_delante(D, R, sil, tt, fw, bajar, t)
    _tocado(D, R, fw, tt, t)


def _ojo(D, ex, ey, cs, ab, tipo, R, dx, dy, sombra, sd):
    col = (60, 24, 60)
    if tipo == "cerrados" or (tipo == "abiertos" and ab < 0.12):
        w = 0.22 * cs
        pts = [(ex - w, ey - 0.02), (ex - w * 0.4, ey + 0.05), (ex + w * 0.4, ey + 0.05), (ex + w, ey - 0.02), (ex + w * 0.8, ey - 0.005), (ex + w * 0.3, ey + 0.085), (ex - w * 0.3, ey + 0.085), (ex - w * 0.8, ey - 0.005)]
        D.cat(pts, col, 1.0, n=4)
        if R.get("pesta"):
            D.poly([(ex - w, ey - 0.02), (ex - w - 0.07 * cs, ey - 0.08), (ex - w * 0.7, ey + 0.0)], col, 1.0)
            D.poly([(ex + w, ey - 0.02), (ex + w + 0.07 * cs, ey - 0.08), (ex + w * 0.7, ey + 0.0)], col, 1.0)
        return
    if tipo == "feliz":
        w = 0.22 * cs
        D.cat([(ex - w, ey + 0.05), (ex - w * 0.4, ey - 0.06), (ex + w * 0.4, ey - 0.06), (ex + w, ey + 0.05), (ex + w * 0.8, ey + 0.03), (ex + w * 0.3, ey - 0.10), (ex - w * 0.3, ey - 0.10), (ex - w * 0.8, ey + 0.03)], col, 1.0, n=4)
        return
    blanco = tipo == "abiertos_grandes"
    if blanco:
        D.ell(ex, ey, 0.25 * cs, 0.20 * ab, (252, 248, 244), 1.0)
    D.ell(ex + dx * cs, ey + dy, 0.115 * cs * (1.25 if blanco else 1.0), 0.145 * min(1.1, ab), (56, 22, 56), 1.0)
    D.ell(ex + dx * cs + 0.035 * cs, ey + dy - 0.045, 0.035 * cs, 0.04, (255, 255, 255), 0.95)
    if R.get("pesta"):
        w = 0.17 * cs
        D.poly([(ex - w, ey - 0.10 * ab), (ex - w - 0.07 * cs, ey - 0.16 * ab), (ex - w * 0.4, ey - 0.15 * ab)], (56, 22, 56), 0.9)


def _boca(D, mx, mw, by, curva_b, ab_b, habla, t, seed, tt):
    my = -0.82 + by * 0.65
    mw = 0.30 * mw
    boca_a = ab_b + (habla * (0.28 + 0.26 * math.sin(t * 13.0 + seed)) if habla > 0 else 0.0)
    cur = curva_b * 0.10 + 0.04 * boca_a
    if boca_a > 0.08:
        ap = 0.06 + 0.22 * min(boca_a, 1.0)
        D.cat([(mx - mw, my), (mx - mw * 0.5, my - 0.02 + cur * 0.3), (mx, my - 0.03), (mx + mw * 0.5, my - 0.02 + cur * 0.3), (mx + mw, my), (mx + mw * 0.5, my + ap + cur), (mx, my + ap * 1.25),
               (mx - mw * 0.5, my + ap + cur)], (104, 30, 64), 1.0, n=4)
        if boca_a > 0.3:
            D.cat([(mx - mw * 0.6, my + ap * 0.7), (mx, my + ap * 0.5), (mx + mw * 0.6, my + ap * 0.7), (mx, my + ap * 1.2)], (240, 110, 130), 0.9, n=4)
    else:
        D.cat([(mx - mw, my - cur), (mx - mw * 0.4, my + cur * 0.4), (mx, my + cur * 0.5), (mx + mw * 0.4, my + cur * 0.4), (mx + mw, my - cur), (mx + mw * 0.4, my + cur * 0.4 + 0.05),
               (mx, my + cur * 0.5 + 0.065), (mx - mw * 0.4, my + cur * 0.4 + 0.05)], (110, 36, 70), 1.0, n=4)


def _anillo(D, cx, cy, rx, ry, g, rot, color, n=40):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)

    def el(rx_, ry_):
        x_, y_ = rx_ * np.cos(th), ry_ * np.sin(th)
        return np.stack([cx + x_ * math.cos(rot) - y_ * math.sin(rot), cy + x_ * math.sin(rot) + y_ * math.cos(rot)], 1)
    ext, inn = el(rx, ry), el(rx - g, ry - g)[::-1]
    D.poly(np.concatenate([ext, ext[:1], inn, inn[:1]]), color, 1.0)


def _gafas(D, R, eb, ef, by, ox):
    col = R["gafas"]
    lentes = []
    for (ex, wc, sd) in ((eb[0], eb[1], -1), (ef[0], ef[1], 1)):
        ey = -1.66 + by
        rx = 0.39 * max(0.40, wc)
        D.ell(ex, ey, rx - 0.04, 0.27, (255, 255, 255), 0.07, rot=-0.12 * sd)
        _anillo(D, ex, ey, rx, 0.31, 0.065, -0.12 * sd, col)
        lentes.append((ex, ey, rx))
    (x1, y1, r1), (x2, y2, r2) = lentes
    D.poly([(x1 + r1 - 0.03, y1 - 0.07), (x2 - r2 + 0.03, y2 - 0.07), (x2 - r2 + 0.03, y2 + 0.0), (x1 + r1 - 0.03, y1 + 0.0)], col, 1.0)
    D.poly([(x1 - r1 + 0.03, y1 - 0.06), (ox + 0.05, y1 - 0.05), (ox + 0.05, y1 + 0.02), (x1 - r1 + 0.03, y1 + 0.01)], col, 1.0)


def _vello(D, R, sil, mx, mw, tt, by):
    pelo = R["pelo"]
    col = P.oscurecer(pelo, 0.05)
    if R.get("bigote"):
        w = mw
        D.cat([(mx, -1.10 + by * 0.6), (mx + 0.30 * w, -1.07 + by * 0.6), (mx + 0.52 * w, -0.98 + by * 0.6), (mx + 0.40 * w, -0.84 + by * 0.6), (mx, -0.92 + by * 0.6), (mx - 0.40 * w, -0.84 + by * 0.6),
               (mx - 0.52 * w, -0.98 + by * 0.6), (mx - 0.30 * w, -1.07 + by * 0.6)], col, 1.0, n=4)
    b = R.get("barba")
    if b:
        L = 0.42 if b == "puntiaguda" else 0.14
        cm = np.array([mx, -1.02])
        ids = (4, 5, 6, 7, 8, 9, 10)
        ext = []
        inn = []
        for k in ids:
            p_ = sil[k].copy()
            q_ = cm + (p_ - cm) * 0.60
            if k == 7:
                p_ = p_ + np.array([0.0, L])
            ext.append((p_[0], p_[1] + by * 0.3))
            inn.append((q_[0], q_[1] + by * 0.3))
        ext[0] = (ext[0][0] - 0.02, ext[0][1] - 0.12)
        ext[-1] = (ext[-1][0] + 0.02, ext[-1][1] - 0.12)
        D.cat(ext + inn[::-1], col, 1.0, n=4)


# ---- peinados y tocados (se dibujan en el marco «mira a la derecha»)
def _pelo_atras(D, R, sil, tt, fw):
    pelo = R["pelo"]
    st = R.get("peinado", "corto")
    osc = P.oscurecer(pelo, 0.24)
    if st in ("largo", "trenzas"):
        pts = [tuple(sil[13] * 1.10), tuple(sil[12] * 1.10), tuple(sil[11] * 1.12), (-1.30, -0.7), (-1.38, 0.3), (-1.0, 1.0), (-0.1, 0.8), (sil[9][0], sil[9][1] + 0.1)]
        D.cat(pts, osc, 1.0, n=6)
        if tt < 0.7:                                                      # el mechón del otro lado, que se esconde al girar
            w = 1 - tt * 1.4
            pts2 = [tuple(sil[1] * 1.08), tuple(sil[2] * 1.10), (1.22 * fw, -1.5), (1.34 * fw * w + 0.1, -0.7), (1.30 * fw * w, 0.3), (0.9, 0.9), (0.2, 0.6), (sil[7][0], sil[7][1] + 0.1)]
            D.cat(pts2, osc, 1.0, n=6)
    elif st == "chongo":
        D.ell(-0.25, -3.12, 0.55, 0.45, osc, 1.0)


def _pelo_delante(D, R, sil, tt, fw, bajar, t):
    pelo = R["pelo"]
    st = R.get("peinado", "corto")
    luz_p = P.aclarar(pelo, 0.22) if sum(pelo) < 560 else P.oscurecer(pelo, 0.08)
    sh = P.oscurecer(pelo, 0.24)
    by = 0.12 * bajar
    if st in ("corto", "largo", "trenzas", "chongo"):
        ctr = np.array([sil[:, 0].mean(), -1.8])
        def ex_(k, f_):
            return tuple(ctr + (sil[k] - ctr) * f_)
        arco = [ex_(11, 1.05), ex_(12, 1.09), ex_(13, 1.08), ex_(0, 1.06), ex_(1, 1.06), ex_(2, 1.05)]
        hl = [(_lerp(1.0, 1.05, tt), -2.12 + by), (_lerp(0.62, 0.80, tt), -2.38 + by), (_lerp(0.25, 0.38, tt), -2.45 + by), (_lerp(-0.2, -0.12, tt), -2.38 + by * 0.5), (-0.62, -2.15), (-0.98, -1.82)]
        pts = arco + hl
        _sombreado(D, pts, pelo, sh, luz=(-0.05, -0.07), n=7)
        with D.lz.recorte(D.pts(catmull(np.array(pts, float), 7, True))):
            D.cat([(-0.75, -2.80), (-0.1, -2.98), (0.55, -2.80), (0.05, -2.62), (-0.55, -2.66)], luz_p, 0.45, n=4)
        if st == "trenzas":
            for k in range(5):
                D.ell(-1.18 + 0.05 * math.sin(t * 1.5 + k), -0.8 + k * 0.28, 0.20, 0.17, P.aclarar(pelo, 0.08) if k % 2 else pelo, 1.0)
    elif st == "tonsura":
        for sd in (-1, 1):
            D.cat([(sd * 1.0, -2.05), (sd * 0.88, -2.0), (sd * 0.84, -1.55), (sd * 0.92, -1.25), (sd * 1.04, -1.5)], pelo, 1.0, n=4)


def _tocado(D, R, fw, tt, t):
    hx = lambda px, py: px * fw
    t_ = R.get("tocado")
    if t_ == "plumas" or t_ == "plumas_grande":
        gr = 1.35 if t_ == "plumas_grande" else 1.0
        cols = [(222, 70, 120), (250, 200, 84), (80, 200, 190), (120, 90, 220), (222, 70, 120)]
        D.poly([(hx(-1.05, -2.35), -2.35), (hx(1.05, -2.35), -2.35), (hx(1.05, -2.18), -2.18), (hx(-1.05, -2.18), -2.18)], (250, 200, 84), 1.0)
        for k in range(5):
            ang = -0.75 + 0.375 * k
            bx, by_ = hx(-0.7 + 0.35 * k, -2.3), -2.3
            lon = (1.0 + 0.35 * math.cos(ang * 1.4)) * gr
            ox_, oy_ = math.sin(ang) * lon * 0.9, -math.cos(ang) * lon
            bal = 0.04 * math.sin(t * 2.1 + k * 0.8)
            D.cat([(bx - 0.10, by_), (bx + ox_ * 0.5 - 0.17 + bal, by_ + oy_ * 0.5), (bx + ox_ + bal * 2, by_ + oy_), (bx + ox_ * 0.5 + 0.17 + bal, by_ + oy_ * 0.5), (bx + 0.10, by_)], cols[k], 1.0, n=4)
    elif t_ in ("flores", "flores_plumas"):
        if t_ == "flores_plumas":
            cols = [(222, 70, 120), (250, 200, 84), (80, 200, 190), (120, 90, 220), (222, 70, 120), (250, 200, 84), (80, 200, 190)]
            for k in range(7):
                ang = -1.0 + 0.333 * k
                bx = hx(-0.9 + 0.3 * k, -2.3)
                lon = 2.2 + 0.4 * math.cos(ang * 1.4)
                ox_, oy_ = math.sin(ang) * lon * 0.9, -math.cos(ang) * lon
                bal = 0.05 * math.sin(t * 2.1 + k * 0.8)
                D.cat([(bx - 0.14, -2.3), (bx + ox_ * 0.5 - 0.22 + bal, -2.3 + oy_ * 0.5), (bx + ox_ + bal * 2, -2.3 + oy_), (bx + ox_ * 0.5 + 0.22 + bal, -2.3 + oy_ * 0.5), (bx + 0.14, -2.3)], cols[k], 1.0, n=4)
        D.poly([(hx(-1.05, -2.34), -2.34), (hx(1.05, -2.34), -2.34), (hx(1.05, -2.16), -2.16), (hx(-1.05, -2.16), -2.16)], (84, 168, 100), 1.0)
        for k in range(5):
            fx = hx(-0.85 + 0.425 * k, -2.30)
            for j in range(8):
                a = j * math.pi / 4 + t * 0.3 + k
                D.cat([(fx + math.cos(a) * 0.05, -2.30 + math.sin(a) * 0.05), (fx + math.cos(a - 0.35) * 0.22, -2.30 + math.sin(a - 0.35) * 0.22), (fx + math.cos(a) * 0.30, -2.30 + math.sin(a) * 0.30),
                       (fx + math.cos(a + 0.35) * 0.22, -2.30 + math.sin(a + 0.35) * 0.22)], (255, 150, 40) if (k + j) % 2 else (255, 190, 60), 1.0, n=3)
            D.ell(fx, -2.30, 0.07, 0.07, (160, 80, 20), 1.0)
    elif t_ == "cinta":
        D.poly([(hx(-1.06, -2.36), -2.36), (hx(1.06, -2.36), -2.36), (hx(1.06, -2.22), -2.22), (hx(-1.06, -2.22), -2.22)], R.get("ropa2", (222, 70, 120)), 1.0)
    elif t_ in ("morrion", "morrion_plumas"):
        casco = (176, 186, 214)
        D.cat([(hx(-1.15, -2.0), -2.0), (hx(-1.0, -2.8), -2.8), (hx(0.0, -3.25), -3.25), (hx(1.0, -2.8), -2.8), (hx(1.15, -2.0), -2.0), (hx(0.0, -2.2), -2.2)], P.oscurecer(casco, 0.25), 1.0, n=6)
        D.cat([(hx(-1.1, -2.05), -2.05), (hx(-0.95, -2.8), -2.8), (hx(-0.1, -3.2), -3.2), (hx(0.5, -3.0), -3.0), (hx(0.0, -2.35), -2.35)], casco, 1.0, n=6)
        D.poly([(hx(-1.7, -2.1), -2.1), (hx(1.7, -2.1), -2.1), (hx(1.4, -1.95), -1.95), (hx(-1.4, -1.95), -1.95)], P.oscurecer(casco, 0.12), 1.0)
        D.poly([(hx(-0.06, -3.25), -3.25), (hx(0.06, -3.25), -3.25), (hx(0.06, -2.3), -2.3), (hx(-0.06, -2.3), -2.3)], P.aclarar(casco, 0.3), 0.8)
        if t_ == "morrion_plumas":
            for k in range(4):
                D.cat([(hx(0.0, -3.2), -3.2), (hx(0.3 + 0.2 * k, -3.7 - 0.15 * k), -3.7 - 0.15 * k), (hx(0.8 + 0.2 * k, -3.5 - 0.1 * k), -3.5 - 0.1 * k), (hx(0.3, -3.2), -3.2)], (214, 60, 70) if k % 2 == 0 else (250, 244, 230), 1.0, n=4)
    elif t_ in ("sombrero_palma", "sombrero_ala"):
        pal = (236, 196, 116) if t_ == "sombrero_palma" else (60, 52, 80)
        D.cat([(hx(-1.1, -2.1), -2.1), (hx(-0.95, -2.75), -2.75), (hx(0.0, -2.95), -2.95), (hx(0.95, -2.75), -2.75), (hx(1.1, -2.1), -2.1), (hx(0.0, -2.35), -2.35)], P.aclarar(pal, 0.05), 1.0, n=6)
        D.cat([(hx(-2.5, -2.3), -2.3), (hx(-1.6, -2.5), -2.5), (hx(0.0, -2.52), -2.52), (hx(1.6, -2.5), -2.5), (hx(2.5, -2.3), -2.3), (hx(1.6, -2.05), -2.05), (hx(0.0, -2.15), -2.15), (hx(-1.6, -2.05), -2.05)], pal, 1.0, n=6)
        D.poly([(hx(-1.0, -2.46), -2.46), (hx(1.0, -2.46), -2.46), (hx(1.0, -2.32), -2.32), (hx(-1.0, -2.32), -2.32)], (214, 70, 70) if t_ == "sombrero_palma" else (250, 200, 84), 1.0)
    elif t_ == "mascara_tastoan":
        # máscara de madera de tastoán (Jalisco/Zacatecas): cara rosada tallada, nariz larga, ojos saltones, boca con dientes,
        # cabellera de ixtle que cae a los lados y dos cuernitos
        crin, crin2 = (96, 66, 44), (170, 128, 80)
        sw = 0.08 * math.sin(t * 6.0)
        for k in range(9):                                            # cabellera de ixtle (mechones largos)
            sd = -1 if k < 5 else 1
            x0 = (-1.15 + 0.12 * k) if sd < 0 else (0.15 + 0.12 * k)
            D.cat([(hx(x0, -2.7), -2.7), (hx(x0 + sd * 0.55 + sw, -1.4), -1.4), (hx(x0 + sd * 0.45 + sw * 1.6, 0.1), 0.1), (hx(x0 + sd * 0.2 + sw, -1.5), -1.5)],
                  crin if k % 2 else crin2, 1.0, n=4)
        for sd in (-1, 1):                                            # cuernitos
            D.cat([(hx(sd * 0.45, -2.6), -2.6), (hx(sd * 0.75, -3.35), -3.35), (hx(sd * 0.95, -3.4), -3.4), (hx(sd * 0.7, -2.6), -2.6)], (240, 228, 200), 1.0, n=4)
        cara_m = [(hx(-0.95, -2.55), -2.55), (hx(-1.0, -1.4), -1.4), (hx(-0.7, -0.55), -0.55), (hx(0.0, -0.35), -0.35), (hx(0.7, -0.55), -0.55), (hx(1.0, -1.4), -1.4),
                  (hx(0.95, -2.55), -2.55), (hx(0.0, -2.85), -2.85)]
        D.cat(cara_m, (196, 92, 96), 1.0, n=6)
        D.cat([(x * 0.9 - 0.06, y * 0.98 - 0.02) for x, y in cara_m], (226, 128, 124), 1.0, n=6)
        for sd in (-1, 1):                                            # cejas talladas y ojos saltones
            D.poly([(hx(sd * 0.85, -2.22), -2.22), (hx(sd * 0.15, -2.05), -2.05), (hx(sd * 0.15, -1.93), -1.93), (hx(sd * 0.85, -2.06), -2.06)], (110, 50, 50), 1.0)
            D.ell(hx(sd * 0.46, -1.72), -1.72, 0.27, 0.22, (60, 26, 40), 1.0)
            D.ell(hx(sd * 0.46, -1.72), -1.72, 0.2, 0.16, (250, 244, 230), 1.0)
            D.ell(hx(sd * 0.46, -1.70), -1.70, 0.08, 0.08, (30, 16, 30), 1.0)
            D.ell(hx(sd * 0.62, -1.15), -1.15, 0.2, 0.12, (250, 120, 120), 0.8)
        D.poly([(hx(-0.12, -1.85), -1.85), (hx(0.12, -1.85), -1.85), (hx(0.34, -0.95), -0.95), (hx(0.0, -0.82), -0.82), (hx(-0.34, -0.95), -0.95)], (240, 150, 140), 1.0)
        D.poly([(hx(0.0, -0.82), -0.82), (hx(0.34, -0.95), -0.95), (hx(0.12, -1.85), -1.85)], (200, 104, 104), 0.8)
        D.cat([(hx(-0.45, -0.72), -0.72), (hx(0.0, -0.62), -0.62), (hx(0.45, -0.72), -0.72), (hx(0.0, -0.42), -0.42)], (70, 20, 30), 1.0, n=4)
        for k in range(4):
            D.poly([(hx(-0.3 + 0.16 * k, -0.68), -0.68), (hx(-0.2 + 0.16 * k, -0.68), -0.68), (hx(-0.25 + 0.16 * k, -0.56), -0.56)], (250, 244, 230), 1.0)


# ---------------------------------------------------------------- torso
def _torso(D, R, a, t, seed, resp, mano, brazo, inc):
    ropa, ropa2 = R.get("ropa", (140, 108, 200)), R.get("ropa2", (200, 170, 230))
    piel = PIEL2D[R.get("piel", "canela")]
    sh = P.oscurecer(ropa, 0.30)
    sa = math.sin(a)
    d = 1 if a < 0 else -1                   # hacia dónde mira (signo en x del dibujo)
    resp_y = resp * 0.02
    # hombros: el del lado al que mira (cercano) es más ancho
    wn = 2.3                                  # hombro cercano
    wf = 1.25 + 0.4 * (1 - abs(sa))          # hombro lejano
    base = [(-d * wf, 0.30), (-d * (wf - 0.6), -0.02 + resp_y), (-0.55, -0.12 + resp_y), (0.55, -0.12 + resp_y), (d * (wn - 0.6), -0.02 + resp_y), (d * wn, 0.35), (d * (wn + 0.35), 1.7), (d * (wn + 0.25), 4.4), (-d * (wf + 0.2), 4.4), (-d * (wf + 0.05), 1.5)]
    D.cat(base, sh, 1.0, n=6)
    luz = [(-d * (wf - 0.1), 0.34), (-d * (wf - 0.6), 0.0), (-0.55, -0.10 + resp_y), (0.55, -0.10 + resp_y), (d * (wn - 0.7), 0.02), (d * (wn - 0.2), 0.4), (d * (wn + 0.1), 1.7), (d * (wn + 0.05), 4.4), (-d * (wf + 0.0), 4.4), (-d * (wf - 0.1), 1.6)]
    D.cat(luz, ropa, 1.0, n=6)
    tr = R.get("torso", "camiseta")
    cu = (0.0, 0.0)
    if tr == "camiseta":
        D.cat([(-0.62, -0.10), (0.0, 0.35), (0.62, -0.10), (0.5, 0.0), (0.0, 0.18), (-0.5, 0.0)], PIEL2D[R.get("piel", "canela")], 0.0)
        D.cat([(-0.70, -0.05), (0.0, 0.52), (0.70, -0.05), (0.64, 0.30), (0.0, 0.72), (-0.64, 0.30)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=4)
        D.cat([(-0.70, -0.05), (0.0, 0.52), (0.70, -0.05), (0.80, 0.05), (0.0, 0.66), (-0.80, 0.05)], P.aclarar(ropa, 0.12), 1.0, n=4)
    elif tr == "huipil":
        D.cat([(-0.75, -0.05), (0.75, -0.05), (0.78, 0.45), (-0.78, 0.45)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=3)
        D.poly([(-0.9, 0.0), (0.9, 0.0), (0.94, 0.20), (-0.94, 0.20)], ropa2, 1.0)
        for k in range(6):
            D.poly([(-0.9 + k * 0.30, 0.65), (-0.75 + k * 0.30, 0.45), (-0.6 + k * 0.30, 0.65), (-0.75 + k * 0.30, 0.85)], ropa2, 0.95)
        for k in range(3):
            D.poly([(-2.4, 2.6 + k * 0.5), (2.4, 2.6 + k * 0.5), (2.4, 2.72 + k * 0.5), (-2.4, 2.72 + k * 0.5)], ropa2, 0.9)
    elif tr == "capa_plumas":
        D.cat([(-0.75, -0.05), (0.75, -0.05), (0.78, 0.5), (-0.78, 0.5)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=3)
        cols = [ropa2, (222, 70, 120), (80, 200, 190), ropa2]
        for k in range(4):
            yy = 0.15 + k * 0.7
            D.cat([(-2.5 + k * 0.2, yy), (-1.2, yy + 0.35), (0.0, yy + 0.55), (1.2, yy + 0.35), (2.5 - k * 0.2, yy), (2.3 - k * 0.2, yy + 0.5), (0.0, yy + 0.95), (-2.3 + k * 0.2, yy + 0.5)], cols[k], 1.0, n=5)
        col = R.get("collar", (80, 200, 190))
        for k in range(7):
            ang = math.pi * (0.15 + 0.7 * k / 6)
            D.ell(math.cos(ang) * 0.85, 0.15 + math.sin(ang) * 0.38, 0.09, 0.09, col, 1.0)
    elif tr == "coraza":
        D.cat([(-0.70, -0.05), (0.70, -0.05), (0.72, 0.5), (-0.72, 0.5)], (120, 130, 160), 1.0, n=3)
        D.cat([(-2.4, 0.5), (-1.0, 0.1), (0.0, 0.0), (1.0, 0.1), (2.4, 0.5), (2.2, 2.8), (0.0, 3.2), (-2.2, 2.8)], R.get("ropa", (150, 160, 190)), 1.0, n=6)
        D.cat([(-1.4, 0.4), (0.0, 0.1), (1.4, 0.4), (1.2, 1.9), (0.0, 2.1), (-1.2, 1.9)], P.aclarar(R.get("ropa", (150, 160, 190)), 0.2), 0.9, n=5)
        D.poly([(-0.07, 0.1), (0.07, 0.1), (0.1, 3.0), (-0.1, 3.0)], P.oscurecer(R.get("ropa", (150, 160, 190)), 0.25), 0.9)
        D.poly([(-2.4, 0.5), (-1.0, 0.1), (-1.0, 0.45), (-2.3, 0.9)], ropa2, 1.0)
        D.poly([(2.4, 0.5), (1.0, 0.1), (1.0, 0.45), (2.3, 0.9)], ropa2, 1.0)
    elif tr == "habito":
        D.cat([(-0.75, -0.05), (0.75, -0.05), (0.78, 0.5), (-0.78, 0.5)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=3)
        D.cat([(-1.5, 0.0), (0.0, 0.7), (1.5, 0.0), (1.9, 0.7), (0.0, 1.6), (-1.9, 0.7)], ropa2, 1.0, n=5)      # capucha caída
        D.poly([(-0.10, 1.0), (0.10, 1.0), (0.24, 4.0), (-0.24, 4.0)], P.oscurecer(ropa, 0.25), 1.0)
        for k in range(4):
            D.ell(0.12 * math.sin(k), 2.2 + k * 0.5, 0.11, 0.11, (240, 232, 214), 1.0)         # cordón con nudos
    elif tr == "levita":
        D.cat([(-0.55, 0.0), (0.55, 0.0), (0.7, 0.7), (-0.7, 0.7)], ropa2, 1.0, n=3)
        D.poly([(-0.45, 0.3), (0.0, 1.0), (0.45, 0.3), (1.3, 1.1), (0.0, 4.0), (-1.3, 1.1)], ropa2, 0.95)
        D.poly([(-0.20, 0.4), (0.20, 0.4), (0.10, 1.4), (-0.10, 1.4)], (206, 60, 70), 1.0)
        for sd in (-1, 1):
            D.poly([(sd * 0.55, 0.0), (sd * 1.4, 0.7), (sd * 0.5, 2.6), (0.0, 1.0)], P.aclarar(ropa, 0.08), 1.0)
    elif tr == "bandolera":
        D.cat([(-0.7, -0.05), (0.7, -0.05), (0.72, 0.5), (-0.72, 0.5)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=3)
        D.poly([(-0.7, 0.0), (0.0, 0.9), (0.7, 0.0), (1.0, 0.3), (0.0, 1.5), (-1.0, 0.3)], ropa, 1.0)
        D.poly([(-2.4, 0.5), (-1.9, 0.2), (2.5, 3.8), (1.9, 4.1)], ropa2, 1.0)           # cuartelera cruzada
        for k in range(7):
            D.ell(-1.6 + k * 0.52, 0.55 + k * 0.52, 0.11, 0.17, (250, 200, 84), 1.0, rot=0.8)
    elif tr == "rebozo":
        D.cat([(-0.7, 0.0), (0.7, 0.0), (0.74, 0.55), (-0.74, 0.55)], P.mezcla(piel, SOMBRA_P, 0.4), 1.0, n=3)
        D.cat([(-0.9, 0.0), (0.0, 1.0), (0.9, 0.0), (2.4, 0.9), (2.6, 4.4), (-2.6, 4.4), (-2.4, 0.9)], ropa, 1.0, n=6)
        for k in range(5):
            D.poly([(-2.5 + k * 0.1, 1.5 + k * 0.5), (2.5 - k * 0.1, 1.5 + k * 0.5), (2.5 - k * 0.1, 1.64 + k * 0.5), (-2.5 + k * 0.1, 1.64 + k * 0.5)], ropa2, 0.9)
    # brazo cercano + mano
    if brazo:
        _brazo(D, R, a, d, wn, ropa, sh, piel, mano, t, seed)


def _capsula(D, p0, p1, r0, r1, color, a=1.0, n=14):
    p0, p1 = np.array(p0, float), np.array(p1, float)
    v = p1 - p0
    L = float(np.hypot(*v)) + 1e-9
    nrm = np.array([-v[1], v[0]]) / L
    ang = math.atan2(v[1], v[0])
    pts = []
    for k in range(n + 1):                                   # semicírculo en p1
        th = ang - math.pi / 2 + math.pi * k / n
        pts.append(p1 + r1 * np.array([math.cos(th), math.sin(th)]))
    for k in range(n + 1):                                   # semicírculo en p0
        th = ang + math.pi / 2 + math.pi * k / n
        pts.append(p0 + r0 * np.array([math.cos(th), math.sin(th)]))
    D.poly(pts, color, a)


def _mano_forma(D, c, ang, k, color, sombra, abierta=False):
    """Mano de «guante» con pulgar: c = centro de la palma, ang = dirección de los dedos."""
    ca, sa = math.cos(ang), math.sin(ang)
    R_ = lambda u, v: (c[0] + (u * ca - v * sa) * k, c[1] + (u * sa + v * ca) * k)
    palma = [R_(-0.25, -0.30), R_(0.35, -0.34), R_(0.62, -0.20), R_(0.66, 0.06), R_(0.58, 0.30), R_(0.30, 0.38), R_(-0.22, 0.34)]
    D.cat(palma, sombra, 1.0, n=5)
    D.cat([R_(-0.22, -0.28), R_(0.32, -0.32), R_(0.6, -0.18), R_(0.64, 0.02), R_(0.56, 0.22), R_(0.28, 0.30), R_(-0.20, 0.26)], color, 1.0, n=5)
    # dedos (cuatro cápsulas cortas) y pulgar
    for i, v in enumerate((-0.20, -0.07, 0.07, 0.20)):
        D.cat([R_(0.40, v - 0.065), R_(0.66 + (0.08 if abierta else 0.0), v - 0.06), R_(0.70 + (0.08 if abierta else 0.0), v), R_(0.66 + (0.08 if abierta else 0.0), v + 0.06), R_(0.40, v + 0.065)], color if i % 2 == 0 else P.mezcla(color, sombra, 0.25), 1.0, n=3)
    D.cat([R_(0.0, -0.28), R_(0.30, -0.52), R_(0.52, -0.46), R_(0.46, -0.34), R_(0.22, -0.30)], P.mezcla(color, sombra, 0.2), 1.0, n=4)


def _brazo(D, R, a, d, wn, ropa, sh, piel, mano, t, seed):
    hombro = (d * (wn - 0.5), 0.6)
    manga0 = P.oscurecer(ropa, 0.12)
    manga1 = P.aclarar(ropa, 0.32)
    if mano == "estomago":
        codo = (d * (wn - 0.05), 2.0)
        mn = (-d * 0.35, 2.25 + 0.04 * math.sin(t * 1.9 + seed))
        ang = math.atan2(0.05, -d)
    elif mano == "pecho":
        codo = (d * (wn - 0.05), 1.9)
        mn = (-d * 0.2, 1.25)
        ang = math.atan2(-0.25, -d)
    elif mano == "frente":
        codo = (d * (wn - 0.3), 0.9)
        mn = (-d * 0.35, -1.95)
        ang = math.atan2(-0.9, -d)
    elif mano == "boca":
        codo = (d * (wn - 0.3), 1.0)
        mn = (-d * 0.9, -0.85)
        ang = math.atan2(-0.6, -d)
    elif mano == "alzada":
        codo = (d * (wn + 0.35), 1.6)
        mn = (d * (wn + 0.25), -0.5 + 0.08 * math.sin(t * 2.0 + seed))
        ang = -math.pi / 2
    else:
        codo = (d * (wn + 0.2), 2.9)
        mn = (d * (wn + 0.15), 4.2)
        ang = math.pi / 2
        _capsula(D, hombro, codo, 0.52, 0.44, manga0)
        _capsula(D, codo, mn, 0.44, 0.40, manga1)
        if abs(a) < 0.4:
            h2 = (-hombro[0], hombro[1]); c2 = (-codo[0], codo[1]); m2 = (-mn[0], mn[1])
            _capsula(D, h2, c2, 0.52, 0.44, manga0)
            _capsula(D, c2, m2, 0.44, 0.40, manga1)
        return
    D.grad([hombro, codo, mn], manga0, manga1, hombro, mn, 0.0)
    _capsula(D, hombro, codo, 0.64, 0.54, manga0)
    # antebrazo con degradado de color (se aclara hacia la muñeca, como la manga del original)
    v = np.array(mn) - np.array(codo)
    L = float(np.hypot(*v))
    nrm = np.array([-v[1], v[0]]) / L
    pts = [np.array(codo) + nrm * 0.54, np.array(mn) + nrm * 0.46, np.array(mn) - nrm * 0.46, np.array(codo) - nrm * 0.54]
    D.grad(pts, manga0, manga1, codo, mn)
    D.ell(codo[0], codo[1], 0.54, 0.54, manga0, 1.0)
    D.ell(mn[0], mn[1], 0.47, 0.47, manga1)
    _mano_forma(D, (mn[0] + v[0] / L * 0.15, mn[1] + v[1] / L * 0.15), ang, 0.95, P.aclarar(piel, 0.0), P.mezcla(piel, SOMBRA_P, 0.5))


# ====================================================================================================== CUERPO COMPLETO
# Origen en los PIES (centro). Unidades como el busto (cabeza ≈ 2,4 u de alto); altura total ≈ 7,9 u. mirar = +1 derecha / -1 izquierda.
L_MUSLO, L_PIERNA, L_BRAZO, L_ANTEBRAZO, L_TORSO = 1.55, 1.50, 1.20, 1.15, 2.05
MANGA = {"camiseta": "larga", "levita": "larga", "coraza": "larga", "habito": "larga", "bandolera": "larga", "rebozo": "larga",
         "huipil": "corta", "capa_plumas": "sin"}
FALDA = {"huipil", "habito", "rebozo"}
GIRO_CAMINA = 0.9                  # ciclos por segundo con vel = 1


def v_marcha(s, vel=1.0):
    """Velocidad del suelo (px/s) para que los pies no resbalen con `piernas='camina'` a escala s."""
    return 6.0 * GIRO_CAMINA * vel * s


def _ik(p0, p1, l1, l2, signo):
    """Codo/rodilla de una cadena de dos huesos de p0 hacia p1; signo ±1 elige a qué lado dobla."""
    p0, p1 = np.array(p0, float), np.array(p1, float)
    d = p1 - p0
    L = float(np.hypot(*d))
    L = min(max(L, abs(l1 - l2) + 1e-3), l1 + l2 - 1e-3)
    u = d / (float(np.hypot(*d)) + 1e-9)
    a = (l1 * l1 - l2 * l2 + L * L) / (2 * L)
    h = math.sqrt(max(0.0, l1 * l1 - a * a))
    return p0 + u * a + np.array([-u[1], u[0]]) * h * signo, p0 + u * L


def _fk(p0, ang, L):
    """Punto a distancia L de p0 con ángulo `ang` medido desde «hacia abajo»; + = hacia delante (+x)."""
    return np.array([p0[0] + L * math.sin(ang), p0[1] + L * math.cos(ang)])


def _pose_pierna(th, amp, flex_max):
    a = amp * math.sin(th)
    flex = flex_max * max(0.0, math.cos(th)) ** 1.2
    return a, a - flex


def _dibuja_obj(D, fn, mano, ang, t, seed):
    if fn is not None:
        fn(D, mano, ang, t, seed)


def cuerpo(lz, x, y, s, spec="hombre", t=0.0, piernas="idle", brazos="balanceo", mirar=1, vista="perfil", ph=None, vel=1.0, cara="auto", obj_d=None, obj_i=None,
           seed=0, alfa=1.0, sombra=True, lean=0.0, emocion="neutro", objetivo=None, escala_h=1.0):
    """Personaje de cuerpo entero. piernas: idle | camina | corre | baila | arrodillado | sentado.
    brazos: balanceo | idle | señala | arriba | saluda | carga | labra | baila | defensa | pecho.
    vista: perfil (camina bien) | frente | tres (3/4, cabeza y pecho girados). objetivo: punto (px) al que apunta/alcanza si brazos='señala'."""
    R = TIPOS[spec] if isinstance(spec, str) else spec
    S = escala_h * s
    piel = PIEL2D[R.get("piel", "canela")]
    sombra_p = P.mezcla(piel, SOMBRA_P, 0.42)
    ropa, ropa2 = R.get("ropa", (140, 108, 200)), R.get("ropa2", (200, 170, 230))
    tr = R.get("torso", "camiseta")
    falda = tr in FALDA
    manga = MANGA.get(tr, "larga")
    col_pant = R.get("pantalon", P.oscurecer(ropa2, 0.45) if sum(ropa2) > 300 else P.oscurecer(ropa2, 0.1))
    if tr in ("levita", "coraza"):
        col_pant = (70, 60, 96)
    if ph is None:
        ph = t * 2 * math.pi * GIRO_CAMINA * vel + seed * 1.7
    A = alfa
    px = 0.0 if vista != "perfil" else 0.0
    D = _D(lz, x, y, S, mirar, A)
    # -------- sombra de suelo
    if sombra:
        lz.relleno(elipse(x, y - 0.05 * S, 1.6 * S, 0.30 * S, 0.0, 24), (14, 6, 34), alfa=0.28 * A)
    sw = math.sin(ph)
    # -------- piernas y cadera
    flexL = flexR = 0.0
    if piernas in ("camina", "corre"):
        amp, fm = (0.50, 0.95) if piernas == "camina" else (0.80, 1.35)
        aN, bN = _pose_pierna(ph, amp, fm)
        aF, bF = _pose_pierna(ph + math.pi, amp, fm)
        ext = max(L_MUSLO * math.cos(aN) + L_PIERNA * math.cos(bN), L_MUSLO * math.cos(aF) + L_PIERNA * math.cos(bF))
        hip_y = -(ext + 0.12) + (0.0 if piernas == "camina" else -0.35 * abs(math.sin(ph)))
        lean_ = lean + (0.06 if piernas == "camina" else 0.28)
    elif piernas == "baila":
        aN, bN = 0.35 * math.sin(ph * 1.0), 0.35 * math.sin(ph) - 0.5 * max(0, math.cos(ph))
        aF, bF = -0.35 * math.sin(ph), -0.35 * math.sin(ph) - 0.5 * max(0, -math.cos(ph))
        ext = max(L_MUSLO * math.cos(aN) + L_PIERNA * math.cos(bN), L_MUSLO * math.cos(aF) + L_PIERNA * math.cos(bF))
        hip_y = -(ext + 0.12) - 0.28 * abs(math.sin(ph * 2.0))
        lean_ = lean + 0.10 * math.sin(ph)
    elif piernas == "arrodillado":
        aN, bN, aF, bF = 0.0, -1.57, 0.25, 0.0
        hip_y = -(L_MUSLO + 0.3)
        lean_ = lean
    elif piernas == "sentado":
        aN, bN, aF, bF = 1.45, 0.0, 1.45, 0.0
        hip_y = -(L_PIERNA + 0.25)
        lean_ = lean
    else:                                                  # idle: respira y cambia el peso
        aN, bN, aF, bF = 0.04 * math.sin(ph * 0.4), 0.04 * math.sin(ph * 0.4), -0.04, -0.04
        hip_y = -(L_MUSLO + L_PIERNA) * 0.995 + 0.025 * math.sin(t * 1.9 + seed)
        lean_ = lean + 0.02 * math.sin(t * 0.9 + seed)
    hip = np.array([0.0, hip_y])
    if vista == "frente":
        _cuerpo_frente(D, R, hip, aN, bN, aF, bF, t, ph, piernas, brazos, piel, sombra_p, ropa, ropa2, col_pant, tr, falda, manga, cara, emocion, seed, lean_, obj_d, obj_i, mirar, S, objetivo)
        return
    tt_cab = 0.95 if vista == "perfil" else 0.55
    # -------- cadena de huesos
    kN = _fk(hip + np.array([0.12, 0.0]), aN, L_MUSLO)
    anN = _fk(kN, bN, L_PIERNA)
    kF = _fk(hip + np.array([-0.12, 0.0]), aF, L_MUSLO)
    anF = _fk(kF, bF, L_PIERNA)
    sh = hip + L_TORSO * np.array([math.sin(lean_), -math.cos(lean_)])
    sh_f = sh + np.array([-0.06, 0.0])
    cuello = sh + 0.30 * np.array([math.sin(lean_), -math.cos(lean_)])
    oscP = P.oscurecer(col_pant, 0.28)
    # -------- brazo lejano (detrás)
    brN, brF = _pose_brazos(brazos, ph, t, sh, lean_, objetivo, S, x, y, mirar, seed, vel)
    _brazo_cuerpo(D, sh_f, brF, P.oscurecer(ropa, 0.30) if manga != "sin" else sombra_p, sombra_p, manga, P.oscurecer(ropa, 0.30), sombra_p, 0.46, far=True)
    # -------- pierna lejana, falda / pantalón, torso, pierna cercana
    if not falda:
        _pierna(D, hip + np.array([-0.12, 0.0]), kF, anF, oscP, P.oscurecer(col_pant, 0.5), 0.52, 0.45, 0.36)
    _tronco(D, R, hip, sh, cuello, lean_, ropa, ropa2, tr, falda, ph, t, piernas, col_pant, piel, sombra_p, vista)
    if not falda:
        _pierna(D, hip + np.array([0.12, 0.0]), kN, anN, col_pant, P.oscurecer(col_pant, 0.55), 0.54, 0.47, 0.38)
    else:
        for an, col in ((anF, P.oscurecer((60, 40, 50), 0.0)), (anN, (74, 48, 56))):
            D.ell(an[0] + 0.30, an[1] - 0.05, 0.50, 0.22, col, 1.0)
    # -------- cabeza
    cab_y = 0.0
    roll = -0.5 * lean_ + (0.06 * math.sin(t * 1.3 + seed))
    if piernas in ("camina", "corre"):
        cab_y = 0.05 * math.sin(ph * 2)
    _cabeza_simple(lz, x + cuello[0] * S * mirar, y + (cuello[1] + cab_y) * S, S, R, tt_cab, piel, sombra_p, 0.2 + 0.4 * max(0.0, lean_), t, seed, cara, emocion, mirar, roll, A)
    # -------- brazo cercano (delante)
    _brazo_cuerpo(D, sh, brN, ropa if manga != "sin" else piel, piel, manga, ropa, piel, 0.50, far=False, obj=obj_d, t=t, seed=seed)
    if obj_i is not None:
        pass


def _pose_brazos(brazos, ph, t, sh, lean, objetivo, S, x, y, mirar, seed, vel):
    """Devuelve las poses (codo, mano, ang_mano) de brazo cercano y lejano en el marco del personaje."""
    def cadena(p0, ang1, ang2):
        e = _fk(p0, ang1, L_BRAZO)
        return e, _fk(e, ang2, L_ANTEBRAZO), ang2
    sw = math.sin(ph)
    if brazos == "balanceo":
        n = cadena(sh, -0.55 * sw + lean * 0.5, -0.55 * sw + lean * 0.5 + 0.30 + 0.35 * max(0.0, -sw))
        f = cadena(sh, 0.55 * sw + lean * 0.5, 0.55 * sw + lean * 0.5 + 0.30 + 0.35 * max(0.0, sw))
    elif brazos == "idle":
        n = cadena(sh, 0.05 + 0.04 * math.sin(t * 1.9 + seed), 0.12)
        f = cadena(sh, -0.05, 0.05)
    elif brazos == "arriba":
        w = 0.15 * math.sin(t * 3.0 + seed)
        n = cadena(sh, 2.7 + w, 2.9 + w)
        f = cadena(sh, 2.5 - w, 2.8 - w)
    elif brazos == "saluda":
        n = cadena(sh, 2.5, 2.6 + 0.55 * math.sin(t * 7.0 + seed))
        f = cadena(sh, 0.05, 0.1)
    elif brazos == "baila":
        n = cadena(sh, 1.9 + 0.9 * sw, 2.2 + 0.9 * sw)
        f = cadena(sh, 1.9 - 0.9 * sw, 2.2 - 0.9 * sw)
    elif brazos == "carga":
        mano = sh + np.array([1.05, 1.35])
        e, m = _ik(sh, mano, L_BRAZO, L_ANTEBRAZO, 1.0)
        n = (e, m, 1.6)
        mano2 = sh + np.array([0.85, 1.45])
        e2, m2 = _ik(sh, mano2, L_BRAZO, L_ANTEBRAZO, 1.0)
        f = (e2, m2, 1.6)
    elif brazos == "pecho":
        mano = sh + np.array([0.55, 0.85])
        e, m = _ik(sh, mano, L_BRAZO, L_ANTEBRAZO, 1.0)
        n = (e, m, 2.0)
        f = cadena(sh, 0.05, 0.1)
    elif brazos == "defensa":
        mano = sh + np.array([1.0, -0.25])
        e, m = _ik(sh, mano, L_BRAZO, L_ANTEBRAZO, 1.0)
        n = (e, m, 1.9)
        f = (e + np.array([-0.1, 0.0]), m + np.array([-0.15, 0.1]), 1.9)
    elif brazos == "labra":
        c = math.sin(ph * 0.9)
        n = cadena(sh, 1.2 - 0.9 * max(0, c), 1.5 - 1.3 * max(0, c))
        f = cadena(sh, 1.0 - 0.9 * max(0, c), 1.4 - 1.3 * max(0, c))
    elif brazos == "señala":
        if objetivo is not None:
            d = np.array([(objetivo[0] - x) * mirar / S, (objetivo[1] - y) / S]) - sh
            a_ = math.atan2(d[0], d[1])
        else:
            a_ = 2.0
        n = cadena(sh, a_, a_)
        f = cadena(sh, 0.05, 0.1)
    else:
        n = cadena(sh, 0.05, 0.1)
        f = cadena(sh, -0.05, 0.05)
    return n, f


def _tronco(D, R, hip, sh, cuello, lean, ropa, ropa2, tr, falda, ph, t, piernas, col_pant, piel, sombra_p, vista):
    d = sh - hip
    L = float(np.hypot(*d))
    u = d / L
    n = np.array([-u[1], u[0]])                       # perpendicular (hacia delante cuando va a la derecha)
    ancho_c = 1.02 if vista == "perfil" else 1.15
    ancho_h = 0.88 if vista == "perfil" else 1.0
    # torso base y sombra de la espalda
    pts = [hip - n * ancho_h, hip + n * ancho_h, sh + n * ancho_c, sh - n * ancho_c]
    D.cat([tuple(p) for p in pts], P.oscurecer(ropa, 0.30), 1.0, n=3)
    pts2 = [hip - n * (ancho_h - 0.18) + u * 0.1, hip + n * ancho_h, sh + n * ancho_c, sh - n * (ancho_c - 0.2)]
    D.cat([tuple(p) for p in pts2], ropa, 1.0, n=3)
    if tr == "coraza":
        D.cat([tuple(sh - n * 0.5 - u * 0.2), tuple(sh + n * 0.7 - u * 0.1), tuple(hip + n * 0.6 + u * 0.9), tuple(hip - n * 0.4 + u * 0.9)], P.aclarar(ropa, 0.2), 0.9, n=3)
    elif tr == "capa_plumas":
        cols = [ropa2, (222, 70, 120), (80, 200, 190), ropa2]
        for k in range(4):
            c0 = sh - u * (0.1 + k * 0.45)
            D.cat([tuple(c0 - n * 1.0), tuple(c0 + n * 0.0 + u * -0.1), tuple(c0 + n * 1.0), tuple(c0 + n * 0.8 - u * 0.5), tuple(c0 - n * 0.9 - u * 0.5)], cols[k], 1.0, n=3)
    elif tr == "habito":
        D.poly([tuple(hip + n * 0.1 + u * 1.4), tuple(hip + n * 0.1 + u * 0.2)] + [tuple(hip - n * 0.1 + u * 0.2), tuple(hip - n * 0.1 + u * 1.4)], P.oscurecer(ropa, 0.25), 0.8)
    elif tr == "bandolera":
        D.poly([tuple(sh - n * 0.9 - u * 0.1), tuple(sh - n * 0.5 + u * 0.1), tuple(hip + n * 0.9 + u * 0.2), tuple(hip + n * 0.5)], ropa2, 1.0)
    elif tr in ("huipil", "rebozo", "levita"):
        D.poly([tuple(sh - n * 0.9 - u * 0.5), tuple(sh + n * 0.9 - u * 0.5), tuple(sh + n * 0.95 - u * 0.75), tuple(sh - n * 0.95 - u * 0.75)], ropa2, 0.9)
    # cinturón / faja
    D.poly([tuple(hip - n * (ancho_h + 0.02) + u * 0.12), tuple(hip + n * (ancho_h + 0.02) + u * 0.12), tuple(hip + n * (ancho_h + 0.02) - u * 0.12), tuple(hip - n * (ancho_h + 0.02) - u * 0.12)],
           ropa2 if not falda else P.oscurecer(ropa2, 0.1), 1.0)
    # falda larga con vaivén
    if falda:
        col_f = ropa if tr == "habito" else ropa2 if tr == "huipil" else (70, 62, 110)
        sway = 0.18 * math.sin(ph) if piernas in ("camina", "corre", "baila") else 0.04 * math.sin(t * 1.5)
        D.cat([tuple(hip - n * ancho_h + u * 0.1), tuple(hip + n * ancho_h + u * 0.1), (hip[0] + 1.25 + sway, -0.35), (hip[0] + 0.1, -0.12 + 0.05 * math.sin(ph)), (hip[0] - 1.2 + sway, -0.35)], P.oscurecer(col_f, 0.08), 1.0, n=4)
        D.cat([tuple(hip - n * (ancho_h - 0.2) + u * 0.1), tuple(hip + n * ancho_h + u * 0.1), (hip[0] + 1.25 + sway, -0.35), (hip[0] + 0.2, -0.14), (hip[0] - 0.7 + sway, -0.3)], col_f, 1.0, n=4)
        D.poly([(hip[0] - 1.2 + sway, -0.35), (hip[0] + 1.25 + sway, -0.35), (hip[0] + 1.22 + sway, -0.5), (hip[0] - 1.18 + sway, -0.5)], ropa2 if tr != "huipil" else ropa, 0.9)


def _pierna(D, cad, rod, tob, col, col_zapato, r0, r1, r2):
    _capsula(D, cad, rod, r0, r1, col)
    _capsula(D, rod, tob, r1, r2, col)
    D.ell(tob[0] + 0.32, tob[1] + 0.02, 0.52, 0.24, col_zapato, 1.0)


def _brazo_cuerpo(D, sh, pose, col_manga, col_piel, manga, col_m2, col_p2, r, far=False, obj=None, t=0.0, seed=0):
    e, m, ang = pose
    largo = manga == "larga"
    _capsula(D, sh, e, r + 0.04, r, col_manga if manga != "sin" else col_piel)
    _capsula(D, e, m, r, r * 0.88, col_manga if largo else col_piel)
    D.ell(m[0], m[1], 0.34, 0.34, col_piel, 1.0)
    if obj is not None:
        obj(D, m, ang, t, seed)


def _cuerpo_frente(D, R, hip, aN, bN, aF, bF, t, ph, piernas, brazos, piel, sombra_p, ropa, ropa2, col_pant, tr, falda, manga, cara, emocion, seed, lean_, obj_d, obj_i, mirar, S, objetivo):
    """Vista frontal: cuerpo simétrico; las piernas se acortan/levantan en vez de oscilar hacia delante."""
    lz = D.lz
    sw = math.sin(ph)
    lift = 0.0
    if piernas in ("camina", "corre", "baila"):
        lift = 0.5 if piernas != "baila" else 0.7
    hipy = hip[1] - (0.10 * abs(math.sin(ph)) if lift else 0.0) - (0.25 * abs(math.sin(ph * 2)) if piernas == "baila" else 0.0)
    levL, levR = lift * max(0.0, sw), lift * max(0.0, -sw)
    hipy = -(L_MUSLO + L_PIERNA) * 0.99 + (hipy - hip[1]) + hip[1] - (-(L_MUSLO + L_PIERNA) * 0.99 - hip[1]) if False else hipy
    sh = np.array([0.0, hipy - L_TORSO])
    # brazos
    nrm, frn = _pose_brazos(brazos, ph, t, np.array([0.0, sh[1]]), lean_, objetivo, S, 0, 0, mirar, seed, 1.0)
    def lado(pose, sgn):
        e, m, ang = pose
        # en vista frontal los brazos se abren hacia los lados: el ángulo «hacia delante» se convierte en «hacia afuera»
        e2 = np.array([sgn * (1.05 + abs(e[0]) * 0.55 * (1 if e[0] >= 0 else -1) * 0.0 + e[0] * 0.65), e[1]])
        m2 = np.array([sgn * (1.1 + m[0] * 0.65), m[1]])
        return (e2, m2, ang)
    pa = lado(nrm, 1)
    pb = lado(frn, -1)
    for sgn, pose, osc in ((-1, pb, True), (1, pa, False)):
        pass
    col_m = P.oscurecer(ropa, 0.18)
    _brazo_cuerpo(D, np.array([-1.0, sh[1] + 0.1]), pb, P.oscurecer(ropa, 0.30) if manga != "sin" else sombra_p, sombra_p, manga, ropa, piel, 0.40, far=True)
    # piernas
    for sgn, lev, col in ((-1, levL, P.oscurecer(col_pant, 0.2)), (1, levR, col_pant)):
        if falda:
            break
        cad = np.array([sgn * 0.5, hipy])
        tob = np.array([sgn * 0.55, -0.1 - lev])
        rod = np.array([sgn * 0.52, (cad[1] + tob[1]) / 2 - 0.05 * lev])
        _capsula(D, cad, rod, 0.5, 0.42, col)
        _capsula(D, rod, tob, 0.42, 0.34, col)
        D.ell(tob[0] + sgn * 0.08, tob[1] + 0.02, 0.50, 0.24, P.oscurecer(col_pant, 0.55), 1.0)
    # tronco
    D.cat([(-0.95, hipy), (0.95, hipy), (1.1, sh[1]), (-1.1, sh[1])], P.oscurecer(ropa, 0.18), 1.0, n=3)
    D.cat([(-0.85, hipy), (0.95, hipy), (1.1, sh[1]), (-1.0, sh[1])], ropa, 1.0, n=3)
    if tr == "capa_plumas":
        cols = [ropa2, (222, 70, 120), (80, 200, 190), ropa2]
        for k in range(4):
            yy = sh[1] + 0.05 + k * 0.45
            D.cat([(-1.1, yy), (0.0, yy + 0.25), (1.1, yy), (0.95, yy + 0.5), (0.0, yy + 0.7), (-0.95, yy + 0.5)], cols[k], 1.0, n=3)
    elif tr == "coraza":
        D.cat([(-0.7, sh[1] + 0.2), (0.7, sh[1] + 0.2), (0.6, hipy - 0.3), (-0.6, hipy - 0.3)], P.aclarar(ropa, 0.2), 0.9, n=3)
    elif tr == "bandolera":
        D.poly([(-1.0, sh[1] + 0.1), (-0.6, sh[1] + 0.05), (1.0, hipy), (0.6, hipy)], ropa2, 1.0)
    elif tr in ("huipil", "rebozo", "levita"):
        D.poly([(-1.1, sh[1] + 0.3), (1.1, sh[1] + 0.3), (1.05, sh[1] + 0.55), (-1.05, sh[1] + 0.55)], ropa2, 0.9)
    D.poly([(-0.98, hipy + 0.1), (0.98, hipy + 0.1), (0.98, hipy - 0.12), (-0.98, hipy - 0.12)], ropa2 if not falda else P.oscurecer(ropa2, 0.1), 1.0)
    if falda:
        col_f = ropa if tr == "habito" else ropa2 if tr == "huipil" else (70, 62, 110)
        sway = 0.12 * math.sin(ph) if piernas in ("camina", "corre", "baila") else 0.03 * math.sin(t * 1.5)
        D.cat([(-0.9, hipy), (0.9, hipy), (1.3 + sway, -0.3), (0.0, -0.1 + 0.06 * math.sin(ph)), (-1.3 + sway, -0.3)], col_f, 1.0, n=4)
        D.poly([(-1.3 + sway, -0.3), (1.3 + sway, -0.3), (1.28 + sway, -0.48), (-1.28 + sway, -0.48)], ropa2 if tr != "huipil" else ropa, 0.9)
        for sgn, lev in ((-1, levL), (1, levR)):
            D.ell(sgn * 0.55, -0.12 - lev, 0.5, 0.22, (74, 48, 56), 1.0)
    # cabeza
    cuello = (0.0, sh[1] - 0.3)
    roll = 0.06 * math.sin(t * 1.3 + seed) + (0.08 * sw if piernas == "baila" else 0.0)
    _cabeza_simple(lz, D.x + 0.0, D.y + cuello[1] * D.s, D.s, R, 0.0, piel, sombra_p, 0.0, t, seed, cara, emocion, 1, roll, D.A)
    _brazo_cuerpo(D, np.array([1.0, sh[1] + 0.1]), pa, ropa if manga != "sin" else piel, piel, manga, ropa, piel, 0.43, far=False, obj=obj_d, t=t, seed=seed)


def _cabeza_simple(lz, x, y, S, R, tt, piel, sombra, bajar, t, seed, cara, emocion, mirar, roll, A):
    """Cabeza de personaje de cuerpo entero (origen = base del cuello). Pocas formas; cara según el tamaño."""
    alto_px = 2.4 * S
    if cara == "auto":
        cara = "ninguna" if alto_px < 56 else ("minima" if alto_px < 120 else "completa")
    if alto_px < 16:                                              # cabeza diminuta: disco y pelo
        lz.relleno(elipse(x, y - 1.6 * S, 1.0 * S, 1.2 * S, 0.0, 14), piel, alfa=A)
        lz.relleno(elipse(x, y - 2.3 * S, 1.05 * S, 0.75 * S, 0.0, 14), R["pelo"], alfa=A)
        return
    fw = R.get("fw", 1.0) * R.get("escala_cabeza", 1.0) ** 0.5
    with lz.grupo(x, y, 1.0, roll * mirar):
        D = _D(lz, 0.0, 0.0, S, mirar, A)
        sil = _sil(tt, fw)
        _pelo_atras(D, R, sil, tt, fw)
        D.cat([(-0.40 - 0.14 * tt, -0.9), (0.40 - 0.14 * tt, -0.9), (0.46, 0.05), (-0.46, 0.05)], P.mezcla(piel, sombra, 0.35), n=3)
        _sombreado(D, [tuple(p) for p in sil], piel, sombra, luz=(-0.07, -0.05))
        if cara != "ninguna":
            ef = (_lerp(0.43 * fw, 0.84, tt), _lerp(1.0, 0.5, tt))
            eb = (_lerp(-0.43 * fw, 0.30, tt), _lerp(1.0, 0.92, tt))
            ox = _lerp(-1.02 * fw, -0.42, tt)
            D.ell(ox, -1.5, 0.20, 0.32, P.mezcla(piel, sombra, 0.10), 1.0)
            ab = {"sorpresa": 1.2, "miedo": 1.25, "enojo": 0.75, "triste": 0.8}.get(emocion, 1.0)
            per = 3.4 + 2.4 * h01(seed, 17)
            ciclo = (t + seed * 1.7) % per
            cierre = max(0.0, 1.0 - abs(ciclo - (per - 0.1)) / 0.07) if ciclo > per - 0.2 else 0.0
            for (ex, wc) in (eb, ef):
                D.ell(ex, -1.66, 0.12 * wc, 0.15 * ab * (1 - 0.9 * cierre) + 0.01, (56, 22, 56), 1.0)
                if cara == "completa":
                    D.ell(ex + 0.035, -1.71, 0.035 * wc, 0.04, (255, 255, 255), 0.9 * (1 - cierre))
                    inc = {"enojo": 0.35, "triste": -0.3, "miedo": -0.3}.get(emocion, 0.0)
                    D.poly([(ex - 0.28 * wc, -2.02 + inc * 0.3), (ex + 0.28 * wc, -2.02 - inc * 0.3), (ex + 0.28 * wc, -1.96 - inc * 0.3), (ex - 0.28 * wc, -1.96 + inc * 0.3)], P.mezcla(R["pelo"], CEJA_OSC, 0.45), 0.9)
            if cara == "completa":
                mx, mw = _lerp(0.0, 0.64, tt), _lerp(1.0, 0.62, tt)
                _boca(D, mx, mw, 0.0, {"alegre": 0.55, "triste": -0.5, "enojo": -0.4}.get(emocion, 0.0), {"sorpresa": 0.5, "grito": 0.9, "alegre": 0.2}.get(emocion, 0.0), 0.0, t, seed, tt)
                D.ell(_lerp(-0.66 * fw, 0.12, tt), -1.12, 0.26, 0.15, (240, 96, 96), R.get("rubor", 0.3))
            if R.get("pintura"):
                for (cx_, w_) in (eb, ef):
                    for k in range(2):
                        D.poly([(cx_ - 0.25 * w_, -1.38 + k * 0.13), (cx_ + 0.25 * w_, -1.42 + k * 0.13), (cx_ + 0.25 * w_, -1.33 + k * 0.13), (cx_ - 0.25 * w_, -1.29 + k * 0.13)], (250, 220, 120) if k == 0 else (80, 200, 190), 0.9)
            if R.get("gafas") and cara == "completa":
                _gafas(D, R, eb, ef, 0.0, ox)
            mx, mw = _lerp(0.0, 0.64, tt), _lerp(1.0, 0.62, tt)
            _vello(D, R, sil, mx, mw, tt, 0.0)
        _pelo_delante(D, R, sil, tt, fw, bajar, t)
        _tocado(D, R, fw, tt, t)
