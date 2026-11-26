# -*- coding: utf-8 -*-
"""Ventanas del ORIGINAL (N64) para las comparativas de oot_remake_anadido (6-nov-2026; receta de oot_remake_cambios):
baja un tramo de cada fuente, le quita el marco/barras y lo deja en medios/n64/<slug>.mp4 a 640 px de ancho, 30 fps, sin audio.
efectos.py las pone con FX `video` (ancho) + marco encima, mientras el cuadro grande muestra el remake.
    python bajar_ventanas.py
Rutas relativas a ESTA carpeta (medios/n64/); no toca otros videos.
"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "medios", "n64")
NSO = 0.131   # marco gris de Switch Online (serie ZeldaCentral)

# slug: (id de YouTube, segundo, largo, recorte (izq, arriba, der, abajo) en fraccion, beats donde se compara con el remake)
VENTANAS = {   # 11-nov, oot_remake_anadido
    "ocarina": ("MJxGJpBja_w", 800, 10, (NSO, 0, NSO, 0)),         # N64: Saria y la ocarina quieta en el puente -> p11/p10
    "zelda": ("FO9OG9QXGS4", 1188, 11, (NSO, 0, NSO, 0)),          # N64: Zelda da la Ocarina del Tiempo en el foso -> p10
    "pocion": ("csFvvR08QFY", 333, 10, (NSO, 0, NSO, 0)),          # N64: tienda de pociones -> p9
    "redead": ("XPvYWutj5ag", 26, 10, (0.08, 0.06, 0.08, 0.06)),   # N64: ReDead -> p7
    "espada": ("M--gXMSdJxY", 640, 11, (NSO, 0, NSO, 0)),          # N64: Espada Maestra y Ganondorf en texto -> p4
    "rauru": ("M--gXMSdJxY", 760, 11, (NSO, 0, NSO, 0)),           # N64: Cámara de los Sabios -> p3
    "mq": ("EFhB23Z1OWw", 160, 11, (0.125, 0, 0.125, 0)),          # GameCube: Master Quest -> p2
}


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (vid, s, largo, (i, a, d, ab)) in VENTANAS.items():
        dest = os.path.join(OUT, slug + ".mp4")
        if os.path.exists(dest):
            continue
        tmp = os.path.join(OUT, "_" + slug + ".mp4")
        subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=1080][height>=480][vcodec^=avc1]/bv*[height<=1080][height>=480]",
                        "--download-sections", f"*{s}-{s + largo + 2}", "-o", tmp, "--force-overwrites",
                        f"https://youtu.be/{vid}"], check=False)
        vf = f"crop=iw*{1 - i - d:.3f}:ih*{1 - a - ab:.3f}:iw*{i}:ih*{a},scale=640:-2,fps=30"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.5", "-i", tmp, "-t", str(largo), "-an", "-vf", vf,
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", dest], check=True)
        os.remove(tmp)
        print("ok", slug, flush=True)


if __name__ == "__main__":
    main()
