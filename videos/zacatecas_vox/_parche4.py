# -*- coding: utf-8 -*-
import re


def rw(p, fn):
    s = open(p, encoding='utf-8').read()
    s2 = fn(s)
    assert s2 != s, p
    open(p, 'w', encoding='utf-8').write(s2)


def rep(s, a, b, cnt=1):
    assert a in s, a[:70]
    return s.replace(a, b, cnt)


# ---------------------------------------------------------------- 1. años: el odómetro llega al número al decirlo
def f(s):
    a = s.index("AÑO = Anios([")
    b = s.index("def alfa_placa")
    return s[:a] + '''AÑO = Anios([
    (0.0, 1500), (CM.A["seis"] + 0.25, 1546, 1.8),
    (A_C["ocho"] + 0.3, 1548, 0.8),
    (A_CM["c49"] + 0.3, 1549, 0.8),
    (A_CM["c50"] + 0.4, 1550, 0.8),
    (A_P["siete"] + 0.3, 1557, 1.0),
    (A_CA["c50"] + 0.4, 1550, 1.0),
    (A_CA["n90"] + 0.4, 1590, 1.6),
    (A_CD["c58"] + 0.3, 1558, 2.0),
    (A_CD["o85"] + 0.9, 1585, 1.2),
    (A_CD["o88"] + 0.8, 1588, 0.8),
])


''' + s[b:]


rw('escenas.py', f)

# ---------------------------------------------------------------- 2. odómetro: fundido en vez de recorte duro
def f(s):
    a = s.index("                with lz.recorte(celda):")
    b = s.index("            lz.relleno(np.array([[-w / 2 + 20, h / 2 - 9]")
    return s[:a] + '''                with lz.recorte(celda):
                    lz.texto(str(d), xx, DIG_PX * 0.05 - roll * CELDA_H * 0.9, DIG_PX, "vox_x", color=color, borde=None,
                             alfa=alfa * (1 - roll), temblor=0.0)
                    if roll > 0.001:
                        lz.texto(str((d + 1) % 10), xx, DIG_PX * 0.05 + (1 - roll) * CELDA_H * 0.9, DIG_PX, "vox_x",
                                 color=color, borde=None, alfa=alfa * roll, temblor=0.0)
''' + s[b:]


rw('ui_vox.py', f)


def f(s):
    s = rep(s, 'def contador(lz, valor, texto, cx, cy, px=170, alfa=1.0, color=V.AMARILLO, sufijo="", fuente="vox_x"):',
            'def contador(lz, valor, texto, cx, cy, px=170, alfa=1.0, color=V.AMARILLO, sufijo="", fuente="vox_x", color2=V.CREMA):')
    s = rep(s, 'V.rotulo(lz, texto, cx, cy + px * 0.72, px * 0.27, color=V.CREMA, fuente="vox_b", alfa=alfa, sombra=0.5)',
            'V.rotulo(lz, texto, cx, cy + px * 0.72, px * 0.27, color=color2, fuente="vox_b", alfa=alfa, sombra=0.0)')
    return s


rw('ui_vox.py', f)

# ---------------------------------------------------------------- 3. ui_caps
def f(s):
    s = rep(s, 'U.contador(lz, n, "MINAS EN OPERACIÓN · 1550", CX, 520, px=200 * k, alfa=k, color=V.AMARILLO)',
            'U.contador(lz, n, "MINAS EN OPERACIÓN · 1550", CX, 520, px=200 * k, alfa=k, color=V.ROJO, color2=V.TINTA)')
    s = rep(s, 'cnt = 300 * e_out(prog(t, a["tres"] - 0.3, a["tres"] + 1.4))', 'cnt = 300 * e_out(prog(t, a["tres"] - 0.3, a["tres"] + 1.2))\n        cnt = 300 if cnt > 299.5 else cnt')
    s = rep(s, 'V.pastilla(lz, cx_ - 90 * u, 830, "PARA EL DUEÑO", 24, k=k * u, fondo=V.CREMA)\n        V.pastilla(lz, cx_ + 90 * u, 890, "PARA ÉL", 24, k=k * u, fondo=V.AMARILLO)',
            'V.pastilla(lz, cx_ - 110 * u, 850, "PARA EL DUEÑO", 32, k=k * u, fondo=V.CREMA)\n        V.pastilla(lz, cx_ + 110 * u, 930, "PARA ÉL", 32, k=k * u, fondo=V.AMARILLO)')
    s = rep(s, '''        V.rotulo(lz, f"{int(v)}", CX, 560, 170 * k, color=V.ROJO, sombra=0.0)
        V.rotulo(lz, "AFRICANOS EN 1597", CX, 650, 40 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)''',
            '''        if t > a["doscientos"] - 0.3:
            V.rotulo(lz, f"{int(v)}", CX, 560, 170 * k, color=V.ROJO, sombra=0.0)
        V.rotulo(lz, "AFRICANOS EN 1597", CX, 650, 40 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)''')
    return s


rw('ui_caps.py', f)


def f(s):
    s = rep(s, 'V.rotulo(lz, "1588", W / 2, 1160, 110, color=V.CREMA, alfa=k)', 'V.pastilla(lz, W / 2, 400, "1588", 70, k=k, fondo=V.AMARILLO)')
    return s


rw('cap_ciudad.py', f)

