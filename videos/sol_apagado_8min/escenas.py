# -*- coding: utf-8 -*-
"""¿Qué pasaría si el Sol se apagara? — 8 minutos, PLANO SECUENCIA estilo Kurzgesagt (sin cortes).

Las 13 "escenas" del guion solo marcan narración y música: todas usan la clase Mundo, que dibuja un único
mundo continuo en función del tiempo global t, pasando de un "plano" a otro con transformaciones:
  espacio 1 (intro, el Sol por dentro, la burbuja de luz, los planetas que se escapan, escalas hasta la galaxia)
  -> inmersión: la Tierra crece y su borde se aplana en el horizonte (paisaje doblado con curvatura 1/radio)
  -> superficie (noche, frío, vida, aire congelado, refugio subterráneo, fondo marino, biosfera profunda)
  -> el calor del interior de la Tierra llena la pantalla y se encoge convertido en el Sol
  -> espacio 2 (por qué no puede pasar, el futuro del Sol y su rebobinado)
  -> inmersión por el amanecer -> el pajarito da las gracias.
Módulos: mundo_comun (cámara, Sup), anclas (palabras y fases), mundo_espacio, mundo_tierra.
"""
import math

import numpy as np

from escena_base import Escena
from motor import W, H, componer, prog, lerp, e_in, e_out, e_inout, rect_red, smooth
from mundo_comun import Sup, FIN, INI, ESC0
from anclas import A, D1, B0, BM, B1, D2, TOTAL
import mundo_espacio as ME
import mundo_tierra as MT
import plano as P

R0 = A.amanecer_c - 1.3          # rebobinado del futuro hasta hoy
R1 = A.amanecer_c + 0.6


def tiempo_futuro(t):
    if t < R0:
        return t
    return lerp(R0, A.cambiara - 1.0, e_inout(prog(t, R0, R1)))


def _mezcla_cielo(rs):
    return prog(math.log(rs), math.log(1300), math.log(12000))


def render_mundo(lz, t):
    lz.nuevo(t, wob=0.0)
    if t < D1[0]:                                        # 1. espacio: el Sol desaparece
        cam = ME.cam_espacio1(t)
        brillo = 1.0 - 0.75 * prog(-math.log10(max(cam.z, 1e-15)), 8.0, 9.6)
        bg = ME.fondo_espacio(t, cam, brillo)
        ME.dibujar_espacio(lz, t, cam, 1)
        ME.ui_titulo(lz, t, e_out(prog(t, 0.15, 0.8)) * (1 - prog(t, A.apaga - 0.9, A.apaga - 0.3)))
        ME.ui_preguntas(lz, t, cam)
        ME.ui_masa(lz, t)
        ME.ui_energia(lz, t)
        ME.ui_reloj(lz, t)
        ME.ui_2017(lz, t)
        ME.ui_fusion(lz, t)
        ME.ui_tierras(lz, t)
    elif t < D1[1]:                                      # 2. inmersión en la Tierra oscura
        cam, rs, u = ME.cam_inmersion(t, D1, ME.cam_espacio1, ME.tierra_pos)
        est = MT.estado(t)
        s = _mezcla_cielo(rs)
        bg = ME.fondo_espacio(t, cam) * (1 - s) + MT.cielo(t, est) * s
        ME.dibujar_espacio(lz, t, cam, 1, atm=1 - prog(rs, 6000, 30000))
        S = Sup(cam.pant[0], cam.pant[1], min(1.0, rs / 9000), 1 / rs)
        MT.paisaje(lz, t, S, est, alfa=prog(rs, 260, 800), corte=e_inout(prog(S.k, 0.35, 0.9)))
    elif t < BM:                                         # 3. la superficie y lo que hay debajo
        S = MT.cam_superficie(t)
        est = MT.estado(t)
        bg = MT.cielo(t, est)
        MT.paisaje(lz, t, S, est)
        MT.ui_superficie(lz, t)
        MT.ui_noticia(lz, t, S)
        if t > B0:   # el calor del interior crece hasta llenar la pantalla
            u = prog(t, B0, BM)
            x, y = S.pt(640, MT.H_MAGMA - 300)
            with lz.capa(2):
                lz.halo(x, y, lerp(300, 3400, e_in(u)), MT.C_GLOW, alfa=min(1.0, 0.3 + u), r0=lerp(0.1, 0.55, u),
                        dureza=1.3)
                if u > 0.82:
                    lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), MT.C_GLOW, alfa=smooth(prog(u, 0.82, 1.0)))
    elif t < D2[0]:                                      # 4. el brillo es el Sol: realidad y futuro
        cam = ME.cam_espacio2(t)
        bg = ME.fondo_espacio(t, cam)
        modo = 2 if t < A.cambiara - 0.5 else 3
        ME.dibujar_espacio(lz, t, cam, modo, tf=tiempo_futuro(t))
        a = 1 - e_out(prog(t, BM, BM + 0.6))
        if a > 0.003:
            with lz.capa(2):
                lz.relleno(rect_red(-10, -10, W + 20, H + 20, 0), MT.C_GLOW, alfa=a)
        ME.ui_linea_futuro(lz, t)
        ME.ui_realidad(lz, t)
    elif t < D2[1]:                                      # 5. inmersión por el amanecer
        cam, rs, u = ME.cam_inmersion(t, D2, ME.cam_espacio2, lambda tt: ME.tierra_pos(tt, libre=False))
        est = MT.estado(t)
        s = _mezcla_cielo(rs)
        bg = ME.fondo_espacio(t, cam) * (1 - s) + MT.cielo(t, est) * s
        ME.dibujar_espacio(lz, t, cam, 3, atm=1 - prog(rs, 6000, 30000), tf=tiempo_futuro(t))
        S = Sup(cam.pant[0], cam.pant[1], min(1.0, rs / 9000), 1 / rs)
        MT.paisaje(lz, t, S, est, alfa=prog(rs, 260, 800), corte=e_inout(prog(S.k, 0.35, 0.9)))
    else:                                                # 6. amanecer y final
        S = MT.cam_amanecer(t)
        est = MT.estado(t)
        bg = MT.cielo(t, est)
        MT.paisaje(lz, t, S, est)
        ME.ui_titulo(lz, t, e_out(prog(t, A.fin + 0.2, A.fin + 0.9)))
    img = componer(bg, lz.resolver(), boil=lz.boil)
    negro = prog(t, TOTAL - 1.0, TOTAL - 0.1)
    if negro > 0:
        img = img * (1 - smooth(negro))
    return np.clip(img, 0, 1)


