# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
Imágenes vivas elegidas el 23-oct mirando previews/vivo_01..04.jpg: fuera las que recortaban la mesa, la máquina de rodillos,
el edificio o la cuadrícula de comensales (009, 037, 044, 061, 068, 070, 080, 083, 094).
"""

VIVO_AUTO = 12   # parallax por profundidad en todas las imágenes

CAMARA = {
}
FUNDIDO = {
}
FX = [
    dict(tipo="vivo", beat="scene-016", anim="respira"),               # el doctor muele la galleta
    dict(tipo="vivo", beat="scene-019", anim="balanceo", capa=1),      # el anciano asustado (la mesa se queda)
    dict(tipo="vivo", beat="scene-025", anim="respira"),               # Will paga y contesta el teléfono
    dict(tipo="vivo", beat="scene-027", anim="baile"),                 # el doctor regaña a Will
    dict(tipo="vivo", beat="scene-032", anim="respira", capa=0),       # los hermanos con la olla
    dict(tipo="vivo", beat="scene-042", anim="respira"),               # miran la hojuela a contraluz
    dict(tipo="vivo", beat="scene-046", anim="balanceo", capa=1),      # Will con la libreta junto a la máquina
    dict(tipo="vivo", beat="scene-049", anim="respira"),               # el doctor firma la patente
    dict(tipo="vivo", beat="scene-075", anim="respira"),               # la fila de mujeres del día del guiño
    dict(tipo="vivo", beat="scene-096", anim="balanceo", capa=0),      # las manos sirven el plato
]
ROTULOS = [
    dict(texto="AGOSTO 1894", en="Agosto de mil ochocientos", tam=130, color="amarillo", y=.18),
    dict(texto="¿AZÚCAR?", en="Azúcar", tam=170, color="amarillo", y=.2),
    dict(texto="EL DÍA DEL GUIÑO", en="el día del guiño", tam=130, color="amarillo", y=.18),
    dict(texto="MÉXICO · 1951", en="llegó a México", tam=130, color="amarillo", y=.18),
]
SFX = {
}
PISTAS = [
]
