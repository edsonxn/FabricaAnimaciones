# -*- coding: utf-8 -*-
"""Teotihuacán: la ciudad que se quedó sin nombre — 6 minutos, PLANO SECUENCIA estilo Kurzgesagt (sin cortes).
Las 11 "escenas" del guion solo marcan narración y música; todas usan la clase Mundo, que dibuja un único mundo
continuo en función del tiempo global t. Los "planos" (panorama, mapa, conjunto en corte, mito) se enlazan con
portales circulares que crecen desde un punto del plano anterior (nunca hay cortes):
  panorama (noche -> ruinas) -> portal -> mapa (valle, ciudad desde arriba) -> portal -> panorama (pirámides)
  -> portal -> corte de un conjunto habitacional -> portal -> mapa de Mesoamérica (comercio) -> portal -> panorama
  (hueco, túnel, incendio, olvido) -> portal -> mito del Quinto Sol -> portal -> panorama (hoy) -> cierre.
Módulos: anclas (palabras), mundo (panorama), mapa, especiales (corte, mito, portal)."""
import math

import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, lerp, smooth, e_in, e_out, e_inout, e_back, circulo, rect_red
import plano as P
import mundo as M
import mapa as MP
import especiales as E
from anclas import A, INI, FIN, TOTAL

BG = np.zeros((H, W, 3), np.float32)
OSC = (46, 32, 98)
XS = M.X_SOL
LC = MP.lonlat_ciudad


# ======================================================================== utilidades de animación
def K(t, pts, ease=e_inout):
    """Interpolación por claves [(t, v), ...] (v escalar o secuencia)."""
    if t <= pts[0][0]:
        return np.array(pts[0][1], float) if not np.isscalar(pts[0][1]) else pts[0][1]
    for (t0, v0), (t1, v1) in zip(pts[:-1], pts[1:]):
        if t <= t1:
            u = ease(prog(t, t0, t1)) if t1 > t0 else 1.0
            if np.isscalar(v0):
                return v0 + (v1 - v0) * u
            return np.array(v0, float) + (np.array(v1, float) - np.array(v0, float)) * u
    v = pts[-1][1]
    return np.array(v, float) if not np.isscalar(v) else v


def Kcam(t, pts):
    """Claves de cámara [(t, (a, b, z)), ...] con el zoom interpolado en escala logarítmica."""
    q = [(tt, (v[0], v[1], math.log(v[2]))) for tt, v in pts]
    r = K(t, q)
    return float(r[0]), float(r[1]), math.exp(float(r[2]))


def ventana(t, a, b, fi=0.3, fo=0.3):
    return e_out(prog(t, a, a + fi)) * (1 - e_in(prog(t, b - fo, b)))


def pop(t, t0, dur=0.35):
    return 0.0 if t < t0 else e_back(prog(t, t0, t0 + dur))


def etq(lz, t, t0, t1, texto, x, y, px=40, fondo=(255, 255, 255), color=(34, 28, 80)):
    a = ventana(t, t0, t1)
    if a <= 0.01:
        return
    k = max(0.01, pop(t, t0))
    P.pastilla(lz, x, y, texto, px=px, k=k, fondo=fondo, color=color, alfa=min(1.0, a * 1.4))


def gran(lz, t, t0, t1, texto, x, y, px=120, color=(255, 255, 255)):
    a = ventana(t, t0, t1, 0.4, 0.4)
    if a <= 0.01:
        return
    P.rotulo(lz, x, y, texto, px=px, k=max(0.01, pop(t, t0, 0.5)), color=color, alfa=min(1.0, a * 1.3))


def llamada(lz, t, t0, t1, p0, p1):
    a = ventana(t, t0, t1)
    if a > 0.02:
        with lz.capa(2):
            P.linea_llamada(lz, p0, p1, frac=e_out(prog(t, t0, t0 + 0.4)), alfa=a)


# ======================================================================== segmentos y portales
DUR_P = 1.5
PT1 = FIN("intro") - 0.5          # panorama -> mapa (valle)
PT2 = A.sesenta - 0.9             # mapa -> panorama (pirámide del Sol)
PT3 = A.conjuntos - 0.9           # panorama -> conjunto en corte
PT4 = INI("comercio") - 0.3       # corte -> mapa de Mesoamérica
PT5 = INI("tunel") - 0.2          # mapa -> panorama (Ciudadela)
PT6 = A.oscuridad - 0.9           # panorama -> mito
PT7 = FIN("mexicas") - 0.4        # mito -> panorama (amanecer de hoy)

