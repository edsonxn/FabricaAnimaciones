# Tira con el marcador superior (reloj, oro, kills) y el centro del banner de varios cuadros de un VOD, leyendo sin bajar:
# python lotl_reloj.py <vid> <salida> t1 t2 ...  -> ../previews/cuadros/lotl_<salida>.jpg (una fila por cuadro)
import subprocess, sys, os
import cv2
import numpy as np
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.abspath(__file__))
vid, sal, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
url = open(os.path.join(D, f"lotl_url_{vid}.txt")).read().strip()
tmp = os.environ.get("TMP_LOTL", os.path.join(D, "_lotl_tmp.jpg"))
fil = []
for t in ts:
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", url, "-frames:v", "1", "-q:v", "2", tmp], check=False)
    f = cv2.imread(tmp)
    if f is None:
        print("sin cuadro", t); continue
    H, W = f.shape[:2]
    c = f[0:int(H * .26), int(W * .25):int(W * .76)]
    c = cv2.resize(c, (960, int(c.shape[0] * 960 / c.shape[1])))
    cv2.putText(c, t, (4, 20), 0, .6, (0, 255, 255), 2)
    fil.append(c)
cv2.imwrite(os.path.join(D, "..", "previews", "cuadros", f"lotl_{sal}.jpg"), np.vstack(fil), [cv2.IMWRITE_JPEG_QUALITY, 85])
if os.path.exists(tmp):
    os.remove(tmp)
