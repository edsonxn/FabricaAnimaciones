# -*- coding: utf-8 -*-
"""Coreografía (1/4): gancho (16 soldados y 2 vecinos → 8 millones en la feria; labios, Villa y la Catrina), orígenes (cazadores,
El Ocote, guamares, guachichiles, zacatecos, caxcanes y tecuexes = «chichimecas», la leyenda del Cerro del Muerto), la plata
(Tolosa 1546, Camino Real de Tierra Adentro, Guerra Chichimeca, presidios) y la fundación (22-oct-1575, Orozco, Montoro y 12 vecinos
de Lagos, el nombre larguísimo, el charco termal, el censo de 1584).
Dibujos = pegatinas de Flow (`pegflow.P`), fotos reales = `foto_peg.FotoPeg`. Capas de terreno: 0 = principal, 1-9 = pueblos/zonas.
Semillas 1-299."""
import foto_peg as FP
import mapa as M
import obj_a as A
from core import FIN, INI, T
from coreo_peg import andar_ciclo, grupo_ciclo
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo
from pegflow import P, ciclo

CH = lambda n, **k: P("01_chichimecas_hoja", n, **k)   # 0 arquero guachichil, 1 guamar, 2 madre, 3 cazador, 4 sacerdote, 5 fogata, 6 nopal, 7 roca pintada
PL = lambda n, **k: P("02_plata_hoja", n, **k)         # 0 carreta, 1 soldado, 2 presidio, 3 mula, 4 minero, 5 jinete chichimeca, 6 rueda, 7 plata
FU = lambda n, **k: P("03_fundacion_hoja", n, **k)     # 0 oidor, 1 colono, 2 colona, 3 carta, 4 poza termal, 5 jacal, 6 cruz, 7 estandarte
XI = lambda n, **k: P("05_xix_hoja", n, **k)           # 6 escudo con labios
AR = lambda n, **k: P("06_arte_hoja", n, **k)          # 2 catrina
PO = lambda n, **k: P("07_porfiriato_hoja", n, **k)    # 7 teatro
RV = lambda n, **k: P("08_revolucion_hoja", n, **k)    # 0 Villa
TU = lambda n, **k: P("10_turismo_hoja", n, **k)       # 0 turista, 1 familia, 4 rueda de la fortuna
C_CHI = ciclo("11_chichimeca_corre")
C_SOL = ciclo("12_soldado_marcha")
C_CAR = [f for f in ciclo("13_carreta_camina")]

MAR_TXT = (58, 108, 148)
TIERRA_TXT = (146, 110, 72)
EDO_TXT = (120, 96, 70)
AGS = CI["aguascalientes"]


def cortes(R):
    pass


def construir(R):
    _rotulos(R)
    _gancho(R)
    _origenes(R)
    _plata(R)
    _fundacion(R)


def _rotulos(R):
    R.mar("mx", "SIERRA FRÍA", -102.62, 22.18, 24, 0.32, rot=-0.5, color=TIERRA_TXT)
    R.mar("mx", "SIERRA DEL LAUREL", -102.78, 21.68, 22, 0.30, rot=-1.0, color=TIERRA_TXT)
    R.mar("mx", "LOS ALTOS", -102.2, 21.25, 24, 0.30, color=TIERRA_TXT)
    R.mar("mx", "PRESA CALLES", -102.45, 22.11, 16, 0.38, color=MAR_TXT)
    for txt, lon, lat in (("ZACATECAS", -102.95, 22.65), ("JALISCO", -102.95, 21.3), ("SAN LUIS POTOSÍ", -101.35, 22.35),
                          ("GUANAJUATO", -101.3, 21.15), ("AGUASCALIENTES", -102.32, 22.06)):
        R.mar("mx", txt, lon, lat, 22, 0.28, color=EDO_TXT)


