# Prueba del mapa de Tequisquiapan (VERTICAL 1080x1920): 6 cuadros → previews/mapa_t1..t6.jpg + hoja 3x2 previews/mapa_test.jpg
# (con --puntos: mapa_t*_puntos.jpg y mapa_test_puntos.jpg, con ciudades y rutas)
# uso (desde esta carpeta): PYTHONPATH="<esta carpeta>;C:\FabricaAnimaciones\nucleo" python _mapa_test.py [--puntos]
# Solo usa mapa.py (no core/escenas). Fuerza FORMATO vertical aunque guion.py aún no lo diga.
import sys
import types

if "guion" not in sys.modules:
    try:
        import guion as _g
        if getattr(_g, "FORMATO", "") != "vertical":
            raise ImportError
    except Exception:
        sys.modules["guion"] = types.SimpleNamespace(FORMATO="vertical")

import cv2
import numpy as np

import mapa as M
from motor import H, W

assert (W, H) == (1080, 1920), (W, H)
M.cargar()
M.usar("mx")
PUNTOS = "--puntos" in sys.argv          # dibuja ciudades y rutas (solo para comprobar posiciones)
SUF = "_puntos" if PUNTOS else ""
EDOS = ("edo_queretaro", "edo_guanajuato", "edo_hidalgo", "edo_mexico", "edo_cdmx", "edo_san_luis_potosi", "edo_michoacan")
TOMAS = [
    ("t1_caja", (-99.95, 20.76, 0.77), [], ["camino_real", "tren"]),
    ("t2_estado", (-99.81, 20.80, 1.02), ["edo_queretaro"], ["camino_real", "ruta_sierra"]),
    ("t3_zona", (-99.92, 20.57, 3.2), ["municipio_tequis"], ["ruta_turista", "ruta_queso_vino"]),
    ("t4_pueblo", (-99.889, 20.530, 7.0), ["mancha_tequis"], ["tequis_sjr", "tequis_bernal"]),
    ("t5_pueblos", (-99.95, 20.76, 0.80), ["otomies", "pames", "jonaces", "purepechas", "mexicas"], []),
    ("t6_sierra", (-99.62, 21.05, 1.9), ["sierra_gorda", "semidesierto"], ["ruta_sierra"]),
]
ROT_EDOS = (("QUERETARO", (-99.95, 20.95)), ("GUANAJUATO", (-100.75, 21.15)), ("HIDALGO", (-99.15, 20.35)),
            ("SAN LUIS POTOSI", (-99.90, 22.15)), ("MEXICO", (-99.75, 19.65)), ("MICHOACAN", (-100.85, 19.55)))
tiles = []
for nombre, (lon, lat, z), capas, rutas in TOMAS:
    cam = M.Cam(lon, lat, z)
    img, base = M.pintar_base(cam, 0)
    if nombre == "t1_caja":                # estados con su color, para comprobar las fronteras
        for c in EDOS:
            M.pintar(img, cam.proyectar(M.CAMPOS[c]), M.COL[c], 0.45, 0, luz=base.luz)
    if nombre == "t3_zona":
        M.pintar(img, cam.proyectar(M.CAMPOS["edo_queretaro"]), M.COL["edo_queretaro"], 0.30, 0, luz=base.luz)
    for c in capas:
        M.pintar(img, cam.proyectar(M.CAMPOS[c]), M.COL[c], 0.8 if nombre != "t4_pueblo" else 0.5, 0, luz=base.luz)
    M.pintar_rios(img, cam, base)
    if nombre == "t1_caja":
        for n, (lo, la) in ROT_EDOS:
            M.rotulo_mapa(img, n, cam, lo, la, 34, 0.5)
    out = (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    if PUNTOS:
        for r in rutas:
            P = np.rint(cam.pant_pts(M.RUTAS[r])).astype(np.int32)
            cv2.polylines(out, [P], False, (40, 40, 160), 3, cv2.LINE_AA)
        for k, (lo, la) in M.CIUDADES.items():
            x, y = cam.pant(lo, la)
            if 0 <= x < W and 0 <= y < H:
                cv2.circle(out, (int(x), int(y)), 6, (30, 30, 30), -1)
                cv2.putText(out, k, (int(x) + 8, int(y) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.imwrite(f"previews/mapa_{nombre}{SUF}.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 90])
    tiles.append(cv2.resize(out, (W // 3, H // 3), interpolation=cv2.INTER_AREA))
cv2.imwrite(f"previews/mapa_test{SUF}.jpg", np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print(f"ok: previews/mapa_t1_caja{SUF}.jpg … mapa_t6_sierra{SUF}.jpg y previews/mapa_test{SUF}.jpg")
