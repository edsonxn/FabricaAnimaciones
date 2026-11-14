# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Skyrim (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Copiado de er_malenia_atrocidades. Pistas en audio/ost/
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


SECCIONES = [   # tes_sentinel_teaser (3-nov-2026): ESO (Brad Derrick) + Oblivion/Morrowind (Jeremy Soule), pistas en audio/ost/
    ((0.0, T("p15")), [("past_defines_the_future", 0)]),   # gancho + presentación de las siete voces
    ((T("p15"), T("p13")), [("reign_of_the_septims", 0), ("through_gates_of_flame", 0)]),   # 15-14 Johnny: Bethesda y Todd
    ((T("p13"), T("p11")), [("hinterlands", 0)]),   # 13-12 Edoardo: teasers y filtración
    ((T("p11"), T("p10")), [("sands_of_the_alikr", 0)]),   # 11 Hope: Sentinel + cr1
    ((T("p10"), T("p9")), [("tombs_unremembered", 0)]),   # 10 Hope: Daggerfall, Numidium
    ((T("p9"), T("ag1")), [("a_land_of_war_and_poetry", 0)]),   # 9-8 José: Alik'r y Yokuda
    ((T("ag1"), T("p6")), [("beauty_of_dawn", 0)]),   # ag1 (El Jefe) + 7 Mario
    ((T("p6"), T("p5")), [("isles_of_the_starry_dream", 0)]),   # 6 + cr2 Mario
    ((T("p5"), T("p4")), [("weapons_drawn", 0)]),   # 5 MariCarmen: la guerra
    ((T("p4"), T("p3")), [("virtue_betrayal", 0)]),   # 4 MariCarmen: el sacerdote
    ((T("p3"), T("p2")), [("even_paradise_has_shadows", 0)]),   # 3 + campaña, el Profeta
    ((T("p2"), T("p1")), [("nerevar_rising", 0), ("past_defines_the_future", 120)]),   # 2 + cr3
    ((T("p1"), None), [("through_gates_of_flame", 0)]),   # 1 + cierre y votación
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