def _soldados16(R, t0, t1, y=1000, sem=1, s=0.36, sale="encoger"):
    """La guarnición de 1584: 16 soldados en fila que aparecen uno a uno."""
    for k in range(16):
        x = 470 + k * 70
        pa(R, PL(1), x, y - (k % 2) * 14, s, t0 + 0.07 * k, t1, sem=sem + k, z=3, sale=sale, d_in=0.3,
           extra=[(0.0, "pop", 0.18)] if k % 5 == 0 else ())


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_1584, t_nue, t_vil, t_16, t_cap, t_2v = T(e, "1584"), T(e, "nueve"), T(e, "villa"), T(e, "16"), T(e, "capitan"), T(e, "vecinos")
    t_des, t_hoy, t_fer, t_8, t_vis = T(e, "desaparecer"), T(e, "hoy"), T(e, "feria"), T(e, "8"), T(e, "visitantes")
    t_esc, t_lab, t_tea, t_pan, t_bal, t_cal, t_fam = (T(e, "escudo"), T(e, "labios"), T(e, "teatros"), T(e, "pancho"), T(e, "balazos"),
                                                       T(e, "calavera"), T(e, "famosa"))
    t_his, t_ags, t_lug, t_com = T(e, "historia"), T(e, "aguascalientes", frase=3), T(e, "lugares"), T(e, "comprobarla")

    # cámara: la villa de cerca → el estado → el valle → el estado con margen para el título
    R.camara(0.0, -102.30, 21.885, 4.6)
    R.camara(t_16 - 0.3, -102.29, 21.88, 5.2)
    R.camara(t_des + 0.2, -102.29, 21.9, 3.6)
    R.camara(t_hoy + 0.3, -102.32, 21.95, 2.2)
    R.camara(t_esc - 0.2, -102.33, 21.98, 1.85)
    R.camara(t_his - 0.2, -102.36, 22.0, 1.65)
    R.camara(FIN(e) + 0.6, -102.38, 22.0, 1.55)

    # frase 0: 1584, una villa con 16 soldados, un capitán y 2 vecinos
    R.anio(t_1584, 1584)
    ga(R, PL(2), AGS, i0, t_hoy, s=0.62, off=(0, 40), sem=1, zs=0.35, z=2, entra="sube", dy=260, extra=[(0.05, "crece", 0.35)])
    ga(R, FU(5), AGS, i0 + 0.3, t_hoy, s=0.42, off=(-210, 60), sem=2, zs=0.35, z=1)
    ga(R, FU(5), AGS, i0 + 0.5, t_hoy, s=0.38, off=(220, 70), sem=3, zs=0.35, z=1)
    ga(R, FU(6), AGS, t_vil - 0.1, t_hoy, s=0.40, off=(120, -40), sem=4, zs=0.35, z=1)
    R.texto(t_nue - 0.1, t_16 - 0.7, "NUEVA ESPAÑA, 1584", (960, 190), px=70, d=0.6)
    _soldados16(R, t_16 - 0.2, t_des + 0.4, sem=10)
    R.contador(t_16 - 0.2, t_des + 0.2, 0, 16, (960, 196), px=70, formato="{:,} SOLDADOS", hasta_t=t_16 + 1.1)
    pa(R, PL(1), 1660, 1000, 0.62, t_cap - 0.15, t_des + 0.4, sem=30, extra=[(0.04, "fanfarria", 0.22)])
    R.texto(t_cap, t_des + 0.1, "1 CAPITÁN", (1660, 690), px=44, d=0.3)
    pa(R, FU(1), 210, 1000, 0.55, t_2v - 0.15, t_des + 0.4, sem=31)
    pa(R, FU(2), 330, 1000, 0.52, t_2v - 0.05, t_des + 0.4, sem=32)
    R.texto(t_2v + 0.1, t_des + 0.1, "2 VECINOS", (270, 720), px=44, d=0.3)

    # frase 1: casi desaparece → hoy, 8 millones en su feria
    R.snd(t_des, "whoosh", 0.35, dur=0.7)
    R.anio(t_hoy, 2026)
    R.terreno(t_hoy - 0.1, "aguascalientes", COL["aguascalientes"], 1.0)
    pa(R, TU(4), 1560, 1010, 1.15, t_fer - 0.2, t_esc - 0.1, sem=33, entra="sube", dy=320, extra=[(0.05, "feria", 0.35)])
    pa(R, TU(1), 380, 1010, 0.95, t_fer, t_esc - 0.1, sem=34)
    R.contador(t_8 - 0.2, t_esc - 0.2, 0, 8000000, (960, 196), px=76, formato="{:,} VISITANTES", hasta_t=t_vis + 0.3)

    # frase 2: unos labios, Pancho Villa y la calavera más famosa
    pa(R, XI(6), 330, 1010, 0.95, t_esc - 0.1, t_his - 0.1, sem=35, extra=[(0.05, "beso", 0.4)])
    R.texto(t_lab, t_his - 0.2, "UNOS LABIOS", (330, 600), px=44, d=0.3)
    pa(R, PO(7), 860, 1010, 0.95, t_tea - 0.15, t_his - 0.1, sem=36)
    pa(R, RV(0), 1150, 1015, 1.0, t_pan - 0.1, t_his - 0.1, sem=37, extra=[(0.05, "galope", 0.3, {"dur": 0.7})])
    R.texto(t_bal - 0.05, t_his - 0.2, "¡BALAZOS!", (1060, 520), px=52, d=0.25)
    R.snd(t_bal + 0.05, "impacto", 0.4)
    pa(R, AR(2), 1620, 1015, 1.05, t_cal - 0.15, t_his - 0.1, sem=38, extra=[(0.05, "campana", 0.25)])
    R.texto(t_fam, t_his - 0.2, "LA CATRINA", (1620, 580), px=44, d=0.3)

    # frase 3: título + los lugares para comprobarla
    R.texto(t_his - 0.2, FIN(e) + 0.6, "LA HISTORIA DE AGUASCALIENTES", (960, 176), px=92, d=0.9)
    R.snd(t_his - 0.2, "escribir", 0.4, dur=0.9)
    R.texto(t_lug - 0.1, FIN(e) + 0.6, "y dónde comprobarla", (960, 292), px=64, d=0.6)
    for k, (cl, txt, lado) in enumerate((("plaza_patria", "CENTRO", "arriba"), ("cerro_muerto", "CERRO DEL MUERTO", "izq"),
                                         ("real_asientos", "REAL DE ASIENTOS", "der"), ("calvillo", "CALVILLO", "abajo"),
                                         ("cristo_roto", "CRISTO ROTO", "izq"))):
        ciudad(R, t_lug + 0.25 * k, FIN(e) + 0.5, cl, txt, lado, 34)
    pa(R, TU(0), 1640, 1010, 1.0, t_ags - 0.1, FIN(e) + 0.6, sem=39, extra=[(0.05, "pasos", 0.25, {"dur": 0.8})])
    R.terreno(FIN(e) + 0.3, None, COL["aguascalientes"], 0.5)


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0 = INI(e)
    t_caz, t_rec = T(e, "cazadores"), T(e, "recolectores")
    t_600, t_tec, t_pin, t_roj, t_ocote, t_inah = (T(e, "600"), T(e, "tecuanes"), T(e, "pinto"), T(e, "rojas"), T(e, "ocote"),
                                                   T(e, "1985"))
    t_sig, t_gua, t_gch, t_zac, t_cax, t_tcx = (T(e, "siglos"), T(e, "guamares"), T(e, "guachichiles"), T(e, "zacatecos"),
                                                T(e, "caxcanes"), T(e, "tecuexes"))
    t_mex, t_chi, t_pero, t_nom, t_arq, t_som = (T(e, "mexicas"), T(e, "chichimecas", frase=3), T(e, "pero", frase=3), T(e, "nomadas"),
                                                 T(e, "arqueros"), T(e, "someter"))
    t_ley, t_cen = T(e, "leyenda"), T(e, "centro")
    t_sac, t_gig, t_cha, t_sem, t_sal = T(e, "sacerdote"), T(e, "gigante"), T(e, "charcos"), T(e, "sembrar"), T(e, "sal")
    t_fle, t_cor, t_cay, t_mon, t_roj2, t_san = (T(e, "flecha"), T(e, "corazon"), T(e, "cayo"), T(e, "montana"), T(e, "rojo"),
                                                 T(e, "sangre"))
    t_cer, t_mir, t_sil, t_aco, t_man = T(e, "cerro", frase=7), T(e, "miralo"), T(e, "silueta"), T(e, "acostado"), T(e, "manos")

    R.camara(i0 - 0.2, -102.38, 22.0, 1.55)
    R.camara(t_rec + 0.4, -102.45, 21.9, 1.9)
    R.camara(t_tec - 0.1, -102.56, 21.78, 3.4)
    R.camara(t_inah + 0.4, -102.55, 21.79, 3.6)
    R.camara(t_sig + 0.3, -102.3, 21.95, 1.05)
    R.camara(t_tcx + 0.6, -102.35, 21.9, 0.95)
    R.camara(t_mex, -102.3, 21.95, 1.15)
    R.camara(t_ley - 0.1, -102.35, 21.89, 2.2)
    R.camara(t_sac, -102.42, 21.87, 3.4)
    R.camara(t_fle + 0.2, -102.43, 21.87, 3.9)
    R.camara(t_cer - 0.2, -102.38, 21.875, 3.2)
    R.camara(FIN(e) + 0.4, -102.36, 21.88, 3.0)

    R.anio(i0, 600)
    R.sello(i0 + 0.3, "piramide_mx", "TIERRA CHICHIMECA", color=(196, 120, 62))
    # frase 0: cazadores y recolectores
    R.terreno(i0, "chichimecas", COL["chichimecas"], 1.2, capa=1)
    pa(R, CH(3), 330, 1010, 1.0, i0 + 0.05, t_600 - 0.1, sem=40, extra=[(0.05, "pasos", 0.25, {"dur": 0.6})])
    pa(R, CH(6), 1580, 1010, 0.9, t_caz - 0.2, t_600 - 0.1, sem=41, entra="sube", dy=280)
    pa(R, CH(2), 1300, 1010, 0.85, t_rec - 0.2, t_600 - 0.1, sem=42)
    R.texto(t_caz, t_600 - 0.2, "CAZADORES Y RECOLECTORES", (960, 196), px=66, d=0.6)

    # frase 1: El Ocote, hacia el año 600
    R.anio(t_600, 600)
    lugar(R, t_tec, t_sig - 0.2, "CERRO LOS TECUANES", CI["el_ocote"], off=(0, -290), px=36)
    ga(R, CH(7), CI["el_ocote"], t_pin - 0.2, t_sig - 0.1, s=0.62, off=(-40, 30), sem=43, zs=0.35, z=2, entra="sube", dy=240,
       extra=[(0.05, "pincel", 0.35)])
    pa(R, FP.F("origenes_1"), 1430, 960, FP.s_para(0.46), t_roj - 0.2, t_inah + 1.2, entra="pluma", sem=44, z=4)
    titulo(R, t_ocote - 0.1, t_sig - 0.15, "EL OCOTE", px=86, snd=True)
    R.texto(t_inah - 0.1, t_sig - 0.15, "registrado por el INAH en 1985", (960, 300), px=48, d=0.5)
    pa(R, CH(1), 300, 1010, 0.95, t_pin, t_sig - 0.1, sem=45)

    # frase 2: los pueblos del norte
    R.anio(t_sig, 1300)
    R.terreno(t_sig, None, COL["chichimecas"], 0.4, capa=1)
    for capa, (t_, campo, dib, n, geo) in enumerate((
            (t_gua, "guamares", CH(1), "GUAMARES", (-101.55, 21.45)),
            (t_gch, "guachichiles", CH(0), "GUACHICHILES", (-101.5, 22.45)),
            (t_zac, "zacatecos", CH(3), "ZACATECOS", (-102.85, 22.6)),
            (t_cax, "caxcanes", CH(1), "CAXCANES", (-103.1, 21.55)),
            (t_tcx, "tecuexes", CH(2), "TECUEXES", (-102.55, 21.15))), start=2):
        R.terreno(t_ - 0.15, campo, COL[campo], 0.7, capa=capa)
        ga(R, dib, geo, t_ - 0.1, t_ley - 0.1, s=0.6, off=(0, 40), sem=46 + capa, zs=0.4, z=2, flip=capa % 2 == 0,
           extra=[(0.05, "tambor", 0.22, {"dur": 0.5})] if capa in (2, 5) else ())
        lugar(R, t_, t_ley - 0.2, n, geo, off=(0, 86), px=36)

    # frase 3: «chichimecas»: una forma de vida
    titulo(R, t_chi - 0.1, t_ley - 0.2, "«CHICHIMECAS»", px=96, snd=True)
    R.texto(t_pero, t_ley - 0.2, "no un pueblo: una forma de vida", (960, 312), px=54, d=0.6)
    grupo_ciclo(R, C_CHI, [(-101.8, 22.3), (-102.3, 22.05), (-102.75, 21.85)], t_nom - 0.3, 3.4, n=4, ancho=70, t1=t_ley - 0.1, s=0.5,
                sem=60, fps=12, extra=[(0.05, "pasos", 0.3, {"dur": 1.4})])
    pa(R, CH(5), 960, 1010, 0.7, t_nom - 0.1, t_ley - 0.1, sem=65, extra=[(0.05, "fuego", 0.3, {"dur": 1.2})])
    pa(R, CH(0), 330, 1010, 1.05, t_arq - 0.15, t_ley - 0.1, sem=66, extra=[(0.05, "flecha", 0.35)])
    pa(R, CH(1), 1600, 1010, 1.0, t_som - 0.3, t_ley - 0.1, sem=67, flip=True)
    for c in range(1, 7):
        R.terreno(t_ley - 0.1, None, (0, 0, 0), 0.4, capa=c)

    # frase 4-7: la leyenda del Cerro del Muerto
    R.sello(t_ley, "olmeca", "LEYENDA", color=(120, 90, 160))
    ciudad(R, t_cen - 0.2, t_cer, "plaza_patria", "CENTRO", "der", 34)
    R.texto(t_ley + 0.2, t_sac - 0.2, "una leyenda que se ve desde la ciudad", (960, 196), px=56, d=0.6)
    pa(R, CH(2), 330, 1010, 0.95, t_ley - 0.1, t_sac - 0.1, sem=79)
    pa(R, CH(5), 620, 1010, 0.6, t_ley + 0.2, t_sac - 0.1, sem=81, extra=[(0.05, "fuego", 0.25, {"dur": 0.8})])
    pa(R, TU(0), 1600, 1010, 0.95, t_cen - 0.3, t_sac - 0.1, sem=82)
    pa(R, CH(4), 760, 1020, 1.4, t_sac - 0.2, t_cay + 0.4, sem=70, z=3, entra="sube", dy=320, sale="caer", d_out=0.7,
       extra=[(0.05, "crece", 0.35, {"dur": 0.9})])
    R.texto(t_gig, t_fle - 0.2, "UN SACERDOTE GIGANTE", (960, 196), px=64, d=0.5)
    pa(R, FU(4), 1260, 1000, 0.62, t_cha - 0.2, t_mon + 0.4, sem=71, extra=[(0.05, "agua_termal", 0.35)])
    pa(R, FU(4), 1560, 990, 0.5, t_sem - 0.1, t_mon + 0.4, sem=72)
    R.texto(t_sem, t_fle - 0.2, "«sembrar manantiales» con agua y sal", (960, 304), px=48, d=0.5)
    pa(R, PL(7), 330, 1010, 0.55, t_sal - 0.2, t_fle, sem=73)
    R.snd(t_fle, "flecha", 0.45)
    pa(R, CH(0), 330, 1010, 1.05, t_fle - 0.3, t_cer - 0.1, sem=74, flip=True)
    pa(R, CH(2), 1600, 1010, 0.95, t_cay, t_cer - 0.1, sem=77)
    pa(R, CH(5), 1180, 1010, 0.6, t_mon - 0.2, t_cer - 0.1, sem=78)
    R.snd(t_cay + 0.35, "impacto", 0.4)
    R.texto(t_mon - 0.1, t_cer - 0.2, "…y su cuerpo se volvió montaña", (960, 196), px=58, d=0.5)
    R.texto(t_roj2, t_cer - 0.2, "el rojo del atardecer: su sangre", (960, 300), px=46, d=0.5)
    pa(R, FP.F("origenes_7"), 1380, 965, FP.s_para(0.46), t_cer - 0.2, FIN(e) + 0.6, entra="pluma", sem=75, z=4)
    lugar(R, t_cer, FIN(e) + 0.4, "CERRO DEL MUERTO", CI["cerro_muerto"], off=(0, -120), px=44)
    R.texto(t_sil, FIN(e) + 0.4, "HOY: MÍRALO DESDE EL CENTRO", (560, 196), px=50, d=0.5)
    pa(R, TU(0), 360, 1010, 0.9, t_mir - 0.1, FIN(e) + 0.5, sem=76)
    R.snd(t_aco, "suspiro", 0.25)


