# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 30 MISTERIOS más raros de Call of Duty» (SECUENCIA YT, Expediente 141, 10-nov-2026).
Helpers de videos/cod_mandela/efectos.py (kit nucleo/mg_cod.py + peg_estilos/peg_anim/presenta con tema «cod»).
MG propios de este guion: `C.caso` (veredicto RESUELTO / SIN RESOLVER / FALSO / ERA VERDAD al cierre de cada puesto) y
`C.descifra` (Morse de Blundell, ADFGX, anagrama de Nyarlathotep); mapa real de Verdansk con la ruta de los teléfonos (tema «cod»).
Sonidos nombrados (regla 31-oct-2026): PISTAS voz=True con sfx/s_*.mp3 (audio/cortes/_cortar.py).
    python fab.py cod_misterios fx --seco   tiempos      python fab.py cod_misterios fx hoja   previews/fx_NN.jpg
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
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=30), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


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


FX = [
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("motd", "EXPEDIENTE 141", ["Asunto: lo inexplicable", "30 misterios", "Clasificación: secreto"],
        de="Asunto: lo que nadie", a=("Azotea de Alcatraz", -.1), x=.78, y=.50),
    pv("Azotea de Alcatraz", "alcatraz", "Alcatraz", dur=3.0, x=.80, y=.60, tam=360),
    mg_en(C.objetivo("Mira los fuegos artificiales", "Con el francotirador"), "Un rifle de francotirador", 3.4, "objetivo mira", x=.30, y=.82),
    pant("cara_motd", ("Mira bien", .9), ("Mira bien|fin", 2.0), zoom=(1.12, 1.0)),
    caso("nadie sabe de quién es esa cara", "sin_resolver", "La cara de Alcatraz", "Mob of the Dead · 2013", dur=2.6),
    cam("Una voz que Treyarch cambió", "samantha", "Samantha", dur=2.4, x=.16, y=.66),
    pv("Un fantasma sin arma", "vacant", "Vacant · CoD 4", dur=2.6, x=.80, y=.62, tam=330),
    pv("Un corazón escondido", "der_eisendrache", "Der Eisendrache", dur=2.8, x=.18, y=.64, tam=330),
    pv("Un platillo volante", "c_finesthour", "Finest Hour · 2004", dur=2.6, x=.80, y=.62, tam=320),
    sil("Y un hombre de traje", "shadowman", "¿?", "Modern Warfare 3 · 2011", lado="der", dur=3.4),
    mg_en(C.contador(30, "MISTERIOS", "Expediente 141"), "Treinta misterios y leyendas", 2.6, "contador 30", x=.30, y=.30),
    mg_en(C.balanza("Estado de los expedientes", [("Resueltos leyendo el código", True, "unos"), ("Todavía abiertos", False, "otros")]),
          "Unos resueltos años después", 4.2, "balanza resueltos", y=.50),
    mg_en(C.objetivo("Compruébalo en pantalla", "Cada misterio, con el juego real"), "Todo con el juego", 3.0, "objetivo pantalla", x=.30, y=.82),
    pv("Infinity Ward nunca quiso", "infinityward", "Infinity Ward", dur=2.8, x=.80, y=.60, tam=320),

    # ---------------- 30 · Private Eye
    puesto("Número treinta", 30, "El chicle que nunca salió", "ZOMBIES / SHADOWS OF EVIL / BLACK OPS 3"),
    leg("soe", "SHADOWS OF EVIL", ["Black Ops 3 · 2015", "Morg City · años 40"], de="Shadows of Evil, Black Ops 3",
        a=("Las máquinas de GobbleGum", -.1), x=.78, y=.52),
    rel("Las máquinas de GobbleGum", "gobblegum", "GobbleGum", "Chicles con poderes", dur=3.4, x=.77, y=.52, tam=420),
    ficha("uno te da todas las perks", "Perkaholic", "Te da *todas las perks* de golpe.", "INTEL / GOBBLEGUM", dur=3.0),
    ficha("los zombis no te vean", "En llamas de sombra", "Los zombis *no te ven* un rato.", "INTEL / GOBBLEGUM", dur=3.0),
    mg_en(C.marcador("Cartel", 15, "Morg City"), "en los carteles de la ciudad", 2.8, "marcador cartel", x=.55, y=.38),
    mg_en(C.descifra("PRIVATE_EYE.gum", "DETECTIVE PRIVADO", "ARCHIVOS DEL JUEGO", "Nombre interno"), "En los archivos se llama", 3.6,
          "descifra private eye", x=.5, y=.30),
    mg_en(C.fallida("Chicle no encontrado", "Nunca llegó a salir"), "nunca llegó a salir", 2.2, "fallida chicle"),
    caso("se quedó sin caso", "sin_resolver", "Private Eye", "Nadie sabe qué hacía"),

    # ---------------- 29 · ¿muerto desde la primera misión?
    puesto("En el veintinueve", 29, "¿Muerto desde la primera misión?", "CAMPAÑA / BLACK OPS 3"),
    pv("Black Ops 3. En la primera misión", "c_bo3", "Black Ops 3 · 2015", dur=3.0, x=.18, y=.64, tam=320),
    pv("destrozado por un robot", "taylor", "John Taylor", dur=3.0, x=.80, y=.62, tam=330),
    ficha("brazos y piernas mecánicas", "Cirugía de combate", "Brazos y piernas *mecánicas*.", "INTEL / CAMPAÑA", dur=3.2),
    sil("Una teoría de los fans", "corvus", "Corvus", "La IA que te habla", lado="der", dur=3.8),
    rel("un bosque congelado", "frozen_forest", "Bosque congelado", "Vuelve una y otra vez", dur=3.6, x=.24, y=.55, tam=420),
    mg_en(C.balanza("¿Cuándo empieza el sueño?", [("En la 1.ª misión", None, "unos"), ("Al final", None, "otros"),
                                                   ("Nunca", None, "Treyarch")]), "ni los que la defienden", 4.0, "balanza sueño", y=.50),
    caso("el bosque estaba muy frío", "sin_resolver", "La teoría del sueño", "Treyarch nunca la confirmó"),

    # ---------------- 28 · Russman
    puesto("Número veintiocho", 28, "El viejo sin nombre", "ZOMBIES / TRANZIT / BLACK OPS 2"),
    leg("tranzit", "TRANZIT", ["Black Ops 2 · 2012", "Un autobús", "Lo conduce un robot"], de="TranZit, Black Ops 2", a=("y cuatro supervivientes", -.1)),
    pv("Un autobús que conduce un robot", "bus", "El autobús", dur=2.8, x=.18, y=.64, tam=320),
    aba([("misty", "Misty"), ("marlton", "Marlton"), ("stuhlinger", "Stuhlinger"), ("russman", "Russman")],
        de="cuatro supervivientes", a=("Ese anciano es", -.1), marcas=["Misty", "Marlton", "Stuhlinger", "un anciano"], nombre="victis",
        x=.66, y=.60, tam=260),
    sil("Ese anciano es Russman", "russman", "Russman", "Sin nombre de pila", lado="izq", dur=4.0),
    ficha("cada perk le cura una enfermedad", "Russman", "Cada perk le cura *una enfermedad*.", "INTEL / TRANZIT", dur=3.4, x=.73),
    mg_en(C.descifra("oldman", "EL VIEJO", "ARCHIVOS DEL JUEGO", "Así se llama en el código"), "se llama, simplemente", 3.4, "descifra oldman", y=.30),
    pv("Volvió en Black Ops 4", "c_bo4", "Black Ops 4", dur=2.8, x=.80, y=.62, tam=310),
    caso("para siempre como el viejo", "sin_resolver", "El nombre de Russman"),

    # ---------------- 27 · el fuego verde
    puesto("En el veintisiete", 27, "El fuego verde", "ZOMBIES / DEAD OF THE NIGHT / BLACK OPS 4"),
    rel("una mansión con vampiros", "dotn", "Dead of the Night", "Black Ops 4 · 2019", dur=3.4, x=.77, y=.52, tam=420),
    pv("Su arma maravilla", "alistair", "Alistair's Folly", dur=3.2, x=.18, y=.64, tam=330),
    mg_en(C.linea("La mejora del arma", [("1.ª", "Mejora", "fuego verde"), ("2.ª", "Mejora", "fuego azul")], h=400),
          "se mejora dos veces", 5.5, "linea mejoras", x=.5, y=.30),
    mg_en(C.objetivo("Enciende las chimeneas", "Con el fuego azul"), "sirve para encender las chimeneas", 3.2, "objetivo chimeneas", x=.30, y=.82),
    mg_en(C.fallida("Fuego verde", "No sirve para nada"), "no sirve para nada", 2.2, "fallida verde"),
    mg_en(C.marcador("Mausoleo", 30, "Batería sin uso"), "Cerca del mausoleo", 2.8, "marcador mausoleo", x=.55, y=.38),
    caso("se fue sin decir para qué", "sin_resolver", "El fuego verde", "Easter egg cancelado"),

    # ---------------- 26 · los retratos de Kino
    puesto("Número veintiséis", 26, "Los retratos en sombra", "ZOMBIES / KINO DER TOTEN / BLACK OPS"),
    rel("el teatro de Black Ops", "kino", "Kino der Toten", "Black Ops · 2010", dur=3.2, x=.77, y=.52, tam=420),
    mg(PE.abanico([(P("dempsey"), "Dempsey"), (P("nikolai"), "Nikolai"), (P("takeo"), "Takeo"), (P("richtofen"), "Richtofen")], 260, tema=TEMA),
       de="Dempsey, Nikolai", a=("Pero hay dos cuadros", -.1), marcas=["Dempsey", "Nikolai", "Takeo", "Richtofen"], nombre="ultimis", x=.32, y=.62),
    mg_en(C.contador(2, "CUADROS MÁS", "Kino der Toten"), "Pero hay dos cuadros", 2.6, "contador cuadros", x=.30, y=.30),
    mg_en(C.marcador("Cuadro en el suelo", 6, "Figura en sombra"), "tirado en el suelo", 2.8, "marcador cuadro", x=.55, y=.40),
    caso("un cuadro sin cara", "sin_resolver", "Los retratos en sombra", "Nadie ha dicho quién es"),

    # ---------------- 25 · la esfera del Golden Gate
    puesto("En el veinticinco", 25, "La esfera del Golden Gate", "ZOMBIES / MOB OF THE DEAD / BLACK OPS 2"),
    leg("motd", "MOB OF THE DEAD", ["Black Ops 2 · 2013", "Alcatraz · años 30", "4 gánsteres muertos"], de="Mob of the Dead: Alcatraz",
        a=("Desde el puente", -.1)),
    pv("Desde el puente", "golden_gate", "El Golden Gate", dur=3.0, x=.18, y=.64, tam=330),
    mg_en(C.marcador("Bola naranja", 900, "Sobre la bahía"), "hay una bola naranja", 3.2, "marcador bola", x=.62, y=.26),
    zoom("si miras al cielo", ("Treyarch nunca la explicó", -.1), 1.2, cy=-.2),
    rel("un foo fighter", "foo_fighter", "Foo fighter", "Segunda Guerra Mundial", dur=3.8, x=.77, y=.52, tam=420),
    caso("una farola muy ambiciosa", "sin_resolver", "La esfera naranja", "Treyarch nunca la explicó", dur=2.6),

    # ---------------- 24 · el ordenador de la CIA
    puesto("Número veinticuatro", 24, "El ordenador de la CIA", "MENÚ / BLACK OPS 2010"),
    pv("Black Ops, dos mil diez", "c_bo1", "Black Ops · 2010", dur=2.8, x=.80, y=.62, tam=320),
    mg_en(C.objetivo("Suéltate de la silla", "Pulsa los botones correctos"), "si pulsas los botones correctos", 3.2, "objetivo silla", x=.30, y=.82),
    ficha("un ordenador de la CIA", "CIA Data System", "Archivos secretos, *correos* y juegos escondidos.", "INTEL / TERMINAL", dur=3.6, x=.73),
    mg_en(C.codigo("3ARC", "COMANDO", "Acceso a la terminal"), "Escribes los comandos correctos", 3.0, "codigo terminal", x=.30, y=.30),
    muro([("dead_ops", "Dead Ops Arcade"), ("zork", "Zork")], de="Dead Ops Arcade", a=("El juego de guerra más", -.1),
         marcas=["Dead Ops Arcade", "Y Zork"], titulo="Juegos escondidos"),
    mg_en(C.logro("Comido por un grue", "Zork · dejarte devorar en la oscuridad"), "un trofeo por dejarte", 3.4, "logro grue", x=.5, y=.84),
    caso("Para el que se levantara", "resuelto", "El ordenador de la CIA", "Comandos documentados"),

    # ---------------- 23 · el libro de Dr Disrespect
    puesto("En el veintitrés", 23, "Un libro en una estantería", "CAMPAÑA / MODERN WARFARE 3 2011"),
    sil("Antes de ser Dr Disrespect", "drdisrespect", "Guy Beahm", "Dr Disrespect", lado="der", dur=3.8),
    pv("trabajó en Sledgehammer Games", "sledgehammer", "Sledgehammer Games", dur=3.0, x=.18, y=.64, tam=320),
    ficha("en la misión Tierra quemada", "Tierra quemada", "Modern Warfare 3 · *una librería*.", "INTEL / MW3 2011", dur=3.4),
    mg_en(C.marcador("Estante", 3, "Libro de Guy Beahm"), "en un estante, un libro", 3.0, "marcador libro", x=.55, y=.40),
    mg_en(C.contador(11, "AÑOS", "Sin que nadie lo viera"), "Once años ahí", 2.6, "contador once", x=.30, y=.30),
    mg_en(C.sello("1 DE ABRIL", "¿BROMA?"), "el día de las bromas", 2.4, "sello abril", x=.5, y=.46),
    caso("Hasta que el propio Doc", "verdad", "El libro de Guy Beahm", "Lo confirmó él mismo"),

    # ---------------- 22 · Shadowman / Nyarlathotep
    puesto("Número veintidós", 22, "El nombre del Hombre Sombra", "ZOMBIES / SHADOWS OF EVIL / BLACK OPS 3"),
    sil("es el Shadowman", "shadowman", "El Shadowman", "Shadows of Evil", lado="izq", dur=4.0),
    mg_en(C.descifra("TONY HALE RAPT", "NYARLATHOTEP", "ANAGRAMA", "Mismas letras, otro orden"), "Pon esas letras en otro orden", 4.2,
          "descifra nyarlathotep", y=.30),
    pv("los mitos de Lovecraft", "lovecraft", "H. P. Lovecraft", dur=3.0, x=.80, y=.62, tam=320),
    cam("el creador de Cthulhu", "cthulhu", "Cthulhu", dur=2.6, x=.16, y=.66),
    rel("un Apothicon", "apothicon", "Apothicon", "Dios del vacío", dur=3.4, x=.77, y=.52, tam=420),
    peg("en el expediente anterior, H.Hoster", "com_UgxrYkaGwQ3IKB7YjMF4AaABAg", "", dur=7.0, x=.36, y=.30, tam=760, giro=-2),
    mg_en(C.balanza("Shadows of Evil", [("El Easter egg", True, "tremendo"), ("La recompensa", False, "una tarjeta")]),
          "Y tiene razón", 3.6, "balanza tarjeta", y=.62),
    caso("para una tarjeta", "resuelto", "El anagrama", "Nyarlathotep, exacto", dur=2.6),

    # ---------------- 21 · aliens
    puesto("En el veintiuno", 21, "Los aliens de Call of Duty", "FINEST HOUR / BLACK OPS"),
    pv("Finest Hour, dos mil cuatro", "c_finesthour", "Finest Hour · 2004", dur=2.8, x=.80, y=.62, tam=320),
    mg_en(C.marcador("Platillo volante", 12, "Sótano secreto"), "un platillo volante nazi", 3.0, "marcador platillo", x=.55, y=.40),
    pv("en el Área cincuenta y uno", "area51", "Área 51", dur=3.0, x=.18, y=.64, tam=330),
    rel("Hangar dieciocho", "hangar18", "Hangar 18", "Black Ops · Annihilation", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.contador(4, "DEDOS", "Manos bajo la sábana"), "manos de cuatro dedos", 2.6, "contador dedos", x=.30, y=.30),
    mg_en(C.marcador("Mesa de autopsias", 4, "Con sangre"), "una mesa de autopsias", 3.0, "marcador autopsia", x=.55, y=.40),
    caso("tampoco les quitó la sábana", "sin_resolver", "Los aliens", "Nunca confirmados", dur=2.6),

    # ---------------- 20 · Ghosts
    puesto("Número veinte", 20, "La historia que se quedó colgada", "CAMPAÑA / GHOSTS 2013"),
    pv("Call of Duty Ghosts", "c_ghosts", "Ghosts · 2013", dur=2.8, x=.80, y=.62, tam=320),
    vs(("logan", "Logan"), ("rorke", "Rorke"), de="Logan pelea con Rorke", a=("Pero Rorke se levanta", -.1), marcas=["Logan", "Rorke"],
       ganador=1, titulo="La playa"),
    mg_en(C.radio("Rorke", "«Habrías sido un gran Ghost.»", "CAMPAÑA / FINAL"), "habrías sido un gran Ghost", 3.4, "radio rorke", y=.28),
    mg_en(C.fallida("Ghosts 2", "Nunca se hizo"), "Ghosts 2 nunca se hizo", 2.4, "fallida ghosts2"),
    mg_en(C.contador(13, "AÑOS", "Esperando"), "Trece años después, Logan", 2.6, "contador trece", x=.30, y=.30),
    pv("y Riley, el perro", "riley", "Riley", dur=3.0, x=.18, y=.64, tam=330),
    caso("si alguien lo va a contar", "sin_resolver", "Logan en manos de Rorke"),

    # ---------------- 19 · el dedo de Reznov
    puesto("En el diecinueve", 19, "El dedo de Reznov", "CAMPAÑA / BLACK OPS 2010"),
    sil("Viktor Reznov te acompaña", "reznov", "Viktor Reznov", "Black Ops · 2010", lado="der", dur=4.0),
    pv("murió en Vorkutá", "vorkuta", "Vorkutá", dur=2.8, x=.18, y=.64, tam=320),
    cam("una alucinación de Mason", "mason", "Alex Mason", dur=2.8),
    mg_en(C.marcador("Dedo índice", 0, "Mano derecha"), "le falta el dedo índice", 3.0, "marcador dedo", x=.55, y=.40),
    mg_en(C.balanza("¿El dedo de Reznov?", [("Pista escondida", None, "?"), ("Descuido de animación", None, "?")]),
          "Una pista escondida", 4.2, "balanza dedo", y=.50),
    pv("Black Ops 4 y en Black Ops 6", "c_bo6", "Black Ops 6", dur=2.8, x=.80, y=.62, tam=310),
    caso("Pero fuera de la historia", "sin_resolver", "El dedo de Reznov", dur=2.6),

    # ---------------- 18 · IX
    puesto("Número dieciocho", 18, "El concierto escondido", "ZOMBIES / IX / BLACK OPS 4"),
    rel("Nueve, el mapa del coliseo", "ix", "IX", "Black Ops 4 · 2018", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.objetivo("Dispara a los tambores", "En ciertas rondas"), "Si disparabas a los tambores", 3.0, "objetivo tambores", x=.30, y=.82),
    mg_en(C.contador(930, "DÍAS", "Sin que nadie supiera seguir"), "novecientos treinta días", 3.0, "contador 930", x=.30, y=.30),
    ficha("un modder publicó los scripts", "Scripts descompilados", "Abril de 2021 · *el código del juego*.", "INTEL / IX", dur=3.4),
    pv("golpear zombis con el escudo", "zombie_shield", "Escudo", dur=3.0, x=.18, y=.64, tam=320),
    caso("Lo resolvieron leyendo el código", "resuelto", "El concierto de IX", "Tardaron 930 días"),

    # ---------------- 17 · la calavera con escopetas
    puesto("En el diecisiete", 17, "La calavera con escopetas", "ZOMBIES / BLACK OPS 2"),
    pv("Black Ops 2 Zombies", "c_bo2", "Black Ops 2", dur=2.6, x=.80, y=.62, tam=310),
    mg_en(C.linea("Los emblemas de rango", [("1", "Un hueso", ""), ("2", "Dos huesos", ""), ("3", "Calavera", ""),
                                            ("4", "Con cuchillo", ""), ("5", "Con escopetas", "la más temida")], h=400),
          "un hueso, dos huesos", 6.0, "linea rangos", x=.5, y=.30),
    mg_en(C.fallida("Bajas", "No cuentan nada"), "Las bajas no cuentan nada", 2.2, "fallida bajas"),
    mg_en(C.contador(30, "HORAS", "Para las escopetas"), "unas treinta horas jugadas", 2.8, "contador horas", x=.30, y=.30),
    ficha("Las rayas de tiza", "Rayas de tiza", "Días *seguidos* jugando.", "INTEL / RANGO", dur=3.0),
    ficha("si la calavera tiene los ojos azules", "Ojos azules", "Jugaste en los *últimos 5 días*.", "INTEL / RANGO", dur=3.2, x=.73),
    caso("Sin saber qué significaba", "resuelto", "La calavera", "Más de 10 años después", dur=2.6),

    # ---------------- 16 · Alex
    puesto("Número dieciséis", 16, "Alex murió… hasta que no", "CAMPAÑA / MODERN WARFARE 2019"),
    pv("Modern Warfare, dos mil diecinueve", "c_mw2019", "Modern Warfare · 2019", dur=2.8, x=.80, y=.62, tam=320),
    sil("Alex se queda atrás", "alex", "Alex", "Se queda atrás", lado="izq", dur=4.0),
    mg_en(C.fallida("Detonador", "No funciona"), "el detonador falla", 2.2, "fallida detonador"),
    cam("junto a Ghost", "ghost_mw19", "Ghost", dur=2.8, x=.84, y=.66),
    ficha("con una pierna de metal", "Temporada 3", "Abril de 2020 · *vivo*, con pierna de metal.", "INTEL / MW 2019", dur=3.4),
    caso("El rumor era verdad", "verdad", "Alex vive", "Le costó una pierna", dur=3.0),

    # ---------------- 15 · Pawn Takes Pawn
    puesto("En el quince", 15, "Las cintas de Pawn Takes Pawn", "ARG / WARZONE 2020"),
    pv("proyectores de diapositivas", "proyector", "Proyector", dur=3.0, x=.18, y=.64, tam=320),
    rel("Pawn Takes Pawn", "pawn", "Pawn Takes Pawn", "Agosto de 2020", dur=3.2, x=.77, y=.52, tam=420),
    pv("una cinta VHS nueva", "vhs", "Cinta VHS", dur=2.8, x=.80, y=.62, tam=300),
    mg_en(C.codigo("2608", "CÓDIGO", "Puertas de Verdansk"), "Esos códigos abrían puertas", 3.2, "codigo puertas", x=.30, y=.30),
    mg_en(C.contador(26, "DE AGOSTO", "La fecha"), "veintiséis de agosto", 2.4, "contador agosto", x=.62, y=.30),
    rel("Black Ops Cold War", "c_bocw", "Black Ops Cold War", "Revelado en Warzone", dur=3.4, x=.24, y=.55, tam=420),
    caso("Lo desenterraron los jugadores", "resuelto", "Pawn Takes Pawn", "ARG completado"),

    # ---------------- 14 · Warzone antes de Warzone
    puesto("Número catorce", 14, "Warzone existía antes de existir", "FILTRACIÓN / MODERN WARFARE 2019"),
    ficha("un dataminero, Senescallo", "Senescallo", "Noviembre de 2019 · *battle royale* en los archivos.", "INTEL / FILTRACIÓN", dur=3.6),
    mg_en(C.descifra("BR_DUOS / BR_QUADS", "WARZONE", "ARCHIVOS", "Listas de dúos y cuartetos"), "Archivos con el nombre Warzone", 3.6,
          "descifra warzone", y=.30),
    mg_en(C.fallida("Cuenta cerrada", "Activision"), "Activision le cierra la cuenta", 2.4, "fallida cuenta"),
    rel("salió Warzone, gratis", "c_warzone", "Warzone", "10 de marzo de 2020", dur=3.6, x=.77, y=.52, tam=440),
    caso("lo escribió el propio juego", "verdad", "La filtración de Warzone", "Fecha exacta"),

    # ---------------- 13 · búnker 11
    puesto("En el trece", 13, "El búnker once", "WARZONE / VERDANSK 2020"),
    pv("Un búnker cerrado", "bunker11", "Búnker 11", dur=3.0, x=.80, y=.62, tam=330),
    mg_en(C.radio("Teléfono", "Una voz en ruso dicta números…", "VERDANSK / LÍNEA 11"), "una voz en ruso dicta", 4.4, "radio ruso", y=.28),
    mapa("verdansk", [(.17, .22, "La presa"), (.48, .66, "El hospital"), (.74, .27, "La cantera")],
         de="Cada número es otro teléfono", a=("Los llamas en orden", 1.5), marcas=["el nueve", "El ocho", "El tres"],
         titulo="Verdansk", sub="Los teléfonos, en orden", entrada="mesa"),
    mg_en(C.codigo("983", "LLAMADA", "En orden"), "Los llamas en orden", 2.6, "codigo telefonos", x=.30, y=.30),
    pv("un plano secreto del MP7", "mp7", "MP7", dur=3.0, x=.18, y=.64, tam=320),
    caso("con una guía telefónica", "resuelto", "El búnker 11", "Abierto en 2020", dur=2.6),

    # ---------------- 12 · Blundell en Morse
    puesto("Número doce", 12, "El director que parpadeaba en Morse", "ZOMBIES / TREYARCH 2016"),
    sil("Jason Blundell, el director", "blundell", "Jason Blundell", "Director de Zombies", lado="der", dur=4.0),
    pv("Tres usuarios de Reddit", "reddit", "Reddit", dur=2.8, x=.18, y=.64, tam=300),
    mg_en(C.descifra("-. --- / .---- .---- .....", "NO PONGAS 115", "CÓDIGO MORSE", "Los parpadeos"), "no pongas ciento quince", 3.8,
          "descifra morse", y=.30),
    cam("Confía en mí, Sam", "samantha", "Sam", dur=2.6, x=.84, y=.66),
    mg_en(C.balanza("¿Mensaje o casualidad?", [("El cerebro busca patrones", True, "casi seguro"), ("Sabía Morse", None, "?")]),
          "Casi seguro es casualidad", 4.6, "balanza morse", y=.62),
    caso("Nunca dijo si quiso", "sin_resolver", "El Morse de Blundell", dur=2.6),

    # ---------------- 11 · la voz de Samantha
    puesto("En el once", 11, "La voz de Samantha", "ZOMBIES / ORIGINS / BLACK OPS 2"),
    leg("origins", "ORIGINS", ["Agosto de 2013", "Cinemática de presentación"], de="Treyarch estrena la cinemática", a=("suena así", -.1)),
    vs(("samantha", "21 de agosto"), ("samantha", "23 de agosto"), de="Dos días después", a=("De una voz grave", 2.0),
       marcas=["Dos días después", "De una voz grave"], titulo="La misma frase"),
    mg_en(C.contador(2, "DÍAS", "Lo que tardó el cambio"), "cambió de voz en dos días", 2.6, "contador dos dias", x=.30, y=.30),
    caso("preguntarle por qué", "sin_resolver", "La voz de Samantha", "Nunca explicado", dur=2.6),

    # ---------------- 10 · la cara de Alcatraz
    puesto("Número diez", 10, "La cara de Alcatraz", "ZOMBIES / MOB OF THE DEAD / BLACK OPS 2"),
    mg_en(C.objetivo("Apunta a los fuegos artificiales", "Desde la azotea"), "apuntas con un francotirador", 3.4, "objetivo fuegos", x=.30, y=.82),
    pant("cara_motd", "Una cara deformada", ("durante una fracción", 1.6), zoom=(1.0, 1.15)),
    muro([("russman", "¿Russman?"), ("nero", "¿Nero?"), ("samantha", "¿Samantha?")], de="El viejo Russman", a=("Treyarch nunca lo dijo", .4),
         marcas=["Russman", "Nero", "Samantha"], titulo="¿De quién es la cara?"),
    caso("Y sigue sin nombre", "sin_resolver", "La cara de Alcatraz", "13 años después"),

    # ---------------- 9 · el corazón
    puesto("En el nueve", 9, "El corazón del castillo", "ZOMBIES / DER EISENDRACHE / BLACK OPS 3"),
    rel("un castillo nevado en los Alpes", "der_eisendrache", "Der Eisendrache", "Black Ops 3 · 2016", dur=3.6, x=.77, y=.52, tam=440),
    pv("y dragones", "dragon", "Dragón", dur=2.6, x=.18, y=.64, tam=320),
    mg_en(C.linea("La receta", [("R2", "Barricadas", "que las rompan"), ("2", "Tablas", "en cada una"), ("RK5", "Compra", "+2 tablas"),
                                ("Shiva", "Cambia", "+1 tabla"), ("5 s", "Patio", "abre la puerta")], h=420),
          "En la ronda dos", 13.0, "linea receta", x=.5, y=.30),
    pv("Compra la RK5", "rk5", "RK5", dur=2.4, x=.80, y=.66, tam=280),
    pv("cámbiala por la Shiva", "shiva", "Sheiva", dur=2.4, x=.80, y=.66, tam=280),
    mg_en(C.logro("Homenaje", "Drew Marlowe · a su esposa y a su hijo"), "Un homenaje de Drew Marlowe", 4.0, "logro corazon", x=.5, y=.84),
    caso("no estaba hecho para nosotros", "resuelto", "El corazón", "3 años y medio después"),

    # ---------------- 8 · Spectre
    puesto("Número ocho", 8, "Spectre", "ESPECIALISTA / BLACK OPS 3"),
    sil("Un especialista con máscara", "spectre", "Spectre", "Especialista", lado="der", dur=4.0),
    leg("spectre", "SPECTRE", ["Nombre real: DESCONOCIDO", "Nacimiento: DESCONOCIDO", "Género: DESCONOCIDO"],
        de="Nombre real: desconocido", a=("Volvió en Black Ops 4", -.1),
        marcas=["Nombre real", "Fecha y lugar", "casilla de género"], sello=("DESCONOCIDO", 2), x=.30, y=.52),
    pv("Black Ops 7 y a Warzone", "c_bo7", "Black Ops 7", dur=3.0, x=.80, y=.62, tam=310),
    mg_en(C.contador(11, "AÑOS", "Con la máscara"), "Once años en la saga", 2.6, "contador spectre", x=.30, y=.30),
    caso("la máscara sigue puesta", "sin_resolver", "¿Quién es Spectre?", dur=2.6),

    # ---------------- 7 · las voces del cementerio
    puesto("En el siete", 7, "Las voces del cementerio", "MULTIJUGADOR / MODERN WARFARE 3"),
    rel("Sanctuary, Modern Warfare 3", "sanctuary", "Sanctuary", "Modern Warfare 3 · 2011", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.marcador("Parches de césped", 2, "Cementerio"), "los parches de césped", 3.0, "marcador cesped", x=.55, y=.40),
    ficha("Una niña. Y su padre", "Sanctuary", "Se oye… *y no hay nadie*.", "INTEL / AUDIO", dur=3.0),
    rel("la familia Davis", "davis", "Davis Family Vacation", "Campaña de MW3", dur=3.6, x=.24, y=.55, tam=420),
    cam("La niña se llama Sarah", "sarah", "Sarah Davis", dur=3.0, x=.84, y=.66),
    caso("la dejó ahí, jugando", "resuelto", "Las voces del cementerio", "Audio de la campaña", dur=2.6),

    # ---------------- 6 · el mensaje de amor
    puesto("Número seis", 6, "El mensaje de amor perdido", "MULTIJUGADOR / CALL OF DUTY 3"),
    pv("Call of Duty 3", "c_cod3", "Call of Duty 3", dur=2.6, x=.80, y=.62, tam=310),
    rel("Ironclad, un mapa descargable", "ironclad", "Ironclad", "Solo Xbox 360 · 2007", dur=3.4, x=.24, y=.55, tam=420),
    pv("solo para Xbox 360", "xbox360", "Xbox 360", dur=2.6, x=.80, y=.64, tam=280),
    mg_en(C.radio("Jason McCord", "«Estoy como 90 % seguro de que lo hice.»", "TUIT DEL PROGRAMADOR / 2021"), "estoy como noventa por ciento", 3.8,
          "radio mccord", y=.28),
    mg_en(C.contador(2, "PEDIDAS DE MANO", "Sin descubrir"), "pedidas de mano secretas", 2.8, "contador pedidas", x=.30, y=.30),
    mg_en(C.marcador("Juliana", 20, "Nombre en un barco"), "Encontró un nombre en un barco", 3.2, "marcador juliana", x=.55, y=.40),
    caso("Y el más maldito", "sin_resolver", "El mensaje de Ironclad", "19 años escondido"),

    # ---------------- 5 · el fantasma de Vacant
    puesto("En el cinco", 5, "El fantasma de Vacant", "MULTIJUGADOR / CALL OF DUTY 4"),
    pv("el mapa de oficinas abandonadas", "vacant", "Vacant", dur=3.0, x=.18, y=.64, tam=330),
    pv("Call of Duty 4. Una figura", "c_cod4", "Call of Duty 4", dur=2.6, x=.80, y=.62, tam=310),
    mg_en(C.fallida("Objetivo", "No se le puede matar"), "no se le puede matar", 2.4, "fallida fantasma"),
    mg_en(C.contador(500000, "VISTAS", "Agosto de 2008", desde=0), "Más de medio millón", 2.8, "contador vistas", x=.30, y=.30),
    pv("otro fantasma en Backlot", "backlot", "Backlot", dur=2.8, x=.80, y=.62, tam=310),
    mg_en(C.balanza("Pruebas del montaje", [("El marcador cambia", False, "corte"), ("Dice sin editar", False, "editado"),
                                            ("Tiene gamertag", False, "jugador")]), "El marcador cambia", 5.0, "balanza montaje", y=.50),
    caso("tenía gamertag", "falso", "El fantasma de Vacant", "Era un montaje", dur=2.8),

    # ---------------- 4 · ADFGX
    puesto("Número cuatro", 4, "El cifrado de Alcatraz", "ZOMBIES / MOB OF THE DEAD / BLACK OPS 2"),
    pant("adfgx_pantalla", "En la pantalla de carga", ("Es el cifrado que usaba", 2.0), zoom=(1.0, 1.12)),
    ficha("Es el cifrado que usaba Alemania", "ADFGX", "Alemania · *Primera Guerra Mundial*.", "INTEL / CIFRADO", dur=3.4),
    mg_en(C.descifra("XAGDF FXDAG", "ZOMBIE", "CLAVE", "No salía nada"), "la palabra zombie. Pero no salía", 3.0, "descifra clave", y=.30),
    mg_en(C.fallida("Solución falsa", "El cómic de 2017"), "Hubo una solución falsa", 2.4, "fallida comic"),
    pv("un usuario de Reddit lo logró", "reddit", "Reddit · 2018", dur=3.0, x=.80, y=.62, tam=300),
    mg_en(C.descifra("ADFGX ADFGX FGXAD", "EL GIGANTE ESTÁ EN FRANCIA", "MENSAJE", "Urgente"), "El mensaje, en alemán", 5.0,
          "descifra gigante", y=.30),
    rel("un robot gigante, en la Francia", "robot_origins", "Origins", "Francia · 1918", dur=3.6, x=.77, y=.52, tam=440),
    caso("nadie lo leyó a tiempo", "resuelto", "El cifrado ADFGX", "5 años después", dur=2.8),

    # ---------------- 3 · Kennedy
    puesto("Número tres", 3, "¿Alex Mason mató a Kennedy?", "CAMPAÑA / BLACK OPS 2010"),
    tabl([("mason", "Mason"), ("dragovich", "Dragovich"), ("reznov", "Reznov"), ("jfk", "Kennedy")],
         [(1, 0), (2, 0), (0, 3)], de="Dragovich programa a Mason", a=("En el Pentágono", -.1),
         marcas=["Dragovich", "Mason", "Reznov altera", "Reznov altera"], titulo="La programación"),
    sil("Mason se imagina apuntándole", "jfk", "John F. Kennedy", "Presidente de EE. UU.", lado="der", dur=3.8),
    cam("mientras Hudson le dice", "hudson", "Jason Hudson", dur=3.0),
    rel("Dallas, veintidós", "dealey", "Dealey Plaza", "Dallas · 22-nov-1963", dur=3.8, x=.77, y=.52, tam=420),
    mg_en(C.marcador("¿Mason?", 40, "Entre la multitud"), "alguien que se parece a Mason", 3.0, "marcador multitud", x=.5, y=.38),
    caso("sin cerrar el expediente", "sin_resolver", "Mason y Kennedy", "Nunca confirmado"),

    # ---------------- 2 · el Easter egg imposible
    puesto("En el dos", 2, "El Easter egg imposible", "ZOMBIES / BLACK OPS 3"),
    cam("Jason Blundell, otra vez él", "blundell", "Blundell", dur=3.0),
    mg_en(C.objetivo("Uno que no podrán romper", "Black Ops 3 · 2015"), "promete meter en Black Ops 3", 3.4, "objetivo imposible", x=.30, y=.82),
    mg_en(C.balanza("Lo que sacaron los datamineros", [("El corazón", True, "sí"), ("Todo lo demás", True, "sí"), ("El imposible", False, "no")]),
          "Los datamineros abrieron", 4.6, "balanza datamineros", y=.50),
    mg_en(C.radio("Blundell", "«La pista está en el nombre.»", "RESPUESTA / 2023"), "la pista está en el nombre", 3.4, "radio pista", y=.28),
    pv("en el mapa The Giant", "the_giant", "The Giant", dur=2.8, x=.80, y=.62, tam=310),
    pv("un rifle dentro de un teseracto", "kn44", "KN-44", dur=2.8, x=.18, y=.64, tam=300),
    caso("sigue cumpliendo su promesa", "sin_resolver", "El imposible", "11 años después"),

    # ---------------- 1 · el hombre de traje
    puesto("Y el número uno", 1, "El hombre de traje", "CAMPAÑA / MODERN WARFARE 3 2011"),
    vs(("price", "Price"), ("makarov", "Makárov"), de="Price mata a Makárov", a=("se sienta en la azotea", .2), marcas=["Price", "Makárov"],
       ganador=0, titulo="Dubái"),
    pv("en el hotel de Dubái", "hotel_oasis", "Hotel Oasis", dur=2.8, x=.80, y=.62, tam=310),
    ficha("dos modders restauraron una escena", "Escena cortada", "Mayo de 2024 · *restaurada* por modders.", "INTEL / MW3 2011", dur=3.6),
    mg_en(C.marcador("Hombre de traje", 15, "Sin diálogo · sin nombre"), "un hombre de traje, en la penumbra", 3.4, "marcador traje", x=.5, y=.36),
    mg_en(C.descifra("anim_shadowman_enter", "SHADOWMAN ENTRA", "ARCHIVOS", "Nombre de la animación"), "sus animaciones se llaman así", 3.6,
          "descifra shadowman", y=.30),
    vs(("shadowman", "MW3 · 2011"), ("nero", "Shadows of Evil"), de="no es el mago de Zombies", a=("Infinity Ward nunca lo ha", -.1),
       marcas=["no es el mago"], titulo="Mismo nombre, no el mismo"),
    mg_en(C.contador(15, "AÑOS", "En el disco de MW3"), "Quince años dentro del disco", 2.8, "contador quince", x=.30, y=.30),
    caso("esperando a que alguien le", "sin_resolver", "El hombre de traje", "Nadie sabe quién es", dur=3.4),

    # ---------------- cierre
    mg_en(C.sello("EXPEDIENTE CERRADO", "141"), "Expediente cerrado", 2.4, "sello cerrado", x=.5, y=.46),
    mg_en(C.balanza("Treinta misterios", [("Resueltos leyendo el código", True, "unos"), ("Todavía abiertos", False, "otros")]),
          "Treinta misterios: unos resueltos", 4.0, "balanza cierre", y=.50),
    mg_en(C.objetivo("¿Cuál se resuelve primero?", "Dímelo en los comentarios"), "Dímelo en los comentarios", 3.2, "objetivo comentarios", x=.30, y=.82),
    peg("Y a LDVader", "com_UgyYYiuB4qw9-ODBi454AaABAg", "", dur=7.5, x=.36, y=.30, tam=760, giro=2),
    mg_en(C.sello("TRAMPA", "PRESS F"), "Trampa es que te pidan", 2.4, "sello trampa", x=.75, y=.62),
    pv("los efectos Mandela de Call of Duty", "c_bo2", "20 efectos Mandela", dur=3.0, x=.18, y=.64, tam=310),
    pv("los veinticinco secretos", "c_mw2019", "25 secretos de MW4", dur=3.0, x=.80, y=.62, tam=310),
    mg_en(C.objetivo("Suscríbete", "El siguiente expediente"), "suscríbete", 3.2, "objetivo suscribete", x=.30, y=.82),
    mg_en(C.sello("RETÍRATE, SOLDADO", "EXPEDIENTE 141"), "Retírate, soldado", 3.0, "sello retirate", x=.5, y=.46),
]

