"""3.ª pasada (28-oct): «mañana» → «hoy» en la voz. Rehace solo los tramos con voz nueva (0-130, 260-390, 691.5-774.55) en
piezas cortas, 4 a la vez, y concatena con las piezas que no cambian -> salida/video_sin_audio.mp4."""
import os
import subprocess
import time
from concurrent.futures import ThreadPoolExecutor

R = r"C:\FabricaAnimaciones"
V = os.path.join(R, "videos", "ig_lyon_worlds")
NUEVAS = [("hoy_0", 0, 43.33), ("hoy_1", 43.33, 86.67), ("hoy_2", 86.67, 130),
          ("hoy_3", 260, 303.33), ("hoy_4", 303.33, 346.67), ("hoy_5", 346.67, 390),
          ("hoy_6", 691.5, 733), ("hoy_7", 733, 774.55)]
ORDEN = ["hoy_0", "hoy_1", "hoy_2", "par_1", "hoy_3", "hoy_4", "hoy_5", "par_3",
         "fix_0", "fix_1", "fix_2", "fix_3", "hoy_6", "hoy_7"]
LOG = os.path.join(V, "render_par")
os.makedirs(LOG, exist_ok=True)
t0 = time.time()


def uno(p):
    n, a, b = p
    with open(os.path.join(LOG, f"{n}.log"), "w", encoding="utf-8") as f:
        r = subprocess.run(["python", "fab.py", "ig_lyon_worlds", "video", "--tramo", f"{a}-{b}", "--salida", f"salida/{n}.mp4"],
                           cwd=R, stdout=f, stderr=subprocess.STDOUT)
    print(f"{n}: código {r.returncode} · {time.time() - t0:.0f} s", flush=True)
    return r.returncode


with ThreadPoolExecutor(4) as ex:
    codigos = list(ex.map(uno, NUEVAS))
if any(codigos):
    raise SystemExit("falló algún tramo: no se concatena")
lista = os.path.join(V, "salida", "lista3.txt")
with open(lista, "w", encoding="utf-8") as fl:
    for n in ORDEN:
        fl.write(f"file '{n}.mp4'\n")
r = subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy",
                    os.path.join(V, "salida", "video_sin_audio.mp4")], capture_output=True, text=True)
print("concat:", r.returncode, r.stderr[-400:], f"· total {time.time() - t0:.0f} s")
