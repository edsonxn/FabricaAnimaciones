# Igual que marcador completo (kills, oro, reloj) con cada cuadro con ffmpeg -ss exacto (cv2 salta mal en H.264): python hud_ff.py <fuente> <salida> t1 t2 ...
import subprocess, cv2, os, sys
import numpy as np
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n, sal, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
src = os.path.join(D, "medios", "_fuente", n + ".mp4")
tmp = os.path.join(D, "investigacion", f"_tmp_{n}.png")
fil = []
for t in ts:
    subprocess.run([FF, "-loglevel", "error", "-y", "-i", src, "-ss", t, "-frames:v", "1", tmp], check=False)
    f = cv2.imread(tmp)
    H, W = f.shape[:2]
    c = f[int(H * .0):int(H * .098), int(W * .36):int(W * .64)]
    c = cv2.resize(c, (640, int(c.shape[0] * 640 / c.shape[1])))
    lab = np.zeros((c.shape[0], 120, 3), np.uint8)
    cv2.putText(lab, t, (4, c.shape[0] - 10), 0, .8, (0, 255, 255), 2)
    fil.append(np.hstack([lab, c]))
os.remove(tmp)
cv2.imwrite(os.path.join(D, "previews", "cuadros", f"{sal}.jpg"), np.vstack(fil), [cv2.IMWRITE_JPEG_QUALITY, 85])
