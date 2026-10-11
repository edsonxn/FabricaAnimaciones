# -*- coding: utf-8 -*-
sd = open("s_d.py", encoding="utf-8").read()


def rep(a, b):
    global sd
    if a not in sd:
        print("NO ENCONTRADO:", a[:70])
        return
    sd = sd.replace(a, b, 1)


# cables, tubería y cerámica en el subsuelo + fantasma del templo
rep('''def _piedra_luna(lz, x, y, r, t, brillo=0.0):''', '''def _detalles_subsuelo(lz, t):
    """Cables (los electricistas), tubería, cascotes y raíces para que el terreno no quede vacío; etiquetas de capas."""
    for k in range(60):
        x = -300 + 50 * k
        lz.relleno(rect_red(x, SY + 58, 26, 9, 2), (255, 214, 60) if k % 2 == 0 else (40, 40, 52))
    lz.relleno(rect_red(-400, SY + 92, 3000, 14, 6), (70, 140, 210))
    lz.relleno(rect_red(-400, SY + 96, 3000, 4, 2), (150, 200, 250))
    for i in range(46):
        x = -300 + 2600 * h01(31, i)
        y = SY + 150 + 700 * h01(32, i) ** 1.3
        c = [(210, 160, 110), (150, 130, 150), (226, 190, 140), (120, 100, 120)][i % 4]
        lz.relleno(np.array([[x, y], [x + 22, y - 6], [x + 30, y + 10], [x + 6, y + 18]]) * 1.0, c, alfa=0.8)
    for i in range(14):
        x = -200 + 180 * i
        lz.trazo(np.array([[x, SY + 120], [x + 20 * math.sin(i), SY + 190], [x - 12, SY + 250]]), (110, 76, 60), 5.0, temblor=0.0, capa=1)
    for (yy, txt) in ((SY + 50, "cables y asfalto"), (SY + 215, "relleno colonial"), (SY + 560, "lodo del antiguo lago")):
        P.pastilla(lz, 230, yy, txt, px=26)


def _piedra_luna(lz, x, y, r, t, brillo=0.0):''')
rep("        _capas_terreno(lz, 1.0)\n", "        _capas_terreno(lz, 1.0)\n        _detalles_subsuelo(lz, t)\n")
# contorno discontinuo del templo enterrado
rep("        # zanja\n", '''        if cubre > 0.01 and t > T_ROCA + 1.2:
            u_ = smooth(prog(t, T_ROCA + 1.2, T_ROCA + 2.6)) * cubre
            base = np.array([[1080, SY + 720], [1620, SY + 720], [1560, SY + 500], [1500, SY + 500], [1440, SY + 500], [1380, SY + 500], [1320, SY + 500], [1260, SY + 500], [1200, SY + 500], [1140, SY + 500], [1080, SY + 720]])
            P.discontinua(lz, np.array([[1080, SY + 720], [1620, SY + 720], [1540, SY + 500], [1160, SY + 500], [1080, SY + 720]]), (255, 230, 150), ancho=5.0, largo=20, hueco=14, fase=-t * 20, frac=u_, capa=2)
            P.pastilla(lz, 1350, SY + 440, "el Templo Mayor, dos metros más abajo", px=30, alfa=u_) if False else P.pastilla(lz, 1350, SY + 440, "el Templo Mayor sigue enterrado", px=30, alfa=u_)
        # zanja
''')
# gráfica: la cifra de aliados va encima de la barra
rep('cifra(lz, t, ta, "1 000 a 4 000", x0 + 1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6) + 230, y, px=60, col=BLANCO)', 'pass')
open("s_d.py", "w", encoding="utf-8").write(sd)

sc = open("s_c.py", encoding="utf-8").read()
a = 'cifra(lz, t, ta, "1 000 a 4 000", x0 + 1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6) + 230, y, px=60, col=BLANCO)'
b = 'cifra(lz, t, ta, "1 000 a 4 000", x0 + (1000 * k + 3000 * k * max(0, (u - 0.4) / 0.6)) / 2, y - 78, px=58, col=BLANCO)'
if a in sc:
    sc = sc.replace(a, b)
else:
    print("gráfica: no encontrado")
open("s_c.py", "w", encoding="utf-8").write(sc)

g = open("guion.py", encoding="utf-8").read()
g = g.replace('ESTILO_VISUAL = "documental"', 'ESTILO_VISUAL = "kurzgesagt"')
g = g.replace("SUBTITULOS = False          # el estilo dibuja su propio texto sincronizado; el .srt se genera igual\n", "")
open("guion.py", "w", encoding="utf-8").write(g)
print("ok", "SUBTITULOS" in g, 'kurzgesagt' in g)
