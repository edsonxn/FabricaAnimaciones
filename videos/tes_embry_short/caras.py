"""Detecta caras (Haar frontal + perfil de OpenCV) en cada momento cada 0,25 s y guarda caras.json:
{clave: [[t, cx%, cy%, alto%], ...]} con la detección más cercana al punto guía (GUIA) de cada momento.
Uso: python caras.py [clave ...]"""
import json, os, sys
import cv2

AQUI = os.path.dirname(os.path.abspath(__file__))
R = {m["c"]: m for m in json.load(open(os.path.join(AQUI, "momentos.json"), encoding="utf-8"))}
# punto guía aproximado (x%, y%) de la cara de quien habla, mirado en previews/momentos_*.jpg
GUIA = {"hijas": (48, 38), "alcohol": (50, 30), "orca": (49, 36), "pan": (56, 42), "sombrero": (52, 38),
        "dormir": (62, 40), "yelmo": (52, 30), "dorthe": (47, 45), "diego": (48, 40), "trio": (45, 45),
        "fracaso": (72, 20), "autografo": (45, 40), "tiktok": (52, 30)}
fr_cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
pr_cas = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_profileface.xml")

out = json.load(open(os.path.join(AQUI, "caras.json"), encoding="utf-8")) if os.path.exists(os.path.join(AQUI, "caras.json")) else {}
for c in sys.argv[1:] or list(GUIA):
    m = R[c]
    cap = cv2.VideoCapture(os.path.join(AQUI, "segmentos", "clips", c + ".mp4"))
    gx, gy = GUIA[c]
    res = []
    for a, b in m["trozos"]:
        t = a
        while t <= b + 0.01:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, f = cap.read()
            if ok:
                H, W = f.shape[:2]
                g = cv2.equalizeHist(cv2.cvtColor(cv2.resize(f, (W // 2, H // 2)), cv2.COLOR_BGR2GRAY))
                dets = list(fr_cas.detectMultiScale(g, 1.1, 4, minSize=(14, 14)))
                dets += list(pr_cas.detectMultiScale(g, 1.1, 4, minSize=(14, 14)))
                dets += [(g.shape[1] - x - w, y, w, h) for x, y, w, h in pr_cas.detectMultiScale(cv2.flip(g, 1), 1.1, 4, minSize=(14, 14))]
                mejor = None
                for x, y, w, h in dets:
                    cx, cy = (x + w / 2) / g.shape[1] * 100, (y + h / 2) / g.shape[0] * 100
                    d = ((cx - gx) ** 2 + (cy - gy) ** 2) ** .5
                    if d < 18 and (mejor is None or d < mejor[0]):
                        mejor = (d, cx, cy, h / g.shape[0] * 100)
                if mejor:
                    res.append([round(t, 2), round(mejor[1], 1), round(mejor[2], 1), round(mejor[3], 1)])
            t += 0.25
    n = sum(int((b - a) / .25) + 1 for a, b in m["trozos"])
    print("%-10s %2d/%2d cuadros con cara  %s" % (c, len(res), n, res[:3]))
    out[c] = res
json.dump(out, open(os.path.join(AQUI, "caras.json"), "w", encoding="utf-8"))
