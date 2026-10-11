import cv2, numpy as np
import escenas as E
import mapa as M
t = 12.0
m = E.Mundo(E.TL["escenas"][0], 0)
w = E.R.peso_am(t)
st = E.estado_cam(t, w)
fs = E.B.fase(t)
for nom in ("eu", "am"):
    img, cam, formas = E.fondo_rejilla(nom, st, t, fs)
    big = (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    cv2.imwrite(f"previews/_dbg/capa_{nom}.jpg", big[150:350, 650:1600], [cv2.IMWRITE_JPEG_QUALITY, 92])
    # fila con la línea: ¿hay una fila de píxeles con valor distinto?
    f = img[:, 800:1400].mean(axis=(1, 2))
    d = np.abs(np.diff(f, 2))
    ys = np.argsort(d)[-4:]
    print(nom, "filas raras:", sorted(int(y) for y in ys), "w=", round(w, 2))
