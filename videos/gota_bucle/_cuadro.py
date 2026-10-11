import sys, cv2, numpy as np
import escenas as S
m = S.CLASES["nube"](S._ESC["nube"], 0)
t = float(sys.argv[1]); y0 = int(sys.argv[2]); y1 = int(sys.argv[3])
im = (m.render(None, t) * 255).astype(np.uint8)[y0:y1]
cv2.imwrite('previews/cuadro.png', cv2.cvtColor(im, cv2.COLOR_RGB2BGR))
