# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
Imágenes vivas elegidas el 23-oct mirando previews/vivo_01..04.jpg: fuera las que recortaban mesas, ollas, la máquina, el
cobertizo del museo, la multitud o el humo (016, 020, 033, 038, 041, 051, 054, 062, 073, 081, 087, 089).
"""

VIVO_AUTO = 12   # parallax por profundidad en todas las imágenes

CAMARA = {
}
FUNDIDO = {
}
FX = [
    dict(tipo="vivo", beat="scene-014", anim="respira"),               # las becas a los estudiantes
    dict(tipo="vivo", beat="scene-043", anim="respira", capa=1),       # la esposa mira los fideos (la mesa se queda)
    dict(tipo="vivo", beat="scene-064", anim="respira"),               # la azafata le da las nueces
    dict(tipo="vivo", beat="scene-079", anim="flota"),                 # el astronauta sin gravedad
]
ROTULOS = [
    dict(texto="DOS AÑOS DE CÁRCEL", en="dos años en la cárcel", tam=120, color="amarillo", y=.18),
    dict(texto="1957 · QUIEBRA", en="cincuenta y siete, la cooperativa", tam=130, color="amarillo", y=.18),
    dict(texto="25 · AGOSTO · 1958", en="veinticinco de agosto", tam=120, color="amarillo", y=.18),
    dict(texto="35 YENES", en="treinta y cinco yenes", tam=170, color="amarillo", y=.2),
    dict(texto="1971", en="setenta y uno, con sesenta", tam=170, color="amarillo", y=.2),
    dict(texto="MÁS DE 1 000 MILLONES AL AÑO", en="más de mil millones", tam=110, color="amarillo", y=.18),
]
SFX = {
}
PISTAS = [
]
