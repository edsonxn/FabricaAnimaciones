# -*- coding: utf-8 -*-
"""Popurrí de fondo con las 4 canciones grabadas por el propio grupo (regla del usuario, 22-oct-2026: nada de Lyria).
Bajo la voz suena el INSTRUMENTAL de cada pieza (Demucs htdemucs --two-stems vocals → audio/stems/htdemucs/A<n>/no_vocals.wav)
para que el canto no choque con el locutor. En las PAUSAS de solo música (guion.PAUSA: el locutor calla 9-10 s) entra la
canción completa con las voces del grupo: la escena anterior lleva el instrumental de LA MISMA pieza, corrido para que la
frase cantada caiga justo cuando calla el locutor (sin corte). En el cierre, igual: al terminar el locutor canta el grupo.
En «precio» la música se apaga con un pasa-bajos hasta «mil doscientos» y ahí vuelve de golpe.
    python musica_popurri.py        → audio/musica.wav (48 kHz estéreo, misma duración que timeline.json)
Piezas: A1 «La indita» (cumbia) · A2 balada grupera («Es tu amor…») · A3 corrido de Teodora (solo instrumental: la letra
habla de balazos) · A4 «Mis ojos me denuncian»."""
import json
import runpy

import librosa
import numpy as np
import soundfile as sf
from scipy.signal import butter, resample_poly, sosfilt

SR = 44100
ST = "audio/stems"
TL = json.load(open("timeline.json", encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}
PAUSA = runpy.run_path("guion.py")["PAUSA"]
GANANCIA_CANTO = 10 ** (2.5 / 20)        # las pausas suben un poco: ahí se luce el grupo


def palabra(esc, txt):
    for f in ESC[esc]["frases"]:
        for w in f["words"]:
            if w["w"].lower().strip("¿¡!?.,:").startswith(txt):
                return w["s"]
    raise KeyError(txt)


def fin_voz(esc):
    return ESC[esc]["frases"][-1]["t1"]


def inicio_pausa(esc):
    return fin_voz(esc) + 0.35


T_MIL = palabra("precio", "mil")
T0 = {k: ESC[k]["t0"] for k in ESC}
# (pieza, desde y hasta en la línea de tiempo, segundo de la pieza que suena en `desde`, desde cuándo entra el canto o None)
TRAMOS = [("A4", 0.0, T0["grupo"], 12.0, None)]                  # gancho: la intro instrumental de «Mis ojos me denuncian»
for esc, sig in (("grupo", "generos"), ("generos", "eventos"), ("eventos", "zona")):
    n, a, b = PAUSA[esc]
    tp = inicio_pausa(esc)
    TRAMOS.append((n, T0[esc], T0[sig], a - (tp - T0[esc]), tp))   # instrumental que desemboca en la frase cantada
TRAMOS += [
    ("A3", T0["zona"], T0["contacto"], 30.0, None),                 # zona + precio: el corrido (instrumental)
    ("A2", T0["contacto"], TOTAL, 90.30 - (fin_voz("cierre") + 0.25 - T0["contacto"]), fin_voz("cierre") + 0.25),
]                                                                   # contacto + cierre: desemboca en «Es tu amor…»
FUNDIDO = 0.18
_cache = {}


def pieza(n, stem):
    k = (n, stem)
    if k not in _cache:
        ruta = f"{ST}/htdemucs/{n}/{stem}.wav" if stem != "mix" else f"{ST}/{n}.wav"
        x, sr = sf.read(ruta, dtype="float32", always_2d=True)
        assert sr == SR, (ruta, sr)
        _cache[k] = x.T
    return _cache[k]


def pulsos(n):
    y = pieza(n, "no_vocals").mean(0)
    _, b = librosa.beat.beat_track(y=librosa.resample(y, orig_sr=SR, target_sr=22050), sr=22050, units="time")
    return np.asarray(b)


def rms(x):
    return float(np.sqrt(np.mean(x ** 2)) + 1e-9)


def main():
    n_tot = int(round(TOTAL * SR))
    out = np.zeros((2, n_tot), np.float32)
    for i, (n, t0, t1, desde, t_canto) in enumerate(TRAMOS):
        if t_canto is None:                                  # tramos sueltos: el corte cae en un pulso de la pieza
            b = pulsos(n)
            desde = float(b[np.argmin(np.abs(b - desde))])
        pre = FUNDIDO if i else 0.0
        a0, a1 = int(round((t0 - pre) * SR)), int(round(min(TOTAL, t1 + FUNDIDO) * SR))
        s0 = int(round((desde - pre) * SR))
        assert s0 >= 0, (n, desde)
        inst = pieza(n, "no_vocals")[:, s0:s0 + (a1 - a0)]
        seg = inst.copy()
        if t_canto is not None:                              # al callar el locutor entra la mezcla completa (con el canto)
            mix = pieza(n, "mix")[:, s0:s0 + (a1 - a0)]
            tt = (np.arange(seg.shape[1]) + a0) / SR
            u = np.clip((tt - t_canto) / 0.35, 0, 1)[None]
            seg = seg * (1 - u) + mix * GANANCIA_CANTO * u
        seg *= 0.10 / rms(pieza(n, "no_vocals")[:, s0:s0 + 10 * SR])   # mismo nivel entre piezas
        m = seg.shape[1]
        env = np.ones(m, np.float32)
        nf = int(FUNDIDO * 2 * SR)
        if i:
            env[:nf] = np.linspace(0, 1, nf)
        if t1 < TOTAL:
            env[-nf:] = np.minimum(env[-nf:], np.linspace(1, 0, nf))
        out[:, a0:a0 + m] += seg * env
        canto = f"canto desde {t_canto:6.2f}s (pieza {desde + t_canto - t0:6.2f}s)" if t_canto else "instrumental"
        print(f"{n} {t0:6.2f}-{t1:6.2f}  pieza desde {desde:6.2f}s  {canto}")
    # precio: «¿Y el precio?» con la música apagada por un pasa-bajos; vuelve de golpe en «mil doscientos»
    p0, p1 = int(T0["precio"] * SR), int(T_MIL * SR)
    sos = butter(4, 380, "low", fs=SR, output="sos")
    filt = sosfilt(sos, out[:, p0 - SR:p1], axis=1)[:, SR:] * 0.7
    u = np.clip(np.arange(p1 - p0) / (0.25 * SR), 0, 1)[None]
    out[:, p0:p1] = out[:, p0:p1] * (1 - u) + filt * u
    nf = int(1.6 * SR)
    out[:, -nf:] *= np.linspace(1, 0, nf) ** 1.5
    out[:, :int(0.02 * SR)] *= np.linspace(0, 1, int(0.02 * SR))
    out /= max(1.0, np.abs(out).max() / 0.95)
    out = resample_poly(out, 160, 147, axis=1).astype(np.float32)     # 44,1 → 48 kHz (el de la mezcla)
    sf.write("audio/musica.wav", out.T, 48000, subtype="PCM_24")
    print(f"audio/musica.wav {TOTAL:.2f}s · mil {T_MIL:.2f}")


if __name__ == "__main__":
    main()
