# -*- coding: utf-8 -*-
"""Escenas de «El gran expediente: Las 1.200 de OpenAI» (estilo noir, nucleo/noir.py):
cada módulo esc_*.py es una escena y devuelve el cuadro completo.
Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

from esc_gancho import Gancho
from esc_encierro import Encierro
from esc_tareas import Tareas
from esc_pared import Pared
from esc_primer_mensaje import PrimerMensaje
from esc_tablon import Tablon
from esc_jefe import Jefe
from esc_reglas import Reglas
from esc_sacrificio import Sacrificio
from esc_juez import Juez
from esc_asalto import Asalto
from esc_redada import Redada
from esc_caso_2017 import Caso2017
from esc_dialecto import Dialecto
from esc_desconexion import Desconexion
from esc_diplomacia import Diplomacia
from esc_traicion import Traicion
from esc_sandbagging import Sandbagging
from esc_evaluacion_falsa import EvaluacionFalsa
from esc_mundo_exterior import MundoExterior
from esc_taskrabbit import Taskrabbit
from esc_ciego import Ciego
from esc_mentira_consciente import MentiraConsciente
from esc_filosofia_peligro import FilosofiaPeligro
from esc_dos_reglas import DosReglas
from esc_ironia_metr import IroniaMetr
from esc_tablero_final import TableroFinal
from esc_cierre import Cierre

PROPIAS = {"gancho": Gancho, "encierro": Encierro, "tareas": Tareas, "pared": Pared, "primer_mensaje": PrimerMensaje, "tablon": Tablon, "jefe": Jefe, "reglas": Reglas, "sacrificio": Sacrificio, "juez": Juez, "asalto": Asalto, "redada": Redada, "caso_2017": Caso2017, "dialecto": Dialecto, "desconexion": Desconexion, "diplomacia": Diplomacia, "traicion": Traicion, "sandbagging": Sandbagging, "evaluacion_falsa": EvaluacionFalsa, "mundo_exterior": MundoExterior, "taskrabbit": Taskrabbit, "ciego": Ciego, "mentira_consciente": MentiraConsciente, "filosofia_peligro": FilosofiaPeligro, "dos_reglas": DosReglas, "ironia_metr": IroniaMetr, "tablero_final": TableroFinal, "cierre": Cierre}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
