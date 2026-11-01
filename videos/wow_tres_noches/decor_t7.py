# -*- coding: utf-8 -*-
"""Decorados del tramo 7 de «Tres noches» (5:50-8:50, 15-oct-2026), estilo «grabado de peste» en espacio 3D:
  alba              el amanecer del Alba Argenta (cura): los furiosos escriben, la cura, la plaga se apaga en ceniza, el Rey
                    Exánime en las nubes, y los que eligen seguir siendo la plaga
  fila / emboscada  las aguas termales de Cuna del Invierno (funeral, fila, emboscada): la jugadora que pescaba, el farol III,
                    los foros, la fila con velas junto al agua, la colina... y la carga de la hermandad
  cementerio_final  el cementerio del Ángel: «video» (las almas del funeral llegan con sus velas; el video y los correos) y
                    «promesa» (los tres faroles, «fueron ustedes», la tumba sin nombre que se cierra)
  plaza             el memorial seguro dentro de la ciudad
  seleccion / cierre  la pantalla de selección: tu personaje, solo, esperando
  susto3 / susto4   la carga que se te echa encima (7:17) · el Ángel abre los ojos (8:42)
Por respeto: la jugadora del funeral no tiene nombre ni cara; los correos se parafrasean (no se citan)."""
import math

import numpy as np

import anclas as A
import comun as C
import fig as F
import fig2 as F2
import grabado as GR
import grabado_3d as G3
import look as L
from decor_t6 import _cartel, _colgar
from grabado import ESPECTRO, HIELO, ORO, PLAGA, SANGRE, TINTA, G, circ_pts, e_out, lerp, pr, rnd, smooth

NIEVE_COLOR = (0.86, 0.89, 0.92)


def tr_(pts, x, y, ang):
    return GR.tr(pts, x, y, 1.0, ang)


def flash(nombre, t):
    if nombre == "alba":                                     # el sol sale a «Alba»
        return 0.22 * smooth(pr(t, A.u_alba - 0.2, A.u_alba + 0.2)) * (1 - smooth(pr(t, A.u_alba + 0.3, A.u_alba + 1.2)))
    return 0.0


def _p(cam, X, Y, Z):
    px, py, zc = cam.pt(X, Y, Z)
    return px, py, cam.k(zc)


# ====================================================================== 1. EL AMANECER DEL ALBA ARGENTA (cura)
CAM_AL = dict(x=0.0, y=-240.0, z=0.0, guinada=0.0, cabeceo=-3.0, f=1450.0, foco=1500.0, apertura=3.0, bruma=0.5,
              lejos=3400.0)
KF_ALBA = [(A.T_FIN_T6 - 0.3, dict(x=0.0, y=-240.0, z=-80.0, guinada=-6.0, cabeceo=-3.0, foco=1300.0)),
           (A.u_escribian, dict(x=-30.0, y=-245.0, z=0.0, guinada=-10.0, cabeceo=-4.0, foco=1200.0)),
           (A.u_alba, dict(x=0.0, y=-250.0, z=80.0, guinada=0.0, cabeceo=-5.0, foco=2200.0)),
           (A.u_rey, dict(x=10.0, y=-260.0, z=140.0, guinada=2.0, cabeceo=-10.0, foco=3500.0)),
           (A.u_muchos, dict(x=0.0, y=-240.0, z=220.0, guinada=0.0, cabeceo=-2.0, foco=1350.0)),
           (A.TR_TERMALES + 0.6, dict(x=0.0, y=-235.0, z=280.0, guinada=0.0, cabeceo=-1.0, foco=1300.0))]
QUEJAS = [("Foro", "Kaelthor", "llevo tres días sin poder jugar", 0.0), ("Foro", "Brunilda", "esto ya no tiene gracia", 0.9),
          ("Foro", "Zarg", "¡quiten la plaga de una vez!", 1.8), ("Foro", "Liessa", "me comieron en el banco OTRA vez", 2.7)]


def alba(t):
    cam = C.camara(t, KF_ALBA, CAM_AL)
    g = G(t)
    hz = cam.horizonte()
    sol = smooth(pr(t, A.u_seis, A.u_cura + 0.5))
    GR.cielo(g, t, hz + 40, tono_alto=0.95 - 0.25 * sol, tono_bajo=0.55 - 0.35 * sol, estrellas=int(40 * (1 - sol)))
    ox = cam.pt(0, 0, 9000)[0] - 960
    sx, sy = 960 + ox, hz + 30 - 120 * sol                  # el sol que asoma
    if sol > 0.01:
        g.papel(circ_pts(sx, sy, 90, 40), sol)
        g.trama(circ_pts(sx, sy, 90, 40), 0.1, ang=0, per=4, cruz=False, op=sol)
        g.acento_luz(sx, sy, 900, ORO, 0.75 * sol)
        G3.haz(g, sx, sy, -90, 120, 900, t, op=0.25 * sol, color=(1.0, 0.92, 0.75))
    rey = C.env(t, A.u_rey - 0.4, A.u_aprendi, 0.6, 0.8)
    if rey > 0.01:
        F2.corona_lich(g, 1400 + ox * 0.8, hz - 330, 1.25, t, op=rey)
    GR.nube(g, 400 + ox * 0.8, hz - 300, 560, t, sem=81, vel=5, tono=0.35)
    for j, (y0, amp, tn) in enumerate(((hz - 60, 90, 0.5), (hz - 10, 50, 0.62))):
        GR.colina(g, GR.perfil_colina(-80, 2000, y0, amp, sem=80 + j, n=14), tono=tn, tono2=tn + 0.3, ang=-8, per=5.4,
                  contorno=1.6, cruz=False)
    G3.plano(g, cam, (-6000, 0, -600), (1, 0, 0), (0, 0, 1), 12000, 6000, 0.55, familias=((0.0, 15.0),),
             luces=[(0, -300, 4000, 3000, 0.3 + 0.5 * sol)], oscuro=0.2)
    objs = []
    for i in range(14):                                      # árboles muertos de las Tierras de la Peste
        X = (rnd(i, 91) - 0.5) * 5000
        Z = 1300 + 2500 * rnd(i, 92)
        if abs(X) < 500:
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: GR.arbol_seco(c, *cam.pt(X, 0, Z)[:2], 0.9 * cam.k(cam.pt(X, 0, Z)[2]),
                                                                      t, sem=i + 40)))
    # el campamento del Alba Argenta: estandartes y centinelas REALES
    for sg in (-1, 1):
        X, Z = sg * 640, 1500
        objs.append((X, 0, Z, lambda c, X=X, Z=Z: G3.trazo3d(c, cam, [(X, 0, Z), (X, -760, Z)], 12, afilado=0.0)))
    C.peg(objs, cam, t, "Argent Sentry", -520.0, 1350.0, 370.0, sem=700)
    C.peg(objs, cam, t, "Lord Maxwell Tyrosus", 520.0, 1420.0, 370.0, sem=701, espejo=True)
    # los necrófagos del campo: se deshacen en ceniza a «cura» / «apagó»
    ceniza = smooth(pr(t, A.u_cura - 0.2, A.u_apago + 0.4))
    for i in range(8):
        X = -450 + 130 * i + 60 * rnd(i, 93)
        Z = 2000 + 600 * rnd(i, 94)
        op = 1 - smooth(pr(ceniza, 0.1 * (i % 4), 0.6 + 0.1 * (i % 4)))
        if op <= 0.01:
            continue
        if i % 3 == 0:
            C.peg(objs, cam, t, ("Ghoul Ravener", "Rotted One", "Flesh Eater")[i % 3], X, Z, 330.0, op=op, aura=0.6 * op,
                  color_aura=PLAGA, sem=710 + i)
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i, op=op: F2.necrofago(
            c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, fase=i, anda=0.3, op=op, sem=720 + i)))
    # los supervivientes; a «eligen», unos cuantos vuelven a encender su aura verde (eligen ser la plaga)
    elige = smooth(pr(t, A.u_eligen - 0.3, A.u_plaga2 + 0.3))
    for j in range(6):
        X = (-1 if j < 3 else 1) * (620 + 190 * (j % 3))
        Z = 1750 + 120 * (j % 3)
        verde = elige if j in (1, 4) else 0.0
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, j=j, verde=verde: F.persona(
            c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, ("capa", "enano", "guerrero", "sanador", "capa",
                                                                         "mercader")[j], fase=j, anda=0.0,
            dirx=-1 if j % 2 else 1, aura=verde, color_aura=PLAGA, sem=730 + j,
            brazos=(2.4, 2.7) if verde > 0.5 else None)))
    if elige > 0.01:                                          # uno baila: la danza macabra vuelve a empezar
        X, Z = 640.0, 1950.0
        objs.append((X, 0, Z, lambda c: (
            c.acento_luz(*cam.pt(X, -200, Z)[:2], 280 * cam.k(cam.pt(X, 0, Z)[2]), PLAGA, 0.7 * elige),
            GR.esqueleto_baila(c, *cam.pt(X, 0, Z)[:2], 0.9 * cam.k(cam.pt(X, 0, Z)[2]), t, 0.5, op=elige,
                         ojos=1.0))))
    C.figuras(g, cam, objs)
    for sg in (-1, 1):                                        # los estandartes del Alba Argenta (tela con el sol)
        _cartel(g, cam, (sg * 640 + sg * 10, -560.0, 1495.0), "Alba Argenta", t, op=1.0, ancho=300, alto=110, px=36,
                U=(1, 0, 0), giro=sg * 2 * math.sin(t))
    op = C.env(t, A.u_odiaron - 0.4, A.u_seis, 0.4, 0.6)
    if op > 0.01:
        s = G(t, 900, 300, alfa=True)
        GR.chat(s, 20, 290, [(c_, a_, x_, A.u_odiaron + d_) for c_, a_, x_, d_ in QUEJAS], t, corr=0.15, ancho=860, px=30,
                sem=4, color_canal=PLAGA)
        _colgar(g, cam, s, (-260.0, -470.0 + 6 * math.sin(t), 1500.0), 760, t, op=op, techo=-1300, U=(0.92, 0, 0.38),
                sombra=0.35)
    G3.iluminar(g, [(sx, sy, 1400, 0.3 + 0.5 * sol, ORO)], amb=0.25 + 0.15 * sol, fuerza=0.55, acento=0.15)
    G3.particulas(g, t, "ceniza", int(30 + 80 * ceniza), (0, 200, 1920, 1080), sem=95, op=0.4 + 0.6 * ceniza)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2000)[1]
    GR.niebla(g, y_nb - 50, y_nb + 10, t, op=0.5, sem=96, vel=14)
    with G3.capa_prof(g, cam, 240) as c:
        px, py, zc = cam.pt(cam.C[0] - 300, 0, cam.C[2] + 320)
        GR.arbol_seco(c, px, py, 1.1 * cam.k(zc), t, sem=97)
    return g


