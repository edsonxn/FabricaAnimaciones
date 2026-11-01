# -*- coding: utf-8 -*-
"""«¿Cómo sobrevivían los humanos prehistóricos al FRÍO extremo?» — Sapiens con Wifi, estilo PEGATINA FLOW (21-oct-2026,
nucleo/pegaflow.py, docs/estilo_pegatina_flow.md): 37 escenarios de Flow (x2 encuadres) con cámara y parallax por profundidad;
Sapi (la mascota con diadema de wifi), cazadora, neandertal, inuit, gente, mamuts, renos y cuervos recortados de hojas de Flow
(ciclos de caminar/correr/aleteo en la misma imagen) y animados como pegatinas; nieve y ventisca, aliento, escarcha, flechas de
aire frío/tibio, ruta en el mapa, cotas, hélice de ADN y tachones por código. Mapa de piezas en ESTADO.md.
Nombres de módulo con PREFIJO por escena (H_, I_, C_, F_, R_, V_, N_, A_, G_, U_, O_): una tanda nueva no pisa las viejas."""
import functools
import math

import cv2
import numpy as np

import pegaflow as PF
import docu as D
from escena_base import Escena, TL
from motor import W, H, clamp01, e_inout, lerp, prog, smooth

TOTAL = TL["total"]
_ESC = {e["id"]: e for e in TL["escenas"]}


def T(eid, pref, frase=None, n=0, fin=False):
    return PF.T(TL, eid, pref, frase, n, fin)


def F(eid, i):
    """Inicio de la frase i de la escena (primera palabra)."""
    return _ESC[eid]["frases"][i]["words"][0]["s"]


def FE(eid, i):
    return _ESC[eid]["frases"][i]["words"][-1]["e"]


# ------------------------------------------------------------------ luz de cada escena sobre las pegatinas
DIA = (0.95, 0.98, 1.04)
GRIS = (0.86, 0.90, 0.96)
NOCHE = (0.58, 0.66, 0.90)
FUEGO = (1.08, 0.88, 0.70)
CALIDO = (1.10, 0.98, 0.84)
OCASO = (1.02, 0.86, 0.82)
CUEVA = (0.70, 0.74, 0.84)
SABANA = (1.08, 1.0, 0.86)
FANTASMA = (0.62, 0.92, 1.06)

SFX = []


def snd(t, n, v=1.0, **kw):
    SFX.append((t, n, v, kw))


# ------------------------------------------------------------------ ayudantes de toma (receta de jalpa / wow_darrowshire)
MIRA = {"sapi_camina": 1, "cazadora_camina": 1, "cazador_corre": 1, "mamut_camina": 1, "renos_camina": 1,
        "neandertal_hoja/05": 1, "fauna_hoja/04": 1, "fauna_hoja/07": 1, "fauna_hoja/00": -1, "fauna_hoja/02": -1,
        "fauna_hoja/05": -1, "inuit_hoja/02": -1, "utileria_ropa/13": 1, "utileria_ropa/14": 1, "cazadora_hoja/02": 1}


def rumbo(pieza, x0, x1, flip):
    m = MIRA.get(pieza.split("/ciclo")[0]) if "/ciclo" in pieza else MIRA.get(pieza)
    if m is None or abs(x1 - x0) < 1e-6:
        return flip
    return (x1 - x0) * m < 0


def quieto(lz, pl, t, pieza, x, y, frac, flip=False, op=1.0, tono=None, capa=1.0, fase=0.0, t_in=None, t_out=None, rot=0.0,
           dx=0.0):
    if t_in is not None:
        if t < t_in:
            return
        u = PF.entra(t, t_in, 0.4)
    else:
        u = 1.0
    if t_out is not None:
        if t > t_out + 0.4:
            return
        op *= 1.0 - smooth(prog(t, t_out, t_out + 0.35))
    X, Y, h = pl.en(t, x, y, frac, capa)
    PF.actor(lz, pieza, X + dx, Y, h * (0.6 + 0.4 * u), flip=flip, op=op * clamp01(u * 4), tono=tono,
             sy=PF.respira(t, fase=fase), rot=rot + (1 - u) * 8)


