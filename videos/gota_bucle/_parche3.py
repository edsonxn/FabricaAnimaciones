# -*- coding: utf-8 -*-
o = open('objetos.py', encoding='utf-8').read()
o = o.replace("""    ang = np.arctan2(pts[:, 1] - 20, pts[:, 0] - 20)
    pts = pts[np.argsort(ang)]
    pts = pts[np.argsort(pts[:, 0], kind="stable")] if False else pts
    P = np.vstack([pts, bl[::-1], pts[:1]])
    det =""", """    P = np.vstack([pts, bl])
    ang = np.arctan2(P[:, 1] - 20, P[:, 0] - 20)
    P = P[np.argsort(ang)]
    P = np.vstack([P, P[:1]])
    det =""")
o = o.replace("""    ang = np.arctan2(pts[:, 1] - 10, pts[:, 0])
    pts = pts[np.argsort(ang)]
    P = np.vstack([pts, bl[::-1], pts[:1]])
    return Dib([T(P, 5.0""", """    P = np.vstack([pts, bl])
    ang = np.arctan2(P[:, 1] - 10, P[:, 0])
    P = P[np.argsort(ang)]
    P = np.vstack([P, P[:1]])
    return Dib([T(P, 5.0""")
o = o.replace("""    pelo = curva([(-160, -60), (-120, -150), (-30, -190), (70, -172), (150, -100), (170, -40)], 8)""",
              """    ext = arco_(0, 0, 180, 190, 350, 22)
    inte = arco_(0, -14, 138, 350, 190, 22)
    pelo = ext
    pelo_pol = np.vstack([ext, inte])""")
o = o.replace("""T(pelo, 6, peso=0.3), R(np.vstack([pelo, [(170, -120), (-160, -140)]]), (94, 66, 52), peso=0.3, sp=8),""",
              """T(pelo, 6, peso=0.3), R(pelo_pol, (110, 78, 58), peso=0.3, sp=8),""")
open('objetos.py', 'w', encoding='utf-8').write(o)
