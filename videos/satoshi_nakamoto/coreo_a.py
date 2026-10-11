# -*- coding: utf-8 -*-
"""Coreografía A: ORIGEN, GÉNESIS, FANTASMA, FORTUNA, PERFIL. Piezas en el tablero (coordenadas del mundo), cámara y textos.
Zonas: origen arriba-izquierda (-3900, -2100) · génesis arriba-centro (0, -2200) · fantasma arriba-derecha (3900, -2100) ·
fortuna alrededor del centro · perfil abajo-izquierda (-3800, 2150). El centro (0, 0) es la tarjeta de SATOSHI."""
import json
import os

import tablero as T
import piezas as PZ
import piezas2 as P2
import portales as PO
from coreo_comun import *  # noqa: F401,F403

Pz = T.Pieza
ROJA, AZUL, AMAR, VERDE = (0.82, 0.10, 0.10), (0.15, 0.42, 0.88), (0.92, 0.78, 0.12), (0.18, 0.62, 0.32)


def pol(nombre, ley, ancho=460, asp=1.0, foco=(0.5, 0.4), gris=False):
    return T.polaroid(nombre, ancho, asp, foco, ley, gris=gris)[0]


def portal_pz(nombre, ley, x, y, rot, t_in, ancho=560, s=1.0, **kw):
    L, ven = T.polaroid(None, ancho, 16 / 9, leyenda=ley, ventana=True, seed=abs(hash(nombre)) % 50)
    return Pz(L, x, y, rot, s, t_in=t_in, portal=PO.PORTAL[nombre], ventana=ven, **kw)


# ============================================================================================ CENTRO (siempre)
P_SAT = Pz(T.silueta_card("SATOSHI NAKAMOTO", "¿QUIÉN ES?", 520), 0, 0, -1.5, 1.35, t_in=-1, entrada=None, chinchetas=((0, None, ROJA),))
P_BOVEDA = portal_pz("boveda", "LA FORTUNA DE SATOSHI", -1050, 720, -3, -1, 560, entrada=None, chinchetas=((0, None, AMAR),))

# ============================================================================================ ORIGEN
o = "origen"
CAL_SEP = Pz(PZ.calendario(9, 2008, (15,)), -4950, -2480, -4, t_in=INI(o, 0) + 0.7)
P_LEHMAN = portal_pz("lehman", "LEHMAN BROTHERS · 15-SEP-2008", -4250, -2330, 3, ww(o, 1, "quince") - 0.7)
P_RESCATE = portal_pz("rescate", "RESCATES CON DINERO PÚBLICO", -3420, -2650, -2, INI(o, 2) - 0.3)
P_ESCRI = portal_pz("escritorio", "ALGUIEN EMPIEZA A PROGRAMAR", -3250, -1930, 2, INI(o, 3) - 0.3)
F_DOMINIO = Pz(T.ficha("18-AGO-2008\nSe registra el dominio bitcoin.org", titulo="DOMINIO"), -4980, -1760, -3, t_in=ww(o, 4, "agosto"))
P_NAV = portal_pz("navegador", "bitcoin.org", -4300, -1520, 4, ww(o, 4, "agosto") + 0.6, 500)
F_CORREO = Pz(T.ficha("20-AGO-2008 · Satoshi escribe a Adam Back: ¿cómo citar Hashcash?\n(correos presentados en un juicio en 2024)", 600, 360,
                      titulo="PRIMER RASTRO", px=31), -3580, -1270, -2, t_in=ww(o, 5, "desconocido") - 0.2, chinchetas=((0, None, AZUL),))
