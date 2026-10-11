import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8, componer
import kz_mapa as KM
import kz_mapa_dib as MD
MP = KM.MAPA
casos = [(-60.0, 28.0, z) for z in (0.30, 0.27, 0.24, 0.21)]
tiles = []
for k, cam in enumerate(casos):
    lz = Lienzo(); lz.nuevo(1.0 + 0.1 * k, wob=0.0)
    MD.mar_vivo(lz, cam, 1.0 + 0.1 * k, seed=2)
    bg = MP.base(cam, 1.0 + 0.1 * k)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    tiles.append(cv2.resize(cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR), (960, 540), interpolation=cv2.INTER_AREA))
hoja = np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])])
cv2.imwrite("previews/olas_test.png", hoja)
print("ok")
