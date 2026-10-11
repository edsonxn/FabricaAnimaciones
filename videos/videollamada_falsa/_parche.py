# -*- coding: utf-8 -*-
"""Parches de texto sobre las escenas (sustituciones exactas; avisa de la que no encuentre). Editar CAMBIOS y ejecutar.
(No editar las escenas con PowerShell Set-Content: mete BOM.)
Tras un render: `--conservar` da por vigentes los segmentos guardados (docs/panel.md) para poder usar `video --rehacer t0-t1`."""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
NUCLEO = os.path.abspath(os.path.join(AQUI, "..", "..", "nucleo"))
CAMBIOS = {
    "esc_cierre.py": [          # el interrogatorio se veía casi negro en el MASTER
        ('        s = 1.75\n        self.sosp.dibujar(h, dict(x=1300 + dx, y=430 + 474 * s + dy,',
         '        s = 2.05\n        self.sosp.dibujar(h, dict(x=1300 + dx, y=400 + 474 * s + dy,'),
        ('        h.ambiente[:] = 0.24\n        N.motas(h, t, n=110, k=0.7)\n        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False))\n\n    # ------------------------------------------------------------------ ahora la cara',
         '        h.ambiente[:] = 0.40\n        h.luz_radial(330, 480, 700, (1.0, 1.0, 1.0), k=1.1)                 # el detective, a contraluz de la lámpara\n'
         '        N.motas(h, t, n=110, k=0.7)\n        return h.acabado(t, niebla=dict(dens=0.2, vel=10, y0=-300, y1=900, sube=False))\n\n    # ------------------------------------------------------------------ ahora la cara'),
    ],
    "esc_sinrostro.py": [       # la celda vacía pasaba 3 s a oscuras
        ('        h.ambiente[:] = 0.46\n        h.luz_cono(640, -600, math.pi / 2, 0.55, 2200, (1.4, 1.4, 1.4), k=1.2, suave=0.6)',
         '        h.ambiente[:] = 0.62\n        h.luz_cono(640, -600, math.pi / 2, 0.55, 2200, (1.4, 1.4, 1.4), k=1.5, suave=0.6)\n'
         '        h.luz_persiana(np.array([[150, 120], [1100, 60], [1250, 1000], [60, 1080]]), k=0.9, tipo="persiana", n=7, abierto=0.6)'),
    ],
}
if "--conservar" in sys.argv:
    sys.path.insert(0, NUCLEO)
    import cache_escenas
    print("escenas dadas por vigentes:", cache_escenas.conservar_escenas(AQUI, NUCLEO))
    raise SystemExit
for nombre, pares in CAMBIOS.items():
    p = os.path.join(AQUI, nombre)
    s = open(p, encoding="utf-8").read()
    for a, b in pares:
        if a not in s:
            print(f"NO ENCONTRADO en {nombre}: {a[:70]}")
            continue
        s = s.replace(a, b)
    open(p, "w", encoding="utf-8", newline="\n").write(s)
    print("ok", nombre)