SEG = [(0.0, "pan", None), (PT1, "mapa", (960, 600)), (PT2, "pan", (960, 560)), (PT3, "casa", (760, 640)),
       (PT4, "mapa", (1420, 780)), (PT5, "pan", (960, 560)), (PT6, "mito", (960, 500)), (PT7, "pan", (960, 320))]


# ======================================================================== PANORAMA
def hora_pan(t):
    return float(K(t, [(0, 0.0), (A.cien, 0.9), (A.pir, 2.0), (A.siglos - 0.2, 2.2), (A.ruinas + 1.4, 6.3),
                       (A.esta, 7.0), (PT1 + DUR_P, 7.0), (PT2 - 0.2, 10.0), (INI("gente"), 10.3),
                       (INI("tunel"), 10.6), (A.tormenta, 11.0), (A.arder, 11.2), (FIN("fuego"), 11.5),
                       (INI("silencio"), 11.8), (A.lluvia, 12.0), (A.siglos_s, 16.0), (INI("mexicas"), 17.5),
                       (PT7, 17.0), (A.suben, 17.4), (A.bajo_h, 18.0), (A.enorme, 18.6), (A.misterio, 19.4),
                       (TOTAL - 0.5, 20.0)]))


def est_pan(t):
    h = hora_pan(t)
    hh = h % 4.0
    ruina = float(K(t, [(0, 0.0), (A.siglos, 0.0), (A.ruinas + 1.2, 1.0), (PT1 + DUR_P, 1.0), (PT2 - 0.3, 0.0),
                        (INI("silencio"), 0.0), (A.lluvia, 0.15), (A.maleza + 0.8, 1.0), (PT6, 1.0),
                        (PT7, 0.9), (A.patrim + 1.5, 0.12), (TOTAL, 0.12)]))
    luces = (1.0 - smooth(prog(hh, 0.5, 1.3))) if hh < 2.0 else smooth(prog(hh, 2.6, 3.4))
    est = dict(
        hora=h, ruina=ruina, luces=luces * (1.0 - ruina),
        gente=float(K(t, [(0, 0.35), (A.cien, 0.9), (A.pir, 1.0), (A.siglos - 0.2, 1.0), (A.siglos + 1.0, 0.0),
                          (PT2, 0.0), (INI("gente"), 0.0), (INI("gente") + 0.6, 1.0), (PT3 + DUR_P, 1.0),
                          (PT5, 0.3), (A.tunel - 0.3, 0.3), (A.tunel + 1.0, 0.0), (A.arder - 0.5, 0.0), (A.arder + 0.5, 0.4), (A.destroz, 0.1), (INI("silencio"), 0.2),
                          (A.dispersaron, 0.0), (A.llegaron, 0.0), (A.llegaron + 1.0, 0.3), (PT6, 0.3),
                          (PT7, 0.0)])),
        fuego=float(K(t, [(A.arder - 0.3, 0.0), (A.arder + 1.4, 1.0), (A.varias + 1.5, 1.0),
                          (INI("silencio") + 2.5, 0.0)])),
        estatuas=1.0 if PT2 <= t < PT6 else 0.0,
        rotura=float(K(t, [(A.escult, 0.0), (A.destroz + 1.5, 1.0)])),
        obreros=float(K(t, [(A.animales - 0.4, 0.0), (A.animales + 0.5, 1.0), (INI("gente") - 0.2, 1.0),
                            (INI("gente") + 0.3, 0.0)])),
        turistas=float(K(t, [(A.millon - 0.5, 0.0), (A.millon + 1.4, 1.0), (A.bajo_h, 1.0), (A.bajo_h + 0.8, 0.0)])),
        brazos=float(K(t, [(A.suben, 0.0), (A.luz_h, 1.0), (A.bajo_h - 0.2, 1.0), (A.bajo_h + 0.5, 0.0)])),
        hueco=float(K(t, [(A.hueco - 0.2, 0.0), (A.hueco + 1.2, 1.0)])),
        lluvia=float(K(t, [(INI("tunel", 1) - 0.3, 0.0), (A.tormenta, 1.0), (A.hueco + 1.0, 1.0),
                           (A.tunel - 0.2, 0.3), (A.tunel + 1.0, 0.0)])),
        tunel=float(K(t, [(A.tunel - 0.1, 0.0), (A.camaras + 0.8, 1.0)])),
    )
    return est


