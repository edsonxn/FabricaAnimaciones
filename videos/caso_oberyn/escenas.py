# -*- coding: utf-8 -*-
"""Escenas de «El caso de la Víbora Roja» (estilo noir). Mapeo estático a BaseNoir."""
import json as _json

from esc_gancho import Gancho
from esc_testigos import Testigos
from esc_sospechoso import Sospechoso
from esc_motivo import Motivo
from esc_pruebas import Pruebas
from esc_desenlace import Desenlace
from esc_caso_abierto import CasoAbierto

PROPIAS = {
    "gancho": Gancho,
    "testigos": Testigos,
    "sospechoso": Sospechoso,
    "motivo": Motivo,
    "pruebas": Pruebas,
    "desenlace": Desenlace,
    "caso_abierto": CasoAbierto,
}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
