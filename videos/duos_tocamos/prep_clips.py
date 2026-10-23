# -*- coding: utf-8 -*-
"""Los 4 videos de celular del grupo, ENTEROS, a clips/v1..v4.mp4 (1080x1920, 30 fps, sin audio): escala lanczos (cubre y
recorta), reducción de ruido, nitidez suave y color un poco más cálido (mismo filtro que videos/duos_promo/prep_clips.py).
Las tomas se eligen en escenas.TOMAS por (video, segundo).
V1 salón con globos (bailes; teclado PSR de cerca 11-15) · V2 salón grande con mesas (manos arriba 61-69)
V3 terraza de columnas amarillas (familia a la mesa 0-4; tecladista cantando 31-39) · V4 patio de noche (señoras bailando)"""
import os
import subprocess

MAT = r"E:\FabricaAnimaciones\videos\duos_promo\material"
V = {1: "WhatsApp Video 2026-10-22 at 10.45.14 AM.mp4", 2: "WhatsApp Video 2026-10-22 at 10.45.15 AM.mp4",
     3: "WhatsApp Video 2026-10-22 at 10.45.16 AM.mp4", 4: "WhatsApp Video 2026-10-22 at 10.45.17 AM.mp4"}
FILTRO = ("scale=1080:1920:force_original_aspect_ratio=increase:flags=lanczos,crop=1080:1920,fps=30,"
          "hqdn3d=3:3:6:6,unsharp=7:7:0.55:5:5:0,eq=contrast=1.07:saturation=1.14:gamma=1.02,"
          "colorbalance=rs=0.03:gs=0.0:bs=-0.04:rm=0.02:bm=-0.03,format=yuv420p")

os.makedirs("clips", exist_ok=True)
for n, f in V.items():
    out = os.path.join("clips", f"v{n}.mp4")
    if os.path.exists(out):
        continue
    subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-i", os.path.join(MAT, f), "-an", "-vf", FILTRO,
                    "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-g", "15", out], check=True)
    print("ok", out)
