"""Hojas de prueba de los ítems nuevos: python _hoja_items.py [ids...] → previews/hoja_it_<k>.jpg (6 cuadros por ítem, 3 ítems por hoja)."""
import sys, time; sys.path.insert(0, "../../nucleo")
import numpy as np, cv2
import escenas as E
from comun import ORDEN, T0, T1
ids = sys.argv[1:] or [e for e in ORDEN if e in E.ANC and e not in ("m15", "m14", "p10")] + ["suscribe", "cierre"]
def tiempos(e):
    if e in E.ANC:
        a = E.ANC[e]
        anc = sorted([s["t0"] for s in a["sec"]] + [n[0] for n in a["notas"]])
        mid = [anc[int(i * (len(anc) - 1) / 3)] + 0.6 for i in range(4)] if anc else []
        return [a["stk"] + 0.9] + mid + [a["sello_t"] + 0.9]
    t0, t1 = T0(e), T1(e)
    return [t0 + (t1 - t0) * f for f in (0.12, 0.3, 0.45, 0.62, 0.8, 0.97)]
t00 = time.time(); n = 0
for g in range(0, len(ids), 3):
    ims = []
    for e in ids[g:g + 3]:
        for t in tiempos(e):
            im = E.cuadro(t)
            im = cv2.resize((np.clip(im, 0, 1)[..., ::-1] * 255).astype(np.uint8), (640, 360), interpolation=cv2.INTER_AREA)
            cv2.putText(im, f"{e} {t:.1f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 0), 4)
            cv2.putText(im, f"{e} {t:.1f}", (8, 24), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
            ims.append(im); n += 1
    while len(ims) % 3: ims.append(np.zeros_like(ims[0]))
    filas = [np.hstack(ims[i:i + 3]) for i in range(0, len(ims), 3)]
    cv2.imwrite(f"previews/hoja_it_{g // 3}.jpg", np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 82])
print(f"{n} cuadros, {(time.time() - t00) / n:.2f} s/cuadro")
