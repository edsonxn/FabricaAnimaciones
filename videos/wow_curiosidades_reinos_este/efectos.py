# -*- coding: utf-8 -*-
"""Capa de EFECTOS (opcional) del motor SECUENCIA: cámara dirigida, golpes, rótulos de énfasis y SFX de ElevenLabs anclados
a las palabras de la voz. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
Vacío = el video se arma como siempre. Ejemplos reales: videos/guason_fumado/efectos.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

import os
import mg_tes as T
import mg_wow as M

# PEGATINAS (el usuario, 18-oct-2026: «cuando hables de objetos y personajes, ropa etc, busca imágenes de eso y ponlos como
# pegatinas sin quitar los elementos visuales que ya tienes»): imagen REAL de Wowpedia (Fandom) en pegatinas/, con la animación
# de mg_tes.pegatina (rebote, giro, flota, píldora con el nombre). Abajo a la izquierda; en fila (x .13/.30/.47) si la voz enumera.
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=460):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


# PANTALLA COMPLETA (el usuario, 18-oct-2026: «donde el video no encaja con lo que dice el guion, una imagen que represente
# mejor, a pantalla completa con alguna animación lenta, solo en curiosidades que de verdad lo requieran»): imagen REAL
# (Wowpedia, fuentes en pantallas/_fuentes.txt) con zoom/paneo lento; va DEBAJO de tarjetas y pegatinas (FX `pantalla`).
_PAN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pantallas")


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


CAMARA = {
    # "scene-003": dict(a=(1.05, 0, 0), b=(1.33, 0, .3)),      # (zoom, cx, cy) inicial y final
}
FUNDIDO = {
    # "scene-006": 0,                                          # corte seco al entrar a ese beat
}
FX = [
    # ---- pantallas completas: solo donde el clip no enseña lo que la curiosidad necesita ver
    pant("terraneos", "Los titanes crearon a los terráneos", ("descienden los enanos|fin", .3), pan=(0, -.4, 0, .3)),
    pant("defias", ("scene-044", -.4), ("fundó la Hermandad Defias|fin", .4), pan=(.4, 0, -.2, 0)),
    pant("katrana", "el rey Varian Wrynn está desaparecido", ("la respuesta correcta|fin", .3), zoom=(1.0, 1.14), pan=(-.5, 0, .3, -.2)),
    pant("naxxramas", "Hay una pirámide flotando", ("muy cerca de Stratholme|fin", .4), zoom=(1.0, 1.15), pan=(0, .3, 0, -.4)),
    pant("darrowshire", "Lo que Pamela no sabe", ("la Plaga lo corrompió|fin", .3), zoom=(1.0, 1.07), pan=(.7, 0, 1, 0)),
    pant("muralla", "se levanta la Muralla de Cringris", ("su gran puerta nunca se abre|fin", .3), zoom=(1.0, 1.16), pan=(0, -.5, 0, .5)),
    pant("thrall", "el teniente general Aedelas Blackmoore", ("significa esclavo|fin", .3), zoom=(1.0, 1.08)),
    pant("portal", "El Portal Oscuro estaba apagado", ("trajo a la Horda a Azeroth|fin", .4), zoom=(1.0, 1.18), pan=(0, 0, -.2, -.3)),
    pant("quelthalas", "Más allá de las Tierras de la Peste", ("se pueda entrar|fin", .3), zoom=(1.0, 1.45), pan=(0, 0, .1, -1)),
    # ---- motion graphics (3, regla de canal)
    dict(tipo="mg", fn=M.filas("PARA INVOCAR A GAHZ'RANKA", [
        ("Cinta de medir", 1, ["inv_misc_note_01"]), ("Cebo", 1, ["inv_misc_fish_02"]),
        ("Peces turbios", 5, ["inv_misc_fish_02"]),
    ]), de=("necesitas un cebo especial", -.3), a=("trescientos treinta de pesca|fin", 1.0),
        marcas=["le devuelves su cinta de medir", "necesitas un cebo especial|fin", "Luego hay que pescar cinco peces"],
        y=.76, sale=.4, nombre="MG gahzranka", ver=16.0),
    dict(tipo="mg", fn=M.filas("ROBOTS OOX POR RESCATAR", [
        ("Interior", 1, ["spell_magic_polymorphchicken"]), ("Feralas", 1, ["spell_magic_polymorphchicken"]),
        ("Tanaris", 1, ["spell_magic_polymorphchicken"]),
    ], ancho=900), de=("Pero hay tres robots así", -.2), a=("como mascota|fin", 1.0),
        marcas=["las Tierras del Interior", "Feralas", "Tanaris"],
        y=.76, sale=.4, nombre="MG oox", ver=12.0),
    dict(tipo="mg", fn=M.grupos("UN VOLCÁN, CINCO INSTANCIAS", [
        (3, "inv_misc_key_03", "Mazmorras", M.ORO_T), (2, "inv_misc_head_dragon_01", "Bandas", M.VERDE),
    ], ancho=1000), de=("Dentro de la Montaña Roca Negra están", -.2), a=("Ragnaros en el fondo|fin", 1.0),
        marcas=["las Profundidades de Roca Negra", "el Núcleo de Magma"], y=.76, sale=.4, nombre="MG volcan", ver=14.0),
    # ---- pegatinas (0:00-8:30)
    peg("un cartero muerto que sigue", "malown", "Cartero muerto", dur=6.5, x=.13, tam=350),
    peg("una gallina que te da una misión", "gallina", "Gallina", dur=4.0, x=.30, tam=320),
    peg("Y hay una espada que hace arrodillarse", "ashbringer_c", "La espada", dur=4.3, x=.47, tam=360),
    peg("tres carteros no-muertos", "cartero_nm", "Cartero no-muerto", dur=4.5),
    peg("aparece él, el jefe de correos Malown", "malown", "Malown", dur=4.5, x=.25, y=.50, tam=620),
    peg("un conjunto completo de cartero", "conjunto_cartero", "Conjunto del cartero", dur=4.5),
    peg("Se llama Gahz'ranka", "gahzranka", "Gahz'ranka", dur=5.0, x=.25, y=.50, tam=660),
    peg("que vende Nat Pagle", "nat_pagle", "Nat Pagle", dur=5.0),
    peg("Uno de sus frascos se llama", "roids", "R.O.I.D.S.", dur=5.5, tam=320),
    peg("Weldon, que sigue siendo humano", "weldon", "Weldon Barov", dur=4.5, x=.13, tam=360),
    peg("y Alexi, que es un renegado", "alexi", "Alexi Barov", dur=4.0, x=.31, tam=360),
    peg("porque hablamos de Hogger", "hogger", "Hogger", dur=5.5, x=.26, y=.50, tam=720),
    peg("con tu espada de principiante", "espada_novato", "Espada de novato", dur=4.0, tam=360),
    peg("unos fragmentos brillantes", "fragmentos", "Fragmentos iridiscentes", dur=3.5, x=.13, tam=320),
    peg("llena de kobolds", "kobold", "Kobold", dur=3.5, x=.30, tam=320),
    peg("La voz se llama Myzrael", "myzrael", "Myzrael", dur=5.0, x=.25, y=.50, tam=600),
    peg("que mates a un guardián de piedra", "fozruk", "Fozruk", dur=3.8, x=.13, y=.70, tam=340),
    peg("Es la frase más famosa de los kobolds", "kobold_minero", "Kobold minero", dur=5.0, x=.75, y=.52, tam=660),
    peg("Y en medio están Maybell Maclure", "maybell", "Maybell Maclure", dur=5.5, x=.13, tam=350),
    peg("y Tommy Joe Stonefield", "tommy", "Tommy Joe Stonefield", dur=4.5, x=.30, tam=350),
    peg("el caudillo Thoradin", "thoradin", "Thoradin", dur=5.0),
    peg("Leeroy Jenkins. El grupo entero", "leeroy", "Leeroy Jenkins", dur=4.5, x=.25, y=.48, tam=680),
    peg("por lo menos tiene pollo", "gallina", "Pollo", dur=3.2, x=.47, y=.78, tam=260),
    peg("los Discos de Norgannon", "discos", "Discos de Norgannon", dur=3.0),
    peg("a los terráneos, unos seres de piedra", "terraneo", "Terráneo", dur=4.5),
    peg("su líder, Edwin VanCleef", "vancleef", "Edwin VanCleef", dur=5.5, x=.25, y=.50, tam=640),
    peg("el hechicero Thaurissan", "thaurissan", "Thaurissan", dur=4.5),
    peg("Les salió Ragnaros", "ragnaros", "Ragnaros", dur=4.5, x=.27, y=.50, tam=740),
    peg("Anger'rel, Seeth'rel", "anger", "Anger'rel", dur=7.0, x=.13, tam=320),
    peg("Dope'rel, Gloom'rel", "dope", "Dope'rel", dur=5.5, x=.30, tam=320),
    peg("y Doom'rel", "doom", "Doom'rel", dur=4.0, x=.47, tam=320),
    peg("el mayordomo Executus", "executus", "Executus", dur=5.0),
    peg("solo lo ves de la cintura para arriba", "ragnaros", "Ragnaros", dur=4.5),
    peg("Por eso existe Lothos Riftwaker", "lothos", "Lothos Riftwaker", dur=5.0),
    # ---- pegatinas (8:30-30:56)
    peg("Abercrombie, un ermitaño", "abercrombie", "Abercrombie", dur=5.0),
    peg("la abominación, Stitches", "stitches", "Stitches", dur=5.0, x=.25, y=.50, tam=640),
    peg("su jefe final, Hakkar", "hakkar", "Hakkar", dur=5.0, x=.25, y=.50, tam=640),
    peg("Los Bucaneros Velasangre son", "bloodsail", "Bucanero Velasangre", dur=5.0),
    peg("está Lady Katrana Prestor", "katrana", "Katrana Prestor", dur=5.0, x=.13),
    peg("Katrana Prestor es Onyxia", "onyxia", "Onyxia", dur=5.0, x=.27, y=.50, tam=660),
    peg("En una de sus estaciones está Monty", "monty", "Monty", dur=5.0),
    peg("el barón Rivendare tiene presa", "rivendare", "Barón Rivendare", dur=4.5, x=.13, tam=360),
    peg("a Ysida Harmon", "ysida", "Ysida Harmon", dur=4.0, x=.31, tam=360),
    peg("el OOX-09/HL", "oox", "OOX-09/HL", dur=4.5, tam=300),
    peg("el gnomo te regala", "oglethorpe", "Oglethorpe", dur=4.0),
    peg("Kel'Thuzad y su Culto", "kelthuzad", "Kel'Thuzad", dur=5.5, x=.25, y=.50, tam=680),
    peg("vive Hemet Nesingwary", "nesingwary", "Hemet Nesingwary", dur=5.0),
    peg("el maestro de canes Loksey", "loksey", "Loksey", dur=5.0),
    peg("el comandante Mograine y", "mograine_sm", "Comandante Mograine", dur=4.5, x=.13, tam=360),
    peg("la alta inquisidora Melenablanca", "whitemane", "Melenablanca", dur=5.0, x=.31, tam=360),
    peg("llevárselos a Riggle Bassbait", "riggle", "Riggle Bassbait", dur=5.0, x=.33, tam=420),
    peg("mató a su padre, el rey Terenas", "arthas", "Arthas", dur=5.0, x=.25, y=.50, tam=640),
    peg("el rey Terenas, en Warcraft", "terenas", "Rey Terenas", dur=4.0, x=.75, y=.52, tam=520),
    peg("junto a Sylvanas, hay un demonio", "sylvanas", "Sylvanas", dur=4.5, x=.77, y=.52, tam=600),
    peg("Short John Mithril", "shortjohn", "Short John Mithril", dur=5.0),
    peg("el tabernero, Plugger Spazzring", "plugger", "Plugger Spazzring", dur=5.0),
    peg("la torre de Medivh", "medivh", "Medivh", dur=5.0, x=.77, y=.52, tam=600),
    peg("Tirion Fordring, el paladín", "tirion", "Tirion Fordring", dur=5.0, x=.25, y=.50, tam=620),
    peg("a su hijo, Taelan", "taelan", "Taelan Fordring", dur=4.5),
    peg("el gran inquisidor Isillien", "isillien", "Isillien", dur=4.5),
    peg("aparece Pamela Redpath", "pamela", "Pamela Redpath", dur=5.0),
    peg("el capitán Joseph Redpath", "joseph", "Joseph Redpath", dur=5.0),
    peg("los orcos Faucedraco", "faucedraco", "Orco Faucedraco", dur=4.5),
    peg("prisionera a Alexstrasza", "alexstrasza", "Alexstrasza", dur=5.0, x=.76, y=.50, tam=620),
    peg("Ysondre, Lethon", "ysondre", "Ysondre", dur=6.0, x=.12, tam=300),
    peg("Lethon, Emeriss", "lethon", "Lethon", dur=5.5, x=.28, tam=300),
    peg("Emeriss y Taerar", "emeriss", "Emeriss", dur=5.0, x=.44, tam=300),
    peg("y Taerar aparecían", "taerar", "Taerar", dur=4.5, x=.60, tam=300),
    peg("el rey Genn Cringris", "genn", "Genn Cringris", dur=4.5, x=.31, tam=360),
    peg("Están Turalyon", "turalyon", "Turalyon", dur=7.0, x=.10, tam=280),
    peg("Alleria Brisaveloz", "alleria", "Alleria", dur=6.0, x=.25, tam=280),
    peg("Khadgar, Danath", "khadgar", "Khadgar", dur=5.0, x=.40, tam=280),
    peg("Danath Aterratrols", "danath", "Danath", dur=4.5, x=.55, tam=280),
    peg("Kurdran Martillo Salvaje", "kurdran", "Kurdran", dur=4.0, x=.70, tam=280),
    peg("Moira Barbabronce, hija de Magni", "moira", "Moira", dur=5.0, x=.13, tam=360),
    peg("hija de Magni", "magni", "Magni", dur=4.0, x=.31, tam=360),
    peg("junto al emperador", "thaurissan_dagran", "Dagran Thaurissan", dur=5.0),
    peg("Aedelas Blackmoore crió", "blackmoore", "Blackmoore", dur=4.5, x=.13, tam=360),
    peg("le puso Thrall", "thrall", "Thrall", dur=4.5, x=.31, tam=360),
    peg("los gnomos no tienen zona", "gnomo", "Gnomos", dur=4.5),
    peg("invadida por los troggs", "trogg", "Trogg", dur=4.5),
    peg("está la mansión Ravenholdt", "ravenholdt", "Ravenholdt", dur=5.0),
    peg("el jefe final, Nefarian", "nefarian", "Nefarian", dur=5.0, x=.26, y=.50, tam=720),
    peg("el sumo sacerdote Thekal", "thekal", "Thekal", dur=4.5, x=.13, tam=360),
    peg("el señor de sangre Mandokir", "mandokir", "Mandokir", dur=4.5, x=.31, tam=360),
    peg("la feria montaba sus carpas", "feria", "Feria de la Luna Negra", dur=5.0),
    peg("un jefe de mundo, Lord Kazzak", "kazzak", "Lord Kazzak", dur=5.0, x=.25, y=.50, tam=640),
    peg("para adorar a Hakkar", "hakkar", "Hakkar", dur=4.0),
    peg("Ysera, la aspecto", "ysera", "Ysera", dur=5.0, x=.26, y=.50, tam=640),
    peg("para que aparezca un jefe oculto", "atalalarion", "Atal'alarion", dur=4.5),
    peg("el gran cruzado Dathrohan", "dathrohan", "Dathrohan", dur=5.0),
    peg("es Balnazzar, un señor del terror", "balnazzar", "Balnazzar", dur=5.0, x=.25, y=.50, tam=640),
    peg("el archimago Arugal", "arugal", "Arugal", dur=5.0),
    peg("invocó a los huargen", "huargen", "Huargen", dur=4.5),
    peg("se llama Varimathras", "varimathras", "Varimathras", dur=5.5, x=.26, y=.50, tam=700),
    peg("la Aldea Piroleña parece", "pirolena", "Aldea Piroleña", dur=5.0),
    peg("se convierten en huargen", "huargen", "Huargen de Piroleña", dur=4.5),
    peg("está Aurius, un paladín", "aurius", "Aurius", dur=5.0),
    peg("contra el barón Rivendare, la puerta", "rivendare", "Barón Rivendare", dur=4.0),
    peg("frente a cualquier gallina", "gallina", "Gallina", dur=4.5),
    peg("el granjero Saldean", "saldean", "Granjero Saldean", dur=4.5),
    peg("sale tu propia gallina", "gallina", "Tu gallina", dur=4.5, x=.75, y=.52, tam=640),
    peg("Es la Crematoria, la Ashbringer", "ashbringer", "La Ashbringer", dur=4.2, x=.27, y=.50, tam=760),
    peg("existe una versión corrupta", "ashbringer_c", "Ashbringer corrupta", dur=3.4, x=.25, y=.50, tam=600),
    peg("uno de los Cuatro Jinetes", "mograine_hl", "Alto señor Mograine", dur=5.0),
    peg("el espíritu de Alexandros Mograine", "alexandros", "Alexandros Mograine", dur=5.0),
    peg("porque ese comandante es su hijo, Renault", "renault", "Renault Mograine", dur=2.6, x=.75, y=.50, tam=600),
    # ---- pegatinas nuevas (18-oct, «mete más pegatinas, de diferentes tamaños y posiciones»)
    peg("Lo que queda de aquella cuna es Stromgarde", "stromgarde", "Stromgarde", dur=4.5, x=.22, y=.40, tam=520),
    peg("lanzaba una maldición que saltaba", "sangre_corrupta", "Sangre Corrupta", dur=4.0, x=.59, y=.19, tam=250),
    peg("es el sombrero de almirante Velasangre", "sombrero_velasangre", "Sombrero de almirante", dur=5.0, x=.26, y=.50, tam=560),
    peg("sus páginas andan desperdigadas", "pagina", "Página del libro", dur=4.0, x=.20, y=.66, tam=300),
    peg("cuarenta peces sabrosos moteados", "pez_moteado", "Pez sabroso moteado", dur=3.0, x=.13, y=.66, tam=300),
    peg("una caña de arcanita", "cana_arcanita", "Caña de arcanita", dur=4.5, x=.20, y=.62, tam=320),
    peg("En la Arena Gurubashi aparece", "arena_gurubashi", "Arena Gurubashi", dur=4.0, x=.76, y=.42, tam=560),
    peg("está el Grim Guzzler", "grim_guzzler", "Grim Guzzler", dur=4.0, x=.25, y=.45, tam=560),
    peg("llevarte las jarras de la barra", "jarra", "Jarra", dur=2.6, x=.17, y=.66, tam=300),
    peg("comandantes, misiones y refuerzos", "vanndar", "Vanndar Pico Tormenta", dur=5.0, x=.14, y=.60, tam=420),
    peg("misiones y refuerzos que no se acababan", "drekthar", "Drek'Thar", dur=4.5, x=.36, y=.60, tam=420),
    peg("hasta el Puerto de Menethil", "menethil", "Puerto de Menethil", dur=5.0, x=.27, y=.50, tam=580),
    peg("empiezan a convertir en oveja", "oveja", "Oveja", dur=3.5, x=.17, y=.64, tam=320),
    peg("te dejaba con los boletos en la mano", "boleto", "Boleto de la feria", dur=3.5, x=.20, y=.62, tam=320),
    peg("Ragnaros en el fondo", "ragnaros", "Ragnaros", dur=3.5, x=.84, y=.36, tam=420),
    peg("el Vuelo Negro arriba", "nefarian", "Vuelo Negro", dur=3.5, x=.16, y=.36, tam=420),
    peg("una pista de aterrizaje enana", "girocoptero", "Girocóptero enano", dur=5.0, x=.25, y=.50, tam=600),
    peg("el reino de los altos elfos", "alto_elfo", "Alto elfo", dur=4.5, x=.22, y=.55, tam=560),
    peg("Renault traicionó a su propio padre", "alexandros", "Alexandros (padre)", dur=6.5, x=.25, y=.50, tam=600),
    peg("lo más difícil no es tumbar a Ragnaros", "ragnaros", "Ragnaros", dur=2.8, x=.25, y=.50, tam=560),
    peg("es convencer a una gallina", "gallina", "La gallina", dur=6.0, x=.72, y=.50, tam=760),
    # dict(tipo="abre", en=0, dur=.8),
    # dict(tipo="temblor", en="palabras de la voz", amp=34),
    # dict(tipo="destello", en="palabras de la voz"),
    # dict(tipo="latido", de="desde estas palabras", a="hasta estas|fin"),
]
ROTULOS = [
    # dict(texto="DOS PALABRAS", en="palabras de la voz", tam=150, color="amarillo", y=.2),
]
SFX = {
    # "boom": ("Deep cinematic sub boom hit with a long reverb tail", 4),
}
PISTAS = [
    # dict(sfx="boom", en="palabras de la voz", vol=.6),
]

# APOYOS: tooltips REALES de Wowhead (classic; ids comprobados el 18-oct en nether.wowhead.com) y tarjetas SOLO con datos del guion.
V, GRIS, ROJO = "verde", "gris", "#ff3b3b"
APOYOS = [
    # ---- intro
    dict(en="vuelve el cuatro de noviembre", dur=3.6, x=.72, size=.44, tarjeta=dict(titulo="World of Warcraft Forever",
         calidad="amarillo", icono="inv_misc_map_01", lineas=["Sale el 4 de noviembre", dict(t="Los Reinos del Este, otra vez", c=GRIS)])),
    dict(en="sesenta y dos curiosidades de los Reinos", dur=5.0, tarjeta=dict(titulo="62 curiosidades", calidad="oro",
         icono="inv_misc_questionmark", lineas=["Reinos del Este, tal como están en Classic", dict(t="Cuenta regresiva: 62 → 1", c=GRIS)])),
    # ---- 62 Malown
    dict(en="Cada buzón que abres suelta", dur=5.0, x=.72, size=.46, tarjeta=dict(titulo="Buzones de Stratholme", calidad="blanco",
         icono="inv_letter_01", lineas=[dict(t="Cada buzón", der="3 carteros de élite"), dict(t="3 buzones abiertos", der="Malown", c=V)])),
    # Wowhead es-MX lo llama «Jefe de correos Gassol»: tarjeta con el nombre que dice la voz
    dict(en="el jefe de correos Malown", dur=4.5, x=.72, size=.44, anim="fade", tarjeta=dict(titulo="Jefe de correos Malown",
         calidad="blanco", icono="spell_shadow_raisedead", lineas=["Nivel 60 · No-muerto (élite)", dict(t="Fantasma de Stratholme", c=GRIS)])),
    dict(en="un conjunto completo de cartero", dur=4.5, x=.72, size=.44, tarjeta=dict(titulo="Conjunto del jefe de correos",
         calidad="amarillo", icono="inv_letter_01", lineas=["Solo lo suelta Malown"])),
    # ---- 61 Gahz'ranka
    dict(en="Se llama Gahz'ranka", dur=5.0, x=.72, size=.44, wowhead="classic/npc/15114"),
    # ---- 60 R.O.I.D.S.
    dict(en="Nethergarde hay dos magos", dur=5.0, x=.72, size=.46, tarjeta=dict(titulo="Castillo de Nethergarde", calidad="blanco",
         icono="achievement_zone_blastedlands_01", lineas=["Partes de monstruos → consumibles", dict(t="Fuerza, agilidad o intelecto", c=GRIS)])),
    # Wowhead es-MX lo traduce «IFRDHR»: tarjeta con el nombre en inglés y los datos reales del tooltip (classic/8410)
    dict(en="se llama, con todas sus letras", dur=6.5, tarjeta=dict(titulo="R.O.I.D.S.", calidad="blanco", icono="inv_potion_61",
         lineas=[dict(t="Uso: aumenta 25 p. la fuerza", c=V), "El efecto dura 60 minutos", dict(t="Castillo de Nethergarde", c=GRIS)])),
    # ---- 59 Barov
    dict(en="De la familia quedan dos herederos", dur=6.5, x=.72, size=.46, tarjeta=dict(titulo="Herederos Barov", calidad="amarillo",
         icono="inv_scroll_03", lineas=[dict(t="Weldon · humano", der="Alianza"), dict(t="Alexi · renegado", der="Horda", c=ROJO)])),
    dict(en="Los dos quieren las escrituras", dur=5.0, x=.72, size=.44, anim="fade", tarjeta=dict(titulo="Escrituras Barov",
         calidad="blanco", icono="inv_scroll_03", lineas=["Caer Darrow", "Rémol", "Molino Tarren", "Costasur"])),
    # ---- 58 Hogger
    dict(en="Es un gnoll de élite de nivel once", dur=5.5, x=.72, size=.44, wowhead="classic/npc/448"),
    dict(en="lo convirtió en carta de Hearthstone", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Hogger, fuera de Elwynn",
         calidad="amarillo", icono="inv_misc_head_gnoll_01", lineas=["Carta de Hearthstone", "Jefe de las Mazmorras de Ventormenta",
                                                                     dict(t="Meme de más de 20 años", c=GRIS)])),
    # ---- 57 Myzrael
    dict(en="resulta que Myzrael es un elemental", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Myzrael", calidad="amarillo",
         icono="spell_nature_earthquake", lineas=[dict(t="«Una princesa atrapada»", c=V), dict(t="Elemental de tierra encerrada", c=ROJO)])),
    # ---- 56 kobolds
    dict(en="Tú no llevar vela", dur=3.0, tarjeta=dict(titulo="Kobold de Elwynn", calidad="blanco", icono="inv_misc_candle_01",
         lineas=[dict(t="«¡Tú no llevar vela!»", c=V), dict(t="You no take candle!", c=GRIS)])),
    # ---- 55 Stonefield y Maclure
    dict(en="los Stonefield y los Maclure", dur=5.0, x=.72, size=.46, tarjeta=dict(titulo="Granjas de Elwynn", calidad="blanco",
         icono="inv_letter_01", lineas=[dict(t="Maybell Maclure", der="♥"), dict(t="Tommy Joe Stonefield", der="♥")])),
    dict(en="los Hatfield y los McCoy", dur=5.5, tarjeta=dict(titulo="No es Romeo y Julieta", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=["Referencia: Hatfield contra McCoy", dict(t="La pelea de familias más famosa de EE. UU.", c=GRIS)])),
    # ---- 54 Arathor
    dict(en="el caudillo Thoradin unió", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Arathor", calidad="oro", icono="inv_misc_map_01",
         lineas=["Lo funda Thoradin", dict(t="Capital", der="Strom"), dict(t="Hace casi 3 000 años", c=GRIS)])),
    dict(en="De Arathor salieron después", dur=6.0, x=.72, size=.44, anim="fade", tarjeta=dict(titulo="Los hijos de Arathor",
         calidad="blanco", icono="inv_misc_map_01", lineas=["Ventormenta", "Lordaeron", "Gilneas", "Kul Tiras", "Alterac", "Dalaran"])),
    # ---- 53 Leeroy
    dict(en="planea la entrada con todo detalle", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Pals for Life · 2005",
         calidad="amarillo", icono="inv_misc_note_01", lineas=[dict(t="Probabilidad de sobrevivir", der="32,33 %"),
                                                              dict(t="Cumbre de Roca Negra", c=GRIS)])),
    dict(en="Leeroy Jenkins. El grupo entero", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="LEEROY JENKINS", calidad="oro",
         icono="inv_misc_questionmark", lineas=[dict(t="«Por lo menos tengo pollo»", c=V)])),
    # ---- 52 Uldaman
    dict(en="los Discos de Norgannon", dur=7.0, x=.72, size=.46, tarjeta=dict(titulo="Discos de Norgannon", calidad="oro",
         icono="inv_misc_gem_pearl_04", lineas=["Los titanes crean a los terráneos (piedra)", dict(t="Maldición de la Carne", c=ROJO),
                                                dict(t="De ellos descienden los enanos", c=V)])),
    # ---- 51 Minas de la Muerte
    dict(en="su líder, Edwin VanCleef", dur=5.5, x=.72, size=.44, wowhead="classic/npc/639"),
    # ---- 50 Los Siete
    dict(en="Y fíjate en los nombres", dur=10.0, x=.72, size=.46, tarjeta=dict(titulo="Los Siete", calidad="oro",
         icono="spell_shadow_raisedead", lineas=[dict(t="Anger'rel", der="ira"), dict(t="Seeth'rel", der="rabia"),
                                                dict(t="Dope'rel", der="tontería"), dict(t="Gloom'rel", der="tristeza"),
                                                dict(t="Vile'rel", der="vileza"), dict(t="Hate'rel", der="odio"),
                                                dict(t="Doom'rel", der="perdición", c=ROJO)])),
    # ---- 49 Ragnaros
    dict(en="el mayordomo Executus te entrega", dur=5.5, x=.72, size=.44, wowhead="classic/npc/11502"),
    dict(en="Su grito es too soon", dur=4.5, tarjeta=dict(titulo="Ragnaros", calidad="oro", icono="spell_shadow_raisedead",
         lineas=[dict(t="«TOO SOON!»", c=ROJO), "«¡Demasiado pronto!»"])),
    # ---- 48 Lothos
    # Wowhead es-MX: «Lothos Levantagrietas»; la voz dice Riftwaker -> tarjeta
    dict(en="Por eso existe Lothos Riftwaker", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Lothos Riftwaker", calidad="blanco",
         icono="inv_misc_key_03", lineas=["Nivel 60 · Humanoide (élite)", dict(t="Sintonización al Núcleo de Magma", der="nivel 55", c=V)])),
    # ---- 47 Costasur / Molino Tarren
    dict(en="Costasur de la Alianza y Molino Tarren", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Laderas de Trabalomas", calidad="blanco",
         icono="inv_misc_map_01", lineas=[dict(t="Costasur", der="Alianza"), dict(t="Molino Tarren", der="Horda", c=ROJO)])),
    # ---- 46 Stitches
    dict(en="Cuando terminas su cadena", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Stitches", calidad="amarillo",
         icono="spell_shadow_raisedead", lineas=["Abominación de Abercrombie", dict(t="Camina hasta Villa Oscura", c=ROJO)])),
    # ---- 45 Sangre Corrupta
    dict(en="lanzaba una maldición que saltaba", dur=5.0, x=.72, size=.46, wowhead="classic/spell/24328"),
    dict(en="Fue tan realista que unos epidemiólogos", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Sangre Corrupta · 2005",
         calidad="blanco", icono="spell_shadow_raisedead", lineas=["Estudiada por epidemiólogos", dict(t="Modelo de reacción ante un brote", c=GRIS)])),
    # ---- 44 Velasangre
    dict(en="es el sombrero de almirante Velasangre", dur=6.0, x=.72, size=.46, wowhead="classic/12185"),
    # ---- 43 Onyxia
    dict(en="Katrana Prestor es Onyxia", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Lady Katrana Prestor", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=[dict(t="Consejera del rey niño", c=GRIS), dict(t="En realidad: Onyxia, hija de Alamuerte", c=ROJO)])),
    # ---- 42 Monty
    dict(en="Te da una flauta y una misión", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Misión de Monty", calidad="blanco",
         icono="inv_misc_note_01", lineas=["Toca la flauta", "Las ratas te siguen", dict(t="Llévaselas a Monty", c=V)])),
    # ---- 41 barón
    dict(en="tienes cuarenta y cinco minutos", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="Stratholme", calidad="blanco",
         icono="spell_shadow_raisedead", lineas=[dict(t="Tiempo para salvar a Ysida", der="45 min", c=ROJO)])),
    dict(en="las riendas del destrero de la muerte", dur=6.0, x=.72, size=.46, wowhead="classic/13335"),
    # ---- 40 OOX
    # ---- 39 Andorhal
    dict(en="mezclaron la plaga con el grano", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Andorhal", calidad="blanco",
         icono="spell_shadow_raisedead", lineas=["Centro de reparto de grano", dict(t="Grano apestado → no-muertos", c=ROJO)])),
    # ---- 38 Nesingwary
    dict(en="Las verdes colinas de África", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Hemingway → Nesingwary", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Hemingway: Las verdes colinas de África", dict(t="Nesingwary: Las verdes colinas de Tuercespina", c=V)])),
    # ---- 37 Monasterio
    dict(en="la misma frase del señor Burns", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="«Release the hounds!»", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=[dict(t="Loksey · Monasterio Escarlata", c=V), dict(t="Señor Burns · Los Simpson", c=GRIS)])),
    # ---- 36 concurso de pesca
    dict(en="cada domingo de dos a cuatro", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Concurso de pesca de Tuercespina",
         calidad="oro", icono="inv_misc_fish_02", lineas=[dict(t="Domingos", der="14:00-16:00"), dict(t="Peces sabrosos moteados", der="40"),
                                                          dict(t="Bahía del Botín", c=GRIS)])),
    dict(en="una caña de arcanita", dur=5.5, x=.72, size=.46, wowhead="classic/19970"),
    # ---- 35 Entrañas
    dict(en="primero cruzas las ruinas", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Entrañas", calidad="blanco",
         icono="spell_shadow_raisedead", lineas=["Bajo las ruinas de Lordaeron", dict(t="El salón donde Arthas mató a Terenas", c=ROJO)])),
    # ---- 34 Gurubashi
    dict(en="Quien lo abre se queda", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Arena Gurubashi", calidad="amarillo",
         icono="inv_misc_coin_01", lineas=[dict(t="Cofre", der="cada 3 h"), dict(t="Todos contra todos", c=ROJO)])),
    # ---- 33 Grim Guzzler
    dict(en="un bar de enanos Hierro Negro", dur=5.5, x=.72, size=.46, tarjeta=dict(titulo="Grim Guzzler", calidad="blanco",
         icono="inv_misc_candle_01", lineas=["Taberna en las Profundidades de Roca Negra", dict(t="No robes las jarras", c=ROJO)])),
    # ---- 32 Karazhan
    dict(en="Blizzard la abrió como banda", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Karazhan", calidad="oro",
         icono="inv_misc_key_03", lineas=[dict(t="Classic", der="cerrada"), dict(t="The Burning Crusade", der="banda", c=V)])),
    # ---- 31 Tirion
    dict(en="Tirion llega al galope", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="La cadena de Tirion", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["Tierras de la Peste del Este", dict(t="Taelan muere ante su padre", c=ROJO)])),
    # ---- 30 Naxxramas
    dict(en="Era la banda más difícil del juego", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Naxxramas", calidad="oro",
         icono="spell_shadow_raisedead", lineas=["Último gran parche del juego original", dict(t="Muy pocos la vieron completa", c=GRIS)])),
    # ---- 29 Pamela
    dict(en="Te pide que encuentres su muñeca", dur=5.0, x=.72, size=.44, tarjeta=dict(titulo="La muñeca de Pamela", calidad="blanco",
         icono="inv_misc_questionmark", lineas=["Pedazos repartidos por Darrowshire"])),
    # ---- 28 Valle de Alterac
    dict(en="con cuarenta jugadores por bando", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Valle de Alterac original",
         calidad="amarillo", icono="inv_misc_map_01", lineas=[dict(t="Jugadores por bando", der="40"), dict(t="Duración", der="horas o días", c=ROJO)])),
    # ---- 27 Grim Batol
    dict(en="Grim Batol, una antigua fortaleza", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Grim Batol", calidad="blanco",
         icono="inv_misc_key_03", lineas=[dict(t="Classic", der="cerrada"), dict(t="Prisión de Alexstrasza", c=ROJO)])),
    # ---- 26 puerto
    dict(en="Para tomar un barco", dur=6.0, x=.72, size=.46, tarjeta=dict(titulo="Barcos de la Alianza en Classic", calidad="blanco",
         icono="inv_misc_map_01", lineas=["Puerto de Menethil (Los Humedales)", "Bahía del Botín",
                                          dict(t="Puerto de Ventormenta: llega con el Rey Exánime", c=GRIS)])),
    # ---- 25 Pesadilla (arriba: abajo van las 4 pegatinas)
    dict(en="De esos portales salían", dur=5.0, x=.72, y=.22, size=.42, tarjeta=dict(titulo="Dragones de la Pesadilla", calidad="oro",
         icono="spell_shadow_raisedead", lineas=["4 jefes de mundo", dict(t="Salían de los portales del Sueño Esmeralda", c=GRIS)])),
    # ---- 24 Gilneas
    dict(en="En el juego original, Gilneas", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Gilneas", calidad="blanco",
         icono="inv_misc_key_03", lineas=[dict(t="Classic", der="cerrada"), dict(t="Cataclysm", der="inicio huargen", c=V)])),
    # ---- 22 Moira
    dict(en="en lugar de darte las gracias", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Moira Barbabronce", calidad="amarillo",
         icono="inv_jewelry_ring_03", lineas=["Hija de Magni", dict(t="Esposa de Dagran Thaurissan", c=ROJO)])),
    # ---- 21 Thrall
    dict(en="que en inglés significa esclavo", dur=4.5, x=.72, size=.42, tarjeta=dict(titulo="Thrall", calidad="blanco",
         icono="inv_misc_note_01", lineas=[dict(t="thrall (inglés)", der="esclavo", c=ROJO)])),
    # ---- 20 gnomos
    dict(en="Así que los gnomos son refugiados", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Gnomeregan", calidad="blanco",
         icono="inv_misc_questionmark", lineas=[dict(t="Classic", der="sin zona de inicio"), dict(t="Viven en", der="Ciudad Manitas")])),
    # ---- 19 Ravenholdt
    dict(en="Mucha gente jugó años en Trabalomas", dur=5.5, x=.72, size=.42, tarjeta=dict(titulo="Mansión Ravenholdt", calidad="blanco",
         icono="inv_misc_key_03", lineas=["Montañas de Alterac", dict(t="Liga de asesinos", c=ROJO)])),
    # ---- 18 Nefarian
    dict(en="Grita guerreros y los fuerza", dur=12.0, x=.72, size=.46, tarjeta=dict(titulo="Nefarian llama a tu clase", calidad="oro",
         icono="spell_shadow_raisedead", lineas=[dict(t="Guerreros", der="actitud rabiosa"), dict(t="Cazadores", der="arco roto"),
                                                dict(t="Sacerdotes", der="curar hace daño", c=ROJO), dict(t="Druidas", der="forma felina"),
                                                dict(t="Magos", der="ovejas aliadas", c=ROJO)])),
    # ---- 17 Bosque del Ocaso
    dict(en="La zona está siempre en penumbra", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Bosque del Ocaso", calidad="blanco",
         icono="spell_shadow_raisedead", lineas=["Penumbra perpetua", dict(t="Sombra de Karazhan y de la Pesadilla", c=GRIS)])),
    # ---- 16 monturas de Zul'Gurub
    # una sola tarjeta: las dos fichas de Wowhead iban a 1,8 s una de otra y se encimaban (fx_08, 1335 s)
    dict(en="Thekal un tigre", dur=7.0, x=.72, size=.44, tarjeta=dict(titulo="Monturas de Zul'Gurub", calidad="morado",
         icono="ability_mount_jungletiger", lineas=[dict(t="Tigre zulian presto", der="Thekal", c="morado"),
                                          dict(t="Raptor Razzashi presto", der="Mandokir", c="morado"),
                                          dict(t="Botín raro de jefe · nivel 60", c=GRIS)])),
    # ---- 15 Feria
    dict(en="unas semanas a las afueras de Villadorada", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Feria de la Luna Negra",
         calidad="amarillo", icono="inv_misc_coin_01", lineas=[dict(t="Villadorada", der="Elwynn"), dict(t="Mulgore", der="Kalimdor")])),
    # ---- 14 Kazzak
    dict(en="Kazzak se curaba", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Lord Kazzak", calidad="oro", icono="spell_shadow_raisedead",
         lineas=["Jefe de mundo · Tierras Devastadas", dict(t="Se cura al matar jugadores", c=ROJO)])),
    # ---- 13 Atal'Hakkar
    dict(en="seis estatuas que hay que activar", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Templo de Atal'Hakkar", calidad="amarillo",
         icono="inv_misc_questionmark", lineas=[dict(t="Estatuas", der="6"), dict(t="Orden exacto → jefe oculto", c=V)])),
    # ---- 12 Forjaz
    dict(en="La casa de subastas y el banco", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Forjaz", calidad="blanco",
         icono="inv_misc_coin_01", lineas=["Subastas y banco a unos pasos", dict(t="La capital de verdad de la Alianza", c=V)])),
    # ---- 11 Dalaran
    dict(en="el Kirin Tor la está reconstruyendo", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Dalaran", calidad="amarillo",
         icono="inv_misc_gem_pearl_04", lineas=[dict(t="Classic", der="burbuja violeta"), dict(t="Rey Exánime", der="vuela a Rasganorte")])),
    # ---- 10 Montaña Roca Negra
    # ---- 09 Dathrohan
    dict(en="Los señores del terror son los demonios", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Gran cruzado Dathrohan",
         calidad="amarillo", icono="spell_shadow_raisedead", lineas=[dict(t="En realidad: Balnazzar, señor del terror", c=ROJO)])),
    # ---- 08 Arugal
    dict(en="convencido de que podría controlarlos", dur=5.5, x=.72, size=.42, tarjeta=dict(titulo="Archimago Arugal", calidad="blanco",
         icono="spell_shadow_raisedead", lineas=["Mago de Dalaran", dict(t="Invocó a los huargen", c=ROJO)])),
    # ---- 07 Varimathras
    dict(en="además es hermano de Balnazzar", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Varimathras", calidad="amarillo",
         icono="spell_shadow_raisedead", lineas=["Señor del terror", dict(t="Hermano de Balnazzar", c=ROJO),
                                                dict(t="Traiciona a Sylvanas en el Rey Exánime", c=GRIS)])),
    # ---- 06 aeródromo
    dict(en="hay un valle alto con una pista", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Aeródromo de Forjaz", calidad="amarillo",
         icono="inv_misc_map_01", lineas=[dict(t="Classic", der="sin nombre en el mapa"), dict(t="Citado en el esfuerzo de guerra de Ahn'Qiraj", c=GRIS)])),
    # ---- 05 Quel'Thalas
    dict(en="Ahí está Quel'Thalas", dur=6.5, x=.72, size=.46, tarjeta=dict(titulo="Quel'Thalas", calidad="amarillo",
         icono="inv_misc_map_01", lineas=[dict(t="Classic", der="no se puede entrar"), dict(t="The Burning Crusade", der="Canción Eterna", c=V),
                                          dict(t="Teoría de jugadores, no oficial", c=GRIS)])),
    # ---- 04 Aldea Piroleña
    dict(en="Los centinelas pasan a ser huargen", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Aldea Piroleña", calidad="amarillo",
         icono="spell_shadow_raisedead", lineas=[dict(t="De día", der="humanos"), dict(t="De noche", der="huargen de élite", c=ROJO)])),
    # ---- 03 Aurius
    dict(en="te pide un medallón de fe", dur=5.5, x=.72, size=.46, wowhead="classic/12845"),
    dict(en="porque Aurius es hijo del barón", dur=5.5, x=.72, size=.44, tarjeta=dict(titulo="Aurius", calidad="oro",
         icono="inv_jewelry_ring_03", lineas=[dict(t="Hijo del barón Rivendare", c=ROJO), dict(t="Muere peleando a tu lado", c=GRIS)])),
    # ---- 02 CLUCK!
    dict(en="que se llama, con toda la seriedad", dur=3.5, x=.72, size=.44, tarjeta=dict(titulo="CLUCK!", calidad="amarillo",
         icono="spell_magic_polymorphchicken", lineas=["Misión oculta", dict(t="Gesto de gallina, una y otra vez", c=V)])),
    dict(en="Te pide un pienso especial", dur=5.5, x=.72, size=.46, wowhead="classic/11109"),
    # ---- 01 Ashbringer
    dict(en="La suelta en Naxxramas", dur=6.5, x=.72, size=.46, wowhead="classic/22691"),
    dict(en="se giran hacia ti y se arrodillan", dur=6.0, x=.72, size=.44, tarjeta=dict(titulo="Monasterio Escarlata", calidad="oro",
         icono="inv_misc_questionmark", lineas=[dict(t="Los cruzados se arrodillan", c=V), dict(t="Solo con la Ashbringer corrupta", c=GRIS)])),
    dict(en="Renault traicionó a su propio padre", dur=6.5, x=.72, size=.44, tarjeta=dict(titulo="Renault Mograine", calidad="amarillo",
         icono="spell_shadow_raisedead", lineas=[dict(t="Mató a su padre con su espada", c=ROJO), dict(t="Así se corrompió la Ashbringer", c=GRIS)])),
]
