# -*- coding: utf-8 -*-
"""Genera youtube.json (título, descripción con capítulos reales del timeline, fuentes, créditos, etiquetas) a partir de timeline.json."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
CAP = {
    "gancho": "Portland, 1981", "leyenda": "La leyenda: pesadillas y hombres de traje", "casos": "Lo que sí pasó en 1981",
    "gobierno": "El ejército, Atari y el hombre señalado", "pruebas": "¿Dónde está la máquina?", "origen": "El verdadero origen: año 2000",
    "porque": "Por qué nos la creímos", "cierre": "La pregunta que queda",
}


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


caps = "\n".join(f"{mmss(0 if i == 0 else e['t0'])} {CAP.get(e['id'], e['id'])}" for i, e in enumerate(TL["escenas"]))
cr = json.load(open(os.path.join(AQUI, "imagenes", "creditos.json"), encoding="utf-8"))
USADAS = ["portland_estacion", "asteroids", "tempest_logo", "battlezone_cab", "bradley1", "polibio_busto", "polibio_1548"]
fotos = []
for k in USADAS:
    for n, v in cr.items():
        if n.lower().startswith(k + "."):
            autor = v["autor"].split(chr(10))[0][:50].replace("Unknown authorUnknown author", "autor desconocido")
            fotos.append(f"{autor} ({v['licencia']})")
desc = f"""Portland, Oregón, 1981. Cuenta la leyenda que en unos pocos salones recreativos apareció una máquina negra llamada Polybius: provocaba pesadillas y amnesia, unos hombres de traje recogían sus datos cada noche… y un día desapareció sin dejar un solo tornillo. Este es el tablero completo del caso: qué pasó de verdad en 1981, qué tiene que ver el ejército con Atari, por qué nadie ha encontrado nunca la máquina y cuándo aparece realmente la historia por primera vez.

⏱️ CAPÍTULOS
{caps}

📚 FUENTES
• Polybius (leyenda urbana): https://en.wikipedia.org/wiki/Polybius_(urban_legend)
• Bradley Trainer (la versión militar del juego de tanques de Atari): https://en.wikipedia.org/wiki/Bradley_Trainer
• Polibio, historiador griego: https://es.wikipedia.org/wiki/Polibio
• Investigación del escéptico Brian Dunning (Skeptoid) y artículo de Inverse sobre el origen de la leyenda, citados en la entrada de Wikipedia
• Prensa de Oregón de 1981 sobre los jugadores enfermos y las redadas por apuestas, citada en la entrada de Wikipedia

ℹ️ No existe ninguna foto, programa ni registro de una máquina Polybius de 1981, y en este video no se muestra ninguna. Las pantallas de juego, la página web del año 2000, los periódicos y la revista que aparecen son recreaciones dibujadas, no documentos reales. Las personas sin foto con licencia libre aparecen como silueta.

📷 Fotos (Wikimedia Commons): {"; ".join(fotos)}. Mapa: Natural Earth (dominio público). Animaciones y gráficos: producción propia. Música: Lyria. Narración con voz sintética.

¿Tú crees que existió? Te leo en los comentarios 👇

#Polybius #Misterio #Videojuegos"""
datos = {
    "titulo": "Polybius: el videojuego que nunca existió",
    "titulos_alternativos": ["Polybius: la máquina arcade que «borraba la memoria»", "El videojuego maldito de 1981 que nadie ha encontrado"],
    "descripcion": desc,
    "etiquetas": ["polybius", "polybius videojuego", "polybius leyenda", "videojuego maldito", "leyenda urbana videojuegos", "arcade 1981", "portland oregon",
                  "misterios de internet", "creepypasta", "misterio", "documental", "atari", "battlezone", "tempest", "sinnesloschen", "hombres de negro",
                  "leyendas urbanas", "videojuegos retro", "misterios sin resolver", "historia de los videojuegos", "maquinas recreativas"],
    "categoria": 27,
    "idioma": "es", "idioma_audio": "es", "para_ninos": False,
    "miniatura": "salida/miniatura.jpg",
    "subtitulos": "salida/polybius.srt",
}
json.dump(datos, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("youtube.json listo; etiquetas:", sum(len(e) + 1 for e in datos["etiquetas"]), "caracteres; título", len(datos["titulo"]), "; descripción", len(desc))
print(caps)
