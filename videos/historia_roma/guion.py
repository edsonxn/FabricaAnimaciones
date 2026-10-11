# -*- coding: utf-8 -*-
"""La historia de Roma en 5 minutos (estilo BOCETO + GUACHE, 16:9, plano secuencia sobre un mapa del Mediterráneo).

Canal Cronopapel, video de prueba técnica. Hilo narrativo: de una humilde aldea de pastores a orillas del Tíber,
hasta convertirse en el mayor imperio de la antigüedad, su fractura y su legado eterno.

Datos y fuentes históricas (Tito Livio, Polibio, Tácito, Suetonio, Cambridge Ancient History, UNESCO):
  - Fundación tradicional de Roma: 753 a. C. en el monte Palatino, junto al Tíber. Siete reyes tradicionales.
  - Expulsión de Tarquinio el Soberbio en 509 a. C.: fundación de la República romana (SPQR).
  - Guerras samnitas (343-290 a. C.) y conquista de la Magna Grecia (Pirro, 280-275 a. C.). Construcción de la Vía Apia (312 a. C.).
  - Guerras Púnicas contra Cartago (264-146 a. C.): Aníbal cruza los Alpes (218 a. C.), batalla de Cannas (216 a. C.), Escipión vence en Zama (202 a. C.), destrucción de Cartago (146 a. C.).
  - Mare Nostrum: conquista de Macedonia, Grecia (146 a. C.), Hispania y el reino de Pérgamo.
  - Julio César: Guerra de las Galias (58-50 a. C.), cruce del Rubicón (49 a. C.), dictadura y asesinato en los Idus de Marzo (15 de marzo de 44 a. C.).
  - Augusto (Octavio) vence en Accio (31 a. C.) y se convierte en el primer emperador en 27 a. C. Inicio de la Pax Romana. Coliseo inaugurado en 80 d. C.
  - Trajano (98-117 d. C.): máxima extensión territorial del Imperio (Britania a Mesopotamia, Dacia, Arabia Pétrea).
  - Crisis del siglo III (235-284 d. C.): anarquía militar, presión bárbara e inflación.
  - Diocleciano (tetrarquía en 284-305 d. C.) y Constantino el Grande (Edicto de Milán 313 d. C., fundación de Constantinopla 330 d. C.). División definitiva del imperio en 395 d. C.
  - Saqueos de Roma (Alarico 410, vándalos 455). Rómulo Augústulo depuesto en 476 d. C. El Imperio de Oriente (Bizancio) sobrevive hasta 1453.
"""

TITULO = "La historia de Roma en 5 minutos"
ARCHIVO = "historia_roma_5min"
ESTILO_VISUAL = "boceto"
DURACION = None
BPM = 112
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Gaia.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.5)

# Equivalencias fonéticas y ortográficas para el control de calidad de Whisper
ALIAS_QA = {
    "spqr": "ese pe cu erre", "s.p.q.r.": "ese pe cu erre",
    "cesar": "césar", "julio cesar": "julio césar", "tiber": "tíber", "rubicon": "rubicón",
    "anibal": "aníbal", "escipion": "escipión", "trajano": "trajano",
    "diocleciano": "diocleciano", "constantino": "constantino", "constantinopla": "constantinopla",
    "bizancio": "bizancio", "bizantino": "bizantino", "romulo": "rómulo",
    "mare nostrum": "mare nostrum", "samnitas": "samnitas", "etruscos": "etruscos",
    "siglo tres": "siglo tercero",
}

