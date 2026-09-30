import sys, time, os
import numpy as np, cv2
import boceto as B, mapa as M
M.cargar()
os.makedirs('previews', exist_ok=True)
claves = sys.argv[1:] or ['dario', 'ciro', 'alejandro', 'partos', 'sasanidas', 'califato', 'mongol', 'safavidas', 'elam', 'medos', 'persis', 'iran']
tiles = []
for k in claves:
    cam = M.Cam(50, 31, 1.2 if k not in ('elam', 'medos', 'persis', 'iran', 'safavidas') else 2.1)
    img = M.fondo_base()
    M.pintar_tierra(img, cam, 0)
    M.pintar(img, cam.proyectar(M.CAMPOS[k]), M.COL.get(k, (180, 120, 120)), 1.0, 0)
    h = B.Hoja(); h.limpiar(); h.fondo = img
    out = np.clip(h.componer(), 0, 1)
    sm = cv2.resize((out[..., ::-1] * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
    cv2.putText(sm, k, (10, 345), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
    tiles.append(sm)
while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite('previews/_mapas.jpg', np.vstack([np.hstack(tiles[i:i+3]) for i in range(0, len(tiles), 3)]))
