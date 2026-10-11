# -*- coding: utf-8 -*-
"""'El viaje de una gota' — estilo boceto DINÁMICO (v2), formato vertical, animación en BUCLE.

Ritmo de la referencia: un cambio visual cada ~1,5 s; objetos que aparecen como boceto de lápiz que la tinta cierra
('lt'), que saltan ('pop'), suben, caen y rebotan; físicas (lluvia, gotas, salpicaduras, aplastamiento al aterrizar);
cada movimiento lleva su efecto de sonido (campo `sfx` de cada actor y `Mundo.sonidos`).
Una sola clase (`Mundo`) dibuja todo en función del tiempo global. La gota mascota viaja entre escenas por "pases".
El último cuadro es idéntico al primero (nube + sol + gota): el temblor/parpadeo vuelven a fase 0 en el cuadro final.
La versión anterior (más lenta) quedó en escenas_v1.py.
"""
import math
import types

import numpy as np

import boceto as B
import objetos as O
from escena_base import *  # noqa: F401,F403
from motor import H, W, e_back, e_in, e_inout, e_out, lerp, prog, smooth

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
FIN_CUADRO = TOTAL - 1.5 / 30      # desde aquí el temblor y el parpadeo vuelven a la fase 0 (= primer cuadro)
# la "vida" (respiración, ondulación, giro del sol) usa ciclos ENTEROS en la duración total: el movimiento cierra el bucle
B.OMEGA = 2 * math.pi * round(TOTAL / 1.85) / TOTAL
B.GIRO_SOL = 2 * math.pi * 3 / TOTAL



def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


# ------------------------------------------------------------------ anclas (palabras de la narración)
t_gota, t_miles, t_millones, t_vueltas = T("nube", "gota"), T("nube", "miles"), T("nube", "millones"), T("nube", "vueltas")
t_nunca, t_salido, t_planeta = T("nube", "nunca"), T("nube", "salido"), T("nube", "planeta")
t_hoy, t_cae, t_lluvia, t_mont = T("montana", "hoy"), T("montana", "cae"), T("montana", "lluvia"), T("montana", "montana")
t_congela, t_decadas, t_glaciar = T("hielo", "congela"), T("hielo", "decadas"), T("hielo", "glaciar")
t_derrite, t_baja, t_donde = T("rio", "derrite"), T("rio", "baja"), T("rio", "donde")
t_apenas, t_meses = T("rio", "apenas"), T("rio", "meses")
t_termina, t_vaso_p, t_luego, t_ti = T("vaso", "termina"), T("vaso", "vaso"), T("vaso", "luego"), T("vaso", "ti")
t_devuelves, t_sigue, t_camino = T("vaso", "devuelves"), T("vaso", "sigue"), T("vaso", "camino")
t_final, t_llega, t_quedarse = T("mar", "final"), T("mar", "llega"), T("mar", "quedarse")
t_tres, t_anos = T("mar", "tres"), T("mar", "anos")
t_sol, t_calienta, t_levanta, t_cielo = T("sol", "sol"), T("sol", "calienta"), T("sol", "levanta"), T("sol", "cielo")
t_arriba, t_nueve, t_dias = T("cierre", "arriba"), T("cierre", "nueve"), T("cierre", "dias")
t_vuelve, t_empezar = T("cierre", "vuelve"), T("cierre", "empezar")

C0_NUBE = (560, 720, 1.2)
C0_SOL = (170, 470, 1.0)
C0_GOTA = (620, 410, 1.0)
PEAK_C = (470, 990)
RIO_TF = (540, 900, 0.9)
GLASS_A = (713, 1040, 1.0, 0.0)
GLASS_B = (392, 1195, 0.62, -0.95)
PERSONA = (270, 1170, 0.85)
MOUTH = (270, 1238)
SOP = (MOUTH[0] + 190, MOUTH[1] - 190)
SPOUT = (713, 545)
t_ride0, t_ride1 = t_baja + 0.55, t_meses + 0.45
t_gm0, t_gm1 = t_luego + 0.15, t_luego + 0.55
t_bebe = t_ti + 0.9
t_land_mont = t_cae + 1.4
t_land_plan = t_planeta + 0.35
t_aterriza = t_dias - 0.2              # la gota vuelve a posarse sobre la nube


# ------------------------------------------------------------------ movimiento de la gota
def pase(t0, t1, p0, p1, s0, s1, h=0.0, ease="inout", rot=0.0, giro=0.0):
    """Movimiento de la gota entre dos puntos (con salto de altura h y, opcional, vueltas). fn(t) -> (x, y, s, rot)."""
    def fn(t):
        u = prog(t, t0, t1)
        k = e_inout(u) if ease == "inout" else (e_in(u) if ease == "in" else e_out(u) if ease == "out" else u)
        return (lerp(p0[0], p1[0], u if ease == "in" else k), lerp(p0[1], p1[1], k) - h * math.sin(math.pi * u),
                lerp(s0, s1, k), rot * math.sin(math.pi * u) + 2 * math.pi * giro * e_inout(u))
    return fn


def vaso_tf(t):
    k = smooth(prog(t, t_gm0, t_gm1))
    return (lerp(GLASS_A[0], GLASS_B[0], k), lerp(GLASS_A[1], GLASS_B[1], k), lerp(GLASS_A[2], GLASS_B[2], k),
            lerp(GLASS_A[3], GLASS_B[3], k))


def nivel_agua(t):
    n = 0.32 + 0.38 * smooth(prog(t, t_vaso_p + 0.5, t_vaso_p + 1.0))
    return n - 0.66 * smooth(prog(t, t_gm1 + 0.12, t_gm1 + 0.85))


def rio_a_pantalla(v, dy=0.0):
    p = O.punto_rio(v)
    return RIO_TF[0] + p[0] * RIO_TF[2], RIO_TF[1] + p[1] * RIO_TF[2] + dy


def _u_rio(t):
    return prog(t, t_baja - 0.15, t_baja + 1.35)


def _v_rio(t):
    return min(smooth(prog(t, t_ride0, t_ride1)) * 0.995, max(0.0, _u_rio(t) - 0.1))


def camino_punteado():
    return B.curva([SOP, (760, 470), (900, 330), (740, 250), (540, 262)], 14)


