# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Rykard QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 22-nov-2026).
Molde: videos/er_godfrey_atrocidades/efectos.py (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS · MOTION GRAPHICS
NUEVOS · MAPAS) con el kit de Elden Ring (nucleo/mg_er.py) y los estilos de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS reales (bajar_pegatinas.py; hoja previews/pegatinas_hoja.jpg). `rykard` = `rykard_jefe`, `serpiente` =
  `serpiente_jefe`, `gideon` = `gideon_npc`, `tanith` = `tanith_npc` (misma imagen); `godwyn` = cadáver oscuro → solo camafeo.
- COMENTARIOS reales (≤ 10 días, ESTADO.md): Héctor, uueee y Zohar (pidieron el tema) · críticas con contraburla: m0h4xd
  (gigantes = Messmer, intro), Yuzo («¿la IA hizo la edición?», p3c), Bnet («voz sin IA», p1c) · agradecen: Braulio y Juan
  José (p4b), Andrés, D424, Evil Ryu, Kanintor y Wsefsd (subs).
- FICHAS solo con citas en español verificadas (_investigacion/dossier.md § 1-3: [EG]/[ES-wiki]). Los diálogos verificados
  SOLO en inglés (Gideon, Parches, alma estancada, fantasma, Rya, Bernahl, Tanith, muerte de Rykard) NO van entre comillas:
  rótulos `puesto` parafraseados. Única línea de Rykard verificada en español: «Únete a la familia del Rey Serpiente…».
- MG NUEVOS (mg_er, 22-nov): `inquisicion` (intro, p5b), `red_secuestro` (intro, p4b), `estandarte_caido` (intro, p3),
  `incubadora` (p2), `recibo` (intro con «???», p1). Reusados: expediente (un cargo por puesto; «el juez, juzgado»; sello en
  el n.º 1), linaje (hijos de Rennala ×2; lo que parió la blasfemia ×2), acuerdo (tareas de Márika; la oferta y el botón),
  audiencia (lo ya contado; los narradores de carne y hueso), domino ×3, triada, balanza, muerte_suelta, estandartes, cien.
- MAPAS (mundo.jpg, coordenadas MEDIDAS del dossier § 4): Mansión del Volcán · Raya Lucaria (p4) · red Raya → Caria →
  Leyndell → Mansión (p4b) · Leyndell → Monte Gelmir (p3) · Mansión → Farum Azula con Bernahl de viajero (p1).
- PISTAS voz=True (cortes en sfx/, `post` en guion.py): s_rykard (p3b), s_rya (p2b), s_serpiente (p1b), con rótulo.
  FAB_FX_FINAL=1 python fab.py er_rykard_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALAS TODAS)
