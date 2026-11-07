# -*- coding: utf-8 -*-
"""GUION de un video del motor SECUENCIA (clips e imágenes de Google Flow, uno por beat de la narración).
Se crea con:  python fab.py nuevo <nombre> --secuencia      Flujo y reglas: docs/estilo_secuencia_flow.md

Reglas de la voz (Chatterbox): frases cortas (< ~200 caracteres); números, años y siglos SIEMPRE en letras
("mil novecientos cuarenta y cinco", "siglo diecinueve"); nada de siglas que se lean mal.
Ritmo: en la zona de imagen cada ~11-13 palabras deben traer algo ilustrable (sujeto, acción o detalle nuevo).
ESCENAS = bloques narrativos (gancho, promesa, escalada..., cierre). Aquí NO se describen imágenes: los cortes
visuales salen de `beats` (pausas reales de la voz) y los prompts van en prompts.json.
"""

TITULO = "Título del video"
# ARCHIVO = "nombre_base_de_salida"
MOTOR = "secuencia"
# FORMATO = "vertical"   # reel 9:16 (1080x1920): pedir 9:16 a Flow y cambiar la FICHA; ver docs/estilo_secuencia_flow.md
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=120,        # segundos iniciales cubiertos con VIDEO de Flow (0 = todo imagen); el usuario suele pedir 60-120
    clip_s=8,           # duración de cada clip de Flow (4, 6, 8 o 10)
    video_calidad="360p",   # 360p gasta menos puntos; se baja con «720p · Resolución mejorada» (gratis)
    combinar=False,     # True (con clip_s=10): cada clip une DOS escenas del guion con una transición dibujada
    img_s=4.0,          # s por imagen hasta `rapido_hasta` (15 imágenes por minuto)
    rapido_hasta=300,   # después de este segundo el ritmo baja a `img_s_lento`
    img_s_lento=6.0,    # 10 imágenes por minuto
    fundido=0.2,        # fundido entre beats (0 = corte seco)
    ambiente=0.5,       # volumen del sonido propio de los clips de Flow bajo la voz (0 = mudo)
    ambiente_por={},    # por clip: {"scene-004": 0.0} calla uno que suene mal
    # carpeta_descargas="flow-<video>",   # subcarpeta de Descargas donde Flow deja scene-XXX.*
)

# Ficha visual del episodio: se repite PALABRA POR PALABRA en cada prompt donde aparezca (triple anclaje).
FICHA = dict(
    estilo="Diorama cinematográfico horizontal dieciséis nueve hecho íntegramente de plastilina artesanal stop-motion, "
           "textura mate con huellas de dedos visibles",
    personajes={
        # "nombre": "descripción física y de vestuario fija (edad, pelo, ropa, colores)",
    },
    objeto="",          # objeto estrella: descripción técnica exacta + exclusiones ("sin caballos, sin vapor")
    epoca="",           # lugar, año y materiales de la época; lo que NO debe aparecer
    cierre="Sin texto, sin letras, sin logotipos, sin objetos modernos.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    # "gancho": dict(sabor="tension"), "cierre": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.5, "frases": [
        "Primera frase: una contradicción o un riesgo visible en menos de veinte segundos.",
    ]},
    {"id": "cierre", "frases": [
        "Cierre circular: vuelve a la imagen del gancho.",
    ]},
]
