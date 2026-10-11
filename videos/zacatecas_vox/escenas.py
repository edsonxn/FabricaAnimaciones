# -*- coding: utf-8 -*-
"""Zacatecas, 1546-1600 — PLANO SECUENCIA vertical estilo Vox (sin cortes).

Las "escenas" del guion solo marcan narración y música: todas usan la clase Mundo, que dibuja un único mundo
continuo en función del tiempo global t. Una cámara recorre: mapa de la Nueva España -> zoom a Zacatecas -> cerro
y campamento -> caída por el pozo de la mina -> subida al patio de beneficio -> camino de la plata y guerra
chichimeca -> la aldea se vuelve ciudad -> ruta de la plata hasta Sevilla -> regreso a la mina y a la ciudad de hoy.
Personajes dibujados CUADRO A CUADRO (ciclos de poses en vox.py), a 15 dibujos por segundo.
"""
import math

import numpy as np

import cap_camino as CC
import cap_cerro as CE
import cap_ciudad as CD
import cap_cierre as CZ
import cap_local as CL
import cap_mapa as CM
import cap_mina as CMI
import cap_patio as CP
import cap_plata as CPL
import geo as G
import locales as L
import ui_caps as UC
import ui_vox as U
import vox as V
import fondos as F
from cap_local import SUR
from ctx import LOC, TOTAL, Camara, Anios, KL, KM, T, INI, FIN, lerp_color
from escena_base import Escena, TL
from motor import W, H, mat_t, mat_s, mat_r, prog, clamp01, smooth, e_inout, e_out, e_back, lerp, rect_red

# ------------------------------------------------------------------ anclas de fase
A_C, A_CM, A_M, A_P, A_CA, A_CD, A_PL, A_Z = CL.A, CL.A, CMI.A, CP.A, CC.A, CD.A, CPL.A, CZ.A
T_DIVE0 = CM.A["chichi"] + 0.5
T_LLEGADA = T_DIVE0 + 3.4
X_PAZ_ = CC.X_PAZ
ZX, ZY = G.xy(*G.CIUDADES["zacatecas"])
MEX = G.xy(*G.CIUDADES["mexico"])
VER = G.xy(*G.CIUDADES["veracruz"])
SEV = CPL.SEV

# ------------------------------------------------------------------ cámara
CAM_A = Camara([   # del mapa hasta el inicio de la mina
    KM(0.0, 20, -50, 0.58),
    KM(CM.A["seis"], 20, -50, 0.6),
    KM(T_DIVE0, 4, -30, 0.7),
    KL(T_LLEGADA, -200, -240, 1.0),
    KL(A_C["tolosa"] + 0.5, -250, 10, 2.5),
    KL(A_C["llega"] + 0.6, -240, 10, 2.4),
    KL(A_C["odre"] - 0.2, 330, -330, 1.0),
    KL(A_C["bufa"] + 0.4, 560, -380, 0.85),
    KL(A_C["arma"] + 0.9, 520, -60, 1.5),
    KL(A_C["veta"] - 0.1, 740, -245, 1.3),
    KL(A_C["fiebre"] + 0.5, 500, -100, 0.9),
    KL(INI("campamento") + 0.5, 200, -140, 0.95),
    KL(A_CM["casas"] + 0.3, 130, -50, 1.3),
    KL(A_CM["laderas"] + 0.3, 380, -100, 1.2),
    KL(A_CM["caro"] + 0.3, 300, -40, 1.3),
    KL(A_CM["ranch"] + 0.5, 520, -40, 1.15),
    KL(A_CM["t34"] - 0.5, 100, -180, 0.45),
    KL(A_CM["hosp"] + 0.8, 100, -180, 0.45),
    KL(A_M["ini"] - 0.1, -40, SUR + 60, 1.5),
], respira=0.0)
CAM_B = Camara([   # patio, camino, mapa de vuelta, ciudad, ruta de la plata, cierre
    KL(A_M["fin"] - 0.2, -40, -20, 1.5),
    KL(A_P["ini"] + 2.6, -830, -140, 1.15),
    KL(A_P["mulas"] - 0.6, -830, -120, 1.25),
    KL(A_P["atrapa"] - 0.4, -830, -60, 1.5),
    KL(A_P["atrapa"] + 1.5, -830, -30, 2.6),
    KL(A_P["pobre"] + 0.4, -700, -60, 1.2),
    KL(A_P["espana"] + 0.3, -540, -100, 1.0),
    KL(A_CA["ini"] + 0.6, -300, -150, 1.4),
    KL(A_CA["camino"] + 0.4, 250, -150, 1.4),
    KL(A_CA["atacan"] - 0.4, 820, -330, 0.85),
    KL(A_CA["atacan"] + 0.9, 800, -470, 1.3),
    KL(A_CA["tierras"], 900, -260, 0.95),
    KL(A_CA["conflicto"] + 2.0, 900, -260, 0.95),
    KL(A_CA["presidios"] + 0.2, 1500, -200, 1.0),
    KL(A_CA["escolta"] + 1.0, 1800, -150, 1.4),
    KL(A_CA["basta"] + 0.4, 2000, -140, 1.4),
    KL(A_CA["n90"] + 0.8, X_PAZ_ + 20, -120, 1.5),
    KL(A_CA["paz"] + 0.6, X_PAZ_ + 60, -110, 1.6),
    KL(A_CA["fin"] - 0.5, X_PAZ_ + 60, -110, 1.6),
    KM(A_CA["fin"] + 0.7, 4, -40, 1.6),            # sale al mapa ...
    KL(A_CD["ciudad0"] + 0.8, 20, -100, 1.0),       # ... y vuelve a Zacatecas (ya ciudad)
    KL(A_CD["convento"] + 0.2, 60, -100, 1.5),
    KL(A_CD["o85"] + 0.5, 30, -100, 1.0),
    KL(A_CD["mercados"] + 0.1, 0, -80, 1.15),
    KL(A_CD["fin"] + 0.3, 0, -80, 1.15),
    KM(A_PL["ini"] + 2.2, 2680, -380, 0.165),
    KM(A_PL["lejos"] - 0.6, 2680, -380, 0.165),
    KM(A_PL["monedas"] - 0.2, SEV[0] - 300, SEV[1] - 100, 0.30),
    KM(A_Z["ini"] - 0.4, SEV[0] - 300, SEV[1] - 100, 0.30),
    KM(A_Z["ini"] + 0.9, 1500, -300, 0.22),
    KM(A_Z["ini"] + 1.9, 40, -40, 1.5),
    KL(A_Z["ini"] + 2.9, -170, SUR + 2040, 1.7),
    KL(A_Z["hoy"] - 0.3, -170, SUR + 2040, 1.7),
    KL(A_Z["hoy"] + 2.2, -30, -290, 0.72),
    KL(A_Z["patrimonio"] + 1.6, -30, -290, 0.72),
    KL(A_Z["calle"] + 0.4, 130, -130, 1.05),
    KL(A_Z["bajo"] + 0.3, -40, SUR - 30, 1.9),
    KL(A_Z["fin"] + 1.6, -40, SUR + 40, 3.2),
    KL(A_Z["fin"] + 4.0, -40, SUR + 40, 3.2),
], respira=0.0)


