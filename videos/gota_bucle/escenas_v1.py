# -*- coding: utf-8 -*-
"""'El viaje de una gota' — estilo boceto, formato vertical, animación en BUCLE.

Una sola clase (`Mundo`) dibuja todo en función del tiempo global: cada elemento se dibuja trazo a trazo (`Dib`),
se borra/cae/encoge al terminar su escena y la gota mascota viaja entre escenas (pases). El último cuadro es idéntico
al primero: nube + sol + gota (composición C0) y la fase del temblor/parpadeo se reinicia en el cuadro final.
"""
import math
import types

import numpy as np

import boceto as B
import objetos as O
from escena_base import *  # noqa: F401,F403
from motor import H, W, e_in, e_inout, e_out, lerp, prog, smooth

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]
FIN_CUADRO = TOTAL - 1.5 / 30      # desde aquí el temblor y el parpadeo vuelven a la fase 0 (= primer cuadro)


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


# ------------------------------------------------------------------ anclas
C0_NUBE = (560, 720, 1.2)
C0_SOL = (170, 470, 1.0)
C0_GOTA = (620, 410, 1.0)
PEAK = (470, 992)

t_mont = INI("montana") - 0.25          # dibujar montaña
t_cae = T("montana", "cae")
t_aterriza = t_cae + 1.05
t_hielo = INI("hielo") - 0.45           # borrar cielo y montaña
t_congela = T("hielo", "congela")
t_decadas = T("hielo", "decadas")
t_rio = INI("rio") - 0.5                # se funde el hielo
t_rio_dib = INI("rio") - 0.15
t_ride0 = t_rio_dib + 1.0
t_ride1 = INI("vaso") - 0.45
t_vaso = INI("vaso") - 0.3
t_forma = INI("vaso") + 0.75
t_cae_v = T("vaso", "vaso") - 0.15
t_luego = T("vaso", "luego")
t_ti = T("vaso", "ti")
t_devuelves = T("vaso", "devuelves")
t_camino = T("vaso", "camino")
t_bebe_fin = t_ti + 1.45
t_mar = INI("mar") - 0.35
t_llega = T("mar", "llega") - 0.1
t_tres = T("mar", "tres")
t_sol_ini = INI("sol") - 0.3
t_calienta = T("sol", "calienta")
t_levanta = T("sol", "levanta")
t_cierre = INI("cierre") - 0.4

GLASS_A = (713, 1040, 1.0, 0.0)
GLASS_B = (392, 1195, 0.62, -0.95)
t_gm0 = t_ti - 0.55
t_gm1 = t_ti + 0.15
PERSONA = (270, 1170, 0.85)
MOUTH = (270, 1238)


# ------------------------------------------------------------------ pases de la gota
def pase(t0, t1, p0, p1, s0, s1, h=0.0, ease="inout", rot=0.0):
    """Movimiento de la gota entre dos puntos (con salto de altura h). Devuelve fn(t) -> (x, y, s, rot)."""
    def fn(t):
        u = prog(t, t0, t1)
        k = e_inout(u) if ease == "inout" else (e_in(u) if ease == "in" else e_out(u) if ease == "out" else u)
        return (lerp(p0[0], p1[0], u if ease == "in" else k), lerp(p0[1], p1[1], k) - h * math.sin(math.pi * u),
                lerp(s0, s1, k), rot * math.sin(math.pi * u))
    return fn


def vaso_tf(t):
    k = smooth(prog(t, t_gm0, t_gm1))
    return (lerp(GLASS_A[0], GLASS_B[0], k), lerp(GLASS_A[1], GLASS_B[1], k), lerp(GLASS_A[2], GLASS_B[2], k),
            lerp(GLASS_A[3], GLASS_B[3], k))


def nivel_agua(t):
    n = 0.32 + 0.38 * smooth(prog(t, t_cae_v + 0.42, t_cae_v + 1.3))
    return n - 0.66 * smooth(prog(t, t_gm1 + 0.15, t_gm1 + 1.2))


RIO_TF = (540, 900, 0.9)


def rio_a_pantalla(v, dy=0.0):
    p = O.punto_rio(v)
    return RIO_TF[0] + p[0] * RIO_TF[2], RIO_TF[1] + p[1] * RIO_TF[2] + dy


def _v_rio(t):
    u_r = prog(t, t_rio_dib, t_rio_dib + 2.2)
    return min(smooth(prog(t, t_ride0, t_ride1)) * 0.995, max(0.0, u_r - 0.1))


