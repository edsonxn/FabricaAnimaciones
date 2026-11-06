# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

import os
import mg_tes as T

# PEGATINAS — REGLA FIJA DEL CANAL (el usuario, 18-oct-2026): cada personaje, criatura, objeto o prenda que nombre la voz lleva su
# imagen REAL como pegatina animada, ADEMÁS de clips, apoyos y MG (~4 por minuto). Imágenes en pegatinas/<slug>.png (Warcraft:
# API de Wowpedia en Fandom); abajo a la izquierda, en fila (x .13/.30/.47) si la voz enumera; tarjetas a la derecha (x=.72).
# Receta: docs/estilo_secuencia_yt.md § PEGATINAS · ejemplo: videos/wow_curiosidades_reinos_este/efectos.py
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)
# Tamaños variados (18-oct-2026): ~1 de cada 5 GRANDE, media pantalla (x=.25 o .75, y=.50, tam 600-760), del lado contrario a la tarjeta.
# REGLA DE ORO (30-oct-2026): las reglas SUMAN, lo que dice la voz SE VE, ningún clip de otro juego, MG desde el gancho y ≥ 1 de cada 3
# pegatinas en estilo no estándar (`nucleo/peg_estilos.py`: silueta, reliquia, banda, camafeo, legajo, abanico; temas tes/wow/er/gaming).
# Lista: docs/estilo_secuencia_yt.md § REGLA DE ORO · ejemplo: videos/tes_secretos_40/efectos.py · `python fab.py <v> chequeo` antes de `video`.
# CATÁLOGO DE ANIMACIONES (el usuario, 5-nov-2026, TODOS los canales: «muchas más formas para que no se sientan repetidas»):
# usa pv() en vez de peg() para la mayoría: cada pegatina sale con otra combinación de MARCO + ENTRADA + ESTANCIA + SALIDA
# (`nucleo/peg_anim.py`: polaroid que cae, carta que se voltea, tinta, cristal roto, tijera, ventana, ceniza, glitch…) y el
# rotador del video NUNCA repite la misma dos veces seguidas. Fija una parte si el guion lo pide: pv(..., entrada="sello").
# pil() = pila de fotos que se reparte con las marcas de la voz. Tabla: docs/estilo_secuencia_yt.md § CATÁLOGO DE ANIMACIONES.
TEMA_PEG = "wow"      # colores: tes · wow · er · gaming · spyro · n64 · pokemon · cod · plasti (peg_estilos.TEMAS)


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    fn = PA.variado(os.path.join(_PEG, slug + ".png"), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=340, dur=4.6):
    """Fila de pegatinas variadas; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    """Pila de fotos que se reparte (una por marca de la voz); fotos = [(slug, etiqueta)]."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(os.path.join(_PEG, s + ".png"), e) for s, e in fotos], tam, TEMA_PEG, marco), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


# COMENTARIO REAL de quien pidió el tema o corrigió algo (27-oct-2026): `python fab.py yt comentario <v> <canal> <id>` y
# peg(en, "com_<id>", "", tam=760, x=.30, y=.30). Receta: docs/estilo_secuencia_yt.md § COMENTARIOS.


# MOTION GRAPHICS NUEVOS (el usuario, 19-oct-2026; Warcraft, Tamriel y Runa): donde el guion tenga una relación, una
# transformación, una serie, una tríada o una causa → efecto, PROPÓN y programa 2-4 MG propios de ESTE guion en el kit del canal
# (mg_wow / mg_tes / mg_er), además de pegatinas y fichas. NUEVOS y DIFERENTES cada vez (no repetir los ya hechos): que muestren
# mejor esa idea o escena. Nivel de referencia: mg_er.hilos «Los seguidores de Miquella».
# Receta: docs/estilo_secuencia_yt.md § MOTION GRAPHICS NUEVOS · ejemplo: videos/er_miquella_atrocidades/efectos.py


# PANTALLA COMPLETA (el usuario, 18-oct-2026): donde el clip no enseña lo que la curiosidad necesita ver, imagen REAL a cuadro
# entero con zoom/paneo lento (pantallas/<slug>.jpg), DEBAJO de tarjetas y pegatinas. Solo donde de verdad hace falta.
_PAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantallas")


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


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
    # peg("palabras de la voz", "slug", "Nombre"),   # una por personaje/objeto/prenda nombrado (regla de canal)
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