def camara(t):
    if t < A_M["ini"]:
        return CAM_A(t)
    if t < A_M["fin"] - 0.2:
        lx, ly, zl = CMI.camara_pos(t)
        return (lx * LOC, ly * LOC, zl / LOC, 0.0)
    return CAM_B(t)


# ------------------------------------------------------------------ año (odómetro)
AÑO = Anios([
    (0.0, 1500), (CM.A["seis"] + 0.25, 1546, 1.8),
    (A_C["ocho"] + 0.3, 1548, 0.8),
    (A_CM["c49"] + 0.3, 1549, 0.8),
    (A_CM["c50"] + 0.4, 1550, 0.8),
    (A_P["siete"] + 0.3, 1557, 1.0),
    (A_CA["c50"] + 0.4, 1550, 1.0),
    (A_CA["n90"] + 0.4, 1590, 1.6),
    (A_CD["c58"] + 0.3, 1558, 2.0),
    (A_CD["o85"] + 0.9, 1585, 1.2),
    (A_CD["o88"] + 0.8, 1588, 0.8),
])


def alfa_placa(t):
    a = smooth(prog(t, CM.A["mil"] - 0.2, CM.A["mil"] + 0.3))
    b = 1 - smooth(prog(t, A_Z["costo"] - 0.6, A_Z["costo"] + 0.0))          # se apaga en el cierre
    return a * b


# ------------------------------------------------------------------ hora del día (color del cielo)
def hora_dia(t):
    """(color arriba, color abajo) del cielo según la escena."""
    tabla = [(0.0, "alba"), (A_CM["ini"] if "ini" in A_CM else INI("campamento"), "dia"), (A_P["ini"], "dia"),
             (A_CA["ini"], "dia"), (A_CA["atacan"], "tarde"), (A_CA["n90"], "alba"), (A_CD["ini"], "dia"),
             (A_Z["hoy"] - 1.0, "dia"), (A_Z["hoy"] + 0.5, "alba"), (A_Z["hoy"] + 6.0, "dia")]
    # patio: cielo en cámara rápida (día -> noche -> día, varias veces)
    if A_P["mulas"] <= t <= A_P["semanas"] + 3.0:
        ciclo = ["dia", "tarde", "noche", "alba"]
        u = (t - A_P["mulas"]) / 2.4
        i = int(u) % 4
        f = smooth(u - int(u))
        a, b = L.CIELO[ciclo[i]], L.CIELO[ciclo[(i + 1) % 4]]
        return (lerp_color(a[0], b[0], f), lerp_color(a[1], b[1], f))
    cur = tabla[0][1]
    prev = tabla[0][1]
    for ti, k in tabla:
        if t >= ti:
            prev = cur
            cur = k
    # transición suave de 1.2 s
    ti = max(x for x, k in tabla if x <= t) if any(x <= t for x, _ in tabla) else 0.0
    f = smooth(prog(t, ti, ti + 1.2))
    a, b = L.CIELO[prev], L.CIELO[cur]
    return (lerp_color(a[0], b[0], f), lerp_color(a[1], b[1], f))