P_BACK = Pz(pol("adam_back", "ADAM BACK", 480, 0.9, (0.45, 0.38)), 3800, 120, 4, 1.1, t_in=ww(o, 5, "bak") - 0.35)
F_BACK = Pz(T.ficha("Criptógrafo británico.\nCreó Hashcash en 1997.", 480, 260, titulo="ADAM BACK"), 3250, 620, -4, t_in=ww(o, 5, "citar"))
T.Punteada(F_CORREO, P_BACK, ww(o, 5, "escribe"), color=(1.0, 0.85, 0.45), curva=0.06, dur=1.6, paquetes=5, vel=0.25, grosor=7.0)
sello_en(F_CORREO, "PRIMER RASTRO", ww(o, 6, "primer"), 40, 40, -8, 50)
rojo(F_CORREO, P_SAT, ww(o, 6, "rastro") + 0.2, 1.2)
P_WP = Pz(T.hoja_img("whitepaper", 900, (0, 0, 1, 0.965)), -2420, -2160, 2, t_in=ww(o, 7, "documento") - 0.2, chinchetas=((0, None, AMAR),))
for k in range(3):
    Pz(T.oscura(T.hoja_img("whitepaper", 900, (0, 0, 1, 0.965)), 0.85), -2420 + 26 * (k + 1), -2160 + 20 * (k + 1), 2 + 2 * (k + 1),
       t_in=ww(o, 7, "documento") - 0.2, entrada="aparece", chinchetas=(), capa=0, sonido=False)
P_P2P = portal_pz("p2p", "SIN BANCOS", -2350, -1300, -3, INI(o, 9) - 0.4)

TX(S([("2008", INI(o, 0) + 1.6)], W / 2, 180, 120), INI(o, 0) + 1.5, FIN(o, 0), False)
TX(R(pk(o, 2, "los", "publico")), ww(o, 2, "los"), FIN(o, 2))
TX(R(pk(o, 3, "otra", "idea"), cy=880), ww(o, 3, "otra"), FIN(o, 3) + 0.3)
TX(S([("Adam", ww(o, 5, "bak") - 0.2), ("Back", ww(o, 5, "bak"))], W / 2, 900, 110), ww(o, 5, "bak") - 0.2, FIN(o, 5))
TX(N("9 PÁGINAS", W / 2, 920, 120, ww(o, 7, "nueve"), (0.95, 1.0, 0.1)), ww(o, 7, "nueve"), FIN(o, 7) + 0.2)
TX(R(pk(o, 8, "un", "persona", 0, 1), cy=890, px=74), ww(o, 8, "un"), FIN(o, 8))
TX(R(pk(o, 9, "dinero", "matematicas"), cy=190, px=80), INI(o, 9), FIN(o, 9), False)
FOTO_CRED("lehman_dia", ww(o, 1, "quince"), FIN(o, 1))
FOTO_CRED("adam_back", ww(o, 5, "bak"), FIN(o, 5))

# cámara ORIGEN
K(INI(o, 0) - 0.2, -4500, -2300, 0.75, -3, 6, 8)
K(INI(o, 0) + 1.5, -4800, -2420, 1.25, -2, 3, 4)
DENTRO(P_LEHMAN, ww(o, 1, "quince") - 0.1, ww(o, 1, "quiebra") + 0.4, FIN(o, 1) + 0.1)
K(INI(o, 2) + 0.4, -3900, -2500, 1.1, 0, 4, 6)
DENTRO(P_RESCATE, INI(o, 2) + 1.2, ww(o, 2, "rescatan"), FIN(o, 2) + 0.1)
K(INI(o, 3) + 0.4, -3300, -2250, 1.0, 1, -3, 5)
DENTRO(P_ESCRI, INI(o, 3) + 1.2, ww(o, 3, "trabajando"), FIN(o, 3) + 0.2)
K(INI(o, 4) + 0.6, -4700, -1700, 1.15, -2, 4, -5)
DENTRO(P_NAV, ww(o, 4, "registrado") - 0.4, ww(o, 4, "dominio") + 0.4, FIN(o, 4) - 0.1, 1.5)
K(INI(o, 5) + 0.2, -3580, -1270, 1.35, -1, 3, 3)
K(ww(o, 5, "britanico"), 0, -560, 0.42, 0, 8, 0)
K(ww(o, 5, "bak") + 0.3, 3700, 220, 1.15, 3, -3, -6, modo="suave")
K(FIN(o, 5) - 0.2, 3500, 380, 1.25, 1, -2, -4)
LATIGO(FIN(o, 5) + 0.05, INI(o, 6) + 0.5, -3560, -1260, 1.45, -1, 2, 2)
K(FIN(o, 6) + 0.1, -3300, -1500, 1.0, 0, 3, -4)
K(ww(o, 7, "documento"), -2450, -2000, 0.95, 1, 4, 5)
K(FIN(o, 7), -2420, -2160, 1.15, 2, 2, 3)
K(INI(o, 8) + 0.5, -2420, -2480, 2.4, 2, 0, 0, modo="suave")
K(FIN(o, 8), -2420, -2440, 2.6, 2, 0, 0)
DENTRO(P_P2P, INI(o, 9) + 0.1, INI(o, 9) + 1.0, FIN(o, 9) + 0.2)

