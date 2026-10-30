# -*- coding: utf-8 -*-
"""Fragmentos REALES del canal para la trayectoria (ids en canales/formula/edsonxn_videos.json), 720p sin audio, en capturas/arch_*.mp4. Nada de Skyrim, WoW ni Shadowlands.
  python archivo_canal.py [nombre ...]      python archivo_canal.py hoja [nombre ...]"""
import subprocess
import sys

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
FP = FF.replace("ffmpeg.exe", "ffprobe.exe")

# nombre: (id, desde, hasta)
FRAG = {
    "ragdoll": ("T6TcLZPtI4Q", 30, 40),
    "tutorial": ("WbyScpgl5mw", 300, 310),
    "toro": ("hf_6SlW_y0Q", 20, 30),
    "slime": ("mwEpeqI3dZQ", 5, 15),
    "vr": ("1Ax6sXN-KlU", 20, 30),
    "iajuego": ("Z5CWqT-Nvkk", 600, 610),
    "doc": ("6rqPo_fgz58", 60, 70),
    # videos hechos por la fábrica en canales permitidos (Cronopapel y Crónicas del gaming: de su MASTER local, aún no son públicos o son privados)
    "bita": ("dPk9bs6dX0Q", 120, 128),
}


LOCAL = {"crono": ("../historia_jalisco/salida/historia_jalisco_5min_MASTER.mp4", 60, 8), "gaming": ("../majora_mask/salida/majora_mask_MASTER.mp4", 200, 8)}


def baja(n):
    if n in LOCAL:
        r, a, d = LOCAL[n]
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", str(a), "-t", str(d), "-i", r, "-an", "-vf", "scale=1280:720,fps=30", "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", f"capturas/arch_{n}.mp4"], check=True)
        return print("ok", n)
    i, a, b = FRAG[n]
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "--force-overwrites", "-f", "bv*[height<=720][ext=mp4]/bv*[height<=720]/b[height<=720]",
                    "--download-sections", f"*{a}-{b}", "--force-keyframes-at-cuts", "--ffmpeg-location", r"C:\ffmpeg\bin", "-o", f"capturas/_a_{n}.%(ext)s",
                    f"https://www.youtube.com/watch?v={i}"], check=True)
    import glob
    origen = glob.glob(f"capturas/_a_{n}.*")[0]
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", origen, "-an", "-vf", "scale=1280:720:force_original_aspect_ratio=decrease,pad=1280:720:(ow-iw)/2:(oh-ih)/2,fps=30", "-c:v", "libx264", "-preset", "veryfast",
                    "-crf", "22", "-pix_fmt", "yuv420p", f"capturas/arch_{n}.mp4"], check=True)
    import os
    os.remove(origen)
    print("ok", n)


def vertical(n, ancho=1.0):
    """Clip vertical a 16:9: el cuadro al centro sobre su propia copia borrosa. ancho = fracción útil, sin las franjas negras del original."""
    f = f"[0:v]crop=iw*{ancho}:ih,split[a][b];[b]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,boxblur=30:3,eq=brightness=-.22[bg];[a]scale=-2:1080[fg];[bg][fg]overlay=(W-w)/2:0"
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"capturas/{n}.mp4", "-filter_complex", f, "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", f"capturas/{n}_16x9.mp4"], check=True)
    print("ok", n)


def hoja(n):
    d = float(subprocess.run([FP, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f"capturas/arch_{n}.mp4"], capture_output=True, text=True).stdout)
    subprocess.run([FF, "-y", "-loglevel", "error", "-i", f"capturas/arch_{n}.mp4", "-vf", f"fps=6/{d:.2f},scale=426:-1,tile=3x2", "-frames:v", "1", f"previews/arch_{n}.jpg"], check=True)


if __name__ == "__main__":
    pide = sys.argv[1:]
    if pide[:1] == ["vertical"]:
        vertical("arch_slime", .27)
        vertical("arch_vr", .32)
        vertical("movil")
        sys.exit()
    if pide[:1] == ["hoja"]:
        for n in pide[1:] or FRAG:
            hoja(n)
        sys.exit()
    for n in pide or [*FRAG, *LOCAL]:
        baja(n)
        hoja(n)
