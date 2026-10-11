# -*- coding: utf-8 -*-
o = open('objetos.py', encoding='utf-8').read()
o = o.replace("""    xs = np.linspace(x0, x1, 26)
    bl = np.stack([xs, base + 4 * np.sin(xs / 60)], 1)
    return np.vstack([pts, bl, pts[:1]])""", """    xs = np.linspace(pts[-1, 0], pts[0, 0], 26)              # de donde termina el arco izquierdo hasta donde empieza el derecho
    bl = np.stack([xs, base + 4 * np.sin(xs / 60)], 1)
    return np.vstack([pts, bl, pts[:1]])""")
open('objetos.py', 'w', encoding='utf-8').write(o)
e = open('escenas.py', encoding='utf-8').read()
e = e.replace("""        for i in range(15):
            x = 330 + i * 34 + 9 * math.sin(i * 2.1)""", """        mx, my = self.mascota(t)[:2]
        for i in range(15):
            x = 330 + i * 34 + 9 * math.sin(i * 2.1)""")
e = e.replace("""            L = 46 * kk
            if L < 4:
                continue""", """            L = 46 * kk
            if L < 4 or (abs(x - mx) < 78 and abs(y0 + 20 - my) < 130):      # la lluvia no cruza a la gota
                continue""")
open('escenas.py', 'w', encoding='utf-8').write(e)
