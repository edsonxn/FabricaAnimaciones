import escenas as E, mapa as M
from core import T
def pos(t, geo):
    w = E.R.peso_am(t); st = E.estado_cam(t, w); M.usar("am" if w > 0 else "eu")
    cam = M.Cam(*st); return tuple(round(v) for v in cam.pant(*geo)), round(st[2], 2)
tp, tg, tc = T("ochocientos", "palabra"), T("ochocientos", "guerrilla"), T("ochocientos", "cadiz")
print("palabra", round(tp, 2), "guerrilla", round(tg, 2), "cadiz", round(tc, 2))
for t in (tp, tg, tg + 0.7, tc - 0.5):
    print(round(t, 2), [pos(t, g) for g in ((-5.0, 40.9), (-1.8, 40.6), (-3.4, 38.4), (-6.0, 38.9))])
td, ta = T("reyes", "doce"), T("reyes", "america")
print("doce", round(td, 2), "america", round(ta, 2))
for t in (td, td + 0.5, ta - 0.3):
    print(round(t, 2), "guanahani", pos(t, (-74.5, 24.0)))