def construir_pases():
    P = []
    g0 = C0_GOTA
    P.append((t_gota - 0.05, t_gota + 0.45, pase(t_gota - 0.05, t_gota + 0.45, g0, g0, 1, 1, 75, rot=0.25)))
    P.append((t_vueltas, t_vueltas + 0.7, pase(t_vueltas, t_vueltas + 0.7, g0, g0, 1, 1, 40, giro=1.0)))
    P.append((t_nunca - 0.05, t_nunca + 0.5, pase(t_nunca - 0.05, t_nunca + 0.5, g0[:2], (540, 780), 1, 1, 120, rot=-0.2)))
    P.append((t_planeta - 0.15, t_planeta + 0.35, pase(t_planeta - 0.15, t_planeta + 0.35, (540, 780), (540, 827), 1, 0.9, 90)))
    t_x = INI("montana") - 0.6
    P.append((t_x, t_x + 0.35, pase(t_x, t_x + 0.35, (540, 827), (540, 827), 0.9, 0.02, 0, "lin")))
    P.append((t_cae - 0.05, t_cae + 0.25, pase(t_cae - 0.05, t_cae + 0.25, (560, 880), (560, 880), 0.02, 0.7, 0, "lin")))
    P.append((t_cae + 0.25, t_land_mont, pase(t_cae + 0.25, t_land_mont, (560, 880), PEAK_C, 0.7, 0.8, 0, "in")))
    t_h = INI("hielo") + 0.2
    P.append((t_h, t_h + 0.55, pase(t_h, t_h + 0.55, PEAK_C, (540, 900), 0.8, 1.0, 150, rot=0.3)))
    r0 = rio_a_pantalla(0.0, -40)
    P.append((t_derrite + 0.55, t_derrite + 1.05,
              pase(t_derrite + 0.55, t_derrite + 1.05, (540, 900), r0, 1.0, 0.62, 120, rot=-0.3)))

    def rio_(t):
        x, y = rio_a_pantalla(_v_rio(t), -40)
        return x, y + 3 * math.sin(t * 5), 0.62, 0.07 * math.sin(t * 3.0)
    P.append((t_ride0, t_ride1, rio_))
    fin_rio = rio_a_pantalla(0.995, -40)
    P.append((t_ride1 + 0.05, t_ride1 + 0.35, pase(t_ride1 + 0.05, t_ride1 + 0.35, fin_rio, fin_rio, 0.62, 0.02, 0, "lin")))
    P.append((t_termina - 0.02, t_termina + 0.4, pase(t_termina - 0.02, t_termina + 0.4, SPOUT, SPOUT, 0.02, 0.55, 0, "lin")))
    P.append((t_vaso_p + 0.05, t_vaso_p + 0.5, pase(t_vaso_p + 0.05, t_vaso_p + 0.5, SPOUT, (713, 1055), 0.55, 0.5, 0, "in")))

    def en_vaso(t):
        gx, gy, gs, gr = vaso_tf(t)
        q = B.transformar([(0.0, 130 - 250 * nivel_agua(t) - 15)], gx, gy, gs, gr)[0]
        return q[0], q[1], 0.5 * gs, gr * 0.6 + 0.05 * math.sin(t * 4)
    P.append((t_vaso_p + 0.5, t_bebe, en_vaso))
    q = en_vaso(t_bebe)
    P.append((t_bebe, t_bebe + 0.35, pase(t_bebe, t_bebe + 0.35, q[:2], MOUTH, q[2], 0.02, 20, "lin")))
    P.append((t_devuelves + 0.1, t_devuelves + 0.5, pase(t_devuelves + 0.1, t_devuelves + 0.5, SOP, SOP, 0.02, 0.5, 0, "lin")))
    P.append((t_sigue, t_sigue + 0.8, pase(t_sigue, t_sigue + 0.8, SOP, (900, 330), 0.5, 0.9, 150, rot=0.3)))
    P.append((t_final - 0.7, t_final + 0.05, pase(t_final - 0.7, t_final + 0.05, (900, 330), (540, 262), 0.9, 0.9, 60, rot=-0.2)))
    P.append((t_llega - 0.1, t_llega + 0.5, pase(t_llega - 0.1, t_llega + 0.5, (540, 262), (540, 1040), 0.9, 1.0, 0, "in")))
    P.append((t_llega + 0.5, t_llega + 1.35, pase(t_llega + 0.5, t_llega + 1.35, (540, 1040), (540, 1200), 1.0, 1.0, 0, "out")))
    P.append((t_levanta - 0.05, t_levanta + 1.3, pase(t_levanta - 0.05, t_levanta + 1.3, (540, 1200), (540, 640), 1.0, 0.95, 0)))
    P.append((t_levanta + 1.3, t_nueve - 0.7, pase(t_levanta + 1.3, t_nueve - 0.7, (540, 640), (540, 520), 0.95, 0.95, 0, "lin")))
    P.append((t_nueve - 0.7, t_aterriza, pase(t_nueve - 0.7, t_aterriza, (540, 520), g0[:2], 0.95, 1.0, 110, rot=-0.2)))
    P.append((t_empezar - 0.05, t_empezar + 0.45, pase(t_empezar - 0.05, t_empezar + 0.45, g0, g0, 1, 1, 60, rot=0.15)))
    return P


def construir_exprs():
    return [(-10, "abiertos", "sonrisa"), (t_gota, "feliz", "sonrisa"), (t_gota + 0.6, "abiertos", "sonrisa"),
            (t_vueltas, "feliz", "abierta"), (t_vueltas + 0.8, "abiertos", "sonrisa"),
            (t_salido, "miedo", "o"), (t_planeta + 0.1, "feliz", "sonrisa"), (t_cae, "miedo", "o"),
            (t_land_mont + 0.05, "abiertos", "o"), (t_land_mont + 0.9, "abiertos", "sonrisa"),
            (INI("hielo") - 0.5, "miedo", "zigzag"), (t_derrite, "feliz", "abierta"), (t_ride1, "abiertos", "sonrisa"),
            (t_vaso_p, "miedo", "o"), (t_vaso_p + 0.6, "feliz", "sonrisa"), (t_devuelves + 0.3, "abiertos", "sonrisa"),
            (t_sigue + 0.9, "abiertos", "o"), (t_llega, "miedo", "o"), (t_llega + 0.9, "abiertos", "o"),
            (t_quedarse - 0.1, "cerrados", "ronca"), (t_calienta - 0.1, "abiertos", "sonrisa"),
            (t_calienta + 0.1, "miedo", "o"), (t_levanta, "feliz", "abierta"), (t_aterriza, "abiertos", "sonrisa")]


