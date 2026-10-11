"""Hoja de contacto: python _prueba.py t1 t2 ... -> previews/hoja.jpg (cuadros 960x540 en rejilla)"""
import os, sys, time
AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(AQUI, "..", "..", "nucleo")))
sys.path.insert(0, AQUI)
import numpy as np, cv2
import escenas as E

os.makedirs('previews', exist_ok=True)
args = [a for a in sys.argv[1:]]
if not args:
    # Por defecto toma un punto medio de cada escena
    ts = [(e["t0"] + e["t1"]) / 2 for e in E.TL["escenas"]]
else:
    ts = [float(a) for a in args]

cols = 4 if len(ts) >= 8 else (3 if len(ts) > 4 else 2)
d = E.TL["escenas"][0]
m = E.Mundo(d, 0)
m.preparar()
tiles = []
for t in ts:
    t0 = time.time()
    im = m.render(None, t)
    dt = time.time() - t0
    print(f't={t:6.2f}  {dt*1000:5.0f} ms')
    small = cv2.resize((np.clip(im[..., ::-1] * 255, 0, 255)).astype(np.uint8), (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(small, f't={t:.1f}s', (20, 510), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (20, 20, 220), 2)
    tiles.append(small)
while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
hoja = np.vstack(rows)
cv2.imwrite('previews/hoja.jpg', hoja)
print('Hoja guardada en previews/hoja.jpg con', len(ts), 'cuadros')
