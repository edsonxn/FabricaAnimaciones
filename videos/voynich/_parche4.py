# -*- coding: utf-8 -*-
"""Parche 4: fondo difuso de la misma página en las tomas de folio, pieles separadas, primer texto más grande."""
s = open("escenas.py", encoding="utf-8").read()

# helper
s = s.replace("def corcho():", '''def fondo_borroso(nombre, brillo=0.30, tinte=(1.0, 0.9, 0.78)):
    """Fondo: la propia imagen ampliada (cover), muy desenfocada y oscurecida; da capas al plano sin distraer."""
    def mk():
        im = D.cargar(D.ruta_img(nombre), 700)
        h, w = im.shape[:2]
        k = max(480 / w, 270 / h)
        r = cv2.resize(im, (int(w * k) + 1, int(h * k) + 1), interpolation=cv2.INTER_AREA)
        y0, x0 = (r.shape[0] - 270) // 2, (r.shape[1] - 480) // 2
        r = r[y0:y0 + 270, x0:x0 + 480].astype(np.float32) / 255.0
        r = cv2.GaussianBlur(r, (0, 0), 14)
        out = cv2.resize(r, (W, H), interpolation=cv2.INTER_CUBIC) * np.float32(tinte) * brillo
        return np.clip(out, 0, 1).astype(np.float32)
    return spr(("fb", nombre, brillo), mk)


def corcho():''', 1)

# gancho libro
s = s.replace("    lz[:] = D.pozo_luz(0.32, 0.45, 0.7)\n    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.22, W / 2 + 40, H / 2 - 10, 0.0), G1 - 0.1, mano=0.6)(t)",
              "    lz[:] = fondo_borroso(\"f001\", 0.34) * (0.55 + 0.45 * D.pozo_luz(0.32, 0.45, 0.7)[..., :1] / 0.3).clip(0, 1.4)\n    cam = D.Cam((1.0, W / 2, H / 2, 0.0), (1.22, W / 2 + 40, H / 2 - 10, 0.0), G1 - 0.1, mano=0.6)(t)")
s = s.replace('pal = bloque(kar("gancho", 0, 4, 11), 1370, 520, 92, lineas=(3,))\n    D.dibujar_bloque(lz, pal, t, "serif", 92, salida=G1 - 0.55)',
              'pal = bloque(kar("gancho", 0, 4, 11), 1390, 520, 110, lineas=(3,))\n    D.dibujar_bloque(lz, pal, t, "serif", 110, salida=G1 - 0.55)')

# héroes de contenido
s = s.replace('    if fondo:\n        lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.26, 0.19, 0.11))', '    if fondo:\n        lz[:] = fondo_borroso(f"f{nombre:03d}", 0.30)')
# duenos libro y fracaso
s = s.replace("def t_duenos_libro(lz, t):\n    tl = t - (d_quiso - PAD)\n    lz[:] = D.pozo_luz(0.5, 0.45, 0.8, (0.26, 0.19, 0.11))",
              "def t_duenos_libro(lz, t):\n    tl = t - (d_quiso - PAD)\n    lz[:] = fondo_borroso(\"f001\", 0.30)")
s = s.replace("def t_int_fracaso(lz, t):\n    tl = t - (I2 - PAD)\n    lz[:] = D.pozo_luz(0.35, 0.45, 0.8, (0.24, 0.17, 0.10))",
              "def t_int_fracaso(lz, t):\n    tl = t - (I2 - PAD)\n    lz[:] = fondo_borroso(\"f190\", 0.30)")
# pieles más estrechas
s = s.replace("cw, ch = int(w * 0.55), int(h * 0.36)", "cw, ch = int(w * 0.42), int(h * 0.34)")
open("escenas.py", "w", encoding="utf-8").write(s)
print("ok")
