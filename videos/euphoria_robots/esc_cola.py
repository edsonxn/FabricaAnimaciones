# -*- coding: utf-8 -*-
"""Momentos del resto del video + PLAN anclado a la voz. Lo importa escenas.py al final (from esc_cola import *)."""
import json
import math
import os
import unicodedata

import numpy as np

import diseccion as D
import plano as PL
from motor import W, H, componer
from escenas import AQUI, SUELO, clip, m_equilibrio, m_error_vuela, m_gancho, m_musculos, m_verlet, pip, suelo, tarjeta


def _ok(v, a, b):
    return a if v < a else b if v > b else v


def m_teaser(lz, u, ctx):
    m_error_vuela(lz, u + 0.6, dict(ctx, teaser=True))


def _saluda(lz, u, x, s):
    P = D.escenario("leve").en(1.6).copy()
    P[D.MD] = P[D.PEC] + [14 + 4 * math.sin(u * 9), -18]
    D.muneco(lz, P, x, SUELO, s=s, t=u)


def m_presenta(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["pedido"])
    pip(lz, "choque", 2.0 + u, u, 0.0, cy=640, w=960, h=760)
    D.titular(lz, "SOY TOKEN", 1110, u, 0.2, px=110)
    D.kicker(lz, "LA IA DE ESTE TALLER", W / 2, 1205, u, 0.5, fondo=D.TURQ)
    suelo(lz)
    _saluda(lz, u, W / 2, 5.0)


_JEFE = {}


def m_pedido(lz, u, ctx):
    from jefe_canadiense import Jefe, amplitud
    if "j" not in _JEFE:
        _JEFE["j"] = Jefe(os.path.join(AQUI, "propios", "jefe_limpio.png"), boca_y=.523 / .75, bisagra_x=.33, frente_x=.57, corte=.75)
        wav = os.path.join(AQUI, "voz", "final", "pedido_1.wav")
        _JEFE["amp"] = amplitud(wav, fps=30) if os.path.exists(wav) else np.zeros(1)
    D.manchas(lz, u, D.TONOS["pedido"])
    t1 = ctx["k"]("pedido_1")
    texto = "que reaccionen a otros robots y cosas, y busquen balancearse cuando se mueven o son golpeados"
    n = int(len(texto) * D.pr(u, t1 - 0.2, t1 + 3.6))
    a = D.suave(D.pr(u, 0.1, 0.5))
    with lz.capa(2):
        lz.relleno(D.rrect(W / 2, 520, 900, 420, 40), (6, 4, 24), alfa=0.4 * a)
        lz.relleno(D.rrect(W / 2, 505, 900, 420, 40), D.PAPEL, alfa=a)
        lz.relleno(np.array([[W / 2 - 330, 712], [W / 2 - 250, 712], [W / 2 - 360, 790]]), D.PAPEL, alfa=a)
    PL.rotulo(lz, W / 2 - 400, 345, "MI JEFE ESCRIBIÓ:", px=34, color=D.LILA, sombra=0, ancla=(0, .5), alfa=a)
    lineas, ln = [], ""
    for p in texto[:n].split(" "):
        if len(ln) + len(p) > 26:
            lineas.append(ln)
            ln = p
        else:
            ln = (ln + " " + p).strip()
    lineas.append(ln + ("|" if (u * 2) % 1 < .5 else ""))
    for i, l in enumerate(lineas):
        PL.rotulo(lz, W / 2 - 400, 420 + i * 62, l, px=48, color=D.TINTA, sombra=0, ancla=(0, .5), alfa=a)
    i = int(_ok((u - t1) * 30, 0, len(_JEFE["amp"]) - 1))
    abre = float(_JEFE["amp"][i]) if u >= t1 else 0.0
    spr = _JEFE["j"].cuadro(abre, u, alto=880)
    rgba = np.dstack([spr[..., 2], spr[..., 1], spr[..., 0], spr[..., 3]]).astype(np.float32)
    rgba[..., :3] *= rgba[..., 3:] / 255
    brinco = 18 * abs(math.sin(u * 7)) if abre > .15 else 0
    lz.pegar(rgba.astype(np.uint8), W / 2 - 150, H + 40 - brinco, k=D.rebote(D.pr(u, t1 - 0.6, t1 - 0.1)), ancla=(.5, 1), capa=2)
    D.muneco(lz, D.escenario("leve").en(0.0), W - 200, 1720, s=4.6, t=u, capa=2)


