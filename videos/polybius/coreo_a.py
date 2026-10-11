# -*- coding: utf-8 -*-
"""Coreografía A: GANCHO, LEYENDA, CASOS y GOBIERNO. Piezas en el tablero (coordenadas del mundo), cámara y textos, todo anclado a palabras.
Zonas: gancho arriba-izquierda (-3300, -2000) · leyenda arriba (2200, -2000) · casos derecha (4300, 0) · gobierno abajo-derecha (3400, 2300).
El centro (0, 0) es la polaroid de POLYBIUS (portal «búsqueda»)."""
import tablero as T
import piezas as PZ
import portales as PO
from coreo_comun import *  # noqa: F401,F403

Pz = T.Pieza
ROJA, AZUL, AMAR, VERDE = (0.82, 0.10, 0.10), (0.15, 0.42, 0.88), (0.92, 0.78, 0.12), (0.18, 0.62, 0.32)


def pol(nombre, ley, ancho=460, asp=1.0, foco=(0.5, 0.4), gris=False):
    return T.polaroid(nombre, ancho, asp, foco, ley, gris=gris)[0]


def portal_pz(nombre, ley, x, y, rot, t_in, ancho=560, s=1.0, **kw):
    L, ven = T.polaroid(None, ancho, 16 / 9, leyenda=ley, ventana=True, seed=sum(map(ord, nombre)) % 50)
    return Pz(L, x, y, rot, s, t_in=t_in, portal=PO.PORTAL[nombre], ventana=ven, **kw)


# ============================================================================================ CENTRO (siempre)
P_POLY = portal_pz("busqueda", "POLYBIUS · ¿EXISTIÓ?", 0, 0, -1.5, -1, 600, 1.3, entrada=None, chinchetas=((0, None, ROJA),))

