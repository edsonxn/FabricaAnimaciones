# -*- coding: utf-8 -*-
"""Coreografía (3/4) de «Toda la historia de los AZTECAS»: el tributo (cargadores de las provincias al centro, el Códice Mendoza,
mantas, maíz, trajes, plumas, jaguar, cacao, oro, hule; la red de pueblos), Axayácatl (Tlatelolco 1473 y Moquíhuix, la derrota
ante los purépechas, la Piedra del Sol y su hallazgo en 1790), Ahuízotl (el Soconusco, el Templo Mayor doble de 1487, los 80 000
«exagerados», el Huey Tzompantli, la inundación de 1499, el ahuizote) y Moctezuma II (protocolo, zoológico, la ciudad, el imperio
de 1519, los presagios y Xolo aullando).
Dibujos = pegatinas de Flow; fotos = FotoPeg. sem 600-899. Capas de terreno: 30 imperio, 31 Tlatelolco, 32 purépechas,
50 (agua) la inundación; se limpian al salir."""
import math
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

import boceto as B
import foto_peg as FP
import mapa as M
import obj_c as OC
from core import FIN, INI, T
from coreo_peg import andar_ciclo, ciclo_pant, grupo_ciclo
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo, tramo
from motor import e_inout, e_out, prog
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (números de piezas/<hoja>/_indice.jpg)
XO = lambda n, **k: P("01_xolo_hoja", n, **k)          # 0 sentado, 1 camina, 2 asustado, 3 bajo el petate, 4 aúlla, 5 salta, 6 duerme, 7 sospecha
XS = lambda n, **k: P("24_xolo_salta", n, **k)         # 0-7 saltos/carrera
MI = lambda n, **k: P("18_mictlan_hoja", n, **k)       # 7 Xolo con tocado de guerrero
TR = lambda n, **k: P("10_tributo_hoja", n, **k)       # 0 maíz, 1 traje de guerrero, 2 plumas, 3 piel de jaguar, 4 cañones de oro, 5 disco de oro, 6 hule, 7 calpixqui, 8 cargador
AX = lambda n, **k: P("11_axayacatl_hoja", n, **k)     # 0 Axayácatl, 1 rey cae, 2 guerrero purépecha, 3 rey purépecha, 4 Piedra del Sol, 5 piedra en bruto, 6 cantero, 7 pirámide doble, 8 peones 1790
AH = lambda n, **k: P("12_ahuizotl_hoja", n, **k)      # 0 Ahuízotl, 1 Templo Mayor, 2 Tláloc, 3 tzompantli, 4 sacerdote, 5 ahuizotl, 6-7 casas inundadas, 9 cacao
MO = lambda n, **k: P("13_moctezuma2_hoja", n, **k)    # 0 Moctezuma en el trono, 1 cortesano, 2 jaguar enjaulado, 3 quetzal y guacamaya, 4 cometa, 5 templo en llamas, 6 mujer que llora, 7 la ciudad en el lago
VI = lambda n, **k: P("08_vida_hoja", n, **k)          # 10 cacao, 12 mantas
ME = lambda n, **k: P("09_mercado_hoja", n, **k)       # 6 gente, 7 tlacuilo
CH = lambda n, **k: P("03_chapultepec_hoja", n, **k)   # 3 señor en su trono, 4 serpientes
FU = lambda n, **k: P("04_fundacion_hoja", n, **k)     # 0 águila
MG = lambda n, **k: P("02_migracion_hoja", n, **k)     # 3 Huitzilopochtli
M1 = lambda n, **k: P("07_moctezuma1_hoja", n, **k)    # 4 acueducto, 6 guerrero
AL = lambda n, **k: P("06_alianza_hoja", n, **k)       # 6 guerrero águila


def _cic(hoja, n=8):
    """Ciclo de Flow; si la carpeta no trae `ciclo_NN.png` (estas traen NN.png), las piezas numeradas."""
    fr = ciclo(hoja)
    return fr if fr else [P(hoja, k) for k in range(n)]


C_XOLO = _cic("19_xolo_corre")
C_CARG = _cic("20_mexica_camina")
C_GUER = _cic("23_guerrero_corre")

TM = CI["templo_mayor"]
ZOCALO = (-99.1332, 19.4326)            # Plaza Mayor (hoy Zócalo): ahí apareció la Piedra del Sol en 1790
PALACIO = (-99.1312, 19.4326)           # casas de Moctezuma (hoy Palacio Nacional), aprox.
TZOMPANTLI = (-99.1327, 19.4352)        # Huei Tzompantli, República de Guatemala 24, aprox.
TAXIMAROA = (-100.54, 19.70)            # Taximaroa (hoy Ciudad Hidalgo, Mich.), donde perdieron en 1478
AGUA_INUND = (112, 160, 196)

_SEM = iter(range(600, 900))


def S():
    return next(_SEM)


def foco(lon, lat, z, dy=140):
    """Clave de cámara que deja (lon, lat) ~dy px por DEBAJO del centro (los dibujos crecen hacia arriba)."""
    return lon, lat + dy / (300.0 * z * 1.06), z


def paseo(R, t0, t1, a, b, paso=2.0):
    """Claves de cámara cada ~paso s de a=(lon, lat, z) a b (movimiento continuo; CamPath añade el vaivén)."""
    n = max(1, int(round((t1 - t0) / paso)))
    for k in range(n + 1):
        u = e_inout(k / n)
        R.camara(t0 + (t1 - t0) * k / n, a[0] + (b[0] - a[0]) * u, a[1] + (b[1] - a[1]) * u, a[2] * (b[2] / a[2]) ** u)


# ------------------------------------------------------------------ primitivas propias
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
    """Sello de goma con texto en un color propio, como pegatina: pies en (x, y), s escala el tamaño de letra (kit de Aguascalientes)."""

    def __init__(self, txt, color, px=58, rot=0.12):
        self.txt, self.color, self.px, self.rot = txt, color, px, rot
        self.alto = px * 1.9

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


EXAGERADO = SelloTxt("EXAGERADO", (196, 52, 46), px=74, rot=-0.10)
REAL = SelloTxt("SÍ FUE REAL", (52, 128, 84), px=62, rot=0.08)
LEYENDA = SelloTxt("LEYENDA", (120, 90, 160), px=64, rot=0.12)
CONQUISTADA = SelloTxt("CONQUISTADA", (196, 52, 46), px=46, rot=-0.12)


def tachar(R, t0, t1, txt, pos, px, sem=0):
    """Raya de tinta que tacha un rótulo de pantalla (se dibuja en 0,35 s y se borra con él en t1)."""
    w = B.ancho_texto(txt, px)
    x, y = pos
    Pt = np.stack([np.linspace(x - w / 2 - 16, x + w / 2 + 16, 14), np.linspace(y - 0.1 * px + 8, y - 0.1 * px - 6, 14)], 1)

    def f(h, cam, t, fs, te):
        if t < t0 or t > t1 + 0.3:
            return
        u = prog(t, t0, t0 + 0.35)
        v = int(255 * (1 - prog(t, t1, t1 + 0.3)))
        if v > 0:
            h.trazo(Pt, 8.0, 640 + sem, fs, u, amp=1.6, v=v)
    R.frente.append(R._acot(f, t0))
    R.snd(t0, "escribir", 0.32, dur=0.4)


def gira(R, dib, cx, cy, s, t0, t1, rot_fn, sem, alto=400.0, entra="pop", sale="encoger", z=2, sfx=()):
    """Pegatina que gira alrededor de su CENTRO (cx, cy) con rot_fn(t) (Peg gira por los pies)."""
    h = alto * s

    def pos(t):
        r = rot_fn(t)
        return (cx - 0.5 * h * math.sin(r), cy + 0.5 * h * math.cos(r), s, r)
    return R.act(dib, pos=pos, t_in=t0, d_in=0.45, entra=entra, sem=sem, sfx=list(sfx), t_out=t1, sale=sale, z=z)


