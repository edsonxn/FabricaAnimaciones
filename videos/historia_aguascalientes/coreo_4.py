# -*- coding: utf-8 -*-
"""Coreografía (4/4): siglo XX (la Presa Calles y el pueblo hundido de San José de Gracia, el Cristo Roto, viñedos y Feria de la Uva,
la guayaba de Calvillo, Nissan, el INEGI que llegó tras el sismo de 1985 y el estado en cifras), la ruta para visitar (mapa turístico
de la capital y los Pueblos Mágicos) y el cierre (del charco caliente y los 16 soldados al estado lleno de historia; el beso y
«suscríbete a Cronopapel»).

Rango de semillas 900-1199 · capas de terreno 30-39 (30 sin uso, 31 presa, 32 viñedos, 33 sismo, 34 estado/municipios, 36 cierre).
El mapa turístico de la capital EXAGERA las distancias (×7 desde la Plaza de la Patria): con la rejilla de ~160 m/px los barrios del
centro caben en ~140 px aun con el zoom máximo; los lugares lejanos (Cerro del Muerto, pueblos) van en su sitio real."""
import math

import numpy as np

import boceto as B
import foto_peg as FP
import mapa as M
import obj_c as OC
from core import FIN, INI, T, ZREF
from coreo_peg import ciclo_pant
from coreo_util import CI, COL, ciudad, ga, pa, titulo
from motor import e_inout, e_out, lerp, prog
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (número = el de piezas/<hoja>/_indice.jpg)
CH = lambda n, **k: P("01_chichimecas_hoja", n, **k)   # 0 arquero guachichil … 6 nopal+mezquite
PL = lambda n, **k: P("02_plata_hoja", n, **k)         # 0 carreta de plata
FU = lambda n, **k: P("03_fundacion_hoja", n, **k)     # 1 colono, 2 colona, 4 poza termal, 5 jacal
CO = lambda n, **k: P("04_colonia_hoja", n, **k)       # 0 catedral, 1 palacio, 2 San Marcos, 5 mina, 6 túnel de agua, 9 vacas
XI = lambda n, **k: P("05_xix_hoja", n, **k)           # 4 tina, 6 escudo con labios
AR = lambda n, **k: P("06_arte_hoja", n, **k)          # 0 grabador (Posada), 2 catrina, 5 pintor, 6 cuadro de la diosa
PF = lambda n, **k: P("07_porfiriato_hoja", n, **k)    # 0 locomotora, 1 humo, 7 teatro, 8 templo de San Antonio
RV = lambda n, **k: P("08_revolucion_hoja", n, **k)    # 0 Villa
SX = lambda n, **k: P("09_sigloxx_hoja", n, **k)       # 0 presa, 1 campanario inundado, 2 Cristo Roto, 3 lancha, 4 uvas, 5 barrica,
#                                                        6 guayabas, 7 guayabo, 8 motor, 9 coche, 10 INEGI
TU = lambda n, **k: P("10_turismo_hoja", n, **k)       # 0 turista, 1 familia, 2 tina con pato, 3 mariachi, 4 rueda, 5 charro, 6 letrero, 7 autobús
C_SOLDADO = ciclo("12_soldado_marcha")

AGUA = (96, 160, 206)
SECA = (176, 156, 112)
VINAS = (128, 92, 140)

# mapa turístico de la capital (distancias ×7 desde la Plaza de la Patria)
PZ = CI["plaza_patria"]
K_TUR = 10.0
SAN_ANTONIO = (-102.2912, 21.8853)      # aprox. (templo de San Antonio, Pedro Parga y Zaragoza)


def _tz(geo):
    return (PZ[0] + K_TUR * (geo[0] - PZ[0]), PZ[1] + K_TUR * (geo[1] - PZ[1]))


T_PLAZA, T_ENCINO, T_SANANT, T_SANMAR, T_OJO = PZ, _tz(CI["encino"]), _tz(SAN_ANTONIO), _tz(CI["san_marcos"]), _tz(CI["ojocaliente"])
T_MUSEO = (T_SANANT[0] + 0.040, T_SANANT[1] + 0.006)   # Museo de Aguascalientes: frente a San Antonio (separado para que se lea)
NISSAN = (-102.262, 21.800)             # aprox. (planta A1, al sur de la ciudad)
INEGI = (-102.282, 21.852)              # aprox. (sede del INEGI, al sur del centro)


# ------------------------------------------------------------------ ayudas
class _Hunde:
    """Pegatina que se hunde en el agua: se dibuja más abajo una fracción f de su alto y se corta en la línea del agua (fija);
    sobre la línea, una onda de agua pintada a crayón."""

    def __init__(self, peg, f, linea=0.13):
        self.p, self.f, self.linea = peg, f, linea

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, u=1.0, fase_=0, semilla=0, peg=True, **kw):
        hp = self.p.alto * s
        n0 = len(getattr(hoja, "fotos", []))
        self.p.dibujar(hoja, x, y + self.f * hp, s, rot, flip, u, fase_, semilla, peg=False, **kw)
        if len(getattr(hoja, "fotos", [])) <= n0:
            return
        rgb, a, x0, y0 = hoja.fotos[-1]
        hh, ww = a.shape
        yl = y - self.linea * hp                     # línea del agua en pantalla
        corte = int(round(yl - y0))
        if corte < hh:
            rgb, a = rgb.copy(), a.copy()
            rgb[max(0, corte):] = 0
            a[max(0, corte):] = 0
            hoja.fotos[-1] = (rgb, a, x0, y0)
        if peg:
            hoja.peg_mascara((a > 0.5).astype(np.uint8) * 255, x0, y0)
        if u > 0.5:
            rx, ry = 0.46 * ww, max(6.0, 0.06 * hp)
            hoja.silueta(B.circ(x, yl, rx + 8, n=40, ry=ry + 8))
            hoja.relleno(B.circ(x, yl, rx, n=40, ry=ry), AGUA, semilla + 3, fase_, 1.0, sp=7, alfa=255)
            hoja.trazo(B.circ(x, yl, rx, n=44, ry=ry), 4.0, semilla + 5, fase_, 1.0, amp=1.0)
            for k in (-1, 1):
                xs = x + k * 0.28 * ww
                hoja.trazo(np.array([(xs - 22, yl + 2), (xs, yl - 4), (xs + 22, yl + 2)]), 3.0, semilla + 7 + k, fase_, 1.0, amp=0.6, v=120)


