# -*- coding: utf-8 -*-
"""REPASO EXPRÉS + CIERRE.
repaso: tres columnas MATERIA / ATMÓSFERA / DEFENSA; cada idea entra como tarjetita cuando la voz la dice y la que se está diciendo
brilla en amarillo (con su dibujito: jeringa, Tierra, gato-mono-león, Y del anticuerpo, balón del autogol).
cierre: ¡LOGRO DESBLOQUEADO! con trofeo y las 6 fotos de su cuaderno en abanico → REPÁSENLO ANTES DE DORMIR (cama, luna, zzz) y
DORMIR BIEN CUIDA SU DEFENSA (escudo) → ¡ÉCHENLE GANAS! ¡YO SÉ QUE PUEDEN! → ¡MUCHO ÉXITO, SEXTO B! con corazones y confeti."""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import titulo
from fondos_amaya import papel
from iconos_ia import palomita, trofeo
from personajes import AMARILLO, corazon, destello
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, letrero, papa, tarjeta
from piezas_es import ROSA_M, polaroid
from piezas_fj import base, cama, luna, zzz
from piezas_ci import anticuerpo, balon, celula, tierra
from plano_e import escudo

T_INI = T0("repaso")
RP, CI = "repaso", "cierre"
tRep = ww(RP, 0, "repaso")
COLS = [("MATERIA", ROJO, ww(RP, 0, "materia"), [("OCUPA LUGAR Y TIENE MASA", ww(RP, 0, "ocupa")),
                                                  ("GAS: SIN FORMA NI VOLUMEN", ww(RP, 0, "gas")),
                                                  ("POR ESO VA EN UN RECIPIENTE", ww(RP, 0, "eso")),
                                                  ("JERINGA: EL AIRE OCUPA LUGAR", ww(RP, 0, "jeringa"))]),
        ("ATMÓSFERA", AZUL, ww(RP, 1, "atmosfera"), [("CAPA DE GASES", ww(RP, 1, "capa")),
                                                     ("SE QUEDA POR LA GRAVEDAD", ww(RP, 1, "queda")),
                                                     ("78 % NITRÓGENO", ww(RP, 1, "setenta")),
                                                     ("CASI 21 % OXÍGENO", ww(RP, 1, "casi"))]),
        ("DEFENSA", VERDE, ww(RP, 2, "defensa"), [("1.ª BARRERA: INMUNIDAD INNATA", ww(RP, 2, "primera")),
                                                  ("LEUCOCITOS: GATOS, MONOS, LEONES", ww(RP, 2, "leucocitos")),
                                                  ("ANTÍGENO = AJENO", ww(RP, 2, "antigeno")),
                                                  ("ANTICUERPO: LO HACE TU CUERPO", ww(RP, 2, "anticuerpo")),
                                                  ("VACUNA = PARTIDO DE PRÁCTICA", ww(RP, 2, "vacuna")),
                                                  ("AUTOINMUNE = AUTOGOL", ww(RP, 2, "autoinmune"))])]
XS = (300, 760, 1220)
T_CI = T0(CI)
tSexto, tLogro, tTodo, tCuad = ww(CI, 0, "sexto"), ww(CI, 0, "logro"), ww(CI, 0, "todo"), ww(CI, 0, "cuaderno")
T_CI2 = ww(CI, 0, "repasenlo") - 0.3
tAntes, tDormir2, tCuida = ww(CI, 0, "antes"), ww(CI, 0, "dormir", 1), ww(CI, 0, "cuida")
T_CI3 = ww(CI, 1, "echenle") - 0.3
tGanas, tYo, tPueden, tMucho, tSextoB = ww(CI, 1, "ganas"), ww(CI, 1, "yo"), ww(CI, 1, "pueden"), ww(CI, 1, "mucho"), ww(CI, 1, "sexto")
FOTOS = ["materia", "aire", "atmosfera", "jeringa", "inmune1", "inmune2"]


def _todos():
    """Lista plana (t, col, k, texto) para saber cuál se está diciendo."""
    out = []
    for c, (_, _, _, items) in enumerate(COLS):
        for k, (txt, tk) in enumerate(items):
            out.append((tk, c, k, txt))
    return sorted(out)


TODOS = _todos()


def _dos(txt):
    """Parte el texto en dos renglones (después de «:» o antes de «=», o en el espacio más cercano a la mitad)."""
    if len(txt) <= 16:
        return [txt]
    for sep in (": ", " = "):
        if sep in txt:
            a, b = txt.split(sep, 1)
            return [a + sep.rstrip() if sep == ": " else a, b if sep == ": " else "= " + b]
    sp = [i for i, ch in enumerate(txt) if ch == " "]
    i = min(sp, key=lambda i: abs(i - len(txt) / 2))
    return [txt[:i], txt[i + 1:]]


