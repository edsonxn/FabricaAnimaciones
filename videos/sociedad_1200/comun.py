# -*- coding: utf-8 -*-
"""Utilidades comunes de «Las 1.200» (noir color): geometría, rótulos de énfasis, letreros a máquina, reflejos, video real
teñido por rampa, chispas, sacudidas de cámara y parpadeos. Nada aquí dibuja un decorado: eso va en mundos_*.py y props_s.py."""
import math

import cv2
import numpy as np

import noir as N
import noir_color as NC
from motor import H, W, clamp01, e_inout
from toon import elipse_

IMPACT = "C:/Windows/Fonts/impact.ttf"


def rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float)


def rot(P, a, c=(0.0, 0.0)):
    P = np.asarray(P, float).reshape(-1, 2)
    c = np.asarray(c, float)
    ca, sa = math.cos(a), math.sin(a)
    Q = P - c
    return np.stack([Q[:, 0] * ca - Q[:, 1] * sa, Q[:, 0] * sa + Q[:, 1] * ca], 1) + c


def T_obj(cx, cy, ang=0.0, s=1.0, sx=1.0):
    """Transformación local -> mundo de un objeto (escala, espejo sx=-1 y giro alrededor de su origen)."""
    c = np.array([cx, cy], float)

    def f(P):
        P = np.asarray(P, float).reshape(-1, 2) * (s * sx, s)
        return rot(P, ang) + c
    return f


def a_pantalla(h, P, prof=1.0):
    M = h.matriz_capa(prof)
    return np.asarray(P, float) @ M[:2, :2].T + M[:2, 2]


def ambiente(h, k, col="luna"):
    h.ambiente[:] = np.array(h.pal[col], np.float32) * k


def lerp(a, b, u):
    return a + (b - a) * u


def ventana(t, t0, t1, ent=0.25, sal=0.25):
    """0..1..0: entra en t0 (ent s) y sale en t1 (sal s)."""
    return clamp01((t - t0) / max(1e-3, ent)) * (1 - clamp01((t - t1) / max(1e-3, sal)))


# ====================================================================== rótulos
def banda(h, s, cx, cy, px, t, t0, claro=False, sem=0, fuente=None, mundo=False, sale=None, acento=False):
    """Rótulo de énfasis sólido (negro con letra crema, crema con letra negra o ACENTO rojo apagado) que entra con un golpe."""
    if t < t0 or (sale is not None and t > sale):
        return
    u = clamp01((t - t0) / 0.14)
    k = 1.0 + 0.25 * (1 - u) ** 2
    fu = fuente or N.FUENTE_SELLO
    im, _ = N._txt_img(s, px, fu, 3.0)
    an, al = (im.shape[1] + px * 0.9) * k, (px * 1.5) * k
    fondo, rp, tono = (228, "papel", 0.05) if claro else ((120, "vino", 0.95) if acento else (10, "personaje", 0.94))

    def pintar(cx, cy):
        h.pieza(rect(cx - an / 2, cy - al / 2, an, al), fondo, sem + 770, w=5, luz=(0, -1), d=4, sombra=0, trama=0,
                jit=0.6, rampa=rp)
        h.luz_fija(rect(cx - an / 2 - 4, cy - al / 2 - 4, an + 8, al + 8), 0.95)
        N.texto_maquina(h, s, cx, cy, px * k, t, -99, cps=1e9, tono=tono, centro=True, fuente=fu, track=3.0, encuadrar=False, ang=0.0, ancho_max=1e5)
    if mundo:
        pintar(cx, cy)
    else:
        with h.capa(0.0):
            pintar(min(max(cx, an / 2 + 36), W - an / 2 - 36), min(max(cy, al / 2 + 36), H - al / 2 - 36))


def cinta(h, s, x, y, px, t, t0, cps=28.0, sem=0, ang=-0.02, sale=None, esquina="izq"):
    """Rótulo de lugar/fecha: tira de cinta de rotuladora (papel crema) que se pega y se escribe a máquina. En pantalla (fijo)."""
    if t < t0 or (sale is not None and t > sale + 0.3):
        return
    a = clamp01((t - t0) / 0.2)
    if sale is not None and t > sale:
        a = min(a, 1 - clamp01((t - sale) / 0.3))
    im, _ = N._txt_img(s, px, N.FUENTE_MAQ, 1.0)
    an, al = im.shape[1] + px * 1.0, px * 1.7
    with h.capa(0.0):
        x0 = x if esquina == "izq" else x - an
        c = np.array([x0 + an / 2, y])
        P = rot(rect(x0, y - al / 2, an * (0.15 + 0.85 * a), al), ang, c)
        h.pieza(P, 214, sem + 880, w=3, luz=(0.2, -1), d=5, sombra=0.25, trama=0, rim=0, jit=0.5, rampa="papel")
        h.luz_fija(rot(rect(x0 - 6, y - al / 2 - 6, an + 12, al + 12), ang, c), 0.93)
        if a >= 1:
            N.texto_maquina(h, s, x0 + px * 0.5, y - px * 0.62, px, t, t0 + 0.2, cps=cps, tono=np.array(h.pal["tinta"]) * 2.0,
                            fuente=N.FUENTE_MAQ, track=1.0, encuadrar=False, ang=ang, ancho_max=1e5)


