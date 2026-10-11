# -*- coding: utf-8 -*-
"""Christa Pike: la ejecución que no terminó — estilo documental v3 (ver docs/estilo_documental.md).
Las tomas están en tomas_a.py (gancho → corredor) y tomas_b.py (debate → cierre); el kit propio en kit_cp.py.
Cada toma se ancla a PALABRAS de la voz (`ww`, `pk`, `INI`, `FIN`), así que nada queda desincronizado cuando cambia la voz."""
from kit_cp import *  # noqa: F401,F403
import tomas_a  # noqa: F401  (registra sus tomas en SHOTS)
import tomas_b  # noqa: F401


class Mundo(Escena):
    def preparar(self):
        if self.idx == 0:
            self.sonidos()

    def sonidos(self):
        e = self.ev
        for t, n, v, kw in SND:
            e(t, n, v, **kw)
        e(INI("cierre", 3) + 0.2, "latido", 0.5, dur=1.4)
        e(FIN("cierre", 3) + 0.9, "apagon", 0.5)

    def render(self, lz, t):
        i = 0
        for k, d in enumerate(SHOTS):
            if d["t0"] <= t:
                i = k
        d = SHOTS[i]
        img = np.zeros((H, W, 3), np.float32)
        dibujar(d, img, t)
        tipo, dur = d["ent"]
        if i > 0 and t < d["t0"] + dur:
            Ab = np.zeros((H, W, 3), np.float32)
            dibujar(SHOTS[i - 1], Ab, t)
            img = X.mezcla2(Ab, img, (t - d["t0"]) / dur, tipo, i)
        img = X.cine(img, t, **d["grado"])
        img *= smooth(prog(t, 0.0, 0.9))
        return np.clip(img, 0, 1).astype(np.float32)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
