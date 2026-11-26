# -*- coding: utf-8 -*-
"""Coreografía (4/4) de «Toda la historia de los AZTECAS»: la llegada de Cortés (11 barcos en la costa de Veracruz, Malintzin, los
barcos hundidos, la ruta `cortes_ida` con el ciclo de galope, totonacas y tlaxcaltecas, Cholula, el 8-nov-1519 en la calzada de
Iztapalapa con zoom a la isla, Moctezuma prisionero, el penacho de Viena), la caída (Tóxcatl, la muerte de Moctezuma, la Noche
Triste por la calzada de Tlacopan y el ahuehuete, la viruela y Cuitláhuac, los 13 bergantines, el acueducto cortado, Cuauhtémoc
capturado en canoa el 13-ago-1521), el legado (la ciudad encima, los lagos que se secan, el náhuatl de hoy y sus palabras, la
bandera, el rescate del xolo y su trabajo de guía al Mictlán), la RUTA para visitar hoy (Templo Mayor, Antropología, Tlatelolco,
Xochimilco, Teotihuacan) y el cierre con Xolo diciendo adiós.

Semillas 900-1199 (contador `_S`) · capas de terreno: 0 (imperio de 1519, la «principal»: se pone al llegar Cortés y se quita al
caer la ciudad), 41 (Tlaxcala), 44 (cierre: imperio → México). La CDMX de hoy y los lagos que se secan NO son capas: se pintan en un
`R.fondo` propio (si no, el lago seco tapaba el tinte de la ciudad). La noche (Noche Triste, Mictlán) es un velo en `R.trans`."""
import math
from functools import lru_cache

import numpy as np

import boceto as B
import foto_peg as FP
import mapa as M
import obj_a as A
import obj_base as OB
import obj_c as OC
from core import FIN, INI, T
from coreo_peg import andar_ciclo
from coreo_util import CI, COL, ga, lugar, pa, titulo, tramo
from motor import H, W, e_in, e_inout, e_out, lerp, prog
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (número = el de piezas/<hoja>/_indice.jpg)
XO = lambda n, **k: P("01_xolo_hoja", n, **k)        # 0 sentado, 1 camina, 2 asustado, 3 bajo el petate, 4 aúlla, 5 salta, 6 duerme, 7 sospecha
MI = lambda n, **k: P("18_mictlan_hoja", n, **k)     # 0 guía un alma, 1 nada con el alma, 2 perro de Colima, 3 criadora, 4 patos en la
#                                                      chinampa, 5 Xolo nervioso, 6 olla, 7 Xolo con penacho, 8 Xolo dice adiós
CO = lambda n, **k: P("14_cortes_hoja", n, **k)      # 0 Cortés, 1 barco, 2 jinete, 3 Malintzin, 4 señor totonaca, 5 tlaxcalteca, 6 cañón,
#                                                      7 Moctezuma con el collar, 8 Cortés con los brazos arriba
CA = lambda n, **k: P("15_caida_hoja", n, **k)       # 0 Alvarado, 1 danzante, 2/3/4/6 olas, 5 soldado que se hunde con oro,
#                                                      7 ahuehuete con Cortés llorando, 8 enfermo de viruela, 9 Cuitláhuac, 10 bergantín,
#                                                      11 Cuauhtémoc en canoa
LE = lambda n, **k: P("16_legado_hoja", n, **k)      # 0 catedral, 1 edificio que se hunde, 3 tomate, 4 aguacate, 7 cacahuate,
#                                                      11 bandera, 12 mujer nahua
RU = lambda n, **k: P("17_ruta_hoja", n, **k)        # 0 turista, 1 trabajador de 1978, 2 Coyolxauhqui, 3 Coatlicue, 4 Piedra del Sol,
#                                                      5 museo, 6 Tres Culturas, 8 trajinera, 9 Pirámide del Sol
M2 = lambda n, **k: P("13_moctezuma2_hoja", n, **k)  # 0 Moctezuma con su penacho
M1 = lambda n, **k: P("07_moctezuma1_hoja", n, **k)  # 4 acueducto, 6 guerrero con escudo, 7 captor con su cautivo, 8-10 guerrero andando
AL = lambda n, **k: P("06_alianza_hoja", n, **k)     # 6 guerrero águila, 7 guerrero jaguar
AH = lambda n, **k: P("12_ahuizotl_hoja", n, **k)    # 1 Templo Mayor
AX = lambda n, **k: P("11_axayacatl_hoja", n, **k)   # 0 Axayácatl, 5 piedra
TR = lambda n, **k: P("10_tributo_hoja", n, **k)     # 0 canasta de maíz, 5 disco de oro
FU = lambda n, **k: P("04_fundacion_hoja", n, **k)   # 0 águila con el pájaro sobre el nopal, 1 águila con la serpiente
MG = lambda n, **k: P("02_migracion_hoja", n, **k)   # 0 peregrino
C_CAB = ciclo("22_caballo_galope")
C_CANOA = ciclo("21_canoa_ciclo")
C_XOLO = ciclo("19_xolo_corre")
C_MEX = ciclo("20_mexica_camina")
C_GUE = [M1(8), M1(9), M1(10), M1(9)]                # guerrero que camina (23_guerrero_corre no trae ciclo alineado)

ORO_TXT = (150, 110, 40)
LAGO_SECO = (206, 186, 146)
NOCHE = (0.50, 0.56, 0.86)
MICTLAN = (0.52, 0.46, 0.78)

TM = CI["templo_mayor"]
TEN = CI["tenochtitlan"]
MNA = (-99.1864, 19.4261)            # Museo Nacional de Antropología (Wikipedia: 19°25′34″ N, 99°11′11″ O)
XOCHI = CI["xochimilco"]
RUTA_IDA = M.RUTAS["cortes_ida"]     # 0 Villa Rica, 1 Cempoala … 8 Tlaxcala, 9 Cholula … 14 Iztapalapa … 18 Tenochtitlan
CALZ_TLAC = M.RUTAS["calzada_tlacopan"]
NOCHE_T = M.RUTAS["noche_triste"]

# ------------------------------------------------------------------ semillas y cámara del tramo
_S = [900]


def S(n=1):
    """Reserva n semillas del rango del tramo (900-1199)."""
    v = _S[0]
    _S[0] += n
    assert _S[0] <= 1200, "coreo_4: semillas fuera de su rango"
    return v


_CL = []


def _cam(t, lon, lat, z):
    _CL.append((t, lon, lat, z))


def _volcar_cam(R, paso=2.0):
    """Claves del tramo COMPENSANDO la deriva lenta de CamPath (±90 px en x, ±60 en y) y con claves intermedias cada ≤ `paso` s
    (copia de historia_aguascalientes/coreo_4): el lugar encuadrado no se va al borde y la cámara sigue viva."""
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


# ------------------------------------------------------------------ ayudantes
def _pin(R, t0, t1, geo, txt=None, lado="arriba", px=40, t1_txt=None, sfx=False):
    """Punto de tinta en geo (lon, lat) + nombre (que puede borrarse antes que el punto)."""
    R.ciudad(t0, t1, "pin", geo, None, sfx=sfx)
    if txt:
        mw = B.ancho_texto(txt, px)
        dx, dy = {"arriba": (0, -50), "abajo": (0, 52), "der": (28 + mw / 2, 0), "izq": (-28 - mw / 2, 0)}[lado]
        R.texto(t0 + 0.1, t1 if t1_txt is None else t1_txt, txt, None, px=px, d=0.45, geo=geo, off=(dx, dy))


def _foto(R, clave, x, t0, t1, f=0.44, y=985, sem=None):
    """Foto real impresa (FotoPeg) a un lado, cae girando («pluma»)."""
    return pa(R, FP.F(clave), x, y, FP.s_para(f), t0, t1, entra="pluma", sem=S() if sem is None else sem, z=4, d_in=0.55,
              extra=[(0.0, "papel", 0.22)])


_OLA_WH = {2: (325, 40), 3: (103, 33), 4: (73, 29), 6: (95, 32)}


def _ola(R, n, x, y, ancho, t0, t1, z=4, entra="pop", dy=160):
    """Ola de la hoja 15 (pieza n) con un ANCHO en px (las piezas son muy apaisadas: con s fija salían de 2000 px)."""
    w, h = _OLA_WH[n]
    return pa(R, CA(n), x, y, ancho * h / w / 400.0, t0, t1, sem=S(), z=z, entra=entra, dy=dy)


def _tc(prev, e):
    """Justo después del punto medio del cambio de escena: la primera pegatina no espera a INI."""
    return (FIN(prev) + INI(e)) / 2 + 0.05


def _movil(R, dib, P_, t0, dur, t1=None, s=0.3, zs=0.35, z=2, flip=None, off=(0, 0), sale="encoger", d_out=0.4, extra=(), entra="pop"):
    """Pegatina que viaja por el camino geográfico P_ (barcos, bergantines, canoas, aliados)."""
    if flip is None:
        flip = float(P_[-1][0]) < float(P_[0][0])
    if isinstance(dib, list):                      # ciclo de Flow (canoas): cuadro según el tiempo
        dib = (lambda t, fr=dib, k=_S[0]: fr[int(t * 8 + k) % len(fr)])
    return R.act(dib, pos_geo=R.camino_pos(P_, t0, dur), off=off, s=s, t_in=t0, d_in=0.4, entra=entra, sem=S(), sfx=list(extra),
                 t_out=t1, sale=sale, zs=zs, z=z, flip=flip, d_out=d_out)


def _arco(R, dib, a, b, t0, dur, t1, s=0.14, alto=110.0, zs=0.35):
    """Pegatina que salta de a a b (lon, lat) en arco (las piedras del templo a la catedral)."""
    off = lambda t: (0.0, -alto * math.sin(math.pi * min(1.0, max(0.0, (t - t0) / dur))))
    return R.act(dib, pos_geo=R.camino_pos([a, b], t0, dur), off=off, s=s, t_in=t0, d_in=0.2, entra="pop", sem=S(), t_out=t1,
                 sale="encoger", zs=zs, z=3)


class _Velo:
    """Velo de color sobre el cuadro final (noche): multiplica por `col` con viñeta; entra y sale en `d` s. Va en R.trans."""
    _VIG = None

    def __init__(self, t0, t1, col, d=0.8, k=1.0):
        self.t0, self.t1, self.col, self.d, self.k = t0, t1, np.float32(col), d, k

    def activa(self, t):
        return self.t0 <= t <= self.t1 + self.d

    def aplicar(self, out, t, fs):
        a = self.k * e_inout(prog(t, self.t0, self.t0 + self.d)) * (1 - e_inout(prog(t, self.t1, self.t1 + self.d)))
        if a <= 0.002:
            return
        if _Velo._VIG is None:
            yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
            r = np.hypot((xx - W / 2) / (W / 2), (yy - H / 2) / (H / 2)) / math.sqrt(2)
            _Velo._VIG = (1.0 - 0.38 * r ** 1.6).astype(np.float32)
        m = (1 - a * (1 - self.col)).astype(np.float32)
        out *= (1 - a + a * _Velo._VIG)[..., None]
        out *= m


@lru_cache(maxsize=None)
def _papalote():
    """Papalote (no hay pieza de Flow): rombo de colores con varillas, cola con moños y el hilo que baja al origen (los pies)."""
    tp, de, ab, iz, c = (120, -640), (240, -480), (120, -330), (0, -480), (120, -480)
    ops = [OB.trazo((0, 0), (40, -110), (70, -220), (120, -330), w=3.0, peso=0.02)]
    ops += OB.forma(OB.pol(tp, de, c), (226, 86, 112), 5.0, peso=0.4, sp=8)
    ops += OB.forma(OB.pol(de, ab, c), (240, 196, 72), 5.0, peso=0.4, sp=8)
    ops += OB.forma(OB.pol(ab, iz, c), (226, 86, 112), 5.0, peso=0.4, sp=8)
    ops += OB.forma(OB.pol(iz, tp, c), (96, 160, 196), 5.0, peso=0.4, sp=8)
    ops += [OB.trazo(tp, ab, w=4.0, peso=0.03), OB.trazo(iz, de, w=4.0, peso=0.03)]
    ops += [OB.trazo(ab, (150, -290), (200, -270), (230, -220), (260, -190), w=3.0, peso=0.02)]
    for k, (x, y) in enumerate(((150, -290), (200, -268), (240, -210))):
        col = (226, 86, 112) if k % 2 == 0 else (240, 196, 72)
        ops += OB.forma(OB.pol((x - 18, y - 12), (x, y), (x - 18, y + 12)), col, 3.6, peso=0.2, sp=5)
        ops += OB.forma(OB.pol((x + 18, y - 12), (x, y), (x + 18, y + 12)), col, 3.6, peso=0.2, sp=5)
    return B.Dib(ops)


