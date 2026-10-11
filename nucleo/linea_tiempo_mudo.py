# -*- coding: utf-8 -*-
"""timeline.json para videos SIN VOZ (guion.py: SIN_VOZ = True).

Cada escena del guion es una sección musical y trae "compases": N (compás = UNIDAD de 4 tiempos a BPM). No hay
frases ni palabras: las anclas son los tiempos (múltiplos del pulso) que escenas.py calcula desde BEAT.
La suma de compases debe dar DURACION (si se indica). Campos que escribe además de los normales:
  escenas[-1]["fin_musica"]  instante del golpe final de la música (por defecto TOTAL - 3 pulsos)."""
import json

import config

ESCENAS = config.ESCENAS
BPM = float(config.BPM)
BEAT = 60 / BPM
BARRA = 4 * BEAT
import os
# VOZ_ANCLADA: la narración (voz/palabras.json, generada con voz + seleccionar) se coloca en los pulsos "anclas" de cada
# escena; la imagen y la música no dependen de su duración (las frases deben caber en su época: se avisa si no).
PAL = json.load(open("voz/palabras.json", encoding="utf-8")) if os.path.exists("voz/palabras.json") else {}
escenas, t = [], 0.0
for k, e in enumerate(ESCENAS):
    n = int(e["compases"])
    esc = {kk: vv for kk, vv in e.items() if kk not in ("frases", "anclas")}
    frases = []
    for i, txt in enumerate(e.get("frases") or []):
        key = f"{e['id']}_{i}"
        if key not in PAL or "anclas" not in e:
            continue
        p = PAL[key]
        t0 = e["anclas"][i] * BEAT
        words = [dict(w=w["w"], s=round(t0 + w["s"], 3), e=round(t0 + w["e"], 3)) for w in p["words"]]
        frases.append(dict(key=key, texto=txt, t0=round(t0, 3), t1=round(t0 + p["dur"], 3), words=words))
    for a_, b_ in zip(frases, frases[1:]):
        if a_["t1"] > b_["t0"] + 0.05:
            print(f"AVISO: '{a_['key']}' ({a_['t1'] - a_['t0']:.2f}s) pisa a '{b_['key']}' por {a_['t1'] - b_['t0']:.2f}s: acórtala")
    esc.update(t0=round(t, 4), t1=round(t + n * BARRA, 4), compases=n, frases=frases,
               fin_voz=round(frases[-1]["t1"] if frases else t, 3), beats=4 * n)
    escenas.append(esc)
    t += n * BARRA
TOTAL = round(t, 4)
if config.DURACION is not None and abs(TOTAL - config.DURACION) > 0.02:
    raise SystemExit(f"Los compases suman {TOTAL:.3f}s y DURACION es {config.DURACION}s: ajusta BPM o compases "
                     f"(60 s a 128 BPM = 32 compases).")
escenas[-1]["fin_musica"] = round(TOTAL - 3 * BEAT, 4)
trans = [dict(t=escenas[i]["t1"], t0=round(escenas[i]["t1"] - 0.05, 4), t1=round(escenas[i]["t1"] + 0.05, 4),
              tipo="continua", de=escenas[i]["id"], a=escenas[i + 1]["id"]) for i in range(len(escenas) - 1)]
tl = dict(bpm=BPM, beat=BEAT, unidad=4, total=TOTAL, titulo=config.TITULO, estilo=config.ESTILO_VISUAL,
          sin_voz=not PAL, anclada=bool(PAL), escenas=escenas, transiciones=trans)
json.dump(tl, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"sin voz: {len(escenas)} secciones, {TOTAL:.3f}s a {BPM} BPM ({sum(e['compases'] for e in escenas)} compases)")
for e in escenas:
    print(f"{e['id']:12s} {e['t0']:7.2f} -> {e['t1']:7.2f}  ({e['compases']} compases)")
