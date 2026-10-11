# -*- coding: utf-8 -*-
"""El Asalto Pirata: Batalla en el Fuerte del Caribe (1 minuto, Estilo Kurzgesagt Isométrico).

Demostración de alta energía cinética:
- Galeón en oleaje caribeño tridimensional animado.
- Cañones con retroceso, fogonazo, anillos de humo y ondas de choque.
- Combate cuerpo a cuerpo entre piratas y guardias con sables y mosquetes.
- Fuego, chispas volantes, humo denso, palmeras y cámara en vuelo dinámico continuo.
"""

TITULO = "El Asalto Pirata: Batalla en el Fuerte del Caribe"
ARCHIVO = "asalto_pirata_1min"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 116
GAP = 0.28
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.85, cfg_weight=0.35, temperature=0.75)
MEZCLA = dict(musica=-20.0, sfx=-20.0)

ALIAS_QA = {
    "1680": "mil seiscientos ochenta",
    "san felipe": "san felipe",
}

SUBTITULOS = False

TRANSICIONES = [("continua", 0.08)] * 4

MUSICA = {
    "acercamiento": dict(sabor="tension", raiz=45),
    "bombardeo": dict(sabor="epico", raiz=43),
    "combate": dict(sabor="epico", raiz=45),
    "fuga": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {
        "id": "acercamiento",
        "pre": 0.4,
        "frases": [
            "Año mil seiscientos ochenta. En las aguas turquesas del Mar Caribe, un galeón corsario navega a toda vela hacia la bahía colonial.",
            "Su objetivo: asaltar el bastión de San Felipe antes de que los centinelas puedan dar la alarma general.",
        ],
    },
    {
        "id": "bombardeo",
        "pre": 0.3,
        "frases": [
            "Fuego en las almenas. Las baterías de costa responden al instante con una atronadora descarga de artillería pesada.",
            "Las balas de cañón silban sobre las olas y abren una mortífera brecha en los muros exteriores del baluarte.",
        ],
    },
    {
        "id": "combate",
        "pre": 0.3,
        "frases": [
            "A golpe de sable y mosquete, la tripulación pirata desembarca en el muelle y toma el patio central en un feroz combate cuerpo a cuerpo.",
            "Entre humo y llamas de pólvora, los defensores retroceden mientras cae la puerta principal de la fortaleza.",
        ],
    },
    {
        "id": "fuga",
        "pre": 0.4,
        "frases": [
            "Con más de cincuenta mil doblones de oro en las bodegas, el navío vira a toda prisa rumbo a alta mar.",
            "Un asalto relámpago que convirtió esta costa caribeña en leyenda inmortal.",
        ],
    },
]
