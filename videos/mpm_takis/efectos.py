# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

import os
import mg_tes as T
import mg_planta as P

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
TEMA_PEG = "planta"      # colores: tes · wow · er · gaming · spyro · n64 · pokemon · cod · plasti (peg_estilos.TEMAS)


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


# VARIAS IMÁGENES A LA VEZ (el usuario, 5-nov-2026, TODOS los canales: «nuevas formas de presentar pegatinas, imágenes y
# mapas»): `nucleo/presenta.py`. Cuando la voz ORDENA (tier list, podio), COMPARA (versus), ENUMERA (carrusel, muro) o
# RELACIONA (tablero con hilo rojo). Una marca de la voz por imagen; fondo transparente (el clip sigue debajo).
# fotos = [(slug, "Nombre")]; tier: items = [(slug, "Nombre", "S")]. Tabla: docs/estilo_secuencia_yt.md § PRESENTACIONES.
def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(os.path.join(_PEG, s + ".png"), n) for s, n in fotos]


def tier(items, de, a, marcas, titulo=None, filas=("S", "A", "B", "C", "D")):
    import presenta as PR
    return _pres(PR.tierlist([(os.path.join(_PEG, s + ".png"), n, f) for s, n, f in items], filas, titulo, TEMA_PEG), de, a, marcas, "tier list")


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def tabl(fotos, hilos, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.tablero(_f(fotos), hilos, titulo, TEMA_PEG), de, a, marcas, "tablero")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA_PEG, destaca=destaca, titulo=titulo), de, a, marcas, "muro")


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
TEMA_MAPA = "planta"


# Ampliación 5-nov-2026: entrada="desenrolla"|"pliegue"|"mesa"|"foco" (cómo aparece el mapa; rota entre mapas del video),
# territorios=[dict(poli=[(x, y), …], nombre=…, en=j)] (región que se extiende) y tipo "poder" en un punto (ondas).
def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, tema=None, **kw):
    import mg_mapa as MP
    if kw.get("entrada"):
        fx = mapa.__wrapped__(slug, puntos, de, a, marcas, titulo, sub, ventana, x, y, tema, **kw)
        fx["entra"] = fx["sale"] = .05
        return fx
    return mapa.__wrapped__(slug, puntos, de, a, marcas, titulo, sub, ventana, x, y, tema, **kw)


def _mapa_fx(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, tema=None, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, tema or TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


mapa.__wrapped__ = _mapa_fx


def mg(fn, de, a, marcas=(), x=.5, y=.5, nombre="mg", ver=2.0, sale=.06):
    """MG de mg_planta con ventana de voz (de/a = anclas o (ancla, s))."""
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=sale, nombre=nombre, ver=ver)


def plano(activa, de, a, marcas=(), sub=None):
    """FIRMA: plano de la línea a pantalla completa (estación activa o recorrido con marcas)."""
    return dict(tipo="pantalla", fn=P.plano(ESTACIONES, activa, "Así se fabrica un Taki", sub=sub), de=de, a=a, marcas=list(marcas),
                entra=.4, sale=.4, nombre=f"plano {activa}", ver=3.0)


ESTACIONES = [("Maíz", "silo"), ("Nixtamal", "olla"), ("Molino", "molino"), ("Laminado", "laminadora"), ("Corte", "corte"),
              ("Enrollado", "enrollado"), ("Freidora", "freidora"), ("Sazonado", "tambor"), ("Empaque", "bolsa"),
              ("Cajas y camiones", "camion")]


# ======================================================================================================================
# mpm_takis (sesión 2, 19-nov-2026). Datos: investigacion.md (cada uno con fuente). Clips: metraje.md / fuentes.json.
# OJO: CAMARA solo mueve IMÁGENES, no clips de video (secuencia.py: Imagen sí, Clip no) → los recortes de 019/030/045/106 se
# hicieron con ffmpeg en el propio archivo (originales en medios/_respaldo/*_orig_crop.mp4).
CAMARA = {}
FUNDIDO = {}

from PIL import Image as _Im, ImageDraw as _Dr
import json as _json


