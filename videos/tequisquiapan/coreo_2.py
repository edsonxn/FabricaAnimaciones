# -*- coding: utf-8 -*-
"""Coreografía (2/2) de «La historia de Tequisquiapan» (VERTICAL): el «centro de México» (placa de 1978, el decreto que no aparece,
el centro calculado en Zacatecas), el turismo (años 50, Feria del Queso y el Vino 1976, Pueblo Mágico 2012, cestería, ópalos,
la Peña de Bernal) y la ruta para comprobarlo (con la frase «te dejo en la descripción cómo llegar», regla del 22-oct-2026) y el
cierre del agua. Misma composición que coreo_1. Semillas 300-599."""
import mapa as M
from core import FIN, INI, T
from coreo_1 import BE, CE, CX, FU, SI, TEQ, YF, YP, foto, rot
from coreo_util import CI, COL, ciudad, ga, pa
from pegflow import P, ciclo

TU = lambda n, **k: P("05_turismo_hoja", n, **k)     # 0 coche·1 alberca·2 queso·3 vino·4 puesto·5 artesano·6 cestos·7 ópalo·8 minero
C_TUR = ciclo("07_turista_camina")
_S = [300]


def S():
    _S[0] += 1
    return _S[0]


def cortes(R):
    pass


def construir(R):
    _centro(R)
    _turismo(R)
    _ruta(R)


