# -*- coding: utf-8 -*-
"""Sonic.exe: el CD maldito que nunca existió — estilo «terror CRT» con MONITOR de PC (kit pix.py + terror.py + terror_pc.py).
Todas las escenas usan `Mundo`, que dibuja el cuadro completo en función del tiempo global (plano secuencia): cuarto de 2011 a oscuras ->
el CD viaja al lector -> la cámara entra en el monitor -> la corrupción se sale al cuarto -> la verdad (wiki, captura, .exe) -> el legado ->
algo entra al cuarto. Los SFX NO pasan por `ev`: los ancla `fx_audio.py` a las mismas palabras (anclas.py) y los deja en audio/fx.wav."""
import math

import numpy as np

import anclas as A
import terror_crt as T
import terror_pc as X
from escena_base import TL, Escena
from terror_pix import TOTAL, P, acabado, clamp, e_out, golpe, lerp, mix, pop, pr, rnd, smooth
from terror_crt import FRIO, HUESO, SANGRE, SC, SH, SW

CLIPS = ("fuego", "demonio", "tails", "knuckles", "eggman", "hola")

# tiempos propios de la pantalla (derivados de las anclas)
T_NIV = {"fuego": A.a_cac - 0.5, "demonio": A.a_ojos - 0.3, "tails": A.a_tails - 0.3, "knuckles": A.a_knuc - 0.3,
         "eggman": A.a_vill - 0.3, "hola": A.a_queda - 0.6}
T_APAGA = A.a_apaga - 0.1
T_REENC = A.a_ocurrio - 0.3
T_WIKI = A.a_fic - 0.4
T_ERR = A.a_nohab - 0.4
T_CAPT = A.a_capt - 0.3
T_EXE = A.a_truco - 0.3
T_DOC = A.a_amat - 0.3
T_REAL = A.a_func - 0.3
T_GJ = A.a_grande - 0.4
T_VID = A.a_meses - 0.3
T_DESC = A.a_nunca - 0.3
T_ELIM = A.a_2014 - 0.3
T_BLOG = A.a_blog - 0.3
T_BROMA = A.a_broma - 0.3
T_CIERRE = A.a_ano - 0.3
SC_ = (SC[0], SC[1])

# ------------------------------------------------------------------ cámara
KF = [(0.0, 1.00, 960, 540), (A.T_ON + 0.8, 1.02, 1000, 545), (A.a_car - 0.4, 1.10, 780, 520), (A.a_nota + 0.5, 1.12, 740, 500),
      (A.T_DISCO0 - 0.1, 1.12, 740, 500), (A.T_DISCO1 - 0.5, 1.55, 1560, 600), (A.a_comp + 0.6, 1.55, 1500, 590),
      (A.T_TIT + 0.1, 2.60, SC_[0], SC_[1]), (A.a_nivel, 2.60, SC_[0], SC_[1]), (A.a_queda + 0.3, 1.45, 1260, 540),
      (A.a_apaga + 0.3, 1.45, 1260, 540), (A.a_vuelta - 0.2, 1.15, 760, 600), (A.a_cama + 0.2, 1.25, 400, 620),
      (A.a_ocurrio - 0.5, 1.25, 400, 620), (A.a_ocurrio + 1.5, 1.0, 960, 540), (A.a_fic - 0.9, 1.0, 960, 540),
      (A.a_fic - 0.1, 2.55, SC_[0], SC_[1]), (A.a_nohab, 2.45, SC_[0], SC_[1]), (A.a_capt, 2.60, SC_[0], SC_[1]),
      (A.a_truco, 2.50, SC_[0], SC_[1]), (A.a_amat, 2.65, SC_[0], SC_[1]), (A.a_grande, 2.50, SC_[0], SC_[1]),
      (A.a_meses, 2.62, SC_[0], SC_[1]), (A.a_2014, 2.50, SC_[0], SC_[1]), (A.a_blog, 2.65, SC_[0], SC_[1]),
      (A.a_broma - 0.5, 2.55, SC_[0], SC_[1]), (A.a_ano + 1.5, 1.0, 960, 540), (A.a_duda, 1.04, 900, 540),
      (A.a_capt2 + 0.2, 1.40, 1180, 520), (A.a_unas + 0.5, 1.45, 1230, 520), (A.a_gente + 0.6, 1.0, 960, 540),
      (A.a_espe + 0.4, 1.0, 960, 540), (A.a_cambiara + 0.8, 1.22, 1220, 540), (A.a_disc2 + 0.6, 1.30, 1250, 570),
      (A.a_start2 - 0.3, 1.14, 880, 565), (A.T_FIN, 1.14, 880, 565), (TOTAL, 1.14, 880, 565)]


