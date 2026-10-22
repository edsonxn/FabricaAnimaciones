# -*- coding: utf-8 -*-
"""Coreografía (2/4) de «La historia de Aguascalientes»: la colonia (San Marcos y la boda de 1621, la parroquia de 1738 que hoy es la
Catedral, el Palacio de Gobierno de 1665 y los murales de Osvaldo Barra, Real de Asientos y sus túneles, el Cristo negro del Encino),
las aguas (el charco, la carta de 1808 que nadie contestó, los Baños de Ojocaliente de 1831, Los Arquitos de 1821), la Feria de San
Marcos (1828, el terreno de 168 × 88 m, el jardín y su balaustrada, 8 millones de visitantes) y el beso (1835, Santa Anna y la
leyenda, el decreto, el escudo de 1946, Elías L. Torres en 1927, 1848 y 1857, la exposición del INAH en 2025).
Dibujos = pegatinas de Flow; fotos = FotoPeg. sem 300-599. Capas de terreno 10-19 (se limpian al salir de cada escena).
Código visual de la escena «beso»: sello morado «LEYENDA» (y rótulos en gris) para el cuento; sello verde «HECHO» para lo documentado."""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import foto_peg as FP
import mapa as M
import obj_a as A
import obj_c as C
from boceto import ROJO, Dib, R as RC, T as TT, linea
from core import FIN, INI, T
from coreo_peg import grupo_ciclo, ciclo_pant
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo, tramo
from motor import e_inout, prog
from obj_base import PIEDRA, forma, rect
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (números de piezas/<hoja>/_indice.jpg)
PL = lambda n, **k: P("02_plata_hoja", n, **k)          # 1 soldado arcabuz, 4 minero, 7 plata
FU = lambda n, **k: P("03_fundacion_hoja", n, **k)      # 0 oidor, 1 colono, 2 colona, 3 carta con sello, 4 poza termal, 5 jacal, 7 estandarte
CO = lambda n, **k: P("04_colonia_hoja", n, **k)        # 0 catedral, 1 palacio, 2 San Marcos, 3 cura, 4 novios, 5 mina, 6 túnel, 7 Cristo, 8 vaca, 9 vacas, 10 vaquero
XI = lambda n, **k: P("05_xix_hoja", n, **k)            # 0 Santa Anna, 1 dama, 2 caballero, 3 baños, 4 tina, 5 cadena, 6 escudo labios, 7 puesto, 8 jardín
AR = lambda n, **k: P("06_arte_hoja", n, **k)           # 5 pintor
PO = lambda n, **k: P("07_porfiriato_hoja", n, **k)     # 9 arquitecto / ingeniero
SX = lambda n, **k: P("09_sigloxx_hoja", n, **k)        # 4 uvas
TU = lambda n, **k: P("10_turismo_hoja", n, **k)        # 0 turista, 1 familia, 2 tina con pato, 3 mariachi, 4 rueda de la fortuna
C_SOLD = ciclo("12_soldado_marcha")

ARQUITOS = (-102.2865, 21.8890)        # baños de Los Arquitos (aprox., junto a la Alameda)
LEY_COL = (120, 90, 160)               # morado de «LEYENDA» (el mismo del sello de coreo_1)
HECHO_COL = (52, 128, 84)              # verde de «HECHO»
GRIS_LEY = 165                         # tinta gris de los rótulos de la leyenda
ESQ = (1640, 385)                      # pies del sello LEYENDA/HECHO (arriba a la derecha, bajo la fila de sellos)

_SEM = iter(range(300, 600))


def S():
    return next(_SEM)


def foco(lon, lat, z, dy=120):
    """Clave de cámara que deja (lon, lat) ~dy px por DEBAJO del centro (los dibujos crecen hacia arriba)."""
    return lon, lat + dy / (640.0 * z * 1.07), z


