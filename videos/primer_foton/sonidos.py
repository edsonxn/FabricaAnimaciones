# -*- coding: utf-8 -*-
"""Efectos de sonido del Short, anclados a las palabras de la narración y a los instantes de la coreografía.
Formato: (t, nombre, volumen, {kwargs: tono, dur, pan}). Los nombres existen en nucleo/sfx.py."""


def eventos():
    import escenas as S
    T = S.T
    E = []
    a = E.append

    # ---------------- 1. gancho
    a((0.05, "zoom_whoosh", 0.55, dict(dur=0.7, tono=1.3)))
    a((0.45, "impacto", 0.9, {}))
    a((1.11, "impacto", 0.8, dict(tono=0.9)))
    a((1.37, "viento", 0.35, dict(dur=1.3)))
    a((2.31, "impacto", 0.95, dict(tono=0.8)))
    a((2.35, "zap", 0.5, {}))
    a((3.62, "whoosh", 0.6, dict(dur=0.6, tono=1.2)))
    a((4.12, "pop", 0.8, dict(tono=1.1)))
    a((4.34, "pop", 0.7, dict(tono=1.0)))
    a((4.45, "bling", 0.4, {}))
    a((5.00, "pop", 0.7, dict(tono=1.2)))
    a((5.28, "brillo", 0.7, {}))
    # ---------------- 2. calor
    a((6.15, "suspiro", 0.5, dict(dur=0.9)))
    a((6.89, "tick", 0.4, {}))
    a((7.79, "zap", 0.45, {}))
    a((8.15, "fuego", 0.5, dict(dur=3.0)))
    a((8.15, "crece", 0.5, dict(dur=1.0)))
    a((8.97, "boing", 0.6, dict(tono=0.9)))
    a((9.17, "explosion", 0.7, dict(tono=1.2)))
    a((9.8, "whoosh", 0.5, dict(dur=0.5, tono=0.8)))
    a((10.0, "burbujas", 0.5, dict(dur=0.9)))
    for k in range(14):
        a((10.0 + 0.37 * k, "plop", 0.35, dict(tono=0.9 + 0.12 * (k % 4))))
    # ---------------- 3. higgs
    a((11.6, "pincel", 0.5, dict(dur=0.7)))
    for k in range(8):
        a((12.5 + 0.25 * k, "tick", 0.28, dict(tono=1.0 + 0.04 * k)))
    a((14.1, "whoosh", 0.5, dict(dur=0.45, tono=0.9)))
    a((14.52, "clink", 0.9, dict(tono=0.7)))
    a((14.52, "zap", 0.6, {}))
    a((14.6, "ola", 0.5, dict(dur=1.8)))
    for k, tc in enumerate([17.30, 17.52, 17.74, 17.96, 18.18, 18.34]):
        a((tc - 0.05, "whoosh", 0.3, dict(dur=0.25, tono=1.4)))
        a((tc + 0.2, "bonk", 0.75, dict(tono=0.85 + 0.07 * k)))
    a((19.3, "zoom_whoosh", 0.7, dict(dur=0.7, tono=1.2)))
    a((19.98, "pop", 0.8, {}))
    a((20.22, "brillo", 0.8, {}))
    a((20.22, "ding", 0.5, dict(tono=1.2)))
    # ---------------- 4. multitud
    a((21.3, "pincel", 0.5, dict(dur=0.7)))
    for k in range(6):
        a((22.99 + 0.08 * k, "pop", 0.55, dict(tono=1.0 + 0.1 * k)))
    for k in range(12):
        a((23.55 + 0.05 * k, "pop", 0.4, dict(tono=1.3 + 0.03 * k)))
    a((24.0, "pop", 0.7, dict(tono=0.8)))
    a((24.23, "ding", 0.55, dict(tono=1.1)))
    a((25.47, "explosion", 0.5, dict(tono=1.3)))
    a((25.5, "brillo_caleido", 0.6, dict(dur=0.95)))
    a((26.53, "ding", 0.6, dict(tono=1.0)))
    a((27.23, "bling", 0.6, {}))
    # ---------------- 5. niebla
    a((28.9, "iris", 0.45, dict(dur=0.7)))
    a((29.6, "viento", 0.3, dict(dur=2.0)))
    for k, tc in enumerate([32.28, 32.72, 32.88, 33.50, 33.76, 33.90, 34.06]):
        a((tc, "bonk", 0.7, dict(tono=1.2 - 0.05 * k)))
        a((tc, "estrellitas", 0.3, dict(tono=1.0 + 0.04 * k)))
    a((34.99, "suspiro", 0.6, dict(dur=0.9)))
    a((35.2, "reloj_rapido", 0.5, dict(dur=1.7)))
    a((36.71, "campana", 0.6, dict(tono=0.8)))
    # ---------------- 6. libre
    a((37.6, "pincel", 0.5, dict(dur=0.7)))
    a((38.4, "hielo", 0.55, dict(dur=1.0)))
    a((39.01, "brr", 0.6, {}))
    for k in range(6):
        a((40.2 + 0.12 * k, "pop", 0.5, dict(tono=1.0 + 0.1 * k)))
        a((41.1 + 0.15 * k, "bling", 0.35, dict()))
    a((42.95, "campana", 0.6, dict(tono=1.2)))
    a((43.6, "viento", 0.4, dict(dur=1.6)))
    a((44.4, "ola", 0.4, dict(dur=0.85)))
    a((45.5, "ding", 0.7, dict(tono=1.1)))
    a((46.30, "crece", 0.6, dict(dur=0.5)))
    a((46.44, "zoom_whoosh", 0.9, dict(dur=0.9)))
    a((46.55, "impacto", 0.8, dict(tono=1.1)))
    a((46.55, "brillo", 0.8, dict(tono=1.1)))
    # ---------------- 7. hoy
    a((47.4, "iris", 0.45, dict(dur=0.6)))
    a((47.7, "whoosh", 0.5, dict(dur=0.7, tono=1.3)))
    a((48.4, "brr", 0.5, {}))
    a((48.9, "suspiro", 0.5, dict(dur=0.9)))
    a((49.55, "boing", 0.7, dict(tono=0.9)))
    a((50.25, "glitch", 0.6, dict(dur=0.7)))
    a((50.3, "siseo", 0.28, dict(dur=5.8)))
    a((51.03, "pop", 0.7, dict(tono=0.9)))
    a((51.83, "ding", 0.6, dict(tono=1.0)))
    # ---------------- 8. cierre
    a((53.3, "pop", 0.6, dict(tono=0.8)))
    a((55.2, "zoom_whoosh", 0.8, dict(dur=1.2, tono=0.9)))
    a((56.25, "impacto", 1.0, dict(tono=0.9)))
    a((56.49, "explosion", 0.6, dict(tono=1.0)))
    a((56.75, "brillo", 0.8, {}))
    a((56.9, "ding", 0.6, dict(tono=1.3)))
    return E
