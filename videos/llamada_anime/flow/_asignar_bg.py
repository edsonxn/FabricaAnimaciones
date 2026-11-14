# Asigna cada edición anime (flow/bg_raw/rNN.jpg) a su original de ../llamada_domingo/flow/bg por contenido.
import glob, os, numpy as np
from PIL import Image, ImageFilter
O = sorted(glob.glob('../llamada_domingo/flow/bg/*.jpg'))
def f(p):
    im = Image.open(p).convert('L').filter(ImageFilter.GaussianBlur(6)).resize((48, 27), Image.BOX)
    a = np.asarray(im, np.float32); a = (a - a.mean()) / (a.std() + 1e-6); return a.ravel()
FO = {os.path.basename(p)[:-4]: f(p) for p in O}
R = sorted(glob.glob('flow/bg_raw/*.jpg'))
for p in R:
    v = f(p); sc = sorted(((float(v @ FO[k]) / v.size, k) for k in FO), reverse=True)
    print(os.path.basename(p)[:-4], sc[0][1], round(sc[0][0], 2), sc[1][1], round(sc[1][0], 2))
