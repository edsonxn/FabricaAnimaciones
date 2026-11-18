# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 15 cosas que NUNCA debes hacer en Fallout 4» (SECUENCIA YT, Radio Yermo, 1.er video, 17-nov-2026).
REGLA DE ORO (tes_secretos_40) con la receta de Tamriel: kit Pip-Boy `nucleo/mg_fo.py` (puesto, ficha, objetivo, special, terminal,
vats, enemigo, rads, radio, botin, aviso, rejilla, contador), pegatinas `pv()` con el rotador + estilos de peg_estilos (tema "fo"),
presentaciones (muro del cierre) y mapas REALES del Pip-Boy con ruta (lugares ubicados en `mapas/_coords.json` con `_ubicar3.py`,
comprobados ícono por ícono en `previews/_coords_check.jpg`). Plan: `_plan_efectos.md`. Datos: `_investigacion_A.md` / `_B.md`.
    python fab.py fo_nunca_f4 fx --seco      FAB_FX_FINAL=1 python fab.py fo_nunca_f4 fx hoja
"""
import json
import os

import mg_fo as F
import peg_estilos as PE

CAMARA = {}
FUNDIDO = {}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_PEG = "fo"
TEMA_MAPA = "fo"
_FX, _FY = .76, .30
C = {k: tuple(v["xy"]) for k, v in json.load(open(os.path.join(_MAP, "_coords.json"), encoding="utf-8")).items()}


def P(slug):
    return os.path.join(_PEG, slug + ".png")


# ---------------------------------------------------------------- helpers (de tes_builds_rotas)
def pv(en, slug, titulo, dur=4.0, x=.18, y=.60, tam=380, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6, xs=(.14, .32, .50, .68, .86)):
    """Fila de pegatinas; items = [(slug, titulo, ancla o None = la misma)]."""
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro([(P(s), n) for s, n in fotos], tema=TEMA_PEG, destaca=destaca, titulo=titulo), de, a, marcas, "muro")


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def mg(fn, de, a, marcas, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def pu(en, n, titulo, sub, y=.26):
    """Entrada de cada puesto (DATOS > MISIONES del Pip-Boy)."""
    return mg_en(F.puesto(n, titulo, sub), en, 3.8, f"puesto {n}", y=y)


def fi(en, nombre, filas, texto=None, cab=None, dur=4.4, x=_FX, y=_FY):
    return mg_en(F.ficha(nombre, filas, texto, cab), en, dur, "ficha " + nombre, x=x, y=y)


def ob(en, texto, sub=None, hecho=False, dur=3.6, x=.30, y=.20, marca=1.4):
    fn = F.objetivo(texto, sub, hecho=hecho)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG objetivo " + texto, ver=1.0,
                **({"marcas": [(en, marca)]} if hecho else {}))


def av(en, texto, sub=None, icono=None, dur=3.2, x=.30, y=.13):
    return mg_en(F.aviso(texto, sub, icono=icono), en, dur, "aviso " + texto, x=x, y=y)


def cont(en, valor, unidad, titulo, desde=0, dur=3.4, x=.76, y=.30):
    return mg_en(F.contador(valor, unidad, titulo, desde=desde), en, dur, "contador " + titulo, x=x, y=y)


def _recorta(puntos, lado):
    """Recorte cuadrado (fracción del mapa) centrado en los puntos, de `lado` o más si no caben; puntos en coords del recorte.
    Sin esto cada mapa trabaja el Pip-Boy entero a 4200 px y la hoja/el render se quedan sin memoria (17-nov-2026)."""
    xs, ys = [p[0] for p in puntos], [p[1] for p in puntos]
    L = max(lado, max(xs) - min(xs) + .14, max(ys) - min(ys) + .14)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    x0, y0 = min(max(0.0, cx - L / 2), 1 - L), min(max(0.0, cy - L / 2), 1 - L)
    nue = [((p[0] - x0) / L, (p[1] - y0) / L) + tuple(p[2:]) for p in puntos]
    return (x0, y0, x0 + L, y0 + L), nue


def mapa(titulo, puntos, de, a, marcas, sub, ventana=False, x=.70, y=.44, lado=None, **kw):
    import mg_mapa as MP
    rec, puntos = _recorta(puntos, lado or (.34 if ventana else .46))
    fn = MP.mapa(os.path.join(_MAP, "commonwealth.png"), puntos, TEMA_MAPA, titulo=titulo, sub=sub, recorte=rec,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    e = .05 if kw.get("entrada") else .5
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=e, sale=e, nombre="mapa " + sub, ver=4.0)


def pt(slug, nombre, tipo="meta", foto=None):
    x, y = C[slug]
    return (x, y, nombre, tipo) + ((P(foto),) if foto else ())


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_AQUI, "pantallas", slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


FX = [
    # ================= GANCHO (0-42 s): un elemento nuevo cada 2-3 s
    mg(F.radio(["Radio Yermo"], 0, "Transmitiendo desde lo que queda de la Commonwealth"), "Buenos días, Yermo",
       ("de la Commonwealth|fin", .2), [], "radio saludo", y=.46),
    mg_en(F.terminal(["> CARGAR LISTA", "Las 15 cosas que *NUNCA* debes hacer", "Fallout 4"]), "Las quince cosas que nunca", 5.6,
          "terminal título", y=.80),
    pv("Un niño del Refugio", "austin", "Austin", dur=3.0, x=.18, y=.60, tam=360),
    cont("por diez puntos de vida", 10, "PS máx.", "LO QUE TE CURAS", dur=2.6, x=.78, y=.30),
    pv("Una servoarmadura que se queda", "servoarmadura", "Servoarmadura", dur=2.6, x=.80, y=.60, tam=360),
    pv("en el fondo de un pozo", "dunwich", "Dunwich Borers", dur=2.4, x=.20, y=.60, tam=340),
    cam("Un viejo con corona", "lorenzo", "Lorenzo Cabot", dur=3.2, x=.16, y=.64, tam=320),
    cont("encerrado desde", 1898, "", "ENCERRADO DESDE", desde=2287, dur=3.0, x=.76, y=.30),
    pv("un pueblo entero que desaparece", "far_harbor", "Far Harbor", dur=3.0, x=.80, y=.60, tam=360),
    ob("Todo comprobado en el juego", "Todo comprobado en el juego", hecho=True, dur=3.0),
    av("el número uno no tiene arreglo", "El n.º 1 no tiene arreglo", "Quédate hasta el final", dur=3.4, y=.80),

    # ================= 15 · LEGENDARIO A MEDIAS
    pu("Número quince", 15, "Dejar a un legendario a medias", "Guarda el golpe gordo"),
    mg(F.enemigo("Enemigo legendario", 1.0, .45), "Ves la estrella", ("piensas que ya casi está|fin", .2),
       ["le bajas más de la mitad"], "enemigo legendario", y=.22),
    mg(F.enemigo("Enemigo legendario", .45, 1.0), "muta. Recupera", ("se envuelve en un aura|fin", .3),
       ["Recupera toda la vida"], "enemigo muta", y=.22),
    fi("Si es una criatura", "Mutación legendaria", [("Criatura", "Daño ×2"), ("Humano / supermutante", "+50 % daño")],
       "Y puntería *perfecta*. Solo pasa *una vez*", "LEGENDARIO", dur=6.0),
    ob("Lo correcto es guardar", "Bájalo del 50 % y deja que mute", dur=3.4),
    ob("luego lo rematas", "Remátalo después de la mutación", hecho=True, dur=3.2, marca=.8),
    cont("gastar todas las balas", 0, "balas", "PRIMER ACTO", desde=120, dur=3.4),

    # ================= 14 · MAR RESPLANDECIENTE
    pu("Número catorce", 14, "Entrar al Mar Resplandeciente sin protección", "Traje, Rad-X y RadAway"),
    mapa("Mar Resplandeciente", [pt("crater_atomo", "Cráter del Átomo", "poder", "crater_atomo")], "El suroeste de la Commonwealth",
         ("casi constantes|fin", .4), ["El suroeste de la Commonwealth"], "suroeste", ventana=True, ancho=900, x=.70, y=.45,
         entrada="foco"),
    pv("con tormentas radiactivas", "tormenta_rad", "Tormenta radiactiva", dur=3.4, x=.18, y=.60, tam=360),
    fi("cada diez rads te quitan", "Radiación", [("10 rads", "−1 % PS máx."), ("1000 rads", "Muerte")],
       "La vida perdida *no vuelve sola*", "EST / ESTADO", dur=7.0),
    cont("dura menos de dos minutos", 2, "min", "SIN PROTECCIÓN, MENOS DE", dur=3.4),
    mg_en(F.rads(300, 1.0, .6, titulo="Cráter del Átomo · por segundo"), "trescientos rads por segundo", 4.0, "rads cráter", y=.80),
] + filav("Lleva un traje Hazmat", [("hazmat", "Traje Hazmat", None), ("servoarmadura", "Servoarmadura", "o servoarmadura"),
                                     ("radx", "Rad-X", "Rad-X antes de entrar"), ("radaway", "RadAway", "RadAway en el bolsillo")],
          dur=6.4, xs=(.14, .34, .66, .86)) + [

    # ================= 13 · SUPERMUTANTE SUICIDA
    pu("Número trece", 13, "Dejar que el suicida llegue hasta ti", "Dispárale al brazo"),
    mg_en(F.enemigo("Supermutante suicida", 1.0), "Es un supermutante que viene", 4.2, "enemigo suicida", y=.22),
    pv("con una minibomba encendida", "minibomba", "Minibomba", dur=3.6, x=.80, y=.60, tam=360),
    cont("son cuatrocientos cincuenta de daño", 450, "de daño", "MINIBOMBA", dur=4.0),
    mg_en(F.vats([(.50, .22, 38), (.64, .52, 95), (.37, .52, 61), (.50, .86, 72)], crit=.6, titulo="Supermutante suicida"),
          "dispararle al brazo de la bomba", 4.6, "vats brazo"),
    mg_en(F.botin("Supermutante suicida", ["Minibomba"]), "la minibomba es tuya", 3.4, "botín minibomba", x=.72, y=.50),
    mapa("Commonwealth", [pt("medford", "Hospital de Medford", "peligro", "medford")], "En el hospital de Medford",
         ("sentado en el vestíbulo|fin", .3), ["En el hospital de Medford"], "Medford", ventana=True, ancho=860, x=.70, y=.45),
    av("que se llama Touchdown", "¡Touchdown!", "Logro desbloqueado", icono="ok", dur=4.2),

    # ================= 12 · CAÍDA CON SERVOARMADURA
    pu("Número doce", 12, "Caer con servoarmadura junto a aliados", "Aterriza lejos de la gente"),
    fi("anula todo el daño por caída", "Servoarmadura", [("Daño por caída", "0")], "Aterrizas *como un héroe*", "INV / ARMADURA",
       dur=5.0),
    av("se vuelve hostil", "Toda su facción se ha vuelto hostil", dur=3.6),
    av("Ellos sí se rompen", "Piernas lisiadas", "Tu compañero", dur=3.2, y=.86),
    mapa("Commonwealth", [pt("diamond_city", "Diamond City", "meta")], "Bienvenido a Diamond City", ("Bienvenido a Diamond City|fin", 2.6),
         ["Bienvenido a Diamond City"], "Diamond City", ventana=True, ancho=820, x=.70, y=.45, entrada="foco"),

    # ================= 11 · BAÚL AJENO
    pu("Número once", 11, "Guardar tus cosas en un baúl ajeno", "Usa los de tus asentamientos"),
    pv("Encuentras una caja fuerte", "caja_fuerte", "Caja fuerte", dur=3.4, x=.18, y=.60, tam=360),
    mg(F.botin("Caja fuerte", ["Munición", "Armas", "Chatarra"]), "tu munición, tus armas", ("tu chatarra|fin", 1.0),
       ["tu munición", "tus armas", "tu chatarra"], "botín caja", x=.28, y=.50),
    cont("El juego reinicia esas cajas", 0, "objetos", "LA CAJA, DÍAS DESPUÉS", desde=347, dur=3.6),
    mapa("Commonwealth", [pt("sanctuary", "Sanctuary Hills", "meta", "sanctuary")], "como el taller de Sanctuary",
         ("hace limpieza|fin", .2), ["como el taller de Sanctuary"], "Sanctuary taller", ventana=True, ancho=860, x=.70, y=.45),

    # ================= 10 · CABEZÓN ANTES DE TIEMPO
    pu("Número diez", 10, "Recoger un cabezón antes de tiempo", "Primero sube el atributo a 10"),
    pv("Hay un cabezón por cada", "cabezones", "Cabezones de Vault-Tec", dur=3.6, x=.80, y=.60, tam=380),
    mg(F.special([5, 4, 3, 3, 4, 3, 3]), "S.P.E.C.I.A.L., fuerza", ("y el resto|fin", .5), [], "special lista", x=.30, y=.48),
    mg(F.special([10, 4, 3, 3, 4, 3, 3], foco="Fuerza", cambios=[("Fuerza", 11)], nota="Por encima del máximo"),
       "Si recoges el cabezón cuando", ("Por encima del máximo|fin", .4), [("sube a once", 0)], "special 11", x=.30, y=.48),
    mg(F.special([9, 4, 3, 3, 4, 3, 3], foco="Fuerza", cambios=[("Fuerza", 10)], nota="El 11 ya no llega"),
       "Pero si lo recoges antes", ("El once lo perdiste|fin", .4), [("cuenta como una subida normal", 0)], "special 10", x=.30, y=.48),
    mapa("Commonwealth", [pt("mass_fusion", "Edificio de Mass Fusion", "meta", "cabezon_fuerza")], "en el edificio de Mass Fusion",
         ("por encima del mostrador|fin", .2), ["en el edificio de Mass Fusion"], "Mass Fusion", ventana=True, ancho=860, x=.70, y=.45),
    rel("Un muñequito de plástico", "cabezon_fuerza", "Cabezón de Fuerza", "Castiga la impaciencia", dur=5.0, x=.76, y=.52, tam=500),

    # ================= 9 · MAMÁ MURPHY
    pu("Número nueve", 9, "Darle a Mamá Murphy su quinta dosis", "Convéncela con carisma"),
    mapa("Commonwealth", [pt("sanctuary", "Sanctuary Hills", "meta", "mama_murphy")], "Mamá Murphy vive en Sanctuary",
         ("visiones de tu futuro|fin", .2), ["Mamá Murphy vive en Sanctuary"], "Sanctuary Murphy", ventana=True, ancho=860, x=.70, y=.45,
         entrada="foco"),
    pv("en su sillón, y a cambio", "sillon_murphy", "El sillón de Mamá Murphy", dur=3.6, x=.18, y=.60, tam=360),
] + filav("la contraseña de la banda", [("skinny_malone", "Skinny Malone", None), ("kellogg", "Kellogg", "la llave de Kellogg")],
          dur=5.0, y=.62, xs=(.14, .32)) + [
    fi("porque en la pelea Kellogg", "Visión de Mamá Murphy", [("Daño de Kellogg", "−25 %")], "En la pelea *final*", "VENTAJA",
       dur=5.0),
    mg(F.rejilla("Visiones de Mamá Murphy", 5, 5, "La quinta es la última", cols=5), "Pero solo tiene cinco visiones",
       ("muere en su sillón|fin", .6), ["solo tiene cinco visiones"], "rejilla visiones", y=.30),
    ob("dos pruebas difíciles de carisma", "[Carisma] Convéncela de que lo deje", "Pierde la visión, pero vive", hecho=True,
       dur=5.0, marca=3.0),

    # ================= 8 · NÚCLEO PUESTO
    pu("Número ocho", 8, "Dejar la servoarmadura con el núcleo", "Retira el núcleo de fusión"),
    ob("Y la armadura no está", "Encuentra tu servoarmadura", dur=3.4),
    pv("que tenga un núcleo puesto", "nucleo_fusion", "Núcleo de fusión", dur=3.8, x=.80, y=.60, tam=360),
    mg_en(F.botin("Láser Gatling", ["Núcleo de fusión"]), "con láser Gatling", 4.0, "botín gatling", x=.72, y=.50),
    av("al bajarte, saca el núcleo", "Núcleo de fusión retirado", "Servoarmadura", icono="ok", dur=4.0),
    pv("Comunismo de asentamiento", "armazon", "Armazón de servoarmadura", dur=4.6, x=.20, y=.60, tam=380),

    # ================= 7 · SINJIN
    pu("Número siete", 7, "Matar a Sinjin de un disparo furtivo", "Intimídalo o usa V.A.T.S."),
    mapa("La Mortaja Plateada", [pt("goodneighbor", "Goodneighbor", "inicio", "kent"), pt("milton", "Hospital Milton General", "peligro", "sinjin")],
         "En la misión de la Mortaja", ("hospital Milton General|fin", .8), ["en Goodneighbor", "el hospital Milton"], "Sinjin",
         entrada="pliegue"),
    pv("si matas a Sinjin con", "sinjin", "Sinjin", dur=4.0, x=.20, y=.60, tam=360),
    pv("y matan a Kent", "kent", "Kent Connolly", dur=3.8, x=.80, y=.60, tam=380),
    ob("La salida segura es intimidarlo", "[Intimidar] Sinjin", "O entra en V.A.T.S.", hecho=True, dur=4.0, marca=1.2),
    pv("las tres mejoras del traje", "traje_mortaja", "Traje de Mortaja Plateada", dur=4.6, x=.20, y=.58, tam=400),

    # ================= 6 · INSTITUTO SIN EVACUAR
    pu("Número seis", 6, "Volar el Instituto sin evacuarlo", "Da la orden desde la terminal"),
    mapa("Commonwealth", [pt("instituto", "Ruinas del C.I.T. · el Instituto", "peligro")], "En la misión final",
         ("la terminal del director|fin", .2), ["En la misión final"], "Instituto", ventana=True, ancho=860, x=.70, y=.45),
    ob("dar la orden de evacuación", "Da la orden de evacuación", "Opcional · La opción nuclear", dur=5.2, y=.80),
    pv("la próxima vez que te vea el Ferrocarril", "desdemona", "Desdemona · el Ferrocarril", dur=3.8, x=.18, y=.60, tam=360),
    pv("Preston te reprocha", "preston", "Preston Garvey", dur=3.8, x=.80, y=.60, tam=360),
    ob("lee la lista de tareas", "(Opcional) Lee la lista de tareas", dur=4.0),

    # ================= 5 · LA CURA DEL REFUGIO 81
    pu("Número cinco", 5, "Quedarte la cura del Refugio 81", "Dásela a Austin"),
    mapa("Commonwealth", [pt("refugio81", "Refugio 81", "meta", "puerta_r81")], "En la sección secreta del Refugio",
         ("te contagias|fin", .2), ["En la sección secreta del Refugio"], "Refugio 81", ventana=True, ancho=860, x=.70, y=.45),
    pv("un niño, Austin", "austin", "Austin", dur=4.0, x=.80, y=.60, tam=380),
    pv("Curie solo puede hacer", "curie", "Curie", dur=3.4, x=.18, y=.60, tam=360),
    cont("una dosis de la cura", 1, "dosis", "LA CURA", dur=3.4),
    cont("Diez puntos de vida máxima", 10, "PS máx.", "¿Y QUÉ TE CURASTE?", dur=4.0),
    pv("Hay estimulantes que curan", "estimulante", "Estimulante", dur=3.6, x=.80, y=.60, tam=340),

    # ================= PAUSA · SUSCRIPCIÓN (sin cifra: canal recién encendido)
    mg(F.radio(["Radio Yermo"], 0, "Cada suscripción, un watt más de señal"), "Una pausa en la transmisión",
       ("un watt más de señal|fin", .3), [], "radio suscripción", y=.46),
    ob("suscríbete y activa la campana", "Suscríbete y activa la campana", "Radio Yermo", hecho=True, dur=5.0, marca=2.0),

    # ================= 4 · NUKA-WORLD
    pu("Número cuatro", 4, "Hacerte jefe de los saqueadores de Nuka-World", "Preston no lo perdona"),
    pv("ser el jefe de sus bandas", "jefes_banda", "Las bandas de Nuka-World", dur=4.2, x=.80, y=.58, tam=420),
    pv("Preston Garvey pasa a odiarte", "preston", "Preston Garvey", dur=3.6, x=.18, y=.60, tam=360),
    fi("aunque tengas su afinidad", "Preston Garvey", [("Afinidad", "Máx. → Odio")], "Deja de trabajar *contigo*", "COMPAÑERO",
       dur=5.4),
    ob("deja de pedírtelo", "Otro asentamiento necesita tu ayuda", "Ya nadie te lo pide", hecho=True, dur=4.4, marca=1.0),

    # ================= 3 · DUNWICH BORERS
    pu("Número tres", 3, "Bajar con servoarmadura al pozo de Dunwich", "Bájate de la armadura antes"),
    mapa("Commonwealth", [pt("dunwich", "Dunwich Borers", "poder", "dunwich")], "Al fondo de la cantera", ("en el noreste del mapa|fin", 2.4),
         ["en el noreste del mapa"], "Dunwich", entrada="foco"),
    rel("está el Diente de Kremvh", "kremvh", "Diente de Kremvh", "Arma única", dur=4.4, x=.76, y=.52, tam=480),
    pv("junto a dos minibombas", "minibomba", "Dos minibombas", dur=3.0, x=.20, y=.60, tam=320),
    pv("Con servoarmadura no puedes nadar", "servoarmadura", "No flota", dur=3.6, x=.80, y=.60, tam=360),
    pv("el armazón se queda ahí", "armazon", "Para siempre", dur=4.0, x=.20, y=.60, tam=380),

    # ================= 2 · LORENZO CABOT
    pu("Número dos", 2, "Liberar a Lorenzo Cabot", "Haz lo que pide Jack"),
    mapa("Commonwealth", [pt("manicomio", "Manicomio Estatal Parsons", "peligro", "manicomio")], "En el sótano del Manicomio",
         ("por su propio hijo|fin", .2), ["En el sótano del Manicomio"], "Parsons", ventana=True, ancho=860, x=.70, y=.45),
    cam("Lorenzo Cabot, con una corona", "lorenzo", "Lorenzo Cabot", dur=4.4, x=.18, y=.62, tam=340),
    pv("Jack Cabot te pide", "jack_cabot", "Jack Cabot", dur=4.0, x=.80, y=.60, tam=360),
    mapa("La huida de Lorenzo", [pt("manicomio", "Manicomio Estatal Parsons", "inicio"), pt("casa_cabot", "Casa Cabot", "peligro", "casa_cabot")],
         "Lorenzo va a la Casa Cabot", ("y a Emogene|fin", .4), ["Lorenzo va", "a la Casa Cabot"], "Casa Cabot", ventana=True, ancho=900,
         x=.66, y=.45, viajeros=[P("lorenzo")]),
] + filav("mata a Jack", [("jack_cabot", "Jack", None), ("wilhelmina", "Wilhelmina", "a Wilhelmina"), ("emogene", "Emogene", "y a Emogene")],
          dur=4.0, y=.70, tam=260, xs=(.12, .27, .42)) + [
    pv("A cambio te promete suero", "suero", "Suero misterioso", dur=3.6, x=.80, y=.62, tam=340),
    fi("más fuerza, más resistencia", "Suero misterioso", [("Fuerza", "+5"), ("Resist. al daño", "+50"), ("Radiación", "−10 rads/s")],
       "Durante *1 hora*. Y de *uno en uno*", "AYUDA", dur=7.0),
    rel("el Artefacto de Lorenzo", "artefacto_lorenzo", "Artefacto de Lorenzo", "Lo pierdes para siempre", dur=5.0, x=.76, y=.52, tam=500),

    # ================= 1 · FAR HARBOR
    pu("Número uno#2", 1, "Meter el código del parque eólico", "Far Harbor depende de él", y=.80),
    pv("En Far Harbor, el pueblo", "far_harbor", "Far Harbor", dur=3.4, x=.80, y=.60, tam=380),
    pv("los condensadores de niebla", "condensador", "Condensador de niebla", dur=3.8, x=.18, y=.60, tam=360),
] + filav("En los recuerdos de DiMA", [("dima", "DiMA", None), ("tektus", "Tektus", "y Tektus")], dur=5.4, y=.62, xs=(.14, .32)) + [
    pv("las turbinas del parque eólico", "parque_eolico", "Parque eólico", dur=3.6, x=.80, y=.58, tam=380),
    av("se corta la electricidad", "Condensadores de niebla sin energía", dur=4.0),
    pv("El Viejo Longfellow se vuelve", "longfellow", "El Viejo Longfellow", dur=4.0, x=.80, y=.60, tam=360),
    av("Fallan todas sus misiones", "Misiones de Far Harbor: fallidas", dur=3.8, y=.86),

    # ================= CIERRE
    muro([("austin", "Austin"), ("armazon", "El pozo"), ("lorenzo", "Lorenzo"), ("far_harbor", "Far Harbor"), ("mama_murphy", "Mamá Murphy")],
         "Esas son las quince", ("en el fondo de un pozo#2|fin", .6),
         ["Esas son las quince", "cuál de estas hiciste", "dejó morir a Austin", "buscando su servoarmadura", "en el fondo de un pozo#2"],
         titulo="¿Cuál hiciste tú?"),
    mg(F.radio(["Radio Yermo"], 0, "Todos los comentarios se leen"), "Todos los comentarios se leen", ("próxima transmisión|fin", .3),
       [], "radio comentarios", y=.46),
    mg(F.radio(["Radio Yermo"], 0, "Esto fue Radio Yermo. No salgas del refugio sin escucharnos."), "Esto fue Radio Yermo",
       ("la repite|fin", 1.0), [], "radio despedida", y=.40),
    ob("Suscríbete, no salgas", "Suscríbete a Radio Yermo", hecho=True, dur=4.0, x=.70, y=.88, marca=1.0),
]

# ---- EXTRA (huecos de > 4 s sin apoyo medidos con `fx --seco`, sesión 2): cada uno con lo que nombra la voz
EXTRA = [
    cont("por debajo del cincuenta por ciento", 50, "%", "VIDA DEL LEGENDARIO", desde=100, dur=4.0),
    zoom(("esa vez duele", -3.0), ("esa vez duele|fin", .4), 1.12),
    mg_en(F.rads(1000, 1.0, 1.0, titulo="Con mil rads"), "Con mil rads, mueres", 4.0, "rads mil", y=.80),
    zoom("De cerca, sin servoarmadura", ("casi imposible sobrevivir|fin", .2), 1.15),
    pv("hay un logro por dejar", "suicida", "Supermutante suicida", dur=4.2, x=.80, y=.60, tam=360),
    dict(tipo="temblor", en="El impacto daña mucho", amp=30),
    zoom("El problema es el aterrizaje", ("amigo o neutral|fin", .2), 1.12),
    cont("tres tenderos muertos", 3, "tenderos", "ATERRIZAJE HEROICO", dur=4.0),
    pv("Pues los objetos que dejas", "baul", "Contenedor ajeno", dur=4.2, x=.80, y=.60, tam=360),
    rel("Los colonos de Sanctuary se juntan", "mama_murphy", "Mamá Murphy", "Quinta dosis", dur=5.0, x=.76, y=.52, tam=480),
    cam("La única vidente del Yermo", "mama_murphy", "La vidente", dur=4.4, x=.16, y=.64, tam=300),
    pv("Aparcas tu armadura", "servoarmadura", "Tu servoarmadura", dur=4.4, x=.80, y=.60, tam=360),
    fi("La estación de servoarmadura solo", "Estación de servoarmadura", [("Colonos ociosos", "No la tocan")],
       "Los demás, *sí*", "TALLER", dur=5.0),
    cam("Si Sinjin te descubre", "sinjin", "Sinjin", dur=4.0, x=.16, y=.64, tam=300),
    av("con la radio apagada", "Sin señal", "La radio de la Mortaja Plateada", dur=4.4),
    dict(tipo="temblor", en="mueren con la explosión", amp=40),
    dict(tipo="destello", en="mueren con la explosión"),
    av("pierdes una facción entera", "El Ferrocarril se ha vuelto hostil", dur=4.0, y=.86),
    av("todo el refugio te culpa", "Todo el Refugio 81 te culpa", dur=3.6),
    fi("Pierdes el rifle de jeringas", "Lo que pierdes", [("Rifle de jeringas", "Perdido"), ("Habitación", "Perdida")],
       "Por *10 PS* máximos", "REFUGIO 81", dur=5.0),
    cont("todavía quedan cuatro puestos", 4, "puestos", "QUEDAN", dur=4.0),
    ob("y luego te pide conquistar", "Conquista asentamientos de la Commonwealth", "Nuka-World", dur=4.4),
    av("su confianza se pierde", "Su confianza se pierde para siempre", "Preston Garvey", dur=4.0, y=.86),
    ob("Y las paredes del pozo", "Sal del pozo", "Las paredes son verticales", dur=4.4),
    fi("Solo lo recuperas si", "Recuperar el armazón", [("Un compañero dentro", "+ viaje rápido"), ("O bien", "Cargar partida")],
       None, "SERVOARMADURA", dur=5.6),
    zoom("el casco te deja respirar", ("negocio redondo para el pozo|fin", .3), 1.14),
    ob("activar cuatro interruptores", "Activa los cuatro interruptores", "Celda de Lorenzo", dur=4.6),
    cont("Pero te da uno cada vez", 1, "suero", "CADA VEZ", dur=3.8, x=.30),
    pv("Una familia entera por un suero", "casa_cabot", "La Casa Cabot", dur=4.6, x=.80, y=.58, tam=380),
    dict(tipo="destello", en="la Niebla se traga Far Harbor"),
    zoom("El pueblo queda en ruinas", ("habitantes mueren|fin", .2), 1.12),
    pv("la recompensa de los Hijos", "tektus", "Tektus · Hijos del Átomo", dur=4.4, x=.80, y=.60, tam=360),
    cont("con una sola línea de código", 1, "línea de código", "PARA BORRAR UN PUEBLO", dur=4.6),
    rel("el canal hermano es Crónicas", "tamriel_canal", "Crónicas de Tamriel", "El canal hermano", dur=7.0, x=.74, y=.50, tam=520),
    av("Tienes que salirte de la armadura", "Sal de la servoarmadura", "Bajo el agua", dur=3.8),
    pv("Un pueblo entero, por un objeto", "far_harbor", "Far Harbor", dur=4.6, x=.20, y=.58, tam=380),
    av("Así se borra un pueblo", "Far Harbor", "Sin un solo disparo", dur=3.6, y=.86),
    # MEMORIAL de Austin (promesa visual): captura REAL del aula del Refugio 81 (QNtCXe2BwvU a los 57,6 s, 1080p), recorte del mueble
    # del fondo con el jarrón de flores y el osito; zoom lento hacia él.
    pant("memorial_austin", "Le ponen un pequeño memorial", ("y un osito|fin", 1.2), zoom=(1.0, 1.15), pan=(0, 0, 0, 0)),
    av("Le ponen un pequeño memorial", "El memorial de Austin", "Aula del Refugio 81", dur=4.0, y=.86),
]
FX = FX + EXTRA

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/fallout4/ → sfx/*.mp3), solo en momentos clave
_NUM = ["quince", "catorce", "trece", "doce", "once", "diez", "nueve", "ocho", "siete", "seis", "cinco", "cuatro", "tres", "dos"]
PISTAS = [dict(sfx="pipboy", en="Número " + n, vol=.30) for n in _NUM]
PISTAS += [dict(sfx="subir_nivel", en="Número uno#2", vol=.26), dict(sfx="mision_completada", en="Esas son las quince", vol=.24),
           dict(sfx="lugar_descubierto", en="Bienvenido a Diamond City", vol=.22),
           dict(sfx="lugar_descubierto", en="en el noreste del mapa", vol=.22),
           dict(sfx="geiger", en="cada diez rads te quitan", vol=.30), dict(sfx="geiger", en="trescientos rads por segundo", vol=.34),
           dict(sfx="vats", en="dispararle al brazo de la bomba", vol=.40), dict(sfx="vats", en="Lo lógico es esconderte", vol=.40),
           dict(sfx="logro", en="que se llama Touchdown", vol=.30), dict(sfx="terminal", en="Las quince cosas que nunca", vol=.30)]
