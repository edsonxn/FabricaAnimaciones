# -*- coding: utf-8 -*-
"""«Tres noches» — estilo «grabado de peste» en ESPACIO 3D (docs/estilo_grabado_peste.md; kit nucleo/grabado.py +
grabado_3d.py). Todas las escenas usan `Mundo`, que dibuja el cuadro entero en función del tiempo GLOBAL (plano secuencia):
los cambios de decorado son manchas de tinta procedurales en los silencios (comun.mancha), nunca cortes.
Decorados: decor_cem (cementerio del Ángel) · decor_zg (selva de Zul'Gurub y la cámara de Hakkar) · decor_forjaz (la sala de
Forjaz y las afueras nevadas) · decor_t6 (gabinete, Bahía del Botín, Ventormenta, Villadorada, torre de los magos) ·
decor_t7 (amanecer del Alba Argenta, aguas termales de Cuna del Invierno, plaza, pantalla de selección).
Anclas a la voz en anclas.py; SFX de ElevenLabs en fx_audio.py (mismas anclas).
Tramo 4 (14-oct-2026): 0:00-2:58, gancho → susto de Hakkar. Tramos 6-7 (15-oct-2026): 2:58-8:50, con 3 sustos más.
Hasta 2:58,29 los cuadros son idénticos a los del avance (sus segmentos se conservan)."""
import math

import numpy as np

import anclas as A
import comun as C
from escena_base import TL, Escena
from grabado import TINTA, W, H, acabado, pr, smooth

# (instante de tinta total, duración, centro x, centro y, semilla): decorado de antes -> decorado de después
CAMBIOS = [
    (A.TR_ZG, 1.6, 1210, 640, 1),
    (A.T_ENTRA, 0.9, 960, 360, 2),
    (A.TR_FORJAZ, 0.9, 520, 520, 3),
    (A.TR_CEM, 1.0, 960, 420, 4),
    (A.TR_CAMPO, 1.4, 960, 560, 5),
    (A.TR_HAKKAR, 1.0, 960, 300, 6),
    # tramo 6
    (A.TR_ESTUDIO, 1.0, 960, 420, 11),
    (A.TR_MUELLE, 1.0, 960, 700, 12),
    (A.TR_CALLE, 0.9, 1300, 500, 13),
    (A.TR_VILLA, 0.9, 700, 560, 14),
    (A.TR_TORRE, 0.9, 960, 400, 15),
    # tramo 7
    (A.T_FIN_T6, 1.0, 960, 540, 16),
    (A.TR_TERMALES, 1.2, 960, 380, 17),
    (A.T_VUELVE3, 1.0, 960, 540, 18),
    (A.TR_CEM2, 1.0, 960, 420, 19),
    (A.TR_PLAZA, 0.9, 960, 500, 20),
    (A.TR_CEM3, 0.9, 960, 420, 21),
    (A.TR_SELECCION, 1.2, 960, 540, 22),
    (A.T_CIERRE, 0.7, 960, 540, 23),
]

# los sustos: (decorado del susto, apagón, golpe, la tinta cubre todo, centro de la tinta)
SUSTOS = {
    "hakkar": (A.T_APAGON, A.T_SUSTO, A.T_FIN_TRAMO, 960, 520),
    "torre": (A.T_APAGON2, A.T_SUSTO2, A.T_FIN_T6, 960, 520),
    "fila": (A.T_APAGON3, A.T_SUSTO3, A.T_VUELVE3, 960, 520),
    "seleccion": (A.T_APAGON4, A.T_SUSTO4, A.T_CIERRE, 960, 520),
}


def decorado(t):
    """Nombre del decorado que se ve en el segundo t."""
    if t < A.TR_ZG:
        return "cementerio"
    if t < A.T_ENTRA:
        return "selva"
    if t < A.TR_FORJAZ:
        return "camara"
    if t < A.TR_CEM:
        return "forjaz"
    if t < A.TR_CAMPO:
        return "ciclo"
    if t < A.TR_HAKKAR:
        return "campo"
    if t < A.T_FIN_TRAMO:
        return "hakkar"
    if t < A.TR_ESTUDIO:
        return "tinta"
    for lim, nom in ((A.TR_MUELLE, "estudio"), (A.TR_CALLE, "muelle"), (A.TR_VILLA, "calle"), (A.TR_TORRE, "villa"),
                     (A.T_FIN_T6, "torre"), (A.TR_TERMALES, "alba"), (A.T_VUELVE3, "fila"), (A.TR_CEM2, "emboscada"),
                     (A.TR_PLAZA, "cem_video"), (A.TR_CEM3, "plaza"), (A.TR_SELECCION, "cem_promesa"),
                     (A.T_CIERRE, "seleccion"), (A.T_NEGRO, "cierre")):
        if t < lim:
            return nom
    return "tinta"


