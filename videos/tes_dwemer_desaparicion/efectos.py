# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «¿Qué pasó con los DWEMER? Los 20 secretos…» (SECUENCIA YT, Crónicas de Tamriel, 4-nov-2026).
REGLA DE ORO (tes_secretos_40) + «sin tramos vacíos»: kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras:
- 20 avisos (uno por secreto) arriba al centro; fichas de inventario SOLO con datos de UESP (`_investigacion.md`).
- Pegatinas REALES (Fandom) en todos los estilos de `nucleo/peg_estilos.py` (silueta, reliquia, banda, camafeo, legajo, abanico).
- Comentarios REALES de ≤ 10 días: petición (@chuymoreno6820), corrección justa (@federicoherrera2105), 5 agradecimientos, 2 críticas
  con burla (voz femenina, «kyrim») y el recuento de votos de Sentinel.
- MG NUEVO de este guion: `destello` (todos los dwemer se borran a la vez y queda ceniza; mg_tes) + recuento de votos (barras),
  receta del experimento (Kagrenac y Arniel), cadena de los falmer, cuatro versiones de la Montaña Roja (lecturas), cronología del
  Numidium, balanza razón/fe.
- Mapas reales con ruta (coordenadas de UESP, `_coords_uesp.py`): Blackreach, Alftand, la Forja del Aeterio, Mzulft, Septimus →
  Mzark, Markarth, Bthardamz; Morrowind (Montaña Roja, Tel Fyr, Mournhold).
  python fab.py tes_dwemer_desaparicion fx --seco   tiempos      python fab.py tes_dwemer_desaparicion fx hoja   previews/fx_NN.jpg
