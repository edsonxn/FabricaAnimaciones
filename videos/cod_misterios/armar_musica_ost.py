"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de los CoD de los que habla cada puesto (CoD 4, MW2, MW3, Black Ops; regla del usuario del 23-oct-2026:
en los canales de videojuegos va la música del juego, NUNCA Lyria). Pistas en audio/ost/ (`_catalogo.txt`, `_bajar.sh`; álbum
oficial en «Stephen Barton - Topic» y su resubida completa en modENASh1). Receta de bt_mundos_ranking: cada sección a -23 LUFS,
fundidos cruzados de 2 s; la banda sonora se APARTA en los beats con sonido original (guion.SECUENCIA["ambiente_por"]).
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py cod_misterios mezcla`)
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

# escena del guion -> pistas que la llenan en orden: (slug, desde s). OST oficial de cada saga (audio/ost/_catalogo.txt)
SECCIONES = [   # cod_misterios (10-nov-2026): audio/ost/_catalogo.txt (Ghosts, BO2, MW2019, IW, Ascension); «Dead Again» no (es canción)
    ("intro", [("gh_ghoststories", 0)]), ("p30", [("z_abracadavre", 0)]), ("p29", [("iw_safeharbor", 0)]),
    ("p28", [("bo2_alexdavid", 0)]), ("p27", [("z_abracadavre", 120)]), ("p26", [("z_abracadavre", 200)]),
    ("p25", [("bo2_menendez", 0)]), ("p24", [("bo2_panama", 0)]), ("p23", [("mw19_stpete", 0)]),
    ("p22", [("z_abracadavre", 260)]), ("p21", [("gh_hack", 0)]), ("p20", [("gh_tema", 0)]),
    ("p19", [("bo2_alexdavid", 30)]), ("p18", [("bo2_panama", 50)]), ("p17", [("bo2_menendez", 70)]),
    ("p16", [("mw19_execute", 0)]), ("p15", [("gh_hack", 40)]), ("p14", [("mw19_stpete", 80)]),
    ("p13", [("mw19_execute", 60)]), ("p12", [("iw_home", 0)]), ("p11", [("gh_tema", 100)]),
    ("p10", [("bo2_menendez", 150)]), ("p09", [("gh_ghoststories", 40)]), ("p08", [("iw_safeharbor", 60)]),
    ("p07", [("iw_home", 50)]), ("p06", [("mw19_stpete", 160)]), ("p05", [("gh_tema", 20)]),
    ("p04", [("z_abracadavre", 320), ("bo2_alexdavid", 0)]), ("p03", [("bo2_alexdavid", 40)]), ("p02", [("iw_safeharbor", 0)]),
    ("p01", [("mw19_stpete", 0)]), ("cierre", [("gh_tema", 140)]),
]
# SONIDOS NOMBRADOS (PISTAS voz=True de efectos.py): la banda sonora también se aparta ahí (s, s) de `fx --seco`
TRAMOS_SONIDO = [(14.1, 16.3), (567.4, 572.0), (792.6, 797.3), (873.3, 880.7), (887.2, 893.6), (931.3, 933.4), (1050.8, 1057.9)]


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
    g = 10 ** (APARTA_DB / 20)
    for a, b in TRAMOS_SONIDO:
        i0, i1 = int(a * SR), min(len(out), int(b * SR))
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