LAND = [(t_land_plan, 0.3), (t_land_mont, 0.36), (INI("hielo") + 0.75, 0.2), (t_vaso_p + 0.5, 0.12), (t_aterriza, 0.3)]
CAIDAS = [(t_cae + 0.25, t_land_mont), (t_llega - 0.1, t_llega + 0.5)]


def squash_gota(t):
    """Aplastamiento al aterrizar (amortiguado) y estiramiento mientras cae."""
    for t0, a in LAND:
        d = t - t0
        if 0 <= d < 0.55:
            return a * math.exp(-d * 8) * math.cos(d * 20)
    for a, b in CAIDAS:
        if a <= t <= b:
            return -0.13
    return 0.0


# ------------------------------------------------------------------ actores (objetos dibujados)
def rebote(v):
    """Caída con rebote: v 0..1 -> (altura relativa 1..0, aplastamiento)."""
    if v < 0.6:
        return 1 - (v / 0.6) ** 2, -0.12 * (v / 0.6)
    w = (v - 0.6) / 0.4
    return 0.10 * math.sin(math.pi * min(1.0, w * 1.4)) * (1 - w), 0.3 * math.exp(-w * 6) * math.cos(w * 12)


def A(acts, d, pos, t_in, d_in=0.5, entra="pluma", t_out=None, d_out=0.45, sale="encoger", sem=0, dy=900, dx=900,
      flip=False, rot=0.0, sfx=(), sfx_out=(), vida=1.0):
    """Registra un actor. entra: pluma | lt (lápiz->tinta) | pop | sube | izq | cae | fija. sale: borrar | encoger | caer |
    baja | sube_fuera | izq_fuera. sfx = [(nombre, dt, vol, {kw})]: sonidos ligados a la entrada (sfx_out: a la salida)."""
    a = dict(d=d, pos=pos, t_in=t_in, d_in=d_in, entra=entra, t_out=t_out, d_out=d_out, sale=sale, sem=sem, dy=dy, dx=dx,
             flip=flip, rot=rot, snd=[], vida=vida)
    for s in sfx:
        a["snd"].append((t_in + s[1], s[0], s[2], s[3] if len(s) > 3 else {}))
    if t_out is not None:
        for s in sfx_out:
            a["snd"].append((t_out + s[1], s[0], s[2], s[3] if len(s) > 3 else {}))
    acts.append(a)
    return a


def _pos_barca(t):
    x, y = rio_a_pantalla(_v_rio(min(t, t_ride1)), -40)
    return x, y + 34 + 3 * math.sin(t * 5), 0.72, 0.07 * math.sin(t * 3.0)


def _pos_pez_salto(t):
    u = prog(t, t_llega + 0.75, t_llega + 1.65)
    return lerp(760, 980, u), 1085 - 330 * math.sin(math.pi * u), 0.7, -0.9 * math.cos(math.pi * u)


def SOL(te):
    return O.sol_din(76, te)


MORFS = []


def M(sa, sb, t0, dur=0.55, sfx=True):
    """Transformación del actor `sa` en el actor `sb` (técnica de la referencia): sa se corta al empezar y sb aparece al terminar;
    entre medias `Mundo.morf` dibuja la metamorfosis (contorno que se deforma, crayón que se disuelve y vuelve a aparecer)."""
    sa["t_out"], sa["sale"], sa["d_out"] = t0, "cortar", 0.01
    sb["t_in"], sb["entra"], sb["d_in"] = t0 + dur, "fija", 0.01
    MORFS.append(dict(a=sa, b=sb, t0=t0, dur=dur))
    if sfx:
        sb["snd"] += [(t0, "morph", 0.8, {}), (t0 + 0.05, "garabato", 0.5, {"dur": 0.45}), (t0 + dur, "pop", 0.45, {"tono": 1.2})]
    return sb


