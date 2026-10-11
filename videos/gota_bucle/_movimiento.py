# Mide cuánto cambia cada zona del cuadro entre cuadros consecutivos: ninguna forma debe quedarse quieta.
import numpy as np
import escenas as S
m = S.CLASES["nube"](S._ESC["nube"], 0)
def d(t):
    a = m.render(None, t); b = m.render(None, t + 1 / 12)
    return float(np.abs(a - b).mean() * 1000)
for t in (0.3, 0.9, 5.7, 6.4, 10.5, 13.5, 15.0, 19.5, 24.4, 29.0, 32.5, 36.5, 43.6):
    print(f"t={t:5.1f}  cambio medio x1000 = {d(t):.2f}")
