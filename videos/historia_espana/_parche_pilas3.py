# -*- coding: utf-8 -*-
"""Parche 3 (4-oct-2026): guerrilleros anclados a la pantalla (el zoom hacia Cádiz los subía bajo el título) y rótulo EXILIO fuera de la ruta."""
D = r"C:\FabricaAnimaciones\videos\historia_espana"
s = open(f"{D}\\coreo_4.py", encoding="utf-8").read()


def sub(s, viejo, nuevo):
    assert s.count(viejo) == 1, (viejo[:70], s.count(viejo))
    return s.replace(viejo, nuevo)


s = sub(s, '''    # junto al centro de la cámara y con separación fija en pantalla: el zoom hacia Cádiz no los saca del cuadro ni los pone bajo el título
    for k, dxy in enumerate(((-420, -40), (-140, 70), (140, -40), (420, 70))):
        ga(R, lambda t, k=k: E4.guerrillero(int(t * 4 + k) % 2, "enojo"), (-4.2, 39.0), t_palabra + 0.12 * k, t_cadiz - 0.5, s=0.6, off=dxy, sem=210 + k, z=2)''',
        '''    # fijos en pantalla, bajo el título: el zoom hacia Cádiz sacaba a los anclados al mapa por arriba, encima del rótulo
    for k, (gx, gy) in enumerate(((600, 690), (880, 770), (1160, 690), (1440, 770))):
        pa(R, lambda t, k=k: E4.guerrillero(int(t * 4 + k) % 2, "enojo"), gx, gy, 0.8, t_palabra + 0.12 * k, t_cadiz - 0.5, sem=210 + k, z=2)''')
s = sub(s, 'lugar(R, t_exil, t_sesenta - 0.2, "EXILIO", (-0.6, 41.6), off=(0, 70), px=50)',
        'R.texto(t_exil, t_sesenta - 0.2, "EXILIO", (560, 520), px=50, d=0.3)      # fuera de la ruta de los exiliados (subía hasta Cataluña)')
open(f"{D}\\coreo_4.py", "w", encoding="utf-8").write(s)
print("parche 3 aplicado")
