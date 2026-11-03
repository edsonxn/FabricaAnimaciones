"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Modern Warfare 4 (Stephen Barton; regla del usuario del 23-oct-2026:
en los canales de videojuegos va la música del juego, NUNCA Lyria). Pistas en audio/ost/ (`_catalogo.txt`, `_bajar.sh`; álbum
oficial en «Stephen Barton - Topic» y su resubida completa en modENASh1). Receta de bt_mundos_ranking: cada sección a -23 LUFS,
fundidos cruzados de 2 s; la banda sonora se APARTA en los beats con sonido original (guion.SECUENCIA["ambiente_por"]).
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py cod_mw4_secretos mezcla`)
"""
import json
import os
import subprocess
import sys

import numpy as np

SR = 48000
CRUCE = 2.0
LUFS = -23.0
APARTA_DB = -14.0       # la banda sonora baja esto donde suena el juego (beats con ambiente_por en guion.SECUENCIA)

# escena del guion -> pistas que la llenan en orden: (slug, desde s)
SECCIONES = [
    ("intro", [("tema", 0)]),                    # gancho: el tema principal «Modern Warfare 4»
    ("p25", [("archivos", 0)]),                  # «Searching the Archives»: abrimos el expediente
    ("p23", [("patrulla", 0)]),                  # «First Patrol»
    ("p21", [("relentless", 0)]),                # «Relentless»
    ("p19", [("ordenes", 0)]),                   # «Following Orders» = la misión Cumpliendo órdenes
    ("p17", [("sombras", 0)]),                   # «Into the Shadows»
    ("p15", [("safehouse", 0)]),                 # «Safehouse»
    ("p14", [("outlaws", 0)]),                   # «Outlaws»: Graves y Shadow Company
    ("p13", [("freight", 0)]),                   # «Freight and Savage»: el norte nevado, Hajin
    ("p11", [("losing", 0)]),                    # «Losing Ground»
    ("p09", [("contraataque", 0)]),              # «Counterattack» = el contraataque en la costa de Hajin
    ("p08", [("hunted", 0)]),                    # «Hunted»: Huida
    ("p07", [("responder", 0)]),                 # «Choose How You Respond»: la comandante Ri
    ("p06", [("assassins", 0)]),                 # «Assassins»: París y Prípiat
    ("p04", [("ticking", 0)]),                   # «Ticking Clocks»: la persecución de Makarov
    ("p03", [("disorder", 0)]),                  # «New World Disorder»: el retrato del Líder
    ("spoilers", [("nuclear", 0)]),              # «The Nuclear Option»: el final
    ("p02c", [("hunted", 90)]),                  # la caja fuerte de Gaz
    ("p01", [("archivos", 90)]),                 # el número uno (se aparta donde suena el juego)
    ("cierre", [("tema", 0)]),                   # cierre: vuelve el tema principal
]


def cargar(n):
    import soundfile as sf
    from scipy.signal import resample_poly
    x, sr = sf.read(os.path.join("audio", "ost", n + ".wav"), always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    return x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)


def rampa(n, sube=True):
    r = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    return np.sin(r * np.pi / 2)[:, None]


def armar():
    import pyloudnorm as pyln
    import soundfile as sf
    tl = json.load(open("timeline.json", encoding="utf-8"))
    total = float(tl["total"])
    t0s = {e["id"]: float(e["t0"]) for e in tl["escenas"]}
    t0s.update({b["id"]: float(b["t0"]) for b in json.load(open("beats.json", encoding="utf-8"))})   # cortes por beat
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
    # SONIDO ORIGINAL (el usuario, 26-oct-2026): en los beats con ambiente_por la banda sonora se aparta y se oye el juego
    import guion
    vols = guion.SECUENCIA.get("ambiente_por", {})
    gan = np.ones(len(out))
    r = int(.5 * SR)
    for b in json.load(open("beats.json", encoding="utf-8")):
        if vols.get(b["id"], 0) > 0:
            i0, i1 = int(b["t0"] * SR), min(len(out), int(b["t1"] * SR))
            g = 10 ** (APARTA_DB / 20)
            gan[i0:i1] = np.minimum(gan[i0:i1], g)
            gan[max(0, i0 - r):i0] = np.minimum(gan[max(0, i0 - r):i0], np.linspace(1, g, i0 - max(0, i0 - r)))
            gan[i1:i1 + r] = np.minimum(gan[i1:i1 + r], np.linspace(g, 1, len(gan[i1:i1 + r])))
    out *= gan[:, None]
    print(f"banda sonora apartada {APARTA_DB} dB en {sum(1 for v in vols.values() if v > 0)} beats con sonido original")
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    armar()
