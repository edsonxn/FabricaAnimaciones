# -*- coding: utf-8 -*-
"""Coreografía (4/4): derechos civiles (Rosa Parks en Montgomery, la marcha sobre Washington, las leyes de 1964 y 1965),
la era moderna (fin de la URSS, Silicon Valley e Internet, el 11-S, la crisis de 2008 y Obama), la actualidad (340 millones,
50 estados, la mayor economía, 65 millones de hispanos, el español de San Antonio, Santa Fe y Los Ángeles), el cierre y
los cambios de escena procedurales.
Capas: 0 = EE. UU., 1-3 = la huella hispana (lo que fue de España y México)."""
import math

import mapa as M
import obj_a as A
import obj_c as C
import obj_us1 as P1
import obj_us2 as P2
import obj_us3 as P3
from core import FIN, INI, T
from coreo_util import CI, COL, andar, ciudad, foco, ga, lugar, pa, para, titulo
from trans import SFX, Transicion


def cortes(R):
    pass


def construir(R):
    _derechos(R)
    _moderno(R)
    _actualidad(R)
    _cierre(R)
    _transiciones(R)


# ------------------------------------------------------------------ DERECHOS CIVILES
def _derechos(R):
    e = "derechos"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_sur, t_ros, t_nie, t_asi, t_aut, t_bla = W(0, "sur"), W(0, "rosa"), W(0, "niega"), W(0, "asiento"), W(0, "autobus"), W(0, "blanco")
    t_mar, t_enc, t_mch, t_was, t_sue, t_igu, t_dos = (W(1, "martin"), W(1, "encabeza"), W(1, "marcha"), W(1, "washington"), W(1, "sueno"),
                                                       W(1, "igualdad"), W(1, "doscientas"))
    t_mil2, t_ley, t_seg, t_ano, t_gar, t_vot = W(2, "mil"), W(2, "ley"), W(2, "segregacion"), W(2, "ano"), W(2, "garantiza"), W(2, "voto")

    # cámara: Montgomery -> Washington (Lincoln Memorial) -> el país entero
    foco(R, i0 - 0.7, t_bla + 0.4, CI["montgomery"], 6.0)
    foco(R, t_mar + 0.1, t_mil2 - 0.4, CI["washington"], 6.2)
    para(R, t_mil2 + 0.5, FIN(e) + 0.6, -93.0, 37.6, 0.95)

    R.anio(i0 + 0.1, 1955)
    R.anio(t_mar, 1963)
    R.anio(t_mil2 + 0.3, 1964)
    R.anio(t_ano, 1965)

    # frase 0: Rosa Parks (Montgomery, 1955)
    R.terreno(i0 - 0.3, "eeuu_mod", COL["eeuu"], 0.6)
    ciudad(R, t_sur, t_mar - 0.2, "montgomery", "MONTGOMERY", "abajo", 46)
    ga(R, P3.autobus_montgomery(), CI["montgomery"], t_ros - 0.2, t_mar - 0.2, s=0.56, off=(0, -20), sem=700, zs=0.5, z=2, entra="sube",
       dy=280, extra=[(0.05, "zoom_whoosh", 0.35)])
    pa(R, P1.rosa_parks(0, "serio"), 310, 1010, 1.06, t_ros - 0.15, t_mar, sem=701)
    R.texto(t_ros + 0.2, t_mar - 0.1, "ROSA PARKS", (310, 580), px=44, d=0.4)
    titulo(R, t_nie - 0.2, t_mar - 0.2, "«NO» (1955)", px=88)
    pa(R, P1.manifestante(0, "feliz"), 1620, 1010, 1.0, t_aut - 0.1, t_mar, sem=702, flip=True)
    pa(R, P1.manifestante(1, "serio"), 1370, 1010, 0.94, t_bla - 0.3, t_mar, sem=703)
    R.sello(t_mch, "balanza", "DERECHOS CIVILES", color=(92, 120, 160))

    # frase 1: Martin Luther King y la marcha sobre Washington (1963)
    ciudad(R, t_was - 0.2, t_mil2 - 0.2, "washington", "WASHINGTON", "abajo", 44)
    ga(R, P3.monumento_lincoln(), CI["washington"], t_mar - 0.2, t_mil2 - 0.2, s=0.56, off=(0, -30), sem=710, zs=0.5, z=2, entra="pluma",
       d_in=0.9, extra=[(0.05, "crece", 0.4)])
    pa(R, P1.mlk(0, "feliz"), 330, 1010, 1.1, t_mar - 0.15, t_mil2, sem=711, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_mar + 0.2, t_mil2 - 0.1, "MARTIN LUTHER KING", (330, 560), px=40, d=0.4)
    pa(R, P3.microfono_antiguo(), 620, 1000, 0.7, t_enc, t_mil2, sem=712)
    pa(R, A.multitud(10, 7), 1450, 1010, 1.6, t_mch - 0.1, t_mil2, sem=713, entra="sube", dy=260, extra=[(0.05, "pasos", 0.4, {"dur": 1.2})])
    titulo(R, t_sue - 0.3, t_dos - 0.2, "«I HAVE A DREAM»", px=88)
    R.contador(t_dos - 0.2, t_dos + 0.9, 0, 250_000, (960, 196), px=80, formato="{:,} PERSONAS", hasta_t=t_mil2 - 0.1)
    R.snd(t_dos - 0.2, "reloj_rapido", 0.35, dur=0.9)

    # frase 2: 1964, fin de la segregación; 1965, derecho al voto
    R.romper("estados", t_ley - 0.2, t_ley + 0.5, t_ano - 0.2, t_ano + 0.5, gap=10.0, deriva=16.0, fijas=(0,))
    R.snd(t_ley - 0.2, "crujido", 0.35, dur=0.7)
    pa(R, P2.constitucion(), 960, 1010, 1.0, t_ley - 0.3, t_gar, sem=720, entra="sube", dy=340, extra=[(0.05, "papel", 0.45)])
    titulo(R, t_seg - 0.3, t_gar - 0.1, "FIN DE LA SEGREGACIÓN (1964)", px=74)
    pa(R, P1.manifestante(0, "feliz"), 310, 1010, 1.02, t_ley - 0.1, FIN(e) + 0.3, sem=721)
    pa(R, P3.urna_voto(), 960, 1000, 0.9, t_gar - 0.1, FIN(e) + 0.3, sem=722, entra="sube", dy=300, extra=[(0.05, "pop", 0.5)])
    pa(R, P1.ciudadano_hoy(0, "feliz"), 1620, 1010, 1.02, t_gar, FIN(e) + 0.3, sem=723, flip=True)
    titulo(R, t_vot - 0.4, FIN(e) + 0.2, "DERECHO AL VOTO (1965)", px=80)


