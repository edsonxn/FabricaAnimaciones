# -*- coding: utf-8 -*-
"""Mete una PAUSA SIN VOZ en el timeline ya hecho (para que suene algo que la voz nombra: el usuario, 13-nov-2026, «pon la
música de Dragonborn épica y déjala sonar unos segundos» tras «…era Sangre de Dragón»). Corre +D s todo lo que empieza en/tras
T (palabras, frases, escenas, transiciones, total) en timeline.json, timeline_beats.json y beats.json, y añade un beat de video
nuevo [T, T+D] con su id (su clip con `bajar <n> --q …`). La escena que contiene T crece D s (= compases enteros). Idempotente:
apunta la pausa en timeline.json["pausas"] y no la repite.
    python _pausa.py 1912.091 6.0 scene-245 "(Dragonborn: la música suena sola)"
OJO: un `tiempo` o `beats` nuevo la borra → volver a correr este script (y `reajustar` no la conoce).
"""
import json
import sys

T, D, BID, TXT = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3], sys.argv[4]
tl = json.load(open("timeline.json", encoding="utf-8"))
if any(abs(p["t"] - T) < .01 for p in tl.get("pausas", [])):
    raise SystemExit(f"la pausa en {T} ya está")
barra = tl["beat"] * tl["unidad"]
assert abs(D / barra - round(D / barra)) < 1e-6, f"D debe ser compases enteros ({barra} s)"
sh = lambda t: round(t + D, 4) if t >= T - 1e-6 else t
for e in tl["escenas"]:
    contiene = e["t0"] < T < e["t1"]
    for f in e["frases"]:
        f["t0"], f["t1"] = sh(f["t0"]), sh(f["t1"])
        for w in f["words"]:
            w["s"], w["e"] = sh(w["s"]), sh(w["e"])
    e["t0"], e["t1"], e["fin_voz"] = sh(e["t0"]), sh(e["t1"]), sh(e["fin_voz"])
    if contiene:
        if e.get("compases"):
            e["compases"] += int(round(D / barra))
        if e.get("beats"):
            e["beats"] += int(round(D / tl["beat"]))
        print("escena que crece:", e["id"])
for tr in tl["transiciones"]:
    tr["t"], tr["t0"], tr["t1"] = sh(tr["t"]), sh(tr["t0"]), sh(tr["t1"])
tl["total"] = round(tl["total"] + D, 4)
tl.setdefault("pausas", []).append(dict(t=T, d=D, beat=BID, nota=TXT))
bs = json.load(open("beats.json", encoding="utf-8"))
assert not any(b["id"] == BID for b in bs), BID
assert any(abs(b["t0"] - T) < .01 for b in bs), "T debe caer en un corte de beat"
for b in bs:
    # el beat que TERMINA en T no se estira (si no, se encima al beat nuevo y el render sigue con su clip: 13-nov-2026)
    b["t0"], b["t1"] = sh(b["t0"]), (sh(b["t1"]) if b["t1"] > T + 1e-3 else b["t1"])
i = next(k for k, b in enumerate(bs) if b["t0"] >= T + D - 1e-6)
bs.insert(i, dict(id=BID, t0=round(T, 3), t1=round(T + D, 3), tipo="video", texto=TXT, clip_s=int(D) + 2))
json.dump(tl, open("timeline.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(tl, open("timeline_beats.json", "w", encoding="utf-8"), ensure_ascii=False)
json.dump(bs, open("beats.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"pausa de {D} s en {T} · total {tl['total']:.2f} s · beat nuevo {BID} en la posición {i}")
