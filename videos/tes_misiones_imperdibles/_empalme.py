# -*- coding: utf-8 -*-
"""Empalma por número de cuadro los tramos re-renderizados (salida/tramo_*.mp4) sobre la imagen del MASTER y conserva su audio
(y la pantalla final). Sale salida/<v>_MASTER_empalme.mp4; si cuadra, se renombra a MASTER.
    python _empalme.py"""
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(AQUI, "salida")
MASTER = os.path.join(S, "tes_misiones_imperdibles_MASTER.mp4")
FPS = 30
TRAMOS = [(100.0, "tramo_100_114.mp4", 435), (144.0, "tramo_144_156.mp4", 375), (547.0, "tramo_547_560.mp4", 390)]

ins = ["-i", MASTER] + sum([["-i", os.path.join(S, f)] for _, f, _ in TRAMOS], [])
partes, filtros, cur = [], [], 0
for k, (t0, _, n) in enumerate(TRAMOS):
    f0 = int(round(t0 * FPS))
    filtros.append(f"[0:v]trim=start_frame={cur}:end_frame={f0},setpts=PTS-STARTPTS[a{k}]")
    filtros.append(f"[{k + 1}:v]trim=end_frame={n},setpts=PTS-STARTPTS[t{k}]")
    partes += [f"[a{k}]", f"[t{k}]"]
    cur = f0 + n
filtros.append(f"[0:v]trim=start_frame={cur},setpts=PTS-STARTPTS[z]")
partes.append("[z]")
filtros.append("".join(partes) + f"concat=n={len(partes)}:v=1:a=0[v]")
out = os.path.join(S, "tes_misiones_imperdibles_MASTER_empalme.mp4")
cmd = ["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", *ins, "-filter_complex", ";".join(filtros), "-map", "[v]", "-map", "0:a",
       "-c:v", "h264_nvenc", "-preset", "p5", "-cq", "19", "-pix_fmt", "yuv420p", "-r", str(FPS), "-c:a", "copy", "-movflags", "+faststart", out]
subprocess.run(cmd, check=True)
print("listo:", out)