def construir_actores():
    MORFS.clear()
    R = []
    t_out_pl = INI("montana") - 0.6
    # ---- inicio: nube + sol (C0), que se van al hablar del planeta
    A(R, SOL, C0_SOL, -10, 0.1, t_out=t_nunca + 0.12, sale="encoger", sem=1, sfx_out=[("puf", 0, 0.4)])
    A(R, O.nube_din, C0_NUBE, -10, 0.1, t_out=t_nunca, sale="encoger", sem=2)
    # hojas de calendario que cruzan volando ("miles de millones de años")
    for i in range(6):
        t0 = t_miles + 0.16 * i
        yy = 760 + 95 * (i % 3) + 30 * math.sin(i * 1.9)
        A(R, O.hoja_cal(), (lambda t, t0=t0, yy=yy, i=i: (1240 - 1480 * prog(t, t0, t0 + 0.95), yy + 26 * math.sin((t - t0) * 9),
                                                          0.9, 0.45 * math.sin((t - t0) * 7 + i))),
          t0, 0.01, "fija", t_out=t0 + 1.0, d_out=0.01, sem=30 + i, sfx=[("papel", 0, 0.55)])
    # flecha circular ("dando vueltas")
    A(R, O.flecha_circ(120), (C0_GOTA[0], C0_GOTA[1], 1.15), t_vueltas, 0.4, "pluma", t_out=t_vueltas + 1.0, d_out=0.3,
      sale="borrar", sem=40, sfx=[("garabato", 0, 0.5, {"dur": 0.4}), ("whoosh", 0.05, 0.55, {"dur": 0.6})],
      sfx_out=[("borrar", 0, 0.4, {"dur": 0.3})])
    # ---- "nunca ha salido del planeta"
    A(R, O.flecha_ida(), (540, 590, 1.0), t_salido, 0.28, "pluma", t_out=t_out_pl + 0.1, d_out=0.3, sem=41,
      sfx=[("garabato", 0, 0.5, {"dur": 0.3}), ("whoosh", 0.12, 0.4, {"dur": 0.4})])
    A(R, O.tache(), (540, 360, 1.25), t_salido + 0.33, 0.3, "pop", t_out=t_out_pl + 0.1, d_out=0.3, sem=42,
      sfx=[("error", 0, 0.5), ("golpe_suave", 0.02, 0.8)])
    sp_planeta = A(R, O.planeta(), (540, 1060, 1.35), t_planeta, 0.4, "pop", t_out=t_out_pl, d_out=0.35, sem=43,
                   sfx=[("pop", 0, 0.9), ("golpe_suave", 0.18, 0.7)])
    for k, (px, py, ps) in enumerate([(300, 880, 0.9), (830, 770, 0.7), (800, 1330, 1.0)]):
        A(R, O.chispa(), (px, py, ps), t_planeta + 0.35 + 0.2 * k, 0.25, "pop", t_out=t_out_pl + 0.1, d_out=0.25, sem=44 + k,
          sfx=[("brillo", 0, 0.4, {"tono": 1.0 + 0.2 * k})])
    # ---- lluvia y montaña
    sp_nube2 = A(R, O.nube_din, C0_NUBE, t_hoy - 0.35, 0.5, "lt", t_out=INI("hielo") - 0.05, d_out=0.5, sale="sube_fuera", sem=2,
                 sfx_out=[("whoosh", 0, 0.5, {"dur": 0.5})])
    M(sp_planeta, sp_nube2, INI("montana") - 0.7, 0.5)
    sp_mont = A(R, O.montana(), (540, 1440, 0.95), t_cae + 0.45, 0.7, "sube", dy=700, t_out=INI("hielo") + 0.15, d_out=0.4,
                sale="borrar", sem=3, sfx=[("crece", 0, 0.7, {"dur": 0.8})])
    # ---- hielo
    sp_hielo = A(R, O.bloque_hielo(), (lambda t: (540, 905, 1.5 * (1 + 0.07 * math.sin(math.pi * prog(t, t_glaciar, t_glaciar + 0.5))))),
                 t_congela + 0.02, 0.4, "lt", t_out=t_derrite + 0.05, d_out=1.0, sale="encoger", sem=4,
                 sfx=[("hielo", 0.5, 0.9), ("tick", 0.9, 0.5)])
    M(sp_mont, sp_hielo, INI("hielo") + 0.1, 0.55)
    A(R, O.copo(70), (210, 600, 1.3), t_congela + 0.5, 0.35, "pop", t_out=t_derrite - 0.1, d_out=0.8, sale="caer", sem=5,
      sfx=[("tick", 0, 0.5, {"tono": 1.1})])
    A(R, O.copo(70), (880, 680, 0.8), t_congela + 0.85, 0.35, "pop", t_out=t_derrite - 0.1, d_out=0.8, sale="caer", sem=6,
      sfx=[("tick", 0, 0.5, {"tono": 1.3})])
    A(R, O.reloj(), (900, 1300, 1.0), t_decadas, 0.35, "lt", t_out=t_derrite - 0.35, d_out=0.35, sem=7,
      sfx=[("pop", 0.3, 0.6), ("reloj_rapido", 0.3, 0.7, {"dur": 1.4})])
    A(R, O.marcas(20), (120, 1250, 1.0), t_decadas + 0.1, 1.2, "pluma", t_out=t_derrite - 0.35, d_out=0.4, sale="borrar", sem=8,
      sfx=[("garabato", 0, 0.55, {"dur": 1.2})], sfx_out=[("borrar", 0, 0.5, {"dur": 0.4})])
    # ---- deshielo, río
    sp_charco = A(R, O.charco(), (lambda t: (540, 1225, 0.4 + 1.1 * smooth(prog(t, t_derrite + 0.3, t_derrite + 1.4)))),
                  t_derrite + 0.3, 0.3, "pop", t_out=t_baja + 0.6, d_out=0.4, sem=9, sfx=[("plop", 0.6, 0.7)])
    M(sp_hielo, sp_charco, t_derrite + 0.02, 0.6)
    sp_rio = A(R, O.rio(), RIO_TF, t_baja - 0.15, 1.5, "pluma", t_out=t_meses + 0.6, d_out=0.5, sale="borrar", sem=10,
               sfx=[("chorro", 0, 0.7, {"dur": 1.6})])
    A(R, O.hoja_barca(), _pos_barca, t_ride0 - 0.1, 0.35, "pop", t_out=t_ride1, d_out=0.4, sem=11,
      sfx=[("plop", 0, 0.7), ("ola", 0.3, 0.35, {"dur": 2.0})])
    # ---- grifo, vaso, persona, aliento
    sp_grifo = A(R, O.grifo(), (700, 430, 1.0), t_termina - 0.35, 0.35, "izq", dx=800, t_out=t_camino + 0.7, d_out=0.4,
                 sale="izq_fuera", sem=12, sfx=[("clink", 0.62, 0.7)])
    M(sp_rio, sp_grifo, t_meses + 0.5, 0.6)
    sp_vaso = A(R, O.vaso(), vaso_tf, t_vaso_p - 0.25, 0.3, "pop", t_out=t_bebe + 0.6, d_out=0.3, sem=13,
                sfx=[("clink", 0.05, 0.8, {"tono": 1.2}), ("pop", 0.1, 0.5)])
    A(R, O.persona("sonrisa"), PERSONA, t_luego - 0.05, 0.4, "sube", dy=650, t_out=t_camino + 0.5, d_out=0.4, sale="baja", sem=14,
      sfx=[("whoosh", 0, 0.4, {"dur": 0.4}), ("pop", 0.35, 0.7)], vida=1.5)
    sp_soplo = A(R, O.soplo(), (MOUTH[0] + 200, MOUTH[1] - 195, 0.9), t_devuelves, 0.4, "lt", t_out=t_sigue + 0.1, d_out=0.3,
                 sem=15, sfx=[("puf", 0.5, 0.9)])
    M(sp_vaso, sp_soplo, t_devuelves - 0.08, 0.55)
    # ---- mar
    t_mar = t_camino + 1.4
    A(R, O.mar_capa(1010, 530, B.AZUL_CL, ph=0.5), (0, 0, 1.0), t_mar, 0.9, "sube", dy=700, t_out=t_levanta + 0.3, d_out=0.7,
      sale="baja", sem=16, sfx=[("ola", 0, 0.7, {"dur": 0.9}), ("crece", 0, 0.4, {"dur": 0.8})])
    A(R, O.mar_capa(1120, 420, B.AZUL, ph=2.0), (0, 0, 1.0), t_mar + 0.2, 0.9, "sube", dy=700, t_out=t_levanta + 0.3, d_out=0.7,
      sale="baja", sem=17)
    A(R, O.pez(), lambda t: (300 + 35 * math.sin(t * 0.8), 1360, 0.8, 0.0), t_mar + 0.8, 0.3, "pop", t_out=t_levanta + 0.3,
      d_out=0.7, sale="baja", sem=18, sfx=[("burbuja", 0, 0.6)])
    A(R, O.pez(), lambda t: (830 + 30 * math.sin(t * 0.7 + 1), 1430, 0.6, 0.0), t_mar + 1.0, 0.3, "pop", t_out=t_levanta + 0.3,
      d_out=0.7, sale="baja", flip=True, sem=19, sfx=[("burbuja", 0, 0.5, {"tono": 1.3})])
    A(R, O.alga(), (130, 1530, 0.9), t_mar + 0.7, 0.3, "pop", t_out=t_levanta + 0.3, d_out=0.7, sale="baja", sem=20)
    A(R, O.alga(), (950, 1530, 0.8), t_mar + 0.85, 0.3, "pop", t_out=t_levanta + 0.3, d_out=0.7, sale="baja", sem=21)
    A(R, O.pez(), _pos_pez_salto, t_llega + 0.75, 0.01, "fija", t_out=t_llega + 1.65, d_out=0.01, sem=22,
      sfx=[("chapuzon", 0, 0.5, {"tono": 1.3})], sfx_out=[("plop", -0.05, 0.5, {"tono": 1.5})])
    # sol <-> luna: pasan los años (cada cambio es una transformación rápida)
    POS_SL = (880, 560, 1.0)
    ts0 = t_tres + 0.7
    forma = [O.sol(46), O.luna(), O.sol(46), O.luna()]
    prev = A(R, forma[0], POS_SL, ts0, 0.22, "pop", sem=50, sfx=[("tick", 0, 0.5)])
    for i in range(1, 4):
        nxt = A(R, forma[i], POS_SL, ts0 + 9, 0.1, "fija", sem=50 + i)
        M(prev, nxt, ts0 + 0.3 + 0.5 * (i - 1), 0.24, sfx=False)
        nxt["snd"] += [(ts0 + 0.3 + 0.5 * (i - 1), "morph", 0.45, {}), (ts0 + 0.54 + 0.5 * (i - 1), "tick", 0.5, {"tono": 1.0 + 0.15 * i})]
        prev = nxt
    prev["t_out"], prev["d_out"], prev["sale"] = ts0 + 0.3 + 0.5 * 2 + 0.24 + 0.45, 0.3, "encoger"
    # ---- sol grande y vapor
    A(R, SOL, (190, 700, 1.35), t_sol - 0.45, 0.7, "sube", dy=450, t_out=t_levanta + 0.3, d_out=0.7, sale="baja", sem=23,
      sfx=[("amanecer", 0, 0.7, {"dur": 1.6})])
    A(R, O.vapor(2, 200), (540, 1010, 1.0), t_calienta, 0.9, "pluma", t_out=t_levanta + 0.5, d_out=0.4, sale="borrar", sem=24,
      sfx=[("siseo", 0, 0.6, {"dur": 0.9})], sfx_out=[("borrar", 0, 0.4, {"dur": 0.3})], vida=2.6)
    # ---- cierre: se forma la nube y vuelve C0
    t_c = t_cielo + 2.7
    for k, (px, py, ps) in enumerate([(400, 720, 0.55), (610, 770, 0.55), (500, 660, 0.7)]):
        A(R, O.soplo(), (px, py, ps), t_cielo + 1.4 + 0.25 * k, 0.3, "pop", t_out=t_c, d_out=0.25, sem=60 + k,
          sfx=[("puf", 0, 0.6, {"tono": 1.0 + 0.1 * k})])
    A(R, O.nube_din, C0_NUBE, t_c, 0.55, "lt", sem=2, sfx=[("garabato", 0, 0.6, {"dur": 0.5}), ("pop", 0.5, 0.7, {"tono": 0.9})])
    A(R, SOL, C0_SOL, t_c + 0.7, 0.3, "pop", sem=1, sfx=[("brillo", 0, 0.6)])
    for k in range(9):                        # nueve días: nueve puntos que se cuentan
        A(R, O.gota("ninguno", "ninguna", False), (200 + 85 * k, 930, 0.32), t_nueve + 0.05 + 0.1 * k, 0.16, "pop",
          t_out=t_dias + 0.9, d_out=0.25, sem=70 + k, sfx=[("tick", 0, 0.4, {"tono": 1.0 + 0.06 * k})])
    A(R, O.flecha_circ(330), (540, 620, 1.0), t_vuelve, 0.55, "pluma", t_out=t_empezar + 0.5, d_out=0.45, sale="borrar", sem=80,
      sfx=[("garabato", 0, 0.6, {"dur": 0.55}), ("whoosh", 0.1, 0.5, {"dur": 0.6})], sfx_out=[("borrar", 0, 0.4, {"dur": 0.45})])
    return R


