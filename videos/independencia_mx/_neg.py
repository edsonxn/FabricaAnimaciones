import estilos
estilos.activar("kurzgesagt")
import escenas as S
for k, d in enumerate(S.SHOTS):
    for tb in (17.4, 80.93, 116.93, 139.07, 391.9):
        if abs(d["t0"] - tb) < 1.2:
            print(tb, "shot", k, "t0=%.2f t1=%.2f" % (d["t0"], d["t1"]), "ent=", d["ent"], "dib=", getattr(d["dib"], "__name__", d["dib"]))
