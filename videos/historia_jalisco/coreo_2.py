# -*- coding: utf-8 -*-
"""Coreografía (2/4): Guadalajara (las cuatro fundaciones y Atemajac 1542, capital de la Nueva Galicia, catedral, camino de la plata,
haciendas, el tequila de 1795, la universidad y el Hospicio Cabañas), la Independencia (el Amo Torres, Hidalgo en Guadalajara y la
abolición, El Despertador Americano, Puente de Calderón, 1821) y el federalismo (Estado Libre de Jalisco, 1823)."""
import obj_c as C
from core import FIN, INI, T
from coreo_peg import PERIODICO, C_INSURG, CO, IN, SI, XI, XX, grupo_ciclo
from coreo_util import CI, COL, ciudad, ga, lugar, pa, titulo
import mapa as M


def cortes(R):
    pass


def construir(R):
    _guadalajara(R)
    _independencia(R)
    _federalismo(R)


# ------------------------------------------------------------------ GUADALAJARA COLONIAL
def _guadalajara(R):
    e = "guadalajara"
    i0 = INI(e)
    t_mud, t_tres, t_mil, t_ase, t_val, t_ate = (T(e, "mudarse"), T(e, "tres"), T(e, "mil"), T(e, "asienta"), T(e, "valle"),
                                                 T(e, "atemajac"))
    t_cap, t_tri, t_cat, t_cam, t_min, t_pla = (T(e, "capital"), T(e, "tribunal"), T(e, "catedral"), T(e, "camino"), T(e, "minas"),
                                                T(e, "plata"))
    t_hac, t_gan, t_cab, t_des, t_aga, t_mil2, t_lic, t_rey, t_teq = (T(e, "haciendas"), T(e, "ganado"), T(e, "caballo"), T(e, "destila"),
                                                                       T(e, "agave"), T(e, "mil", frase=2), T(e, "licencia"), T(e, "rey"),
                                                                       T(e, "tequila"))
    t_sig, t_uni, t_hos, t_nin, t_cbn = T(e, "siglo"), T(e, "universidad"), T(e, "hospicio"), T(e, "ninos"), T(e, "cabanas")

    R.camara(i0 - 0.2, -103.1, 21.0, 2.0)
    R.camara(t_ase - 0.2, -103.2, 20.9, 2.1)
    R.camara(t_ate - 0.1, -103.36, 20.69, 3.0)
    R.camara(t_cam - 0.2, -103.36, 20.69, 2.8)
    R.camara(t_min + 0.3, -102.9, 21.7, 1.3)
    R.camara(t_hac - 0.1, -103.0, 21.2, 1.4)
    R.camara(t_des + 0.2, -103.7, 20.85, 2.8)
    R.camara(t_sig - 0.1, -103.6, 20.8, 2.7)
    R.camara(t_sig + 0.5, -103.36, 20.68, 3.6)
    R.camara(FIN(e) + 0.4, -103.36, 20.68, 3.8)

    R.anio(i0, 1532)
    R.terreno(i0 - 0.1, "nueva_galicia", COL["nueva_galicia"], 0.6)
    # frase 0: cuatro fundaciones y Atemajac
    for k, (c, txt) in enumerate((("nochistlan", "1. NOCHISTLÁN"), ("tonala", "2. TONALÁ"), ("tlacotan", "3. TLACOTÁN"), ("atemajac", "4. ATEMAJAC"))):
        ciudad(R, t_mud - 0.2 + 0.55 * k, t_ase - 0.15, c, txt, "der" if k != 1 else "abajo", 36)
    R.ruta(M.RUTAS["gdl_mudanzas"], t_mud - 0.1, 2.4, ancho=4.0, t1=t_cap - 0.1, flecha=True)
    R.act(SI(7), pos_geo=R.camino_pos(M.RUTAS["gdl_mudanzas"], t_mud - 0.1, 2.4), off=(0, -6), s=0.5, t_in=t_mud - 0.2, d_in=0.3,
          entra="pop", sem=100, zs=0.4, z=3, t_out=t_ase, sale="encoger")
    R.snd(t_mud, "pasos", 0.3, dur=2.0)
    R.anio(t_mil, 1542)
    ga(R, CO(0), CI["guadalajara"], t_ase - 0.1, FIN(e) + 0.3, s=0.7, off=(0, 10), sem=101, zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "campana", 0.35)])
    titulo(R, t_val - 0.1, t_cap - 0.2, "VALLE DE ATEMAJAC · 1542", px=72, snd=True)

    # frase 1: capital del occidente
    R.sello(t_cap, "corona", "NUEVA GALICIA", color=(214, 156, 58))
    for k, (dx, dy) in enumerate(((-210, 60), (190, 70), (-120, 140), (120, 150))):
        ga(R, SI(7), CI["guadalajara"], t_cap + 0.12 * k, FIN(e) + 0.3, s=0.36, off=(dx, dy), sem=125 + k, zs=0.4, z=1)
    pa(R, CO(8), 1600, 1010, 0.95, t_tri - 0.1, t_hac - 0.1, sem=129)
    pa(R, CO(7), 330, 1010, 0.72, t_tri - 0.15, t_hac - 0.1, sem=103, entra="sube", dy=300)
    R.texto(t_tri, t_hac - 0.2, "REAL AUDIENCIA", (330, 640), px=46, d=0.4)
    R.texto(t_cat, t_cam + 0.4, "CATEDRAL", (960, 196), px=70, d=0.4)
    R.ruta(M.RUTAS["camino_plata"], t_cam - 0.1, 2.2, ancho=4.5, t1=t_hac, flecha=True)
    R.act(CO(4), pos_geo=R.camino_pos(M.RUTAS["camino_plata"], t_cam, 2.6), off=(0, 0), s=0.4, t_in=t_cam, d_in=0.3, entra="pop", sem=104,
          zs=0.4, z=3, t_out=t_hac)
    ciudad(R, t_min, t_hac, "zacatecas", "MINAS DE ZACATECAS", "abajo", 40)
    pa(R, CO(4), 1240, 1010, 0.85, t_pla - 0.15, t_hac - 0.1, sem=105, extra=[(0.05, "monedas", 0.4)])

    # frase 2: haciendas, caballos y tequila
    for k, off in enumerate(((-120, 40), (110, 20))):
        ga(R, CO(3), CI["tepatitlan"] if k == 0 else CI["lagos_moreno"], t_hac - 0.1 + 0.15 * k, t_des, s=0.42, off=off, sem=106 + k, zs=0.4, z=2)
    pa(R, XX(5), 330, 1010, 1.05, t_cab - 0.2, t_lic, sem=108, extra=[(0.05, "galope", 0.35, {"dur": 0.8})])
    for k, (dx, dy) in enumerate(((-150, 40), (-40, 70), (80, 50), (190, 30), (-90, 110), (60, 120))):
        ga(R, SI(4), CI["tequila"], t_aga - 0.1 + 0.06 * k, t_sig, s=0.3, off=(dx, dy), sem=110 + k, zs=0.4, z=1)
    ga(R, CO(5), CI["tequila"], t_des, t_sig, s=0.42, off=(-40, -30), sem=117, zs=0.4, z=2)
    ga(R, CO(6), CI["tequila"], t_des + 0.15, t_sig, s=0.30, off=(60, -20), sem=118, zs=0.4, z=2)
    R.anio(t_mil2, 1795)
    pa(R, CO(8), 1600, 1010, 0.95, t_rey - 0.2, t_sig, sem=119, extra=[(0.05, "fanfarria", 0.3)])
    pa(R, CO(7), 1360, 1010, 0.5, t_lic - 0.1, t_sig, sem=120)
    titulo(R, t_teq - 0.05, t_sig - 0.1, "TEQUILA · 1795", px=82, snd=True)

    # frase 3: universidad y Hospicio Cabañas
    R.anio(t_sig, 1792)
    pa(R, CO(2), 340, 1010, 0.75, t_uni - 0.15, FIN(e) + 0.3, sem=122, entra="sube", dy=320)
    R.texto(t_uni, FIN(e) + 0.2, "UNIVERSIDAD · 1792", (340, 650), px=44, d=0.4)
    R.anio(t_hos, 1805)
    pa(R, CO(1), 1000, 1010, 1.05, t_hos - 0.2, FIN(e) + 0.3, sem=123, entra="sube", dy=360, extra=[(0.05, "crece", 0.45)])
    pa(R, XI(3), 1620, 1010, 0.6, t_nin - 0.1, FIN(e) + 0.3, sem=124)
    titulo(R, t_cbn - 0.15, FIN(e) + 0.3, "HOSPICIO CABAÑAS", px=82)


