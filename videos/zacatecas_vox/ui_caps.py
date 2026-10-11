# -*- coding: utf-8 -*-
"""Rótulos, tarjetas y contadores de pantalla de cada capítulo (espacio de pantalla 1080x1920)."""
import math

import numpy as np

import cap_camino as CC
import cap_cerro as CE
import cap_ciudad as CD
import cap_cierre as CZ
import cap_local as CL
import cap_mina as CMI
import cap_patio as CP
import cap_plata as CPL
import ui_vox as U
import vox as V
from ctx import T, INI, FIN
from motor import W, H, prog, e_out, e_back, e_inout, smooth, clamp01, h01, lerp, rect_red

CX = W / 2
A_CE, A_CM = CL.A, CL.A
NOMBRES = dict(onate=T("cerro", "Oñate"), ibarra=T("cerro", "Ibarra"), banuelos=T("cerro", "Bañuelos"),
               hospicios=T("campamento", "hospicios"))


def ventana(t, t0, t1, ent=0.35, sal=0.3):
    """Factor de aparición 0..1 con rebote de entrada y salida suave."""
    if t < t0 or t > t1 + sal:
        return 0.0
    return e_back(prog(t, t0, t0 + ent), 1.6) * (1 - smooth(prog(t, t1, t1 + sal)))


def titular(lz, t, t0, t1, lineas, y=470, px=76, color=V.TINTA, marca=True):
    k = ventana(t, t0, t1 - 0.25, 0.35, 0.25)
    if k > 0.01:
        U.frase_grande(lz, lineas, CX, y, px=px, k=k, color=color, marcador=(len(lineas) - 1) if marca else None)


def pill(lz, t, t0, t1, x, y, txt, px=38, fondo=V.AMARILLO, color=V.TINTA, rot=0.0):
    k = ventana(t, t0, t1)
    if k > 0.01:
        V.pastilla(lz, x, y, txt, px, k=k, fondo=fondo, color=color, rot=rot)


def ui(lz, t):
    cerro(lz, t)
    campamento(lz, t)
    mina(lz, t)
    patio(lz, t)
    camino(lz, t)
    ciudad(lz, t)
    plata(lz, t)
    cierre(lz, t)


# ------------------------------------------------------------------ cerro
def cerro(lz, t):
    a = CL.A
    titular(lz, t, a["brill"] - 0.6, a["llega"] - 0.3, ["PIEDRAS", "BRILLANTES"], y=470)
    titular(lz, t, a["odre"] - 0.1, a["arma"] - 0.2, ["EL CERRO DE", "LA BUFA"], y=470)
    # veta de San Bernabé: sello de fecha
    k = ventana(t, a["ocho"] - 0.2, a["fiebre"] - 0.4)
    if k > 0.01:
        V.pastilla(lz, CX, 470, "11 DE JUNIO DE 1548", 44, k=k, fondo=V.ROJO, color=V.CREMA, rot=-0.03)
        V.pastilla(lz, CX, 560, "VETA DE SAN BERNABÉ", 40, k=k, fondo=V.AMARILLO, rot=0.02)
    titular(lz, t, a["fiebre"] - 0.1, a["fiebre"] + 2.6, ["LA FIEBRE", "DE LA PLATA"], y=470)
    # socios
    n = NOMBRES
    for i, (k_, nm) in enumerate((("onate", "CRISTÓBAL DE OÑATE"), ("ibarra", "DIEGO DE IBARRA"), ("banuelos", "BALTASAR DE BAÑUELOS"))):
        pill(lz, t, n[k_] - 0.1, CE_FIN + 0.3, CX, 430 + 92 * i, nm, 36, fondo=V.CREMA, rot=-0.02 + 0.02 * i)


CE_FIN = FIN("cerro") - 0.6


