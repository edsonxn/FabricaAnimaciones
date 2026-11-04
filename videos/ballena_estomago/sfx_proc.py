# -*- coding: utf-8 -*-
"""SFX SINTETIZADOS POR CÓDIGO (pedido del usuario, 4-nov-2026: «SFX hechos por ti»): nada de ElevenLabs ni bibliotecas.
Cada sonido es una función numpy (osciladores, ruido filtrado, envolventes) y se ancla a las MISMAS palabras que la animación
(importa las anclas de los planos). Escribe audio/fx.wav (48 kHz, estéreo); `mezcla` lo suma con MEZCLA["fx"] de guion.py.

    python sfx_proc.py            arma audio/fx.wav
    python sfx_proc.py --lista    lista los eventos (segundo, sonido, volumen)
    python sfx_proc.py --muestras escribe previews/sfx_<nombre>.wav de cada sonido suelto
"""
import math
import os
import sys

import numpy as np
import soundfile as sf
from scipy.signal import butter, sosfilt

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

SR = 48000


# ------------------------------------------------------------ bloques básicos
def _t(dur):
    return np.arange(int(dur * SR)) / SR


def _rng(seed):
    return np.random.default_rng(seed)


def _filtro(x, tipo, f, orden=2):
    f = np.atleast_1d(f) / (SR / 2)
    f = np.clip(f, 1e-4, 0.999)
    return sosfilt(butter(orden, f if len(f) > 1 else f[0], tipo, output="sos"), x)


def lp(x, f, o=2):
    return _filtro(x, "lowpass", f, o)


def hp(x, f, o=2):
    return _filtro(x, "highpass", f, o)


def bp(x, f0, f1, o=2):
    return _filtro(x, "bandpass", [f0, f1], o)


def osc(freq, dur, forma="sin", fase=0.0):
    """Oscilador con frecuencia variable (array o número)."""
    n = int(dur * SR)
    f = np.broadcast_to(np.asarray(freq, float), (n,))
    ph = 2 * np.pi * np.cumsum(f) / SR + fase
    if forma == "sin":
        return np.sin(ph)
    if forma == "tri":
        return 2 / np.pi * np.arcsin(np.sin(ph))
    if forma == "cuad":
        return np.tanh(3 * np.sin(ph))
    if forma == "saw":
        return 2 * ((ph / (2 * np.pi)) % 1) - 1
    raise ValueError(forma)


def env(dur, a=0.005, d=None, curva=4.0):
    """Ataque lineal + caída exponencial (d = constante de caída; None = sostenido con salida suave)."""
    t = _t(dur)
    e = np.clip(t / max(a, 1e-4), 0, 1)
    if d is None:
        e *= np.clip((dur - t) / 0.05, 0, 1)
    else:
        e *= np.exp(-np.maximum(t - a, 0) / d)
    return e


def barrido(f0, f1, dur, exp=True):
    u = _t(dur) / dur
    return f0 * (f1 / f0) ** u if exp else f0 + (f1 - f0) * u


def ruido(dur, seed=0):
    return _rng(seed).normal(0, 1, int(dur * SR))


def norm(x, pico=0.8):
    m = np.abs(x).max()
    return x * (pico / m) if m > 0 else x


# ------------------------------------------------------------ sonidos
def burbuja(seed=0, grave=1.0):
    """«blup»: la resonancia de una burbuja sube de tono al despegarse (Minnaert)."""
    r = _rng(seed)
    dur = r.uniform(0.05, 0.11) * (1 + 0.6 * (grave - 1))
    f0 = r.uniform(380, 650) / grave
    x = osc(barrido(f0, f0 * r.uniform(2.0, 2.8), dur), dur) * env(dur, 0.003, dur * 0.35)
    return norm(x, r.uniform(0.35, 0.6))


