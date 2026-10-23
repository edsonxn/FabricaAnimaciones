# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""
import os

# MAPAS REALES CON RUTA (el usuario, 23-oct-2026; Warcraft, Runa Caída, Tamriel y Crónicas del gaming): cuando la voz cuente una
# misión (dónde empieza, por dónde vas, dónde acaba) o un lugar que el espectador querría saber DÓNDE está, el mapa REAL del juego
# (mapas/<slug>.jpg|png, de la wiki; coordenadas con `python nucleo/mg_mapa.py rejilla mapas/<slug>.jpg`) con la ruta que se traza
# con las marcas de la voz. Pantalla completa para rutas; `ventana=True` (3-5 s, sobre el clip) para «está aquí». 1-4 por video.
# TEMA_MAPA: "wow" Warcraft · "er" Runa Caída · "tes" Tamriel · "gaming"/"zelda" o uno nuevo con la interfaz de ESE juego.
# Receta: docs/estilo_secuencia_yt.md § MAPAS REALES CON RUTA.
_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas")
TEMA_MAPA = "wow"


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, tema=None, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, tema or TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


CAMARA = {
    # "scene-003": dict(a=(1.05, 0, 0), b=(1.33, 0, .3)),      # (zoom, cx, cy) inicial y final
}
FUNDIDO = {
    # "scene-006": 0,                                          # corte seco al entrar a ese beat
}
FX = [
    # mapa("elwynn", [(.485, .385, "Villanorte"), (.47, .50), (.43, .61, "Villadorada")], de="Todo empieza en Villanorte",
    #      a=("Villadorada|fin", 1.5), marcas=["Villanorte", "Villadorada"], titulo="Bosque de Elwynn"),   # ruta de misión
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
