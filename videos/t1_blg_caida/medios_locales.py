# -*- coding: utf-8 -*-
"""Clip de cada beat (medios/scene-NNN.mp4) cortado de las fuentes locales. En este video el FX `video` de efectos.py cubre los
919 s sin huecos, así que estos clips solo sirven para el Montaje del panel y el chequeo: van a 640x360, sin audio, para no gastar
disco (C: anda corto). Cada escena usa una fuente de SU serie. Salta lo que falte (t1_koi_worlds vive en E:); sin spoiler en el
gancho. python videos/lol_final_previa/medios_locales.py [--rehacer]"""
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
    """lol_final_previa: el clip de cada beat sale del FX `video` de efectos.py que lo cubre (misma fuente, mismo segundo)"""
    rehacer = "--rehacer" in sys.argv
    sys.path[:0] = [D, os.path.join(D, "..", "..", "nucleo")]
    import efectos
    beats = json.load(open(os.path.join(D, "beats.json"), encoding="utf-8"))
    vids = [f for f in efectos.FX if f.get("tipo") == "video"]
    hechos, faltan = 0, []
    for b in beats:
        mid = (b["t0"] + b["t1"]) / 2
        f = next((f for f in vids if f["de"] <= mid < f["a"]), None)
        out = os.path.join(D, "medios", b["id"] + ".mp4")
        if f is None or not os.path.exists(f["ruta"]):      # beat sobre fondo animado (sin VOD): el escenario, solo para el Montaje
            f = dict(ruta=os.path.join(D, "medios", "_fuente", "r_escenario.mp4"), desde=0.0, de=b["t0"], vel=1)
            faltan.append(b["id"])
        if os.path.exists(out) and not rehacer:
            continue
        L = b["t1"] - b["t0"] + .4
        s0 = max(0.0, f["desde"] + max(0.0, f.get("vel", 1) or 0) * (b["t0"] - f["de"]))
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{s0:.2f}", "-i", f["ruta"], "-t", f"{L:.2f}", "-an", "-vf",
                        "scale=640:360,fps=30,tpad=stop_mode=clone:stop_duration=30", "-t", f"{L:.2f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "30", "-pix_fmt", "yuv420p", out], check=True)
        hechos += 1
    print(f"{hechos} clips cortados · sin fuente: {' '.join(faltan) or '—'}")


if __name__ == "__main__":
    main()