def pvr(en, ruta, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    """pv() con una imagen fuera de pegatinas/ (pantallas/, mapas…)."""
    import peg_anim as PA
    fn = PA.variado(ruta, titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + os.path.basename(ruta), ver=1.0)


def _ref_tag():
    """Placa chica «EQUIPO DE REFERENCIA»: el clip es maquinaria del mismo tipo, no la línea de Takis (regla del canal)."""
    f1, f2 = P.fuente("b", 26, "Bold Condensed"), P.fuente("b", 19, "SemiBold Condensed")
    w, h = 420, 64

    def fn(dt, dur, marcas):
        im = _Im.new("RGBA", (w, h), (0, 0, 0, 0))
        d = _Dr.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 6, fill=(15, 18, 22, 190))
        P._franjas(d, 6, 8, 22, h - 8, 255, paso=7)
        P._txt(d, (34, 22), "EQUIPO DE REFERENCIA", f1, P.AMARILLO, "lm")
        P._txt(d, (34, 46), "maquinaria del mismo tipo · no es la línea de Takis", f2, P.HUESO, "lm", 230)
        a = min(P._eo(dt / .4), max(0.0, (dur - dt) / .4))
        return P._bgra(im, a)
    return fn


# beats cuyo clip es maquinaria genérica (Casa Herrera, Heat and Control, How It's Made, Manufacturas Lenin)
_GEN = {"y_XpsXdGO3g", "uQyv9RdIS2Q", "TUDMAlF5AHs", "2-ed6djsAWk", "YkLTUxN0GgU", "jgnDqmJ-mtk"}
_fu = _json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "fuentes.json"), encoding="utf-8"))
_REF = [dict(tipo="mg", fn=_ref_tag(), de=k, a=k + ":fin", x=.15, y=.935, sale=.06, nombre="ref " + k, ver=1.0)
        for k, v in sorted(_fu.items()) if v.get("video") in _GEN and k not in ("scene-025", "scene-113")]


def est(n, nombre, frase, porque, dur_plano=2.6, dur_card=3.6):
    """Estación N: PLANO de la línea (pantalla) al decir «Estación N» y luego la tarjeta con el porqué sobre el clip."""
    return [plano(n - 1, (frase, -.15), (frase, dur_plano), sub=f"Estación {n} de 10 · {nombre}"),
            mg(P.estacion(n, 10, nombre, porque), (frase, dur_plano), (frase, dur_plano + dur_card), x=.30, y=.80,
               nombre=f"estacion {n}")]


