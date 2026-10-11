# -*- coding: utf-8 -*-
import re


def parchea(nombre, reglas):
    s = open(nombre, encoding="utf-8").read()
    for a, b in reglas:
        if a not in s:
            print("NO ENCONTRADO en", nombre, ":", a[:80].replace("\n", "\\n"))
            continue
        s = s.replace(a, b, 1)
    open(nombre, "w", encoding="utf-8").write(s)


# ------------------------------------------------------------------ s_b
sb = open("s_b.py", encoding="utf-8").read()
# (a) horno: cámara
sb = sb.replace("    incl = K(t, [(T_BARRAS - 0.4, 0.0), (T_BARRAS + 0.4, 0.55), (T_BARRAS + 2.0, 0.55), (T_BARRAS + 2.6, 0.0)], e_inout)\n",
                "    incl = K(t, [(T_BARRAS - 0.4, 0.0), (T_BARRAS + 0.4, 0.55), (T_BARRAS + 2.0, 0.55), (T_BARRAS + 2.6, 0.0)], e_inout)\n    _cm = cam(lz, 940, 640, 1.16)\n    _cm.__enter__()\n", 1)
sb = sb.replace("    # arte: brilla y se conserva (frase 0)\n", "    _cm.__exit__(None, None, None)\n    # arte: brilla y se conserva (frase 0)\n", 1)
# ... pero el chorro y los moldes van después: se dibujan fuera de la cámara; los meto dentro moviendo el cierre al final de los moldes
sb = sb.replace("    _cm.__exit__(None, None, None)\n    # arte: brilla y se conserva (frase 0)\n", "    # arte: brilla y se conserva (frase 0)\n", 1)
sb = sb.replace("    etq(lz, t, T_BARRAS - 0.6, T_BARRAS + 1.6, \"moldes de barras\", 1590, 940 - 120, px=34)\n",
                "    _cm.__exit__(None, None, None)\n    etq(lz, t, T_BARRAS - 0.6, T_BARRAS + 1.6, \"moldes de barras\", 1560, 740, px=34)\n", 1)
# (b) f_nada: los objetos se encogen en vez de taparse con un rectángulo
a = sb.index("@shot(T_NADA")
b = sb.index("snd(T_NADA + 0.6")
nuevo = '''@shot(T_NADA, bg=lambda t: bg_grad((30, 20, 44), (16, 10, 30)), ent=("tinta", 0.7))
def f_nada(lz, t):
    tt = INI(E6, 2)
    for i, (kind, x, y) in enumerate((("disco", 330, 430), ("plata", 960, 400), ("mascara", 1560, 460))):
        u = smooth(prog(t, tt + 0.8 + i * 0.3, tt + 1.6 + i * 0.3))
        k = max(1.0 - u, 0.0)
        with lz.grupo(x, y, 1.0):
            if k > 0.02:
                if kind == "disco":
                    F.disco(lz, 0, 0, 150 * k, t, "oro")
                elif kind == "plata":
                    F.disco(lz, 0, 0, 150 * k, t, "plata")
                else:
                    _mascara(lz, 0, 60 * k, 4.0 * k)
            ring = circulo(0, 0, 160, 60)
            P.discontinua(lz, np.vstack([ring, ring[:1]]), (255, 214, 96), ancho=6.0, largo=22, hueco=16, fase=-t * 20, frac=u)
            if u > 0.5:
                lz.trazo(np.array([[-110, -110], [110, 110]]), (240, 70, 70), 16.0, temblor=0.0, capa=2)
                lz.trazo(np.array([[110, -110], [-110, 110]]), (240, 70, 70), 16.0, temblor=0.0, capa=2)
    gran(lz, t, tt + 1.4, T1(E6) - 0.2, "Ninguna se conserva", 960, 190, px=90, col=(255, 200, 100))
    etq(lz, t, tt + 0.2, tt + 2.0, "Las piezas que vio Durero", 960, 700, px=38)


'''
sb = sb[:a] + nuevo + sb[b:]
# (c) plaza: bailarines y atacantes más grandes
sb = sb.replace("_bailarin(lz, x, y + 4 * math.sin(t * 6 + k), 1.0, t, k, viva)", "_bailarin(lz, x, y + 4 * math.sin(t * 6 + k), 1.4, t, k, viva)")
sb = sb.replace("lz.relleno(circulo(sx, sy, 13, 14), (172, 180, 200))\n                lz.relleno(circulo(sx, sy, 7, 10), (206, 70, 62))",
                "lz.relleno(circulo(sx, sy, 21, 14), (172, 180, 200))\n                lz.relleno(circulo(sx, sy, 11, 10), (206, 70, 62))")
