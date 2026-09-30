# -*- coding: utf-8 -*-
"""Coreografía (1/3): gancho, meseta (Elam, qanats, medos y persas), Ciro y Darío."""
import math

import numpy as np

import mapa as M
import obj_a as A
import obj_b as Bb
import obj_c as C
import obj_p as P
from motor import e_back, e_in, e_inout, e_out, lerp, prog
from obj_base import *  # noqa: F401,F403
from core import INI, FIN, T, kf  # noqa: E402  (después del * para que T sea el tiempo, no el trazo)

COL = M.COL
PURPURA = P.PURPURA


def pop(R, dib, t, pos=None, geo=None, off=(0, 0), s=1.0, snd="pop", vol=0.6, **k):
    sfx = [(0.0, snd, vol)] if snd else []
    if pos is not None:
        return R.act(dib, pos=pos, t_in=t, sfx=sfx, **k)
    return R.act(dib, geo=geo, off=off, s=s, t_in=t, sfx=sfx, **k)


def campo_extra(R, nombre, color, t0, t1=None, d=0.9, alfa=1.0):
    """Pinta otro campo (p. ej. un segundo pueblo) encima del territorio principal, con fundido de entrada y salida."""
    def f(img, cam, t, fs):
        if t < t0:
            return
        a = alfa * prog(t, t0, t0 + d)
        if t1 is not None:
            a *= 1 - prog(t, t1, t1 + 0.6)
        if a > 0.01:
            M.pintar(img, cam.proyectar(M.CAMPOS[nombre]), color, a, fs)
    R.fondo.append(R._acot(f, t0))


def lugar(R, t0, t1, txt, geo, off=(0, -60), px=54, d=0.5):
    return R.texto(t0, t1, txt, None, px=px, d=d, geo=geo, off=off)


def construir(R):
    _gancho(R)
    _meseta(R)
    _ciro(R)
    _dario(R)


# ------------------------------------------------------------------ GANCHO
def _gancho(R):
    e = "gancho"
    t_hace, t_imperio, t_egipto, t_india = T(e, "hace"), T(e, "imperio"), T(e, "egipto"), T(e, "india")
    t_cayo, t_renacio, t_muchas, t_jamas = T(e, "cayo"), T(e, "renacio"), T(e, "muchas"), T(e, "jamas")
    t_historia, t_iran, t_cinco, t_min = T(e, "historia"), T(e, "iran"), T(e, "cinco"), T(e, "minutos")
    R.camara(0.0, 47.5, 31.0, 1.4)
    R.camara(t_cayo, 47.5, 31.0, 1.46)
    R.camara(t_jamas - 0.3, 49.0, 31.5, 1.5)
    R.camara(t_iran, 53.0, 32.4, 1.95)
    R.camara(t_min + 0.4, 53.5, 32.6, 2.0)
    R.anio(t_hace - 0.3, -500)
    R.anio(t_hace + 1.2, -500)
    R.terreno(t_imperio - 0.1, "dario", COL["aquemenida"], 1.4)
    R.snd(t_imperio, "brillo", 0.5)
    lugar(R, t_egipto - 0.05, t_cayo - 0.1, "EGIPTO", (30.5, 27.8), off=(0, 0), px=58)
    lugar(R, t_india - 0.05, t_cayo - 0.1, "INDIA", (73.0, 29.8), off=(0, 0), px=58)
    R.snd(t_egipto, "escribir", 0.5, dur=0.6)
    R.snd(t_india, "escribir", 0.5, dur=0.6)
    # caravana de jinetes de un extremo al otro
    Pr = R.ruta([(31.0, 29.5), (38.0, 35.0), (48.3, 32.3), (60.0, 32.0), (72.0, 30.0)], t_imperio + 0.3, 2.6, ancho=5.0, t1=t_cayo - 0.3)
    for k in range(2):
        R.act(lambda t, k=k: Bb.jinete(int(t * 7) + k, PURPURA if k == 0 else ROJO_OSC, "gorro", False, False, "feliz"),
              pos_geo=R.camino_pos(Pr, t_imperio + 0.5 + 0.5 * k, 2.6, ease=lambda u: u), off=(0, -18), s=0.26, t_in=t_imperio + 0.4 + 0.5 * k, d_in=0.3, entra="pop", sem=2 + k,
              sfx=[(0, "galope", 0.4, {"dur": 2.4})] if k == 0 else [], t_out=t_cayo - 0.1, sale="encoger", zs=0.6, z=1)
    # cae: el imperio se rompe en pedazos y se reúne; vuelve a romperse; al final queda la forma actual de Irán
    R.romper("gancho", t_cayo - 0.05, t_cayo + 0.45, t_cayo + 0.8, t_renacio + 0.45, colores=None, gap=12, deriva=34)
    R.romper("gancho", t_muchas - 0.12, t_muchas + 0.45, t_jamas - 0.45, t_jamas + 0.2, colores=None, gap=14, deriva=48, nervio=1.5)
    R.snd(t_cayo - 0.05, "crujido", 0.9, dur=0.7)
    R.snd(t_cayo + 0.8, "whoosh", 0.5, dur=0.7, tono=1.2)
    R.snd(t_renacio + 0.3, "boing", 0.7)
    R.snd(t_muchas - 0.12, "crujido", 0.95, dur=0.9)
    R.snd(t_jamas - 0.3, "whoosh", 0.5, dur=0.8, tono=1.2)
    R.snd(t_jamas + 0.2, "ding", 0.6)
    R.terreno(t_jamas, "iran", COL["iran"], 1.3)
    # título y cronómetro
    R.texto(t_historia - 0.05, FIN(e) + 1.0, "LA HISTORIA DE IRÁN", (960, 150), px=118, d=0.9)
    R.texto(t_cinco - 0.05, FIN(e) + 1.0, "en 5 minutos", (960, 262), px=84, d=0.6)
    R.snd(t_historia, "escribir", 0.6, dur=0.9)
    R.snd(t_cinco, "escribir", 0.5, dur=0.6)
    pop(R, lambda t: C.cronometro((t - t_cinco) * 2.0 * math.pi / max(0.6, FIN(e) - t_cinco + 0.6)), t_cinco + 0.15, pos=(1660, 520, 1.15), t_out=FIN(e) + 0.6, sale="encoger",
        d_in=0.5, snd="pop", vol=0.7, sem=6)
    R.snd(t_cinco + 0.3, "reloj_rapido", 0.45, dur=1.6)


