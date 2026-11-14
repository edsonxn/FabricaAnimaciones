# -*- coding: utf-8 -*-
"""V3 (13-nov-2026): cruza cada escena de Flow v3 (pegatinas/flow3_NNN.png) con su beat y con los FX ya puestos
(pantallas y MG a cuadro entero) para ver con qué choca.   python _flow3_plan.py"""
import glob
import os
import sys

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())
import secuencia_fx as SF  # noqa: E402

capa = SF.cargar()
ids = sorted(os.path.basename(p)[6:9] for p in glob.glob("pegatinas/flow3_*.png"))
pant = [(d["de"], d["a"], d.get("nombre", "")) for d in capa.fx if d["tipo"] == "pantalla"]
mgs = [(d["de"], d["a"], d.get("nombre", "")) for d in capa.fx if d["tipo"] == "mg"]
for n in ids:
    b = capa.por_id[f"scene-{n}"]
    t0, t1 = b["t0"], b["t1"]
    cho = [f"P:{x[2][15:40]}({x[0]:.1f}-{x[1]:.1f})" for x in pant if x[0] < t1 - .3 and x[1] > t0 + .3]
    chm = [f"M:{x[2][3:30]}({x[0]:.1f}-{x[1]:.1f})" for x in mgs if x[0] < t1 - .3 and x[1] > t0 + .3]
    print(f"{n} {t0:7.1f}-{t1:7.1f} ({t1 - t0:4.1f}s) {b.get('tipo', '')[:5]} " + " ".join(cho + chm))


# ---- genera el bloque FLOW3 para efectos.py (anclas relativas a cada beat: no dependen de números sueltos)
GRANDES = ("red cap", "rbol", "sus", "cronolog", "maormer", "Kintyra", "bando", "maldici", "dos versiones", "cordura", "teor",
           "rusel", "trono", "xima historia", "quince", "Ichidag")
MOV = [((1.0, 1.10), (0, 0, 0, 0)), ((1.10, 1.0), (0, 0, 0, 0)), ((1.04, 1.12), (-.6, 0, .6, 0)), ((1.06, 1.14), (.5, .3, -.5, -.3)),
       ((1.12, 1.03), (0, -.5, 0, .5)), ((1.03, 1.12), (.6, 0, -.6, 0))]
if "--emitir" in sys.argv:
    S = set(ids)
    out = ["# v3 (13-nov): ESCENAS DE FLOW v3 (Oblivion 2006 / Skyrim vanilla, flow/escenas_v3.md) a cuadro entero en la frase",
           "# que cuentan; quitan el gameplay que no encajaba (glitch, tops, HUD). Debajo de pegatinas, fichas y redes.",
           "# Generado por _flow3_plan.py --emitir (recortadas contra las pantallas de v2 que ya estaban).", "FLOW3 = ["]
    for k, n in enumerate(ids):
        b = capa.por_id[f"scene-{n}"]
        t0, t1 = b["t0"], b["t1"]
        de, a = 0.0, 0.0
        nxt = f"{int(n) + 1:03d}"
        if nxt in S:
            a = .5                                           # se encadena con la siguiente (fundido encima)
        for x in pant:
            if x[0] < t1 - .3 and x[1] > t0 + .3:
                if x[0] > t0 + .3:                           # la de v2 entra a media frase: esta termina ahí
                    a = min(a, x[0] + .5 - t1)
                else:                                        # la de v2 sale a media frase: esta empieza ahí
                    de = max(de, x[1] - .5 - t0)
        big = any(g in x[2] for x in mgs if x[0] < t1 - .3 and x[1] > t0 + .3 for g in GRANDES)
        z, p = MOV[k % len(MOV)]
        osc = .22 if big else .08
        out.append(f'    fl3("{n}", ("scene-{n}", {de:.2f}), ("scene-{n}:fin", {a:.2f}), zoom={z}, pan={p}, oscuro={osc}),')
    out.append("]")
    open("_flow3_bloque.py", "w", encoding="utf-8").write("\n".join(out) + "\n")
    print("escrito _flow3_bloque.py", len(ids))
