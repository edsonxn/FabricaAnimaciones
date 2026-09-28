# -*- coding: utf-8 -*-
"""Sintetizador: osciladores band-limited (PolyBLEP), filtros SVF con modulación por muestra,
envolventes, reverb por convolución, delay y dinámica. Todo a 48 kHz, float32/64."""
import math

import numpy as np
from numba import njit
from scipy.signal import fftconvolve, butter, sosfilt

SR = 48000


def mtof(m):
    return 440.0 * 2 ** ((np.asarray(m, dtype=np.float64) - 69) / 12)


# ------------------------------------------------------------ osciladores
@njit(cache=True)
def _polyblep(t, dt):
    if t < dt:
        t /= dt
        return t + t - t * t - 1.0
    if t > 1.0 - dt:
        t = (t - 1.0) / dt
        return t * t + t + t + 1.0
    return 0.0


@njit(cache=True)
def saw_blep(freq, sr, fase0):
    """freq: array de frecuencias por muestra."""
    n = freq.shape[0]
    out = np.empty(n)
    ph = fase0
    for i in range(n):
        dt = freq[i] / sr
        out[i] = 2.0 * ph - 1.0 - _polyblep(ph, dt)
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
    return out


@njit(cache=True)
def square_blep(freq, sr, fase0, pw):
    n = freq.shape[0]
    out = np.empty(n)
    ph = fase0
    for i in range(n):
        dt = freq[i] / sr
        v = 1.0 if ph < pw else -1.0
        v += _polyblep(ph, dt)
        p2 = ph - pw
        if p2 < 0.0:
            p2 += 1.0
        v -= _polyblep(p2, dt)
        out[i] = v
        ph += dt
        if ph >= 1.0:
            ph -= 1.0
    return out


def seno(freq, fase0=0.0):
    f = np.broadcast_to(np.asarray(freq, np.float64), np.shape(freq))
    return np.sin(2 * np.pi * (np.cumsum(f) / SR) + fase0)


def sierra(freq, fase0=0.0):
    return saw_blep(np.ascontiguousarray(freq, dtype=np.float64), float(SR), fase0)


def cuadrada(freq, pw=0.5, fase0=0.0):
    return square_blep(np.ascontiguousarray(freq, dtype=np.float64), float(SR), fase0, pw)


def supersaw(f0, n, voces=7, detune=0.18, seed=0):
    rng = np.random.default_rng(seed)
    offs = np.linspace(-1, 1, voces) * detune * 0.06
    L = np.zeros(n)
    R = np.zeros(n)
    for k, o in enumerate(offs):
        f = np.full(n, f0 * (1 + o * 0.25))
        s = sierra(f, rng.random())
        pan = 0.5 + 0.45 * (k / (voces - 1) - 0.5) * 2
        L += s * math.cos(pan * math.pi / 2)
        R += s * math.sin(pan * math.pi / 2)
    return np.stack([L, R]) / math.sqrt(voces)


def ruido(n, seed=0):
    return np.random.default_rng(seed).uniform(-1, 1, n)


# ------------------------------------------------------------ filtros
@njit(cache=True)
def svf(x, cutoff, q, modo):
    """Filtro de estado variable (TPT / Zavalishin). cutoff por muestra en Hz.
    modo 0=LP 1=BP 2=HP."""
    n = x.shape[0]
    out = np.empty(n)
    ic1 = 0.0
    ic2 = 0.0
    k = 1.0 / q
    for i in range(n):
        fc = cutoff[i]
        if fc > 20000.0:
            fc = 20000.0
        if fc < 20.0:
            fc = 20.0
        g = math.tan(math.pi * fc / 48000.0)
        a1 = 1.0 / (1.0 + g * (g + k))
        a2 = g * a1
        a3 = g * a2
        v3 = x[i] - ic2
        v1 = a1 * ic1 + a2 * v3
        v2 = ic2 + a2 * ic1 + a3 * v3
        ic1 = 2.0 * v1 - ic1
        ic2 = 2.0 * v2 - ic2
        if modo == 0:
            out[i] = v2
        elif modo == 1:
            out[i] = v1
        else:
            out[i] = x[i] - k * v1 - v2
    return out


def lp(x, fc, q=0.707):
    return svf(np.ascontiguousarray(x, np.float64), np.broadcast_to(np.asarray(fc, np.float64), x.shape).copy(), q, 0)


