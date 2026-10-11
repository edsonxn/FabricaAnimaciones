import sys, time, json, cv2, numpy as np
from motor import Lienzo, a_uint8, VERTICAL as VERT
import escenas as S
TL = json.load(open("timeline.json", encoding="utf-8"))
CLASES = S.CLASES
eid = sys.argv[1]; tiempos = [float(x) for x in sys.argv[2:]]
d = [e for e in TL["escenas"] if e["id"] == eid][0]
esc = CLASES[eid](d, 0)
import os
os.makedirs("previews", exist_ok=True)
lz = Lienzo(); tiles = []
for t in tiempos:
    t0 = time.time(); img = esc.render(lz, t); dt = time.time() - t0
    im = cv2.resize(a_uint8(img), ((360, 640) if VERT else (640, 360)), interpolation=cv2.INTER_AREA)
    cv2.putText(im, f"{t:.2f}s {dt*1000:.0f}ms", (8, im.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,0), 3, cv2.LINE_AA)
    cv2.putText(im, f"{t:.2f}s {dt*1000:.0f}ms", (8, im.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255,255,255), 1, cv2.LINE_AA)
    tiles.append(im)
while len(tiles) % 3: tiles.append(np.zeros_like(tiles[0]))
sheet = np.vstack([np.hstack(tiles[i:i+3]) for i in range(0, len(tiles), 3)])
cv2.imwrite(f"previews/esc_{eid}.jpg", cv2.cvtColor(sheet, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("eventos sfx:", len(esc.sfx))