"""
import os

import mg_er as E
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .70, .32     # fichas: arriba a la derecha (caja real 966 px → borde derecho a 4,8 %)
TEMA_MAPA = "er"
TEMA = "er"

CAMARA = {}
FUNDIDO = {}

_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")
FALTAN = []             # pantallas pedidas que aún no existen (se cubren con su alternativa)


def _hay(slug):
    return os.path.exists(_P(slug))


def _foto(*cands):
    """Primera imagen que exista: 'p:<pantalla>' o '<pegatina>'."""
    for c in cands:
        r = _P(c[2:]) if c.startswith("p:") else _G(c)
        if os.path.exists(r):
            return r
    return None


def pto(xy, nombre, foto=None, tipo=None):
    return (xy[0], xy[1], nombre, tipo, foto) if foto else (xy[0], xy[1], nombre, tipo)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **fijo):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_G(slug), titulo, tam, tema=TEMA, **fijo), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=600, y=.48, **fijo):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=y, tam=tam, **fijo)


def com(en, cid, dur=6.0, x=.28, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def sil(en, ruta, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara visible y el video corriendo detrás."""
    fn = PE.silueta(ruta, nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="silueta " + os.path.basename(ruta), ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.24, y=.44, tam=500):
    """Objeto flotando sobre un círculo de runas."""
    return dict(tipo="mg", fn=PE.reliquia(_G(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="reliquia " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(_G(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="camafeo " + slug, ver=1.0)


def ban(en, ruta, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    """Tira de cine a todo lo ancho con el rostro en primer plano."""
    return dict(tipo="mg", fn=PE.banda(ruta, nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="banda " + os.path.basename(ruta), ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=290):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(slug, etiqueta ≤ 12 letras)]."""
    return dict(tipo="mg", fn=PE.abanico([(_G(s), t) for s, t in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="abanico " + nombre, ver=2.0)


def leg(slug, titulo, lineas, de, a, marcas, sello=None, x=.22, y=.45, ancho=400):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca) se estampa con la voz."""
    return dict(tipo="mg", fn=PE.legajo(_G(slug), titulo, lineas, sello=sello, ancho=ancho, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + slug, ver=1.6)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0, alt=None):
    """Imagen REAL a pantalla completa (mg_wow.pantalla); si `slug` aún no existe, `alt` (otra pantalla que sí exista)."""
    if not _hay(slug):
        FALTAN.append(slug)
        slug = alt
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None, y=_FY):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None),
             en=en, x=_FX, y=y, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def ban_p(de, a, arriba, titulo, nombre):
    """Rótulo `puesto` con inicio y fin anclados."""
    return mg(E.puesto(arriba, titulo), de, a, [], nombre, y=.80)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def msg(lineas, de, a, marcas, nombre, y=.76):
    """Mensaje del suelo (texto ámbar), para citas en español que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=y)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + (titulo or slug), ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + (titulo or slug), ver=4.0)


# Comentarios (ESTADO.md, leídos el 22-nov; tarjetas en pegatinas/com_<id>.png)
C_HECTOR, C_UUEEE, C_ZOHAR = "UgzskfYL0s1hBc_69Jp4AaABAg", "UgzVNhAjBxzitJU7BEp4AaABAg", "Ugx4vzwfxHhaoJ1zPIh4AaABAg"
C_M0H4, C_YUZO, C_BNET = "UgxWdxhJnobSFfQUNJ14AaABAg", "Ugzh9bqhzp91EhvMG6d4AaABAg", "UgyS54tWqAGyBx1XOpJ4AaABAg"
C_BRAULIO, C_JUANJO = "Ugxqcei_2Z53MIcnz0V4AaABAg", "UgzY9zCIUdDYyIDx5gR4AaABAg"
C_ANDRES, C_D424, C_EVILRYU = "Ugz5ufUmtfLMCJeEC2d4AaABAg", "UgxgUaLISz_C4Zuk2jt4AaABAg", "UgzHsAoNtXF8VTBkEMp4AaABAg"
C_KANINTOR, C_WSEFSD = "UgwEkOuOemdQUfRK0Dp4AaABAg", "UgwFFGipiZmsmyb_ERd4AaABAg"

# Coordenadas MEDIDAS (fracción de mapas/mundo.jpg; dossier § 4). Las marcadas «NO VERIFICADO» allí NO se usan.
M_MANSION = (.228, .325)     # Mansión del Volcán (cotejada con el mapa de mazmorra)
M_RAYA = (.195, .540)        # Academia de Raya Lucaria
M_CARIA = (.19, .405)        # Mansión de los Caria
M_LEYND = (.44, .37)         # Leyndell, capital del Reino
M_FARUM = (.87, .48)         # Farum Azula, la ciudad en ruinas

CARGOS = ["Juez con taller de tortura", "Secuestros a domicilio", "Abandonó su propia guerra", "Los hijos del ritual",
          "Cobró por la noche del complot"]


def expe(k, titulo_frase, dur=3.2):
    """Ficha del acusado al abrir el puesto k (0 = n.º 5): escribe el cargo k; en el n.º 1 cae el sello CULPABLE."""
    fin = (titulo_frase + "|fin", dur + (1.2 if k == 4 else 0))
    marcas = [(titulo_frase + "|fin", -.2)] + ([(titulo_frase + "|fin", 2.0)] if k == 4 else [])
    return mg(E.expediente(acusado="Rykard", sub="pretor, señor de la Blasfemia", cargos=CARGOS[:k + 1], ya=k,
                           sello="CULPABLE" if k == 4 else None, titulo="El juez, juzgado"),
              (titulo_frase + "|fin", -.4), fin, marcas, f"expediente {k + 1}")


INSTR = [("Candelabro de inquisidor", _G("candelabro")), ("Rueda de Ghiza", _G("rueda_ghiza")),
         ("Máscara ensangrentada", _G("mascara_ensangrentada")), ("Atuendo de oficial", _G("atuendo_oficial"))]
VIRGENES = ["Academia de Raya Lucaria", "Mansión de los Caria", "Monte Gelmir", "Afueras de la capital", "Leyndell"]

# Los 3 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026 y regla 10; cortes en sfx/, `post` en guion.py)
PISTAS = [
    dict(sfx="s_rykard", en="en su propia voz. Escúchalo|fin", vol=1.0, voz=True),
    dict(sfx="s_rya", en="de ese cuerpo maldito. Escúchala|fin", vol=1.0, voz=True),
    dict(sfx="s_serpiente", en="una serpiente nunca muere. Escúchalo|fin", vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    ban(("Pretor Rykard", 0), _G("rykard"), "Pretor Rykard", "señor de la Blasfemia", foco=(.5, .45, 1.4), dur=3.0),
    mg(E.linaje(raiz=("Rennala y Radagon", "la reina y su consorte"),
                hijos=(("Rykard", "el pretor"), ("Radahn", "el general"), ("Ranni", "la bruja")),
                medio="los hijos de la reina", remate="Según Zohar, el más cruel de los tres", titulo="Los hijos de Rennala",
                injertos=()),
       ("Hijo de la reina Rennala", -.3), ("y dueño de la Mansión del Volcán", 0.0),   # deja ver la mansión
       ["Hijo de la reina Rennala", "y de Radagon", ("y de Radagon|fin", .2), "hermano de Radahn", "y de Ranni",
        ("y de Ranni|fin", 0)], "hijos de rennala 1"),
    pant("mansion_exterior", ("y dueño de la Mansión del Volcán", -.2), ("en lo alto del monte Gelmir|fin", .6),
         zoom=(1.0, 1.10)),
    mapa("mundo", [pto(M_MANSION, "Mansión del Volcán", _foto("p:mansion_wiki"), "poder")],
         ("en lo alto del monte Gelmir", -.4), ("en lo alto del monte Gelmir|fin", 2.4), ["en lo alto del monte Gelmir"],
         titulo="Monte Gelmir", sub="Mansión del Volcán", ventana=True, x=.66, y=.40, entrada="foco", traza=99),
    cam("Casi todo el mundo lo recuerda", "rykard_jefe", "Rykard", dur=3.6, x=.16, y=.66, foco=(.5, .45, 1.4)),
    grande("el semidiós que se dejó comer", "serpiente", "Serpiente devoradioses", lado="der", dur=4.6, tam=620, y=.44),
    msg(["Únete a la familia del Rey Serpiente.", "¡Juntos devoraremos a los dioses!"], ("únete a la familia", -.1),
        ("Juntos devoraremos a los dioses|fin", 1.2), ["únete a la familia", "Juntos devoraremos"], "unete"),
    puesto("Pero dejarse comer es lo que menos", "Dejarse comer", "Lo que menos daño hizo", dur=3.0),
    mg(E.inquisicion(INSTR, titulo="Su propio taller de tortura"), ("Antes de la serpiente fue juez", -.2),
       ("su propio taller de tortura|fin", .6),
       [("Antes de la serpiente fue juez", 0), ("Antes de la serpiente fue juez", .5), ("y tenía su propio taller", 0),
        ("y tenía su propio taller", .5)], "inquisicion gancho"),
    mg(E.red_secuestro(VIRGENES, destino="Su sótano", sub_destino="Mansión del Volcán", remate="Por todo el mapa",
                       titulo="Máquinas que secuestran gente"),
       ("Hay máquinas que secuestran", -.2), ("y la dejan en su sótano|fin", .6),
       [("Hay máquinas que secuestran", 0), ("Hay máquinas que secuestran", .35), ("Hay máquinas que secuestran", .7),
        ("secuestran gente por todo", 0), ("secuestran gente por todo", .4), "y la dejan en su sótano"], "red gancho"),
    mg(E.estandarte_caido(emblema="Caballeros de Gelmir", quien="la guerra del pretor Rykard",
                          remate="La guerra más espantosa de la Devastación", titulo="La guerra que dejó tirada"),
       ("Y dejó tirada la guerra", -.2), ("guerra más espantosa de toda la Devastación|fin", 1.0),
       [("Y dejó tirada la guerra", .2), ("Y dejó tirada la guerra", 1.0), "guerra más espantosa de toda la Devastación"],
       "estandarte gancho"),
    puesto("Y la número uno la llevaste", "La número uno", "En tu inventario", dur=3.2),
    cam("contra uno de los jefes más difíciles", "maliketh", "Maliketh", dur=3.6, x=.84, y=.40, foco=(.5, .4, 1.3)),
    mg(E.recibo(concepto="la noche en que murió un dios", pagador="???", cobrador="Rykard", pago="???", sello="PAGADO",
                titulo="Era un pago"),
       ("Era un pago", -.3), ("Era un pago. Por la noche en que murió un dios|fin", 1.2),
       [("Era un pago", 0), ("Era un pago", .4), ("Era un pago. Por la noche", 0), ("Era un pago. Por la noche", .5),
        ("Era un pago. Por la noche en que murió un dios|fin", .1)], "recibo gancho"),
    puesto(("Este video lo pidieron ustedes", 1.2), "Lo pidieron ustedes", "Con mucha insistencia", dur=3.0),
    com("Héctor lleva siete intentos", C_HECTOR, dur=10.6),
    com("Otro usuario nos lleva la cuenta", C_UUEEE, dur=6.4, x=.72, y=.36),
    com("Y Zohar nos pidió cerrar", C_ZOHAR, dur=7.6),
    cam("de los hijos de Rennala", "rennala", "Rennala", dur=3.4, x=.84, y=.30, foco=(.5, .4, 1.4)),   # chequeo: se nombra
    aba([("ranni", "Ranni"), ("radahn", "Radahn"), ("rykard", "Rykard")], ("cerrar la trilogía", -.1),
        ("el más cruel de los tres|fin", .6), ["cerrar la trilogía", ("cerrar la trilogía", .5), "este es el más cruel"],
        "trilogia", x=.74, y=.68, tam=230),
    puesto("Héctor, no hizo falta el octavo", "Héctor", "No hizo falta el octavo", dur=3.4),
    cam("los contratos de asesinato de Tanith", "tanith", "Tanith", dur=2.2, x=.16, y=.66, foco=(.5, .3, 1.6)),
    mg(E.audiencia(campeones=("Campeón", "Campeón", "Campeón"), tu="Hoy", sub_tu="todo lo demás",
                   remate="Ya contado en el video del Sinluz", titulo="La audiencia con la serpiente"),
       ("y la audiencia con la serpiente", .5), ("que es bastante peor|fin", .8),
       [("y la audiencia con la serpiente", .6), ("y la audiencia con la serpiente", 1.1),
        ("y la audiencia con la serpiente", 1.6), "Hoy va todo lo demás"], "audiencia sinluz"),
    puesto("Antes de empezar, una corrección", "Antes de empezar", "Una corrección", dur=2.8),
    com("En el video de Godfrey, alguien", C_M0H4, dur=7.0),
    cam("Messmer también exterminaba", "messmer", "Messmer", dur=5.4, x=.84, y=.40, foco=(.5, .3, 1.6)),
    ban_p(("su cruzada purificadora", -.1), ("en el Reino de las Sombras|fin", .6), "La cruzada de Messmer",
          "Contra los cornamentados", "cruzada"),
    cam("Los gigantes fueron cosa de Godfrey", "godfrey", "Godfrey", dur=2.6, x=.16, y=.40),
    rel("Lo dice su propia corona", "corona_senor", "Corona de Señor del Círculo", dur=5.0),
    ficha("Lo dice su propia corona", "Corona de Señor del Círculo", "Corona de Godfrey, el primer Señor del Círculo. La era "
          "del Árbol Áureo empezó en mitad de un enfrentamiento, cuando Godfrey era el señor de la Batalla. *Lideró la "
          "guerra contra los gigantes*.", tipo="Yelmo", icono="corona_senor",
          a=("lideró la guerra contra los gigantes|fin", .6)),
    mg(E.acuerdo(["Al marido: los gigantes", "Al hijo: los cornamentados"], "Exterminar sin quejarse",
                 letra="Guerras de exterminio por encargo", titulo="Las tareas de la casa", remate="Sin quejas",
                 cab=("Márika reparte", "Ellos cumplen")),
       ("Márika repartía las guerras", -.2), ("Y ninguno se quejó|fin", 1.6),
       ["Una para el marido", "otra para el hijo", ("otra para el hijo|fin", .3), "Y ninguno se quejó",
        ("Y ninguno se quejó|fin", .2)], "tareas"),

    # ================================================================ 5 · EL JUEZ CON TALLER DE TORTURA
    puesto("Número cinco", "Atrocidad número 5", "El juez con taller de tortura"),
    expe(0, "El juez con taller de tortura", dur=3.0),
    # pantallas/retrato_rykard.jpg NO es el retrato de Rykard (revisión 22-nov: el de la wiki es de perfil, con corona y
    # espada) → su textura real (wiki ES «Retrato de Rykard»), en marco de museo
    peg(("Rykard era la ley", -.2), "retrato_rykard_wiki", "Retrato de Rykard", dur=5.6, x=.22, y=.40, tam=440,
        marco="museo"),
    ban_p(("Rykard era la ley", -.1), ("es el de un magistrado|fin", .4), "Rykard era la ley", "Pretor: un magistrado",
          "pretor"),
    cam("En la Mesa Redonda, Gideon", "mesa_redonda", "Mesa Redonda", dur=2.6, x=.84, y=.30, foco=(.5, .5, 1.2)),
    peg("el Omnisciente, te lo describe", "gideon_npc", "Gideon Ofnir", dur=4.4, x=.22, y=.34, tam=420),
    ban_p(("como un juez despiadado", -.1), ("compañía de inquisidores|fin", 1.0), "Según Gideon",
          "Juez despiadado al mando de inquisidores", "juez despiadado"),
    puesto("lo aborrecían por sus maneras", "Lo aborrecían", "Por sus maneras de serpiente", dur=3.6),
    cam("antes de que fuera una serpiente de verdad", "serpiente_jefe", "La serpiente", dur=3.4, x=.84, y=.40,
        foco=(.5, .45, 1.3)),
    rel("El casco de sus caballeros de Gelmir", "casco_gelmir", "Casco de caballero de Gelmir", dur=9.0),
    ficha("El casco de sus caballeros de Gelmir", "Casco de caballero de Gelmir", "[…] *Su penacho de plumas rojas es un "
          "símbolo del pedigrí de Rykard como hijo del señor Radagon*.", tipo="Yelmo", icono="casco_gelmir",
          a=("como hijo del señor Radagon|fin", .2)),
    cam(("El rojo de Radagon", .3), "radagon", "Radagon", dur=3.6, x=.84, y=.68, foco=(.5, .25, 1.6)),
    pant("mansion_wiki", ("La Mansión del Volcán parece un palacio", -.3), ("te ofrece una familia|fin", .4),
         zoom=(1.0, 1.10)),
    cam("una anfitriona amable", "tanith", "Tanith", dur=3.4, x=.84, y=.66, foco=(.5, .3, 1.6)),
    puesto("Pero fíjate en los nombres", "Fíjate en los nombres", "De sus lugares de gracia", dur=3.6),
    pant("iglesia_penados", ("Uno se llama Iglesia", -.3), ("Otro, Cámara subterránea", -.1), zoom=(1.0, 1.10)),
    ban_p(("Uno se llama Iglesia", -.1), ("de la ciudad de los penados|fin", .4), "Lugar de gracia",
          "Iglesia de la ciudad de los penados", "penados"),
    pant("camara_inquisicion", ("Otro, Cámara subterránea", -.3), ("Otro, Cámara subterránea de la inquisición|fin", 1.0),
         zoom=(1.0, 1.10)),
    ban_p(("Otro, Cámara subterránea", -.1), ("Otro, Cámara subterránea de la inquisición|fin", .8), "Lugar de gracia",
          "Cámara subterránea de la inquisición", "camara"),
    puesto("Nadie les pone esos nombres", "Casa de huéspedes", "Con cámara de inquisición", dur=4.0),
    puesto("el juego te deja un objeto", "Un objeto", "Que lo cuenta todo", dur=2.8),
    rel("lo cuenta todo. El Candelabro", "candelabro", "Candelabro de inquisidor", dur=11.0),

    # ---- 5b · el candelabro, Ghiza y su ropa
    ficha("Instrumento de tortura utilizado en secreto", "Candelabro de inquisidor", "Instrumento de tortura utilizado *en "
          "secreto contra nobles* en la Mansión del Volcán del monte Gelmir. Sus numerosas púas atraviesan la carne antes de "
          "hacerla arder con las llamas del arma. El olor a sangre quemada provocaba la desesperación de la víctima. Un "
          "candelabro concebido por una mente meticulosa.", tipo="Arma de asta", icono="candelabro",
          a=("concebido por una mente meticulosa|fin", .8), y=.37),
    ban_p(("En secreto, y contra nobles", -.1), ("ni contra herejes de la calle|fin", .5), "En secreto",
          "Y contra nobles", "en secreto"),
    mg(E.inquisicion(INSTR, titulo="Archivo de la inquisición"), ("Contra gente con apellido", -.2),
       ("en la casa del juez|fin", .8), ["Contra gente con apellido"], "inquisicion 1"),
    puesto("Y la inquisición tenía empleados", "La inquisición", "Tenía empleados", dur=3.2),
    grande("el inquisidor Ghiza, armado", "ghiza", "Inquisidor Ghiza", lado="der", dur=4.6, tam=560, y=.46),
    rel("La Rueda de Ghiza es un instrumento", "rueda_ghiza", "Rueda de Ghiza", dur=9.4),
    ficha("La Rueda de Ghiza es un instrumento", "Rueda de Ghiza", "Gran rueda de hierro revestida de cuchillas que desgarran "
          "la carne. Es un instrumento de tortura usado por el inquisidor Ghiza. *El giro de la rueda provoca fuertes "
          "dolores y hemorragia*.", tipo="Gran martillo", icono="rueda_ghiza",
          a=("fuertes dolores y hemorragia|fin", .8)),
    peg("con la Máscara ensangrentada", "mascara_ensangrentada", "Máscara ensangrentada", dur=6.4, x=.20, y=.56, tam=420),
    ficha("con la Máscara ensangrentada", "Máscara ensangrentada", "*Máscara hecha a partir de vendas muy ceñidas y "
          "empapadas en sangre*. Incluso la cobertura más macabra resulta más atractiva que la cara supurante que oculta "
          "debajo.", tipo="Yelmo", icono="mascara_ensangrentada", a=("y empapadas en sangre|fin", .3)),
    rel("Y su ropa es el Atuendo", "atuendo_oficial", "Atuendo de oficial", dur=8.0),
    ficha("Y su ropa es el Atuendo", "Atuendo de oficial", "Túnica azul mugrienta que llevan *los oficiales autorizados para "
          "desempeñar su macabro oficio*. Control, ejecuciones, rituales truculentos... *Las tareas más oscuras mueven los "
          "engranajes de la humanidad*.", tipo="Armadura", icono="atuendo_oficial",
          a=("mueven los engranajes de la humanidad|fin", .4)),
    ban_p(("Esa descripción termina con una frase", -.1), ("el lema de la mansión entera|fin", .4), "Atuendo de oficial",
          "El lema de la mansión", "lema"),
    mg(E.inquisicion(INSTR, titulo="Archivo de la inquisición"), ("Ese era Rykard antes de la blasfemia", .2),
       ("El hombre que juzgaba a los demás|fin", 1.2),
       [("Ese era Rykard antes de la blasfemia", .2), ("Ese era Rykard antes de la blasfemia", .5),
        ("Ese era Rykard antes de la blasfemia", .8), ("Ese era Rykard antes de la blasfemia", 1.1),
        "El hombre que juzgaba"], "inquisicion 2"),
    cam("Y la rueda de Ghiza no se quedó", "rueda_ghiza", "La rueda", dur=3.6, x=.84, y=.40, foco=(.5, .4, 1.3)),
    puesto("Su diseño se copió", "Su diseño se copió", "Para algo más grande", dur=3.4),

    # ================================================================ 4 · SECUESTROS A DOMICILIO
    puesto("Número cuatro", "Atrocidad número 4", "Secuestros a domicilio", dur=3.0),
    expe(1, "Secuestros a domicilio", dur=2.2),
    mapa("mundo", [pto(M_RAYA, "Academia de Raya Lucaria", _foto("p:raya_lucaria"), "meta")],
         ("en Liurnia, un personaje", -.2), ("te da un consejo|fin", .4), ["en Liurnia, un personaje"],
         titulo="Liurnia", sub="Academia de Raya Lucaria", ventana=True, x=.34, y=.40,
         entrada="desenrolla", traza=99),
    grande("Es Parches, el mismo", "parches", "Parches", lado="der", dur=5.0, tam=540, y=.46),
    grande("Te habla de las vírgenes", "virgen_raptora", "Virgen raptora", lado="izq", dur=5.6, tam=520, y=.40),
    ban_p(("máquinas torpes, torbellinos", -.1), ("y ruedas con púas|fin", .5), "Vírgenes de hierro",
          "Hoces y ruedas con púas", "hoces"),
    ban_p(("un hechizo de transposición", -.2), ("Que pueden llevarte muy lejos|fin", .8), "Según Parches",
          "Un hechizo de transposición", "transposicion"),
    pant("virgen_noria", ("en el fondo de la gran noria", -.3), ("queda una que todavía funciona|fin", .8),
         zoom=(1.0, 1.10)),
    puesto("te saca justo al pie del Árbol", "Según Parches", "Te saca al pie del Árbol Áureo", dur=3.8),
    cam("O eso dicen", "parches", "Parches", dur=3.0, x=.84, y=.40, foco=(.5, .25, 1.6)),
    puesto("Y miles de jugadores lo hicieron", "Miles de jugadores", "Se dejaron agarrar", dur=3.6),
    ban("La virgen raptora abre el pecho", _G("virgen_raptora"), "Virgen raptora", "tentáculos de serpiente",
        foco=(.5, .45, 1.0), dur=4.6, y=.20),
    ban_p(("y no te suelta hasta que estás muerto", -.1), ("hasta que estás muerto|fin", 1.0), "No te suelta",
          "Hasta que estás muerto", "muerto"),
    mapa("mundo", [pto(M_RAYA, "Academia de Raya Lucaria", None, "inicio"),
                   pto(M_MANSION, "Mansión del Volcán", _foto("p:camara_inquisicion"), "meta")],
         ("Y despiertas encerrado", -.3), ("de la inquisición de la Mansión del Volcán|fin", .6),
         ["Y despiertas encerrado", "sino en la Cámara subterránea"], titulo="El atajo de Parches",
         sub="Cámara subterránea de la inquisición", entrada="foco", traza=99),
    pant("camara_wiki", ("Sin poder salir y sin poder viajar", -.3), ("dos vírgenes raptoras más|fin", .6),
         zoom=(1.0, 1.10)),
    ban_p(("Sin poder salir y sin poder viajar", -.1), ("dos vírgenes raptoras más|fin", .5), "Encerrado",
          "Hasta vencer a dos vírgenes más", "encerrado"),
    puesto("Una gira con ruedas dentadas", "Dos vírgenes raptoras", "Ruedas y guadañas", dur=4.0),
    rel("te dejan su premio", "candelabro", "Candelabro de inquisidor", "su premio", dur=5.0, y=.40),
    ban_p(("El mismo instrumento de tortura de la mansión", -.1), ("El mismo instrumento de tortura de la mansión|fin", 1.0),
          "El mismo instrumento", "De la mansión", "mismo instrumento"),

    # ---- 4b · la red de secuestro
    puesto("Y aquí se cierra el círculo", "Aquí se cierra", "El círculo", dur=3.0),
    rel("La descripción completa de la Rueda", "rueda_ghiza", "Rueda de Ghiza", dur=10.6),
    ficha("La descripción completa de la Rueda", "Rueda de Ghiza", "Gran rueda de hierro revestida de cuchillas que desgarran "
          "la carne. Es un instrumento de tortura usado por el inquisidor Ghiza. El giro de la rueda provoca fuertes dolores "
          "y hemorragia. *Su diseño se adoptó para usarlo en las emblemáticas armas blandidas por las vírgenes de hierro*.",
          tipo="Gran martillo", icono="rueda_ghiza", a=("blandidas por las vírgenes de hierro|fin", .8), y=.35),
    aba([("rueda_ghiza", "Ghiza"), ("virgen_raptora", "Las vírgenes")], ("La rueda del torturador", -.2),
        ("te dejó en su sótano|fin", .6), ["La rueda del torturador", "es la rueda de las máquinas"], "misma rueda",
        tam=330),
    mapa("mundo", [pto(M_RAYA, "Academia de Raya Lucaria", _foto("p:virgen_noria"), "inicio"),
                   pto(M_CARIA, "Mansión de los Caria"), pto(M_LEYND, "Leyndell, capital del Reino"),
                   pto(M_MANSION, "Mansión del Volcán", None, "meta")],     # sin foto: tapaba su rótulo y el de Caria
         ("Y no es solo la de la Academia", -.3), ("de punta a punta del mapa|fin", .4),
         ["Y no es solo la de la Academia", "en la Mansión de los Caria", "dentro de la propia Leyndell",
          "Una red de máquinas de secuestro"], titulo="Las vírgenes raptoras", sub="Una red de punta a punta",
         entrada="mesa", traza=1.7),
    mg(E.red_secuestro(VIRGENES, destino="Cámara de la inquisición", sub_destino="Mansión del Volcán",
                       remate="Todas acaban en el sótano de Rykard", titulo="Adónde van los pasajeros"),
       ("Ojo con esto: el juego nunca dice", -.2), ("En la cámara de la inquisición de Rykard|fin", .6),
       [("Ojo con esto", .2), ("Ojo con esto", .6), ("Ojo con esto", 1.0), "el juego nunca dice quién", "Lo que sí enseña",
        "En la cámara de la inquisición de Rykard"], "red de secuestro"),
    leg("parches", "Parches", ["Oficio: estafador", "Te mandó a la virgen", "Su versión: no mintió"],
        ("Y Parches lo sabía", .2), ("te lo dice con toda la calma del mundo|fin", .6),
        [("Y Parches lo sabía", .3), ("te lo dice con toda la calma", 0)]),
    ban_p(("que él no había mentido en absoluto", -.1), ("estaba justo ahí fuera|fin", .8), "Según Parches",
          "El Árbol estaba justo fuera", "no mintio"),
    pant("gelmir", ("Más tarde, en las laderas", -.3), ("que te alejes de la Mansión del Volcán|fin", .4),
         zoom=(1.0, 1.12)),
    ban_p(("te empuja por un precipicio", -.1), ("que te alejes de la Mansión del Volcán|fin", .4), "Parches te empuja",
          "Aléjate de la Mansión del Volcán", "alejate"),
    ban_p(("ha oído que los brutos", -.1), ("como si fueran animales|fin", .8), "Allí", "Cazan Sinluz como animales",
          "cazan sinluz"),
    puesto("Es el único consejo honesto", "El único consejo honesto", "De Parches", dur=3.4),
    puesto("Y te lo da después de tirarte", "Después de tirarte", "Por un barranco", dur=3.0),
    puesto("Y antes de seguir, dos comentarios", "Antes de seguir", "Dos comentarios", dur=2.4),
    com("Braulio dice que se volvió adicto", C_BRAULIO, dur=5.6),
    com("Y Juan José dice que se han vuelto", C_JUANJO, dur=8.0, x=.75, y=.36),
    puesto("Juan José, ese día es hoy", "Juan José", "Ese día es hoy", dur=3.4),
    puesto("Braulio, lo tuyo no tiene cura", "Braulio", "Lo tuyo no tiene cura", dur=3.0),
    peg("Pero conozco una virgen raptora", "virgen_raptora", "Directo al Árbol Áureo", dur=5.0, x=.76, y=.50, tam=400),

    # ================================================================ 3 · LA GUERRA QUE ABANDONÓ
    puesto("Número tres", "Atrocidad número 3", "La guerra que abandonó", dur=3.0),
    expe(2, "La guerra que abandonó", dur=2.4),
    mapa("mundo", [pto(M_LEYND, "Leyndell, capital del Reino", None, "inicio"),
                   pto(M_MANSION, "Monte Gelmir", _foto("p:gelmir"), "peligro")],
         ("el monte Gelmir, al oeste", -.3), ("Devastación. De todas|fin", .8),
         ["el monte Gelmir, al oeste", "fue el escenario de la batalla"], titulo="Meseta Altus",
         sub="La batalla más espantosa", entrada="mesa", traza=99),
    pant("monumento_asalto", ("Junto al noveno campamento", -.3), ("que no concede la gloria|fin", 1.4),
         zoom=(1.42, 1.48), pan=(0, -1, .2, -1)),            # recorta el texto en inglés del monumento (abajo)
    puesto("un monumento con una espada clavada", "Noveno campamento del monte Gelmir", "Un monumento con espada",
           dur=3.6),
    msg(["El asalto a la Mansión del Volcán:", "lo sórdido, lo enfermizo, lo profano;",
         "una guerra miserable interminable", "que no concede la gloria."],
        ("El asalto a la Mansión del Volcán", -.1), ("que no concede la gloria|fin", 1.2),
        ["El asalto a la Mansión del Volcán", "Lo sórdido, lo enfermizo", "Una guerra miserable interminable",
         "que no concede la gloria"], "asalto", y=.60),
    ficha("El propio mapa del monte Gelmir", "Mapa: Monte Gelmir", "El monte Gelmir, en cuya cima se encuentra la Mansión "
          "del Volcán, se caracteriza por sus escarpados acantilados y su clima amenazador, *peligros que se agudizan aún "
          "más tras la Devastación*.", tipo="Objeto clave", a=("aún más tras la Devastación|fin", 1.0)),
    puesto("Todavía hoy, las laderas", "Todavía hoy", "Campamentos en ruinas", dur=3.8),
    ban_p(("Era su guerra", -.1), ("y su mansión|fin", .1), "Era su guerra", "Su montaña, sus caballeros, su mansión",
          "su guerra"),
    puesto(("Y en plena guerra, el semidiós", .2), "En plena guerra", "El que la dirigía hizo esto", dur=3.2),
    rel("La Gran Runa de Rykard lo cuenta", "runa_rykard", "Gran Runa de Rykard", dur=7.6),
    ficha("La Gran Runa de Rykard lo cuenta", "Gran Runa de Rykard", "Rykard era uno de los hijos de Rennala y Radagon, y se "
          "convirtió en semidiós adoptivo tras la unión de Radagon con la Reina Márika. *Pero Rykard se ofreció como "
          "alimento a la serpiente blasfema, runa incluida*.", tipo="Gran Runa", icono="runa_rykard",
          a=("a la serpiente blasfema, runa incluida|fin", .6)),
    puesto(("Runa incluida#2", 0), "Runa incluida", "Su fragmento del Círculo", dur=2.2),
    mg(E.domino(["Su fragmento del Círculo", "El poder de la guerra", "A una serpiente", "Sus hombres, muriendo"],
                titulo="Runa incluida"),
       ("Su fragmento del Círculo de Elden", .1), ("morían ahí fuera por él|fin", 1.0),
       [("Su fragmento del Círculo", .2), "el poder por el que todos", "se lo entregó a la boca", "Mientras sus hombres morían"],
       "runa incluida"),
    puesto("Y sus hombres se dieron cuenta", "Sus hombres", "Se dieron cuenta", dur=2.6),
    pant("almas_camino", ("En el camino que sube a la mansión", -.3), ("hablándole a su señor|fin", .5), zoom=(1.0, 1.10)),
    ban_p(("Le dice que si este campo de muerte", -.1), ("Nadie puede|fin", 1.0), "Alma estancada",
          "Si esto trae tu blasfemia, nadie te seguirá", "nadie puede"),
    rel("La Armadura de caballero de Gelmir lo deja", "armadura_gelmir", "Armadura de caballero de Gelmir", dur=6.0),
    ficha("La Armadura de caballero de Gelmir lo deja", "Armadura de caballero de Gelmir", "Armadura usada por los caballeros "
          "que antaño le eran leales al pretor Rykard. Muestra un emblema que ya nadie usa, puesto que representa a *un "
          "señor que empezó con nobles ambiciones pero acabó cayendo en una ávida depravación*.", tipo="Armadura",
          icono="armadura_gelmir", a=("acabó cayendo en una ávida depravación|fin", .4)),
    mg(E.estandarte_caido(emblema="Caballeros de Gelmir", quien="un señor que empezó con nobles ambiciones",
                          remate="Perdieron a su maestro", titulo="Un emblema que ya nadie usa"),
       ("Al perder el señor su dignidad", -.4), ("perdieron a su maestro|fin", 1.6),
       ["Al perder el señor su dignidad", "estos caballeros también perdieron", ("perdieron a su maestro|fin", .1)],
       "estandarte gelmir"),

    # ---- 3b · los que quisieron detenerlo
    puesto("Pero no todos se fueron", "No todos se fueron", "Algunos intentaron arreglarlo", dur=3.8),
    rel("El Cazador de serpientes, una lanza", "cazador_serpientes", "Cazador de serpientes", dur=10.0),
    ficha("El Cazador de serpientes, una lanza", "Cazador de serpientes", "[…] Cuando las aspiraciones heroicas del señor "
          "degeneraron hasta convertirse en mera avaricia, *sus hombres buscaron un arma con la que pudieran detenerlo*.",
          tipo="Gran lanza", icono="cazador_serpientes", a=("con la que pudieran detenerlo|fin", .8)),
    ban_p(("Sus propios soldados, buscando", -.1), ("para matar a su señor|fin", .6), "Sus propios soldados",
          "Un arma para matar a su señor", "matar a su senor"),
    pant("cadaveres_cazador", ("Clavada en un montón de cadáveres", -.4), ("No llegaron a usarla|fin", .8),
         zoom=(1.0, 1.10)),
    puesto("Y uno de ellos ni siquiera se fue", "Uno de ellos", "Ni muerto se fue", dur=3.6),
    peg("aparece el fantasma de un caballero", "casco_gelmir", "Un caballero de Gelmir", dur=5.0, x=.20, y=.40, tam=400),
    ban_p(("Te pide, por favor, que alguien lo mate", -.1), ("A esa horrible serpiente. Al pretor Rykard|fin", .8),
          "El fantasma", "Que alguien lo mate", "que lo maten"),
    cam("dejó la lanza matasierpes", "cazador_serpientes", "Matasierpes", dur=3.6, x=.16, y=.40, foco=(.5, .4, 1.4)),
    ban_p(("Y que las ambiciones del pretor", -.1), ("en cuanto se entregó a la serpiente|fin", .8), "Un soberano digno",
          "Reducido a una depravación glotona", "glotona"),
    ban_p(("Y remata: lo que sea esa cosa", -.1), ("más deshonra|fin", .6), "Esa cosa", "Ya no es el pretor Rykard",
          "esa cosa"),
    cam("lo que sea esa cosa", "serpiente_jefe", "Esa cosa", dur=3.8, x=.84, y=.40, foco=(.5, .45, 1.3)),
    puesto("El último leal que le quedaba", "El último leal", "Te pide que lo mates", dur=4.0),
    pant("arena_rykard", ("Y cuando lo haces, en el sitio", -.3), ("te queda un gesto: dar las gracias|fin", .6),
         zoom=(1.0, 1.10)),
    puesto("te queda un gesto", "Su último regalo", "Un gesto: dar las gracias", dur=4.0),
    ban_p(("Es el único habitante de esa mansión", -.1), ("que te agradece algo de verdad|fin", .8), "El único",
          "Que te agradece algo de verdad", "agradece"),
    puesto("Y qué había dentro de la serpiente", "Dentro de la serpiente", "¿Qué había?", dur=2.6),
    rel("La Hoja blasfema, la espada", "hoja_blasfema", "Hoja blasfema", dur=8.0),
    ficha("La Hoja blasfema, la espada", "Hoja blasfema", "Arma sagrada de Rykard, señor de la Blasfemia. *Los restos de la "
          "infinidad de héroes a los que ha devorado se retuercen en la superficie de esta espada*. Ahora, comparten la "
          "misma sangre y están unidos como familia.", tipo="Espadón", icono="hoja_blasfema",
          a=("están unidos como familia|fin", .6)),
    pant("arena_rykard", ("En la arena, junto a la serpiente", -.3), ("con el Sobretodo ocular|fin", .6),
         zoom=(1.10, 1.0)),
    peg("con el Sobretodo ocular", "sobretodo_ocular", "Sobretodo ocular", dur=6.0, x=.20, y=.54, tam=420),
    ficha("con el Sobretodo ocular", "Sobretodo ocular", "*La insignia de la parte delantera designa a su portador como los "
          "ojos y oídos de Sir Gideon el Omnisciente*.", tipo="Armadura", icono="sobretodo_ocular",
          a=("Sir Gideon el Omnisciente|fin", 1.0)),
    puesto("El espía de Gideon también", "El espía de Gideon", "También acabó en el menú", dur=3.6),
    ban("Y así es como Rykard te invita", _G("rykard_jefe"), "Rykard", "en su propia voz", foco=(.5, .45, 1.4), dur=5.4,
        y=.20),
    ban_p(("en su propia voz. Escúchalo|fin", .1), ("en su propia voz. Escúchalo|fin", 9.8),
          "Únete a la familia del Rey Serpiente", "Juntos devoraremos a los dioses", "pista rykard"),

    # ---- 3c · Yuzo y la IA
    puesto("Familia, lo llama", "Familia", "Lo llama", dur=2.8),
    com("Yuzo nos preguntó", C_YUZO, dur=7.0),
    ban_p(("No, Yuzo, no eres tú", -.1), ("nunca se lo hemos escondido a nadie|fin", .8), "No eres tú",
          "Aquí hay inteligencia artificial", "ia"),
    cam("Pero no te preocupes por eso", "tanith", "Tanith", dur=3.2, x=.84, y=.40, foco=(.5, .3, 1.6)),
    grande("lo más artificial sigue siendo", "tanith_npc", "Tanith", lado="izq", dur=4.8, tam=500, y=.42),
    puesto("lo más artificial sigue siendo", "Lo más artificial", "La sonrisa de Tanith", dur=4.0),

    # ================================================================ 2 · LOS HIJOS DEL RITUAL
    puesto("Número dos", "Atrocidad número 2", "Los hijos del ritual", dur=2.6),
    expe(3, "Los hijos del ritual", dur=2.4),
    ban_p(("Lo repite en cada frase", -.1), ("Y la consiguió|fin", .8), "Rykard quería", "Una familia", "una familia"),
    puesto("Lo que nadie hizo fue preguntarle", "Nadie le preguntó", "A la familia", dur=3.4),
    grande("los hombres serpiente, con látigos", "hombre_serpiente", "Hombre serpiente", lado="der", dur=3.6, tam=560,
           y=.46),
    rel("Sus cenizas de espíritu cuentan", "cenizas_hombre_serpiente", "Cenizas de hombre serpiente", dur=16.0),
    ficha("Sus cenizas de espíritu cuentan", "Cenizas de hombre serpiente", "Espíritu de un hombre serpiente deformado que "
          "empuña un látigo de magma. *Se dice que, hace mucho tiempo, la anciana serpiente que habitaba en el Monte Gelmir "
          "devoró a un semidiós, lo cual provocó el nacimiento de los hombres serpiente*.", tipo="Cenizas de espíritu",
          icono="cenizas_hombre_serpiente", a=("el nacimiento de los hombres serpiente|fin", .4)),
    mg(E.linaje(raiz=("Rykard", "el semidiós devorado"), hijos=(("Hombres serpiente", "una especie entera"),),
                medio="la blasfemia", remate="Parió una especie entera", titulo="Lo que parió la blasfemia", injertos=()),
       ("Un semidiós devorado por la serpiente", .4), ("Parió una especie entera|fin", 1.4),
       [("Un semidiós devorado por la serpiente", .5), "solo sabemos de uno que", "La blasfemia de Rykard no se quedó",
        "Parió una especie entera"], "parió una especie"),
    rel("El Disparo de magma dice", "disparo_magma", "Disparo de magma", dur=7.0),
    ficha("El Disparo de magma dice", "Disparo de magma", "*Tras descubrir los antiguos maleficios de Gelmir, Rykard, hijo de "
          "la Reina Rennala, los volvió a poner en práctica* como nuevas formas de hechicería.", tipo="Hechizo",
          icono="disparo_magma", a=("los volvió a poner en práctica|fin", .8)),
    puesto("Resucitó una religión vieja", "Resucitó", "Una religión vieja", dur=3.4),
    rel("De esa religión queda la Espada curva", "espada_dios_serpiente", "Espada curva de dios serpiente", dur=12.6),
    ficha("De esa religión queda la Espada curva", "Espada curva de dios serpiente", "Espada curva que presenta la imagen de "
          "una antigua deidad con forma de serpiente. Herramienta empleada en una religión olvidada que se practicaba en el "
          "Monte Gelmir. *Aunque antes se usaba para ofrecer sacrificios*, esta espada restaura PS al matar a un enemigo.",
          tipo="Espada curva", icono="espada_dios_serpiente", a=("se usaba para ofrecer sacrificios|fin", 1.0), y=.35),
    pant("eiglay", ("Ahora entra en el Templo de Eiglay", -.3), ("la iglesia de la mansión|fin", .3), zoom=(1.0, 1.10)),
    ban_p(("Ahora entra en el Templo de Eiglay", -.1), ("la iglesia de la mansión|fin", .3), "Lugar de gracia",
          "Templo de Eiglay", "eiglay"),
    pant("altar_eiglay", ("Sobre el altar cuelga", -.3), ("una piel de serpiente mudada|fin", .8), zoom=(1.0, 1.25),
         pan=(0, 0, .5, -.6)),                                 # la piel de serpiente, arriba a la derecha
    cam("después de matar al Noble sacrodermo", "noble_sacrodermo", "Noble sacrodermo", dur=3.4, x=.84, y=.66,
        foco=(.5, .35, 1.3)),
    rel("encuentras un objeto húmedo", "amnios", "Amnios de serpiente", dur=4.6, y=.44),
    mg(E.incubadora(etiqueta="Vástago no deseado", sub="fruto de un repulsivo ritual de parto",
                    remate="Jamás llegará a secarse", titulo="Amnios de serpiente"),
       ("Amnios del útero que albergó", -.3), ("jamás llegará a secarse|fin", 1.6),
       ["Amnios del útero que albergó", "pobre vástago no deseado", "jamás llegará a secarse"], "amnios"),

    # ---- 2b · Rya
    puesto("De quién era ese útero", "¿De quién era", "Ese útero?", dur=3.0),
    grande("Rya, la chica de Liurnia", "rya", "Rya", lado="izq", dur=5.0, tam=500, y=.44),
    ban_p(("por tener la mano firme", -.1), ("incluso con los tuyos|fin", .8), "Rya te elogió",
          "Despiadado, incluso con los tuyos", "despiadado"),
    ban_p(("Un día oye algo detrás", -.1), ("escamas que se arrastran|fin", .6), "Detrás de las paredes",
          "Respiración, escamas que se arrastran", "paredes"),
    pant("rya_serpiente", ("Y cuando por fin se ve a sí misma", -.3), ("su nombre real es Zorayas|fin", 1.0),
         zoom=(1.0, 1.10)),
    puesto("su nombre real es Zorayas", "Su nombre real", "Zorayas", dur=3.6),
    ban_p(("A ella le habían contado", -.1), ("de un rey glorioso|fin", .5), "Le contaron",
          "Nació por la gracia de un rey glorioso", "rey glorioso"),
    cam("Y Tanith la crio", "tanith", "Tanith", dur=3.2, x=.84, y=.66, foco=(.5, .3, 1.6)),
    rel("cuando le llevas el amnios", "amnios", "Amnios de serpiente", dur=6.0),
    ficha("cuando le llevas el amnios", "Amnios de serpiente", "Amnios del útero que albergó este *pobre vástago no deseado "
          "fruto de un repulsivo ritual de parto*. Permanece siempre húmedo y jamás llegará a secarse.", tipo="Objeto clave",
          icono="amnios", a=("nació dentro de eso|fin", 1.2)),
    puesto("Lo que dice después es lo más triste", "Lo más triste", "De toda la mansión", dur=3.2),
    mg(E.domino(["Una hija no deseada", "Nacida de un ritual", "Ni hombres ni serpientes"], titulo="Lo que dice Rya"),
       ("Que fue una hija no deseada", -.4), ("ni por las serpientes|fin", 1.0),
       ["Que fue una hija no deseada", "Nacida no de la gracia", "Algo que nunca podrá ser aceptado"], "rya"),
    ban("Y entonces te pide una única cosa", _G("rya"), "Rya", "Zorayas", foco=(.5, .42, 1.3), dur=5.6, y=.20),
    ban_p(("de ese cuerpo maldito. Escúchala|fin", .1), ("de ese cuerpo maldito. Escúchala|fin", 4.6), "Rya",
          "Mátame, por favor", "pista rya"),

    # ---- 2c · la hija y la carta
    ban_p(("sus últimas palabras son para ti", -.1), ("gracias, mi adalid. Madre|fin", .4), "Sus últimas palabras",
          "Gracias, mi adalid. Madre", "adalid"),
    mg(E.linaje(raiz=("Rykard", "el rey glorioso"), hijos=(("Hombres serpiente", "una especie entera"),
                                                           ("Zorayas", "solo pide morir")),
                medio="un repulsivo ritual de parto", remate="La familia del Rey Serpiente",
                titulo="Lo que parió la blasfemia", injertos=()),
       ("Ese es el rey glorioso", .1), ("una criatura que solo pide morir|fin", 1.4),
       [("Ese es el rey glorioso", .1), ("Ese es el rey glorioso", .4), ("Ese es el rey glorioso", .7),
        "Y esa es la hija que dejó", "una criatura que solo pide morir"], "familia rey serpiente"),
    rel("te deja una carta", "carta_zorayas", "Carta de Zorayas", dur=6.0),
    ficha("te deja una carta", "Carta de Zorayas", "Deseo emprender un viaje. De ese modo, algún día, podré continuar el "
          "trabajo de mi madre. *Podré ser la orgullosa hija de Tanith de la Mansión del Volcán*. Adiós. Siempre has sido "
          "tan amable, tan inflexible... Mi adalid.", tipo="Objeto", icono="carta_zorayas",
          a=("hija de Tanith de la Mansión del Volcán|fin", 1.0)),
    ban_p(("Hasta en su mejor final", -.1), ("la casa de las cámaras de tortura|fin", .6), "Su mejor final",
          "Heredar las cámaras de tortura", "mejor final"),
    puesto("Esa es la familia del Rey Serpiente", "Esa es", "La familia del Rey Serpiente", dur=3.6),
    rel("Y la Ira de Gelmir, el hechizo", "ira_gelmir", "Ira de Gelmir", dur=11.0),
    cam("el hechizo que te regala Bernahl", "bernahl", "Bernahl", dur=3.4, x=.56, y=.70, foco=(.5, .3, 1.4)),
    ficha("Y la Ira de Gelmir, el hechizo", "Ira de Gelmir", "Este hechizo se lanza en representación de la furia del "
          "volcán, pero *la arrogancia de intentar dominarlo es propio únicamente de hombres y víboras*.", tipo="Hechizo",
          icono="ira_gelmir", a=("únicamente de hombres y víboras|fin", 1.0)),

    # ================================================================ COMENTARIOS Y CAMPAÑA
    puesto("Antes del número uno, varios comentarios", "Antes del número uno", "Varios comentarios", dur=3.0),
    com("Andrés escribió que Miquella", C_ANDRES, dur=8.0),
    cam("ese es el encanto de Miquella", "miquella", "Miquella", dur=3.6, x=.84, y=.40, foco=(.5, .3, 1.5)),
    grande("A Rykard, por lo menos", "rykard", "Rykard", lado="izq", dur=5.6, tam=560, y=.46, marco="museo"),
    com("Otro nos conoció con el video de Morgott", C_D424, dur=5.4),
    com("Evil Ryu dice que este fue", C_EVILRYU, dur=6.6, x=.72, y=.62),
    com("Y Kanintor encontró el canal", C_KANINTOR, dur=6.0),
    com("Y Wsefsd celebró", C_WSEFSD, dur=6.0, x=.72, y=.36),
    msg(["eeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"], ("más larga que cualquier mensaje", -.1),
        ("del suelo de las Tierras Intermedias|fin", 1.0), ["más larga que cualquier mensaje"], "eeee", y=.78),
    ban_p(("ya somos más de mil doscientos", -.1), ("Gracias de corazón|fin", .2), "Runa Caída",
          "Más de 1 200 suscriptores", "mil doscientos"),
    mg(E.cien("De cada 100 que ven Runa Caída", 7, remate=("Solo 7 están suscritos", 1)), ("Aun así, de cada cien", -.2),
       ("solo siete están suscritos|fin", .4), ["de cada cien que ven", "solo siete están suscritos"], "cien", y=.44),
    puesto("El siguiente objetivo son dos mil", "Siguiente objetivo", "2 000 suscriptores", dur=2.6),
    mg(E.acuerdo(["Una familia"], "Que te devore una serpiente", letra="Aquí solo es un botón", titulo="Dos ofertas",
                 remate="Suscríbete", cab=("Rykard te da", "Tú pones")),
       ("Rykard te ofrecía una familia", -.2), ("Aquí solo es un botón|fin", .6),
       ["Rykard te ofrecía una familia", "a cambio de que te devorara", ("Aquí solo es un botón", -.3),
        ("Aquí solo es un botón", .3)], "oferta"),
    msg(["Intenta suscribirte."], ("Aquí solo es un botón|fin", .7), ("se leen, uno por uno|fin", .2),
        [("Aquí solo es un botón|fin", .8)], "suscribete"),
    puesto("con ellos se decide lo que viene", "Los comentarios", "Deciden lo que viene", dur=3.0),

    # ================================================================ 1 · LA PROPINA DE LA NOCHE DEL COMPLOT
    puesto("Número uno#3", "Atrocidad número 1", "La propina de la noche del complot", dur=3.0),
    expe(4, "La propina de la noche del complot", dur=1.6),
    ban_p(("Esta la hizo para conseguirlo", -.1), ("Esta la hizo para conseguirlo|fin", .4), "Esta la hizo",
          "Para conseguir el poder", "conseguirlo"),
    puesto("Y tú la llevaste en el inventario", "Y tú", "La llevaste en el inventario", dur=3.2),
    mapa("mundo", [pto(M_MANSION, "Mansión del Volcán", None, "inicio"),
                   pto(M_FARUM, "Farum Azula", _foto("p:farum_wiki", "farum_azula"), "meta")],
         ("Al final del juego, en Farum Azula", -.3), ("el recusante de la Mansión del Volcán|fin", .6),
         [("Al final del juego, en Farum Azula", -.2), "la ciudad en ruinas, te invade"], titulo="Farum Azula",
         sub="La ciudad en ruinas", entrada="desenrolla", traza=99, viajeros=[_G("bernahl")]),
    rel("suelta una losa con una garra grabada", "garra_blasfema", "Garra blasfema", dur=5.6),
    pant("garra_maliketh", ("el combate contra Maliketh", -.3), ("desviar el poder de su espada|fin", .6),
         zoom=(1.45, 1.52), pan=(.3, -1, .35, -1)),        # recorta «Maliketh, the Black Blade» y los rótulos del HUD
    cam("el combate contra Maliketh, la Hoja", "maliketh", "Maliketh", dur=3.4, x=.84, y=.40, foco=(.5, .4, 1.3)),
    puesto("Lo que casi nadie leyó", "Lo que casi nadie leyó", "De dónde sale", dur=3.0),
    ficha("Una losa grabada con los restos", "Garra blasfema", "Una losa grabada con los restos de la Runa de la Muerte. "
          "Puede desviar el poder de la hoja negra. *En la noche del complot, Ranni recompensó con estos restos al pretor "
          "Rykard*.", tipo="Herramienta", icono="garra_blasfema",
          a=("recompensó con estos restos al pretor Rykard|fin", .4)),
    cam("Ranni recompensó con estos", "ranni", "Ranni", dur=3.6, x=.16, y=.66, foco=(.5, .4, 1.4)),
    mg(E.recibo(concepto="la noche del complot", pagador="Ranni", cobrador="pretor Rykard",
                pago="restos de la Runa de la Muerte", sello="PAGADO", titulo="Pago en agradecimiento"),
       ("Recompensó. En japonés", -.2), ("Y qué noche era esa|fin", .8),
       [("Recompensó. En japonés", 0), "la palabra es todavía más clara", "es un pago en agradecimiento",
        ("es un pago en agradecimiento|fin", .3), "A Rykard le pagaron"], "recibo"),
    grande("Rogier te lo contó hace mucho", "rogier", "Rogier", lado="izq", dur=3.6, tam=460, y=.44),
    mg(E.muerte_suelta(["Godwyn, el Dorado"], titulo="La Runa de la Muerte", remate="La noche del complot"),
       ("Alguien robó un fragmento", -.2), ("asesinó a Godwyn, el Dorado|fin", .5),
       ["Alguien robó un fragmento", "a Maliketh, la Hoja Negra. Y una", "asesinó a Godwyn"], "runa muerte"),
    mg(E.domino(["Muere Godwyn", "La Devastación", "La guerra de su montaña", "Rykard cobró"], titulo="La primera ficha"),
       ("La muerte del primer semidiós", .2), ("es que Rykard cobró|fin", 1.4),
       [("La muerte del primer semidiós", .3), "La chispa que acabó", "la de su propia montaña", "es que Rykard cobró"],
       "chispa"),

    # ---- 1b · para qué quería el pago
    mg(E.balanza("Lo que hizo", "Lo que dice el juego", [("i", "¿Un cuchillo?"), ("i", "¿Una puerta?"),
                                                         ("i", "¿Mirar a otro lado?"), ("d", "Le pagaron"),
                                                         ("d", "Y aceptó")],
                 remate="Cobró. Eso sí se sabe", titulo="La noche del complot"),
       ("El juego no dice qué hizo Rykard", -.2), ("Y que aceptó|fin", 1.8),
       ["si sujetó un cuchillo", "si abrió una puerta", "o si solo miró hacia otro lado", "Dice que le pagaron",
        "Y que aceptó", ("Y que aceptó|fin", .5)], "balanza"),
    rel("La garra termina así", "garra_blasfema", "Garra blasfema", dur=13.0),
    ficha("La garra termina así", "Garra blasfema", "[…] En la noche del complot, Ranni recompensó con estos restos al pretor "
          "Rykard. *Si algún día se revela el allanamiento, servirán como último recurso y permitirán a Rykard desafiar a "
          "Maliketh, la Hoja Negra*, la oscura bestia de la Muerte Escrita.", tipo="Herramienta", icono="garra_blasfema",
          a=("la oscura bestia de la Muerte Escrita|fin", .8), y=.35),
    ban_p(("En japonés no dice allanamiento", -.1), ("Dice el día de la blasfemia|fin", .4), "En japonés",
          "El día de la blasfemia", "dia blasfemia"),
    mg(E.triada([("Juez", "castigaba a los demás"), ("Complot", "murió un dios"),
                 ("Blasfemo", "ya planeaba la suya")], titulo="El juez del Árbol Áureo"),
       ("El juez del Árbol Áureo", .1), ("ya planeaba su propia blasfemia la noche|fin", 1.6),
       [("El juez del Árbol Áureo", .2), "el que tenía inquisidores", "ya planeaba su propia blasfemia"], "juez blasfemo"),
    puesto("Por eso quería esa losa", "Por eso quería esa losa", "Para pelearle a la Muerte", dur=3.6),
    cam("el día en que la Muerte viniera", "maliketh", "La Muerte", dur=3.4, x=.84, y=.40, foco=(.5, .4, 1.3)),
    ban("El mismo hombre que luego se hizo serpiente", _G("serpiente_jefe"), "Serpiente devoradioses",
        "devorar, crecer, vivir", foco=(.5, .5, 1.2), dur=5.0, y=.24),
    rel("El Recuerdo del blasfemo lo resume", "recuerdo_blasfemo", "Recuerdo del blasfemo", dur=13.0),
    ficha("El Recuerdo del blasfemo lo resume", "Recuerdo del blasfemo", "Rykard se transformó en una serpiente gigante capaz "
          "de devorar a sus presas para seguir creciendo y vivir eternamente. *Lo entiendo. El camino de la blasfemia es "
          "largo y peligroso, por lo que no es posible recorrerlo si no se está listo para pecar*.", tipo="Recuerdo",
          icono="recuerdo_blasfemo", a=("si no se está listo para pecar|fin", .8), y=.35),
    puesto("Rykard estaba listo desde la noche", "Rykard estaba listo", "Desde la noche del complot", dur=3.6),
    grande("Bernahl, que cargaba la garra", "bernahl", "Bernahl", lado="izq", dur=5.4, tam=480, y=.42),
    ban_p(("que los fuertes toman", -.1), ("en su propia carne|fin", 1.0), "Según Bernahl",
          "Estaba listo para un final miserable", "final miserable"),
    ban("la serpiente con la cara del pretor", _G("rykard"), "Rykard", "no pide perdón", foco=(.5, .45, 1.4), dur=6.0,
        y=.20),
    ban_p(("una serpiente nunca muere. Escúchalo|fin", .1), ("una serpiente nunca muere. Escúchalo|fin", 9.9),
          "Nadie me tendrá cautivo", "Una serpiente nunca muere", "pista serpiente"),

    # ---- 1c · su seguro contra la Muerte; Bnet
    puesto("Nunca muere, dice", "Nunca muere", "Dice", dur=2.0),
    ban_p(("Y su seguro contra la Muerte", -.1), ("contra la Muerte en persona|fin", 1.0), "Su seguro contra la Muerte",
          "Terminó en tu bolsillo", "seguro"),
    cam("y tú lo usaste contra la Muerte", "maliketh", "Maliketh", dur=3.4, x=.84, y=.40, foco=(.5, .4, 1.3)),
    grande("Parches lo resume mejor que nadie", "parches", "Parches", lado="der", dur=5.0, tam=500, y=.42),
    cam("que Tanith ha perdido la cabeza", "tanith", "Tanith", dur=3.4, x=.16, y=.40, foco=(.5, .3, 1.6)),
    ban_p(("si papá ambición andaba", -.1), ("de la señora blasfemia|fin", 1.2), "Papá ambición",
          "Enamorado de la señora blasfemia", "papa ambicion"),
    puesto("Y aquí va el último comentario", "El último comentario", "De hoy", dur=2.4),
    com("Bnet nos escribió", C_BNET, dur=7.0),
    mg(E.audiencia(campeones=("Narrador", "Narrador", "Narrador"), tu="El siguiente", sub_tu="narrador",
                   remate="Ninguno volvió para grabar", titulo="Narradores de carne y hueso"),
       ("Pero cada vez que mandábamos", -.2), ("para grabar el cierre|fin", 1.4),
       ["Pero cada vez que mandábamos", "a un narrador de carne y hueso", "Tanith le ofrecía una audiencia",
        "Y ninguno volvió para grabar"], "narradores"),

    # ================================================================ CIERRE
    mg(E.estandartes(["Nobles en secreto", "Secuestros", "Su guerra", "Una especie", "Un pago por Godwyn"],
                     remate="Todo, firmado por el pretor", titulo="La lista de Rykard"),
       ("Esa es la lista", -.2), ("en que murió Godwyn|fin", 1.0),
       ["Un juez con un candelabro", "Máquinas que te secuestran", "Una guerra espantosa que abandonó",
        "Una especie entera nacida", "Y un pago por la noche", ("en que murió Godwyn|fin", .2)], "lista"),
    grande("Y Tanith, cuando lo matas", "tanith_npc", "Tanith", lado="izq", dur=5.0, tam=500, y=.42),
    ban_p(("que su señor aún era débil", -.1), ("que algún día volverá, más fuerte|fin", 1.0), "Según Tanith",
          "Es inmortal y volverá más fuerte", "volvera"),
    cam("Bernahl te deja otro recuerdo", "bernahl", "Bernahl", dur=2.4, x=.84, y=.72, foco=(.5, .3, 1.4)),
    rel("el Cetro de devorador, con forma", "cetro_devorador", "Cetro de devorador", dur=13.0),
    ficha("el Cetro de devorador, con forma", "Cetro de devorador", "Cetro con forma de serpiente devorando el mundo. Esta "
          "arma se convertirá, algún día, en el símbolo del señor de la Blasfemia. […] *Dicen que su diseño es una breve "
          "visión del futuro que tuvo Rykard en sus últimos momentos de vida, tras ser devorado por la gran serpiente*.",
          tipo="Sello sagrado", icono="cetro_devorador", a=("tras ser devorado por la gran serpiente|fin", .6), y=.35),
    cam("Una serpiente que se come el mundo", "serpiente_jefe", "Devorando el mundo", dur=3.2, x=.84, y=.40,
        foco=(.5, .45, 1.3)),
    puesto("Eso fue lo último que vio", "Lo último que vio", "Y le pareció bien", dur=4.0),
    mg(E.linaje(raiz=("Rennala y Radagon", "la reina y su consorte"),
                hijos=(("Ranni", "contada"), ("Radahn", "contado"), ("Rykard", "hoy")),
                medio="los hijos de la reina", remate="La trilogía, completa", titulo="Los hijos de Rennala",
                injertos=()),
       ("Con este, Zohar", -.2), ("Ranni, Radahn y Rykard|fin", 1.2),
       [("Con este, Zohar", 0), ("Con este, Zohar", .4), "Ranni, Radahn y Rykard", "Radahn y Rykard",
        ("Ranni, Radahn y Rykard|fin", -.4), ("Ranni, Radahn y Rykard|fin", 0)], "hijos de rennala 2"),
    aba([("rennala", "Rennala"), ("zampaheces", "Zampaheces"), ("gideon", "Gideon"), ("messmer", "Messmer"),
         ("bayle", "Bayle")],                                   # hoja final: la voz nombra a Bayle y no salía
        ("ya está apuntada la madre", .1), ("Dinos cuál quieres que sea el siguiente|fin", .8),
        [("ya está apuntada la madre", .2), "además del Zampaheces", "con Gideon, Messmer", ("con Gideon, Messmer", .6),
         ("Messmer y Bayle|fin", -.3)], "apuntados", y=.50, tam=250),
    aba([("marika", "Márika"), ("radagon", "Radagon"), ("miquella", "Miquella"), ("ranni", "Ranni")],
        ("En el canal tienes las atrocidades", -.2), ("Malenia, Ranni|fin", .3),
        ["de Márika y Radagon", ("de Márika y Radagon|fin", -.2), "de Miquella#2", "Malenia, Ranni"], "canal 1", tam=260),
    aba([("melina", "Melina"), ("radahn", "Radahn"), ("godfrey", "Godfrey")], ("Melina, Radahn", .1), ("y las tuyas|fin", .6),
        [("Melina, Radahn", .1), ("Melina, Radahn|fin", -.2), "Godrick, Godfrey"], "canal 2", tam=260),
    puesto("Suscríbete, que vamos por los dos mil", "Suscríbete", "Vamos por los 2 000", dur=3.6),
    cam("Y si te gustan los mundos", "marika", "Hasta los dioses", dur=3.4, x=.16, y=.40, foco=(.5, .4, 1.3)),
    ban_p(("Crónicas de Tamriel, nuestro canal hermano", -.3), ("Te lo dejo aquí al final|fin", 1.0), "Canal hermano",
          "Crónicas de Tamriel", "tamriel"),
    ban("Y la próxima vez que una máquina", _G("virgen_raptora"), "Virgen raptora", "piénsalo dos veces",
        foco=(.5, .45, 1.0), dur=5.4),
    rel("A lo mejor tiene una rueda de Ghiza", "rueda_ghiza", "Rueda de Ghiza", "esperándote", dur=4.6, x=.50, y=.46),
]

FX = [d for d in FX if d]
if FALTAN:
    print("efectos.py: pantallas que aún no existen (cubiertas con su alternativa):", " ".join(sorted(set(FALTAN))))
