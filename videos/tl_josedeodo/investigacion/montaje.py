# Junta cuadros en una hoja: python montaje.py <salida.jpg> <cols> <ancho_celda> img1 img2 ...  (rotula cada uno con su nombre)
import sys, cv2, numpy as np, os
out, cols, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
ims = []
for p in sys.argv[4:]:
    im = cv2.imread(p)
    if im is None: continue
    im = cv2.resize(im, (w, int(w * im.shape[0] / im.shape[1])))
    t = os.path.splitext(os.path.basename(p))[0]
    cv2.putText(im, t, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 4)
    cv2.putText(im, t, (5, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
    ims.append(im)
h = max(i.shape[0] for i in ims)
ims = [cv2.copyMakeBorder(i, 0, h - i.shape[0], 0, 0, cv2.BORDER_CONSTANT) for i in ims]
while len(ims) % cols: ims.append(np.zeros_like(ims[0]))
rows = [np.hstack(ims[k:k + cols]) for k in range(0, len(ims), cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 85])
print(out)