ROTULOS = [
    dict(texto="MIRA BIEN", en="Mira bien", tam=150, color="amarillo", y=.22, dur=1.6),
    dict(texto="DETECTIVE PRIVADO", en="detective privado", tam=110, color="amarillo", y=.22, dur=2.0),
    dict(texto="OLDMAN", en="oldman: el viejo", tam=150, color="amarillo", y=.22, dur=2.0),
    dict(texto="NO SIRVE PARA NADA", en="el fuego verde no sirve", tam=110, color="amarillo", y=.22, dur=2.2),
    dict(texto="UN CUADRO SIN CARA", en="un cuadro sin cara", tam=110, color="amarillo", y=.22, dur=2.0),
    dict(texto="NYARLATHOTEP", en="Nyarlathotep. El dios", tam=130, color="amarillo", y=.22, dur=2.2),
    dict(texto="NUNCA SE HIZO", en="Ghosts 2 nunca se hizo", tam=130, color="amarillo", y=.22, dur=2.0),
    dict(texto="930 DÍAS", en="novecientos treinta días", tam=150, color="amarillo", y=.22, dur=1.8),
    dict(texto="LEYENDO EL CÓDIGO", en="Lo resolvieron leyendo", tam=110, color="amarillo", y=.22, dur=2.2),
    dict(texto="ERA VERDAD", en="El rumor era verdad", tam=140, color="amarillo", y=.22, dur=1.8),
    dict(texto="UNA GUÍA TELEFÓNICA", en="con una guía telefónica", tam=110, color="amarillo", y=.22, dur=2.2),
    dict(texto="DESCONOCIDO", en="en la casilla de género", tam=140, color="amarillo", y=.22, dur=2.0),
    dict(texto="NO HAY NADIE", en="Pero no hay nadie", tam=140, color="amarillo", y=.22, dur=2.0),
    dict(texto="JULIANA", en="en un barco: Juliana", tam=160, color="amarillo", y=.22, dur=2.0),
    dict(texto="ERA UN MONTAJE", en="Era un montaje", tam=130, color="amarillo", y=.22, dur=2.0),
    dict(texto="EL GIGANTE ESTÁ EN FRANCIA", en="El gigante está en Francia", tam=96, color="amarillo", y=.22, dur=2.6),
    dict(texto="ES IMPOSIBLE", en="Es imposible", tam=150, color="amarillo", y=.22, dur=1.8),
    dict(texto="SIN NOMBRE", en="Sin diálogo. Sin nombre", tam=150, color="amarillo", y=.22, dur=2.0),
]

