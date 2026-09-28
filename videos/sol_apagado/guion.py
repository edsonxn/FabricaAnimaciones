# -*- coding: utf-8 -*-
"""¿Qué pasaría si el Sol se apagara? — 1 minuto, estilo Kurzgesagt (vector plano, espacio, brillos).
PLANO SECUENCIA: no hay cortes; las "escenas" solo marcan secciones de narración y música. Todo se dibuja
en un único mundo continuo (escenas.py -> Mundo) donde cada cosa se transforma en la siguiente.

Datos verificados:
  - La luz del Sol tarda ~8 min 20 s (499 s) en llegar a la Tierra (NASA).
  - Los cambios de gravedad viajan a la velocidad de la luz (ondas gravitacionales, GW170817, LIGO/Virgo 2017).
  - Velocidad orbital media de la Tierra: 29,78 km/s (NASA Earth Fact Sheet).
  - Temperatura media: bajo 0 °F (−18 °C) en una semana; ~−100 °F (−73 °C) en un año;
    el hielo superficial aísla el agua de abajo (David Stevenson, Caltech; Popular Science / Live Science).
  - Microbios de la corteza y de fuentes hidrotermales (quimiosíntesis) sobrevivirían.
  - Al Sol le quedan ~5 000 millones de años en la secuencia principal (NASA).
"""

TITULO = "¿Qué pasaría si el Sol se apagara?"
ARCHIVO = "si_el_sol_se_apagara"
ESTILO_VISUAL = "kurzgesagt"
DURACION = 60.0
BPM = 100
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)      # narración casi continua: fondo un poco más bajo
TRANSICIONES = [("continua", 0.1)] * 5      # sin cortes: el mundo se transforma solo
MUSICA = {
    "intro": dict(sabor="espacio"),
    "luz": dict(sabor="tension"),
    "deriva": dict(sabor="vacio"),
    "frio": dict(sabor="vacio", raiz=38),
    "vida": dict(sabor="esperanza"),
    "cierre": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Imagina que, de repente, el Sol se apaga.",
            "¿Qué le pasaría a la Tierra?",
        ],
    },
    {
        "id": "luz",
        "frases": [
            "Durante unos ocho minutos, no notarías nada.",
            "Su última luz sigue en camino, y su gravedad tarda lo mismo en desaparecer.",
        ],
    },
    {
        "id": "deriva",
        "frases": [
            "Cuando nos alcanza, la Tierra, sin nada que la sujete, sale disparada en línea recta a treinta kilómetros por segundo.",
            "Y aquí abajo, el cielo se vuelve negro.",
        ],
    },
    {
        "id": "frio",
        "frases": [
            "En una semana, la temperatura cae por debajo de dieciocho grados bajo cero.",
            "En un año, a setenta y tres bajo cero.",
            "Sin luz no hay fotosíntesis, y los océanos se congelan desde arriba.",
        ],
    },
    {
        "id": "vida",
        "frases": [
            "Pero ese hielo funciona como una manta, y el agua de abajo sigue líquida.",
            "Y en el fondo del mar, junto a fuentes hidrotermales, algunos microbios seguirían vivos.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Por suerte, al Sol le quedan unos cinco mil millones de años.",
            "Así que mañana, cuando salga, dale las gracias.",
        ],
    },
]
