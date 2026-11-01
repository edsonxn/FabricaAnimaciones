# Saca cuadros sueltos de un VOD sin bajarlo: python lotl_cuadro.py <vid> <etiqueta> t1 t2 ... -> ../previews/cuadros/lotl_<etiqueta>_<t>.jpg
# La URL directa (1080p sin audio) se guarda en lotl_url_<vid>.txt para no repetir yt-dlp. Si t lleva ":" se toma HUD+K con env K.
import subprocess, sys, os, time
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.abspath(__file__))
vid, et, ts = sys.argv[1], sys.argv[2], sys.argv[3:]
cache = os.path.join(D, f"lotl_url_{vid}.txt")
if os.path.exists(cache) and time.time() - os.path.getmtime(cache) < 3 * 3600:
    url = open(cache).read().strip()
else:
    url = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=1080][ext=mp4]", f"https://youtu.be/{vid}"], capture_output=True, text=True).stdout.split()[0]
    open(cache, "w").write(url)
W = os.environ.get("ANCHO", "1280")
sal = os.path.join(D, "..", "previews", "cuadros")
os.makedirs(sal, exist_ok=True)
for t in ts:
    out = os.path.join(sal, f"lotl_{et}_{t}.jpg")
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", t, "-i", url, "-frames:v", "1", "-vf", f"scale={W}:-2", "-q:v", "3", out], check=False)
    print(out, os.path.exists(out))
