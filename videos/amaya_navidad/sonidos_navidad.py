# -*- coding: utf-8 -*-
"""SFX sintetizados de amaya_navidad (bloques de sfx_proc.py + sonidos_base.py). Los eventos salen de escenas.EV, con las MISMAS
anclas que la animación. `python sfx_proc.py` arma audio/fx.wav; `--lista` los enumera."""
import numpy as np

from sfx_proc import SR, _rng, _t, barrido, boing, bp, destello, env, hp, lp, norm, osc, pop, ruido, whoosh
from sonidos_base import bajon, ficha, papel_


def _mezcla(*partes):
    n = max(len(p) for _, p in partes)
    out = np.zeros(n, np.float32)
    for i, p in partes:
        out[i:i + len(p)] += p[:max(0, n - i)]
    return out


def sello(seed=0):
    """Golpe seco de sello de goma + papel."""
    d = 0.35
    golpe = lp(ruido(d, seed), 700) * env(d, 0.001, 0.12) * 1.4 + osc(90, d) * env(d, 0.001, 0.15)
    return norm(golpe + papel_(seed)[:len(golpe)] * 0.25, 0.7)


def cae(seed=0):
    """Sticker que cae y rebota: «tup» suave + pop."""
    d = 0.22
    tup = osc(160, d) * env(d, 0.002, 0.1) + lp(ruido(d, seed), 1200) * env(d, 0.001, 0.05) * 0.4
    return norm(_mezcla((0, tup), (int(0.09 * SR), pop(seed, 900, 500, 0.1) * 0.5)), 0.5)


def pop_avatar(seed=0):
    return norm(_mezcla((0, boing(seed, 420, 880, 0.18)), (int(0.06 * SR), pop(seed + 1, 1300, 700, 0.1) * 0.6)), 0.5)


def letras(seed=0, n=6):
    """Recortes de papel que caen uno tras otro."""
    rg = _rng(seed)
    partes = []
    for k in range(n):
        x = bp(ruido(0.05, seed + k), 2500, 7000) * env(0.05, 0.001, 0.04)
        partes.append((int(k * rg.uniform(0.045, 0.07) * SR), x * rg.uniform(0.6, 1.0)))
    return norm(_mezcla(*partes), 0.4)


def etiqueta(seed=0):
    """Etiqueta de cartón que se columpia: tic + rozón."""
    return norm(_mezcla((0, ficha(seed, 1250)), (int(0.08 * SR), bp(ruido(0.3, seed), 800, 3000) * env(0.3, 0.05, 0.2) * 0.3)), 0.4)


def nota(seed=0):
    """Notita adhesiva que se pega."""
    d = 0.12
    return norm(bp(ruido(d, seed), 1500, 6000) * env(d, 0.002, 0.08) + osc(700, d) * env(d, 0.001, 0.05) * 0.3, 0.35)


def acierto(seed=0):
    out = np.zeros(int(1.2 * SR), np.float32)
    for k, f in enumerate((1046.5, 1568.0)):
        d = 0.3
        x = (osc(f, d, "tri") + 0.3 * osc(f * 2, d)) * env(d, 0.003, 0.22)
        i = int(k * 0.1 * SR)
        out[i:i + len(x)] += x
    dz = destello(seed)
    out[:len(dz)] += dz[:len(out)] * 0.5
    return norm(out, 0.5)


def tv(seed=0):
    """Estática de tele vieja (0,5 s) con zumbido."""
    d = 0.55
    x = hp(ruido(d, seed), 900) * 0.7 + osc(60, d, "saw") * 0.15
    return norm(x * env(d, 0.01, 0.15), 0.4)


def rasgado(seed=0):
    """Hoja de papel que se rasga."""
    d = 0.5
    t = _t(d)
    x = bp(ruido(d, seed), 1500, 8000) * (0.4 + 0.6 * (np.sin(2 * np.pi * 37 * t) > 0.2)) * env(d, 0.02, 0.3)
    return norm(x, 0.45)


def megafono(seed=0):
    """Pitidito de megáfono que se enciende."""
    d = 0.3
    return norm(osc(1900, d, "cuad") * env(d, 0.005, 0.25) * 0.3 + bp(ruido(d, seed), 1500, 2500) * env(d, 0.005, 0.2) * 0.3, 0.3)


def boing_triste(seed=0):
    return bajon(seed)


def cinta(seed=0):
    """Cinta adhesiva que se despega y se pega."""
    d = 0.45
    return norm(bp(ruido(d, seed), 600, 4000) * env(d, 0.25, 0.08) * (0.6 + 0.4 * np.sin(2 * np.pi * 60 * _t(d))), 0.4)


