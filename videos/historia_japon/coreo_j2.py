# -*- coding: utf-8 -*-
"""Coreografía (2/3): mongoles, guerra civil (Sengoku), unificación, periodo Edo y los barcos negros de Perry."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_j as J
import obj_p as P
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402
from coreo_j1 import lugar

COL = M.COL


def construir(R):
    _mongoles(R)
    _sengoku(R)
    _unificacion(R)
    _edo(R)
    _perry(R)


# ------------------------------------------------------------------ MONGOLES
def _mongoles(R):
    e = "mongoles"
    i0 = INI(e)
    t_1274, t_flota, t_gig, t_china, t_mong, t_kublai = T(e, "doscientos"), T(e, "flota"), T(e, "gigante"), T(e, "china"), T(e, "mongoles"), T(e, "kublai")
    t_sam, t_resis, t_siete, t_regr, t_miles, t_barcos = T(e, "samurais"), T(e, "resisten"), T(e, "siete"), T(e, "regresan"), T(e, "miles"), T(e, "barcos")
    t_pero, t_torm, t_hunde, t_jap, t_kami, t_viento, t_divino = T(e, "pero"), T(e, "tormenta"), T(e, "hunde"), T(e, "japoneses"), T(e, "kamikaze"), T(e, "viento"), T(e, "divino")
    R.camara(i0 - 0.3, 138.0, 35.5, 3.6)
    R.camara(t_1274, 130.5, 34.6, 5.0)
    R.camara(t_flota, 129.6, 34.4, 6.0)
    R.camara(t_sam - 0.2, 130.4, 33.7, 7.6)
    R.camara(t_siete, 130.3, 34.0, 6.6)
    R.camara(t_pero - 0.2, 129.8, 34.2, 6.2)
    R.camara(t_kami, 130.4, 34.0, 6.6)
    R.camara(FIN(e), 131.0, 34.5, 5.0)
    R.anio(i0, 1192)
    R.anio(t_1274 - 0.3, 1192)
    R.anio(t_1274 + 0.8, 1274)
    R.anio(t_siete - 0.1, 1274)
    R.anio(t_siete + 1.0, 1281)
    # flota mongola que cruza desde Corea
    Pm = R.ruta(M.RUTA_MONGOL, t_flota - 0.2, 1.9, ancho=6.0, t1=t_sam + 0.6)
    for k, dy in enumerate((-50, 10, 70)):
        R.act(J.barco_mongol(), pos_geo=R.camino_pos(M.RUTA_MONGOL, t_flota + 0.1 * k, 2.4), off=(-40 * k, dy - 40), s=0.26, t_in=t_flota + 0.1 * k, d_in=0.4, entra="pop", sem=600 + k,
              sfx=[(0, "pop", 0.4)] + ([(0.1, "cuerno", 0.5)] if k == 0 else []), t_out=t_sam + 0.5, sale="encoger", zs=0.7, z=1)
    lugar(R, t_china, t_sam, "CHINA (YUAN)", (128.0, 35.9), off=(0, -90), px=48)
    R.act(Bb.emperador(0, "enojo"), pos=(1560, 800, 0.74), t_in=t_kublai - 0.1, d_in=0.45, entra="pop", sem=603, sfx=[(0, "pop", 0.5)], t_out=t_sam - 0.2, sale="encoger", z=1)
    R.texto(t_kublai - 0.1, t_sam - 0.3, "KUBLAI KAN", (1560, 500), px=66, d=0.8)
    R.snd(t_mong, "tambor", 0.6)
    # los samuráis resisten en la bahía de Hakata
    for k, (dx, dy) in enumerate(((-150, 30), (-50, 70), (50, 20), (150, 60))):
        R.act(lambda t, k=k: J.samurai(int(t * 7) + k, (40, 130), "enojo"), geo=(130.4, 33.6), off=(dx, dy), s=0.4, t_in=t_sam + 0.1 * k, d_in=0.4, entra="pop", sem=604 + k, sfx=[(0, "pop", 0.4), (0.05, "clink", 0.5)],
              zs=0.7, z=1)
    R.act(A.torre_muralla(1.0), geo=(130.4, 33.6), off=(0, -10), s=0.5, t_in=t_resis - 0.2, d_in=0.5, entra="pop", sem=608, sfx=[(0, "golpe_suave", 0.6)], zs=0.7, z=0)
    lugar(R, t_resis - 0.1, t_siete, "HAKATA", (130.4, 33.6), off=(0, -150), px=56)
    # siete años después: miles de barcos
    for k in range(6):
        R.act(J.barco_mongol(), geo=(129.5 - 0.15 * (k % 3), 34.2 + 0.18 * (k // 3)), off=lambda t, k=k: (12 * math.sin(t * 1.5 + k), 6 * math.sin(t * 2 + k)), s=0.2, t_in=t_regr + 0.1 * k, d_in=0.35, entra="pop", sem=609 + k,
              sfx=[(0, "pop", 0.3)] if k % 2 == 0 else [], t_out=t_hunde + 0.3 + 0.1 * k, sale="caer", d_out=0.8, zs=0.7, z=1)
    R.texto(t_miles - 0.1, t_pero - 0.3, "MILES DE BARCOS", (960, 200), px=86, d=0.9)
    R.snd(t_miles, "escribir", 0.5, dur=0.9)
    # tormenta: el viento divino
    R.act(Bb.tormenta(), pos=(960, 330, 1.5), t_in=t_torm - 0.1, d_in=0.5, entra="pop", sem=616, sfx=[(0, "trueno", 0.8), (0.3, "lluvia", 0.5, {"dur": 2.4})], t_out=FIN(e) + 0.3, sale="encoger", z=3)
    R.snd(t_hunde, "chapuzon", 0.7)
    R.snd(t_hunde + 0.3, "crujido", 0.7, dur=0.6)
    R.texto(t_kami - 0.1, FIN(e) + 0.3, "KAMIKAZE = VIENTO DIVINO", (960, 200), px=86, d=1.2)
    R.snd(t_kami, "escribir", 0.5, dur=1.0)
    R.act(J.sol_naciente(), pos=lambda t: (960, 620 + 8 * math.sin(t * 3), 0.9), t_in=t_divino - 0.2, d_in=0.5, entra="pop", sem=617, sfx=[(0, "brillo", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", z=1)


# ------------------------------------------------------------------ SENGOKU
def _sengoku(R):
    e = "sengoku"
    i0 = INI(e)
    t_sin, t_poder, t_deb, t_1467, t_estalla, t_civil = T(e, "sin"), T(e, "poder"), T(e, "debilita"), T(e, "cuatrocientos"), T(e, "estalla"), T(e, "civil")
    t_comienza, t_periodo, t_paises, t_cien, t_senor, t_lucha, t_todos = T(e, "comienza"), T(e, "periodo"), T(e, "paises"), T(e, "cien"), T(e, "senor"), T(e, "lucha"), T(e, "todos")
    t_1543, t_port, t_isla, t_armas, t_fuego = T(e, "quinientos"), T(e, "portugueses"), T(e, "isla"), T(e, "armas"), T(e, "fuego")
    t_jap, t_apr, t_fab, t_pocos = T(e, "japoneses"), T(e, "aprenden"), T(e, "fabricarlas"), T(e, "pocos")
    t_amb, t_oda, t_nob, t_usa, t_aplast, t_enem = T(e, "ambicioso"), T(e, "oda"), T(e, "nobunaga"), T(e, "usa"), T(e, "aplastar"), T(e, "enemigos")
    R.camara(i0 - 0.3, 138.0, 35.5, 3.5)
    R.camara(t_estalla - 0.2, 136.4, 35.4, 3.7)
    R.camara(t_periodo, 136.8, 35.6, 3.2)
    R.camara(t_1543 - 0.3, 131.0, 31.6, 4.6)
    R.camara(t_isla, 131.0, 30.9, 7.4)
    R.camara(t_jap - 0.2, 131.6, 32.0, 5.2)
    R.camara(t_amb - 0.3, 136.9, 35.1, 5.4)
    R.camara(FIN(e), 136.9, 35.1, 5.0)
    R.anio(i0, 1281)
    R.anio(t_1467 - 0.3, 1281)
    R.anio(t_1467 + 0.8, 1467)
    R.anio(t_1543 - 0.3, 1467)
    R.anio(t_1543 + 0.9, 1543)
    # el país se rompe en estados
    colores = [(206, 98, 72), (96, 134, 184), (122, 160, 104), (238, 178, 64), (170, 110, 150), (70, 144, 146), (200, 120, 60), (140, 120, 190)]
    tu = T("unificacion", "unifica")
    R.romper("sengoku", t_estalla - 0.2, t_estalla + 0.7, tu - 0.3, tu + 0.9, colores=colores, gap=20, deriva=38, nervio=1.3)
    R.snd(t_estalla - 0.2, "crujido", 0.9, dur=0.8)
    R.sello(t_periodo + 0.1, "戦", "Sengoku", color=(206, 110, 50))
    for k, (lon, lat) in enumerate(M.CELDAS["sengoku"]):
        R.act(lambda t, k=k: J.samurai(int(t * 8) + k, (40, 130), "enojo", colores[k % len(colores)]), geo=(lon, lat), off=lambda t, k=k: (10 * math.sin(t * 2 + k), 0), s=0.36,
              t_in=t_civil + 0.1 * k, d_in=0.35, entra="pop", sem=620 + k, sfx=[(0, "pop", 0.3)] + ([(0.1, "clink", 0.5)] if k % 2 == 0 else []), zs=0.6, z=1)
    R.texto(t_deb - 0.1, t_periodo - 0.2, "GUERRA CIVIL", (960, 200), px=92, d=0.9)
    R.snd(t_civil, "tambor", 0.7)
    R.texto(t_paises - 0.1, t_1543 - 0.4, "PAÍSES EN GUERRA", (960, 200), px=92, d=0.9)
    R.snd(t_paises, "escribir", 0.5, dur=0.9)
    R.contador(t_cien - 0.3, t_cien + 0.8, 0, 100, (960, 330), px=110, formato="+{} años")
    R.snd(t_cien - 0.2, "reloj_rapido", 0.45, dur=1.0)
    # portugueses llegan a Tanegashima con armas de fuego
    R.ruta(M.RUTA_PORTUGUESES, t_port - 0.3, 2.0, ancho=6.0, t1=t_fab)
    R.act(Bb.carabela(), pos_geo=R.camino_pos(M.RUTA_PORTUGUESES, t_port, 2.4), off=(0, -30), s=0.38, t_in=t_port, d_in=0.4, entra="pop", sem=630, sfx=[(0, "pop", 0.5), (0.1, "ola", 0.4, {"dur": 2.0})],
          t_out=t_armas + 0.6, sale="encoger", zs=0.7, z=1)
    lugar(R, t_isla - 0.1, t_fab, "TANEGASHIMA", (131.0, 30.6), off=(0, -130), px=54)
    R.act(J.ashigaru(0, "feliz"), geo=(131.0, 30.6), off=(-60, 50), s=0.6, t_in=t_armas - 0.1, d_in=0.45, entra="pop", sem=631, sfx=[(0, "pop", 0.5)], zs=0.7, z=1)
    R.act(A.estallido(14, 30, 90), geo=(131.0, 30.6), off=(120, -60), s=0.7, t_in=t_fuego, d_in=0.12, entra="fija", sem=632,
          sfx=[(0, "canonazo", 0.7)], t_out=t_fuego + 0.4, sale="cortar", zs=0.7, z=3)
    R.texto(t_armas - 0.1, t_jap - 0.3, "ARMAS DE FUEGO", (960, 200), px=90, d=0.9)
    R.snd(t_armas, "escribir", 0.5, dur=0.9)
    # los japoneses aprenden a fabricarlas
    for k, (dx, dy) in enumerate(((-200, 40), (-70, 70), (60, 30), (190, 60))):
        R.act(lambda t, k=k: J.ashigaru(int(t * 6) + k, "enojo"), geo=(131.6, 32.0), off=(dx, dy), s=0.5, t_in=t_apr + 0.14 * k, d_in=0.4, entra="pop", sem=633 + k,
              sfx=[(0, "pop", 0.4), (0.2, "canonazo", 0.35)], zs=0.7, z=1)
    R.contador(t_pocos - 0.3, t_pocos + 0.9, 0, 40, (960, 330), px=104, formato="{} armeros")
    # Oda Nobunaga aplasta a sus enemigos
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "enojo", (200, 50, 50)), geo=(136.9, 35.18), off=(0, 60), s=0.9, t_in=t_nob - 0.2, d_in=0.45, entra="pop", sem=640,
          sfx=[(0, "pop", 0.6), (0.1, "tambor", 0.6)], zs=0.6, z=2)
    lugar(R, t_oda, t_aplast, "ODA NOBUNAGA", (136.9, 35.18), off=(0, -250), px=66)
    for k, (dx, dy) in enumerate(((-300, 50), (-210, 90), (300, 50), (220, 90))):
        R.act(lambda t, k=k: J.ashigaru(int(t * 6) + k, "enojo"), geo=(136.9, 35.18), off=(dx, dy), s=0.5, t_in=t_usa + 0.1 * k, d_in=0.4, entra="pop", sem=641 + k,
              sfx=[(0, "pop", 0.4), (0.15, "canonazo", 0.5)], zs=0.6, z=1)
    for k, (dx, dy) in enumerate(((-520, 70), (520, 70))):
        R.act(persona((150, 120, 100), PIEL, "casco", "miedo", (60, 60), k, traje="armadura"), geo=(136.9, 35.18), off=(dx, dy), s=0.5, t_in=t_aplast + 0.15 * k, d_in=0.4, entra="pop", sem=645 + k,
              sfx=[(0, "pop", 0.4)], t_out=t_enem + 0.3, sale="caer", d_out=0.8, zs=0.6, z=1)


# ------------------------------------------------------------------ UNIFICACIÓN
def _unificacion(R):
    e = "unificacion"
    i0 = INI(e)
    t_nob, t_muere, t_trai, t_gen, t_hide, t_camp, t_alto, t_cont = T(e, "nobunaga"), T(e, "muere"), T(e, "traicionado"), T(e, "general"), T(e, "hideyoshi"), T(e, "campesino"), T(e, "alto"), T(e, "continua")
    t_unif, t_pais, t_pero, t_muerte, t_rival, t_pelear = T(e, "unifica"), T(e, "pais"), T(e, "pero"), T(e, "muerte"), T(e, "rivales"), T(e, "pelear")
    t_1600, t_bat, t_seki, t_triun, t_toku, t_ieya = T(e, "seiscientos"), T(e, "batalla"), T(e, "sekigahara"), T(e, "triunfa"), T(e, "tokugawa"), T(e, "ieyasu")
    t_tres, t_shog, t_funda, t_cap, t_aldea, t_pesc, t_edo = T(e, "tres"), T(e, "shogun"), T(e, "funda"), T(e, "capital"), T(e, "aldea"), T(e, "pescadores"), T(e, "edo")
    t_hoy, t_lugar, t_llama, t_tokio = T(e, "hoy"), T(e, "lugar"), T(e, "llama"), T(e, "tokio")
    R.terreno(t_unif - 0.2, "sin_hokkaido", COL["sengoku"], 1.4)
    R.terreno(t_toku - 0.1, "sin_hokkaido", COL["tokugawa"], 1.4)
    R.sello(t_shog + 0.15, "江", "Edo", color=(52, 110, 170))
    R.camara(i0 - 0.3, 136.9, 35.1, 5.0)
    R.camara(t_muere - 0.2, 135.76, 35.01, 8.0)
    R.camara(t_hide - 0.2, 136.0, 34.9, 5.4)
    R.camara(t_unif - 0.2, 135.5, 34.8, 4.4)
    R.camara(t_pero, 136.0, 35.2, 4.0)
    R.camara(t_seki - 0.3, 136.46, 35.36, 8.0)
    R.camara(t_tres - 0.2, 139.69, 35.69, 7.4)
    R.camara(t_aldea, 139.69, 35.69, 9.0)
    R.camara(t_tokio - 0.3, 139.69, 35.69, 7.0)
    R.camara(FIN(e), 139.69, 35.69, 6.0)
    R.anio(i0, 1543)
    R.anio(t_muere - 0.2, 1543)
    R.anio(t_muere + 0.6, 1582)
    R.anio(t_1600 - 0.3, 1582)
    R.anio(t_1600 + 0.8, 1600)
    R.anio(t_tres - 0.2, 1600)
    R.anio(t_tres + 1.0, 1603)
    R.anio(t_hoy, 1603)
    R.anio(t_hoy + 1.2, 2026)
    # Nobunaga traicionado (el templo arde)
    R.act(J.templo(), geo=(135.76, 35.01), off=(0, 60), s=0.9, t_in=t_nob - 0.4, d_in=0.5, entra="pop", sem=650, sfx=[(0, "pop", 0.5)], zs=0.7, z=0, t_out=t_hide - 0.2, sale="encoger")
    for k, dx in enumerate((-90, 0, 90)):
        R.act(lambda t, k=k: A.llama(int(t * 9) + k), geo=(135.76, 35.01), off=(dx, -30), s=0.9, t_in=t_muere + 0.1 * k, d_in=0.3, entra="pop", sem=651 + k, z=3, zs=0.7, t_out=t_hide - 0.2, sale="encoger",
              sfx=[(0, "fuego", 0.5, {"dur": 2.4})] if k == 1 else [])
    R.act(lambda t: J.samurai(0, (20, 20), "miedo", (200, 50, 50)), geo=(135.76, 35.01), off=(-260, 70), s=0.8, t_in=t_nob - 0.1, d_in=0.45, entra="pop", sem=654, sfx=[(0, "pop", 0.5)],
          t_out=t_trai + 0.4, sale="caer", d_out=0.8, zs=0.7, z=1)
    lugar(R, t_trai - 0.1, t_gen, "¡TRAICIÓN!", (135.76, 35.01), off=(0, -300), px=84)
    R.snd(t_trai, "impacto", 0.7)
    # Hideyoshi, el campesino que llegó a lo más alto
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "feliz", (214, 160, 50)), pos=(1400, 800, 1.05), t_in=t_hide - 0.1, d_in=0.45, entra="pop", sem=655, sfx=[(0, "pop", 0.6)], t_out=t_unif - 0.1, sale="encoger", z=1)
    R.act(J.campesino_jp(0), pos=(620, 850, 0.8), t_in=t_camp - 0.1, d_in=0.45, entra="pop", sem=656, sfx=[(0, "pop", 0.5)], t_out=t_unif - 0.1, sale="encoger", z=1)
    Pup = [(620, 850), (1000, 780), (1400, 800)]
    R.texto(t_hide - 0.1, t_unif - 0.2, "HIDEYOSHI", (1400, 470), px=74, d=0.8)
    R.texto(t_camp - 0.1, t_unif - 0.2, "CAMPESINO", (620, 560), px=58, d=0.7)
    for k in range(4):
        R.act(A.estrella5(30), pos=lambda t, k=k: (800 + 130 * k, 640 - 50 * k + 6 * math.sin(t * 4 + k), 1.0), t_in=t_alto + 0.12 * k, d_in=0.35, entra="pop", sem=657 + k,
              sfx=[(0, "pluck", 0.5, {"tono": 1.0 + 0.2 * k})], t_out=t_unif - 0.1, sale="encoger", z=2)
    # unifica casi todo el país, pero vuelven los rivales
    R.snd(t_unif, "whoosh", 0.6, dur=0.8)
    R.texto(t_unif - 0.1, t_pero - 0.2, "JAPÓN UNIFICADO", (960, 200), px=92, d=1.0)
    R.snd(t_unif + 0.05, "escribir", 0.5, dur=1.0)
    R.act(A.espadas(), pos=(960, 700, 1.1), t_in=t_rival - 0.2, d_in=0.4, entra="pop", sem=661, sfx=[(0, "impacto", 0.6)], t_out=t_1600 - 0.1, sale="encoger", z=2)
    # Sekigahara
    R.ruta(M.RUTA_SEKIGAHARA, t_seki - 0.4, 1.6, ancho=6.0, t1=t_tres - 0.2)
    lugar(R, t_seki - 0.1, t_tres - 0.3, "SEKIGAHARA", (136.46, 35.36), off=(0, -200), px=62)
    for k, (dx, dy, col) in enumerate(((-260, 40, (60, 100, 160)), (-160, 90, (60, 100, 160)), (260, 40, (60, 140, 90)), (160, 90, (60, 140, 90)))):
        R.act(lambda t, k=k, col=col: J.samurai(int(t * 7) + k, (40, 130), "enojo", col), geo=(136.46, 35.36), off=(dx, dy), s=0.5, t_in=t_bat + 0.1 * k, d_in=0.4, entra="pop", sem=662 + k,
              sfx=[(0, "pop", 0.4), (0.1, "clink", 0.5)], t_out=t_triun + 0.6 if k < 2 else t_tres - 0.2, sale="caer" if k < 2 else "encoger", d_out=0.7, zs=0.7, z=1)
    R.act(lambda t: J.samurai(int(t * 6), (14, 130), "feliz", (60, 140, 90)), geo=(136.46, 35.36), off=(0, 60), s=0.85, t_in=t_triun - 0.1, d_in=0.45, entra="pop", sem=666,
          sfx=[(0, "pop", 0.6), (0.1, "bling", 0.6)], t_out=t_tres - 0.2, sale="encoger", zs=0.7, z=2)
    lugar(R, t_toku, t_tres - 0.3, "TOKUGAWA IEYASU", (136.46, 35.36), off=(0, -330), px=62)
    R.snd(t_bat, "tambor", 0.6)
    R.snd(t_triun, "gong", 0.6)
    # Edo, aldea de pescadores
    for k, dx in enumerate((-160, -40, 90, 200)):
        R.act(A.casa(), geo=(139.69, 35.69), off=(dx, 30 + 8 * (k % 2)), s=0.55, t_in=t_aldea + 0.1 * k, d_in=0.4, entra="pop", sem=667 + k, sfx=[(0, "pop", 0.4)], zs=0.8, z=0)
    lugar(R, t_funda, t_tokio - 0.3, "EDO", (139.69, 35.69), off=(0, -170), px=92)
    R.act(J.castillo(), geo=(139.75, 35.68), off=(0, 40), s=0.9, t_in=t_cap, d_in=0.7, entra="pluma", sem=672, sfx=[(0, "crece", 0.6, {"dur": 0.7})], zs=0.8, z=1)
    # hoy: Tokio
    R.act(C.rascacielos(300, 90, (120, 150, 190)), geo=(139.69, 35.69), off=(-240, 40), s=0.8, t_in=t_tokio - 0.1, d_in=0.45, entra="pop", sem=673, sfx=[(0, "pop", 0.5)], zs=0.8, z=1)
    R.act(C.rascacielos(380, 100, (150, 130, 190)), geo=(139.69, 35.69), off=(250, 40), s=0.8, t_in=t_tokio, d_in=0.45, entra="pop", sem=674, sfx=[(0, "pop", 0.5)], zs=0.8, z=1)
    R.texto(t_tokio - 0.1, FIN(e) + 0.3, "TOKIO", (960, 200), px=128, d=0.7)
    R.snd(t_tokio, "escribir", 0.5, dur=0.7)


# ------------------------------------------------------------------ EDO
def _edo(R):
    e = "edo"
    i0 = INI(e)
    t_toku, t_gob, t_dos, t_cinc, t_anos, t_paz = T(e, "tokugawa"), T(e, "gobiernan"), T(e, "doscientos"), T(e, "cincuenta"), T(e, "anos"), T(e, "paz")
    t_sam, t_dejan, t_guerra, t_conv, t_func, t_flor, t_teat, t_kab, t_grab, t_art = T(e, "samurais"), T(e, "dejan"), T(e, "guerra"), T(e, "convierten"), T(e, "funcionarios"), T(e, "florecen"), T(e, "teatro"), T(e, "kabuki"), T(e, "grabados"), T(e, "artistas")
    t_pero, t_temen, t_europ, t_mis, t_traig, t_probl = T(e, "pero"), T(e, "temen"), T(e, "europeos"), T(e, "misioneros"), T(e, "traigan"), T(e, "problemas")
    t_asi, t_jap, t_cierra, t_puertas, t_expulsa, t_extr, t_prohibe, t_salir = T(e, "asi"), T(e, "japon"), T(e, "cierra"), T(e, "puertas"), T(e, "expulsa"), T(e, "extranjeros"), T(e, "prohibe"), T(e, "salir")
    t_solo, t_pocos, t_comer, t_hol, t_chinos, t_entrar, t_isla, t_art2 = T(e, "solo"), T(e, "pocos"), T(e, "comerciantes"), T(e, "holandeses"), T(e, "chinos"), T(e, "entrar"), T(e, "isla"), T(e, "artificial")
    R.camara(i0 - 0.3, 139.69, 35.69, 6.0)
    R.camara(t_gob, 138.0, 35.8, 3.6)
    R.camara(t_sam - 0.2, 136.6, 35.2, 4.0)
    R.camara(t_pero - 0.2, 135.5, 34.6, 3.6)
    R.camara(t_asi - 0.2, 136.0, 35.0, 3.0)
    R.camara(t_solo - 0.3, 129.87, 32.75, 6.0)
    R.camara(t_isla, 129.87, 32.75, 10.0)
    R.camara(FIN(e), 130.0, 33.0, 8.0)
    R.anio(i0, 1603)
    R.anio(t_paz + 0.5, 1868)
    R.anio(t_pero - 0.2, 1868)
    R.anio(t_pero + 0.6, 1635)
    R.anio(t_solo - 0.3, 1635)
    # 250 años de paz
    R.contador(t_dos - 0.3, t_anos + 0.3, 0, 250, (960, 330), px=120, formato="{} años")
    R.snd(t_dos - 0.2, "reloj_rapido", 0.45, dur=1.2)
    R.act(J.samurai_paz(0, "feliz"), pos=(1400, 810, 1.0), t_in=t_paz - 0.2, d_in=0.45, entra="pop", sem=680, sfx=[(0, "pop", 0.5)], t_out=t_sam - 0.2, sale="encoger", z=1)
    R.act(J.cerezo(0), pos=(520, 830, 0.9), t_in=t_paz - 0.1, d_in=0.6, entra="pluma", sem=681, sfx=[(0, "brillo", 0.5)], t_out=t_sam - 0.2, sale="encoger", z=1)
    R.texto(t_paz - 0.1, t_sam - 0.3, "PAZ", (960, 200), px=140, d=0.6)
    R.snd(t_paz, "campana", 0.5)
    # los samuráis dejan la guerra y se vuelven funcionarios; florece el arte
    R.act(lambda t: J.samurai_paz(int(t * 2), "normal"), pos=(560, 810, 1.0), t_in=t_sam - 0.1, d_in=0.45, entra="pop", sem=682, sfx=[(0, "pop", 0.5)], t_out=t_pero - 0.2, sale="encoger", z=1)
    R.act(A.espadas(), pos=lambda t: (560 + 200 * prog(t, t_dejan, t_dejan + 0.8), 560 + 420 * e_in(prog(t, t_dejan, t_dejan + 0.8)), 0.6, 1.4 * prog(t, t_dejan, t_dejan + 0.8)), t_in=t_sam, d_in=0.3, entra="pop", sem=683,
          t_out=t_conv, sale="cortar", z=2)
    R.act(A.papel_hoja(), pos=(760, 780, 1.0), t_in=t_func - 0.1, d_in=0.45, entra="pop", sem=684, sfx=[(0, "papel", 0.5)], t_out=t_pero - 0.2, sale="encoger", z=2)
    R.texto(t_func - 0.1, t_pero - 0.3, "FUNCIONARIOS", (560, 450), px=64, d=0.8)
    R.act(J.mascara_kabuki(), pos=lambda t: (1100, 640 + 6 * math.sin(t * 3), 1.3), t_in=t_kab - 0.2, d_in=0.45, entra="pop", sem=685, sfx=[(0, "pop", 0.6), (0.1, "tambor", 0.5)], t_out=t_pero - 0.2, sale="encoger", z=1)
    R.act(J.gran_ola(), pos=(1500, 830, 1.05), t_in=t_grab - 0.1, d_in=0.5, entra="pop", sem=686, sfx=[(0, "ola", 0.5, {"dur": 1.0})], t_out=t_pero - 0.2, sale="encoger", z=1)
    R.texto(t_kab - 0.1, t_pero - 0.3, "KABUKI", (1100, 380), px=64, d=0.7)
    R.texto(t_grab - 0.1, t_pero - 0.3, "GRABADOS", (1500, 470), px=64, d=0.7)
    # temen a los europeos y a sus misioneros
    R.act(Bb.carabela(), pos=lambda t: (lerp(2050, 1450, e_out(prog(t, t_europ - 0.3, t_europ + 1.2))), 830, 0.52), t_in=t_europ - 0.3, d_in=0.3, entra="fija", sem=687, sfx=[(0, "cuerno", 0.4)], t_out=t_asi - 0.3, sale="der_fuera", d_out=0.7, z=1)
    R.act(J.sacerdote(0), pos=(1100, 810, 0.95), t_in=t_mis - 0.1, d_in=0.45, entra="pop", sem=688, sfx=[(0, "pop", 0.5)], t_out=t_asi - 0.3, sale="encoger", z=1)
    R.act(J.samurai(0, (14, 130), "miedo"), pos=(520, 810, 1.0), t_in=t_temen - 0.1, d_in=0.45, entra="pop", sem=689, sfx=[(0, "pop", 0.5), (0.2, "hmm", 0.4)], t_out=t_asi - 0.3, sale="encoger", z=1)
    R.texto(t_temen - 0.1, t_asi - 0.3, "¿PROBLEMAS?", (960, 200), px=100, d=0.8)
    R.snd(t_probl, "error", 0.4)
    # cierra sus puertas: expulsa a los extranjeros
    R.act(lambda t: Bb.gran_puerta_cerrada(round(kf(t, [(t_cierra - 0.2, 0.0), (t_puertas + 0.6, 1.0)]), 1)), pos=(960, 780, 1.4), t_in=t_cierra - 0.2, d_in=0.45, entra="pop", sem=690,
          sfx=[(0, "pop", 0.5), (0.7, "golpe_suave", 0.7)], t_out=t_solo - 0.2, sale="encoger", z=2)
    R.texto(t_jap - 0.1, t_solo - 0.3, "JAPÓN CERRADO", (960, 200), px=100, d=0.9)
    R.snd(t_jap, "escribir", 0.5, dur=0.9)
    R.snd(t_puertas + 0.2, "crujido", 0.8, dur=0.7)
    # Dejima: la isla artificial
    lugar(R, t_solo, FIN(e) + 0.3, "DEJIMA", (129.87, 32.75), off=(0, -170), px=84)
    R.act(C.isla_trozo(60), geo=(129.87, 32.75), off=(0, 40), s=1.1, t_in=t_isla - 0.3, d_in=0.6, entra="pop", sem=691, sfx=[(0, "pop", 0.6)], zs=0.9, z=0)
    R.act(Bb.junco(1.0, 2), geo=(129.87, 32.75), off=(-260, 70), s=0.42, t_in=t_chinos - 0.1, d_in=0.45, entra="pop", sem=692, sfx=[(0, "pop", 0.5), (0.1, "ola", 0.4, {"dur": 1.4})], zs=0.9, z=1)
    R.act(Bb.carabela(), geo=(129.87, 32.75), off=(270, 70), s=0.4, t_in=t_hol - 0.1, d_in=0.45, entra="pop", sem=693, sfx=[(0, "pop", 0.5)], zs=0.9, z=1, flip=True)
    R.act(J.comerciante(0), geo=(129.87, 32.75), off=(0, 20), s=0.6, t_in=t_comer - 0.1, d_in=0.45, entra="pop", sem=694, sfx=[(0, "pop", 0.5)], zs=0.9, z=2)


# ------------------------------------------------------------------ PERRY
def _perry(R):
    e = "perry"
    i0 = INI(e)
    t_hasta, t_1853, t_apar, t_bahia, t_cuatro, t_buques, t_negros, t_canon = T(e, "hasta"), T(e, "ochocientos"), T(e, "aparecen"), T(e, "bahia"), T(e, "cuatro"), T(e, "buques"), T(e, "negros"), T(e, "canones")
    t_son, t_eeuu, t_como, t_exige, t_abrir, t_comercio = T(e, "son"), T(e, "estados"), T(e, "comodoro"), T(e, "exige"), T(e, "abrir"), T(e, "comercio")
    t_sam, t_pueden, t_compet, t_canv, t_vapor, t_shog, t_cede = T(e, "samurais"), T(e, "pueden"), T(e, "competir"), T(e, "canones", frase=2), T(e, "vapor"), T(e, "shogun", frase=2), T(e, "cede")
    t_mucho, t_indig, t_idea, t_ext, t_shog2, t_fall, t_emp, t_volver, t_gobern = T(e, "muchos"), T(e, "indignan"), T(e, "idea"), T(e, "extiende"), T(e, "shogun", frase=3), T(e, "fallado"), T(e, "emperador"), T(e, "volver"), T(e, "gobernar")
    R.camara(i0 - 0.3, 130.0, 33.0, 6.0)
    R.camara(t_hasta - 0.2, 141.0, 34.5, 4.2)
    R.camara(t_bahia, 139.72, 35.2, 8.0)
    R.camara(t_cuatro, 139.8, 35.1, 8.6)
    R.camara(t_son - 0.2, 139.7, 35.3, 8.6)
    R.camara(t_sam - 0.2, 139.7, 35.5, 7.6)
    R.camara(t_mucho - 0.3, 137.5, 35.5, 3.9)
    R.camara(t_emp - 0.3, 136.5, 35.3, 4.2)
    R.camara(FIN(e), 137.0, 35.5, 3.8)
    R.anio(i0, 1635)
    R.anio(t_1853 - 0.3, 1635)
    R.anio(t_1853 + 0.9, 1853)
    # cuatro buques negros en la bahía de Edo
    Pp = R.ruta(M.RUTA_PERRY, t_apar - 0.3, 2.4, ancho=6.0, t1=t_sam)
    for k in range(4):
        R.act(lambda t, k=k: J.barco_negro(int(t * 8) + k), pos_geo=R.camino_pos(M.RUTA_PERRY, t_apar + 0.18 * k, 2.6), off=(-50 * k, 30 - 18 * k), s=0.3, t_in=t_apar + 0.18 * k, d_in=0.4, entra="pop", sem=700 + k,
              sfx=[(0, "pop", 0.4)] + ([(0.1, "cuerno", 0.6), (0.3, "ola", 0.4, {"dur": 2.4})] if k == 0 else []), t_out=t_sam + 1.0, sale="encoger", zs=0.7, z=1)
    R.contador(t_cuatro - 0.3, t_cuatro + 0.5, 0, 4, (960, 300), px=130, formato="{} buques")
    R.texto(t_negros - 0.1, t_sam - 0.3, "BARCOS NEGROS", (960, 190), px=96, d=0.8)
    R.snd(t_negros, "escribir", 0.5, dur=0.8)
    R.snd(t_canon, "canonazo", 0.8)
    R.act(A.estallido(14, 40, 120), geo=(139.72, 35.05), off=(120, -90), s=0.8, t_in=t_canon + 0.1, d_in=0.12, entra="fija", sem=704, sfx=[(0, "explosion", 0.6)], t_out=t_canon + 0.5, sale="cortar", zs=0.7, z=3)
    lugar(R, t_bahia, t_sam - 0.3, "BAHÍA DE EDO", (139.72, 35.25), off=(0, -220), px=56)
    # el comodoro estadounidense exige abrir el país
    R.act(J.marino_yanqui(0), pos=(520, 810, 1.0), t_in=t_como - 0.1, d_in=0.45, entra="pop", sem=705, sfx=[(0, "pop", 0.6)], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.texto(t_eeuu - 0.1, t_sam - 0.3, "ESTADOS UNIDOS", (520, 450), px=62, d=0.8)
    R.act(Bb.gran_puerta_cerrada(0.0), pos=(1400, 790, 1.2), t_in=t_abrir - 0.2, d_in=0.45, entra="pop", sem=706, sfx=[(0, "pop", 0.5), (0.2, "crujido", 0.6)], t_out=t_sam - 0.3, sale="encoger", z=1)
    R.act(C.caja_te(), pos=(1130, 850, 0.8), t_in=t_comercio - 0.1, d_in=0.4, entra="pop", sem=707, sfx=[(0, "monedas", 0.5)], t_out=t_sam - 0.3, sale="encoger", z=1)
    # los samuráis no pueden competir con los cañones
    R.act(J.samurai(0, (40, 130), "miedo"), pos=(560, 810, 1.0), t_in=t_sam - 0.1, d_in=0.45, entra="pop", sem=708, sfx=[(0, "pop", 0.5)], t_out=t_mucho - 0.2, sale="encoger", z=1)
    R.act(C.canon(0.0), pos=(1400, 830, 1.2), t_in=t_canv - 0.2, d_in=0.45, entra="pop", sem=709, sfx=[(0, "pop", 0.5), (0.3, "canonazo", 0.7)], t_out=t_mucho - 0.2, sale="encoger", z=1)
    R.act(J.barco_negro(0), pos=(1330, 600, 0.45), t_in=t_vapor - 0.1, d_in=0.45, entra="pop", sem=710, sfx=[(0, "pop", 0.4)], t_out=t_mucho - 0.2, sale="encoger", z=1)
    R.texto(t_sam - 0.1, t_shog - 0.2, "¿ESPADAS CONTRA CAÑONES?", (960, 200), px=74, d=1.1)
    R.act(J.samurai(0, (20, 20), "lloron", (60, 100, 160)), pos=(960, 810, 1.0), t_in=t_shog - 0.1, d_in=0.45, entra="pop", sem=711, sfx=[(0, "pop", 0.5), (0.3, "suspiro", 0.5)], t_out=t_mucho - 0.2, sale="encoger", z=2)
    R.act(A.rollo_escritura(1), pos=lambda t: (960, 560 - 40 * math.sin(math.pi * prog(t, t_cede, t_cede + 0.9)), 1.1), t_in=t_cede - 0.1, d_in=0.4, entra="pop", sem=712, sfx=[(0, "papel", 0.5)], t_out=t_mucho - 0.2, sale="encoger", z=2)
    # la indignación y la idea: que vuelva el emperador
    R.terreno(t_mucho - 0.2, "sin_hokkaido", COL["tokugawa"], 0.6)
    for k, (lon, lat) in enumerate(((139.7, 35.7), (136.0, 35.0), (133.0, 34.4), (131.0, 33.6), (140.7, 38.3))):
        R.act(J.samurai_paz(int(k), "enojo"), geo=(lon, lat), off=(0, 40), s=0.42, t_in=t_indig + 0.1 * k, d_in=0.4, entra="pop", sem=713 + k, sfx=[(0, "pop", 0.4)], t_out=t_emp + 0.1, sale="encoger", zs=0.6, z=1)
    R.act(A.estallido(12, 30, 80), geo=(139.7, 35.7), off=(0, -90), s=0.7, t_in=t_indig, d_in=0.12, entra="fija", sem=718, sfx=[(0, "impacto", 0.6)], t_out=t_indig + 0.4, sale="cortar", zs=0.6, z=3)
    R.texto(t_idea - 0.1, t_shog2, "UNA IDEA...", (960, 200), px=104, d=0.7)
    R.snd(t_idea, "escribir", 0.5, dur=0.7)
    R.act(A.signo_pregunta(), pos=lambda t: (960, 650 + 10 * math.sin(t * 4), 1.0), t_in=t_fall - 0.2, d_in=0.4, entra="pop", sem=719, sfx=[(0, "error", 0.5)], t_out=t_emp - 0.1, sale="encoger", z=2)
    R.act(J.samurai(0, (20, 20), "lloron", (60, 100, 160)), pos=(520, 800, 0.85), t_in=t_shog2, d_in=0.4, entra="pop", sem=720, sfx=[(0, "pop", 0.4)], t_out=t_volver, sale="baja", d_out=0.8, z=1)
    R.act(J.emperador_jp(0, "feliz"), pos=(1400, 800, 1.0), t_in=t_emp - 0.1, d_in=0.5, entra="sube", sem=721, sfx=[(0, "pop", 0.5), (0.1, "brillo", 0.6)], z=1)
    R.act(J.sol_naciente(), pos=lambda t: (1400, 520 + 6 * math.sin(t * 3), 0.85), t_in=t_volver - 0.2, d_in=0.5, entra="pop", sem=722, sfx=[(0, "brillo", 0.6)], z=0)
    R.texto(t_gobern - 0.2, FIN(e) + 0.3, "¡VUELVE EL EMPERADOR!", (960, 200), px=82, d=1.0)
    R.snd(t_gobern, "escribir", 0.5, dur=0.9)