# ---------------------------------------------------------------- 4. mapa: rótulos solo cuando el mapa se ve entero; ortografía
def f(s):
    s = rep(s, "    reposo = t > A[\"fin\"] + 1.0", "    rotulos = z < 1.0\n    reposo = t > A[\"fin\"] + 1.0")
    s = rep(s, 'etiqueta(lz, t, A["chichi"] + 0.9, zx, zy - 64 / z, "ZACATECAS"', 'etiqueta(lz, t, A["chichi"] + 0.9, zx, zy - 110 / z, "ZACATECAS"')
    s = rep(s, '"GUACHICHILES"', '"HUACHICHILES"')
    # etiquetas y líneas de llamada solo con z < 1
    s = rep(s, "    if t >= A[\"zacatecos\"]:\n", "    if t >= A[\"zacatecos\"] and rotulos:\n")
    s = rep(s, "    if t >= A[\"huachi\"]:\n", "    if t >= A[\"huachi\"] and rotulos:\n")
    return s


rw('cap_mapa.py', f)

# ---------------------------------------------------------------- 5. odre
def f(s):
    s = rep(s, "        odre(lz, 470, -690, 2.2 * ko)\n        V.trazo_mano(lz, np.array([[560, -700], [660, -690], [790, -560]]), prog(t, A[\"odre\"] + 0.3, A[\"odre\"] + 1.0), V.CREMA, 10, seed=3)",
            "        odre(lz, 590, -560, 1.7 * ko)\n        V.pastilla(lz, 590, -430, \"ODRE DE VINO\", 30, k=ko, fondo=V.CREMA)\n        V.trazo_mano(lz, np.array([[700, -600], [780, -640], [850, -700]]), prog(t, A[\"odre\"] + 0.3, A[\"odre\"] + 1.0), V.CREMA, 10, seed=3)")
    s = rep(s, 'bocamina(lz, MINAS34_X[i], 20 - 30 * (i % 2), 1.25, prog(', 'bocamina(lz, MINAS34_X[i], 4 - 44 * (i % 2), 1.7, prog(')
    s = rep(s, "MINAS34_X = [(-1150 + i * 72 + 14 * h01(77, i)) for i in range(34)]", "MINAS34_X = [(-1300 + (i // 2) * 160 + (i % 2) * 80 + 10 * h01(77, i)) for i in range(34)]")
    return s


rw('cap_cerro.py', f)

# ---------------------------------------------------------------- 6. patio: piña más pequeña
def f(s):
    s = rep(s, "lz.relleno(V.elipse_pts(0, -50 * pina, 66 * pina, 56 * pina), V.PLATA", "lz.relleno(V.elipse_pts(0, -30 * pina, 40 * pina, 34 * pina), V.PLATA")
    s = rep(s, "lz.relleno(V.elipse_pts(-16 * pina, -66 * pina, 28 * pina, 20 * pina), V.aclarar(V.PLATA, 0.7)", "lz.relleno(V.elipse_pts(-10 * pina, -40 * pina, 17 * pina, 12 * pina), V.aclarar(V.PLATA, 0.7)")
    s = rep(s, "L.chispa(lz, 40 * pina, -96 * pina, 26 * pina, t, capa=2)", "L.chispa(lz, 26 * pina, -58 * pina, 20 * pina, t, capa=2)")
    return s


rw('cap_patio.py', f)

# ---------------------------------------------------------------- 7. guachichil
def f(s):
    a = s.index('    "guachichil": dict(')
    b = s.index('    "fraile": dict(')
    return s[:a] + '''    "guachichil": dict(piel=PIELES[1], ropa=(186, 74, 58), ropa2=(240, 230, 200), pant=PIELES[1], bota=None,
                       sombrero="pintura", sombrero_col=ROJO, pelo=(24, 20, 22), falda=22, pintura=True),
''' + s[b:]


rw('../../nucleo/vox.py', f)

# ---------------------------------------------------------------- 8. plata: etiquetas dentro de pantalla y geografía rotulada
def f(s):
    s = rep(s, "x = SEV[0] + 1250 * math.cos(ang) * 1.05\n                y = SEV[1] - 80 + 1250 * math.sin(ang) * 0.7 - 330", "x = SEV[0] + 900 * math.cos(ang) * 1.0 - 100\n                y = SEV[1] - 80 + 1000 * math.sin(ang) * 0.6 - 330")
    s = rep(s, "moneda(lz, x, y, 30 / z,", "moneda(lz, x, y, 36 / z,")
    s = rep(s, "    # monedas: barras que se vuelven monedas", '''    # rótulos de la geografía (España, Francia, África) mientras se ve el Atlántico oriental
    if A["sevilla"] < t < A["contin"] + 1.5 and z < 0.4:
        for lon_lat, txt in (((-3.5, 40.0), "ESPAÑA"), ((2.0, 47.0), "FRANCIA"), ((-2.0, 30.5), "ÁFRICA")):
            gx, gy = G.xy(*lon_lat)
            V.rotulo(lz, txt, gx, gy, 26 / z * 0.9, color=V.TINTA, fuente="vox_b", sombra=0.0)
    # monedas: barras que se vuelven monedas''')
    return s


rw('cap_plata.py', f)

# ---------------------------------------------------------------- 9. extensiones del mundo
def f(s):
    s = rep(s, "L.colinas_fondo(lz, cam_l[0], 0.3, -180, 520, 1.0, (206, 172, 190), -4200, 4200,", "L.colinas_fondo(lz, cam_l[0], 0.3, -180, 520, 1.0, (206, 172, 190), -14000, 14000,")
    s = rep(s, "L.colinas_fondo(lz, cam_l[0], 0.6, -40, 360, 3.0, (196, 146, 138), -4200, 4200,", "L.colinas_fondo(lz, cam_l[0], 0.6, -40, 360, 3.0, (196, 146, 138), -14000, 14000,")
    s = rep(s, "L.suelo(lz, -3400, 6400, SUR, alfa=a3)", "L.suelo(lz, -20000, 20000, SUR, alfa=a3)")
    return s


rw('cap_local.py', f)
print("ok")