def rafaga_burbujas(n=9, seed=0, dur=1.2):
    out = np.zeros(int(dur * SR) + SR // 4)
    r = _rng(seed)
    for k in range(n):
        b = burbuja(seed * 31 + k, r.uniform(0.8, 1.3))
        i = int(r.uniform(0, dur * 0.85) * SR)
        out[i:i + len(b)] += b * r.uniform(0.5, 1.0)
    return norm(out, 0.7)


def destello(seed=0):
    """Campanita de cristal: parciales inarmónicos que entran en arpegio + brillo de aire."""
    r = _rng(seed)
    dur = 1.6
    out = np.zeros(int(dur * SR))
    base = r.uniform(1900, 2300)
    for k, m in enumerate((1.0, 1.5, 2.0, 2.76, 3.0)):
        i = int(k * 0.035 * SR)
        d = dur - k * 0.035
        out[i:i + int(d * SR)] += osc(base * m * (1 + r.normal(0, 0.003)), d) * env(d, 0.002, 0.35 / (1 + 0.3 * k)) / (1 + 0.5 * k)
    out += hp(ruido(dur, seed), 7000) * env(dur, 0.01, 0.25) * 0.08
    return norm(out, 0.55)


def pop(seed=0, f0=950, f1=420, dur=0.16):
    x = osc(barrido(f0, f1, dur), dur, "tri") * env(dur, 0.002, 0.05)
    n = int(0.012 * SR)
    x[:n] += lp(ruido(0.012, seed), 3000)[:n] * 0.4 * np.linspace(1, 0, n)          # clic del «pop»
    return norm(x, 0.6)


def boing(seed=0, f0=330, f1=620, dur=0.32):
    """«¡!»: resorte cómico que sube con vibrato."""
    f = barrido(f0, f1, dur) * (1 + 0.06 * np.sin(2 * np.pi * 18 * _t(dur)))
    return norm(osc(f, dur, "tri") * env(dur, 0.004, 0.12), 0.55)


def signo(seed=0):
    """«?»: dos notas de pizzicato que preguntan (la segunda más alta)."""
    a = osc(660, 0.14, "tri") * env(0.14, 0.002, 0.04)
    b = osc(880, 0.2, "tri") * env(0.2, 0.002, 0.06)
    out = np.zeros(int(0.36 * SR))
    out[:len(a)] += a
    out[int(0.12 * SR):int(0.12 * SR) + len(b)] += b
    return norm(out, 0.5)


def bip(seed=0, f=1320, dur=0.07, dos=True):
    """Kuri: pitido de robot."""
    x = osc(f, dur, "cuad") * env(dur, 0.002, dur * 0.6)
    if not dos:
        return norm(lp(x, 5000), 0.35)
    y = osc(f * 1.335, dur, "cuad") * env(dur, 0.002, dur * 0.6)
    out = np.zeros(int((dur * 2 + 0.04) * SR))
    out[:len(x)] += x
    out[int((dur + 0.04) * SR):int((dur + 0.04) * SR) + len(y)] += y
    return norm(lp(out, 5000), 0.35)


def canto_ballena(seed=0, dur=2.6, f0=210, f1=120):
    """Gemido de ballena: tono grave que baja con vibrato lento y armónicos, filtrado como bajo el agua."""
    t = _t(dur)
    u = t / dur
    f = (f0 * (1 - u) + f1 * u + 25 * np.sin(np.pi * u)) * (1 + 0.025 * np.sin(2 * np.pi * 4.2 * t))
    x = sum(osc(f * k, dur) / k ** 1.3 for k in (1, 2, 3, 4))
    e = np.sin(np.pi * np.clip(u, 0, 1)) ** 0.7
    return norm(lp(x * e, 900, 3), 0.8)


def retumbo(dur=2.0, seed=0):
    """Sombra enorme que se acerca: sub grave + ruido muy filtrado que crece."""
    t = _t(dur)
    e = (t / dur) ** 1.6
    x = osc(38 + 8 * t / dur, dur) * 0.8 + osc(57, dur) * 0.3 + lp(ruido(dur, seed), 140, 3) * 2.5
    return norm(x * e, 0.9)


def trago(seed=0):
    """GULP grande: caída de tono grave + golpe húmedo + burbuja gorda."""
    dur = 0.75
    x = osc(barrido(190, 42, 0.5), 0.5) * env(0.5, 0.01, 0.2)
    out = np.zeros(int(dur * SR))
    out[:len(x)] += x
    n = lp(ruido(0.3, seed), 500, 3) * env(0.3, 0.005, 0.07) * 2
    out[:len(n)] += n
    b = burbuja(seed + 5, grave=3.2) * 1.4
    i = int(0.18 * SR)
    out[i:i + len(b)] += b
    return norm(out, 0.95)


def glup(seed=0):
    """«¡GLUP!» de fuera: tres bloops que bajan."""
    out = np.zeros(int(0.7 * SR))
    for k, f in enumerate((520, 400, 300)):
        d = 0.14
        x = osc(barrido(f, f * 1.9, d), d) * env(d, 0.003, 0.05)
        i = int(k * 0.16 * SR)
        out[i:i + len(x)] += x * (1 - 0.15 * k)
    return norm(lp(out, 2500), 0.75)


def latido(seed=0):
    out = np.zeros(int(0.7 * SR))
    for k, (i, a) in enumerate(((0.0, 1.0), (0.24, 0.65))):
        d = 0.22
        x = osc(barrido(70, 42, d), d) * env(d, 0.004, 0.06) * a
        j = int(i * SR)
        out[j:j + len(x)] += x
    return norm(lp(out, 300), 0.8)


def whoosh(dur=0.6, seed=0, f0=300, f1=2600):
    t = _t(dur)
    n = ruido(dur, seed)
    out = np.zeros_like(n)
    trozos = 12
    for k in range(trozos):          # filtro de banda que barre (por trozos con solape)
        a, b = int(k * len(n) / trozos), int((k + 1) * len(n) / trozos)
        fc = f0 * (f1 / f0) ** (k / (trozos - 1))
        out[a:b] = bp(n, fc * 0.7, min(fc * 1.4, 20000))[a:b]
    e = np.sin(np.pi * t / dur) ** 2
    return norm(out * e, 0.5)


def ambiente_agua(dur, seed=0):
    """Cama submarina: rumor grave que respira + burbujitas lejanas."""
    t = _t(dur)
    x = lp(ruido(dur, seed), 260, 3) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.17 * t))
    x = norm(x, 0.35)
    r = _rng(seed)
    for k in range(int(dur * 2.2)):
        b = burbuja(seed + 100 + k, r.uniform(0.7, 1.5)) * r.uniform(0.05, 0.16)
        i = int(r.uniform(0, dur - 0.2) * SR)
        x[i:i + len(b)] += b
    return x