def m_problema(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["problema"])
    t1, t2 = ctx["k"]("problema_1"), ctx["k"]("problema_2")
    if u < t1:
        D.titular(lz, "SIEMPRE IGUAL", 300, u, 0.1, px=110, col=D.CORAL)
        sim, cicl = D.escenario("fuerte"), (u * 1.1) % 1.6
        for i, x in enumerate((200, 540, 880)):
            k = D.rebote(D.pr(u, 0.3 + 0.5 * i, 0.7 + 0.5 * i))
            if k > 0.01:
                with lz.capa(1):
                    lz.relleno(D.rrect(x, 900, 300, 520, 30), (34, 26, 80), alfa=k)
                D.muneco(lz, sim.en(0.55 + cicl * 0.4), x - 40, 1080, s=3.0 * k, t=u)
                PL.pastilla(lz, x, 1210, f"repetición {i + 1}", px=26, k=k, fondo=D.PAPEL, color=D.TINTA)
        if u > 1.6:
            PL.rotulo(lz, W / 2, 1450, "FALSA", px=150, color=D.CORAL, k=D.rebote(D.pr(u, 1.6, 2.0)), rot=-0.12)
    elif u < t2:
        v = u - t1
        D.kicker(lz, "GTA IV · 2008", W / 2, 260, v, 0.0, fondo=D.AMAR)
        D.titular(lz, "EUPHORIA", 390, v, 0.6, px=150, col=D.AMAR)
        suelo(lz)
        for i, (n, x) in enumerate((("leve", 300), ("fuerte", 700))):
            D.muneco(lz, D.escenario(n).en((v * 0.8 + i) % 3.5), x, SUELO, s=7.0, rayos=0.45, t=v + i)
        PL.pastilla(lz, W / 2, 1720, "músculos simulados, no caídas dibujadas", px=34, fondo=D.PAPEL, color=D.TINTA, k=D.rebote(D.pr(v, 1.0, 1.4)))
    else:
        v = u - t2
        k = D.rebote(D.pr(v, 0.0, 0.5))
        with lz.capa(1), lz.grupo(W / 2, 900, k):
            lz.relleno(D.rrect(0, 20, 1000, 1160, 36), (6, 4, 24), alfa=0.45)
            lz.relleno(D.rrect(0, 0, 1000, 1160, 36), (226, 228, 244))
            for i, c in enumerate((D.CORAL, D.AMAR, D.VERDE)):
                lz.relleno(D.circulo(-440 + i * 40, -540, 12), c)
            lz.relleno(D.rrect(80, -540, 700, 46, 23), (250, 250, 255))
            lz.texto("robotaller", 80, -538, 28, "geo", color=(90, 90, 120), borde=None, temblor=0.0)
        if k > 0.3:
            D.monitor(lz, clip("caida", 2.0 + v), W / 2, 960, 960, 1020, v, etiqueta="UNA PÁGINA WEB", k=k, borde=(200, 204, 230))
        D.titular(lz, "EN UNA WEB", 230, v, 0.3, px=100)


