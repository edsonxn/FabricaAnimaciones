# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (SECUENCIA YT, Crónicas de Warcraft, 22-nov-2026).
Modelos: videos/wow_ruta_forever/efectos.py (helpers) y videos/wow_errores_30_60/efectos.py (lista + bloque Overgear, /CRONICAS/6).
- Cada puesto: reliquia/pegatina real al decir «Número N» (pegatinas/_creditos.json) + MAPA REAL con ruta en 13 de 25 (coordenadas
  de `_coords.md`: Wowhead Forever y la investigación; los puntos MEDIA van marcados en su subrótulo) + fichas de interfaz (APOYOS).
- MG NUEVOS de este guion (nucleo/mg_wow60.py): cuenta_atras (14 días / 2 semanas para las bandas), aforo (bandas fijas 10/20/40 contra
  una hermandad de 14; y los 39 amigos del cierre), consolas (4 colores × 15 cristales = 60), rangos (lacres por rango; tope semanal
  3 → 14 y reinicio a rango 1), tope_hora (10 → 5 entradas por hora), entregas (la cadena del 0.5 se come el conjunto de mazmorra).
- Comentarios en pantalla (≤ 10 días, ninguno repetido): gracias1 i.a.2.0.2.5, Torrikus, AndresBece04 · gracias2 Teniente Dandadan,
  Zargues · burlas Alejandro (burla0), Jclothus (burla1), Rafael (burla2) · correcciones Gespexp, Aztero, Sastakai.
- Overgear (escena overgear): fondo de marca DEBAJO de reseñas, packshot y código; captura de la página de coaching; nunca gameplay detrás.
  python fab.py wow_errores_60 fx --seco | FAB_FX_FINAL=1 python fab.py wow_errores_60 fx hoja | fx
