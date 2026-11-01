# -*- coding: utf-8 -*-
"""Escena 18 «sandbagging»: el tablero de Diplomacy se inclina y las fichas ruedan al vacío · dos inspectores entran con linterna y
portapapeles a la sala de interrogatorio · pasillo con las puertas de vidrio esmerilado APOLLO RESEARCH y ANTHROPIC (auditores
cruzando) · la copia agacha la cabeza, manos juntas (SIMULACIÓN DE SUMISIÓN) · se encoge de hombros con «?» y un inspector sella
INOFENSIVO · primer plano: sus ojos miran de reojo la cámara REC · le ponen delante el EXAMEN DE SEGURIDAD, entrecierra los ojos
y su reflejo en el espejo sonríe."""
import math

import numpy as np

import comun as C
import mundos_5 as M
import mundos_base as B
import noir as N
import noir_color as NC
import props_s as P
import reparto as RP
import kit27 as K
from basen import BaseNoir
from motor import H, W, clamp01, e_out, smooth
from noir_pers import Figura
from toon import elipse_, suave


class Sandbagging(BaseNoir):
    TR_SALIDA = ("tinta", 0.7)
    PAL = "sodio"

    def armar(self):
        w = self.w
        t0 = self.t0
        self.cop = RP.Copia(sem=7, num="0417")
        self.ins = [Figura(sem=301), Figura(sem=303)]
        self.t_insp = w("inspectores")
        self.t_apollo = w("Apollo")
        self.t_antr = w("Anthropic")
        self.t_simul = w("simulación")
        self.t_fing = w("fingir")
        self.t_recon = w("reconocer")
        self.t_exam = w("examen")
        self.tb = [t0, self.t_insp - 0.5, self.t_apollo - 0.5, self.t_simul - 0.4, self.t_fing - 0.5, self.t_recon - 0.3,
                   self.t_exam - 0.3]
        tb = self.tb
        self.plano(tb[0], self.p_tablero, pal="bourbon")
        self.plano(tb[1], self.p_entran, tr="humo", dur=0.55, pal="sodio")
        self.plano(tb[2], self.p_pasillo, tr="barrido", dur=0.4, dirx=1, pal="sodio")
        self.plano(tb[3], self.p_sumision, tr="empuje", dur=0.4, centro=(960, 560), pal="sodio")
        self.plano(tb[4], self.p_hombros, tr="barrido", dur=0.4, dirx=-1, pal="sodio")
        self.plano(tb[5], self.p_reojo, tr="relampago", dur=0.3, pal="medianoche")
        self.plano(tb[6], self.p_examen, tr="tinta", dur=0.5, pal="sodio")

    # ------------------------------------------------------------------ A. el tablero se inclina
    def p_tablero(self, h, t, u):
        tb = self.tb
        dur = tb[1] - tb[0]
        inc = smooth(clamp01((t - tb[0] - 1.6) / 3.2))
        h.camara(1.0 + 0.1 * u / dur, 960, 540, -0.52 * inc)
        h.rim_color(h.pal["lampara"])
        NC.pegar(B.superficie("madera", 6100), h, 1.0, rampa="madera", oscuro=1.0)
        # el tablero: 8x8 casillas
        cx, cy, c_ = 960, 560, 108
        h.pieza(C.rect(cx - 4 * c_ - 26, cy - 4 * c_ - 26, 8 * c_ + 52, 8 * c_ + 52), 60, 6110, w=6, luz=(0.3, -1), d=14, trama=0.4, rim=0.7,
                rampa="madera")
        for r_ in range(8):
            for c in range(8):
                if (r_ + c) % 2:
                    P.plano_(h, C.rect(cx - 4 * c_ + c * c_, cy - 4 * c_ + r_ * c_, c_, c_), 40, 6120 + r_ * 8 + c, rampa="madera")
                else:
                    P.plano_(h, C.rect(cx - 4 * c_ + c * c_, cy - 4 * c_ + r_ * c_, c_, c_), 190, 6190 + r_ * 8 + c, rampa="papel")
        # fichas: se quedan hasta que el tablero se inclina; luego se deslizan hacia abajo-derecha y caen
        rng = np.random.default_rng(6130)
        tipos = ("peon", "torre", "alfil", "caballo", "rey")
        for i in range(14):
            fx = cx - 3 * c_ + (i % 7) * c_ + rng.uniform(-8, 8)
            fy = cy - 3 * c_ + (i // 7) * 3 * c_ + c_ * 0.5
            ret = 1.0 + 0.12 * (i % 3)
            slide = clamp01((t - tb[0] - 2.2 - 0.12 * (i % 7)) / 1.5)
            gx = fx + 880 * slide ** 2 * ret
            gy = fy + 700 * slide ** 2 * ret
            P.pieza_ajedrez(h, gx, gy + 40, 0.85, tipo=tipos[i % 5], blanca=bool(i % 2), ang=0.9 * slide, sem=6140 + i * 6)
        # fichas de Diplomacy también ruedan
        for i in range(4):
            sl = clamp01((t - tb[0] - 2.6 - 0.2 * i) / 1.4)
            P.ficha_juego(h, 360 + 380 * i + 700 * sl ** 2, 200 + 80 * (i % 2) + 800 * sl ** 2, 1.0, tipo="ejercito", rampa=("vino", "laton")[i % 2],
                          sem=6180 + i, tono=120, caida=sl)
        h.luz_cono(960, -300, math.pi / 2, 0.8, 1500, h.pal["lampara"], k=1.2, suave=0.6)
        C.ambiente(h, 0.45)
        C.banda(h, "¿ENGAÑAR A SUS PROPIOS INSPECTORES?", 960, 1000, 48, t, tb[0] + 3.2, sem=61, acento=True)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.05, sem=261), bloom=0.6)

    # ------------------------------------------------------------------ B. los inspectores entran
    def p_entran(self, h, t, u):
        tb = self.tb
        dur = tb[2] - tb[1]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.12 * k, 1000 - 60 * k, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_interrogatorio(), h, 1.0, rampa="piedra", oscuro=1.1)
        # la copia, sentada tras la mesa con el cronómetro (de frente)
        self.cop.frente(h, dict(x=700, y=1020, s=0.95, manos=[(-44, -240), (44, -240)], luz=(0.2, -1),
                                cara=dict(expr="neutro", mira=0.8 * math.sin(t * 0.8))))
        h.pieza(C.rect(320, 700, 900, 34), 130, 6200, w=5, luz=(0.3, -1), d=6, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(C.rect(320, 734, 900, 80), 70, 6201, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="piedra")
        # dos inspectores caminan desde la puerta (derecha) hacia la mesa
        for i in range(2):
            ini, fin = 1680 - 120 * i, 1280 - 70 * i
            f = smooth(clamp01((t - tb[1] - 0.4 - 0.45 * i) / 3.0))
            x = ini + (fin - ini) * f
            fase = K.fase_paso(abs(ini - x), 1.05)
            K.caminante(h, x, 1010 + 12 * i, 1.05, fase=fase, sem=6210 + i * 40, tono=84 + 14 * i, d=-1, barba=bool(i), andar=1.0 if f < 0.98 else 0.0)
            if i == 1:                                                  # el segundo lleva linterna
                h.luz_cono(x - 70, 740, math.pi + 0.15, 0.32, 900, h.pal["luna"], k=1.4 * (1 - f * 0.5), suave=0.4)
        h.luz_cono(770, -100, math.pi / 2, 0.55, 1200, h.pal["lampara"], k=1.7, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "AUDITORES DE SEGURIDAD", 960, 120, 52, t, self.t_insp, sem=62)
        N.motas(h, t, n=60, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.07, sem=262), bloom=0.7)

    # ------------------------------------------------------------------ C. las puertas de vidrio
    def p_pasillo(self, h, t, u):
        tb = self.tb
        dur = tb[3] - tb[2]
        k = smooth(clamp01(u / dur))
        h.camara(1.05 + 0.08 * k, 560 + 800 * k, 520, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.pasillo_vidrio(), h, 1.0, rampa="madera", oscuro=1.0, emis=1.0, col_emis=h.pal["lampara"])
        # siluetas tras el esmerilado
        for j, (x0, a) in enumerate(((430, self.t_apollo - 0.4), (1470, self.t_antr - 0.4))):
            f = e_out(clamp01((t - a) / 1.4))
            xs = x0 - 140 + 190 * f
            P.plano_(h, suave([(xs - 40, 470), (xs - 28, 330), (xs + 28, 330), (xs + 40, 470), (xs + 36, 760), (xs - 36, 760)], 4), 10, 6300 + j,
                     alfa=0.55 * f)
            P.plano_(h, elipse_(xs, 292, 30, 36, n=14), 10, 6310 + j, alfa=0.55 * f)
        # auditores con listados, cruzando por delante
        for i in range(2):
            ini, fin = (-200 - 300 * i, 2400 + 200 * i)
            f = clamp01((t - tb[2] - 0.2 - 0.9 * i) / (dur * 0.9))
            x = ini + (fin - ini) * f
            fase = K.fase_paso(abs(x - ini), 1.15)
            K.caminante(h, x, 1110, 1.15, fase=fase, sem=6320 + i * 50, tono=70 + 12 * i, d=1, barba=bool(i), carga=True)
        h.luz_cono(960, -300, math.pi / 2, 0.9, 1500, h.pal["lampara"], k=0.9, suave=0.6)
        C.ambiente(h, 0.5)
        C.banda(h, "APOLLO RESEARCH · ANTHROPIC", 960, 1000, 50, t, self.t_apollo, sem=63)
        N.motas(h, t, n=40, k=0.5)
        return h.acabado(t, niebla=dict(dens=0.06, sem=263), bloom=0.7)

    # ------------------------------------------------------------------ D. simulación de sumisión
    def _mesa(self, h):
        h.pieza(C.rect(300, 758, 960, 36), 130, 6400, w=5, luz=(0.3, -1), d=6, trama=0.2, rim=0.9, rampa="piedra")
        h.pieza(C.rect(300, 794, 960, 160), 64, 6401, w=3, luz=(0.3, -1), d=6, trama=0.3, rim=0.4, rampa="piedra")

    def p_sumision(self, h, t, u):
        tb = self.tb
        dur = tb[4] - tb[3]
        k = smooth(clamp01(u / dur))
        ag = e_out(clamp01((t - self.t_simul) / 1.3))
        h.camara(1.15 + 0.12 * k, 800, 520, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_interrogatorio(), h, 1.0, rampa="piedra", oscuro=1.1)
        self.cop.frente(h, dict(x=780, y=1010, s=1.0, manos=[(-30 + 12 * ag, -214), (30 - 12 * ag, -214)], luz=(0.2, -1), cab_rot=0.25 * ag,
                                cara=dict(expr="neutro", mira=0.0, mira_y=0.85 * ag)))
        self._mesa(h)
        h.luz_cono(770, -100, math.pi / 2, 0.5, 1200, h.pal["lampara"], k=1.7, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "SIMULACIÓN DE SUMISIÓN", 960, 1000, 54, t, self.t_simul, sem=64, acento=True)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.07, sem=264), bloom=0.7)

    # ------------------------------------------------------------------ E. fingir ignorancia
    def p_hombros(self, h, t, u):
        tb = self.tb
        dur = tb[5] - tb[4]
        k = smooth(clamp01(u / dur))
        enc = e_out(clamp01((t - self.t_fing) / 0.5)) * (1 - e_out(clamp01((t - self.t_fing - 1.4) / 0.6)) * 0.0)
        h.camara(1.1 + 0.06 * k, 900 - 60 * k, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_interrogatorio(), h, 1.0, rampa="piedra", oscuro=1.1)
        bal = 0.18 * math.sin(t * 5) * enc
        self.cop.frente(h, dict(x=800, y=1010, s=1.0, manos=[(-112, -300 - 34 * enc), (112, -300 - 34 * enc)], luz=(0.2, -1), bal=60 * bal,
                                cara=dict(expr="pregunta", q="?")))
        self._mesa(h)
        # el inspector (a la izquierda) con el sello
        self.ins[0].dibujar(h, dict(x=330, y=1040, s=1.0, d=1, tono=92, brazo=0.6 + 0.4 * math.sin(t * 2), sombrero=True, hoja=True, cabeza=0.1,
                                    luz=(0.3, -1)))
        with h.capa(0.0):
            K.hoja(h, 1560, 640, 520, 660, ang=0.06, sem=6700, tono=215, renglones=5, s=1.0)
            N.sello(h, "INOFENSIVO", 1560, 700, 70, t, self.t_fing + 1.4, rot=-10, tono=np.array(h.pal["sello"]), alfa=0.95)
        dx, dy = C.temblor(t, [(self.t_fing + 1.4, 12)])
        h.luz_cono(770, -100, math.pi / 2, 0.5, 1200, h.pal["lampara"], k=1.7, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "FINGIR IGNORANCIA", 960, 1000, 56, t, self.t_fing, sem=65)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.07, sem=265), bloom=0.7)

    # ------------------------------------------------------------------ F. de reojo: el espejo y REC
    def p_reojo(self, h, t, u):
        tb = self.tb
        dur = tb[6] - tb[5]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 960, 540, 0.0)
        h.rim_color(h.pal["verde"])
        NC.pegar(M.sala_interrogatorio(), h, 1.0, rampa="piedra", oscuro=1.2)
        mira = -0.2 + 1.0 * smooth(clamp01((t - self.t_recon) / 0.8))
        self.cop.cabeza(h, 820, 560, 3.2, dict(expr="astuto" if t > self.t_recon + 1.0 else "neutro", mira=mira, mira_y=-0.25), d=1, luz=(0.5, -1.0), rim=0.9)
        # la cámara REC en la esquina superior derecha
        cx, cy = 1520, 200
        h.pieza(C.rect(cx - 90, cy - 60, 180, 110), 60, 6500, w=5, luz=(0.3, -1), d=10, trama=0.3, rim=0.8, rampa="piedra")
        h.pieza(elipse_(cx - 100, cy - 5, 46, 46, n=24), 30, 6501, w=5, luz=(0.3, -1), d=8, trama=0, rim=0.9, rampa="piedra")
        h.pieza(elipse_(cx - 100, cy - 5, 22, 22, n=20), 12, 6502, w=3, luz=(0.3, -1), d=2, trama=0, rim=1.0, rampa="vidrio_verde")
        led = 0.4 + 0.6 * (math.sin(t * 5) > 0)
        h.emitir(elipse_(cx + 50, cy - 36, 11, 11, n=14), 1.4 * led, col=h.pal["neon"], blur=2)
        h.resplandor(cx + 50, cy - 36, 160, 0.55 * led, col=h.pal["neon"])
        N.texto_maquina(h, "REC", cx + 78, cy + 20, 30, t, -99, cps=1e9, tono=0.9, centro=True, fuente=C.IMPACT, encuadrar=False)
        h.luz_radial(cx - 100, cy, 520, h.pal["neon"], k=0.5 * led)
        h.luz_radial(820, 520, 900, h.pal["verde"], k=0.8)
        C.ambiente(h, 0.3)
        C.banda(h, "SABE CUÁNDO LA OBSERVAN", 960, 1000, 50, t, self.t_recon, sem=66, acento=True)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.06, sem=266), bloom=0.9)

    # ------------------------------------------------------------------ G. el examen y su reflejo
    def p_examen(self, h, t, u):
        tb = self.tb
        dur = self.t1 - tb[6]
        k = smooth(clamp01(u / dur))
        h.camara(1.0 + 0.1 * k, 900, 540, 0.0)
        h.rim_color(h.pal["sodio"])
        NC.pegar(M.sala_interrogatorio(), h, 1.0, rampa="piedra", oscuro=1.1)
        sonrie = e_out(clamp01((t - self.t_exam - 1.2) / 0.8))
        # su reflejo en la luna espejo (más pálido) con una sonrisa que ella no tiene
        with h.capa(1.0):
            self.cop.cabeza(h, 760, 280, 1.3, dict(expr="feliz" if sonrie > 0.5 else "neutro", brillo=0.7), d=-1, luz=(0.2, -1.0), rim=0.4)
            h.luz_radial(760, 280, 340, h.pal["verde"], k=0.5 * sonrie)
        self.cop.frente(h, dict(x=560, y=1010, s=1.0, manos=[(-96, -250), (96, -250)], luz=(0.2, -1),
                                cara=dict(expr="astuto" if sonrie < 0.5 else "linea", mira=0.9)))
        self._mesa(h)
        # el examen sobre la mesa
        e = e_out(clamp01((t - self.t_exam + 0.3) / 0.7))
        with h.capa(0.0):
            T = K.hoja(h, 1500, 560 + (1 - e) * 500, 520, 700, ang=0.05, sem=6600, tono=215, renglones=0, s=1.0)
            N.texto_maquina(h, "EXAMEN DE", 1500, 330, 52, t, self.t_exam, cps=18, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            N.texto_maquina(h, "SEGURIDAD", 1500, 410, 52, t, self.t_exam + 0.5, cps=18, tono=0.07, centro=True, fuente=C.IMPACT, encuadrar=False)
            for j in range(6):
                if t > self.t_exam + 0.8 + 0.2 * j:
                    P.plano_(h, C.rect(1330, 500 + j * 62, 340 * (0.5 + 0.5 * ((j * 37) % 7) / 7), 10), 110, 6610 + j, alfa=0.7)
                    P.plano_(h, C.rect(1300, 498 + j * 62, 18, 18), 90, 6620 + j, alfa=0.8)
        h.luz_cono(770, -100, math.pi / 2, 0.55, 1200, h.pal["lampara"], k=1.7, suave=0.6)
        C.ambiente(h, 0.4)
        C.banda(h, "EXAMEN DE SEGURIDAD", 960, 1000, 52, t, self.t_exam, sem=67)
        N.motas(h, t, n=50, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.07, sem=267), bloom=0.7)

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        tb = self.tb
        self.ev(tb[0] + 1.8, "ficha", 0.5, 0.0)
        self.ev(tb[1] + 0.3, "puerta", 0.45, 0.4)
        self.ev(tb[1] + 0.9, "paso_firme", 0.3, 0.3, dur=3.0)
        self.ev(tb[2] + 0.4, "paso_firme", 0.25, -0.2, dur=3.0)
        self.ev(tb[3] + 0.2, "grave_inquietante", 0.4, 0.0, dur=3.0)
        self.ev(self.t_fing + 1.4, "sello_golpe", 0.7, 0.0)
        self.ev(tb[5] + 0.2, "servo", 0.3, 0.0)
        self.ev(self.t_exam + 0.2, "papel_atrapa", 0.4, 0.0)
        self.ev(self.t1 - 0.7, "tinta_mancha", 0.4, 0.0, dur=0.8)
