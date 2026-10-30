# -*- coding: utf-8 -*-
"""El Jefe como canadiense de South Park: foto recortada cuya parte de arriba de la cabeza sube y baja como bisagra a la altura de la boca,
movida por la amplitud de su voz; cuerpo casi quieto, brinquitos. Es un recorte movido por código, no un deepfake. Doc: docs/estilo_jefe_robots.md § «El Jefe».

  python nucleo/jefe_canadiense.py propios/jefe_foto.webp propios/jefe_limpio.png      recorta (una vez; la foto y el recorte no van a git)
  from jefe_canadiense import Jefe
  j = Jefe("propios/jefe_limpio.png", boca_y=.7, bisagra_x=.33, frente_x=.57, corte=.75)
  amp = amplitud("voz/final/como_2.wav", fps=30)      # 0..1 por cuadro
  rgba = j.cuadro(amp[n], n / 30, alto=620)           # uint8 BGRA
"""
import sys

import cv2
import numpy as np


def recorte(foto, salida, caja=None):
    """Quita el fondo con rembg y deja cabeza y hombros. caja = (x0, y0, x1, y1) en fracciones de la foto, antes de recortar el fondo."""
    from PIL import Image
    from rembg import new_session, remove
    im = Image.open(foto).convert("RGB")
    if caja:
        w, h = im.size
        im = im.crop((int(caja[0] * w), int(caja[1] * h), int(caja[2] * w), int(caja[3] * h)))
    sal = remove(im, session=new_session("isnet-general-use"), alpha_matting=True, alpha_matting_foreground_threshold=240, alpha_matting_background_threshold=20)
    sal = sal.crop(sal.getchannel("A").point(lambda v: 255 if v > 20 else 0).getbbox())
    sal.save(salida)
    return salida


def amplitud(wav, fps=30, suave=.45):
    """Envolvente 0..1 de la voz, un valor por cuadro: la cabeza abre con cada sílaba."""
    import soundfile as sf
    y, sr = sf.read(wav, dtype="float32", always_2d=True)
    y = y.mean(axis=1)
    paso = sr / fps
    n = max(1, int(np.ceil(len(y) / paso)))    # ceil: con una toma de largo múltiplo exacto del cuadro, el último trozo salía vacío (NaN)
    v = np.array([float(np.sqrt(np.mean(y[int(i * paso):int((i + 1) * paso)] ** 2) + 1e-9)) for i in range(n)])
    v = np.clip(v / (np.percentile(v, 96) + 1e-6), 0, 1) ** .8
    out = np.zeros_like(v)
    for i in range(1, n):                      # abre de golpe, cierra un poco más lento: se lee como habla, no como temblor
        out[i] = v[i] if v[i] > out[i - 1] else out[i - 1] * suave + v[i] * (1 - suave)
    return out


class Jefe:
    def __init__(self, png, boca_y=.62, bisagra_x=.14, frente_x=.86, angulo=24, corte=1.0):
        im = cv2.imread(png, cv2.IMREAD_UNCHANGED)
        im = im[:int(im.shape[0] * corte)].copy()
        azul = (im[..., 0].astype(int) > im[..., 2].astype(int) + 18) & (np.arange(im.shape[0])[:, None] > im.shape[0] * .5)   # el agua: pasa a ser camiseta
        im[azul, :3] = (34, 30, 30)
        pelo = (im[..., :3].max(axis=2) > 95) & (np.arange(im.shape[0])[:, None] < im.shape[0] * .17)                          # brillos del fondo entre los rizos
        im[pelo, :3] = (28, 24, 24)
        self.im = im.astype(np.float32)
        self.h, self.w = im.shape[:2]
        self.by = int(boca_y * self.h)
        self.hx = int(bisagra_x * self.w)
        self.fx = int(frente_x * self.w)
        self.ang = angulo

    def _lienzo(self, abre):
        """La cabeza abierta a tamaño de la foto, con margen arriba para que quepa la tapa levantada. Devuelve BGRA float."""
        w, h, by, hx = self.w, self.h, self.by, self.hx
        m = int(h * .42)
        L = np.zeros((h + m, w, 4), np.float32)
        y0 = by + m
        # lo de abajo: mandíbula, cuello y hombros, fijo
        L[y0:] = self.im[by:]
        # el hueco de la boca: oscuro, entre la línea fija y la tapa
        a = -self.ang * float(np.clip(abre, 0, 1))
        rad = np.deg2rad(-a)
        px = self.fx - hx
        tope = (self.fx, int(y0 - np.sin(rad) * px) - 5)     # 5 px de más: que no se vea el fondo entre la tapa y el hueco
        interior = np.zeros(L.shape[:2], np.uint8)
        cv2.fillPoly(interior, [np.array([(hx, y0), (self.fx, y0 + 2), tope], np.int32)], 255, cv2.LINE_AA)
        interior = cv2.GaussianBlur(interior, (0, 0), 1.2).astype(np.float32) / 255
        for c, v in enumerate((16, 12, 58)):       # BGR: rojo muy oscuro
            L[..., c] = L[..., c] * (1 - interior) + v * interior
        L[..., 3] = np.maximum(L[..., 3], interior * 255)
        # la tapa: lo de arriba de la boca, girado sobre la bisagra
        arriba = np.zeros_like(L)
        arriba[m:y0] = self.im[:by]
        M = cv2.getRotationMatrix2D((float(hx), float(y0)), -a, 1.0)
        arriba = cv2.warpAffine(arriba, M, (L.shape[1], L.shape[0]), flags=cv2.INTER_LINEAR, borderValue=(0, 0, 0, 0))
        al = arriba[..., 3:] / 255
        L[..., :3] = arriba[..., :3] * al + L[..., :3] * (1 - al)
        L[..., 3] = arriba[..., 3] + L[..., 3] * (1 - al[..., 0])
        return L

    def cuadro(self, abre, t, alto=640):
        """BGRA uint8, alto en píxeles de lo que ocupa la foto (la tapa levantada se sale por arriba). Brinquito suave mientras habla."""
        L = self._lienzo(abre)
        k = alto / self.h
        L = cv2.resize(L, (int(L.shape[1] * k), int(L.shape[0] * k)), interpolation=cv2.INTER_AREA)
        return np.clip(L, 0, 255).astype(np.uint8)


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        print(recorte(sys.argv[1], sys.argv[2], (.22, .24, .98, 1.0)))
