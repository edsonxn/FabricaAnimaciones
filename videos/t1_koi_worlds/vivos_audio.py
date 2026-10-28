# -*- coding: utf-8 -*-
"""audio/ambiente.wav = la narración ORIGINAL (español) de cada tramo EN VIVO, cortada de medios/_fuente con la misma
fuente y segundo que el FX `video` de efectos.py (VIVO): imagen y voz alineadas, duración exacta (lección del 28-oct: los
clips de yt-dlp con audio salían más cortos y el motor los estiraba). `video` borra ambiente.wav si ningún beat lleva
ambiente_por, así que esto se corre DESPUÉS de `video` y antes de `mezcla`. python videos/t1_koi_worlds/vivos_audio.py"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
SR = 48000          # el de nucleo/sinte.py (mezcla lo exige)
VIVOS = {"jugada1": ("g1_j2", 48), "jugada2": ("g1_j3", 42), "jugada3": ("g1_j4", 54), "jugada4": ("g1_j5", 52),
         "jugada5": ("g2_j1", 66), "jugada6": ("g2_j2", 40), "jugada7": ("g2_j3", 44)}
VOL_RMS = 0.075


def main():
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    es = {e["id"]: e for e in tl["escenas"]}
    N = int(tl["escenas"][-1]["t1"] * SR) + SR
    out = np.zeros((N, 2), np.float32)
    tmp = os.path.join(D, "audio", "_vivo_tmp.wav")
    for sid, (n, t) in VIVOS.items():
        e0, f0 = es[sid]["t0"], es[sid]["frases"][0]["t0"]
        dur = f0 - e0 + 0.6                                   # medio segundo de cola que se funde bajo la voz
        subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i",
                        os.path.join(D, "medios", "_fuente", n + ".mp4"), "-t", f"{dur:.3f}", "-vn", "-ar", str(SR), "-ac", "2",
                        tmp], check=True)
        x, _ = sf.read(tmp, always_2d=True, dtype="float32")
        x *= VOL_RMS / float(np.sqrt(np.mean(x ** 2)) + 1e-9)
        f = int(.25 * SR)
        x[:f] *= np.linspace(0, 1, f)[:, None]
        g = int(.9 * SR)
        x[-g:] *= np.linspace(1, 0, g)[:, None]
        i = int(e0 * SR)
        out[i:i + len(x)] += x[:N - i]
        print(f"{sid}: {n} desde {t} s · {e0:.2f}-{f0:.2f}")
    os.remove(tmp)
    out = np.tanh(out * 2.0) / 2.0
    sf.write(os.path.join(D, "audio", "ambiente.wav"), out, SR, subtype="PCM_16")
    print("audio/ambiente.wav listo")


if __name__ == "__main__":
    main()
