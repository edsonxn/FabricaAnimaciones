# -*- coding: utf-8 -*-
"""Reescribe escenas.py con imports ESTÁTICOS de los esc_<id>.py que ya existen (la clase es la única BaseNoir del módulo)."""
import json
import os
import re

AQUI = os.path.dirname(os.path.abspath(__file__))
IDS = [e["id"] for e in json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))["escenas"]]
imp, prop = [], []
for i in IDS:
    p = os.path.join(AQUI, f"esc_{i}.py")
    if not os.path.exists(p):
        continue
    m = re.search(r"^class (\w+)\(BaseNoir\)", open(p, encoding="utf-8").read(), re.M)
    imp.append(f"from esc_{i} import {m.group(1)}")
    prop.append(f'"{i}": {m.group(1)}')
src = '''# -*- coding: utf-8 -*-
"""Escenas de «El gran expediente: Las 1.200 de OpenAI» (estilo NOIR COLOR, nucleo/noir_color.py): cada módulo esc_*.py es una
escena y devuelve el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

%s

PROPIAS = {%s}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
# escenas aún sin hacer: usan la primera clase como relleno (solo para poder renderizar tramos parciales; no se dibujan)
import numpy as _np
import motor as _motor
from basen import BaseNoir as _BaseNoir


class _Relleno(_BaseNoir):
    def armar(self):
        self.plano(self.t0, lambda h, t, u: _np.zeros((_motor.H, _motor.W, 3), _np.float32))


_RELLENO = _Relleno
CLASES = {e["id"]: PROPIAS.get(e["id"], _RELLENO) for e in _TL["escenas"]}
''' % ("\n".join(imp), ", ".join(prop))
open(os.path.join(AQUI, "escenas.py"), "w", encoding="utf-8", newline="\n").write(src)
print(len(imp), "escenas registradas")
