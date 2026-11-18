# -*- coding: utf-8 -*-
"""Mete silencios DENTRO de las frases ya grabadas (sin regenerar voz) para que el VOD corra a x1 y cada muerte caiga cuando la voz la
nombra (regla «nunca cámara rápida», 31-oct-2026). guion.ESPACIOS_VOZ = {frase: [(palabra, aparición, segundos), …]}: silencio ANTES de
esa palabra; "$ini" = antes de la primera, "$fin" = después de la última. Corta en el punto de menos energía entre las dos palabras.
Reescribe voz/final/<frase>.wav y voz/palabras.json; el original queda en voz/final_orig/. Se puede repetir: siempre parte del original.
OJO: `seleccionar` (acto B) rehace voz/final y palabras.json: tras él, correr esto otra vez y luego `tiempo`.
python videos/lol_final_previa/espaciar_voz.py"""
import json
import os
import re
import shutil
import sys
import unicodedata

import numpy as np
import soundfile as sf

D = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, D)
from guion import ESPACIOS_VOZ  # noqa: E402

PAL = os.path.join(D, "voz", "palabras.json")
ORIG = os.path.join(D, "voz", "final_orig")
os.makedirs(ORIG, exist_ok=True)
FUNDIDO = .012
MARGEN = .06                                       # voz a salvo a cada lado del corte
ANCHO_MIN = 2 * MARGEN                             # la pausa real debe dar ese margen


def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))


def indice(words, palabra, n):
    p = norm(palabra)
    hits = [i for i, w in enumerate(words) if norm(w["w"]).startswith(p)]
    if len(hits) <= n:
        raise KeyError(f"no encuentro «{palabra}» ({n}) en: {' '.join(w['w'] for w in words)}")
    return hits[n]


def envolvente(x, sr):
    """(energía en dB cada 5 ms, salto en s, umbral de silencio = 28 dB bajo la voz fuerte de la frase)"""
    hop = int(.005 * sr)
    m = x.mean(axis=1)
    env = 10 * np.log10(np.convolve(m ** 2, np.ones(2 * hop) / (2 * hop), mode="same")[::hop] + 1e-10)
    return env, hop / sr, np.percentile(env, 90) - 28


def pausa(env, hop, umbral, e_ant, s_sig):
    """la pausa REAL más ancha que toca el hueco entre dos palabras: (centro en s, ancho en s). Sin pausa: ancho 0."""
    a, b = max(int((e_ant - .12) / hop), 0), min(int((s_sig + .12) / hop), len(env) - 1)
    mejor, k = (0.0, 0.0), a
    while k <= b:
        if env[k] < umbral:
            f = k
            while f + 1 < len(env) and env[f + 1] < umbral:
                f += 1
            i = k
            while i > 0 and env[i - 1] < umbral:
                i -= 1
            if (f - i + 1) * hop > mejor[1]:
                mejor = ((i + f + 1) / 2 * hop, (f - i + 1) * hop)
            k = f + 1
        else:
            k += 1
    return mejor


def espaciar(key, spec, pal):
    ruta, copia = os.path.join(D, "voz", "final", key + ".wav"), os.path.join(ORIG, key + ".wav")
    p = pal[key]
    if p.get("espaciado"):                        # ya espaciada: se rehace desde el original y sus tiempos
        p.update(p.pop("espaciado"))
    else:
        shutil.copy2(ruta, copia)
    x, sr = sf.read(copia, always_2d=True)
    sub = sf.info(copia).subtype
    words = p["words"]
    env, hop, umbral = envolvente(x, sr)
    pos = []                                      # (índice de palabra, muestra, segundos)
    for palabra, n, seg, *t in spec:
        if palabra == "$ini":
            pos.append((0, 0, seg, None))
        elif palabra == "$fin":
            pos.append((len(words), len(x), seg, None))
        else:
            i = indice(words, palabra, n)
            c, ancho = pausa(env, hop, umbral, *(t * 2 or (words[i - 1]["e"], words[i]["s"])))
            if ancho < ANCHO_MIN:                 # nunca dentro de una palabra: mover el corte a una pausa natural de la frase
                raise SystemExit(f"{key}: sin pausa real antes de «{palabra}» ({ancho * 1000:.0f} ms); elige otro punto en ESPACIOS_VOZ")
            pos.append((i, int(c * sr), seg, (c - ancho / 2, c + ancho / 2)))
    pos.sort(key=lambda q: q[:2])
    trozos, ult, f = [], 0, int(FUNDIDO * sr)
    for _, m, seg, _p in pos:
        tr = x[ult:m].copy()
        if len(tr) > 2 * f:
            tr[:f] *= np.linspace(0, 1, f)[:, None] if ult else 1
            tr[-f:] *= np.linspace(1, 0, f)[:, None]
        trozos += [tr, np.zeros((int(round(seg * sr)), x.shape[1]))]
        ult = m
    tr = x[ult:].copy()
    if len(tr) > f:
        tr[:f] *= np.linspace(0, 1, f)[:, None]
    trozos.append(tr)
    sf.write(ruta, np.concatenate(trozos), sr, subtype=sub)
    guarda = dict(dur=p["dur"], words=[dict(w) for w in words])
    extra = [0.0] * (len(words) + 1)
    for i, _, seg, pz in pos:
        if pz:                                    # los tiempos de palabra fallan: junto al corte manda la pausa medida
            words[i - 1]["e"] = min(words[i - 1]["e"], round(pz[0], 3))
            words[i]["s"] = max(words[i]["s"], round(pz[1], 3))
            words[i]["e"] = max(words[i]["e"], words[i]["s"] + .1)
        for k in range(i, len(words) + 1):
            extra[k] += seg
    for k, w in enumerate(words):
        w["s"] = round(w["s"] + extra[k], 3)
        w["e"] = round(w["e"] + extra[k], 3)
    p["dur"] = round(p["dur"] + sum(q[2] for q in pos), 3)
    p["espaciado"] = guarda
    print(f"{key}: +{sum(q[2] for q in pos):.2f} s")


def main():
    pal = json.load(open(PAL, encoding="utf-8"))
    for key, p in pal.items():                    # frase que ya no lleva espacios: vuelve a su original
        if p.get("espaciado") and key not in ESPACIOS_VOZ:
            p.update(p.pop("espaciado"))
            shutil.copy2(os.path.join(ORIG, key + ".wav"), os.path.join(D, "voz", "final", key + ".wav"))
    for key, spec in ESPACIOS_VOZ.items():
        espaciar(key, spec, pal)
    json.dump(pal, open(PAL, "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    print("total", round(sum(q[2] for spec in ESPACIOS_VOZ.values() for q in spec), 1), "s de silencios")


if __name__ == "__main__":
    main()