def camara(t):
    for (t0, z0, x0, y0), (t1, z1, x1, y1) in zip(KF, KF[1:]):
        if t < t1:
            u = smooth(pr(t, t0, t1))
            return lerp(z0, z1, u), lerp(x0, x1, u), lerp(y0, y1, u)
    return KF[-1][1:]


def temblor(t, z):
    a = 1.0 if z < 1.5 else 0.45
    return a * (5 * math.sin(t * 0.83) + 3 * math.sin(t * 2.3)), a * (4 * math.sin(t * 0.67 + 1) + 2 * math.sin(t * 1.9))


# ------------------------------------------------------------------ pantalla del monitor
def _niv(nombre, t, ini=0.0, brillo=1.0):
    return X.pant_clip43(nombre, t - T_NIV[nombre] + ini, 0.0, 8.0, brillo)


def pantalla(t):
    """Devuelve (búfer con efecto CRT, glitch global 0..1, flash 0..1)."""
    gl, flash, tono, ruido = 0.0, 0.0, (1.0, 1.0, 1.0), 0.045
    if t < A.T_ON:
        return T.crt(np.zeros((SH, SW, 3), np.float32) + 0.010, t, 0.0, ruido=0.02), 0.0, 0.0
    if T_APAGA + 0.9 < t < T_REENC:
        return np.zeros((SH, SW, 3), np.float32) + 0.005, 0.0, 0.0
    if t >= A.T_FIN:
        return np.zeros((SH, SW, 3), np.float32), 0.0, 0.0

    # ----------------------------------------------------------- cd: escritorio de 2011
    if t < A.T_TIT - 0.3:
        q = X.pant_escritorio(t, pr(t, A.a_comp, A.a_comp + 0.5), pr(t, A.a_comp + 1.0, A.a_comp + 1.6))
        img = q.im
        if t < A.T_ON + 0.7:
            img = X.encendido(img, (t - A.T_ON) / 0.7)
        gl = 0.10 + 0.5 * golpe(t, A.a_comp + 1.7, 0.4)
        if A.T_DISCO1 < t < A.T_DISCO1 + 0.8:                                   # el lector lee: la pantalla parpadea
            gl += 0.25
    # ----------------------------------------------------------- titulo: la pantalla real se corrompe
    elif t < T_NIV["fuego"]:
        seg = t - A.T_TIT
        q = X.pant_titulo(t, seg, pr(t, A.a_cielo, A.a_cielo + 1.4), pr(t, A.a_oxid, A.a_oxid + 1.4), pr(t, A.a_666 - 0.05, A.a_666 + 0.2),
                          pr(t, A.a_roja - 0.2, A.a_roja + 1.2), 1.0, pr(t, A.a_apag, A.a_apag + 0.4) * (t < A.a_start + 0.3))
        img = q.im
        tono = (1.0, 1.0 - 0.1 * pr(t, A.a_roja, A.a_start), 1.0 - 0.12 * pr(t, A.a_roja, A.a_start))
        gl = 0.05 + 0.9 * golpe(t, A.T_TIT, 0.35) + 0.5 * golpe(t, A.a_cielo, 0.4) + 0.6 * golpe(t, A.a_oxid, 0.4) \
            + 0.9 * golpe(t, A.a_666, 0.45) + 0.7 * golpe(t, A.a_roja, 0.5) + 0.9 * golpe(t, A.a_start, 0.4)
        flash = 0.12 * golpe(t, A.a_666, 0.18)
        if t > A.a_start + 0.45:                                                  # «start»: el monitor cae a ruido y espera la cacería
            n = T.ruido_tv(SW, SH, t, 0.9) * np.float32((0.9, 1.0, 1.0))
            u_ap = pr(t, A.a_start + 1.4, A.a_start + 2.2)
            img = n * (0.6 - 0.12 * u_ap) * np.float32((1.0, 1.0 - 0.25 * u_ap, 1.0 - 0.30 * u_ap))   # el ruido se enrojece
            yb = int(SH * (1.0 - (t * 0.55) % 1.0))                               # banda de tracking que sube
            img[max(0, yb - 40):yb + 40] *= 2.6
            f_ = T_NIV["fuego"]
            if f_ - 0.95 < t < f_ - 0.77 or f_ - 0.40 < t < f_ - 0.28:            # dos cuadros del demonio entre el ruido
                img = X.pant_clip43("demonio", 3.2, 0.0, 8.0, 0.9).im
            gl = 0.7
    # ----------------------------------------------------------- niveles: la cacería, todo dentro del monitor
    elif t < T_APAGA:
        if t < T_NIV["demonio"]:
            q, c = _niv("fuego", t), "fuego"
        elif t < T_NIV["tails"]:
            q, c = _niv("demonio", t), "demonio"
        elif t < T_NIV["knuckles"]:
            q, c = _niv("tails", t, 0.5), "tails"
        elif t < T_NIV["eggman"]:
            q, c = _niv("knuckles", t), "knuckles"
        elif t < T_NIV["hola"]:
            q, c = _niv("eggman", t), "eggman"
        else:
            q, c = _niv("hola", t), "hola"
        img = q.im
        for nom in CLIPS:
            gl = max(gl, 0.9 * golpe(t, T_NIV[nom], 0.35))
        gl += 0.08 + 0.4 * pr(t, A.a_nivel, A.a_tom2) + (0.5 * golpe(t, A.a_pup, 0.5))
        pulso = 0.5 + 0.5 * math.sin(t * 15)
        k_r = pr(t, A.a_pup, A.a_tom2)
        tono = (1.0, 1.0 - 0.18 * k_r * pulso, 1.0 - 0.25 * k_r * pulso)
        flash = 0.07 * k_r * (math.sin(t * 15) > 0.85)
    # ----------------------------------------------------------- final: se apaga; luego el escritorio vuelve «normal»
    elif t < T_APAGA + 0.9:
        q = X.pant_clip43("hola", 4.2, 0.0, 8.0, 1.0)
        img = X.apagado(q.im, (t - T_APAGA) / 0.8)
        gl = 0.3
    elif t < T_WIKI:
        q = X.pant_escritorio(t)
        img = q.im
        if t < T_REENC + 0.7:
            img = X.encendido(img, (t - T_REENC) / 0.7)
        gl = 0.08 + 0.5 * golpe(t, A.a_ocurrio + 0.2, 0.3)
    # ----------------------------------------------------------- autor: la verdad (pantallas dibujadas)
    elif t < T_ERR:
        q = X.pant_wiki(t, T_WIKI)
        k = pop(t, A.a_fic, 0.4)
        q.texto("FICCIÓN", SW / 2, 800, 120, HUESO, "serif", clamp(pr(t, A.a_fic, A.a_fic + 0.15)) * (1 - pr(t, A.a_jc - 0.1, A.a_jc + 0.2)),
                "mm", 0.03, 0.9)
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_WIKI, 0.35)
    elif t < T_CAPT:
        q = X.pant_escritorio(t, 0, 0, pr(t, A.a_nohab, A.a_nohab + 0.3))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_ERR, 0.4) + 0.4 * golpe(t, A.a_kyle2, 0.3)
    elif t < T_EXE:
        q = X.pant_captura(t, pr(t, A.a_capt, A.a_capt + 1.2))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_CAPT, 0.4) + 0.5 * golpe(t, A.a_idea, 0.4)
    elif t < T_DOC:
        q = X.pant_exe(t, pr(t, T_EXE, T_EXE + 0.5), pr(t, A.a_corres - 0.2, A.a_corres + 0.6), T_EXE)
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_EXE, 0.4) + 0.8 * golpe(t, A.a_corres, 0.5) + 0.4 * golpe(t, A.a_prog, 0.4)
    elif t < T_REAL:
        q = X.pant_doc(t, T_DOC, pr(t, A.a_amat + 0.5, A.a_func))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_DOC, 0.4)
    elif t < T_GJ:
        q = X.pant_titulo(t, t - T_REAL, 0.85 * pr(t, A.a_inq - 0.2, A.a_inq + 0.9), 0.0, 0.0, 0.0, 1.0, 0.0)
        img = q.im
        gl = 0.05 + 0.6 * golpe(t, T_REAL, 0.35) + 0.6 * golpe(t, A.a_inq, 0.5)
    # ----------------------------------------------------------- legado: cada hecho una página con su fecha
    elif t < T_VID:
        q = X.pant_web(t, "gj", T_GJ, pr(t, A.a_2012, A.a_2012 + 0.4), pr(t, A.a_my5t, A.a_my5t + 0.4))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_GJ, 0.35) + 0.3 * golpe(t, A.a_2012, 0.3)
    elif t < T_DESC:
        q = X.pant_web(t, "video", T_VID, pr(t, A.a_pew, A.a_pew + 0.4), pr(t, T_VID + 0.4, T_VID + 0.8))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_VID, 0.35) + 0.3 * golpe(t, A.a_pew, 0.3)
    elif t < T_ELIM:
        q = X.pant_web(t, "gj", T_DESC - 6.0, 1.0, 1.0, pr(t, A.a_desc - 0.3, A.a_desc + 0.3))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_DESC, 0.35) + 0.5 * golpe(t, A.a_desc, 0.35)
    elif t < T_BLOG:
        q = X.pant_wiki(t, -10.0, pr(t, A.a_borro - 0.1, A.a_borro + 1.4), pr(t, A.a_mal, A.a_mal + 0.35), pr(t, A.a_clich, A.a_clich + 0.35))
        img = q.im
        gl = 0.06 + 0.7 * golpe(t, T_ELIM, 0.35) + 0.9 * golpe(t, A.a_borro, 0.45) + 0.6 * golpe(t, A.a_mal, 0.3) \
            + 0.6 * golpe(t, A.a_clich, 0.3)
    elif t < T_BROMA:
        q = X.pant_web(t, "blog", T_BLOG, pr(t, A.a_rebel - 0.5, A.a_rebel + 0.4))
        img = q.im
        gl = 0.10 + 0.7 * golpe(t, T_BLOG, 0.35) + 0.8 * golpe(t, A.a_rebel, 0.5)
    elif t < T_CIERRE:
        q = X.pant_web(t, "broma", T_BROMA)
        img = q.im
        gl = 0.05 + 0.6 * golpe(t, T_BROMA, 0.35)
    # ----------------------------------------------------------- cierre: «una captura retocada», «unas cuantas palabras»
    elif A.a_capt2 - 0.15 <= t < A.a_unas - 0.1:
        q = X.pant_captura(t, pr(t, A.a_capt2, A.a_capt2 + 1.1))
        img = q.im
        gl = 0.06 + 0.8 * golpe(t, A.a_capt2 - 0.15, 0.4)
    elif A.a_unas - 0.1 <= t < A.a_espe - 0.2:
        q = X.pant_wiki(t, A.a_unas - 0.1)
        img = q.im
        gl = 0.06 + 0.8 * golpe(t, A.a_unas - 0.1, 0.4)
    # ----------------------------------------------------------- cierre: la pantalla de título esperando
    else:
        u_o = pr(t, A.a_cambiara, A.a_start2)
        q = X.pant_titulo(t, t - T_CIERRE, 0.85 * u_o, 0.5 * u_o, 0.0, 0.5 * pr(t, A.a_start2 - 1.0, A.a_start2), 1.0,
                          pr(t, A.a_espe, A.a_espe + 0.5))
        img = q.im
        gl = 0.05 + 0.6 * golpe(t, T_CIERRE, 0.35) + 0.7 * golpe(t, A.a_espe - 0.2, 0.35) + 0.15 * u_o + 0.9 * golpe(t, A.a_start2, 0.5)
        flash = 0.10 * golpe(t, A.a_start2, 0.15)

    return T.crt(img, t, gl, tono, ruido), gl, flash


