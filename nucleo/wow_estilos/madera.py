# -*- coding: utf-8 -*-
"""ESTILO «madera» (madera y pergamino) del kit de Crónicas de Warcraft — motor. API: nucleo/mg_wow_estilos.py.

Sustituye al «holograma» arcano (regla del usuario, 25-nov-2026, `wow_ruta_profesiones`: «esa animación está buena y los
efectos, pero el color y tipo arcano creo que se sale del estilo visual… tal vez con un estilo más de pergamino, madera,
algo más del estilo actual»). Es EL MISMO motor que holograma.py (mismas piezas, misma API y las mismas animaciones: la
ficha que se abre desde una línea, los aros rúnicos que giran, los hexágonos de los íconos, el texto que se descifra, la
barra, el sello) con otra piel:
  · paleta cálida: oro viejo (bordes y brillos), ámbar (filo interior), rojo lacre (acentos) y marfil (texto);
  · el cristal azul translúcido pasa a TABLA DE MADERA oscura con veta, casi opaca, y un fino filo de pergamino;
  · letra serif (Georgia) en vez de Bahnschrift/Consolas; el descifrado usa solo letras, sin símbolos;
  · sin líneas de barrido (scanlines), sin glitch al entrar y con un brillo (bloom) más suave y cálido.
holograma.py se conserva como referencia; ningún video nuevo lo usa (mg_wow_estilos manda «holograma» aquí)."""
import os as _os

import cv2
import numpy as np
from PIL import ImageFont

_RUTA_HOLO = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "holograma.py")
_SRC = open(_RUTA_HOLO, encoding="utf-8").read()
# MAPA (el usuario, 25-nov-2026: «replicar esa animación y efectos pero conservando el mapa original… de magia pero sin el
# filtro azul, eso parece incluso futurista»): el mapa se ve CON SUS COLORES, sin rejilla y sin el temblor de glitch al
# revelarse; se quedan el haz que cae, los anillos rúnicos que pulsan, la ruta con chispas y el título que se descifra.
for _a, _b in (
        ("tex = (duo * 0.62 + orig * np.array([0.40, 0.52, 0.80], np.float32) * 0.34 + e[..., None] * c(CIAN) * 0.20) * 0.84",
         "tex = orig"),
        ("        for i in range(0, 41):\n            X = vx + vw / 2 + (i * s.W0 / 40.0 - cx) * sc",
         "        for i in range(0, 0):\n            X = vx + vw / 2 + (i * s.W0 / 40.0 - cx) * sc"),
        ("                for _ in range(int(10 * k) + 1):", "                for _ in range(0):"),
        ("objeto=None, vista=(160, 110, 1600, 890),", "objeto=None, vista=(70, 56, 1780, 968),"),
        ("borderValue=(3, 5, 20))", "borderValue=(30, 20, 12))"),
        # REGLA DEL USUARIO (25-nov-2026): «cuando muestres personajes así en tarjeta asegúrate siempre que se le vea la
        # cara». La foto se recorta desde ARRIBA (15 %), no desde el centro: en un cuerpo entero el centro es el pecho.
        ("        T = (im.height - h) // 2", "        T = int((im.height - h) * 0.15)"),
        # etiquetas de la ficha: Georgia es más ancha que Bahnschrift y se pisaban («desuellopeletería»): tamaño que quepa
        ("tq = texto(decodificar(txt, uq, g + 5 * i), 54, BLANCO, \"Bold\", glow=col, gk=1.1, track=2)",
         "tq = texto(decodificar(txt, uq, g + 5 * i), _tq(txt), BLANCO, \"Bold\", glow=col, gk=1.1, track=1)"),
        ("wq = texto(txt, 54, BLANCO, \"Bold\", glow=col, gk=1.1, track=2).w",
         "wq = texto(txt, _tq(txt), BLANCO, \"Bold\", glow=col, gk=1.1, track=1).w"),
):
    assert _a in _SRC, "madera.py: holograma.py cambió; revisar el parche: " + _a[:60]
    _SRC = _SRC.replace(_a, _b, 1)
exec(compile(_SRC, _RUTA_HOLO, "exec"), globals())

# ------------------------------------------------------------------ paleta (los nombres se conservan: el motor los usa)
CIAN = (236, 186, 92)        # oro viejo: bordes, líneas y brillos
VIOLETA = (178, 112, 52)     # ámbar: filo interior
MAGENTA = (196, 62, 44)      # rojo lacre: acentos
BLANCO = (252, 241, 214)     # marfil: texto
NOCHE = (20, 13, 8)
VIDRIO = (46, 29, 16)        # madera oscura
PERGAMINO = (226, 204, 160)
GLIFOS = "ABCDEFGHJKLMNPQRSTUVWXYZ"
# foto_holo mezcla la foto con LUT_MAPA (duotono azul del holograma): aquí, duotono cálido de pergamino
LUT_MAPA = lut([(0, (22, 13, 6)), (.40, (110, 70, 34)), (.75, (214, 176, 118)), (1, (255, 246, 222))])
LUT_GP = LUT_MAPA

# los argumentos por defecto se fijaron al ejecutar holograma.py: se rehacen con la paleta nueva
Panel.__init__.__defaults__ = (28, CIAN, VIOLETA)
Tarjeta.__init__.__defaults__ = (None, None, None, 640, (CIAN, VIOLETA, MAGENTA, (120, 170, 70)))
Rotulo.__init__.__defaults__ = (None, 100, MAGENTA)
COLS = [(214, 70, 52), (236, 186, 92), (92, 128, 170), (120, 170, 70), (170, 104, 160), (226, 138, 52)]