# ====================================================================== 2. LAS AGUAS TERMALES DE CUNA DEL INVIERNO
CAM_W = dict(x=0.0, y=-230.0, z=0.0, guinada=0.0, cabeceo=-3.0, f=1450.0, foco=1400.0, apertura=3.0, bruma=0.5,
             lejos=3600.0)
POZA = (-150.0, 2000.0, 650.0, 380.0)            # centro x, z, semiejes
CANA = (-330.0, 1560.0)
COLINA_X = 700.0
KF_FILA = [(A.TR_TERMALES - 0.6, dict(x=-60.0, y=-260.0, z=-100.0, guinada=-3.0, cabeceo=-4.0, foco=1700.0)),
           (A.f_2006, dict(x=-60.0, y=-260.0, z=40.0, guinada=-6.0, cabeceo=-4.0, foco=1500.0)),
           (A.f_jugadora, dict(x=-120.0, y=-240.0, z=180.0, guinada=-12.0, cabeceo=-3.0, foco=1300.0)),
           (A.f_real + 0.5, dict(x=-140.0, y=-240.0, z=230.0, guinada=-14.0, cabeceo=-3.0, foco=1250.0)),
           (A.f_companeros, dict(x=-80.0, y=-260.0, z=200.0, guinada=-4.0, cabeceo=-4.0, foco=1700.0)),
           (A.f_aguas, dict(x=-40.0, y=-270.0, z=200.0, guinada=0.0, cabeceo=-6.0, foco=1900.0)),
           (A.f_pescar, dict(x=-160.0, y=-240.0, z=300.0, guinada=-16.0, cabeceo=-2.0, foco=1200.0)),
           (A.f_foros, dict(x=-60.0, y=-260.0, z=280.0, guinada=-2.0, cabeceo=-4.0, foco=1100.0)),
           (A.f_cualquiera2, dict(x=40.0, y=-270.0, z=300.0, guinada=14.0, cabeceo=-6.0, foco=2800.0)),
           (A.i_llegaron, dict(x=0.0, y=-280.0, z=260.0, guinada=0.0, cabeceo=-5.0, foco=1700.0)),
           (A.i_illidan, dict(x=30.0, y=-280.0, z=300.0, guinada=4.0, cabeceo=-5.0, foco=1700.0)),
           (A.i_nadie, dict(x=60.0, y=-270.0, z=340.0, guinada=12.0, cabeceo=-7.0, foco=2600.0)),
           (A.T_APAGON3, dict(x=70.0, y=-265.0, z=380.0, guinada=15.0, cabeceo=-8.0, foco=2800.0))]
KF_EMB = [(A.T_VUELVE3 - 0.3, dict(x=80.0, y=-300.0, z=300.0, guinada=12.0, cabeceo=-8.0, foco=2600.0)),
          (A.e_hermandad, dict(x=60.0, y=-300.0, z=260.0, guinada=8.0, cabeceo=-6.0, foco=2000.0)),
          (A.e_mataron, dict(x=0.0, y=-290.0, z=220.0, guinada=0.0, cabeceo=-4.0, foco=1700.0)),
          (A.e_defendio, dict(x=-40.0, y=-280.0, z=180.0, guinada=-4.0, cabeceo=-4.0, foco=1600.0)),
          (A.TR_CEM2 + 0.6, dict(x=-50.0, y=-280.0, z=160.0, guinada=-5.0, cabeceo=-4.0, foco=1600.0))]
FILA = [(-650.0 + 115 * i, 1640.0 - 30 * math.sin(i * 0.7) + (i % 2) * 40) for i in range(13)]
FORO = [("Foro de Illidan", "", "Memorial en las aguas termales de Cuna del Invierno.", 0.0),
        ("Foro de Illidan", "", "Le gustaba pescar ahí. Todos son bienvenidos.", 1.2)]


def _poza(g, cam, t):
    """La poza termal: agua (trazo quebrado), orilla de nieve, la roca roja del centro y el vapor."""
    cx, cz, ax, az = POZA
    borde = [(cx + ax * 1.12 * math.cos(a), 0, cz + az * 1.15 * math.sin(a)) for a in np.linspace(0, 6.2832, 48)]
    scr, _ = G3.proyectar(cam, borde)
    if scr is not None:
        g.figura(scr, 0.25, contorno=2.4, ang=0, per=4.8, cruz=False)
    agua = [(cx + ax * math.cos(a), 6, cz + az * math.sin(a)) for a in np.linspace(0, 6.2832, 48)]
    scr, _ = G3.proyectar(cam, agua)
    if scr is not None:
        g.figura(scr, 0.6, contorno=2.0, ang=0, per=4.2, cruz=False)
        for j in range(9):                                   # trazos quebrados horizontales: agua que se mueve
            yy = scr[:, 1].min() + (scr[:, 1].max() - scr[:, 1].min()) * (j + 0.5) / 9
            x0, x1 = scr[:, 0].min() + 30, scr[:, 0].max() - 30
            for k_ in range(6):
                xa = lerp(x0, x1, (k_ + 0.15 * math.sin(t * 1.3 + j + k_)) / 6)
                g.trazo([(xa, yy), (xa + (x1 - x0) / 14, yy)], 1.6, color=g.fondo_papel, op=0.6, afilado=0.6)
        g.acento(scr, HIELO, 0.4, sem=3)
    rx, ry, k = _p(cam, cx + 40, 0, cz + 40)                 # la roca del centro con su brasa roja
    g.figura(np.float32([(rx - 110 * k, ry), (rx - 60 * k, ry - 130 * k), (rx + 20 * k, ry - 160 * k), (rx + 90 * k, ry - 90 * k),
                         (rx + 120 * k, ry)]), 0.55, contorno=2.2, ang=60, per=4.4, cruz=False)
    g.acento_luz(rx, ry - 170 * k, 120 * k, SANGRE, 0.7)
    GR.llama(g, rx, ry - 150 * k, 0.5 * k, t, sem=8, color=SANGRE)
    for i in range(5):                                        # vapor
        vx, vy, kk = _p(cam, cx + (i - 2) * ax * 0.35, 0, cz + (rnd(i, 5) - 0.5) * az)
        G3.humo(g, vx, vy, 1.3 * kk * 3, t, sem=i + 30, op=0.35, color=NIEVE_COLOR, alto=420, hebras=2)


