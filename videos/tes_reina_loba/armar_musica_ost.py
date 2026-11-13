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


SECCIONES = [   # tes_reina_loba (12-nov-2026): pista = (archivo, desde) o (archivo, desde, hasta); SIN canto bajo la voz (_canto.json)
    ((0.0, T("c1")), [("the_gathering_storm", 0)]),                                   # gancho: el ritual
    ((T("c1"), T("c2")), [("glory_of_cyrodiil", 0), ("harvest_dawn", 0)]),           # la niña de las cerraduras (Cyrodiil)
    ((T("c2"), T("pregunta")), [("a_winters_tale", 0)]),                              # reina de Soledad
    ((T("pregunta"), T("c3")), [("secunda", 0)]),                                     # pregunta al público
    ((T("c3"), T("c4")), [("silent_footsteps", 0)]),                                  # la gema del lobo (intriga)
    ((T("c4"), T("cr1")), [("auriels_ascension", 0)]),                                # los elfos del mar
    ((T("cr1"), T("c5")), [("caught_off_guard", 0)]),                                 # crítica 1
    ((T("c5"), T("c6")), [("silence_unbroken", 0), ("imperial_throne", 0)]),          # Kintyra
    ((T("c6"), T("ag1")), [("shattered_shields", 0), ("reign_of_the_septims", 0)]),   # guerra del Diamante Rojo
    ((T("ag1"), T("cr2")), [("harvest_dawn", 70)]),                                   # agradecimientos
    ((T("cr2"), T("c7")), [("caught_off_guard", 40)]),                                # crítica 2
    ((T("c7"), T("cr3")), [("journeys_end", 0)]),                                     # la loba sola
    ((T("cr3"), T("c8")), [("secunda", 60)]),                                         # crítica 3
    ((T("c8"), T("campana")), [("imperial_throne", 50), ("reign_of_the_septims", 20), ("a_winters_tale", 150)]),   # Pelagio el Loco
    ((T("campana"), T("c9")), [("king_and_country", 0, 100)]),                        # campaña
    ((T("c9"), T("c9b")), [("kynes_peace", 70, 160), ("the_gathering_storm", 95), ("dawn", 105)]),   # Skyrim: la Reina Loba despierta
    ((T("c9b"), T("cierre")), [("masser", 55, 215)]),                                 # la mente de Pelagio
    ((T("cierre"), None), [("dawn", 130)]),                                           # cierre
]


# DESTACADOS (el usuario, 13-nov-2026: «cuando dices usa Fuerza Implacable porque era Sangre de Dragón pon la música de Skyrim de
# Dragonborn épica y déjala sonar unos segundos»): la voz CALLA (pausa metida con _pausa.py en timeline/beats) y suena la pista,
# más fuerte que el fondo, que se aparta. (t = inicio de la pausa, pista, desde = segundo de la pista en t, dur, +dB, antes, cola)
DESTACADOS = [(t["t"], "dragonborn", 33.0, t["d"], 5.0, 1.0, 2.5)
              for t in json.load(open("timeline.json", encoding="utf-8")).get("pausas", []) if t.get("beat") == "scene-245"]

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
        pistas = [(q[0], q[1], q[2] if len(q) > 2 else None) for q in pistas]
        for n, desde, hasta in pistas:
            x = cargar(n)[int(desde * SR):int(hasta * SR) if hasta else None]
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
        for n, desde, hasta in pistas:
            d = min(_resto, (hasta or len(cargar(n)) / SR) - desde)
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
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(q[0] for q in pistas):24s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    for t, n, desde, d, db, antes, cola in DESTACADOS:
        i0, i1 = int((t - antes) * SR), int((t + d + cola) * SR)
        x = cargar(n)[int((desde - antes) * SR):][:i1 - i0]
        x = x * 10 ** ((LUFS - meter.integrated_loudness(x)) / 20) * 10 ** (db / 20)
        env = np.ones(len(x))
        ka, kc = int(antes * SR), int(cola * SR)
        env[:ka] = np.sin(np.linspace(0, 1, ka) * np.pi / 2)
        env[-kc:] = np.cos(np.linspace(0, 1, kc) * np.pi / 2)
        out[i0:i0 + len(x)] *= (1 - .85 * env)[:, None]                  # el fondo se aparta
        out[i0:i0 + len(x)] += x * env[:, None]
        print(f"destacado {n} ({desde:.0f} s) en {t:.1f}-{t + d:.1f} (+{db} dB, voz callada)")
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