# ------------------------------------------------------------------ campamento
def campamento(lz, t):
    a = CL.A
    # 300 personas: matriz de puntos + contador
    t0, t1 = a["tres"] - 0.5, a["casas"] - 0.2
    k = ventana(t, t0, t1, 0.3, 0.4)
    if k > 0.01:
        cnt = 300 * e_out(prog(t, a["tres"] - 0.3, a["tres"] + 1.2))
        cnt = 300 if cnt > 299.5 else cnt
        U.tarjeta(lz, CX, 640, 800, 640, k, 0.0)
        cols, dx, dy = 20, 34, 30
        x0, y0 = CX - (cols - 1) * dx / 2, 640 - 15 * dy / 2 + 30 - 20
        if int(cnt) > 0:
            lz.puntos([(x0 + (i % cols) * dx, y0 + (i // cols) * dy) for i in range(int(cnt))], 10 * k, (216, 96, 70), capa=2)
        V.rotulo(lz, f"{int(cnt)} PERSONAS", CX, 400, 74 * k, color=V.TINTA, sombra=0.0)
        V.rotulo(lz, "1 PUNTO = 1 PERSONA", CX, 940, 30 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)
    # precios del maíz: flecha que sube
    k = ventana(t, a["caro"] - 0.2, a["ranch"] + 1.3)
    if k > 0.01:
        U.tarjeta(lz, CX, 640, 760, 480, k, 0.0)
        V.rotulo(lz, "TODO SE VENDE CARO", CX, 440, 56 * k, color=V.TINTA, sombra=0.0)
        pts = np.array([[CX - 300, 800], [CX - 180, 770], [CX - 60, 720], [CX + 40, 690], [CX + 140, 610], [CX + 300, 520]])
        fr = smooth(prog(t, a["caro"], a["maiz"] + 1.6))
        V.trazo_mano(lz, pts, fr, V.ROJO, 14, seed=5)
        if fr > 0.92:
            for s_ in (-0.5, 0.5):
                d = np.array([math.cos(-0.9 + s_), math.sin(-0.9 + s_)]) * 46
                lz.trazo(np.array([pts[-1], pts[-1] - d]), V.ROJO, 14, afinar=False, temblor=0.0, capa=2)
        pill(lz, t, a["maiz"], a["ranch"] + 1.3, CX - 170, 880, "MAÍZ", 36, V.AMARILLO)
        pill(lz, t, a["carne"], a["ranch"] + 1.3, CX + 130, 880, "CARNE", 36, V.CREMA)
    # 34 minas: contador
    n = int(34 * prog(t, a["t34"] - 0.2, a["t34"] + 3.2))
    k = ventana(t, a["t34"] - 0.5, a["hosp"] - 0.2)
    if k > 0.01:
        U.contador(lz, n, "MINAS EN OPERACIÓN · 1550", CX, 520, px=200 * k, alfa=k, color=V.ROJO, color2=V.TINTA)
    pill(lz, t, a["hosp"], a["cfin"] - 0.4, CX - 150, 500, "HOSPITALES", 40, V.CREMA, rot=-0.03)
    pill(lz, t, NOMBRES["hospicios"], a["cfin"] - 0.4, CX + 160, 590, "HOSPICIOS", 40, V.AMARILLO, rot=0.03)


# ------------------------------------------------------------------ mina
def silueta(lz, x, y, s, col, alfa=1.0):
    lz.relleno(V.elipse_pts(x, y - 40 * s, 13 * s, 13 * s), col, temblor=0.0, capa=2, alfa=alfa)
    lz.relleno(V.capsula([x, y - 24 * s], [x, y + 20 * s], 26 * s, 20 * s), col, temblor=0.0, capa=2, alfa=alfa)


def mina(lz, t):
    a = CMI.A
    # sin pueblos cercanos
    k = ventana(t, a["pueblos"] - 0.3, a["llegan"] - 0.3)
    if k > 0.01:
        U.tarjeta(lz, CX, 590, 820, 560, k, 0.0)
        V.rotulo(lz, "SIN PUEBLOS CERCANOS", CX, 370, 50 * k, color=V.TINTA, sombra=0.0)
        V.rotulo(lz, "a quienes obligar a trabajar", CX, 430, 34 * k, color=V.TINTA, fuente="vox_serif", sombra=0.0)
        for i, r in enumerate((70, 130, 190)):
            pts = np.array([[CX + r * math.cos(a_), 620 + r * math.sin(a_)] for a_ in np.linspace(0, 2 * math.pi, 40)])
            fr = smooth(prog(t, a["pueblos"] + 0.1 * i, a["pueblos"] + 0.8 + 0.1 * i))
            V.trazo_mano(lz, pts, fr, V.ROJO if i == 2 else (150, 130, 110), 5, seed=i)
        from mapa_dib import estrella
        estrella(lz, CX, 620, 26 * k, alfa=k)
        for i in range(4):
            ang = 0.7 + i * 1.5
            kx = e_back(prog(t, a["obligar"] - 0.6 + 0.1 * i, a["obligar"] - 0.2 + 0.1 * i))
            if kx > 0.01:
                px_, py_ = CX + 150 * math.cos(ang), 620 + 150 * math.sin(ang)
                lz.trazo(np.array([[px_ - 12 * kx, py_ - 12 * kx], [px_ + 12 * kx, py_ + 12 * kx]]), V.ROJO, 8, afinar=False, temblor=0.0, capa=2)
                lz.trazo(np.array([[px_ - 12 * kx, py_ + 12 * kx], [px_ + 12 * kx, py_ - 12 * kx]]), V.ROJO, 8, afinar=False, temblor=0.0, capa=2)
    # trabajadores libres: una parte del mineral
    k = ventana(t, a["llegan"] - 0.3, a["esclav"] - 0.5)
    if k > 0.01:
        U.tarjeta(lz, CX, 590, 820, 560, k, 0.0)
        V.rotulo(lz, "TRABAJADORES LIBRES", CX, 370, 50 * k, color=V.TINTA, sombra=0.0)
        V.figura(lz, CX - 180, 740, 0.62 * k, V.CAMINAR[V.cuadro(V.CAMINAR, t, 15.0)], "minero", 1, capa=2, seed=5)
        # montón de mineral que se parte en dos
        u = smooth(prog(t, a["parte"] - 0.2, a["parte"] + 1.0))
        for j, sx in enumerate((-1, 1)):
            V.rotulo(lz, "", 0, 0, 1) if False else None
        cx_ = CX + 150
        lz.relleno(V.poligono_reg(cx_ - 70 * u, 720, 62, 6, 0.3), (128, 120, 118), temblor=0.0, capa=2, alfa=k)
        lz.relleno(V.poligono_reg(cx_ + 70 * u, 720, 62, 6, 1.1), (128, 120, 118), temblor=0.0, capa=2, alfa=k)
        lz.relleno(V.poligono_reg(cx_ - 70 * u - 12, 700, 14, 5, 0.4), V.PLATA, temblor=0.0, capa=2, alfa=k)
        lz.relleno(V.poligono_reg(cx_ + 70 * u + 12, 700, 14, 5, 0.4), V.PLATA, temblor=0.0, capa=2, alfa=k)
        V.pastilla(lz, cx_ - 110 * u, 850, "PARA EL DUEÑO", 32, k=k * u, fondo=V.CREMA)
        V.pastilla(lz, cx_ + 110 * u, 930, "PARA ÉL", 32, k=k * u, fondo=V.AMARILLO)
    # esclavizados
    k = ventana(t, a["esclav"] - 0.3, a["fin"] + 0.4)
    if k > 0.01:
        U.tarjeta(lz, CX, 610, 860, 620, k, 0.0)
        V.rotulo(lz, "ESCLAVIZADOS", CX, 350, 60 * k, color=V.TINTA, sombra=0.0)
        V.rotulo(lz, "INDÍGENAS Y AFRICANOS", CX, 415, 30 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)
        v = 230 * e_out(prog(t, a["doscientos"] - 0.2, a["doscientos"] + 1.6))
        if t > a["doscientos"] - 0.3:
            V.rotulo(lz, f"{int(v)}", CX, 560, 170 * k, color=V.ROJO, sombra=0.0)
        V.rotulo(lz, "AFRICANOS EN 1597", CX, 650, 40 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)
        n = int(23 * prog(t, a["doscientos"] - 0.1, a["doscientos"] + 1.7))
        for i in range(n):
            silueta(lz, CX - 11 * 34 + (i % 12) * 34 + (i // 12) * 17, 760 + (i // 12) * 70, 0.9 * k, (60, 44, 50))
        V.rotulo(lz, "1 SILUETA = 10 PERSONAS", CX, 880, 26 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)


# ------------------------------------------------------------------ patio
def patio(lz, t):
    a = CP.A
    titular(lz, t, a["benef"] - 0.2, a["muele"] - 0.2, ["EL BENEFICIO", "DE PATIO"], y=470)
    pill(lz, t, a["mineral"] - 0.1, a["atrapa"] - 0.4, CX - 200, 430, "MINERAL MOLIDO", 34, V.CREMA, rot=-0.02)
    pill(lz, t, a["sal"] - 0.1, a["atrapa"] - 0.4, CX + 210, 520, "+ SAL", 40, V.CREMA, rot=0.03)
    pill(lz, t, a["mercurio"] - 0.1, a["atrapa"] - 0.4, CX - 120, 610, "+ MERCURIO", 40, V.AMARILLO, rot=-0.02)
    # semanas: tira de calendario
    k = ventana(t, a["semanas"] - 0.2, a["atrapa"] - 0.5)
    if k > 0.01:
        n = int(21 * prog(t, a["semanas"] - 0.1, a["semanas"] + 2.0))
        V.rotulo(lz, "DURANTE SEMANAS", CX, 720, 54 * k, color=V.TINTA, sombra=0.0)
        for i in range(n):
            x = CX - 10 * 42 + (i % 21) * 42
            lz.relleno(rect_red(x - 16, 770, 32, 36, 6), (250, 240, 224) if i % 7 else V.ROJO, temblor=0.0, capa=2, alfa=k)
    titular(lz, t, a["atrapa"] - 0.1, a["pobre"] - 0.4, ["EL MERCURIO", "ATRAPA LA PLATA"], y=470)
    pill(lz, t, a["pobre"] - 0.1, a["espana"] - 0.5, CX, 470, "MINERAL POBRE  →  PLATA", 40, V.AMARILLO)
    pill(lz, t, a["espana"] - 0.1, a["fin"] + 0.5, CX, 470, "MERCURIO DE ESPAÑA", 46, V.CREMA)


# ------------------------------------------------------------------ camino
def camino(lz, t):
    a = CC.A
    titular(lz, t, a["camino"] - 0.1, a["guerra"] - 0.2, ["CAMINO REAL", "DE TIERRA ADENTRO"], y=470, px=68)
    titular(lz, t, a["guerra"] - 0.1, a["c50"] - 0.1, ["TERRITORIO", "EN GUERRA"], y=470)
    # línea de tiempo de la guerra
    k = ventana(t, a["conflicto"] - 0.3, a["presidios"] - 0.4)
    if k > 0.01:
        U.tarjeta(lz, CX, 560, 860, 360, k, 0.0)
        V.rotulo(lz, "GUERRA CHICHIMECA", CX, 440, 54 * k, color=V.TINTA, sombra=0.0)
        fr = smooth(prog(t, a["conflicto"], a["caro"] + 0.8))
        lz.relleno(rect_red(CX - 340, 580, 680, 16, 8), (210, 196, 170), temblor=0.0, capa=2, alfa=k)
        lz.relleno(rect_red(CX - 340, 580, 680 * fr, 16, 8), V.ROJO, temblor=0.0, capa=2, alfa=k)
        V.rotulo(lz, "1550", CX - 340, 640, 46 * k, color=V.TINTA, ancla=(0.0, 0.5), sombra=0.0)
        V.rotulo(lz, "1590", CX + 340, 640, 46 * k, color=V.TINTA, ancla=(1.0, 0.5), sombra=0.0)
        V.rotulo(lz, f"{int(1550 + 40 * fr)}", CX, 520, 90 * k, color=V.ROJO, sombra=0.0) if False else None
        V.rotulo(lz, "LA MÁS LARGA Y CARA", CX, 700, 38 * k, color=V.TINTA, fuente="vox_b", sombra=0.0)
    titular(lz, t, a["presidios"] - 0.1, a["final"] - 0.2, ["PRESIDIOS", "Y ESCOLTAS"], y=470)
    titular(lz, t, a["final"] - 0.1, a["n90"] - 0.5, ["LA FUERZA", "NO BASTA"], y=470)
    pill(lz, t, a["caldera"] - 0.2, a["fin"] + 0.3, CX, 430, "MIGUEL CALDERA · 1590", 40, V.CREMA)
    k = ventana(t, a["paz"] - 0.1, a["fin"] + 0.3, 0.3, 0.3)
    if k > 0.01:
        with lz.capa(2):
            with lz.grupo(CX, 560, 1.0, -0.08):
                lz.relleno(rect_red(-190, -70, 380, 140, 14), V.ROJO, temblor=0.0, alfa=k)
                lz.relleno(rect_red(-176, -56, 352, 112, 8), (206, 66, 52), temblor=0.0, alfa=k)
                lz.texto("PAZ", 0, 6, 120 * k, "vox_x", color=V.CREMA, borde=None, temblor=0.0)
    pill(lz, t, a["comida"] - 0.1, a["fin"] + 0.3, CX - 240, 700, "COMIDA", 38, V.AMARILLO)
    pill(lz, t, a["ropa"] - 0.1, a["fin"] + 0.3, CX + 20, 780, "ROPA", 38, V.CREMA)
    pill(lz, t, a["ganado"] - 0.1, a["fin"] + 0.3, CX + 250, 700, "GANADO", 38, V.AMARILLO)


# ------------------------------------------------------------------ ciudad
def ciudad(lz, t):
    a = CD.A
    titular(lz, t, a["aldea"] - 0.1, a["francis"] - 0.2, ["DE ALDEA", "A CIUDAD"], y=470)
    pill(lz, t, a["francis"] - 0.1, a["o85"] - 0.5, CX, 470, "CONVENTO FRANCISCANO · 1558", 36, V.CREMA)
    pill(lz, t, a["mercados"] - 0.1, a["fin"] + 0.3, CX - 200, 470, "MERCADOS", 44, V.AMARILLO, rot=-0.02)
    pill(lz, t, a["matadero"] - 0.1, a["fin"] + 0.3, CX + 190, 560, "MATADERO", 44, V.CREMA, rot=0.02)


# ------------------------------------------------------------------ plata
def plata(lz, t):
    a = CPL.A
    titular(lz, t, a["ini"] + 0.2, a["mar"] - 0.4, ["LA RUTA", "DE LA PLATA"], y=470, color=V.TINTA)


# ------------------------------------------------------------------ cierre
def cierre(lz, t):
    a = CZ.A
    # HOY (placa) y patrimonio
    k = ventana(t, a["hoy"] - 0.1, a["humanidad"] + 1.0, 0.4, 0.5)
    if k > 0.01:
        U.placa_texto(lz, "HOY", CX, 210, px=120, alfa=min(1.0, k))
    titular(lz, t, a["patrimonio"] - 0.3, a["calle"] - 0.2, ["PATRIMONIO DE", "LA HUMANIDAD"], y=470, px=70)
    titular(lz, t, a["ini"] + 0.4, a["pagaron"] + 0.6, ["EL COSTO"], y=470, px=100, color=V.TINTA, marca=True)
    # tarjeta final
    k2 = smooth(prog(t, a["fin"] + 0.6, a["fin"] + 1.4))
    if k2 > 0.01:
        with lz.capa(2):
            lz.relleno(np.array([[0, 0], [W, 0], [W, H], [0, H]]), (18, 14, 20), temblor=0.0, alfa=k2)
        V.rotulo(lz, "ZACATECAS", CX, 840, 120 * k2, color=V.CREMA, sombra=0.0)
        V.rotulo(lz, "1546 – 1600", CX, 960, 74 * k2, color=V.AMARILLO, sombra=0.0)
        V.rotulo(lz, "BITÁCORA PERDIDA", CX, 1120, 40 * k2, color=V.CREMA, fuente="vox_b", sombra=0.0)