def cartel(h, s, cx, cy, px, t, t0=-99, cps=1e9, tono=0.06, ang=0.0, fuente=None, fondo=212, rampa="papel", sem=0, pad=0.7,
           marco=True, luz_k=None, w=4):
    """Letrero (placa, etiqueta, cartel en una puerta) EN EL MUNDO: papel o chapa con el texto paralelo y dentro."""
    fu = fuente or N.FUENTE_MAQ
    im, _ = N._txt_img(s, px, fu, 1.5)
    an, al = im.shape[1] - 20 + px * pad * 2, px * (1.0 + pad * 1.6)
    P = rot(rect(cx - an / 2, cy - al / 2, an, al), ang, (cx, cy))
    if marco:
        h.pieza(P, fondo, sem + 990, w=w, luz=(0.2, -1), d=4, sombra=0.3, trama=0, rim=0.3, jit=0.4, rampa=rampa)
    if luz_k is not None:
        h.luz_fija(rot(rect(cx - an / 2 - 4, cy - al / 2 - 4, an + 8, al + 8), ang, (cx, cy)), luz_k)
    N.soporte(h, cx, cy, an, al, ang, 1.0, margen=px * 0.3)
    N.texto_maquina(h, s, cx, cy, px, t, t0, cps=cps, tono=tono, centro=True, fuente=fu, track=1.5, encuadrar=False, ang=0.0, ancho_max=1e5)


# ====================================================================== suelo mojado, parpadeos, brasas
def reflejar(h, t, y_mundo, k=0.32):
    """Suelo mojado: refleja lo que hay sobre y_mundo (también la emisión con su color)."""
    ys = h.tf(np.array([[0, y_mundo]]))[0][1]
    if not (40 < ys < H - 20):
        return
    N.reflejo(h.img, ys, k=k, t=t, onda=4.0, desv=3.0)
    if h._E is not None:
        N.reflejo(h._E, ys, k=k * 0.9, t=t, onda=4.0, desv=3.0)
        Ec = h._color_emision()
        y = int(ys)
        alto = min(H - y, y)
        Ec[y:y + alto] = Ec[y - alto:y][::-1]


def parpadeo(t, eventos=(), sem=0):
    """Intensidad de un tubo viejo: zumbido fino y apagones cortos (eventos = (t0, dur))."""
    v = 0.93 + 0.05 * math.sin(t * 113 + sem) * math.sin(t * 7.1 + sem)
    for t0, d in eventos:
        if t0 <= t < t0 + d:
            u = (t - t0) / d
            v *= 0.08 + 0.5 * (math.sin(u * 37) > 0.4) * (u > 0.5)
    return v


def brasa(h, tip, b):
    q = np.array([[tip[0] - 3, tip[1] - 3], [tip[0] + 3, tip[1] - 3], [tip[0] + 3, tip[1] + 3], [tip[0] - 3, tip[1] + 3]])
    h.emitir(q, 0.9 + 0.5 * b, col=(1.0, 0.38, 0.10))
    h.luz_radial(tip[0], tip[1], 60 + 110 * b, (1.0, 0.45, 0.15), k=0.5 + 0.9 * b)


def temblor(t, golpes, amp=14.0, f=21.0, dec=7.0):
    """Sacudida de cámara (dx, dy) tras cada golpe t0 (o (t0, amp))."""
    dx = dy = 0.0
    for g in golpes:
        t0, a = (g, amp) if np.ndim(g) == 0 else g
        d = t - t0
        if 0 <= d < 1.2:
            e = a * math.exp(-d * dec)
            dx += e * math.sin(d * f * 6.28 * 0.5 + 1.3)
            dy += e * math.cos(d * f * 6.28 * 0.37)
    return dx, dy


# ====================================================================== partículas
def chispas(h, t, x, y, t0, dur=1.2, n=26, vel=520.0, sem=0, col=(1.0, 0.55, 0.15), ang=-math.pi / 2, abre=1.6, grav=900.0,
            continuo=False, k=1.0):
    """Chispas que saltan de (x, y): trazos emisivos que caen con gravedad. continuo=True: chorro sostenido (soldadura)."""
    if t < t0:
        return
    rng = np.random.default_rng(sem)
    for i in range(n):
        if continuo:
            per = rng.uniform(0.35, 0.8)
            fase = rng.uniform(0, per)
            u = ((t - t0) + fase) % per
            if t - t0 > dur:
                continue
        else:
            u = t - t0 - rng.uniform(0, 0.08)
            if u < 0:
                continue
        vida = rng.uniform(0.25, 0.75)
        if u > vida:
            continue
        a = ang + rng.uniform(-abre / 2, abre / 2)
        v = vel * rng.uniform(0.4, 1.2)
        px = x + math.cos(a) * v * u
        py = y + math.sin(a) * v * u + 0.5 * grav * u * u
        qx = px - math.cos(a) * v * 0.025
        qy = py - (math.sin(a) * v + grav * u) * 0.025
        e = (1 - u / vida) * k
        P = np.array([[px, py], [qx, qy], [qx + 2, qy + 2], [px + 2, py + 2]])
        h.emitir(P, 1.4 * e, col=col, blur=0.8)


