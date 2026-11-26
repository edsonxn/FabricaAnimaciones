# -*- coding: utf-8 -*-
"""Coreografía (2/4) de «Toda la historia de los AZTECAS»: chinampas (cómo se hacen, ahuejotes, cosechas, Xochimilco hoy, vasallos
de Azcapotzalco y Tezozómoc, Acamapichtli, Xolo cuida patos), la Triple Alianza (Maxtla, Itzcóatl, Nezahualcóyotl en el árbol,
1428, las tres ciudades, la quema de libros, Tlacaélel, el billete de 100), Moctezuma Ilhuicamina (la flecha, la expansión por
etapas, heladas y hambruna, Xolo bajo el petate, acueducto y albarradón, la guerra florida con Tlaxcala) y la vida diaria
(macehuales y pipiltin, telpochcalli y calmécac, el humo de chile, mantas y cacao, falsificadores, el mercado de Tlatelolco y
Xolo «sin contacto visual» junto a la canasta de perritos).
Dibujos = pegatinas de Flow (`pegflow.P`), fotos reales = `foto_peg.FotoPeg`. Semillas 300-599.
Capas de terreno: 10 = imperio (Triple Alianza → 1469), 11 = Tlaxcala; la 50 (agua que tapa la isla de 1325) se encoge aquí:
las chinampas hacen crecer la isla. Fondo propio: parcelas de chinampa en la isla (rejilla «cuenca»), mancha tepaneca, helada,
albarradón y calzadas."""
import math

import cv2
import numpy as np

import boceto as B
import foto_peg as FP
import mapa as M
import obj_a as A
import obj_base as OB
from core import FIN, INI, T
from coreo_peg import andar_ciclo, ciclo_pant, grupo_ciclo
from coreo_util import CI, COL, ga, lugar, pa, titulo
from motor import H, W, e_in, e_inout, e_out, prog
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (números de piezas/<hoja>/_indice.jpg)
XO = lambda n, **k: P("01_xolo_hoja", n, **k)         # 0 sentado, 1 camina, 2 asustado, 3 bajo el petate, 4 aúlla, 5 salta, 6 duerme, 7 de reojo
XM = lambda n, **k: P("18_mictlan_hoja", n, **k)      # 4 Xolo con patos en la chinampa, 5 Xolo nervioso, 6 olla de barro
CH = lambda n, **k: P("05_chinampas_hoja", n, **k)    # 0 estacas, 1 cerca de carrizo, 2 chinampa, 3 ahuejote, 4 trajinera, 5 Tezozómoc, 6 Acamapichtli, 7 mercenario
AL = lambda n, **k: P("06_alianza_hoja", n, **k)      # 0 Itzcóatl, 1 árbol con el príncipe, 2 Nezahualcóyotl, 3 Maxtla, 4 libros ardiendo, 5 Tlacaélel, 6 águila, 7 jaguar
MO = lambda n, **k: P("07_moctezuma1_hoja", n, **k)   # 0 Moctezuma flecha, 1 milpa helada, 2 familia, 3 canasta vacía, 4 acueducto, 5 dique, 6 tlaxcalteca, 7 prisionero, 8-10 guerreros
VI = lambda n, **k: P("08_vida_hoja", n, **k)         # 0 macehual, 1 milpa, 2 noble, 3 leña, 4 barre, 5 pirámide, 6 sacerdote, 7 alumno, 8 padre, 9 chile, 10 cacao, 11 mazorca, 12 mantas, 13 falsificador
ME = lambda n, **k: P("09_mercado_hoja", n, **k)      # 0 puesto, 1 guajolotera, 2 guajolote, 3 pochteca, 4 yerbera, 5 perritos, 6 gente, 7 tlacuilo, 8 tortillera
C_XOLO = ciclo("19_xolo_corre")
C_MEX = ciclo("20_mexica_camina")
C_CAN = ciclo("21_canoa_ciclo")
C_GUE = ciclo("23_guerrero_corre")

_SEM = iter(range(300, 600))


def S(n=1):
    """Semilla de temblor del rango 300-599 (n seguidas para grupos)."""
    v = next(_SEM)
    for _ in range(n - 1):
        next(_SEM)
    return v


_ULT = [None]


def anio(R, t, v, hold=0.5):
    """Año grande con espera (el contador no cuenta despacio entre dos años lejanos)."""
    if _ULT[0] is not None and _ULT[0] != v:
        R.anio(t - hold, _ULT[0])
    R.anio(t, v)
    _ULT[0] = v


class Crece:
    """Envuelve una pegatina y la hace crecer (o encoger) de s0 a s1 entre t0 y t1."""

    def __init__(self, p, t0, t1, s0=0.3, s1=1.0):
        self.p, self.t0, self.t1, self.s0, self.s1 = p, t0, t1, s0, s1
        self.alto = getattr(p, "alto", 400.0)
        self.total = 1.0

    def dibujar(self, hoja, x, y, s=1.0, *a, **k):
        tv = k.get("tv")
        g = 1.0 if tv is None else self.s0 + (self.s1 - self.s0) * e_inout(prog(tv, self.t0, self.t1))
        self.p.dibujar(hoja, x, y, s * g, *a, **k)


def tachar(R, t0, t1, txt, pos, px, sem=0):
    """Raya de tinta que tacha un rótulo de pantalla."""
    w = B.ancho_texto(txt, px)
    x, y = pos
    Pt = np.stack([np.linspace(x - w / 2 - 16, x + w / 2 + 16, 14), np.linspace(y - 0.1 * px + 8, y - 0.1 * px - 6, 14)], 1)

    def f(h, cam, t, fs, te):
        if t < t0 or t > t1 + 0.3:
            return
        u = prog(t, t0, t0 + 0.35)
        v = int(255 * (1 - prog(t, t1, t1 + 0.3)))
        if v > 0:
            h.trazo(Pt, 8.0, 340 + sem, fs, u, amp=1.6, v=v)
    R.frente.append(R._acot(f, t0))
    R.snd(t0, "escribir", 0.32, dur=0.4)


def foto(R, clave, x, y, frac, t0, t1, sem=None, **kw):
    if clave not in FP.creditos():
        return None
    return pa(R, FP.F(clave), x, y, FP.s_para(frac), t0, t1, entra="pluma", sem=S() if sem is None else sem, z=4, **kw)


def viaja(R, dib, P_, t0, dur, t1, s=0.3, zs=0.4, z=2):
    """Pegatina que viaja por un camino geográfico (tributo que va de una ciudad a otra)."""
    return R.act(dib, pos_geo=R.camino_pos(P_, t0, dur), s=s, t_in=t0, d_in=0.3, entra="pop", sem=S(), t_out=t1, sale="encoger",
                 zs=zs, z=z)


def billete():
    """Billete de 100 pesos (serie vieja, rojizo) dibujado por código: marco, óvalo del retrato y guardas."""
    ops = OB.forma(OB.rect(-190, -210, 190, 0, r=14), (214, 124, 106), 5.5, peso=0.4, sp=9)
    ops += OB.forma(OB.rect(-168, -190, 168, -20, r=10), None, 3.5, peso=0.2)
    ops += OB.elipse(70, -105, 62, 74, OB.CREMA, 4.5, peso=0.25)
    ops += [OB.rayita(-150, -60, -40, -60, 3.5), OB.rayita(-150, -42, -70, -42, 3.5)]
    return OB.Dib(ops)


# ------------------------------------------------------------------ capas de fondo propias
_XY = []


def _malla():
    if not _XY:
        ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
        _XY.extend([xs, ys])
    return _XY


def _env(t, a, b, c, d):
    return e_out(prog(t, a, b)) * (1 - e_in(prog(t, c, d)))


def _fondo_tepanecas(R, t0, t1):
    """Mancha azul del dominio tepaneca: nace en Azcapotzalco y cubre el valle (sin campo «tepanecas» aún); se encoge al caer."""
    lon0, lat0 = CI["azcapotzalco"]
    R0 = 0.34

    def f(img, cam, t, fs):
        k = _env(t, t0, t0 + 1.4, t1, t1 + 1.6)
        if k <= 0.01:
            return
        x0, y0 = cam.pant(lon0, lat0)
        x1, y1 = cam.pant(lon0 + R0 * k, lat0 - R0 * 0.8 * k)
        rx, ry = abs(x1 - x0) + 1e-3, abs(y1 - y0) + 1e-3
        if rx < 3:
            return
        xs, ys = _malla()
        Sd = (np.hypot((xs - x0) / rx, (ys - y0) / ry) - 1.0) * np.float32(min(rx, ry))
        alfa = 0.54 - 0.28 * min(1.0, max(0.0, (cam.z - 3.0) / 9.0))
        M.pintar(img, Sd, COL["tepanecas"], alfa, fs, borde=0.8, sombra=0.1)
    R.fondo.append(("mx", f))


def _fondo_helada(R, t0, t1):
    hielo = np.array([0.86, 0.92, 0.97], np.float32)

    def f(img, cam, t, fs):
        a = 0.34 * _env(t, t0, t0 + 0.9, t1, t1 + 1.0)
        if a > 0.005:
            img *= (1 - a)
            img += hielo * a
    R.fondo.append(("mx", f))


def _fondo_obras(R, t_dique, t_fin):
    """Albarradón de Nezahualcóyotl (se construye entre t_dique y +2 s) y, desde la vida diaria, las calzadas de la isla."""
    t_calz = INI("vida") - 0.3

    def f(img, cam, t, fs):
        if t < t_dique or t > t_fin + 0.5 or cam.z < 3.5:
            return
        k = 1 - prog(t, t_fin, t_fin + 0.5)
        u = prog(t, t_dique, t_dique + 2.0)
        M.pintar_calzadas(img, cam, claves=("albarradon",), alfa=k, u=u, ancho_m=max(100.0, 2400.0 / cam.z), albarradon=u >= 1)
        if t >= t_calz:
            M.pintar_calzadas(img, cam, claves=("calzada_tepeyac", "calzada_tlacopan", "calzada_iztapalapa", "calzada_coyoacan"),
                              alfa=k * prog(t, t_calz, t_calz + 0.6), ancho_m=70.0, albarradon=False)
    R.fondo.append(("mx", f))


