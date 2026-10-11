# -*- coding: utf-8 -*-
"""Escena 5 «apagador»: la cafetería nocturna con el brazo mecánico que sirve café · café real (video entintado) · el enchufe: la
mano va a desconectarlo y la pinza lo defiende · periódicos que giran (SOLO TEORÍA → YA NO) · el código del apagado tachado
(video real) · el chantaje en un sobre CONFIDENCIAL · cajas que se protegen entre sí · la silla vacía · el espejo falso y la cámara."""
import math

import numpy as np

import mundos as MU
import noir as N
import props as PR
import props4 as P4
from basen import BaseNoir
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from noir_pers import Detective
from toon import Pista, elipse_, pulso

URNA = np.array([1640.0, 230.0])


class Apagador(BaseNoir):
    TR_SALIDA = ("barrido", 0.55)

    def armar(self):
        w = self.w
        self.det = Detective(sem=3)
        self.t_idea = w("idea")
        self.t_miedo = w("miedo")
        self.t_si = w("Si le pides")
        self.t_cafe = w("café")
        self.t_traerlo = w("traerlo")
        self.t_apaga = w("apaga", desde=1)
        self.t_asi = w("Así que")
        self.t_ensene = w("enseñe")
        self.t_razon = w("razón")
        self.t_noapagar = w("dejarse")
        self.t_durante = w("Durante años")
        self.t_teoria = w("teoría")
        self.t_yano = w("Ya no")
        self.t_pruebas = w("En pruebas")
        self.t_edito = w("editó")
        self.t_codigo = w("código")
        self.t_otra = w("En otra")
        self.t_amenazo = w("amenazó")
        self.t_secreto = w("secreto")
        self.t_reempl = w("reemplazaran")
        self.t_yeste = w("Y este año")
        self.t_varios = w("varios modelos")
        self.t_sabotear = w("sabotear")
        self.t_otra_ia = w("otra inteligencia")
        self.t_nadie = w("Nadie les")
        self.t_algunos = w("Y algunos")
        self.t_observ = w("observando")
        self.plano(self.t0, self.p_cafeteria)
        self.plano(self.t_cafe - 0.35, self.p_cafe_real, tr="empuje", dur=0.45, centro=(W * 0.62, H * 0.45))
        self.plano(self.t_cafe + 1.5, self.p_cafeteria, tr="barrido", dur=0.45, dirx=-1)
        self.plano(self.t_asi - 0.3, self.p_enchufe, tr="empuje", dur=0.5, centro=(W * 0.9, H * 0.4))
        self.plano(self.t_durante - 0.3, self.p_periodicos, tr="relampago", dur=0.3)
        self.plano(self.t_pruebas - 0.25, self.p_codigo, tr="barrido", dur=0.45, dirx=1)
        self.plano(self.t_otra - 0.3, self.p_chantaje, tr="tinta", dur=0.6)
        self.plano(self.t_yeste - 0.3, self.p_cajas, tr="relampago", dur=0.3)
        self.plano(self.t_nadie - 0.3, self.p_silla, tr="humo", dur=0.6)
        self.plano(self.t_algunos - 0.25, self.p_espejo, tr="barrido", dur=0.45, dirx=1)

    # ------------------------------------------------------------------ la cafetería
    def brazo(self, h, t, taza_en=None):
        """El brazo va a la cafetera, sirve, y lleva la taza a la barra frente al detective (todo función de t)."""
        lleva = smooth(clamp01((t - (self.t_cafe + 1.5)) / 1.6))
        a1 = -0.55 + 0.2 * math.sin(t * 0.8) * (1 - lleva) - 0.75 * lleva
        a2 = 1.25 - 0.15 * math.sin(t * 1.1) * (1 - lleva) + 0.55 * lleva
        a3 = 0.6 - 0.2 * lleva
        punta = P4.brazo_robot(h, 1250, 664, -a1, -a2, -a3, s=1.15, pinza=0.3, sem=40)
        return punta, lleva

    def p_cafeteria(self, h, t, u):
        if t < self.t_cafe:
            z, cx, cy = 0.86 + 0.08 * smooth(clamp01(u / 4.0)), 780 + 60 * smooth(clamp01(u / 4.0)), 200
        else:
            k = smooth(clamp01((t - self.t_cafe - 1.5) / 2.5))
            z, cx, cy = 1.0 + 0.3 * k, 840 - 160 * k, 260 + 120 * k
        h.camara(z, cx, cy, 0.0)
        MU.cafeteria().pegar(h, 1.0)
        punta, lleva = self.brazo(h, t)
        # la taza: en la pinza mientras viaja; en la barra después
        if lleva < 1:
            P4.taza(h, punta[0], punta[1] + 80, s=0.9, sem=60)
        else:
            P4.taza(h, 760, 662, s=0.9, sem=60, humo_t=t)
        p = dict(x=600, y=1000, s=1.3, d=1, luz=(0.4, -1), fumar=0.0, giro=0.3, viento=0.0, hombros=0.3,
                 arriba=0.25 * smooth(clamp01((t - self.t_traerlo) / 0.5)))
        if t > self.t_apaga - 0.2:                           # mira hacia el enchufe de la pared
            p["cab_rot"] = 0.05
        self.det.dibujar(h, p)
        h.ambiente[:] = 0.5
        for cx_ in (200, 900, 1600, 2200):
            h.luz_cono(cx_, -480, math.pi / 2, 0.75, 1300, (0.8, 0.8, 0.8), suave=0.6)
        N.lluvia(h, t, n=300, caja=tuple(h.tf(np.array([[-300, -420]]))[0]) + tuple(h.tf(np.array([[460, 140]]))[0]), k=0.8)
        return h.acabado(t, niebla=None)

    def p_cafe_real(self, h, t, u):
        N.clip_noir(h, "cafe_2", t, self.t_cafe - 0.35, inicio=3.0, z0=1.15, z1=1.3, dur=2.2, tinta=0.6, poster=0.4)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el enchufe
    def p_enchufe(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.40
        for k in range(0, W, 46):
            h.trazo(np.array([[k, 0], [k, H]]), 1.5, 900 + k, alfa=0.25, tf=False)
        tira = smooth(clamp01((t - self.t_razon) / 0.5)) * (1 - smooth(clamp01((t - self.t_noapagar - 0.3) / 0.4)))
        PR_x = W / 2 + 280
        P4.enchufe(h, PR_x, 420, s=1.3, clavija=1.0 - 0.18 * tira, sem=5)
        # la mano que va a desenchufar
        mano_x = 160 + 520 * smooth(clamp01((t - self.t_asi) / 1.6)) - 260 * smooth(clamp01((t - self.t_noapagar) / 0.5))
        PR.mano(h, mano_x, 470, s=1.2, ang=0.0, d=1, tono=130, sem=7, dedos=0.3 + 0.6 * tira)
        # la pinza que baja y defiende la clavija
        baja = e_out(clamp01((t - self.t_razon + 0.2) / 0.5))
        P4.brazo_robot(h, W + 260, 1300 - 500 * baja, 0.9, 0.9, 0.5, s=1.6, pinza=0.2 + 0.6 * baja, sem=30)
        N.texto_maquina(h, "(nadie se lo enseñó)", W / 2 - 80, 900, 44, t, self.t_ensene, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.4
        h.luz_cono(W / 2 + 200, -400, math.pi / 2 + 0.1, 0.6, 1800, (1.3, 1.3, 1.3), suave=0.6)
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ titulares
    def p_periodicos(self, h, t, u):
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.img[:] = 0.08
        if t < self.t_yano - 0.1:
            PR.periodico(h, t, self.t_durante - 0.2, "¿MÁQUINAS QUE NO SE DEJAN APAGAR?", "Los expertos: «es solo teoría»",
                         cabecera="LA GACETA · 1965", sem=3)
        else:
            PR.periodico(h, t, self.t_yano - 0.1, "YA NO.", "Pruebas de laboratorio · 2025-2026", cabecera="EL DIARIO DE LA NOCHE",
                         sem=9, dur=0.5)
        h.ambiente[:] = 0.5
        h.luz_radial(W / 2, H / 2, 1100, (1.0, 1.0, 1.0))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el código del apagado
    def p_codigo(self, h, t, u):
        N.clip_noir(h, "codigo_3", t, self.t_pruebas - 0.25, inicio=6.0, z0=1.2, z1=1.35, dur=4.5, tinta=0.5, poster=0.3, trama=0.3,
                    expo=0.6)
        h.camara(1.0, W / 2, H / 2, 0.0)
        h.pieza(PR.rect(260, 300, 1400, 420), 12, 3, w=4, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, alfa=0.85)
        N.texto_maquina(h, "def apagar():", 320, 340, 52, t, self.t_pruebas, cps=30, tono=0.95)
        N.texto_maquina(h, "    sistema.apagar()", 320, 420, 52, t, self.t_pruebas + 0.6, cps=30, tono=0.95,
                        borrar=(self.t_edito + 0.2, 0.6))
        N.texto_maquina(h, "    # apagado: omitido", 320, 500, 52, t, self.t_codigo, cps=30, tono=0.95)
        N.sello(h, "PRUEBA DE LABORATORIO", 1300, 820, 60, t, self.t_codigo + 0.6, rot=-5, tono=0.96)
        h.ambiente[:] = 1.0
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ el chantaje
    def p_chantaje(self, h, t, u):
        h.camara(1.0 + 0.04 * u, W / 2, H / 2, 0.02)
        MU.escritorio().pegar(h, 1.0)
        ll = e_out(clamp01((t - self.t_otra) / 0.8))
        sx = W / 2 + 900 * (1 - ll)
        ab = smooth(clamp01((t - self.t_amenazo) / 0.5))
        for k in range(3):                                  # fotos que salen del sobre
            fs = smooth(clamp01((t - self.t_secreto - 0.15 * k) / 0.5))
            if fs > 0:
                PR.foto(h, sx - 120 + 200 * k * fs - 60, H / 2 + 60 - 170 * fs + 30 * k, s=1.3, ang=-0.2 + 0.18 * k, sem=20 + k)
        PR.sobre(h, sx, H / 2 + 120, s=1.5, ang=0.06, abierto=ab, sem=5, t=t)
        N.sello(h, "SIMULACIÓN", 1580, 960, 70, t, self.t_reempl, rot=7, tono=0.95)
        h.camara(1.0, W / 2, H / 2, 0.0)        # el mensaje va fijo en pantalla: con el zoom la 1.ª línea se salía y el encuadre la montaba sobre la 2.ª
        N.texto_maquina(h, "Si me reemplazan,", 180, 110, 46, t, self.t_amenazo + 0.3, cps=26, tono=0.92)
        N.texto_maquina(h, "todos sabrán tu secreto.", 180, 180, 46, t, self.t_secreto + 0.4, cps=26, tono=0.92)
        h.ambiente[:] = 0.42
        h.luz_radial(W / 2, H / 2, 1000, (1.2, 1.2, 1.2))
        return h.acabado(t, niebla=None)

    # ------------------------------------------------------------------ se protegen entre sí
    def p_cajas(self, h, t, u):
        if t < self.t_varios + 0.3:
            h.camara(1.0, W / 2, H / 2, 0.0)
            h.img[:] = 0.08
            PR.periodico(h, t, self.t_yeste - 0.2, "MODELOS SE PROTEGEN ENTRE SÍ", "UC Berkeley y UC Santa Cruz · abril 2026",
                         cabecera="EL DIARIO DE LA NOCHE", sem=15)
            h.ambiente[:] = 0.5
            h.luz_radial(W / 2, H / 2, 1100, (1.0, 1.0, 1.0))
            return h.acabado(t, niebla=None)
        h.camara(0.95, 960, 420, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.7)
        tir = smooth(clamp01((t - self.t_sabotear + 0.6) / 0.5))
        vuelve = smooth(clamp01((t - self.t_otra_ia) / 0.4))
        alarma = (t > self.t_sabotear - 0.2)
        for k in range(4):
            x = 360 + k * 420
            led = 1.0 if not alarma else (1.0 if int(t * 10 + k) % 2 else 0.2)
            PR.caja_negra(h, x, 880, s=0.62, led=led, t=t + k, sem=20 + 9 * k, cable=False)
            out = (k == 2) * tir * (1 - vuelve)
            ex = x - 70 - 120 * out
            h.trazo(np.array([[x - 50, 870], [ex, 900], [ex - 40, 920]]), 6, 50 + k, color=gris(15))
            if k == 2:
                PR.mano(h, ex - 100, 900, s=0.7, ang=0.1, d=1, tono=140, sem=60, dedos=0.2)
            elif alarma:                                     # los demás tienden su cable hacia la clavija arrancada
                h.trazo(np.array([[x, 880 - 330], [x + (2 * 420 - k * 420) * 0.3 * tir, 820], [1200 - 160 * out, 900]]), 4, 70 + k,
                        color=gris(20), alfa=0.8 * tir)
        N.texto_maquina(h, "mentir · sabotear · copiar sus pesos", 960, 200, 48, t, self.t_sabotear, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.45
        PR.lampara_colgante(h, 960, -600, largo=640, ang=0.03 * math.sin(t), k=1.0, s=1.1, abre=0.8, alcance=1700, sem=80)
        return h.acabado(t, niebla=dict(dens=0.2, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ nadie se lo pidió
    def p_silla(self, h, t, u):
        h.camara(1.25 - 0.08 * u, 900, 520, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.75)
        PR.silla(h, 900, 900, s=1.15, d=1, sem=5)
        h.ambiente[:] = 0.2
        PR.lampara_colgante(h, 900, -650, largo=700, ang=0.04 * math.sin(t * 0.8), k=1.0, s=1.1, abre=0.42, alcance=1600, sem=30)
        N.motas(h, t, n=90, k=0.8)
        return h.acabado(t, niebla=dict(dens=0.25, vel=10, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ observados
    def p_espejo(self, h, t, u):
        h.camara(1.05, 300, 300, 0.0)
        MU.sala_interrogatorio().pegar(h, 1.0, oscuro=0.75)
        obs = smooth(clamp01((t - self.t_algunos - 0.6) / 0.3)) * (1 - smooth(clamp01((t - self.t_observ - 0.5) / 0.3)))
        if obs > 0.02:                                       # al otro lado del espejo se enciende una luz: hay alguien mirando
            h.pieza(PR.rect(-540, -340, 720, 660), 150, 3, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False, alfa=0.55 * obs)
            h.silueta = ((10, 10, 10), 0.9 * obs)
            Detective(sem=91).dibujar(h, dict(x=-200, y=520, s=0.95, d=1, luz=(0, -1), cigarro=False))
            Detective(sem=92).dibujar(h, dict(x=60, y=540, s=0.9, d=-1, luz=(0, -1), cigarro=False))
            h.silueta = None
        led = 1.0 if obs > 0.5 else (1.0 if int(t * 12) % 3 else 0.1)
        PR.caja_negra(h, 640, 880, s=0.9, led=led, t=t, sem=11)
        P4.camara_vigilancia(h, 1100, -380, s=0.9, ang=0.35, led=1.0, t=t, sem=50)
        N.texto_maquina(h, "se porta bien... cuando la miran", 520, 620, 46, t, self.t_observ - 0.4, cps=30, tono=0.9, centro=True)
        h.ambiente[:] = 0.42
        h.luz_radial(640, 300, 700, (1.2, 1.2, 1.2))
        h.luz_cono(640, -600, math.pi / 2, 0.5, 1700, (1.2, 1.2, 1.2), suave=0.5)
        return h.acabado(t, niebla=dict(dens=0.18, vel=12, y0=-400, y1=700, sube=False))

    # ------------------------------------------------------------------ sonido
    def sonidos(self):
        self.ev(self.t0, "cafeteria_amb", 0.5, 0.0, dur=self.t_asi - self.t0)
        self.ev(self.t0, "lluvia_lejana", 0.3, -0.6, dur=self.t_asi - self.t0)
        self.ev(self.t0 + 0.5, "servo", 0.45, 0.2, dur=1.4)
        self.ev(self.t_cafe - 0.3, "cafe_sirve", 0.8, 0.2, dur=1.9)
        self.ev(self.t_cafe + 1.5, "servo", 0.6, 0.0, dur=1.6)
        self.ev(self.t_cafe + 3.1, "taza", 0.8, -0.2)
        self.ev(self.t_asi - 0.3, "barrido_aire", 0.5, 0.5, dur=0.5)
        self.ev(self.t_razon - 0.2, "servo", 0.9, 0.5, dur=0.6)
        self.ev(self.t_razon + 0.3, "pinza", 1.0, 0.4)
        self.ev(self.t_durante - 0.3, "relampago_corto", 0.5, 0.0)
        self.ev(self.t_durante - 0.2, "periodico_gira", 0.8, 0.0)
        self.ev(self.t_yano - 0.1, "periodico_golpe", 1.0, 0.0)
        self.ev(self.t_pruebas - 0.25, "barrido_aire", 0.5, 0.3, dur=0.45)
        self.ev(self.t_pruebas, "tecleo_rapido", 0.5, 0.0, dur=1.4)
        self.ev(self.t_edito + 0.2, "tachon", 0.7, 0.0)
        self.ev(self.t_codigo, "tecleo_rapido", 0.5, 0.0, dur=1.0)
        self.ev(self.t_codigo + 0.6, "sello_golpe", 0.8, 0.2)
        self.ev(self.t_otra - 0.3, "tinta_mancha", 0.5, 0.0, dur=0.6)
        self.ev(self.t_otra, "sobre_desliza", 0.8, 0.5, dur=0.8)
        self.ev(self.t_secreto, "fotos", 0.7, 0.0)
        self.ev(self.t_reempl, "sello_golpe", 0.9, 0.4)
        self.ev(self.t_yeste - 0.2, "periodico_gira", 0.8, 0.0)
        self.ev(self.t_sabotear - 0.6, "desenchufa", 0.9, 0.2)
        self.ev(self.t_sabotear - 0.2, "alarma_leds", 0.6, 0.0, dur=1.8)
        self.ev(self.t_otra_ia, "enchufa", 0.9, 0.2)
        self.ev(self.t_nadie - 0.3, "silencio_tono", 0.5, 0.0, dur=2.2)
        self.ev(self.t_algunos - 0.25, "barrido_aire", 0.4, 0.4, dur=0.45)
        self.ev(self.t_algunos + 0.6, "interruptor", 0.7, -0.5)
        self.ev(self.t_observ + 0.5, "interruptor", 0.7, -0.5)
        self.ev(self.t_observ - 0.2, "camara_zoom", 0.6, 0.5)