SUBTITULOS = False            # subtítulos en .srt para YouTube, no quemados
TRANSICIONES = [("continua", 0.1)] * 12
MUSICA = {
    "gancho": dict(sabor="epico", raiz=41),
    "origenes": dict(sabor="ambiente", raiz=41),
    "republica": dict(sabor="lounge", raiz=43),
    "italia": dict(sabor="epico", raiz=43),
    "cartago": dict(sabor="tension", raiz=41),
    "mediterraneo": dict(sabor="epico", raiz=43),
    "cesar": dict(sabor="tension", raiz=41),
    "imperio": dict(sabor="esperanza", raiz=43),
    "maxima": dict(sabor="epico", raiz=45),
    "crisis": dict(sabor="tension", raiz=40),
    "division": dict(sabor="ambiente", raiz=41),
    "caida": dict(sabor="esperanza", raiz=41),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.6, "frases": [
        "Una pequeña aldea de chozas de barro junto a un río terminó conquistando todo el mundo conocido.",
        "Gobernó sobre tres continentes y cincuenta millones de personas.",
        "Esta es la historia de Roma, en cinco minutos.",
    ]},
    {"id": "origenes", "frases": [
        "Todo comienza en el año setecientos cincuenta y tres antes de Cristo, a orillas del río Tíber.",
        "Pastores latinos se asientan entre siete colinas para defenderse y comerciar.",
        "Nace Roma, gobernada primero por reyes bajo la influencia de sus poderosos vecinos etruscos.",
    ]},
    {"id": "republica", "frases": [
        "Pero en el año quinientos nueve antes de Cristo, los romanos se cansan de la tiranía y expulsan a su último rey.",
        "Juran que ningún hombre volverá a coronarse en Roma: nace la República.",
        "El poder se reparte entre los cónsules y el Senado, bajo un lema eterno: el Senado y el pueblo de Roma, ese pe cu erre.",
    ]},
    {"id": "italia", "frases": [
        "Rodeada de enemigos feroces, Roma aprende a pelear como nadie.",
        "Sus legiones derrotan a los samnitas en las montañas, construyen calzadas de piedra como la Vía Apia y absorben las ciudades griegas del sur.",
        "En dos siglos, la península itálica entera ondea el estandarte romano.",
    ]},
    {"id": "cartago", "frases": [
        "Pero el mar Mediterráneo ya tenía un dueño: Cartago, una rica potencia comercial del norte de África.",
        "El choque es inevitable. El general Aníbal cruza los Alpes nevados con elefantes y aplasta a las legiones.",
        "Aun al borde del abismo, Roma jamás se rinde. Escipión contraataca en África y Cartago es reducida a cenizas.",
    ]},
    {"id": "mediterraneo", "frases": [
        "Ahora nada puede detener a Roma.",
        "Grecia, Macedonia, Hispania y las costas de Asia Menor caen una tras otra.",
        "El Mediterráneo pasa a llamarse simplemente Mare Nostrum: nuestro mar.",
    ]},
    {"id": "cesar", "frases": [
        "Pero tanto oro y poder desestabilizan a la República.",
        "Los generales acumulan ejércitos leales a su mando y no a las leyes.",
        "Julio César conquista las Galias, cruza el río Rubicón desafiando al Senado y se proclama dictador.",
        "En los Idus de Marzo del cuarenta y cuatro antes de Cristo, es asesinado a puñaladas.",
    ]},
    {"id": "imperio", "frases": [
        "La República ya no puede salvarse. Tras otra guerra civil, su sobrino Octavio Augusto se convierte en el primer emperador.",
        "Comienza la Pax Romana: dos siglos de orden, comercio, acueductos colosales y el gran Coliseo.",
    ]},
    {"id": "maxima", "frases": [
        "En el año ciento diecisiete después de Cristo, con el emperador Trajano, el Imperio alcanza su máxima gloria.",
        "Se extiende desde la lluviosa Britania hasta el desierto de Arabia, y desde el Atlántico hasta el río Éufrates.",
    ]},
    {"id": "crisis", "frases": [
        "Pero un territorio tan gigantesco se vuelve casi imposible de defender.",
        "En el siglo tercero, la peste, las guerras civiles y decenas de emperadores caídos llevan a Roma al borde del colapso.",
        "Pueblos germánicos presionan las fronteras del Rin y el Danubio.",
    ]},
    {"id": "division", "frases": [
        "Para gobernar semejante imperio, se decide dividirlo en dos mitades: Occidente y Oriente.",
        "El emperador Constantino funda una nueva capital en el este: Constantinopla.",
        "Mientras Oriente se enriquece, el Imperio de Occidente se desangra y pierde sus provincias.",
    ]},
    {"id": "caida", "frases": [
        "En el año cuatrocientos setenta y seis, el último emperador de Roma es depuesto.",
        "Occidente colapsa, mientras Oriente sobrevivirá mil años más como el Imperio Bizantino.",
        "Pero Roma jamás murió del todo: sus leyes, sus idiomas, su arte y su pensamiento siguen vivos en nosotros.",
    ]},
]
