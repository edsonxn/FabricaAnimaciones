# -*- coding: utf-8 -*-
"""Video de apoyo (Pexels) del documental: descarga los nuevos y reutiliza los del video voynich. Créditos en clips/creditos_clips.json."""
import json
import os
import shutil
import sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import videos_stock as V

AQUI = os.path.dirname(os.path.abspath(__file__))
D = os.path.join(AQUI, "clips")
VOY = os.path.join(AQUI, "..", "voynich", "clips")
os.makedirs(D, exist_ok=True)
NUEVOS = {
    "lluvia_noche": ("pexels", 1470714), "gotas": ("pexels", 4420319), "lago": ("pexels", 27926983),
    "antorcha": ("pexels", 4765799), "antorcha2": ("pexels", 4423711), "joyas": ("pexels", 8706305),
    "joyas2": ("pexels", 6208744), "excavadora": ("pexels", 10932285), "cdmx": ("pexels", 34849951), "cdmx2": ("pexels", 11690475),
}
REUSO = ["vela", "vela2", "pluma", "escribir", "polvo", "polvo2", "biblioteca", "monedas", "monedas2", "mapa_vela", "mapa_lupa",
         "reloj_bolsillo", "tinta", "humo", "papel_fuego", "carta", "carta_lupa", "paginas1", "paginas2", "pagina_cerca", "proyector"]

cred_voy = json.load(open(os.path.join(VOY, "creditos_clips.json"), encoding="utf-8"))
for n in REUSO:
    dst = os.path.join(D, n + ".mp4")
    if not os.path.exists(dst):
        shutil.copy(os.path.join(VOY, n + ".mp4"), dst)


def uno(item):
    nombre, (fuente, vid) = item
    ruta = os.path.join(D, nombre + ".mp4")
    if os.path.exists(ruta) and os.path.getsize(ruta) > 100000:
        return nombre, "ya"
    try:
        v = V.buscar_id(fuente, vid)[0]
        f = V.descargar(v, ruta)
        V.anotar(D, nombre, v, f)
        return nombre, f"{f['w']}x{f['h']} {os.path.getsize(ruta) // 1024} KB"
    except Exception as e:
        return nombre, f"FALLO {e}"


with ThreadPoolExecutor(4) as ex:
    for n, r in ex.map(uno, NUEVOS.items()):
        print(n, r, flush=True)

# créditos de los reutilizados
ruta_c = os.path.join(D, "creditos_clips.json")
cred = json.load(open(ruta_c, encoding="utf-8")) if os.path.exists(ruta_c) else {}
for n in REUSO:
    if n in cred_voy and n not in cred:
        cred[n] = cred_voy[n]
json.dump(cred, open(ruta_c, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("créditos:", len(cred))
