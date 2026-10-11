# -*- coding: utf-8 -*-
"""Escenas de «¿Quién envenenó al rey?» (estilo noir feudal): cada módulo esc_*.py es una escena y
devuelve el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

from esc_gancho import Gancho
from esc_victima import Victima
from esc_banquete import Banquete
from esc_muerte import Muerte
from esc_acusado import Acusado
from esc_veneno import Veneno
from esc_collar import Collar
from esc_culpables import Culpables
from esc_cierre import Cierre

PROPIAS = {"gancho": Gancho, "victima": Victima, "banquete": Banquete, "muerte": Muerte, "acusado": Acusado, "veneno": Veneno, "collar": Collar, "culpables": Culpables, "cierre": Cierre}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