"""
import os

import mg_tes as T
import mg_wow as W
import peg_estilos as PE


def _cad(titulo, pasos, **kw):
    """mg_tes.cadena pide (texto, ruta|None): «Nombre · detalle» sin retrato."""
    return T.cadena(titulo, [(f"{a} · {b}", None) for a, b in pasos], **kw)


CAMARA = {}
FUNDIDO = {}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def ficha(en, nombre, efecto, origen=None, dur=4.5, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def peg(en, slug, titulo, dur=3.5, x=.17, y=.62, tam=400, giro=-6.0):
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.0, x=.25, tam=640):
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def sil(en, slug, nombre=None, sub=None, dur=4.5, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mis(en, arriba, titulo, dur=3.0, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam, giro=-3.0)


def aviso(en, n, titulo, dur=3.4):
    return dict(tipo="mg", fn=T.mision(f"Secreto · número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mapa(img, titulo, puntos, de, a, marcas, sub, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, img), puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=.5, sale=.5, nombre="mapa " + sub, ver=4.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


# coordenadas reales (UESP → mapas/skyrim.jpg, `_coords_uesp.py`, 4-nov-2026)
ALFTAND, MZINCH, RALDB = (.663, .281), (.504, .262), (.687, .452)
ARKNG, DEEPF, BTHALFT, MZULFT, ALMACEN = (.188, .596), (.115, .332), (.695, .755), (.868, .543), (.868, .557)
BTHARD, SEPTIM, COLEGIO, LABY = (.127, .371), (.740, .097), (.744, .183), (.450, .382)
MARKARTH, UNDERST, WINTERH, WINDHELM, DAWNSTAR, KAGRENZ = (.108, .488), (.097, .493), (.729, .208), (.792, .402), (.555, .198), (.923, .590)
# mapas/morrowind.jpg (provincia, ESO): a ojo sobre el dibujo — Montaña Roja = mancha roja del centro de Vvardenfell
MONTANA, TELFYR, MOURNHOLD = (.436, .379), (.61, .45), (.52, .66)


def pt(xy, nombre, tipo, foto=None):
    return (xy[0], xy[1], nombre, tipo) + ((P(foto),) if foto else ())


# comentarios (≤ 10 días)
C_CHUY, C_FEDE, C_MIGUEL, C_MELVAL, C_SHADOW = ("UgxBTdS9KvH1sufKm7F4AaABAg", "UgwNcSsvmI-euGxgzh14AaABAg", "Ugydd3_GmGgJNQFdGoV4AaABAg",
                                                "UgwA1RvZeaaO1sTrCWB4AaABAg", "UgzSA8Xd7u6zPs6LWfN4AaABAg")
C_MOON, C_MINE, C_GALINA, C_KYRIM = "UgzM4KMdw79jp6v8ZZd4AaABAg", "UgxSVgWrGtUESixL3NR4AaABAg", "Ugxo0a-MaJTRje72hA54AaABAg", "UgzJYFZJk-eBnw3xQoB4AaABAg"
C_PROF1, C_PROF2, C_MARI, C_HOPE, C_JOHN, C_TURNO = ("UgzfgAVrwRxAYfhaZTp4AaABAg", "Ugxa5P-s_uj4Q8ssMkV4AaABAg", "UgzURnqqeHP9q-eWUgB4AaABAg",
                                                    "UgxeGas2--5GzKT2Oll4AaABAg", "UgyCXtnEuOmGjrR91Nd4AaABAg", "Ugxv_RgJeOEXswzRyL14AaABAg")

FX = [
    # ---------------- GANCHO: un elemento nuevo cada 2-3 s
    zoom(0.0, "Y un día, en un solo instante", 1.14),
    mis("Una raza entera", "Crónicas de Tamriel", "Los dwemer", dur=2.6, y=.22),
    peg("Ciudades bajo tierra", "blackreach", "Blackreach", dur=2.2, x=.18, y=.64, tam=380, giro=5),
    rel("máquinas de vapor", "centurion", "Centurión enano", "Sigue encendido", dur=2.4, x=.80, y=.52, tam=440),
    cam("un dios de latón", "numidium", "Numidium", dur=2.2, x=.16, y=.66, foco=(.5, .4, 1.3)),
    mg(T.destello("Los dwemer", 60, ("NADIE", 2)), "en un solo instante", ("No dejaron ni una tumba", .2),
       ["en un solo instante", "en un solo instante", "nadie"], "destello gancho", y=.42),
    mg_en(T.contadores("Desde que desaparecieron", [("Años", 3750, None, None)], remate=("Y SIGUEN TRABAJANDO", 0)),
          "casi cuatro mil años", 3.6, "anios gancho", x=.70, y=.34),
    sil("como si el jefe fuera a volver", "centurion", "Centurión", "Esperando a su amo", dur=3.0, lado="der", alto=860),
    mis("el misterio más grande", "The Elder Scrolls", "El mayor misterio", dur=3.0, y=.30),
    com("Nos lo pidió @chuymoreno6820", C_CHUY, dur=7.0, x=.50, y=.40, tam=1000),
    mis("Veinte secretos", "Crónicas de Tamriel", "20 secretos de los dwemer", dur=3.2, y=.22),
    ficha("todos comprobados en UESP", "Fuentes", "Cada dato con su enlace de *UESP*", "En la descripción", dur=3.0),
    peg("por qué los llamas enanos", "gigante", "¿Enanos?", dur=2.4, x=.18, y=.64, tam=360, giro=-5),
    cam("con tus propias manos", "arniel", "Arniel Gane", dur=2.8, x=.84, y=.66),
    mis("vuelven las siete voces", "Ronda 2", "Siete voces compiten", dur=3.4, y=.30),

    # ---------------- recuento real de votos (Sentinel)
    mg(T.barras("Recuento de votos · Sentinel", [(None, "El Profeta", 4, 0, T.ORO), (None, "Hope", 2, 1, T.HUESO),
                                                (None, "MariCarmen", 2, 1, T.HUESO), (None, "Johnny", 2, 1, T.HUESO),
                                                (None, "Edoardo · José · Mario", 0, 2, T.SANGRE)], unidad=" votos",
                remate=("PRIMERAS HORAS", 3)),
       "Recuento de los comentarios", ("Ni su madre", .6), ["El Profeta, cuatro", "Hope, dos", "Y Edoardo", "Ni uno"], "recuento", y=.44),
    com("El Profeta, cuatro votos", C_PROF1, dur=3.0, x=.18, y=.20, tam=560),
    com("Hope, dos", C_HOPE, dur=2.6, x=.82, y=.20, tam=560),
    com("Yo, Johnny, dos", C_JOHN, dur=2.6, x=.18, y=.84, tam=560),

    # ---------------- 20 · no eran enanos
    aviso("Número veinte", 20, "No eran enanos"),
    aba([("centurion", "Centurión enano"), ("esfera", "Esfera enana"), ("arana", "Araña enana")], "En Skyrim todo es enano",
        ("los dwemer no eran bajitos", .3), ["Ruinas enanas", "armadura enana", "esferas enanas"], "todo enano"),
    ficha("Dwemer significa", "Dwemer", "«El pueblo *profundo*» · elfos de lo hondo", "Deep-Elves / Deep Folk", dur=5.0),
    mg(_cad("Familia de los mer", [("Altmer", "Altos elfos"), ("Dunmer", "Elfos oscuros"), ("Dwemer", "Los profundos")]),
       "Eran mer, elfos", ("elfos oscuros", 1.0), ["Eran mer", "primos de los altmer", "elfos oscuros"], "familia mer", y=.35),
    sil("de los gigantes", "gigante", "Gigante", "Les puso el mote", dur=4.4, lado="der", alto=900),
    mis("cualquier elfo es pequeño", "Para un gigante", "Todos son enanos", dur=3.0, y=.72),
    mis("Como si a ti te bautizara un mamut", "Bautizo", "Por un mamut", dur=2.8, y=.30),
    cam("Sotha Sil", "sotha_sil", "Sotha Sil", dur=3.4, x=.16, y=.66, foco=(.5, .25, 2.0)),
    ficha("los hijos del latón", "Hijos del latón", "Así los llamaba *Sotha Sil*", "Dios de Morrowind", dur=4.0),

    # ---------------- 19 · las máquinas que nadie apagó
    aviso("En el diecinueve", 19, "Las máquinas que nadie apagó"),
    aba([("arana", "Araña"), ("esfera", "Esfera"), ("centurion", "Centurión")], "Las arañas, las esferas y los centuriones",
        ("se llaman animunculi", 1.0), ["Las arañas", "las esferas", "los centuriones"], "animunculi"),
    ficha("siguen funcionando en ciudades perdidas", "Animunculi", "Siguen haciendo *el trabajo de sus amos*", "UESP", dur=5.0),
    rel("La araña se esconde en las tuberías", "arana", "Araña enana", "Salta desde las tuberías", dur=3.4, x=.78, y=.52, tam=440),
    rel("La esfera llega rodando", "esfera", "Esfera enana", "Se despliega · a veces con ballesta", dur=3.8, x=.22, y=.52, tam=460),
    sil("el centurión espera inmóvil", "centurion", "Centurión enano", "Golpea como un dragón", dur=5.0, lado="der", alto=900),
    mg(T.barras("Golpe", [(None, "Dragón", 10, 0, T.HUESO), (None, "Centurión enano", 10, 1, T.ORO)], remate=("A LA ALTURA", 2)),
       "Escupe vapor", ("de un dragón", .8), ["Escupe vapor", "sus golpes", "de un dragón"], "golpe dragon", y=.32),
    mis("Truco: no puede bajar los brazos", "Truco", "Pégate a sus pies", dur=4.2, y=.72),
    ficha("siempre suelta su núcleo dinamo", "Núcleo dinamo de centurión", "Botín *garantizado* + gema de alma enorme", "Centurión enano", dur=4.6),
    mapa("skyrim.jpg", "Skyrim", [pt(BTHARD, "Bthardamz", "meta", "bthardamz")], "solo uno en todo Skyrim patrulla", ("esperando", .8),
         ["patrulla", "Los demás llevan milenios"], "El único centurión que patrulla", ventana=True, ancho=1000, x=.30, y=.45),
    mg_en(T.contadores("Turno de los animunculi", [("Años sin vacaciones", 3750, None, None), ("Sindicatos", 0, None, None)]),
          "Casi cuatro mil años sin vacaciones", 5.0, "vacaciones", x=.70, y=.34),

    # ---------------- 18 · vives dentro de una ciudad dwemer
    aviso("Número dieciocho", 18, "Vives dentro de una ciudad dwemer"),
    grande("Markarth, la capital del Reach", "markarth", "Markarth · el Reach", dur=4.4, x=.28, tam=640),
    mapa("skyrim.jpg", "Skyrim", [pt(MARKARTH, "Markarth", "inicio", "markarth"), pt(UNDERST, "Understone Keep", "meta", "understone")],
         "Las calles, las cascadas", ("tallado en la montaña", .6), ["Las calles", "Understone Keep"], "Markarth, ciudad dwemer",
         ventana=True, ancho=1000, x=.70, y=.45),
    ficha("Understone Keep, es el viejo palacio", "Understone Keep", "El castillo del yarl = *palacio dwemer*", "Markarth", dur=5.0),
    mis("Los humanos solo se mudaron", "Markarth", "Inquilinos", dur=2.8, y=.72),
    peg("la ciudad original, Nchuand-Zel", "nchuand_zel", "Nchuand-Zel", dur=3.8, x=.80, y=.62, tam=440, giro=5),
    cam("sin hacer caso al sabio", "calcelmo", "Calcelmo", dur=2.8, x=.16, y=.66, foco=(.5, .22, 2.4)),
    mg(T.informe("La expedición perdida", (P("nchuand_zel"), "Nchuand-Zel"),
                 [("1", "Alethius", 0), ("2", "Stromm", 0), ("3", "Erj", 1), ("4", "Krag", 1), ("5", "Staubin", 2)], sello=("DEFENSAS ACTIVAS", 3)),
       "Encuentras sus cuerpos", ("las defensas de los dwemer", .8), ["Encuentras sus cuerpos", "uno a uno", "la última palanca", "vuelve a encender"],
       "expedicion perdida", y=.46),
    mis("estás en el salón de otro", "Recordatorio", "El dueño no se ha ido", dur=4.0, y=.72),

    # ---------------- 17 · Calcelmo y su piedra
    aviso("En el diecisiete", 17, "El experto y su piedra"),
    sil("Calcelmo, el mago altmer", "calcelmo", "Calcelmo", "El mayor experto en los dwemer", dur=5.0, lado="izq", alto=880),
    grande("Tiene un museo propio", "museo_dwemer", "Museo dwemer · Markarth", dur=3.6, x=.74, tam=600),
    mis("cuidado con las vitrinas", "Calcelmo", "«Cuidado con las vitrinas»", dur=3.4, y=.80),
    rel("una losa enorme", "piedra_calcelmo", "Piedra de Calcelmo", "Dwemer y falmer grabados", dur=4.6, x=.76, y=.52, tam=520),
    mis("Respuestas difíciles", "Gremio de Ladrones", "Respuestas difíciles", dur=3.4, y=.30),
    ficha("con carbón y papel", "Calco de la piedra", "Carbón + *papel*", "Respuestas difíciles", dur=4.0),
    rel("En Enanos, tercer volumen", "libro_enanos3", "Enanos, vol. III", "Calcelmo", dur=4.0, x=.22, y=.52, tam=440),
    mg(T.cronologia("¿Cuánto tardaron en desaparecer?", [("¿Un día?", "Sin pruebas", 0), ("¿Años?", "Posible", 1), ("¿Décadas?", "Posible", 2)]),
       "no hay prueba de que desaparecieran", ("O décadas", .8), ["no hay prueba", "Pudieron ser años", "O décadas"], "cuanto tardaron", y=.30),
    mg(T.informe("Hipótesis de Calcelmo", (P("calcelmo"), "Calcelmo"),
                 [("1", "Una peste", 0), ("2", "Magia contaminada", 1), ("3", "Experimentos con Aetherius", 2), ("4", "Un viaje a Oblivion", 3)],
                 sello=("NO SABE", 4)),
       "Y no descarta nada", ("Por eso es el mayor experto", .6), ["una peste", "magia contaminada", "experimentos con Aetherius",
                                                                  "un viaje a Oblivion", "no sabe"], "hipotesis calcelmo", y=.46),

    # ---------------- CORRECCIÓN · @federicoherrera2105 (queja justa)
    mis("hoy toca correo", "Correo del canal", "Corrección", dur=2.6, y=.18),
    com("nos dijo que no podemos decir", C_FEDE, dur=8.0, x=.50, y=.40, tam=1000),
    mg(_cad("Pronunciación", [("Jarl", "Como se escribe"), ("Yarl", "Como se dice")]), "Se dice yarl", ("no es Oblivión", -.2),
       ["Tiene toda la razón", "Se dice yarl"], "yarl", y=.72),
    mg(_cad("Pronunciación", [("Oblivión", "Agudo"), ("Oblivion", "Como se dice")]), "no es Oblivión", ("Ya has oído", -.1),
       ["no es Oblivión", "Es Oblivion"], "oblivion", y=.72),
    mg_en(T.contadores("Yarls bien dichos", [("Por Edoardo", 2, None, None)], remate=("CUÉNTALAS", 0)), "Ya has oído a Edoardo", 4.0,
          "yarls", x=.70, y=.34),

    # ---------------- 16 · los falmer
    aviso("Número dieciséis", 16, "Los falmer no eran monstruos"),
    cam("los elfos de las nieves", "elfo_nieves", "Elfos de las nieves", dur=3.4, x=.16, y=.66, foco=(.5, .3, 1.6)),
    sil("los nórdicos de Ysgramor", "ysgramor", "Ysgramor", "Los echó hacia el sur", dur=4.4, lado="der", alto=880),
    mg(_cad("Cómo se hace un falmer", [("Elfos de las nieves", "Casi extinguidos"), ("Refugio", "Con los dwemer"),
                                           ("Hongos tóxicos", "Ciegos"), ("Esclavos", "Bajo tierra")]),
       "pidieron refugio a sus primos", ("esclavos ciegos", 1.0), ["pidieron refugio", "A cambio de un precio", "hongos tóxicos", "esclavos ciegos"],
       "cadena falmer", y=.32),
    sil("esclavos ciegos", "falmer", "Falmer", "Cegados por los dwemer", dur=4.0, lado="izq", alto=860),
    ficha("Las cámaras de tortura", "Cámaras de tortura", "Para *controlar* a los falmer", "Ruinas dwemer", dur=4.6, rojo=True),
    mis("La guerra del Risco", "Rebelión falmer", "La guerra del Risco", dur=3.4, y=.30),
    mis("el enemigo dejó de estar", "La guerra acaba", "Sin enemigo", dur=3.6, y=.72),

    # ---------------- 15 · la batalla que nunca empezó
    aviso("En el quince", 15, "La batalla que nunca empezó"),
    rel("Los falmer, un estudio", "libro_falmer", "Los falmer: un estudio", "Ursa Uthrax", dur=4.6, x=.78, y=.52, tam=460),
    peg("en el museo de Calcelmo", "museo_dwemer", "Museo dwemer", dur=3.0, x=.18, y=.62, tam=380, giro=-4),
    mis("la última batalla", "Guerra del Risco", "La batalla final", dur=3.0, y=.30),
    mg(T.destello("Los dwemer · el día de la batalla", 40, ("LA RAZA ENTERA, DESAPARECIDA", 2)), "Y se encontraron con que",
       ("había desaparecido", 1.4), ["Y se encontraron", "había desaparecido", "había desaparecido"], "destello falmer", y=.42),
    mis("que el otro no se presente", "Venganza", "Cancelada por ausencia", dur=4.0, y=.72),
    sil("Hoy los encuentras en casi cada ruina", "falmer", "Falmer", "Todavía ahí abajo", dur=4.0, lado="der", alto=860),
    ban("Ysgramor les cortaba la nariz", "falmer", "Falmer", "Sin nariz, según los nórdicos", foco=(.5, .32, 2.2), dur=4.6, y=.70),

    # ---------------- 14 · Blackreach
    aviso("Número catorce", 14, "Hay un mundo debajo de Skyrim"),
    pant("blackreach", "Blackreach. Una caverna", ("solo te enseña una parte", .6), zoom=(1.0, 1.12)),
    mapa("skyrim.jpg", "Las puertas de Blackreach", [pt(ALFTAND, "Alftand", "inicio", "alftand"), pt(MZINCH, "Mzinchaleft", "paso", "mzinchaleft"),
                                                     pt(RALDB, "Raldbthar", "meta", "raldbthar")],
         "Se entra por tres ruinas", ("una esfera de sintonía", .6), ["Alftand", "Mzinchaleft", "Raldbthar"], "Tres entradas a Blackreach"),
    ficha("una esfera de sintonía", "Esfera de sintonía", "Abre las *tres* entradas", "Blackreach", dur=3.6),
    mis("una ciudad muerta", "Blackreach", "La ciudad silenciosa", dur=3.0, y=.30),
    mis("un gran globo naranja", "Grito", "Fuerza Implacable", dur=3.0, y=.30),
    rel("viene un dragón: Vulthuryol", "vulthuryol", "Vulthuryol", "Solo una vez", dur=4.0, x=.76, y=.52, tam=460),
    rel("la raíz Nirn carmesí", "nirn_carmesi", "Raíz Nirn carmesí", "Solo en Blackreach", dur=4.2, x=.22, y=.52, tam=460),
    mg_en(T.contadores("Encargo de Sinderion", [("Raíces Nirn carmesí", 30, None, None)], remate=("DONDE LLORASTE", 0)),
          "si alguna vez un elfo te pidió treinta", 4.4, "nirn 30", x=.70, y=.34),

    # ---------------- 13 · Alftand
    aviso("En el trece", 13, "Los que bajaron a buscarlos"),
    mapa("skyrim.jpg", "Skyrim", [pt(WINTERH, "Hibernalia", "inicio"), pt(ALFTAND, "Alftand", "meta", "alftand")],
         "Alftand, al suroeste de Hibernalia#2", ("tesoros dwemer", .6), ["Una expedición imperial", "excavó el glaciar"], "Alftand",
         ventana=True, ancho=1000, x=.70, y=.45),
    cam("la de Sulla Trebatius", "sulla", "Sulla Trebatius", dur=3.0, x=.16, y=.66),
    mg(T.informe("Expedición de Alftand", (P("alftand"), "Alftand"),
                 [("1", "Valie · sala de tortura", 0), ("2", "Endrast · huyó de los falmer", 1), ("3", "J'zhar · muerto", 2),
                  ("4", "J'darr · hostil", 2)], sello=("BAJAS", 3)),
       "Lo que encuentras es su lista", ("y hostil contigo", .8), ["Valie", "Endrast", "J'zhar", "hostil contigo"], "alftand bajas", y=.46),
    sil("Y J'darr, con un hacha", "jdarr", "J'darr", "De pie sobre su hermano", dur=3.6, lado="der", alto=860),
    aba([("sulla", "Sulla"), ("umana", "Umana")], "Sulla y Umana", ("Y casi siempre gana Umana", 1.2), ["Sulla y Umana", "gana Umana"], "sulla umana",
        x=.30, y=.64),
    mis("Moraleja", "Moraleja", "Buscar dwemer, desaparecer", dur=4.2, y=.30),

    # ---------------- AGRADECIMIENTOS
    mis("esta para dar las gracias", "Correo del canal", "Gracias", dur=4.0, y=.16),
    com("@Miguel_Salvatierra dice", C_MIGUEL, dur=9.0, x=.30, y=.42, tam=760),
    com("@MelVal54, muchas gracias", C_MELVAL, dur=4.0, x=.70, y=.30, tam=640),
    com("@MoonrakerYo79, gracias", C_MOON, dur=4.0, x=.32, y=.62, tam=640),
    com("@ShadowPriestBear dice", C_SHADOW, dur=6.0, x=.66, y=.46, tam=720),
    com("@minecrafttv2081 se rio", C_MINE, dur=5.0, x=.40, y=.38, tam=760),
    mis("Leemos todos los comentarios", "Siempre", "Los leemos todos", dur=6.0, y=.16),
    mis("Mario, ¿esto era correr menos?", "Mario", "Prometió correr menos", dur=2.6, y=.72),

    # ---------------- 12 · construían con sonido
    aviso("Número doce", 12, "Construían con sonido"),
    rel("arquitectos tonales", "resonador", "Arquitectura tonal", "El sonido cambia la realidad", dur=5.0, x=.76, y=.52, tam=500),
    ficha("collares mágicos", "Arquitecto tonal", "Su *voz*, amplificada con torques", "UESP", dur=4.4),
    mg(T.ruleta("Lo que hacía un resonador", [("Calma", T.HUESO), ("Placer", T.ORO), ("Paranoia", T.SANGRE), ("Terror", T.SANGRE)], [0, 1, 2, 3]),
       "fabricaban resonadores", ("o terror", .8), ["calma", "placer", "paranoia", "terror"], "resonadores", y=.40),
    mapa("skyrim.jpg", "Skyrim", [pt(MARKARTH, "Markarth", "inicio"), pt(ARKNG, "Arkngthamz", "meta", "arkngthamz")],
         "En Arkngthamz, una ruina", ("golpear en orden", .6), ["Arkngthamz", "cinco resonadores"], "Arkngthamz · el Reach",
         ventana=True, ancho=1000, x=.70, y=.45),
    mg(T.soldados("Fallos en la cerradura tonal", 3, remate=("ARAÑAS · ESFERAS · CENTURIÓN", 2), cols=3, ancho=760),
       "Cada vez que fallas", ("te dispara", .4), ["primero arañas", "luego esferas", "luego un centurión"], "fallos tonal", x=.30, y=.42),
    mis("el jefe de esos arquitectos", "Recuerda el nombre", "Kagrenac", dur=4.4, y=.30),

    # ---------------- 11 · la forja del aeterio
    aviso("En el once", 11, "La guerra contra sí mismos"),
    ficha("Las guerras del aeterio", "Las guerras del aeterio", "Cuatro ciudades dwemer · *tres años*", "Dawnguard · Taron Dreth", dur=5.0),
    mg(T.soldados("Ciudades dwemer alrededor de Arkngthamz", 4, remate=("HUNDIDAS EN 3 AÑOS", 2), cols=4, ancho=820),
       "cuatro ciudades dwemer", ("un cristal azul que brilla", .4), ["cuatro ciudades", "en solo tres años"], "cuatro ciudades", y=.40),
    sil("la guía Katria", "katria", "Katria", "Fantasma de Arkngthamz", dur=5.0, lado="der", alto=880),
    mapa("skyrim.jpg", "Los fragmentos de aeterio", [pt(ARKNG, "Arkngthamz", "inicio", "arkngthamz"), pt(DEEPF, "Cruce del Pueblo Profundo", "paso"),
                                                     pt(RALDB, "Raldbthar", "paso", "raldbthar"), pt(ALMACEN, "Almacén enano", "paso"),
                                                     pt(BTHALFT, "Ruinas de Bthalft", "meta", "bthalft")],
         "Juntas cuatro fragmentos", ("baja a la forja", 1.0), ["de Arkngthamz, del Cruce", "del Cruce", "de Raldbthar", "un almacén", "Bthalft"],
         "La ruta de la forja"),
    grande("un ascensor baja a la forja", "forja_aeterio", "La Forja del Aeterio", dur=3.6, x=.74, tam=600),
    aba([("corona_aeterea", "Corona"), ("escudo_aetereo", "Escudo"), ("baculo_aetereo", "Báculo")], "solo puedes hacer una pieza",
        ("una araña o una esfera", .8), ["la corona", "el escudo", "o el báculo"], "piezas aeterio", x=.30, y=.62),
    rel("su arco, Céfiro", "zephyr", "Céfiro", "Dispara un 30 % más rápido", dur=4.4, x=.76, y=.52, tam=480),
    mis("cuídamelo bien", "Katria", "«Cuídamelo bien»", dur=3.0, y=.80),

    # ---------------- 10 · Mzulft y el oculario
    aviso("En el diez", 10, "La máquina que ve todo Skyrim"),
    mapa("skyrim.jpg", "Skyrim", [pt(WINDHELM, "Ventalia", "inicio"), pt(MZULFT, "Mzulft", "meta", "mzulft")],
         "Mzulft, al sur de Ventalia", ("a casi todos", .6), ["Mzulft, al sur", "el Sínodo"], "Mzulft · Eastmarch", ventana=True, ancho=1000, x=.30, y=.45),
    cam("Gavros Plinius", "gavros", "Gavros Plinius", dur=3.4, x=.84, y=.66, foco=(.5, .4, 1.4)),
    mis("busca a Paratus", "Últimas palabras", "«Busca a Paratus»", dur=3.4, y=.72),
    grande("El oculario es una máquina dwemer", "oculario", "El oculario de Mzulft", dur=4.4, x=.72, tam=640),
    mg(_cad("Ajustar el oculario", [("Cristal", "En el armilar"), ("Escarcha", "Acerca las lentes"), ("Fuego", "Las aleja")]),
       "Le pones el cristal", ("un mapa entero de Skyrim", .8), ["Le pones el cristal", "con escarcha", "y con fuego", "proyecta un mapa"], "oculario receta", y=.40),
    mapa("skyrim.jpg", "La proyección", [pt(MZULFT, "Mzulft", "inicio", "oculario"), pt(LABY, "Labyrinthian", "meta", "baculo_magnus")],
         "el bastón de Magnus", ("Nerien", .6), ["el bastón de Magnus", "Labyrinthian"], "El bastón de Magnus"),
    cam("Orden Psijic, Nerien", "nerien", "Nerien", dur=2.8, x=.16, y=.66),
    mg_en(T.contadores("Mzulft", [("Lingotes dwemer", 498, None, None)], remate=("RÉCORD DE SKYRIM", 0)), "Hasta cuatrocientos noventa y ocho",
          4.4, "498 lingotes", x=.70, y=.34),

    # ---------------- CRÍTICA · voz femenina (Hope y MariCarmen)
    mis("esta va por nosotras", "Correo del canal", "Crítica", dur=2.6, y=.18),
    com("qué ridícula la voz femenina", C_GALINA, dur=6.0, x=.50, y=.38, tam=1000),
    mg(T.barras("Votos de las voces femeninas", [(None, "Hope", 2, 0, T.ORO), (None, "MariCarmen", 2, 1, T.ORO), (None, "Johnny", 2, 1, T.HUESO),
                                                (None, "Tres señores", 0, 2, T.SANGRE)], unidad=" votos", remate=("EMPATE TÉCNICO", 3)),
       "Y yo tengo dos votos", ("Gracias por escucharnos", -.1), ["Y yo tengo dos", "Y yo otros dos", "empata con Johnny", "tres señores"],
       "votos femeninas", y=.46),
    mis("vota por la menos ridícula", "Hope", "La menos ridícula", dur=3.4, y=.72),

    # ---------------- 9 · el oculario de la Torre de Mzark
    aviso("Número nueve", 9, "Leían los Pergaminos con una máquina"),
    cam("se quedaba ciego leyendo", "pergamino_dragon", "Pergamino Antiguo", dur=3.4, x=.16, y=.66, foco=(.5, .5, 1.0)),
    sil("Septimus Signus, un erudito", "septimus", "Septimus Signus", "Una cueva helada", dur=4.6, lado="izq", alto=880),
    mapa("skyrim.jpg", "Skyrim", [pt(SEPTIM, "Puesto de Septimus", "inicio", "septimus"), pt(ALFTAND, "Blackreach", "paso", "blackreach")],
         "vive en una cueva helada", ("los Pergaminos Antiguos#2", .6), ["una cueva helada", "en Blackreach"], "De Septimus a Blackreach",
         ventana=True, ancho=1000, x=.70, y=.45),
    pant("torre_mzark", "el oculario de la Torre de Mzark", ("una ranura para un léxico", .6), zoom=(1.0, 1.12)),
    mg(_cad("El oculario de Mzark", [("Léxico", "En la ranura"), ("Botones", "Las lentes se alinean"), ("Pergamino", "A tus manos")]),
       "Pulsas los botones", ("tumbar a Alduin", -.3), ["Pulsas los botones", "las lentes se alinean", "el pergamino baja"], "mzark", y=.36),
    rel("El de la misión de Dragonrend", "pergamino_dragon", "Pergamino Antiguo (Dragón)", "Dragonrend", dur=4.0, x=.76, y=.52, tam=520),
    mis("un esqueleto, Drokt", "Diario de Drokt", "Murió sin enfocarla", dur=4.0, y=.72),

    # ---------------- 8 · no creían en nada
    aviso("En el ocho", 8, "No creían en nada"),
    mg(T.balanza("La fe de los dwemer", ("Razón y lógica", None), [("Fe · Daedra · dioses", None)], remate=("AGNÓSTICOS", 2)),
       "la cultura dwemer era agnóstica", ("la razón y la lógica", .8), ["agnóstica", "prefería la razón", "Despreciaban a los daedra"],
       "razon fe", y=.46),
    mis("Era un problema de ingeniería", "Para un dwemer", "Un dios = ingeniería", dur=3.6, y=.30),
    ficha("un cuento dwemer tiene este chiste", "Cuentos antiguos de los dwemer", "«…un dios imaginario, y *encima muerto*»", "Elder Scrolls Online",
          dur=6.0),
    ficha("Marobar Sul", "Marobar Sul", "Seudónimo · *poco fiable*", "Autor de los cuentos", dur=4.4, rojo=True),
    mis("intenta fabricarse uno", "Siguiente paso", "Fabricar un dios", dur=3.4, y=.72),

    # ---------------- 7 · el Numidium
    aviso("En el siete", 7, "El dios de latón"),
    sil("El Numidium", "numidium", "Numidium", "El dios de latón", dur=5.0, lado="der", alto=920, encuadre=(0, .55)),
    mg(T.cronologia("El Numidium", [("1E 700", "Kagrenac lo construye", 0), ("2E 896", "Tiber Septim conquista", 1),
                                     ("3E 417", "La Distorsión del Oeste", 2), ("3E 427", "Akulakhan destruido", 3)]),
       "Más de tres mil años después", ("siete potencias activaron", -.3), ["Más de tres mil", "Un solo gólem", "Akulakhan", "Lo destruyes tú"],
       "crono numidium", y=.30),
    cam("Tiber Septim lo puso en marcha", "tiber", "Tiber Septim", dur=3.4, x=.16, y=.66),
    rel("con la Mantella como corazón", "mantella", "La Mantella", "El corazón del Numidium", dur=3.6, x=.78, y=.52, tam=440),
    mis("Un solo gólem", "Islas de Estivalia", "Un gólem, un continente", dur=3.6, y=.72),
    mg(T.soldados("Siete potencias, el mismo día", 7, remate=("EL TIEMPO SE ROMPE", 2), cols=7, ancho=900),
       "siete potencias activaron", ("la de Sentinel", .6), ["siete potencias", "el tiempo se rompió"], "siete potencias", y=.40),
    sil("Dagoth Ur construyó otro", "dagoth_ur", "Dagoth Ur", "Construyó el Akulakhan", dur=3.4, lado="izq", alto=860),
    rel("el Akulakhan", "akulakhan", "Akulakhan", "El segundo Numidium", dur=4.4, x=.76, y=.52, tam=460),
    mis("Imagina lo que no se dejaron", "Inventario dwemer", "Lo que no se dejaron", dur=4.0, y=.30),

    # ---------------- CAMPAÑA DE SUSCRIPCIÓN
    mg(T.rejilla("De cada cien que ven el canal", n=100, encendidas=11, remate=("SOLO 11 SUSCRITOS", 2)),
       "De cada cien que ven", ("están suscritos", 1.2), ["De cada cien", "solo once", "solo once"], "suscritos", y=.42),
    mg(T.contadores("Crónicas de Tamriel", [("Suscriptores hoy", 6480, None, 0), ("Meta", 10000, 1, 2)], remate=("Y NO DESAPARECEMOS", 3)),
       "Somos seis mil", ("no somos dwemer", .8), ["Somos seis mil", "Si te suscribes", "diez mil", "no desaparecemos"], "meta subs", y=.40),

    # ---------------- 6 · la caja (el Humano tras el Telón)
    aviso("Número seis. La caja", 6, "La caja que nadie debía abrir"),
    sil("Septimus Signus tiene en su cueva", "septimus", "Septimus Signus", "«El corazón de un dios»", dur=4.6, lado="der", alto=880),
    mg(_cad("La cerradura de la caja", [("Altmer", "sangre"), ("Bosmer", "sangre"), ("Dunmer", "sangre"), ("Orco", "sangre"), ("Falmer", "sangre")]),
       "sacar sangre de cinco elfos", ("Falta uno", .4), ["elfos: altmer", "bosmer", "dunmer", "orco", "orco y falmer|fin"], "sangre cinco", y=.36),
    mis("Falta uno", "Sangre que falta", "Dwemer · ni una gota", dur=4.4, y=.72),
    rel("Hay un libro: el Oghma Infinium", "oghma", "Oghma Infinium", "¿Es solo un libro?", dur=4.4, x=.76, y=.52, tam=480),
    sil("Hermaeus Mora lo levanta", "hermaeus", "Hermaeus Mora", "Daedra del conocimiento", dur=4.0, lado="izq", alto=820, encuadre=(0, .5)),
    mis("un montón de ceniza", "De Septimus queda", "Ceniza", dur=3.4, y=.30),
    mis("Lo has leído de una nota", "Crítica", "Leído de una nota", dur=2.6, y=.72),

    # ---------------- 5 · el corazón bajo la montaña
    aviso("Llegamos al cinco", 5, "El corazón bajo la montaña"),
    mapa("morrowind.jpg", "Morrowind", [pt(MONTANA, "Montaña Roja", "meta", "montana_roja")], "Bajo la Montaña Roja de Morrowind",
         ("no era de este mundo", .6), ["Montaña Roja"], "Vvardenfell · la Montaña Roja", ventana=True, ancho=900, x=.30, y=.45),
    rel("el corazón de Lorkhan", "corazon_lorkhan", "Corazón de Lorkhan", "Arrancado al dios que creó Nirn", dur=5.0, x=.76, y=.52, tam=520),
    mis("energía. La de un dios", "Lo que vio Kagrenac", "Energía de un dios", dur=3.4, y=.30),
    ficha("Metafísica divina", "Metafísica divina", "Crear un *dios nuevo* · inmortalidad", "Plan de Kagrenac", dur=5.0),
    cam("Para los chimer", "vivec", "Chimer", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.8)),
    ficha("está escrito en dwemeris", "Metafísica divina", "Escrito en *dwemeris* · sin traducción", "Nadie lo puede leer", dur=5.6, rojo=True),

    # ---------------- 4 · las herramientas
    aviso("En el cuatro", 4, "Tres herramientas"),
    rel("Sunder, un martillo", "sunder", "Sunder", "Saca una cantidad exacta de poder", dur=4.0, x=.22, y=.52, tam=460),
    rel("Keening, una hoja corta", "keening", "Keening", "Desuella y enfoca el poder", dur=3.6, x=.78, y=.52, tam=440),
    rel("Y Wraithguard, un guantelete", "wraithguard", "Wraithguard", "Sin él, las otras dos matan", dur=4.0, x=.22, y=.52, tam=440),
    mg(T.receta("El experimento de Kagrenac", [(P("sunder"), "Sunder"), (P("keening"), "Keening"), (P("wraithguard"), "Wraithguard")],
                (P("corazon_lorkhan"), "Corazón de Lorkhan"), "UN DIOS NUEVO"),
       "Kagrenac era famoso", ("Bthuand Mzahnch", -.1), ["Kagrenac era famoso", "meticuloso", "prudente"], "receta kagrenac", y=.38),
    ficha("El huevo del tiempo", "El huevo del tiempo", "Quita importancia *a los riesgos*", "Bthuand Mzahnch", dur=5.0, rojo=True),
    mis("los efectos secundarios", "Advertencia", "Efectos secundarios enormes", dur=3.6, y=.72),
    mis("Lo de siempre en cualquier empresa", "Acta de la reunión", "«No pasa nada»", dur=3.6, y=.30),

    # ---------------- CRÍTICA · «kyrim»
    mis("la última carta del día", "Correo del canal", "Crítica n.º 2", dur=2.6, y=.18),
    com("se nota que Kyrim", C_KYRIM, dur=7.0, x=.50, y=.40, tam=1000),
    mg(_cad("Juegos que jugamos", [("Kyrim", "Nunca"), ("Skyrim", "Con ese")]), "Kyrim no es lo nuestro", ("Pero gracias", -.2),
       ["Kyrim no es lo nuestro", "Lo nuestro es Skyrim"], "kyrim", y=.72),
    mis("serás el primero en enseñárnoslo", "Pendiente", "Que salga Kyrim", dur=3.4, y=.30),

    # ---------------- 3 · la batalla
    aviso("Número tres", 3, "Nadie se pone de acuerdo"),
    mg(T.cronologia("La batalla de la Montaña Roja", [("1E 668", "Una canción nórdica", 1), ("1E 700", "La fecha más citada", 0)]),
       "Primera era, setecientos", ("seiscientos sesenta y ocho", 1.0), ["Primera era", "seiscientos sesenta"], "fecha batalla", y=.30),
    aba([("nerevar", "Nerevar"), ("dumac", "Dumac")], "De un lado, Nerevar", ("su aliado", .6), ["Nerevar", "Dumac"], "nerevar dumac", x=.30, y=.62),
    mg(T.lecturas("Cuatro versiones de un mismo día", ["«Un golpe cruel, una traición amarga» · Dagoth Ur"],
                  [("Vivec", "Kagrenac usó las herramientas", 0), ("Vivec, otra vez", "Kagrenac ni estaba allí", 1),
                   ("El Templo", "Nerevar y Azura los destruyeron", 2), ("Los ashlanders", "El Tribunal envenenó a Nerevar", 3)]),
       "Versión de Vivec", ("una traición amarga", .8), ["Versión de Vivec", "ni siquiera estaba", "Versión del Templo", "los ashlanders"],
       "cuatro versiones", y=.30),
    cam("con ayuda de Azura", "azura", "Azura", dur=3.0, x=.84, y=.78, tam=260),
    cam("Y Dagoth Ur, en una carta", "dagoth_ur", "Dagoth Ur", dur=3.4, x=.16, y=.80, tam=260, foco=(.5, .25, 1.8)),
    mis("todas son verdad a la vez", "Teoría", "El tiempo se rompió", dur=4.0, y=.72),

    # ---------------- 2 · el último dwemer
    aviso("En el dos", 2, "El último de su raza"),
    mapa("morrowind.jpg", "Morrowind", [pt(MONTANA, "Montaña Roja", "inicio", "montana_roja"), pt(TELFYR, "Tel Fyr", "meta", "divayth")],
         "bajo la torre del mago Divayth Fyr", ("El último dwemer", 1.0), ["Divayth Fyr", "Yagrum Bagarn"], "Tel Fyr · Vvardenfell",
         ventana=True, ancho=900, x=.30, y=.45),
    sil("vive Yagrum Bagarn", "yagrum", "Yagrum Bagarn", "El último dwemer vivo conocido", dur=6.0, lado="der", alto=860, encuadre=(0, .5)),
    ficha("Hinchado por el corprus", "Corprus", "La enfermedad de *Dagoth Ur*", "Yagrum la pilló buscando respuestas", dur=5.0, rojo=True),
    mis("Porque no estaba", "Dónde estaba Yagrum", "En un reino exterior", dur=4.0, y=.30),
    ficha("Su teoría", "Teoría de Yagrum", "Vida eterna, con *consecuencias imprevistas*", "O la destrucción de su raza", dur=6.0),
    mapa("morrowind.jpg", "Morrowind", [pt(MONTANA, "Montaña Roja", "inicio"), pt(MOURNHOLD, "Bamz-Amschend · Mournhold", "meta", "bamz")],
         "En Bamz-Amschend, bajo Mournhold", ("al final de la batalla", .6), ["Bamz-Amschend", "montones de ceniza"], "La ceniza de Bamz-Amschend",
         ventana=True, ancho=900, x=.70, y=.45),
    mg(T.destello("Bamz-Amschend", 40, ("CENIZA", 2), cols=10, ancho=760), "hay montones de ceniza", ("Y recuerda la ceniza", -.1),
       ["hay montones", "se hubieran vuelto polvo", "polvo"], "destello ceniza", x=.25, y=.67),
    cam("la ceniza de Septimus", "septimus", "Septimus Signus", dur=4.0, x=.84, y=.66),

    # ---------------- 1 · Arniel
    aviso("Y llegamos al número uno", 1, "Skyrim te deja repetirlo"),
    sil("vive Arniel Gane", "arniel", "Arniel Gane", "Colegio de Hibernalia", dur=5.0, lado="izq", alto=880),
    mg(T.receta("El experimento de Arniel", [(P("convector"), "Gema de alma"), (P("keening"), "Keening")], (P("sombra_arniel"), "Arniel Gane"), "DESAPARECER"),
       "Con una gema de alma en lugar", ("La herramienta de Kagrenac", .8), ["Con una gema de alma", "Keening en lugar", "Sí. Keening"],
       "receta arniel", y=.36),
    aba([("engranaje", "Engranajes dwemer"), ("enthir", "Enthir"), ("convector", "Convector dwemer")], "Le llevas diez engranajes",
        ("se destruyen al usarlos", .6), ["diez engranajes", "Enthir te da", "convectores dwemer"], "pasos arniel", x=.70, y=.62),
    rel("recuperar Keening", "keening", "Keening", "Llegaba desde Morrowind", dur=3.8, x=.22, y=.52, tam=440),
    mg(T.destello("El experimento", 1, ("ARNIEL YA NO ESTÁ", 2), cols=1, ancho=700), "Una vez, nada",
       ("Solo queda Keening en el suelo", 1.2), ["Una vez, nada", "un destello", "Arniel ya no está"], "destello arniel", y=.42),
    ficha("el experimento funcionó", "Arniel Gane", "El experimento *funcionó*", "UESP", dur=4.6),
    mis("nadie nota que falta", "Colegio de Hibernalia", "Nadie lo echa de menos", dur=3.6, y=.72),
    sil("puedes invocar su sombra", "sombra_arniel", "Sombra de Arniel", "Invulnerable · te cura", dur=5.0, lado="der", alto=760, encuadre=(0, .5)),
    mg_en(T.contadores("Sombra de Arniel", [("Coste de magia", 0, None, None), ("Segundos", 60, None, None)], remate=("TE CURA", 0)),
          "No cuesta magia", 5.0, "sombra", x=.30, y=.34),
    mis("Se fueron a algún sitio", "La respuesta de Skyrim", "No murieron: se fueron", dur=4.6, y=.30),
    mis("La pena es que no habla", "Sombra de Arniel", "No habla", dur=3.4, y=.72),

    # ---------------- cierre
    mis("Esos son los veinte secretos", "Misión completada", "20 secretos de los dwemer", dur=6.0, y=.25),
    mg(T.lecturas("¿Qué les pasó?", ["Déjalo en los comentarios"], [("Borrados", "", 0), ("Dioses", "", 1), ("Con Arniel", "", 2)]),
       "¿Qué crees que les pasó?", ("Déjalo en los comentarios", 1.0), ["Borrados", "convertidos en dioses", "con Arniel"], "encuesta", y=.42),
    mis("los quince secretos del teaser", "En el canal", "15 secretos del teaser de Sentinel", dur=4.0, y=.72),
    mis("Suscríbete si aún no", "Crónicas de Tamriel", "Suscríbete", dur=6.0, y=.30),
]

# ---- SIETE VOCES + el Humano tras el Telón: placa de quién narra en cada presentación y en cada cambio de voz, abajo a la derecha;
# la papeleta de la votación en el cierre (cada voz marca su casilla cuando pide el voto)
VOCES = ["Johnny", "Edoardo", "Hope", "José", "Mario", "MariCarmen", "el Profeta"]
_LEMA = {"Johnny": "El veinte y el diecinueve", "Edoardo": "El dieciocho y el diecisiete", "Hope": "El doce, el once y el diez",
         "José": "El dieciséis y el quince", "Mario": "El catorce y el trece", "MariCarmen": "El nueve, el ocho y el siete",
         "el Profeta": "Del cinco al uno"}
_HUMANO = "el Humano tras el Telón"


def narra(en, nombre, dur=4.0, lema=None):
    n = VOCES.index(nombre) + 1 if nombre in VOCES else None
    return dict(tipo="mg", fn=T.narrador(nombre, lema or _LEMA.get(nombre, "Crítico n.º 1 · hoy narra el seis"), n, 7 if n else None),
                en=en, dur=dur, x=.80, y=.83, sale=.35, nombre="placa narra " + nombre, ver=1.2)


NARRA = [
    narra("Recuento de los comentarios", "Johnny"),
    narra("Edoardo. Me tocan", "Edoardo"), narra("José, para servirte", "José"), narra("Mario. Catorce y trece", "Mario"),
    narra("Hope. Doce, once", "Hope"), narra("MariCarmen. Nueve, ocho", "MariCarmen"), narra("Yo soy el Profeta", "el Profeta"),
    narra("Y el seis es mío", _HUMANO, dur=5.0), narra("Qué miedo. Empiezo yo", "Johnny"),
    narra("Gracias, Johnny. Ahora", "Edoardo"), narra("José. Número dieciséis", "José"), narra("Muy bonito, José", "Mario"),
    narra("Y aquí salgo yo", _HUMANO, dur=5.0), narra("Porque hace falta", _HUMANO),
    narra("Gracias, señor filtrador", "Hope"), narra("Y yo otros dos", "MariCarmen"), narra("MariCarmen, empiezo", "MariCarmen"),
    narra("Gracias, MariCarmen. Y ahora", _HUMANO, dur=5.0), narra("Lo has leído de una nota", "Johnny"),
    narra("Y tú tienes cuatro votos", "MariCarmen"), narra("Llegamos al cinco", "el Profeta"),
    mg(T.votacion("¿Qué voz se queda?", VOCES, "Un nombre en los comentarios"), "Y vota otra vez", ("Leído de una nota#2", 0.0),
       ["Leído de una nota#2", "Edoardo. Cero votos", "Hope. Con hache", "José. Sin voz", "Mario. Ya sé", "MariCarmen. La menos",
        "Yo no pido votos", "Un nombre, y listo"], "votación", y=.45),   # marcas en el orden de VOCES + remate
]
FX = FX + NARRA

# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número veinte", "Número dieciocho", "Número dieciséis", "Número catorce",
                                                                 "Número doce", "Número nueve", "Número tres")]
PISTAS += [dict(sfx="mision_iniciada", en=e, vol=.20) for e in ("En el diecinueve", "En el diecisiete", "En el quince", "En el trece",
                                                                "En el once", "En el diez", "En el ocho", "En el siete", "En el cuatro", "En el dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in ("Se entra por tres ruinas", "Juntas cuatro fragmentos", "Mzulft, al sur de Ventalia",
                                                                  "Alftand, al suroeste de Hibernalia")]
PISTAS += [dict(sfx="subir_nivel", en="Y llegamos al número uno", vol=.24), dict(sfx="subir_nivel", en="Veinte secretos", vol=.18),
           dict(sfx="mision_completada", en="Esos son los veinte secretos", vol=.22), dict(sfx="grito", en="viene un dragón", vol=.16)]


# ---- RELLENO DE HUECOS > 4 s (s3, 4-nov-2026; `_huecos.py`): cada tramo con la voz sin gráfico recibe pegatina, ficha o rótulo
FX += [
    ficha("No dejaron ni una tumba", "Dwemer", "Ni una tumba", dur=3.4, y=.62),
    mis("sigo siendo el único serio", "Edoardo", "0 votos · 100 % serio", dur=3.6, y=.30),
    mis("sin voz de locutor", "José", "Sin voz de locutor", dur=3.4, y=.30),
    mis("Prometo correr menos", "Mario", "Promete correr menos", dur=3.6, y=.30),
    mis("ya sabe dónde vivo", "MariCarmen", "Que nadie le robe un voto", dur=3.6, y=.30),
    mis("Así está escrito", "El Profeta", "Así está escrito", dur=3.4, y=.30),
    mis("os vais a enterar de cómo se hace", "El Humano tras el Telón", "Narra un secreto", dur=3.6, y=.30),
    mg_en(T.destello("Arniel Gane", 30, ("DESAPARECE", 2)), "quédate hasta el número uno", 4.6, "teaser numero uno", x=.5, y=.45),
    cam("ni los mejores magos de Tamriel", "arniel", "Arniel Gane", dur=4.0, x=.84, y=.66),
    ficha("Lo de enanos es el nombre que usa el Imperio", "Enanos", "Nombre *imperial*, no dwemer", "La fábula de los gigantes", dur=4.0),
    mis("con cariño, a sus amigos dwemer", "Para los gigantes", "Sus pequeños amigos", dur=3.4, y=.30),
    cam("es un mote de gigante", "gigante", "Gigante", dur=3.6, x=.84, y=.66),
    cam("la próxima vez que discutas con el yarl", "understone", "Understone Keep", dur=4.0, x=.16, y=.66),
    rel("Su gran obra es traducir", "piedra_calcelmo", "Piedra de Calcelmo", "Falmer y dwemer", dur=4.4, x=.24, y=.52, tam=440),
    ficha("si hizo falta el paso de generaciones", "Falmer", "¿Hongo o generaciones?", dur=3.6, y=.62),
    cam("Al final se rebelaron", "falmer", "Falmer", dur=3.4, x=.84, y=.66),
    mis("esa guerra acabó de golpe", "Guerra del Risco", "Fin repentino", dur=3.6, y=.30),
    aba([("falmer", "Falmer"), ("dumac", "Dwemer")], "Los falmer se prepararon para el golpe definitivo", ("para la última batalla", .5),
        ["Los falmer se prepararon", "Salieron a buscar"], "golpe definitivo", x=.30, y=.62),
    ficha("Imagina preparar durante décadas", "Venganza falmer", "Décadas de ensayo", dur=4.0, y=.62),
    cam("se quedaron con las ciudades", "blackreach", "Ciudades dwemer", dur=3.6, x=.84, y=.66),
    ficha("Pero con menos estilo", "Expedición de Sulla", "Desaparecidos sin estilo", dur=3.4, y=.62),
    mis("Y los que más corrige son los suyos", "Crítico n.º 1", "El Humano tras el Telón", dur=3.6, y=.30),
    ficha("Que si la música", "Correcciones", "Música · voz · ritmo", dur=3.6, y=.62),
    ficha("manipular el sonido para cambiar la realidad", "Arquitectura tonal", "Sonido que *cambia la realidad*", "UESP", dur=4.4),
    cam("amplificada con collares", "resonador", "Resonador", dur=3.0, x=.16, y=.66),
    cam("su aprendiz le robó la investigación", "katria", "Katria", dur=4.0, x=.16, y=.66),
    ficha("Y en el mapa aparece", "Oculario de Mzulft", "Un mapa de Skyrim", dur=3.4, y=.62),
    ficha("donde más lingotes dwemer puedes sacar", "Récord", "Lingotes dwemer", dur=3.4, y=.62),
    ficha("Por si te sobra la capacidad", "Capacidad de carga", "No te sobra", dur=3.6, y=.62),
    ficha("Gracias por escucharnos hasta el final", "Hope", "Escuchó hasta el final", dur=3.6, y=.62),
    rel("escondieron en Blackreach un modo", "pergamino_dragon", "Pergamino Antiguo", "Escondido en Blackreach", dur=4.4, x=.76, y=.52, tam=440),
    ficha("Mal día para leer las instrucciones", "Drokt", "Manual no incluido", dur=3.4, y=.62),
    ficha("un dios no era alguien a quien rezar", "Dwemer", "Un dios = un problema", dur=4.0, y=.62),
    ficha("Ojo: esos cuentos", "Aviso de UESP", "Ficción con seudónimo", dur=3.6, y=.62),
    cam("los escribió un autor", "libro_enanos3", "Marobar Sul", dur=3.6, x=.84, y=.66),
    mis("Porque un pueblo que no cree en los dioses", "Razón sobre fe", "Fabricarse un dios", dur=4.0, y=.30),
    rel("alimentado por un corazón muy especial", "corazon_lorkhan", "Corazón de Lorkhan", "El motor del Numidium", dur=4.4, x=.24, y=.52, tam=440),
    aba([("numidium", "Numidium"), ("keening", "Keening"), ("mantella", "Mantella")], "lo que deja olvidado en un cajón", ("conquistar el mundo", .5),
        ["lo que deja olvidado", "le basta a un emperador"], "cajon dwemer", x=.30, y=.62),
    rel("Para abrirla te manda a la Torre de Mzark", "torre_mzark", "Torre de Mzark", "Con su léxico", dur=4.4, x=.76, y=.52, tam=440),
    ficha("La caja se abre", "Caja de Septimus", "Abierta", dur=3.4, y=.62),
    mis("Con datos, con suspense", "El Humano tras el Telón", "Sin presumir", dur=3.4, y=.30),
    ficha("lo que todo dwemer quería", "Kagrenac", "La energía de un dios", dur=4.0, y=.62),
    mis("quizá hacer inmortales a los dwemer", "Plan de Kagrenac", "Dwemer inmortales", dur=3.6, y=.30),
    cam("aquello era una blasfemia", "nerevar", "Los chimer", dur=3.4, x=.16, y=.66),
    ficha("nadie lo puede leer", "Metafísica divina", "Ilegible", dur=3.4, y=.62),
    ficha("Hubo una reunión", "Acta de la reunión", "«No pasa nada»", dur=4.0, y=.62),
    ficha("el video de las cosas inútiles", "Crítica", "Desde las cosas inútiles", dur=3.4, y=.62),
    ficha("Si algún día sale Kyrim", "Kyrim", "Próximamente (nunca)", dur=3.6, y=.62),
    grande("La batalla de la Montaña Roja", "montana_roja", "Montaña Roja", dur=4.0, x=.25, tam=600),
    mg_en(T.destello("Montaña Roja", 40, ("EL TIEMPO SE ROMPE", 2)), "Hay una teoría para tantas versiones", 5.0, "tiempo roto", x=.5, y=.42),
    ficha("Lo pilló al volver a la Montaña Roja", "Yagrum", "Corprus en la Montaña Roja", dur=4.0, y=.62),
    cam("mi pueblo ya no estaba", "yagrum", "Yagrum Bagarn", dur=4.0, x=.84, y=.66),
    ficha("Aunque admite que también pudo destruirla", "Yagrum", "O destruirla entera", dur=4.0, y=.62),
    ficha("y lo que queda es lo mismo", "Ceniza", "Septimus = Bamz-Amschend", dur=3.6, y=.62),
    ficha("recrear el momento exacto", "Arniel Gane", "Recrear la desaparición", dur=4.0, y=.62),
    rel("Arniel golpea la gema con la daga", "keening", "Keening", "Tres golpes", dur=4.0, x=.76, y=.52, tam=440),
    cam("invocado del juego que te cura", "sombra_arniel", "Sombra de Arniel", dur=3.6, x=.16, y=.66),
    mis("los dwemer no murieron en una explosión", "La respuesta de Skyrim", "Se fueron a algún sitio", dur=5.0, y=.30),
    ficha("Ahora te toca a ti", "Tu teoría", "En los comentarios", dur=3.6, y=.62),
]

PISTAS += [dict(sfx="grito", en="Fuerza Implacable", vol=.30), dict(sfx="grito", en="Escupe vapor", vol=.18)]

# ---- AJUSTES de `_desencimar.py` (s3, 4-nov-2026): 0 encimados según `_bordes.py` (índices de FX sin ajustar)
import json as _json  # noqa: E402

_AJ = os.path.join(_AQUI, "_ajustes.json")
if os.path.exists(_AJ) and not os.environ.get("FAB_SIN_AJUSTES"):
    for _k, _v in sorted(_json.load(open(_AJ, encoding="utf-8")).items(), key=lambda kv: -int(kv[0])):
        _d = FX[int(_k)]
        if _v.get("quitar"):
            FX.pop(int(_k))
            continue
        if "retraso" in _v:
            _e = _d["en"]
            _d["en"] = (_e[0], _e[1] + _v["retraso"]) if isinstance(_e, tuple) else (_e, _v["retraso"])
        if "dur" in _v:
            _d["dur"] = _v["dur"]
