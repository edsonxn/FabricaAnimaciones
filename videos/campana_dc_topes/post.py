# -*- coding: utf-8 -*-
"""POST de campana_dc_topes (27-nov-2026): rótulos de videojuego dibujados a 270×480 SIN suavizado, HUD de pelea (barra
«SUSPENSIÓN» que baja en cada tope, contador de topes, «K.O.»), escala ×4 con vecino más cercano a 1080×1920 y sonido
chiptune sintetizado aquí (motor, boings, mofle, crack, pisotón, topes que salen volando, redoble, fanfarria) + música de la
biblioteca agachada bajo la voz. Dos salidas: salida/topes_daniel_MASTER.mp4 (sin censura) y
salida/topes_daniel_PITIDOS_MASTER.mp4 (groserías tapadas con pitido).

  python post.py [--solo-audio]
"""
import glob
import json
import os
import re
import subprocess
import sys

import librosa
import numpy as np
import soundfile as sf
from PIL import Image, ImageDraw, ImageFont

import plan as P

AQUI = os.path.dirname(os.path.abspath(__file__))
FPS, SEG = P.FPS, P.SEG
SR = 48000
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"
FONT = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts", "Montserrat-Black.ttf")
AMARILLO, BLANCO, ROJO, VERDE = (255, 216, 40), (255, 255, 255), (255, 60, 50), (90, 230, 90)
EV = json.load(open(os.path.join(AQUI, "eventos.json")))
FR = P.FRASES

ROTULOS = [   # (t0, t1, texto, y, tamaño, color) — a 270×480
    (0.25, FR[0][1] + .1, "DANIEL CERVANTES", 20, 19, AMARILLO),
    (0.55, FR[0][1] + .1, "VS.", 44, 14, BLANCO),
    (0.75, FR[0][1] + .1, "LOS TOPES", 60, 26, ROJO),
    (P.W(2, "más") - .05, FR[1][1] + .2, "MÁS TOPES", 28, 26, AMARILLO),
    (P.W(2, "calles") - .05, FR[1][1] + .2, "QUE CALLES", 58, 20, BLANCO),
    (P.W(6, "primera") - .05, FR[5][1] + .3, "PRIMERA ORDEN", 30, 24, AMARILLO),
    (P.W(6, "presidente") - .05, FR[5][1] + .3, "COMO PRESIDENTE", 58, 15, BLANCO),
    (P.T_PISOTON + .2, FR[6][1] + .3, "¡FUERA TOPES!", 36, 28, AMARILLO),
    (P.T_SOY - .05, SEG + 1, "DANIEL CERVANTES", 26, 22, AMARILLO),
    (P.T_SOY + .4, SEG + 1, "JUCHIPILA SIN TOPES", 56, 16, BLANCO),
    (P.T_CIERRE, SEG + 1, "SÁTIRA · HECHO CON IA", 456, 9, BLANCO),
]
HUD0, HUD1 = FR[2][0] - .1, P.T_SUSP + 1.6
GOLPES = [t for t, _ in P.GOLPES_B]
KO = (P.T_SUSP, P.T_SUSP + 1.4)


def letrero(im, texto, y, tam, color, x=None):
    d = ImageDraw.Draw(im)
    d.fontmode = "1"
    f = ImageFont.truetype(FONT, tam)
    w = d.textlength(texto, font=f)
    x = int((im.width - w) / 2) if x is None else x
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1, 2):
            if dx or dy:
                d.text((x + dx, y + dy), texto, font=f, fill=(0, 0, 0))
    d.text((x, y), texto, font=f, fill=color)


def hud(im, t):
    d = ImageDraw.Draw(im)
    n = sum(1 for g in GOLPES if t >= g)
    vida = max(0.0, 1 - .16 * n) if t < P.T_SUSP else 0.0
    letrero(im, "SUSPENSIÓN", 10, 10, BLANCO, x=10)
    d.rectangle((9, 25, 131, 35), fill=(0, 0, 0))
    d.rectangle((10, 26, 130, 34), fill=(70, 20, 20))
    w = int(120 * vida)
    if w > 0:
        col = VERDE if vida > .5 else (AMARILLO if vida > .25 else ROJO)
        if any(0 <= t - g < .2 for g in GOLPES) and int(t * 30) % 2:
            col = BLANCO                                   # parpadea al recibir el golpe
        d.rectangle((10, 26, 10 + w, 34), fill=col)
    letrero(im, f"TOPES: {n}", 10, 11, AMARILLO, x=180)
    if KO[0] <= t < KO[1]:
        u = t - KO[0]
        tam = 60 if u < 2 / FPS else 48
        if int(u * 8) % 2 == 0 or u > .5:
            letrero(im, "K.O.", 150, tam, ROJO)


