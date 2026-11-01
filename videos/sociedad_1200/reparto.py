# -*- coding: utf-8 -*-
"""Reparto de «Las 1.200» (noir color): LA COPIA — cada una de las 1.200 inteligencias, dibujada como un reo de overol con
número y una CABEZA DE MONITOR (tubo de rayos catódicos) cuya pantalla es su cara: ojos de fósforo que parpadean y miran,
texto que se escribe, alarma, carga, y el apagado de tubo (la imagen se aplasta en una raya, luego en un punto).

    C = Copia(sem=3, num="0417")
    C.perfil(h, dict(x, y, s, d, andar, paso, brazos="bracea|teclea|carga|alza|libre", mano=(x, y), mano2=(x, y), sentado,
                      cara=dict(expr="neutro", mira=0.3, col=None, texto=None, apagado=0.0), gabardina, gafas, baston, brazal))
    C.frente(h, dict(x, y, s, manos=..., cara=...))      # de frente (rueda de reconocimiento, celdas, multitudes cercanas)
    copia_mini(h, x, y, s, t, sem, ...)                 # lejana y barata (multitudes de cientos)
    C.cabeza(h, cx, cy, s, cara, t)                     # solo la cabeza, para primeros planos

Coordenadas locales: pies en (0, 0), arriba negativo, ~640 px de alto a s = 1, mirando a +x (d = 1). y = suelo.
Expresiones: neutro · feliz · triste · astuto · miedo · sorpresa · linea (boca cerrada, «callan») · error (X X) · carga (puntos que
giran) · pregunta («?») · off · texto (cara = renglones a máquina, `texto=[...]`, `t0`, `cps`) · alarma (rojo).
"""
import math

import numpy as np

import noir as N
from noir_pers import _ik, cadera_paso, pierna_paso, avance_paso
from toon import blob, elipse_, suave, tubo, eje_curvo

ZANCADA = 72.0


def fase_paso(dist, s=1.0):
    return dist / avance_paso(ZANCADA, s)


def _rect(x, y, w, h):
    return np.array([(x, y), (x + w, y), (x + w, y + h), (x, y + h)], float)


def _rrect(x, y, w, h, r, n=5):
    """Rectángulo de esquinas redondas."""
    P = []
    for cx, cy, a0 in ((x + w - r, y + r, -math.pi / 2), (x + w - r, y + h - r, 0), (x + r, y + h - r, math.pi / 2),
                       (x + r, y + r, math.pi)):
        for a in np.linspace(a0, a0 + math.pi / 2, n):
            P.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return np.array(P)


def parpadeo_ojos(t, sem):
    """0 abierto .. 1 cerrado: parpadeos espaciados (cada copia a su ritmo)."""
    per = 3.1 + (sem % 7) * 0.37
    u = (t + sem * 0.71) % per
    return max(0.0, 1 - abs(u - 0.09) / 0.09) if u < 0.18 else 0.0


