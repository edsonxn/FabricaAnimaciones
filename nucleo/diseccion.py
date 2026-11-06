# -*- coding: utf-8 -*-
"""Estilo «DISECCIÓN EN VIVO» (Edsonxn, 5-nov-2026; primer video: videos/euphoria_robots/). Doc: docs/estilo_diseccion.md.

Idea: vector plano tipo Kurzgesagt (sin contornos, 2 tonos, halos) en VERTICAL, donde la grabación REAL de la herramienta vive en
un monitor flotante y el código la «abre» como en rayos X: un barrido convierte la imagen en radiografía y deja ver el esqueleto,
las fuerzas, el centro de masa. Debajo, el mismo muñeco corre SIMULADO en Python (Verlet de verdad, mismos 7 puntos, masas y
huesos que nucleo/panel_vivo_ragdoll.js): lo que explica la voz no es una animación dibujada, es la física funcionando.

  import diseccion as D
  bg = D.fondo(t, tono)                              # float32 HxWx3: degradado + rejilla de puntos que deriva + manchas de luz
  D.monitor(lz, frame_bgr, cx, cy, w, h, t, rayos=0..1, barrido=u)   # grabación real enmarcada; barrido = radiografía de izq. a der.
  sim = D.escenario("leve")                          # Sim precalculada (30 fps): "trapo" | "rigido" | "leve" | "fuerte" | "vuela"
  D.muneco(lz, sim.en(t - t0), ox, oy, s, rayos=.6, etiquetas=1)     # el robot (Token) en plano, con su esqueleto encima
  D.flecha(lz, p0, p1, AMAR, 26, frac)  ·  D.centro_masa(lz, x, y, r)  ·  D.base(lz, x0, x1, y, dentro)
  D.titular(lz, "VERLET", y, t, t0)  ·  D.kicker(lz, "PASO 1", x, y, t, t0)  ·  D.rejilla_medida(...)
Todo es función del tiempo y determinista (se renderiza en paralelo): las simulaciones se calculan una vez al importar.
"""
import math

import cv2
import numpy as np

import plano as PL
from motor import W, H

# ---------------------------------------------------------------- paleta (RGB)
FONDO_A, FONDO_B = (16, 12, 44), (46, 26, 96)
TURQ, TURQ_O = (125, 243, 225), (44, 150, 168)
AMAR, CORAL, LILA, VERDE = (255, 206, 84), (255, 104, 120), (164, 132, 255), (120, 232, 150)
PAPEL, TINTA = (246, 244, 255), PL.TINTA
CUERPO, CUERPO_O = (232, 236, 250), (150, 156, 196)
TONOS = dict(gancho=(CORAL, LILA), pedido=(LILA, TURQ), problema=(CORAL, AMAR), verlet=(TURQ, LILA), musculos=(AMAR, CORAL),
             equilibrio=(VERDE, TURQ), mundo=(AMAR, LILA), errores=(CORAL, TURQ), cierre=(TURQ, AMAR))


def clamp(u, a=0.0, b=1.0):
    return a if u < a else b if u > b else u


