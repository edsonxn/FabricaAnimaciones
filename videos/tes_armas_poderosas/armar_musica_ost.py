# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Skyrim (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Copiado de er_malenia_atrocidades. Pistas en audio/ost/
(yt-dlp de «Jeremy Soule - Topic»), NINGUNA de las que sonaron en tes_cosas_inutiles (Far Horizons, Out of the Cold, Ancient
Stones, Sky Above Voice Within): dragonborn 813-3iL5OsE · unbroken_road PAhZIQvJdlY · steel_on_steel X7PDqUbcgeU ·
blood_and_steel 0udsdFv2YQA · tundra sx3aFAfQrZA · secunda VPgZFgOvJDE · awake TIVpIo49WXo · kynes_peace LbNMvsSRThw ·
one_they_fear ez6jJHk3X4A · aurora SR1HOltzolY · death_or_sovngarde mctA-WlBbn0 · sovngarde c6q2t2GSJb8
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py tes_armas_poderosas mezcla`)
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
    ((0.0, 40.0), [("dragonborn", 0)]),                             # gancho: el tema del Sangre de Dragón
    ((40.0, 170.7), [("unbroken_road", 0)]),                        # 15 Viento Cortante · 14 Wabbajack (aventura)
    ((170.7, 288.0), [("steel_on_steel", 0), ("blood_and_steel", 0)]),   # 13 Sangreskal · 12 Molag Bal (combate)
    ((288.0, 394.7), [("tundra", 0)]),                              # 11 hacha rúnica · 10 Volendrung
    ((394.7, 509.3), [("secunda", 0), ("awake", 0)]),               # 9 Hoja de ébano · 8 Bastón de Magnus (noche, magia)
    ((509.3, 618.7), [("kynes_peace", 0)]),                         # 7 Quebrantadora · 6 Ruiseñor
    ((618.7, 728.0), [("one_they_fear", 0)]),                       # 5 Miraak · 4 Azote de dragones (dragones)
    ((728.0, 853.3), [("aurora", 0)]),                              # 3 Desgarradora gélida · 2 Arco de Auriel (hielo, luz)
    ((853.3, 941.3), [("death_or_sovngarde", 0)]),                  # 1 la daga que forjas tú
    ((941.3, None), [("sovngarde", 0)]),                            # cierre
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
