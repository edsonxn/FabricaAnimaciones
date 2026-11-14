# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 15 SECRETOS del teaser de The Elder Scrolls VI: Sentinel» (SECUENCIA YT, Crónicas de Tamriel, 3-nov-2026).
REGLA DE ORO (tes_secretos_40) + «sin tramos vacíos» (3-nov-2026): kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a
palabras de la voz:
- 15 avisos (uno por puesto) arriba al centro + gancho saturado (cortes `vid()` con otros clips, un elemento cada 2-3 s).
- Fichas de inventario SOLO con datos verificados en UESP (`_investigacion.md`), arriba a la derecha.
- Pegatinas REALES (Fandom) en todos los estilos de `nucleo/peg_estilos.py`: silueta (Todd, Saadia, Nazir), reliquia, banda, camafeo,
  legajo y abanico.
- Comentarios REALES: 3 críticas con burla disfrazada (cr1 @alcoholikmisanthroper1934, cr2 @JoseAkua, cr3 @nyarlathotep2265) y
  4 agradecimientos juntos (ag1).
- MG NUEVOS de este guion (mg_tes): cifrado (número de Starfield = SENTINEL), ceguera (la vista del Sacerdote de la Polilla) y
  lecturas (las tres lecturas de la cita); además rejilla 44 → 4, cronologías 4E 175 → 201 → 206 y la de los 40 años de BGS.
- Mapas reales con ruta: Bahía de Iliac (Daggerfall), Hammerfell (Pocket Guide) Skyrim → Alik'r → Sentinel, Sentinel de ESO.
  python fab.py tes_sentinel_teaser fx --seco   tiempos      python fab.py tes_sentinel_teaser fx hoja   previews/fx_NN.jpg
  python fab.py tes_sentinel_teaser chequeo     densidad contra el canal y narración ↔ imagen
"""
import os

import mg_tes as T
import mg_wow as W
import peg_estilos as PE

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


def vid(n, de, a, desde=0.0):
    """Corte rápido con OTRO clip ya bajado a cuadro entero; van PRIMERO en FX (debajo de todo). `n` = número del beat de la
    versión de una sola voz (beats_v1.json): sus clips viven en medios/_v1/ desde el cambio a siete voces (_remapear.py)."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", "_v1", f"scene-{n:03d}.mp4"), de=de, a=a, desde=desde,
                entra=.12, sale=.12, nombre=f"corte clip {n:03d}")


C_ALCO, C_JOSE, C_NYAR = "UgyR2Rnl7yIODqxw1z14AaABAg", "UgyRNHW2x-zACQueNkF4AaABAg", "UgyYrD3Rsm_VnW1DviV4AaABAg"
C_BVSQ, C_SKEL, C_HECT, C_ADOL = "UgwCQjEzicZxzVKi9hh4AaABAg", "UgwXgEixna-BnCV_8rR4AaABAg", "UgwFLX1Ah-oUWDO79Ct4AaABAg", "Ugz7qkuyocZuM-A4dNB4AaABAg"
CITA = ["«El pergamino solo me ofreció un destello, un velo apenas levantado ante mis ojos.",
        "Un futuro perdido. Una victoria deshecha. Arenas del tiempo dispersas por el destino.»"]

# ---- cortes rápidos (gancho y puntos de giro): debajo de MG y pegatinas
VIDEOS = [
    vid(110, "Un pergamino con una gema", "Una palabra"),
    vid(6, "Una palabra", ("Y una frase firmada", -.1)),
    vid(122, "Y una frase firmada", "Parece poco"),
    vid(37, "una ciudad real", "una reina que nadie"),
    vid(77, "una reina que nadie", "una fecha exacta"),
    vid(71, "una fecha exacta", "y una pista"),
    vid(86, "contra los Thalmor", "Hoy te traigo"),
    vid(129, "lo que hiciste en Skyrim", ("de nada", .3)),
    vid(48, "todos los finales ocurrieron", "Lo llaman"),
    vid(54, "dunas que el viento", "Hammerfell es la provincia"),
    vid(102, "Dexion Evicus lee tres", "Y a partir de ahí"),
    vid(130, "lo que hiciste en Skyrim, la guerra civil", ("Todo esto es teoría", -.2)),
]

