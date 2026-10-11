# -*- coding: utf-8 -*-
"""Prueba de 30 s del estilo NOIR FEUDAL (noir a color en época medieval; kit nucleo/noir_color.py + nucleo/noir_feudal.py,
doc docs/estilo_noir_color.md § «Variante FEUDAL»). Tres planos encadenados con mancha de tinta, sin voz:
A la villa amurallada de noche (castillo bajo la luna, casas de entramado, antorcha, estandarte; el pesquisidor llega con su
farol y lo alza hacia el bando), B la cámara de la torre (ventana ojival con luna, tapiz, antorcha, busto encapuchado con vaho),
C la mesa (pergamino que se escribe solo, copa volcada, frasco de veneno, daga, vela y sello de lacre; relámpago y tinta).

    python videos/prueba_noir_feudal/prueba.py hoja 2 5 9 13 17 22 26 28     -> previews/hoja.jpg (+ PNG completos)
    python videos/prueba_noir_feudal/prueba.py paletas 9                       -> previews/paletas_9.jpg (antorcha · pergamino)
    python videos/prueba_noir_feudal/prueba.py video [--procs 6] [--paleta antorcha]
"""
import math
import os
import subprocess
import sys
import time
import wave

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.join(AQUI, "..", "..", "nucleo")
sys.path[:0] = [AQUI, NUCLEO]
os.chdir(AQUI)

import cv2
import numpy as np

import mundos_fe as MU
import noir as N
import noir_color as NC
import noir_feudal as NF
from motor import FPS, H, W, clamp01, smooth
from noir_pers import Detective, avance_paso
from toon import Pista, blob, elipse_, suave, tubo

FFMPEG = "C:/ffmpeg/bin/ffmpeg.exe"
DUR = 30.0
T_B, T_C = 10.6, 20.2
TR = 0.75
PALETA = os.environ.get("NC_PALETA", "antorcha")

_H = None


def lienzo():
    global _H
    if _H is None:
        _H = NC.NoirColor(PALETA)
    return _H


def rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float)


def rot(P, a, c):
    P = np.asarray(P, float).reshape(-1, 2) - c
    ca, sa = math.cos(a), math.sin(a)
    return np.stack([P[:, 0] * ca - P[:, 1] * sa, P[:, 0] * sa + P[:, 1] * ca], 1) + c


def a_pantalla(h, P, prof):
    M = h.matriz_capa(prof)
    return np.asarray(P, float) @ M[:2, :2].T + M[:2, 2]


def reflejar(h, t, y_mundo, k=0.32):
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


# ====================================================================== plano A: la villa amurallada
CAM_A = Pista([(0.0, (860.0, -1150.0, 1.0)), (1.2, (870.0, -1080.0, 1.0), "io"), (5.2, (900.0, 600.0, 1.0), "io"),
               (8.0, (1010.0, 610.0, 1.05), "io"), (T_B + 0.8, (1110.0, 560.0, 1.2), "io")])
PESQ_X = Pista([(0.0, 120.0), (1.6, 120.0), (7.4, 1080.0, "io"), (30.0, 1080.0)])
ALZA_A = Pista([(0.0, 0.0), (8.0, 0.0), (8.9, 0.85, "io"), (30.0, 0.85)])
MIRA_A = Pista([(0.0, 0.0), (8.2, 0.0), (9.0, 0.55, "io"), (30.0, 0.55)])
PESQ = NF.Pesquisidor(sem=3)


def pose_a(t):
    s = 0.95
    x = PESQ_X(t)
    dt = 1 / 60
    vel = abs(PESQ_X(t + dt) - PESQ_X(t - dt)) / (2 * dt)
    return dict(x=x, y=915.0, s=s, d=1, luz=(0.4, -1.0), rim=0.9, andar=clamp01(vel / 150.0),
                paso=(x - 120.0) / avance_paso(Detective.ZANCADA, s), alzar=float(ALZA_A(t)), arriba=float(MIRA_A(t)),
                viento=0.35 + 0.15 * math.sin(t * 1.7), hombros=0.2, capa=0.2 * math.sin(t * 1.1) ** 2)


