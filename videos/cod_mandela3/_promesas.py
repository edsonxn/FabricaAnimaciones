# -*- coding: utf-8 -*-
"""Hoja de PROMESAS VISUALES de cod_mandela3 (regla 5-nov-2026): un cuadro del clip de cada beat que tiene que enseñar lo que
dice la voz -> previews/promesas_01.jpg (la tabla de promesas.md lleva el mismo número). python _promesas.py"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
P = [  # (beat, segundo dentro del clip, rótulo)
    ("scene-010", 4, "1 intro MW2 Gaz"), ("scene-012", 4, "2 lata Max Ammo"), ("scene-016", 4, "3 CoD 4 multijugador"),
    ("scene-021", 4, "4 menu BO1 cristal"), ("scene-028", 4, "5 granja TranZit"), ("scene-031", 4, "6 carne / Grief"),
    ("scene-035", 4, "7 Extinction aliens"), ("scene-039", 4, "8 Reznov Stalingrado"), ("scene-041", 4, "9 Reznov Alemania"),
    ("scene-045", 4, "10 OITC pistola"), ("scene-048", 4, "11 Ghost MW2"), ("scene-052", 4, "12 Price CoD 1"),
    ("scene-054", 4, "13 Tirpitz"), ("scene-057", 4, "14 Piccadilly"), ("scene-062", 4, "15 Nacht"), ("scene-066", 3, "16 menu CoD 4"),
    ("scene-068", 2, "17 mision Pripiat"), ("scene-073", 4, "18 Outbreak Golova"), ("scene-076", 4, "19 Ray Gun II"),
    ("scene-080", 9, "20 ascensor No Russian"), ("scene-083", 2, "21 doblaje japones"), ("scene-088", 3, "22 Jackson original"),
    ("scene-089", 5, "23 Jackson remaster"), ("scene-092", 4, "24 Nuketown maniqui"), ("scene-095", 4, "25 Alpha Omega"),
    ("scene-102", 4, "26 Menendez celda"), ("scene-103", 3, "27 linea de tiempo"), ("scene-105", 4, "28 Black Ops 7"),
]
if __name__ == "__main__":
    tmp = os.path.join(AQUI, "previews", "_prom")
    os.makedirs(tmp, exist_ok=True)
    fs = []
    for i, (b, s, r) in enumerate(P):
        out = os.path.join(tmp, f"{i:02d}.jpg")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(s), "-i", os.path.join(AQUI, "medios", b + ".mp4"), "-frames:v", "1",
                        "-vf", f"scale=384:216,drawbox=y=186:w=384:h=30:color=black@0.7:t=fill,"
                               f"drawtext=text='{b[-3:]} {r}':x=6:y=192:fontsize=18:fontcolor=white", out], check=True)
        fs.append(out)
    args = sum([["-i", f] for f in fs], [])
    n = len(fs)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex",
                    "".join(f"[{k}]" for k in range(n)) + f"xstack=inputs={n}:grid=7x4", os.path.join(AQUI, "previews", "promesas_01.jpg")],
                   check=True)
    print("previews/promesas_01.jpg", n)
