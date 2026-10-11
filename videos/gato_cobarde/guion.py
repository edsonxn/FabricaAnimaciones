# -*- coding: utf-8 -*-
"""MOSTACHO Y EL RUIDO DE LA COCINA — dibujo animado de los 90 (ref. «Coraje el perro cobarde»), vertical, 60 s, sin voz.

PRUEBA DE ESTILO «cartoon90» (nucleo/toon.py): cada cuadro se redibuja a mano (tinta que hierve a 12 dibujos/s, formas elásticas,
squash/stretch, smears, acción superpuesta). Sin narración: gags visuales, gritos y música/efectos (como el programa).
Historia (personajes originales, solo se imita el ESTILO):
  Mostacho, un gato flaco y miedoso, duerme frente a la tele con estática en una casa solitaria en medio de la nada.
  Un ruido en la cocina lo despierta. Con linterna y cascabel que delata cada paso cruza el pasillo (retratos que lo siguen con la
  mirada, una sombra que crece). Abre el refri: un ojo enorme lo mira. GRITO, salta al techo. La «Cosa» sale... y resulta que
  tiene tanto miedo como él (o hambre). Remate con iris.
Escenas = secciones musicales (compases de 4 tiempos a 96 BPM = 2,5 s; 24 compases = 60,000 s).
"""

TITULO = "Mostacho y el ruido de la cocina"
ARCHIVO = "mostacho_cocina"
ESTILO_VISUAL = "cartoon90"
FORMATO = "vertical"
SIN_VOZ = True
DURACION = 60.0
BPM = 96
SUBTITULOS = False
MEZCLA = dict(musica=-19.0, sfx=-17.0)

ESCENAS = [
    dict(id="exterior", compases=3, frases=[]),
    dict(id="sala", compases=3, frases=[]),
    dict(id="pasillo", compases=4, frases=[]),
    dict(id="cocina", compases=5, frases=[]),
    dict(id="cosa", compases=5, frases=[]),
    dict(id="final", compases=4, frases=[]),
]
MUSICA = {
    "exterior": dict(sabor="tension", raiz=40),
    "sala": dict(sabor="vacio", raiz=40),
    "pasillo": dict(sabor="tension", raiz=41),
    "cocina": dict(sabor="tension", raiz=40),
    "cosa": dict(sabor="epico", raiz=40),
    "final": dict(sabor="lounge", raiz=41),
}
