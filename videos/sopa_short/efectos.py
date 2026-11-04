# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

VIVO_AUTO = 12   # parallax en todas

CAMARA = {
    # "scene-003": dict(a=(1.05, 0, 0), b=(1.33, 0, .3)),      # (zoom, cx, cy) inicial y final
}
FUNDIDO = {
    # "scene-006": 0,                                          # corte seco al entrar a ese beat
}
FX = [
    # 009 y 013 descartadas: el recorte arrastraba la estufa y la freidora
    dict(tipo="vivo", beat="scene-001", anim="baile"),                 # Masako friendo + Ando asomado
    dict(tipo="vivo", beat="scene-011", anim="flota", capa=1),         # los palillos con la tempura partida (el plato se queda)
    dict(tipo="vivo", beat="scene-016", anim="respira"),               # la montaña de tazones
    dict(tipo="vivo", beat="scene-018", anim="respira"),               # el policía soplando la sopa
    # dict(tipo="abre", en=0, dur=.8),
    # dict(tipo="temblor", en="palabras de la voz", amp=34),
    # dict(tipo="destello", en="palabras de la voz"),
    # dict(tipo="latido", de="desde estas palabras", a="hasta estas|fin"),
]
ROTULOS = [
    # dict(texto="DOS PALABRAS", en="palabras de la voz", tam=150, color="amarillo", y=.2),
]
SFX = {
    # "boom": ("Deep cinematic sub boom hit with a long reverb tail", 4),
}
PISTAS = [
    # dict(sfx="boom", en="palabras de la voz", vol=.6),
]