def paseo(lz, pl, t, pieza, ta, tb, x0, x1, y, frac, flip=False, tono=None, pasos=2.2, capa=1.0, op=1.0, y1=None,
          desde_antes=True, hasta_despues=True):
    if (t < ta and not desde_antes) or (t > tb and not hasta_despues):
        return
    flip = rumbo(pieza, x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x, yy = lerp(x0, x1, u), lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    mov = ta < t < tb
    ph = (t - ta) * pasos * math.pi
    bote = abs(math.sin(ph)) if mov else 0.0
    rot = 3.0 * math.sin(ph) if mov else 0.0
    PF.actor(lz, pieza, X, Y - bote * 0.035 * h, h, flip=flip, tono=tono, rot=rot, op=op, sy=PF.respira(t))


def anda(lz, pl, t, ciclo, ta, tb, x0, x1, y, frac, paso=0.95, flip=False, tono=None, capa=1.0, op=1.0, desde_antes=False,
         hasta_despues=True, y1=None):
    """Ciclo de la hoja (los pies no patinan: el cuadro sale de la distancia recorrida). Los ciclos salen ~25 % más chicos que
    `frac` (lienzo común con margen): aquí ya se compensa con 1,3."""
    if t < ta and not desde_antes:
        return
    if t > tb and not hasta_despues:
        return
    if t > tb + 0.05 and (x1 < -0.1 or x1 > 1.1):
        return
    flip = rumbo(ciclo + "/ciclo", x0, x1, flip)
    u = clamp01((t - ta) / max(tb - ta, 1e-3))
    x = lerp(x0, x1, u)
    yy = lerp(y, y1 if y1 is not None else y, u)
    X, Y, h = pl.en(t, x, yy, frac, capa)
    n = PF.ciclo_n(ciclo)
    dist = abs(x - x0) * pl.ancho_mundo(t)
    i = PF.cuadro_ciclo(dist, paso * h, n) if ta < t < tb else 0
    PF.actor(lz, f"{ciclo}/ciclo_{i:02d}", X, Y, h * 1.3, flip=flip, tono=tono, op=op)


def cuervos(lz, t, vuelos, tono=None):
    """vuelos: [(t_ini, dur, y0, y1, alto px, sentido, fase)] en pantalla; aleteo a 9 cuadros/s."""
    n = PF.ciclo_n("cuervos_aleteo")
    for t_i, dur, y0, y1, hpx, sent, fa in vuelos:
        u = (t - t_i) / dur
        if not 0 <= u <= 1:
            continue
        x = lerp(-0.08, 1.08, u) if sent > 0 else lerp(1.08, -0.08, u)
        y = lerp(y0, y1, u) + 0.012 * math.sin(t * 2.1 + fa)
        k = int((t * 9 + fa * 7)) % n
        PF.actor(lz, f"cuervos_aleteo/ciclo_{k:02d}", x * W, y * H, hpx, flip=sent < 0, ancla=(0.5, 0.5), suelo=0, tono=tono)


def pega(lz, pieza, X, Y, hpx, t, t_in, t_out=None, rot=0.0, tono=None, flip=False, salida=0.35, op=1.0):
    """Pegatina en coordenadas de PANTALLA (centro en X, Y): se pega con rebote en t_in y se despega en t_out; flota un poco."""
    if t < t_in:
        return
    u = PF.entra(t, t_in, 0.45)
    o = op if t_out is None else op * (1.0 - smooth(prog(t, t_out, t_out + salida)))
    if o <= 0.01:
        return
    PF.actor(lz, pieza, X, Y + 4 * math.sin(1.3 * t + t_in), hpx * (0.6 + 0.4 * u), rot=rot + (1 - u) * 10 + 0.8 * math.sin(1.1 * t),
             op=o * clamp01(u * 4), ancla=(0.5, 0.5), suelo=0, tono=tono, flip=flip)


def rot_(lz, txt, X, Y, px, t, t0, t1=None, rot=-2.0, **kw):
    PF.rotulo(lz, txt, X, Y, px, t, t0, t1, rot=rot, **kw)


def brillo_en(lz, pl, t, x, y, r, color=(1.0, 0.58, 0.22), inten=0.45, sem=0, chis=0):
    X, Y, s = pl.P(t, x, y)
    PF.brillo(lz, X, Y, r * s, color=color, inten=inten, t=t, sem=sem)
    if chis:
        PF.chispas(lz, t, X, Y, s=s * 1.2, n=chis, sem=sem)


def humo_en(lz, pl, t, x, y, s=1.0, color=(0.62, 0.64, 0.66), op=0.24, sem=0):
    X, Y, sc = pl.P(t, x, y)
    PF.humo(lz, t, X, Y, s=s * sc * 1.4, color=color, op=op, sem=sem)


def tinte(lz, color, k):
    if k <= 0.003:
        return
    g = lz.mean(2, keepdims=True)
    lz[:] = lz * (1 - k) + (0.55 * lz + 0.45 * g) * np.float32(color) * k


def oscurece(lz, k):
    if k > 0.003:
        lz *= 1.0 - k


def desenfoca(lz, s):
    lz[:] = cv2.GaussianBlur(lz, (0, 0), s)


# ------------------------------------------------------------------ frío por código
@functools.lru_cache(maxsize=16)
def _copos(n, sem):
    r = np.random.default_rng(sem)
    return r.random((n, 5)).astype(np.float32)          # x, y, tamaño, velocidad, fase


def nieve(lz, t, n=140, viento=0.15, op=0.85, sem=0, tam=1.0, caida=0.10):
    """Nieve en pantalla en 2 profundidades; `viento` > 1 = ventisca (copos como rayas casi horizontales)."""
    if op <= 0.01:
        return
    m = np.zeros((H // 2, W // 2), np.uint8)
    b = _copos(n, sem)
    for x, y, s, v, f in b:
        cerca = s > 0.7
        vy = (caida + 0.10 * v) * (1.6 if cerca else 1.0)
        vx = viento * (0.18 + 0.12 * v) * (1.6 if cerca else 1.0)
        yy = ((y + t * vy) % 1.1 - 0.05) * H / 2
        xx = ((x + t * vx + 0.02 * math.sin(t * 1.3 + f * 6.3)) % 1.1 - 0.05) * W / 2
        r = (1.0 + 2.6 * s * s) * tam
        if viento > 1.0:
            L = 8 + 26 * v * min(viento, 3) / 3
            cv2.line(m, (int(xx), int(yy)), (int(xx - L), int(yy - L * vy / max(vx, 1e-3) * 0.4)), int(150 + 100 * s),
                     max(1, int(r * 0.7)), cv2.LINE_AA)
        else:
            cv2.circle(m, (int(xx), int(yy)), max(1, int(round(r))), int(170 + 85 * s), -1, cv2.LINE_AA)
    a = cv2.resize(cv2.GaussianBlur(m, (0, 0), 0.8), (W, H)).astype(np.float32) / 255.0 * op
    lz[:] = lz * (1 - a[..., None]) + np.float32((0.96, 0.98, 1.0)) * a[..., None]


@functools.lru_cache(maxsize=2)
def _escarcha_mascara():
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.minimum(np.minimum(xx, W - 1 - xx) / W, np.minimum(yy, H - 1 - yy) / H * 1.4)
    r = np.random.default_rng(11)
    ruido = cv2.resize(r.random((H // 24, W // 24)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
    fino = cv2.GaussianBlur(r.random((H, W)).astype(np.float32), (0, 0), 2.0)
    return d, 0.6 + 0.4 * ruido, fino


def escarcha(lz, k):
    """Escarcha que crece desde los bordes del cuadro (k 0..1)."""
    if k <= 0.01:
        return
    d, ruido, fino = _escarcha_mascara()
    m = (np.clip((0.16 * k * ruido - d) / (0.10 * k + 1e-3), 0, 1) ** 1.5 * (0.75 + 0.25 * fino))[..., None] * 0.80
    lz[:] = lz * (1 - m) + np.float32((0.86, 0.93, 1.0)) * m


def aliento(lz, X, Y, h, t, t0, cada=1.8, flip=False):
    """Vaho que sale de la boca (X, Y en pantalla) cada `cada` s."""
    if t < t0:
        return
    u = ((t - t0) % cada) / cada
    if u > 0.85:
        return
    PF.actor(lz, "iglu_utileria/11", X + (-1 if flip else 1) * u * h * 0.9, Y - u * h * 0.25, h * (0.35 + 0.8 * u),
             op=0.75 * (1 - u / 0.85), ancla=(0.5, 0.5), suelo=0, sombra=False, flip=flip)


def tirita(t, k=1.0):
    """(dx px, rot grados) del temblor de frío."""
    return k * (3.2 * math.sin(t * 61.0) + 1.6 * math.sin(t * 37.0)), k * 1.6 * math.sin(t * 47.0)


def trazo(lz, pts, color, ancho=10, op=1.0, u=1.0, punta=False):
    """Polilínea de pantalla dibujada hasta la fracción u de su largo (con punta de flecha opcional)."""
    if u <= 0.001 or op <= 0.01 or len(pts) < 2:
        return
    p = np.array(pts, np.float32)
    seg = np.linalg.norm(np.diff(p, axis=0), axis=1)
    L = seg.sum() * clamp01(u)
    out, acc = [p[0]], 0.0
    for i, s in enumerate(seg):
        if acc + s >= L:
            out.append(p[i] + (p[i + 1] - p[i]) * ((L - acc) / max(s, 1e-6)))
            break
        out.append(p[i + 1])
        acc += s
    q = np.array(out, np.int32)
    m = np.zeros((H, W), np.uint8)
    cv2.polylines(m, [q.reshape(-1, 1, 2)], False, 255, int(ancho), cv2.LINE_AA)
    if punta and len(q) >= 2:
        a, b = q[-2].astype(np.float32), q[-1].astype(np.float32)
        d = b - a
        n = np.linalg.norm(d)
        if n > 1:
            d /= n
            o = np.array([-d[1], d[0]])
            tri = np.array([b + d * ancho * 1.6, b - d * ancho * 1.4 + o * ancho * 1.5, b - d * ancho * 1.4 - o * ancho * 1.5], np.int32)
            cv2.fillPoly(m, [tri], 255, cv2.LINE_AA)
    a = cv2.GaussianBlur(m, (0, 0), 0.7).astype(np.float32)[..., None] / 255.0 * op
    lz[:] = lz * (1 - a) + np.float32(color) * a


def tacha(lz, X, Y, r, t, t0, color=(0.82, 0.12, 0.10)):
    """Tachón rojo en X (dos trazos de rotulador)."""
    if t < t0:
        return
    u1, u2 = smooth(prog(t, t0, t0 + 0.25)), smooth(prog(t, t0 + 0.2, t0 + 0.45))
    trazo(lz, [(X - r, Y - r), (X + r, Y + r)], (0.12, 0.05, 0.04), 30, 0.35, u1)
    trazo(lz, [(X - r, Y - r), (X + r, Y + r)], color, 22, 1.0, u1)
    trazo(lz, [(X + r, Y - r), (X - r, Y + r)], (0.12, 0.05, 0.04), 30, 0.35, u2)
    trazo(lz, [(X + r, Y - r), (X - r, Y + r)], color, 22, 1.0, u2)


def cota(lz, X0, Y0, X1, Y1, t, t0, color=(0.98, 0.95, 0.88), ancho=6):
    """Línea de medida con topes que se traza desde el centro."""
    if t < t0:
        return
    u = smooth(prog(t, t0, t0 + 0.7))
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    a = (cx + (X0 - cx) * u, cy + (Y0 - cy) * u)
    b = (cx + (X1 - cx) * u, cy + (Y1 - cy) * u)
    d = np.array([X1 - X0, Y1 - Y0], np.float32)
    d /= max(np.linalg.norm(d), 1e-3)
    o = np.array([-d[1], d[0]]) * 22
    trazo(lz, [a, b], (0.1, 0.08, 0.08), ancho + 6, 0.4)
    trazo(lz, [a, b], color, ancho)
    for p in (a, b):
        trazo(lz, [(p[0] - o[0], p[1] - o[1]), (p[0] + o[0], p[1] + o[1])], color, ancho, u)


def helice(lz, X, Y, alto, t, t0, op=1.0):
    """Hélice de ADN dibujada (dos hebras y peldaños) que gira despacio."""
    if t < t0:
        return
    u = smooth(prog(t, t0, t0 + 1.0)) * op
    n = 60
    ys = np.linspace(-alto / 2, alto / 2, n)
    ph = ys / alto * 4 * math.pi + t * 1.4
    r = alto * 0.16
    a = [(X + r * math.sin(p), Y + y) for p, y in zip(ph, ys)]
    b = [(X - r * math.sin(p), Y + y) for p, y in zip(ph, ys)]
    for k in range(0, n, 4):
        trazo(lz, [a[k], b[k]], (0.95, 0.80, 0.45), 6, 0.9 * u)
    trazo(lz, a, (0.35, 0.75, 0.95), 11, u)
    trazo(lz, b, (0.95, 0.45, 0.35), 11, u)


def burbujas(lz, X, Y, R, t, t0, n=22, sem=3):
    """Burbujas de aire atrapadas (círculos de contorno) que aparecen dentro de un círculo de radio R."""
    if t < t0:
        return
    r = np.random.default_rng(sem)
    b = r.random((n, 4))
    for k, (bx, by, bs, bf) in enumerate(b):
        tk = t0 + 0.08 * k
        if t < tk:
            continue
        u = PF.entra(t, tk, 0.35)
        ang, rad = bx * 2 * math.pi, math.sqrt(by) * R
        x = X + rad * math.cos(ang) + 4 * math.sin(t * 1.7 + bf * 6)
        y = Y + rad * math.sin(ang) - 3 * math.sin(t * 1.3 + bf * 5)
        rr = (10 + 26 * bs) * u
        cv2.circle(lz, (int(x), int(y)), int(rr), (0.25, 0.45, 0.70), 4, cv2.LINE_AA)
        cv2.circle(lz, (int(x - rr * 0.35), int(y - rr * 0.35)), max(2, int(rr * 0.22)), (0.95, 0.98, 1.0), -1, cv2.LINE_AA)


def corazon_brillo(lz, X, Y, r, t, color, inten):
    PF.brillo(lz, X, Y, r, color=color, inten=inten * (0.85 + 0.15 * math.sin(t * 7.0)), t=t)


# ------------------------------------------------------------------ tomas
TOMAS = []


def toma(t0, ent=("fundido", 0.5)):
    def deco(f):
        TOMAS.append(dict(t0=t0, ent=ent, dib=f))
        return f
    return deco


HK, HI, CU, FU, RO, CV, NO, AR, IG, TU, OU = ("hook", "hielo", "cuerpo", "fuego", "ropa", "cuevas", "noche", "artico", "iglu",
                                              "tu", "outro")

# ================================================================== GANCHO (0 - 72)
H_f = [F(HK, i) for i in range(15)]
H_chamarra, H_ventana, H_calef = T(HK, "chamarra", 1), T(HK, "ventana", 1), T(HK, "calefacción", 1)
H_listo = T(HK, "listo", 2)
H_cuarenta, H_viento, H_diecio = T(HK, "cuarenta", 4), T(HK, "viento", 4), T(HK, "dieciocho", 4)
H_veinte, H_edad = T(HK, "veinte", 5), T(HK, "edad", 5)
H_tropical, H_africa, H_chimp = T(HK, "tropical", 6), T(HK, "áfrica", 7), T(HK, "chimpancé", 8)
H_siberia, H_artico, H_glaciares = T(HK, "siberia", 9), T(HK, "ártico", 9), T(HK, "glaciares", 9)
H_como = T(HK, "cómo", 10)
H_cueva, H_temblando = T(HK, "cueva", 11), T(HK, "temblando", 11)
H_mal = T(HK, "mal", 12)
H_inventos, H_casa, H_iglu = T(HK, "inventos", 13), T(HK, "casa", 13), T(HK, "iglú", 13)

H1 = PF.Plano("sala_moderna", 0.0, H_f[3], z0=1.04, z1=1.16, c0=(0.50, 0.58), c1=(0.44, 0.60), par=(26, 6))
snd(0.2, "viento", 0.35, dur=4.0)
snd(H_chamarra, "pop", 0.6)
snd(H_ventana, "golpe_suave", 0.5)
snd(H_calef, "pop", 0.6, tono=1.1)
snd(H_listo, "ding", 0.45)


@toma(0.0)
def h1(lz, t):
    H1.fondo(lz, t)
    brillo_en(lz, H1, t, 0.66, 0.42, 120, color=(1.0, 0.75, 0.40), inten=0.30, sem=1)        # lámpara
    calor = smooth(prog(t, H_calef, H_calef + 1.5))
    brillo_en(lz, H1, t, 0.28, 0.62, 260, color=(1.0, 0.55, 0.25), inten=0.30 * calor, sem=2)  # radiador encendido
    frio = 1.0 - smooth(prog(t, H_chamarra, H_listo))
    dx, rr = tirita(t, frio)
    X, Y, h = H1.en(t, 0.50, 0.95, 0.56)
    pz = "sapi_hoja/03" if t < H_chamarra + 0.2 else ("sapi_hoja/00" if t < H_listo else "sapi_hoja/01")
    PF.actor(lz, pz, X + dx, Y, h, rot=rr, sy=PF.respira(t))
    if t < H_chamarra + 0.3:
        aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.22 * h, t, 0.3)
    pega(lz, "moderno_hoja/00", W * 0.80, H * 0.36, H * 0.30, t, H_chamarra, H_f[3] - 0.6, rot=6)
    pega(lz, "moderno_hoja/10", W * 0.80, H * 0.72, H * 0.18, t, H_listo, H_f[3] - 0.6, rot=-3)
    rot_(lz, "LISTO.", W * 0.50, H * 0.14, 64, t, H_listo + 0.1, H_f[3] - 0.4)
    tinte(lz, (0.70, 0.82, 1.05), 0.25 * frio)


H2 = PF.Plano("ventisca_noche", H_f[3] - 0.4, H_f[5], z0=1.02, z1=1.20, c0=(0.50, 0.56), c1=(0.56, 0.60), par=(30, 8))
snd(H_f[3] - 0.4, "viento", 0.9, dur=10.0)
snd(H_cuarenta, "hielo", 0.6)
snd(H_viento, "brr", 0.5)


@toma(H_f[3] - 0.4, ("desenfoque", 0.7))
def h2(lz, t):
    H2.fondo(lz, t)
    brillo_en(lz, H2, t, 0.55, 0.16, 160, color=(0.65, 0.78, 1.0), inten=0.12, sem=3)
    dx, rr = tirita(t)
    X, Y, h = H2.en(t, 0.40, 0.95, 0.52)
    PF.actor(lz, "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=NOCHE, sy=PF.respira(t))
    aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.22 * h, t, H_f[3])
    nieve(lz, t, n=150, viento=2.4, op=0.75, sem=1)
    escarcha(lz, smooth(prog(t, H_f[3], H_f[5])) * 0.45)
    rot_(lz, "-40 °C", W * 0.74, H * 0.24, 110, t, H_cuarenta, rot=3)
    rot_(lz, "18 HORAS DE NOCHE", W * 0.72, H * 0.42, 52, t, H_diecio, rot=-2)


H3 = PF.Plano("estepa_atardecer", H_f[5] - 0.4, H_f[6], z0=1.02, z1=1.12, c0=(0.48, 0.54), c1=(0.54, 0.54), par=(30, 8))
snd(H_f[5], "pasos", 0.35, dur=4.0)
snd(H_veinte, "papel", 0.5)


@toma(H_f[5] - 0.4, ("fundido", 0.7))
def h3(lz, t):
    H3.fondo(lz, t)
    brillo_en(lz, H3, t, 0.50, 0.30, 260, color=(1.0, 0.55, 0.30), inten=0.18, sem=4)
    anda(lz, H3, t, "mamut_camina", H_f[5] - 0.4, H_f[6] + 0.5, 0.62, 0.86, 0.50, 0.10, paso=1.4, tono=OCASO, desde_antes=True)
    anda(lz, H3, t, "mamut_camina", H_f[5] - 0.4, H_f[6] + 0.5, 0.48, 0.70, 0.47, 0.08, paso=1.4, tono=OCASO, desde_antes=True)
    anda(lz, H3, t, "cazadora_camina", H_f[5] - 0.4, H_f[6] + 0.5, 0.10, 0.42, 0.93, 0.40, tono=OCASO, desde_antes=True)
    nieve(lz, t, n=90, viento=0.5, op=0.6, sem=2)
    rot_(lz, "HACE 20 000 AÑOS", W * 0.30, H * 0.14, 56, t, H_veinte)
    rot_(lz, "EDAD DE HIELO", W * 0.66, H * 0.22, 64, t, H_edad, rot=2)


H4 = PF.Plano("sabana_africa", H_f[6] - 0.4, H_f[9], z0=1.03, z1=1.18, c0=(0.50, 0.55), c1=(0.44, 0.58), par=(30, 8))
snd(H_f[6] - 0.3, "whoosh", 0.5)
snd(H_tropical, "papel", 0.5)
snd(H_africa, "pasos", 0.4, dur=3.0)
snd(H_chimp, "boing", 0.4)


@toma(H_f[6] - 0.4, ("latigo", 0.5))
def h4(lz, t):
    H4.fondo(lz, t)
    brillo_en(lz, H4, t, 0.78, 0.14, 300, color=(1.0, 0.85, 0.45), inten=0.30, sem=5)       # sol
    if t < H_chimp:
        anda(lz, H4, t, "sapi_camina", H_f[6], H_chimp - 0.3, 0.12, 0.46, 0.94, 0.46, tono=SABANA, desde_antes=True)
    else:
        X, Y, h = H4.en(t, 0.46, 0.94, 0.50)
        PF.actor(lz, "sapi_hoja/04", X, Y, h, tono=SABANA, sy=PF.respira(t))
    rot_(lz, "UN ANIMAL TROPICAL", W * 0.50, H * 0.13, 60, t, H_tropical, H_chimp - 0.3)
    rot_(lz, "ÁFRICA", W * 0.74, H * 0.30, 70, t, H_africa, H_chimp - 0.3, rot=3)
    rot_(lz, "CASI SIN PELO", W * 0.72, H * 0.46, 46, t, T(HK, "pelo", 7), H_chimp - 0.3, rot=-2)
    rot_(lz, "UN CHIMPANCÉ TIENE MÁS ABRIGO QUE TÚ", W * 0.50, H * 0.14, 50, t, H_chimp)


# mapa del mundo: puntos (x, y) del escenario mapa_mundo_a (rejilla previews/_rej1.jpg)
RUTA_MAPA = [(0.56, 0.60), (0.59, 0.45), (0.55, 0.36), (0.50, 0.32), (0.58, 0.30), (0.68, 0.26), (0.78, 0.24), (0.88, 0.25)]
RUTA_AMER = [(0.10, 0.27), (0.16, 0.30), (0.21, 0.40), (0.26, 0.55), (0.30, 0.75)]
H6 = PF.Plano("mapa_mundo", H_f[9] - 0.4, H_f[11], z0=1.02, z1=1.30, c0=(0.50, 0.50), c1=(0.62, 0.40), par=(0, 0), mano=0.4)
snd(H_f[9] - 0.3, "papel", 0.7)
snd(H_f[9] + 0.5, "garabato", 0.5)
snd(H_siberia, "pop", 0.5)
snd(H_artico, "pop", 0.5, tono=1.1)
snd(H_como, "boing", 0.5)


def ruta_mapa(lz, pl, t, ta, tb, puntos, op=1.0):
    u = smooth(prog(t, ta, tb))
    pts = [pl.P(t, x, y)[:2] for x, y in puntos]
    trazo(lz, pts, (0.30, 0.18, 0.10), 14, 0.5 * op, u)
    trazo(lz, pts, (0.86, 0.24, 0.14), 8, op, u, punta=u < 0.98)
    return pts, u


@toma(H_f[9] - 0.4, ("desenfoque", 0.6))
def h6(lz, t):
    H6.fondo(lz, t)
    pts, u = ruta_mapa(lz, H6, t, H_f[9] + 0.3, H_artico + 1.0, RUTA_MAPA)
    if u > 0.98:
        ruta_mapa(lz, H6, t, H_artico + 1.0, H_glaciares + 1.0, RUTA_AMER)
    X, Y, _ = H6.P(t, *RUTA_MAPA[0])
    pega(lz, "sapi_hoja/00", X, Y - 40, 120, t, H_f[9])
    rot_(lz, "SIBERIA", *H6.P(t, 0.70, 0.18)[:2], 40, t, H_siberia)
    rot_(lz, "ÁRTICO", *H6.P(t, 0.84, 0.14)[:2], 40, t, H_artico, rot=2)
    if t > H_como - 0.2:
        oscurece(lz, 0.35 * smooth(prog(t, H_como - 0.2, H_como + 0.3)))
        pega(lz, "sapi_hoja/04", W * 0.50, H * 0.56, H * 0.62, t, H_como - 0.1)
        rot_(lz, "¿CÓMO?", W * 0.50, H * 0.15, 110, t, H_como)


H7 = PF.Plano("cueva_fondo", H_f[11] - 0.4, H_f[13], z0=1.45, z1=1.62, c0=(0.58, 0.55), c1=(0.61, 0.57), par=(26, 6))
snd(H_f[11] - 0.3, "gota", 0.5)
snd(H_f[11] + 2.0, "gota", 0.4, tono=1.2)
snd(H_temblando, "brr", 0.5)
snd(H_mal, "error", 0.5)


@toma(H_f[11] - 0.4, ("fundido", 0.6))
def h7(lz, t):
    H7.fondo(lz, t)
    brillo_en(lz, H7, t, 0.60, 0.545, 70, color=(1.0, 0.55, 0.22), inten=0.45, sem=6, chis=4)
    dx, rr = tirita(t, 0.6)
    quieto(lz, H7, t, "neandertal_hoja/06", 0.53, 0.66, 0.24, tono=CUEVA, dx=dx, rot=rr)
    quieto(lz, H7, t, "gente_hoja/00", 0.68, 0.645, 0.21, tono=CUEVA, flip=True, fase=1.2)
    k = smooth(prog(t, H_mal, H_mal + 0.6))
    oscurece(lz, 0.25 * k)
    tacha(lz, W * 0.58, H * 0.50, H * 0.26, t, H_mal)
    rot_(lz, "MITO", W * 0.58, H * 0.15, 90, t, H_mal + 0.3, rot=-4)


H8 = PF.Plano("casa_mamut_b", H_f[13] - 0.4, H_f[14], z0=1.10, z1=1.20, c0=(0.5, 0.5), c1=(0.5, 0.48), par=(0, 0))
snd(H_inventos, "pop", 0.6)
snd(H_casa, "pop", 0.6, tono=0.9)
snd(H_iglu, "pop", 0.6, tono=1.2)


@toma(H_f[13] - 0.4, ("latigo", 0.5))
def h8(lz, t):
    H8.fondo(lz, t)
    desenfoca(lz, 5)
    oscurece(lz, 0.25)
    nieve(lz, t, n=70, viento=0.3, op=0.5, sem=3)
    pega(lz, "utileria_fuego/01", W * 0.20, H * 0.54, H * 0.30, t, H_inventos, rot=-4)
    pega(lz, "utileria_ropa/00", W * 0.40, H * 0.40, H * 0.14, t, H_inventos + 0.4, rot=-25)
    pega(lz, "huesos_mamut/00", W * 0.60, H * 0.56, H * 0.34, t, H_casa, rot=3)
    pega(lz, "iglu_utileria/02", W * 0.80, H * 0.50, H * 0.30, t, H_iglu, rot=-3)
    rot_(lz, "LOS INVENTOS QUE NOS SALVARON", W * 0.50, H * 0.16, 54, t, H_inventos + 0.3)


H9 = PF.Plano("ventisca_noche_b", H_f[14] - 0.4, F(HI, 0), z0=1.04, z1=1.16, c0=(0.46, 0.56), c1=(0.54, 0.56), par=(30, 8))
snd(H_f[14] - 0.3, "viento", 0.8, dur=5.0)


@toma(H_f[14] - 0.4, ("desenfoque", 0.5))
def h9(lz, t):
    H9.fondo(lz, t)
    anda(lz, H9, t, "cazador_corre", H_f[14] - 0.4, F(HI, 0) + 0.2, 0.05, 0.80, 0.92, 0.42, paso=1.35, tono=NOCHE, desde_antes=True)
    nieve(lz, t, n=150, viento=2.6, op=0.75, sem=4)
    escarcha(lz, 0.3)


# ================================================================== HIELO (72 - 117,3)
I_f = [F(HI, i) for i in range(8)]
I_canada, I_tres, I_europa, I_ciudades = T(HI, "canadá", 1), T(HI, "tres", 1), T(HI, "europa", 2), T(HI, "ciudades", 2)
I_ciento = T(HI, "ciento", 3)
I_estepa, I_mamuts, I_rinos, I_renos, I_bisontes, I_caballos = (T(HI, "estepa", 5), T(HI, "mamuts", 5), T(HI, "rinocerontes", 5),
                                                                 T(HI, "renos", 5), T(HI, "bisontes", 5), T(HI, "caballos", 5))
I_noche, I_poco = T(HI, "noche", 6), T(HI, "poco", 7)

I1 = PF.Plano("estepa_mamut", I_f[0] - 0.4, I_f[1], z0=1.02, z1=1.12, c0=(0.50, 0.52), c1=(0.56, 0.52), par=(30, 8))
snd(I_f[0] - 0.3, "viento", 0.5, dur=5.0)
snd(I_f[0] + 1.2, "papel", 0.5)


@toma(I_f[0] - 0.4, ("destello", 0.8))
def i1(lz, t):
    I1.fondo(lz, t)
    anda(lz, I1, t, "mamut_camina", I_f[0] - 0.4, I_f[1] + 0.4, 0.10, 0.48, 0.66, 0.20, paso=1.4, tono=DIA, desde_antes=True)
    anda(lz, I1, t, "mamut_camina", I_f[0] - 0.4, I_f[1] + 0.4, -0.06, 0.30, 0.62, 0.16, paso=1.4, tono=DIA, desde_antes=True)
    cuervos(lz, t, [(I_f[0], 6.0, 0.18, 0.12, 60, 1, 0.3)], tono=DIA)
    nieve(lz, t, n=60, viento=0.4, op=0.5, sem=5)
    rot_(lz, "EL MOMENTO MÁS FRÍO", W * 0.50, H * 0.13, 58, t, I_f[0] + 1.2)


I2 = PF.Plano("glaciar_canada", I_f[1] - 0.4, I_f[2], z0=1.02, z1=1.10, c0=(0.50, 0.50), c1=(0.50, 0.46), par=(30, 8))
snd(I_canada, "papel", 0.5)
snd(I_tres, "crece", 0.5)


@toma(I_f[1] - 0.4, ("latigo", 0.5))
def i2(lz, t):
    I2.fondo(lz, t)
    quieto(lz, I2, t, "cazadora_hoja/01", 0.30, 0.88, 0.15, tono=GRIS)
    quieto(lz, I2, t, "renos_camina/ciclo_00", 0.46, 0.86, 0.10, tono=GRIS)
    X0, Y0, _ = I2.P(t, 0.88, 0.62)
    X1, Y1, _ = I2.P(t, 0.88, 0.12)
    cota(lz, X0, Y0, X1, Y1, t, I_tres - 0.2)
    rot_(lz, "3 KM DE HIELO", X0 - 220, (Y0 + Y1) / 2, 54, t, I_tres, rot=-3)
    rot_(lz, "CANADÁ", W * 0.24, H * 0.14, 64, t, I_canada)
    Xs, Ys, hs = I2.fg(t, 0.13, 1.04, 0.62)
    PF.actor(lz, "sapi_hoja/04", Xs, Ys, hs, tono=GRIS, sy=PF.respira(t), suelo=0)
    nieve(lz, t, n=70, viento=0.3, op=0.55, sem=6)


I3 = PF.Plano("glaciar_canada_b", I_f[2] - 0.4, I_f[3], z0=1.04, z1=1.14, c0=(0.48, 0.52), c1=(0.54, 0.50), par=(30, 8))
snd(I_europa, "papel", 0.5)


@toma(I_f[2] - 0.4, ("desenfoque", 0.5))
def i3(lz, t):
    I3.fondo(lz, t)
    anda(lz, I3, t, "renos_camina", I_f[2] - 0.4, I_f[3] + 0.4, 0.05, 0.45, 0.88, 0.16, paso=1.3, tono=GRIS, desde_antes=True)
    anda(lz, I3, t, "renos_camina", I_f[2] - 0.4, I_f[3] + 0.4, -0.10, 0.30, 0.92, 0.18, paso=1.3, tono=GRIS, desde_antes=True)
    rot_(lz, "NORTE DE EUROPA", W * 0.34, H * 0.14, 58, t, I_europa)
    rot_(lz, "DONDE HOY HAY CIUDADES", W * 0.64, H * 0.26, 44, t, I_ciudades, rot=2)
    nieve(lz, t, n=70, viento=0.3, op=0.55, sem=7)


I4 = PF.Plano("costa_mar_bajo", I_f[3] - 0.4, I_f[4], z0=1.03, z1=1.12, c0=(0.50, 0.52), c1=(0.46, 0.54), par=(30, 8))
snd(I_ciento, "whoosh", 0.5)


@toma(I_f[3] - 0.4, ("latigo", 0.5))
def i4(lz, t):
    I4.fondo(lz, t)
    anda(lz, I4, t, "cazadora_camina", I_f[3] - 0.4, I_f[4] + 0.4, 0.15, 0.48, 0.90, 0.36, tono=GRIS, desde_antes=True)
    u = smooth(prog(t, I_ciento - 0.3, I_ciento + 1.2))
    Ya = lerp(H * 0.30, H * 0.40, 0.0)
    trazo(lz, [(W * 0.04, Ya), (W * 0.96, Ya)], (0.20, 0.55, 0.85), 6, 0.9 * clamp01(u * 3))
    rot_(lz, "EL MAR DE HOY", W * 0.16, Ya - 40, 34, t, I_ciento - 0.3, rot=0)
    trazo(lz, [(W * 0.86, Ya + 10), (W * 0.86, Ya + 10 + 160 * u)], (0.86, 0.24, 0.14), 10, 1.0, 1.0, punta=True)
    rot_(lz, "-120 METROS", W * 0.74, Ya + 120, 52, t, I_ciento + 0.6)


I5 = PF.Plano("estepa_mamut_b", I_f[4] - 0.4, I_f[6], z0=1.02, z1=1.24, c0=(0.50, 0.54), c1=(0.56, 0.58), par=(32, 8))
snd(I_f[4], "viento", 0.6, dur=4.0)
snd(I_mamuts, "pop", 0.5)
snd(I_rinos, "pop", 0.5, tono=0.9)
snd(I_renos, "pop", 0.5, tono=1.1)
snd(I_bisontes, "pop", 0.5, tono=0.85)
snd(I_caballos, "pop", 0.5, tono=1.2)


@toma(I_f[4] - 0.4, ("desenfoque", 0.5))
def i5(lz, t):
    I5.fondo(lz, t)
    PF.arena_viento(lz, t, fuerza=0.6, y0=0.70, color=(0.95, 0.97, 1.0))
    anda(lz, I5, t, "mamut_camina", I_f[4] - 0.4, I_f[6] + 0.4, 0.06, 0.46, 0.70, 0.26, paso=1.4, tono=DIA, desde_antes=True)
    anda(lz, I5, t, "mamut_camina", I_f[4] - 0.4, I_f[6] + 0.4, 0.22, 0.56, 0.64, 0.18, paso=1.4, tono=DIA, desde_antes=True)
    anda(lz, I5, t, "mamut_camina", I_f[4] - 0.4, I_f[6] + 0.4, 0.40, 0.66, 0.60, 0.12, paso=1.4, tono=DIA, desde_antes=True)
    quieto(lz, I5, t, "fauna_hoja/00", 0.70, 0.72, 0.18, tono=DIA, t_in=I_rinos)
    anda(lz, I5, t, "renos_camina", I_renos - 0.2, I_f[6] + 0.4, 0.40, 0.62, 0.62, 0.12, paso=1.3, tono=DIA)
    quieto(lz, I5, t, "fauna_hoja/02", 0.88, 0.80, 0.22, tono=DIA, t_in=I_bisontes)
    quieto(lz, I5, t, "fauna_hoja/04", 0.54, 0.92, 0.26, tono=DIA, t_in=I_caballos)
    rot_(lz, "LA ESTEPA DEL MAMUT", W * 0.50, H * 0.13, 64, t, I_estepa)


I6 = PF.Plano("estepa_atardecer_b", I_f[6] - 0.4, I_f[7], z0=1.04, z1=1.14, c0=(0.50, 0.55), c1=(0.56, 0.55), par=(30, 8))
snd(I_f[6], "pasos", 0.5, dur=3.0)


@toma(I_f[6] - 0.4, ("fundido", 0.6))
def i6(lz, t):
    I6.fondo(lz, t)
    anda(lz, I6, t, "renos_camina", I_f[6] - 0.4, I_f[7] + 0.4, 0.40, 0.95, 0.80, 0.24, paso=1.3, tono=OCASO, desde_antes=True)
    anda(lz, I6, t, "cazador_corre", I_f[6] - 0.4, I_f[7] + 0.4, -0.05, 0.60, 0.92, 0.38, paso=1.35, tono=OCASO, desde_antes=True)
    k = smooth(prog(t, I_noche - 0.3, I_f[7] + 0.4))
    tinte(lz, (0.45, 0.55, 0.95), 0.6 * k)
    oscurece(lz, 0.3 * k)


I7 = PF.Plano("estepa_sin_arboles", I_f[7] - 0.4, F(CU, 0), z0=1.10, z1=1.22, c0=(0.40, 0.58), c1=(0.38, 0.62), par=(26, 6))
snd(I_f[7], "viento", 0.8, dur=5.5)
snd(I_poco, "hielo", 0.5)


@toma(I_f[7] - 0.4, ("negro", 0.6))
def i7(lz, t):
    I7.fondo(lz, t)
    tinte(lz, (0.45, 0.55, 0.95), 0.7)
    oscurece(lz, 0.35)
    dx, rr = tirita(t)
    X, Y, h = I7.en(t, 0.42, 0.94, 0.46)
    PF.actor(lz, "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=NOCHE, sy=PF.respira(t))
    aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.22 * h, t, I_f[7])
    nieve(lz, t, n=160, viento=1.6, op=0.8, sem=8)
    escarcha(lz, smooth(prog(t, I_f[7], F(CU, 0))))
    rot_(lz, "POCO A POCO", W * 0.70, H * 0.20, 60, t, I_poco - 0.2)


# ================================================================== CUERPO (117,3 - 194,7)
C_f = [F(CU, i) for i in range(14)]
C_treinta5 = T(CU, "cinco", 0)
C_hipo = T(CU, "hipotermia", 0)
C_tiritas = T(CU, "tiritas", 1)
C_manos, C_pies, C_corazon, C_cerebro = T(CU, "manos", 2), T(CU, "pies", 2), T(CU, "corazón", 2), T(CU, "cerebro", 2)
C_dedos = T(CU, "dedos", 3)
C_confundes, C_sueno, C_peligroso = T(CU, "confundes", 4), T(CU, "sueño", 4), T(CU, "peligroso", 4)
C_neander, C_bajitos, C_anchos, C_barril, C_cortos = (T(CU, "neandertales", 5), T(CU, "bajitos", 6), T(CU, "anchos", 6),
                                                      T(CU, "barril", 6), T(CU, "cortos", 6))
C_oso = T(CU, "oso", 7)
C_largos = T(CU, "largos", 8)
C_inuit, C_grasa, C_especie = T(CU, "inuit", 10), T(CU, "grasa", 10), T(CU, "especie", 10)
C_lenta = T(CU, "lentísima", 11)
C_invento = T(CU, "inventó", 12)
C_poderoso = T(CU, "poderoso", 13)

C1 = PF.Plano("campamento_viento", C_f[0] - 0.4, C_f[1], z0=1.04, z1=1.14, c0=(0.50, 0.56), c1=(0.56, 0.58), par=(28, 6))
snd(C_f[0], "latido", 0.5)
snd(C_hipo, "hielo", 0.6)


@toma(C_f[0] - 0.4, ("destello", 0.7))
def c1(lz, t):
    C1.fondo(lz, t)
    nieve(lz, t, n=90, viento=0.8, op=0.6, sem=9)
    X, Y, h = C1.en(t, 0.68, 0.96, 0.62)
    PF.actor(lz, "sapi_hoja/01", X, Y, h, tono=GRIS, sy=PF.respira(t))
    pega(lz, "moderno_hoja/03", W * 0.24, H * 0.50, H * 0.62, t, C_f[0], rot=-3)
    v = 37.0 if t < C_treinta5 - 0.2 else lerp(37.0, 35.0, smooth(prog(t, C_treinta5 - 0.2, C_treinta5 + 0.6)))
    if t > C_f[0] + 0.3:
        rot_(lz, f"{v:.0f} °C", W * 0.40, H * 0.30, 74, t, C_f[0] + 0.3, rot=2)
    k = smooth(prog(t, C_hipo - 0.2, C_hipo + 0.8))
    tinte(lz, (0.55, 0.70, 1.05), 0.35 * k)
    rot_(lz, "HIPOTERMIA", W * 0.40, H * 0.84, 70, t, C_hipo, rot=-2)


C2 = PF.Plano("campamento_viento_b", C_f[1] - 0.4, C_f[2], z0=1.30, z1=1.40, c0=(0.50, 0.60), c1=(0.52, 0.60), par=(22, 6))
snd(C_tiritas, "brr", 0.7)


@toma(C_f[1] - 0.4, ("latigo", 0.45))
def c2(lz, t):
    C2.fondo(lz, t)
    desenfoca(lz, 2.0)
    nieve(lz, t, n=110, viento=1.0, op=0.7, sem=10)
    dx, rr = tirita(t, 1.4 if t > C_tiritas else 0.3)
    X, Y, h = W * 0.50, H * 1.08, H * 0.98
    PF.actor(lz, "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=GRIS, suelo=0)
    aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.20 * h, t, C_f[1], cada=1.2)
    rot_(lz, "TIRITAR = FABRICAR CALOR", W * 0.50, H * 0.12, 54, t, C_tiritas + 0.6)


@functools.lru_cache(maxsize=1)
def _fondo_cuerpo():
    return None


C3 = PF.Plano("campamento_viento_b", C_f[2] - 0.4, C_f[5], z0=1.10, z1=1.10, c0=(0.30, 0.50), c1=(0.30, 0.50), par=(0, 0))
snd(C_corazon, "latido", 0.7)
snd(C_cerebro, "pop", 0.4)
snd(C_dedos, "hielo", 0.7)
snd(C_confundes, "eco", 0.5)
snd(C_peligroso, "impacto", 0.6)


@toma(C_f[2] - 0.4, ("desenfoque", 0.6))
def c3(lz, t):
    C3.fondo(lz, t)
    desenfoca(lz, 7)
    oscurece(lz, 0.35)
    tinte(lz, (0.55, 0.65, 1.0), 0.4)
    # zoom a la mano en «dedos»: Sapi grande en pantalla, el ancla se va hacia su mano izquierda
    kz = 0.0
    h = H * 0.92 * (1.0 + 1.6 * kz)
    X = lerp(W * 0.50, W * 0.50 + 0.22 * h, kz)               # en «dedos» la mano izquierda de Sapi queda al centro
    Y = lerp(H * 1.0, H * 0.55 + 0.42 * h, kz)
    conf = smooth(prog(t, C_confundes - 0.2, C_confundes + 1.0))
    dx, rr = tirita(t, 0.5 + 0.8 * conf)
    PF.actor(lz, "sapi_hoja/00" if conf < 0.5 else "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=(0.9, 0.92, 1.0), suelo=0)
    # el calor se queda en el centro (corazón y cerebro); manos y pies se enfrían
    kc = smooth(prog(t, C_corazon - 0.3, C_corazon + 0.4))
    corazon_brillo(lz, X - 0.02 * h, Y - 0.58 * h, 0.30 * h, t, (1.0, 0.30, 0.20), 0.55 * kc)
    corazon_brillo(lz, X, Y - 0.86 * h, 0.22 * h, t, (1.0, 0.55, 0.25), 0.45 * smooth(prog(t, C_cerebro - 0.3, C_cerebro + 0.4)))
    km = smooth(prog(t, C_manos - 0.2, C_manos + 0.6))
    kd = smooth(prog(t, C_dedos - 0.3, C_dedos + 0.5))
    for mx, my, r in ((-0.17, -0.42, 0.07), (0.17, -0.42, 0.07), (-0.08, -0.05, 0.08), (0.08, -0.05, 0.08)):
        PF._blob(lz, X + mx * h, Y + my * h, r * h * (1 + 0.4 * kd), (0.45, 0.72, 1.0), (0.55 + 0.30 * kd) * km)
        if kd > 0:
            PF.brillo(lz, X + mx * h, Y + my * h, 0.10 * h, color=(0.8, 0.95, 1.0), inten=0.5 * kd, t=t)
    rot_(lz, "CORAZÓN", W * 0.16, H * 0.30, 50, t, C_corazon, C_dedos - 0.4)
    rot_(lz, "CEREBRO", W * 0.84, H * 0.18, 50, t, C_cerebro, C_dedos - 0.4, rot=2)
    rot_(lz, "LOS DEDOS, PRIMERO", W * 0.50, H * 0.12, 60, t, C_dedos, C_f[4] - 0.3)
    if t > C_f[4] - 0.4:
        s = 3.0 * conf * (0.5 + 0.5 * math.sin(t * 2.2))
        if s > 0.3:
            desenfoca(lz, s)
        escarcha(lz, 0.7 * conf)
    rot_(lz, "EL MOMENTO MÁS PELIGROSO", W * 0.50, H * 0.13, 58, t, C_peligroso - 0.2)


C4 = PF.Plano("bosque_neandertal", C_f[5] - 0.4, C_f[6], z0=1.02, z1=1.14, c0=(0.50, 0.55), c1=(0.56, 0.56), par=(30, 8))
snd(C_neander, "papel", 0.5)
snd(C_f[5], "pasos", 0.4, dur=4.0)


@toma(C_f[5] - 0.4, ("latigo", 0.5))
def c4(lz, t):
    C4.fondo(lz, t)
    paseo(lz, C4, t, "neandertal_hoja/05", C_f[5] - 0.4, C_f[6] - 0.5, 0.10, 0.52, 0.92, 0.42, tono=GRIS, pasos=1.8)
    nieve(lz, t, n=120, viento=0.2, op=0.7, sem=11)
    rot_(lz, "NEANDERTALES", W * 0.50, H * 0.13, 70, t, C_neander)
    rot_(lz, "CIENTOS DE MILES DE AÑOS", W * 0.66, H * 0.26, 44, t, T(CU, "cientos", 5), rot=2)


C5 = PF.Plano("bosque_neandertal_b", C_f[6] - 0.4, C_f[8], z0=1.06, z1=1.12, c0=(0.50, 0.58), c1=(0.50, 0.60), par=(26, 6))
snd(C_bajitos, "pop", 0.4)
snd(C_anchos, "pop", 0.4, tono=0.9)
snd(C_barril, "boing", 0.4)
snd(C_oso, "pop", 0.6)


@toma(C_f[6] - 0.4, ("desenfoque", 0.5))
def c5(lz, t):
    C5.fondo(lz, t)
    nieve(lz, t, n=90, viento=0.2, op=0.6, sem=12)
    Xn, Yn, hn = C5.en(t, 0.34, 0.95, 0.50)
    Xs, Ys, hs = C5.en(t, 0.64, 0.95, 0.60)
    PF.actor(lz, "neandertal_hoja/00", Xn, Yn, hn, tono=GRIS, sy=PF.respira(t))
    PF.actor(lz, "sapi_hoja/00", Xs, Ys, hs, tono=GRIS, sy=PF.respira(t, fase=1.0))
    cota(lz, Xn - hn * 0.40, Yn - hn * 1.05, Xn + hn * 0.40, Yn - hn * 1.05, t, C_anchos)
    rot_(lz, "BAJITO", Xn, Yn - hn * 1.25, 46, t, C_bajitos, C_oso - 0.4)
    rot_(lz, "ANCHO", Xn - hn * 0.62, Yn - hn * 0.55, 44, t, C_anchos, C_oso - 0.4, rot=3)
    rot_(lz, "PECHO DE BARRIL", Xn + hn * 0.66, Yn - hn * 0.72, 36, t, C_barril, C_oso - 0.4, rot=-3)
    rot_(lz, "BRAZOS Y PIERNAS CORTOS", W * 0.50, H * 0.90, 48, t, C_cortos, C_oso - 0.4)
    if t > C_oso - 0.3:
        oscurece(lz, 0.3 * smooth(prog(t, C_oso - 0.3, C_oso + 0.2)))
        pega(lz, "fauna_hoja/07", W * 0.50, H * 0.54, H * 0.44, t, C_oso)
        rot_(lz, "REDONDO = PIERDE MENOS CALOR", W * 0.50, H * 0.86, 50, t, C_oso + 0.5)


C6 = PF.Plano("sabana_africa_b", C_f[8] - 0.4, C_f[9], z0=1.03, z1=1.12, c0=(0.50, 0.55), c1=(0.56, 0.56), par=(30, 8))
snd(C_f[8] - 0.3, "whoosh", 0.5)


@toma(C_f[8] - 0.4, ("latigo", 0.5))
def c6(lz, t):
    C6.fondo(lz, t)
    brillo_en(lz, C6, t, 0.80, 0.12, 300, color=(1.0, 0.85, 0.45), inten=0.28, sem=13)
    anda(lz, C6, t, "sapi_camina", C_f[8] - 0.4, C_f[9] + 0.4, 0.15, 0.62, 0.94, 0.50, tono=SABANA, desde_antes=True)
    rot_(lz, "LARGOS Y DELGADOS", W * 0.50, H * 0.13, 62, t, C_largos)


C7 = PF.Plano("groenlandia_costa", C_f[9] - 0.4, C_f[11], z0=1.03, z1=1.16, c0=(0.48, 0.56), c1=(0.56, 0.58), par=(30, 8))
snd(C_inuit, "papel", 0.5)
snd(C_grasa, "burbujas", 0.4)
snd(C_especie, "aparicion", 0.5)


@toma(C_f[9] - 0.4, ("desenfoque", 0.6))
def c7(lz, t):
    C7.fondo(lz, t)
    brillo_en(lz, C7, t, 0.78, 0.78, 120, color=(1.0, 0.55, 0.22), inten=0.40, sem=14, chis=5)
    quieto(lz, C7, t, "fauna_hoja/09", 0.40, 0.70, 0.10, tono=DIA)
    quieto(lz, C7, t, "inuit_hoja/04", 0.24, 0.95, 0.46, tono=DIA)
    quieto(lz, C7, t, "inuit_hoja/05", 0.58, 0.92, 0.40, tono=DIA, flip=True, fase=1.0)
    rot_(lz, "INUIT DE GROENLANDIA", W * 0.40, H * 0.13, 56, t, C_inuit)
    if t > C_grasa - 0.4:
        oscurece(lz, 0.3 * smooth(prog(t, C_grasa - 0.4, C_grasa)))
        helice(lz, W * 0.80, H * 0.48, H * 0.62, t, C_grasa - 0.3)
        rot_(lz, "GRASA QUE PRODUCE CALOR", W * 0.66, H * 0.86, 46, t, C_grasa + 0.4, C_especie - 0.4)
    if t > C_especie - 0.3:
        X, Y, h = W * 0.42, H * 0.90, H * 0.44
        k = smooth(prog(t, C_especie - 0.3, C_especie + 0.8))
        PF.brillo(lz, X, Y - 0.5 * h, 1.1 * h, color=(0.4, 0.8, 0.95), inten=0.22 * k, t=t)
        PF.actor(lz, "neandertal_hoja/00", X, Y, h, op=0.55 * k, tono=FANTASMA, suelo=0, sombra=False)
        rot_(lz, "OTRA ESPECIE HUMANA", X, H * 0.32, 44, t, C_especie + 0.4, rot=2)


C8 = PF.Plano("groenlandia_costa_b", C_f[11] - 0.4, C_f[12], z0=1.04, z1=1.10, c0=(0.50, 0.55), c1=(0.52, 0.55), par=(26, 6))
snd(C_lenta, "reloj_rapido", 0.3, dur=2.0)


@toma(C_f[11] - 0.4, ("fundido", 0.5))
def c8(lz, t):
    C8.fondo(lz, t)
    nieve(lz, t, n=180, viento=1.5, op=0.8, sem=13)
    oscurece(lz, 0.15)
    u = 0.04 + 0.06 * smooth(prog(t, C_f[11], C_f[12]))                       # la barra de la evolución casi no avanza
    x0, x1, y = W * 0.22, W * 0.78, H * 0.52
    trazo(lz, [(x0, y + 6), (x1, y + 6)], (0.05, 0.04, 0.04), 60, 0.35)
    trazo(lz, [(x0, y), (x1, y)], (0.96, 0.93, 0.86), 54, 1.0)
    trazo(lz, [(x0, y), (lerp(x0, x1, u), y)], (0.90, 0.45, 0.18), 34, 1.0)
    rot_(lz, "MILES Y MILES DE AÑOS", W * 0.50, H * 0.60, 40, t, C_f[11] + 0.6, rot=0)
    rot_(lz, "EVOLUCIÓN", W * 0.50, H * 0.40, 52, t, C_f[11])
    rot_(lz, "EL FRÍO NO ESPERA", W * 0.50, H * 0.80, 62, t, T(CU, "espera", 11), rot=2)


C9 = PF.Plano("abrigo_entrada_b", C_f[12] - 0.4, F(FU, 0), z0=1.04, z1=1.18, c0=(0.42, 0.58), c1=(0.38, 0.62), par=(28, 6))
snd(C_invento, "ding", 0.6)
snd(C_poderoso, "fuego", 0.5, dur=2.5)


@toma(C_f[12] - 0.4, ("latigo", 0.5))
def c9(lz, t):
    C9.fondo(lz, t)
    nieve(lz, t, n=70, viento=0.4, op=0.5, sem=14)
    X, Y, h = C9.en(t, 0.40, 0.95, 0.52)
    pz = "sapi_hoja/01" if t < C_poderoso - 0.3 else "sapi_hoja/05"
    PF.actor(lz, pz, X, Y, h, tono=GRIS if pz.endswith("01") else FUEGO, sy=PF.respira(t))
    if pz.endswith("05"):
        k = smooth(prog(t, C_poderoso - 0.3, C_poderoso + 0.5))
        PF.brillo(lz, X + 0.22 * h, Y - 1.0 * h, 0.9 * h, color=(1.0, 0.55, 0.22), inten=0.55 * k, t=t)
        PF.chispas(lz, t, X + 0.22 * h, Y - 1.0 * h, s=1.4, n=8)
    pega(lz, "moderno_hoja/09", X + 0.05 * h, Y - 1.25 * h, H * 0.18, t, C_invento, C_poderoso - 0.4)
    rot_(lz, "NO CAMBIÓ EL CUERPO", W * 0.70, H * 0.20, 52, t, T(CU, "cambió", 12))
    rot_(lz, "INVENTÓ COSAS", W * 0.70, H * 0.34, 64, t, C_invento, rot=2)


# ================================================================== FUEGO (194,7 - 280)
F_f = [F(FU, i) for i in range(15)]
F_millon, F_cuatroc = T(FU, "millón", 1), T(FU, "cuatrocientos", 2)
F_encender = T(FU, "encenderlo", 3)
F_francia, F_cincuenta = T(FU, "francia", 4), T(FU, "cincuenta", 4)
F_pirita, F_chispas, F_encendedor = T(FU, "pirita", 5), T(FU, "chispas", 5), T(FU, "encendedor", 5)
F_secaba = T(FU, "secaba", 6)
F_arboles, F_huesos = T(FU, "árboles", 7), T(FU, "huesos", 8)
F_grasa, F_despacio = T(FU, "grasa", 9), T(FU, "despacio", 9)
F_lamparas, F_diecis = T(FU, "lámparas", 10), T(FU, "diecisiete", 10)
F_cama = T(FU, "cama", 11)
F_dosc, F_ceniza = T(FU, "doscientos", 12), T(FU, "ceniza", 12)
F_insectos, F_colchon = T(FU, "insectos", 13), T(FU, "colchón", 13)
F_defecto, F_puesto = T(FU, "defecto", 14), T(FU, "puesto", 14)

FU1 = PF.Plano("campamento_fuego", F_f[0] - 0.5, F_f[1], z0=1.06, z1=1.16, c0=(0.50, 0.54), c1=(0.50, 0.52), par=(28, 6))
snd(F_f[0] - 0.4, "fuego", 0.7, dur=3.0)
snd(F_f[0] + 0.1, "papel", 0.6)


@toma(F_f[0] - 0.5, ("destello", 0.8))
def fu1(lz, t):
    FU1.fondo(lz, t)
    brillo_en(lz, FU1, t, 0.50, 0.50, 260, color=(1.0, 0.55, 0.22), inten=0.55, sem=20, chis=10)
    quieto(lz, FU1, t, "grupo_dormir/01", 0.30, 0.80, 0.26, tono=FUEGO)
    quieto(lz, FU1, t, "gente_hoja/04", 0.70, 0.84, 0.32, tono=FUEGO, flip=True, fase=1.0)
    rot_(lz, "1. EL FUEGO", W * 0.50, H * 0.15, 92, t, F_f[0])


FU2 = PF.Plano("cueva_sudafrica", F_f[1] - 0.4, F_f[2], z0=1.04, z1=1.18, c0=(0.50, 0.55), c1=(0.60, 0.62), par=(30, 8))
snd(F_f[1] + 0.3, "papel", 0.5)
snd(F_millon, "golpe_suave", 0.6)


@toma(F_f[1] - 0.4, ("latigo", 0.5))
def fu2(lz, t):
    FU2.fondo(lz, t)
    brillo_en(lz, FU2, t, 0.50, 0.30, 300, color=(1.0, 0.62, 0.30), inten=0.18, sem=21)
    quieto(lz, FU2, t, "utileria_fuego/15", 0.70, 0.80, 0.10, tono=CALIDO, t_in=F_f[1] + 0.2)
    quieto(lz, FU2, t, "huesos_mamut/05", 0.56, 0.86, 0.07, tono=CALIDO, t_in=F_f[1] + 0.6, rot=-12)
    quieto(lz, FU2, t, "utileria_fuego/06", 0.82, 0.88, 0.07, tono=CALIDO, t_in=F_f[1] + 1.0, rot=8)
    cuervos(lz, t, [(F_f[1], 6.0, 0.30, 0.24, 46, -1, 0.4)], tono=CALIDO)
    rot_(lz, "SUDÁFRICA", W * 0.30, H * 0.14, 60, t, F_f[1] + 0.3)
    rot_(lz, "HACE 1 MILLÓN DE AÑOS", W * 0.66, H * 0.26, 56, t, F_millon, rot=2)


FU3 = PF.Plano("campamento_fuego_b", F_f[2] - 0.4, F_f[4], z0=1.04, z1=1.20, c0=(0.50, 0.56), c1=(0.56, 0.58), par=(28, 6))
snd(F_cuatroc, "papel", 0.5)
snd(F_f[2], "fuego", 0.5, dur=8.0)
snd(F_encender, "match", 0.7)


@toma(F_f[2] - 0.4, ("desenfoque", 0.5))
def fu3(lz, t):
    FU3.fondo(lz, t)
    brillo_en(lz, FU3, t, 0.60, 0.50, 240, color=(1.0, 0.55, 0.22), inten=0.50, sem=22, chis=8)
    quieto(lz, FU3, t, "gente_hoja/00", 0.22, 0.86, 0.34, tono=FUEGO)
    quieto(lz, FU3, t, "gente_hoja/02", 0.40, 0.80, 0.28, tono=FUEGO, fase=0.6)
    quieto(lz, FU3, t, "cazadora_hoja/03", 0.78, 0.88, 0.34, tono=FUEGO, flip=True, fase=1.3)
    quieto(lz, FU3, t, "gente_hoja/01", 0.92, 0.94, 0.26, tono=FUEGO, flip=True, fase=2.0)
    rot_(lz, "HACE 400 000 AÑOS", W * 0.50, H * 0.13, 58, t, F_cuatroc)
    rot_(lz, "SABÍAN ENCENDERLO", W * 0.50, H * 0.26, 52, t, F_encender, rot=2)


FU4 = PF.Plano("cueva_pinturas_b", F_f[4] - 0.4, F_f[5], z0=1.08, z1=1.20, c0=(0.42, 0.62), c1=(0.38, 0.64), par=(26, 6))
snd(F_francia, "papel", 0.5)
for _k in range(5):
    snd(F_f[4] + 1.2 + 1.1 * _k, "clink", 0.35, tono=1.0 + 0.05 * (_k % 2))


@toma(F_f[4] - 0.4, ("latigo", 0.5))
def fu4(lz, t):
    FU4.fondo(lz, t)
    brillo_en(lz, FU4, t, 0.42, 0.64, 160, color=(1.0, 0.55, 0.22), inten=0.40, sem=23)
    golpe = abs(math.sin((t - F_f[4]) * math.pi / 1.1))
    X, Y, h = FU4.en(t, 0.40, 0.95, 0.46)
    PF.actor(lz, "neandertal_hoja/01", X, Y, h, tono=FUEGO, rot=-3 * (1 - golpe), sy=PF.respira(t))
    if golpe > 0.92:
        PF.chispas(lz, t * 3, X + 0.10 * h, Y - 0.20 * h, s=1.0, n=8, sem=3)
    rot_(lz, "FRANCIA", W * 0.30, H * 0.14, 58, t, F_francia)
    rot_(lz, "NEANDERTALES · HACE 50 000 AÑOS", W * 0.62, H * 0.26, 46, t, F_cincuenta, rot=2)


FU5 = PF.Plano("cueva_pinturas_b", F_f[5] - 0.4, F_f[6], z0=1.3, z1=1.3, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
snd(F_pirita - 0.2, "pop", 0.6)
for _k in range(4):
    snd(F_chispas + 0.5 * _k, "match", 0.6, tono=1.0 + 0.1 * _k)


@toma(F_f[5] - 0.4, ("desenfoque", 0.5))
def fu5(lz, t):
    FU5.fondo(lz, t)
    desenfoca(lz, 7)
    oscurece(lz, 0.40)
    pega(lz, "utileria_fuego/03", W * 0.62, H * 0.52, H * 0.34, t, F_pirita - 0.2)
    if t > F_f[5]:                          # el pedernal golpea la pirita: va y viene y salta la chispa
        g = abs(math.sin((t - F_f[5]) * math.pi / 0.9))
        Xp = W * 0.40 + 90 * g
        Yp = H * 0.44 - 50 * g
        PF.actor(lz, "utileria_fuego/02", Xp, Yp, H * 0.30, rot=-20 + 14 * g, ancla=(0.5, 0.5), suelo=0)
        if g < 0.25 and t > F_chispas - 0.3:
            PF.brillo(lz, W * 0.54, H * 0.50, 200, color=(1.0, 0.75, 0.3), inten=0.7, t=t)
            PF.chispas(lz, t * 2.5, W * 0.54, H * 0.52, s=2.0, n=14, sem=5)
    rot_(lz, "PIRITA", W * 0.66, H * 0.80, 64, t, F_pirita)
    rot_(lz, "EL ENCENDEDOR DE LA EDAD DE PIEDRA", W * 0.50, H * 0.13, 52, t, F_encendedor)


FU6 = PF.Plano("choza_dentro_b", F_f[6] - 0.4, F_f[7], z0=1.06, z1=1.22, c0=(0.50, 0.58), c1=(0.58, 0.55), par=(26, 6))
snd(F_f[6], "fuego", 0.6, dur=7.0)
snd(F_secaba, "siseo", 0.4)


@toma(F_f[6] - 0.4, ("fundido", 0.6))
def fu6(lz, t):
    FU6.fondo(lz, t)
    brillo_en(lz, FU6, t, 0.58, 0.62, 220, color=(1.0, 0.55, 0.22), inten=0.55, sem=24, chis=8)
    humo_en(lz, FU6, t, 0.62, 0.42, s=0.6, color=(0.92, 0.90, 0.86), op=0.20 * smooth(prog(t, F_secaba - 0.5, F_secaba + 0.5)), sem=2)
    quieto(lz, FU6, t, "cazadora_hoja/03", 0.36, 0.95, 0.46, tono=FUEGO)
    rot_(lz, "SECAR LA ROPA MOJADA", W * 0.50, H * 0.13, 56, t, F_secaba)


FU7 = PF.Plano("estepa_sin_arboles_b", F_f[7] - 0.4, F_f[9], z0=1.02, z1=1.20, c0=(0.50, 0.52), c1=(0.70, 0.62), par=(30, 8))
snd(F_f[7], "viento", 0.6, dur=5.0)
snd(F_huesos, "golpe_suave", 0.6)


@toma(F_f[7] - 0.4, ("latigo", 0.5))
def fu7(lz, t):
    FU7.fondo(lz, t)
    nieve(lz, t, n=90, viento=0.8, op=0.6, sem=20)
    brillo_en(lz, FU7, t, 0.78, 0.80, 120, color=(1.0, 0.55, 0.22), inten=0.45 * smooth(prog(t, F_huesos - 0.3, F_huesos + 0.5)), sem=25, chis=5)
    paseo(lz, FU7, t, "cazadora_hoja/02", F_f[8] - 0.5, F_huesos, 0.40, 0.66, 0.92, 0.38, tono=GRIS, pasos=2.0)
    rot_(lz, "NI UN ÁRBOL", W * 0.50, H * 0.14, 70, t, F_arboles)
    rot_(lz, "HUESOS", W * 0.30, H * 0.30, 80, t, F_huesos, rot=-3)


FU8 = PF.Plano("campamento_fuego", F_f[9] - 0.4, F_f[10], z0=1.55, z1=1.75, c0=(0.50, 0.52), c1=(0.50, 0.52), par=(22, 6))
snd(F_f[9], "fuego", 0.7, dur=6.0)
snd(F_grasa, "pop", 0.5)


@toma(F_f[9] - 0.4, ("desenfoque", 0.5))
def fu8(lz, t):
    FU8.fondo(lz, t)
    brillo_en(lz, FU8, t, 0.50, 0.50, 300, color=(1.0, 0.55, 0.22), inten=0.60, sem=26, chis=12)
    quieto(lz, FU8, t, "utileria_fuego/09", 0.50, 0.58, 0.12, tono=FUEGO)
    quieto(lz, FU8, t, "gente_hoja/04", 0.70, 0.66, 0.28, tono=FUEGO, flip=True)
    pega(lz, "utileria_fuego/06", W * 0.24, H * 0.42, H * 0.30, t, F_grasa, rot=-8)
    rot_(lz, "GRASA POR DENTRO", W * 0.24, H * 0.66, 46, t, F_grasa + 0.3)
    rot_(lz, "ARDEN DESPACIO", W * 0.50, H * 0.13, 56, t, F_despacio)


FU9 = PF.Plano("cueva_pinturas", F_f[10] - 0.4, F_f[11], z0=1.04, z1=1.24, c0=(0.50, 0.40), c1=(0.56, 0.50), par=(26, 6))
snd(F_lamparas, "pop", 0.6)
snd(F_diecis, "papel", 0.5)


@toma(F_f[10] - 0.4, ("fundido", 0.6))
def fu9(lz, t):
    FU9.fondo(lz, t)
    brillo_en(lz, FU9, t, 0.62, 0.62, 160, color=(1.0, 0.55, 0.22), inten=0.45, sem=27, chis=4)
    quieto(lz, FU9, t, "cazadora_hoja/05", 0.40, 0.86, 0.36, tono=FUEGO)
    pega(lz, "utileria_fuego/04", W * 0.76, H * 0.48, H * 0.30, t, F_lamparas, rot=4)
    if t > F_lamparas:
        PF.brillo(lz, W * 0.80, H * 0.40, 220, color=(1.0, 0.65, 0.25), inten=0.55 * PF.entra(t, F_lamparas, 0.6), t=t)
    rot_(lz, "LÁMPARAS DE GRASA", W * 0.40, H * 0.13, 56, t, F_lamparas + 0.3)
    rot_(lz, "HACE 17 000 AÑOS", W * 0.74, H * 0.76, 48, t, F_diecis, rot=2)


FU10 = PF.Plano("refugio_camas", F_f[11] - 0.4, F_f[13], z0=1.04, z1=1.20, c0=(0.50, 0.55), c1=(0.60, 0.58), par=(28, 6))
snd(F_cama, "papel", 0.6)
snd(F_dosc, "papel", 0.5)


@toma(F_f[11] - 0.4, ("latigo", 0.5))
def fu10(lz, t):
    FU10.fondo(lz, t)
    brillo_en(lz, FU10, t, 0.67, 0.57, 140, color=(1.0, 0.45, 0.18), inten=0.40, sem=28, chis=4)
    humo_en(lz, FU10, t, 0.67, 0.55, s=0.7, op=0.18, sem=3)
    quieto(lz, FU10, t, "gente_hoja/04", 0.84, 0.86, 0.36, tono=CALIDO, flip=True)
    quieto(lz, FU10, t, "utileria_fuego/08", 0.36, 0.86, 0.16, tono=CALIDO, t_in=F_cama)
    quieto(lz, FU10, t, "grupo_dormir/03", 0.36, 0.84, 0.20, tono=CALIDO, t_in=F_ceniza)
    rot_(lz, "LA CAMA", W * 0.36, H * 0.30, 80, t, F_cama)
    rot_(lz, "HACE 200 000 AÑOS", W * 0.66, H * 0.14, 52, t, F_dosc, rot=2)


FU11 = PF.Plano("refugio_camas_b", F_f[13] - 0.4, F_f[14], z0=1.30, z1=1.30, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
snd(F_insectos, "pop", 0.4)
snd(F_colchon, "boing", 0.5)


@toma(F_f[13] - 0.4, ("desenfoque", 0.5))
def fu11(lz, t):
    FU11.fondo(lz, t)
    desenfoca(lz, 6)
    oscurece(lz, 0.3)
    pega(lz, "utileria_fuego/08", W * 0.30, H * 0.52, H * 0.40, t, F_f[13])
    rot_(lz, "CENIZA: SIN INSECTOS", W * 0.30, H * 0.80, 44, t, F_insectos)
    rot_(lz, "PASTO: AISLA DEL SUELO", W * 0.30, H * 0.20, 44, t, T(FU, "pasto", 13))
    rot_(lz, "=", W * 0.52, H * 0.50, 110, t, F_colchon - 0.2, rot=0)
    pega(lz, "moderno_hoja/02", W * 0.74, H * 0.52, H * 0.34, t, F_colchon, rot=3)
    rot_(lz, "UN COLCHÓN", W * 0.74, H * 0.80, 56, t, F_colchon + 0.3)


FU12 = PF.Plano("campamento_sol_b", F_f[14] - 0.4, F(RO, 0), z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.60, 0.58), par=(28, 6))
snd(F_defecto, "error", 0.4)
snd(F_puesto, "brr", 0.6)


@toma(F_f[14] - 0.4, ("latigo", 0.5))
def fu12(lz, t):
    FU12.fondo(lz, t)
    nieve(lz, t, n=60, viento=0.3, op=0.5, sem=21)
    if t < F_puesto - 0.2:
        anda(lz, FU12, t, "sapi_camina", F_f[14] - 0.4, F_puesto - 0.2, 0.30, 0.60, 0.94, 0.46, tono=DIA, desde_antes=True)
    else:
        dx, rr = tirita(t)
        X, Y, h = FU12.en(t, 0.60, 0.94, 0.48)
        PF.actor(lz, "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=DIA, sy=PF.respira(t))
        aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.2 * h, t, F_puesto)
    rot_(lz, "NO TE LO PUEDES LLEVAR PUESTO", W * 0.50, H * 0.13, 52, t, F_puesto - 0.6)


# ================================================================== ROPA (280 - 376)
R_f = [F(RO, i) for i in range(17)]
R_ropa = T(RO, "ropa", 0)
R_pudre = T(RO, "pudre", 1)
R_piojo = T(RO, "piojo", 2)
R_cabeza, R_ropa3 = T(RO, "cabeza", 3), T(RO, "ropa", 3)
R_ochenta = T(RO, "ochenta", 5)
R_conto = T(RO, "contó", 6)
R_capa = T(RO, "capa", 7)
R_aire = T(RO, "aire", 8)
R_aguja = T(RO, "aguja", 9)
R_siberia, R_cuarenta = T(RO, "siberia", 10), T(RO, "cuarenta", 10)
R_mangas, R_capuchas, R_pantalones = T(RO, "mangas", 11), T(RO, "capuchas", 11), T(RO, "pantalones", 11)
R_tumbas, R_treinta = T(RO, "tumbas", 12), T(RO, "treinta", 12)
R_cuentas = T(RO, "cuentas", 13)
R_gorro, R_camisa, R_pant, R_botas = T(RO, "gorro", 15), T(RO, "camisa", 15), T(RO, "pantalones", 15), T(RO, "botas", 15)
R_moda = T(RO, "moda", 16)

RO1 = PF.Plano("taller_pieles", R_f[0] - 0.4, R_f[1], z0=1.04, z1=1.14, c0=(0.48, 0.58), c1=(0.52, 0.60), par=(28, 6))
snd(R_ropa, "papel", 0.6)
snd(R_f[0], "puntada", 0.4)


@toma(R_f[0] - 0.4, ("destello", 0.8))
def ro1(lz, t):
    RO1.fondo(lz, t)
    brillo_en(lz, RO1, t, 0.48, 0.60, 120, color=(1.0, 0.55, 0.22), inten=0.40, sem=30, chis=4)
    quieto(lz, RO1, t, "cazadora_hoja/04", 0.40, 0.94, 0.44, tono=DIA, rot=2 * math.sin(t * 4))
    quieto(lz, RO1, t, "gente_hoja/03", 0.76, 0.92, 0.36, tono=DIA, flip=True, fase=1.0)
    nieve(lz, t, n=50, viento=0.2, op=0.4, sem=30)
    rot_(lz, "2. LA ROPA", W * 0.50, H * 0.15, 92, t, R_ropa)


RO2 = PF.Plano("excavacion_rusia", R_f[1] - 0.4, R_f[2], z0=1.10, z1=1.24, c0=(0.42, 0.58), c1=(0.40, 0.60), par=(26, 6))
snd(R_pudre, "siseo", 0.5)


@toma(R_f[1] - 0.4, ("latigo", 0.5))
def ro2(lz, t):
    RO2.fondo(lz, t)
    k = smooth(prog(t, R_pudre - 0.2, R_f[2] - 0.5))
    X, Y, s = RO2.P(t, 0.40, 0.56)
    PF.actor(lz, "utileria_ropa/07", X, Y, 260 * s / 1.4, op=1.0 - k, tono=(1.0 - 0.4 * k, 0.95 - 0.45 * k, 0.85 - 0.5 * k),
             ancla=(0.5, 0.5), suelo=0, rot=-8)
    PF.humo(lz, t, X, Y, s=1.2, color=(0.55, 0.45, 0.30), op=0.25 * k * (1 - k) * 4, sem=4)
    rot_(lz, "LA ROPA SE PUDRE", W * 0.50, H * 0.13, 58, t, R_pudre)


RO3 = PF.Plano("bosque_pelo", R_f[2] - 0.4, R_f[4], z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.56, 0.60), par=(30, 8))
snd(R_piojo, "boing", 0.6)
snd(R_ropa3, "boing", 0.5, tono=0.8)


@toma(R_f[2] - 0.4, ("desenfoque", 0.6))
def ro3(lz, t):
    RO3.fondo(lz, t)
    paseo(lz, RO3, t, "utileria_ropa/13", R_f[2] - 0.4, R_f[3] + 1.5, 0.04, 0.42, 0.90, 0.30, tono=CALIDO, pasos=5.0)
    paseo(lz, RO3, t, "utileria_ropa/14", R_ropa3 - 0.3, R_ropa3 + 1.6, 0.92, 0.68, 0.92, 0.28, tono=CALIDO, pasos=5.0, desde_antes=False)
    rot_(lz, "UN PIOJO", W * 0.30, H * 0.14, 60, t, R_piojo, R_cabeza - 0.3)
    rot_(lz, "PIOJO DE LA CABEZA", W * 0.28, H * 0.20, 48, t, R_cabeza)
    rot_(lz, "PIOJO DE LA ROPA", W * 0.70, H * 0.30, 48, t, R_ropa3, rot=2)


RO4 = PF.Plano("bosque_pelo_b", R_f[4] - 0.4, R_f[5], z0=1.10, z1=1.18, c0=(0.50, 0.58), c1=(0.52, 0.58), par=(26, 6))
snd(R_f[4], "papel", 0.4)


@toma(R_f[4] - 0.4, ("latigo", 0.5))
def ro4(lz, t):
    RO4.fondo(lz, t)
    X, Y, h = RO4.en(t, 0.50, 0.94, 0.34)
    PF.actor(lz, "utileria_ropa/16", X, Y + 0.05 * h, h * 0.9, tono=CALIDO, rot=-4)
    salto = abs(math.sin((t - R_f[4]) * 3.0)) * 0.12 * h
    PF.actor(lz, "utileria_ropa/14", X, Y - 0.70 * h - salto, h * 0.55, tono=CALIDO, suelo=0)
    rot_(lz, "SIN ROPA NO EXISTE", W * 0.50, H * 0.13, 58, t, T(RO, "existir", 4))


RO5 = PF.Plano("bosque_pelo_b", R_f[5] - 0.4, R_f[7], z0=1.25, z1=1.25, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
snd(R_f[5] + 0.4, "burbujas", 0.4)
snd(R_ochenta, "pop", 0.7)
snd(R_conto, "bling", 0.5)


@toma(R_f[5] - 0.4, ("desenfoque", 0.5))
def ro5(lz, t):
    RO5.fondo(lz, t)
    desenfoca(lz, 7)
    oscurece(lz, 0.35)
    helice(lz, W * 0.25, H * 0.52, H * 0.70, t, R_f[5])
    rot_(lz, "COMPARANDO SUS GENES", W * 0.62, H * 0.14, 50, t, R_f[5] + 0.2)
    rot_(lz, "AL MENOS", W * 0.62, H * 0.32, 48, t, R_ochenta - 0.5)
    rot_(lz, "83 000 AÑOS", W * 0.62, H * 0.48, 110, t, R_ochenta, rot=-3)
    pega(lz, "utileria_ropa/14", W * 0.62, H * 0.76, H * 0.24, t, R_conto - 0.3, rot=8 * math.sin(t * 5))
    rot_(lz, "Y UN PIOJO NOS LO CONTÓ", W * 0.62, H * 0.92, 40, t, R_conto, rot=1)


RO6 = PF.Plano("costa_mar_bajo_b", R_f[7] - 0.4, R_f[9], z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.44, 0.60), par=(28, 6))
snd(R_f[7], "viento", 0.7, dur=10.0)
snd(R_aire, "brr", 0.6)


@toma(R_f[7] - 0.4, ("fundido", 0.6))
def ro6(lz, t):
    RO6.fondo(lz, t)
    X, Y, h = RO6.en(t, 0.42, 0.95, 0.50)
    if t < R_f[8]:
        PF.actor(lz, "neandertal_hoja/04", X, Y, h, tono=GRIS, sy=PF.respira(t))
    else:
        dx, rr = tirita(t)
        PF.actor(lz, "neandertal_hoja/06", X + dx, Y, h, tono=GRIS, rot=rr, sy=PF.respira(t))
        aliento(lz, X + 0.12 * h, Y - 0.82 * h, 0.2 * h, t, R_f[8])
    PF.arena_viento(lz, t, fuerza=0.8, y0=0.30, y1=0.95, color=(0.95, 0.97, 1.0))
    rot_(lz, "PIELES COMO CAPA", W * 0.70, H * 0.16, 56, t, R_capa)
    rot_(lz, "PERO EL AIRE ENTRA", W * 0.70, H * 0.30, 50, t, R_aire, rot=2)


RO7 = PF.Plano("cueva_siberia", R_f[9] - 0.4, R_f[11], z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.58, 0.56), par=(28, 6))
snd(R_aguja, "bling", 0.6)
snd(R_siberia, "papel", 0.5)


@toma(R_f[9] - 0.4, ("latigo", 0.5))
def ro7(lz, t):
    RO7.fondo(lz, t)
    paseo(lz, RO7, t, "gente_hoja/03", R_f[9] - 0.4, R_aguja, 0.20, 0.42, 0.90, 0.34, tono=DIA, pasos=2.0)
    nieve(lz, t, n=60, viento=0.2, op=0.45, sem=31)
    if t > R_aguja - 0.3:
        oscurece(lz, 0.3 * smooth(prog(t, R_aguja - 0.3, R_aguja + 0.2)))
        k = PF.entra(t, R_aguja, 0.6)
        PF.brillo(lz, W * 0.50, H * 0.48, 380, color=(1.0, 0.95, 0.80), inten=0.30 * k, t=t)
        PF.actor(lz, "utileria_ropa/00", W * 0.50, H * 0.48, H * 0.34 * (0.6 + 0.4 * k), rot=-20 + 6 * math.sin(t * 0.8),
                 op=clamp01(k * 3), ancla=(0.5, 0.5), suelo=0)
    rot_(lz, "LA AGUJA DE HUESO", W * 0.50, H * 0.13, 64, t, R_aguja + 0.2)
    rot_(lz, "SIBERIA", W * 0.24, H * 0.82, 56, t, R_siberia)
    rot_(lz, "MÁS DE 40 000 AÑOS", W * 0.74, H * 0.82, 50, t, R_cuarenta, rot=2)


RO8 = PF.Plano("taller_pieles_b", R_f[11] - 0.4, R_f[12], z0=1.06, z1=1.18, c0=(0.44, 0.60), c1=(0.40, 0.62), par=(26, 6))
snd(R_f[11] + 0.5, "puntada", 0.5)
snd(R_mangas, "pop", 0.5)
snd(R_capuchas, "pop", 0.5, tono=1.1)
snd(R_pantalones, "pop", 0.5, tono=0.9)


@toma(R_f[11] - 0.4, ("desenfoque", 0.5))
def ro8(lz, t):
    RO8.fondo(lz, t)
    brillo_en(lz, RO8, t, 0.60, 0.72, 120, color=(1.0, 0.55, 0.22), inten=0.40, sem=32, chis=4)
    quieto(lz, RO8, t, "cazadora_hoja/00", 0.30, 0.95, 0.46, tono=DIA, rot=1.5 * math.sin(t * 6))
    pega(lz, "utileria_ropa/11", W * 0.62, H * 0.36, H * 0.30, t, R_mangas, rot=-4)
    pega(lz, "iglu_utileria/09", W * 0.80, H * 0.30, H * 0.22, t, R_capuchas, rot=5)
    pega(lz, "utileria_ropa/04", W * 0.86, H * 0.62, H * 0.30, t, R_pantalones, rot=3)
    rot_(lz, "ROPA AJUSTADA", W * 0.50, H * 0.12, 60, t, T(RO, "ajustada", 11))


RO9 = PF.Plano("excavacion_rusia_b", R_f[12] - 0.4, R_f[15], z0=1.04, z1=1.30, c0=(0.50, 0.52), c1=(0.48, 0.56), par=(28, 6))
snd(R_tumbas, "papel", 0.5)
snd(R_cuentas, "clink", 0.6)
CUENTAS = [(float(x), float(y), float(r)) for x, y, r in np.random.default_rng(8).uniform((0.28, 0.48, -40), (0.70, 0.60, 40), (26, 3))]


@toma(R_f[12] - 0.4, ("latigo", 0.5))
def ro9(lz, t):
    RO9.fondo(lz, t)
    for k, (x, y, r) in enumerate(CUENTAS):
        tk = R_tumbas + 0.4 + 0.22 * k
        if t > tk:
            X, Y, s = RO9.P(t, x, y)
            PF.actor(lz, "utileria_ropa/02", X, Y, 46 * s * (0.6 + 0.4 * PF.entra(t, tk, 0.3)), rot=r, ancla=(0.5, 0.5), suelo=0,
                     tono=CALIDO)
    rot_(lz, "TUMBAS DE RUSIA", W * 0.50, H * 0.13, 58, t, R_tumbas, R_treinta - 0.5)
    rot_(lz, "MÁS DE 30 000 AÑOS", W * 0.50, H * 0.13, 58, t, R_treinta - 0.3)
    rot_(lz, "MILES DE CUENTAS DE MARFIL", W * 0.50, H * 0.86, 50, t, R_cuentas + 0.5)


RO10 = PF.Plano("excavacion_rusia_b", R_f[15] - 0.4, R_f[16], z0=1.2, z1=1.2, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
snd(R_gorro, "pop", 0.5)
snd(R_camisa, "pop", 0.5, tono=1.1)
snd(R_pant, "pop", 0.5, tono=0.9)
snd(R_botas, "pop", 0.5, tono=1.2)


@toma(R_f[15] - 0.4, ("desenfoque", 0.5))
def ro10(lz, t):
    RO10.fondo(lz, t)
    desenfoca(lz, 6)
    oscurece(lz, 0.3)
    cx = W * 0.62
    PF.actor(lz, "sapi_hoja/00", cx, H * 0.98, H * 0.86, op=0.30, tono=FANTASMA, suelo=0, sombra=False)
    rot_(lz, "EL ATUENDO, DIBUJADO", W * 0.62, H * 0.06, 40, t, R_f[15], R_gorro - 0.3)
    pega(lz, "utileria_ropa/06", cx, H * 0.18, H * 0.18, t, R_gorro)
    pega(lz, "utileria_ropa/03", cx, H * 0.40, H * 0.30, t, R_camisa)
    pega(lz, "utileria_ropa/04", cx, H * 0.66, H * 0.26, t, R_pant)
    pega(lz, "utileria_ropa/05", cx, H * 0.88, H * 0.16, t, R_botas)
    rot_(lz, "GORRO", W * 0.32, H * 0.18, 46, t, R_gorro)
    rot_(lz, "CAMISA", W * 0.32, H * 0.40, 46, t, R_camisa)
    rot_(lz, "PANTALONES", W * 0.32, H * 0.66, 46, t, R_pant)
    rot_(lz, "BOTAS", W * 0.32, H * 0.88, 46, t, R_botas)


RO11 = PF.Plano("campamento_sol", R_f[16] - 0.4, F(CV, 0), z0=1.04, z1=1.14, c0=(0.48, 0.56), c1=(0.54, 0.56), par=(28, 6))
snd(R_moda, "bling", 0.6)


@toma(R_f[16] - 0.4, ("fundido", 0.6))
def ro11(lz, t):
    RO11.fondo(lz, t)
    humo_en(lz, RO11, t, 0.42, 0.62, s=0.6, op=0.16, sem=5)
    anda(lz, RO11, t, "cazadora_camina", R_f[16] - 0.4, F(CV, 0) + 0.4, 0.10, 0.50, 0.94, 0.44, tono=DIA, desde_antes=True)
    quieto(lz, RO11, t, "gente_hoja/02", 0.76, 0.90, 0.38, tono=DIA, flip=True)
    nieve(lz, t, n=40, viento=0.2, op=0.35, sem=32)
    rot_(lz, "UN TRAJE COMPLETO PARA LA NIEVE", W * 0.50, H * 0.13, 50, t, R_f[16])
    rot_(lz, "YA HABÍA MODA", W * 0.66, H * 0.28, 66, t, R_moda, rot=3)


# ================================================================== CUEVAS (376 - 453,3)
V_f = [F(CV, i) for i in range(13)]
V_mito, V_no = T(CV, "mito", 0), T(CV, "no", 1)
V_conservan = T(CV, "conservan", 2)
V_oscuro, V_humedo, V_diez = T(CV, "oscuro", 3), T(CV, "húmedo", 3), T(CV, "diez", 3)
V_entrada = T(CV, "entrada", 4)
V_casas = T(CV, "casas", 5)
V_don, V_circulo = T(CV, "don", 6), T(CV, "círculo", 6)
V_doce = T(CV, "doce", 7)
V_sesenta, V_craneos, V_mandib, V_colmi = T(CV, "sesenta", 8), T(CV, "cráneos", 8), T(CV, "mandíbulas", 8), T(CV, "colmillos", 8)
V_veinti = T(CV, "veinticinco", 9)
V_casa2, V_almacen, V_reunion = T(CV, "casa", 10), T(CV, "almacén", 10), T(CV, "reunión", 10)
V_vigas, V_esqueleto = T(CV, "vigas", 11), T(CV, "esqueleto", 11)
V_carne, V_grasa, V_huesos, V_marfil = T(CV, "carne", 12), T(CV, "grasa", 12), T(CV, "huesos", 12), T(CV, "marfil", 12)

CV1 = PF.Plano("cueva_fondo_b", V_f[0] - 0.4, V_f[2], z0=1.04, z1=1.20, c0=(0.50, 0.52), c1=(0.54, 0.56), par=(26, 6))
snd(V_mito, "eco", 0.5)
snd(V_no, "error", 0.5)


@toma(V_f[0] - 0.4, ("negro", 0.7))
def cav1(lz, t):
    CV1.fondo(lz, t)
    brillo_en(lz, CV1, t, 0.56, 0.60, 100, color=(1.0, 0.55, 0.22), inten=0.35, sem=40, chis=3)
    quieto(lz, CV1, t, "neandertal_hoja/02", 0.50, 0.72, 0.30, tono=CUEVA)
    rot_(lz, "¿CAVERNÍCOLAS?", W * 0.50, H * 0.14, 80, t, V_mito)
    tacha(lz, W * 0.50, H * 0.14, H * 0.10, t, V_no)
    rot_(lz, "NO MUCHO", W * 0.50, H * 0.30, 60, t, V_no + 0.3, rot=3)


CV2 = PF.Plano("cueva_humeda", V_f[2] - 0.4, V_f[4], z0=1.04, z1=1.20, c0=(0.50, 0.56), c1=(0.40, 0.58), par=(26, 6))
for _k in range(6):
    snd(V_f[2] + 0.8 + 2.1 * _k, "gota", 0.4, tono=1.0 + 0.1 * (_k % 3))
GOTAS = [(0.22, 0.20, 0.0), (0.46, 0.14, 0.7), (0.70, 0.22, 1.3), (0.84, 0.16, 0.4)]


@toma(V_f[2] - 0.4, ("latigo", 0.5))
def cav2(lz, t):
    CV2.fondo(lz, t)
    brillo_en(lz, CV2, t, 0.20, 0.74, 90, color=(1.0, 0.55, 0.22), inten=0.30, sem=41)
    for x, y, f in GOTAS:                               # gotas que caen del techo
        u = ((t * 0.55 + f) % 1.0)
        X, Y, s = CV2.P(t, x, y + u * 0.55)
        PF._blob(lz, X, Y, 6 * s, (0.80, 0.90, 1.0), 0.8 * (1 - u * 0.6))
    quieto(lz, CV2, t, "huesos_mamut/02", 0.58, 0.88, 0.10, tono=CUEVA, t_in=V_conservan, rot=-10)
    quieto(lz, CV2, t, "huesos_mamut/01", 0.74, 0.92, 0.14, tono=CUEVA, t_in=V_conservan + 0.3, rot=6)
    rot_(lz, "AQUÍ LOS RESTOS SE CONSERVAN", W * 0.50, H * 0.13, 50, t, V_conservan, V_oscuro - 0.3)
    rot_(lz, "OSCURO", W * 0.24, H * 0.14, 50, t, V_oscuro)
    rot_(lz, "HÚMEDO", W * 0.50, H * 0.20, 50, t, V_humedo, rot=2)
    rot_(lz, "SIEMPRE 10 °C", W * 0.76, H * 0.14, 50, t, V_diez, rot=-2)


CV3 = PF.Plano("abrigo_entrada", V_f[4] - 0.4, V_f[5], z0=1.04, z1=1.16, c0=(0.44, 0.58), c1=(0.50, 0.58), par=(28, 6))
snd(V_f[4], "fuego", 0.5, dur=5.0)


@toma(V_f[4] - 0.4, ("desenfoque", 0.5))
def cav3(lz, t):
    CV3.fondo(lz, t)
    brillo_en(lz, CV3, t, 0.29, 0.64, 140, color=(1.0, 0.55, 0.22), inten=0.45, sem=42, chis=5)
    humo_en(lz, CV3, t, 0.29, 0.62, s=0.9, op=0.22, sem=6)
    quieto(lz, CV3, t, "cazadora_hoja/00", 0.44, 0.86, 0.32, tono=CALIDO)
    quieto(lz, CV3, t, "gente_hoja/04", 0.16, 0.86, 0.34, tono=CALIDO, fase=1.0)
    paseo(lz, CV3, t, "gente_hoja/01", V_f[4], V_f[5], 0.80, 0.60, 0.84, 0.24, tono=DIA, pasos=3.0)
    rot_(lz, "EN LA ENTRADA", W * 0.62, H * 0.13, 58, t, V_entrada)
    rot_(lz, "O AL AIRE LIBRE", W * 0.70, H * 0.27, 50, t, T(CV, "aire", 4), rot=2)


CV4 = PF.Plano("rio_don", V_f[5] - 0.4, V_f[7], z0=1.04, z1=1.20, c0=(0.50, 0.54), c1=(0.58, 0.58), par=(30, 8))
snd(V_casas, "papel", 0.5)
snd(V_don, "papel", 0.5)
snd(V_circulo, "golpe_suave", 0.6)


@toma(V_f[5] - 0.4, ("latigo", 0.5))
def cav4(lz, t):
    CV4.fondo(lz, t)
    brillo_en(lz, CV4, t, 0.80, 0.75, 110, color=(1.0, 0.55, 0.22), inten=0.40, sem=43, chis=4)
    paseo(lz, CV4, t, "cazadora_hoja/02", V_f[5] - 0.4, V_f[7], 0.10, 0.52, 0.94, 0.40, tono=DIA, pasos=2.0)
    nieve(lz, t, n=60, viento=0.4, op=0.45, sem=40)
    rot_(lz, "CONSTRUYERON CASAS", W * 0.50, H * 0.13, 60, t, V_casas)
    rot_(lz, "RÍO DON · RUSIA", W * 0.66, H * 0.26, 52, t, V_don, rot=2)


CV5 = PF.Plano("casa_mamut", V_f[7] - 0.4, V_f[9], z0=1.04, z1=1.24, c0=(0.50, 0.52), c1=(0.52, 0.48), par=(30, 8))
snd(V_doce, "crece", 0.5)
snd(V_craneos, "pop", 0.6)
snd(V_mandib, "pop", 0.6, tono=0.9)
snd(V_colmi, "pop", 0.6, tono=1.1)


@toma(V_f[7] - 0.4, ("destello", 0.8))
def cav5(lz, t):
    CV5.fondo(lz, t)
    brillo_en(lz, CV5, t, 0.47, 0.67, 90, color=(1.0, 0.55, 0.22), inten=0.45, sem=44, chis=4)
    humo_en(lz, CV5, t, 0.53, 0.18, s=0.8, op=0.18, sem=7)
    quieto(lz, CV5, t, "gente_hoja/03", 0.80, 0.88, 0.22, tono=DIA, flip=True)
    X0, Y0, _ = CV5.P(t, 0.36, 0.80)
    X1, Y1, _ = CV5.P(t, 0.74, 0.80)
    cota(lz, X0, Y0, X1, Y1, t, V_doce - 0.2)
    rot_(lz, "12,5 METROS", (X0 + X1) / 2, Y0 + 60, 54, t, V_doce)
    if t > V_sesenta - 0.3:
        rot_(lz, "MÁS DE 60 MAMUTS", W * 0.50, H * 0.13, 62, t, V_sesenta)
        pega(lz, "huesos_mamut/00", W * 0.14, H * 0.40, H * 0.24, t, V_craneos)
        pega(lz, "huesos_mamut/02", W * 0.14, H * 0.66, H * 0.18, t, V_mandib, rot=-6)
        pega(lz, "huesos_mamut/03", W * 0.86, H * 0.50, H * 0.26, t, V_colmi, rot=10)


CV6 = PF.Plano("casa_mamut_dentro", V_f[9] - 0.4, V_f[11], z0=1.04, z1=1.18, c0=(0.50, 0.56), c1=(0.50, 0.60), par=(28, 6))
snd(V_f[9], "fuego", 0.6, dur=12.0)
snd(V_veinti, "papel", 0.5)
snd(V_casa2, "pop", 0.4)
snd(V_almacen, "pop", 0.4, tono=1.1)
snd(V_reunion, "pop", 0.4, tono=0.9)


@toma(V_f[9] - 0.4, ("desenfoque", 0.6))
def cav6(lz, t):
    CV6.fondo(lz, t)
    brillo_en(lz, CV6, t, 0.50, 0.58, 220, color=(1.0, 0.55, 0.22), inten=0.55, sem=45, chis=8)
    humo_en(lz, CV6, t, 0.50, 0.50, s=0.9, op=0.16, sem=8)
    quieto(lz, CV6, t, "grupo_dormir/01", 0.30, 0.88, 0.34, tono=FUEGO)
    quieto(lz, CV6, t, "gente_hoja/00", 0.74, 0.90, 0.38, tono=FUEGO, flip=True, fase=1.0)
    rot_(lz, "HACE 25 000 AÑOS", W * 0.50, H * 0.13, 58, t, V_veinti)
    rot_(lz, "¿CASA?", W * 0.20, H * 0.30, 54, t, V_casa2, rot=-3)
    rot_(lz, "¿ALMACÉN?", W * 0.50, H * 0.26, 54, t, V_almacen, rot=2)
    rot_(lz, "¿REUNIÓN?", W * 0.80, H * 0.30, 54, t, V_reunion, rot=-2)


CV7 = PF.Plano("casa_mamut_dentro_b", V_f[11] - 0.4, F(NO, 0), z0=1.06, z1=1.22, c0=(0.50, 0.50), c1=(0.52, 0.56), par=(28, 6))
snd(V_esqueleto, "golpe_suave", 0.6)
snd(V_carne, "pop", 0.5)
snd(V_grasa, "pop", 0.5, tono=1.1)
snd(V_huesos, "pop", 0.5, tono=0.9)
snd(V_marfil, "bling", 0.5)


@toma(V_f[11] - 0.4, ("latigo", 0.5))
def cav7(lz, t):
    CV7.fondo(lz, t)
    brillo_en(lz, CV7, t, 0.50, 0.62, 200, color=(1.0, 0.55, 0.22), inten=0.45, sem=46, chis=6)
    quieto(lz, CV7, t, "cazadora_hoja/02", 0.30, 0.92, 0.40, tono=FUEGO, t_out=V_carne - 0.5)
    rot_(lz, "SIN ÁRBOLES PARA VIGAS", W * 0.50, H * 0.13, 54, t, V_vigas, V_carne - 0.4)
    rot_(lz, "NADA SE DESPERDICIABA", W * 0.50, H * 0.13, 58, t, V_carne - 0.3)
    if t > V_carne - 0.5:
        oscurece(lz, 0.3 * smooth(prog(t, V_carne - 0.5, V_carne)))
    for k, (pz, tk, txt) in enumerate((("utileria_fuego/14", V_carne, "COMIDA"), ("utileria_fuego/13", V_grasa, "COMBUSTIBLE"),
                                      ("huesos_mamut/05", V_huesos, "PAREDES"), ("utileria_ropa/02", V_marfil, "JOYERÍA"))):
        X = W * (0.16 + 0.226 * k)
        pega(lz, pz, X, H * 0.50, H * 0.24, t, tk, rot=(-1) ** k * 5)
        rot_(lz, txt, X, H * 0.72, 42, t, tk + 0.2, rot=(-1) ** k * 2)


# ================================================================== NOCHE (453,3 - 512)
N_f = [F(NO, i) for i in range(11)]
N_noche, N_veinti = T(NO, "noche", 0), T(NO, "veinticinco", 1)
N_viento, N_nieve = T(NO, "viento", 2), T(NO, "nieve", 2)
N_ropa, N_mojado, N_secar = T(NO, "ropa", 3), T(NO, "mojado", 3), T(NO, "secar", 3)
N_roba = T(NO, "roba", 4)
N_agua, N_comer, N_error = T(NO, "agua", 5), T(NO, "comer", 5), T(NO, "error", 5)
N_derretian = T(NO, "derretían", 6)
N_solo = T(NO, "solo", 7)
N_juntos, N_ninos = T(NO, "juntos", 8), T(NO, "niños", 8)
N_bombilla, N_cien, N_diez, N_estufa = T(NO, "bombilla", 9), T(NO, "cien", 9), T(NO, "diez", 9), T(NO, "estufa", 9)
N_gente = T(NO, "gente", 10)

NO1 = PF.Plano("choza_noche", N_f[0] - 0.4, N_f[3], z0=1.04, z1=1.30, c0=(0.50, 0.55), c1=(0.62, 0.60), par=(30, 8))
snd(N_f[0] - 0.3, "viento", 0.8, dur=14.0)
snd(N_veinti, "papel", 0.5)


@toma(N_f[0] - 0.4, ("negro", 0.7))
def no1(lz, t):
    NO1.fondo(lz, t)
    brillo_en(lz, NO1, t, 0.65, 0.62, 140, color=(1.0, 0.55, 0.22), inten=0.50, sem=50)
    # la cazadora llega a la choza contra el viento y entra
    k = 1.0 - smooth(prog(t, N_f[2] - 0.5, N_f[2] + 0.3))
    anda(lz, NO1, t, "cazadora_camina", N_f[0] - 0.4, N_f[2], 0.10, 0.60, 0.80, 0.34, tono=NOCHE, desde_antes=True, op=k)
    nieve(lz, t, n=170, viento=1.4 + 1.2 * smooth(prog(t, N_viento - 0.5, N_viento + 1.0)), op=0.8, sem=50)
    rot_(lz, "UNA NOCHE DE INVIERNO", W * 0.32, H * 0.13, 56, t, N_f[1])
    rot_(lz, "HACE 25 000 AÑOS", W * 0.32, H * 0.25, 48, t, N_veinti, rot=2)


NO2 = PF.Plano("choza_dentro", N_f[3] - 0.4, N_f[5], z0=1.04, z1=1.18, c0=(0.48, 0.56), c1=(0.40, 0.56), par=(26, 6))
snd(N_f[3], "fuego", 0.6, dur=11.0)
snd(N_secar, "siseo", 0.4)
snd(N_roba, "brr", 0.4)


@toma(N_f[3] - 0.4, ("desenfoque", 0.6))
def no2(lz, t):
    NO2.fondo(lz, t)
    brillo_en(lz, NO2, t, 0.63, 0.55, 220, color=(1.0, 0.55, 0.22), inten=0.55, sem=51, chis=8)
    humo_en(lz, NO2, t, 0.32, 0.36, s=0.6, color=(0.92, 0.90, 0.86), op=0.18, sem=9)        # vapor de la ropa que se seca
    quieto(lz, NO2, t, "cazadora_hoja/03", 0.64, 0.92, 0.42, tono=FUEGO, flip=True)
    pega(lz, "utileria_ropa/08", W * 0.20, H * 0.62, H * 0.18, t, N_mojado, rot=-6)
    rot_(lz, "REVISAR LA ROPA", W * 0.50, H * 0.13, 56, t, N_ropa)
    rot_(lz, "MOJADA = FRÍO", W * 0.24, H * 0.80, 52, t, N_roba, rot=-2)


NO3 = PF.Plano("choza_dentro", N_f[5] - 0.4, N_f[7], z0=1.55, z1=1.70, c0=(0.52, 0.58), c1=(0.56, 0.58), par=(22, 6))
snd(N_agua, "gota", 0.5)
snd(N_error, "error", 0.5)
snd(N_derretian, "siseo", 0.5)


@toma(N_f[5] - 0.4, ("latigo", 0.5))
def no3(lz, t):
    NO3.fondo(lz, t)
    brillo_en(lz, NO3, t, 0.63, 0.55, 220, color=(1.0, 0.55, 0.22), inten=0.55, sem=52, chis=8)
    X, Y, h = W * 0.24, H * 1.02, H * 0.82
    PF.actor(lz, "sapi_hoja/04" if t < N_derretian else "sapi_hoja/01", X, Y, h, tono=FUEGO, sy=PF.respira(t), suelo=0)
    pega(lz, "iglu_utileria/01", W * 0.64, H * 0.36, H * 0.20, t, N_comer, N_derretian - 0.3, rot=-4)
    if t < N_derretian - 0.3:
        tacha(lz, W * 0.64, H * 0.36, H * 0.13, t, N_error)
    if t > N_derretian - 0.3:
        X2, Y2, s = NO3.P(t, 0.51, 0.62)
        PF.humo(lz, t, X2, Y2 - 40, s=1.3, color=(0.95, 0.95, 0.95), op=0.22, sem=11)
        rot_(lz, "DERRETIRLA JUNTO AL FUEGO", W * 0.62, H * 0.13, 52, t, N_derretian)
    rot_(lz, "COMER NIEVE: UN ERROR", W * 0.62, H * 0.13, 52, t, N_error, N_derretian - 0.3)


NO4 = PF.Plano("choza_dentro", N_f[7] - 0.4, N_f[9], z0=1.20, z1=1.30, c0=(0.50, 0.66), c1=(0.52, 0.66), par=(22, 6))
snd(N_f[7], "fuego", 0.4, dur=9.0)
snd(N_ninos, "pop", 0.4)


@toma(N_f[7] - 0.4, ("fundido", 0.7))
def no4(lz, t):
    NO4.fondo(lz, t)
    oscurece(lz, 0.25)
    brillo_en(lz, NO4, t, 0.63, 0.55, 200, color=(1.0, 0.50, 0.20), inten=0.45, sem=53, chis=4)
    quieto(lz, NO4, t, "grupo_dormir/00", 0.40, 0.95, 0.40, tono=FUEGO, fase=0.5)
    quieto(lz, NO4, t, "grupo_dormir/02", 0.84, 0.90, 0.36, tono=FUEGO, flip=True)
    rot_(lz, "NADIE DORMÍA SOLO", W * 0.50, H * 0.13, 58, t, N_solo)
    rot_(lz, "LOS NIÑOS, EN MEDIO", W * 0.40, H * 0.30, 48, t, N_ninos, rot=2)


NO5 = PF.Plano("choza_dentro", N_f[9] - 0.4, F(AR, 0), z0=1.2, z1=1.2, c0=(0.5, 0.6), c1=(0.5, 0.6), par=(0, 0))
snd(N_bombilla, "ding", 0.5)
snd(N_estufa, "fuego", 0.6, dur=3.0)
snd(N_gente, "bling", 0.5)


@toma(N_f[9] - 0.4, ("desenfoque", 0.5))
def no5(lz, t):
    NO5.fondo(lz, t)
    desenfoca(lz, 6)
    oscurece(lz, 0.35)
    k = smooth(prog(t, N_diez - 0.3, N_estufa))
    X, Y, h = W * 0.30, H * 0.52, H * 0.40
    PF.brillo(lz, X, Y, 300, color=(1.0, 0.85, 0.45), inten=0.30 * PF.entra(t, N_bombilla, 0.5), t=t)
    pega(lz, "moderno_hoja/09", X, Y, h, t, N_bombilla)
    rot_(lz, "100 W", X, H * 0.84, 70, t, N_cien)
    pega(lz, "grupo_dormir/00", W * 0.72, H * 0.50, H * 0.36, t, N_diez - 0.2)
    PF.brillo(lz, W * 0.72, H * 0.50, 420, color=(1.0, 0.55, 0.22), inten=0.45 * k, t=t)
    rot_(lz, "x 10 = UNA ESTUFA", W * 0.72, H * 0.84, 56, t, N_estufa - 0.3)
    rot_(lz, "LA CALEFACCIÓN MÁS ANTIGUA: LA GENTE", W * 0.50, H * 0.13, 50, t, N_gente - 0.6)


# ================================================================== ÁRTICO (512 - 576)
A_f = [F(AR, i) for i in range(11)]
A_lejos = T(AR, "lejos", 0)
A_circulo, A_treinta = T(AR, "círculo", 1), T(AR, "treinta", 1)
A_sol, A_mamuts, A_renos, A_liebres = T(AR, "sol", 2), T(AR, "mamuts", 2), T(AR, "renos", 2), T(AR, "liebres", 2)
A_fuerte, A_preparada = T(AR, "fuerte", 3), T(AR, "preparada", 3)
A_plato = T(AR, "plato", 4)
A_energia = T(AR, "energía", 5)
A_grasa, A_magra = T(AR, "grasa", 6), T(AR, "magra", 6)
A_tuetano, A_hervian = T(AR, "tuétano", 7), T(AR, "hervían", 7)
A_alaska = T(AR, "alaska", 8)
A_extremo = T(AR, "extremo", 9)
A_frio = T(AR, "frío", 10)

# mapa_mundo_b (rejilla previews/_rej5.jpg)
RUTA_NORTE = [(0.55, 0.62), (0.58, 0.48), (0.53, 0.40), (0.62, 0.32), (0.72, 0.24), (0.76, 0.19)]
RUTA_AMER_B = [(0.10, 0.30), (0.18, 0.38), (0.24, 0.52), (0.29, 0.70), (0.32, 0.88)]
AR1 = PF.Plano("mapa_mundo_b", A_f[0] - 0.4, A_f[1], z0=1.04, z1=1.40, c0=(0.50, 0.50), c1=(0.66, 0.32), par=(0, 0), mano=0.4)
snd(A_f[0], "garabato", 0.5)
snd(A_lejos, "pop", 0.5)


@toma(A_f[0] - 0.4, ("destello", 0.8))
def ar1(lz, t):
    AR1.fondo(lz, t)
    ruta_mapa(lz, AR1, t, A_f[0], A_lejos + 0.8, RUTA_NORTE)
    X, Y, _ = AR1.P(t, *RUTA_NORTE[-1])
    pega(lz, "utileria_fuego/00", X, Y - 30, 110, t, A_lejos)
    rot_(lz, "MÁS LEJOS QUE NUNCA", W * 0.50, H * 0.85, 56, t, A_lejos - 0.4)


AR2 = PF.Plano("artico_noche", A_f[1] - 0.4, A_f[3], z0=1.04, z1=1.18, c0=(0.50, 0.52), c1=(0.56, 0.56), par=(30, 8))
snd(A_f[1], "viento", 0.6, dur=13.0)
snd(A_mamuts, "pop", 0.5)
snd(A_renos, "pop", 0.5, tono=1.1)
snd(A_liebres, "pop", 0.5, tono=1.3)


@toma(A_f[1] - 0.4, ("desenfoque", 0.6))
def ar2(lz, t):
    AR2.fondo(lz, t)
    for k, x in enumerate((0.25, 0.50, 0.75)):                     # la aurora late
        X, Y, s = AR2.P(t, x, 0.10)
        PF.brillo(lz, X + 40 * math.sin(t * 0.5 + k), Y, 420 * s / 1.4, color=(0.35, 1.0, 0.55),
                  inten=0.10 + 0.06 * math.sin(t * 0.9 + 2 * k), t=t, sem=k)
    brillo_en(lz, AR2, t, 0.50, 0.60, 150, color=(1.0, 0.55, 0.22), inten=0.50, sem=54, chis=5)
    anda(lz, AR2, t, "renos_camina", A_f[1] - 0.4, A_f[3] + 0.4, 1.05, 0.55, 0.72, 0.16, paso=1.3, tono=NOCHE, desde_antes=True)
    anda(lz, AR2, t, "cazador_corre", A_f[1] - 0.4, A_f[3] + 0.4, -0.10, 0.70, 0.93, 0.38, paso=1.35, tono=NOCHE, desde_antes=True)
    pega(lz, "mamut_camina/ciclo_00", W * 0.16, H * 0.30, H * 0.18, t, A_mamuts, A_f[3] - 0.3)
    pega(lz, "fauna_hoja/08", W * 0.84, H * 0.30, H * 0.16, t, A_liebres, A_f[3] - 0.3)
    nieve(lz, t, n=80, viento=0.6, op=0.6, sem=51)
    rot_(lz, "CÍRCULO POLAR ÁRTICO", W * 0.50, H * 0.13, 58, t, A_circulo, A_sol - 0.3)
    rot_(lz, "HACE 32 000 AÑOS", W * 0.50, H * 0.25, 48, t, A_treinta, A_sol - 0.3, rot=2)
    rot_(lz, "SEMANAS SIN SOL", W * 0.50, H * 0.13, 60, t, A_sol)


AR3 = PF.Plano("artico_noche_b", A_f[3] - 0.4, A_f[5], z0=1.06, z1=1.16, c0=(0.50, 0.58), c1=(0.46, 0.60), par=(28, 6))
snd(A_preparada, "bling", 0.5)
snd(A_plato, "clink", 0.6)


@toma(A_f[3] - 0.4, ("latigo", 0.5))
def ar3(lz, t):
    AR3.fondo(lz, t)
    brillo_en(lz, AR3, t, 0.63, 0.58, 160, color=(1.0, 0.55, 0.22), inten=0.50, sem=55, chis=5)
    quieto(lz, AR3, t, "cazadora_hoja/01", 0.30, 0.96, 0.56, tono=NOCHE)
    nieve(lz, t, n=90, viento=0.8, op=0.65, sem=52)
    rot_(lz, "NO POR SER MÁS FUERTE", W * 0.64, H * 0.20, 50, t, A_fuerte)
    rot_(lz, "LLEGÓ PREPARADA", W * 0.64, H * 0.34, 64, t, A_preparada, rot=2)
    pega(lz, "utileria_fuego/14", W * 0.70, H * 0.66, H * 0.22, t, A_plato, rot=-8)


AR4 = PF.Plano("cueva_siberia_b", A_f[5] - 0.4, A_f[8], z0=1.06, z1=1.24, c0=(0.60, 0.58), c1=(0.70, 0.62), par=(28, 6))
snd(A_energia, "crece", 0.5)
snd(A_grasa, "pop", 0.6)
snd(A_magra, "pop", 0.5, tono=0.8)
for _k in range(4):
    snd(A_tuetano - 0.6 + 0.55 * _k, "golpe_suave", 0.5)
snd(A_hervian, "burbujas", 0.5)


@toma(A_f[5] - 0.4, ("desenfoque", 0.5))
def ar4(lz, t):
    AR4.fondo(lz, t)
    brillo_en(lz, AR4, t, 0.77, 0.66, 140, color=(1.0, 0.55, 0.22), inten=0.50, sem=56, chis=5)
    nieve(lz, t, n=60, viento=0.4, op=0.5, sem=53)
    golpe = abs(math.sin((t - A_tuetano) * math.pi / 0.55)) if t > A_tuetano - 0.6 else 1.0
    if not (A_grasa - 0.4 < t < A_tuetano - 0.6):
        quieto(lz, AR4, t, "neandertal_hoja/01", 0.50, 0.95, 0.46, tono=DIA, rot=-3 * (1 - golpe))
    rot_(lz, "EL CUERPO QUEMA ENERGÍA", W * 0.40, H * 0.13, 54, t, A_energia, A_grasa - 0.4)
    if A_grasa - 0.4 < t < A_tuetano - 0.5:
        oscurece(lz, 0.3)
    pega(lz, "utileria_fuego/13", W * 0.30, H * 0.46, H * 0.32, t, A_grasa, A_tuetano - 0.6)
    rot_(lz, ">", W * 0.50, H * 0.46, 120, t, A_magra - 0.3, A_tuetano - 0.6, rot=0)
    pega(lz, "utileria_fuego/14", W * 0.70, H * 0.48, H * 0.18, t, A_magra, A_tuetano - 0.6)
    rot_(lz, "GRASA", W * 0.30, H * 0.72, 56, t, A_grasa + 0.2, A_tuetano - 0.6)
    rot_(lz, "CARNE MAGRA", W * 0.70, H * 0.72, 48, t, A_magra + 0.2, A_tuetano - 0.6)
    pega(lz, "utileria_fuego/06", W * 0.20, H * 0.34, H * 0.24, t, A_tuetano, rot=-8)
    rot_(lz, "EL TUÉTANO", W * 0.20, H * 0.52, 50, t, A_tuetano + 0.3)
    if t > A_hervian - 0.3:
        pega(lz, "utileria_fuego/12", W * 0.84, H * 0.44, H * 0.22, t, A_hervian - 0.3)
        PF.humo(lz, t, W * 0.84, H * 0.36, s=1.2, color=(0.95, 0.95, 0.95), op=0.22, sem=12)


AR5 = PF.Plano("puente_bering_b", A_f[8] - 0.4, A_f[9], z0=1.03, z1=1.12, c0=(0.46, 0.55), c1=(0.54, 0.55), par=(30, 8))
snd(A_f[8], "pasos", 0.5, dur=6.0)
snd(A_alaska, "papel", 0.5)


@toma(A_f[8] - 0.4, ("latigo", 0.5))
def ar5(lz, t):
    AR5.fondo(lz, t)
    brillo_en(lz, AR5, t, 0.70, 0.60, 110, color=(1.0, 0.55, 0.22), inten=0.40, sem=57, chis=4)
    ta, tb = A_f[8] - 0.4, A_f[9] + 0.4
    anda(lz, AR5, t, "renos_camina", ta, tb, 0.30, 0.80, 0.70, 0.16, paso=1.3, tono=DIA, desde_antes=True)
    anda(lz, AR5, t, "cazadora_camina", ta, tb, 0.18, 0.56, 0.86, 0.32, tono=DIA, desde_antes=True)
    anda(lz, AR5, t, "cazador_corre", ta, tb, -0.08, 0.40, 0.95, 0.40, paso=1.6, tono=DIA, desde_antes=True)
    nieve(lz, t, n=50, viento=0.5, op=0.45, sem=54)
    rot_(lz, "DE SIBERIA A ALASKA", W * 0.50, H * 0.13, 60, t, A_alaska - 0.6)


AR6 = PF.Plano("mapa_mundo_b", A_f[9] - 0.4, A_f[10], z0=1.04, z1=1.04, c0=(0.50, 0.50), c1=(0.50, 0.50), par=(0, 0), mano=0.4)
snd(A_f[9], "garabato", 0.5)
snd(A_extremo, "bling", 0.5)


@toma(A_f[9] - 0.4, ("desenfoque", 0.5))
def ar6(lz, t):
    AR6.fondo(lz, t)
    ruta_mapa(lz, AR6, t, A_f[9] - 0.4, A_f[9] + 0.2, RUTA_NORTE + [(0.86, 0.30)])
    ruta_mapa(lz, AR6, t, A_f[9] + 0.3, A_extremo + 0.6, RUTA_AMER_B)
    rot_(lz, "DE UN EXTREMO AL OTRO DEL PLANETA", W * 0.50, H * 0.92, 50, t, A_extremo - 0.3)


AR7 = PF.Plano("iglu_fuera_b", A_f[10] - 0.4, F(IG, 0), z0=1.04, z1=1.22, c0=(0.50, 0.55), c1=(0.44, 0.58), par=(30, 8))
snd(A_f[10], "viento", 0.6, dur=7.0)
snd(A_frio, "hielo", 0.5)


@toma(A_f[10] - 0.4, ("fundido", 0.6))
def ar7(lz, t):
    AR7.fondo(lz, t)
    brillo_en(lz, AR7, t, 0.58, 0.48, 70, color=(1.0, 0.60, 0.25), inten=0.45, sem=58)
    brillo_en(lz, AR7, t, 0.36, 0.63, 60, color=(1.0, 0.55, 0.22), inten=0.30, sem=59)
    paseo(lz, AR7, t, "inuit_hoja/04", A_f[10] - 0.4, A_f[10] + 3.5, 0.90, 0.66, 0.90, 0.40, tono=GRIS, pasos=2.0)
    nieve(lz, t, n=110, viento=1.0, op=0.65, sem=55)
    rot_(lz, "UNA CASA HECHA DE FRÍO", W * 0.50, H * 0.13, 60, t, A_frio - 0.5)


# ================================================================== IGLÚ (576 - 642,7)
G_f = [F(IG, i) for i in range(12)]
G_absurdo, G_nieve = T(IG, "absurdo", 1), T(IG, "nieve", 1)
G_burbujas, G_aisla = T(IG, "burbujas", 2), T(IG, "aísla", 2)
G_bloques, G_espiral, G_cupula = T(IG, "bloques", 3), T(IG, "espiral", 3), T(IG, "cúpula", 3)
G_entrada = T(IG, "entrada", 4)
G_tunel, G_baja = T(IG, "túnel", 5), T(IG, "baja", 5)
G_frio, G_abajo = T(IG, "frío", 6), T(IG, "abajo", 6)
G_plataforma, G_tibio = T(IG, "plataforma", 7), T(IG, "tibio", 7)
G_lampara, G_decenas = T(IG, "lámpara", 8), T(IG, "decenas", 8)
G_afuera, G_adentro, G_comodidad = T(IG, "afuera", 9), T(IG, "adentro", 9), T(IG, "comodidad", 9)
G_fisica, G_abuelos = T(IG, "física", 10), T(IG, "abuelos", 10)
G_casa, G_paredes, G_poco, G_centro = T(IG, "casa", 11), T(IG, "paredes", 11), T(IG, "poco", 11), T(IG, "centro", 11)

IG1 = PF.Plano("iglu_fuera", G_f[0] - 0.5, G_f[2], z0=1.04, z1=1.16, c0=(0.55, 0.50), c1=(0.52, 0.54), par=(30, 8))
snd(G_f[0] - 0.1, "papel", 0.6)
snd(G_absurdo, "boing", 0.4)


@toma(G_f[0] - 0.5, ("destello", 0.8))
def ig1(lz, t):
    IG1.fondo(lz, t)
    brillo_en(lz, IG1, t, 0.74, 0.38, 70, color=(1.0, 0.60, 0.25), inten=0.45, sem=60)
    nieve(lz, t, n=80, viento=0.5, op=0.55, sem=60)
    X, Y, h = IG1.en(t, 0.24, 0.96, 0.50)
    dx, rr = tirita(t, 0.5)
    PF.actor(lz, "sapi_hoja/04", X + dx, Y, h, rot=rr, tono=GRIS, sy=PF.respira(t))
    aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.2 * h, t, G_f[0])
    rot_(lz, "3. EL IGLÚ", W * 0.50, H * 0.15, 92, t, G_f[0] - 0.1, G_absurdo - 0.3)
    rot_(lz, "¿CALIENTE? ¿CON NIEVE?", W * 0.56, H * 0.15, 60, t, G_absurdo)


IG2 = PF.Plano("iglu_fuera", G_f[2] - 0.4, G_f[3], z0=1.3, z1=1.3, c0=(0.6, 0.45), c1=(0.6, 0.45), par=(0, 0))
snd(G_burbujas, "burbujas", 0.6)
snd(G_aisla, "bling", 0.5)


@toma(G_f[2] - 0.4, ("desenfoque", 0.5))
def ig2(lz, t):
    IG2.fondo(lz, t)
    desenfoca(lz, 7)
    oscurece(lz, 0.25)
    k = PF.entra(t, G_f[2] - 0.2, 0.5)
    PF.actor(lz, "iglu_utileria/00", W * 0.40, H * 0.52, H * 0.46 * (0.6 + 0.4 * k), ancla=(0.5, 0.5), suelo=0, op=clamp01(k * 3))
    burbujas(lz, W * 0.40, H * 0.52, H * 0.16, t, G_burbujas - 0.2, n=22)
    rot_(lz, "LLENA DE AIRE", W * 0.74, H * 0.36, 56, t, G_burbujas)
    rot_(lz, "AIRE QUIETO = AISLANTE", W * 0.72, H * 0.56, 52, t, G_aisla - 0.4, rot=2)


IG3 = PF.Plano("iglu_corte_b", G_f[3] - 0.4, G_f[4], z0=1.2, z1=1.2, c0=(0.5, 0.5), c1=(0.5, 0.5), par=(0, 0))
for _k in range(9):
    snd(G_bloques + 0.45 * _k, "pop", 0.35, tono=0.9 + 0.04 * _k)


def _bloques_cupula():
    out = []
    for fila, (n, r) in enumerate(((7, 1.0), (6, 0.86), (5, 0.68), (3, 0.44), (1, 0.12))):
        for i in range(n):
            a = math.pi * (i + 0.5) / n if n > 1 else math.pi / 2
            out.append((fila, -math.cos(a) * r * 0.32, -fila * 0.105, a))
    return out


BLOQUES = _bloques_cupula()


@toma(G_f[3] - 0.4, ("latigo", 0.5))
def ig3(lz, t):
    IG3.fondo(lz, t)
    desenfoca(lz, 6)
    oscurece(lz, 0.35)
    cx, cy = W * 0.50, H * 0.80
    for k, (fila, dx, dy, a) in enumerate(BLOQUES):
        tk = G_bloques + 0.13 * k
        if t < tk:
            continue
        u = PF.entra(t, tk, 0.35)
        PF.actor(lz, "iglu_utileria/0" + str(k % 2), cx + dx * W, cy + dy * H - (1 - u) * 60, H * 0.10 * (0.6 + 0.4 * u),
                 rot=math.degrees(a - math.pi / 2) * 0.6, ancla=(0.5, 0.5), suelo=0, op=clamp01(u * 3))
    quieto_p = PF.respira(t)
    PF.actor(lz, "inuit_hoja/00", W * 0.16, H * 0.96, H * 0.50, sy=quieto_p, tono=GRIS)
    PF.actor(lz, "inuit_hoja/01", W * 0.86, H * 0.96, H * 0.48, sy=quieto_p, tono=GRIS, flip=True)
    rot_(lz, "BLOQUES DE NIEVE EN ESPIRAL", W * 0.50, H * 0.13, 54, t, G_espiral - 0.5)
    rot_(lz, "UNA CÚPULA", W * 0.50, H * 0.26, 50, t, G_cupula, rot=2)


IG4 = PF.Plano("iglu_corte", G_f[4] - 0.4, G_f[8], z0=1.06, z1=1.14, c0=(0.50, 0.50), c1=(0.46, 0.54), par=(0, 0), mano=0.5)
snd(G_entrada, "pop", 0.5)
snd(G_baja, "whoosh", 0.4)
snd(G_frio, "viento", 0.5, dur=4.0)
snd(G_tibio, "fuego", 0.4, dur=4.0)


@functools.lru_cache(maxsize=4)
def _particulas(n, sem):
    return np.random.default_rng(sem).random((n, 3))


@toma(G_f[4] - 0.4, ("desenfoque", 0.6))
def ig4(lz, t):
    IG4.fondo(lz, t)
    brillo_en(lz, IG4, t, 0.61, 0.66, 70, color=(1.0, 0.60, 0.25), inten=0.45, sem=61)
    P = lambda x, y: IG4.P(t, x, y)[:2]                                       # noqa: E731
    if t > G_entrada - 0.2:                                                    # foco en la entrada
        k = smooth(prog(t, G_entrada - 0.2, G_entrada + 0.4)) * (1 - smooth(prog(t, G_frio - 0.3, G_frio + 0.3)))
        X, Y = P(0.27, 0.62)
        PF.brillo(lz, X, Y, 260, color=(1.0, 0.95, 0.70), inten=0.30 * k, t=t)
    # nivel del piso donde se duerme y nivel del túnel (más bajo)
    cota(lz, *P(0.60, 0.555), *P(0.86, 0.555), t, G_baja - 0.4, color=(0.95, 0.70, 0.30))
    cota(lz, *P(0.16, 0.70), *P(0.38, 0.70), t, G_baja, color=(0.45, 0.75, 1.0))
    rot_(lz, "PISO", *P(0.73, 0.50), 40, t, G_baja - 0.2)
    rot_(lz, "TÚNEL: MÁS BAJO", *P(0.27, 0.80), 42, t, G_baja + 0.2)
    if t > G_frio - 0.3:                                                       # el aire frío se queda abajo, en el túnel
        u = smooth(prog(t, G_frio - 0.3, G_frio + 1.2))
        trazo(lz, [P(0.04, 0.60), P(0.14, 0.68), P(0.26, 0.72), P(0.36, 0.72)], (0.25, 0.55, 0.95), 14, 0.9, u, punta=True)
        for x, y, f in _particulas(30, 3):
            ph = (t * 0.25 + f) % 1.0
            X, Y = P(0.06 + 0.30 * ph, 0.66 + 0.06 * y)
            PF._blob(lz, X, Y, 9, (0.55, 0.80, 1.0), 0.6 * u)
        rot_(lz, "EL AIRE FRÍO PESA MÁS", *P(0.22, 0.42), 44, t, G_abajo - 0.6, rot=-2)
    if t > G_plataforma - 0.3:                                                 # el aire tibio sube hasta la plataforma
        u = smooth(prog(t, G_plataforma - 0.3, G_plataforma + 1.2))
        trazo(lz, [P(0.61, 0.62), P(0.58, 0.40), P(0.60, 0.28), P(0.70, 0.36), P(0.70, 0.46)], (0.95, 0.50, 0.20), 14, 0.9, u,
              punta=True)
        for x, y, f in _particulas(30, 5):
            ph = (t * 0.22 + f) % 1.0
            X, Y = P(0.58 + 0.12 * x, 0.62 - 0.36 * ph)
            PF._blob(lz, X, Y, 9, (1.0, 0.70, 0.35), 0.55 * u * (1 - ph))
        rot_(lz, "AIRE TIBIO ARRIBA", *P(0.80, 0.24), 44, t, G_tibio - 0.4, rot=2)
    paseo(lz, IG4, t, "inuit_hoja/02", G_f[5], G_f[5] + 3.0, 0.06, 0.34, 0.76, 0.17, tono=GRIS, pasos=3.0, hasta_despues=False,
          desde_antes=False)


IG5 = PF.Plano("iglu_dentro", G_f[8] - 0.4, G_f[10], z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.54, 0.58), par=(26, 6))
snd(G_lampara, "fuego", 0.5, dur=10.0)
snd(G_afuera, "hielo", 0.5)
snd(G_adentro, "fuego", 0.5, dur=2.0)


@toma(G_f[8] - 0.4, ("fundido", 0.6))
def ig5(lz, t):
    IG5.fondo(lz, t)
    brillo_en(lz, IG5, t, 0.58, 0.66, 160, color=(1.0, 0.60, 0.25), inten=0.55, sem=62, chis=3)
    quieto(lz, IG5, t, "inuit_hoja/03", 0.44, 0.94, 0.42, tono=CALIDO)
    quieto(lz, IG5, t, "grupo_dormir/03", 0.30, 0.56, 0.18, tono=CALIDO, fase=1.0)
    rot_(lz, "CUERPOS + LÁMPARA DE FOCA", W * 0.50, H * 0.13, 52, t, G_lampara - 0.4, G_afuera - 0.4)
    if t > G_afuera - 0.4:
        rot_(lz, "AFUERA: -40 °C", W * 0.26, H * 0.15, 60, t, G_afuera, rot=-2, papel=(214, 232, 250))
        rot_(lz, "ADENTRO: CERCA DE 0 °C", W * 0.72, H * 0.15, 60, t, G_adentro, rot=2, papel=(252, 226, 190))
        rot_(lz, "ESO ES COMODIDAD", W * 0.72, H * 0.29, 46, t, G_comodidad)


IG6 = PF.Plano("iglu_dentro_b", G_f[10] - 0.4, G_f[11], z0=1.04, z1=1.14, c0=(0.50, 0.56), c1=(0.56, 0.58), par=(26, 6))
snd(G_abuelos, "bling", 0.4)


@toma(G_f[10] - 0.4, ("latigo", 0.5))
def ig6(lz, t):
    IG6.fondo(lz, t)
    brillo_en(lz, IG6, t, 0.42, 0.55, 140, color=(1.0, 0.60, 0.25), inten=0.50, sem=63, chis=3)
    quieto(lz, IG6, t, "gente_hoja/00", 0.62, 0.94, 0.46, tono=CALIDO, flip=True)
    quieto(lz, IG6, t, "gente_hoja/01", 0.80, 0.95, 0.30, tono=CALIDO, fase=1.0, flip=True)
    quieto(lz, IG6, t, "inuit_hoja/04", 0.24, 0.94, 0.44, tono=CALIDO, fase=2.0)
    rot_(lz, "NADIE ESTUDIÓ FÍSICA", W * 0.50, H * 0.13, 54, t, G_fisica)
    rot_(lz, "DE ABUELOS A NIETOS", W * 0.50, H * 0.26, 50, t, G_abuelos, rot=2)


IG7 = PF.Plano("sala_moderna_b", G_f[11] - 0.4, F(TU, 0), z0=1.04, z1=1.14, c0=(0.50, 0.58), c1=(0.44, 0.60), par=(26, 6))
snd(G_paredes, "pop", 0.4)
snd(G_poco, "pop", 0.4, tono=1.1)
snd(G_centro, "pop", 0.4, tono=0.9)


@toma(G_f[11] - 0.4, ("destello", 0.8))
def ig7(lz, t):
    IG7.fondo(lz, t)
    brillo_en(lz, IG7, t, 0.85, 0.40, 140, color=(1.0, 0.75, 0.40), inten=0.30, sem=64)
    brillo_en(lz, IG7, t, 0.15, 0.58, 220, color=(1.0, 0.55, 0.25), inten=0.35 * smooth(prog(t, G_centro - 0.3, G_centro + 0.6)), sem=65)
    quieto(lz, IG7, t, "sapi_hoja/01", 0.34, 0.97, 0.54, tono=CALIDO)
    rot_(lz, "LA IDEA DE TU CASA", W * 0.50, H * 0.13, 56, t, G_casa - 0.3)
    rot_(lz, "PAREDES QUE AÍSLAN", W * 0.80, H * 0.62, 40, t, G_paredes, rot=2)
    rot_(lz, "POCO AIRE FRÍO", W * 0.80, H * 0.74, 40, t, G_poco, rot=-2)
    rot_(lz, "CALOR EN EL CENTRO", W * 0.80, H * 0.86, 40, t, G_centro, rot=2)


# ================================================================== TÚ (642,7 - 688)
U_f = [F(TU, i) for i in range(9)]
U_ropa, U_aguja = T(TU, "ropa", 1), T(TU, "aguja", 1)
U_colchon, U_cama = T(TU, "colchón", 2), T(TU, "cama", 2)
U_calef, U_fogata = T(TU, "calefacción", 3), T(TU, "fogata", 3)
U_intentes, U_dedos = T(TU, "intentes", 4), T(TU, "dedos", 4)
U_refugio, U_mojada, U_dormido = T(TU, "refugio", 5), T(TU, "mojada", 5), T(TU, "dormido", 5)
U_emerg = T(TU, "emergencias", 6)
U_compartian = T(TU, "compartían", 7)
U_lampara, U_aguja2, U_tunel, U_ensena = T(TU, "lámpara", 8), T(TU, "aguja", 8), T(TU, "túnel", 8), T(TU, "enseña", 8)

TU1 = PF.Plano("casa_moderna_dia", U_f[0] - 0.4, U_f[2], z0=1.04, z1=1.14, c0=(0.50, 0.58), c1=(0.44, 0.60), par=(26, 6))
snd(U_f[0], "papel", 0.5)
snd(U_ropa, "pop", 0.5)
snd(U_aguja, "pop", 0.5, tono=1.2)


@toma(U_f[0] - 0.4, ("destello", 0.8))
def tu1(lz, t):
    TU1.fondo(lz, t)
    brillo_en(lz, TU1, t, 0.88, 0.62, 160, color=(1.0, 0.60, 0.30), inten=0.25, sem=66)
    quieto(lz, TU1, t, "sapi_hoja/01", 0.22, 0.96, 0.56, tono=DIA)
    rot_(lz, "¿QUÉ TIENES TÚ DE ELLOS?", W * 0.50, H * 0.13, 60, t, U_f[0], U_ropa - 0.3)
    pega(lz, "moderno_hoja/05", W * 0.52, H * 0.46, H * 0.24, t, U_ropa)
    rot_(lz, "=", W * 0.66, H * 0.46, 110, t, U_aguja - 0.2, rot=0)
    pega(lz, "utileria_ropa/00", W * 0.82, H * 0.46, H * 0.18, t, U_aguja, rot=-10)
    rot_(lz, "TU ROPA CON COSTURAS", W * 0.66, H * 0.74, 46, t, U_ropa + 0.2)


TU2 = PF.Plano("casa_moderna_dia_b", U_f[2] - 0.4, U_f[4], z0=1.04, z1=1.14, c0=(0.50, 0.58), c1=(0.56, 0.60), par=(26, 6))
snd(U_colchon, "pop", 0.5)
snd(U_cama, "pop", 0.5, tono=1.2)
snd(U_calef, "pop", 0.5, tono=0.9)
snd(U_fogata, "fuego", 0.5, dur=3.0)


@toma(U_f[2] - 0.4, ("latigo", 0.5))
def tu2(lz, t):
    TU2.fondo(lz, t)
    desenfoca(lz, 3)
    oscurece(lz, 0.35)
    sale = U_calef - 0.4
    pega(lz, "moderno_hoja/02", W * 0.30, H * 0.40, H * 0.24, t, U_colchon, sale)
    rot_(lz, "=", W * 0.50, H * 0.40, 110, t, U_cama - 0.2, sale, rot=0)
    pega(lz, "utileria_fuego/08", W * 0.70, H * 0.40, H * 0.22, t, U_cama, sale)
    pega(lz, "moderno_hoja/01", W * 0.30, H * 0.48, H * 0.30, t, U_calef)
    rot_(lz, "=", W * 0.50, H * 0.48, 110, t, U_fogata - 0.2, rot=0)
    pega(lz, "utileria_fuego/01", W * 0.70, H * 0.48, H * 0.30, t, U_fogata)
    if t > U_fogata:
        PF.brillo(lz, W * 0.70, H * 0.46, 300, color=(1.0, 0.55, 0.22), inten=0.40 * PF.entra(t, U_fogata, 0.6), t=t)
    rot_(lz, "ALGUIEN LA MANTUVO ENCENDIDA TODA LA NOCHE", W * 0.50, H * 0.84, 42, t, U_fogata + 0.6)


TU3 = PF.Plano("calle_helada", U_f[4] - 0.4, U_f[7], z0=1.04, z1=1.16, c0=(0.50, 0.56), c1=(0.56, 0.60), par=(30, 8))
snd(U_f[4], "viento", 0.6, dur=16.0)
snd(U_intentes, "error", 0.5)
snd(U_emerg, "ding", 0.5)


@toma(U_f[4] - 0.4, ("fundido", 0.6))
def tu3(lz, t):
    TU3.fondo(lz, t)
    nieve(lz, t, n=110, viento=0.8, op=0.65, sem=66)
    dx, rr = tirita(t, 0.6)
    X, Y, h = TU3.en(t, 0.22, 0.97, 0.52)
    PF.actor(lz, "sapi_hoja/03", X + dx, Y, h, rot=rr, tono=NOCHE, sy=PF.respira(t))
    aliento(lz, X + 0.10 * h, Y - 0.80 * h, 0.2 * h, t, U_f[4])
    rot_(lz, "NO LO INTENTES", W * 0.60, H * 0.13, 64, t, U_intentes, U_refugio - 0.4)
    rot_(lz, "BUSCA REFUGIO", W * 0.66, H * 0.30, 50, t, U_refugio, rot=-2)
    rot_(lz, "QUÍTATE LA ROPA MOJADA", W * 0.66, H * 0.44, 50, t, U_mojada, rot=2)
    rot_(lz, "NO TE DUERMAS A LA INTEMPERIE", W * 0.66, H * 0.58, 50, t, U_dormido, rot=-1)
    if t > U_emerg - 0.6:
        oscurece(lz, 0.35 * smooth(prog(t, U_emerg - 0.6, U_emerg)))
        pega(lz, "moderno_hoja/04", W * 0.60, H * 0.50, H * 0.40, t, U_emerg - 0.4)
        rot_(lz, "LLAMA A EMERGENCIAS", W * 0.60, H * 0.82, 60, t, U_emerg)


TU4 = PF.Plano("campamento_sol_b", U_f[7] - 0.4, F(OU, 0), z0=1.04, z1=1.16, c0=(0.50, 0.58), c1=(0.50, 0.62), par=(28, 6))
snd(U_f[7], "fuego", 0.4, dur=11.0)
snd(U_lampara, "pop", 0.5)
snd(U_aguja2, "pop", 0.5, tono=1.1)
snd(U_tunel, "pop", 0.5, tono=0.9)


@toma(U_f[7] - 0.4, ("desenfoque", 0.6))
def tu4(lz, t):
    TU4.fondo(lz, t)
    brillo_en(lz, TU4, t, 0.50, 0.60, 140, color=(1.0, 0.55, 0.22), inten=0.45, sem=67, chis=5)
    quieto(lz, TU4, t, "gente_hoja/00", 0.20, 0.92, 0.40, tono=DIA)
    quieto(lz, TU4, t, "cazadora_hoja/05", 0.38, 0.96, 0.44, tono=DIA, fase=0.7)
    quieto(lz, TU4, t, "gente_hoja/01", 0.62, 0.95, 0.28, tono=DIA, flip=True, fase=1.4)
    quieto(lz, TU4, t, "gente_hoja/03", 0.80, 0.93, 0.40, tono=DIA, flip=True, fase=2.1)
    rot_(lz, "COMPARTÍAN LO QUE SABÍAN", W * 0.50, H * 0.13, 58, t, U_compartian - 0.4)
    pega(lz, "iglu_utileria/04", W * 0.28, H * 0.36, H * 0.16, t, U_lampara)
    pega(lz, "utileria_ropa/00", W * 0.50, H * 0.34, H * 0.12, t, U_aguja2, rot=-15)
    pega(lz, "iglu_utileria/02", W * 0.72, H * 0.36, H * 0.16, t, U_tunel)
    rot_(lz, "SI NADIE TE ENSEÑA...", W * 0.50, H * 0.52, 46, t, U_ensena - 0.3)


# ================================================================== OUTRO (688 - 711,3)
O_f = [F(OU, i) for i in range(5)]
O_chamarra, O_aguja, O_casa, O_cazador = T(OU, "chamarra", 0), T(OU, "aguja", 1), T(OU, "casa", 1), T(OU, "cazador", 1)
O_primero, O_cadena = T(OU, "primero", 2), T(OU, "cadena", 3)
O_sapiens, O_wifi = T(OU, "sapiens", 4), T(OU, "wifi", 4)

OU1 = PF.Plano("ventana_nieve", O_f[0] - 0.4, O_f[2], z0=1.04, z1=1.16, c0=(0.50, 0.55), c1=(0.50, 0.50), par=(26, 6))
snd(O_chamarra, "pop", 0.6)
snd(O_aguja, "pop", 0.5)
snd(O_casa, "pop", 0.5, tono=0.9)
snd(O_cazador, "pop", 0.5, tono=1.1)


@toma(O_f[0] - 0.4, ("fundido", 0.7))
def ou1(lz, t):
    OU1.fondo(lz, t)
    brillo_en(lz, OU1, t, 0.85, 0.45, 160, color=(1.0, 0.75, 0.40), inten=0.30, sem=70)
    nieve(lz, t, n=50, viento=0.1, op=0.30, sem=70)
    pega(lz, "moderno_hoja/00", W * 0.50, H * 0.52, H * 0.40, t, O_chamarra, O_aguja - 0.3)
    pega(lz, "utileria_ropa/00", W * 0.22, H * 0.46, H * 0.14, t, O_aguja, rot=-15)
    pega(lz, "huesos_mamut/00", W * 0.50, H * 0.46, H * 0.28, t, O_casa)
    pega(lz, "inuit_hoja/02", W * 0.78, H * 0.48, H * 0.26, t, O_cazador)
    rot_(lz, "DETRÁS DE TU CHAMARRA", W * 0.50, H * 0.13, 54, t, O_aguja - 0.6)


OU2 = PF.Plano("puente_bering", O_f[2] - 0.4, TOTAL, z0=1.04, z1=1.14, c0=(0.48, 0.56), c1=(0.54, 0.56), par=(30, 8))
snd(O_f[2], "pasos", 0.5, dur=4.0)
snd(O_sapiens, "bling", 0.6)
snd(O_wifi, "ding", 0.7)


@toma(O_f[2] - 0.4, ("destello", 0.8))
def ou2(lz, t):
    OU2.fondo(lz, t)
    brillo_en(lz, OU2, t, 0.47, 0.72, 120, color=(1.0, 0.55, 0.22), inten=0.45, sem=71, chis=5)
    ta, tb = O_f[2] - 0.4, TOTAL
    anda(lz, OU2, t, "mamut_camina", ta, tb, 0.50, 0.80, 0.58, 0.10, paso=1.4, tono=OCASO, desde_antes=True)
    anda(lz, OU2, t, "cazador_corre", ta, tb, 0.02, 0.40, 0.80, 0.26, paso=1.6, tono=OCASO, desde_antes=True)
    anda(lz, OU2, t, "cazadora_camina", ta, tb, 0.14, 0.52, 0.84, 0.30, tono=OCASO, desde_antes=True)
    anda(lz, OU2, t, "sapi_camina", ta, O_sapiens - 0.3, 0.30, 0.56, 0.95, 0.40, tono=OCASO, desde_antes=True, hasta_despues=False)
    if t > O_sapiens - 0.3:
        k = PF.entra(t, O_sapiens - 0.3, 0.5)
        X, Y, h = OU2.en(t, 0.56, 0.95, 0.54)
        PF.actor(lz, "sapi_hoja/00", X, Y, h * (0.8 + 0.2 * k), tono=OCASO, sy=PF.respira(t))
        if t > O_wifi - 0.2:                               # la diadema de wifi se enciende
            kw = smooth(prog(t, O_wifi - 0.2, O_wifi + 0.4))
            PF.brillo(lz, X, Y - 0.86 * h, 0.35 * h, color=(0.55, 0.85, 1.0), inten=0.6 * kw, t=t)
    rot_(lz, "NO ERES EL PRIMERO", W * 0.50, H * 0.13, 60, t, O_primero - 0.5, O_cadena - 0.3)
    rot_(lz, "UNA LARGA CADENA", W * 0.50, H * 0.13, 60, t, O_cadena - 0.2, O_sapiens - 0.4)
    rot_(lz, "HOMO SAPIENS", W * 0.50, H * 0.13, 84, t, O_sapiens)
    rot_(lz, "...CON WIFI", W * 0.66, H * 0.27, 70, t, O_wifi, rot=3)


# ------------------------------------------------------------------ composición
def _cuadro(d, t):
    lz = np.zeros((H, W, 3), np.float32)
    d["dib"](lz, t)
    return lz


def render_mundo(t):
    i = 0
    for k, d in enumerate(TOMAS):
        if d["t0"] <= t:
            i = k
    d = TOMAS[i]
    img = _cuadro(d, t)
    tipo, dur = d["ent"]
    if i > 0 and t < d["t0"] + dur and tipo != "corte":
        img = D.mezcla_tomas(_cuadro(TOMAS[i - 1], t), img, (t - d["t0"]) / dur, tipo)
    img = PF.acabado(img, t, vineta=0.40, calido=0.0)
    img = img * smooth(prog(t, 0.0, 0.8)) * (1.0 - smooth(prog(t, TOTAL - 1.4, TOTAL - 0.1)))
    return np.clip(img, 0, 1).astype(np.float32)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            for t, n, v, kw in SFX:
                self.ev(t, n, v, **kw)

    def render(self, lz, t):
        return render_mundo(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