# ------------------------------------------------------------------ ERA MODERNA
def _moderno(R):
    e = "moderno"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_der, t_uni, t_sil, t_int, t_con, t_pla = W(0, "derrumba"), W(0, "union"), W(0, "silicon"), W(0, "internet"), W(0, "conecta"), W(0, "planeta")
    t_onc, t_ate, t_tor, t_abr, t_gue = W(1, "once"), W(1, "atentados"), W(1, "torres"), W(1, "abren"), W(1, "guerras")
    t_dos2, t_cri, t_sac, t_bar, t_pri, t_afr = W(2, "dos"), W(2, "crisis"), W(2, "sacude"), W(2, "barack"), W(2, "primer"), W(2, "afroamericano")

    SV = CI["silicon_valley"]

    # cámara: Silicon Valley -> el país conectado -> Nueva York -> Washington
    para(R, i0 - 0.7, t_der + 0.8, -100.0, 38.0, 0.95)
    foco(R, t_sil, t_int + 0.5, CI["silicon_valley"], 4.6)
    para(R, t_con + 0.3, t_pla + 0.6, -100.0, 38.5, 0.86)
    foco(R, t_onc + 0.2, t_dos2 - 0.6, CI["nueva_york"], 6.2)
    foco(R, t_dos2 + 0.2, FIN(e) + 0.6, CI["washington"], 5.4)

    R.anio(i0 + 0.1, 1991)
    R.anio(t_int, 1995)
    R.anio(t_onc, 2001)
    R.anio(t_dos2 + 0.2, 2008)

    # frase 0: cae la URSS; Silicon Valley e Internet conectan al planeta
    pa(R, P3.trozo_muro_berlin(), 310, 1010, 0.9, i0, t_sil, sem=730, entra="sube", dy=300)
    pa(R, P3.bandera_urss(), 1600, 1010, 0.92, i0 + 0.2, t_sil, sem=731, flip=True)
    ga(R, A.grietas_hueso(), (-100.0, 38.0), t_der - 0.1, t_sil, s=0.5, off=(0, 0), sem=732, zs=0.35, z=3)
    pa(R, A.grietas_hueso(), 1600, 860, 0.6, t_der - 0.1, t_sil, sem=733, extra=[(0.05, "crujido", 0.5)])
    titulo(R, t_der - 0.2, t_sil - 0.1, "FIN DE LA UNIÓN SOVIÉTICA (1991)", px=70)
    ciudad(R, t_sil - 0.2, t_onc - 0.2, "silicon_valley", "SILICON VALLEY", "der", 44)
    ga(R, P3.ordenador_personal(), SV, t_sil - 0.1, t_con + 0.2, s=0.44, off=(-150, -10), sem=734, zs=0.45, z=2, entra="sube", dy=240)
    pa(R, P1.programador(0, "feliz"), 310, 1010, 1.04, t_sil, t_onc, sem=735, extra=[(0.05, "pluck", 0.4)])
    pa(R, P3.telefono_movil(), 580, 1000, 0.6, t_int, t_onc, sem=736, extra=[(0.05, "ding", 0.4)])
    titulo(R, t_int - 0.2, t_onc - 0.2, "INTERNET", px=90)
    R.sello(t_int, "chip", "ERA DIGITAL", color=(72, 150, 150))
    for k, c in enumerate(("seattle", "chicago", "nueva_york", "miami", "dallas", "denver")):
        R.ruta([SV, CI[c]], t_con - 0.2 + 0.1 * k, 0.8, ancho=4.0, t1=t_onc - 0.2)
        ciudad(R, t_con + 0.1 * k, t_onc - 0.2, c, None, "arriba", 30)
    pa(R, P3.globo_internet(), 1600, 1000, 0.9, t_con - 0.2, t_onc, sem=737, entra="sube", dy=300, extra=[(0.05, "brillo", 0.4)])

    # frase 1: el 11 de septiembre de 2001
    ciudad(R, t_onc, t_dos2 - 0.2, "nueva_york", "NUEVA YORK", "izq", 44)
    ga(R, P3.torres_gemelas(), CI["nueva_york"], t_onc - 0.1, t_dos2 - 0.2, s=0.66, off=(60, -10), sem=740, zs=0.5, z=2, entra="sube",
       dy=300)
    ga(R, lambda t: C.humo(int(t * 4) % 4), CI["nueva_york"], t_ate, t_dos2 - 0.2, s=0.66, off=(70, -260), sem=741, zs=0.5, z=3,
       extra=[(0.05, "apagon", 0.4)])
    titulo(R, t_onc - 0.1, t_abr - 0.1, "11 DE SEPTIEMBRE DE 2001", px=80)
    pa(R, P1.bombero(0, "serio"), 310, 1010, 1.04, t_ate - 0.2, t_dos2, sem=742)
    R.contador(t_tor - 0.2, t_tor + 0.7, 0, 3000, (1560, 560), px=60, formato="~{:,} VÍCTIMAS", hasta_t=t_abr + 0.2)
    pa(R, P1.soldado_ww2(0, "serio"), 1620, 1010, 1.0, t_abr - 0.1, t_dos2, sem=743, flip=True)
    pa(R, lambda t: P3.helicoptero_huey(int(t * 10) % 4), 1300, 360, 0.6, t_gue - 0.3, t_dos2, sem=744, extra=[(0.05, "viento", 0.35)])
    R.texto(t_abr, t_dos2 - 0.1, "UNA NUEVA ERA DE GUERRAS", (960, 196), px=64, d=0.5)

    # frase 2: la crisis de 2008 y Barack Obama
    ciudad(R, t_dos2, FIN(e) + 0.3, "washington", "WASHINGTON", "abajo", 42)
    ga(R, P3.casa_blanca(), CI["washington"], t_dos2, FIN(e) + 0.3, s=0.56, off=(0, -20), sem=750, zs=0.5, z=2, entra="pluma", d_in=0.9)
    pa(R, P3.casa_embargo(), 320, 1000, 0.86, t_cri - 0.2, t_bar, sem=751, entra="sube", dy=280, extra=[(0.05, "apagon", 0.4)])
    pa(R, P3.grafico_crash(), 640, 1000, 0.7, t_cri, t_bar, sem=752)
    R.texto(t_cri, t_bar - 0.1, "CRISIS FINANCIERA", (480, 600), px=44, d=0.4)
    pa(R, P1.obama(0, "feliz"), 1600, 1010, 1.12, t_bar - 0.2, FIN(e) + 0.3, sem=753, flip=True, extra=[(0.05, "fanfarria", 0.45)])
    R.texto(t_bar + 0.1, FIN(e) + 0.2, "BARACK OBAMA", (1600, 560), px=44, d=0.4)
    titulo(R, t_pri - 0.3, FIN(e) + 0.2, "PRIMER PRESIDENTE AFROAMERICANO", px=66)
    pa(R, P3.bandera_eeuu(), 330, 1010, 0.9, t_pri - 0.1, FIN(e) + 0.3, sem=754, entra="sube", dy=300)