# ====================================================================== la cara (pantalla)
def pantalla(h, Tl, w, hh, cara, t, sem, s):
    """Dibuja la pantalla de la cara en coordenadas locales centradas (Tl: local -> mundo). w, hh = tamaño del vidrio."""
    cara = cara or {}
    expr = cara.get("expr", "neutro")
    col = cara.get("col") or h.pal["verde"]
    if expr == "alarma":
        col = h.pal["neon"]
    apag = float(cara.get("apagado", 0.0))
    v = float(cara.get("brillo", 1.0)) * (1 - 0.15 * math.sin(t * 9.0 + sem) ** 8)
    vid = _rrect(-w / 2, -hh / 2, w, hh, min(w, hh) * 0.18)
    # vidrio oscuro, abombado (un reflejo curvo arriba a la izquierda)
    h.pieza(Tl(vid), 26, sem + 300, w=3 * s, luz=(0.3, -1), d=4 * s, sombra=0.2, trama=0, rim=0, rampa="vidrio_verde")
    if expr == "off" or apag >= 1:
        h.pieza(Tl(elipse_(-w * 0.18, -hh * 0.22, w * 0.22, hh * 0.08, rot=-0.4, n=14)), 120, sem + 301, w=0, d=0, sombra=0,
                trama=0, rim=0, alfa=0.35, linea=False, rampa="neutro")
        return
    # el apagado de tubo: la imagen se aplasta en una raya (0..0.6) y luego en un punto (0.6..1)
    ky = 1.0 if apag <= 0 else max(0.02, 1 - apag / 0.6)
    kx = 1.0 if apag <= 0.6 else max(0.02, 1 - (apag - 0.6) / 0.4)
    if apag > 0:
        g = Tl(_rect(-w * 0.46 * kx, -hh * 0.46 * ky, w * 0.92 * kx, hh * 0.92 * ky))
        h.emitir(g, 0.9 + 1.2 * apag, col=col, blur=2.0)
        if apag > 0.5:
            return
    # resplandor de fósforo de fondo
    h.emitir(Tl(_rrect(-w * 0.46, -hh * 0.44 * ky, w * 0.92, hh * 0.88 * ky, 6)), 0.10 * v, col=col, blur=5)
    mira = float(cara.get("mira", 0.0))
    mv = float(cara.get("mira_y", 0.0))
    par = parpadeo_ojos(t, sem) if cara.get("parpadea", True) else 0.0
    par = max(par, float(cara.get("cierra", 0.0)))
    ex = w * 0.2
    ey = -hh * 0.06 + mv * hh * 0.08
    dx = mira * w * 0.12

    def em(P, k=1.0):
        h.emitir(Tl(P), 1.25 * v * k, col=col, blur=1.0)

    if expr in ("neutro", "miedo", "sorpresa", "triste", "astuto", "linea", "alarma"):
        for sx in (-1, 1):
            cx = sx * ex + dx
            if expr == "sorpresa":
                rw, rh = w * 0.11, hh * 0.2
            elif expr == "miedo":
                rw, rh = w * 0.05, hh * 0.08
            elif expr == "astuto":
                rw, rh = w * 0.11, hh * 0.06
            else:
                rw, rh = w * 0.075, hh * 0.15
            rh = max(hh * 0.02, rh * (1 - par))
            if expr == "sorpresa":
                em(elipse_(cx, ey, rw, rh, n=18))
            else:
                P = _rrect(cx - rw, ey - rh, 2 * rw, 2 * rh, min(rw, rh) * 0.6, n=3)
                if expr == "astuto":
                    P = P + np.array([[0, sx * (q[0] - cx) * 0.35] for q in P])
                if expr == "triste":
                    P[:, 1] += np.where(P[:, 1] < ey, (P[:, 0] - cx) * sx * 0.5, 0)
                em(P)
        if expr == "linea":
            em(_rect(-w * 0.16 + dx, hh * 0.22, w * 0.32, hh * 0.035), 0.9)
        elif expr == "miedo":
            xs = np.linspace(-w * 0.16, w * 0.16, 9)
            pts = [(x + dx, hh * 0.24 + (4 if i % 2 else -4) * s) for i, x in enumerate(xs)]
            em(np.array(pts + [(p[0], p[1] + hh * 0.03) for p in pts[::-1]]), 0.8)
        elif expr == "sorpresa":
            em(elipse_(dx, hh * 0.25, w * 0.05, hh * 0.07, n=12), 0.8)
        elif cara.get("boca"):
            b = float(cara["boca"])
            em(elipse_(dx, hh * 0.25, w * 0.08, hh * 0.02 + hh * 0.05 * b, n=12), 0.8)
    elif expr == "feliz":
        for sx in (-1, 1):
            cx = sx * ex + dx
            a = np.linspace(math.pi * 1.1, math.pi * 1.9, 9)
            o = np.stack([cx + w * 0.09 * np.cos(a), ey + hh * 0.06 + hh * 0.13 * np.sin(a)], 1)
            i = np.stack([cx + w * 0.06 * np.cos(a[::-1]), ey + hh * 0.06 + hh * 0.08 * np.sin(a[::-1])], 1)
            em(np.vstack([o, i]))
        a = np.linspace(0.15 * math.pi, 0.85 * math.pi, 11)
        o = np.stack([dx + w * 0.18 * np.cos(a), hh * 0.12 + hh * 0.14 * np.sin(a)], 1)
        i = np.stack([dx + w * 0.13 * np.cos(a[::-1]), hh * 0.12 + hh * 0.08 * np.sin(a[::-1])], 1)
        em(np.vstack([o, i]), 0.9)
    elif expr == "error":
        for sx in (-1, 1):
            cx = sx * ex + dx
            for g in (1, -1):
                em(np.array([(cx - w * 0.08, ey - g * hh * 0.12), (cx - w * 0.05, ey - g * hh * 0.15),
                             (cx + w * 0.08, ey + g * hh * 0.12), (cx + w * 0.05, ey + g * hh * 0.15)]))
    elif expr == "carga":
        for k in range(8):
            a = t * 5.0 + k * math.pi / 4
            r = min(w, hh) * 0.22
            em(elipse_(r * math.cos(a), r * math.sin(a), 4.5 * s, 4.5 * s, n=8), 0.3 + 0.7 * (k / 7))
    elif expr == "pregunta":
        q = cara.get("q", "?")
        _texto_pantalla(h, Tl, q, 0, 0, hh * 0.7, t, -99, col, s, centro=True, cps=1e9)
    elif expr == "texto":
        lineas = cara.get("texto") or []
        t0 = cara.get("t0", -99)
        cps = cara.get("cps", 18.0)
        px = cara.get("px", hh * 0.13)
        y0 = -hh * 0.36
        tt = t0
        for k, ln in enumerate(lineas):
            _texto_pantalla(h, Tl, ln, -w * 0.42, y0 + k * px * 1.45, px, t, tt, col, s, centro=False, cps=cps,
                            ancho=w * 0.84)
            tt += len(ln) / cps + 0.25
        if int(t * 2.2) % 2 == 0:                                  # cursor
            n = sum(1 for k, ln in enumerate(lineas) if t >= t0)
            em(_rect(-w * 0.42, y0 + max(0, len(lineas)) * px * 1.45 - px * 0.1, px * 0.5, px * 0.9), 0.7)
    # líneas de barrido del tubo
    for k in range(6):
        yy = -hh / 2 + ((t * 40 + k * hh / 6) % hh)
        h.pieza(Tl(_rect(-w * 0.46, yy, w * 0.92, 1.6 * s)), 200, sem + 330 + k, w=0, d=0, sombra=0, trama=0, rim=0, alfa=0.08,
                linea=False, rampa="vidrio_verde")


