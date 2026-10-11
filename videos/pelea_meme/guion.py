# -*- coding: utf-8 -*-
"""UN HOMBRE CONTRA CINCO CRIATURAS — video meme de ~1 min, estilo `guache` (ilustración de libro infantil
en gouache: paleta apagada, sin contornos, grano de papel). Pelea por rondas, una criatura por escenario,
con un arma distinta cada vez. PLANO SECUENCIA: la cámara camina por un mundo continuo (desierto -> selva ->
océano -> Luna -> volcán) sin cortes; cada escena del guion es una ronda.

Es humor: no hay datos que verificar. Recurso repetido (gag): la chancla del primer round vuelve al final.
"""

TITULO = "Un hombre contra cinco criaturas"
ARCHIVO = "hombre_vs_criaturas"
ESTILO_VISUAL = "guache"
DURACION = None
BPM = 112
GAP = 0.28
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.85, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-23.0, sfx=-23.5)
TRANSICIONES = [("continua", 0.1)] * 6
MUSICA = {
    "intro": dict(sabor="brillo"),
    "r1": dict(sabor="funk"),
    "r2": dict(sabor="acid"),
    "r3": dict(sabor="dub"),
    "r4": dict(sabor="reloj"),
    "r5": dict(sabor="epico"),
    "cierre": dict(sabor="final"),
}

ESCENAS = [
    {"id": "intro", "pre": 0.15, "frases": [
        "Un hombre normal. Cinco criaturas. Una por una.",
    ]},
    {"id": "r1", "frases": [
        "Ronda uno. El desierto.",
        "Un escorpión gigante.",
        "El hombre saca su arma secreta: la chancla.",
        "Chanclazo. Nocaut.",
    ]},
    {"id": "r2", "frases": [
        "Ronda dos. La selva.",
        "Un tiranosaurio, con sus bracitos ridículos.",
        "El hombre responde con una sartén.",
        "Sartenazo directo. Nocaut.",
    ]},
    {"id": "r3", "frases": [
        "Ronda tres. El océano.",
        "Un tiburón gigante.",
        "Él contraataca con un pez espada.",
        "Duelo de espadas. Nocaut.",
    ]},
    {"id": "r4", "frases": [
        "Ronda cuatro. La Luna.",
        "Un extraterrestre, en su platillo volador.",
        "Solo tiene un extintor, y lo usa de cohete.",
        "Adiós, alienígena. Nocaut.",
    ]},
    {"id": "r5", "frases": [
        "Ronda cinco. El volcán.",
        "Un dragón que escupe fuego.",
        "Se cubre con una tapa de olla.",
        "Y entonces, la chancla regresa. Nocaut final.",
    ]},
    {"id": "cierre", "post": 1.2, "frases": [
        "Marcador final: hombre, cinco. Criaturas, cero.",
        "Nunca subestimes a una chancla.",
    ]},
]
