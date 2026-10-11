# -*- coding: utf-8 -*-
"""Construye timeline.json: fuente única de verdad para voz, música, SFX y animación.

- Cada escena (salvo la última) dura un número entero de compases (o medios compases) -> los
  cambios de escena caen en tiempo fuerte.
- Con DURACION fija, se busca el BPM (108-132) para que el video dure exactamente eso.
  Con DURACION = None se usa guion.BPM (120 por defecto) y la duración natural.
Márgenes por defecto (s) — cualquier escena puede sobrescribirlos con "pre"/"post" en guion.py.
"""
import json
import math

import config

PRE_PRIMERA, POST_PRIMERA = 1.10, 0.45     # la primera escena deja una entrada musical
PRE_ULTIMA, POST_ULTIMA = 0.45, 2.6        # la última incluye la tarjeta final
PRE_ITEM, POST_ITEM = 0.30, 0.40
GAP_TITULO = 0.42                          # tras "Número X: ..."
GAP = config.GAP                           # 0.30 por defecto; guion.py puede fijar GAP
ULTIMA_HOLGURA = (0.0, 2.2)                # con DURACION fija, la última escena puede estirarse

if getattr(config._g, "AUDIO_EXTERNO", None):   # el audio ya viene grabado: se transcribe y ese es el timeline
    import linea_tiempo_audio  # noqa: F401
    raise SystemExit(0)

if config.SIN_VOZ:                       # video sin narración: timeline por compases (sin voz/palabras.json)
    import linea_tiempo_mudo  # noqa: F401
    raise SystemExit(0)

ESCENAS = config.ESCENAS
pal = json.load(open("voz/palabras.json", encoding="utf-8"))


def margenes(k, e):
    if k == 0:
        pre, post = PRE_PRIMERA, POST_PRIMERA
    elif k == len(ESCENAS) - 1:
        pre, post = PRE_ULTIMA, POST_ULTIMA
    else:
        pre, post = PRE_ITEM, POST_ITEM
    return e.get("pre", pre), e.get("post", post)


def min_dur(k, e):
    durs = [pal[f"{e['id']}_{i}"]["dur"] for i in range(len(e["frases"]))]
    pre, post = margenes(k, e)
    gaps = ((GAP_TITULO if "num" in e else GAP) + GAP * (len(durs) - 2)) if len(durs) > 1 else 0.0
    return pre + sum(durs) + gaps + post


mins = [min_dur(k, e) for k, e in enumerate(ESCENAS)]
print("mínimos:", [round(m, 2) for m in mins], "suma", round(sum(mins), 2))

# ---- tempo y cuantización
if config.DURACION is None:
    BPM = float(config.BPM)
    UNIDAD = 4
    barra = UNIDAD * 60 / BPM
    COMPASES = [math.ceil(m / barra - 1e-9) for m in mins[:-1]]
    beat = 60 / BPM
    TOTAL = round(sum(COMPASES) * barra + math.ceil(mins[-1] / beat) * beat, 4)
    print(f"duración natural: {TOTAL:.2f}s a {BPM} BPM")
else:
    TOTAL = float(config.DURACION)
    mejor = None
    for unidad, castigo in ((4, 0.0), (2, 1.5)):          # compás entero; si no cabe, medio compás
        for bpm10 in range(1080, 1321):
            bpm = bpm10 / 10
            barra = unidad * 60 / bpm
            compases = [math.ceil(m / barra - 1e-9) for m in mins[:-1]]
            ultima = TOTAL - sum(compases) * barra
            extra = ultima - mins[-1]
            if not (ULTIMA_HOLGURA[0] <= extra <= ULTIMA_HOLGURA[1]):
                continue
            holgura = sum(c * barra - m for c, m in zip(compases, mins[:-1]))
            costo = castigo + abs(bpm - config.BPM) * 0.05 + holgura * 0.1 + abs(extra - 1.0) * 0.3
            if mejor is None or costo < mejor[0]:
                mejor = (costo, bpm, compases, extra, holgura, unidad)
    if mejor is None:
        raise SystemExit(f"No hay BPM que encaje en {TOTAL}s (voz+márgenes = {sum(mins):.1f}s). "
                         "Opciones: DURACION = None (natural), otra DURACION, o recortar/alargar el guion.")
    _, BPM, COMPASES, EXTRA, HOLG, UNIDAD = mejor
    print(f"BPM={BPM}  unidad={UNIDAD} beats  bloques={COMPASES}  holgura={HOLG:.2f}s  extra última={EXTRA:.2f}s")