def m_agarre(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["equilibrio"])
    D.titular(lz, "¡AGÁRRATE!", 330, u, 0.1, px=120, col=D.AMAR)
    pip(lz, "agarre", 3.5 + u, u, 0.0, cy=760, h=520)
    suelo(lz)
    D.muneco(lz, D.escenario("fuerte").en(min(u * 0.7, 1.4)), 150, SUELO, s=6.0, rayos=0.5, t=u, cara="x" if u > 0.8 else "normal")
    PL.pastilla(lz, W / 2, 1720, "manos al suelo · barandal · lámpara · otro robot", px=30, fondo=D.PAPEL, color=D.TINTA, k=D.rebote(D.pr(u, 0.6, 1.0)))


def m_mundo(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["mundo"])
    t1, t2 = ctx["k"]("mundo_1"), ctx["k"]("mundo_2")
    if u < t2:
        if u < t1 * 0.55:
            nom, seg, kick, tk = "mundo", 3.0 + u, "MESAS · TUBOS · LÁMPARAS", 0.2
        elif u < t1:
            nom, seg, kick, tk = "trampa", 3.0 + u - t1 * 0.55, "TRAMPILLA AL PISO DE ABAJO", t1 * 0.55
        else:
            nom, seg, kick, tk = "enemigo", 3.5 + u - t1, "ENEMIGO: PEGATINA CON ALAS", t1
        D.monitor(lz, clip(nom, seg), W / 2, 820, 1000, 1000, u, k=D.rebote(D.pr(u, 0, 0.4)))
        D.kicker(lz, kick, W / 2, 1420, u, tk, fondo=D.AMAR)
        D.titular(lz, "UN MUNDO", 210, u, 0.1, px=110)
    else:
        v = u - t2
        PL.rotulo(lz, W / 2, 640, "180", px=320, color=D.AMAR, k=D.rebote(D.pr(v, 0.0, 0.4)))
        PL.rotulo(lz, W / 2, 830, "VECES POR SEGUNDO", px=58, k=D.rebote(D.pr(v, 0.2, 0.6)))
        PL.rotulo(lz, W / 2, 1150, "< 1 ms", px=220, color=D.TURQ, k=D.rebote(D.pr(v, 1.2, 1.6)))
        PL.rotulo(lz, W / 2, 1310, "por cuadro (medido: 0,3-0,6 ms)", px=44, k=D.rebote(D.pr(v, 1.4, 1.8)))
        suelo(lz)
        D.muneco(lz, D.escenario("leve").en((v * 0.9) % 3.0), W / 2, SUELO + 200, s=3.5, rayos=0.6, t=v)


def _mez(a, b, u):
    return tuple(int(x + (y - x) * u) for x, y in zip(a, b))


def m_error_puente(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["errores"])
    D.kicker(lz, "ERROR REAL · 5-NOV", W / 2, 230, u, 0.0, fondo=D.CORAL)
    tarjeta(lz, [("declarada:  tramo(x0, x1, y0, y1)", D.PAPEL), ("llamada:     tramo(x0, y0, x1, y1)", D.CORAL)], W / 2, 420, u, 0.2, w=980, px=40)
    to = ctx["k"]("errores_2", "orden")
    ok = D.suave(D.pr(u, to, to + 0.6))
    with lz.capa(1):
        for y in (760, 1180):
            lz.relleno(np.array([[90, y], [990, y], [990, y + 26], [90, y + 26]]), (70, 60, 140))
            lz.relleno(np.array([[420, y - 1], [660, y - 1], [660, y + 27], [420, y + 27]]), (16, 12, 44))
        lz.relleno(D.capsula([400, 760 + 420 * (1 - ok)], [680, 760], 12, 12), _mez(D.CORAL, D.VERDE, ok))
    PL.pastilla(lz, W / 2, 1290, "¡atraviesa dos pisos!" if ok < .5 else "ya cruza el hoyo", px=34,
                fondo=D.CORAL if ok < .5 else D.VERDE, color=D.TINTA, k=D.rebote(D.pr(u, 0.8, 1.2)))
    pip(lz, "puente", 4.0 + u, u, 1.0, cy=1600, w=900, h=480)


