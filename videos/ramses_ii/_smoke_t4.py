import os, sys, time, traceback
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import escenas as E
T = E.TOMAS
print(len(T), len(E._POS))
for i in range(13, len(T)):
    t0, fn, _ = T[i]
    tb = T[i + 1][0] if i + 1 < len(T) else E.TOTAL
    for u in (0.15, 0.6, 0.95):
        t = t0 + (tb - t0) * u
        try:
            a = time.time(); fn(t, t0, tb); d = time.time() - a
        except Exception as ex:
            print("ERROR", fn.__name__, round(t, 1), repr(ex)); traceback.print_exc(limit=-2); break
    else:
        print("ok", fn.__name__, round(t0, 1), f"{d:.2f}s")
