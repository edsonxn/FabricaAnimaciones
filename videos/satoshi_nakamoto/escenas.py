# -*- coding: utf-8 -*-
"""¿Quién es Satoshi Nakamoto? — TABLERO DE DETECTIVE VIVO (ver tablero.py y docs/estilo_documental.md).
Un solo plano secuencia sobre un corcho infinito: la coreografía está en coreo_a.py (origen → perfil), coreo_b.py (Dorian → cierre) y
coreo_c.py (Le Roux, archivo, espejo y el gancho). Todo se ancla a PALABRAS de la voz (ww/pk/INI/FIN)."""
import numpy as np

from kit import *  # noqa: F401,F403
from kit import _sombra_inf
import tablero as T
import piezas as PZ
import coreo_a  # noqa: F401
import coreo_b  # noqa: F401
import coreo_c  # noqa: F401
from coreo_comun import TXT

# papeles de fondo: el corcho nunca se ve vacío (se deja aire alrededor de cada pista)
_LIBRES = [(p.x, p.y, max(p.L.w, p.L.h) * p.s * 0.36) for p in T.PIEZAS]
PZ.relleno(-6300, 6500, -3500, 4100, 470, 7, _LIBRES)


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        for t, n, v, kw in SND:
            self.ev(t, n, v, **kw)

    def render(self, lz, t):
        img = np.zeros((H, W, 3), np.float32)
        T.render_tablero(img, t)
        act = [(a, b, f, s) for a, b, f, s in TXT if a - 0.05 <= t <= b + 0.6]
        if any(s for _, _, _, s in act):
            img *= _sombra_inf()
        for a, b, f, s in act:
            k = 1.0 - smooth(prog(t, b, b + 0.5))
            if k >= 0.999:
                f(img, t)
            else:
                tmp = img.copy()
                f(tmp, t)
                img += (tmp - img) * k
        img = X.cine(img, t, tilt=2.2, vineta=0.62, escaneo=0.11)
        img *= smooth(prog(t, 0.0, 0.6))
        img *= 1.0 - smooth(prog(t, TOTAL - 1.2, TOTAL - 0.1))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
