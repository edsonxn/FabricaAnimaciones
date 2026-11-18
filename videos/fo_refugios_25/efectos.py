# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 25 refugios más malvados y raros de Fallout» (SECUENCIA YT, Radio Yermo, 2.º video, 17-nov-2026).
REGLA DE ORO (tes_secretos_40) con la receta de Tamriel: kit Pip-Boy `nucleo/mg_fo.py`, pegatinas `pv()` con el rotador + estilos
de peg_estilos (tema "fo"), presentaciones (muro, versus, podio) y MAPAS REALES del Pip-Boy de CADA juego (mapas/<juego>.png,
refugios ubicados en mapas/_coords.json por el agente de mapas, comprobados en previews/_coords_check_<juego>.jpg).
Recreaciones de Flow (lo que no tiene imagen ni video) en pantallas/ como pant(): llevan su rótulo «RECREACIÓN».
Pegatinas: pegatinas/_lista.md (identidad revisada; NO usar r77_puerta: palabrota). Hilo Braun: 88 → 75 → 112.
    python fab.py fo_refugios_25 fx --seco      FAB_FX_FINAL=1 python fab.py fo_refugios_25 fx hoja
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
C = {j: {k: tuple(v["xy"]) for k, v in d.items()} for j, d in json.load(open(os.path.join(_MAP, "_coords.json"), encoding="utf-8")).items()}


def P(slug):
    return os.path.join(_PEG, slug + ".png")


# ---------------------------------------------------------------- helpers (de fo_nunca_f4)
def pv(en, slug, titulo, dur=4.0, x=.18, y=.60, tam=380, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6, xs=(.14, .32, .50, .68, .86)):
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro([(P(s), n) for s, n in fotos], tema=TEMA_PEG, destaca=destaca, titulo=titulo), de, a, marcas, "muro")


def versus(a_, b_, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.versus((P(a_[0]), a_[1]), (P(b_[0]), b_[1]), tema=TEMA_PEG, titulo=titulo), de, a, marcas, "versus")


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(en, slug, titulo, lineas, sello=None, dur=5.0, x=.74, y=.50):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, (sello, 0) if sello else None, tema=TEMA_PEG), en=en, dur=dur, x=x,
                y=y, sale=.35, nombre="legajo " + slug, ver=1.2, **({"marcas": [(en, 1.6)]} if sello else {}))


def mg(fn, de, a, marcas, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def pu(en, n, titulo, sub, y=.26):
    return mg_en(F.puesto(n, titulo, sub, total=25, cab="LOS 25 PEORES REFUGIOS"), en, 3.8, f"puesto {n}", y=y)


def fi(en, nombre, filas, texto=None, cab=None, dur=4.6, x=_FX, y=_FY):
    return mg_en(F.ficha(nombre, filas, texto, cab), en, dur, "ficha " + nombre, x=x, y=y)


def ob(en, texto, sub=None, hecho=False, dur=3.6, x=.30, y=.20, marca=1.4):
    fn = F.objetivo(texto, sub, hecho=hecho)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG objetivo " + texto, ver=1.0,
                **({"marcas": [(en, marca)]} if hecho else {}))


def av(en, texto, sub=None, icono=None, dur=3.2, x=.30, y=.13):
    return mg_en(F.aviso(texto, sub, icono=icono), en, dur, "aviso " + texto, x=x, y=y)


def cont(en, valor, unidad, titulo, desde=0, dur=3.4, x=.76, y=.30):
    return mg_en(F.contador(valor, unidad, titulo, desde=desde), en, dur, "contador " + titulo, x=x, y=y)


def term(en, lineas, dur=5.0, y=.78, titulo="ROBCO INDUSTRIES (TM) TERMLINK"):
    return mg_en(F.terminal(lineas, titulo=titulo), en, dur, "terminal " + lineas[0][:20], y=y)


def _recorta(puntos, lado):
    xs, ys = [p[0] for p in puntos], [p[1] for p in puntos]
    L = max(lado, max(xs) - min(xs) + .14, max(ys) - min(ys) + .14)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    x0, y0 = min(max(0.0, cx - L / 2), 1 - L), min(max(0.0, cy - L / 2), 1 - L)
    nue = [((p[0] - x0) / L, (p[1] - y0) / L) + tuple(p[2:]) for p in puntos]
    return (x0, y0, x0 + L, y0 + L), nue


def mapa(juego, titulo, puntos, de, a, marcas, sub, x=.70, y=.45, lado=.34, ancho=860, **kw):
    """Mapa REAL del Pip-Boy del juego en ventana, con el refugio marcado (y su foto)."""
    import mg_mapa as MP
    rec, puntos = _recorta(puntos, lado)
    fn = MP.mapa(_recorte_disco(juego, rec), puntos, TEMA_MAPA, titulo=titulo, sub=sub, recorte=None, modo="ventana",
                 ancho=ancho, **kw)
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)


def _recorte_disco(juego, rec):
    """El recorte del Pip-Boy guardado en disco (≤ 1600 px): sin esto cada mapa carga el mapa entero (hasta 4096 px) y la hoja
    y el render se quedan sin RAM (18-nov-2026)."""
    from PIL import Image
    d = os.path.join(_MAP, "_cache"); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"{juego}_{'_'.join(f'{v:.4f}' for v in rec)}.png")
    if not os.path.exists(f):
        im = Image.open(os.path.join(_MAP, juego + ".png")).convert("RGB")
        W, H = im.size
        im = im.crop((int(rec[0] * W), int(rec[1] * H), int(rec[2] * W), int(rec[3] * H)))
        im.thumbnail((1600, 1600)); im.save(f)
    return f


def pt(juego, slug, nombre, tipo="meta", foto=None):
    x, y = C[juego][slug]
    return (x, y, nombre, tipo) + ((P(foto),) if foto else ())