def _chinampas_parcelas(t_ini, t_crece, t_fin):
    """Parcelas de chinampa (rectángulos verdes con canales) donde la isla de 1519 aún era agua en 1325: aparecen de la orilla del
    islote hacia afuera entre t_ini y t_crece (la isla crece) y se quedan hasta t_fin. Solo se ven de cerca (z > 7)."""
    rc = M.REJ_CUENCA
    if "isla_1519" not in rc.campos:
        return None

    def val(k, lon, lat):
        c = rc.campos.get(k)
        if c is None:
            return np.full(np.shape(lon), 1e3)
        x, y = rc.proj(np.asarray(lon), np.asarray(lat))
        xi = np.clip(np.rint(x).astype(int), 0, c.shape[1] - 1)
        yi = np.clip(np.rint(y).astype(int), 0, c.shape[0] - 1)
        return c[yi, xi].astype(np.float64) / M.ESC_I16

    dl, dla = 0.00220, 0.00085
    lon, lat = np.meshgrid(np.arange(-99.175, -99.10, dl), np.arange(19.395, 19.47, dla))
    lon = lon + (np.arange(lon.shape[0])[:, None] % 2) * dl * 0.5        # hileras en tresbolillo
    lon, lat = lon.ravel(), lat.ravel()
    a = val("isla_1519", lon, lat)
    d = np.minimum(val("islote_1325", lon, lat), val("islote_tlatelolco", lon, lat))
    m = (a < -0.6) & (d > 0.8)
    lon, lat, d = lon[m], lat[m], d[m]
    if not len(lon):
        return None
    rng = np.random.default_rng(321)
    q = np.argsort(np.argsort(d + rng.uniform(0, 6, len(d)))) / max(1, len(d) - 1)
    tk = t_ini + (t_crece - t_ini) * q ** 0.85
    ang = -0.10
    hw, hh = dl * 0.42, dla * 0.37
    base = np.array([(-hw, -hh), (hw, -hh), (hw, hh), (-hw, hh)])
    rot = np.array([[math.cos(ang), -math.sin(ang)], [math.sin(ang), math.cos(ang)]])
    base = base @ rot.T
    verdes = [(0.48, 0.64, 0.33), (0.56, 0.70, 0.38), (0.42, 0.58, 0.30), (0.62, 0.68, 0.36)]
    grupo = rng.integers(0, len(verdes), len(lon))
    tinta = (0.30, 0.27, 0.22)

    def f(img, cam, t, fs):
        if t < t_ini or t > t_fin + 0.7 or cam.z < 7:
            return
        u = np.clip((t - tk) / 0.5, 0, 1)
        if t > t_fin:
            u = u * (1 - prog(t, t_fin, t_fin + 0.7))
        vis = u > 0.02
        if not vis.any():
            return
        uv = u[vis]
        uu = (1 - (1 - uv) ** 3)[:, None, None]
        C = np.stack([lon[vis], lat[vis]], 1)[:, None, :] + base[None] * uu
        Q = cam.pant_pts(C.reshape(-1, 2)).reshape(-1, 4, 2)
        dentro = (Q[:, :, 0].max(1) > -20) & (Q[:, :, 0].min(1) < W + 20) & (Q[:, :, 1].max(1) > -20) & (Q[:, :, 1].min(1) < H + 20)
        if not dentro.any():
            return
        Qi = np.rint(Q * 8).astype(np.int32)
        g = grupo[vis]
        for j, col in enumerate(verdes):
            sel = dentro & (g == j)
            if sel.any():
                cv2.fillPoly(img, list(Qi[sel]), col, cv2.LINE_AA, 3)
        grosor = 1
        cv2.polylines(img, list(Qi[dentro]), True, tinta, grosor, cv2.LINE_AA, 3)
    return f


def cortes(R):
    pass


def construir(R):
    t_fin = FIN("vida")
    f = _chinampas_parcelas(T("chinampas", "chinampas", frase=0), T("chinampas", "chile", frase=3), t_fin)
    if f is not None:
        R.fondo.append(("mx", f))
    _agua_isla(R)
    _fondo_tepanecas(R, T("chinampas", "azcapotzalco", frase=5), T("alianza", "derrotaron", frase=3))
    _fondo_helada(R, T("moctezuma1", "heladas", frase=2) - 0.3, T("moctezuma1", "xolo", frase=4) - 0.5)
    _fondo_obras(R, T("moctezuma1", "dique", frase=6), t_fin)
    _chinampas(R)
    _alianza(R)
    _moctezuma1(R)
    _vida(R)


def _agua_isla(R):
    """Capa 50 (agua que tapa lo que la isla aún no era): con las chinampas se encoge y la isla crece hasta la de 1519."""
    if "agua_isla_1325" not in M.CAMPOS:
        return
    i0 = INI("chinampas")
    k = sorted(R.terr.get(("mx", 50), []), key=lambda c: c["t"])
    prev = [c for c in k if c["t"] <= i0]
    if any(c["t"] > i0 for c in k):
        return                                   # otro tramo ya la controla
    if prev and prev[-1]["campo"] is None:
        if prev[-1]["t"] < i0 - 3.0:
            return                               # retirada hace mucho: no la resucito
        # coreo_1 la retira al salir (limpieza): la dejo puesta para que las chinampas hagan crecer la isla en esta escena
        R.terreno(prev[-1]["t"] + 0.01, "agua_isla_1325", COL["agua_isla_1325"], 0.01, capa=50)
    elif not prev:
        R.terreno(i0 - 0.5, "agua_isla_1325", COL["agua_isla_1325"], 0.01, capa=50)
    R.terreno(T("chinampas", "chinampas", frase=0), None, COL["agua_isla_1325"], 26.0, capa=50)