def pr(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def suave(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def rebote(u, s=1.7):
    """Entrada con rebote (e_back)."""
    u = clamp(u)
    return 1 + (s + 1) * (u - 1) ** 3 + s * (u - 1) ** 2


def mezcla(a, b, u):
    return tuple(int(x + (y - x) * u) for x, y in zip(a, b))


# ---------------------------------------------------------------- fondo
_CACHE = {}


def _base_fondo():
    if "bg" not in _CACHE:
        y = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
        a, b = np.array(FONDO_A, np.float32) / 255, np.array(FONDO_B, np.float32) / 255
        bg = a * (1 - y) + b * y
        _CACHE["bg"] = np.repeat(bg, W, axis=1)
        paso = 54
        g = np.zeros((H + paso, W + paso), np.float32)
        for yy in range(0, H + paso, paso):
            for xx in range(0, W + paso, paso):
                cv2.circle(g, (xx, yy), 2, 1.0, -1, cv2.LINE_AA)
        _CACHE["rejilla"], _CACHE["paso"] = g, paso
    return _CACHE["bg"], _CACHE["rejilla"], _CACHE["paso"]


def fondo(t, tono=(TURQ, LILA), rejilla=0.11):
    """Degradado azul-violeta + rejilla de laboratorio que deriva en diagonal (nada quieto)."""
    bg, g, paso = _base_fondo()
    ox, oy = int(t * 9) % paso, int(t * 14) % paso
    rej = g[oy:oy + H, ox:ox + W][..., None]
    col = np.array(tono[0], np.float32) / 255
    return np.clip(bg + rej * col * rejilla, 0, 1)


def manchas(lz, t, tono, alfa=0.22):
    """Tres manchas de luz grandes a distinta profundidad (capa 0): dan aire y profundidad al fondo."""
    with lz.capa(0):
        for i, (bx, by, r, v) in enumerate(((.18, .22, 520, .11), (.86, .58, 640, .07), (.3, .9, 560, .09))):
            x = W * bx + 90 * math.sin(t * v * 2 + i * 2.1)
            y = H * by + 70 * math.cos(t * v * 1.6 + i)
            lz.halo(x, y, r, tono[i % 2], alfa=alfa, dureza=1.2)


# ---------------------------------------------------------------- formas
def rrect(cx, cy, w, h, r):
    return PL.rect_red(cx - w / 2, cy - h / 2, w, h, r)


def circulo(x, y, r, n=40):
    a = np.linspace(0, 2 * math.pi, n, endpoint=False)
    return np.stack([x + r * np.cos(a), y + r * np.sin(a)], 1)


def capsula(p0, p1, r0, r1, n=10):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    L = math.hypot(*d) or 1e-6
    ang = math.atan2(d[1], d[0])
    a1 = np.linspace(ang + math.pi / 2, ang + 3 * math.pi / 2, n)
    a2 = np.linspace(ang - math.pi / 2, ang + math.pi / 2, n)
    return np.concatenate([np.stack([p0[0] + r0 * np.cos(a1), p0[1] + r0 * np.sin(a1)], 1),
                           np.stack([p1[0] + r1 * np.cos(a2), p1[1] + r1 * np.sin(a2)], 1)])


def flecha(lz, p0, p1, col=AMAR, grosor=24, frac=1.0, alfa=1.0, capa=2):
    """Flecha de fuerza plana (cuerpo + punta), crece de p0 a p1 con frac."""
    if frac <= 0.01 or alfa <= 0.01:
        return
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    p1 = p0 + (p1 - p0) * clamp(frac)
    d = p1 - p0
    L = math.hypot(*d)
    if L < 2:
        return
    u = d / L
    n = np.array([-u[1], u[0]])
    cab = min(grosor * 1.9, L * 0.6)
    b = p1 - u * cab
    cuerpo = [p0 + n * grosor / 2, b + n * grosor / 2, b + n * grosor * 1.25, p1, b - n * grosor * 1.25, b - n * grosor / 2, p0 - n * grosor / 2]
    with lz.capa(capa):
        lz.relleno(np.array(cuerpo) + [3, 5], (10, 8, 30), alfa=0.35 * alfa)
        lz.relleno(np.array(cuerpo), col, alfa=alfa)
        lz.relleno(np.array([p0 + n * grosor / 2, b + n * grosor / 2, b + n * grosor * 0.05, p0 + n * grosor * 0.05]),
                   PL.aclarar(col, 0.35), alfa=alfa)


def centro_masa(lz, x, y, r=22, alfa=1.0, giro=0.0, capa=2):
    """Símbolo clásico del centro de masa: círculo en cuartos alternos."""
    if alfa <= 0.01:
        return
    with lz.capa(capa):
        lz.halo(x, y, r * 3.2, PAPEL, alfa=0.35 * alfa)
        lz.relleno(circulo(x, y, r + 4), TINTA, alfa=alfa)
        lz.relleno(circulo(x, y, r), PAPEL, alfa=alfa)
        for k in (0, 2):
            a = np.linspace(giro + k * math.pi / 2, giro + (k + 1) * math.pi / 2, 12)
            lz.relleno(np.concatenate([[[x, y]], np.stack([x + r * np.cos(a), y + r * np.sin(a)], 1)]), TINTA, alfa=alfa)


def base(lz, x0, x1, y, dentro=True, alfa=1.0, capa=2):
    """Base de apoyo entre los pies: verde si el centro de masa cae dentro, coral si se sale."""
    if alfa <= 0.01:
        return
    col = VERDE if dentro else CORAL
    with lz.capa(capa):
        lz.relleno(rrect((x0 + x1) / 2, y, abs(x1 - x0) + 28, 16, 8), col, alfa=0.85 * alfa)
        lz.halo((x0 + x1) / 2, y, abs(x1 - x0) * 0.8 + 60, col, alfa=0.35 * alfa)


def punteada(lz, p0, p1, col=PAPEL, ancho=4, alfa=0.8, fase=0.0, capa=2):
    with lz.capa(capa):
        PL.discontinua(lz, np.array([p0, p1], float), col + (int(255 * alfa),), ancho=ancho, largo=18, hueco=12, fase=fase)


# ---------------------------------------------------------------- texto
def titular(lz, texto, y, t, t0, px=132, col=PAPEL, x=None, sale=None):
    """Palabra clave GIGANTE con entrada de rebote (y salida rápida si se da `sale`)."""
    u = rebote(pr(t, t0, t0 + 0.42))
    if sale is not None:
        u *= 1 - suave(pr(t, sale, sale + 0.25))
    if u <= 0.01:
        return
    PL.rotulo(lz, W / 2 if x is None else x, y, texto, px=px, k=u, color=col, sombra=0.5)


def kicker(lz, texto, x, y, t, t0, fondo=AMAR, px=34, sale=None):
    u = rebote(pr(t, t0, t0 + 0.35))
    if sale is not None:
        u *= 1 - suave(pr(t, sale, sale + 0.2))
    PL.pastilla(lz, x, y, texto, px=px, k=u, fondo=fondo, color=TINTA)


# ---------------------------------------------------------------- monitor con la grabación real
def _rayos_x(rgb):
    """Radiografía: luminancia invertida, teñida de turquesa, con líneas de barrido."""
    g = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
    inv = 1 - g
    out = np.stack([inv * 0.35, inv * 0.95, inv * 0.88], -1) * 0.85 + 0.04
    out[::4] *= 0.78
    bordes = cv2.Canny(rgb, 60, 140).astype(np.float32)[..., None] / 255
    out = out * (1 - bordes) + bordes * np.array([0.9, 1.0, 0.98], np.float32)
    return np.clip(out * 255, 0, 255).astype(np.uint8)


def monitor(lz, frame_bgr, cx, cy, w, h, t, rayos=0.0, barrido=None, etiqueta="GRABACIÓN REAL", alfa=1.0, k=1.0, rot=0.0,
            borde=LILA, capa=1):
    """La grabación real en un monitor flotante (sombra, bisel de 2 tonos, brillo arriba, etiqueta con punto rojo de EN VIVO).
    rayos = 0..1 mezcla de radiografía en toda la pantalla; barrido = 0..1 posición de la barra (a la izquierda, radiografía)."""
    if alfa <= 0.01 or k <= 0.01:
        return
    fh, fw = frame_bgr.shape[:2]
    rgb = cv2.cvtColor(frame_bgr, cv2.COLOR_BGR2RGB)
    if rayos > 0.01 or barrido is not None:
        rx = _rayos_x(rgb)
        m = np.full((fh, fw), rayos, np.float32)
        if barrido is not None:
            xb = int(fw * clamp(barrido))
            m[:, :xb] = 1.0
        rgb = (rgb * (1 - m[..., None]) + rx * m[..., None]).astype(np.uint8)
    spr = np.dstack([rgb, np.full((fh, fw), 255, np.uint8)])
    flota = 6 * math.sin(t * 1.3)
    with lz.capa(capa), lz.grupo(cx, cy + flota, k, rot=rot):
        lz.relleno(rrect(0, 26, w + 40, h + 40, 40), (6, 4, 24), alfa=0.45 * alfa)
        lz.halo(0, 0, max(w, h) * 0.75, borde, alfa=0.18 * alfa)
        lz.degradado(rrect(0, 0, w + 30, h + 30, 38), PL.aclarar(borde, 0.25), PL.oscurecer(borde, 0.45), (0, -h / 2), (0, h / 2), alfa=alfa)
        with lz.recorte(rrect(0, 0, w, h, 26)):
            lz.pegar(spr, 0, 0, k=w / fw * 1.0, alfa=alfa)
            if barrido is not None and 0.0 < barrido < 1.0:
                xb = -w / 2 + w * barrido
                lz.relleno(np.array([[xb - 3, -h / 2], [xb + 3, -h / 2], [xb + 3, h / 2], [xb - 3, h / 2]]), TURQ, alfa=alfa)
                lz.halo(xb, 0, h * 0.55, TURQ, alfa=0.5 * alfa)
            lz.relleno(np.array([[-w / 2, -h / 2], [w / 2, -h / 2], [w / 2, -h / 2 + 10], [-w / 2, -h / 2 + 10]]), PAPEL, alfa=0.12 * alfa)
        if etiqueta:
            from motor import ancho_texto
            px = 28
            ew = ancho_texto(etiqueta, "geo", px) + 74
            x0, y0 = -w / 2 + 24 + ew / 2, -h / 2 + 34
            lz.relleno(rrect(x0, y0, ew, 48, 24), (14, 10, 40), alfa=0.78 * alfa)
            parpa = 0.55 + 0.45 * (math.sin(t * 6) > -0.2)
            lz.relleno(circulo(x0 - ew / 2 + 26, y0, 9), CORAL, alfa=parpa * alfa)
            lz.texto(etiqueta, x0 + 14, y0 + 1, px, "geo", color=PAPEL, borde=None, alfa=alfa, temblor=0.0)


# ---------------------------------------------------------------- el muñeco simulado (mismo modelo que panel_vivo_ragdoll.js)
CAB, PEC, CAD, MI, MD, PI, PD = range(7)
NOMBRES = ("cabeza", "pecho", "cadera", "mano", "mano", "pie", "pie")
PARADO = np.array([[0, -45], [0, -25], [0, -11], [-15, -14], [15, -14], [-6, -2.6], [6, -2.6]], float)
RAD = np.array([16, 11, 9, 3.4, 3.4, 2.6, 2.6])
MASA = np.array([3, 4, 4, .6, .6, .8, .8])
HUESOS = [(CAB, PEC, 20, 20), (PEC, CAD, 14, 14), (CAB, CAD, 30, 34.5), (PEC, MI, 7, 21), (PEC, MD, 7, 21), (CAD, PI, 6, 11),
          (CAD, PD, 6, 11), (PI, PD, 3, 20)]
HZ, GRAV = 180, 820.0


class Sim:
    """Verlet a 180 Hz, huesos con largo mínimo y máximo, músculos (resortes hacia una pose; k 0 = trapo, 1 = animación),
    equilibrio por centro de masa con paso de captura, reflejo de cubrirse la cabeza. Se graba a 30 cuadros/s."""

    def __init__(self, x0=0.0, k=0.75, ancla="pies", equilibrio=True, suelo=0.0, pared=None):
        self.P = PARADO.copy()
        self.P[:, 0] += x0
        self.Q = self.P.copy()
        self.k, self.ancla, self.eq, self.suelo, self.pared = k, ancla, equilibrio, suelo, pared
        self.t, self.cuadros, self.info = 0.0, [], []
        self.extra = {}                 # objetivos extra por punto (p. ej. la mano del error)
        self.paso_pie = None            # (pie, x0, x1, t0, dur)
        self.cayendo, self.reflejo, self.inclina = False, 0.0, 0.0
        self.eventos = []               # (t, fn)

    # -- herramientas
    def empuja(self, t, vx, vy=0.0, puntos=(CAB, PEC, CAD, MI, MD)):
        def f(s):
            for i in puntos:
                s.Q[i] -= np.array([vx, vy]) / HZ
        self.eventos.append((t, f))

    def en_t(self, t, fn):
        self.eventos.append((t, fn))

    def com(self):
        return (self.P * MASA[:, None]).sum(0) / MASA.sum()

    def _objetivos(self):
        if self.ancla == "cadera":          # el error del 5-nov: la meta se mide desde el propio cuerpo y viaja con él
            a = np.array([self.P[CAD, 0], self.P[CAD, 1] + 11])
        else:
            a = np.array([(self.P[PI, 0] + self.P[PD, 0]) / 2, self.suelo])
        T = PARADO + a
        T[CAB, 0] -= self.inclina * 9
        T[PEC, 0] -= self.inclina * 4
        if abs(self.inclina) > 0.05:      # brazos abiertos al tambalearse
            T[MI] = a + [-24, -30 - 6 * abs(self.inclina)]
            T[MD] = a + [24, -30 - 6 * abs(self.inclina)]
        if self.reflejo > 0:               # manos a la cabeza
            for m in (MI, MD):
                T[m] = T[m] * (1 - self.reflejo) + (self.P[CAB] + [0, 6]) * self.reflejo
        for i, v in self.extra.items():
            T[i] = (self.P[PEC] if self.ancla == "cadera" else a + [0, -25]) + v
        return T

    def _paso(self):
        dt = 1 / HZ
        for te, fn in list(self.eventos):
            if te <= self.t:
                fn(self)
                self.eventos.remove((te, fn))
        V = (self.P - self.Q) * 0.996
        self.Q = self.P.copy()
        self.P = self.P + V + np.array([0, GRAV]) * dt * dt
        # músculos
        k = 0.0 if self.cayendo and self.reflejo < 0.01 else self.k
        if k > 0:
            T = self._objetivos()
            g = 0.055 * k
            mov = [CAB, PEC, CAD, MI, MD]
            self.P[mov] += (T[mov] - self.P[mov]) * g
            if self.ancla == "cadera":
                self.P[[PI, PD]] += (T[[PI, PD]] - self.P[[PI, PD]]) * g * 0.6
        # paso de captura en curso
        if self.paso_pie is not None:
            pie, xa, xb, t0, dur = self.paso_pie
            u = clamp((self.t - t0) / dur)
            self.P[pie, 0] = xa + (xb - xa) * suave(u)
            self.P[pie, 1] = self.suelo - RAD[pie] - 9 * math.sin(math.pi * u)
            self.Q[pie] = self.P[pie]
            if u >= 1:
                self.paso_pie = None
        # huesos (largo mínimo y máximo)
        w = 1 / MASA
        for _ in range(4):
            for a, b, lo, hi in HUESOS:
                d = self.P[b] - self.P[a]
                L = math.hypot(*d) or 1e-6
                obj = lo if L < lo else hi if L > hi else None
                if obj is None:
                    continue
                c = d * (L - obj) / L / (w[a] + w[b])
                if self.paso_pie is not None and b == self.paso_pie[0]:
                    self.P[a] += c * (w[a] + w[b])
                else:
                    self.P[a] += c * w[a]
                    self.P[b] -= c * w[b]
            # suelo con fricción
            for i in range(7):
                lim = self.suelo - RAD[i]
                if self.P[i, 1] > lim:
                    self.P[i, 1] = lim
                    fr = 0.25 if i in (PI, PD) else 0.6
                    self.Q[i, 0] = self.P[i, 0] - (self.P[i, 0] - self.Q[i, 0]) * fr
                    self.Q[i, 1] = self.P[i, 1]
            if self.pared is not None:
                for i in range(7):
                    if self.P[i, 0] + RAD[i] > self.pared:
                        self.P[i, 0] = self.pared - RAD[i]
        # equilibrio: centro de masa contra la base de los pies
        c = self.com()
        v = (self.P - self.Q)[:, 0] @ MASA / MASA.sum() * HZ
        cp = c[0] + v * math.sqrt(max(1.0, self.suelo - c[1]) / GRAV)   # el motor real usa velocidad · 0,2 s con pasos limitados y músculos que suben en 1,2 s
        x0, x1 = sorted((self.P[PI, 0], self.P[PD, 0]))
        fuera = cp - x1 if cp > x1 + 3 else cp - x0 if cp < x0 - 3 else 0.0
        self.inclina += (clamp(fuera / 14, -1, 1) - self.inclina) * 0.04
        if self.eq and not self.cayendo and self.k > 0:
            if abs(fuera) > 38:
                self.cayendo = True
                self.reflejo = 1.0
                self.k = 0.0
                self.paso_pie = None
            elif abs(fuera) > 3 and self.paso_pie is None:
                d = 1 if fuera > 0 else -1
                pies = sorted((PI, PD), key=lambda p: self.P[p, 0] * d)
                pie = pies[0]                     # el de atrás respecto a la caída pasa adelante
                destino = cp + d * 7
                self.paso_pie = (pie, self.P[pie, 0], destino, self.t, 0.2)    # el real: 170 ms, 1-4 pasos al azar
        if self.cayendo:
            self.reflejo = max(0.0, self.reflejo - 0.12 / HZ)
        self.t += dt
        return c, cp, (x0, x1), fuera

    def correr(self, dur, fps=30):
        n = int(round(dur * HZ))
        cada = HZ / fps
        sig = 0.0
        for i in range(n):
            c, cp, b, fuera = self._paso()
            if i >= sig:
                self.cuadros.append(self.P.copy())
                self.info.append(dict(com=c.copy(), cp=cp, base=b, fuera=fuera, cae=self.cayendo, paso=self.paso_pie is not None,
                                      inclina=self.inclina))
                sig += cada
        self.fps = fps
        return self

    def en(self, t):
        i = int(clamp(t * self.fps, 0, len(self.cuadros) - 1))
        return self.cuadros[i]

    def dato(self, t):
        return self.info[int(clamp(t * self.fps, 0, len(self.info) - 1))]


def escenario(nombre, dur=6.0):
    """Experimentos fijos (deterministas) que se ven en el video."""
    clave = (nombre, dur)
    if clave in _CACHE:
        return _CACHE[clave]
    if nombre == "trapo":                     # Verlet + huesos, sin músculos: se desarma
        s = Sim(k=0.0, equilibrio=False)
        s.empuja(0.05, 40)
    elif nombre == "rigido":                  # animación: fuerza 1, sin equilibrio; el empujón casi no le hace nada
        s = Sim(k=1.0, equilibrio=False)
        s.k = 18.0
        s.empuja(0.8, 260)
    elif nombre == "leve":                    # empujón leve: tambalea, paso de captura y se queda parado
        s = Sim(k=0.8)
        s.empuja(0.7, 150)
    elif nombre == "fuerte":                  # empujón fuerte: pasos que no alcanzan, se cae y se cubre la cabeza
        s = Sim(k=0.8)
        s.empuja(0.7, 520, -60)
    elif nombre in ("vuela", "arreglado"):    # el error del 5-nov: cae a un hoyo y el reflejo «aletea» jala las manos a 32 sobre
        alto = 32.0 if nombre == "vuela" else 18.0   # el pecho con un brazo de 21: la meta viaja con el cuerpo y lo saca volando.
        s = Sim(k=0.8, ancla="cadera", equilibrio=False, suelo=1e4)     # Arreglo real: las manos a <= 18 del pecho.
        s.extra = {MI: np.array([-7.0, -alto]), MD: np.array([7.0, -alto])}
    else:
        raise KeyError(nombre)
    s.correr(dur)
    _CACHE[clave] = s
    return s


# ---------------------------------------------------------------- dibujo del muñeco (Token en plano)
def muneco(lz, P, ox, oy, s=6.0, col=TURQ, rayos=0.0, etiquetas=0.0, alfa=1.0, t=0.0, cara="normal", capa=2, d=1):
    """Dibuja los 7 puntos como robot plano (cápsulas de 2 tonos, cabeza-pantalla con ojos) y, con rayos > 0, su esqueleto:
    huesos blancos y puntos amarillos que brillan; etiquetas > 0 pone el nombre de cada punto."""
    if alfa <= 0.01:
        return
    Q = np.asarray(P, float) * s + [ox, oy]
    cu = alfa * (1 - 0.72 * rayos)
    claro, oscuro = CUERPO, CUERPO_O
    with lz.capa(capa):
        lz.relleno(np.array([[Q[:, 0].min() - 20, oy - 4], [Q[:, 0].max() + 20, oy - 4], [Q[:, 0].max() + 30, oy + 10],
                             [Q[:, 0].min() - 30, oy + 10]]), (8, 6, 26), alfa=0.25 * alfa)
        if cu > 0.01:
            # extremidades de atrás (más oscuras)
            lz.relleno(capsula(Q[PEC], Q[MI], 3.2 * s, 2.6 * s), oscuro, alfa=cu)
            lz.relleno(capsula(Q[CAD], Q[PI], 3.4 * s, 2.8 * s), oscuro, alfa=cu)
            # torso
            lz.relleno(capsula(Q[PEC], Q[CAD], 7.0 * s, 6.0 * s), claro, alfa=cu)
            lz.relleno(capsula(Q[PEC] + [-2.0 * s * d, 0], Q[CAD] + [-2.0 * s * d, 0], 4.4 * s, 3.7 * s), PL.oscurecer(claro, 0.12), alfa=cu)
            pecho = Q[PEC] * 0.55 + Q[CAD] * 0.45
            lz.relleno(circulo(pecho[0], pecho[1], 2.6 * s), col, alfa=cu)
            lz.halo(pecho[0], pecho[1], 7 * s, col, alfa=0.45 * cu)
            # cabeza-pantalla, girada con el cuello
            dv = Q[CAB] - Q[PEC]
            ang = math.atan2(dv[1], dv[0]) + math.pi / 2
            with lz.grupo(Q[CAB][0], Q[CAB][1], 1.0, rot=ang):
                lz.relleno(PL.rect_red(-12 * s, -10.5 * s, 24 * s, 21 * s, 7 * s), claro, alfa=cu)
                lz.relleno(PL.rect_red(-9.4 * s, -7.4 * s, 18.8 * s, 14.4 * s, 5 * s), (22, 20, 54), alfa=cu)
                parp = 0.15 if (t % 3.1) < 0.12 else 1.0
                if cara == "x":
                    for ex in (-5, 5):
                        for sg in (-1, 1):
                            lz.trazo(np.array([[ex * s - 2.2 * s, -2.2 * s * sg], [ex * s + 2.2 * s, 2.2 * s * sg]]), col, 1.6 * s, afinar=False)
                else:
                    for ex in (-5, 5):
                        lz.relleno(rrect(ex * 0.85 * s + 1.0 * s * d, 0, 3.2 * s, 5.6 * s * parp, 1.6 * s), col, alfa=cu)
                lz.relleno(rrect(0, -12.8 * s, 1.6 * s, 4.6 * s, 0.8 * s), oscuro, alfa=cu)
                lz.relleno(circulo(0, -15.6 * s, 2.2 * s), CORAL, alfa=cu)
                lz.halo(0, -15.6 * s, 6 * s, CORAL, alfa=0.5 * cu)
            # extremidades de delante
            lz.relleno(capsula(Q[CAD], Q[PD], 3.4 * s, 2.8 * s), claro, alfa=cu)
            lz.relleno(capsula(Q[PEC], Q[MD], 3.2 * s, 2.6 * s), claro, alfa=cu)
            for i in (MI, MD):
                lz.relleno(circulo(Q[i, 0], Q[i, 1], 3.6 * s), col if i == MD else TURQ_O, alfa=cu)
            for i in (PI, PD):
                lz.relleno(rrect(Q[i, 0] + 1.5 * s * d, Q[i, 1] + 0.6 * s, 9 * s, 4.4 * s, 2.2 * s), oscuro if i == PI else (70, 66, 120), alfa=cu)
        if rayos > 0.01:
            for a, b, lo, hi in HUESOS:
                lz.trazo(np.array([Q[a], Q[b]]), PAPEL + (int(230 * rayos * alfa),), 1.3 * s, afinar=False)
            for i in range(7):
                lz.halo(Q[i, 0], Q[i, 1], RAD[i] * s * 0.9 + 16, AMAR, alfa=0.55 * rayos * alfa)
                lz.relleno(circulo(Q[i, 0], Q[i, 1], max(2.2, RAD[i] * 0.32) * s), AMAR, alfa=rayos * alfa)
                lz.relleno(circulo(Q[i, 0], Q[i, 1], max(1.0, RAD[i] * 0.14) * s), PAPEL, alfa=rayos * alfa)
        if etiquetas > 0.01:
            lados = {CAB: (1, -1), PEC: (1, 0), CAD: (1, 0.4), MI: (-1, 0), MD: (1, 0), PI: (-1, 1), PD: (1, 1)}
            for i in range(7):
                sx, sy = lados[i]
                p1 = Q[i] + [sx * 120, sy * 46]
                u = rebote(clamp(etiquetas * 7 - i))
                if u <= 0.01:
                    continue
                PL.linea_llamada(lz, Q[i], p1, frac=u, col=PAPEL, ancho=2.5)
                PL.pastilla(lz, p1[0] + sx * 60, p1[1], NOMBRES[i], px=28, k=u, fondo=PAPEL, color=TINTA)
    return Q
