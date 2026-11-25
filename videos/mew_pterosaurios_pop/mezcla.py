# -*- coding: utf-8 -*-
"""Mezcla del Recetario de los pterosaurios: su voz (Demucs, con el corte de la intro de banda) + música de la biblioteca
(arana_techo__lyria_tramo1 desde 50 s: marimba, pizzicato, celesta; documental curioso) con «ducking»
+ SFX de papel, sellos, pluma, huellas y pase de hoja sintetizados por código → audio/mezcla_recetario.wav (48 kHz)."""
import subprocess, sys
from pathlib import Path
import numpy as np
from scipy.io import wavfile
from scipy.signal import butter, sosfilt
sys.path.insert(0, str(Path(__file__).parent))
from comun import CUT_A, GAP, SRC_B, SRC_FIN, FIN_EL, DUR, salida

A = Path(__file__).parent
SR = 48000
MUS_DESDE = 50.0
rng = np.random.default_rng(11)


def leer(f, ss=None, t=None):
    tmp = A / "audio/_tmp.wav"
    cmd = ["ffmpeg", "-y", "-v", "error"] + (["-ss", str(ss)] if ss is not None else []) + ["-i", str(f)] + (["-t", str(t)] if t else []) + ["-ac", "2", "-ar", str(SR), str(tmp)]
    subprocess.run(cmd, check=True)
    _, x = wavfile.read(tmp); tmp.unlink()
    return x.astype(np.float32) / 32768


n = int(DUR * SR)
src = leer(A / "audio/_demucs/htdemucs/voz_completa/vocals.wav")
voz = np.zeros((n, 2), np.float32)
a = src[:int(CUT_A * SR)].copy()
a[-int(0.08 * SR):] *= np.linspace(1, 0, int(0.08 * SR))[:, None]
voz[:len(a)] = a
b = src[int(SRC_B * SR):int(SRC_FIN * SR)].copy()
b[:int(0.04 * SR)] *= np.linspace(0, 1, int(0.04 * SR))[:, None]
b[-int(0.15 * SR):] *= np.linspace(1, 0, int(0.15 * SR))[:, None]
i0 = int((CUT_A + GAP) * SR)
voz[i0:i0 + len(b)] = b[:n - i0]

mus = leer(A / "audio/musica_src.mp3", MUS_DESDE, DUR + 0.5)[:n]
mus = np.pad(mus, ((0, n - len(mus)), (0, 0)))
t = np.arange(n) / SR
mus *= np.minimum(t / 0.6, 1)[:, None] * np.clip((DUR - t) / 1.8, 0, 1)[:, None]
e = np.abs(voz).mean(1)
e = sosfilt(butter(1, 3, "low", fs=SR, output="sos"), e)
e = e / (e.max() + 1e-9)
duck = 1 - 0.55 * np.clip(e * 4, 0, 1)
rms_v = np.sqrt((voz[voz.any(1)] ** 2).mean())
rms_m = np.sqrt((mus ** 2).mean()) + 1e-9
mus *= (rms_v * 10 ** (-16 / 20) / rms_m) * duck[:, None]
mus[int(FIN_EL * SR):] *= 1.7                                   # el cierre sin voz: la música sube
out = voz + mus


def env(m, a=0.003, d=0.12):
    x = np.arange(m) / SR
    return np.minimum(x / a, 1) * np.exp(-x / d)


def banda(x, lo, hi):
    return sosfilt(butter(2, [lo, hi], "band", fs=SR, output="sos"), x)


def papel_cae(dur=0.22):
    m = int(dur * SR)
    return (banda(rng.standard_normal(m), 400, 6000) * env(m, 0.004, 0.05) * 1.3).astype(np.float32)


def pagina(dur=0.5):
    m = int(dur * SR); x = rng.standard_normal(m)
    y = np.zeros(m, np.float32)
    for k in range(12):
        a_, b_ = m * k // 12, m * (k + 1) // 12
        fc = 900 + 3500 * k / 12
        y[a_:b_] = banda(x[a_:b_], fc * 0.5, fc * 1.5)
    s = np.arange(m) / m
    return y * np.sin(np.pi * s) ** 1.2 * 1.6


def sello(dur=0.3):                                             # sello de goma: golpe sordo sobre la mesa
    m = int(dur * SR); x = np.arange(m) / SR
    tono = np.sin(2 * np.pi * (130 * np.exp(-x * 25) + 60) * x) * np.exp(-x / 0.05)
    r = sosfilt(butter(2, 1500, "low", fs=SR, output="sos"), rng.standard_normal(m)) * np.exp(-x / 0.012)
    return (tono * 0.9 + r * 0.7).astype(np.float32)


