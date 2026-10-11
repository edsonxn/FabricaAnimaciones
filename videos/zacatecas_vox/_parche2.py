# -*- coding: utf-8 -*-
p = 'cap_mapa.py'
s = open(p, encoding='utf-8').read()
s = s.replace('''    u = clamp01((math.log(max(z, 1e-6)) - math.log(1.6)) / (math.log(9.0) - math.log(1.6)))
    return 1.0 - smooth(u)''', '''    u = clamp01((math.log(max(z, 1e-6)) - math.log(1.2)) / (math.log(6.0) - math.log(1.2)))
    return 1.0 - smooth(u)''')
s = s.replace('''    M.sierras(lz, alfa=a''', '''    reposo = t > A["fin"] + 1.0        # tras la primera vez, el mapa se muestra limpio (sin rótulos)
    M.sierras(lz, alfa=a''')
s = s.replace('''    mx, my = G.xy(*G.CIUDADES["mexico"])
    kn = _pop(t, A["nueva"] + 0.1)''', '''    mx, my = G.xy(*G.CIUDADES["mexico"])
    if reposo:
        zx, zy = G.xy(*G.CIUDADES["zacatecas"])
        M.edificio_mexico(lz, mx, my + 4, 0.55 / max(z, 0.3) * 1.1, alfa=a)
        M.estrella(lz, zx, zy, 30 / max(z, 0.3), alfa=a, color=V.ROJO)
        return
    kn = _pop(t, A["nueva"] + 0.1)''')
open(p, 'w', encoding='utf-8').write(s)

p = 'cap_local.py'
s = open(p, encoding='utf-8').read()
s = s.replace('''    u = clamp01((math.log(max(z, 1e-6)) - math.log(1.5)) / (math.log(8.0) - math.log(1.5)))
    return smooth(u)''', '''    u = clamp01((math.log(max(z, 1e-6)) - math.log(3.0)) / (math.log(12.0) - math.log(3.0)))
    return smooth(u)''')
open(p, 'w', encoding='utf-8').write(s)

p = 'mapa_dib.py'
s = open(p, encoding='utf-8').read()
s = s.replace("[[-9000, -6000], [16000, -6000], [16000, 6000], [-9000, 6000]]", "[[-40000, -40000], [60000, -40000], [60000, 40000], [-40000, 40000]]")
open(p, 'w', encoding='utf-8').write(s)