def _imperio_puesto(R, t):
    """¿Alguna capa de imperio sigue pintada en t (por otro tramo)?"""
    for (rej, capa), cl in R.terr.items():
        prev = [c for c in cl if c["t"] <= t]
        if prev and max(prev, key=lambda c: c["t"])["campo"] and str(max(prev, key=lambda c: c["t"])["campo"]).startswith("imperio"):
            return True
    return False


def cortes(R):
    pass


def construir(R):
    _CL.clear()
    _S[0] = 900
    _fondos(R)
    _cortes(R)
    _caida(R)
    _legado(R)
    _ruta(R)
    _cierre(R)
    _volcar_cam(R)


# ------------------------------------------------------------------ fondos propios: calzadas, lagos que se secan, CDMX de hoy
def _fondos(R):
    t_cz0, t_cz1 = T("cortes", "calzada", frase=6) - 1.2, INI("legado", 1)
    t_sec = T("legado", "secaron")
    t_hoy = T("legado", "hoy", frase=1)
    dur_sec = max(2.5, t_hoy - t_sec + 0.6)
    cdmx = [(T("legado", "hoy", frase=1) - 0.1, T("legado", "nunca", frase=2) + 0.3),
            (T("legado", "ciudad de mexico", frase=5) - 0.2, FIN("legado", 5) + 0.2),
            ]

    def calzadas(img, cam, t, fs):
        if t < t_cz0 or t > t_cz1 + 0.8:
            return
        a = prog(t, t_cz0, t_cz0 + 0.8) * (1 - prog(t, t_cz1, t_cz1 + 0.8)) * min(1.0, max(0.0, (cam.z - 3.5) / 3.0))
        if a > 0.02:
            M.pintar_calzadas(img, cam, alfa=a)

    def lagos(img, cam, t, fs):
        """De 1600 a hoy: tierra seca que avanza desde la orilla hacia el centro de cada lago."""
        if t < t_sec:
            return
        u = e_inout(prog(t, t_sec, t_sec + dur_sec))
        if u <= 0.003:
            return
        campo = M.CAMPOS["lagos_cuenca"] if cam.z > 1.8 else M.CAMPOS["lagos_1519"]
        S_ = cam.proyectar(campo)
        d = u * 0.14 * cam.z * M.PXDEG_REF + (60.0 if u > 0.999 else 0.0)
        M.pintar(img, np.maximum(S_, -S_ - d), LAGO_SECO, 1.0, fs, borde=0.35, sombra=0.06, ruido=0.8)

    R.fondo.append(("mx", calzadas))
    R.fondo.append(("mx", lagos))
    if R.ubic:              # la CDMX de hoy con sus fronteras reales (el campo edo_cdmx excluye los lagos de 1519: salía con huecos)
        for a0, a1 in cdmx[:2]:
            R.ubic.estado(a0, a1, cartela=False, tarjeta=True, escala=False)


def _manchas(R, t0, t1, pts, sem):
    """La viruela en el mapa: manchas rojas que brotan pueblo tras pueblo (tinta del mapa: debajo de las pegatinas)."""
    def f(h, cam, t, fs, te):
        if t < t0 or t > t1 + 0.5:
            return
        v = 1 - prog(t, t1, t1 + 0.5)
        for k, (lon, lat) in enumerate(pts):
            tk = t0 + 0.2 * k
            if t < tk:
                continue
            u = e_out(prog(t, tk, tk + 0.7))
            x, y = cam.pant(lon, lat)
            r = (8 + 15 * u + 3 * math.sin(t * 3 + k)) * v
            if r < 2 or not (-40 < x < W + 40 and -40 < y < H + 40):
                continue
            h.relleno(B.circ(x, y, r, n=18), (184, 50, 50), sem + k, fs, 1.0, sp=4)
            h.trazo(B.circ(x, y, r, n=22), 3.2, sem + k, fs, 1.0, amp=0.9, v=int(230 * v))
    R.fondo_tinta.append(R._acot(f, t0))