def p_villa(h, t, u):
    pal = h.pal
    cx, cy, z = CAM_A(t)
    h.camara(z, cx, cy, 0.01 * math.sin(t * 0.4))
    h.rim_color(pal["luna"])
    NC.pegar(MU.cielo(), h, 0.05, rampa="cielo", dx=t * 5.0)
    NC.pegar(MU.castillo(), h, 0.3, rampa="muralla", bruma=0.26)
    NC.pegar(MU.villa(), h, 0.6, rampa="entramado", bruma=0.22)
    NC.pegar(MU.frente(), h, 1.0, rampa="entramado", emis=0.85)
    NC.pegar(MU.suelo(), h, 1.0, rampa="muralla")
    NF.estandarte(h, t, MU.ESTANDARTE_A[0], MU.ESTANDARTE_A[1], w=170, hh=380, sem=5, emblema="sol", viento=1.0)
    p = pose_a(t)
    PESQ.dibujar(h, p)
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.80
    h.luz_cono(560, -560, math.pi / 2 + 0.35, 0.9, 2600, pal["luna"], k=0.25, suave=0.8)          # luna de costado
    NF.antorcha(h, t, MU.ANTORCHA_A[0], MU.ANTORCHA_A[1], s=0.9, sem=7, luz=1.1, alcance=600)
    reflejar(h, t, MU.Y_CALLE + 12)
    N.lluvia(h, t, n=520, vel=1300.0)
    y0 = h.tf(np.array([[0, MU.Y_CALLE]]))[0][1]
    y1 = h.tf(np.array([[0, 1400]]))[0][1]
    if y1 > 0 and y0 < H:
        N.salpicaduras(h, t, max(0, y0), min(H, y1), n=60)
    return h.acabado(t, niebla=dict(dens=0.3, y0=0, y1=H, sem=1), flash=N.relampago(t, [0.6]))


# ====================================================================== plano B: la cámara de la torre
BUSTO = NF.BustoEncapuchado(sem=5)
BB = dict(arriba=Pista([(0, 0.0), (4.6, 0.0), (5.6, 0.6, "io"), (8.2, 0.6), (9.4, 0.15, "io")]),
          boca=Pista([(0, 0.0), (1.4, 0.0), (1.7, 0.35, "o"), (2.6, 0.2), (3.0, 0.0, "io")]))


def p_camara(h, t, u):
    pal = h.pal
    k = smooth(clamp01(u / 9.6))
    h.camara(1.02 + 0.07 * k, 940 + 40 * k, 545 - 10 * k, -0.006)
    h.rim_color(pal["luna"])
    NC.pegar(MU.exterior(), h, 0.15, rampa="muralla", bruma=0.25)
    x0, y0, x1, y1 = MU.VENT
    cv = a_pantalla(h, [(x0, y0), (x1, y1)], 0.5)
    caja = (int(cv[0, 0]), int(cv[0, 1]), int(cv[1, 0]), int(cv[1, 1]))
    N.lluvia(h, t, n=360, caja=caja, k=0.8, vel=1200.0)
    NC.pegar(MU.camara(), h, 0.5, rampa="muralla")
    NC.pegar(MU.ventanal(), h, 0.5, rampa="hierro")
    with h.capa(0.5):
        NF.estandarte(h, t, 120, 40, w=300, hh=640, sem=9, emblema="luna", viento=0.12)          # tapiz de la casa
        NF.antorcha(h, t, 1030, 300, s=0.9, sem=11, luz=0.8, alcance=560)
    p = dict(x=690.0, y=440.0, s=1.0, d=1, luz=(0.85, -0.5), rim=0.95, arriba=float(BB["arriba"](u)), boca=float(BB["boca"](u)))
    BUSTO.dibujar(h, p)
    NF.vela(h, t, 1420, 1090, s=1.3, sem=21, alto=170, luz=0.8, alcance=520)
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.30
    Q = [(180, 60), (1190, 120), (1190, 880), (120, 1060)]                        # la luna atraviesa la vidriera
    h.luz_persiana(Q, k=1.05, tipo="ventana", col=pal["luna"])
    h.luz_radial(1500, 330, 900, pal["luna"], k=0.45)
    b = BUSTO.boca(p)
    NF.vaho(h, t, b[0] + 12, b[1] + 6, ciclo=3.6, fase=0.4, k=1.1, sem=3)
    N.motas(h, t, n=70, k=0.5)
    return h.acabado(t, niebla=dict(dens=0.14, y0=0, y1=H, sem=2, vel=12.0))


