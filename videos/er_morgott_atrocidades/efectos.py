# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Morgott QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 5-nov-2026).
Fórmula de Radahn/Melina/Malenia (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS)
con el kit de Elden Ring (nucleo/mg_er.py) y los estilos de pegatina de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS de cada personaje/objeto que nombra la voz (eldenring.fandom.com, pegatinas/), con silueta, reliquia, camafeo,
  banda, legajo y abanico repartidos (regla de oro: ≥ 1 de cada 3 no estándar).
- COMENTARIOS reales (≤ 10 días): Conker ×2 (pidió el tema), Mister Hunter y Pablo (la pronunciación corregida), Barial
  (Llama Frenética), Manuel (la crítica, con burla disfrazada) y en el cierre Pachón, Luis, Juan Camilo, El Imputable y
  Antithesis (la corrección de «sick»).
- PANTALLAS a cuadro entero (pantallas/) donde el clip no enseña lo que hace falta ver.
- FICHAS solo con citas verificadas (investigacion.md §7; ES oficial donde existe, si no traducción propia).
- MG NUEVOS de este guion (mg_er): `dos_nombres` (Margit = Morgott), `pila` (la Segunda Defensa de Leyndell, 2 apariciones),
  `subsuelo` (la ciudad dorada y las celdas de abajo; el sello), `trono_vacio` (los hermanos tachados y el muro de espinas,
  2 apariciones) y `cadena` (la Orden Dorada → Morgott). Además `balanza`, `mensaje`, `cien` y `puesto` del kit.
- MAPAS: Necrolimbo (de la primera gracia a la Puerta Tormentosa; Agualóbrega), Altus (al muro exterior y Leyndell) y el
  mundo (Leyndell ↔ Velo Tormentoso, «la otra punta del mapa»).
  python fab.py er_morgott_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_morgott_atrocidades fx         audio/fx.wav