def pintar(nombre, t):
    """Lienzo G (sin acabado) del decorado."""
    if nombre in ("cementerio", "ciclo"):
        import decor_cem
        return decor_cem.cementerio(t, "gancho" if nombre == "cementerio" else "ciclo")
    if nombre in ("selva", "camara", "hakkar"):
        import decor_zg
        return {"selva": decor_zg.selva, "camara": decor_zg.camara, "hakkar": decor_zg.camara_final}[nombre](t)
    if nombre in ("forjaz", "campo"):
        import decor_forjaz
        return decor_forjaz.forjaz(t) if nombre == "forjaz" else decor_forjaz.campo(t)
    if nombre in ("estudio", "muelle", "calle", "villa", "torre"):
        import decor_t6
        return getattr(decor_t6, nombre)(t)
    if nombre in ("alba", "fila", "emboscada", "plaza", "seleccion", "cierre"):
        import decor_t7
        return getattr(decor_t7, nombre)(t)
    if nombre in ("cem_video", "cem_promesa"):
        import decor_t7
        return decor_t7.cementerio_final(t, nombre[4:])
    return None


def _pintar_susto(nombre, t):
    if nombre == "hakkar":
        import decor_zg
        return decor_zg.susto(t)
    if nombre == "torre":
        import decor_t6
        return decor_t6.susto2(t)
    import decor_t7
    return decor_t7.susto3(t) if nombre == "fila" else decor_t7.susto4(t)


def _golpes(t):
    """Sacudida de la estampa en los golpes fuertes (el susto y los sobresaltos)."""
    g = 0.0
    for t0, f in ((A.T_SUSTO, 1.0), (A.m_salio - 0.05, 0.25), (A.c_instante, 0.18), (A.h_huir, 0.2), (A.z_sangre, 0.2),
                  (A.T_SUSTO2, 1.0), (A.T_SUSTO3, 1.0), (A.T_SUSTO4, 1.0), (A.d_quema, 0.15), (A.r_mordia, 0.2),
                  (A.n_guardias, 0.15), (A.e_mataron, 0.3)):
        if t0 <= t < t0 + 0.5:
            g = max(g, f * (1 - (t - t0) / 0.5) ** 2)
    return g


def _flash(nombre, t):
    if nombre == "torre":
        import decor_t6
        return decor_t6.flash_portal(t)
    if nombre in ("alba", "cem_promesa", "seleccion"):
        import decor_t7
        return decor_t7.flash(nombre, t)
    return 0.0


def cuadro(t):
    nombre = decorado(t)
    if nombre == "tinta" or t >= TL["total"]:
        return np.zeros((H, W, 3), np.float32) + np.float32(TINTA)
    sus = SUSTOS.get(nombre)
    if sus and t >= sus[1]:                                # EL SUSTO: golpe de un cuadro en negativo y la tinta lo traga
        ap, ts, tf, cx, cy = sus
        g = _pintar_susto(nombre, t)
        u = t - ts
        img = acabado(g, golpe=_golpes(t), negativo=1.0 if u < 1.5 / 30 else 0.0, vineta=1.3)
        img = C.mancha(img, smooth(pr(t, ts + 0.32, tf - 0.2)), 960, 540, 9)
        return img
    g = pintar(nombre, t)
    oscuro = 0.0
    if sus:
        oscuro = 0.55 * smooth(pr(t, sus[0], sus[0] + 0.5))
    img = acabado(g, golpe=_golpes(t), oscuro=oscuro, vineta=1.15, flash=_flash(nombre, t))
    if t < 1.2:                                            # el video se abre desde la tinta
        img = C.mancha(img, 1 - smooth(pr(t, 0.05, 1.2)), 960, 600, 0)
    for tc, dur, cx, cy, sem in CAMBIOS:
        if tc - dur / 2 <= t < tc:
            img = C.mancha(img, smooth(pr(t, tc - dur / 2, tc)), cx, cy, sem)
        elif tc <= t < tc + dur / 2:
            img = C.mancha(img, 1 - smooth(pr(t, tc, tc + dur / 2)), cx, cy, sem + 20)
    if sus and t >= sus[0]:                                # silencio previo al susto: todo se hunde en negro
        img = C.mancha(img, 0.85 * smooth(pr(t, sus[0], sus[1] - 0.05)), sus[3], sus[4], 8)
    if nombre == "cierre":                                 # el final: la tinta se lo traga todo
        img = C.mancha(img, smooth(pr(t, A.T_NEGRO - 1.3, A.T_NEGRO)), 960, 540, 30)
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
