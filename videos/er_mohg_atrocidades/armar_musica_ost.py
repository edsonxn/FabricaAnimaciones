# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Elden Ring (regla del usuario, 23-oct-2026: Runa Caída usa la música
del juego, no Lyria). Copia de er_melina_atrocidades/armar_musica_ost.py; los cortes salen de los t0 de timeline.json.
Pistas en audio/ost/ (bajar_ost.py; canales oficiales «- Topic»): tema = «Elden Ring» · margit = «Margit, the Fell Omen»
(Tsukasa Saitoh - Topic) · morgott = «Morgott, the Omen King» · leyndell = «Leyndell, Royal Capital» · godfrey = «Godfrey,
First Elden Lord» (Tai Tomisawa - Topic) · mohg = «Mohg, Lord of Blood» · frenesi = la Llama Frenética · mesa = «Roundtable Hold»
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py er_mohg_atrocidades mezcla`)
"""
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
CRUCE = 2.0          # fundido cruzado entre secciones (s)
LUFS = -23.0         # cada sección a la misma sonoridad (la mezcla luego la baja bajo la voz)

# (escena donde empieza, pistas en orden: (archivo, desde s)); la sección dura hasta la siguiente
SECCIONES = [
    ("intro", [("mohg", 0)]),                                   # gancho: «Mohg, Lord of Blood»
    ("p5", [("mesa", 0)]),                                      # #5 Varré y los Sinluz (la Mesa Redonda)
    ("p5b", [("godskin", 0)]),                                  # los Dedos Sangrientos (cazadores de los suyos)
    ("p4", [("omen", 0)]),                                      # #4 la sangre de una doncella
    ("p4b", [("frenesi", 0)]),                                  # la ceremonia del dedo
    ("p4c", [("mesa", 90)]),                                    # la Medalla y la muerte de Varré
    ("p3", [("omen", 30)]),                                     # #3 cirujanos y albináuricos
    ("p3b", [("godskin", 120)]),                                # la corte: nobles y panteón
    ("p2", [("malenia", 0)]),                                   # #2 Miquella robado; Malenia espera
    ("p2b", [("mohg", 60)]),                                    # el lago de sangre
    ("p1", [("astel", 0)]),                                     # #1 la Madre Informe, un dios exterior
    ("p1b", [("mohg", 130)]),                                   # Nihil y el plan de la dinastía
    ("p1c", [("mohg", 200)]),                                   # su muerte
    ("cierre", [("tema", 20)]),                                 # cierre
]


def cargar(n):
    x, sr = sf.read(os.path.join("audio", "ost", n + ".wav"), always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    return x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)


def rampa(n, sube=True):
    r = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    return np.sin(r * np.pi / 2)[:, None]


def main():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    total = float(tl["total"])
    t0s = {e["id"]: float(e["t0"]) for e in tl["escenas"]}
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for i, (esc, pistas) in enumerate(SECCIONES):
        t0 = 0.0 if i == 0 else t0s[esc]
        t1 = t0s[SECCIONES[i + 1][0]] if i + 1 < len(SECCIONES) else total
        largo = int((t1 - t0 + CRUCE) * SR)                         # se solapa CRUCE con la siguiente
        seg = np.zeros((0, 2))
        for n, desde in pistas:
            x = cargar(n)[int(desde * SR):]
            if len(seg):
                k = min(nc, len(seg), len(x))
                seg[-k:] = seg[-k:] * rampa(k, False) + x[:k] * rampa(k)
                seg = np.vstack([seg, x[k:]])
            else:
                seg = x
            if len(seg) >= largo:
                break
        while len(seg) < largo:                                       # si aún falta, repite la primera pista
            x = cargar(pistas[0][0])
            k = min(nc, len(seg), len(x))
            seg[-k:] = seg[-k:] * rampa(k, False) + x[:k] * rampa(k)
            seg = np.vstack([seg, x[k:]])
        seg = seg[:largo].copy()
        l = meter.integrated_loudness(seg)
        seg *= 10 ** ((LUFS - l) / 20)
        if t0 == 0:
            seg[:SR] *= rampa(SR)
        else:
            seg[:nc] *= rampa(nc)
        seg[-nc:] *= rampa(nc, False)
        i0 = int(max(0.0, t0 - CRUCE / 2) * SR) if t0 > 0 else 0
        out[i0:i0 + len(seg)] += seg[:len(out) - i0]
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(p for p, _ in pistas):24s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    main()
