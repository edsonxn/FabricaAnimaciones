# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Cómo murió REALMENTE cada villano de Call of Duty» (SECUENCIA YT, Expediente 141, 17-nov-2026).
Helpers de videos/cod_misterios/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta con tema «cod»).
MG propios de este guion: `C.fusion` (dos recuerdos reales → el recuerdo falso: Weaver+Pyle, AUG+MTAR, Downhill+Alpine, Verrückt+Kino)
y `C.caso(..., "falso" | "a_medias")` al cierre de cada puesto. Sonidos nombrados: PISTAS voz=True con sfx/s_*.mp3.
    python fab.py cod_villanos fx --seco   tiempos      FAB_FX_FINAL=1 python fab.py cod_villanos fx hoja   previews/fx_NN.jpg
"""
import os

import mg_cod as C
import mg_wow as W
import peg_estilos as PE

TEMA = "cod"
CAMARA = {}
FUNDIDO = {}

_FX, _FY = .75, .30            # fichas: arriba a la derecha
_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "cod"


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    return os.path.join(_PEG, slug + ".png")


def ficha(en, titulo, texto, tipo=None, dur=4.0, x=.27, y=.28, ancho=640):
    return dict(tipo="mg", fn=C.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=3.4, x=.17, y=.64, tam=380, giro=-5.0):
    return dict(tipo="mg", fn=C.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def pv(en, slug, titulo, dur=3.6, x=.17, y=.62, tam=400, **anim):
    """Pegatina con marco + entrada + estancia + salida que rotan (catálogo 5-nov-2026)."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(P(slug), titulo, tam, tema=TEMA, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(P(s), e) for s, e in fotos], tam, TEMA, marco), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


def sil(en, slug, nombre=None, sub=None, dur=4.2, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=3.8, x=.77, y=.52, tam=440):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.2, x=.16, y=.66, tam=300, foco=(.5, .3, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=460, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=280):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.4, sale=.4,
                nombre="pantalla " + slug, ver=2.0)


def puesto(en, n, titulo, sub, dur=4.2):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=20), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