def ref(juego, slug, nombre, foto, en, hasta, sub, **kw):
    """Mapa de UN refugio: entra con su nombre y se va al terminar la frase `hasta`."""
    return mapa(juego, titulo=sub, puntos=[pt(juego, slug, nombre, "poder", foto)], de=en, a=(hasta + "|fin", .3), marcas=[en],
                sub=nombre, entrada="foco", **kw)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_AQUI, "pantallas", slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


FX = [
    # ================= GANCHO: un elemento por frase
    mg(F.radio(["Radio Yermo"], 0, "Transmitiendo desde debajo de la tierra"), "Buenos días, Yermo",
       ("desde debajo de la tierra|fin", .2), [], "radio saludo", y=.46),
    rel("Vault-Tec vendió los refugios", "gen_logo", "Vault-Tec", "La salvación de América", dur=4.6, x=.74, y=.50, tam=480),
    cont("Ciento veintidós refugios", 122, "refugios", "PARA 400 MILLONES", dur=4.0, x=.26, y=.30),
    pv("Eran laboratorios", "gen_vaultboy", "Vault Boy", dur=3.6, x=.80, y=.60, tam=360),
    term("Hoy, los veinticinco refugios", ["> CARGAR EXPEDIENTES", "Los 25 refugios más *MALVADOS*", "y más *RAROS* de Fallout"], dur=5.2),
    pv("Un refugio con una puerta que no cierra", "r12_necropolis", "Refugio 12", dur=2.8, x=.18, y=.60, tam=340),
    pv("veinte hombres, diez mujeres y una pantera", "r43_vineta", "Refugio 43", dur=3.0, x=.50, y=.60, tam=340),
    pv("había que elegir a quién matar", "r11_cartel1", "Refugio 11", dur=3.0, x=.82, y=.60, tam=340),
    cam("Y un hombre que diseñó", "r112_braun", "¿Quién es?", dur=4.6, x=.80, y=.62, tam=320),
    av("Ponte el mono", "Ponte el mono", "Baja el volumen del Pip-Boy", dur=3.2, y=.80),

    # ================= 25 · REFUGIOS 55 Y 56
    pu("Número veinticinco", 25, "Refugios 55 y 56", "El aburrimiento como arma"),
    leg("Estos dos no salen en ningún juego", "gen_logo", "Experimentos 55 / 56", ["Fuera de los juegos", "Lista de los creadores"],
        "ARCHIVO", dur=5.4),
    pant("r55_pared", "En el cincuenta y cinco", ("mirando la pared|fin", .6), zoom=(1.0, 1.12)),
    pant("r56_comico", "En el cincuenta y seis", ("para siempre|fin", .4), zoom=(1.04, 1.14)),
    versus(("r55_holocinta", "55 · Sin cintas"), ("r55_holocinta", "56 · Un cómico malo"), "predijeron que el cincuenta y seis",
           ("por toda la eternidad|fin", .3), ["iba a caer primero"], titulo="¿Cuál cae primero?"),
    pant("r56_comico_b", "Por eso, en esta emisora", ("por su propia seguridad|fin", .3)),

    # ================= 24 · REFUGIO 21
    pu("Número veinticuatro", 24, "Refugio 21", "Todo se decide apostando"),
    mapa("mojave", "El Strip de New Vegas", [pt("mojave", "strip_puerta_norte", "Strip · Refugio 21", "poder", "r21_exterior")],
         "Está en pleno Strip", ("abiertamente como un hotel|fin", .3), ["Está en pleno Strip"], "Refugio 21", entrada="foco"),
    pv("perfectamente simétrico", "r21_atrio", "El atrio", dur=4.0, x=.18, y=.60, tam=380),
    ob("Y lo increíble es que funcionó", "El experimento funcionó", hecho=True, dur=3.6),
    pv("Hasta que llegó Mister House", "r21_house_pantalla", "Mister House", dur=4.4, x=.80, y=.58, tam=400),
    cont("una partida de blackjack", 1, "mano", "LA ÚLTIMA APUESTA", dur=3.6, x=.26),
    pv("House se quedó el refugio", "r21_tienda", "Lo que quedó", dur=3.6, x=.80, y=.60, tam=360),
    pv("con Sarah Weintraub", "r21_sarah", "Sarah Weintraub", dur=3.6, x=.18, y=.60, tam=360),
    cam("un tal Doc Mitchell", "r21_doc_mitchell", "Doc Mitchell", dur=4.8, x=.80, y=.60, tam=330),

    # ================= 23 · REFUGIO 118
    pu("Número veintitrés", 23, "Refugio 118", "El club de los cerebros ricos"),
    mapa("la_isla", "La Isla · Far Harbor", [pt("la_isla", "refugio118", "Refugio 118", "poder", "r118_entrada")],
         "En La Isla de Far Harbor", ("un apartheid de lujo|fin", .3), ["En La Isla de Far Harbor"], "Refugio 118", entrada="foco"),
    fi("diez ultrarricos servidos por robots", "Plan del Refugio 118", [("Grupo A", "10 ultrarricos"), ("Grupo B", "300 trabajadores")],
       "Los ricos *juzgan*. Los robots *ejecutan*", "VAULT-TEC", dur=7.0),
    cam("Ezra Parker", "r118_ezra", "Ezra Parker", dur=3.4, x=.80, y=.62),
    pant("r118_islenos", "no dejaron entrar a los isleños", ("golpeando la puerta|fin", .5), zoom=(1.0, 1.12)),
    pv("metieron sus cerebros en robocerebros", "r118_robocerebro", "Robocerebro", dur=4.0, x=.80, y=.60, tam=380),
    pv("con su playa artificial", "r118_playa", "La playa artificial", dur=3.6, x=.18, y=.60, tam=360),
    term("Su diario termina así", ["DIARIO DEL SUPERVISOR", "Me he convertido en el", "*sujeto de prueba*."], dur=6.0),
    pv("a resolver un asesinato", "r118_maxwell", "Maxwell", dur=3.6, x=.18, y=.60, tam=360),

    # ================= 22 · REFUGIO 43
    pu("Número veintidós", 22, "Refugio 43", "Veinte hombres, diez mujeres y una pantera"),
    pv("Este sale en un cómic oficial", "r43_vineta", "El cómic oficial", dur=4.4, x=.80, y=.58, tam=420),
    pant("r43_pantera", "Y una pantera viva", ("a ver qué pasa|fin", .5), zoom=(1.0, 1.14)),
    fi("No hay registros", "Refugio 43", [("Hombres", "20"), ("Mujeres", "10"), ("Panteras", "1")], "Desenlace: *desconocido*",
       "INVENTARIO", dur=5.6),
    pant("r43_pantera_b", "Lo único seguro es que alguien", ("el único que nunca pasó hambre fue el gato|fin", .3)),

    # ================= 21 · REFUGIO 88
    pu("Número veintiuno", 21, "Refugio 88", "El científico malvado eres tú"),
    mapa("commonwealth", "Canteras de Quincy", [pt("commonwealth", "refugio88", "Refugio 88", "poder", "r88_puerta")],
         "bajo las canteras de Quincy", ("seguridad y el reactor|fin", .3), ["bajo las canteras de Quincy"], "Refugio 88",
         entrada="foco"),
    pv("Valery Barstow", "r88_barstow", "Valery Barstow", dur=4.4, x=.80, y=.58, tam=400),
    cam("un tal Stanislaus Braun", "r112_braun", "Stanislaus Braun", dur=4.0, x=.20, y=.62),
    av("Recuerda ese nombre", "Nombre registrado", "S. Braun", dur=3.0, y=.84),
    pv("Una bicicleta que genera electricidad", "r88_powercycle", "Power Cycle 1000", dur=4.0, x=.80, y=.60, tam=380),
    cont("un cinco por ciento", 5, "% diario", "PROBABILIDAD DE MORIR", dur=3.6, x=.26),
] + filav("Una fuente de refrescos", [("r88_foropter", "Forópter", "un aparato de la vista"),
                                       ("r88_tragaperras", "Tragaperras", "tragaperras programadas")], xs=(.30, .70), dur=4.2) + [
    pv("El conejillo de indias se llama Clem", "r88_clem", "Clem", dur=4.4, x=.80, y=.60, tam=380),
    ob("Si eliges las opciones crueles", "Experimento cruel elegido", "Barstow te aprueba", hecho=True, dur=4.4),

    # ================= 20 · REFUGIO 101
    pu("Número veinte", 20, "Refugio 101", "Nadie entra, nadie sale"),
    ref("yermo_capital", "refugio101", "Refugio 101", "r101_exterior", "Tu casa en Fallout tres", "al sur de Megatón",
        "Yermo Capital"),
    fi("no abrir nunca, jamás", "Refugio 101", [("Piezas de repuesto", "De sobra"), ("G.E.C.K.", "Ninguno")],
       "La puerta *no se abre*", "EXPERIMENTO", dur=6.0),
    mg_en(F.radio(["Radio del supervisor"], 0, "Transmisiones falsas grabadas antes de la guerra"), "emitía transmisiones de radio falsas",
          5.0, "radio falsa", y=.46),
    pv("con el supervisor Almodóvar", "r101_almodovar", "Almodóvar", dur=4.0, x=.80, y=.60, tam=380),
    pv("matan a golpes a Jonas", "r101_jonas", "Jonas", dur=3.8, x=.18, y=.60, tam=360),
    pv("el robot médico, Andy", "r101_andy", "Andy", dur=4.4, x=.80, y=.60, tam=380),
    pv("Amata te destierra", "r101_amata", "Amata", dur=4.0, x=.18, y=.60, tam=360),
    av("Salvas el refugio", "Has sido desterrado", "Refugio 101", dur=3.6, y=.84),

    # ================= 19 · REFUGIO 22
    pu("Número diecinueve", 19, "Refugio 22", "El refugio verde"),
    ref("mojave", "refugio22", "Refugio 22", "r22_exterior", "En el Mojave, al este de Jacobstown", "las plantas matan", "El Mojave"),
    pv("solo científicos agrícolas", "r22_atrio", "El refugio verde", dur=4.0, x=.18, y=.60, tam=380),
    fi("Un contratista les regaló un hongo", "Hongo de Big MT", [("Plagas", "Muertas"), ("Cadáveres", "Esparcen esporas")],
       "También infecta a *humanos*", "INVESTIGACIÓN", dur=6.0),
    pv("portadores de esporas", "r22_portador", "Portador de esporas", dur=4.4, x=.80, y=.58, tam=400),
    cont("Ciento dieciocho supervivientes", 118, "supervivientes", "HACIA EL CAÑÓN ZION", dur=4.0, x=.26),
    pv("Randall Clark", "r22_randall", "Randall Clark", dur=4.4, x=.80, y=.60, tam=380),

    # ================= 18 · REFUGIO 106
    pu("Número dieciocho", 18, "Refugio 106", "Drogas por la ventilación"),
    ref("yermo_capital", "refugio106", "Refugio 106", "r106_exterior", "En una caverna al sureste de Arefu", "doce investigadores",
        "Yermo Capital"),
    term("Diez días después del sellado", ["SECUENCIA DE CONTROL 46-2A", "15:30 · LIBERAR AGENTE", "16:00 · FIN"], dur=7.0),
    term("El supervisor le dio una instrucción", ["A SEGURIDAD:", "Si notan un olor raro,", "*pequeña irregularidad* del filtrado."],
         dur=6.0),
    pv("una mini nuke", "r106_mininuke", "Mini nuke", dur=3.6, x=.80, y=.60, tam=340),
    pv("la pantalla se tiñe de azul", "r106_alucinacion", "Alucinación", dur=4.4, x=.80, y=.58, tam=400),
    pv("a Amata y al supervisor", "r106_amata", "Amata (alucinación)", dur=3.6, x=.18, y=.60, tam=360),
    av("convencidos de que son los moradores", "Estado: drogado", "Refugio 106", dur=3.6, y=.84),

    # ================= 17 · REFUGIO 63
    pu("Número diecisiete", 17, "Refugio 63", "El búnker de un ejecutivo"),
    ref("apalaches", "refugio63", "Refugio 63", "r63_puerta", "En los Apalaches, bajo la mansión", "después del apocalipsis",
        "Apalaches · Shenandoah"),
    cam("Lo construyó Hugo Stolz", "r63_hugo", "Hugo Stolz", dur=4.0, x=.20, y=.62),
    pv("control del clima", "r63_clima", "Máquina del clima", dur=4.0, x=.80, y=.60, tam=380),
    av("El día de la guerra, no los dejó entrar", "Acceso denegado", "Dark Hollow Falls", dur=3.4, y=.84),
    cam("su esposa, Cassidy", "r63_cassidy", "Cassidy Stolz", dur=3.6, x=.80, y=.62),
    pv("los Perdidos", "r63_lost", "Los Perdidos", dur=4.4, x=.18, y=.58, tam=400),
    cont("una tercera vez", 3, "activación", "PRÓXIMA", dur=3.4, x=.76),

    # ================= 16 · REFUGIO 81
    pu("Número dieciséis", 16, "Refugio 81", "Se salvó por una traición"),
    ref("commonwealth", "refugio81", "Refugio 81", "r81_puerta", "En la Commonwealth. Uno de los pocos", "moradores originales",
        "Commonwealth"),
    fi("una cura universal", "Plan del Refugio 81", [("Enfermedades", "Por boquillas"), ("Evacuación", "Incinerar a todos")],
       "Cobayas: *los residentes*", "VAULT-TEC", dur=8.0),
    term("La supervisora, la doctora Olivette", ["SUPERVISORA OLIVETTE:", "Lista de llamadas", "*SABOTEADA*"], dur=5.0),
    pv("selló la sección secreta", "r81_secreto", "La sección secreta", dur=4.4, x=.80, y=.58, tam=400),
    pv("las ratas topo de laboratorio", "r81_rata_topo", "Rata topo", dur=3.4, x=.18, y=.60, tam=340),
    pv("Curie, que siguió sola", "r81_curie", "Curie", dur=4.4, x=.80, y=.60, tam=380),
    versus(("r81_austin", "Austin"), ("gen_mono", "Tú"), "la última dosis es para él", ("o para ti|fin", 1.4), ["o para ti"],
           titulo="Una sola cura"),

    # ================= 15 · REFUGIO 108
    pu("Número quince", 15, "Refugio 108", "Gary"),
    ref("yermo_capital", "refugio108", "Refugio 108", "r108_entrada", "Al sur de Canterbury Commons", "setenta y cinco residentes",
        "Yermo Capital"),
    fi("El experimento oficial ya era malo", "Refugio 108", [("Generador", "Falla a los 20 años"), ("Armas", "×3"),
                                                              ("Entretenimiento", "0")], None, "EXPERIMENTO", dur=7.0),
    leg("Y al supervisor, Brody Jones", "gen_mono", "Brody Jones", ["Cáncer: 3 años", "«Un catalizador adecuado»"], "ELEGIDO",
        dur=6.0),
    pv("clonaba en serie a un hombre llamado Gary", "r108_gary", "Gary", dur=4.4, x=.80, y=.58, tam=400),
    cont("Después del clon cincuenta y tres", 54, "", "CLON N.º", desde=1, dur=3.8, x=.26),
    pv("solo quedan Garys", "r108_lab", "Laboratorio de clonación", dur=3.6, x=.18, y=.60, tam=360),
    rel("Gary no se olvida", "r108_gary_ficha", "Gary", "Clon n.º 54", dur=4.0),

    # ================= 14 · REFUGIO 0
    pu("Número catorce", 14, "Refugio 0", "Cerebros en frascos"),
    pv("Bajo la montaña Cheyenne", "r0_entrada", "Refugio 0", dur=4.0, x=.80, y=.58, tam=380),
    av("Fallout Tactics", "Fallout Tactics", "Canon dudoso", dur=3.4, y=.84),
    pv("les sacaron el cerebro", "r0_calculadora_juego", "Cerebros en tanques", dur=4.4, x=.18, y=.58, tam=400),
    rel("la Calculadora", "r0_calculadora", "La Calculadora", "Supercomputadora", dur=4.4),
    cont("murió el sesenta y tres por ciento", 63, "%", "MUERTOS AL DESPERTAR", dur=4.0, x=.26),
    term("La Calculadora, corrompida", ["PROTOCOLO DE PACIFICACIÓN", "OBJETIVO: *TODA LA VIDA*", "ESTADO: ACTIVO"], dur=5.4),
    cont("el ochenta y cinco por ciento", 85, "%", "PROGRAMACIÓN CORRUPTA", dur=3.6, x=.76),

    # ================= 13 · REFUGIO 77
    pu("Número trece", 13, "Refugio 77", "Un hombre y una caja de marionetas"),
    pv("Otro cómic oficial de Bethesda", "r77_vaultboy", "El cómic oficial", dur=4.4, x=.80, y=.58, tam=420),
    av("el refugio se selló con una sola persona", "Moradores: 1", "Refugio 77", dur=3.6, y=.84),
    pant("r77_caja", "Solo tenía una caja", ("que le hablaba|fin", .4), zoom=(1.0, 1.14)),
    pv("Le arrancó la cabeza al rey", "r77_caja", "La caja", dur=3.8, x=.80, y=.58, tam=380),
    pant("r77_hormiga", "Afuera montó una hormiga gigante", ("ya había matado antes|fin", .4), zoom=(1.0, 1.12)),
    pv("Última viñeta", "r77_sale", "Última viñeta", dur=4.0, x=.80, y=.58, tam=400),
    pv("todavía está su mono del setenta y siete", "r77_mono", "Mono del Refugio 77", dur=4.4, x=.18, y=.58, tam=380),

    # ================= 12 · REFUGIO 94
    pu("Número doce", 12, "Refugio 94", "Los pacifistas"),
    ref("apalaches", "refugio94", "Refugio 94", "r94_exterior", "En los Apalaches, entre La División Salvaje", "pacifista y religiosa",
        "Apalaches"),
    fi("Vault-Tec les dio muchos recursos", "Refugio 94", [("G.E.C.K.", "1"), ("Semillas", "Banco completo"), ("Armas", "0")],
       None, "SUMINISTROS", dur=5.6),
    pv("un GECK y un banco de semillas", "r94_semillas", "Banco de semillas", dur=3.6, x=.18, y=.60, tam=360),
    term("El día de la guerra, la puerta se cerró sola", ["01:30 · PUERTA SELLADA", "03:00 · LLEGA EL 2.º AUTOBÚS",
                                                          "*ACCESO DENEGADO*"], dur=6.0),
    pv("le dispararon al GECK", "r94_geck", "El G.E.C.K.", dur=4.0, x=.80, y=.58, tam=380),
    mg_en(F.rads(7800, 1.0, .9, titulo="Refugio 94 · por segundo"), "Siete mil ochocientos rads", 4.4, "rads 94", y=.80),
    pv("toda La Ciénaga", "r94_atrio", "El atrio, hoy", dur=3.6, x=.18, y=.60, tam=360),

    # ================= 11 · REFUGIOS 68 Y 69
    pu("Número once", 11, "Refugios 68 y 69", "Los números son a propósito"),
    pant("r69_hombre", "En el sesenta y nueve entraron mil personas", ("cuando se cierra la puerta|fin", .4), zoom=(1.0, 1.12)),
    pv("Y el cómic oficial de Bethesda", "r69_vineta", "El cómic oficial", dur=4.4, x=.80, y=.58, tam=400),
    cont("Mil una personas", 1001, "personas", "SEGÚN EL CÓMIC", desde=1000, dur=3.4, x=.26),
    pant("r68_puerta", "Luego está el sesenta y ocho", ("ni Vault-Tec se atrevió a apuntar|fin", .3), zoom=(1.0, 1.16)),

    # ================= 10 · REFUGIO 95
    pu("Número diez", 10, "Refugio 95", "La recaída programada"),
    ref("commonwealth", "refugio95", "Refugio 95", "r95_exterior", "Al borde noreste del Mar Resplandeciente", "láseres trampa",
        "Commonwealth"),
    pv("una sala de desintoxicación", "r95_detox", "Desintoxicación", dur=3.8, x=.18, y=.60, tam=360),
    cont("Durante cinco años", 5, "años", "LIMPIOS", dur=3.6, x=.76),
    pant("r95_alijo", "un agente infiltrado de Vault-Tec", ("un alijo secreto de drogas|fin", .4), zoom=(1.0, 1.14)),
    av("Recayeron todos", "Adicción contraída", "Todos los residentes", dur=3.6, y=.84),
    pv("El alijo sigue ahí", "r95_alijo", "El alijo", dur=4.0, x=.80, y=.58, tam=380),
    pv("Cait, tu compañera", "r95_cait", "Cait", dur=4.4, x=.18, y=.58, tam=380),

    # ================= 9 · REFUGIO 111
    pu("Número nueve", 9, "Refugio 111", "El congelador"),
    ref("commonwealth", "refugio111", "Refugio 111", "r111_preguerra", "En la colina sobre Sanctuary Hills", "empieza Fallout cuatro",
        "Commonwealth"),
    pv("las cápsulas eran de descontaminación", "r111_capsulas", "Cápsulas criogénicas", dur=4.4, x=.80, y=.58, tam=400),
    cont("aguantar ciento ochenta días", 180, "días", "SELLADO MÍNIMO", dur=3.8, x=.26),
    cam("Kellogg, del Instituto", "r111_kellogg", "Kellogg", dur=3.6, x=.80, y=.62),
    pv("llega a por tu hijo, Shaun", "r111_secuestro", "El secuestro", dur=4.0, x=.18, y=.60, tam=380),
    term("Y los demás no murieron por el frío", ["ESTADO DEL OCUPANTE:", "*FALLECIDO*", "Asfixia: fallo del soporte vital"],
         dur=6.0),
    rel("Te prometieron un refugio para toda la vida", "r111_mono", "Mono del 111", "Para toda la vida", dur=4.8),

    # ================= 8 · REFUGIO 12
    pu("Número ocho", 8, "Refugio 12", "La puerta que no cierra"),
    cont("quince mil galones", 15000, "galones/día", "PURIFICADORA", dur=4.0, x=.76),
    ob("Por eso la puerta se diseñó para no cerrar", "Puerta del refugio: no cierra", "Diseño de Vault-Tec", dur=4.0),
    pant("r12_puerta", "la gente de Bakersfield entró a la fuerza", ("Es decir: no funcionó|fin", .5), zoom=(1.0, 1.14)),
    pv("fundaron una ciudad de muertos vivientes", "r12_necropolis", "Necrópolis", dur=4.4, x=.80, y=.58, tam=400),
    pv("Un necrófago llamado Set", "r12_set", "Set", dur=4.0, x=.18, y=.60, tam=380),
    rel("a robarle el chip de agua", "r12_chip_intro", "Chip de agua", "Refugio 12", dur=4.4),
    pant("r12_puerta_b", "Les vendieron una puerta", ("era decorativa|fin", .4)),

    # ================= 7 · REFUGIO 92
    pu("Número siete", 7, "Refugio 92", "La orquesta asesina"),
    ref("yermo_capital", "refugio92", "Refugio 92", "r92_exterior", "Al noroeste de Old Olney", "el talento musical de América",
        "Yermo Capital"),
    term("El plan secreto", ["PROYECTO W.N.M.S.C.E.", "Ruido blanco + música", "= *órdenes de combate*"], dur=6.0),
    pv("llevó el ruido blanco hasta los dormitorios", "r92_estudio", "Los estudios", dur=4.0, x=.80, y=.58, tam=380),
    av("Así sonaba", "Ruido blanco", "Dormitorios · 03:00", dur=3.6, y=.84),
    cont("casi veintitrés disparos", 23, "disparos", "PARA TUMBARLO", dur=3.6, x=.26),
    cont("treinta y cinco muertos", 35, "muertos", "BALANCE DE MALLEUS", dur=3.8, x=.76),
    cam("el profesor Malleus", "r92_malleus", "Profesor Malleus", dur=3.6, x=.20, y=.62, foco=(.5, .3, 1.3)),
    pv("la descarga de ruido mata al instante", "r92_pruebas", "Sala de pruebas", dur=4.0, x=.80, y=.58, tam=380),
    rel("Eso sí es preservar el talento", "r92_violin", "Violín Stradivarius", "Refugio 92", dur=4.4),

    # ================= 6 · REFUGIO 87
    pu("Número seis", 6, "Refugio 87", "La fábrica de supermutantes"),
    ref("yermo_capital", "refugio87", "Refugio 87", "r87_entrada", "Al noroeste de Little Lamplight", "impacto nuclear directo",
        "Yermo Capital"),
    mg_en(F.rads(4000, 1.0, 1.0, titulo="Entrada del Refugio 87 · por segundo"), "casi cuatro mil rads", 5.0, "rads 87", y=.80),
    pv("laboratorio del virus de evolución forzada", "r87_fev", "Virus de evolución forzada", dur=4.4, x=.80, y=.58, tam=400),
    cont("Ochenta y siete muertes sin definir", 87, "muertes", "CAUSA DESCONOCIDA", dur=4.0, x=.26),
    pv("entre restos de experimentos y centauros", "r87_centauro", "Centauro", dur=3.6, x=.18, y=.60, tam=360),
    pv("encuentras a Fawkes", "r87_fawkes", "Fawkes", dur=4.8, x=.80, y=.58, tam=420),

    # ================= SUSCRIPCIÓN (antes del top 5)
    mg(F.radio(["Radio Yermo"], 0, "Aviso de la emisora"), "Antes del top cinco", ("lo menos cruel que vas a hacer hoy|fin", .3),
       [], "radio aviso", y=.40),
    mg_en(F.objetivo("Suscríbete a Radio Yermo", "Que tu refugio sí abra la puerta"), "Este canal acaba de nacer", 7.0,
          "objetivo suscripción", x=.30, y=.80),

    # ================= 5 · REFUGIO 96
    pu("Número cinco", 5, "Refugio 96", "El arca con fecha de exterminio"),
    ref("apalaches", "refugio96", "Refugio 96", "r96_exterior", "En La División Salvaje, en los Apalaches", "diez mil animales",
        "Apalaches"),
    cont("Solo había cinco humanos", 5, "humanos", "RESIDENTES", dur=3.6, x=.26),
    pv("Ganaban créditos mutando criaturas", "r96_camara", "Cámara de pruebas", dur=4.4, x=.80, y=.58, tam=400),
    cont("doscientas cincuenta semanas", 250, "semanas", "LUEGO, EXTERMINIO", dur=4.0, x=.76),
    term("En la semana ciento cuarenta y ocho", ["CUOTA SEMANAL: 568 CRÉDITOS", "NINA VALAYA: *NO CUMPLE*", "ACCIÓN: ELIMINAR"], dur=6.0),
    av("activó el protocolo Omega", "Protocolo Omega", "Refugio resellado", dur=3.6, y=.84),
    pv("Hoy está cubierto de hielo", "r96_crio", "Refugio 96, hoy", dur=4.0, x=.18, y=.58, tam=380),
    cam("un científico de West-Tek", "r96_blackburn", "Edgar Blackburn", dur=3.6, x=.80, y=.62),

    # ================= 4 · REFUGIO 51
    pu("Número cuatro", 4, "Refugio 51", "El reality show de la IA"),
    ref("apalaches", "refugio51", "Refugio 51", "r51_puerta", "En el Bosque, en los Apalaches", "una inteligencia artificial llamada ZAX",
        "Apalaches"),
    rel("ZAX", "r51_zax", "ZAX 1.3c", "Supervisor", dur=4.0, x=.76),
    pv("todos los candidatos se votaron a sí mismos", "r51_candidatos", "Los candidatos", dur=4.0, x=.18, y=.58, tam=380),
    pv("Montó un casino", "r51_apuestas", "El casino", dur=3.6, x=.80, y=.60, tam=360),
    term("ZAX lo registró", ["REGISTRO ZAX 1.3c:", "*INTENTO DE SELECCIÓN", "DE SUPERVISOR N.º 37*"], dur=6.0),
    cam("Quedó uno solo, Reuben Gill", "r51_reuben", "Reuben Gill", dur=4.0, x=.80, y=.62),
    av("supervisor de nadie", "Supervisor: Reuben Gill", "Residentes: 0", dur=3.4, y=.84),

    # ================= 3 · REFUGIO 11
    pu("Número tres", 3, "Refugio 11", "La democracia del sacrificio"),
    ref("mojave", "refugio11", "Refugio 11", "r11_exterior", "En el Mojave, al oeste de Boulder City", "o morirán todos", "El Mojave"),
    pv("Decidieron hacerlo con elecciones", "r11_interior", "Refugio 11", dur=3.6, x=.18, y=.60, tam=360),
    pv("campañas al revés", "r11_cartel1", "Propaganda electoral", dur=4.6, x=.80, y=.58, tam=420),
    pv("Katherine Stone", "r11_cartel_kate", "«I hate Kate»", dur=4.6, x=.18, y=.58, tam=380),
    cont("la guerra civil dejó solo cinco vivos", 5, "vivos", "QUEDAN", desde=60, dur=3.6, x=.76),
    pant("r11_cinco", "Los cinco entraron juntos a la cámara", ("La puerta se abrió|fin", .5), zoom=(1.0, 1.12)),
    term("Nunca había hecho falta", ["RESULTADO DEL EXPERIMENTO:", "Negarse = *la puerta se abre*", "Desde el año 1"], dur=5.0),
    pv("En la entrada dejaron una grabación", "r11_ordenador", "La grabación", dur=4.0, x=.80, y=.58, tam=380),
    av("se oyen cuatro disparos", "Grabación de la entrada", "Voces 1 a 5", dur=8.0, y=.84),
    cont("En la entrada hay cuatro esqueletos", 4, "esqueletos", "EN LA ENTRADA", dur=3.4, x=.26),
    pv("te espera la silla", "r11_camara", "La cámara del sacrificio", dur=4.4, x=.80, y=.58, tam=400),
    cont("dieciséis esqueletos", 16, "esqueletos", "EN LA CÁMARA", dur=3.6, x=.26),

    # ================= 2 · REFUGIO 75
    pu("Número dos", 2, "Refugio 75", "La escuela"),
    ref("commonwealth", "refugio75", "Refugio 75", "r75_entrada", "Bajo la escuela de Malden", "subsidiadas para sus familias",
        "Commonwealth"),
    av("a los adultos los llevaron a una supuesta orientación", "Orientación de padres", "Atrio · 23-oct-2077", dur=4.0, y=.84),
    pv("A los niños les enseñaron a temer", "r75_atrio", "El atrio", dur=4.0, x=.18, y=.60, tam=380),
    pv("en el laboratorio de genómica", "r75_lab", "Laboratorio de genómica", dur=4.4, x=.80, y=.58, tam=400),
    term("Hay un informe que celebra", ["INFORME: PROMOCIÓN ELIMINADA", "Solo el *74 %*", "Gasto de eliminación: MUY BAJO"], dur=7.0),
    leg("entre las firmas del documento", "r112_braun", "DIRECTIVA PRINCIPAL", ["Refinamiento genético", "Firmas: V. Schlett, I. Lambe,",
                                                                                "*S. Braun*"], "SECRETO", dur=6.0),
    pv("una sala de simulación de combate", "r75_simulacion", "Simulación de combate", dur=4.0, x=.80, y=.58, tam=380),
    pv("Nunca dijo de quién", "r75_esqueleto", "Refugio 75", dur=3.6, x=.18, y=.60, tam=340),

    # ================= 1 · REFUGIO 112
    pu("Número uno. Refugio ciento doce", 1, "Refugio 112", "Tranquility Lane"),
    ref("yermo_capital", "refugio112", "Refugio 112", "r112_puerta", "Bajo el garaje de Smith Casey", "el doctor Stanislaus Braun",
        "Yermo Capital"),
    muro([("r75_lab", "75 · La escuela"), ("r88_barstow", "88 · La supervisora"), ("r112_braun", "112 · Braun"),
          ("gen_geck", "El G.E.C.K.")], "Sí, ese Braun", ("el creador del GECK|fin", .4),
         ["firmaba los experimentos", "supervisora del ochenta y ocho", "Uno de los hombres que diseñaron", "el creador del GECK"],
         destaca=2, titulo="Stanislaus Braun"),
    pv("Los ocupantes entraron en unas tumbonas", "r112_tumbonas", "Las tumbonas", dur=4.4, x=.80, y=.58, tam=400),
    pv("un barrio feliz de los años cincuenta", "r112_barrio", "Tranquility Lane", dur=4.0, x=.18, y=.58, tam=400),
    cam("disfrazado de Betty", "r112_betty", "Betty", dur=4.4, x=.80, y=.62, tam=330),
    pant("r112_laguna", "Antes de este barrio hubo otros dos mundos", ("una laguna tropical|fin", .6), zoom=(1.0, 1.12)),
    pant("r112_chalet", "y un chalet de esquí", ("el que más ha durado|fin", .3), zoom=(1.0, 1.12)),
    pv("Tu padre está ahí, convertido en perro", "r112_james", "Tu padre, en su tumbona", dur=3.6, x=.18, y=.60, tam=360),
    pv("matar a una anciana con su propio robot", "r112_mabel", "Mabel Henderson", dur=3.6, x=.80, y=.60, tam=360),
    av("Si intentas atacar a Betty", "Betty es invulnerable", "Simulación reiniciada", dur=4.0, y=.84),
    cont("doscientos dos coma tres años", 202.3, "años", "LLEGAS TARDE", dur=4.0, x=.26),
    pv("una invasión china que borra el barrio", "r112_invasion", "La invasión china", dur=4.8, x=.80, y=.58, tam=420),
    rel("Y ese es el peor refugio de Fallout", "r112_braun_conectado", "Stanislaus Braun", "Refugio 112", dur=6.0, x=.74, y=.52),

    # ================= CIERRE
    mg_en(F.objetivo("¿Cuál es el peor para ti?", "112 · 75 · 11"), "Esos son los veinticinco", 6.0, "objetivo comentario", y=.20),
    rel("el canal hermano es Crónicas", "tamriel_canal", "Crónicas de Tamriel", "El canal hermano", dur=7.0, x=.74, y=.50, tam=520),
    mg(F.radio(["Radio Yermo"], 0, "Fin de la transmisión"), "Esto fue Radio Yermo", ("qué número tiene tu refugio|fin", 1.5), [],
       "radio despedida", y=.46),
]

