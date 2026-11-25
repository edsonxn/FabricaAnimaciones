# Cuadros de un clip local: python cuadros_clip.py <clip.mp4> <prefijo> <t1> <t2> ... -> previews/cuadros/<prefijo>_<t>.jpg (1920)
import sys, os, cv2
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cap = cv2.VideoCapture(sys.argv[1]); pre = sys.argv[2]
for t in sys.argv[3:]:
    cap.set(cv2.CAP_PROP_POS_MSEC, float(t) * 1000); ok, f = cap.read()
    if ok:
        p = os.path.join(D, "previews", "cuadros", f"{pre}_{t}.jpg"); cv2.imwrite(p, f, [cv2.IMWRITE_JPEG_QUALITY, 90]); print(p)
