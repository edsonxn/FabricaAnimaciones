# Cuadro(s) sueltos del VOD SIN bajarlo: python blte_cuadro.py <vid> <ancho> t1 t2 ... -> previews/cuadros/v_<vid>_<t>.jpg
# Con mosaico: python blte_cuadro.py <vid> <ancho> --hoja t1 t2 ... -> una hoja por llamada (solo para localizar, nunca para medir).
import os, subprocess, sys
from concurrent.futures import ThreadPoolExecutor
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sal = os.path.join(D, "previews", "cuadros"); os.makedirs(sal, exist_ok=True)
vid, ancho = sys.argv[1], int(sys.argv[2])
args = sys.argv[3:]
hoja = "--hoja" in args
ts = [float(x) for x in args if x != "--hoja"]
cache = os.path.join(D, "investigacion", "blte_subs", vid + ".url")
def bajar_url():
    u = subprocess.run(["yt-dlp", "-g", "-f", "299/bv*[height<=1080][ext=mp4]", f"https://youtu.be/{vid}"],
                       capture_output=True, text=True).stdout.split()[0]
    open(cache, "w").write(u)
    return u
url = open(cache).read().strip() if os.path.exists(cache) else bajar_url()
def uno(t):
    p = os.path.join(sal, f"v_{vid}_{t:g}.jpg")
    if os.path.exists(p): os.remove(p)
    r = subprocess.run([FF, "-loglevel", "quiet", "-y", "-ss", str(t), "-i", url, "-frames:v", "1", "-vf", f"scale={ancho}:-2", "-q:v", "3", p])
    return p if os.path.exists(p) else None
def lote(ts):
    with ThreadPoolExecutor(4) as ex:
        return list(ex.map(uno, ts))
ps = lote(ts)
for _ in range(5):
    if all(ps): break
    url = bajar_url()
    ps = lote(ts)
assert all(ps), "403 persistente"
if hoja:
    import cv2, numpy as np
    ims = [cv2.imread(p) for p in ps]
    cols = 3
    filas = [np.hstack(ims[i:i + cols] + [np.zeros_like(ims[0])] * (cols - len(ims[i:i + cols]))) for i in range(0, len(ims), cols)]
    p = os.path.join(sal, f"h_{vid}_{ts[0]:g}.jpg")
    cv2.imwrite(p, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(p)
else:
    print("\n".join(ps))
