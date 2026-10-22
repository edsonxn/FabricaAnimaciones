# -*- coding: utf-8 -*-
"""Coreografía (3/4) de «La historia de Aguascalientes»: Posada (San Marcos 1852, el grabado, León y la Ciudad de México, 5 millones
de copias, la Calavera Garbancera que Rivera volvió Catrina, la fosa sin nombre y el museo junto al Encino), el Porfiriato (el tren de
1884, los talleres de 80 ha, Tres Centurias, los Guggenheim y el Cerro de la Grasa, el Teatro Morelos, San Antonio y Refugio Reyes,
Saturnino Herrán) y la Soberana Convención de 1914 (la bandera firmada, Villa, Soto y Gama, Eulalio Gutiérrez y el teatro hoy).
Dibujos = pegatinas de Flow; fotos = FotoPeg. sem 600-899. Capas de terreno 20-29 (se limpian al salir de cada escena)."""
import math

import numpy as np

import boceto as B
import foto_peg as FP
import mapa as M
import obj_a as A
from core import FIN, INI, T, kf
from coreo_peg import andar_ciclo, grupo_ciclo
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo, tramo
from motor import e_inout, e_out, prog
from pegflow import P, ciclo

# ------------------------------------------------------------------ atajos de hojas (números de piezas/<hoja>/_indice.jpg)
FU = lambda n, **k: P("03_fundacion_hoja", n, **k)      # 1 colono, 2 colona, 3 carta con sello, 6 cruz
CO = lambda n, **k: P("04_colonia_hoja", n, **k)        # 2 templo de San Marcos, 3 cura
XI = lambda n, **k: P("05_xix_hoja", n, **k)            # 1 dama, 2 caballero
AR = lambda n, **k: P("06_arte_hoja", n, **k)           # 0 grabador, 1 prensa, 2 catrina, 3 calavera baila, 4 hoja volante, 5 pintor, 6 cuadro diosa, 7 cempasúchil
PO = lambda n, **k: P("07_porfiriato_hoja", n, **k)     # 0 locomotora, 1-2 humo, 3 ferrocarrilero, 4 taller, 5 fundición, 6 escoria, 7 teatro, 8 templo S. Antonio, 9 arquitecto
RV = lambda n, **k: P("08_revolucion_hoja", n, **k)     # 0 Villa, 1 Obregón, 2 zapatista, 3 bandera firmada, 4 discuten, 5 adelita, 6 Eulalio, 7 tribuna
PL = lambda n, **k: P("02_plata_hoja", n, **k)          # 7 plata (lingotes)
C_VILLA = ciclo("14_villa_galope")
C_SOLD = ciclo("12_soldado_marcha")

SAN_ANTONIO = (-102.2905, 21.8862)     # templo de San Antonio (y el Museo de Aguascalientes enfrente), aprox.
FUNDICION = (-102.2840, 21.9050)       # Gran Fundición Central / Cerro de la Grasa, al norte de la estación (aprox.)

_SEM = iter(range(600, 900))


def S():
    return next(_SEM)


_ULT = [None]


def anio(R, t, v, hold=0.5):
    """Año grande con espera: el contador no cuenta despacio entre dos años lejanos (sostiene el anterior hasta t - hold)."""
    if _ULT[0] is not None and _ULT[0] != v:
        R.anio(t - hold, _ULT[0])
    R.anio(t, v)
    _ULT[0] = v


def foco(lon, lat, z, dy=140):
    """Clave de cámara que deja (lon, lat) ~dy px por DEBAJO del centro (los dibujos crecen hacia arriba)."""
    return lon, lat + dy / (640.0 * z * 1.07), z


class Crece:
    """Envuelve una pegatina y la hace crecer de s0 a 1 entre t0 y t1 (humo que se expande, escoria que se amontona)."""

    def __init__(self, p, t0, t1, s0=0.3):
        self.p, self.t0, self.t1, self.s0 = p, t0, t1, s0
        self.alto = getattr(p, "alto", 400.0)
        self.total = 1.0

    def dibujar(self, hoja, x, y, s=1.0, *a, **k):
        tv = k.get("tv")
        g = 1.0 if tv is None else self.s0 + (1 - self.s0) * e_out(prog(tv, self.t0, self.t1))
        self.p.dibujar(hoja, x, y, s * g, *a, **k)


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


def firmas(R, t0, t1, caja, n, dur, sem=0):
    """Firmas manuscritas que aparecen una por una dentro de caja=(x0, y0, x1, y1) (pantalla)."""
    rng = np.random.default_rng(sem)
    x0, y0, x1, y1 = caja
    trazos = []
    for k in range(n):
        cx, cy = rng.uniform(x0 + 40, x1 - 40), y0 + (y1 - y0) * ((k + 0.5) / n) + rng.uniform(-12, 12)
        w = rng.uniform(42, 70)
        xs = np.linspace(-w, w, 26)
        fr, ph, a = rng.uniform(0.12, 0.22), rng.uniform(0, 6.3), rng.uniform(7, 13)
        ys = a * np.sin(xs * fr + ph) - 5 * np.cos(xs * fr * 2.3)
        trazos.append((np.stack([cx + xs, cy + ys], 1), np.array([(cx - w * 0.8, cy + 15), (cx + w * 0.9, cy + 11)]),
                       t0 + dur * k / n))

    def f(h, cam, t, fs, te):
        if t < t0 or t > t1 + 0.3:
            return
        v = int(255 * (1 - prog(t, t1, t1 + 0.3)))
        for i, (Pf, Pr, tk) in enumerate(trazos):
            u = prog(t, tk, tk + 0.3)
            if u > 0 and v > 0:
                h.trazo(Pf, 4.0, 700 + sem + i, fs, u, amp=0.9, v=v)
                if u >= 1:
                    h.trazo(Pr, 2.6, 760 + sem + i, fs, prog(t, tk + 0.3, tk + 0.45), amp=0.7, v=v)
    R.frente.append(R._acot(f, t0))


def humo_geo(R, geo, tb, dur=1.5, s=0.32, off0=(0, 0), deriva=(-60, -170), n=1, z=3):
    """Bocanada de humo anclada al mapa: nace pequeña en off0, sube, se expande y se apaga."""
    ga(R, Crece(PO(n), tb, tb + dur, 0.35), geo, tb, tb + dur - 0.3, s=s,
       off=lambda t, a=tb: (off0[0] + deriva[0] * prog(t, a, a + dur), off0[1] + deriva[1] * prog(t, a, a + dur)),
       entra="pop", sale="encoger", d_in=0.3, d_out=0.3, sem=S(), z=z, zs=0.4)


