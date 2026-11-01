"""Mapea las imágenes <uuid>.jpg que baja la extensión (Descargas, desde las 14:49 del 12-oct) a medios/scene-NNN.jpg
en orden de descarga, quitando duplicados por contenido. Uso (desde la carpeta del video):
  python _ingerir.py            # simulación: muestra el mapa
  python _ingerir.py --copiar   # copia a medios/ (empieza en scene-020; --desde N para otro inicio)
"""
import glob, hashlib, os, shutil, sys, time

DESC = os.path.join(os.path.expanduser("~"), "Downloads")
DESDE = time.mktime((2026, 10, 12, 14, 49, 0, 0, 0, -1))
ini = 20
if "--desde" in sys.argv:
    ini = int(sys.argv[sys.argv.index("--desde") + 1])

fs = [f for f in glob.glob(os.path.join(DESC, "*.jpg")) + glob.glob(os.path.join(DESC, "*.png"))
      if os.path.getmtime(f) >= DESDE and os.path.getsize(f) > 20000]
fs.sort(key=os.path.getmtime)
vistos, util = {}, []
for f in fs:
    h = hashlib.md5(open(f, "rb").read()).hexdigest()
    if h in vistos:
        continue
    vistos[h] = f
    util.append(f)
print(f"{len(fs)} archivos, {len(util)} distintos")
for k, f in enumerate(util):
    sid = f"scene-{ini + k:03d}"
    print(sid, os.path.basename(f), time.strftime("%H:%M:%S", time.localtime(os.path.getmtime(f))))
    if "--copiar" in sys.argv:
        for viejo in glob.glob(os.path.join("medios", sid + ".*")):
            os.remove(viejo)
        shutil.copy2(f, os.path.join("medios", sid + os.path.splitext(f)[1].lower()))
