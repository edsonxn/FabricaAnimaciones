# -*- coding: utf-8 -*-
"""Coreografía (1/2) de «La historia de Tequisquiapan» (VERTICAL 1080x1920): gancho (el «centro de México» que no lo es, la sal,
la capital por unos días, la estación «Bernal»), orígenes (manantiales, otomíes y chichimecas, el nombre y el tequesquite),
fundación (1551, la cruz bajo el mezquite = leyenda, La Pila 1567, 1656) y siglos (reloj 1897, tren 1902, presa 1910, capital 1920).
Composición vertical: fila de año/sellos en y ≈ 200 · títulos en y 300-460 · FOTO real en la mitad de arriba (pies en y ≈ 1180) ·
pegatinas de Flow abajo (pies en y ≈ 1480; fuera de la columna de botones de Shorts, x > 930) · el mapa respira en medio.
Semillas 1-299."""
import foto_peg as FP
import mapa as M
from core import FIN, INI, T
from coreo_util import CI, COL, ciudad, ga, pa
from motor import W
from pegflow import P, ciclo

OR = lambda n, **k: P("01_origenes_hoja", n, **k)    # 0 otomí·1 otomí mujer·2 arquero·3 bañistas·4 tequesquite·5 esquites·6 nopal·7 mezquite·8 manantial
FU = lambda n, **k: P("02_fundacion_hoja", n, **k)   # 0 cacique·1 fraile·2 mezquite·3 cruz·4 carta·5 pila·6 huerta·7 canal·8 hacienda
SI = lambda n, **k: P("03_siglos_hoja", n, **k)      # 0 parroquia·1 reloj·2 tren·3 estación·4 presa·5 poste·6 gobernador·7 rebelde
CE = lambda n, **k: P("04_centro_hoja", n, **k)      # 0 monumento·1 Carranza·2 pin·3 selfie·4 lupa·5 rosa·6 letrero·7 familia
BE = lambda n, **k: P("06_bernal_hoja", n, **k)      # 0 peña·1 magma·2 viñedo·3 excursionista·4 turista mapa·5 gota·6 pozo·7 llave
C_JIN = ciclo("08_jinete_galope")[:3]                # el 4.º cuadro salió pegado a otros: solo 0-2

TEQ = CI["tequisquiapan"]
PLAZA = CI["plaza_tequis"]
CX = W // 2
YP = 1480                                            # pies de las pegatinas de abajo
YF = 1190                                            # pies de las fotos reales
TIERRA_TXT = (146, 110, 72)
EDO_TXT = (120, 96, 70)
_S = [0]


def S():
    _S[0] += 1
    return _S[0]


def foto(R, clave, t0, t1, x=CX, y=YF, frac=0.8, alto=0.33, sem=None):
    """Foto real pegada con cinta en la mitad de arriba; ocupa ~80 % del ancho sin pasar de un tercio del alto."""
    pa(R, FP.F(clave), x, y, FP.s_ancho(clave, frac, alto), t0, t1, entra="pluma", sem=sem or S(), z=4,
       extra=[(0.0, "foto", 0.32)])


def rot(R, t0, t1, txt, y=330, px=72, d=None):
    R.snd(t0, "escribir", 0.32, dur=min(1.0, 0.06 * len(txt)))
    R.texto(t0, t1, txt, (CX, y), px=px, d=d if d is not None else min(0.9, 0.05 * len(txt) + 0.25))


def cortes(R):
    pass


def construir(R):
    _rotulos(R)
    _gancho(R)
    _origenes(R)
    _fundacion(R)
    _siglos(R)