# ============================================================================================ GÉNESIS
g = "genesis"
P_BLOQ = portal_pz("bloques", "BLOQUE 0 · 3-ENE-2009", -1150, -2330, -3, INI(g, 0) - 0.5)
L_HEX, _f = PZ.impresion_hex()
P_HEX = Pz(L_HEX, -150, -2230, 1.5, t_in=INI(g, 1) + 0.2, chinchetas=((-380, None, ROJA), (380, None, ROJA)))
P_TIMES = Pz(T.hoja_img("genesis_periodico", 860), 700, -2420, -3, t_in=ww(g, 2, "titular") - 0.2)
P_DARLING = Pz(pol("darling_2009", "ALISTAIR DARLING", 430, 0.85, (0.20, 0.38)), 1420, -2150, 4, t_in=ww(g, 2, "ministro") - 0.2)
F_DARLING = Pz(T.ficha("Ministro de Hacienda del Reino Unido (2007-2010)", 430, 210, px=28, rayada=False), 1430, -1720, -2,
               t_in=ww(g, 2, "hacienda"), chinchetas=((0, None, AZUL),))
T.Cinta(260, -2300, 70, ww(g, 2, "titular") + 0.4, 170)
P_CODE = Pz(PZ.impresion_codigo(1440, 30, 820, 18, resaltar=15), 250, -1600, -2, t_in=INI(g, 3) + 0.2)
sello_en(P_HEX, "3 ENE 2009", ww(g, 3, "sello") + 0.1, -180, 120, -7, 56)
N_POL = Pz(T.nota("¿MENSAJE POLÍTICO?", 280), 860, -1620, 6, t_in=ww(g, 3, "declaracion"), chinchetas=((0, None, None),), entrada="aparece", dur=0.3)
P_UK = Pz(P2.bandera_uk(), 1500, -1300, -5, t_in=ww(g, 4, "britanico") - 0.1, chinchetas=((0, None, ROJA),))
N_UK = Pz(T.nota("¿BRITÁNICO?", 260, (0.98, 0.86, 0.25)), 1880, -1150, 5, t_in=ww(g, 4, "britanico") + 0.3, chinchetas=((0, None, None),),
          entrada="aparece", dur=0.3)
rojo(P_UK, P_SAT, ww(g, 4, "japones"), 1.1, etiqueta=T.ficha("PISTA: INGLÉS BRITÁNICO", 330, 80, rayada=False, px=24))
P_V01 = Pz(PZ.impresion_codigo(0, 14, 680, 18, resaltar=0, titulo="Bitcoin v0.1 · publicado el 9-ENE-2009"), -900, -1480, 3,
           t_in=ww(g, 5, "publica") - 0.2)
CAL_ENE = Pz(PZ.calendario(1, 2009, (3, 9, 12)), -1550, -1760, -5, t_in=INI(g, 5) - 0.2)
P_HAL = Pz(pol("hal_finney", "HAL FINNEY", 480, 0.85, (0.5, 0.33), True), -2350, -600, -3, 1.1, t_in=ww(g, 5, "jal") - 0.3)
P_TWEET = Pz(T.hoja_img("running_bitcoin", 300), -2980, -1120, -4, t_in=ww(g, 6, "escribe") - 0.1)
F_TX = Pz(T.ficha("12-ENE-2009 · bloque 170\nSatoshi envía 10 BTC a Hal Finney", 520, 300, titulo="1.ª TRANSACCIÓN"), -1680, -1150, 2,
          t_in=ww(g, 7, "doce") - 0.1, chinchetas=((0, None, (0.95, 0.55, 0.1)),))
