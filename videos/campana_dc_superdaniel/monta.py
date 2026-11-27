# -*- coding: utf-8 -*-
"""MONTAJE «Súper Daniel» (27-nov-2026): `python monta.py [--prueba]`.
Tramo A = clips/c12_360.mp4 (clip 1 + Ampliar 10 s, 20 s) reescalado local 360x640 -> 1080x1920.
Tramo B = remate clips/c4_720.mp4 («720p mejorada» de Flow; si no está, c4_360) -> 1080x1920.
Cartela por código (logo PAN + DANIEL CERVANTES + «Hecho con IA») con fundido desde el remate.
Audio = audio/c12_daniel.wav + audio/c4_daniel.wav (voz convertida a la de Daniel con sts.py) + cola; loudnorm -14 LUFS.
Salida: salida/superdaniel_MASTER.mp4 (1080x1920, 24 fps)."""
import math
import os
import subprocess
import sys

import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFilter, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
W, H, FPS, SR = 1080, 1920, 24, 48000
A_FIN = 19.96            # corte del tramo A (justo antes del último cuadro)
CART = 2.2               # duración de la cartela
XF = 0.4                 # fundido remate -> cartela
AZUL, AZUL_OSC, CIAN, BLANCO = (0, 51, 160), (4, 22, 70), (41, 182, 246), (255, 255, 255)
_FD = [os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts"), "C:/Windows/Fonts"]


def p(*a):
    return os.path.join(AQUI, *a)


def fuente(arch, tam, resp="arialbd.ttf"):
    for d in _FD:
        for a in (arch, resp):
            if os.path.exists(os.path.join(d, a)):
                return ImageFont.truetype(os.path.join(d, a), tam)
    raise SystemExit("sin fuente")


def ff(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True)


ESCALA = "scale=1080:1920:flags=lanczos,unsharp=5:5:0.55:5:5:0.0,format=yuv420p"


def tramo_a():
    ff("-i", p("clips", "c12_360.mp4"), "-t", f"{A_FIN}", "-an",
       "-vf", "hqdn3d=1.2:1.2:3:3," + ESCALA, "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "slow",
       p("render", "a.mp4"))


def tramo_b():
    src = p("clips", "c4_720.mp4") if os.path.exists(p("clips", "c4_720.mp4")) else p("clips", "c4_360.mp4")
    print("remate:", os.path.basename(src))
    ff("-i", src, "-an", "-vf", ESCALA, "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "slow",
       p("render", "b.mp4"))


def ease(x):
    x = max(0.0, min(1.0, x))
    return 1 - (1 - x) ** 3


def cartela():
    logo = Image.open(p("fuente", "pan_2025.png")).convert("RGBA")
    fN = fuente("Poppins-Black.ttf", 90)
    fS = fuente("Poppins-ExtraBold.ttf", 46)
    fIA = fuente("Poppins-SemiBold.ttf", 30, "segoeuib.ttf")
    # fondo: degradado radial azul PAN
    yy, xx = np.mgrid[0:H, 0:W]
    r = np.sqrt(((xx - W / 2) / W) ** 2 + ((yy - H * .42) / H) ** 2)
    k = np.clip(r / .75, 0, 1)[..., None]
    fondo = (np.array(AZUL) * (1 - k) + np.array(AZUL_OSC) * k).astype(np.uint8)
    fondo = Image.fromarray(fondo, "RGB").convert("RGBA")
    os.makedirs(p("render", "cart"), exist_ok=True)
    n = int(round(CART * FPS))
    for i in range(n):
        t = i / FPS
        fr = fondo.copy()
        # halo cian detrás del logo
        u = ease(t / .5)
        lw = int(560 * (0.86 + 0.14 * u) * (1 + 0.015 * math.sin(t * 3)))
        lg = logo.resize((lw, int(lw * logo.height / logo.width)), Image.LANCZOS)
        halo = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        hd = ImageDraw.Draw(halo)
        cy = 700
        hd.ellipse((W / 2 - 360, cy - 360, W / 2 + 360, cy + 360), fill=CIAN + (int(110 * u),))
        halo = halo.filter(ImageFilter.GaussianBlur(90))
        fr = Image.alpha_composite(fr, halo)
        # placa blanca redondeada para que el logo (fondo transparente, letras azules) se lea
        placa = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        pd = ImageDraw.Draw(placa)
        pw, ph = lw + 90, lg.height + 90
        pd.rounded_rectangle((W / 2 - pw / 2, cy - ph / 2, W / 2 + pw / 2, cy + ph / 2), radius=60,
                             fill=BLANCO + (int(255 * u),))
        fr = Image.alpha_composite(fr, placa)
        lg.putalpha(lg.getchannel("A").point(lambda v: int(v * u)))
        fr.alpha_composite(lg, (W // 2 - lw // 2, cy - lg.height // 2))
        d = ImageDraw.Draw(fr)
        a2 = ease((t - .35) / .45)
        if a2 > 0:
            y = int(1130 + (1 - a2) * 60)
            d.text((W / 2, y), "DANIEL CERVANTES", font=fN, fill=BLANCO + (int(255 * a2),), anchor="ma")
            d.text((W / 2, y + 140), "JUCHIPILA, CON LUZ", font=fS, fill=CIAN + (int(255 * a2),), anchor="ma")
        a3 = ease((t - .6) / .4)
        if a3 > 0:
            d.text((W / 2, H - 120), "Hecho con IA", font=fIA, fill=(200, 215, 240, int(230 * a3)), anchor="ma")
        fr.convert("RGB").save(p("render", "cart", f"{i:04d}.png"))
    ff("-framerate", str(FPS), "-i", p("render", "cart", "%04d.png"), "-c:v", "libx264", "-crf", "16",
       "-pix_fmt", "yuv420p", p("render", "c.mp4"))


def dur(f):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f],
                                capture_output=True, text=True).stdout)


