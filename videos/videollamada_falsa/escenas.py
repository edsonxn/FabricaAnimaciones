# -*- coding: utf-8 -*-
"""Escenas de «La videollamada donde nadie era real» (estilo noir, nucleo/noir.py): cada módulo esc_*.py es una escena y devuelve
el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports)."""
import json as _json

from esc_regla import Regla
from esc_mensaje import Mensaje
from esc_llamada import LlamadaEsc
from esc_dinero import Dinero
from esc_descubre import Descubre
from esc_truco import Truco
from esc_manual import Manual
from esc_victima import Victima
from esc_sinrostro import SinRostro
from esc_senales import Senales
from esc_leccion import Leccion
from esc_cierre import Cierre

PROPIAS = {"regla": Regla, "mensaje": Mensaje, "llamada": LlamadaEsc, "dinero": Dinero, "descubre": Descubre, "truco": Truco, "manual": Manual, "victima": Victima, "sinrostro": SinRostro, "senales": Senales, "leccion": Leccion, "cierre": Cierre}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