"""
import os

import mg_er as E
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .30     # fichas: arriba a la derecha
TEMA_MAPA = "er"
TEMA = "er"

CAMARA = {}
FUNDIDO = {}

_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_G(slug), titulo, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=680):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.50, tam=tam)


def fila(en, items, y=.64, tam=340, dur=4.6):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, cid, dur=6.0, x=.30, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def sil(en, ruta, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara visible y el video corriendo detrás."""
    fn = PE.silueta(ruta, nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="silueta " + os.path.basename(ruta), ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
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


def leg(ruta, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(ruta, titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + titulo, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(ruta, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico(list(fotos), tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="abanico " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None),
             en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def msg(lineas, de, a, marcas, nombre):
    """Mensaje del suelo (texto ámbar) abajo, para citas que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=.76)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


C_CONKER1, C_CONKER2 = "Ugyh3XMSDrJ1xal_SDV4AaABAg", "UgyppalrKyGb--4l40x4AaABAg"
C_HUNTER, C_PABLO = "UgyKYa_8TTyGYI3ihYJ4AaABAg", "UgycXktJS6QoB4djdsx4AaABAg"
C_BARIAL, C_MANUEL = "UgxKnX5-jBFDVoSHpY94AaABAg", "UgxN7FsFbc-sVXXketl4AaABAg"
C_PACHON, C_LUIS, C_JUAN, C_IMPUTABLE, C_ANTI = ("Ugxez7l5kJWcSIYuErJ4AaABAg", "Ugycu-1ujfOjieSx_KN4AaABAg",
                                                 "Ugzby98xKr9km_ko2iV4AaABAg", "UgxX4yX1F1fIHZvUPtd4AaABAg",
                                                 "Ugy57OmtmXhA6zI41lh4AaABAg")
HERMANOS = ["Godrick", "Miquella y Malenia", "Radahn", "Rykard", "Ranni"]
PESOS = [("d", "Ningún texto dice que lo ordenara"), ("i", "Ninguno dice que lo impidiera"), ("i", "Era el rey"),
         ("i", "Asesinos en su propia capital")]
ESLABONES = ["Cuernos sagrados, hechos impureza", "Bebés mutilados", "La realeza, encerrada", "El grillete",
             "Vergüenza de su sangre"]

FX = [
    # ================================================================ GANCHO
    com("En el video de Radahn, Conker Lord nos dejó dos comentarios", C_CONKER1, dur=6.5),
    com("Y en el segundo, hace nada", C_CONKER2, dur=5.0, x=.68, y=.36),
    grande("Pues aquí lo tienes, Conker", "morgott_icono", "Morgott, rey de los Augurios", lado="der", dur=4.6, tam=620),
    sil("Morgott es, probablemente, el jefe más trágico", _P("morgott_render"), "Morgott", "rey de los Augurios", dur=5.2,
        lado="der", encuadre=(0, .55)),
    pant("subsuelo", ("escondido bajo la capital", -.1), ("escondido bajo la capital|fin", 1.2), zoom=(1.0, 1.08)),
    aba([(_G("godrick"), "Godrick"), (_G("malenia"), "Malenia"), (_G("radahn"), "Radahn"), (_G("ranni"), "Ranni")],
        ("cuando todos sus hermanos se fueron", -.2), ("a pelear por su cuenta|fin", 1.0),
        ["cuando todos sus hermanos", "se fueron", "a pelear", "por su cuenta"], "hermanos 1"),
    ficha("Su propio recuerdo lo dice", "Recuerdo del rey de los Augurios", "Jamás recibió ninguna muestra de afecto por ello, "
          "pero aún así, *él amó*.", tipo="Recuerdo", icono="recuerdo_morgott", a=("Simplemente amó|fin", 1.0)),
    pant("trono_trailer", ("Y media comunidad se pone triste", -.2), ("caer de rodillas en el Trono de Elden|fin", .4),
         zoom=(1.0, 1.12)),
    peg("es el primer muro de casi todos los jugadores", "margit_cara", "El primer muro", tam=420),
    mg(E.dos_nombres(), ("Antes de saber su nombre", -.2), ("que te espera en la puerta del primer castillo|fin", .6),
       ["Antes de saber su nombre"], "dos nombres 1"),
    aba([(_G("armadura_noche"), "Las armaduras"), (_P("monumento2"), "Los monumentos"), (_G("parvulo"), "Los muñecos"),
         (_G("recuerdo_morgott"), "Sus palabras")],
        ("si juntas lo que dicen de él", -.2), ("empieza a parecerse a otra cosa|fin", .6),
        ["las armaduras", "los monumentos", "los muñecos del subsuelo", "sus propias palabras"], "pistas", x=.50, y=.62),
    puesto("Así que van las cinco peores atrocidades de Morgott", "Las 5 peores atrocidades de", "Morgott", dur=4.2),
    sil("la número uno no es contra ti", _P("morgott_boca"), None, None, dur=4.0, lado="izq", encuadre=(0, .7)),
    peg("le compres un grillete a Parches", "parches", "Parches", tam=400),
    rel("fíjate bien de quién era esa cadena", "grillete_margit", "Grillete de Margit", dur=4.0),

    # ================================================================ 5 · TE CAZA DESDE EL PRIMER DÍA
    puesto("Número cinco. Te caza desde el primer día", "Atrocidad número 5", "Te caza desde el primer día"),
    mapa("limgrave", [(.63, .36, "La primera gracia", "inicio"), (.59, .31), (.56, .27),
                      (.47, .23, "Puerta Tormentosa", "Margit", _P("puerta_tormentosa")), (.43, .21),
                      (.40, .18, "Castillo de Velo Tormentoso", "meta", _P("velo_carga"))],
         ("Acabas de salir de la cueva del principio", -.3), ("y en medio del paso aparece él|fin", 1.0),
         ["Subes por la Colina Tormentosa", "cruzas la Puerta Tormentosa", "y en medio del paso aparece él"], titulo="Necrolimbo",
         sub="El primer día", traza=99),
    grande("Repugnante Sinluz", "margit_cara", "Margit, el Augurio Caído", lado="izq", dur=5.0, tam=560),
    ficha("Repugnante Sinluz", "Margit", "Repugnante Sinluz. Tú que andas tras el Círculo de Elden. Envalentonado por las llamas "
          "de la ambición. *Alguien debe extinguir tu llama*.", tipo="Lo que te dice", a=("¡Y ese será Margit, el Caído!|fin", .6)),
    cam("El castillo ni siquiera es suyo, es de Godrick", "godrick", "Godrick", dur=3.8, x=.84, y=.66),
    mg(E.puesto("Tu delito", "La ambición"), ("Te para por querer ser señor", -.1), ("Ese es tu delito|fin", .8), [],
       "delito", y=.80),
    *fila("Margit fue el segundo jefe con más intentos", [
        ("margit_render", "2.º · Margit", None),
        ("malenia", "1.º · Malenia", "Solo Malenia le ganaba")], dur=5.0, tam=360),
    msg(["Más te vale olvidar", "esa absurda ambición."], ("Si te mata, te deja un consejo", -.1),
        ("esa absurda ambición|fin", .8), ["más te vale olvidar", "esa absurda ambición"], "consejo"),
    ficha("Te recordaré, Sinluz", "Margit", "Te recordaré, Sinluz. Ardiendo con tu miserable llama. *Teme a la noche*. Las manos "
          "del Augurio Caído no tendrán piedad contigo.", tipo="Cuando lo vences", a=("no tendrán piedad contigo|fin", .6)),
    peg("los jinetes negros que patrullan los caminos", "glaive_noche", "Guja de la Caballería nocturna", tam=420),
    rel("La Caballería nocturna", "casco_noche", "Caballería nocturna", dur=4.0, x=.80, y=.55),
    ficha("Su casco lo explica", "Yelmo de la Caballería nocturna", "La Caballería nocturna, que ahora vaga por los caminos "
          "oscuros de la noche, *antaño la dirigía el Augurio Caído*. Eran la muerte de grandes guerreros, caballeros y campeones.",
          tipo="Casco", icono="casco_noche", a=("caballeros y campeones|fin", .8)),
    rel("Y su armadura añade un detalle", "armadura_noche", "Armadura de la Caballería nocturna", dur=4.6, x=.24, y=.52),
    ficha("negra como la brea", "Armadura de la Caballería nocturna", "Negra como la brea, con una fina capa de *sangre seca*.",
          tipo="Armadura", icono="armadura_noche", a=("lo dirigía Margit|fin", .6)),
    cam("lo dirigía Margit", "margit_cara", "Margit", dur=3.4, x=.16, y=.66),

    # ---- 5b · el segundo encuentro
    mapa("altus", [(.30, .66, "Meseta de Altus", "llegas"), (.42, .58), (.52, .55),
                   (.62, .50, "Muro exterior", "Margit otra vez", _P("gracia_muro")), (.72, .56),
                   (.82, .62, "Leyndell", "su capital", _P("leyndell"))],
         ("Cuando por fin llegas a la Meseta de Altus", -.3), ("antes de que llame a la puerta|fin", .4),
         ["a las afueras de la capital", "vuelve a salirte al paso", "Es el señor de una capital saliendo de su ciudad"],
         titulo="Meseta de Altus", sub="Te sale al paso otra vez", traza=99),
    ficha("Te encontré, Sinluz", "Margit · en Altus", "Te encontré, Sinluz. *Todavía ardiendo con esa miserable llama de "
          "ambición*.", tipo="Lo que te dice", dur=6.0),
    pant("monumento2", ("Ese encuentro es junto a un monumento", -.2), ("que es la número cuatro|fin", .4), zoom=(1.0, 1.10)),
    mg(E.dos_nombres(), ("Si consigues llegar al trono", -.2), ("Porque nunca fue un guardia. Era él|fin", 1.4),
       ["Si consigues llegar al trono", "y matar a Morgott antes que a Margit", "Era él"], "dos nombres 2"),
    ficha("La Capa del Augurio Caído lo confirma", "Capa del Augurio Caído", "Capa de pelo raído que *llevaba Margit* sobre el "
          "cuerpo.", tipo="Armadura", icono="capa_augurio", a=("la capa de pelo raído que llevaba Margit sobre el cuerpo|fin", .4)),
    cam("solo te la vende Enia", "enia", "Enia", dur=3.8),
    ficha("Y si juegas en japonés", "Margit y Morgott · en japonés", "Cuando te matan, los dos dicen la misma frase: *«más te "
          "vale olvidar tu absurda ambición»*.", tipo="Al morir", a=("olvidar tu absurda ambición|fin", .6)),
    *fila("las dobla el mismo actor", [
        ("margit_cara", "Margit", None),
        ("morgott_icono", "Morgott", "el último rey de las Tierras Intermedias")], dur=4.6, tam=360),
    mapa("mundo", [(.44, .37, "Leyndell", "el rey", _P("leyndell")), (.42, .46), (.37, .57),
                   (.34, .70, "Castillo de Velo Tormentoso", "el portero", _P("velo_carga"))],
         ("haciendo de portero en la otra punta del mapa", -.6), ("haciendo de portero en la otra punta del mapa|fin", 2.2),
         ["en la otra punta del mapa"], titulo="Las Tierras Intermedias", sub="De rey a portero", ventana=True, traza=99),
    peg("el rey de Leyndell ya te está esperando", "morgott_icono", "El rey de Leyndell", tam=380, x=.80, y=.62),

    # ================================================================ 4 · APILA LOS CADÁVERES DE LOS HÉROES
    puesto("Número cuatro. Apila los cadáveres", "Atrocidad número 4", "Apila a los héroes"),
    pant("morgott_radahn", ("La introducción del juego lo enseña", -.2), ("peleando contra Radahn|fin", .6), zoom=(1.0, 1.12)),
    grande("Sí, el mismo Radahn del video anterior", "radahn", "Radahn", lado="der", dur=4.4, tam=600),
    ficha("Su texto dice esto", "Monumento · Segunda Defensa de Leyndell", "La Segunda Defensa de Leyndell: el Augurio Caído "
          "*apila los cadáveres de los héroes*. Pero el Árbol Áureo se mantiene inquebrantable.", tipo="Monumento",
          a=("se mantiene inquebrantable|fin", .4)),
    mg(E.pila(["Los que sitiaron la capital", "Los campeones", "Los héroes"]), ("No dice que salvó la ciudad", -.2),
       ("para celebrarlo|fin", .9), ["No dice que salvó la ciudad", "Dice que apiló cadáveres", "De héroes",
                                     "Y lo dice el monumento"], "pila 1"),
    pant("afueras", ("Mira alrededor de ese monumento", -.2), ("tal como él lo dejó|fin", .3), zoom=(1.0, 1.10)),
    peg("algunos del Castillo de Velo Tormentoso", "godrick", "Godrick", tam=380, x=.80, y=.62),
    leg(_G("kenneth"), "Kenneth Haight", ["Noble de Necrolimbo.", "Godrick huyó de la capital", "escondido entre las mujeres."],
        ("Y Kenneth Haight, el noble de Necrolimbo", -.2), ("escondido entre las mujeres|fin", 1.6),
        ["el noble de Necrolimbo", "Godrick huyó", "escondido entre las mujeres"], sello=("¿Quién lo echó?", 2)),
    cam("Pero ya sabes quién guardaba la puerta", "margit_cara", "Margit", dur=3.6, x=.80, y=.66),
    ficha("Y la capa de Margit lo cuenta", "Capa del Augurio Caído", "Tras masacrar a incontables campeones durante la "
          "Devastación, el Augurio Caído se ha convertido en *el horror de quienes ambicionan el Árbol Áureo o el señorío*.",
          tipo="Armadura", icono="capa_augurio", a=("o el señorío|fin", .8)),
    ficha("En japonés es aún más fuerte", "Capa del Augurio Caído · en japonés", "*La pesadilla* de todos los que desafían al "
          "Árbol con ambición de rey.", tipo="Armadura", icono="capa_augurio", a=("Durante toda la guerra|fin", .6)),

    # ---- 4b · quiénes eran esos campeones
    aba([(_G("marika"), "Márika"), (_G("godrick"), "Godrick"), (_G("radahn"), "Radahn"), (_G("malenia"), "Malenia"),
         (_G("ranni"), "Ranni")],
        ("Cuando Márika rompió el Círculo de Elden", -.2), ("Hacia el trono|fin", .6),
        ["Cuando Márika rompió", "sus hijos se repartieron los pedazos", "de una forma u otra", "miraban hacia el Árbol",
         "Hacia el trono"], "hijos de Márika", x=.50, y=.64),
    mg(E.pila(["Sus hermanos", "Sus ejércitos", "Los Sinluz"], remate="Todo el que se acercaba con ambición",
              titulo="La pila"), ("Morgott no hizo la guerra para conquistar nada", -.2), ("acababa en la pila|fin", .9),
       ["Ni sus hermanos", "ni sus ejércitos", "ni los Sinluz", "acababa en la pila"], "pila 2"),
    ficha("Margit casi te felicita", "Margit", "Vaya, tienes cierta habilidad. *Por tus venas debe correr sangre de guerrero*, "
          "Sinluz.", tipo="Al perder la primera fase", a=("sangre de guerrero, Sinluz|fin", .6)),
    ficha("En japonés lo dice más claro todavía", "Margit · en japonés", "Así que *los Sinluz sí son descendientes de "
          "guerreros*.", tipo="Al perder la primera fase", dur=5.4),
    sil("A Godfrey. Su padre", _P("godfrey_jefe"), "Godfrey", "su padre", dur=4.6, lado="der", encuadre=(0, .7)),
    msg(["Sus ejércitos dorados, invictos y sin doblegarse,", "encuentran la gracia perdida, raída y apagada."],
        ("El monumento de Godfrey lo cuenta", -.1), ("raída y apagada|fin", .6),
        ["sus ejércitos dorados", "encuentran la gracia perdida"], "monumento Godfrey"),
    *fila("el hijo se pasa la guerra apilando héroes", [
        ("morgott_icono", "El hijo", None),
        ("godfrey", "El padre", "del ejército de su propio padre")], dur=5.4, tam=360),
    com("Mister Hunter escribió en el video de Radahn", C_HUNTER, dur=6.5),
    com("Y Pablo, que en el video de Malenia", C_PABLO, dur=6.0, x=.68, y=.34),
    cam("Hoy el examen es Morgott", "morgott_icono", "Morgott", dur=3.6, x=.16, y=.66),

    # ================================================================ 3 · EL REY DE UNA CIUDAD QUE MUTILA A LOS SUYOS
    puesto("Número tres. El rey de una ciudad", "Atrocidad número 3", "Mutila a los suyos"),
    pant("subsuelo", ("el Subsuelo de los marginados", -.3), ("el Subsuelo de los marginados|fin", 2.0), zoom=(1.0, 1.10)),
    grande("Gente nacida con cuernos, como él", "augurio_machete", "Augurios", lado="izq", dur=4.4, tam=560),
    rel("el Párvulo maldito, un muñequito", "parvulo", "Párvulo maldito", dur=4.6),
    ficha("Su descripción es de las más duras", "Párvulo maldito", "A los bebés augurio les extirpan todos los cuernos, *y la "
          "mayoría muere*. Estos fetiches se hacen para recordarlos.", tipo="Objeto", icono="parvulo",
          a=("se hacen para recordarlos|fin", .8)),
    msg(["Por favor, no me odies", "ni me maldigas. Por favor."], ("Y el muñeco lleva una frase escrita", -.1),
        ("ni me maldigas. Por favor|fin", 1.0), ["no me odies", "ni me maldigas"], "parvulo"),
    sil("Para eso están los asesinos de augurios", _G("asesino_augurios"), "Asesino de augurios", None, dur=4.6, lado="der",
        encuadre=(0, .75)),
    cam("Los de la máscara sonriente", "mascara_sonriente", "Máscara sonriente", dur=3.6),
    rel("Fíjate de qué está hecho ese machete", "machete_asesino", "Gran machete de asesino", dur=4.6, x=.24, y=.52),
    ficha("su hoja es una hilera de cuernos", "Gran machete de asesino de augurios", "La hoja de este enorme y repugnante "
          "machete *es una hilera de cuernos de augurio amputados*.", tipo="Arma", icono="machete_asesino",
          a=("cuernos de augurio amputados|fin", .8)),
    peg("Rollo, el asesino de augurios", "rollo", "Rollo, ceniza de guerra", tam=420),
    leg(_G("rollo"), "Rollo", ["Asesino de augurios.", "Se bebió una medicina", "para librarse de las emociones."],
        ("tiene una descripción sin anestesia", -.1), ("Cazar augurios|fin", .8),
        ["se bebió una medicina", "para librarse de las emociones", "Cazar augurios"], sello=("Cazar augurios", 2), x=.78, y=.50),
    rel("les daban un machete con una maldición", "machete_augurio", "Machete de augurio", dur=4.6),
    ficha("El arma lo explica con toda la calma", "Machete de augurio", "Al entregar un arma, *hay que prepararse para "
          "quitarla*.", tipo="Arma", icono="machete_augurio", a=("hay que prepararse para quitarla|fin", 1.0)),

    # ---- 3b · ¿no lo sabía?
    pant("gracia_iglesia", ("Junto a la Iglesia inferior de la capital", -.2), ("Trabajando|fin", .6), zoom=(1.0, 1.10)),
    peg("hay un asesino de augurios. Trabajando", "asesino_augurios", "En su capital", tam=420, x=.80, y=.60),
    grande("Gideon lo llama el monarca velado", "gideon_cara", "Gideon Ofnir", lado="izq", dur=4.6, tam=540),
    ficha("Gideon lo llama el monarca velado", "Gideon", "El monarca velado, *el señor de Leyndell*.", tipo="Lo que dice",
          dur=5.0),
    mg(E.balanza("Lo permitió", "No lo sabía", PESOS, remate="¿De verdad no sabía?", titulo="¿Lo sabía?"),
       ("Ojo: ningún texto dice que Morgott lo ordenara", -.2), ("lo que pasaba debajo de su trono|fin", .8),
       ["ningún texto dice que Morgott lo ordenara", "tampoco hay uno solo que diga que lo impidió", "Era el rey",
        "lo que pasaba debajo de su trono"], "balanza"),
    rel("el Párvulo maldito de la realeza", "parvulo_realeza", "Párvulo maldito de la realeza", dur=5.0, x=.24, y=.52),
    ficha("a los bebés augurio nacidos de la realeza", "Párvulo maldito de la realeza", "A los bebés augurio nacidos de la "
          "realeza no les extirpan los cuernos. *Los guardan bajo tierra, sin que nadie lo sepa, encerrados para siempre*.",
          tipo="Objeto", icono="parvulo_realeza", a=("encerrados para siempre|fin", 1.0)),
    cam("Del príncipe con cuernos", "morgott_icono", "El príncipe con cuernos", dur=3.8, x=.80, y=.66),
    mg(E.subsuelo(), ("Y cuando salió, y llegó a gobernar la capital", -.2), ("No consta que sacara a uno solo|fin", .8),
       ["Y cuando salió", "el subsuelo siguió igual"], "subsuelo 1"),
    pant("gracia_catedral", ("En la Catedral de los Desamparados", -.2), ("detrás de un altar falso|fin", .4),
         zoom=(1.0, 1.10)),
    msg(["Sellado por Morgott,", "el agraciado."], ("hay un pasaje cerrado con este mensaje", -.1),
        ("sellado por Morgott, el agraciado|fin", 1.2), ["sellado por Morgott", "el agraciado"], "sello"),
    pant("gracia_llama", ("Detrás está la Llama Frenética", -.2), ("el fuego que lo quema todo|fin", .2), zoom=(1.0, 1.10)),
    mg(E.subsuelo(), ("Ese sello sí lo puso", -.3), ("A los de abajo los dejó donde estaban|fin", 1.0),
       ["Ese sello sí lo puso", "Ese sello sí lo puso", "Ese sello sí lo puso", "A los de abajo los dejó"], "subsuelo 2"),
    com("Por cierto, Barial nos pidió", C_BARIAL, dur=6.0),
    com("Y Manuel nos dejó esto", C_MANUEL, dur=7.5, x=.50, y=.32),
    mg(E.puesto("Gracias por lo de", "Buen video"), ("Gracias por lo de buen video, Manuel", -.1),
       ("Gracias por lo de buen video, Manuel|fin", .8), [], "gracias Manuel", y=.80),
    pant("muro_espinas", ("Hay un árbol que lleva mil años decayendo", -.2), ("y nadie le escribe|fin", .6), zoom=(1.0, 1.10)),

    # ================================================================ 2 · MATA POR UN TRONO QUE SABE VACÍO
    puesto("Número dos. Mata por un trono", "Atrocidad número 2", "Un trono vacío"),
    pant("gracia_trono", ("Cuando por fin llegas al Trono de Elden", -.2), ("ante estos tronos|fin", .4), zoom=(1.0, 1.10)),
    ficha("Morgott te recibe con un discurso", "Morgott", "Sinluz sin gracia. *¿Qué asunto te trae ante estos tronos?*",
          tipo="Lo que te dice", a=("ante estos tronos|fin", .8)),
    mg(E.trono_vacio(HERMANOS, titulo="Traidores deliberados"), ("Y empieza a nombrar a sus hermanos", -.2),
       ("Traidores deliberados, todos ellos|fin", .8),
       ["Godrick el Dorado", "Miquella y Malenia", "El general Radahn", "El pretor Rykard", "La princesa de la Luna"],
       "trono 1"),
    peg("Casi todos ya han pasado por este canal", "ranni", "Ranni", tam=400, x=.80, y=.60),
    grande("Su gemelo, Mohg", "mohg", "Mohg, el gemelo", lado="der", dur=5.0, tam=620),
    cam("Nombra a todos los traidores menos a su hermano", "mohg_icono", "Mohg", dur=3.8),
    ficha("Que lo escriban en tu patética tumba", "Morgott", "Sois todos de la misma calaña. Saqueadores. Que lo escriban en tu "
          "patética tumba: *¡derrotado por el rey Morgott! El último de todos los reyes*.", tipo="Lo que te dice",
          a=("El último de todos los reyes|fin", .8)),
    ficha("en la primera versión del juego esa frase terminaba distinto", "Morgott · versión 1.0", "Derrotado por el rey "
          "Morgott, *¡Señor del Círculo!*", tipo="Antes del parche", a=("por el último de todos los reyes|fin", .6)),
    rel("Su propio recuerdo dice que él nació", "recuerdo_morgott", "Recuerdo del rey de los Augurios", dur=5.0, x=.24, y=.52),
    ficha("Te insulta con lo que él es", "Recuerdo del rey de los Augurios", "Nació como un augurio *sin la gracia*.",
          tipo="Recuerdo", icono="recuerdo_morgott", dur=4.4),

    # ---- 2b · la silla vacía
    sil("cae de rodillas y te dice la verdad", _P("morgott_render1"), "Morgott", "vencido", dur=5.0, lado="izq",
        encuadre=(0, .62)),
    ficha("Sinluz, no eres más que un necio", "Morgott", "El Árbol Áureo rechaza a todo el que se le acerca. Estamos… todos "
          "estamos abandonados. *Nadie puede reclamar el título de Señor del Círculo*.", tipo="Al morir",
          a=("el título de Señor del Círculo|fin", .8)),
    msg(["Tus hazañas acabarán en fracaso.", "Igual que yo."], ("Y si vuelves a hablarle", -.1), ("Igual que yo|fin", 1.0),
        ["tus hazañas acabarán en fracaso", "Igual que yo"], "fracaso"),
    *fila("mientras sus jinetes cazaban campeones de noche", [
        ("casco_noche", "Sus jinetes", None),
        ("margit_cara", "El paso de Necrolimbo", "mientras te esperaba en el paso de Necrolimbo")], dur=4.6, tam=340),
    mg(E.trono_vacio(HERMANOS + ["Los Sinluz"], titulo="El trono que defendía"),
       ("La entrada del Árbol Áureo se cierra", -.6), ("se cierra con un muro de espinas|fin", 1.6),
       ["La entrada del Árbol Áureo"] * 6 + ["con un muro de espinas"], "trono 2"),
    cam("Enia, en la Mesa Redonda#2", "enia", "Enia", dur=4.0),
    ficha("te lo confirma: el Árbol te ha rechazado", "Enia", "El Árbol te ha rechazado. Tendrán que pasar *miles de lunas, si no "
          "decenas de miles*, antes de que cambie.", tipo="Lo que te dice", a=("antes de que cambie|fin", .8)),
    mg(E.pila(["Los campeones", "Los Sinluz", "Y nadie lo iba a ocupar"], remate="Un trono que nadie iba a ocupar",
              titulo="Para nada"), ("Toda la Devastación, todos los campeones", -.2), ("Ni siquiera él|fin", .8),
       ["todos los campeones de la pila", "todos los Sinluz", "murieron por intentar llegar", "Ni siquiera él"], "pila 3"),
    pant("trono_trailer", ("No defendía el trono de los usurpadores", -.2), ("Y la defendía matando|fin", .8),
         zoom=(1.0, 1.16)),
    mg(E.cien("De cada 100 que ven el canal", 3, remate=("menos de 4 están suscritos", 1)),
       ("De cada cien personas que ven este canal", -.3), ("menos de cuatro están suscritas|fin", 1.8),
       ["De cada cien personas", "menos de cuatro están suscritas"], "cien"),
    mg(E.puesto("Rumbo a los mil", "456 → 500 → 1 000"), ("Estamos a nada de los quinientos", -.1),
       ("la meta grande es mil|fin", 1.0), [], "meta", y=.80),
    rel("Solo pulsar un botón", "runa_morgott", "Gran Runa de Morgott", dur=3.8),

    # ================================================================ 1 · EL MÁS LEAL
    puesto("Número uno. El más leal", "Atrocidad número 1", "El más leal"),
    mapa("limgrave", [(.71, .22, "Cueva de Agualóbrega", "Parches", _P("agualobrega")), (.62, .24), (.54, .23),
                      (.47, .23, "Puerta Tormentosa", "Margit", _P("puerta_tormentosa"))],
         ("en la Cueva de Agualóbrega hay un comerciante", -.4), ("Parches, el estafador de siempre|fin", .6),
         ["en la Cueva de Agualóbrega", "Parches#2"], titulo="Necrolimbo", sub="Una ayuda para Margit", ventana=True, traza=99),
    grande("Parches, el estafador de siempre", "parches", "Parches", lado="izq", dur=4.4, tam=520),
    rel("el Grillete de Margit", "grillete_margit", "Grillete de Margit", dur=4.6),
    peg("Lo usas en la pelea y Margit cae al suelo", "sigilo_grillete", "El sello del grillete", tam=380),
    ficha("Un fetiche bañado en magia dorada", "Grillete de Margit", "Los grilletes se usaban para atar al pueblo maldito al que "
          "llaman augurios. *Estos se hicieron para mantener a un augurio concreto bajo el más estricto encierro*.",
          tipo="Herramienta", icono="grillete_margit", a=("bajo el más estricto encierro|fin", .6)),
    ficha("Aunque débiles, todavía conservan algo de poder", "Grillete de Margit", "Aunque débiles, todavía conservan algo de "
          "poder: lo bastante para atrapar en la tierra *a Margit, que una vez estuvo encadenado*.", tipo="Herramienta",
          icono="grillete_margit", a=("que una vez estuvo encadenado|fin", 1.0)),
    *fila("Y hay otro igual, el Grillete de Mohg", [
        ("grillete_margit", "Para Margit", None),
        ("grillete_mohg", "Para Mohg", "hecho para su gemelo")], dur=4.8, tam=340),
    rel("la Espada maldita de Morgott", "espada_maldita", "Espada maldita de Morgott", dur=4.8, x=.24, y=.52),
    ficha("Su descripción dice: la sangre maldita", "Espada maldita de Morgott", "La sangre maldita que Morgott *repudió y "
          "selló* se transformó en esta hoja.", tipo="Arma", icono="espada_maldita", a=("se transformó en esta hoja|fin", .8)),
    ficha("se le escapa esto", "Morgott · segunda fase", "Los tronos… manchados por mi maldición… *Una vergüenza que no puedo "
          "soportar*.", tipo="Lo que dice", a=("Es una vergüenza que no puedo soportar|fin", .8)),
    *fila("La Gran Runa de Mohg, en cambio", [
        ("runa_morgott", "Morgott: la encerró", None),
        ("runa_mohg", "Mohg: la abrazó", "empapada en sangre maldita")], dur=6.0, tam=360),
    ficha("está empapada en sangre maldita", "Gran Runa de Mohg", "Empapada en sangre maldita, *por el amor devoto que sentía por "
          "el fango miserable donde nació*.", tipo="Gran Runa", icono="runa_mohg", a=("El otro lo encerró en una espada|fin", .6)),

    # ---- 1b · la Orden Dorada
    *fila("La Orden Dorada. La de Márika y Radagon", [
        ("marika", "Márika", None),
        ("radagon", "Radagon", "y Radagon")], dur=4.6, tam=360),
    rel("Hay un talismán, la Pluma del Crisol", "pluma_crisol", "Pluma del Crisol", dur=5.0, x=.24, y=.52),
    ficha("los rasgos del Crisol se consideraban", "Pluma del Crisol", "Los rasgos del Crisol se consideraban en la antigüedad "
          "*una señal de lo divino*. Pero, a medida que avanzaba la civilización, se desprecian cada vez más como una impureza.",
          tipo="Talismán", icono="pluma_crisol", a=("como una impureza|fin", .8)),
    rel("Y otro muñeco, el Párvulo cornudo", "parvulo_cornudo", "Párvulo cornudo", dur=4.6),
    ficha("los cuernos enredados son un símbolo", "Párvulo cornudo", "Los cuernos enredados son *un símbolo de "
          "espiritualidad*.", tipo="Objeto", icono="parvulo_cornudo", a=("La Orden Dorada los convirtió en una condena|fin", .4)),
    mg(E.cadena(ESLABONES, remate="El mejor soldado del sistema que lo odiaba", titulo="La cadena de la Orden Dorada"),
       ("Esa Orden es la que les corta los cuernos", -.3), ("Fue el mejor soldado del sistema que lo odiaba|fin", 1.2),
       ["Esa Orden es la que", "a los bebés#3", "La que encierra a los de la realeza", "La que lo encadenó a él",
        "La que le enseñó a avergonzarse", "Fue el mejor soldado del sistema"], "cadena"),
    aba([(_G("miquella"), "Miquella"), (_G("malenia"), "Malenia"), (_G("radahn"), "Radahn"), (_G("ranni"), "Ranni")],
        ("Ninguno de sus hermanos la defendió como él", -.2), ("todos se fueron por su lado|fin", .8),
        ["los gemelos prodigio#2", "ni Radahn", "ni Ranni", "todos se fueron por su lado"], "se fueron", x=.50, y=.64),
    cam("el hijo que la familia escondió en las cloacas", "parvulo_realeza", "Escondido", dur=4.0, x=.80, y=.66),
    rel("Su recuerdo lo dice así en la versión oficial", "recuerdo_morgott", "Recuerdo del rey de los Augurios", dur=6.0,
        x=.24, y=.52),
    ficha("Su recuerdo lo dice así en la versión oficial", "Recuerdo del rey de los Augurios", "Pese a haber nacido como un "
          "augurio más sin la Gracia, Morgott decidió convertirse en el protector del Árbol Áureo. Jamás recibió ninguna muestra "
          "de afecto por ello, *pero aún así, él amó*.", tipo="Recuerdo", icono="recuerdo_morgott", a=("pero aun así, él amó|fin", 1.2)),
    pant("ceniza", ("con la capital hecha ceniza", -.3), ("Es Godfrey|fin", .3), zoom=(1.0, 1.10)),
    pant("godfrey_llora", ("Y le habla por su nombre", -.2), ("Larga y dura fue tu lucha|fin", 1.0), zoom=(1.0, 1.14)),
    msg(["Ha pasado mucho tiempo, Morgott.", "Larga y dura fue tu lucha."], ("Ha pasado mucho tiempo, Morgott", -.1),
        ("Larga y dura fue tu lucha|fin", 1.0), ["Ha pasado mucho tiempo", "Larga y dura fue tu lucha"], "Godfrey"),
    ban(("Su padre. El que se fue al exilio", -.1), _P("godfrey_llora2"), "Godfrey", "su padre", foco=(.5, .4, 1.6), dur=4.6),
    pant("godfrey_jefe", ("Y luego se levanta, y viene a por ti", -.2), ("Y luego se levanta, y viene a por ti|fin", 1.0),
         zoom=(1.0, 1.12)),

    # ================================================================ CIERRE
    aba([(_G("margit_cara"), "Te caza"), (_G("casco_noche"), "Sus jinetes"), (_P("monumento2"), "La pila"),
         (_G("parvulo"), "La ciudad"), (_P("muro_espinas"), "El trono vacío"), (_G("grillete_margit"), "La cadena")],
        ("Esa es la lista", -.2), ("al sistema que lo encadenó|fin", .8),
        ["El viejo del primer castillo", "dirigía a los jinetes", "apiló héroes en las murallas", "reinó sobre una ciudad",
         "mató durante toda una guerra", "defendió hasta la muerte"], "lista", x=.50, y=.62, tam=270),
    cam("de todos los hijos de Márika", "marika", "Márika", dur=4.6, x=.80, y=.66),
    com("Pachón dijo", C_PACHON, dur=5.0),
    com("Luis nos contó", C_LUIS, dur=5.4, x=.68, y=.36),
    com("Juan Camilo nos pidió", C_JUAN, dur=4.6),
    com("Y El Imputable lo resumió", C_IMPUTABLE, dur=4.6, x=.68, y=.36),
    com("Y Antithesis nos corrigió algo", C_ANTI, dur=8.0, x=.50, y=.32),
    peg("Cuando Blaidd dice en inglés", "blaidd", "Blaidd", tam=380, x=.16, y=.70),
    *fila("Por eso Cristian ya tiene a Rennala apuntada", [
        ("rennala", "Rennala", None),
        ("godfrey", "Godfrey", "y John, a Godfrey"),
        ("godwyn_peg", "Godwyn", "y a Godwyn")], dur=5.0, tam=330),
    msg(["¿Héroe trágico,", "o el carcelero más fiel de su madre?"], ("¿Morgott fue un héroe trágico", -.1),
        ("el carcelero más fiel de su madre|fin", 1.0), ["héroe trágico", "el carcelero más fiel"], "pregunta"),
    cam("Y Conker, espero que siga siendo tu favorito", "morgott_icono", "Para Conker", dur=3.8, x=.80, y=.66),
    aba([(_G("marika"), "Márika y Radagon"), (_G("miquella"), "Miquella"), (_G("malenia"), "Malenia"), (_G("ranni"), "Ranni"),
         (_G("melina"), "Melina"), (_G("radahn"), "Radahn")],
        ("en el canal tienes las atrocidades de Márika", -.2), ("y de Radahn|fin", .8),
        ["de Márika y Radagon#2", "de Miquella#2", "de Malenia#3", "de Ranni#2", "de Melina", "y de Radahn"], "en el canal",
        x=.50, y=.62, tam=270),
    mg(E.puesto("Suscríbete", "Rumbo a los 500"), ("Y si te suscribes", -.1), ("nos acercas a los quinientos|fin", .8), [],
       "suscribete", y=.80),
    rel("acuérdate: antes de servirte a ti", "grillete_margit", "Grillete de Margit", dur=4.4, x=.24, y=.52),
    sil("Morgott, el rey de los augurios#2", _P("morgott_render"), "Morgott", "rey de los Augurios", dur=4.8, lado="der",
        encuadre=(0, .55)),
]
