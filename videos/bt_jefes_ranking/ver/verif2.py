import cv2, json, sys, numpy as np, os, subprocess, importlib.util
from concurrent.futures import ThreadPoolExecutor
spec = importlib.util.spec_from_file_location('plan', '../plan_clips.py'); P = importlib.util.module_from_spec(spec); spec.loader.exec_module(P)
E1 = 'E:/FabricaAnimaciones/videos/bt_jefes_ranking/cache360/'; E2 = 'E:/FabricaAnimaciones/videos/bt_50_secretos/cache360/'
def ruta(k):
    if k == 'PROS': return E1 + 'PROS.mp4'
    if k == 'P11': return E1 + 'P11.mp4'
    if k.startswith('P'): return E2 + k + '.mp4'
    ids = {'MM_LUNA': '9wGRK6uFx1k', 'MM_FD': 'M_Nmq5Qo_L0', 'XB_COAL': '54Cxuye80G8', 'XB_KLUNGO': '9bsKMc35x14', 'SMASH': 'bw6h7xAb0pw', 'NB_PATCH': 'AvrCwXFb4GE'}
    return 'x/' + ids[k] + '.mp4'
os.makedirs('tmpf', exist_ok=True)
OFF = [0.5, 2.5, 4.5, 6.5, 7.8]
def job(a):
    n, k, f, t = a
    out = f'tmpf/{n:03d}_{k}.png'
    subprocess.run(['C:/ffmpeg/bin/ffmpeg', '-y', '-v', 'error', '-ss', str(t), '-i', ruta(f), '-frames:v', '1', '-vf', 'scale=320:180', out])
    return out
jobs = []
for n in range(1, 170):
    f, s, q = P.PLAN[n]
    for k, o in enumerate(OFF): jobs.append((n, k, f, s + o))
with ThreadPoolExecutor(8) as ex: list(ex.map(job, jobs))
W, H = 160, 90
rec = {'PROS': (0, 0, 0, .075), 'P01': (.144, 0, .144, 0), 'SMASH': (0, .08, 0, .18), 'XB_KLUNGO': (0, .1, 0, 0)}
tiles, flags = [], []
for n in range(1, 170):
    f, s, q = P.PLAN[n]
    br, ims = [], []
    for k in range(5):
        fr = cv2.imread(f'tmpf/{n:03d}_{k}.png')
        if fr is None: br.append(-1); ims.append(None); continue
        br.append(cv2.cvtColor(fr, cv2.COLOR_BGR2GRAY).mean()); ims.append(fr)
    if min(br) < 0: flags.append((n, 'SIN_IMAGEN', br))
    elif min(br) < 14: flags.append((n, 'NEGRO', [round(b) for b in br]))
    if all(i is not None for i in ims):
        d = [np.abs(ims[i].astype(float) - ims[i + 1].astype(float)).mean() for i in range(4)]
        if max(d) < 2.0: flags.append((n, 'QUIETO', [round(x, 1) for x in d]))
    for k in (0, 2, 4):
        fr = ims[k] if ims[k] is not None else np.zeros((180, 320, 3), np.uint8)
        h, w = fr.shape[:2]; r = rec.get(f)
        if r: fr = fr[int(h * r[1]):h - int(h * r[3]), int(w * r[0]):w - int(w * r[2])]
        im = cv2.resize(fr, (W, H))
        t = f"{n:03d} {f} {s}"
        cv2.putText(im, t, (2, 12), cv2.FONT_HERSHEY_SIMPLEX, .38, (0, 0, 0), 2); cv2.putText(im, t, (2, 12), cv2.FONT_HERSHEY_SIMPLEX, .38, (0, 255, 255), 1)
        tiles.append(im)
print(flags)
cols, filas = 9, 8; per = cols * filas
for j in range(0, len(tiles), per):
    img = np.zeros((filas * H, cols * W, 3), np.uint8)
    for i, t in enumerate(tiles[j:j + per]):
        y, x = divmod(i, cols); img[y * H:(y + 1) * H, x * W:(x + 1) * W] = t
    cv2.imwrite(f'V_{j // per}.jpg', img, [cv2.IMWRITE_JPEG_QUALITY, 82])
print(len(tiles))