def cam_pan(t):
    cam = _cam_pan(t)
    b = ventana(t, A.animales - 0.2, INI("gente") + 0.2, 0.9, 0.6)         # sigue al bloque que arrastran
    if b > 0.001:
        sig = (XS - 1120 + (t * 34) % 900 + 320, -80.0, 1.55)
        cam = (lerp(cam[0], sig[0], b), lerp(cam[1], sig[1], b), math.exp(lerp(math.log(cam[2]), math.log(sig[2]), b)))
    return cam


def _cam_pan(t):
    return Kcam(t, [
        (0.0, (XS - 600, -230, 0.7)), (A.pir, (XS - 100, -230, 0.85)), (A.siglos, (XS - 100, -230, 0.85)),
        (A.ni, (XS, -250, 0.95)), (A.esta, (XS, -240, 0.9)), (PT1 + DUR_P, (XS, -240, 0.9)),
        (PT2, (XS, -230, 0.95)), (PT2 + DUR_P, (XS - 100, -230, 1.0)), (A.animales - 0.5, (XS - 120, -230, 1.0)),
        (A.animales + 0.6, (XS - 700, -110, 0.9)), (INI("gente") - 0.3, (XS - 700, -110, 0.9)),
        (INI("gente") + 0.8, (XS - 200, -150, 0.7)), (PT3 + DUR_P, (XS - 200, -150, 0.7)),
        (PT5, (-1700, -60, 1.5)), (A.tunel, (-1700, -60, 1.5)), (A.tunel + 2.0, (-1690, 50, 4.5)),
        (A.camaras, (-1600, 90, 7.5)), (A.conchas, (-1500, 90, 10.0)), (A.paisaje, (-1500, 90, 13.0)),
        (A.tumba, (-1500, 90, 9.0)), (FIN("tunel") + 0.5, (-1500, 60, 4.0)),
        (INI("fuego") + 2.6, (XS, -250, 0.85)), (A.casas - 0.3, (XS - 300, -250, 0.85)),
        (A.casas + 0.8, (XS - 1700, -70, 1.0)), (A.quien - 0.4, (XS - 1700, -70, 1.0)),
        (A.quien + 0.8, (XS - 300, -250, 0.85)), (INI("silencio"), (XS - 300, -250, 0.85)),
        (A.lluvia, (XS + 300, -200, 0.55)), (A.siglos_s, (XS, -220, 0.6)), (INI("mexicas"), (XS + 400, -220, 0.75)),
        (A.dioses_m - 0.5, (XS + 100, -280, 0.85)), (PT6, (XS, -330, 1.2)),
        (PT7, (XS, -250, 0.8)), (A.suben, (XS, -260, 1.05)), (A.bajo_h - 0.4, (XS, -260, 1.05)),
        (A.bajo_h + 1.6, (-1650, 50, 3.8)), (A.tuneles + 0.6, (-1550, 90, 6.0)), (FIN("hoy") + 0.2, (-1500, 90, 5.0)),
        (INI("cierre"), (-1500, 40, 2.6)), (INI("cierre") + 3.5, (XS - 400, -240, 0.75)),
        (TOTAL, (XS, -300, 0.5)),
    ])


