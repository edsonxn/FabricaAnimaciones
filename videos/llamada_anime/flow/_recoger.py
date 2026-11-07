# Recoge las descargas del navegador integrado (~/Downloads/*.tmp, completas pero sin renombrar).
# Cada blob lleva al final la marca b"##FAB:<ruta relativa a flow/>##" (la pone la página). La quita y guarda el JPEG.
# python flow/_recoger.py   → mueve lo marcado a flow/<ruta>; deja intacto lo que no lleve marca.
import glob
import os
import re

BASE = os.path.dirname(os.path.abspath(__file__))
DL = os.path.join(os.path.expanduser("~"), "Downloads")
n = 0
for f in sorted(glob.glob(os.path.join(DL, "*.tmp")) + glob.glob(os.path.join(DL, "fab_*"))):
    try:
        d = open(f, "rb").read()
    except OSError:
        continue
    m = re.search(rb"##FAB:([\w./-]+)##$", d[-200:])
    if not m:
        continue
    rel = m.group(1).decode().replace("..", "")
    dst = os.path.join(BASE, rel)
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    open(dst, "wb").write(d[: len(d) - len(m.group(0))])
    try:
        os.remove(f)
    except OSError:
        pass
    n += 1
print(n, "recogidas")