def cronometro(t):
    return OC.cronometro(round(((t * 1.6) % 1.0) * 12) / 12 * 2 * math.pi)


def cortes(R):
    pass


def construir(R):
    _calzadas(R)
    _tributo(R)
    _axayacatl(R)
    _ahuizotl(R)
    _moctezuma2(R)
    R.terreno(FIN("moctezuma2") + 0.2, None, COL["imperio_1519"], 0.6, capa=30)


def _calzadas(R):
    """Calzadas y albarradón de la isla mientras la cámara está cerca de la ciudad (solo en este tramo)."""
    t0, t1 = INI("tributo") - 0.3, FIN("moctezuma2") + 0.6

    def f(img, cam, t, fs):
        if t < t0 or t > t1:
            return
        a = min(1.0, max(0.0, (cam.z - 7.0) / 7.0))
        if a > 0.02:
            M.pintar_calzadas(img, cam, alfa=0.85 * a)
    R.fondo.append(("mx", f))


# ------------------------------------------------------------------ TRIBUTO
def _tributo(R):
    e = "tributo"
    i0, fin = INI(e), FIN(e)
    t_trib, t_anot, t_dib = T(e, "tributo"), T(e, "anotado"), T(e, "dibujos")
    t_man, t_mai, t_tra, t_plu, t_pie = T(e, "mantas"), T(e, "maiz"), T(e, "trajes"), T(e, "plumas"), T(e, "pieles")
    t_prov, t_cac, t_oro, t_hul = T(e, "provincias"), T(e, "cacao"), T(e, "oro"), T(e, "pelotas")
    t_cam, t_sen, t_dio, t_idi, t_pag = T(e, "cambio"), T(e, "senores"), T(e, "dioses"), T(e, "idioma"), T(e, "pagara")
    t_nop, t_ejer = T(e, "si no pagaba"), T(e, "ejercito")
    t_asi, t_pais, t_ymas, t_red, t_mala = T(e, "asi"), T(e, "pais"), T(e, "y mas"), T(e, "red"), T(e, "mala")
    ten = CI["tenochtitlan"]

    # cámara: el imperio (1469) entero alrededor del centro; se acerca un poco con la lista y se aleja para la red
    R.camara(i0 - 0.2, -97.95, 18.98, 1.04)
    paseo(R, i0 + 1.6, t_man, (-97.9, 18.96, 1.07), (-97.95, 18.92, 1.12))
    paseo(R, t_man + 2.0, t_prov, (-98.05, 18.9, 1.14), (-97.85, 18.9, 1.1))
    paseo(R, t_prov + 2.0, t_nop, (-97.8, 18.88, 1.08), (-97.95, 18.9, 1.04))
    paseo(R, t_ejer, fin - 1.0, (-97.9, 18.82, 1.0), (-97.8, 18.7, 0.94))

    # el imperio (capa 30 todo el tramo; Axayácatl lo hace crecer a 1481)
    R.terreno(i0 - 0.3, "imperio_1469", COL["imperio_1469"], 1.2, capa=30)

    # frase 0: rutas de las provincias (puntos dentro del imperio de 1469, sin nombre) al centro + cargadores
    def fin_(dx, dy):
        return (ten[0] + dx, ten[1] + dy)
    prov = [[(-95.6, 18.5), CI["cuetlaxtlan"], (-97.3, 19.05), (-98.3, 19.12), fin_(0.10, -0.02)],
            [(-99.75, 18.05), CI["tlachco"], (-99.4, 18.95), fin_(-0.06, -0.10)],
            [(-99.2, 17.9), (-99.0, 18.1), CI["huaxtepec"], fin_(0.04, -0.12)],
            [(-99.5, 19.72), (-99.3, 19.6), fin_(-0.04, 0.10)],
            [(-96.6, 18.55), (-97.5, 18.75), (-98.6, 18.95), fin_(0.12, -0.08)]]
    pa(R, TR(8), 330, 1010, 0.92, i0 - 0.1, t_man - 0.3, sem=S(), extra=[(0.0, "pasos", 0.35)])
    ciudad(R, i0 + 0.2, t_ejer, "tenochtitlan", "TENOCHTITLAN", "izq", 40)
    for k, Pr in enumerate(prov):
        tk = i0 + 0.25 + 0.45 * k
        dur = 7.5 + 0.5 * k
        R.ruta(Pr, tk, 1.6, ancho=4.0, t1=t_red - 0.2, flecha=True)
        R.ciudad(tk, t_man, f"prov{k}", Pr[0], None)
        andar_ciclo(R, C_CARG, Pr, tk + 0.3, dur, t1=tk + 0.3 + dur - 0.9, s=0.58, sem=S(), z=2, fps=8)
    R.snd(i0 + 0.3, "whoosh", 0.35, dur=0.7)
    andar_ciclo(R, C_XOLO, prov[0], i0 + 1.0, 7.0, t1=i0 + 7.8, s=0.42, sem=S(), z=3, fps=12, off=(50, 12),
                extra=[(0.4, "ladrido", 0.3)])
    titulo(R, t_trib, t_man - 0.2, "TRIBUTO", snd=True)
    pa(R, FP.F("mendoza_tributo_46r"), 1560, 1005, FP.s_para(0.5), t_anot - 0.3, t_man + 0.4, entra="pluma", d_in=0.6, sem=S(), z=6)
    pa(R, ME(7), 1040, 1012, 0.62, t_anot + 0.1, t_man + 0.2, sem=S(), z=4, extra=[(0.0, "escribir", 0.35)])
    R.texto(t_dib, t_man - 0.3, "PUEBLO POR PUEBLO", (1040, 700), px=40, d=0.5)

    # frase 1: la lista del tributo en fila (abajo) + el Códice Mendoza (f. 52r, Tuchpan)
    fila = [(t_man, VI(12), 230, 0.56, "papel"), (t_mai, TR(0), 470, 0.62, "golpe_suave"), (t_tra, TR(1), 720, 0.74, "pop"),
            (t_plu, TR(2), 950, 0.66, "whoosh"), (t_pie, TR(3), 1190, 0.62, "golpe_suave")]
    for k, (tk, dib, x, s, snd) in enumerate(fila):
        pa(R, dib, x, 1010 - 8 * (k % 2), s, tk - 0.1, t_prov + 0.6 + 0.12 * k, sem=S(), z=4, rot=0.05 * (k % 3 - 1),
           extra=[(0.0, snd, 0.35)])
    pa(R, FP.F("mendoza_tributo_52r"), 1590, 1005, FP.s_para(0.5), t_tra - 0.2, t_prov + 0.5, entra="pluma", d_in=0.6, sem=S(), z=6)

    # frase 2: cacao, oro en polvo, hule (en provincias distintas, sin nombrarlas) + segunda oleada de cargadores
    for tk, dib, geo, s, off, snd in ((t_cac, VI(10), CI["cuetlaxtlan"], 0.55, (20, -10), "monedas"),
                                      (t_oro, TR(4), (-99.2, 17.95), 0.55, (-40, -10), "brillo"),
                                      (t_oro + 0.25, TR(5), (-99.2, 17.95), 0.4, (70, -10), None),
                                      (t_hul, TR(6), (-95.6, 18.5), 0.55, (-30, -10), "golpe_suave")):
        ga(R, dib, geo, tk - 0.1, t_cam + 0.6, s=s, off=off, sem=S(), z=3, zs=0.4, extra=[(0.0, snd, 0.4)] if snd else ())
    lugar(R, t_cac, t_cam, "CACAO", CI["cuetlaxtlan"], off=(20, -230), px=42)
    lugar(R, t_oro, t_cam, "ORO EN POLVO", (-99.2, 17.95), off=(10, -230), px=42)
    lugar(R, t_hul, t_cam, "HULE", (-95.6, 18.5), off=(-30, -230), px=42)
    for k in (1, 3, 4):
        Pr = prov[k]
        andar_ciclo(R, C_CARG, Pr, t_prov + 0.2 + 0.3 * k, 8.0, t1=t_prov + 8.0 + 0.3 * k, s=0.58, sem=S(), z=2, fps=8)

    # frase 3: señores, dioses, idioma… mientras pagara; si no, el ejército
    pa(R, TR(7), 330, 1010, 0.9, t_cam - 0.1, t_nop - 0.2, sem=S(), extra=[(0.0, "pop", 0.3)])
    pa(R, CH(3), 760, 1010, 0.7, t_sen - 0.1, t_nop, sem=S(), z=3)
    pa(R, AH(2), 1060, 1010, 0.62, t_dio - 0.1, t_nop + 0.1, sem=S(), z=3, extra=[(0.0, "flauta", 0.3)])
    pa(R, OC.globo_dialogo(), 900, 640, 1.3, t_idi - 0.05, t_nop + 0.1, sem=S(), z=4)
    R.texto(t_idi + 0.1, t_nop + 0.1, "OTOMÍ, MIXTECO...", (900, 612), px=28, d=0.4)
    R.texto(t_sen, t_nop + 0.1, "SUS SEÑORES", (520, 196), px=54, d=0.5)
    R.texto(t_dio, t_nop + 0.1, "SUS DIOSES", (960, 196), px=54, d=0.5)
    R.texto(t_idi, t_nop + 0.1, "SU IDIOMA", (1400, 196), px=54, d=0.5)
    titulo(R, t_pag - 0.1, t_nop + 0.1, "...MIENTRAS PAGARA", y=300, px=62)
    R.snd(t_pag, "monedas", 0.45)
    ciclo_pant(R, C_GUER, -160, 1250, 1005, t_nop + 0.1, 3.0, t1=t_asi + 0.4, s=0.62, sem=S(), z=3, fps=12)
    ciclo_pant(R, C_GUER, -360, 1050, 1015, t_nop + 0.3, 3.0, t1=t_asi + 0.4, s=0.6, sem=S(), z=3, fps=12)
    ciclo_pant(R, C_GUER, -560, 850, 1000, t_nop + 0.5, 3.0, t1=t_asi + 0.4, s=0.58, sem=S(), z=3, fps=12)
    R.snd(t_nop + 0.2, "tambor", 0.5)
    titulo(R, t_ejer - 0.1, t_asi - 0.1, "LLEGABA EL EJÉRCITO", px=64)
    grupo_ciclo(R, C_GUER, prov[4][::-1], t_ejer - 0.2, 2.8, n=3, ancho=60, t1=t_ymas, s=0.5, sem=S(), fps=12)
    pa(R, XO(2), 1640, 1012, 0.55, t_ejer - 0.3, t_ymas, sem=S(), z=4, extra=[(0.2, "gemido_perro", 0.4)])

    # frase 4: ¿un país? no: una red de pueblos que pagaban de mala gana (el imperio se parte en provincias)
    pa(R, TR(8), 330, 1010, 0.9, t_asi - 0.2, fin + 0.5, sem=S(), flip=True)
    titulo(R, t_pais - 0.3, t_red - 0.3, "UN PAÍS", px=84)
    tachar(R, t_ymas, t_red - 0.3, "UN PAÍS", (960, 196), 84, sem=S())
    titulo(R, t_red - 0.15, fin + 0.6, "UNA RED DE PUEBLOS", px=76, snd=True)
    R.romper("provincias", t_red - 0.4, t_red + 0.5, fin - 0.1, fin + 0.6, capa=30, rej="mx")
    R.snd(t_red - 0.3, "crece", 0.45)
    for k, n in enumerate(("tochtepec", "cuetlaxtlan", "tlapan", "tlachco", "toluca", "tepeaca", "cuauhnahuac", "coyolapan",
                           "malinalco", "huaxtepec", "xilotepec", "tochpan")):
        R.ciudad(t_red + 0.06 * k, fin + 0.5, n, CI[n], None)
    pa(R, XO(7), 1640, 1012, 0.55, t_mala - 0.4, fin + 0.6, sem=S(), z=4)
    R.texto(t_mala, fin + 0.6, "DE MALA GANA", (1440, 300), px=44, d=0.4)