FX = [
    # ---------------------------------------------------------------- firma: contador de dólares (todo el video hasta el cierre)
    mg(P.contador_produccion(34.88, "USD", "DE TAKIS VENDIDOS EN EE.UU. DESDE QUE EMPEZÓ ESTE VIDEO",
                             nota="1,100 M USD al año ÷ segundos del año · Circana 2024", prefijo="$"),
       0, ("scene-112:fin", .4), x=.855, y=.085, nombre="contador dolares", ver=1.0),

    # ---------------------------------------------------------------- gancho
    pv("Una bolsa morada", "takis_fuego_bolsa", "Takis Fuego", dur=3.8, x=.80, y=.52, tam=460),
    mg(P.cifra(1100, "$", "", "TAKIS · VENTAS EN EE.UU. EN UN AÑO", texto="$1,100 MILLONES"), ("se vendieron mil cien", -.1),
       ("De rollitos de tortilla|fin", .3), y=.50, nombre="cifra 1100"),
    pvr("una máquina patentada", os.path.join(_PAN, "patente_fig1.jpg"), "Patente de 2001", dur=4.2, x=.78, y=.50, tam=520),
    pv("una empresa de pan", "bimbo_logo", "Grupo Bimbo", dur=3.2, x=.17, y=.60),
    pv("no quiso comprar Sabritas", "sabritas_logo", "Sabritas", dur=3.0, x=.80, y=.55, tam=380),
    vs(("takis_fuego_bolsa", "Takis"), ("doritos_bolsa", "Doritos"), ("terminó inventando la botana", -.1),
       ("le pelea el anaquel a Doritos|fin", .5), ["terminó inventando la botana", "a Doritos"], titulo="El anaquel"),
    plano(None, ("Así que hoy entramos a la planta", -.1), ("realmente un Taki|fin", .2), sub="10 estaciones, del maíz al camión"),
    mg(P.etiqueta("MIRA LA ESQUINA", "dólares de Takis vendidos en EE.UU."), "Mira la esquina", ("desde que empezó este video|fin", .2),
       x=.55, y=.24, nombre="etiqueta esquina"),

    # ---------------------------------------------------------------- quién los hace
    *filav("Barcel, la división", [("barcel_logo", "Barcel", None), ("bimbo_logo", "Grupo Bimbo", "de Grupo Bimbo")], dur=4.2),
    pv("Roberto Servitje, uno de los fundadores", "roberto_servitje", "Roberto Servitje", dur=4.6, x=.78, y=.55, tam=440),
    pv("comprar Sabritas.", "sabritas_logo", "La oferta: Sabritas", dur=3.4, x=.17, y=.62),
    mg(P.etiqueta("UN ERROR", "así lo llamó Roberto Servitje"), "Él mismo lo llamó un error", ("Él mismo lo llamó un error|fin", 1.6),
       x=.42, y=.26, nombre="etiqueta error"),
    pv("Sabritas terminó en manos de PepsiCo", "pepsico_logo", "PepsiCo", dur=3.4, x=.80, y=.58),
    *filav("Lorenzo y Roberto Servitje", [("lorenzo_servitje", "Lorenzo Servitje", None),
                                          ("roberto_servitje", "Roberto Servitje", ("Lorenzo y Roberto Servitje", .6))], dur=4.4),
    mg(P.linea_tiempo("BARCEL DENTRO DE BIMBO", [("AÑOS 70", "Entra al grupo: botanas y dulces"), ("DESPUÉS", "Se separa: solo lo salado")]),
       ("a Barcel en el grupo", -.2), ("dedicarse solo a lo salado|fin", .6), ["a Barcel en el grupo", "Barcel se separó"],
       y=.30, nombre="linea barcel"),
    mg(P.cifra(1999, texto="1999", titulo="NACEN LOS TAKIS"), "Hasta 1999", ("Hasta 1999|fin", 1.4), y=.40, nombre="cifra 1999"),
    pv("Lorenzo Servitje participaba", "lorenzo_servitje", "Lorenzo Servitje", dur=4.0, x=.80, y=.55, tam=420),
    mg(P.etiqueta("TOTOPO ENROLLADO", "la idea que parecía un chiste"), "un totopo enrollado", ("un totopo enrollado|fin", 1.8),
       x=.50, y=.30, nombre="etiqueta totopo"),
    pv("frito y bañado en chile y limón", "takis_original", "Takis", dur=3.6, x=.82, y=.55),
    mg(P.etiqueta("TAQUIS Y TORTIS", "el dicho de la suegra"), "taquis y tortis", ("taquis y tortis|fin", 1.8), x=.50, y=.28,
       nombre="etiqueta taquis"),
    pant("patente_us_registro_taquis", ("en 2001 Grupo Bimbo pidió", -.2), ("la Q se volvió K", .1), zoom=(1.0, 1.12)),
    mg(P.etiqueta("DE TAQUIS A TAKIS"), "la Q se volvió K", ("la Q se volvió K|fin", 1.4), x=.50, y=.30, nombre="etiqueta qk"),
    pv("Y en 2006 llegó el sabor", "takis_fuego_bolsa", "Takis Fuego · 2006", dur=4.6, x=.78, y=.55, tam=440),
    mg(P.etiqueta("2006 · LLEGA A EE.UU."), "Ese mismo año empezó a venderse", ("Ese mismo año empezó a venderse|fin", 1.6), x=.50, y=.26,
       nombre="etiqueta 2006"),
    pv("este es el primer video de Mil por Minuto", "logo_mpm", "Mil por Minuto", dur=4.4, x=.50, y=.50, tam=520),
    mg(P.etiqueta("SUSCRÍBETE", "es gratis"), "suscríbete. Es gratis", ("me ayuda más de lo que crees|fin", .3), x=.50, y=.78,
       nombre="etiqueta suscribete"),

    # ---------------------------------------------------------------- la planta: 10 estaciones
    *est(1, "Maíz", "Estación uno: el maíz", "No trigo ni papa: maíz, como una tortilla"),
    pv("La etiqueta de los Takis en Estados Unidos", "takis_etiqueta_us", "Etiqueta EE.UU.", dur=6.4, x=.74, y=.50, tam=640),
    mg(P.etiqueta("CAL", "la clave de todo"), "cal, es la clave", ("es la clave de todo|fin", 1.0), x=.30, y=.30, nombre="etiqueta cal"),
    *est(2, "Nixtamal", "Estación dos: la nixtamalización", "Maíz cocido en agua con cal, y en reposo"),
    pv("le cambia la química a la masa", "masa_maiz", "Masa de maíz", dur=4.0, x=.80, y=.55),
    *est(3, "Molino", "Estación tres: el molino", "El maíz cocido se muele hasta volverse masa"),
    mg(P.etiqueta("PREDECIBLE", "un lote húmedo descompone todo"), "Tiene que ser predecible", ("Tiene que ser predecible|fin", 2.0),
       x=.50, y=.28, nombre="etiqueta predecible"),
    *est(4, "Laminado", "Estación cuatro: el laminado", "Rodillos de acero: una lámina delgada y continua"),
    *est(5, "Corte", "Estación cinco: el corte", "Forma, tamaño y grosor exactos"),
    mg(P.etiqueta("BANDA MÁS RÁPIDA", "separa las piezas: la masa cruda se pega"), "Para separarlas", ("se pega.|fin", .2), x=.50, y=.26,
       nombre="etiqueta banda"),
    *est(6, "Enrollado", "Estación seis: el enrollado", "La parte que hace a un Taki ser un Taki", dur_card=3.0),
    pant("patente_portada", ("En 2001, una empresa de Grupo Bimbo", -.2), ("en forma de taco|fin", .1), zoom=(1.0, 1.10)),
    pant("patente_fig1", ("Primero, unas mallas de pre-enrollado", -.1), ("colgadas como una cortina", .0), zoom=(1.0, 1.25),
         pan=(0, 0, .1, .05)),
    mg(P.etiqueta("CORTINA DE MALLA", "enrolla en crudo, sin parar"), "colgadas como una cortina", ("hasta cerrar el rollito|fin", .2),
       x=.50, y=.24, nombre="etiqueta cortina"),
    pant("patente_fig1_hoja", ("Los inventores registrados", -.1), ("Peña Sánchez|fin", .3), zoom=(1.0, 1.08)),
    mg(P.cuenta(["ESPIRIDIÓN VALDÉS RODRÍGUEZ", "EFRAÍN JOEL PEÑA SÁNCHEZ"], "PATENTE US 6,393,974 · 2001", titulo="LOS INVENTORES"),
       ("Los inventores registrados", .2), ("Peña Sánchez|fin", .3), ["Espiridión Valdés", "Efraín Joel", ("Peña Sánchez|fin", -.1)],
       x=.70, y=.40, nombre="cuenta inventores"),
    *est(7, "Freidora", "Estación siete: la freidora", "Los rollitos caen al aceite caliente", dur_card=3.0),
    mg(P.ingredientes(["Harina de maíz (procesada con cal)", "Aceite vegetal (palma, soya y/o canola)", "Sazonador"], resalta=(1,),
                      titulo="INGREDIENTES · BOLSA DE EE.UU."), ("La etiqueta habla de aceite", -.1), ("de soya o de canola|fin", 1.0),
       ["aceite de palma"], x=.50, y=.40, nombre="ingredientes aceite"),
    mg(P.etiqueta("CRUJIENTE"), "sale crujiente", ("sale crujiente|fin", 1.2), x=.50, y=.30, nombre="etiqueta crujiente"),
    mapa("norteamerica", [(.6858, .2068, "Coppell, Texas", "meta", None)], "la planta de Barcel en Texas",
         ("para volver a usarlo|fin", .3), ["la planta de Barcel en Texas"], ventana=True, x=.74, y=.36),
    *est(8, "Sazonado", "Estación ocho: el sazonado", "Aquí nace el famoso polvo"),
    mg(P.ingredientes(["Sal", "maltodextrina", "ácido cítrico", "azúcar", "glutamato monosódico", "proteína de soya hidrolizada",
                       "cebolla", "extracto de levadura", "Rojo 40 laca", "Amarillo 6 laca", "sabores", "bicarbonato",
                       "aceite de soya", "chile", "inosinato y guanilato disódico", "TBHQ"], resalta=(2, 8, 9),
                      titulo="SAZONADOR · BOLSA DE EE.UU."),
       ("Sal, maltodextrina", -.2), ("Rojo 40 y Amarillo 6|fin", 1.0), ["ácido cítrico", "dice Rojo 40", "y Amarillo 6"],
       x=.50, y=.42, nombre="ingredientes sazonador"),
    pv("En la de México, además, Amarillo 5", "takis_fuego_bolsa_mx_sellos", "Bolsa de México", dur=5.6, x=.74, y=.50, tam=620),
    mg(P.etiqueta("+ AMARILLO 5", "solo en la bolsa mexicana"), "además, Amarillo 5", ("además, Amarillo 5|fin", 1.6), x=.28, y=.26,
       nombre="etiqueta amarillo5"),
    *est(9, "Empaque", "Estación nueve: el empaque", "Forma la bolsa, la llena y la sella"),
    pv("un consumidor de Nueva York demandó", "corte_manhattan", "Corte federal · Nueva York", dur=5.0, x=.78, y=.52, tam=520),
    mg(P.etiqueta("DEMANDA 2018", "Morrison contra Barcel USA"), "un consumidor de Nueva York demandó", ("demandó a Barcel|fin", 1.5),
       x=.32, y=.24, nombre="etiqueta demanda"),
    mg(P.cifra(64, "", "%", "AIRE EN LA BOLSA, SEGÚN LA DEMANDA", texto="59–64 %"), ("más de la mitad de la bolsa", -.1),
       ("venía vacía|fin", 1.2), y=.42, nombre="cifra aire"),
    mg(P.etiqueta("COLCHÓN DE AIRE", "para que no lleguen hechos polvo"), "es un colchón", ("hechos polvo|fin", .3), x=.50, y=.26,
       nombre="etiqueta colchon"),
    *est(10, "Cajas y camiones", "Estación diez: las cajas y los camiones", "Bolsas, cajas, tarimas y camiones", dur_card=3.4),
    mg(P.cuenta(["BOLSAS A CAJAS", "CAJAS A TARIMAS", "TARIMAS A LA RED DE BIMBO"], "LA MISMA QUE REPARTE EL PAN", titulo="LA SALIDA"),
       ("las bolsas van a cajas", -.1), ("la misma que reparte el pan|fin", .8),
       ["las bolsas van a cajas", "las cajas a tarimas", "las tarimas a la red", "la misma que reparte el pan"],
       x=.70, y=.40, nombre="cuenta salida"),
    mg(P.etiqueta("EL ARMA SECRETA"), "Esa red es el arma secreta", ("el arma secreta|fin", 1.4), x=.50, y=.80, nombre="etiqueta arma"),
    pv("deja también los Takis", "takis_fuego_bolsa", "Takis", dur=3.0, x=.80, y=.55, tam=380),

    # ---------------------------------------------------------------- trivia
    mg(P.trivia("¿Con qué se pintan los Takis Fuego en Europa?", ["A · Rojo 40", "B · Pimentón y cúrcuma", "C · Betabel"]),
       ("Los Takis Fuego que se venden en Europa", -.1), ("Déjalo en los comentarios|fin", .8),
       ["con Rojo 40", "con pimentón", "con betabel"], y=.48, nombre="trivia pregunta"),

    # ---------------------------------------------------------------- el negocio
    mg(P.etiqueta("EL NEGOCIO"), "Ahora, el negocio", ("Venderlo por miles de millones es otra|fin", .2), x=.50, y=.82,
       nombre="etiqueta negocio"),
    mapa("norteamerica", [(.6139, .7754, "Plantas en México", "inicio", None), (.60, .60), (.6141, .4419, "La frontera", "meta", None)],
         "se hacían en México", ("cruzaban la frontera|fin", .8), ["se hacían en México", "cruzaban la frontera"],
         ventana=True, x=.72, y=.40),
    mg(P.etiqueta("PLANTA N.º 100", "de Grupo Bimbo · Mexicali, 2011"), "la planta número cien", ("pensada sobre todo para exportar|fin", .3),
       x=.50, y=.20, nombre="etiqueta planta100"),
    mg(P.cifra(28000, "", "M²", "BARCEL USA · COPPELL, TEXAS · 2012"), ("de unos veintiocho mil", -.2),
       ("donde hoy se hace buena parte", .2), y=.44, nombre="cifra coppell"),
    mg(P.etiqueta("LA PUERTA DE ATRÁS", "tiendas de conveniencia y gasolineras"), "se metieron por la puerta de atrás",
       ("lo que trae en el bolsillo|fin", .3), x=.50, y=.24, nombre="etiqueta puerta"),
    pant("houston_press_2013", ("Ya en 2013 un periódico de Houston", -.2), ("en la primaria", .0), zoom=(1.0, 1.10)),
    vs(("flamin_hot_cheetos", "Primaria"), ("takis_fuego_bolsa", "Secundaria"), ("en la primaria", -.1),
       ("ya mandaban los Takis|fin", .6), ["los Flamin' Hot Cheetos", "ya mandaban los Takis"], ganador=1, titulo="Houston, 2013"),
    mg(P.etiqueta("PREMIO NIELSEN 2014", "innovación en EE.UU."), "ganó el premio de Nielsen", ("ganó el premio de Nielsen", 3.4),
       x=.50, y=.24, nombre="etiqueta nielsen"),
    mg(P.cifra(17000, "", "", "PRODUCTOS NUEVOS EN EE.UU. · SOLO 14 EMPRESAS GANARON", texto="14 de 17,000"),
       ("De más de diecisiete mil", -.1), ("scene-076:fin", .2), y=.44, nombre="cifra nielsen"),
    mg(P.etiqueta("ARE YOU TAKIS ENOUGH?", "el lema en EE.UU."), "Eres lo bastante valiente", ("Era un desafío|fin", .3),
       x=.50, y=.24, nombre="etiqueta lema"),
    mg(P.cifra(400, "$", "", "TAKIS EN EE.UU. · 2020", texto="+$400 MILLONES"), ("En 2020, Takis vendía", -.1),
       ("Cuatro años después", -.05), y=.44, nombre="cifra 400"),
    mg(P.cifra(1100, "$", "", "TAKIS EN EE.UU. · 2024", desde=400, texto="$1,100 MILLONES"), ("Cuatro años después", -.05),
       ("Casi el triple|fin", .5), y=.44, nombre="cifra 400-1100"),
    mg(P.barras("EE.UU. · UN AÑO (MILES DE MILLONES DE USD)", [("Takis", 1.1), ("Doritos", 3.9), ("Tostitos", 1.6)], "", resalta=0),
       ("Para que lo dimensiones", -.1), ("y Tostitos mil seiscientos|fin", 1.2), ["Para que lo dimensiones", "Doritos vendió", "y Tostitos"],
       y=.46, nombre="barras marcas"),
    pv("las marcas de PepsiCo", "pepsico_logo", "PepsiCo", dur=3.2, x=.17, y=.60),
    pv("sus propios rollitos picantes", "doritos_dinamita", "Doritos Dinamita · 2012", dur=4.4, x=.78, y=.55, tam=440),
    mg(P.cifra(2000, "$", "", "TAKIS EN TODO EL MUNDO · SEGÚN LA MARCA", texto="+$2,000 MILLONES"), ("más de dos mil millones", -.2),
       ("scene-084:fin", .2), y=.44, nombre="cifra 2000"),
    pv("Roberto Servitje lo resumió en 2024", "roberto_servitje", "Roberto Servitje · 2024", dur=4.4, x=.80, y=.55, tam=420),
    mg(P.etiqueta("NÚMERO UNO", "el producto que más vende Bimbo"), "Número uno", ("Número uno|fin", 1.8), x=.40, y=.26,
       nombre="etiqueta numero uno"),
    pv("La empresa que no compró Sabritas", "sabritas_logo", "Sabritas", dur=3.4, x=.17, y=.60),

    # ---------------------------------------------------------------- mitos
    mg(P.etiqueta("RUMORES VS. DATOS"), "también llegaron los rumores", ("Vamos a separarlos con datos|fin", .3), x=.50, y=.26,
       nombre="etiqueta rumores"),
    mg(P.etiqueta("FALSO", "úlceras o cáncer · verificadores de datos"), "lo calificaron como falso", ("como falso|fin", 1.8), x=.50, y=.30,
       nombre="etiqueta falso1"),
    mg(P.cifra(100, "", "NIÑOS AL MES", "HOSPITAL INFANTIL · MEMPHIS · 2018"), ("fácilmente cien niños", -.1),
       ("ligados a botanas muy picantes|fin", .4), y=.44, nombre="cifra memphis"),
    pv("La respuesta de Barcel", "barcel_usa_logo", "Barcel USA", dur=4.4, x=.80, y=.55),
    pv("el One Chip Challenge", "paqui_one_chip", "Paqui · One Chip Challenge", dur=5.0, x=.78, y=.52, tam=460),
    mg(P.etiqueta("NO ERA DE TAKIS"), "No era de Takis", ("No era de Takis|fin", 1.6), x=.32, y=.26, nombre="etiqueta noera"),
    mg(P.etiqueta("FALSO", "«Takis mortales» · desmentido en 2025"), "Los verificadores lo desmintieron",
       ("lo desmintieron|fin", 1.6), x=.50, y=.30, nombre="etiqueta falso2"),
    mg(P.cuenta(["ROJO 40", "AMARILLO 5", "AMARILLO 6", "… Y OTROS"], "FUERA DE LA COMIDA ESCOLAR · FIN DE 2027",
                titulo="CALIFORNIA · LEY AB 2316"),
       ("California aprobó una ley", -.1), ("a partir de finales de 2027|fin", 1.0),
       ["saca el Rojo 40", "el Amarillo 5 y", "y el Amarillo 6", "entre otros", "a partir de finales de 2027"],
       x=.70, y=.40, nombre="cuenta california"),
    mg(P.etiqueta("SOLO ESCUELAS", "no prohíbe venderlos en tiendas"), "no prohíbe venderlos", ("no prohíbe venderlos|fin", 1.4), x=.50, y=.26,
       nombre="etiqueta escuelas"),
    pv("Grupo Bimbo prometió", "bimbo_logo", "Grupo Bimbo", dur=4.0, x=.17, y=.60),

    # ---------------------------------------------------------------- mapa completo
    mapa("norteamerica", [(.6139, .7754, "Lerma, Edo. Méx.", "inicio", os.path.join(_PEG, "takis_etiqueta_mx.png")),
                          (.2869, .3756, "Hermosillo, Sonora · 2006", "paso", None),
                          (.1578, .2212, "Mexicali, B. C. · 2011", "paso", None),
                          (.5045, .7205, "Guadalajara, Jalisco · 2013", "paso", None),
                          (.6858, .2068, "Coppell, Texas · 2012", "meta", os.path.join(_PEG, "takis_etiqueta_coppell.png"))],
         ("Hagamos el mapa completo", -.1), ("desde 2012.|fin", .5),
         ["la planta de Lerma", "En Sonora, Hermosillo", "En Baja California, Mexicali", "En Jalisco, Guadalajara", "la planta de Coppell"],
         titulo="Dónde se hacen los Takis", sub="Plantas de Barcel", ajuste=.7),
    mapa("atlantico", [(.2044, .6238, "Coppell, Texas", "inicio", None),
                       (.9028, .2241, "Rotherham, Inglaterra · 2024-2025", "meta", os.path.join(_PAN, "planta_rotherham.jpg"))],
         ("Y del otro lado del océano", -.1), ("para hacer Takis en Europa|fin", .4), ["Y del otro lado del océano", "en Rotherham"],
         titulo="Takis para Europa", sub="Planta nueva en el Reino Unido", ajuste=.8, traza=99, entrada="pliegue"),

    # ---------------------------------------------------------------- cierre
    plano(None, ("piensa en todo lo que pasó", -.1), ("Aceite, polvo rojo y aire|fin", .6),
          marcas=["Maíz cocido con cal", ("Maíz cocido con cal", .7), "Una masa predecible", ("Una masa predecible", .5),
                  ("Una masa predecible", 1.0), "Una cortina de malla", "Aceite, polvo rojo y aire", ("Aceite, polvo rojo y aire", .5),
                  ("Aceite, polvo rojo y aire", 1.0), ("Aceite, polvo rojo y aire", 1.5)], sub="Del maíz a la bolsa morada"),
    mg(P.trivia("¿Con qué se pintan los Takis Fuego en Europa?", ["A · Rojo 40", "B · Pimentón y cúrcuma", "C · Betabel"], correcta=1,
                cabecera="TRIVIA · LA RESPUESTA"),
       ("La respuesta de la trivia#2", -.1), ("se colorean con pimentón y cúrcuma|fin", .4),
       [("La respuesta de la trivia#2", 0), ("La respuesta de la trivia#2", .15), ("La respuesta de la trivia#2", .3), "la B. En Europa"],
       y=.48, nombre="trivia respuesta"),
    vs(("takis_fuego_bolsa", "Europa: pimentón y cúrcuma"), ("takis_fuego_bolsa_mx_sellos", "México: Rojo 40 y Amarillo 6"),
       ("En México, con Rojo 40", -.1), ("dos recetas|fin", .6), ["En México, con Rojo 40", "La misma bolsa"],
       titulo="La misma bolsa"),
    mg(P.etiqueta("CASI $30,000", "vendidos en EE.UU. mientras veías"), "Y el contador de la esquina", ("scene-112:fin", .3),
       x=.62, y=.26, nombre="etiqueta contador final"),
    mg(P.etiqueta("¿QUÉ MARCA SIGUE?", "dímelo en los comentarios"), "dime cuál en los comentarios", ("scene-113:fin", .2),
       x=.50, y=.26, nombre="etiqueta siguiente"),
    pv("Y suscríbete a Mil por Minuto", "logo_mpm", "Suscríbete", dur=5.0, x=.50, y=.48, tam=520),
] + _REF


