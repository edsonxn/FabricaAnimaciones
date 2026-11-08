# -*- coding: utf-8 -*-
"""Clips PROPIOS de las escenas casa* (los add-ons del usuario): recortes de sus grabaciones de OBS
(D:\\wowForeverVoces\\grabaciones_obs) a medios/scene-NNN.mp4, con su AUDIO (el PNJ doblado), de la duración exacta del beat.
En el beat del «Escucha» (casa1) y de la posada (casa3) el recorte se alinea para que la voz callada (post) caiga en el
tramo donde habla el PNJ (g1 Willem 4-12 s, g4 Mortero 4-10 s). Correr ANTES de `bajar` (bajar salta los medios que ya existen).
  python _obs.py          (escribe y lista)        python _obs.py --ver    (solo lista)
"""
import json
import os
import subprocess
import sys

os.chdir(os.path.dirname(os.path.abspath(__file__)))
D = r"D:\wowForeverVoces\grabaciones_obs"
GR = {1: "2026-11-07 11-35-43.mp4", 2: "2026-11-07 11-37-50.mp4", 3: "2026-11-07 11-39-04.mp4",
      4: "2026-11-07 12-12-17.mp4", 5: "2026-11-07 12-13-27.mp4",
      6: "2026-11-08 08-40-55.mp4", 7: "2026-11-08 08-41-30.mp4", 8: "2026-11-08 08-42-04.mp4", 10: "2026-11-08 08-40-40.mp4"}   # 8-nov: orcos
LARGO = {1: 67.8, 2: 31.4, 3: 40.8, 4: 62.7, 5: 32.5, 6: 30.3, 7: 7.6, 8: 43.0, 10: 12.3}
# por escena: lista de (grabación, segundo de inicio) que se reparte entre sus beats en orden
PLAN = {   # sin repetir tramo de ninguna grabación (7-nov, comprobado a mano con `--ver`)
    "casa1": [(1, 34.0), (1, 51.0), (4, 53.0), (2, 4.0)],      # scene-044 (post de Spoken) va con el clip de KEL, no aquí
    "casa2": [(1, 4.0), (1, 13.6)],
    "casa3": [(2, 16.0), (4, 26.0), (4, 4.0)],
    "casa4": [(5, 4.0), (3, 0.0), (3, 9.0), (3, 17.0), (3, 27.0), (1, 44.0), (4, 12.0), (4, 44.0)],
}
# el PNJ habla desde este segundo de la grabación: el post (voz callada) se alinea ahí
SALTA = {"scene-064"}   # 8-nov: lo arma _orcos_064() (3 grabaciones encadenadas)
# 3.ª versión (Overgear al min 4, posts largos): tramo exacto por beat, sin repetir (comprobado a mano)
EXPL = {"scene-049": (4, 32.0), "scene-050": (1, 34.0), "scene-051": (2, 4.0), "scene-052": (1, 46.0), "scene-054": (1, 21.0),
        "scene-055": (1, 25.0), "scene-056": (2, 16.0), "scene-057": (4, 40.0), "scene-059": (5, 4.0), "scene-060": (5, 8.0),
        "scene-061": (3, 0.0), "scene-062": (3, 6.0), "scene-063": (3, 14.0), "scene-064": (3, 24.0), "scene-065": (4, 48.0),
        "scene-066": (1, 56.0), "scene-067": (10, 0.0), "scene-068": (4, 20.0)}
OYE = {"casa1": (1, 4.0, "casa1_4"), "casa3": (4, 4.0, "casa3_1")}


def main(escribir=True):
    beats = json.load(open("beats.json", encoding="utf-8"))
    esc = json.load(open("_beat_escena.json", encoding="utf-8"))
    tl = json.load(open("timeline.json", encoding="utf-8"))
    fin_frase = {f["key"]: f["t1"] for e in tl["escenas"] for f in e["frases"]}
    usados = {}
    for b in beats:
        e = esc.get(b["id"], "")
        if not e.startswith("casa") or b["id"] in SALTA:
            continue
        k = usados.get(e, 0)
        usados[e] = k + 1
        g, s = EXPL.get(b["id"]) or PLAN[e][min(k, len(PLAN[e]) - 1)]
        dur = b["t1"] - b["t0"]
        for gg, oye, clave in OYE.values():      # el post puede caer en el beat de la escena siguiente
            tpost = fin_frase.get(clave)
            if tpost is not None and b["t0"] <= tpost + .3 < b["t1"]:
                g, s = gg, max(0.0, oye - (tpost + .15 - b["t0"]))
        s = min(s, LARGO[g] - dur - .1)
        out = os.path.join("medios", b["id"] + ".mp4")
        print(f"{b['id']} {e:6s} {b['t0']:7.2f}-{b['t1']:7.2f} ({dur:4.1f} s) <- g{g} desde {s:5.1f} s")
        if escribir:
            os.makedirs("medios", exist_ok=True)
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{s:.3f}", "-i", os.path.join(D, GR[g]), "-t", f"{dur:.3f}",
                            "-vf", "scale=1920:1080,fps=30", "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac",
                            "-b:a", "192k", "-ar", "48000", out], check=True)


def _orcos_064():
    """scene-064 (543,15-567,47): Razor Hill (g7) hasta el fin de casa4_4 + Kaltunk HABLANDO (g6 desde 2,6 s: «Por fin ha llegado el
    momento, recluta…», se oye como PISTA oye_kaltunk) durante el post de 13 s + Gornek (g8) bajo casa5_0."""
    b = next(x for x in json.load(open("beats.json", encoding="utf-8")) if x["id"] == "scene-064")
    tl = json.load(open("timeline.json", encoding="utf-8"))
    tpost = next(f["t1"] for e in tl["escenas"] for f in e["frases"] if f["key"] == "casa4_4")
    d1 = tpost + .15 - b["t0"]
    d2 = 13.6
    d3 = b["t1"] - b["t0"] - d1 - d2
    partes = [(7, 1.0, d1), (6, 2.6, d2), (8, 20.0, d3)]
    args, fil = [], []
    for k, (g, s, d) in enumerate(partes):
        args += ["-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", os.path.join(D, GR[g])]
        fil.append(f"[{k}:v]scale=1920:1080,fps=30,setpts=PTS-STARTPTS[v{k}];[{k}:a]aresample=48000,asetpts=PTS-STARTPTS[a{k}]")
    fil.append("".join(f"[v{k}][a{k}]" for k in range(3)) + "concat=n=3:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", ";".join(fil), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "medios/scene-064.mp4"], check=True)
    print(f"scene-064 <- g7 {d1:.1f} s + g6 (Kaltunk) {d2:.1f} s + g8 {d3:.1f} s")


if __name__ == "__main__":
    main(escribir="--ver" not in sys.argv)
    if "--ver" not in sys.argv:
        _orcos_064()
