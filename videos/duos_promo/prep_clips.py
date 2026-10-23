# -*- coding: utf-8 -*-
"""Recorta los tramos elegidos de los 4 videos de celular del grupo y los deja en clips/<nombre>.mp4 a 1080x1920, 30 fps,
sin audio: escala lanczos (cubre y recorta), reducción de ruido, nitidez suave y color un poco más cálido y contrastado.
    python prep_clips.py            (rehace solo los que falten)      python prep_clips.py --todo
Videos: V1 salón con globos (bailes, tecladista con Yamaha PSR) · V2 salón grande con mesas (manos arriba al final)
        V3 terraza con columnas amarillas (tecladista de camisa oscura cantando, 31-39 s) · V4 patio de noche (señoras bailando)"""
import os
import subprocess
import sys

MAT = r"E:\FabricaAnimaciones\videos\duos_promo\material"
V = {1: "WhatsApp Video 2026-10-22 at 10.45.14 AM.mp4", 2: "WhatsApp Video 2026-10-22 at 10.45.15 AM.mp4",
     3: "WhatsApp Video 2026-10-22 at 10.45.16 AM.mp4", 4: "WhatsApp Video 2026-10-22 at 10.45.17 AM.mp4"}
# nombre: (video, desde, hasta)
CLIPS = {
    "baile_globos": (1, 39.5, 47.0),     # gancho: parejas bailando, señor de cuadros al centro
    "tecladista": (3, 30.0, 39.6),       # grupo: el tecladista canta con su Yamaha
    "teclado": (1, 11.0, 15.5),          # grupo: el teclado PSR de cerca
    "baile_a": (1, 0.0, 5.0),            # géneros
    "noche_a": (4, 21.0, 27.0),
    "baile_b": (1, 31.0, 37.0),
    "noche_b": (4, 45.0, 51.0),
    "baile_c": (1, 23.0, 29.5),
    "manos": (2, 61.0, 69.0),            # eventos: «fiestas», la gente con las manos arriba
    "mesas": (3, 0.0, 6.0),              # eventos: reunión familiar a la mesa (terraza de columnas amarillas)
    "salon": (2, 22.0, 30.0),            # eventos privados: salón grande
}
FILTRO = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
          "hqdn3d=3:3:6:6,unsharp=7:7:0.55:5:5:0,eq=contrast=1.07:saturation=1.14:gamma=1.02,"
          "colorbalance=rs=0.03:gs=0.0:bs=-0.04:rm=0.02:bm=-0.03,format=yuv420p")


def main():
    os.makedirs("clips", exist_ok=True)
    todo = "--todo" in sys.argv
    for nom, (v, a, b) in CLIPS.items():
        out = os.path.join("clips", nom + ".mp4")
        if os.path.exists(out) and not todo:
            continue
        cmd = [r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-ss", f"{a:.2f}", "-to", f"{b:.2f}",
               "-i", os.path.join(MAT, V[v]), "-an", "-vf", FILTRO, "-c:v", "libx264", "-crf", "16", "-preset", "medium",
               "-g", "15", out]
        subprocess.run(cmd, check=True)
        print("ok", nom, f"V{v} {a}-{b}")


if __name__ == "__main__":
    main()