# ---- SFX del JUEGO (banco fallout4 → sfx/*.mp3) + los sonidos que la voz nombra (regla 31-oct: se oyen con la voz callada)
_NUM = ["veinticinco", "veinticuatro", "veintitrés", "veintidós", "veintiuno", "veinte", "diecinueve", "dieciocho", "diecisiete",
        "dieciséis", "quince", "catorce", "trece", "doce", "once", "diez", "nueve", "ocho", "siete", "seis", "cinco", "cuatro",
        "tres", "dos"]
PISTAS = [dict(sfx="pipboy", en="Número " + n + ".", vol=.30) for n in _NUM]
PISTAS += [dict(sfx="subir_nivel", en="Número uno. Refugio ciento doce", vol=.26),
           dict(sfx="mision_completada", en="Esos son los veinticinco", vol=.24),
           dict(sfx="terminal", en="Hoy, los veinticinco refugios", vol=.30),
           dict(sfx="geiger", en="casi cuatro mil rads", vol=.34), dict(sfx="geiger", en="Siete mil ochocientos rads", vol=.32),
           dict(sfx="logro", en="Y lo increíble es que funcionó", vol=.26),
           dict(sfx="ruido_blanco", en="Así sonaba.|fin", vol=.55),
           dict(sfx="r11_grabacion", en="se oyen cuatro disparos.|fin", vol=.95)]