# ------------------------------------------------------------------ piezas dibujadas por código (primitivas)
@lru_cache(maxsize=64)
def _mascaras_sello(txt, px, rot):
    f = ImageFont.truetype("C:/Windows/Fonts/georgiab.ttf", px)
    bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pad = int(px * 0.42)
    w, h = tw + 2 * pad, th + 2 * pad
    n = int(math.hypot(w, h)) + 8
    tinta = Image.new("L", (n, n), 0)
    papel = Image.new("L", (n, n), 0)
    x0, y0 = (n - w) // 2, (n - h) // 2
    d = ImageDraw.Draw(tinta)
    g = max(3, int(px * 0.09))
    d.rounded_rectangle((x0, y0, x0 + w, y0 + h), radius=int(px * 0.22), outline=255, width=g)
    d.rounded_rectangle((x0 + g + 4, y0 + g + 4, x0 + w - g - 4, y0 + h - g - 4), radius=int(px * 0.16), outline=255, width=max(1, g // 3))
    d.text((x0 + pad - bb[0], y0 + pad - bb[1]), txt, font=f, fill=255)
    ImageDraw.Draw(papel).rounded_rectangle((x0 - 6, y0 - 6, x0 + w + 6, y0 + h + 6), radius=int(px * 0.26), fill=255)
    Mr = cv2.getRotationMatrix2D((n / 2, n / 2), math.degrees(rot), 1.0)
    t = cv2.warpAffine(np.asarray(tinta, np.uint8), Mr, (n, n), flags=cv2.INTER_LINEAR)
    p = cv2.warpAffine(np.asarray(papel, np.uint8), Mr, (n, n), flags=cv2.INTER_LINEAR)
    ys, xs = np.nonzero(p)
    return t[ys.min():ys.max() + 1, xs.min():xs.max() + 1], p[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


class SelloTxt:
    """Sello de goma con texto (LEYENDA / HECHO) en un color propio, como pegatina: pies en (x, y), s escala el tamaño de letra."""

    def __init__(self, txt, color, px=58, rot=0.12):
        self.txt, self.color, self.px, self.rot = txt, color, px, rot

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fase_=0, semilla=0, ancho=1.0, sq=0.0, lapiz=0.0, tv=None,
                vida=1.0, peg=True):
        px = int(self.px * s)
        if px < 8 or u <= 0:
            return
        tinta, papel = _mascaras_sello(self.txt, px, round(self.rot + rot, 2))
        x0, y0 = x - tinta.shape[1] / 2, y - tinta.shape[0]
        if peg:
            hoja.peg_mascara(papel, x0, y0)
        hoja.sello(tinta, x0, y0, self.color, 240, 0.10, semilla)


LEYENDA = SelloTxt("LEYENDA", LEY_COL)
HECHO = SelloTxt("HECHO", HECHO_COL, rot=-0.08)
LEYENDA_GRANDE = SelloTxt("LEYENDA", LEY_COL, px=112, rot=0.22)


@lru_cache(maxsize=None)
def columna():
    ops = forma(rect(-48, -24, 48, 0, 4), PIEDRA, 5, peso=0.3, sp=7)
    ops += forma(rect(-30, -330, 30, -22, 3), PIEDRA, 5, peso=0.5, sp=8)
    ops += forma(rect(-50, -356, 50, -326, 4), PIEDRA, 5, peso=0.3, sp=7)
    ops += [TT(linea((-12, -318), (-12, -34)), 3.2, peso=0.05), TT(linea((12, -318), (12, -34)), 3.2, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def corazon():
    t = np.linspace(0, 2 * math.pi, 48)
    Pc = np.stack([16 * np.sin(t) ** 3, -(13 * np.cos(t) - 5 * np.cos(2 * t) - 2 * np.cos(3 * t) - np.cos(4 * t))], 1) * 5.0
    Pc[:, 1] -= Pc[:, 1].max()
    return Dib(forma(Pc, ROJO, 5.5, peso=0.4, sp=6, cerrada=False))


@lru_cache(maxsize=None)
def terreno_168x88():
    """Rectángulo del terreno de 1831 (168 × 88 m, proporción real), con pasto de crayón."""
    Pr = rect(-380, -398, 380, 0, 6)
    return Dib([TT(Pr, 7, peso=0.7), RC(Pr, (168, 200, 120), peso=0.5, sp=14)])


@lru_cache(maxsize=None)
def tachon():
    return Dib([TT(linea((-190, -30), (190, -120)), 13, peso=0.18), TT(linea((-180, -120), (185, -25)), 13, peso=0.18)])


@lru_cache(maxsize=None)
def flecha_curva(w=430, h=120):
    u = np.linspace(0, 1, 24)[:, None]
    A_, C_, B_ = np.array([-w / 2, 0.0]), np.array([0.0, -h]), np.array([w / 2, 0.0])
    Pf = (1 - u) ** 2 * A_ + 2 * (1 - u) * u * C_ + u ** 2 * B_
    d = Pf[-1] - Pf[-3]
    a = math.atan2(d[1], d[0])
    cab = [TT(linea(tuple(B_), (B_[0] - 34 * math.cos(a + s_ * 0.5), B_[1] - 34 * math.sin(a + s_ * 0.5))), 7, peso=0.05) for s_ in (-1, 1)]
    return Dib([TT(Pf, 7, peso=0.5)] + cab)


def cron(t0, vel=1.6):
    return lambda t: C.cronometro(round(((t - t0) * vel) % 1.0 * 2 * math.pi, 1))


def vela(t):
    return C.vela(round(0.88 + 0.12 * math.sin(t * 11.0), 2))


def limpiar(R, t, capas):
    for c in capas:
        R.terreno(t, None, (0, 0, 0), 0.3, capa=c)


def construir(R):
    _colonia(R)
    _aguas(R)
    _feria(R)
    _beso(R)


def cortes(R):
    pass


# ------------------------------------------------------------------ COLONIA
def _colonia(R):
    e = "colonia"
    i0, fin = INI(e), FIN(e)
    t_nac, t_pue, t_sm, t_reg, t_boda, t_1621 = (T(e, "nacio"), T(e, "pueblo", frase=0), T(e, "san marcos"), T(e, "registro"),
                                                 T(e, "boda"), T(e, "1621"))
    t_par, t_asu, t_1738, t_hoy1, t_cat, t_pla = (T(e, "parroquia", frase=1), T(e, "asuncion"), T(e, "1738"), T(e, "hoy", frase=1),
                                                  T(e, "catedral"), T(e, "plaza"))
    t_cas, t_rin, t_1665, t_pal = T(e, "casona"), T(e, "rincon"), T(e, "1665"), T(e, "palacio")
    t_ent, t_mur, t_osv = T(e, "entra"), T(e, "murales"), T(e, "osvaldo")
    t_nor, t_min, t_cre, t_real = T(e, "norte"), T(e, "mineria"), T(e, "crecer"), T(e, "real")
    t_par5, t_1705, t_tun, t_agua, t_hoy5, t_pm = (T(e, "parroquia", frase=5), T(e, "1705"), T(e, "tuneles"), T(e, "agua", frase=5),
                                                   T(e, "hoy", frase=5), T(e, "pueblo magico"))
    t_bar, t_enc, t_cri, t_neg = T(e, "barrio"), T(e, "encino"), T(e, "cristo"), T(e, "negro")
    t_ley, t_cre7, t_col, t_finm = T(e, "leyenda"), T(e, "creciendo"), T(e, "columna"), T(e, "fin del mundo")
    sm, pp, ra, en = CI["san_marcos"], CI["plaza_patria"], CI["real_asientos"], CI["encino"]

    # cámara: la villa y San Marcos -> la plaza -> el palacio -> vuelo al norte (Real de Asientos) -> el Encino
    R.camara(i0 - 0.2, *foco(-102.297, 21.880, 4.6))
    R.camara(t_sm, *foco(-102.301, 21.879, 5.3))
    R.camara(t_par - 0.4, *foco(-102.299, 21.8805, 5.6))
    R.camara(t_cat, *foco(-102.2965, 21.8815, 6.0))
    R.camara(t_pal, *foco(-102.2955, 21.8815, 6.1))
    R.camara(t_nor - 0.2, *foco(-102.2945, 21.882, 6.4))
    R.camara(t_min, *foco(-102.19, 22.06, 2.7))
    R.camara(t_real + 0.3, *foco(-102.09, 22.236, 3.6))
    R.camara(t_par5, *foco(-102.088, 22.236, 3.8))
    R.camara(t_hoy5, *foco(-102.086, 22.238, 3.9))
    R.camara(t_bar - 0.1, *foco(-102.087, 22.237, 4.1))
    R.camara(t_enc, *foco(-102.2915, 21.8763, 5.2))
    R.camara(fin + 0.3, *foco(-102.2915, 21.8763, 5.7))

    R.terreno(i0 - 0.1, "nueva_galicia", COL["nueva_galicia"], 1.0, capa=10)

    # frase 0: la villa y, al poniente, el pueblo de indios de San Marcos (boda de 1621)
    ga(R, FU(5), pp, i0, t_par, s=0.30, off=(250, 30), sem=S(), zs=0.4, z=1)
    ga(R, FU(5), pp, i0 + 0.15, t_par, s=0.26, off=(400, 50), sem=S(), zs=0.4, z=1, flip=True)
    ciudad(R, i0 + 0.2, t_sm - 0.1, "aguascalientes", "LA VILLA", "abajo", 40)
    ga(R, CO(2), sm, t_nac - 0.1, t_par, s=0.42, off=(-300, 40), sem=S(), zs=0.4, z=2, extra=[(0.05, "crece", 0.35, {"dur": 0.8})])
    for k, (dx, dy) in enumerate(((-480, 60), (-150, 70), (-420, -40))):
        ga(R, FU(5), sm, t_pue - 0.1 + 0.12 * k, t_par, s=0.22, off=(dx, dy), sem=S(), zs=0.4, z=1, flip=k % 2 == 1)
    lugar(R, t_sm, t_par - 0.1, "SAN MARCOS", sm, off=(-300, 100), px=42)
    titulo(R, t_sm - 0.1, t_1621 + 1.3, "PUEBLO DE INDIOS", px=74, snd=True)
    pa(R, CO(3), 1290, 1010, 1.0, t_reg - 0.15, t_par, sem=S(), flip=True)
    pa(R, CO(4), 1590, 1010, 0.95, t_boda - 0.15, t_par, sem=S(), extra=[(0.1, "campana", 0.4, {"dur": 2.4})])
    R.texto(t_boda + 0.2, t_par - 0.1, "BODA · 1621", (1470, 380), px=50, d=0.5)
    R.anio(t_1621, 1621)

    # frase 1: la parroquia de la Asunción (1738), hoy Catedral en la Plaza de la Patria
    ga(R, CO(0), pp, t_par - 0.1, t_nor, s=0.52, off=(-210, 140), sem=S(), zs=0.4, z=2, entra="sube", dy=280,
       extra=[(0.05, "crece", 0.4, {"dur": 0.9})])
    titulo(R, t_par, t_hoy1 - 0.2, "PARROQUIA DE LA ASUNCIÓN", px=70, snd=True)
    pa(R, CO(3), 330, 1010, 1.0, t_par + 0.1, t_hoy1 - 0.3, sem=S())
    pa(R, FU(7), 1600, 1010, 0.95, t_asu - 0.15, t_hoy1 + 0.4, sem=S())
    R.anio(t_1738, 1738)
    pa(R, FP.F("colonia_1"), 330, 1000, FP.s_para(0.52), t_hoy1 - 0.1, t_hoy1 + 4.5, entra="pluma", sem=S())
    titulo(R, t_hoy1, t_cas - 0.2, "HOY: LA CATEDRAL", px=70)
    ciudad(R, t_pla - 0.1, t_cas - 0.1, "plaza_patria", "PLAZA DE LA PATRIA", "der", 40)

    # frase 2: la casona de los Rincón Gallardo (1665) -> Palacio de Gobierno
    ga(R, CO(1), pp, t_cas - 0.1, t_nor, s=0.36, off=(250, 140), sem=S(), zs=0.4, z=2, extra=[(0.05, "pop", 0.4)])
    pa(R, FU(0), 330, 1010, 1.0, t_rin - 0.2, t_ent - 0.3, sem=S())
    R.texto(t_rin, t_pal - 0.1, "FAMILIA RINCÓN GALLARDO", (360, 560), px=40, d=0.5)
    R.anio(t_1665, 1665)
    titulo(R, t_pal - 0.1, t_ent - 0.2, "PALACIO DE GOBIERNO", px=76, snd=True)

    # frase 3: entra al patio: los murales de Osvaldo Barra (se puede visitar)
    pa(R, TU(0), lambda t: 300 + 220 * e_inout(prog(t, t_ent, t_ent + 2.2)), lambda t: 1010, 0.95, t_ent - 0.15, t_nor, sem=S(),
       extra=[(0.05, "pasos", 0.3, {"dur": 1.6})])
    pa(R, FP.F("colonia_3"), 1440, 1000, FP.s_para(0.47), t_mur - 0.1, t_mur + 4.4, entra="pluma", sem=S())
    titulo(R, t_ent, t_osv - 0.5, "HOY: PATIO DEL PALACIO DE GOBIERNO", px=58)
    R.texto(t_ent + 0.4, t_osv - 0.5, "entrada libre", (960, 296), px=48, d=0.4)
    ciudad(R, t_ent, t_nor, "plaza_patria", None)
    titulo(R, t_osv, t_nor - 0.15, "MURALES DE OSVALDO BARRA (CHILE)", px=58)

    # frase 4: al norte, la minería y Real de Asientos
    R.ruta([CI["aguascalientes"], (-102.24, 21.98), (-102.17, 22.10), ra], t_nor - 0.1, 1.6, ancho=5.0, t1=t_tun, flecha=True)
    ga(R, CO(5), ra, t_min - 0.1, t_bar, s=0.42, off=(-40, -20), sem=S(), zs=0.4, z=2, entra="sube", dy=260)
    pa(R, PL(4), 330, 1010, 1.0, t_min - 0.15, t_par5 - 0.25, sem=S(), extra=[(0.1, "clink", 0.4)])
    ga(R, PL(7), ra, t_cre, t_bar, s=0.22, off=(190, 30), sem=S(), zs=0.4, z=3, extra=[(0.05, "brillo", 0.3)])
    for k, (dx, dy) in enumerate(((-260, 40), (150, -60), (-220, -70))):
        ga(R, FU(5), ra, t_cre + 0.1 + 0.15 * k, t_bar, s=0.2, off=(dx, dy), sem=S(), zs=0.4, z=1, flip=k == 1)
    ciudad(R, t_real - 0.1, t_bar, "real_asientos", "REAL DE ASIENTOS", "abajo", 42)

    # frase 5: la parroquia de 1705, los túneles con agua (se recorren con guía), Pueblo Mágico
    R.anio(t_1705, 1705)
    pa(R, FP.F("colonia_5"), 430, 1000, FP.s_para(0.46), t_par5 - 0.1, t_par5 + 4.5, entra="pluma", sem=S())
    pa(R, CO(6), 1540, 1000, 0.95, t_tun - 0.15, t_bar, sem=S(), entra="sube", dy=320)
    R.snd(t_agua - 0.2, "agua_tunel", 0.4)
    R.texto(t_tun + 0.4, t_hoy5 - 0.1, "TÚNELES · SIGLO XVIII", (1540, 560), px=44, d=0.5)
    pa(R, TU(0), 360, 1010, 0.95, t_hoy5 - 0.1, t_bar, sem=S())
    titulo(R, t_hoy5, t_pm - 0.15, "HOY: TÚNELES CON GUÍA", px=72)
    titulo(R, t_pm - 0.1, t_bar + 0.5, "PUEBLO MÁGICO", px=100, snd=False)
    R.snd(t_pm, "pluck", 0.4)

    # frase 6: el Cristo negro del Encino
    pa(R, FU(2), 360, 1010, 1.0, t_bar - 0.15, fin + 0.3, sem=S(), extra=[(0.05, "pasos", 0.25, {"dur": 1.0})])
    ciudad(R, t_enc - 0.1, t_ley - 0.1, "encino", None)
    titulo(R, t_enc - 0.1, t_ley - 0.2, "BARRIO DEL ENCINO", px=74)
    cr = t_cri - 0.15
    R.act(CO(7), pos=lambda t: (900, 1010, 1.08 + 0.2 * e_inout(prog(t, t_cre7, t_col + 0.3))), t_in=cr, d_in=0.5, entra="sube", dy=320,
          sem=S(), z=2)
    R.texto(t_neg - 0.1, t_ley - 0.1, "CRISTO NEGRO", (900, 520), px=50, d=0.5)
    pa(R, CO(3), 1600, 1010, 0.95, t_neg, fin + 0.3, sem=S(), flip=True)

    # frase 7: la leyenda (crece; si toca la columna, el fin del mundo)
    pa(R, LEYENDA, ESQ[0], ESQ[1], 1.0, t_ley - 0.05, fin + 0.3, sem=S(), extra=[(0.0, "sello", 0.45)])
    R.snd(t_ley + 0.5, "latido", 0.35, dur=3.0)
    R.snd(t_cre7, "crece", 0.4, dur=2.4)
    pa(R, columna(), 1135, 1010, 1.3, t_col - 0.3, fin + 0.3, sem=S())
    titulo(R, t_finm - 0.1, fin + 0.3, "¿EL FIN DEL MUNDO?", px=84)
    R.snd(t_finm, "trueno", 0.3)
    limpiar(R, fin + 0.35, (10,))


# ------------------------------------------------------------------ AGUAS
def _aguas(R):
    e = "aguas"
    i0, fin = INI(e), FIN(e)
    t_cha, t_1808, t_due, t_hac, t_per, t_vir, t_nun = (T(e, "charco"), T(e, "1808", frase=1), T(e, "dueno"), T(e, "hacienda"),
                                                        T(e, "permiso"), T(e, "virrey"), T(e, "nunca"))
    t_est, t_ind = T(e, "estallo"), T(e, "independencia")
    t_gui, t_1808b, t_ban3, t_abr, t_1831 = T(e, "guias"), T(e, "1808", frase=3), T(e, "banos", frase=3), T(e, "abrieron"), T(e, "1831")
    t_sig, t_200, t_des, t_tina, t_mis, t_nom = (T(e, "siguen"), T(e, "200"), T(e, "despues", frase=4), T(e, "tina"), T(e, "mismo"),
                                                 T(e, "nombre"))
    t_arq, t_1821, t_ali, t_hoy, t_cc = T(e, "arquitos"), T(e, "1821"), T(e, "alimentados"), T(e, "hoy", frase=5), T(e, "centro cultural")
    oj = CI["ojocaliente"]
    ruta_mx = tramo(M.RUTAS["camino_plata"], CI["aguascalientes"], CI["ciudad_mexico"])

    R.camara(i0 - 0.2, *foco(-102.274, 21.8795, 5.4))
    R.camara(t_due, *foco(-102.272, 21.8795, 5.8))
    R.camara(t_per - 0.2, *foco(-102.27, 21.875, 4.6))
    R.camara(t_vir + 0.4, -101.62, 21.17, 0.95)
    R.camara(t_ind, -101.66, 21.20, 0.92)
    R.camara(t_1808b, -101.70, 21.24, 0.98)
    R.camara(t_ban3 - 0.4, *foco(-102.272, 21.8795, 5.0))
    R.camara(t_sig, *foco(-102.2725, 21.8795, 5.5))
    R.camara(t_arq - 0.2, *foco(-102.276, 21.882, 5.6))
    R.camara(fin + 0.3, *foco(-102.279, 21.884, 5.9))

    R.terreno(t_per - 0.2, "aguascalientes", COL["territorio"], 1.0, capa=10)
    R.terreno(t_ban3 - 0.5, None, COL["territorio"], 0.5, capa=10)

    # frase 0: el charco caliente seguía ahí
    ga(R, FU(4), oj, i0 - 0.05, t_per, s=0.42, off=(-110, -25), sem=S(), zs=0.4, z=2, entra="sube", dy=260,
       extra=[(0.1, "agua_termal", 0.4)])
    pa(R, FU(1), 330, 1010, 1.0, i0 + 0.3, t_due - 0.25, sem=S())
    ciudad(R, t_cha - 0.1, t_per - 0.2, "ojocaliente", "OJOCALIENTE", "abajo", 42)
    titulo(R, t_cha - 0.1, t_1808 - 0.2, "EL CHARCO CALIENTE", px=80, snd=True)

    # frase 1: 1808: el hacendado escribe al virrey… y nadie contesta
    R.anio(t_1808, 1808)
    pa(R, XI(2), 330, 1010, 1.0, t_due - 0.15, t_est, sem=S(), sale="baja")
    R.texto(t_hac, t_vir - 0.1, "EL HACENDADO", (330, 560), px=44, d=0.4)
    pa(R, FU(3), 640, 1000, 0.6, t_per - 0.2, t_vir + 0.1, sem=S(), extra=[(0.05, "papel", 0.4)])
    R.ruta(ruta_mx, t_vir - 0.1, 2.2, ancho=5.0, t1=t_est + 0.3, flecha=True)
    R.act(FU(3), pos_geo=R.camino_pos(ruta_mx, t_vir, 2.3), off=(0, -10), s=0.42, t_in=t_vir, d_in=0.3, entra="pop", sem=S(), zs=0.4, z=3,
          t_out=t_est, sale="caer", sfx=[(0.0, "whoosh", 0.35)])
    ciudad(R, t_vir + 0.3, t_ban3 - 0.4, "ciudad_mexico", "AL VIRREY · MÉXICO", "arriba", 40)
    pa(R, cron(t_nun), 1560, 640, 0.95, t_nun - 0.1, t_est + 0.4, sem=S(), extra=[(0.05, "reloj_rapido", 0.4, {"dur": 1.6})])
    titulo(R, t_nun - 0.1, t_est - 0.1, "…Y NUNCA LE CONTESTARON", px=70)

    # frase 2: estalla la guerra de Independencia
    R.anio(t_est, 1810)
    R.sello(t_ind, "gorro", "INDEPENDENCIA", color=(74, 146, 98))
    R.terreno(t_est - 0.1, "insurgentes", COL["insurgentes"], 0.9, capa=11)
    R.terreno(t_ban3 - 0.4, None, COL["insurgentes"], 0.4, capa=11)
    ciclo_pant(R, C_SOLD, -150, 1050, 1010, t_est - 0.1, 3.2, t1=t_gui + 0.3, s=0.85, sem=S())
    R.snd(t_est, "tambor", 0.4, dur=1.6)
    R.snd(t_ind + 0.3, "canonazo", 0.4)

    # frase 3: las guías dicen 1808, pero abrieron en 1831
    pa(R, TU(0), 330, 1010, 1.0, t_gui - 0.6, t_sig - 0.1, sem=S())
    titulo(R, t_gui - 0.1, t_ban3 - 0.2, "MUCHAS GUÍAS DICEN…", px=70)
    R.texto(t_1808b - 0.1, t_1831 + 0.6, "1808", (1300, 560), px=150, d=0.4)
    pa(R, tachon(), 1300, 650, 1.0, t_ban3 - 0.3, t_1831 + 0.6, sem=S(), entra="pluma", d_in=0.45, extra=[(0.0, "garabato", 0.4)])
    ga(R, XI(3), oj, t_ban3 - 0.1, fin + 0.3, s=0.42, off=(-40, 150), sem=S(), zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "pop", 0.4)])
    titulo(R, t_abr - 0.1, t_sig - 0.15, "BAÑOS DE OJOCALIENTE · 1831", px=66, snd=True)
    R.anio(t_1831, 1831)
    R.texto(t_1831, t_sig - 0.1, "1831", (1300, 800), px=150, d=0.4)

    # frase 4: siguen abiertos (se pueden visitar): la tina de agua termal
    pa(R, FP.F("aguas_4"), 450, 1000, FP.s_para(0.46), t_sig - 0.1, t_sig + 4.6, entra="pluma", sem=S())
    titulo(R, t_sig - 0.05, t_tina - 0.6, "¡SIGUEN ABIERTOS!", px=88)
    ciudad(R, t_sig, t_arq, "ojocaliente", None)
    R.texto(t_200 - 0.1, t_tina - 0.6, "CASI 200 AÑOS", (960, 312), px=54, d=0.4)
    R.anio(t_des, 2026)
    titulo(R, t_tina - 0.5, t_arq - 0.2, "HOY: BAÑOS DE OJOCALIENTE", px=64)
    pa(R, XI(4), 1680, 1010, 0.85, t_tina - 0.25, t_hoy, sem=S(), extra=[(0.05, "burbujas", 0.35, {"dur": 1.2})])
    pa(R, TU(2), 450, 1010, 0.75, t_mis - 0.1, t_cc - 0.3, sem=S(), extra=[(0.05, "plop", 0.35)])
    R.texto(t_nom - 0.2, t_arq - 0.1, "«AGUAS CALIENTES»", (960, 312), px=46, d=0.6)

    # frase 5: Los Arquitos (1821), la misma agua, hoy centro cultural
    R.anio(t_1821, 1821)
    ga(R, XI(3), ARQUITOS, t_arq - 0.15, fin + 0.3, s=0.36, off=(480, 150), sem=S(), zs=0.4, z=2, flip=True,
       extra=[(0.05, "pop", 0.35)])
    R.ciudad(t_arq, fin + 0.2, "arquitos", ARQUITOS, None)
    lugar(R, t_arq + 0.1, t_hoy - 0.1, "LOS ARQUITOS · 1821", ARQUITOS, off=(480, 200), px=42)
    pa(R, flecha_curva(), 1000, 420, 1.0, t_ali - 0.1, fin + 0.3, sem=S(), entra="pluma", d_in=0.8,
       extra=[(0.05, "agua_termal", 0.3)])
    R.texto(t_ali + 0.4, t_hoy - 0.1, "la misma agua", (1000, 280), px=46, d=0.5)
    pa(R, AR(5), 330, 1010, 0.9, t_cc - 0.3, fin + 0.3, sem=S(), extra=[(0.05, "pincel", 0.3)])
    titulo(R, t_hoy, fin + 0.3, "HOY: CENTRO CULTURAL LOS ARQUITOS", px=60)
    limpiar(R, fin + 0.35, (10, 11))


# ------------------------------------------------------------------ FERIA
def _feria(R):
    e = "feria"
    i0, fin = INI(e), FIN(e)
    t_1828, t_vil, t_fer, t_cos, t_gan = T(e, "1828"), T(e, "villa"), T(e, "feria", frase=0), T(e, "cosechas"), T(e, "ganado")
    t_1831, t_ayu, t_com, t_ter, t_168, t_88, t_jar1 = (T(e, "1831"), T(e, "ayuntamiento"), T(e, "compro"), T(e, "terreno"), T(e, "168"),
                                                        T(e, "88"), T(e, "jardin", frase=1))
    t_mud, t_jar2, t_bal, t_abril, t_fie = T(e, "mudo"), T(e, "jardin", frase=2), T(e, "balaustrada"), T(e, "abril"), T(e, "fiestas")
    t_hoy, t_fn, t_2026, t_cer, t_vis = T(e, "hoy", frase=3), T(e, "feria nacional"), T(e, "2026"), T(e, "cerca"), T(e, "visitantes")
    t_jar4, t_abi, t_cor, t_ind = T(e, "jardin", frase=4), T(e, "abierto"), T(e, "corazon"), T(e, "indios", frase=4)
    f3 = FIN(e, 3)
    sm = CI["san_marcos"]

    R.camara(i0 - 0.2, *foco(-102.301, 21.879, 5.0))
    R.camara(t_1831, *foco(-102.3025, 21.878, 5.3))
    R.camara(t_jar2, *foco(-102.304, 21.8778, 5.7))
    R.camara(t_hoy + 0.3, *foco(-102.302, 21.879, 4.6))
    R.camara(t_jar4, *foco(-102.3044, 21.8778, 6.0))
    R.camara(fin + 0.3, *foco(-102.3044, 21.8778, 6.3))


    # frase 0: 1828, feria de cosechas y ganado
    R.anio(t_1828, 1828)
    pa(R, XI(7), 960, 1010, 1.0, i0 - 0.05, t_ayu, sem=S(), entra="sube", dy=340, extra=[(0.1, "pop", 0.4)])
    titulo(R, t_fer - 0.1, t_1831 - 0.2, "FERIA DE COSECHAS Y GANADO", px=70)
    R.snd(t_fer, "feria", 0.45)
    pa(R, FU(1), 330, 1010, 1.0, i0 + 0.3, t_cos - 0.2, sem=S())
    pa(R, FU(2), 1600, 1010, 1.0, i0 + 0.5, t_gan - 0.25, sem=S(), flip=True)
    pa(R, SX(4), 330, 1010, 0.75, t_cos - 0.1, t_ter - 0.2, sem=S())
    pa(R, CO(8), 1480, 1010, 0.72, t_gan - 0.15, t_ter - 0.2, sem=S(), extra=[(0.1, "mugido", 0.4)])
    pa(R, CO(10), 1760, 1010, 0.92, t_gan + 0.15, t_ter - 0.2, sem=S(), flip=True)
    ga(R, CO(9), sm, t_gan + 0.05, t_ter - 0.2, s=0.3, off=(-300, 60), sem=S(), zs=0.4, z=1)

    # frase 1: 1831, el Ayuntamiento compra un terreno de 168 × 88 m para un jardín
    R.anio(t_1831, 1831)
    pa(R, XI(2), 330, 1010, 1.0, t_ayu - 0.2, t_jar2, sem=S())
    R.texto(t_ayu, t_168, "EL AYUNTAMIENTO", (330, 560), px=44, d=0.4)
    pa(R, A.bolsa_dinero(), 500, 1000, 1.0, t_com - 0.1, t_jar1, sem=S(), extra=[(0.05, "monedas", 0.4)])
    pa(R, terreno_168x88(), 960, 1000, 1.0, t_ter - 0.1, t_jar2 + 0.3, sem=S(), entra="pluma", d_in=1.0,
       extra=[(0.0, "escribir", 0.3, {"dur": 0.9})])
    R.texto(t_168 - 0.05, t_jar2, "168 m", (960, 572), px=56, d=0.4)
    R.texto(t_88 - 0.05, t_jar2, "88 m", (1440, 801), px=56, d=0.4)
    R.texto(t_jar1 - 0.1, t_jar2 - 0.2, "UN JARDÍN", (960, 820), px=64, d=0.5)

    # frase 2: la feria se muda al Jardín de San Marcos (balaustrada de cantera), en abril
    pa(R, XI(8), 860, 1010, 1.0, t_jar2 - 0.15, t_hoy, sem=S(), extra=[(0.05, "pluck", 0.35)])
    pa(R, XI(7), lambda t: 150 + 220 * e_inout(prog(t, t_mud, t_mud + 1.4)), lambda t: 1010, 0.72, t_mud - 0.2, t_hoy, sem=S())
    ciudad(R, t_jar2, t_abril - 0.1, "san_marcos", None)
    titulo(R, t_jar2, t_abril - 0.2, "JARDÍN DE SAN MARCOS", px=70)
    pa(R, FP.F("feria_2"), 1460, 1000, FP.s_para(0.46), t_bal - 0.1, t_bal + 4.5, entra="pluma", sem=S())
    titulo(R, t_abril - 0.1, t_hoy - 0.15, "ABRIL · FIESTAS DE SAN MARCOS", px=66)
    R.snd(t_fie, "campana", 0.35, dur=2.0)

    # frase 3: hoy, la Feria Nacional de San Marcos: cerca de 8 millones de visitantes (2026)
    titulo(R, t_fn - 0.1, t_cer - 0.15, "FERIA NACIONAL DE SAN MARCOS", px=72)
    R.snd(t_fn, "fanfarria", 0.35)
    pa(R, FP.F("feria_3"), 450, 1000, FP.s_para(0.46), t_hoy - 0.05, t_hoy + 4.5, entra="pluma", sem=S())
    pa(R, TU(4), 1580, 1010, 1.15, t_fn + 0.2, f3 + 0.4, sem=S(), entra="sube", dy=360)
    R.anio(t_2026, 2026)
    pa(R, TU(1), 1130, 1010, 0.9, t_2026 - 0.1, fin + 0.3, sem=S())
    pa(R, TU(3), 430, 1010, 0.95, t_hoy + 4.6, fin + 0.3, sem=S())
    R.contador(t_cer - 0.05, t_vis, 0, 8000000, (960, 330), px=80, formato="{:,} VISITANTES", hasta_t=f3 + 0.4)
    R.snd(t_vis, "brillo", 0.35)

    # frase 4: el jardín, abierto todo el año, en el corazón del antiguo pueblo de indios (se puede visitar)
    ga(R, XI(8), sm, t_jar4 - 0.1, fin + 0.3, s=0.42, off=(-130, 110), sem=S(), zs=0.4, z=2, extra=[(0.05, "pop", 0.35)])
    ciudad(R, t_jar4, fin + 0.2, "san_marcos", None)
    titulo(R, t_jar4, fin + 0.3, "HOY: JARDÍN DE SAN MARCOS", px=66)
    R.texto(t_abi, fin + 0.3, "abierto todo el año", (960, 300), px=52, d=0.5)
    ga(R, CO(2), sm, t_cor - 0.1, fin + 0.3, s=0.36, off=(250, 100), sem=S(), zs=0.4, z=2, extra=[(0.05, "crece", 0.3)])
    pa(R, CO(4), 1600, 1010, 0.85, t_ind - 0.4, fin + 0.3, sem=S())
    limpiar(R, fin + 0.35, (10,))


# ------------------------------------------------------------------ BESO
def _beso(R):
    e = "beso"
    i0, fin = INI(e), FIN(e)
    t_1835, t_ags0, t_dep, t_reb, t_ant, t_sa0 = (T(e, "1835", frase=0), T(e, "aguascalientes", frase=0), T(e, "dependia"),
                                                  T(e, "rebelo"), T(e, "antonio"), T(e, "santa anna", frase=0))
    t_ley, t_noc, t_casa, t_ped, t_esp, t_lui, t_lib = (T(e, "leyenda"), T(e, "noche"), T(e, "casa"), T(e, "pedro"), T(e, "esposa"),
                                                        T(e, "luisa"), T(e, "libertad", frase=1))
    t_ace, t_cam, t_beso = T(e, "acepto"), T(e, "cambio"), T(e, "beso", frase=2)
    t_23, t_dec, t_sep = T(e, "23"), T(e, "decreto"), T(e, "separo")
    t_esc, t_1946, t_lab, t_cad = T(e, "escudo"), T(e, "1946"), T(e, "labios"), T(e, "cadena")
    t_pero, t_his, t_esc5, t_ing, t_eli, t_1927, t_sig, t_conc = (T(e, "pero"), T(e, "historia", frase=5), T(e, "escribio"),
                                                                  T(e, "ingeniero"), T(e, "elias"), T(e, "1927"), T(e, "siglo"),
                                                                  T(e, "concurso"))
    t_sepr, t_cas, t_zac6, t_perd, t_gue = T(e, "separacion"), T(e, "castigo"), T(e, "zacatecas", frase=6), T(e, "perdido"), T(e, "guerra")
    t_dur, t_1848, t_vol, t_anex, t_cons, t_1857, t_ags7, t_edo = (T(e, "duro"), T(e, "1848"), T(e, "volvio"), T(e, "anexarse"),
                                                                   T(e, "constitucion"), T(e, "1857"), T(e, "aguascalientes", frase=7),
                                                                   T(e, "estado", frase=7))
    t_2025, t_mus, t_expo, t_unb = T(e, "2025"), T(e, "museo"), T(e, "exposicion"), T(e, "un beso", frase=8)
    ags, zac = CI["aguascalientes"], CI["zacatecas"]
    REG = (-102.42, 22.42, 0.98)          # Aguascalientes + Zacatecas enteros

    R.camara(i0 - 0.2, *foco(-102.30, 21.879, 5.8))
    R.camara(t_ags0 + 0.2, *REG)
    R.camara(t_sa0 + 2.0, -102.38, 22.33, 1.12)
    R.camara(t_noc + 0.3, *foco(-102.2916, 21.8818, 4.6))
    R.camara(t_23 - 0.2, *foco(-102.2916, 21.8818, 5.2))
    R.camara(t_dec - 0.4, *REG)
    R.camara(t_esc - 0.3, -102.38, 22.30, 1.15)
    R.camara(t_lab, -102.33, 22.06, 1.6)
    R.camara(t_pero, -102.32, 22.02, 1.75)
    R.camara(t_sepr - 0.2, -102.33, 22.06, 1.65)
    R.camara(t_cas, *REG)
    R.camara(t_1848, -102.42, 22.36, 1.1)
    R.camara(t_edo, -102.38, 22.30, 1.15)
    R.camara(t_2025 + 0.2, -102.36, 22.20, 1.25)
    R.camara(t_mus, *foco(-102.2916, 21.8818, 5.0))
    R.camara(fin + 0.4, *foco(-102.2916, 21.8818, 5.6))

    # frase 0 (HECHO): 1835, Aguascalientes dependía de Zacatecas; Zacatecas se rebela contra Santa Anna
    R.anio(t_1835, 1835)
    pa(R, PL(1), 330, 1010, 1.0, i0 - 0.05, t_sa0 - 0.2, sem=S())
    ga(R, PL(1), zac, i0 + 0.3, t_noc, s=0.5, off=(-90, 120), sem=S(), zs=0.4, z=2)
    ciudad(R, i0 + 0.2, t_noc, "zacatecas", "ZACATECAS", "der", 42)
    pa(R, HECHO, ESQ[0], ESQ[1], 1.0, t_1835 + 0.3, t_ley - 0.15, sem=S(), d_out=0.25, extra=[(0.0, "golpe_suave", 0.4)])
    ciudad(R, t_ags0, t_noc, "aguascalientes", "AGUASCALIENTES", "der", 42)
    R.terreno(t_ags0 + 0.2, "zacatecas_dep", COL["zacatecas_dep"], 1.2, capa=12)
    lugar(R, t_dep, t_sa0, "PARTE DE ZACATECAS", ags, off=(0, -90), px=42)
    ga(R, XI(5), ags, t_dep + 0.1, t_sa0, s=0.32, off=(0, 60), sem=S(), zs=0.4, z=2, extra=[(0.05, "clink", 0.35)])
    for k, dx in enumerate((60, 190)):
        ga(R, PL(1), zac, t_reb + 0.1 * k, t_noc, s=0.48, off=(dx, 120 + 20 * k), sem=S(), zs=0.4, z=2, flip=True)
    ga(R, A.espadas(), zac, t_reb - 0.1, t_noc, s=0.55, off=(250, 70), sem=S(), zs=0.4, z=3, extra=[(0.05, "espada", 0.4)])
    R.snd(t_reb + 0.3, "tambor", 0.35, dur=1.2)
    pa(R, XI(0), 1560, 1010, 1.05, t_ant - 0.15, t_23, sem=S())
    R.texto(t_ant, t_ley - 0.1, "ANTONIO LÓPEZ DE SANTA ANNA", (1530, 560), px=40, d=0.6)
    pa(R, FP.F("beso_0"), 400, 1000, FP.s_para(0.52), t_sa0 - 0.1, t_ped - 0.15, entra="pluma", sem=S())
    R.ruta(M.RUTAS["santa_anna"], t_sa0, 2.4, ancho=5.0, t1=t_noc + 0.3, flecha=True)
    grupo_ciclo(R, C_SOLD, M.RUTAS["santa_anna"], t_sa0 + 0.1, 2.4, n=3, ancho=60, t1=t_noc + 0.3, s=0.5, sem=S(),
                extra=[(0.05, "pasos", 0.3, {"dur": 1.6})])
    S(), S()

    # frases 1-2 (LEYENDA): la noche en casa de Pedro García Rojas, Luisa Fernández Villa y el beso
    pa(R, LEYENDA, ESQ[0], ESQ[1], 1.0, t_ley - 0.05, t_23 - 0.15, sem=S(), d_out=0.25, extra=[(0.0, "sello", 0.45)])
    R.snd(t_ley + 0.2, "suspiro", 0.3)
    pa(R, vela, 960, 1010, 1.15, t_noc - 0.1, t_23, sem=S(), z=1)
    ciudad(R, t_casa - 0.1, t_lui - 0.1, "aguascalientes", "SU CASA", "abajo", 40)
    pa(R, XI(2), 330, 1010, 1.0, t_ped - 0.15, t_23, sem=S())
    R.texto(t_ped + 0.1, t_esp - 0.1, "PEDRO GARCÍA ROJAS", (330, 560), px=40, d=0.5, v=GRIS_LEY)
    pa(R, XI(1), lambda t: 700 + 480 * e_inout(prog(t, t_cam - 0.3, t_beso)), lambda t: 1010, 1.0, t_esp - 0.15, t_23, sem=S(), z=3)
    R.texto(t_lui - 0.05, t_ace - 0.1, "LUISA FERNÁNDEZ VILLA", (720, 540), px=40, d=0.5, v=GRIS_LEY)
    titulo(R, t_lib - 0.1, t_cam - 0.4, "«LA LIBERTAD DE AGUASCALIENTES»", px=62)
    titulo(R, t_cam - 0.3, t_23 - 0.15, "…A CAMBIO DE UN BESO", px=74)
    pa(R, corazon(), 1330, 640, 1.0, t_beso - 0.05, t_23, sem=S(), z=4, extra=[(0.0, "beso", 0.6)])

    # frase 3 (HECHO): el decreto del 23 de mayo de 1835 separa Aguascalientes de Zacatecas
    pa(R, HECHO, ESQ[0], ESQ[1], 1.0, t_23, t_pero - 0.15, sem=S(), d_out=0.25, extra=[(0.0, "golpe_suave", 0.4)])
    titulo(R, t_23, t_sep - 0.1, "23 DE MAYO DE 1835", px=80, snd=True)
    pa(R, FU(3), 330, 1010, 0.85, t_23 + 0.2, t_esc - 0.2, sem=S(), extra=[(0.05, "papel", 0.35)])
    R.texto(t_dec - 0.1, t_esc - 0.3, "DECRETO", (330, 620), px=48, d=0.4)
    R.sello(t_dec + 0.2, "balanza", "DECRETO · 1835", color=(176, 52, 48))
    R.terreno(t_sep, "edo_zacatecas", COL["edo_zacatecas"], 1.0, capa=12)
    R.terreno(t_sep + 0.05, "aguascalientes", COL["aguascalientes"], 1.0, capa=13)
    R.snd(t_sep, "crujido", 0.45)
    ciudad(R, t_sep + 0.2, t_esc - 0.2, "aguascalientes", "AGUASCALIENTES", "der", 44)
    ciudad(R, t_sep + 0.3, t_esc - 0.2, "zacatecas", "ZACATECAS", "der", 40)

    # frase 4 (HECHO): el escudo, desde 1946, labios rodeados por una cadena
    ex, ey, es = 960, 1000, 1.15
    pa(R, XI(6), ex, ey, es, t_esc - 0.15, t_1927, sem=S(), entra="sube", dy=360, z=2, extra=[(0.05, "brillo", 0.35)])
    titulo(R, t_esc, t_lab - 0.2, "EL ESCUDO DEL ESTADO", px=74)
    R.anio(t_1946, 1946)
    titulo(R, t_lab - 0.1, t_cad - 0.15, "UNOS LABIOS…", px=74)
    pa(R, XI(5), ex, ey - 0.52 * 400 * es + 0.5 * 400 * 0.6, 0.6, t_cad - 0.1, t_1927, sem=S(), z=3, extra=[(0.05, "clink", 0.4)])
    titulo(R, t_cad - 0.05, t_pero - 0.15, "…Y UNA CADENA", px=74)

    # frase 5: «Pero…»: la escribió Elías L. Torres en 1927 para un concurso literario
    titulo(R, t_pero - 0.05, t_his - 0.1, "PERO…", px=150)
    R.snd(t_pero, "hmm", 0.4)
    pa(R, LEYENDA_GRANDE, ex, 820, 1.0, t_his - 0.05, t_1927, sem=S(), z=4, extra=[(0.0, "sello", 0.55)])
    pa(R, LEYENDA, ESQ[0], ESQ[1], 1.0, t_his + 0.3, t_sepr - 0.15, sem=S(), d_out=0.25)
    pa(R, PO(9), 330, 1010, 1.0, t_ing - 0.15, t_sepr, sem=S())
    R.texto(t_eli - 0.05, t_1927 + 1.0, "ELÍAS L. TORRES", (330, 560), px=46, d=0.5)
    pa(R, FU(3), 1560, 1010, 0.8, t_esc5 - 0.1, t_sepr, sem=S(), extra=[(0.05, "papel", 0.35)])
    R.texto(t_conc - 0.05, t_sepr - 0.1, "CONCURSO LITERARIO", (1560, 640), px=40, d=0.5)
    R.anio(t_1927, 1927)
    titulo(R, t_1927 - 0.05, t_sepr - 0.15, "LO INVENTÓ EN 1927", px=100, snd=True)
    R.texto(t_sig - 0.2, t_sepr - 0.15, "92 años después", (960, 330), px=58, d=0.5)

    # frase 6 (HECHO): un castigo político a Zacatecas, que había perdido la guerra
    pa(R, HECHO, ESQ[0], ESQ[1], 1.0, t_sepr, fin + 0.3, sem=S(), extra=[(0.0, "golpe_suave", 0.4)])
    ga(R, XI(0), zac, t_sepr - 0.05, t_anex, s=0.55, off=(-140, 120), sem=S(), zs=0.4, z=2)
    ciudad(R, t_sepr, t_cons, "zacatecas", "ZACATECAS", "der", 40)
    ciudad(R, t_sepr + 0.1, t_mus - 0.4, "aguascalientes", "AGUASCALIENTES", "der", 42)
    titulo(R, t_cas - 0.1, t_dur - 0.1, "CASTIGO POLÍTICO", px=84, y=350)
    R.anio(t_sepr, 1835)
    R.snd(t_cas, "impacto", 0.45)
    R.terreno(t_cas, "edo_zacatecas", (198, 70, 60), 0.7, capa=12)
    R.terreno(t_gue + 0.6, "edo_zacatecas", COL["edo_zacatecas"], 0.8, capa=12)
    ga(R, PL(1), zac, t_zac6, t_perd, s=0.48, off=(90, 120), sem=S(), zs=0.4, z=2, flip=True, sale="caer", d_out=0.6,
       sfx_out=[(0.1, "golpe_suave", 0.35)])
    pa(R, A.espadas(), 1560, 1010, 0.9, t_zac6 - 0.2, t_dur, sem=S(), sale="caer", d_out=0.6)

    # frase 7 (HECHO): 1848 vuelve a Zacatecas; 1857 estado para siempre
    R.anio(t_1848, 1848)
    titulo(R, t_vol - 0.1, t_cons - 0.15, "1848: OTRA VEZ ZACATECAS", px=66, y=350)
    R.terreno(t_anex, "zacatecas_dep", COL["zacatecas_dep"], 0.9, capa=12)
    R.terreno(t_anex, None, COL["aguascalientes"], 0.6, capa=13)
    ga(R, XI(5), ags, t_1848, t_edo, s=0.5, off=(0, 60), sem=S(), zs=0.4, z=2, extra=[(0.05, "clink", 0.4)])
    pa(R, FU(3), 330, 1010, 0.85, t_cons - 0.15, t_2025 - 0.1, sem=S())
    R.texto(t_cons, t_2025 - 0.2, "CONSTITUCIÓN DE 1857", (330, 620), px=40, d=0.5)
    R.anio(t_1857, 1857)
    R.terreno(t_ags7, "edo_zacatecas", COL["edo_zacatecas"], 0.8, capa=12)
    R.terreno(t_ags7 + 0.05, "aguascalientes", COL["aguascalientes"], 0.9, capa=13)
    titulo(R, t_edo - 0.1, t_2025 - 0.15, "ESTADO PARA SIEMPRE", px=88)
    R.snd(t_edo, "gong", 0.35)
    pa(R, XI(6), 1660, 1010, 0.85, t_edo, fin + 0.3, sem=S(), extra=[(0.05, "fanfarria", 0.3)])

    # frase 8 (HECHO): 2025, el Museo Regional de Historia (INAH) y la exposición «¿Un beso por la libertad?»
    R.anio(t_2025, 2025)
    pa(R, TU(0), 330, 1010, 1.0, t_mus - 0.15, fin + 0.3, sem=S())
    ciudad(R, t_mus, fin + 0.2, "aguascalientes", "MUSEO REGIONAL DE HISTORIA", "arriba", 40)
    titulo(R, t_mus, t_unb - 0.2, "HOY: MUSEO REGIONAL DE HISTORIA (INAH)", px=56)
    ga(R, XI(1), ags, t_expo - 0.4, fin + 0.3, s=0.5, off=(-270, 330), sem=S(), zs=0.4, z=2)
    ga(R, XI(0), ags, t_expo - 0.25, fin + 0.3, s=0.5, off=(270, 330), sem=S(), zs=0.4, z=2, flip=True)
    pa(R, corazon(), 960, 830, 0.7, t_expo, fin + 0.3, sem=S(), z=3)
    titulo(R, t_unb - 0.15, fin + 0.3, "¿UN BESO POR LA LIBERTAD?", px=84)
    R.texto(t_expo, fin + 0.3, "exposición · 2025", (960, 300), px=48, d=0.5)
    R.snd(t_unb, "revelar", 0.35)
    limpiar(R, t_mus - 0.6, (12, 13))
