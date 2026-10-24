# -*- coding: utf-8 -*-
"""Reparación del 24-oct-2026: un `bajar --rehacer` sin ids (stdin comido por un bucle) movió los 357 clips a _respaldo, rehízo 7 y
se cayó por disco lleno; fuentes.json quedó con 7 entradas. Aquí: (1) se restauran los 7 clips aprobados desde _respaldo (sufijos
1792858089/1792858090 = estado aprobado antes de esa vuelta), (2) se reconstruye fuentes.json con la ÚLTIMA línea «ok» de cada beat en
los logs buenos (bajar_log, rehacer1_log y los 4 primeros de rehacer2_log), (3) _rechazados sin el video final de cada beat."""
import glob
import json
import os
import re
import shutil

LOGS = r"E:\FabricaAnimaciones\videos\wow_100_curiosidades_tbc_wotlk"
ROTOS = ["scene-001", "scene-002", "scene-003", "scene-004", "scene-006", "scene-008", "scene-009"]
SUF = ("1792858089", "1792858090")

# (1) clips
for sid in ROTOS:
    cands = [f for f in glob.glob(f"medios/_respaldo/{sid}_*.mp4") if f.rsplit("_", 1)[1][:-4] in SUF]
    assert cands, sid
    src = max(cands, key=os.path.getmtime)
    shutil.copy2(src, f"medios/{sid}.mp4")
    print("restaurado", sid, "<-", os.path.basename(src), os.path.getsize(src))
# comprobación: un clip no tocado debe medir igual que su respaldo
for sid in ("scene-020", "scene-200", "scene-357"):
    r = [f for f in glob.glob(f"medios/_respaldo/{sid}_*.mp4") if f.rsplit("_", 1)[1][:-4] in SUF]
    print(sid, "igual al respaldo:", os.path.getsize(f"medios/{sid}.mp4") == os.path.getsize(r[0]))

# (2) fuentes
pat = re.compile(r"^\s*(scene-\d{3}) ok\s+(\S+)@(\d+)s\s+(.*?) · (.*)$")
fu_nuevo = {}
def leer(nombre, solo=None):
    for ln in open(os.path.join(LOGS, nombre), encoding="utf-8", errors="replace"):
        m = pat.match(ln.rstrip("\n"))
        if m and (solo is None or m.group(1) in solo):
            fu_nuevo[m.group(1)] = dict(video=m.group(2), desde=float(m.group(3)), titulo=m.group(5).strip(), canal=m.group(4).strip())
leer("bajar_log.txt")
leer("rehacer1_log.txt")
leer("rehacer2_log.txt", solo={"scene-011", "scene-012", "scene-015", "scene-018"})
fu = json.load(open("fuentes.json", encoding="utf-8"))
bq = json.load(open("busquedas.json", encoding="utf-8"))
faltan = [f"scene-{n:03d}" for n in range(1, 358) if f"scene-{n:03d}" not in fu_nuevo]
print("beats sin fuente en los logs:", faltan)
for k, v in fu_nuevo.items():
    v["q"] = bq[k][0] if isinstance(bq[k], list) else bq[k]
rech = fu.get("_rechazados", {})
for k, v in fu_nuevo.items():
    if k in rech:
        rech[k] = [x for x in rech[k] if x != v["video"]]
salida = {"_busquedas": fu.get("_busquedas", {}), "_rechazados": rech}
salida.update(fu_nuevo)
json.dump(salida, open("fuentes.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("fuentes.json:", len(fu_nuevo), "beats;", sum(len(v) for v in rech.values()), "rechazados en total")
