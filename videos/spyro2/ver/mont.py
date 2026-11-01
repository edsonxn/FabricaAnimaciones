# mont.py <salida> <cols> <ancho> <imgs...>
import cv2, sys, numpy as np
out, cols, w = sys.argv[1], int(sys.argv[2]), int(sys.argv[3]); fs = sys.argv[4:]
tiles=[]
for f in fs:
    im = cv2.imread(f); h = int(im.shape[0]*w/im.shape[1]); im = cv2.resize(im,(w,h))
    cv2.putText(im, f.split('_')[-1][:-4], (6,24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,0), 4)
    cv2.putText(im, f.split('_')[-1][:-4], (6,24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 1)
    tiles.append(im)
H = max(t.shape[0] for t in tiles)
while len(tiles)%cols: tiles.append(np.zeros((H,w,3),np.uint8))
rows=[np.hstack(tiles[i:i+cols]) for i in range(0,len(tiles),cols)]
cv2.imwrite(out, np.vstack(rows), [cv2.IMWRITE_JPEG_QUALITY, 88])