def rayo(im, x, y, s, t, seed):
    pts = np.array([(x + 10 * s, y - 60 * s), (x - 30 * s, y + 8 * s), (x - 2 * s, y + 8 * s), (x - 14 * s, y + 62 * s),
                    (x + 32 * s, y - 10 * s), (x + 4 * s, y - 10 * s)], np.float32)
    forma(im, pts, AMARILLO, t, seed, tinta=4 * s)


def repaso(t):
    im = cache("h_rep", lambda: papel("calido")).copy()
    titulo(im, "REPASO EXPRÉS", t, tRep, 29000, col=MORADO, x=760, y=80, px=74)
    if t > tRep - 0.3:
        e = entra(t, tRep - 0.3)
        rayo(im, 440, 80, 1.1 * e, t, 29005)
        rayo(im, 1080, 80, 1.1 * e, t, 29006)
        if t < COLS[0][2]:
            for c, (nom, col, _, _) in enumerate(COLS):
                letrero(im, nom, XS[c], 500, 56, t, col=col, txt=CREMA, seed=29007 + c, esc=entra(t, tRep + 0.3 + 0.3 * c), rot=(c - 1) * 0.04)
    activo = None
    for j, (tk, c, k, _) in enumerate(TODOS):
        if t >= tk - 0.2:
            activo = (c, k)
    for c, ((nom, col, tc, items), x) in enumerate(zip(COLS, XS)):
        if t <= tc - 0.3:
            continue
        e = entra(t, tc - 0.3)
        letrero(im, nom, x, 190, 50, t, col=col, txt=CREMA, seed=29010 + c * 50, esc=e, rot=(c - 1) * 0.03)
        for k, (txt, tk) in enumerate(items):
            if t <= tk - 0.3:
                continue
            ek = entra(t, tk - 0.3)
            y = 300 + 128 * k
            on = activo == (c, k)
            fondo = AMARILLO if on else CREMA
            b = 1.06 if on else 1.0
            rt = ((k + c) % 2 - 0.5) * 0.03
            tarjeta(im, x, y, 440 * ek * b, 116 * ek * b, t, fondo, 29020 + c * 50 + k * 5, rot=rt)
            lns = _dos(txt)
            px = min(36.0, 400 / (0.56 * max(len(l) for l in lns) + 0.5))
            for j, ln in enumerate(lns):
                dy = (j - (len(lns) - 1) / 2) * px * 1.15
                rotulo(im, ln, x, y + 3 + dy, px * ek * b + 1, col * 0.75, t, seed=29021 + c * 50 + k * 5 + j * 100, tinta=False, rot=rt)
            if ek > 0.9 and t > tk + 0.4:
                palomita(im, x + 205, y - 40, 0.35, t, seed=29023 + c * 50 + k * 5, col=VERDE)
    # dibujito del que se está diciendo, abajo
    if activo is not None:
        c, k = activo
        tk = COLS[c][3][k][1]
        e = entra(t, tk - 0.2)
        x, y = 760, 960
        if c == 1:
            tierra(im, x, y - 10, 70 * e + 1, t, seed=29200, atm=1.0)
        elif (c, k) == (2, 1):
            for j, tp in enumerate(("gato", "mono", "leon")):
                celula(im, x - 170 + 170 * j, y, 0.5 * e, t, seed=29210 + j * 20, tipo=tp, granos=1.0 if j == 0 else 0)
        elif (c, k) == (2, 3):
            anticuerpo(im, x, y, 1.0 * e, t, seed=29280, rot=0.2 * math.sin(t * 3))
        elif (c, k) == (2, 5):
            balon(im, x + 60 * math.sin(t * 2), y, 40 * e + 1, t, seed=29290, gira=t * 4)
        elif c == 2 and k == 0:
            escudo(im, x, y, 0.5 * e, t, 29295)
    return im


# ------------------------------------------------------------ cierre
def cierre1(t):
    im = cache("h_c1", lambda: papel("rosa")).copy()
    if t > tSexto - 0.3:
        rotulo(im, "SEXTO B:", 760, 110, 70, MORADO, t, seed=29300, esc=entra(t, tSexto - 0.3))
    if t > tLogro - 0.3:
        e = entra(t, tLogro - 0.3)
        brillo(im, 760, 260, 360, rgb("fff3a0"), 0.4 * e)
        forma(im, rrect(760, 240, 900 * e + 1, 120 * e + 1, 24, -0.02), rgb("3a3a5a"), t, 29305, tinta=5)
        rotulo(im, "¡LOGRO DESBLOQUEADO!", 820, 244, 58 * e + 1, AMARILLO, t, seed=29306, rot=-0.02)
        trofeo(im, 400, 260, 0.55 * e, t, seed=29310)
        chispas(im, 760, 240, 420, t, tLogro, seed=29315, col=AMARILLO, n=12)
    for k, nom in enumerate(FOTOS):
        tk = tTodo - 0.3 + 0.15 * k
        if t <= tk:
            continue
        a = (k - 2.5) * 0.12
        polaroid(im, nom, 760 + (k - 2.5) * 200, 600 + 30 * abs(k - 2.5), entra(t, tk), t, rot=a, seed=29320 + k * 10, alto=170,
                 cinta=False)
    if t > tCuad - 0.3:
        letrero(im, "¡TODO SU CUADERNO DE CIENCIAS!", 760, 880, 50, t, col=VERDE, txt=CREMA, seed=29390, esc=entra(t, tCuad - 0.3),
                rot=0.02)
    return im


