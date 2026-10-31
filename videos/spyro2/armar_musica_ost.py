# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de Spyro 2 (regla del 23-oct-2026: en Crónicas del gaming va la música del juego,
NUNCA Lyria). 44 pistas en audio/ost/. Receta de mario64_secretos; s19 y s20 usan las versiones de demo y las dos de Ripto's Arena.
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py spyro2 mezcla`)
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

PISTAS = {}            # ya bajadas a mano (audio/ost/<slug>.wav); ver el docstring

# escena del guion -> pistas que la llenan en orden: (slug, desde s)
SECCIONES = [
    ("intro", [("01_gateway_to_glimmer", 0)]),             # el gancho: Glimmer, el primer nivel
    ("h1", [("03_idol_springs", 0)]),                      # el origen
    ("h2", [("12_autumn_plains", 0)]),                     # Avalar
    ("h3", [("02_summer_forest", 0)]),                     # Copeland: «Summer Forest suena a verano»
    ("h4", [("30_winter_tundra", 0)]),                     # lanzamiento
    ("s30", [("03_idol_springs", 30)]),                    # se oye el tema compartido por Idol Springs y Fracture Hills
    ("s29", [("33_agent_zero_s_secret_hideout", 0)]),      # trucos y prototipo
    ("s27", [("34_robotica_farms", 0)]),                   # Moneybags
    ("s26", [("06_hockey", 0)]),
    ("s25", [("32_cloud_temples", 0)]),                    # Elora, las alas
    ("s23", [("16_dem_bones", 0)]),                        # las voces
    ("s21", [("29_gulp_s_overlook", 0)]),
    ("s20", [("37_ripto_s_arena", 0)]),                    # con voz de ópera (EE. UU.)
    ("scene-079", [("43_ripto_s_arena_alternate", 10)]),   # «en la versión europea, la quitaron»
    ("scene-081", [("40_sunny_beach_demo", 0)]),           # versión larga de la demo
    ("s18", [("09_aquaria_towers", 0)]),
    ("s17", [("24_magma_cone", 0)]),
    ("s16", [("20_gear_grab", 0)]),
    ("s15", [("21_zephyr", 0)]),                           # nombres viejos
    ("s13", [("36_canyon_speedway", 0)]),                  # prototipos
    ("s11", [("07_hurricos", 0)]),                         # el juego sin final, Elora y Hurricos
    ("s09", [("19_breeze_harbor", 0)]),
    ("s08", [("05_colossus", 0)]),
    ("s07", [("11_crush_s_dungeon", 0)]),
    ("s06", [("35_metropolis", 0)]),
    ("s05", [("01_gateway_to_glimmer", 60)]),              # el puente de Glimmer
    ("s04", [("26_shady_oasis", 0)]),
    ("s03", [("10_ocean_speedway", 0)]),
    ("s02", [("22_scorch", 0)]),
    ("s01", [("31_mystic_marsh", 0)]),
    ("cierre", [("38_dragon_shores", 0), ("39_end_credits", 0)]),
]


def bajar():
    os.makedirs(os.path.join("audio", "ost"), exist_ok=True)
    for slug, nombre in PISTAS.items():
        out = os.path.join("audio", "ost", slug + ".wav")
        if os.path.exists(out):
            continue
        q = f"ytsearch5:{CANAL} The Legend of Zelda Ocarina of Time OST - {nombre}"
        r = subprocess.run(["yt-dlp", q, "--flat-playlist", "--print", "%(id)s|%(channel)s|%(title)s"],
                           capture_output=True, text=True, encoding="utf-8", errors="replace")
        elegido = None
        for linea in r.stdout.splitlines():
            vid, canal, titulo = (linea.split("|", 2) + ["", ""])[:3]
            if canal == CANAL and "Ocarina of Time OST" in titulo and titulo.rsplit(" - ", 1)[-1].strip().lower() == nombre.lower():
                elegido = (vid, titulo)
                break
        if not elegido:
            print(f"  ✗ {slug}: no encontrada «{nombre}»")
            continue
        subprocess.run(["yt-dlp", "-q", "-x", "--audio-format", "wav", "-o", os.path.join("audio", "ost", slug + ".%(ext)s"),
                        f"https://youtu.be/{elegido[0]}"], check=False)
        print(f"  {slug:15s} {elegido[0]}  {elegido[1]}")


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
    bajar() if sys.argv[1:] == ["bajar"] else armar()