def misterio(seed=0):
    """Dos notas suaves de caja de música que dejan duda (mi-do#, pregunta)."""
    out = np.zeros(int(1.4 * SR), np.float32)
    for k, f in enumerate((1318.5, 1108.7)):
        d = 0.8
        x = (osc(f, d) + 0.2 * osc(f * 3, d)) * env(d, 0.003, 0.6)
        i = int(k * 0.32 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.4)


def ding(seed=0):
    d = 0.6
    return norm(sum(osc(f, d) * env(d, 0.002, 0.45 / (1 + j)) * (0.6 / (1 + j)) for j, f in enumerate((1760, 2640, 3960))), 0.4)


def corazones(seed=0):
    return norm(_mezcla(*[(int(k * 0.22 * SR), pop(seed + k, 700 + 120 * k, 1000 + 120 * k, 0.12)) for k in range(5)]), 0.4)


def clic(seed=0):
    """Clic de ratón: dos tics secos."""
    d = 0.05
    t1 = hp(ruido(d, seed), 2500) * env(d, 0.0005, 0.012)
    return norm(_mezcla((0, t1), (int(0.07 * SR), t1 * 0.6)), 0.5)


def campana(seed=0):
    """Campanita de notificación que se columpia (tres golpes)."""
    out = np.zeros(int(1.4 * SR), np.float32)
    for k in range(3):
        d = 0.9
        x = sum(osc(f, d) * env(d, 0.001, 0.5 / (1 + j)) * (0.6 / (1 + j)) for j, f in enumerate((1975.5, 2960, 4400)))
        i = int(k * 0.16 * SR)
        out[i:i + len(x)] += x * (1.0 - 0.25 * k)
    return norm(out, 0.45)


def flash(seed=0):
    """Obturador de cámara instantánea + motorcito que saca la foto."""
    d = 0.08
    obt = bp(ruido(d, seed), 1500, 6000) * env(d, 0.0005, 0.03)
    dm = 0.9
    motor = (osc(180, dm, "saw") * 0.3 + bp(ruido(dm, seed + 1), 300, 1400) * 0.4) * env(dm, 0.05, 0.6)
    return norm(_mezcla((0, obt), (int(0.06 * SR), obt * 0.7), (int(0.25 * SR), motor * 0.5)), 0.5)


def spray(seed=0):
    d = 0.55
    return norm(hp(ruido(d, seed), 3500) * env(d, 0.01, 0.4), 0.35)


def crujido(seed=0):
    """Algo que se quiebra (paleta de sombras)."""
    rg = _rng(seed)
    partes = [(int(rg.uniform(0, 0.25) * SR), bp(ruido(0.04, seed + k), 1200, 5000) * env(0.04, 0.0005, 0.02)) for k in range(9)]
    return norm(_mezcla(*partes), 0.5)


def lata(seed=0):
    """«Suena como lata»: golpe metálico hueco con zumbido."""
    d = 0.7
    x = sum(osc(f, d) * env(d, 0.001, 0.35) * a for f, a in ((523, 0.5), (1247, 0.4), (2311, 0.3), (3170, 0.2)))
    return norm(x + bp(ruido(d, seed), 2000, 6000) * env(d, 0.001, 0.05) * 0.5, 0.45)


def claqueta(seed=0):
    d = 0.18
    return norm(lp(ruido(d, seed), 3000) * env(d, 0.0005, 0.06) + osc(220, d) * env(d, 0.001, 0.08) * 0.5, 0.6)


def cajita(seed=0):
    """Tres notas de cajita de música (bocina que suena)."""
    out = np.zeros(int(1.3 * SR), np.float32)
    for k, f in enumerate((1046.5, 1318.5, 1568.0, 2093.0)):
        d = 0.6
        x = (osc(f, d) + 0.25 * osc(f * 2, d)) * env(d, 0.002, 0.35)
        i = int(k * 0.15 * SR)
        out[i:i + len(x)] += x
    return norm(out, 0.4)


SON = {
    "clic": clic, "campana": campana, "flash": flash, "spray": spray, "crujido": crujido, "lata": lata, "claqueta": claqueta,
    "cajita": cajita,
    "pop": lambda s: pop(s), "pop_avatar": pop_avatar, "cae": cae, "letras": letras, "sello": sello, "etiqueta": etiqueta,
    "nota": nota, "acierto": acierto, "bajon": bajon, "tv": tv, "rasgado": rasgado, "whoosh": lambda s: whoosh(0.6, s, 400, 2400),
    "destello": destello, "megafono": megafono, "boing_triste": boing_triste, "cinta": cinta, "misterio": misterio,
    "ding": ding, "corazones": corazones,
}


def pistas():
    import escenas
    ev = []
    for k, (t, nombre, vol, pan) in enumerate(escenas.EV):
        if nombre not in SON:
            raise KeyError(f"sonido sin síntesis: {nombre}")
        ev.append((t, SON[nombre](k), vol, max(-1.0, min(1.0, pan))))
    return ev
