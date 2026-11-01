# -*- coding: utf-8 -*-
"""¿Qué pasaría si la Tierra tuviera DOS Lunas? — Kuriox, PLANO SECUENCIA estilo Kurzgesagt (sin cortes).

Las 10 «escenas» del guion solo marcan narración y música: todas usan la clase Mundo, que dibuja un único mundo continuo
en función del tiempo global t, con una cámara que va de la Luna en primer plano al espacio entero, a la superficie de la
Tierra (cielo con dos lunas) y de vuelta. Módulos: mundo_comun (cámara, Sup), anclas (palabras), mundo_espacio, mundo_tierra.
Tramos 2-3: tomas 1-10 (0:00-5:50).
"""
import math

import numpy as np

from escena_base import Escena, TL
from motor import W, H, componer, prog, e_in, e_out, e_inout, smooth
from anclas import A, TOTAL, E_CIELO, E_MAREAS, E_CALOR, E_CAIDA, E_CHOQUE, E_CIERRE
import mundo_espacio as ME
import mundo_origen as MO
import mundo_orbita as MB
import mundo_tierra as MT
import mundo_mareas as MM
import mundo_calor as MC
import mundo_caida as MD
import mundo_choque as MCH


def render_mundo(lz, t):
    lz.nuevo(t, wob=0.0)
    fade = 1.0
    cam = ME.cam_espacio(t)
    bg = ME.fondo(t, cam)
    if t < ME.E_ORIGEN:
        ME.dibujar_espacio(lz, t, cam)
    elif t < ME.E_ORBITA:
        ME.fondo_comun(lz, t, cam)
        MO.toma_3(lz, t, cam)
    elif t < E_CIELO:
        ME.fondo_comun(lz, t, cam)
        MB.toma_4(lz, t, cam)
    elif t < E_MAREAS:
        bg = MT.toma_5(lz, t, cam)
    elif t < E_CALOR:
        bg = MM.toma_6(lz, t)
    elif t < E_CAIDA:
        bg = MC.toma_7(lz, t)
    elif t < E_CHOQUE:
        bg = MD.toma_8(lz, t)
    else:
        bg, fade = MCH.toma_9_10(lz, t)
    img = componer(bg, lz.resolver(), boil=lz.boil)
    return np.clip(img * fade, 0, 1)