def _real_tag():
    """Placa chica «LÍNEA REAL DE BARCEL»: metraje auténtico de una planta de Barcel (contraste con EQUIPO DE REFERENCIA)."""
    f1, f2 = P.fuente("b", 26, "Bold Condensed"), P.fuente("b", 19, "SemiBold Condensed")
    w, h = 400, 64

    def fn(dt, dur, marcas):
        im = _Im.new("RGBA", (w, h), (0, 0, 0, 0))
        d = _Dr.Draw(im)
        d.rounded_rectangle((0, 0, w - 1, h - 1), 6, fill=(15, 18, 22, 190))
        d.rectangle((6, 8, 22, h - 8), fill=P.NARANJA + (255,))
        P._txt(d, (34, 22), "PLANTA REAL DE BARCEL", f1, P.NARANJA, "lm")
        P._txt(d, (34, 46), "metraje de Grupo Bimbo / Barcel", f2, P.HUESO, "lm", 230)
        return P._bgra(im, min(P._eo(dt / .4), max(0.0, (dur - dt) / .4)))
    return fn


_REAL = [dict(tipo="mg", fn=_real_tag(), de=k, a=k + ":fin", x=.15, y=.935, sale=.06, nombre="real " + k, ver=1.0)
         for k in ("scene-008", "scene-009", "scene-044", "scene-045", "scene-053", "scene-057", "scene-059", "scene-061", "scene-069")]


