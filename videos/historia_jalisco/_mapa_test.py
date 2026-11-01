# Prueba rápida del mapa: base + Jalisco + vecinos → previews/mapa_test.jpg
import cv2, numpy as np
import mapa as M
M.cargar(); M.usar("mx")
tiles = []
for (lon, lat, z, capas) in [(-103.6, 20.8, 1.05, ["jalisco"]), (-103.35, 20.62, 3.2, ["metro"]), (-103.2, 21.3, 2.0, ["caxcanes", "tecuexes", "cocas", "wixarika"]),
                              (-102.6, 20.9, 0.75, ["jalisco", "edo_nayarit", "edo_zacatecas", "edo_michoacan", "edo_guanajuato", "edo_colima", "edo_aguascalientes", "resto_mx"])]:
    cam = M.Cam(lon, lat, z)
    img, base = M.pintar_base(cam, 0)
    for k, c in enumerate(capas):
        M.pintar(img, cam.proyectar(M.CAMPOS[c]), M.COL_CELDAS[k % len(M.COL_CELDAS)], 0.8, 0, luz=base.luz)
    M.pintar_rios(img, cam, base)
    tiles.append(cv2.resize((np.clip(img, 0, 1)[..., ::-1] * 255).astype(np.uint8), (960, 540)))
cv2.imwrite("previews/mapa_test.jpg", np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])]))