def bp(x, fc, q=1.0):
    return svf(np.ascontiguousarray(x, np.float64), np.broadcast_to(np.asarray(fc, np.float64), x.shape).copy(), q, 1)


def hp(x, fc, q=0.707):
    return svf(np.ascontiguousarray(x, np.float64), np.broadcast_to(np.asarray(fc, np.float64), x.shape).copy(), q, 2)


def butter_hp(x, fc, orden=2):
    sos = butter(orden, fc, "hp", fs=SR, output="sos")
    return sosfilt(sos, x, axis=-1)


def butter_lp(x, fc, orden=2):
    sos = butter(orden, fc, "lp", fs=SR, output="sos")
    return sosfilt(sos, x, axis=-1)


def peq(x, fc, gain_db, q=1.0):
    """Ecualizador paramétrico (biquad RBJ)."""
    A = 10 ** (gain_db / 40)
    w0 = 2 * math.pi * fc / SR
    alpha = math.sin(w0) / (2 * q)
    b0, b1, b2 = 1 + alpha * A, -2 * math.cos(w0), 1 - alpha * A
    a0, a1, a2 = 1 + alpha / A, -2 * math.cos(w0), 1 - alpha / A
    sos = np.array([[b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0]])
    return sosfilt(sos, x, axis=-1)


def shelf(x, fc, gain_db, alto=True):
    A = 10 ** (gain_db / 40)
    w0 = 2 * math.pi * fc / SR
    alpha = math.sin(w0) / 2 * math.sqrt(2)
    c = math.cos(w0)
    s = 1 if alto else -1
    b0 = A * ((A + 1) + s * (A - 1) * c + 2 * math.sqrt(A) * alpha)
    b1 = -2 * s * A * ((A - 1) + s * (A + 1) * c)
    b2 = A * ((A + 1) + s * (A - 1) * c - 2 * math.sqrt(A) * alpha)
    a0 = (A + 1) - s * (A - 1) * c + 2 * math.sqrt(A) * alpha
    a1 = 2 * s * ((A - 1) - s * (A + 1) * c)
    a2 = (A + 1) - s * (A - 1) * c - 2 * math.sqrt(A) * alpha
    sos = np.array([[b0 / a0, b1 / a0, b2 / a0, 1.0, a1 / a0, a2 / a0]])
    return sosfilt(sos, x, axis=-1)


# ------------------------------------------------------------ envolventes
def adsr(n, a, d, s, r, dur_nota):
    """n muestras totales; dur_nota = segundos hasta note-off."""
    t = np.arange(n) / SR
    env = np.where(t < a, t / max(a, 1e-4), s + (1 - s) * np.exp(-(t - a) / max(d, 1e-4)))
    off = dur_nota
    lvl_off = (off / max(a, 1e-4)) if off < a else s + (1 - s) * math.exp(-(off - a) / max(d, 1e-4))
    env = np.where(t >= off, lvl_off * np.exp(-(t - off) / max(r, 1e-4)), env)
    return env


def perc(n, ataque=0.002, caida=0.2):
    t = np.arange(n) / SR
    return np.minimum(1.0, t / ataque) * np.exp(-t / caida)


# ------------------------------------------------------------ efectos
def respuesta_reverb(dur=2.4, predelay=0.02, seed=11, brillo=6000.0):
    n = int(dur * SR)
    t = np.arange(n) / SR
    rng = np.random.default_rng(seed)
    ir = np.zeros((2, n + int(predelay * SR)))
    for c in range(2):
        r = rng.standard_normal(n) * np.exp(-t * 6.9 / dur)
        r = butter_lp(r, brillo, 2)
        r = butter_hp(r, 150, 2)
        # reflexiones tempranas
        for k in range(8):
            pos = int((0.007 + 0.011 * k + rng.random() * 0.006) * SR)
            if pos < n:
                r[pos] += (0.7 ** k) * (1 if rng.random() > 0.5 else -1) * 1.5
        ir[c, int(predelay * SR):] = r
    ir /= np.sqrt((ir ** 2).sum(axis=1, keepdims=True))
    return ir


_IR_CACHE = {}


def reverb(x, mezcla=0.25, dur=2.4, brillo=6000.0):
    """x estéreo (2, n). Devuelve wet+dry."""
    key = (dur, brillo)
    if key not in _IR_CACHE:
        _IR_CACHE[key] = respuesta_reverb(dur, brillo=brillo)
    ir = _IR_CACHE[key]
    mono = x.mean(axis=0)
    wet = np.stack([fftconvolve(mono, ir[0])[:x.shape[1]], fftconvolve(mono, ir[1])[:x.shape[1]]])
    return x * (1 - mezcla * 0.5) + wet * mezcla