# ------------------------------------------------------------------ CORTÉS (1519)
def _cortes(R):
    e = "cortes"
    i0 = INI(e)
    t_1519, t_cos, t_once, t_500, t_16, t_man, t_her = (T(e, "1519"), T(e, "costa"), T(e, "once"), T(e, "quinientos"),
                                                       T(e, "dieciseis"), T(e, "mandaba"), T(e, "hernan"))
    t_muj, t_mal, t_mal2, t_nah, t_maya, t_pro, t_voz = (T(e, "mujer"), T(e, "malintzin"), T(e, "malinche"), T(e, "nahuatl", frase=1),
                                                         T(e, "maya"), T(e, "pronto"), T(e, "voz"))
    t_hun, t_reg, t_cam = T(e, "hundir"), T(e, "regresarse"), T(e, "camino", frase=2)
    t_tot, t_cem, t_har, t_uni, t_tlx, t_pel, t_tam = (T(e, "totonacas"), T(e, "cempoala"), T(e, "hartos"), T(e, "unieron"),
                                                      T(e, "tlaxcala", frase=3), T(e, "pelear", frase=3), T(e, "tambien"))
    t_acu, t_flo, t_cue, t_ten = T(e, "acuerdas"), T(e, "florida"), T(e, "cuentas"), T(e, "tenochtitlan", frase=4)
    t_cho, t_mat, t_mil = T(e, "cholula"), T(e, "mataron"), T(e, "miles")
    t_8, t_calz, t_izt, t_moc, t_rec = T(e, "8", frase=6), T(e, "calzada", frase=6), T(e, "iztapalapa"), T(e, "moctezuma", frase=6), T(e, "recibirlo")
    t_reg2, t_col, t_hos, t_pad, t_poc, t_pri = (T(e, "regalo"), T(e, "collares"), T(e, "hospedo"), T(e, "padre"), T(e, "pocos"),
                                                 T(e, "prisionero"))
    t_pen, t_mus, t_vie, t_ni, t_suy = T(e, "penacho"), T(e, "museo"), T(e, "viena"), T(e, "siquiera"), T(e, "suyo")
    f0, f1, f2, f3, f4, f5, f6, f7 = (FIN(e, k) for k in range(8))
    fin = FIN(e)

    # ---- cámara: la costa → tierra adentro → Tlaxcala/Tenochtitlan → Cholula → el valle → la isla → de vuelta al centro de México
    _cam(i0 - 0.2, -96.30, 19.70, 2.3)
    _cam(t_her, -96.30, 19.68, 2.5)
    _cam(t_voz, -96.30, 19.66, 2.7)
    _cam(t_cam - 0.2, -96.36, 19.66, 2.7)
    _cam(t_cem + 0.2, -96.85, 19.52, 2.1)
    _cam(t_tlx + 0.2, -97.55, 19.58, 1.55)
    _cam(t_flo + 0.3, -98.55, 19.55, 1.6)
    _cam(t_cue + 0.4, -98.62, 19.52, 1.65)
    _cam(t_cho + 0.3, -98.33, 19.12, 3.1)
    _cam(f5, -98.42, 19.12, 3.0)
    _cam(t_calz - 0.4, -98.95, 19.30, 5.4)
    _cam(t_moc + 0.3, -99.12, 19.40, 13.0)
    _cam(t_reg2 + 0.3, -99.132, 19.430, 24.0)
    _cam(t_pri + 0.4, -99.134, 19.433, 27.0)
    _cam(t_pen + 0.5, -99.10, 19.43, 9.0)
    _cam(t_vie + 0.6, -98.10, 19.55, 1.45)
    _cam(fin - 0.25, -97.95, 19.50, 1.4)

    if not _imperio_puesto(R, i0):           # coreo_3 deja el imperio de 1519 en su capa 30: no pintarlo dos veces
        R.terreno(i0 - 0.3, "imperio_1519", COL["imperio_1519"], 0.8, capa=0)
    R.sello(i0 + 0.3, "espadas", "LA CONQUISTA", color=(70, 96, 150))
    R.anio(i0, 1519)

    # ---- frase 0: 11 barcos, 500 españoles, 16 caballos; Hernán Cortés
    pa(R, XO(2), 640, 1015, 0.55, _tc("moctezuma2", e), t_man - 0.1, sem=S(), flip=True, extra=[(0.4, "gemido_perro", 0.25)])
    R.snd(i0 + 0.1, "ola", 0.4)
    barcos = []
    for k in range(11):
        fila, col = k % 3, k // 3
        lon1, lat1 = -96.28 + 0.15 * col + 0.07 * fila, 19.66 - 0.115 * fila - 0.03 * col
        b = _movil(R, CO(1), [(lon1 + 0.55, lat1 + 0.30), (lon1, lat1)], _tc("moctezuma2", e) + 0.12 * k, 5.6, t1=t_hun + 0.1 + 0.09 * k, s=0.22,
                   zs=0.4, z=2, flip=True, sale="baja", d_out=1.3)
        barcos.append(b)
    lugar(R, i0 + 0.3, t_once - 0.3, "GOLFO DE MÉXICO", (-95.80, 19.30), off=(0, 0), px=40)
    _pin(R, t_cos - 0.1, t_cem, CI["villa_rica"], "COSTA DE VERACRUZ", "izq", 38, t1_txt=t_once + 2.5)
    R.contador(t_once - 0.15, t_once + 0.5, 0, 11, (960, 176), px=64, formato="{:,} BARCOS", hasta_t=t_man - 0.1)
    R.contador(t_500 - 0.15, t_500 + 0.7, 0, 500, (960, 258), px=58, formato="{:,} ESPAÑOLES", hasta_t=t_man - 0.1)
    R.contador(t_16 - 0.15, t_16 + 0.6, 0, 16, (960, 336), px=58, formato="{:,} CABALLOS", hasta_t=t_man - 0.1)
    for k in range(5):
        ga(R, CO(0), CI["villa_rica"], t_500 - 0.1 + 0.1 * k, t_hun, s=0.22, off=(-90 - 78 * k, 70 + 24 * (k % 2)), sem=S(), zs=0.4,
           z=2, extra=[(0.0, "pasos", 0.25, {"dur": 0.8})] if k == 0 else ())
    for k in range(3):
        ga(R, CO(2), CI["villa_rica"], t_16 - 0.1 + 0.12 * k, t_hun, s=0.26, off=(-140 - 130 * k, 230), sem=S(), zs=0.4, z=2,
           flip=True, extra=[(0.0, "galope", 0.25, {"dur": 0.8})] if k == 0 else ())
    pa(R, CO(0), 330, 1010, 1.05, t_man - 0.2, f0 + 0.1, sem=S(), extra=[(0.05, "pluck", 0.3)])
    titulo(R, t_her - 0.05, f0 - 0.1, "HERNÁN CORTÉS", px=82, snd=True)
    _foto(R, "cortes_retrato", 1500, t_man - 0.1, f0 + 0.25, f=0.50)

    # ---- frase 1: Malintzin, la voz de Cortés
    pa(R, CO(3), 1590, 1010, 1.05, t_muj - 0.15, f1 + 0.1, sem=S(), extra=[(0.05, "brillo", 0.3)])
    R.texto(t_mal - 0.05, f1 - 0.1, "MALINTZIN", (1590, 560), px=50, d=0.4)
    R.texto(t_mal2 - 0.05, f1 - 0.1, "«LA MALINCHE»", (1590, 500), px=38, d=0.4)
    for k, (tt, txt) in enumerate(((t_nah, "NÁHUATL"), (t_maya, "MAYA"), (t_pro + 0.25, "ESPAÑOL"))):
        R.texto(tt - 0.05, t_voz - 0.25, txt, (620 + 340 * k, 196), px=60, d=0.35)
        R.snd(tt, "pluck", 0.28, tono=1.0 + 0.12 * k)
    pa(R, XO(0), 1000, 1015, 0.5, t_muj + 0.2, f1 + 0.1, sem=S())
    _foto(R, "duran_cortes_malinche", 500, t_mal - 0.1, t_voz - 0.3, f=0.36)
    pa(R, CO(8), 330, 1010, 1.0, t_voz - 0.2, f1 + 0.1, sem=S())
    titulo(R, t_voz - 0.1, f1 - 0.1, "LA VOZ DE CORTÉS", px=80)

    # ---- frase 2: hunde sus barcos y camina tierra adentro
    pa(R, CO(8), 330, 1010, 1.0, f1 + 0.2, t_cam + 0.6, sem=S())
    big = pa(R, CO(1), 1480, 1000, 1.0, t_hun - 0.35, t_reg - 0.1, sem=S(), z=3, sale="baja", d_out=1.7,
             extra=[(0.3, "barco_hunde", 0.45)])
    for k, (n, dx, an) in enumerate(((2, -60, 520), (3, -250, 200), (4, 250, 170), (6, 60, 220))):
        _ola(R, n, 1480 + dx, 1030 + 22 * (k % 2), an, t_hun - 0.3 + 0.06 * k, t_cam + 0.3)
    titulo(R, t_reg - 0.1, t_cam + 1.2, "¡SIN REGRESO!", px=96, snd=True)
    pa(R, XO(7), 640, 1015, 0.5, t_hun, t_tot - 0.1, sem=S(), flip=True)
    P0 = RUTA_IDA[0:2]
    R.ruta(P0, t_cam - 0.1, 2.2, ancho=5.0, t1=fin + 0.4, flecha=True)
    andar_ciclo(R, C_CAB, P0, t_cam - 0.1, 2.4, t1=t_tot + 0.4, s=0.42, sem=S(), fps=10, zs=0.4, z=3,
                extra=[(0.0, "galope", 0.35, {"dur": 2.0})])
    R.texto(t_cam + 0.1, t_tot - 0.2, "…Y TIERRA ADENTRO", (960, 300), px=58, d=0.5)

    # ---- frase 3: totonacas de Cempoala y tlaxcaltecas
    pa(R, CO(4), 330, 1010, 1.0, t_tot - 0.2, t_tlx - 0.05, sem=S(), extra=[(0.05, "tambor", 0.25, {"dur": 0.7})])
    R.texto(t_tot, t_tlx - 0.2, "TOTONACAS", (330, 560), px=44, d=0.3)
    _pin(R, t_cem - 0.1, f4, CI["cempoala"], "CEMPOALA", "abajo", 38, t1_txt=t_tlx + 0.6)
    pa(R, TR(0), 600, 1005, 0.5, t_har - 0.15, min(t_uni + 0.3, t_tlx - 0.1), sem=S(), sale="caer", d_out=0.6)
    titulo(R, t_har - 0.1, t_tlx - 0.2, "¡HARTOS DEL TRIBUTO!", px=74)
    for k in range(3):
        R.act(CO(4), pos_geo=R.camino_pos(RUTA_IDA[1:9], t_uni + 0.1 + 0.25 * k, f3 - t_uni + 0.3), off=(-60 - 50 * k, 20 + 12 * (k % 2)),
              s=0.24, t_in=t_uni + 0.1 + 0.25 * k, d_in=0.3, entra="pop", sem=S(), zs=0.4, z=2, t_out=f4 - 0.2, flip=True)
    P1 = RUTA_IDA[1:9]
    R.ruta(P1, t_uni - 0.2, f3 - t_uni + 0.2, ancho=5.0, t1=fin + 0.4, flecha=True)
    andar_ciclo(R, C_CAB, P1, t_uni - 0.2, f3 - t_uni + 0.3, t1=t_flo, s=0.42, sem=S(), fps=10, zs=0.4, z=3,
                extra=[(0.0, "galope", 0.3, {"dur": 2.4})])
    R.terreno(t_tlx - 0.2, "tlaxcala", COL["tlaxcala"], 0.8, capa=41)
    _pin(R, t_tlx - 0.1, f5, CI["tlaxcala"], "TLAXCALA", "abajo", 42, t1_txt=t_cue + 0.8)
    pa(R, CO(5), 1600, 1010, 1.05, t_tlx - 0.1, f4 - 0.1, sem=S(), flip=True)
    _foto(R, "lienzo_cortes_malinche", 520, t_tlx, f3 + 0.3, f=0.40)
    ga(R, A.estallido(), CI["tlaxcala"], t_pel, t_tam + 0.2, s=0.5, off=(70, -40), sem=S(), zs=0.3, z=3,
       extra=[(0.0, "batalla", 0.4, {"dur": 1.4})])
    titulo(R, t_tam - 0.1, f3 - 0.1, "TAMBIÉN ALIADOS", px=78)

    # ---- frase 4: la guerra florida y las cuentas pendientes
    pa(R, M1(7), 360, 1010, 1.0, t_acu - 0.15, f4 + 0.1, sem=S(), extra=[(0.05, "flauta", 0.3)])
    pa(R, XO(7), 1040, 1015, 0.5, t_acu - 0.05, f4 + 0.1, sem=S())
    titulo(R, t_acu - 0.1, f4 - 0.1, "¿TE ACUERDAS?", px=74)
    R.texto(t_flo - 0.05, t_cue - 0.1, "LA GUERRA FLORIDA", (960, 290), px=60, d=0.5)
    R.ruta([CI["tlaxcala"], (-98.70, 19.52), TEN], t_cue - 0.15, 1.3, ancho=5.5, t1=f4 + 0.1, flecha=True)
    _pin(R, t_ten - 0.15, f4 + 0.1, TEN, "TENOCHTITLAN", "abajo", 40)
    R.texto(t_cue, f4 - 0.1, "CUENTAS PENDIENTES", (960, 290), px=60, d=0.5)
    R.snd(t_cue + 0.1, "tambor", 0.35, dur=1.2)

    # ---- frase 5: Cholula
    P2 = RUTA_IDA[8:10]
    R.ruta(P2, t_cho - 0.6, 1.4, ancho=5.0, t1=fin + 0.4, flecha=True)
    andar_ciclo(R, C_CAB, P2, t_cho - 0.6, 1.5, t1=f5 + 0.3, s=0.40, sem=S(), fps=10, zs=0.35, z=3)
    for k in range(3):
        R.act(CO(5), pos_geo=R.camino_pos(P2, t_cho - 0.4 + 0.2 * k, 1.6), off=(-70 - 55 * k, 16 * (k % 2)), s=0.24,
              t_in=t_cho - 0.4 + 0.2 * k, d_in=0.3, entra="pop", sem=S(), zs=0.35, z=2, t_out=f5 + 0.2)
    _pin(R, t_cho - 0.1, f5 + 0.2, CI["cholula"], "CHOLULA", "abajo", 42)
    ga(R, CO(6), CI["cholula"], t_mat - 0.2, f5 + 0.1, s=0.34, off=(230, 70), sem=S(), zs=0.35, z=3, flip=True,
       extra=[(0.15, "canonazo", 0.4)])
    titulo(R, t_cho, f5 - 0.1, "MATANZA DE CHOLULA", px=80, snd=True)
    R.texto(t_mil - 0.1, f5 - 0.1, "MILES DE MUERTOS EN UNAS HORAS", (960, 290), px=52, d=0.6)
    R.snd(t_mat, "batalla", 0.35, dur=2.0)
    pa(R, XO(3), 1600, 1015, 0.62, t_cho - 0.1, f5 + 0.1, sem=S(), extra=[(0.5, "gemido_perro", 0.3)])
    pa(R, CO(0), 330, 1010, 1.0, t_mat - 0.3, f5 + 0.1, sem=S())

    # ---- frase 6: 8 de noviembre de 1519, calzada de Iztapalapa (zoom a la isla)
    P3 = RUTA_IDA[9:]
    R.ruta(P3, t_8 - 0.3, t_moc - t_8 + 0.2, ancho=5.0, t1=t_pen, flecha=True)
    andar_ciclo(R, C_CAB, P3, t_8 - 0.3, t_moc - t_8 + 0.4, t1=t_hos, s=0.34, sem=S(), fps=10, zs=0.28, z=3,
                extra=[(0.0, "galope", 0.3, {"dur": 2.4})])
    for k in range(2):
        R.act(CO(5), pos_geo=R.camino_pos(P3, t_8 - 0.1 + 0.25 * k, t_moc - t_8 + 0.5), off=(-80 - 60 * k, 14), s=0.22,
              t_in=t_8 - 0.1 + 0.25 * k, d_in=0.3, entra="pop", sem=S(), zs=0.28, z=2, t_out=t_hos)
    titulo(R, t_8 - 0.1, t_moc - 0.2, "8 DE NOVIEMBRE DE 1519", px=78, snd=True)
    lugar(R, t_calz + 0.1, t_reg2, "CALZADA DE IZTAPALAPA", (-99.128, 19.392), off=(150, 0), px=40)
    R.snd(t_calz, "multitud", 0.25, dur=3.0)
    pa(R, CO(8), 330, 1010, 1.0, t_izt - 0.2, f6 + 0.1, sem=S())
    pa(R, M2(0), 1600, 1010, 1.05, t_moc - 0.2, f6 + 0.1, sem=S(), extra=[(0.05, "caracol", 0.35)])
    R.texto(t_moc, f6 - 0.1, "MOCTEZUMA", (1600, 550), px=48, d=0.4)
    R.texto(t_rec - 0.1, f6 - 0.1, "SALE A RECIBIRLO", (960, 196), px=64, d=0.5)
    pa(R, XO(5), 960, 1015, 0.5, t_rec - 0.2, f6 + 0.1, sem=S(), extra=[(0.1, "ladrido", 0.3)])

    # ---- frase 7: collares, el palacio de su padre… y prisionero
    ga(R, CO(7), TEN, t_reg2 - 0.15, f7 + 0.1, s=0.34, off=(-40, 40), sem=S(), zs=0.3, z=3, extra=[(0.05, "brillo", 0.3)])
    titulo(R, t_col - 0.1, t_pri - 0.2, "COLLARES DE REGALO", px=72)
    _foto(R, "malinche_tlaxcala", 470, t_hos - 0.1, f7 + 0.1, f=0.42)
    ga(R, AX(0), TEN, t_pad - 0.3, t_pri - 0.1, s=0.24, off=(150, 20), sem=S(), zs=0.3, z=3)
    R.texto(t_pad - 0.1, t_pri - 0.2, "EL PALACIO DE SU PADRE, AXAYÁCATL", (960, 300), px=46, d=0.6)
    ga(R, A.puerta(0.0, True), TEN, t_pri - 0.2, f7 + 0.1, s=0.36, off=(150, 30), sem=S(), zs=0.3, z=3,
       extra=[(0.1, "sello", 0.35)])
    pa(R, CO(0), 1600, 1010, 1.05, t_poc - 0.2, f7 + 0.1, sem=S(), flip=True)
    titulo(R, t_pri - 0.1, f7 - 0.1, "¡PRISIONERO EN SU PROPIA CIUDAD!", px=66, snd=True)

    # ---- frase 8: el penacho de Viena (¿de verdad era suyo?)
    pa(R, M2(0), 400, 1010, 1.15, t_pen - 0.2, fin + 0.3, sem=S(), extra=[(0.05, "brillo", 0.35)])
    R.texto(t_pen, fin, "EL PENACHO", (400, 520), px=52, d=0.4)
    R.ruta([TEN, (-98.6, 19.75), (-97.4, 20.1), (-96.3, 20.25)], t_mus - 0.3, 2.0, ancho=5.5, t1=fin + 0.3, flecha=True)
    titulo(R, t_mus - 0.1, fin, "HOY: WELTMUSEUM DE VIENA", px=70, snd=True)
    R.texto(t_vie, fin, "VIENA, AUSTRIA", (1450, 470), px=50, d=0.4)
    _foto(R, "penacho", 1450, t_pen + 0.1, t_suy - 0.5, f=0.40)
    pa(R, A.signo_pregunta(), 760, 760, 1.1, t_ni - 0.1, fin + 0.3, sem=S(), z=5, extra=[(0.05, "pluck", 0.3)])
    R.texto(t_ni, fin, "¿DE VERDAD ERA SUYO?", (960, 300), px=56, d=0.5)
    pa(R, MI(7), 1560, 1015, 0.75, t_suy - 0.4, fin + 0.3, sem=S(), flip=True, extra=[(0.2, "ladrido", 0.3)])


