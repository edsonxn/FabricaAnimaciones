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
    # Toma un punto medio de cada escena
    ts = [(e["t0"] + e["t1"]) / 2 for e in E.TL["escenas"]]
else:
    ts = [float(a) for a in args]

cols = 3
lz = E.Lienzo()
tiles = []
for t in ts:
    # Buscar qué escena corresponde a t
    esc_match = None
    for e_dict in E.TL["escenas"]:
        if e_dict["t0"] <= t < e_dict["t1"]:
            esc_match = e_dict
            break
    if esc_match is None:
        esc_match = E.TL["escenas"][-1]
    
    idx = [i for i, ed in enumerate(E.TL["escenas"]) if ed["id"] == esc_match["id"]][0]
    escena_obj = E.CLASES[esc_match["id"]](esc_match, idx)
    
    t0 = time.time()
    im = escena_obj.render(lz, t)
    dt = time.time() - t0
    print(f'[{esc_match["id"]}] t={t:6.2f}s  {dt*1000:5.0f} ms')
    small = cv2.resize((np.clip(im[..., ::-1] * 255, 0, 255)).astype(np.uint8), (960, 540), interpolation=cv2.INTER_AREA)
    cv2.putText(small, f'{esc_match["id"]} (t={t:.1f}s)', (25, 510), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (255, 255, 255), 2)
    tiles.append(small)

while len(tiles) % cols:
    tiles.append(np.zeros_like(tiles[0]))
rows = [np.hstack(tiles[i:i + cols]) for i in range(0, len(tiles), cols)]
hoja = np.vstack(rows)
cv2.imwrite('previews/hoja.jpg', hoja)
print('Hoja guardada en previews/hoja.jpg con', len(ts), 'cuadros')