class Mundo(Escena):
    """Plano secuencia: todas las escenas del guion comparten este mismo mundo continuo."""

    def preparar(self):
        self.tc = 0.0
        if self.idx == 0:
            registrar_sfx(self)

    def render(self, lz, t):
        self.tc = t
        return super().render(lz, t)

    def matriz_camara(self, t):
        cx, cy, z, rot = camara(t)
        return mat_t(W / 2, H / 2) @ mat_r(rot) @ mat_s(z) @ mat_t(-cx, -cy)

    def fondo(self, t):
        cx, cy, z, rot = camara(t)
        pap = F.papel(t, dx=cx * z * 0.05, dy=cy * z * 0.05)
        al = CL.alfa_local(z)
        if al > 0.01:
            return F.cielo_fondo(hora_dia(t), al, pap)
        return pap

    def dibujar(self, lz, t):
        cx, cy, z, rot = camara(self.tc)
        CM.dibujar(lz, t, z)
        if A_PL["ini"] - 1.0 <= t <= A_Z["costo"] + 5.0:
            CPL.dibujar(lz, t, z) if CM.alfa_mapa(z) > 0.05 else None
        al = CL.alfa_local(z)
        if al > 0.01:
            with lz.grupo(0, 0, LOC):
                cam_l = (cx / LOC, cy / LOC)
                hd = hora_dia(t)
                CL.base_local(lz, t, cam_l, hd, alfa=al)
                self.mundo_local(lz, t, cam_l, z / (1 / LOC))

    def mundo_local(self, lz, t, cam_l, zl):
        """Contenido local según el momento del plano secuencia."""
        if CL.alfa_local(camara(self.tc)[2]) < 0.95:      # durante el zoom desde el mapa solo se ve el paisaje
            return
        if cam_l[1] + 960 / zl > SUR - 20:
            CMI.dibujar(lz, t, self.tc, cam_l)
        if t < A_CM["cfin"] + 0.5:
            if t < INI("campamento"):
                CE.dibujar_cerro(lz, t, self.tc, cam_l)
            else:
                CE.dibujar_campamento(lz, t, self.tc, cam_l)
        if INI("patio") - 1.5 <= t < A_CA["ini"] + 3.0:
            CP.dibujar(lz, t, self.tc, cam_l)
        if INI("patio") - 2.5 <= t < A_CA["fin"] + 1.0:
            CC.dibujar(lz, t, self.tc, cam_l)
        if INI("ciudad") - 1.0 <= t < A_PL["ini"] + 4.0 or A_Z["hoy"] - 2.0 <= t:
            CD.dibujar(lz, t, self.tc, cam_l) if t < A_Z["costo"] else None
        if t >= A_Z["ini"] + 1.8:
            self.cierre(lz, t, cam_l, zl)

    def cierre(self, lz, t, cam_l, zl):
        ka = smooth(prog(t, A_Z["ini"] + 2.6, A_Z["ini"] + 3.4)) * (1 - smooth(prog(t, A_Z["hoy"] - 1.2, A_Z["hoy"] - 0.2)))
        if ka > 0.01:
            CZ.mina_oscura(lz, t, self.tc, ka)
        kh = smooth(prog(t, A_Z["hoy"] + 0.2, A_Z["hoy"] + 3.0))
        if kh > 0.01:
            CZ.casas_hoy(lz, kh)
            CZ.catedral(lz, -30, float(L.h(-30)) + 150, 1.0, kh)
            CZ.teleferico(lz, t, kh)

    def ui(self, lz, t):
        U.odometro(lz, AÑO(t), alfa=alfa_placa(t))
        CM.ui(lz, t)
        UC.ui(lz, t)
        CD.ui(lz, t)
        return True


def ui_capitulos(lz, t):
    """Rótulos, tarjetas y contadores de cada capítulo (espacio de pantalla)."""
    pass


def registrar_sfx(m):
    import sonido
    sonido.registrar(m, T_DIVE0, None)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