sb = sb.replace("(230, 236, 250), 4.0, temblor=0.0, capa=2)\n    if u > 0.02:", "(230, 236, 250), 6.0, temblor=0.0, capa=2)\n    if u > 0.02:")
sb = sb.replace("sx + math.cos(ang + 3.14) * -26, sy + math.sin(ang + 3.14) * -26", "sx + math.cos(ang + 3.14) * -48, sy + math.sin(ang + 3.14) * -48")
# (d) Moctezuma cae en las dos versiones; piedras más grandes
sb = sb.replace("        F.tlatoani(lz, xm, 500 + 0 * caida, 1.5, t, lado=-1, brazos=0.5 * (1 - caida), seed=3)",
                "        with lz.grupo(xm, 500, 1.0, 1.35 * caida):\n            F.tlatoani(lz, 0, 0, 1.5, t, lado=-1, brazos=0.5 * (1 - caida), seed=3)")
sb = sb.replace("        F.tlatoani(lz, xm, 500, 1.5, t, lado=-1, brazos=0.3 * (1 - caida), seed=3)",
                "        with lz.grupo(xm, 500, 1.0, -1.35 * caida):\n            F.tlatoani(lz, 0, 0, 1.5, t, lado=-1, brazos=0.3 * (1 - caida), seed=3)")
sb = sb.replace("lz.relleno(circulo(px, py, 8, 8), (150, 150, 160))", "lz.relleno(circulo(px, py, 13, 10), (150, 150, 160))")
open("s_b.py", "w", encoding="utf-8").write(sb)

# ------------------------------------------------------------------ s_c
sc = open("s_c.py", encoding="utf-8").read()
# patio: cámara más cerca y disposición más amplia
sc = sc.replace("    cxx = K(t, [(T0(E9), 900.0), (w_(E9, 1, 3), 940.0), (w_(E9, 1, 8), 1280.0), (T1(E9), 1500.0)], e_inout)\n    with cam(lz, cxx, 540, 1.0):",
                "    ZP = 1.5\n    cxx = K(t, [(T0(E9), 760.0), (w_(E9, 1, 3), 900.0), (w_(E9, 1, 8), 1420.0), (T1(E9), 1700.0)], e_inout)\n    with cam(lz, cxx, 690, ZP):")
sc = sc.replace("F.brasero(lz, x, GY9, 1.5, t)", "F.brasero(lz, x, GY9, 1.5, t)")
sc = sc.replace("        for x in (140, 1090, 2000):", "        for x in (100, 1120, 2100):")
sc = sc.replace("            x0 = 700 + i * 60\n            xt = 1420 + i * 46", "            x0 = 430 + i * 70\n            xt = 1500 + i * 46")
sc = sc.replace("_monton(lz, 1560, GY9, n_pila - taken, t)", "_monton(lz, 1640, GY9, n_pila - taken, t)")
sc = sc.replace("for (tt, x, txt) in ((t_rey, 900, \"Quinto del rey\"), (t_suyo, 1040, \"Quinto de Cortés\")):", "for (tt, x, txt) in ((t_rey, 1060, \"Quinto del rey\"), (t_suyo, 1200, \"Quinto de Cortés\")):")
sc = sc.replace("ti = t_carga + 0.35 * k + (0.0 if x == 900 else 1.2)", "ti = t_carga + 0.35 * k + (0.0 if x == 1060 else 1.2)")
sc = sc.replace("for j, hx in enumerate((230, 470)):", "for j, hx in enumerate((170, 400)):")
sc = sc.replace("for (x, jj) in ((900, 0), (1040, 1)):", "for (x, jj) in ((1060, 0), (1200, 1)):")
sc = sc.replace("px = lerp(x, 230 + 240 * jj, e_inout(u))", "px = lerp(x, 170 + 230 * jj, e_inout(u))")
sc = sc.replace("F.soldado(lz, 780, GY9, 2.0, t, lado=1, arma=\"espada\", seed=1, tunica=(150, 40, 60),", "F.soldado(lz, 930, GY9, 2.0, t, lado=1, arma=\"espada\", seed=1, tunica=(150, 40, 60),")
sc = sc.replace("            x0 = 640 - 55 * i + (0 if i < 3 else 0)\n            x0 = 520 + i * 40\n            xt = 1420 + i * 46", "            x0 = 430 + i * 70\n            xt = 1500 + i * 46")
sc = sc.replace("    for (tt, txt, sx) in ((t_rey, \"Quinto del rey\", 900), (t_suyo, \"Quinto de Cortés\", 1040)):\n        a = vent(t, tt, t_carga + 1.0)\n        if a > 0.01:\n            P.pastilla(lz, W / 2 + (sx - cxx), 640, txt, px=34, alfa=a)",
                "    for (tt, txt, sx) in ((t_rey, \"Quinto del rey\", 1060), (t_suyo, \"Quinto de Cortés\", 1200)):\n        a = vent(t, tt, t_carga + 1.0)\n        if a > 0.01:\n            P.pastilla(lz, W / 2 + (sx - cxx) * ZP, H / 2 + (GY9 - 190 - 690) * ZP, txt, px=34, alfa=a)")
