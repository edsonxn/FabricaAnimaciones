# -*- coding: utf-8 -*-
"""Parche: éxodo de familias en la calle del pueblo arruinado (mundos_b.PuebloRuina) y cámara más cercana en t02."""
s = open('mundos_b.py', encoding='utf-8').read()
a = s.index("class PuebloRuina:")
nuevo = '''class PuebloRuina:
    """Pueblo de calle principal con casas en venta y tapiadas, un éxodo de familias con bultos y carretas cargadas, y el campo de tierra donde brotan las plantas del descontento."""

    def __init__(self):
        self._est = None

    def suelo(self, lz, iso, t):
        I.isla(lz, iso, -160, -120, 520, 380, color_top=(150, 168, 120), t=t, seed=9, esp=36)
        DC.parches(lz, iso, -160, -120, 520, 380, (150, 168, 120), n=16, var=20, seed=17, alfa=0.55, tam=(40, 90))
        I.suelo_curvo(lz, iso, [(-60, -20), (400, -20), (410, 300), (-60, 310)], (200, 184, 150))
        I.camino(lz, iso, [(-160, 150), (120, 150), (240, 160), (520, 170)], 46, (224, 206, 160), borde=(200, 180, 140))
        I.suelo_rect(lz, iso, 40, 200, 260, 100, (150, 112, 84))
        for k in range(6):
            I.suelo_rect(lz, iso, 40, 210 + k * 16, 260, 3.2, (126, 92, 70), alfa=0.8)
        DC.hierba(lz, iso, -160, -120, 520, 380, n=120, seed=6, t=t, color=(128, 150, 100), flores=0.04)

    def objetos(self, t):
        self._t = t
        if self._est is None:
            m = I.Mundo()
            for i, (x, y, w, d) in enumerate(((-40, -10, 70, 50), (46, -10, 64, 50), (126, -10, 70, 50), (210, -10, 60, 50), (290, -10, 70, 50), (-30, 96, 66, 50), (56, 96, 64, 50), (140, 100, 68, 50), (230, 100, 66, 48), (310, 100, 60, 48))):
                A.casa_colonial(m, x, y, w, d, 42 + 6 * (i % 3), muro=[A.CAL, A.OCRE, A.ROSA, A.VERDE_CAL][i % 4], techo=A.TEJA2, eje="x", ventanas=2, seed=i, puerta=(i % 3 != 2))
                # ventanas tapiadas con tablones
                m.add(x, y + d, x + w, y + d + 4, 60, (lambda x, y, w, d: (lambda lz, iso: _tablones(lz, iso, x, y + d, w)))(x, y, w, d), clave=x + y + d + w)
            DC.bosque(m, -150, -110, 510, 370, n=22, seed=41, evitar=((-60, -20, 400, 160), (40, 200, 300, 300), (-160, 120, 520, 190)), t_fn=lambda: self._t, tipos=("arbol", "arbusto", "cipres"),
                      colores=[(110, 150, 100), (96, 136, 96), (128, 156, 104)])
            self._est = m
        m = I.Mundo()
        m.fijos = list(self._est.fijos)
        mu = G.Multitud()
        # éxodo de familias: caminan de izquierda a derecha por la calle, cada una a su ritmo, cargando bultos
        tipos = ("campesino", "campesina", "nino", "campesina", "campesino", "nino", "indigena_f", "mestizo", "nino", "campesina")
        for i in range(10):
            mu.camina([(-170, 148 + 6 * (i % 3)), (130, 152 + 6 * (i % 3)), (260, 162 + 6 * (i % 3)), (540, 172 + 6 * (i % 3))], tipos[i], vel=9 + 1.2 * (i % 4), seed=980 + i, fase=0.04 * i, bucle=True, h=44 if tipos[i] != "nino" else 30,
                    accion="carga" if i % 3 == 0 else None)
        mu.quieto((20, 80), "campesina", dir=(0, 1), seed=990, h=44, accion="habla")
        mu.quieto((30, 86), "nino", dir=(0, 1), seed=991, h=30)
        mu.quieto((166, 86), "campesino", dir=(0, 1), seed=992, h=44)
        mu.dibujar(m, t)
        for k, (fase, bul) in enumerate(((0.10, True), (0.42, True), (0.74, True))):
            m.add(0, 0, 4, 4, 30, (lambda k, fase: (lambda lz, iso: O.carreta(lz, iso, -170 + 710 * ((t * 0.034 + fase) % 1.0), 156 + 4 * k, t, mov=1.0, s=1.35, bultos=True)))(k, fase), fijo=False, clave=300 + k)
        m.add(0, 0, 4, 4, 20, lambda lz, iso: _perro(lz, iso, -170 + 710 * ((t * 0.05 + 0.2) % 1.0), 190, t), fijo=False, clave=330)
        return m


def _tablones(lz, iso, x, y, w):
    """Tablones clavados cruzados sobre la fachada (casa abandonada)."""
    k = iso.z
    for (a, b, c, d) in ((0.2, 14, 0.8, 30), (0.2, 30, 0.8, 14)):
        p0 = iso.P(x + w * a, y, b)
        p1 = iso.P(x + w * c, y, d)
        _tira2(lz, p0, p1, 2.6 * k, (126, 90, 66))
    p0, p1 = iso.P(x + w * 0.5, y, 40), iso.P(x + w * 0.5, y, 8)
    _tira2(lz, p0, p1, 2.4 * k, (110, 78, 58))


def _tira2(lz, p0, p1, ancho, color):
    d = np.array([p1[0] - p0[0], p1[1] - p0[1]], float)
    L = float(np.hypot(*d))
    if L < 1e-6:
        return
    n = np.array([-d[1], d[0]]) / L * ancho / 2
    a, b = np.array([float(p0[0]), float(p0[1])]), np.array([float(p1[0]), float(p1[1])])
    lz.relleno(np.array([a + n, b + n, b - n, a - n]), color)


def _perro(lz, iso, x, y, t):
    sx, sy = iso.P(x, y, 0)
    k = iso.z
    I.sombra_elipse(lz, iso, x + 1, y + 0.6, 6, 3, 0.2)
    ph = t * 9
    for dx, f in ((-5, 0.0), (-2, math.pi), (4, math.pi), (7, 0.0)):
        lz.relleno(rect_red(sx + (dx - 0.8) * k + math.sin(ph + f) * 1.4 * k, sy - 4.5 * k, 1.6 * k, 4.5 * k, 0.5 * k), tint((120, 86, 62)))
    lz.relleno(elipse(sx, sy - 6 * k, 8 * k, 3.6 * k, 0, 12), tint((170, 124, 86)))
    lz.relleno(circulo(sx + 8.5 * k, sy - 8 * k, 3 * k, 8), tint((170, 124, 86)))
    lz.relleno(np.array([[sx + 9 * k, sy - 11 * k], [sx + 11 * k, sy - 14.5 * k], [sx + 12 * k, sy - 10 * k]]), tint((120, 86, 62)))
    lz.relleno(np.array([[sx - 8 * k, sy - 7 * k], [sx - 12 * k, sy - 11 * k + math.sin(t * 12) * 2 * k], [sx - 9 * k, sy - 5 * k]]), tint((170, 124, 86)))
'''
s = s[:a] + nuevo
s = s.replace("from kz_iso import tint\n", "") if False else s
if "from kz_iso import tint" not in s:
    s = s.replace("import kz_iso as I\n", "import kz_iso as I\nfrom kz_iso import tint\n", 1)
open('mundos_b.py', 'w', encoding='utf-8').write(s)

# cámara y rótulos de la ruina en t02
t = open('t02.py', encoding='utf-8').read()
a = t.index("def cam_ruina(t):")
b = t.index("@shot(T_RUINA")
t = t[:a] + '''def cam_ruina(t):
    return K(t, [(T_RUINA, (-20, 140, 30, 3.0)), (t_fam, (60, 150, 30, 3.3)), (t_ruina, (170, 150, 30, 3.1)), (t_desc - 0.5, (230, 170, 20, 2.7)), (t_desc + 0.7, (180, 250, 0, 2.7)), (T1(E2) - 0.2, (185, 255, 0, 2.2))])


''' + t[b:]
open('t02.py', 'w', encoding='utf-8').write(t)
print('ok')
