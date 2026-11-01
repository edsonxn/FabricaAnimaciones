# -*- coding: utf-8 -*-
"""BEN Drowned — estilo «terror CRT» (kit pix.py + terror.py). Todas las escenas usan `Mundo`, que dibuja el cuadro completo en
función del tiempo global (plano secuencia): cuarto a oscuras -> la cámara entra en la tele -> el juego se corrompe -> sale al cuarto.
Los SFX de ElevenLabs NO pasan por `ev`: los ancla `fx_audio.py` a las mismas palabras (anclas.py) y los deja en audio/fx.wav."""
import math

import cv2
import numpy as np

import anclas as A
import terror as T
from escena_base import TL, Escena
from pix import TOTAL, P, acabado, clamp, e_out, golpe, lerp, mix, pop, pr, rnd, smooth
from terror import HUESO, SANGRE, FRIO, SW, SH, SC

# ------------------------------------------------------------------ cámara
KF = [(0.0, 1.00, 960, 540), (A.T_ON + 0.8, 1.00, 990, 545), (A.a_car - 0.3, 1.06, 900, 540), (A.T_INS1, 1.10, 1000, 550),
      (A.a_noc, 1.12, 1060, 540), (19.9, 2.75, SC[0], SC[1]), (A.a_rel + 8.7, 2.85, SC[0], SC[1]),
      (43.6, 1.00, 960, 540), (A.a_vid - 0.3, 1.00, 960, 540), (A.a_term + 0.6, 1.45, 1300, 520),
      (A.T_NEGRO, 1.45, 1300, 520), (A.T_REG, 1.05, 900, 545), (A.a_alguien, 1.05, 900, 545), (A.T_OFF, 1.16, 760, 560),
      (TOTAL, 1.16, 760, 560)]


def camara(t):
    for (t0, z0, x0, y0), (t1, z1, x1, y1) in zip(KF, KF[1:]):
        if t < t1:
            u = smooth(pr(t, t0, t1))
            if t1 - t0 < 0.05:
                u = 1.0
            return lerp(z0, z1, u), lerp(x0, x1, u), lerp(y0, y1, u)
    return KF[-1][1:]


def temblor(t, z):
    """Cámara en mano muy leve; mucho más sutil cuando estamos dentro de la tele."""
    a = 1.0 if z < 1.5 else 0.45
    return a * (5 * math.sin(t * 0.83) + 3 * math.sin(t * 2.3)), a * (4 * math.sin(t * 0.67 + 1) + 2 * math.sin(t * 1.9))


# ------------------------------------------------------------------ pantalla de la tele
def _encendido(img, u):
    """La tele se enciende: una línea blanca que se abre en el centro hasta llenar el tubo."""
    h, w = img.shape[:2]
    ancho = smooth(pr(u, 0.0, 0.3))
    alto = smooth(pr(u, 0.28, 1.0))
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    m = ((np.abs(y - h / 2) < 3 + alto * h / 2) & (np.abs(x - w / 2) < ancho * w / 2)).astype(np.float32)[..., None]
    lin = np.exp(-((np.abs(y - h / 2) / (5 + 40 * alto)) ** 2)) * (ancho > 0) * (1 - alto)
    return img * m + (m * lin[..., None] * 1.6)


def _apagado(img, u):
    """La tele se apaga: se aplasta a una línea y queda un punto."""
    h, w = img.shape[:2]
    alto = 1 - smooth(pr(u, 0.0, 0.45))
    ancho = 1 - smooth(pr(u, 0.4, 0.8))
    y = np.arange(h, dtype=np.float32)[:, None]
    x = np.arange(w, dtype=np.float32)[None, :]
    m = ((np.abs(y - h / 2) < 3 + alto * h / 2) & (np.abs(x - w / 2) < 6 + ancho * w / 2)).astype(np.float32)[..., None]
    pt = np.exp(-(((x - w / 2) ** 2 + (y - h / 2) ** 2) / (2 * 22 ** 2)))[..., None] * (1 - smooth(pr(u, 0.75, 1.0))) * 1.2
    return img * m * (1.0 + 1.5 * (1 - alto)) + pt


