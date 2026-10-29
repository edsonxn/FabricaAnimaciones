# -*- coding: utf-8 -*-
"""Arma audio/musica.wav con la BANDA SONORA OFICIAL de World of Warcraft (el usuario, 29-oct-2026: «Música: banda sonora oficial
de WoW»; misma receta que videos/er_malenia_atrocidades/armar_musica_ost.py). Pistas en audio/ost/ (yt-dlp, 29-oct):
  invincible «Invincible» (4n6WP9qHyRM) · arthas_hijo «Arthas, My Son» (Neal Acree, ZRsToniFCYo) · tirisfal (Wowmusicable,
  IwlPgQtGguw) · costasur «Hillsbrad Foothills» (SgA_w6vOG20) · forjaz (Wowmusicable, X1eU2usWg3M) · peste_oeste (Wowmusicable,
  X0UTcGvIbzU) · peste_este (DwZlUFQqj2A) · the_culling «The Culling» (Glenn Stafford - Topic, hithOeycCHE) · stratholme «Culling
  of Stratholme General Music» (WoWMusicGuru, eghspESM7v8) · naxxramas (ddcDtn0GyrQ) · monasterio (Wowmusicable, RO-V1npJFa8) ·
  capilla1/capilla2 «Light's Hope Chapel» (GJdq0lQD9ww, RECzfbvL8-0) · acherus «Ebon Hold» (WoWMusicGuru, 44mqaOtLhbA) ·
  corona «Icecrown» (WoWMusicGuru, ubCaPKfESkE).
Cada sección empieza en el t0 de su escena (timeline.json) y dura hasta la siguiente; pistas en orden (archivo, desde s), fundido
cruzado de 2 s, todas a la misma sonoridad. Content ID: si llega un reclamo, cambiar la pista aquí → `mezcla` → `final`.
    python armar_musica_ost.py        (desde la carpeta del video; luego `python fab.py gaia_crematoria mezcla`)
"""
import json
import os

import numpy as np
import pyloudnorm as pyln
import soundfile as sf
from scipy.signal import resample_poly

SR = 48000
CRUCE = 2.0
LUFS = -23.0

# (escena donde empieza la sección, [(pista, desde s), …])
SECCIONES = [
    ("gancho", [("arthas_hijo", 0)]),                         # la capilla bajo la lluvia de sangre
    ("elena", [("tirisfal", 0)]),                             # Rémol, el arroyo helado, el orbe
    ("mano_plata", [("costasur", 0)]),                        # Lordaeron en paz, la posada de Costasur
    ("forja", [("forjaz", 0)]),                               # Forjaz, la Gran Yunque
    ("eitrigg", [("peste_oeste", 0), ("tirisfal", 90)]),      # Vega del Amparo, el orco, el juicio
    ("plaga", [("the_culling", 0)]),                          # la Plaga, Stratholme, Balnazzar
    ("complot", [("stratholme", 0)]),                         # el complot y la traición en las puertas
    ("testigo", [("naxxramas", 0)]),                          # Ribalimpia, Naxxramas, los susurros
    ("culpa", [("monasterio", 0)]),                           # Renault, la Cruzada Escarlata
    ("cta_mitad", [("tirisfal", 100)]),                       # pausa cálida
    ("darion_busca", [("naxxramas", 240)]),                   # Darion contra su padre
    ("monasterio", [("monasterio", 240)]),                    # el Monasterio y el misterio
    ("ermitano", [("peste_este", 0)]),                        # el ermitaño, Taelan, la cadena
    ("en_suenos", [("peste_oeste", 0), ("arthas_hijo", 60)]),  # «En sueños»
    ("capilla_1", [("capilla1", 0), ("capilla2", 0)]),        # primera batalla de la Capilla
    ("acherus", [("acherus", 0)]),                            # el caballero de la muerte
    ("alba", [("corona", 0)]),                                # «La luz del alba»
    ("epilogo", [("invincible", 0)]),                         # Corona de Hielo, Legion
    ("cierre", [("capilla2", 40)]),                           # dos padres, dos hijos
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


def t0_de(tl, id_):
    for e in tl["escenas"]:
        if e["id"] == id_:
            return float(e.get("t0", e.get("inicio", 0.0)))
    raise SystemExit(f"escena {id_} no está en timeline.json")


def main():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    total = float(tl.get("total") or tl.get("duracion") or max(e["fin"] for e in tl["escenas"]))
    secs = [(0.0 if i == 0 else t0_de(tl, sid), pistas) for i, (sid, pistas) in enumerate(SECCIONES)]
    meter = pyln.Meter(SR)
    out = np.zeros((int(total * SR) + SR, 2))
    nc = int(CRUCE * SR)
    for i, (t0, pistas) in enumerate(secs):
        t1 = secs[i + 1][0] if i + 1 < len(secs) else total
        largo = int((t1 - t0 + CRUCE) * SR)
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
        while len(seg) < largo:                                # si aún falta, repite la primera pista
            x = cargar(pistas[0][0])
            k = min(nc, len(seg), len(x))
            seg[-k:] = seg[-k:] * rampa(k, False) + x[:k] * rampa(k)
            seg = np.vstack([seg, x[k:]])
        seg = seg[:largo].copy()
        l = meter.integrated_loudness(seg)
        seg *= 10 ** ((LUFS - l) / 20)
        seg[:SR if t0 == 0 else nc] *= rampa(SR if t0 == 0 else nc)
        seg[-nc:] *= rampa(nc, False)
        i0 = int(max(0.0, t0 - CRUCE / 2) * SR) if t0 > 0 else 0
        out[i0:i0 + len(seg)] += seg[:len(out) - i0]
        print(f"{t0:7.1f}-{t1:7.1f}  {' + '.join(p for p, _ in pistas):26s}  {l:6.1f} LUFS -> {LUFS}")
    out = out[:int(total * SR)]
    out[-4 * SR:] *= rampa(4 * SR, False)
    sf.write(os.path.join("audio", "musica.wav"), out.astype(np.float32), SR, subtype="FLOAT")
    print(f"audio/musica.wav listo ({len(out) / SR:.2f} s)")


if __name__ == "__main__":
    main()
