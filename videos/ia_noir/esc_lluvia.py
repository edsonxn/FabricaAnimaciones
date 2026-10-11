# -*- coding: utf-8 -*-
"""Escena 1 «lluvia» (gancho): grúa desde el cielo de tormenta hasta el rascacielos de cristal del laboratorio (las plantas
encendidas: «los que la construyeron tampoco [duermen]») y bajada a la calle; el detective bajo la farola atrapa la hoja que trae
el viento; primer plano del prospecto con el sello RIESGO EXISTENCIAL; paneo al loco de la esquina y a la bolsa; primer plano
del detective: calada, humo y la colilla que cae al charco."""
import math

import cv2
import numpy as np

import mundos as MU
import noir as N
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, prog, smooth
from noir import gris
from noir_pers import Busto, Detective, Figura
from toon import Pista, pulso

DET = dict(x=950.0, y=905.0, s=0.82, d=1, luz=(0.35, -1.0))
FAROL = (1020.0, 448.0)
FAROL2 = (MU.X_ESQUINA - 60.0, 448.0)


def luces_calle(h, k=1.0):
    h.ambiente[:] = 0.78
    h.luz_cono(FAROL[0], FAROL[1], math.pi / 2 + 0.04, 0.46, 640, (1.5, 1.5, 1.5), k=k, suave=0.5)
    h.luz_radial(FAROL[0], FAROL[1], 140, (0.9, 0.9, 0.9), k=k)
    h.luz_cono(FAROL2[0], FAROL2[1], math.pi / 2 - 0.04, 0.46, 640, (1.4, 1.4, 1.4), k=k, suave=0.5)
    h.luz_radial(FAROL2[0], FAROL2[1], 140, (0.9, 0.9, 0.9), k=k)


def fondo_ciudad(h, t, nubes=True):
    MU.cielo().pegar(h, 0.05, dx=-(t * 6.0) % 400 if nubes else 0.0)
    MU.lejos().pegar(h, 0.3, bruma=0.55, tono_bruma=0.40)
    MU.medio().pegar(h, 0.6, bruma=0.28, tono_bruma=0.40)


def rayo(h, t, t0, x0, sem=0):
    """Rayo dibujado en el cielo (capa lejana) durante el destello."""
    u = t - t0
    if not (0 <= u < 0.35):
        return
    r = np.random.default_rng(sem)
    P = [(x0, -1200.0)]
    for k in range(9):
        P.append((P[-1][0] + r.uniform(-70, 70), P[-1][1] + r.uniform(90, 150)))
    with h.capa(0.25):
        h.trazo(np.array(P), 9, sem, color=(255, 255, 255), taper=(0.1, 0.6), jit=0.5)
        for k in (3, 5):
            Q = [P[k]]
            for j in range(4):
                Q.append((Q[-1][0] + r.uniform(20, 70), Q[-1][1] + r.uniform(50, 90)))
            h.trazo(np.array(Q), 4, sem + k, color=(240, 240, 240), taper=(0.1, 0.8), jit=0.5)


def salpicar_calle(h, t, k=1.0):
    y0 = h.tf(np.array([[0, MU.Y_ACERA]]))[0][1]
    y1 = h.tf(np.array([[0, 1250]]))[0][1]
    if y1 > 0 and y0 < H:
        N.salpicaduras(h, t, max(0, y0), min(H, y1), n=70, k=k)


def reflejar(h, t, k=0.38):
    ys = h.tf(np.array([[0, MU.Y_BORDILLO + 10]]))[0][1]
    if 40 < ys < H - 20:
        N.reflejo(h.img, ys, k=k, t=t)
        if h._E is not None:
            N.reflejo(h._E, ys, k=k * 0.8, t=t)