# ------------------------------------------------------------------ LA CAÍDA (1520-1521)
def _caida(R):
    e = "caida"
    i0 = INI(e)
    t_1520, t_sal, t_otr, t_ped = T(e, "1520"), T(e, "salio", frase=0), T(e, "otros"), T(e, "pedro")
    t_fie, t_tox, t_tm, t_alv, t_ata, t_nob, t_des = (T(e, "fiesta"), T(e, "toxcatl"), T(e, "templo mayor"), T(e, "alvarado", frase=1),
                                                     T(e, "ataco"), T(e, "nobles"), T(e, "desarmados"))
    t_lev, t_moc, t_calm, t_mur, t_esp, t_pie, t_mexs, t_matl = (T(e, "levanto"), T(e, "moctezuma", frase=2), T(e, "calmar"),
                                                                 T(e, "murio"), T(e, "espanoles", frase=2), T(e, "piedras"),
                                                                 T(e, "mexicas", frase=2), T(e, "mataron", frase=2))
    t_30, t_huy, t_tlac, t_oro, t_aho, t_pes = T(e, "30"), T(e, "huyeron"), T(e, "tlacopan"), T(e, "oro"), T(e, "ahogaron"), T(e, "peso")
    t_noc, t_ley, t_llo, t_ahu = T(e, "noche triste"), T(e, "leyenda"), T(e, "lloro"), T(e, "ahuehuete")
    t_peo, t_vir = T(e, "peor"), T(e, "viruela", frase=5)
    t_nad, t_epi, t_mil, t_nue, t_cui, t_rei = (T(e, "nadie"), T(e, "epidemia"), T(e, "miles", frase=6), T(e, "nuevo"),
                                               T(e, "cuitlahuac"), T(e, "reinar"))
    t_vol, t_1521, t_dec, t_ali, t_tre, t_ber, t_pzs, t_lag = (T(e, "volvio"), T(e, "1521", frase=7), T(e, "decenas"),
                                                               T(e, "aliados", frase=7), T(e, "trece"), T(e, "bergantines"),
                                                               T(e, "piezas"), T(e, "lago", frase=7))
    t_cor, t_cha, t_agu, t_com, t_pst, t_res = (T(e, "cortaron"), T(e, "chapultepec"), T(e, "agua dulce"), T(e, "comida"),
                                                T(e, "peste"), T(e, "resistio"))
    t_ult, t_cua, t_agi, t_25 = T(e, "ultimo"), T(e, "cuauhtemoc", frase=9), T(e, "aguila", frase=9), T(e, "veinticinco")
    t_13, t_cap, t_can, t_ten, t_cay = (T(e, "13"), T(e, "capturado"), T(e, "canoa"), T(e, "tenochtitlan", frase=10), T(e, "cayo"))
    t_casi, t_200, t_nop = T(e, "casi", frase=11), T(e, "doscientos"), T(e, "nopal")
    f = [FIN(e, k) for k in range(12)]
    fin = FIN(e)

    # ---- cámara
    _cam(i0 - 0.2, -97.85, 19.45, 1.45)
    _cam(t_ped, -97.95, 19.45, 1.5)
    _cam(t_tox - 0.1, -99.125, 19.43, 14.0)
    _cam(t_tm + 0.3, -99.121, 19.441, 30.0)
    _cam(t_lev + 0.2, -99.125, 19.441, 26.0)
    _cam(f[2] - 0.3, -99.140, 19.440, 22.0)
    _cam(t_huy + 0.2, -99.158, 19.446, 24.0)
    _cam(t_aho + 0.5, -99.165, 19.449, 26.0)
    _cam(t_ley, -99.175, 19.452, 24.0)
    _cam(t_ahu + 0.8, -98.95, 19.50, 4.4)
    _cam(t_peo + 0.4, -98.72, 19.62, 3.3)
    _cam(t_vir + 0.2, -99.02, 19.45, 5.4)
    _cam(t_cui, -99.05, 19.44, 6.0)
    _cam(t_vol + 0.2, -98.92, 19.47, 5.0)
    _cam(t_ber + 0.5, -98.98, 19.46, 5.6)
    _cam(t_cor - 0.2, -99.150, 19.432, 15.0)
    _cam(t_res, -99.145, 19.435, 17.0)
    _cam(t_cua, -99.135, 19.440, 20.0)
    _cam(t_13 + 0.2, -99.108, 19.468, 22.0)
    _cam(t_cay + 0.3, -99.112, 19.462, 20.0)
    _cam(t_casi + 0.4, -99.10, 19.43, 9.0)
    _cam(fin - 0.25, -99.08, 19.43, 7.5)

    R.sello(i0 + 0.3, "aguila", "LA CAÍDA", color=(150, 48, 48))

    # ---- frase 0: Cortés sale a pelear contra otros españoles; Alvarado al mando
    R.anio(t_1520, 1520)
    pa(R, CO(0), 330, 1010, 1.0, _tc("cortes", e), t_ped + 0.6, sem=S())
    vuelta = list(reversed(RUTA_IDA))[0:18]
    andar_ciclo(R, C_CAB, vuelta, t_sal - 0.1, t_ped - t_sal + 0.6, t1=t_ped + 1.0, s=0.4, sem=S(), fps=10, zs=0.4, z=3,
                extra=[(0.0, "galope", 0.35, {"dur": 2.4})])
    andar_ciclo(R, C_XOLO, vuelta, t_sal + 0.2, t_ped - t_sal + 0.6, t1=t_ped + 1.0, s=0.22, sem=S(), fps=12, zs=0.4, z=3,
                off=(-60, 6))
    _pin(R, i0 + 0.1, t_ped + 0.6, TEN, "TENOCHTITLAN", "abajo", 38)
    titulo(R, t_otr - 0.1, f[0] - 0.1, "CONTRA OTROS ESPAÑOLES", px=70, snd=True)
    pa(R, CA(0), 1600, 1010, 1.05, t_ped - 0.2, f[0] + 0.1, sem=S(), extra=[(0.05, "golpe_suave", 0.3)])
    R.texto(t_ped, f[0] - 0.1, "PEDRO DE ALVARADO", (1600, 550), px=42, d=0.4)
    R.texto(t_ped + 0.6, f[0] - 0.1, "AL MANDO", (960, 300), px=56, d=0.4)

    # ---- frase 1: la fiesta de Tóxcatl junto al Templo Mayor
    ga(R, AH(1), TM, t_fie - 0.3, t_lev + 0.2, s=0.3, off=(20, -10), sem=S(), zs=0.28, z=1)
    bail = []
    for k, (dx, dy) in enumerate(((-170, 60), (-60, 90), (60, 80), (170, 55))):
        bail.append(ga(R, CA(1), TM, t_fie - 0.1 + 0.15 * k, t_ata + 0.15 + 0.12 * k, s=0.22, off=(lambda t, dx=dx, dy=dy, k=k: (dx, dy + 8 * math.sin(t * 7 + k))),
                       sem=S(), zs=0.28, z=2, sale="caer", d_out=0.7, flip=k % 2 == 1))
    R.snd(t_fie, "tambor", 0.3, dur=2.0)
    R.snd(t_fie + 0.3, "flauta", 0.25)
    titulo(R, t_tox - 0.1, f[1] - 0.1, "FIESTA DE TÓXCATL", px=84, snd=True)
    _foto(R, "matanza_templo_mayor", 1440, t_tm - 0.15, t_lev - 0.1, f=0.40)
    pa(R, CA(0), 330, 1010, 1.05, t_alv - 0.2, f[1] + 0.1, entra="izq", sem=S(), extra=[(0.05, "impacto", 0.4)])
    R.snd(t_ata + 0.1, "batalla", 0.4, dur=2.2)
    R.texto(t_nob - 0.05, f[1] - 0.1, "NOBLES DESARMADOS", (960, 300), px=60, d=0.5)
    pa(R, XO(3), 760, 1015, 0.5, t_ata - 0.1, f[1] + 0.1, sem=S())

    # ---- frase 2: la ciudad se levanta; muere Moctezuma (dos versiones)
    for k, (dib, dx, dy) in enumerate(((AL(6), -190, 70), (AL(7), 180, 60), (M1(6), -70, 110), (M1(9), 80, 120), (AL(6), 250, 110))):
        ga(R, dib, TM, t_lev - 0.1 + 0.12 * k, t_mur, s=0.22, off=(dx, dy), sem=S(), zs=0.28, z=2, flip=dx > 0,
           extra=[(0.0, "batalla", 0.35, {"dur": 1.8})] if k == 0 else ())
    titulo(R, t_lev - 0.1, t_mur - 0.2, "LA CIUDAD SE LEVANTÓ", px=78, snd=True)
    pa(R, M2(0), 960, 1010, 0.95, t_moc - 0.2, t_mur + 0.4, sem=S(), sale="borrar", d_out=0.9)
    R.texto(t_calm - 0.05, t_mur - 0.1, "«¡CALMA!»", (960, 560), px=52, d=0.4)
    titulo(R, t_mur - 0.1, f[2] - 0.1, "¿CÓMO MURIÓ MOCTEZUMA?", px=72)
    R.texto(t_esp - 0.05, f[2] - 0.1, "LOS ESPAÑOLES:", (430, 330), px=40, d=0.4)
    R.texto(t_pie - 0.1, f[2] - 0.1, "PIEDRAS DE LOS SUYOS", (430, 390), px=44, d=0.5)
    for k in range(3):
        pa(R, AX(5), 290 + 130 * k, 1000 - 20 * (k % 2), 0.35, t_pie + 0.1 * k, f[2] + 0.1, entra="cae", sem=S(),
           extra=[(0.25, "piedra", 0.3)] if k == 0 else ())
    R.texto(t_mexs - 0.05, f[2] - 0.1, "LOS MEXICAS:", (1500, 330), px=40, d=0.4)
    R.texto(t_matl - 0.1, f[2] - 0.1, "LO MATARON LOS ESPAÑOLES", (1500, 390), px=44, d=0.5)
    _foto(R, "muerte_moctezuma", 1560, t_mexs - 0.2, f[2] + 0.2, f=0.48)
    pa(R, XO(7), 1060, 1015, 0.48, t_mur + 0.5, f[2] + 0.1, sem=S())

    # ---- frase 3: la noche del 30 de junio, por la calzada de Tlacopan, cargados de oro
    R.trans.append(_Velo(t_30 - 0.4, t_ahu + 1.2, NOCHE, d=0.9))
    titulo(R, t_30 - 0.1, t_noc - 0.2, "30 DE JUNIO DE 1520, DE NOCHE", px=66, snd=True)
    R.ruta(CALZ_TLAC, t_huy - 0.1, 2.6, ancho=6.0, t1=f[4], flecha=True)
    R.texto(t_tlac - 0.1, t_aho - 0.25, "POR LA CALZADA DE TLACOPAN", (960, 300), px=52, d=0.5)
    andar_ciclo(R, C_CAB, CALZ_TLAC, t_huy - 0.1, 3.4, t1=f[3] + 0.1, s=0.22, sem=S(), fps=11, zs=0.28, z=3,
                extra=[(0.0, "galope", 0.35, {"dur": 2.6})])
    for k in range(2):
        _movil(R, C_CANOA, [(-99.138 + 0.010 * k, 19.426 - 0.004 * k), (-99.156 + 0.010 * k, 19.430 - 0.004 * k)],
               t_huy + 0.4 + 0.4 * k, 3.5, t1=f[3] + 0.1, s=0.18, zs=0.28, z=2, extra=[(0.1, "remo", 0.3)] if k == 0 else ())
    pa(R, TR(5), 330, 1005, 0.55, t_oro + 0.15, f[3] + 0.1, sem=S(), extra=[(0.05, "monedas", 0.35)])
    R.texto(t_oro - 0.05, f[3] - 0.1, "CARGADOS DE ORO", (330, 700), px=46, d=0.4)
    for k, g in enumerate(((-99.145, 19.4365), (-99.158, 19.441), (-99.168, 19.447))):
        ga(R, CA(5), g, t_aho - 0.2 + 0.25 * k, t_pes + 0.6 + 0.2 * k, s=0.26, off=(0, 50), sem=S(), zs=0.28, z=3, sale="baja",
           d_out=1.6, extra=[(0.1, "inundacion", 0.3, {"dur": 1.6})] if k == 0 else ())
    R.texto(t_aho, f[3] - 0.1, "MUCHOS SE AHOGARON", (960, 300), px=56, d=0.5)
    pa(R, XO(2), 760, 1015, 0.5, t_30 - 0.1, t_llo - 0.2, sem=S(), flip=True, extra=[(0.4, "gemido_perro", 0.22)])
    _foto(R, "noche_triste", 1440, t_huy + 0.3, f[3] + 0.2, f=0.38)
    pa(R, CO(0), 330, 1010, 0.95, t_30 - 0.05, t_oro - 0.25, sem=S(), flip=True)

    # ---- frase 4: la Noche Triste y el ahuehuete
    titulo(R, t_noc - 0.1, f[4] - 0.1, "LA NOCHE TRISTE", px=96, snd=True)
    pa(R, CA(7), 1480, 1010, 1.3, t_ley - 0.2, f[4] + 0.2, sem=S(), entra="sube", dy=300, extra=[(0.1, "crece", 0.3)])
    R.texto(t_ley, f[4] - 0.1, "CUENTA LA LEYENDA…", (960, 300), px=50, d=0.5)
    R.texto(t_ahu - 0.05, f[4] - 0.1, "UN AHUEHUETE", (1480, 430), px=48, d=0.4)
    pa(R, XO(4), 380, 1015, 0.6, t_llo - 0.3, f[4] + 0.2, sem=S(), extra=[(0.2, "aullido", 0.25)])
    resto = NOCHE_T[3:]
    R.ruta(resto, t_ahu - 0.2, f[5] - t_ahu + 0.2, ancho=5.0, t1=f[5] + 0.3, flecha=True)
    andar_ciclo(R, C_CAB, resto, t_ahu - 0.2, f[5] - t_ahu + 0.3, t1=f[5] + 0.3, s=0.3, sem=S(), fps=10, zs=0.4, z=3)

    # ---- frase 5-6: la viruela; Cuitláhuac
    pueblos = [CI[k] for k in ("tenochtitlan", "tlatelolco", "texcoco", "iztapalapa", "coyoacan", "tlacopan", "azcapotzalco",
                               "xochimilco", "chalco", "culhuacan", "tepeyac", "ecatepec", "huexotla", "coatlinchan", "tlahuac",
                               "mexicaltzingo", "tenayuca", "acolman", "chimalhuacan", "ayotzingo")]
    _manchas(R, t_vir - 0.2, f[6] + 0.1, pueblos, S(len(pueblos)))
    titulo(R, t_peo - 0.1, t_vir - 0.1, "EL PEOR ENEMIGO NO TRAÍA ESPADA", px=62)
    titulo(R, t_vir - 0.1, f[5] + 0.1, "LA VIRUELA", px=110, snd=True)
    pa(R, CA(8), 400, 1000, 0.95, t_vir - 0.2, t_nue - 0.1, sem=S(), extra=[(0.2, "tos", 0.35)])
    pa(R, XO(2), 760, 1015, 0.5, t_peo, t_nue - 0.1, sem=S(), flip=True, extra=[(0.3, "gemido_perro", 0.25)])
    _foto(R, "viruela", 1440, t_vir + 0.2, t_nue - 0.1, f=0.40)
    titulo(R, t_nad - 0.1, t_mil - 0.1, "AQUÍ NADIE LA CONOCÍA", px=74)
    titulo(R, t_mil - 0.1, f[6] - 0.1, "MATÓ A MILES", px=84)
    for k, g in enumerate(((-99.02, 19.50), (-98.93, 19.43), (-99.17, 19.36), (-99.06, 19.30))):
        ga(R, CA(8), g, t_epi + 0.15 * k, f[6] + 0.1, s=0.2, sem=S(), zs=0.35, z=2, extra=[(0.0, "tos", 0.22)] if k == 2 else ())
    pa(R, CA(9), 1600, 1010, 1.05, t_nue - 0.2, f[6] + 0.1, sem=S(), sale="borrar", d_out=0.9, extra=[(0.05, "caracol", 0.25)])
    R.texto(t_cui, f[6] - 0.1, "CUITLÁHUAC", (1600, 550), px=48, d=0.4)
    R.texto(t_rei - 0.1, f[6] - 0.1, "UNOS 80 DÍAS EN EL TRONO", (960, 300), px=52, d=0.5)
    pa(R, XO(6), 420, 1015, 0.55, t_nue, f[6] + 0.1, sem=S())

    # ---- frase 7: Cortés vuelve con decenas de miles de aliados y 13 bergantines
    R.anio(t_1521, 1521)
    llegada = [(-98.40, 19.56), (-98.62, 19.53), (-98.85, 19.515)]
    andar_ciclo(R, C_CAB, llegada, t_vol - 0.2, 2.8, t1=f[7] + 0.1, s=0.32, sem=S(), fps=10, zs=0.35, z=3,
                extra=[(0.0, "galope", 0.3, {"dur": 2.0})])
    for k in range(7):
        g0 = [(-98.38 - 0.02 * (k % 3), 19.55 - 0.03 * k), (-98.83 - 0.01 * (k % 3), 19.56 - 0.015 * k)]
        andar_ciclo(R, C_GUE if k % 3 else [CO(5)], g0, t_dec - 0.3 + 0.18 * k, 3.4, t1=f[7] + 0.1, s=0.22, sem=S(), fps=6, zs=0.35, z=2,
                    extra=[(0.0, "pasos", 0.3, {"dur": 2.0})] if k == 0 else ())
    titulo(R, t_dec - 0.1, t_tre - 0.2, "DECENAS DE MILES DE ALIADOS INDÍGENAS", px=58)
    _pin(R, t_vol, f[7] + 0.1, CI["texcoco"], "TEXCOCO", "izq", 40, t1_txt=t_tre - 0.1)
    for k in range(13):
        fila = k % 4
        a = (-98.905 - 0.006 * fila, 19.50 + 0.012 * fila)
        b = (-99.035 - 0.012 * (k // 4) - 0.004 * fila, 19.47 - 0.02 * fila + 0.006 * (k // 4))
        _movil(R, CA(10), [a, b], t_tre + 0.12 * k, 3.6, t1=f[7] + 0.1, s=0.17, zs=0.4, z=3,
               extra=[(0.0, "remo", 0.22)] if k % 5 == 0 else ())
    R.contador(t_tre - 0.1, t_ber + 0.6, 0, 13, (960, 196), px=74, formato="{:,} BERGANTINES", hasta_t=f[7] + 0.1)
    pa(R, CA(10), 1580, 1005, 0.9, t_ber - 0.2, f[7] + 0.1, sem=S(), extra=[(0.05, "ola", 0.25, {"dur": 1.5})])
    R.texto(t_pzs - 0.1, f[7] - 0.1, "ARMADOS PIEZA POR PIEZA", (960, 296), px=52, d=0.5)
    R.snd(t_pzs, "cincel", 0.3, dur=1.4)
    pa(R, XO(7), 380, 1015, 0.5, t_vol, f[7] + 0.1, sem=S(), flip=True)

    # ---- frase 8: el acueducto cortado, sin agua, sin comida, con la peste: casi tres meses
    acu = [CI["chapultepec"], (-99.168, 19.426), (-99.152, 19.432), (-99.138, 19.4345)]
    R.rio(acu, t_cor - 1.0, 0.8, (88, 148, 196), ancho=9, t1=t_cor + 0.5)
    ga(R, M1(4), CI["chapultepec"], t_cor - 0.6, f[8] + 0.1, s=0.17, off=(60, 10), sem=S(), zs=0.3, z=2)
    _pin(R, t_cha - 0.15, f[8], CI["chapultepec"], "CHAPULTEPEC", "izq", 40)
    titulo(R, t_cor - 0.1, t_agu - 0.1, "¡CORTARON EL ACUEDUCTO!", px=74, snd=True)
    ga(R, A.estallido(), (-99.160, 19.429), t_cor + 0.4, t_cor + 1.3, s=0.36, sem=S(), zs=0.3, z=3, extra=[(0.0, "impacto", 0.35)])
    for k, (tt, txt) in enumerate(((t_agu, "SIN AGUA DULCE"), (t_com, "SIN COMIDA"), (t_pst, "CON LA PESTE"))):
        R.texto(tt - 0.05, t_res - 0.15, txt, (960, 196 + 74 * k), px=56, d=0.4)
    pa(R, MI(6), 1240, 1005, 0.6, t_com - 0.15, f[8] + 0.1, sem=S())
    pa(R, MI(5), 1530, 1015, 0.62, t_com - 0.05, f[8] + 0.1, sem=S(), flip=True, extra=[(0.3, "gemido_perro", 0.3)])
    pa(R, CA(8), 420, 1000, 0.8, t_pst - 0.15, t_res - 0.1, sem=S(), extra=[(0.1, "tos", 0.3)])
    _foto(R, "tzilacatzin", 500, t_res - 0.05, f[8] + 0.2, f=0.40)
    titulo(R, t_res - 0.1, f[8] - 0.1, "RESISTIÓ CASI 3 MESES", px=78)
    ronda = [(-99.112, 19.425), (-99.118, 19.452), (-99.128, 19.462), (-99.150, 19.460), (-99.158, 19.445)]
    for k in range(3):
        _movil(R, CA(10), ronda[k:] + ronda[:k], t_cor + 0.4 * k, f[10] - t_cor, t1=f[10] + 0.1, s=0.13, zs=0.3, z=2)

    # ---- frase 9: Cuauhtémoc, «el águila que desciende», unos 25 años
    pa(R, CA(11), 400, 1015, 1.1, f[8] + 0.25, f[9] + 0.1, sem=S(), extra=[(0.05, "caracol", 0.3)])
    R.texto(t_cua, f[9] - 0.1, "CUAUHTÉMOC", (400, 540), px=52, d=0.4)
    titulo(R, t_ult - 0.1, t_agi - 0.2, "EL ÚLTIMO TLATOANI", px=78)
    pa(R, AL(6), 1560, 1010, 1.0, t_agi - 0.2, f[9] + 0.1, entra="baja_entra", dy=900, sem=S(), extra=[(0.0, "aguila", 0.4)])
    titulo(R, t_agi - 0.1, f[9] - 0.1, "«ÁGUILA QUE DESCIENDE»", px=74)
    R.contador(t_25 - 0.1, t_25 + 0.8, 0, 25, (960, 300), px=60, formato="UNOS {:,} AÑOS", hasta_t=f[9] - 0.05)
    pa(R, XO(0), 700, 1015, 0.46, t_cua, f[9] + 0.1, sem=S())

    # ---- frase 10: 13 de agosto de 1521, Cuauhtémoc capturado en una canoa; Tenochtitlan cayó
    titulo(R, t_13 - 0.1, t_cay - 0.2, "13 DE AGOSTO DE 1521", px=80, snd=True)
    huida = [(-99.118, 19.458), (-99.106, 19.463), (-99.095, 19.468)]
    R.act(CA(11), pos_geo=R.camino_pos(huida, t_13, t_cap - t_13 + 0.3), off=(0, 20), s=0.26, t_in=t_13, d_in=0.3, entra="pop",
          sem=S(), zs=0.3, z=3, t_out=t_cay + 0.6, flip=False, sfx=[(0.2, "remo", 0.3)])
    R.act(CA(10), pos_geo=R.camino_pos([(-99.070, 19.480), (-99.086, 19.473)], t_13 + 0.3, t_cap - t_13), off=(30, 10), s=0.26,
          t_in=t_13 + 0.3, d_in=0.3, entra="pop", sem=S(), zs=0.3, z=3, t_out=t_cay + 0.6, flip=True)
    ga(R, A.estallido(), huida[-1], t_cap + 0.1, t_cap + 1.2, s=0.4, off=(20, -60), sem=S(), zs=0.3, z=4, extra=[(0.0, "impacto", 0.4)])
    R.texto(t_cap + 0.15, t_cay - 0.15, "¡CAPTURADO!", (560, 420), px=64, d=0.4)
    ga(R, AH(1), TM, t_13, t_cay + 0.2, s=0.25, off=(0, 0), sem=S(), zs=0.28, z=1, sale="caer", d_out=1.0)
    titulo(R, t_cay - 0.1, f[10] - 0.05, "TENOCHTITLAN CAYÓ", px=96)
    R.snd(t_cay + 0.15, "impacto", 0.4)
    R.snd(t_cay + 0.6, "campana", 0.3)
    pa(R, XO(2), 330, 1015, 0.55, t_13, f[10] + 0.1, sem=S())
    _foto(R, "captura_cuauhtemoc", 1440, t_cap - 0.2, f[10] + 0.2, f=0.40)

    # ---- frase 11: casi 200 años después del águila sobre el nopal
    pa(R, FU(0), 960, 1000, 1.05, t_casi - 0.2, fin + 0.3, sem=S(), entra="sube", dy=320, extra=[(0.3, "aguila", 0.25)])
    titulo(R, t_casi - 0.1, fin, "1325 · 1521", px=86)
    R.contador(t_200 - 0.1, t_nop + 0.3, 0, 196, (960, 300), px=60, formato="{:,} AÑOS", hasta_t=fin + 0.2)
    pa(R, XO(6), 1560, 1015, 0.6, t_casi, fin + 0.3, sem=S())
    for c in (0, 30):                         # el imperio se acaba (el de coreo_3 vive en la capa 30)
        if ("mx", c) in R.terr:
            R.terreno(t_casi, None, COL["imperio_1519"], 1.6, capa=c)
    R.terreno(t_casi, None, COL["tlaxcala"], 1.2, capa=41)


# ------------------------------------------------------------------ EL LEGADO
def _legado(R):
    e = "legado"
    i0 = INI(e)
    t_rui, t_con, t_cdmx, t_pie = T(e, "ruinas"), T(e, "construyeron"), T(e, "ciudad de mexico", frase=0), T(e, "piedras", frase=0)
    t_sec, t_lag, t_poco, t_hoy, t_hun, t_cm = (T(e, "secaron"), T(e, "lagos", frase=1), T(e, "poco a poco"), T(e, "hoy", frase=1),
                                                T(e, "hunde"), T(e, "centimetros"))
    t_nun, t_mill, t_hab = T(e, "nunca", frase=2), T(e, "millon"), T(e, "hablan")
    t_tu, t_tom, t_agu, t_cac, t_pap, t_pal = (T(e, "tu", frase=3), T(e, "tomate"), T(e, "aguacate"), T(e, "cacahuate"),
                                               T(e, "papalote"), T(e, "palabras"))
    t_agi, t_ban, t_nom, t_mex = T(e, "aguila", frase=4), T(e, "bandera"), T(e, "nombre"), T(e, "mexicas", frase=4)
    t_yx, t_par, t_des, t_sig, t_cri, t_2026, t_cdmx2, t_patr = (T(e, "xolo", frase=5), T(e, "parientes"), T(e, "desaparecen"),
                                                                 T(e, "siglo"), T(e, "criadores"), T(e, "2026"),
                                                                 T(e, "ciudad de mexico", frase=5), T(e, "patrimonio"))
    t_xol, t_gui, t_alm, t_cru, t_mic, t_mun = (T(e, "xoloitzcuintle"), T(e, "guiar"), T(e, "almas"), T(e, "cruzar"), T(e, "mictlan"),
                                                T(e, "mundo"))
    t_osea, t_menu, t_gui2 = T(e, "o sea"), T(e, "menu"), T(e, "guia", frase=7)
    f = [FIN(e, k) for k in range(8)]
    fin = FIN(e)

    _cam(i0 - 0.2, -99.120, 19.432, 16.0)
    _cam(t_con, -99.132, 19.435, 30.0)
    _cam(f[0] - 0.3, -99.132, 19.434, 28.0)
    _cam(t_sec + 0.6, -99.03, 19.44, 6.4)
    _cam(t_hoy + 0.3, -99.06, 19.40, 6.0)
    _cam(f[1], -99.05, 19.40, 5.6)
    _cam(t_mill, -98.20, 19.70, 1.05)
    _cam(f[2], -98.15, 19.60, 1.1)
    _cam(t_pal, -98.30, 19.50, 1.25)
    _cam(t_ban, -97.80, 18.60, 0.85)
    _cam(f[4], -97.75, 18.55, 0.80)
    _cam(t_sig, -98.60, 19.20, 1.6)
    _cam(t_cdmx2 + 0.3, -99.12, 19.33, 4.0)
    _cam(f[5], -99.12, 19.33, 4.4)
    _cam(t_mic, -99.10, 19.38, 5.2)
    _cam(t_gui2, -99.11, 19.40, 6.5)
    _cam(fin - 0.25, -99.12, 19.42, 8.0)

    # ---- frase 0: sobre las ruinas, la Ciudad de México con las piedras de los templos
    R.anio(i0, 1524)
    R.sello(i0 + 0.3, "corona", "NUEVA ESPAÑA", color=(176, 52, 48))
    ga(R, AH(1), TM, _tc("caida", e), t_pie + 1.4, s=0.3, off=(-160, 10), sem=S(), zs=0.28, z=1, sale="encoger", d_out=0.9)
    ga(R, LE(0), TM, t_con - 0.15, f[0] + 0.1, s=0.36, off=(130, 30), sem=S(), zs=0.28, z=2, entra="sube", dy=240,
       extra=[(0.05, "cincel", 0.35, {"dur": 1.2})])
    _foto(R, "templo_mayor_ruinas", 470, t_rui - 0.1, f[0] + 0.1, f=0.40)
    titulo(R, t_cdmx - 0.1, f[0] - 0.1, "LA CIUDAD DE MÉXICO", px=86, snd=True)
    R.snd(t_cdmx + 0.3, "campana", 0.3)
    for k in range(5):
        _arco(R, AX(5), (TM[0] - 0.0016, TM[1] + 0.0002), (TM[0] + 0.0013, TM[1] - 0.0001), t_pie - 0.1 + 0.3 * k, 0.8,
              t_pie + 0.7 + 0.3 * k, s=0.09)
    R.snd(t_pie + 0.2, "piedra", 0.35)
    R.texto(t_pie - 0.05, f[0] - 0.1, "CON LAS PIEDRAS DE LOS TEMPLOS", (960, 300), px=52, d=0.6)
    pa(R, XO(7), 1200, 1015, 0.55, i0 + 0.1, f[0] + 0.1, sem=S(), flip=True)

    # ---- frase 1: secaron los lagos… y la ciudad se hunde
    R.anio(t_sec, 1600)
    R.anio(t_poco, 1900)
    R.anio(t_hoy, 2026)
    titulo(R, t_sec - 0.1, t_hoy - 0.2, "SECARON LOS LAGOS", px=86, snd=True)
    R.snd(t_lag, "viento_frio", 0.25, dur=2.4)
    pa(R, XO(2), 1180, 1015, 0.55, t_sec, f[1] + 0.1, sem=S(), extra=[(0.6, "gemido_perro", 0.22)])
    _pin(R, t_hoy - 0.1, f[1] + 0.1, TEN, "CIUDAD DE MÉXICO", "abajo", 42)
    R.snd(t_hoy, "ciudad", 0.3, dur=2.4)
    R.act(LE(1), pos=lambda t, a=t_hun - 0.3: (1560, 1010 + 70 * e_inout(prog(t, a + 0.4, f[1])), 0.95, -0.04 * prog(t, a, f[1])),
          t_in=t_hun - 0.3, d_in=0.45, entra="pop", sem=S(), t_out=f[1] + 0.1, sale="baja", z=3, sfx=[(0.3, "piedra", 0.3)])
    titulo(R, t_hun - 0.1, f[1] - 0.1, "LA CIUDAD SE HUNDE", px=82)
    R.texto(t_cm - 0.1, f[1] - 0.1, "VARIOS CENTÍMETROS CADA AÑO", (960, 300), px=52, d=0.6)

    # ---- frase 2: más de un millón y medio hablan náhuatl
    pa(R, LE(12), 360, 1010, 1.05, t_nun - 0.15, t_tom - 0.35, sem=S(), extra=[(0.05, "flauta", 0.3)])
    titulo(R, t_nun - 0.1, t_mill - 0.2, "NUNCA SE FUERON DEL TODO", px=76)
    R.contador(t_mill - 0.1, t_hab + 0.6, 0, 1651958, (960, 196), px=64, formato="{:,} HABLAN NÁHUATL", hasta_t=f[2] + 0.1)
    for k, g in enumerate(((-98.55, 21.0), (-97.75, 19.95), (-97.05, 18.68), (-98.60, 17.55), (-99.03, 19.19), (-97.95, 20.35),
                           (-98.25, 19.05))):
        ga(R, LE(12), g, t_hab - 0.3 + 0.16 * k, f[2] + 0.1, s=0.3, sem=S(), zs=0.4, z=2,
           extra=[(0.0, "pop", 0.25, {"tono": 0.9 + 0.06 * k})] if k % 3 == 0 else ())
    pa(R, XO(0), 1600, 1015, 0.58, t_nun, t_pap - 0.3, sem=S(), extra=[(0.4, "ladrido", 0.25)])

    # ---- frase 3: tomate, aguacate, cacahuate, papalote
    titulo(R, t_tu - 0.1, t_pal - 0.15, "Y TÚ TAMBIÉN LO HABLAS", px=76)
    for k, (tt, dib, x, s, pal, raiz) in enumerate(((t_tom, LE(3), 330, 0.62, "TOMATE", "tomatl"),
                                                    (t_agu, LE(4), 760, 0.62, "AGUACATE", "ahuacatl"),
                                                    (t_cac, LE(7), 1180, 0.58, "CACAHUATE", "cacáhuatl"))):
        pa(R, dib, x, 1000, s, tt - 0.15, f[3] + 0.1, sem=S(), extra=[(0.05, "pop", 0.3, {"tono": 0.95 + 0.08 * k})])
        R.texto(tt, f[3] - 0.1, pal, (x, 640), px=52, d=0.35)
        R.texto(tt + 0.3, f[3] - 0.1, raiz, (x, 700), px=40, d=0.35)
    pa(R, _papalote(), 1500, 1000, 0.72, t_pap - 0.15, f[3] + 0.1, sem=S(), extra=[(0.05, "viento_frio", 0.2, {"dur": 0.9})])
    R.texto(t_pap, f[3] - 0.1, "PAPALOTE", (1560, 300), px=52, d=0.35)
    R.texto(t_pap + 0.3, f[3] - 0.1, "papalotl: mariposa", (1560, 360), px=38, d=0.35)
    pa(R, XO(5), 1560, 1020, 0.48, t_pap - 0.05, f[3] + 0.1, sem=S(), extra=[(0.2, "ladrido", 0.3)])
    titulo(R, t_pal - 0.1, f[3] - 0.1, "¡PALABRAS EN NÁHUATL!", px=78, snd=True)

    # ---- frase 4: el águila de la bandera; México viene de los mexicas
    pa(R, FU(1), 380, 1000, 0.85, t_agi - 0.2, f[4] + 0.1, sem=S(), extra=[(0.05, "aguila", 0.3)])
    R.act(LE(11), pos=lambda t: (1000, 1010, 1.2, 0.04 * math.sin(t * 2.3)), t_in=t_ban - 0.25, d_in=0.5, entra="sube", dy=420,
          sem=S(), t_out=f[4] + 0.1, sale="encoger", z=3, sfx=[(0.1, "fanfarria", 0.35)])
    R.terreno(t_nom - 0.2, "mexico_mod", COL["mexico_mod"], 1.0, capa=44)
    titulo(R, t_nom - 0.1, f[4] - 0.1, "MEXICAS · MÉXICO", px=88, snd=True)
    R.terreno(f[4] + 0.1, None, COL["mexico_mod"], 0.8, capa=44)

    # ---- frase 5: ¿y Xolo? casi desaparecen; los criadores; patrimonio de la CDMX en 2026
    pa(R, XO(0), 960, 1015, 1.05, t_yx - 0.25, t_par + 0.2, sem=S(), extra=[(0.1, "ladrido", 0.35)])
    titulo(R, t_yx - 0.1, t_par - 0.15, "¿Y XOLO?", px=100, snd=True)
    pa(R, MI(2), 330, 1000, 0.7, t_par - 0.15, t_cri - 0.2, sem=S(), extra=[(0.05, "piedra", 0.25)])
    R.texto(t_par, t_cri - 0.2, "SUS PARIENTES DE BARRO (COLIMA)", (960, 196), px=56, d=0.5)
    _foto(R, "perro_colima", 1450, t_par + 0.1, t_cri - 0.3, f=0.38)
    _foto(R, "xolo_vivo2", 480, t_cri, t_2026 + 0.1, f=0.40)
    for k in range(5):
        pa(R, XO(1), 640 + 110 * k, 1015 - 10 * (k % 2), 0.4, t_par + 0.3 + 0.15 * k, t_des + 0.3 + 0.25 * k if k else t_2026, sem=S(),
           sale="borrar", d_out=0.6)
    R.texto(t_des - 0.05, t_cri - 0.2, "CASI DESAPARECEN", (960, 300), px=58, d=0.4)
    R.anio(t_sig, 1956)
    pa(R, MI(3), 1560, 1010, 1.05, t_cri - 0.2, t_2026 + 0.2, sem=S(), extra=[(0.05, "brillo", 0.3)])
    titulo(R, t_cri - 0.1, t_2026 - 0.2, "LOS CRIADORES MEXICANOS LOS RESCATARON", px=54)
    R.anio(t_2026, 2026)
    _pin(R, t_cdmx2 - 0.15, f[5] + 0.1, TEN, "CIUDAD DE MÉXICO", "abajo", 40)
    pa(R, MI(7), 960, 1015, 0.95, t_cdmx2 - 0.2, f[5] + 0.1, sem=S(), entra="sube", dy=300, extra=[(0.1, "fanfarria", 0.3)])
    R.sello(t_patr - 0.1, "aguila", "PATRIMONIO CULTURAL", color=(120, 70, 150))
    titulo(R, t_patr - 0.1, f[5] - 0.1, "PATRIMONIO CULTURAL DE LA CDMX", px=66, snd=True)

    # ---- frase 6: guía de las almas hacia el Mictlán (remate emocional, de noche)
    R.trans.append(_Velo(t_xol - 0.2, t_gui2 + 0.2, MICTLAN, d=1.1, k=0.9))
    titulo(R, t_xol - 0.1, t_mic - 0.2, "UN TRABAJO MUY IMPORTANTE", px=70)
    pa(R, XO(0), 960, 1015, 0.9, f[5] + 0.2, t_gui - 0.2, sem=S(), extra=[(0.2, "ladrido", 0.25)])
    R.act(MI(0), pos=lambda t, a=t_gui - 0.3: (lerp(260, 900, e_inout(prog(t, a, t_cru))), 1010, 1.0), t_in=t_gui - 0.3, d_in=0.5,
          entra="pop", sem=S(), t_out=t_cru, sale="borrar", d_out=0.4, z=4, sfx=[(0.2, "flauta", 0.35)])
    R.texto(t_alm - 0.05, t_cru - 0.1, "GUIAR A LAS ALMAS", (960, 300), px=56, d=0.5)
    for k, (n, x, an) in enumerate(((2, 260, 520), (3, 640, 240), (2, 980, 520), (6, 1330, 260), (2, 1680, 520),
                                    (4, 460, 180), (6, 1160, 200), (3, 1500, 220))):
        _ola(R, n, x, 1000 if k < 5 else 1070, an * 1.25, t_cru - 0.5 + 0.06 * k, f[6] + 0.1, z=3 if k < 5 else 6, entra="sube")
    R.snd(t_cru - 0.3, "agua_lago", 0.35, dur=3.5)
    R.act(MI(1), pos=lambda t, a=t_cru: (lerp(420, 1500, e_inout(prog(t, a, f[6]))), 1030 + 10 * math.sin(t * 4), 0.95),
          t_in=t_cru, d_in=0.5, entra="pop", sem=S(), t_out=f[6] + 0.1, z=5)
    titulo(R, t_mic - 0.1, f[6] - 0.1, "MICTLÁN", px=110, snd=True)
    R.texto(t_mun - 0.05, f[6] - 0.1, "EL MUNDO DE LOS MUERTOS", (900, 300), px=56, d=0.5)
    _foto(R, "xolotl_borgia", 1600, t_alm, f[6] + 0.2, f=0.34, y=720)
    R.texto(t_alm + 0.3, f[6] - 0.1, "XÓLOTL, EL DIOS PERRO", (1600, 330), px=40, d=0.4)
    R.snd(t_mun + 0.4, "aullido", 0.2)

    # ---- frase 7: nunca terminó en el menú: terminó siendo el guía
    pa(R, MI(6), 520, 1005, 0.75, t_osea - 0.2, t_menu + 0.6, sem=S(), sale="encoger", d_out=0.5)
    pa(R, MI(5), 860, 1015, 0.62, t_osea - 0.1, t_menu + 0.6, sem=S(), flip=True)
    R.texto(t_menu - 0.1, t_gui2 - 0.2, "¿EL MENÚ? ¡NUNCA!", (960, 300), px=58, d=0.4)
    R.snd(t_menu + 0.5, "pop", 0.35, tono=0.8)
    pa(R, MI(0), 1000, 1010, 1.2, t_gui2 - 0.4, fin + 0.3, sem=S(), entra="sube", dy=320, extra=[(0.2, "brillo", 0.4)])
    titulo(R, t_gui2 - 0.1, fin, "EL GUÍA", px=120, snd=True)
    R.snd(t_gui2 + 0.6, "ladrido", 0.3)


# ------------------------------------------------------------------ LA RUTA PARA VISITAR HOY
def _ruta(R):
    e = "ruta"
    i0 = INI(e)
    t_qui, t_zoc, t_mtm, t_coy, t_tra, t_1978 = (T(e, "quieres"), T(e, "zocalo"), T(e, "museo del templo mayor"), T(e, "coyolxauhqui"),
                                                 T(e, "trabajadores"), T(e, "1978"))
    t_sig, t_mna, t_ps, t_coa = T(e, "sigue"), T(e, "museo nacional"), T(e, "piedra del sol"), T(e, "coatlicue")
    t_lue, t_tla, t_3c, t_cay, t_xoc, t_chi = (T(e, "luego"), T(e, "tlatelolco"), T(e, "tres culturas"), T(e, "cayo"),
                                               T(e, "xochimilco"), T(e, "chinampas"))
    t_dia, t_teo, t_rui, t_lle, t_aso = T(e, "dia mas"), T(e, "teotihuacan", frase=3), T(e, "ruinas"), T(e, "llegaron"), T(e, "asombro")
    t_dej, t_des = T(e, "dejo"), T(e, "descripcion")
    f = [FIN(e, k) for k in range(5)]
    fin = FIN(e)
    TLA, TEO = CI["tlatelolco"], CI["teotihuacan"]

    _cam(i0 - 0.2, -99.128, 19.440, 22.0)
    _cam(t_zoc + 0.3, -99.131, 19.442, 28.0)
    _cam(t_1978, -99.133, 19.442, 29.0)
    _cam(t_sig + 0.2, -99.150, 19.432, 24.0)
    _cam(t_mna + 0.4, -99.162, 19.430, 22.0)
    _cam(f[1], -99.158, 19.436, 21.0)
    _cam(t_tla + 0.3, -99.140, 19.456, 22.0)
    _cam(t_cay + 0.4, -99.139, 19.456, 21.0)
    _cam(t_xoc - 0.4, -99.120, 19.330, 9.0)
    _cam(t_chi + 0.2, -99.100, 19.262, 14.0)
    _cam(f[2], -99.090, 19.300, 9.0)
    _cam(t_teo + 0.3, -98.99, 19.66, 6.0)
    _cam(t_aso, -99.00, 19.62, 5.4)
    _cam(t_dej + 0.2, -99.01, 19.56, 4.3)
    _cam(fin - 0.25, -99.01, 19.56, 4.2)

    R.anio(i0, 2026)
    R.sello(i0 + 0.3, "piramide_mx", "SE PUEDE VISITAR", color=(64, 128, 96))

    # ---- frase 0: el Zócalo y el Museo del Templo Mayor; la Coyolxauhqui de 1978
    pa(R, RU(0), 330, 1010, 1.0, _tc("legado", e), t_tra - 0.1, sem=S(), extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    pa(R, XO(1), 560, 1015, 0.5, i0 + 0.15, t_tra - 0.1, sem=S(), extra=[(0.3, "ladrido", 0.25)])
    titulo(R, t_qui - 0.1, t_zoc - 0.2, "COMPRUÉBALO CON TUS OJOS", px=72)
    llegar = [(-99.150, 19.441), (-99.141, 19.437), TM]
    R.ruta(llegar, i0 + 0.6, 2.2, ancho=5.0, t1=f[0], flecha=True)
    andar_ciclo(R, C_XOLO, llegar, i0 + 0.6, 2.4, t1=t_mtm, s=0.24, sem=S(), fps=12, zs=0.25, z=3,
                extra=[(0.0, "ladrido", 0.22)])
    _pin(R, t_zoc - 0.1, fin + 0.3, TM, "ZÓCALO", "abajo", 40, t1_txt=t_ps - 0.3, sfx=True)
    titulo(R, t_mtm - 0.1, f[0] - 0.1, "HOY: MUSEO DEL TEMPLO MAYOR", px=66, snd=True)
    ga(R, RU(5), TM, t_mtm, f[0] + 0.1, s=0.22, off=(-90, -20), sem=S(), zs=0.25, z=2)
    ga(R, RU(2), TM, t_coy - 0.15, f[0] + 0.1, s=0.2, off=(110, 70), sem=S(), zs=0.25, z=3, extra=[(0.05, "brillo", 0.3)])
    # (tzompantli_piedra NO: «Mexico-6064 Wall of Skulls» de D. Jarvis parece el tzompantli de Chichén Itzá, no el del Templo Mayor)
    pa(R, AH(1), 1440, 1000, 0.95, t_zoc + 0.1, t_coy - 0.2, sem=S(), entra="sube", dy=300, extra=[(0.05, "crece", 0.3)])
    pa(R, RU(2), 1440, 1000, 1.0, t_coy - 0.15, f[0] + 0.2, sem=S(), extra=[(0.05, "piedra", 0.3)])
    R.texto(t_coy + 0.2, f[0] - 0.1, "LA COYOLXAUHQUI", (1440, 470), px=46, d=0.4)
    pa(R, RU(1), 330, 1010, 1.0, t_tra - 0.15, f[0] + 0.1, sem=S(), extra=[(0.05, "cincel", 0.3, {"dur": 1.0})])
    R.texto(t_tra + 0.1, f[0] - 0.1, "TRABAJADORES DE LA LUZ", (480, 560), px=40, d=0.4)
    R.texto(t_1978 - 0.1, f[0] - 0.1, "EN 1978", (330, 480), px=70, d=0.4)

    # ---- frase 1: Museo Nacional de Antropología: Piedra del Sol y Coatlicue
    vis = [TM, (-99.150, 19.433), (-99.170, 19.428), MNA]
    R.ruta(vis, t_sig - 0.2, 1.4, ancho=5.0, t1=fin + 0.3, flecha=True)
    andar_ciclo(R, C_XOLO, vis, t_sig - 0.2, 1.6, t1=t_mna + 0.2, s=0.26, sem=S(), fps=12, zs=0.25, z=3)
    _pin(R, t_mna - 0.1, fin + 0.3, MNA, "ANTROPOLOGÍA", "abajo", 40, t1_txt=f[1] - 0.1, sfx=True)
    titulo(R, t_mna - 0.1, f[1] - 0.1, "HOY: MUSEO NACIONAL DE ANTROPOLOGÍA", px=60, snd=True)
    ga(R, RU(5), MNA, t_mna, f[1] + 0.1, s=0.32, off=(0, -20), sem=S(), zs=0.25, z=2)
    _foto(R, "mna_paraguas", 470, t_mna - 0.05, t_ps + 0.6, f=0.40)
    pa(R, RU(4), 1440, 1000, 1.05, t_ps - 0.15, f[1] + 0.3, sem=S(), extra=[(0.05, "brillo", 0.3)])
    R.texto(t_ps + 0.1, f[1] - 0.1, "PIEDRA DEL SOL", (1440, 560), px=44, d=0.4)
    _foto(R, "coatlicue", 470, t_coa - 0.1, t_tla + 0.6, f=0.44)
    R.texto(t_coa + 0.1, t_lue - 0.1, "COATLICUE", (470, 450), px=44, d=0.4)
    ga(R, RU(3), MNA, t_coa - 0.1, f[1] + 0.1, s=0.2, off=(150, -10), sem=S(), zs=0.25, z=3)

    # ---- frase 2: Tlatelolco (Tres Culturas) y Xochimilco (chinampas)
    v2 = [MNA, (-99.165, 19.440), (-99.150, 19.448), TLA]
    R.ruta(v2, t_lue - 0.1, 1.2, ancho=5.0, t1=fin + 0.3, flecha=True)
    andar_ciclo(R, C_XOLO, v2, t_lue - 0.1, 1.3, t1=t_xoc - 0.2, s=0.26, sem=S(), fps=12, zs=0.25, z=3)
    _pin(R, t_tla - 0.1, fin + 0.3, TLA, "TLATELOLCO", "izq", 40, t1_txt=t_cay, sfx=True)
    titulo(R, t_tla - 0.1, t_xoc - 0.2, "HOY: TLATELOLCO, TRES CULTURAS", px=62, snd=True)
    ga(R, RU(6), TLA, t_3c - 0.1, t_xoc, s=0.22, off=(60, 70), sem=S(), zs=0.25, z=2)
    _foto(R, "tres_culturas", 1440, t_3c - 0.1, t_xoc + 0.2, f=0.40)
    R.texto(t_cay - 0.1, t_xoc - 0.2, "DONDE CAYÓ LA CIUDAD", (960, 300), px=52, d=0.4)
    v3 = [TLA, (-99.120, 19.420), (-99.105, 19.350), (-99.100, 19.290), XOCHI]
    R.ruta(v3, t_xoc - 0.4, 1.4, ancho=5.0, t1=fin + 0.3, flecha=True)
    _pin(R, t_xoc - 0.1, fin + 0.3, XOCHI, "XOCHIMILCO", "abajo", 40, t1_txt=t_dia + 0.3, sfx=True)
    titulo(R, t_xoc - 0.05, f[2] - 0.1, "HOY: XOCHIMILCO", px=76, snd=True)
    _movil(R, RU(8), [(XOCHI[0] - 0.006, XOCHI[1] + 0.004), (XOCHI[0] + 0.006, XOCHI[1] + 0.001)], t_xoc + 0.2, 5.5, t1=f[2] + 0.2,
           s=0.32, zs=0.3, z=2, flip=False, extra=[(0.1, "trajinera", 0.35, {"dur": 3.0})])
    pa(R, RU(8), 470, 1000, 0.85, t_chi - 0.25, f[2] + 0.3, sem=S(), extra=[(0.05, "agua_lago", 0.25, {"dur": 1.5})])
    pa(R, MI(4), 1520, 1010, 0.9, t_chi - 0.2, f[2] + 0.2, sem=S(), extra=[(0.1, "ladrido", 0.25)])

    # ---- frase 3: Teotihuacan, ya en ruinas cuando llegaron los mexicas
    v4 = [XOCHI, (-99.06, 19.36), (-98.98, 19.50), (-98.90, 19.62), TEO]
    R.ruta(v4, t_dia - 0.1, 1.8, ancho=5.0, t1=fin + 0.3, flecha=True)
    andar_ciclo(R, C_XOLO, v4, t_dia - 0.1, 2.0, t1=t_rui, s=0.26, sem=S(), fps=12, zs=0.35, z=3)
    _pin(R, t_teo - 0.1, fin + 0.3, TEO, "TEOTIHUACAN", "der", 42, t1_txt=t_dej - 0.2, sfx=True)
    titulo(R, t_teo - 0.05, f[3] - 0.1, "HOY: TEOTIHUACAN", px=80, snd=True)
    ga(R, RU(9), TEO, t_teo, f[3] + 0.2, s=0.3, off=(-110, 10), sem=S(), zs=0.35, z=2, entra="sube", dy=200,
       extra=[(0.05, "crece", 0.3)])
    _foto(R, "teotihuacan_sol", 470, t_teo + 0.2, t_lle - 0.15, f=0.40)
    R.texto(t_rui - 0.1, f[3] - 0.1, "YA ESTABA EN RUINAS", (700, 300), px=56, d=0.4)
    grupo = [TEN, (-99.03, 19.53), (-98.93, 19.63), (-98.865, 19.68)]
    for k in range(3):
        andar_ciclo(R, C_MEX, grupo, t_lle - 0.3 + 0.2 * k, f[3] - t_lle + 0.4, t1=f[3] + 0.2, s=0.24, sem=S(), fps=8, zs=0.35, z=2,
                    off=(-40 * k, 12 * (k % 2)), extra=[(0.0, "pasos", 0.25, {"dur": 2.0})] if k == 0 else ())
    pa(R, MG(0), 380, 1010, 1.0, t_lle - 0.2, f[3] + 0.1, sem=S())
    R.texto(t_aso - 0.1, f[3] - 0.1, "¡CON ASOMBRO!", (420, 560), px=50, d=0.4)
    pa(R, XO(5), 760, 1015, 0.5, t_aso - 0.1, f[3] + 0.1, sem=S(), extra=[(0.1, "ladrido", 0.3)])

    # ---- frase 4: cómo llegar, en la descripción
    titulo(R, t_dej - 0.1, fin + 0.3, "CÓMO LLEGAR: EN LA DESCRIPCIÓN", px=70, snd=True)
    for k, (g, txt, lado) in enumerate(((TM, "TEMPLO MAYOR", "der"), (MNA, "ANTROPOLOGÍA", "izq"), (TLA, "TLATELOLCO", "arriba"),
                                        (XOCHI, "XOCHIMILCO", "der"), (TEO, "TEOTIHUACAN", "der"))):
        mw = B.ancho_texto(txt, 36)
        dx, dy = {"arriba": (0, -50), "abajo": (0, 52), "der": (28 + mw / 2, 0), "izq": (-28 - mw / 2, 0)}[lado]
        R.texto(t_dej + 0.15 * k, fin + 0.2, txt, None, px=36, d=0.4, geo=g, off=(dx, dy))
    pa(R, RU(0), 1600, 1010, 1.0, t_dej - 0.15, fin + 0.3, sem=S(), flip=True, extra=[(0.05, "papel", 0.3)])
    pa(R, XO(1), 380, 1015, 0.55, t_dej, fin + 0.3, sem=S())


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_tri, t_imp, t_pai = T(e, "tribu"), T(e, "imperio"), T(e, "pais")
    t_que, t_com, t_sus, t_cro, t_xol, t_agr = (T(e, "que otra"), T(e, "comentarios"), T(e, "suscribete"), T(e, "cronopapel"),
                                                T(e, "xolo", frase=1), T(e, "agradece"))
    f0 = FIN(e, 0)
    fin = FIN(e)

    _cam(i0 - 0.2, -99.0, 19.5, 3.0)
    _cam(t_tri + 0.3, -98.6, 19.3, 1.3)
    _cam(t_imp + 0.4, -97.40, 18.15, 0.6)
    _cam(f0, -97.45, 18.20, 0.62)
    _cam(t_sus, -97.70, 18.40, 0.7)
    _cam(fin - 0.25, -97.70, 18.45, 0.72)

    # ---- frase 0: de una tribu que nadie quería… al imperio… y a un país
    pa(R, MG(0), 380, 1010, 1.0, _tc("ruta", e), t_imp + 0.2, sem=S(), extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    pa(R, XO(1), 620, 1015, 0.5, i0, t_imp + 0.2, sem=S())
    R.ruta(M.RUTAS["migracion"], i0, 2.2, ancho=5.0, t1=f0 + 0.2, flecha=True)
    titulo(R, t_tri - 0.1, t_imp - 0.15, "UNA TRIBU QUE NADIE QUERÍA…", px=72)
    R.terreno(t_imp - 0.2, "imperio_1519", COL["imperio_1519"], 1.0, capa=44)
    titulo(R, t_imp - 0.1, t_pai - 0.15, "…UN IMPERIO…", px=84, snd=True)
    R.snd(t_imp, "caracol", 0.35)
    R.terreno(t_pai - 0.2, "mexico_mod", COL["mexico_mod"], 1.0, capa=44)
    pa(R, LE(11), 1560, 1010, 1.1, t_pai - 0.3, f0 + 0.2, sem=S(), extra=[(0.1, "fanfarria", 0.35)])
    titulo(R, t_pai - 0.1, f0 - 0.05, "…Y EL NOMBRE DE UN PAÍS", px=78)

    # ---- frase 1: comentarios, suscríbete; Xolo se despide
    titulo(R, t_que - 0.1, t_sus - 0.2, "¿QUÉ CIVILIZACIÓN CONTAMOS AHORA?", px=64, snd=True)
    pa(R, OC.globo_dialogo(), 1450, 560, 1.0, t_com - 0.2, t_sus - 0.1, sem=S(), z=6, extra=[(0.05, "pop", 0.3)])
    R.texto(t_com - 0.1, t_sus - 0.2, "DÉJAMELO EN LOS COMENTARIOS", (960, 300), px=54, d=0.5)
    R.texto(t_com + 0.1, t_sus - 0.2, "¿CUÁL?", (1450, 528), px=48, d=0.4)
    titulo(R, t_cro - 0.2, 1e9, "CRONOPAPEL", y=380, px=140, d=0.8)
    R.snd(t_cro - 0.2, "escribir", 0.4, dur=0.8)
    pa(R, OC.boton_suscribir(), 960, 690, 1.15, t_sus - 0.1, None, sem=S(), z=6, extra=[(0.05, "brillo", 0.4)])
    R.texto(t_sus + 0.1, 1e9, "SUSCRÍBETE", (960, 690), px=66, d=0.6)
    pa(R, MI(8), 1560, 1015, 1.05, t_xol - 0.3, None, sem=S(), extra=[(0.3, "ladrido", 0.4)])
    R.texto(t_agr - 0.1, 1e9, "¡GRACIAS!", (1560, 560), px=56, d=0.4)
    pa(R, XO(0), 360, 1015, 0.6, t_que, None, sem=S())
