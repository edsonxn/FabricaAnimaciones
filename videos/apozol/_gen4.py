# -*- coding: utf-8 -*-
"""Arma mundos_4.py: la plantilla + las funciones de caballo 2D y siluetas copiadas de los recursos de Juchipila (kit evolucionado en ese video)."""
h = open("../juchipila/mundos_h.py", encoding="utf-8").read()
a = h.index("CAB = (120, 76, 52)")
b = h.index("def sobre(")
copiado = h[a:b]
ma = open("../juchipila/mundos_a.py", encoding="utf-8").read()
copiado += "\n\n" + ma[ma.index("def silueta_guerrero("):]
pl = open("_mundos_4_plantilla.py", encoding="utf-8").read()
open("mundos_4.py", "w", encoding="utf-8").write(pl.replace("#@@COPIADO@@", copiado))
print("mundos_4.py generado")