FX = [
    # ---------------- GANCHO (0-62 s): un elemento nuevo cada 2-3 s
    zoom(0.0, "Un pergamino con una gema", 1.14),
    mis("Ocho años. Ocho años", "Crónicas de Tamriel", "The Elder Scrolls VI", dur=3.2, y=.22),
    mg_en(T.contadores("La espera", [("Años desde el primer teaser", 8, None, None)]), "Ocho años esperando", 3.0, "espera", x=.76, y=.32),
    rel("Un pergamino con una gema", "pergamino_sr", "Pergamino Antiguo", "Gema azul en el centro", dur=2.6, x=.78, y=.52, tam=460),
    mis("Una palabra", "Nombre revelado", "Sentinel", dur=2.4, y=.70),
    cam("firmada por un sacerdote", "dexion", "Sacerdote de la Polilla", dur=2.6, x=.16, y=.66),
    peg("una ciudad real", "alikr_desierto", "Hammerfell", dur=2.0, x=.20, y=.64, tam=380, giro=5),
    ficha("una reina que nadie", "Alta Reina Iradne", "Aparece por *primera vez* en el teaser", "Hammerfell", dur=2.2),
    mis("una fecha exacta", "Fecha de la cita", "4E 206", dur=2.0, y=.72),
    cam("la Gran Guerra contra", "elenwen", "Thalmor", dur=2.4, x=.84, y=.62),
    mis("Hoy te traigo quince secretos", "Crónicas de Tamriel", "15 secretos del teaser", dur=3.0, y=.25),
    ficha("Todos comprobados", "Fuentes", "Cada dato con su enlace de *UESP*", "En la descripción", dur=3.2),
    mis("hay siete voces", "Novedad del canal", "Siete voces compiten", dur=3.4, y=.30),
    mg(T.rejilla("Quince secretos", n=15, encendidas=1, cols=15, ancho=980), "el número uno es una teoría", ("esa frase", 1.0),
       ["el número uno", "una teoría"], "rejilla 15", y=.30),
    aba([("alduin", "Alduin"), ("talos_estatua", "Talos"), ("elenwen", "Thalmor")], "lo que hiciste en Skyrim podría",
        ("Número quince", -.2), ["lo que hiciste", "podría no haber"], "lo de skyrim"),

    # ---------------- 15 · el logo en la arena (62-104)
    aviso("Número quince", 15, "El logo escondido en la arena"),
    pant("t_logo", "aparece el engranaje", ("No es casualidad", .3), zoom=(1.0, 1.08)),
    ficha("los cuarenta años del estudio", "Bethesda Game Studios", "Desde *1986* · Bethesda, Maryland", "40 aniversario", dur=5.0),
    zoom("donde todo empezó", "Todd Howard lo presentó", 1.12),
    sil("Todd Howard lo presentó", "todd", "Todd Howard", "Director · Bethesda Game Studios", dur=5.0, lado="der", encuadre=(0, .75)),
    mg_en(T.contadores("La respuesta", [("Años de preguntas", 8, None, None), ("Palabras reveladas", 1, None, None)]),
          "Ocho años de preguntas", 4.0, "respuesta", x=.76, y=.34),
    mis("es más de lo que teníamos ayer", "Objetivo completado", "Saber el nombre", dur=3.0, y=.30),

    # ---------------- 14 · lo que contó Todd (104-152)
    aviso("En el catorce", 14, "Lo que Todd contó"),
    cam("Todd repasa cuarenta años", "todd", "Todd Howard", dur=3.4, x=.16, y=.66, foco=(.47, .28, 3.2)),
    mg(T.cronologia("40 años de Bethesda Game Studios", [("1986", "Gridiron", 0), ("1991", "Terminator", 1), ("1993", "Todd llama a la puerta", 2)]),
       "Su primer juego fue Gridiron", ("para pedir trabajo", 1.0), ["Gridiron", "Terminator", "enero de mil"], "cronologia bgs", y=.30),
    mg(T.barras("Memoria de la Xbox 360", [(None, "Lo previsto", 256, 0, T.GRIS), (None, "Lo que llegó", 512, 1, T.ORO)], unidad=" MB",
                remate=("FIESTA EN EL ESTUDIO", 2)),
       "Y que cuando les dijeron", ("como querían", .6), ["trescientos sesenta", "quinientos doce", "montaron una fiesta"], "ram", y=.32),
    peg("para poder hacer Oblivion", "oblivion_logo", "Oblivion · 2006", dur=3.0, x=.16, y=.64, tam=360, giro=6),
    ficha("Skyrim sigue siendo", "Skyrim", "*15 años* después, su juego más jugado", "Todd Howard · 40 aniversario", dur=4.6),
    mis("Que no te extrañe", "Pista", "El seis mira a Skyrim", dur=3.0, y=.70),

    # ---------------- 13 · el teaser de 2018 (152-198)
    aviso("Número trece", 13, "El teaser de 2018"),
    ficha("El diez de junio", "Teaser de 2018", "*E3* · 10 de junio de 2018 · *36* segundos", "Solo paisaje", dur=5.0),
    zoom("niebla, colinas", "Ni nombre", 1.16),
    mis("Ni nombre, ni fecha", "Datos revelados", "Ninguno", dur=2.6, y=.70),
    mg_en(T.contadores("Lo que dio el teaser", [("Nombres", 0, None, None), ("Fechas", 0, None, None), ("Segundos de paisaje", 36, None, None)]),
          "Solo el tema de la saga", 4.0, "teaser 2018", x=.76, y=.34),
    mapa("iliac.jpg", "Bahía de Iliac", [(.17, .36, "Roca Alta", "inicio"), (.27, .58, "Bahía de Iliac", "paso"),
                                         (.354, .77, "Sentinel", "meta", P("alikr_desierto"))],
         "La apuesta más repetida", ("no iban tan mal", .6), ["Roca Alta", "bahía de Iliac", "la ciudad más famosa"], "La apuesta de los fans",
         ventana=True, ancho=1150),
    mis("Los detectives de internet", "Logro desbloqueado", "Detective de internet", dur=3.0, y=.84),

    # ---------------- 12 · la filtración y Starfield (198-268)
    aviso("En el doce", 12, "El nombre se filtró"),
    ficha("El veintinueve de octubre", "The Verge · Tom Warren", "*29 de octubre*: «Sentinel», en Hammerfell", "Filtración", dur=5.5),
    rel("historia de los propios Pergaminos", "pergamino_sr", "Pergaminos Antiguos", "El tema del juego, según The Verge", dur=4.2),
    ficha("tu número de empleado", "Starfield · 2023", "Número de empleado *siempre el mismo*", "Al crear tu personaje", dur=4.0),
    mg(T.cifrado("Número de empleado · Starfield", ["19", "05", "14", "20", "09", "14", "05", "12"], "SENTINEL", ("LLEVABA AHÍ DESDE 2023", 4)),
       "uno nueve, cero cinco", ("desde dos mil veintitrés", 1.2), ["uno nueve", "Cambia cada par", "Sale Sentinel", "Sale Sentinel", "Llevaba ahí"],
       "cifrado starfield", y=.42),
    zoom("Bethesda no dijo nada", "El nombre ha salido", 1.12),
    peg("dio por revelado el lugar", "alikr_desierto", "Hammerfell", dur=3.4, x=.18, y=.62, tam=420),
    ficha("Lo que no ha salido es fecha", "The Elder Scrolls VI: Sentinel", "Fecha: *—* · Consolas: *—*", "«Aún pasará un tiempo»", dur=5.5, rojo=True),
    mis("Traducido: siéntate", "Consejo", "Siéntate", dur=2.8, y=.72),

    # ---------------- 11 · Sentinel existe (268-328)
    aviso("Número once", 11, "Sentinel existe"),
    mapa("iliac.jpg", "Hammerfell", [(.354, .77, "Sentinel", "inicio", P("alikr_desierto")), (.27, .58, "Bahía de Iliac", "paso"),
                                    (.30, .95, "Desierto de Alik'r", "meta")],
         "Sentinel es la capital de Hammerfell", ("al sur", .8), ["Sentinel es la capital", "bahía de Iliac al norte", "al sur"],
         "La capital de los redguard", ventana=True, ancho=1150),
    cam("la provincia de los redguard", "redguard", "Redguard", dur=3.0, x=.16, y=.66, foco=(.5, .3, 1.6)),
    mapa("hammerfell.jpg", "Hammerfell", [(.93, .07, "Skyrim", "inicio"), (.58, .17, "Cola del Dragón", "paso"), (.40, .31, "El Alik'r", "paso"),
                                         (.133, .457, "Sentinel", "meta", P("alikr_desierto"))],
         "Si sales de Skyrim", ("Ahí está", .8), ["Skyrim hacia el oeste", "Cola del Dragón", "atraviesas el Alik'r", "llegas al mar"],
         "De Skyrim a Sentinel", ventana=True, ancho=1300, x=.60, y=.48),
    ficha("Empezó como un puesto", "Sentinel", "Nació como *puesto de vigía*", "Pescadores y mercaderes", dur=4.5),
    mis("Un centinela. Sentinel", "Sentinel", "= Centinela", dur=2.6, y=.70),
    peg("Sale en Daggerfall", "daggerfall_logo", "Daggerfall · 1996", dur=3.4, x=.16, y=.60, tam=360, giro=6),
    mapa("sentinel_eso.jpg", "Sentinel", [(.27, .24, "El puerto", "inicio"), (.62, .72, "El palacio", "meta")],
         "en The Elder Scrolls Online es la capital", ("su palacio", 1.6), ["Online es la capital", "su palacio"], "Sentinel en ESO · 2E 582"),
    ficha("si no puedes esperar", "The Elder Scrolls Online", "Sentinel, *2E 582*", "Casi mil años antes", dur=5.0),

    # ---------------- CRÍTICA 1 · @alcoholikmisanthroper1934 (328-370)
    mis("Una pausa, que hoy toca correo", "Correo del canal", "Crítica n.º 1", dur=2.6, y=.18),
    com("nos escribió esto en el video", C_ALCO, dur=13.0, x=.50, y=.40, tam=1000),
    rel("Lo de la recarga es verdad", "daga_hueso", "Daga de hueso de dragón", "Sin encantamiento: no se gasta", dur=4.5, x=.78, y=.52, tam=480),
    mis("Apuntado, y gracias", "Corrección", "Apuntada", dur=2.4, y=.72),
    mis("se llama número uno", "Lógica de las listas", "Número uno = al final", dur=3.2, y=.30),
    mg_en(T.contadores("Gracias por", [("Ver el video hasta el final", 100, None, None)], remate=("RETENCIÓN", 0)), "se llama retención", 4.0,
          "retencion", x=.70, y=.36),

    # ---------------- 10 · la ciudad que se tragó a sus vecinos (370-458)
    aviso("En el diez", 10, "La ciudad que se tragó a sus vecinos"),
    sil("gobernado por la reina Akorithi", "akorithi", "Reina Akorithi", "Sentinel · Daggerfall", dur=5.0, lado="izq", alto=820),
    leg("akorithi", "Expediente: Arthago", ["Primogénito de Akorithi", "Desaparece de niño", "Culpables: sus padres"],
        "Su primogénito, Arthago", ("dejar morir en una mazmorra", 1.0), ["Su primogénito", "Se culpó", "La verdad era peor"],
        sello=("SECUESTRO", 2), x=.78, y=.50),
    rel("el gigante de latón", "numidium", "Numidium", "El gigante de Tiber Septim", dur=4.0, x=.76, y=.50, tam=500),
    cam("Tiber Septim", "tiber", "Tiber Septim", dur=2.8, x=.16, y=.66),
    mg(T.soldados("Lo activaron el mismo día", 7), "Akorithi lo activó para Sentinel", ("el mismo día", .8), ["Akorithi lo activó", "otras seis potencias"],
       "siete potencias", y=.30),
    mis("todos los finales ocurrieron a la vez", "Daggerfall", "Todos los finales a la vez", dur=3.4, y=.30),
    ficha("Lo llaman el Milagro", "Milagro de la Paz", "También llamado *Distorsión del Oeste*", "3E 417", dur=4.6),
    mg(T.rejilla("Ciudades estado de la bahía de Iliac", n=44, encendidas=4, cols=11, ancho=900, remate=("44 → 4 · SENTINEL, LA QUE MÁS GANÓ", 2)),
       "Antes había cuarenta y cuatro", ("ganó fue Sentinel", .8), ["cuarenta y cuatro", "Después, cuatro", "ganó fue Sentinel"], "44 a 4", y=.40),
    grande("En el Muro de Alduin", "muro_alduin", "El Muro de Alduin · Skyrim", dur=4.2, x=.30, tam=620),
    mis("cuando la torre de latón camine", "Profecía del Muro de Alduin", "«Cuando la torre de latón camine»", dur=4.0, y=.78),
    rel("Esa torre es el Numidium", "numidium", "Numidium", "La torre de latón", dur=3.4, x=.78, y=.50, tam=440),
    mis("Guárdate esto", "Pista para el número uno", "El tiempo ya se rompió en Sentinel", dur=4.4, y=.30),

    # ---------------- 9 · esa arena (458-518)
    aviso("Número nueve", 9, "Esa arena no es de cualquier desierto"),
    peg("Hammerfell es la provincia del desierto", "alikr_desierto", "Desierto de Alik'r", dur=3.6, x=.20, y=.62, tam=440, giro=5),
    sil("Los guerreros de Alik'r", "alikr_guerrero", "Guerrero de Alik'r", "Carrera Blanca", dur=4.0, lado="der", alto=860),
    sil("Ella es Saadia", "saadia", "Saadia", "La Yegua Abanderada", dur=4.0, lado="izq", alto=860),
    mg(T.versiones("Dos versiones de la misma mujer", (P("saadia"), "Saadia", ["Noble de la Casa Suda", "Perseguida por los Thalmor"], 0),
                   (P("kematu"), "Kematu", ["Cuenta otra historia", "Busca a una traidora"], 1)),
       "Dice ser Iman", ("cuenta otra historia", 1.2), ["Dice ser Iman", "Kematu, el jefe"], "saadia kematu", y=.46),
    cam("tienes a Nazir", "nazir", "Nazir", dur=3.2, x=.16, y=.66, foco=(.5, .22, 2.2)),
    rel("comparte cara con el Guerrero de Ébano", "guerrero_ebano", "Guerrero de Ébano", "La misma cara que Nazir", dur=4.0, x=.78, y=.50, tam=460),
    mis("la mitad elegiste mal", "Misión", "En mi hora de necesidad", dur=3.4, y=.30),

    # ---------------- 8 · el pueblo de Yokuda (518-560)
    aviso("En el ocho", 8, "El pueblo que llegó huyendo"),
    ficha("Vienen de Yokuda", "Yokuda", "Continente al *oeste*, hundido en el mar", "Origen de los redguard", dur=4.6),
    mis("los Ra Gada", "La ola de guerreros", "Ra Gada", dur=3.4, y=.30),
    cam("los Cantores de Espadas", "redguard", "Cantor de Espadas", dur=3.4, x=.16, y=.66, foco=(.5, .3, 1.6)),
    ficha("La llamaban Shehai", "Shehai", "La *espada del espíritu*", "Se invoca con la mente", dur=4.2),
    rel("Un pueblo de espadachines", "cimitarra", "Cimitarra", "El arma de Hammerfell", dur=4.0, x=.78, y=.50, tam=440),
    mis("que lo haga un mod", "Plan B", "Que lo haga un mod", dur=2.8, y=.72),

    # ---------------- AGRADECIMIENTOS (560-603)
    mis("esta para dar las gracias", "Correo del canal", "Gracias", dur=4.5, y=.16),
    com("nos dijo que ni al trabajo", C_BVSQ, dur=8.0, x=.30, y=.28, tam=720),
    com("nos dejó un muy buen video", C_SKEL, dur=7.6, x=.70, y=.44, tam=720),
    com("dice que esta serie", C_HECT, dur=6.6, x=.32, y=.62, tam=720),
    com("buen video por cierto", C_ADOL, dur=6.8, x=.70, y=.78, tam=720),
    mis("Leemos todos los comentarios", "Siempre", "Los leemos todos", dur=7.0, y=.16),

    # ---------------- 7 · la fecha (603-650)
    aviso("Número siete", 7, "La fecha del teaser"),
    pant("t_cita", "va firmada con fecha", ("doscientos seis", .8), zoom=(1.0, 1.12)),
    mg(T.cronologia("La línea del tiempo", [("4E 201", "Empieza Skyrim", 0), ("4E 206", "Firma de la cita", 1)]),
       "Skyrim empieza en la cuarta era", ("rumbo a Helgen", .8), ["Skyrim empieza", "cinco años después"], "4e201 a 206", y=.32),
    cam("Después de Alduin", "alduin", "Alduin", dur=2.6, x=.14, y=.66, foco=(.5, .4, 1.4)),
    aba([("ulfric", "Ulfric"), ("tullius", "Tullius")], "la guerra civil entre Ulfric", ("Con los Thalmor", -.1), ["Ulfric", "Tullius"], "guerra civil",
        x=.30, y=.64),
    cam("Con los Thalmor todavía", "elenwen", "Thalmor", dur=2.8, x=.84, y=.62),
    mis("la primera vez que la saga se pone después", "Primera vez", "Después de Skyrim", dur=3.4, y=.72),

    # ---------------- 6 · la reina Iradne (650-688)
    aviso("En el seis, una reina", 6, "Una reina que no conocía nadie"),
    ficha("Alta Reina Iradne de Hammerfell", "Alta Reina Iradne", "Reina de *toda* Hammerfell", "Nueva en la saga", dur=5.0),
    mis("En ningún juego anterior", "Personaje nuevo", "Iradne", dur=3.0, y=.72),
    mg(T.balanza("La pelea de Hammerfell", ("Las Coronas · nobleza de Yokuda", None), [("Los Antepasados · abiertos al Imperio", None)],
                 remate=("¿QUIÉN GANÓ?", 2)),
       "dos bandos", ("unirlos a la fuerza", .8), ["las Coronas", "los Antepasados", "alguien ha tenido que ganar"], "coronas antepasados", y=.46),

    # ---------------- CRÍTICA 2 · @JoseAkua (688-725)
    mis("Una pausa más", "Correo del canal", "Crítica n.º 2", dur=2.6, y=.18),
    com("nos dejó una orden muy clara", C_JOSE, dur=10.0, x=.50, y=.40, tam=1000),
    mis("Le hemos dado el recado", "Recado", "Entregado", dur=2.6, y=.72),
    mg_en(T.contadores("Fuentes de este video", [("Enlaces en la descripción", 15, None, None), ("Comprobaciones de la fecha", 2, None, None)],
                       remate=("CON BIBLIOGRAFÍA", 0)), "cada dato lleva su enlace", 6.0, "fuentes", x=.72, y=.36),
    mis("el despropósito vino con bibliografía", "Despropósito", "Con bibliografía", dur=3.6, y=.30),

    # ---------------- 5 · la victoria de Hammerfell (725-790)
    aviso("Número cinco", 5, "La victoria que Hammerfell ganó sola"),
    ficha("en el Concordato de Oro Blanco", "Concordato de Oro Blanco", "Paz con los Thalmor · cede parte del *sur de Hammerfell*", "4E 175",
          dur=5.5, rojo=True),
    cam("con los Thalmor en el Concordato", "elenwen", "Thalmor", dur=3.0, x=.16, y=.66),
    mis("Sin legiones, sin Emperador", "Hammerfell", "Sola", dur=3.0, y=.72),
    ficha("Segundo Tratado de Stros", "Segundo Tratado de Stros M'Kai", "Hammerfell *expulsa* a los Thalmor", "Victoria redguard", dur=5.0),
    mapa("hammerfell.jpg", "Hammerfell", [(.133, .457, "Sentinel", "inicio"), (.216, .915, "Stros M'Kai", "meta")],
         "Y ganó", ("Stros M'Kai", 1.2), ["Echó a los Thalmor", "Stros M'Kai"], "La paz se firmó en Stros M'Kai", ventana=True, ancho=1000, x=.30, y=.45),
    mis("La Noche del Fuego Verde", "4E 42 · Sentinel", "La Noche del Fuego Verde", dur=4.0, y=.30),
    sil("te lo cuenta el legado Fasendil", "fasendil", "Legado Fasendil", "Te lo cuenta en Skyrim", dur=4.4, lado="der", alto=860),
    mis("Dice: una victoria deshecha", "La cita", "«Una victoria deshecha»", dur=3.6, y=.72),
    zoom("Qué victoria se puede deshacer", ("demasiado bien", .5), 1.16),

    # ---------------- 4 · el sacerdote (790-850)
    aviso("En el cuatro", 4, "Un sacerdote que no debería estar ahí"),
    sil("Quien firma es Yazar", "dexion", "Sacerdote de la Polilla", "Como Yazar, el de la cita", dur=4.6, lado="izq", alto=860),
    rel("leer los Pergaminos Antiguos sin", "pergamino_sr", "Pergaminos Antiguos", "Solo ellos los leen", dur=3.6, x=.78, y=.50, tam=460),
    ficha("en la Torre de Oro Blanco", "Biblioteca Imperial", "En la *Torre de Oro Blanco*", "Allí se guardaban los pergaminos", dur=4.6),
    cam("el de Dawnguard", "dexion", "Dexion Evicus", dur=3.0, x=.16, y=.66),
    mg(T.cronologia("Los pergaminos", [("Antes", "En la Biblioteca Imperial", 0), ("4E 175", "Fin de la Gran Guerra: desaparecen", 1),
                                       ("4E 206", "Un sacerdote sirve a Hammerfell", 2)]),
       "Pero en la cuarta era, ciento setenta", ("rompió con el Imperio", .8), ["Pero en la cuarta era", "desaparecieron", "dice servir a la reina"],
       "pergaminos 175", y=.32),
    mg(T.informe("Hipótesis", (P("dexion"), "Sacerdote de la Polilla"),
                 [("1", "La orden se ha partido", 0), ("2", "El Imperio ha caído", 1), ("3", "Hammerfell tiene un pergamino", 2)],
                 sello=("¿CUÁL?", 3)),
       "o la orden se ha partido", ("sabe leerlo", .8), ["la orden se ha partido", "el Imperio ha caído", "Hammerfell tiene ahora", "Un pergamino"],
       "hipotesis", y=.46),

    # ---------------- 3 · lo que cuesta leer (850-907)
    aviso("Número tres", 3, "Lo que le cuesta leer"),
    mg(T.ceguera("Sacerdote de la Polilla", P("dexion"), [("Primera lectura", 0), ("Meses de espera", 1), ("Lectura con prisas: ciego", 2)],
                 ("CADA LECTURA CUESTA VISTA", 3)),
       "Cada lectura le quita", ("del todo", .3), ["Cada lectura", "un poco de vista", "ciego del todo", "ciego del todo"], "ceguera", y=.40),
    mis("Algunos esperan meses", "Para no quedarse ciego", "Meses entre lecturas", dur=3.6, y=.72),
    rel("Dexion Evicus lee tres", "pergamino_sr", "Tres pergaminos", "Dawnguard", dur=4.0, x=.78, y=.50, tam=440),
    mis("el que tiene que leer eres tú", "Misión", "Lees tú el pergamino", dur=3.4, y=.30),
    grande("en la Arboleda Ancestral", "arbol_cantico", "Arboleda Ancestral", dur=4.0, x=.28, tam=600),
    peg("las polillas vienen a ti", "polilla", "Polillas ancestrales", dur=3.4, x=.80, y=.60, tam=420, giro=5),
    pant("t_cita", "Ahora relee la frase", ("ante mis ojos", 1.0), zoom=(1.0, 1.10)),
    mis("Yazar no está contando", "Lo que vio Yazar", "Casi nada", dur=3.6, y=.72),

    # ---------------- CAMPAÑA DE SUSCRIPCIÓN (907-928)
    mg(T.rejilla("De cada cien que ven el canal", n=100, encendidas=13, remate=("SOLO 13 SUSCRITOS", 2)),
       "De cada cien que ven", ("están suscritos", 1.2), ["De cada cien", "solo trece", "solo trece"], "suscritos", y=.42),
    mg(T.contadores("Crónicas de Tamriel", [("Suscriptores hoy", 6450, None, 0), ("Meta", 10000, 1, 2)], remate=("ANTES DE QUE SENTINEL TENGA FECHA", 3)),
       "Somos seis mil", ("tiempo de sobra", .8), ["Somos seis mil", "Si te suscribes", "diez mil", "antes de que Sentinel"], "meta subs", y=.40),
    mis("viendo a Bethesda", "Siguiente objetivo", "10 000 suscriptores", dur=3.4, y=.20),

    # ---------------- 2 · el pergamino (928-1003)
    aviso("En el dos", 2, "El pergamino no es un adorno"),
    pant("t_scroll", "sale un Pergamino Antiguo", ("a su alrededor", .8), zoom=(1.0, 1.14)),
    ficha("fragmentos de la creación", "Pergamino Antiguo", "Fragmento de la creación, *fuera del tiempo*", "Lo que pasó y lo que podría pasar", dur=8.0),
    mis("puede cambiar de una lectura a otra", "Pergaminos", "Cambian si la profecía no se cumple", dur=4.0, y=.72),
    rel("el fondo del pergamino que lees", "pergamino_sr", "El pergamino de Skyrim", "Fondo: cielo del polo sur", dur=4.2, x=.78, y=.50, tam=440),
    peg("El mismo que en Oblivion", "oblivion_logo", "Oblivion", dur=3.0, x=.16, y=.62, tam=340, giro=6),
    mis("Lo enseña enterrado en la arena", "4E 175", "Perdidos y dispersos", dur=8.0, y=.72),
    ficha("Si The Verge acierta", "The Verge", "El primer juego sobre *los pergaminos*", "Sin confirmar por Bethesda", dur=9.0, rojo=True),
    mg_en(T.contadores("The Elder Scrolls", [("Años de saga", 30, None, None), ("Entregas", 6, None, None)], remate=("POR FIN VA DE LOS PERGAMINOS", 0)),
          "Llevamos treinta años", 9.0, "30 anios", x=.72, y=.36),

    # ---------------- CRÍTICA 3 · @nyarlathotep2265 (1003-1035)
    mis("la última carta del día", "Correo del canal", "Crítica n.º 3", dur=2.6, y=.18),
    com("nos escribió que están mejor", C_NYAR, dur=9.0, x=.50, y=.40, tam=1000),
    mis("si no lo sigues, síguelo", "Recomendación", "El Gerber", dur=3.0, y=.72),
    mg_en(T.contadores("Para que se entienda", [("Mapas", 5, None, None), ("Fechas", 6, None, None), ("Dibujos", 40, None, None)]),
          "hoy hemos traído mapas", 5.0, "mapas fechas dibujos", x=.72, y=.36),
    mis("Muy despacio", "Modo", "Muy despacio", dur=2.6, y=.30),

    # ---------------- 1 · la frase entera (1035-1125)
    aviso("Y llegamos al número uno", 1, "La frase entera"),
    pant("t_cita", "El teaser termina así", ("dispersas por el destino", 1.0), zoom=(1.0, 1.12)),
    mg(T.lecturas("Una victoria deshecha", CITA[1:], [("La guerra", "Los Thalmor vuelven a Hammerfell", 1),
                                                     ("El tiempo", "Un pergamino que cambia la historia", 2),
                                                     ("Los Thalmor", "Talos prohibido: Skyrim no sirvió de nada", 3)]),
       "Primera lectura, la política", ("Tercera lectura", -.2), ["Primera lectura", "Primera lectura", "Segunda lectura", "Tercera lectura"],
       "lecturas 1 2", y=.30),
    cam("Los elfos vuelven", "elenwen", "Thalmor", dur=3.0, x=.84, y=.78, tam=260),
    peg("Arenas del tiempo dispersas por el destino. Los", "herida_tiempo", "La Herida del Tiempo · Skyrim", dur=4.0, x=.82, y=.78, tam=360, giro=5),
    mis("cuando todos los finales de Daggerfall", "Daggerfall", "Distorsión del Oeste", dur=3.6, y=.86),
    mg(T.lecturas("Una victoria deshecha", CITA[1:], [("La guerra", "Los Thalmor vuelven a Hammerfell", 0),
                                                     ("El tiempo", "Un pergamino que cambia la historia", 0),
                                                     ("Los Thalmor", "Talos prohibido: Skyrim no sirvió de nada", 1)]),
       "Tercera lectura, la más oscura", ("prohibir el culto", -.1), ["Tercera lectura", "Tercera lectura"], "lecturas 3", y=.30),
    ban("prohibir el culto a Talos", "talos", "Talos", "Prohibido por el Concordato", foco=(.5, .35, 1.4), dur=4.0, y=.70),
    aba([("alduin", "Alduin"), ("ulfric", "La guerra civil"), ("talos_estatua", "Talos")], "lo que hiciste en Skyrim, la guerra civil",
        ("Todo esto es teoría", -.2), ["la guerra civil", "Alduin", "todo"], "skyrim deshecho", x=.30, y=.64),
    mg_en(T.contadores("Lo que dio Bethesda", [("Frases", 4, None, None)], remate=("ALGO VIO", 0)), "Bethesda solo nos ha dado", 9.0,
          "cuatro frases", x=.72, y=.36),

    # ---------------- cierre (1125-1161)
    mis("Esos son los quince secretos", "Misión completada", "15 secretos del teaser", dur=7.5, y=.25),
    mg(T.lecturas("¿Cuál te convence?", ["Déjalo en los comentarios"], [("La guerra", "", 0), ("El tiempo", "", 1), ("Los Thalmor", "", 2)]),
       "Cuál de las tres lecturas", ("Déjalo en los comentarios", 1.0), ["la guerra", "el tiempo", "o los Thalmor"], "encuesta", y=.42),
    mis("los cuarenta secretos de Skyrim", "En el canal", "40 secretos de Skyrim", dur=4.0, y=.72),
    mis("Suscríbete si aún no", "Crónicas de Tamriel", "Suscríbete", dur=8.0, y=.30),
    # ---------------- rellenos de huecos > 4 s (`_huecos.py`, 3-nov-2026)
    mg_en(T.contadores("El teaser", [("Segundos", 65, None, None)]), "Parece poco", 3.4, "duracion teaser", x=.76, y=.32),
    ficha("El teaser no empieza", "El teaser", "*65* segundos de arena y un pergamino", "The Elder Scrolls VI: Sentinel", dur=5.0),
    mis("qué mejor momento", "Todd Howard", "«¿Cómo se llama?»", dur=3.4, y=.72),
    mis("niebla, colinas", "Lo que se veía", "Niebla, colinas, costa, fortaleza", dur=5.0, y=.72),
    mis("como si fueran detectives", "Fans", "Modo detective", dur=3.0, y=.72),
    mis("que estaría en Hammerfell", "Según The Verge", "Hammerfell", dur=3.4, y=.72),
    mis("una pista todavía más vieja", "Pista", "Starfield · 2023", dur=3.4, y=.30),
    mis("Hasta hoy", "Bethesda", "Silencio... hasta hoy", dur=3.4, y=.72),
    mis("Casi mil años antes", "The Elder Scrolls Online", "Segunda Era", dur=3.6, y=.72),
    mis("Daggerfall tenía varios finales", "Daggerfall", "Varios finales", dur=3.4, y=.72),
    mis("dunas que el viento", "El teaser", "Arena en movimiento", dur=3.4, y=.72),
    ficha("uno de los más duros", "Desierto de Alik'r", "Uno de los más *duros* de Tamriel", "Hammerfell", dur=4.6),
    mis("tu primer dragón", "Tras matar a", "Mirmulnir", dur=3.4, y=.72),
    cam("Los redguard no son", "redguard", "Redguard", dur=3.4, x=.16, y=.66, foco=(.5, .3, 1.6)),
    mis("Llegaron en barcos", "Yokuda → Tamriel", "En barcos", dur=3.4, y=.72),
    mis("Si Elder Scrolls seis no aprovecha", "Petición a Bethesda", "Cantores de Espadas", dur=3.0, y=.30),
    ficha("la cita es de esa fecha", "La cita", "Fechada en *4E 206*", "El juego podría pasar más tarde", dur=5.0),
    mis("ya es historia de Tamriel", "Skyrim", "Historia de Tamriel", dur=3.4, y=.72),
    mis("Alta Reina, de toda la provincia", "El título", "Alta Reina de Hammerfell", dur=3.4, y=.30),
    cam("Hammerfell casi nunca", "redguard", "Hammerfell", dur=3.4, x=.16, y=.80, foco=(.5, .3, 1.6)),
    pant("t_cita", "Hasta la fecha del teaser", ("Ya lo ves", 0.0), zoom=(1.0, 1.08)),
    mis("Hammerfell no lo aceptó", "Hammerfell", "Se separa del Imperio", dur=3.4, y=.30),
    ficha("sus agentes atacaron", "Sentinel · 4E 42", "Los Thalmor arrasan el barrio *altmer*", "La Noche del Fuego Verde", dur=5.0, rojo=True),
    aba([("tullius", "El Imperio"), ("elenwen", "Los elfos")], "Por eso los redguard no se fían", ("Y por eso la frase", .2),
        ["del Imperio", "de los elfos"], "imperio elfos", x=.30, y=.64),
    mis("Hay una que encaja", "Pista", "La victoria contra los Thalmor", dur=3.6, y=.72),
    mis("Su orden servía al Imperio", "Sacerdotes de la Polilla", "Al servicio del Imperio", dur=3.4, y=.72),
    ficha("Nos está diciendo que apenas", "Yazar", "Vio *casi nada*", "Y le costó la vista", dur=5.0, rojo=True),
    mis("Antes de los dos últimos", "Un dato", "Antes del top 2", dur=2.6, y=.30),
]

