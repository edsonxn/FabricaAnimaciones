# -*- coding: utf-8 -*-
"""Ordena lo bajado de Flow (21-oct-2026): variante elegida = `<clave>_a.jpg` (recortar y escenas solo leen `_a`).
Escenarios en 1K (imagenes/), con el marco de papel recortado; hojas en 2K desde Descargas (hojas/), comprobando que cada 2K
es la variante elegida (correlación con las dos 1K). Ejecutar desde la carpeta del video."""
import glob
import os
import shutil

import numpy as np
from PIL import Image

ELEGIDA = {  # escenarios (1K)
    "ciudad_lluvia": "b", "oficina": "b", "pasillo_puerta": "a", "archivo": "a", "servidores": "a", "callejon_puerta": "b",
    "aula": "b", "interrogatorio": "a", "observacion": "b", "sala_control": "b", "teatro": "b", "dos_puertas": "b",
    "escritorio_diario": "a", "salon_alfombra": "b", "calle_final": "a", "laboratorio": "b",
}
HOJAS = {  # hoja: (variante elegida, prefijo del archivo 2K en Descargas)
    "detective_hoja": ("b", "Detective_character_model_sheet_2K"),
    "detective_camina": ("a", "Detective_walk_cycle_sprite_sheet_2K"),
    "ia_hoja": ("b", "Android_character_model_sheet_poses_2K"),
    "ia_camina": ("b", "Android_walk_cycle_sprite_sheet_2K"),
    "investigadores_hoja": ("a", "Researchers_drawn_as_film_noir_2K"),
    "utileria": ("a", "Detective_prop_sheet_grid_objects_2K"),
    "humo_papel": ("a", "Graphic_novel_illustration_prop_"),
    "polilla_aleteo": ("a", "Dark_moth_wing-flap_flight_2K"),
}
DESC = os.path.join(os.environ["USERPROFILE"], "Downloads")


def gris(p, n=64):
    return np.asarray(Image.open(p).convert("L").resize((n * 16 // 9, n)), np.float32)


def corr(a, b):
    a, b = a - a.mean(), b - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-6))


def sin_marco(im):
    """Quita el marco de papel claro/uniforme que Flow pinta a veces alrededor de la lámina y deja 16:9."""
    a = np.asarray(im.convert("L"), np.float32)
    h, w = a.shape

    def borde(lineas):
        n = 0
        for v in lineas:
            if v.std() < 9 and (v.mean() > 175 or v.mean() < 18):
                n += 1
            else:
                break
        return n
    t = borde(a[i] for i in range(h // 6))
    b = borde(a[h - 1 - i] for i in range(h // 6))
    l = borde(a[:, i] for i in range(w // 6))
    r = borde(a[:, w - 1 - i] for i in range(w // 6))
    if max(t, b, l, r) == 0:
        return im, (0, 0, 0, 0)
    m = 4                                                    # unos píxeles más para llevarse el canto del marco
    x0, y0, x1, y1 = l + m * (l > 0), t + m * (t > 0), w - r - m * (r > 0), h - b - m * (b > 0)
    cw, ch = x1 - x0, y1 - y0
    if cw / ch > 16 / 9:                                     # recorta al 16:9 desde el centro
        nw = int(ch * 16 / 9); x0 += (cw - nw) // 2; x1 = x0 + nw
    else:
        nh = int(cw * 9 / 16); y0 += (ch - nh) // 2; y1 = y0 + nh
    return im.crop((x0, y0, x1, y1)).resize((w, h), Image.LANCZOS), (t, b, l, r)


os.makedirs("imagenes/_flow1k", exist_ok=True)
for k, v in ELEGIDA.items():
    for x in "ab":
        p = f"imagenes/{k}_{x}.jpg"
        if os.path.exists(p):
            shutil.move(p, f"imagenes/_flow1k/{k}_{x}.jpg")
    im, marco = sin_marco(Image.open(f"imagenes/_flow1k/{k}_{v}.jpg").convert("RGB"))
    im.save(f"imagenes/{k}_a.jpg", quality=95)
    print(f"{k:20s} variante {v}  marco t/b/l/r = {marco}")

os.makedirs("hojas/_flow1k", exist_ok=True)
for k, (v, pref) in HOJAS.items():
    for x in "ab":
        p = f"hojas/{k}_{x}.jpg"
        if os.path.exists(p):
            shutil.move(p, f"hojas/_flow1k/{k}_{x}.jpg")
    c = sorted(glob.glob(os.path.join(DESC, pref + "*.jpg")), key=os.path.getmtime)
    if not c:
        print("FALTA 2K", k)
        continue
    g2 = gris(c[-1])
    ca, cb = corr(g2, gris(f"hojas/_flow1k/{k}_a.jpg")), corr(g2, gris(f"hojas/_flow1k/{k}_b.jpg"))
    ok = (ca > cb) == (v == "a")
    shutil.move(c[-1], f"hojas/{k}_a.jpg")
    print(f"{k:20s} 2K {Image.open(f'hojas/{k}_a.jpg').size}  corr a={ca:.2f} b={cb:.2f}  {'OK' if ok else '¡NO ES LA ELEGIDA!'}")
