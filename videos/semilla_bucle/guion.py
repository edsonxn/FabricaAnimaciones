# -*- coding: utf-8 -*-
"""El viaje de una semilla (estilo `boceto`: cada trazo y relleno se dibuja cuadro a cuadro).
Formato VERTICAL (1080x1920), ~42 s, ANIMACIÓN EN BUCLE: el último cuadro es idéntico al primero
(el pompón de diente de león con la semilla despegando) y la última frase enlaza directamente con la primera.

Ciclo del diente de león (Taraxacum officinale):
  - El vilano (pappus) actúa como un paracaídas aerodinámico con vórtice anular que le permite viajar kilómetros.
  - La semilla puede caer en cualquier grieta y resistir el invierno bajo tierra.
  - Al llegar la primavera, germina con raíces pivotantes fuertes y florece en una flor amarilla radiante.
  - Al madurar, la flor se transforma en una esfera de semillas listas para dispersarse con el viento.
"""

TITULO = "El viaje de una semilla"
ARCHIVO = "viaje_de_una_semilla"
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = None
BPM = 100
GAP = 0.25
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.7, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-24.0)
TRANSICIONES = [("continua", 0.1)] * 7

MUSICA = {
    "vuelo": dict(sabor="esperanza", raiz=43),
    "viento": dict(sabor="lounge", raiz=41),
    "tormenta": dict(sabor="ambiente", raiz=40),
    "grieta": dict(sabor="ambiente", raiz=40),
    "brote": dict(sabor="esperanza", raiz=43),
    "flor": dict(sabor="brillo", raiz=45),
    "morfosis": dict(sabor="lounge", raiz=41),
    "cierre": dict(sabor="esperanza", raiz=43),
}

ESCENAS = [
    {"id": "vuelo", "pre": 1.2, "frases": [
        "Esta pequeña semilla está lista para recorrer el mundo.",
        "Solo necesita que sople un poco de viento.",
    ]},
    {"id": "viento", "frases": [
        "Es capaz de subir cientos de metros y flotar durante días enteros.",
    ]},
    {"id": "tormenta", "frases": [
        "Pero una sola gota de lluvia puede cambiarlo todo.",
    ]},
    {"id": "grieta", "frases": [
        "Aterriza en una diminuta grieta, fría y olvidada.",
    ]},
    {"id": "brote", "frases": [
        "Hasta que el calor de la primavera despierta sus raíces.",
    ]},
    {"id": "flor", "frases": [
        "De la piedra nace un brillante sol amarillo.",
    ]},
    {"id": "morfosis", "frases": [
        "Con el paso del tiempo, el amarillo se vuelve nieve.",
    ]},
    {"id": "cierre", "post": 1.4, "frases": [
        "Cientos de hermanas esperan pacientes su turno.",
        "Y con la siguiente brisa...",
    ]},
]