def pluma(dur):
    m = int(dur * SR); x = np.arange(m) / SR
    am = 0.5 + 0.5 * np.sin(2 * np.pi * 9 * x + rng.uniform(0, 6)) ** 2
    return (banda(rng.standard_normal(m), 2500, 8000) * am * np.minimum(x / 0.02, 1) * np.clip((dur - x) / 0.05, 0, 1) * 0.5).astype(np.float32)


def tajo(dur=0.2):                                             # tachón rápido de pluma
    m = int(dur * SR)
    return (banda(rng.standard_normal(m), 2000, 9000) * env(m, 0.01, 0.06) * 1.2).astype(np.float32)


def aleteo(dur=1.6):                                           # el pterosaurio planea: viento suave que pasa
    m = int(dur * SR); x = np.arange(m) / SR
    y = banda(rng.standard_normal(m), 250, 1800) * np.sin(np.pi * x / dur) ** 2
    golpes = sum(np.exp(-((x - k) / 0.05) ** 2) for k in (0.35, 0.9))
    return (y * (0.6 + 0.8 * golpes) * 0.9).astype(np.float32)


def pop():
    m = int(0.25 * SR); x = np.arange(m) / SR
    return (np.sin(2 * np.pi * (500 + 900 * np.exp(-x * 30)) * x) * np.exp(-x / 0.05) * 0.7).astype(np.float32)


def pisada():
    m = int(0.18 * SR); x = np.arange(m) / SR
    return (np.sin(2 * np.pi * 70 * x) * np.exp(-x / 0.04) + banda(rng.standard_normal(m), 200, 1200) * np.exp(-x / 0.015) * 0.5).astype(np.float32)


def pon(x, tt, db, pan=0.0):
    i = int(tt * SR)
    if i >= n or i < 0:
        return
    x = x[: n - i] * 10 ** (db / 20)
    out[i:i + len(x), 0] += x * (1 - max(pan, 0))
    out[i:i + len(x), 1] += x * (1 + min(pan, 0))


S = salida
for tt in (CUT_A + 0.02, S(33.30), S(46.80), S(54.70), S(70.70)):
    pon(pagina(), tt - 0.02, -20)
for ts in (3.7, 5.32, 23.5, 27.45, 33.5, 46.8, 49.95, 60.55, 61.15, 64.25, 78.8, 81.95):
    pon(papel_cae(), S(ts) + 0.18, -21, rng.uniform(-0.3, 0.3))
for ts in (6.9, 32.9, 37.34, 46.3, 60.5, 65.4):
    pon(sello(), S(ts) + 0.08, -15)
pon(sello(0.45), 12.48 + 0.08, -11)                            # ¡COMENZAMOS!
pon(sello(0.3), CUT_A + GAP - 0.05, -17)                        # sello del capítulo
pon(sello(0.5), S(90.75) + 0.08, -11)                           # CONTINUARÁ
pon(aleteo(), 0.05, -19, 0.3)
for ts in (29.6, 38.2):
    pon(tajo(), S(ts), -19)
for k in range(8):
    pon(pisada(), S(53.0 + 0.17 * k), -17, -0.4 + 0.1 * k)
pon(pop(), 9.6, -20); pon(pop(), S(76.2), -21)
for t0, txt in ((0.55, "los primeros vertebrados"), (1.55, "en volar"), (4.08, "la era de los dinosaurios"), (6.12, "casi tanto éxito"),
                (9.36, "¿de qué animales hablo?"), (26.9, "«pterodáctilos»"), (28.1, "pterodáctilo"), (30.0, "Pterodactylus = un solo género"),
                (32.3, "pterosaurio"), (34.0, "Crystal Palace, Londres"), (36.2, "«dinosaurios»"), (41.8, "la misma época"),
                (44.68, "no forman parte"), (47.7, "cocodrilos"), (48.4, "su propio orden"), (50.7, "anatomía"), (54.0, "locomoción"),
                (58.5, "patas debajo de la cadera"), (64.8, "a los lados"), (67.8, "zigzag de tinta"), (68.2, "zigzaguean y reptan"),
                (70.9, "círculos"), (74.06, "características"), (75.2, "sí son similares"), (79.4, "Sordes pilosus"), (81.2, "picnofibras"),
                (82.7, "pluma"), (84.8, "árbol"), (87.8, "en sus ancestros"), (91.2, "el video completo, en YouTube")):
    pon(pluma(min(0.9, 0.05 * len(txt) + 0.2)), S(t0), -29, rng.uniform(-0.25, 0.25))

pico = np.abs(out).max()
if pico > 0.97:
    out *= 0.97 / pico
wavfile.write(A / "audio/mezcla_recetario.wav", SR, (out * 32767).astype(np.int16))
print("audio/mezcla_recetario.wav", f"{len(out) / SR:.2f} s, pico {pico:.2f}")