def et(texto, sub, de, dur=2.6, x=.50, y=.26):
    return mg(P.etiqueta(texto, sub), de, (de, dur), x=x, y=y, nombre="etiqueta " + texto.lower()[:18])


FX += _REAL + [
    pv("Un rollito de maíz", "takis_original", "Un Taki", dur=3.4, x=.17, y=.62, tam=360),
    et("SOLO EN EE.UU.", "en un año", "Pero solo en Estados Unidos", dur=2.6, y=.72),
    et("¿QUIÉN LOS HACE?", None, "quién los hace", dur=2.6, x=.62, y=.84),
    et("NO LA COMPRARON", None, "Y no la compraron", dur=2.2),
    vs(("barcel_logo", "Barcel"), ("sabritas_logo", "Sabritas"), ("Barcel fue la competencia chica", -.1),
       ("el sueño a Sabritas|fin", .6), ["Barcel fue la competencia chica", "el sueño a Sabritas"], ganador=1, titulo="Antes de 1999"),
    pv("Según Roberto Servitje", "roberto_servitje", "Roberto Servitje", dur=3.6, x=.80, y=.55, tam=380),
    et("PIEZA POR PIEZA", "cómo se fabrican las marcas", "pieza por pieza", dur=3.0),
    et("MILES DE AÑOS", "la técnica de Mesoamérica", "Es la misma técnica", dur=3.4),
    et("POR TONELADAS", "la masa de tu tortillería", "pero por toneladas", dur=2.6),
    et("¿QUÉ HAY EN EL POLVO?", None, "Qué hay en ese polvo", dur=2.2),
    pv("donde hoy se hace buena parte", "takis_etiqueta_coppell", "Hecho en Coppell, Texas", dur=4.4, x=.76, y=.52, tam=560),
    et("DÓNDE LOS VENDIERON", None, "Es dónde los vendieron", dur=3.0),
    et("SUPER BOWL 2024", "el relanzamiento de Doritos Dinamita", "con un anuncio en el Super Bowl", dur=2.8),
    et("MITO 1", "¿úlceras o cáncer?", "Primero: ¿los Takis causan", dur=2.8, x=.30),
    et("REAL: DOLOR DE ESTÓMAGO", "si te comes de más", "Lo que sí es real", dur=3.0),
    et("MEMPHIS · 2018", "un hospital infantil", "Un médico de un hospital infantil", dur=3.0, x=.34, y=.22),
    et("MITO 2", "el chip más picante", "Segundo: el famoso reto", dur=2.8, x=.30),
    et("RETIRADO · 2023", None, "que retiró el producto en 2023", dur=2.4, x=.32),
    et("MITO 3", "«Takis mortales»", "Tercero: en 2025", dur=2.8, x=.30),
    et("MITO 4", "los colorantes", "Y cuarto, los colorantes", dur=2.6, x=.30),
    et("2026 · SIN COLORANTES ARTIFICIALES", "Takis Fuego en EE.UU.", "Y en 2026 Barcel empezó", dur=3.4),
    et("CAMBIANDO DE RECETA", "mientras ves este video", "está cambiando de receta", dur=3.0),
    et("¿DÓNDE? EN LA TRIVIA", None, "Y en otro lugar del mundo", dur=3.0),
    *filav("De una olla con cal", [("maiz_mazorca", "México", None), ("takis_fuego_bolsa", "Texas", "una gasolinera de Texas"),
                                   ("takis_logo", "Londres", "una tienda de Londres")], dur=4.8),
]