# ------------------------------------------------------------------ ACTUALIDAD
def _actualidad(R):
    e = "actualidad"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_hoy, t_tre, t_cin, t_may, t_eco = W(0, "hoy"), W(0, "trescientos"), W(0, "cincuenta"), W(0, "mayor"), W(0, "economia")
    t_ses, t_his, t_pai, t_hab, t_esp = W(1, "sesenta"), W(1, "hispanos"), W(1, "paises"), W(1, "habla"), W(1, "espanol")
    t_flo, t_cal, t_ciu, t_san, t_sfe, t_los, t_rec, t_len = (W(2, "florida"), W(2, "california"), W(2, "ciudades"), W(2, "san"), W(2, "santa"),
                                                               W(2, "los"), W(2, "recuerdan"), W(2, "lengua"))

    # cámara: el país entero -> el suroeste hispano -> de Florida a California
    R.camara(i0 - 0.3, -95.5, 37.6, 0.80)
    R.camara(t_ses, -97.0, 35.0, 0.92)
    R.camara(t_flo - 0.2, -96.0, 31.5, 1.0)
    R.camara(t_ciu, -106.0, 32.5, 1.45)
    R.camara(t_los + 0.4, -110.0, 33.0, 1.30)
    R.camara(FIN(e) + 0.4, -100.0, 34.0, 0.95)

    R.anio(i0 + 0.1, 2024)

    # frase 0: 340 millones, 50 estados, la mayor economía del mundo
    R.contador(t_tre - 0.2, t_tre + 0.9, 0, 340, (960, 196), px=82, formato="{} MILLONES", hasta_t=t_cin - 0.1)
    R.snd(t_tre - 0.2, "reloj_rapido", 0.35, dur=0.9)
    R.romper("estados", t_cin - 0.2, t_cin + 0.5, t_eco - 0.1, t_eco + 0.6, gap=10.0, deriva=18.0, fijas=(0,))
    R.snd(t_cin - 0.2, "crujido", 0.35, dur=0.7)
    R.contador(t_cin - 0.1, t_cin + 0.6, 1, 50, (960, 196), px=82, formato="{} ESTADOS", hasta_t=t_may - 0.1)
    titulo(R, t_may - 0.2, t_ses - 0.2, "LA MAYOR ECONOMÍA DEL MUNDO", px=72)
    pa(R, P3.bandera_eeuu(), 310, 1010, 1.0, t_hoy - 0.2, t_ses, sem=800, entra="sube", dy=320)
    ga(R, P3.skyline_nyc(), CI["nueva_york"], t_hoy, t_ses - 0.1, s=0.36, off=(0, -10), sem=801, zs=0.4, z=2, entra="sube", dy=240)
    ga(R, P3.golden_gate(), CI["san_francisco"], t_hoy + 0.2, t_ses - 0.1, s=0.34, off=(20, 0), sem=802, zs=0.4, z=2, entra="sube", dy=240)
    pa(R, P2.bolsa_dolares(), 1620, 1000, 0.86, t_eco - 0.3, t_ses, sem=804, entra="cae", dy=300, extra=[(0.05, "monedas", 0.45)])
    R.sello(t_may, "estrella", "HOY", color=(62, 88, 150))

    # frase 1: 65 millones de hispanos, uno de los países donde más se habla español
    R.terreno(t_ses - 0.2, "perdido_1848", (232, 168, 70), 1.0, capa=1)
    R.terreno(t_ses - 0.1, "texas_1836", (232, 168, 70), 1.0, capa=2)
    R.terreno(t_ses, "florida_1783", (232, 168, 70), 1.0, capa=3)
    R.snd(t_ses - 0.2, "whoosh", 0.4, dur=0.8)
    R.contador(t_ses - 0.2, t_his + 0.3, 0, 65, (960, 196), px=80, formato="{} MILLONES DE HISPANOS", hasta_t=t_flo - 0.2)
    pa(R, P1.ciudadana_hispana(0, "feliz"), 310, 1010, 1.06, t_ses - 0.1, t_flo, sem=810, extra=[(0.05, "fanfarria", 0.35)])
    pa(R, P1.ciudadano_hoy(1, "feliz"), 570, 1010, 1.0, t_his, t_flo, sem=811, flip=True)
    pa(R, P1.ciudadana_hispana(1, "guino"), 1620, 1010, 1.0, t_pai - 0.2, t_flo, sem=812, flip=True)
    titulo(R, t_hab - 0.3, t_flo - 0.2, "¡AQUÍ SE HABLA ESPAÑOL!", px=80, y=320)

    # frase 2: de Florida a California: San Antonio, Santa Fe, Los Ángeles
    ciudad(R, t_flo, t_ciu - 0.3, "san_agustin", "SAN AGUSTÍN", "der", 36)
    ciudad(R, t_flo + 0.1, t_ciu - 0.3, "miami", "MIAMI", "der", 36)
    ciudad(R, t_cal, t_ciu - 0.3, "san_francisco", "SAN FRANCISCO", "der", 36)
    ciudad(R, t_san - 0.2, FIN(e) + 0.3, "san_antonio", "SAN ANTONIO", "abajo", 44)
    ga(R, P2.el_alamo(), CI["san_antonio"], t_san - 0.2, FIN(e) + 0.3, s=0.40, off=(0, -30), sem=820, zs=0.45, z=2, entra="sube", dy=240,
       extra=[(0.05, "pluck", 0.35)])
    ciudad(R, t_sfe - 0.2, FIN(e) + 0.3, "santa_fe", "SANTA FE", "abajo", 44)
    ga(R, P2.mision_espanola(), CI["santa_fe"], t_sfe - 0.2, FIN(e) + 0.3, s=0.40, off=(0, -30), sem=821, zs=0.45, z=2, entra="sube", dy=240,
       extra=[(0.05, "campana", 0.35)])
    ciudad(R, t_los - 0.2, FIN(e) + 0.3, "los_angeles", "LOS ÁNGELES", "abajo", 44)
    ga(R, P3.letrero_hollywood(), CI["los_angeles"], t_los - 0.2, FIN(e) + 0.3, s=0.36, off=(0, -50), sem=822, zs=0.45, z=2, entra="sube",
       dy=240)
    for k, (c, dx) in enumerate((("phoenix", -40), ("phoenix", 70), ("las_vegas", 0))):
        ga(R, P3.saguaro(), CI[c], t_ciu + 0.15 * k, FIN(e) + 0.3, s=0.28, off=(dx, 10), sem=823 + k, zs=0.4, z=1, entra="sube", dy=200)
    pa(R, P1.fraile_franciscano(0, "feliz"), 310, 1010, 1.0, t_rec - 0.2, FIN(e) + 0.3, sem=826)
    pa(R, P1.ciudadana_hispana(0, "feliz"), 1660, 1010, 1.0, t_rec, FIN(e) + 0.3, sem=827, flip=True)
    titulo(R, t_rec - 0.1, FIN(e) + 0.2, "UNA HISTORIA ESCRITA TAMBIÉN EN ESPAÑOL", px=60)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)

    def W(i, w):
        return T(e, w, frase=i)

    t_nac, t_tre, t_bie, t_cam, t_mun = W(0, "nacion"), W(0, "trece"), W(0, "bien"), W(0, "cambio"), W(0, "mundo")
    t_que, t_dim, t_com = W(1, "que"), W(1, "dimelo"), W(1, "comentarios")

    R.camara(i0 - 0.3, -78.0, 38.5, 2.6)
    R.camara(t_bie, -95.5, 37.4, 0.76)
    R.camara(FIN(e) + 1.2, -95.3, 37.3, 0.72)

    R.anio(i0 + 0.1, 2024)

    # de las trece colonias al país de hoy
    R.terreno(i0 - 0.3, None, (232, 168, 70), 0.5, capa=1)
    R.terreno(i0 - 0.3, None, (232, 168, 70), 0.5, capa=2)
    R.terreno(i0 - 0.3, "trece", COL["colonias"], 0.6, capa=3)
    R.terreno(t_bie, None, COL["colonias"], 1.2, capa=3)
    R.snd(t_bie, "whoosh", 0.45, dur=1.0)
    R.morf(P2.bandera_13(), P3.bandera_eeuu(), t_bie, 0.9, (330, 1010, 1.05), sem=850, t_a=t_tre - 0.2, salida=t_que)
    pa(R, P3.estatua_libertad(), 1620, 1010, 0.82, t_nac, t_que, sem=852, entra="sube", dy=360)
    titulo(R, t_tre - 0.2, t_que - 0.1, "DE 13 COLONIAS A SUPERPOTENCIA", px=72)
    R.texto(t_bie - 0.1, t_que - 0.1, "PARA BIEN Y PARA MAL", (960, 320), px=56, d=0.4)
    ga(R, P3.capitolio(), CI["washington"], t_cam - 0.2, t_que - 0.1, s=0.30, off=(0, -10), sem=853, zs=0.4, z=2, entra="sube", dy=240)
    ga(R, P3.golden_gate(), CI["san_francisco"], t_cam, t_que - 0.1, s=0.30, off=(20, 0), sem=854, zs=0.4, z=2, entra="sube", dy=240)

    # pregunta final y llamada a la acción
    titulo(R, t_que, FIN(e) + 1.2, "¿QUÉ PAÍS O IMPERIO SIGUE?", px=78)
    R.texto(t_dim, FIN(e) + 1.1, "¡DÍMELO ABAJO!", (1520, 320), px=56, d=0.4)
    R.texto(t_com - 0.2, FIN(e) + 1.1, "SUSCRÍBETE", (680, 320), px=68, d=0.5)
    pa(R, C.campana(), 1050, 315, 0.82, t_com - 0.3, FIN(e) + 1.2, sem=860, extra=[(0.08, "campana", 0.5)])
    pa(R, P1.ciudadano_hoy(0, "feliz"), 330, 1010, 1.0, t_que - 0.1, FIN(e) + 1.2, sem=861)
    pa(R, P1.ciudadana_hispana(0, "guino"), 1620, 1010, 1.0, t_que + 0.2, FIN(e) + 1.2, sem=862, flip=True)


# ------------------------------------------------------------------ cambios de escena procedurales
def _transiciones(R):
    tipos = ["tinta", "pincel", "papel", "portal", "rollo", "puntos", "ola", "pincel", "tinta", "papel", "persianas", "portal", "rollo"]
    colores = [
        (176, 112, 64), (196, 70, 62), (62, 88, 150), (196, 132, 70), (110, 116, 128), (196, 132, 60), (122, 126, 78),
        (176, 64, 58), (92, 120, 160), (72, 150, 150), (62, 88, 150), (196, 70, 62), (220, 176, 74),
    ]
    ids = [e["id"] for e in __import__("escena_base").TL["escenas"]]
    centros = [(FIN(a) + INI(b)) / 2 for a, b in zip(ids, ids[1:])]
    for k, tc in enumerate(centros):
        tipo, color = tipos[k % len(tipos)], colores[k % len(colores)]
        R.trans.append(Transicion(tc, tipo, color, (960, 540), (960, 540), dur=0.8, seed=k + 1))
        R.snd(tc - 0.4, SFX[tipo], 0.45, dur=0.8)
