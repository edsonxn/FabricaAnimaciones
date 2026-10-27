# -*- coding: utf-8 -*-
"""Ventanas del ORIGINAL de N64 para las comparativas (oot_remake_cambios, 26-oct-2026): baja un tramo de la serie
ZeldaCentral (Switch Online, 1080p) y lo deja en medios/n64/<slug>.mp4 sin el marco gris de NSO (4:3, 640 px, sin audio).
efectos.py las pone con FX `video` (ancho) + mg_oot.marco encima.
    python bajar_ventanas.py
"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQUI, "medios", "n64")
P = {1: "N6rM3KhqHIo", 2: "MJxGJpBja_w", 3: "BAnsTh2fHmU", 11: "FO9OG9QXGS4", 13: "M--gXMSdJxY", 24: "quu9fmNlsGk"}
VENTANAS = {   # slug: (parte, segundo, largo) — segundos de videos/zelda_oot/mapa_clips.md
    "kokiri": (1, 380, 9),       # aldea Kokiri
    "mercado3": (13, 494, 12),   # mercado de la Ciudadela y Templo del Tiempo: fondos prerrenderizados, cámaras fijas
    "mercado2": (13, 440, 14),   # mercado: callejón prerrenderizado con DIÁLOGO DE TEXTO (p5)
    "menu": (24, 840, 12),       # menú de equipo con las botas
    "rodar": (11, 30, 12),       # campo de Hyrule
    "salto": (2, 105, 12),       # dentro del Árbol Deku: saltos automáticos
}
NSO = 0.131


def main():
    os.makedirs(OUT, exist_ok=True)
    for slug, (parte, s, largo) in VENTANAS.items():
        dest = os.path.join(OUT, slug + ".mp4")
        if os.path.exists(dest):
            continue
        tmp = os.path.join(OUT, "_" + slug + ".mp4")
        subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=1080][height>=720][vcodec^=avc1]/bv*[height<=1080][height>=720]",
                        "--download-sections", f"*{s}-{s + largo + 2}", "-o", tmp, "--force-overwrites",
                        f"https://youtu.be/{P[parte]}"], check=False)
        vf = f"crop=iw*{1 - 2 * NSO:.3f}:ih:iw*{NSO}:0,scale=640:-2,fps=30"
        subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", "0.5", "-i", tmp, "-t", str(largo), "-an", "-vf", vf,
                        "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", dest], check=True)
        os.remove(tmp)
        print("ok", slug, flush=True)


if __name__ == "__main__":
    main()
