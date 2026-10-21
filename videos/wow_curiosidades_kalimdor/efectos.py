# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA (wow_curiosidades_kalimdor): pegatinas, pantallas, motion graphics, rótulos y apoyos
anclados a las palabras de la voz. Receta: docs/estilo_secuencia_yt.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera la capa)    python fab.py <v> fx hoja
Nombres en pantalla = localización oficial es-MX de Wowhead (comprobados el 21-oct-2026): Anaia Correalba, Cerellean Zarpablanca,
Karna Tripirrem, Memo 01 (A-Me 01 en inglés), Smeed Mezclatornillos, Fizzle Pernolatón, disfraz de ogro Gordok, kombobulador kodo,
cristal resonador negro qiraji, Marra de Zul'Farrak, Quintaesencia de agua, Trueno Furioso (Thunderfury).
"""

import os
import mg_tes as T
import mg_wow as M

# PEGATINAS — REGLA FIJA DEL CANAL (18-oct-2026): imagen REAL de cada personaje/criatura/objeto que nombra la voz (Wowpedia en
# Fandom, fuentes en pegatinas/_fuentes.json), ADEMÁS de clips, apoyos y MG. Chicas abajo a la izquierda; ~1 de cada 5 GRANDE
# (x .25/.75, y .50, tam 600-720) del lado contrario a la tarjeta (x .72); en fila (x .13/.30/.47) cuando la voz enumera.
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=420):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def gran(en, slug, titulo, dur=4.5, x=.25, tam=660):
    return peg(en, slug, titulo, dur, x, .50, tam)


# PANTALLA COMPLETA (18-oct-2026): imagen REAL a cuadro entero solo donde el clip no enseña lo que la curiosidad necesita
# (fuentes en pantallas/_fuentes.txt); va DEBAJO de tarjetas y pegatinas.
_PAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantallas")


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


CAMARA = {
    "scene-101": dict(a=(1.0, 0, 0), b=(1.18, 0, -.12)),   # puerta titán cerrada con la cámara quieta: acercamiento lento
    "scene-061": dict(a=(1.0, 0, 0), b=(1.15, .2, .1)),    # Frondavil de ambiente, plano casi fijo: acercamiento lento
}
FUNDIDO = {}
FX = [
    # ---- pantallas completas (3): la Isla de los GM, el circuito de carreras y el Muro del Escarabajo cerrado
    pant("isla_gm", "Es la Isla de los Maestros de Juego", ("revisara tu cuenta|fin", .3), zoom=(1.0, 1.14), pan=(-.4, 0, .3, -.2)),
    pant("circuito", "Cada equipo tenía su coche cohete", ("público de los dos bandos y apuestas|fin", .3), zoom=(1.0, 1.12)),
    pant("muro_escarabajo", "Cuando se abrieron las puertas de Ahn'Qiraj", ("las mejores hermandades|fin", .3),
         zoom=(1.0, 1.16), pan=(0, 0, 0, -.3)),

    # ---- motion graphics NUEVOS de este guion (regla del 19-oct): runas, linaje, cadena y consola
    dict(tipo="mg", fn=M.runas("NÚCLEO DE MAGMA", 7, "spell_fire_fire", "inv_potion_76", "AZSHARA", "CADA SEMANA",
                               "APARECE EXECUTUS"),
         de=("En el Núcleo de Magma hay siete runas", -.2), a=("del otro lado del continente|fin", 1.2),
         marcas=["siete runas de fuego", "pedirle una quintaesencia", "volver cada semana", "Siete runas y una banda"],
         y=.74, sale=.4, nombre="MG runas", ver=1.0),
    dict(tipo="mg", fn=M.linaje((os.path.join(_PEG, "theradras.png"), "Theradras", "princesa elemental de tierra"),
                                (os.path.join(_PEG, "zaetar.png"), "Zaetar", "primer hijo de Cenarius"),
                                (os.path.join(_PEG, "centauro.png"), "Los centauros", "sus hijos"),
                                "EL ORIGEN DE LOS CENTAUROS", "DESOLACE"),
         de=("la princesa Theradras", -.4), a=("a lo que quedó|fin", 1.4),
         marcas=["la princesa Theradras", "Zaetar el primer hijo", "nacieron los centauros", "mataron a su padre",
                 "le pusieron Desolace"],
         y=.52, sale=.4, nombre="MG linaje", ver=1.0),
    dict(tipo="mg", fn=M.cadena("LA HERIDA DE FANDRAL", [
        (os.path.join(_PEG, "rajaxx.png"), "Valstann, partido en dos", "Guerra de las Arenas Movedizas", False),
        (os.path.join(_PEG, "fandral.png"), "Fandral no lo supera", "la Pesadilla usa su herida", False),
        (os.path.join(_PEG, "ragnaros.png"), "Del lado de Ragnaros", "Cataclysm", True),
    ], ("TODO EMPEZÓ CON UN GRITO", 3)),
         de=("Habla de Valstann", -.2), a=("un grito en Silithus|fin", 1.4),
         marcas=["Habla de Valstann", "Fandral nunca lo superó", "del lado de Ragnaros", "Todo empezó con un grito"],
         y=.66, sale=.4, nombre="MG cadena", ver=1.0),
    dict(tipo="mg", fn=M.consola("VIGÍA DE PIEDRA DE NORGANNON", [
        ("DISCOS DE NORGANNON", "PRESENTES", M.VERDE, 0),
        ("PLACAS DE ULDUM", "FALTAN", M.ROJO, 1),
        ("ACCESO A ULDUM", "DENEGADO", M.ROJO, 2),
    ], [("VISITA REPROGRAMADA", M.ORO_T, 3), ("VUELVA PRONTO", M.ORO_T, 4), ("EN ESPERA HASTA CATACLYSM", M.ROJO, 5)]),
         de=("aparece un vigía de piedra de Norgannon", -.2), a=("se congela hasta Cataclysm|fin", 2.0),
         marcas=["aparece un vigía de piedra", "te faltan las placas de Uldum", "así no se entra", "ha sido reprogramada",
                 "vuelvas pronto", "se congela hasta Cataclysm"],
         y=.66, sale=.4, nombre="MG consola", ver=1.0),

    # ---- pegatinas: intro
    peg("un goblin que revive kodos", "smeed", "Goblin de Desolace", dur=4.2, x=.13, tam=340),
    peg("un diablillo que te reta", "pusillin", "Diablillo", dur=4.0, x=.30, tam=340),
    peg("una puerta de los titanes en Tanaris", "uldum_puerta", "Una puerta en Tanaris", dur=5.0, x=.25, y=.50, tam=620),
    # 30 Pusillín
    gran("Se llama Pusillín", "pusillin", "Pusillín", dur=5.0),
    # 29 kodos
    peg("el cementerio de los kodos", "kodo", "Kodo anciano", dur=4.5),
    gran("hay un goblin que vio ahí", "smeed", "Smeed Mezclatornillos", dur=4.5, tam=600),
    peg("te pide tres para su caravana", "kombobulator", "Kombobulador kodo", dur=4.0, tam=300),
    # 28 Memo 01
    gran("una gorila robot", "ame01", "Memo 01", dur=4.5),
    peg("la inventora Karna Tripirrem", "karna", "Karna Tripirrem", dur=4.5),
    peg("Lo último que vio", "ame01", "A-Me 01", dur=4.0, x=.17, tam=360),
    # 27 Mankrik
    gran("la esposa de Mankrik", "mankrik", "Mankrik", dur=4.5),
    peg("peleando contra los jabaespines", "jabaespin", "Jabaespín", dur=3.8),
    peg("lo que encuentras es su cuerpo", "esposa", "La esposa de Mankrik", dur=4.5, tam=440),
    # 26 Ringo
    gran("hay un goblin desmayado", "ringo", "Ringo", dur=4.5),
    peg("le eches agua", "cantimplora", "Cantimplora", dur=3.5, tam=300),
    # 25 Thunderfury
    peg("Sus dos ataduras", "ataduras", "Ataduras del Buscavientos", dur=4.5, x=.13, tam=300),
    peg("caen de Garr", "garr", "Garr", dur=4.0, x=.30, tam=340),
    peg("del barón Geddon", "geddon", "Barón Geddon", dur=3.6, x=.47, tam=340),
    peg("el alto señor Demitrian", "demitrian", "Alto señor Demitrian", dur=2.0, tam=380),
    gran("aparece el príncipe Thunderaan", "thunderaan", "Príncipe Thunderaan", dur=4.0),
    peg("al que Ragnaros se comió", "ragnaros", "Ragnaros", dur=4.0, x=.75, y=.30, tam=380),
    # 24 Neeru
    peg("un demonio llamado Taragaman", "taragaman", "Taragaman el Hambriento", dur=4.0, tam=400),
    gran("está Neeru Hojafuego", "neeru", "Neeru Hojafuego", dur=5.0),
    peg("Thrall se entera gracias a ti", "thrall", "Thrall", dur=4.0),
    # 23 Naralex
    gran("Naralex quiso usar", "naralex", "Naralex", dur=4.5, tam=620),
    peg("los Druidas del Colmillo", "colmillo", "Druida del Colmillo", dur=4.0),
    # 22 Hydraxis (el MG runas va abajo: pegatinas arriba)
    gran("Para llegar a Ragnaros", "ragnaros", "Ragnaros", dur=3.0, tam=600),
    peg("al duque Hydraxis", "hydraxis", "Duque Hydraxis", dur=4.5, x=.15, y=.28, tam=360),
    peg("el mayordomo Executus", "executus", "Mayordomo Executus", dur=4.0, x=.85, y=.28, tam=340),
    # 20 Gahz'rilla
    gran("Es Gahz'rilla", "gahzrilla", "Gahz'rilla", dur=4.5),
    peg("los trols de arena", "zul_trol", "Trols de arena", dur=2.8, x=.75, y=.55, tam=360),
    # 19 Linken
    gran("un gnomo guerrero sin memoria", "linken", "Linken", dur=5.0),
    peg("te da su espada", "espada_linken", "Espada de maestría de Linken", dur=4.0, x=.11, tam=300),
    peg("o su bumerán", "bumeran", "Bumerán de Linken", dur=3.6, x=.32, tam=300),
    # 17 sable de escarcha
    gran("Es el sable de escarcha", "sable", "Sable de escarcha", dur=4.5, tam=640),
    # 16 Tiragarde
    peg("el almirante Daelin Valiente", "daelin", "Daelin Valiente", dur=4.5, x=.13, tam=340),
    peg("el padre de Jaina", "jaina", "Jaina Valiente", dur=4.0, x=.30, tam=340),
    gran("con el teniente Benedict al mando", "benedict", "Teniente Benedict", dur=4.5, tam=600),
    peg("en paz con Thrall", "thrall", "Thrall", dur=3.5),
    # 15 Gordok
    gran("Si llegas al rey Gordok", "gordok", "Rey Gordok", dur=4.5),
    peg("el disfraz de ogro Gordok", "traje_ogro", "Disfraz de ogro Gordok", dur=4.0, tam=300),
    # 14 Agamaggan
    gran("Agamaggan el Gran Jabalí", "agamaggan", "Agamaggan", dur=5.0),
    peg("para que Malfurion llegara", "malfurion", "Malfurion", dur=2.6, x=.75, y=.30, tam=360),
    peg("donde viven los jabaespines", "jabaespin", "Jabaespín", dur=3.8),
    # 13 flores cantoras
    peg("unas flores que valían", "flor_c", "Flor cantora corrupta", dur=4.5, x=.13, tam=360),
    peg("una flor limpia", "flor", "Flor cantora", dur=4.5, x=.32, tam=380),
    # 12 carreras
    peg("el goblin Pozzik", "pozzik", "Pozzik", dur=4.0, x=.11, tam=360),
    peg("el gnomo Fizzle", "fizzle", "Fizzle Pernolatón", dur=3.8, x=.34, tam=360),
    # 11 Zalazane
    gran("Zalazane el médico brujo", "zalazane", "Zalazane", dur=4.5, tam=620),
    peg("en el poblado Sen'jin", "voljin", "Vol'jin", dur=4.0),
    # 10 yeti (los tres amigos, con el lugar que dice la voz)
    gran("una goblin llamada Umi", "umi", "Umi", dur=4.5, tam=600),
    peg("Quiere fabricar un yeti mecánico", "yeti", "Yeti mecánico", dur=4.0),
    peg("en Vista Eterna en Gadgetzan", "legacki", "En Vista Eterna", dur=4.6, x=.13, tam=300),
    peg("en Gadgetzan y en Un'Goro", "sprinkle", "En Gadgetzan", dur=4.0, x=.30, tam=300),
    peg("y en Un'Goro repartidos", "quixxil", "En Un'Goro", dur=3.6, x=.47, tam=300),
    # 9 Grom
    gran("Ahí Grom Grito Infernal", "grom", "Grom Grito Infernal", dur=4.5),
    gran("a Mannoroth el demonio", "mannoroth", "Mannoroth", dur=4.0, x=.75),
    # 8 Teldrassil
    gran("lo plantaron Fandral Corzocelada", "fandral", "Fandral Corzocelada", dur=4.5, tam=600),
    peg("con furbolgs enloquecidos", "furbolg", "Furbolg de Teldrassil", dur=4.0),
    # 7 Ahn'Qiraj
    peg("la cadena del cetro", "cetro", "El cetro", dur=4.0, tam=300),
    gran("y la montura del cristal resonador", "qiraji", "Cristal resonador negro qiraji", dur=4.5, tam=620),
    # 6 Malfurion
    gran("Malfurion Tempestira está en coma", "malfurion", "Malfurion Tempestira", dur=5.0),
    peg("Tyrande lo encontró", "tyrande", "Tyrande", dur=4.0, tam=400),
    # 5 Onyxia
    gran("vive Onyxia", "onyxia", "Onyxia", dur=4.5),
    peg("las crías de dragón", "cria", "Cría de Onyxia", dur=4.0, x=.17, y=.30, tam=380),
    # 4 Quel'Serrar
    peg("un libro que casi nunca caía", "compendio", "El compendio", dur=4.0, tam=300),
    gran("para que Onyxia la quemara", "onyxia", "Onyxia", dur=4.0, tam=600),
    # 3 Anaia
    gran("Anaia Correalba murió", "anaya", "Anaia Correalba", dur=5.0),
    gran("el druida Cerellean Zarpablanca", "cerellean", "Cerellean Zarpablanca", dur=5.0, x=.25),
    # 2 Rajaxx (la cadena va abajo)
    gran("un jefe se burla del archidruida", "rajaxx", "General Rajaxx", dur=5.0),
    # 1 Uldum (la consola va abajo: pegatinas arriba)
    gran("hay una puerta de los titanes que estuvo", "uldum_puerta", "La puerta de Uldum", dur=5.0, tam=680),
    peg("con unos discos de los titanes", "discos", "Discos de Norgannon", dur=2.4, x=.17, y=.30, tam=380),
    peg("Al tocar un pedestal", "pedestal", "Pedestal de Uldum", dur=3.6, x=.15, y=.24, tam=340),
    peg("aparece un vigía de piedra", "vigia", "Vigía de piedra", dur=5.0, x=.85, y=.24, tam=320),
    # cierre
    peg("la esposa de Mankrik sin ayuda", "mankrik", "Mankrik", dur=3.6),
    peg("conseguir el agua", "quintaesencia", "Quintaesencia de agua", dur=3.6, tam=300),
]
ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="¿ALGUIEN DIJO THUNDERFURY?", en="alguien dijo Thunderfury", dur=3.0, tam=110, color="amarillo", y=.2),
    dict(texto="REY DE LOS OGROS", en="te proclaman su nuevo rey", dur=3.0, tam=130, color="amarillo", y=.2),
    dict(texto="50 DKP MINUS", en="fifty DKP minus", dur=1.8, tam=150, color="rojo", y=.2),
    dict(texto="MANY WHELPS, HANDLE IT", en="many whelps handle it", dur=3.0, tam=110, color="amarillo", y=.2),
]
SFX = {}
PISTAS = []

# APOYOS: tooltips REALES de Wowhead (classic, es-MX; ids comprobados el 21-oct en nether.wowhead.com) y tarjetas SOLO con datos
# del guion (o de su fuente verificada, en el docstring de guion.py).
V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
APOYOS = [
    # ---- intro
    dict(en="vuelve el cuatro de noviembre", dur=3.6, x=.72, size=.44, tarjeta=dict(titulo="World of Warcraft Forever",
         calidad="amarillo", icono="inv_misc_map_01", lineas=["Sale el 4 de noviembre", dict(t="Kalimdor, otra vez", c=GRIS)])),
    dict(en="Son treinta curiosidades", dur=5.0, tarjeta=dict(titulo="30 curiosidades", calidad="oro",
         icono="inv_misc_questionmark", lineas=["Kalimdor, tal como está en Classic", dict(t="Cuenta regresiva: 30 → 1", c=GRIS)])),
    # ---- 30 Pusillín
    dict(en="te suelta una rima", dur=5.0, x=.72, size=.44, wowhead="classic/npc/14354"),
    # ---- 29 kodos
    dict(en="kombobulador kodo", dur=5.0, x=.72, size=.44, wowhead="classic/13892"),
    dict(en="te pide tres para su caravana", dur=4.5, x=.72, size=.44, anim="fade", tarjeta=dict(titulo="El rodeo kodo",
         calidad="blanco", icono="ability_mount_kodo_01", lineas=["Kodos viejos y moribundos", dict(t="Tres domados para la caravana", c=V)])),
    # ---- 28 Memo 01
    dict(en="que se lee igual que Amy", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="A-Me 01 = «Amy»", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=["En español: Memo 01", dict(t="Amy, la gorila de Congo", c=GRIS)])),
    # ---- 27 Mankrik
    dict(en="te pide que la busques", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Perdida en la batalla", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Mankrik · El Cruce", dict(t="Encuentra a su esposa", c=GRIS)])),
    dict(en="preguntando lo mismo", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="1. General - Los Baldíos", calidad="blanco",
         icono="inv_letter_01", lineas=["¿a alguien le gusta metallica?", "metallica apesta", dict(t="¿¿dónde está la esposa de mankrik??", c=V)])),
    # ---- 26 Ringo
    dict(en="A Little Help From My Friends", dur=5.0, x=.72, size=.46, tarjeta=dict(titulo="A Little Help From My Friends",
         calidad="amarillo", icono="inv_misc_note_01", lineas=["Escolta a Ringo por Un'Goro", dict(t="Canción de los Beatles (la canta Ringo Starr)", c=GRIS)])),
    dict(en="le des una cachetada", dur=5.0, x=.72, size=.46, anim="fade", tarjeta=dict(titulo="Instrucciones de la misión",
         calidad="blanco", icono="inv_drink_waterskin_01", lineas=[dict(t="¿Débil?", der="cachetada"), dict(t="¿Desmayado?", der="agua", c=V)])),
    # ---- 25 Thunderfury
    dict(en="la espada legendaria más famosa", dur=5.0, x=.72, size=.46, wowhead="classic/19019"),
    # ---- 24 Neeru
    dict(en="está la Sima Ígnea", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Sima Ígnea", calidad="blanco",
         icono="spell_fire_fire", lineas=["Debajo de Orgrimmar", dict(t="Una facción del Consejo de la Sombra", c=ROJO)])),
    dict(en="el líder secreto del Filo Ardiente", dur=5.0, x=.72, size=.44, anim="fade", tarjeta=dict(titulo="Neeru Hojafuego",
         calidad="amarillo", icono="spell_shadow_shadowbolt", lineas=["Líder del Filo Ardiente", dict(t="Manda novatos a la Sima Ígnea", c=GRIS)])),
    # ---- 23 Naralex
    dict(en="la Pesadilla Esmeralda lo atrapó", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Cuevas de los Lamentos",
         calidad="blanco", icono="spell_nature_sleep", lineas=["El sueño de Naralex", dict(t="Atrapado por la Pesadilla Esmeralda", c=ROJO)])),
    # ---- 22 Hydraxis (el MG va abajo; el tooltip arriba a la derecha)
    dict(en="pedirle una quintaesencia", dur=4.5, x=.72, y=.30, size=.40, wowhead="classic/17333"),
    # ---- 21 Isla de los GM
    dict(en="más allá del mapa", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Isla de los GM", calidad="amarillo",
         icono="inv_misc_map_01", lineas=["Al noroeste de Teldrassil, fuera del mapa", dict(t="Solo para los maestros de juego", c=GRIS)])),
    # ---- 20 Gahz'rilla
    dict(en="con un mazo muy concreto", dur=4.5, x=.72, size=.44, wowhead="classic/9240"),
    dict(en="Ese mazo se hacía en las Tierras del Interior", dur=6.5, x=.72, size=.46, anim="fade", tarjeta=dict(
         titulo="Cómo se hacía el mazo", calidad="blanco", icono="inv_hammer_19", lineas=[
             dict(t="1. Mazo sagrado", der="altar de Zul"), dict(t="2. Consagrarlo", der="Jintha'Alor"),
             dict(t="3. Llamar a la hidra", der="Zul'Farrak", c=V)])),
    # ---- 19 Linken
    dict(en="igual que Link al principio", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Linken = Link", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=["Balsa rota y sin memoria: Link's Awakening", dict(t="It's a Secret to Everybody: el primer Zelda", c=GRIS)])),
    dict(en="va con espada y bumerán", dur=4.5, x=.72, size=.44, wowhead="classic/11905"),
    # ---- 17 sable de escarcha
    dict(en="Había que subir de neutral a exaltado", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Sable de escarcha de Cuna del Invierno",
         calidad="morado", icono="ability_mount_pinktiger", lineas=[dict(t="Solo Alianza", c=GRIS), dict(t="Neutral", der="Exaltado"),
             dict(t="Misiones repetibles", der="furbolgs y gigantes")])),
    # ---- 16 Tiragarde
    dict(en="Es el Fuerte de Tiragarde", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Fuerte de Tiragarde", calidad="blanco",
         icono="inv_misc_map_01", lineas=["Costa de Durotar", dict(t="Tropas de Daelin Valiente", c=ROJO)])),
    # ---- 15 Gordok
    dict(en="el disfraz de ogro Gordok", dur=5.0, x=.72, size=.44, wowhead="classic/18258"),
    dict(en="El premio es un cofre de tributo", dur=5.5, x=.72, size=.46, anim="fade", tarjeta=dict(titulo="Tributo de La Masacre",
         calidad="amarillo", icono="inv_box_02", lineas=["Rey Gordok muerto, los demás jefes vivos", dict(t="Cofre de tributo", c=V),
             dict(t="Cerveza y beneficios de dos horas", c=GRIS)])),
    # ---- 14 Agamaggan
    dict(en="De sus restos nació el Rajacieno", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Rajacieno", calidad="blanco",
         icono="inv_misc_herb_07", lineas=["Los restos de Agamaggan", dict(t="El laberinto de zarzas de los jabaespines", c=GRIS)])),
    # ---- 13 flores
    dict(en="sumando beneficios de mundo", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Serenata de la flor cantora",
         calidad="blanco", icono="spell_holy_mindvision", lineas=["Para todo el que pase", dict(t="Se pierde al morir", c=ROJO)])),
    # ---- 11 Zalazane
    dict(en="rodeado de trols hechizados", dur=4.5, x=.72, size=.44, wowhead="classic/npc/3205"),
    # ---- 10 yeti
    dict(en="asustar a tres amigos", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="La broma del yeti", calidad="amarillo",
         icono="inv_misc_head_dragon_01", lineas=["Vista Eterna", "Gadgetzan", dict(t="Cráter de Un'Goro", c=V)])),
    # ---- 9 Grom
    dict(en="rondando el monumento", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Monumento a Grom Grito Infernal",
         calidad="amarillo", icono="inv_axe_09", lineas=["Donde cayó Mannoroth", dict(t="Peregrinación orca", c=GRIS)])),
    # ---- 8 Teldrassil
    dict(en="sin la bendición de los Aspectos", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Teldrassil", calidad="blanco",
         icono="inv_misc_herb_07", lineas=[dict(t="Sin la bendición de los Aspectos", c=ROJO), dict(t="Nordrassil sí la tuvo", c=GRIS)])),
    # ---- 7 Ahn'Qiraj
    dict(en="cristal resonador negro qiraji", dur=5.0, x=.72, size=.44, wowhead="classic/21176"),
    dict(en="El primer servidor en lograrlo", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Puertas de Ahn'Qiraj", calidad="amarillo",
         icono="inv_misc_qirajicrystal_05", lineas=[dict(t="Primer servidor", der="Medivh"), dict(t="Fecha", der="enero de 2006"),
             dict(t="Guerra", der="10 horas", c=V)])),
    # ---- 6 Malfurion
    dict(en="El Círculo Cenarion decidió no moverlo", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Claro de la Luna", calidad="blanco",
         icono="spell_nature_sleep", lineas=["El cuerpo de Malfurion, en su túmulo", dict(t="Su espíritu, en el Sueño Esmeralda", c=GRIS)])),
    # ---- 5 Onyxia
    dict(en="La hermandad europea Wipe Club", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Wipe Club", calidad="amarillo",
         icono="inv_misc_head_dragon_black", lineas=["Hermandad europea", dict(t="Líder de banda: Dives", c=GRIS)])),
    # ---- 4 Quel'Serrar
    dict(en="Te dice que te escondas bajo un puente", dur=7.0, x=.72, size=.48, tarjeta=dict(titulo="Compendio para matar dragones",
         calidad="morado", icono="inv_misc_book_11", lineas=["«Escóndete bajo un saliente o un puente»",
             "«Curación completa, de cinco a quince clérigos»", dict(t="Una burla a EverQuest", c=GRIS)])),
    dict(en="y así nacía Quel'Serrar", dur=5.0, x=.72, size=.44, wowhead="classic/18348"),
    # ---- 3 Anaia
    dict(en="su espíritu se quedó atrapado allí", dur=4.5, x=.72, size=.44, wowhead="classic/npc/3667"),
    # ---- 2 Rajaxx
    dict(en="El general Rajaxx grita", dur=6.5, x=.72, size=.46, tarjeta=dict(titulo="General Rajaxx", calidad="morado",
         icono="spell_shadow_unholyfrenzy", lineas=["«Corzocelada suplicará por su vida,", "igual que su cachorro de hijo»",
             dict(t="Ruinas de Ahn'Qiraj", c=GRIS)])),
    # ---- cierre
    dict(en="dime en los comentarios", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="30 curiosidades de Kalimdor", calidad="oro",
         icono="inv_misc_questionmark", lineas=[dict(t="¿Cuál vas a buscar primero?", c=V)])),
]