def video():
    tmp = os.path.join(AQUI, "post"); os.makedirs(tmp, exist_ok=True)
    fs = sorted(glob.glob(os.path.join(AQUI, "render", "f_*.png")))
    for k, f in enumerate(fs):
        t = k / FPS
        im = Image.open(f).convert("RGB")
        if t >= P.T_CIERRE:                                # cierre: el fondo se oscurece un poco
            u = min(1.0, (t - P.T_CIERRE) / .4)
            im = Image.blend(im, Image.new("RGB", im.size, (8, 16, 60)), .35 * u)
        for t0, t1, tx, y, tam, col in ROTULOS:
            if t0 <= t < t1:
                letrero(im, tx, y, max(8, int(tam * (.7 if t - t0 < 1.5 / FPS else 1))), col)
        if HUD0 <= t < HUD1:
            hud(im, t)
        im.resize((1080, 1920), Image.NEAREST).save(os.path.join(tmp, f"p_{k:04d}.png"))
    out = os.path.join(AQUI, "salida", "video_sin_audio.mp4")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(tmp, "p_%04d.png"),
                    "-vf", "fps=30", "-c:v", "libx264", "-crf", "16", "-preset", "slow", "-pix_fmt", "yuv420p", out], check=True)
    return out, len(fs)


# ------------------------------------------------------------------ sonidos chiptune sintetizados
def cuadrada(f0, f1, dur, vol=.3, duty=.5, vib=0.0):
    n = int(dur * SR); t = np.arange(n) / SR
    fr = np.linspace(f0, f1, n) * (1 + vib * np.sin(2 * np.pi * 18 * t))
    fase = np.cumsum(fr) / SR
    s = np.where((fase % 1) < duty, 1.0, -1.0) * vol
    env = np.minimum(1, t / .004) * np.clip(1 - t / dur, 0, 1) ** .6
    return (s * env).astype(np.float32)


def ruido8(dur, vol=.3, paso=24, caida=2.0, semilla=3):
    n = int(dur * SR); r = np.random.default_rng(semilla).uniform(-1, 1, n)
    r = np.repeat(r[::paso], paso)[:n]
    return (r * vol * np.linspace(1, 0, n) ** caida).astype(np.float32)


def boing(f=160, dur=.45, vol=.3):
    return cuadrada(f, f * 5, dur, vol, .3, vib=.12)


def golpe(vol=.4):
    n = int(.18 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (90 - 200 * t) * t) * np.exp(-t * 22) * vol
    return (s + ruido8(.18, vol * .6, 12, 3)).astype(np.float32)


def motor(dur, f0, f1, vol=.08):
    return cuadrada(f0, f1, dur, vol, .25, vib=.05)


def clank():
    return np.concatenate([cuadrada(1900, 1700, .05, .22, .5), cuadrada(1400, 1300, .07, .18, .5)])


def blip():
    return np.concatenate([cuadrada(880, 880, .05, .22), cuadrada(1320, 1320, .07, .2)])


def fanfarria():
    return np.concatenate([cuadrada(f, f, d, .2, .25) for f, d in ((523, .1), (659, .1), (784, .1), (1047, .28))])


def ko():
    return np.concatenate([cuadrada(f, f, .16, .25, .5) for f in (523, 392, 262)] + [cuadrada(196, 110, .4, .25, .5)])


def redoble(dur):
    n = int(dur * SR); out = np.zeros(n, np.float32)
    k = 0; t = 0.0
    while t < dur - .05:
        a = int(t * SR); s = ruido8(.045, .12 + .18 * t / dur, 8, 3, semilla=k)
        out[a:a + len(s)] += s[: n - a]
        t += .055; k += 1
    return out


def boom():
    n = int(.9 * SR); t = np.arange(n) / SR
    s = np.sin(2 * np.pi * (70 - 30 * t) * t) * np.exp(-t * 5) * .6
    return (s + ruido8(.9, .45, 40, 2.5)).astype(np.float32)