# ------------------------------------------------------------------ CHINAMPAS
def _chinampas(R):
    e = "chinampas"
    i0, fin = INI(e), FIN(e)

    def w(p, i, **k):
        return T(e, p, frase=i, **k)
    t_chi = w("chinampas", 0)
    t_est, t_cer, t_lod, t_sem = w("estacas", 1), w("cercas", 1), w("lodo", 1), w("sembraban", 1)
    t_ahu, t_rai = w("ahuejotes", 2), w("raices", 2)
    t_isl, t_cos, t_mai, t_fri, t_cal, t_chl = w("islas", 3), w("cosechas", 3), w("maiz", 3), w("frijol", 3), w("calabaza", 3), w("chile", 3)
    t_exi, t_xoc, t_tra, t_pat = w("existen", 4), w("xochimilco", 4), w("trajinera", 4), w("patrimonio", 4)
    t_vas, t_azc, t_tep, t_tez, t_ast = w("vasalla", 5), w("azcapotzalco", 5), w("tepanecas", 5), w("tezozomoc", 5), w("astuto", 5)
    t_tri, t_gue, t_apr = w("tributo", 6), w("guerras", 6), w("aprendian", 6)
    t_1376, t_tla, t_hab, t_aca, t_cul = w("1376", 7), w("tlatoani", 7), w("habla", 7), w("acamapichtli", 7), w("culhuacan", 7)
    t_xo, t_trab, t_pato = w("xolo", 8), w("trabajo", 8), w("patos", 8)

    # cámara: la isla de cerca (las chinampas crecen) → Xochimilco → el valle (Azcapotzalco) → Culhuacán-isla → la isla
    for tc, lon, lat, z in ((i0 - 0.2, -99.138, 19.431, 18), (299.5, -99.137, 19.433, 28), (302.0, -99.136, 19.434, 36),
                            (304.5, -99.134, 19.436, 41), (307.0, -99.132, 19.437, 43), (309.5, -99.136, 19.433, 40),
                            (312.0, -99.140, 19.431, 36), (315.0, -99.137, 19.436, 34), (318.0, -99.134, 19.438, 38),
                            (321.0, -99.133, 19.434, 42), (t_chl + 0.2, -99.128, 19.412, 30), (t_xoc - 0.4, -99.108, 19.30, 15),
                            (t_tra - 0.2, -99.100, 19.262, 24), (330.0, -99.098, 19.257, 27), (t_vas - 0.3, -99.10, 19.28, 20),
                            (t_azc - 1.2, -99.08, 19.44, 6.6), (t_tez - 0.4, -99.10, 19.46, 7.2), (t_ast + 0.6, -99.12, 19.47, 7.6),
                            (t_tri, -99.13, 19.47, 7.3), (t_gue + 0.2, -99.16, 19.48, 7.9), (t_apr + 0.5, -99.14, 19.44, 9.0),
                            (t_1376 + 1.4, -99.12, 19.395, 11.0), (t_aca - 0.4, -99.12, 19.39, 12.0), (t_cul - 0.6, -99.115, 19.382, 12.6),
                            (t_xo - 0.1, -99.13, 19.42, 22), (361.5, -99.135, 19.431, 32), (363.5, -99.136, 19.433, 37),
                            (fin - 0.25, -99.135, 19.434, 40)):
        R.camara(tc, lon, lat, z)

    anio(R, i0 + 0.3, 1340)
    # frase 0: hambre → chinampas (Xolo mira la olla: a un paso del menú)
    pa(R, XM(5), 320, 1000, 0.62, i0, t_chi + 0.4, sem=S(), extra=[(0.3, "gemido_perro", 0.3)])
    pa(R, XM(6), 560, 1000, 0.42, i0 + 0.5, t_chi + 0.4, sem=S(), entra="sube", dy=300)
    R.texto(i0 + 0.7, t_chi - 0.3, "¿Y QUÉ COMEMOS?", (440, 520), px=48, d=0.5)
    ciclo_pant(R, C_CAN, 2050, 1250, 1010, i0 + 0.2, 4.2, t1=t_chi + 0.6, s=0.55, sem=S())
    titulo(R, t_chi - 0.1, t_sem + 1.0, "CHINAMPAS", px=100, snd=True)
    R.texto(t_chi + 0.3, t_est - 0.2, "jardines sobre el lago", (960, 312), px=54, d=0.6)
    pa(R, CH(2), 1520, 1000, 0.85, t_chi + 0.2, t_ahu - 0.3, sem=S(), entra="sube", dy=320, extra=[(0.05, "crece", 0.35)])

    # frase 1: estacas → cerca de carrizo → lodo y plantas → a sembrar
    pa(R, CH(0), 330, 1000, 0.95, t_est - 0.2, t_ahu - 0.3, sem=S(), extra=[(0.1, "golpe_suave", 0.3), (0.5, "golpe_suave", 0.25)])
    R.texto(t_est, t_ahu - 0.4, "1. ESTACAS", (330, 560), px=44, d=0.35)
    pa(R, CH(1), 900, 1000, 0.80, t_cer - 0.2, t_ahu - 0.3, sem=S(), extra=[(0.05, "papel", 0.3)])
    R.texto(t_cer, t_ahu - 0.4, "2. CERCA DE CARRIZO", (900, 560), px=44, d=0.45)
    R.texto(t_lod - 0.1, t_ahu - 0.4, "3. LODO Y PLANTAS", (900, 625), px=40, d=0.45)
    R.snd(t_lod, "agua_lago", 0.3, dur=1.2)
    R.texto(t_sem - 0.1, t_ahu - 0.4, "4. ¡A SEMBRAR!", (1520, 560), px=44, d=0.4)

    # frase 2: ahuejotes en las orillas de las chinampas
    pa(R, CH(3), 300, 1010, 1.25, t_ahu - 0.25, t_isl - 0.2, sem=S(), entra="sube", dy=420, extra=[(0.05, "crece", 0.3)])
    R.texto(t_ahu + 0.1, t_isl - 0.3, "AHUEJOTES", (300, 450), px=52, d=0.4)
    for k, geo in enumerate(((-99.143, 19.428), (-99.127, 19.429), (-99.146, 19.441), (-99.124, 19.442), (-99.136, 19.448))):
        ga(R, CH(3), geo, t_ahu + 0.2 + 0.22 * k, t_isl + 2.0, s=0.30, sem=S(), zs=0.3, z=1, entra="sube", dy=160)
    R.texto(t_rai - 0.1, t_isl - 0.3, "sus raíces amarran la tierra", (960, 196), px=60, d=0.6)
    foto(R, "chinampas_xochimilco", 1460, 960, 0.44, t_ahu + 0.4, t_isl - 0.1)
    pa(R, XO(1), 620, 1010, 0.42, t_ahu + 1.0, t_isl - 0.2, sem=S())

    # frase 3: islas de cultivo, varias cosechas al año
    pa(R, CH(2), 760, 1010, 1.05, t_isl - 0.1, t_exi + 0.3, sem=S(), entra="sube", dy=360, extra=[(0.05, "crece", 0.35)])
    titulo(R, t_cos - 0.1, t_exi + 0.2, "VARIAS COSECHAS AL AÑO", px=78)
    pa(R, VI(1), 280, 1010, 0.95, t_mai - 0.15, t_exi + 0.3, sem=S())
    for k, (txt, tt) in enumerate((("MAÍZ", t_mai), ("FRIJOL", t_fri), ("CALABAZA", t_cal), ("CHILE", t_chl))):
        R.texto(tt - 0.05, t_exi + 0.2, txt, (1500, 440 + 92 * k), px=56, d=0.3)
        R.snd(tt, "pop", 0.3, tono=1.0 + 0.1 * k)
    pa(R, XO(5), 1720, 1010, 0.5, t_cos, t_exi + 0.3, sem=S(), extra=[(0.1, "ladrido", 0.25)])
    ciclo_pant(R, C_CAN, -250, 2100, 1060, t_isl + 0.3, 6.5, t1=t_exi + 0.2, s=0.45, sem=S(), z=1)

    # frase 4: Xochimilco hoy: trajinera, patrimonio
    foto(R, "chinampas_canal", 470, 960, 0.46, t_exi - 0.1, t_vas - 0.3)
    R.ciudad(t_xoc - 0.1, t_vas - 0.4, "xochimilco", CI["xochimilco"], "XOCHIMILCO", "arriba", 44)
    titulo(R, t_xoc, t_vas - 0.3, "HOY: SE PUEDE VISITAR", px=70)
    pa(R, CH(4), 1460, 1010, 1.0, t_tra - 0.2, t_vas - 0.2, sem=S(), entra="der", dx=700, extra=[(0.05, "trajinera", 0.4)])
    pa(R, XO(0), 1360, 905, 0.36, t_tra + 0.5, t_vas - 0.2, sem=S(), z=3)
    R.texto(t_pat - 0.1, t_vas - 0.3, "PATRIMONIO DE LA HUMANIDAD (UNESCO, 1987)", (960, 300), px=44, d=0.8)

    # frase 5: vasalla de Azcapotzalco, de los tepanecas; Tezozómoc
    anio(R, t_vas, 1370)
    pa(R, XO(2), 320, 1000, 0.55, t_vas - 0.3, t_tri - 0.2, sem=S(), extra=[(0.2, "gemido_perro", 0.25)])
    titulo(R, t_vas - 0.1, t_tep - 0.2, "PERO... VASALLA", px=84, snd=True)
    R.ciudad(t_vas, fin, "tenochtitlan", CI["tenochtitlan"], "TENOCHTITLAN", "der", 38)
    R.ciudad(t_azc - 0.1, t_1376, "azcapotzalco", CI["azcapotzalco"], "AZCAPOTZALCO", "izq", 40, sfx=True)
    lugar(R, t_tep, t_apr + 0.3, "TEPANECAS", (-99.24, 19.56), off=(0, 0), px=56)
    pa(R, CH(5), 1600, 1000, 1.05, t_tez - 0.2, t_1376 - 0.2, sem=S(), entra="sube", dy=320, extra=[(0.05, "tambor", 0.25)])
    R.texto(t_tez, t_1376 - 0.3, "TEZOZÓMOC", (1600, 560), px=48, d=0.4)
    R.texto(t_ast - 0.3, t_tri - 0.1, "viejo y astuto", (1600, 490), px=40, d=0.4)
    titulo(R, t_tez - 0.4, t_apr + 0.6, "EL DUEÑO DEL VALLE", px=70)

    # frase 6: tributo y guerras para Azcapotzalco… y aprendían
    Pt = [CI["tenochtitlan"], (-99.16, 19.465), CI["azcapotzalco"]]
    R.ruta(Pt, t_tri - 0.2, 1.2, ancho=4.0, flecha=True, t1=t_apr + 0.8)
    viaja(R, VI(12), Pt, t_tri, 2.2, t_tri + 2.6, s=0.22)
    viaja(R, VI(10), Pt, t_tri + 0.5, 2.2, t_tri + 3.0, s=0.18)
    R.snd(t_tri, "monedas", 0.3)
    pa(R, CH(7), 330, 1000, 1.0, t_gue - 0.6, t_1376 - 0.2, sem=S(), extra=[(0.05, "tambor", 0.3)])
    R.texto(t_gue - 0.4, t_1376 - 0.3, "MERCENARIOS", (330, 560), px=44, d=0.4)
    grupo_ciclo(R, C_GUE, [CI["azcapotzalco"], (-99.27, 19.50), (-99.36, 19.49)], t_gue - 0.3, 3.0, n=3, ancho=60, t1=t_apr + 0.6,
                s=0.26, sem=S(3), extra=[(0.05, "batalla", 0.25, {"dur": 1.4})])
    R.texto(t_apr - 0.1, t_1376 - 0.3, "...Y APRENDÍAN", (960, 300), px=58, d=0.5)
    pa(R, XO(7), 640, 1010, 0.45, t_apr - 0.3, t_1376 + 0.3, sem=S())

    # frase 7: 1376, primer tlatoani: Acamapichtli, de Culhuacán
    anio(R, t_1376, 1376)
    titulo(R, t_tla - 0.1, t_xo - 0.3, "PRIMER TLATOANI", px=84, snd=True)
    R.texto(t_hab - 0.6, t_xo - 0.3, "«el que habla»", (330, 480), px=46, d=0.5)
    pa(R, CH(6), 330, 1000, 1.05, t_1376 + 1.0, t_xo - 0.2, sem=S(), entra="sube", dy=320, extra=[(0.05, "fanfarria", 0.25)])
    R.texto(t_aca, t_xo - 0.3, "ACAMAPICHTLI", (330, 560), px=48, d=0.5)
    foto(R, "acamapichtli_tovar", 1470, 960, 0.46, t_tla - 0.2, t_cul - 0.6)
    R.ciudad(t_cul - 0.4, t_xo - 0.2, "culhuacan", CI["culhuacan"], "CULHUACÁN", "der", 40, sfx=True)
    R.ruta([CI["culhuacan"], (-99.12, 19.39), CI["tenochtitlan"]], t_cul - 0.2, 1.3, ancho=4.0, flecha=True, t1=fin - 0.5)
    R.texto(t_cul + 0.5, t_xo - 0.3, "sangre noble", (960, 380), px=44, d=0.4)
    foto(R, "mendoza_acamapichtli", 1500, 960, 0.48, t_cul - 0.4, t_pato - 0.4)
    pa(R, XO(0), 600, 1010, 0.42, t_1376 + 0.3, t_xo - 0.2, sem=S())

    # frase 8: Xolo cuida los patos de la chinampa
    pa(R, XM(4), 760, 1010, 1.25, t_xo - 0.15, fin + 0.3, sem=S(), entra="sube", dy=380, extra=[(0.1, "ladrido", 0.35)])
    titulo(R, t_trab - 0.1, fin + 0.2, "SU PRIMER TRABAJO SERIO", px=74, snd=True)
    R.texto(t_pato - 0.6, fin + 0.2, "cuidar patos", (760, 470), px=54, d=0.4)
    R.snd(t_pato, "patos", 0.4)
    andar_ciclo(R, C_XOLO, [(-99.150, 19.424), (-99.142, 19.428), (-99.132, 19.430)], t_xo + 0.3, 2.6, t1=fin + 0.3, s=0.16,
                sem=S(), zs=0.4)
    ciclo_pant(R, C_CAN, 2050, 1350, 1040, t_trab, 3.8, t1=fin + 0.3, s=0.5, sem=S(), z=1)


