# -*- coding: utf-8 -*-
"""Parche 3 de t03: trono y celda más cercanos y detallados, ricos sin amontonarse, arresto nocturno con luz y acción, golpe de estado animado en el Palacio."""
p = 't03.py'
s = open(p, encoding='utf-8').read()

# ---------------------------------------------------------------- trono + celda
a = s.index("def _celda(lz, iso, t, mx=0.0):")
b = s.index("# ------------------------------------------------------------------------------------------------ 5. LA CAPITAL: EL AYUNTAMIENTO")
nuevo = '''def _celda(lz, iso, t):
    import kz_iso_int as N
    c = I.habitacion(lz, iso, 0, 0, 260, 220, 140, piso=(104, 100, 112), pared_a=(142, 138, 152), pared_b=(122, 118, 136), friso=(86, 82, 98))
    for i in range(7):
        for j in range(6):
            I.suelo_rect(lz, iso, 6 + i * 36, 6 + j * 34, 34, 32, (120 + 8 * ((i + j) % 2), 116 + 8 * ((i + j) % 2), 130), z=0.1, alfa=0.8)
    # ventana alta con barrotes y haz de luz
    I.cara_rect(lz, iso, c, "yi", 100, 150, 70, 120, (180, 210, 250))
    for kx in range(4):
        I.cara_rect(lz, iso, c, "yi", 108 + kx * 12, 111 + kx * 12, 70, 120, (60, 56, 76))
    lz.relleno(iso.pts([(100, 4, 120), (150, 4, 120), (190, 150, 0), (110, 150, 0)]), (255, 244, 200), alfa=0.20, capa=2)
    # sillares en la pared, cadenas, antorcha, paja, jarra y un baúl
    for k in range(1, 8):
        I.cara_rect(lz, iso, c, "yi", 0, 260, k * 18 - 0.5, k * 18 + 0.5, (110, 106, 124), tono=False)
        I.cara_rect(lz, iso, c, "xi", 0, 220, k * 18 - 0.5, k * 18 + 0.5, (96, 92, 110), tono=False)
    N.cadenas(lz, iso, c, "yi", 40, 96, n=6, t=t)
    N.cadenas(lz, iso, c, "yi", 60, 90, n=5, t=t + 1.0)
    N.cadenas(lz, iso, c, "xi", 150, 96, n=6, t=t + 0.5)
    N.paja(lz, iso, 20, 120, 140, 210, n=110, seed=5)
    O.antorcha(lz, iso, 6, 80, t, h=64, seed=3)
    lz.halo(*iso.P(6, 80, 80), 200 * iso.z / 3.0, (255, 160, 80), alfa=0.18, capa=2)
    return c


@shot(T_TRONO, bg=lambda t: bg_grad((50, 28, 112), (140, 60, 130)), post=[GRAD], ent=("fundido", 0.5))
def p_trono(lz, t):
    import kz_iso_int as N
    I.luz()
    tn = e_inout(prog(t, T_PRIS, T_PRIS + 0.8))            # 0: pantalla completa del trono; 1: dividida por la mitad
    xdiv = lerp(W + 40, W / 2, tn)
    # --- mitad izquierda: el trono y José Bonaparte
    pol = np.array([[-10, -10], [xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10], [-10, H + 10]], float)
    with lz.recorte(pol):
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (66, 36, 130), capa=0)
        U.bokeh(lz, t, seed=5, n=10, colores=((255, 190, 90), (255, 80, 150), (120, 100, 255)), r=(50, 150), alfa=0.22)
        iso = I.Iso(150, 140, 30, 3.4, sx0=lerp(W / 2 + 40, 520, tn), sy0=640)
        c = md.dibujar_salon(lz, iso, t, tipo="trono")
        md._alfombra(lz, iso, 80, 60, 140, 190)
        m = I.Mundo()
        m.add(130, 40, 170, 80, 60, lambda lz, iso: md.trono(lz, iso, 150, 60, t, 1.2, corona=False), clave=100)
        k_c = e_inout(prog(t, t_herm - 0.2, t_herm + 0.9))
        m.add(130, 40, 170, 80, 60, lambda lz, iso: O2.corona(lz, iso, lerp(210, 150, k_c), lerp(100, 78, k_c), lerp(80, 74, k_c) + 12 * math.sin(math.pi * k_c), 0.9, rot=0.0), fijo=False, clave=300)
        m.add(140, 62, 160, 92, 60, lambda lz, iso: G.persona(lz, iso, 150, 82, t, "monarca", dir=(0, 1), seed=90, piel=G.PIELES[0], h=54, accion="saluda" if t > t_herm + 0.8 else None, z=14, cara="alegre" if t > t_herm + 0.8 else None), fijo=False, clave=250)
        m.add(190, 90, 210, 110, 60, lambda lz, iso: G.persona(lz, iso, 198, 100, t, "napoleon", dir=(-0.5, 1.0), seed=91, h=54, accion="chaleco" if t > t_herm + 0.8 else "habla", cara="serio"), fijo=False, clave=330)
        for i, (x, y) in enumerate(((70, 60), (70, 120), (230, 60), (230, 120), (80, 200), (220, 200))):
            m.add(x - 4, y - 4, x + 4, y + 4, 40, (lambda x, y, i: (lambda lz, iso: G.persona(lz, iso, x, y, t, "granadero" if i < 4 else "noble", dir=(0.6 if x < 150 else -0.6, 1), seed=92 + i, h=52, accion="vitorea" if (i >= 4 and t > t_herm + 1.0) else None)))(x, y, i), fijo=False, clave=x + y)
        m.add(14, 200, 28, 214, 30, lambda lz, iso: N.maceta(lz, iso, 20, 206, 1.3, t))
        m.dibujar(lz, iso)
        N.araña(lz, iso, 150, 130, 140, t, velas=6, s=1.3)
        kk = U.pop(t, t_herm - 0.1)
        if kk > 0.01:
            qx, qy = iso.P(150, 82, 110)
            U.llamada(lz, float(qx), float(qy) - 20, "José Bonaparte", color=U.COL["azul"], px=44, k=kk, cola="abajo")
    # --- mitad derecha: la celda del rey prisionero
    if tn > 0.01:
        pol2 = np.array([[xdiv + 26, -10], [W + 10, -10], [W + 10, H + 10], [xdiv - 26, H + 10], [xdiv + 26, H / 2]], float)
        with lz.recorte(pol2):
            lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (34, 36, 70), capa=0)
            iso2 = I.Iso(120, 120, 30, 3.4, sx0=lerp(W + 700, 1430, tn), sy0=640)
            _celda(lz, iso2, t)
            m2 = I.Mundo()
            m2.add(100, 80, 140, 130, 60, lambda lz, iso: G.persona(lz, iso, 112, 124, t, "monarca", dir=(0.3, 1), seed=71, piel=G.PIELES[0], h=54, cara="triste"), fijo=False, clave=200)
            m2.add(100, 80, 140, 130, 60, lambda lz, iso: O2.grillete(lz, iso, 112, 124, 4, t), fijo=False, clave=201)
            m2.add(60, 150, 70, 160, 60, lambda lz, iso: G.persona(lz, iso, 190, 166, t, "granadero", dir=(-1, 0.4), seed=95, h=54), fijo=False, clave=350)
            m2.add(50, 20, 60, 30, 60, lambda lz, iso: O.barril(lz, iso, 40, 40, 1.2), clave=90)
            m2.add(60, 60, 70, 70, 30, lambda lz, iso: N.jarra_pan(lz, iso, 70, 150, 1.3), clave=140)
            m2.add(200, 20, 224, 40, 40, lambda lz, iso: N.baul(lz, iso, 200, 24), clave=100)
            m2.dibujar(lz, iso2)
            O2.barrotes(lz, iso2, 10, 214, 240, 100, n=12, z=0.0)
            kk = U.pop(t, t_pris - 0.5)
            if kk > 0.01:
                qx, qy = iso2.P(112, 124, 110)
                U.llamada(lz, float(qx) + 40, float(qy) - 30, "El rey, prisionero", color=U.COL["rojo"], px=44, k=kk, cola="abajo")
        lz.trazo(np.array([[xdiv - 26, -10], [xdiv + 26, H / 2], [xdiv - 26, H + 10]]), (255, 255, 255), 6.0, afinar=False, temblor=0.0, capa=2)
    kf = U.pop(t, T_TRONO + 0.2) * U.salida(t, t_pron - 0.1, 0.3)
    if kf > 0.01:
        U.llamada(lz, 440, 130, "su propio hermano", color=U.COL["naranja"], px=56, k=kf, cola=None)


'''
s = s[:a] + nuevo + s[b:]

