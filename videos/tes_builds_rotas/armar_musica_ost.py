# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Skyrim (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Copiado de er_malenia_atrocidades / tes_sentinel_teaser. Pistas en audio/ost/
(yt-dlp de «Jeremy Soule - Topic», `_bajar_ost.py`, ids en audio/ost/_ids.json), 19 pistas copiadas de tes_cosas_nunca, tes_armas_poderosas y tes_cosas_inutiles (30-oct-2026).
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py tes_secretos_40 ambiente` y `mezcla`)
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
APARTA_DB = -14.0    # la banda sonora baja esto donde suena el juego (beats con ambiente_por en guion.SECUENCIA)

# (inicio, fin) de cada sección en el video y las pistas que la llenan en orden: (archivo, desde s)
_ESC = {e["id"]: e["t0"] for e in json.load(open("timeline.json", encoding="utf-8"))["escenas"]}


def T(esc, dt=-2.5):
    """Inicio de la escena `esc` en timeline.json (menos dt: la pista nueva entra justo antes de que hable la voz). Así las
    secciones siguen solas a la voz cuando cambia (siete voces, 3-nov-2026)."""
    return round(_ESC[esc] + dt, 2)


SECCIONES = [   # v3 (12-nov-2026): SIN CANTO bajo la voz (audio/ost/_canto.json de nucleo/ost_canto.py; fuera Age of Oppression, coro entero)
    ((0.0, T("p10")), [("age_of_aggression", 0)]),   # gancho + tabla de builds
    ((T("p10"), T("p9")), [("far_horizons", 0)]),   # 10 arquero (canto desde 150 s)
    ((T("p9"), T("cr1")), [("into_darkness", 0)]),   # 9 carterista
    ((T("cr1"), T("p8")), [("dragonsreach", 0)]),   # correo
    ((T("p8"), T("p7")), [("the_jerall_mountains", 82)]),   # 8 titiritero (antes Ancient Stones: canto a los 65 s)
    ((T("p7"), T("p6")), [("the_gathering_storm", 0)]),   # 7 Señor de los Vampiros
    ((T("p6"), T("ag1")), [("under_an_ancient_sun", 0)]),   # 6 nigromante (antes Age of Oppression = MÚSICA CANTADA, 7:25 de la v2)
    ((T("ag1"), T("p5")), [("dawn", 0)]),   # agradecimientos (canto a los 65 s)
    ((T("p5"), T("p4")), [("tooth_and_claw", 0), ("into_darkness", 100)]),   # 5 asesino (+ guiño)
    ((T("p4"), T("cr2")), [("death_or_sovngarde", 0)]),   # 4 mago sin coste (canto desde 125 s)
    ((T("cr2"), T("p3")), [("dragonsreach", 60)]),   # crítica 2 (@edgarvillalobos1492)
    ((T("p3"), T("campana")), [("steel_on_steel", 31), ("age_of_aggression", 0)]),   # 3 pararrayos (canto a los 25 s)
    ((T("campana"), T("p2")), [("solitude", 0)]),   # campaña de suscripción (canto desde 30 s)
    ((T("p2"), T("cr3")), [("imperial_throne", 0)]),   # 2 artesano
    ((T("cr3"), T("p1")), [("dawn", 80)]),   # crítica 3 (@YetRise)
    ((T("p1"), None), [("out_of_the_cold", 0), ("imperial_throne", 0)]),   # 1 boticario + cierre
]


_CJ = os.path.join("audio", "ost", "_canto.json")
CANTO = json.load(open(_CJ, encoding="utf-8")) if os.path.exists(_CJ) else {}   # nucleo/ost_canto.py (12-nov-2026)


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
        _usado, _resto = [], (t1 - t0 + CRUCE)
        for n, desde in pistas:
            d = min(_resto, len(cargar(n)) / SR - desde)
            _usado.append((n, desde, d))
            _resto -= d
            if _resto <= 0:
                break
        for n, desde, d in _usado:
            malas = [c for c in CANTO.get(n, []) if desde - 5 < c < desde + d]
            if malas:
                raise SystemExit(f"CANTO bajo la voz: {n} {desde:.0f}-{desde + d:.0f} s pisa canto en {malas} (sección {t0:.0f}-{t1:.0f})")
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
    main()
