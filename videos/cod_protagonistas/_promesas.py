# -*- coding: utf-8 -*-
"""Hoja de PROMESAS VISUALES de cod_protagonistas (regla 5-nov-2026): un cuadro del clip de cada beat que tiene que enseñar lo que
dice la voz -> previews/promesas_01.jpg (la tabla de promesas.md lleva el mismo número). python _promesas.py"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
P = [  # (beat, segundo dentro del clip, rótulo) — cod_protagonistas 24-nov-2026
    ("scene-009", 4, "1 Reyes visor"), ("scene-013", 4, "2 Rorke se lleva a Logan"), ("scene-014", 2, "3 Logan en el pozo"),
    ("scene-017", 5, "4 Alex entra al horno"), ("scene-021", 6, "5 Jackson ruinas y hongo"), ("scene-025", 5, "6 Al-Fulani en el coche"),
    ("scene-027", 3, "7 Victor copiloto"), ("scene-032", 7, "8 Allen ambulancia"), ("scene-037", 4, "9 Yuri atravesado"),
    ("scene-038", 3, "10 Yuri dispara"), ("scene-040", 4, "11 helicoptero al mar"), ("scene-044", 4, "12 tumba de Mason"),
    ("scene-049", 4, "13 Ghost arrastra a Roach"), ("scene-050", 2, "14 Shepherd cita"), ("scene-059", 4, "15 Reznov tren"),
    ("scene-065", 4, "16 Soap en la mesa"), ("scene-067", 5, "17 M1911 en el pecho"), ("scene-070", 3, "18 Woods ventana"),
    ("scene-075", 5, "19 Adler acantilado"), ("scene-080", 5, "20 bolsa y Mason"), ("scene-084", 3, "21 cirugia BO3"),
    ("scene-087", 4, "22 final B/N Taylor"), ("scene-090", 6, "23 atados a sillas"), ("scene-092", 6, "24 entra el Archer"),
    ("scene-097", 3, "25 Soap y la bomba"), ("scene-099", 2, "26 cenizas Escocia"), ("scene-103", 3, "27 lago helado"),
    ("scene-106", 3, "28 Ghost le toma la mano"), ("scene-107", 3, "29 Laswell borra"), ("scene-110", 3, "30 Price WWII Tirpitz"),
    ("scene-102", 4, "31 convoy Price"), ("scene-021", 2, "32 helicoptero nuke"),
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
                    "".join(f"[{k}]" for k in range(n)) + f"xstack=inputs={n}:grid=8x4", os.path.join(AQUI, "previews", "promesas_01.jpg")],
                   check=True)
    print("previews/promesas_01.jpg", n)