SFX = {}
# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/cod/ → sfx/cod_*.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_puesto", en="Número treinta", vol=.24),
    dict(sfx="cod_fallida", en="nunca llegó a salir", vol=.26),
    dict(sfx="cod_puesto", en="En el veinticinco", vol=.22),
    dict(sfx="cod_logro", en="un trofeo por dejarte", vol=.28),
    dict(sfx="cod_radio", en="habrías sido un gran Ghost", vol=.22),
    dict(sfx="cod_puesto", en="Número veinte", vol=.22),
    dict(sfx="cod_puesto", en="En el quince", vol=.22),
    dict(sfx="cod_radio", en="una voz en ruso dicta", vol=.20),
    dict(sfx="cod_sello", en="Número diez", vol=.24),
    dict(sfx="cod_logro", en="Un homenaje de Drew Marlowe", vol=.28),
    dict(sfx="cod_puesto", en="En el cinco", vol=.22),
    dict(sfx="cod_fallida", en="Era un montaje", vol=.26),
    dict(sfx="cod_radio", en="la pista está en el nombre", vol=.22),
    dict(sfx="cod_puesto", en="Y el número uno", vol=.26),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_chillido", en=("Mira bien|fin", .15), vol=1.0, voz=True),
    dict(sfx="s_chillido", en=("con un chillido|fin", .05), vol=.55, voz=True),
    dict(sfx="s_riff", en="sonaba esto|fin", vol=1.0, voz=True),
    dict(sfx="s_ruso", en="dicta números|fin", vol=1.0, voz=True),
    dict(sfx="s_sam1", en="Samantha, suena así|fin", vol=1.0, voz=True),
    dict(sfx="s_sam2", en="la misma frase suena así|fin", vol=1.0, voz=True),
    dict(sfx="s_sanct", en="se oye esto|fin", vol=1.0, voz=True),
]

