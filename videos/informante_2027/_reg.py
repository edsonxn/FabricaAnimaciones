# -*- coding: utf-8 -*-
"""Reescribe escenas.py con imports ESTÁTICOS de los esc_<id>.py que ya existen (la clase es la única BaseNoir del módulo)."""
import os, re
AQUI = os.path.dirname(os.path.abspath(__file__))
IDS = ["gancho", "cliente", "profecia", "renuncia", "precio", "escandalo", "expediente", "agentes", "robo", "ejercito", "afuera",
       "mentira", "filtracion", "voto", "carrera", "freno", "dudas", "marcador", "plan", "cierre"]
imp, prop = [], []
for i in IDS:
    p = os.path.join(AQUI, f"esc_{i}.py")
    if not os.path.exists(p):
        continue
    m = re.search(r"^class (\w+)\(BaseNoir\)", open(p, encoding="utf-8").read(), re.M)
    imp.append(f"from esc_{i} import {m.group(1)}")
    prop.append(f'"{i}": {m.group(1)}')
src = '''# -*- coding: utf-8 -*-
"""Escenas de «El informante que le puso fecha al final» (estilo noir, nucleo/noir.py): cada módulo esc_*.py es una escena y
devuelve el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

%s

PROPIAS = {%s}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
''' % ("\n".join(imp), ", ".join(prop))
open(os.path.join(AQUI, "escenas.py"), "w", encoding="utf-8", newline="\n").write(src)
print(len(imp), "escenas registradas")
