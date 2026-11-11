# Cuadro con rejilla FINA (cada 0,05; etiquetas cada 0,1 en los 4 bordes) a 1280 px: python rejilla2.py <n> <t> ...
# → previews/cuadros/r_j<n>_<t>.jpg. Las coordenadas se leen SIEMPRE dentro de UN cuadro (nunca en hojas 2×2: 28-oct-2026).
import os, sys
import cv2
D = os.path.dirname(os.path.abspath(__file__))
n, ts = sys.argv[1], [float(x) for x in sys.argv[2:]]
cap = cv2.VideoCapture(os.path.join(D, "medios", "_fuente", f"{n}.mp4"))
for t in ts:
    cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
    ok, im = cap.read()
    im = cv2.resize(im, (1280, 720))
    for k in range(1, 20):
        f = k / 20
        col = (0, 255, 255) if k % 2 == 0 else (0, 160, 160)
        g = 1 if k % 2 else 1
        cv2.line(im, (int(f * 1280), 0), (int(f * 1280), 720), col, g)
        cv2.line(im, (0, int(f * 720)), (1280, int(f * 720)), col, g)
        if k % 2 == 0:
            for (x, y) in ((int(f * 1280) + 2, 14), (int(f * 1280) + 2, 714)):
                cv2.putText(im, f"{f:.1f}", (x, y), 0, .42, (0, 255, 255), 1)
            for (x, y) in ((2, int(f * 720) - 3), (1250, int(f * 720) - 3)):
                cv2.putText(im, f"{f:.1f}", (x, y), 0, .42, (0, 255, 255), 1)
    cv2.putText(im, f"{n} t={t}", (1100, 40), 0, .7, (255, 255, 255), 2)
    cv2.imwrite(os.path.join(D, "previews", "cuadros", f"r_{n}_{t:g}.jpg"), im)