def humo_pant(R, xf, yf, tb, dur=1.6, s=0.45, deriva=(-140, -260), n=1, z=1):
    """Bocanada de humo en pantalla que sale de (xf(t), yf(t)) en tb."""
    x0, y0 = xf(tb), yf(tb)
    pa(R, Crece(PO(n), tb, tb + dur, 0.35), lambda t, a=tb: x0 + deriva[0] * prog(t, a, a + dur),
       lambda t, a=tb: y0 + deriva[1] * prog(t, a, a + dur), s, tb, tb + dur - 0.3, d_in=0.3, d_out=0.3, sem=S(), z=z)


def cortes(R):
    pass


def construir(R):
    _posada(R)
    _porfiriato(R)
    _convencion(R)


# ------------------------------------------------------------------ POSADA
def _posada(R):
    e = "posada"
    i0, fin = INI(e), FIN(e)
    t_bar, t_sanm, t_jose = T(e, "barrio"), T(e, "san marcos"), T(e, "jose", frase=0)
    t_apr, t_gra, t_tal, t_leon, t_cdmx = T(e, "aprendio"), T(e, "grabar"), T(e, "taller"), T(e, "leon"), T(e, "ciudad")
    t_per, t_cor = T(e, "periodicos"), T(e, "corridos")
    t_calc, t_5, t_cop = T(e, "calcula"), T(e, "5", frase=2), T(e, "copias")
    t_cal, t_cri, t_mila, t_not, t_gen, t_leer = (T(e, "calaveras"), T(e, "crimenes"), T(e, "milagros"), T(e, "noticias"),
                                                  T(e, "gente"), T(e, "leer"))
    t_pers, t_catr1, t_calav = T(e, "personaje"), T(e, "catrina", frase=3), T(e, "calavera garbancera")
    t_bur, t_neg, t_eur = T(e, "burla"), T(e, "negaban"), T(e, "europeos")
    t_dec, t_riv, t_vis, t_gala, t_con, t_catr2 = (T(e, "decadas"), T(e, "rivera"), T(e, "vistio"), T(e, "gala"),
                                                   T(e, "conocemos"), T(e, "catrina", frase=4))
    t_pos5, t_pob, t_1913, t_fosa, t_hoy, t_nad, t_res = (T(e, "posada", frase=5), T(e, "pobre"), T(e, "1913"), T(e, "fosa"),
                                                          T(e, "hoy", frase=5), T(e, "nadie"), T(e, "restos"))
    t_obra, t_mus, t_enc = T(e, "obra"), T(e, "museo"), T(e, "encino")
    f4 = FIN(e, 4)
    sm, en = CI["san_marcos"], CI["encino"]

    # cámara: San Marcos de cerca -> la región (Ags, León, Ciudad de México) -> hacia la capital del país -> el Encino
    R.camara(i0 - 0.2, *foco(sm[0], sm[1], 4.0))
    R.camara(t_sanm, *foco(sm[0] - 0.003, sm[1], 5.4))
    R.camara(t_apr, *foco(sm[0], sm[1], 4.6))
    R.camara(t_leon - 0.3, -101.62, 21.45, 1.3)
    R.camara(t_calc, -101.58, 21.42, 1.36)
    R.camara(t_pers, -101.62, 21.45, 1.5)
    R.camara(t_dec, -101.5, 21.3, 1.75)
    R.camara(t_pos5, -101.4, 21.2, 2.05)
    R.camara(t_res, -101.45, 21.25, 2.2)
    R.camara(t_mus - 0.3, *foco(en[0], en[1], 5.0))
    R.camara(fin, *foco(en[0] + 0.002, en[1], 5.5))

    R.anio(i0 - 0.3, 1852)
    anio(R, i0, 1852)
    # frase 0: nace en San Marcos
    pa(R, AR(7), 320, 1010, 0.78, i0 - 0.1, t_apr, sem=S())
    ga(R, CO(2), sm, t_bar - 0.15, t_apr + 0.3, s=0.55, off=(-20, -6), sem=S(), zs=0.4, z=1, entra="sube", dy=240,
       extra=[(0.05, "crece", 0.3)])
    ciudad(R, t_sanm, t_apr + 0.2, "san_marcos", "BARRIO DE SAN MARCOS", "abajo", 40)
    pa(R, FP.F("posada_0"), 1560, 1010, FP.s_para(0.42), t_jose - 0.45, t_gra + 0.8, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_jose, t_apr - 0.1, "JOSÉ GUADALUPE POSADA", px=76, snd=True)

    # frase 1: el taller, León, Ciudad de México, periódicos y corridos
    pa(R, AR(0), 330, 1010, 1.0, t_gra - 0.15, t_cal - 0.2, sem=S())
    pa(R, AR(1), 640, 1010, 0.78, t_tal - 0.1, t_calc - 0.1, sem=S(), extra=[(0.1, "golpe_suave", 0.4)])
    ags, leon, cdmx = CI["aguascalientes"], CI["leon"], CI["ciudad_mexico"]
    R.ruta([ags, (-102.1, 21.6), (-101.93, 21.36), leon], t_leon - 0.5, 1.0, ancho=5.0, t1=t_calc, flecha=True)
    R.ruta([leon, (-101.35, 21.0), (cdmx[0] + 0.06, cdmx[1] + 0.06)], t_cdmx - 0.3, 1.0, ancho=5.0, t1=t_calc, flecha=True)
    R.snd(t_leon - 0.5, "whoosh", 0.4, dur=0.7)
    ciudad(R, t_leon - 0.1, t_calc, "aguascalientes", "AGUASCALIENTES", "der", 36)
    ciudad(R, t_leon, t_calc, "leon", "LEÓN", "izq", 40)
    lugar(R, t_cdmx, t_calc - 0.2, "A LA CIUDAD DE MÉXICO", cdmx, off=(-260, -70), px=40)
    for k, (dx, dy) in enumerate(((-60, -60), (-170, -110), (-60, -190), (-250, -40), (-160, -230), (-290, -150))):
        ga(R, AR(4), cdmx, t_per - 0.1 + 0.2 * k, t_calc - 0.1, s=0.34, off=(dx, dy), sem=S(), zs=0.4, z=2 + k, rot=0.12 * (k % 3 - 1),
           extra=[(0.0, "papel", 0.35)] if k in (0, 3) else ())

    # frase 2: 5 millones de copias, calaveras, crímenes, milagros y noticias
    R.contador(t_5 - 0.3, t_cop + 0.2, 0, 5000000, (960, 196), px=74, formato="{:,} DE COPIAS", hasta_t=t_gen)
    for k, (x, rot) in enumerate(((760, -0.10), (900, 0.06), (1040, -0.04), (820, 0.12), (980, -0.12), (1110, 0.08))):
        pa(R, AR(4), x, 1000 - 22 * (k % 2), 0.56, t_calc + 0.3 * k, t_leer + 0.3, sem=S(), z=3 + k, rot=rot)
    R.snd(t_calc, "papel", 0.35)
    pa(R, AR(3), 330, 1010, 1.0, t_cal - 0.1, t_riv - 0.2, sem=S(), extra=[(0.05, "pluck", 0.35)])
    for k, (txt, t_, x) in enumerate((("CALAVERAS", t_cal, 430), ("CRÍMENES", t_cri, 790), ("MILAGROS", t_mila, 1150),
                                      ("NOTICIAS", t_not, 1510))):
        R.texto(t_, t_leer + 0.3, txt, (x, 316), px=46, d=0.4)
    pa(R, FU(2), 1420, 1010, 0.9, t_gen - 0.1, t_pers + 0.3, sem=S())
    pa(R, FU(1), 1640, 1010, 0.95, t_gen + 0.1, t_pers + 0.3, sem=S())

    # frase 3: no se llamaba Catrina: Calavera Garbancera
    R.texto(t_catr1 - 0.25, t_calav - 0.3, "¿CATRINA?", (960, 196), px=84, d=0.4)
    tachar(R, t_catr1 + 0.45, t_calav - 0.3, "¿CATRINA?", (960, 196), 84, sem=1)
    R.texto(t_calav, t_catr2 + 0.4, "CALAVERA GARBANCERA", (960, 196), px=80, d=0.8)
    pa(R, FP.F("posada_3"), 1500, 1010, FP.s_para(0.5), t_calav - 0.1, t_dec + 0.6, entra="pluma", d_in=0.6, sem=S(),
       extra=[(0.1, "pop", 0.35, {"tono": 0.9})])
    R.texto(t_bur, t_eur - 0.35, "UNA BURLA", (960, 316), px=50, d=0.4)
    pa(R, XI(1), 720, 1010, 0.92, t_neg - 0.1, t_vis - 0.2, sem=S())
    pa(R, XI(2), 980, 1010, 0.95, t_neg + 0.15, t_vis - 0.2, sem=S())
    R.texto(t_eur - 0.3, t_dec + 0.2, "«PARECER EUROPEOS»", (960, 316), px=50, d=0.5)

    # frase 4: Diego Rivera la viste de gala: la Catrina
    pa(R, AR(5), 330, 1010, 1.0, t_riv - 0.25, f4 + 0.4, sem=S())
    R.texto(t_riv, f4 + 0.3, "DIEGO RIVERA", (330, 560), px=44, d=0.4)
    pa(R, AR(2), 960, 1010, 1.18, t_vis - 0.1, f4 + 0.5, sem=S(), entra="sube", dy=380, extra=[(0.1, "fanfarria", 0.3)])
    tachar(R, t_gala + 0.1, t_catr2 + 0.4, "CALAVERA GARBANCERA", (960, 196), 80, sem=2)
    R.texto(t_con, f4 + 0.5, "CATRINA", (1560, 560), px=100, d=0.6)
    pa(R, AR(7), 1560, 1010, 0.62, t_con - 0.1, f4 + 0.5, sem=S())

    # frase 5: muere pobre en 1913, fosa sin nombre
    anio(R, t_1913, 1913)
    pa(R, AR(0), 330, 1010, 1.0, t_pos5 - 0.15, t_fosa - 0.2, sem=S(), sale="baja", d_out=0.7)
    titulo(R, t_pob - 0.1, t_fosa - 0.3, "MURIÓ POBRE", px=80)
    pa(R, AR(4), 700, 1010, 0.6, t_pob, t_fosa - 0.2, sem=S(), entra="cae", dy=700, rot=0.2, sale="baja", d_out=0.7)
    pa(R, AR(1), 1000, 1010, 0.7, t_pob + 0.3, t_fosa - 0.2, sem=S(), sale="baja", d_out=0.7)
    R.snd(t_1913, "golpe_suave", 0.45)
    titulo(R, t_fosa - 0.1, t_res + 0.6, "FOSA SIN NOMBRE", px=80)
    pa(R, FU(6), 960, 1010, 0.8, t_fosa - 0.2, t_obra - 0.1, sem=S(), entra="sube", dy=300)
    pa(R, AR(7), 1300, 1015, 0.75, t_fosa + 0.2, t_obra - 0.1, sem=S(), entra="sube", dy=200)
    pa(R, AR(3), 560, 1010, 0.7, t_fosa + 0.5, t_obra - 0.1, sem=S())
    R.texto(t_nad, t_res + 0.6, "¿DÓNDE?", (960, 320), px=66, d=0.4)
    pa(R, AR(7), 1600, 1010, 0.72, t_hoy - 0.1, t_mus, sem=S())

    # frase 6: el Museo José Guadalupe Posada junto al Encino (se puede visitar)
    pa(R, AR(4), 300, 1010, 0.8, t_obra - 0.15, fin + 0.3, sem=S(), rot=-0.06)
    pa(R, AR(3), 560, 1010, 0.85, t_obra + 0.1, fin + 0.3, sem=S())
    ga(R, CO(2), en, t_mus - 0.2, fin + 0.3, s=0.5, off=(-170, -8), sem=S(), zs=0.4, z=1, entra="sube", dy=240)
    titulo(R, t_mus - 0.1, fin + 0.3, "HOY: MUSEO JOSÉ GUADALUPE POSADA", px=64, snd=True)
    ciudad(R, t_mus + 0.2, fin + 0.3, "encino", "TEMPLO DEL ENCINO", "izq", 38)
    pa(R, FP.F("posada_6"), 1580, 1010, FP.s_para(0.43), t_mus - 0.3, fin + 0.3, entra="pluma", d_in=0.6, sem=S())


