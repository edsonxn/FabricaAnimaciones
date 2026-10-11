# -*- coding: utf-8 -*-
"""GUION de «La Tierra hace cien mil años: Cuando no estábamos solos».
Motor SECUENCIA (Google Flow) en estilo ilustración dibujada (tinta negra, color plano, fondo completo).
Estilo: Secuencia Flow (mismo estilo visual que Wild Next Door).
Video sin canal, 3 minutos (~460 palabras), voz Dan (Chatterbox en español).
"""

TITULO = "La Tierra hace cien mil años: Cuando no estábamos solos"
ARCHIVO = "humanidad_100k"
MOTOR = "secuencia"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 96
GAP = 0.26
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(
    video_s=0,              # 100% ilustraciones fijas con cámara dirigida (ahorra puntos de Flow)
    clip_s=8,
    video_calidad="360p",
    combinar=False,
    img_s=4.0,              # ritmo dinámico de ~15 imágenes por minuto
    rapido_hasta=300,
    img_s_lento=5.0,
    fundido=0.2,            # fundido suave entre beats
    ambiente=0.5,
    ambiente_por={},
    carpeta_descargas="flow-humanidad_100k",
)

# Ficha visual del episodio (triple anclaje en inglés para Google Flow, estilo Wild Next Door)
FICHA = dict(
    estilo="Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, "
           "simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, "
           "sixteen by nine horizontal",
    personajes={
        "sapiens": "a simple expressive cartoon early Homo sapiens with tanned skin, dark messy hair, wearing brown leather and fur wraps, big round curious eyes, bold black outlines",
        "neanderthal": "a stocky cartoon Neanderthal with a heavy brow ridge, thick beard, warm fur cloak, holding a wooden spear, friendly and expressive round eyes",
        "denisovan": "a tall cartoon Denisovan hunter with braided dark hair, wearing thick animal pelts and polished bone beads",
        "child": "a small cute cartoon prehistoric human child with wide innocent eyes, playing with small smooth river stones",
    },
    objeto="a flint-tipped wooden hunting spear tied with plant fibers and resin, and glowing campfires",
    epoca="Pleistocene ice age savanna and cold European forests, mammoth bones, starry night skies, rocky limestone shelters",
    cierre="No text, no letters, no words, no logos, no watermark.",
)

TRANSICIONES = [("continua", 0.1)] * 20
MUSICA = {
    "gancho": dict(sabor="tension"),
    "otras_especies": dict(sabor="espacio"),
    "vida_diaria": dict(sabor="esperanza"),
    "mente_igual": dict(sabor="espacio"),
    "fragilidad": dict(sabor="tension"),
    "cierre": dict(sabor="esperanza"),
}

ESCENAS = [
    {"id": "gancho", "pre": 0.4, "frases": [
        "Si sales a la calle y miras a cualquier persona, sabes que todos pertenecemos a la misma especie.",
        "Pero si viajaras cien mil años al pasado, descubrirías un planeta irreconocible.",
        "En esa época, los humanos modernos no éramos los únicos dueños de la Tierra.",
        "No estábamos solos.",
    ]},
    {"id": "otras_especies", "frases": [
        "Hace cien mil años, al menos cinco especies humanas distintas caminaban por el mundo al mismo tiempo.",
        "En el calor de África vivían nuestros ancestros directos, los Homo sapiens.",
        "Mientras tanto, en los valles helados de Europa, los neandertales cazaban renos con lanzas pesadas.",
        "Eran fuertes, robustos y estaban perfectamente adaptados al frío glacial.",
        "Más hacia el oriente, en las montañas de Siberia, habitaban los misteriosos denisovanos.",
        "Y en las selvas de una isla remota de Indonesia, vivía una especie diminuta de menos de un metro de altura.",
    ]},
    {"id": "vida_diaria", "frases": [
        "Durante mucho tiempo nos dijeron que eran seres primitivos que solo sabían gruñir en cuevas oscuras.",
        "La ciencia moderna ha demostrado que eso era una completa mentira.",
        "Aquellos humanos vivían en pequeños clanes familiares de unas veinte o treinta personas.",
        "Dominaban el fuego a la perfección y cocinaban carne fresca sobre brasas ardientes.",
        "Fabricaban herramientas afiladas atando puntas de piedra a madera con resina de árbol.",
        "Molían minerales de color rojo brillante para pintar sus cuerpos y decorar pieles de animales.",
        "Y perforaban conchas marinas con una paciencia infinita para fabricar los primeros collares del mundo.",
    ]},
    {"id": "mente_igual", "frases": [
        "Hay un detalle asombroso que solemos olvidar.",
        "Biológicamente, aquellos humanos eran idénticos a nosotros.",
        "Tenían exactamente la misma capacidad cerebral, la misma curiosidad y los mismos miedos.",
        "Si trajeras al presente a un recién nacido de hace cien mil años, crecería sin ninguna diferencia.",
        "Aprendería a hablar cualquier idioma moderno, usaría un teléfono móvil y podría estudiar ingeniería.",
        "Sentían amor, despedían a sus muertos con flores y contaban leyendas bajo cielos repletos de estrellas.",
    ]},
    {"id": "fragilidad", "frases": [
        "Pero su supervivencia pendía de un hilo constante.",
        "Eran pocos, apenas unos miles de individuos dispersos por inmensos paisajes vírgenes.",
        "A su alrededor merodeaban hienas gigantes, felinos con colmillos de sable y mamuts colosales.",
        "Una simple herida o un invierno demasiado duro podía significar el final de todo un grupo.",
    ]},
    {"id": "cierre", "frases": [
        "Con el paso de los milenios, todas las demás especies humanas fueron desapareciendo una a una.",
        "Solo nosotros logramos cruzar los continentes y poblar cada rincón del globo.",
        "Sin embargo, aquellos otros humanos no se borraron del todo.",
        "Parte de su código genético todavía late en nuestra propia sangre.",
        "Hace cien mil años compartimos el fuego con ellos, y en nuestro interior, su historia sigue viva.",
    ]},
]