# ---------------------------------------------------------------- capital: zoom máximo 6; etiquetas separadas
s = s.replace("return Klog(t, [(T_AYU, (-99.13, 19.43, 1.6)), (T_AYU + 1.5, (-99.13, 19.43, 14.0))])", "return Klog(t, [(T_AYU, (-99.13, 19.43, 1.6)), (T_AYU + 1.4, (-99.13, 19.43, 6.0))])")
s = s.replace('U.llamada(lz, W / 2, 150, "¡Algo inaudito!", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_inau + 0.4), cola=None)', 'U.llamada(lz, W / 2, 960, "¡Algo inaudito!", color=U.COL["rojo"], px=64, k=k * U.repop(t, t_inau + 0.4), cola=None)')

# ---------------------------------------------------------------- ricos: composición limpia
a = s.index("    # los ricos españoles: tres retratos furiosos en fila + «¡TRAICIÓN!»")
b = s.index("# ------------------------------------------------------------------------------------------------ 7. EL ARRESTO DE NOCHE")
nuevo = '''    # los ricos españoles: tres retratos furiosos en fila + «¡TRAICIÓN!» (el virrey sale de escena)
    kr = U.pop(t, T_RICOS)
    if kr > 0.01:
        lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]], float), (60, 10, 40), alfa=0.9 * min(1.0, kr), capa=0)
        for i, (qn, px_, sh) in enumerate((("peninsular", 330, 0), ("yermo", 960, 1), ("carlos", 1590, 2))):
            ki = U.pop(t, T_RICOS + 0.15 * i, 1.2)
            if ki > 0.01:
                RT.retrato(lz, px_, 1010, 150 * ki, qn, t, emocion="enojo", habla=0.3 if t > t_trai else 0.0, mirar=(i - 1) * 0.2, seed=20 + i, luz_borde=(255, 120, 90))
        U.titulo_grande(lz, t, t_trai - 0.1, T1(E3) - 18, "¡TRAICIÓN!", x=W / 2, y=240, px=170, color=(255, 90, 90))
        kk = U.pop(t, t_ricos) * U.salida(t, t_trai, 0.2)
        if kk > 0.01:
            U.llamada(lz, W / 2, 130, "ricos españoles", color=U.COL["naranja"], px=60, k=kk, cola=None)


'''
s = s[:a] + nuevo + s[b:]
# el virrey sale cuando entran los ricos
s = s.replace('    RT.retrato(lz, 640, 960, 215 * (0.92 + 0.08 * k), "virrey", t, emocion="serio" if t < t_acep else "pensativo", habla=0.0, mirar=0.35, seed=5)\n    U.llamada(lz, 640, 150, "El virrey Iturrigaray", color=U.COL["rojo"], px=56, k=U.pop(t, t_vir) * U.salida(t, T_RICOS - 0.2), cola=None)',
              '    kv = U.salida(t, T_RICOS - 0.1, 0.25)\n    if kv > 0.01:\n        RT.retrato(lz, 640, 960, 215 * (0.92 + 0.08 * k), "virrey", t, emocion="serio" if t < t_acep else "pensativo", habla=0.0, mirar=0.35, seed=5, alfa=kv)\n    U.llamada(lz, 640, 150, "El virrey Iturrigaray", color=U.COL["rojo"], px=56, k=U.pop(t, t_vir) * U.salida(t, T_RICOS - 0.2), cola=None)')
open(p, 'w', encoding='utf-8').write(s)
print('ok')
