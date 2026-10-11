# -*- coding: utf-8 -*-
import cv2, numpy as np, docu as D, docu_fx as X
from motor import W, H
def gr(t): return None
def guardar(nombre, cuadros):
    hoja = np.vstack([np.hstack(cuadros[i:i + 2]) for i in range(0, len(cuadros), 2)])
    hoja = cv2.resize(hoja, (1920, int(1920 * hoja.shape[0] / hoja.shape[1])), interpolation=cv2.INTER_AREA)
    cv2.imwrite(f"previews/{nombre}.jpg", cv2.cvtColor((np.clip(hoja, 0, 1) * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])

def a1(t):
    lz = np.zeros((H, W, 3), np.float32)
    X.clip_bg(lz, "pluma", t, 6, 1.0, z0=1.05, z1=1.2, tono=(0.75, 0.68, 0.6))
    D.franja_texto = None
    pal = X.titular([("Nadie", 0.2), ("ha", 0.45), ("podido", 0.7), ("leerlo", 1.0)], W / 2, 800, 150, clave=[3], lineas=(2,))
    X.slam(lz, pal, t)
    cap = X.titular([("Cuando", 0.3), ("de", 0.5), ("pronto,", 0.7), ("ve", 1.0), ("algo", 1.2), ("que", 1.4), ("no", 1.6), ("entiende", 1.8)], W / 2, 300, 42, fnt="pop_sbi", lineas=(3,))
    X.caption(lz, cap, t)
    return D.acabado(lz, t)
def a2(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, D.ruta_img("f187") if False else "beinecke_interior", t, 6, 1.05, 1.2, par=(60, 10), tono=(0.7, 0.7, 0.7))
    X.linea_medida(lz, (300, 700), (1620, 640), D.e_out(D.prog(t, 0.2, 1.6)), "240 páginas", t, 1.0)
    X.elipse_luz(lz, 1400, 320, 260, 130, D.prog(t, 0.3, 1.6))
    return D.acabado(lz, t)
def a3(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, "friedman", t, 6, 1.05, 1.25, (0.32, 0.42), (0.34, 0.36), par=(60, 10))
    sp = X.recorte_borde("imagenes/recortes/voynich_retrato.png")
    D.pegar(lz, sp, D.poner(sp.w, sp.h, 1400, 560, 0.8, 4))
    est = X.estampilla("kircher", "1665")
    D.pegar(lz, est, D.poner(est.w, est.h, 420, 330, 0.9, -6))
    sc = X.sello_circular("Manuscrito", "MS 408", "Yale University")
    D.pegar(lz, sc, D.poner(sc.w, sc.h, 470, 800, 0.6, -14), 0.95)
    return D.acabado(lz, t)
def a4(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, D.ruta_img("f187"), t, 6, 1.6, 1.8, (0.4, 0.3), (0.5, 0.4), par=(0, 0), tono=(0.9, 0.9, 0.86), lado=3800) if False else D.foto_parallax(lz, "folios_hd/f187", t, 6, 1.6, 1.8, (0.4, 0.3), (0.5, 0.4), par=(0, 0), lado=3800)
    X.resaltador(lz, 300, 440, 1100, 500, D.prog(t, 0.2, 1.4))
    X.resaltador(lz, 500, 640, 1400, 700, D.prog(t, 0.9, 2.0), semilla=2)
    return D.acabado(lz, t)
cu = [a1(1.6), a2(1.8), a3(1.5), a4(1.9)]
guardar("fx_a", cu)
# transiciones
A = a1(2.0); B = a3(1.5)
tr = [X.mezcla2(A, B, p, k, 3) for k, p in (("tinta", 0.33), ("destello", 0.5), ("aberracion", 0.5), ("glitch", 0.35), ("zoom", 0.5), ("tinta", 0.62))]
guardar("fx_b", tr)
print("ok")