# ------------------------------------------------------------------ TRIPLE ALIANZA
def _alianza(R):
    e = "alianza"
    i0, fin = INI(e), FIN(e)

    def w(p, i, **k):
        return T(e, p, frase=i, **k)
    t_1426, t_mur, t_tez, t_max, t_apr = w("1426", 0), w("murio", 0), w("tezozomoc", 0), w("maxtla", 0), w("apretar", 0)
    t_itz, t_ali, t_pri, t_huy, t_nez, t_tex = (w("itzcoatl", 1), w("aliaron", 1), w("principe", 1), w("huyendo", 1),
                                                w("nezahualcoyotl", 1), w("texcoco", 1))
    t_ley, t_muc, t_arb, t_tep, t_pad = w("leyenda", 2), w("muchacho", 2), w("arbol", 2), w("tepanecas", 2), w("padre", 2)
    t_1428, t_mex, t_txc, t_tlc, t_der, t_azc = (w("1428", 3), w("mexicas", 3), w("texcocanos", 3), w("tlacopan", 3), w("derrotaron", 3),
                                                 w("azcapotzalco", 3))
    t_tri, t_tres, t_trib, t_med, t_man, t_ten = (w("triple", 4), w("tres", 4), w("tributo", 4), w("medio", 4), w("mandaba", 4),
                                                  w("tenochtitlan", 4))
    t_itz2, t_mod, t_que, t_lib = w("itzcoatl", 5), w("moderno", 5), w("quemar", 5), w("libros", 5)
    t_cod, t_don, t_his, t_ele, t_sol = w("codices", 6), w("don", 6), w("historia", 6), w("elegido", 6), w("sol", 6)
    t_con, t_var, t_tlc2 = w("consejero", 7), w("varios", 7), w("tlacaelel", 7)
    t_nez2, t_rey, t_cons, t_poe, t_bil, t_cien = (w("nezahualcoyotl", 8), w("rey", 8), w("constructor", 8), w("poeta", 8),
                                                   w("billetes", 8), w("cien", 8))

    for tc, lon, lat, z in ((i0 - 0.2, -99.10, 19.47, 7.2), (369.0, -99.12, 19.48, 7.6), (371.5, -99.15, 19.49, 8.0),
                            (374.0, -99.08, 19.47, 7.0), (376.5, -99.03, 19.48, 6.6), (379.5, -98.96, 19.50, 6.8),
                            (382.0, -98.92, 19.51, 7.2), (384.5, -98.93, 19.50, 7.8), (387.5, -98.96, 19.49, 7.4),
                            (t_1428 + 0.2, -99.03, 19.48, 6.4), (393.0, -99.04, 19.48, 6.2), (t_der + 0.4, -99.10, 19.49, 6.8),
                            (t_tri - 0.6, -99.05, 19.46, 4.8), (t_tres + 0.2, -98.75, 19.05, 1.6), (t_med - 0.3, -98.62, 18.90, 1.2),
                            (t_man, -98.70, 18.95, 1.3), (t_ten + 0.2, -99.0, 19.33, 3.0), (408.5, -99.12, 19.43, 12),
                            (410.5, -99.134, 19.434, 18), (413.0, -99.135, 19.435, 22), (415.5, -99.133, 19.436, 20),
                            (418.0, -99.13, 19.44, 17), (420.5, -99.12, 19.44, 15), (423.0, -99.13, 19.435, 18),
                            (425.5, -99.135, 19.437, 21), (t_nez2 - 0.6, -99.08, 19.46, 10), (430.5, -98.96, 19.50, 8.0),
                            (433.0, -98.91, 19.51, 8.6), (435.5, -98.89, 19.51, 9.2), (fin - 0.25, -98.92, 19.50, 8.8)):
        R.camara(tc, lon, lat, z)

    # frase 0: 1426 muere Tezozómoc; Maxtla aprieta
    anio(R, t_1426, 1426)
    pa(R, CH(5), 1600, 1000, 1.0, i0, t_mur + 0.3, sem=S(), sale="caer", d_out=0.8, extra=[(0.0, "pop", 0.3)],
       sfx_out=[(0.1, "golpe_suave", 0.4)])
    titulo(R, t_mur - 0.1, t_itz - 0.3, "MUERE TEZOZÓMOC", px=80, snd=True)
    R.ciudad(i0, t_itz - 0.3, "azcapotzalco", CI["azcapotzalco"], "AZCAPOTZALCO", "izq", 40)
    R.ciudad(t_1428 - 0.3, t_tri - 0.3, "azcapotzalco", CI["azcapotzalco"], "AZCAPOTZALCO", "izq", 40)
    lugar(R, i0 + 0.2, t_itz - 0.3, "TEPANECAS", (-99.24, 19.56), off=(0, 0), px=56)
    lugar(R, t_1428 - 0.2, t_der + 1.0, "TEPANECAS", (-99.24, 19.56), off=(0, 0), px=56)
    pa(R, AL(3), 1600, 1000, 1.05, t_max - 0.2, t_itz + 0.6, sem=S(), entra="sube", dy=320, extra=[(0.05, "impacto", 0.3)])
    R.texto(t_max, t_itz + 0.4, "MAXTLA", (1600, 560), px=48, d=0.35)
    R.texto(t_apr - 0.1, t_itz + 0.4, "¡MÁS TRIBUTO!", (1180, 470), px=52, d=0.35)
    pa(R, XO(7), 330, 1000, 0.55, t_max - 0.3, t_itz - 0.2, sem=S())

    # frase 1: Itzcóatl + Nezahualcóyotl, el heredero de Texcoco que vivía huyendo
    pa(R, AL(0), 330, 1000, 1.05, t_itz - 0.3, t_ley - 0.35, sem=S(), entra="sube", dy=320, extra=[(0.05, "tambor", 0.25)])
    R.texto(t_itz, t_ley - 0.45, "ITZCÓATL", (330, 560), px=48, d=0.35)
    R.texto(t_ali - 0.1, t_ley - 0.45, "+", (960, 820), px=150, d=0.25)
    titulo(R, t_ali - 0.1, t_ley - 0.2, "SE ALÍAN", px=86, snd=True)
    pa(R, AL(2), 1600, 1000, 1.05, t_pri - 0.1, t_ley - 0.35, sem=S(), entra="der", dx=800, d_in=0.6,
       extra=[(0.0, "pasos", 0.3, {"dur": 0.7})])
    R.texto(t_nez - 0.1, t_ley - 0.45, "NEZAHUALCÓYOTL", (1600, 560), px=46, d=0.5)
    R.texto(t_huy - 0.2, t_nez - 0.2, "(huyendo)", (1600, 490), px=40, d=0.3)
    R.ciudad(t_tex - 0.2, t_ley + 0.8, "texcoco", CI["texcoco"], "TEXCOCO", "der", 42, sfx=True)
    R.ciudad(t_rey - 0.2, fin, "texcoco", CI["texcoco"], "TEXCOCO", "der", 46)
    R.ciudad(t_itz, t_ley - 0.2, "tenochtitlan", CI["tenochtitlan"], "TENOCHTITLAN", "der", 38)

    # frase 2: la leyenda: desde un árbol vio cómo los tepanecas mataban a su padre
    titulo(R, t_ley - 0.1, t_1428 - 0.3, "CUENTA LA LEYENDA...", px=78, snd=True)
    pa(R, AL(1), 700, 1010, 1.25, t_ley + 0.05, t_1428 - 0.1, sem=S(), entra="sube", dy=420, extra=[(0.05, "papel", 0.3)])
    R.texto(t_arb, t_1428 - 0.2, "un muchacho en el árbol", (960, 300), px=50, d=0.5)
    foto(R, "nezahualcoyotl_xolotl", 1470, 960, 0.44, t_muc - 0.2, t_1428 - 0.1)
    ciclo_pant(R, C_GUE, -200, 1150, 1050, t_tep - 0.2, 2.6, t1=t_pad + 0.5, s=0.62, sem=S())
    ciclo_pant(R, C_GUE, -420, 950, 1060, t_tep + 0.1, 2.6, t1=t_pad + 0.5, s=0.58, sem=S())
    R.snd(t_tep, "tambor", 0.3, dur=1.2)
    pa(R, XO(2), 200, 1000, 0.45, t_arb - 0.2, t_1428 - 0.1, sem=S(), z=3, extra=[(0.4, "gemido_perro", 0.25)])

    # frase 3: 1428: mexicas, texcocanos y Tlacopan derrotan a Azcapotzalco
    anio(R, t_1428, 1428)
    R.ciudad(t_mex - 0.1, t_tri - 0.3, "tenochtitlan", CI["tenochtitlan"], "MEXICAS", "abajo", 42, sfx=True)
    R.ciudad(t_txc - 0.1, t_tri - 0.3, "texcoco", CI["texcoco"], "TEXCOCANOS", "abajo", 42, sfx=True)
    R.ciudad(t_tlc - 0.1, t_tri - 0.3, "tlacopan", CI["tlacopan"], "TLACOPAN", "izq", 42, sfx=True)
    pa(R, AL(6), 280, 1000, 0.92, t_mex - 0.2, t_tres - 0.1, sem=S(), extra=[(0.05, "tambor", 0.3)])
    pa(R, AL(7), 1640, 1000, 0.92, t_txc - 0.2, t_tri - 0.3, sem=S())
    pa(R, CH(7), 1000, 1000, 0.85, t_tlc - 0.2, t_tres - 0.1, sem=S())
    azc = CI["azcapotzalco"]
    for k, (tt, cl) in enumerate(((t_mex, "tenochtitlan"), (t_txc, "texcoco"), (t_tlc, "tlacopan"))):
        a = CI[cl]
        grupo_ciclo(R, C_GUE, [a, ((a[0] + azc[0]) / 2, (a[1] + azc[1]) / 2 + 0.01), azc], tt, 2.6 if k < 2 else 1.6, n=3, ancho=44,
                    t1=t_der + 1.2, s=0.24, sem=S(3))
    R.snd(t_der, "batalla", 0.5, dur=2.0)
    lugar(R, t_azc, t_tri, "¡DERROTADA!", azc, off=(0, -120), px=50)
    R.snd(t_azc + 0.1, "impacto", 0.35)
    R.texto(t_1428, t_mex - 0.2, "1428", (960, 196), px=96, d=0.3)

    # frase 4: la Triple Alianza: tres ciudades que se reparten el tributo… pero mandaba Tenochtitlan
    R.sello(t_tri, "columnas", "TRIPLE ALIANZA", color=(176, 56, 46))
    titulo(R, t_tri - 0.1, t_ten + 0.8, "LA TRIPLE ALIANZA", px=92, snd=True)
    R.terreno(t_tri - 0.2, "imperio_1440", COL["imperio_1440"], 2.0, capa=10)
    cols3 = [(196, 74, 52), (214, 164, 64), (98, 120, 176)]           # Tenochtitlan, Texcoco, Tlacopan
    R.romper("triple_alianza", t_tres, t_tres + 0.9, t_man - 0.2, t_ten + 0.6, colores=cols3, capa=10, gap=3.0, deriva=30.0)
    R.terreno(t_ten + 0.7, None, COL["imperio_1440"], 1.2, capa=10)          # se retira al entrar a la isla (vuelve con Moctezuma)
    R.texto(t_trib - 0.1, t_man - 0.3, "el tributo de medio México", (960, 300), px=52, d=0.6)
    for k, (x, txt) in enumerate(((520, "TENOCHTITLAN"), (960, "TEXCOCO"), (1400, "TLACOPAN"))):
        tt = t_tres + 0.25 * k
        if k == 0:
            dib = Crece(VI(5), t_man, t_ten, 1.0, 1.45)
        else:
            dib = Crece(VI(5), t_man, t_ten, 1.0, 0.6)
        pa(R, dib, x, 1010, 0.6, tt, t_ten + 0.8, sem=S(), extra=[(0.0, "pop", 0.3, {"tono": 1 + 0.1 * k})])
        R.texto(tt + 0.1, t_man - 0.2, txt, (x, 1040 - 0.6 * 400 - 50), px=38, d=0.4)
    R.texto(t_man - 0.1, t_ten + 0.9, "...pero mandaba TENOCHTITLAN", (960, 300), px=56, d=0.7)
    pa(R, XO(5), 1700, 1010, 0.45, t_ten - 0.6, t_itz2 + 0.3, sem=S(), extra=[(0.1, "ladrido", 0.3)])

    # frase 5: Itzcóatl manda quemar los libros antiguos
    pa(R, AL(0), 300, 1000, 0.95, t_itz2 - 0.2, t_don + 0.2, sem=S())
    R.texto(t_itz2, t_que - 0.2, "ITZCÓATL", (300, 580), px=46, d=0.35)
    foto(R, "itzcoatl_tovar", 1470, 960, 0.46, t_itz2 - 0.1, t_que + 0.3)
    titulo(R, t_que - 0.1, t_cod + 0.4, "QUEMA DE LIBROS", px=90, snd=True)
    pa(R, AL(4), 900, 1010, 1.15, t_que - 0.1, t_his - 0.2, sem=S(), entra="sube", dy=300, extra=[(0.05, "fuego", 0.5, {"dur": 2.5})])
    pa(R, XM(5), 1600, 1000, 0.6, t_lib + 0.5, t_his - 0.2, sem=S(), extra=[(0.2, "gemido_perro", 0.25)])

    # frase 6: en los códices viejos eran «don nadie»; en la historia nueva, el pueblo elegido del sol
    R.texto(t_cod, t_his + 0.2, "ANTES: UNOS DON NADIE", (960, 300), px=60, d=0.6)
    tachar(R, t_don + 0.4, t_his + 0.2, "ANTES: UNOS DON NADIE", (960, 300), 60, sem=S())
    pa(R, ME(7), 380, 1000, 0.95, t_his - 0.3, t_tlc2 - 0.2, sem=S(), extra=[(0.05, "escribir", 0.35, {"dur": 1.0})])
    R.texto(t_his - 0.1, t_con - 0.2, "LA HISTORIA NUEVA:", (960, 196), px=74, d=0.5)
    R.texto(t_ele - 0.4, t_con - 0.2, "el pueblo elegido del sol", (960, 300), px=58, d=0.6)
    pa(R, A.sol_brillo(70), 1500, 700, 2.1, t_sol - 0.3, t_con - 0.3, sem=S(), extra=[(0.05, "brillo", 0.35)])

    # frase 7: detrás, Tlacaélel, el consejero
    pa(R, AL(5), 1500, 1000, 1.1, t_con + 0.1, t_nez2 - 0.1, sem=S(), entra="der", dx=600)
    titulo(R, t_con - 0.1, t_nez2 - 0.2, "EL CONSEJERO DE VARIOS TLATOANIS", px=60)
    R.texto(t_tlc2 - 0.1, t_nez2 - 0.2, "TLACAÉLEL", (1500, 530), px=52, d=0.4)
    R.snd(t_tlc2, "flauta", 0.3)
    pa(R, XO(7), 760, 1000, 0.6, t_con, t_nez2 - 0.1, sem=S())

    # frase 8: Nezahualcóyotl, rey de Texcoco, constructor y poeta… en el billete de 100 pesos
    pa(R, AL(2), 330, 1000, 1.1, t_nez2 - 0.15, fin + 0.3, sem=S(), entra="sube", dy=320, extra=[(0.05, "flauta", 0.3)])
    R.texto(t_nez2 + 0.3, fin + 0.2, "NEZAHUALCÓYOTL", (330, 530), px=46, d=0.5)
    titulo(R, t_rey - 0.1, fin + 0.2, "REY DE TEXCOCO", px=84, snd=True)
    R.texto(t_cons - 0.1, t_bil - 0.2, "constructor y poeta", (960, 300), px=56, d=0.6)
    pa(R, billete(), 1450, 930, 1.05, t_bil - 0.2, fin + 0.3, sem=S(), entra="sube", dy=300, extra=[(0.05, "papel", 0.35)])
    R.texto(t_bil, fin + 0.2, "100", (1300, 760), px=52, d=0.3)
    pa(R, AL(2), 1523, 890, 0.34, t_bil + 0.1, fin + 0.3, sem=S(), z=3)
    R.texto(t_cien - 0.1, fin + 0.2, "100 PESOS", (1450, 640), px=48, d=0.4)
    pa(R, XO(5), 860, 1010, 0.45, t_poe - 0.2, fin + 0.3, sem=S(), extra=[(0.1, "ladrido", 0.25)])


