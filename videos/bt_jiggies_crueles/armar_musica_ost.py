"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Banjo-Tooie (Grant Kirkhope; regla del usuario, 23-oct-2026: en los
canales de videojuegos va la música del juego, no Lyria). No hay álbum oficial de Tooie en «Grant Kirkhope - Topic» (solo
Re-Jiggyed de BK): pistas ripeadas del juego en «Video-Game OST HQ» (ids en audio/ost/_catalogo.txt), en audio/ost/.
Una pista por puesto según lo que cuenta: el tema de Banjo en el gancho, Jiggywiggy en el contexto, el mundo o el jefe de
cada Jiggy («Racin' With Mary» para Canary Mary, «Ordinance Storage», «Vs. Mr. Patch»), los créditos en el cierre.
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py bt_jiggies_crueles mezcla`)
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

# (inicio, fin) de cada sección en el video y las pistas que la llenan en orden: (archivo, desde s)
SECCIONES = [
    ((0.0, 42.5), [("tema", 0)]),                    # gancho: Banjo's Theme
    ((42.5, 90.0), [("jiggywiggy", 0)]),             # contexto: Jiggywiggy's Temple
    ((90.0, 140.0), [("ccl", 0)]),                   # 10 Zubbas (Cloud Cuckooland)
    ((140.0, 187.5), [("funngames", 0)]),            # 9 olla de oro (prueba contrarreloj)
    ((187.5, 250.0), [("atlantis", 0)]),             # 8 Chris P. Bacon (Atlantis)
    ((250.0, 312.5), [("tdl", 0)]),                  # 7 Scrotty (Terrydactyland)
    ((312.5, 365.0), [("patch", 0)]),                # 6 Vs. Mr. Patch
    ((365.0, 407.5), [("jrl", 40)]),                 # 5 Lord Woo Fak Fak (Jolly Roger's Lagoon)
    ((407.5, 472.5), [("gi_dentro", 0)]),            # 4 Weldar (Grunty Industries, dentro de la fábrica)
    ((472.5, 522.5), [("ordnance", 0)]),             # 3 Ordinance Storage
    ((522.5, 575.0), [("gi", 0)]),                   # 2 Clinker's Cavern (Grunty Industries)
    ((575.0, 657.5), [("mary", 0)]),                 # 1 Racin' With Mary
    ((657.5, None), [("creditos", 0)]),              # cierre: Staff Credits
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
    total = float(tl.get("total") or tl.get("duracion") or max(e["fin"] for e in tl["escenas"]))
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for (t0, t1), pistas in SECCIONES:
        t1 = total if t1 is None else t1
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