# ------------------------------------------------------------------ cuadro completo
def _slam(p, txt, x, y, px, color, t, t0, sale, fnt="serif", anchor="mm"):
    if t < t0 or t > sale + 0.3:
        return
    k = pop(t, t0, 0.32)
    s = lerp(1.7, 1.0, min(1.0, k)) if k < 1 else k
    op = pr(t, t0, t0 + 0.1) * (1 - pr(t, sale, sale + 0.3))
    with p.pivote(x, y, s):
        p.texto(txt, x, y, px, color, fnt, op, anchor, 0.03, 0.9)


def _cd_pos(t):
    """Posición, escala y perspectiva del CD: reposa en el foco y, tras «¿qué podía salir mal?», viaja a la bandeja del lector."""
    u = smooth(pr(t, A.T_DISCO0, A.T_DISCO1 - 0.3))
    x = lerp(560, 1776, u)
    y = lerp(500 + 8 * math.sin(t * 1.3), 596, u) - 260 * math.sin(math.pi * u) ** 1.2
    return x, y, lerp(1.7, 0.66, u), lerp(0.62, 0.35, u)


def cuadro(t):
    scr, gl, flash = pantalla(t)
    z, cx, cy = camara(t)
    dx, dy = temblor(t, z)
    cm = T.color_medio(scr)
    brillo = float(clamp(cm.mean() * 1.6, 0, 1.2))
    apagado = (T_APAGA + 0.6 <= t < T_REENC) or t < A.T_ON or t >= A.T_FIN
    col_n = cm / max(cm.max(), 1e-3)
    luz_col = tuple(0.45 * np.array(T.FRIO) + 0.55 * col_n)
    k_luz = (0.25 + 2.4 * brillo) * (0.0 if apagado else 1.0)
    u_oscuro = pr(t, A.a_cac, A.a_ojos)                                         # la cacería enrojece el cuarto

    p = P()
    with p.cam(z, cx, cy, dx=dx, dy=dy):
        X.cuarto_pc(p, t)
        c_tv = p._t([SC])[0]
        T.iluminar(p, c_tv, 1500 * p.s, luz_col, k_luz, amb=(0.072, 0.086, 0.118) if not apagado else (0.030, 0.036, 0.052))
        T.ventana(p, t)
        u_gente = pr(t, A.a_gente - 0.3, A.a_gente + 0.8) * (1 - pr(t, A.a_amigo - 0.4, A.a_amigo + 0.4))
        if u_gente > 0.01:                                                       # «mucha gente mirando»: las pantallas de los lectores
            p.im *= 1 - 0.40 * u_gente
            T.pared_pantallas(p, t, A.a_gente - 0.3, u_gente)
        if apagado:                                                              # luna sobre la cama
            p.glow(250, 690, 560, X.MOON, 0.16, 1.6)
            X.cama_luna(p, 1.0 - pr(t, A.T_REENC if hasattr(A, 'T_REENC') else T_REENC, T_REENC + 0.1))
        p.poly([(1060, 806), (1560, 806), (1900, 880), (760, 880)], luz_col, 0.07 * k_luz, aditivo=True)   # luz sobre el escritorio
        p.glow(SC[0], SC[1], 900, luz_col, 0.20 * k_luz, 1.8)
        # la corrupción se sale del monitor (niveles)
        u_der = pr(t, A.a_nivel, A.a_queda + 0.5) * (t < T_APAGA + 0.3)
        if u_der > 0.01:
            for i in range(16):
                fase = int(t * 14) + i * 3
                y = 120 + 820 * rnd(i, 5) + 24 * math.sin(t * 3 + i)
                ancho = (500 + 1300 * rnd(fase, 6)) * u_der
                xx = SC[0] + (rnd(fase, 7) - 0.5) * 900
                alto = 5 + 38 * rnd(i, 8) ** 2
                c = mix((0.75, 0.10, 0.08), (1.0, 0.55, 0.5), 0.3 * rnd(fase, 9))
                p.rect(xx - ancho / 2, y, xx + ancho / 2, y + alto, c, 0.10 * u_der * (0.4 + rnd(fase, 10)), aditivo=True)
            p.glow(SC[0], SC[1], 1500, (0.55, 0.05, 0.05), 0.22 * u_der, 1.4)
        # Sonic de pie: algo entra al cuarto (cierre)
        k_son = pr(t, A.a_start2 - 0.7, A.a_start2 + 0.2) * (t < A.T_FIN)
        X.sonic_sil(p, 330 + 22 * (1 - k_son), 806, 1.9, mix(luz_col, X.MOON, 0.4), t, ojos=pr(t, A.a_start2, A.a_start2 + 0.4), k=k_son)
        # peluche sobre la cama (final)
        k_pel = pr(t, A.a_pel - 0.2, A.a_pel + 0.5) * (1 - pr(t, A.a_ocurrio + 0.2, A.a_ocurrio + 1.0))
        X.sonic_sil(p, 300, 704, 0.95, X.MOON, t, ojos=pr(t, A.a_pel + 0.3, A.a_pel + 1.0) * k_pel, sangre=pr(t, A.a_sang, A.a_sang + 2.5),
                    peluche=True, k=k_pel)
        # monitor, torre, jugador
        k_lee = pr(t, A.T_DISCO1 + 0.3, A.T_DISCO1 + 2.0) * (t < A.T_TIT + 3)
        bandeja = pr(t, A.T_DISCO1 - 1.0, A.T_DISCO1 - 0.4) * (1 - pr(t, A.T_DISCO1, A.T_DISCO1 + 0.7))
        X.torre_luces(p, t, bandeja, k_lee)
        X.monitor_pc(p, scr, t, luz_col, apagado)
        X.jugador_pc(p, t, luz_col, giro=smooth(pr(t, A.a_vuelta - 0.2, A.a_vuelta + 0.9)) * (t < T_REENC) + 0.0, k=1.0)
        # --- recuerdo del CD: foco de luz, CD sin carátula y la nota de Kyle; luego el CD viaja al lector
        u_foco = pr(t, A.a_cd - 0.4, A.a_car + 0.3) * (1 - pr(t, A.T_DISCO0, A.T_DISCO0 + 0.6))
        u_foco2 = pr(t, A.a_ben - 0.2, A.a_ben + 0.5) * (1 - pr(t, A.a_duda, A.a_duda + 0.7))     # cierre: el cartucho de Ben
        u_foco3 = pr(t, A.a_nunca2 - 0.2, A.a_nunca2 + 0.4) * (1 - pr(t, A.a_real + 0.3, A.a_real + 0.9))   # «un disco real»
        for u_f in (u_foco, u_foco2, u_foco3):
            if u_f > 0.01:
                p.im *= 1 - 0.55 * u_f
                p.poly([(480, -30), (800, -30), (1030, 790), (260, 790)], (0.85, 0.92, 1.0), 0.13 * u_f, aditivo=True)
                p.elip(650, 800, 360, 40, (0.85, 0.92, 1.0), 0.10 * u_f, aditivo=True)
        if A.a_cd - 0.4 < t < A.T_DISCO1:
            kc = pop(t, A.a_cd, 0.4)
            x, y, s, tl = _cd_pos(t)
            X.cd_disco(p, x, y, s * min(kc, 1.2) if t < A.T_DISCO0 else s, tl, pr(t, A.a_sonic, A.a_exe + 0.6))
        if A.a_kyle - 0.2 < t < A.T_DISCO0 + 0.6:
            k = e_out(pr(t, A.a_kyle, A.a_kyle + 0.5))
            sal = pr(t, A.T_DISCO0, A.T_DISCO0 + 0.5)
            X.nota_arrugada(p, 880, lerp(-100, 500, k) + 220 * sal, 1.55, t, pr(t, A.a_no, A.a_no + 0.9), pr(t, A.a_dest, A.a_dest + 0.9))
        if A.T_DISCO1 - 0.35 < t < A.T_DISCO1 + 0.75 and bandeja > 0.15:
            h = 62 * smooth(bandeja)
            X.cd_disco(p, 1776, 528 + h * 0.55, 0.66, 0.35, 1.0)
        if A.a_ben - 0.2 < t < A.a_duda + 0.4:                                   # cartucho de Ben Drowned (otro objeto «embrujado»)
            k = pop(t, A.a_ben, 0.4)
            T.cartucho(p, 650, 470 + 10 * math.sin(t * 1.4), 1.55 * k * (1 - pr(t, A.a_duda, A.a_duda + 0.5)))
        if A.a_disco_r - 0.2 < t < A.a_real + 1.0:                               # «un disco real»: aparece y se deshace en polvo
            u_d = pr(t, A.a_real, A.a_real + 0.8)
            kd = pop(t, A.a_disco_r, 0.35) * (1 - e_out(u_d))
            if kd > 0.03:
                X.cd_disco(p, 650 + 5 * math.sin(t * 40) * u_d, 470 + 8 * math.sin(t * 1.3), 1.5 * kd, 0.62, 1.0, 1.0 - 0.5 * u_d)
            for i in range(16):
                a_ = 6.28 * rnd(i, 21)
                r_ = 40 + 210 * u_d * (0.4 + rnd(i, 22))
                p.circ(650 + r_ * math.cos(a_), 470 + r_ * math.sin(a_) * 0.6 - 40 * u_d, 2 + 3 * rnd(i, 23), (0.85, 0.9, 1.0),
                       0.8 * (1 - u_d) * (u_d > 0.01))
        if A.a_disc2 - 0.1 < t < A.T_FIN:                                        # «un disco sin carátula»: otro CD sobre el escritorio
            kd2 = pop(t, A.a_disc2, 0.4)
            p.glow(1590, 822, 130, mix(luz_col, (0.85, 0.92, 1.0), 0.5), 0.30 * min(kd2, 1.0), 1.6)
            X.cd_disco(p, 1590, 826, 0.62 * kd2, 0.30, 0.0, 1.0)
        T.polvo(p, t, SC, 1.0 if not apagado else 0.2)
    # ------------------------------------------------------------ rótulos de énfasis (fuera de cámara)
    _slam(p, "AGOSTO", 1130, 90, 80, HUESO, t, A.a_ago, A.a_tom - 0.3, "serif", "lm")
    _slam(p, "2011", 1130, 172, 104, HUESO, t, A.a_2011, A.a_tom - 0.3, "serif", "lm")

    fx = golpe(t, A.a_666, 0.35) * 0.4 + golpe(t, A.a_pup, 0.4) * 0.3 + golpe(t, A.a_corres, 0.5) * 0.4 + golpe(t, A.a_start2, 0.4) * 0.5
    img = acabado(p.im, t, fx, gl * 0.18, flash, bloom=0.85)
    img *= smooth(pr(t, 0.0, 0.7))
    if t >= A.T_FIN:                                                             # corte seco a negro
        img *= 0.0
    return img


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