# ------------------------------------------------------------------ AXAYÁCATL
def _axayacatl(R):
    e = "axayacatl"
    i0, fin = INI(e), FIN(e)
    t_1473, t_axa, t_mal, t_riv, t_her, t_conq = (T(e, "1473"), T(e, "axayacatl", frase=0), T(e, "malas"), T(e, "rivalidad"),
                                                  T(e, "hermana"), T(e, "conquisto"))
    t_rey, t_moq, t_cay, t_pir = T(e, "rey"), T(e, "moquihuix"), T(e, "cayendo"), T(e, "piramide")
    t_pero, t_der, t_pure, t_mich = T(e, "pero"), T(e, "derrota"), T(e, "purepechas", frase=2), T(e, "michoacan")
    t_pure3, t_met, t_imp, t_oes, t_nun = T(e, "purepechas", frase=3), T(e, "metal"), T(e, "imperio", frase=3), T(e, "oeste"), T(e, "nunca")
    t_estos, t_fam, t_ps = T(e, "estos"), T(e, "famosa"), T(e, "piedra del sol")
    t_no, t_cal, t_monu, t_25, t_ton, t_eras, t_term = (T(e, "no", frase=5), T(e, "calendario"), T(e, "monumento"), T(e, "25"),
                                                       T(e, "toneladas"), T(e, "eras"), T(e, "terminado"))
    t_desp, t_ent, t_reap, t_1790, t_plaza = T(e, "despues"), T(e, "enterraron"), T(e, "reaparecio"), T(e, "1790"), T(e, "plaza")
    ten, tla = CI["tenochtitlan"], CI["tlatelolco"]

    # cámara: la isla de cerca (Tenochtitlan abajo, Tlatelolco arriba) → el oeste purépecha → la plaza (Piedra del Sol)
    paseo(R, i0 - 0.2, t_rey + 1.0, foco(-99.1345, 19.4425, 34, 60), foco(-99.1335, 19.4435, 40, 60))
    R.camara(t_pir + 0.5, *foco(-99.1350, 19.4440, 42, 40))
    R.camara(t_pero + 1.2, -99.55, 19.45, 3.2)
    paseo(R, t_der - 0.2, t_mich + 0.6, (-100.15, 19.42, 1.42), (-100.35, 19.45, 1.32))
    paseo(R, t_met, t_nun + 1.6, (-100.55, 19.42, 1.30), (-100.75, 19.40, 1.24))
    R.camara(t_estos + 0.9, -99.40, 19.43, 6.0)
    paseo(R, t_fam + 0.3, fin - 0.25, foco(ZOCALO[0], ZOCALO[1], 36, 200), foco(ZOCALO[0] + 0.0012, ZOCALO[1], 42, 200))

    R.anio(t_1473, 1473)
    # frase 0: Axayácatl contra la ciudad hermana
    pa(R, AX(0), 330, 1010, 1.0, i0 - 0.1, t_rey - 0.1, sem=S(), extra=[(0.0, "caracol", 0.35)])
    titulo(R, t_axa, t_mal + 1.2, "AXAYÁCATL", snd=True)
    pa(R, FP.F("axayacatl_tlatelolco"), 1580, 1005, FP.s_para(0.52), t_axa + 0.3, t_conq + 0.2, entra="pluma", d_in=0.6, sem=S())
    R.ciudad(t_1473 + 0.3, t_pero, "tenochtitlan", ten, "TENOCHTITLAN", "abajo", 40)
    R.ciudad(t_1473 + 0.6, t_pero, "tlatelolco", tla, "TLATELOLCO", "der", 40)
    R.terreno(t_riv - 0.2, "islote_tlatelolco", (84, 118, 172), 0.8, capa=31)
    R.terreno(t_conq, "islote_tlatelolco", COL["imperio_1481"], 1.0, capa=31)
    R.terreno(t_pero, None, COL["imperio_1481"], 0.5, capa=31)
    pa(R, AX(0), 1590, 1010, 0.95, t_pero - 0.1, t_der + 0.4, sem=S(), extra=[(0.0, "tambor", 0.4)])
    R.terreno(t_pero + 0.5, "imperio_1481", COL["imperio_1481"], 1.8, capa=30)      # las conquistas de Axayácatl (Toluca...)
    ga(R, AX(7), tla, t_riv - 0.1, t_pir + 0.6, s=0.62, off=(-190, 10), sem=S(), z=2, zs=0.0, extra=[(0.0, "pop", 0.3)])
    ga(R, AL(6), ten, t_riv + 0.2, t_conq + 0.4, s=0.5, off=(-170, 20), sem=S(), z=2, zs=0.0)
    R.texto(t_her, t_conq - 0.1, "LA CIUDAD HERMANA", None, px=40, geo=tla, off=(40, -250))
    ciclo_pant(R, C_GUER, -160, 1060, 1010, t_mal, 2.6, t1=t_conq + 0.3, s=0.55, sem=S(), z=3, fps=12)
    ciclo_pant(R, C_GUER, -380, 860, 1000, t_mal + 0.25, 2.6, t1=t_conq + 0.3, s=0.53, sem=S(), z=3, fps=12)
    R.snd(t_mal, "tambor", 0.45)
    R.snd(t_conq, "batalla", 0.45)
    ga(R, CONQUISTADA, tla, t_conq, t_pero - 0.2, s=1.0, off=(-190, -290), sem=S(), z=5, zs=0.0, extra=[(0.0, "sello", 0.5)])

    # frase 1: Moquíhuix cae de lo alto de su pirámide
    R.texto(t_moq, t_pero - 0.2, "MOQUÍHUIX", (1610, 540), px=52, d=0.45)
    R.act(AX(1), pos=lambda t: (1610, 1012, 1.0, 0.07 * math.sin(t * 7.0)), t_in=t_rey - 0.1, d_in=0.4, entra="pop", sem=S(),
          sfx=[(t_cay - t_rey + 0.1, "whoosh", 0.4), (t_pir - t_rey, "impacto", 0.45)], t_out=t_pero + 0.1, sale="caer", z=3)
    pa(R, XO(2), 400, 1012, 0.6, t_rey + 0.3, t_pero + 0.2, sem=S(), z=3, extra=[(t_pir - t_rey + 0.1, "gemido_perro", 0.35)])

    # frase 2: la peor derrota, contra los purépechas (1478, Taximaroa)
    R.anio(t_der, 1478)
    titulo(R, t_der - 0.1, t_pure3 - 0.3, "LA PEOR DERROTA", px=78, snd=True)
    camino = [ten, (-99.6, 19.36), (-100.1, 19.55), TAXIMAROA]
    R.ruta(camino, t_pero + 0.4, 2.0, ancho=5.0, t1=t_oes, flecha=True)
    grupo_ciclo(R, C_GUER, camino, t_pero + 0.5, 2.6, n=3, ancho=70, t1=t_der + 1.8, s=0.56, sem=S(), fps=12)
    ga(R, AX(2), TAXIMAROA, t_der + 0.2, t_pure3, s=0.62, off=(-120, 0), sem=S(), z=3, extra=[(0.0, "batalla", 0.5)])
    ciudad(R, t_der + 0.3, t_nun, "tzintzuntzan", "TZINTZUNTZAN", "arriba", 34)
    R.ciudad(t_der + 0.2, t_oes, "taximaroa", TAXIMAROA, "TAXIMAROA", "abajo", 32)
    huida = [TAXIMAROA, (-100.1, 19.55), (-99.6, 19.36), ten]
    grupo_ciclo(R, C_GUER, huida, t_der + 1.9, 3.2, n=3, ancho=70, t1=t_pure3 + 0.5, s=0.52, sem=S(), fps=14)
    andar_ciclo(R, C_XOLO, huida, t_der + 1.7, 3.0, t1=t_pure3 + 0.5, s=0.4, sem=S(), z=3, fps=14, off=(60, 20),
                extra=[(0.3, "ladrido", 0.3)])
    pa(R, FP.F("derrota_1478"), 420, 1005, FP.s_para(0.44), t_der + 0.2, t_pure3 + 0.6, entra="pluma", d_in=0.6, sem=S())
    R.terreno(t_pure - 0.2, "purepecha", COL["purepecha"], 1.0, capa=32)
    R.terreno(t_estos + 0.4, None, COL["purepecha"], 0.6, capa=32)
    pa(R, AX(3), 960, 1010, 0.92, t_pure - 0.15, t_estos, sem=S(), extra=[(0.0, "pop", 0.3)])
    lugar(R, t_mich, t_nun + 0.3, "MICHOACÁN", CI["tzintzuntzan"], off=(-40, 110), px=40)

    # frase 3: metal, su propio imperio al oeste, nunca conquistados
    pa(R, AX(2), 1590, 1010, 1.0, t_pure3 + 0.3, t_estos + 0.2, sem=S(), extra=[(t_met - t_pure3 - 0.2, "brillo", 0.4)])
    R.texto(t_met, t_nun - 0.1, "COBRE", (1590, 520), px=48, d=0.4)
    R.texto(t_imp, t_estos, "IMPERIO PURÉPECHA", None, px=46, geo=CI["tzintzuntzan"], off=(40, -120))
    R.snd(t_imp, "crece", 0.4)
    titulo(R, t_nun - 0.1, t_estos + 0.2, "NUNCA PUDIERON CON ELLOS", px=64)
    pa(R, XO(7), 1260, 1012, 0.52, t_nun - 0.4, t_estos + 0.3, sem=S(), z=4)

    # frase 4: la Piedra del Sol (el cantero, la piedra en bruto que se vuelve la piedra tallada)
    pa(R, AX(6), 360, 1010, 0.9, t_estos - 0.1, t_cal, sem=S(), extra=[(0.3, "cincel", 0.5)])
    pa(R, AX(5), 760, 1010, 0.78, t_estos + 0.2, t_ps - 0.15, sem=S(), sale="borrar", d_out=0.3)
    piedra = gira(R, AX(4), 760, 840, 0.85, t_ps - 0.25, t_ent, lambda t: 0.05 * math.sin(t * 1.3), S(), entra="pluma",
                  sale="baja", sfx=[(0.0, "brillo", 0.45)])
    piedra.d_out = 1.0
    pa(R, FP.F("piedra_sol"), 1560, 1005, FP.s_para(0.5), t_ps - 0.2, t_monu, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_ps, t_cal - 0.2, "PIEDRA DEL SOL", snd=True)
    pa(R, XO(0), 1120, 1012, 0.45, t_fam - 0.3, t_eras - 0.2, sem=S(), z=3)

    # frase 5: no es un calendario: monumento al sol de casi 25 toneladas, con cuatro eras terminadas
    titulo(R, t_cal - 0.05, t_monu - 0.15, "CALENDARIO", px=80)
    tachar(R, t_cal + 0.6, t_monu - 0.15, "CALENDARIO", (960, 196), 80, sem=S())
    titulo(R, t_monu, t_eras - 0.2, "MONUMENTO AL SOL", px=78, snd=True)
    R.contador(t_25 - 0.2, t_ton + 0.3, 0, 25, (1480, 330), px=62, formato="CASI {} TONELADAS", hasta_t=t_eras)
    R.snd(t_ton, "impacto", 0.45)
    pa(R, AX(6), 330, 1010, 0.82, t_cal + 0.3, t_desp, sem=S(), flip=True, extra=[(0.4, "cincel", 0.35)])
    titulo(R, t_eras - 0.1, t_desp, "4 ERAS YA TERMINADAS", px=70)
    for k in range(4):           # las cuatro eras (soles) que ya terminaron: aparecen y se apagan
        pa(R, AX(4), 1190 + 160 * k, 560, 0.34, t_eras - 0.1 + 0.18 * k, t_term + 0.5 + 0.25 * k, sem=S(), z=3,
           extra=[(0.0, "pluck", 0.3)] if k % 2 == 0 else ())
        R.texto(t_eras + 0.2 * k, t_term + 0.5 + 0.25 * k, f"{k + 1}", (1190 + 160 * k, 610), px=44, d=0.3)
    pa(R, XO(5), 1580, 1012, 0.5, t_term - 0.4, t_reap + 0.3, sem=S(), z=3, extra=[(0.2, "ladrido", 0.3)])

    # frase 6: la enterraron; reapareció en 1790 arreglando la plaza
    R.snd(t_ent, "piedra", 0.5)
    titulo(R, t_ent, t_reap, "ENTERRADA", px=74)
    R.anio(t_1790, 1790)
    pa(R, AX(8), 820, 1012, 1.0, t_reap - 0.2, fin + 0.6, sem=S(), extra=[(0.0, "piedra", 0.4), (0.4, "pasos", 0.3)])
    pa(R, XS(5), 1300, 1012, 0.5, t_reap + 0.2, t_plaza, sem=S(), z=3, extra=[(0.1, "ladrido", 0.35)])
    pa(R, XO(0), 1300, 1012, 0.48, t_plaza, fin + 0.6, sem=S(), z=3)
    titulo(R, t_reap, t_plaza - 0.2, "17 DE DICIEMBRE DE 1790", px=66, snd=True)
    titulo(R, t_plaza - 0.1, fin + 0.6, "PLAZA MAYOR (HOY ZÓCALO)", px=66)
    R.texto(t_plaza + 0.5, fin + 0.6, "HOY ESTÁ EN EL MUSEO NACIONAL DE ANTROPOLOGÍA", (960, 300), px=36, d=0.7)


