import estilos
estilos.activar("kurzgesagt")
import escenas as S
for k, d in enumerate(S.SHOTS):
    print(k, round(d["t0"], 1), round(d["t1"], 1), getattr(d["dib"], "__name__", "?"), d["ent"][0])
