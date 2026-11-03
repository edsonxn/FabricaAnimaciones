# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA ORIGINAL de Game Boy de Pokémon Rojo/Azul (regla del 23-oct-2026: en Crónicas del gaming
va la música del juego, NUNCA Lyria). 35 pistas en audio/ost/ (`python bajar_ost.py`). Receta de spyro2; s07 = Pueblo Lavanda y la
Torre Pokémon, s06 = la Mansión (los diarios de Mew), s05 = Isla Canela + Surf (la costa de MissingNo), s11 = combate del campeón.
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py pokemon_rojo_azul mezcla`)
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
    ("intro", [("titulo", 0)]),
    ("h1", [("pallet", 0), ("route1", 0)]),
    ("h2", [("pewter", 0), ("pkcenter", 0)]),
    ("h3", [("route3_4", 0), ("cerulean", 0)]),
    ("s20", [("oak", 0), ("rival", 0), ("oak_lab", 0)]),
    ("s19", [("celadon", 0)]),
    ("s18", [("silph", 0)]),
    ("s17", [("mtmoon", 0)]),
    ("s16", [("forest", 0)]),
    ("s15", [("vermilion", 0), ("ssanne", 0)]),
    ("s14", [("gymleader", 0)]),
    ("s13", [("wild", 0)]),
    ("s12", [("trainer", 0)]),
    ("s11", [("champion", 0)]),
    ("s10", [("cycling", 0)]),
    ("s09", [("route6", 0)]),
    ("s08", [("gym", 0)]),
    ("s07", [("lavender", 0), ("tower", 0)]),
    ("s06", [("mansion", 0)]),
    ("s05", [("cinnabar", 0), ("surf", 0)]),
    ("s04", [("route24", 0)]),
    ("s03", [("victoria_lider", 0), ("capturado", 0)]),
    ("s02", [("casino", 0)]),
    ("s01", [("indigo", 0), ("hall_fame", 0)]),
    ("cierre", [("credits", 0)]),
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
