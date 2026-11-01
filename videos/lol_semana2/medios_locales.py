# -*- coding: utf-8 -*-
"""Clip de cada beat (medios/scene-NNN.mp4) cortado de las fuentes locales. En este video el FX `video` de efectos.py cubre los
919 s sin huecos, así que estos clips solo sirven para el Montaje del panel y el chequeo: van a 640x360, sin audio, para no gastar
disco (C: anda corto). Cada escena usa una fuente de SU serie. Salta lo que falte (t1_koi_worlds vive en E:); sin spoiler en el
gancho. python videos/lol_semana2/medios_locales.py [--rehacer]"""
import json
import os
import subprocess
import sys

D = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
PROBE = r"C:\ffmpeg\bin\ffprobe.exe"
T1 = os.path.abspath(os.path.join(D, "..", "t1_koi_worlds", "medios", "_fuente"))
KC = os.path.abspath(os.path.join(D, "..", "cfo_kc_jugadas", "medios", "_fuente"))
P = os.path.join(D, "medios", "_fuente")
FUENTES = {"gancho": [(P, "blte_j3"), (P, "lotl_j1"), (P, "lyig_j2")], "correcciones": [(P, "lyig_j1")], "donde": [(KC, "g1_j4")],
           "t1ko": [(T1, "g1_j5"), (T1, "g2_j2"), (T1, "g2_j1")], "lyig": [(P, "lyig_j1"), (P, "lyig_j2"), (P, "lyig_j3")],
           "kccf": [(KC, "g2_j4"), (KC, "g2_j8"), (KC, "g1_j8")], "blte": [(P, "blte_j3"), (P, "blte_j2"), (P, "blte_g3")],
           "lotl": [(P, "lotl_j1"), (P, "lotl_j2"), (P, "lotl_j3")], "g2hl": [(P, "g2hl_j3"), (P, "g2hl_j2"), (P, "g2hl_j1")],
           "tabla4": [(P, "lyig_j1")], "kcmk": [(P, "kcmk_j1"), (P, "kcmk_j3"), (P, "kcmk_j2")], "loly": [(P, "loly_j1"), (P, "loly_j2"), (P, "loly_j3")],
           "hlbl": [(P, "hlbl_j1"), (P, "hlbl_g2"), (P, "hlbl_g2f")], "tabla5": [(P, "hlbl_j1")], "sem": [(P, "hlbl_j1"), (P, "kcmk_fin"), (P, "loly_fin2"), (P, "blte_j1")],
           "llave": [(P, "hlbl_j1")]}


def dur(r):
    s = subprocess.run([PROBE, "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", r], capture_output=True, text=True)
    return float(s.stdout.strip() or 0)


def main():
    rehacer = "--rehacer" in sys.argv
    tl = json.load(open(os.path.join(D, "timeline.json"), encoding="utf-8"))
    beats = json.load(open(os.path.join(D, "beats.json"), encoding="utf-8"))
    esc = [(e["id"], e["t0"], e["t1"]) for e in tl["escenas"]]
    largo, cursor, hechos, faltan = {}, {}, 0, []
    for b in beats:
        mid = (b["t0"] + b["t1"]) / 2
        sid = next((s for s, a, z in esc if a <= mid < z), esc[-1][0])
        lista = [os.path.join(c, n + ".mp4") for c, n in FUENTES[sid.split("_")[0]]]
        lista = [r for r in lista if os.path.exists(r)]
        out = os.path.join(D, "medios", b["id"] + ".mp4")
        if not lista:
            faltan.append(b["id"])
            continue
        if os.path.exists(out) and not rehacer:
            continue
        L = b["t1"] - b["t0"] + .4
        r = lista[hechos % len(lista)]
        largo.setdefault(r, dur(r))
        s = cursor.get(r, 0.0)
        if s + L > largo[r] - .2:
            s = 0.0
        cursor[r] = s + L
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{s:.2f}", "-i", r, "-t", f"{L:.2f}", "-an", "-vf", "scale=640:360,fps=30",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p", out], check=True)
        hechos += 1
    print(f"{hechos} clips cortados · sin fuente aún: {' '.join(faltan) or '—'}")


if __name__ == "__main__":
    main()