def ui_pan(lz, t, cam):
    cx, cy, z = cam

    def sp(x, y):
        return M.GX + (x - cx) * z, M.GY + (y - cy) * z

    # intro
    if t < PT1 + DUR_P:
        etq(lz, t, A.cien - 0.1, A.pir + 0.4, "+ 100 000 personas", 960, 210, px=46)
        gran(lz, t, A.ni, A.esta + 0.2, "?", 960, 380, px=260)
        gran(lz, t, A.teo, PT1 + 0.9, "TEOTIHUACÁN", 960, 340, px=150)
        gran(lz, t, A.nombre_i - 0.2, PT1 + 0.9, "la ciudad que se quedó sin nombre", 960, 470, px=52)
    # trazo (pirámide del Sol, 65 m)
    if PT2 <= t < PT3:
        a = ventana(t, A.sesenta - 0.2, A.animales - 0.4)
        if a > 0.02:
            x0, y0 = sp(XS + 470, 0)
            x1, y1 = sp(XS + 470, -470)
            with lz.capa(2):
                P.linea_llamada(lz, (x0, y0), (x1, y1), frac=e_out(prog(t, A.sesenta - 0.2, A.sesenta + 0.7)), alfa=a)
            etq(lz, t, A.sesenta, A.animales - 0.4, "65 m", x0 + 90, (y0 + y1) / 2, px=44)
            xp, yp = sp(XS + 560, 14)
            with lz.grupo(xp, yp, 0.7 * z):
                M.persona(lz, 0, 0, 1.0, t, ropa=1, piel=1, seed=4)
        etq(lz, t, A.animales, A.gente_t - 0.2, "sin animales de carga", 960, 250, px=44)
        etq(lz, t, A.gente_t, INI("gente"), "a fuerza de gente", 960, 250, px=44)
    # gente
    if INI("gente") <= t < PT3 + 0.3:
        n = int(100000 * e_out(prog(t, A.cien_g - 0.2, A.cien_g + 2.4)))
        etq(lz, t, INI("gente"), PT3 + 0.3, f"{n:,}".replace(",", " ") + "+", 960, 260, px=120)
    # túnel
    if INI("tunel") <= t < INI("fuego") + 1.0:
        xh, yh = sp(M.X_HUECO, 0)
        gran(lz, t, A.dos2003 - 0.2, A.tunel - 0.2, "2003", 960, 330, px=150)
        etq(lz, t, A.hueco, A.tunel - 0.2, "hundimiento", xh, yh - 110, px=40)
        a = ventana(t, A.cien_u - 0.2, A.camaras + 0.2)
        if a > 0.02:
            xa, ya = sp(M.X_HUECO, M.Y_TUNEL - 24)
            xb, yb = sp(M.CAMARAS[0][0], M.Y_TUNEL - 24)
            ya = min(ya, 760)
            yb = ya
            with lz.capa(2):
                P.linea_llamada(lz, (xa, ya), (xb, yb), frac=e_out(prog(t, A.cien_u - 0.2, A.cien_u + 0.8)), alfa=a)
            etq(lz, t, A.cien_u, A.camaras + 0.2, "casi 100 m", (xa + xb) / 2, ya - 60, px=40)
        etq(lz, t, A.sellado, A.camaras + 0.4, "sellado hace ≈ 1 800 años", 960, 230, px=42)
        for (tt, txt, dx) in ((A.conchas, "conchas", -240), (A.jade, "jade", -20), (A.esferas, "pirita", 200)):
            xc, yc = sp(M.CAMARAS[1][0], M.CAMARAS[1][1] - 26)
            etq(lz, t, tt, A.paisaje - 0.3, txt, xc + dx, yc - 170, px=36)
        xc, yc = sp(M.CAMARAS[1][0], M.CAMARAS[1][1] + 20)
        etq(lz, t, A.mercurio, A.tumba - 0.2, "mercurio líquido", 960, 300, px=44)
        gran(lz, t, A.tumba, A.todavia - 0.1, "¿tumba?", 960, 330, px=120)
        gran(lz, t, A.todavia, FIN("tunel") + 0.6, "aún no aparece", 960, 330, px=80)
    # incendio
    if INI("fuego") <= t < INI("silencio"):
        gran(lz, t, A.quinientos - 0.3, A.calzada_f + 0.2, "≈ año 550", 960, 300, px=120)
        etq(lz, t, A.elite, A.escult - 0.2, "edificios de la élite", 960, 250, px=44)
        etq(lz, t, A.salvaron - 1.0, A.quien - 0.2, "casas comunes: en pie", 960, 250, px=44)
        gran(lz, t, A.quien, A.rebelo - 0.2, "¿quién?", 960, 330, px=140)
        etq(lz, t, A.rebelo - 0.3, A.ataque - 0.2, "revuelta del pueblo", 620, 300, px=44)
        etq(lz, t, A.ataque - 0.2, A.clima - 0.3, "ataque externo", 1300, 300, px=44)
        etq(lz, t, A.clima - 0.2, A.varias - 0.2, "sequía y hambre (535–536)", 960, 300, px=44)
        etq(lz, t, A.varias - 0.1, INI("silencio") - 0.2, "¿todo a la vez?", 960, 300, px=52)
    # silencio
    if INI("silencio") <= t < PT6:
        yr = int(lerp(550, 1300, e_inout(prog(t, A.lluvia - 0.5, A.nombre_s + 1.6))))
        gran(lz, t, A.lluvia - 0.6, INI("mexicas") + 0.5, str(yr), 960, 300, px=150)
        etq(lz, t, A.simbolos, A.lluvia - 0.5, "símbolos", 960, 250, px=44)
        etq(lz, t, A.texto, A.lluvia - 0.5, "ningún texto descifrable", 960, 330, px=44)
        etq(lz, t, INI("mexicas"), A.dioses_m - 0.6, "siglo XIV", 960, 220, px=46)
        etq(lz, t, A.dioses_m - 0.5, PT6 + 0.5, "¿obra de los dioses?", 960, 220, px=46)
    # hoy
    if PT7 + DUR_P <= t < A.bajo_h + 2.5:
        etq(lz, t, A.patrim - 0.2, A.millon - 0.3, "Patrimonio Mundial · UNESCO 1987", 960, 220, px=42)
        n = int(1000000 * e_out(prog(t, A.millon - 0.2, A.millon + 1.6)))
        gran(lz, t, A.millon - 0.3, A.primavera - 0.2, f"{n:,}".replace(",", " ") + "+", 960, 260, px=120)
        etq(lz, t, A.millon - 0.1, A.primavera - 0.2, "visitantes al año", 960, 350, px=42)
        etq(lz, t, A.primavera, A.bajo_h - 0.4, "equinoccio de primavera", 960, 230, px=44)
    if A.bajo_h <= t < FIN("hoy") + 1.5:
        for (tt, txt, xx) in ((A.tuneles, "túneles", 560), (A.murales_h, "murales", 960), (A.tumbas_h, "tumbas", 1360)):
            etq(lz, t, tt, FIN("hoy") + 0.8, txt, xx, 260, px=44)
    # cierre
    if t >= INI("cierre"):
        gran(lz, t, A.enorme, A.fascina - 0.2, "un misterio", 960, 300, px=110)
        gran(lz, t, A.bitacora - 0.1, TOTAL, "BITÁCORA PERDIDA", 960, 420, px=110)
        gran(lz, t, A.bitacora + 0.5, TOTAL, "historias perdidas de México", 960, 520, px=48)


