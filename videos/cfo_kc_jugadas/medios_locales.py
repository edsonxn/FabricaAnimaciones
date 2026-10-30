# -*- coding: utf-8 -*-
"""Clips de cada beat (medios/scene-NNN.mp4) cortados de las FUENTES LOCALES 1080p (medios/_fuente/g<p>_j<k>.mp4, VOD de Twitch
LATAM) en vez de `busquedas` + `bajar` de YouTube: el VOD de YouTube de la G2 no salía aún (29-oct-2026) y las fuentes ya están
medidas. Por sección, una lista de (fuente, segundo); cada beat sigue donde se quedó el anterior en esa fuente (sin repetir
plano). SIN SPOILER: antes del desenlace de cada partida, nada de nexo ni pantalla de victoria. Las jugadas las tapa el FX
`video`: su clip es solo relleno. python videos/cfo_kc_jugadas/medios_locales.py [--rehacer]  (salta las fuentes que falten)"""
import json
import os
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
G1_PRE = [("g1_j2", 0), ("g1_j5", 0), ("g1_j3", 0), ("g1_j1", 0), ("g1_j4", 0)]           # G1 sin desenlace
G1_TODO = [("g1_j8", 0), ("g1_j6", 140), ("g1_j7", 0), ("g1_j6", 0)]
G2_PRE = [("g2_j1", 0), ("g2_j2", 0), ("g2_j3", 0), ("g2_j4", 0), ("g2_j5", 0)]          # G2 sin desenlace
G2_TODO = [("g2_j8", 100), ("g2_j6", 0), ("g2_j7", 20), ("g2_j4", 0)]
FUENTES = {
    "gancho": [("g1_j4", 18), ("g1_j6", 40), ("g1_j2", 20), ("g1_j5", 20), ("g1_j6", 110)],
    "juego": [("g1_j3", 0), ("g1_j2", 0), ("g1_j5", 0)],
    "draft1": [("g1_j1", 0), ("g1_j2", 40), ("g1_j3", 36)],
    "curva1": G1_TODO, "draft2": G2_PRE + G1_TODO,
    "curva2": G2_TODO + G1_TODO, "predicciones": G2_TODO + G1_TODO, "boleta_kc": G1_TODO + G2_TODO,
    "boleta_cfo": G2_TODO + G1_TODO, "numeros": G1_TODO + G2_TODO, "sigue": G2_TODO + G1_TODO, "cierre": G1_TODO + G2_TODO,
}


def relleno(sid):
    """jugadas (las tapa el FX `video`): cualquier tramo de su partida"""
    n = int("".join(c for c in sid.split("_")[0] if c.isdigit()))
    return G1_PRE if n <= 5 else G2_PRE


def dur(n):
    r = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                        os.path.join(D, "medios", "_fuente", n + ".mp4")], capture_output=True, text=True)
    return float(r.stdout.strip() or 0)


def main():
    rehacer = "--rehacer" in sys.argv
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    beats = json.load(open(os.path.join(D, "beats.json"), encoding="utf-8"))
    esc = [(e["id"], e["t0"], e["t1"]) for e in tl["escenas"]]
    hay = {f[:-4] for f in os.listdir(os.path.join(D, "medios", "_fuente")) if f.endswith(".mp4")}
    largo = {n: dur(n) for n in hay}
    cursor, k_sec, hechos, faltan = {}, {}, 0, []
    for b in beats:
        mid = (b["t0"] + b["t1"]) / 2
        sid = next((s for s, a, z in esc if a <= mid < z), esc[-1][0])
        lista = [x for x in FUENTES.get(sid) or relleno(sid) if x[0] in hay]
        L = b["t1"] - b["t0"] + .4
        if not lista:
            faltan.append(b["id"])
            continue
        k = k_sec.get(sid, 0)
        for intento in range(len(lista)):
            n, s0 = lista[(k + intento) % len(lista)]
            s = max(s0, cursor.get((sid, n, s0), s0))
            if s + L <= largo[n] - .2:
                break
            cursor[(sid, n, s0)] = s0                 # fuente agotada: vuelve a su inicio la próxima vez
        else:
            n, s0 = lista[k % len(lista)]
            s = s0
        k_sec[sid] = k + 1
        cursor[(sid, n, s0)] = s + L
        out = os.path.join(D, "medios", b["id"] + ".mp4")
        if os.path.exists(out) and not rehacer:
            continue
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{s:.2f}", "-i", os.path.join(D, "medios", "_fuente", n + ".mp4"),
                        "-t", f"{L:.2f}", "-an", "-vf", "scale=1920:1080,fps=30", "-c:v", "libx264", "-preset", "veryfast",
                        "-crf", "18", "-pix_fmt", "yuv420p", out], check=True)
        hechos += 1
    print(f"{hechos} clips cortados · sin fuente aún: {' '.join(faltan) or '—'}")


if __name__ == "__main__":
    main()
