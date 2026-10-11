# -*- coding: utf-8 -*-
"""Parche (4-oct-2026, revisión del MASTER): grupos que marchan juntos se encimaban, «→» sin glifo, título tapado por un barco,
guerrilleros fuera de cuadro. Cada reemplazo se verifica."""
import re

D = r"C:\FabricaAnimaciones\videos\historia_espana"


def leer(n):
    return open(f"{D}\\{n}", encoding="utf-8").read()


def guardar(n, s):
    open(f"{D}\\{n}", "w", encoding="utf-8").write(s)


def sub(s, viejo, nuevo, n=1):
    assert s.count(viejo) == n, (viejo[:60], s.count(viejo))
    return s.replace(viejo, nuevo)


# --- coreo_util: formación a distancia fija en pantalla
u = leer("coreo_util.py")
u = sub(u, "def mece(a=6.0, w=2.2, ph=0.0):", '''def formacion(k, n, ancho):
    """Desplazamiento en px (dx, dy) de la figura k de un grupo de n que marcha junta: en hilera escalonada y a distancia FIJA en pantalla.
    Las rutas separadas solo décimas de grado se encimaban al acercarse la cámara (legionarios, carabelas, soldados: «montón» de trazos)."""
    return ((k - (n - 1) / 2) * ancho, (-1) ** k * 0.22 * ancho)


def mece(a=6.0, w=2.2, ph=0.0):''')
guardar("coreo_util.py", u)

# --- coreo_1: legionarios + flecha dibujada en vez de «→»
c = leer("coreo_1.py")
c = sub(c, "from coreo_util import CI, COL, andar, ciudad, ga, lugar, mece, pa, titulo", "from coreo_util import CI, COL, andar, ciudad, formacion, ga, lugar, mece, pa, titulo")
c = sub(c, "import obj_a as A\n", "import obj_a as A\nimport obj_b as Bb\n")
c = sub(c, "t_guerra + 0.2 * k, 3.0, t1=t_conq + 0.2, s=0.58, sem=32 + k, z=2, flip=True)",
        "t_guerra + 0.2 * k, 3.0, t1=t_conq + 0.2, s=0.58, sem=32 + k, z=2, flip=True, off=formacion(k, 3, 130))")
c = sub(c, '    R.texto(t_abue - 0.1, t_le - 0.3, "→", (960, 990), px=86, d=0.2)\n',
        '    pa(R, Bb.flecha(), 970, 985, 0.62, t_abue - 0.1, t_le - 0.3, sem=52, snd=("pop", 0.3))      # la fuente no tiene «→»\n')
guardar("coreo_1.py", c)

# --- coreo_2: visigodos y galeras
c = leer("coreo_2.py")
m = re.search(r"from coreo_util import ([^\n]+)", c)
assert m and "formacion" not in m.group(1)
c = c.replace(m.group(0), "from coreo_util import " + ", ".join(sorted(set(m.group(1).split(", ")) | {"formacion"}, key=str.lower)), 1)
c = sub(c, "t_lleg + 0.15 * k, 2.6, t1=t_pero,\n              s=0.6, sem=60 + k, z=2)", "t_lleg + 0.15 * k, 2.6, t1=t_pero,\n              s=0.6, sem=60 + k, z=2, off=formacion(k, 3, 120))")
c = sub(c, "t1=t_gen, s=0.36, sem=70 + k, zs=0.4, z=2, fps=4, flip=False, snd=(\"ola\", 0.35))", "t1=t_gen, s=0.36, sem=70 + k, zs=0.4, z=2, fps=4, flip=False, snd=(\"ola\", 0.35), off=formacion(k, 3, 120))")
guardar("coreo_2.py", c)

# --- coreo_3: exiliados, carabelas, tlaxcaltecas, armada, 12 de octubre
c = leer("coreo_3.py")
m = re.search(r"from coreo_util import ([^\n]+)", c)
assert m and "formacion" not in m.group(1)
c = c.replace(m.group(0), "from coreo_util import " + ", ".join(sorted(set(m.group(1).split(", ")) | {"formacion"}, key=str.lower)), 1)
c = sub(c, "sem=125 + k, z=2, fps=4, snd=None, ease=lambda u: u)", "sem=125 + k, z=2, fps=4, snd=None, ease=lambda u: u, off=formacion(k, 3, 90))")
c = sub(c, 'fps=3, snd=("ola", 0.35) if k == 0 else None)\n    R.texto(t_india', 'fps=3, snd=("ola", 0.35) if k == 0 else None, off=formacion(k, 3, 190))\n    R.texto(t_india')
c = sub(c, "t1=t_piz - 0.5, s=0.45, sem=141 + k, z=2, fps=6)", "t1=t_piz - 0.5, s=0.45, sem=141 + k, z=2, fps=6, off=formacion(k, 3, 95))")
c = sub(c, 'fps=3, snd=("ola", 0.3) if k == 0 else None, ease=lambda u: u)', 'fps=3, snd=("ola", 0.3) if k == 0 else None, ease=lambda u: u, off=formacion(k, 3, 170))')
c = sub(c, '"12 DE OCTUBRE DE 1492", px=72)', '"12 DE OCTUBRE DE 1492", y=140, px=72)')
guardar("coreo_3.py", c)

# --- coreo_4: soldados franceses, exiliados de 1939, guerrilleros
c = leer("coreo_4.py")
m = re.search(r"from coreo_util import ([^\n]+)", c)
assert m and "formacion" not in m.group(1)
c = c.replace(m.group(0), "from coreo_util import " + ", ".join(sorted(set(m.group(1).split(", ")) | {"formacion"}, key=str.lower)), 1)
c = sub(c, 't1=t_pueblo, s=0.62, sem=201 + k, z=2, fps=6, snd=("pasos", 0.3) if k == 0 else None)', 't1=t_pueblo, s=0.62, sem=201 + k, z=2, fps=6, snd=("pasos", 0.3) if k == 0 else None, off=formacion(k, 3, 125))')
c = sub(c, "t1=t_sesenta, s=0.48, sem=264 + k, z=2, fps=4, snd=None, ease=lambda u: u)", "t1=t_sesenta, s=0.48, sem=264 + k, z=2, fps=4, snd=None, ease=lambda u: u, off=formacion(k, 3, 90))")
# los guerrilleros salen antes de que la cámara (zoom 2,4 -> 4,5 hacia Cádiz) los saque por arriba y choquen con el título
c = sub(c, "geo, t_palabra + 0.12 * k, t_cadiz - 0.2, s=0.6, sem=210 + k, z=2)", "geo, t_palabra + 0.12 * k, t_cadiz - 1.0, s=0.6, sem=210 + k, z=2)")
c = sub(c, 'titulo(R, t_guerr - 0.15, t_cadiz - 0.2, "«GUERRILLA»"', 'titulo(R, t_guerr - 0.15, t_cadiz - 0.6, "«GUERRILLA»"')
guardar("coreo_4.py", c)
print("parche aplicado")
