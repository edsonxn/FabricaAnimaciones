# Recorta el marcador de arriba (reloj, kills, oro) de cuadros a 1920: python reloj.py <salida.jpg> img1 img2 ...
import sys, cv2, numpy as np, os
out = sys.argv[1]; filas = []
for p in sys.argv[2:]:
    im = cv2.imread(p)
    if im is None: continue
    if im.shape[1] != 1920: im = cv2.resize(im, (1920, int(1920 * im.shape[0] / im.shape[1])))
    c = im[20:110, 660:1260]
    c = cv2.resize(c, (960, 144))
    lab = np.zeros((144, 160, 3), np.uint8)
    cv2.putText(lab, os.path.splitext(os.path.basename(p))[0].split("_")[-1], (4, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 255), 2)
    filas.append(np.hstack([lab, c]))
cv2.imwrite(out, np.vstack(filas)); print(out)