def _termales(t, kf, base, clave):
    """Fondo de las aguas termales, cacheado por tick de HERVOR (GR.fondo): cielo, luna y montañas (se corren con el
    horizonte) y, con la cámara quieta, el suelo y la colina nevada. La poza (agua que se mueve) va en vivo."""
    def lejos(g, tt):
        cam = C.camara(tt, kf, base)
        hz = cam.horizonte()
        GR.cielo(g, tt, hz + 40, tono_alto=0.96, tono_bajo=0.6, estrellas=50)
        ox = cam.pt(0, 0, 9000)[0] - 960
        GR.luna(g, 650 + ox, hz - 360, 58, tt, tono_cielo=0.86)
        for j, (y0, amp, tn) in enumerate(((hz - 280, 170, 0.42), (hz - 130, 110, 0.55))):
            perf = GR.perfil_colina(-80, 2000, y0, amp, sem=100 + j, n=18, ondas=2.5)
            GR.colina(g, perf, tono=tn, tono2=tn + 0.3, ang=-25, per=5.5, contorno=1.8)
            for (cx_, cy_) in perf[perf[:, 1] < y0 - amp * 0.3][::2]:
                g.papel(circ_pts(cx_, cy_ + 18, 46, 10, 20), 0.85)

    def f_lejos(tt):
        cam = C.camara(tt, kf, base)
        return cam.horizonte(), cam.pt(0, 0, 9000)[0]
    g = GR.fondo(t, clave, [(lejos, f_lejos), (lambda g, tt: _termales_cerca(g, C.camara(tt, kf, base)),
                                                lambda tt: G3.firma_cerca(C.camara(tt, kf, base)))])
    _poza(g, C.camara(t, kf, base), t)
    return g


def _termales_cerca(g, cam):
    G3.plano(g, cam, (-6000, 0, -600), (1, 0, 0), (0, 0, 1), 12000, 6000, lambda a, b, zc: 0.12 + 0.08 * np.clip(b / 3000, 0, 1),
             familias=((0.0, 22.0),), oscuro=0.15)
    # la colina nevada por donde bajarán (a la derecha): ladera inclinada hacia el fondo
    cresta = [(COLINA_X + x_, -2600 * 0.45 - 40 * math.sin(x_ / 170.0), 900 + 2600 * 0.89) for x_ in np.linspace(0, 3000, 40)]
    falda = [(COLINA_X - 900 + 900 * s_, -1170 * s_ ** 1.6, 900 + 2314 * s_) for s_ in np.linspace(0, 1, 14)]
    pie = [(COLINA_X + 3000, 0, 900), (COLINA_X - 900, 0, 900)]
    scr, _ = G3.proyectar(cam, falda + cresta + pie)
    if scr is not None:                                      # la colina nevada por donde bajarán
        g.figura(scr, 0.3, contorno=2.6, tono2=0.5, luz=-30, ang=-22, per=5.4, cruz=False)
        sc2, _ = G3.proyectar(cam, falda + cresta, cerrado=False)
        if sc2 is not None:
            g.trazo(sc2 + np.float32((0, 8)), 10, color=g.fondo_papel, op=0.8, afilado=0.2)


def _pinos_nieve():
    out = []
    for i in range(30):
        X = (rnd(i, 121) - 0.5) * 6000
        Z = 2700 + 1800 * rnd(i, 122)
        out.append((X, Z, 0.8 + 0.6 * rnd(i, 123), i))
    for i in range(8):
        out.append((-1200 - 900 * rnd(i, 124), 1300 + 1200 * rnd(i, 125), 0.9 + 0.4 * rnd(i, 126), 50 + i))
    return out


def _pinos_ladera():
    """Pinos sobre la ladera de la derecha (Y sigue la pendiente): dan escala y la hacen colina, no cuña."""
    out = []
    for i in range(12):
        b = 300 + 2200 * rnd(i, 127)
        X = COLINA_X + 250 + 2600 * rnd(i, 128)
        out.append((X, -b * 0.45, 900 + b * 0.89, 0.8 + 0.4 * rnd(i, 129), 70 + i))
    return out


PINOS_LADERA = _pinos_ladera()


PINOS = _pinos_nieve()


def _comun_termales(objs, cam, t):
    for X, Z, s_, i in PINOS:
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, s_=s_, i=i: F.pino(c, *cam.pt(X, 0, Z)[:2], s_ * cam.k(cam.pt(X, 0, Z)[2]),
                                                                       t, sem=i)))
    for X, Y, Z, s_, i in PINOS_LADERA:
        objs.append((X, Y, Z, lambda c, X=X, Y=Y, Z=Z, s_=s_, i=i: F.pino(c, *cam.pt(X, Y, Z)[:2],
                                                                            s_ * cam.k(cam.pt(X, Y, Z)[2]), t, sem=i)))
    C.peg(objs, cam, t, "Donova Snowden", -1050.0, 2150.0, 360.0, sem=800)
    C.peg(objs, cam, t, "Frostsaber Stalker", 1250.0, 2700.0, 300.0, sem=801, espejo=True)