# ====================================================================== plano C: la mesa del pesquisidor
LINEAS = [("Pesquisa VII", 66, 0.3, NF.FUENTE_GOTICA), ("Asunto: la muerte del rey", 30, 1.5, NF.FUENTE_PLUMA_R),
          ("Lugar: el gran salón, al alba", 30, 2.6, NF.FUENTE_PLUMA_R), ("Testigos: tres. Mienten dos.", 30, 3.7, NF.FUENTE_PLUMA_R),
          ("Arma: veneno en la copa", 30, 4.6, NF.FUENTE_PLUMA_R)]
CPS = 18.0
T_SELLO = T_C + 6.0
T_RAYO = T_C + 7.75
T_TINTA = DUR - 0.8


def hoja_T(cx, cy, ang, s=1.0):
    c = np.array([cx, cy], float)
    return lambda P: rot(np.asarray(P, float).reshape(-1, 2) * s + c, ang, c)


def pluma(h, x, y, ang, sem=0):
    """Pluma de ave para escribir (x, y = punta)."""
    c = np.array([x, y], float)
    eje = rot(np.array([[0, 0], [380, 0]], float) + c, ang, c)
    bar = []
    for v in np.linspace(0.25, 1.0, 14):
        a = 34 * math.sin(math.pi * (v - 0.25) / 0.75) ** 0.7
        bar.append((v * 380, -a))
    bar += [(v * 380, a * 0.75) for v, a in [((p[0] / 380), -p[1]) for p in bar[::-1]]]
    with h.con_rampa("pergamino"):
        h.pieza(rot(np.array(bar) + c, ang, c), 205, sem, w=3, d=10, trama=0.3, rim=0.8)
    for j in range(16):
        v = 0.3 + j * 0.043
        q0 = rot(np.array([[v * 380, 0]]) + c, ang, c)[0]
        q1 = rot(np.array([[v * 380 + 26, -30 * math.sin(math.pi * v)]]) + c, ang, c)[0]
        h.trazo(np.array([q0, q1]), 1.2, sem + j, color=(90, 80, 70), alfa=0.6, tf=True)
    h.trazo(eje, 3.5, sem + 30, color=(60, 50, 40))
    with h.con_rampa("hierro"):
        h.pieza(rot(np.array([[-6, -4], [40, -6], [40, 6], [-6, 4], [-14, 0]], float) + c, ang, c), 40, sem + 31, w=2, d=2,
                sombra=0, trama=0, rim=0.8)