# ------------------------------------------------------------------ LA PLATA
def _plata(R):
    e = "plata"
    i0 = INI(e)
    t_1546, t_tol, t_pla, t_zac = T(e, "1546"), T(e, "tolosa"), T(e, "plata"), T(e, "zacatecas")
    t_lle, t_mex, t_cam, t_rut = T(e, "llevarla"), T(e, "mexico"), T(e, "camino"), T(e, "ruta")
    t_res, t_car, t_emp, t_gue, t_50, t_emb = (T(e, "respondieron"), T(e, "carretas"), T(e, "empezo"), T(e, "guerra"), T(e, "50"),
                                               T(e, "emboscadas"))
    t_lev, t_pre, t_fue, t_lar = T(e, "levantaron"), T(e, "presidios"), T(e, "fuertes"), T(e, "largo")
    t_fal, t_lag, t_zac2, t_man, t_cal = T(e, "faltaba"), T(e, "lagos"), T(e, "zacatecas", frase=4), T(e, "manantiales"), T(e, "caliente")
    ruta = M.RUTAS["camino_plata"]

    R.camara(i0 - 0.2, -102.5, 22.55, 2.0)
    R.camara(t_zac + 0.3, -102.58, 22.74, 2.6)
    R.camara(t_lle + 0.2, -102.25, 22.1, 0.95)
    R.camara(t_res, -102.1, 21.9, 0.85)
    R.camara(t_lev - 0.1, -102.18, 22.12, 1.25)
    R.camara(t_fal - 0.1, -102.15, 22.05, 1.0)
    R.camara(t_man - 0.2, -102.28, 21.88, 2.6)
    R.camara(FIN(e) + 0.4, -102.28, 21.88, 3.4)

    R.sello(i0 + 0.2, "corona", "NUEVA ESPAÑA", color=(176, 52, 48))
    # frase 0: Tolosa encuentra plata en Zacatecas
    R.anio(t_1546, 1546)
    pa(R, PL(4), 330, 1010, 1.0, i0, t_lle, sem=80, extra=[(0.05, "golpe_suave", 0.3)])
    R.texto(t_tol, t_lle - 0.1, "JUAN DE TOLOSA", (330, 600), px=44, d=0.3)
    ga(R, PL(7), CI["zacatecas"], t_pla - 0.15, t_cam - 0.3, s=0.6, off=(0, 40), sem=81, zs=0.4, z=2, entra="sube", dy=200,
       extra=[(0.05, "monedas", 0.4)])
    ciudad(R, t_zac - 0.2, t_cam - 0.3, "zacatecas", "ZACATECAS (1548)", "der", 40)
    titulo(R, t_pla, t_lle - 0.1, "¡PLATA!", px=110)

    # frase 1: el Camino Real de Tierra Adentro
    R.ruta(ruta, t_lle - 0.1, 3.0, ancho=5.0, t1=FIN(e) + 0.4, flecha=True)
    ciudad(R, t_mex - 0.2, t_lev, "ciudad_mexico", "A CIUDAD DE MÉXICO", "abajo", 34)
    titulo(R, t_cam - 0.1, t_res - 0.15, "CAMINO REAL DE TIERRA ADENTRO", px=74, snd=True)
    R.texto(t_rut, t_res - 0.15, "la ruta de la plata", (960, 300), px=54, d=0.5)
    pa(R, PL(0), 330, 1010, 1.0, t_cam - 0.1, t_res - 0.1, sem=99, entra="sube", dy=260)
    pa(R, PL(4), 1600, 1010, 0.95, t_rut - 0.2, t_res - 0.1, sem=79, flip=True)
    andar_ciclo(R, C_CAR, list(reversed(ruta)), t_lle, 7.0, t1=t_lev, s=0.8, sem=82, fps=6, extra=[(0.05, "pasos", 0.2, {"dur": 1.5})])
    R.act(PL(3), pos_geo=R.camino_pos(list(reversed(ruta)), t_lle + 0.6, 7.0), off=(-90, 20), s=0.7, t_in=t_lle + 0.6, d_in=0.35,
          entra="pop", sem=83, zs=0.4, z=2, t_out=t_lev, flip=True)

    # frase 2: la Guerra Chichimeca
    R.terreno(t_res - 0.1, "chichimecas", COL["chichimecas"], 0.9, capa=1)
    grupo_ciclo(R, C_CHI, [(-101.5, 22.4), (-101.95, 22.1), (-102.28, 21.98)], t_res, 2.4, n=4, ancho=72, t1=t_lev, s=0.5, sem=84,
                fps=12, extra=[(0.05, "tambor", 0.35, {"dur": 1.2})])
    pa(R, PL(5), 330, 1010, 1.0, t_car - 0.2, t_lev - 0.1, sem=88, extra=[(0.05, "flecha", 0.4)])
    pa(R, PL(6), 1600, 1010, 0.8, t_car + 0.2, t_lev - 0.1, sem=89, extra=[(0.04, "crujido", 0.3)])
    titulo(R, t_gue - 0.1, t_lev - 0.15, "GUERRA CHICHIMECA", px=86, snd=True)
    R.texto(t_50, t_lev - 0.15, "1550 - 1600: CASI 50 AÑOS", (960, 300), px=56, d=0.5)
    R.terreno(t_lev - 0.1, None, COL["chichimecas"], 0.5, capa=1)

    # frase 3: presidios
    R.anio(t_lev, 1570)
    for k, cl in enumerate(("cienega_grande", "bocas_gallardo", "palmillas")):
        ga(R, PL(2), CI[cl], t_pre - 0.1 + 0.25 * k, FIN(e) + 0.3, s=0.6, off=(0, 30), sem=90 + k, zs=0.35, z=2,
           extra=[(0.05, "sello", 0.3)] if k == 0 else ())
    titulo(R, t_pre, t_fal - 0.15, "PRESIDIOS", px=90)
    pa(R, PL(2), 330, 1010, 1.0, t_pre - 0.2, t_fal - 0.1, sem=78, entra="sube", dy=260)
    pa(R, PL(1), 1600, 1010, 1.0, t_fue - 0.2, t_fal - 0.1, sem=77, flip=True)
    R.texto(t_fue, t_fal - 0.15, "pequeños fuertes", (960, 300), px=54, d=0.5)
    grupo_ciclo(R, C_SOL, ruta[3:9], t_lev, 3.2, n=3, ancho=80, t1=t_fal + 0.5, s=0.62, sem=93, extra=[(0.05, "pasos", 0.3, {"dur": 1.5})])

    # frase 4: faltaba uno, junto a los manantiales
    ciudad(R, t_lag - 0.2, FIN(e) + 0.2, "lagos_moreno", "LAGOS", "der", 36)
    ciudad(R, t_zac2 - 0.2, FIN(e) + 0.2, "zacatecas", "ZACATECAS", "der", 36)
    ga(R, lambda t: A.signo_pregunta(), AGS, t_fal, t_man + 0.3, s=0.6, off=(0, -40), sem=96, zs=0.3, z=3, extra=[(0.05, "pluck", 0.3)])
    ga(R, FU(4), CI["ojocaliente"], t_man - 0.1, FIN(e) + 0.5, s=0.62, off=(0, 50), sem=97, zs=0.35, z=3,
       extra=[(0.05, "agua_termal", 0.4)])
    R.texto(t_cal - 0.1, FIN(e) + 0.4, "AGUA CALIENTE", (960, 196), px=74, d=0.5)
    pa(R, PL(1), 1600, 1010, 0.95, t_man - 0.2, FIN(e) + 0.5, sem=98, flip=True)