def fila(t):
    """Aguas termales (funeral + fila): 6:17-7:17."""
    cam = C.camara(t, KF_FILA, CAM_W)
    g = _termales(t, KF_FILA, CAM_W, "fila")
    luces = []
    objs = []
    _comun_termales(objs, cam, t)
    # el farol III (la tercera noche, azul helado) a la orilla
    f3 = smooth(pr(t, A.f_tercera - 0.3, A.f_tercera + 0.3)) * (1 - 0.8 * smooth(pr(t, A.T_APAGON3 - 0.2, A.T_APAGON3 + 0.2)))

    def farol3(c):
        fx, fy, k = F.farol(c, cam, 380.0, 1350.0, t, HIELO, f3, sem=810, alto=1.2)
        if f3 > 0.02:
            luces.append((fx, fy, 380 * k * f3, 0.6 * f3, HIELO))
        c.texto("III", *cam.pt(380, 0, 1350)[:2], max(12, int(30 * cam.k(cam.pt(380, 0, 1350)[2]))), TINTA, "gara_b", 0.9)
    objs.append((380.0, 0, 1350.0, farol3))
    # la jugadora que pescaba (de espaldas, sin cara): aparece a «jugadora» y se desvanece a «murió»; queda la caña
    op = C.env(t, A.f_jugadora - 0.4, A.f_murio, 0.5, 1.4)
    X, Z = CANA[0] - 60, CANA[1] - 80
    if op > 0.01:
        objs.append((X, 0, Z, lambda c, op=op, X=X, Z=Z: F.persona(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, "capa",
                                                          anda=0.0, dirx=1, op=op, sem=820, brazos=(0.5, 1.2), arma=False)))
    if t > A.f_jugadora - 0.4:
        objs.append((CANA[0], 0, CANA[1], lambda c: F2.cana(c, cam, CANA[0], CANA[1], t, agua=(POZA[0] - 260, POZA[1] - 200),
                                                             op=smooth(pr(t, A.f_jugadora - 0.4, A.f_jugadora)))))
    # los compañeros de hermandad y luego la fila larga junto al agua, con velas, en silencio
    llegan = smooth(pr(t, A.f_companeros - 0.5, A.f_juego + 0.5))
    fila_ = smooth(pr(t, A.i_llegaron - 0.6, A.i_silencio))
    for i, (X, Z) in enumerate(FILA):
        n_vis = 3 + int(10 * fila_)
        if i >= n_vis or (llegan <= 0.01 and fila_ <= 0.01):
            continue
        u = smooth(pr(t, A.f_companeros - 0.5 + 0.2 * i, A.f_companeros + 0.6 + 0.2 * i)) if i < 3 else \
            smooth(pr(t, A.i_llegaron - 0.6 + 0.25 * (i - 3), A.i_llegaron + 0.5 + 0.25 * (i - 3)))
        Xi = lerp(X - 700, X, u)
        Zi = lerp(Z + 300, Z, u)
        if i % 4 == 2:                                        # algunos dolientes REALES (pegatinas)
            C.peg(objs, cam, t, ("Brother Paxton", "Ironforge Mountaineer", "Archmage Malin")[i % 3], Xi, Zi,
                  (365.0, 285.0, 370.0)[i % 3], op=u, sem=830 + i, espejo=True)
            continue
        objs.append((Xi, 0, Zi, lambda c, Xi=Xi, Zi=Zi, i=i, u=u: (
            F.persona(c, *cam.pt(Xi, 0, Zi)[:2], 0.95 * cam.k(cam.pt(Xi, 0, Zi)[2]), t, ("capa", "enano", "sanador", "capa")[i % 4],
                      fase=i, anda=1.0 * (1 - u), dirx=1, op=u, sem=840 + i, brazos=(0.3, 1.5), arma=False),
            F2.vela(c, *cam.pt(Xi + 30, -230, Zi - 20)[:2], 1.3 * cam.k(cam.pt(Xi, 0, Zi)[2]), t, sem=i, op=u))))
    # en la cresta: a «verdad» asoman siluetas
    asoman = smooth(pr(t, A.i_verdad - 0.2, A.i_verdad + 0.8))
    for i in range(7):
        if asoman <= 0.01:
            break
        X = COLINA_X + 500 + 260 * i
        Z = 900 + 2600 * 0.89
        Y = -2600 * 0.45 + 5
        objs.append((X, Y, Z, lambda c, X=X, Y=Y, Z=Z, i=i: F.persona(
            c, *cam.pt(X, Y, Z)[:2], 0.95 * cam.k(cam.pt(X, Y, Z)[2]), t, "guerrero", anda=0.0, dirx=-1, op=asoman,
            tono=0.85, sem=850 + i)))
    C.figuras(g, cam, objs)
    # cartelas y lienzos colgados
    _cartel(g, cam, (-200.0, -620.0 + 6 * math.sin(t), 2100.0), "Illidan · MMVI", t,
            op=C.env(t, A.f_2006 - 0.3, A.f_jugadora, 0.4, 0.6), techo=-1400, ancho=520)
    _cartel(g, cam, (-560.0, -640.0 + 6 * math.sin(t), 2200.0), "Cuna del Invierno", t,
            op=C.env(t, A.f_cuna - 0.4, A.f_pescar + 0.4, 0.4, 0.6), techo=-1400, ancho=620)
    op = C.env(t, A.f_aguas - 0.4, A.f_foros - 0.2, 0.5, 0.5)
    C.recuerdo_colgado(g, cam, (380.0, -620.0 + 8 * math.sin(t), 2000.0), (0.9, 0, -0.44), "_crudos/MTmS8s5x3iI",
                       47.0 + (t - A.f_aguas) * 0.6, t, ancho=500, alto=320, texto="Fuentes termales", op=op, z=1.7,
                       cx=0.62, cy=0.36, tinta=0.25, sem=61)
    op = C.env(t, A.f_foros - 0.4, A.i_llegaron, 0.4, 0.6)
    if op > 0.01:
        s = G(t, 1000, 240, alfa=True)
        GR.chat(s, 20, 230, [(c_, a_, x_, A.f_foros + d_) for c_, a_, x_, d_ in FORO], t, ancho=960, px=30, sem=7,
                color_canal=HIELO)
        _colgar(g, cam, s, (-120.0, -470.0 + 6 * math.sin(t), 1650.0), 900, t, op=op, techo=-1400, sombra=0.35)
    op = C.env(t, A.i_fila - 0.4, A.i_illidan + 0.3, 0.4, 0.6)
    C.recuerdo_colgado(g, cam, (-520.0, -640.0 + 8 * math.sin(t), 2050.0), (0.9, 0, 0.44), "_crudos/MEpv7YxnLCQ",
                       205.0 + (t - A.i_fila) * 0.8, t, ancho=500, alto=330, texto="La fila · MMVI", op=op, z=1.25,
                       cx=0.48, cy=0.45, tinta=0.25, sem=62)
    _cartel(g, cam, (300.0, -620.0 + 6 * math.sin(t), 2000.0), "Jugador contra Jugador", t,
            op=C.env(t, A.i_jugador - 0.4, A.i_nadie - 0.2, 0.4, 0.6), techo=-1400, ancho=760)
    G3.iluminar(g, luces + [(*cam.pt(0, 0, 9000)[:2], 800, 0.25)], amb=0.36, fuerza=0.5, acento=0.12)
    G3.particulas(g, t, "nieve", 140, (0, 0, 1920, 1080), sem=111)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2400)[1]
    GR.niebla(g, y_nb - 40, y_nb + 10, t, op=0.45, sem=112, vel=20)
    with G3.capa_prof(g, cam, 260) as c:                      # primer plano: ramas de abeto nevadas
        px, py, zc = cam.pt(cam.C[0] - 340, 0, cam.C[2] + 300)
        F.pino(c, px, py, 1.1 * cam.k(zc), t, sem=113)
    return g


def emboscada(t):
    """La carga: bajan por la colina y matan a todos. 7:19-7:35."""
    cam = C.camara(t, KF_EMB, CAM_W)
    g = _termales(t, KF_EMB, CAM_W, "emboscada")
    objs = []
    _comun_termales(objs, cam, t)
    V = (0.0, -0.45, 0.89)
    carga = pr(t, A.T_VUELVE3 - 0.5, A.e_mataron + 0.4)
    for i in range(10):                                        # los atacantes bajan por la ladera hacia la fila
        u = smooth(min(1.0, carga * (1.0 + 0.08 * i)))
        L0 = 2400 - 300 * (i % 3)
        Ld = L0 * (1 - u)
        X0 = COLINA_X + 300 + 220 * (i % 5)
        tx, tz = FILA[(i * 3) % len(FILA)]
        X = lerp(X0, tx + 140, u)
        Z = lerp(900 + Ld * 0.89, tz + 90, u) if Ld > 0 else tz + 90
        Y = -Ld * 0.45 if X > COLINA_X else 0.0
        ataque = smooth(pr(t, A.e_mataron - 0.3 + 0.1 * i, A.e_mataron + 0.3 + 0.1 * i))
        objs.append((X, Y, Z, lambda c, X=X, Y=Y, Z=Z, i=i, u=u, ataque=ataque: F.persona(
            c, *cam.pt(X, Y, Z)[:2], 0.95 * cam.k(cam.pt(X, Y, Z)[2]), t, ("guerrero", "capa", "guerrero", "cazador")[i % 4],
            fase=i, anda=2.0 * (1 - smooth(pr(u, 0.9, 1.0))) + 0.1, dirx=-1, tono=0.75, sem=900 + i,
            brazos=(2.6, 2.4 - 2.2 * ataque) if u > 0.6 else (2.5, 2.7))))
    # los dolientes: no se defienden; caen uno a uno; quedan las velas en la nieve
    for i, (X, Z) in enumerate(FILA):
        tc = A.e_mataron + 0.22 * i
        cae = smooth(pr(t, tc, tc + 0.6))
        if i % 4 == 2:
            C.peg(objs, cam, t, ("Brother Paxton", "Ironforge Mountaineer", "Archmage Malin")[i % 3], X, Z,
                  (365.0, 285.0, 370.0)[i % 3], alza=1 - 0.6 * cae, op=1 - 0.85 * cae, sem=830 + i, espejo=True)
        else:
            objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i, cae=cae: F.persona(
                c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, ("capa", "enano", "sanador", "capa")[i % 4],
                fase=i, anda=0.0, dirx=1, cae=cae, sem=840 + i, brazos=(0.3, 1.5 - 1.2 * cae), arma=False)))
        objs.append((X + 30, 0, Z - 30, lambda c, X=X, Z=Z, i=i, cae=cae: F2.vela(
            c, *cam.pt(X + 40, 0, Z - 40)[:2] if cae > 0.5 else cam.pt(X + 30, -230, Z - 20)[:2],
            1.3 * cam.k(cam.pt(X, 0, Z)[2]), t, fuerza=1.0 - 0.7 * cae, sem=i)))
        if cae > 0.05:                                          # la sangre en la nieve
            objs.append((X, 0, Z - 40, lambda c, X=X, Z=Z, i=i, cae=cae: GR.salpicadura(
                c, *cam.pt(X + 60, -4, Z - 40)[:2], 70 * cam.k(cam.pt(X, 0, Z)[2]), sem=i, color=SANGRE, op=0.9 * cae,
                crece=cae)))
    C.figuras(g, cam, objs)
    # hechizos que cruzan: rayos de escarcha y de fuego
    for j in range(4):
        tj = A.e_armas + 0.5 * j
        u = pr(t, tj, tj + 0.5)
        if 0 < u < 1:
            a = cam.pt(COLINA_X + 600 + 200 * j, -900 + 100 * j, 2400)
            b = cam.pt(FILA[j * 3][0], -200, FILA[j * 3][1])
            p = (lerp(a[0], b[0], u), lerp(a[1], b[1], u))
            g.trazo([(lerp(a[0], b[0], max(0.0, u - 0.15)), lerp(a[1], b[1], max(0.0, u - 0.15))), p], 8, color=HIELO if j % 2
                    else SANGRE, op=0.9, afilado=0.7)
            g.acento_luz(p[0], p[1], 90, HIELO if j % 2 else SANGRE, 0.8)
    _cartel(g, cam, (900.0, -900.0 + 6 * math.sin(t), 2300.0), "Serenity Now", t,
            op=C.env(t, A.e_serenity - 0.3, A.e_mataron, 0.3, 0.5), techo=-1700, ancho=520, U=(0.95, 0, -0.3))
    op = C.env(t, A.e_mataron - 0.2, A.TR_CEM2 - 0.3, 0.4, 0.5)
    C.recuerdo_colgado(g, cam, (-430.0, -640.0 + 8 * math.sin(t), 2050.0), (0.9, 0, 0.44), "_crudos/MEpv7YxnLCQ",
                       298.0 + (t - A.e_mataron) * 0.8, t, ancho=500, alto=330, texto="Illidan · MMVI", op=op, z=1.25,
                       cx=0.48, cy=0.45, tinta=0.25, sem=63)
    G3.iluminar(g, [(*cam.pt(0, 0, 9000)[:2], 800, 0.25)], amb=0.34, fuerza=0.5, acento=0.15)
    G3.particulas(g, t, "nieve", 140, (0, 0, 1920, 1080), sem=114)
    y_nb = cam.pt(cam.C[0], 0, cam.C[2] + 2400)[1]
    GR.niebla(g, y_nb - 40, y_nb + 10, t, op=0.45, sem=115, vel=20)
    with G3.capa_prof(g, cam, 260) as c:
        px, py, zc = cam.pt(cam.C[0] - 340, 0, cam.C[2] + 300)
        F.pino(c, px, py, 1.1 * cam.k(zc), t, sem=113)
    return g


