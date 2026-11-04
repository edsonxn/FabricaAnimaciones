# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 EFECTOS MANDELA más raros de Call of Duty» (SECUENCIA YT, Expediente 141, 3-nov-2026).
Helpers copiados de videos/cod_mw4_secretos/efectos.py (kit nucleo/mg_cod.py + peg_estilos con tema «cod»).
MG propio de este guion: `mandela()` = espejo «LO QUE RECUERDAS / LO QUE ES». Portadas de BO2/BO1 a pantalla con `pant()`.
Sonidos nombrados (regla 31-oct-2026): PISTAS voz=True con sfx/s_*.mp3 (audio/cortes/_cortar.py).
    python fab.py cod_mandela fx --seco   tiempos      python fab.py cod_mandela fx hoja   previews/fx_NN.jpg
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
TEMA_MAPA = "gaming"


def P(slug):
    for e in (".png", ".jpg", ".webp"):
        r = os.path.join(_PEG, slug + e)
        if os.path.exists(r):
            return r
    return os.path.join(_PEG, slug + ".png")


def ficha(en, titulo, texto, tipo=None, dur=5.0, x=_FX, y=_FY, ancho=880):
    return dict(tipo="mg", fn=C.ficha(titulo, texto, tipo, ancho=ancho), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + titulo, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.64, tam=400, giro=-5.0):
    """Pegatina con la imagen REAL de lo que nombra la voz: abajo a la izquierda."""
    return dict(tipo="mg", fn=C.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.27, tam=640):
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.78, y=.52, ancho=500, giro=3.5):
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.64, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla " + slug, ver=2.0)


def puesto(en, n, titulo, sub, dur=4.5):
    return dict(tipo="mg", fn=C.puesto(n, titulo, sub, total=20), en=en, dur=dur, x=.5, y=.80, sale=.4, nombre=f"puesto {n}", ver=1.4)