def polvo_cae(h, t, x0, x1, y0, t0, dur=2.0, n=40, sem=0):
    """Polvo / yeso que cae de un golpe (aditivo, brilla con la luz)."""
    if t < t0 or t > t0 + dur + 1.0:
        return
    A = h.aditivo()
    rng = np.random.default_rng(sem)
    for i in range(n):
        u = t - t0 - rng.uniform(0, dur * 0.5)
        if u < 0:
            continue
        x = rng.uniform(x0, x1) + 20 * math.sin(u * 2 + i)
        y = y0 + 60 * u + 180 * u * u
        P = h.a_pant(np.array([[x, y]]))[0]
        a = 0.5 * math.exp(-u * 1.2)
        cv2.circle(A, (int(P[0]), int(P[1])), 1, a, -1, cv2.LINE_AA)


# ====================================================================== video real teñido por rampa
def clip_color(h, nombre, t, t_ini, rampa="lejos", **kw):
    """N.clip_noir (tinta y aguada) y luego cada gris se lee en la rampa (el clip toma el color del plano)."""
    N.clip_noir(h, nombre, t, t_ini, **kw)
    g = np.clip(h.img[..., 0] * 255, 0, 255).astype(np.uint8)
    h.img[:] = NC.lut(rampa)[g]


def clip_en(h, nombre, t, t_ini, caja, rampa="vidrio_verde", emis=0.45, vel=1.0, inicio=0.0, z=1.0, col=None, tinta=0.5):
    """Video real dentro de una pantalla del mundo: caja = (x, y, w, hh) del mundo; tinta + rampa; la pantalla emite."""
    from docu_fx import Clip
    clip = Clip.abrir(nombre)
    lo, hi = N._niveles(nombre, clip)
    idx = int((inicio + max(0.0, t - t_ini) * vel) * clip.fps)
    f = clip.frame(idx)
    g = cv2.cvtColor(f, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255.0
    g = np.clip((g - lo) / max(1e-3, hi - lo), 0, 1)
    x, y, w, hh = caja
    Q = h.tf(np.array([[x, y], [x + w, y], [x + w, y + hh], [x, y + hh]], float))
    # recorte centrado del clip al aspecto de la caja
    asp = w / hh
    ch, cw = g.shape
    if cw / ch > asp:
        nw = int(ch * asp / z)
        nh = int(ch / z)
    else:
        nw = int(cw / z)
        nh = int(cw / asp / z)
    x0, y0 = (cw - nw) // 2, (ch - nh) // 2
    src = np.float32([[x0, y0], [x0 + nw, y0], [x0 + nw, y0 + nh], [x0, y0 + nh]])
    M = cv2.getPerspectiveTransform(src, np.float32(Q))
    gw = cv2.warpPerspective(g, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    mk = np.zeros((H, W), np.float32)
    cv2.fillConvexPoly(mk, np.rint(Q).astype(np.int32), 1.0, cv2.LINE_AA)
    gw = N.tinta_de_foto(gw, tinta, 0.3, 0.3, h.dib % 3) * mk
    v = NC.lut(rampa)[np.clip(gw * 255, 0, 255).astype(np.uint8)]
    a = mk[..., None]
    h.img *= 1 - a
    h.img += v * a
    E = h.emisivo()
    E += gw * emis * mk
    h.teñir_emision(mk * 0.9, 0, 0, col if col is not None else h.pal["verde"])


def rejilla_luces(h, xs, ys, tam, v=1.0, col=None, prof=1.0, cara=False):
    """Muchas luces pequeñas (pantallas vistas de lejos) dibujadas DIRECTO en la capa emisiva con cv2 (miles por cuadro, barato):
    xs, ys = arreglos de centros en el mundo; tam = (ancho, alto) en px del mundo."""
    import cv2 as _cv
    M = h.matriz_capa(prof)
    X = xs * M[0, 0] + ys * M[0, 1] + M[0, 2]
    Y = xs * M[1, 0] + ys * M[1, 1] + M[1, 2]
    z = math.hypot(M[0, 0], M[1, 0])
    aw, ah = max(1.0, tam[0] * z / 2), max(1.0, tam[1] * z / 2)
    ok = (X > -aw) & (X < W + aw) & (Y > -ah) & (Y < H + ah)
    E = h.emisivo()
    m = np.zeros((H, W), np.float32)
    for x, y in zip(X[ok], Y[ok]):
        _cv.rectangle(m, (int(x - aw), int(y - ah)), (int(x + aw), int(y + ah)), 1.0, -1)
    if aw > 3:
        m = _cv.GaussianBlur(m, (0, 0), 0.8)
    np.maximum(E, m * v, out=E)
    h.teñir_emision(np.clip(m, 0, 1), 0, 0, col if col is not None else h.pal["verde"])
