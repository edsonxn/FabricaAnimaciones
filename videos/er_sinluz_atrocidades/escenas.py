# -*- coding: utf-8 -*-
"""Motor SECUENCIA: aquí no se dibuja nada (el video lo arma nucleo/secuencia.py con los medios de Flow).
Este archivo solo existe para la etapa `sfx`, que pide los efectos de cada escena: por defecto, ninguno.
Para poner un efecto en un momento de la narración, añade eventos a SFX[id_de_escena]:
    SFX = {"gancho": [dict(t=3.2, nombre="suspiro", vol=0.6, pan=0.0)]}      (t = segundo global del video)
"""
import guion

SFX = {}


class _Bloque:
    def __init__(self, e, i):
        self.sfx = list(SFX.get(e["id"], []))


CLASES = {e["id"]: _Bloque for e in guion.ESCENAS}