def mg(fn, de, a, marcas, nombre, x=.5, y=.52):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    """Acercamiento lento de cámara sobre el clip (3-nov-2026: más animación en los tramos sin apoyo)."""
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def vid(n, de, a, desde=0.0, recorte=0.0):
    """Corte rápido con OTRO clip ya bajado del video (medios/scene-NNN.mp4) a cuadro entero, para que el gancho cambie de
    plano cada 1-3 s sin renumerar los beats (3-nov-2026). Van PRIMERO en FX: se dibujan debajo de MG y pegatinas."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                recorte=recorte, entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


def mandela(titulo, izq, der, de, a, nombre, centro="EFECTO MANDELA", marcas=None):
    """Espejo «LO QUE RECUERDAS / LO QUE ES» (MG propio de este guion): izq = el recuerdo, der = el juego real."""
    return mg(C.espejo(titulo, izq, der, centro), de=de, a=a, marcas=marcas or [], nombre="mandela " + nombre, y=.50)


FX = [
    # ---------------- gancho: un elemento nuevo cada 2-3 s
    mg_en(C.sello("CLASIFICADO", "EXPEDIENTE 141"), "Expediente ciento", 2.4, "sello", x=.33, y=.42),
    leg("c_bo2", "EXPEDIENTE 141", ["Asunto: tu memoria", "20 efectos Mandela", "Clasificación: secreto"], de="Asunto: tu memoria",
        a=("En dos mil veintiuno", .6), x=.78, y=.50, ancho=460),
    mg_en(C.contador(2021, "", "El debate", desde=2012), "En dos mil veintiuno", 2.4, "contador 2021", x=.30, y=.30),
    mg_en(C.marcador("Letrero amarillo", 12, "Standoff · Black Ops 2"), "este letrero amarillo", 3.0, "marcador letrero", x=.56, y=.34),
    rel("La perk más famosa", "juggernog", "Jugger-Nog", "La perk más famosa", dur=2.6, x=.77, y=.52, tam=430),
    peg("escrito en su propia botella", "c_waw", "World at War · 2008", dur=2.2, x=.18, y=.66, tam=300, giro=-5),
    cam("Medio internet pulsó F", "irons", "Will Irons", dur=2.4, x=.16, y=.66, foco=(.5, .3, 1.5)),
    peg("presentar respetos", "teclado_f", "Press F", dur=2.2, x=.80, y=.60, tam=320, giro=6),
    mg_en(C.fallida("Tecla no encontrada", "En consola nunca salió la F"), "nunca viste esa letra", 1.8, "fallida F"),
    sil("Y el sargento Foley", "ramirez", "Ramírez", "Recibe todas las órdenes", lado="der", dur=3.4),
    mg_en(C.contador(20, "EFECTOS MANDELA", "Expediente 141"), "Veinte efectos Mandela", 2.4, "contador 20", y=.50),
    ficha("cosas que recuerdas", "Efecto Mandela", "Un recuerdo *compartido por miles*… que nunca pasó.", "INTEL / MEMORIA",
          dur=3.4, x=.27, y=.28, ancho=700),
    mg_en(C.objetivo("Compruébalo en pantalla", "Cada efecto, con el juego real"), "Todo comprobado", 3.0, "objetivo comprobado", x=.30, y=.82),
    sil("una frase del Capitán Price", "price_mw2019", "Capitán Price", "Modern Warfare · 2019", lado="izq", dur=4.0),

    # ---------------- 20 · Pack-a-Punch en Verrückt
    puesto("Número veinte", 20, "El Pack-a-Punch del manicomio", "ZOMBIES / VERRÜCKT / WORLD AT WAR"),
    rel("Verrückt, el manicomio", "verruckt", "Verrückt", "World at War · 2008", dur=3.4, x=.77, y=.52, tam=440),
    cam("El mapa donde debutó Juggernog", "juggernog", "Debuta aquí", dur=2.6, x=.16, y=.66, foco=(.5, .45, 1.2)),
    mg_en(C.marcador("Sala de la luz", 20, "Aquí no hay máquina"), "en la sala de la luz", 2.8, "marcador sala luz", x=.55, y=.38),
    mandela("Pack-a-Punch", ("2008", "VERRÜCKT", ["Lo que recuerdas:", "mejorar armas aquí"], P("verruckt")),
            ("2009", "DER RIESE", ["Lo que es:", "la máquina debuta aquí"], P("der_riese")),
            de="La máquina llegó dos mapas", a=("Si mejoraste", -.1), nombre="pap", marcas=["dos mapas después", "en Der Riese", "la fábrica"]),
    rel("Fue tu cerebro", "pap", "Pack-a-Punch", "Der Riese · 2009", dur=3.2, x=.77, y=.52, tam=420),
    ficha("la Porter's X2", "Porter's X2 Ray Gun", "La Ray Gun mejorada: *rayos rojos*.", "INTEL / PACK-A-PUNCH",
          dur=4.0, x=.27, y=.28, ancho=640),
    # ---------------- 19 · Double Tap en Origins
    puesto("En el diecinueve", 19, "La máquina de Double Tap", "ZOMBIES / ORIGINS / BLACK OPS 2"),
    leg("origins", "ORIGINS", ["Black Ops 2 · 2013", "Primera Guerra Mundial", "Barro hasta las rodillas"], de="Origins, Black Ops 2",
        a=("Seis generadores", -.1), x=.78, y=.52, ancho=460),
    mg_en(C.contador(6, "GENERADORES", "Origins"), "Seis generadores", 1.6, "contador generadores", x=.30, y=.30),
    rel("robots gigantes", "robot_origins", "Robots gigantes", "Te pisan", dur=3.2, x=.24, y=.55, tam=440),
    mandela("Double Tap en Origins", ("2013", "ORIGINS", ["Lo que recuerdas:", "su máquina, junto a las demás"], P("double_tap")),
            ("2013", "DER WUNDERFIZZ", ["Lo que es:", "solo sale al azar"], P("wunderfizz")),
            de="Esa máquina no existe", a=("Y la confusión", -.1), nombre="double tap", marcas=["no existe", "Der Wunderfizz", "al azar"]),
    rel("en Revelations", "revelations", "Revelations", "Black Ops 3 · ahí sí hay", dur=3.6, x=.77, y=.52, tam=420),
    # ---------------- 18 · las dos cajas del faro
    puesto("Número dieciocho", 18, "Las dos cajas del faro", "ZOMBIES / CALL OF THE DEAD"),
    cam("el mapa de George Romero", "romero", "George A. Romero", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.marcador("El faro", 80, "Call of the Dead"), "y un faro al fondo", 2.4, "marcador faro", x=.60, y=.30),
    mg_en(C.contador(1, "CAJA ARRIBA", "No dos", desde=2), "Arriba hay una sola", 2.6, "contador caja", x=.30, y=.30),
    rel("encima de PhD Flopper", "phd", "PhD Flopper", "La otra caja, encima", dur=3.2, x=.77, y=.52, tam=420),
    peg("en el mismo cuarto", "caja", "Caja misteriosa", dur=2.6, x=.18, y=.66, tam=320, giro=-5),
    aba([("cotd", "Gellar"), ("cotd", "Trejo"), ("cotd", "Rooker"), ("cotd", "Englund")], de="Sarah Michelle Gellar",
        a=("En el diecisiete", -.2), marcas=["Gellar", "Trejo", "Rooker", "Englund"], nombre="actores", x=.68, y=.60, tam=270),
    # ---------------- 17 · ¿quién mató a Ghost?
    puesto("En el diecisiete", 17, "¿Quién mató a Ghost?", "MISIÓN / CABOS SUELTOS / MW2 2009"),
    leg("loose_ends", "CABOS SUELTOS", ["Modern Warfare 2 · 2009", "Ghost y Roach", "La pista de aterrizaje"], de="misión Cabos sueltos",
        a=("heridos, con el disco", .5), x=.78, y=.52, ancho=460),
    cam("el disco duro de Makárov", "makarov", "Makárov", dur=2.6, x=.16, y=.66, foco=(.5, .3, 1.5)),
    sil("El que dispara es el general", "shepherd", "Shepherd", "Su propio comandante", lado="der", dur=3.0),
    peg("Un cabo suelto menos", "magnum44", ".44 Magnum", dur=2.6, x=.80, y=.60, tam=320, giro=5),
    aba([("ghost", "Ghost"), ("roach", "Roach")], de="Los rocían con gasolina", a=("Y el traidor", -.1), marcas=["Los rocían"],
        nombre="ghost roach", x=.30, y=.64, tam=300),
    mg_en(C.fallida("Traición", "Lo ordenó el general Shepherd"), "Y el traidor era el mismo", 2.4, "fallida traicion"),
    cam("Price y Soap lo persiguen", "soap", "Soap", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    # ---------------- 16 · zombis en la Wii
    puesto("Número dieciséis", 16, "Zombies en la Wii", "WORLD AT WAR / WII"),
    rel("Muchos recuerdan jugar Nacht", "nacht", "Nacht der Untoten", "El primer mapa", dur=3.0, x=.77, y=.52, tam=420),
    peg("apuntando a la pantalla", "wii_zapper", "Mando de Wii", dur=2.6, x=.18, y=.66, tam=320, giro=-6),
    mandela("Zombies en la Wii", ("2008", "WORLD AT WAR · WII", ["Lo que recuerdas:", "Nacht en la Wii"], P("c_waw")),
            ("2010", "BLACK OPS · WII", ["Lo que es:", "los zombis llegan aquí"], P("c_bo1")),
            de="Pero World at War de Wii", a=("El mando era el mismo", -.1), nombre="wii",
            marcas=["no tenía modo Zombies", "Los zombis llegaron", "con Kino der Toten"]),
    # ---------------- 15 · Shadows of Evil sin logro
    puesto("En el quince", 15, "El logro que nunca te dieron", "ZOMBIES / SHADOWS OF EVIL / BLACK OPS 3"),
    cam("y el Hombre Sombra", "shadowman", "El Hombre Sombra", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    aba([("soe", "Nero"), ("soe", "Jessica"), ("soe", "Jack"), ("soe", "Floyd")], de="El mago Nero", a=("Casi todos los mapas", -.1),
        marcas=["Nero", "Jessica", "Jack", "Floyd"], nombre="cuatro", x=.68, y=.60, tam=270),
    mg_en(C.logro("El principio del fin", "Completa los rituales"), "El logro El principio", 3.0, "logro principio", x=.5, y=.24),
    mg_en(C.objetivo("Termina el Easter egg", "Recompensa: XP y una tarjeta"), "Terminar el Easter egg entero", 3.4, "objetivo easter egg",
          x=.30, y=.82),
    mg_en(C.sello("SIN LOGRO", "SHADOWS OF EVIL"), "Y nada más", 2.0, "sello sin logro", x=.5, y=.46),
    # ---------------- 14 · el brazo de Zakhaev
    puesto("Número catorce", 14, "El brazo de Zakhaev", "CoD 4 / PRÍPIAT / 1996"),
    leg("one_shot", "UN DISPARO, UNA BAJA", ["CoD 4 · 2007", "Prípiat · 1996", "Teniente Price"], de="CoD 4, dos mil siete, Prípiat",
        a=("joven y camuflado", .8), x=.78, y=.52, ancho=460),
    cam("contra Imran Zakhaev", "zakhaev", "Imran Zakhaev", dur=2.6, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.contador(1000, "METROS", "El tiro de Prípiat", desde=0), "a más de un kilómetro", 2.4, "contador metros", x=.30, y=.30),
    ficha("hasta por el efecto Coriolis", "MacMillan", "Corrige por el *viento*… y por el *efecto Coriolis*.", "INTEL / FRANCOTIRADOR",
          dur=3.6, x=.27, y=.28, ancho=680),
    cam("Escucha a MacMillan", "macmillan", "MacMillan", dur=3.4, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.contador(15, "AÑOS", "Zakhaev sobrevive"), "Zakhaev sobrevive quince", 2.6, "contador 15", x=.30, y=.30),
    rel("le desliza su pistola", "m1911", "M1911 de Price", "Se la da a Soap", dur=1.8, x=.77, y=.52, tam=420),
    sil("Y es Soap quien lo remata", "soap", "Soap", "Lo remata en el puente", lado="der", dur=3.0),
    # ---------------- 13 · los números
    puesto("En el trece", 13, "¿Quién pregunta por los números?", "BLACK OPS / 2010 / INTERROGATORIO"),
    sil("Alex Mason, atado", "mason", "Alex Mason", "Atado a una silla", lado="der", dur=4.0),
    mg_en(C.codigo("1964", "ESTACIÓN DE NÚMEROS", "¿Qué significan?"), "Y una voz que no deja", 2.6, "codigo numeros", x=.30, y=.30),
    aba([("reznov", "Reznov"), ("dragovich", "Dragovich")], de="en boca de Reznov", a=("Pero es la voz", -.1), marcas=["Reznov", "Dragovich"],
        nombre="sospechosos", x=.30, y=.64, tam=300),
    aba([("hudson", "Hudson"), ("weaver", "Weaver")], de="Jason Hudson, de la CIA", a=("Los números los transmitía", -.1),
        marcas=["Hudson", "Weaver"], nombre="interrogadores", x=.70, y=.60, tam=300),
    mg_en(C.sello("TU BANDO", "CIA"), "El que los pedía", 2.2, "sello bando", x=.5, y=.46),
    rel("murió en la fuga de Vorkutá", "reznov", "Viktor Reznov", "Murió en Vorkutá", dur=3.2, x=.77, y=.52, tam=420),
    # ---------------- 12 · World at War ya tenía finales
    puesto("Número doce", 12, "Black Ops 2 no inventó los finales", "WORLD AT WAR / OKINAWA / 2008"),
    mandela("Decisiones que cambian la historia", ("2012", "BLACK OPS 2", ["Lo que recuerdas:", "el primero con finales"], P("c_bo2")),
            ("2008", "WORLD AT WAR", ["Lo que es:", "ya te hacía elegir"], P("c_waw")),
            de="Black Ops 2 se recuerda", a=("Okinawa, el castillo", -.1), nombre="finales", marcas=["el primer Call of Duty", "cuatro años antes"]),
    leg("shuri", "BREAKING POINT", ["Okinawa · 1945", "Castillo de Shuri"], de="Okinawa, el castillo de Shuri", a=("Unos soldados", .3),
        x=.78, y=.52, ancho=440),
    aba([("roebuck", "Roebuck"), ("polonsky", "Polonsky")], de="se lanzan sobre Roebuck", a=("El que no salvas", -.1),
        marcas=["Roebuck", "Polonsky", "Solo puedes salvar"], nombre="roebuck polonsky", x=.70, y=.60, tam=300),
    mg_en(C.objetivo("Salva a uno", "El otro muere"), "Solo puedes salvar a uno", 2.6, "objetivo salva", x=.30, y=.82),
    rel("las chapas que te dan", "roebuck", "Chapas de Roebuck", "Aunque lo salves", dur=3.6, x=.77, y=.52, tam=420),
    # ---------------- 11 · Final Fronts
    puesto("En el once", 11, "Las misiones perdidas de World at War", "PLAYSTATION 2 / 2008"),
    mg_en(C.marcador("Misión perdida", 50, "No sale en la campaña"), "Un entrenamiento disparando", 2.6, "marcador mision", x=.55, y=.36),
    rel("En PlayStation 2 salió", "c_finalfronts", "Final Fronts", "PS2 · 2008", dur=3.6, x=.77, y=.52, tam=440),
    peg("World at War: Final Fronts", "ps2", "PlayStation 2", dur=2.6, x=.18, y=.66, tam=320, giro=-5),
    ficha("Lo hizo otro estudio", "Final Fronts", "Otro estudio: *Rebellion* · otra campaña entera.", "INTEL / PS2",
          dur=3.6, x=.27, y=.28, ancho=640),
    # ---------------- 10 · botas doradas
    puesto("Número diez", 10, "Las botas doradas", "ZOMBIES / ORIGINS"),
    mg_en(C.marcador("Montón de tierra", 4, "Cava con la pala"), "Con la pala puedes cavar", 2.6, "marcador tierra", x=.5, y=.46),
    mg_en(C.fallida("Objeto no encontrado", "Las botas doradas no existen"), "No existen. Lo único dorado", 2.0, "fallida botas"),
    aba([("pala_dorada", "Pala dorada"), ("casco_dorado", "Casco dorado")], de="la pala dorada, y el casco", a=("Para el barro", -.1),
        marcas=["la pala dorada", "y el casco dorado"], nombre="dorados", x=.70, y=.60, tam=320),
    rel("lo que había era Stamin-Up", "staminup", "Stamin-Up", "Para el barro", dur=2.6, x=.77, y=.52, tam=400),
    # ---------------- 9 · Evanescence
    puesto("En el nueve", 9, "Evanescence en Zombies", "ZOMBIES / KINO DER TOTEN"),
    cam("que Bring Me to Life", "evanescence", "Evanescence", dur=3.2, x=.16, y=.66, foco=(.5, .4, 1.2)),
    mg_en(C.fallida("No encontrada", "Ni en un mapa, ni en un tráiler"), "Nunca estuvo. Ni en un mapa", 2.2, "fallida evanescence"),
    peg("los montajes de YouTube", "kino", "Montajes de 2010", dur=2.6, x=.80, y=.60, tam=320, giro=5),
    rel("de Elena Siegman", "elena_siegman", "Elena Siegman", "«115» · Kino der Toten", dur=6.5, x=.76, y=.52, tam=460),
    # ---------------- 8 · Menéndez
    puesto("Número ocho", 8, "Menéndez en llamas", "BLACK OPS 2 / FINAL MALO"),
    sil("Raúl Menéndez, el villano", "menendez", "Raúl Menéndez", "El villano de Black Ops 2", lado="der", dur=3.4),
    cam("su hermana Josefina", "josefina", "Josefina", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mandela("Menéndez en llamas", ("2012", "LO QUE RECUERDAS", ["Lo ves arder", "sobre la tumba"], P("menendez")),
            ("2012", "LO QUE ES", ["La imagen", "corta a negro"], P("c_bo2")),
            de="Se prende fuego, sí", a=("La escena gráfica", .5), nombre="menendez", marcas=["Se prende fuego", "corta a negro"]),
    # ---------------- 7 · la perk gratis de la Luna
    puesto("En el siete", 7, "La perk gratis de la Luna", "ZOMBIES / MOON / BLACK OPS"),
    rel("Moon, el último mapa", "moon", "Moon", "Black Ops · 2011", dur=3.0, x=.77, y=.52, tam=420),
    mg_en(C.marcador("Plataforma de salto", 15, "Biodomo"), "En el biodomo hay", 2.6, "marcador plataforma", x=.5, y=.40),
    mg_en(C.fallida("Sin recompensa", "Nada en el mapa ni en el código"), "No hay nada de eso", 2.2, "fallida moon"),
    rel("la granada cuántica", "qed", "QED", "Perk al azar", dur=3.2, x=.77, y=.52, tam=400),
    mg_en(C.contador(3, "MISILES", "Hacia la Tierra"), "tres misiles salen", 2.4, "contador misiles", x=.30, y=.30),
    # ---------------- 6 · la portada
    puesto("Número seis", 6, "Mira bien la portada", "BLACK OPS 2 / BLACK OPS"),
    pant("c_bo2", de="La portada de Black Ops 2", a=("Y la de Black Ops, la de", -.05), zoom=(1.0, 1.55), pan=(0, 0, 0, .28)),
    mg_en(C.marcador("Cuchillo", 1, "En la otra mano"), "lleva un cuchillo", 2.6, "marcador cuchillo", x=.42, y=.80),
    pant("c_bo1", de="Y la de Black Ops, la de", a=("En el cinco", -.1), zoom=(1.0, 1.25), pan=(0, 0, 0, .15)),
    mg_en(C.contador(2, "PISTOLAS", "Black Ops · 2010", desde=1), "Lleva dos, una en cada", 2.0, "contador pistolas", x=.75, y=.30),
    # ---------------- 5 · Ramírez
    puesto("En el cinco", 5, "¡Ramírez, haz de todo!", "MISIÓN / WOLVERINES! / MW2 2009"),
    leg("burger_town", "WOLVERINES!", ["Modern Warfare 2 · 2009", "Virginia · Burger Town"], de="la invasión de Virginia",
        a=("El sargento Foley no deja", .5), x=.78, y=.52, ancho=440),
    cam("El sargento Foley no deja", "ramirez", "Soldado Ramírez", dur=4.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.objetivo("Ramírez, haz de todo", "Orden no encontrada"), "Pero Ramírez, haz de todo", 3.0, "objetivo ramirez", x=.30, y=.82),
    rel("en un meme de internet", "knowyourmeme", "El meme", "Noviembre de 2009", dur=3.2, x=.77, y=.52, tam=420),
    mg_en(C.contador(17, "AÑOS", "Y sigue", desde=0), "Y diecisiete años después", 2.4, "contador 17", x=.30, y=.30),
    # ---------------- 4 · Press F
    puesto("Número cuatro", 4, "Pulsa F", "ADVANCED WARFARE / 2014"),
    cam("El funeral del soldado Will Irons", "irons", "Will Irons", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mandela("Pulsa F", ("2014", "PC", ["Press F", "to Pay Respects"], P("teclado_f")),
            ("2014", "CONSOLA", ["Hold [botón]", "to Pay Respects"], P("c_aw")),
            de="Pero esa F solo salía", a=("O sea: millones", .5), nombre="press f", marcas=["solo salía en PC", "En PlayStation y Xbox"]),
    # ---------------- 3 · Juggernog
    puesto("En el tres", 3, "La botella de Juggernog", "ZOMBIES / WORLD AT WAR · BLACK OPS"),
    mg_en(C.contador(2500, "PUNTOS", "Jugger-Nog"), "por dos mil quinientos puntos", 2.4, "contador 2500", x=.30, y=.30),
    rel("con su propia canción", "juggernog", "Jugger-Nog", "Su canción", dur=5.5, x=.77, y=.52, tam=420),
    mandela("La etiqueta", ("2008-2010", "WORLD AT WAR · BLACK OPS", ["Juggernaut Soda"], P("c_bo1")),
            ("2012", "BLACK OPS 2", ["Jugger-Nog Soda"], P("c_bo2")),
            de="decían otra cosa", a=("La bebiste", -.1), nombre="juggernaut", centro="CORREGIDA", marcas=["Juggernaut Soda", "En Black Ops 2"]),
    # ---------------- 2 · Standoff
    puesto("Número dos", 2, "El letrero de Standoff", "MULTIJUGADOR / STANDOFF / BLACK OPS 2"),
    rel("Standoff, el mapa de Black Ops 2", "standoff", "Standoff", "Black Ops 2 · 2012", dur=3.0, x=.77, y=.52, tam=440),
    peg("ya está en Cold War", "c_bocw", "Cold War", dur=2.6, x=.18, y=.66, tam=320, giro=-5),
    mg_en(C.radio("iLLeY", "«No puedo creer que acaban de poner este letrero»", "PUBLICACIÓN / JULIO 2021"), "un jugador profesional, iLLeY",
          4.4, "radio illey", y=.28),
    mg_en(C.contador(2015, "", "Video de Standoff", desde=2021), "subido en dos mil quince", 2.4, "contador 2015", x=.30, y=.30),
    mg_en(C.marcador("El letrero", 3, "En su poste"), "Y ahí está el letrero", 3.0, "marcador poste", x=.56, y=.36),
    mandela("El letrero", ("2021", "LO QUE CREÍAN", ["Nuevo en Cold War"], P("c_bocw")),
            ("2012", "LO QUE ES", ["Siempre estuvo", "en Black Ops 2"], P("standoff")),
            de="El mapa de Cold War salió", a=("Y el número uno. La", -.2), nombre="standoff", marcas=["salió sin él", "lo devolvió", "El letrero no era nuevo"]),
    # ---------------- 1 · Bravo Six
    puesto("Y el número uno. La frase", 1, "La frase de Price", "MODERN WARFARE / 2019"),
    rel("Modern Warfare, dos mil diecinueve", "price_mw2019", "Capitán Price", "Modern Warfare · 2019", dur=3.0, x=.24, y=.42, tam=380),
    leg("clean_house", "CASA LIMPIA", ["Modern Warfare · 2019", "Visión nocturna", "Londres"], de="La recuerdas en la campaña",
        a=("Pero es del tráiler", .3), x=.78, y=.52, ancho=440),
    rel("Pero es del tráiler", "c_mw2019", "Tráiler de presentación", "Mayo de 2019", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.radio("Bravo 6", "«Bravo seis, al primer piso.»", "CAMPAÑA / CASA LIMPIA"), "Bravo seis, al primer piso", 1.5, "radio piso 1", y=.28),
    mg_en(C.radio("Bravo 6", "«Bravo seis, al segundo.»", "CAMPAÑA / CASA LIMPIA"), "Bravo seis, al segundo", 2.6, "radio piso 2", y=.42),
    rel("literalmente, Going Dark", "going_dark", "Going Dark", "Tampoco está", dur=3.4, x=.77, y=.52, tam=420),
    mg_en(C.sello("SOLO EN UN TRÁILER", "BRAVO 6, GOING DARK"), "Solo en un tráiler", 2.6, "sello trailer", x=.5, y=.46),
    # ---------------- cierre
    mg_en(C.sello("EXPEDIENTE CERRADO", "141"), "Expediente cerrado", 2.4, "sello cerrado", x=.5, y=.46),
    rel("Yo apuesto por el letrero", "standoff", "Mi apuesta", "El letrero", dur=3.0, x=.77, y=.52, tam=420),
    peg("los veinticinco secretos", "c_mw2019", "25 secretos de MW4", dur=3.0, x=.18, y=.66, tam=320, giro=-5),
    mg_en(C.objetivo("Suscríbete", "El siguiente expediente"), "suscríbete", 3.4, "objetivo suscribete", x=.30, y=.82),
]

ROTULOS = [
    dict(texto="TU MEMORIA", en="Asunto: tu memoria", tam=150, color="amarillo", y=.22, dur=1.8),
    dict(texto="NUNCA PASÓ", en="dice que nunca pasaron", tam=150, color="amarillo", y=.22, dur=2.0),
    dict(texto="NO EXISTE", en="Esa máquina no existe", tam=150, color="amarillo", y=.22, dur=2.0),
    dict(texto="UNA SOLA", en="Arriba hay una sola", tam=150, color="amarillo", y=.22, dur=1.8),
    dict(texto="Y NO", en="Y no. El que dispara", tam=160, color="amarillo", y=.22, dur=1.4),
    dict(texto="EL JUEGO, NO", en="El juego, no", tam=140, color="amarillo", y=.22, dur=1.8),
    dict(texto="LE VUELA EL BRAZO", en="Le vuela el brazo", tam=120, color="amarillo", y=.22, dur=2.2),
    dict(texto="ESTABA EN TU CABEZA", en="Todo lo demás, estaba", tam=110, color="amarillo", y=.22, dur=2.4),
    dict(texto="SE OYE, NO SE VE", en="Se oye, y no se ve", tam=130, color="amarillo", y=.22, dur=2.2),
    dict(texto="UNA ORDEN QUE NADIE DIO", en="Una orden que nadie dio", tam=100, color="amarillo", y=.22, dur=2.4),
    dict(texto="F", en="nunca vieron. F", tam=220, color="amarillo", y=.40, dur=1.6),
    dict(texto="JUGGERNAUT SODA", en="Juggernaut Soda", tam=130, color="amarillo", y=.22, dur=2.2),
    dict(texto="NUNCA LEÍSTE LA ETIQUETA", en="nunca leíste la etiqueta", tam=100, color="amarillo", y=.22, dur=2.2),
    dict(texto="BRAVO 6, GOING DARK", en="Bravo Seis, a oscuras", tam=110, color="amarillo", y=.22, dur=2.6),
]

SFX = {}
# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/cod/ → sfx/cod_*.mp3), solo en momentos clave
PISTAS = [
    dict(sfx="cod_sello", en="Expediente ciento", vol=.30),
    dict(sfx="cod_fallida", en="nunca viste esa letra", vol=.28),
    dict(sfx="cod_puesto", en="Número veinte", vol=.24),
    dict(sfx="cod_puesto", en="En el quince", vol=.22),
    dict(sfx="cod_sello", en="Número diez", vol=.24),
    dict(sfx="cod_puesto", en="En el cinco", vol=.22),
    dict(sfx="cod_fallida", en="Y el traidor era el mismo", vol=.28),
    dict(sfx="cod_logro", en="El logro El principio", vol=.30),
    dict(sfx="cod_sello", en="Y nada más", vol=.26),
    dict(sfx="cod_radio", en="Y una voz que no deja", vol=.22),
    dict(sfx="cod_fallida", en="No existen. Lo único dorado", vol=.28),
    dict(sfx="cod_fallida", en="No hay nada de eso", vol=.28),
    dict(sfx="cod_radio", en="un jugador profesional, iLLeY", vol=.24),
    dict(sfx="cod_puesto", en="Y el número uno. La frase", vol=.26),
    dict(sfx="cod_sello", en="Solo en un tráiler", vol=.28),
    dict(sfx="cod_sello", en="Expediente cerrado", vol=.28),
    # ---- SONIDOS NOMBRADOS (regla 31-oct-2026): la voz los anuncia y se oyen en el hueco (post), a nivel de voz
    dict(sfx="s_shepherd", en="Y lo dice así|fin", vol=1.0, voz=True),
    dict(sfx="s_brazo", en="Escucha a MacMillan|fin", vol=1.0, voz=True),
    dict(sfx="s_numbers", en="que no deja de preguntar|fin", vol=1.0, voz=True),
    dict(sfx="s_115", en="de Elena Siegman|fin", vol=1.0, voz=True),
    dict(sfx="s_ramirez", en="soldado Ramírez. Escucha|fin", vol=1.0, voz=True),
    dict(sfx="s_jingle", en="con su propia canción|fin", vol=1.0, voz=True),
    dict(sfx="s_bravo6", en="del Price moderno, es esta|fin", vol=1.0, voz=True),
]

# Cortes rápidos del gancho con clips ya bajados (debajo de todo lo demás)
VIDEOS = [
    vid(90, "este letrero amarillo", ("Y miles le creyeron", .8), desde=0.5),        # el letrero en el video de 2015
    vid(85, "escrito en su propia botella", ("Medio internet", -.1), desde=0.3),    # la botella
    vid(80, "pulsó F para presentar", ("nunca viste esa letra", -.05), desde=1.0),  # «Press F» en PC
    vid(81, "nunca viste esa letra", ("Y el sargento Foley", -.1), desde=1.0),      # «Hold [botón]» en consola
    vid(11, "Veinte efectos Mandela", ("cosas que recuerdas", .2), desde=1.0),       # la Ray Gun
    vid(41, ("cosas que recuerdas", .2), "y que el propio juego", desde=1.5),       # el interrogatorio
    vid(64, "y que el propio juego", ("Todo comprobado", -.1), desde=1.0),         # la tumba de Josefina
    vid(69, ("Todo comprobado", 1.2), "Y el número uno es", desde=1.0),            # los misiles de Moon
    vid(93, "Y el número uno es", ("Número veinte", -.15), desde=4.0),             # el tráiler de MW2019
]
FX = VIDEOS + FX

# ---- 2.ª pasada de relleno: ningún tramo de > 4 s con el clip solo (medido con `fx --seco`)
FX += [
    mg_en(C.marcador("Ray Gun", 2, "La primera en entrar"), "Y la primera arma", 3.0, "marcador ray gun", x=.52, y=.40),
    peg("Y muchos juran que compraban", "double_tap", "Double Tap", dur=3.2, x=.80, y=.60, tam=330, giro=5),
    zoom("bastones elementales", ("Y muchos juran", -.1), 1.15),
    mg_en(C.objetivo("Compra Double Tap", "En Revelations, sí"), "Y ahí sí hay máquina", 3.4, "objetivo revelations", x=.30, y=.82),
    mg_en(C.marcador("El ojo", 1, "Endgame · Afganistán"), "clavándole un cuchillo", 3.0, "marcador ojo", x=.5, y=.38),
    peg("El mando era el mismo", "wii", "Wii", dur=3.0, x=.80, y=.60, tam=320, giro=5),
    leg("soe", "SHADOWS OF EVIL", ["Black Ops 3 · 2015", "Morg City · años 40"], de="Shadows of Evil, Black Ops 3", a=("El mago Nero", -.1),
        x=.78, y=.52, ancho=440),
    mg_en(C.balanza("Logro por el Easter egg", [("Origins", True, "sí"), ("Moon", True, "sí"), ("Shadows of Evil", False, "no")]),
          "Casi todos los mapas", 5.0, "balanza logros", y=.50),
    mg_en(C.marcador("El puente", 30, "Game Over"), "Y al final, en el puente", 3.0, "marcador puente", x=.5, y=.40),
    peg("Price, herido en el suelo", "game_over", "Game Over", dur=3.0, x=.18, y=.66, tam=320, giro=-5),
    ficha("Mucha gente pone esa frase", "«The numbers, Mason»", "¿Quién lo pregunta? *No es Reznov.*", "INTEL / INTERROGATORIO",
          dur=3.6, x=.27, y=.28, ancho=640),
    zoom("Pero es la voz del interrogador", ("Jason Hudson", -.1), 1.15),
    mg_en(C.marcador("Reznov", 5, "Vorkutá · 1963"), "Y ya que estamos: Reznov", 3.0, "marcador reznov", x=.5, y=.38),
    mg_en(C.fallida("Polonsky K.I.A.", "El que no salvas"), "El que no salvas, muere", 2.4, "fallida polonsky"),
    peg("Y un detalle cruel", "breaking_point", "Breaking Point", dur=3.2, x=.18, y=.66, tam=320, giro=-5),
    rel("jugadores que recuerdan misiones", "c_waw", "World at War", "La campaña de PC y consolas", dur=3.6, x=.77, y=.52, tam=400),
    mg_en(C.marcador("Tren", 40, "Final Fronts"), "Un tramo en tren", 2.6, "marcador tren", x=.5, y=.40),
    mandela("Mismo nombre, otra campaña", ("2008", "WORLD AT WAR", ["PC · PS3 · Xbox 360 · Wii"], P("c_waw")),
            ("2008", "FINAL FRONTS", ["PlayStation 2", "otra campaña"], P("c_finalfronts")),
            de="Mismo nombre, misma guerra", a=("Número diez", -.2), nombre="final fronts", centro="MISMO NOMBRE", marcas=["Mismo nombre", "otra campaña"]),
    rel("y premios dorados", "pala_dorada", "Pala dorada", "Premio dorado", dur=3.0, x=.77, y=.52, tam=400),
    mg_en(C.marcador("Botas doradas", 0, "No existen"), "Muchos recuerdan unas botas", 3.2, "marcador botas", x=.5, y=.62),
    rel("La canción real de Kino", "kino_115", "«115»", "Kino der Toten", dur=3.6, x=.77, y=.52, tam=420),
    zoom("retorciéndose sobre la tumba", ("Se prende fuego", -.1), 1.18),
    mg_en(C.sello("CORTE A NEGRO", "BLACK OPS 2"), "tu cabeza la rellenó", 2.4, "sello corte", x=.5, y=.46),
    mg_en(C.objetivo("Salto perfecto", "Recompensa: ninguna"), "si saltabas perfecto", 3.2, "objetivo salto", x=.30, y=.82),
    mg_en(C.balanza("Lo que da una perk en Moon", [("Saltar perfecto", False, "nada"), ("La QED", True, "a veces")]),
          "ni en las guías", 4.6, "balanza moon", y=.50),
    rel("Lo que sí es real en Moon", "luna", "La Tierra", "Desde la Luna", dur=4.0, x=.77, y=.52, tam=420),
    mg_en(C.sello("NADIE LA DIO", "MW2 · 2009"), "la orden más famosa", 2.6, "sello orden", x=.5, y=.46),
    peg("Y el letrero que se volvió meme", "knowyourmeme", "Meme · 2014", dur=3.0, x=.80, y=.60, tam=320, giro=5),
    mg_en(C.contador(1, "TECLA", "Que nunca vieron", desde=0), "millones de jugadores de consola", 2.8, "contador tecla", x=.30, y=.30),
    mg_en(C.marcador("Jugger-Nog", 2, "La máquina"), "En la máquina dice", 3.0, "marcador maquina", x=.5, y=.36),
    peg("el logo de World at War", "c_waw", "World at War", dur=2.8, x=.18, y=.66, tam=300, giro=-5),
    cam("La bebiste cientos de veces", "juggernog", "Jugger-Nog", dur=3.0, x=.16, y=.66, foco=(.5, .45, 1.2)),
    mg_en(C.contador(1000, "LO CREYERON", "Miles", desde=1), "Miles le dieron la razón", 2.8, "contador miles", x=.30, y=.30),
    zoom("Juraban que en Black Ops 2", ("Pero este es un video", -.1), 1.15),
    cam("En la campaña, en la misión de la casa", "price_mw2019", "Price", dur=3.2, x=.16, y=.66, foco=(.5, .3, 1.5)),
    mg_en(C.radio("Price", "«Usaremos la oscuridad para cubrirnos.»", "CAMPAÑA / GOING DARK"), "Price solo dice que usarán", 3.6,
          "radio oscuridad", y=.28),
    peg("¿cuál de los veinte", "mandela", "Efecto Mandela", dur=3.4, x=.80, y=.60, tam=320, giro=5),
    mg_en(C.sello("RETÍRATE, SOLDADO", "EXPEDIENTE 141"), "Retírate, soldado", 3.0, "sello retirate", x=.5, y=.46),
]

# ---- fichas tácticas (chequeo 3-nov: 0,3/min contra 1,4 del canal): una por puesto, arriba a la izquierda, fuera de espejos y contadores
F = dict(dur=3.4, x=.27, y=.28, ancho=640)
FX += [
    ficha("Mucha gente recuerda haber mejorado", "Verrückt", "Debut de *Juggernog* · sin Pack-a-Punch.", "INTEL / WORLD AT WAR", **F),
    ficha("Y la confusión tiene culpable", "Revelations", "Black Ops 3 · imita a Origins · *con* Double Tap.", "INTEL / ZOMBIES", **F),
    ficha(("La otra está cerca", .7), "Call of the Dead", "Arriba del faro: *una* caja. La otra, encima de PhD Flopper.", "INTEL / BLACK OPS", **F),
    ficha("La respuesta rápida es Makárov", "Cabos sueltos", "Quien dispara: *el general Shepherd*.", "INTEL / MW2 2009", **F),
    ficha("Muchos recuerdan jugar Nacht", "Nacht der Untoten", "World at War de Wii: *sin* modo Zombies.", "INTEL / WII", **F),
    ficha("Shadows of Evil, Black Ops 3", "Shadows of Evil", "Logro por el Easter egg final: *ninguno*.", "INTEL / BLACK OPS 3", **F),
    ficha("Okinawa, el castillo de Shuri", "Breaking Point", "Elige a quién salvar: *Roebuck* o *Polonsky*.", "INTEL / WORLD AT WAR", **F),
    ficha("Volvemos al barro de Origins", "Origins", "Al cavar: armas, potenciadores y *premios dorados*.", "INTEL / BLACK OPS 2", **F),
    ficha("Hay quien recuerda que Bring Me", "Bring Me to Life", "Evanescence: *nunca* sonó en Call of Duty.", "INTEL / ZOMBIES", **F),
    ficha("Muchos juran que, si saltabas", "Moon", "Biodomo: *ninguna perk* por saltar.", "INTEL / BLACK OPS", **F),
    ficha("Nació en noviembre de dos mil nueve", "Ramírez, haz de todo", "Meme de internet · *noviembre de 2009*.", "INTEL / MW2 2009", **F),
    ficha("Advanced Warfare, dos mil catorce", "Atlas", "El funeral de *Will Irons* · 2014.", "INTEL / ADVANCED WARFARE", **F),
    ficha("Pero es del tráiler", "Tráiler de presentación", "Mayo de 2019 · *Bravo Six, going dark*.", "INTEL / MW 2019", **F),
    ficha(("Y ahora, la pregunta", 1.0), "Tu turno", "¿Cuál te hizo *dudar de tu memoria*?", "INTEL / COMENTARIOS", **F),
]
