# -*- coding: utf-8 -*-
"""Hoja con varias escenas dibujadas: python _hoja_mg.py nombre:tl,tl nombre2:tl ... [--out previews/mg_hoja.jpg]  (3 columnas a 640x360)"""
import sys, importlib
import cv2, numpy as np
import mg_esc as E
for _m in ('mg_esc2', 'mg_esc3', 'mg_esc4'):
    try:
        importlib.import_module(_m)
    except ModuleNotFoundError:
        pass
from motor import H, W
_o = sys.argv.index('--out') if '--out' in sys.argv else len(sys.argv)
args = sys.argv[1:_o]
out = sys.argv[sys.argv.index('--out') + 1] if '--out' in sys.argv else 'previews/mg_hoja.jpg'
ims = []
for a in args:
    nombre, _, tls = a.partition(':')
    fn, ini, fin = E.ESC[nombre]
    t0, t1 = ini(), fin()
    dur = t1 - t0 + 0.5
    for tl in ([float(x) for x in tls.split(',')] if tls else [1.0, (t1 - t0) / 2, t1 - t0 - 0.4]):
        lz = np.zeros((H, W, 3), np.float32)
        fn(lz, tl, t0 + tl, dur, 1.0)
        f8 = cv2.cvtColor((np.clip(lz, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR)
        f8 = cv2.resize(f8, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.rectangle(f8, (0, 0), (250, 22), (0, 0, 0), -1)
        cv2.putText(f8, f"{nombre} {tl:.1f}", (4, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 255), 1, cv2.LINE_AA)
        ims.append(f8)
while len(ims) % 3:
    ims.append(np.zeros_like(ims[0]))
cv2.imwrite(out, np.vstack([np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]), [cv2.IMWRITE_JPEG_QUALITY, 88])
print('ok', len(ims))