sc = sc.replace("        P.pastilla(lz, W / 2 + (1560 - cxx), 500, \"«el oro que quisieran»\", px=38, alfa=a)", "        P.pastilla(lz, W / 2 + (1640 - cxx) * ZP, H / 2 + (GY9 - 330 - 690) * ZP, \"«el oro que quisieran»\", px=38, alfa=a)")
# calzada de la noche: más zoom
sc = sc.replace("    zoom = K(t, [(T0(E10), 1.0), (T_J0 - 0.4, 1.0), (T_J0 + 1.2, 1.4), (T_HUND - 0.3, 1.45)], e_inout)",
                "    zoom = K(t, [(T0(E10), 1.3), (T_J0 - 0.4, 1.3), (T_J0 + 1.2, 1.65), (T_HUND - 0.3, 1.7)], e_inout)")
sc = sc.replace("    with lz.grupo(W / 2, 540, zoom):\n        with lz.grupo(-W / 2, -540, 1.0):\n            _calzada_noche", "    with lz.grupo(W / 2, 560, zoom):\n        with lz.grupo(-W / 2, -690, 1.0):\n            _calzada_noche")
# gráfica de bajas: escala menor y números encima
sc = sc.replace("    k = 0.36\n    x0 = 470", "    k = 0.28\n    x0 = 470")
sc = sc.replace("cifra(lz, t, ta, txt, x0 + largo + 130 + 20, y, px=64, col=col if False else (255, 255, 255))", "cifra(lz, t, ta, txt, x0 + largo + 190, y, px=64, col=(255, 255, 255))")
sc = sc.replace("cifra(lz, t, ta, \"1 000 a 4 000\", x0 + 1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6) + 190, y, px=60, col=BLANCO)", "cifra(lz, t, ta, \"1 000 a 4 000\", x0 + 1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6) + 230, y, px=60, col=BLANCO)")
open("s_c.py", "w", encoding="utf-8").write(sc)

# ------------------------------------------------------------------ s_d
sd = open("s_d.py", encoding="utf-8").read()
# sospechas: personajes más grandes
sd = sd.replace("F.soldado(lz, 660, gy, 2.2, t, lado=1, arma=None, seed=1, tunica=(150, 40, 60), brazos=(-0.3, 1.2))", "F.soldado(lz, 640, gy, 3.0, t, lado=1, arma=None, seed=1, tunica=(150, 40, 60), brazos=(-0.3, 1.2))")
sd = sd.replace("        F.soldado(lz, 1080 + 130 * i, gy + 6 * (i % 2), 1.8, t, lado=-1 if (vuelta > 0.5 or True) else 1, arma=None, seed=i + 40,", "        F.soldado(lz, 1000 + 150 * i, gy + 6 * (i % 2), 2.5, t, lado=-1, arma=None, seed=i + 40,")
sd = sd.replace("burbuja(lz, 1300, 470, \"¿Y mi parte?\"", "burbuja(lz, 1300, 420, \"¿Y mi parte?\"")
sd = sd.replace("        burbuja(lz, 1080 + 130 * i, 520 - 40 * (i % 2), \"?\"", "        burbuja(lz, 1000 + 150 * i, 480 - 40 * (i % 2), \"?\"")
sd = sd.replace("    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (214, 180, 140))\n    for i in range(7):\n        x = 100 + i * 300", "    lz.relleno(rect_red(-20, gy, W + 40, 260, 0), (214, 180, 140))\n    for i in range(7):\n        x = 100 + i * 300")
sd = sd.replace("F.saco(lz, 590, gy - 8, 1.5, brillo=1.0)", "F.saco(lz, 500, gy - 8, 2.0, brillo=1.0)")
sd = sd.replace("F.bergantin(lz, 230, 700, 1.2, t, lado=1, seed=2)", "F.bergantin(lz, 230, 660, 1.5, t, lado=1, seed=2)")
sd = sd.replace("lz.relleno(blob(770, 640, 38 * bolsa + 8, 3, 0.1, 20, 4), F.ORO_S)", "lz.relleno(blob(790, 640, 38 * bolsa + 8, 3, 0.1, 20, 4), F.ORO_S)")
# corte de sección: la capa que oculta el templo repite el degradado del terreno; zoom mayor al inicio
sd = sd.replace("""        cubre = 1.0 - smooth(prog(t, T_DESC + 0.4, T_DESC + 3.2))
        if cubre > 0.01:
            lz.relleno(np.array([[900, SY + 20], [1800, SY + 20], [1800, SY + 740], [900, SY + 740]]), (126, 98, 108), alfa=cubre)
            lz.relleno(np.array([[900, SY + 20], [1800, SY + 20], [1800, SY + 330], [900, SY + 330]]), (176, 132, 96), alfa=cubre * 0.0)""",
"""        cubre = 1.0 - smooth(prog(t, T_DESC + 0.4, T_DESC + 3.2))
        if cubre > 0.01:
            with lz.recorte(np.array([[880, SY + 20], [1820, SY + 20], [1820, SY + 760], [880, SY + 760]])):
                _capas_terreno(lz, cubre)""")