def construir_pases():
    P = []
    g0 = C0_GOTA

    def salto_nube(t):                      # sale de la nube por la derecha y cae sobre el pico
        u = prog(t, t_cae, t_aterriza)
        if u < 0.45:
            v = u / 0.45
            return (lerp(g0[0], 985, e_out(v)), lerp(g0[1], 380, e_out(v)) - 120 * math.sin(math.pi * v), 1.0, 0.0)
        v = (u - 0.45) / 0.55
        return (lerp(985, PEAK[0], e_inout(v)), lerp(380, PEAK[1] - 20, e_in(v)), lerp(1.0, 0.8, v), 0.0)
    P.append((t_cae - 0.1, t_aterriza, salto_nube))
    P.append((t_hielo + 0.1, t_hielo + 0.75,
              pase(t_hielo + 0.1, t_hielo + 0.75, (PEAK[0], PEAK[1] - 20), (540, 900), 0.8, 1.0, 130, rot=0.3)))
    r0 = rio_a_pantalla(0.0, -40)
    P.append((t_rio + 0.1, t_rio + 0.7, pase(t_rio + 0.1, t_rio + 0.7, (540, 900), r0, 1.0, 0.62, 120, rot=-0.3)))

    def rio_(t):
        x, y = rio_a_pantalla(_v_rio(t), -40)
        return x, y + 3 * math.sin(t * 5), 0.62, 0.07 * math.sin(t * 3.0)
    P.append((t_ride0, t_ride1, rio_))
    fin_rio = rio_a_pantalla(0.995, -40)
    P.append((t_ride1 + 0.05, t_ride1 + 0.4, pase(t_ride1 + 0.05, t_ride1 + 0.4, fin_rio, fin_rio, 0.62, 0.02, 0, "lin")))
    SP = (713, 545)
    P.append((t_forma, t_forma + 0.5, pase(t_forma, t_forma + 0.5, SP, SP, 0.02, 0.55, 0, "lin")))
    P.append((t_cae_v, t_cae_v + 0.5, pase(t_cae_v, t_cae_v + 0.5, SP, (713, 1055), 0.55, 0.5, 0, "in")))

    def en_vaso(t):
        gx, gy, gs, gr = vaso_tf(t)
        q = B.transformar([(0.0, 130 - 250 * nivel_agua(t) - 15)], gx, gy, gs, gr)[0]
        return q[0], q[1], 0.5 * gs, gr * 0.6 + 0.05 * math.sin(t * 4)
    t_bebe = t_ti + 1.0
    P.append((t_cae_v + 0.5, t_bebe, en_vaso))
    q = en_vaso(t_bebe)
    P.append((t_bebe, t_bebe + 0.45, pase(t_bebe, t_bebe + 0.45, q[:2], MOUTH, q[2], 0.02, 20, "lin")))
    SOP = (MOUTH[0] + 190, MOUTH[1] - 190)
    P.append((t_devuelves + 0.2, t_devuelves + 0.65,
              pase(t_devuelves + 0.2, t_devuelves + 0.65, SOP, SOP, 0.02, 0.5, 0, "lin")))
    P.append((t_camino, t_camino + 0.9, pase(t_camino, t_camino + 0.9, SOP, (900, 330), 0.5, 0.9, 150, rot=0.3)))
    P.append((t_llega, t_llega + 0.75, pase(t_llega, t_llega + 0.75, (900, 330), (540, 1040), 0.9, 1.0, 0, "in")))
    P.append((t_llega + 0.75, t_llega + 1.6, pase(t_llega + 0.75, t_llega + 1.6, (540, 1040), (540, 1200), 1.0, 1.0, 0, "out")))
    P.append((t_levanta - 0.1, t_levanta + 1.6,
              pase(t_levanta - 0.1, t_levanta + 1.6, (540, 1200), (540, 640), 1.0, 0.95, 0)))
    P.append((t_cierre + 0.9, t_cierre + 2.0,
              pase(t_cierre + 0.9, t_cierre + 2.0, (540, 640), C0_GOTA[:2], 0.95, 1.0, 90, rot=-0.2)))
    return P


def construir_exprs():
    return [(-10, "abiertos", "sonrisa"), (t_cae, "miedo", "o"), (t_aterriza + 0.05, "abiertos", "o"),
            (t_aterriza + 0.9, "abiertos", "sonrisa"), (t_congela, "miedo", "zigzag"), (t_rio + 0.3, "feliz", "abierta"),
            (t_ride1, "abiertos", "sonrisa"), (t_cae_v, "miedo", "o"), (t_cae_v + 0.6, "feliz", "sonrisa"),
            (t_devuelves + 0.3, "abiertos", "sonrisa"), (t_llega, "miedo", "o"), (t_llega + 0.8, "abiertos", "o"),
            (T("mar", "quedarse") - 0.2, "cerrados", "ronca"), (INI("sol") + 0.2, "abiertos", "sonrisa"),
            (t_levanta, "feliz", "abierta"), (t_cierre + 2.0, "abiertos", "sonrisa")]


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


