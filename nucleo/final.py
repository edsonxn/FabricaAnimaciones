# -*- coding: utf-8 -*-
"""Etapa final: salida/video_sin_audio.mp4 + audio/final.wav ->
   salida/<titulo>_MASTER.mp4 (video sin recomprimir, AAC 320k),
   salida/<titulo>.srt  (+ salida/<titulo>_WHATSAPP.mp4 720p solo si FAB_WHATSAPP=1)"""
import json
import os
import re
import subprocess
import unicodedata

import config

TL = json.load(open("timeline.json", encoding="utf-8"))


def slug(s):
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")[:60] or "video"


def ff(*args):
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args], check=True)


def srt(ruta):
    def ts(x):
        h, r = divmod(x, 3600)
        m, s = divmod(r, 60)
        return f"{int(h):02d}:{int(m):02d}:{int(s):02d},{int(round((s - int(s)) * 1000)):03d}"
    n = 0
    with open(ruta, "w", encoding="utf-8") as f:
        for e in TL["escenas"]:
            for fr in e["frases"]:
                n += 1
                f.write(f"{n}\n{ts(fr['t0'])} --> {ts(fr['t1'])}\n{fr['texto']}\n\n")


def main():
    titulo = TL.get("titulo") or os.path.basename(os.getcwd())
    base = os.path.join("salida", config.ARCHIVO or slug(titulo))
    master, wa = base + "_MASTER.mp4", base + "_WHATSAPP.mp4"
    # fuente de video: el render sin audio; si ya se limpió, la pista de video del MASTER anterior
    fuente = "salida/video_sin_audio.mp4"
    if not os.path.exists(fuente):
        if not os.path.exists(master):
            raise SystemExit("Falta salida/video_sin_audio.mp4: corre antes 'python fab.py <video> video'")
        fuente = base + "_video_previo.mp4"
        os.replace(master, fuente)
    tmp = master + ".tmp.mp4"
    ff("-i", fuente, "-i", "audio/final.wav", "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
       "-c:a", "aac", "-b:a", "320k", "-ar", "48000", "-movflags", "+faststart", "-metadata", f"title={titulo}", tmp)
    os.replace(tmp, master)
    if fuente.endswith("_video_previo.mp4"):
        os.remove(fuente)
    dur = TL["total"]
    if not os.environ.get("FAB_WHATSAPP"):
        wa = None
    vbr = int(max(700, min(3500, (52 * 8 * 1024 * 1024 / dur - 128_000) / 1000)))
    log = os.path.join("salida", "wa2pass")
    comun = [] if wa is None else ["-i", master, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "slow", "-b:v", f"{vbr}k"]
    if wa is not None:
        ff(*comun, "-pass", "1", "-passlogfile", log, "-an", "-f", "mp4", os.devnull)
    if wa is not None:
        ff(*comun, "-maxrate", f"{int(vbr * 1.5)}k", "-bufsize", f"{vbr * 3}k", "-pass", "2", "-passlogfile", log,
       "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "128k", "-ar", "48000",
       "-movflags", "+faststart", wa)
    for x in os.listdir("salida"):
        if x.startswith("wa2pass"):
            os.remove(os.path.join("salida", x))
    srt(base + ".srt")
    for r in [x for x in (master, wa, base + ".srt") if x]:
        print(f"{r}  {os.path.getsize(r) / 1e6:.1f} MB")
    # limpiar intermedios regenerables (~1 GB por video de 3 min); FAB_CONSERVAR=1 para mantenerlos
    if not os.environ.get("FAB_CONSERVAR"):
        import shutil
        shutil.rmtree("segmentos", ignore_errors=True)
        if os.path.exists("salida/video_sin_audio.mp4"):
            os.remove("salida/video_sin_audio.mp4")
        print("intermedios borrados (segmentos/ y video_sin_audio.mp4); el MASTER conserva el video")


if __name__ == "__main__":
    main()
