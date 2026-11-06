# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 10 JEFES de Banjo-Tooie, del PEOR al MEJOR» (SECUENCIA YT, Crónicas del gaming, 5-nov-2026).
Plantilla: videos/bt_50_secretos/efectos.py (mismos helpers) + catálogo de animaciones de pegatina (`pv/filav/pil`, nucleo/peg_anim.py).
- Cada puesto: `escalera` (el ranking que crece, con los retratos de peor a mejor) + rótulo de PUESTO con el Jiggy real (~4 s)
  + `vida_jefe` al decir su vida (las celdas caen en las frases de combate) + `mira` sobre el punto débil + `cuatro_listas` en el
  «¿por qué…?» de 5 puestos (notas reales de investigacion_jefes.md § 1).
- MG nuevos de ESTE guion en mg_banjo: vida_jefe, escalera, mira, despiece (Old King Coal pierde trozos), pociones (Klungo),
  pedido (pizza de 12 pies), funden (dos mundos -> dos dragones), fases (las 10 de la Hag 1), luna (broma de Majora).
- MAPAS REALES de la Guía oficial de Nintendo (mapas/_coordenadas.md + rejillas medidas el 5-nov): GGM, MT, JRL, HFP lava y hielo,
  WW, CCL (las dos calaveras de Mumbo), GI. TDL e isla: sin punto seguro, sin mapa.
- Comentarios reales (≤ 10 días): 4 agradecimientos + la crítica de JaVik0 con burla disfrazada (luna y reloj de 3 días).
- SFX DEL JUEGO (regla del 29-oct): sfx/bt_*.mp3.
  python fab.py bt_jefes_ranking fx --seco | fx hoja | fx
