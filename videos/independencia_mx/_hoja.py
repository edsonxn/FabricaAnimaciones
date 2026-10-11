"""Hoja de varios cuadros completos a 960x540: python _hoja.py nombre t1 t2 ... (cuadros con el acabado final; 2 columnas)"""
import sys
import cv2, numpy as np
import estilos
estilos.activar("kurzgesagt")
from motor import Lienzo, a_uint8
import escenas as S
import efectos as E
lz = Lienzo()
tiles = []
for ts in sys.argv[2:]:
    t = float(ts)
    img = S.render_mundo(lz, t)
    img = E.acabado(img, int(t * 10))
    bgr = cv2.cvtColor(a_uint8(np.clip(img, 0, 1)), cv2.COLOR_RGB2BGR)
    tiles.append(cv2.resize(bgr, (960, 540), interpolation=cv2.INTER_AREA))
    cv2.putText(tiles[-1], ts, (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2, cv2.LINE_AA)
if len(tiles) % 2: tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + 2]) for i in range(0, len(tiles), 2)]
cv2.imwrite(f"previews/{sys.argv[1]}.jpg", np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
