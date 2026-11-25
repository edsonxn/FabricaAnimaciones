# Cuadros sueltos de un VOD de YouTube sin descargarlo: python cuadros_url.py <vid> <prefijo> <t1> <t2> ... [--w 1280]
# -> previews/cuadros/<prefijo>_<t>.jpg ; la URL de yt-dlp -g se guarda en investigacion/_url_<vid>.txt (caduca en ~6 h)
import subprocess, sys, os, time
from concurrent.futures import ThreadPoolExecutor
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = sys.argv[1:]
w = 1280
if "--w" in args:
    i = args.index("--w"); w = int(args[i + 1]); del args[i:i + 2]
vid, pre, ts = args[0], args[1], args[2:]
cache = os.path.join(D, "investigacion", f"_url_{vid}.txt")
if not os.path.exists(cache) or time.time() - os.path.getmtime(cache) > 4 * 3600:
    u = subprocess.run(["yt-dlp", "-g", "-f", "bv*[height<=1080][ext=mp4]/bv*[height<=1080]", f"https://youtu.be/{vid}"],
                       capture_output=True, text=True).stdout.split()[0]
    open(cache, "w").write(u)
u = open(cache).read().strip()
out = os.path.join(D, "previews", "cuadros")
os.makedirs(out, exist_ok=True)
def uno(t):
    f = os.path.join(out, f"{pre}_{t}.jpg")
    subprocess.run([FF, "-loglevel", "error", "-y", "-ss", str(t), "-i", u, "-frames:v", "1", "-vf", f"scale={w}:-2", "-q:v", "3", f])
    return f
with ThreadPoolExecutor(6) as ex:
    for f in ex.map(uno, ts):
        print(f)