def _noche():
    im = np.zeros((H, W, 3), np.float32)
    from acuarela import degradado
    degradado(im, rgb("3a3f78"), rgb("23264a"))
    rg = np.random.default_rng(9)
    for k in range(60):
        x, y, r = rg.uniform(0, W), rg.uniform(0, 600), rg.uniform(1.5, 3.5)
        forma(im, elipse(x, y, r, r), rgb("fbf3df"), 0, 29400 + k, tinta=0)
    return im


def cierre2(t):
    im = cache("h_c2", _noche).copy()
    luna(im, 1300, 190, 80, t, seed=29470)
    cama(im, 620, 700, 1.0, t, seed=29480)
    # el cuaderno abierto sobre la almohada
    forma(im, rrect(420, 600, 150, 100, 8, -0.15), CREMA, t, 29490, tinta=3)
    linea(im, [(420, 555), (420, 645)], 3, GRIS, seed=29491, t=t)
    rotulo(im, "CIENCIAS", 420, 600, 22, AZUL, t, seed=29492, tinta=False, rot=-0.15)
    zzz(im, 760, 520, t, s=1.3, seed=29495)
    if t > tAntes - 0.5:
        letrero(im, "REPÁSENLO ANTES DE DORMIR", 760, 120, 56, t, col=CREMA, txt=MORADO, seed=29500, esc=entra(t, tAntes - 0.5),
                rot=-0.02)
    if t > tCuida - 0.6:
        e = entra(t, tCuida - 0.6)
        escudo(im, 1250, 600, 0.7 * e, t, 29510, col=VERDE)
        brillo(im, 1250, 600, 180, rgb("fff3a0"), 0.3 * e)
        letrero(im, "DORMIR BIEN CUIDA SU DEFENSA", 760, 920, 48, t, col=VERDE, txt=CREMA, seed=29515, esc=e, rot=0.02)
    return im


def cierre3(t):
    im = cache("h_c3", lambda: papel("calido")).copy()
    # confeti que cae
    rg = np.random.default_rng(29600)
    cols = [ROJO, AZUL, VERDE, AMARILLO, MORADO, ROSA_M]
    for k in range(80):
        x0, v, f = rg.uniform(0, W), rg.uniform(120, 260), rg.uniform(0, 1200)
        y = (f + v * (t - T_CI3)) % 1250 - 80
        x = x0 + 30 * math.sin(t * 2 + k)
        forma(im, rrect(x, y, 34, 18, 4, t * 3 + k), cols[k % 6], t, 29601 + k, tinta=0, alfa=0.85)
    if t > tGanas - 0.5:
        rotulo(im, "¡ÉCHENLE GANAS!", 760, 200, 100, ROJO, t, seed=29700, esc=entra(t, tGanas - 0.5), rot=-0.04)
    if t > tYo - 0.3:
        rotulo(im, "¡YO SÉ QUE PUEDEN!", 760, 360, 70, MORADO, t, seed=29705, esc=entra(t, tYo - 0.3), rot=0.03)
    if t > tMucho - 0.3:
        e = entra(t, tMucho - 0.3)
        forma(im, rrect(760, 620, 1180 * e + 1, 200 * e + 1, 30, -0.02), VERDE, t, 29710, tinta=6)
        rotulo(im, "¡MUCHO ÉXITO EN SU EXAMEN,", 760, 580, 56 * e + 1, CREMA, t, seed=29711, rot=-0.02)
        if t > tSextoB - 0.3:
            rotulo(im, "SEXTO B!", 760, 670, 76 * entra(t, tSextoB - 0.3) + 1, AMARILLO, t, seed=29712, rot=-0.02)
        for j in range(6):
            a = j * math.pi / 3 + t * 0.6
            corazon(im, 760 + 640 * math.cos(a) * 0.95, 620 + 250 * math.sin(a), (1.4 + 0.2 * math.sin(t * 5 + j)) * e, t,
                    seed=29720 + j, col=[ROJO, ROSA_M][j % 2])
        chispas(im, 760, 620, 520, t, tSextoB, seed=29740, col=AMARILLO, n=14)
    return im


TRAMOS = [(T_INI, repaso), (T_CI, cierre1), (T_CI2, cierre2), (T_CI3, cierre3)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