"""
import os

import mg_oro as O
import mg_ruta as R
import mg_tes as T
import mg_wow as M
import mg_wow60 as W
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", -0.4)   # el código del creativo sale ~3 s después de entrar: así coincide con la voz
FIN_OG = ("Número veintitrés", -.1)
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
AZUL = (70, 140, 255)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    if slug.startswith("o_"):
        tam = min(tam, 340)
        if "marco" not in anim:   # el marco «vitral» parte el ícono en vidrieras y no se reconoce (hoja fx 22-nov): otro marco
            anim["marco"] = ("polaroid", "carta", "estampilla", "naipe", "museo", "clasico")[sum(map(ord, slug)) % 6]
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    if slug.startswith("o_"):   # íconos de 56 px: más chicos, que no se vean borrosos (regla 10-nov)
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    if slug.startswith("o_"):   # ícono entero, sin el zoom de cara (recortado se veía como una mancha borrosa, 15-nov)
        foco = (.5, .5, 1.0)
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420, foco=(.5, .5, 1.0)):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, foco=foco, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0):
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel([(F(s), n) for s, n in fotos], tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def P(x, y, rot, sub=None, foto=None):
    return (x, y, rot, sub, F(foto) if foto else None)


def tar(en, titulo, icono, lineas, calidad="amarillo", dur=5.0, x=.72, size=.50):
    """Ficha de interfaz (tooltip del juego) a la derecha."""
    return dict(en=en, dur=dur, x=x, size=size, tarjeta=dict(titulo=titulo, calidad=calidad, icono=icono, lineas=lineas))


BANDAS3 = [(F("cavernas_tumulo"), "Cavernas del Túmulo", "10 jugadores"), (F("cima_hyjal"), "Cima Hyjal", "20 jugadores"),
           (F("guarida_onyxia"), "Guarida de Onyxia", "40 jugadores")]

CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== OVERGEAR: fondo de marca PRIMERO (debajo de reseñas, packshot y código)
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="Si reservas dos horas", a=FIN_OG,
         entra=.3, nombre="og fondo marca"),
    # =========================================================== GANCHO: un elemento cada 2-3 s, MG desde el segundo 0
    mg(W.cuenta_atras("FALTAN PARA LAS BANDAS", 14, "DÍAS", "9 de diciembre", BANDAS3),
       .1, ("decide cómo te va a ir ese día|fin", .4),
       [("Faltan catorce días", .1), ("abran las tres bandas", .1), ("abran las tres bandas", .7), ("abran las tres bandas", 1.3)],
       "cuenta atrás 14 días", y=.50),
    mg(M.contadores("LA PRIMERA SEMANA DE FOREVER", [("inv_misc_bone_humanskull_01", "millones de muertes de jugadores", 196, 0, 1)],
                    ("LAS DEL 9 DE DICIEMBRE, LAS MÁS CARAS", 2)),
       ("En la primera semana de Forever hubo ciento", -.2), ("van a ser las más caras|fin", .5),
       ["hubo ciento noventa y seis millones", "de muertes de jugadores. Las", "Las del nueve de diciembre van"], "196 millones", y=.55),
    aba([("cavernas_tumulo", "Cavernas · 10"), ("cima_hyjal", "Cima Hyjal · 20"), ("guarida_onyxia", "Onyxia · 40")],
        ("Porque las tres bandas reinician", -.1), ("una semana entera de botín|fin", .4),
        [("Porque las tres bandas reinician", .2), ("Porque las tres bandas reinician", .7), ("Porque las tres bandas reinician", 1.2)],
        "tres bandas", x=.30, y=.62),
] + filav("Y hay trampas nuevas", [("o_berrido", "Beneficios que se apagan", "beneficios que se apagan en la puerta"),
                                   ("o_reloj", "Tope por hora", "mazmorras con tope por hora"),
                                   ("o_interrogacion", "Botín que nadie ha visto", "un botín que todavía no ha visto")], y=.64, tam=300, dur=3.0) + [
    ban(("Blizzard dice que Forever tiene más gente", .5), "monte_hyjal", "MÁS GENTE QUE EN 15 AÑOS", "cada grupo de banda, disputado", dur=5.4),
    mg(M.tiempos("LA SAGA DE LOS ERRORES", [("1 → 30", 8, VERDE), ("30 → 60", 8, AMAR), ("EL 60", 8, ROJO)], "la tercera parte"),
       ("Ya hicimos los errores de los primeros niveles", -.2), ("lo que pasa cuando por fin llegas al sesenta|fin", .3),
       ["los errores de los primeros niveles", "y los del treinta al sesenta", "Esta es la tercera parte", ("Esta es la tercera parte", .9)],
       "saga", y=.50),
    dict(tipo="mg", fn=PE.banda(F("guarida_onyxia"), "25 ERRORES AL LLEGAR AL 60", "del 25 al 1 · y cómo arreglarlos", foco=(.5, .5, 1.0),
                                alto=380, tema="wow"), en=("Hoy te traigo veinticinco errores", -.2), dur=5.0, x=.5, y=.78, sale=.3,
         nombre="banda 25", ver=1.0),
] + filav("Unos te cuestan oro", [("o_oro", "Oro", None), ("o_reloj", "Semanas", "otros semanas"),
                                  ("scholomance", "Repetir mazmorras", "repetir mazmorras que ya habías terminado")], y=.64, tam=300, dur=4.0) + [
    # =========================================================== 25 · los anillos
    rel("Número veinticinco. Cambiar un anillo", "o_anillo_canalizador", "Anillo de canalizador", "no hay vuelta atrás"),
    pv("Y a la Sortija de la Luz bendita", "o_sortija_luz", "Sortija de la Luz bendita", dur=4.6, x=.24, y=.56, tam=340),
    pv("ese cambio se hace con un vendedor, Pix", "pix_xizzix", "Pix Xizzix · el vendedor", dur=4.6, x=.76, y=.50, tam=540),
] + filav("pon los dos anillos uno junto al otro", [("o_sortija_luz", "Sortija de la Luz bendita", None),
                                                    ("o_anillo_canalizador", "Anillo de canalizador", "uno junto al otro")], y=.64, tam=320, dur=5.0) + [
    # =========================================================== 24 · tareas semanales de JcJ
    rel("Número veinticuatro. Ignorar las tareas", "o_marca_garganta", "Tareas semanales", "del Campo de honor"),
    mg(M.meta("LAS TAREAS DE LA TEMPORADA", [("ability_dualwield", "10 duelos"), ("inv_misc_rune_07", "3 batallas · Garganta"),
                                            ("achievement_bg_killxenemies_generalsroom", "25 jugadores · Garganta")], 0),
       ("Y la primera es casi un regalo", -.2), ("en la misma Garganta|fin", .5),
       ["ganar diez duelos", "completar tres batallas", "matar a veinticinco jugadores"], "tareas JcJ", y=.42),
    cam("Mucha gente al sesenta solo mira la banda", "guarida_onyxia", "solo la banda", dur=3.4, x=.16, y=.66),
    pv("y deja pasar semanas de tareas", "garganta_grito_guerra", "Garganta Grito de Guerra", dur=4.2, x=.74, y=.50, tam=560),
    pv("Diez duelos en la puerta de tu capital", "o_marca_garganta", "10 duelos · 1 tarde", dur=4.4, x=.24, y=.56, tam=340),
    # =========================================================== OVERGEAR (min 3) — logo, coaching, pros, captura, reseñas, packshot, código
    # capturas de overgear.com/games/wow-forever/coaching (recortes de medios/_overgear/coaching_pagina_26oct.png, 22-nov): ANTES del
    # logo para que el logo quede encima; la de precio («Save 5 %», «Cashback») cae en «con reembolso en cada pedido».
    dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, "og_coaching_hero.jpg"), (1.0, 1.06)), de="para las bandas del nueve de diciembre",
         a="Si reservas dos horas", entra=.4, sale=.3, nombre="og captura coaching", ver=2.0),
    dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, "og_coaching_precio.jpg"), (1.0, 1.08)), de=("con reembolso en cada pedido", -.3),
         a="El enlace está en la descripción, y hay", entra=.4, sale=.3, nombre="og captura precio", ver=2.0),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción, y hay", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Son sesiones individuales", dur=4.0,
         sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="Un coach mira tus talentos", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="Si reservas dos horas", dur=4.0, sale=.25,
         nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción, y hay",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=FIN_OG, entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== 23 · Onyxia sin conocer la pelea
    rel("Número veintitrés. Entrar a la Guarida", "onyxia", "Onyxia", "un solo jefe · tres fases"),
    mapa("marjal", [P(65.0, 47.1, "Theramore"), P(52.9, 77.7, "Guarida de Onyxia", "banda de 40 · un solo jefe", "guarida_onyxia")],
         ("La banda más grande del nueve", -.2), ("pasa un buen rato de la pelea volando|fin", .3),
         [("La banda más grande del nueve", .3), "se juega contra un solo jefe"], "MARJAL REVOLCAFANGO", "Guarida de Onyxia"),
    mg(M.tiempos("LAS TRES FASES DE ONYXIA", [("FASE 1 · TIERRA", 10, VERDE), ("FASE 2 · VUELA", 10, AMAR), ("FASE 3 · RUGIDO", 10, ROJO)],
                 "cada fase tiene su trampa"),
       ("Blizzard confirma que la pelea tiene", -.2), ("cada fase tiene su trampa|fin", .5),
       ["la pelea tiene tres fases", ("la pelea tiene tres fases", .6), ("la pelea tiene tres fases", 1.2), "cada fase tiene su trampa"],
       "fases Onyxia", y=.50),
    pv("porque el coletazo te manda a volar", "o_barrido_cola", "Barrido de cola", dur=4.0, x=.20, y=.58, tam=340),
    pv("de los huevos salen crías", "cria_onyxia", "Cría de Onyxia", dur=4.2, x=.76, y=.50, tam=520),
] + filav("El que recibe la bola de fuego", [("o_bola_fuego_onyxia", "Bola de Fuego", None),
                                             ("o_aliento_onyxia", "Respiración", "para no comerse su aliento")], y=.64, tam=320, dur=4.6) + [
    pv("Y en la tercera llega el rugido", "onyxia", "Fase 3 · el rugido del miedo", dur=5.0, x=.74, y=.50, tam=600),
    # =========================================================== 22 · lacres envalentonados
    rel("Número veintidós. Gastar el honor", "o_lacre_muneca", "Lacre envalentonado", "de muñeca · rango 8"),
    mg(W.rangos("LOS LACRES ENVALENTONADOS", [(8, F("o_lacre_muneca"), "muñeca y cinturón · rango 8"), (13, F("o_lacre_cabeza"), "cabeza · rango 13"),
                                             (11, "ability_mount_charger", "monturas de JcJ · rango 11")]),
       ("El épico se hace con la pieza azul", -.2), ("llegan con el rango once|fin", 1.0),
       ["piden rango ocho", "El de cabeza, rango trece", "llegan con el rango once"], "rangos lacres", y=.50),
    cam("venderla porque te cayó algo mejor", "o_oro", "vendida", dur=3.6, x=.16, y=.66),
    pv("Son la base de tu conjunto épico", "o_lacre_cabeza", "Lacre de cabeza · rango 13", dur=4.4, x=.76, y=.52, tam=340),
    # =========================================================== burla0 (Alejandro)
    com("Alejandro escribió: hay un poco", "alejandro_quevedo", dur=6.0, x=.32, y=.30),
    mg(M.tiempos("LAS PROPORCIONES", [("UN POCO DE VIDEO", 7, ROJO), ("MUCHA INTELIGENCIA", 14, VERDE)], "un poco de suerte, mucha preparación"),
       ("Y fíjate en las proporciones", -.2), ("y mucha preparación|fin", .6),
       ["un poco de video, mucha", "mucha inteligencia. Igual", "un poco de suerte"], "proporciones", y=.55),
    cam("no alcanzan ni para la banda de diez", "cavernas_tumulo", "banda de 10", dur=3.4, x=.80, y=.40, tam=320),   # 3,4 s: no esconderse tras la reliquia del 21
    # =========================================================== 21 · el rango no es para siempre
    rel("Número veintiuno. Creer que tu rango", "o_marca_alterac", "Rango de JcJ", "no es para siempre"),
    mg(W.rangos("CADA TEMPORADA NUEVA", reinicio="TODOS AL RANGO 1"), ("En Forever el rango no funciona", -.2),
       ("Además, el rango tiene un tope", -.3), [("vuelve al rango uno", 0)], "reinicio rango", y=.50),
    mg(W.rangos("EL RANGO TIENE TOPE POR SEMANA", techos=[("SEMANA 1 · TOPE RANGO 3", 3), ("SEMANA 10 · TOPE RANGO 14", 14)]),
       ("Además, el rango tiene un tope", -.1), ("Y el rango no baja si dejas de jugar", 0),   # cede el sitio al rótulo
       ["empieza en el rango tres", "no llega al catorce"], "tope rango", y=.50),
    pv("Y ojo con el Valle de Alterac", "valle_alterac", "Valle de Alterac · misiones al 58", dur=5.0, x=.74, y=.50, tam=560),
    pant("islas_lanza_negra", ("Y el campo de batalla nuevo, las Islas", -.1), ("frente al Marjal Revolcafango|fin", .6)),
    cam("de quince contra quince", "o_marca_lanza_negra", "15 contra 15", dur=3.6, x=.16, y=.66),
    cam("el equipo que compras se queda contigo", "o_lacre_muneca", "se queda contigo", dur=3.6, x=.84, y=.62),
    # =========================================================== 20 · consumibles la última semana
    rel("Número veinte. Comprar los consumibles", "o_pocion_fuego", "Consumibles", "cómpralos ya"),
    mg(M.tiempos("LA ECONOMÍA DE FOREVER", [("4 NOV · DE CERO", 8, VERDE), ("SIN REFERENCIA", 8, AMAR), ("TODO SUBE", 8, ROJO)]),
       ("La economía de Forever empezó de cero", -.2), ("los días antes de una banda nueva, todo sube|fin", .5),
       ["empezó de cero el cuatro", "No hay precios de referencia", "todo sube"], "economía", y=.50),
] + filav("Pociones de protección de fuego para Onyxia", [("o_pocion_fuego", "Protección de fuego", None),
                                                          ("o_pocion_mana", "Maná sublime", "pociones de maná y de curación"),
                                                          ("o_pocion_curacion", "Curación sublime", "y de curación sublimes"),
                                                          ("o_elixir_mangosta", "Elixir de la mangosta", "el Elixir de la mangosta"),
                                                          ("o_bolas_masa", "Comida con estadísticas", "y comida con estadísticas")],
          y=.66, tam=260, dur=4.4) + [
    # =========================================================== 19 · sin oro para reparar
    rel("Número diecinueve. Llegar al nueve", "o_reparar", "Reparar", "aparta el oro"),
] + filav("de las dos bandas nuevas", [("cima_hyjal", "Cima Hyjal", None), ("cavernas_tumulo", "Cavernas del Túmulo", "Se van a descubrir a ciegas")],
          y=.62, tam=340, dur=4.6) + [
    pv("hubo casi doscientos millones de muertes", "espiritu", "Ángel de la resurrección", dur=4.6, x=.74, y=.50, tam=540),
    cam("El que se gasta todo en la montura épica", "o_montura_epica", "montura épica", dur=3.8, x=.16, y=.66),
    cam("si el grupo no acuerda antes", "o_interrogacion", "¿y el botín?", dur=3.6, x=.84, y=.62),
    # =========================================================== gracias1
    com("Un espectador nuevo nos escribió", "ia2025", dur=6.0, x=.30, y=.30),
    com("Torrikus dice que siempre", "torrikus", dur=3.2, x=.68, y=.36),
    com("Y Andrés, después del video", "andresbece", dur=5.6, x=.32, y=.32),
    pv("todavía no has hecho cola para la Cumbre", "cumbre_superior", "Cumbre de Roca Negra superior", dur=4.6, x=.74, y=.52, tam=560),
    # =========================================================== 18 · la Cima Hyjal no es la de TBC
    rel("Número dieciocho. Ir a la Cima Hyjal", "cima_hyjal", "Cima Hyjal", "la de Forever es otra"),
    pv("era la banda de Archimonde", "archimonde", "Archimonde · The Burning Crusade", dur=4.6, x=.82, y=.56, tam=560),   # a la derecha: el rótulo OTRA BANDA le tapaba la cara
    mapa("hyjal", [P(68.6, 44.0, "Vuelo", "Fayran Elthas"), P(78.5, 36.9, "Cima de la Eternidad", "junto a Nordrassil"),
                   P(85.0, 33.0, "Cima Hyjal", "20 jugadores · 13 jefes · portal aprox.")],
         ("Es de veinte jugadores, con trece jefes", -.2), ("Y Archimonde no está en ella|fin", .4),
         [("Es de veinte jugadores, con trece jefes", .2), "en la cima del Monte Hyjal", "junto a Nordrassil"], "MONTE HYJAL", "la banda de 20"),
    pant("cima_hyjal_2", ("Empieza contra un guardián antiguo", -.1), ("que hay que limpiar los tres antes del final|fin", .4)),
    mg(M.expediente("LO QUE DICEN LOS ARCHIVOS", [("1", "Bandalar", None), ("2", "Sylvestris Dusksong", None), ("3", "The Wild King · ¿el último?", NAR)], None),
       ("En los datos del juego hay nombres", -.2), ("que probablemente es el último|fin", .5),
       ["nombres como Bandalar", "Sylvestris Dusksong", "o The Wild King"], "archivos Cima", y=.50),
    rel("existe un arma que se llama", "o_arma_inutil", "Arma inútil", "de la Cima Hyjal"),
    # =========================================================== 17 · las tres entradas de las Cavernas
    rel("Número diecisiete. No saber que las Cavernas", "cavernas_tumulo", "Cavernas del Túmulo", "banda de 10 · 3 entradas"),
    pant("cavernas_tumulo_2", ("La banda de diez está escondida", -.1), ("durante diez mil años|fin", .4)),
    mapa("cavernas_puertas", [P(36.1, 64.2, "Puerta del Monte Hyjal", "posición aprox.", "monte_hyjal"),
                              P(52.8, 22.0, "Cuna del Invierno", "la zona · puerta sin coordenada", "cuna_invierno"),
                              P(57.8, 71.5, "Puerta del Bastión Faucenegra", "norte de Azshara", "bastion_faucenegra")],
         ("Y tiene tres entradas", -.2), ("Cada una da a una parte distinta de la prisión|fin", .3),
         ["desde el Monte Hyjal", "desde Cuna del Invierno", "y desde el Bastión Faucenegra"], "LAS 3 ENTRADAS", "Cavernas del Túmulo", zmax=1.25),
] + filav("medio grupo esperando en Cuna", [("cuna_invierno", "Cuna del Invierno", None), ("monte_hyjal", "Monte Hyjal", "y la otra mitad en Hyjal")],
          y=.62, tam=340, dur=4.6) + [
    rel("Y hay una moneda de oro de Sonya", "o_moneda_sonya", "Moneda de oro", "de Sonya Sombrasanto", dur=6.0, x=.24),
    # =========================================================== 16 · el Bastión Faucenegra
    rel("Número dieciséis. Entrar al Bastión", "bastion_faucenegra", "Bastión Faucenegra", "mazmorra nueva · 55-60"),
    mapa("azshara", [P(21.8, 50.0, "Valormok", "vuelo"), P(38.4, 32.6, "Bastión Faucenegra", "piedra de encuentro", "bastion_faucenegra")],
         ("Es la mazmorra nueva del cincuenta y cinco", -.2), ("más grande que Profundidades de Roca Negra|fin", .4),
         [("Es la mazmorra nueva del cincuenta y cinco", .3), "una ciudad furbolg en el norte"], "AZSHARA", "el Bastión Faucenegra"),
    cam(("más grande que Profundidades de Roca Negra", -.6), "profundidades_roca_negra", "Profundidades de Roca Negra", dur=3.6, x=.84, y=.66),
    mg(M.contadores("EL BASTIÓN FAUCENEGRA", [("inv_misc_note_01", "misiones por bando", 7, 0, 1), ("inv_misc_book_11", "experiencia (más de)", 80000, 1, 2)],
                    ("NINGÚN DADOR ESTÁ DENTRO", 3)),
       ("Cada bando tiene siete misiones", -.2), ("Y ningún dador está dentro|fin", .6),
       ["Cada bando tiene siete misiones", "que juntas dan más de ochenta", "mil puntos de experiencia", "Y ningún dador está dentro"],
       "misiones Bastión", y=.55),
] + filav("La primera empieza con Nara", [("nara_wildmane", "Nara Wildmane · Cima del Trueno", "con Nara Wildmane"),
                                          ("mathrengyl", "Mathrengyl Bearwalker · Darnassus", "o con Mathrengyl Bearwalker")], y=.62, tam=360, dur=4.8) + [
    pant("bastion_faucenegra", ("Y un detalle: el Bastión está", -.1), "scene-083:fin"),   # hasta el fin del beat: el clip acaba en rojo (vida baja)
    cam("llevan a las Cavernas del Túmulo", "cavernas_tumulo_3", "Cavernas del Túmulo", dur=3.6, x=.84, y=.66),
    # =========================================================== burla1 (Jclothus)
    com("Jclothus escribió: deja de interrumpir", "jclothus", dur=7.6, x=.32, y=.30),
    # =========================================================== 15 · el Bancal del Creador
    rel("Número quince. Entrar al Bancal", "bancal_creador", "Bancal del Creador", "4 consolas · 60 cristales"),
    mapa("ungoro_norte", [P(43.6, 23.9, "Refugio de los Mariscales", None, "refugio_mariscales"),
                          P(47.3, 10.8, "Bancal del Creador", "mazmorra · 58-60", "bancal_creador")],
         ("Es la otra mazmorra nueva", -.2), ("subiendo desde el Refugio de los Mariscales|fin", .5),
         ["un lugar de los titanes", "subiendo desde el Refugio"], "CRÁTER DE UN'GORO", "al norte del cráter"),
    mg(W.consolas("BANCAL DEL CREADOR · 4 CONSOLAS", [((235, 60, 50), "Rojo", "Cinder", "fuego", F("o_cristal_rojo")),
                                                     ((255, 210, 40), "Amarillo", "Bolt", "rayo", F("o_cristal_amarillo")),
                                                     ((70, 140, 255), "Azul", "Snowtalon", "escarcha", F("o_cristal_azul")),
                                                     ((60, 200, 90), "Verde", "Vitrix (probable)", "veneno", F("o_cristal_verde"))], 15,
                  ("inv_misc_gem_crystal_01", "NANAYA", "jefa final · cambia de elemento cada 25 %"), "SIN CRISTALES: 5 JEFES"),
       ("Dentro hay cuatro consolas titánicas", -.2), ("te quedas en cinco jefes|fin", .6),
       ["Rojo para Cinder", "Amarillo para Bolt", "Azul para Snowtalon", "Y el verde, probablemente", "despierta la jefa final, Nanaya",
        "Sin los cristales"], "consolas", y=.52),
] + filav("juntad quince de cada color", [("o_cristal_rojo", "Rojo ×15", None), ("o_cristal_amarillo", "Amarillo ×15", None),
                                          ("o_cristal_azul", "Azul ×15", None), ("o_cristal_verde", "Verde ×15", None)], y=.66, tam=260, dur=5.0) + [
    # =========================================================== 14 · la montura épica
    rel("Número catorce. Llegar al sesenta sin plan", "o_montura_epica", "Palomino veloz", "montura épica"),
    mg(O.factura("LA MONTURA ÉPICA EN FOREVER", [("spell_nature_swiftness", "Equitación del 60", 1000), ("ability_mount_ridinghorse", "Montura épica", 200)],
                 "TOTAL", "−10 % CON HONORABLE"),
       ("La equitación del sesenta en Forever cuesta", -.2), ("en las dos cosas|fin", .6),
       ["cuesta mil de oro", "y la montura, doscientas más", "Haz la cuenta con mil doscientas", "te ahorras un diez por ciento"],
       "factura montura", y=.52),
    mg(M.contadores("UN JUGADOR LLEGÓ AL 60", [("inv_misc_coin_01", "oro en la bolsa", 1391, 0, 1)], ("SIN FARMEAR EN SERIO", 2)),
       ("Para que te hagas una idea", -.2), ("Llegar rico es llegar justo|fin", .4),
       ["llegó al sesenta con mil", "trescientas noventa y una", "sin farmear en serio"], "1391 de oro", y=.55),
    cam("empieza a juntar desde el cincuenta y cinco", "o_oro", "desde el 55", dur=3.6, x=.16, y=.66),
    # =========================================================== 13 · listas de botín de internet
    rel("Número trece. Planear la banda", "o_interrogacion", "Botín oculto", "nadie lo ha visto"),
    mg(M.censurado("EL BOTÍN DE BANDA DE FOREVER", [("inv_misc_spyglass_02", "No está en las bases de datos"),
                                                   ("inv_misc_book_11", "Estadísticas: solo al despojarlo"),
                                                   ("inv_misc_bag_10", "Más de 12 500 objetos ocultos")], "ESA LISTA, INVENTADA"),
       ("En Forever, el botín de las bandas", -.2), ("esa lista se la inventó|fin", .6),
       ["no está en las bases de datos", "solo muestran sus estadísticas", "más de doce mil quinientos", "esa lista se la inventó"],
       "botín oculto", y=.52),
    aba([("cavernas_tumulo_3", "Cavernas"), ("cima_hyjal", "Cima Hyjal"), ("guarida_onyxia", "Onyxia")],
        ("el primer conjunto se reparte entre las tres", -.1), ("mucho mejores que el resto|fin", .4),
        [("el primer conjunto se reparte entre las tres", .2), ("el primer conjunto se reparte entre las tres", .7),
         ("el primer conjunto se reparte entre las tres", 1.2)], "botín 3 bandas", x=.30, y=.62),
    cam("con nueve personas mirándote", "cavernas_tumulo", "banda de 10", dur=3.6, x=.84, y=.62),
    # =========================================================== 12 · farmear un fallo
    rel("Número doce. Farmear un fallo", "o_oro", "Un fallo del juego", "no es legal"),
    mapa("azshara", [P(38.4, 32.6, "Bastión Faucenegra", "14-16 nov · el fallo del botín de élite", "bastion_faucenegra")],
         ("El fin de semana del catorce", -.2), ("soltaba el botín completo de un élite|fin", .3), ["en el Bastión Faucenegra, un grupo"],
         "AZSHARA", "el fallo del Bastión"),
    mg(M.expediente("EL FALLO DEL BASTIÓN FAUCENEGRA", [("14", "un grupo normal con botín de élite", None), ("16", "Blizzard lo arregla", None),
                                                        ("17", "cientos lo farmearon a sabiendas", ROJO),
                                                        ("→", "sin economía, sin oro, suspendidos", ROJO)], ("SANCIONADOS", 4)),
       ("Blizzard lo arregló el dieciséis", -.3), ("suspendieron a los que más abusaron|fin", .8),
       [("Blizzard lo arregló el dieciséis", -.2), "Blizzard lo arregló el dieciséis|fin", "un par de cientos de jugadores",
        "A esas cuentas les bloquearon", "y suspendieron a los que más"], "expediente fallo", y=.52),
    # =========================================================== correcciones
    com("En el video del oro recomendé Auctionator", "gespexp", dur=7.0, x=.30, y=.30),
    com("Aztero nos recordó que el brujo", "aztero", dur=6.4, x=.66, y=.34),
    com("Sastakai nos corrigió que", "sastakai", dur=6.4, x=.30, y=.30),
    rel("en el video del treinta al sesenta dijimos", "o_lacre_ascension", "Lacre de Ascensión", "la misión sí lo da", dur=5.6),
    # =========================================================== 11 · la Cumbre superior con cinco
    rel("Vamos con el número once", "cumbre_superior", "Cumbre de Roca Negra superior", "mazmorra de 10"),
    mapa("estepas", [P(85.9, 67.6, "Vigilia de Morgan"), P(33.0, 25.2, "Cumbre de Roca Negra", "la única mazmorra de 10", "cumbre_superior")],
         ("La Cumbre superior es especial", -.2), ("la única mazmorra de diez jugadores del juego|fin", .5),
         [("La Cumbre superior es especial", .3), "la única mazmorra de diez"], "LAS ESTEPAS ARDIENTES", "la Cumbre de Roca Negra"),
    mg(M.tiempos("LA CUMBRE SUPERIOR EN FOREVER", [("SEMANAS 1-2 · ROTA", 10, VERDE), ("17 NOV · ARREGLADA", 10, ROJO)],
                 "ahora: grupo completo y atento"),
       ("Y en las dos primeras semanas de Forever estaba", -.2), ("de jugadores atentos para terminarla|fin", .5),
       ["Y en las dos primeras semanas de Forever estaba", "Blizzard lo arregló, y avisó", "un grupo completo de jugadores"],
       "cumbre rota", y=.50),
    cam("y alguien con el Lacre de Ascensión", "o_lacre_ascension", "Lacre de Ascensión", dur=3.8, x=.84, y=.62),
    # =========================================================== 10 · el amuleto en el banco
    rel("Número diez. Terminar la sintonización", "o_amuleto_pirodraco", "Amuleto de Pirodraco", "llévalo encima"),
    mapa("marjal", [P(52.9, 77.7, "Guarida de Onyxia", "sin el amuleto encima, no entras", "o_amuleto_pirodraco")],
         ("Pero para entrar a la Guarida", -.2), ("En el banco, no|fin", .5), ["cada jugador tiene que llevar"], "MARJAL REVOLCAFANGO",
         "la puerta de Onyxia"),
    pv("para pelear contra la dueña de la casa", "onyxia", "Onyxia · la dueña de la casa", dur=4.6, x=.74, y=.50, tam=560),
    # =========================================================== 9 · resistencia al fuego
    rel("Número nueve. Entrar a Onyxia", "o_pocion_fuego", "Protección de fuego", "poción superior"),
    ban(("Blizzard lo escribió en su anuncio", -.1), "guarida_onyxia", "PREPARA RESISTENCIA AL FUEGO", "el anuncio de las bandas", dur=5.0),
    mg(M.contadores("RESISTENCIA AL FUEGO EN FOREVER", [("inv_jewelry_talisman_11", "Amuleto de Pirodraco", 15, 0, 1),
                                                       ("inv_jewelry_ring_01", "Lacre de Ascensión", 10, 1, 2),
                                                       ("inv_chest_plate03", "Conjunto · 2 piezas (todas)", 8, 2, 3)],
                    ("ESE CONJUNTO QUE MUCHOS VENDEN", 4)),
       ("Y en Forever hay resistencia al fuego", -.2), ("Volvemos a él en el número uno|fin", .4),
       ["El Amuleto de Pirodraco da quince", "El Lacre de Ascensión, diez", "con solo dos piezas, da ocho", ("con solo dos piezas, da ocho", 1.2),
        "Sí, ese conjunto que mucha gente vende"], "resistencias", y=.55),
] + filav("Y la Capa de escamas de Onyxia", [("o_capa_onyxia", "Capa de escamas · +16", None),
                                             ("o_escama_onyxia", "Escama de Onyxia", "se hace con una escama de Onyxia")], y=.64, tam=320, dur=5.4) + [
    # =========================================================== gracias2
    com("El Teniente Dandadan nos cuenta", "teniente_dandadan", dur=6.4, x=.30, y=.30),
    com("Y Zargues, con tres semanas", "zargues", dur=7.0, x=.66, y=.34),
    # =========================================================== 8 · una banda que tu grupo no llena
    rel("Número ocho. Apuntar a una banda", "guarida_onyxia", "Guarida de Onyxia", "40 jugadores · ¿los tienes?"),
    mg(W.aforo("LAS BANDAS DE FOREVER SON FIJAS", [("Cavernas del Túmulo", 10, "8 jefes"), ("Cima Hyjal", 20, "13 jefes"),
                                                  ("Guarida de Onyxia", 40, "1 jefe")], 14, "Tu hermandad: 14 que siempre se conectan"),
       ("Las bandas de Forever son fijas", -.2), ("Y la Cima Hyjal, de veinte, también|fin", .8),
       ["Las Cavernas del Túmulo, de diez", "La Cima Hyjal, de veinte", "Y Onyxia, de cuarenta jugadores", "Si tu hermandad son catorce"],
       "aforo bandas", y=.50),
    pv("se parecen más a Karazhan", "cavernas_tumulo_3", "Cavernas del Túmulo · como Karazhan", dur=4.6, x=.74, y=.50, tam=560),
    mapa("kalimdor_bandas", [P(57.6, 30.7, "Cavernas del Túmulo", "grupo fijo de 10"), P(53.1, 24.1, "Cima Hyjal", "20 · aprox."),
                             P(52.7, 92.7, "Guarida de Onyxia", "40 · alianzas")],
         ("El arreglo: arma un grupo fijo de diez", -.2), ("busca alianzas con otras hermandades|fin", .5),
         ["arma un grupo fijo de diez", "suma gente para la Cima Hyjal", "y para Onyxia, busca alianzas"], "KALIMDOR", "las tres bandas", zmax=1.0),   # sin zoom: Onyxia (y 92 %) se salía por abajo
    # =========================================================== 7 · profesión por debajo de 300
] + filav("Dejar la herrería, la peletería", [("o_herreria", "Herrería", None), ("o_peleteria", "Peletería", "la peletería o la sastrería"),
                                             ("o_sastreria", "Sastrería", "o la sastrería por debajo")], y=.64, tam=300, dur=3.8) + [
    mg(M.meta("PUNTOS DE LEGADO DE TU PROFESIÓN", [("trade_blacksmithing", "150"), ("trade_leatherworking", "225"), ("trade_tailoring", "300")],
              0, "PUNTOS DE LEGADO"),
       ("Y cada profesión de fabricación da puntos", -.2), ("doscientos veinticinco y trescientos|fin", 1.0),
       [("da puntos de Legado a ciento cincuenta", .9), "doscientos veinticinco y trescientos", "doscientos veinticinco y trescientos|fin",
        ("doscientos veinticinco y trescientos|fin", .5)], "legado profesiones", y=.42),
    mg(M.forja("UNA PIEZA DEL CONJUNTO DE ARTESANO", [("inv_misc_tabard_guardiansofhyjal", "Reputación", None),
                                                     ("trade_blacksmithing", "Profesión al máximo", None),
                                                     ("ability_druid_cyclone", "Esencias de la banda", None),
                                                     ("trade_engraving", "Un encantador", None)], ("inv_shoulder_10", "Pieza de artesano"),
               "el objeto más de equipo"),
       ("La receta te pide reputación", -.2), ("Es el objeto más de equipo de todo Forever|fin", .5),
       ["La receta te pide reputación", "una profesión al máximo", "esencias que solo da la banda", "y un encantador. Es",
        "Es el objeto más de equipo", ("Es el objeto más de equipo", 1.0)], "forja artesano", y=.52),
    # =========================================================== 6 · los Guardianes de Hyjal
    rel("Número seis. Ignorar a los Guardianes", "o_tabardo_guardianes", "Guardianes de Hyjal", "facción nueva"),
    pv("Es una facción nueva de Forever, en el Monte", "monte_hyjal_2", "Monte Hyjal · los dos bandos", dur=4.6, x=.74, y=.50, tam=560),
    rel("necesitas la Vaina de semilla", "o_vaina_semilla", "Vaina de semilla", "reanimadora · 10 de oro", dur=3.0, x=.24),   # 3 s: no pisar el mapa de Rhylin
    mapa("hyjal", [P(70.6, 51.2, "Rhylin Espinapiedra", "intendente · 10 de oro, reverenciado")],
         ("Esa vaina la vende su intendente", -.2), ("Pero pide reputación reverenciada|fin", .4), ["la vende su intendente, Rhylin"],
         "MONTE HYJAL", "Guardianes de Hyjal"),
    mg(M.contadores("GUARDIANES DE HYJAL", [("inv_misc_tabard_guardiansofhyjal", "reverenciado", 21000, 0, 1),
                                           ("inv_misc_note_01", "5 misiones conocidas", 650, 1, 2)], ("EL RESTO, SIN DESCUBRIR", 3)),
       ("Y reverenciado son veintiún mil", -.2), ("todavía no se sabe|fin", .5),
       ["Y reverenciado son veintiún mil", "Hoy solo se conocen cinco", "que dan seiscientos cincuenta", "El camino al reverenciado"],
       "reputación Guardianes", y=.55),
    pv("una semilla caída de Nordrassil", "nordrassil", "Nordrassil", dur=4.4, x=.74, y=.50, tam=560),
    # =========================================================== burla2 (Rafael)
    com("Rafael escribió: deja de hacer", "rafael_veliz", dur=6.0, x=.32, y=.30),
] + filav("cuántos cristales pide el Bancal", [("o_cristal_rojo", "15 por consola", None), ("o_lacre_cabeza", "rango 13", "en qué rango sale cada lacre"),
                                               ("o_pocion_fuego", "1950-3250", "cuánto absorbe una poción de fuego")], y=.64, tam=300, dur=5.0) + [
    cam("lo que te dice la puerta de Onyxia", "guarida_onyxia", "sin el amuleto", dur=3.8, x=.84, y=.62),
    # =========================================================== 5 · el tope de cinco por hora
    rel("Número cinco. Farmear mazmorras", "o_reloj", "5 por hora", "el tope nuevo"),
    mapa("peste_forever", [P(56.7, 24.1, "Stratholme", None, "stratholme"), P(44.4, 79.7, "Scholomance", None, "scholomance")],
         ("Al sesenta, todo el mundo farmea", -.2), ("Roca Negra, el Bancal del Creador|fin", .3), ["todo el mundo farmea", "Scholomance, Roca Negra"],
         "TIERRAS DE LA PESTE", "lo que se farmea al 60"),
    mg(W.tope_hora("ENTRADAS A CADA MAZMORRA", ("ANTES: 10 POR HORA", 10), ("DESDE EL 20 DE NOVIEMBRE: 5", 5), "DEMASIADAS ESTANCIAS"),
       ("Y el veinte de noviembre, hace solo", -.2), ("ha entrado en demasiadas estancias|fin", .6),
       [("Y el veinte de noviembre, hace solo", .4), "cinco veces por hora", "con el aviso de que ha entrado"], "tope 5 por hora", y=.52),
] + filav("y alterna mazmorras", [("stratholme", "Stratholme", None), ("scholomance", "Scholomance", None)], y=.62, tam=320, dur=4.4) + [
    # =========================================================== 4 · el Lacre de Ascensión
    rel("Número cuatro. Que nadie de tu grupo", "o_lacre_ascension", "Lacre de Ascensión", "basta con uno"),
    carr([("drakkisath", "General Drakkisath"), ("rend", "Rend Puño Negro"), ("valthalak", "Lord Valthalak")],
         ("La Cumbre de Roca Negra superior es la llave", -.2), ("y también Rend y Lord Valthalak|fin", .5),
         ["Dentro está el general Drakkisath", "y también Rend", "y Lord Valthalak"], titulo="DENTRO DE LA CUMBRE SUPERIOR"),
    pant("cumbre_superior", ("Y la puerta solo se abre", -.1), ("Basta con uno para abrirla para todos|fin", .4)),
    mg(M.forja("EL LACRE DE ASCENSIÓN", [("racial_dwarf_findtreasure", "Lacre sin adornar", None), ("inv_misc_gem_opal_01", "Gema de Espina Ahumada", None),
                                       ("inv_misc_gem_diamond_02", "Gema de Cumbrerroca", None), ("inv_misc_gem_bloodstone_01", "Gema de Hacha de Sangre", None)],
               ("inv_jewelry_ring_01", "Lacre de Ascensión")),
       ("Para conseguirlo necesitas un lacre", -.2), ("De media, son unas cinco pasadas|fin", .4),
       ["necesitas un lacre sin adornar", "y las tres gemas de sus generales", ("y las tres gemas de sus generales", .7),
        ("y las tres gemas de sus generales", 1.4), "De media, son unas cinco pasadas"], "forja lacre", y=.52),
    mapa("marjal", [P(56.6, 87.6, "Brasaliza", "Ciénaga de Fuego · nivel 61", "brasaliza")],
         ("Y al final tienes que forjarlo", -.2), ("hasta que te hace de soplete|fin", .4), ["en el Marjal Revolcafango, dominando"],
         "MARJAL REVOLCAFANGO", "donde se forja el lacre"),
    # =========================================================== 3 · el botín de banda al vendedor
    rel("Número tres. Vender al vendedor", "o_esencia_maleable", "Esencia maleable", "de la Naturaleza"),
    mg(M.forja("EL CONJUNTO DE ARTESANO", [("ability_druid_cyclone", "Esencia maleable de la Naturaleza", None),
                                         ("spell_holy_removecurse", "Desencantar: Cima Hyjal o Cavernas", None)],
               ("inv_shoulder_10", "Las 4 piezas"), "Onyxia no cuenta"),   # el texto largo se salía del panel
       ("se fabrica con un material", -.2), ("Onyxia no cuenta|fin", .8),
       ["la Esencia maleable de la Naturaleza", "se consigue al desencantar objetos", "de las Cavernas del Túmulo. Onyxia", "Onyxia no cuenta"],
       "forja esencias", y=.52),
    cam("acaba en el vendedor por unas monedas", "o_oro", "unas monedas", dur=3.6, x=.16, y=.66),
    pv("Y si la banda va sin encantador", "o_encantamiento", "Encantamiento · parte del botín", dur=5.0, x=.74, y=.52, tam=340),
    cam("que todo lo que sobre se desencante", "o_desencantar", "Desencantar", dur=3.6, x=.16, y=.66),
    # =========================================================== 2 · los beneficios de mundo
    rel("Número dos. Farmear beneficios", "o_berrido", "Beneficios de mundo", "no van en la banda"),
    carr([("rend", "Rend · su cabeza"), ("o_serenata", "Serenata Cantaflor"), ("la_masacre", "La Masacre"), ("feria_luna_negra", "Feria de la Luna Negra")],
         ("El veterano llega al sesenta", -.2), ("y por la Feria de la Luna Negra|fin", .5),
         ["mata a Rend", "se come la Serenata Cantaflor", "pasa por La Masacre", "y por la Feria de la Luna Negra"], titulo="LO DE SIEMPRE"),
    pv("puedes matar a Onyxia, colgar su cabeza", "o_cabeza_onyxia", "Cabeza de Onyxia", dur=4.6, x=.24, y=.56, tam=340),
] + filav("el Poderío de Ventormenta", [("o_poderio_ventormenta", "Poderío de Ventormenta", None),
                                       ("o_bendicion_jefe", "Bendición del Jefe de Guerra", "y la Bendición del Jefe")], y=.64, tam=320, dur=5.0) + [
    cam("así que el beneficio de Rend te llega", "o_cabeza_rend", "Cabeza de Rend", dur=3.8, x=.16, y=.66),
    rel("Y el Reubicador cronológico", "o_reubicador", "Reubicador cronológico", "guarda lo que no sirve"),
    # =========================================================== 1 · vender el conjunto de mazmorra
    rel("Número uno. Vender las piezas", "o_yelmo_forjaluz", "Yelmo Forjaluz", "no lo vendas"),
    carr([("gandling", "Gandling · el casco"), ("osahendido", "Barón Osahendido · las piernas"), ("drakkisath", "Drakkisath · el peto")],
         ("El primer conjunto de mazmorra cae", -.2), ("y el peto el general Drakkisath|fin", .5),
         ["El casco lo suelta el Maestro", "las piernas el Barón Osahendido", "y el peto el general Drakkisath"], titulo="EL CONJUNTO DE MAZMORRA"),
    mg(W.entregas("LA CADENA DEL CONJUNTO 0.5", [("inv_bracer_14", "Brazales"), ("inv_belt_27", "Cinturón"), ("inv_gauntlets_29", "Guantes"),
                                                ("inv_boots_plate_06", "Botas"), ("inv_pants_04", "Piernas"), ("inv_shoulder_10", "Hombreras"),
                                                ("inv_helmet_08", "Casco"), ("inv_chest_plate03", "Peto")],
                  6, "¿Vendiste el casco? A matar a Gandling otra vez"),
       ("Porque la cadena del segundo conjunto", -.2), ("hasta que lo suelte otra vez|fin", .6),
       ["entregando brazales", "brazales, cinturón", "cinturón, guantes", "guantes, botas", "botas, piernas", "piernas y hombreras",
        "Y al final, el casco", ("Y al final, el casco", .8), "Si vendiste el casco"], "entregas 0.5", y=.52),
    mapa("mundo_bandas", [P(28.7, 85.6, "Tanaris", "Mux Malamaná", "mux"), P(77.7, 34.2, "Stratholme", "carrera de 45 minutos", "anthion"),
                          P(17.4, 72.5, "La Masacre", None, "la_masacre"), P(72.7, 78.6, "Roca Negra", "Bodley · y la Cumbre superior", "bodley"),
                          P(75.5, 81.8, "Las Estepas Ardientes", "Ejecutor Asharell · aprox.")],
         ("Y la cadena es una vuelta al mundo", -.2), ("Ardientes y la Cumbre superior|fin", .6),
         ["una vuelta al mundo: Tanaris", "Stratholme con una carrera", "La Masacre, Roca Negra", "Roca Negra, Las Estepas", "Ardientes y la Cumbre"],
         "LA VUELTA AL MUNDO", "la cadena del 0.5", zmax=1.2),
    rel("Y el brasero sagrado que necesitas", "o_brasero_sagrado", "Brasero sagrado", "Alba Argenta · honorable", dur=5.0),
    mapa("estepas", [P(74.0, 66.0, "Ejecutor Asharell", "élite 62 · posición aprox.")],   # sin Vigilia: su rótulo tapaba el punto
         ("En Forever hay un jefe nuevo en esa cadena", -.2), ("en el sur de Las Estepas Ardientes|fin", .5),
         [("En Forever hay un jefe nuevo en esa cadena", .3), "el Ejecutor Asharell"], "LAS ESTEPAS ARDIENTES", "jefe nuevo del 0.5"),
    pv("si matas a Lord Valthalak", "valthalak", "Lord Valthalak", dur=4.6, x=.74, y=.50, tam=560),
    # =========================================================== cierre
] + filav("del anillo que no tiene vuelta atrás", [("o_anillo_canalizador", "El anillo", None),
                                                   ("o_yelmo_forjaluz", "El conjunto", "al conjunto que no se vende")], y=.64, tam=320, dur=3.0) + [
    mg(W.cuenta_atras("FALTAN PARA LAS BANDAS", 2, "SEMANAS", "9 de diciembre", BANDAS3),
       ("Faltan dos semanas para el nueve", .9), ("o te quedas en la puerta|fin", .4),
       [("Faltan dos semanas para el nueve", 1.0), ("Faltan dos semanas para el nueve", 1.5), ("Faltan dos semanas para el nueve", 2.0),
        ("Faltan dos semanas para el nueve", 2.5)], "cuenta atrás 2 semanas", y=.50),
    mg(W.aforo("PARA LA BANDA DE CUARENTA", [("Guarida de Onyxia", 40, "40 jugadores")], 1, "Tú y 39 amigos más"),
       ("Si este video te sirvió, suscríbete y", -.2), ("treinta y nueve amigos más|fin", .8),
       [("Si este video te sirvió, suscríbete y", .3), "treinta y nueve amigos más"], "39 amigos", y=.42),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos); colores de la paleta (nada de «verde»)
    dict(texto="REINICIO SEMANAL", en="Porque las tres bandas reinician cada semana", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="NO SE PUEDE DESHACER", en="Y Blizzard avisa que no se puede deshacer", dur=3.0, tam=120, color="rojo", y=.2),
    dict(texto="−SANACIÓN", en="acaba de regalar su sanación", dur=3.0, tam=150, color="rojo", y=.2),
    dict(texto="TAMBIÉN EN TEMPORADAS FUTURAS", en="se pueden completar en temporadas futuras", dur=3.0, tam=100, color="amarillo", y=.2),
    dict(texto="9 DERROTADOS", en="Bueno, a nueve personas sí", dur=3.0, tam=140, color="rojo", y=.2),
    dict(texto="¡LEJOS DE LOS NIDOS!", en="que tenga miedo lejos de los nidos", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="NO LA VENDAS", en="el épico se construía encima de ella", dur=3.0, tam=150, color="rojo", y=.2),
    dict(texto="6 ME GUSTA", en="una crítica que se llevó seis me gusta", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="EL RANGO NO BAJA", en="Y el rango no baja si dejas de jugar", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="VER EL Nº 2", en="por un motivo que vas a ver en el número dos", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="ARMADURA EN ROJO", en="con la armadura en rojo", dur=3.0, tam=130, color="rojo", y=.2),
    dict(texto="OTRA BANDA", en="Pero la de Forever es otra", dur=3.0, tam=130, color="rojo", y=.2),
    dict(texto="CERO TÁCTICAS DE 2007", en="cero tácticas de dos mil siete", dur=3.0, tam=110, color="amarillo", y=.2),
    dict(texto="WELL OF SORROW", en="uno de los jefes es un pozo", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="DECIDID LA ENTRADA ANTES", en="decidid la entrada antes del día", dur=3.0, tam=110, color="amarillo", y=.2),
    dict(texto="LOS DOS CAMINOS", en="y recorre los dos caminos aunque tardes más", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="MANUELITO: HOY NO", en="Manuelito, lo siento, hoy no sales", dur=3.0, tam=130, color="rojo", y=.2),
    dict(texto="¡SIN BICHOS ALREDEDOR!", en="no metas cristales en la consola", dur=3.0, tam=120, color="rojo", y=.2),
    dict(texto="CIELONATOS: ARREGLADO", en="los cielonatos no recibían el descuento", dur=3.0, tam=110, color="amarillo", y=.2),
    dict(texto="CAJA SORPRESA", en="cada primer jefe va a ser una caja sorpresa", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="REPÓRTALO", en="disfrútalo una tarde y repórtalo", dur=3.0, tam=150, color="amarillo", y=.2),
    dict(texto="CORRECCIONES", en="Y ahora, las correcciones de la semana", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="GUÍAS DE ANTES DEL 17: VIEJAS", en="cualquier guía o video de antes del diecisiete", dur=3.0, tam=100, color="rojo", y=.2),
    dict(texto="BOLSA: SÍ · BANCO: NO", en="En la bolsa sirve. En el banco, no", dur=3.0, tam=120, color="amarillo", y=.86),
    dict(texto="PRIMERO HAY QUE MATARLA", en="Para protegerte de ella, primero hay que matarla", dur=3.0, tam=110, color="rojo", y=.2),
    dict(texto="MEJOR QUE SOBRE", en="nadie lo sabe todavía: mejor que sobre", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="SUSCRÍBETE", en="Si este video te está ahorrando oro", dur=3.0, tam=150, color="amarillo", y=.2),
    dict(texto="PEQUEÑO Y FIJO", en="un grupo pequeño que siempre está", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="240 NO ES 300", en="con la profesión en doscientos cuarenta", dur=3.0, tam=140, color="rojo", y=.2),
    dict(texto="TOP 5", en="Quédate al top cinco", dur=3.0, tam=170, color="amarillo", y=.2),
    dict(texto="SIN EXPERIENCIA PARA NADIE", en="le quita la experiencia a todo el grupo", dur=3.0, tam=100, color="rojo", y=.2),
    dict(texto="DE 10 A 5", en="Blizzard pasó de diez a cinco", dur=3.0, tam=170, color="rojo", y=.2),
    dict(texto="4 %", en="más o menos un cuatro por ciento", dur=3.0, tam=150, color="rojo", y=.12),
    dict(texto="NO FUNCIONAN EN BANDAS", en="los beneficios de mundo no funcionan en las bandas", dur=3.0, tam=110, color="rojo", y=.2),
    dict(texto="SE CANCELAN AL MORIR", en="se cancelan siempre al morir", dur=3.0, tam=120, color="rojo", y=.2),
    dict(texto="PARA LA BANDA: CONSUMIBLES", en="Para la banda, consumibles", dur=3.0, tam=100, color="amarillo", y=.2),
    dict(texto="EL ERROR QUE MÁS CUESTA", en="ahí está justo el error que más cuesta", dur=3.0, tam=110, color="rojo", y=.2),
    dict(texto="~227 DE ORO", en="En total, unas doscientas veintisiete", dur=3.0, tam=150, color="amarillo", y=.2),
    dict(texto="¿EN QUÉ NIVEL VAS?", en="Cuéntame en los comentarios en qué nivel vas", dur=3.0, tam=120, color="amarillo", y=.2),
]
SFX = {}
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número veinticinco. Cambiar", "Número veinte. Comprar", "Número quince. Entrar",
                                                                 "Número diez. Terminar", "Número cinco. Farmear")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Hoy te traigo veinticinco errores", "Número uno. Vender las piezas")]

APOYOS = [
    tar("Al Anillo de canalizador le quitó", "Anillo de canalizador", "inv_jewelry_ring_24",
        ["13 de noviembre", dict(t="− espíritu", c=RJ), dict(t="+ poder con hechizos", c=V)], calidad="azul"),
    tar("El Anillo da intelecto, golpe", "Anillo de canalizador", "inv_jewelry_ring_24",
        ["Intelecto", "Golpe", dict(t="Algo de poder con hechizos", c=V)], calidad="azul", dur=8.0, x=.28, size=.42),
    tar("La Sortija da aguante, espíritu", "Sortija de la Luz bendita", "inv_jewelry_ring_60",
        ["Aguante", "Espíritu", dict(t="Hasta 31 de sanación", c=V)], calidad="azul", dur=5.0, x=.72, size=.42),
    tar("Una rama de talentos escrita antes", "Rama de talentos de una guía", "inv_misc_book_09",
        ["Escrita antes del último ajuste", dict(t="Puede estar desfasada", c=RJ), dict(t="El coach mira la versión de hoy", c=V)], dur=5.6),
    tar("Cada temporada de JcJ trae una ruta", "Tareas semanales de JcJ", "inv_misc_rune_07",
        ["Honor", "Puntos de rango", dict(t="3 de ellas: 1 punto de Legado", c=V)]),
    tar("El arreglo: que los cuarenta vean la pelea", "El plan de Onyxia", "inv_misc_head_dragon_black",
        ["Fase 1: nadie detrás, nadie en los nidos", "Fase 2: apártate con la bola de fuego", dict(t="Fase 3: el miedo, lejos de los huevos", c=RJ)], dur=6.0),
    tar("El honor de Forever compra dos conjuntos", "Conjuntos de JcJ", "inv_helmet_41",
        [dict(t="Azul: con honor", c="azul"), dict(t="Épico: pieza azul + lacre", c="morado"), dict(t="El épico no se compra", c=RJ)]),
    tar(("da un cinco por ciento de experiencia", -.2), "Bolas de masa del desierto ahumadas", "inv_misc_food_64",
        ["Comida de Forever", dict(t="+5 % de experiencia por muertes", c=V), dict(t="Al 60: experiencia que no existe", c=GR)], dur=5.5),
    tar("El arreglo: aparta un dinero solo para reparar", "La primera semana de banda", "ability_repair",
        [dict(t="Oro aparte para reparar", c=V), dict(t="Reparto del botín, por escrito", c=V), "Antes del primer jefe"]),
    tar("Y luego se abren tres caminos", "Cima Hyjal (Forever)", "inv_misc_map02",
        ["20 jugadores · 13 jefes", "Un guardián antiguo", "3 caminos: ruinas y bajo tierra", dict(t="Los tres antes del final", c=RJ)], dur=6.0),
    tar("cuyo texto dice: esto no tiene sentido", "Moneda de oro de Sonya Sombrasanto", "inv_misc_coin_17",
        [dict(t="«Esto no tiene sentido,", c="amarillo"), dict(t="¿para qué voy a tirar", c="amarillo"), dict(t="una moneda a la fuente?»", c="amarillo")], dur=6.0),
    tar("Y otra misión pide un objeto de Withermaw", "Una misión, dos caminos", "inv_misc_note_01",
        ["Withermaw: un camino", "Bonesnout: el otro", dict(t="Uno solo = misión a medias", c=RJ)], dur=6.0),
    tar("las monturas raciales de vendedor se ligan", "Monturas raciales de vendedor", "ability_mount_ridinghorse",
        ["Desde el 10 de noviembre", dict(t="Se ligan al recogerlas", c=RJ), dict(t="Ya no se revenden", c=GR)]),
    tar("Eso sí, Blizzard aclaró que nadie", "El aviso de Blizzard", "inv_misc_note_01",
        [dict(t="Sin querer: no pasa nada", c=V), dict(t="A sabiendas: sanción", c=RJ)], dur=6.0),
    tar("Y es personal: no se comparte", "Amuleto de Pirodraco", "inv_jewelry_talisman_11",
        [dict(t="Personal: no es de cuenta", c=RJ), "Cada alt, su cadena", dict(t="Forever: +10 aguante · +15 res. fuego", c=V)], calidad="azul", dur=9.0),
    tar("Y está la Poción de protección de fuego", "Poción de protección de Fuego superior", "inv_potion_24",
        [dict(t="Absorbe 1950-3250 de fuego", c=V), "Dura 2 minutos"], calidad="verde", dur=6.0),
    tar("Las recetas del conjunto de artesano", "Conjunto de artesano", "inv_shoulder_10",
        ["Herrería, peletería o sastrería", dict(t="Habilidad 300", c=V), dict(t="Planos: jefes de mazmorra", c=GR)], dur=6.4),
    tar("Del conjunto de artesano, el que se fabrica, solo", "Conjunto de artesano", "inv_misc_tabard_guardiansofhyjal",
        [dict(t="Solo 1 pieza equipada", c=RJ), dict(t="2 piezas: Vaina de semilla", c=V)], dur=5.4),
    tar("Y otra regla: una mazmorra no da experiencia", "Experiencia en mazmorras", "inv_misc_book_11",
        ["Alguien 12+ niveles por encima", dict(t="= sin experiencia para el grupo", c=RJ)], dur=6.0),
    tar("Y en Forever, el lacre da además", "Lacre de Ascensión (Forever)", "inv_jewelry_ring_01",
        [dict(t="+10 res. al fuego", c=V), dict(t="+10 res. a la naturaleza", c=V), dict(t="+10 res. a la escarcha", c=V)], calidad="azul"),
    tar("El texto del de la cabeza de Onyxia", "Berrido de convocación del matadragones", "inv_misc_head_dragon_01",
        ["Beneficio de mundo", dict(t="No surte efecto en estancias de banda", c=RJ)], dur=6.0),
    tar("Lo bueno: Blizzard puso heraldos", "Heraldos del beneficio de Rend", "inv_misc_head_orc_01",
        ["Villadorada", "Villa del Lago", "Colina del Centinela", "Cerrotajo"], dur=6.4),
    tar("Y la novedad buena: en cada entrega", "Conjunto 0.5 en Forever", "inv_helmet_08",
        [dict(t="Una versión por especialización", c=V), "Druida: entre 4", "Paladín y chamán: entre 3"], calidad="morado", dur=6.0),
]


# ====================================================================== REVISIÓN DE HUECOS (fx --seco, 22-nov-2026): tramos de > 5 s sin
# pegatina ni MG → frases que nombran algo y no tenían nada. Van AL FINAL (regla 13-nov).
FX += [
    mg(M.tiempos("ASÍ VAN LOS COMENTARIOS HOY", [("ERRORES", 10, AZUL), ("PARADA", 6, AMAR), ("ERRORES", 10, AZUL), ("PARADA", 6, AMAR)],
                 "unos 3 minutos entre paradas"),
       ("Y para que veas que escuchamos", -.2), ("Esta es una de ellas|fin", .5),
       ["en paradas cortas", ("en paradas cortas", .5), ("en paradas cortas", 1.0), ("en paradas cortas", 1.5), "con unos tres minutos"],
       "paradas", y=.50),
    cam("si tienes alquimia o cocina", "o_elixir_mangosta", "alquimia", dur=3.6, x=.16, y=.66),
    cam("tres caminos, para un grupo nuevo", "cima_hyjal", "3 caminos = 3 noches", dur=3.8, x=.84, y=.62),
    cam("si algo da diez veces más oro", "bastion_faucenegra", "el fallo", dur=3.8, x=.16, y=.66),
    cam("arreglaron un pilar de piedra rebelde", "cumbre_superior", "un pilar rebelde", dur=4.0, x=.84, y=.62),
    cam("Lo de empezar pronto la sintonización", "guarida_onyxia", "sintonización", dur=3.8, x=.16, y=.66),
    pv("te dan el Amuleto de Pirodraco", "o_amuleto_pirodraco", "Amuleto de Pirodraco", dur=4.4, x=.24, y=.56, tam=340),
    cam("lleva el amuleto encima y varias", "o_amuleto_pirodraco", "encima", dur=3.8, x=.84, y=.62),
    cam("así no te pierdes lo que viene", "cima_hyjal", "9 de diciembre", dur=3.8, x=.84, y=.62),
    cam("busca un fabricante en tu hermandad", "o_herreria", "un fabricante", dur=3.6, x=.84, y=.62),
    cam("Farmear en Forever se volvió", "o_reloj", "puntualidad", dur=3.6, x=.16, y=.66),
    cam("El arreglo: los beneficios de mundo", "o_pocion_mana", "consumibles", dur=4.0, x=.84, y=.62),
    cam("Te cae un azul nuevo", "o_quijotes_forjaluz", "la pieza del conjunto", dur=3.8, x=.16, y=.66),
] + filav("guarda cada pieza del conjunto aunque", [("o_yelmo_forjaluz", "Guarda cada pieza", None),
                                                    ("o_oro", "Unas 230 de oro", "aparta unas doscientas treinta"),
                                                    ("o_brasero_sagrado", "Honorable · Alba Argenta", "y llega a honorable con el Alba")], y=.64, tam=300, dur=4.6)
ROTULOS += [
    dict(texto="NI UN POCO DE VIDEO", en="que no traen ni un poco de video", dur=3.0, tam=120, color="amarillo", y=.2),
    dict(texto="UN POCO CADA SEMANA", en="JcJ un poco cada semana", dur=3.0, tam=120, color="amarillo", y=.2),
    dict(texto="FABRÍCALO TÚ", en="fabrícalo tú", dur=3.0, tam=150, color="amarillo", y=.2),
    dict(texto="GRACIAS", en="gracias por los comentarios de esta semana", dur=3.0, tam=160, color="amarillo", y=.2),
    dict(texto="INTERRUPCIÓN", en="interrumpo el video para interactuar", dur=3.0, tam=150, color="rojo", y=.2),
    dict(texto="TE LEO A TI", en="te leo a ti, que lo pediste", dur=3.0, tam=150, color="amarillo", y=.2),
    dict(texto="NO TE CASES CON NINGUNA LISTA", en="no te cases con ninguna lista", dur=3.0, tam=100, color="amarillo", y=.2),
    dict(texto="PILAR REBELDE", en="Un pilar rebelde, en una fortaleza", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="AL BANCO NO", en="y lo metes en el banco", dur=3.0, tam=150, color="rojo", y=.2),
    dict(texto="300 ANTES DEL 9", en="sube tu profesión de fabricación a trescientos", dur=3.0, tam=140, color="amarillo", y=.2),
    dict(texto="AL MENOS DOS CON LACRE", en="que al menos dos de tu grupo fijo", dur=3.0, tam=120, color="amarillo", y=.2),
    dict(texto="3 A 8 ESENCIAS POR RECETA", en="entre tres y ocho", dur=3.0, tam=110, color="amarillo", y=.2),
    dict(texto="NADA DE BANDA AL VENDEDOR", en="Nada de banda al vendedor", dur=3.0, tam=110, color="rojo", y=.2),
]
FX += [
    cam("Y en Forever, el amuleto da diez", "o_amuleto_pirodraco", "+15 res. al fuego", dur=4.4, x=.16, y=.66),
    cam("lleva un encantador a cada banda", "o_encantamiento", "un encantador", dur=3.6, x=.84, y=.62),
]
ROTULOS += [
    dict(texto="6 < 10", en="Seis personas te dieron la razón", dur=3.0, tam=170, color="amarillo", y=.2),
    dict(texto="AL 60: NO SIRVE", en="Al sesenta, pagas por una experiencia", dur=3.0, tam=140, color="rojo", y=.2),
    dict(texto="ENTENDIDO", en="Pues mira, Jclothus, entendido", dur=3.0, tam=150, color="amarillo", y=.2),
]

# ====================================================================== CHEQUEO (22-nov-2026): densidad de mapas 0,5/min contra 0,7 del canal
# → 3 mapas más con coordenadas de `_coords.md` (WHF = mapa mundial de Wowhead Forever); sustituyen a las pegatinas de Tiala y Vaelan
# (la foto va en el punto). Van AL FINAL (regla 13-nov).
FX += [
    mapa("cuna_invierno", [P(61.2, 38.2, "Vista Eterna", "ata aquí la piedra de hogar"), P(58.2, 85.6, "Garganta Negro Rumor", "el paso a Hyjal")],
         ("decidid la entrada antes", 0), ("cerca de esa puerta|fin", .5), ["decidid la entrada antes", "atad la piedra de hogar"],
         "CUNA DEL INVIERNO", "¿por qué puerta entráis?"),
    mapa("hyjal", [P(68.8, 50.4, "Tiala Melenablanca", "El bastón de la montaña", "tiala")],
         ("haz ya la cadena de Tiala", -.3), ("que aparezca|fin", .4), ["haz ya la cadena de Tiala"], "MONTE HYJAL", "la cadena de Tiala"),
    mapa("estepas", [P(33.0, 25.2, "Cumbre de Roca Negra", "Vaelan · Cumbre inferior", "vaelan")],
         ("Y empiézalo con Vaelan", -.2), ("en la Cumbre inferior|fin", .6), ["empiézalo con Vaelan"], "LAS ESTEPAS ARDIENTES", "donde empieza el lacre"),
]