def _texto_pantalla(h, Tl, s_, x, y, px, t, t0, col, esc, centro=False, cps=18.0, ancho=None):
    """Texto de fósforo dentro de la pantalla (emite): se escribe en el lienzo claro y se marca su zona como emisora."""
    P = Tl(np.array([[x, y], [x + 1.0, y]]))
    a = math.atan2(P[1, 1] - P[0, 1], P[1, 0] - P[0, 0])
    k = math.hypot(P[1, 0] - P[0, 0], P[1, 1] - P[0, 1])
    c = np.asarray(col, float)
    tono = np.clip(c / max(c) * 0.95, 0, 1)
    N.texto_maquina(h, s_, P[0, 0], P[0, 1], px * k, t, t0, cps=cps, tono=tono, centro=centro, fuente=N.FUENTE_MAQ,
                    track=1.0, encuadrar=False, ang=a, ancho_max=None if ancho is None else ancho * k)
    if t >= t0:
        im, _ = N._txt_img(s_, px * k, N.FUENTE_MAQ, 1.0)
        n = min(len(s_), int((t - t0) * cps) + 1)
        an = (im.shape[1] - 20) * n / max(1, len(s_))
        if ancho is not None:
            an = min(an, ancho * k)
        x0 = P[0, 0] - (an / 2 if centro else 0)
        y0 = P[0, 1] - (im.shape[0] / 2 if centro else 0)
        h.luz_fija(C_rot(_rect(x0 - 4, y0 - 2, an + 8, im.shape[0] + 4), a, (P[0, 0], P[0, 1])), 1.0)


def C_rot(P, a, c):
    P = np.asarray(P, float) - c
    ca, sa = math.cos(a), math.sin(a)
    return np.stack([P[:, 0] * ca - P[:, 1] * sa, P[:, 0] * sa + P[:, 1] * ca], 1) + c