def mg(fn, de, a, marcas, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def caso(en, estado, titulo, sub=None, dur=3.2, x=.72, y=.26):
    """Veredicto del expediente (MG propio de este guion): al cerrar cada puesto."""
    return mg_en(C.caso(estado, titulo, sub), en, dur, "caso " + titulo, x=x, y=y)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def vid(n, de, a, desde=0.0, recorte=0.0):
    """Corte rápido con OTRO clip ya bajado (medios/scene-NNN.mp4) a cuadro entero (va PRIMERO en FX)."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                recorte=recorte, entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    fx = dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)
    if kw.get("entrada"):
        fx["entra"] = fx["sale"] = .05
    return fx


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def tabl(fotos, hilos, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.tablero(_f(fotos), hilos, titulo, TEMA), de, a, marcas, "tablero")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA, titulo), de, a, marcas, "versus")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA, destaca=destaca, titulo=titulo), de, a, marcas, "muro")





# ------------------------------------------------------------------ MG propios de este guion (17-nov-2026)
def _ll(lat, lon, rec):
    """lat/lon reales → fracción del mapa equirectangular recortado (mapas/mundo.jpg, NASA)."""
    x, y = (lon + 180) / 360, (90 - lat) / 180
    return (x - rec[0]) / (rec[2] - rec[0]), (y - rec[1]) / (rec[3] - rec[1])


def _sagas():
    return [("MODERN WARFARE", [(P(s), n) for s, n in [("zakhaev", "Zakhaev"), ("alasad", "Al-Asad"), ("victor", "Victor"),
                                                      ("shepherd", "Shepherd"), ("makarov", "Makarov")]]),
            ("BLACK OPS", [(P(s), n) for s, n in [("dragovich", "Dragovich"), ("kravchenko", "Kravchenko"), ("steiner", "Steiner"),
                                                 ("menendez", "Menéndez"), ("perseus", "Perseus"), ("harrow", "Harrow")]]),
            ("REINICIO", [(P(s), n) for s, n in [("wolf", "El Lobo"), ("barkov", "Barkov"), ("hassan", "Hassan"), ("graves", "Graves"),
                                                ("makarov_r", "Makarov 2023")]]),
            ("OTROS", [(P(s), n) for s, n in [("amsel", "Amsel"), ("rorke", "Rorke"), ("irons", "Irons"), ("kotch", "Kotch"),
                                             ("richtofen", "Richtofen")]])]


def bajas(de, a, tachados=(), foco=None, marca=None, titulo="20 VILLANOS · 20 EXPEDIENTES"):
    return dict(tipo="mg", fn=C.bajas(_sagas(), tachados, foco, titulo, w=1640, lado=128), de=de, a=a,
                marcas=[marca] if marca else [], x=.5, y=.50, sale=.35, nombre="MG bajas " + (foco or "gancho"), ver=3.0)


def acta(nombre, slug, filas, estado, sub, de, a, marcas=None, x=.5, y=.46):
    """Marcas automáticas (17-nov-2026, hoja fx: el sello quedaba fuera del tramo): fila cada 0,45 s desde `de`, sello al final."""
    t, o = (de, 0.0) if isinstance(de, str) else de
    marcas = [(t, o + .35 + .45 * i) for i in range(len(filas) + 1)]
    return dict(tipo="mg", fn=C.acta(nombre, P(slug), filas, estado, sub, w=1120), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="MG acta " + nombre, ver=3.0)


def com(en, cid, dur=5.0, x=.30, y=.30, tam=760):
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam, giro=-2.0)


def puesto(en, n, titulo, sub, dur=4.2):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=20), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


MUERTOS = []   # se llena en orden: el tablero de cada tramo tacha a los anteriores


REC_K = (.653, .25, .833, .472)          # Indochina → Afganistán
REC_Z = (.542, .111, .778, .361)         # Ucrania → Altái
REC_M = (.236, .10, .708, .567)          # Nueva York ↔ Dubái

FX = [
    # cortes que tapan lo que sigue a cada cita (violencia: nunca el disparo; lección de cod_mandela2)
    vid(45, "No estamos atacando", ("Ghost no lo deja", -.05), desde=0.5),        # Hassan: antes del disparo de Ghost
    # ---------------- gancho: elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.30, y=.40),
    leg("c_cod4", "EXPEDIENTE 141 · VILLANOS", ["Asunto: los villanos", "Causa de muerte REAL", "20 expedientes"],
        de="Asunto: los villanos", a=("Uno murió a puñetazos", -.1), x=.78, y=.50),
    pv("a puñetazos en un callejón", "makarov_r", "Makarov · MW4", dur=2.6, x=.80, y=.60, tam=330),
    pv("colgado de un cable", "makarov", "Makarov · Dubái", dur=2.6, x=.18, y=.62, tam=330),
    sil("sigue vivo, aunque", "rorke", "Rorke", "Sigue vivo", lado="der", dur=3.0),
    mg_en(C.marcador("Magnum .44", 1, "Una sola bala"), "le dispararon con un Magnum", 2.2, "marcador magnum", x=.40, y=.40),
    cam("lo viste morir con tus propios", "steiner", "Steiner", dur=2.8, x=.16, y=.66),
    mg_en(C.fallida("EL JUEGO TE MINTIÓ", "Sobre quién lo mató"), "el juego te mintió", 2.4, "fallida mintio"),
    bajas("Veinte villanos, cada muerte", ("Aviso: hay spoilers", -.2)),
    mg_en(C.radio("EXPEDIENTE 141", "Spoilers de Modern Warfare 4", "AVISO / CANAL TÁCTICO"), "Aviso: hay spoilers", 2.6,
          "radio spoilers", x=.5, y=.24),
    pv("un villano que tuvo que morir dos veces", "c_mw3", "¿Dos veces?", dur=2.6, x=.82, y=.62, tam=280),

    # ---------------- 20 · Amsel
    puesto("Número veinte. El general", 20, "Heinrich Amsel", "CAMPAÑA / WORLD AT WAR · 2008"),
    rel("Stalingrado, misión Vendetta", "amsel", "Heinrich Amsel", "Stalingrado · 1942", dur=3.6, x=.78, y=.50, tam=400),
    pv("Reznov y Dimitri Petrenko", "reznov", "Viktor Reznov", dur=2.8, x=.18, y=.60, tam=300),
    pv("dos francotiradores rusos", "petrenko", "Dimitri Petrenko", dur=2.8, x=.80, y=.62, tam=300),
    mg_en(C.objetivo("Elimina al general Amsel", "Vendetta · Stalingrado"), "Amsel huye de su cuartel", 2.8, "objetivo amsel",
          x=.30, y=.82),
    ficha("el Mosin-Nagant que le dio", "Mosin-Nagant", "Fusil con mira *de Reznov*.", "INTEL / VENDETTA", dur=3.2),
    mg_en(C.balanza("¿Por qué no disparó Reznov?", [("Tenía la venganza", True, "sí"), ("Tenía el dedo del gatillo", False, "se lo volaron")]),
          "por qué no disparó Reznov", 3.0, "balanza reznov", y=.50),
    acta("Heinrich Amsel", "amsel", [("AUTOR", "Dimitri Petrenko"), ("ARMA", "Mosin-Nagant de Reznov"), ("MISIÓN", "Vendetta · 1942")],
         "confirmado", "Reznov se ríe", de="Porque los alemanes", a=("En el diecinueve", -.1),
         marcas=[("El del gatillo|fin", .0), ("El del gatillo|fin", .5), ("El del gatillo|fin", 1.0), ("El del gatillo|fin", 1.6)]),

    # ---------------- 19 · Al-Asad
    puesto("En el diecinueve, Khaled", 19, "Khaled Al-Asad", "CAMPAÑA / CALL OF DUTY 4 · 2007"),
    pv("Call of Duty 4, dos mil siete", "c_cod4", "Call of Duty 4 · 2007", dur=2.4, x=.86, y=.80, tam=220),
    sil("El hombre que ejecutó al presidente", "alasad", "Al-Asad", "El golpe de Estado", lado="der", dur=4.0),
    mg_en(C.radio("TRANSMISIÓN", "«This is how it begins»", "TV ESTATAL / THE COUP"), "delante de una cámara", 3.0, "radio coup",
          x=.5, y=.24),
    pv("Price lo tiene atado", "price", "Capitán Price", dur=2.8, x=.18, y=.62, tam=310),
    mg_en(C.objetivo("Interroga a Al-Asad", "Casa franca · Azerbaiyán"), "y lo interroga", 2.4, "objetivo interroga", x=.30, y=.82),
    mg_en(C.marcador("Teléfono", 1, "Llamada entrante"), "suena el teléfono de Al-Asad", 3.2, "marcador telefono", x=.55, y=.36),
    pv("Del otro lado está Imran Zakhaev", "zakhaev", "Imran Zakhaev", dur=3.0, x=.80, y=.60, tam=330),
    mg_en(C.espejo("Atado a una silla", ("AL-FULANI", "The Coup", ["Atado a una silla", "Un tiro, ante la cámara"], None),
                   ("AL-ASAD", "Casa franca", ["Atado a una silla", "Un tiro, la M1911 de Price"], None), "MISMO FINAL"),
          "Murió exactamente como mató", 5.0, "espejo silla", x=.5, y=.40),
    ficha("la bomba que mató a treinta", "La bomba nuclear", "30 000 marines · *por orden de Makarov*.", "INTEL / MW3 REVELA", dur=3.6),
    pv("Por orden de Makarov", "makarov", "Makarov", dur=2.8, x=.18, y=.62, tam=300),
    acta("Khaled Al-Asad", "alasad", [("AUTOR", "John Price"), ("ARMA", "M1911"), ("MISIÓN", "Casa franca · CoD 4")], "confirmado",
         "Atado a una silla", de="Eso no lo supimos", a=("Número dieciocho", -.1),
         marcas=[("hasta Modern Warfare 3|fin", -.2), ("hasta Modern Warfare 3|fin", .3), ("hasta Modern Warfare 3|fin", .8),
                 ("hasta Modern Warfare 3|fin", 1.4)]),

    # ---------------- 18 · Victor
    puesto("Número dieciocho. Victor", 18, "Victor Zakhaev", "CAMPAÑA / LOS PECADOS DEL PADRE"),
    cam("el hijo del ultranacionalista", "victor", "Victor Zakhaev", dur=3.0, x=.16, y=.34),
    aba([("soap", "Soap"), ("gaz", "Gaz"), ("price", "Price")], de="Soap, Gaz y Price", a=("hasta la azotea", .3),
        marcas=["Soap", "Gaz", "Price persiguen"], nombre="abanico 141", x=.78, y=.62),
    mg_en(C.marcador("Azotea", 25, "Cinco pisos"), "hasta la azotea de un edificio", 2.6, "marcador azotea", x=.5, y=.30),
    ficha("la versión oficial del Pentágono", "Versión oficial", "«Accidente de coche» en *Volgogrado*.", "INTEL / PENTÁGONO · MW2", dur=4.0),
    acta("Victor Zakhaev", "victor", [("CAUSA", "Su propia M1911"), ("LUGAR", "Una azotea · Volgogrado")], "confirmado",
         "Versión oficial: un coche", de="Un accidente de coche. En", a=("En el diecisiete", -.05),
         marcas=[("En una azotea|fin", -.4), ("En una azotea|fin", .1), ("En una azotea|fin", .6)], y=.42),

    # ---------------- 17 · El Lobo
    puesto("En el diecisiete, Omar", 17, "Omar «El Lobo» Sulaman", "CAMPAÑA / MODERN WARFARE · 2019"),
    pv("En el Modern Warfare de dos mil diecinueve", "c_mw19", "Modern Warfare · 2019", dur=2.4, x=.86, y=.80, tam=220),
    rel("el terrorista más buscado", "wolf", "El Lobo", "Urzikstán", dur=3.6, x=.78, y=.50, tam=400),
    mg_en(C.objetivo("Encuentra al Lobo", "La guarida del Lobo"), "En La guarida del Lobo", 2.6, "objetivo lobo", x=.30, y=.82),
    mg_en(C.objetivo("Corta el cable verde", "Chaleco bomba · cuenta atrás"), "hay que cortar el cable verde", 3.0, "objetivo chaleco",
          x=.30, y=.82),
    vs(("wolf", "El Lobo"), ("hadir", "Hadir"), de="el robo del gas no", a=("el hermano de Farah", .5), marcas=["no lo planeó el Lobo", "Lo planeó Hadir"],
       ganador=1, titulo="¿Quién robó el gas?"),
    acta("Omar Sulaman", "wolf", [("CAUSA", "Un disparo a la cabeza"), ("TENÍA", "Chaleco bomba armado")], "confirmado",
         "Con el crimen de otro", de="El Lobo murió con el crimen", a=("Número dieciséis", -.1),
         marcas=["El Lobo murió", "con el crimen", "en su ficha"], y=.42),

    # ---------------- 16 · Barkov
    puesto("Número dieciséis. El general", 16, "Roman Barkov", "CAMPAÑA / EN EL HORNO"),
    sil("El general ruso que invadió", "barkov", "Barkov", "Ejército ruso", lado="izq", dur=4.4),
    mg_en(C.radio("MOSCÚ", "…", "SIN RESPUESTA / CANAL DE MANDO"), "Moscú deja de contestarle", 2.8, "radio moscu", x=.62, y=.24),
    mg_en(C.marcador("Helicóptero", 20, "Lo pilota Nikolai"), "escapa en su propio helicóptero", 3.0, "marcador helo", x=.55, y=.32),
    pv("Farah sube a bordo", "farah", "Farah Karim", dur=2.8, x=.80, y=.62, tam=310),
    ficha("Sus últimas palabras", "Últimas palabras", "«Debí hacer *más*».", "INTEL / EN EL HORNO", dur=3.4),
    mg_en(C.logro("Sin ascenso", "Charreteras de coronel, no de general"), "lleva charreteras de coronel", 3.2, "logro charreteras",
          x=.5, y=.84),
    acta("Roman Barkov", "barkov", [("AUTOR", "Farah Karim"), ("ARMA", "Cuchillo"), ("LUGAR", "Su propio helicóptero")], "confirmado",
         "Murió sin el ascenso", de="Y un detalle del expediente", a=("En el quince, Jonathan", -.05),
         marcas=[("Murió sin el ascenso|fin", -1.0), ("Murió sin el ascenso|fin", -.6), ("Murió sin el ascenso|fin", -.2),
                 ("Murió sin el ascenso|fin", .2)], y=.42),
    bajas(("En el quince, Jonathan", -.1), ("Advanced Warfare. El dueño", 0), tachados=("Amsel", "Al-Asad", "Victor", "El Lobo"),
          foco="Barkov", marca=("En el quince, Jonathan", .3), titulo="BAJAS CONFIRMADAS"),

    # ---------------- 15 · Irons
    puesto("Advanced Warfare. El dueño", 15, "Jonathan Irons", "CAMPAÑA / ADVANCED WARFARE · 2014"),
    rel("El dueño de Atlas", "irons", "Jonathan Irons", "Atlas Corporation", dur=3.6, x=.78, y=.50, tam=400),
    pv("le dio a Jack Mitchell un brazo", "mitchell", "Jack Mitchell", dur=3.0, x=.18, y=.60, tam=310),
    ficha("después de que perdiera el suyo", "El brazo de Mitchell", "Prótesis de *Atlas*, tras Seúl.", "INTEL / ATLAS", dur=3.4),
    mg_en(C.objetivo("Detén a Irons", "Terminal · Nueva Bagdad"), "Misión final, Terminal", 2.4, "objetivo irons", x=.30, y=.82),
    mg_en(C.radio("IRONS", "«I gave you that arm»", "AUDIO / TERMINAL"), ("Del brazo artificial. Escucha|fin", .2), 4.0,
          "radio irons", x=.5, y=.24),
    ficha("Y Mitchell se lo corta", "Le devuelve el brazo", "Lo corta con *su propio cuchillo*.", "INTEL / TERMINAL", dur=3.4),
    com("la voz es IA, nomás", "UgxMmZO1yx8ruCS7b_t4AaABAg", dur=5.0, x=.33, y=.30),
    mg(C.espejo("Artificial", ("LA VOZ", "Expediente 141", ["Artificial"], None), ("EL BRAZO", "Jack Mitchell", ["Artificial", "Acabó con Irons"], None),
                "HACEN EL TRABAJO"), "Mitchell también tenía un brazo", ("Lo artificial también hace", -.15), [], "espejo artificial", y=.40),
    acta("Jonathan Irons", "irons", [("CAUSA", "La caída"), ("AUTOR", "Jack Mitchell"), ("ARMA", "El brazo que Irons le dio")],
         "confirmado", "Lo artificial hace el trabajo", de="Lo artificial también hace", a=("Número catorce", -.05),
         marcas=[("hace el trabajo|fin", -1.2), ("hace el trabajo|fin", -.8), ("hace el trabajo|fin", -.4), ("hace el trabajo|fin", .0)],
         y=.42),

    # ---------------- 14 · Kotch
    puesto("Número catorce. El almirante", 14, "Salen Kotch", "CAMPAÑA / INFINITE WARFARE · 2016"),
    pv("Infinite Warfare, dos mil dieciséis", "c_iw", "Infinite Warfare · 2016", dur=2.4, x=.86, y=.80, tam=220),
    vs(("kotch", "Salen Kotch"), ("kit_harington", "Kit Harington"), de="interpretado por Kit Harington", a=("de Juego de Tronos|fin", .6),
       marcas=["interpretado por", "el Jon Snow"], titulo="El villano y su actor"),
    pv("Reyes lo acorrala", "reyes", "Nick Reyes", dur=2.8, x=.18, y=.60, tam=300),
    ficha("le suelta el discurso", "Último discurso", "«Matarme *no es ganar*».", "INTEL / BANDERA NEGRA", dur=3.2),
    mg_en(C.logro("You Know Nothing", "Interrumpe el discurso de Kotch"), "el juego te da un logro", 3.6, "logro you know", x=.5, y=.84),
    mg_en(C.linea("Las operaciones de Infinite Warfare", [("6.ª", "Bandera Negra", "Muere Kotch"), ("7.ª", "Tormenta de Sangre", "Marte, sin él")],
                  h=400), "Muere en la sexta operación", 4.2, "linea operaciones", x=.5, y=.30),
    com("Como qtdrox, que escribió", "UgxBZqOspRcF59gChr54AaABAg", dur=5.6, x=.33, y=.30),
    acta("Salen Kotch", "kotch", [("AUTOR", "Nick Reyes"), ("ARMA", "Robot + cuchillo"), ("CUÁNDO", "Operación 6 de 7")], "confirmado",
         "No llegó al final", de="Kotch tampoco terminó", a=("En el trece, Hassan", -.05),
         marcas=[("el final en Marte|fin", -.8), ("el final en Marte|fin", -.4), ("el final en Marte|fin", .0), ("el final en Marte|fin", .4)],
         y=.42),

    # ---------------- 13 · Hassan
    puesto("En el trece, Hassan", 13, "Hassan Zyani", "CAMPAÑA / MODERN WARFARE II · 2022"),
    pv("Modern Warfare 2, dos mil veintidós", "c_mw22", "Modern Warfare II · 2022", dur=2.4, x=.86, y=.80, tam=220),
    sil("Hassan arrastra a Soap", "hassan", "Hassan", "Al-Qatala", lado="izq", dur=4.0),
    mg_en(C.marcador("Ventana", 3, "Acaba de volar"), "hacia una ventana que acaba", 2.6, "marcador ventana", x=.55, y=.36),
    mg_en(C.radio("HASSAN", "«We are not attacking… We are invading»", "AUDIO / COUNTDOWN"), ("su amenaza final. Escucha|fin", .2),
          5.0, "radio hassan", x=.5, y=.24),
    pv("Ghost no lo deja decir", "ghost", "Ghost", dur=3.0, x=.80, y=.60, tam=320),
    mg_en(C.objetivo("Tiro perfecto, teniente", "Francotirador desde enfrente", completo=True), "lo derriba con un francotirador", 3.0,
          "objetivo ghost", x=.30, y=.82),
    acta("Hassan Zyani", "hassan", [("AUTOR", "Simon «Ghost» Riley"), ("ARMA", "Francotirador"), ("MISIÓN", "Countdown · Chicago")],
         "confirmado", "Amenazó a un escocés", de="Lo mejor: Hassan amenaza", a=("Número doce", -.05),
         marcas=[("Soap es escocés|fin", -.4), ("Soap es escocés|fin", .0), ("Soap es escocés|fin", .4), ("Soap es escocés|fin", .9)]),

    # ---------------- 12 · Rorke
    puesto("Número doce. Gabriel Rorke", 12, "Gabriel Rorke", "CAMPAÑA / GHOSTS · 2013"),
    pv("En Call of Duty Ghosts", "c_gh", "Ghosts · 2013", dur=2.4, x=.86, y=.80, tam=220),
    rel("el antiguo líder de los Ghosts", "rorke", "Gabriel Rorke", "El cazador de Ghosts", dur=3.6, x=.78, y=.50, tam=400),
    pv("Hesh lo sujeta", "hesh", "Hesh", dur=2.6, x=.18, y=.60, tam=290),
    pv("y Logan le dispara", "logan", "Logan", dur=2.6, x=.80, y=.62, tam=290),
    mg_en(C.marcador("Magnum", 1, "Una sola bala"), "un Magnum que tiene una sola", 2.6, "marcador bala", x=.5, y=.34),
    mg_en(C.fallida("OBJETIVO VIVO", "Rorke se levanta en la orilla"), "Rorke se levanta", 2.4, "fallida rorke"),
    mg_en(C.marcador("Pozo", 0, "Amazonas"), "en un pozo en el Amazonas", 2.8, "marcador pozo", x=.5, y=.40),
    acta("Gabriel Rorke", "rorke", [("DISPARO", "Magnum, una sola bala"), ("AUTOR", "Logan Walker")], "sobrevivio",
         "Nunca hubo segunda parte", de="Y nunca salió una segunda", a=("En el once, Edward", -.05),
         marcas=["Y nunca salió", "una segunda parte", "Rorke no murió"], y=.42),

    # ---------------- 11 · Richtofen
    puesto("En el once, Edward", 11, "Edward Richtofen", "ZOMBIES / LA HISTORIA DEL ÉTER"),
    cam("El doctor de los Zombies", "richtofen", "Richtofen", dur=3.0, x=.16, y=.34),
    mg_en(C.espejo("Dos Richtofen", ("PRIMIS", "The Giant · BO3", ["Sale del teletransportador", "Dispara"], None),
                   ("ULTIMIS", "The Giant · BO3", ["Su otra versión", "Muere"], None), "EL MISMO HOMBRE"),
          "su versión de Primis sale", 6.0, "espejo richtofen", x=.5, y=.40),
    ficha("Todos alrededor de una fogata", "Tag der Toten", "La fogata · *todos envenenados*.", "INTEL / BLACK OPS 4", dur=3.6),
    mg_en(C.radio("RICHTOFEN", "«Lo sé. Y lo siento mucho»", "AUDIO / TAG DER TOTEN"), "Richtofen dice: lo sé", 3.2, "radio richtofen",
          x=.5, y=.24),
    acta("Edward Richtofen", "richtofen", [("AUTOR", "Nikolai, su amigo"), ("ARMA", "Revólver"), ("POR QUÉ", "Cerrar el multiverso")],
         "confirmado", "No lo mató un zombi", de="No lo mató un zombi", a=("Número diez. Perseus", -.05),
         marcas=["No lo mató", "un zombi", "Lo mató su", ("Lo mató su amigo|fin", .1)], y=.42),

    # ---------------- 10 · Perseus
    puesto("Número diez. Perseus", 10, "Perseus", "CAMPAÑA / BLACK OPS COLD WAR · 2020"),
    pv("Black Ops Cold War, dos mil veinte", "c_cw", "Cold War · 2020", dur=2.4, x=.86, y=.80, tam=220),
    sil("El espía soviético", "perseus", "Perseus", "Espía soviético", lado="der", dur=4.0),
    mg_en(C.balanza("Los finales de Cold War", [("Final bueno", False, "Perseus escapa"), ("Final malo", False, "se burla de Adler")]),
          "En ningún final lo matas", 6.0, "balanza perseus", y=.50),
    pv("se burla del cadáver de Adler", "adler", "Russell Adler", dur=2.6, x=.18, y=.62, tam=300),
    mg_en(C.contador(1983, "", "MUERE DE CÁNCER", desde=1960), "De cáncer, en mil novecientos", 2.8, "contador 1983", x=.30, y=.30),
    ban("Adler encuentra a Stitch", "adler", "Adler", "Temporada 6", foco=(.5, .3, 1.8), dur=3.6),
    com("Y leukojb me preguntó", "UgxsmSKehGcvUGYRLAR4AaABAg", dur=4.6, x=.33, y=.30),
    pv("si Bell está muerto", "bell", "Bell", dur=3.0, x=.88, y=.80, tam=240),
    acta("Perseus", "perseus", [("CAUSA", "Cáncer · 1983"), ("REVELADO", "Temporada 6 · Verdansk")], "sin_cuerpo", "Era una idea",
         de="Buena pregunta", a=("En el nueve, Jane", -.05),
         marcas=["Esa da para", "un expediente", ("expediente entero|fin", .1)], y=.42),

    # ---------------- 9 · Harrow
    puesto("En el nueve, Jane", 9, "Jane Harrow", "CAMPAÑA / BLACK OPS 6 · 2024"),
    pv("Black Ops 6, dos mil veinticuatro", "c_bo6", "Black Ops 6 · 2024", dur=2.4, x=.86, y=.80, tam=220),
    rel("La espía que traicionó", "harrow", "Jane Harrow", "El Panteón", dur=3.6, x=.78, y=.50, tam=400),
    pv("Case la sujeta bajo el agua", "case", "Case", dur=2.8, x=.18, y=.60, tam=300),
    mg_en(C.radio("¿?", "«Termínalo»", "VOZ EN SU CABEZA / TOXINA CRADLE"), "una voz le dice", 2.8, "radio terminalo", x=.5, y=.24),
    mg_en(C.fallida("SEÑAL PERDIDA", "La pantalla se va a negro"), "la pantalla se va a negro", 2.6, "fallida negro"),
    vs(("harrow", "Jane Harrow"), ("adler", "Russell Adler"), de="Harrow descubre que Adler", a=("Todo su odio venía", -.15),
       marcas=["Harrow descubre", "no mató a sus padres"], titulo="El odio de Harrow"),
    acta("Jane Harrow", "harrow", [("AUTOR", "Case"), ("LUGAR", "Mar Negro · 1991"), ("PRUEBA", "Corte a negro")], "sin_cuerpo",
         "Muerte deducida", de="Todo su odio venía", a=("Número ocho. Lev", 1.2),
         marcas=[("venía de un error|fin", .1), ("venía de un error|fin", .5), ("venía de un error|fin", .9), ("venía de un error|fin", 1.3)],
         y=.42),

    # ---------------- 8 · Kravchenko
    puesto("Número ocho. Lev", 8, "Lev Kravchenko", "CAMPAÑA / BLACK OPS 1 Y 2"),
    cam("el hombre que sobrevivió", "kravchenko", "Kravchenko", dur=3.0, x=.16, y=.34),
    pv("Woods lo apuñala", "woods", "Frank Woods", dur=2.8, x=.80, y=.60, tam=320),
    mg_en(C.marcador("Granadas", 2, "Atadas al cinturón"), "tira de las granadas", 2.6, "marcador granadas", x=.5, y=.36),
    mg_en(C.objetivo("Encuentra a Woods", "Dado por muerto"), "Mason los da por muertos", 2.6, "objetivo woods", x=.30, y=.82),
    mapa("mundo", [(*_ll(18.0, 103.0, REC_K), "Laos · 1968", "inicio", P("woods")), (*_ll(21.03, 105.85, REC_K), "Hanói · Woods preso", "paso", P("woods")),
                   (*_ll(33.33, 69.92, REC_K), "Jost, Afganistán · 1986", "meta", P("kravchenko"))],
         de="el cinturón se soltó", a=("misión Viejas heridas", 2.0), marcas=["el cinturón se soltó", "preso a Vietnam", "Afganistán"],
         titulo="La ruta de Kravchenko", sub="1968 - 1986", recorte=REC_K),
    ficha("suelta que Menéndez tiene gente", "Última confesión", "Menéndez tiene gente *en la CIA*.", "INTEL / VIEJAS HERIDAS", dur=2.6),
    acta("Lev Kravchenko", "kravchenko", [("1.ª MUERTE", "Granadas · falsa"), ("AUTOR", "Frank Woods"), ("MISIÓN", "Viejas heridas · 1986")],
         "confirmado", "Murió dos veces", de="Dieciocho años después", a=("En el siete, Phillip", -.05),
         marcas=[("la deuda en persona|fin", -1.0), ("la deuda en persona|fin", -.6), ("la deuda en persona|fin", -.2),
                 ("la deuda en persona|fin", .2)], y=.42),

    # ---------------- 7 · Graves
    puesto("En el siete, Phillip", 7, "Phillip Graves", "CAMPAÑA / MW II → MW 4"),
    sil("El jefe de Shadow Company", "graves", "Graves", "Shadow Company", lado="der", dur=4.0),
    mg_en(C.marcador("Tanque", 30, "¿Graves dentro?"), "Soap revienta el tanque", 2.8, "marcador tanque", x=.5, y=.34),
    mg_en(C.fallida("TANQUE VACÍO", "Graves nunca estuvo dentro"), "Graves nunca estuvo dentro", 2.4, "fallida tanque"),
    mg_en(C.linea("Graves", [("2022", "MW II", "Muerte falsa"), ("2023", "MW III", "Vivo"), ("2026", "MW 4", "Hired Gun")], h=400),
          "Muere en Modern Warfare 4", 4.0, "linea graves", x=.5, y=.30),
    pv("Price derriba su helicóptero", "price", "Capitán Price", dur=2.8, x=.18, y=.62, tam=300),
    acta("Phillip Graves", "graves", [("AUTOR", "John Price"), ("CAUSA", "Tiro en la frente"), ("MISIÓN", "Hired Gun · París")],
         "confirmado", "No estaba en el tanque", de="Y si dudas más de dos", a=("Número seis. El", -.05),
         marcas=["Aquí, dudar", "es perder", "la partida", ("la partida|fin", .5)], y=.42),

    # ---------------- 6 · Zakhaev
    puesto("Número seis. El", 6, "Imran Zakhaev", "CAMPAÑA / CALL OF DUTY 4"),
    rel("El villano de Call of Duty 4", "zakhaev", "Imran Zakhaev", "Ultranacionalista", dur=3.4, x=.78, y=.50, tam=400),
    mg_en(C.marcador("Barrett", 897, "Price, 1996"), "con una Barrett", 3.0, "marcador barrett", x=.5, y=.34),
    mapa("mundo", [(*_ll(51.40, 30.06, REC_Z), "Prípiat · 1996", "inicio", P("price")), (*_ll(50.5, 86.0, REC_Z), "Montes Altái · 2011", "meta", P("soap"))],
         de="Quince años después", a=("y Soap acaba con él|fin", .3), marcas=["Quince años después", "en el puente de Fin"],
         titulo="Zakhaev · 15 años", sub="Del brazo a la cabeza", recorte=REC_Z),
    pv("Zakhaev ejecuta a Gaz", "gaz", "Gaz", dur=2.6, x=.18, y=.62, tam=290),
    mg_en(C.espejo("¿Dónde le dio Soap?", ("TORSO", "Intro de MW2", ["Disparo al torso"], None),
                   ("CABEZA", "Flashback de MW3", ["Disparo a la cabeza"], None), "EL MISMO TIRO"), "En la intro de Modern Warfare 2",
          4.6, "espejo tiro", x=.5, y=.40),
    acta("Imran Zakhaev", "zakhaev", [("AUTOR", "Soap MacTavish"), ("ARMA", "La M1911 de Price"), ("IMPACTO", "¿Torso o cabeza?")],
         "confirmado", "La saga no se pone de acuerdo", de="La saga no se pone de acuerdo", a=("En el cinco, Nikita", -.05),
         marcas=[("con su propio disparo|fin", -1.2), ("con su propio disparo|fin", -.8), ("con su propio disparo|fin", -.4),
                 ("con su propio disparo|fin", .0)], y=.42),

    # ---------------- 5 · Dragovich
    puesto("En el cinco, Nikita", 5, "Nikita Dragovich", "CAMPAÑA / BLACK OPS · 2010"),
    sil("El general soviético de los números", "dragovich", "Dragovich", "Nova 6", lado="izq", dur=4.0),
    mg_en(C.fallida("OBJETIVO VIVO", "Dragovich fingió su muerte"), "Pero Dragovich había fingido", 2.4, "fallida limusina"),
    pv("Mason le echa en cara", "mason", "Alex Mason", dur=2.8, x=.80, y=.60, tam=310),
    mg_en(C.radio("DRAGOVICH", "«Tried?»", "AUDIO / REDENCIÓN"), ("una sola palabra. Escucha|fin", .2), 3.4, "radio tried", x=.5, y=.24),
    ficha("deja la duda de si Mason participó", "¿Kennedy?", "«¿Intentado?» · la duda de *Dallas*.", "INTEL / REDENCIÓN", dur=3.6),
    acta("Nikita Dragovich", "dragovich", [("1.ª MUERTE", "Limusina · falsa"), ("AUTOR", "Alex Mason"), ("CAUSA", "Ahogado")], "confirmado",
         "«¿Intentado?»", de="Y Mason lo ahoga", a=("Número cuatro. El general", -.05),
         marcas=["Y Mason", "lo ahoga", "en el agua", ("en el agua que sube|fin", .3)], y=.42),

    # ---------------- 4 · Shepherd
    puesto("Número cuatro. El general", 4, "General Shepherd", "CAMPAÑA / MODERN WARFARE 2 · 2009"),
    pv("Modern Warfare 2, dos mil nueve", "c_mw2", "Modern Warfare 2 · 2009", dur=2.4, x=.86, y=.80, tam=220),
    carr([("ghost", "Ghost"), ("roach", "Roach"), ("soap", "Soap")], de="mató a Ghost y a Roach", a=("Misión final, Fin de partida", -.2),
         marcas=["Ghost", "Roach", "a Soap"], titulo="La traición de Shepherd"),
    rel("Misión final, Fin de partida", "shepherd", "Shepherd", "Fin de partida", dur=3.4, x=.78, y=.50, tam=400),
    mg_en(C.marcador("Cuchillo", 5, "El de Shepherd"), "Soap se saca del pecho", 3.0, "marcador cuchillo", x=.5, y=.34),
    ficha("fue enterrado en Arlington", "Arlington", "Enterrado como *héroe de guerra*.", "INTEL / DESPUÉS DE MW2", dur=3.6),
    pv("Price y Soap quedaron como fugitivos", "price", "Price · fugitivo", dur=2.8, x=.18, y=.62, tam=300),
    acta("General Shepherd", "shepherd", [("AUTOR", "Soap MacTavish"), ("ARMA", "Su propio cuchillo, al ojo"), ("REINICIO", "Price, tiro en la frente")],
         "confirmado", "Price lo mató dos veces", de=("en su propia oficina del Pentágono|fin", -1.4), a=("Un dato antes del podio", -.05),
         marcas=[("del Pentágono|fin", -1.2), ("del Pentágono|fin", -.8), ("del Pentágono|fin", -.4), ("del Pentágono|fin", .0)], y=.42),

    # ---------------- suscripción
    mg_en(C.contador(6, "DE CADA 1 000", "SUSCRITOS AL CANAL"), "De cada mil personas", 3.6, "contador subs", x=.5, y=.40),
    mg_en(C.objetivo("Suscríbete", "Únete a la unidad", completo=True), "Suscríbete, y el siguiente", 3.0, "objetivo subs", x=.30, y=.82),
    mg_en(C.logro("Ya eres de la unidad", "Llegaste hasta el podio"), "ya eres de la unidad", 2.8, "logro unidad", x=.5, y=.84),

    # ---------------- 3 · Menéndez
    puesto("En el tres, Raúl", 3, "Raúl Menéndez", "CAMPAÑA / BLACK OPS 2 · 2012"),
    rel("el villano de los tres finales", "menendez", "Raúl Menéndez", "Cordis Die", dur=3.4, x=.78, y=.50, tam=400),
    pv("Section le cae encima", "david_mason", "David «Section» Mason", dur=2.8, x=.18, y=.60, tam=310),
    mg_en(C.radio("MENÉNDEZ", "«Martyr me… for Cordis Die»", "AUDIO / JUDGMENT DAY"), ("en mártir. Escucha|fin", .2), 4.4,
          "radio martyr", x=.5, y=.24),
    mg_en(C.balanza("Los tres finales", [("Lo matas", True, "arde la Casa Blanca"), ("Lo capturas · Chloe vive", False, "se ríe en prisión"),
                                         ("Lo capturas · Chloe muere", False, "mata a Woods")]), "Si lo matas, se activa", 9.0,
          "balanza finales", y=.50),
    pv("Si lo capturas y Chloe vive", "chloe", "Chloe Lynch", dur=2.8, x=.86, y=.80, tam=240),
    pv("mata a Woods con el colgante", "woods", "Frank Woods", dur=2.8, x=.88, y=.80, tam=240),
    acta("Raúl Menéndez", "menendez", [("FINAL A", "Section lo mata"), ("FINAL B", "Preso, se ríe"), ("FINAL C", "Se prende fuego")],
         "depende", "Y aun así gana", de="Y si lo capturas y Chloe murió", a=("Número dos. El doctor", -.05),
         marcas=["el villano", "se elimina", "a sí mismo", "Y aun así gana"], y=.42),

    # ---------------- 2 · Steiner
    puesto("Número dos. El doctor", 2, "Friedrich Steiner", "CAMPAÑA / BLACK OPS · RENACIMIENTO"),
    cam("El científico nazi del gas", "steiner", "Steiner", dur=3.0, x=.16, y=.34),
    vs(("reznov", "Lo que viste"), ("mason", "Lo que pasó"), de="ves a Reznov entrar", a=("el que mata a Steiner es Mason", 1.0),
       marcas=["ves a Reznov", "es Mason"], ganador=1, titulo="¿Quién mató a Steiner?"),
    pv("Pero luego juegas como Hudson", "hudson", "Jason Hudson", dur=2.8, x=.80, y=.60, tam=300),
    mg_en(C.radio("MASON", "«My name is Viktor Reznov!»", "AUDIO / RENACIMIENTO"), ("Gritando esto. Escucha|fin", .2), 4.0,
          "radio reznov", x=.5, y=.24),
    ficha("llevaba cinco años muerto", "Viktor Reznov", "Muerto desde *Vorkuta*, 1963.", "INTEL / HUDSON", dur=3.4),
    com("Y FABIAN me escribió", "UgzNIv3Ae0b4WJKlGNJ4AaABAg", dur=5.4, x=.33, y=.30),
    mg_en(C.objetivo("¿Quién mató a Steiner?", "Responde, Fabian"), "Fabian, una pregunta", 3.0, "objetivo fabian", x=.30, y=.82),
    acta("Friedrich Steiner", "steiner", [("AUTOR", "Alex Mason"), ("CREÍA SER", "Viktor Reznov"), ("TESTIGO", "Hudson, tras el cristal")],
         "confirmado", "El juego te engañó", de="Si tu respuesta fue Reznov", a=("Y el número uno", -.05),
         marcas=["Si tu respuesta", "fue Reznov", "el juego te", "Y lo viste"], y=.42),

    # ---------------- 1 · Makarov
    bajas(("Y el número uno", -.2), ("El original, en Modern", -.1), tachados=("Amsel", "Al-Asad", "Victor", "El Lobo", "Barkov", "Irons", "Kotch",
          "Hassan", "Richtofen", "Kravchenko", "Graves", "Zakhaev", "Dragovich", "Shepherd", "Steiner"), foco="Makarov",
          marca=("tuvo que morir dos veces", .2), titulo="EL ÚLTIMO EXPEDIENTE"),
    puesto("El original, en Modern", 1, "Vladimir Makarov", "CAMPAÑA / MW3 2011 · MW4 2026"),
    pv("Hotel Oasis, Dubái", "c_mw3", "Modern Warfare 3 · 2011", dur=2.6, x=.86, y=.80, tam=220),
    pv("mata a Yuri delante de él", "yuri", "Yuri", dur=2.6, x=.18, y=.62, tam=290),
    mg_en(C.marcador("Techo de cristal", 15, "Hotel Oasis"), "los dos atraviesan el techo", 2.8, "marcador cristal", x=.5, y=.34),
    mg_en(C.codigo("3", "INTENTOS DEL ENCENDEDOR", "El puro de Price"), "al tercer intento", 3.0, "codigo encendedor", x=.5, y=.30),
    mg_en(C.logro("Fin de la trilogía", "Modern Warfare 1 · 2 · 3"), "empiezan los créditos de la trilogía", 3.0, "logro trilogia", x=.5, y=.84),
    sil("el nuevo Makarov mata a Soap", "makarov_r", "Makarov", "Reinicio · 2023", lado="der", dur=4.0),
    mapa("mundo", [(*_ll(25.20, 55.27, REC_M), "Dubái · MW3 2011", "inicio", P("makarov")),
                   (*_ll(40.71, -74.0, REC_M), "Nueva York · MW4 2026", "meta", P("makarov_r"))],
         de="Y muere en Modern Warfare 4", a=("Price lo mata a puñetazos|fin", .4), marcas=["Y muere en Modern", "un callejón nevado"],
         titulo="Los dos Makarov", sub="Dos finales, el mismo Price", recorte=REC_M),
    pv("Laswell le pregunta", "laswell", "Kate Laswell", dur=2.8, x=.80, y=.60, tam=300),
    mg_en(C.radio("PRICE", "«Off the list»", "AUDIO / MODERN WARFARE 4"), ("dónde está Makarov. Escucha|fin", .2), 3.6, "radio off list",
          x=.5, y=.24),
    acta("Vladimir Makarov", "makarov", [("2011", "Ahorcado · Dubái"), ("2026", "A puñetazos · Nueva York"), ("AUTOR", "John Price, las dos veces")],
         "confirmado", "Fuera de la lista", de="Fuera de la lista", a=("Expediente cerrado", -.05),
         marcas=["Fuera de la", "Dos Makarov", "dos finales", "el mismo hombre"], y=.42),

    # ---------------- cierre
    bajas("Expediente cerrado", ("Todos los comentarios se leen", -.1), tachados=("Amsel", "Al-Asad", "Victor", "El Lobo", "Barkov",
          "Irons", "Kotch", "Hassan", "Richtofen", "Kravchenko", "Graves", "Zakhaev", "Dragovich", "Shepherd", "Steiner", "Makarov",
          "Makarov 2023", "Menéndez"), titulo="EXPEDIENTES CERRADOS"),
    com("Como el de Prophet", "UgyRF13zDr2wzol-qph4AaABAg", dur=5.6, x=.33, y=.30),
    com("O el de Daan", "UgzM77HNO_4LXHpQx1h4AaABAg", dur=3.4, x=.68, y=.30, tam=700),
    com("O el de almidon", "Ugyy2ozNTVrDvg8olAd4AaABAg", dur=4.6, x=.33, y=.68, tam=700),
    com("Y v5x777 aclaró", "UgxjFOBNNW0MPOXEEw94AaABAg", dur=5.6, x=.33, y=.30),
    mg_en(C.objetivo("¿Qué villano merece su expediente?", "Escríbelo en los comentarios"), "qué villano de Call of Duty merece", 3.4,
          "objetivo comenta", x=.30, y=.82),
    mg_en(C.sello("CERRADO", "EXPEDIENTE 141"), "Retírate, soldado", 2.4, "sello cerrado", x=.5, y=.45),
]

# ---------------- 2.ª capa (17-nov-2026, chequeo: fichas 0,7/min y pegatinas 3,5/min → subir a la mediana del canal)
FX += [
    pv("Otro, colgado de un cable", "price", "John Price", dur=2.2, x=.86, y=.82, tam=220),
    pv("Veinte villanos, cada muerte", "c_mw2", "Modern Warfare 2", dur=2.0, x=.10, y=.84, tam=200),
    ficha("cazan al general alemán", "Stalingrado · 1942", "Dos francotiradores contra *un general*.", "INTEL / WORLD AT WAR", dur=3.2, x=.73),
    pv("Reznov se ríe a carcajadas", "c_waw", "World at War · 2008", dur=2.4, x=.86, y=.80, tam=220),
    ficha("El hombre que ejecutó al presidente", "Al-Fulani", "Presidente ejecutado *ante la cámara*.", "INTEL / THE COUP", dur=3.4, x=.73),
    pv("Price lo tiene atado", "gaz", "Gaz", dur=2.4, x=.86, y=.82, tam=220),
    pv("Misión Los pecados del padre", "c_cod4", "Call of Duty 4", dur=2.4, x=.86, y=.80, tam=220),
    ficha("Acorralado, Victor saca", "Victor Zakhaev", "Acorralado en *una azotea*.", "INTEL / VOLGOGRADO", dur=3.0, x=.73),
    pv("al que culpan de robar el gas", "alejandro", "Alex Keller", dur=2.4, x=.14, y=.82, tam=220),
    ficha("grabando un mensaje frente", "El mensaje", "Una cámara y *un chaleco bomba*.", "INTEL / LA GUARIDA", dur=3.2, x=.73),
    pv("El general ruso que invadió", "c_mw19", "Modern Warfare · 2019", dur=2.4, x=.86, y=.80, tam=220),
    pv("Pero el piloto es Nikolai", "barkov", "Roman Barkov", dur=2.4, x=.14, y=.82, tam=220),
    pv("Advanced Warfare. El dueño", "c_aw", "Advanced Warfare · 2014", dur=2.4, x=.86, y=.80, tam=220),
    pv("Irons cae con el brazo", "irons", "Irons", dur=2.4, x=.14, y=.82, tam=220),
    ficha("Muere en la sexta operación", "Infinite Warfare", "El jefe final *no es Kotch*.", "INTEL / 7 OPERACIONES", dur=3.0, x=.73, y=.62),
    pv("En la Operación Bandera Negra", "salter", "Nora Salter", dur=2.4, x=.86, y=.82, tam=220),
    pv("Hassan arrastra a Soap", "soap", "Soap MacTavish", dur=2.6, x=.86, y=.82, tam=230),
    ficha("Misión Countdown, un rascacielos", "Countdown", "Un rascacielos *de Chicago*.", "INTEL / MW II", dur=3.0, x=.73),
    pv("se pasó a la Federación", "elias", "Elias Walker", dur=2.4, x=.14, y=.82, tam=220),
    ficha("el tren descarrila y cae", "El tren", "Descarrila y *cae al agua*.", "INTEL / THE GHOST KILLER", dur=3.0, x=.73),
    pv("Murió más de una vez", "c_bo2", "Black Ops", dur=2.0, x=.86, y=.82, tam=200),
    ficha("para cerrar la paradoja", "La paradoja", "Cerrar el *multiverso* del Éter.", "INTEL / ZOMBIES", dur=2.0, x=.73),
    ficha("De cáncer, en mil", "Perseus", "Muere *fuera del juego*.", "INTEL / TEMPORADA 6", dur=3.0, x=.73, y=.62),
    pv("La espía que traicionó al equipo", "adler", "Russell Adler", dur=2.4, x=.14, y=.82, tam=220),
    pv("la pantalla se va a negro", "marshall", "Troy Marshall", dur=2.4, x=.86, y=.82, tam=220),
    pv("Black Ops, dos mil diez. Misión Venganza", "c_bo1", "Black Ops · 2010", dur=2.4, x=.86, y=.80, tam=220),
    pv("Graves nunca estuvo dentro", "c_mw22", "MW II · 2022", dur=2.2, x=.86, y=.80, tam=210),
    ficha("Muere en Modern Warfare 4", "Hired Gun", "París · *armadura Argonaut*.", "INTEL / MW 4", dur=3.0, x=.73, y=.62),
    pv("en Prípiat, Price le vuela", "price", "Price · 1996", dur=2.4, x=.14, y=.82, tam=220),
    pv("Price, herido, le desliza", "soap", "Soap", dur=2.4, x=.86, y=.82, tam=220),
    ficha("En Baikonur, el equipo destruye", "Baikonur", "La limusina *estaba vacía*.", "INTEL / BLACK OPS", dur=3.2, x=.73),
    pv("Su final real es en Redención", "hudson", "Jason Hudson", dur=2.4, x=.14, y=.82, tam=220),
    pv("Price derriba su helicóptero, caen", "soap", "Soap", dur=2.2, x=.86, y=.82, tam=220),
    pv("Black Ops 2, el villano de los", "c_bo2", "Black Ops 2", dur=2.2, x=.86, y=.80, tam=210),
    ficha("Si lo matas, se activa", "Cordis Die", "Un video grabado *para su muerte*.", "INTEL / FINAL A", dur=3.0, x=.73, y=.24),
    pv("El científico nazi del gas", "weaver", "Grigori Weaver", dur=2.4, x=.86, y=.82, tam=220),
    ficha("Hudson lo dice clarito", "Hudson", "«Nunca estuvo *aquí*».", "INTEL / RENACIMIENTO", dur=3.2, x=.73),
    pv("Price se le echa encima, le enrolla", "price", "Price", dur=2.4, x=.14, y=.82, tam=220),
    pv("Doce años después llega", "c_mw23", "MW III · 2023", dur=2.4, x=.86, y=.80, tam=220),
    pv("En Modern Warfare 3 de dos mil veintitrés", "soap", "Soap · 2023", dur=2.4, x=.14, y=.82, tam=220),
    pv("Todos los comentarios se leen", "c_cod4", "Expediente 141", dur=2.0, x=.86, y=.84, tam=200),
]
