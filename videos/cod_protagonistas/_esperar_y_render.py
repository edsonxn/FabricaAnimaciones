# Espera a que no haya NINGÚN render de fab.py activo (progreso_render.json tocado hace < 4 min) y lanza video + final de este video.
import glob, json, subprocess, sys, time, os
os.chdir(r"C:\FabricaAnimaciones")
def activos():
    out = []
    for f in glob.glob("videos/*/salida/progreso_render.json"):
        if "cod_protagonistas" in f: continue
        try:
            if time.time() - os.path.getmtime(f) < 240: out.append(f)
        except OSError: pass
    return out
while True:
    a = activos()
    if not a: break
    print(time.strftime("%H:%M"), "esperando:", a, flush=True); time.sleep(60)
time.sleep(90)
if activos(): sys.exit("otro render arrancó; relanzar")
print(time.strftime("%H:%M"), "VIDEO", flush=True)
r = subprocess.run([sys.executable, "fab.py", "cod_protagonistas", "video"])
print("FIN video", r.returncode, flush=True)
if r.returncode == 0:
    r = subprocess.run([sys.executable, "fab.py", "cod_protagonistas", "final"])
    print("FIN final", r.returncode, flush=True)
