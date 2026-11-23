# -*- coding: utf-8 -*-
"""Hoja de PROMESAS VISUALES de cod_mandela_zombies (regla 5-nov-2026): un cuadro del clip de cada beat que tiene que enseñar lo que
dice la voz -> previews/promesas_01.jpg (la tabla de promesas.md lleva el mismo número). python _promesas.py"""
import json
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
P = [  # (beat, segundo dentro del clip, rótulo)
    ("scene-007", 4, "1 intro Five B/N"), ("scene-009", 3, "2 Nixon se desmaya"), ("scene-010", 4, "3 salen armados"),
    ("scene-013", 4, "4 Nikolai final"), ("scene-019", 4, "5 The Defector Hue"), ("scene-022", 4, "6 Verruckt"),
    ("scene-027", 4, "7 Speed Cola / banco"), ("scene-033", 4, "8 Quick Revive"), ("scene-036", 4, "9 Type 100 pared"),
    ("scene-039", 4, "10 escudo Origins"), ("scene-043", 4, "11 Thundergun Kino"), ("scene-048", 4, "12 maquinas perks"),
    ("scene-055", 3, "13 Juggernog"), ("scene-060", 4, "14 Moon color"), ("scene-058", 4, "15 Ascension gris"),
    ("scene-064", 2, "16 intro Nacht"), ("scene-066", 4, "17 Hard Landing"), ("scene-069", 4, "18 mision Rebirth"),
    ("scene-070", 3, "19 silla del menu"), ("scene-071", 4, "20 Zombie Royale"), ("scene-075", 3, "21 Tombstone Town"),
    ("scene-080", 4, "22 Blundergat"), ("scene-082", 4, "23 Electric Cherry"), ("scene-085", 4, "24 caido BO2"),
    ("scene-089", 3, "25 gas Nova 6"), ("scene-091", 4, "26 Thundergun campana"), ("scene-095", 4, "27 puente TranZit"),
    ("scene-100", 4, "28 charcos / estatuas"), ("scene-101", 3, "29 Ray Gun en la playa"), ("scene-018", 4, "30 Defector fuego"),
    ("scene-024", 4, "31 zombis rapidos"), ("scene-103", 3, "32 Ray Gun mano"),
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
