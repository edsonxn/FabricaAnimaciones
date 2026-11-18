# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL del juego de cada refugio (fo_refugios_25); antes Fallout 4 (Inon Zur; fo_nunca_f4, 17-nov-2026; antes Skyrim) (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
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


SECCIONES = [   # OST oficial del juego de CADA refugio (audio/ost/_ids.json); sin canto bajo la voz (audio/ost/_canto.json)
    ((0.0, T("p25")), [("fo3_main_title", 0)]),                    # saludo + gancho
    ((T("p25"), T("p24")), [("fo4_imagine_utopia", 0)]),            # 55/56 (recreación FO4)
    ((T("p24"), T("p23")), [("fnv_main_title", 0)]),                # 21 New Vegas
    ((T("p23"), T("p22")), [("fo4_welcome_far_harbor", 0), ("fo4_lost_memories", 0)]),   # 118 Far Harbor
    ((T("p22"), T("p21")), [("fo4_lone_wandering", 40)]),           # 43 pantera (FO4)
    ((T("p21"), T("p20")), [("fo4_science_secrecy", 0)]),           # 88
    ((T("p20"), T("p19")), [("fo3_what_remains", 0)]),              # 101
    ((T("p19"), T("p18")), [("fnv_rubble_of_the_forgotten", 0)]),   # 22
    ((T("p18"), T("p17")), [("fo3_forgotten", 0)]),                 # 106
    ((T("p17"), T("p16")), [("fo76_the_grafton_damned", 0)]),       # 63
    ((T("p16"), T("p15a")), [("fo4_rebuild_renew", 40)]),           # 81
    ((T("p15a"), T("p14")), [("fo3_unwelcome_guest", 0)]),         # 108 Gary
    ((T("p14"), T("p13")), [("fot_haunted_desolation", 0)]),        # 0 Tactics
    ((T("p13"), T("p12")), [("fo3_wandering_the_wastes", 0)]),      # 77
    ((T("p12"), T("p11")), [("fo76_landscape_lament", 0)]),         # 94
    ((T("p11"), T("p10")), [("fo3_the_ferals", 0)]),                # 68/69
    ((T("p10"), T("p9")), [("fo4_glowing_sea_1", 0)]),              # 95 Mar Resplandeciente
    ((T("p9"), T("p8")), [("fo4_main_theme", 0)]),                  # 111
    ((T("p8"), T("p7a")), [("fo1_city_of_the_dead", 0)]),           # 12 Necrópolis
    ((T("p7a"), T("p6")), [("fo3_behemoth", 0)]),                   # 92
    ((T("p6"), T("subs")), [("fo3_metal_on_metal", 0)]),            # 87 supermutantes
    ((T("subs"), T("p5")), [("fo1_vault_of_the_future", 0)]),       # suscripción
    ((T("p5"), T("p4")), [("fo76_something_lurking", 0), ("fo76_scorched_earth", 0)]),   # 96
    ((T("p4"), T("p3a")), [("fo76_main_theme", 0), ("fo76_the_grafton_damned", 120)]),  # 51
    ((T("p3a"), T("p2")), [("fnv_industrial_de_evolution", 0)]),    # 11
    ((T("p2"), T("p1")), [("fo4_glowing_sea_2", 0), ("fo4_science_secrecy", 100)]),     # 75
    ((T("p1"), T("cierre")), [("fo3_forgotten", 60), ("fo3_unwelcome_guest", 100)]),    # 112
    ((T("cierre"), None), [("fo3_main_title", 30)]),                # despedida
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
