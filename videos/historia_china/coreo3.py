# -*- coding: utf-8 -*-
"""Coreografía (3/3): Qing, siglo XX y hoy, cierre, y los cambios de escena procedurales entre épocas."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402
from coreo1 import pop
from trans import SFX, Transicion

COL = M.COL


def construir(R):
    _qing(R)
    _moderna(R)
    _cierre(R)
    _transiciones(R)


# ------------------------------------------------------------------ QING
def _qing(R):
    e = "qing"
    i0 = INI(e)
    t_manch, t_pekin = T(e, "manchues"), T(e, "pekin")
    t_nace, t_qing, t_grande = T(e, "nace"), T(e, "qing", frase=1), T(e, "grande")
    t_europa, t_vapor, t_canon, t_comprar, t_seda = T(e, "europa"), T(e, "vapor"), T(e, "canones"), T(e, "comprar"), T(e, "seda", frase=2)
    t_ingl, t_opio, t_frenar, t_guerra = T(e, "ingleses"), T(e, "opio"), T(e, "frenarlos"), T(e, "guerra")
    t_pierde, t_hong, t_brit = T(e, "pierde"), T(e, "hong"), T(e, "britanicas")
    t_abdica, t_nino, t_seis = T(e, "abdica"), T(e, "nino"), T(e, "seis", frase=5)
    # territorio
    R.terreno(t_pekin + 0.1, "ming", COL["qing"], 1.0)
    R.terreno(t_grande - 1.0, "qing", COL["qing"], 2.0)
    R.terreno(t_abdica, "qing", (176, 166, 152), 1.4)
    R.sello(t_qing - 0.05, "清", "Qing")
    # cámara
    R.camara(i0, 121.0, 43.0, 1.9)
    R.camara(t_pekin, 117.5, 41.0, 2.3)
    R.camara(t_grande, 105.0, 38.0, 1.12)
    R.camara(t_europa, 118.0, 24.0, 1.75)
    R.camara(t_opio, 113.6, 23.4, 3.1)
    R.camara(t_pierde, 114.2, 22.3, 4.6)
    R.camara(t_abdica, 116.4, 39.9, 2.4)
    R.camara(FIN(e), 116.4, 39.9, 2.3)
    R.anio(t_manch, 1644)
    R.anio(t_grande + 0.6, 1644)
    R.anio(t_ingl, 1839)
    R.anio(t_pierde + 0.6, 1842)
    R.anio(t_abdica + 0.2, 1912)
    # manchúes a caballo entran en Pekín
    P = [(127.5, 48.0), (122.0, 44.0), (118.5, 41.6), (116.6, 40.1)]
    R.act(C.puerta_ciudad(), geo=(116.4, 39.9), off=(0, 20), s=0.7, t_in=t_manch - 0.3, d_in=0.45, entra="pop", sem=200, sfx=[(0, "pop", 0.6)], t_out=t_grande - 0.4, sale="encoger", zs=0.5)
    for k in range(5):
        R.act(lambda t, k=k: C.jinete_manchu(int(t * 6) + k), pos_geo=R.camino_pos(P, t_manch - 0.6 + 0.14 * k, 2.6 - 0.05 * k, ease=e_inout), off=lambda t, k=k: (0, 5 * math.sin(t * 12 + k)),
              s=0.4, t_in=t_manch - 0.7 + 0.1 * k, d_in=0.25, entra="pop", sem=201 + k, flip=True, t_out=t_pekin + 0.6, sale="encoger", zs=0.5, z=1)
    R.snd(t_manch - 0.6, "galope", 0.7, dur=2.6)
    R.snd(t_manch - 0.6, "tambor", 0.6)
    R.snd(t_pekin + 0.1, "impacto", 0.7)
    # Europa: vapor y cañones, té y seda
    R.act(lambda t: C.vapor(int(t * 5)), pos_geo=R.camino_pos([(129, 16.5), (122.5, 20.6), (116.5, 21.8)], t_europa, 5.2, ease=e_out), off=lambda t: (0, 6 * math.sin(t * 3)), s=0.4, t_in=t_vapor - 0.4, d_in=0.4,
          entra="pop", sem=210, sfx=[(0, "pop", 0.5), (0.1, "campana", 0.5)], t_out=t_opio + 3.3, sale="encoger", zs=0.5, z=1)
    R.act(C.canon(), pos=(470, 800, 1.0), t_in=t_canon - 0.1, d_in=0.4, entra="pop", sem=211, sfx=[(0, "pop", 0.6), (0.25, "canonazo", 0.8)], t_out=t_ingl - 0.1, sale="encoger")
    R.act(A.estallido(10, 40, 120), pos=(620, 740, 1.0), t_in=t_canon + 0.2, d_in=0.3, entra="pop", sem=212, z=3, t_out=t_canon + 0.75, sale="encoger")
    R.act(C.caja_te(), pos=(1130, 820, 1.0), t_in=t_comprar, d_in=0.4, entra="pop", sem=213, sfx=[(0, "pop", 0.6), (0.2, "monedas", 0.5)], t_out=t_ingl - 0.1, sale="encoger")
    R.act(A.rollo_seda(), pos=(1420, 830, 0.95), t_in=t_seda, d_in=0.4, entra="pop", sem=214, sfx=[(0, "papel", 0.7)], t_out=t_ingl - 0.1, sale="encoger")
    # opio y guerra
    for k in range(3):
        R.act(C.caja_opio(), pos=(300 + 130 * k, 820 - 10 * k, 0.72), t_in=t_opio - 0.1 + 0.15 * k, d_in=0.4, entra="cae", dy=500, sem=215 + k, sfx=[(0.3, "bonk", 0.5, {"tono": 0.8})],
              t_out=t_frenar + 0.5 + 0.12 * k, sale="caer", d_out=0.9)
    R.act(C.ingles(0), pos=(800, 850, 1.0), t_in=t_ingl, d_in=0.45, entra="pop", sem=219, sfx=[(0, "pop", 0.6), (0.2, "monedas", 0.4)], t_out=t_pierde - 0.2, sale="encoger")
    R.act(C.funcionario_opio(0), pos=(1560, 840, 1.0), t_in=t_frenar - 0.1, d_in=0.45, entra="pop", sem=220, sfx=[(0, "pop", 0.6)], t_out=t_pierde - 0.2, sale="encoger")
    for k, (x, y) in enumerate(((1100, 420), (1340, 520), (800, 560))):
        R.act(A.estallido(12, 50, 150), pos=(x, y, 1.0), t_in=t_guerra + 0.2 * k, d_in=0.3, entra="pop", sem=221 + k, z=3, t_out=t_guerra + 0.2 * k + 0.6, sale="encoger", sfx=[(0, "canonazo", 0.7, {"tono": 1.0 + 0.1 * k})])
    R.snd(t_guerra - 0.2, "trueno", 0.5)
    # Hong Kong se separa del mapa
    R.act(C.isla_trozo(46), pos=(960, 540, 1.0), t_in=t_hong - 0.1, d_in=0.4, entra="pop", sem=225, sfx=[(0, "pin", 0.6)], t_out=t_brit, sale="cortar", z=2)
    R.act(C.isla_trozo(46), pos=lambda t: (lerp(960, 1580, e_inout(prog(t, t_brit, t_brit + 0.9))), lerp(540, 620, e_inout(prog(t, t_brit, t_brit + 0.9))) - 140 * math.sin(math.pi * prog(t, t_brit, t_brit + 0.9)),
                                          1.0, 0.0 + 4.0 * prog(t, t_brit, t_brit + 0.9)), t_in=t_brit, d_in=0.01, entra="fija", sem=226, t_out=t_abdica - 0.5, sale="encoger", z=2,
          sfx=[(0, "whoosh", 0.5, {"dur": 0.8}), (0.85, "splat", 0.6)])
    R.act(C.ingles(1), pos=(1600, 850, 1.0), t_in=t_brit - 0.3, d_in=0.4, entra="pop", sem=227, sfx=[(0, "pop", 0.6)], t_out=t_abdica - 0.5, sale="encoger")
    R.texto(t_hong, t_abdica - 0.6, "Hong Kong", (960, 380), px=76, d=0.7)
    # el último emperador: un niño en un trono enorme
    R.act(A.trono(), pos=(960, 900, 1.55), t_in=t_abdica, d_in=0.5, entra="pop", sem=230, sfx=[(0, "pop", 0.7)], z=-1, t_out=FIN(e) + 0.4, sale="encoger")
    R.act(C.nino_emperador(0), pos=(960, 850, 0.66), t_in=t_nino - 0.1, d_in=0.45, entra="pop", sem=231, sfx=[(0, "pop", 0.6), (0.1, "bocinazo", 0.3, {"tono": 1.4})], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.act(C.corona_grande(), pos=lambda t: (960, 660 + 70 * e_in(prog(t, t_seis, t_seis + 1.0)), 0.9, 0.0 + 0.25 * math.sin((t - t_seis) * 5) * prog(t, t_seis, t_seis + 1.0)), t_in=t_nino, d_in=0.4, entra="pop", sem=232,
          t_out=FIN(e) + 0.4, sale="encoger", z=2)
    R.texto(t_seis - 0.1, FIN(e) + 0.2, "6 años", (1340, 560), px=92, d=0.5)
    R.snd(t_seis, "escribir", 0.5, dur=0.6)


# ------------------------------------------------------------------ SIGLO XX Y HOY
def _moderna(R):
    e = "moderna"
    i0 = INI(e)
    t_term, t_emp, t_caud, t_inv, t_civil = T(e, "terminan"), T(e, "emperadores"), T(e, "caudillos"), T(e, "invasion"), T(e, "civil")
    t_nov, t_mao, t_proc = T(e, "novecientos"), T(e, "mao", frase=1), T(e, "proclama")
    t_camp, t_salto, t_ham = T(e, "campanas"), T(e, "salto"), T(e, "hambruna")
    t_muere, t_suc, t_abre, t_gato, t_rat = T(e, "muere"), T(e, "sucesor"), T(e, "abre"), T(e, "gato"), T(e, "ratones")
    t_cuar, t_cientos, t_pobr, t_seg, t_econ = T(e, "cuarenta", frase=4), T(e, "cientos"), T(e, "pobreza"), T(e, "segunda"), T(e, "economia", frase=4)
    t_hoy, t_hab, t_tren, t_rap, t_plan = T(e, "hoy"), T(e, "habitantes"), T(e, "trenes"), T(e, "rapidos"), T(e, "planeta")
    # territorio y fracturas
    R.terreno(i0 - 0.2, "rep", COL["rep"], 1.2)
    R.romper("caudillos", t_caud - 0.25, t_caud + 0.5, t_proc - 0.45, t_proc + 0.65, colores=None, gap=12, deriva=34, nervio=1.4)
    R.snd(t_caud - 0.25, "crujido", 0.9, dur=0.9)
    R.terreno(t_proc - 0.3, "prc", COL["prc"], 1.0)
    R.snd(t_proc + 0.3, "boing", 0.7)
    R.terreno(t_ham, "prc", (218, 176, 128), 1.6)
    R.terreno(t_suc, "prc", COL["prc"], 1.2)
    R.sello(t_proc + 0.1, "中", "República Popular")
    # cámara
    R.camara(i0, 109.0, 36.0, 1.3)
    R.camara(t_inv, 119.0, 35.0, 1.6)
    R.camara(t_civil, 113.0, 33.5, 1.55)
    R.camara(t_proc - 0.3, 116.4, 39.9, 2.3)
    R.camara(t_camp, 112.0, 35.0, 1.6)
    R.camara(t_muere, 110.0, 31.0, 1.7)
    R.camara(t_cuar, 118.0, 30.0, 2.0)
    R.camara(t_hoy, 106.0, 35.0, 1.3)
    R.camara(t_tren, 112.0, 33.0, 1.55)
    R.camara(FIN(e), 108.0, 34.0, 1.45)
    # contadores
    R.anio(t_term, 1912)
    R.anio(t_nov, 1912)
    R.anio(t_proc + 0.3, 1949)
    R.anio(t_salto, 1958)
    R.anio(t_ham + 1.0, 1961)
    R.anio(t_muere, 1976)
    R.anio(t_cuar, 1978)
    R.anio(t_seg + 0.8, 2010)
    R.anio(t_hoy, 2010)
    R.anio(t_hab + 0.6, 2026)
    R.texto(t_emp - 0.2, t_caud + 0.4, "más de 2.000 años de emperadores", (960, 250), px=72, d=1.0)
    # guerras: soldados en los pedazos, avión japonés, guerra civil
    for k, (lon, lat, fl) in enumerate(((113.0, 39.5, False), (118.5, 34.0, True), (105.0, 30.5, False), (113.2, 29.0, True))):
        R.act(lambda t, k=k: C.soldado_fusil(k + int(t * 3)), geo=(lon, lat), off=(0, 50), s=0.42, flip=fl, t_in=t_caud + 0.12 * k, d_in=0.4, entra="pop", sem=240 + k, sfx=[(0, "pop", 0.5), (0.15, "bonk", 0.4)],
              t_out=t_civil + 0.3, sale="encoger", zs=0.5, z=1)
    R.snd(t_caud + 0.2, "tambor", 0.6)
    Pj = [(139.5, 37.0), (131.0, 36.4), (124.0, 34.6), (121.6, 31.6)]
    R.rio(Pj, t_inv - 0.1, 1.3, (70, 62, 80), ancho=24, t1=t_civil - 0.4)
    R.act(C.avion(), pos_geo=R.camino_pos(Pj, t_inv - 0.1, 1.5, ease=e_inout), off=(0, -30), s=0.4, flip=True, t_in=t_inv - 0.15, d_in=0.3, entra="pop", sem=246, sfx=[(0, "whoosh", 0.6, {"dur": 1.4, "tono": 0.8})],
          t_out=t_civil - 0.3, sale="encoger", zs=0.5, z=1)
    R.act(A.espadas(), geo=(114.0, 33.5), off=(0, 0), s=0.85, t_in=t_civil, d_in=0.4, entra="pop", sem=247, sfx=[(0, "impacto", 0.7)], t_out=t_proc - 0.5, sale="encoger", zs=0.5)
    R.act(A.estallido(10, 40, 120), geo=(114.0, 33.5), off=(0, -20), s=0.9, t_in=t_civil + 0.1, d_in=0.3, entra="pop", sem=248, t_out=t_civil + 0.7, sale="encoger", zs=0.5)
    # 1949: la proclamación
    R.act(C.tribuna(), pos=(1420, 880, 1.0), t_in=t_proc - 0.6, d_in=0.45, entra="pop", sem=250, sfx=[(0, "pop", 0.6)], z=-1, t_out=t_camp - 0.1, sale="encoger")
    R.act(lambda t: C.lider(int(t * 2), "feliz"), pos=(1420, 760, 0.85), t_in=t_mao, d_in=0.45, entra="pop", sem=251, sfx=[(0, "pop", 0.6)], t_out=t_camp - 0.1, sale="encoger", z=1)
    R.act(C.bandera(), pos=(1000, 880, 0.9), t_in=t_proc, d_in=0.45, entra="pop", sem=252, sfx=[(0, "pop", 0.6), (0.1, "brillo", 0.5)], t_out=t_camp - 0.1, sale="encoger", z=1)
    # Gran Salto Adelante y hambruna
    R.act(C.horno_patio(), pos=(470, 850, 1.05), t_in=t_salto - 0.5, d_in=0.45, entra="pop", sem=253, sfx=[(0, "pop", 0.6), (0.1, "fuego", 0.4, {"dur": 2.0})], t_out=t_muere - 0.3, sale="encoger")
    R.act(lambda t: C.humo(int(t * 6)), pos=(470, 650, 1.1), t_in=t_salto - 0.3, d_in=0.3, entra="pop", sem=254, peg=False, t_out=t_muere - 0.3, sale="encoger", z=2)
    R.act(C.cuenco_vacio(), pos=(960, 850, 1.1), t_in=t_ham - 0.1, d_in=0.45, entra="pop", sem=255, sfx=[(0, "pop", 0.6), (0.15, "bocinazo", 0.3, {"tono": 0.8})], t_out=t_muere - 0.3, sale="encoger")
    R.act(lambda t: C.trigo(prog(t, t_ham - 0.2, t_ham + 1.6)), pos=(1420, 880, 1.15), t_in=t_ham - 0.3, d_in=0.45, entra="pop", sem=256, t_out=t_muere - 0.3, sale="encoger")
    # muere el líder: se apaga la vela; llega el sucesor y abre la economía; el gato
    R.act(lambda t: C.vela(1.0 - prog(t, t_muere + 0.2, t_muere + 1.0)), pos=(420, 850, 1.3), t_in=t_muere - 0.15, d_in=0.45, entra="pop", sem=257, sfx=[(0, "pop", 0.6), (0.3, "siseo", 0.6, {"dur": 0.8})],
          t_out=t_suc - 0.1, sale="encoger")
    R.act(C.lider_nuevo(0), pos=(1560, 850, 1.0), t_in=t_suc, d_in=0.45, entra="pop", sem=258, sfx=[(0, "pop", 0.6)], t_out=t_cuar - 0.15, sale="encoger")
    R.act(lambda t: A.puerta(e_inout(prog(t, t_abre, t_abre + 0.9))), pos=(1140, 820, 0.78), t_in=t_abre - 0.2, d_in=0.45, entra="pop", sem=259, sfx=[(0, "pop", 0.6), (0.2, "persianas", 0.5)], t_out=t_cuar - 0.15, sale="encoger")
    for nombre, dx, col in (("blanco", 0, "blanco"), ("negro", 230, "negro")):
        R.act(lambda t, col=col: C.gato(col, int(t * 6)), pos=lambda t, dx=dx: (lerp(-260 - dx, 2050, prog(t, t_gato - 0.3, t_rat + 1.3)), 890 + 6 * math.sin(t * 13), 0.62), t_in=t_gato - 0.3, d_in=0.01, entra="fija", sem=260 + dx // 230,
              t_out=t_rat + 1.4, sale="cortar", z=3, sfx=[(0, "pasos", 0.35, {"dur": 2.2})] if dx == 0 else [])
    R.act(lambda t: C.raton(int(t * 8)), pos=lambda t: (lerp(120, 2250, prog(t, t_gato - 0.3, t_rat + 1.3)), 900 + 5 * math.sin(t * 17), 0.6), t_in=t_gato - 0.3, d_in=0.01, entra="fija", sem=263, t_out=t_rat + 1.4,
          sale="cortar", z=3, sfx=[(0.4, "pio", 0.4, {"tono": 1.6}), (1.0, "pio", 0.4, {"tono": 1.8})])
    # crecimiento económico: rascacielos, fábrica y podio
    hs = [260, 340, 420, 300, 380]
    for k in range(5):
        R.act(C.rascacielos(hs[k], 92, [(120, 150, 190), (196, 120, 100), (140, 170, 130), (170, 140, 190), (220, 180, 90)][k]), pos=(330 + 130 * k, 890, 0.85), t_in=t_cientos - 0.3 + 0.17 * k, d_in=0.9,
              entra="pluma", sem=270 + k, sfx=[(0, "crece", 0.4, {"dur": 0.7})], t_out=t_hoy - 0.1, sale="encoger")
    R.act(C.fabrica(), pos=(1250, 880, 0.75), t_in=t_pobr - 0.3, d_in=0.8, entra="pluma", sem=276, sfx=[(0, "crece", 0.4, {"dur": 0.7})], t_out=t_hoy - 0.1, sale="encoger")
    R.act(lambda t: C.humo(int(t * 6)), pos=(1330, 620, 0.8), t_in=t_pobr + 0.5, d_in=0.3, entra="pop", sem=277, peg=False, t_out=t_hoy - 0.1, sale="encoger", z=2)
    R.act(C.podio(), pos=(1560, 880, 0.85), t_in=t_seg - 0.3, d_in=0.45, entra="pop", sem=278, sfx=[(0, "pop", 0.6), (0.15, "bling", 0.6)], t_out=t_hoy - 0.1, sale="encoger")
    R.texto(t_seg, t_hoy - 0.3, "N.º 2", (1560, 680), px=92, d=0.5)
    # hoy: habitantes y trenes
    R.contador(t_hab - 0.3, t_hab + 1.2, 0, 1400000000, (960, 240), px=110)
    R.snd(t_hab, "reloj_rapido", 0.45, dur=1.4)
    Bj = R.rio([(116.4, 39.9), (117.2, 34.3), (119.4, 32.4), (121.5, 31.2)], t_tren - 0.1, 1.3, (250, 242, 232), ancho=12, t1=None)
    Gz = R.rio([(116.4, 39.9), (114.3, 34.8), (114.3, 30.6), (113.3, 23.1)], t_tren + 0.1, 1.4, (250, 242, 232), ancho=12, t1=None)
    Cd = R.rio([(121.5, 31.2), (114.3, 30.6), (108.9, 30.6), (104.1, 30.7)], t_tren + 0.3, 1.4, (250, 242, 232), ancho=12, t1=None)
    for k, Pt in enumerate((Bj, Gz, Cd)):
        R.act(C.tren_bala(), pos_geo=R.camino_pos(Pt, t_tren + 0.6 + 0.25 * k, 2.4, ease=lambda u: u), off=(0, -10), s=0.42, t_in=t_tren + 0.4 + 0.25 * k, d_in=0.3, entra="pop", sem=280 + k,
              sfx=[(0, "tren", 0.5, {"dur": 2.4})], t_out=FIN(e) + 0.6, sale="encoger", zs=0.5, z=1)
    for k, (lon, lat) in enumerate(((116.4, 39.9), (121.5, 31.2), (113.3, 23.1), (104.1, 30.7), (114.3, 30.6))):
        R.act(A.estrella5(30), geo=(lon, lat), off=(0, -18), s=0.8, t_in=t_tren + 0.2 * k, d_in=0.3, entra="pop", sem=285 + k, sfx=[(0, "tick", 0.4, {"tono": 1.0 + 0.1 * k})], t_out=FIN(e) + 0.6, sale="encoger", zs=0.4, z=1)


# ------------------------------------------------------------------ CIERRE
def _cierre(R):
    e = "cierre"
    i0 = INI(e)
    t_rom0, t_unio, t_rom1 = T(e, "rompio", n=0), T(e, "unio"), T(e, "rompio", n=1)
    t_otra, t_sigue, t_tres = T(e, "otra"), T(e, "sigue"), T(e, "tres", frase=0)
    t_pais, t_minutos, t_coment = T(e, "pais"), T(e, "minutos"), T(e, "comentarios")
    R.terreno(i0 - 0.1, "prc", COL["prc"], 0.8)
    R.romper("caudillos", t_rom0 - 0.05, t_rom0 + 0.35, t_rom0 + 0.45, t_unio + 0.25, colores=None, gap=12, deriva=34)
    R.romper("caudillos", t_rom1 - 0.05, t_rom1 + 0.4, t_sigue - 0.5, t_sigue + 0.15, colores=None, gap=16, deriva=46, nervio=1.4)
    R.snd(t_rom0 - 0.05, "crujido", 0.9, dur=0.6)
    R.snd(t_unio, "boing", 0.7)
    R.snd(t_rom1 - 0.05, "crujido", 0.9, dur=0.7)
    R.snd(t_sigue - 0.5, "whoosh", 0.5, dur=0.6, tono=1.2)
    R.snd(t_sigue + 0.1, "gong", 0.6)
    R.camara(i0, 106.0, 35.0, 1.3)
    R.camara(t_sigue, 106.0, 35.5, 1.22)
    R.camara(t_tres, 108.0, 36.0, 1.1)
    R.camara(t_pais, 112.0, 35.0, 0.96)
    R.camara(FIN(e), 112.0, 34.0, 0.92)
    R.anio(t_otra, 2026)
    R.texto(t_tres - 0.1, t_pais - 0.2, "3.000 años", (960, 240), px=120, d=0.8)
    R.snd(t_tres, "escribir", 0.5, dur=0.8)
    paises = [(138.0, 36.5), (127.8, 36.5), (78.5, 22.5), (102.0, 47.0), (100.0, 57.0), (121.0, 14.0), (45.0, 38.0)]
    for k, (lon, lat) in enumerate(paises):
        R.act(A.signo_pregunta(), geo=(lon, lat), off=lambda t, k=k: (0, -16 + 12 * math.sin(t * 4 + k)), s=0.72, t_in=t_pais + 0.14 * k, d_in=0.4, entra="pop", sem=300 + k,
              sfx=[(0, "pluck", 0.5, {"tono": (1.0, 1.125, 1.26, 1.5, 1.68, 2.0, 2.25)[k]})], zs=0.3, z=1)
    R.texto(t_minutos, FIN(e) + 1.0, "¿cuál sigue?", (960, 200), px=112, d=0.9)
    R.act(C.boton_suscribir(), pos=lambda t: (960, 800 + 4 * math.sin(t * 5), 1.0), t_in=t_coment - 0.6, d_in=0.5, entra="pop", sem=310, sfx=[(0, "pop", 0.7), (0.1, "bling", 0.6)], z=2)
    R.texto(t_coment - 0.4, FIN(e) + 1.0, "SUSCRÍBETE", (960, 800), px=76, d=0.7)
    R.act(C.campana(), pos=lambda t: (1270, 790, 0.8, 0.35 * math.sin((t - t_coment) * 9) * math.exp(-(t - t_coment) * 0.4)), t_in=t_coment - 0.3, d_in=0.4, entra="pop", sem=311,
          sfx=[(0, "pop", 0.6), (0.1, "campana", 0.6)], z=2)
    R.act(C.globo_dialogo(), pos=(1470, 520, 1.1), t_in=t_coment - 0.1, d_in=0.45, entra="pop", sem=312, sfx=[(0, "pop", 0.6)], z=2)
    R.texto(t_coment, FIN(e) + 1.0, "...", (1470, 500), px=92, d=0.4)


# ------------------------------------------------------------------ CAMBIOS DE ESCENA (procedurales, sin cortes)
def _transiciones(R):
    ids = ["gancho", "rio", "zhou", "qin", "han", "tang", "song", "yuan", "ming", "qing", "moderna", "cierre"]
    spec = [
        ("tinta", (214, 172, 72), (960, 170), (1000, 620)),
        ("puntos", COL["zhou"], (960, 540), (960, 540)),
        ("pincel", COL["qin"], (960, 540), (960, 540)),
        ("portal", COL["han"], (1560, 780), (1500, 760)),
        ("rollo", COL["tang"], (960, 540), (960, 540)),
        ("papel", COL["song"], (960, 540), (960, 540)),
        ("ola", COL["yuan"], (960, 540), (960, 540)),
        ("portal", COL["ming"], (1300, 800), (820, 800)),
        ("persianas", COL["qing"], (960, 540), (960, 540)),
        ("tinta", (62, 56, 74), (1000, 700), (960, 540)),
        ("ola", (186, 214, 216), (960, 540), (960, 540)),
    ]
    for k, (tipo, color, a, b) in enumerate(spec):
        tc = (FIN(ids[k]) + INI(ids[k + 1])) / 2
        R.trans.append(Transicion(tc, tipo, color, a, b, dur=0.8, seed=k + 1))
        R.snd(tc - 0.36, SFX[tipo], 0.55, dur=0.8) if SFX[tipo] in ("pincel", "zoom_whoosh", "ola") else R.snd(tc - 0.36, SFX[tipo], 0.55)