def p_mesa(h, t, u):
    pal = h.pal
    k = smooth(clamp01(u / 9.8))
    h.camara(1.0 + 0.12 * k, 930 - 40 * k, 560 - 30 * k, -0.025 + 0.035 * k)
    h.rim_color(pal["vela"])
    NC.pegar(MU.mesa(), h, 1.0, rampa="entramado")
    # el pergamino desenrollado con sus dos rollos
    Th = hoja_T(860, 560, 0.03)
    with h.con_rampa("pergamino"):
        h.pieza(Th([(-350, -390), (350, -400), (346, 400), (-340, 410)]), 205, 10, w=4, luz=(0.2, -1), d=12, trama=0.2, rim=0.2)
        for yy, sg in ((-410, 1), (420, -1)):
            h.pieza(Th(rect(-372, yy - 26, 744, 52)), 175, 11 + sg, w=4, d=16, trama=0.5, rim=0.8)
            h.pieza(Th(rect(-372, yy - 26 + 30 * (sg < 0), 744, 12)), 120, 13 + sg, w=0, d=0, sombra=0, rim=0, alfa=0.7)
            for xx in (-380, 380):
                h.pieza(Th(elipse_(xx, yy, 12, 28, n=16)), 150, 15 + sg, w=3, d=4, trama=0, rim=0.6)
    N.soporte(h, 860, 560, 700, 780, 0.03, 1.0)
    for i, (s, px, t0, fu) in enumerate(LINEAS):
        P = Th([(0 if i == 0 else -290, -330 + (0 if i == 0 else 50) + i * 64)])[0]
        N.texto_maquina(h, s, P[0], P[1], px, t, T_C + t0, cps=CPS, tono=np.array(pal["tinta"]) * 2.0, fuente=fu, track=1.0,
                        centro=(i == 0))
    with h.con_rampa("pergamino"):                                                # adorno y renglones ya escritos
        for i in range(4):
            L = 520 * (0.6 + 0.4 * abs(math.sin(i * 2.3)))
            h.pieza(Th(rect(-290, 40 + i * 44, L, 6)), 110, 40 + i, w=0, d=0, sombra=0, rim=0, alfa=0.5)
    # tintero de hierro y la pluma
    with h.con_rampa("hierro"):
        h.pieza(elipse_(1340, 300, 76, 70, n=36), 70, 20, w=5, d=12, trama=0.4, rim=0.8)
        h.pieza(elipse_(1340, 300, 38, 36, n=24), 12, 21, w=3, d=0, sombra=0, rim=0)
    pluma(h, 1330, 296, -0.75, sem=22)
    # copa volcada, vino derramado y el frasco del veneno
    with h.con_rampa("vino"):
        h.pieza(suave([(1360, 640), (1470, 600), (1620, 640), (1700, 720), (1640, 800), (1500, 790), (1400, 740)], 4), 70, 30, w=0,
                d=0, sombra=0, rim=0, alfa=0.85)
    with h.con_rampa("oro"):
        c = np.array([1520.0, 690.0])
        h.pieza(rot(np.array([[-110, -54], [40, -40], [40, 40], [-110, 54]]) + c, 0.35, c), 130, 31, w=4, d=12, trama=0.3, rim=0.9)
        h.pieza(rot(elipse_(-110, 0, 18, 56, n=24) + c, 0.35, c), 60, 32, w=3, d=0, sombra=0, rim=0.5)
        h.pieza(rot(tubo(np.array([[40.0, 0.0], [120.0, 0.0]]), 18, 14) + c, 0.35, c), 140, 33, w=3, d=6, trama=0, rim=0.9)
        h.pieza(rot(elipse_(128, 0, 14, 52, n=20) + c, 0.35, c), 150, 34, w=3, d=4, trama=0, rim=0.9)
    with h.con_rampa("vidrio_verde"):
        h.pieza(elipse_(1660, 980, 46, 46, n=28), 120, 35, w=4, d=10, trama=0, rim=0.9)
        h.pieza(rect(1648, 900, 24, 44), 100, 36, w=3, d=4, trama=0, rim=0.8)
        h.pieza(elipse_(1648, 965, 14, 10, n=12), 240, 37, w=0, d=0, sombra=0, rim=0, alfa=0.8)
    with h.con_rampa("cuero"):
        h.pieza(rect(1650, 880, 20, 22), 90, 38, w=2, d=2, trama=0, rim=0.6)
    # la daga como prueba
    c = np.array([1180.0, 960.0])
    with h.con_rampa("hierro"):
        h.pieza(rot(np.array([[0, -16], [300, -6], [340, 0], [300, 6], [0, 16]], float) + c, -0.18, c), 170, 40, w=3, d=6, trama=0,
                rim=1.0)
        h.trazo(rot(np.array([[10, 0], [290, 0]], float) + c, -0.18, c), 2.0, 41, color=(40, 44, 50), alfa=0.6)
    with h.con_rampa("oro"):
        h.pieza(rot(rect(-14, -54, 24, 108) + c, -0.18, c), 150, 42, w=3, d=4, trama=0, rim=0.9)
    with h.con_rampa("cuero"):
        h.pieza(rot(tubo(np.array([[-14.0, 0.0], [-130.0, 0.0]]), 26, 24) + c, -0.18, c), 70, 43, w=3, d=6, trama=0.4, rim=0.7)
    with h.con_rampa("oro"):
        h.pieza(rot(elipse_(-140, 0, 20, 20, n=16) + c, -0.18, c), 150, 44, w=3, d=4, trama=0, rim=0.9)
    # la vela (arriba a la izquierda) y su charco de luz
    NF.vela(h, t, 300, 560, s=1.0, sem=50, alto=160, luz=1.2, alcance=1250)
    NF.vela(h, t, 1700, 470, s=0.85, sem=51, alto=90, luz=0.9, alcance=900)
    # sello de lacre sobre el pergamino
    P = Th([(170, 250)])[0]
    NF.lacre(h, t, T_SELLO, P[0], P[1], r=92, sem=60, emblema="sol")
    fl = N.relampago(t, [T_RAYO])
    h.ambiente[:] = np.array(pal["luna"], np.float32) * 0.30
    h.luz_radial(2150, 250, 900, pal["luna"], k=0.35)
    if fl > 0:
        h.luz_persiana([(1900, -200), (2300, 400), (600, 1500), (-200, 900)], k=2.4 * fl, tipo="ventana", col=pal["relampago"])
    N.motas(h, t, n=80, k=0.5)
    img = h.acabado(t, flash=0.35 * fl)
    if t >= T_TINTA:
        img = N.tinta_cubre(img, (t - T_TINTA) / (DUR - T_TINTA) * 1.05, sem=5, tono=np.array(pal["tinta"]))
    return img