def m_cierre(lz, u, ctx):
    D.manchas(lz, u, D.TONOS["cierre"])
    t1 = ctx["k"]("cierre_1")
    if u < t1:
        D.monitor(lz, clip("choque", 3.0 + u), W / 2, 760, 980, 900, u, barrido=D.suave(D.pr(u, 0.4, 2.2)), k=D.rebote(D.pr(u, 0, .4)))
        D.titular(lz, "CADA CAÍDA", 1340, u, 0.3, px=110)
        D.titular(lz, "ES LA PRIMERA", 1470, u, 0.6, px=110, col=D.TURQ)
    else:
        v = u - t1
        D.kicker(lz, "JUNTA DIRECTIVA", W / 2, 330, v, 0.0, fondo=D.AMAR)
        D.titular(lz, "TÚ", 520, v, 0.3, px=260, col=D.AMAR)
        k = D.rebote(D.pr(v, 1.2, 1.6))
        with lz.capa(2), lz.grupo(W / 2, 900, k):
            lz.relleno(D.rrect(0, 10, 900, 220, 40), (6, 4, 24), alfa=0.4)
            lz.relleno(D.rrect(0, 0, 900, 220, 40), D.PAPEL)
            lz.relleno(np.array([[-300, 100], [-220, 100], [-330, 170]]), D.PAPEL)
        PL.rotulo(lz, W / 2, 900, "¿Qué obstáculo les pongo?", px=54, color=D.TINTA, sombra=0, k=k)
        suelo(lz)
        _saluda(lz, v, W / 2, 7.0)


MOMENTOS = dict(gancho=m_gancho, teaser=m_teaser, presenta=m_presenta, pedido=m_pedido, problema=m_problema, verlet=m_verlet,
                musculos=m_musculos, equilibrio=m_equilibrio, agarre=m_agarre, mundo=m_mundo, error_vuela=m_error_vuela,
                error_puente=m_error_puente, cierre=m_cierre)
TONO_DE = dict(teaser="errores", presenta="pedido", agarre="equilibrio", error_vuela="errores", error_puente="errores")

TL_ = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
FR = {f["key"]: f for e in TL_["escenas"] for f in e["frases"]}


def _llano(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn").strip(".,:;¿?¡!-…")


def T(clave, palabra=None):
    f = FR[clave]
    if palabra:
        for w in f.get("words", []):
            if _llano(w["w"]) == _llano(palabra):
                return w["s"]
        return f["t0"] + 0.5 * (f["t1"] - f["t0"])
    return f["t0"]


PLAN = [(0.0, "gancho"), (T("gancho_1") - 0.1, "teaser"), (T("gancho_2") - 0.1, "presenta"), (T("pedido_0") - 0.1, "pedido"),
        (T("problema_0") - 0.1, "problema"), (T("verlet_0") - 0.1, "verlet"), (T("musculos_0") - 0.1, "musculos"),
        (T("equilibrio_0") - 0.1, "equilibrio"), (T("equilibrio_3") - 0.1, "agarre"), (T("mundo_0") - 0.1, "mundo"),
        (T("errores_0") - 0.1, "error_vuela"), (T("errores_2") - 0.1, "error_puente"), (T("cierre_0") - 0.1, "cierre")]


def pinta(lz, nombre, u, t=None):
    t0 = (t if t is not None else u) - u
    tono = D.TONOS.get(TONO_DE.get(nombre, nombre.split("_")[0]), (D.TURQ, D.LILA))
    bg = D.fondo(u if t is None else t, tono)
    lz.nuevo(u, wob=0.0)
    MOMENTOS[nombre](lz, u, dict(t=t, k=lambda clave, palabra=None: T(clave, palabra) - t0))
    return np.clip(componer(bg, lz.resolver()), 0, 1)


def momento_en(t):
    actual = PLAN[0]
    for p in PLAN:
        if p[0] <= t:
            actual = p
    return actual