# ------------------------------------------------------------------ LA FUNDACIÓN
def _fundacion(R):
    e = "fundacion"
    i0 = INI(e)
    t_22, t_1575, t_gdl, t_oro, t_fir, t_rey, t_car = (T(e, "22"), T(e, "1575"), T(e, "guadalajara"), T(e, "orozco"), T(e, "firmo"),
                                                       T(e, "rey"), T(e, "carta"))
    t_rec, t_mon, t_12, t_lag, t_no, t_col = T(e, "recibio"), T(e, "montoro"), T(e, "12"), T(e, "lagos"), T(e, "no", frase=1), T(e, "colonos")
    t_nom, t_vil, t_agu = T(e, "nombre", frase=2), T(e, "villa"), T(e, "aguas", frase=2)
    t_cha, t_poz, t_tal = T(e, "charco"), T(e, "poza"), T(e, "tallarse")
    t_oid, t_cau = T(e, "oidor"), T(e, "causa")
    t_pero, t_ata, t_cen, t_1584, t_16, t_cap, t_2 = (T(e, "pero"), T(e, "ataques"), T(e, "censo"), T(e, "1584"), T(e, "16"),
                                                      T(e, "capitan"), T(e, "vecinos", frase=5))
    t_sob, t_mil, t_apa, t_cre = T(e, "sobrevivio"), T(e, "milagro"), T(e, "apago"), T(e, "crecer")

    R.camara(i0 - 0.2, -102.7, 21.4, 1.0)
    R.camara(t_rec - 0.2, -102.5, 21.4, 1.1)
    R.camara(t_lag + 0.4, -102.1, 21.6, 1.6)
    R.camara(t_nom - 0.1, -102.29, 21.95, 3.2)
    R.camara(t_cha - 0.2, -102.272, 21.915, 5.2)
    R.camara(t_oid, -102.28, 21.92, 4.8)
    R.camara(t_pero - 0.1, -102.29, 21.94, 3.8)
    R.camara(t_sob, -102.3, 21.925, 4.4)
    R.camara(FIN(e) + 0.4, -102.3, 21.925, 4.6)

    # frase 0: 22 de octubre de 1575, Orozco firma la carta de fundación
    R.anio(t_1575, 1575)
    R.sello(t_22, "corona", "FUNDACIÓN", color=(176, 52, 48))
    titulo(R, t_22 - 0.1, t_rec - 0.2, "22 DE OCTUBRE DE 1575", px=84, snd=True)
    ciudad(R, t_gdl - 0.2, t_rec, "guadalajara", "GUADALAJARA", "arriba", 36)
    pa(R, FU(0), 330, 1010, 1.05, i0 + 0.05, t_rec - 0.1, sem=100)
    R.texto(t_oro, t_rec - 0.2, "JERÓNIMO DE OROZCO", (330, 580), px=40, d=0.3)
    pa(R, FU(3), 1580, 1010, 0.95, t_fir - 0.15, t_rec - 0.1, sem=101, entra="sube", dy=300, extra=[(0.05, "escribir", 0.4, {"dur": 0.8})])
    R.snd(t_car + 0.3, "sello", 0.45)
    R.texto(t_rey, t_rec - 0.2, "en nombre de Felipe II", (960, 300), px=50, d=0.5)

    # frase 1: Juan de Montoro y 12 vecinos de Lagos
    ruta = [CI["lagos_moreno"], (-102.1, 21.47), (-102.24, 21.6), AGS]
    R.ruta(ruta, t_rec, 3.2, ancho=4.5, t1=t_nom, flecha=True)
    for k in range(12):
        R.act(FU(1) if k % 3 else FU(2), pos_geo=R.camino_pos(ruta, t_rec + 0.12 * k, 4.0), off=((k % 4 - 1.5) * 46, (k // 4) * 34 - 30),
              s=0.42, t_in=t_rec + 0.12 * k, d_in=0.3, entra="pop", sem=102 + k, zs=0.4, z=2, t_out=t_nom + 0.3, flip=True)
    pa(R, FU(1), 330, 1010, 1.05, t_mon - 0.15, t_nom - 0.1, sem=115, extra=[(0.05, "galope", 0.25, {"dur": 0.7})])
    R.texto(t_mon, t_nom - 0.2, "JUAN DE MONTORO", (330, 580), px=40, d=0.3)
    R.contador(t_12 - 0.2, t_nom - 0.2, 0, 12, (1060, 930), px=64, formato="{:,} VECINOS DE LAGOS", hasta_t=t_lag + 0.2)
    R.texto(t_no, t_nom - 0.2, "colonos de la frontera, no de España", (1060, 1020), px=44, d=0.5)
    pa(R, FU(2), 1660, 1010, 1.0, t_col - 0.3, t_nom - 0.1, sem=116)

    # frase 2: el nombre larguísimo
    ga(R, FU(6), AGS, t_nom - 0.1, FIN(e) + 0.5, s=0.45, off=(60, -20), sem=117, zs=0.35, z=2)
    ga(R, FU(5), AGS, t_nom + 0.1, FIN(e) + 0.5, s=0.42, off=(-120, 30), sem=118, zs=0.35, z=1)
    pa(R, FU(7), 1600, 1010, 1.05, t_vil - 0.2, t_cha - 0.1, sem=119, extra=[(0.05, "campana", 0.3)])
    R.texto(t_vil - 0.05, t_cha - 0.2, "VILLA DE NUESTRA SEÑORA DE LA ASUNCIÓN", (900, 176), px=58, d=1.0)
    R.texto(t_agu - 0.1, t_cha - 0.2, "DE LAS AGUAS CALIENTES", (900, 272), px=72, d=0.6)
    R.snd(t_vil, "escribir", 0.35, dur=1.4)

    # frase 3-4: un charco termal, «la causa principal»
    ga(R, FU(4), CI["ojocaliente"], t_cha - 0.25, t_pero, s=0.85, off=(0, 60), sem=120, zs=0.3, z=3, entra="sube", dy=200,
       extra=[(0.05, "agua_termal", 0.45)])
    lugar(R, t_cha, t_pero - 0.2, "OJOCALIENTE", CI["ojocaliente"], off=(0, 150), px=40)
    titulo(R, t_cha, t_oid - 0.15, "UN CHARCO", px=100)
    R.texto(t_poz, t_oid - 0.15, "una poza termal para tallarse", (960, 304), px=50, d=0.5)
    pa(R, FU(1), 330, 1010, 0.95, t_tal - 0.3, t_pero - 0.1, sem=121)
    pa(R, FU(0), 1600, 1010, 1.05, t_oid - 0.15, t_pero - 0.1, sem=122, flip=True)
    R.texto(t_cau - 0.05, t_pero - 0.2, "«la causa principal»", (960, 196), px=70, d=0.5)

    # frase 5: el censo de 1584
    R.anio(t_1584, 1584)
    R.texto(t_cen - 0.1, t_sob - 0.2, "CENSO DE 1584", (960, 176), px=74, d=0.5)
    pa(R, PL(5), 1520, 1010, 1.1, t_pero - 0.1, t_16 - 0.4, sem=157, extra=[(0.05, "galope", 0.3, {"dur": 0.8})])
    R.texto(t_pero, t_cen - 0.2, "LA VILLA NO PROSPERÓ", (960, 196), px=66, d=0.5)
    _soldados16(R, t_16 - 0.2, t_sob + 0.3, sem=130)
    pa(R, PL(1), 1680, 1000, 0.6, t_cap - 0.15, t_sob + 0.3, sem=150)
    pa(R, FU(1), 200, 1000, 0.5, t_2 - 0.15, t_sob + 0.3, sem=151)
    pa(R, FU(2), 310, 1000, 0.48, t_2 - 0.05, t_sob + 0.3, sem=152)
    R.texto(t_16, t_sob - 0.2, "16 soldados · 1 capitán · 2 vecinos", (960, 290), px=50, d=0.5)
    grupo_ciclo(R, C_CHI, [(-102.05, 22.0), (-102.2, 21.93), (-102.27, 21.89)], t_ata - 0.2, 1.8, n=3, ancho=60, t1=t_cen + 0.6, s=0.48,
                sem=153, fps=12, extra=[(0.05, "flecha", 0.3)])

    # frase 6: sobrevivió de milagro y empezó a crecer
    R.texto(t_mil - 0.1, FIN(e) + 0.4, "SOBREVIVIÓ DE MILAGRO", (960, 196), px=70, d=0.5)
    pa(R, CH(5), 1560, 700, 0.6, t_sob, t_apa + 0.2, sem=156, sale="encoger", d_out=0.8)
    for k, (dx, dy) in enumerate(((-260, 40), (240, 60), (-140, 120), (150, -60), (310, -30), (-320, -40), (40, 140))):
        ga(R, FU(5), AGS, t_apa + 0.15 * k, FIN(e) + 0.6, s=0.34, off=(dx, dy), sem=160 + k, zs=0.35, z=1,
           extra=[(0.05, "crece", 0.3)] if k == 0 else ())
    R.texto(t_cre, FIN(e) + 0.4, "…y empezó a crecer", (960, 300), px=54, d=0.5)
    pa(R, FU(2), 330, 1010, 1.0, t_apa - 0.1, FIN(e) + 0.6, sem=170)