SUBS = [(f, _lineas(f)) for e in TL["escenas"] for f in e["frases"]]


def dibujar_subs(h, t, fs):
    for f, pals in SUBS:
        ini = f["t0"] - 0.05
        fin = f["t1"] + 0.6
        if not (ini <= t < fin + 0.35):
            continue
        v = int(255 * (1 - prog(t, fin, fin + 0.3)))
        dy = (1 if fs == 1 else 0) * 1.0
        for w, x, y in pals:
            dur = max(w["e"] - w["s"], 0.16)
            u = prog(t, w["s"] - 0.03, w["s"] - 0.03 + dur)
            if u <= 0:
                continue
            m = B.mascara_texto(w["w"], PX_SUB)
            h.pegar_mascara(m, x - 4 + (fs - 1) * 0.6, y - 38 + dy, cols=int(m.shape[1] * u), v=v)


# ------------------------------------------------------------------ el mundo
class Mundo(Escena):
    def preparar(self):
        self.h = B.Hoja()
        self.pases = construir_pases()
        self.pases.sort(key=lambda p: p[0])
        self.exprs = construir_exprs()
        self.fs = 0
        if self.idx == 0:
            self.sonidos()

    # ---- sonido
    def sonidos(self):
        e = self.ev
        e(t_mont, "pincel", 0.8, dur=1.5)
        e(t_cae + 0.1, "whoosh", 0.5, dur=0.5)
        e(t_aterriza, "pop", 0.8, tono=0.9)
        for k in range(5):
            e(t_cae + 0.4 + 0.5 * k, "burbuja", 0.25, pan=-0.4 + 0.2 * k)
        e(t_hielo, "whoosh", 0.4, dur=0.6)
        e(t_congela, "hielo", 0.9)
        e(t_decadas, "tick", 0.5)
        for k in range(4):
            e(t_decadas + 0.3 + 0.45 * k, "tick", 0.35, pan=-0.3)
        e(t_rio, "puf", 0.5)
        e(t_rio_dib, "pincel", 0.8, dur=2.2)
        e(t_ride0, "ola", 0.4, dur=2.5)
        e(t_vaso, "pincel", 0.7, dur=1.2)
        e(t_forma, "burbuja", 0.7)
        e(t_cae_v + 0.4, "chapuzon", 0.9)
        e(t_ti + 0.3, "burbuja", 0.7)
        e(t_ti + 0.9, "burbuja", 0.5, tono=0.8)
        e(t_devuelves + 0.1, "puf", 0.9)
        e(t_camino, "whoosh", 0.6, dur=0.6)
        e(t_mar, "pincel", 0.7, dur=1.4)
        e(t_llega + 0.7, "chapuzon", 1.0)
        e(t_tres, "escribir", 0.7)
        e(t_sol_ini + 0.2, "amanecer", 0.7)
        e(t_calienta, "viento", 0.5, dur=1.5)
        e(t_cierre + 0.1, "pincel", 0.8, dur=1.6)
        e(t_cierre + 2.0, "pop", 0.8, tono=1.1)
        e(t_cierre + 2.1, "brillo", 0.8)

    # ---- utilidades de dibujo
    def act(self, d, x, y, s, t, t_in, d_in, t_out=None, d_out=0.7, modo="borrar", rot=0.0, flip=False, sem=0, u_max=1.0):
        u = prog(t, t_in, t_in + d_in) * u_max
        if u <= 0:
            return
        if t_out is not None and t > t_out:
            uo = prog(t, t_out, t_out + d_out)
            if uo >= 1:
                return
            if modo == "borrar":
                u = min(u, 1 - uo)
            elif modo == "caer":
                y += 1500 * e_in(uo)
                rot += 0.7 * uo
            elif modo == "encoger":
                s *= 1 - e_in(uo)
        d.dibujar(self.h, x, y, s, rot, flip, u, self.fs, sem)

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
        fs = self.fs

        # --- cielo C0 (inicio) y su retirada
        self.act(O.sol(76), *C0_SOL, t, -10, 0.1, t_out=t_hielo, d_out=0.7, sem=1)
        self.act(O.nube(), *C0_NUBE, t, -10, 0.1, t_out=t_hielo, d_out=0.7, sem=2)
        # --- montaña + lluvia
        self.act(O.montana(), 540, 1440, 0.95, t, t_mont, 1.5, t_out=t_hielo, d_out=0.7, sem=3)
        self.lluvia(t, te)
        # --- hielo, copo, marcas
        self.act(O.bloque_hielo(), 540, 905, 1.5, t, t_congela - 0.2, 1.1, t_out=t_rio, d_out=0.9, modo="encoger", sem=4)
        self.act(O.copo(70), 210, 600, 1.3, t, t_congela + 0.1, 1.0, t_out=t_rio, d_out=0.9, modo="caer", sem=5, rot=0.0)
        self.act(O.copo(70), 880, 680, 0.8, t, t_congela + 0.5, 0.8, t_out=t_rio, d_out=0.9, modo="caer", sem=6)
        self.act(O.marcas(20), 260, 1250, 1.0, t, t_decadas - 0.2, 2.2, t_out=t_rio, d_out=0.7, sem=7)
        # --- río y barquita
        self.act(O.rio(), *RIO_TF, t, t_rio_dib, 2.2, t_out=t_ride1 + 0.05, d_out=0.9, sem=8)
        if t_ride0 - 0.1 <= t < t_ride1 + 0.9:
            x, y, s_, r_ = self.mascota(min(t, t_ride1))
            self.act(O.hoja_barca(), x, y + 34, 0.72, t, t_ride0 - 0.1, 0.4, t_out=t_ride1, d_out=0.6, modo="borrar", rot=r_, sem=9)
        # --- grifo, vaso, persona, aliento
        self.escena_vaso(t)
        # --- mar
        self.escena_mar(t, te)
        # --- sol y vapor
        self.escena_sol(t)
        # --- cierre: C0 se vuelve a dibujar
        self.act(O.nube(), *C0_NUBE, t, t_cierre + 0.1, 1.7, sem=2)
        self.act(O.sol(76), *C0_SOL, t, t_cierre + 0.9, 1.1, sem=1)
        # --- la gota mascota (siempre encima)
        self.dibujar_gota(t, te)
        # --- subtítulos
        dibujar_subs(h, t, fs)
        return np.clip(h.componer(), 0, 1)

    def gota_dib(self, x, y, s, rot, t, ojos, boca, u=1.0, mej=True):
        if s < 0.03:
            return
        O.gota(ojos, boca, mej).dibujar(self.h, x, y, s, rot, False, u, self.fs, 0)

    def dibujar_gota(self, t, te):
        x, y, s, rot = self.mascota(t)
        ojos, boca = self.expr(t)
        if ojos == "abiertos" and ((te + 1.0) % 3.1) < 0.13:          # parpadeo cada 3,1 s
            ojos = "cerrados"
        y += 3.0 * math.sin(te * 2 * math.pi / 1.7)                    # balanceo de reposo
        if t_congela + 0.3 < t < t_rio:                                # tiembla de frío dentro del hielo
            x += (1 if self.fs == 1 else -1) * 3.0
        self.gota_dib(x, y, s, rot, t, ojos, boca)
        u_b = min(prog(t, t_tres, t_tres + 2.3), 1 - prog(t, INI("sol") + 0.1, INI("sol") + 0.9))
        if u_b > 0:
            O.barba().dibujar(self.h, x, y, s, rot, False, u_b, self.fs, 21)

    def lluvia(self, t, te):
        a, b = INI("montana") + 0.2, t_hielo + 0.3
        if not (a <= t <= b):
            return
        kk = smooth(prog(t, a, a + 0.5)) * (1 - smooth(prog(t, b - 0.4, b)))
        mx, my = self.mascota(t)[:2]
        for i in range(15):
            x = 330 + i * 34 + 9 * math.sin(i * 2.1)
            f = (te * 1.1 + (i * 0.37) % 1.0) % 1.0
            y0 = 880 + f * 190
            L = 46 * kk
            if L < 4 or (abs(x - mx) < 78 and abs(y0 + 20 - my) < 130):      # la lluvia no cruza a la gota
                continue
            self.h.trazo(np.array([(x, y0), (x - 10, y0 + L)]), 4.2, 100 + i, self.fs, 1.0, amp=1.0, v=235)

    def escena_vaso(self, t):
        h = self.h
        t_out = t_mar
        self.act(O.grifo(), 700, 430, 1.0, t, t_vaso, 1.0, t_out=t_out, d_out=0.8, sem=10)
        gx, gy, gs, gr = vaso_tf(t)
        self.act(O.vaso(), gx, gy, gs, t, INI("vaso") + 0.15, 0.9, t_out=t_bebe_fin, d_out=0.5, rot=gr, sem=11)
        if INI("vaso") + 0.9 < t < t_out + 0.8:
            n = nivel_agua(t)
            pol = O.agua_poli(max(n, 0.0))
            if pol is not None:
                uo = prog(t, t_bebe_fin, t_bebe_fin + 0.5)
                if uo < 1:
                    Pp = B.transformar(pol, gx, gy, gs, gr)
                    h.relleno(Pp, B.AZUL, 12, self.fs, min(1.0, prog(t, INI("vaso") + 0.4, INI("vaso") + 1.0)) * (1 - uo), sp=10, ang=20)
        self.act(O.persona("sonrisa"), *PERSONA, t, t_luego - 0.2, 1.1, t_out=t_out, d_out=0.8, sem=13)
        # aliento con la gota dentro
        self.act(O.soplo(), MOUTH[0] + 200, MOUTH[1] - 195, 0.9, t, t_devuelves, 0.7, t_out=t_out, d_out=0.8, sem=14)

    def escena_mar(self, t, te):
        t_out = t_cierre
        self.act(O.mar_capa(1010, 530, B.AZUL_CL, ph=0.5), 0, 0, 1.0, t, t_mar, 1.3, t_out=t_out, d_out=0.9, sem=15)
        self.act(O.mar_capa(1120, 420, B.AZUL, ph=2.0), 0, 0, 1.0, t, t_mar + 0.25, 1.3, t_out=t_out, d_out=0.9, sem=16)
        self.act(O.pez(), 300 + 35 * math.sin(t * 0.8), 1360, 0.8, t, t_mar + 1.2, 0.8, t_out=t_out, d_out=0.7, sem=17)
        self.act(O.pez(), 830 + 30 * math.sin(t * 0.7 + 1), 1430, 0.6, t, t_mar + 1.5, 0.8, t_out=t_out, d_out=0.7, flip=True, sem=18)
        self.act(O.alga(), 130, 1530, 0.9, t, t_mar + 0.9, 0.8, t_out=t_out, d_out=0.7, sem=19)
        self.act(O.alga(), 950, 1530, 0.8, t, t_mar + 1.1, 0.8, t_out=t_out, d_out=0.7, sem=20)
        # salpicadura
        tl = t_llega + 0.75
        if tl <= t < tl + 0.7:
            u = prog(t, tl, tl + 0.7)
            for k in range(7):
                a = math.pi * (0.12 + 0.76 * k / 6)
                r0, r1 = 30 + 90 * e_out(u), 60 + 140 * e_out(u)
                self.h.trazo(np.array([(540 + r0 * math.cos(a), 1040 - r0 * math.sin(a) * 1.1),
                                       (540 + r1 * math.cos(a), 1040 - r1 * math.sin(a) * 1.1)]), 4.2, 50 + k, self.fs,
                             1.0 - 0.3 * u, amp=1.0, v=int(255 * (1 - u)))
        # "3000" y zzz
        if t_tres - 0.1 <= t < INI("sol") + 0.5:
            u = prog(t, t_tres - 0.1, t_tres + 1.1) * (1 - prog(t, INI("sol") - 0.2, INI("sol") + 0.4))
            if u > 0:
                m = B.mascara_texto("3000", 250)
                self.h.pegar_mascara(m, 540 - m.shape[1] / 2 + (self.fs - 1) * 0.7, 430, cols=m.shape[1] * (u if u < 1 else 1),
                                     v=int(255 * min(1.0, u * 4)))
        for k in range(3):
            ts = T("mar", "quedarse") + 0.2 + 1.1 * k
            if ts <= t < INI("sol"):
                u = prog(t, ts, ts + 0.9)
                m = B.mascara_texto("z", 46 + 16 * k)
                self.h.pegar_mascara(m, 640 + 40 * k + 10 * math.sin(t * 2), 1130 - 55 * k - 30 * u, v=int(255 * (1 - u * 0.4)))

    def escena_sol(self, t):
        t_out = t_cierre
        self.act(O.sol(76), 190, 700, 1.35, t, t_sol_ini + 0.2, 1.3, t_out=t_out, d_out=0.8, sem=22)
        self.act(O.vapor(2, 200), 540, 1010, 1.0, t, t_calienta, 1.5, t_out=t_out, d_out=0.8, sem=23)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
