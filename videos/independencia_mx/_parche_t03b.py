# -*- coding: utf-8 -*-
s = open('t03.py', encoding='utf-8').read()

# 1) países menos teñidos + etiquetas
s = s.replace('''    for nombre, col in (("France", (80, 130, 230)), ("Spain", (255, 210, 70)), ("Portugal", (90, 190, 120)), ("Italy", (150, 130, 230)), ("Germany", (240, 160, 70)), ("Switzerland", (230, 90, 100))):
        MD.pais(lz, cam, nombre, col, alfa=0.28, borde=(255, 236, 160) if nombre in ("Spain", "France") else None, ancho=3.0)''',
'''    for nombre, col in (("France", (80, 130, 230)), ("Spain", (255, 210, 70)), ("Portugal", (90, 190, 120)), ("Italy", (150, 130, 230)), ("Germany", (240, 160, 70)), ("Switzerland", (230, 90, 100))):
        MD.pais(lz, cam, nombre, col, alfa=0.10, borde=col if nombre in ("Spain", "France") else None, ancho=4.0)
    for txt, ll, col in (("FRANCIA", (2.2, 46.4), U.COL["azul"]), ("ESPAÑA", (-4.2, 40.0), U.COL["rojo"]), ("PORTUGAL", (-8.0, 39.6), U.COL["verde"])):
        sx, sy = MP.proy(cam, ll[0], ll[1])
        k_ = U.pop(t, T_INV + 0.2)
        if k_ > 0.01 and cam[2] > 1.2:
            U.llamada(lz, float(sx), float(sy), txt, color=col, px=34, k=k_, cola=None)''')

# 2) ciudades pequeñas con nombre
s = s.replace('''    MD.ciudad(lz, cam, BAYONA, t, T_INV + 0.3, tam=1.2, tipo="puerto", bando=(80, 130, 230), nombre="Bayona", px=26)''',
'''    MD.ciudad(lz, cam, BAYONA, t, T_INV + 0.3, tam=1.2, tipo="puerto", bando=(80, 130, 230), nombre="Bayona", px=26)
    for j, (lug, nom) in enumerate((((-0.88, 41.65), "Zaragoza"), ((-3.70, 42.34), "Burgos"), ((-4.72, 41.65), "Valladolid"), ((-0.58, 44.84), "Burdeos"), ((1.44, 43.60), "Toulouse"), ((2.17, 41.39), "Barcelona"),
                                    ((-5.99, 37.39), "Sevilla"), ((-0.38, 39.47), "Valencia"))):
        MD.pueblo(lz, cam, lug, nom, t, T_INV + 0.4 + 0.08 * j)''')

# 3) tropas más grandes
s = s.replace("MD.ejercito(lz, x + 12 * j, y + 10 * j, 12, bando=(46, 80, 190), t=t + j, s=1.2 * max(1.0, cam[2] ** 0.2), dir=1, estandarte=TRI, semilla=j)",
              "MD.ejercito(lz, x + 26 * j, y + 18 * j, 12, bando=(46, 80, 190), t=t + j, s=2.5 * max(1.0, cam[2] ** 0.2), dir=1, estandarte=TRI, semilla=j)")
open('t03.py', 'w', encoding='utf-8').write(s)

q = r'..\..\nucleo\kz_mapa_dib.py'
m = open(q, encoding='utf-8').read()
if "def pueblo(" not in m:
    m += '''

def pueblo(lz, cam, lugar, nombre, t, t0=0.0, color=(255, 255, 255), px=24, solo_desde=1.2):
    """Punto de población con anillo y nombre pequeño (para dar densidad geográfica sin tapar el mapa). Solo se dibuja con el zoom alto."""
    k = U.pop(t, t0)
    if k <= 0.01 or cam[2] < solo_desde:
        return
    lo, la = CIUDADES[lugar] if isinstance(lugar, str) else lugar
    x, y = M.proy(cam, lo, la)
    if x < -60 or x > W + 60 or y < -40 or y > H + 40:
        return
    with lz.capa(2):
        lz.relleno(circulo(float(x), float(y), 9 * k, 14), (20, 14, 60), alfa=0.35)
        lz.relleno(circulo(float(x), float(y), 7 * k, 14), color)
        lz.relleno(circulo(float(x), float(y), 3.4 * k, 10), (214, 70, 76))
        P.rotulo(lz, float(x), float(y) + 22 * k, nombre, px=int(px * k), k=1.0, color=(255, 255, 255), sombra=0.7, alfa=min(1.0, k))
'''
    open(q, 'w', encoding='utf-8').write(m)
print('ok')