# ============================================================================================ GANCHO
g = "gancho"
P_PORT = Pz(pol("portland_estacion", "PORTLAND · DIC 1981", 620, 1.35, (0.38, 0.42)), -3500, -2100, -3, 1.1, t_in=-1, entrada=None)
A81 = Pz(PZ.anio_card(1981, 400, 30, sub="OREGÓN · EE. UU."), -2700, -2450, 4, t_in=ww(g, 0, "mil") - 0.25)
P_SALON = portal_pz("salon", "UN SALÓN RECREATIVO", -2750, -1650, 2, INI(g, 1) - 0.6, 620)
N_LEY = Pz(T.nota("«cuenta la leyenda…»", 270, px=44), -3550, -1500, -6, t_in=ww(g, 1, "leyenda") - 0.2, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
rojo(P_SALON, P_POLY, ww(g, 3, "polybius") - 0.5, 1.0)

TX(S([("Portland,", INI(g, 0) + 0.05), ("Oregón", ww(g, 0, "oregon"))], W / 2, 900, 120), INI(g, 0), ww(g, 0, "mil") - 0.35)
TX(N("1981", W / 2, 900, 200, ww(g, 0, "mil") + 0.45, (0.95, 1.0, 0.1)), ww(g, 0, "mil") + 0.45, FIN(g, 0) + 0.3)
TX(R(pk(g, 1, "una", "antes"), cy=900, px=80), ww(g, 1, "una"), FIN(g, 1) + 0.1)
TX(S([("Polybius", ww(g, 3, "polybius"))], W / 2, 190, 170), ww(g, 3, "polybius"), FIN(g, 3) + 0.4, False)
TX(R(pk(g, 3, "no", "divertir", 1), cy=900, px=92), ww(g, 3, "no", 1), FIN(g, 3) + 0.4)
FOTO_CRED("portland_estacion", INI(g, 0), FIN(g, 0))

K(0.0, -3500, -2150, 1.75, -3, 0, 0, modo="suave")
K(ww(g, 0, "mil"), -3300, -2200, 1.25, -1, 3, -4)
K(FIN(g, 0) + 0.2, -2900, -2250, 1.15, 2, 2, -3)
DENTRO(P_SALON, INI(g, 1) + 0.5, ww(g, 1, "salones") + 0.2, FIN(g, 2) - 0.2)
K(INI(g, 3) + 0.1, -2500, -1500, 0.9, 1, 4, -6)
LATIGO(ww(g, 3, "polybius") - 0.55, ww(g, 3, "polybius") + 0.1, 0, 0, 0.84, -1.5, 0, 0)
K(FIN(g, 3) + 0.3, 0, 0, 0.94, -1.5, 0, 0)


def _apagon(t, a=FIN(g, 3) + 0.25, b=INI("leyenda", 0) - 0.15):
    """Parpadeo de la lámpara entre el gancho y la leyenda."""
    if t < a or t > b + 0.9:
        return 1.0
    if t < b:
        return 1 - 0.7 * T.sm(T.pr(t, a, a + 0.2))
    e = t - b
    return (0.3 + 0.7 * T.sm(T.pr(e, 0, 0.5))) * (0.3 if (0.12 < e < 0.2 or 0.36 < e < 0.42) else 1.0)


T.LUZ_FX.append(_apagon)
snd(INI("leyenda", 0) - 0.15, "match", 0.4)

# ============================================================================================ LEYENDA
le = "leyenda"
P_FASC = portal_pz("fascinados", "«QUEDABAN FASCINADOS»", 1350, -2250, -3, INI(le, 0) - 0.5)
N_NAU = Pz(T.nota("NÁUSEAS", 250, (0.70, 0.92, 0.55), 52), 1980, -2620, 5, t_in=ww(le, 1, "nauseas") - 0.15, chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
N_PES = Pz(T.nota("PESADILLAS", 250, (0.55, 0.85, 0.95), 46), 2290, -2560, -4, t_in=ww(le, 1, "pesadillas") - 0.15, chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
N_LAG = Pz(T.nota("LAGUNAS DE MEMORIA", 250, (0.95, 0.55, 0.60), 44), 2600, -2620, 6, t_in=ww(le, 1, "lagunas") - 0.15, chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
P_PESA = portal_pz("pesadilla", "SIN DORMIR DURANTE SEMANAS", 2280, -1900, 2, INI(le, 1) - 0.2)
P_HOM = portal_pz("hombres", "HOMBRES DE TRAJE OSCURO", 3200, -2300, -2, INI(le, 3) - 0.5, chinchetas=((0, None, (0.05, 0.05, 0.06)),))
P_VAC = portal_pz("vacio", "UN DÍA, TODAS DESAPARECIERON", 3250, -1500, 3, INI(le, 4) - 0.5)
N_SEG = Pz(T.nota("«según la historia»", 240, px=40), 800, -1750, -7, t_in=INI(le, 0) + 0.2, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)

TX(R(pk(le, 0, "los", "fascinados"), cy=900, px=92), ww(le, 0, "los"), FIN(le, 0) + 0.2)
TX(R(pk(le, 1, "lagunas", "memoria"), cy=900, px=92), ww(le, 1, "lagunas"), FIN(le, 1) + 0.2)
TX(R(pk(le, 2, "perdian", "semanas"), cy=900, px=84), ww(le, 2, "perdian"), FIN(le, 2) + 0.2)
TX(R(pk(le, 3, "sin", "dinero"), cy=900, px=92), ww(le, 3, "sin"), FIN(le, 3) + 0.1)
TX(R(pk(le, 4, "sin", "tornillo"), cy=900, px=88), ww(le, 4, "sin"), FIN(le, 4) + 0.2)

K(INI(le, 0) - 0.1, 700, -1500, 0.8, -2, 5, 6)
DENTRO(P_FASC, INI(le, 0) + 0.5, ww(le, 0, "quedaban"), FIN(le, 0) + 0.1)
K(INI(le, 1) + 0.5, 2100, -2150, 0.85, 1, 3, 4)
K(ww(le, 1, "nauseas") + 0.3, 2280, -2330, 1.05, 2, 0, 0)
DENTRO(P_PESA, ww(le, 1, "pesadillas") + 0.5, ww(le, 1, "lagunas"), FIN(le, 2) + 0.1, 1.5)
K(INI(le, 3) + 0.3, 2900, -2250, 1.05, -1, 3, 5)
DENTRO(P_HOM, INI(le, 3) + 1.0, ww(le, 3, "abrian") - 0.2, FIN(le, 3) + 0.1)
K(INI(le, 4) + 0.2, 3230, -1850, 1.05, 2, -3, 2)
DENTRO(P_VAC, INI(le, 4) + 0.7, ww(le, 4, "desaparecieron") - 0.3, FIN(le, 4) + 0.2)

# ============================================================================================ CASOS REALES
c = "casos"
for k, pz_ in enumerate((P_FASC, P_PESA, P_HOM, P_VAC)):          # la leyenda, atada al centro
    T.Hilo(pz_, P_POLY, INI(c, 0) + 0.15 * k, 1.1, "rojo", sonido=(k == 0))
A81B = Pz(PZ.anio_card(1981, 420, 31, sub="PORTLAND"), 3350, -520, -4, t_in=ww(c, 0, "año") - 0.3)
circulo(A81B, ww(c, 0, "elegido"), 0.6, 0, 30, 190, 120)
J1 = Pz(T.silueta_card("CHICO · 12 AÑOS", "SIN FOTO", 400), 3950, -640, 3, t_in=ww(c, 1, "dos") - 0.2, chinchetas=((0, None, AZUL),))
J2 = Pz(T.silueta_card("OTRO ADOLESCENTE", "SIN FOTO", 400, 6), 4450, -600, -4, t_in=ww(c, 1, "dos") + 0.15, chinchetas=((0, None, AZUL),))
N_MAL = Pz(T.nota("se sintieron mal JUGANDO", 260, (0.55, 0.85, 0.95), 42), 4200, -1080, 4, t_in=ww(c, 1, "sintieron"), chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
P_MAR = portal_pz("maraton", "28 HORAS SEGUIDAS", 3800, 120, -2, INI(c, 2) - 0.4)
P_AST = Pz(pol("asteroids", "EL JUEGO DEL RÉCORD", 420, 0.75, (0.45, 0.45)), 4500, 60, 5, t_in=ww(c, 2, "asteroids") - 0.35)
P_MIG = portal_pz("migrana", "MIGRAÑA", 3900, 880, 2, INI(c, 3) - 0.4)
L_TEMP = Pz(T.hoja_img("tempest_logo", 130), 4560, 720, -5, 1.25, t_in=ww(c, 3, "tempest") - 0.3, chinchetas=((0, None, AMAR),))
RC1 = Pz(PZ.recorte("DOS CHICOS ENFERMAN TRAS HORAS EN LOS RECREATIVOS", 520, 3, True, 38), 5100, -560, 3, t_in=ww(c, 4, "periodicos") - 0.3)
P_RED = portal_pz("redada", "AGENTES FEDERALES EN LOS SALONES", 5150, 330, -3, ww(c, 4, "agentes") - 1.0)
F_FBI = Pz(T.ficha("Redadas en salones de Portland por máquinas trucadas para apostar. Decenas de arrestos.", 540, 320, titulo="1981 · APUESTAS", px=28),
           5750, -100, 4, t_in=ww(c, 5, "apostar") - 0.2, chinchetas=((0, None, AMAR),))
P_COR = portal_pz("corazon", "1982 · OTRO ESTADO", 5350, 1100, 2, INI(c, 6) - 0.4)
T.Hilo(J1, P_MAR, ww(c, 2, "veintiocho") - 0.6, 0.8, "azul")
T.Hilo(J2, P_MIG, INI(c, 3) + 0.1, 0.8, "azul")
T.Hilo(RC1, J1, ww(c, 4, "contaron"), 0.9, "blanco")

TX(R(pk(c, 0, "no", "azar"), cy=900, px=92), ww(c, 0, "no"), FIN(c, 0) + 0.2)
TX(S([("Dos", ww(c, 1, "dos")), ("adolescentes", ww(c, 1, "adolescentes")), ("de", ww(c, 1, "portland") - 0.1), ("Portland", ww(c, 1, "portland"))], W / 2, 900, 110),
   ww(c, 1, "dos"), FIN(c, 1) + 0.2)
TX(N("28 HORAS", W / 2, 190, 150, ww(c, 2, "veintiocho"), (0.95, 1.0, 0.1)), ww(c, 2, "veintiocho"), ww(c, 2, "asteroids") - 0.3, False)
TX(R(pk(c, 3, "que", "moverse"), cy=900, px=84), ww(c, 3, "que"), FIN(c, 3) + 0.2)
TX(R(pk(c, 5, "no", "maldito"), cy=180, px=84), INI(c, 5), ww(c, 5, "buscaban", 1) + 0.2, False)
TX(R(pk(c, 6, "el", "mas"), cy=900, px=80), ww(c, 6, "el"), FIN(c, 6) + 0.2)
FOTO_CRED("asteroids", ww(c, 2, "asteroids"), FIN(c, 2) + 0.3)
FOTO_CRED("tempest_logo", ww(c, 3, "tempest"), ww(c, 3, "tempest") + 2.2)

K(INI(c, 0) + 0.4, 1900, -1100, 0.36, 0, 7, 3)
K(ww(c, 0, "año") + 0.5, 3350, -520, 1.3, -3, 2, -3, modo="suave")
K(FIN(c, 0) + 0.2, 3400, -540, 1.5, -3, 0, 0)
K(ww(c, 1, "dos") + 0.6, 4150, -560, 1.05, 0, 3, 4)
K(FIN(c, 1), 4220, -520, 1.15, 1, 0, 0)
DENTRO(P_MAR, INI(c, 2) + 0.5, ww(c, 2, "veintiocho") + 0.2, ww(c, 2, "asteroids") - 0.5)
K(ww(c, 2, "asteroids") + 0.35, 4480, 80, 1.5, 4, 0, 0, modo="suave")
K(FIN(c, 2) + 0.1, 4350, 150, 1.3, 2, 2, -2)
DENTRO(P_MIG, INI(c, 3) + 0.6, ww(c, 3, "migra") - 0.2, ww(c, 3, "tempest") - 0.35)
K(ww(c, 3, "tempest") + 0.45, 4540, 730, 1.9, -4, 0, 0, modo="suave")
K(ww(c, 3, "formas"), 4250, 800, 1.25, 0, 3, 3)
K(FIN(c, 3) + 0.1, 3950, 860, 1.5, 2, 0, 0)
K(ww(c, 4, "periodicos") + 0.5, 5080, -540, 1.35, 2, 2, -3, modo="suave")
DENTRO(P_RED, ww(c, 4, "agentes") - 0.3, ww(c, 4, "entraron"), FIN(c, 5) - 0.6)
K(FIN(c, 5) + 0.3, 5650, -60, 1.25, 3, 2, -4)
DENTRO(P_COR, INI(c, 6) + 0.8, ww(c, 6, "murio") - 0.4, FIN(c, 6) + 0.1)

# ============================================================================================ GOBIERNO
gb = "gobierno"
I_GOB = Pz(PZ.icono_card("placa", 300, 3, pie="EL GOBIERNO"), 2500, 1750, -4, t_in=ww(gb, 0, "gobierno") - 0.3, chinchetas=((0, None, AMAR),))
T.Hilo(P_POLY, I_GOB, ww(gb, 0, "hilo") - 0.2, 1.6, "amarillo", etiqueta=T.ficha("¿?", 120, 80, rayada=False, px=40))
N_HILO = Pz(T.nota("otro hilo suelto…", 260, (0.55, 0.85, 0.95), 46), 2020, 1560, -6, t_in=ww(gb, 0, "hilo") - 0.1, chinchetas=((0, None, None),),
            entrada="aparece", dur=0.25)
HV_G = Pz(PZ.hoja_vector(2, 440, 2), 3020, 1340, 5, t_in=ww(gb, 0, "videojuegos") - 0.3)
P_BZ = Pz(pol("battlezone_cab", "JUEGO DE TANQUES · ATARI", 440, 0.72, (0.5, 0.35)), 4350, 1850, 4, t_in=ww(gb, 1, "atari") - 0.35)
I_EJ = Pz(PZ.icono_card("placa", 260, 5, pie="EJÉRCITO DE EE. UU."), 3050, 1620, 5, t_in=ww(gb, 1, "ejercito") - 0.3)
P_TAN = portal_pz("tanque", "DE JUEGO A SIMULADOR", 3600, 1900, -2, INI(gb, 1) - 0.2)
T.Punteada(I_EJ, P_BZ, ww(gb, 1, "encargo"), color=(1.0, 0.85, 0.45), curva=0.10, dur=1.2, paquetes=4, vel=0.3, grosor=7.0)
H_BR = Pz(T.hoja_img("bradley1", 420), 4300, 2620, -3, t_in=ww(gb, 2, "prensa") - 0.3, chinchetas=((0, None, VERDE),))
RC2 = Pz(PZ.recorte("EL EJÉRCITO QUIERE ENTRENAR CON UN VIDEOJUEGO", 520, 5, False, 38), 3550, 2700, 3, t_in=ww(gb, 2, "conto") - 0.4)
T.Hilo(RC2, H_BR, ww(gb, 2, "mano") - 0.3, 0.8, "verde")
P_ROT = Pz(T.silueta_card("ED ROTBERG", "SIN FOTO LIBRE", 440, 7), 2750, 2600, -3, 1.05, t_in=ww(gb, 3, "ed") - 0.35)
F_ROT = Pz(T.ficha("Programador de Atari. Hizo el juego de tanques. No quería la versión militar.", 500, 300, titulo="ED ROTBERG", px=28), 2150, 2350, 4,
           t_in=ww(gb, 3, "no") - 0.1)
P_PRU = portal_pz("prueba", "PRUEBAS EN SALONES REALES", 2050, 3050, 2, INI(gb, 4) - 0.4)
H_CREA = T.Hilo(P_ROT, P_POLY, ww(gb, 5, "señalado") - 0.2, 1.5, "rojo", corte=ww(gb, 6, "nego") + 0.1, etiqueta=T.ficha("¿CREADOR?", 230, 80, rayada=False, px=30))
sello_en(P_ROT, "LO NIEGA", ww(gb, 6, "nego") + 0.25, 0, -40, -9, 60)
C_ROT = Pz(PZ.tarjeta_cita("Nunca vi ni oí hablar de un juego llamado Polybius.", "— Ed Rotberg", 640, 38), 2000, 1850, -3, t_in=ww(gb, 6, "dijo") - 0.2,
           chinchetas=((0, None, AZUL),))

TX(R(pk(gb, 0, "el", "videojuegos"), cy=900, px=86), ww(gb, 0, "el"), FIN(gb, 0) + 0.2)
TX(R(pk(gb, 2, "ya", "mano"), cy=900, px=92), ww(gb, 2, "ya"), FIN(gb, 2) + 0.2)
TX(S([("Ed", ww(gb, 3, "ed")), ("Rotberg", ww(gb, 3, "rotberg"))], W / 2, 900, 130), ww(gb, 3, "ed"), FIN(gb, 3) + 0.2)
TX(R(pk(gb, 4, "sin", "nadie"), cy=900, px=92), ww(gb, 4, "sin"), FIN(gb, 4) + 0.1)
TX(R(pk(gb, 5, "el", "polybius"), cy=900, px=86), ww(gb, 5, "el"), FIN(gb, 5) + 0.1)
FOTO_CRED("battlezone_cab", ww(gb, 1, "atari"), ww(gb, 1, "atari") + 2.0)
FOTO_CRED("bradley1", ww(gb, 2, "prensa"), FIN(gb, 2))
TX(CRED("Captura real del simulador militar (dominio público)", ww(gb, 2, "prensa") + 0.2, FIN(gb, 2), y=980), ww(gb, 2, "prensa") + 0.2, FIN(gb, 2), False)

K(INI(gb, 0) + 0.3, 3900, 900, 0.5, 0, 5, -5)
K(ww(gb, 0, "gobierno") + 0.4, 2400, 1720, 1.1, -3, 2, 3, modo="suave")
K(FIN(gb, 0) + 0.2, 2650, 1800, 0.95, -1, 2, 2)
K(ww(gb, 1, "ejercito") + 0.5, 3050, 1640, 1.4, 4, 0, 0)
K(ww(gb, 1, "atari") + 0.5, 4330, 1850, 1.35, 3, 0, -3, modo="suave")
DENTRO(P_TAN, ww(gb, 1, "convertir") + 0.2, ww(gb, 1, "tanques"), FIN(gb, 1) + 0.1)
K(ww(gb, 2, "prensa") + 0.7, 4280, 2620, 1.6, -3, 0, 0, modo="suave")
K(ww(gb, 2, "conto") + 0.6, 3700, 2690, 1.25, 1, 2, 3)
K(FIN(gb, 2) + 0.1, 3900, 2660, 1.05, 0, 3, 0)
K(ww(gb, 3, "ed") + 0.4, 2750, 2600, 1.5, -3, 0, 0, modo="suave")
K(FIN(gb, 3) + 0.1, 2450, 2480, 1.2, 0, 2, 4)
DENTRO(P_PRU, INI(gb, 4) + 0.6, ww(gb, 4, "probaba") + 0.5, FIN(gb, 4) + 0.1)
K(INI(gb, 5) + 0.5, 2750, 2600, 1.3, -3, 0, 0)
K(ww(gb, 5, "señalado") + 0.9, 1400, 1300, 0.6, -2, 5, 5)
K(FIN(gb, 5) + 0.1, 300, 250, 0.85, -1, 3, 3)
K(ww(gb, 6, "nego") + 0.5, 1700, 1650, 0.7, 0, 4, 3)
K(ww(gb, 6, "dijo") + 0.6, 2000, 1850, 1.45, -3, 0, 0, modo="suave")
K(FIN(gb, 6) + 0.2, 2020, 1870, 1.65, -3, 0, 0)