def dib_pan(lz, t):
    cam = cam_pan(t)
    est = est_pan(t)
    M.panorama(lz, t, est, cam)
    ui_pan(lz, t, cam)


# ======================================================================== MAPA
def cam_mapa(t):
    lo, la, z = Kcam(t, [
        (0.0, (-98.98, 19.56, 3.8)),
        (INI("valle"), (-98.98, 19.56, 3.8)), (A.cuenca, (-98.98, 19.56, 3.3)), (A.pobladores - 0.3, (-98.98, 19.56, 3.3)),
        (A.dosmil + 0.5, MP.TEO + (14.0,)), (A.veinte + 0.6, MP.TEO + (45.0,)), (A.dioses_v, MP.TEO + (45.0,)),
        (INI("trazo"), MP.TEO + (45.0,)), (A.cuadr, LC(1, 4) + (60.0,)), (A.calzada, LC(0, 0) + (55.0,)),
        (A.luna - 0.3, LC(0, 6) + (60.0,)), (A.luna + 0.7, LC(0, 21.4) + (300.0,)), (A.luna + 1.9, LC(1, 14) + (110.0,)),
        (A.sol_t - 0.2, LC(1.9, 7) + (120.0,)), (A.sol_t + 0.6, LC(1.9, 7) + (300.0,)), (PT2 + DUR_P, LC(1.9, 7) + (300.0,)),
        (PT4, (-98.9, 19.9, 0.9)), (INI("comercio"), (-95.5, 19.0, 0.40)),
        (A.navajas + 0.5, (-95.5, 19.0, 0.40)), (A.pachuca - 0.3, (-98.8, 19.9, 1.6)),
        (A.mayas - 0.4, (-98.8, 19.9, 1.6)), (A.mayas + 0.8, (-94.5, 18.8, 0.42)), (A.tikal - 0.4, (-94.5, 18.8, 0.42)),
        (A.tikal + 1.2, (-91.8, 18.4, 0.75)), (A.lejos, (-91.8, 18.4, 0.75)), (A.lejos + 1.6, (-95.5, 19.0, 0.40)),
        (PT5 + DUR_P, (-95.5, 19.0, 0.40)),
    ])
    return lo, la, z