T.Punteada(P_SAT, P_HAL, ww(g, 7, "envia"), color=(1.0, 0.70, 0.25), curva=-0.12, paquetes=3, vel=0.5)
rojo(F_TX, P_HAL, ww(g, 7, "primera"), 0.8)

TX(S([("Bloque", ww(g, 0, "bloque", 1)), ("Génesis", ww(g, 0, "genesis"))], W / 2, 900, 110), ww(g, 0, "bloque", 1), FIN(g, 0) + 0.3)
TX(R(pk(g, 2, "el", "bancos", 1), cy=175, px=70), ww(g, 2, "ministro"), FIN(g, 2) + 0.2, False)
TX(S([("The", ww(g, 2, "taims") - 0.15), ("Times", ww(g, 2, "taims")), ("·", ww(g, 2, "taims")), ("3", ww(g, 2, "taims")), ("Ene", ww(g, 2, "taims")),
      ("2009", ww(g, 2, "taims"))], W / 2, 170, 84), ww(g, 2, "taims") - 0.15, ww(g, 2, "ministro") - 0.2, False)
TX(S([("«Running", ww(g, 6, "corriendo")), ("Bitcoin»", ww(g, 6, "bitcoin"))], W / 2, 900, 110), ww(g, 6, "corriendo"), FIN(g, 6) + 0.3)
TX(N("10 BTC", W / 2, 880, 150, ww(g, 7, "diez"), (0.98, 0.62, 0.12)), ww(g, 7, "diez"), FIN(g, 7) + 0.2)
FOTO_CRED("genesis_periodico", ww(g, 2, "titular"), INI(g, 3))
FOTO_CRED("darling_2009", ww(g, 2, "ministro") + 0.5, FIN(g, 2))
FOTO_CRED("hal_finney", ww(g, 5, "jal"), FIN(g, 5))
FOTO_CRED("running_bitcoin", ww(g, 6, "escribe"), FIN(g, 6))
T.Lupa([(ww(g, 1, "escondido"), -150 + 160, -2230 - 120), (ww(g, 1, "mensaje") + 0.6, -150 + 300, -2230 - 30),
        (FIN(g, 1) + 1.8, -150 + 250, -2230 + 60)], 240, 2.0)

# cámara GÉNESIS
K(FIN(o, 9) + 1.0, -1700, -2100, 0.8, 0, 5, 6)
DENTRO(P_BLOQ, INI(g, 0) + 0.3, ww(g, 0, "crea"), FIN(g, 0) + 0.1)
K(INI(g, 1) + 0.5, -150, -2230, 1.4, 1, 3, -3)
K(FIN(g, 1), 100, -2260, 1.9, 1.5, 0, 0)
K(ww(g, 2, "titular"), 300, -2350, 1.05, 0, 3, 4)
K(ww(g, 2, "taims") + 0.2, 700, -2420, 1.6, -2, 0, 2)
K(ww(g, 2, "ministro"), 1200, -2100, 1.15, 2, -3, -3)
K(FIN(g, 2), 1420, -2000, 1.35, 3, 0, -2)
K(INI(g, 3) + 0.4, 200, -1900, 0.95, 0, 4, 4)
K(ww(g, 3, "sello"), -200, -2150, 1.5, 1, 0, 0)
K(ww(g, 3, "declaracion"), 700, -1650, 1.35, 3, -3, 3)
K(FIN(g, 3), 500, -1580, 1.6, 0, 0, 0)
K(ww(g, 4, "britanico"), 1550, -1250, 1.35, -3, 2, -4)
K(ww(g, 4, "japones") + 0.3, 1450, -1100, 1.0, -2, 4, 3)
K(FIN(g, 4) + 0.2, 1200, -900, 0.9, 0, 4, 3)
K(ww(g, 5, "publica"), -900, -1450, 1.4, 3, 0, 4)
K(ww(g, 5, "descargarlo"), -1500, -1650, 1.2, -3, -2, 3)
K(ww(g, 5, "jal") + 0.1, -2300, -650, 1.3, -2, 2, -3, modo="suave")
K(ww(g, 6, "escribe") + 0.2, -2900, -1050, 1.6, -3, 0, -2)
K(FIN(g, 6), -2950, -1120, 2.1, -4, 0, 0)
K(ww(g, 7, "satoshi"), -1100, -500, 0.62, 0, 5, 4)
K(ww(g, 7, "primera"), -1700, -1100, 1.3, 1, 0, -3)
K(FIN(g, 7) + 0.3, -1900, -900, 1.15, 0, 2, 2)