# ---- EXTRA (chequeo 18-nov: pegatinas 2,4/min < 3,1 de la regla de oro): todo lo que la voz nombra con imagen disponible
EXTRA = [
    pv("baja el volumen del Pip-Boy", "gen_pipboy", "Pip-Boy", dur=3.0, x=.80, y=.60, tam=320),
    pv("se llevó la tecnología", "r21_house_estasis", "Mister House", dur=3.4, x=.18, y=.60, tam=340),
    pv("Ellos van a vivir para siempre", "r118_atrio", "Refugio 118", dur=3.6, x=.80, y=.60, tam=340),
    pv("El lema: nacemos en el refugio", "r101_atrio", "Refugio 101", dur=3.4, x=.18, y=.60, tam=340),
    pv("llegó el culto a su persona", "r101_cartel", "Culto al supervisor", dur=3.6, x=.80, y=.60, tam=340),
    cam("Cuando tu padre huye, Almodóvar", "r101_almodovar", "Almodóvar", dur=3.0, x=.20, y=.62),
    pv("y ningún GECK", "gen_geck", "G.E.C.K.", dur=3.2, x=.18, y=.60, tam=320),
    pv("todavía se lee la advertencia", "r22_cartel", "«Las plantas matan»", dur=3.6, x=.80, y=.60, tam=340),
    pv("Ciento siete habitantes", "r106_atrio", "Refugio 106", dur=3.4, x=.18, y=.60, tam=340),
    cam("ves a tu padre", "r112_james", "Tu padre", dur=2.8, x=.50, y=.62),
    pv("La radiación convirtió a los de dentro", "r63_atrio", "Refugio 63", dur=3.6, x=.80, y=.60, tam=340),
    pv("hasta el día en que murieron", "r81_tumbas", "Las tumbas", dur=3.4, x=.18, y=.60, tam=340),
    pv("Refugio ciento ocho: Gary.", "r108_puerta", "Refugio 108", dur=3.2, x=.82, y=.62, tam=300),
    pv("una marioneta de Vault Boy", "gen_vaultboy", "Vault Boy", dur=3.2, x=.18, y=.60, tam=320),
    pv("huyó del refugio por miedo", "r77_apartamento", "Refugio 77", dur=3.4, x=.80, y=.60, tam=340),
    mg_en(F.radio(["Radio Yermo"], 0, "Para que nadie esté solo"), "Por eso existe la radio", 4.0, "radio 77", y=.46),
    pv("un GECK y un banco de semillas", "gen_geck", "G.E.C.K.", dur=3.2, x=.80, y=.60, tam=320),
    pv("la puerta se cerró sola", "r94_puerta", "Refugio 94", dur=3.4, x=.18, y=.60, tam=340),
    pv("fortaleza de los Artilleros", "r95_puerta", "Refugio 95", dur=3.4, x=.18, y=.60, tam=340),
    pv("A las familias de Sanctuary", "r111_preguerra", "Sanctuary Hills, 2077", dur=3.6, x=.80, y=.60, tam=340),
    cam("llega a por tu hijo, Shaun", "r111_shaun", "Shaun", dur=3.0, x=.80, y=.62),
    pv("La radiación más alta de toda la saga", "r87_radiacion", "Entrada irradiada", dur=3.4, x=.18, y=.60, tam=340),
    pv("el profesor Malleus contó", "r92_holocinta", "Holocintas de Malleus", dur=3.4, x=.80, y=.60, tam=320),
    pv("unos diez mil animales", "r96_atrio", "Refugio 96", dur=3.4, x=.18, y=.60, tam=340),
    pv("Cincuenta y dos residentes", "r51_atrio", "Refugio 51", dur=3.4, x=.18, y=.60, tam=340),
    cam("ZAX lo fue dejando fuera", "r51_zax", "ZAX", dur=3.0, x=.80, y=.62),
    pv("la puerta se bloqueó", "r11_puerta", "Refugio 11", dur=3.4, x=.18, y=.60, tam=340),
    cam("Braun controla la simulación", "r112_braun_conectado", "Braun", dur=3.4, x=.80, y=.62),
    cam("Y Braun se queda solo", "r112_braun", "Stanislaus Braun", dur=3.6, x=.20, y=.62),
    pv("Doscientos años sin perder una apuesta", "r21_atrio", "Refugio 21", dur=3.4, x=.18, y=.60, tam=320),
    pv("Siguen ahí, con su playa", "r118_robocerebro", "Robocerebros", dur=3.0, x=.50, y=.62, tam=300),
    # mapas con ruta (lo que cuenta la voz recorre el mapa)
    mapa("apalaches", "Apalaches", [pt("apalaches", "refugio51", "Refugio 51", "inicio", "r51_reuben"),
                                    pt("apalaches", "refugio76", "Refugio 76", "meta", "gen_puerta")],
         "Huyó en una caja de envío", ("murió en una cabaña|fin", .4), ["Huyó en una caja de envío"], "La huida de Reuben"),

    mapa("yermo_capital", "Yermo Capital", [pt("yermo_capital", "refugio101", "Refugio 101", "inicio", "r101_almodovar"),
                                            pt("yermo_capital", "refugio106", "Refugio 106", "meta", "r106_alucinacion")],
         "al supervisor del ciento uno", ("multiplicados|fin", .4), ["al supervisor del ciento uno"], "Del 101 al 106"),
]
FX = FX + EXTRA
