# -*- coding: utf-8 -*-
"""Música ORIGINAL de World of Warcraft en lugar de Lyria (regla del canal, 23-oct-2026; copiado de wow_curiosidades_kalimdor).

UN TEMA POR ZONA del recorrido: `audio/wow/_temas.json` (zona -> [id de YouTube, título, canal]) con las mismas claves que
`guion.ZONA_DE`. Cada tramo de `LYRIA.tramos` recibe el tema de la zona más frecuente entre sus escenas (así la música cambia al
cambiar de zona). El audio se bajó con `yt-dlp -f bestaudio` a audio/wow/<id>.<ext>; aquí se convierte a WAV 48 kHz si falta,
se le quitan los huecos de silencio, se iguala en sonoridad (LUFS) y se corta para cada tramo la pieza audio/lyria_tramoN.wav
con la duración justa (+ el cruce de 3 s); cada tema sigue donde se quedó, sin repetir pasaje.
Luego `python fab.py wow_100_curiosidades_tbc_wotlk musica` (armar) los une como siempre.

Uso (desde la carpeta del video):   python musica_wow.py
"""
import glob
import json
import os
import subprocess
import sys
from collections import Counter

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import lyria_tramos as lt  # noqa: E402
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion  # noqa: E402

TEMAS = json.load(open("audio/wow/_temas.json", encoding="utf-8"))   # zona -> [id, título, canal]
SR, LUFS, CRUCE, FUNDIDO = 48000, -20.0, 3.0, 0.4
FFMPEG = r"C:\ffmpeg\bin\ffmpeg.exe"


def wav_de(id_):
    """audio/wow/<id>.wav (lo convierte desde el bestaudio bajado si todavía no existe)."""
    w = f"audio/wow/{id_}.wav"
    if not os.path.exists(w):
        src = [f for f in glob.glob(f"audio/wow/{id_}.*") if not f.endswith(".wav")]
        assert src, f"falta el audio de {id_}: yt-dlp -f bestaudio -o 'audio/wow/%(id)s.%(ext)s' https://youtu.be/{id_}"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src[0], "-ac", "2", "-ar", str(SR), w], check=True)
    return w


def limpio(zona):
    """El tema sin huecos de silencio (ventanas de 0,5 s 25 dB bajo su RMS, ≥ 1,5 s seguidos), unido con fundidos cortos."""
    id_, nombre, _ = TEMAS[zona]
    x, sr = sf.read(wav_de(id_), always_2d=True)
    assert sr == SR, (id_, sr)
    m, w = x.mean(1), sr // 2
    n = len(m) // w
    db = 20 * np.log10(np.sqrt((m[:n * w].reshape(n, w) ** 2).mean(1)) + 1e-9)
    sil = db < 20 * np.log10(np.sqrt((m ** 2).mean()) + 1e-9) - 25
    partes, i0, i = [], 0, 0
    while i < n:
        if sil[i]:
            j = i
            while j < n and sil[j]:
                j += 1
            if j - i >= 3:
                if i > i0:
                    partes.append(x[i0 * w:i * w])
                i0 = j
            i = j
        else:
            i += 1
    if n > i0:
        partes.append(x[i0 * w:n * w])
    nf = int(FUNDIDO * sr)
    rampa = np.linspace(0, 1, nf)[:, None]
    for p in partes:
        p[:nf] *= rampa
        p[-nf:] *= rampa[::-1]
    y = np.vstack(partes).astype(np.float64)
    y *= 10 ** ((LUFS - pyln.Meter(sr).integrated_loudness(y)) / 20)
    print(f"{zona} · {nombre}: {len(x) / sr:.1f} s -> {len(y) / sr:.1f} s sin huecos ({len(partes)} partes)")
    return y.astype(np.float32)


def zona_de_tramo(ids):
    return Counter(guion.ZONA_DE[i] for i in ids).most_common(1)[0][0]


def main():
    asigna = [zona_de_tramo(ids) for ids, _ in lt.TRAMOS]
    print("tramos ->", asigna)
    temas = {z: limpio(z) for z in sorted(set(asigna))}
    pos = dict.fromkeys(temas, 0)
    for n, ((ids, _), z) in enumerate(zip(lt.TRAMOS, asigna), 1):
        t0, t1 = lt.limites(ids)
        largo = int(round((t1 - t0 + CRUCE + 0.5) * SR))
        y, p = temas[z], pos[z]
        seg = np.take(y, np.arange(p, p + largo) % len(y), axis=0)   # da la vuelta al tema si se acaba
        pos[z] = (p + largo) % len(y)
        sf.write(f"audio/lyria_tramo{n}.wav", seg, SR, subtype="FLOAT")
        print(f"tramo {n}: {t0:.0f}-{t1:.0f} s <- {TEMAS[z][1]} desde {p / SR:.0f} s")
    os.makedirs("salida", exist_ok=True)
    l = ["", "Música (banda sonora original de World of Warcraft, © Blizzard Entertainment):"]
    l += [f"- {nom} — https://youtu.be/{k} ({canal})" for z, (k, nom, canal) in TEMAS.items() if z in temas]
    open("audio/creditos_musica.txt", "w", encoding="utf-8").write("\n".join(l) + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