# ------------------------------------------------------------------ MESETA: Elam, qanats, medos y persas
def _meseta(R):
    e = "meseta"
    i0 = INI(e)
    t_meseta, t_monta, t_desi = T(e, "meseta"), T(e, "montanas"), T(e, "desiertos")
    t_susa, t_elam, t_tab, t_hace = T(e, "susa"), T(e, "elamitas"), T(e, "tablillas"), T(e, "hace")
    t_viv, t_qan, t_tun, t_agua = T(e, "vivir"), T(e, "qanats"), T(e, "tuneles"), T(e, "agua")
    t_mil, t_trib, t_jin, t_medos, t_persas = T(e, "mil", frase=3), T(e, "tribus"), T(e, "jinetes"), T(e, "medos", frase=3), T(e, "persas")
    t_unen, t_babi, t_destr, t_asirio = T(e, "unen"), T(e, "babilonia"), T(e, "destruyen"), T(e, "asirio")
    R.camara(i0 - 0.4, 53.0, 32.4, 2.0)
    R.camara(t_meseta + 0.5, 53.5, 32.2, 2.15)
    R.camara(t_susa - 0.2, 52.0, 32.0, 2.3)
    R.camara(t_susa + 0.6, 49.0, 31.8, 3.2)
    R.camara(t_viv, 50.0, 32.5, 2.6)
    R.camara(t_mil - 0.1, 51.0, 32.5, 2.2)
    R.camara(t_medos + 0.2, 50.5, 32.5, 2.25)
    R.camara(t_unen, 47.5, 34.0, 2.3)
    R.camara(t_destr - 0.2, 45.5, 34.6, 2.6)
    R.camara(FIN(e), 45.0, 35.2, 2.5)
    # 1) la meseta: montañas alrededor y desierto
    R.terreno(i0 - 0.3, "meseta", COL["meseta"], 1.0)
    R.anio(t_hace - 0.6, -500)
    R.anio(t_hace - 0.2, -500)
    R.anio(t_hace + 0.9, -3000)
    for k, (lon, lat, s) in enumerate(((46.0, 36.9, 0.34), (51.6, 38.3, 0.3), (58.0, 37.0, 0.32), (45.2, 30.8, 0.26))):
        pop(R, P.montanas(), t_monta + 0.14 * k, geo=(lon, lat), off=(0, 40), s=s, sem=10 + k, snd="pop" if k == 0 else None, t_out=t_susa - 0.15, sale="encoger", zs=0.5)
    R.act(A.camello(0), geo=(58.5, 30.0), off=(0, 20), s=0.42, t_in=t_desi + 0.05, d_in=0.45, entra="pop", sem=14, sfx=[(0, "pop", 0.5)], t_out=t_susa - 0.15, sale="encoger", zs=0.5)
    R.act(lambda t: A.camello(int(t * 3)), geo=(55.5, 28.6), off=(0, 20), s=0.36, t_in=t_desi + 0.25, d_in=0.45, entra="pop", sem=15, t_out=t_susa - 0.15, sale="encoger", zs=0.5)
    R.act(A.sol_brillo(40), pos=(1600, 250, 0.9), t_in=t_desi + 0.3, d_in=0.5, entra="pop", sem=16, sfx=[(0, "brillo", 0.45)], t_out=t_susa - 0.15, sale="sube_fuera", d_out=0.5, z=-1)
    lugar(R, t_meseta, t_susa - 0.2, "MESETA IRANÍ", (53.0, 33.5), off=(0, -30), px=60)
    R.snd(t_meseta, "escribir", 0.5, dur=0.8)
    # 2) Susa: Elam y las tablillas
    R.terreno(t_susa - 0.15, "elam", COL["elam"], 1.2)
    R.act(P.tablilla(), geo=(48.25, 32.2), off=(0, -90), s=0.7, t_in=t_tab - 0.1, d_in=0.45, entra="pop", sem=20, sfx=[(0, "pop", 0.6)], t_out=t_viv - 0.2, sale="encoger", zs=0.4, z=1)
    R.act(persona(ARCILLA, PIEL_OSC, "pelo", "feliz", (30, 120), 0, traje="corta", acc_d="pincel"), geo=(48.9, 31.6), off=(70, 80), s=0.5, t_in=t_elam, d_in=0.45, entra="pop", sem=21,
          sfx=[(0, "pop", 0.6)], t_out=t_viv - 0.2, sale="encoger", zs=0.4)
    R.act(persona(MADERA, PIEL_OSC, "pelo", "normal", (30, 30), 1, traje="corta", acc_d="tazon"), geo=(47.6, 31.6), off=(-70, 80), s=0.46, t_in=t_elam + 0.2, d_in=0.45, entra="pop", sem=22,
          sfx=[(0, "pop", 0.5)], t_out=t_viv - 0.2, sale="encoger", zs=0.4)
    lugar(R, t_susa, t_viv - 0.3, "SUSA", (48.25, 32.2), off=(0, -200), px=70)
    R.snd(t_susa, "escribir", 0.5, dur=0.6)
    R.snd(t_tab, "garabato", 0.6, dur=1.4)
    R.anio(t_hace + 1.6, -3000)
    # 3) qanats
    R.terreno(t_viv - 0.1, "meseta", COL["meseta"], 1.0)
    R.act(lambda t: P.qanat(int(t * 5)), pos=(960, 760, 1.55), t_in=t_qan - 0.2, d_in=0.6, entra="pop", sem=24, sfx=[(0, "pop", 0.6), (0.2, "chorro", 0.35, {"dur": 2.6})],
          t_out=t_mil - 0.2, sale="encoger", z=1)
    R.act(persona(AZUL_IMP, PIEL_OSC, "kolah", "feliz", (30, 60), 0, traje="corta", acc_d="tazon"), pos=(1560, 880, 0.7), t_in=t_agua + 0.1, d_in=0.45, entra="pop", sem=25,
          sfx=[(0, "pop", 0.5), (0.2, "glug", 0.4)], t_out=t_mil - 0.2, sale="encoger")
    R.texto(t_qan, t_mil - 0.3, "QANAT", (600, 300), px=84, d=0.6)
    R.snd(t_qan, "escribir", 0.5, dur=0.6)
    R.snd(t_tun, "gota", 0.5)
    # 4) medos y persas llegan a caballo
    R.anio(t_mil - 0.3, -3000)
    R.anio(t_mil + 0.4, -1000)
    R.terreno(t_medos - 0.2, "medos", COL["medos"], 1.1)
    campo_extra(R, "persis", COL["persis"], t_persas - 0.3)
    R.sello(t_medos + 0.1, "م", "Medos", color=(72, 130, 82))
    for k, (lon, lat, col, hat) in enumerate(((47.0, 36.2, VERDE_OSC, "gorro"), (50.4, 37.0, VERDE_OSC, "gorro"))):
        R.act(lambda t, k=k, col=col, hat=hat: Bb.jinete(int(t * 7) + k, col, hat, True, False, "feliz"), geo=(lon, lat), off=lambda t, k=k: (80 * math.sin(t * 0.8 + k) - 40, 30),
              s=0.3, t_in=t_trib - 0.1 + 0.25 * k, d_in=0.4, entra="pop", sem=30 + k, sfx=[(0, "galope", 0.35, {"dur": 2.2})] if k == 0 else [], t_out=t_unen - 0.2, sale="encoger", zs=0.5, z=1)
    for k, (lon, lat) in enumerate(((52.0, 29.6), (54.0, 30.4))):
        R.act(lambda t, k=k: Bb.jinete(int(t * 7) + k, (214, 170, 60), "gorro", True, False, "feliz"), geo=(lon, lat), off=lambda t, k=k: (70 * math.sin(t * 0.7 + k * 2) - 30, 30),
              s=0.3, t_in=t_persas - 0.1 + 0.25 * k, d_in=0.4, entra="pop", sem=34 + k, sfx=[(0, "galope", 0.35, {"dur": 2.2})] if k == 0 else [], t_out=t_unen - 0.2, sale="encoger", zs=0.5, z=1)
    lugar(R, t_medos, t_unen - 0.3, "MEDOS", (49.6, 35.6), off=(0, -10), px=52)
    lugar(R, t_persas, t_unen - 0.3, "PERSAS", (53.0, 28.8), off=(0, 40), px=52)
    # 5) los medos se unen y, con Babilonia, destruyen Nínive
    R.terreno(t_unen - 0.2, "medo_persa", COL["medos"], 1.2)
    R.anio(t_unen, -1000)
    R.anio(t_destr + 0.6, -612)
    Pm = R.ruta([(48.5, 34.8), (46.5, 35.6), (44.0, 36.2)], t_unen + 0.2, 1.2, ancho=6.0)
    Pb = R.ruta([(44.4, 32.5), (44.2, 34.5), (43.3, 36.0)], t_babi + 0.1, 1.0, ancho=6.0)
    R.act(A.torre_muralla(1.0), geo=(43.15, 36.36), off=(0, 0), s=0.55, t_in=t_babi - 0.2, d_in=0.45, entra="pop", sem=40, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.3, sale="caer", d_out=0.8, zs=0.5)
    R.act(A.espadas(), geo=(43.4, 35.9), off=(0, 0), s=0.8, t_in=t_destr + 0.05, d_in=0.3, entra="pop", sem=41, sfx=[(0, "impacto", 0.7)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.5, z=2)
    R.act(A.estallido(14, 40, 120), geo=(43.15, 36.36), off=(0, -30), s=0.8, t_in=t_asirio - 0.05, d_in=0.15, entra="fija", sem=42, sfx=[(0, "explosion", 0.7)], t_out=t_asirio + 0.45, sale="cortar", z=3, zs=0.5)
    lugar(R, t_babi - 0.2, FIN(e), "BABILONIA", (44.4, 32.5), off=(0, 34), px=46)
    lugar(R, t_destr, FIN(e), "NÍNIVE", (43.15, 36.36), off=(-110, -30), px=46)


# ------------------------------------------------------------------ CIRO
def _ciro(R):
    e = "ciro"
    i0 = INI(e)
    t_persas, t_secreto, t_joven, t_ciro = T(e, "persas"), T(e, "secreto"), T(e, "joven"), T(e, "ciro")
    t_550, t_derr, t_medos, t_imp = T(e, "quinientos"), T(e, "derrota"), T(e, "medos"), T(e, "imperio")
    t_lidia, t_babi = T(e, "lidia"), T(e, "babilonia")
    t_noc, t_dioses, t_volver, t_cauti = T(e, "destruye"), T(e, "dioses"), T(e, "volver"), T(e, "cautivos")
    t_cil, t_arc, t_decl, t_der = T(e, "cilindro"), T(e, "arcilla"), T(e, "declaracion"), T(e, "derechos")
    R.terreno(i0 - 0.6, "persis", COL["persis"], 1.0)
    R.camara(i0 - 0.5, 50.0, 32.0, 2.4)
    R.camara(t_secreto, 53.0, 30.6, 3.1)
    R.camara(t_550 - 0.2, 52.0, 32.6, 2.3)
    R.camara(t_derr + 0.5, 50.0, 34.0, 2.1)
    R.camara(t_lidia - 0.4, 40.0, 36.5, 1.9)
    R.camara(t_lidia + 0.4, 34.0, 38.0, 2.2)
    R.camara(t_babi - 0.3, 41.0, 35.0, 1.9)
    R.camara(t_babi + 0.5, 44.4, 33.0, 2.7)
    R.camara(t_dioses, 44.4, 33.4, 2.9)
    R.camara(t_volver + 0.5, 40.5, 32.6, 2.4)
    R.camara(t_cil - 0.2, 47.0, 33.5, 2.0)
    R.camara(FIN(e), 47.0, 33.8, 1.95)
    R.anio(i0, -612)
    R.anio(t_550 - 0.3, -612)
    R.anio(t_550 + 0.7, -550)
    R.anio(t_lidia, -546)
    R.anio(t_babi + 0.3, -539)
    # 1) un secreto: un joven llamado Ciro
    R.act(A.signo_pregunta(), geo=(53.0, 30.2), off=lambda t: (0, -120 + 10 * math.sin(t * 4)), s=0.8, t_in=t_secreto, d_in=0.4, entra="pop", sem=50, sfx=[(0, "pluck", 0.5, {"tono": 1.2})],
          t_out=t_ciro + 0.15, sale="encoger", zs=0.4, z=2)
    R.act(persona(PURPURA, PIEL_OSC, "diadema", "feliz", (20, 110), 0, traje="tunica", faja=ORO, cuello=ORO, acc_d=None), geo=(53.0, 30.3), off=(0, 60), s=0.8, t_in=t_ciro - 0.05, d_in=0.45,
          entra="pop", sem=51, sfx=[(0, "pop", 0.6), (0.1, "brillo", 0.5)], t_out=t_550 - 0.3, sale="encoger", zs=0.4, z=1)
    lugar(R, t_ciro, t_550 - 0.4, "CIRO", (53.0, 30.3), off=(0, -160), px=84)
    R.snd(t_ciro, "escribir", 0.5, dur=0.5)
    # 2) derrota a los medos: nace el imperio aqueménida
    campo_extra(R, "medos", COL["medos"], i0, t_derr, d=0.3)
    R.terreno(t_derr - 0.05, "medo_persa", COL["aquemenida"], 1.3)
    R.sello(t_imp + 0.05, "ه", "Aqueménidas", color=(122, 70, 134))
    R.act(A.espadas(), geo=(48.5, 34.8), off=(0, 0), s=0.8, t_in=t_derr, d_in=0.3, entra="pop", sem=52, sfx=[(0, "impacto", 0.7)], t_out=t_medos + 0.6, sale="encoger", zs=0.5, z=2)
    R.act(P.estandarte_persa(), geo=(53.2, 30.2), off=(0, 30), s=0.85, t_in=t_imp - 0.1, d_in=0.45, entra="pop", sem=53, sfx=[(0, "pop", 0.6), (0.1, "bling", 0.5)], t_out=t_lidia - 0.3, sale="encoger", zs=0.5)
    R.act(persona(PURPURA, PIEL_OSC, "tiara", "feliz", (20, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), geo=(50.4, 31.0), off=(0, 60), s=0.7, t_in=t_imp, d_in=0.45, entra="pop", sem=54,
          sfx=[(0, "pop", 0.6)], t_out=t_lidia - 0.3, sale="encoger", zs=0.4, z=1)
    lugar(R, t_imp, t_lidia - 0.4, "IMPERIO AQUEMÉNIDA", (52.0, 35.4), off=(0, -10), px=62)
    # 3) Lidia y Babilonia
    campo_extra(R, "lidia", COL["aquemenida"], t_lidia - 0.1, d=0.9)
    R.ruta([(48.0, 35.0), (42.0, 37.6), (35.0, 38.6), (27.5, 38.5)], t_lidia - 0.4, 1.3, ancho=6.0)
    R.act(A.moneda(58), geo=(26.5, 38.5), off=(0, -40), s=0.8, t_in=t_lidia + 0.3, d_in=0.4, entra="pop", sem=55, sfx=[(0, "monedas", 0.6)], t_out=t_babi - 0.6, sale="encoger", zs=0.5, z=1)
    lugar(R, t_lidia + 0.1, t_babi - 0.5, "LIDIA", (31.0, 39.4), off=(0, -10), px=60)
    R.terreno(t_babi - 0.2, "ciro", COL["aquemenida"], 1.4)
    R.ruta([(50.0, 33.5), (47.5, 33.0), (44.4, 32.5)], t_babi - 0.6, 1.0, ancho=6.0)
    R.act(A.torre_muralla(1.0), geo=(44.4, 32.5), off=(-30, 0), s=0.85, t_in=t_babi - 0.1, d_in=0.45, entra="pop", sem=56, sfx=[(0, "pop", 0.6)], t_out=t_cil - 0.4, sale="encoger", zs=0.5)
    R.act(A.torre_muralla(0.8), geo=(44.4, 32.5), off=(50, 10), s=0.7, t_in=t_babi, d_in=0.45, entra="pop", sem=57, sfx=[], t_out=t_cil - 0.4, sale="encoger", zs=0.5)
    lugar(R, t_babi, t_volver, "BABILONIA", (44.4, 32.5), off=(0, 50), px=56)
    # 4) respeta a sus dioses, deja volver a los cautivos
    R.act(A.estrella5(46), geo=(44.4, 32.5), off=lambda t: (-10, -190 + 8 * math.sin(t * 4)), s=1.0, t_in=t_dioses - 0.1, d_in=0.4, entra="pop", sem=58, sfx=[(0, "bling", 0.5)], t_out=t_cil - 0.4,
          sale="encoger", zs=0.4, z=2)
    Pv = R.ruta([(44.4, 32.5), (40.0, 32.6), (37.0, 32.0), (35.3, 31.8)], t_volver - 0.1, 2.0, ancho=6.0)
    R.act(lambda t: A.multitud(6, 4), pos_geo=R.camino_pos(Pv, t_volver, 2.2, ease=lambda u: u), off=(0, -6), s=0.34, t_in=t_volver - 0.1, d_in=0.4, entra="pop", sem=59,
          sfx=[(0, "pasos", 0.35, {"dur": 2.2})], t_out=t_cil - 0.3, sale="encoger", zs=0.5, z=1)
    lugar(R, t_cauti - 0.2, t_cil - 0.3, "DE VUELTA A CASA", (39.5, 32.8), off=(0, 60), px=52)
    R.snd(t_noc, "brillo", 0.4)
    # 5) el cilindro
    R.act(P.cilindro(), pos=(960, 800, 1.6), t_in=t_cil - 0.1, d_in=0.6, entra="pop", sem=60, sfx=[(0, "pop", 0.7), (0.2, "bling", 0.6)], t_out=FIN(e) + 0.4, sale="encoger", z=1)
    R.act(A.estrella5(34), pos=lambda t: (1380, 640 + 8 * math.sin(t * 4), 1.0), t_in=t_decl, d_in=0.4, entra="pop", sem=61, sfx=[(0, "bling", 0.5)], t_out=FIN(e) + 0.4, sale="encoger", z=2)
    R.texto(t_decl - 0.15, FIN(e) + 0.2, "DERECHOS HUMANOS", (960, 290), px=84, d=1.0)
    R.snd(t_decl, "escribir", 0.5, dur=1.0)


# ------------------------------------------------------------------ DARÍO
def _dario(R):
    e = "dario"
    i0 = INI(e)
    t_dario, t_egipto, t_indo = T(e, "dario"), T(e, "egipto"), T(e, "indo")
    t_prov, t_mon, t_camino, t_km = T(e, "provincias"), T(e, "monedas"), T(e, "camino"), T(e, "kilometros")
    t_mens, t_posta, t_sem = T(e, "mensajeros"), T(e, "posta"), T(e, "semana")
    t_pers, t_col, t_pueb, t_reg = T(e, "persepolis"), T(e, "columnas"), T(e, "pueblos"), T(e, "regalos")
    t_jerjes, t_grecia, t_med, t_derrota = T(e, "jerjes"), T(e, "grecia"), T(e, "medicas"), T(e, "derrota")
    R.terreno(i0 - 0.2, "dario", COL["aquemenida"], 1.5)
    R.camara(i0 - 0.3, 47.0, 32.0, 1.6)
    R.camara(t_indo + 0.5, 47.5, 31.5, 1.45)
    R.camara(t_prov, 47.5, 31.5, 1.5)
    R.camara(t_camino - 0.3, 38.0, 36.0, 1.9)
    R.camara(t_mens, 34.0, 37.5, 2.3)
    R.camara(t_posta + 0.5, 42.0, 35.0, 2.1)
    R.camara(t_pers - 0.4, 50.0, 31.0, 2.4)
    R.camara(t_pers + 0.6, 52.9, 29.9, 3.4)
    R.camara(t_reg + 0.3, 52.9, 29.8, 3.2)
    R.camara(t_jerjes - 0.2, 32.0, 37.5, 1.9)
    R.camara(FIN(e), 27.0, 37.5, 2.3)
    R.anio(i0, -539)
    R.anio(t_dario, -539)
    R.anio(t_dario + 0.8, -522)
    R.anio(t_col, -518)
    R.anio(t_jerjes, -490)
    R.anio(t_med, -480)
    # 1) el imperio más grande: Egipto – río Indo
    R.act(persona(AZUL_IMP, PIEL_OSC, "tiara", "feliz", (20, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), pos=(1640, 820, 0.85), t_in=t_dario - 0.05, d_in=0.45, entra="pop",
          sem=70, sfx=[(0, "pop", 0.6), (0.1, "brillo", 0.5)], t_out=t_prov - 0.15, sale="encoger", z=1)
    R.texto(t_dario, t_prov - 0.2, "DARÍO I", (1640, 540), px=76, d=0.6)
    lugar(R, t_egipto - 0.1, t_prov - 0.2, "EGIPTO", (30.5, 27.8), off=(0, 0), px=58)
    lugar(R, t_indo - 0.1, t_prov - 0.2, "RÍO INDO", (72.5, 28.6), off=(0, 0), px=58)
    R.snd(t_egipto, "escribir", 0.5, dur=0.6)
    R.snd(t_indo, "escribir", 0.5, dur=0.6)
    # 2) provincias, monedas y Camino Real
    R.romper("gancho", t_prov - 0.05, t_prov + 0.35, t_mon - 0.3, t_mon + 0.1, colores=None, gap=5, deriva=10)
    R.snd(t_prov, "crujido", 0.5, dur=0.5)
    for k, (lon, lat) in enumerate(((31.0, 27.5), (34.0, 39.0), (44.0, 33.5), (54.0, 33.5), (64.0, 38.0), (69.0, 29.0))):
        R.act(P.gota_oro(34), geo=(lon, lat), off=(0, -30), s=1.0, t_in=t_mon + 0.15 * k, d_in=0.4, entra="cae", dy=400, sem=71 + k, sfx=[(0, "monedas", 0.45)] if k % 2 == 0 else [],
              t_out=t_camino + 0.3, sale="encoger", zs=0.4, z=1)
    R.rio(M.CAMINO_REAL, t_camino - 0.2, 2.6, (226, 176, 70), ancho=16, t1=t_pers - 0.3)
    R.snd(t_camino - 0.2, "pincel", 0.6, dur=2.4)
    R.texto(t_camino, t_mens - 0.2, "CAMINO REAL", (960, 210), px=86, d=0.8)
    R.contador(t_km - 0.4, t_km + 0.9, 0, 2500, (960, 330), px=104)
    R.snd(t_km - 0.3, "reloj_rapido", 0.45, dur=1.3)
    R.texto(t_km + 0.5, t_mens - 0.2, "kilómetros", (960, 420), px=58, d=0.5)
    # 3) mensajeros: relevos a caballo
    for k, (u0, u1) in enumerate(((0.0, 0.4), (0.3, 0.7), (0.6, 1.0))):
        Tt0 = t_mens + 0.1 + 1.6 * u0
        R.act(lambda t, k=k: Bb.jinete(int(t * 8) + k, ROJO_OSC if k % 2 == 0 else PURPURA, "gorro", False, False, "feliz"),
              pos_geo=R.camino_pos(M.CAMINO_REAL, t_mens + 0.15 + 1.9 * u0, 1.9 * (u1 - u0) + 0.2, ease=lambda u: u), off=(0, -18), s=0.3, t_in=t_mens + 0.05 + 1.9 * u0,
              d_in=0.3, entra="pop", sem=80 + k, sfx=[(0, "galope", 0.4, {"dur": 1.5})], t_out=t_mens + 0.15 + 1.9 * u1 + 0.3, sale="encoger", zs=0.6, z=1)
    for k, (lon, lat) in enumerate(((35.0, 39.4), (40.0, 37.8), (44.6, 35.4), (47.0, 33.4))):
        R.act(P.carta(), geo=(lon, lat), off=(0, -10), s=0.7, t_in=t_posta + 0.2 * k, d_in=0.3, entra="pop", sem=84 + k, sfx=[(0, "tick", 0.4, {"tono": 1.0 + 0.12 * k})], t_out=t_sem + 0.3, sale="encoger", zs=0.4, z=1)
    R.texto(t_sem - 0.2, t_pers - 0.4, "7 DÍAS", (960, 780), px=112, d=0.6)
    R.snd(t_sem, "escribir", 0.5, dur=0.6)
    # 4) Persépolis: columnas gigantes y delegaciones con regalos
    R.terreno(t_pers - 0.3, "persis", COL["aquemenida"], 1.4)
    cols = [(380, 1.0), (620, 0.9), (1300, 0.9), (1540, 1.0)]
    for k, (x, al) in enumerate(cols):
        R.act(P.columna(al), pos=(x, 560 + 120 * al, 1.25), t_in=t_col - 0.1 + 0.16 * k, d_in=0.8, entra="pluma", sem=90 + k, sfx=[(0, "crece", 0.45, {"dur": 0.6})], t_out=t_jerjes - 0.2, sale="encoger", z=-1)
    R.texto(t_pers, t_jerjes - 0.3, "PERSÉPOLIS", (960, 190), px=92, d=0.8)
    R.snd(t_pers, "escribir", 0.5, dur=0.8)
    gentes = [(ROJO_CH, "kolah", "saco"), (VERDE_OSC, "gorro", "cuenco"), (MORADO, "pelo", "copa"), (ORO_OSC, "kufiya", "tetera")]
    for k, (ropa, hat, acc) in enumerate(gentes):
        x0 = 2150 + 90 * k
        R.act(lambda t, k=k, ropa=ropa, hat=hat, acc=acc: persona(ropa, PIEL_OSC, hat, "feliz", (40, 80 + 10 * (k % 2)), int(t * 3) + k, traje="corta", acc_d=acc),
              pos=lambda t, x0=x0, k=k: (lerp(x0, 820 + 140 * k, e_out(prog(t, t_pueb - 0.3 + 0.2 * k, t_reg + 0.3 + 0.2 * k))), 900 + 6 * math.sin(t * 9 + k), 0.6),
              t_in=t_pueb - 0.3 + 0.2 * k, d_in=0.01, entra="fija", sem=95 + k, sfx=[(0, "pasos", 0.25, {"dur": 1.6})] if k == 0 else [], t_out=t_jerjes - 0.2, sale="encoger", z=2)
    R.act(lambda t: A.camello(int(t * 3)), pos=lambda t: (lerp(2400, 1730, e_out(prog(t, t_pueb - 0.1, t_reg + 0.4))), 930, 0.45), t_in=t_pueb - 0.1, d_in=0.01, entra="fija", sem=99,
          t_out=t_jerjes - 0.2, sale="encoger", z=2)
    # 5) Grecia: las guerras médicas terminan en derrota
    R.terreno(t_jerjes - 0.3, "dario", COL["aquemenida"], 1.0)
    R.act(persona(PURPURA, PIEL_OSC, "tiara", "serio", (20, 110), 0, barba=NEGRO, traje="tunica", faja=ORO, cuello=ORO), geo=(30.5, 39.6), off=(40, 60), s=0.8, t_in=t_jerjes, d_in=0.45, entra="pop",
          sem=100, sfx=[(0, "pop", 0.6)], t_out=t_derrota + 0.1, sale="caer", d_out=0.9, zs=0.4, z=1)
    lugar(R, t_jerjes, t_derrota, "JERJES", (30.5, 39.6), off=(40, -160), px=70)
    R.act(persona(ROJO_OSC, PIEL_OSC, "casco_griego", "enojo", (20, 140), 1, traje="armadura", acc_d="lanza"), geo=(22.4, 38.8), off=(0, 40), s=0.7, t_in=t_grecia - 0.1, d_in=0.45, entra="pop",
          sem=101, sfx=[(0, "pop", 0.6)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.4, z=1)
    R.act(persona(ROJO_OSC, PIEL_OSC, "casco_griego", "enojo", (20, 140), 0, traje="armadura", acc_d="espada"), geo=(23.4, 37.0), off=(0, 50), s=0.62, t_in=t_grecia + 0.1, d_in=0.45, entra="pop",
          sem=102, sfx=[(0, "pop", 0.5)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.4, z=1)
    Pg = R.ruta([(30.0, 39.0), (26.0, 38.4), (23.9, 38.1)], t_grecia - 0.1, 1.0, ancho=6.0)
    R.act(A.espadas(), geo=(25.6, 38.4), off=(0, -10), s=0.8, t_in=t_med, d_in=0.3, entra="pop", sem=103, sfx=[(0, "impacto", 0.7)], t_out=FIN(e) + 0.3, sale="encoger", zs=0.5, z=2)
    R.act(A.pulgar(False), pos=(1560, 640, 0.9), t_in=t_derrota - 0.1, d_in=0.3, entra="pop", sem=104, sfx=[(0, "bocinazo", 0.35)], t_out=FIN(e) + 0.3, sale="encoger", z=3)
    R.texto(t_med, FIN(e), "MARATÓN · SALAMINA", (960, 200), px=70, d=0.9)
    R.snd(t_derrota, "error", 0.4)