# ------------------------------------------------------------------ subtítulos manuscritos
PX_SUB = 64
ANCHO_SUB = 900


def _lineas(frase):
    palabras = [dict(w=w["w"].lower(), s=w["s"], e=w["e"]) for w in frase["words"]]
    lineas, cur, ancho = [], [], 0.0
    esp = B.ancho_texto(" ", PX_SUB)
    for w in palabras:
        aw = B.ancho_texto(w["w"], PX_SUB)
        if cur and ancho + esp + aw > ANCHO_SUB:
            lineas.append(cur)
            cur, ancho = [], 0.0
        cur.append((w, aw))
        ancho += aw + (esp if len(cur) > 1 else 0)
    if cur:
        lineas.append(cur)
    out = []
    n = len(lineas)
    for li, ln in enumerate(lineas):
        tot = sum(a for _, a in ln) + esp * (len(ln) - 1)
        x = W / 2 - tot / 2
        y = 1655 - (n - 1) * 46 + li * 92
        for w, aw in ln:
            out.append((w, x, y))
            x += aw + esp
    return out


_FR = [f for e in TL["escenas"] for f in e["frases"]]
# cada frase se ve hasta 0,9 s tras decirse, pero se desvanece antes de que empiece la siguiente (nunca se pisan)
SUBS = [(f, _lineas(f), min(f["t1"] + 0.9, (_FR[i + 1]["t0"] - 0.05) if i + 1 < len(_FR) else 1e9)) for i, f in enumerate(_FR)]


