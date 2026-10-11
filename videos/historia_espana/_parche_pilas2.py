# -*- coding: utf-8 -*-
"""Parche 2 (4-oct-2026): las rutas con desvío en grados se cancelaban con la formación en píxeles. Todas las figuras de un grupo
siguen la MISMA ruta y se separan solo con formacion(); barcos con más separación; guerrilleros junto al centro de la cámara."""
D = r"C:\FabricaAnimaciones\videos\historia_espana"


def leer(n):
    return open(f"{D}\\{n}", encoding="utf-8").read()


def guardar(n, s):
    open(f"{D}\\{n}", "w", encoding="utf-8").write(s)


def sub(s, viejo, nuevo):
    assert s.count(viejo) == 1, (viejo[:70], s.count(viejo))
    return s.replace(viejo, nuevo)


c = leer("coreo_1.py")
c = sub(c, "[(3.1 + 0.6 * k, 42.1 - 0.3 * k), (0.2 - 0.6 * k, 40.8 - 0.4 * k), (-2.2 - 0.5 * k, 39.6 - 0.3 * k)]", "[(3.1, 42.1), (0.2, 40.8), (-2.2, 39.6)]")
guardar("coreo_1.py", c)

c = leer("coreo_2.py")
c = sub(c, "[(x + 0.35 * k, y + 0.3 * k) for x, y in Pv]", "Pv")
c = sub(c, "[(x - 0.12 + 0.12 * k, y + 0.02 * k) for x, y in Pt]", "Pt")
c = sub(c, 'snd=("ola", 0.35), off=formacion(k, 3, 120))', 'snd=("ola", 0.35), off=formacion(k, 3, 230))')
guardar("coreo_2.py", c)

c = leer("coreo_3.py")
c = sub(c, "[(x - 0.45 * k, y + 0.25 * k) for x, y in Pj]", "Pj")
c = sub(c, "off=formacion(k, 3, 90))", "off=formacion(k, 3, 110))")
c = sub(c, "[(x + 0.6 * k, y - 0.5 * k) for x, y in Pc]", "Pc")
c = sub(c, "[(x - 0.8 - 0.5 * k, y + 0.5 - 0.6 * k) for x, y in Pco]", "[(x - 0.8, y + 0.5) for x, y in Pco]")
c = sub(c, "off=formacion(k, 3, 95))", "off=formacion(k, 3, 110))")
c = sub(c, "[(x - 0.6 * k, y - 0.35 * k) for x, y in Par]", "Par")
c = sub(c, "off=formacion(k, 3, 170))", "off=formacion(k, 3, 230))")
c = sub(c, '"12 DE OCTUBRE DE 1492", y=140, px=72)', '"12 DE OCTUBRE DE 1492", y=155, px=72)')
guardar("coreo_3.py", c)

c = leer("coreo_4.py")
c = sub(c, "[(x - 0.7 - 0.5 * k, y - 0.4 - 0.3 * k) for x, y in Pn[1:]]", "[(x - 0.7, y - 0.4) for x, y in Pn[1:]]")
c = sub(c, "off=formacion(k, 3, 125))", "off=formacion(k, 3, 140))")
c = sub(c, "[(-3.7 + 0.3 * k, 40.4 - 0.2 * k), (-1.8, 41.4), (0.6 + 0.2 * k, 41.9)]", "[(-3.7, 40.4), (-1.8, 41.4), (0.6, 41.9)]")
c = sub(c, "ease=lambda u: u, off=formacion(k, 3, 90))", "ease=lambda u: u, off=formacion(k, 3, 110))")
c = sub(c, '''    for k, geo in enumerate(((-5.0, 40.9), (-1.8, 40.6), (-3.4, 38.4), (-6.0, 38.9))):
        ga(R, lambda t, k=k: E4.guerrillero(int(t * 4 + k) % 2, "enojo"), geo, t_palabra + 0.12 * k, t_cadiz - 1.0, s=0.6, sem=210 + k, z=2)''',
        '''    # junto al centro de la cámara y con separación fija en pantalla: el zoom hacia Cádiz no los saca del cuadro ni los pone bajo el título
    for k, dxy in enumerate(((-420, -40), (-140, 70), (140, -40), (420, 70))):
        ga(R, lambda t, k=k: E4.guerrillero(int(t * 4 + k) % 2, "enojo"), (-4.2, 39.0), t_palabra + 0.12 * k, t_cadiz - 0.5, s=0.6, off=dxy, sem=210 + k, z=2)''')
guardar("coreo_4.py", c)
print("parche 2 aplicado")
