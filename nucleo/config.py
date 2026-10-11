# -*- coding: utf-8 -*-
"""Configuración del video activo: lee guion.py (en la carpeta del video) y completa con valores por defecto.

Campos opcionales de guion.py:
  TITULO, ESTILO_VISUAL, DURACION (s o None), BPM (preferido si DURACION es None),
  VOZ = dict(referencia, idioma, exaggeration, cfg_weight, temperature),
  TRANSICIONES = [(tipo, dur), ...], MUSICA = {id_escena: dict(bombo, modo, raiz, sabor)}
Campos opcionales por escena: "pre", "post" (márgenes en s antes/después de la voz).
SIN_VOZ = True: sin voz; cada escena (sección musical) indica "compases": N y "frases": [] (ver linea_tiempo_mudo.py).
"""
import os
import re

import guion as _g

ESCENAS = _g.ESCENAS
# Etiquetas de actuación de ElevenLabs v3 («[sighs] Nadie lo sabía. [short pause] Ni yo.», docs/voz.md § Corchetes): solo las lee
# el TTS. Aquí se separan: FRASES_TTS[clave] guarda la frase con corchetes y ESCENAS queda limpia para Whisper, timeline, .srt y escenas.
_ETIQUETA = re.compile(r"\s*\[[A-Za-z][A-Za-z' -]*\]\s*")
FRASES_TTS = {}
for _e in ESCENAS:
    for _i, _f in enumerate(_e.get("frases") or []):
        if isinstance(_f, str) and _ETIQUETA.search(_f):
            FRASES_TTS[f"{_e['id']}_{_i}"] = _f
            _e["frases"][_i] = _ETIQUETA.sub(" ", _f).strip()
IDS = [e["id"] for e in ESCENAS]
PRIMERA, ULTIMA = IDS[0], IDS[-1]
TITULO = getattr(_g, "TITULO", "Video")
ARCHIVO = getattr(_g, "ARCHIVO", None)          # nombre base de los archivos de salida (opcional)
ESTILO_VISUAL = os.environ.get("FAB_ESTILO") or getattr(_g, "ESTILO_VISUAL", "doodle_psicodelico")
DURACION = getattr(_g, "DURACION", None)
BPM = getattr(_g, "BPM", 120)
GAP = getattr(_g, "GAP", 0.30)                 # pausa (s) entre frases de una escena
SUBTITULOS = getattr(_g, "SUBTITULOS", False)      # REGLA DEL USUARIO (30-sep-2026): sin subtítulos quemados en ningún canal; el .srt sí se genera (para YouTube)
SIN_VOZ = getattr(_g, "SIN_VOZ", False)         # video sin narración: cada escena trae "compases" y no hay frases

VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es", exaggeration=0.8, cfg_weight=0.3,
           temperature=0.8)
VOZ.update(getattr(_g, "VOZ", {}))
# niveles de mezcla (LUFS de partida de música y efectos antes del ducking); opcional en guion.py
MEZCLA = dict(musica=-20.0, sfx=-22.0, fx=-6.0)   # fx = recorte en dB de audio/fx.wav (SFX de ElevenLabs, secuencia con efectos)
MEZCLA.update(getattr(_g, "MEZCLA", {}))

TRANS_DEFECTO = [("garabato", 1.0), ("mancha", 0.8), ("espiral", 0.85), ("glitch", 0.7), ("zoom", 0.9),
                 ("persianas", 0.8), ("derretir", 1.0), ("ola", 0.85), ("burbujas", 0.9), ("iris", 1.0),
                 ("caleido", 0.95), ("pixeles", 0.8)]
_tr = getattr(_g, "TRANSICIONES", None) or []
TRANSICIONES = [(_tr[k] if k < len(_tr) else TRANS_DEFECTO[k % len(TRANS_DEFECTO)]) for k in range(len(ESCENAS) - 1)]

# sabores musicales disponibles (ver musica.py) con su bombo/modo/raíz por defecto
SABORES = {
    "build": dict(bombo="4x4", modo="dorico", raiz=45), "acid": dict(bombo="4x4", modo="dorico", raiz=45),
    "funk": dict(bombo="break", modo="mixolidio", raiz=43), "flauta": dict(bombo="4x4", modo="frigio", raiz=45),
    "epico": dict(bombo="medio", modo="menor", raiz=40), "brillo": dict(bombo="4x4", modo="lidio", raiz=41),
    "disco": dict(bombo="4x4", modo="dorico", raiz=43), "reloj": dict(bombo="4x4", modo="menor", raiz=45),
    "dub": dict(bombo="break", modo="mixolidio", raiz=40), "lounge": dict(bombo="latido", modo="dorico", raiz=41),
    "ambiente": dict(bombo="nada", modo="menor", raiz=40), "final": dict(bombo="4x4", modo="dorico", raiz=45),
    # sabores "documental" (estilo Kurzgesagt): sin bombo, pads + celesta + pulsos suaves
    "espacio": dict(bombo="nada", modo="lidio", raiz=41), "tension": dict(bombo="nada", modo="menor", raiz=40),
    "vacio": dict(bombo="nada", modo="frigio", raiz=40), "esperanza": dict(bombo="nada", modo="lidio", raiz=43),
}
SUAVES = ("ambiente", "espacio", "tension", "vacio", "esperanza")   # sin batería ni golpes de transición fuertes
_ciclo = ["acid", "funk", "flauta", "epico", "brillo", "disco", "reloj", "dub", "lounge"]
_mus = getattr(_g, "MUSICA", {})
MUSICA = {}
for _k, _id in enumerate(IDS):
    if _id in _mus:
        _m = dict(_mus[_id])
    elif _id == PRIMERA:
        _m = dict(sabor="build")
    elif _id == ULTIMA:
        _m = dict(sabor="final")
    else:
        _m = dict(sabor=_ciclo[(_k - 1) % len(_ciclo)])
    MUSICA[_id] = {**SABORES[_m["sabor"]], **_m}
