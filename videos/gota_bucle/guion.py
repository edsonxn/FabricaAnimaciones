# -*- coding: utf-8 -*-
"""El viaje de una gota (prueba del estilo `boceto`: cada elemento se dibuja trazo a trazo, cuadro a cuadro).
Formato VERTICAL (1080x1920), ~1 min, ANIMACIÓN EN BUCLE: el último cuadro es igual al primero (nube + sol + gota)
y la última frase enlaza con la primera.

Datos (USGS, "Water Cycle"; NASA):
  - El agua de la Tierra es la misma desde hace miles de millones de años: casi no se pierde al espacio.
  - Tiempo medio de residencia: atmósfera ~9 días; ríos ~2 semanas a meses; glaciares ~20 a 100 años (décadas);
    océanos ~3.200 años.
"""

TITULO = "El viaje de una gota"
ARCHIVO = "viaje_de_una_gota"
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
    "nube": dict(sabor="lounge", raiz=41),
    "montana": dict(sabor="lounge", raiz=41),
    "hielo": dict(sabor="ambiente", raiz=40),
    "rio": dict(sabor="lounge", raiz=43),
    "vaso": dict(sabor="lounge", raiz=43),
    "mar": dict(sabor="ambiente", raiz=41),
    "sol": dict(sabor="esperanza", raiz=43),
    "cierre": dict(sabor="lounge", raiz=41),
}

ESCENAS = [
    {"id": "nube", "pre": 1.3, "frases": [
        "Esta gota de agua lleva miles de millones de años dando vueltas.",
        "Y nunca ha salido del planeta.",
    ]},
    {"id": "montana", "frases": [
        "Hoy cae como lluvia sobre una montaña.",
    ]},
    {"id": "hielo", "frases": [
        "Se congela, y puede esperar décadas dentro de un glaciar.",
    ]},
    {"id": "rio", "frases": [
        "Cuando se derrite, baja por un río, donde apenas se queda unos meses.",
    ]},
    {"id": "vaso", "frases": [
        "A veces termina en tu vaso, y luego en ti.",
        "Tú la devuelves, y sigue su camino.",
    ]},
    {"id": "mar", "frases": [
        "Al final llega al mar, donde puede quedarse unos tres mil años.",
    ]},
    {"id": "sol", "frases": [
        "Hasta que el Sol la calienta, y la levanta al cielo.",
    ]},
    {"id": "cierre", "post": 1.4, "frases": [
        "Arriba solo dura unos nueve días.",
        "Entonces, vuelve a empezar.",
    ]},
]
