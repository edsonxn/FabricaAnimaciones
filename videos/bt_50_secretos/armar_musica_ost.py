# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la banda sonora de Banjo-Tooie (regla del usuario del 23-oct-2026: en Crónicas del gaming va la
música del juego, NUNCA Lyria). Pistas ya bajadas en audio/ost/ (preparar_base.py, ripeo del juego en «Video-Game OST HQ»). Receta
de mario64_secretos: cada sección a -23 LUFS, fundidos cruzados de 2 s, rampa final; la banda sonora se APARTA en los beats con
sonido original (guion.SECUENCIA["ambiente_por"]).
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py bt_50_secretos mezcla`)
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

# escena del guion -> pistas que la llenan en orden: (slug, desde s). Una pista por secreto, la de su mundo o su tema;
# las de audio/ost_extra (vs_hag1, cauldron, tower) se bajaron para este video.
SECCIONES = [
    ("intro", [("overture", 0)]), ("s50", [("spiral", 0)]), ("s49", [("ggm", 0)]), ("s48", [("seleccion", 0)]),
    ("s47", [("atlantis", 0)]), ("s46", [("cauldron", 0)]), ("s45", [("jinjo", 0)]), ("s44", [("mt", 0)]),
    ("s43", [("ggm_cuevas", 0)]), ("s42", [("vs_klungo", 0)]), ("s41", [("plan", 0)]), ("s40", [("jiggywiggy", 0)]),
    ("s39", [("vs_hag1", 60)]), ("s38", [("ww", 0)]), ("s37", [("jrl", 0)]), ("s36", [("tower", 0)]),
    ("s35", [("isla", 0)]), ("s34", [("hfp_hielo", 0)]), ("s33", [("mt", 120)]), ("s32", [("tema", 0)]),
    ("s31", [("cauldron", 120)]), ("s30", [("ordnance", 0)]), ("s29", [("tower", 120)]), ("s28", [("funngames", 0)]),
    ("s27", [("vs_hag1", 0)]), ("s26", [("jinjo", 90)]), ("mitad", [("spiral", 60)]), ("s25", [("ww", 120)]),
    ("s24", [("hfp_lava", 0)]), ("s23", [("tower", 240)]), ("s22", [("tdl", 0)]), ("s21", [("jinjo", 180)]),
    ("s20", [("jiggywiggy", 90)]), ("s19", [("problema", 0)]), ("s18", [("mt", 240)]), ("s17", [("jrl", 120)]),
    ("s16", [("gi_dentro", 0)]), ("s15", [("seleccion", 90)]), ("s14", [("overture", 60)]), ("s13", [("overture", 150)]),
    ("s12", [("vs_klungo", 60)]), ("s11", [("spiral", 150)]), ("s10", [("gi", 0)]), ("s09", [("jrl", 240)]),
    ("s08", [("ccl", 0)]), ("s07", [("mary", 0)]), ("s06", [("gi_elevador", 0)]), ("s05", [("ordnance", 120)]),
    ("s04", [("vs_terry", 0)]), ("s03", [("fallo", 0)]), ("s02", [("tdl", 120)]), ("s01", [("fin", 0)]),
    ("cierre", [("creditos", 0)]),
]
# «Escucha…» sobre la PROPIA banda sonora (regla del 31-oct: lo que la voz nombra se oye): en el silencio `post` de estas escenas
# la pista sube estos dB (la voz calla) y no se aparta.
SUBE_DB = {"s47": 9.0, "s35": 9.0, "s27": 9.0}


def cargar(n):
    import soundfile as sf
    from scipy.signal import resample_poly
    r = os.path.join("audio", "ost", n + ".wav")
    if not os.path.exists(r):
        r = os.path.join("audio", "ost_extra", n + ".wav")
    x, sr = sf.read(r, always_2d=True)
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
    # subidas de los «escucha»: desde que acaba la última frase de la escena hasta el inicio de la siguiente
    ids = [e["id"] for e in tl["escenas"]]
    for k, e in enumerate(tl["escenas"]):
        if e["id"] in SUBE_DB:
            fin_voz = float(e["fin_voz"]) + .3
            t1 = float(e["t1"])
            i0, i1 = int(fin_voz * SR), int(t1 * SR)
            g = 10 ** (SUBE_DB[e["id"]] / 20)
            gan[i0:i1] = g
            gan[max(0, i0 - r):i0] = np.linspace(1, g, i0 - max(0, i0 - r))
            gan[i1:i1 + r] = np.linspace(g, 1, len(gan[i1:i1 + r]))
            print(f"sube {e['id']} +{SUBE_DB[e['id']]} dB {fin_voz:.1f}-{t1:.1f}")
    out *= gan[:, None]
    print(f"banda sonora apartada {APARTA_DB} dB en {sum(1 for v in vols.values() if v > 0)} beats con sonido original")
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    armar()
