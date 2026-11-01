# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (tequila, mariachi y charros; Alvarado, Hidalgo y el federalismo), orígenes (Xalisco, los
Guachimontones de la tradición Teuchitlán, las tumbas de tiro, caxcanes, tecuexes, cocas y wixárikas, la guerra del salitre con los
purépechas) y la conquista (Nuño de Guzmán, la Nueva Galicia, Guadalajara 1532, la guerra del Mixtón, Alvarado y el virrey Mendoza).
Dibujos = pegatinas de Flow (`coreo_peg`). Capas: 0 = territorio principal, 1-5 = pueblos / zonas, 50 = agua."""
import obj_c as C
from core import FIN, INI, T, kf
from coreo_peg import (C_CAXCAN, C_SOLDADO, CO, CQ, HO, IN, OC, PU, SI, XI, XX, andar_ciclo, ciclo_pant, grupo_ciclo)
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo
import mapa as M

MAR_TXT = (58, 108, 148)
TIERRA_TXT = (146, 110, 72)
EDO_TXT = (120, 96, 70)


def cortes(R):
    pass


def construir(R):
    _mares(R)
    _gancho(R)
    _origenes(R)
    _conquista(R)


def _mares(R):
    R.mar("mx", "OCÉANO PACÍFICO", -106.3, 19.4, 46, 0.44, rot=-0.35, color=MAR_TXT)
    R.mar("mx", "LAGO DE CHAPALA", -103.05, 20.12, 22, 0.42, color=MAR_TXT)
    R.mar("mx", "SIERRA MADRE OCCIDENTAL", -104.75, 22.75, 24, 0.32, rot=-0.95, color=TIERRA_TXT)
    R.mar("mx", "LOS ALTOS", -102.35, 21.15, 26, 0.32, color=TIERRA_TXT)
    R.mar("mx", "BAJÍO", -100.9, 20.75, 26, 0.30, color=TIERRA_TXT)
    for txt, lon, lat in (("NAYARIT", -104.95, 22.05), ("ZACATECAS", -102.75, 23.35), ("AGUASCALIENTES", -102.33, 22.12),
                          ("GUANAJUATO", -100.95, 21.15), ("MICHOACÁN", -101.85, 19.25), ("COLIMA", -103.95, 19.05)):
        R.mar("mx", txt, lon, lat, 22, 0.28, color=EDO_TXT)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    t_teq, t_mar, t_cha, t_mun, t_mex, t_sol = (T(e, "tequila"), T(e, "mariachi"), T(e, "charros"), T(e, "mundo"), T(e, "mexico"),
                                                T(e, "sola"))
    t_aqui, t_con, t_hid, t_esc, t_fed = T(e, "aqui"), T(e, "conquistador"), T(e, "hidalgo"), T(e, "esclavitud"), T(e, "federalismo")
    t_his, t_jal, t_cin = T(e, "historia"), T(e, "jalisco"), T(e, "cinco")

    # cámara: valle de Tequila de cerca -> el occidente entero -> Jalisco
    R.camara(0.0, -103.82, 20.86, 3.4)
    R.camara(t_mun - 0.2, -103.6, 20.8, 2.6)
    R.camara(t_sol + 0.4, -102.9, 20.8, 0.98)
    R.camara(t_aqui + 0.2, -103.4, 20.9, 1.25)
    R.camara(t_his + 0.3, -103.6, 20.7, 1.2)
    R.camara(FIN(e) + 0.6, -103.6, 20.7, 1.17)

    # frase 0: tequila, mariachi y charros
    for k, (dx, dy) in enumerate(((-260, -60), (-160, -30), (160, -35), (260, -65), (-210, 10), (210, 5))):
        ga(R, SI(4), CI["tequila"], 0.05 + 0.07 * k, t_mun + 0.2, s=0.30, off=(dx, dy), sem=1 + k, zs=0.5, z=1)
    ga(R, OC(5), CI["volcan_tequila"], 0.0, t_mun + 0.2, s=0.5, off=(0, -60), sem=8, zs=0.5, z=0, entra="sube", dy=300)
    pa(R, SI(1), 330, 1010, 0.95, t_teq - 0.1, t_aqui, sem=9, entra="sube", dy=320, extra=[(0.05, "pluck", 0.35)])
    pa(R, SI(2), 470, 1010, 0.42, t_teq + 0.2, t_aqui, sem=10)
    R.texto(t_teq, t_aqui - 0.1, "TEQUILA", (380, 560), px=56, d=0.4)
    pa(R, XX(4), 960, 1010, 1.0, t_mar - 0.1, t_aqui, sem=11, extra=[(0.05, "fanfarria", 0.32)])
    R.texto(t_mar, t_aqui - 0.1, "MARIACHI", (960, 560), px=56, d=0.4)
    pa(R, XX(5), 1590, 1010, 1.05, t_cha - 0.1, t_aqui, sem=12, extra=[(0.05, "galope", 0.35, {"dur": 0.8})])
    R.texto(t_cha, t_aqui - 0.1, "CHARROS", (1590, 560), px=56, d=0.4)
    R.terreno(t_mex - 0.2, "mexico_mod", COL["nueva_espana"], 0.8)
    R.terreno(t_sol - 0.1, "jalisco", COL["jalisco"], 0.9, capa=1)
    R.snd(t_sol - 0.1, "whoosh", 0.45, dur=0.8)
    R.texto(t_sol + 0.2, t_aqui - 0.1, "UNA SOLA TIERRA", (960, 196), px=74, d=0.6)

    # frase 1: un conquistador, Hidalgo y el federalismo
    pa(R, CQ(1), 330, 1010, 1.0, t_con - 0.1, FIN(e) + 0.5, sem=13, sale="caer", extra=[(0.05, "espada", 0.4)])
    pa(R, IN(0), 960, 1010, 1.0, t_hid - 0.1, FIN(e) + 0.5, sem=14)
    pa(R, IN(10), 1240, 1000, 0.5, t_esc - 0.1, FIN(e) + 0.5, sem=15, extra=[(0.05, "crujido", 0.4)])
    pa(R, XI(6), 1600, 1010, 0.62, t_fed - 0.15, t_cin - 0.2, sem=16, entra="sube", dy=300)
    R.texto(t_fed, t_his - 0.2, "FEDERALISMO", (1600, 680), px=50, d=0.4)

    # frase 2: título
    R.texto(t_his - 0.2, FIN(e) + 0.6, "LA HISTORIA DE JALISCO", (960, 178), px=96, d=0.9)
    R.texto(t_cin - 0.1, FIN(e) + 0.6, "en 5 minutos", (960, 296), px=74, d=0.6)
    R.snd(t_his - 0.2, "escribir", 0.45, dur=0.9)
    pa(R, lambda t: C.cronometro(round(kf(t, [(t_cin, 0.0), (FIN(e) + 0.8, 0.9)], ease=lambda u: u), 2)), 1640, 860, 0.85, t_cin - 0.1,
       FIN(e) + 0.6, sem=17, extra=[(0.08, "reloj_rapido", 0.4, {"dur": 1.1})])
    pa(R, SI(0), 1560, 640, 0.5, t_jal - 0.1, FIN(e) + 0.6, sem=18, entra="cae", dy=600)
    R.terreno(FIN(e) + 0.4, None, COL["nueva_espana"], 0.3)


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_nah, t_xal, t_sob, t_are = T(e, "nahuatl"), T(e, "xalisco"), T(e, "sobre"), T(e, "arena")
    t_hace, t_vol, t_tra, t_lev, t_gua, t_pir, t_uni = (T(e, "hace"), T(e, "volcan"), T(e, "tradicion"), T(e, "levanto"),
                                                        T(e, "guachimontones"), T(e, "piramides"), T(e, "unicas"))
    t_bajo, t_tum, t_ent, t_fig, t_esc, t_vid = (T(e, "bajo"), T(e, "tumbas"), T(e, "enterraban"), T(e, "figurillas"), T(e, "escenas"),
                                                 T(e, "vida"))
    t_sig, t_cax, t_tec, t_coc, t_wix, t_def, t_sal, t_pur = (T(e, "siglos"), T(e, "caxcanes"), T(e, "tecuexes"), T(e, "cocas"),
                                                              T(e, "wixarikas"), T(e, "defendieron"), T(e, "salinas"), T(e, "purepechas"))

    R.camara(i0 - 0.2, -103.6, 20.7, 1.17)
    R.camara(t_hace - 0.1, -103.6, 20.7, 1.25)
    R.camara(t_vol + 0.2, -103.83, 20.74, 3.6)
    R.camara(t_bajo - 0.1, -103.8, 20.72, 3.8)
    R.camara(t_bajo + 0.5, -103.9, 20.55, 1.9)
    R.camara(t_sig - 0.1, -103.7, 20.6, 1.8)
    R.camara(t_sig + 0.6, -103.4, 21.15, 1.3)
    R.camara(t_sal - 0.2, -103.2, 20.6, 1.4)
    R.camara(FIN(e) + 0.4, -102.9, 20.3, 1.3)

    R.sello(i0 + 0.3, "piramide_mx", "OCCIDENTE ANTIGUO", color=(196, 120, 62))
    # frase 0: Xalisco, sobre la arena
    R.terreno(i0, "jalisco", COL["jalisco"], 0.6)
    R.texto(t_xal - 0.1, t_hace - 0.2, "XALISCO", (960, 190), px=104, d=0.6)
    R.snd(t_xal - 0.1, "escribir", 0.4, dur=0.6)
    R.texto(t_sob, t_hace - 0.2, "«sobre la arena»", (960, 312), px=64, d=0.6)
    R.terreno(t_hace + 0.2, None, COL["jalisco"], 0.6)
    pa(R, PU(2), 320, 1010, 0.95, i0 + 0.1, t_hace + 0.2, sem=20)
    pa(R, PU(5), 1600, 1010, 0.8, t_sob - 0.2, t_hace + 0.2, sem=21)
    pa(R, OC(7), 960, 1010, 0.55, t_are - 0.2, t_hace + 0.2, sem=22, entra="sube", dy=260, extra=[(0.05, "pluck", 0.3)])

    # frase 1: Guachimontones
    R.anio(t_hace, -300)
    R.terreno(t_tra - 0.1, "teuchitlan", COL["teuchitlan"], 1.0, capa=1)
    ga(R, OC(5), CI["volcan_tequila"], t_vol - 0.1, t_bajo + 0.6, s=0.5, off=(560, 60), sem=23, zs=0.4, z=0, entra="sube", dy=320,
       extra=[(0.05, "crece", 0.4)])
    lugar(R, t_vol + 0.2, t_tra - 0.1, "VOLCÁN DE TEQUILA", CI["volcan_tequila"], off=(560, 110), px=40)
    ga(R, OC(0), CI["guachimontones"], t_lev - 0.1, t_bajo + 0.6, s=0.72, off=(0, 170), sem=24, zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "crece", 0.45, {"dur": 0.9})])
    ga(R, OC(0), CI["guachimontones"], t_lev + 0.15, t_bajo + 0.6, s=0.45, off=(-300, 210), sem=25, zs=0.4, z=1)
    ga(R, OC(0), CI["guachimontones"], t_lev + 0.3, t_bajo + 0.6, s=0.40, off=(300, 220), sem=26, zs=0.4, z=1)
    titulo(R, t_gua - 0.1, t_bajo - 0.1, "GUACHIMONTONES", px=82, snd=True)
    R.texto(t_pir, t_bajo - 0.1, "pirámides redondas", (960, 300), px=56, d=0.5)
    pa(R, PU(1), 300, 1010, 0.95, t_tra, t_bajo, sem=27)
    pa(R, OC(4), 1620, 1010, 0.62, t_uni - 0.1, t_bajo + 0.2, sem=28)

    # frase 2: tumbas de tiro y figurillas
    R.terreno(t_tum - 0.1, "tumbas", COL["tumbas"], 1.1, capa=2)
    pa(R, OC(1), 960, 1010, 1.05, t_tum - 0.15, t_sig - 0.1, sem=29, entra="sube", dy=340, extra=[(0.05, "crujido", 0.35)])
    titulo(R, t_tum, t_sig - 0.15, "TUMBAS DE TIRO", px=78)
    pa(R, OC(2), 330, 1010, 0.78, t_fig - 0.1, t_sig - 0.1, sem=30, extra=[(0.05, "pluck", 0.3)])
    pa(R, OC(3), 1590, 1010, 0.9, t_fig + 0.15, t_sig - 0.1, sem=31)
    pa(R, OC(4), 600, 1010, 0.5, t_vid - 0.2, t_sig - 0.1, sem=32)
    R.texto(t_fig + 0.1, t_sig - 0.2, "figurillas de barro", (960, 300), px=52, d=0.5)
    R.terreno(t_sig - 0.2, None, COL["tumbas"], 0.4, capa=2)
    R.terreno(t_sig - 0.2, None, COL["teuchitlan"], 0.4, capa=1)

    # frase 3: los pueblos y las salinas
    R.anio(t_sig, 1480)
    for capa, (t_, campo, col, dib, n, geo) in enumerate((
            (t_cax, "caxcanes", COL["caxcanes"], PU(0), "CAXCANES", (-103.15, 21.75)),
            (t_tec, "tecuexes", COL["tecuexes"], PU(1), "TECUEXES", (-102.8, 20.85)),
            (t_coc, "cocas", COL["cocas"], PU(2), "COCAS", (-103.35, 20.38)),
            (t_wix, "wixarika", COL["wixarika"], PU(3), "WIXÁRIKAS", (-103.95, 21.95))), start=1):
        R.terreno(t_ - 0.15, campo, col, 0.8, capa=capa)
        ga(R, dib, geo, t_ - 0.1, FIN(e) + 0.2, s=0.62, off=(0, 40), sem=33 + capa, zs=0.4, z=2)
        lugar(R, t_, FIN(e) + 0.1, n, geo, off=(0, 84), px=40)
    R.terreno(t_sal - 0.2, "salinas", (236, 232, 220), 0.6, capa=5)
    ga(R, OC(7), CI["sayula"], t_sal - 0.15, FIN(e) + 0.2, s=0.42, off=(-90, 70), sem=38, zs=0.4, z=2, extra=[(0.05, "pluck", 0.3)])
    lugar(R, t_sal, FIN(e) + 0.1, "SALINAS DE SAYULA", CI["sayula"], off=(0, 80), px=38)
    R.terreno(t_pur - 0.2, "purepecha", COL["purepecha"], 0.9, capa=6)
    lugar(R, t_pur, FIN(e) + 0.1, "PURÉPECHAS", (-101.9, 19.65), off=(0, 0), px=44)
    for k in range(3):
        R.act(PU(4), pos_geo=R.camino_pos([(-101.9, 19.6), (-102.75, 19.75)], t_pur - 0.3 + 0.15 * k, 2.2), off=((k - 1) * 95, (k % 2) * 30),
              s=0.55, t_in=t_pur - 0.3 + 0.15 * k, d_in=0.35, entra="pop", sem=40 + k, zs=0.4, z=3, flip=True)
    R.snd(t_pur, "tambor", 0.4, dur=1.2)
    for c in range(1, 7):
        R.terreno(FIN(e) + 0.35, None, (0, 0, 0), 0.3, capa=c)


# ------------------------------------------------------------------ CONQUISTA
def _conquista(R):
    e = "conquista"
    i0 = INI(e)
    t_mil0, t_nun, t_cru, t_que, t_her = T(e, "mil"), T(e, "nuno"), T(e, "crueles"), T(e, "quemando"), T(e, "herrando")
    t_rei, t_gal, t_mil1, t_fun, t_gdl = T(e, "reino"), T(e, "galicia"), T(e, "mil", frase=1), T(e, "fundan"), T(e, "guadalajara")
    t_mil2, t_cax, t_cer, t_mix, t_ten = T(e, "mil", frase=2), T(e, "caxcanes"), T(e, "cerro"), T(e, "mixton"), T(e, "tenamaxtli")
    t_tem, t_alv, t_apl, t_mue, t_cab, t_ret = (T(e, "temido"), T(e, "alvarado"), T(e, "aplastarlos"), T(e, "muere"), T(e, "caballo"),
                                                T(e, "retirada"))
    t_vir, t_men, t_dec, t_ali, t_apa = T(e, "virrey"), T(e, "mendoza"), T(e, "decenas"), T(e, "aliados"), T(e, "apagar")

    R.camara(i0 - 0.2, -103.0, 20.9, 1.05)
    R.camara(t_her + 0.3, -103.6, 21.3, 1.0)
    R.camara(t_gdl - 0.2, -103.1, 21.1, 1.6)
    R.camara(t_mil2 - 0.1, -103.05, 21.3, 1.9)
    R.camara(t_mix + 0.2, -103.05, 21.3, 2.3)
    R.camara(t_tem + 0.3, -103.0, 21.15, 2.1)
    R.camara(t_vir - 0.1, -102.2, 20.9, 1.15)
    R.camara(FIN(e) + 0.4, -102.6, 21.0, 1.2)

    R.anio(i0, 1530)
    R.sello(t_nun, "espadas", "CONQUISTA", color=(176, 52, 48))
    # frase 0: Nuño de Guzmán
    R.ruta(M.RUTAS["guzman"], t_mil0, 3.2, ancho=4.5, t1=t_gal - 0.2, flecha=True)
    R.terreno(t_mil0 + 0.3, "guzman", COL["guzman"], 2.8)
    grupo_ciclo(R, C_SOLDADO, M.RUTAS["guzman"], t_mil0 + 0.1, 3.6, n=3, ancho=80, t1=t_gal, s=0.5, sem=50,
                extra=[(0.05, "pasos", 0.3, {"dur": 1.6})])
    pa(R, CQ(0), 320, 1010, 1.05, t_nun - 0.1, t_rei - 0.1, sem=53, extra=[(0.05, "espada", 0.35)])
    R.texto(t_nun + 0.1, t_rei - 0.2, "NUÑO DE GUZMÁN", (320, 560), px=46, d=0.4)
    ciudad(R, t_que - 0.2, t_gal, "tonala", "TONALÁ", "abajo", 40)
    for k, g in enumerate(("tonala", "tequila", "tepic")):
        ga(R, CQ(6), CI[g], t_que + 0.12 * k, t_rei, s=0.36, off=(30, -10), sem=54 + k, zs=0.4, z=2,
           extra=[(0.05, "fuego", 0.3, {"dur": 1.0})] if k == 0 else ())
    pa(R, CQ(7), 1600, 1010, 0.7, t_her - 0.15, t_rei - 0.1, sem=57, extra=[(0.05, "golpe_suave", 0.4)])

    # frase 1: Nueva Galicia y Guadalajara (1532)
    R.terreno(t_rei - 0.1, "nueva_galicia", COL["nueva_galicia"], 1.4)
    R.terreno(t_rei + 0.2, None, COL["guzman"], 0.01)
    titulo(R, t_gal - 0.1, t_mil2 - 0.2, "REINO DE LA NUEVA GALICIA", px=74, snd=True)
    R.anio(t_mil1, 1532)
    ciudad(R, t_fun - 0.1, t_mil2 - 0.1, "nochistlan", "GUADALAJARA (1532)", "der", 40)
    ga(R, SI(7), CI["nochistlan"], t_fun, t_mil2 - 0.1, s=0.5, off=(0, -20), sem=58, zs=0.4, z=2)
    pa(R, CQ(3), 320, 1010, 0.95, t_rei, t_cax, sem=59)
    pa(R, CQ(4), 1600, 1010, 0.95, t_fun - 0.2, t_cax, sem=60, flip=True)

    # frase 2: el Mixtón y Tenamaxtli
    R.anio(t_mil2, 1541)
    R.terreno(t_cax - 0.2, "caxcanes", COL["mixton"], 0.9, capa=1)
    lugar(R, t_cer, t_tem + 0.4, "CERRO DEL MIXTÓN", CI["mixton"], off=(0, -265), px=42)
    ga(R, OC(5), CI["mixton"], t_cer - 0.15, t_vir, s=0.5, off=(0, 10), sem=61, zs=0.4, z=1, entra="sube", dy=260)
    for k, (dx, dy, n) in enumerate(((-170, 175, 0), (-60, 205, 7), (60, 200, 0), (170, 170, 0))):
        ga(R, PU(n), CI["mixton"], t_cax + 0.1 * k, t_vir, s=0.5, off=(dx, dy), sem=80 + k, zs=0.4, z=2,
           extra=[(0.05, "cuerno", 0.35)] if k == 0 else ())
    ga(R, CQ(6), CI["tlacotan"], t_mix + 0.8, t_vir, s=0.45, off=(-90, -20), sem=84, zs=0.4, z=2, extra=[(0.05, "fuego", 0.3, {"dur": 1.0})])
    ciudad(R, t_mix + 0.6, t_vir, "tlacotan", "GUADALAJARA", "der", 38)
    grupo_ciclo(R, C_CAXCAN, M.RUTAS["caxcanes_ataque"], t_mix, 3.4, n=4, ancho=70, t1=t_vir, s=0.48, sem=62, fps=12,
                extra=[(0.05, "tambor", 0.4, {"dur": 1.4})])
    pa(R, PU(7), 1600, 1010, 1.1, t_ten - 0.15, t_alv + 0.6, sem=66, extra=[(0.05, "cuerno", 0.4)])
    R.texto(t_ten + 0.1, t_alv + 0.5, "TENAMAXTLI", (1600, 540), px=48, d=0.4)

    # frase 3: Alvarado
    pa(R, CQ(1), 330, 1010, 1.05, t_alv - 0.15, t_cab + 0.25, sem=67, sale="caer", d_out=0.6)
    R.texto(t_alv + 0.05, t_mue, "PEDRO DE ALVARADO", (330, 560), px=44, d=0.4)
    R.ruta(M.RUTAS["alvarado"], t_apl - 0.2, 1.4, ancho=4.5, t1=t_vir, flecha=True)
    R.snd(t_cab + 0.25, "impacto", 0.5)
    R.texto(t_mue + 0.1, t_vir - 0.1, "† 1541", (330, 470), px=64, d=0.4)

    # frase 4: el virrey Mendoza y los aliados indígenas
    pa(R, CQ(2), 330, 1010, 1.05, t_vir - 0.1, FIN(e) + 0.3, sem=68, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_men, FIN(e) + 0.2, "VIRREY MENDOZA", (330, 560), px=44, d=0.4)
    R.ruta(M.RUTAS["mendoza"], t_vir, 3.0, ancho=5.0, t1=FIN(e) + 0.2, flecha=True)
    for k in range(5):
        R.act(CQ(5), pos_geo=R.camino_pos(M.RUTAS["mendoza"], t_dec - 0.3 + 0.18 * k, 3.2), off=((k % 3 - 1) * 60, (k % 2) * 30),
              s=0.48, t_in=t_dec - 0.3 + 0.18 * k, d_in=0.35, entra="pop", sem=70 + k, zs=0.4, z=3)
    grupo_ciclo(R, C_SOLDADO, M.RUTAS["mendoza"], t_vir + 0.2, 3.4, n=2, ancho=70, s=0.48, sem=76)
    R.contador(t_dec - 0.2, FIN(e) + 0.2, 0, 50000, (1350, 196), px=74, formato="{:,} ALIADOS", hasta_t=t_ali + 0.2)
    pa(R, CQ(5), 1600, 1010, 1.0, t_ali - 0.2, FIN(e) + 0.3, sem=78, flip=True)
    R.terreno(t_apa - 0.1, None, COL["mixton"], 0.8, capa=1)
    R.snd(t_apa, "canonazo", 0.4)
