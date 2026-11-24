# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Cómo acabó REALMENTE cada protagonista de Call of Duty» (SECUENCIA YT, Expediente 141, 24-nov-2026).
Plantilla: videos/cod_mandela3/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta, tema «cod»).
MG NUEVOS de este guion: `C.consola` (el código de BO2 que desmiente el desangrado, n.º 4) y `C.golpes` (golpes con Juggernog, n.º 10).
Citas (post): el clip va alineado al hueco (_escribir_busquedas.py) y lo que se OYE es sfx/s_*.mp3 (recortes medidos con
_citas.py) en PISTAS voz=True, al acabar la frase; `ambiente_por` no sirve: suena el beat entero, encima de la voz.
    python fab.py cod_protagonistas fx --seco   tiempos      FAB_FX_FINAL=1 python fab.py cod_protagonistas fx hoja
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





# ------------------------------------------------------------------ MG propios de este guion (24-nov-2026)
def com(en, cid, dur=6.4, x=.36, y=.30, giro=-2):
    """Comentario real del canal (pegatinas/com_<id>.png, ≤ 10 días, ninguno repetido)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=giro)


def placa(nombre, lineas, estado, sub, de, a, x=.74, y=.42):
    """Placa de identificación (MG nuevo `C.placa`): una línea cada 0,45 s desde `de`, sello al final (marcas automáticas)."""
    t, o = (de, 0.0) if isinstance(de, str) else de
    marcas = [(t, o + .6 + .45 * i) for i in range(len(lineas) + 1)]
    return dict(tipo="mg", fn=C.placa(nombre, lineas, estado, sub), de=de, a=a, marcas=marcas, x=x, y=y, sale=.35,
                nombre="MG placa " + nombre, ver=2.6)


def serv(nombre, slug, filas, de, a, marcas, y=.46):
    """Hoja de servicio (MG nuevo `C.servicio`): una fila por juego, cada una en su marca."""
    return dict(tipo="mg", fn=C.servicio(nombre, P(slug), filas), de=de, a=a, marcas=list(marcas), x=.5, y=y, sale=.35,
                nombre="MG servicio " + nombre, ver=3.0)


def _ll(lat, lon, rec):
    """lat/lon reales → fracción del mapa equirectangular recortado (mapas/mundo.jpg, NASA)."""
    x, y = (lon + 180) / 360, (90 - lat) / 180
    return (x - rec[0]) / (rec[2] - rec[0]), (y - rec[1]) / (rec[3] - rec[1])


def _sagas():
    return [("MODERN WARFARE", [(P(s), n) for s, n in [("soap", "Soap"), ("roach", "Roach"), ("ghost", "Ghost"), ("yuri", "Yuri"),
                                                      ("jackson", "Jackson"), ("allen", "Allen")]]),
            ("BLACK OPS", [(P(s), n) for s, n in [("mason", "Mason"), ("woods", "Woods"), ("reznov", "Reznov"), ("section", "Section"),
                                                 ("bell", "Bell"), ("case", "Case")]]),
            ("REINICIO", [(P(s), n) for s, n in [("price_r", "Price 2026"), ("soap_r", "Soap 2023"), ("gaz_r", "Gaz 2026"), ("ghost_r", "Ghost 2026"),
                                                ("keller", "Alex Keller")]]),
            ("OTROS", [(P(s), n) for s, n in [("reyes", "Reyes"), ("logan", "Logan"), ("player_bo3", "BO3"), ("alfulani", "Al-Fulani")]])]


def bajas(de, a, tachados=(), foco=None, marca=None, titulo="20 PROTAGONISTAS · 20 EXPEDIENTES"):
    return dict(tipo="mg", fn=C.bajas(_sagas(), tachados, foco, titulo, w=1640, lado=128), de=de, a=a,
                marcas=[marca] if marca else [], x=.5, y=.50, sale=.35, nombre="MG bajas " + (foco or "gancho"), ver=3.0)


REC_Y = (.52, .14, .72, .40)     # Ucrania/Moscú → Golfo (Yuri)
REC_P = (.80, .17, .92, .33)     # Corea (Price, MW4)
_D, _I = dict(x=.80, y=.62), dict(x=.18, y=.64)
_I2, _D2 = dict(x=.18, y=.64, tam=280), dict(x=.80, y=.62, tam=280)

FX = [
    # cortes que tapan lo que sigue a cada cita (violencia: nunca el disparo; lección de cod_mandela2)
    vid(49, ("Escucha lo que contesta Shepherd|fin", 2.4), ("gasolina", -.1), desde=1.0),   # Shepherd: el disparo cae a 5 s del clip 050
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("c_mw4", "EXPEDIENTE 141 · PROTAGONISTAS", ["Asunto: los protagonistas", "Destino REAL", "20 expedientes"],
        de="Asunto: los protagonistas", a=("El capitán Price", -.1), x=.78, y=.50),
    carr([("price_r", "Price"), ("soap", "Soap"), ("gaz_r", "Gaz"), ("ghost_r", "Ghost"), ("mason", "Mason"), ("woods", "Woods"),
          ("reznov", "Reznov")], de="El capitán Price", a=("Les salvaste la vida", -.05),
         marcas=["el sargento Soap", "Gaz y el teniente", "El agente Mason", "el sargento Woods", "el viejo Reznov"], titulo="Los manejaste a todos"),
    mg_en(C.contador(100, "VECES", "LES SALVASTE LA VIDA"), "Les salvaste la vida", 2.4, "contador cien", x=.30, y=.30),
    mg_en(C.fallida("CASI NINGUNO", "Terminó como crees"), "Y casi ninguno terminó", 2.2, "fallida casi ninguno"),
    pv("Uno estaba muerto desde la segunda", "player_bo3", "¿Muerto desde la misión 2?", dur=2.4, tam=300, **_D),
    pv("Otro murió de viejo", "woods", "¿104 años?", dur=2.4, tam=300, **_I),
    pv("Y al capitán Price lo mataron", "price_r", "Capitán Price · 2026", dur=2.8, tam=320, **_D),
    mg_en(C.objetivo("Revisar cada destino", "Juego por juego · con la escena", completo=True), "Revisé el destino de cada uno", 2.6,
          "objetivo revisar", x=.30, y=.82),
    ficha("Aviso: hay spoilers", "Aviso", "Spoilers de *Modern Warfare 4* y *Black Ops 7*.", "INTEL / EXPEDIENTE 141", dur=3.2),
    bajas("Veinte protagonistas de Call of Duty", ("Empezamos por el que", -.05)),
    mg_en(C.marcador("Marte", 225, "Millones de km"), "llegó más lejos: al espacio", 2.4, "marcador marte", x=.55, y=.36),

    # ---------------- 20 · Nick Reyes
    puesto("Número veinte. Nick Reyes", 20, "Nick Reyes", "CAMPAÑA / INFINITE WARFARE · 2016"),
    sil("Capitán de la nave Retribution", "reyes", "Nick Reyes", "Capitán de la Retribution", lado="izq", dur=3.8),
    ficha("el personaje jugable de mayor rango", "Rango", "Comandante *O-5*: el jugable de mayor rango.", "INTEL / INFINITE WARFARE",
          dur=3.2, x=.73),
    pv("sobre Marte", "marte", "Marte", dur=2.6, tam=300, **_D),
    pv("le ordena a Salter", "salter", "Nora Salter", dur=2.8, tam=300, **_I),
    mg(C.golpes("El visor de Reyes", 3, "Tres trozos de metralla"), de="tres trozos de metralla", a=("hasta que la pantalla", 1.2),
       marcas=["tres trozos", "de metralla", "le van rompiendo", "el visor del casco"], nombre="golpes visor", y=.50),
    mg_en(C.linea("Reyes · tres veces", [("1", "La Luna", "Visor agrietado"), ("2", "Titán", "A la deriva"), ("3", "Marte", "Sin rescate")],
                  h=400), "Antes ya se había salvado dos veces", 5.2, "linea reyes", x=.5, y=.30),
    placa("Nick Reyes", ["Capitán · UNSA Retribution", "Infinite Warfare · 2016"], "kia", "Nadie fue a buscarlo",
          de=("A la tercera, nadie", -.6), a=("En el diecinueve, Logan", -.05)),

    # ---------------- 19 · Logan Walker (+ @Keengan12239)
    puesto("En el diecinueve, Logan", 19, "Logan Walker", "CAMPAÑA / GHOSTS · 2013"),
    pv("un tren que cae al agua", "m_ghost_killer", "The Ghost Killer", dur=2.6, tam=300, **_D),
    mg_en(C.contador(1, "BALA", "LA ÚNICA QUE LE LANZA HESH"), "una sola bala", 2.4, "contador bala", x=.30, y=.30),
    pv("su hermano Hesh", "hesh", "Hesh Walker", dur=2.6, tam=300, **_I),
    sil("Rorke está vivo", "rorke", "Gabriel Rorke", "Sigue vivo", lado="der", dur=3.8),
    mg_en(C.objetivo("Sobrevive en el pozo", "Bajo la lluvia"), "Logan despierta en un pozo", 2.6, "objetivo pozo", x=.30, y=.82),
    mg_en(C.contador(13, "AÑOS", "SIN SECUELA"), "Han pasado trece años", 2.4, "contador 13", x=.30, y=.30),
    placa("Logan Walker", ["Ghosts · 2013", "Prisionero de Rorke"], "mia", "Sigue en el pozo", de="No hubo secuela",
          a=("Keengan lo dijo así", -.05)),
    com("Keengan lo dijo así", "UgzSoYq5kEbcJO6x-Sh4AaABAg", dur=6.4),
    mg_en(C.logro("Rorke ganó", "Y nadie le dio el crédito"), "Rorke ganó", 2.6, "logro rorke", x=.5, y=.30),

    # ---------------- 18 · Alex Keller
    puesto("Número dieciocho. Alex", 18, "Alex Keller", "CAMPAÑA / MODERN WARFARE · 2019"),
    pv("En la fábrica de Barkov", "barkov", "Roman Barkov", dur=2.6, tam=300, **_D),
    pv("en Georgia", "borjomi", "Borjomi, Georgia", dur=2.4, tam=280, **_I),
    pv("le pide la orden a Farah", "farah", "Farah Karim", dur=2.8, tam=300, **_D),
    mg_en(C.fallida("DADO POR MUERTO", "Into the Furnace"), "Todos lo dieron por muerto", 2.2, "fallida keller"),
    serv("Alex Keller", "keller", [("Into the Furnace", 2019, "mia", "Dado por muerto"), ("5 meses escondido", 2020, "desconocido", "Acusado de desertor"),
                                   ("Temporada 3 · MW II", 2020, "vuelve", "Con prótesis")],
         de="Sobrevivió a la explosión", a=("El sacrificio más heroico", .4),
         marcas=["Sobrevivió a la explosión", "pasó cinco meses", "y volvió con una prótesis"]),
    placa("Alex Keller", ["CIA · Modern Warfare", "Sin la pierna izquierda"], "vivo", "Le costó una pierna",
          de=("El sacrificio más heroico", -.2), a=("En el diecisiete, el sargento", -.05)),

    # ---------------- 17 · Paul Jackson
    puesto("En el diecisiete, el sargento", 17, "Paul Jackson", "CAMPAÑA / CALL OF DUTY 4 · 2007"),
    pv("Call of Duty 4.", "c_cod4", "Call of Duty 4", dur=2.4, tam=280, **_D),
    pv("estalla la bomba nuclear", "m_shock", "Shock and Awe", dur=2.8, tam=300, **_I),
    ficha("caminas entre ruinas rojas", "Aftermath", "Sin cinemática: *todo en primera persona*.", "INTEL / CALL OF DUTY 4", dur=3.4, x=.73),
    mg(C.consola("objetivos_cortados.cfg", ["Get radiation equipment", "Locate commanding officer", "Find secure overhead cover"],
                 resalta=(0, 1, 2), nota="CORTADOS · NUNCA SE USARON"),
       de="tres objetivos cortados", a=("Jackson iba a sobrevivir", -.1),
       marcas=["buscar equipo", "localizar al oficial", "ponerte a cubierto"], nombre="consola jackson", y=.48),
    placa("Paul Jackson", ["Sargento · USMC", "Call of Duty 4 · 2007"], "kia", "Iba a sobrevivir",
          de="Jackson iba a sobrevivir", a=("Número dieciséis. El presidente", -.05)),

    # ---------------- 16 · Al-Fulani
    puesto("Número dieciséis. El presidente", 16, "Yasir Al-Fulani", "CAMPAÑA / CALL OF DUTY 4 · THE COUP"),
    sil("Lo controlas, pero no puedes", "alfulani", "Al-Fulani", "Presidente", lado="izq", dur=3.8),
    mg_en(C.objetivo("No puedes hacer nada", "Solo mirar por la ventana"), "en el asiento de atrás de un coche", 2.6, "objetivo coup",
          x=.30, y=.82),
    pv("un patio lleno de soldados", "alasad", "Al-Asad", dur=2.6, tam=300, **_D),
    rel("es Victor Zakhaev", "victor", "Victor Zakhaev", "El copiloto", dur=3.6, x=.77, y=.52, tam=420),
    pv("el hijo del villano", "zakhaev", "Imran Zakhaev", dur=2.6, tam=280, **_I),
    placa("Al-Fulani", ["Presidente", "The Coup · CoD 4"], "kia", "Duró una misión", de=("El primer protagonista del Modern", -.1),
          a=("Antes del quince, un comentario", -.05)),

    # ---------------- crítica 1 · @andreshico1220
    com("Antes del quince, un comentario", "UgyOXQ2qm9ubc342COF4AaABAg", dur=7.4),
    ficha("el perro de una familia", "Riley", "Un perro de familia, *en una misión encubierta*.", "INTEL / COMENTARIOS", dur=3.2, x=.73, y=.70),
    mg_en(C.logro("Dato recibido", "Gracias, Andrés"), "Gracias, Andrés", 2.4, "logro andres", x=.5, y=.30),
    mg_en(C.balanza("Lo que se salvó del expediente", [("El perro", True, "Riley"), ("Todo lo demás", False, "según Andrés")]),
          "lo único que se salvó fue el perro", 3.6, "balanza perro", y=.55),

    # ---------------- 15 · Joseph Allen
    puesto("Número quince. Joseph", 15, "Joseph Allen", "CAMPAÑA / MODERN WARFARE 2 · 2009"),
    pv("Entra encubierto con la banda de Makarov", "allen", "¿Quién es Alexei Borodin?", dur=3.6, tam=380, **_D),
    ficha("con otro nombre", "Alias", "*Alexei Borodin*, infiltrado de la CIA.", "INTEL / MODERN WARFARE 2", dur=3.0),
    pv("Makarov le tiende la mano", "makarov", "Makarov", dur=2.8, tam=300, **_I),
    mg_en(C.radio("MAKAROV · ESTACIONAMIENTO", "Ya sabía quién era."), "Y ya sabía quién era", 2.6, "radio makarov", x=.5, y=.20),
    mg_en(C.objetivo("El mensaje", "Un estadounidense en el aeropuerto"), "justo el mensaje que necesitaba", 2.8, "objetivo mensaje",
          x=.30, y=.82),
    placa("Joseph Allen", ["Ranger · alias Borodin", "Modern Warfare 2 · 2009"], "kia", "No fue el infiltrado: fue la carta",
          de=("Allen no fue el infiltrado", -.3), a=("En el catorce, Yuri", -.05)),

    # ---------------- 14 · Yuri (mapa con ruta)
    puesto("En el catorce, Yuri", 14, "Yuri", "CAMPAÑA / MODERN WARFARE 3 · 2011"),
    pv("En la misión Blood Brothers", "m_blood_brothers", "Blood Brothers", dur=2.6, tam=300, **_D),
    mapa("mundo", [(*_ll(51.40, 30.06, REC_Y), "Prípiat · 1996", "inicio", P("yuri")), (*_ll(55.41, 37.90, REC_Y), "Aeropuerto · Moscú", "paso", P("makarov")),
                   (*_ll(25.20, 55.27, REC_Y), "Dubái · 2017", "meta", P("price"))],
         de="en Prípiat en mil", a=("Muere en la última misión", 1.6), marcas=["en Prípiat", "y en el aeropuerto", "en el hotel de Dubái"],
         titulo="Yuri estuvo en todas partes", sub="1996 - 2017", recorte=REC_Y),
    pv("Atravesado por una barra", "m_dust", "Dust to Dust", dur=2.6, tam=300, **_I),
    vs(("yuri", "Yuri"), ("makarov", "Makarov"), de="Y aun así se levanta", a=("Le salvó la vida", -.1),
       marcas=["Y aun así se levanta", "y le dispara a Makarov"], ganador=0, titulo="Yuri salva a Price"),
    placa("Yuri", ["Ex Ultranacionalista", "Modern Warfare 3 · 2011"], "kia", "Le costó la suya", de=("Le salvó la vida", -.3),
          a=("Número trece. Case", -.05)),

    # ---------------- 13 · Case
    puesto("Número trece. Case", 13, "William «Case» Calderon", "CAMPAÑA / BLACK OPS 6 · 2024"),
    pv("el helicóptero de Jane Harrow", "harrow", "Jane Harrow", dur=2.8, tam=300, **_D),
    pv("cae al mar Negro", "mar_negro", "Mar Negro · 1991", dur=2.4, tam=280, **_I),
    ficha("con una voz en la cabeza", "La voz", "«*Finish this*»: efecto de la toxina Cradle.", "INTEL / BLACK OPS 6", dur=3.2, x=.73),
    mg_en(C.radio("MARSHALL · RADIO", "«¡Lo logramos, Case!»"), "Marshall grita que lo lograron", 3.0, "radio marshall", x=.5, y=.20),
    pv("Lo responde Black Ops 7", "c_bo7", "Black Ops 7", dur=2.4, tam=280, **_D),
    ficha("una muestra de sus restos", "Black Ops 7 · 2035", "Recuperan *una muestra de sus restos*.", "INTEL / BLACK OPS 7", dur=3.4, x=.73),
    placa("Case", ["Black Ops 6 · 1991", "Sujeto de prueba Cradle n.º 1"], "kia", "Cerrado con una muestra", de=("El final abierto se cerró", -.2),
          a=("En el doce, David", -.05)),

    # ---------------- 12 · Section
    puesto("En el doce, David", 12, "David «Section» Mason", "CAMPAÑA / BLACK OPS 2 → BLACK OPS 7"),
    sil("Section deja su pistola", "section", "Section", "David Mason", lado="izq", dur=3.8),
    pv("frente a la tumba de su padre", "m_judgment", "Judgment Day", dur=2.6, tam=300, **_D),
    mg_en(C.contador(2035, "AÑO", "BLACK OPS 7", desde=2025), "en dos mil treinta y cinco", 2.6, "contador 2035", x=.30, y=.30),
    mg(C.balanza("El final oficial de Black Ops 2", [("Harper", True, "vivo"), ("Karma", True, "viva"), ("Alex Mason", False, "muerto")]),
       de="Harper vivo", a=("Section sobrevive a todo", -.1), marcas=["Harper vivo", "Karma viva", "y Alex Mason muerto"], nombre="balanza bo2"),
    placa("Section", ["Black Ops 2 · Black Ops 7", "Specter One · 2035"], "vivo", "Sobrevive a todo", de="Section sobrevive a todo",
          a=("Número once. Roach", -.05)),

    # ---------------- 11 · Roach y Ghost (post: «one less loose end»)
    puesto("Número once. Roach", 11, "Roach y Ghost · los originales", "CAMPAÑA / MODERN WARFARE 2 · LOOSE ENDS"),
    carr([("roach", "Roach"), ("ghost", "Ghost")], de="Roach y Ghost, los originales", a=("Roach acaba de cargar", -.05),
         marcas=["Roach y Ghost", "los originales"], titulo="Los originales"),
    ficha("Roach acaba de cargar el disco", "El DSM", "El disco con la *información de Makarov*.", "INTEL / LOOSE ENDS", dur=3.2, x=.73),
    pv("el helicóptero del general Shepherd", "shepherd", "General Shepherd", dur=3.0, tam=320, **_I),
    mg_en(C.radio("SHEPHERD · LOOSE ENDS", "Escucha lo que contesta."), "Escucha lo que contesta Shepherd", 3.2, "radio shepherd", x=.5, y=.20),
    ficha("Un cabo suelto menos", "Shepherd", "«*One less loose end*»: un cabo suelto menos.", "INTEL / LOOSE ENDS", dur=3.4, x=.73),
    serv("Roach y Ghost", "ghost", [("Roach · Loose Ends", 2009, "kia", "Disparo y fuego"), ("Ghost · Loose Ends", 2009, "kia", "Disparo y fuego"),
                                    ("Remaster", 2020, "retcon", "Ghost mira a Roach")],
         de="En el remaster agregaron", a=("Lo que nunca le dieron", 1.4), marcas=["En el remaster", "Ghost mira a Roach", "agarrarle la muñeca"]),

    # ---------------- 10 · Ghost del reinicio (+ @TMPLR5)
    puesto("En el diez, el otro Ghost", 10, "Simon «Ghost» Riley", "CAMPAÑA / REINICIO 2019 → MW 4"),
    mg_en(C.linea("Ghost · reinicio", [("2019", "MW", "Sin aparecer"), ("2022", "MW II", "Ghost Team"), ("2023", "MW III", "El funeral"),
                                       ("2026", "MW 4", "El último")], h=400), "Modern Warfare dos mil diecinueve, Modern", 5.0, "linea ghost",
          x=.5, y=.30),
    bajas("es el único de la fuerza", ("TMPLR5 lo vio venir", -.05), tachados=("Soap 2023", "Gaz 2026", "Price 2026"),
          titulo="FUERZA 141 · REINICIO"),
    com("TMPLR5 lo vio venir", "Ugzo4vO15C-dMfGwhM14AaABAg", dur=6.6),
    pv("Laswell borra su expediente", "laswell", "Kate Laswell", dur=2.8, tam=300, **_D),
    placa("Simon Riley", ["Teniente · Fuerza 141", "Reinicio · 2019-2026"], "vivo", "El único en pie", de=("el que nunca enseñó la cara", -.4),
          a=("Número nueve. Viktor", -.05)),

    # ---------------- 9 · Reznov (post: «For you, Mason…»)
    puesto("Número nueve. Viktor", 9, "Viktor Reznov", "CAMPAÑA / WORLD AT WAR → BLACK OPS"),
    pv("Vorkuta, mil novecientos sesenta", "vorkuta", "Vorkuta · 1963", dur=2.8, tam=300, **_D),
    sil("Reznov se queda atrás", "reznov", "Viktor Reznov", "Se queda atrás", lado="izq", dur=3.4),
    mg_en(C.radio("REZNOV · VORKUTA", "Su despedida."), "Escucha su despedida", 3.0, "radio reznov", x=.5, y=.20),
    ficha("Muere en Vorkuta", "Reznov", "«*For you, Mason… not for me*».", "INTEL / VORKUTA", dur=3.2, x=.73),
    mg_en(C.fallida("NUNCA ESTUVO AHÍ", "Vietnam · la isla Rebirth"), "nunca estuvo ahí", 2.4, "fallida reznov"),
    pv("Hudson se lo dice a Mason", "hudson", "Jason Hudson", dur=2.8, tam=300, **_I),
    mg_en(C.contador(5, "AÑOS", "MUERTO"), "llevaba cinco años muerto", 2.4, "contador cinco", x=.30, y=.30),
    aba([("dragovich", "Dragovich"), ("kravchenko", "Kravchenko"), ("steiner", "Steiner")], de="se vengó de Dragovich",
        a=("Muerto, y a través de otro", .8), marcas=["de Dragovich", "de Kravchenko", "y de Steiner"], nombre="venganza reznov"),

    # ---------------- 8 · Soap original (post: «Makarov… knows… Yuri»)
    puesto("En el ocho, John Soap", 8, "John «Soap» MacTavish", "CAMPAÑA / CoD 4 → MODERN WARFARE 3"),
    serv("Soap MacTavish", "soap", [("Call of Duty 4", 2007, "vivo", "Mata a Zakhaev"), ("Modern Warfare 2", 2009, "vivo", "Un cuchillo en el pecho"),
                                    ("Modern Warfare 3", 2011, "kia", "Praga")],
         de="Mataste a Zakhaev con él", a=("Estas son sus últimas", -.2), marcas=["Mataste a Zakhaev", "sobreviviste a un cuchillo", "en Praga"]),
    pv("Soap empuja a Yuri", "yuri", "Yuri", dur=2.4, tam=280, **_I),
    mg_en(C.radio("SOAP · ÚLTIMAS PALABRAS", "Praga, 2016."), "Estas son sus últimas palabras", 3.6, "radio soap", x=.5, y=.20),
    rel("la misma pistola M1911", "m1911", "M1911", "La de Zakhaev", dur=3.6, x=.77, y=.52, tam=420),
    placa("Soap MacTavish", ["Capitán · Fuerza 141", "CoD 4 · MW2 · MW3"], "kia", "Solo pudiste verlo morir",
          de=("Solo lo controlaste en la primera", -.2), a=("Número siete. Frank", -.05)),

    # ---------------- 7 · Woods
    puesto("Número siete. Frank", 7, "Frank Woods", "CAMPAÑA / BLACK OPS → BLACK OPS 7"),
    serv("Frank Woods", "woods", [("Black Ops · granadas", 1968, "vuelve", "Sobrevive"), ("Black Ops 2 · Menéndez", 2025, "retcon", "No cuenta"),
                                  ("Cold War · Bell", 1981, "retcon", "No cuenta"), ("Black Ops 7 · Arlington", 2034, "kia", "De viejo, 104 años")],
         de="Murió tres veces", a=("está enterrado en Arlington", -.1),
         marcas=["con Kravchenko y un cinturón", "Menéndez lo mata", "lo ejecuta Bell", "Woods murió en dos mil treinta y cuatro"]),
    pv("está enterrado en Arlington", "arlington", "Arlington", dur=2.8, tam=300, **_D),
    mg_en(C.contador(104, "AÑOS", "FRANK WOODS · 1930-2034", desde=60), "de viejo, con ciento cuatro años, y está", 2.6, "contador 104", x=.30, y=.30),
    mg_en(C.logro("Sobreviviente", "Vietnam · Kravchenko · Menéndez · Bell"), "Sobrevivió a Vietnam", 2.8, "logro woods", x=.5, y=.30),

    # ---------------- 6 · Bell (post: «It was never personal»)
    puesto("En el seis, Bell", 6, "Bell", "CAMPAÑA / BLACK OPS COLD WAR · 2020"),
    ficha("Lo creas tú", "Bell", "Nombre, origen, todo: *lo eliges tú*.", "INTEL / COLD WAR", dur=3.0, x=.73),
    pv("Adler te lleva a un acantilado", "adler", "Russell Adler", dur=2.8, tam=320, **_I),
    pv("salvas Europa", "solovetsky", "Islas Solovetsky", dur=2.4, tam=280, **_D),
    mg_en(C.radio("ADLER · EL ACANTILADO", "Antes del disparo."), "Antes, Adler le dice esto", 3.4, "radio adler", x=.5, y=.20),
    ficha("En el juego nunca se sabe", "Adler", "«*It was never personal*»: nunca fue personal.", "INTEL / COLD WAR", dur=3.2),
    mg_en(C.caso("verdad", "¿Quién disparó primero?", "Adler · podcast oficial 2024"), "disparó Adler primero", 3.0, "caso adler"),
    placa("Bell", ["Black Ops Cold War", "Final bueno · 1981"], "kia", "El final bueno también te mata",
          de=("Elegiste el final bueno", -.1), a=("Número cinco. Alex", -.05)),

    # ---------------- 5 · Alex Mason
    puesto("Número cinco. Alex", 5, "Alex Mason", "CAMPAÑA / BLACK OPS → BLACK OPS 2"),
    pv("Panamá, mil novecientos ochenta", "miraflores", "Panamá · 1989", dur=2.6, tam=300, **_D),
    pv("Noriega te entrega", "noriega", "Noriega", dur=2.6, tam=300, **_I),
    mg_en(C.objetivo("Dispara", "Orden de Hudson"), "Hudson te ordena dispararle", 2.4, "objetivo dispara", x=.30, y=.82),
    sil("Woods le quita la bolsa", "mason", "Alex Mason", "Bajo la bolsa", lado="der", dur=3.6),
    mg(C.balanza("Black Ops 2 · dos finales", [("Mason herido", None, "final 1"), ("Mason muerto", True, "el oficial (2024)")]),
       de="El juego te dejaba salvarlo", a=("Y Hudson, también muerto", 1.0), marcas=["El juego te dejaba", "Mason está muerto"],
       nombre="balanza mason"),
    placa("Alex Mason", ["Black Ops · Black Ops 2", "Panamá · 1989"], "kia", "Lo mató Woods", de=("Y Hudson, también muerto", .4),
          a=("Durante años, Woods", 1.0)),
    pv("Woods le dijo a David", "section", "David, de niño", dur=2.8, tam=300, **_I),

    # ---------------- 4 · jugador de BO3
    puesto("En el cuatro, el protagonista", 4, "El jugador de Black Ops 3", "CAMPAÑA / BLACK OPS 3 · 2015"),
    pv("En la segunda misión te operan", "m_newworld", "New World", dur=2.6, tam=300, **_D),
    mg_en(C.fallida("SOPORTE VITAL", "Mueres en la camilla"), "mueres en la camilla", 2.4, "fallida camilla"),
    pv("Taylor se conecta a tu cerebro", "taylor", "John Taylor", dur=2.8, tam=300, **_I),
    mg_en(C.objetivo("Todo lo demás", "Simulación con los recuerdos de Taylor"), "Todo lo que juegas después", 2.8, "objetivo simulacion",
          x=.30, y=.82),
    ficha("el doctor dice que el paciente", "New World", "«*He's a dead man anyway*».", "INTEL / BLACK OPS 3", dur=3.4, x=.73),
    pv("un soldado le pregunta su nombre", "m_life", "Life", dur=2.6, tam=300, **_D),
    placa("Taylor", ["Black Ops 3 · 2065", "Sin nombre · n.º 25954"], "kia", "Muerto desde la misión 2", de=("Y responde: Taylor", -.1),
          a=("Antes del tres, un comentario", -.05)),

    # ---------------- crítica 2 · @HdadDelJubileoensuEsperanza («¿Y Archer?»)
    com("Antes del tres, un comentario", "Ugzlg2I1GWc_pZ9Y_R94AaABAg", dur=6.0),
    mg_en(C.contador(3, "PALABRAS", "EL REPORTE MÁS CORTO"), "Es el reporte más corto", 2.4, "contador tres palabras", x=.30, y=.30),
    pv("Hoy sí sale", "archer", "The Archer", dur=2.8, tam=320, **_D),

    # ---------------- 3 · Gaz (post: «There is a line…»)
    puesto("Número tres. Gaz", 3, "Gaz · los dos", "CAMPAÑA / CoD 4 · MODERN WARFARE 4"),
    pv("Modern Warfare 4, Corea del Norte", "kumsusan", "Pyongyang · 2026", dur=2.6, tam=300, **_D),
    carr([("price_r", "Price"), ("ghost_r", "Ghost"), ("gaz_r", "Gaz")], de="Price, Ghost y Gaz, atados", a=("Gaz ya es capitán", -.05),
         marcas=["Price, Ghost", "y Gaz"], titulo="Atados a unas sillas"),
    mg_en(C.radio("GAZ · COUNTER ATTACK", "Escucha lo que le dice."), "Escucha lo que le dice", 3.2, "radio gaz", x=.5, y=.20),
    ficha("Entra el Archer", "Gaz", "«There is a line. *And it's one we don't cross*».", "INTEL / MODERN WARFARE 4", dur=3.4, x=.73),
    sil("el padre de Makarov", "archer", "The Archer", "Ministro de Defensa ruso", lado="izq", dur=3.6),
    mg_en(C.espejo("Las dos muertes de Gaz", ("CoD 4 · 2007", "Zakhaev", ["En el puente", "Herido y desarmado"], P("gaz")),
                   ("MW 4 · 2026", "El Archer", ["Atado a una silla", "Delante de Price"], P("gaz_r")), "LA MISMA MUERTE"),
          "Y el Gaz original", 5.4, "espejo gaz", y=.50),
    placa("Kyle Garrick", ["Capitán · SAS", "Modern Warfare 4 · 2026"], "kia", "Lo vengó Price", de=("Dos Gaz, dos villanos", -.1),
          a=("En el dos, Johnny", -.05)),

    # ---------------- 2 · Soap del reinicio (post: funeral)
    puesto("En el dos, Johnny", 2, "Johnny «Soap» MacTavish", "CAMPAÑA / MODERN WARFARE III · 2023"),
    pv("El túnel bajo el canal", "eurotunel", "Canal de la Mancha", dur=2.6, tam=300, **_D),
    mg_en(C.objetivo("Corta los dos cables", "A la de tres"), "guía a Price para cortar los cables", 2.6, "objetivo cables", x=.30, y=.82),
    pv("Entra Makarov", "makarov_r", "Makarov", dur=2.4, tam=280, **_I),
    pv("en las montañas de Escocia", "tf141", "Fuerza 141 · Escocia", dur=2.8, tam=300, **_D),
    ficha("El reinicio mató a Soap", "El funeral", "«*He was the best of us*».", "INTEL / MODERN WARFARE III", dur=3.4, x=.73),
    pv("matar a Shepherd en su propia oficina", "shepherd", "Shepherd · 2023", dur=2.8, tam=300, **_I),
    placa("Johnny MacTavish", ["Sargento · Fuerza 141", "Modern Warfare III · 2023"], "kia", "Yo no estaba en ese túnel",
          de=("La comunidad se lo tomó tan mal", -.1), a=("Y el número uno", -.05)),

    # ---------------- 1 · Price (post: «Gaz was right… Hold the line») + @itsmaibel7486 (mapa con ruta)
    puesto("Y el número uno", 1, "Capitán John Price", "CAMPAÑA / MODERN WARFARE 4 · GREATER GOOD"),
    pv("Price va preso en un convoy", "konni", "Konni", dur=2.6, tam=300, **_D),
    mapa("mundo", [(*_ll(39.03, 125.75, REC_P), "Pyongyang · Gaz", "inicio", P("gaz_r")), (*_ll(42.3, 130.6, REC_P), "Frontera rusa · el lago", "meta", P("price_r"))],
         de="Herido, persigue al Archer", a=("Llega Ghost", -.1), marcas=["Herido, persigue", "hasta un lago helado"],
         titulo="Greater Good", sub="20 de octubre de 2026", recorte=REC_P),
    mg_en(C.radio("PRICE · GREATER GOOD", "Su respuesta."), "Escucha lo que contesta Price", 3.6, "radio price", x=.5, y=.20),
    ficha("Gaz tenía razón", "Price", "«Gaz was right… *Hold the line*».", "INTEL / MODERN WARFARE 4", dur=3.6, x=.73),
    pv("Laswell borra los expedientes", "laswell", "Kate Laswell", dur=2.8, tam=300, **_I),
    leg("tf141", "PROGRAMA WATCHER", ["Gaz · borrado", "Ghost · borrado", "Price · borrado"], de="Bienvenidos al programa Watcher",
        a=("Maibel lo notó", 1.6), x=.78, y=.50),
    com("Maibel lo notó", "Ugx7rVqdGXavX78a8qJ4AaABAg", dur=6.2),
    pv("en el modo DMZ", "dmz", "DMZ", dur=2.4, tam=280, **_D),
    carr([("price_ww2", "Price · 1944"), ("price_r", "Price · 2026"), ("price", "Price · 2007")], de="Y hay tres Price en la saga",
         a=("El único que sobrevive", .3), marcas=["El de la Segunda Guerra", "El del reinicio", "El único que sobrevive"],
         titulo="Los tres Price"),
    placa("John Price", ["Capitán · SAS / Fuerza 141", "Modern Warfare 4 · 2026"], "kia", "Mantuvo la línea",
          de=("El de dos mil siete", -.4), a=("Expediente cerrado", -.05)),

    # ---------------- cierre
    mg_en(C.sello("CERRADO", "EXPEDIENTE 141"), "Expediente cerrado", 1.5, "sello cerrado", x=.33, y=.42),
    bajas("Veinte protagonistas, y la mayoría", ("Gracias a Keengan", -.05),
          tachados=("Soap", "Roach", "Ghost", "Yuri", "Jackson", "Allen", "Mason", "Woods", "Reznov", "Bell", "Case", "Price 2026", "Gaz 2026", "Soap 2023",
                    "Reyes", "BO3", "Al-Fulani"), titulo="LA MAYORÍA NO SALIÓ VIVA"),
    mg_en(C.logro("Datos del expediente", "Keengan · TMPLR5 · Maibel · Andrés · Hdad"), "Gracias a Keengan", 3.4, "logro gracias",
          x=.5, y=.30),
    com("Y v5x777 votó que se quede", "Ugw-012RdhJ69uFTBLV4AaABAg", dur=5.0, x=.62, y=.62),
    mg_en(C.objetivo("¿Quién merecía otro final?", "Escríbelo en los comentarios"), "qué protagonista crees", 3.0, "objetivo comentarios",
          x=.30, y=.82),
    pv("cómo murió cada villano", "makarov", "Cómo murió cada villano", dur=3.0, tam=320, **_D),
    mg_en(C.logro("Suscríbete", "Retírate, soldado"), "Suscríbete", 2.8, "logro suscribete", x=.5, y=.30),
]

PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_fallida", en="Y casi ninguno terminó", vol=.22),
    dict(sfx="cod_puesto", en="Número veinte. Nick Reyes", vol=.24),
    dict(sfx="cod_fallida", en="Todos lo dieron por muerto", vol=.22),
    dict(sfx="cod_puesto", en="Número dieciséis. El presidente", vol=.22),
    dict(sfx="cod_logro", en="Gracias, Andrés", vol=.22),
    dict(sfx="cod_puesto", en="Número trece. Case", vol=.22),
    dict(sfx="cod_puesto", en="Número once. Roach", vol=.22),
    dict(sfx="cod_fallida", en="nunca estuvo ahí", vol=.22),
    dict(sfx="cod_puesto", en="Número siete. Frank", vol=.22),
    dict(sfx="cod_puesto", en="Número cinco. Alex", vol=.22),
    dict(sfx="cod_fallida", en="mueres en la camilla", vol=.22),
    dict(sfx="cod_puesto", en="Número tres. Gaz", vol=.24),
    dict(sfx="cod_puesto", en="Y el número uno", vol=.26),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_loose", en=("Escucha lo que contesta Shepherd|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_reznov", en=("Escucha su despedida|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_soap", en=("Estas son sus últimas palabras|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_bell", en=("Antes, Adler le dice esto|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_gaz", en=("Escucha lo que le dice|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_soap23", en=("Ghost esparce sus cenizas|fin", .1), vol=1.0, voz=True),
    dict(sfx="s_price", en=("Escucha lo que contesta Price|fin", .1), vol=1.0, voz=True),
]

# ---- 2.ª capa de pegatinas y fichas (meta ≥ 5/min; se ajusta tras `chequeo`)
FX += [
    pv("Revisé el destino", "c_mw23", "Modern Warfare III", dur=2.2, **_D2),
    pv("Número veinte. Nick Reyes, Infinite", "c_iw", "Infinite Warfare · 2016", dur=2.4, **_D2),
    pv("se queda dentro del astillero", "retribution", "La Retribution", dur=2.6, **_I2),
    pv("El final: un tren", "c_gh", "Ghosts · 2013", dur=2.2, **_I2),
    pv("Número dieciocho. Alex", "c_mw19", "Modern Warfare · 2019", dur=2.2, **_D2),
    pv("Despiertas entre los restos", "jackson", "Paul Jackson", dur=2.6, **_D2),
    pv("Te desplomas", "pelayo", "Capitana Pelayo", dur=2.2, **_I2),
    pv("Te llevan en el asiento", "m_coup", "The Coup", dur=2.2, **_D2),
    pv("a la misión del aeropuerto", "m_norussian", "No Russian", dur=2.4, **_I2),
    pv("en el hotel de Dubái", "price", "Price · 2017", dur=2.2, **_D2),
    pv("Número trece. Case, el protagonista", "case", "Case", dur=2.6, **_D2),
    pv("Por la radio, Marshall", "marshall", "Troy Marshall", dur=2.4, **_I2),
    pv("Y ese juego volvió oficial", "harper", "Mike Harper", dur=2.2, **_I2),
    pv("Karma viva", "karma", "Karma", dur=2.2, **_D2),
    pv("Un disparo, una zanja", "m_loose", "Loose Ends", dur=2.4, **_D2),
    pv("Al final de Modern Warfare 4, es el único", "ghost_r", "Ghost · 2026", dur=2.6, **_I2),
    pv("Y todo el Reznov que acompaña", "m_vorkuta", "Vorkuta", dur=2.2, **_D2),
    pv("En Modern Warfare 3, en Praga", "praga", "Praga · 2016", dur=2.4, **_I2),
    pv("Makarov sabe. Yuri", "makarov", "Makarov", dur=2.4, **_D2),
    pv("En el seis, Bell", "c_cw", "Cold War · 2020", dur=2.2, **_D2),
    pv("Los dos sacan la pistola", "m_countdown", "The Final Countdown", dur=2.4, **_D2),
    pv("y es Mason", "m_suffer", "Suffer With Me", dur=2.2, **_I2),
    pv("Lo mató Woods", "woods", "Frank Woods", dur=2.2, **_I2),
    pv("El que no tiene nombre", "c_bo3", "Black Ops 3 · 2015", dur=2.2, **_D2),
    pv("Al final, en blanco y negro", "player_bo3", "El jugador", dur=2.4, **_I2),
    pv("en el puente, a manos de Zakhaev", "gaz", "Gaz · 2007", dur=2.4, **_I2),
    pv("Modern Warfare 3, dos mil veintitrés", "soap_r", "Soap · 2023", dur=2.6, **_D2),
    pv("Soap se levanta", "m_trojan", "Trojan Horse", dur=2.2, **_D2),
    pv("Modern Warfare 4, la última misión", "m_greater", "Greater Good", dur=2.4, **_D2),
    pv("Ghost le toma la mano", "ghost_r", "Ghost", dur=2.4, **_D2),
    pv("El de la Segunda Guerra Mundial", "m_tirpitz", "Acorazado Tirpitz", dur=2.4, **_D2),
    ficha("Al-Fulani, la primera misión", "The Coup", "La primera misión de *Call of Duty 4*.", "INTEL / CALL OF DUTY 4", dur=3.0, x=.73),
    ficha("El final: un tren que cae", "The Ghost Killer", "La última misión de *Ghosts*.", "INTEL / GHOSTS", dur=3.0, x=.73),
    ficha("Muere en la última misión, en el hotel", "Dust to Dust", "Hotel Oasis, *Dubái*, 2017.", "INTEL / MODERN WARFARE 3", dur=3.0),
    ficha("En la segunda misión te operan", "New World", "Zúrich, *2065*.", "INTEL / BLACK OPS 3", dur=3.0),
    ficha("Herido, persigue al Archer", "Greater Good", "La *última misión* del reinicio.", "INTEL / MODERN WARFARE 4", dur=3.0),
]

# ---- 3.ª capa (fx --seco 24-nov: 14 huecos de > 4 s sin MG ni pegatina)
FX += [
    ficha("Sale despedido al vacío", "Astillero de Tharsis", "En órbita de *Marte*.", "INTEL / INFINITE WARFARE", dur=3.4, x=.73),
    ficha("Pero en el código del juego", "El código", "Tres objetivos *que nunca se usaron*.", "INTEL / CALL OF DUTY 4", dur=3.0, x=.73),
    pv("El cuerpo de un estadounidense", "c_mw2", "Modern Warfare 2 · 2009", dur=2.8, **_D2),
    pv("No terminó. En Black Ops 7", "c_bo7", "Black Ops 7 · 2035", dur=2.8, **_I2),
    pv("Lo que nunca le dieron a Roach", "roach", "Roach · sin voz", dur=3.0, **_D2),
    mg_en(C.radio("ROACH · CLIFFHANGER", "Su único grito."), "su único grito", 2.8, "radio roach", x=.5, y=.20),
    mg_en(C.fallida("EL CALENDARIO", "Causa de muerte: 104 años"), "Lo único que lo pudo matar", 2.6, "fallida calendario"),
    mg_en(C.radio("NEW WORLD · QUIRÓFANO", "«He's a dead man anyway»."), "El protagonista contesta que", 3.4, "radio quirofano",
          x=.5, y=.20),
    ficha("Hablaba de sí mismo", "El jugador", "Hablaba *de sí mismo*.", "INTEL / BLACK OPS 3", dur=3.0, x=.73),
    pv("Gaz ya es capitán", "gaz_r", "Capitán Kyle Garrick", dur=3.0, **_I2),
    pv("Ghost lo embosca", "ghost_r", "Ghost · la emboscada", dur=2.8, **_I2),
    mg_en(C.marcador("Convoy de Konni", 60, "El Archer dentro"), "el camión choca", 2.6, "marcador convoy", x=.55, y=.36),
    mg_en(C.fallida("PRICE · K.I.A.", "Greater Good · 2026"), "El programa sigue. Price, no", 2.6, "fallida price"),
    aba([("rorke", "Keengan · Rorke"), ("ghost_r", "TMPLR5 · Ghost"), ("laswell", "Maibel · Watcher"), ("archer", "Hdad · Archer")],
        de="por los datos de este expediente", a=("Y v5x777 votó", -.05),
        marcas=[("por los datos de este", 0), ("por los datos de este", .5), ("por los datos de este", 1.0), ("por los datos de este", 1.5)],
        nombre="gracias datos"),
    mg_en(C.logro("Voto anotado", "La votación sigue abierta"), "el voto está anotado", 2.6, "logro voto", x=.5, y=.30),
    pv("Los mejores comentarios salen", "tf141", "Expediente 141", dur=3.2, **_I2),
]
