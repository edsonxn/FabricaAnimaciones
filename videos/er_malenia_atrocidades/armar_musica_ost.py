# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Elden Ring (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Pistas en audio/ost/ (yt-dlp de los canales oficiales):
tema = «Elden Ring» (Tsukasa Saitoh - Topic, KBP1zYwBzOE) · malenia = «Malenia, Blade of Miquella» (Yuka Kitamura, W3SWV8tvu18)
haligtree = «Miquella's Haligtree» (Tai Tomisawa - Topic, waM5_Nv-rHk) · elphael = «Elphael» (Tai Tomisawa - Topic, Z-lGjnJLgv8)
radahn = «Starscourge Radahn» (Shoi Miyazawa - Topic, Z1ts4FP1WWM) · mesa = «Roundtable Hold» (Tsukasa Saitoh - Topic, iRxpAnq3X9c)
diosa = «Malenia, Goddess of Rot» (fase 2, vrUOggNFIwc)
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py er_malenia_atrocidades mezcla`)
"""
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
CRUCE = 2.0          # fundido cruzado entre secciones (s)
LUFS = -23.0         # cada sección a la misma sonoridad (la mezcla luego la baja bajo la voz)

# (inicio, fin) de cada sección en el video y las pistas que la llenan en orden: (archivo, desde s)
SECCIONES = [
    ((0.0, 78.0), [("tema", 0)]),                                   # gancho: tema principal
    ((78.0, 276.0), [("malenia", 0)]),                              # #5 nunca conoció la derrota
    ((276.0, 477.0), [("haligtree", 0), ("elphael", 0)]),           # #4 sus caballeros (Árbol Sagrado / Elphael)
    ((477.0, 681.0), [("radahn", 0)]),                              # #3 Caelid y Radahn
    ((681.0, 897.0), [("mesa", 0), ("elphael", 80)]),               # #2 Millicent: melancolía de la Mesa Redonda
    ((897.0, 1101.0), [("diosa", 0)]),                              # #1 la tercera flor (fase 2)
    ((1101.0, None), [("tema", 20)]),                               # cierre
]


def cargar(n):
    x, sr = sf.read(os.path.join("audio", "ost", n + ".wav"), always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    return x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)


def rampa(n, sube=True):
    r = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    return np.sin(r * np.pi / 2)[:, None]


def main():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    total = float(tl.get("total") or tl.get("duracion") or max(e["fin"] for e in tl["escenas"]))
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for (t0, t1), pistas in SECCIONES:
        t1 = total if t1 is None else t1
        largo = int((t1 - t0 + CRUCE) * SR)                         # se solapa CRUCE con la siguiente
        seg = np.zeros((0, 2))
        for n, desde in pistas:
            x = cargar(n)[int(desde * SR):]
            if len(seg):
                k = min(nc, len(seg), len(x))
                seg[-k:] = seg[-k:] * rampa(k, False) + x[:k] * rampa(k)
                seg = np.vstack([seg, x[k:]])
            else:
                seg = x
            if len(seg) >= largo:
                break
        while len(seg) < largo:                                       # si aún falta, repite la primera pista
            x = cargar(pistas[0][0])
            k = min(nc, len(seg), len(x))
            seg[-k:] = seg[-k:] * rampa(k, False) + x[:k] * rampa(k)
            seg = np.vstack([seg, x[k:]])
        seg = seg[:largo].copy()
        l = meter.integrated_loudness(seg)
        seg *= 10 ** ((LUFS - l) / 20)
        if t0 == 0:
            seg[:SR] *= rampa(SR)
        else:
            seg[:nc] *= rampa(nc)
        seg[-nc:] *= rampa(nc, False)
        i0 = int(max(0.0, t0 - CRUCE / 2) * SR) if t0 > 0 else 0
        out[i0:i0 + len(seg)] += seg[:len(out) - i0]
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(p for p, _ in pistas):24s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    main()