def pantalla(t):
    """Devuelve (búfer de pantalla con efecto CRT, glitch global 0..1, flash 0..1)."""
    q = None
    dlg = None
    gl = 0.0
    flash = 0.0
    tono = (1.0, 1.0, 1.0)
    ruido = 0.045
    on = A.T_ON
    final_off = t >= A.T_OFF

    if t < on:
        img = np.zeros((SH, SW, 3), np.float32) + 0.012
        return T.crt(img, t, 0.0, ruido=0.02), 0.0, 0.0
    if final_off and t > A.T_OFF + 0.6:
        return np.zeros((SH, SW, 3), np.float32) + 0.006, 0.0, 0.0

    # ----------------------------------------------------------- cartucho: estática -> archivo
    if t < A.a_par:
        img = T.ruido_tv(SW, SH, t, 0.75) * np.float32((0.85, 0.95, 1.0))
        img = img * (0.55 + 0.1 * math.sin(t * 7))
        if t < on + 0.7:
            img = _encendido(img, (t - on) / 0.7)
        gl = 0.15 + 0.5 * golpe(t, A.T_INS1 - 0.2, 0.3)
    elif t < A.T_JUEGO:
        k_ben = pr(t, A.a_due, A.a_due + 0.5)
        rojo = pr(t, A.a_sell, A.a_ben1 + 0.25)
        q = T.pant_archivo(t, k_ben, rojo)
        img = q.im
        gl = 0.9 * golpe(t, A.a_par, 0.35) + 0.8 * golpe(t, A.a_ben1, 0.45) + 0.12 * rojo
        flash = 0.12 * golpe(t, A.a_ben1, 0.2)
        if t < A.a_par + 0.18:
            img = img * 0.2
    # ----------------------------------------------------------- falla: el juego
    elif t < A.a_pue + 0.0:
        seg = t - A.T_JUEGO
        if A.a_fal < t < A.a_fal + 0.7:                         # el video se traba (cuadros repetidos)
            seg = A.a_fal - A.T_JUEGO + int((t - A.a_fal) * 6) / 6.0 * 0.2
        q = T.pant_clip("pueblo", seg, 38.0, 58.0, 1.05)
        img = q.im
        gl = 0.05 + 1.0 * golpe(t, A.T_JUEGO, 0.3) + 1.0 * golpe(t, A.a_fal, 0.7) + 0.9 * golpe(t, A.T_SALTO, 0.5)
        flash = 0.15 * golpe(t, A.T_SALTO, 0.15)
        if A.a_ter - 0.2 < t:
            u = pr(t, A.a_ter, A.a_fin + 0.25)
            rojo = 1.0 if t >= A.T_SALTO else 0.0
            T.pant_hud_dia(q, t, u, rojo)
            img = q.im
            if rojo:
                tono = (1.0, 0.75, 0.75)
    elif t < A.a_vend:
        q = T.pant_clip("pueblo", t - A.a_pue + 6, 82.0, 98.0, 0.8)
        img = q.im * np.float32((0.8, 0.9, 1.0))
        k = pop(t, A.a_vac, 0.35)
        if t > A.a_vac:
            q2 = P(SW, SH)
            q2.texto("VACÍO", SW / 2, SH * 0.5, 120, SANGRE, "pixel", clamp(k))
            img = img * (1 - 0.35 * clamp(k)) + q2.im
        gl = 0.1 + 0.5 * golpe(t, A.a_pue, 0.3) + 0.7 * golpe(t, A.a_vac, 0.4)
    elif t < A.a_est2:
        q = T.pant_clip("mascara", t - A.a_vend, 4.4, 10.2, 1.0)
        img = q.im
        ri = 1 if t > A.a_rei else 0
        pulso = 0.5 + 0.5 * math.sin(t * 17)
        gl = 0.12 + 0.9 * golpe(t, A.a_vend, 0.3) + ri * (0.25 + 0.3 * pulso)
        tono = (1.0, 1.0 - 0.2 * ri * pulso, 1.0 - 0.3 * ri * pulso)
        flash = 0.06 * ri * (math.sin(t * 17) > 0.8)
    elif t < A.a_rel - 0.45:
        q = T.pant_clip("estatua", t - A.a_est2, 7.8, 13.7, 1.0)
        img = q.im
        u_oj = pr(t, A.a_mir, A.a_mir + 0.5)
        if u_oj > 0:
            q2 = P(SW, SH)
            q2.im[:] = 0
            q2.rect(0, 0, SW, SH, (0, 0, 0), 0.55 * u_oj)
            mx, my = 0.6 * math.sin(t * 2.2), 0.3 * math.cos(t * 1.7)
            for sx in (-1, 1):
                x, y = SW / 2 + sx * 95, SH * 0.55
                q2.elip(x, y, 44, 25, (0.95, 0.95, 0.9), u_oj)
                q2.circ(x + mx * 18, y + my * 8, 12, (0.02, 0.02, 0.02), u_oj)
                q2.circ(x + mx * 18 + 4, y + my * 8 - 4, 3.5, (1, 1, 1), u_oj)
            img = img * (1 - 0.55 * u_oj) + q2.im * np.float32(1.0)
        gl = 0.1 + 0.6 * golpe(t, A.a_est2, 0.3) + 0.35 * pr(t, A.a_mir, A.a_rel - 0.5)
    # ----------------------------------------------------------- ben: el estanque
    elif t < A.a_fic - 0.45:
        u = pr(t, A.a_ben2, A.a_hab + 0.8)
        gl_agua = 0.5 * pr(t, A.a_desde, A.a_hab) * (1.0 if t < A.a_hab else 0.15)
        q = T.pant_agua(t, u, gl_agua)
        img = q.im
        if A.a_12 - 0.1 < t < A.a_ahog + 1.4:
            q2 = P(SW, SH)
            k = pop(t, A.a_12 - 0.05, 0.3) * (1 - pr(t, A.a_ahog + 0.9, A.a_ahog + 1.4))
            q2.texto("12 AÑOS", SW * 0.32, 330, 96, HUESO, "serif", clamp(k), "mm", 0.02, 0.9)
            img = img + q2.im * 1.0
        if t > A.a_hab:                                        # diálogo de juego: se pinta APARTE y se pega sin glitch para que se lea
            q2 = P(SW, SH)
            q2.rrect(130, 660, SW - 130, 860, 16, (0.0, 0.0, 0.0), 1.0, borde=HUESO, w=5)
            letras = "B . . . E . . . N"[:int(clamp((t - A.a_hab) * 9, 0, 17))]
            q2.texto(letras, 200, 760, 84, (1.0, 0.25, 0.25), "pixel", 1.0, "lm")
            qm = P(SW, SH)
            qm.rrect(130, 660, SW - 130, 860, 16, (1.0, 1.0, 1.0), 0.93)
            dlg = (q2.im, qm.im[..., 0])
        gl = 0.10 + 0.9 * golpe(t, A.a_rel - 0.45, 0.4) + 0.7 * gl_agua + 0.5 * golpe(t, A.a_ben2, 0.3)
        tono = (0.85, 1.0, 1.0)
    # ----------------------------------------------------------- foro: «era ficción»
    elif t < A.a_vid:
        q = T.pant_foro(t, A.a_fic)
        img = q.im
        gl = 0.8 * golpe(t, A.a_fic - 0.45, 0.4) + 0.08
        if t < A.a_fic + 0.2:
            img = img * 0.4
    # ----------------------------------------------------------- cierre: se sale de la tele
    elif t < A.T_NEGRO:
        u = pr(t, A.a_vid, A.a_jue)
        q = T.pant_foro(t, A.a_fic)
        img = q.im
        n = T.ruido_tv(SW, SH, t, 0.9) * np.float32((0.9, 1.0, 1.0))
        k = pr(t, A.a_vid, A.a_vid + 0.6) ** 1.5
        img = img * (1 - 0.8 * k) + n * (0.85 * k)
        gl = 0.25 + 0.7 * u + 0.8 * golpe(t, A.a_vid, 0.4) + 0.9 * golpe(t, A.a_mil, 0.4)
        flash = 0.30 * golpe(t, A.a_jue, 0.22)
    elif t < A.T_REG:
        img = np.zeros((SH, SW, 3), np.float32) + 0.004
    elif t < A.a_ben3 - 0.05:
        img = T.ruido_tv(SW, SH, t, 0.5) * np.float32((0.8, 0.95, 1.0))
        u = pr(t, A.T_REG, A.T_REG + 0.5)
        img = img * 0.55 * u
        gl = 0.1 + 0.9 * golpe(t, A.a_alg, 0.5) + 0.9 * golpe(t, A.a_alguien, 0.6)
        flash = 0.0
    elif t < A.T_OFF:                                         # «Ben»: el nombre del archivo
        q = P(SW, SH)
        q.fondo((0, 0, 0), (0, 0, 0))
        dx = int(8 * (1 if int(t * 22) % 2 else -1))
        q.texto("BEN", SW / 2 + dx, SH / 2, 190, SANGRE, "pixel", 0.9)
        q.texto("BEN", SW / 2, SH / 2, 190, HUESO, "pixel", 1.0)
        img = q.im
        gl = 0.55 + 0.4 * golpe(t, A.a_ben3, 0.3)
        flash = 0.10 * golpe(t, A.a_ben3, 0.18)
    else:
        img = T.ruido_tv(SW, SH, t, 0.5)
        img = _apagado(img, (t - A.T_OFF) / 0.6)
        gl = 0.0

    out = T.crt(img, t, gl, tono, ruido)
    if dlg is not None:
        out = T.crt_superpuesto(out, dlg[0], dlg[1], t)
    return out, gl, flash


