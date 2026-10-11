# -*- coding: utf-8 -*-
"""La Conspiración y el Grito de Dolores — ~2 minutos, estándar Kurzgesagt ISOMÉTRICO (Bitácora Perdida).
Recreación fidedigna de alta densidad visual con el motor de 'independencia_mx':
  - Interior en corte de la tertulia secreta (casa colonial, chimenea, candelabros, conspiradores).
  - Mapa con relieve topográfico real (ETOPO1/Natural Earth) con ciudades y rutas de mensajeros.
  - Diorama isométrico de la calle de Querétaro con acueducto y mensajero a caballo.
  - Diorama isométrico del pueblo de Dolores al amanecer: isla flotante en el cielo con nubes,
    iglesia de cantera de dos torres, campana repicando con ondas sonoras doradas y multitud en la plaza.
  - Retratos expresivos en medallón con iluminación de borde (Josefa Ortiz, Ignacio Allende, Miguel Hidalgo).
  - Cápsulas de UI flotantes de fecha y lugar.
"""

TITULO = "La Conspiración y el Grito de Dolores"
ARCHIVO = "conspiracion_grito_dolores"
ESTILO_VISUAL = "kurzgesagt"
DURACION = None
BPM = 96
GAP = 0.65
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-22.5)
SUBTITULOS = False

TRANSICIONES = [("continua", 0.1)] * 4

MUSICA = {
    "intro": dict(sabor="vacio", raiz=38),
    "conspiracion": dict(sabor="tension", raiz=36),
    "correo": dict(sabor="tension", raiz=40),
    "dolores": dict(sabor="esperanza", raiz=41),
    "cierre": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "En septiembre de mil ochocientos diez, la Nueva España vivía bajo una aparente calma.",
            "Pero en el corazón del Bajío, un grupo secreto preparaba una rebelión histórica.",
        ],
    },
    {
        "id": "conspiracion",
        "frases": [
            "En Querétaro, bajo la apariencia de simples tertulias literarias, criollos y militares conspiraban en secreto.",
            "Doña Josefa Ortiz de Domínguez e Ignacio Allende planeaban levantarse en armas contra el virreinato.",
            "Pero una delación lo cambió todo: las autoridades descubrieron las reuniones y ordenaron arrestarlos de inmediato.",
        ],
    },
    {
        "id": "correo",
        "frases": [
            "Desde su encierro, Josefa logró avisar a tiempo, y un mensajero partió a galope tendido en medio de la noche.",
            "Cabalgaron sin descanso por caminos oscuros para advertir a los líderes antes de que los soldados reales los capturaran.",
        ],
    },
    {
        "id": "dolores",
        "frases": [
            "Al amanecer del dieciséis de septiembre, la noticia llegó al pueblo de Dolores.",
            "El cura Miguel Hidalgo tomó una decisión irreversible: hacer sonar la campana de la parroquia.",
            "El repique congregó a campesinos y artesanos en la plaza, iniciando una lucha que cambiaría el destino de la nación.",
        ],
    },
    {
        "id": "cierre",
        "frases": [
            "Esa madrugada nació un movimiento imparable.",
            "Una chispa que encendió la libertad de todo un continente.",
        ],
    },
]