def est_mapa(t):
    return dict(
        cdmx=float(K(t, [(A.ciudad_v - 0.2, 0.0), (A.ciudad_v + 0.5, 1.0)])),
        lago_brillo=1 if A.lagos - 0.3 < t < A.montanas else 0,
        rutas=float(K(t, [(A.navajas - 0.3, 0.0), (A.tikal + 1.4, 1.0)])) if t > PT4 - 1 else 0.0,
        ciudad_alfa=float(K(t, [(A.pobladores, 0.0), (A.veinte + 0.4, 1.0)])),
        gente_top=float(K(t, [(A.veinte + 0.5, 0.0), (A.veinte + 2.0, 1.0)])) if t < PT4 - 1 else 0.0,
    )


def ui_mapa(lz, t, cam):
    lo, la, z = cam
    if t < PT2 + DUR_P:
        # valle
        MP.marcador(lz, cam, "teo", "Teotihuacán", alfa=ventana(t, A.cuarenta - 0.3, A.dioses_v - 0.2),
                    dx=0, dy=-56)
        MP.marcador(lz, cam, MP.CDMX, "Ciudad de México (hoy)", alfa=ventana(t, A.ciudad_v - 0.1, A.pobladores - 0.4),
                    dx=0, dy=64, color=(180, 180, 255))
        # línea de 40 km
        a = ventana(t, A.cuarenta - 0.3, A.pobladores - 0.4)
        if a > 0.02:
            x0, y0 = MP.scr(cam, *MP.CDMX)
            x1, y1 = MP.scr(cam, *MP.TEO)
            with lz.capa(2):
                P.linea_llamada(lz, (x0, y0), (x1, y1), frac=e_out(prog(t, A.cuarenta - 0.2, A.cuarenta + 1.0)),
                                col=(255, 255, 255), ancho=4, alfa=a)
            etq(lz, t, A.cuarenta, A.pobladores - 0.4, "≈ 40 km", (x0 + x1) / 2 + 60, (y0 + y1) / 2, px=44)
        xl, yl = MP.scr(cam, -98.99, 19.44)
        etq(lz, t, A.lagos, A.pobladores - 0.4, "lagos", xl, yl, px=44)
        xm, ym = MP.scr(cam, -98.64, 19.2)
        etq(lz, t, A.montanas, A.pobladores - 0.4, "montañas", xm, ym - 60, px=44)
        xt, yt = MP.scr(cam, *MP.TEO)
        etq(lz, t, A.pobladores, A.veinte - 0.2, "hace más de 2 000 años", xt, yt - 130, px=44)
        etq(lz, t, A.veinte, A.mexicas_v - 0.3, "≈ 20 km²", xt, yt - 320, px=54)
        etq(lz, t, A.mexicas_v, A.dioses_v - 0.2, "nombre puesto por los mexicas", 960, 250, px=44)
        etq(lz, t, A.dioses_v - 0.2, A.sabemos - 0.4, "el lugar donde nacieron los dioses", 960, 830, px=58)
        gran(lz, t, A.sabemos, INI("trazo") + 0.6, "?", 960, 380, px=260, color=OSC)
        etq(lz, t, A.sabemos + 0.4, INI("trazo") + 0.6, "nombre original: desconocido", 960, 250, px=44)
        # trazo
        if t >= INI("trazo"):
            etq(lz, t, A.km, A.calzada - 0.2, "≈ 4 km", 960, 250, px=48)
            etq(lz, t, A.calzada, A.tumbas + 0.2, "Calzada de los Muertos", 960, 250, px=46)
            etq(lz, t, A.tumbas, A.templos - 0.1, "¿tumbas?", 960, 330, px=56)
            etq(lz, t, A.templos, A.luna - 0.2, "templos y palacios", 960, 330, px=50)
            etq(lz, t, A.luna, A.sol_t - 0.4, "Pirámide de la Luna", 960, 250, px=46)
            etq(lz, t, A.sol_t - 0.1, PT2 + 0.4, "Pirámide del Sol", 960, 250, px=46)
    # comercio
    if PT4 <= t < PT5 + DUR_P:
        MP.marcador(lz, cam, "teo", "Teotihuacán", alfa=ventana(t, INI("comercio"), PT5), dx=-40, dy=-56)
        MP.marcador(lz, cam, "pachuca", "Pachuca", alfa=ventana(t, A.pachuca - 0.3, A.mayas - 0.4), dx=70, dy=-56,
                    color=(120, 230, 170))
        MP.marcador(lz, cam, "oaxaca", "Oaxaca", alfa=ventana(t, A.navajas + 0.6, PT5 - 0.2), dx=0, dy=-56,
                    color=(255, 214, 96))
        MP.marcador(lz, cam, "golfo", "Golfo", alfa=ventana(t, A.navajas + 0.9, PT5 - 0.2), dx=0, dy=-56,
                    color=(255, 150, 110))
        MP.marcador(lz, cam, "tikal", "Tikal", alfa=ventana(t, A.tikal - 0.2, PT5 - 0.2), dx=0, dy=-56,
                    color=(255, 110, 170))
        etq(lz, t, A.mayas, A.tikal - 0.3, "selvas mayas", 1300, 520, px=44)
        etq(lz, t, A.tikal, A.tres78 - 0.2, "a ≈ 1 000 km", 960, 240, px=46)
        etq(lz, t, A.tres78, A.rey - 0.2, "378", 960, 400, px=170)
        etq(lz, t, A.guerrero, A.rey - 0.2, "un guerrero extranjero", 960, 250, px=46)
        etq(lz, t, A.rey, A.trono, "muere el rey de Tikal", 960, 250, px=46)
        etq(lz, t, A.trono, A.conquista - 0.3, "sube un joven al estilo teotihuacano", 960, 250, px=44)
        etq(lz, t, A.conquista, A.lejos - 0.3, "¿conquista?", 560, 250, px=48)
        etq(lz, t, A.alianza, A.lejos - 0.3, "¿alianza?", 960, 250, px=48)
        etq(lz, t, A.mezcla, A.lejos - 0.3, "¿mezcla?", 1360, 250, px=48)
        etq(lz, t, A.lejos - 0.2, PT5, "influencia a larga distancia", 960, 250, px=44)


