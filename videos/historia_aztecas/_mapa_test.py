# Prueba del mapa de los aztecas: 6 cuadros a 1920x1080 → previews/mapa_t1..t6.jpg + hoja 3x2 previews/mapa_test.jpg
# uso (desde esta carpeta): ./run.sh _mapa_test.py [--puntos] [--solo t3_valle,t4_isla]
import sys
import time

import cv2
import numpy as np

import mapa as M

M.cargar()
M.usar("mx")
PUNTOS = "--puntos" in sys.argv          # dibuja ciudades y rutas (solo para comprobar posiciones)
SOLO = sys.argv[sys.argv.index("--solo") + 1].split(",") if "--solo" in sys.argv else None
# (nombre, (lon, lat, z), capas [(campo, alfa)], rutas, calzadas, rótulos de lagos)
TOMAS = [
    ("t1_caja", (-97.40, 18.15, 0.575), [("imperio_1519", 0.55), ("tlaxcala", 0.7), ("purepecha", 0.6)], ["comercio_pochteca", "migracion"], False, False),
    ("t2_centro", (-97.85, 19.32, 1.55), [("imperio_1519", 0.35), ("tlaxcala", 0.6)], ["cortes_ida", "noche_triste"], False, False),
    ("t3_valle", (-99.02, 19.48, 6.2), [], ["migracion", "calzada_tepeyac", "calzada_tlacopan", "calzada_iztapalapa", "calzada_coyoacan"], True, True),
    ("t4_isla", (-99.140, 19.425, 40.0), [], ["calzada_tepeyac", "calzada_tlacopan", "calzada_iztapalapa"], True, False),
    ("t5_imperio", (-97.70, 17.90, 0.80), [("imperio_1519", 0.75), ("tlaxcala", 0.8), ("teotitlan", 0.8), ("yopitzinco", 0.8), ("purepecha", 0.7)], [], False, False),
    ("t6_etapas", (-98.40, 18.70, 1.05), [("imperio_1502", 0.30), ("imperio_1481", 0.35), ("imperio_1469", 0.40), ("imperio_1440", 0.55),
                                         ("imperio_1428", 0.7)], [], False, False),
]
COLS_ETAPA = {"imperio_1440": (196, 74, 52), "imperio_1469": (226, 150, 64), "imperio_1481": (110, 120, 190), "imperio_1502": (90, 160, 100),
              "imperio_1428": (120, 40, 40)}
tiles = []
for nombre, (lon, lat, z), capas, rutas, calz, lagos in TOMAS:
    if SOLO and nombre not in SOLO:
        continue
    t0 = time.time()
    cam = M.Cam(lon, lat, z)
    img, base = M.pintar_base(cam, 0)
    for c, a in capas:
        if c in M.CAMPOS:
            M.pintar(img, cam.proyectar(M.CAMPOS[c]), COLS_ETAPA.get(c, M.COL.get(c, (200, 80, 60))) if nombre == "t6_etapas" else M.COL.get(c, (200, 80, 60)),
                     a, 0, luz=base.luz)
    if nombre == "t4_isla":           # la isla de 1325 (islote) sobre la de 1519, para ver los dos contornos
        M.pintar(img, cam.proyectar(M.CAMPOS["islote_1325"]), M.COL["imperio"], 0.35, 0, luz=base.luz)
    M.pintar_rios(img, cam, base)
    if calz:
        M.pintar_calzadas(img, cam)
    if lagos:
        for n, (lo, la) in M.LAGOS_ROT.items():
            M.rotulo_mapa(img, n, cam, lo, la, 30, 0.55, rot=0.0)
    if nombre in ("t1_caja", "t5_imperio"):
        for n, (lo, la) in (("GOLFO DE MÉXICO", (-94.6, 20.6)), ("OCÉANO PACÍFICO", (-99.0, 15.4))):
            M.rotulo_mapa(img, n, cam, lo, la, 40, 0.5)
    out = (np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8)
    if PUNTOS:
        for r in rutas:
            P = np.rint(cam.pant_pts(M.RUTAS[r])).astype(np.int32)
            cv2.polylines(out, [P], False, (40, 40, 160), 3, cv2.LINE_AA)
        for k, (lo, la) in M.CIUDADES.items():
            x, y = cam.pant(lo, la)
            if 0 <= x < 1920 and 0 <= y < 1080:
                cv2.circle(out, (int(x), int(y)), 6, (30, 30, 30), -1)
                cv2.putText(out, k, (int(x) + 8, int(y) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (30, 30, 30), 2, cv2.LINE_AA)
    cv2.imwrite(f"previews/mapa_{nombre}.jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 90])
    tiles.append(cv2.resize(out, (960, 540), interpolation=cv2.INTER_AREA))
    print(f"{nombre}: {time.time() - t0:.2f} s", flush=True)
if len(tiles) == 6:
    cv2.imwrite("previews/mapa_test.jpg", np.vstack([np.hstack(tiles[:3]), np.hstack(tiles[3:])]))
    print("ok: previews/mapa_t1_caja.jpg … mapa_t6_etapas.jpg y previews/mapa_test.jpg")