# ------------------------------------------------------------------ AHUÍZOTL
def _ahuizotl(R):
    e = "ahuizotl"
    i0, fin = INI(e), FIN(e)
    t_lle, t_ahu, t_gue, t_llev, t_fro, t_soc, t_cac = (T(e, "llego"), T(e, "ahuizotl", frase=0), T(e, "guerrero"), T(e, "llevo"),
                                                        T(e, "frontera"), T(e, "soconusco"), T(e, "cacao"))
    t_1487, t_tm, t_doble, t_huit, t_tlal, t_lluv = (T(e, "1487"), T(e, "templo mayor"), T(e, "doble"), T(e, "huitzilopochtli"),
                                                     T(e, "tlaloc"), T(e, "lluvia"))
    t_se, t_80, t_pers, t_4d = T(e, "se dice"), T(e, "ochenta"), T(e, "personas", frase=2), T(e, "cuatro")
    t_cifra, t_exag, t_cada, t_dia, t_pero, t_real = (T(e, "cifra"), T(e, "exagerada"), T(e, "cada"), T(e, "dia y noche"),
                                                      T(e, "pero"), T(e, "real"))
    t_2015, t_enc, t_huey, t_muro, t_cien, t_hom, t_muj, t_nin = (T(e, "2015"), T(e, "encontraron"), T(e, "huey"), T(e, "muro"),
                                                                  T(e, "cientos"), T(e, "hombres"), T(e, "mujeres"), T(e, "ninos"))
    t_para, t_sol, t_san, t_mov, t_sin, t_mundo = (T(e, "para los"), T(e, "sol"), T(e, "sangre"), T(e, "moviendose"),
                                                   T(e, "sin sacrificios"), T(e, "mundo"))
    t_ahu6, t_agua, t_acu, t_func, t_dem, t_inu = (T(e, "ahuizotl", frase=6), T(e, "agua", frase=6), T(e, "acueducto"),
                                                   T(e, "funciono"), T(e, "demasiado"), T(e, "inundo"))
    t_nom, t_anim, t_mit, t_pal, t_ahz, t_mol, t_mol2 = (T(e, "nombre"), T(e, "animal"), T(e, "mitico"), T(e, "palabra"),
                                                          T(e, "ahuizote"), T(e, "molesta"), T(e, "molesta", n=1))
    ten, soc, coy = CI["tenochtitlan"], CI["soconusco"], CI["coyoacan"]

    # cámara: centro → el imperio hasta el Soconusco → la isla de cerca (Templo Mayor, tzompantli) → isla con Coyoacán (acueducto)
    R.camara(i0 - 0.1, -98.95, 19.05, 1.2)
    R.camara(t_gue, -98.6, 18.85, 1.06)
    R.camara(t_llev + 0.4, -97.3, 17.9, 0.76)
    paseo(R, t_fro, t_1487, (-96.1, 17.0, 0.79), (-95.8, 16.8, 0.80), paso=1.6)
    R.camara(t_1487 + 1.1, -99.0, 19.3, 7.0)
    paseo(R, t_tm, t_para, foco(TM[0] + 0.0016, TM[1], 38, 280), foco(TM[0] + 0.0010, TM[1], 44, 280))
    R.camara(t_sin + 0.6, *foco(TM[0], TM[1], 30, 200))
    paseo(R, t_ahu6 + 0.6, t_inu + 0.6, (-99.150, 19.392, 13.5), (-99.146, 19.395, 15.0))
    paseo(R, t_nom + 0.4, fin - 0.2, (-99.142, 19.410, 17.0), (-99.138, 19.415, 19.0))

    # frase 0: Ahuízotl, el más guerrero, lleva el imperio al Soconusco
    R.anio(T(e, "1486"), 1486)
    R.terreno(i0 - 0.2, "imperio_1486", COL["imperio_1486"], 1.0, capa=30)
    R.terreno(t_llev, "imperio_1502", COL["imperio_1502"], 2.6, capa=30)
    pa(R, AH(0), 330, 1010, 1.0, i0 - 0.15, t_soc - 0.2, sem=S(), extra=[(0.0, "tambor", 0.4)])
    titulo(R, t_ahu, t_llev, "AHUÍZOTL", snd=True)
    pa(R, FP.F("ahuizotl_tovar"), 1590, 1005, FP.s_para(0.5), t_ahu - 0.2, t_llev + 0.6, entra="pluma", d_in=0.6, sem=S())
    pa(R, MI(7), 760, 1012, 0.52, t_gue - 0.2, t_soc, sem=S(), z=3, extra=[(0.2, "ladrido", 0.35)])
    R.texto(t_gue + 0.2, t_llev + 0.4, "EL MÁS GUERRERO", (760, 560), px=40, d=0.45)
    ruta = tramo(M.RUTAS["comercio_pochteca"], ten, soc)
    R.ruta(ruta, t_llev, 2.6, ancho=5.0, t1=t_1487, flecha=True)
    grupo_ciclo(R, C_GUER, ruta[-4:-1] + [(soc[0] - 0.55, soc[1] + 0.35)], t_llev + 0.3, 3.4, n=3, ancho=60, t1=t_cac + 0.6, s=0.58,
                sem=S(), fps=12)
    R.snd(t_llev, "batalla", 0.35)
    R.ciudad(t_soc - 0.1, t_1487, "soconusco", soc, "SOCONUSCO", "abajo", 44)
    R.texto(t_fro, t_1487, "FRONTERA CON GUATEMALA", (1440, 300), px=40, d=0.5)
    ga(R, AH(9), soc, t_cac - 0.6, t_1487 + 0.2, s=0.7, off=(-150, -40), sem=S(), z=3, zs=0.4, extra=[(0.0, "crece", 0.35)])
    pa(R, FP.F("mendoza_tributo_47r"), 400, 1005, FP.s_para(0.5), t_soc - 0.1, t_1487 + 1.4, entra="pluma", d_in=0.6, sem=S())
    R.texto(t_cac, t_1487 + 0.6, "TIERRA DE CACAO", (960, 196), px=64, d=0.5)
    pa(R, FP.F("cacao_mazorca"), 1040, 1005, FP.s_para(0.38), t_cac - 0.3, t_tm - 0.6, entra="pluma", d_in=0.5, sem=S())
    ciclo_pant(R, C_XOLO, -200, 2050, 1012, t_1487 + 0.3, 3.2, t1=t_tm + 0.6, s=0.45, sem=S(), z=4, fps=13)
    R.snd(t_cac, "monedas", 0.4)

    # frase 1: el Templo Mayor doble (Tláloc al norte/izquierda, Huitzilopochtli al sur/derecha)
    R.anio(t_1487, 1487)
    ga(R, AH(1), TM, t_tm - 0.4, t_para, s=1.0, sem=S(), z=1, zs=0.0, flip=True, entra="sube", dy=500,
       extra=[(0.0, "caracol", 0.5)])
    R.sello(t_tm + 0.3, "piramide_mx", "TEMPLO MAYOR", color=(176, 56, 46))
    titulo(R, t_doble - 0.2, t_huit - 0.1, "PIRÁMIDE DOBLE", px=78, snd=True)
    pa(R, MG(3), 1590, 1010, 0.95, t_huit - 0.15, t_se + 0.2, sem=S(), extra=[(0.0, "tambor", 0.35)])
    R.texto(t_huit, t_se, "HUITZILOPOCHTLI", None, px=40, geo=TM, off=(170, -470))
    pa(R, AH(2), 330, 1010, 0.95, t_tlal - 0.15, t_se + 0.2, sem=S(), extra=[(t_lluv - t_tlal, "trueno", 0.35)])
    R.texto(t_tlal, t_se, "TLÁLOC", None, px=44, geo=TM, off=(-170, -470))
    pa(R, XO(1), 1180, 1012, 0.42, t_doble, t_huit + 1.4, sem=S(), z=3)

    # frase 2: «80 000 en cuatro días» (contador) — frase 3: EXAGERADO; una cada 4 s; pero sí fue real
    pa(R, AH(4), 330, 1010, 0.92, t_se - 0.1, t_cifra + 1.4, sem=S(), extra=[(0.3, "tambor", 0.4)])
    R.contador(t_80 - 0.2, t_pers + 0.3, 0, 80000, (960, 230), px=92, formato="{:,} PERSONAS", hasta_t=t_pero)
    R.texto(t_4d, t_cifra + 0.6, "EN 4 DÍAS", (960, 345), px=56, d=0.4)
    pa(R, XO(3), 1600, 1012, 0.52, t_se + 0.6, t_exag, sem=S(), z=3, extra=[(0.3, "gemido_perro", 0.35)])
    tachar(R, t_exag - 0.1, t_pero, "80.000 PERSONAS", (960, 230), 92, sem=S())
    pa(R, EXAGERADO, 960, 345, 1.0, t_exag, t_pero, sem=S(), z=6, entra="pop", extra=[(0.0, "sello", 0.6)])
    R.act(lambda t: cronometro(t), pos=(1590, 820, 1.1), t_in=t_cada - 0.2, d_in=0.4, entra="pop", sem=S(), t_out=t_pero, z=3,
          sfx=[(0.0, "pop", 0.3)])
    R.texto(t_cada, t_dia - 0.1, "UNA CADA 4 SEGUNDOS", (1590, 560), px=40, d=0.5)
    R.texto(t_dia, t_pero + 0.2, "DÍA Y NOCHE", (1590, 560), px=48, d=0.4)
    pa(R, XO(2), 330, 1012, 0.55, t_cifra + 1.4, t_real + 0.8, sem=S(), z=3)
    pa(R, REAL, 960, 345, 1.0, t_real - 0.3, t_2015 + 0.3, sem=S(), z=6, extra=[(0.0, "sello", 0.5)])

    # frase 4: 2015, el Huey Tzompantli (cráneos de hombres, mujeres y niños)
    R.anio(t_2015, 2015)
    ga(R, AH(3), TM, t_huey - 0.3, t_para, s=0.62, off=(-380, 30), sem=S(), z=2, zs=0.0, extra=[(0.0, "piedra", 0.4)])
    titulo(R, t_huey, t_cien - 0.1, "HUEY TZOMPANTLI", snd=True)
    R.texto(t_enc, t_hom, "CALLE GUATEMALA 24", None, px=34, geo=TM, off=(-380, 70))
    pa(R, FP.F("huey_tzompantli"), 1630, 1005, FP.s_para(0.38), t_2015, t_cien + 0.2, entra="pluma", d_in=0.6, sem=S())
    pa(R, FP.F("maqueta_tzompantli"), 1630, 1005, FP.s_para(0.38), t_cien + 0.1, t_sol, entra="pluma", d_in=0.6, sem=S())
    R.texto(t_cien, t_hom - 0.1, "CIENTOS DE CRÁNEOS", (960, 196), px=62, d=0.5)
    R.texto(t_hom, t_sol - 0.3, "HOMBRES", (520, 196), px=56, d=0.35)
    R.texto(t_muj, t_sol - 0.3, "MUJERES", (960, 196), px=56, d=0.35)
    R.texto(t_nin, t_sol - 0.3, "NIÑOS", (1400, 196), px=56, d=0.35)
    pa(R, XO(3), 1060, 1015, 0.42, t_muro, t_sol, sem=S(), z=4)

    # frase 5: el sol necesitaba sangre; sin sacrificios, el mundo se acababa
    titulo(R, t_sol, t_sin - 0.15, "EL SOL NECESITABA SANGRE", px=66)
    gira(R, AX(4), 960, 720, 0.8, t_sol - 0.2, t_mundo + 0.6,
         lambda t: 0.25 * (t - t_sol) + (0.08 * math.sin(t * 40) * prog(t, t_mundo - 0.2, t_mundo) if t > t_mundo - 0.2 else 0),
         S(), sale="baja", sfx=[(0.0, "crece", 0.4)])
    pa(R, MG(3), 330, 1010, 0.95, t_para - 0.1, t_ahu6, sem=S())
    pa(R, FP.F("tzompantli_duran"), 1580, 1005, FP.s_para(0.5), t_san - 0.2, t_ahu6 + 0.2, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_sin - 0.05, t_ahu6, "SIN SACRIFICIOS: FIN DEL MUNDO", px=60)
    R.snd(t_mundo, "trueno", 0.5)

    # frase 6: el acueducto de Coyoacán y la inundación de 1499
    R.anio(t_ahu6, 1499)
    pa(R, AH(0), 330, 1010, 0.95, t_ahu6 - 0.1, t_func, sem=S(), extra=[(0.0, "pop", 0.3)])
    ciudad(R, t_agua - 0.3, t_nom, "coyoacan", "COYOACÁN", "izq", 40)
    ciudad(R, t_agua, t_nom, "tenochtitlan", "TENOCHTITLAN", "der", 40)
    canal = [coy, CI["xoloc"], (-99.132, 19.426), ten]
    R.rio(canal, t_acu - 0.6, 1.8, AGUA_INUND, ancho=16, t1=t_nom)
    R.snd(t_acu - 0.5, "agua_lago", 0.4)
    ga(R, M1(4), CI["xoloc"], t_acu - 0.3, t_nom, s=0.5, off=(-230, 40), sem=S(), z=2, zs=0.0, extra=[(0.0, "piedra", 0.35)])
    titulo(R, t_acu, t_func - 0.1, "UN NUEVO ACUEDUCTO", px=70, snd=True)
    titulo(R, t_dem - 0.1, t_nom - 0.2, "...DEMASIADO BIEN", px=72)
    R.terreno(t_inu - 0.4, "isla_1519", AGUA_INUND, 1.0, capa=50, rej="mx")
    R.terreno(t_nom + 0.6, None, AGUA_INUND, 0.8, capa=50, rej="mx")
    R.snd(t_inu, "inundacion", 0.55)
    ga(R, AH(6), ten, t_inu - 0.1, t_nom + 0.4, s=0.55, off=lambda t: (-140, 250 + 8 * math.sin(t * 3)), sem=S(), z=3, zs=0.0,
       entra="sube", dy=300)
    ga(R, AH(7), ten, t_inu + 0.2, t_nom + 0.4, s=0.55, off=lambda t: (150, 230 + 8 * math.sin(t * 3 + 1)), sem=S(), z=3, zs=0.0,
       entra="sube", dy=300)
    pa(R, XS(2), lambda t: 1600, lambda t: 1000 - 60 * abs(math.sin(t * 4.0)), 0.5, t_inu - 0.2, t_nom + 0.5, sem=S(), z=4,
       extra=[(0.3, "ladrido", 0.35)])

    # frase 7: el ahuizotl mítico y el «ahuizote» que molesta sin parar
    def x_ahz(t):
        return 1060 - 300 * max(0.0, math.sin((t - t_mol) * 3.2)) * prog(t, t_mol - 0.4, t_mol)
    pa(R, AH(5), x_ahz, lambda t: 1010, 0.85, t_nom - 0.2, fin + 0.6, sem=S(), z=3, extra=[(t_anim - t_nom, "agua_lago", 0.35)])
    titulo(R, t_anim, t_pal - 0.2, "ANIMAL DE AGUA MÍTICO", px=66)
    pa(R, FP.F("ahuizotl_lapida"), 1590, 1005, FP.s_para(0.46), t_anim - 0.1, t_ahz + 0.4, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_ahz, fin + 0.6, "AHUIZOTE", px=96, snd=True)
    R.texto(t_mol - 0.4, fin + 0.6, "ALGUIEN QUE MOLESTA Y MOLESTA", (960, 310), px=46, d=0.6)
    pa(R, XO(7), 380, 1012, 0.6, t_pal - 0.3, fin + 0.6, sem=S(), z=4, extra=[(t_mol2 - t_pal + 0.3, "ladrido", 0.4)])


