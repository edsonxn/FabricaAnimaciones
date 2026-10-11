# -*- coding: utf-8 -*-
p = "s_a.py"
s = open(p, encoding="utf-8").read()
a = s.index("# ======================================================================== 2. LLEGADA")
b = s.index("# ======================================================================== 3. PUERTA")
nuevo = open("_nuevo_ll.txt", encoding="utf-8").read()
s = s[:a] + nuevo + s[b:]


def rep(x, y):
    global s
    assert x in s, x[:70]
    s = s.replace(x, y, 1)


rep("PX0, PY0, PW, PH = 1090.0, 560.0, 130.0, 300.0     # el hueco de la puerta tapiada (centro-x del muro en 1100)",
    "PX0, PY0, PW, PH = 1090.0, 508.0, 96.0, 300.0      # el hueco de la puerta tapiada (el muro va de x=1030 a x=1150)")
rep('''        lz.relleno(rect_red(1080, 220, 40, PY0 - 220, 0), (150, 110, 110))
        lz.relleno(rect_red(1080, PY0 + PH, 40, 840 - (PY0 + PH), 0), (150, 110, 110))
        lz.relleno(rect_red(1080, 220, 40, 620, 0), (150, 110, 110), alfa=0.0)
        lz.relleno(rect_red(PX0 - PW / 2 - 14, PY0 - 14, PW + 28, PH + 14, 6), (150, 110, 110))''',
    '''        lz.relleno(rect_red(1030, 220, 120, PY0 - 220, 0), (150, 110, 110))                      # dintel
        lz.relleno(rect_red(1030, PY0, PX0 - PW / 2 - 1030, 840 - PY0, 0), (150, 110, 110))      # jamba izquierda
        lz.relleno(rect_red(PX0 + PW / 2, PY0, 1150 - (PX0 + PW / 2), 840 - PY0, 0), (150, 110, 110))   # jamba derecha''')
rep("lz.relleno(PANT * 0 + np.array([[1100, 220], [1770, 220], [1770, 840], [1100, 840]]), (10, 6, 24), alfa=0.92 * (1 - abierto))",
    "lz.relleno(np.array([[1030, 220], [1770, 220], [1770, 840], [1030, 840]]), (10, 6, 24), alfa=0.92 * (1 - abierto))")
rep("lz.relleno(rect_red(1100, 220, 670, 620, 6), (108, 78, 92))          # cámara de la derecha",
    "lz.relleno(rect_red(1030, 220, 740, 620, 6), (108, 78, 92))          # cámara de la derecha")
rep("lz.relleno(rect_red(150, 220, 950, 620, 6), (128, 92, 100))          # sala de los españoles",
    "lz.relleno(rect_red(150, 220, 880, 620, 6), (128, 92, 100))          # sala de los españoles")
rep("zoom = K(t, [(T0(E3), 1.0), (T_ROMPE - 0.4, 1.0), (T_ROMPE + 2.5, 1.35), (FIN(E3), 1.5)], e_inout)",
    "zoom = K(t, [(T0(E3), 1.28), (T_ROMPE - 0.4, 1.36), (T_ROMPE + 2.5, 1.5), (FIN(E3), 1.6)], e_inout)")
rep("cxx = K(t, [(T0(E3), 960.0), (T_ROMPE, 1000.0), (T_ROMPE + 2.5, 1230.0), (FIN(E3), 1230.0)], e_inout)",
    "cxx = K(t, [(T0(E3), 780.0), (T_ROMPE, 900.0), (T_ROMPE + 2.5, 1180.0), (FIN(E3), 1200.0)], e_inout)")
rep("cyy = K(t, [(T0(E3), 540.0), (T_ROMPE + 2.5, 600.0)], e_inout)", "cyy = K(t, [(T0(E3), 560.0), (T_ROMPE + 2.5, 600.0)], e_inout)")
rep("    cols, rows = 4, 10", "    cols, rows = 3, 10") if "    cols, rows = 4, 10" in s else None
s = s.replace("    cols, rows = 4, 10", "    cols, rows = 3, 10")
rep('''    # fuego que derrite para los españoles
    fa = smooth(prog(t, w_(E4, 3, 4), w_(E4, 3, 6)))''', '''    # un noble mexica admira el jade; un soldado español abraza el oro
    F.tlatoani(lz, 130 - 260 * (1 - mex), 860, 1.7, t, lado=1, brazos=0.35 + 0.1 * math.sin(t * 3), seed=2)
    F.soldado(lz, 1800 + 260 * mex, 860, 1.7, t, lado=-1, brazos=(-2.6, 2.6) if ind_e > 0.5 else (-0.3, 0.3), seed=7, carga=0.3)
    # fuego que derrite para los españoles
    fa = smooth(prog(t, w_(E4, 3, 4), w_(E4, 3, 6)))''')
open(p, "w", encoding="utf-8").write(s)
print("ok")