# ------------------------------------------------------------ pistas
def pistas():
    """(segundo, sonido(array), volumen, paneo -1..1)"""
    import plano_gancho as G
    P = []

    def add(t, x, v=1.0, pan=0.0):
        P.append((t, x, v, pan))

    # GANCHO
    add(0.0, ambiente_agua(G.T_NEGRO + 0.2, 1), 0.9)
    k = 0
    tb = 0.0
    while tb < G.T_NEGRO:                          # una burbuja por cada una que sale del regulador
        if k % 2 == 0:
            add(tb + 0.05, burbuja(200 + k), 0.35, -0.25)
        k += 1
        tb = k * 0.33
    add(G.tTanque - 0.05, destello(3), 0.8, -0.35)
    add(G.tAire, rafaga_burbujas(8, 4), 0.85, -0.2)
    add(G.tPronto - 0.3, retumbo(G.tTodo + 0.6 - G.tPronto + 0.3, 5), 1.0)
    add(G.tPronto, boing(6), 0.7, 0.45)
    add(G.tPronto + 0.05, bip(7, 1500), 0.5, 0.45)
    add(G.tPronto + 0.25, canto_ballena(8, 2.4), 0.9)
    add(G.tTodo + 0.9, trago(9), 1.0)
    add(G.T_NEGRO + 0.15, latido(10), 0.8)
    add(G.T_NEGRO + 0.5, bip(11, 1100, 0.06, dos=False), 0.4, 0.45)
    add(G.T_FUERA - 0.05, whoosh(0.7, 12, 250, 1800), 0.6)
    add(G.T_FUERA, ambiente_agua(G.T_FIN - G.T_FUERA + 0.4, 13), 0.8)
    add(G.tBallena + 0.05, signo(14), 0.6, -0.5)
    add(G.tTragar - 0.1, glup(15), 1.0)
    add(G.tTragar + 0.4, canto_ballena(16, 1.6, 170, 140), 0.45, 0.2)

    try:
        import plano_resto as R
        P += R.sonidos(sys.modules[__name__])
    except ImportError:
        pass
    return P


def armar():
    from comun import TOTAL
    N = int(TOTAL * SR) + SR
    out = np.zeros((2, N), np.float32)
    for (t, x, v, pan) in pistas():
        i = int(max(0, t) * SR)
        x = np.asarray(x, np.float32)[:max(0, N - i)] * v
        gl, gr = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
        out[0, i:i + len(x)] += x * gl * 1.41
        out[1, i:i + len(x)] += x * gr * 1.41
    pico = np.abs(out).max()
    if pico > 0.98:
        out *= 0.98 / pico
    os.makedirs("audio", exist_ok=True)
    sf.write("audio/fx.wav", out[:, :int(TOTAL * SR)].T, SR, subtype="FLOAT")
    print(f"audio/fx.wav: {len(pistas())} eventos, pico {pico:.2f}")


if __name__ == "__main__":
    if "--lista" in sys.argv:
        for (t, x, v, pan) in sorted(pistas(), key=lambda p: p[0]):
            print(f"{t:7.2f}  {len(x) / SR:5.2f} s  vol {v:.2f}  pan {pan:+.2f}")
    elif "--muestras" in sys.argv:
        for nombre, fn in (("burbuja", burbuja), ("destello", destello), ("boing", boing), ("signo", signo), ("bip", bip),
                           ("canto", canto_ballena), ("retumbo", retumbo), ("trago", trago), ("glup", glup), ("latido", latido),
                           ("whoosh", whoosh)):
            sf.write(f"previews/sfx_{nombre}.wav", fn().astype(np.float32), SR)
    else:
        armar()
