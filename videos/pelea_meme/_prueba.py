import sys, numpy as np, cv2
import escenas as S
import efectos as E
from motor import Lienzo, a_uint8

def hoja(ts, nombre, cols=3, ancho=640):
    lz = Lienzo()
    tiles = []
    for t in ts:
        img = S.render_mundo(lz, t)
        img = E.acabado(img, int(t * 10))
        im = a_uint8(np.clip(img, 0, 1))
        im = cv2.resize(im, (ancho, int(ancho * 9 / 16)), interpolation=cv2.INTER_AREA)
        cv2.putText(im, f"{t:.2f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        tiles.append(im)
    while len(tiles) % cols:
        tiles.append(np.zeros_like(tiles[0]))
    filas = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
    cv2.imwrite(f"previews/{nombre}.jpg", cv2.cvtColor(np.vstack(filas), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 88])

if __name__ == "__main__":
    nombre = sys.argv[1]
    ts = [float(x) for x in sys.argv[2:]]
    hoja(ts, nombre)
    print("ok")