# ====================================================================== montaje
PLANOS = [(0.0, p_villa), (T_B, p_camara), (T_C, p_mesa)]


def _r(i, t):
    h = lienzo()
    h.nuevo(t, None)
    t0, fn = PLANOS[i]
    return fn(h, t, t - t0)


def cuadro(t):
    i = max(k for k, (t0, _) in enumerate(PLANOS) if t0 <= t)
    img = _r(i, t)
    if i > 0 and t < PLANOS[i][0] + TR:
        prev = _r(i - 1, t)
        img = N.transicion(prev, img, (t - PLANOS[i][0]) / TR, "tinta", sem=i * 3)
    return np.clip(img, 0, 1)


def a_u8(img):
    return (np.clip(img, 0, 1) * 255 + 0.5).astype(np.uint8)


# ====================================================================== sonido (sintetizado, nucleo/sfx_noir.py)
def audio(ruta):
    import sfx_noir as S
    from sinte import SR
    n = int(DUR * SR)
    mix = np.zeros((2, n))

    def mete(x, t0, g):
        x = np.asarray(x, float)
        if x.ndim == 1:
            x = np.stack([x, x])
        i = int(t0 * SR)
        m = min(x.shape[1], n - i)
        if m > 0:
            mix[:, i:i + m] += x[:, :m] * g

    mete(S.s_lluvia_amb(T_B + 0.6), 0.0, 0.36)
    mete(S.s_grave_inquietante(5.0), 0.0, 0.25)
    mete(S.s_trueno_lejano(4.0), 0.6, 0.5)
    mete(S.s_chisporroteo(), 0.2, 0.0)
    mete(S.s_lampara_chisporrotea(T_B), 0.0, 0.10)
    mete(S.s_pasos_mojados(5.8), 1.7, 0.42)
    mete(S.s_lluvia_lejana(T_C - T_B + 0.6), T_B - 0.2, 0.36)
    mete(S.s_lampara_chisporrotea(T_C - T_B), T_B, 0.14)
    mete(S.s_exhala(), T_B + 1.4, 0.4)
    mete(S.s_lluvia_lejana(DUR - T_C), T_C - 0.2, 0.22)
    for s, px, t0, fu in LINEAS:
        mete(S.s_lapiz(len(s) / CPS), T_C + t0, 0.45)
    mete(S.s_sello_golpe(), T_SELLO, 0.7)
    mete(S.s_sombra_crece(2.5), T_SELLO + 0.3, 0.25)
    mete(S.s_trueno_noir(4.0), T_RAYO, 0.75)
    for tt in (T_B - 0.35, T_C - 0.35, T_TINTA):
        mete(S.s_tinta_mancha(0.8), tt, 0.35)
    f = np.ones(n)
    f[-int(0.6 * SR):] = np.linspace(1, 0, int(0.6 * SR))
    mix *= f
    mix *= 0.85 / (np.abs(mix).max() + 1e-9)
    pcm = (mix.T * 32767).astype(np.int16)
    with wave.open(ruta, "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(pcm.tobytes())


# ====================================================================== render
def _trozo(args):
    i, f0, f1, paleta = args
    global PALETA
    PALETA = paleta
    ruta = os.path.join(AQUI, "segmentos", f"seg_{paleta}_{i:03d}.mp4")
    cmd = [FFMPEG, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", ruta]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for f in range(f0, f1):
        pr.stdin.write(a_u8(cuadro(f / FPS)).tobytes())
    pr.stdin.close()
    pr.wait()
    return ruta


def video(procs, paleta):
    from multiprocessing import Pool
    nf = int(DUR * FPS)
    trozos = [(k, f, min(nf, f + 30), paleta) for k, f in enumerate(range(0, nf, 30))]
    t0 = time.time()
    with Pool(procs) as pool:
        rutas = []
        for r in pool.imap(_trozo, trozos):
            rutas.append(r)
            print(f"  {len(rutas)}/{len(trozos)} trozos ({time.time() - t0:.0f} s)", flush=True)
    lista = os.path.join(AQUI, "segmentos", f"lista_{paleta}.txt")
    with open(lista, "w", encoding="utf-8") as fh:
        for r in rutas:
            fh.write(f"file '{r.replace(os.sep, '/')}'\n")
    wav = os.path.join(AQUI, "segmentos", "audio.wav")
    audio(wav)
    out = os.path.join(AQUI, "salida", f"prueba_noir_feudal_{paleta}.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-i", wav, "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out], check=True)
    print(f"-> {out}  ({time.time() - t0:.0f} s)")


def hoja(tiempos, nombre="hoja"):
    tiles = []
    for t in tiempos:
        t1 = time.time()
        im = a_u8(cuadro(t))
        dt = time.time() - t1
        cv2.imwrite(os.path.join("previews", f"f_{PALETA}_{t:05.2f}.png"), cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
        sm = cv2.resize(im, (640, 360), interpolation=cv2.INTER_AREA)
        for c, g in (((0, 0, 0), 3), ((255, 255, 255), 1)):
            cv2.putText(sm, f"t={t:.2f} {dt * 1000:.0f}ms", (6, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.5, c, g, cv2.LINE_AA)
        tiles.append(sm)
    while len(tiles) % 3:
        tiles.append(np.zeros_like(tiles[0]))
    img = np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, len(tiles), 3)])
    cv2.imwrite(os.path.join("previews", f"{nombre}.jpg"), cv2.cvtColor(img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print(f"{len(tiempos)} cuadros -> previews/{nombre}.jpg")


if __name__ == "__main__":
    a = sys.argv[1:]
    if "--paleta" in a:
        PALETA = a[a.index("--paleta") + 1]
    if a[0] == "hoja":
        hoja([float(x) for x in a[1:] if x.replace(".", "").isdigit()])
    elif a[0] == "paletas":
        t = float(a[1])
        tiles = []
        for pal in ("antorcha", "pergamino"):
            _H = None
            PALETA = pal
            im = a_u8(cuadro(t))
            sm = cv2.resize(im, (960, 540), interpolation=cv2.INTER_AREA)
            cv2.putText(sm, pal, (14, 40), cv2.FONT_HERSHEY_SIMPLEX, 1.1, (255, 255, 255), 2, cv2.LINE_AA)
            tiles.append(sm)
        cv2.imwrite(os.path.join("previews", f"paletas_{t:05.2f}.jpg"), cv2.cvtColor(np.hstack(tiles), cv2.COLOR_RGB2BGR),
                    [cv2.IMWRITE_JPEG_QUALITY, 90])
        print(f"-> previews/paletas_{t:05.2f}.jpg")
    elif a[0] == "video":
        procs = int(a[a.index("--procs") + 1]) if "--procs" in a else 6
        video(procs, PALETA)
