import numpy as np
import mapa as M
M.cargar()
for nom in ("am", "eu"):
    rej = M.REJ[nom]
    P = np.asarray(rej.r_pts, float)
    X, Y = rej.proj(P[:, 0], P[:, 1])
    cut = list(rej.r_cortes)
    mal = []
    for k, (a, b) in enumerate(zip(cut[:-1], cut[1:])):
        if b - a < 2:
            continue
        dx = np.abs(np.diff(X[a:b]))
        j = int(np.argmax(dx))
        if dx[j] > rej.FW / 2:
            mal.append((k, round(float(P[a + j, 0]), 2), round(float(P[a + j + 1, 0]), 2), round(float(P[a + j, 1]), 2), int(dx[j])))
    print(nom, "FW", rej.FW, "ríos con salto > FW/2:", mal, "total", len(mal))