BEAT = 60 / BPM
BARRA = UNIDAD * BEAT

# ---- colocar frases, repartiendo la holgura de cada escena
escenas = []
t = 0.0
for k, e in enumerate(ESCENAS):
    ultima = k == len(ESCENAS) - 1
    dur = COMPASES[k] * BARRA if not ultima else TOTAL - t
    sl = dur - mins[k]
    n = len(e["frases"])
    pre0, _ = margenes(k, e)
    pre = pre0 + min(0.25, sl * 0.3)
    sl_rest = sl - min(0.25, sl * 0.3)
    gap_extra = min(0.35, sl_rest * 0.5 / max(1, n - 1)) if not ultima else 0.0
    frases = []
    cur = t + pre
    for i in range(n):
        key = f"{e['id']}_{i}"
        p = pal[key]
        words = [dict(w=w["w"], s=round(cur + w["s"], 3), e=round(cur + w["e"], 3)) for w in p["words"]]
        frases.append(dict(key=key, texto=e["frases"][i], t0=round(cur, 3), t1=round(cur + p["dur"], 3), words=words))
        cur += p["dur"]
        if i < n - 1:
            cur += (GAP_TITULO if (i == 0 and "num" in e) else GAP) + gap_extra
    esc = {kk: vv for kk, vv in e.items() if kk != "frases"}
    esc.update(t0=round(t, 4), t1=round(t + dur, 4), compases=None if ultima else COMPASES[k],
               frases=frases, fin_voz=round(cur, 3))
    assert cur <= t + dur + 1e-6, (e["id"], cur, t + dur)
    escenas.append(esc)
    t += dur

trans = []
for k in range(len(escenas) - 1):
    tipo, d = config.TRANSICIONES[k]
    b = escenas[k]["t1"]
    # normalmente 65% antes del cambio de escena; si eso pisaría la voz, se corre hacia después
    t0 = max(b - 0.65 * d, escenas[k]["fin_voz"] - 0.15)
    trans.append(dict(t=b, t0=round(t0, 4), t1=round(t0 + d, 4), tipo=tipo,
                      de=escenas[k]["id"], a=escenas[k + 1]["id"]))
    # la transición no debe pisar voz (cada clip trae 0.12 s de cola silenciosa)
    assert trans[-1]["t0"] >= escenas[k]["fin_voz"] - 0.15, (tipo, trans[-1]["t0"], escenas[k]["fin_voz"])
    assert trans[-1]["t1"] <= escenas[k + 1]["frases"][0]["t0"] + 0.35, (tipo,)

for e in escenas:
    e["beats"] = int(round((e["t1"] - e["t0"]) / BEAT)) if e["compases"] else None
tl = dict(bpm=BPM, beat=BEAT, unidad=UNIDAD, total=TOTAL, titulo=config.TITULO, estilo=config.ESTILO_VISUAL,
          escenas=escenas, transiciones=trans)
json.dump(tl, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for e in escenas:
    print(f"{e['id']:12s} {e['t0']:7.2f} -> {e['t1']:7.2f}  ({e['t1'] - e['t0']:5.2f}s)  voz: "
          + "  ".join(f"{f['t0']:.2f}-{f['t1']:.2f}" for f in e["frases"]))
