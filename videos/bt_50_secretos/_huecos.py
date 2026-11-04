# -*- coding: utf-8 -*-
"""Huecos > 4 s sin pegatina ni MG (regla del 3-nov-2026, cod_mw4_secretos). Los avisos (secreto/contador) no cuentan.
    python _huecos.py"""
import os, sys
AQUI = os.path.dirname(os.path.abspath(__file__)); os.chdir(AQUI)
sys.path[:0] = [AQUI, os.path.join(AQUI, "..", "..", "nucleo")]
import secuencia_fx as SF  # noqa: E402
capa = SF.cargar()
iv = [(d["de"], d["a"]) for d in capa.fx if d["tipo"] in ("mg", "pantalla") and not d.get("nombre", "").startswith("aviso")]
iv += [(r["de"], r["a"]) for r in capa.rot if "de" in r]
iv.sort()
fin = max(a for _, a in iv)
t, huecos = 0.0, []
for de, a in iv:
    if de - t > 4:
        huecos.append((t, de))
    t = max(t, a)
tot = sum(b - a for a, b in huecos)
for a, b in huecos:
    print(f"{int(a // 60)}:{a % 60:04.1f}  {b - a:4.1f} s")
print(f"{len(huecos)} huecos > 4 s, {tot:.0f} s en total")