# ============================================================================================ FANTASMA
f = "fantasma"
_posts = [p for p in json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "datos", "forum_posts.json"), encoding="utf-8"))
          if p.get("satoshi_id")]
_rng = __import__("numpy").random.default_rng(31)
RAFAGA = []
for i in range(30):
    p_ = _posts[int(i * len(_posts) / 30)]
    cx, cy = 2650 + (i % 6) * 250 + _rng.uniform(-30, 30), -2780 + (i // 6) * 165 + _rng.uniform(-20, 20)
    L = T.ficha(f"{p_['date'][:10]}\n{p_.get('subject', '')[:26]}", 250, 150, None, i, px=19, fuente="courier", rayada=False)
    RAFAGA.append(Pz(L, cx, cy, _rng.uniform(-8, 8), 1.0, t_in=INI(f, 0) + 0.25 + i * 0.16, dur=0.45, sonido=(i % 5 == 0),
                     chinchetas=((0, None, [ROJA, AZUL, AMAR, VERDE][i % 4]),)))
P_CODE2 = Pz(PZ.impresion_codigo(2200, 26, 640, 16, 3), 4600, -2650, 3, t_in=INI(f, 1) + 0.8)
ICON = [Pz(P2.icono_card(n), 2900 + k * 420, -1600, [-4, 3, -2][k], t_in=INI(f, 2) + 0.3 + k * 0.25) for k, n in enumerate(("telefono", "camara", "reunion"))]
for k, w_ in enumerate(("llamada", "foto", "reunion")):
    tache(ICON[k], ww(f, 2, w_))
F_PERFIL = Pz(T.ficha("Hombre · 37 años · vive en Japón · nacido el 5-abr-1975", 560, 320, titulo="PERFIL (P2P FOUNDATION)"), 4550, -1720, 2,
              t_in=INI(f, 3) + 0.2)
circulo(F_PERFIL, ww(f, 3, "japones"), 0.5, 0, 30, 240, 90)
N_JAP = Pz(T.nota("¿JAPONÉS?", 240), 5050, -1450, 6, t_in=ww(f, 3, "japones") + 0.4, chinchetas=((0, None, None),), entrada="aparece", dur=0.3)
P_PIZZAF = Pz(pol("pizza_day", "22-MAY-2010", 420, 0.85, (0.5, 0.42)), 4500, -2620, -3, t_in=INI(f, 4) - 0.2)
P_PIZZA = portal_pz("pizza", "2 PIZZAS = 10.000 BTC", 5250, -2250, 3, INI(f, 4) + 0.6)
P_WIKI = portal_pz("wikileaks", "DIC-2010 · DONACIONES BLOQUEADAS", 2600, -1250, 3, INI(f, 5) - 0.3)
Q_CALOR = Pz(PZ.tarjeta_cita("Esa atención probablemente nos destruiría en esta etapa.",
                             "Satoshi, dic-2010 · «the heat you would bring would likely destroy us at this stage»", 720, 38), 3350, -1000, -2,
             t_in=INI(f, 6) + 0.2)
F_ULT = Pz(T.ficha("12-DIC-2010\nÚltimo mensaje público en el foro", 480, 260, titulo="SE DESPIDE"), 4150, -1180, 3, t_in=INI(f, 7) + 0.1)
Q_OTRAS = Pz(PZ.tarjeta_cita("Me he pasado a otras cosas.", "Satoshi a Mike Hearn, abril de 2011 · «I've moved on to other things»", 740, 50),
             4950, -1150, 2, t_in=ww(f, 8, "abril") - 0.1)
rojo(Q_OTRAS, P_SAT, ww(f, 9, "silencio") - 0.6, 1.6, color="negro")


def _silencio(t, a=ww(f, 9, "silencio") - 0.1, b=INI("fortuna", 0) + 0.4):
    if t < a or t > b + 0.6:
        return 1.0
    return 1 - 0.62 * T.sm(T.pr(t, a, a + 0.7)) * (1 - T.sm(T.pr(t, b, b + 0.6)))


T.LUZ_FX.append(_silencio)
snd(ww(f, 9, "silencio") - 0.1, "apagon", 0.45)

TX(N("543", W / 2, 860, 170, ww(f, 1, "quinientos"), (0.95, 1.0, 0.1)), ww(f, 1, "quinientos"), FIN(f, 1) + 0.2)
TX(S([("Japón", ww(f, 3, "japones")), ("·", ww(f, 3, "nacido")), ("1975", ww(f, 3, "nacido") + 0.3)], W / 2, 900, 110), ww(f, 3, "japones"), FIN(f, 3))
TX(R(pk(f, 8, "se", "cosas"), cy=880), ww(f, 8, "se"), FIN(f, 8) + 0.6)
FOTO_CRED("pizza_day", INI(f, 4), ww(f, 4, "pizzas"))

# cámara FANTASMA
K(INI(f, 0) - 0.3, 600, -2000, 0.5, 0, 6, 6)
K(INI(f, 0) + 1.6, 2900, -2600, 1.0, -2, 4, -3)
K(FIN(f, 0), 3300, -2450, 0.85, 0, 3, 3)
K(ww(f, 1, "quinientos"), 3700, -2300, 0.75, 2, 2, -4)
K(FIN(f, 1), 4300, -2450, 1.0, 2, 0, 0)
K(INI(f, 2) + 0.4, 3300, -1700, 1.0, 0, 4, 4)
K(FIN(f, 2), 3500, -1620, 1.25, 0, 0, 0)
K(INI(f, 3) + 0.4, 4550, -1700, 1.3, 2, -2, -3)
K(FIN(f, 3), 4800, -1620, 1.45, 3, 0, 0)
K(INI(f, 4) + 0.3, 4600, -2550, 1.3, -2, 3, 3)
DENTRO(P_PIZZA, ww(f, 4, "pizzas"), ww(f, 4, "bitcoins") + 0.2, FIN(f, 4) + 0.1)
K(INI(f, 5) + 0.3, 3200, -1500, 0.85, 0, 4, 6)
DENTRO(P_WIKI, INI(f, 5) + 1.0, ww(f, 5, "donaciones"), FIN(f, 5) + 0.1)
K(INI(f, 6) + 0.5, 3350, -1000, 1.35, -2, 2, 3)
K(FIN(f, 6), 3350, -980, 1.6, -2, 0, 0)
K(INI(f, 7) + 0.3, 4150, -1180, 1.4, 3, -2, -3)
K(ww(f, 8, "abril") + 0.5, 4900, -1180, 1.25, 1, 2, -3)
K(ww(f, 8, "escribe") + 0.3, 4950, -1150, 1.45, 2, 0, 0, modo="suave")
K(FIN(f, 8), 4950, -1140, 1.7, 2, 0, 0)
K(FIN(f, 9) + 0.3, 4950, -1130, 2.1, 1, 0, 0, modo="suave")

# ============================================================================================ FORTUNA
fo = "fortuna"
P_PATOSHI = Pz(P2.esquema_patoshi(), 1150, -650, 2, t_in=ww(fo, 1, "investigador") - 0.2)
F_LERNER = Pz(T.ficha("Sergio Lerner (2013): una misma huella de minado en miles de los primeros bloques.", 520, 300, titulo="EL PATRÓN"),
              1750, -300, -3, t_in=ww(fo, 1, "huella") - 0.2)
P_DIR = Pz(P2.rejilla_direcciones(), -1150, -760, -2, t_in=INI(fo, 3) + 0.1)
P_PRUEBA = Pz(P2.casillas("LA ÚNICA PRUEBA", ("Mover una moneda de Satoshi", "Firmar un mensaje con su llave"), 760, px=34), 700, 840, -2, 1.05,
              t_in=ww(fo, 5, "basta") - 0.3, chinchetas=((0, None, ROJA),))
P_LLAVE = Pz(P2.icono_card("llave", 260), 1250, 1050, 6, t_in=ww(fo, 5, "llave") - 0.2)
sello_en(P_PRUEBA, "NADIE", ww(fo, 6, "nadie"), 0, 40, -10, 90)
rojo(P_PRUEBA, P_SAT, ww(fo, 5, "basta") + 0.4, 0.8)
rojo(P_BOVEDA, P_SAT, INI(fo, 2) + 0.3, 0.8, color="amarillo")

TX(S([("≈", ww(fo, 2, "millon")), ("1.100.000", ww(fo, 2, "millon")), ("BTC", ww(fo, 2, "bitcoins"))], W / 2, 170, 110), ww(fo, 2, "millon"),
   FIN(fo, 2) + 0.3, False)
TX(N("≈ 22.000", W / 2, 880, 140, ww(fo, 3, "veintidos"), (0.95, 1.0, 0.1)), ww(fo, 3, "veintidos"), FIN(fo, 3))
TX(R(pk(fo, 4, "la", "tablero"), cy=880, px=92), ww(fo, 4, "la"), FIN(fo, 4) + 0.3)
TX(R(pk(fo, 6, "en", "hecho"), cy=175, px=82), INI(fo, 6), FIN(fo, 6) + 0.6, False)

# cámara FORTUNA
K(INI(fo, 0) + 0.6, 2800, -600, 0.62, -2, 5, -4)
K(ww(fo, 1, "investigador") + 0.3, 1150, -650, 1.3, 2, 0, 3)
K(ww(fo, 1, "huella") + 0.3, 1450, -480, 1.2, 0, -2, 3)
K(FIN(fo, 1), 1450, -500, 1.2, 0, -3, 3)
DENTRO(P_BOVEDA, INI(fo, 2) + 0.2, ww(fo, 2, "acumulo"), FIN(fo, 2))
K(INI(fo, 3) + 0.6, -1150, -760, 1.3, -2, 2, -3)
K(FIN(fo, 3), -1100, -700, 1.5, -2, 0, 0)
K(ww(fo, 4, "clave"), 0, 0, 1.05, -1, 3, 3, modo="suave")
K(FIN(fo, 4) + 0.2, 0, 0, 1.25, -1, 0, 0)
K(ww(fo, 5, "documento"), 250, 300, 0.9, 0, 4, 0)
K(ww(fo, 5, "basta") + 0.4, 700, 820, 1.4, -2, 0, 3)
K(ww(fo, 5, "llave"), 950, 950, 1.3, 2, -2, -3)
K(FIN(fo, 5), 800, 860, 1.5, 0, 0, 0)
K(ww(fo, 6, "nadie") + 0.2, 680, 830, 1.75, -2, 0, 0, modo="suave")
K(FIN(fo, 6) + 0.7, 400, 600, 1.2, 0, 3, 3)

# ============================================================================================ PERFIL
pe = "perfil"
P_POSTS = Pz(P2.post_real(0, 3), -4650, 1850, -2, t_in=INI(pe, 0) - 0.3)
T.Lupa([(INI(pe, 0) + 1.2, -4900, 1700), (FIN(pe, 0), -4500, 1850), (FIN(pe, 1), -4700, 2050)], 230, 1.9)
N_NAT = Pz(T.nota("INGLÉS NATIVO", 260), -3950, 1480, 4, t_in=ww(pe, 1, "nativo"), chinchetas=((0, None, None),), entrada="aparece", dur=0.3)
P_UK2 = Pz(P2.bandera_uk(300), -3500, 1680, -6, t_in=ww(pe, 1, "britanicos") - 0.2)
F_ORTO = Pz(T.ficha("colour (2) · color (4)\ngrey · maths · «bloody hard»", 560, 330, titulo="ORTOGRAFÍA Y EXPRESIONES", px=34), -3300, 2200, 2,
            t_in=INI(pe, 2) + 0.2)
resalta(F_ORTO, ww(pe, 2, "reino"), -240, 0, -40)
resalta(F_ORTO, ww(pe, 2, "mezcla"), 10, 200, -40)
P_MAQ = portal_pz("maquina", "DOS ESPACIOS TRAS EL PUNTO", -4350, 2700, 3, INI(pe, 3) - 0.4)
L_GR, VEN_GR = P2.marco_grafica()
_t_bar = ww(pe, 5, "analizamos")
P_GRAF = Pz(L_GR, -2350, 2000, -1.5, 1.0, t_in=INI(pe, 4) - 0.2, portal=lambda t: P2.grafica_horas_viva(T.sm((t - _t_bar) / 3.0)),
            ventana=VEN_GR)
circulo(P_GRAF, ww(pe, 6, "cinco"), 0.6, -101, -10, 140, 190)
P_RELOJ = portal_pz("relojes", "LONDRES · NUEVA YORK · TOKIO", -2550, 2900, 2, ww(pe, 7, "costa") - 1.2)
N_EEUU = Pz(T.nota("¿COSTA ESTE DE EE. UU.?", 280), -1750, 2550, -5, t_in=ww(pe, 7, "este"), chinchetas=((0, None, None),), entrada="aparece", dur=0.3)
rojo(N_EEUU, P_SAT, ww(pe, 7, "japon"), 1.2, color="azul")

TX(R(pk(pe, 0, "estudiar", "escribe"), cy=880, px=86), ww(pe, 0, "estudiar"), FIN(pe, 0) + 0.3)
TX(N("543 MENSAJES", W / 2, 950, 100, ww(pe, 5, "quinientos"), (0.95, 1.0, 0.1)), ww(pe, 5, "quinientos"), FIN(pe, 5))
TX(S([("5:00", ww(pe, 6, "cinco")), ("–", ww(pe, 6, "mediodia")), ("12:00", ww(pe, 6, "mediodia")), ("UTC", ww(pe, 6, "universal"))], W / 2, 170, 96),
   ww(pe, 6, "cinco"), FIN(pe, 6), False)
TX(N("7", W / 2, 860, 230, ww(pe, 6, "siete"), (0.95, 0.15, 0.12)), ww(pe, 6, "siete"), FIN(pe, 6) + 0.5)

# cámara PERFIL
K(INI(pe, 0) + 0.2, -3200, 1300, 0.55, 0, 6, 5)
K(INI(pe, 0) + 1.8, -4650, 1850, 1.25, -2, 2, -3)
K(FIN(pe, 0), -4500, 1900, 1.35, -1, 0, 0)
K(ww(pe, 1, "nativo"), -4100, 1600, 1.2, 2, -2, 3)
K(FIN(pe, 1), -3600, 1650, 1.35, -4, 0, 0)
K(INI(pe, 2) + 0.3, -3300, 2150, 1.45, 2, 2, -3)
K(FIN(pe, 2), -3300, 2200, 1.65, 2, 0, 0)
DENTRO(P_MAQ, INI(pe, 3) + 0.2, ww(pe, 3, "espacios"), FIN(pe, 3) + 0.1)
K(INI(pe, 4) + 0.6, -2400, 2050, 1.1, -1, 4, 4)
K(ww(pe, 5, "analizamos"), -2350, 2000, 1.35, -1.5, 0, 0)
K(FIN(pe, 5), -2380, 2020, 1.45, -1.5, 0, 0)
K(ww(pe, 6, "cinco"), -2550, 2000, 1.7, -1.5, 0, 0, modo="suave")
K(FIN(pe, 6), -2600, 2000, 1.9, -1.5, 0, 0)
DENTRO(P_RELOJ, ww(pe, 7, "costa") - 0.5, ww(pe, 7, "este") + 0.3, ww(pe, 7, "japon") - 0.3)
K(ww(pe, 7, "tarde") + 0.2, -1800, 2500, 1.2, -4, 2, 3)
K(FIN(pe, 7) + 0.3, -1500, 2200, 0.9, 0, 4, -3)