# ------------------------------------------------------------------ MOCTEZUMA II
def _moctezuma2(R):
    e = "moctezuma2"
    i0, fin = INI(e), FIN(e)
    t_1502, t_tro, t_moc, t_jov, t_seg = T(e, "1502"), T(e, "trono"), T(e, "moctezuma xocoyotzin"), T(e, "joven"), T(e, "segundo")
    t_sac, t_gue, t_pro, t_nad = T(e, "sacerdote"), T(e, "guerrero"), T(e, "protocolo"), T(e, "nadie")
    t_zoo, t_jag, t_agu, t_ser, t_avi, t_paj = (T(e, "zoologico"), T(e, "jaguares"), T(e, "aguilas"), T(e, "serpientes"),
                                                T(e, "aviarios"), T(e, "pajaros"))
    t_ten, t_75, t_200, t_hab, t_seg2, t_sev, t_roma, t_aquel = (T(e, "tenochtitlan"), T(e, "setenta"), T(e, "doscientos"),
                                                                 T(e, "habitantes"), T(e, "segun quien"), T(e, "sevilla"), T(e, "roma"),
                                                                 T(e, "aquel"))
    t_imp, t_cob, t_dec, t_gol, t_pac = T(e, "imperio", frase=4), T(e, "cobraba"), T(e, "decenas"), T(e, "golfo"), T(e, "pacifico")
    t_ent, t_pres, t_com, t_tem, t_ard, t_muj, t_llo, t_noc = (T(e, "entonces"), T(e, "presagios", frase=5), T(e, "cometa"),
                                                               T(e, "templo"), T(e, "ardio"), T(e, "mujer"), T(e, "lloraba"),
                                                               T(e, "noche"))
    t_ojo, t_esc, t_conq, t_expl = T(e, "ojo"), T(e, "escribieron"), T(e, "conquista"), T(e, "explicar")
    t_xolo, t_aull = T(e, "xolo"), T(e, "aullando")

    # cámara: las casas de Moctezuma → la ciudad → el imperio de 1519 entero → la isla de noche
    paseo(R, i0 - 0.15, t_zoo - 0.4, foco(PALACIO[0], PALACIO[1], 30, 200), foco(PALACIO[0] - 0.0015, PALACIO[1] + 0.0008, 36, 200))
    paseo(R, t_zoo + 0.6, t_ten - 0.6, foco(PALACIO[0] - 0.002, PALACIO[1] + 0.001, 34, 200), foco(PALACIO[0], PALACIO[1], 28, 200))
    paseo(R, t_ten + 0.2, t_aquel, (-99.137, 19.425, 16.0), (-99.133, 19.430, 12.0))
    paseo(R, t_imp + 0.6, t_ent, (-97.40, 18.15, 0.58), (-97.35, 18.10, 0.60), paso=1.6)
    paseo(R, t_pres, t_xolo, foco(TM[0], TM[1], 14.0, 120), foco(TM[0], TM[1], 18.0, 120))
    R.camara(fin - 0.25, *foco(TM[0], TM[1], 20.0, 120))

    R.anio(t_1502, 1502)
    R.terreno(i0 - 0.2, "imperio_1502", COL["imperio_1502"], 0.8, capa=30)
    # frase 0: Moctezuma Xocoyotzin sube al trono
    pa(R, MO(0), 960, 1012, 1.15, i0 - 0.15, t_zoo - 0.2, sem=S(), extra=[(0.0, "caracol", 0.4), (t_tro - i0, "fanfarria", 0.3)])
    titulo(R, t_moc, t_seg - 0.1, "MOCTEZUMA XOCOYOTZIN", px=72, snd=True)
    titulo(R, t_seg + 0.25, t_sac - 0.1, "MOCTEZUMA II", px=84)
    pa(R, FP.F("moctezuma2_tovar"), 1590, 1005, FP.s_para(0.5), t_moc - 0.3, t_seg + 0.6, entra="pluma", d_in=0.6, sem=S())
    pa(R, XO(0), 330, 1012, 0.55, t_tro - 0.3, t_seg + 0.1, sem=S(), z=3, extra=[(0.2, "ladrido", 0.3)])

    # frase 1: sacerdote y guerrero; protocolo: nadie lo mira a la cara
    pa(R, FP.F("moctezuma2_petroglifo"), 360, 1005, FP.s_para(0.44), t_seg + 0.2, t_pro + 0.2, entra="pluma", d_in=0.6, sem=S())
    pa(R, FP.F("moctezuma2_duran"), 1580, 1005, FP.s_para(0.40), t_sac - 0.1, t_pro + 0.4, entra="pluma", d_in=0.6, sem=S())
    R.texto(t_sac, t_pro - 0.1, "SACERDOTE", (620, 196), px=56, d=0.4)
    R.texto(t_gue, t_pro - 0.1, "Y GUERRERO", (1300, 196), px=56, d=0.4)
    pa(R, MO(1), 360, 1012, 0.9, t_pro + 0.2, t_zoo - 0.2, sem=S(), extra=[(0.0, "pop", 0.3)])
    pa(R, MO(1), 1560, 1012, 0.9, t_pro + 0.5, t_zoo - 0.2, sem=S(), flip=True)
    titulo(R, t_pro, t_nad - 0.1, "PROTOCOLO", px=78)
    titulo(R, t_nad, t_zoo - 0.1, "NADIE LO MIRA A LA CARA", px=66)
    pa(R, XO(3), 1250, 1015, 0.42, t_nad, t_zoo, sem=S(), z=4, extra=[(0.1, "gemido_perro", 0.3)])

    # frase 2: el zoológico (jaguares, águilas, serpientes) y el aviario
    titulo(R, t_zoo, t_avi - 0.1, "ZOOLÓGICO", snd=True)
    pa(R, MO(2), 360, 1012, 0.92, t_jag - 0.2, t_ten - 0.3, sem=S(), extra=[(0.0, "jaguar", 0.45)])
    pa(R, FU(0), 760, 1012, 0.72, t_agu - 0.15, t_ten - 0.2, sem=S(), extra=[(0.0, "aguila", 0.4)])
    pa(R, CH(4), 1140, 1012, 0.62, t_ser - 0.15, t_ten - 0.1, sem=S(), extra=[(0.0, "cascabel", 0.4)])
    pa(R, XO(2), 1620, 1012, 0.5, t_jag + 0.2, t_avi - 0.3, sem=S(), z=4, extra=[(0.2, "gemido_perro", 0.3)])
    pa(R, MO(3), 1150, 640, 0.6, t_avi - 0.15, t_ten + 0.1, sem=S(), z=4, extra=[(0.0, "brillo", 0.35)])
    pa(R, FP.F("florentino_totocalli"), 1600, 1005, FP.s_para(0.34), t_avi - 0.2, t_ten + 0.3, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_avi, t_ten - 0.2, "AVIARIO", px=78)

    # frase 3: entre 75 000 y 200 000 habitantes; más que Sevilla y Roma
    pa(R, MO(7), 400, 1012, 1.0, t_ten - 0.2, t_imp - 0.2, sem=S(), extra=[(0.0, "agua_lago", 0.35)])
    ciudad(R, t_ten, t_roma - 0.3, "tenochtitlan", "TENOCHTITLAN", "arriba", 44)
    R.contador(t_75 - 0.1, t_75 + 0.7, 0, 75000, (560, 230), px=74, formato="{:,}", hasta_t=t_seg2 + 0.8)
    R.texto(t_200 - 0.4, t_seg2 + 0.8, "A", (800, 230), px=56, d=0.3)
    R.contador(t_200 - 0.1, t_200 + 0.6, 75000, 200000, (1320, 230), px=74, formato="{:,} HABITANTES", hasta_t=t_seg2 + 0.8)
    pa(R, ME(6), 1560, 1012, 0.95, t_75 - 0.2, t_imp - 0.2, sem=S(), extra=[(0.0, "multitud", 0.3)])
    R.texto(t_seg2, t_sev - 0.2, "SEGÚN QUIÉN HAGA LA CUENTA", (960, 330), px=42, d=0.5)
    titulo(R, t_sev - 0.2, t_imp - 0.1, "MÁS GRANDE QUE SEVILLA", px=70)
    R.texto(t_roma, t_imp - 0.1, "Y QUE ROMA", (960, 310), px=60, d=0.4)
    R.snd(t_sev, "fanfarria", 0.3)
    ciclo_pant(R, C_XOLO, 2000, -200, 1012, t_seg2 - 0.4, 4.2, t1=t_imp, s=0.42, sem=S(), z=4, fps=13)

    # frase 4: el imperio de 1519 completo, del Golfo al Pacífico, partido en provincias
    R.anio(t_imp, 1519)
    R.terreno(t_imp - 0.2, "imperio_1519", COL["imperio_1519"], 1.6, capa=30)
    pa(R, MO(0), 330, 1012, 1.0, t_imp - 0.2, t_com - 0.2, sem=S())
    pa(R, XO(7), 1600, 1012, 0.55, t_ent, t_com + 0.2, sem=S(), z=4, extra=[(0.3, "gemido_perro", 0.3)])
    R.romper("provincias", t_dec - 0.4, t_dec + 0.4, t_pac + 0.6, t_ent + 0.6, capa=30, rej="mx")
    R.snd(t_dec - 0.3, "crece", 0.4)
    for k, (n, dib, s) in enumerate((("cuetlaxtlan", TR(1), 0.5), ("tochtepec", TR(6), 0.45), ("coyolapan", TR(4), 0.5),
                                     ("tlapan", TR(0), 0.5), ("tlachco", TR(3), 0.5), ("xilotepec", VI(12), 0.42),
                                     ("tepeaca", TR(2), 0.5))):
        ga(R, dib, CI[n], t_cob + 0.25 * k, t_ent + 0.2, s=s, off=(0, 10), sem=S(), z=3, zs=0.4,
           extra=[(0.0, "pop", 0.25)] if k % 3 == 0 else ())
    R.contador(t_dec - 0.2, t_dec + 0.8, 0, 38, (1450, 980), px=70, formato="{} PROVINCIAS", hasta_t=t_ent + 0.4)
    R.texto(t_gol - 0.1, t_ent + 0.3, "GOLFO DE MÉXICO", None, px=40, geo=(-94.9, 19.5))
    R.texto(t_pac - 0.1, t_ent + 0.3, "OCÉANO PACÍFICO", None, px=40, geo=(-98.0, 15.9))
    R.snd(t_gol, "ola", 0.3)

    # frase 5: los presagios (LEYENDA): cometa, templo en llamas, la mujer que llora
    R.snd(t_ent, "viento_frio", 0.35)
    titulo(R, t_pres - 0.1, t_com - 0.1, "LOS PRESAGIOS", px=80, snd=True)
    pa(R, LEYENDA, 1640, 385, 1.0, t_pres, t_ojo + 0.4, sem=S(), z=6, extra=[(0.0, "sello", 0.5)])
    pa(R, MO(4), lambda t: 1700 - 1000 * e_out(prog(t, t_com - 0.2, t_tem + 1.6)), lambda t: 700 - 120 * prog(t, t_com - 0.2, t_tem + 1.6),
       0.85, t_com - 0.2, t_muj + 0.3, sem=S(), z=3, extra=[(0.0, "cometa", 0.5)])
    R.texto(t_com, t_tem - 0.1, "UN COMETA", (960, 196), px=62, d=0.4)
    pa(R, MO(5), 1180, 1012, 0.95, t_tem - 0.1, t_ojo + 0.2, sem=S(), z=2, extra=[(t_ard - t_tem, "fuego", 0.45)])
    R.texto(t_tem, t_muj - 0.1, "UN TEMPLO QUE ARDE SOLO", (960, 196), px=56, d=0.5)
    pa(R, MO(6), 360, 1012, 1.0, t_muj - 0.15, t_esc, sem=S(), z=3, extra=[(t_llo - t_muj, "llanto", 0.45)])
    R.texto(t_muj, t_ojo - 0.1, "UNA MUJER QUE LLORA DE NOCHE", (960, 196), px=52, d=0.5)
    pa(R, XO(2), 760, 1012, 0.48, t_noc - 0.2, t_esc, sem=S(), z=4)

    # frase 6: se escribieron después de la conquista; explicar lo inexplicable
    pa(R, ME(7), 1500, 1012, 0.85, t_ojo - 0.1, t_xolo, sem=S(), extra=[(0.3, "escribir", 0.4)])
    titulo(R, t_ojo, t_xolo - 0.1, "ESCRITOS DESPUÉS DE 1521", px=66, snd=True)
    R.texto(t_esc + 0.4, t_xolo - 0.1, "(SAHAGÚN, HACIA 1555-1577)", (960, 300), px=38, d=0.5)
    pa(R, FP.F("presagio_bicefalo"), 420, 1005, FP.s_para(0.46), t_esc - 0.1, t_xolo, entra="pluma", d_in=0.6, sem=S())
    R.texto(t_expl, t_xolo, "¿?", (760, 560), px=150, d=0.4)

    # frase 7: Xolo llevaba días aullando
    pa(R, XO(4), 960, 1012, 1.05, t_xolo - 0.2, fin + 0.8, sem=S(), z=4, extra=[(t_aull - t_xolo, "aullido", 0.6)])
    R.texto(t_xolo + 0.2, fin + 0.8, "XOLO", (960, 520), px=60, d=0.4)
    pa(R, MO(4), 1560, 600, 0.55, t_xolo + 0.1, fin + 0.8, sem=S(), z=2, rot=0.05)
