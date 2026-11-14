# -*- coding: utf-8 -*-
"""Vuelo 15 de Starship — kit LÍNEA 3D + video real de SpaceX. Todo el cuadro se dibuja en función del tiempo global
(`cuadro(t)`) con planos encadenados por fundidos cortos. Piezas comunes en comun.py; planos en planos1/2/3.py."""
import numpy as np

from comun import TL, TOTAL, F0, T0, pr, smooth, L3, Cam
import planos1 as P1

try:
    import planos2 as P2
except ImportError:
    P2 = None
try:
    import planos3 as P3
except ImportError:
    P3 = None


def _negro(t):
    return L3(Cam((0, -10, 0), (0, 0, 0)))


def _planos():
    p = [(0.0, P1.g_real1), (F0("gancho", 2) - 0.4, P1.g_real2), (F0("gancho", 3) - 0.3, P1.g_real3),
         (F0("gancho", 4) - 0.3, P1.g_captura3d), (F0("gancho", 5) - 0.4, P1.g_booster), (F0("gancho", 6) - 0.4, P1.g_titulo),
         (T0("presenta"), P1.p_mapa), (F0("presenta", 1) - 0.3, P1.p_pila), (F0("presenta", 7) - 0.3, P1.p_carga),
         (F0("presenta", 8) - 0.3, P1.p_meta), (T0("plan"), P1.pl_plan), (T0("despegue"), P1.d_real),
         (F0("despegue", 3) - 0.3, P1.d_abajo), (T0("maxq"), P1.q_maxq), (T0("separa"), P1.s_caliente),
         (F0("separa", 4) - 0.3, P1.s_real)]
    p += P2.PLANOS if P2 else [(T0("propulsor"), _negro)]
    p += P3.PLANOS if P3 else ([(T0("lenta"), _negro)] if P2 else [])
    return p


PLANOS = _planos()
FUNDIDO = 0.3


def cuadro(t):
    idx = max(i for i, (t0, _) in enumerate(PLANOS) if t >= t0 or i == 0)
    img = PLANOS[idx][1](t).final(t)
    if idx > 0 and t < PLANOS[idx][0] + FUNDIDO:
        u = smooth(pr(t, PLANOS[idx][0], PLANOS[idx][0] + FUNDIDO))
        prev = PLANOS[idx - 1][1](t).final(t)
        img = prev * (1 - u) + img * u
    img = img * smooth(pr(t, 0.0, 0.4))
    img = img * (1.0 - smooth(pr(t, TOTAL - 0.6, TOTAL - 0.02)))
    return np.asarray(img, np.float32)


def eventos_sfx():
    v = []
    for m in (P1, P2, P3):
        if m is not None and hasattr(m, "sfx"):
            v += m.sfx()
    return sorted(v)


try:
    from escena_base import Escena  # noqa: E402

    class Mundo(Escena):
        def preparar(self):
            for t, nom, vol, pan, dur in eventos_sfx():
                if self.t0 <= t < self.t1 or (self.idx == 0 and t < self.t0):
                    kw = {"dur": dur} if dur else {}
                    self.ev(t, nom, vol, pan, **kw)

        def render(self, lz, t):
            return cuadro(t)

    CLASES = {e["id"]: Mundo for e in TL["escenas"]}
except Exception:
    CLASES = {}
