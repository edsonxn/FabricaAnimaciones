# -*- coding: utf-8 -*-
"""Ventanas del ORIGINAL (N64) para las comparativas de oot_remake_eliminado (6-nov-2026; receta de oot_remake_cambios):
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
VENTANAS = {
    "retratos": ("ON8HBpJiK_E", 21, 12, (0, 0, 0, 0)),            # pared con los 5 cuadros (480p basta para 640 px) -> scene-002 / 062
    "guardia": ("MaUCTYb1VtI", 28.5, 12, (0.125, 0, 0.125, 0)),   # «Hey you!» y la bomba que explota a ~35 s -> scene-062 / 064
    "puente": ("VgZgYI0DUCY", 4, 12, (0, 0, 0, 0)),               # Link trepa por la cadena y cae al centro -> scene-047
    "lupa": ("pm0S_b-nq-U", 250, 11, (0.125, 0, 0.125, 0)),       # cofre del Pozo y «Lens of Truth» -> scene-016
    "kaepora": ("MJxGJpBja_w", 946, 11, (NSO, 0, NSO, 0)),        # «Did you get all that? No / Yes» -> scene-020
    "archivo": ("N6rM3KhqHIo", 50, 9, (NSO, 0, NSO, 0)),          # «Please select a file» con 3 ranuras -> scene-037
    "hadas": ("m29XeXRn-2Y", 36, 11, (NSO, 0, NSO, 0)),           # Gran Hada: «Welcome Link!» -> scene-032 / 033
    "ganon": ("pMzN9Y5LnW4", 26.8, 10, (0, 0.14, 0, 0.14)),       # v1.0: sangre roja -> scene-057 / 058
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
