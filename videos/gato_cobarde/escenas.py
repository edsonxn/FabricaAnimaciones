# -*- coding: utf-8 -*-
"""Escenas de «Mostacho y el ruido de la cocina» (estilo cartoon90, nucleo/toon.py): cada módulo esc_*.py es una escena y dibuja el cuadro
completo (render devuelve float32). Los imports son estáticos a propósito: la firma de la vista previa del panel sigue el cierre de imports."""
import json as _json

from esc_cocina import Cocina
from esc_cosa import Cosa5
from esc_exterior import Exterior
from esc_final import Final
from esc_pasillo import Pasillo
from esc_sala import Sala

PROPIAS = {"exterior": Exterior, "sala": Sala, "pasillo": Pasillo, "cocina": Cocina, "cosa": Cosa5, "final": Final}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"]}
