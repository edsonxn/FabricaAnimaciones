# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Skyrim (regla del usuario, 23-oct-2026: en Warcraft, Tamriel,
Runa Caída y Crónicas del gaming va la música del juego, no Lyria). Copiado de er_malenia_atrocidades. Pistas en audio/ost/
(yt-dlp de «Jeremy Soule - Topic», `_bajar_ost.py`, ids en audio/ost/_ids.json), 18 pistas que la Fábrica no había usado en el canal + 6 de tes_armas_poderosas (28-oct-2026).
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py tes_misiones_imperdibles ambiente` y `mezcla`)
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
    ((0.0, 53.3), [("sky_above_voice_within", 0)]),                  # gancho: el comentario que lo empezó todo
    ((53.3, 109.3), [("into_darkness", 0)]),                          # 25 Simas insondables (ruina dwemer)
    ((109.3, 154.7), [("beneath_the_ice", 0)]),                       # 24 La expedición perdida (máquinas)
    ((154.7, 210.7), [("silence_unbroken", 0)]),                      # 23 Vuelta a las raíces (Límite Sombrío)
    ((210.7, 261.3), [("the_white_river", 0)]),                       # 22 Kyne (cacería por el mapa)
    ((261.3, 309.3), [("the_bannered_mare", 0)]),                     # 21 Colegio de Bardos (fiesta)
    ((309.3, 360.0), [("standing_stones", 0)]),                       # 20 Saadia (dilema)
    ((360.0, 400.0), [("ancient_stones", 0)]),                        # 19 Neloth
    ((400.0, 440.0), [("far_horizons", 0)]),                          # 18 El Vial Blanco (triste)
    ((440.0, 488.0), [("shattered_shields", 0)]),                     # 17 Thorald (asalto al fuerte)
    ((488.0, 533.3), [("out_of_the_cold", 0)]),                       # 16 Águila Roja
    ((533.3, 584.0), [("journeys_end", 0)]),                          # 15 stalhrim (Solstheim)
    ((584.0, 640.0), [("imperial_throne", 0)]),                       # 14 Se sirve mejor fría (intriga)
    ((640.0, 688.0), [("skyrim_atmospheres", 600)]),                  # 13 Arvak (Recordatorio de las Almas)
    ((688.0, 741.3), [("the_gathering_storm", 0)]),                   # 12 Estigma mortal (tesoro pirata)
    ((741.3, 797.3), [("skyrim_atmospheres", 1500)]),                 # 11 Apócrifa
    ((797.3, 853.3), [("unbound", 0), ("aurora", 60)]),               # 10 Desenterrado (el que despierta)
    ((853.3, 901.3), [("one_they_fear", 0)]),                         # 9 Durnehviir
    ((901.3, 949.3), [("sovngarde", 0)]),                             # 8 Kodlak va a Sovngarde
    ((949.3, 1008.0), [("kynes_peace", 0)]),                          # 7 Meridia
    ((1008.0, 1058.7), [("solitude", 0)]),                            # 6 la Reina Loba de Soledad
    ((1058.7, 1104.0), [("steel_on_steel", 0)]),                      # 5 el guerrero de ébano
    ((1104.0, 1154.7), [("skyrim_atmospheres", 2400)]),               # 4 Séptimo y el Oghma (Límite Sombrío)
    ((1154.7, 1208.0), [("secunda", 0)]),                             # 3 Leyenda prohibida
    ((1208.0, 1258.7), [("dawn", 0)]),                                # 2 el Valle Olvidado
    ((1258.7, 1325.3), [("aurora", 0)]),                              # 1 Sheogorath
    ((1325.3, None), [("sky_above_voice_within", 120)]),              # cierre: vuelve el tema del gancho
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
