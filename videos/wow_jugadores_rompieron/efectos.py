# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 10 jugadores REALES que ROMPIERON WoW Vanilla» (motor SECUENCIA YT, Crónicas de Warcraft, 27-oct-2026).
- Segmento Overgear campaña 2 (coaching self-play de WoW Forever; scene-029..034): insignias en pares con croma, recorrido por
  overgear.com/games/wow-forever/coaching como clip de scene-031 (el brief exige screencast), logo y la IMAGEN del tramo del
  creativo con CRONICAS10 (33,0-39,97 s) justo antes de scene-035, SIN su audio (el código lo dice nuestra voz).
- MG NUEVOS de este guion (nucleo/mg_wow.py): `reckoning` (cargas sin tope → Kazzak en segundos → parche: máx. 4),
  `inmortal` (Kazzak en Ventormenta: cada muerte le rellena la barra; entra un MJ) y `expediente` (Blizzard contra Glider).
- MAPAS REALES con ruta y foto en cada paso: las zonas prohibidas de la RIdPEF, Kazzak de las Tierras Devastadas a Ventormenta
  y las puertas de Ahn'Qiraj.
- Pegatinas de cada jefe/objeto nombrado (Wowpedia), tooltips de Wowhead es-MX y tarjetas SOLO con datos del guion.
  python fab.py wow_jugadores_rompieron apoyos | fx hoja | fx