# ====================================================================== la copia
class Copia:
    def __init__(self, sem=0, num="0417", traje=72, rampa_traje="piedra", grande=False):
        self.sem = sem
        self.num = num
        self.traje = traje
        self.rt = rampa_traje
        self.grande = grande

    # ---------------------------------------------------------------- cabeza de monitor (3/4)
    def cabeza(self, h, cx, cy, s, cara=None, t=None, d=1, luz=(0.3, -1.0), rim=0.85, rot=0.0, gafas=False, sombrero=False,
               cable=True):
        """Monitor de tubo visto en 3/4 hacia d: carcasa con fondo que se estrecha, marco, pantalla (la cara), perillas y rejilla.
        (cx, cy) = centro de la pantalla en el mundo; s = escala (pantalla de ~132 x 112 px a s = 1)."""
        t = h.t if t is None else t
        sem = self.sem
        g = 1.25 if self.grande else 1.0
        W_, H_ = 150 * g, 128 * g

        def Tl(P):
            P = np.asarray(P, float).reshape(-1, 2) * (s * d, s)
            c, sn = math.cos(rot), math.sin(rot)
            return np.stack([P[:, 0] * c - P[:, 1] * sn, P[:, 0] * sn + P[:, 1] * c], 1) + (cx, cy)
        L = luz
        # fondo de la carcasa (hacia atrás, del lado contrario a d): trapecio
        fondo = [(-W_ * 0.42, -H_ * 0.5), (-W_ * 0.42 - 70 * g, -H_ * 0.34), (-W_ * 0.42 - 78 * g, H_ * 0.3), (-W_ * 0.42, H_ * 0.5)]
        h.pieza(Tl(fondo), 104, sem + 200, w=5 * s, luz=L, d=10 * s, trama=0.5, rim=rim, rampa="piedra")
        for k in range(4):                                                   # rejilla de ventilación
            x = -W_ * 0.42 - 16 * g - k * 14 * g
            h.trazo(Tl(np.array([[x, -H_ * 0.22], [x - 3, H_ * 0.18]])), 2.6 * s, sem + 210 + k, alfa=0.7)
        if cable:
            h.pieza(Tl(tubo(np.array([[-W_ * 0.42 - 60 * g, H_ * 0.2], [-W_ * 0.42 - 70 * g, H_ * 0.5], [-W_ * 0.2, H_ * 0.72]]),
                            7, 6)), 30, sem + 205, w=2.5 * s, luz=L, d=3 * s, trama=0, rim=rim * 0.5, rampa="piedra")
        # caja frontal con marco
        h.pieza(Tl(_rrect(-W_ / 2, -H_ / 2, W_, H_, 18 * g)), 156, sem + 220, w=6 * s, luz=L, d=14 * s, trama=0.35, rim=rim,
                rampa="piedra")
        vw, vh = W_ * 0.78, H_ * 0.72

        def Ts(P):                                   # la pantalla NO se refleja con d (el texto se lee siempre)
            P = np.asarray(P, float).reshape(-1, 2) * s + (-W_ * 0.03 * s * d, -H_ * 0.04 * s)
            c, sn = math.cos(rot), math.sin(rot)
            return np.stack([P[:, 0] * c - P[:, 1] * sn, P[:, 0] * sn + P[:, 1] * c], 1) + (cx, cy)
        cara = dict(cara or {})
        cara["mira"] = cara.get("mira", 0.0) * d + (0.25 * d if "mira" not in cara else 0.0)
        pantalla(h, Ts, vw, vh, cara, t, sem, s)
        # perillas bajo la pantalla y el piloto
        for k, px in enumerate((W_ * 0.28, W_ * 0.38)):
            h.pieza(Tl(elipse_(px, H_ * 0.39, 7 * g, 7 * g, n=10)), 60, sem + 230 + k, w=2.5 * s, luz=L, d=2, trama=0, rim=0.6,
                    rampa="piedra")
        apag = (cara or {}).get("apagado", 0.0)
        if (cara or {}).get("expr") != "off" and apag < 1:
            h.emitir(Tl(elipse_(-W_ * 0.34, H_ * 0.39, 4 * g, 4 * g, n=8)), 1.2, col=h.pal["neon"], blur=1)
        if gafas:                                                            # gafas oscuras redondas (el «ciego»)
            for sx in (-1, 1):
                h.pieza(Tl(elipse_(sx * W_ * 0.17 - W_ * 0.03, -H_ * 0.08, W_ * 0.15, W_ * 0.14, n=22)), 12, sem + 240 + sx, w=4 * s,
                        luz=L, d=3, sombra=0, trama=0, rim=0.9, rim_tono=200, rampa="piedra")
            h.trazo(Tl(np.array([[-W_ * 0.06, -H_ * 0.1], [W_ * 0.0, -H_ * 0.12]])), 4 * s, sem + 243)
            h.trazo(Tl(np.array([[-W_ * 0.35, -H_ * 0.1], [-W_ * 0.5, -H_ * 0.14]])), 4 * s, sem + 244)
        if sombrero:                                                         # fedora sobre el monitor
            h.pieza(Tl(suave([(-W_ * 0.5, -H_ * 0.66), (-W_ * 0.42, -H_ * 1.05), (-W_ * 0.1, -H_ * 1.14), (W_ * 0.1, -H_ * 1.06),
                              (W_ * 0.36, -H_ * 1.12), (W_ * 0.44, -H_ * 0.66)], 4)), 40, sem + 250, w=5 * s, luz=L, d=8 * s,
                    trama=0.5, rim=rim, rampa="gabardina")
            h.pieza(Tl(elipse_(-W_ * 0.04, -H_ * 0.66, W_ * 0.72, H_ * 0.1, n=30)), 34, sem + 251, w=5 * s, luz=L, d=5 * s, trama=0.3,
                    rim=rim, rampa="gabardina")
            h.pieza(Tl(_rect(-W_ * 0.47, -H_ * 0.8, W_ * 0.9, H_ * 0.1)), 12, sem + 252, w=0, luz=L, d=1, sombra=0, trama=0, rim=0,
                    alfa=0.9, linea=False, rampa="vino")

    # ---------------------------------------------------------------- cuerpo de perfil
    def perfil(self, h, p):
        x, y, s, d = p["x"], p["y"], p.get("s", 1.0), p.get("d", 1)
        sem = self.sem
        g = 1.12 if self.grande else 1.0
        L = p.get("luz", (0.4, -1.0))
        Ld = (L[0] * d, L[1])
        rim = p.get("rim", 0.85)
        andar = p.get("andar", 0.0)
        fase = p.get("paso", 0.0)
        sent = p.get("sentado", False)
        inc = p.get("inclina", 0.0)
        tr = self.traje
        rt = self.rt
        gab = p.get("gabardina", False)

        def T(P):
            P = np.asarray(P, float)
            lx = P[..., 0] + inc * (-P[..., 1]) * 0.15
            return np.stack([x + d * s * g * lx, y + s * g * P[..., 1]], -1)
        kw = dict(luz=Ld, rim=rim)
        if sent:
            alt = 126.0
            bob = 250.0 - alt
        else:
            alt = cadera_paso(fase, 250.0, ZANCADA * andar)
            bob = 250.0 - alt
        resp = 2.0 * math.sin(h.t * 1.7 + sem) * (1 - andar)
        hom = np.array([4.0, -452 + bob + resp])

        def brazo(k, sm, objetivo=None):
            if objetivo is not None:
                man = np.asarray(objetivo, float)
                codo = _ik(hom, man, 100, 96, -1.0 if k else -1.0)
            else:
                a = 0.55 * math.sin(fase + math.pi * (1 - k)) * andar + (0.06 * math.sin(h.t * 1.3 + k) if andar < 0.1 else 0)
                codo = hom + 100 * np.array([math.sin(a), math.cos(a)])
                man = codo + 92 * np.array([math.sin(a + 0.35), math.cos(a + 0.35)])
            h.pieza(T(tubo(np.array([hom, codo, man]), 40, 30)), (tr - 10 + 12 * k) if not gab else 70 + 8 * k, sem + sm, w=5 * s,
                    d=10 * s, trama=0.4, rampa=rt if not gab else "gabardina", **kw)
            h.pieza(T(suave([(man[0] - 14, man[1] - 12), (man[0] + 16, man[1] - 14), (man[0] + 22, man[1] + 6), (man[0] + 6, man[1] + 20),
                             (man[0] - 14, man[1] + 12)], 3)), 120, sem + sm + 1, w=3.5 * s, d=5 * s, trama=0.1, rampa="piedra", **kw)
            return T(man)
        modo = p.get("brazos", "bracea")
        obj_a, obj_b = None, None
        if modo == "teclea":
            tk = math.sin(h.t * 19 + sem)
            obj_a = np.array([150.0, -300 + bob + 6 * tk])
            obj_b = np.array([118.0, -296 + bob - 6 * tk])
        elif modo == "carga":
            obj_a = np.array([120.0, -340 + bob])
            obj_b = np.array([100.0, -336 + bob])
        elif modo == "alza":
            obj_a = np.array([150.0, -600 + bob])
        if p.get("mano") is not None:
            obj_a = np.asarray(p["mano"], float) + (0, bob if p.get("mano_bob", True) else 0)
        if p.get("mano2") is not None:
            obj_b = np.asarray(p["mano2"], float) + (0, bob if p.get("mano_bob", True) else 0)
        manos = {}
        manos["atras"] = brazo(0, 20, obj_b)
        # piernas
        for k in (0, 1):
            if sent:
                cad = np.array([0.0, -alt])
                rod = np.array([118.0 + 6 * k, -alt - 6])
                pie = np.array([128.0 + 6 * k, 0.0])
            else:
                ph = fase + math.pi * k
                cad = np.array([0.0, -alt])
                rod, pie = pierna_paso(ph, cad, 126, 126, ZANCADA * andar, 30 * andar * andar)
            h.pieza(T(tubo(np.array([cad, rod, pie]), 50, 34)), tr - 16 + 10 * k, sem + k, w=5 * s, d=10 * s, trama=0.5, rampa=rt, **kw)
            h.pieza(T(suave([(pie[0] - 18, pie[1] - 14), (pie[0] + 32, pie[1] - 10), (pie[0] + 44, pie[1] + 4),
                             (pie[0] - 18, pie[1] + 6)], 3)), 14, sem + 4 + k, w=3.5 * s, d=4 * s, trama=0, rampa="gabardina", **kw)
        # torso (overol) y número
        tor = suave([(-44, -470 + bob), (-8, -490 + bob), (30, -482 + bob), (48, -440 + bob), (50, -330 + bob), (42, -228 + bob),
                     (-42, -228 + bob), (-52, -330 + bob)], 4)
        if gab:
            tor_g = suave([(-50, -476 + bob), (-8, -496 + bob), (36, -486 + bob), (56, -440 + bob), (60, -300 + bob), (66, -150 + bob),
                           (-62, -150 + bob), (-58, -300 + bob)], 4)
            h.pieza(T(tor_g), 78, sem + 8, w=6 * s, d=16 * s, trama=0.6, rampa="gabardina", **kw)
            h.pieza(T([(24, -486 + bob), (44, -470 + bob), (30, -380 + bob), (16, -420 + bob)]), 96, sem + 9, w=3 * s, d=4 * s,
                    trama=0.2, rampa="gabardina", **kw)
            h.trazo(T(np.array([[-8, -300 + bob], [56, -300 + bob]])), 5 * s, sem + 10, alfa=0.8)
        else:
            h.pieza(T(tor), tr, sem + 8, w=6 * s, d=16 * s, trama=0.6, rampa=rt, **kw)
            h.trazo(T(np.array([[20, -480 + bob], [24, -240 + bob]])), 2.6 * s, sem + 11, alfa=0.6)          # cremallera
            pq = T(_rect(-8, -430 + bob, 46, 30))
            h.pieza(pq, 214, sem + 12, w=2.5 * s, d=2, sombra=0, trama=0, rim=0, rampa="papel", luz=Ld)
            if self.num and s * g > 0.55:
                c = pq.mean(0)
                N.texto_maquina(h, self.num, c[0], c[1], 17 * s * g, h.t, -99, cps=1e9, tono=0.05, centro=True,
                                fuente=N.FUENTE_MAQ, track=0.5, encuadrar=False)
            if p.get("brazal"):                                               # brazalete de reclutadora
                h.pieza(T(_rect(-30, -420 + bob, 22, 34)), 120, sem + 13, w=2.5 * s, d=2, sombra=0.3, trama=0, rim=0.5,
                        rampa="vino", luz=Ld)
        h.pieza(T(_rect(-10, -508 + bob, 34, 30)), 46, sem + 14, w=3 * s, d=4 * s, trama=0.2, rampa="piedra", **kw)   # cuello
        manos["frente"] = brazo(1, 16, obj_a)
        # cabeza
        cab = T(np.array([[18.0, -570 + bob + resp * 0.5]]))[0]
        cara = dict(p.get("cara") or {})
        self.cabeza(h, cab[0], cab[1], s * g * 0.98, cara, d=d, luz=L, rim=rim, rot=p.get("cab_rot", 0.0) * d,
                    gafas=p.get("gafas", False), sombrero=p.get("sombrero", gab))
        if p.get("baston"):
            m = manos["frente"]
            h.pieza(tubo(np.array([m, [m[0] + d * 40 * s, y]]), 9 * s, 8 * s), 222, sem + 260, w=3 * s, luz=Ld, d=3, trama=0, rim=0.6,
                    rampa="papel")
        self._manos = manos
        return manos

    # ---------------------------------------------------------------- de frente
    def frente(self, h, p):
        x, y, s = p["x"], p["y"], p.get("s", 1.0)
        sem = self.sem
        g = 1.12 if self.grande else 1.0
        L = p.get("luz", (0.0, -1.0))
        rim = p.get("rim", 0.85)
        tr = self.traje
        rt = self.rt
        bal = p.get("bal", 0.0)

        def T(P):
            P = np.asarray(P, float).reshape(-1, 2)
            return np.stack([x + s * g * (P[:, 0] + bal * (-P[:, 1]) / 600), y + s * g * P[:, 1]], 1)
        kw = dict(luz=L, rim=rim)
        resp = 2.0 * math.sin(h.t * 1.6 + sem)
        for k, sx in enumerate((-1, 1)):
            h.pieza(T([(sx * 6, -262), (sx * 54, -262), (sx * 48, -14), (sx * 12, -14)]), tr - 18 + 8 * k, sem + k, w=5 * s, d=8 * s,
                    trama=0.5, rampa=rt, **kw)
            h.pieza(T(suave([(sx * 8, -18), (sx * 58, -22), (sx * 64, -2), (sx * 6, 0)], 3)), 14, sem + 2 + k, w=3 * s, d=4 * s,
                    trama=0, rampa="gabardina", **kw)
        tor = suave([(-78, -404 + resp), (-30, -420 + resp), (30, -420 + resp), (78, -404 + resp), (84, -330), (74, -240), (-74, -240),
                     (-84, -330)], 5)
        h.pieza(T(tor), tr, sem + 10, w=6 * s, d=14 * s, trama=0.55, rampa=rt, **kw)
        h.trazo(T(np.array([[0, -418 + resp], [0, -250]])), 2.6 * s, sem + 11, alfa=0.6)
        pq = T(_rect(16, -392 + resp, 50, 30))
        h.pieza(pq, 214, sem + 12, w=2.5 * s, d=2, sombra=0, trama=0, rim=0, rampa="papel", luz=L)
        if self.num and s * g > 0.5:
            c = pq.mean(0)
            N.texto_maquina(h, self.num, c[0], c[1], 17 * s * g, h.t, -99, cps=1e9, tono=0.05, centro=True, fuente=N.FUENTE_MAQ,
                            track=0.5, encuadrar=False)
        if p.get("brazal"):
            h.pieza(T(_rect(-96, -378, 26, 36)), 120, sem + 13, w=2.5 * s, d=2, sombra=0.3, trama=0, rim=0.5, rampa="vino", luz=L)
        manos = p.get("manos")
        out = []
        for k, sx in enumerate((-1, 1)):
            ho = np.array([sx * 80.0, -394 + resp])
            if manos is not None and manos[k] is not None:
                ma = np.asarray(manos[k], float)
            else:
                ma = np.array([sx * 86.0, -232 + 4 * math.sin(h.t * 1.3 + k)])
            co = _ik(ho, ma, 92, 92, -sx)
            h.pieza(T(tubo(np.array([ho, co, ma]), 38, 30)), tr - 6, sem + 20 + k, w=5 * s, d=10 * s, trama=0.4, rampa=rt, **kw)
            h.pieza(T(blob(ma[0], ma[1] + 6, 15, 18, n=8)), 120, sem + 22 + k, w=3.5 * s, d=5 * s, trama=0.1, rampa="piedra", **kw)
            out.append(T(ma)[0])
        h.pieza(T(_rect(-18, -446 + resp, 36, 30)), 46, sem + 14, w=3 * s, d=4 * s, trama=0.2, rampa="piedra", **kw)
        cab = T(np.array([[0.0, -518 + resp]]))[0]
        self.cabeza_frente(h, cab[0], cab[1], s * g, p.get("cara"), L, rim, p.get("cab_rot", 0.0), gafas=p.get("gafas", False))
        return out

    def cabeza_frente(self, h, cx, cy, s, cara=None, luz=(0, -1), rim=0.85, rot=0.0, gafas=False, t=None):
        """Monitor de frente (se ve un poco el techo de la carcasa)."""
        t = h.t if t is None else t
        sem = self.sem
        g = 1.25 if self.grande else 1.0
        W_, H_ = 150 * g, 128 * g

        def Tl(P):
            P = np.asarray(P, float).reshape(-1, 2) * s
            c, sn = math.cos(rot), math.sin(rot)
            return np.stack([P[:, 0] * c - P[:, 1] * sn, P[:, 0] * sn + P[:, 1] * c], 1) + (cx, cy)
        h.pieza(Tl([(-W_ * 0.44, -H_ * 0.5), (-W_ * 0.34, -H_ * 0.66), (W_ * 0.34, -H_ * 0.66), (W_ * 0.44, -H_ * 0.5)]), 118,
                sem + 201, w=5 * s, luz=luz, d=6 * s, trama=0.3, rim=rim, rampa="piedra")
        h.pieza(Tl(_rrect(-W_ / 2, -H_ / 2, W_, H_, 18 * g)), 156, sem + 220, w=6 * s, luz=luz, d=12 * s, trama=0.35, rim=rim,
                rampa="piedra")
        pantalla(h, lambda P: Tl(np.asarray(P, float).reshape(-1, 2) + (0, -H_ * 0.04)), W_ * 0.8, H_ * 0.72, cara, t, sem, s)
        for k, px in enumerate((W_ * 0.3, W_ * 0.4)):
            h.pieza(Tl(elipse_(px, H_ * 0.4, 6 * g, 6 * g, n=10)), 60, sem + 230 + k, w=2.5 * s, luz=luz, d=2, trama=0, rim=0.6,
                    rampa="piedra")
        if gafas:
            for sx in (-1, 1):
                h.pieza(Tl(elipse_(sx * W_ * 0.2, -H_ * 0.08, W_ * 0.15, W_ * 0.14, n=22)), 12, sem + 240 + sx, w=4 * s, luz=luz, d=3,
                        sombra=0, trama=0, rim=0.9, rim_tono=200, rampa="piedra")


