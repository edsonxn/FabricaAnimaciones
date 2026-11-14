import cv2, json, sys, numpy as np, os
sys.path.insert(0, '..')
import importlib.util
spec = importlib.util.spec_from_file_location('plan', '../plan_clips.py'); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
E1 = 'E:/FabricaAnimaciones/videos/bt_jefes_ranking/cache360/'; E2 = 'E:/FabricaAnimaciones/videos/bt_50_secretos/cache360/'
def ruta(k):
    if k == 'PROS': return E1 + 'PROS.mp4'
    if k == 'P11': return E1 + 'P11.mp4'
    if k.startswith('P'): return E2 + k + '.mp4'
    ids = {'MM_LUNA': '9wGRK6uFx1k', 'MM_FD': 'M_Nmq5Qo_L0', 'XB_COAL': '54Cxuye80G8', 'XB_KLUNGO': '9bsKMc35x14', 'SMASH': 'bw6h7xAb0pw', 'NB_PATCH': 'AvrCwXFb4GE'}
    return 'x/' + ids[k] + '.mp4'
caps = {}
W, H = 160, 90
tiles = []
flags = []
rec = {'PROS': (0, 0, 0, .075), 'P01': (.144, 0, .144, 0), 'SMASH': (0, .08, 0, .18), 'XB_KLUNGO': (0, .1, 0, 0)}
for n in range(1, 170):
    f, s, q = P.PLAN[n]
    cap = caps.setdefault(f, cv2.VideoCapture(ruta(f)))
    br, prev, diffs = [], None, []
    imgs = []
    for k in range(0, 17):
        t = s + k * 0.5
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000); ok, fr = cap.read()
        if not ok: br.append(-1); continue
        g = cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY)
        br.append(g.mean())
        if prev is not None: diffs.append(np.abs(g.astype(float) - prev).mean())
        prev = g.astype(float)
        if k in (1, 8, 15):
            h, w = fr.shape[:2]
            r = rec.get(f)
            if r: fr = fr[int(h * r[1]):h - int(h * r[3]), int(w * r[0]):w - int(w * r[2])]
            imgs.append(cv2.resize(fr, (W, H)))
    m = min(br)
    if m < 12: flags.append((n, 'NEGRO', round(m, 1)))
    if min(br) < 0: flags.append((n, 'FIN', -1))
    if diffs and np.mean(diffs[:6]) < 0.6 and np.mean(diffs[8:]) < 0.6: flags.append((n, 'QUIETO', round(float(np.mean(diffs)), 2)))
    for k, im in enumerate(imgs):
        cv2.putText(im, f"{n:03d} {f} {s}", (2, 12), cv2.FONT_HERSHEY_SIMPLEX, .38, (0, 0, 0), 2)
        cv2.putText(im, f"{n:03d} {f} {s}", (2, 12), cv2.FONT_HERSHEY_SIMPLEX, .38, (0, 255, 255), 1)
        tiles.append(im)
print(flags)
cols, filas = 9, 8
per = cols * filas
for j in range(0, len(tiles), per):
    img = np.zeros((filas * H, cols * W, 3), np.uint8)
    for i, t in enumerate(tiles[j:j + per]):
        y, x = divmod(i, cols); img[y * H:(y + 1) * H, x * W:(x + 1) * W] = t
    cv2.imwrite(f'V_{j // per}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 82])
print(len(tiles))