# ------------------------------------------------------------------ EL «CENTRO DE MÉXICO»
def _centro(R):
    e = "centro"
    i0, fin = INI(e), FIN(e)
    t_cen, t_mon, t_1978, t_pla, t_ven = T(e, "centro"), T(e, "monumento"), T(e, "1978"), T(e, "placa"), T(e, "venustiano")
    t_nad, t_dec, t_calc, t_zac, t_450, t_km = (T(e, "nadie"), T(e, "decreto"), T(e, "calculado"), T(e, "zacatecas"), T(e, "450"),
                                               T(e, "kilometros"))
    geo = CI["centro_geografico"]

    R.camara(i0 - 0.2, -99.889, 20.515, 5.0)
    R.camara(t_mon, -99.888, 20.514, 6.4)
    R.camara(t_nad - 0.2, -99.89, 20.52, 5.0)
    R.camara(t_calc, -100.2, 21.2, 0.85)
    R.camara(fin - 0.25, -100.2, 21.25, 0.8)

    rot(R, i0 + 0.05, t_mon - 0.1, "¿EL CENTRO DE MÉXICO?", y=330, px=64)
    ga(R, CE(0), geo, i0 + 0.1, t_calc, s=0.55, zs=0.2, sem=S(), z=2, entra="sube", dy=220, extra=[(0.05, "crece", 0.3)])
    R.anio(t_1978 - 0.2, 1978)
    foto(R, "centro_2", t_mon - 0.15, t_pla - 0.1)
    R.texto(t_1978, t_pla - 0.1, "MONUMENTO DE 1978", (CX, 330), px=60, d=0.3)
    foto(R, "centro_3", t_pla - 0.15, t_nad + 0.3, sem=S())
    R.texto(t_pla, t_nad, "LA PLACA DICE: CARRANZA", (CX, 330), px=54, d=0.35)
    pa(R, CE(1), 270, YP, 0.88, t_ven - 0.2, t_calc, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    pa(R, CE(3), 760, YP, 0.86, t_mon + 0.3, t_calc, sem=S(), z=3, extra=[(0.03, "camara", 0.3)])

    # f1: el decreto no aparece · el centro calculado está en Zacatecas, a 450 km
    pa(R, CE(4), CX, YP - 260, 1.1, t_dec - 0.2, t_calc + 0.2, sem=S(), z=4, entra="sube", dy=260, extra=[(0.03, "papel", 0.3)])
    R.texto(t_dec - 0.05, t_calc, "¿Y EL DECRETO? NO APARECE", (CX, 330), px=52, d=0.3)
    R.snd(t_dec + 0.4, "pluck", 0.32)
    R.ruta([geo, (-100.25, 20.95), (-100.6, 21.5), (-100.98, 22.38)], t_calc + 0.2, 1.4, ancho=6.0, t1=fin + 0.4, flecha=True)
    rot(R, t_calc + 0.1, fin + 0.4, "EL CENTRO CALCULADO:", y=310, px=52)
    pa(R, CE(6), 300, YP, 0.85, t_calc + 0.1, fin + 0.4, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    rot(R, t_zac + 0.1, fin + 0.4, "ZACATECAS", y=388, px=88)
    R.contador(t_450 - 0.3, fin + 0.4, 0, 450, (CX, 1400), px=88, formato="{} KM", hasta_t=t_km + 0.3)
    ga(R, CE(2), geo, t_calc + 0.1, fin + 0.4, s=0.32, zs=0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    pa(R, CE(5), 840, 1180, 0.6, t_calc, fin + 0.4, sem=S(), z=3, extra=[(0.03, "whoosh", 0.25)])


# ------------------------------------------------------------------ TURISMO
def _turismo(R):
    e = "turismo"
    i0, fin = INI(e), FIN(e)
    t_cin, t_fam, t_cap, t_ter = T(e, "cincuenta"), T(e, "familias"), T(e, "capital"), T(e, "termales")
    t_1976, t_fer, t_que, t_vin, t_2012, t_mag = T(e, "1976"), T(e, "feria"), T(e, "queso"), T(e, "vino"), T(e, "2012"), T(e, "magico")
    t_art, t_ces, t_cer, t_opa, t_pena, t_vol, t_433 = (T(e, "artesanos"), T(e, "cestos"), T(e, "cerros"), T(e, "opalos"), T(e, "pena"),
                                                      T(e, "volcan"), T(e, "433"))
    mx = CI["mexico"]

    R.camara(i0 - 0.2, -99.6, 19.95, 1.3)
    R.camara(t_ter - 0.4, -99.85, 20.4, 2.8)
    R.camara(t_1976 - 0.2, -99.892, 20.522, 5.4)
    R.camara(t_art - 0.2, -99.893, 20.525, 4.6)
    R.camara(t_pena - 0.4, -99.94, 20.735, 3.4)
    R.camara(fin - 0.25, -99.945, 20.74, 3.6)

    # f0: años 50, las familias de la capital y sus aguas termales
    R.anio(i0 + 0.1, 1955)
    R.sello(i0 + 0.4, "campana", "TURISMO", color=(60, 120, 150))
    P_cdmx = [mx, (-99.55, 19.95), (-99.8, 20.25), (-99.99, 20.39), TEQ]
    R.ruta(P_cdmx, t_cin, 2.6, ancho=6.0, t1=t_1976 - 0.3, flecha=True)
    R.act(TU(0), pos_geo=R.camino_pos(P_cdmx, i0, 5.2), s=0.42, zs=0.25, t_in=i0 - 0.1, d_in=0.4, entra="pop", sem=S(),
          t_out=t_1976 - 0.2, sale="encoger", z=3, flip=False, sfx=[(0.0, "whoosh", 0.3)])
    ciudad(R, t_cin, t_1976 - 0.3, "mexico", "CIUDAD DE MÉXICO", "abajo", 30)
    rot(R, t_cin - 0.1, t_ter - 0.2, "LOS AÑOS 50: LA FAMA", y=330, px=62)
    pa(R, CE(7), 280, YP, 0.86, i0 - 0.1, t_1976 - 0.2, sem=S(), z=3, extra=[(0.03, "multitud", 0.25, {"dur": 2.0})])
    pa(R, TU(1), 760, YP, 0.92, t_ter - 0.2, t_1976 - 0.2, sem=S(), z=3, extra=[(0.03, "chapuzon", 0.35)])
    rot(R, t_ter - 0.1, t_1976 - 0.2, "AGUAS TERMALES", y=330, px=70)
    foto(R, "relox", t_ter - 0.15, t_1976 + 1.2, frac=0.72)

    # f1: 1976 Feria del Queso y el Vino · 2012 Pueblo Mágico
    R.anio(t_1976 - 0.2, 1976)
    foto(R, "feria_entrada", t_fer - 0.15, t_2012 - 0.15, frac=0.72)
    rot(R, t_fer - 0.1, t_2012 - 0.2, "FERIA DEL QUESO Y EL VINO", y=330, px=50)
    pa(R, TU(2), 250, YP, 0.7, t_que - 0.15, t_2012 + 0.3, sem=S(), z=3, extra=[(0.03, "pop", 0.25)])
    pa(R, TU(3), 520, YP, 0.86, t_vin - 0.15, t_2012 + 0.3, sem=S(), z=3, extra=[(0.03, "copas", 0.35)])
    pa(R, TU(4), 790, YP, 0.82, t_vin + 0.2, t_2012 + 0.3, sem=S(), z=3, extra=[(0.03, "feria", 0.25, {"dur": 2.5})])
    R.anio(t_2012 - 0.2, 2012)
    rot(R, t_mag - 0.4, t_art - 0.2, "PUEBLO MÁGICO", y=330, px=84)
    R.snd(t_mag - 0.3, "brillo", 0.4)
    foto(R, "kiosco", t_2012 - 0.1, t_art - 0.1, frac=0.72)

    # f2: cestos de vara · ópalos · la Peña de Bernal (un volcán que nunca salió, 433 m)
    foto(R, "artesano", t_art - 0.15, t_cer - 0.1, frac=0.7)
    pa(R, TU(5), 270, YP, 0.86, t_art - 0.1, t_pena - 0.2, sem=S(), z=3, extra=[(0.03, "cesteria", 0.35)])
    pa(R, TU(6), 520, YP, 0.78, t_ces - 0.1, t_pena - 0.2, sem=S(), z=3, extra=[(0.03, "pop", 0.22)])
    R.texto(t_ces, t_cer, "CESTOS DE VARA", (CX, 330), px=60, d=0.3)
    foto(R, "opalo", t_opa - 0.2, t_pena - 0.1, frac=0.6)
    pa(R, TU(7), 790, YP - 20, 0.7, t_opa - 0.1, t_pena - 0.2, sem=S(), z=3, extra=[(0.03, "brillo", 0.35)])
    R.texto(t_opa - 0.05, t_pena - 0.1, "ÓPALOS", (CX, 330), px=70, d=0.25)
    ga(R, BE(0), CI["pena_bernal"], t_pena - 0.3, fin + 0.4, s=0.6, zs=0.25, sem=S(), z=2, entra="sube", dy=240,
       extra=[(0.05, "crece", 0.32)])
    foto(R, "bernal_1", t_pena - 0.15, t_vol + 0.2, frac=0.62)
    rot(R, t_pena - 0.1, fin + 0.4, "PEÑA DE BERNAL", y=330, px=76)
    pa(R, BE(1), CX, YP, 1.15, t_vol - 0.2, fin + 0.4, sem=S(), z=3, entra="sube", dy=280, extra=[(0.05, "volcan", 0.4)])
    R.texto(t_vol, t_433, "UN VOLCÁN QUE NUNCA SALIÓ", (CX, 420), px=46, d=0.4)
    R.contador(t_433 - 0.2, fin + 0.4, 0, 433, (CX, 420), px=80, formato="{} METROS", hasta_t=t_433 + 0.8)


# ------------------------------------------------------------------ RUTA PARA COMPROBARLO + CIERRE
def _ruta(R):
    e = "ruta"
    i0, fin = INI(e), FIN(e)
    t_par, t_rel, t_pla, t_mon, t_pil, t_mer, t_pre, t_pena = (T(e, "parroquia"), T(e, "reloj"), T(e, "plaza"), T(e, "monumento"),
                                                               T(e, "pila"), T(e, "mercado"), T(e, "presa"), T(e, "pena"))
    t_des, t_lle = T(e, "descripcion"), T(e, "llegar")
    t_agua, t_acu, t_5, t_cub = T(e, "termales"), T(e, "acuifero"), T(e, "5"), T(e, "cubicos")
    t_cui, t_dim, t_baj = T(e, "cuidala"), T(e, "dime"), T(e, "bajio")

    R.camara(i0 - 0.2, -99.892, 20.522, 6.0)
    R.camara(t_pre - 0.3, -99.9, 20.51, 5.0)
    R.camara(t_pena - 0.2, -99.93, 20.62, 2.8)
    R.camara(t_des, -99.93, 20.62, 2.7)
    R.camara(t_acu, -99.892, 20.53, 3.4)
    R.camara(t_dim, -99.95, 20.78, 1.05)
    R.camara(fin - 0.25, -99.95, 20.8, 1.0)

    R.anio(i0, 2026)
    rot(R, i0 + 0.05, t_des - 0.2, "PARA COMPROBARLO", y=330, px=70)
    # f0: lista rápida de lugares, cada uno con su foto o su dibujo y su punto en el mapa
    paradas = [(t_par, "parroquia_1", "plaza_tequis", "PARROQUIA"), (t_pla, "plaza", None, None),
               (t_mon, "pendulo", None, None), (t_pil, None, None, None),
               (t_mer, "mercado_1", None, None), (t_pre, None, "presa_centenario", "PRESA"), (t_pena, "bernal_3", "pena_bernal", "PEÑA")]
    for k, (t, clave, cl, txt) in enumerate(paradas):
        t1 = paradas[k + 1][0] - 0.05 if k + 1 < len(paradas) else t_des - 0.1
        if clave:
            foto(R, clave, t - 0.12, t1 + 0.25, x=CX + (-40 if k % 2 else 40), frac=0.7, sem=S())
        if cl:
            ciudad(R, t, t_des + 1.2, cl, txt, ("der", "izq")[k % 2], 30)
    pa(R, SI(1), 300, YP, 0.72, t_rel - 0.1, t_pla, sem=S(), z=3, extra=[(0.03, "reloj", 0.3, {"dur": 1.0})])
    pa(R, FU(5), CX, YP, 1.0, t_pil - 0.1, t_mer, sem=S(), z=4, entra="sube", dy=260, extra=[(0.03, "agua_termal", 0.3, {"dur": 1.0})])
    R.texto(t_pil, t_mer - 0.05, "PARQUE LA PILA", (CX, 1060), px=52, d=0.25)
    pa(R, SI(4), CX, YP, 1.0, t_pre - 0.1, t_pena, sem=S(), z=4, entra="sube", dy=260, extra=[(0.03, "presa", 0.3, {"dur": 1.0})])
    R.ruta(M.RUTAS["tequis_bernal"], t_pena - 0.2, 1.6, ancho=6.0, t1=t_acu - 0.2)
    R.act(lambda t: C_TUR[int(t * 9) % len(C_TUR)], pos_geo=R.camino_pos(M.RUTAS["tequis_bernal"], t_pena - 0.1, 4.0), s=0.36, zs=0.25,
          t_in=t_pena - 0.1, d_in=0.3, entra="pop", sem=S(), t_out=t_acu - 0.2, z=3, flip=False, sfx=[(0.0, "pasos", 0.25, {"dur": 1.5})])

    # f1: «Te dejo en la descripción cómo llegar a cada lugar»
    rot(R, t_des - 0.3, t_agua - 0.5, "CÓMO LLEGAR A CADA LUGAR:", y=310, px=48)
    rot(R, t_des - 0.1, t_agua - 0.5, "EN LA DESCRIPCIÓN", y=390, px=74)
    pa(R, CE(2), 300, YP, 0.9, t_des - 0.2, t_agua - 0.3, sem=S(), z=3, entra="sube", dy=220, extra=[(0.03, "pop", 0.3)])
    pa(R, BE(4), 700, YP, 0.92, t_lle - 0.3, t_agua - 0.3, sem=S(), z=3, extra=[(0.03, "papel", 0.3)])

    # f2: el acuífero pierde 5 millones de m³ al año
    R.terreno(t_agua - 0.3, "municipio_tequis", COL["municipio_tequis"], 0.9, capa=5)
    pa(R, BE(5), 280, YP, 0.95, t_agua - 0.1, t_cui - 0.2, sem=S(), z=3, entra="sube", dy=240, extra=[(0.03, "gotas", 0.35, {"dur": 2.0})])
    pa(R, BE(6), 560, YP, 0.86, t_acu - 0.2, t_cui - 0.2, sem=S(), z=3)
    pa(R, BE(7), 820, YP - 40, 0.7, t_acu + 0.1, t_cui - 0.2, sem=S(), z=3)
    rot(R, t_agua + 0.35, t_acu - 0.1, "SE QUEDA SIN AGUA", y=330, px=70)
    R.contador(t_5 - 0.1, t_cui - 0.2, 0, 5000000, (CX, 330), px=74, formato="{:,} m³", hasta_t=t_5 + 0.9)
    R.texto(t_cub, t_cui - 0.2, "MENOS CADA AÑO", (CX, 420), px=46, d=0.3)
    R.terreno(t_cui - 0.2, None, COL["municipio_tequis"], 0.5, capa=5)

    # f3: cuídala · ¿qué pueblo del Bajío contamos después?
    R.texto(t_cui - 0.1, t_dim - 0.1, "¡CUÍDALA!", (CX, 330), px=90, d=0.25)
    pa(R, BE(5), CX, YP, 1.1, t_cui - 0.1, t_dim, sem=S(), z=3, extra=[(0.03, "brillo", 0.3)])
    rot(R, t_dim + 0.25, fin + 1.2, "¿QUÉ PUEBLO DEL BAJÍO", y=310, px=56)
    rot(R, t_baj + 0.1, fin + 1.2, "CONTAMOS DESPUÉS?", y=386, px=64)
    pa(R, CE(7), CX, YP, 0.95, t_dim, fin + 1.2, sem=S(), z=3, extra=[(0.03, "pop", 0.3)])
    for k, (cl, tx) in enumerate((("bernal", "BERNAL"), ("cadereyta", "CADEREYTA"), ("san_juan_rio", "SAN JUAN DEL RÍO"), ("amealco", "AMEALCO"))):
        ciudad(R, t_baj + 0.15 * k, fin + 1.2, cl, tx, ("der", "izq", "der", "izq")[k], 28)
