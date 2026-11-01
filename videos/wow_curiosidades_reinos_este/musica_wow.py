"""Música ORIGINAL de World of Warcraft en lugar de Lyria (el usuario, 18-oct-2026; excepción solo para este video).

4 temas de zona bajados con yt-dlp (solo audio) a audio/wow/<id>.wav. Este script les quita los huecos de silencio
(la taberna trae ~6 s entre pieza y pieza), los iguala en sonoridad (LUFS) y corta para cada tramo de `LYRIA.tramos` la
pieza audio/lyria_tramoN.wav con la duración justa (+ el cruce de 3 s); cada tema sigue donde se quedó la vez anterior,
así no se repite el mismo pasaje. Luego `python fab.py wow_curiosidades_reinos_este musica` (armar) los une como siempre.

Uso (desde la carpeta del video):   python musica_wow.py
"""
import os
import sys

import numpy as np
import pyloudnorm as pyln
import soundfile as sf

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import lyria_tramos as lt  # noqa: E402

TEMAS = {   # id de YouTube: (nombre, canal) -> créditos
    "MDMa49NrQPM": ("Elwynn Forest", "Release - Topic"),
    "bGCKLFsDDVw": ("Tavern (Human)", "ilikesmecookies"),
    "2ncJktFwb5E": ("Duskwood", "Agostini"),
    "IwlPgQtGguw": ("Tirisfal Glades", "Wowmusicable"),
}
E, T, D, TI = TEMAS
ASIGNA = [E, T, D, TI, E, T, TI, T, D, TI, D, E]   # un tema por tramo (12), según el ánimo de sus curiosidades
SR, LUFS, CRUCE, FUNDIDO = 48000, -20.0, 3.0, 0.4


def limpio(id_):
    """El tema sin huecos de silencio (ventanas de 0,5 s 25 dB bajo su RMS, ≥ 1,5 s seguidos), unido con fundidos cortos."""
    x, sr = sf.read(f"audio/wow/{id_}.wav", always_2d=True)
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
    print(f"{TEMAS[id_][0]}: {len(x) / sr:.1f} s -> {len(y) / sr:.1f} s sin huecos ({len(partes)} partes)")
    return y.astype(np.float32)


def main():
    assert len(ASIGNA) == len(lt.TRAMOS), (len(ASIGNA), len(lt.TRAMOS))
    temas = {k: limpio(k) for k in TEMAS}
    pos = dict.fromkeys(TEMAS, 0)
    for n, ((ids, _), k) in enumerate(zip(lt.TRAMOS, ASIGNA), 1):
        t0, t1 = lt.limites(ids)
        largo = int(round((t1 - t0 + CRUCE + 0.5) * SR))
        y, p = temas[k], pos[k]
        seg = np.take(y, np.arange(p, p + largo) % len(y), axis=0)   # da la vuelta al tema si se acaba
        pos[k] = (p + largo) % len(y)
        sf.write(f"audio/lyria_tramo{n}.wav", seg, SR, subtype="FLOAT")
        print(f"tramo {n}: {t0:.0f}-{t1:.0f} s <- {TEMAS[k][0]} desde {p / SR:.0f} s")
    os.makedirs("salida", exist_ok=True)
    l = ["", "Música (banda sonora original de World of Warcraft, © Blizzard Entertainment):"]
    l += [f"- {nom} — https://youtu.be/{k} ({canal})" for k, (nom, canal) in TEMAS.items()]
    open("audio/creditos_musica.txt", "w", encoding="utf-8").write("\n".join(l) + "\n")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
