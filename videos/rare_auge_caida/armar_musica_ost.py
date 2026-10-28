# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de los juegos de Rare de cada época (regla del usuario del 23-oct-2026:
en Crónicas del gaming va la música del juego, NUNCA Lyria). Pistas ya bajadas con yt-dlp en audio/ost/ (28-oct-2026):
Nintendo Music Archive (DKC), Grant Kirkhope - Topic (Banjo-Kazooie), Sea of Thieves - Topic, Video-Game OST HQ (GoldenEye,
Perfect Dark), Myld the Archivist (Kameo, Steve Burke), GBelair (Battletoads NES), Games OST (Killer Instinct)...
Receta de oot_remake_cambios/armar_musica_ost.py: cada sección a -23 LUFS, fundidos cruzados de 2 s, rampa final; la banda
sonora se APARTA en los beats con sonido original (guion.SECUENCIA["ambiente_por"]).
    python armar_musica_ost.py         arma audio/musica.wav (luego `python fab.py rare_auge_caida mezcla`)
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
CANAL = "Nintendo Music Archive"

PISTAS = {}            # ya bajadas a mano (audio/ost/<slug>.wav); ver el docstring

# escena del guion -> pistas que la llenan en orden: (slug, desde s)
SECCIONES = [
    ("intro", [("dkc_tema", 0)]),                          # gancho: el tema de Donkey Kong Country
    ("c1", [("btoads_titulo", 0)]),                        # Ultimate (la Spectrum casi no tenía música): Battletoads
    ("c2", [("btoads_ragnarok", 0)]),                      # la NES: Battletoads
    ("c3", [("dkc_aquatic", 0)]),                          # la apuesta y DKC: Aquatic Ambiance
    ("scene-045", [("ki_tema", 0)]),                       # «Después llegaron Killer Instinct…»
    ("c4", [("ge_archives", 0)]),                          # GoldenEye: Archives
    ("c5", [("bk_spiral", 0)]),                            # DKR, Banjo y Dream: Spiral Mountain
    ("scene-069", [("pd_carrington", 0)]),                 # «En el año 2000 llegó Perfect Dark»
    ("scene-072", [("conker_windy", 0)]),                  # «…nadie veía venir. Conker.»
    ("c6", [("sfa_thorntail", 0)]),                        # el divorcio: Star Fox Adventures
    ("c7", [("kameo_heroe", 0)]),                          # Ghoulies, Kameo, PDZ: Kameo (Steve Burke)
    ("scene-097", [("viva_tema", 0), ("bk_clickclock", 0)]),  # «En 2006 llegó Viva Piñata» … Nuts and Bolts, Kinect
    ("c8", [("sot_estrella", 0)]),                         # Sea of Thieves
    ("cierre", [("dkc_creditos", 0)]),                     # cierre: los créditos de DKC
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