# ------------------------------------------------------------------ cuadro completo
def _slam(p, txt, x, y, px, color, t, t0, sale, fnt="serif", anchor="mm"):
    """Rótulo de golpe en pantalla (fuera de la cámara): entra grande y se asienta; sale con fundido."""
    if t < t0 or t > sale + 0.3:
        return
    k = pop(t, t0, 0.32)
    s = lerp(1.7, 1.0, min(1.0, k)) if k < 1 else k
    op = pr(t, t0, t0 + 0.1) * (1 - pr(t, sale, sale + 0.3))
    with p.pivote(x, y, s):
        p.texto(txt, x, y, px, color, fnt, op, anchor, 0.03, 0.9)


def cuadro(t):
    scr, gl, flash = pantalla(t)
    z, cx, cy = camara(t)
    dx, dy = temblor(t, z)
    cm = T.color_medio(scr)
    brillo = float(clamp(cm.mean() * 1.6, 0, 1.2))
    apagado = t >= A.T_OFF + 0.6 or (A.T_NEGRO <= t < A.T_REG)
    col_n = cm / max(cm.max(), 1e-3)
    luz_col = tuple(0.45 * np.array(T.FRIO) + 0.55 * col_n)
    k_luz = (0.25 + 2.4 * brillo) * (0.0 if apagado else 1.0)

    p = P()
    with p.cam(z, cx, cy, dx=dx, dy=dy):
        T.cuarto_albedo(p, t)
        c_tv = p._t([SC])[0]
        T.iluminar(p, c_tv, 1500 * p.s, luz_col, k_luz, amb=(0.072, 0.086, 0.118) if not apagado else (0.030, 0.036, 0.052))
        T.ventana(p, t)
        # pantallitas de los lectores (cierre)
        if A.a_mil - 0.2 < t < A.T_NEGRO:
            T.pared_pantallas(p, t, A.a_mil, 1.0)
        # luz derramada de la tele sobre el cuarto
        T.luz_suelo(p, luz_col, k_luz * 0.8)
        p.glow(SC[0], SC[1], 900, luz_col, 0.20 * k_luz, 1.8)
        # el juego se sale de la tele
        u_der = pr(t, A.a_sab, A.a_jue) * (t < A.T_NEGRO)
        if u_der > 0.01:
            for i in range(16):                                    # la corrupción sale de la tele en tiras
                fase = int(t * 14) + i * 3
                y = 120 + 820 * rnd(i, 5) + 24 * math.sin(t * 3 + i)
                ancho = (500 + 1300 * rnd(fase, 6)) * u_der
                xx = SC[0] + (rnd(fase, 7) - 0.5) * 900
                alto = 5 + 38 * rnd(i, 8) ** 2
                c = mix(luz_col, (1, 1, 1), 0.25 + 0.4 * rnd(fase, 9))
                p.rect(xx - ancho / 2, y, xx + ancho / 2, y + alto, c, 0.16 * u_der * (0.4 + rnd(fase, 10)), aditivo=True)
            p.glow(SC[0], SC[1], 1500, luz_col, 0.35 * u_der, 1.4)
        # estatua (aparece al final, detrás del jugador)
        k_est = pr(t, A.a_alguien, A.a_alguien + 0.7)
        if t >= A.a_est2 - 0.01 and t < A.a_rel:           # destello en el cuarto cuando la tele nombra a la estatua: se ve de fondo
            pass
        T.estatua(p, t, luz_col, k_est, ojos=pr(t, A.a_acu - 0.2, A.a_acu + 0.4) * (1 - pr(t, TOTAL - 0.45, TOTAL - 0.05)), esc=1.0 + 0.9 * pr(t, A.T_OFF, TOTAL - 0.5))
        T.tele(p, scr, t, apagada=apagado)
        # consola + cartucho
        k_c = 1.0 if t >= A.T_INS1 else 0.0
        T.consola(p, t, k_c)
        T.jugador(p, t, luz_col, giro=smooth(pr(t, A.a_acu - 0.3, A.a_ben3 + 0.2)) * (t < A.T_OFF + 0.3), k=1.0)
        # --- recuerdo del cartucho: foco de luz, cartel de venta de garaje y el cartucho viajando a la consola
        u_foco = pr(t, A.a_car - 0.3, A.a_car + 0.3) * (1 - pr(t, A.T_INS0, A.T_INS0 + 0.5))
        if u_foco > 0.01:
            p.im *= 1 - 0.55 * u_foco
            p.poly([(570, -30), (710, -30), (930, 790), (380, 790)], (0.85, 0.92, 1.0), 0.13 * u_foco, aditivo=True)
            p.elip(655, 800, 280, 36, (0.85, 0.92, 1.0), 0.10 * u_foco, aditivo=True)
        if A.a_car - 0.3 < t < A.T_INS0:
            k = pop(t, A.a_car, 0.4)
            T.cartucho(p, 640, 430 + 10 * math.sin(t * 1.4), 1.55 * k)
        if A.a_ven - 0.2 < t < A.T_INS0 + 0.3:
            k = e_out(pr(t, A.a_ven, A.a_ven + 0.55))
            sal = pr(t, A.T_INS0, A.T_INS0 + 0.4)
            T.cartel_garaje(p, 270, lerp(-120, 250, k) - 360 * sal, t, 0.82)
        if A.T_INS0 <= t < A.T_INS1:
            u = smooth(pr(t, A.T_INS0, A.T_INS1))
            T.cartucho(p, lerp(640, 1180, u), lerp(430, 845, u) - 150 * math.sin(math.pi * u), lerp(1.55, 0.8, u))
        T.polvo(p, t, c_tv if False else SC, 1.0 if not apagado else 0.2)
        # tarjetas que se salen de la tele
        for tipo, t0, xf, yf in (("video", A.a_vid, 1760, 330), ("web", A.a_web, 860, 480), ("chat", A.a_men, 1740, 640)):
            u = e_out(pr(t, t0 - 0.1, t0 + 0.9))
            vis = u * (1 - pr(t, A.a_jue - 0.2, A.a_jue + 0.1))
            if vis > 0.01:
                x = lerp(SC[0], xf, u)
                y = lerp(SC[1], yf, u) - 60 * math.sin(math.pi * u) + 8 * math.sin(t * 1.3 + xf)
                T.tarjeta(p, tipo, x, y, lerp(0.2, 0.85, u), vis, t, luz_col)
    # ------------------------------------------------------------ rótulos de énfasis (fuera de cámara)
    _slam(p, "SEPTIEMBRE", 150, 120, 84, HUESO, t, A.a_sep, A.a_est - 0.3, "serif", "lm")
    _slam(p, "2010", 150, 205, 120, SANGRE, t, A.a_2010, A.a_est - 0.3, "serif", "lm")
    _slam(p, "ALEX D. HALL", 120, 930, 66, HUESO, t, A.a_alex, A.a_jad - 0.15, "serif", "lm")
    _slam(p, "JADUSABLE", 120, 930, 96, SANGRE, t, A.a_jad, A.a_jad + 2.4, "serif", "lm")
    _slam(p, "MILLONES", 110, 140, 120, HUESO, t, A.a_mil, A.a_sab + 0.6, "serif", "lm")

    fx = golpe(t, A.a_ben1, 0.35) * 0.4 + golpe(t, A.T_SALTO, 0.4) * 0.3 + golpe(t, A.a_jue, 0.5) * 0.7
    img = acabado(p.im, t, fx, gl * 0.18, flash, bloom=0.85)
    img *= smooth(pr(t, 0.0, 0.7))
    img *= 1.0 - smooth(pr(t, TOTAL - 0.5, TOTAL - 0.02))
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