def susto3(t):
    """EL SUSTO (7:17): el yelmo de cubo de un atacante, pegado a la cámara, con los ojos helados ardiendo en la rendija,
    y el tajo de su espada que cruza el cuadro."""
    g = G(t)
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.97, ang=8, per=4.6)
    u = t - A.T_SUSTO3
    s = 1.0 + 0.18 * e_out(min(1.0, u / 0.5))
    x0, y0 = 1010, 560
    W_, H_ = 430 * s, 560 * s
    g.acento_luz(x0, y0, 1100, SANGRE, 0.35)
    gola = np.float32([(x0 - W_ * 1.25, 1140), (x0 - W_ * 0.9, y0 + H_ * 0.5), (x0 + W_ * 0.9, y0 + H_ * 0.5),
                       (x0 + W_ * 1.25, 1140)])
    g.figura(gola, 0.8, contorno=3.0, tono2=0.95, luz=-90, ang=10, per=4.2, cruz=False)
    yelmo = np.float32([(x0 - W_, y0 - H_ * 0.62), (x0 - W_ * 0.95, y0 - H_ * 0.9), (x0, y0 - H_ * 1.0),
                        (x0 + W_ * 0.95, y0 - H_ * 0.9), (x0 + W_, y0 - H_ * 0.62), (x0 + W_ * 0.96, y0 + H_ * 0.45),
                        (x0 + W_ * 0.5, y0 + H_ * 0.62), (x0 - W_ * 0.5, y0 + H_ * 0.62), (x0 - W_ * 0.96, y0 + H_ * 0.45)])
    g.figura(GR.catmull(yelmo, 3, True), 0.72, contorno=3.4, tono2=0.95, luz=-50, ang=80, per=3.8)
    for k_ in range(9):                                      # remaches
        g.circ(x0 - W_ * 0.85 + k_ * W_ * 0.21, y0 - H_ * 0.66, 7 * s, g.fondo_papel, 0.8)
    g.trazo([(x0 - W_, y0 - H_ * 0.6), (x0 + W_, y0 - H_ * 0.6)], 10 * s, afilado=0.0)
    # la rendija en T: ojos y respiradero, negros, con dos brasas de hielo
    g.macizo(np.float32([(x0 - W_ * 0.82, y0 - H_ * 0.2), (x0 + W_ * 0.82, y0 - H_ * 0.2), (x0 + W_ * 0.82, y0 - H_ * 0.08),
                         (x0 - W_ * 0.82, y0 - H_ * 0.08)]))
    g.macizo(np.float32([(x0 - W_ * 0.07, y0 - H_ * 0.08), (x0 + W_ * 0.07, y0 - H_ * 0.08), (x0 + W_ * 0.07, y0 + H_ * 0.45),
                         (x0 - W_ * 0.07, y0 + H_ * 0.45)]))
    for sg in (-1, 1):
        ex, ey = x0 + sg * W_ * 0.42, y0 - H_ * 0.14
        for r_, a_ in ((W_ * 0.7, 0.9), (W_ * 0.3, 1.0)):
            g.acento_luz(ex, ey, r_, HIELO, a_, 1.0)
        ojo = circ_pts(ex, ey, W_ * 0.12, 16, H_ * 0.03)
        g.papel(ojo, 1.0)
        g.acento(ojo, HIELO, 1.0)
    # el tajo de la espada
    k = min(1.0, u / 0.22)
    a0 = np.float32((1990, -80))
    a1 = a0 + (np.float32((-120, 1200)) - a0) * k
    d = (a1 - a0) / (np.linalg.norm(a1 - a0) + 1e-6)
    nrm = np.float32((-d[1], d[0]))
    hoja = np.float32([a0 + nrm * 46, a1 + nrm * 16, a1 - nrm * 16, a0 - nrm * 46])
    g.figura(hoja, 0.35, contorno=3.0, tono2=0.8, luz=0, ang=-40, per=3.6, cruz=False)
    g.trazo([a0 + nrm * 8, a1], 4, color=g.fondo_papel, op=0.9, afilado=0.8)
    for j in range(4):
        o = nrm * (70 + 34 * j)
        g.trazo([a0 + o, a1 + o * 0.6], 3, op=0.5 - 0.1 * j, afilado=0.9)
    GR.salpicadura(g, 560, 860, 320, sem=5, color=SANGRE, op=0.95, crece=min(1.0, u / 0.3))
    G3.particulas(g, t, "nieve", 160, (0, 0, 1920, 1080), sem=116, escala=2.0)
    return g


# ====================================================================== 3. EL CEMENTERIO DEL ÁNGEL (video, promesa)
KF_CVIDEO = [(A.TR_CEM2 - 0.3, dict(x=-40.0, y=-170.0, z=100.0, guinada=-3.0, cabeceo=-1.0)),
             (A.e_otro, dict(x=-20.0, y=-180.0, z=180.0, guinada=-2.0, cabeceo=-1.5)),
             (A.v_video, dict(x=0.0, y=-200.0, z=240.0, guinada=0.0, cabeceo=-6.0)),
             (A.v_famosos, dict(x=0.0, y=-210.0, z=200.0, guinada=0.0, cabeceo=-9.0)),
             (A.TR_PLAZA + 0.6, dict(x=10.0, y=-210.0, z=220.0, guinada=0.0, cabeceo=-9.0))]
KF_CPROMESA = [(A.TR_CEM3 - 0.3, dict(x=-60.0, y=-170.0, z=60.0, guinada=0.0, cabeceo=0.0)),
               (A.o_funeral, dict(x=-30.0, y=-175.0, z=140.0, guinada=2.0, cabeceo=-1.0)),
               (A.o_ustedes, dict(x=0.0, y=-190.0, z=220.0, guinada=3.0, cabeceo=-2.0, foco=1700.0)),
               (A.o_moriste, dict(x=200.0, y=-180.0, z=520.0, guinada=9.0, cabeceo=2.0, foco=900.0)),
               (A.o_volviste, dict(x=300.0, y=-170.0, z=700.0, guinada=10.0, cabeceo=6.0, foco=640.0)),
               (A.TR_SELECCION + 0.6, dict(x=320.0, y=-160.0, z=740.0, guinada=10.0, cabeceo=8.0, foco=600.0))]
