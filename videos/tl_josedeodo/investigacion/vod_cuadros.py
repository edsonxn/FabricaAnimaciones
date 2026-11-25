# Cuadros del VOD sin bajarlo (H.264 1080p, itag 299/137): python vod_cuadros.py <vid> <salida> <modo> t1 t2 ...
# modo hud = tira del marcador superior (reloj, oro, kills) + centro (banners); modo full = cuadro completo a 640x360 en hoja de 2 columnas
# -> ../previews/cuadros/<salida>.jpg . La URL se guarda 3 h en vod_url_<vid>.txt
import subprocess, sys, os, time
import cv2
import numpy as np
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.abspath(__file__))
vid, sal, modo, ts = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4:]
cache = os.path.join(D, f"vod_url_{vid}.txt")
if os.path.exists(cache) and time.time() - os.path.getmtime(cache) < 3 * 3600:
    url = open(cache).read().strip()
else:
    url = subprocess.run(["yt-dlp", "-g", "-f", "299/137", f"https://youtu.be/{vid}"], capture_output=True, text=True).stdout.split()[0]
    open(cache, "w").write(url)
tmp = os.path.join(D, f"_tmp_{vid}.jpg")
ims = []
for t in ts:
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", url, "-frames:v", "1", "-q:v", "2", tmp], check=False)
    f = cv2.imread(tmp)
    if f is None:
        print("sin cuadro", t); continue
    H, W = f.shape[:2]
    if modo == "hud":
        c = f[0:int(H * .10), int(W * .30):int(W * .70)]
        c = cv2.resize(c, (960, int(c.shape[0] * 960 / c.shape[1])))
        b = f[int(H * .10):int(H * .30), int(W * .30):int(W * .70)]
        b = cv2.resize(b, (960, int(b.shape[0] * 960 / b.shape[1])))
        c = np.vstack([c, b])
    else:
        c = cv2.resize(f, (640, 360))
    cv2.putText(c, t, (4, 20), 0, .6, (0, 0, 0), 4)
    cv2.putText(c, t, (4, 20), 0, .6, (0, 255, 255), 2)
    ims.append(c)
if modo == "full":
    if len(ims) % 2:
        ims.append(np.zeros_like(ims[0]))
    s = np.vstack([np.hstack(ims[i:i + 2]) for i in range(0, len(ims), 2)])
else:
    s = np.vstack(ims)
os.makedirs(os.path.join(D, "..", "previews", "cuadros"), exist_ok=True)
cv2.imwrite(os.path.join(D, "..", "previews", "cuadros", f"{sal}.jpg"), s, [cv2.IMWRITE_JPEG_QUALITY, 85])
if os.path.exists(tmp):
    os.remove(tmp)
print("ok", len(ims))