# ------------------------------------------------------------------ INDEPENDENCIA
def _independencia(R):
    e = "independencia"
    i0 = INI(e)
    t_mil, t_est, t_amo, t_tom, t_ins = T(e, "mil"), T(e, "estalla"), T(e, "amo"), T(e, "toma"), T(e, "insurgentes")
    t_hid, t_ciu, t_abo, t_esc, t_lan, t_per, t_des = (T(e, "hidalgo"), T(e, "ciudad"), T(e, "abolicion"), T(e, "esclavitud"),
                                                       T(e, "lanza"), T(e, "periodico"), T(e, "despertador"))
    t_ene, t_pue, t_cal, t_rea, t_sei, t_dis, t_dec = (T(e, "enero"), T(e, "puente"), T(e, "calderon"), T(e, "realista"), T(e, "seis"),
                                                       T(e, "dispersa"), T(e, "decenas"))
    t_gue, t_mil3, t_mex, t_ind = T(e, "guerra"), T(e, "mil", frase=3), T(e, "mexico", frase=3), T(e, "independiente")

    R.camara(i0 - 0.2, -103.3, 20.5, 1.8)
    R.camara(t_tom + 0.2, -103.35, 20.62, 2.6)
    R.camara(t_hid - 0.1, -102.6, 20.3, 1.6)
    R.camara(t_ciu + 0.3, -103.3, 20.66, 3.2)
    R.camara(t_ene - 0.1, -103.25, 20.63, 3.0)
    R.camara(t_pue + 0.2, -103.02, 20.62, 4.0)
    R.camara(t_gue - 0.1, -102.9, 20.7, 2.0)
    R.camara(t_mil3 + 0.2, -103.1, 20.9, 0.98)
    R.camara(FIN(e) + 0.4, -103.1, 20.9, 0.96)

    R.anio(i0, 1810)
    pa(R, C.campana(), 960, 900, 1.3, i0 - 0.1, t_amo, sem=128, extra=[(0.05, "campana", 0.4)])
    R.sello(t_est, "campana", "INDEPENDENCIA", color=(74, 146, 98))
    R.snd(t_est - 0.1, "campana", 0.45)
    # frase 0: el Amo Torres toma Guadalajara
    R.terreno(t_est, "insurgentes", COL["insurgentes"], 1.6)
    pa(R, IN(1), 330, 1010, 1.05, t_amo - 0.15, t_hid - 0.1, sem=130)
    R.texto(t_amo + 0.05, t_hid - 0.2, "EL AMO TORRES", (330, 560), px=46, d=0.4)
    R.ruta(M.RUTAS["torres"], t_amo, 1.6, ancho=4.5, t1=t_hid, flecha=True)
    grupo_ciclo(R, C_INSURG, M.RUTAS["torres"], t_amo, 2.0, n=4, ancho=70, t1=t_hid + 0.3, s=0.48, sem=131,
                extra=[(0.05, "pasos", 0.3, {"dur": 1.6})])
    ciudad(R, t_tom, t_ene - 0.2, "guadalajara", "GUADALAJARA", "abajo", 42)

    # frase 1: Hidalgo, la abolición y El Despertador Americano
    R.ruta(M.RUTAS["hidalgo"], t_hid - 0.2, 1.8, ancho=4.5, t1=t_ene, flecha=True)
    pa(R, IN(0), 1600, 1010, 1.05, t_hid - 0.15, t_ene - 0.1, sem=135, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_hid + 0.1, t_ene - 0.2, "MIGUEL HIDALGO", (1600, 560), px=46, d=0.4)
    pa(R, IN(10), 900, 1000, 0.62, t_abo - 0.15, t_per, sem=136, extra=[(0.05, "crujido", 0.45)])
    pa(R, IN(11), 1080, 960, 0.55, t_esc - 0.1, t_per, sem=137)
    titulo(R, t_abo, t_lan, "ABOLICIÓN DE LA ESCLAVITUD · 1810", px=64, snd=True)
    pa(R, PERIODICO, 960, 1010, 0.95, t_per - 0.15, t_ene - 0.1, sem=138, entra="sube", dy=320, extra=[(0.05, "pincel", 0.3)])
    titulo(R, t_des - 0.1, t_ene - 0.15, "EL DESPERTADOR AMERICANO", px=68)
    pa(R, IN(3), 330, 1010, 0.95, t_ciu, t_ene - 0.1, sem=139)

    # frase 2: Puente de Calderón
    R.anio(t_ene, 1811)
    R.ruta(M.RUTAS["calleja"], t_ene, 2.2, ancho=5.0, t1=t_gue, flecha=True)
    ga(R, IN(13), CI["puente_calderon"], t_pue - 0.1, t_gue + 0.2, s=0.75, off=(0, 20), sem=140, zs=0.4, z=2, entra="sube", dy=300,
       extra=[(0.05, "canonazo", 0.45)])
    lugar(R, t_cal, t_gue, "PUENTE DE CALDERÓN", CI["puente_calderon"], off=(0, 70), px=42)
    ga(R, IN(12), CI["puente_calderon"], t_rea - 0.1, t_gue + 0.2, s=0.42, off=(230, 40), sem=141, zs=0.4, z=3, flip=True,
       extra=[(0.1, "canonazo", 0.4)])
    pa(R, IN(2), 1600, 1010, 1.05, t_ene - 0.1, t_gue, sem=142, extra=[(0.05, "tambor", 0.35)])
    R.texto(t_ene + 0.1, t_gue - 0.1, "CALLEJA", (1600, 560), px=46, d=0.4)
    R.contador(t_sei - 0.1, t_sei + 0.6, 0, 6000, (1600, 470), px=58, formato="{:,} REALISTAS", hasta_t=t_gue)
    R.terreno(t_dis - 0.1, None, COL["insurgentes"], 0.8)
    grupo_ciclo(R, C_INSURG, [(-103.0, 20.6), (-103.5, 20.4)], t_dis - 0.1, 2.2, n=5, ancho=65, t1=t_gue + 0.2, s=0.45, sem=143, fps=13)
    pa(R, IN(3), 330, 1010, 1.0, t_dec - 0.1, t_gue, sem=148, sale="izq_fuera")

    # frase 3: 1821
    R.anio(t_mil3, 1821)
    R.terreno(t_mil3 - 0.1, "mexico_mod", COL["mexico_mod"], 1.0)
    titulo(R, t_ind - 0.15, FIN(e) + 0.3, "MÉXICO INDEPENDIENTE · 1821", px=74, snd=True)
    pa(R, IN(1), 330, 1010, 0.95, t_gue, FIN(e) + 0.3, sem=149)
    pa(R, IN(3), 1600, 1010, 0.95, t_gue + 0.2, FIN(e) + 0.3, sem=150, flip=True)
    R.terreno(FIN(e) + 0.4, None, COL["mexico_mod"], 0.3)