# ---- 2.ª pasada (chequeo 10-nov: pegatinas 3,5/min contra 5,6 del canal; fichas 0,6 contra 1,4)
_I, _D = dict(x=.18, y=.64, tam=300), dict(x=.80, y=.62, tam=300)
FX += [
    pv("Pero en los carteles", "soe", "Morg City", **_I), pv("Nadie sabe qué hacía", "gobblegum", "¿Qué hacía?", **_D),
    cam("dentro de la mente de tu personaje", "taylor", "Taylor"), pv("Treyarch nunca la confirmó", "treyarch", "Treyarch", **_D),
    pv("y la historia de su grupo se cerró", "tranzit", "Victis", **_I),
    pv("hay salas de un Easter egg", "dotn", "Dead of the Night", **_D), cam("el fuego de las trampas", "alistair", "El arma"),
    pv("Nadie ha dicho quién es", "kino", "Kino der Toten", **_D), cam("Cuatro gánsteres muertos", "motd", "Los gánsteres"),
    pv("El juego de guerra más vendido", "c_bo1", "Black Ops · 2010", **_D),
    pv("medio internet pensó que era broma", "drdisrespect", "Dr Disrespect", **_I),
    pv("Y en la ciudad se hace llamar", "soe", "Morg City", **_D), pv("Más adelante sale otro", "shadowman", "¿Otro?", **_I),
    cam("tres cuerpos bajo sábanas", "hangar18", "Hangar 18"), pv("Call of Duty nunca confirmó", "area51", "Área 51", **_D),
    pv("arrastra a Logan herido", "rorke", "Rorke", **_I), pv("Logan sigue en manos", "logan", "Logan", **_D),
    pv("Al Reznov real", "reznov", "El Reznov real", **_I), pv("O un descuido de animación", "c_bo1", "Black Ops", **_D),
    pv("Y ahí estaba el resto", "ix", "Los scripts", **_D),
    pv("Treyarch nunca explicó cómo se subía", "treyarch", "Treyarch", **_D), pv("un modder lo sacó del código", "reddit", "El modder", **_I),
    pv("La explosión", "alex", "Alex", **_D), pv("Muchos sospechaban", "ghost_mw19", "Ghost", **_I),
    pv("una oficina a oscuras", "pawn", "La oficina", **_I), pv("transmisiones de la Guerra Fría", "c_bocw", "Guerra Fría", **_D),
    pv("Modern Warfare lleva un mes", "c_mw2019", "Modern Warfare", **_I), pv("Y después, el mapa entero", "verdansk", "Verdansk", **_D),
    pv("Verdansk, Warzone", "verdansk", "Verdansk", **_I), pv("La puerta más blindada", "bunker11", "Búnker 11", **_D),
    pv("Y salen frases", "morse", "Código Morse", **_D), pv("Contacta al doctor", "richtofen", "¿El doctor?", **_I),
    cam("a una niña estadounidense", "samantha", "Samantha"),
    pv("Mob of the Dead, dos mil trece", "motd", "Mob of the Dead", **_D), pv("Subes a la azotea", "alcatraz", "La azotea", **_I),
    pv("la comunidad leyó el código", "reddit", "La comunidad", **_I), pv("con arcos de fuego", "wrath", "Arco de fuego", **_I),
    pv("una espada", "ripper", "Ripper", **_I), pv("con su propia operación", "c_bo4", "Black Ops 4", **_D),
    pv("Esas voces son de la campaña", "c_mw3_2011", "Modern Warfare 3", **_D), pv("Infinity Ward escondió", "infinityward", "Infinity Ward", **_I),
    pv("Su diseñador, Jason McCord", "ironclad_mapa", "Ironclad", **_D), pv("un youtuber lo buscó", "ironclad", "Ironclad", **_I),
    pv("Secuelas", "vacant", "Vacant", **_I),
    pv("Mob of the Dead, abril", "motd", "Mob of the Dead", **_D), pv("Era el anuncio de Origins", "origins", "Origins", **_I),
    pv("En Vorkutá, Dragovich", "vorkuta", "Vorkutá", **_I), pv("Treyarch metió a su protagonista", "mason", "Mason", **_D),
    pv("Encontraron el corazón", "der_eisendrache", "El corazón", **_I), pv("títulos de libros", "der_eisendrache", "Der Eisendrache", **_D),
    pv("Pero en mayo de dos mil veinticuatro", "c_mw3_2011", "Modern Warfare 3", **_I), pv("Price, desplomado", "price", "Price", **_D),
]
FX += [
    ficha("Se descubrió a finales", "Private Eye", "Descubierto a *finales de 2015*.", "INTEL / ARCHIVOS"),
    ficha("un final que nadie termina", "El final", "Nadie lo *termina de entender*.", "INTEL / CAMPAÑA"),
    ficha("Pero nunca se dijo su nombre", "Russman", "Apellido, *no nombre*.", "INTEL / VICTIS"),
    ficha("Dead of the Night, Black Ops 4", "Dead of the Night", "Mansión · *vampiros y hombres lobo*.", "INTEL / BLACK OPS 4"),
    ficha("Y cada uno comenta el suyo", "Retratos", "Cada personaje *comenta el suyo*.", "INTEL / KINO"),
    ficha("Cuatro gánsteres muertos", "Mob of the Dead", "4 gánsteres *intentan escapar*.", "INTEL / ALCATRAZ"),
    ficha("En el menú principal", "Menú principal", "Atado a *la silla del interrogatorio*.", "INTEL / BLACK OPS"),
    ficha("diseñando niveles", "Guy Beahm", "Diseñador de niveles · *Sledgehammer*.", "INTEL / MW3 2011"),
    ficha("Seis años después, Black Ops", "Hangar 18", "Mapa del DLC *Annihilation* · 2011.", "INTEL / BLACK OPS"),
    ficha("lavarle el cerebro", "El plan de Rorke", "Convertir a Logan en *uno de los suyos*.", "INTEL / GHOSTS"),
    ficha("Y el Reznov que ve Mason", "El dedo", "El Reznov de Mason *lo tiene*.", "INTEL / BLACK OPS"),
    ficha("Al final, un concierto de rock", "Concierto", "Un concierto *en el coliseo*.", "INTEL / IX"),
    ficha("Activision lo sacó como operador", "Alex", "Operador jugable · *Temporada 3*.", "INTEL / MW 2019"),
    ficha("Las pistas llevan a una web", "La web", "Oficina a oscuras · *tele vieja*.", "INTEL / ARG"),
    ficha("Los filtradores dijeron", "La fecha", "Filtrado: *principios de marzo*.", "INTEL / FILTRACIÓN"),
    ficha("Dentro: cabezas nucleares", "Búnker 11", "Cabezas *nucleares* + plano del MP7.", "INTEL / VERDANSK"),
    ficha("Blundell le contó al entrevistador", "Blundell", "Sabía Morse · *lo bastante*.", "INTEL / ENTREVISTA"),
    ficha("Está documentada", "La cara", "Documentada · *sin identidad*.", "INTEL / MOB OF THE DEAD"),
    ficha("Tres años y medio escondido", "Der Eisendrache", "Encontrado en *julio de 2019*.", "INTEL / BLACK OPS 3"),
    ficha("Jesse Snider, el creador", "Jesse Snider", "Creador del modo *Zombies*.", "INTEL / TREYARCH"),
    ficha("Nueve de agosto de dos mil ocho", "El video", "9 de agosto de 2008 · *«sin editar»*.", "INTEL / YOUTUBE"),
    ficha("Ni Black Ops 2 ni Cold War", "Black Ops", "Ni BO2 ni Cold War *lo aclararon*.", "INTEL / CAMPAÑA"),
    ficha("Blundell dejó Treyarch", "Jason Blundell", "Dejó Treyarch · *sin redes sociales*.", "INTEL / TREYARCH"),
    ficha("Infinity Ward nunca lo ha explicado", "Infinity Ward", "Nunca *lo explicó*.", "INTEL / MW3 2011"),
]

# Cortes rápidos del gancho con clips ya bajados (debajo de todo lo demás)
VIDEOS = [
    vid(102, "Una voz que Treyarch cambió", ("Un fantasma sin arma", -.1), desde=1.0),     # cinemática de Origins
    vid(135, "Un fantasma sin arma", ("Un corazón escondido", -.1), desde=0.5),           # el fantasma de Vacant
    vid(116, "Un corazón escondido", ("Un platillo volante", -.1), desde=1.0),            # el corazón de Der Eisendrache
    vid(161, "Y un hombre de traje", ("Treinta misterios", -.1), desde=1.0),              # la figura de traje
]
FX = VIDEOS + FX