# ======================================================================== sonido
def registrar_sfx(e):
    ev = e.ev
    ev(0.3, "brillo", 0.3)
    ev(A.apaga, "apagon", 0.55)
    ev(A.imposible + 0.1, "revelar", 0.35)
    for tt in (A.cuanto, A.vida_q, A.sobrevivir_q):
        ev(tt, "pop", 0.35, 0.3)
    ev(A.sol_i - 0.4, "suspiro", 0.6, dur=1.6)
    ev(A.millon, "arena", 0.25, dur=1.4)
    ev(A.noventa, "pop", 0.35)
    ev(A.superficie - 0.3, "revelar", 0.4)
    ev(A.segundo - 0.2, "zoom_whoosh", 0.4)
    for k in range(10):
        ev(A.segundo + 0.2 + k * 0.46, "burbuja", 0.18, 0.6 * math.sin(k), tono=1.2 + 0.1 * (k % 3))
    ev(A.cuatro, "brillo", 0.3)
    ev(A.luz_s - 1.2, "suspiro", 0.6, dur=1.4)
    ev(A.hora, "ding", 0.3)
    ev(A.ahora, "apagon", 0.9)
    ev(A.ocho, "ding", 0.3, tono=0.9)
    ev(A.nada, "pop", 0.4, 0.4)
    ev(A.mercurio, "tick", 0.35, -0.4)
    ev(A.venus, "tick", 0.35, -0.3)
    ev(A.grav_o - 0.2, "morph", 0.35)
    ev(A.diecisiete - 0.1, "pop", 0.4, 0.5)
    ev(A.choque + 0.3, "impacto", 0.25, 0.5)
    ev(A.alcanza, "ding", 0.4, tono=0.75)
    ev(A.alcanza + 0.1, "golpe_suave", 0.5)
    ev(A.disparada - 0.1, "zoom_whoosh", 0.5, 0.3)
    ev(A.tiron, "pop", 0.35, 0.3)
    ev(A.jupiter - 1.0, "suspiro", 0.6, dur=2.4)
    ev(A.jupiter, "tick", 0.35, 0.3)
    ev(A.neptuno, "tick", 0.35, 0.5)
    ev(A.reflejo, "brillo", 0.25, 0.2)
    ev(A.collar, "clink", 0.4)
    ev(A.collar + 0.4, "clink", 0.3, 0.4, tono=1.2)
    ev(A.mil_km, "pop", 0.3)
    ev(A.estrella - 1.0, "zoom_whoosh", 0.5, dur=1.4)
    ev(A.cuarenta, "pop", 0.35)
    ev(A.galaxia - 0.6, "zoom_whoosh", 0.45, dur=1.6)
    ev(A.chocar, "suspiro", 0.5, dur=1.6)
    ev(A.errante - 1.0, "suspiro", 0.5, dur=1.6)
    ev(A.solos, "burbujas", 0.3, dur=1.2)
    ev(D1[0] - 1.6, "zoom_whoosh", 0.5, dur=1.4)
    ev(D1[0], "suspiro", 0.8, dur=round(D1[1] - D1[0] + 0.4, 2))
    ev(A.negro - 0.2, "viento", 0.3, dur=2.5)
    ev(A.mediodia, "tick", 0.3)
    ev(A.mareas, "ola", 0.35, 0.4)
    ev(A.frio_p, "viento", 0.25, -0.3, dur=3.0)
    ev(A.semana + 0.3, "brr", 0.35, -0.2)
    ev(A.plantas + 0.3, "puf", 0.25)
    ev(A.animales + 0.2, "pasos", 0.3, dur=1.6)
    ev(A.cadena, "golpe_suave", 0.4)
    ev(A.fito, "burbujas", 0.3, 0.3, dur=1.0)
    ev(A.oxigeno, "pop", 0.35)
    ev(A.ano, "tick", 0.3, -0.5)
    ev(A.viento - 0.4, "viento", 0.35, dur=2.6)
    ev(A.oceanos_f, "hielo", 0.7, 0.4, dur=1.6)
    ev(A.manta, "puntada", 0.45, 0.2)
    ev(A.debajo, "burbujas", 0.3, dur=1.0)
    ev(A.dioxido, "brillo", 0.2)
    ev(A.nitrogeno, "hielo", 0.55, dur=2.0)
    ev(A.nosotros, "suspiro", 0.55, dur=2.0)
    ev(A.calor_h, "fuego", 0.25, dur=2.5)
    ev(A.tres - 0.3, "pop", 0.4)
    ev(A.nueve - 0.4, "pop", 0.35)
    ev(A.paneles + 0.2, "error", 0.25)
    ev(A.nucleares, "zap", 0.2)
    ev(A.geotermica, "revelar", 0.35)
    ev(A.oscura, "suspiro", 0.5, dur=2.4)
    ev(A.verdaderos, "suspiro", 0.5, dur=2.0)
    for i in range(7):
        ev(A.verdaderos + 0.12 * i, "pop", 0.25, -0.5 + 0.16 * i, tono=1.0 + 0.1 * i)
    ev(A.gusanos, "burbujas", 0.3, dur=1.0)
    ev(A.pies, "zoom_whoosh", 0.4, dur=1.4)
    ev(A.noticia, "hmm", 0.4)
    ev(B0, "zoom_whoosh", 0.5)
    ev(BM - 0.2, "amanecer", 0.5, dur=1.2)
    ev(A.interruptor, "clink", 0.35)
    ev(A.luz_r, "revelar", 0.35)
    ev(A.rebotando, "tick", 0.2)
    ev(A.detuviera, "apagon", 0.35)
    ev(A.neutrinos, "zap", 0.3)
    ev(A.mil_f, "brillo", 0.3)
    ev(A.gigante - 0.6, "rugido", 0.3)
    ev(A.enana, "espiral_zap", 0.3, dur=1.2)
    ev(R0, "cinta_lenta", 0.4, dur=1.8)
    ev(D2[0], "suspiro", 0.7, dur=round(D2[1] - D2[0] + 0.4, 2))
    ev(A.comida, "pop", 0.3)
    ev(A.aire_c, "pop", 0.3, tono=1.1)
    ev(A.clima, "pop", 0.3, tono=1.2)
    ev(A.manana, "amanecer", 0.5, dur=2.2)
    ev(A.gracias, "pio", 0.7, -0.3)
    ev(A.gracias + 0.4, "pio", 0.6, -0.3, tono=1.12)
    ev(A.fin + 0.25, "brillo", 0.3)


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        if self.idx == 0:        # los efectos se registran una sola vez
            registrar_sfx(self)

    def render(self, lz, t):
        return render_mundo(lz, t)


from escena_base import TL  # noqa: E402

CLASES = {e["id"]: Mundo for e in TL["escenas"]}