# ------------------------------------------------------------------ FEDERALISMO
def _federalismo(R):
    e = "federalismo"
    i0 = INI(e)
    t_mil, t_ade, t_pro, t_est, t_jal = T(e, "mil"), T(e, "adelanta"), T(e, "proclama"), T(e, "estado"), T(e, "jalisco")
    t_exi, t_fed, t_est2, t_cen = T(e, "exige"), T(e, "federacion"), T(e, "estados"), T(e, "centralista")
    t_cuna, t_fed2 = T(e, "cuna"), T(e, "federalismo")

    R.camara(i0 - 0.2, -103.4, 20.8, 1.2)
    R.camara(t_exi - 0.1, -103.2, 20.8, 1.15)
    R.camara(t_fed + 0.3, -102.6, 20.9, 0.95)
    R.camara(FIN(e) + 0.4, -102.8, 20.9, 0.98)

    R.anio(i0, 1823)
    R.sello(t_pro, "balanza", "ESTADO LIBRE", color=(204, 72, 58))
    ga(R, XI(5), CI["guadalajara"], t_ade - 0.1, FIN(e) + 0.3, s=0.5, off=(0, 0), sem=160, zs=0.4, z=2, entra="sube", dy=280)
    pa(R, XI(0), 330, 1010, 1.05, i0 - 0.1, FIN(e) + 0.3, sem=161, extra=[(0.05, "fanfarria", 0.3)])
    R.texto(t_ade + 0.1, t_cuna, "PRISCILIANO SÁNCHEZ", (330, 560), px=42, d=0.4)
    R.terreno(t_est - 0.1, "jalisco", COL["estado_libre"], 0.8)
    titulo(R, t_est - 0.1, t_exi + 0.3, "ESTADO LIBRE DE JALISCO", px=78, snd=True)

    # frase 1: federación de estados libres (cada vecino toma su color)
    for k, (campo, nombre) in enumerate((("edo_nayarit", "Nayarit"), ("edo_zacatecas", "Zacatecas"), ("edo_aguascalientes", "Aguascalientes"),
                                         ("edo_guanajuato", "Guanajuato"), ("edo_michoacan", "Michoacán"), ("edo_colima", "Colima"),
                                         ("resto_mx", "México"))):
        R.terreno(t_fed - 0.2 + 0.16 * k, campo, M.COL_ESTADOS[nombre], 0.6, capa=1 + k)
    R.snd(t_fed - 0.2, "crece", 0.4, dur=1.2)
    titulo(R, t_fed, t_cuna - 0.2, "FEDERACIÓN DE ESTADOS", px=74)
    pa(R, XI(6), 1600, 1010, 0.72, t_exi - 0.1, FIN(e) + 0.3, sem=162, entra="sube", dy=300)
    pa(R, XI(7), 1440, 840, 0.38, t_est2, FIN(e) + 0.3, sem=163)
    R.texto(t_cen - 0.05, t_cuna - 0.2, "NO AL CENTRALISMO", (1600, 640), px=40, d=0.4)

    # frase 2: cuna del federalismo
    titulo(R, t_cuna - 0.1, FIN(e) + 0.3, "CUNA DEL FEDERALISMO", px=84, snd=True)
    for c in range(1, 8):
        R.terreno(FIN(e) + 0.35, None, (0, 0, 0), 0.3, capa=c)
