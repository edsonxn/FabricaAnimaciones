# -*- coding: utf-8 -*-
"""Escenas de «El informante que le puso fecha al final» (estilo noir, nucleo/noir.py): cada módulo esc_*.py es una escena y
devuelve el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

from esc_gancho import Gancho
from esc_puerta import Puerta
from esc_interrogatorio import Interrogatorio
from esc_fingir import Fingir
from esc_cierre import Cierre

PROPIAS = {"gancho": Gancho, "puerta": Puerta, "interrogatorio": Interrogatorio, "fingir": Fingir, "cierre": Cierre}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
