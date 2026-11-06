# -*- coding: utf-8 -*-
"""Empalma tramos re-renderizados (salida/tramo_A_B.mp4 de `fab.py bt_jefes_ranking video --tramo A-B`) sobre el MASTER
(corrección del 6-nov-2026: pegatinas que no eran de lo que nombraba la voz; pegatinas_check.md). Corta por CUADROS (30 fps),
re-codifica el video una vez y copia el audio del MASTER tal cual.
    python empalmar_tramos.py 31-43 377-410 628-638 1062-1077 1408-1421
"""
import os
import subprocess
import sys

FPS = 30
AQUI = os.path.dirname(os.path.abspath(__file__))
M = os.path.join(AQUI, "salida", "bt_jefes_ranking_MASTER.mp4")
OUT = os.path.join(AQUI, "salida", "bt_jefes_ranking_MASTER_v2.mp4")

tramos = sorted(tuple(int(x) for x in t.split("-")) for t in sys.argv[1:])
ins, filt, partes, k = ["-i", M], [], [], 1
pos = 0
for a, b in tramos:
    f0, f1 = a * FPS, b * FPS
    filt.append(f"[0:v]trim=start_frame={pos}:end_frame={f0},setpts=PTS-STARTPTS[v{len(partes)}]")
    partes.append(f"[v{len(partes)}]")
    ins += ["-i", os.path.join(AQUI, "salida", f"tramo_{a}_{b}.mp4")]
    filt.append(f"[{k}:v]trim=start_frame=0:end_frame={f1 - f0},setpts=PTS-STARTPTS[v{len(partes)}]")
    partes.append(f"[v{len(partes)}]")
    k += 1
    pos = f1
filt.append(f"[0:v]trim=start_frame={pos},setpts=PTS-STARTPTS[v{len(partes)}]")
partes.append(f"[v{len(partes)}]")
filt.append("".join(partes) + f"concat=n={len(partes)}:v=1:a=0[v]")
cmd = ["ffmpeg", "-y", "-loglevel", "error"] + ins + ["-filter_complex", ";".join(filt), "-map", "[v]", "-map", "0:a",
       "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy",
       "-movflags", "+faststart", OUT]
r = subprocess.run(cmd)
if r.returncode:
    raise SystemExit("ffmpeg falló")
d = lambda f: subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                             capture_output=True, text=True).stdout.strip()
print("MASTER", d(M), "-> v2", d(OUT), OUT)