p = 'cap_cerro.py'
s = open(p, encoding='utf-8').read()
s = s.replace("MINAS34_X = [(-1900 + i * 118 + 30 * h01(77, i)) for i in range(34)]", "MINAS34_X = [(-1150 + i * 72 + 14 * h01(77, i)) for i in range(34)]")
s = s.replace("bocamina(lz, MINAS34_X[i], 16 - 18 * (i % 2), 0.95, prog(", "bocamina(lz, MINAS34_X[i], 20 - 30 * (i % 2), 1.25, prog(")
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- mina: tiempos
p = 'cap_mina.py'
s = open(p, encoding='utf-8').read()
a = s.index("T_CLIMB0 = ")
b = s.index("def u_escalera")
s = s[:a] + "T_CLIMB0 = A[\"carg\"] + 0.6\nT_CLIMB1 = A[\"fin\"] - 0.2\n\n\n" + s[b:]
a = s.index("def camara_pos")
b = s.index("def dibujar")
s = s[:a] + '''def camara_pos(t):
    """Centro de cámara local que sigue la acción de la mina. Devuelve (lx, ly, zl)."""
    t_g1 = A["ini"] + 1.7                       # llega a la galería 1
    t_f0, t_f1 = A["carg"] - 0.5, A["carg"] + 1.5   # caída a la galería 3
    if t < t_g1:
        u = e_inout(prog(t, A["ini"], t_g1))
        return lerp(-40, -250, u), lerp(SUR + 60, SUR + Y_G1 - 60, u), lerp(1.5, 1.25, u)
    if t < t_f0:
        return -250, SUR + Y_G1 - 60, 1.25
    if t < t_f1:
        u = e_inout(prog(t, t_f0, t_f1))
        return lerp(-250, -40, u), lerp(SUR + Y_G1 - 60, SUR + Y_G3 - 120, u), lerp(1.25, 1.35, u)
    x, y, d = pos_cargador(t)
    return -40, y - 180, 1.35


''' + s[b:]
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- camino
p = 'cap_camino.py'
s = open(p, encoding='utf-8').read()
a = s.index("X_ATAQUE = ")
b = s.index("def x_tren")
s = s[:a] + '''X_ATAQUE = 1000.0
X_FUERTE = 1900.0
X_PAZ = 2500.0
TREN = [(INI("patio"), -560.0), (A["ini"], -560.0), (A["ini"] + 3.0, 160.0), (A["atacan"] - 0.3, X_ATAQUE),
        (A["conflicto"] + 2.0, X_ATAQUE), (A["presidios"] + 2.2, X_FUERTE), (A["basta"] + 0.3, X_FUERTE),
        (A["n90"] + 0.6, X_PAZ - 320), (A["fin"], X_PAZ - 320)]


''' + s[b:]
s = s.replace("camino_cinta(lz, -1500, 4800)", "camino_cinta(lz, -480, 4200)")
# caravana con ciclo rápido (30 dib/s => 4 poses distintas a 15 dibujos/s)
s = s.replace("f = V.cuadro(V.CAMINAR, t + 0.09 * i, 15.0) if marcha else 0", "f = V.cuadro(V.CAMINAR, t + 0.09 * i, 30.0) if marcha else 0")
s = s.replace("fr = V.cuadro(V.CAMINAR, t, 15.0) if marcha else 0", "fr = V.cuadro(V.CAMINAR, t, 30.0) if marcha else 0")
s = s.replace("V.cuadro(V.CAMINAR, t + i * 0.1, 15.0) if marcha else V.IDLE[0]", "V.cuadro(V.CAMINAR, t + i * 0.1, 30.0) if marcha else V.IDLE[0]")
s = s.replace('''    for i, bx in enumerate((X_ATAQUE + 380, X_ATAQUE + 470, X_ATAQUE + 560)):''', '''    for i, (bx, by) in enumerate(((742, -470), (800, -520), (838, -640))):''')
s = s.replace("            yb = float(L.h(bx)) + 60\n", "            yb = by\n")
s = s.replace("            xs = lerp(X_ATAQUE + 380, X_ATAQUE - 240, ph)\n            ys = y_camino(xs) - 260 - 200 * math.sin(math.pi * ph)\n            flecha(lz, np.array([xs, ys]), math.pi - 0.5 + 1.1 * ph, 1.0)",
              "            xs = lerp(760, X_ATAQUE - 60 - 90 * i, ph)\n            ys = lerp(-500, y_camino(xs) - 30, ph) - 220 * math.sin(math.pi * ph)\n            flecha(lz, np.array([xs, ys]), 1.1 + 1.0 * ph - 0.2 * i, 1.0)")
s = s.replace("if A[\"camino\"] - 1.0 < t < A[\"camino\"] + 6:\n        letrero(lz, -150, y_camino(-150) - 10, \"MÉXICO →\", 1.2)",
              "if A[\"llegar\"] - 1.0 < t < A[\"camino\"] + 5:\n        letrero(lz, 60, y_camino(60) - 6, \"MÉXICO →\", 1.2)")
open(p, 'w', encoding='utf-8').write(s)

