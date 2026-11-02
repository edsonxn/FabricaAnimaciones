# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 8 pistas que Blizzard YA dejó sobre lo que viene después de WoW Forever» (SECUENCIA YT).
- APOYOS: tooltips reales de Wowhead (classic, es-MX) y tarjetas estilo tooltip SOLO con datos del guion (nucleo/apoyos.py).
- Segmento Overgear (scene-028..032; campaña 2 del 26-oct: coaching de WoW Forever, vía bandas): recorrido por la web de
  coaching, insignias en pares con croma, logo, y la IMAGEN del tramo del creativo con CRONICAS10 (33,0-39,97 s) que acaba
  justo en el «Número cinco», SIN su audio: el código lo dice nuestra voz.
- 3 motion graphics por código (nucleo/mg_wow.py): la hoja de ruta 3/6/2, los 4 portales de las Cavernas (2 + «??») y los
  registros de Gilneas (3 zonas + 1 campo de batalla).
  python fab.py wow_pistas_futuro apoyos     genera apoyos/*.png y la hoja previews/fx_NN.jpg
  python fab.py wow_pistas_futuro fx         arma audio/fx.wav
"""
import mg_wow as M

OG = r"medios\_overgear" + "\\"                   # copias de D:\Cronicas de Warcraft\Overgear\ y del creativo de Descargas
OGF = OG + "forever\\"                             # kit WoW Forever (nov) del 28-oct: D:\Cronicas de Warcraft\Overgear\Forever\
CREATIVO = OG + "CRONICAS10_forever.mp4"          # creativo del código de Forever (Alice, 28-oct): rótulo en verde de 10 s
                                                   # «-10% WITH PROMO CODE CRONICAS10» (2,5-6 s) → «LINK IN THE DESCRIPTION»
CODIGO = ("Número cinco", -9.47)   # el creativo entra 2,5 s antes de «CRONICAS10» y acaba en el puesto siguiente

CAMARA = {}   # scene-029 = recorrido por overgear.com/games/wow-forever/coaching (26-oct, el brief pide screencast): ya se mueve solo
FUNDIDO = {}
FX = [
    # ---- patrocinio Overgear, campaña 2: coaching de WoW Forever, vía bandas, con el kit «WoW - Forever (nov)» (28-oct-2026):
    # logo de esquina todo el anuncio, par de USP, tarjeta de coaching, reseñas reales (croma ROJO) y packshot «PLAY BETTER FOREVER»
    # fondo oficial de marca (Alice, 29-oct; SIEMPRE en todo video con Overgear, el usuario 1-nov): cuadro entero
    # DEBAJO de reseñas, packshot y código (va antes en la lista para quedar debajo)
    dict(tipo="video", ruta=OG + "background\Background.mp4", bucle=True, de="Como en Forever el equipo no caduca", a=("Número cinco", 0),
         entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True, de="preparado está Overgear",
         a="El enlace está en la descripción", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="te explica por voz", dur=3.0, sale=.25,
         nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="mazmorras nuevas", dur=4.0,
         sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo",
         en="Como en Forever el equipo no caduca", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=("Número cinco", 0), entra=.15, nombre="og CODIGO", ver=3.0),
    # ---- motion graphics (3, regla de canal)
    dict(tipo="mg", fn=M.filas("HOJA DE RUTA DE FOREVER", [
        ("9 de diciembre", 3, ["achievement_boss_onyxia", "inv_misc_head_dragon_01", "inv_misc_head_dragon_01"]),
        ("Primavera 2027", 6, ["inv_misc_head_dragon_01", "inv_misc_head_dragon_01", "inv_misc_key_03", "inv_misc_key_03",
                               "inv_misc_map_01", "inv_staff_13"]),
        ("Verano 2027", 2, ["inv_misc_head_dragon_01", "inv_misc_questionmark"]),
    ]), de=("El nueve de diciembre abren", -.3), a=("banda icónica renovada|fin", 2.2),
        marcas=["El nueve de diciembre abren", "Para la primavera", "Y para el verano"],
        y=.76, sale=.4, nombre="MG hoja de ruta", ver=24.0),
    dict(tipo="mg", fn=M.grupos("LOS 4 PORTALES DE LAS CAVERNAS DEL TIEMPO", [
        (2, "spell_holy_borrowedtime", "Identificados en los foros", M.VERDE),
        (2, "spell_holy_borrowedtime", None, None),
    ], ancho=1100), de=("cuatro portales de instancia apagados", -.3), a=("precisamente los que importan|fin", .8),
        marcas=["En los foros identifican dos"], y=.76, sale=.4, nombre="MG cavernas", ver=9.0),
    dict(tipo="mg", fn=M.contadores("GILNEAS EN LOS ARCHIVOS DE LA BETA", [
        ("inv_misc_map_01", "Registros de zona nuevos", 3, 0, 1),
        ("achievement_battleground_battleforgilneas", "Campos de batalla", 1, 2, 3),
    ], remate=("CONSTRUIDO Y TODAVÍA APAGADO", 4)), de=("aparecieron tres registros de zona", -.2), a=("la muralla derrumbándose|fin", .8),
        marcas=["aparecieron tres registros de zona", "Gilneas a secas|fin", "También hay un campo de batalla", "Batalla por Gilneas|fin",
                "la muralla derrumbándose"],
        y=.76, sale=.4, nombre="MG gilneas", ver=20.0),
]

V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
PORT = "Portales tapiados"
APOYOS = [
    # ---- intro
    dict(en="Un diseñador de Blizzard toma", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="BlizzCon 2026", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["13 de septiembre", "Panel de World of Warcraft Forever"])),
    dict(en="World of Warcraft Forever ya salió", dur=5.2, tarjeta=dict(titulo="WoW Forever", calidad="amarillo",
         lineas=["Salió el 4 de noviembre", dict(t="Lo que viene después: sin anunciar", c=GRIS)])),
    dict(en="casi nada de esto está confirmado", dur=5.5, tarjeta=dict(titulo="Aviso", calidad="blanco",
         icono="inv_misc_questionmark", lineas=["Pistas de la beta y de la BlizzCon", dict(t="Casi nada está confirmado", c=ROJO)])),
    # ---- 8: calendario
    dict(en="Barrow Deeps, la Cima Hyjal", dur=5.5, y=.34, tarjeta=dict(titulo="Primeras bandas · 9 de diciembre",
         calidad="oro", icono="achievement_boss_onyxia", lineas=["Barrow Deeps", "Cima Hyjal", "Guarida de Onyxia"])),
    dict(en="la idea no está fuera de la mesa", dur=5.0, tarjeta=dict(titulo="¿Clase nueva?", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=[dict(t="«No está fuera de la mesa»", c=V), dict(t="Sin anuncio ni fecha", c=GRIS)])),
    dict(en="la zona nueva y el legendario", dur=5.5, tarjeta=dict(titulo="Guarda estos dos", calidad="oro", icono="inv_misc_map_01",
         lineas=[dict(t="Zona nueva", der="primavera 2027"), dict(t="Cadena legendaria", der="primavera 2027")])),
    # ---- 7: Azshara
    dict(en="El que habló fue Josh Greenfield", dur=5.0, x=.74, size=.40, tarjeta=dict(titulo="Josh Greenfield", calidad="blanco",
         lineas=["Diseñador sénior de World of Warcraft"])),
    dict(en="un hueco del tamaño de un cráter", dur=7.5, tarjeta=dict(titulo="Azshara", calidad="amarillo",
         icono="achievement_zone_azshara_01", lineas=[dict(t="«Quizá hay un hueco del tamaño de un cráter»", c=V),
                                                     dict(t="«…¿tal vez lo rellenemos?»", c=V)],
         pie="Josh Greenfield · BlizzCon, 13 de septiembre")),
    dict(en="Son veintidós años con un hoyo", dur=5.0, tarjeta=dict(titulo="El cráter de Azshara", calidad="blanco",
         icono="achievement_zone_azshara_01", lineas=["Vacío desde 2004", dict(t="22 años sin contenido", c=ROJO)])),
    # ---- 6: portales tapiados (la lista crece)
    dict(en="Hay una en Los Baldíos", dur=2.9, x=.72, size=.46, tarjeta=dict(titulo=PORT, calidad="amarillo",
         icono="spell_arcane_portalironforge", lineas=[dict(t="Los Baldíos · Bael Modan", der="1 / 6")])),
    dict(en="otra en Sierra Espolón", dur=3.2, x=.72, size=.46, anim="fade", tarjeta=dict(titulo=PORT, calidad="amarillo",
         icono="spell_arcane_portalironforge", lineas=["Los Baldíos · Bael Modan",
                                                       dict(t="Sierra Espolón · Risco Cortaviento", der="2 / 6")])),
    dict(en="Hay una más en las montañas", dur=6.7, x=.72, size=.46, anim="fade", tarjeta=dict(titulo=PORT, calidad="amarillo",
         icono="spell_arcane_portalironforge", lineas=["Los Baldíos · Bael Modan", "Sierra Espolón · Risco Cortaviento",
                                                       "Los Humedales · montañas del sur",
                                                       dict(t="Tierras Altas de Arathi", der="4 / 6")])),
    dict(en="La quinta está en Farhold Keep", dur=6.3, x=.72, size=.46, anim="fade", tarjeta=dict(titulo=PORT, calidad="amarillo",
         icono="spell_arcane_portalironforge", lineas=["Los Baldíos · Bael Modan", "Sierra Espolón · Risco Cortaviento",
                                                       "Los Humedales · montañas del sur", "Tierras Altas de Arathi",
                                                       dict(t="Riverglades · Farhold Keep", der="5 / 6")])),
    dict(en="Y la sexta es la vieja conocida", dur=6.5, x=.72, size=.46, anim="fade", tarjeta=dict(titulo=PORT, calidad="amarillo",
         icono="spell_arcane_portalironforge", lineas=["Los Baldíos · Bael Modan", "Sierra Espolón · Risco Cortaviento",
                                                       "Los Humedales · montañas del sur", "Tierras Altas de Arathi",
                                                       "Riverglades · Farhold Keep", dict(t="Ventormenta", der="6 / 6", c=V)])),
    dict(en="Un creador llamado Uncas", dur=4.6, x=.74, size=.40, tarjeta=dict(titulo="Uncas", calidad="blanco",
         lineas=["Creador de YouTube", dict(t="Visitó los portales uno por uno", c=GRIS)])),
    # ---- 5: mazmorras en los archivos
    dict(en="las Criptas de Karazhan, con once", dur=6.0, tarjeta=dict(titulo="Criptas de Karazhan", calidad="oro",
         icono="achievement_boss_princemalchezaar_02", lineas=["Entrada en los archivos de la beta", dict(t="11 jefes listados", c=V)],
         pie="Una sola publicación en un foro")),
    dict(en="se llama Manor Mistmantle", dur=6.5, tarjeta=dict(titulo="Manor Mistmantle", calidad="oro",
         icono="inv_misc_bone_humanskull_01", lineas=["Mazmorra de 5 jugadores", "Bosque del Ocaso", dict(t="Todavía sin jefes", c=GRIS)])),
    dict(en="la de la historia de Stalvan", dur=4.8, x=.72, size=.44, wowhead="classic/npc/315"),
    dict(en="esto sale de una sola publicación", dur=5.5, tarjeta=dict(titulo="Ojo", calidad="blanco", icono="inv_misc_note_01",
         lineas=["Fuente: una sola publicación en un foro", dict(t="Estar en los archivos no es llegar al juego", c=ROJO)])),
    # ---- 4: Cavernas del Tiempo
    dict(en="una cueva cerrada en Tanaris", dur=5.0, tarjeta=dict(titulo="Cavernas del Tiempo", calidad="amarillo",
         icono="spell_holy_borrowedtime", lineas=["Tanaris", dict(t="Cerradas en el juego original", c=GRIS)])),
    dict(en="la guerra entre los trols y los aqir", dur=7.0, tarjeta=dict(titulo="Lo que sueña Uncas", calidad="blanco",
         icono="inv_misc_questionmark", lineas=["La guerra de los trols y los aqir", "La caída de Ventormenta"],
         pie="Un deseo, no una pista")),
    # ---- 3: el legendario
    dict(en="cadena de misiones legendaria, primavera", dur=5.5, tarjeta=dict(titulo="? ? ?", calidad="naranja", icono="inv_misc_questionmark",
         lineas=["Cadena de misiones legendaria", "Primavera de 2027", dict(t="Estadísticas cifradas", c=GRIS)])),
    dict(en="éxito del ritual legendario", dur=3.5, tarjeta=dict(titulo="Éxito del ritual legendario", calidad="amarillo",
         icono="spell_nature_healingtouch", lineas=["Mejora", dict(t="Ritual con el Círculo Cenarion", c=V)], pie="Textos de la beta")),
    dict(en="un Stormwraith, ligada a Sylvestris", dur=6.0, tarjeta=dict(titulo="Sylvestris Dusksong", calidad="oro",
         icono="spell_nature_stormreach", lineas=["Jefe de la Cima Hyjal", dict(t="Ligado a un Stormwraith", c=V)], pie="Textos de la beta")),
    dict(en="Serían tres etapas", dur=8.5, x=.72, size=.46, tarjeta=dict(titulo="El legendario, según los textos", calidad="naranja",
         icono="inv_staff_13", lineas=["Rama de Nordrassil cargada", "Túmulos de Claro de la Luna", "Pilones del Cráter de Un'Goro"],
         pie="Tres etapas")),
    dict(en="se llama Archimonde's Fall", dur=5.5, tarjeta=dict(titulo="Archimonde's Fall", calidad="oro",
         icono="spell_shadow_summonvoidwalker", lineas=["«La caída de Archimonde»", dict(t="Mapa para un solo jugador", c=V)])),
    dict(en="un arma solo para sanadores", dur=5.0, tarjeta=dict(titulo="¿Arma de sanador?", calidad="blanco",
         icono="spell_nature_healingtouch", lineas=[dict(t="Especulación de la comunidad", c=ROJO)])),
    # ---- 2: Grim Batol
    dict(en="la puerta que lleva cerrada desde", dur=5.0, tarjeta=dict(titulo="Grim Batol", calidad="oro",
         icono="achievement_dungeon_grimbatol", lineas=["Los Humedales", dict(t="Cerrada desde 2004", c=ROJO)])),
    dict(en="una presencia de dragones rojos mucho", dur=6.0, tarjeta=dict(titulo="Grim Batol", calidad="amarillo",
         icono="ability_mount_drake_red", lineas=[dict(t="«Una presencia de dragones rojos mucho mayor fuera de la montaña»", c=V)],
         pie="Josh Greenfield · BlizzCon, 13 de septiembre")),
    dict(en="lleva el título de guardia real", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Dragones de la entrada", calidad="amarillo",
         icono="inv_misc_head_dragon_red", lineas=[dict(t="<Guardia real>", c=V)], pie="Según Uncas")),
    # ---- 1: Gilneas
    dict(en="la Muralla de Cringris era", dur=5.0, tarjeta=dict(titulo="Muralla de Cringris", calidad="amarillo",
         icono="inv_misc_key_03", lineas=["Sur del Bosque de Argénteos", dict(t="No se abría nunca", c=ROJO)])),
    dict(en="el creador Esfand publicó", dur=5.0, x=.74, size=.40, tarjeta=dict(titulo="Esfand", calidad="blanco",
         lineas=["Creador · 28 de septiembre", dict(t="Lo invocaron dentro de Gilneas", c=GRIS)])),
    dict(en="un tiburón lo mató", dur=5.0, tarjeta=dict(titulo="Tiburón de seguridad", calidad="oro", icono="inv_misc_fish_02",
         lineas=["Costa entre Los Humedales y Gilneas", dict(t="Mata a quien llega nadando", c=ROJO)], pie="Según Uncas")),
    dict(en="la maldición huargen quizá todavía", dur=5.5, tarjeta=dict(titulo="Maldición huargen", calidad="blanco",
         icono="inv_misc_monstertail_03", lineas=[dict(t="En esta línea temporal, ¿todavía se puede detener?", c=V)])),
    # ---- cierre
    dict(en="la zona nueva de primavera es Gilneas", dur=6.0, tarjeta=dict(titulo="Mi apuesta", calidad="oro", icono="inv_misc_map_01",
         lineas=[dict(t="Zona nueva de primavera", der="Gilneas"), dict(t="Legendario", der="Cima Hyjal")], pie="Apuesta, no dato")),
    dict(en="Dime en los comentarios cuál", dur=5.0, tarjeta=dict(titulo="¿Cuál es la banda icónica?", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=[dict(t="Déjalo en los comentarios", c=V)])),
    dict(en="el video de las clases y profesiones", dur=5.6, size=.50, img="C:/FabricaAnimaciones/videos/wow_pistas_futuro/medios/_overgear/mini_clases.jpg",
         titulo="Las 9 clases y profesiones OCULTAS de WoW Forever"),
]

ROTULOS = []
SFX = {}
PISTAS = []   # sin el audio del creativo: el código lo dice nuestra voz
