# -*- coding: utf-8 -*-
"""audio/ambiente.wav = la narración ORIGINAL (español) de cada tramo EN VIVO, cortada de medios/_fuente con la misma
fuente y segundo que el FX `video` de efectos.py (VIVO): imagen y voz alineadas, duración exacta (lección del 28-oct: los
clips de yt-dlp con audio salían más cortos y el motor los estiraba). `video` borra ambiente.wav si ningún beat lleva
ambiente_por, así que esto se corre DESPUÉS de `video` y antes de `mezcla`. python videos/lol_semana2/vivos_audio.py"""
import json
import os
import subprocess

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
SR = 48000          # el de nucleo/sinte.py (mezcla lo exige)
# (escena, ruta de la fuente, segundo inicial, e0, f0): lo escribe efectos.py al importarlo (AUD_VIVOS)
VIVOS = json.load(open(os.path.join(D, "investigacion", "vivos.json"), encoding="utf-8"))
VOL_RMS = 0.075


def main():
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    N = int(tl["escenas"][-1]["t1"] * SR) + SR
    out = np.zeros((N, 2), np.float32)
    tmp = os.path.join(D, "audio", "_vivo_tmp.wav")
    for sid, ruta, t, e0, f0 in VIVOS:
        dur = f0 - e0 + 0.6                                   # medio segundo de cola que se funde bajo la voz
        subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-ss", f"{t:.3f}", "-i", ruta, "-t", f"{dur:.3f}", "-vn",
                        "-ar", str(SR), "-ac", "2", tmp], check=True)
        x, _ = sf.read(tmp, always_2d=True, dtype="float32")
        if len(x) < 1.4 * SR:                                 # esa fuente se queda sin audio antes que el video: sin narración aquí
            print(f"{sid}: {os.path.basename(ruta)} desde {t} s · sin audio, se salta")
            continue
        x *= VOL_RMS / float(np.sqrt(np.mean(x ** 2)) + 1e-9)
        f = int(.25 * SR)
        x[:f] *= np.linspace(0, 1, f)[:, None]
        g = int(.9 * SR)
        x[-g:] *= np.linspace(1, 0, g)[:, None]
        i = int(e0 * SR)
        out[i:i + len(x)] += x[:N - i]
        print(f"{sid}: {os.path.basename(ruta)} desde {t} s · {e0:.2f}-{f0:.2f}")
    os.remove(tmp)
    out = np.tanh(out * 2.0) / 2.0
    sf.write(os.path.join(D, "audio", "ambiente.wav"), out, SR, subtype="PCM_16")
    print("audio/ambiente.wav listo")


if __name__ == "__main__":
    main()
