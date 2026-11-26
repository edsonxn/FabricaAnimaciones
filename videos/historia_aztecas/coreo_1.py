# -*- coding: utf-8 -*-
"""Coreografía (1/4) de «Toda la historia de los AZTECAS»: gancho (1519: la calzada, la ciudad sobre el agua, «dos siglos antes»
un islote; presentación de Xolo), Aztlán (aztecas = mexicas, Aztlán sin ubicar, Huitzilopochtli, la promesa del águila, la caminata
por la ruta `migracion`, Coatepec: Coatlicue, Coyolxauhqui cayendo del cerro, Tula), Chapultepec (el valle con sus ciudades,
el cerro del chapulín, la expulsión, Huitzilíhuitl, Tizapán y las víboras, la hija del señor de Culhuacán = Toci, la huida al lago) y
la fundación (1325: el águila con el pájaro, sola en el Códice Mendoza y con la serpiente en la bandera; islote_1325 → isla_1325;
Tlatelolco 1337). Xolo sale en cada escena. Pegatinas de Flow (`pegflow.P`) y fotos reales (`foto_peg`).
Capas de terreno propias: 1 (imperio en el gancho), 11 (isla de Tenochtitlan), 12 (Tlatelolco), 50 (agua que tapa la isla de 1519).
Semillas 1-299."""
import math

import foto_peg as FP
import mapa as M
import obj_a as A
from core import FIN, INI, T
from coreo_peg import andar_ciclo, ciclo_pant, grupo_ciclo
from coreo_util import CI, COL, ciudad, formacion, ga, lugar, pa, titulo, tramo
from pegflow import P, ciclo

XO = lambda n, **k: P("01_xolo_hoja", n, **k)          # 0 sentado orgulloso, 1 camina, 2 asustado, 3 bajo el petate, 4 aúlla, 5 salta, 6 duerme, 7 receloso
MI = lambda n, **k: P("02_migracion_hoja", n, **k)     # 0 peregrino, 1 peregrina, 2 sacerdote con bulto, 3 Huitzilopochtli, 4 Coatlicue, 5 Coyolxauhqui cae, 6 Aztlán, 7 atlante
CH = lambda n, **k: P("03_chapultepec_hoja", n, **k)   # 0 cerro del chapulín, 1 vecino enojado, 2 jefe prisionero, 3 señor de Culhuacán, 4 víboras, 5 asa víbora, 6 fogata, 7 princesa, 8 canoa en juncos
FU = lambda n, **k: P("04_fundacion_hoja", n, **k)     # 0 águila con pájaro, 1 águila con serpiente, 2 islote con garza, 3 choza, 4 templito, 5 pescador, 6-7 discuten, 8 pato, 9 patos
CO = lambda n, **k: P("14_cortes_hoja", n, **k)        # 0 soldado, 1 nao, 2 jinete, 8 soldado con los brazos arriba
AH = lambda n, **k: P("12_ahuizotl_hoja", n, **k)      # 1 templo doble, 6-7 chozas con canoa
MO = lambda n, **k: P("13_moctezuma2_hoja", n, **k)    # 0 Moctezuma II, 7 Tenochtitlan en el lago
VI = lambda n, **k: P("08_vida_hoja", n, **k)          # 0 macehual, 2 noble, 3 cargador, 7 mujer, 12 mantas
MC = lambda n, **k: P("18_mictlan_hoja", n, **k)       # 5 Xolo nervioso, 6 olla
RU = lambda n, **k: P("17_ruta_hoja", n, **k)          # 1 trabajador de 1978, 2 Coyolxauhqui de piedra
LE = lambda n, **k: P("16_legado_hoja", n, **k)        # 11 bandera
CN = lambda n, **k: P("05_chinampas_hoja", n, **k)     # 7 guerrero mercenario
CA = lambda n, **k: P("15_caida_hoja", n, **k)         # 1 danzante
C_XOLO = ciclo("19_xolo_corre")
C_MEX = ciclo("20_mexica_camina")
C_CANOA = ciclo("21_canoa_ciclo")
C_CAB = ciclo("22_caballo_galope")
C_GUE = ciclo("23_guerrero_corre")

RUTA = M.RUTAS["migracion"]
AGUA = COL["agua_isla_1325"]
ISLA = (196, 96, 60)          # tinte de la isla recién fundada (rojo almagre suave sobre el guache de la isla)
TLAT = (214, 150, 70)


def cortes(R):
    pass


def construir(R):
    _fondos(R)
    _gancho(R)
    _aztlan(R)
    _chapultepec(R)
    _fundacion(R)


# ------------------------------------------------------------------ utilidades
def paseo(R, t0, t1, lon, lat, z, paso=2.1, px=36, dz=0.05, fase=0.0):
    """Claves de cámara cada ~2 s alrededor de un punto (vaivén suave de ±px de pantalla): nunca queda quieta."""
    n = max(1, int((t1 - t0) / paso))
    for k in range(n + 1):
        t = t0 + (t1 - t0) * k / n
        a = fase + 1.9 * k
        g = px / (z * M.PXDEG_REF)
        R.camara(t, lon + g * math.cos(a), lat + 0.6 * g * math.sin(a), z * (1 + dz * math.sin(a * 0.7)))


def cae(x0, y0, x1, y1, t0, dur, s, giro=2.4):
    """Posición (x, y, s, rot) de algo que rueda cerro abajo entre t0 y t0+dur (aceleración tipo caída, giro continuo)."""
    def f(t):
        u = min(1.0, max(0.0, (t - t0) / dur))
        uu = u * u
        return (x0 + (x1 - x0) * u, y0 + (y1 - y0) * uu - 60 * math.sin(math.pi * u), s, giro * uu * math.pi)
    return f


def _fondos(R):
    """Calzadas de 1519 (solo en el gancho) y rótulos de los lagos cuando se ve el valle entero."""
    def calz(img, cam, t, fs):
        if not (4.5 <= t <= 28.0):
            return
        a = min(1.0, (t - 4.5) / 1.5) * (1.0 - min(1.0, max(0.0, (t - 26.4) / 1.2)))
        M.pintar_calzadas(img, cam, alfa=a)
    R.fondo.append(("mx", calz))

    def lagos(img, cam, t, fs):
        for ta, tb in ((153.0, 164.0),):
            if ta <= t <= tb and cam.z < 9:
                a = 0.55 * min(1.0, (t - ta) / 0.8) * (1.0 - min(1.0, max(0.0, (t - tb + 0.8) / 0.8)))
                for n, (lo, la) in M.LAGOS_ROT.items():
                    M.rotulo_mapa(img, n, cam, lo, la, 24, a, rot=0.0)
    R.fondo.append(("mx", lagos))