def delay_pingpong(x, tiempo, feedback=0.4, mezcla=0.3, lp_fc=5000.0):
    d = int(tiempo * SR)
    n = x.shape[1]
    out = x.copy()
    eco = x.mean(axis=0)
    g = 1.0
    for k in range(1, 7):
        g *= feedback
        if k * d >= n:
            break
        eco = butter_lp(eco, lp_fc, 1)
        c = k % 2
        out[c, k * d:] += mezcla * g * eco[:n - k * d] / feedback * feedback
    return out


def panear(x, pan):
    """x mono -> estéreo con ley de potencia constante; pan en [-1, 1]."""
    a = (pan + 1) * math.pi / 4
    return np.stack([x * math.cos(a), x * math.sin(a)])


@njit(cache=True)
def _seguidor(x, at, rl):
    n = x.shape[0]
    out = np.empty(n)
    e = 0.0
    for i in range(n):
        v = abs(x[i])
        c = at if v > e else rl
        e = c * e + (1 - c) * v
        out[i] = e
    return out


def envolvente(x, ataque=0.005, liberacion=0.15):
    at = math.exp(-1 / (ataque * SR))
    rl = math.exp(-1 / (liberacion * SR))
    return _seguidor(np.ascontiguousarray(np.abs(x).max(axis=0) if x.ndim == 2 else np.abs(x), np.float64), at, rl)


def compresor(x, umbral_db=-18, ratio=3.0, ataque=0.005, liberacion=0.12, makeup_db=0.0):
    env = envolvente(x, ataque, liberacion)
    lvl = 20 * np.log10(env + 1e-9)
    sobre = np.maximum(0, lvl - umbral_db)
    gr = -sobre * (1 - 1 / ratio)
    g = 10 ** ((gr + makeup_db) / 20)
    return x * g


@njit(cache=True)
def _ganancia_limitador(pico, techo, look, rel):
    n = pico.shape[0]
    req = np.empty(n)
    for i in range(n):
        req[i] = techo / pico[i] if pico[i] > techo else 1.0
    # mínimo deslizante hacia adelante en [i, i+look] (deque monótona)
    mn = np.empty(n)
    dq = np.empty(n, np.int64)
    h = 0
    tl = 0
    j = 0
    for i in range(n):
        while j < n and j <= i + look:
            while tl > h and req[dq[tl - 1]] >= req[j]:
                tl -= 1
            dq[tl] = j
            tl += 1
            j += 1
        while dq[h] < i:
            h += 1
        mn[i] = req[dq[h]]
    # liberación exponencial (ataque instantáneo sobre el mínimo ya anticipado)
    g = np.empty(n)
    gg = 1.0
    for i in range(n):
        if mn[i] < gg:
            gg = mn[i]
        else:
            gg = rel * gg + (1.0 - rel) * mn[i]
        g[i] = gg
    # suavizado (media móvil de 'look' muestras) para que la ganancia llegue sin clics
    out = np.empty(n)
    acc = 0.0
    for i in range(n):
        acc += g[i]
        if i >= look:
            acc -= g[i - look]
        k = look if i >= look else i + 1
        out[i] = min(acc / k, g[i])
    return out


def limitador(x, techo_db=-1.2, lookahead=0.005, liberacion=0.08):
    techo = 10 ** (techo_db / 20)
    x = np.ascontiguousarray(x, np.float64)
    pico = np.abs(x).max(axis=0)
    look = int(lookahead * SR)
    g = _ganancia_limitador(pico, techo, look, math.exp(-1 / (liberacion * SR)))
    # la ganancia se calcula mirando hacia adelante: se aplica tal cual (ya anticipa el pico)
    return x * g


def saturar(x, drive=1.5):
    return np.tanh(x * drive) / math.tanh(drive)


def sumar(buf, señal, t, gain=1.0):
    """Suma señal (mono o estéreo) en buf estéreo (2, N) en el tiempo t (s)."""
    i0 = int(round(t * SR))
    if señal.ndim == 1:
        señal = np.stack([señal, señal])
    n = señal.shape[1]
    if i0 >= buf.shape[1] or i0 + n <= 0:
        return
    a = max(0, -i0)
    b = min(n, buf.shape[1] - i0)
    buf[:, i0 + a:i0 + b] += gain * señal[:, a:b]
