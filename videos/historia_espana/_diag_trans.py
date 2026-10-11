import escenas as E
TL = E.TL
print("escenas:", [(e["id"], round(e["t0"], 1), round(e["t1"], 1)) for e in TL["escenas"]])
for tr in E.R.trans:
    for a in ("t0", "t1", "tipo", "dur", "nombre"):
        pass
    print("trans:", {k: (round(v, 2) if isinstance(v, float) else v) for k, v in vars(tr).items() if isinstance(v, (int, float, str))})
import core
for t in (75.0, 75.5, 76.0, 76.25, 76.5, 76.75, 77.0, 162.0, 162.25, 162.5, 162.75, 163.0, 189.5, 190.0, 190.5, 191.0):
    st = E.estado_cam(t, E.R.peso_am(t))
    print(f"t={t:6.2f} cam lon={st[0]:7.2f} lat={st[1]:6.2f} zoom={st[2]:5.2f} w={E.R.peso_am(t):.2f}")
