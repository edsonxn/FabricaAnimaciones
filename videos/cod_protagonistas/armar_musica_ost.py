"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de los CoD de los que habla cada puesto (toda la saga; regla del usuario del 23-oct-2026:
en los canales de videojuegos va la música del juego, NUNCA Lyria). Pistas en audio/ost/ (`_catalogo.txt`, `_bajar.sh`; álbum
oficial en «Stephen Barton - Topic» y su resubida completa en modENASh1). Receta de bt_mundos_ranking: cada sección a -23 LUFS,
fundidos cruzados de 2 s; la banda sonora se APARTA en los beats con sonido original (guion.SECUENCIA["ambiente_por"]).
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py cod_protagonistas mezcla`)
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
SECCIONES = [   # cod_protagonistas (24-nov-2026): audio/ost/_catalogo.txt (11 pistas de campaña nuevas en el canal)
    ("intro", [("mw22_tema", 0)]), ("intro_b", [("mw22_tema", 40)]), ("p20", [("aw_overture", 0)]), ("p19", [("gh_rorke", 0)]),
    ("p18", [("mw19_comrades", 0)]), ("p17", [("cod4_crew", 0)]), ("p16", [("cod4_crew", 90)]), ("crit1", [("mw22_hindsight", 0)]),
    ("p15", [("mw23_tema", 0)]), ("p14", [("mw3_standalone", 0)]), ("p13", [("cw_bell", 0)]), ("p12", [("cw_bell", 100)]),
    ("p11", [("mw22_hindsight", 40)]), ("p11b", [("mw22_hindsight", 80)]), ("p10", [("mw22_tema", 90)]), ("p09", [("waw_reznov", 0)]),
    ("p09b", [("waw_reznov", 30)]), ("p08", [("mw3_standalone", 60)]), ("p08b", [("mw3_standalone", 110)]), ("p07", [("ww2_brotherhood", 0)]),
    ("p06", [("cw_bell", 170)]), ("p06b", [("cw_bell", 220)]), ("p05", [("mw19_comrades", 70)]), ("p04", [("aw_overture", 80)]),
    ("crit2", [("mw23_tema", 80)]), ("p03", [("mw23_tema", 110)]), ("p03b", [("mw22_hindsight", 150)]), ("p02", [("mw22_tema", 120)]),
    ("p02b", [("mw19_comrades", 150)]), ("p01", [("mw23_tema", 150)]), ("p01b", [("mw3_standalone", 170)]), ("cierre", [("ww2_brotherhood", 60)]),
]
# SONIDOS NOMBRADOS (citas, regla 10 del 19-nov-2026): la banda sonora se aparta en el hueco «post» de cada escena con cita
# (del fin de su última frase al final de la escena, leído de timeline.json: sigue valiendo si cambia el tiempo)
def _tramos_citas():
    import guion
    tl = json.load(open("timeline.json", encoding="utf-8"))
    post = {e["id"] for e in guion.ESCENAS if e.get("post", 0) >= 2.0}
    return [(float(e["frases"][-1]["t1"]) - .2, float(e["t1"]) + .1) for e in tl["escenas"] if e["id"] in post]


TRAMOS_SONIDO = _tramos_citas()


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
