# -*- coding: utf-8 -*-
"""SFX SINTETIZADOS de 10,8-75 s (garganta → cierre), anclados a las mismas palabras que plano_b y plano_c.
Sonidos nuevos hechos aquí con los bloques de sfx_proc (S): rotulador, chirrido de goma, chasquidos de cachalote, sorbido,
«wah-wah», silbido de caída, chof, clic de linterna, tripas, crujido de músculo/presión, chisporroteo del ácido, ping de sonar,
impacto, tic del manómetro, alarma, siseo del tanque, acorde de veneno, «ding» de idea, arcada, clac de picos, olas, gaviota."""
import math

import numpy as np

import plano_b as B
import plano_c as C
from acuarela import pr, suave


def lista(S):
    SR = S.SR
    _t, osc, env, barrido, ruido, norm, lp, hp, bp = S._t, S.osc, S.env, S.barrido, S.ruido, S.norm, S.lp, S.hp, S.bp
    rng = S._rng

    # ------------------------------------------------------------ sonidos nuevos
    def rotulador(seed=0, dur=0.2):
        """Trazo de pincel/rotulador: ruido de banda media con raspado irregular."""
        n = bp(ruido(dur, seed), 1800, 5200) * (0.6 + 0.4 * np.abs(lp(ruido(dur, seed + 1), 40)) * 3)
        return norm(n * env(dur, 0.01, None), 0.45)

    def chirrido_goma(seed=0, dur=0.35):
        """Neopreno que roza la carne: tono que tiembla rápido (stick-slip) entre 700 y 1400 Hz."""
        r = rng(seed)
        t = _t(dur)
        f = r.uniform(700, 900) * (1 + 0.5 * t / dur) * (1 + 0.08 * np.sign(np.sin(2 * np.pi * 34 * t)))
        x = bp(osc(f, dur, "saw"), 500, 3000) * env(dur, 0.01, None)
        return norm(x, 0.45)

    def chasquidos(n=12, seed=0, ritmo=0.09):
        """Clics de ecolocalización del cachalote: tren de golpes secos con eco corto."""
        out = np.zeros(int((n * ritmo + 0.4) * SR))
        r = rng(seed)
        for k in range(n):
            d = 0.012
            c = bp(ruido(d, seed + k), 1500, 6000) * np.exp(-_t(d) / 0.002)
            i = int(k * ritmo * (1 + r.normal(0, 0.06)) * SR)
            out[i:i + len(c)] += c
            j = i + int(0.045 * SR)
            out[j:j + len(c)] += c * 0.3
        return norm(out, 0.55)

    def sorbido(seed=0, dur=1.4):
        """Aspiración gigante: ruido que baja de tono con gorgoteo."""
        t = _t(dur)
        n = ruido(dur, seed)
        out = np.zeros_like(n)
        for k in range(10):
            a, b = int(k * len(n) / 10), int((k + 1) * len(n) / 10)
            fc = 2400 * (0.15) ** (k / 9)
            out[a:b] = bp(n, fc * 0.6, fc * 1.5)[a:b]
        gorgo = 0.5 + 0.5 * np.sin(2 * np.pi * 11 * t) ** 2
        return norm(out * gorgo * np.sin(np.pi * t / dur) ** 0.8, 0.6)

    def wahwah(seed=0):
        """Trombón triste: dos notas que bajan con «wah» de filtro."""
        out = np.zeros(int(1.3 * SR))
        for k, (f, d) in enumerate(((233, 0.42), (208, 0.75))):
            t = _t(d)
            x = osc(f * (1 + 0.02 * np.sin(2 * np.pi * 6 * t)) * (1 - 0.06 * (t / d) * k), d, "saw")
            x = lp(x, 900) * env(d, 0.03, None) * (0.6 + 0.4 * np.sin(np.pi * np.clip(t / 0.25, 0, 1)))
            i = int(k * 0.45 * SR)
            out[i:i + len(x)] += x
        return norm(out, 0.5)

    def silbido_caida(dur=1.0):
        return norm(osc(barrido(1800, 380, dur), dur) * env(dur, 0.05, None), 0.35)

    def chof(seed=0, grave=1.0):
        """Golpe húmedo blando (cae sobre carne / charco)."""
        d = 0.45
        x = osc(barrido(140 / grave, 50 / grave, 0.3), 0.3) * env(0.3, 0.003, 0.08)
        n = lp(ruido(d, seed), 1400, 3) * env(d, 0.002, 0.07) * 1.6
        out = n.copy()
        out[:len(x)] += x
        for k in range(3):
            b = S.burbuja(seed + 7 + k, grave=1.6 * grave) * 0.6
            i = int((0.05 + 0.07 * k) * SR)
            out[i:i + len(b)] += b
        return norm(out, 0.85)

    def clic(seed=0):
        d = 0.05
        x = bp(ruido(d, seed), 2000, 8000) * np.exp(-_t(d) / 0.004) + osc(3200, d) * np.exp(-_t(d) / 0.006) * 0.4
        return norm(x, 0.5)

    def tripas(dur, seed=0):
        """Rugidos de estómago: tonos graves que se doblan + borboteo."""
        t = _t(dur)
        r = rng(seed)
        out = lp(ruido(dur, seed), 120, 3) * 3
        for k in range(int(dur / 1.6) + 1):
            d = r.uniform(0.5, 1.1)
            f = barrido(r.uniform(70, 110), r.uniform(140, 220), d) * (1 + 0.15 * np.sin(2 * np.pi * 9 * _t(d)))
            g = lp(osc(f, d, "saw"), 500) * np.sin(np.pi * _t(d) / d) ** 2
            i = int(r.uniform(0, max(0.01, dur - d)) * SR)
            out[i:i + len(g)] += g * 0.6
        return norm(out, 0.5)

    def crujido(dur=1.0, seed=0, f0=60):
        """Músculo o casco que se aprieta: diente de sierra grave con fricción irregular."""
        t = _t(dur)
        r = rng(seed)
        j = np.cumsum(r.normal(0, 1, len(t)))
        j = (j - j.mean()) / (np.abs(j).max() + 1e-6)
        f = f0 * (1 + 0.35 * j) * (1 + 0.3 * t / dur)
        x = bp(osc(f, dur, "saw"), 80, 1400) * (0.5 + 0.5 * np.abs(np.sin(2 * np.pi * 7 * t)))
        return norm(x * np.sin(np.pi * t / dur) ** 0.6, 0.6)

    def chisporroteo(dur, seed=0):
        """Ácido: siseo agudo + chasquiditos al azar."""
        r = rng(seed)
        x = hp(ruido(dur, seed), 3500) * 0.18 * (0.7 + 0.3 * np.sin(2 * np.pi * 0.7 * _t(dur)))
        for k in range(int(dur * 28)):
            d = 0.006
            c = hp(ruido(d, seed + 50 + k), 2500) * np.exp(-_t(d) / 0.0015) * r.uniform(0.3, 1.0)
            i = int(r.uniform(0, dur - 0.01) * SR)
            x[i:i + len(c)] += c
        return norm(x * env(dur, 0.2, None), 0.4)

    def ping(f=1180, dur=1.6):
        """Ping de sonar: tono puro con eco largo."""
        x = osc(f, dur) * env(dur, 0.002, 0.18)
        e = np.zeros_like(x)
        k = int(0.32 * SR)
        e[k:] = x[:-k] * 0.35
        return norm(lp(x + e, 4000), 0.4)

    def impacto(seed=0):
        """Golpe grave de rótulo grande (boom con cola)."""
        d = 1.4
        x = osc(barrido(90, 32, d), d) * env(d, 0.004, 0.35) + lp(ruido(d, seed), 200, 3) * env(d, 0.002, 0.12) * 2
        return norm(x, 0.85)

    def tic(f=2600):
        d = 0.03
        return norm(osc(f, d, "cuad") * np.exp(-_t(d) / 0.004), 0.35)

    def alarma(dur):
        t = _t(dur)
        f = np.where((t * 4) % 1 < 0.5, 880, 660)
        x = lp(osc(f, dur, "cuad"), 3000) * ((t * 8) % 1 < 0.8)
        return norm(x * env(dur, 0.01, None), 0.32)

    def siseo(dur, seed=0):
        """El tanque se vacía: siseo que baja de fuerza y tono."""
        t = _t(dur)
        n = ruido(dur, seed)
        out = np.zeros_like(n)
        for k in range(8):
            a, b = int(k * len(n) / 8), int((k + 1) * len(n) / 8)
            out[a:b] = bp(n, 3000 * (0.5) ** (k / 7), 9000 * (0.6) ** (k / 7))[a:b]
        return norm(out * (1 - 0.7 * t / dur) * env(dur, 0.05, None), 0.4)

    def acorde_veneno(dur=1.6):
        """Acorde disonante grave (tritono + segunda) que se tuerce."""
        t = _t(dur)
        x = sum(osc(f * (1 - 0.03 * t / dur), dur, "saw") for f in (110, 155.6, 116.5))
        return norm(lp(x, 700) * env(dur, 0.04, 0.6), 0.55)

    def ding(seed=0):
        """«¡Idea!»: campana brillante (fundamental + parciales de campana)."""
        d = 1.4
        x = sum(osc(1568 * m, d) * env(d, 0.002, 0.5 / (1 + i)) / (1 + i) for i, m in enumerate((1, 2.0, 2.4, 3.0)))
        return norm(x, 0.5)

    def arcada(seed=0, dur=0.9):
        """Arcada de la ballena: gruñido grave con formantes que suben y ruido húmedo."""
        t = _t(dur)
        f = 70 * (1 + 0.5 * t / dur) * (1 + 0.08 * np.sin(2 * np.pi * 13 * t))
        x = osc(f, dur, "saw")
        x = bp(x, 200, 900) + 0.6 * lp(ruido(dur, seed), 900, 3)
        return norm(x * np.sin(np.pi * t / dur) ** 0.5, 0.85)

    def clac(seed=0):
        """Pico de calamar (quitina) que choca: clic de madera."""
        d = 0.08
        r = rng(seed)
        f = r.uniform(900, 1500)
        x = osc(f, d) * np.exp(-_t(d) / 0.012) + bp(ruido(d, seed), 1500, 5000) * np.exp(-_t(d) / 0.004) * 0.6
        return norm(x, 0.45)

    def olas(dur, seed=0):
        t = _t(dur)
        x = lp(ruido(dur, seed), 900, 2) * (0.35 + 0.65 * (0.5 + 0.5 * np.sin(2 * np.pi * t / 3.3)) ** 2)
        return norm(x, 0.35)

    def gaviota(seed=0):
        d = 0.5
        out = np.zeros(int(1.0 * SR))
        for k in range(2):
            dd = d * (0.7 if k else 1)
            t = _t(dd)
            f = barrido(2200, 1300, dd) * (1 + 0.04 * np.sin(2 * np.pi * 30 * t))
            x = bp(osc(f, dd, "saw"), 900, 4000) * np.sin(np.pi * t / dd) ** 0.5
            i = int(k * 0.42 * SR)
            out[i:i + len(x)] += x
        return norm(out, 0.3)

    def chapuzon(seed=0):
        d = 0.9
        x = lp(ruido(d, seed), 3000, 2) * env(d, 0.005, 0.18)
        x[:int(0.3 * SR)] += osc(barrido(220, 70, 0.3), 0.3) * env(0.3, 0.003, 0.1)
        return norm(x, 0.7)

    # ------------------------------------------------------------ eventos
    P = []

    def add(t, x, v=1.0, pan=0.0):
        P.append((t, x, v, pan))

    # ===== plano_b: casi ninguna ballena, garganta, jorobada 2021, cachalote
    add(B.T_INI - 0.05, S.whoosh(0.6, 101, 300, 2000), 0.5)
    add(B.T_INI, S.ambiente_agua(B.T_GARG - B.T_INI + 0.3, 102), 0.7)
    for k in range(3):
        tx = B.gNing + 0.25 + 0.3 * k
        add(tx, rotulador(110 + k, 0.18), 0.6, -0.3 + 0.3 * k)
        add(tx + 0.12, rotulador(120 + k, 0.18), 0.55, -0.3 + 0.3 * k)
    add(B.gNot + 0.1, S.destello(130), 0.6, -0.3)
    add(B.gNot + 0.2, S.bip(131, 1500), 0.4, 0.4)
    add(B.T_GARG - 0.05, S.whoosh(0.5, 132, 200, 1200), 0.5)
    add(B.T_GARG, tripas(B.T_JOR - B.T_GARG + 0.3, 133), 0.5)
    add(B.gGar, silbido_caida(B.gEstr - B.gGar), 0.4)
    add(B.gGar + 0.3, S.burbuja(134), 0.4, 0.2)                     # el pez pasa
    add(B.gEstr - 0.05, chof(135, 0.8), 0.8)
    for k in range(4):
        add(B.gEstr + 0.05 + 0.33 * k, chirrido_goma(140 + k, 0.28), 0.7, -0.2 + 0.13 * k)
    add(B.gEstr + 0.05, S.boing(141, 260, 520), 0.6)
    add(B.gEstr + 0.3, S.bip(142, 1700, 0.05), 0.35, 0.5)
    add(B.T_JOR - 0.05, S.whoosh(0.5, 150, 400, 2500), 0.5)
    add(B.T_JOR, S.ambiente_agua(B.T_CACH - B.T_JOR + 0.3, 151), 0.8)
    add(B.j2021 - 0.05, S.destello(152), 0.6, 0.4)
    add(B.j2021, impacto(153), 0.45)
    add(B.jJor - 0.5, S.whoosh(1.0, 154, 120, 900), 0.7)
    add(B.jJor - 0.2, S.canto_ballena(155, 1.6, 260, 180), 0.6, -0.2)
    add(B.jAtr + 0.05, chof(156, 1.4), 0.9)
    add(B.jAtr + 0.1, S.rafaga_burbujas(6, 157, 0.6), 0.6)
    add(B.jBoca + 0.3, S.signo(158), 0.55, 0.4)
    add(B.jEsc - 0.05, S.pop(159, 700, 260, 0.2), 0.8)
    add(B.jEsc, S.rafaga_burbujas(10, 160, 1.0), 0.8)
    add(B.jEsc + 0.05, S.whoosh(0.8, 161, 300, 2200), 0.55)
    add(B.jEsc + 0.5, S.destello(162), 0.35, 0.3)
    add(B.T_CACH - 0.05, S.whoosh(0.6, 170, 150, 900), 0.5)
    add(B.T_CACH, S.ambiente_agua(B.T_FIN - B.T_CACH + 0.6, 171), 0.7)
    add(B.T_CACH + 0.3, chasquidos(14, 172, 0.1), 0.6, 0.5)
    add(B.cCach - 0.1, S.canto_ballena(173, 2.0, 140, 95), 0.6, 0.3)
    add(B.cCach - 0.1, impacto(174), 0.4)
    add(B.cPuede, S.boing(175), 0.55, -0.1)
    add(B.cTraga - 0.4, chasquidos(8, 176, 0.06), 0.45, 0.3)
    add(B.cCalam + 0.2, sorbido(177, B.cEnt + 0.4 - B.cCalam), 0.8, -0.3)
    add(B.cEnt + 0.4, S.trago(178), 0.9)
    add(B.cEnt - 0.2, wahwah(179), 0.5, -0.4)

    # ===== plano_c: estómago
    add(C.T_INI - 0.05, S.whoosh(0.6, 200, 150, 900), 0.5)
    add(C.T_INI, tripas(C.T_INM - C.T_INI, 201), 0.55)
    k, tl = 0, C.aCae + 1.5
    while tl < C.T_INM - 0.5:                                   # latido lejano, cada vez más rápido al apretar
        add(tl, S.latido(210 + k), 0.35)
        tl += 1.0 if tl < C.aPar else 0.8
        k += 1
    add(C.aCae - 0.2, silbido_caida(1.0), 0.45)
    add(C.aCae + 0.9, chof(220), 0.9)
    add(C.aOsc + 0.15, clic(221), 0.7, -0.1)
    add(C.aOsc + 0.25, S.bip(222, 1200, 0.06), 0.35, 0.4)
    add(C.a37 - 0.15, S.pop(223, 500, 900, 0.18), 0.5, -0.5)
    add(C.a37, S.osc(S.barrido(300, 900, 0.7), 0.7, "tri") * S.env(0.7, 0.01, None) * 0.25, 0.6, -0.5)
    add(C.a37 + 0.5, S.burbuja(224, 0.6), 0.35, -0.2)
    add(C.a37 + 0.8, S.burbuja(225, 0.6), 0.35, 0.2)
    add(C.aPar - 0.1, crujido(C.aApr + 0.8 - C.aPar, 226, 55), 0.75)
    add(C.aPar, S.boing(227, 300, 180, 0.4), 0.5)
    for k in range(3):
        add(C.aPar + 0.4 + 0.5 * k, chirrido_goma(228 + k, 0.25), 0.5, -0.3 + 0.3 * k)
    add(C.bMas - 0.15, S.whoosh(1.0, 230, 1200, 200), 0.5)
    add(C.bMas + 0.9, chapuzon(231), 0.8)
    add(C.bMas + 0.9, chisporroteo(C.T_INM - C.bMas - 0.6, 232), 0.7)
    add(C.bMas + 0.9, S.rafaga_burbujas(12, 233, C.T_INM - C.bMas - 1.2), 0.45)
    add(C.bAcido - 0.05, S.pop(234, 900, 400, 0.2), 0.6)
    add(C.bAcido, chisporroteo(1.2, 235), 0.7, 0.2)
    add(C.bPiel - 0.2, S.pop(236, 600, 1200, 0.15), 0.5, 0.3)
    add(C.bPiel, S.boing(237, 400, 800, 0.3), 0.55, 0.4)
    add(C.bPiel + 0.1, chisporroteo(1.4, 238), 0.9, 0.3)
    add(C.bNo + 0.1, S.bip(239, 900, 0.08), 0.35, 0.5)

    # ===== inmersión: el cachalote baja a 1 000 m
    add(C.T_INM - 0.05, S.whoosh(0.5, 300, 200, 1500), 0.5)
    add(C.T_INM, S.ambiente_agua(C.T_PRES - C.T_INM + 0.4, 301), 0.8)
    add(C.iCach - 0.2, S.canto_ballena(302, 2.2, 180, 120), 0.7)
    add(C.iBaja - 0.2, S.retumbo(C.iMil + 1.0 - C.iBaja, 303), 0.5)
    add(C.iBaja, S.whoosh(1.5, 304, 900, 120), 0.45)
    prof = lambda t: suave(pr(t, C.iBaja - 0.1, C.iMil + 0.7)) * 0.86 + 0.14 * pr(t, C.iMil + 0.7, C.T_PRES + 0.5)
    tt = np.arange(C.iBaja - 0.2, C.T_PRES, 0.01)
    pp = np.array([prof(x) for x in tt])
    for k, marca in enumerate((0.25, 0.5, 0.75)):          # ping de sonar al pasar cada marca de 250 m
        i = int(np.argmax(pp >= marca))
        if pp[i] >= marca:
            add(tt[i], ping(1180 - 120 * k), 0.5, -0.6)
    add(C.iMil - 0.1, impacto(305), 0.6)
    add(C.iMil + 0.2, crujido(1.2, 306, 40), 0.45)

    # ===== presión ×100, el tanque se vacía, el O2 se vuelve veneno
    add(C.T_PRES - 0.05, S.whoosh(0.5, 400, 150, 900), 0.5)
    add(C.T_PRES, tripas(C.vVom - C.T_PRES, 401), 0.4)
    add(C.pPres - 0.1, crujido(2.2, 402, 45), 0.8)
    for k in range(4):
        add(C.pPres - 0.1 + 0.06 * k, S.whoosh(0.3, 403 + k, 1500, 300), 0.35, (-0.6, 0.6, 0.0, 0.0)[k])
    add(C.pCien - 0.05, impacto(410), 0.9)
    add(C.pCien, S.boing(411, 200, 500, 0.35), 0.4)
    add(C.pTanq - 0.25, S.pop(412, 700, 1100, 0.15), 0.5, -0.5)
    add(C.pVac - 0.3, siseo(C.pMin + 0.5 - C.pVac, 413), 0.7, -0.2)
    add(C.pVac - 0.3, S.rafaga_burbujas(14, 414, C.pMin + 0.4 - C.pVac), 0.5)
    t_, k = C.pVac, 0
    while t_ < C.pMin + 0.1:                                  # tic del manómetro, cada vez más rápido
        add(t_, tic(2600 + 40 * k), 0.5, -0.5)
        t_ += max(0.06, 0.22 - 0.025 * k)
        k += 1
    add(C.pMin + 0.05, alarma(C.pVen + 0.8 - C.pMin), 0.45, -0.5)
    add(C.pOxi - 0.1, S.pop(420, 800, 1300, 0.15), 0.5, 0.4)
    add(C.pVen - 0.1, acorde_veneno(1.8), 0.7, 0.3)
    add(C.pVen + 0.1, S.boing(421, 500, 250, 0.5), 0.4)
    add(C.vSal - 0.1, ding(430), 0.7, 0.4)
    add(C.vSal, S.bip(431, 1600), 0.45, 0.4)

    # ===== el vómito
    add(C.vVom - 0.15, arcada(440, 0.85), 1.0)
    add(C.vVom - 0.1, crujido(0.6, 441, 70), 0.6)
    add(C.T_FUERA - 0.05, S.whoosh(0.5, 442, 300, 2500), 0.6)
    add(C.T_FUERA + 0.05, chapuzon(443), 0.9)
    add(C.T_FUERA + 0.1, S.rafaga_burbujas(16, 444, 1.2), 0.8)
    add(C.T_FUERA + 0.15, S.ambiente_agua(C.T_ATAR - C.T_FUERA + 0.4, 445), 0.7)
    add(C.T_FUERA + 0.2, S.whoosh(1.0, 446, 400, 2800), 0.5, -0.4)
    for k in range(7):
        ts = C.vPicos - 0.5 + 0.12 * k
        add(ts, clac(450 + k), 0.6, 0.3 - 0.1 * k)
        add(ts + 0.7 + 0.1 * k, clac(460 + k), 0.4, -0.4)
    add(C.T_FUERA + 1.0, S.destello(470), 0.35, -0.3)
    add(C.T_FUERA + 0.6, S.bip(471, 1400), 0.4, 0.2)

    # ===== cierre: atardecer
    add(C.T_ATAR - 0.05, S.whoosh(0.7, 500, 2000, 300), 0.5)
    add(C.T_ATAR, olas(C.T_FIN - C.T_ATAR + 0.2, 501), 0.8)
    add(C.T_ATAR + 0.4, chapuzon(502), 0.4)
    add(C.T_ATAR + 0.8, gaviota(503), 0.4, 0.6)
    add(C.zDif + 1.3, gaviota(504), 0.3, -0.6)
    add(C.zEres - 0.2, S.bip(505, 1300), 0.45, 0.2)
    for k in range(4):
        add(C.zEres + 0.2 + 0.5 * k, S.pop(506 + k, 900 + 100 * k, 1400 + 100 * k, 0.12), 0.3, 0.1 * k)
    add(C.zDif - 0.5, chapuzon(510), 0.6, 0.6)
    add(C.zDif + 0.2, S.canto_ballena(511, 1.8, 230, 170), 0.4, 0.6)
    add(C.zDig, S.destello(512), 0.55)
    return P
