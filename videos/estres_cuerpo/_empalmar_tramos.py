# -*- coding: utf-8 -*-
"""Empalma salida/tramo_*.mp4 (re-render de `video --tramo a-b`) dentro de salida/_video_sin_audio_v1.mp4, cuadro exacto,
y escribe salida/video_sin_audio.mp4 con los mismos ajustes del motor (libx264 medium crf 18). Uso: python empalmar.py <v>"""
import os, subprocess, sys

os.chdir(sys.argv[1])
FPS, TOTAL = 30, 24075
TRAMOS = [(99.0, 104.0), (130.0, 133.0), (196.0, 198.5), (202.5, 205.5), (243.5, 246.5), (347.0, 350.0), (395.0, 398.0),
          (473.5, 476.5), (597.0, 600.0), (719.0, 723.5), (798.0, 802.5)]
FF, FP = r"C:\ffmpeg\bin\ffmpeg.exe", r"C:\ffmpeg\bin\ffprobe.exe"


def cuadros(r):
    return int(subprocess.run([FP, "-v", "error", "-count_packets", "-select_streams", "v:0", "-show_entries",
                               "stream=nb_read_packets", "-of", "csv=p=0", r], capture_output=True, text=True).stdout)


ins, partes, filtro, cur = ["-i", "salida/_video_sin_audio_v1.mp4"], [], [], 0
for k, (a, b) in enumerate(TRAMOS, 1):
    f0, f1 = int(round(a * FPS)), int(round(min(b, TOTAL / FPS) * FPS))
    r = f"salida/tramo_{int(a)}_{int(b)}.mp4"
    n = cuadros(r)
    assert n == f1 - f0, f"{r}: {n} cuadros, esperaba {f1 - f0}"
    if f0 > cur:
        partes.append(("o", cur, f0))
    partes.append(("t", k, None))
    ins += ["-i", r]
    cur = f1
if cur < TOTAL:
    partes.append(("o", cur, TOTAL))
no = sum(1 for p in partes if p[0] == "o")
filtro.append(f"[0:v]split={no}" + "".join(f"[s{i}]" for i in range(no)))
etq, i = [], 0
for j, p in enumerate(partes):
    if p[0] == "o":
        filtro.append(f"[s{i}]trim=start_frame={p[1]}:end_frame={p[2]},setpts=PTS-STARTPTS[p{j}]")
        i += 1
    else:
        filtro.append(f"[{p[1]}:v]setpts=PTS-STARTPTS[p{j}]")
    etq.append(f"[p{j}]")
filtro.append("".join(etq) + f"concat=n={len(etq)}:v=1:a=0,fps={FPS}[v]")
subprocess.run([FF, "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(filtro), "-map", "[v]", "-c:v", "libx264",
                "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-movflags", "+faststart",
                "salida/video_sin_audio.mp4"], check=True)
n = cuadros("salida/video_sin_audio.mp4")
print("video_sin_audio.mp4:", n, "cuadros", "OK" if n == TOTAL else f"MAL (esperaba {TOTAL})")