def mezcla(pitidos=False):
    n = int(SEG * SR)
    mez = np.zeros(n, np.float32)
    v, _ = librosa.load(os.path.join(AQUI, "voz", "voz.wav"), sr=SR, mono=True)
    v = v / (np.max(np.abs(v)) + 1e-9) * .89
    i0 = int(P.VOZ_OFF * SR); voz = np.zeros(n, np.float32); voz[i0:i0 + len(v)] = v[: n - i0]
    if pitidos:
        for f_, w, a, b in P.PALABRAS:
            if w in P.GROSERIAS:
                a_, b_ = int((a - .03) * SR), int((b + .04) * SR)
                tt = np.arange(b_ - a_) / SR
                voz[a_:b_] = (np.sin(2 * np.pi * 1000 * tt) * .32 * np.minimum(1, tt / .005) * np.minimum(1, (tt[-1] - tt) / .005)).astype(np.float32)
    m, _ = librosa.load(r"E:\FabricaAnimaciones\musica_biblioteca\robotaller_4apps__lyria_tramo2.mp3", sr=SR, mono=True,
                        offset=20.0, duration=SEG)
    m = np.pad(m, (0, max(0, n - len(m))))[:n]
    rms = np.sqrt(np.convolve(voz ** 2, np.ones(2400) / 2400, "same"))
    act = np.convolve((rms > .02).astype(np.float32), np.ones(9600) / 9600, "same")
    t = np.arange(n) / SR
    g = 10 ** (-15 / 20) * (1 - np.clip(act, 0, 1) * (1 - 10 ** (-8 / 20)))
    g *= np.clip(t / .3, 0, 1) * np.clip((SEG - t) / 1.0, 0, 1)
    mez += m * g + voz

    def pon(t0, s, db=0.0):
        a = int(t0 * SR); b = min(n, a + len(s))
        if b > a:
            mez[a:b] += s[: b - a] * 10 ** (db / 20)
    for t0, *_ in ROTULOS:
        pon(t0, blip(), -8)
    # 1 · vocho rojo: arranca, BOING y vuela; aterriza y rebota calle arriba
    pon(0.0, motor(P.T_CHOQUE_A, 70, 150), -4)
    pon(P.T_CHOQUE_A, golpe(.5), -2); pon(P.T_CHOQUE_A, boing(140, .6, .3), -3)
    pon(EV["aterriza_A"], golpe(.4), -6)
    for k, (tg, _) in enumerate(EV["golpes_A"]):
        pon(tg, boing(260 + 40 * k, .25, .2), -10 - k)
    # 3-4 · vocho verde: motor, un boing por «tope» (cada vez más agudo), mofle, crack de la suspensión, llanta, K.O.
    pon(P._B[0][0], motor(P.T_SUSP - P._B[0][0], 80, 130, .06), -6)
    for k, tg in enumerate(P.TOPES_L3):
        pon(tg, golpe(.35), -5); pon(tg + .02, boing(180 + 60 * k, .32, .22), -6)
    pon(P.T_MOFLE, golpe(.45), -3); pon(P.T_MOFLE + .22, clank(), -4)
    pon(P.T_MOFLE + .67, clank(), -9); pon(P.T_MOFLE + .9, clank(), -13)
    pon(P.T_SUSP, ruido8(.3, .5, 6, 3, 7), -3); pon(P.T_SUSP + .02, cuadrada(600, 90, .5, .25, .5), -6)
    for k in range(4):
        pon(P.T_SUSP + .3 + .57 * k, golpe(.25), -8 - 2 * k)
    pon(P.T_SUSP + .15, ko(), -7)
    pon(P.T_SUSTO, cuadrada(300, 1200, .3, .25, .25), -6)
    # 5 · coraje: siseo de vapor, pisotón, patada y brinquitos
    pon(FR[4][0], ruido8(FR[4][1] - FR[4][0] + .3, .07, 2, .3, 11), -10)
    pon(P.T_VERGA5 + .15, golpe(.4), -6)
    pon(P.T_PATADA + .02, golpe(.6), -2); pon(P.T_PATADA + .05, cuadrada(900, 300, .15, .2, .5), -8)
    t = P.T_PIE
    while t < FR[4][1] + .25:
        pon(t + .1, cuadrada(500, 800, .06, .15, .25), -12); t += .26
    # 6 · redoble · 7 · brinco, PISOTÓN y cada tope que sale volando
    pon(P.W(6, "primera"), redoble(FR[5][1] - P.W(6, "primera") + .25), -6)
    pon(P.T_TIRAR, cuadrada(200, 900, .35, .22, .25), -6)
    pon(P.T_PISOTON, boom(), -1)
    for k, tv in enumerate(P.T_VUELAN):
        pon(tv, cuadrada(300 + 30 * k, 1500 + 80 * k, .35, .16, .25), -9)
    pon(EV["vuela_B"], boing(120, .7, .25), -6)
    # 8 · fanfarria y el carro blanco pasando liso
    pon(P.T_BAILE, fanfarria(), -6)
    pon(EV["carro_C"], motor(2.5, 110, 140, .05), -10)
    pon(P.T_CIERRE + .1, fanfarria(), -5)
    os.makedirs(os.path.join(AQUI, "audio"), exist_ok=True)
    nombre = "mezcla_pitidos" if pitidos else "mezcla"
    cruda = os.path.join(AQUI, "audio", nombre + "_cruda.wav"); sf.write(cruda, np.stack([mez, mez]).T, SR, subtype="FLOAT")
    # sonoridad: se mide, se aplica la ganancia que falta y un limitador (loudnorm de 1 pasada se queda corto con picos)
    r = subprocess.run([FFMPEG, "-hide_banner", "-i", cruda, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True)
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    gan = -14.0 - lufs
    out = os.path.join(AQUI, "audio", nombre + ".wav")
    subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", cruda, "-af", f"volume={gan:.2f}dB,alimiter=limit=0.84:attack=2:release=40:level=false",
                    "-ar", str(SR), "-ac", "2", out], check=True)
    print(nombre, f"{lufs:.1f} LUFS -> +{gan:.1f} dB")
    return out


def main():
    if "--solo-audio" in sys.argv:
        vid = os.path.join(AQUI, "salida", "video_sin_audio.mp4")
    else:
        vid, nf = video(); print("video", nf, "cuadros")
    for pit, nom in ((False, "topes_daniel_MASTER.mp4"), (True, "topes_daniel_PITIDOS_MASTER.mp4")):
        aud = mezcla(pit)
        master = os.path.join(AQUI, "salida", nom)
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", vid, "-i", aud, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                        "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", master], check=True)
        print("OK", master)


if __name__ == "__main__":
    main()
