# -*- coding: utf-8 -*-
"""Arma audio/musica.wav de n64_secretos con la BANDA SONORA del juego de CADA secreto (regla del 23-oct-2026: Crónicas del gaming usa
la OST de lo que cuenta, NUNCA Lyria). Una pista (un tramo de ~dur+14 s) por escena del guion, sin repetir pista ni tramo.
Fuentes (investigacion.md § E, comprobadas con yt-dlp el 31-oct-2026): ripeos de fans en YouTube (la N64 no tiene álbumes «- Topic»);
Final Fantasy VI y VII salen del canal oficial SQUARE ENIX MUSIC. Super Mario 64 (file, créditos) se copia de mario64_secretos.
    python armar_musica_ost.py bajar     baja a audio/ost/<escena>_<juego>.wav el tramo de cada escena (reanuda: salta las que ya están)
    python armar_musica_ost.py           arma audio/musica.wav leyendo los t0 de timeline.json (luego `python fab.py n64_secretos mezcla`)
Elegir otro tramo: cambiar «desde» en PISTAS, borrar el .wav de esa escena y repetir `bajar`.
"""
import json
import math
import os
import shutil
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
OST = os.path.join(AQUI, "audio", "ost")
SR = 48000
CRUCE = 2.0
LUFS = -23.0
APARTA_DB = -14.0       # la banda sonora baja esto donde suena el juego (beats con ambiente_por en guion.SECUENCIA)
MARGEN = 14             # segundos de pista de más sobre la duración de la escena (cruces y rampas)
MARIO64 = os.path.join("C:/FabricaAnimaciones/videos/mario64_secretos/audio/ost")

