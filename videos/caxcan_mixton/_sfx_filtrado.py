# -*- coding: utf-8 -*-
"""audio/sfx.wav sin los procedurales que ya tienen versión GRABADA (`_fx_eventos.QUITAR`): filtra escenas.SFX en memoria y
corre nucleo/sfx.py, así no hay que tocar escenas.py (la firma del render). Usar EN LUGAR de `fab.py caxcan_mixton sfx`.
Uso: desde C:\\FabricaAnimaciones, `python videos/caxcan_mixton/_sfx_filtrado.py`."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import escenas  # noqa: E402
import _fx_eventos as EV  # noqa: E402


def quitar(ev):
    t, n = ev[0], ev[1]
    for q, a, b in EV.QUITAR:
        if n == q and (a is None or a <= t <= b):
            return True
    return False


antes = len(escenas.SFX)
escenas.SFX[:] = [e for e in escenas.SFX if not quitar(e)]
print(f"procedurales: {antes} → {len(escenas.SFX)} (quitados {antes - len(escenas.SFX)} con versión grabada)")
import sfx  # noqa: E402

sfx.main()
