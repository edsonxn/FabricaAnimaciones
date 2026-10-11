# -*- coding: utf-8 -*-
"""¿Cómo nació el primer fotón? — Short vertical (boceto + guache). Cada escena es una función PURA del tiempo global
(coreo_*.py): pinta el fondo a guache (capas con paralaje + efectos), pega los dibujos de boceto como pegatinas y devuelve el cuadro.
Entre escenas hay cambios procedurales (iris, pincelada, ola, destello) hechos con el mismo pincel: se mezcla el cuadro de la escena
vecina con una máscara pintada, así nunca hay cortes duros."""
import math
import types
from contextlib import contextmanager

import cv2
import numpy as np

import boceto as B
import kit as K
import pintura as P
from escena_base import Escena, TL
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

_ESC = {e["id"]: e for e in TL["escenas"]}
_ORD = [e["id"] for e in TL["escenas"]]
TOTAL = TL["total"]
pi = math.pi


def T(eid, texto, **kw):
    """Instante (s) en que se dice `texto` en la escena `eid` (prefijo de palabra; `frase=` para desambiguar)."""
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid):
    return _ESC[eid]["t0"]


def FIN(eid):
    return _ESC[eid]["t1"]


# ------------------------------------------------------------------ cambios de escena pintados
_YY, _XX = np.mgrid[0:H, 0:W].astype(np.float32)
_VIG = None


def vineta():
    global _VIG
    if _VIG is None:
        d = np.hypot((_XX - W / 2) / (W * 0.62), (_YY - H / 2) / (H * 0.62))
        _VIG = (1 - 0.20 * np.clip(d - 0.55, 0, 1) ** 1.6)[..., None].astype(np.float32)
    return _VIG


def mascara_cambio(tipo, u, cx=W / 2, cy=H / 2, ang=0.0, seed=3):
    """(máscara 0..1 de lo NUEVO, anillo de borde) para un cambio pintado. u 0..1."""
    n = P.campo(seed, 110, 2, shape=(H, W)) * 0.045
    if tipo == "iris":
        rmax = math.hypot(max(cx, W - cx), max(cy, H - cy)) * 1.05
        f = np.hypot(_XX - cx, _YY - cy) / rmax + n
        thr = u * 1.12
    else:                                    # pincelada que barre en la dirección `ang`
        c, s = math.cos(ang), math.sin(ang)
        pr = _XX * c + _YY * s
        pr = (pr - pr.min()) / (pr.max() - pr.min())
        f = pr + n + 0.06 * np.sin(_YY / 60.0 + seed)
        thr = u * 1.25 - 0.1
    m = (f < thr).astype(np.float32)
    ring = ((f >= thr - 0.028) & (f < thr)).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.2)
    return m, ring


CAMBIOS = {   # escena que ENTRA -> (tipo, dur, kwargs)
    "calor": ("iris", 0.7, dict(cx=W / 2, cy=760)),
    "higgs": ("pincel", 0.7, dict(ang=0.25)),
    "multitud": ("pincel", 0.7, dict(ang=pi / 2 + 0.3)),
    "niebla": ("iris", 0.7, dict(cx=W / 2, cy=980)),
    "libre": ("pincel", 0.7, dict(ang=-0.5)),
    "hoy": ("iris", 0.6, dict(cx=W / 2, cy=900)),
}
COL_BORDE = (251, 238, 208)


# ------------------------------------------------------------------ contexto de dibujo (uno por proceso)
def _ext(d):
    """Radio (px locales) que abarca un Dib desde su origen."""
    if not hasattr(d, "_ext"):
        d._ext = max(float(np.hypot(op[1][:, 0], op[1][:, 1]).max()) for op in d.ops)
    return d._ext