"""
import os

import mg_banjo as B
import mg_mapa as MP
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .42     # fichas: a la derecha
TEMA = "gaming"
TEMA_PEG = "gaming"
JIGGY = os.path.join(_PEG, "jiggy.png")

CAMARA = {}
FUNDIDO = {}


def P(slug):
    for e in (".png", ".jpg"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    raise FileNotFoundError(slug)


# ------------------------------------------------------------------ pegatinas (estilos variados)
def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-6.0):
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam, giro), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def pv(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, **anim):
    """Pegatina con animación variada (marco + entrada + estancia + salida del rotador del video)."""
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    """Pila de fotos que se reparte (una por marca de la voz); fotos = [(slug, etiqueta)]."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(P(s), e) for s, e in fotos], tam, TEMA_PEG, marco), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=620):
    return pv(en, slug, titulo, dur=dur, x=.27 if lado == "izq" else .73, y=.53, tam=tam)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=800, encuadre=(0, 1.0)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con el video corriendo detrás."""
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.6, x=.26, y=.54, tam=540):
    """Objeto sobre el círculo."""
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .45, 1.4), dur=4.5, y=.72, lado="der"):
    """Tira de cine a todo lo ancho."""
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.14, y=.68, tam=290, foco=(.5, .3, 1.3)):
    """Medallón para menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.22, y=.54, ancho=480, giro=3.5):
    """Expediente con retrato; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.62, tam=290):
    """Cartas en abanico cuando la voz enumera. fotos = [(slug, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def com(en, cid, dur=7.0, x=.30, y=.30):
    """Captura del comentario REAL (yt comentario)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760, giro=-2.0)


# ------------------------------------------------------------------ fichas y MG
def ficha(en, titulo, texto, sub=None, dur=5.5, a=None, x=_FX, y=_FY, ancho=820):
    d = dict(tipo="mg", fn=B.ficha(titulo, texto, sub, ancho=ancho), en=en, x=x, y=y, sale=.35, nombre="ficha " + titulo, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def xbox(en, dur=5.0):
    return dict(tipo="mg", fn=B.ficha("Xbox 360", "Versión de 2009", ancho=430), en=en, dur=dur, x=.86, y=.24, sale=.3,
                nombre="rótulo Xbox", ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def vs(de, a, marcas, izq, der, titulo=None, marca="CAMBIÓ", y=.54):
    """versus: izq/der = (etiqueta, texto, slug o None)."""
    def col(c):
        return dict(etiqueta=c[0], texto=c[1], icono=P(c[2]) if len(c) > 2 and c[2] else None)
    return mg(B.versus(col(izq), col(der), titulo, marca), de, a, marcas, "versus " + (titulo or izq[0]), y=y)


def cad(de, a, marcas, titulo, pasos, final, y=.55):
    """cadena: pasos = [(slug o None, texto)], final = (slug o None, texto)."""
    return mg(B.cadena(titulo, [(P(s) if s else None, t) for s, t in pasos], (P(final[0]) if final[0] else None, final[1])),
              de, a, marcas, "cadena " + titulo, y=y)


def donde(en, items, dur=4.4):
    """Tira baja: items = [(slug, etiqueta, nombre)] (MUNDO / JEFE…)."""
    return dict(tipo="mg", fn=B.ficha_mundo([(P(s), e, n) for s, e, n in items]), en=(en, .5), dur=dur, x=.5, y=.86, sale=.35,
                nombre="MG dónde " + items[0][2], ver=1.3)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub="Guía oficial de Nintendo", ventana=False, x=.70, y=.44, recorte=None, **kw):
    """Mapa REAL con ruta (tema gaming). `puntos` en fracciones de la imagen ENTERA; 5.º elemento = slug de la foto."""
    ruta = os.path.join(_MAP, slug + ".jpg")
    if recorte:
        x0, y0, x1, y1 = recorte
        puntos = [((p[0] - x0) / (x1 - x0), (p[1] - y0) / (y1 - y0)) + tuple(p[2:]) for p in puntos]
    puntos = [p[:4] + ((P(p[4]) if p[4] else None),) if len(p) > 4 else p for p in puntos]
    fn = MP.mapa(ruta, puntos, "gaming", titulo=titulo, sub=sub, recorte=recorte, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


# ------------------------------------------------------------------ nuevos helpers de este guion
def vida(nombre, golpes, de, a, marcas=(), quedan=0, sub=None):
    """Barra de vida del jefe ARRIBA (como en el juego): las celdas caen en las marcas o repartidas en las frases de combate."""
    return mg(B.vida_jefe(nombre, golpes, quedan=quedan, sub=sub), de, a, marcas, "vida " + nombre, y=.17)


def mira(en, texto, x=.5, y=.52, dur=3.4):
    """Retícula de punto débil sobre el clip."""
    return dict(tipo="mg", fn=B.mira(texto), en=en, dur=dur, x=x, y=y, sale=.3, nombre="MG mira " + texto, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    """Imagen a cuadro entero con zoom/paneo lento, DEBAJO de fichas y pegatinas."""
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla " + slug, ver=2.0)


def recre(slug, de, a, titulo, texto, sub=None, marca_a=None, zoom=(1.0, 1.10), pan=(0, 0, 0, 0)):
    """LO QUE NO EXISTE (el usuario, 5-nov-2026; docs/estilo_secuencia_yt.md § «Lo que no existe»): imagen de Flow hecha con
    ingredientes REALES del juego (pegatinas/flow_<slug>, anotada en _fuentes.txt), a pantalla completa, con su ficha abajo y la
    marca chica «RECREACIÓN · Así pudo verse» arriba a la derecha: nunca se presenta como captura auténtica. `marca_a` alarga la
    marca si después sigue un MG con la misma imagen."""
    return [pant(slug, de, a, zoom=zoom, pan=pan),
            dict(tipo="mg", fn=B.ficha("RECREACIÓN", "Así pudo verse", ancho=420), de=de, a=marca_a or a, x=.85, y=.12, sale=.3,
                 nombre="marca recreación " + slug, ver=1.0),
            dict(tipo="mg", fn=B.ficha(titulo, texto, sub, ancho=900), de=(de, .4) if isinstance(de, str) else (de[0], de[1] + .4), a=a,
                 x=.5, y=.83, sale=.35, nombre="ficha recreación " + slug, ver=1.6)]


_LISTAS = ["Easy Geek", "Super Joe Bros", "Super Joe Bros (chat)", "ivanavi", "Acute-Dilute", "MABUS", "WatchMojo"]


def listas(de, a, titulo, notas, media, marcas=()):
    """Dónde pone cada una de las 7 listas a este jefe (escala 1 = peor, 10 = mejor; investigacion_jefes.md § 1). Una nota de
    None (la lista no lo puntúa) no sale. `notas` en el orden de la tabla: Easy Geek, SJB chat, SJB propia, ivanavi, Acute-Dilute,
    MABUS, WatchMojo (se reordenan a como las nombra la voz)."""
    notas = [notas[0], notas[2], notas[1]] + list(notas[3:])
    filas = [(n, [str(k) for k in range(1, 11)], int(v + .5) - 1) for n, v in zip(_LISTAS, notas) if v is not None]
    return mg(B.cuatro_listas(titulo, filas, media, ancho=1260), de, a, marcas, "listas " + titulo, y=.50)


# Ranking de consenso, del peor (10) al mejor (1).
RANKING = [("terry", "Terry"), ("old_king_coal", "Old King Coal"), ("targitzan", "Targitzan"), ("lord_woo", "Lord Woo Fak Fak"),
           ("klungo", "Klungo"), ("chilli_billi", "Chilli Billi y Chilly Willy"), ("mr_patch", "Mr. Patch"),
           ("mingy_jongo", "Mingy Jongo"), ("hag1", "Hag 1"), ("weldar", "Weldar")]
PUESTOS = {10: "Número diez", 9: "Número nueve", 8: "Número ocho", 7: "Número siete", 6: "Número seis", 5: "Número cinco",
           4: "Número cuatro", 3: "Número tres", 2: "Número dos", 1: "Número uno. Weldar"}


def _puestos():
    out = []
    for n, en in PUESTOS.items():
        k = 10 - n + 1
        nombre = RANKING[k - 1][1]
        out.append(mg(B.escalera([P(s) for s, _ in RANKING[:k]], 10), en, (en, 4.6), [], f"escalera {n}", y=.80))
        out.append(dict(tipo="mg", fn=B.puesto(n, nombre, JIGGY, etiqueta="PUESTO", max_ancho=1500), en=(en, .2), dur=4.0, x=.5, y=.19,
                        sale=.45, nombre=f"aviso puesto {n}", ver=1.4))
    return out


_MT_RUTA = [(.255, .91, "Inicio", "inicio"), (.245, .72), (.31, .50), (.385, .35), (.56, .37, "Puente", "paso"), (.66, .50), (.665, .70),
            (.56, .69), (.52, .60, "Templo de Targitzan", "meta", "templo_targitzan")]
_JRL_RUTA = [(.32, .04, "Inicio", "inicio"), (.35, .18), (.41, .30), (.50, .52, "El muelle", "paso"), (.57, .77, "Fondo del mar", "meta", "lord_woo")]
_CCL_RUTA = [(.80, .65, "Inicio", "inicio"), (.69, .61), (.63, .60), (.655, .39, "Calavera 1", "meta", "mumbo_skull"), (.45, .48),
             (.245, .53, "Calavera 2", "meta", "mumbo_skull_rojo")]   # 6-nov: las calaveras REALES de CCL (azul / roja), no la de Mayahem
_GI_RUTA = [(.235, .83, "Inicio", "inicio"), (.30, .76), (.39, .63, "Puerta", "paso"), (.47, .70), (.54, .62, "La fábrica", "meta", "weldar")]

FX = [
    # ================================================================ GANCHO (un elemento nuevo cada 2-3 s)
    pv("Tres jefes de Banjo-Tooie casi", "caja_bt", "Banjo-Tooie", dur=2.6, x=.78, y=.56, tam=460),
    # promesas.md #1-3: las tres recreaciones GRANDES (antes, iconos de 60 px en una cadena: no se distinguía la roca ni la avispa)
    pil([("flow_boss_boulder", "Una roca"), ("flow_kogs", "The Kogs"), ("flow_avispa_mushroomland", "Una avispa gigante")],
        de="Uno iba a ser una roca", a=("el tercero, una avispa gigante|fin", .6),
        marcas=["Uno iba a ser una roca", "unos engranajes llamados", "Y el tercero, una avispa"], nombre="casi no existen", x=.5, y=.56, tam=440),
    dict(tipo="mg", fn=B.ficha("RECREACIÓN", "Así pudo verse", ancho=420), de="Uno iba a ser una roca", a=("el tercero, una avispa gigante|fin", .6),
         x=.85, y=.12, sale=.3, nombre="marca recreación gancho", ver=1.0),
    sil("Hay un tótem que se autodestruye", "targitzan", "Targitzan", "Se autodestruye", lado="der", dur=3.4, alto=720),
    ficha("y sigue hablando", "Y sigue", "*hablando*", dur=2.0, x=.36, y=.26, ancho=560),
    pv("Un pez que, después de morir", "lord_woo", "Lord Woo Fak Fak", dur=3.4, x=.20, y=.62, tam=420),
    ficha("te pide que dejes de dispararle", "Después de morir", "«¡Deja de *dispararme*!»", dur=2.0, x=.72, y=.40),
    grande("Y un dragón que te confunde", "chilli_billi", "¿El de la pizza?", lado="der", dur=3.4, tam=560),
    pv("Un rey de carbón que pierde", "old_king_coal", "Old King Coal", dur=3.4, x=.20, y=.56, tam=360),
    ficha("y sigue diciendo que va ganando", "Sin brazos", "…y *va ganando*", dur=2.0, x=.72, y=.40, ancho=600),
    vs("Y un robot que se hace pasar", ("por tu mejor amigo|fin", .8), ["Y un robot que se hace", "por tu mejor amigo", ("por tu mejor amigo|fin", .2)],
       ("MUMBO", "Tu amigo", "mumbo"), ("MINGY JONGO", "Un robot", "mingy_jongo"), titulo="¿Cuál es cuál?", marca="IMPOSTOR"),
    pil([("caja_bt", "Su historia"), ("jiggy", "Jiggies crueles"), ("isla_mapa", "Ocho mundos"), ("logo_bt_jp", "50 secretos")],   # 6-nov: los 8 mundos, no solo Witchyworld
        de="Ya te contamos la historia", a=("Creías que estaba todo|fin", 0),
        marcas=["la historia de Banjo-Tooie", "sus Jiggies más crueles", "sus ocho mundos", "y cincuenta secretos"], nombre="videos anteriores"),
    mg(B.escalera([], 10), "Faltaban ellos", ("del peor al mejor|fin", 0), [], "escalera vacía", y=.50),
    ficha(("Y el número uno ni siquiera", .4), "El número 1", "*Ni siquiera* estaba en los planes de Rare", dur=4.0, x=.70, y=.40),
    cam("en los planes de Rare", "rare_hq", "Rare", x=.15, y=.66, dur=3.0),

    # ================================================================ MÉTODO
    ficha("Para que no sea solo nuestra", "El método", "*Siete* rankings, *una* media", sub="Jugadores y creadores", a=("la media de cada jefe|fin", .4)),
    pv("juntamos siete rankings", "jiggy", "7 listas", dur=3.4, x=.20, y=.62, tam=360),
    listas("Están Easy Geek", ("su nota en cada lista|fin", .3), "LA NOTA DE CADA LISTA", [3, 5, 6, 6, 6, 4, 6.6], "Ejemplo: Klungo, media 5,23",
           marcas=["Están Easy Geek", "la suya y", "la de su chat", "ivanavi", "Acute-Dilute", "MABUS y", "y WatchMojo", "Cada jefe tiene su nota"]),
    cam("Klungo, al que peleas tres", "klungo", "Klungo ×3", x=.15, y=.66, dur=3.4),
    aba([("chilli_billi", "Chilli Billi"), ("chilly_willy", "Chilly Willy")], de="Los dos dragones de Hailfire", a=("Peaks, también|fin", .6),
        marcas=["Los dos dragones", "Peaks, también"], nombre="dragones método", x=.70),
    ficha("Quedan diez", "Diez jefes", "Del *peor* al *mejor*", dur=2.2, x=.5, y=.36, ancho=640),

    # ================================================================ 10 · TERRY
    rel(("vive en un nido, en la cima", 1.2), "terry_nest", "Terry's Nest", "En la cima", dur=4.2, x=.74, y=.52, tam=500),
    pv("te recibe a escupitajos", "cap_terry_escupe", "A escupitajos", dur=3.4, x=.24, y=.60, tam=440),   # promesas.md #13
    sil("Te acusa de robarle los huevos", "terry", "Terry", "Padre Pterodáctilo Contrariado", lado="der", dur=4.2),
    ficha("le contesta que da igual", "Kazooie", "«Tu especie está a punto de *extinguirse*»", dur=4.4, x=.30, y=.44),
    vida("Terry", 10, "Tiene treinta de vida", ("y vuelta a empezar|fin", .4), sub="30 de vida"),
    mira("no apunta a donde estás", "A DONDE VAS A ESTAR", x=.52, y=.58, dur=3.2),
    ficha("Si corres en círculo", "El truco", "Corre en *círculo*", dur=3.0, x=.28, y=.55, ancho=560),
    pv("los Mucoids", "mucoid", "Mucoid", dur=2.8, x=.78, y=.62, tam=380),
    ban("Los rompes rodando", "mucoid_b", "Mucoids", "Se rompen rodando", foco=(.5, .5, 1.2), dur=3.2, y=.76, lado="izq"),
    cam("la versión japonesa", "logo_bt_jp", "Japón", x=.10, y=.19, tam=220, dur=3.0),
    vs("Por el nombre sería", ("Y Terry, sí|fin", .8), ["Por el nombre sería", "no tenían dientes", "Y Terry, sí"],
       ("PTERANODON", "Sin dientes", "pteranodon_vida"), ("TERRY", "Con dientes", "terry"), titulo="¿Pteranodon?", marca="DIENTES"),
    pant("cap_terry_cenital", "salta a una vista desde arriba", ("y te quita el control|fin", .3)),   # promesas.md #21 (Prosafia @1000)
    ficha("está el último? Porque cada", "La cámara", "Salta a una vista *desde arriba*", sub="Y te quita el control",
          a=("y te quita el control|fin", .3)),
    listas("Las listas lo repiten", ("la pelea no tanto|fin", .3), "TERRY EN LAS 7 LISTAS", [5, 1, 4, 1, 5, 2, 1.6], "Media 2,79 · el último"),
    leg("terry", "Terry", ["Fe de erratas", "Dijimos: «la jefa»", "Es macho y padre soltero"], de="Y aquí nos toca corregir",
        a=("lo dejó antes del juego|fin", .5), marcas=["Terry es macho"], sello=("CORREGIDO", 0), x=.26, y=.54),
    pv("En nuestro ranking de mundos", "titulo_tdl", "Ranking de mundos", dur=3.4, x=.76, y=.58, tam=420),
    ficha("y padre soltero", "Según la wiki", "Padre *soltero*", sub="Cita el manual", dur=3.6, x=.74, y=.36, ancho=640),
    pv("Perdón, Terry", "terry", "Perdón, Terry", dur=3.2, x=.80, y=.60, tam=380),
    mg(B.rotulos([("TERRY", "«Perdón por ser tan bruto»", "Al ver que no tenías sus huevos"), ("KAZOOIE", "«Yo lo disfruté»")]),
       "se disculpa por haber sido", ("que ella lo disfrutó|fin", 1.0), ["se disculpa por haber sido", "que ella lo disfrutó"], "rótulos Terry", y=.30),
    cam("Y Kazooie le contesta que ella", "kazooie", "Kazooie", x=.14, y=.74, dur=3.0),
    pil([("terry_baby", "Cría"), ("terry_baby2", "La más gorda")], de="que le devuelvas a sus crías", a=("en el Taxi Pack", 0),
        marcas=["que le devuelvas", "La última es tan gorda"], nombre="crías", x=.30),
    rel("en el Taxi Pack", "taxi_pack", "Taxi Pack", dur=3.6, x=.74, y=.56, tam=480),
    rel("darle con un huevo granada", "granada", "Huevo granada", dur=3.6, x=.26, y=.56, tam=460),
    ficha("Kazooie lo llama desalmado", "Terry", "«*Es broma*»", sub="Kazooie: «¡Desalmado!»", dur=4.4, x=.74, y=.42, ancho=600),
    mg(B.fechas([("Documento «Dino #21»", "20 ene 1999", P("rare_hq"))], "Documento de diseño de Rare"),
       "En el documento de diseño de Rare", ("noventa y nueve|fin", .8), ["de enero de mil"], "fecha Terry", y=.25),
    *recre("flow_terry_borde_nido", "Terry iba a dar vueltas", ("te atacaban los mocos|fin", 1.0), "El plan original",
           "Volaba *bajo el borde* del nido", sub="Mientras atacan los Mucoids"),
    vs("Y en ese primer plan", ("acabó ocupando Mayahem Temple|fin", .8), ["Terrydactyland no era", "Era el primero", "acabó ocupando Mayahem"],
       ("PRIMER PLAN", "Terrydactyland, mundo 1", "titulo_tdl"), ("EL JUEGO", "Mayahem Temple, mundo 1", "titulo_mt"), titulo="El orden de los mundos"),

    # ================================================================ 9 · OLD KING COAL
    mapa("ggm", [(.75, .15, "Estación", "meta", "chuffy")], de=("Un rey hecho de carbón", .9), a=("pelear con él|fin", .3),
         marcas=["la caldera del tren"], titulo="Glitter Gulch Mine", ventana=True),
    pv(("Un rey hecho de carbón", 1.1), "old_king_coal2", "Old King Coal", dur=3.0, x=.20, y=.54, tam=330),
    rel("del tren, Chuffy", "chuffy", "Chuffy", "El tren", dur=3.4, x=.24, y=.56, tam=460),
    ficha("la caldera te habla", "La caldera", "Primero, *pelea* con el rey", sub="Si usas el tren antes", dur=4.0, x=.27, y=.42, ancho=640),
    vida("Old King Coal", 10, "Tiene cincuenta de vida", ("le quitan más|fin", .4), quedan=3, sub="50 de vida"),
    ficha("la segunda cifra más alta", "Vida", "*50*: solo el jefe final tiene más", dur=4.0, x=.74, y=.55),
    mira("Y no tiene punto débil", "SIN PUNTO DÉBIL", x=.52, y=.56, dur=3.0),
    vs("Los huevos de fuego no", ("le quitan más|fin", .8), ["Los huevos de fuego no", "Los de hielo", "le quitan más"],
       ("FUEGO", "No le hace nada", "fire_nest"), ("HIELO", "Le quita más", "ice_nest"), titulo="Huevos contra el carbón", marca="MÁS DAÑO", y=.58),
    mg(B.despiece(P("old_king_coal"), [(.62, .28, 1, .9), (0, .28, .38, .9), (0, 0, 1, .5)],
                  ["No pasa nada, tengo otro", "No necesito brazos", "¿Y si nos sentamos a hablar?"], titulo="CÓMO PIERDE UN REY"),
       "Lo mejor es cómo pierde", ("propone sentarse a hablar|fin", 1.0), ["se le cae el brazo", "Luego el derecho", "Luego la mitad de arriba"],
       "despiece Old King Coal", y=.52),
    cad("la caldera se calienta", ("donde no te alcanza|fin", .6), ["la caldera se calienta", "el suelo se pone al rojo", "el humo te ahoga",
                                                                    "Te salvas subiéndote"],
        "LA CALDERA", [(None, "Se calienta"), (None, "Suelo al rojo"), (None, "Humo que ahoga")], ("old_king_coal2", "Súbete a sus trozos")),
    mg(B.crueldad(1, 5, "DIFICULTAD"), "es el más fácil del juego", ("no te puede tocar|fin", .6), [], "dificultad Coal", y=.24),
    pv("Subido a una plataforma", "old_king_coal", "Ni te toca", dur=3.4, x=.27, y=.62, tam=340),
    ficha("Super Joe Bros le pone", "Super Joe Bros", "Buena nota… *por el esfuerzo*", sub="«A for effort»", a=("por el esfuerzo|fin", .5),
          x=.72, y=.50),
    cam("Y casi ni existe", "rare_hq", "Rare", x=.89, y=.19, tam=220, dur=2.6),
    ficha("En la primera lista de mundos", "Primera lista de Rare", "El jefe de la *mina*…", a=("Boss Boulder", 0), x=.72, y=.42, ancho=640),
    *recre("flow_boss_boulder", "Boss Boulder", ("Boulder». Una roca|fin", 1.0), "«Boss Boulder»", "El jefe de la mina: *una roca*",
           sub="Primera lista de Rare"),
    *recre("flow_okc_formandose", "muchos trozos de carbón", ("Rare se quedó con la opción B", 0), "Opción A",
           "Trozos de carbón que se juntan *uno a uno*", sub="Su entrada", marca_a=("menos exigente para la consola|fin", .8)),
    vs("Rare se quedó con la opción B", ("menos exigente para la consola|fin", .8), ["Rare se quedó con la opción B",
                                                                                      ("Rare se quedó con la opción B", .5), "menos exigente"],
       ("OPCIÓN A", "Trozos de carbón que se juntan uno a uno", "flow_okc_formandose"), ("OPCIÓN B", "Sale del carbón de golpe", "old_king_coal2"),
       titulo="Su entrada", marca="ELEGIDA"),
    cam("menos exigente para la consola", "n64", "Nintendo 64", x=.09, y=.20, tam=220, dur=3.0),
    ficha("En alemán se llama", "En alemán", "*Briketto Blanko*", sub="Old King Coal", dur=3.8, x=.72, y=.42, ancho=640),
    cam("del cantante Roberto Blanco", "roberto_blanco", "Roberto Blanco", x=.16, y=.62, tam=300, dur=3.8, foco=(.5, .22, 1.7)),
    cam("el Caballero Negro de Monty", "old_king_coal", "Old King Coal", x=.16, y=.64, dur=4.0, tam=300),   # regla 3: nada de imágenes de película; la ficha de abajo lo cuenta
    ficha("Y la wiki lo compara", "Según la wiki", "Como el *Caballero Negro*: «solo es un rasguño»", sub="Monty Python",
          a=("solo es un rasguño|fin", .8), x=.72, y=.42),
    xbox("En Xbox 360, el logro", dur=4.4),
    ficha("el logro por vencerlo", "Logro de Xbox 360", "«*A Merry Old Soul*»", sub="Canción infantil", dur=4.4, x=.30, y=.42, ancho=700),
    pv("Su pie, en cambio", "old_king_coal2", "Su pie", dur=3.4, x=.78, y=.62, tam=400),

    # ================================================================ 8 · TARGITZAN
    mapa("mt", _MT_RUTA, de="El dios maya del tiro", a=("cubierto de dianas|fin", 1.0), marcas=["El dios maya del tiro", "un tótem que gira"],
         titulo="Mayahem Temple", ventana=True, x=.74, y=.42),   # ventana: la promesa «un tótem que gira» se ve en el clip (promesas.md #44)
    mg(B.rotulos([("TARGITZAN", "Despotic Dizzy Totem God"), ("APUNTZAN", "Despótico Dios Tótem Mareado", "En español")]),
       "La traducción al español lo", ("Tótem Mareado|fin", .5), ["La traducción al español lo", "Despótico Dios Tótem"], "rótulos Targitzan", y=.30),
    pv("de apuntar", "targitzan", "Apuntzan", dur=3.2, x=.80, y=.70, tam=360),
    cad("Para llegar a él necesitas", ("toda la pelea es en primera persona|fin", .6), ["veinte estatuas de jade", "y el Breegull Blaster",
                                                                                         "toda la pelea es"],
        "PARA LLEGAR A ÉL", [("jade_grove", "20 estatuas de jade"), ("blaster", "Breegull Blaster")], ("targitzan", "Todo en primera persona")),
    vida("Targitzan", 16, "Tiene dieciséis de vida", ("explota durante tres segundos|fin", .4), sub="4 pisos × 4 dianas"),
    mira("cuatro dianas cada uno", "16 DIANAS", x=.52, y=.56, dur=3.2),
    pv("suelta más Moggies", "moggy", "Moggies", dur=3.4, x=.20, y=.64, tam=380),
    ficha("le salen más caras", "Cada piso roto", "Más caras que *escupen dardos*", dur=4.0, x=.74, y=.55, ancho=700),
    ficha("grita que ya no siente", "Targitzan", "«¡Ya no siento *las piernas*!»", sub="Al perder el piso de abajo", dur=4.2, x=.30, y=.40),
    cam("sus Moggies inútiles", "moggy", "Moggies inútiles", x=.86, y=.68, dur=3.2),
    rel("Las losas donde te cubres", "templo_targitzan", "La sala sagrada", "Losas que no vuelven", dur=3.6, x=.74, y=.56, tam=500),
    mg(B.cronometro([("Autodestrucción sagrada", "0:03")]), "invoca su autodestrucción sagrada", ("durante tres segundos|fin", 1.2),
       ["invoca su autodestrucción"], "cronómetro Targitzan", y=.56),
    ficha("te exige dominar el apuntado", "En el primer mundo", "Dominar el *apuntado* en primera persona", dur=4.6, x=.72, y=.42),
    cam("en el primer mundo", "titulo_mt", "Mayahem Temple", x=.15, y=.66, dur=3.0),
    ficha("un tiro al blanco sin cerebro", "Una de las listas", "«Sin cerebro»… con *pinta y música* increíbles", sub="ivanavi",
          a=("una música increíbles|fin", .8), x=.30, y=.42),
    cad("Detalle: se autodestruye", ("no le quita el trabajo|fin", .6), ["Detalle: se autodestruye", "convertido en Mumbo", "el tótem sigue ahí",
                                                                         "Es un dios"],
        "SE AUTODESTRUYE… Y SIGUE", [("targitzan", "Se autodestruye"), ("mumbo", "Vuelves como Mumbo"), (None, "«Solo Banjo y Kazooie»")],
        ("targitzan", "Es un dios")),
    mira("Sus ojos son joyas", "SIN PARPADEO", x=.50, y=.42, dur=3.4),
    rel("el Jiggy que corona", "jiggy", "Inalcanzable", dur=3.4, x=.26, y=.56, tam=420),
    pv("un glitch y un Kazooie", "clockwork", "Kazooie de cuerda", dur=3.4, x=.78, y=.55, tam=320),
    *recre("flow_targitzan_dorado", "Bolts, volvió como una estatua", ("balones de fútbol|fin", 1.2), "Banjoland",
           "Estatua dorada que escupe *balones*", sub="Nuts & Bolts"),

    # ================================================================ GRACIAS (4 comentarios reales)
    ficha("Antes de seguir, unos comentarios", "Sus comentarios", "Todos se *leen*", sub="Gracias", dur=3.0, x=.5, y=.22, ancho=600),
    com("riuma77 escribió en el video", "Ugw_CCIkctKMyqDDO9l4AaABAg", dur=7.0, x=.30, y=.44),
    cam("en el video de los Jiggies", "jiggy", "Jiggies crueles", x=.86, y=.70, dur=3.4),
    com("Y en el de Rare dijo", "UgxKny5pWsQET7upHe94AaABAg", dur=8.4, x=.68, y=.44),
    cam("más Banjo y más Conker", "rare_hq", "Rare", x=.14, y=.74, dur=3.4),
    com("antilopezmexicanos dejó en Majora's", "Ugw2j_5-7ktR9uVpcxl4AaABAg", dur=9.0, x=.30, y=.44),
    rel("dejó en Majora's Mask", "majora", "Majora's Mask", dur=4.2, x=.78, y=.58, tam=460),
    com("Y riuma77, otra vez", "UgxdnznPHsijj-I2lE94AaABAg", dur=5.4, x=.68, y=.44),
    # promesas.md #57: el clip ya pasó a la máscara de Majora cuando la voz dice «Fiera Deidad»
    pv("la máscara de la Fiera Deidad", "cap_fiera_deidad", "La Fiera Deidad", dur=3.4, x=.24, y=.62, tam=440),
    ficha("Todos los comentarios se leen", "Gracias", "Muchos acaban *cambiando* el siguiente video", dur=4.6, x=.30, y=.30),
    pv("Gracias, de verdad", "banjo", "¡Gracias!", dur=3.0, x=.84, y=.72, tam=280),

    # ================================================================ 7 · LORD WOO FAK FAK
    mapa("jrl", _JRL_RUTA, de="Un pez abisal gigante", a=("en el cofre de Davy Jones|fin", .8), marcas=["Un pez abisal", "en el fondo del mar"],
         titulo="Jolly Roger's Lagoon"),
    ficha("se queja de lo apretado", "Davy Jones' Locker", "Se queja de lo *apretado* que está", dur=3.0, x=.72, y=.42),
    mg(B.rotulos([("LORD WOO FAK FAK", "Self-Important Anglerfish", "Pez Linterna de Gran Autoestima")]), "En español, Pez Linterna",
       ("de Gran Autoestima|fin", 1.0), ["En español, Pez Linterna"], "rótulo Woo", y=.30),
    ficha("le traen el correo", "Banjo", "«Te traemos *el correo*»", sub="No cuela", dur=3.8, x=.30, y=.64, ancho=640),
    vida("Lord Woo Fak Fak", 12, "En la primera fase tiene", ("te dejan atrapado|fin", .4), sub="6 forúnculos + 3 golpes por ojo"),
    # promesas.md #60: a esa altura el clip ya enseña la boca; el forúnculo rojo, en captura (Prosafia @739,3)
    pant("cap_woo_forunculo", "seis forúnculos en el cuerpo", ("el que parpadea|fin", .4), zoom=(1.0, 1.04)),
    mira("solo puedes reventar el que", "EL QUE PARPADEA", x=.59, y=.55, dur=2.6),
    pv("con la luz de su antena", "woo_fak_fak", "Ojos cerrados", dur=3.4, x=.24, y=.64, tam=400),
    mira("tres veces en cada uno", "3 POR OJO", x=.45, y=.55, dur=3.2),
    ficha("te lanza burbujas", "Segunda fase", "Burbujas que te dejan *atrapado*", dur=3.6, x=.74, y=.58, ancho=700),
    ficha("Al caer, se despide", "Lord Woo Fak Fak", "«Cien años de *tiranía oceánica*…»", sub="Un final nada digno", dur=4.6),
    vs("en la vida real, solo las hembras", ("Y él es lord|fin", 1.0), ["solo las hembras", "tienen farol", "Y él es lord"],
       ("EN LA VIDA REAL", "Solo las hembras tienen farol", "pez_abisal"), ("EN EL JUEGO", "Él es lord… y tiene farol", "lord_woo"),
       titulo="El farol", marca="¿LORD?"),
    grande("sale sangre roja", "woo_sangre", "Sangre roja", lado="der", dur=4.4, tam=470),
    ficha("En un juego para todas", "Para todas las edades", "Sangre *roja*", sub="Super Joe Bros: ¿cómo lo colaron?", dur=4.8, x=.28, y=.42),
    # promesas.md #66: el submarino GRANDE en su frase (antes, solo el icono final de la cadena)
    cad("Porque nadar y apuntar", ("Convertido en submarino", .2), ["Porque nadar y apuntar", "en una sala estrecha", "cuesta no perderlo"],
        "POR QUÉ CUESTA", [(None, "Nadar y apuntar"), (None, "Sala estrecha")], (None, "Lo pierdes de vista")),
    grande("Convertido en submarino", "minisub", "En submarino, más fácil", lado="der", dur=4.2, tam=520),
    pv("Lo mejor viene después", "lord_woo", "Ya derrotado", dur=2.0, x=.24, y=.74, tam=320),
    mg(B.rotulos([("LORD WOO FAK FAK", "«¡Deja de dispararme!»", "Estoy muerto, y no tengo más Jiggies"),
                  ("LORD WOO FAK FAK", "«Conozco a tu padre»", "Si insistes")]),
       "Si le sigues disparando", ("conoce a tu padre|fin", .5), ["Deja de dispararme", "te dice que conoce"], "rótulos Woo", y=.30),
    cam("y no tengo más Jiggies", "jiggy", "Sin más Jiggies", x=.86, y=.72, dur=3.0),
    ficha("Su tema es un arreglo", "Vs. Lord Woo Fak Fak", "Arreglo *dramático* del fondo del mar", sub="Grant Kirkhope", dur=4.4),
    rel("Super Smash Bros. Ultimate, en su", "smash_logo", "Smash Ultimate", "Versión original", dur=4.0, x=.26, y=.56, tam=480),
    ficha("se llama Rey Woohaha", "En Japón", "*Rey Woohaha*", dur=3.4, x=.72, y=.42, ancho=560),
    cam("En Japón, por cierto", "logo_bt_jp", "Japón", x=.86, y=.78, tam=240, dur=3.4),

    # ================================================================ 6 · KLUNGO
    cam(("el único jefe al que peleas", 1.0), "klungo", "Klungo ×3", x=.15, y=.30, tam=260, dur=3.6),
    aba([("tunel_klungo1", "Túnel 1"), ("tunel_klungo2", "Túnel 2"), ("gatehouse", "The Gatehouse")], de="dos en los túneles",   # 6-nov: los Digger Tunnels reales
        a=("donde cae del techo|fin", .8), marcas=["dos en los túneles", "de Isle O' Hags", "la última en la entrada"], nombre="peleas Klungo", x=.70),
    pv("donde cae del techo", "cap_klungo_cae", "Cae del techo", dur=3.6, x=.26, y=.58, tam=440),   # promesas.md #70 (Prosafia @1718,5)
    ficha(("antes de cada pelea|fin", .3), "Klungo", "Su *saludo*", sub="Escucha", dur=3.0, x=.5, y=.84, ancho=520),
    vida("Klungo", 3, "En cada pelea son tres golpes", ("y se bebe una distinta|fin", .4), sub="3 golpes por pelea"),
    pv("se protege con un escudo", "klungo", "Escudo", dur=3.0, x=.20, y=.64, tam=360),
    mg(B.pociones(["GIGANTE", "INVISIBLE", "2, 3, 4 KLUNGOS"]), "La roja lo vuelve gigante", ("cuatro Klungos|fin", .2),
       ["La roja lo vuelve", "La verde lo hace", "Y la azul lo multiplica"], "pociones", y=.50),
    mira(("El de verdad es el que", .4), "NARIZ MÁS CLARA", x=.50, y=.50, dur=4.0),
    vs("En Nintendo 64, qué poción", ("roja, verde y azul|fin", .8), ["En Nintendo 64, qué", "En Xbox 360, en cambio", "siempre van en el mismo"],
       ("NINTENDO 64", "Al azar en cada pelea", "n64"), ("XBOX 360", "Siempre roja, verde y azul", "xbox360"), titulo="Las pociones",
       marca="ORDEN FIJO"),
    listas("Porque las tres peleas", ("todas lo dejan justo aquí|fin", .4), "KLUNGO EN LAS 7 LISTAS", [3, 5, 6, 6, 6, 4, 6.6],
           "Media 5,23 · justo en medio"),
    ficha("Y aun así, un canal", "Jiggylookback", "Un ranking de *fuerza*, con estadísticas", dur=4.2),
    cad("en un todos contra todos", ("Inteligencia, cinco de cinco|fin", .8), ["No fue Grunty", "No fue Weldar", "Fue Klungo"],
        "TODOS CONTRA TODOS", [("gruntilda_bt", "No fue Grunty"), ("weldar", "No fue Weldar")], ("klungo", "Fue Klungo"), y=.60),
    mg(B.crueldad(5, 5, "INTELIGENCIA"), "Inteligencia, cinco de cinco", ("Inteligencia, cinco de cinco|fin", 2.0), [], "inteligencia Klungo", y=.20),
    ficha("Tras la tercera derrota", "Klungo", "«Cada vez *menos guapo*»", sub="Tercera derrota", dur=4.4, x=.30, y=.42, ancho=700),
    ficha("existe una señora Klungo", "La señora Klungo", "Existe. La nombra *una sola vez*", dur=4.4, x=.72, y=.42),
    cam("en la escena del principio", "spiral_tooie", "La intro", x=.11, y=.19, tam=220, dur=3.0),
    # promesas.md #77: la escena real del principio (P01 @155, aclarada) detrás; el Klungo SIN TEXTURAS no se ve en el juego normal
    # (solo con cámara libre): Flow pendiente para la columna «EL OTRO»
    pant("cap_intro_klungo_roca", "en la escena del principio", ("una roca y desaparece|fin", .8)),
    vs("hay un segundo Klungo", ("una roca y desaparece|fin", .8), ["hay un segundo Klungo", "sin texturas", "y desaparece"],
       ("KLUNGO", "El de siempre", "klungo"), ("EL OTRO", "Sin texturas: camina hacia una roca"), titulo="La escena del principio",
       marca="FANTASMA"),
    xbox("En Xbox 360 hasta tiene", dur=4.0),
    ficha("hasta tiene logro propio", "Logro de Xbox 360", "«*Knocked Out Klungo*»", sub="Tumbarlo tres veces", dur=4.6, x=.30, y=.42),
    grande("en la fiesta de Bottles", "bottles_cena", "La fiesta de Bottles", lado="der", dur=4.6, tam=640),
    cam("Klungo se come toda", "klungo", "Klungo", x=.14, y=.68, dur=3.4),
    # hueco de 5,1 s en 12:31 (_huecos.py, 6-nov): cierre de Klungo + entrada a la pregunta del público
    pv("Se lo había ganado", "klungo", "Se lo había ganado", dur=2.4, x=.78, y=.62, tam=340),
    ficha("Y ahora, una pregunta del", "Una pregunta", "Del *público*", sub="JaVik0", dur=3.6, x=.30, y=.30, ancho=560),

    # ================================================================ CRÍTICA (burla disfrazada)
    rel("vio nuestro video de Majora's", "majora", "Majora's Mask", "Su historia y los 12 secretos", dur=4.6, x=.76, y=.54, tam=480),
    com("y escribió", "UgynJhE1FK8jNyNruil4AaABAg", dur=7.0, x=.30, y=.40),
    mg(B.secreto(12, "Con su número en pantalla", total=12, jiggy=JIGGY), "Estaban ahí, los doce", ("con su número en pantalla|fin", 1.4), [],
       "secretos de Majora", y=.80),
    mg(B.luna(), "en Majora's Mask el tiempo", ("antes del primero|fin", 1.2), ["la luna te cayó"], "luna", y=.50),
    vida("Cualquier jefe", 10, "con su barra de vida", ("con su barra de vida y todo|fin", .6), quedan=10, sub="Te espera al final del pasillo"),
    pv("los jefes no se esconden", "hag1_intro", "No se esconden", dur=3.4, x=.78, y=.62, tam=420),

    # ================================================================ 5 · CHILLI BILLI Y CHILLY WILLY
    aba([("chilli_billi", "Chilli Billi"), ("chilly_willy", "Chilly Willy")], de=("Dos dragones hermanos", .8), a=("cuerpecito ridículo|fin", .4),
        marcas=[("Dos dragones hermanos", .8), "de cuello larguísimo"], nombre="dragones", x=.28, y=.58),
    mapa("hfp", [(.49, .85, "Inicio", "inicio"), (.49, .62), (.48, .50), (.49, .17, "Lava Crater", "meta", "chilli_billi")],
         de="el rojo vive en el cráter", a=("y el azul, en el lago", 0), marcas=["el rojo vive en el cráter"], titulo="Hailfire Peaks: lava",
         ventana=True),
    mapa("hfp_hielo", [(.40, .92, "Desde la lava", "inicio"), (.45, .72), (.49, .705, "Ice Crater", "meta", "chilly_willy")],
         de="y el azul, en el lago", a=("helado de la cima|fin", .6), marcas=["y el azul, en el lago"], titulo="Hailfire Peaks: hielo", ventana=True),
    mg(B.pedido([("Chilli Billi", "Carne picante, de doce pies"), ("Chilly Willy", "Una de anchoas")], medida="12 PIES ≈ 3,7 M"),
       "Al verte, cada uno cree", ("Willy, una de anchoas|fin", .4), ["Billi había pedido", "Willy, una de anchoas"], "pedido", y=.50),
    ficha("Kazooie le contesta al rojo", "Kazooie", "«Me temo que no, *cara de verruga*»", dur=4.2, x=.30, y=.42),
    grande("se come a los repartidores", "chilli_billi2", "Chilli Billi", lado="der", dur=2.6, tam=580),
    vs("Se les hace daño con el huevo", ("y fuego al de hielo|fin", .8), ["Se les hace daño", "hielo al de fuego", "y fuego al de hielo"],
       ("CHILLI BILLI", "Huevos de hielo", "ice_nest"), ("CHILLY WILLY", "Huevos de fuego", "fire_nest"), titulo="El huevo contrario", marca=None),
    mira("por dentro de unos cañones", "DENTRO DEL CAÑÓN", x=.50, y=.52, dur=2.4),
    ficha(("te sirven de escudo", .4), "Los cañones", "Te sirven de *escudo*… hasta que revientan", dur=3.6, x=.28, y=.55, ancho=700),
    ficha("te barren con la lengua", "Sin cañones", "Te barren con *la lengua*", dur=3.4, x=.72, y=.42, ancho=640),
    sil("Y el de hielo, además", "chilly_willy", "Chilly Willy", "Muerte instantánea", lado="izq", dur=4.0),
    vida("El primero que enfrentes", 6, "El primero que enfrentes", ("y el segundo, doce", 0), sub="6 de vida"),
    vida("El segundo", 12, "y el segundo, doce", ("pide un trofeo", 0), sub="12 de vida"),
    rel("dan un solo Jiggy", "jiggy", "Un solo Jiggy", "Para los dos", dur=4.4, x=.74, y=.56, tam=460),
    ficha("cuando Kazooie pide un trofeo", "El segundo dragón", "«Es *lo único* que tengo»", dur=4.0, x=.30, y=.42, ancho=640),
    # promesas.md #95: las dos mitades reales (antes, hexágonos vacíos)
    mg(B.funden((P("cap_hfp_hielo"), "Ice Caves"), (P("cap_hfp_lava"), "Lava Island"), (P("titulo_hfp"), "Hailfire Peaks", "EL JEFE SE DUPLICÓ"),
                titulo="DOS MUNDOS, UNA MONTAÑA"),
       "Porque Hailfire Peaks eran", ("el jefe se duplicó|fin", 1.0), ["unas cuevas de hielo", "y una isla de lava", "Al fundirlas en una"],
       "funden", y=.52),
    listas("Es el puesto más dividido", ("contra los dos a la vez|fin", .4), "LOS DRAGONES EN LAS 7 LISTAS", [7, 6, 9, 2, 4, 9, 5.5],
           "Media 6,07 · el más dividido"),
    pv("Al irse volando", "chilly_willy", "Se van", dur=3.0, x=.80, y=.56, tam=330),
    rel("hamburguesas de Big Al", "big_al", "Big Al", "Hamburguesas", dur=4.0, x=.26, y=.56, tam=460),
    ficha("el autoservicio de McJiggy's", "El otro dragón", "¿Dónde queda el autoservicio de *McJiggy's*?", dur=3.2, x=.72, y=.42),

    # ================================================================ 4 · MR. PATCH
    pv(("Un dinosaurio inflable", 2.4), "mr_patch", "Mr. Patch", dur=3.0, x=.24, y=.58, tam=300),
    mapa("ww", [(.82, .58, "Entrada", "inicio"), (.68, .50), (.48, .45, "La carpa", "meta", "big_top")], de="que vive dentro de la carpa",
         a=("dentro de la carpa del circo|fin", .5), marcas=["que vive dentro de la carpa"], titulo="Witchyworld", ventana=True),
    mg(B.rotulos([("MR. PATCH", "Strange Wobbly Inflatable Thing", "Señor Parche, Cosa Inflable, Extraña e Inestable")]),
       "En español, Señor Parche", ("Extraña e Inestable|fin", 1.0), ["En español, Señor Parche"], "rótulo Patch", y=.30),
    vs("Kazooie le responde que Klungo", ("era más grande|fin", .8), ["Kazooie le responde", "al principio del juego", "era más grande"],
       ("MR. PATCH", "«Mira qué grande y fuerte soy»", "mr_patch"), ("KLUNGO", "Al principio del juego: más grande", "klungo"),
       titulo="¿Quién es más grande?", marca="KAZOOIE GANA"),
    vida("Mr. Patch", 12, "Tiene doce parches", ("y más rápido|fin", .5), sub="12 parches"),
    rel("solo los huevos granada", "granada", "Huevos granada", dur=3.4, x=.26, y=.58, tam=440),
    ficha("la pelea sube al aire", "En el aire", "Vuelas, apuntas y esquivas *pelotas explosivas*", dur=4.4, x=.72, y=.50),
    mira("Y cada parche que revientas", "MÁS PEQUEÑO, MÁS RÁPIDO", x=.58, y=.55, dur=3.6),
    mg(B.rotulos([("MR. PATCH", "«Así nunca me vas a ganar»", "Con huevos normales"), ("MR. PATCH", "«No soy un inflable violento»", "En la revancha"),
                  ("KAZOOIE", "«Solo eres aire caliente»")]),
       "Cuando lo intentas con huevos", ("solo es aire caliente|fin", 1.0), ["se ríe de ti", "En la revancha te pide", "Kazooie le dice que solo"],
       "rótulos Patch", y=.30),
    pv("se ríe de ti", "mr_patch", "Se ríe", dur=3.0, x=.26, y=.68, tam=360),
    listas("Es el favorito del público", ("un nudo en el estómago|fin", .4), "MR. PATCH EN LAS 7 LISTAS", [4, 9, 2.5, 10, 9, 6, 7.8],
           "Media 6,89 · el favorito del público"),
    mg(B.fechas([("Documento «Fair #5»", "17 oct 1998", P("rare_hq"))], "Documento de diseño de Rare"),
       "Su documento de diseño, de octubre", ("traía otras ideas", .2), ["de octubre de mil"], "fecha Patch", y=.25),
    *recre("flow_patch_globos", "globos teledirigidos", ("Hoy hay cuatro", 0), "Fair #5 · El documento", "Globos que sueltan *granadas*",
           sub="Y un solo punto de vuelo"),
    pant("cap_patch_pad", "Hoy hay cuatro", ("Hoy hay cuatro|fin", 1.2)),   # promesas.md #105 (punto de vuelo real, Prosafia @486,5)
    ficha("Hoy hay cuatro", "El juego", "*Cuatro* puntos de vuelo", dur=2.8, x=.72, y=.42, ancho=600),
    cam("Y volvió años después", "nuts_bolts", "Nuts & Bolts", x=.86, y=.68, dur=3.0),
    aba([("patch_nutty", "Nutty Acres"), ("patch_banjoland", "Banjoland")], de="encadenado en Nutty Acres", a=("sin un solo parche|fin", .8),
        marcas=["encadenado en Nutty", "y en Banjoland"], nombre="Patch en Nuts & Bolts", x=.30),
    rel("Además, está en Super Smash", "smash_logo", "Smash Ultimate", "Vs. Mr. Patch", dur=4.0, x=.74, y=.56, tam=480),
    mg(B.fechas([("35th Anniversary Collection", "4 ago 2020", P("rare_hq"))], "Rare cumple 35 años"),
       "Y cuando Rare cumplió", ("la de Mr. Patch|fin", .4), ["en dos mil veinte"], "fecha álbum Rare", y=.30),
    ficha(("Mr. Patch. Escúchala|fin", .4), "Mr. Patch", "*35th Anniversary Collection*", sub="Rare, 2020", dur=3.4, x=.5, y=.84, ancho=700),

    # ================================================================ 3 · MINGY JONGO
    mapa("ccl", _CCL_RUTA, de="En ese mundo hay dos calaveras", a=("se sortea en cada partida|fin", 1.0),
         marcas=["hay dos calaveras", "En una está tu amigo", "En la otra, un robot"], titulo="Cloud Cuckooland"),
    vs("Hay pistas: la falsa", ("casi siempre te llama oso|fin", .8), ["la falsa tiene las antorchas", "un Jinjo en vez de", "el robot te saluda"],
       ("MUMBO", "Antorchas encendidas, un Minjo, te llama «oso»", "mumbo_tooie"),
       ("MINGY JONGO", "Antorchas apagadas, un Jinjo, «Hola, Banjo»", "cap_jinjo_falso"), titulo="Las pistas", marca="IMPOSTOR"),
    # promesas.md #118: el disfraz roto y el metal (captura real, ProsafiaGaming 7RlB7mXcqlU @1600)
    pant("cap_mingy_metal", "le arranca un trozo del disfraz", ("Antes ya te había avisado", 0)),
    ficha("te fulmina en plena escena", "En la escena", "Te quita *un panal*", sub="Con uno solo: mueres", a=("empiece la pelea|fin", .6)),
    pv("y te quita un panal", "mingy_bt", "Mingy Jongo", dur=3.6, x=.20, y=.62, tam=420),
    vida("Mingy Jongo", 8, "Tiene ocho de vida", ("la resistencia es inútil|fin", .4), sub="8 de vida"),
    mira("Te dispara magia que te", "MAGIA QUE TE PERSIGUE", x=.55, y=.55, dur=3.2),
    pv("deja ver el metal", "mingy_jongo", "El metal", dur=2.2, x=.80, y=.68, tam=310),
    mg(B.rotulos([("MINGY JONGO", "«Mi elaborado disfraz, arruinado»", "Con el primer golpe"),
                  ("MINGY JONGO", "«La resistencia es inútil»", "Antes de pelear")]),
       "Con el primero se lamenta", ("la resistencia es inútil|fin", .8), ["Con el primero se lamenta", "y de que la resistencia"], "rótulos Mingy",
       y=.45),
    ficha("Por el giro", "El giro", "Tu *chamán* te dispara", dur=2.8, x=.72, y=.42, ancho=640),
    cam("el chamán que te ayuda", "mumbo", "Mumbo", x=.15, y=.66, dur=3.4),
    ficha("es el mejor jefe de Tooie", "Una de las listas", "El *mejor jefe* de Tooie", sub="WatchMojo", dur=2.8, x=.30, y=.42, ancho=640),
    *recre("flow_mingy_ojos_rojos", "Rare iba a ponerle ojos rojos", ("Le quitó los ojos", 0), "El plan", "Ojos *rojos* y látigo *eléctrico*",
           sub="Documento de diseño", marca_a=("la sorpresa fuera el ataque|fin", .8)),
    vs("Le quitó los ojos", ("la sorpresa fuera el ataque|fin", .8), ["Le quitó los ojos", ("Le quitó los ojos", .5), "la sorpresa fuera"],
       ("EL PLAN", "Ojos rojos y látigo eléctrico", "flow_mingy_ojos_rojos"), ("EL JUEGO", "Sin ojos rojos: sorpresa", "mingy_bt"),
       titulo="Documento de diseño", marca="SORPRESA"),
    ficha("Según la wiki, es el único jefe", "Según la wiki", "El único que *muere de verdad*", sub="Líquido verde", dur=4.4, x=.30, y=.42, ancho=700),
    pv("explota, y suelta un líquido", "mingy_jongo", "Explota", dur=3.0, x=.80, y=.62, tam=380),
    vs("Y su música es la única", ("vuelto en tu contra|fin", .6), ["su música es la única", "Es el tema de Mumbo", "vuelto en tu contra"],
       ("LOS DEMÁS", "Su música sale de su mundo"), ("MINGY JONGO", "El tema de Mumbo", "mumbo_tooie"), titulo="La música", marca="EN TU CONTRA"),
    ficha(("en tu contra. Escucha|fin", .4), "Mingy Jongo", "El tema de *Mumbo*, en tu contra", sub="Grant Kirkhope", dur=3.4, x=.5, y=.84, ancho=700),

    # ================================================================ 2 · HAG 1
    grande(("El tanque perforador de las hermanas", .6), "hag1", "Hag 1", lado="der", dur=4.0),
    cam("con Gruntilda al volante", "gruntilda_bt", "Gruntilda", x=.15, y=.66, dur=3.2),
    vida("Hag 1", 10, "Tiene cien de vida", ("y se le cae|fin", .5), sub="100 de vida"),
    mira("cuando Grunty asoma la cabeza", "GRUNTY ASOMA", x=.50, y=.50, dur=3.4),
    mg(B.fases(["Láseres", "Doble láser", "Mortero", "Doble mortero", "Taladro", "Batería 1", "Batería 2", "Magia", "Uggers", "Gas tóxico"]),
       "Son diez fases", ("y al final prepara su hechizo", 0),
       ["Son diez fases", "el doble de láseres", "mortero, doble", "doble mortero y", "y el taladro", "para volar una batería", "Luego, la otra",
        "Grunty pelea con magia", "manda a sus Uggers", "te echa gas tóxico"], "fases Hag 1", y=.58),
    cam("metes un Kazooie de cuerda", "clockwork", "Kazooie de cuerda", x=.10, y=.30, tam=200, dur=3.4),
    cam("manda a sus Uggers", "ugger", "Uggers", x=.90, y=.30, tam=200, dur=3.0),
    grande("prepara su hechizo más fuerte", "hag1_boom", "Se le cae", lado="izq", dur=4.4, tam=600),
    mg(B.cronometro([("Para contestar", "0:05")]), "te hace preguntas, con cinco", ("para contestar|fin", .3), ["con cinco segundos"],
       "cronómetro preguntas", y=.30),
    vs("Si aciertas, ataca más lento", ("Si fallas, más rápido|fin", .8), ["Si aciertas", "Si fallas", ("Si fallas, más rápido|fin", .2)],
       ("ACIERTAS", "Ataca más lento"), ("FALLAS", "Ataca más rápido"), titulo="Cinco segundos", marca=None),
    pv("Y habla sin parar", "gruntilda_bt", "Gruntilda", dur=3.0, x=.20, y=.66, tam=380),
    mg(B.rotulos([("GRUNTILDA", "«¿Dónde está el botón del láser?»", "Que alguien le pase el manual"),
                  ("GRUNTILDA", "«¡Que llamen a una grúa!»", "Sin baterías")]),
       "En la primera fase no encuentra", ("llamen a una grúa|fin", 1.0), ["no encuentra el botón", "pide que llamen a"], "rótulos Grunty", y=.30),
    leg("gruntilda_bt", "Gruntilda", ["Apellido: Winkybunion", "En español: Juanetes", "Amenaza con demandar"], de="se le escapa su apellido",
        a=("Lo sentimos, Grunty|fin", .6), marcas=["Gruntilda Juanetes"], sello=("SECRETO", 0), x=.26, y=.54),
    ficha("Gruntilda Winkybunion", "Su apellido", "*Winkybunion*", sub="En español: Juanetes", dur=4.4, x=.72, y=.42, ancho=640),
    ficha("amenaza con demandarte", "Gruntilda", "«Si se lo cuentas a alguien, *te demando*»", dur=4.0, x=.72, y=.42),
    ficha("no es la primera? Por larga", "Por larga", "Cámaras que te hacen mirar *al lado equivocado*", sub="La queja de las listas",
          a=("al lado equivocado|fin", .8)),
    mg(B.crueldad(5, 5, "ESPECTÁCULO"), "Pero en espectáculo", ("del juego le gana|fin", 1.4), [], "espectáculo Hag", y=.74, x=.30),
    cam("Y no iba a ser así", "cauldron_keep", "Cauldron Keep", x=.88, y=.18, tam=220, dur=2.8),
    *recre("flow_hermanas_torre", "subías la torre", ("Grunty en la cima|fin", .6), "El plan original", "Las hermanas, *una por una*",
           sub="Mingella y Blobbelda"),
    cam("antes de llegar a Grunty", "gruntilda_bt", "Grunty, en la cima", x=.13, y=.40, tam=240, dur=2.6),
    cam("Y antes de la perforadora", "hermanas", "Las hermanas", x=.13, y=.40, tam=220, dur=3.0),
    *recre("flow_caldero_volador", "huían de Spiral Mountain", ("caldero mecánico volador|fin", 1.4), "Guion temprano",
           "Huían en un caldero *mecánico* volador", sub="Antes de la Hag 1"),
    ficha("Un misterio que la wiki", "Sin explicación", "Huellas que suben *en vertical*", sub="Según la wiki", dur=4.0),
    aba([("wasteland", "Wasteland"), ("quagmire", "Quagmire")], de="las huellas de la perforadora", a=("también trepa|fin", .8),
        marcas=["por las paredes de Wasteland", "y de Quagmire"], nombre="huellas", x=.30),
    pv("al parecer, también trepa", "hag1", "Hag 1", dur=2.0, x=.72, y=.64, tam=320),

    # ================================================================ 1 · WELDAR
    mapa("gi", _GI_RUTA, de="Un soplete con forma de serpiente", a=("que casi no ve|fin", 1.2), marcas=["Un soplete con forma", "que casi no ve"],
         titulo="Grunty Industries", ventana=True, x=.74, y=.42),   # ventana: el soplete-serpiente se ve en el clip (promesas.md #133)
    cad("Llegar a él ya es un jefe", ("del taller de reparaciones|fin", .6), ["Mumbo apaga el electroimán", "Banjo se convierte en lavadora",
                                                                              "y bajas al sótano"],
        "LLEGAR YA ES UN JEFE", [("electroiman", "Mumbo apaga el electroimán"), ("washer", "Banjo lavadora: el interruptor")],
        ("repair_depot", "El sótano del taller")),
    ficha("Weldar dice que se dejó", "Weldar", "«Me dejé *las gafas*»", dur=3.8, x=.30, y=.42, ancho=600),
    ficha("Y te pide que te acerques", "Weldar", "«Acércate, que *no te veo*»", dur=4.0, x=.72, y=.42, ancho=640),
    pv("desde ahí no te ve", "weldar", "Casi no ve", dur=3.0, x=.20, y=.68, tam=380),
    vida("Weldar", 6, "Tiene seis golpes", ("electrifica los cables del suelo|fin", .4), sub="6 golpes"),
    mira("y todos van a la boca", "A LA BOCA", x=.35, y=.52, dur=3.4),
    aba([("fire_nest", "Huevo de fuego"), ("granada", "Granada"), ("clockwork", "Kazooie de cuerda")], de="un huevo de fuego, una",
        a=("justo cuando aspira|fin", .6), marcas=["un huevo de fuego", "una granada o", "un Kazooie de cuerda, justo"], nombre="munición Weldar", x=.74),
    cad("Entre medias te lanza bolas", ("patas, y salta para aplastarte|fin", 0), ["bolas de fuego azules", "tuercas y tornillos", "patas, y salta"],
        "ENTRE GOLPE Y GOLPE", [(None, "Bolas de fuego azules"), ("cap_weldar_tuerca", "Tuercas y tornillos con patas")], ("weldar", "Salta para aplastarte"), y=.58),
    pv("suelta tuercas y tornillos", "cap_weldar_tuerca", "Tuercas con patas", dur=3.0, x=.85, y=.34, tam=330),   # promesas.md #138 (Prosafia @1243,8)
    ficha(("Cuando le das, se queja", .3), "Weldar", "«Estoy lleno de *gas inflamable*»", dur=4.4, x=.72, y=.50),
    ficha("busca su interruptor de emergencia", "Tras el tercer golpe", "Su *interruptor de emergencia*", dur=3.6, x=.30, y=.45, ancho=700),
    ficha(("cables del suelo. Escucha|fin", .3), "Suelo electrificado", "Los *cables* del suelo", sub="Escucha", dur=2.8, x=.5, y=.84, ancho=600),
    listas("Porque es difícil, pero justo", ("lo ponen primero|fin", 1.0), "WELDAR EN LAS 7 LISTAS", [8, 10, 10, 9, 7, 10, 8.9],
           "Media 8,98 · tres lo ponen primero"),
    cad("su cabeza sale volando", ("donde había escondido su Jiggy|fin", .6), ["su cabeza sale volando", "choca con una caja", "apaga el ventilador",
                                                                               "donde había escondido"],
        "LA CABEZA DE WELDAR", [("weldar", "Sale volando"), ("cap_weldar_caja", "Caja de alta tensión"), ("aire_planta", "Para el ventilador")],
        ("jiggy", "El Jiggy escondido")),
    # promesas.md #142-143: la caja y el ventilador GRANDES (en la cadena son iconos de 60 px)
    pv("choca con una caja de alta", "cap_weldar_caja", "Alta tensión", dur=2.4, x=.85, y=.28, tam=320),
    pv("apaga el ventilador gigante", "aire_planta", "El ventilador gigante", dur=3.2, x=.85, y=.28, tam=340),
    ficha("cuándo aprenderá a callarse", "Weldar", "«¿Cuándo aprenderé a *callarme*?»", dur=3.6, x=.72, y=.42, ancho=700),
    ficha("Su última pregunta es", "Weldar", "«¿Me recomiendas un buen *técnico*?»", dur=4.4, x=.30, y=.42, ancho=700),
    rel("técnico de reparaciones", "repair_depot", "Repair Depot", dur=3.4, x=.74, y=.56, tam=480),
    mg(B.rotulos([("WELDAR", "«¿Eres un oso?»"), ("KAZOOIE", "«Y tú, a la planta de reciclaje»")]), "la cabeza te pregunta",
       ("la planta de reciclaje|fin", 1.0), ["la cabeza te pregunta", "le contesta que sí"], "rótulos Weldar", y=.30),
    cam("le contesta que sí", "kazooie", "Kazooie", x=.14, y=.72, dur=3.0),
    ficha("el jefe de la fábrica ni siquiera", "Primera lista de Rare", "El jefe de la fábrica *no era él*", a=("Eran The Kogs", 0),
          x=.72, y=.42, ancho=640),
    *recre("flow_kogs", "Eran The Kogs", ("acabó siendo el mejor|fin", 1.0), "«The Kogs»", "Unos *engranajes*", sub="Primera lista de Rare"),
    pv("Weldar no existía", "weldar", "El número 1", dur=3.0, x=.19, y=.50, tam=340),
    rel("cae encima de un Kazooie", "clockwork", "Kazooie de cuerda", dur=3.6, x=.26, y=.56, tam=440),
    ficha("el juego entero se cuelga", "Glitch", "El juego *entero* se cuelga", dur=2.6, x=.72, y=.42, ancho=600),
    cad("Y no acabó en la basura", ("el Aliento de Weldar|fin", .8), ["no acabó en la basura", "Mumbo encontró su cuerpo", "el Aliento de Weldar"],
        "NUTS & BOLTS", [("weldar", "En la basura"), ("mumbo_nyb", "Mumbo lo encuentra")], ("weldar_breath", "«Aliento de Weldar»")),   # 6-nov: Mumbo de N&B
    pv(("el Aliento de Weldar", .2), "weldar_breath", "El Aliento de Weldar", dur=3.4, x=.50, y=.80, tam=380),   # promesas.md #146
    cam("en Nuts and Bolts, según", "nuts_bolts", "Nuts & Bolts", x=.88, y=.19, tam=220, dur=3.0),

    # ================================================================ CIERRE
    mg(B.escalera([P(s) for s, _ in RANKING], 10, titulo="EL RANKING"), "Ese es el ranking", ("siete listas de jugadores|fin", 1.0), [],
       "escalera final", y=.50),
    cam("Mingy Jongo merecía el primero", "mingy_jongo", "Mingy Jongo", x=.20, y=.66, dur=3.0),
    cam("Old King Coal se merece", "old_king_coal", "Old King Coal", x=.80, y=.66, dur=3.2),
    ficha("Déjalo en los comentarios", "Tu ranking", "Déjalo en los *comentarios*", dur=4.0, x=.30, y=.42, ancho=640),
    pv("a veces acaban en el siguiente", "banjo", "Tu comentario", dur=3.4, x=.78, y=.60, tam=400),
    pv("suscríbete", "smash_banjo", "Suscríbete", dur=4.2, x=.78, y=.58, tam=440),
    ficha("Quedan muchos jefes", "Próximamente", "Más jefes por *poner en orden*", dur=3.8, x=.30, y=.42, ancho=640),
] + _puestos()

# Más pegatinas (densidad ≥ 5/min y huecos > 4 s de la simulación del 5-nov: 0,38 s/palabra; repasar con _huecos.py con el timeline real).
FX += [
    cam("Kazooie, con la delicadeza", "kazooie", "Kazooie", x=.12, y=.76, tam=240, dur=3.0),
    pv("Escupe desde lo alto", "terry", "Escupe", dur=2.4, x=.82, y=.62, tam=330),
    pv("cada vez que escupe, la cámara", "terry", "Terry escupe", dur=3.0, x=.20, y=.64, tam=340),
    pv("solo por detrás del jefe final", "hag1", "El jefe final", dur=2.2, x=.18, y=.66, tam=300),
    ban("Él jura que no es ese rey", "old_king_coal", "Old King Coal", "«No soy ese rey»", foco=(.5, .35, 1.3), dur=2.4, y=.76, lado="izq"),
    ban("Cuando pierde el piso de abajo", "targitzan", "Targitzan", "Pierde el piso de abajo", foco=(.5, .55, 1.2), dur=3.4, y=.78),
    pv("con una pinta y una música", "targitzan", "Pinta increíble", dur=3.0, x=.78, y=.64, tam=360),
    cam("Banjo intenta salir del paso", "banjo", "Banjo", x=.86, y=.68, dur=3.0),
    ban("Al caer, se despide", "woo_fak_fak", "Lord Woo Fak Fak", "Cien años de tiranía", foco=(.5, .5, 1.2), dur=3.4, y=.78, lado="izq"),
    cam("ya no lo querrá", "klungo", "Klungo", x=.86, y=.76, tam=240, dur=3.0),
    ban("Y el dragón decide que", "chilli_billi", "Chilli Billi", "Si no hay pizza…", foco=(.5, .3, 1.3), dur=2.4, y=.76, lado="izq"),
    pv("es lo único que tiene", "chilli_billi", "El segundo dragón", dur=2.4, x=.80, y=.64, tam=320),
    pv(("Y cada parche que revientas", .3), "mr_patch", "Más pequeño", dur=3.0, x=.31, y=.66, tam=340),
    pv("el momento que más recuerda", "mingy_bt", "La traición", dur=3.0, x=.78, y=.62, tam=360),
    cam("Entre fase y fase", "gruntilda_bt", "Gruntilda pregunta", x=.86, y=.70, dur=3.0),
    pv("ninguna pelea del juego le gana", "ck_rooftop", "La cima del castillo", dur=3.0, x=.74, y=.62, tam=400),
    cam("Al verte, Weldar dice", "weldar", "Weldar", x=.86, y=.76, tam=240, dur=2.4),
    pv("pierde la paciencia", "weldar", "Sin paciencia", dur=3.0, x=.76, y=.64, tam=340),
    cam("de Terry a Weldar", "terry", "Terry", x=.10, y=.80, tam=220, dur=2.6),
    cam(("de Terry a Weldar", 1.0), "weldar", "Weldar", x=.90, y=.80, tam=220, dur=2.6),
]

# Frases y escenas añadidas al guion el 5-nov (final de p10, p09, p07, p05; Gruntlings en p06b; escenas «mitad» y «fuera»).
FX += [
    # p10: el único que no acaba derrotado
    ficha("es el único jefe que no acaba", "Según la wiki", "El único que *no acaba derrotado*", sub="Terry", dur=4.4),
    rel("puedes volver a su nido", "terry_nest", "Terry's Nest", "Ahí sigue", dur=3.8, x=.26, y=.56, tam=480),
    # p09: el segundo jugador que controlaba al jefe
    cam("Y otro dato de los archivos", "rare_hq", "Rare", x=.88, y=.20, tam=220, dur=2.6),
    # promesas.md #43: el mando GRANDE (antes, icono de 60 px dentro de una cadena)
    ficha("probaron que un segundo jugador", "La prueba de Rare", "Un *2.º jugador* controlaba al jefe", sub="Lo quitaron: nadie podía ganarle",
          a=("nadie podía ganarle|fin", .6), x=.72, y=.42),
    rel("con el mando", "n64_mando", "Con el mando", "Un 2.º jugador", dur=4.2, x=.26, y=.56, tam=460),
    # p07: Jingaling se va de pesca con él
    pv("el rey Jingaling se va", "jingaling", "Rey Jingaling", dur=3.6, x=.22, y=.60, tam=380),
    ficha("Pero te pide que no se lo", "Rey Jingaling", "Va de *pesca* con él… en secreto", sub="Según la wiki", dur=4.0),
    # p06b: la voz de Klungo
    ficha("Y su voz, según la wiki", "La voz de Klungo", "Gruntlings *ralentizados*", sub="Según la wiki", a=("ralentizadas|fin", .6), x=.30, y=.42,
          ancho=700),
    rel("son grabaciones de los Gruntlings", "gruntling", "Gruntling", "Secuaz pequeño", dur=4.0, x=.74, y=.56, tam=460),
    # mitad
    mg(B.escalera([P(s) for s, _ in RANKING[:5]], 10, titulo="VAMOS POR LA MITAD"), "Vamos por la mitad", ("Arriba quedan cinco|fin", .2), [],
       "escalera mitad", y=.50),
    pil([("chilly_willy", "Dos dragones"), ("mr_patch", "Un globo con parches"), ("mingy_jongo", "Un traidor"), ("hag1", "Un tanque"),
         ("weldar", "Un soplete")], de="Y entre ellos hay dos dragones", a=("un tanque y un soplete|fin", .8),
        marcas=["hay dos dragones", "un globo con parches", "un traidor", "un tanque y", "y un soplete"], nombre="los cinco de arriba", y=.56, tam=250),
    # p05: el pingüino
    pv(("Chilly Willy, por cierto", .2), "chilly_willy", "Chilly Willy", dur=2.2, x=.20, y=.60, tam=360),
    ficha(("se llama igual que el pingüino", .5), "Chilly Willy", "Se llama como el *pingüino* de los dibujos animados", sub="El nombre", dur=3.8, x=.27),   # regla 3: sin imagen de otro tema
    ficha(("se llama igual que el pingüino", .3), "Chilly Willy", "Como el *pingüino* de los dibujos animados", dur=4.2),
    # fuera del top
    ficha("Antes del podio", "Fuera del top", "Los que se *quedaron fuera*", dur=3.0, x=.5, y=.26, ancho=640),
    sil("Conga ya no pelea", "conga", "Conga", "Ya no pelea", lado="der", dur=3.6),
    pv("vigila la puerta de la carpa", "big_top", "La carpa", dur=3.4, x=.22, y=.60, tam=400),
    cam("Los Zubbas no son jefes", "zubba", "Zubbas", x=.14, y=.68, tam=260, dur=3.0),
    rel("son un minijuego", "zubba_nido", "Minijuego", "Disparas como abeja", dur=4.0, x=.74, y=.54, tam=520),
    pv("Y los Uggers son solo", "ugger", "Uggers", dur=3.4, x=.22, y=.62, tam=380),
    cam("salen de la Hag 1", "hag1", "Hag 1", x=.86, y=.70, tam=240, dur=2.8),
    cam("Y el jefe que nunca llegó", "rare_hq", "Rare", x=.14, y=.70, dur=2.6),
    pv("Cloud Cuckooland se llamaba", "titulo_ccl", "Cloud Cuckooland", dur=3.6, x=.24, y=.58, tam=420),
    *recre("flow_avispa_mushroomland", "se llamaba Mushroomland", ("su jefe era una avispa gigante|fin", 1.0), "Mushroomland",
           "Su jefe: una *avispa gigante*", sub="El jefe que nunca llegó"),
    mg(B.escalera([P(s) for s, _ in RANKING[:7]], 10, titulo="EL PODIO"), "Ahora sí. Quedan tres", ("Quedan tres. El podio|fin", 1.0), [],
       "escalera podio", y=.50),
]

ROTULOS = [
    dict(texto="LA TRAICIÓN", en="La traición", tam=150, color="amarillo", y=.50, dur=2.0),
    dict(texto="¡ES BROMA!", en="Es broma", tam=130, color="amarillo", y=.80, dur=1.8),
    dict(texto="¿Y LOS SECRETOS?", en="Y los secretos", tam=120, color="amarillo", y=.84, dur=2.2),
    dict(texto="MUERTE INSTANTÁNEA", en="muerte instantánea", tam=110, color="amarillo", y=.84, dur=2.0),
    dict(texto="¡AIRE CALIENTE!", en="solo es aire caliente", tam=110, color="amarillo", y=.84, dur=2.0),
]
SFX = {}
# SONIDOS DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/bt_*.mp3
_ROTA = ["bt_nota", "bt_pluma", "bt_panal", "bt_nota", "bt_correcto", "bt_pluma"]
PISTAS = [dict(sfx="bt_jiggy", en=en, vol=.45) for en in PUESTOS.values()] + [
    dict(sfx=_ROTA[i % len(_ROTA)], en=e, vol=.45) for i, e in enumerate([
        "Tres jefes de Banjo-Tooie casi", "Hay un tótem que se autodestruye", "Un rey de carbón que pierde", "Faltaban ellos",
        "Terry es macho", "Es broma", "Boulder». Una roca", "Luego el derecho", "Despótico Dios Tótem", "Es un dios", "Y él es lord",
        "Deja de dispararme", "Fue Klungo", "Y la azul lo multiplica", "Willy, una de anchoas", "Al fundirlas en una", "era más grande",
        "La traición", "Le quitó los ojos", "Gruntilda Juanetes", "pide que llamen a", "Eran The Kogs", "el juego entero se cuelga"])] + [
    dict(sfx="bt_jinjo", en="Estos son los diez jefes", vol=.5),
    dict(sfx="bt_jiggy", en="Vamos por la mitad", vol=.45),
    dict(sfx="bt_jiggy", en="Quedan tres. El podio", vol=.45),
    dict(sfx="bt_nota", en="Conga ya no pelea", vol=.45),
    dict(sfx="bt_panal_skill", en="la luna te cayó", vol=.45),
    dict(sfx="bt_guhuh", en="Nos vemos en la próxima", vol=.55),
]