"""
import os

import mg_tes as T
import mg_wow as M

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"                   # copias de D:\Cronicas de Warcraft\Overgear\ y del creativo de Descargas
CREATIVO = OG + "overgear_promo_ES_remy_preview_720p.mp4"
CODIGO = ("scene-035", -6.97)                      # el tramo (6,97 s) termina justo donde empieza el puesto 7; entra con «CRONICAS10»


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.5, x=.25, tam=660):
    return peg(en, slug, titulo, dur, x, .50, tam)


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.7, zmin=1.0):
    """Mapa real a cuadro entero con la ruta (mg_wow.ruta): un pin por paso en su marca, con la foto de lo que se nombra."""
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin,
                                           objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def kal(x, y):
    """% del mapa de Kalimdor (-6) -> % del mapa del mundo (-1) (calibrado en wow_objetos_raros, 22-oct-2026)."""
    return (128 + (x / 100 * 1022 - 385) * .826) / 1024 * 100, (130 + (y / 100 * 668 - 100) * .858) / 683 * 100


def ek(x, y):
    """% del mapa de los Reinos del Este (-3) -> % del mapa del mundo (-1)."""
    return (700 + (x / 100 * 1024 - 400) * .785) / 1024 * 100, (285 + (y / 100 * 683 - 290) * .786) / 683 * 100


def pk(xy, t1, t2=None, foto=None):
    return (*kal(*xy), t1, t2, foto)


def pe(xy, t1, t2=None, foto=None):
    return (*ek(*xy), t1, t2, foto)


CAMARA = {}
FUNDIDO = {
    "scene-035": 0,                                # corte seco del creativo («LINK IN THE DESCRIPTION») al «Número siete»
}
FX = [
    # =========================================================== intro
    peg("Uno mató a un jefe pensado", "paladin", "Un paladín", dur=3.6),
    gran("Otros arrastraron a un demonio", "kazzak", "Lord Kazzak", dur=4.2, x=.74),
    # =========================================================== 10 Dives / Onyxia
    gran("la guarida de Onyxia con el chat", "onyxia", "Onyxia", dur=4.5, x=.75),
    peg("salen decenas de crías de dragón", "whelp", "Cría de Onyxia", dur=4.0),
    peg("El grupo murió entero", "whelp", "Cría de Onyxia", dur=3.0, x=.47, y=.66, tam=330),
    peg("Onyxia vuelve en Forever", "onyxia", "Onyxia · nivel 60", dur=4.0),
    # =========================================================== 9 Jokerd
    peg("Le dio a borrar y el juego no lo dejó", "carta", "Correo sin leer", dur=4.6, x=.50, y=.40, tam=360),
    # =========================================================== 8 Death and Taxes
    peg("Contra Firemaw", "firemaw", "Firemaw", dur=3.6, x=.13, tam=360),
    peg("hasta la sala de Vaelastrasz", "vaelastrasz", "Vaelastrasz", dur=3.6, x=.33, tam=360),
    gran("Contra Viscidus", "viscidus", "Viscidus", dur=4.2, x=.25, tam=600),
    peg("Contra Loatheb", "loatheb", "Loatheb", dur=4.0),
    peg("en Chromaggus los maestros", "chromaggus", "Chromaggus", dur=3.4, x=.13, tam=360),
    peg("llegaron a intervenir", "gm", "Maestros de juego", dur=3.6, x=.36, tam=360),
    # =========================================================== Overgear (campaña 2, 26-oct-2026): insignias EN PARES (kit de marca)
    dict(tipo="video", ruta=OG + "1 pair_green.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25,
         nombre="og pros"),
    dict(tipo="video", ruta=OG + "2 pair_green.mp4", croma=True, en="Tácticas de jefes, mazmorras", dur=4.0, sale=.25,
         nombre="og coaching"),
    dict(tipo="video", ruta=OG + "3 pair_green.mp4", croma=True, en="tú eliges, y pagas", dur=3.8, sale=.25, nombre="og trustpilot"),
    dict(tipo="video", ruta=OG + "packshot-logo_greenscreen.mp4", croma=True, en="El enlace está en la descripción", a=CODIGO,
         entra=.2, nombre="og logo", ver=2.0),
    dict(tipo="video", ruta=CREATIVO, desde=33.0, de=CODIGO, a="scene-035", nombre="og CODIGO", ver=3.0),
    # =========================================================== 7 Joana (contadores: lo único con cifras del guion)
    dict(tipo="mg", fn=M.contadores("JOANA · DEL NIVEL 1 AL 60", [
        ("ability_hunter_beastcall", "Días de tiempo jugado (2006)", 4, 0, 1),
        ("ability_hunter_beastcall", "Horas más", 20, 0, 1),
    ], remate=("RÉCORD MUNDIAL", 2)), de=("subió de nivel uno a sesenta", -.2), a=("y lo grabó todo|fin", 2.2),
        marcas=["subió de nivel uno", "y veinte horas", "y lo grabó todo"], y=.74, sale=.4, nombre="MG joana 2006", ver=2.0),
    dict(tipo="mg", fn=M.contadores("CLASSIC · 13 AÑOS DESPUÉS", [
        ("ability_hunter_beastcall", "Días de tiempo jugado (2019)", 4, 0, 1),
        ("ability_hunter_beastcall", "Horas más", 11, 0, 1),
    ]), de=("lo bajó todavía más", -.2), a=("cuatro días y once horas|fin", .5),
        marcas=["lo bajó todavía más", "y once horas"], y=.74, sale=.4, nombre="MG joana 2019", ver=2.0),
    # =========================================================== 6 RIdPEF: lo prohibido en el mapa del mundo
    mapa("azeroth_eses", [pk((43, 11), "Teldrassil", "punto de partida"),
                          pk((57, 33), "Monte Hyjal", "decorado en Vanilla", F("hyjal")),
                          pe((45, 53), "Viejo Forjaz", "Dun Morogh", F("ironforge")),
                          pe((47.5, 51), "Aeropuerto de Forjaz", "zona sin terminar"),
                          pe((45.5, 67), "Bajo Ventormenta", "los túneles", F("stormwind")),
                          pe((42, 37), "Gilneas", "detrás de la muralla"),
                          pe((50, 79), "Zul'Gurub", "por fuera")],
         ("Así pisaron el monte Hyjal", -.3), ("pero fue cerrando cada camino|fin", .4),
         ["Así pisaron el monte", "cuando en el mapa era", "Encontraron el viejo Forjaz", "el famoso aeropuerto",
          "los túneles bajo Ventormenta", "Gilneas detrás", "Zul'Gurub por fuera"],
         "LA RIDPEF", "lo que no se podía pisar", zmax=1.9),
    gran("Hyjal Summit es una de las dos primeras", "hyjal", "Monte Hyjal", dur=4.6, x=.74),
    # =========================================================== 5 Kalahad: el gong
    mapa("azeroth_eses", [pk((42, 88), "Puertas de Ahn'Qiraj", "Silithus", F("gong"))],
         ("Miles de jugadores se juntaron", -.3), ("el servidor se cayó|fin", .4),
         ["se juntaron en Silithus", "sonó el gong"], "MEDIVH · ENERO DE 2006", "el primer gong del mundo",
         objeto="inv_misc_qirajicrystal_05", zmax=1.8),
    gran("el tanque qiraji negro", "tanque_negro", "Tanque qiraji negro", dur=4.6, x=.25, tam=620),
    # =========================================================== 4 Kazzak en Ventormenta
    dict(tipo="mg", fn=M.inmortal(F("kazzak"), "Lord Kazzak", "jefe de mundo · 40 jugadores", "LA REGLA DE KAZZAK",
                                   "SE CURA"),
         de=("con una regla muy peligrosa", -.2), a=("Cada vez que un jugador moría cerca de él, se curaba|fin", 1.2), marcas=["con una regla", "Cada vez que un jugador",
                                                                                   "se curaba"],
         y=.70, sale=.4, nombre="MG kazzak regla", ver=1.0),
    mapa("reinos_este_eses", [(55.5, 80, "Tierras Devastadas", "su casa", F("kazzak")),
                              (45.5, 67, "Ventormenta", "capital de la Alianza", F("stormwind"))],
         ("Jugadores de la Horda, en el servidor", -.2), ("Y Ventormenta estaba llena", 1.5),
         ["lo provocaron", "zona tras zona"], "LA MUDANZA DE KAZZAK", "Kel'Thuzad (EE. UU.)", zmax=1.8),
    dict(tipo="mg", fn=M.inmortal(F("kazzak"), "Lord Kazzak", "en plena Ventormenta", "VENTORMENTA, LLENA DE JUGADORES",
                                   "INMORTAL", retiro=(F("gm"), "Un maestro de juego")),
         de=("Y Ventormenta estaba llena", -.2), a=("saca a un perro de la cocina|fin", .8),
         marcas=["Y Ventormenta estaba llena", "jugadores de bajo nivel", "prácticamente inmortal", "apareció un maestro de juego"],
         y=.70, sale=.4, nombre="MG kazzak inmortal", ver=1.0),
    gran("apareció Highlord Kruul", "kruul", "Highlord Kruul", dur=4.6, x=.75),
    # =========================================================== 3 Overrated
    gran("caminar directo hasta C'Thun", "cthun", "C'Thun", dur=4.6, x=.75, tam=640),
    peg("contra Patchwerk", "patchwerk", "Patchwerk", dur=4.2),
    # =========================================================== 2 Karmerr: la bomba de Reckoning
    peg("Número dos. Karmerr", "paladin", "Karmerr · paladín", dur=4.0),
    dict(tipo="mg", fn=M.reckoning("LA BOMBA DE RECKONING", "spell_holy_blessingofstrength", "Cargas de Reckoning", 1816,
                                    F("kazzak"), "Lord Kazzak", "jefe para 40 jugadores", "PARCHE DEL 12 DE MAYO: MÁXIMO 4"),
         de=("se quedó quieto recibiendo golpes", -.2), a=("el máximo fueron cuatro cargas|fin", 1.4),
         marcas=["se quedó quieto recibiendo", "Cuando juntó mil ochocientas", "buscó a Lord Kazzak", "Mil ochocientos golpes",
                 "corrección urgente el doce de mayo"],
         y=.70, sale=.4, nombre="MG reckoning", ver=1.0),
    # =========================================================== 1 Glider: el expediente
    dict(tipo="mg", fn=M.expediente("BLIZZARD CONTRA GLIDER", [
        ("2005", "Glider: 25 US$ · unas 100 000 copias", None),
        ("2006", "59 000 cuentas baneadas en un mes", M.ROJO),
        ("2006", "Blizzard demanda a Michael Donnelly", None),
        ("2008", "Indemnización: 6 000 000 US$", M.ROJO),
        ("2009", "Glider se apaga por orden judicial", M.ROJO),
        ("2010", "Tribunal de apelaciones de EE. UU.", None),
    ], ("EL JUGADOR NO ES DUEÑO DEL JUEGO", 6), ancho=1360),
        de=("Costaba veinticinco dólares", -.2), a=("solo tiene una licencia para usarlo|fin", 1.6),
        marcas=["Costaba veinticinco", "Blizzard baneó cincuenta", "Blizzard demandó a Donnelly", "se fijó una indemnización",
                "Glider se apagó", "un tribunal de apelaciones", "El jugador no es dueño"],
        y=.56, sale=.4, nombre="MG expediente glider", ver=1.0),
    # =========================================================== cierre: los rotos, en fila
    peg("Unos lo rompieron con talento", "paladin", "Talento", dur=3.0, x=.13, tam=330),
    peg("otros con paredes", "hyjal", "Paredes", dur=2.6, x=.32, tam=330),
    peg("otros con gritos", "whelp", "Gritos", dur=2.4, x=.51, tam=330),
]
ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="6 000 000 US$", en="con una cuenta de seis millones", dur=2.6, tam=140, color="amarillo", y=.2),
    dict(texto="−50 DKP", en="«cincuenta DKP menos»", dur=2.4, tam=170, color="rojo", y=.2),
    dict(texto="CORREGIDO", en="corregido en el parche siguiente", dur=2.4, tam=150, color="rojo", y=.2),
    dict(texto="BANEO PERMANENTE", en="baneo permanente de toda la hermandad", dur=2.8, tam=130, color="rojo", y=.2),
    dict(texto="+60 000 US$", en="más de sesenta mil dólares", dur=2.4, tam=140, color="amarillo", y=.2),
]
SFX = {}
PISTAS = []

# APOYOS: tooltips REALES de Wowhead (classic, es-MX) y tarjetas SOLO con datos del guion (fuentes en videos/_investigacion_wow_jugadores.md)
V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
APOYOS = [
    # ---- 10
    dict(en="los convirtió en logro", dur=5.0, x=.72, size=.52, tarjeta=dict(titulo="Many Whelps! Handle It!", calidad="amarillo",
         icono="achievement_boss_onyxia", lineas=["Logro · parche 3.2.2", "Homenaje a Dives y Wipe Club",
                                                  dict(t="y también: She Deep Breaths More", c=GRIS)])),
    # ---- 9
    dict(en="congelarlos con Nova de escarcha", dur=3.6, x=.72, size=.52, wowhead="classic/spell/122"),
    dict(en="barrerlos con Ventisca", dur=3.6, x=.72, size=.52, wowhead="classic/spell/10"),
    # ---- 8
    dict(en="Abrazo vampírico", dur=4.0, x=.72, size=.52, wowhead="classic/spell/15286"),
    # ---- 7
    dict(en="Número siete. Joana", dur=4.4, x=.72, size=.52, tarjeta=dict(titulo="Joana", calidad="amarillo",
         icono="ability_hunter_beastcall", lineas=["Paul Lucas · cazador", "Servidor Jubei'Thos (EE. UU.)",
                                                   dict(t="1-60 en 4 días y 20 horas", c=V)])),
    dict(en="Joana murió en abril", dur=4.4, x=.72, y=.30, size=.52, tarjeta=dict(titulo="Paul «Joana» Lucas", calidad="gris",
         icono="ability_hunter_beastcall", lineas=["† abril de 2024 · 43 años"])),
    # ---- 6
    dict(en="La RIdPEF, los exploradores", dur=4.6, x=.72, size=.52, tarjeta=dict(titulo="RIdPEF", calidad="amarillo",
         icono="inv_misc_map_01", lineas=["Les Sentinelles (Europa)", "Desde mayo de 2006", dict(t="Sin programas de trampa", c=V)])),
    # ---- 5
    dict(en="para conseguir el cetro", dur=4.4, x=.72, size=.52, wowhead="classic/21175"),
    dict(en="La hermandad Ascent organizó", dur=4.6, x=.72, size=.52, tarjeta=dict(titulo="Kalahad", calidad="amarillo",
         icono="inv_misc_qirajicrystal_05", lineas=["Guerrero enano · líder de Fury", "Medivh (EE. UU.)",
                                                    dict(t="Primer gong del mundo", c=V)])),
    # ---- 3
    dict(en="Número tres. Overrated", dur=4.4, x=.72, size=.52, tarjeta=dict(titulo="Overrated", calidad=ROJO,
         icono="inv_misc_ahnqirajtrinket_05", lineas=["Horda · EE. UU. · noviembre de 2006", "Archivo modificado: Patch-5.MPQ",
                                                      dict(t="Baneo permanente de la hermandad", c=ROJO)])),
    # ---- 2
    dict(en="El talento Reckoning daba", dur=5.0, x=.72, size=.52, tarjeta=dict(titulo="Reckoning (mayo de 2005)", calidad="morado",
         icono="spell_holy_blessingofstrength", lineas=["Golpe extra por cada crítico recibido",
                                                        dict(t="Cargas: SIN LÍMITE", c=ROJO)])),
    # ---- 1
    dict(en="Número uno. Michael Donnelly", dur=4.6, x=.72, size=.52, tarjeta=dict(titulo="Glider", calidad="gris",
         icono="inv_misc_gear_01", lineas=["Michael Donnelly · junio de 2005", "Subía de nivel y juntaba oro solo",
                                           dict(t="Hecho para esconderse de Warden", c=ROJO)])),
]
