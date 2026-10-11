import sys, cv2, numpy as np
ims=[cv2.imread(f"previews/era_{n}.jpg") for n in sys.argv[1:]]
w=min(i.shape[1] for i in ims)
ims=[i[:, :w] for i in ims]
cv2.imwrite("previews/mont.jpg", np.vstack(ims), [cv2.IMWRITE_JPEG_QUALITY, 88])