def video():
    db = dur(p("render", "b.mp4"))
    # A + B por corte seco; B -> cartela con fundido
    ff("-i", p("render", "a.mp4"), "-i", p("render", "b.mp4"), "-i", p("render", "c.mp4"), "-filter_complex",
       f"[0:v][1:v]concat=n=2:v=1:a=0,settb=1/{FPS},setpts=N/{FPS}/TB,fps={FPS}[ab];"
       f"[2:v]settb=1/{FPS},setpts=N/{FPS}/TB,fps={FPS}[c];"
       f"[ab][c]xfade=transition=fade:duration={XF}:offset={A_FIN + db - XF:.3f},format=yuv420p[v]",
       "-map", "[v]", "-r", str(FPS), "-c:v", "libx264", "-crf", "16", "-preset", "slow", p("render", "v.mp4"))


def audio():
    import librosa
    a, _ = librosa.load(p("audio", "c12_daniel.wav"), sr=SR, mono=True)
    b, _ = librosa.load(p("audio", "c4_daniel.wav"), sr=SR, mono=True)
    a = a[:int(A_FIN * SR)]
    na = int(A_FIN * SR)
    a = np.pad(a, (0, max(0, na - len(a))))
    # micro-fundido en el corte A|B para que no truene
    f = int(.02 * SR)
    a[-f:] *= np.linspace(1, 0, f)
    b[:f] *= np.linspace(0, 1, f)
    db = dur(p("render", "b.mp4"))
    b = np.pad(b, (0, max(0, int(db * SR) - len(b))))[:int(db * SR)]
    total = A_FIN + db - XF + CART
    cola = np.zeros(int((total - A_FIN - db) * SR) + SR // 10, np.float32)
    y = np.concatenate([a, b, cola])[:int(total * SR)]
    # fundido de salida en la cartela
    fo = int(1.2 * SR)
    y[-fo:] *= np.linspace(1, 0, fo) ** 2
    sf.write(p("render", "mezcla.wav"), y.astype(np.float32), SR)
    return total


def final(total):
    import json
    import re
    os.makedirs(p("salida"), exist_ok=True)
    # medir con loudnorm y llevar a -14 LUFS con ganancia + limitador (1 pasada dejaba ~-17)
    r = subprocess.run(["ffmpeg", "-hide_banner", "-i", p("render", "mezcla.wav"), "-af",
                        "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    m = json.loads(re.search(r"\{[^{}]+\}", r[r.rfind("Parsed_loudnorm"):]).group(0))
    gan = -14.0 - float(m["input_i"]) + 3.8   # ganancia + limitador (loudnorm lineal se frena por el pico)
    ff("-i", p("render", "v.mp4"), "-i", p("render", "mezcla.wav"), "-map", "0:v", "-map", "1:a",
       "-af", f"volume={gan:.2f}dB,alimiter=limit=0.75:attack=1:release=10:level=false", "-ar", str(SR), "-c:v", "copy", "-c:a", "aac", "-b:a", "192k",
       "-t", f"{total:.3f}", "-movflags", "+faststart", p("salida", "superdaniel_MASTER.mp4"))
    print(f"MASTER: salida/superdaniel_MASTER.mp4 ({total:.2f} s)")


if __name__ == "__main__":
    os.makedirs(p("render"), exist_ok=True)
    if "--cartela" in sys.argv:
        cartela(); sys.exit()
    if "--solo-audio" in sys.argv:
        final(audio()); sys.exit()
    tramo_a(); tramo_b(); cartela(); video(); final(audio())