# ---- SIETE VOCES (el usuario, 3-nov-2026): placa de quién narra en cada presentación y en cada cambio de voz (lo que dice la voz
# se ve), abajo a la derecha; la papeleta de la votación en el cierre (cada voz marca su casilla cuando pide el voto)
VOCES = ["Johnny", "Edoardo", "Hope", "José", "Mario", "MariCarmen", "el Profeta"]
_LEMA = {"Johnny": "El quince y el catorce", "Edoardo": "El trece y el doce", "Hope": "El once y el diez", "José": "El nueve y el ocho",
         "Mario": "El siete y el seis", "MariCarmen": "El cinco y el cuatro", "el Profeta": "El tres, el dos y el uno"}


def narra(en, nombre, dur=4.0, lema=None):
    n = VOCES.index(nombre) + 1 if nombre in VOCES else None
    return dict(tipo="mg", fn=T.narrador(nombre, lema or _LEMA[nombre], n, 7 if n else None), en=en, dur=dur, x=.80, y=.83,
                sale=.35, nombre="placa narra " + nombre, ver=1.2)


NARRA = [
    narra("Edoardo. Me tocan", "Edoardo"), narra("Yo soy Hope", "Hope"), narra("José, para servirte", "José"),
    narra("Mario. La fecha", "Mario"), narra("MariCarmen. La guerra", "MariCarmen"), narra("Yo soy el Profeta", "el Profeta"),
    narra("Qué humildad", "Johnny"),
    narra("Gracias, Johnny", "Edoardo"), narra("Precioso, Edoardo", "Hope"), narra("Hope, eso de la ciudad", "José"),
    narra("Y aquí me cuelo yo", "El Jefe", dur=6.0, lema="El que lee los comentarios"),
    narra("Gracias, jefe", "Mario"), narra("Mario, respira", "MariCarmen"), narra("Gracias, MariCarmen", "el Profeta"),
    mg(T.votacion("¿Qué voz se queda?", VOCES, "Un nombre en los comentarios"), "Y ya que estás en los comentarios", ("Qué miedo", 2.5),
       ["Qué miedo", "Edoardo. El único", "Hope. Con hache", "José, con acento", "Mario. El único", "MariCarmen, todo junto",
        "Yo no pido votos", "Un nombre, y listo"], "votación", y=.45),   # marcas en el orden de VOCES + remate
]
FX = VIDEOS + FX + NARRA

# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número quince", "Número trece", "Número once", "Número nueve",
                                                                 "Número siete", "Número cinco", "Número tres")]
PISTAS += [dict(sfx="mision_iniciada", en=e, vol=.20) for e in ("En el catorce", "En el doce", "En el diez", "En el ocho", "En el seis, una reina",
                                                                "En el cuatro", "En el dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in ("Si sales de Skyrim", "La apuesta más repetida", "Online es la capital")]
PISTAS += [dict(sfx="subir_nivel", en="Y llegamos al número uno", vol=.24), dict(sfx="subir_nivel", en="Hoy te traigo quince secretos", vol=.18),
           dict(sfx="mision_completada", en="Esos son los quince secretos", vol=.22), dict(sfx="grito", en="Esa torre es el Numidium", vol=.16)]
