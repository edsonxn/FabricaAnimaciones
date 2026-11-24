# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Elden Ring (regla del usuario, 23-oct-2026: Runa Caída usa la música
del juego, no Lyria). Molde: er_godfrey_atrocidades/armar_musica_ost.py, adaptado a er_rykard_atrocidades (22-nov-2026); los
cortes salen de los t0 de timeline.json.
Pistas en audio/ost/ (bajar_ost.py; canales oficiales «- Topic»): tema = «Elden Ring» · volcan = «Volcano Manor» · academia =
«Academy of Raya Lucaria» · liurnia = «Liurnia of the Lakes» · rykard = «God-Devouring Serpent» · mesa = «Roundtable Hold» ·
rennala = «Rennala, Queen of the Full Moon» · maliketh = «Beast Clergyman / Maliketh»
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py er_rykard_atrocidades mezcla`)
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
    ("intro", [("messmer", 0)]),                                # gancho: Messmer en lo alto (s_despojados con la voz callada)
    ("introb", [("sombra", 0)]),                                # el reino calcinado, los pedidos, Rico
    ("p5", [("sombra", 60)]),                                   # #5 sus caballeros: Fuego, el ojo arrancado
    ("p5b", [("catacumbas", 0)]),                               # Andreas y Huw en su tumba; el batallón penitenciario
    ("p4", [("rauh", 0)]),                                      # #4 Salza, el fuego prohibido, Rauh
    ("p4b", [("romina", 0)]),                                   # Hilde, el almacén, la iglesia; David y Quixilero
    ("p3", [("belurat", 0)]),                                   # #3 las bestias divinas colgadas
    ("p3b", [("leon", 0)]),                                     # el León Danzante y el canto de la anciana
    ("p3c", [("mesa", 0)]),                                     # Pascual y la IA
    ("p2", [("chaman", 0)]),                                    # #2 la anciana y la sopa
    ("p2b", [("enir", 0)]),                                     # el Cornamentado (s_cornamentado con la voz callada)
    ("p2c", [("enir", 60)]),                                    # su venganza, las almas, Leda, el mayal
    ("subs", [("mesa", 30)]),                                   # comentarios y campaña de suscripción
    ("p1", [("sombra", 0)]),                                    # #1 Queelign y la Insignia de cruzada
    ("p1b", [("messmer", 95)]),                                 # «despojado de luz» (s_madre_sanciona con la voz callada)
    ("p1c", [("messmer", 180)]),                                # la cruzada contra ti; Runa de Márika; Retos
    ("cierre", [("umbrio", 0)]),                                # la Bendición de Márika (s_maldicion con la voz callada)
    ("cierreb", [("tema", 0)]),                                 # cierre
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