def dibujar_subs(h, t, fs):
    for f, pals, hasta in SUBS:
        ini = f["t0"] - 0.05
        if not (ini <= t < hasta):
            continue
        v = int(255 * (1 - prog(t, hasta - 0.25, hasta)))
        for w, x, y in pals:
            dur = max(w["e"] - w["s"], 0.16)
            u = prog(t, w["s"] - 0.03, w["s"] - 0.03 + dur)
            if u <= 0:
                continue
            m = B.mascara_texto(w["w"], PX_SUB)
            h.pegar_mascara(m, x - 4 + (fs - 1) * 0.6, y - 38 + (1.0 if fs == 1 else 0.0), cols=int(m.shape[1] * u), v=v)


def escribir(h, txt, x, y, px, u, fs, v=255, tv=0.0):
    """Rotula `txt` centrado en (x, y), escribiéndose de izquierda a derecha (u 0..1); se mece siempre (nada queda quieto)."""
    if u <= 0 or v <= 0:
        return
    m = B.mascara_texto(txt, px)
    mx = 3.0 * math.sin(2 * B.OMEGA * tv + x * 0.01)
    my = 5.0 * math.sin(B.OMEGA * tv * 3 + y * 0.013)
    h.pegar_mascara(m, x - m.shape[1] / 2 + (fs - 1) * 0.7 + mx, y - m.shape[0] / 2 + my, cols=m.shape[1] * min(1.0, u), v=v)


