# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Majora's Mask (regla del usuario del 23-oct-2026: en Crónicas del gaming
va la música del juego, NUNCA Lyria; recordatorio expreso al empezar este video). Pistas originales de N64 en audio/ost/ (yt-dlp de
la lista «The Legend of Zelda: Majora's Mask (N64) - Complete Soundtrack», Nintendo Music Archive, PLWeCcixVkuYZ9Fun16eKi3x72flKKyL1s;
ids en mapa_clips.md). Una pista (o dos) por sección elegida por lo que cuenta; los cortes salen de timeline.json (t0 de cada escena).
Receta de er_malenia_atrocidades/armar_musica_ost.py: cada sección a -23 LUFS, fundidos cruzados de 2 s, rampa final.
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py majora_mask mezcla`)
"""
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
CRUCE = 2.0
LUFS = -23.0

# escena del guion -> pistas que la llenan en orden: (archivo de audio/ost, desde s)
SECCIONES = [
    ("intro", [("titulo", 0)]),                                  # gancho: tema del título
    ("origen", [("dia1", 0), ("observatorio", 0)]),             # cómo se hizo: Ciudad Reloj, primer día
    ("lore", [("apertura", 0), ("vendedor", 0), ("gigantes", 0)]),   # Skull Kid, el vendedor, los gigantes
    ("p12", [("dia2", 0)]),                                      # el cartero
    ("p11", [("campo", 0)]),                                     # canciones ocultas (el espantapájaros del campo)
    ("p10", [("fantasmas", 0), ("romani", 0)]),                  # «Ellos» y el rancho Romani
    ("p9", [("horas_finales", 0)]),                              # el guardado y la luna encima
    ("p8", [("dia3", 0), ("caja_musica", 0)]),                   # Anju y Kafei
    ("p7", [("bosque", 0)]),                                     # Skull Kid de Ocarina: el Bosque (canción de Saria)
    ("p6", [("pelea_mascara", 0)]),                              # la Fiera Deidad
    ("p5", [("curacion", 0), ("zora", 0)]),                      # Darmani y Mikau
    ("p4", [("palacio_deku", 0), ("elegia", 0)]),                # la máscara Deku y la Elegía del Vacío
    ("p3", [("sharp", 0), ("caja_musica", 30)]),                 # Ben Drowned
    ("p2", [("observatorio", 20)]),                              # el micrófono
    ("p1", [("ikana", 0), ("despedida", 0)]),                    # las cinco etapas del duelo
    ("cierre", [("creditos", 0)]),
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
    cortes = [(t0s[i], pistas) for i, pistas in SECCIONES]
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for k, (t0, pistas) in enumerate(cortes):
        t1 = cortes[k + 1][0] if k + 1 < len(cortes) else total
        largo = int((t1 - t0 + CRUCE) * SR)
        seg = np.zeros((0, 2))
        for n, desde in pistas:
            x = cargar(n)[int(desde * SR):]
            if len(seg):
                c = min(nc, len(seg), len(x))
                seg[-c:] = seg[-c:] * rampa(c, False) + x[:c] * rampa(c)
                seg = np.vstack([seg, x[c:]])
            else:
                seg = x
            if len(seg) >= largo:
                break
        while len(seg) < largo:                                  # si aún falta, repite la primera pista
            x = cargar(pistas[0][0])
            c = min(nc, len(seg), len(x))
            seg[-c:] = seg[-c:] * rampa(c, False) + x[:c] * rampa(c)
            seg = np.vstack([seg, x[c:]])
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
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(p for p, _ in pistas):30s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    main()