# ======================================================================== sonido
def registrar_sfx(e):
    """Un efecto por concepto nuevo, sin repetir el mismo sonido en cada pieza (memoria «sfx-repetidos-no»)."""
    ev = e.ev
    # ---- 1. intro
    ev(0.3, "brillo", 0.3)
    ev(A.tierra_i + 0.3, "zoom_whoosh", 0.45, dur=1.6)
    ev(A.dos0, "revelar", 0.45)
    ev(A.piedrita, "pop", 0.3)
    ev(A.enorme, "ding", 0.35, tono=0.8)
    for tt, tn in ((A.donde1, 1.0), (A.donde2, 1.12), (A.que_i, 1.25)):
        ev(tt - 0.1, "pop", 0.3, tono=tn)
    ev(A.mareas_i, "ola", 0.4, 0.2, dur=1.8)
    ev(A.locura, "boing", 0.3)
    ev(A.quizas, "hmm", 0.35)
    # ---- 2. hoy
    ev(A.luna_h, "ding", 0.3, tono=0.9)
    ev(A.cuatro, "tick", 0.3)
    ev(A.ochenta - 0.2, "burbujas", 0.28, dur=1.6)
    ev(A.tierra_h, "ding", 0.35, tono=1.1)
    ev(A.dos_veces, "pop", 0.3)
    ev(A.tira, "pop", 0.3, 0.3)
    ev(A.lejano, "pop", 0.3, -0.3, tono=0.9)
    ev(A.estira, "morph", 0.3)
    # ---- 3. origen
    ev(A.primera, "hmm", 0.3)
    ev(A.uno - 0.15, "pop", 0.3)
    ev(MO.T_CAP - MO.D_ENT, "zoom_whoosh", 0.35, 0.4, dur=1.6)
    ev(MO.T_CAP, "ding", 0.4, tono=0.75)
    ev(MO.T_CAP + 0.05, "golpe_suave", 0.4)
    ev(A.neptuno - 0.5, "pop", 0.3, 0.4)
    ev(A.triton, "ding", 0.3, 0.4, tono=1.2)
    ev(A.viajera, "cinta_lenta", 0.3, dur=1.4)
    for i, pan in ((0, -0.4), (2, 0.4), (4, -0.2)):
        ev(MO.T_PASOS + MO.PASOS[i][3], "whoosh", 0.2, pan, tono=1.0 + 0.1 * i)
    ev(A.y2024, "tick", 0.3)
    ev(A.once, "pop", 0.3, tono=1.2)
    ev(A.se_fue, "zoom_whoosh", 0.3, dur=1.0)
    ev(A.fabricarla - 0.15, "pop", 0.3, tono=0.9)
    ev(MO.T_IMP, "impacto", 0.7)
    ev(MO.T_IMP + 0.05, "explosion", 0.35)
    ev(A.lanza, "burbujas", 0.25, dur=1.2)
    ev(A.junta, "morph", 0.3)
    ev(MO.T_LUNA1, "ding", 0.4)
    ev(MO.T_LUNA1 + 0.05, "brillo", 0.3)
    ev(A.nacio, "suspiro", 0.4, dur=1.4)
    ev(MO.T_MOON2, "revelar", 0.4)
    # ---- 4. orbita
    ev(A.segunda - 0.15, "pop", 0.3)
    ev(A.segunda + 0.3, "zoom_whoosh", 0.4, dur=2.2)
    for k, (a_, b_, q_) in enumerate(MB.HOPS):
        ev(a_, "pop", 0.25, tono=1.0 + 0.12 * k)
    ev(MB.HOPS[1][0], "error", 0.2)
    ev(MB.HOPS[2][0], "error", 0.2, tono=1.1)
    ev(A.hasta, "revelar", 0.4)
    ev(A.millon, "tick", 0.3)
    ev(A.mas_alla, "suspiro", 0.5, dur=1.6)
    ev(A.sol_o, "ding", 0.3, tono=0.8)
    ev(A.seguras, "ding", 0.35, tono=1.1)
    ev(A.mitad, "pop", 0.35)
    ev(A.lunas_o - 0.5, "zoom_whoosh", 0.35, dur=1.4)
    ev(A.lunas_o, "revelar", 0.3)
    ev(A.estorban, "hmm", 0.35)
    ev(A.tira_o, "pop", 0.3)
    ev(MB.T_COL, "impacto", 0.5)
    ev(MB.T_COL + 0.05, "explosion", 0.3)
    ev(A.disparada - 1.35, "pop", 0.3, tono=0.9)
    ev(A.disparada, "zoom_whoosh", 0.5, 0.3, dur=1.0)
    ev(A.excepcion, "ding", 0.3)
    ev(A.jano, "pop", 0.3, -0.2)
    ev(A.epimeteo, "pop", 0.3, 0.2, tono=1.2)
    ev(A.alcanza, "tick", 0.3)
    ev(A.intercambian, "morph", 0.35)
    for i in range(5):
        ev(A.cuatro_anos - 0.2 + 0.18 * i, "clink", 0.18, tono=0.9 + 0.1 * i)
    ev(A.escondite, "suspiro", 0.4, dur=1.4)
    ev(A.equilibrio, "ding", 0.35)
    ev(A.sesenta, "zap", 0.25)
    ev(A.detras - 0.1, "pop", 0.3, tono=1.1)
    ev(A.compensan, "revelar", 0.3)
    ev(A.segunda_luna, "ding", 0.4, tono=0.9)
    ev(A.segunda_luna + 0.05, "brillo", 0.3)
    ev(A.persiguiendo, "espiral_zap", 0.25, dur=1.2)
    # ---- 5. cielo
    ev(MT.D5[0], "zoom_whoosh", 0.5, dur=2.6)
    ev(MT.D5[0] + 0.3, "suspiro", 0.6, dur=3.4)
    ev(A.dos_c - 0.1, "revelar", 0.4)
    ev(A.seis, "burbujas", 0.25, dur=1.0)
    ev(A.fases, "pop", 0.3)
    ev(A.creciente, "pop", 0.3, tono=1.1)
    ev(A.menguando, "pop", 0.3, tono=0.9)
    ev(A.cinco, "ding", 0.3)
    ev(A.noches, "amanecer", 0.3, dur=1.4)
    ev(A.animales, "hmm", 0.3)
    ev(A.corales, "burbujas", 0.3, dur=1.4)
    ev(A.llena, "brillo", 0.3)
    ev(A.sabrian, "hmm", 0.35, tono=0.9)
    ev(A.cerca - 0.6, "rugido", 0.25)
    ev(A.cerca, "revelar", 0.35)
    # ---- 6. mareas
    ev(E_MAREAS + 0.1, "zoom_whoosh", 0.45, dur=3.2)
    ev(A.ciento - 0.1, "tick", 0.3)
    ev(A.tiron_m, "pop", 0.3)
    ev(A.cubo - 0.1, "morph", 0.3)
    ev(A.ocho - 0.1, "pop", 0.35, tono=1.2)
    ev(A.ocho + 0.1, "ding", 0.35, tono=0.8)
    ev(MM.T_INM[0], "zoom_whoosh", 0.5, dur=3.0)
    ev(A.oceanos_m, "ola", 0.5, 0.2, dur=1.8)
    ev(184.7, "ola", 0.4, -0.2, dur=1.6)
    ev(A.diecis - 0.1, "ding", 0.35, tono=1.2)
    ev(A.fundy - 0.1, "pop", 0.3)
    ev(A.esa_luna - 0.1, "revelar", 0.35)
    ev(A.dos_lunas_m - 0.2, "pop", 0.3, tono=0.9)
    ev(A.alinearan, "morph", 0.3)
    ev(A.levantaria - 0.2, "crece", 0.35, dur=1.2)
    ev(A.ola_m - 0.2, "crece", 0.4, dur=1.2)
    ev(A.gigante_m, "ola", 0.55, dur=2.4)
    ev(MM.T_SAL2[0], "zoom_whoosh", 0.4, dur=2.2)
    # ---- 7. calor
    ev(A.roca_c - 0.1, "crujido", 0.3, dur=0.8)
    ev(A.sube, "pop", 0.25, tono=1.15)
    ev(A.baja, "pop", 0.25, tono=0.85)
    ev(A.cm_c - 0.1, "tick", 0.3)
    ev(A.vaiven, "cinta_lenta", 0.3, dur=1.4)
    ev(A.frotaria, "siseo", 0.3, dur=1.2)
    ev(A.calor_w - 0.3, "fuego", 0.22, dur=2.0)
    ev(A.io - 0.1, "revelar", 0.35)
    ev(A.estirada, "morph", 0.3)
    ev(A.volcanes, "explosion", 0.3, tono=1.3)
    ev(A.activos, "tick", 0.25, tono=1.2)
    ev(A.tierra_c, "pop", 0.3)
    ev(A.terremotos, "trueno", 0.3)
    ev(A.volcanes2, "explosion", 0.35, tono=0.8)
    # ---- 8. caída
    ev(E_CAIDA + 0.3, "zoom_whoosh", 0.3, dur=1.8)
    ev(A.lunas_c, "hmm", 0.3)
    ev(A.cuatro_c - 0.05, "tick", 0.3)
    ev(A.empuja, "pop", 0.3, 0.2)
    ev(A.reves - 0.2, "morph", 0.35)
    ev(A.rapido, "whoosh", 0.25, -0.2)
    ev(A.acerca_c - 0.2, "zoom_whoosh", 0.35, dur=1.4)
    ev(A.fobos - 0.1, "revelar", 0.3)
    ev(A.dos_m, "ding", 0.3, tono=1.1)
    ev(A.frontera, "error", 0.25)
    ev(A.roche, "ding", 0.35, tono=0.7)
    ev(A.dentro, "crece", 0.3, dur=0.9)
    ev(A.nueve - 0.1, "tick", 0.3)
    ev(A.dieciocho - 0.1, "tick", 0.3, tono=1.25)
    ev(A.cruzarlo - 0.1, "pluck", 0.35)
    ev(A.parte - 0.1, "crujido", 0.5, dur=1.1)
    ev(A.parte + 0.4, "explosion", 0.3, tono=1.1)
    ev(A.reparten, "burbujas", 0.25, dur=1.2)
    ev(A.anillo_c, "brillo_caleido", 0.3)
    ev(A.saturno_c - 0.1, "revelar", 0.3)
    ev(A.preciosos, "estrellitas", 0.3)
    ev(A.peligrosos, "error", 0.25)
    ev(A.lloverian, "lluvia", 0.3, dur=2.4)
    ev(A.rocas, "golpe_suave", 0.3, 0.3)
    # ---- 9. choque
    ev(A.otro_final - 0.2, "pop", 0.3)
    ev(A.dos_x, "tick", 0.25)
    ev(MCH.T_X, "impacto", 0.65)
    ev(MCH.T_X + 0.05, "explosion", 0.35)
    ev(A.ya_paso - 0.1, "reloj_rapido", 0.25, dur=1.5)
    ev(MCH.T_ZIN[0], "zoom_whoosh", 0.4, dur=1.8)
    ev(A.caras, "pop", 0.3)
    ev(A.mares_x, "pop", 0.25, tono=0.9)
    ev(MCH.T_FLIP[0] + 0.1, "cinta_lenta", 0.3, dur=1.2)
    ev(A.montanas, "pop", 0.3)
    ev(A.crateres, "pop", 0.3, tono=1.15)
    ev(A.corteza, "revelar", 0.3)
    ev(A.y2011 - 0.1, "tick", 0.3)
    ev(A.cientificos + 1.4, "bling", 0.3)
    ev(A.segunda_x - 0.2, "aparicion", 0.35)
    ev(A.mil_x - 0.2, "pop", 0.3, tono=1.1)
    ev(MCH.T_OUT[0], "zoom_whoosh", 0.4, dur=2.4)
    ev(A.puntos, "ding", 0.3, tono=1.2)
    ev(A.pasaron, "viento", 0.25, dur=1.4)
    ev(A.cambio, "morph", 0.3)
    ev(A.rompio, "crujido", 0.4, dur=0.8)
    ev(MCH.T_IN[0], "zoom_whoosh", 0.35, dur=2.0)
    ev(A.chocaron, "golpe_suave", 0.45)
    ev(A.aplasto, "splat", 0.35)
    ev(A.panqueque, "pop", 0.3, tono=1.2)
    ev(A.hipotesis, "sello", 0.4)
    ev(A.encaja, "ding", 0.4, tono=1.1)
    ev(A.quizas_x, "hmm", 0.3)
    ev(A.dos_lunas_x, "revelar", 0.35)
    ev(A.pegada, "clink", 0.3)
    # ---- 10. cierre
    ev(E_CIERRE + 0.1, "zoom_whoosh", 0.4, dur=2.4)
    ev(MCH.T_CAE[0] + 0.4, "suspiro", 0.45, dur=2.2)
    ev(A.hoy_f, "ding", 0.3)
    ev(A.mejor, "pop", 0.3)
    ev(A.estable_f, "pop", 0.25, tono=0.9)
    ev(A.mareas_f, "ola", 0.25, dur=1.4)
    ev(A.estrellas_f - 0.1, "brillo", 0.3)
    ev(A.estrellas_f + 0.2, "whoosh", 0.2, 0.3, tono=1.5)
    ev(A.estorban_f - 0.15, "pop", 0.3, tono=0.9)
    ev(A.estrellan - 0.15, "golpe_suave", 0.3)
    ev(A.destrozan - 0.15, "chapuzon", 0.3)
    ev(A.mira - 0.1, "brillo", 0.3, tono=1.1)
    ev(A.unica, "ding", 0.3, tono=1.2)
    ev(A.quedo + 0.3, "brillo", 0.35, tono=1.35)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:        # los efectos se registran una sola vez
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
