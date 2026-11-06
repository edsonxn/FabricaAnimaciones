import sys; sys.path.insert(0, "../../nucleo")
import numpy as np, cv2
import diseccion as D
nombres = ["trapo", "rigido", "leve", "fuerte", "vuela"]
ts = [0, .6, .9, 1.2, 1.6, 2.2, 3, 4.5]
img = np.full((len(nombres)*260, len(ts)*260, 3), 30, np.uint8)
for r, n in enumerate(nombres):
    s = D.escenario(n)
    for c, t in enumerate(ts):
        P = s.en(t); d = s.dato(t)
        ox, oy = c*260 + 130 - P[2,0]*2.2 + 0, r*260 + 230
        cx = c*260+130; off = cx - P[2,0]*2.2 if n=="vuela" else c*260+130
        Q = P*2.2 + [off, oy]
        for a,b,lo,hi in D.HUESOS: cv2.line(img, tuple(Q[a].astype(int)), tuple(Q[b].astype(int)), (220,220,220), 2)
        for i in range(7): cv2.circle(img, tuple(Q[i].astype(int)), max(2,int(D.RAD[i]*2.2*.4)), (80,200,255), -1)
        cv2.line(img, (c*260, oy), (c*260+259, oy), (90,90,90), 1)
        cv2.putText(img, f"{n} t={t} x={P[2,0]:.0f} {'CAE' if d['cae'] else ''}{'PASO' if d['paso'] else ''}", (c*260+4, r*260+16), 0, .38, (255,255,255), 1)
cv2.imwrite("previews/_sim_hoja.jpg", img)
for n in nombres:
    s = D.escenario(n); print(n, "cadera x final", round(s.en(6)[2,0],1), "y", round(s.en(6)[2,1],1), "cae", s.dato(6)["cae"])