def _rotulos(R):
    R.mar("mx", "SIERRA GORDA", -99.55, 21.25, 26, 0.32, rot=-0.3, color=TIERRA_TXT)
    R.mar("mx", "SEMIDESIERTO", -99.78, 20.92, 22, 0.30, color=TIERRA_TXT)
    R.mar("mx", "EL BAJÍO", -100.75, 20.45, 26, 0.30, color=TIERRA_TXT)
    for txt, lon, lat in (("QUERÉTARO", -99.95, 21.05), ("GUANAJUATO", -100.82, 21.2), ("HIDALGO", -99.2, 20.4),
                          ("ESTADO DE MÉXICO", -99.75, 19.75), ("SAN LUIS POTOSÍ", -100.2, 22.25)):
        R.mar("mx", txt, lon, lat, 24, 0.28, color=EDO_TXT)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    i0 = INI(e)
    t_mon, t_dic, t_cier = T(e, "monumento"), T(e, "dice"), T(e, "cierto")
    t_sal, t_cap, t_dias, t_est, t_tren, t_nom = T(e, "sal"), T(e, "capital"), T(e, "dias"), T(e, "estacion"), T(e, "tren"), T(e, "nombre")
    t_his, t_teq, t_baj, t_lle = T(e, "historia"), T(e, "tequisquiapan"), T(e, "bajio"), T(e, "llegar")
    fin = FIN(e)

    # cámara: el monumento de cerca → la zona Tequis-Bernal → el estado entero (el Bajío)
    R.camara(0.0, -99.888, 20.512, 6.2)
    R.camara(t_cier, -99.889, 20.515, 5.6)
    R.camara(t_tren - 0.4, -99.91, 20.6, 3.3)
    R.camara(t_his - 0.3, -99.93, 20.62, 2.4)
    R.camara(t_baj + 0.2, -99.95, 20.75, 1.05)
    R.camara(fin - 0.25, -99.95, 20.78, 1.0)

    # f0: «aquí está el centro de México»… y no es cierto
    R.anio(i0 + 0.1, 2026)
    ga(R, CE(0), CI["centro_geografico"], i0, t_his, s=0.42, zs=0.25, sem=S(), z=2, entra="sube", dy=200,
       extra=[(0.05, "crece", 0.3)])
    foto(R, "centro_1", t_mon - 0.1, t_sal - 0.1)
    rot(R, t_dic, t_cier + 0.9, "«AQUÍ ESTÁ EL", y=310, px=64)
    rot(R, t_dic + 0.35, t_cier + 0.9, "CENTRO DE MÉXICO»", y=390, px=64)
    pa(R, CE(2), 290, YP, 0.8, t_dic + 0.2, t_cier + 0.9, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    R.texto(t_cier - 0.15, t_cier + 0.9, "…Y NO ES CIERTO", (CX + 60, 1360), px=58, d=0.3)
    R.snd(t_cier - 0.1, "sello", 0.42)

    # f1: una sal · capital por unos días · la estación «Bernal»
    pa(R, OR(4), 220, YP, 0.72, t_sal - 0.15, t_his - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    R.texto(t_sal + 0.05, t_his - 0.3, "UNA SAL", (220, 1080), px=44, d=0.25)
    pa(R, SI(6), CX, YP, 0.82, t_cap - 0.15, t_his - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    R.texto(t_cap + 0.05, t_his - 0.3, "CAPITAL", (CX, 1040), px=44, d=0.25)
    R.texto(t_dias - 0.1, t_his - 0.3, "¿UNOS DÍAS?", (CX, 1100), px=36, d=0.25)
    pa(R, SI(2), lambda t: 1300 - 470 * min(1.0, max(0.0, (t - t_tren + 0.3) / 1.4)), lambda t: YP, 0.62, t_tren - 0.3, t_his - 0.2,
       sem=S(), z=3, flip=True, extra=[(0.0, "tren", 0.32, {"dur": 2.4})])
    R.texto(t_nom - 0.05, t_his - 0.3, "«BERNAL»", (830, 1110), px=46, d=0.25)
    ciudad(R, t_est, t_his, "pena_bernal", "PEÑA DE BERNAL", "arriba", 34)

    # f2: título + el corazón del Bajío + cómo llegar
    rot(R, t_his - 0.15, fin + 0.6, "LA HISTORIA DE", y=300, px=58)
    rot(R, t_teq - 0.15, fin + 0.6, "TEQUISQUIAPAN", y=392, px=96)
    foto(R, "tequis_noche", t_his - 0.05, t_baj + 0.3, y=1220)
    R.terreno(t_baj - 0.3, "edo_queretaro", COL["edo_queretaro"], 1.0)
    ciudad(R, t_baj, fin + 0.5, "tequisquiapan", "TEQUISQUIAPAN", "der", 34)
    ciudad(R, t_baj + 0.2, fin + 0.5, "queretaro", "QUERÉTARO", "izq", 30)
    R.texto(t_lle - 0.2, fin + 0.6, "y cómo llegar a cada lugar", (CX, 486), px=44, d=0.5)
    pa(R, CE(6), 270, YP, 0.85, t_lle - 0.3, fin + 0.5, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    pa(R, BE(4), 620, YP, 0.85, t_lle - 0.15, fin + 0.5, sem=S(), z=3, extra=[(0.03, "pasos", 0.22, {"dur": 0.6})])
    R.terreno(fin + 0.3, None, COL["edo_queretaro"], 0.5)


# ------------------------------------------------------------------ ORÍGENES
def _origenes(R):
    e = "origenes"
    i0, fin = INI(e), FIN(e)
    t_agua = T(e, "agua", frase=0)
    t_oto, t_chi, t_man, t_tra, t_ban = T(e, "otomies"), T(e, "chichimecas"), T(e, "manantiales"), T(e, "tratos"), T(e, "banarse")
    t_nah, t_nom, t_teq, t_lug, t_tqt = T(e, "nahuatl"), T(e, "nombre"), T(e, "tequisquiapan"), T(e, "lugar"), T(e, "tequesquite", frase=2)
    t_sal, t_bla, t_esq = T(e, "sal", frase=3), T(e, "blanca"), T(e, "esquites")

    R.camara(i0 - 0.2, -99.9, 20.56, 2.2)
    R.camara(t_agua, -99.895, 20.53, 4.6)
    R.camara(t_oto - 0.2, -99.9, 20.6, 2.0)
    R.camara(t_ban - 0.2, -99.893, 20.525, 5.2)
    R.camara(t_nom - 0.2, -99.892, 20.523, 6.0)
    R.camara(fin - 0.25, -99.892, 20.522, 6.4)

    R.sello(i0 + 0.2, "maiz", "OTOMÍES", color=(176, 116, 52))
    R.anio(i0 + 0.1, 0)              # «antes de 1551» (escenas.texto_anio): no hay fecha documentada
    # f0: el agua caliente que ya brotaba
    ga(R, OR(8), TEQ, i0 + 0.1, t_nah, s=0.5, zs=0.25, sem=S(), z=2, entra="sube", dy=160,
       extra=[(0.05, "agua_termal", 0.35, {"dur": 3.0})])
    rot(R, i0 + 0.2, t_oto - 0.1, "ANTES DE LOS ESPAÑOLES", y=330, px=58)
    R.texto(t_agua - 0.1, t_oto - 0.1, "AGUA CALIENTE", (CX, 1360), px=56, d=0.35)
    ga(R, OR(7), TEQ, i0 + 0.5, t_nah, s=0.42, off=(-230, 40), zs=0.25, sem=S(), z=1)
    ga(R, OR(6), TEQ, i0 + 0.7, t_nah, s=0.36, off=(230, 50), zs=0.25, sem=S(), z=1)

    # f1: otomíes y chichimecas → tratos y baño
    R.terreno(t_oto - 0.3, "otomies", (196, 150, 96), 0.9, capa=1)
    R.terreno(t_chi - 0.2, "chichimecas", (170, 112, 82), 0.9, capa=2)
    pa(R, OR(0), 200, YP, 0.8, t_oto - 0.1, t_nah - 0.1, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    pa(R, OR(1), 410, YP + 8, 0.78, t_oto + 0.15, t_nah - 0.1, sem=S(), z=3)
    pa(R, OR(2), 740, YP, 0.82, t_chi - 0.05, t_nah - 0.1, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    R.texto(t_oto, t_man, "OTOMÍES", (300, 1050), px=44, d=0.25)
    R.texto(t_chi + 0.05, t_man, "CHICHIMECAS", (740, 1050), px=44, d=0.25)
    foto(R, "codice_chich", t_man - 0.2, t_nah - 0.2, frac=0.62, alto=0.34)
    R.texto(t_tra - 0.05, t_nah - 0.2, "TRATOS…", (250, 1330), px=48, d=0.25)
    ga(R, OR(3), TEQ, t_ban - 0.2, t_nah + 0.2, s=0.5, off=(0, 20), zs=0.25, sem=S(), z=3,
       extra=[(0.03, "chapuzon", 0.35)])
    R.texto(t_ban, t_nah - 0.2, "…Y BAÑARSE", (780, 1330), px=48, d=0.25)
    R.terreno(t_nah - 0.2, None, (196, 150, 96), 0.6, capa=1)
    R.terreno(t_nah - 0.2, None, (170, 112, 82), 0.6, capa=2)

    # f2: el nombre en náhuatl
    rot(R, t_nom - 0.1, fin + 0.3, "TEQUISQUIAPAN", y=330, px=92)
    R.texto(t_lug - 0.1, fin + 0.3, "«lugar sobre el agua", (CX, 440), px=46, d=0.45)
    R.texto(t_lug + 0.4, fin + 0.3, "de tequesquite»", (CX, 500), px=46, d=0.45)
    ga(R, OR(8), TEQ, t_nom - 0.2, fin + 0.3, s=0.6, off=(0, -150), zs=0.2, sem=S(), z=2, extra=[(0.03, "agua_termal", 0.25, {"dur": 2})])
    pa(R, OR(4), 330, YP, 0.95, t_tqt - 0.15, fin + 0.3, sem=S(), z=3, extra=[(0.03, "brillo", 0.3)])
    R.texto(t_tqt + 0.1, t_sal, "TEQUESQUITE", (330, 1040), px=40, d=0.25)
    # f3: la sal blanca de los esquites
    R.texto(t_bla - 0.1, fin + 0.3, "SAL BLANCA", (330, 1040), px=44, d=0.25)
    pa(R, OR(5), 760, YP, 0.95, t_esq - 0.3, fin + 0.3, sem=S(), z=3, entra="sube", dy=240, extra=[(0.03, "pop", 0.3)])
    R.texto(t_esq, fin + 0.3, "¡ESQUITES!", (760, 1040), px=52, d=0.25)


# ------------------------------------------------------------------ FUNDACIÓN
def _fundacion(R):
    e = "fundacion"
    i0, fin = INI(e), FIN(e)
    t_fun, t_24, t_1551, t_lar, t_san, t_agu = (T(e, "fundacion"), T(e, "24"), T(e, "1551"), T(e, "larguisimo"), T(e, "santa"),
                                               T(e, "aguas"))
    t_tra, t_cac, t_cru, t_mez, t_ley = T(e, "tradicion"), T(e, "cacique"), T(e, "cruz"), T(e, "mezquite"), T(e, "leyenda")
    t_1567, t_pil, t_hue, t_hac, t_hoy, t_par = (T(e, "1567"), T(e, "pila"), T(e, "huertas"), T(e, "hacienda"), T(e, "hoy"),
                                                T(e, "parque"))
    t_def, t_1656 = T(e, "definitivo"), T(e, "1656")

    R.camara(i0 - 0.2, -99.9, 20.6, 1.7)
    R.camara(t_lar, -99.893, 20.53, 3.6)
    R.camara(t_tra - 0.2, -99.892, 20.522, 6.2)
    R.camara(t_1567 - 0.2, -99.893, 20.524, 5.6)
    R.camara(t_def - 0.2, -99.892, 20.522, 4.2)
    R.camara(fin - 0.25, -99.892, 20.522, 4.0)

    # f0: 24 de julio de 1551 y el nombre larguísimo
    R.anio(t_24 - 0.2, 1551)
    R.sello(t_1551 + 0.3, "corona", "NUEVA ESPAÑA", color=(178, 60, 60))
    R.terreno(i0 + 0.2, "nueva_espana", COL["nueva_espana"], 1.0, capa=3)
    pa(R, FU(4), CX, YP, 1.0, t_fun - 0.1, t_tra - 0.2, sem=S(), z=3, entra="sube", dy=260, extra=[(0.03, "papel", 0.35)])
    rot(R, t_24 - 0.1, t_lar, "24 DE JULIO DE 1551", y=330, px=66)
    rot(R, t_san - 0.15, t_tra - 0.2, "SANTA MARÍA DE LA ASUNCIÓN", y=310, px=48)
    rot(R, t_agu - 0.2, t_tra - 0.2, "Y DE LAS AGUAS CALIENTES", y=380, px=48)
    foto(R, "parroquia_1", t_lar - 0.2, t_tra - 0.3)
    R.terreno(t_tra - 0.3, None, COL["nueva_espana"], 0.6, capa=3)

    # f1: la cruz bajo el mezquite (leyenda)
    ga(R, FU(2), PLAZA, t_tra - 0.1, t_1567 - 0.2, s=0.62, off=(-40, 0), zs=0.2, sem=S(), z=2, entra="sube", dy=220,
       extra=[(0.05, "crece", 0.3)])
    pa(R, FU(0), 260, YP, 0.88, t_cac - 0.1, t_1567 - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    ga(R, FU(3), PLAZA, t_cru - 0.1, t_1567 - 0.2, s=0.42, off=(90, 10), zs=0.2, sem=S(), z=3, extra=[(0.03, "golpe_suave", 0.35)])
    pa(R, FU(1), 760, YP, 0.86, t_mez - 0.1, t_1567 - 0.2, sem=S(), z=3)
    R.texto(t_tra, t_ley - 0.1, "DICE LA TRADICIÓN…", (CX, 330), px=56, d=0.4)
    R.texto(t_ley - 0.1, t_1567 - 0.25, "¿LEYENDA?", (CX, 330), px=80, d=0.25)
    R.snd(t_ley - 0.1, "pluck", 0.35)

    # f2: La Pila Grande (1567) → hoy Parque La Pila
    R.anio(t_1567 - 0.1, 1567)
    ga(R, FU(5), TEQ, t_1567 - 0.25, t_def - 0.2, s=0.6, off=(-60, 30), zs=0.2, sem=S(), z=2, entra="sube", dy=200,
       extra=[(0.05, "agua_termal", 0.25, {"dur": 1.5})])
    rot(R, t_pil - 0.1, t_def - 0.2, "LA PILA GRANDE", y=330, px=70)
    pa(R, FU(6), 260, YP, 0.86, t_hue - 0.1, t_def - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.22)])
    pa(R, FU(8), 760, YP, 0.86, t_hac - 0.1, t_def - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.22)])
    R.anio(t_hoy - 0.1, 2026)
    R.texto(t_hoy, t_def - 0.2, "HOY: PARQUE LA PILA", (CX, 420), px=48, d=0.35)
    foto(R, "calle", t_hoy - 0.1, t_def + 1.6, frac=0.7)

    # f3: 1656, el nombre definitivo
    R.anio(t_1656 - 0.2, 1656)
    rot(R, t_def - 0.1, fin + 0.4, "1656: TEQUISQUIAPAN", y=330, px=66)
    pa(R, FU(4), CX, YP, 0.9, t_def - 0.1, fin + 0.4, sem=S(), z=3, extra=[(0.03, "sello", 0.38)])


# ------------------------------------------------------------------ SIGLOS (1897-1920)
def _siglos(R):
    e = "siglos"
    i0, fin = INI(e), FIN(e)
    t_1897, t_par, t_rel, t_pes, t_150 = T(e, "1897"), T(e, "parroquia"), T(e, "reloj"), T(e, "pesas"), T(e, "150")
    t_1902, t_tren, t_est, t_ber, t_pena = T(e, "1902"), T(e, "tren"), T(e, "estacion"), T(e, "bernal"), T(e, "pena")
    t_1910, t_pres, t_luz = T(e, "1910"), T(e, "presa"), T(e, "luz")
    t_1920, t_reb, t_carr, t_gob, t_cap, t_qro, t_dias = (T(e, "1920"), T(e, "rebelion"), T(e, "carranza"), T(e, "gobernador"),
                                                         T(e, "capital"), T(e, "queretaro"), T(e, "dias"))

    R.camara(i0 - 0.2, -99.892, 20.522, 5.4)
    R.camara(t_1902 - 0.1, -99.9, 20.58, 3.0)
    R.camara(t_ber, -99.915, 20.64, 2.6)
    R.camara(t_1910 - 0.2, -99.905, 20.5, 5.2)
    R.camara(t_1920 - 0.2, -99.93, 20.6, 2.0)
    R.camara(t_qro, -99.95, 20.78, 1.05)
    R.camara(fin - 0.25, -99.95, 20.78, 1.0)

    # f0: 1897, el reloj de pesas de la parroquia
    R.anio(t_1897 - 0.2, 1897)
    ga(R, SI(0), PLAZA, i0 - 0.15, t_1902 - 0.2, s=0.6, zs=0.2, sem=S(), z=2, entra="sube", dy=220,
       extra=[(0.05, "campana", 0.3)])
    foto(R, "parroquia_2", t_par - 0.1, t_150 + 0.4)
    pa(R, SI(1), CX, YP, 1.0, t_rel - 0.15, t_1902 - 0.2, sem=S(), z=3, extra=[(0.03, "reloj", 0.4, {"dur": 2.5})])
    R.texto(t_rel, t_pes, "UN RELOJ DE PESAS", (CX, 330), px=60, d=0.35)
    R.contador(t_pes, t_1902 - 0.2, 0, 150, (CX, 330), px=84, formato="{} KILOS", hasta_t=t_150 + 0.5)

    # f1: 1902, el tren y la estación «Bernal»
    R.anio(t_1902 - 0.2, 1902)
    R.sello(t_1902 + 0.2, "locomotora", "PORFIRIATO", color=(196, 146, 68))
    R.ruta(M.RUTAS["tren"], t_tren - 0.3, 2.4, ancho=6.0, dash=18, hueco=10, t1=t_1910 - 0.3)
    pa(R, SI(2), lambda t: -250 + 1100 * min(1.0, max(0.0, (t - t_tren + 0.2) / 3.2)), lambda t: YP, 0.75, t_tren - 0.2, t_1910 - 0.3,
       sem=S(), z=3, extra=[(0.0, "tren", 0.4, {"dur": 3.5})])
    ga(R, SI(3), TEQ, t_est - 0.15, t_1910 - 0.3, s=0.45, off=(-180, -120), zs=0.25, sem=S(), z=2, extra=[(0.03, "pop", 0.25)])
    rot(R, t_ber - 0.2, t_1910 - 0.3, "ESTACIÓN «BERNAL»", y=330, px=66)
    ciudad(R, t_ber, t_1910 - 0.3, "bernal", "BERNAL", "arriba", 34)
    ga(R, BE(0), CI["pena_bernal"], t_pena - 0.2, t_1910 - 0.3, s=0.5, zs=0.25, sem=S(), z=2, entra="sube", dy=200,
       extra=[(0.03, "crece", 0.3)])

    # f2: 1910, la Presa Centenario y la primera luz eléctrica
    R.anio(t_1910 - 0.2, 1910)
    ga(R, SI(4), CI["presa_centenario"], t_1910 - 0.3, t_1920 - 0.2, s=0.55, zs=0.2, sem=S(), z=2, entra="sube", dy=200,
       extra=[(0.05, "presa", 0.32, {"dur": 2.0})])
    ciudad(R, t_pres, t_1920 - 0.2, "presa_centenario", "PRESA CENTENARIO", "abajo", 32)
    pa(R, SI(5), CX, YP, 1.05, t_luz - 0.3, t_1920 - 0.2, sem=S(), z=3, extra=[(0.25, "luz", 0.42)])
    rot(R, t_luz - 0.1, t_1920 - 0.2, "PRIMERA LUZ ELÉCTRICA", y=330, px=62)

    # f3: mayo de 1920, capital de Querétaro… por unos días
    R.anio(t_1920 - 0.2, 1920)
    R.sello(t_reb, "sombrero_rev", "REVOLUCIÓN", color=(198, 70, 60))
    R.act(lambda t, k=0: C_JIN[int(t * 10) % len(C_JIN)], pos=lambda t: (1250 - 1500 * min(1.0, max(0.0, (t - t_1920 + 0.3) / 4.2)), YP, 0.72),
          t_in=t_1920 - 0.3, d_in=0.3, entra="pop", sem=S(), t_out=t_carr + 0.6, z=3, flip=True,
          sfx=[(0.0, "galope", 0.38, {"dur": 2.4})])
    foto(R, "carranza", t_carr - 0.15, t_cap - 0.1, frac=0.5, alto=0.34)
    R.texto(t_carr, t_gob, "VS. CARRANZA", (CX, 330), px=60, d=0.3)
    pa(R, SI(6), CX, YP, 0.95, t_gob - 0.15, fin + 0.4, sem=S(), z=3, extra=[(0.03, "papel", 0.3)])
    R.terreno(t_cap - 0.3, "edo_queretaro", COL["edo_queretaro"], 0.9, capa=4)
    rot(R, t_cap - 0.1, fin + 0.4, "CAPITAL DE QUERÉTARO", y=330, px=64)
    ga(R, CE(2), TEQ, t_cap, fin + 0.4, s=0.5, off=(150, -300), zs=0.3, sem=S(), z=3, entra="sube", dy=200, extra=[(0.03, "sello", 0.4)])
    R.texto(t_dias - 0.15, fin + 0.4, "…POR UNOS DÍAS", (CX, 420), px=52, d=0.3)
    R.terreno(fin + 0.3, None, COL["edo_queretaro"], 0.5, capa=4)