FAROLES = [(-40.0, 1180.0, SANGRE, "I"), (150.0, 1180.0, PLAGA, "II"), (340.0, 1180.0, HIELO, "III")]
VACIA = (560.0, 1290.0)
PEG_USTEDES = [("Orgrimmar Grunt", -560.0, 1700.0, 360.0), ("Stormwind City Guard", -300.0, 2000.0, 375.0),
               ("Ironforge Mountaineer", 820.0, 1900.0, 285.0), ("Thrall", 1050.0, 2200.0, 380.0),
               ("Marshal Dughan", -800.0, 2300.0, 370.0)]
CORREOS = [("Correo", "", "lo que hicieron no tiene nombre", 0.0), ("Correo", "", "era un funeral, por favor", 0.8),
           ("Correo", "", "ojalá algún día lo entiendan", 1.6)]


def cementerio_final(t, modo):
    import decor_cem as DC
    kf = KF_CVIDEO if modo == "video" else KF_CPROMESA
    cam = C.camara(t, kf, L.CAM_A)
    mx, my = 650 - 0.25 * cam.C[0] - 900 * math.sin(math.radians(DC.cam_guinada(cam))), 170
    ax, ay, az = DC.ANGEL

    # FONDO cacheado por tick de HERVOR (GR.fondo): cielo, luna, nube, colina y, con la cámara quieta, el suelo
    def lejos(g, tt):
        cm = C.camara(tt, kf, L.CAM_A)
        hz_ = cm.horizonte()
        GR.cielo(g, tt, hz_ + 70, tono_alto=1.0, tono_bajo=0.56)
        mx_ = 650 - 0.25 * cm.C[0] - 900 * math.sin(math.radians(DC.cam_guinada(cm)))
        GR.luna(g, mx_, my, 74, tt, tono_cielo=0.86)
        G3.haz(g, mx_, my, 62, 22, 1100, tt, op=0.20)
        GR.nube(g, 1350 - 0.2 * cm.C[0], 120, 520, tt, sem=1, vel=5)
        GR.colina(g, GR.perfil_colina(-60, 1980, hz_ + 10, 26, sem=1), tono=0.26, tono2=0.4, ang=-3, per=5.0,
                  contorno=1.6, cruz=False)

    def tono_suelo(a, b, zc):
        base = 0.62 + 0.06 * np.clip(b / 3000.0, 0, 1)
        sendero = np.clip(1 - np.abs(a - L._camino(b)) / (70 + 0.03 * b), 0, 1) * (b < 1500)
        return base - 0.34 * sendero

    def suelo(g, tt):
        G3.plano(g, C.camara(tt, kf, L.CAM_A), (-5000, 0, -800), (1, 0, 0), (0, 0, 1), 10000, 6000, tono_suelo,
                 familias=((0.0, 14.0),), luces=[(ax, 0, az, 950, 0.95)], oscuro=0.2)

    def f_lejos(tt):
        cm = C.camara(tt, kf, L.CAM_A)
        return cm.horizonte(), 650 - 0.25 * cm.C[0] - 900 * math.sin(math.radians(DC.cam_guinada(cm))), 0.2 * cm.C[0]
    g = GR.fondo(t, "cem_" + modo, [(lejos, f_lejos), (suelo, lambda tt: G3.firma_cerca(C.camara(tt, kf, L.CAM_A)))])
    for i in range(3):                                     # los cuervos vuelan alto: nunca tapan la colina
        cx = (300 + 520 * i + t * (38 + 9 * i)) % 2300 - 150
        GR.cuervo(g, cx, 230 + 60 * i + 14 * math.sin(t * 0.8 + i), 0.75 - 0.15 * i, t, fase=i * 2.1)
    objs = []
    for i, (X, Z, fm, inc) in enumerate(DC.TUMBAS):
        objs.append((X, 0, Z, lambda c, o=(Z, "tumba", X, fm, inc, i): L._objeto_cementerio(c, cam, o, t)))
    objs.append((-560, 0, 1500, lambda c: L._objeto_cementerio(c, cam, (1500, "arbol", -560), t)))
    for i in range(46):
        Z = 450 + 2600 * rnd(i, 21) ** 1.3
        X = (rnd(i, 22) - 0.5) * 1.3 * Z
        if any(math.hypot(X - x, Z - z) < 160 for x, z in DC.LIBRE):
            continue
        objs.append((X, 0, Z, lambda c, o=(Z, "pasto", X, i): L._objeto_cementerio(c, cam, o, t)))
    objs.append((ax, 0, az, lambda c: L.angel(c, *cam.pt(ax, ay, az)[:2], 0.74 * cam.k(cam.pt(ax, ay, az)[2]), t, gloria=True)))
    luces = [(mx, my, 760, 0.55)]
    if modo == "video":
        # las almas del funeral llegan una detrás de otra, cada una con su vela
        for i in range(9):
            t0 = A.TR_CEM2 + 0.7 * i
            u = pr(t, t0, t0 + 6.0)
            if u <= 0:
                continue
            X = lerp(-1150 + 40 * i, ax - 200, smooth(u))
            Z = lerp(2100, az + 60, smooth(u))
            op = min(1.0, u * 4) * (1 - smooth(pr(u, 0.92, 1.0)))
            objs.append((X, -150, Z, lambda c, X=X, Z=Z, op=op, i=i: (
                GR.fantasma(c, *cam.pt(X, -150, Z)[:2], 0.5 * cam.k(cam.pt(X, -150, Z)[2]), t, fase=i, op=op, dirx=1,
                            color_estela=HIELO),
                F2.vela(c, *cam.pt(X + 40, -170, Z)[:2], 1.0 * cam.k(cam.pt(X, -150, Z)[2]), t, sem=i, op=op, color=HIELO))))
    else:
        # «fueron ustedes»: tras las tumbas se alzan los personajes de los jugadores (pegatinas REALES)
        al = smooth(pr(t, A.o_ustedes - 0.4, A.o_ustedes + 0.5)) * (1 - smooth(pr(t, A.o_moriste - 0.5, A.o_moriste + 0.3)))
        for j, (nom, X, Z, alto) in enumerate(PEG_USTEDES):
            if al > 0.01:
                C.peg(objs, cam, t, nom, X, Z, alto, alza=al, op=al, sem=1000 + j, espejo=X > 0)
        objs.append((VACIA[0], 0, VACIA[1], lambda c: DC._tumba_vacia(c, cam, A.g_tu + 2.0 + (t - A.o_prometido))))
        cierra = smooth(pr(t, A.o_cerraste - 0.1, A.o_volviste + 0.4))
        if cierra > 0.01:                                       # la losa se corre y cierra la fosa («cerraste el juego»)
            X, Z = VACIA
            dz = -150 + 120 * (1 - cierra) * 0
            losa = [(X - 110 + 260 * (1 - cierra), -6, Z - 160), (X + 110 + 260 * (1 - cierra), -6, Z - 160),
                    (X + 110 + 260 * (1 - cierra), -6, Z - 20), (X - 110 + 260 * (1 - cierra), -6, Z - 20)]
            objs.append((X, 0, Z - 90, lambda c, losa=losa: (lambda scr: scr is not None and c.figura(
                scr, 0.35, contorno=2.6, ang=0, per=4.4, cruz=False))(G3.proyectar(cam, losa)[0])))
    C.figuras(g, cam, objs)
    sx, sy, zc = cam.pt(ax, ay - 250, az)
    luces.append((sx, sy, 900 * cam.k(zc), 0.95))
    for i, (X, Z, col, num) in enumerate(FAROLES):            # los tres faroles de las tres noches
        if modo == "video":
            fz = 1.0 if i < 2 else 0.6
        else:
            fz = smooth(pr(t, (A.o_error, A.o_plaga, A.o_funeral)[i] - 0.2, (A.o_error, A.o_plaga, A.o_funeral)[i] + 0.3))
            fz *= 1 + 0.4 * smooth(pr(t, A.o_dios, A.o_ustedes))
        fx, fy, k = F.farol(g, cam, X, Z, t, col, fz, sem=i, alto=1.0)
        b = cam.pt(X, 0, Z)
        g.texto(num, b[0], b[1] + 26 * k, max(12, int(30 * k)), TINTA, "gara_b", 0.9)
        if fz > 0.02:
            luces.append((fx, fy, 340 * k * fz, 0.6 * fz, col))
    if modo == "video":
        # el video del funeral, colgado en el cielo, con los correos furiosos; luego se multiplica (viral)
        op = C.env(t, A.v_subieron - 0.3, A.TR_PLAZA - 0.3, 0.5, 0.4)
        C.recuerdo_colgado(g, cam, (ax + 560, -620.0 + 8 * math.sin(t), az + 300), (0.92, 0, -0.38), "_crudos/MEpv7YxnLCQ",
                           300.0 + (t - A.v_subieron) * 0.8, t, ancho=560, alto=360, texto="Serenity Now · MMVI", op=op,
                           z=1.25, cx=0.48, cy=0.45, tinta=0.25, sem=64)
        op2 = C.env(t, A.v_correos - 0.3, A.v_famosos, 0.4, 0.6)
        if op2 > 0.01:
            s = G(t, 820, 230, alfa=True)
            GR.chat(s, 20, 220, [(c_, a_, x_, A.v_correos + d_) for c_, a_, x_, d_ in CORREOS], t, corr=0.25, ancho=780,
                    px=30, sem=9, color_canal=SANGRE)
            _colgar(g, cam, s, (ax - 520, -480.0 + 6 * math.sin(t), az + 100), 600, t, op=op2, techo=-1500,
                    U=(0.92, 0, 0.38), sombra=0.35)
        viral = smooth(pr(t, A.v_videos - 0.3, A.v_famosos + 0.4)) * (1 - smooth(pr(t, A.TR_PLAZA - 0.6, A.TR_PLAZA - 0.2)))
        for j, (dx, dy, dz) in enumerate(((-900, -100, 700), (700, -200, 600), (-1300, -420, 1300), (1250, -480, 1200))):
            if viral > 0.01 and viral * 4 > j:
                C.recuerdo_colgado(g, cam, (ax + dx, -600.0 + dy + 8 * math.sin(t + j), az + dz), (1, 0, 0), "_crudos/MEpv7YxnLCQ",
                                   310.0 + 3 * j + (t - A.v_videos) * 0.8, t, ancho=380, alto=250, op=min(1.0, viral * 4 - j),
                                   z=1.25, cx=0.48, cy=0.45, tinta=0.3, sem=65 + j)
    G3.iluminar(g, luces, amb=0.16, fuerza=0.58, acento=0.10)
    G3.particulas(g, t, "polvo", 70, (sx - 600, sy - 400, sx + 600, sy + 500), sem=2)
    for zmin in (2000, 1000, 420):
        y_nb = cam.pt(cam.C[0], 0, cam.C[2] + zmin)[1]
        GR.niebla(g, y_nb - 40, y_nb + 12, t, op=0.4, sem=int(zmin), vel=22)
    with G3.capa_prof(g, cam, 230) as c:
        x0, z0 = cam.C[0], cam.C[2]
        for i in range(9):
            px, py, zc = cam.pt(x0 - 330 + 80 * i, 0, z0 + 300 + 60 * rnd(i, 5))
            GR.pasto(c, px, py, 0.9 * cam.k(zc), t, n=8, sem=i)
        px, py, zc = cam.pt(x0 - 215, 0, z0 + 340)
        GR.lapida(c, px, py, 0.95 * cam.k(zc), "arco", 7, tono=0.8, tono2=0.97, sem=31)
    return g