# escena -> (slug del juego, fuente [id de YouTube | "local:<ruta>"], desde s, qué suena)
PISTAS = [
    ("intro", "mario_party", "iCuKqhnct4M", 0, "Mario Party: Opening (los guantes)"),
    ("h1", "pilotwings64", "LwfPI0o4rmk", 0, "Pilotwings 64: Opening Theme (juego de lanzamiento, tecnología SGI)"),
    ("h2", "fzero_x", "EPn4kCTnJ-0", 1672, "F-Zero X: Title BGM"),
    ("h3", "mario_kart64", "bSb7MrN0bY8", 0, "Mario Kart 64: tema (cuatro mandos)"),
    ("h4", "wave_race64", "R5JjdFqaVaw", 0, "Wave Race 64: Main Title"),
    ("s30", "mario_tennis", "vIuT2e6B1tE", 39, "Mario Tennis: Opening Wario, Waluigi Entrance"),
    ("s29", "excitebike64", "jA6WlM136lU", 0, "Excitebike 64: comienzo del OST"),
    ("s28", "pilotwings64_giro", "LwfPI0o4rmk", 502, "Pilotwings 64: Gyrocopter (los misiles)"),
    ("s27", "1080_snowboarding", "CGFfKa_E0zc", 0, "1080 Snowboarding: comienzo (stick analógico)"),
    ("s26", "paper_mario", "njZgRUhEr10", 0, "Paper Mario: comienzo"),
    ("s25", "star_fox64", "Wzwgztv3oCQ", 596, "Star Fox 64: Corneria (Rumble Pak)"),
    ("s24", "pokemon_stadium_gb", "SZGHVlBML3Q", 2400, "Pokémon Stadium: comienzo (Game Boy)"),
    ("s23", "conker", "utsWdgtPRcI", 0, "Conker's Bad Fur Day: comienzo (juego con Expansion Pak opcional)"),
    ("s22", "super_mario64_file", "local:file.wav", 0, "Super Mario 64: selección de archivo (copiado de mario64_secretos)"),
    ("s21", "mario_kart64_yoshi", "bSb7MrN0bY8", 289, "Mario Kart 64: Moo Moo Farm / Yoshi Valley"),
    ("s20", "pokemon_stadium", "SZGHVlBML3Q", 900, "Pokémon Stadium: tramo del OST (Transfer Pak, Game Boy Tower)"),
    ("s19", "clayfighter", "QEOfCHkAFv0", 0, "ClayFighter Sculptor's Cut: Character Select"),
    ("s18", "superman64", "-QMsv-2szl0", 0, "Superman 64: Menu"),
    ("s17", "killer_instinct", "XkJtYY-kWhA", 0, "Killer Instinct (arcade): Attract Mode"),
    ("s16", "pokemon_snap", "ynTzb_BoHs4", 63, "Pokémon Snap: Title"),
    ("s15", "wave_race64_bahia", "R5JjdFqaVaw", 504, "Wave Race 64: Sunset Bay (hotel)"),
    ("s14", "fzero_x_dream", "EPn4kCTnJ-0", 163, "F-Zero X: Dream Chaser (iQue Player)"),
    ("s13", "perfect_dark", "r2vJ0UorSCI", 25, "Perfect Dark: Perfect Menu (Kirkhope)"),
    ("s12", "donkey_kong64", "uX2Dm7_HtU0", 0, "Donkey Kong 64: comienzo del OST"),
    ("s11", "body_harvest", "oCLoz9dCQ6c", 0, "Body Harvest: comienzo del OST"),
    ("s10", "animal_forest", "liqeh2f_uaI", 2, "Animal Forest (Dobutsu no Mori): medley"),
    ("s09", "mario_artist_paint", "WpBLlCT2NWM", 0, "Mario Artist Paint Studio: Title Theme (64DD)"),
    ("s08", "resident_evil2", "jWvwOyo3pdA", 1200, "Resident Evil 2: OST de PlayStation (la N64 usa versiones comprimidas)"),
    ("s07", "mario_party_minijuego", "iCuKqhnct4M", 1329, "Mario Party: Play A Mini-Game (los guantes)"),
    ("s06", "tetris64", "Cx5JqZ0yhew", 0, "Tetris 64: música del juego (105 s, se repite)"),
    ("s05", "ff6_terra", "ObccgHQdos0", 0, "Final Fantasy VI: Terra's Theme (SQUARE ENIX MUSIC; la demo mostraba a Terra)"),
    ("s04", "ff7_opening", "NoWU28L_ZmQ", 0, "Final Fantasy VII: Opening - Bombing Mission (SQUARE ENIX MUSIC)"),
    ("s03", "earthbound64", "b1uEOZ1JScs", 0, "EarthBound 64: música del tráiler de Space World 99 (60 s, se repite)"),
    ("s02", "mario_artist_talent", "XmC_8kg-SKo", 30, "Mario Artist Talent Studio: Talent Gallery (64DD)"),
    ("s01", "smash_bros64", "law_oQKRPN8", 90, "Super Smash Bros. (N64): comienzo del OST"),
    ("cierre", "super_mario64_creditos", "local:creditos.wav", 0, "Super Mario 64: créditos (copiado de mario64_secretos)"),
]


def _timeline():
    tl = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
    return float(tl["total"]), {e["id"]: float(e["t0"]) for e in tl["escenas"]}


def _ruta(esc, slug):
    return os.path.join(OST, f"{esc}_{slug}.wav")


def _bajar_uno(p, dur):
    esc, slug, fuente, desde, nota = p
    out = _ruta(esc, slug)
    if os.path.exists(out) and os.path.getsize(out) > 100000:
        return f"= {esc:7s} {slug}"
    if fuente.startswith("local:"):
        shutil.copy(os.path.join(MARIO64, fuente[6:]), out)
        return f"+ {esc:7s} {slug} (copia local)"
    largo = int(math.ceil(dur)) + MARGEN
    base = out[:-4]
    r = subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "-x", "--audio-format", "wav",
                        "--download-sections", f"*{desde}-{desde + largo}", "--force-keyframes-at-cuts",
                        "-o", base + ".%(ext)s", "https://www.youtube.com/watch?v=" + fuente],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    ok = os.path.exists(out) and os.path.getsize(out) > 100000
    return f"{'+' if ok else 'X'} {esc:7s} {slug} {fuente} {desde}s +{largo}s" + ("" if ok else "  " + r.stderr.strip()[-200:])


def bajar():
    os.makedirs(OST, exist_ok=True)
    total, t0s = _timeline()
    orden = [e for e, _ in sorted(t0s.items(), key=lambda kv: kv[1])]
    dur = {e: (t0s[orden[i + 1]] if i + 1 < len(orden) else total) - t0s[e] for i, e in enumerate(orden)}
    with ThreadPoolExecutor(4) as ex:
        for linea in ex.map(lambda p: _bajar_uno(p, dur[p[0]]), PISTAS):
            print(linea, flush=True)