class _Volteo:
    """La misma pegatina volteada (para vehículos cuya dirección cambia en el camino)."""

    def __init__(self, peg):
        self.p = peg

    def dibujar(self, hoja, x, y, s=1.0, rot=0.0, flip=False, *a, **k):
        self.p.dibujar(hoja, x, y, s, rot, not flip, *a, **k)


def _claves(cl):
    """t -> (lon, lat) por claves [(t, (lon, lat))] con suavizado en cada tramo (caminante que se detiene en cada lugar)."""
    def f(t):
        if t <= cl[0][0]:
            return cl[0][1]
        for (ta, a), (tb, b) in zip(cl, cl[1:]):
            if t <= tb:
                u = e_inout(prog(t, ta, tb))
                return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
        return cl[-1][1]
    return f


_CL = []


def _cam(R, t, lon, lat, z):
    """Clave de cámara (se guarda; `_volcar_cam` la escribe)."""
    _CL.append((t, lon, lat, z))


def _volcar_cam(R, paso=2.0):
    """Escribe las claves de este tramo COMPENSANDO la deriva lenta de CamPath (±190 px en x, ±130 px en y a cualquier zoom, con
    periodos de 15-20 s): sin esto, entre dos claves alejadas el lugar encuadrado se iba a un borde (el estado o la capital caían
    arriba y los rótulos chocaban). Entre claves se añaden claves intermedias (≤ `paso` s, mismo suavizado e_inout) también
    compensadas, así la deriva solo queda como un vaivén pequeño y la cámara sigue viva."""
    cl = sorted(_CL)
    pts = []
    for (ta, la, pa_, za), (tb, lb, pb, zb) in zip(cl, cl[1:]):
        n = max(1, int(math.ceil((tb - ta) / paso)))
        for i in range(n):
            u = e_inout(i / n)
            pts.append((ta + (tb - ta) * i / n, lerp(la, lb, u), lerp(pa_, pb, u), math.exp(lerp(math.log(za), math.log(zb), u))))
    pts.append(cl[-1])
    for t, lon, lat, z in pts:
        R.camara(t, lon - 0.30 * math.sin(t * 0.43) / z, lat - 0.20 * math.sin(t * 0.31 + 1.0) / z, z)


def _pin(R, t0, t1, geo, txt=None, lado="arriba", px=40, t1_txt=None, sfx=False):
    """Punto de tinta en geo (lon, lat) + nombre (que puede borrarse antes que el punto)."""
    R.ciudad(t0, t1, "pin", geo, None, sfx=sfx)
    if txt:
        mw = B.ancho_texto(txt, px)
        dx, dy = {"arriba": (0, -50), "abajo": (0, 52), "der": (28 + mw / 2, 0), "izq": (-28 - mw / 2, 0)}[lado]
        R.texto(t0 + 0.1, t1 if t1_txt is None else t1_txt, txt, None, px=px, d=0.45, geo=geo, off=(dx, dy))


def _regla(R, t0, t1, geo, off, s, zs, txt):
    """Cinta de medir vertical junto a una pegatina anclada (su alto en pantalla) con la cifra a media altura."""
    def f(h, cam, t, fs, te):
        if t < t0 or t > t1 + 0.3:
            return
        x, y = cam.pant(*geo)
        hp = 400.0 * s * min((cam.z / ZREF) ** zs, 2.0)
        x, y = x + off[0], y + off[1]
        u = e_out(prog(t, t0, t0 + 0.8))
        v = int(255 * (1 - prog(t, t1, t1 + 0.3)))
        if v <= 0:
            return
        y_top = y - hp * u
        h.trazo(np.array([(x, y), (x, y_top)]), 4.5, 951, fs, 1.0, amp=0.8, v=v)
        for yy in (y, y_top):
            h.trazo(np.array([(x - 16, yy), (x + 16, yy)]), 4.5, 952, fs, 1.0, amp=0.6, v=v)
        if u > 0.6:
            from core import rotulo
            rotulo(h, txt, x - 20 - B.ancho_texto(txt, 60) / 2, y - hp * 0.5, 60, prog(t, t0 + 0.5, t0 + 0.9), fs, v, te)
    R.frente.append(R._acot(f, t0))


def _tc(prev, e):
    """Justo después del punto medio del cambio de escena: la primera pegatina ya no espera a INI (el hueco quedaba con mapa solo)."""
    return (FIN(prev) + INI(e)) / 2 + 0.05


def cortes(R):
    pass


def construir(R):
    _CL.clear()
    _siglo20(R)
    _ruta(R)
    _cierre(R)
    _volcar_cam(R)