# ====================================================================== 4. LA PLAZA DEL MEMORIAL (video, frase 3)
CAM_P = dict(x=0.0, y=-240.0, z=0.0, guinada=0.0, cabeceo=-3.0, f=1450.0, foco=1500.0, apertura=4.0, bruma=0.4,
             lejos=3000.0)
KF_PLAZA = [(A.TR_PLAZA - 0.6, dict(x=-60.0, y=-250.0, z=-60.0, guinada=-3.0, cabeceo=-4.0)),
            (A.TR_CEM3 + 0.6, dict(x=40.0, y=-260.0, z=120.0, guinada=3.0, cabeceo=-5.0))]


def plaza(t):
    cam = C.camara(t, KF_PLAZA, CAM_P)
    g = G(t)
    hz = cam.horizonte()
    GR.cielo(g, t, hz + 40, tono_alto=0.95, tono_bajo=0.55, estrellas=40)
    luces = [(0, -300, 1700, 900, 0.7)]
    G3.plano(g, cam, (-1400, -1300, 2600), (1, 0, 0), (0, 1, 0), 2800, 1300, 0.3, familias=((0.0, 15.0),),
             patron=("sillares", 230, 105), var=0.06, luces=luces, oscuro=0.35)                  # fachada de la catedral
    for dx in (-700, 0, 700):                                  # vitrales ojivales
        ven = [(dx - 120, -300, 2598), (dx + 120, -300, 2598), (dx + 120, -900, 2598), (dx, -1080, 2598), (dx - 120, -900, 2598)]
        scr, _ = G3.proyectar(cam, ven)
        if scr is not None:
            g.figura(scr, 0.8, contorno=2.6, ang=0, per=4, cruz=False)
            g.acento(scr, ORO, 0.7)
    G3.plano(g, cam, (-3000, 0, -400), (1, 0, 0), (0, 0, 1), 6000, 3000, 0.45, familias=((0.0, 16.0),), patron=("losas", 160),
             luces=luces, oscuro=0.25)
    objs = []
    X0, Z0 = 0.0, 1700.0                                      # el memorial: una piedra con velas y flores, en círculo
    objs.append((X0, 0, Z0, lambda c: (
        G3.plano(c, cam, (X0 - 90, -260, Z0), (1, 0, 0), (0, 1, 0), 180, 260, 0.25, familias=((0.0, 9.0),), contorno=2.4),
        c.texto("†", *cam.pt(X0, -170, Z0 - 2)[:2], max(12, int(60 * cam.k(cam.pt(X0, 0, Z0)[2]))), TINTA, "gara_b", 0.9))))
    for i in range(14):
        a = i / 14 * 6.2832
        X, Z = X0 + 260 * math.cos(a), Z0 - 60 + 140 * math.sin(a)
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, i=i: F2.vela(c, *cam.pt(X, 0, Z)[:2], 1.3 * cam.k(cam.pt(X, 0, Z)[2]), t,
                                                               sem=i)))
    for j in range(7):                                         # dolientes en paz, de pie y arrodillados
        a = -0.4 - j * 0.38
        X, Z = X0 + 620 * math.cos(a), Z0 + 140 + 300 * abs(math.sin(a))
        if j in (1, 4):
            C.peg(objs, cam, t, ("Brother Paxton", "Innkeeper Farley")[j // 4], X, Z, 365.0, sem=1100 + j, espejo=X > 0)
            continue
        objs.append((X, 0, Z, lambda c, X=X, Z=Z, j=j: (
            F.persona(c, *cam.pt(X, 0, Z)[:2], 0.95 * cam.k(cam.pt(X, 0, Z)[2]), t, ("capa", "enano", "sanador", "mercader")[j % 4],
                      anda=0.0, dirx=1 if X < X0 else -1, sem=1110 + j, brazos=(0.3, 1.5), arma=False),
            F2.vela(c, *cam.pt(X + 30, -230, Z - 20)[:2], 1.3 * cam.k(cam.pt(X, 0, Z)[2]), t, sem=j + 20))))
    for sg in (-1, 1):                                          # la guardia de la ciudad: aquí nadie te ataca
        C.peg(objs, cam, t, "Stormwind City Guard", sg * 900, 2100.0, 375.0, sem=1120 + (sg > 0), espejo=sg > 0)
    C.figuras(g, cam, objs)
    G3.iluminar(g, [(*cam.pt(X0, -200, Z0)[:2], 700, 0.75, ORO)], amb=0.2, fuerza=0.6, acento=0.12)
    G3.particulas(g, t, "polvo", 50, (300, 200, 1600, 1000), sem=120, color=ORO)
    return g


# ====================================================================== 5. LA PANTALLA DE SELECCIÓN (promesa 3-4, cierre)
CAM_S = dict(x=0.0, y=-260.0, z=0.0, guinada=0.0, cabeceo=-2.0, f=1450.0, foco=1100.0, apertura=5.0, bruma=0.3,
             lejos=2600.0)
KF_SEL = [(A.TR_SELECCION - 0.3, dict(x=0.0, y=-300.0, z=200.0, guinada=0.0, cabeceo=-3.0, foco=950.0)),
          (A.o_ropa, dict(x=0.0, y=-280.0, z=420.0, guinada=0.0, cabeceo=-4.0, foco=720.0)),
          (A.o_nada, dict(x=10.0, y=-310.0, z=560.0, guinada=0.0, cabeceo=-8.0, foco=600.0)),
          (A.o_sabe, dict(x=0.0, y=-320.0, z=380.0, guinada=0.0, cabeceo=-6.0, foco=780.0)),
          (A.T_APAGON4, dict(x=0.0, y=-420.0, z=-300.0, guinada=0.0, cabeceo=-2.0, foco=1450.0))]
KF_CIERRE = [(A.T_CIERRE - 0.3, dict(x=0.0, y=-300.0, z=460.0, guinada=0.0, cabeceo=-5.0, foco=700.0)),
             (A.T_NEGRO, dict(x=0.0, y=-310.0, z=560.0, guinada=0.0, cabeceo=-7.0, foco=600.0))]
PEDESTAL = (0.0, 1150.0, 330.0)
PERSONAJE = "Auctioneer Jaxon"


def _seleccion(t, cam, cierre=False):
    g = G(t)
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.9, ang=0, per=5.2, cruz=False)
    X, Z, R = PEDESTAL
    for j, (r, h) in enumerate(((R * 1.25, 40), (R, 80))):     # el pedestal de piedra en dos gradas
        aro = [(X + r * math.cos(a), -h, Z + r * 0.55 * math.sin(a)) for a in np.linspace(0, 6.2832, 48)]
        scr, _ = G3.proyectar(cam, aro)
        if scr is not None:
            g.figura(scr, 0.25 + 0.15 * j, contorno=2.4, ang=0, per=4.4, cruz=False)
    sx, sy, zc = cam.pt(X, -900, Z)
    G3.haz(g, sx, sy - 400, 90, 26, 1300, t, op=0.3)            # el foco de luz desde arriba
    objs = []
    C.peg(objs, cam, t, PERSONAJE, X, Z, 370.0, Y=-80.0, sem=1200, aleteo=0.4, espejo=cierre and t > A.q_cuanto)
    for i in range(10):                                          # pinos nevados del fondo de la pantalla (como la de Dun Morogh)
        Xp = (rnd(i, 131) - 0.5) * 2600
        Zp = 1900 + 900 * rnd(i, 132)
        objs.append((Xp, 0, Zp, lambda c, Xp=Xp, Zp=Zp, i=i: F.pino(c, *cam.pt(Xp, 0, Zp)[:2], 0.9 * cam.k(cam.pt(Xp, 0, Zp)[2]),
                                                                     t, sem=i + 60)))
    C.figuras(g, cam, objs)
    ropa = C.env(t, A.o_ropa - 0.2, A.o_nada + 0.4, 0.3, 0.6)
    if ropa > 0.01:
        px, py, zc = cam.pt(X, -280, Z)
        g.acento_luz(px, py, 220 * cam.k(zc), ORO, 0.6 * ropa)
    if not cierre:
        op = C.env(t, A.o_pantalla - 0.4, A.o_sabe, 0.5, 0.6)
        C.recuerdo_colgado(g, cam, (560.0, -500.0 + 6 * math.sin(t), 1600.0), (0.92, 0, -0.38), "_crudos/NFYgy_J7qVE",
                           20.0 + (t - A.o_pantalla) * 0.5, t, ancho=440, alto=300, texto="Selección de personaje", op=op,
                           z=1.8, cx=0.42, cy=0.45, tinta=0.25, sem=66)
    boton = 1.0 if cierre else smooth(pr(t, A.o_pantalla, A.o_pantalla + 0.6))
    _cartel(g, cam, (X + 430, -170.0, Z - 260), "Entrar al mundo", t, op=boton, ancho=440, alto=100, px=36)
    if cierre:
        lat = 0.5 + 0.5 * math.sin(t * 3)
        px, py, zc = cam.pt(X + 430, -170, Z - 260)
        g.acento_luz(px, py, 260 * cam.k(zc), ORO, 0.4 + 0.3 * lat)
    G3.iluminar(g, [(sx, sy + 300, 600, 0.7)], amb=0.1, fuerza=0.7, acento=0.12)
    G3.particulas(g, t, "polvo", 60, (sx - 500, sy - 200, sx + 500, sy + 900), sem=130)
    return g


def seleccion(t):
    return _seleccion(t, C.camara(t, KF_SEL, CAM_S))


def cierre(t):
    return _seleccion(t, C.camara(t, KF_CIERRE, CAM_S), cierre=True)


def susto4(t):
    """EL SUSTO FINAL (8:42): el rostro del Ángel de la Resurrección bajo la capucha, a un palmo, abre los ojos de golpe
    y te mira. Dibujado a tamaño de pantalla (escalar la figura entera engorda las líneas: parece caricatura)."""
    g = G(t)
    g.trama([(-20, -20), (1940, -20), (1940, 1100), (-20, 1100)], 0.95, ang=0, per=4.6, cruz=False)
    u = t - A.T_SUSTO4
    s = 1.0 + 0.12 * e_out(min(1.0, u / 0.6))
    cx, cy = 960, 560
    R = 760 * s                                              # la gloria de rayos detrás
    g.papel(circ_pts(cx, cy - 60, R, 90), 1.0)
    g.trama(circ_pts(cx, cy - 60, R, 90), lambda X, Y: np.clip(0.2 + 0.7 * (np.sqrt((X - cx) ** 2 + (Y - cy + 60) ** 2) / R) ** 2,
                                                               0, 1), modo="rayos", centro=(cx, cy - 60), n=220, cruz=False)
    g.acento_luz(cx, cy - 60, R * 1.1, ESPECTRO, 0.8, 1.2)
    cap = GR.catmull(np.float32([(cx, cy - 560 * s), (cx + 330 * s, cy - 430 * s), (cx + 470 * s, cy - 60 * s),
                                 (cx + 520 * s, cy + 560 * s), (cx - 520 * s, cy + 560 * s), (cx - 470 * s, cy - 60 * s),
                                 (cx - 330 * s, cy - 430 * s)]), 5, True)
    g.figura(cap, 0.55, contorno=3.0, tono2=0.92, luz=0, ang=70, per=4.4, modo="contorno", borde=0.3, rb=26)
    cara = circ_pts(cx, cy + 40 * s, 250 * s, 64, 320 * s)
    g.figura(cara, 0.05, contorno=2.4, tono2=0.62, luz=-90, ang=0, per=3.8, cruz=False)
    # la capucha le hunde la frente en sombra (degradado de trama, no una mancha) y las mejillas se vacían
    g.trama(cara, lambda X, Y: np.clip((cy - 40 * s - Y) / (260 * s), 0, 0.92), ang=0, per=3.6, cruz=False)
    for sg in (-1, 1):
        g.trama(tr_(circ_pts(0, 0, 34 * s, 32, 150 * s), cx + sg * 165 * s, cy + 150 * s, -0.25 * sg), 0.42, ang=80 * sg,
                per=3.4, cruz=False)
    ab = smooth(min(1.0, u / 0.08))
    for sg in (-1, 1):
        ex, ey = cx + sg * 105 * s, cy - 20 * s
        g.trazo(GR.catmull(np.float32([(ex - 78 * s, ey + 26 * s), (ex, ey + 52 * s), (ex + 78 * s, ey + 26 * s)]), 5), 7 * s,
                op=0.75, afilado=0.6)                         # ojeras
        ojo = GR.catmull(np.float32([(ex - 82 * s, ey), (ex, ey - 44 * s * ab - 3), (ex + 82 * s, ey), (ex, ey + 38 * s * ab + 3)]),
                         5, True)
        g.figura(ojo, 0.0, contorno=3.0)
        if ab > 0.2:
            g.acento_luz(ex, ey, 220 * s, ESPECTRO, 1.0, 1.0)
            g.figura(circ_pts(ex, ey, 17 * s, 24), 0.4, contorno=2.0, ang=0, per=3.0, modo="rayos", centro=(ex, ey), cruz=False)
            g.circ(ex, ey, 4.5 * s, TINTA, 1.0)                # pupilas diminutas: no parpadea
            g.acento(ojo, ESPECTRO, 0.55)
        g.trazo([(ex - 90 * s, ey - 70 * s), (ex - 10 * s * sg, ey - 92 * s), (ex + 80 * s, ey - 66 * s)], 4.0)   # cejas
    g.trazo([(cx, cy + 10 * s), (cx - 16 * s, cy + 120 * s), (cx + 12 * s, cy + 130 * s)], 2.6)
    boca = circ_pts(cx, cy + 225 * s, 30 * s, 24, (10 + 52 * ab) * s)      # la boca se abre, larga
    g.figura(boca, 0.95, contorno=2.4, ang=0, per=3.0, cruz=False)
    G3.particulas(g, t, "polvo", 80, (0, 0, 1920, 1080), sem=140, color=ESPECTRO)
    return g