ROTULOS = []
SFX = {
    "golpe_metal": ("Heavy industrial metal clank, a factory press stamping once, short", 2),
    "maquina": ("Factory production line ambience, conveyor belts rolling and machines humming, steady loop", 10),
    "freidora": ("Deep fryer sizzling, hot oil bubbling vigorously, close and crisp", 6),
    "caja": ("Cash register ka-ching, bright and short", 2),
    "sello": ("Rubber stamp hitting paper hard, single thud", 1),
}
PISTAS = [dict(sfx="golpe_metal", en=f"Estación {n}", vol=.45) for n in
          ("uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez")]
PISTAS += [dict(sfx="maquina", de="Estación uno: el maíz", a=("Vamos con una pregunta", -.3), vol=.10),
           dict(sfx="freidora", de="Los rollitos caen al aceite", a=("para volver a usarlo|fin", .2), vol=.22),
           dict(sfx="caja", en="se vendieron mil cien", vol=.30), dict(sfx="caja", en="Cuatro años después", vol=.30),
           dict(sfx="caja", en="más de dos mil millones", vol=.28),
           dict(sfx="sello", en="lo calificaron como falso", vol=.40), dict(sfx="sello", en="Los verificadores lo desmintieron", vol=.40),
           dict(sfx="sello", en="la Q se volvió K", vol=.35)]
