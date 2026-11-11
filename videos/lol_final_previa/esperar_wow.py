# Espera a que ARRANQUE el render de Warcraft (procesos con cwd videos/wow_* o «wow_» en la línea de un `video`) y luego a que TERMINE.
import os, sys, time
import psutil


def wow():
    for p in psutil.process_iter(["name", "cmdline"]):
        c = " ".join(p.info["cmdline"] or []).lower()
        try:
            cw = os.path.basename(p.cwd()).lower()
        except Exception:
            cw = ""
        if (p.info["name"] or "").lower().startswith(("python", "ffmpeg")) and ("wow_" in cw or "wow_" in c) and \
                ("video" in c or "render" in c or "rawvideo" in c):
            return True
    return False


t0 = time.time()
while not wow():
    if time.time() - t0 > 3 * 3600:
        print("el render de Warcraft no arrancó en 3 h"); sys.exit(2)
    time.sleep(120)
print(time.strftime("%H:%M"), "arrancó el render de Warcraft", flush=True)
libre = 0
while libre < 3:                      # 3 lecturas seguidas sin él (6 min): terminó de verdad
    libre = libre + 1 if not wow() else 0
    time.sleep(120)
print(time.strftime("%H:%M"), "terminó el render de Warcraft", flush=True)
