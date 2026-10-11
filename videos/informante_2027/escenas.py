# -*- coding: utf-8 -*-
"""Escenas de «El informante que le puso fecha al final» (estilo noir, nucleo/noir.py): cada módulo esc_*.py es una escena y
devuelve el cuadro completo. Imports estáticos a propósito (la firma de la vista previa del panel sigue el cierre de imports).
Generado por _reg.py."""
import json as _json

from esc_gancho import Gancho
from esc_cliente import Cliente
from esc_profecia import Profecia
from esc_renuncia import Renuncia
from esc_precio import Precio
from esc_escandalo import Escandalo
from esc_expediente import Expediente
from esc_agentes import Agentes
from esc_robo import Robo
from esc_ejercito import Ejercito
from esc_afuera import Afuera
from esc_mentira import Mentira
from esc_filtracion import Filtracion
from esc_voto import Voto
from esc_carrera import Carrera
from esc_freno import Freno
from esc_dudas import Dudas
from esc_marcador import Marcador
from esc_plan import Plan
from esc_cierre import Cierre

PROPIAS = {"gancho": Gancho, "cliente": Cliente, "profecia": Profecia, "renuncia": Renuncia, "precio": Precio, "escandalo": Escandalo, "expediente": Expediente, "agentes": Agentes, "robo": Robo, "ejercito": Ejercito, "afuera": Afuera, "mentira": Mentira, "filtracion": Filtracion, "voto": Voto, "carrera": Carrera, "freno": Freno, "dudas": Dudas, "marcador": Marcador, "plan": Plan, "cierre": Cierre}

_TL = _json.load(open("timeline.json", encoding="utf-8"))
CLASES = {e["id"]: PROPIAS[e["id"]] for e in _TL["escenas"] if e["id"] in PROPIAS}
