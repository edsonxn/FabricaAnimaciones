# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 9 clases y profesiones OCULTAS de WoW Forever» (motor SECUENCIA YT, Crónicas de Warcraft).
- APOYOS: tooltips reales de Wowhead (classic, es-MX) y tarjetas estilo tooltip SOLO con datos del guion (nucleo/apoyos.py).
- Segmento Overgear (scene-025..028): insignias y carrusel con croma, logo, y la IMAGEN del tramo del creativo con CRONICAS10
  (33,0-39,97 s) justo antes de scene-029, SIN su audio: el código lo dice nuestra voz (overgear_6; el usuario, 13-oct).
- 3 motion graphics «interfaz de WoW» por código (nucleo/mg_wow.py): fogatas 3/5/10, los 19 libros, 119 pergaminos y 12 reinicios.
  python fab.py wow_clases_ocultas apoyos     genera apoyos/*.png y la hoja previews/fx_NN.jpg
  python fab.py wow_clases_ocultas fx         arma audio/fx.wav
"""
import mg_wow as M

OG = r"medios\_overgear" + "\\"                   # copias de D:\Cronicas de Warcraft\Overgear\ y del creativo de Descargas
CREATIVO = OG + "overgear_promo_ES_remy_preview_720p.mp4"
CODIGO = ("scene-029", -6.97)                      # el tramo (6,97 s) termina justo donde empieza el puesto 6; entra con «CRONICAS10»

CAMARA = {
    "scene-026": dict(a=(1.0, 0, -.6), b=(1.12, 0, -.2)),   # captura de overgear.com/games/wow: baja despacio
}
FUNDIDO = {
    "scene-029": 0,                                # corte seco del creativo («LINK IN THE DESCRIPTION») al «Número seis»
}
FX = [
    # ---- patrocinio Overgear (vía: subida de nivel en self-play)
    dict(tipo="video", ruta=OG + "1 pair_green.mp4", croma=True, en="acompañado por jugadores profesionales", dur=4.0, sale=.25,
         nombre="og pros"),
    dict(tipo="video", ruta=OG + "2 pair_green.mp4", croma=True, en="aprendes la ruta", dur=3.2, sale=.25, nombre="og tos"),
    dict(tipo="video", ruta=OG + "cards-carousel_gree-screen.mp4", croma=True, en="Además ya se están preparando", dur=5.8,
         sale=.3, nombre="og carrusel", ver=2.5),
    dict(tipo="video", ruta=OG + "packshot-logo_greenscreen.mp4", croma=True, en="El enlace está en la descripción", a=CODIGO,
         entra=.2, nombre="og logo", ver=2.0),
    dict(tipo="video", ruta=CREATIVO, desde=33.0, de=CODIGO, a="scene-029", nombre="og CODIGO", ver=3.0),
    # el clip de scene-030 trae un tooltip enorme en inglés: se oscurece debajo de la tarjeta del campamento
    dict(tipo="oscurecer", en="Minería pone una piedra imán", dur=13.0, k=.45, entra=.35, sale=.3, nombre="oscurece campamento"),
    # ---- motion graphics (3, regla de canal)
    dict(tipo="mg", fn=M.filas("FOGATAS DEL CAMPAMENTO", [
        ("Básica", 3, ["spell_fire_fire", "inv_stone_sharpeningstone_01", "inv_misc_fish_02"]),
        ("De oficial", 5, ["spell_fire_fire", "inv_stone_sharpeningstone_01", "inv_misc_fish_02", "trade_engineering", "inv_misc_note_01"]),
        ("De experto", 10, ["spell_fire_fire", "inv_stone_sharpeningstone_01", "inv_misc_fish_02", "trade_engineering", "inv_misc_note_01"]),
    ]), de=("fogata básica aguanta", -.3), a=("experto diez|fin", 1.8), marcas=["tres muebles", "oficial cinco", "experto diez"],
        y=.76, sale=.4, nombre="MG fogatas", ver=5.0),
    dict(tipo="mg", fn=M.grupos("LOS 19 LIBROS DE COMPREHENSION", [
        (9, "inv_misc_book_09", "Un collar a elegir", M.ORO_T),
        (9, "inv_misc_book_11", "Estudio e Investigación", M.VERDE),
        (1, "inv_misc_book_09", None, None),
    ]), de=("Con los primeros nueve", -.3), a=("Estudio e Investigación|fin", .6), marcas=["primeros nueve libros", "nueve siguientes"],
        y=.76, sale=.4, nombre="MG libros", ver=8.5),
    dict(tipo="mg", fn=M.contadores("LA CAZA DEL SABLE", [
        ("inv_scroll_06", "Pergaminos descifrados", 119, 0, 1),
        ("inv_misc_bone_humanskull_01", "Reinicios del castillo", 12, 2, 3),
    ], remate=("¡CAYÓ LA HOJA DE FILARGENTA!", 4)), de=("Mientras tanto, Farmerfarms", -.2), a=("número doce, cayó|fin", 1.0),
        marcas=["Mientras tanto, Farmerfarms", "el ciento diecinueve|fin", "Volvieron al castillo", "número doce|fin", "número doce, cayó"],
        y=.76, sale=.4, nombre="MG sable", ver=19.5),
]

V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
ENC = "Encuesta: los 11 conceptos"
APOYOS = [
    # ---- intro
    dict(en="un arma que Blizzard nunca", tarjeta=dict(titulo="? ? ?", calidad="oro", icono="inv_misc_questionmark",
         lineas=["Arma cuerpo a cuerpo", "Requiere nivel 21", dict(t="Equipar: ? ? ?", c=V)], pie="Blizzard nunca la anunció")),
    dict(en="nueve clases y doce profesiones", dur=5.2, tarjeta=dict(titulo="WoW Forever", calidad="amarillo",
         lineas=["Sale el 4 de noviembre", "9 clases · 12 profesiones", dict(t="(oficialmente)", c=GRIS)])),
    # ---- 9: pícaro
    dict(en="Venenos y Ganzúa", dur=4.2, wowhead="classic/5060"),
    dict(en="los venenos ya se pueden usar", wowhead="classic/6947"),
    dict(en="la piedra de afilar y el veneno", dur=4.2, wowhead="classic/2862"),
    # ---- 8: primeros auxilios
    dict(en="las pociones de sanación ya no", wowhead="classic/929"),
    dict(en="con tela de lino", dur=4.0, wowhead="classic/1251"),
    dict(en="pociones de rejuvenecimiento", dur=4.0, wowhead="classic/2456"),
    dict(en="Te devuelven el setenta y cinco", dur=6.0, tarjeta=dict(titulo="Poción descolorida", calidad="blanco",
         icono="inv_potion_54", lineas=["Cura más que la poción normal", dict(t="Devuelve el 75 % de lo curado como daño con el tiempo", c=ROJO)],
         pie="Visto en una sola guía de la beta")),
    # ---- 7: Merchant's Favor
    dict(en="Merchant's Favor", tarjeta=dict(titulo="Merchant's Favor", calidad="amarillo", icono="inv_crate_04",
         lineas=["«El favor del mercader»", dict(t="Sin traducción oficial todavía", c=GRIS)])),
    # ---- 6: campamento
    dict(en="Minería pone una piedra imán", dur=13.0, size=.62, tarjeta=dict(titulo="Muebles del campamento",
         calidad="amarillo", icono="spell_fire_fire", ancha=True, lineas=[
             dict(t="Minería", der="piedra imán · poder de ataque"), dict(t="Sastrería", der="estandarte de facción"),
             dict(t="Peletería", der="tienda · descanso"), dict(t="Ingeniería", der="robot vendedor")])),
    dict(en="pecera que da ocho", dur=5.0, tarjeta=dict(titulo="Pecera", calidad="oro", icono="inv_misc_fish_02",
         lineas=["Mueble de Pesca", dict(t="+8 % a todas las estadísticas", c=V)], pie="Según una guía de la beta")),
    # ---- 5: la encuesta (la lista crece frase a frase)
    dict(en="una encuesta en el lanzador", dur=5.5, tarjeta=dict(titulo="Encuesta de Battle.net", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Septiembre de 2026 · sección Forever", dict(t="Solo a algunas cuentas", c=GRIS)])),
    dict(en="Estaba el manitas", dur=5.8, x=.70, size=.50, tarjeta=dict(titulo=ENC, calidad="amarillo", ancha=True,
         lineas=[dict(t="Manitas · Ilusionista", der="2 / 11")])),
    dict(en="Había un nigromante", dur=5.5, x=.70, size=.50, anim="fade", tarjeta=dict(titulo=ENC, calidad="amarillo", ancha=True,
         lineas=["Manitas · Ilusionista", dict(t="Nigromante · Bruja · Bardo", der="5 / 11")])),
    dict(en="También un vampiro sanléin", dur=6.6, x=.70, size=.50, anim="fade", tarjeta=dict(titulo=ENC, calidad="amarillo", ancha=True,
         lineas=["Manitas · Ilusionista", "Nigromante · Bruja · Bardo", dict(t="Vampiro san'layn · Celadora · Guerrero de runas", der="8 / 11")])),
    dict(en="Y de regreso el monje", dur=6.5, x=.70, size=.50, anim="fade", tarjeta=dict(titulo=ENC, calidad="amarillo", ancha=True,
         lineas=["Manitas · Ilusionista", "Nigromante · Bruja · Bardo", "Vampiro san'layn · Celadora · Guerrero de runas",
                 dict(t="Monje · Cazador de demonios · Caballero de la muerte", der="11 / 11", c=V)],
         pie="Ninguno anunciado para el lanzamiento")),
    # ---- 4: druida serpiente
    dict(en="las cinco piezas del conjunto", dur=9.0, tarjeta=dict(titulo="Conjunto de la víbora", calidad="oro",
         icono="ability_hunter_pet_windserpent", lineas=["Cuevas de los Lamentos · 5 piezas",
         dict(t="(5) Dream Venom: probabilidad de aturdir al objetivo 1 s", c=V), dict(t="Druida feral: forma de víbora", c=V)])),
    dict(en="Lo confirmó Aidan Moon", dur=4.6, x=.74, size=.40, tarjeta=dict(titulo="Aidan «Zirene» Moon", calidad="blanco",
         lineas=["Diseñador sénior de WoW Classic"])),
    # ---- 3: Comprehension
    dict(en="una habilidad nueva, Comprehension", dur=5.0, tarjeta=dict(titulo="Comprehension", calidad="amarillo",
         icono="inv_misc_spyglass_02", lineas=["Habilidad nueva · solo magos", "Descifra pergaminos misteriosos"])),
    dict(en="Uno imbuye una daga", dur=4.8, tarjeta=dict(titulo="Pergamino misterioso", calidad="oro", icono="inv_scroll_03",
         lineas=["Imbuye una daga", dict(t="Tus golpes pueden congelar al enemigo", c=V)])),
    dict(en="Otro encanta una espada", dur=5.8, tarjeta=dict(titulo="Pergamino misterioso", calidad="oro", icono="inv_scroll_05",
         lineas=["Encanta una espada durante 1 hora", dict(t="Si te pegan cuerpo a cuerpo, reinicia un hechizo de Fuego", c=V)])),
    # ---- 2: los 19 libros
    dict(en="Un creador llamado Farmerfarms", dur=4.6, x=.74, size=.40, tarjeta=dict(titulo="Farmerfarms", calidad="blanco",
         lineas=["Creador de YouTube", dict(t="Fuente de los puestos 1 y 2", c=GRIS)])),
    dict(en="Montañas de Alterac, Arathi", dur=6.0, x=.74, size=.40, tarjeta=dict(titulo="La ruta de los libros", calidad="amarillo",
         icono="inv_misc_map_01", lineas=["Montañas de Alterac", "Tierras Altas de Arathi", "Los Humedales", "Loch Modan",
                                          "Montaña Roca Negra"])),
    dict(en="más de una hora y más de treinta", dur=4.6, tarjeta=dict(titulo="Tierras Inhóspitas", calidad="blanco",
         icono="inv_misc_bone_humanskull_01", lineas=["Un solo libro", dict(t="Más de 1 hora", c=ROJO), dict(t="Más de 30 muertes", c=ROJO)])),
    dict(en=("Investigación tiene una hora", .5), dur=5.2, tarjeta=dict(titulo="Investigación", calidad="amarillo",
         icono="inv_feather_04", lineas=["Reutilización: 1 hora", "Gasta plumas ligeras", dict(t="2 objetos por uso (en sus pruebas)", c=V)])),
    # ---- 1: el mago de batalla
    dict(en="el Pergamino del Sable", dur=7.0, tarjeta=dict(titulo="Pergamino del Sable", calidad="oro", icono="inv_scroll_06",
         lineas=[dict(t="Úsalo sobre la hoja de Filargenta para crear un arma poderosa.", c=V)])),
    dict(en="el barón Filargenta es un jefe", dur=4.6, x=.74, size=.42, wowhead="classic/npc/3887"),
    dict(en="el Coldflame Saber", dur=9.0, tarjeta=dict(titulo="Coldflame Saber", calidad="oro", icono="inv_sword_11",
         lineas=["Sable · arma cuerpo a cuerpo", "Requiere nivel 21",
                 dict(t="Equipar: tus golpes cuerpo a cuerpo hacen 98 de daño de Fuego extra a objetivos congelados.", c=V)])),
    dict(en="trae Dedos de Escarcha", dur=5.0, tarjeta=dict(titulo="Dedos de Escarcha", calidad="amarillo",
         icono="ability_mage_wintersgrasp", lineas=["Árbol de Escarcha", dict(t="Trata al enemigo como si estuviera congelado", c=V)])),
    dict(en="Es un mago de batalla", dur=6.0, tarjeta=dict(titulo="Mago de batalla", calidad="oro", icono="inv_misc_questionmark",
         lineas=[dict(t="Pergamino: daga que congela", c=V), dict(t="Dedos de Escarcha", c=V), dict(t="Coldflame Saber: +98 de Fuego", c=V)],
         pie="Teoría de jugadores, no confirmada")),
    # ---- cierre
    dict(en="Dime cuál crees que falta", dur=5.0, tarjeta=dict(titulo="¿Qué secreto falta?", calidad="amarillo",
         lineas=["Guerrero · Chamán · Brujo", dict(t="Déjalo en los comentarios", c=V)])),
    dict(en="el video de los doce secretos", dur=5.6, size=.50, img="https://i.ytimg.com/vi/75HUR132Meg/maxresdefault.jpg",
         titulo="Los 12 objetos SECRETOS que tiene WoW Forever"),
]

ROTULOS = []
SFX = {}
PISTAS = []   # sin el audio del creativo: se notaba el cambio de voz (el usuario, 13-oct)