# ------------------------------------------------------------------ GANCHO (0-60 s)
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_1519, t_400, t_sol, t_calz, t_lago, t_cre = (T(e, "1519"), T(e, "cuatrocientos"), T(e, "soldados"), T(e, "calzada"),
                                                    T(e, "lago"), T(e, "podian"))
    t_ciu, t_tem, t_can, t_cnoa, t_gen, t_eur = (T(e, "una ciudad"), T(e, "templos"), T(e, "canales"), T(e, "canoas"), T(e, "gente"),
                                                 T(e, "europa"))
    t_esc, t_enc, t_lib = T(e, "escribio"), T(e, "encantamiento"), T(e, "libros")
    t_dos, t_nada, t_isl, t_jun, t_tri, t_nad = (T(e, "dos siglos"), T(e, "nada"), T(e, "islote"), T(e, "juncos"), T(e, "tribu"),
                                                 T(e, "nadie"))
    t_his, t_per, t_imp, t_cai, t_dos2 = (T(e, "historia completa"), T(e, "peregrinacion"), T(e, "imperio"), T(e, "caida"),
                                          T(e, "dos anos"))
    t_aco, t_alg, t_xolo = T(e, "acompanar"), T(e, "alguien"), T(e, "xolo", frase=5)
    t_xit, t_pelo, t_leal, t_siem, t_paso, t_menu = (T(e, "xoloitzcuintle"), T(e, "pelo"), T(e, "leal"), T(e, "siempre"),
                                                     T(e, "paso"), T(e, "menu"))
    TEN = CI["tenochtitlan"]

    # apertura: México entero → zoom al Valle de México (la cámara de la coreografía en t = 6)
    R.ubic.apertura(0.0, 6.0)
    R.camara(0.5, -99.05, 19.45, 6.2)
    R.camara(6.0, -99.05, 19.45, 6.2)
    R.camara(8.6, -99.10, 19.40, 11.0)
    R.camara(t_ciu, -99.122, 19.422, 17.0)
    paseo(R, t_ciu + 2.0, t_dos - 0.3, -99.131, 19.431, 19.0, px=40)
    R.camara(t_dos + 0.3, -99.133, 19.440, 26.0)
    R.camara(t_isl, -99.134, 19.444, 34.0)
    R.camara(t_jun + 0.6, -99.133, 19.443, 32.0)
    R.camara(t_tri + 0.2, -99.128, 19.430, 26.0)
    R.camara(t_nad + 0.6, -99.10, 19.42, 12.0)
    R.camara(t_his + 0.6, -98.8, 19.1, 2.6)
    R.camara(t_imp - 0.3, -97.85, 18.15, 0.86)
    R.camara(t_cai, -97.80, 18.12, 0.82)
    R.camara(t_aco, -98.9, 19.3, 2.4)
    R.camara(t_alg + 0.3, -99.05, 19.45, 5.6)
    paseo(R, t_xolo - 0.3, FIN(e) - 0.6, -99.05, 19.45, 6.2, px=30)

    # frase 0: 8 de noviembre de 1519, 400 soldados por la calzada… no podían creer lo que veían
    R.anio(t_1519, 1519)
    pa(R, XO(7), 1830, 1020, 0.42, i0, t_cre - 0.1, sem=2, flip=True)          # Xolo ya está ahí (la cartela de la apertura ocupa el centro)
    pa(R, CO(0), 1620, 1010, 0.95, 2.2, t_cre - 0.15, sem=1, extra=[(0.05, "golpe_suave", 0.3)])
    R.contador(t_400 - 0.1, t_sol + 0.5, 0, 400, (960, 196), px=70, formato="{:,} SOLDADOS", hasta_t=t_calz + 0.4)
    R.snd(t_sol, "pasos", 0.35, dur=1.4)
    cal = list(reversed(M.LINEAS["calzada_iztapalapa"]))           # de Iztapalapa hacia la isla
    andar_ciclo(R, C_CAB, cal, t_calz - 0.3, 14.0, t1=t_esc - 0.2, s=0.26, sem=3, fps=8, zs=0.45,
                extra=[(0.05, "galope", 0.25, {"dur": 1.2})])
    for k in range(4):
        R.act(CO(0), pos_geo=R.camino_pos(cal, t_calz - 0.1 + 0.25 * k, 14.0), off=(-40 - 34 * k, 6 * (k % 2)), s=0.17, t_in=t_calz + 0.25 * k,
              d_in=0.3, entra="pop", sem=4 + k, zs=0.45, z=1, t_out=t_esc - 0.2, flip=True)
    lugar(R, t_lago, t_ciu - 0.1, "CALZADA DE IZTAPALAPA", CI["iztapalapa"], off=(150, 70), px=40)
    pa(R, CO(8), 1620, 1010, 0.95, t_cre - 0.1, t_ciu + 0.2, sem=8, extra=[(0.05, "brillo", 0.35)])

    # frase 1: una ciudad sobre el agua, templos blancos, canales y canoas, más gente que casi cualquier ciudad de Europa
    ga(R, AH(1), TEN, t_ciu - 0.1, t_dos - 0.2, s=0.34, off=(0, 20), sem=9, zs=0.5, z=2, entra="sube", dy=200,
       extra=[(0.05, "crece", 0.35)])
    lugar(R, t_ciu + 0.2, t_gen - 0.2, "TENOCHTITLAN", TEN, off=(0, -320), px=52)
    pa(R, FP.F("nuremberg_1524"), 1440, 975, FP.s_para(0.46), t_ciu + 0.3, t_tem + 0.4, entra="pluma", sem=10, z=4,
       extra=[(0.05, "papel", 0.3)])
    ga(R, AH(6), CI["tlatelolco"], t_tem, t_dos - 0.2, s=0.13, off=(-60, 30), sem=11, zs=0.5)
    ga(R, AH(7), (-99.116, 19.418), t_tem + 0.3, t_dos - 0.2, s=0.13, off=(40, 30), sem=12, zs=0.5)
    pa(R, FP.F("maqueta_tenochtitlan"), 480, 970, FP.s_para(0.42), t_tem + 0.6, t_esc - 0.3, entra="pluma", sem=13, z=4)
    R.texto(t_tem + 0.6, t_esc - 0.4, "templos blancos", (480, 420), px=46, d=0.4)
    for k, (P0, P1) in enumerate((((-99.052, 19.456), (-99.064, 19.430)), ((-99.072, 19.405), (-99.094, 19.396)))):
        andar_ciclo(R, C_CANOA, [P0, P1], t_can - 0.2 + 0.4 * k, 9.0, t1=t_dos - 0.2, s=0.19, sem=14 + k, fps=6, zs=0.45, z=2,
                    extra=[(0.05, "remo", 0.3)] if k == 0 else ())
    R.snd(t_cnoa, "agua_lago", 0.25, dur=3.0)
    pa(R, VI(0), 1380, 1010, 0.72, t_gen - 0.1, t_lib - 0.2, sem=16)
    pa(R, VI(7), 1560, 1015, 0.70, t_gen + 0.1, t_lib - 0.2, sem=17, flip=True)
    pa(R, VI(3), 1740, 1010, 0.70, t_gen + 0.25, t_lib - 0.2, sem=18, extra=[(0.05, "multitud", 0.2, {"dur": 2.5})])
    R.texto(t_eur - 0.1, t_enc - 0.4, "más gente que casi cualquier ciudad de Europa", (960, 196), px=50, d=0.6)  # noqa

    # frase 2: «cosa de encantamiento», como en los libros de caballerías
    pa(R, CO(0), 330, 1010, 1.0, t_esc - 0.1, t_dos - 0.1, sem=19, extra=[(0.05, "escribir", 0.3, {"dur": 0.8})])
    R.texto(t_esc + 0.2, t_dos - 0.3, "UN SOLDADO: BERNAL DÍAZ", (330, 550), px=36, d=0.4)
    R.texto(t_enc - 0.1, t_dos - 0.3, "«COSA DE ENCANTAMIENTO»", (960, 196), px=78, d=0.8)
    R.snd(t_enc, "brillo", 0.45)
    ga(R, lambda t: A.estallido(10, 30, 90), TEN, t_enc, t_lib + 0.6, s=0.7, off=(0, -170), sem=20, zs=0.0, z=1)
    pa(R, C_CAB[1], 1600, 1010, 1.05, t_lib - 0.1, t_dos - 0.1, sem=21, extra=[(0.05, "galope", 0.3, {"dur": 0.8})])
    R.texto(t_lib + 0.2, t_dos - 0.3, "libros de caballerías", (1600, 560), px=40, d=0.4)

    # frase 3: dos siglos antes no había nada: un islote de juncos… y una tribu que nadie quería de vecina
    R.anio(t_dos + 0.1, 1300)
    R.terreno(t_dos - 0.1, "agua_isla_1325", AGUA, 1.4, capa=50)     # la isla de 1519 se hunde: queda el islote
    R.snd(t_dos, "whoosh", 0.4)
    R.snd(t_nada, "agua_lago", 0.35, dur=3.0)
    R.texto(t_dos + 0.1, t_his - 0.3, "DOS SIGLOS ANTES…", (960, 196), px=72, d=0.6)
    ga(R, FU(2), TEN, t_nada - 0.3, t_his - 0.2, s=0.34, off=(0, 40), sem=22, zs=0.3, z=2, entra="sube", dy=160)
    ga(R, FU(8), (-99.129, 19.432), t_jun - 0.2, t_his - 0.2, s=0.30, off=(0, 30), sem=23, zs=0.3)
    ga(R, FU(8), (-99.138, 19.438), t_jun, t_his - 0.2, s=0.28, off=(0, 30), sem=24, zs=0.3, flip=True)
    pa(R, MI(0), 300, 1010, 0.95, t_tri - 0.2, t_per - 0.3, sem=25, extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    pa(R, MI(1), 520, 1015, 0.88, t_tri, t_per - 0.3, sem=26)
    pa(R, XO(1), 710, 1020, 0.48, t_tri + 0.3, t_per - 0.3, sem=27)
    pa(R, CH(1), 1620, 1010, 1.0, t_nad - 0.1, t_imp - 0.1, sem=28, flip=True, extra=[(0.05, "impacto", 0.3)])
    R.texto(t_nad + 0.2, t_his - 0.3, "¡NI LOS QUIERO DE VECINOS!", (1560, 530), px=34, d=0.4)

    # frase 4: la historia completa: peregrinación → imperio → caída en dos años
    titulo(R, t_his - 0.1, t_aco - 0.3, "TODA LA HISTORIA DE LOS AZTECAS", px=82, snd=True)
    ciclo_pant(R, C_MEX, 220, 900, 1010, t_per - 0.2, 3.0, t1=t_imp + 0.4, s=0.8, sem=29)
    R.texto(t_per, t_imp - 0.1, "una peregrinación sin rumbo", (960, 300), px=50, d=0.5)
    R.terreno(t_imp - 0.2, "imperio_1519", COL["imperio_1519"], 1.0, capa=1)
    R.snd(t_imp, "tambor", 0.4, dur=1.2)
    pa(R, MO(0), 1600, 1010, 1.0, t_imp + 0.1, t_cai + 0.4, sem=30, extra=[(0.05, "caracol", 0.3)])
    R.texto(t_imp + 0.4, t_cai - 0.2, "el imperio más poderoso de Mesoamérica", (960, 300), px=48, d=0.5)
    pa(R, CO(0), 360, 1010, 1.0, t_cai - 0.1, t_aco - 0.1, sem=31, extra=[(0.05, "canonazo", 0.3)])
    pa(R, CO(1), 640, 1000, 0.7, t_cai + 0.2, t_aco - 0.1, sem=32)
    R.texto(t_cai + 0.1, t_aco - 0.3, "…y su caída en apenas dos años", (960, 300), px=50, d=0.5)
    R.terreno(t_dos2 - 0.2, None, COL["imperio_1519"], 1.0, capa=1)

    # frase 5: «Él es Xolo» (GRANDE)
    ga(R, lambda t: A.signo_pregunta(), (-99.05, 19.45), t_alg - 0.1, t_xolo - 0.3, s=0.9, off=(0, -80), sem=33, zs=0.0, z=3,
       extra=[(0.05, "pluck", 0.35)])
    pa(R, MC(4), 330, 1015, 0.6, t_aco, t_xolo - 0.2, sem=34)        # Xolo con los patos: «estuvo ahí todo el tiempo»
    pa(R, XO(0), 960, 1055, 1.75, t_xolo - 0.15, t_siem - 0.2, entra="sube", dy=420, sem=35,
       extra=[(0.1, "ladrido", 0.55), (0.0, "crece", 0.3)])
    titulo(R, t_xolo, FIN(e) - 0.2, "XOLO", px=120, snd=False)
    R.snd(t_xolo + 0.05, "fanfarria", 0.3)

    # frase 6: un xoloitzcuintle sin pelo, muy leal… a un paso de terminar en el menú
    R.texto(t_xit, FIN(e) - 0.2, "xoloitzcuintle", (960, 318), px=52, d=0.6)
    pa(R, FP.F("xolo_vivo"), 400, 1000, FP.s_para(0.50), t_xit - 0.2, t_siem - 0.1, entra="pluma", sem=260, z=4,
       extra=[(0.05, "papel", 0.3)])
    R.texto(t_pelo - 0.1, t_siem, "SIN PELO", (400, 420), px=50, d=0.4)
    R.snd(t_pelo, "pop", 0.3)
    R.texto(t_leal - 0.1, t_siem, "MUY LEAL", (1490, 620), px=50, d=0.4)
    pa(R, MC(0), 1500, 1010, 0.62, t_leal, t_siem + 0.2, sem=36, extra=[(0.05, "brillo", 0.25)])
    pa(R, XO(2), 700, 1045, 1.45, t_siem + 0.15, FIN(e) + 0.3, sem=37, extra=[(0.3, "gemido_perro", 0.45)])
    pa(R, CH(6), 1300, 1050, 0.7, t_siem + 0.4, FIN(e) + 0.3, sem=38, extra=[(0.05, "fuego", 0.3, {"dur": 1.8})])
    pa(R, MC(6), 1300, 905, 0.95, t_paso - 0.1, FIN(e) + 0.3, sem=39, z=3, entra="cae", extra=[(0.3, "golpe_suave", 0.35)])
    R.texto(t_menu - 0.1, FIN(e) - 0.2, "EL MENÚ", (1300, 480), px=56, d=0.4)


# ------------------------------------------------------------------ AZTLÁN (60-147,9 s)
def _aztlan(R):
    e = "aztlan"
    i0 = INI(e)
    t_azt, t_nun, t_azt1, t_ori, t_moda, t_ell, t_mex = (T(e, "aztecas", frase=0), T(e, "nunca", frase=0), T(e, "aztlan", frase=1),
                                                         T(e, "origen"), T(e, "moda"), T(e, "ellos"), T(e, "mexicas", frase=1))
    t_sal, t_agua, t_nor, t_s12 = T(e, "salen"), T(e, "agua", frase=2), T(e, "norte"), T(e, "siglo doce")
    t_don, t_nad, t_nay, t_baj, t_eu, t_nex = (T(e, "donde"), T(e, "nadie"), T(e, "nayarit"), T(e, "bajio"), T(e, "estados"),
                                               T(e, "nunca existio"))
    t_gui, t_hui, t_col, t_sol, t_bul, t_sac = (T(e, "guiaba"), T(e, "huitzilopochtli", frase=4), T(e, "colibri"), T(e, "sol"),
                                                T(e, "bulto"), T(e, "sacerdotes"))
    t_pro, t_rec, t_agu, t_nop = T(e, "prometio"), T(e, "reconocerian"), T(e, "aguila"), T(e, "nopal")
    t_cam, t_dos = T(e, "caminata"), T(e, "dos siglos")
    t_coa, t_nac, t_arm, t_mad, t_cli = (T(e, "coatepec"), T(e, "nacio"), T(e, "armado"), T(e, "madre"), T(e, "coatlicue"))
    t_coy, t_mat, t_400, t_ven, t_desp, t_arr = (T(e, "coyolxauhqui", frase=8), T(e, "matarla"), T(e, "cuatrocientos"), T(e, "vencio"),
                                                 T(e, "despedazo"), T(e, "arrojo"))
    t_gua, t_coy2, t_vol, t_1978, t_cal = (T(e, "guarda"), T(e, "coyolxauhqui", frase=9), T(e, "volver"), T(e, "1978"), T(e, "calle"))
    t_tula, t_tol, t_cuna = T(e, "tula"), T(e, "toltecas"), T(e, "cuna")
    seg1 = tramo(RUTA, CI["aztlan_flecha"], CI["tula"])
    seg1 = [seg1[0], (-100.35, 21.35), (-99.95, 20.95), (-99.62, 20.42), seg1[-1]]   # trazo a mano (Aztlán es mítico: solo el arranque)
    TULA = CI["tula"]
    COA = (TULA[0] - 0.03, TULA[1] + 0.05)      # Coatepec, «cerca de Tula» (mítico: punto aproximado, sin rótulo de coordenadas)

    # cámara: del valle al norte (borde de la rejilla) → ruta → Coatepec/Tula → Tula con la CDMX → Tula
    R.camara(i0 - 0.2, -99.3, 19.9, 2.4)
    R.camara(t_nun, -99.9, 20.7, 1.6)
    paseo(R, t_ori, t_don - 0.4, -100.2, 20.95, 1.55, px=34)
    R.camara(t_nay - 0.3, -100.6, 20.75, 1.2)
    paseo(R, t_eu + 0.5, t_cam - 0.4, -100.3, 20.9, 1.45, px=34)
    R.camara(t_cam + 0.3, -99.9, 20.3, 1.1)
    R.camara(t_dos + 0.4, -99.85, 20.28, 1.13)
    R.camara(t_coa + 0.4, -99.45, 20.25, 2.6)
    paseo(R, t_coa + 1.5, t_gua - 0.3, -99.36, 20.12, 3.6, px=30)
    R.camara(t_vol, -99.25, 19.78, 2.0)
    R.camara(t_cal + 0.2, -99.22, 19.72, 2.1)
    R.camara(t_tula - 0.1, -99.33, 20.16, 3.0)
    R.camara(t_tol + 0.4, -99.34, 20.2, 3.2)
    R.camara(FIN(e) - 0.25, -99.32, 20.14, 2.9)

    # frase 0: nunca se llamaron aztecas
    pa(R, MI(0), 330, 1010, 1.0, i0, t_ori - 0.1, sem=40, extra=[(0.05, "pasos", 0.25, {"dur": 0.7})])
    pa(R, MI(1), 1600, 1010, 0.95, i0 + 0.4, t_ori - 0.1, sem=41, flip=True)
    titulo(R, t_azt - 0.1, t_azt1 - 0.2, "«AZTECAS»", px=110, snd=True)
    R.texto(t_nun, t_azt1 - 0.2, "así nunca se llamaron", (960, 320), px=56, d=0.5)
    pa(R, XO(7), 1360, 1020, 0.6, t_nun - 0.2, t_azt1 - 0.1, sem=42, extra=[(0.1, "pluck", 0.3)])

    # frase 1: el nombre viene de Aztlán; ellos se llamaban mexicas
    pa(R, MI(6), 560, 900, 1.0, t_azt1 - 0.2, t_s12 + 0.4, sem=43, entra="sube", dy=260, extra=[(0.05, "agua_lago", 0.3, {"dur": 2.0})])
    R.texto(t_azt1, t_s12 + 0.3, "AZTLÁN", (560, 440), px=62, d=0.5)
    pa(R, FP.F("boturini_aztlan"), 1440, 975, FP.s_para(0.50), t_azt1 + 0.2, t_moda + 1.4, entra="pluma", sem=44, z=4,
       extra=[(0.05, "papel", 0.3)])
    R.texto(t_ori, t_moda + 1.2, "AZTECA: «GENTE DE AZTLÁN»", (960, 196), px=62, d=0.6)
    titulo(R, t_mex - 0.6, t_sal - 0.3, "MEXICAS", px=118, snd=True)
    R.sello(t_mex, "piramide_mx", "MEXICAS", color=(196, 74, 52))

    # frase 2: salen de Aztlán (siglo XII), un lugar rodeado de agua en algún punto del norte
    pa(R, FP.F("boturini_salida"), 1360, 960, FP.s_para(0.40), t_sal - 0.2, t_s12 + 1.0, entra="pluma", sem=46, z=4)
    ciclo_pant(R, C_CANOA, 600, 1000, 1030, t_sal, 6.0, t1=t_s12 + 0.6, s=0.62, sem=47)
    R.snd(t_sal + 0.1, "remo", 0.35)
    R.texto(t_agua - 0.1, t_s12 - 0.3, "rodeado de agua", (560, 360), px=44, d=0.4)
    R.texto(t_nor - 0.1, t_don - 0.2, "¿EN ALGÚN PUNTO DEL NORTE?", (960, 196), px=60, d=0.5)
    R.anio(t_s12, 1116)
    R.texto(t_s12 + 0.1, t_don - 0.2, "SIGLO XII", (960, 300), px=52, d=0.4)

    # frase 3: ¿dónde estaba Aztlán? Nayarit, el Bajío, Estados Unidos… o nunca existió
    titulo(R, t_don - 0.1, t_gui - 0.2, "¿DÓNDE ESTABA AZTLÁN?", px=80, snd=True)
    pa(R, lambda t: A.signo_pregunta(), 960, 620, 1.3, t_nad - 0.2, t_nay, sem=48, extra=[(0.05, "pluck", 0.35)])
    for k, (tt, txt, x, y) in enumerate(((t_nay, "¿NAYARIT?", 330, 760), (t_baj, "¿EL BAJÍO?", 960, 860), (t_eu, "¿ESTADOS UNIDOS?", 1560, 620))):
        pa(R, MI(6), x, y + 150, 0.62, tt - 0.15, t_nex + 0.3 + 0.1 * k, sem=49 + k, entra="pop", extra=[(0.05, "pop", 0.3)])
        R.texto(tt, t_nex + 0.2, txt, (x, y - 140), px=46, d=0.4)
    R.texto(t_nex, t_gui - 0.2, "…¿O NUNCA EXISTIÓ?", (960, 320), px=56, d=0.5)
    R.snd(t_nex + 0.3, "whoosh", 0.35)
    pa(R, XO(7), 1780, 1030, 0.55, t_nad, t_gui, sem=52, flip=True)

    # frase 4: Huitzilopochtli, el colibrí del sur, dios del sol y de la guerra, en un bulto
    pa(R, FP.F("huitzilopochtli_telleriano"), 480, 975, FP.s_para(0.52), t_hui - 0.2, t_bul - 0.7, entra="pluma", sem=53, z=4,
       extra=[(0.05, "papel", 0.3)])
    pa(R, MI(3), 1600, 1010, 1.1, t_hui - 0.1, t_cam - 0.1, sem=54, entra="sube", dy=300, extra=[(0.05, "tambor", 0.35, {"dur": 1.0})])
    R.texto(t_hui + 0.1, t_cam - 0.2, "HUITZILOPOCHTLI", (1600, 540), px=42, d=0.5)
    R.texto(t_col - 0.1, t_bul - 0.3, "«COLIBRÍ DEL SUR»", (960, 196), px=70, d=0.5)
    R.texto(t_sol - 0.1, t_bul - 0.3, "dios del sol y de la guerra", (960, 310), px=50, d=0.5)
    pa(R, lambda t: A.sol_brillo(60), 1150, 500, 1.0, t_sol - 0.15, t_bul, sem=55, extra=[(0.05, "brillo", 0.3)])
    pa(R, MI(2), 400, 1010, 1.05, t_bul - 0.15, t_cam - 0.1, sem=56, extra=[(0.05, "flauta", 0.3)])
    R.texto(t_sac, t_pro - 0.2, "el bulto sagrado", (400, 560), px=40, d=0.4)

    # frase 5: la promesa: un águila parada sobre un nopal
    R.texto(t_pro - 0.1, t_cam - 0.3, "LA TIERRA PROMETIDA:", (960, 196), px=66, d=0.5)
    pa(R, FU(0), 960, 980, 0.95, t_agu - 0.2, t_cam + 0.3, sem=57, entra="sube", dy=260, extra=[(0.1, "aguila", 0.4)])
    R.texto(t_agu, t_cam - 0.2, "un águila sobre un nopal", (960, 306), px=52, d=0.5)
    pa(R, XO(0), 1240, 1020, 0.55, t_rec, t_cam + 0.2, sem=58, flip=True)

    # frase 6: la caminata de casi dos siglos (ruta `migracion`: flecha desde el borde norte)
    R.ruta(seg1, t_cam - 0.6, 4.4, ancho=5.0, flecha=True)
    lin = lambda u: u
    for k in range(3):
        andar_ciclo(R, C_MEX, seg1, t_cam - 0.5 + 0.25 * k, 4.6, t1=t_cli, s=0.46, sem=60 + k, fps=9, off=formacion(k, 3, 58), ease=lin,
                    extra=[(0.05, "pasos", 0.3, {"dur": 1.6})] if k == 0 else ())
    R.act(MI(2), pos_geo=R.camino_pos(seg1, t_cam - 0.8, 4.6, ease=lin), off=(95, -10), s=0.42, t_in=t_cam - 0.8, d_in=0.35, entra="pop",
          sem=59, zs=0.4, z=1, t_out=t_cli)
    andar_ciclo(R, C_XOLO, seg1, t_cam - 0.2, 4.5, t1=t_cli, s=0.26, sem=63, fps=11, off=(-80, 14), ease=lin)
    titulo(R, t_cam + 0.1, t_coa - 0.3, "CASI DOS SIGLOS", x=470, y=300, px=66, snd=True)
    R.texto(t_cam + 0.5, t_coa - 0.3, "caminando", (470, 390), px=58, d=0.5)
    pa(R, FP.F("boturini_l15"), 470, 960, FP.s_para(0.40), t_cam, t_coa + 0.2, entra="pluma", sem=64, z=4)

    # frase 7: Coatepec: nace Huitzilopochtli armado para defender a Coatlicue
    lugar(R, t_coa - 0.1, t_gua - 0.3, "CERRO DE COATEPEC", COA, off=(0, -230), px=44)
    R.snd(t_coa, "trueno", 0.25, dur=1.6)
    pa(R, MI(4), 380, 1010, 1.05, t_coa + 0.2, t_arr + 0.6, sem=65, extra=[(0.05, "flauta", 0.25)])
    R.texto(t_cli, t_mat, "COATLICUE", (380, 560), px=42, d=0.4)
    pa(R, FP.F("huitzilopochtli_nacimiento"), 1440, 975, FP.s_para(0.50), t_nac - 0.3, t_coy - 0.35, entra="pluma", sem=66, z=4,
       extra=[(0.05, "papel", 0.3)])
    R.texto(t_arm - 0.1, t_coy - 0.2, "¡NACIÓ ARMADO!", (960, 196), px=74, d=0.5)
    pa(R, MI(3), 730, 1020, 1.15, t_nac, t_arr + 0.6, sem=67, entra="sube", dy=320, extra=[(0.05, "crece", 0.4)])

    # frase 8: Coyolxauhqui y los 400 hermanos; él la vence y la arroja cerro abajo
    pa(R, MI(5), 1250, 1010, 1.0, t_coy - 0.15, t_arr - 0.05, sem=68, flip=True, sale="cortar", d_out=0.01)
    R.texto(t_coy + 0.2, t_arr - 0.2, "COYOLXAUHQUI", (1250, 540), px=42, d=0.4)
    R.contador(t_400 - 0.1, t_400 + 1.0, 0, 400, (960, 196), px=70, formato="{:,} HERMANOS", hasta_t=t_ven - 0.2)
    for k in range(3):
        ciclo_pant(R, C_GUE, 2060 + 150 * k, 1560 + 130 * k, 1015, t_400 - 0.2 + 0.2 * k, 1.6, t1=t_ven + 0.3, s=0.6, sem=69 + k)
    R.snd(t_400, "batalla", 0.35, dur=1.6)
    pa(R, lambda t: A.estallido(12, 40, 120), 1150, 780, 1.0, t_ven - 0.05, t_ven + 0.7, sem=72, extra=[(0.03, "impacto", 0.45)])
    R.texto(t_ven, t_gua - 0.5, "…¡Y LA ARROJÓ CERRO ABAJO!", (960, 196), px=64, d=0.6)
    R.act(MI(5), pos=cae(1250, 640, 1640, 1030, t_arr - 0.05, 1.3, 0.85, giro=2.0), t_in=t_arr - 0.05, d_in=0.01, entra="fija", sem=73, z=3,
          t_out=t_gua - 0.1, sale="encoger")
    R.snd(t_arr + 0.2, "whoosh", 0.35)
    R.snd(t_arr + 1.2, "piedra", 0.45)
    pa(R, XO(2), 1060, 1035, 0.62, t_arr + 0.4, t_gua + 0.3, sem=74, extra=[(0.2, "gemido_perro", 0.35)])

    # frase 9: guarda ese nombre: la volveremos a encontrar en 1978 bajo una calle de la Ciudad de México
    pa(R, FP.F("coyolxauhqui_piedra"), 1360, 960, FP.s_para(0.44), t_coy2 - 0.1, t_tula - 0.2, entra="pluma", sem=75, z=4,
       extra=[(0.05, "papel", 0.3)])
    R.texto(t_gua, t_vol - 0.2, "GUARDA ESE NOMBRE", (960, 196), px=68, d=0.5)
    titulo(R, t_1978 - 0.1, t_tula - 0.3, "1978", px=120, snd=False)
    R.snd(t_1978, "cincel", 0.35, dur=1.2)
    pa(R, RU(1), 380, 1010, 1.0, t_vol - 0.1, t_tula - 0.1, sem=76, extra=[(0.05, "golpe_suave", 0.3)])
    pa(R, RU(2), 640, 1000, 0.55, t_1978 + 0.2, t_tula - 0.1, sem=77, extra=[(0.05, "piedra", 0.35)])
    R.texto(t_cal - 0.3, t_tula - 0.2, "bajo una calle de la Ciudad de México", (960, 310), px=50, d=0.6)

    # frase 10: Tula, la gran ciudad de los toltecas
    ga(R, MI(7), TULA, t_tula - 0.15, FIN(e) + 0.3, s=0.62, off=(0, -12), sem=78, zs=0.3, z=2, entra="sube", dy=200,
       extra=[(0.05, "piedra", 0.35)])
    ciudad(R, t_tula - 0.1, FIN(e) + 0.2, "tula", "TULA", "abajo", 46)
    titulo(R, t_tol - 0.1, FIN(e) + 0.2, "LOS TOLTECAS", px=84, snd=True)
    R.texto(t_cuna - 0.1, FIN(e) + 0.2, "la cuna de todo lo civilizado", (960, 306), px=52, d=0.5)
    pa(R, MI(0), 330, 1010, 1.0, t_tula - 0.1, FIN(e) + 0.3, sem=79)
    pa(R, XO(5), 1620, 1020, 0.7, t_cuna - 0.2, FIN(e) + 0.3, sem=80, extra=[(0.1, "ladrido", 0.35)])


# ------------------------------------------------------------------ CHAPULTEPEC (147,9-248,6 s)
def _chapultepec(R):
    e = "chapultepec"
    i0 = INI(e)
    t_fin, t_val, t_vac = T(e, "finales"), T(e, "valle"), T(e, "vacio")
    t_lag, t_ciu, t_azc, t_cul, t_tex, t_xoc = (T(e, "lagos"), T(e, "ciudades"), T(e, "azcapotzalco"), T(e, "culhuacan", frase=1),
                                                T(e, "texcoco"), T(e, "xochimilco"))
    t_ins, t_cha, t_chp, t_bro = T(e, "instalaron"), T(e, "chapultepec", frase=2), T(e, "chapulin"), T(e, "brotaba")
    t_pob, t_pel, t_cos, t_vec, t_jun, t_ech = (T(e, "pobres"), T(e, "peleoneros"), T(e, "costumbres"), T(e, "los vecinos se", frase=3),
                                                T(e, "juntaron"), T(e, "echaron"))
    t_jef, t_hui, t_pri, t_sac, t_cul4 = (T(e, "jefe"), T(e, "huitzilihuitl"), T(e, "prisionero"), T(e, "sacrificado"),
                                          T(e, "culhuacan", frase=4))
    t_sob, t_asi, t_sen, t_dio, t_tiz = T(e, "sobrevivientes"), T(e, "asilo"), T(e, "senor", frase=5), T(e, "dio"), T(e, "tizapan")
    t_ped, t_vib, t_cas, t_ide, t_mur = T(e, "pedregal"), T(e, "viboras", frase=6), T(e, "cascabel"), T(e, "idea"), T(e, "murieran")
    t_cue, t_man, t_enc, t_con, t_com = T(e, "cuenta"), T(e, "mando"), T(e, "encontro", frase=7), T(e, "contentos"), T(e, "comido")
    t_xolo, t_salv, t_vib8, t_menu = T(e, "xolo"), T(e, "salvo"), T(e, "viboras", frase=8), T(e, "menu")
    t_merc, t_cul9, t_pid, t_hij, t_cas9, t_dios = (T(e, "mercenarios"), T(e, "culhuacan", frase=9), T(e, "pidieron", frase=9),
                                                    T(e, "hija", frase=9), T(e, "casarla"), T(e, "dios", frase=9))
    t_ley, t_ace, t_org, t_fie, t_sacd, t_piel = (T(e, "leyenda"), T(e, "acepto"), T(e, "orgulloso"), T(e, "fiesta"),
                                                  T(e, "sacerdote"), T(e, "piel"))
    t_hon, t_pri11, t_dio11, t_toci, t_abu, t_pad = (T(e, "honor"), T(e, "princesa"), T(e, "diosa"), T(e, "toci"), T(e, "abuela"),
                                                     T(e, "padre"))
    t_per, t_lag12, t_huy, t_jun12, t_isl = T(e, "persiguieron"), T(e, "lago", frase=12), T(e, "huyeron"), T(e, "juncos"), T(e, "islotes")
    seg2 = tramo(RUTA, CI["tula"], CI["chapultepec"])
    seg3 = tramo(RUTA, CI["chapultepec"], CI["culhuacan"])
    seg4 = [CI["culhuacan"], (-99.15, 19.33), CI["tizapan"]]
    seg5 = [CI["tizapan"], (-99.17, 19.37), (-99.15, 19.405), (-99.134, 19.432)]
    CHA, CUL, TIZ = CI["chapultepec"], CI["culhuacan"], CI["tizapan"]

    # cámara: Tula → el valle con los lagos → Chapultepec → Culhuacán → Tizapán → el lago y los islotes
    R.camara(i0 - 0.2, -99.28, 19.85, 2.5)
    R.camara(t_val - 0.3, -99.12, 19.55, 4.4)
    paseo(R, t_vac, t_ins - 0.4, -99.04, 19.46, 6.2, px=34)
    R.camara(t_cha - 0.2, -99.172, 19.438, 12.0)
    paseo(R, t_cha + 1.8, t_jun - 0.2, -99.176, 19.44, 15.0, px=40)
    R.camara(t_ech + 0.4, -99.15, 19.39, 10.0)
    R.camara(t_cul4 - 0.4, -99.115, 19.345, 12.0)
    R.camara(t_sob + 0.3, -99.12, 19.345, 12.5)
    R.camara(t_dio - 0.2, -99.155, 19.34, 11.0)
    paseo(R, t_tiz, t_merc - 0.4, -99.198, 19.338, 15.0, px=42)
    R.camara(t_merc + 0.4, -99.16, 19.34, 11.0)
    paseo(R, t_cul9 + 0.8, t_per - 0.3, -99.115, 19.343, 12.5, px=40)
    R.camara(t_lag12, -99.16, 19.37, 10.0)
    R.camara(t_huy + 0.4, -99.145, 19.40, 12.0)
    R.camara(t_isl, -99.135, 19.428, 18.0)
    R.camara(FIN(e) + 0.3, -99.134, 19.432, 22.0)

    # frase 0: a finales del s. XIII llegan al Valle de México… y no estaba vacío
    R.anio(t_fin + 0.4, 1299)
    pa(R, MI(1), 330, 1010, 0.95, i0, t_lag - 0.1, sem=100, extra=[(0.05, "pasos", 0.3, {"dur": 0.8})])
    R.ruta(seg2, i0 - 0.1, 17.0, ancho=5.0, flecha=True)
    grupo_ciclo(R, C_MEX, seg2, i0, 17.0, n=3, ancho=50, t1=t_cha + 0.6, s=0.36, sem=101, fps=9, desfase=0.25)
    andar_ciclo(R, C_XOLO, seg2, i0 + 0.5, 17.0, t1=t_cha + 0.6, s=0.22, sem=104, fps=11, off=(56, 12))
    titulo(R, t_val - 0.1, t_lag - 0.3, "EL VALLE DE MÉXICO", px=82, snd=True)
    R.texto(t_vac - 0.2, t_lag - 0.3, "…y no estaba vacío", (960, 312), px=54, d=0.5)
    pa(R, FP.F("tenayuca"), 1440, 965, FP.s_para(0.42), t_vac - 0.3, t_ciu - 0.3, entra="pluma", sem=105, z=4,
       extra=[(0.05, "papel", 0.3)])
    lugar(R, t_vac, t_ciu - 0.3, "TENAYUCA", CI["tenayuca"], off=(0, 55), px=36)

    # frase 1: alrededor de los lagos, ciudades ricas y antiguas
    R.snd(t_lag, "agua_lago", 0.3, dur=3.0)
    pa(R, FP.F("santa_cecilia"), 1530, 975, FP.s_para(0.44), t_ciu, t_ins - 0.4, entra="pluma", sem=106, z=4)
    for k, (tt, cl, txt, lado) in enumerate(((t_azc, "azcapotzalco", "AZCAPOTZALCO", "izq"), (t_cul, "culhuacan", "CULHUACÁN", "der"),
                                             (t_tex, "texcoco", "TEXCOCO", "izq"), (t_xoc, "xochimilco", "XOCHIMILCO", "der"))):
        ciudad(R, tt - 0.15, t_ins - 0.3, cl, txt, lado, 38)
        ga(R, AH(1), CI[cl], tt - 0.1, t_ins - 0.2, s=0.26, off=(0, -12), sem=107 + k, zs=0.3, z=2,
           extra=[(0.05, ("tambor", "flauta", "pluck", "caracol")[k], 0.25)])

    # frase 2: el cerro de Chapultepec, «del chapulín», donde brotaba agua dulce
    ga(R, CH(0), CHA, t_cha - 0.2, t_jun - 0.1, s=0.34, off=(0, -14), sem=111, zs=0.3, z=2, entra="sube", dy=200,
       extra=[(0.05, "crece", 0.35)])
    ciudad(R, t_cha - 0.1, t_jun - 0.2, "chapultepec", "CHAPULTEPEC", "abajo", 44)
    R.texto(t_chp - 0.1, t_pob - 0.2, "«CERRO DEL CHAPULÍN»", (960, 196), px=72, d=0.6)
    pa(R, FP.F("chapultepec_banos"), 1540, 975, FP.s_para(0.44), t_bro - 0.3, t_pel + 0.8, entra="pluma", sem=112, z=4,
       extra=[(0.05, "agua_lago", 0.3, {"dur": 1.5})])
    R.texto(t_bro + 0.1, t_pob - 0.2, "agua dulce", (960, 300), px=54, d=0.4)
    pa(R, MI(0), 330, 1010, 1.0, t_ins - 0.1, t_jun, sem=113)

    # frase 3: pobres, peleoneros y raros: los vecinos se juntan y los echan
    R.texto(t_pob - 0.1, t_jun - 0.3, "POBRES", (330, 560), px=44, d=0.3)
    pa(R, CN(7), 620, 1010, 0.95, t_pel - 0.15, t_jun, sem=114, extra=[(0.05, "golpe_suave", 0.3)])
    R.texto(t_pel, t_jun - 0.3, "PELEONEROS", (620, 560), px=44, d=0.3)
    R.texto(t_cos, t_jun - 0.3, "…y con costumbres raras", (960, 196), px=60, d=0.5)
    pa(R, CH(1), 1600, 1010, 1.0, t_vec - 0.1, t_ech + 1.2, sem=115, flip=True, extra=[(0.05, "impacto", 0.3)])
    for k in range(3):
        ciclo_pant(R, C_GUE, 2050 + 130 * k, -200, 1015, t_jun - 0.1 + 0.18 * k, 3.6, s=0.66, sem=116 + k)
    R.snd(t_jun, "batalla", 0.35, dur=2.0)
    ciclo_pant(R, C_XOLO, 760, -150, 1030, t_jun + 0.3, 1.6, s=0.45, sem=119)
    R.snd(t_jun + 0.4, "gemido_perro", 0.35)
    titulo(R, t_ech - 0.1, t_hui - 0.3, "¡FUERA!", px=110)
    pa(R, FP.F("boturini_l20"), 1260, 955, FP.s_para(0.40), t_ech - 0.2, t_cul4 + 0.4, entra="pluma", sem=120, z=4,
       extra=[(0.05, "papel", 0.3)])

    # frase 4: Huitzilíhuitl el viejo, prisionero y sacrificado en Culhuacán
    pa(R, CH(2), 330, 1010, 1.0, t_jef - 0.15, t_sob, sem=121, extra=[(0.05, "tambor", 0.3, {"dur": 0.9})])
    R.texto(t_hui, t_sob - 0.2, "HUITZILÍHUITL", (330, 550), px=42, d=0.4)
    R.texto(t_pri, t_sob - 0.2, "PRISIONERO", (960, 196), px=74, d=0.4)
    ga(R, CH(3), CUL, t_cul4 - 0.3, t_asi + 2.0, s=0.4, off=(-170, 30), sem=122, zs=0.3, z=2)
    ciudad(R, t_cul4 - 0.1, t_sen - 0.3, "culhuacan", "CULHUACÁN", "der", 44)
    pa(R, XO(3), 1180, 1035, 0.5, t_sac, t_sen - 0.3, sem=123)

    # frase 5: el señor de Culhuacán les da Tizapán
    pa(R, CH(3), 1600, 1010, 1.0, t_sen - 0.2, t_ide, sem=124, flip=True, extra=[(0.05, "caracol", 0.25)])
    R.texto(t_sen + 0.2, t_vib - 0.2, "EL SEÑOR DE CULHUACÁN", (1560, 560), px=38, d=0.4)
    pa(R, MI(1), 330, 1010, 0.95, t_sob, t_ped, sem=125)
    R.texto(t_asi - 0.1, t_tiz - 0.2, "«¿nos da asilo?»", (400, 560), px=44, d=0.4)
    grupo_ciclo(R, C_MEX, seg4, t_dio - 0.2, 2.6, n=2, ancho=46, t1=t_vib - 0.2, s=0.34, sem=126, fps=9)
    ciudad(R, t_tiz - 0.15, t_vib - 0.2, "tizapan", "TIZAPÁN", "der", 46)
    titulo(R, t_tiz, t_ped + 1.0, "TIZAPÁN", px=96, snd=True)

    # frase 6: un pedregal lleno de víboras de cascabel; la idea era que se murieran
    for k, off in enumerate(((0, 40), (-270, 120), (270, 130))):
        ga(R, CH(4), TIZ, t_vib - 0.1 + 0.2 * k, t_com + 0.3 + 0.35 * k, s=0.36 if k == 0 else 0.26, off=off, sem=128 + k, zs=0.3, z=2,
           sale="encoger", extra=[(0.05, "cascabel", 0.35)] if k != 1 else ())
    R.texto(t_cas, t_ide - 0.2, "VÍBORAS DE CASCABEL", (960, 196), px=72, d=0.5)
    R.texto(t_ide, t_cue - 0.2, "la idea: que se murieran", (960, 196), px=60, d=0.5)
    pa(R, XO(2), 330, 1030, 0.85, t_ide - 0.2, t_cue, sem=131, extra=[(0.2, "gemido_perro", 0.3)])

    # frase 7: el señor manda a ver… y están felices: se comieron las víboras
    pa(R, CH(3), 1600, 1010, 1.0, t_man - 0.2, t_xolo - 0.1, sem=132, flip=True)
    R.texto(t_man, t_con - 0.2, "«a ver cómo van…»", (1560, 560), px=42, d=0.4)
    pa(R, CH(6), 520, 1030, 0.62, t_con - 0.4, t_merc, sem=133, extra=[(0.05, "fuego", 0.3, {"dur": 2.0})])
    pa(R, CH(5), 330, 1010, 1.0, t_con - 0.2, t_merc, sem=134, extra=[(0.1, "pop", 0.3)])
    R.texto(t_con + 0.2, t_com - 0.2, "MUY CONTENTOS", (330, 560), px=44, d=0.4)
    titulo(R, t_com - 0.6, t_xolo - 0.2, "¡SE COMIERON LAS VÍBORAS!", px=80, snd=True)
    pa(R, lambda t: A.estallido(10, 30, 90), 1600, 520, 0.9, t_com, t_com + 0.8, sem=135, extra=[(0.03, "impacto", 0.35)])

    # frase 8: Xolo se salvó: había víboras de sobra en el menú
    pa(R, XO(5), 960, 1040, 1.35, t_xolo - 0.1, t_merc - 0.1, sem=136, entra="sube", dy=320, extra=[(0.1, "ladrido", 0.5)])
    R.texto(t_salv - 0.1, t_merc - 0.6, "¡SE SALVÓ!", (960, 196), px=84, d=0.5)
    pa(R, MC(6), 1560, 1000, 0.85, t_vib8 - 0.2, t_merc - 0.1, sem=137, extra=[(0.05, "golpe_suave", 0.3)])
    pa(R, CH(4), 1560, 820, 0.42, t_vib8, t_merc - 0.1, sem=138, z=3)
    R.texto(t_menu - 0.1, t_merc - 0.2, "MENÚ DEL DÍA: VÍBORA", (1500, 470), px=44, d=0.5)
    R.snd(t_menu, "ladrido", 0.3)

    # frase 9: mercenarios de Culhuacán; piden una hija del señor para casarla con su dios
    pa(R, CN(7), 330, 1010, 1.0, t_merc - 0.15, t_ley, sem=139, extra=[(0.05, "batalla", 0.3, {"dur": 1.3})])
    R.texto(t_merc, t_ley - 0.2, "MERCENARIOS", (960, 196), px=78, d=0.5)
    ciudad(R, t_cul9 - 0.1, t_hon - 0.2, "culhuacan", "CULHUACÁN", "der", 44)
    pa(R, CH(3), 1600, 1010, 1.0, t_pid - 0.1, t_hon, sem=140, flip=True)
    pa(R, CH(7), 1330, 1010, 0.9, t_hij - 0.2, t_ley, sem=141, flip=True, extra=[(0.05, "pluck", 0.3)])
    pa(R, MI(3), 700, 1010, 0.9, t_dios - 0.25, t_ley, sem=142, extra=[(0.05, "brillo", 0.3)])
    R.texto(t_cas9, t_ley - 0.2, "«para casarla con nuestro dios»", (960, 310), px=48, d=0.5)
    pa(R, XO(7), 960, 1030, 0.55, t_hij, t_fie, sem=143)

    # frase 10: él acepta, orgulloso… y en la fiesta encuentra a un sacerdote vestido con la piel de su hija
    R.texto(t_ace, t_fie - 0.2, "«¡ACEPTO!»", (1600, 540), px=52, d=0.4)
    R.snd(t_org, "fanfarria", 0.3)
    pa(R, CA(1), 330, 1010, 0.95, t_fie - 0.3, t_hon, sem=144, extra=[(0.05, "tambor", 0.35, {"dur": 1.5})])
    pa(R, CA(1), 600, 1015, 0.85, t_fie - 0.1, t_hon, sem=145, flip=True)
    R.snd(t_fie + 0.1, "flauta", 0.3)
    titulo(R, t_fie - 0.1, t_sacd - 0.2, "LA FIESTA", px=84)
    pa(R, MI(2), 960, 1010, 1.0, t_sacd - 0.15, t_hon, sem=146, extra=[(0.1, "impacto", 0.4)])
    R.texto(t_sacd + 0.1, t_hon - 0.2, "un sacerdote… con la piel de su hija", (960, 196), px=58, d=0.6)
    pa(R, lambda t: A.estallido(10, 30, 90), 1600, 520, 0.9, t_piel, t_piel + 0.9, sem=147)

    # frase 11: para los mexicas un honor (la princesa se vuelve Toci); para su padre, no tanto
    pa(R, CH(7), 960, 1010, 1.05, t_pri11 - 0.2, t_per, sem=148, extra=[(0.05, "crece", 0.35)])
    pa(R, lambda t: A.sol_brillo(70), 960, 470, 1.0, t_dio11 - 0.1, t_per, sem=149, z=1, extra=[(0.05, "brillo", 0.35)])
    R.texto(t_hon - 0.1, t_toci - 0.3, "PARA LOS MEXICAS: UN HONOR", (960, 196), px=62, d=0.5)
    titulo(R, t_toci - 0.1, t_per - 0.2, "TOCI, «NUESTRA ABUELA»", px=78, snd=True)
    pa(R, MI(0), 330, 1010, 0.95, t_hon, t_per, sem=150)
    pa(R, CH(3), 1600, 1010, 1.0, t_pad - 0.2, t_per, sem=151, flip=True, extra=[(0.05, "impacto", 0.35)])
    R.texto(t_pad + 0.2, t_per - 0.2, "SU PADRE: NO TANTO", (1560, 560), px=42, d=0.4)
    pa(R, CH(1), 1255, 1010, 0.85, t_pad + 0.3, t_per, sem=152, flip=True)

    # frase 12: los persiguen hasta el lago; huyen entre los juncos a unos islotes que nadie quería
    for k in range(3):
        ciclo_pant(R, C_GUE, 2050 + 140 * k, 700 + 130 * k, 1015, t_per - 0.1 + 0.2 * k, 2.2, t1=t_jun12, s=0.66, sem=153 + k)
    R.snd(t_per, "batalla", 0.35, dur=1.6)
    andar_ciclo(R, C_CANOA, seg5, t_huy - 0.4, 5.5, t1=FIN(e) + 0.5, s=0.26, sem=156, fps=6, zs=0.45, z=2,
                extra=[(0.05, "remo", 0.35)])
    andar_ciclo(R, C_CANOA, seg5, t_huy - 0.1, 5.5, t1=FIN(e) + 0.5, s=0.24, sem=157, fps=6, zs=0.45, z=2, off=(-70, 24))
    R.ruta(seg5, t_huy - 0.4, 5.5, ancho=3.0, flecha=True)
    pa(R, CH(8), 330, 1015, 0.95, t_lag12, FIN(e) + 0.4, sem=158, extra=[(0.05, "agua_lago", 0.35, {"dur": 2.5})])
    ga(R, FU(8), (-99.14, 19.42), t_jun12 - 0.2, FIN(e) + 0.4, s=0.24, off=(0, 20), sem=159, zs=0.3)
    ga(R, FU(8), (-99.128, 19.428), t_jun12, FIN(e) + 0.4, s=0.22, off=(0, 20), sem=160, zs=0.3, flip=True)
    R.texto(t_isl - 0.1, FIN(e) + 0.3, "unos islotes que nadie quería", (960, 196), px=60, d=0.5)
    pa(R, XO(3), 1540, 1035, 0.62, t_huy, FIN(e) + 0.4, sem=161)       # Xolo escondido bajo un petate


# ------------------------------------------------------------------ FUNDACIÓN (248,6-295,7 s)
def _fundacion(R):
    e = "fundacion"
    i0 = INI(e)
    t_tra, t_1325, t_vie, t_sen, t_agu, t_nop, t_pie = (T(e, "tradicion"), T(e, "1325"), T(e, "vieron"), T(e, "senal"),
                                                        T(e, "aguila", frase=0), T(e, "nopal"), T(e, "piedra", frase=0))
    t_ojo, t_dib, t_ant, t_ser1, t_paj, t_sim = (T(e, "ojo"), T(e, "dibujos"), T(e, "antiguos"), T(e, "serpiente", frase=1),
                                                 T(e, "pajaro"), T(e, "simplemente"))
    t_ser2, t_lleg, t_hoy, t_band = T(e, "serpiente", frase=2), T(e, "llego"), T(e, "hoy"), T(e, "bandera")
    t_llam, t_mt, t_lug, t_tuna = T(e, "llamaron"), T(e, "mexicotenochtitlan"), T(e, "lugar"), T(e, "tuna")
    t_isl, t_pan, t_sp, t_sm, t_st, t_tod, t_tru, t_mal = (T(e, "islote", frase=4), T(e, "pantanoso"), T(e, "sin piedra"),
                                                           T(e, "sin madera"), T(e, "sin buena"), T(e, "todo"), T(e, "trueque"),
                                                           T(e, "mala"))
    t_uno, t_gru, t_pel, t_fun, t_isl5, t_tla = (T(e, "unos"), T(e, "grupo"), T(e, "peleo"), T(e, "fundo"), T(e, "islote", frase=5),
                                                 T(e, "tlatelolco"))
    TEN, TLA = CI["tenochtitlan"], CI["tlatelolco"]
    ISL = (-99.1335, 19.4335)

    # cámara: zoom fuerte a la isla → el islote de cerca → la isla de 1325 → al norte, Tlatelolco
    R.camara(i0 - 0.2, -99.134, 19.438, 23.0)
    R.camara(t_1325, -99.134, 19.441, 32.0)
    R.camara(t_agu - 0.2, -99.1335, 19.4445, 44.0)
    paseo(R, t_agu + 1.6, t_llam - 0.6, -99.1335, 19.4445, 46.0, px=30)
    R.camara(t_mt + 0.3, -99.134, 19.443, 38.0)
    paseo(R, t_lug + 1.0, t_uno - 0.3, -99.1345, 19.4435, 36.0, px=34)
    R.camara(t_fun, -99.136, 19.445, 44.0)
    R.camara(t_tla, -99.1365, 19.4472, 60.0)
    R.camara(FIN(e) - 0.25, -99.137, 19.4474, 62.0)

    # frase 0: 1325: la señal, un águila sobre un nopal que crecía en una piedra
    pa(R, MI(0), 330, 1010, 0.95, i0, t_ojo - 0.1, sem=200, extra=[(0.05, "remo", 0.3)])
    R.anio(t_1325 - 0.1, 1325)
    R.sello(t_vie, "aguila_nopal", "MÉXICO-TENOCHTITLAN", color=(176, 52, 48))
    R.terreno(t_vie - 0.2, "islote_1325", ISLA, 1.0, capa=11)
    titulo(R, t_sen - 0.1, t_ojo - 0.2, "LA SEÑAL", px=96, snd=True)
    ga(R, FU(0), ISL, t_agu - 0.25, t_llam - 0.1, s=0.42, off=(0, 40), sem=201, zs=0.25, z=2, entra="sube", dy=240,
       extra=[(0.1, "aguila", 0.5), (0.0, "crece", 0.3)])
    R.texto(t_nop, t_ojo - 0.2, "un águila, un nopal y una piedra", (960, 306), px=50, d=0.5)
    pa(R, XO(4), 1640, 1030, 0.75, t_pie - 0.3, t_dib, sem=202, extra=[(0.2, "aullido", 0.35)])

    # frase 1: en los dibujos más antiguos no hay serpiente: un pájaro, o el águila sola
    pa(R, FP.F("mendoza_fundacion"), 460, 990, FP.s_para(0.56), t_dib - 0.3, t_hoy - 0.2, entra="pluma", sem=203, z=4,
       extra=[(0.05, "papel", 0.35)])
    R.texto(t_dib, t_ser1 - 0.2, "LOS DIBUJOS MÁS ANTIGUOS", (960, 196), px=66, d=0.5)
    pa(R, FU(1), 1600, 1000, 0.95, t_ser1 - 0.2, t_paj - 0.1, sem=204, extra=[(0.05, "cascabel", 0.3)])
    R.texto(t_ser1 + 0.1, t_paj - 0.2, "¿SERPIENTE? NO", (1600, 550), px=48, d=0.4)
    pa(R, FU(0), 1600, 1000, 1.05, t_paj - 0.1, t_ser2 - 0.1, sem=205, extra=[(0.05, "aguila", 0.35)])
    R.texto(t_paj, t_ser2 - 0.2, "UN PÁJARO", (1600, 550), px=52, d=0.4)
    R.texto(t_paj - 0.1, t_ser2 - 0.2, "el águila se come un pájaro…", (960, 196), px=62, d=0.5)
    R.texto(t_sim, t_ser2 - 0.2, "…o solo está parada", (960, 300), px=54, d=0.5)
    R.texto(t_sim + 0.2, t_hoy - 0.3, "CÓDICE MENDOZA", (460, 345), px=38, d=0.4)

    # frase 2: la serpiente llegó después; hoy está en la bandera
    pa(R, FU(1), 1600, 1000, 1.05, t_ser2 - 0.1, t_mt - 0.1, sem=206, extra=[(0.05, "cascabel", 0.35)])
    R.texto(t_ser2 + 0.1, t_mt - 0.2, "LA SERPIENTE", (1600, 550), px=52, d=0.4)
    R.texto(t_lleg, t_llam - 0.2, "llegó después", (960, 196), px=66, d=0.5)
    pa(R, FP.F("escudo_mexico"), 960, 980, FP.s_para(0.46), t_hoy - 0.2, t_mt - 0.1, entra="pluma", sem=207, z=4,
       extra=[(0.05, "papel", 0.3)])
    pa(R, LE(11), 400, 1010, 0.95, t_band - 0.2, t_mt - 0.1, sem=208, extra=[(0.05, "fanfarria", 0.35)])
    R.texto(t_band, t_llam - 0.2, "HOY, EN LA BANDERA", (960, 300), px=52, d=0.4)

    # frase 3: México-Tenochtitlan, «el lugar de la tuna de piedra»; la isla de 1325
    titulo(R, t_mt - 0.2, t_isl - 0.3, "MÉXICO-TENOCHTITLAN", px=92, snd=True)
    R.terreno(t_mt, "isla_1325", ISLA, 1.6, capa=11)
    R.snd(t_mt + 0.2, "crece", 0.35)
    R.texto(t_lug - 0.1, t_isl - 0.3, "«el lugar de la tuna de piedra»", (960, 308), px=54, d=0.5)
    ga(R, FU(4), ISL, t_mt + 0.2, FIN(e) + 0.4, s=0.30, off=(0, 20), sem=209, zs=0.25, z=2, entra="sube", dy=160,
       extra=[(0.05, "piedra", 0.3)])
    ga(R, FU(3), (-99.1365, 19.4320), t_lug, t_fun, s=0.24, off=(0, 20), sem=210, zs=0.25, z=2)
    ga(R, FU(3), (-99.1300, 19.4360), t_lug + 0.3, t_fun, s=0.22, off=(0, 20), sem=211, zs=0.25, z=2, flip=True)
    ga(R, XO(0), (-99.1318, 19.4318), t_tuna, t_uno, s=0.20, off=(0, 18), sem=212, zs=0.25, z=3, extra=[(0.1, "ladrido", 0.3)])
    pa(R, MI(1), 330, 1010, 0.95, t_mt + 0.3, t_tod, sem=213)

    # frase 4: un islote pantanoso: sin piedra, sin madera, sin buena tierra… trueque o a la mala
    ga(R, FU(2), (-99.1395, 19.4290), t_pan - 0.2, t_gru, s=0.26, off=(0, 20), sem=214, zs=0.25, z=2)
    ga(R, FU(9), (-99.1270, 19.4290), t_pan, t_gru, s=0.24, off=(0, 20), sem=215, zs=0.25, z=2, extra=[(0.05, "agua_lago", 0.3, {"dur": 2.0})])
    R.texto(t_isl, t_tod - 0.2, "UN ISLOTE PANTANOSO", (960, 196), px=74, d=0.5)
    for k, (tt, txt) in enumerate(((t_sp, "SIN PIEDRA"), (t_sm, "SIN MADERA"), (t_st, "SIN BUENA TIERRA"))):
        R.texto(tt + 0.2, t_tod - 0.1, txt, (1560, 420 + 90 * k), px=46, d=0.35)
        R.snd(tt + 0.25, "pluck", 0.3)
    pa(R, XO(2), 1560, 1030, 0.6, t_sp, t_tod, sem=216)
    andar_ciclo(R, C_CANOA, [(-99.118, 19.440), (-99.128, 19.432)], t_pan, 8.0, t1=t_uno, s=0.22, sem=217, fps=6, zs=0.3, z=2)
    pa(R, VI(12), 1300, 1000, 0.62, t_tru - 0.2, t_uno - 0.1, sem=218, extra=[(0.05, "monedas", 0.35)])
    pa(R, VI(2), 1600, 1010, 0.95, t_tru - 0.1, t_uno - 0.1, sem=219, flip=True)
    titulo(R, t_tru - 0.1, t_uno - 0.2, "TRUEQUE…", px=84)
    pa(R, CN(7), 330, 1010, 1.0, t_mal - 0.25, t_gru, sem=220, extra=[(0.05, "impacto", 0.35)])
    R.texto(t_mal, t_uno - 0.2, "…O A LA MALA", (960, 306), px=60, d=0.4)

    # frase 5: unos años después, un grupo se pelea y funda en el islote de al lado: Tlatelolco (1337)
    R.anio(t_uno + 0.2, 1337)
    pa(R, FU(6), 330, 1010, 1.0, t_gru - 0.1, FIN(e) + 0.4, sem=221, extra=[(0.05, "golpe_suave", 0.3)])
    pa(R, FU(7), 1600, 1010, 1.0, t_pel - 0.2, t_isl5 - 0.1, sem=222, extra=[(0.1, "impacto", 0.35)])
    R.texto(t_pel, t_isl5 - 0.2, "¡ME VOY!", (1600, 540), px=46, d=0.3)
    pa(R, FP.F("tlatelolco_ruinas"), 1500, 985, FP.s_para(0.44), t_isl5, FIN(e) + 0.4, entra="pluma", sem=226, z=4,
       extra=[(0.05, "papel", 0.3)])
    andar_ciclo(R, C_CANOA, [(-99.135, 19.438), (-99.136, 19.444), (-99.1375, 19.4485)], t_fun - 0.4, 2.8, t1=FIN(e) + 0.4, s=0.24,
                sem=223, fps=6, zs=0.3, z=2, extra=[(0.05, "remo", 0.3)])
    R.terreno(t_isl5 - 0.2, "islote_tlatelolco", TLAT, 1.0, capa=12)
    ga(R, FU(4), TLA, t_isl5, FIN(e) + 0.4, s=0.24, off=(0, 20), sem=224, zs=0.25, z=2, entra="sube", dy=160,
       extra=[(0.05, "crece", 0.3)])
    titulo(R, t_tla - 0.1, FIN(e) + 0.3, "TLATELOLCO", px=96, snd=True)
    lugar(R, t_tla, FIN(e) + 0.3, "TLATELOLCO (1337)", TLA, off=(340, -90), px=40)
    pa(R, XO(7), 700, 1030, 0.6, t_fun, FIN(e) + 0.4, sem=225)

    # limpieza de mis capas bajo el barrido a «chinampas» (la isla vuelve a su contorno base)
    R.terreno(FIN(e) + 0.35, None, ISLA, 0.3, capa=11)
    R.terreno(FIN(e) + 0.35, None, TLAT, 0.3, capa=12)
    R.terreno(FIN(e) + 0.35, None, AGUA, 0.3, capa=50)