_texto_holo = texto
_AZULES = {(200, 240, 255): (236, 214, 170), (150, 235, 255): (236, 214, 170)}


def texto(s, tam, color=BLANCO, var="Bold", glow=CIAN, gk=0.9, mono=False, track=0, gr=None):
    """El texto de holograma con color marfil en vez de los azules fijos y la mitad de halo (sin neón)."""
    color = _AZULES.get(tuple(color), color) if color is not None else color
    return _texto_holo(s, tam, color, var, glow, gk * .45, mono, track, gr)


def fuente(tam, var="Bold", mono=False):
    k = (tam, var, mono)
    if k not in _F:
        serif_b = "C:/Windows/Fonts/georgiab.ttf"
        serif = "C:/Windows/Fonts/georgia.ttf"
        _F[k] = ImageFont.truetype(serif if var in ("Regular", "Light") and not mono else serif_b, tam)
    return _F[k]


# ------------------------------------------------------------------ tabla de madera (en lugar del cristal)
def _veta(h, w):
    rng = np.random.default_rng(7)
    ys = np.arange(h, dtype=np.float32)[:, None]
    xs = np.arange(w, dtype=np.float32)[None, :]
    ondas = np.sin(ys * .09 + np.sin(xs * .006) * 3.0) * .5 + np.sin(ys * .23 + xs * .004) * .25
    fino = cv2.GaussianBlur(rng.random((h, w)).astype(np.float32), (0, 0), sigmaX=9, sigmaY=.8)
    fino = (fino - fino.mean()) / (fino.std() + 1e-6)
    v = .5 + .22 * ondas + .10 * fino
    return np.clip(v, 0, 1).astype(np.float32)


_VETA = _veta(H, W)


def vidrio(F, x, y, w, h, ch, op, tinte=VIDRIO):
    """Tabla de madera oscura con veta (casi opaca) y filo de pergamino; misma firma que el cristal de holograma."""
    x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    if w < 2 or h < 2 or op <= 0.003:
        return
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, F.shape[1]), min(y + h, F.shape[0])
    if x0 >= x1 or y0 >= y1:
        return
    roi = F[y0:y1, x0:x1]
    m = mascara_chaflan(w, h, ch)[y0 - y:y1 - y, x0 - x:x1 - x] * op * 0.97
    veta = _VETA[y0:y1, x0:x1]
    gy = np.linspace(1.12, .78, h, dtype=np.float32)[y0 - y:y1 - y][:, None]
    val = c(tinte)[None, None, :] * (.62 + .9 * veta * gy)[..., None]
    # filo de pergamino de 5 px por dentro del borde
    dentro = np.zeros((h, w), np.float32)
    if w > 12 and h > 12:                      # al abrirse el panel mide pocos px: sin filo hasta que quepa
        dentro[5:h - 5, 5:w - 5] = mascara_chaflan(w - 10, h - 10, max(0, ch - 4))
    filo = np.clip(mascara_chaflan(w, h, ch) - dentro, 0, 1)[y0 - y:y1 - y, x0 - x:x1 - x]
    val = val * (1 - filo[..., None]) + c(PERGAMINO)[None, None, :] * .85 * filo[..., None]
    roi *= (1 - m)[..., None]
    if F.shape[2] == 4:
        roi[..., :3] += val * m[..., None]
        roi[..., 3] += m
    else:
        roi += val * m[..., None]


def glitch_spr(sp, k, seed):
    """Sin glitch: la entrada la hacen la apertura del panel y el descifrado del texto."""
    return sp


def _fondo():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W / 2) / W) ** 2 + ((ys - H / 2) / H) ** 2)
    base = c(NOCHE)[None, None, :] + (np.clip(1 - d * 1.6, 0, 1) ** 2)[..., None] * c((70, 46, 22))
    return (base * (.75 + .5 * _VETA[..., None])).astype(np.float32)


def _post():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W / 2) / (W / 2)) ** 2 + ((ys - H / 2) / (H / 2)) ** 2)
    return np.clip(1.04 - 0.22 * d ** 2.4, 0.66, 1.0).astype(np.float32)[..., None]


FONDO = _fondo()
POST = _post()


def _componer(s):
    """Igual que holograma, con el brillo más suave y cálido (sin halo de neón)."""
    for k in (0, 1, 2, 3):
        for fn in s.capas[k]:
            fn(s.F)
    h, w = s.F.shape[:2]
    T = s.luz * .8 + s.Lu.astype(np.float32) / 255.0
    sm = cv2.resize(T, (max(1, w // 4), max(1, h // 4)), interpolation=cv2.INTER_AREA)
    b = cv2.GaussianBlur(sm, (0, 0), 2.2) * .55 + cv2.GaussianBlur(sm, (0, 0), 8.0) * .30
    L = T + cv2.resize(b, (w, h), interpolation=cv2.INTER_LINEAR)
    s.F[..., :3] += L
    s.F[..., 3] = np.minimum(1.0, s.F[..., 3] + L.max(-1))
    for fn in s.capas[5]:
        fn(s.F)
    return s.F


Ctx.componer = _componer

_disco_holo = disco


def disco(F, cx, cy, r, col, op):
    """El disco violeta oscuro del sello pasa a madera quemada."""
    return _disco_holo(F, cx, cy, r, (40, 22, 10) if tuple(col) == (34, 8, 46) else col, op)


def _tq(txt, ancho=226):
    """Tamaño de la etiqueta de un ícono de la ficha (≤ 46 px) para que quepa en su columna de 250 px."""
    tam = 46
    while tam > 24 and fuente(tam).getlength(txt) + len(txt) > ancho:
        tam -= 2
    return tam