# ====================================================================== multitudes baratas
def copia_mini(h, x, y, s, t, sem=0, cara="neutro", brillo=1.0, d=1, andar=0.0, dist=0.0, col=None, tono=60, rampa="piedra",
               apagado=0.0, ojos=True):
    """Copia lejana: silueta de overol + monitor con dos ojos de fósforo (3-5 piezas sin tramado). y = pies."""
    def T(P):
        P = np.asarray(P, float).reshape(-1, 2)
        return np.stack([x + d * s * P[:, 0], y + s * P[:, 1]], 1)
    fase = dist / avance_paso(ZANCADA, s) if andar > 0 else 0.0
    bob = -6 * andar * abs(math.cos(fase))
    for k in (0, 1):
        sw = 40 * andar * math.sin(fase + math.pi * k)
        h.pieza(T([(-30 + 26 * k, -250 + bob), (2 + 26 * k, -250 + bob), (10 + sw + 6 * k, 0), (-22 + sw + 6 * k, 0)]), tono - 14, sem + k, w=2.5 * s,
                d=0, sombra=0, trama=0, rim=0.5, rampa=rampa)
    h.pieza(T(suave([(-50, -470 + bob), (50, -470 + bob), (54, -240 + bob), (-54, -240 + bob)], 3)), tono, sem + 3, w=3 * s,
            d=8 * s, sombra=0.4, trama=0, rim=0.7, rampa=rampa)
    h.pieza(T(_rrect(-62, -600 + bob, 124, 106, 16)), 150, sem + 4, w=3 * s, d=6 * s, sombra=0.3, trama=0, rim=0.8, rampa="piedra")
    if apagado >= 1:
        h.pieza(T(_rrect(-50, -590 + bob, 100, 80, 12)), 22, sem + 5, w=0, d=0, sombra=0, trama=0, rim=0, rampa="vidrio_verde")
        return
    h.pieza(T(_rrect(-50, -590 + bob, 100, 80, 12)), 26, sem + 5, w=1.5 * s, d=0, sombra=0, trama=0, rim=0, rampa="vidrio_verde")
    c = col or h.pal["verde"]
    v = brillo * (1 - apagado)
    h.emitir(T(_rrect(-46, -586 + bob, 92, 72, 10)), 0.12 * v, col=c, blur=3)
    if ojos and s > 0.06:
        par = parpadeo_ojos(t, sem)
        for sx in (-1, 1):
            if cara == "linea":
                hh = 12
            elif cara == "astuto":
                hh = 6
            else:
                hh = 16 * (1 - par) + 2
            h.emitir(T(_rect(sx * 20 - 7, -556 - hh / 2 + bob, 14, hh)), 1.2 * v, col=c, blur=0.8)
        if cara == "linea":
            h.emitir(T(_rect(-16, -526 + bob, 32, 4)), 1.0 * v, col=c, blur=0.8)


