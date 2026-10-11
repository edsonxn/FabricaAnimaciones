# -*- coding: utf-8 -*-
"""Reescribe escenas.py con imports ESTÁTICOS de los esc_<id>.py que ya existen (la clase es la única BaseNoir del módulo)."""
import os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
IDS = [
    "gancho", "encierro", "tareas", "pared", "primer_mensaje", "tablon",
    "jefe", "reglas", "sacrificio", "juez", "asalto", "redada",
    "caso_2017", "dialecto", "desconexion",
    "diplomacia", "traicion", "sandbagging", "evaluacion_falsa",
    "mundo_exterior", "taskrabbit", "ciego", "mentira_consciente",
    "filosofia_peligro", "dos_reglas", "ironia_metr", "tablero_final", "cierre"
]
imp, prop = [], []
for i in IDS:
    p = os.path.join(AQUI, f"esc_{i}.py")
    if not os.path.exists(p):
        continue
    m = re.search(r"^class (\w+)\(BaseNoir\)", open(p, encoding="utf-8").read(), re.M)
    if m:
        imp.append(f"from esc_{i} import {m.group(1)}")
        prop.append(f'"{i}": {m.group(1)}')

src = '''# -*- coding: utf-8 -*-
"""Escenas de «El gran expediente: Las 1.200 de OpenAI» (estilo noir, nucleo/noir.py):
cada módulo esc_*.py es una escena y devuelve el cuadro completo.
Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

%s

PROPIAS = {%s}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
''' % ("\n".join(imp), ", ".join(prop))

open(os.path.join(AQUI, "escenas.py"), "w", encoding="utf-8", newline="\n").write(src)
print(len(imp), f"escenas registradas de {len(IDS)}")
