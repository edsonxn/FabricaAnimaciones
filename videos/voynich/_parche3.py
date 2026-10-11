# -*- coding: utf-8 -*-
"""Parche 3: tablero de teorías (posiciones, tarjeta central) y ventana de internet."""
s = open("escenas.py", encoding="utf-8").read()

# ---------------- tablero de teorías
a = s.index("    cx, cy = C0\n    centro = (cx, cy - 20)")
b = s.index("    franja_texto(lz, 0.5, 0.78)\n    D.dibujar_bloque(lz, bloque(kar(\"teorias\", 0, 4, 6)")
nuevo = '''    cx, cy = C0
    ANC, ALT2 = 360, 0.5 * 360 * (0.055 + 0.89 * 1.15 + 0.17)          # ancho y semialtura de las polaroids
    tarjetas = (("alberti", -520, 20, -5, t_codigo, "Disco de cifrado"), ("f190", 0, 90, 3, t_idioma_t, None),
                ("f110", 520, 10, -3, t_fraude, "¿Fraude medieval?"))
    pins = []
    for k, (nom, dx, dy, r, ti, ley) in enumerate(tarjetas):
        sp = pola(nom, ANC, 1.15, (0.5, 0.5) if nom != "f190" else (0.5, 0.35), ley)
        carta(lz, sp, cam, t, ti - 0.1, cx + dx, cy + dy, r, desde=(0, -420), fase=k * 1.3)
        if t > ti + 0.3:
            pins.append((cx + dx, cy + dy - ALT2 + 22))
    # tarjeta central con la pregunta
    if t > T0 + 0.1:
        q = spr("pregunta", lambda: D.Sprite(np.full((220, 360, 3), (240, 235, 220), np.uint8), None, sombra=True, sr=12))
        M = cam @ D.poner(q.w, q.h, cx, cy - 250, 1.0, 1.5)
        D.pegar(lz, q, M, smooth(prog(t, T0 + 0.1, T0 + 0.4)))
        pm, a_, m = D.palabra_img("¿Qué es?", "serif", 84, (0.72, 0.05, 0.05), stroke=0.02, glow=0.0)
        x, y = D.tf(M, q.w / 2, q.h / 2)
        D.mezclar_pm(lz, pm, a_, int(x - pm.shape[1] / 2), int(y - pm.shape[0] / 2), smooth(prog(t, T0 + 0.2, T0 + 0.5)))
    for k, p in enumerate(pins):
        ti = (t_codigo, t_idioma_t, t_fraude)[k]
        D.hilo(lz, cam, (cx, cy - 350), p, smooth(prog(t, ti + 0.2, ti + 0.7)))
    if t > T0 + 0.1:
        D.pin(lz, cam, cx, cy - 350)
    for p in pins:
        D.pin(lz, cam, *p)
    # X rojas: ninguna teoría convenció
    for k, ti in enumerate((t_ninguna, t_teoria, t_convencido)):
        dx, dy = tarjetas[k][1], tarjetas[k][2]
        x, y = D.tf(cam, cx + dx, cy + dy)
        z = float(np.sqrt(abs(np.linalg.det(cam[:2, :2]))))
        D.marcador_mano(lz, "tachado", x, y, ANC * 0.9 * z, ALT2 * 1.7 * z, prog(t, ti, ti + 0.3), grosor=16)
        D.marcador_mano(lz, "tachado", x, y, -ANC * 0.9 * z, ALT2 * 1.7 * z, prog(t, ti + 0.12, ti + 0.42), grosor=16)
'''
s = s[:a] + nuevo + s[b:]

# ---------------- ventana de internet
a = s.index("def t_cierre_internet(lz, t):")
b = s.index("def _ventana():")
nuevo = '''def t_cierre_internet(lz, t):
    tl = t - (K1 - PAD)
    lz[:] = D.pozo_luz(0.5, 0.5, 0.85, (0.17, 0.15, 0.13))
    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.06, W / 2, H / 2 - 8, 0.0), K2 - K1 + 0.4, mano=0.6)(tl)
    vent = spr("ventana", lambda: _ventana())
    D.pegar(lz, vent, cam @ D.poner(vent.w, vent.h, W / 2, 470, 1.0, 0.0), smooth(prog(t, K1 - PAD, K1 + 0.3)))
    # vista previa de la biblioteca digital: cuadrícula de páginas que aparecen una a una
    nomb = (4, 7, 10, 24, 32, 110, 111, 136, 141, 147, 175, 176)
    for k, n in enumerate(nomb):
        col, fila = k % 6, k // 6
        x = 405 + col * 222
        y = 385 + fila * 335 - 6 * math.sin(0.7 * t + k)
        sp = pola(f"f{n:03d}", 205, 1.36, (0.5, 0.45))
        D.pegar(lz, sp, cam @ D.poner(sp.w, sp.h, x, y, 1.0, (k % 3 - 1) * 1.5), smooth(prog(t, k_internet - 0.2 + 0.06 * k, k_internet + 0.3 + 0.06 * k)))
    franja_texto(lz, 0.5, 0.8)
    D.dibujar_bloque(lz, bloque(kar("cierre", 1, 0, 5), W / 2, 985, 76), t, "serif", 76, salida=k_600 - 0.15)
    D.dibujar_bloque(lz, bloque([("Unos", T("cierre", "unos", frase=1)), ("600", k_600), ("Años", T("cierre", "anos", frase=1))], W / 2, 985, 84), t, "serif", 84, salida=T("cierre", "sigue", frase=1) - 0.1)
    D.dibujar_bloque(lz, bloque(kar("cierre", 1, 9, 14), W / 2, 985, 84), t, "serif", 84)


'''
s = s[:a] + nuevo + s[b:]
s = s.replace("    w, h = 1300, 760\n", "    w, h = 1500, 760\n")
open("escenas.py", "w", encoding="utf-8").write(s)
print("ok")