# ------------------------------------------------------------------ PORFIRIATO
def _porfiriato(R):
    e = "porfiriato"
    i0, fin = INI(e), FIN(e)
    t_lle, t_tren, t_pas, t_fc, t_cdmx, t_fro = (T(e, "llego"), T(e, "tren"), T(e, "pasajeros"), T(e, "ferrocarril"),
                                                 T(e, "ciudad"), T(e, "frontera"))
    t_cam, t_emp, t_tal, t_80, t_con, t_loc = (T(e, "cambio"), T(e, "empresa"), T(e, "talleres"), T(e, "80"), T(e, "construir"),
                                               T(e, "locomotoras"))
    t_ags, t_ciu = INI(e, 2), T(e, "ciudad", frase=2)
    t_nav, t_hoy, t_est, t_1911 = T(e, "naves"), T(e, "hoy", frase=3), T(e, "estacion"), T(e, "1911")
    t_gug, t_fun, t_cob, t_cerr, t_1925, t_dej, t_cdlg = (T(e, "guggenheim"), T(e, "fundicion"), T(e, "cobre"), T(e, "cerro", frase=4),
                                                         T(e, "1925"), T(e, "dejo"), T(e, "cerro de la grasa"))
    t_1885, t_tea, t_1896, t_1908, t_tem, t_cup, t_esti = (T(e, "1885"), T(e, "teatro"), T(e, "1896"), T(e, "1908"),
                                                           T(e, "templo", frase=5), T(e, "cupulas"), T(e, "estilos"))
    estilos = [(T(e, w), txt) for w, txt in (("neoclasico", "NEOCLÁSICO"), ("barroco", "BARROCO"), ("gotico", "GÓTICO"),
                                              ("arabe", "ÁRABE"), ("ruso", "RUSO"))]
    t_todo, t_f7, t_ref, t_sin, t_uni, t_1985, t_desp = (T(e, "todo"), INI(e, 7), T(e, "refugio"), T(e, "sin titulo"),
                                                         T(e, "universidad"), T(e, "1985"), T(e, "despues"))
    t_lado, t_musa, t_sat, t_pin, t_1887 = INI(e, 8), T(e, "museo", frase=8), T(e, "saturnino"), T(e, "pintor"), T(e, "1887")
    t_f9, t_31, t_ter, t_tri, t_nue = INI(e, 9), T(e, "31"), T(e, "terminar"), T(e, "triptico"), T(e, "nuestros")
    est, pp = CI["estacion"], CI["plaza_patria"]
    TREN = M.RUTAS["tren"]

    R.camara(i0 - 0.2, *foco(-102.29, 21.88, 3.0))
    R.camara(t_tren, -102.05, 21.85, 0.78)
    R.camara(t_fro, -102.2, 21.98, 0.86)
    R.camara(t_emp + 0.5, *foco(est[0], est[1], 5.0))
    R.camara(t_loc, *foco(est[0] - 0.002, est[1], 4.3))
    R.camara(t_ciu + 0.3, *foco(est[0] - 0.004, est[1], 3.7))
    R.camara(t_comp_cam(e), *foco(est[0], est[1], 5.3))
    R.camara(t_gug + 0.4, *foco(FUNDICION[0], FUNDICION[1], 4.6))
    R.camara(t_cdlg, *foco(FUNDICION[0] - 0.002, FUNDICION[1], 5.0))
    R.camara(t_tea - 0.3, *foco(pp[0] + 0.002, pp[1], 5.2))
    R.camara(t_esti, *foco(pp[0] + 0.004, pp[1] + 0.002, 5.6))
    R.camara(t_f7, *foco(SAN_ANTONIO[0], SAN_ANTONIO[1], 5.0))
    R.camara(t_lado + 0.3, *foco(SAN_ANTONIO[0] - 0.003, SAN_ANTONIO[1], 5.4))
    R.camara(fin + 0.3, *foco(pp[0], pp[1], 5.0))

    anio(R, i0, 1884)
    # frase 0: el primer tren de pasajeros (1884)
    xl = lambda t: 900 + 170 * prog(t, i0, t_tren)
    pa(R, PO(0), xl, lambda t: 1000, 1.15, i0 - 0.1, t_tren - 0.25, entra="izq", dx=1300, sale="der_fuera", d_out=0.6, sem=S(), z=2)
    for k in range(4):                                   # humo de la chimenea (la locomotora mira a la derecha)
        tb = i0 + 0.45 + 0.42 * k
        humo_pant(R, lambda t: xl(t) + 120, lambda t: 560, tb, dur=1.5, s=0.42, n=1 + k % 2)
    R.sello(t_lle, "locomotora", "PORFIRIATO", color=(196, 146, 68))
    R.ruta(TREN, t_tren - 0.2, 4.6, ancho=6.0, dash=18, hueco=10, t1=t_cam + 1.2)
    camino = R.camino_pos(tramo(TREN, CI["leon"], (-102.42, 22.58)), t_tren, 5.2)
    R.act(PO(0), pos_geo=camino, off=(0, -6), s=0.72, t_in=t_tren - 0.1, d_in=0.3, entra="pop", sem=S(), zs=0.4, z=4,
          t_out=t_cam + 0.6, flip=True)
    for k in range(11):
        tb = t_tren + 0.2 + 0.5 * k
        humo_geo(R, camino(tb), tb, dur=1.4, s=0.26, off0=(-20, -110), deriva=(40, -110), n=1 + k % 2)
    R.snd(t_tren - 0.1, "tren", 0.45)
    pa(R, XI(1), 300, 1010, 0.9, t_pas - 0.15, t_cam + 0.2, sem=S())
    pa(R, XI(2), 500, 1010, 0.92, t_pas + 0.1, t_cam + 0.2, sem=S())
    ciudad(R, t_pas + 0.3, t_cam, "aguascalientes", "AGUASCALIENTES", "der", 36)
    titulo(R, t_fc - 0.1, t_fro - 0.15, "FERROCARRIL CENTRAL · 1884", x=1360, y=420, px=58, snd=True)
    lugar(R, t_cdmx, t_cam, "DESDE LA CIUDAD DE MÉXICO", TREN[0], off=(-150, -60), px=38)
    lugar(R, t_fro, t_cam + 0.4, "HACIA LA FRONTERA", CI["zacatecas"], off=(-250, 10), px=38)

    # frase 1: los talleres (80 ha)
    anio(R, t_cam, 1900)
    for k, (dx, dy, s) in enumerate(((0, 0, 0.62), (-250, 30, 0.48), (250, 26, 0.48))):
        ga(R, PO(4), est, t_tal - 0.2 + 0.18 * k, t_gug - 0.3, s=s, off=(dx, dy), sem=S(), zs=0.4, z=1 + (k == 0), entra="sube", dy=260,
           extra=[(0.05, "crece", 0.4)] if k == 0 else ())
    R.contador(t_80 - 0.3, t_80 + 0.5, 0, 80, (960, 196), px=78, formato="{} HECTÁREAS", hasta_t=t_con + 0.8)
    pa(R, PO(3), 330, 1010, 1.0, t_emp - 0.15, t_hoy - 0.2, sem=S())
    R.snd(t_con, "golpe_suave", 0.35)
    pa(R, PO(0), 1600, 1010, 0.72, t_loc - 0.2, t_nav - 0.3, sem=S(), flip=True, extra=[(0.1, "crujido", 0.3)])

    # frase 2: ciudad ferrocarrilera
    R.terreno(t_ags - 0.1, "metro", COL["porfiriato"], 1.0, capa=20)
    titulo(R, t_ciu - 0.2, t_nav - 0.2, "CIUDAD FERROCARRILERA", px=80)
    for k in range(6):
        tb = t_ags - 0.2 + 0.45 * k
        humo_geo(R, est, tb, dur=1.6, s=0.32, off0=((k % 3 - 1) * 230, -150), deriva=(-50, -150), n=1 + k % 2, z=2)

    # frase 3: hoy, Complejo Ferrocarrilero Tres Centurias (se puede visitar)
    pa(R, FP.F("porfiriato_3"), 1520, 1010, FP.s_para(0.46), t_nav - 0.2, t_1911 + 0.9, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_hoy - 0.1, t_gug - 0.3, "HOY: COMPLEJO FERROCARRILERO TRES CENTURIAS", px=54, snd=True)
    pa(R, PO(0), 380, 1010, 0.8, t_hoy - 0.1, t_gug - 0.2, sem=S())
    ciudad(R, t_est - 0.1, t_gug - 0.2, "estacion", None)
    lugar(R, t_est, t_gug - 0.2, "ESTACIÓN DE 1911", est, off=(0, 105), px=40)
    R.terreno(t_gug - 0.4, None, COL["porfiriato"], 0.6, capa=20)

    # frase 4: los Guggenheim, la fundición y el Cerro de la Grasa
    pa(R, XI(2), 330, 1010, 1.0, t_gug - 0.2, t_dej + 0.4, sem=S())
    R.texto(t_gug, t_1925, "LOS GUGGENHEIM", (330, 560), px=44, d=0.4)
    ga(R, PO(5), FUNDICION, t_fun - 0.2, t_cerr + 0.3, s=0.55, off=(-150, 60), sem=S(), zs=0.4, z=2, entra="sube", dy=280,
       extra=[(0.05, "fuego", 0.35, {"dur": 1.2})])
    for k in range(4):
        tb = t_fun + 0.1 + 0.42 * k
        humo_geo(R, FUNDICION, tb, dur=1.5, s=0.3, off0=(-205, -260), deriva=(-50, -90), n=1 + k % 2, z=3)
    titulo(R, t_cob - 0.1, t_cerr - 0.1, "COBRE Y PLOMO", x=1300, px=80)
    pa(R, PL(7), 1600, 1010, 0.62, t_cob - 0.1, t_1925 + 0.3, sem=S(), extra=[(0.05, "monedas", 0.35)])
    anio(R, t_1925, 1925)
    R.snd(t_cerr + 0.3, "golpe_suave", 0.4)
    ga(R, Crece(PO(6), t_dej - 0.2, t_cdlg + 0.6, 0.15), FUNDICION, t_dej - 0.25, t_1885 - 0.2, s=0.7, off=(-120, 150), sem=S(), zs=0.4,
       z=2, entra="fija", d_in=0.05, extra=[(0.05, "crece", 0.4, {"dur": 2.0})])
    titulo(R, t_cdlg - 0.1, t_1885 - 0.2, "CERRO DE LA GRASA", px=84, snd=True)
    pa(R, PO(3), 1600, 1010, 0.95, t_dej + 0.6, t_1885 - 0.1, sem=S(), flip=True)

    # frase 5: Teatro Morelos (1885) y templo de San Antonio (1896-1908)
    anio(R, t_1885, 1885)
    pa(R, XI(1), 1480, 1010, 0.95, t_1885 - 0.15, t_1896, sem=S())
    pa(R, XI(2), 1660, 1010, 0.98, t_1885 + 0.15, t_1896, sem=S())
    ga(R, PO(7), pp, t_tea - 0.15, estilos[0][0] - 0.3, s=0.55, off=(-270, 0), sem=S(), zs=0.4, z=2, entra="sube", dy=260,
       extra=[(0.05, "pluck", 0.35)])
    ciudad(R, t_tea, t_1908, "plaza_patria", None)
    lugar(R, t_tea + 0.1, t_1908, "TEATRO MORELOS", pp, off=(-270, 50), px=38)
    anio(R, t_1896, 1896)
    R.anio(t_1908, 1908)
    _ULT[0] = 1908
    ga(R, PO(8), SAN_ANTONIO, t_tem - 0.15, estilos[0][0] - 0.3, s=0.55, off=(250, -10), sem=S(), zs=0.4, z=2, entra="sube", dy=280,
       extra=[(0.05, "campana", 0.4)])
    lugar(R, t_tem + 0.2, estilos[0][0] - 0.3, "SAN ANTONIO", SAN_ANTONIO, off=(250, 50), px=38)
    pa(R, FP.F("porfiriato_5"), 400, 1010, FP.s_para(0.5), t_cup - 0.2, estilos[2][0] + 0.4, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_esti - 0.1, estilos[0][0] - 0.2, "ESTILOS DE MEDIO MUNDO", px=78)

    # frase 6: neoclásico, barroco, gótico, árabe y ruso
    pa(R, PO(8), 960, 1010, 1.25, estilos[0][0] - 0.35, t_f7 - 0.1, sem=S(), entra="sube", dy=380)
    for k, (t_, txt) in enumerate(estilos):
        R.texto(t_ - 0.05, t_f7 - 0.15, txt, (1560, 330 + 120 * k), px=58, d=0.35)
        R.snd(t_ - 0.05, "pop", 0.35, tono=0.85 + 0.12 * k)
    pa(R, CO(3), 330, 1010, 0.95, estilos[3][0] - 0.1, t_f7, sem=S())
    titulo(R, t_todo - 0.1, t_f7 - 0.15, "TODO EN EL MISMO TEMPLO", px=70)

    # frase 7: Refugio Reyes, arquitecto sin título
    pa(R, PO(9), 330, 1010, 1.0, t_f7 - 0.15, t_lado + 0.3, sem=S())
    R.texto(t_ref, t_sin - 0.15, "REFUGIO REYES", (330, 560), px=44, d=0.4)
    R.texto(t_sin, t_lado + 0.2, "SIN TÍTULO", (330, 560), px=48, d=0.4)
    ga(R, PO(8), SAN_ANTONIO, t_f7 - 0.1, t_sat - 0.2, s=0.6, off=(190, -10), sem=S(), zs=0.4, z=2)
    pa(R, FU(3), 720, 1010, 0.82, t_uni - 0.15, t_lado + 0.2, sem=S(), entra="sube", dy=300, extra=[(0.05, "papel", 0.4)])
    titulo(R, t_1985 - 0.1, t_lado - 0.1, "TÍTULO… EN 1985", px=80, snd=True)
    pa(R, FU(6), 1600, 1010, 0.6, t_desp - 0.1, t_lado + 0.3, sem=S())

    # frase 8: Museo de Aguascalientes, Saturnino Herrán (1887)
    ciudad(R, t_musa - 0.1, t_sat - 0.2, "plaza_patria", None)
    lugar(R, t_musa - 0.1, t_sat - 0.35, "HOY: MUSEO DE AGUASCALIENTES", SAN_ANTONIO, off=(150, 60), px=40)
    pa(R, AR(5), 330, 1010, 1.0, t_musa, t_ter + 0.5, sem=S(), sale="baja", d_out=0.7)
    pa(R, FP.F("porfiriato_8"), 1580, 1010, FP.s_para(0.52), t_sat - 0.25, t_f9 + 0.4, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_sat, t_f9 - 0.2, "SATURNINO HERRÁN", px=80, snd=True)
    anio(R, t_1887, 1887)
    ga(R, PO(8), SAN_ANTONIO, t_sat - 0.1, t_ter - 0.2, s=0.5, off=(-60, -10), sem=S(), zs=0.4, z=1)

    # frase 9: murió a los 31, sin terminar Nuestros dioses
    R.texto(t_31 - 0.1, t_ter + 0.4, "† A LOS 31 AÑOS", (330, 560), px=46, d=0.4)
    R.snd(t_31, "golpe_suave", 0.35)
    pa(R, AR(6), 960, 1010, 1.0, t_ter - 0.15, fin + 0.3, sem=S(), extra=[(0.05, "pincel", 0.35)])
    R.texto(t_ter, t_nue - 0.2, "SIN TERMINAR", (960, 196), px=74, d=0.5)
    pa(R, FP.F("porfiriato_9"), 1540, 1010, FP.s_para(0.5), t_tri - 0.25, fin + 0.35, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_nue - 0.1, fin + 0.3, "«NUESTROS DIOSES»", px=78)