# ------------------------------------------------------------------ SIGLO XX
def _siglo20(R):
    e = "siglo20"
    i0 = INI(e)
    # frases 0-2: la presa y el pueblo hundido
    t_1927, t_emp, t_pre, t_pri, t_rie = T(e, "1927"), T(e, "empezo"), T(e, "presa calles"), T(e, "primeras"), T(e, "riego")
    t_cub, t_sj, t_1930, t_aba, t_gen, t_fun = (T(e, "cubrieron"), T(e, "san jose"), T(e, "1930"), T(e, "abandonado"), T(e, "gente"),
                                                T(e, "fundarlo"))
    t_seq, t_baj, t_aso, t_res = T(e, "sequia"), T(e, "baja"), T(e, "asoman"), T(e, "restos")
    # frases 3-4: el Cristo Roto
    t_2006, t_isl, t_lev, t_cri, t_25, t_bra = T(e, "2006"), T(e, "isla"), T(e, "levanto"), T(e, "cristo"), T(e, "25"), T(e, "brazo")
    t_lle, t_lan = T(e, "llegar"), T(e, "lancha")
    # frases 5-6: uva y guayaba
    t_med, t_vin, t_ciu, t_fer = T(e, "mediados"), T(e, "vinedos"), T(e, "ciudad"), T(e, "feria")
    t_cal, t_hue, t_ter = T(e, "calvillo"), T(e, "huertos"), T(e, "tercio")
    # frases 7-9: Nissan, el sismo y el INEGI
    t_1982, t_nis, t_mot, t_18 = T(e, "1982"), T(e, "nissan"), T(e, "motor"), T(e, "18")
    t_sis, t_1985, t_ine, t_ins, t_mud, t_3000 = (T(e, "terremoto"), T(e, "1985"), T(e, "inegi"), T(e, "instituto"), T(e, "mudo"),
                                                 T(e, "3000"))
    t_edi, t_pir, t_1989 = T(e, "edificio"), T(e, "piramides"), T(e, "1989")
    # frase 10: el estado en cifras
    t_hoy, t_cua, t_5616, t_12, t_14, f10 = T(e, "hoy", frase=10), T(e, "cuarto"), T(e, "5616"), T(e, "11"), T(e, "14"), INI(e, 10)
    fin = FIN(e)

    # ---- cámara
    _cam(R, i0 - 0.2, -102.36, 22.05, 1.75)
    _cam(R, t_pre - 0.2, -102.44, 22.14, 3.4)
    _cam(R, t_rie - 0.2, -102.40, 22.145, 3.1)
    _cam(R, t_cub - 0.1, -102.438, 22.149, 5.2)
    _cam(R, t_seq, -102.437, 22.147, 5.6)
    _cam(R, t_2006, -102.437, 22.158, 5.0)
    _cam(R, t_lev - 0.3, -102.434, 22.165, 5.6)
    _cam(R, t_lan + 0.3, -102.432, 22.165, 5.3)
    _cam(R, t_vin - 0.3, -102.30, 22.03, 2.6)
    _cam(R, t_fer + 0.3, -102.31, 22.0, 2.8)
    _cam(R, t_hue - 0.1, -102.71, 21.89, 3.3)
    _cam(R, t_ter + 1.0, -102.69, 21.885, 3.5)
    _cam(R, t_nis - 0.4, -102.285, 21.82, 4.2)
    _cam(R, t_18 + 1.0, -102.28, 21.82, 4.5)
    _cam(R, t_1985 + 0.4, -101.78, 21.62, 1.0)
    _cam(R, t_3000 + 0.9, -101.85, 21.66, 1.05)
    _cam(R, t_pir - 0.6, -102.29, 21.875, 4.3)
    _cam(R, t_1989 + 1.0, -102.29, 21.875, 4.6)
    _cam(R, t_cua + 0.4, -102.63, 22.04, 1.65)
    _cam(R, fin + 0.4, -102.61, 22.04, 1.58)

    # ---- frase 0: 1927, la Presa Calles
    R.anio(t_1927 - 0.1, 1927)
    pa(R, SX(0), 420, 1000, 0.95, _tc("convencion", e), t_cub - 0.2, sem=900, entra="sube", dy=360, extra=[(0.05, "crece", 0.35)])
    R.sello(t_emp, "maiz", "SIGLO XX", color=(70, 130, 170))
    R.terreno(t_pre - 0.2, "presa_calles", AGUA, 2.6, capa=31)
    R.snd(t_pre, "chorro", 0.35, dur=2.0)
    ciudad(R, t_pre + 0.2, t_cub - 0.2, "presa_calles", "PRESA CALLES", "der", 42)
    titulo(R, t_pri - 0.1, t_cub - 0.3, "UNA DE LAS PRIMERAS GRANDES OBRAS DE RIEGO", px=58)
    R.rio([(-102.405, 22.142), (-102.37, 22.158), (-102.33, 22.165), (-102.29, 22.155), (-102.262, 22.13)], t_rie - 0.3, 1.8,
          M.RIO, ancho=12, t1=t_aba)

    # ---- frase 1: el pueblo bajo el agua
    def hunde(t):
        f = 0.0
        f = lerp(f, 0.45, e_inout(prog(t, t_cub + 0.8, t_fun)))      # se hunde despacio
        f = lerp(f, 0.12, e_out(prog(t, t_aso - 0.3, t_aso + 1.6)))   # en la sequía vuelve a asomar
        return _Hunde(SX(1), f)
    ga(R, hunde, (-102.452, 22.152), t_cub - 0.15, t_lev - 0.4, s=0.62, off=(0, 30), sem=901, zs=0.5, z=2, entra="pop",
       extra=[(0.05, "campana", 0.3), (2.4, "glug", 0.3)])
    titulo(R, t_sj - 0.2, t_aba + 0.2, "EL VIEJO SAN JOSÉ DE GRACIA", px=64)
    R.anio(t_1930 - 0.1, 1930)
    pa(R, FU(1), 300, 1010, 0.95, t_aba - 0.2, t_res + 0.6, sem=902, entra="izq", dx=800, extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    pa(R, FU(2), 470, 1015, 0.9, t_aba, t_res + 0.6, sem=903, entra="izq", dx=900)
    ga(R, FU(5), CI["san_jose_gracia"], t_fun - 0.1, t_lev - 0.3, s=0.32, off=(190, 30), sem=904, zs=0.5, z=2)
    _pin(R, t_fun - 0.1, t_lev - 0.3, CI["san_jose_gracia"], "SAN JOSÉ DE GRACIA (NUEVO)", "abajo", 38, t1_txt=t_seq)
    titulo(R, t_fun - 0.1, INI(e, 2) - 0.1, "FUNDADO DE NUEVO EN OTRO LUGAR", px=60)

    # ---- frase 2: sequía
    R.terreno(t_seq - 0.2, "presa_calles", SECA, 2.2, capa=31)
    R.snd(t_seq, "viento", 0.3, dur=2.0)
    titulo(R, t_seq - 0.1, t_aso - 0.2, "AÑOS DE SEQUÍA", px=74)
    R.snd(t_aso - 0.2, "revelar", 0.35)
    titulo(R, t_aso, INI(e, 3) + 0.4, "ASOMAN RESTOS DEL PUEBLO VIEJO", px=62)

    # ---- frase 3: el Cristo Roto (2006)
    R.anio(t_2006 - 0.05, 2006)
    R.terreno(t_2006 - 0.2, "presa_calles", AGUA, 1.6, capa=31)
    _pin(R, t_isl - 0.1, t_lan + 0.6, CI["cristo_roto"], "CRISTO ROTO", "abajo", 44, t1_txt=t_lle - 0.2)
    titulo(R, t_isl - 0.1, t_lev - 0.3, "UNA ISLA EN LA PRESA", px=66)
    S_CR = 0.56
    ga(R, SX(2), CI["cristo_roto"], t_lev - 0.2, t_lan + 0.6, s=S_CR, off=(0, 8), sem=905, zs=0.5, z=3, entra="sube", dy=260,
       extra=[(0.05, "aparicion", 0.35)])
    pa(R, FP.F("siglo20_3"), 1520, 1000, FP.s_para(0.52), t_cri + 0.1, t_cri + 4.9, entra="pluma", sem=906, z=5,
       extra=[(0.05, "papel", 0.35)])
    _regla(R, t_25 - 0.2, t_lan + 0.4, CI["cristo_roto"], (-150, 8), S_CR, 0.5, "25 m")
    titulo(R, t_bra - 0.3, INI(e, 4) - 0.1, "SIN UN BRAZO Y SIN UNA PIERNA", px=62)

    # ---- frase 4: en lancha
    pa(R, SX(3), lambda t: lerp(1780, 1240, e_inout(prog(t, t_lle - 0.3, t_lan + 0.6))), lambda t: 930, 0.8, t_lle - 0.3, INI(e, 5) + 0.2, sem=907, z=4,
       entra="der", dx=500, extra=[(0.1, "ola", 0.35)])
    R.texto(t_lle - 0.1, INI(e, 5) + 0.1, "HOY SE PUEDE VISITAR", (560, 900), px=60, d=0.6)
    R.texto(t_lle + 0.3, INI(e, 5) + 0.1, "EN LANCHA", (560, 990), px=56, d=0.4)

    # ---- frase 5: viñedos y Feria de la Uva
    R.anio(t_med, 1950)
    R.terreno(t_med - 0.2, None, AGUA, 0.8, capa=31)
    pa(R, SX(5), 340, 1010, 0.8, INI(e, 5) - 0.1, INI(e, 6) - 0.1, sem=908, entra="sube", dy=300, extra=[(0.05, "golpe_suave", 0.35)])
    R.terreno(t_vin - 0.1, "valle", VINAS, 1.8, capa=32)
    for k, (lo, la) in enumerate(((-102.30, 22.06), (-102.36, 22.02), (-102.27, 21.97), (-102.33, 21.94), (-102.25, 22.03),
                                  (-102.38, 21.97))):
        ga(R, SX(4), (lo, la), t_vin + 0.15 * k, INI(e, 6) - 0.1, s=0.26, sem=909 + k, zs=0.5, z=2,
           extra=[(0.0, "pluck", 0.28, {"tono": 1.0 + 0.08 * k})] if k in (0, 3) else ())
    titulo(R, t_vin + 0.3, t_fer - 0.25, "LOS VIÑEDOS LLENAN EL VALLE", px=64)
    ciudad(R, t_ciu - 0.1, INI(e, 6) - 0.1, "aguascalientes", "AGUASCALIENTES", "abajo", 40)
    pa(R, TU(4), 1600, 1010, 1.0, t_fer - 0.25, INI(e, 6) - 0.1, sem=915, extra=[(0.05, "feria", 0.4)])
    pa(R, SX(4), 1330, 1010, 0.55, t_fer, INI(e, 6) - 0.1, sem=916, entra="cae", dy=400)
    titulo(R, t_fer - 0.1, INI(e, 6) - 0.1, "FERIA DE LA UVA", px=78)

    # ---- frase 6: la guayaba de Calvillo
    R.terreno(INI(e, 6) - 0.1, None, VINAS, 1.0, capa=32)
    pa(R, SX(6), 360, 1010, 0.85, INI(e, 6) - 0.1, INI(e, 7) - 0.1, sem=917, entra="sube", dy=300, extra=[(0.05, "plop", 0.35)])
    ciudad(R, t_cal, INI(e, 7) - 0.1, "calvillo", "CALVILLO", "abajo", 44)
    huerto = ((-0.035, 0.05), (0.02, 0.06), (-0.05, 0.0), (0.04, 0.015), (-0.02, -0.035), (0.03, -0.045), (0.0, 0.1), (-0.06, 0.085),
              (0.055, 0.075), (-0.01, -0.08))
    for k, (dlo, dla) in enumerate(huerto):
        ga(R, SX(7), (CI["calvillo"][0] + 1.8 * dlo, CI["calvillo"][1] + 0.9 * dla - 0.02), t_hue - 0.1 + 0.22 * k, INI(e, 7) - 0.1, s=0.26,
           sem=918 + k, zs=0.5, z=2, extra=[(0.0, "crece", 0.25)] if k == 0 else ())
    pa(R, FP.F("siglo20_6"), 1500, 1000, FP.s_para(0.45), t_cal + 0.25, t_cal + 4.9, entra="pluma", sem=928, z=5,
       extra=[(0.05, "papel", 0.3)])
    titulo(R, t_ter - 0.2, INI(e, 7) - 0.1, "CASI 1/3 DE LA GUAYABA DE MÉXICO", px=66)

    # ---- frase 7: Nissan, un motor cada 18 s
    R.anio(t_1982 - 0.1, 1982)
    pa(R, SX(8), 380, 1000, 0.85, INI(e, 7) - 0.1, INI(e, 8) - 0.1, sem=929, entra="sube", dy=300, extra=[(0.05, "golpe_suave", 0.35)])
    _pin(R, t_nis - 0.1, INI(e, 8) - 0.1, NISSAN, "NISSAN", "abajo", 46, sfx=False)
    R.snd(t_nis, "fabrica", 0.4)
    ruta_coches = [NISSAN, (-102.32, 21.797), (-102.38, 21.793), (-102.44, 21.79)]
    for k in range(3):
        R.act(SX(9), pos_geo=R.camino_pos(ruta_coches, t_nis + 0.4 + 1.1 * k, 4.4), off=(0, 0), s=0.24, t_in=t_nis + 0.4 + 1.1 * k, d_in=0.3,
              entra="pop", sem=930 + k, zs=0.5, z=3, t_out=INI(e, 8) - 0.1, flip=True)
    t_cr = t_mot - 0.3

    def crono(t):
        a = round(((max(0.0, t - t_cr) / 1.5) % 1.0) * 48) / 48.0
        return OC.cronometro(a * 2 * math.pi)
    pa(R, crono, 1600, 700, 1.1, t_cr, INI(e, 8) - 0.1, sem=933, z=4, extra=[(0.05, "reloj_rapido", 0.35, {"dur": 1.5})])
    titulo(R, t_mot - 0.1, INI(e, 8) - 0.1, "UN MOTOR CADA 18 SEGUNDOS", px=70)
    R.contador(t_18, t_18 + 1.6, 0, 3227, (1600, 900), px=46, formato="{:,} MOTORES AL DÍA", hasta_t=INI(e, 8) - 0.1)

    # ---- frase 8: el sismo de 1985 y el INEGI
    R.anio(t_1985 - 0.1, 1985)
    R.terreno(t_sis - 0.35, "tierra", (196, 172, 128), 0.35, capa=33)
    R.romper("pueblos", t_sis, t_sis + 0.35, t_sis + 1.9, t_sis + 2.5, colores=[(206, 150, 96), (184, 124, 82), (216, 172, 112)],
             capa=33, gap=46, deriva=60, nervio=6.0)
    R.act(CO(1), pos=lambda t: (1480 + 12 * math.sin(t * 38), 1010, 0.85, 0.07 * math.sin(t * 23)), t_in=t_sis - 0.2, d_in=0.3,
          entra="pop", sem=939, z=4, t_out=t_ine - 0.2, sale="caer")
    R.terreno(t_sis + 2.5, None, (196, 172, 128), 0.6, capa=33)
    R.snd(t_sis, "terremoto", 0.5)
    titulo(R, t_sis - 0.1, t_ine - 0.2, "EL SISMO DE 1985", px=74)
    ga(R, PF(1), CI["ciudad_mexico"], t_sis - 0.1, t_mud + 0.5, s=0.55, off=(-120, -10), sem=934, zs=0.5, z=2)
    _pin(R, t_sis + 0.1, INI(e, 9) - 0.1, CI["ciudad_mexico"], "CIUDAD DE MÉXICO", "arriba", 40, t1_txt=t_mud + 1.0)
    ga(R, SX(10), INEGI, t_ine - 0.2, INI(e, 9) - 0.1, s=0.75, off=(0, 0), sem=935, zs=0.5, z=3, entra="sube", dy=240,
       extra=[(0.05, "crece", 0.3)])
    _pin(R, t_ine, INI(e, 9) - 0.1, INEGI, "INEGI", "abajo", 52)
    R.texto(t_ins - 0.1, t_mud + 0.6, "EL INSTITUTO QUE CUENTA", (1380, 330), px=54, d=0.5)
    R.texto(t_ins + 0.4, t_mud + 0.6, "A TODOS LOS MEXICANOS", (1380, 410), px=54, d=0.5)
    camino = [CI["ciudad_mexico"], (-101.35, 21.15), (-101.85, 21.55), INEGI]
    R.ruta(camino, t_mud - 0.4, 1.6, ancho=6.0, dash=22, hueco=14, flecha=True, t1=INI(e, 9) - 0.2)
    R.snd(t_mud - 0.3, "whoosh", 0.35)
    for k in range(3):
        R.act(TU(1), pos_geo=R.camino_pos(camino, t_mud - 0.2 + 0.35 * k, 2.6), off=((k - 1) * 70, (k % 2) * 30), s=0.62,
              t_in=t_mud - 0.2 + 0.35 * k, d_in=0.3, entra="pop", sem=936 + k, zs=0.5, z=4, t_out=INI(e, 9) - 0.15, flip=True,
              sfx=[(0.0, "pasos", 0.3, {"dur": 1.6})] if k == 0 else ())
    R.contador(t_3000 - 0.2, t_3000 + 0.9, 0, 3000, (1380, 370), px=74, formato="{:,} FAMILIAS", hasta_t=INI(e, 9) - 0.1)

    # ---- frase 9: el edificio pirámide (1989)
    pa(R, SX(10), 1080, 1010, 1.25, t_edi - 0.3, INI(e, 10) - 0.1, sem=940, entra="sube", dy=420, extra=[(0.05, "golpe_suave", 0.4)])
    pa(R, TU(1), 330, 1010, 0.85, INI(e, 9) - 0.1, INI(e, 10) - 0.1, sem=941)
    titulo(R, t_pir - 0.3, INI(e, 10) - 0.1, "INSPIRADO EN LAS PIRÁMIDES", px=72)
    R.anio(t_1989 - 0.05, 1989)
    R.texto(t_1989, INI(e, 10) - 0.1, "SEDE DEL INEGI", (1620, 480), px=50, d=0.5)

    # ---- frase 10: el estado en cifras
    R.anio(t_hoy - 0.1, 2026)
    R.terreno(t_hoy - 0.2, "aguascalientes", COL["aguascalientes"], 1.2, capa=34)
    pa(R, TU(1), 380, 1010, 0.72, f10 - 0.1, fin + 0.3, sem=942, entra="sube", dy=300, extra=[(0.05, "pop", 0.3)])
    titulo(R, t_cua - 0.1, fin + 0.3, "EL 4.º ESTADO MÁS PEQUEÑO", px=74)
    R.snd(t_cua, "revelar", 0.3)
    R.contador(t_5616 - 0.1, t_5616 + 1.6, 0, 5616, (390, 400), px=70, formato="{:,} km²", hasta_t=fin + 0.4)
    R.romper("municipios", t_12 - 0.1, t_12 + 0.5, t_14 + 0.4, t_14 + 1.3, capa=34, gap=12, deriva=20, nervio=0.6)
    R.snd(t_12 - 0.1, "crujido", 0.3)
    R.texto(t_12, fin + 0.4, "11 MUNICIPIOS", (390, 520), px=64, d=0.5)
    for k, g in enumerate(M.CELDAS_SEMILLAS["municipios"]):
        R.ciudad(t_12 + 0.07 * k, fin + 0.3, "m", g, None)
    R.contador(t_14 - 0.2, t_14 + 1.4, 0, 1425607, (390, 630), px=50, formato="{:,} HABITANTES", hasta_t=fin + 0.4)
    R.terreno(fin + 0.45, None, COL["aguascalientes"], 0.5, capa=34)


# ------------------------------------------------------------------ LA RUTA PARA VISITAR
def _ruta(R):
    e = "ruta"
    i0 = INI(e)
    t_vas, t_his, t_cal = T(e, "vas"), T(e, "historia"), T(e, "calle")
    t_pla, t_cat, t_pal, t_tea, t_pas = T(e, "plaza"), T(e, "catedral"), T(e, "palacio"), T(e, "teatro"), T(e, "pasos")
    t_sig, t_enc, t_pos, t_san, t_sma, t_rem, t_ojo = (T(e, "sigue"), T(e, "encino"), T(e, "posada"), T(e, "san antonio"),
                                                       T(e, "san marcos"), T(e, "remojandote"), T(e, "ojocaliente"))
    t_cer, t_hor, t_mus, t_her = T(e, "cerro"), T(e, "horizonte"), T(e, "museo"), T(e, "herran")
    t_dia, t_tun, t_rea, t_cri, t_gua, t_cv = (T(e, "dia"), T(e, "tuneles"), T(e, "real"), T(e, "cristo"), T(e, "guayabas"),
                                               T(e, "calvillo"))
    t_cua, t_mag, t_est, t_car = T(e, "cuatro"), T(e, "magicos"), T(e, "estado"), T(e, "carretera")
    f1, f2, f3, f4, f5, fin = INI(e, 1), INI(e, 2), INI(e, 3), INI(e, 4), INI(e, 5), FIN(e)

    # ---- cámara: del estado a la capital, paseo, y otra vez el estado
    _cam(R, i0 - 0.2, -102.40, 22.02, 1.75)
    _cam(R, f1 - 0.1, -102.29, 21.90, 4.6)
    _cam(R, f2 - 0.2, -102.27, 21.90, 4.75)
    _cam(R, t_ojo + 0.2, -102.176, 21.895, 4.4)
    _cam(R, t_cer + 0.3, -102.20, 21.895, 4.0)
    _cam(R, f4 - 0.1, -102.21, 21.895, 4.2)
    _cam(R, t_rea - 0.2, -102.40, 22.0, 1.85)
    _cam(R, fin + 0.4, -102.42, 22.0, 1.92)

    # ---- frase 0: «si vas a Aguascalientes…»
    pa(R, TU(0), 330, 1010, 1.0, _tc("siglo20", e), f1 + 0.1, sem=1000, entra="sube", dy=340, extra=[(0.05, "whoosh", 0.3)])
    titulo(R, t_vas - 0.2, f1 - 0.1, "SI VAS A AGUASCALIENTES…", px=74)
    R.sello(t_his, "campana", "DE VISITA", color=(196, 120, 62))
    pa(R, TU(6), 960, 1010, 0.85, t_cal - 0.2, f1 + 0.6, sem=1001, extra=[(0.05, "golpe_suave", 0.3)])

    # ---- el turista recorre el mapa turístico de la capital
    tur = _claves([(f1 - 0.1, T_PLAZA), (t_sig, T_PLAZA), (t_enc + 0.4, T_ENCINO), (t_san + 0.2, T_SANANT), (t_sma + 0.2, T_SANMAR),
                   (t_ojo + 0.1, T_OJO), (t_cer + 0.6, T_OJO), (t_mus + 0.2, T_MUSEO), (f4, T_MUSEO)])
    R.act(TU(0), pos_geo=tur, off=lambda t: (-480 * (1 - e_inout(prog(t, t_sig - 0.7, t_sig))), -10 * abs(math.sin(t * 6.0))), s=0.36, t_in=f1 - 0.1, d_in=0.35, entra="pop",
          sem=1002, zs=0.5, z=5, t_out=f4 + 0.1)
    R.ruta([T_PLAZA, T_ENCINO, T_SANANT, T_SANMAR, T_OJO], t_sig - 0.1, t_ojo - t_sig + 0.3, ancho=5.0, dash=20, hueco=14, t1=f4)
    titulo(R, f1 - 0.1, t_cat - 0.3, "1 · PLAZA DE LA PATRIA", px=70)
    _pin(R, t_pla, f4, T_PLAZA, "PLAZA DE LA PATRIA", "abajo", 38, t1_txt=t_sig - 0.3, sfx=True)
    for k, (dib, tt, dx) in enumerate(((CO(0), t_cat, -230), (CO(1), t_pal, 0), (PF(7), t_tea, 230))):
        ga(R, dib, T_PLAZA, tt - 0.15, t_enc + 0.2, s=0.3, off=(dx, -24), sem=1003 + k, zs=0.5, z=3,
           extra=[(0.05, ("campana", "pop", "fanfarria")[k], 0.3)])
    titulo(R, t_cat - 0.1, f2 - 0.1, "HOY: CATEDRAL · PALACIO · TEATRO MORELOS", px=56)
    R.snd(t_pas, "pasos", 0.3, dur=1.0)

    # ---- frase 2: Encino, San Antonio, San Marcos, Ojocaliente
    titulo(R, f2 - 0.1, f4 - 0.2, "HOY SE PUEDE VISITAR", px=64)
    _pin(R, t_enc, f4, T_ENCINO, "EL ENCINO · POSADA", "abajo", 36, t1_txt=t_mus - 0.3, sfx=True)
    ga(R, AR(0), T_ENCINO, t_pos - 0.15, t_sma + 0.5, s=0.32, off=(140, -10), sem=1006, zs=0.5, z=3)
    _pin(R, t_san, f4, T_SANANT, "SAN ANTONIO", "der", 36, t1_txt=t_mus - 0.3)
    ga(R, PF(8), T_SANANT, t_san - 0.1, t_ojo, s=0.32, off=(-140, -20), sem=1007, zs=0.5, z=3, extra=[(0.05, "campana", 0.22)])
    _pin(R, t_sma, f4, T_SANMAR, "SAN MARCOS", "abajo", 36, t1_txt=t_cer - 0.2)
    ga(R, CO(2), T_SANMAR, t_sma - 0.1, t_cer, s=0.32, off=(-120, -16), sem=1008, zs=0.5, z=3)
    _pin(R, t_ojo - 0.2, f4, T_OJO, "OJOCALIENTE", "abajo", 38, sfx=True)
    ga(R, TU(2), T_OJO, t_rem - 0.1, t_hor + 0.3, s=0.36, off=(150, -10), sem=1009, zs=0.5, z=3, extra=[(0.1, "agua_termal", 0.4)])

    # ---- frase 3: el Cerro del Muerto y el Museo de Aguascalientes (Herrán)
    _pin(R, t_cer - 0.1, f4, CI["cerro_muerto"], "CERRO DEL MUERTO", "arriba", 42)
    R.ruta([T_OJO, (T_OJO[0] - 0.04, T_OJO[1] + 0.012), CI["cerro_muerto"]], t_cer - 0.1, 1.4, ancho=4.0, dash=14, hueco=16,
           flecha=True, t1=t_mus - 0.2)
    R.snd(t_cer, "viento", 0.25, dur=1.5)
    _pin(R, t_mus - 0.1, f4, T_MUSEO, "MUSEO DE AGUASCALIENTES", "abajo", 36, sfx=True)
    ga(R, AR(6), T_MUSEO, t_mus, f4 + 0.1, s=0.32, off=(330, -24), sem=1010, zs=0.5, z=3)
    ga(R, AR(5), T_MUSEO, t_her - 0.5, f4 + 0.1, s=0.34, off=(170, -20), sem=1011, zs=0.5, z=3, extra=[(0.05, "pincel", 0.3)])
    R.texto(t_her - 0.2, f4 - 0.2, "SATURNINO HERRÁN", (960, 930), px=56, d=0.5)

    # ---- frase 4: un día más (el autobús por la ruta de los pueblos)
    rt = M.RUTAS["ruta_turista"]
    R.ruta(rt, f4 + 0.1, 6.5, ancho=6.0, dash=24, hueco=14)
    va_izq = R.rumbo(rt, f4 + 0.1, 11.0)
    BUS, BUS_V = TU(7), _Volteo(TU(7))
    R.act(lambda t: BUS_V if va_izq(t) else BUS, pos_geo=R.camino_pos(rt, f4 + 0.1, 11.0), off=(0, 4), s=0.36, t_in=f4 - 0.1, d_in=0.35,
          entra="pop", sem=1012, zs=0.5, z=2, sfx=[(0.05, "bocinazo", 0.3)])
    titulo(R, t_dia - 0.2, t_cua - 0.2, "UN DÍA MÁS", px=74)
    _pin(R, t_rea - 0.1, fin + 0.2, CI["real_asientos"], "REAL DE ASIENTOS", "der", 38, t1_txt=t_cua + 0.1)
    ga(R, CO(6), CI["real_asientos"], t_tun - 0.1, fin + 0.2, s=0.36, off=(0, -8), sem=1013, zs=0.5, z=3, extra=[(0.05, "eco", 0.3)])
    _pin(R, t_cri - 0.1, fin + 0.2, CI["cristo_roto"], "CRISTO ROTO", "izq", 38, t1_txt=t_cua + 0.1)
    ga(R, SX(2), CI["cristo_roto"], t_cri - 0.1, fin + 0.2, s=0.36, off=(-20, -8), sem=1014, zs=0.5, z=3)
    _pin(R, t_cv - 0.2, fin + 0.2, CI["calvillo"], "CALVILLO", "abajo", 40, t1_txt=t_cua + 0.1)
    ga(R, SX(6), CI["calvillo"], t_gua - 0.1, fin + 0.2, s=0.34, off=(0, -8), sem=1015, zs=0.5, z=3, extra=[(0.05, "plop", 0.3)])

    # ---- frase 5: cuatro Pueblos Mágicos
    titulo(R, t_cua - 0.1, fin + 0.3, "4 PUEBLOS MÁGICOS", y=1010, px=80)
    R.snd(t_mag, "brillo", 0.35)
    for k, (cl, txt, lado) in enumerate((("real_asientos", "REAL DE ASIENTOS", "der"), ("calvillo", "CALVILLO", "abajo"),
                                         ("san_jose_gracia", "SAN JOSÉ DE GRACIA", "izq"), ("pabellon_hidalgo", "PABELLÓN DE HIDALGO", "der"))):
        _pin(R, t_cua + 0.25 + 0.3 * k, fin + 0.3, CI[cl], txt, lado, 36)
    pa(R, TU(3), 230, 1010, 0.85, f5 - 0.1, fin + 0.3, sem=1016, entra="izq", dx=700, extra=[(0.05, "fanfarria", 0.3)])
    pa(R, TU(5), 1640, 1010, 0.95, t_est - 0.2, fin + 0.3, sem=1017, entra="der", dx=700, flip=True, extra=[(0.05, "galope", 0.3, {"dur": 1.2})])


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_cha, t_16, t_uno, t_peq, t_his, t_esq = (T(e, "charco"), T(e, "16"), T(e, "uno"), T(e, "pequenos"), T(e, "historia"),
                                               T(e, "esquina"))
    t_tu, t_ley, t_bes, t_cue, t_sus, t_cro = (T(e, "tu"), T(e, "leyenda"), T(e, "beso"), T(e, "cuentamelo"), T(e, "suscribete"),
                                               T(e, "cronopapel"))
    fin = FIN(e)

    _cam(R, i0 - 0.2, -102.272, 21.877, 5.0)
    _cam(R, t_uno - 0.2, -102.28, 21.878, 4.6)
    _cam(R, t_peq + 0.4, -102.36, 22.0, 1.6)
    _cam(R, t_tu, -102.36, 22.0, 1.62)
    _cam(R, fin + 0.4, -102.36, 21.99, 1.25)

    # ---- frase 0: del charco caliente y los 16 soldados…
    R.anio(i0 - 0.05, 1575)
    pa(R, FU(4), 520, 1000, 1.1, _tc("ruta", e), t_uno, sem=1100, entra="sube", dy=320, extra=[(0.05, "burbujas", 0.35)])
    ciudad(R, t_cha, t_uno, "ojocaliente", "OJOCALIENTE", "abajo", 40)
    titulo(R, t_cha - 0.1, t_uno - 0.1, "UN CHARCO CALIENTE Y 16 SOLDADOS", px=64)
    for k in range(4):
        ciclo_pant(R, C_SOLDADO, 1000 - 150 * k, 1700 - 150 * k, 1010 - 12 * (k % 2), t_16 - 0.2 + 0.15 * k, 2.6, t1=t_uno + 0.1,
                   s=0.82, sem=1101 + k, z=3)
    R.snd(t_16 - 0.1, "tambor", 0.35, dur=1.4)
    # …a uno de los estados más pequeños, con historia en cada esquina
    R.anio(t_uno, 2026)
    R.terreno(t_uno - 0.1, "aguascalientes", COL["aguascalientes"], 1.0, capa=36)
    todo = ((CH(0), CI["el_ocote"]), (CO(0), (-102.33, 21.90)), (XI(4), (-102.23, 21.87)), (SX(7), CI["calvillo"]),
            (PL(0), (-102.31, 22.03)), (SX(2), CI["cristo_roto"]), (AR(2), (-102.29, 21.80)), (CO(5), (-102.15, 22.10)),
            (PF(0), (-102.30, 22.14)), (RV(0), (-102.12, 21.74)), (SX(9), (-102.40, 21.70)), (CO(9), CI["el_llano"]),
            (SX(4), (-102.20, 22.10)), (TU(4), (-102.40, 21.95)), (CH(6), (-102.62, 21.92)), (SX(10), (-102.55, 22.02)),
            (TU(5), (-102.08, 22.03)))
    t_a = t_peq - 0.3
    for k, (dib, g) in enumerate(todo):
        ga(R, dib, g, t_a + 0.24 * k, None, s=0.28, sem=1110 + k, zs=0.5, z=2,
           extra=[(0.0, "pop", 0.25, {"tono": 0.9 + 0.05 * (k % 5)})] if k % 4 == 0 else ())
    titulo(R, t_his - 0.1, t_tu - 0.2, "HISTORIA EN CADA ESQUINA", y=1010, px=74)
    R.snd(t_esq, "brillo", 0.35)

    # ---- frase 1: el beso y «suscríbete a Cronopapel»
    titulo(R, t_tu, t_cue - 0.2, "¿YA CONOCÍAS LA LEYENDA DEL BESO?", px=64)
    pa(R, XI(6), 960, 900, 1.1, t_ley - 0.2, t_sus - 0.1, sem=1130, z=6, entra="sube", dy=400, extra=[(t_bes - t_ley + 0.2, "beso", 0.5)])
    titulo(R, t_cue - 0.1, t_sus - 0.2, "CUÉNTAMELO EN LOS COMENTARIOS", px=62)
    pa(R, OC.globo_dialogo(), 1500, 560, 1.0, t_cue - 0.1, t_sus - 0.1, sem=1131, z=6, extra=[(0.05, "pin", 0.3)])
    titulo(R, t_cro - 0.2, 1e9, "CRONOPAPEL", y=380, px=140, d=0.8)
    R.snd(t_cro - 0.2, "escribir", 0.4, dur=0.8)
    pa(R, OC.boton_suscribir(), 960, 690, 1.15, t_sus - 0.1, None, sem=1132, z=6, extra=[(0.05, "ding", 0.4)])
    R.texto(t_sus + 0.1, 1e9, "SUSCRÍBETE", (960, 690), px=66, d=0.6)