def dib_mapa(lz, t):
    cam = cam_mapa(t)
    est = est_mapa(t)
    MP.mapa(lz, t, cam, est)
    ui_mapa(lz, t, cam)
    # dos figuras en Tikal: rey que cae y joven que sube
    if PT4 <= t < PT5 + DUR_P and t > A.guerrero - 0.5:
        x, y = MP.scr(cam, *MP.LUGARES["tikal"])
        with lz.capa(2):
            if t < A.rey + 1.2:
                a = ventana(t, A.guerrero - 0.2, A.rey + 1.2)
                M.persona(lz, x - 90 + 70 * e_out(prog(t, A.guerrero, A.rey)), y + 200, 1.2, t, ropa=1, piel=2,
                          tocado="oro", paso=1.0 if t < A.rey else 0.0, lado=1, seed=7)
            if t > A.trono - 0.2:
                M.persona(lz, x + 60, y + 200, 1.3 * pop(t, A.trono - 0.2), t, ropa=3, piel=1, tocado="plumas", seed=8)


# ======================================================================== CORTE DEL CONJUNTO
def dib_casa(lz, t):
    E.casa_corte(lz, t, dict(casa=prog(t, PT3, PT3 + 1.6)))
    etq(lz, t, A.conjuntos, A.murales - 0.2, "≈ 2 000 conjuntos", 960, 170, px=54)
    etq(lz, t, A.murales, A.extranj - 0.2, "murales", 470, 250, px=46)
    etq(lz, t, A.jaguares, A.extranj - 0.2, "jaguares", 560, 560, px=40)
    etq(lz, t, A.oaxaca - 0.2, A.talleres - 0.2, "barrio de Oaxaca", 1640, 560, px=42)
    etq(lz, t, A.obsidiana, PT4 + 0.6, "obsidiana", 1380, 640, px=44)
    etq(lz, t, A.talleres, PT4 + 0.6, "talleres", 1500, 170, px=50)


# ======================================================================== MITO
def dib_mito(lz, t):
    d = K(t, [(A.rico - 0.2, 0.0), (A.dudo, 0.0), (A.cuatro + 1.4, 4.0)], ease=lambda u: u)
    est = dict(
        alba=float(K(t, [(A.nacio - 0.2, 0.0), (A.nacio + 2.0, 1.0)])),
        llama=float(K(t, [(PT6, 0.15), (A.rico, 0.6), (A.salto, 1.0), (A.salto + 0.8, 1.9), (A.nacio + 1.0, 1.1)])),
        duda=float(d),
        salto=float(K(t, [(A.salto - 0.2, 0.0), (A.salto + 1.4, 1.0)], ease=lambda u: u)),
        sol=float(K(t, [(A.nacio - 0.1, 0.0), (A.nacio + 2.6, 1.0)])),
    )
    E.mito(lz, t, est)
    etq(lz, t, A.rico, A.dudo, "el rico y orgulloso", 560, 300, px=42)
    etq(lz, t, A.pobre - 0.2, A.dudo, "el pobre y enfermo", 1400, 300, px=42)
    gran(lz, t, A.dudo, A.salto - 0.2, "dudó 4 veces", 960, 240, px=90)
    gran(lz, t, A.nacio, FIN("mexicas") + 0.4, "el Quinto Sol", 960, 210, px=100)