sd = sd.replace("        degradado_v(lz, -400, 2600, SY, SY + 120, (120, 116, 132), (176, 132, 96), SY, SY + 120, paso=10.0)\n        degradado_v(lz, -400, 2600, SY + 120, SY + 340, (176, 132, 96), (140, 108, 100), SY + 120, SY + 340, paso=14.0)\n        degradado_v(lz, -400, 2600, SY + 340, SY + 1300, (120, 104, 118), (46, 40, 70), SY + 340, SY + 1200, paso=24.0)\n",
                "        _capas_terreno(lz, 1.0)\n")
sd = sd.replace("def _piedra_luna(lz, x, y, r, t, brillo=0.0):", '''def _capas_terreno(lz, alfa=1.0):
    """Capas del subsuelo: asfalto y cimientos, relleno colonial y lodo del antiguo lago (bandas con alfa)."""
    for (y0, y1, c0, c1, paso) in ((SY, SY + 120, (120, 116, 132), (176, 132, 96), 12.0), (SY + 120, SY + 340, (176, 132, 96), (140, 108, 100), 16.0),
                                   (SY + 340, SY + 1300, (120, 104, 118), (46, 40, 70), 30.0)):
        n = max(1, int((y1 - y0) / paso))
        for i in range(n):
            ya, yb = y0 + (y1 - y0) * i / n, y0 + (y1 - y0) * (i + 1) / n + 1.0
            u = (i + 0.5) / n
            lz.relleno(np.array([[-400, ya], [2600, ya], [2600, yb], [-400, yb]]), P.mezcla(c0, c1, u), alfa=alfa)


def _piedra_luna(lz, x, y, r, t, brillo=0.0):''')
sd = sd.replace("    zoom = K(t, [(T0(E15), 1.0), (T_ROCA, 1.2), (T_DESC + 0.5, 1.0)], e_inout)", "    zoom = K(t, [(T0(E15), 1.12), (T_ROCA, 1.3), (T_DESC + 0.5, 1.05)], e_inout)")
sd = sd.replace("    cy = K(t, [(T0(E15), 470.0), (INI(E15, 1) + 0.6, 470.0), (T_CAVA1, 700.0), (T_ROCA + 0.5, 820.0), (T_DESC, 900.0), (T1(E15), 900.0)], e_inout)", "    cy = K(t, [(T0(E15), 560.0), (INI(E15, 1) + 0.6, 560.0), (T_CAVA1, 720.0), (T_ROCA + 0.5, 820.0), (T_DESC, 900.0), (T1(E15), 900.0)], e_inout)")
# hallazgo: la cifra no debe pisar la etiqueta
sd = sd.replace("cifra(lz, t, w_(E16, 0, 21), \"1,93 kg\", 960, 240, px=120, col=ORO, t1=T1(E16) if False else w_(E16, 1, 0))", "cifra(lz, t, w_(E16, 0, 21), \"1,93 kg\", 960, 330, px=120, col=ORO, t1=w_(E16, 1, 0))")
open("s_d.py", "w", encoding="utf-8").write(sd)
print("ok")