class Lluvia(BaseNoir):
    TR_SALIDA = ("tinta", 0.8)


    def armar(self):
        w = self.w
        self.det = Detective(sem=3)
        self.busto = Busto(sem=5)
        self.loco = Figura(sem=11)
        t0 = self.t0
        self.t_constr = w("construyeron")
        self.t_tampoco = w("tampoco", fin=True)
        self.t_sept = w("septiembre")
        self.t_adv = w("advertencia")
        self.t_que = w("Que lo que", frase=2)
        self.t_exist = w("existencial")
        self.t_human = w("humanidad")
        self.t_nolo = w("No lo dijo")
        self.t_loco = w("loco")
        self.t_dijeron = w("Lo dijeron")
        self.t_bolsa = w("bolsa")
        self.t_yyo = w("Y yo")
        self.t_noches = w("noches")
        self.t_ciudad = w("ciudad", desde=4)
        self.t_quise = w("quise")
        self.t_porque = w("por qué", fin=True)
        self.rayos = [t0 + 0.9, self.t_constr - 0.2, self.t_exist - 0.05]
        # cámara de la ciudad (grúa -> torre -> calle -> empuje lento)
        ta = self.t_tampoco
        self.cam_a = Pista([(t0, (1010, -1950, 0.82)), (self.t_constr - 0.4, (1010, -1640, 1.05), "io"),
                            (ta + 0.2, (1010, -1560, 1.45), "o"),
                            (ta + 2.0, (900, 690, 1.55), "io"), (self.t_que, (960, 700, 1.78), "l")])
        # la hoja que trae el viento
        tc = self.t_adv + 0.15
        self.hoja = Pista([(self.t_sept - 0.4, (-150, 520, 0.0)), (self.t_sept + 1.2, (300, 760, 2.4), "l"),
                           (self.t_sept + 2.6, (620, 600, 5.0), "l"), (tc - 0.6, (900, 690, 7.3), "l"), (tc, (1035, 700, 8.0), "o")])
        self.t_atrapa = tc
        self.pose_b = dict(fumar=Pista([(t0, 0.0), (self.t_sept + 0.6, 0.0), (self.t_sept + 1.3, 1.0), (self.t_sept + 2.6, 1.0),
                                        (self.t_sept + 3.3, 0.0)]),
                           sost=Pista([(tc - 0.35, 0.0), (tc, 1.0, "o")]),
                           giro=Pista([(t0, 0.0), (tc - 1.6, 0.0), (tc - 1.0, -0.4), (tc + 0.6, 0.6, "io")]))
        self.cam_d = Pista([(self.t_nolo - 0.3, (1700, 600, 1.05)), (self.t_loco - 0.2, (2470, 600, 1.3), "o"),
                            (self.t_dijeron, (2560, 610, 1.35), "l"), (self.t_bolsa - 0.3, (3420, 470, 0.98), "io"),
                            (self.t_yyo, (3470, 470, 1.02), "l")])
        self.pose_e = dict(fumar=Pista([(self.t_yyo, 0.0), (self.t_yyo + 1.0, 1.0, "io"), (self.t_ciudad - 0.2, 1.0),
                                        (self.t_ciudad + 0.5, 0.15, "io"), (self.t_porque - 0.4, 0.2), (self.t_porque, 0.55, "a"),
                                        (self.t_porque + 0.25, 0.0, "o")]),
                           brasa=Pista([(self.t_yyo + 1.0, 0.0), (self.t_yyo + 1.6, 1.0), (self.t_ciudad - 0.2, 1.0),
                                        (self.t_ciudad + 0.3, 0.2)]))
        self.plano(t0, self.p_ciudad)
        self.plano(self.t_que - 0.35, self.p_documento, tr="empuje", dur=0.75, centro=(W * 0.56, H * 0.62))
        self.plano(self.t_nolo - 0.35, self.p_esquina, tr="barrido", dur=0.6, dirx=1)
        self.plano(self.t_yyo - 0.3, self.p_cara, tr="barrido", dur=0.6, dirx=-1)

    # ------------------------------------------------------------------ planos
    def p_ciudad(self, h, t, u):
        cx, cy, z = self.cam_a(t)
        h.camara(z, cx, cy, 0.012 * math.sin(t * 0.4))
        fondo_ciudad(h, t)
        for t_r, xr in zip(self.rayos[:2], (1300, 700)):
            rayo(h, t, t_r, xr, sem=int(t_r * 10))
        MU.calle().pegar(h, 1.0)
        self.dibujar_hoja(h, t)
        self.dibujar_det(h, t, self.pose_b)
        luces_calle(h)
        reflejar(h, t)
        N.lluvia(h, t, n=650)
        salpicar_calle(h, t)
        tip = self.det.punta_cigarro(self.pose_det(t, self.pose_b))
        N.humo(h, t, tip[0], tip[1], k=0.9)
        fl = max(N.relampago(t, self.rayos[:2]), 0.0)
        h.ambiente[:] += 0.9 * fl
        return h.acabado(t, niebla=dict(dens=0.22, y0=300, y1=1000, vel=40), flash=0.25 * fl)

    def pose_det(self, t, P):
        p = dict(DET)
        p["fumar"] = float(P["fumar"](t))
        if "sost" in P:
            p["sostener"] = float(P["sost"](t))
            p["giro"] = float(P["giro"](t))
        if "brasa" in P:
            p["brasa"] = float(P["brasa"](t))
        p["viento"] = 0.35 + 0.15 * math.sin(t * 1.7)
        p["hombros"] = 0.4
        return p

    def dibujar_det(self, h, t, P):
        p = self.pose_det(t, P)
        self.det.dibujar(h, p)
        tip = self.det.punta_cigarro(p)
        h.emitir(np.array([[tip[0] - 3, tip[1] - 3], [tip[0] + 3, tip[1] - 3], [tip[0] + 3, tip[1] + 3], [tip[0] - 3, tip[1] + 3]]),
                 0.9 + 0.4 * p.get("brasa", 0.0))
        h.luz_radial(tip[0], tip[1], 60 + 90 * p.get("brasa", 0.0), (0.5, 0.5, 0.5), k=0.6 + 0.8 * p.get("brasa", 0.0))

    def dibujar_hoja(self, h, t):
        if t < self.t_sept - 0.4:
            return
        x, y, gir = self.hoja(t)
        if t >= self.t_atrapa:                          # ya en la mano del detective
            p = self.pose_det(t, self.pose_b)
            hx, hy = self.det._T(p)(np.array([self.det._mano_pos(p, 0.0)]))[0]
            x, y, gir = hx + 18, hy - 10, 8.0
            ang, esc = 0.15 + 0.03 * math.sin(t * 3), 1.0
        else:
            ang = 0.6 * math.sin(gir * 1.3) + 0.2
            esc = 0.35 + 0.65 * abs(math.cos(gir))     # se voltea en el aire
        ww, hh = 62, 80
        c, s = math.cos(ang), math.sin(ang)
        P = np.array([[-ww / 2, -hh / 2], [ww / 2, -hh / 2], [ww / 2, hh / 2], [-ww / 2, hh / 2]]) * (esc, 1)
        P = np.stack([x + P[:, 0] * c - P[:, 1] * s, y + P[:, 0] * s + P[:, 1] * c], 1)
        h.pieza(P, 212, 77, w=3.5, luz=(0.3, -1), d=6, trama=0, rim=0.0, sombra=0.4)
        for k in range(4):
            a = P[0] + (P[3] - P[0]) * (0.2 + 0.15 * k) + (P[1] - P[0]) * 0.12
            b = a + (P[1] - P[0]) * 0.75
            h.trazo(np.array([a, b]), 2.0, 78 + k, alfa=0.5)

    def p_documento(self, h, t, u):
        z = 1.0 + 0.05 * u
        h.camara(z, 30 - 10 * u, 20, -0.03 + 0.012 * u)
        MU.documento().pegar(h, 1.0)
        # gotas que mojan la hoja (manchas que crecen) y gotitas que rebotan
        for k in range(26):
            r = np.random.default_rng(k * 17 + 5)
            tk = self.t_que - 0.3 + r.uniform(0, 5.5)
            if t < tk:
                continue
            a = min(1.0, (t - tk) / 0.5)
            x, y, rr = r.uniform(-560, 580), r.uniform(-620, 640), r.uniform(10, 34)
            h.pieza(np.array([[x + rr * a * math.cos(q) * (1 + 0.15 * math.sin(5 * q + k)), y + rr * a * math.sin(q) * 0.9]
                              for q in np.linspace(0, 2 * math.pi, 18, endpoint=False)]), 150, 300 + k, w=0, luz=(0, -1), d=3,
                    sombra=0, trama=0, alfa=0.45, linea=False, jit=0.4)
        tx = self.t_que + 0.35
        N.texto_maquina(h, "...nuestros modelos podrían suponer riesgos", -470, -40, 38, t, tx, cps=26, tono=0.05)
        N.texto_maquina(h, "catastróficos o existenciales para la humanidad.", -470, 20, 38, t, tx + 1.75, cps=26, tono=0.05)
        N.texto_maquina(h, "80 de 261 páginas dedicadas a riesgos", -470, 470, 30, t, self.t_human, cps=30, tono=0.08)
        N.sello(h, "RIESGO EXISTENCIAL", 120, 250, 92, t, self.t_exist, rot=-9)
        h.ambiente[:] = 0.5
        h.luz_radial(-80, -320, 1250, (1.0, 1.0, 1.0), k=1.0)
        h.luz_cono(-200, -1400, math.pi / 2 + 0.1, 0.5, 2600, (0.5, 0.5, 0.5))
        N.lluvia(h, t, n=420, capas=(0.9, 1.0), vel=2200, k=0.8)
        N.salpicaduras(h, t, 0, H, n=40, k=0.9, ritmo=1.6)
        fl = N.relampago(t, [self.rayos[2]])
        h.ambiente[:] += fl
        return h.acabado(t, flash=0.3 * fl, niebla=None)

    def p_esquina(self, h, t, u):
        cx, cy, z = self.cam_d(t)
        h.camara(z, cx, cy, 0.0)
        fondo_ciudad(h, t)
        MU.calle().pegar(h, 1.0)
        # el loco del cartel bajo la farola de la esquina (se desvanece en la lluvia: «no lo dijo un loco»)
        des = 1 - smooth(clamp01((t - self.t_dijeron + 0.3) / 1.2))
        if des > 0.02:
            self.dibujar_loco(h, t, des)
        luces_calle(h)
        # la bolsa: los ventanales se encienden al decir «bolsa»
        enc = smooth(clamp01((t - self.t_bolsa + 0.2) / 0.6))
        if enc > 0:
            for k in range(7):
                bx = 2800 + 80 + (k + 0.5) * (1240 - 160) / 7
                h.luz_radial(bx, 620, 160, (0.9, 0.9, 0.9), k=enc * 0.7)
            h.luz_radial(3420, 160, 700, (0.6, 0.6, 0.6), k=enc)
        reflejar(h, t)
        N.lluvia(h, t, n=650)
        salpicar_calle(h, t)
        return h.acabado(t, niebla=dict(dens=0.24, y0=300, y1=1000, vel=40))

    def dibujar_loco(self, h, t, alfa):
        x, y = MU.X_ESQUINA - 40, 905
        sw = 3 * math.sin(t * 1.3)
        h.silueta = None
        self.loco.dibujar(h, dict(x=x + sw, y=y, s=0.8, d=-1, luz=(0.4, -1), sombrero=True, tono=60, cabeza=-0.3))
        # cartel de sándwich con letras pintadas a mano
        P = np.array([[x - 62, 560], [x + 62, 560], [x + 66, 840], [x - 66, 840]]) + (sw, 0)
        h.pieza(P, 196, 91, w=5, luz=(0.4, -1), d=10, trama=0.3)
        for (a, b) in (((x - 40, 560), (x - 30, 520)), ((x + 40, 560), (x + 30, 520))):
            h.trazo(np.array([a, b]) + (sw, 0), 4, 92)
        for k_, (s_, yy) in enumerate((("EL FIN", 615), ("ESTÁ", 685), ("CERCA", 755))):
            N.texto_maquina(h, s_, x + sw, yy, 50, t, -99, cps=1e9, tono=0.03, centro=True, fuente=N.FUENTE_SELLO, encuadrar=False)
        if alfa < 1:                                      # se lo traga la lluvia: velo gris sobre él
            m = np.array([[x - 120, 330], [x + 120, 330], [x + 120, 910], [x - 120, 910]])
            h.pieza(m, 40, 93, w=0, luz=(0, -1), d=1, sombra=0, trama=0, alfa=1 - alfa, linea=False, jit=0)

    def p_cara(self, h, t, u):
        # fondo: la calle desenfocada (poca profundidad de campo) y la lluvia delante
        h.camara(1.5, 1150 + 30 * u, 470, 0.0)
        fondo_ciudad(h, t)
        MU.calle().pegar(h, 1.0)
        luces_calle(h)
        bg = cv2.resize(h.img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        h.img[:] = cv2.resize(cv2.GaussianBlur(bg, (0, 0), 3.0), (W, H), interpolation=cv2.INTER_LINEAR)
        if h._E is not None:
            e = cv2.resize(h._E, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
            h._E[:] = cv2.resize(cv2.GaussianBlur(e, (0, 0), 3.0), (W, H), interpolation=cv2.INTER_LINEAR) * 1.3
        L0 = h.mapa_gris()
        h.img *= cv2.resize(L0, (W, H))[..., None] * 0.55
        h.luces = []
        h.camara(1.0, W / 2, H / 2, 0.0)
        # el busto
        P = self.pose_e
        tp = self.t_porque
        mano = smooth(clamp01((t - (tp - 0.95)) / 0.6))
        tira = smooth(clamp01((t - (tp + 0.05)) / 0.35))
        boca = pulso(t, self.t_quise - 0.1, 1.2, 1.0)
        z = 1.0 + 0.06 * smooth(clamp01(u / 6.0))
        p = dict(x=760 - 20 * smooth(clamp01(u / 6.0)), y=500, s=z, d=1, luz=(0.8, -0.7), brasa=float(P["brasa"](t)),
                 mano=mano, tira=tira, boca=boca, arriba=0.1 + 0.3 * pulso(t, self.t_noches - 0.5, 2.4), rot=-0.02 + 0.01 * math.sin(t))
        if tira >= 1.0:
            p["cigarro"] = False
        self.busto.dibujar(h, p)
        h.ambiente[:] = 0.62
        h.luz_cono(1750, -150, math.atan2(650, -950), 0.45, 1900, (1.0, 1.0, 1.0), suave=0.6)
        if tira < 1.0:
            tip = self.busto.punta(p)
            br = p["brasa"]
            h.emitir(np.array([[tip[0] - 6, tip[1] - 6], [tip[0] + 6, tip[1] - 6], [tip[0] + 6, tip[1] + 6], [tip[0] - 6, tip[1] + 6]]),
                     0.9 + 0.5 * br)
            h.luz_radial(tip[0], tip[1], 160 + 260 * br, (0.7, 0.7, 0.7), k=0.6 + 1.3 * br)
            N.humo(h, t, tip[0], tip[1], k=1.0, ancho=2.2, viento=(50, -150))
        else:                                            # la colilla sale volando y se apaga en el charco
            cae = t - (tp + 0.4)
            tip0 = self.busto._T(p)(np.array([[560.0, 0.0]]))[0]
            cx, cy = tip0[0] + 520 * cae, tip0[1] - 300 * cae + 1700 * cae * cae
            if cy < H + 20:
                h.emitir(np.array([[cx - 6, cy - 6], [cx + 6, cy - 6], [cx + 6, cy + 6], [cx - 6, cy + 6]]), max(0.0, 1.1 - cae))
                h.luz_radial(cx, cy, 120, (0.6, 0.6, 0.6), k=max(0.0, 1 - cae))
        bu = t - self.t_quise
        if 0 < bu < 3.2:                                 # bocanada de humo al decir «quise»
            lb = self.busto.labios(p)
            N.humo(h, t, lb[0], lb[1], k=1.3 * (1 - bu / 3.2), sem=9, viento=(160, -70), vida=min(bu, 2.6), hebras=6, ancho=3.2,
                   t_ini=self.t_quise)
        N.lluvia(h, t, n=360, capas=(0.85, 1.0), vel=1900, k=1.3)
        return h.acabado(t, niebla=None, bloom=0.45)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        t0 = self.t0
        self.ev(t0, "lluvia_amb", 0.9, 0.0, dur=self.t1 - t0)
        for tr in self.rayos:
            self.ev(tr, "trueno_noir", 0.85, -0.3, dur=4.0)
        self.ev(self.t_tampoco + 0.1, "barrido_aire", 0.6, 0.0, dur=1.8)
        self.ev(self.t_sept - 0.3, "papel_viento", 0.6, -0.6, dur=self.t_atrapa - self.t_sept + 0.3)
        self.ev(self.t_atrapa, "papel_atrapa", 0.8, 0.2)
        self.ev(self.t_que - 0.35, "barrido_aire", 0.5, 0.0, dur=0.8)
        tx = self.t_que + 0.35
        for k, (ini, n, cps) in enumerate(((tx, 45, 26), (tx + 1.75, 49, 26), (self.t_human, 37, 30))):
            for i in range(n):
                self.ev(ini + i / cps, "tecla", 0.45, -0.2 + 0.4 * (i / n), tono=1.0 + 0.04 * ((i * 7) % 5))
            self.ev(ini + n / cps + 0.05, "carro_maquina", 0.5, 0.3)
        self.ev(self.t_exist, "sello_golpe", 1.0, 0.0)
        self.ev(self.t_nolo - 0.35, "barrido_aire", 0.6, 0.4, dur=0.7)
        self.ev(self.t_bolsa - 0.1, "campana_bolsa", 0.45, 0.4)
        self.ev(self.t_yyo - 0.3, "barrido_aire", 0.6, -0.4, dur=0.7)
        self.ev(self.t_yyo + 1.0, "calada", 0.7, 0.1, dur=1.4)
        self.ev(self.t_quise, "exhala", 0.6, 0.15, dur=1.6)
        self.ev(self.t_porque + 0.25, "colilla", 0.6, 0.2)
        self.ev(self.t_porque + 0.85, "chisporroteo", 0.7, 0.2)
        self.ev(self.t1 - 0.8, "tinta_mancha", 0.6, 0.0, dur=0.9)