# ------------------------------------------------------------------ el mundo
class Mundo(Escena):
    def preparar(self):
        self.h = B.Hoja()
        self.actores = construir_actores()
        self.pases = construir_pases()
        self.pases.sort(key=lambda p: p[0])
        self.exprs = construir_exprs()
        self.fs = 0
        self.te = 0.0
        if self.idx == 0:
            self.sonidos()

    # ---- sonido: un efecto por cada movimiento
    def sonidos(self):
        e = self.ev
        for a in self.actores:
            for t, n, vol, kw in a["snd"]:
                e(t, n, vol, **kw)
        e(t_gota, "boing", 0.7, tono=1.1)
        e(t_vueltas + 0.05, "whoosh", 0.45, dur=0.6, tono=1.2)
        e(t_millones - 0.1, "escribir", 0.6, dur=0.9)
        e(t_nunca, "boing", 0.6, tono=0.9)
        e(t_land_plan, "golpe_suave", 0.7)
        e(t_cae - 0.02, "gota", 0.8)
        e(t_cae + 0.3, "whoosh", 0.35, dur=0.5, tono=1.3)
        e(t_cae + 0.1, "lluvia", 0.5, dur=INI("hielo") - t_cae)
        e(t_land_mont, "golpe_suave", 0.9)
        e(t_land_mont, "plop", 0.6, tono=1.2)
        for k in range(4):
            e(t_land_mont + 0.08 * k, "gota", 0.4, pan=-0.3 + 0.2 * k, tono=1.0 + 0.1 * k)
        e(INI("hielo") - 1.4, "viento", 0.4, dur=1.3)
        e(INI("hielo") - 0.6, "brr", 0.7)
        e(INI("hielo") + 0.2, "boing", 0.6, tono=0.9)
        e(t_glaciar, "brillo", 0.6)
        e(t_derrite, "siseo", 0.35, dur=0.9)
        for k in range(5):
            e(t_derrite + 0.15 + 0.2 * k, "gota", 0.5, pan=0.1 * k - 0.2, tono=0.9 + 0.08 * k)
        e(t_derrite + 0.55, "boing", 0.6)
        for k in range(5):
            e(t_apenas + 0.25 * k + 0.03, "tick", 0.45, tono=1.0 + 0.1 * k)
        e(t_termina, "gota", 0.8)
        e(t_vaso_p + 0.05, "whoosh", 0.3, dur=0.4, tono=1.5)
        e(t_vaso_p + 0.5, "plop", 0.85)
        e(t_gm0, "whoosh", 0.3, dur=0.4)
        for k in range(3):
            e(t_gm1 + 0.14 + 0.16 * k, "glug", 0.8, tono=1.0 - 0.1 * k)
        e(t_bebe + 0.1, "pop", 0.5, tono=0.8)
        e(t_sigue, "whoosh", 0.55, dur=0.6)
        e(t_sigue, "garabato", 0.4, dur=0.8)
        e(t_sigue + 0.3, "viento", 0.35, dur=1.2)
        e(t_final - 0.7, "whoosh", 0.4, dur=0.6, tono=0.9)
        e(t_llega + 0.5, "chapuzon", 1.0)
        e(t_llega + 0.5, "plop", 0.6, tono=0.7)
        e(t_quedarse + 0.2, "ronca", 0.5)
        e(t_quedarse + 1.2, "ronca", 0.5, tono=0.9)
        e(t_tres, "escribir", 0.6, dur=0.9)
        e(t_calienta, "brr", 0.4)
        for k in range(3):
            e(t_calienta + 0.05 + 0.15 * k, "gota", 0.55, tono=1.2)
        e(t_levanta - 0.05, "whoosh", 0.55, dur=0.9, tono=1.3)
        e(t_levanta + 0.3, "whoosh", 0.4, dur=0.7, tono=0.8)
        e(t_aterriza, "golpe_suave", 0.8)
        e(t_aterriza, "pop", 0.7, tono=1.1)
        e(t_empezar - 0.05, "boing", 0.65, tono=1.2)
        e(t_empezar + 0.3, "brillo", 0.7, tono=1.3)

    # ---- actores
    def actor(self, a, t):
        if t < a["t_in"]:
            return
        pos = a["pos"](t) if callable(a["pos"]) else a["pos"]
        x, y, s = pos[0], pos[1], pos[2]
        rot = pos[3] if len(pos) > 3 else a["rot"]
        v = prog(t, a["t_in"], a["t_in"] + a["d_in"])
        u, sq, lap, ent = 1.0, 0.0, 0.0, a["entra"]
        if ent == "pluma":
            u = v
        elif ent == "lt":
            tp = 0.14
            u = prog(t, a["t_in"] + tp, a["t_in"] + tp + a["d_in"])
            lap = 1 - u
        elif ent == "pop":
            s *= e_back(v, 2.2)
            sq = 0.25 * (1 - v) * math.sin(v * 11)
            if s < 0.02:
                return
        elif ent == "sube":
            y += a["dy"] * (1 - e_out(v))
        elif ent == "izq":
            x -= a["dx"] * (1 - e_out(v))
        elif ent == "cae":
            hh, sq = rebote(v)
            y -= a["dy"] * hh
        if a["t_out"] is not None and t > a["t_out"]:
            if a["sale"] == "cortar":
                return
            uo = prog(t, a["t_out"], a["t_out"] + a["d_out"])
            if uo >= 1:
                return
            m = a["sale"]
            if m == "borrar":
                u = min(u, 1 - uo)
            elif m == "caer":
                y += 1500 * e_in(uo)
                rot += 0.7 * uo
            elif m == "encoger":
                s *= 1 - e_in(uo)
            elif m == "baja":
                y += 1300 * e_in(uo)
            elif m == "sube_fuera":
                y -= 1300 * e_in(uo)
            elif m == "izq_fuera":
                x -= 1300 * e_in(uo)
        d = a["d"](self.te) if callable(a["d"]) else a["d"]
        d.dibujar(self.h, x, y, s, rot, a["flip"], u, self.fs, a["sem"], sq=sq, lapiz=lap, tv=self.te, vida=a["vida"])

    def mascota(self, t):
        ps = self.pases
        if t < ps[0][0]:
            return ps[0][2](ps[0][0])
        k = max(i for i, p in enumerate(ps) if p[0] <= t)
        t0, t1, fn = ps[k]
        return fn(min(t, t1))

    def expr(self, t):
        e = self.exprs[0]
        for x in self.exprs:
            if x[0] <= t:
                e = x
        return e[1], e[2]

    # ---- cuadro
    def render(self, lz, t):
        h = self.h
        h.limpiar()
        te = 0.0 if t >= FIN_CUADRO else t          # tiempo "de reposo" (temblor, parpadeo): el último cuadro = el primero
        self.fs = B.fase(te)
        self.te = te
        for a in self.actores:
            self.actor(a, t)
        for m in MORFS:
            if m["t0"] <= t < m["t0"] + m["dur"]:
                self.morf(m, t)
        self.dinamicos(t, te)
        self.dibujar_gota(t, te)
        dibujar_subs(h, t, self.fs)
        return np.clip(h.componer(), 0, 1)

    def morf(self, m, t):
        """Cuadro de la transformación m['a'] -> m['b'] (ver `M`)."""
        def estado(sp):
            pos = sp["pos"](t) if callable(sp["pos"]) else sp["pos"]
            return dict(x=pos[0], y=pos[1], s=pos[2], rot=pos[3] if len(pos) > 3 else sp["rot"], flip=sp["flip"])

        def dib(sp):
            return sp["d"](self.te) if callable(sp["d"]) else sp["d"]
        k = (t - m["t0"]) / m["dur"]
        B.morfosis(self.h, dib(m["a"]), estado(m["a"]), dib(m["b"]), estado(m["b"]), k, self.fs, m["b"]["sem"], tv=self.te,
                   vida=m["b"]["vida"])

    def gota_dib(self, x, y, s, rot, ojos, boca, sq=0.0):
        if s < 0.03:
            return
        mira = int(round(1.2 * math.sin(B.OMEGA * self.te + 1.0)))          # mira a los lados
        O.gota(ojos, boca, True, False, mira).dibujar(self.h, x, y, s, rot, False, 1.0, self.fs, 0, sq=sq, tv=self.te, vida=0.8)

    def dibujar_gota(self, t, te):
        x, y, s, rot = self.mascota(t)
        ojos, boca = self.expr(t)
        if ojos == "abiertos" and ((te + 1.0) % 3.1) < 0.13:          # parpadeo cada 3,1 s
            ojos = "cerrados"
        y += 3.0 * math.sin(te * 2 * math.pi / 1.7)                    # balanceo de reposo
        if INI("hielo") - 0.6 < t < INI("hielo") + 0.15 or t_congela + 0.3 < t < t_derrite + 0.1:   # tiembla de frío
            x += (1 if self.fs == 1 else -1) * 3.0
        if t_calienta < t < t_calienta + 0.8:
            x += (1 if self.fs == 2 else -1) * 2.0
        self.gota_dib(x, y, s, rot, ojos, boca, squash_gota(t) + 0.045 * math.sin(2 * B.OMEGA * te + 0.6))
        u_b = min(prog(t, t_tres, t_tres + 0.9), 1 - prog(t, t_calienta, t_calienta + 0.6))
        if u_b > 0:
            O.barba().dibujar(self.h, x, y, s, rot, False, u_b, self.fs, 21, tv=te, vida=1.2)

    # ---- elementos dinámicos (física y rótulos)
    def dinamicos(self, t, te):
        h, fs = self.h, self.fs
        u = prog(t, t_millones - 0.1, t_millones + 0.75)
        escribir(h, "+4.000.000.000", 540, 1075, 96, u, fs, int(255 * (1 - prog(t, t_vueltas + 0.5, t_vueltas + 0.9))), te)
        # lluvia
        a, b = t_cae + 0.1, INI("hielo") - 0.05
        if a <= t <= b:
            kk = smooth(prog(t, a, a + 0.4)) * (1 - smooth(prog(t, b - 0.35, b)))
            mx, my = self.mascota(t)[:2]
            for i in range(15):
                x = 330 + i * 34 + 9 * math.sin(i * 2.1)
                f = (te * 1.1 + (i * 0.37) % 1.0) % 1.0
                y0 = 880 + f * 190
                L = 46 * kk
                if L < 4 or (abs(x - mx) < 78 and abs(y0 + 20 - my) < 130):
                    continue
                h.trazo(np.array([(x, y0), (x - 10, y0 + L)]), 4.2, 100 + i, fs, 1.0, amp=1.0, v=235)
        self.salpicadura(t, t_land_mont, 470, 1000, 7, 0.65, 95)
        # copitos de nieve que caen antes de congelarse
        for k in range(4):
            t0 = INI("hielo") - 1.6 + 0.3 * k
            if t0 <= t < INI("hielo") + 0.4:
                uu = (t - t0) / 1.4
                O.copo(24).dibujar(h, 260 + 180 * k + 30 * math.sin(uu * 7 + k), 700 + 620 * uu, 1.0, 0.2 * k + 3 * uu, False, 1.0,
                                   fs, 90 + k)
        # gotas del deshielo
        for k in range(5):
            t0 = t_derrite + 0.15 + 0.2 * k
            if t0 <= t < t0 + 0.55:
                uu = (t - t0) / 0.55
                O.gota("ninguno", "ninguna", False).dibujar(h, 480 + 30 * k, 1090 + 130 * uu * uu, 0.26, 0, False, 1.0, fs, 95 + k)
        # meses
        for k, m in enumerate(("ene", "feb", "mar", "abr", "may")):
            t0 = t_apenas + 0.25 * k
            if t0 <= t < t_meses + 0.7:
                escribir(h, m, 890 - 25 * (k % 2), 560 + 120 * k, 74, prog(t, t0, t0 + 0.18), fs,
                         int(255 * (1 - prog(t, t_meses + 0.4, t_meses + 0.7))), te)
        # manecillas del reloj (giran rápido)
        if t_decadas + 0.3 <= t < t_derrite - 0.4:
            for lon, vel, w in ((60, 9.0, 5.0), (40, 0.75, 6.0)):
                ang = -math.pi / 2 + (t - t_decadas) * vel * math.pi
                h.trazo(np.array([(900, 1300), (900 + lon * math.cos(ang), 1300 + lon * math.sin(ang))]), w, 111, fs, 1.0, amp=0.8)
        # gotas de sudor al calentarse
        for k in range(3):
            t0 = t_calienta + 0.05 + 0.15 * k
            if t0 <= t < t0 + 0.6:
                uu = (t - t0) / 0.6
                mx, my = self.mascota(t)[:2]
                O.gota("ninguno", "ninguna", False).dibujar(h, mx + (-95 + 95 * k) - 20 * uu * (k - 1), my - 20 + 110 * uu * uu, 0.2,
                                                          0.0, False, 1.0, fs, 100 + k)
        # mar: anillos, salpicadura, "3000" y zzz
        for i in range(3):
            tt = t - (t_llega + 0.5) - 0.18 * i
            if 0 < tt < 1.1:
                uu = tt / 1.1
                r = 40 + 260 * e_out(uu)
                h.trazo(B.elip(540, 1050, r, r * 0.22, vuelta=1.0, n=36), 4.0 * (1 - uu * 0.5), 200 + i, fs, 1.0, amp=1.2,
                        v=int(255 * (1 - uu)))
        self.salpicadura(t, t_llega + 0.5, 540, 1030, 9, 0.7, 150)
        u = prog(t, t_tres - 0.1, t_tres + 0.7) * (1 - prog(t, t_sol - 0.2, t_sol + 0.2))
        escribir(h, "3000", 540, 430, 250, u, fs, int(255 * min(1.0, u * 4)), te)
        for k in range(3):
            ts = t_quedarse + 0.2 + 0.55 * k
            if ts <= t < t_calienta:
                uu = prog(t, ts, ts + 0.9)
                escribir(h, "z", 650 + 40 * k + 10 * math.sin(t * 2), 1120 - 55 * k - 30 * uu, 46 + 16 * k, 1.0, fs,
                         int(255 * (1 - uu * 0.4)), te)
        self.agua(t, te)
        self.punteado(t)

    def agua(self, t, te):
        """Agua que siempre corre: rayas que avanzan por el río y olas que viajan por el mar."""
        h, fs, w = self.h, self.fs, B.OMEGA
        u_r = _u_rio(t)
        if t_baja + 0.5 < t < t_meses + 0.6 and u_r > 0.3:
            k = 1 - prog(t, t_meses + 0.35, t_meses + 0.6)
            for i in range(9):
                uu = (te * 0.27 + i / 9.0) % 1.0
                if uu > u_r - 0.04:
                    continue
                p, q = O.punto_rio(uu), O.punto_rio(min(1.0, uu + 0.025))
                a = (RIO_TF[0] + p[0] * RIO_TF[2], RIO_TF[1] + p[1] * RIO_TF[2])
                b = (RIO_TF[0] + q[0] * RIO_TF[2], RIO_TF[1] + q[1] * RIO_TF[2])
                h.trazo(np.array([a, b]), 4.0, 400 + i, fs, 1.0, amp=1.0, v=int(200 * k))
        t_m = t_camino + 1.4
        uo = prog(t, t_levanta + 0.3, t_levanta + 1.0)
        if t_m + 0.7 < t and uo < 1:
            dy = 1300 * e_in(uo) + 700 * (1 - e_out(prog(t, t_m, t_m + 0.9)))
            for j, (yy, x0) in enumerate(((1075, 0), (1165, 90), (1260, 20), (1350, 140), (1440, 60))):
                for k in range(5):
                    x = (x0 + k * 230 + 60 * math.sin(w * te + j) + 45 * te * (1 if j % 2 else -1)) % 1200 - 60
                    xs = np.linspace(x, x + 110, 12)
                    ys = yy + dy + 9 * np.sin(xs / 58.0 + 2 * w * te + j * 1.3)
                    h.trazo(np.stack([xs, ys], 1), 3.6, 500 + j * 7 + k, fs, 1.0, amp=0.8, v=170)

    def salpicadura(self, t, t0, x, y, n, dur, alt):
        if not (t0 <= t < t0 + dur):
            return
        u = (t - t0) / dur
        for k in range(n):
            a = math.pi * (0.1 + 0.8 * k / (n - 1))
            r = alt * e_out(u)
            self.h.punto(x + r * math.cos(a) * 1.3, y - r * math.sin(a) + 90 * u * u, 4.5 * (1 - u) + 1.5, k + 7, self.fs,
                         v=int(255 * (1 - 0.6 * u)))

    def punteado(self, t):
        """Línea de puntos que va marcando el camino de la gota (del aliento hasta el mar)."""
        a, b = t_sigue, t_llega - 0.1
        if not (a <= t < b + 0.3):
            return
        P = camino_punteado()
        seg = np.hypot(*np.diff(P, axis=0).T)
        d = np.concatenate([[0.0], np.cumsum(seg)])
        L = d[-1] * (0.72 * prog(t, a, a + 1.0) + 0.28 * prog(t, t_final - 0.7, t_final + 0.05))
        v = int(255 * (1 - prog(t, b, b + 0.3)))
        s0 = 0.0
        while s0 < L:
            s1 = min(s0 + 24, L)
            xs = np.interp([s0, s1], d, P[:, 0])
            ys = np.interp([s0, s1], d, P[:, 1])
            self.h.trazo(np.stack([xs, ys], 1), 4.5, 300 + int(s0), self.fs, 1.0, amp=0.8, v=v)
            s0 += 44


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
