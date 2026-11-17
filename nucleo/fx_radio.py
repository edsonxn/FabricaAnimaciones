# -*- coding: utf-8 -*-
"""Filtro «radio del Yermo» (Radio Yermo, 17-nov-2026): la voz como sale de una radio vieja en los Fallout.
Idea del usuario: «una combinación entre la radio del Yermo y un narrador… con esos filtros y esa forma como se escucha la del juego».

    import fx_radio as R
    y = R.radio(x, sr)                 # radio completa: banda de AM, saturación de válvula, siseo, chasquidos y zumbido
    y = R.tinte(x, sr)                 # narrador con un toque de radio (inteligible durante 15 min)
    y = R.mezcla(x, sr, corte_s)       # radio hasta corte_s y luego el narrador se acerca al micrófono (fundido de 1,2 s)
    y = R.sintonia(sr) + y             # estática con silbido de sintonía antes de la voz (0,9 s)

Todo mono float32 -1..1. Sin dependencias raras: numpy + scipy.signal.
"""
import numpy as np
from scipy import signal


def _banda(x, sr, lo, hi, orden=4):
    sos = signal.butter(orden, [lo, hi], btype="band", fs=sr, output="sos")
    return signal.sosfilt(sos, x)


def _pico(x, sr, f, q, db):
    b, a = signal.iirpeak(f, q, fs=sr)
    return x + (10 ** (db / 20) - 1) * signal.lfilter(b, a, x)


def _norm(x, pico=0.89):
    m = np.max(np.abs(x)) or 1.0
    return (x / m * pico).astype(np.float32)


def _ruido(n, sr, nivel, rng, chasquidos=True, zumbido=True):
    hiss = _banda(rng.standard_normal(n), sr, 900, 6000, 2) * nivel
    if zumbido:                                             # zumbido de red de 60 Hz y su armónico, muy bajito
        t = np.arange(n) / sr
        hiss += (np.sin(2 * np.pi * 60 * t) * 0.6 + np.sin(2 * np.pi * 120 * t) * 0.4) * nivel * 0.35
    if chasquidos:                                          # polvo/estática: impulsos cortos al azar
        k = rng.random(n) < 7.0 / sr
        imp = np.zeros(n)
        imp[k] = rng.choice([-1, 1], k.sum()) * rng.uniform(0.3, 1.0, k.sum())
        imp = signal.lfilter([1], [1, -0.82], imp)
        hiss += _banda(imp, sr, 700, 5000, 2) * nivel * 9
    return hiss


def radio(x, sr, sem=1, nivel_ruido=0.012):
    """Radio vieja: banda 320-3300 Hz, nasal en 1,6 kHz, válvula saturada, un poco de compresión, siseo + chasquidos."""
    rng = np.random.default_rng(sem)
    y = _banda(x, sr, 320, 3300, 4)
    y = _pico(y, sr, 1600, 1.2, 5)
    y = _norm(y, 1.0)
    y = np.tanh(y * 2.4) / np.tanh(2.4)                     # saturación de válvula
    t = np.arange(len(y)) / sr
    y = y * (1 + 0.025 * np.sin(2 * np.pi * 0.45 * t))     # leve vaivén de la señal (onda media)
    y = _banda(y, sr, 300, 3500, 2)                         # la saturación crea agudos: se recortan otra vez
    y = _norm(y, 0.8) + _ruido(len(y), sr, nivel_ruido, rng)
    return _norm(y)


def tinte(x, sr, sem=2):
    """Narrador con un toque de radio: graves y agudos recortados suave, algo de presencia y un siseo apenas audible."""
    rng = np.random.default_rng(sem)
    y = _banda(x, sr, 110, 7200, 2)
    y = _pico(y, sr, 2200, 0.9, 3)
    y = _norm(y, 1.0)
    y = np.tanh(y * 1.3) / np.tanh(1.3)
    y = _norm(y, 0.85) + _ruido(len(y), sr, 0.0035, rng, chasquidos=True, zumbido=False)
    return _norm(y)


def mezcla(x, sr, corte_s, fundido=1.2, sem=3):
    """Radio hasta corte_s y después el narrador limpio (con tinte), con fundido; el siseo se apaga despacio."""
    a, b = radio(x, sr, sem), tinte(x, sr, sem + 1)
    n = len(x)
    i0 = int(max(0, corte_s - fundido / 2) * sr)
    i1 = min(n, i0 + int(fundido * sr))
    g = np.zeros(n, np.float32)
    g[i1:] = 1
    g[i0:i1] = 0.5 - 0.5 * np.cos(np.linspace(0, np.pi, i1 - i0))
    return _norm(a * (1 - g) + b * g)


def sintonia(sr, dur=0.9, sem=4):
    """Estática con el silbido de alguien moviendo el dial hasta encontrar la estación."""
    rng = np.random.default_rng(sem)
    n = int(dur * sr)
    t = np.arange(n) / sr
    f = 2600 - 1900 * (t / dur) ** 0.6
    silbido = np.sin(2 * np.pi * np.cumsum(f) / sr) * 0.22 * (1 - t / dur)
    estatica = _banda(rng.standard_normal(n), sr, 400, 4500, 2) * 0.35
    env = np.minimum(1, t / 0.05) * np.clip((dur - t) / 0.25, 0, 1)
    return (_norm(silbido + estatica, 0.5) * env).astype(np.float32)