def t_comp_cam(e):
    return T(e, "complejo")


# ------------------------------------------------------------------ CONVENCIÓN
def _convencion(R):
    e = "convencion"
    i0, fin = INI(e), FIN(e)
    t_1914, t_rev, t_vic, t_hue, t_gan, t_acu = (T(e, "1914"), T(e, "revolucion"), T(e, "victoriano"), T(e, "huerta"),
                                                 T(e, "ganadores"), T(e, "acuerdo"))
    t_10, t_del, t_lug, t_tea = T(e, "10"), T(e, "delegados", frase=1), T(e, "lugar"), T(e, "teatro", frase=1)
    t_14, t_sob, t_fir, t_jur, t_cum = T(e, "14"), T(e, "soberana"), T(e, "firmaron"), T(e, "jurar"), T(e, "cumplirian")
    t_17, t_vil, t_fir2, t_abr, t_tes = T(e, "17"), T(e, "pancho"), T(e, "firmo"), T(e, "abrazo"), T(e, "testigo")
    t_ya, t_pero, t_hab, t_bal = INI(e, 5), T(e, "pero", frase=5), T(e, "habra"), T(e, "balazos")
    t_zap, t_man, t_ant, t_tom, t_ban6, t_sim = (INI(e, 6), T(e, "mando"), T(e, "antonio"), T(e, "tomo"), T(e, "bandera", frase=6),
                                                 T(e, "simbolo"))
    t_f7, t_ech, t_casi = INI(e, 7), T(e, "echaron"), T(e, "casi")
    t_f8, t_pre, t_eul, t_rom, t_carr2, t_otra, t_revs = (INI(e, 8), T(e, "presidente"), T(e, "eulalio"), T(e, "rompio"),
                                                          T(e, "carranza", frase=8), T(e, "otra", frase=8),
                                                          T(e, "revolucionarios", frase=8))
    t_gue = T(e, "guerra", frase=8)
    t_f9, t_sig, t_pla = INI(e, 9), T(e, "sigue"), T(e, "plaza")
    pp, ags, zac, leon = CI["plaza_patria"], CI["aguascalientes"], CI["zacatecas"], CI["leon"]

    R.camara(i0 - 0.2, *foco(pp[0], pp[1], 4.6))
    R.camara(t_rev, -102.3, 22.0, 1.75)
    R.camara(t_acu, -102.25, 21.98, 1.85)
    R.camara(t_del, *foco(pp[0], pp[1], 5.0))
    R.camara(t_jur, *foco(pp[0] + 0.003, pp[1], 5.4))
    R.camara(t_17 - 0.5, *foco(pp[0], pp[1], 4.2))
    R.camara(t_17 + 0.5, -102.42, 22.45, 1.7)
    R.camara(t_fir2 + 0.2, *foco(ags[0], ags[1], 2.8))
    R.camara(t_abr - 0.2, *foco(pp[0], pp[1], 5.0))
    R.camara(t_man, *foco(pp[0] - 0.003, pp[1], 5.3))
    R.camara(t_f8, *foco(pp[0], pp[1], 5.0))
    R.camara(t_otra - 0.2, -102.15, 21.95, 1.0)
    R.camara(t_f9 - 0.3, -102.2, 21.9, 0.98)
    R.camara(t_pla - 0.4, *foco(pp[0], pp[1], 5.4, dy=230))
    R.camara(fin + 0.4, *foco(pp[0] + 0.002, pp[1], 5.6, dy=230))

    anio(R, t_1914, 1914)
    # frase 0: 1914, Huerta derrocado y los ganadores peleados
    R.terreno(i0 + 0.3, "aguascalientes", COL["revolucion"], 1.0, capa=20)
    pa(R, RV(2), 330, 1010, 1.0, i0 - 0.1, t_10 - 0.1, sem=S())
    R.sello(t_1914 + 0.5, "sombrero_rev", "REVOLUCIÓN", color=(198, 70, 60))
    pa(R, RV(5), 560, 1010, 0.95, t_rev - 0.15, t_10 - 0.1, sem=S())
    R.texto(t_vic - 0.1, t_acu - 0.2, "VICTORIANO HUERTA", (960, 196), px=78, d=0.6)
    tachar(R, t_hue + 0.45, t_acu - 0.2, "VICTORIANO HUERTA", (960, 196), 78, sem=3)
    pa(R, RV(0), 1380, 1010, 1.0, t_gan - 0.15, t_10 - 0.1, sem=S())
    pa(R, RV(1), 1620, 1010, 1.0, t_gan + 0.1, t_10 - 0.1, sem=S())
    pa(R, A.espadas(), 960, 900, 0.9, t_acu - 0.6, t_10 + 0.2, sem=S(), extra=[(0.05, "espada", 0.4)])
    R.terreno(t_10, None, COL["revolucion"], 0.6, capa=20)

    # frase 1: un lugar neutral, el Teatro Morelos
    titulo(R, t_10 - 0.1, t_lug - 0.2, "10 DE OCTUBRE · 9 DE NOVIEMBRE", px=66)
    for k, (dib, x0, x1, s) in enumerate(((RV(2), -150, 300, 0.85), (RV(6), -300, 500, 0.85), (RV(1), 2100, 1660, 0.85),
                                          (XI(2), 2250, 1460, 0.85))):
        tb = t_10 + 0.1 + 0.25 * k
        izq = x1 < 960
        t_sale = t_fir - 0.3 if izq else t_tea - 0.3
        pa(R, dib, lambda t, a=x0, b=x1, c=tb: a + (b - a) * e_out(prog(t, c, c + 2.2)), lambda t: 1010, s, tb, t_sale, entra="fija",
           d_in=0.05, sem=S(), z=4, flip=not izq, extra=[(0.0, "pasos", 0.3, {"dur": 1.2})] if k == 0 else ())
    pa(R, PO(7), 960, 1010, 1.2, t_lug - 0.2, t_fir - 0.3, sem=S(), z=1, entra="sube", dy=360, extra=[(0.05, "whoosh", 0.35)])
    titulo(R, t_lug, t_tea - 0.15, "LUGAR NEUTRAL", px=80)
    titulo(R, t_tea, t_14 - 0.15, "TEATRO MORELOS", px=84, snd=True)
    pa(R, FP.F("convencion_1"), 1540, 1010, FP.s_para(0.46), t_tea - 0.2, t_sob + 0.2, entra="pluma", d_in=0.6, sem=S())

    # frase 2: Soberana Convención y la bandera firmada
    titulo(R, t_14 - 0.1, t_sob - 0.2, "14 DE OCTUBRE", px=80)
    titulo(R, t_sob, t_jur - 0.2, "SOBERANA CONVENCIÓN REVOLUCIONARIA", px=62, snd=True)
    pa(R, RV(3), 960, 1010, 1.3, t_fir - 0.3, t_17 - 0.1, sem=S(), z=2, entra="sube", dy=380)
    firmas(R, t_fir, t_17 - 0.1, (850, 600, 1130, 830), 10, 2.8, sem=1)
    R.snd(t_fir, "escribir", 0.4, dur=2.6)
    pa(R, RV(1), 1600, 1010, 1.0, t_fir - 0.1, t_17 - 0.1, sem=S(), flip=True)

    # frase 3: un juramento
    titulo(R, t_jur + 0.15, t_17 - 0.2, "UN JURAMENTO", px=84)
    pa(R, FU(3), 1330, 1010, 0.58, t_cum - 0.1, t_17 - 0.1, sem=S(), z=3)

    # frase 4: 17 de octubre, llega Villa
    titulo(R, t_17 - 0.1, t_fir2 - 0.2, "17 DE OCTUBRE", x=520, px=84)
    vuelo = tramo(M.RUTAS["tren"], (-102.42, 22.58), ags)
    andar_ciclo(R, C_VILLA, vuelo, t_17 + 0.3, 2.6, t1=t_fir2 + 0.1, s=0.62, sem=S(), z=4, fps=12,
                extra=[(0.05, "galope", 0.45, {"dur": 2.4})])
    ciudad(R, t_17 + 0.2, t_fir2, "zacatecas", "ZACATECAS", "izq", 36)
    ciudad(R, t_17 + 0.6, t_fir2, "aguascalientes", "AGUASCALIENTES", "der", 36)
    R.texto(t_vil, t_fir2 - 0.1, "PANCHO VILLA", (520, 316), px=56, d=0.4)
    xv = lambda t: kf(t, [(t_fir2, 400.0), (t_abr, 400.0), (t_abr + 0.6, 760.0), (t_tes - 0.3, 760.0), (t_tes + 0.3, 400.0)])
    risa = lambda t: 1010 - 9 * abs(math.sin((t - t_ya) * 17)) * (t_ya < t < t_bal + 0.6)
    pa(R, RV(0), xv, risa, 1.05, t_fir2 - 0.15, t_zap - 0.2, sem=S(), z=4)
    pa(R, RV(3), 960, 1010, 0.9, t_fir2 - 0.1, t_abr - 0.35, sem=S(), z=2)
    firmas(R, t_fir2 + 0.2, t_abr - 0.35, (900, 700, 1080, 760), 1, 0.4, sem=7)
    R.snd(t_fir2 + 0.2, "escribir", 0.35, dur=0.5)
    xo = lambda t: kf(t, [(t_abr - 0.5, 2100.0), (t_abr, 1600.0), (t_abr + 0.6, 1160.0), (t_tes - 0.3, 1160.0), (t_tes + 0.3, 1600.0)])
    pa(R, RV(1), xo, lambda t: 1010, 1.0, t_abr - 0.5, t_zap - 0.2, entra="fija", d_in=0.05, sem=S(), z=4, flip=True)
    R.snd(t_abr + 0.55, "golpe_suave", 0.4)
    R.texto(t_abr + 0.1, t_tes - 0.3, "ABRAZO CON OBREGÓN", (960, 196), px=70, d=0.6)
    R.texto(t_tes - 0.2, t_ya - 0.1, "SEGÚN UN TESTIGO…", (960, 196), px=66, d=0.5)
    pa(R, RV(5), 960, 1010, 0.8, t_tes - 0.1, t_zap - 0.2, sem=S(), z=3)

    # frase 5: la cita de Villa
    R.texto(t_ya, fin_f(e, 5), "«YA LES FIRMÉ LA BANDERA…", (960, 180), px=70, d=0.8)
    R.texto(t_pero, fin_f(e, 5), "PERO SI SACAN OTRA VEZ A CARRANZA,", (960, 290), px=56, d=0.9)
    R.texto(t_hab - 0.1, fin_f(e, 5) + 0.2, "¡HABRÁ BALAZOS!»", (960, 404), px=84, d=0.5)
    R.snd(t_bal + 0.35, "balazos", 0.4)

    # frase 6: Zapata manda delegados; Soto y Gama toma la bandera
    titulo(R, t_zap + 0.45, t_ant - 0.2, "ZAPATA NO VINO", px=84)
    for k, x in enumerate((250, 450, 640)):
        pa(R, RV(2), x, 1010, 0.85, t_zap - 0.1 + 0.3 * k, t_ant if k else t_f8 - 0.3, sem=S(), z=4)
    pa(R, FP.F("convencion_6"), 1540, 1010, FP.s_para(0.42), t_man - 0.1, t_tom, entra="pluma", d_in=0.6, sem=S())
    titulo(R, t_ant, t_sim - 0.2, "ANTONIO DÍAZ SOTO Y GAMA", px=66, snd=True)
    pa(R, RV(7), 1000, 1010, 1.1, t_tom - 0.3, t_f8 - 0.2, sem=S(), z=2)
    pa(R, RV(3), 560, 1010, 0.8, t_ban6 - 0.1, t_f7 + 0.2, sem=S(), z=3, rot=-0.18, sale="caer", d_out=0.6)
    R.texto(t_sim - 0.1, t_casi - 0.2, "«SÍMBOLO DE LA REACCIÓN»", (960, 196), px=70, d=0.7)
    pa(R, RV(4), 1560, 1010, 1.0, t_sim, t_f8 - 0.2, sem=S(), z=3)

    # frase 7: se le echan encima
    R.snd(t_f7, "multitud", 0.45)
    for k, (dib, x0, x1) in enumerate(((RV(1), 2150, 1250), (XI(2), 2300, 1380), (PO(9), -250, 400), (PO(3), -400, 190))):
        tb = t_f7 - 0.1 + 0.18 * k
        pa(R, dib, lambda t, a=x0, b=x1, c=tb, j=k: a + (b - a) * e_out(prog(t, c, c + 1.0)) + 10 * math.sin(t * 13 + j),
           lambda t, j=k: 1010 - 8 * abs(math.sin(t * 11 + j * 1.7)), 0.92, tb, t_f8 - 0.2, entra="fija", d_in=0.05, sem=S(), z=5,
           flip=x1 > 960)
    titulo(R, t_casi - 0.1, t_f8 - 0.2, "CASI LE CUESTA LA VIDA", px=78)

    # frase 8: Eulalio Gutiérrez presidente; rompen con Carranza; otra guerra
    pa(R, RV(6), 330, 1010, 1.0, t_f8 - 0.1, t_otra - 0.2, sem=S(), extra=[(0.05, "tambor", 0.35, {"dur": 0.8})])
    R.texto(t_eul, t_otra - 0.3, "EULALIO GUTIÉRREZ", (330, 560), px=42, d=0.4)
    titulo(R, t_pre - 0.1, t_rom - 0.2, "PRESIDENTE", px=84)
    R.texto(t_rom - 0.1, t_otra - 0.3, "CARRANZA", (960, 196), px=84, d=0.5)
    tachar(R, t_carr2 + 0.3, t_otra - 0.3, "CARRANZA", (960, 196), 84, sem=4)
    pa(R, FP.F("convencion_8"), 1530, 1010, FP.s_para(0.40), t_eul - 0.15, t_otra - 0.2, entra="pluma", d_in=0.6, sem=S())
    R.terreno(t_otra - 0.4, "mexico_mod", COL["revolucion"], 1.2, capa=21)
    titulo(R, t_otra, t_f9 - 0.1, "OTRA GUERRA", x=1400, px=90)
    R.texto(t_revs - 0.5, t_f9 - 0.1, "ahora entre revolucionarios", (1400, 316), px=54, d=0.6)
    pa(R, A.espadas(), 960, 1000, 1.0, t_gue - 0.2, t_f9, sem=S(), extra=[(0.05, "canonazo", 0.4)])
    grupo_ciclo(R, C_SOLD, tramo(M.RUTAS["tren"], (-102.42, 22.5), ags), t_otra - 0.1, 3.4, n=3, ancho=95, t1=t_f9, s=0.75, sem=S(),
                extra=[(0.05, "pasos", 0.3, {"dur": 2.0})])
    _ = [S() for _ in range(3)]
    grupo_ciclo(R, C_SOLD, tramo(M.RUTAS["tren"], leon, ags), t_otra + 0.1, 3.4, n=3, ancho=95, t1=t_f9, s=0.75, sem=S())
    _ = [S() for _ in range(3)]
    pa(R, RV(0), 330, 1010, 1.0, t_otra - 0.1, t_f9, sem=S())
    pa(R, RV(1), 1600, 1010, 1.0, t_otra + 0.1, t_f9, sem=S(), flip=True)
    R.terreno(t_f9 + 0.3, None, COL["revolucion"], 0.8, capa=21)

    # frase 9: el teatro sigue en pie con el Museo de la Convención (se puede visitar)
    pa(R, RV(3), 360, 1010, 0.95, t_f9 - 0.1, fin + 0.4, sem=S())
    ga(R, PO(7), pp, t_f9 + 0.4, fin + 0.4, s=0.62, off=(-170, -6), sem=S(), zs=0.4, z=2, entra="sube", dy=260)
    titulo(R, t_sig - 0.1, fin + 0.4, "HOY: TEATRO MORELOS Y MUSEO DE LA CONVENCIÓN", px=54, snd=True)
    ciudad(R, t_pla, fin + 0.4, "plaza_patria", "PLAZA DE LA PATRIA", "abajo", 38)
    pa(R, FP.F("convencion_9"), 1540, 1010, FP.s_para(0.48), t_f9, fin + 0.4, entra="pluma", d_in=0.6, sem=S())
    R.terreno(fin + 0.35, None, COL["revolucion"], 0.3, capa=20)


def fin_f(e, i):
    return FIN(e, i) + 0.4