# ---------------------------------------------------------------- escenas: cámara con tiempos reales
p = 'escenas.py'
s = open(p, encoding='utf-8').read()
a = s.index("T_DIVE0 = ")
b = s.index("ZX, ZY = ")
s = s[:a] + "T_DIVE0 = CM.A[\"chichi\"] + 0.5\nT_LLEGADA = T_DIVE0 + 3.4\n" + s[b:]
a = s.index("CAM_A = Camara([")
b = s.index("def camara(t):")
nuevo = '''CAM_A = Camara([   # del mapa hasta el inicio de la mina
    KM(0.0, 20, -50, 0.58),
    KM(CM.A["seis"], 20, -50, 0.6),
    KM(T_DIVE0, 4, -30, 0.7),
    KL(T_LLEGADA, -200, -240, 1.0),
    KL(A_C["tolosa"] + 0.5, -250, 10, 2.5),
    KL(A_C["llega"] + 0.6, -240, 10, 2.4),
    KL(A_C["llega"] + 1.8, 20, -60, 1.7),
    KL(A_C["bufa"] + 0.2, 560, -380, 0.85),
    KL(A_C["arma"] + 0.9, 520, -60, 1.5),
    KL(A_C["veta"] - 0.1, 740, -245, 1.3),
    KL(A_C["fiebre"] + 0.5, 500, -100, 0.9),
    KL(INI("campamento") + 0.5, 200, -140, 0.95),
    KL(A_CM["casas"] + 0.3, 130, -50, 1.3),
    KL(A_CM["laderas"] + 0.3, 380, -100, 1.2),
    KL(A_CM["caro"] + 0.3, 300, -40, 1.3),
    KL(A_CM["ranch"] + 0.5, 520, -40, 1.15),
    KL(A_CM["t34"] - 0.5, 100, -180, 0.45),
    KL(A_CM["hosp"] + 0.8, 100, -180, 0.45),
    KL(A_M["ini"] - 0.1, -40, SUR + 60, 1.5),
], respira=0.0)
CAM_B = Camara([   # patio, camino, mapa de vuelta, ciudad, ruta de la plata, cierre
    KL(A_M["fin"] - 0.2, -40, -30, 1.35),
    KL(A_P["ini"] + 2.6, -830, -140, 1.15),
    KL(A_P["mulas"] - 0.6, -830, -120, 1.25),
    KL(A_P["atrapa"] - 0.4, -830, -60, 1.5),
    KL(A_P["atrapa"] + 1.5, -830, -30, 2.6),
    KL(A_P["pobre"] + 0.4, -700, -60, 1.2),
    KL(A_P["espana"] + 0.3, -540, -100, 1.0),
    KL(A_CA["ini"] + 0.6, -300, -150, 1.4),
    KL(A_CA["camino"] + 0.4, 250, -150, 1.4),
    KL(A_CA["atacan"] - 0.4, 820, -330, 0.85),
    KL(A_CA["conflicto"] + 2.0, 820, -330, 0.85),
    KL(A_CA["presidios"] + 0.2, 1500, -200, 1.0),
    KL(A_CA["escolta"] + 1.0, 1800, -150, 1.4),
    KL(A_CA["basta"] + 0.4, 2000, -140, 1.4),
    KL(A_CA["n90"] + 0.8, X_PAZ_ - 100, -150, 1.5),
    KL(A_CA["paz"] + 0.6, X_PAZ_ + 40, -130, 2.0),
    KL(A_CA["fin"] - 0.5, X_PAZ_ + 40, -130, 2.0),
    KM(A_CA["fin"] + 0.7, 4, -40, 2.0),            # sale al mapa ...
    KL(A_CD["ciudad0"] + 0.8, 20, -100, 1.0),       # ... y vuelve a Zacatecas (ya ciudad)
    KL(A_CD["convento"] + 0.2, 60, -100, 1.5),
    KL(A_CD["o85"] + 0.5, 30, -100, 1.0),
    KL(A_CD["mercados"] + 0.1, 0, -80, 1.15),
    KL(A_CD["fin"] + 0.3, 0, -80, 1.15),
    KM(A_PL["ini"] + 2.2, 2650, -380, 0.19),
    KM(A_PL["contin"] - 3.6, 2650, -380, 0.19),
    KM(A_PL["monedas"] + 0.6, SEV[0] + 300, SEV[1] + 100, 0.15),
    KM(A_Z["ini"] - 0.3, SEV[0] + 300, SEV[1] + 100, 0.15),
    KM(A_Z["ini"] + 1.8, 1500, -300, 0.22),
    KM(A_Z["ini"] + 3.0, 40, -40, 1.5),
    KL(A_Z["ini"] + 4.2, -170, SUR + 2040, 1.7),
    KL(A_Z["hoy"] - 0.3, -170, SUR + 2040, 1.7),
    KL(A_Z["hoy"] + 2.2, -30, -290, 0.72),
    KL(A_Z["patrimonio"] + 1.6, -30, -290, 0.72),
    KL(A_Z["calle"] + 0.4, 130, -130, 1.05),
    KL(A_Z["bajo"] + 0.3, -40, SUR - 30, 1.9),
    KL(A_Z["fin"] + 1.6, -40, SUR + 40, 3.2),
    KL(A_Z["fin"] + 4.0, -40, SUR + 40, 3.2),
], respira=0.0)


'''
s = s[:a] + nuevo + s[b:]
s = s.replace("ZX, ZY = G.xy", "X_PAZ_ = CC.X_PAZ\nZX, ZY = G.xy")
open(p, 'w', encoding='utf-8').write(s)
print('ok')
