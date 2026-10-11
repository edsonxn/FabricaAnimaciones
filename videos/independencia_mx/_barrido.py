"""Renderiza un cuadro en tres momentos de CADA toma para cazar errores antes del render largo: python _barrido.py"""
import sys, time, traceback
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo
import escenas as S
import efectos as E
lz = Lienzo()
err = 0
for k, d in enumerate(S.SHOTS):
    a, b = d["t0"], d["t1"]
    for f in (0.15, 0.5, 0.9):
        t = a + (b - a) * f
        try:
            img = S.render_mundo(lz, t)
            E.acabado(img, int(t * 10))
        except Exception:
            err += 1
            print("ERROR toma", k, getattr(d["dib"], "__name__", "?"), "t=%.2f" % t)
            traceback.print_exc(limit=3)
            break
print("barrido listo, errores:", err)
