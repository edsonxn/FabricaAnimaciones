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
      6: "2026-11-08 08-40-55.mp4", 7: "2026-11-08 08-41-30.mp4", 8: "2026-11-08 08-42-04.mp4", 10: "2026-11-08 08-40-40.mp4"}   # g10: notificación de WhatsApp en 0,7-7,3 s (privacidad, 8-nov): solo desde 9 s   # 8-nov: orcos
LARGO = {1: 67.8, 2: 31.4, 3: 40.8, 4: 62.7, 5: 32.5, 6: 30.3, 7: 7.6, 8: 43.0, 10: 12.3}
# por escena: lista de (grabación, segundo de inicio) que se reparte entre sus beats en orden
PLAN = {   # sin repetir tramo de ninguna grabación (7-nov, comprobado a mano con `--ver`)
    "casa1": [(1, 34.0), (1, 51.0), (4, 53.0), (2, 4.0)],      # scene-044 (post de Spoken) va con el clip de KEL, no aquí
    "casa2": [(1, 4.0), (1, 13.6)],
    "casa3": [(2, 16.0), (4, 26.0), (4, 4.0)],
    "casa4": [(5, 4.0), (3, 0.0), (3, 9.0), (3, 17.0), (3, 27.0), (1, 44.0), (4, 12.0), (4, 44.0)],
}
# el PNJ habla desde este segundo de la grabación: el post (voz callada) se alinea ahí
SALTA = {"scene-053"}   # 9-nov: tramo de 40 s; 053 ya es casi todo el #14 (se queda el clip remapeado)
# 3.ª versión (Overgear al min 4, posts largos): tramo exacto por beat, sin repetir (comprobado a mano)
EXPL = {"scene-049": (2, 4.0), "scene-052": (8, 0.0)}   # 9-nov: 050 y 051 los alinea OYE (Willem / Kaltunk)
OYE = {"casa1": (1, 8.1, "casa1_1"), "casa2": (6, 2.6, "casa2_0")}


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
    """scene-064 (9-nov, más peso a los orcos): Razor Hill (g7) hasta el fin de casa4_4 → Kaltunk HABLANDO (g6 desde 2,6 s, 23,8 s:
    «Por fin ha llegado el momento, recluta…») → la frase casa4b → Gornek HABLANDO (g8 desde 23,1 s, 10,5 s: «¿Otro de los reclutas
    de Kaltunk, eh?…») y su tienda hasta el fin del beat. El audio va como PISTAS oye_kaltunk / oye_gornek (mismos segundos)."""
    b = next(x for x in json.load(open("beats.json", encoding="utf-8")) if x["id"] == "scene-064")
    tl = json.load(open("timeline.json", encoding="utf-8"))
    fin = {f["key"]: f["t1"] for e in tl["escenas"] for f in e["frases"]}
    ini = {f["key"]: f["t0"] for e in tl["escenas"] for f in e["frases"]}
    tk, tg = fin["casa4_4"] + .15, fin["casa4b_0"] + .15
    corte = ini["casa4b_0"] - .1
    d1, d2 = tk - b["t0"], corte - tk
    s8 = 23.1 - (tg - corte)
    d3 = b["t1"] - corte
    assert 2.6 + d2 <= 30.3 and s8 + d3 <= 43.0 and s8 >= 0, (d2, s8, d3)
    partes = [(7, 1.0, d1), (6, 2.6, d2), (8, s8, d3)]
    args, fil = [], []
    for k, (g, s, d) in enumerate(partes):
        args += ["-ss", f"{s:.3f}", "-t", f"{d:.3f}", "-i", os.path.join(D, GR[g])]
        fil.append(f"[{k}:v]scale=1920:1080,fps=30,setpts=PTS-STARTPTS[v{k}];[{k}:a]aresample=48000,asetpts=PTS-STARTPTS[a{k}]")
    fil.append("".join(f"[v{k}][a{k}]" for k in range(3)) + "concat=n=3:v=1:a=1[v][a]")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *args, "-filter_complex", ";".join(fil), "-map", "[v]", "-map", "[a]",
                    "-c:v", "libx264", "-preset", "fast", "-crf", "18", "-c:a", "aac", "-b:a", "192k", "medios/scene-064.mp4"], check=True)
    print(f"scene-064 <- g7 {d1:.1f} s + g6 Kaltunk {d2:.1f} s + g8 desde {s8:.1f} s ({d3:.1f} s; Gornek habla en {tg:.1f})")

if __name__ == "__main__":
    main(escribir="--ver" not in sys.argv)
