# -*- coding: utf-8 -*-
p = 'cap_plata.py'
s = open(p, encoding='utf-8').read()
a = s.index("    # monedas: barras que se vuelven monedas y salen en abanico")
s = s[:a] + '''    # monedas: barras que se vuelven monedas y salen en abanico hacia Europa, Asia y África
    if t >= A["monedas"] - 0.6:
        u = t - A["monedas"]
        # pila de barras en Sevilla (aparece un poco antes)
        kb = e_back(prog(t, A["monedas"] - 0.6, A["monedas"] - 0.2))
        if kb > 0.01 and u < 1.2:
            for i in range(3):
                with lz.grupo(SEV[0] - 60 + 60 * i, SEV[1] - 40 - 14 * (i % 2), kb * 1.4 / z * 0.2):
                    lz.relleno(np.array([[-46, -14], [46, -14], [58, 16], [-58, 16]]), V.PLATA, temblor=0.0, capa=2)
        dirs = [(-0.75, "GUERRAS", A["guerras"]), (0.05, "IMPERIOS", A["imperios"]), (0.75, "COMERCIO", A["comercio"])]
        for j, (ang, txt, t0) in enumerate(dirs):
            for i in range(9):
                v = clamp01((u - 0.05 - 0.17 * i - 0.25 * j) / 2.6)
                if v <= 0 or v >= 1:
                    continue
                d = 3400 * e_out(v) * (0.55 + 0.08 * (i % 4))
                a_ = ang + 0.10 * ((i % 3) - 1)
                x = SEV[0] + d * math.cos(a_) * 1.05
                y = SEV[1] - 80 + d * math.sin(a_) * 0.7 - 420 * math.sin(math.pi * v)
                moneda(lz, x, y, 34 / z * 0.35, rot=v * 9 * (1 if i % 2 else -1), alfa=1 - 0.7 * smooth(prog(v, 0.85, 1.0)))
            k = e_back(prog(t, t0, t0 + 0.35), 1.7)
            if k > 0.01:
                x = SEV[0] + 2300 * math.cos(ang) * 1.05
                y = SEV[1] - 80 + 2300 * math.sin(ang) * 0.7 - 380
                etiqueta(lz, t, t0, x, y, txt, z, px=30, fondo=V.AMARILLO)
'''
open(p, 'w', encoding='utf-8').write(s)

p = 'escenas.py'
s = open(p, encoding='utf-8').read()
a = s.index('    KM(A_PL["ini"] + 2.2, 2650, -380, 0.19),')
b = s.index('    KL(A_Z["hoy"] - 0.3, -170, SUR + 2040, 1.7),')
s = s[:a] + '''    KM(A_PL["ini"] + 2.2, 2680, -380, 0.165),
    KM(A_PL["lejos"] - 0.6, 2680, -380, 0.165),
    KM(A_PL["monedas"] - 0.2, SEV[0] - 300, SEV[1] - 100, 0.30),
    KM(A_Z["ini"] - 0.4, SEV[0] - 300, SEV[1] - 100, 0.30),
    KM(A_Z["ini"] + 0.9, 1500, -300, 0.22),
    KM(A_Z["ini"] + 1.9, 40, -40, 1.5),
    KL(A_Z["ini"] + 2.9, -170, SUR + 2040, 1.7),
''' + s[b:]
open(p, 'w', encoding='utf-8').write(s)

p = 'cap_cierre.py'
s = open(p, encoding='utf-8').read()
open(p, 'w', encoding='utf-8').write(s)

p = 'escenas.py'
s = open(p, encoding='utf-8').read()
s = s.replace('ka = smooth(prog(t, A_Z["costo"] + 3.0, A_Z["costo"] + 4.5))', 'ka = smooth(prog(t, A_Z["ini"] + 2.6, A_Z["ini"] + 3.4))')
s = s.replace('if t >= A_Z["costo"] + 2.0:\n            self.cierre', 'if t >= A_Z["ini"] + 1.8:\n            self.cierre')
open(p, 'w', encoding='utf-8').write(s)

p = 'ui_caps.py'
s = open(p, encoding='utf-8').read()
s = s.replace('titular(lz, t, a["costo"] - 0.1, a["oscuridad"] + 0.9, ["EL COSTO"], y=470, px=96, color=V.CREMA, marca=False)',
              'titular(lz, t, a["ini"] + 0.4, a["pagaron"] + 0.6, ["EL COSTO"], y=470, px=100, color=V.TINTA, marca=True)')
open(p, 'w', encoding='utf-8').write(s)

p = 'cap_mina.py'
s = open(p, encoding='utf-8').read()
s = s.replace("        S.veta(lz, t, hasta=1.0)\n", "        S.veta(lz, t, hasta=1.0)\n        lz.trazo(np.array([[-380, 0], [380, 0], [380, 3450], [-380, 3450]]), V.CREMA, 9, cerrado=True, afinar=False, temblor=0.0, capa=1)\n")
open(p, 'w', encoding='utf-8').write(s)

p = 'mapa_dib.py'
s = open(p, encoding='utf-8').read()
s = s.replace('''def mar(lz, alfa=1.0, color=MAR_C):
    with lz.capa(0):
        lz.relleno(np.array([[-40000, -40000], [60000, -40000], [60000, 40000], [-40000, 40000]]), color, alfa=alfa, temblor=0.0)''', '''def olas_mar(lz, alfa, z):
    """Marcas de oleaje (trazos cortos claros) repartidas por el océano; se dibujan solo si son visibles."""
    if z > 0.5:
        return
    for i in range(140):
        x = -800 + 7400 * h01(31, i, 1)
        y = -2000 + 3600 * h01(31, i, 2)
        with lz.capa(0):
            lz.trazo(np.array([[x - 46, y], [x - 16, y - 12], [x + 12, y], [x + 40, y - 10]]), (196, 224, 226), 8, afinar=False,
                     temblor=0.0, capa=0, paso=14.0) if alfa > 0.5 else None


def mar(lz, alfa=1.0, color=MAR_C, z=1.0):
    with lz.capa(0):
        lz.relleno(np.array([[-40000, -40000], [60000, -40000], [60000, 40000], [-40000, 40000]]), color, alfa=alfa, temblor=0.0)
    olas_mar(lz, alfa, z)''')
open(p, 'w', encoding='utf-8').write(s)
p = 'cap_mapa.py'
s = open(p, encoding='utf-8').read()
s = s.replace("M.mar(lz, alfa=a * smooth(prog(t, 0.0, 0.5)))", "M.mar(lz, alfa=a * smooth(prog(t, 0.0, 0.5)), z=z)")
open(p, 'w', encoding='utf-8').write(s)
print("ok")
