# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Skyrim (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Copiado de er_malenia_atrocidades. Pistas en audio/ost/
(yt-dlp de «Jeremy Soule - Topic», `_bajar_ost.py`, ids en audio/ost/_ids.json), 20 pistas que NO sonaron en tes_cosas_inutiles ni en tes_armas_poderosas.
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py tes_cosas_nunca ambiente` y `mezcla`)
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
SECCIONES = [
    ((0.0, 48.0), [("from_past_to_present", 0)]),                    # gancho: el tema más reconocible
    ((48.0, 149.3), [("streets_of_whiterun", 0)]),                    # 20 gallina · 19 caballo (pueblo, de broma)
    ((149.3, 194.7), [("a_winters_tale", 0)]),                        # 18 Lydia esperando (soledad)
    ((194.7, 248.0), [("silent_footsteps", 0)]),                      # 17 trampas (mazmorra)
    ((248.0, 304.0), [("tooth_and_claw", 0)]),                        # 16 pelea a puñetazos
    ((304.0, 357.3), [("watch_the_skies", 0)]),                       # 15 Fus Ro Dah (Sangre de Dragón)
    ((357.3, 408.0), [("caught_off_guard", 0)]),                      # 14 bolas de fuego (combate)
    ((408.0, 461.3), [("towers_and_shadows", 0)]),                    # 13 Llave maestra (ladrones)
    ((461.3, 514.7), [("masser", 0)]),                                # 12 la estrella (místico)
    ((514.7, 565.3), [("dragonsreach", 0)]),                          # 11 alma del dragón
    ((565.3, 610.7), [("the_city_gates", 0)]),                        # 10 matones
    ((610.7, 664.0), [("frostfall", 0)]),                             # 9 cárcel
    ((664.0, 714.7), [("around_the_fire", 0)]),                       # 8 la resaca de Sanguine (posada)
    ((714.7, 768.0), [("jerall_mountains", 0)]),                      # 7 comerciantes
    ((768.0, 818.7), [("distant_horizons", 0)]),                      # 6 Cicerón
    ((818.7, 869.3), [("seven_thousand_steps", 0)]),                  # 5 gigante (épico)
    ((869.3, 917.3), [("before_the_storm", 0)]),                      # 4 hombre lobo
    ((917.3, 978.7), [("night_without_stars", 0), ("masser", 200)]),  # 3 vampirismo (noche)
    ((978.7, 1034.7), [("under_an_ancient_sun", 0)]),                 # 2 subir sin pelear
    ((1034.7, 1104.0), [("wind_guide_you", 0)]),                      # 1 los cofres
    ((1104.0, None), [("from_past_to_present", 120)]),                # cierre: vuelve el tema del gancho
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