# ======================================================================== ensamblado
PLANOS = dict(pan=dib_pan, mapa=dib_mapa, casa=dib_casa, mito=dib_mito)


def render_mundo(lz, t):
    lz.nuevo(t, wob=0.0)
    i = 0
    for k, (t0, _, _) in enumerate(SEG):
        if t >= t0:
            i = k
    t0, nom, cen = SEG[i]
    if i > 0 and t < t0 + DUR_P:
        PLANOS[SEG[i - 1][1]](lz, t)
        u = e_inout(prog(t, t0, t0 + DUR_P))
        with E.portal(lz, cen[0], cen[1], 1.0 + 1500 * u, lerp(1.6, 1.0, u)):
            PLANOS[nom](lz, t)
    else:
        PLANOS[nom](lz, t)
    img = componer(BG, lz.resolver(), boil=lz.boil)
    negro = prog(t, TOTAL - 1.4, TOTAL - 0.1)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


def registrar_sfx(e):
    ev = e.ev
    ev(0.4, "amanecer", 0.35, dur=2.4)
    ev(A.teo, "revelar", 0.45)
    ev(A.ni, "hmm", 0.4)
    for tt in (PT1, PT2, PT3, PT4, PT5, PT6):
        ev(tt, "zoom_whoosh", 0.45, dur=1.4)
    ev(PT7, "amanecer", 0.5, dur=2.0)
    ev(A.ciudad_v, "pop", 0.35, 0.3)
    ev(A.cuarenta, "ding", 0.3)
    ev(A.lagos, "burbujas", 0.25, dur=1.0)
    ev(A.veinte, "brillo", 0.3)
    ev(A.dioses_v, "revelar", 0.4)
    ev(A.sabemos, "hmm", 0.4)
    ev(A.km, "tick", 0.3)
    ev(A.luna, "pop", 0.35, -0.2)
    ev(A.sol_t, "pop", 0.35, 0.2)
    ev(A.sesenta, "ding", 0.35)
    ev(A.animales, "pasos", 0.25, dur=2.0)
    ev(A.cien_g, "brillo", 0.3)
    ev(A.conjuntos, "pop", 0.3)
    ev(A.murales, "pincel", 0.3)
    ev(A.obsidiana, "clink", 0.35)
    for tt in (A.pachuca, A.tikal):
        ev(tt, "pop", 0.35)
    ev(A.tres78, "impacto", 0.4)
    ev(A.rey, "golpe_suave", 0.4)
    ev(A.trono, "bling", 0.3)
    for tt in (A.conquista, A.alianza, A.mezcla):
        ev(tt, "pop", 0.3, tono=1.1)
    ev(A.tormenta, "viento", 0.3, dur=2.2)
    ev(A.hueco, "golpe_suave", 0.5)
    ev(A.tunel, "eco", 0.35)
    ev(A.camaras, "brillo", 0.35)
    ev(A.mercurio, "bling", 0.3)
    ev(A.tumba, "hmm", 0.4)
    ev(A.arder, "fuego", 0.5, dur=8.0)
    ev(A.escult, "impacto", 0.4)
    ev(A.destroz, "golpe_suave", 0.4)
    ev(A.quien, "hmm", 0.4)
    ev(INI("silencio"), "suspiro", 0.5, dur=2.0)
    ev(A.lluvia, "viento", 0.3, dur=3.0)
    ev(A.dioses_m, "revelar", 0.35)
    ev(A.dudo, "tick", 0.3)
    ev(A.salto, "whoosh", 0.5)
    ev(A.salto + 1.0, "brillo", 0.5)
    ev(A.nacio, "amanecer", 0.6, dur=2.6)
    ev(A.patrim, "ding", 0.35)
    ev(A.millon, "pop", 0.35)
    ev(A.bajo_h, "zoom_whoosh", 0.4, dur=1.4)
    ev(A.bitacora, "bling", 0.4)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
