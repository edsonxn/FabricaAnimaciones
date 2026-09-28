# -*- coding: utf-8 -*-
"""GUION de un video nuevo. Copia esta carpeta con:  python fab.py nuevo <nombre>

Reglas para que la voz (Chatterbox) salga bien:
  - Frases cortas (< ~200 caracteres). Números ESCRITOS EN PALABRAS ("cuarenta mil", no "40.000").
  - Evitar siglas que se lean mal (p. ej. "ADN" sonó "Adán"): reescribir la frase.
Estructura:
  - Primera escena = intro, última = cierre (reciben música/márgenes especiales).
  - Escena de ítem (lista numerada): "num", "titulo" y EXACTAMENTE 3 frases:
      frase 0 = "Número <n>: <título>"   (el título en pantalla = lo narrado tras las 2 primeras palabras)
      frase 1 = fase A (contexto / antes)      frase 2 = fase B (remate / hoy)
  - Escenas sin "num" = escenas libres (cualquier cantidad de frases).
Campos visuales opcionales por escena (los usan las escenas genéricas):
  icono / icono_hoy  -> nombre del catálogo ICONOS (ver API.md)
  claves             -> [[palabra_ancla, "ETIQUETA"], ...]: la etiqueta aparece cuando se dice la palabra
  dato, fuente       -> tarjeta con el dato y su fuente (fase A)
  sello / sello_hoy  -> sello de esquina en fase A / B (None = sin sello)
  etiqueta_numero    -> texto sobre el número grande (por defecto "NÚMERO")
  cierre             -> texto de la tarjeta final (última escena)
  pre / post         -> segundos de margen antes/después de la voz de esa escena
"""

TITULO = "Dos cosas que tu cerebro hace sin avisarte"
# ARCHIVO = "cerebro_sin_avisar"   # nombre base de los archivos de salida (opcional)
ESTILO_VISUAL = "pizarra"        # doodle_psicodelico | pizarra | cuaderno | neon | recortes | limpio
DURACION = None                  # None = duración natural; o segundos exactos (p. ej. 180.0)
BPM = 120                        # tempo si DURACION es None
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)
# Opcionales (si faltan se eligen solos):
# TRANSICIONES = [("garabato", 1.0), ("mancha", 0.8), ...]      una por cada cambio de escena
# MUSICA = {"intro": dict(sabor="build"), "uno": dict(sabor="funk", raiz=43), ...}

ESCENAS = [
    {
        "id": "intro",
        "frases": [
            "Tu cerebro hace cosas increíbles sin pedirte permiso.",
            "Aquí van dos que ocurren ahora mismo, mientras ves esto.",
        ],
        "claves": [["permiso", "SIN PERMISO"]],
    },
    {
        "id": "uno", "num": 1, "titulo": "PARPADEAR",
        "icono": "ojo", "icono_hoy": "cerebro",
        "dato": "Un adulto parpadea unas 15 a 20 veces por minuto",
        "fuente": "Volkmann, Riggs y Moore, 1980, Science",
        "sello": None,
        "claves": [["quince", "15–20 POR MINUTO"], ["borra", "¡BORRADO!"]],
        "frases": [
            "Número uno: parpadear.",
            "Parpadeas unas quince a veinte veces por minuto, y cada parpadeo te deja a oscuras un instante.",
            "Pero tu cerebro borra esos apagones, así que nunca los notas.",
        ],
    },
    {
        "id": "dos", "num": 2, "titulo": "RELLENAR EL PUNTO CIEGO",
        "icono": "ojo", "icono_hoy": "cerebro",
        "dato": "El punto ciego: donde el nervio óptico sale del ojo",
        "fuente": "Descrito por Edme Mariotte, siglo XVII",
        "sello": None,
        "claves": [["punto ciego", "PUNTO CIEGO"], ["rellena", "RELLENO AUTOMÁTICO"]],
        "frases": [
            "Número dos: rellenar el punto ciego.",
            "Cada ojo tiene un punto ciego, un lugar sin receptores de luz.",
            "Tu cerebro lo rellena con lo que hay alrededor, y tú nunca ves el hueco.",
        ],
    },
    {
        "id": "cierre",
        "cierre": "¿LO SABÍAS?",
        "frases": [
            "Así que no confíes tanto en lo que ves.",
            "Tu cerebro edita la realidad en vivo.",
        ],
    },
]
