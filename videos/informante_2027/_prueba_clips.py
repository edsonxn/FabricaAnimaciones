import os, sys, glob
sys.path[:0] = [".", "../../nucleo"]
import cv2, numpy as np
from noir import Noir, clip_noir
h = Noir(); tiles=[]
noms = sys.argv[1:] or [os.path.basename(p)[:-4] for p in sorted(glob.glob("clips/*.mp4"))]
for n in noms:
    t = 2.0
    h.nuevo(t, None); clip_noir(h, n, t, 0.0, inicio=1.0)
    img = h.acabado(t, niebla=None)
    sm = cv2.resize((img*255).astype(np.uint8), (480, 270)); cv2.putText(sm, n, (6, 262), 0, 0.5, (255,255,255), 1)
    tiles.append(sm)
while len(tiles)%4: tiles.append(np.zeros_like(tiles[0]))
cv2.imwrite("previews/clips_noir.jpg", np.vstack([np.hstack(tiles[i:i+4]) for i in range(0,len(tiles),4)]))
cv2.imwrite("previews/_crop.png", (img*255).astype(np.uint8))
print(len(noms))