class Ctx:
    def __init__(self):
        self.h = B.Hoja()
        self.main = self.h
        self.scratch = B.Hoja()
        self.capas = {}
        self.t = 0.0
        self.cam = (1.0, 0.0, 0.0)
        self.fs = 0
        self.te = 0.0
        self.id = ""

    # --- capas con oclusión: cada pegatina se dibuja aparte y TAPA lo que hay debajo (si no, las tintas se ven a través)
    @contextmanager
    def capa(self, cx, cy, rx, ry=None):
        ry = rx if ry is None else ry
        x0, y0 = max(0, int(cx - rx)), max(0, int(cy - ry))
        x1, y1 = min(W, int(cx + rx) + 1), min(H, int(cy + ry) + 1)
        main, sc = self.main, self.scratch
        self.h = sc
        try:
            yield
        finally:
            self.h = main
            if x1 > x0 and y1 > y0:
                sl = (slice(y0, y1), slice(x0, x1))
                m = ((sc.peg[sl] > 0) | (sc.tinta[sl] > 0) | (sc.cal[sl] > 0)).astype(np.uint8)
                m = cv2.dilate(m, np.ones((5, 5), np.uint8)) > 0
                if m.any():
                    main.tinta[sl][m] = sc.tinta[sl][m]
                    main.cal[sl][m] = sc.cal[sl][m]
                    main.cray[sl][m] = sc.cray[sl][m]
                    np.maximum(main.peg[sl], sc.peg[sl], out=main.peg[sl])
                    main.hay_peg = main.hay_peg or sc.hay_peg
                    main.hay_cray = main.hay_cray or sc.hay_cray
                sc.tinta[sl] = 0
                sc.cal[sl] = 0
                sc.peg[sl] = 0
                sc.hay_peg = False
                sc.hay_cray = False

    # --- cámara
    def xy(self, x, y, f=1.0):
        z, dx, dy = self.cam
        zz = 1 + (z - 1) * f
        return W / 2 + (x - W / 2) * zz + dx * f, H / 2 + (y - H / 2) * zz + dy * f

    def k(self, f=1.0):
        return 1 + (self.cam[0] - 1) * f

    # --- fondo
    def base(self, id_, capas):
        z, dx, dy = self.cam
        return P.componer(capas, z, dx, dy)

    def fondo(self, img8):
        self.main.fondo = img8.astype(np.float32) * (1 / 255.0)

    def fin(self):
        out = np.clip(self.main.componer() * 255 + 0.5, 0, 255).astype(np.uint8)
        return out

    # --- dibujos
    def pon(self, d, x, y, s=1.0, rot=0.0, flip=False, t_in=None, modo="pop", dur=0.38, sem=0, vida=1.0, sq=0.0, dy=0.0, f=1.0,
            u=None, lapiz=0.0, peg=True, t_out=None, d_out=0.25, sale="encoger"):
        """Pega un Dib. t_in/modo: entrada (pop, pluma, lt, sube, cae); t_out: salida (encoger, borrar, sube_fuera, baja)."""
        t = self.t
        sm, uu, q, lap, ddy = 1.0, 1.0, sq, lapiz, dy
        if t_in is not None:
            sm, uu, q2, lap2, d2 = K.entrada(t, t_in, modo, dur)
            q += q2
            lap = max(lap, lap2)
            ddy += d2
            if sm <= 0:
                return
        if u is not None:
            uu = min(uu, u)
        if t_out is not None and t > t_out:
            v = prog(t, t_out, t_out + d_out)
            if v >= 1:
                return
            if sale == "encoger":
                sm *= 1 - e_in(v)
            elif sale == "borrar":
                uu = min(uu, 1 - v)
            elif sale == "sube_fuera":
                ddy -= 1500 * e_in(v)
            elif sale == "baja":
                ddy += 1500 * e_in(v)
        px, py = self.xy(x, y + ddy, f)
        ss = s * sm * self.k(f)
        R_ = _ext(d) * abs(ss) * 1.2 + 40
        if px < -R_ or px > W + R_ or py < -R_ or py > H + R_:
            return
        with self.capa(px, py, R_):
            K.poner(self.h, d, px, py, ss, rot, flip, uu, self.fs, sem, self.te, vida, q, lap, peg)

    def foti(self, x, y, s=1.0, rot=0.0, ojos="abiertos", boca="sonrisa", t_in=None, modo="pop", dur=0.38, cola=True, largo=170.0,
             vida=1.0, f=1.0, flip=False, mejillas=True, sem=3, t_out=None, d_out=0.25, sale="encoger", dy=0.0, amp=15.0, frio=False, u=None, lapiz=0.0):
        t = self.t
        if ojos in ("abiertos", "grandes") and ((t * 0.93 + sem * 0.37) % 3.2) < 0.13:
            ojos = "cerrados"
        if cola:
            c = K.cola(t, largo=largo, amp=amp)
            self._foti_cola(c, x, y, s, rot, t_in, modo, dur, f, flip, t_out, d_out, sale, dy, u, lapiz)
        self.pon(K.foti(ojos, boca, mejillas, 12, frio), x, y, s, rot, flip, t_in, modo, dur, sem, vida, 0.0, dy, f, u, lapiz, True, t_out, d_out, sale)

    def _foti_cola(self, c, x, y, s, rot, t_in, modo, dur, f, flip, t_out, d_out, sale, dy, u=None, lapiz=0.0):
        # la cola es hija del cuerpo: gira con él (rot) y se voltea con flip
        self.pon(c, x, y, s, rot, flip, t_in, modo, dur, 9, 0.6, 0.0, dy, f, u, lapiz, True, t_out, d_out, sale)

    def rot(self, txt, x, y, px=96, rot=0.0, color=(238, 70, 62), t_in=None, dur=0.32, s=1.0, tira=False, f=1.0, t_out=None, d_out=0.2,
            u=None):
        t = self.t
        sm = 1.0
        if t_in is not None:
            if t < t_in:
                return
            sm = e_back(prog(t, t_in, t_in + dur), 2.2)
        if t_out is not None and t > t_out:
            v = prog(t, t_out, t_out + d_out)
            if v >= 1:
                return
            sm *= 1 - e_in(v)
        px_, py_ = self.xy(x, y, f)
        ss = s * sm * self.k(f)
        if ss <= 0.02:
            return
        hw, hh = K.ancho_txt(txt, int(px)) * ss * 0.62 + 50, px * ss * 1.0 + 60
        with self.capa(px_, py_, hw, hh):
            K.rotulo(self.h, txt, px_, py_, px, rot, color, ss, 1.0 if u is None else u, tira)

    # --- cuadro
    def comenzar(self, id_, t):
        self.id = id_
        self.t = t
        self.te = t
        self.fs = B.fase(t)
        self.h = self.main
        self.main.limpiar()

    def capas_de(self, id_, fn):
        if id_ not in self.capas:
            if len(self.capas) >= 2:
                self.capas.pop(next(iter(self.capas)))
            self.capas[id_] = fn()
        return self.capas[id_]


