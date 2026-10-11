# -*- coding: utf-8 -*-
"""Rasgos del reparto de «¿Quién envenenó al rey?» (nucleo/noir_corte.py). Personajes PROPIOS, sin el aspecto de los actores de
la serie: el mismo rasgo en todo el video para que se reconozcan (corona, toca, collar, perilla, remiendos)."""

REY = dict(pelo="corto", pelo_rampa="oro", pelo_tono=150, corona="rey", ropa=("estandarte", 105), capa=("estandarte", 80),
           joven=True, nariz="pequeña", piel=130)
REINA = dict(pelo="largo", pelo_rampa="oro", pelo_tono=160, corona="diadema", ropa=("estandarte", 95), fem=True, cuello="escote",
             piel=128)
ENANO = dict(pelo="corto", pelo_rampa="oro", pelo_tono=120, barba="rala", ropa=("cuero", 95), alto=0.62, nariz="recta", piel=124)
SANSA = dict(pelo="largo", pelo_rampa="cuero", pelo_tono=120, ropa=("azul", 105), fem=True, cuello="escote", collar=7, falta=3,
             piel=134)
ANCIANA = dict(toca=True, edad=1.0, ropa=("tela_verde", 100), fem=True, nariz="aguileña", piel=122, baston=True)
MENIQUE = dict(pelo="corto", pelo_rampa="lana", pelo_tono=46, barba="perilla", ropa=("lana", 52), nariz="recta", piel=124)
DONTOS = dict(pelo="melena", pelo_rampa="lana", pelo_tono=90, barba="corta", ropa=("estandarte", 120), bufon=True, nariz="aguileña",
              piel=136)