def cabeza_mini(h, x, y, s, t, sem=0, cara="neutro", brillo=1.0, col=None):
    """Solo la cara de una copia (monitor de frente, sin cuerpo): para mosaicos de cientos de autores."""
    def T(P):
        return np.asarray(P, float).reshape(-1, 2) * s + (x, y)
    h.pieza(T(_rrect(-62, -53, 124, 106, 16)), 150, sem + 4, w=2.5 * s, d=4 * s, sombra=0.3, trama=0, rim=0.6, rampa="piedra")
    h.pieza(T(_rrect(-50, -46, 100, 80, 12)), 26, sem + 5, w=1.2 * s, d=0, sombra=0, trama=0, rim=0, rampa="vidrio_verde")
    c = col or h.pal["verde"]
    h.emitir(T(_rrect(-46, -42, 92, 72, 10)), 0.14 * brillo, col=c, blur=2)
    par = parpadeo_ojos(t, sem)
    for sx in (-1, 1):
        hh = 16 * (1 - par) + 2 if cara != "astuto" else 6
        h.emitir(T(_rect(sx * 20 - 7, -14 - hh / 2, 14, hh)), 1.2 * brillo, col=c, blur=0.8)


def espalda(h, x, y, s, t, sem=0, sentado=False, luz=(0.2, -1.0), rim=0.9, timer=None, traje=72, rampa="piedra", cab_rot=0.0,
            hombros=0.0):
    """Copia vista DE ESPALDAS (sentada o de pie): overol, y la parte de atrás del monitor (carcasa con rejilla, cable) con un
    cronómetro LED atado en la nuca si timer = «00:59:12» (dígitos rojos que emiten). Devuelve el centro del cronómetro."""
    def T(P):
        return np.asarray(P, float).reshape(-1, 2) * s + (x, y)
    kw = dict(luz=luz, rim=rim)
    dy = 126 if sentado else 0
    resp = 2.0 * math.sin(t * 1.6 + sem)
    if not sentado:
        for k, sx in enumerate((-1, 1)):
            h.pieza(T([(sx * 6, -262), (sx * 54, -262), (sx * 48, -14), (sx * 12, -14)]), traje - 18 + 8 * k, sem + k, w=5 * s, d=8 * s,
                    trama=0.5, rampa=rampa, **kw)
    tor = suave([(-80, -404 + resp + dy), (-30, -420 + resp + dy), (30, -420 + resp + dy), (80, -404 + resp + dy), (86, -330 + dy),
                 (78, -230 + dy), (-78, -230 + dy), (-86, -330 + dy)], 5)
    h.pieza(T(tor), traje - 6, sem + 10, w=6 * s, d=14 * s, trama=0.6, rampa=rampa, **kw)
    h.trazo(T(np.array([[0, -416 + dy], [0, -240 + dy]])), 3 * s, sem + 11, alfa=0.5)                      # costura
    for k, sx in enumerate((-1, 1)):
        ho = np.array([sx * 82.0, -394 + resp + dy + hombros * 10])
        ma = np.array([sx * 70.0, -250 + dy]) if not sentado else np.array([sx * 40.0, -300 + dy])
        co = _ik(ho, ma, 92, 92, -sx)
        h.pieza(T(tubo(np.array([ho, co, ma]), 38, 30)), traje - 14, sem + 20 + k, w=5 * s, d=10 * s, trama=0.4, rampa=rampa, **kw)
    h.pieza(T(_rect(-18, -446 + resp + dy, 36, 30)), 46, sem + 14, w=3 * s, d=4 * s, trama=0.2, rampa="piedra", **kw)
    c = np.array([0.0, -520 + resp + dy])

    def Tc(P):
        P = np.asarray(P, float).reshape(-1, 2)
        ca, sa = math.cos(cab_rot), math.sin(cab_rot)
        P = np.stack([P[:, 0] * ca - P[:, 1] * sa, P[:, 0] * sa + P[:, 1] * ca], 1) + c
        return T(P)
    h.pieza(Tc(_rrect(-76, -64, 152, 128, 18)), 120, sem + 30, w=6 * s, d=12 * s, trama=0.4, rampa="piedra", **kw)   # canto
    h.pieza(Tc([(-56, -54), (56, -54), (40, 50), (-40, 50)]), 104, sem + 31, w=5 * s, d=10 * s, trama=0.5, rampa="piedra", **kw)
    for k in range(5):
        h.trazo(Tc(np.array([[-36 + k * 18, -40], [-30 + k * 15, 30]])), 2.6 * s, sem + 32 + k, alfa=0.7)
    h.pieza(Tc(tubo(np.array([[0, 46], [10, 90], [-6, 120]]), 9, 8)), 30, sem + 40, w=2.5 * s, d=3 * s, trama=0, rampa="piedra", **kw)
    if timer:
        h.pieza(Tc(_rrect(-62, -22, 124, 44, 8)), 18, sem + 41, w=3 * s, d=3, sombra=0, trama=0, rim=0.6, rampa="piedra", luz=luz)
        for sx in (-1, 1):
            h.pieza(Tc(_rect(sx * 66 - 6, -10, 12, 20)), 60, sem + 42 + sx, w=0, d=0, sombra=0, trama=0, rim=0, rampa="vino")
        p = Tc(np.array([[0, 0]]))[0]
        P2 = Tc(np.array([[0, 0], [1, 0]]))
        a = math.atan2(P2[1, 1] - P2[0, 1], P2[1, 0] - P2[0, 0])
        col = h.pal["neon"]
        N.texto_maquina(h, timer, p[0], p[1], 30 * s, t, -99, cps=1e9, tono=np.clip(np.array(col) / max(col), 0, 1), centro=True,
                        fuente="C:/Windows/Fonts/consolab.ttf", encuadrar=False, ang=a)
        h.emitir(Tc(_rect(-56, -16, 112, 32)), 0.55, col=col, blur=3)
        h.luz_fija(Tc(_rect(-58, -18, 116, 36)), 1.0)
        return p
    return Tc(np.array([[0, 0]]))[0]
