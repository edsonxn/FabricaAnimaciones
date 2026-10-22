# Prueba del mapa de Aguascalientes: 4 cuadros a 1920x1080 → previews/mapa_t1..t4.jpg + hoja 2x2 previews/mapa_test.jpg
# uso (desde esta carpeta): PYTHONPATH="<esta carpeta>;C:\FabricaAnimaciones\nucleo" python _mapa_test.py [--puntos]
import sys

import cv2
import numpy as np

import mapa as M

M.cargar()
M.usar("mx")
PUNTOS = "--puntos" in sys.argv          # dibuja ciudades y rutas (solo para comprobar posiciones)
TOMAS = [
    ("t1_caja", (-102.15, 21.95, 0.74), [], ["camino_plata", "tren"]),
    ("t2_estado", (-102.33, 22.04, 1.8), ["aguascalientes"], ["ruta_turista"]),
    ("t3_capital", (-102.30, 21.88, 6.5), ["metro"], ["paseo_capital"]),
    ("t4_chichimecas", (-102.20, 21.95, 1.05), ["guachichiles", "guamares", "zacatecos", "caxcanes", "tecuexes"], []),
]
tiles = []
for nombre, (lon, lat, z), capas, rutas in TOMAS:
    cam = M.Cam(lon, lat, z)
    img, base = M.pintar_base(cam, 0)
    if nombre == "t1_caja":                # estados con su color, para comprobar las fronteras
        for c in ("aguascalientes", "edo_zacatecas", "edo_jalisco", "edo_san_luis_potosi", "edo_guanajuato"):
            M.pintar(img, cam.proyectar(M.CAMPOS[c]), M.COL[c], 0.45, 0, luz=base.luz)
    for c in capas:
        M.pintar(img, cam.proyectar(M.CAMPOS[c]), M.COL[c], 0.8, 0, luz=base.luz)
    M.pintar_rios(img, cam, base)
    if nombre == "t1_caja":
        for n, (lo, la) in (("ZACATECAS", (-102.7, 22.95)), ("JALISCO", (-103.1, 21.2)), ("GUANAJUATO", (-101.3, 21.2)),
                            ("SAN LUIS POTOSI", (-101.0, 22.6)), ("AGUASCALIENTES", (-102.3, 22.05))):
            M.rotulo_mapa(img, n, cam, lo, la, 34, 0.5)
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
cv2.imwrite("previews/mapa_test.jpg", np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])]))
print("ok: previews/mapa_t1_caja.jpg … mapa_t4_chichimecas.jpg y previews/mapa_test.jpg")
