# -*- coding: utf-8 -*-
"""Escenas de «El caso de la máquina» (estilo noir, nucleo/noir.py): cada módulo esc_*.py es una escena y devuelve el cuadro
completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports)."""
import json as _json

from esc_lluvia import Lluvia
from esc_testigos import Testigos
from esc_sospechoso import Sospechoso
from esc_motivo import Motivo
from esc_apagador import Apagador
from esc_carrera import Carrera
from esc_explosion import Explosion
from esc_final import Final
from esc_duda import Duda
from esc_amanecer import Amanecer

PROPIAS = {"lluvia": Lluvia, "testigos": Testigos, "sospechoso": Sospechoso, "motivo": Motivo, "apagador": Apagador, "carrera": Carrera, "explosion": Explosion, "final": Final, "duda": Duda, "amanecer": Amanecer}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