CTX = None


def _ctx():
    global CTX
    if CTX is None:
        CTX = Ctx()
    return CTX


# ------------------------------------------------------------------ registro de escenas
FNS = {}


def escena(id_):
    def deco(fn):
        FNS[id_] = fn
        return fn
    return deco


import coreo_1  # noqa: E402,F401  (gancho)
import coreo_1b  # noqa: E402,F401  (calor, higgs)
import coreo_2  # noqa: E402,F401  (multitud, niebla, libre)
import coreo_3  # noqa: E402,F401  (hoy, cierre)


def pintar_escena(id_, t):
    C = _ctx()
    C.comenzar(id_, t)
    img = FNS[id_](C, t)
    return img


def cuadro(id_, t):
    """Cuadro de la escena `id_` en el tiempo global t, con el cambio pintado hacia/desde la escena vecina si t está en una frontera."""
    k = _ORD.index(id_)
    # ¿entra esta escena? (t cerca de su inicio) -> mezcla con la anterior
    if k > 0 and id_ in CAMBIOS:
        tipo, dur, kw = CAMBIOS[id_]
        tb = INI(id_)
        a, b = tb - dur / 2, tb + dur / 2
        if a <= t <= b:
            u = prog(t, a, b)
            nuevo = pintar_escena(id_, t)
            viejo = pintar_escena(_ORD[k - 1], t)
            m, ring = mascara_cambio(tipo, smooth(u) if tipo == "iris" else u, **kw)
            m3 = m[..., None]
            out = viejo.astype(np.float32) * (1 - m3) + nuevo.astype(np.float32) * m3
            out = out * (1 - ring[..., None]) + np.array(COL_BORDE, np.float32) * ring[..., None]
            return out.astype(np.uint8)
    # ¿sale esta escena? -> la escena siguiente aún no tomó el relevo pero ya empezó su cambio
    if k < len(_ORD) - 1 and _ORD[k + 1] in CAMBIOS:
        sig = _ORD[k + 1]
        tipo, dur, kw = CAMBIOS[sig]
        tb = INI(sig)
        a, b = tb - dur / 2, tb + dur / 2
        if a <= t <= b:
            return cuadro(sig, t)
    return pintar_escena(id_, t)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            import sonidos
            for e in sonidos.eventos():
                self.ev(e[0], e[1], e[2], **(e[3] if len(e) > 3 else {}))

    def render(self, lz, t):
        img = cuadro(self.id, t)
        out = img.astype(np.float32) * (1 / 255.0) * vineta()
        return np.clip(out, 0, 1)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