# ------------------------------------------------------------------ MOCTEZUMA ILHUICAMINA
def _moctezuma1(R):
    e = "moctezuma1"
    i0, fin = INI(e), FIN(e)

    def w(p, i, **k):
        return T(e, p, frase=i, **k)
    t_1440, t_moc, t_ilh, t_fle, t_cie, t_pri = w("1440", 0), w("moctezuma", 0), w("ilhuicamina", 0), w("flecha", 0), w("cielo", 0), w("primero", 0)
    t_eje, t_sal, t_mor, t_gro, t_oax, t_gol = (w("ejercitos", 1), w("salieron", 1), w("morelos", 1), w("guerrero", 1), w("oaxaca", 1),
                                                w("costa", 1))
    t_hel, t_seq, t_ham = w("heladas", 2), w("sequia", 2), w("hambruna", 2)
    t_fam, t_ven, t_hij, t_cos, t_mai = w("familias", 3), w("vendieron", 3), w("hijos", 3), w("costa", 3), w("maiz", 3)
    t_xo, t_esc, t_pet, t_raz = w("xolo", 4), w("escondido", 4), w("petate", 4), w("razon", 4)
    t_mo5, t_dul, t_cha, t_isl, t_acu = w("moctezuma", 5), w("agua", 5), w("chapultepec", 5), w("isla", 5), w("acueducto", 5)
    t_nez, t_diq, t_lag, t_sep, t_sala = w("nezahualcoyotl", 6), w("dique", 6), w("lago", 6), w("separar", 6), w("salada", 6)
    t_rar, t_gf = w("raro", 7), w("guerra", 7)
    t_bat, t_pac, t_tlx, t_vec, t_con, t_cap, t_pris, t_sac = (w("batallas", 8), w("pactadas", 8), w("tlaxcala", 8), w("vecinos", 8),
                                                               w("conquistar", 8), w("capturar", 8), w("prisioneros", 8), w("sacrificio", 8))
    t_tlx2, t_cnq, t_olv = w("tlaxcala", 9), w("conquistada", 9), w("olvido", 9)

    for tc, lon, lat, z in ((i0 - 0.2, -99.05, 19.45, 6.0), (441.5, -99.12, 19.44, 9.0), (444.0, -99.13, 19.435, 12),
                            (t_pri + 0.2, -99.05, 19.30, 4.0), (t_sal - 0.2, -98.70, 18.90, 1.6), (t_mor + 0.4, -98.30, 18.50, 1.05),
                            (t_gol, -98.20, 18.45, 1.0), (t_hel - 1.3, -98.80, 19.20, 2.6), (t_hel + 0.6, -99.05, 19.45, 6.2),
                            (t_ham, -99.03, 19.46, 6.6), (t_ven - 0.8, -98.70, 19.40, 2.4), (t_cos - 0.8, -97.95, 19.45, 1.5),
                            (t_mai, -97.90, 19.45, 1.6), (t_xo + 0.5, -99.0, 19.45, 5.0), (t_pet - 0.4, -99.13, 19.435, 14),
                            (t_raz + 0.6, -99.14, 19.435, 18), (t_cha - 1.0, -99.155, 19.428, 20), (t_acu - 0.2, -99.157, 19.429, 22),
                            (t_nez - 0.2, -99.11, 19.42, 9.0), (t_diq - 0.3, -99.06, 19.43, 7.0), (t_sep, -99.06, 19.43, 7.4),
                            (t_sala + 0.4, -99.00, 19.38, 5.0), (t_rar, -98.70, 19.30, 3.2), (t_bat, -98.55, 19.28, 3.3),
                            (t_con - 0.6, -98.50, 19.27, 3.5), (t_pris, -98.55, 19.27, 3.4), (t_sac, -98.55, 19.29, 3.2),
                            (t_cnq - 0.6, -98.40, 19.28, 3.6), (t_olv - 0.4, -98.38, 19.28, 3.9), (fin - 0.25, -98.45, 19.29, 3.6)):
        R.camara(tc, lon, lat, z)

    # frase 0: 1440, Moctezuma Ilhuicamina, el que flecha el cielo
    anio(R, t_1440, 1440)
    pa(R, MO(0), 360, 1000, 1.1, i0, t_eje - 0.1, sem=S(), entra="sube", dy=320, extra=[(0.05, "caracol", 0.35)])
    R.texto(t_moc - 0.1, t_eje - 0.2, "MOCTEZUMA I", (360, 540), px=50, d=0.45)
    titulo(R, t_ilh - 0.1, t_eje - 0.2, "ILHUICAMINA", px=96, snd=True)
    R.texto(t_fle - 0.3, t_eje - 0.2, "«el que flecha el cielo»", (960, 312), px=56, d=0.6)
    R.snd(t_fle, "flecha", 0.5)
    foto(R, "moctezuma1_tovar", 1480, 960, 0.48, t_moc + 0.2, t_pri + 0.6)
    pa(R, XO(4), 900, 1010, 0.45, t_cie - 0.2, t_eje - 0.1, sem=S(), extra=[(0.2, "aullido", 0.2)])

    # frase 1: los ejércitos salen del valle: Morelos, Guerrero, Oaxaca, la costa del Golfo (imperio 1440 → 1469)
    R.terreno(t_eje - 0.2, "imperio_1440", COL["imperio_1440"], 1.2, capa=10)
    R.terreno(t_sal, "imperio_1469", COL["imperio_1469"], 4.0, capa=10)
    titulo(R, t_eje - 0.1, t_hel - 0.4, "EL IMPERIO CRECE", px=84, snd=True)
    foto(R, "moctezuma1_piedra", 1480, 960, 0.42, t_eje - 0.1, t_mor + 0.1)
    for k, n in enumerate((8, 9, 10)):
        pa(R, MO(n), 200 + 130 * k, 1010, 0.55, t_eje + 0.15 * k, t_hel - 0.3, sem=S(),
           extra=[(0.05, "pasos", 0.3, {"dur": 1.2})] if k == 0 else ())
    ten = CI["tenochtitlan"]
    destinos = ((t_mor, "MORELOS", (-99.12, 18.80), CI["cuauhnahuac"]), (t_gro, "GUERRERO", (-99.55, 17.75), CI["tlachco"]),
                (t_oax, "OAXACA", (-96.72, 16.95), CI["oaxaca"]), (t_gol, "COSTA DEL GOLFO", (-96.25, 19.40), CI["cuetlaxtlan"]))
    for k, (tt, txt, geo, dest) in enumerate(destinos):
        grupo_ciclo(R, C_GUE, [ten, ((ten[0] + dest[0]) / 2, (ten[1] + dest[1]) / 2 + 0.05), dest], t_sal - 0.2 + 0.35 * k, 3.4,
                    n=2, ancho=40, t1=t_hel - 0.2, s=0.42, sem=S(2))
        lugar(R, tt - 0.05, t_gol + 1.0, txt, geo, off=(0, 0), px=46)
        R.snd(tt, "tambor", 0.22, dur=0.5)

    # frase 2: heladas, sequía, hambruna
    anio(R, t_hel, 1454)
    pa(R, XO(2), 330, 1000, 0.6, t_hel - 1.6, t_fam + 0.4, sem=S(), extra=[(0.3, "gemido_perro", 0.3)])
    pa(R, MO(1), 960, 1010, 1.05, t_hel - 0.15, t_fam - 0.1, sem=S(), entra="sube", dy=320, extra=[(0.05, "viento_frio", 0.45)])
    titulo(R, t_hel - 0.1, t_ven - 0.4, "HELADAS Y SEQUÍA", px=90, snd=True)
    R.texto(t_ham - 0.6, t_ven - 0.4, "años de hambruna", (960, 312), px=58, d=0.6)
    pa(R, MO(3), 1600, 1010, 0.55, t_ham - 0.2, t_xo - 0.1, sem=S())

    # frase 3: familias vendieron a sus hijos en la costa a cambio de maíz
    pa(R, MO(2), 420, 1000, 1.05, t_fam - 0.15, t_xo - 0.1, sem=S(), entra="sube", dy=320)
    titulo(R, t_ven - 0.2, t_xo - 0.2, "VENDIERON A SUS HIJOS", px=76, snd=True)
    R.ruta([ten, CI["tlaxcala"], CI["xalapa"], (-96.62, 19.75)], t_ven, 2.2, ancho=5.0, flecha=True, t1=t_xo - 0.2)
    lugar(R, t_cos - 0.1, t_xo - 0.2, "COSTA (TOTONACAPAN)", (-96.95, 20.0), off=(0, 0), px=44)
    pa(R, VI(1), 1250, 1010, 0.75, t_mai - 0.2, t_xo - 0.1, sem=S())
    R.texto(t_mai, t_xo - 0.2, "a cambio de maíz", (1250, 610), px=46, d=0.4)

    # frase 4: Xolo, escondido debajo de un petate… y con razón
    pa(R, XO(3), 960, 1010, 1.35, t_xo - 0.15, t_mo5 - 0.1, sem=S(), entra="sube", dy=360, extra=[(0.2, "gemido_perro", 0.4)])
    titulo(R, t_pet - 0.2, t_mo5 - 0.2, "DEBAJO DE UN PETATE", px=80, snd=True)
    pa(R, XM(6), 1560, 1000, 0.62, t_raz - 0.3, t_mo5 - 0.1, sem=S(), entra="cae", dy=500, extra=[(0.3, "golpe_suave", 0.35)])
    R.texto(t_raz, t_mo5 - 0.2, "¡CON RAZÓN!", (1560, 560), px=50, d=0.3)

    # frase 5: acueducto de Chapultepec a la isla
    R.ciudad(t_cha - 0.2, t_nez + 0.6, "chapultepec", CI["chapultepec"], "CHAPULTEPEC", "abajo", 40, sfx=True)
    R.ciudad(t_isl - 0.1, t_nez + 0.6, "tenochtitlan", ten, "TENOCHTITLAN", "der", 40)
    acu = [CI["chapultepec"], (-99.170, 19.4255), (-99.158, 19.4290), (-99.146, 19.4325), ten]
    R.rio(acu, t_cha, 2.2, M.RIO, ancho=4.5)
    R.snd(t_cha + 0.2, "agua_lago", 0.35, dur=2.0)
    andar_ciclo(R, C_XOLO, acu, t_cha + 0.1, 2.6, t1=t_nez + 0.2, s=0.13, sem=S(), zs=0.4)
    pa(R, MO(4), 440, 1000, 0.68, t_mo5 - 0.1, t_nez + 0.1, sem=S(), entra="sube", dy=300)
    titulo(R, t_acu - 0.2, t_nez + 0.3, "ACUEDUCTO · 1466", px=80, snd=True)
    pa(R, MO(0), 1600, 1000, 0.95, t_mo5 - 0.1, t_nez + 0.1, sem=S(), entra="der", dx=600)
    R.texto(t_mo5 + 0.2, t_nez, "MOCTEZUMA I", (1600, 560), px=44, d=0.4)

    # frase 6: albarradón con Nezahualcóyotl: separa el agua dulce de la salada
    pa(R, AL(2), 330, 1000, 0.95, t_nez - 0.2, t_rar - 0.1, sem=S())
    R.texto(t_nez, t_rar - 0.2, "NEZAHUALCÓYOTL", (330, 580), px=44, d=0.45)
    titulo(R, t_diq - 0.1, t_rar - 0.2, "ALBARRADÓN · HACIA 1449", px=78, snd=True)
    R.snd(t_diq, "piedra", 0.4)
    R.snd(t_diq + 0.8, "cincel", 0.3)
    pa(R, MO(5), 1520, 1000, 1.0, t_diq - 0.1, t_rar - 0.1, sem=S(), entra="sube", dy=280)
    lugar(R, t_diq + 1.2, t_rar - 0.2, "16 KM", (-99.055, 19.485), off=(0, 0), px=40)
    lugar(R, t_sep, t_rar - 0.2, "DULCE", (-99.125, 19.40), off=(0, 0), px=40)
    lugar(R, t_sala - 0.1, t_rar - 0.2, "SALADA", (-98.97, 19.41), off=(0, 0), px=40)

    # frase 7: nació algo muy raro: la guerra florida
    pa(R, AL(6), 330, 1000, 1.0, t_rar - 1.8, t_con - 0.3, sem=S(), extra=[(0.05, "tambor", 0.3)])
    pa(R, XO(7), 650, 1010, 0.5, t_rar - 0.2, t_pac + 0.3, sem=S())
    R.sello(t_gf, "espadas", "GUERRA FLORIDA", color=(176, 56, 46))
    titulo(R, t_gf - 0.1, t_con - 0.3, "LA GUERRA FLORIDA", px=92, snd=True)
    R.texto(t_gf + 0.6, t_pac - 0.2, "xochiyáoyotl", (960, 312), px=52, d=0.5)

    # frase 8: batallas pactadas con Tlaxcala y sus vecinos, para capturar prisioneros
    R.terreno(t_tlx - 0.2, "tlaxcala", COL["tlaxcala"], 1.2, capa=11)
    lugar(R, t_tlx, fin + 0.2, "TLAXCALA", CI["tlaxcala"], off=(0, -60), px=52)
    R.ciudad(t_vec - 0.1, fin, "huexotzinco", CI["huexotzinco"], "HUEXOTZINCO", "izq", 36)
    R.ciudad(t_vec + 0.2, fin, "cholula", CI["cholula"], "CHOLULA", "abajo", 36)
    R.ciudad(t_bat, t_tlx2 - 0.2, "tenochtitlan", ten, "TENOCHTITLAN", "abajo", 38)
    pa(R, MO(6), 1600, 1000, 1.0, t_tlx - 0.2, fin + 0.3, sem=S(), entra="der", dx=600)
    R.texto(t_tlx + 0.4, t_cap - 0.2, "TLAXCALTECA", (1600, 560), px=44, d=0.45)
    R.texto(t_pac - 0.1, t_con - 0.3, "PACTADAS", (960, 312), px=60, d=0.4)
    R.snd(t_bat, "batalla", 0.45, dur=2.2)
    mid = (-98.62, 19.24)
    grupo_ciclo(R, C_GUE, [ten, (-98.95, 19.22), mid], t_bat - 0.2, 3.0, n=3, ancho=50, t1=t_sac + 0.6, s=0.36, sem=S(3))
    titulo(R, t_con - 0.15, t_tlx2 - 0.2, "NO PARA CONQUISTAR", px=78)
    tachar(R, t_con + 0.9, t_tlx2 - 0.2, "NO PARA CONQUISTAR", (960, 196), 78, sem=S())
    R.texto(t_cap - 0.1, t_tlx2 - 0.2, "sino para capturar prisioneros", (960, 312), px=56, d=0.7)
    pa(R, MO(7), 880, 1010, 0.82, t_cap - 0.2, t_tlx2 - 0.1, sem=S(), entra="izq", dx=700, extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    R.snd(t_sac, "tambor", 0.4, dur=1.5)

    # frase 9: Tlaxcala nunca fue conquistada… y nunca lo olvidó
    titulo(R, t_tlx2 - 0.1, fin + 0.2, "NUNCA CONQUISTADA", px=88, snd=True)
    R.terreno(t_cnq, "tlaxcala", (70, 160, 84), 0.6, capa=11)
    R.texto(t_olv - 0.8, fin + 0.2, "...y nunca lo olvidó", (960, 312), px=58, d=0.6)
    pa(R, XM(5), 330, 1000, 0.6, t_tlx2 - 0.1, fin + 0.3, sem=S(), extra=[(0.4, "gemido_perro", 0.25)])
    # limpiar capas al salir (mientras la cámara entra a la isla)
    R.terreno(fin + 0.1, None, COL["imperio_1469"], 1.0, capa=10)
    R.terreno(fin + 0.1, None, COL["tlaxcala"], 1.0, capa=11)
    R.snd(fin + 0.2, "whoosh", 0.35)


# ------------------------------------------------------------------ VIDA DIARIA Y MERCADO DE TLATELOLCO
def _vida(R):
    e = "vida"
    i0, fin = INI(e), FIN(e)

    def w(p, i, **k):
        return T(e, p, frase=i, **k)
    t_pau, t_viv, t_ten = w("pausar", 0), w("vivir", 0), w("tenochtitlan", 0)
    t_mac, t_com, t_cam, t_pes, t_art, t_arr, t_pip, t_nob = (w("macehuales", 1), w("gente", 1), w("campesinos", 1), w("pescadores", 1),
                                                              w("artesanos", 1), w("arriba", 1), w("pipiltin", 1), w("nobles", 1))
    t_nin, t_esc, t_tel, t_gue, t_nob2, t_cal, t_sac = (w("ninos", 2), w("escuela", 2), w("telpochcalli", 2), w("guerreros", 2),
                                                        w("nobles", 2), w("calmecac", 2), w("sacerdotes", 2))
    t_dis, t_cod, t_pad, t_cas, t_hum, t_chi = w("disciplina", 3), w("codice", 3), w("padre", 3), w("castiga", 3), w("humo", 3), w("chiles", 3)
    t_comp, t_mon, t_man, t_alg, t_cac = w("comprar", 4), w("monedas", 4), w("mantas", 4), w("algodon", 4), w("cacao", 4)
    t_fal, t_vac, t_tie = w("falsificadores", 5), w("vaciaban", 5), w("tierra", 5)
    t_mer, t_tla, t_cor, t_rey, t_ses, t_per = (w("mercado", 6), w("tlatelolco", 6), w("cortes", 6), w("rey", 6), w("sesenta", 6),
                                                w("personas", 6))
    t_oro, t_plu, t_jad, t_hie, t_guaj, t_perr, t_perr2, t_come = (w("oro", 7), w("plumas", 7), w("jade", 7), w("hierbas", 7),
                                                                   w("guajolotes", 7), w("perritos", 7), w("perritos", 7, n=1),
                                                                   w("comerselos", 7))
    t_xo, t_proc, t_cont = w("xolo", 8), w("procuraba", 8), w("contacto", 8)

    for tc, lon, lat, z in ((i0 - 0.2, -99.135, 19.435, 30), (506.0, -99.134, 19.436, 38), (508.5, -99.132, 19.434, 42),
                            (511.0, -99.136, 19.432, 44), (513.5, -99.139, 19.437, 40), (516.0, -99.134, 19.439, 42),
                            (518.5, -99.131, 19.435, 46), (521.0, -99.133, 19.431, 44), (523.5, -99.137, 19.434, 40),
                            (526.0, -99.135, 19.437, 42), (528.5, -99.132, 19.436, 45), (531.0, -99.130, 19.433, 47),
                            (533.5, -99.134, 19.431, 44), (536.0, -99.137, 19.435, 41), (538.5, -99.134, 19.438, 43),
                            (541.0, -99.131, 19.436, 46), (543.5, -99.133, 19.433, 43), (546.0, -99.136, 19.436, 41),
                            (548.5, -99.137, 19.440, 38), (t_mer - 0.4, -99.138, 19.443, 40), (553.0, -99.137, 19.442, 44),
                            (555.5, -99.139, 19.443, 47), (558.0, -99.136, 19.441, 45), (560.5, -99.137, 19.442, 43),
                            (563.0, -99.139, 19.443, 46), (565.5, -99.137, 19.442, 49), (568.0, -99.135, 19.441, 46),
                            (570.5, -99.137, 19.442, 48), (573.0, -99.138, 19.443, 50), (fin - 0.25, -99.137, 19.442, 47)):
        R.camara(tc, lon, lat, z)

    # frase 0: pausa: ¿cómo era vivir en Tenochtitlan?
    pa(R, XO(6), 330, 1010, 0.62, i0, t_mac - 0.2, sem=S())
    R.texto(t_pau - 0.1, t_viv - 0.3, "PAUSA", (960, 312), px=64, d=0.4)
    R.snd(t_pau, "pluck", 0.35)
    titulo(R, t_viv - 0.3, t_cam - 0.3, "¿CÓMO ERA VIVIR AQUÍ?", px=84, snd=True)
    R.ciudad(t_ten - 0.1, t_mac, "tenochtitlan", CI["tenochtitlan"], "TENOCHTITLAN", "der", 40)
    andar_ciclo(R, C_CAN, [(-99.160, 19.420), (-99.145, 19.4225), (-99.120, 19.425)], i0 + 0.2, 6.0, t1=t_nin, s=0.16, sem=S(), zs=0.4)
    grupo_ciclo(R, C_MEX, [(-99.142, 19.430), (-99.136, 19.433), (-99.128, 19.436)], i0 + 0.6, 6.5, n=3, ancho=36, t1=t_mac + 2.0,
                s=0.13, sem=S(3))
    pa(R, ME(8), 1580, 1010, 0.8, i0 + 0.4, t_mac - 0.2, sem=S(), extra=[(0.1, "fuego", 0.15, {"dur": 1.0})])

    # frase 1: macehuales (campesinos, pescadores, artesanos) y arriba los pipiltin
    pa(R, VI(5), 960, 1010, 1.15, t_mac - 0.3, t_nin - 0.2, sem=S(), entra="sube", dy=360, extra=[(0.05, "piedra", 0.3)])
    pa(R, VI(0), 300, 1000, 0.95, t_mac + 0.2, t_nin - 0.2, sem=S())
    R.texto(t_com - 0.1, t_nin - 0.3, "GENTE COMÚN", (300, 560), px=44, d=0.4)
    R.texto(t_mac + 0.2, t_nin - 0.3, "MACEHUALES", (960, 960), px=36, d=0.4)
    for k, (tt, txt) in enumerate(((t_cam, "CAMPESINOS"), (t_pes, "PESCADORES"), (t_art, "ARTESANOS"))):
        R.texto(tt - 0.05, t_pip - 0.3, txt, (520 + 440 * k, 196), px=58, d=0.4)
        R.snd(tt, "pop", 0.25, tono=1 + 0.1 * k)
    ciclo_pant(R, C_CAN, 2050, -250, 1060, t_pes - 0.6, 5.0, t1=t_nin - 0.2, s=0.42, sem=S(), z=4)
    pa(R, ME(7), 1600, 1000, 0.85, t_art - 0.1, t_arr + 0.6, sem=S(), extra=[(0.05, "escribir", 0.3, {"dur": 0.8})])
    pa(R, VI(2), 1600, 1000, 1.0, t_pip - 0.3, t_nin - 0.2, sem=S(), entra="sube", dy=320, extra=[(0.05, "brillo", 0.3)])
    R.texto(t_pip - 0.1, t_nin - 0.3, "PIPILTIN (NOBLES)", (1560, 560), px=42, d=0.5)

    # frase 2: escuela: telpochcalli (guerreros) y calmécac (sacerdotes)
    titulo(R, t_esc - 0.2, t_dis - 0.3, "A LA ESCUELA", px=90, snd=True)
    pa(R, VI(3), 280, 1000, 0.9, t_nin - 0.1, t_dis - 0.1, sem=S())
    pa(R, VI(4), 520, 1000, 0.85, t_tel - 0.3, t_dis - 0.1, sem=S())
    R.texto(t_tel - 0.1, t_dis - 0.2, "TELPOCHCALLI", (400, 560), px=48, d=0.5)
    R.texto(t_gue - 0.3, t_dis - 0.2, "para ser guerreros", (400, 490), px=38, d=0.4)
    foto(R, "mendoza_escuela", 960, 960, 0.44, t_esc + 0.2, t_cal - 0.2)
    pa(R, VI(6), 1380, 1000, 1.0, t_nob2 - 0.2, t_dis - 0.1, sem=S())
    pa(R, VI(7), 1640, 1000, 0.85, t_cal - 0.1, t_dis - 0.1, sem=S())
    R.texto(t_cal - 0.1, t_dis - 0.2, "CALMÉCAC", (1500, 560), px=48, d=0.4)
    R.texto(t_sac - 0.4, t_dis - 0.2, "con los sacerdotes", (1500, 490), px=38, d=0.4)
    R.snd(t_cal, "caracol", 0.25)

    # frase 3: la disciplina: el humo de chiles del Códice Mendoza
    titulo(R, t_dis - 0.1, t_comp - 0.3, "DISCIPLINA SERIA", px=88, snd=True)
    pa(R, XO(2), 220, 1010, 0.5, t_dis + 0.2, t_comp - 0.1, sem=S())
    foto(R, "mendoza_castigos", 1480, 960, 0.48, t_cod - 0.2, t_comp - 0.1)
    pa(R, VI(8), 560, 1000, 1.1, t_pad - 0.2, t_comp - 0.1, sem=S(), entra="sube", dy=300, extra=[(0.3, "llanto", 0.12, {"dur": 1.0})])
    pa(R, VI(9), 880, 1010, 0.72, t_hum - 0.3, t_comp - 0.1, sem=S(), extra=[(0.05, "fuego", 0.3, {"dur": 1.2})])
    R.texto(t_hum, t_comp - 0.2, "¡HUMO DE CHILE!", (760, 450), px=52, d=0.4)
    R.snd(t_chi + 0.3, "tos", 0.35)

    # frase 4: no había monedas: mantas de algodón y granos de cacao
    titulo(R, t_comp - 0.1, t_fal - 0.3, "¿Y PARA COMPRAR?", px=84)
    R.texto(t_mon - 0.4, t_fal - 0.3, "MONEDAS", (960, 312), px=60, d=0.4)
    tachar(R, t_mon + 0.3, t_fal - 0.3, "MONEDAS", (960, 312), 60, sem=S())
    pa(R, VI(12), 380, 1010, 0.85, t_man - 0.2, t_fal - 0.1, sem=S(), extra=[(0.05, "papel", 0.3)])
    R.texto(t_man, t_fal - 0.2, "MANTAS DE ALGODÓN", (380, 600), px=44, d=0.5)
    pa(R, VI(10), 1080, 1010, 0.6, t_cac - 0.6, t_fal - 0.1, sem=S(), extra=[(0.05, "monedas", 0.4)])
    R.texto(t_cac - 0.2, t_fal - 0.2, "CACAO", (1080, 700), px=52, d=0.35)
    foto(R, "cacao_mazorca", 1560, 930, 0.38, t_cac - 0.8, t_fal - 0.1)
    pa(R, XO(0), 760, 1010, 0.45, t_man + 0.3, t_fal - 0.1, sem=S())

    # frase 5: falsificadores de cacao
    titulo(R, t_fal - 0.1, t_mer - 0.3, "¡FALSIFICADORES!", px=92, snd=True)
    pa(R, VI(13), 900, 1010, 1.05, t_fal - 0.3, t_mer - 0.1, sem=S(), entra="sube", dy=300)
    R.texto(t_vac, t_mer - 0.2, "cacao relleno de tierra", (900, 312), px=54, d=0.6)
    pa(R, XO(7), 330, 1000, 0.6, t_fal + 0.2, t_mer - 0.1, sem=S())
    foto(R, "cacao_granos", 1500, 960, 0.44, t_fal + 0.3, t_mer - 0.1)
    R.snd(t_tie, "golpe_suave", 0.3)

    # frase 6: el mercado de Tlatelolco: 60 000 personas al día (según Cortés)
    R.snd(t_mer - 0.2, "multitud", 0.4, dur=7.5)
    R.ciudad(t_tla - 0.2, t_xo, "tlatelolco", CI["tlatelolco"], "TLATELOLCO", "der", 42, sfx=True)
    titulo(R, t_mer - 0.1, t_cor - 0.2, "MERCADO DE TLATELOLCO", px=80, snd=True)
    pa(R, ME(6), 960, 1010, 1.05, t_mer - 0.3, t_oro - 0.1, sem=S(), entra="sube", dy=320)
    pa(R, ME(3), 330, 1000, 1.0, t_mer - 0.6, t_ses - 0.6, sem=S(), extra=[(0.05, "pasos", 0.3, {"dur": 0.9})])
    R.texto(t_mer + 0.2, t_ses - 0.7, "POCHTECA", (330, 560), px=44, d=0.4)
    foto(R, "florentino_pochteca", 1500, 960, 0.38, t_tla + 0.2, t_ses - 0.3)
    R.texto(t_cor + 0.1, t_ses - 0.3, "CORTÉS AL REY:", (960, 196), px=70, d=0.5)
    R.contador(t_ses - 0.1, t_per + 0.4, 0, 60000, (960, 196), px=72, formato="{:,} PERSONAS AL DÍA", hasta_t=t_oro - 0.2)
    foto(R, "florentino_tamales", 430, 960, 0.34, t_ses - 0.4, t_oro - 0.1)
    grupo_ciclo(R, C_MEX, [(-99.150, 19.444), (-99.144, 19.447), (-99.139, 19.450)], t_mer, 6.0, n=4, ancho=34, t1=t_oro + 0.5,
                s=0.13, sem=S(4))

    # frase 7: oro, plumas, jade, hierbas, guajolotes… y perritos
    pa(R, ME(0), 300, 1010, 0.5, t_oro - 0.2, t_xo - 0.2, sem=S(), extra=[(0.05, "brillo", 0.3)])
    R.texto(t_oro - 0.05, t_xo - 0.3, "ORO · PLUMAS · JADE", (330, 740), px=40, d=0.5)
    foto(R, "florentino_plumaria", 1450, 900, 0.40, t_plu - 0.2, t_guaj - 0.3)
    pa(R, ME(4), 720, 1010, 0.78, t_hie - 0.2, t_xo - 0.2, sem=S())
    R.texto(t_hie, t_xo - 0.3, "HIERBAS", (720, 640), px=44, d=0.4)
    pa(R, ME(1), 1120, 1010, 0.85, t_guaj - 0.2, t_xo - 0.2, sem=S(), extra=[(0.1, "guajolote", 0.4)])
    R.texto(t_guaj, t_xo - 0.3, "GUAJOLOTES", (1120, 600), px=44, d=0.45)
    pa(R, ME(5), 1600, 1010, 0.95, t_perr - 0.2, fin + 0.3, sem=S(), entra="sube", dy=300, extra=[(0.3, "ladrido", 0.2)])
    R.texto(t_perr, fin + 0.2, "¡PERRITOS!", (1600, 560), px=52, d=0.35)
    titulo(R, t_perr2 - 0.1, t_xo - 0.3, "...PARA COMÉRSELOS", px=86, snd=True)
    R.snd(t_come, "gemido_perro", 0.25)

    # frase 8: Xolo procura no hacer contacto visual
    pa(R, XO(7), 1130, 1010, 0.8, t_xo - 0.15, fin + 0.3, sem=S(), flip=True, entra="izq", dx=700)
    titulo(R, t_proc - 0.2, fin + 0.2, "SIN CONTACTO VISUAL", px=84, snd=True)
    R.texto(t_cont + 0.3, fin + 0.2, "(silbando)", (1130, 560), px=40, d=0.3)
    R.snd(t_proc, "gemido_perro", 0.25)
    pa(R, ME(6), 420, 1010, 0.85, t_xo + 0.2, fin + 0.3, sem=S())