def cargar(ruta):
    import soundfile as sf
    from scipy.signal import resample_poly
    x, sr = sf.read(ruta, always_2d=True)
    if sr != SR:
        g = np.gcd(sr, SR)
        x = resample_poly(x, SR // g, sr // g, axis=0)
    x = x[:, :2] if x.shape[1] >= 2 else np.repeat(x, 2, axis=1)
    fuerte = np.where(np.abs(x).max(1) > 0.02)[0]            # recorta el silencio inicial de la pista (intros suaves de los ripeos)
    return x[max(0, int(fuerte[0]) - int(.1 * SR)):] if len(fuerte) else x


def rampa(n, sube=True):
    r = np.linspace(0, 1, n) if sube else np.linspace(1, 0, n)
    return np.sin(r * np.pi / 2)[:, None]


def armar():
    import pyloudnorm as pyln
    import soundfile as sf
    total, t0s = _timeline()
    faltan = [p[0] for p in PISTAS if not os.path.exists(_ruta(p[0], p[1]))]
    if faltan:
        sys.exit(f"faltan pistas (python armar_musica_ost.py bajar): {faltan}")
    escenas = set(t0s)
    sin_pista = escenas - {p[0] for p in PISTAS}
    if sin_pista:
        sys.exit(f"escenas sin pista: {sorted(sin_pista)}")
    cortes = sorted(((t0s[p[0]], p) for p in PISTAS), key=lambda c: c[0])
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for k, (t0, p) in enumerate(cortes):
        t1 = cortes[k + 1][0] if k + 1 < len(cortes) else total
        largo = int((t1 - t0 + CRUCE) * SR)
        x = cargar(_ruta(p[0], p[1]))
        seg = x
        while len(seg) < largo:                                  # pista corta (tetris, earthbound): la repite con cruce
            c = min(nc, len(seg), len(x))
            seg = np.vstack([seg[:-c], seg[-c:] * rampa(c, False) + x[:c] * rampa(c), x[c:]])
        seg = seg[:largo].copy()
        l = meter.integrated_loudness(seg)
        seg *= 10 ** ((LUFS - l) / 20)
        seg[:SR if t0 == 0 else nc] *= rampa(SR if t0 == 0 else nc)
        seg[-nc:] *= rampa(nc, False)
        i0 = int(max(0.0, t0 - CRUCE / 2) * SR) if t0 > 0 else 0
        out[i0:i0 + len(seg)] += seg[:len(out) - i0]
        print(f"{t0:7.1f}-{t1:7.1f}  {p[0]:7s} {p[1]:24s} {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    # SONIDO ORIGINAL (el usuario, 26-oct-2026): en los beats con ambiente_por la banda sonora se aparta y se oye el juego
    sys.path.insert(0, AQUI)
    import guion
    vols = guion.SECUENCIA.get("ambiente_por", {})
    if vols and os.path.exists(os.path.join(AQUI, "beats.json")):
        gan = np.ones(len(out))
        r = int(.5 * SR)
        for b in json.load(open(os.path.join(AQUI, "beats.json"), encoding="utf-8")):
            if vols.get(b["id"], 0) > 0:
                i0, i1 = int(b["t0"] * SR), min(len(out), int(b["t1"] * SR))
                g = 10 ** (APARTA_DB / 20)
                gan[i0:i1] = np.minimum(gan[i0:i1], g)
                gan[max(0, i0 - r):i0] = np.minimum(gan[max(0, i0 - r):i0], np.linspace(1, g, i0 - max(0, i0 - r)))
                gan[i1:i1 + r] = np.minimum(gan[i1:i1 + r], np.linspace(g, 1, len(gan[i1:i1 + r])))
        out *= gan[:, None]
        print(f"banda sonora apartada {APARTA_DB} dB en {sum(1 for v in vols.values() if v > 0)} beats con sonido original")
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join(AQUI, "audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s; timeline {total:.2f} s)")


if __name__ == "__main__":
    bajar() if sys.argv[1:] == ["bajar"] else armar()
