# -*- coding: utf-8 -*-
o = open('objetos.py', encoding='utf-8').read()
a = o.index("@lru_cache(maxsize=None)\ndef nube():")
b = o.index("@lru_cache(maxsize=None)\ndef sol(r=76):")
nuevo = '''def _contorno_nube(circulos, base, x0, x1, centro):
    """Contorno cerrado de una nube: arcos superiores (ordenados de derecha a izquierda por encima) + base ondulada."""
    pts, _ = union_circulos(circulos, base, centro)
    th = np.arctan2(-(pts[:, 1] - centro[1]), pts[:, 0] - centro[0])
    th = np.where(th < -math.pi / 2, th + 2 * math.pi, th)
    pts = pts[np.argsort(th)]
    xs = np.linspace(x0, x1, 26)
    bl = np.stack([xs, base + 4 * np.sin(xs / 60)], 1)
    return np.vstack([pts, bl, pts[:1]])


@lru_cache(maxsize=None)
def nube():
    circulos = [(-190, 30, 85, 84), (-85, -35, 105, -8), (45, -55, 120, -8), (175, -5, 95, 50), (250, 55, 55, 80)]
    P = _contorno_nube(circulos, 108, -272, 302, (20, 20))
    det = [arco_(-130, 20, 40, 200, 290, 10), arco_(30, -10, 52, 210, 300, 10), arco_(190, 30, 34, 200, 290, 10)]
    return Dib([T(P, 6.0, peso=1.0), R(P, AZUL_CL, peso=0.9, sp=12)] + [T(d, 3.6, peso=0.08) for d in det])


'''
o = o[:a] + nuevo + o[b:]
a = o.index("@lru_cache(maxsize=None)\ndef soplo():")
o = o[:a] + '''@lru_cache(maxsize=None)
def soplo():
    """Nubecita de aliento (la gota se va en él)."""
    circulos = [(-70, 10, 50, 30), (0, -30, 62, -8), (72, 0, 52, 30)]
    P = _contorno_nube(circulos, 54, -118, 120, (0, 10))
    return Dib([T(P, 5.0, peso=0.6), R(P, (222, 236, 248), peso=0.4, sp=10)])
'''
open('objetos.py', 'w', encoding='utf-8').write(o)
