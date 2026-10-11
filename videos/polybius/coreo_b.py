# -*- coding: utf-8 -*-
"""Coreografía B: PRUEBAS, ORIGEN, POR QUÉ y CIERRE.
Zonas: pruebas abajo-centro (0, 2500) · origen abajo-izquierda (-3700, 2300) · por qué izquierda (-4000, -200) · cierre en el centro."""
import tablero as T
import piezas as PZ
from coreo_comun import *  # noqa: F401,F403
from kit import CREDITOS
from coreo_a import Pz, pol, portal_pz, ROJA, AZUL, AMAR, VERDE, P_POLY, P_ROT, RC1, J1, P_FASC, P_HOM

# ============================================================================================ PRUEBAS
pb = "pruebas"
V1 = Pz(PZ.vacia_card("FOTO DE 1981", 400, 40), -800, 2050, -4, t_in=ww(pb, 1, "foto") - 0.3)
V2 = Pz(PZ.vacia_card("COPIA DEL PROGRAMA", 400, 41), -250, 2120, 3, t_in=ww(pb, 1, "copia") - 0.3)
V3 = Pz(PZ.vacia_card("REGISTRO DE LA EMPRESA", 400, 42), 300, 2060, -2, t_in=ww(pb, 1, "registro") - 0.3)
for k, v in enumerate((V1, V2, V3)):
    tache(v, (ww(pb, 1, "foto"), ww(pb, 1, "copia"), ww(pb, 1, "registro"))[k] + 0.45, 0.4)
F_SINN = Pz(T.ficha("Sinne = sentidos\nlöschen = borrar", 620, 360, titulo="«SINNESLÖSCHEN»", px=40), 1000, 2250, 3, t_in=ww(pb, 2, "nombre") - 0.3,
            chinchetas=((0, None, AMAR),))
subraya(F_SINN, ww(pb, 2, "borrar"), -260, 60, 100)
N_ALE = Pz(T.nota("alemán que no suena natural", 270, (0.95, 0.55, 0.60), 42), 1500, 2000, 6, t_in=ww(pb, 2, "aleman") - 0.2, chinchetas=((0, None, None),),
           entrada="aparece", dur=0.25)
P_BUSTO = Pz(pol("polibio_busto", "POLIBIO · c. 200–118 a. C.", 480, 0.8, (0.5, 0.32)), -750, 2950, -3, 1.05, t_in=ww(pb, 3, "historiador") - 0.5)
H_1548 = Pz(T.hoja_img("polibio_1548", 620), -120, 3000, 3, t_in=ww(pb, 3, "griego"), chinchetas=((0, None, AZUL),))
N_TEST = Pz(T.nota("exigía TESTIGOS de cada hecho", 280, px=44), 420, 2800, -5, t_in=ww(pb, 3, "testigos") - 0.2, chinchetas=((0, None, None),),
            entrada="aparece", dur=0.25)
T.Hilo(P_BUSTO, P_POLY, ww(pb, 4, "una") - 0.1, 1.2, "amarillo", etiqueta=T.ficha("IRONÍA", 200, 80, rayada=False, px=32))
P_HEM = portal_pz("hemeroteca", "LA PRENSA DE 1981", 1500, 3000, -2, INI(pb, 5) - 0.6)
T.Hilo(P_HEM, RC1, ww(pb, 6, "si"), 1.4, "blanco", sonido=False)

TX(Q([[("¿Dónde", ww(pb, 0, "donde")), ("está", ww(pb, 0, "esta"))], [("la", ww(pb, 0, "la")), ("máquina", ww(pb, 0, "maquina"))]], ww(pb, 0, "donde"),
     cy=H * 0.84, px=96), ww(pb, 0, "donde"), FIN(pb, 0) + 0.3)
TX(R(pk(pb, 1, "no", "sola"), cy=180, px=92), INI(pb, 1), ww(pb, 1, "foto") + 0.3, False)
TX(R(pk(pb, 2, "borrar", "sentidos"), cy=900, px=96), ww(pb, 2, "borrar"), ww(pb, 2, "aleman") + 0.6)
TX(S([("Polibio", ww(pb, 3, "polybius"))], W / 2, 950, 120), ww(pb, 3, "polybius"), ww(pb, 3, "testigos") + 0.2)
TX(R(pk(pb, 4, "una", "perfecta"), cy=170, px=96), INI(pb, 4), FIN(pb, 4) + 0.2, False)
FOTO_CRED("polibio_busto", ww(pb, 3, "historiador"), FIN(pb, 3))

K(INI(pb, 0) - 0.2, 900, 900, 0.5, 0, 6, 0)
K(ww(pb, 0, "donde") + 0.4, 0, 270, 0.72, -1.5, 2, 0, modo="suave")
K(FIN(pb, 0) + 0.25, 0, 300, 0.76, -1.5, 1, 0, modo="suave")
K(INI(pb, 1) + 1.5, -300, 1500, 0.7, 0, 5, 3)
K(ww(pb, 1, "foto") + 0.3, -780, 2050, 1.35, -3, 0, 4, modo="suave")
K(ww(pb, 1, "copia") + 0.4, -250, 2120, 1.35, 2, 0, 0)
K(ww(pb, 1, "registro") + 0.5, 300, 2060, 1.35, -1, 0, -3)
K(FIN(pb, 1) + 0.1, -200, 2100, 0.85, 0, 3, 0)
K(ww(pb, 2, "nombre") + 0.6, 1000, 2250, 1.4, 3, 0, 0, modo="suave")
K(ww(pb, 2, "aleman") + 0.5, 1250, 2130, 1.2, 4, 2, -3)
K(FIN(pb, 2) + 0.1, 1300, 2120, 1.3, 4, 0, 0)
K(ww(pb, 3, "historiador") + 0.4, -620, 3070, 0.95, -3, 0, 3, modo="suave")
K(ww(pb, 3, "testigos") + 0.2, -100, 2950, 1.1, 1, 2, 0)
K(FIN(pb, 3), 250, 2850, 1.3, -3, 0, -2)
K(INI(pb, 4) + 0.9, -350, 1750, 0.55, -1, 6, 0)
K(FIN(pb, 4) + 0.1, 300, 2100, 0.6, 0, 4, -3)
DENTRO(P_HEM, INI(pb, 5) + 0.5, ww(pb, 5, "periodico") + 0.6, FIN(pb, 6) - 0.5)

# ============================================================================================ ORIGEN
o = "origen"
A81C = Pz(PZ.anio_card(1981, 420, 32), -2700, 1650, 4, t_in=INI(o, 1) - 0.45)
tache(A81C, ww(o, 1, "mil") + 0.3, 0.45)
CAL = Pz(PZ.calendario(2, 2000, (6,), 440), -3450, 1600, -3, t_in=ww(o, 2, "seis") - 0.35, chinchetas=((0, None, AZUL),))
P_WEB = portal_pz("web2000", "UNA FICHA EN UNA WEB · AÑO 2000", -4200, 2100, 2, ww(o, 2, "sitio") - 1.0, 620)
F_DER = Pz(T.ficha("Dice «© 1981».\nNo consta ningún registro de esos derechos.", 520, 300, titulo="DERECHOS DE AUTOR", px=30), -3350, 2420, -2,
           t_in=ww(o, 5, "registro") - 0.5)
sello_en(F_DER, "SIN REGISTRO", ww(o, 5, "derechos") + 0.1, 30, 60, -8, 48)
N98 = Pz(T.nota("fecha de la ficha: 1998", 280, px=46), -2780, 2500, 5, t_in=ww(o, 5, "fecha") - 0.2, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
sello_en(N98, "¿FALSA?", ww(o, 5, "falsa") - 0.1, 0, 100, -10, 46)
P_VIA = portal_pz("viaje", "«MÁS DATOS TRAS EL VIAJE»", -4350, 3000, -3, INI(o, 6) - 0.4)
P_REV = Pz(PZ.revista(), -3450, 3250, 3, 0.95, t_in=ww(o, 7, "revista") - 0.4, chinchetas=((0, None, AZUL),))
N_1A = Pz(T.nota("1.ª mención IMPRESA", 250, (0.70, 0.92, 0.55), 46), -2950, 3050, -5, t_in=ww(o, 7, "primera") - 0.1, chinchetas=((0, None, None),),
          entrada="aparece", dur=0.25)
I_USU = Pz(PZ.icono_card("testigo", 300, 9, pie="UN USUARIO · 2006"), -2500, 3350, 4, t_in=ww(o, 8, "usuario") - 0.35)
sello_en(I_USU, "SIN PRUEBAS", ww(o, 8, "sin") + 0.1, 0, 20, -9, 54)
T.Hilo(CAL, P_REV, ww(o, 7, "dos") - 0.2, 1.0, "azul", etiqueta=T.ficha("3 AÑOS", 190, 80, rayada=False, px=30))
T.Hilo(P_REV, I_USU, ww(o, 8, "dos") - 0.2, 0.9, "azul")
T.Hilo(CAL, P_POLY, ww(o, 2, "febrero"), 1.6, "rojo", etiqueta=T.ficha("PRIMER RASTRO", 260, 80, rayada=False, px=28))

TX(Q([[("¿Cuándo", ww(o, 0, "cuando")), ("aparece", ww(o, 0, "aparece"))], [("realmente", ww(o, 0, "realmente")), ("Polybius", ww(o, 0, "polybius"))]],
     ww(o, 0, "cuando"), cy=H * 0.78, px=96), ww(o, 0, "cuando"), FIN(o, 0) + 0.25)
TX(S([("6", ww(o, 2, "seis")), ("febrero", ww(o, 2, "febrero")), ("2000", ww(o, 2, "dos"))],
     W / 2, 900, 120), ww(o, 2, "seis"), ww(o, 2, "sitio") + 0.3)
TX(R(pk(o, 5, "parece", "falsa"), cy=900, px=100), ww(o, 5, "parece"), FIN(o, 5) + 0.2)
TX(R(pk(o, 6, "nunca", "llegaron"), cy=900, px=100), ww(o, 6, "nunca"), FIN(o, 6) + 0.1)
TX(N("2003", 380, 300, 170, ww(o, 7, "dos"), (0.95, 1.0, 0.1)), ww(o, 7, "dos"), ww(o, 7, "primera"), False)
TX(N("2006", 380, 300, 170, ww(o, 8, "dos"), (0.95, 1.0, 0.1)), ww(o, 8, "dos"), ww(o, 8, "usuario") + 1.2, False)
TX(R(pk(o, 8, "sin", "prueba"), cy=900, px=96), ww(o, 8, "sin"), FIN(o, 8) + 0.2)

K(INI(o, 0) + 0.2, 500, 3700, 0.45, 0, 5, 5)
K(FIN(o, 0) + 0.1, -1300, 3400, 0.5, -1, 4, 6)
K(ww(o, 1, "mil") + 0.3, -2700, 1650, 1.45, 4, 0, 0, modo="suave")
K(ww(o, 2, "seis") + 0.5, -3450, 1600, 1.4, -3, 0, 3, modo="suave")
K(ww(o, 2, "febrero") + 1.0, -3500, 1650, 1.2, -2, 2, 3)
DENTRO(P_WEB, ww(o, 2, "sitio") - 0.2, ww(o, 2, "web") + 0.5, FIN(o, 4) + 0.1)
K(ww(o, 5, "registro") + 0.5, -3350, 2420, 1.4, -2, 0, 0, modo="suave")
K(ww(o, 5, "fecha") + 0.4, -2900, 2480, 1.3, 3, 0, -3)
K(FIN(o, 5) + 0.1, -2780, 2500, 1.6, 5, 0, 0)
DENTRO(P_VIA, INI(o, 6) + 0.5, ww(o, 6, "viaje") - 0.2, FIN(o, 6) + 0.1)
K(ww(o, 7, "revista") + 0.4, -3450, 3250, 1.25, 3, 0, 0, modo="suave")
K(FIN(o, 7), -3200, 3150, 1.15, 0, 2, -3)
K(ww(o, 8, "usuario") + 0.4, -2500, 3350, 1.5, 4, 0, 0, modo="suave")
K(FIN(o, 8) + 0.1, -2550, 3350, 1.7, 4, 0, 0)

# ============================================================================================ POR QUÉ
q = "porque"
P_PAD = portal_pz("padres", "EL MIEDO DE LOS PADRES", -4650, -700, -3, INI(q, 1) - 0.5)
RC3 = Pz(PZ.recorte("¿PUEDEN LAS PANTALLAS PROVOCAR ATAQUES?", 520, 7, True, 40), -3800, -850, 3, t_in=ww(q, 2, "ataques") - 0.4)
I_TV = Pz(PZ.icono_card("tele", 280, 4, pie="PANTALLAS"), -3250, -620, -5, t_in=ww(q, 2, "pantallas") - 0.3)
P_MEN = portal_pz("mente", "RUMORES DE CONTROL MENTAL", -4500, 150, 2, INI(q, 3) - 0.5)
MIEDOS = [T.Hilo(pz_, P_POLY, ww(q, 4, "juntaba") + 0.25 * k, 1.3, "rojo", sonido=(k == 0)) for k, pz_ in enumerate((P_PAD, RC3, P_MEN))]
L_TEMP2 = Pz(T.hoja_img("tempest_logo", 130), -2900, 420, 4, 1.2, t_in=ww(q, 5, "geometricas") - 0.5, chinchetas=((0, None, AMAR),))
HV1 = Pz(PZ.hoja_vector(3, 460, 1), -3350, 330, -4, t_in=ww(q, 5, "juegos") - 0.2)
HV2 = Pz(PZ.hoja_vector(5, 460, 0), -2450, 520, 5, t_in=ww(q, 5, "imagenes") - 0.3)
N_INS = Pz(T.nota("¿inspiración?", 240, px=48), -2900, 760, -4, t_in=ww(q, 5, "inspiraron"), chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
P_REC = portal_pz("recreacion", "UN HOMENAJE GRATUITO · 2007", -3700, 1000, -2, INI(q, 6) - 0.5)
I_SER = Pz(PZ.icono_card("tele", 280, 11, pie="SERIES"), -2250, -980, -4, t_in=ww(q, 7, "series") - 0.3)
I_MUS = Pz(PZ.icono_card("musica", 280, 12, pie="VIDEOCLIPS"), -1900, -1040, 3, t_in=ww(q, 7, "videoclips") - 0.3)
I_VJ = Pz(PZ.icono_card("mando", 280, 13, pie="VIDEOJUEGO · 2017"), -1550, -970, -2, t_in=ww(q, 7, "videojuego") - 0.3)
F_ADM = Pz(T.ficha("Su creador admitió que él mismo había alimentado el mito.", 500, 280, titulo="2017", px=30), -1050, -1000, 3, t_in=ww(q, 7, "admitio") - 0.3,
           chinchetas=((0, None, AMAR),))
for k, pz_ in enumerate((I_SER, I_MUS, I_VJ)):
    T.Hilo(pz_, P_POLY, ww(q, 7, "admitio") + 0.2 * k, 1.0, "verde", sonido=(k == 0))

TX(R(pk(q, 0, "la", "bien"), cy=900, px=88), ww(q, 0, "la"), FIN(q, 0) + 0.2)
TX(R(pk(q, 4, "todos", "maquina"), cy=900, px=84), ww(q, 4, "todos"), FIN(q, 4) + 0.2)
TX(R(pk(q, 5, "juegos", "reales"), cy=900, px=96), ww(q, 5, "juegos"), ww(q, 5, "geometricas"))
TX(R(pk(q, 7, "el", "mismo"), cy=900, px=88), ww(q, 7, "el"), FIN(q, 7) + 0.2)
FOTO_CRED("tempest_logo", ww(q, 5, "geometricas"), ww(q, 5, "geometricas") + 2.5)

K(INI(q, 0) + 0.2, -2600, 2400, 0.5, 0, 5, 6)
K(FIN(q, 0) + 0.1, -3900, 600, 0.45, -1, 6, 4)
DENTRO(P_PAD, INI(q, 1) + 0.6, ww(q, 1, "padres") + 0.4, FIN(q, 1) + 0.1)
K(ww(q, 2, "ataques") + 0.5, -3800, -850, 1.35, 3, 0, 0, modo="suave")
K(ww(q, 2, "pantallas") + 0.3, -3400, -720, 1.2, 0, 2, -4)
K(FIN(q, 2) + 0.1, -3300, -650, 1.4, -4, 0, 0)
DENTRO(P_MEN, INI(q, 3) + 0.5, ww(q, 3, "experimentos") + 0.3, FIN(q, 3) + 0.1)
K(ww(q, 4, "juntaba") + 0.3, -3900, -350, 0.5, 0, 5, 5)
K(ww(q, 4, "miedos") + 0.5, -1700, -200, 0.45, 0, 6, 6)
K(FIN(q, 4) + 0.1, -250, 190, 0.8, -1.5, 3, 3)
K(ww(q, 5, "juegos") + 0.5, -3350, 340, 1.25, -3, 2, 4, modo="suave")
K(ww(q, 5, "geometricas") + 0.5, -2900, 430, 1.6, 4, 0, 0)
K(ww(q, 5, "imagenes") + 0.5, -2470, 520, 1.3, 4, 0, -3)
K(FIN(q, 5) + 0.1, -2800, 600, 1.0, 0, 3, 0)
DENTRO(P_REC, INI(q, 6) + 0.5, ww(q, 6, "gratuito") - 0.3, FIN(q, 6) + 0.1)
K(ww(q, 7, "series") + 0.3, -2250, -960, 1.3, -3, 2, 4, modo="suave")
K(ww(q, 7, "videoclips") + 0.3, -1900, -1010, 1.3, 2, 0, 0)
K(ww(q, 7, "videojuego") + 0.5, -1560, -960, 1.3, -2, 0, -3)
K(ww(q, 7, "admitio") + 0.6, -1080, -960, 1.35, 3, 0, 0, modo="suave")
K(FIN(q, 7) + 0.1, -900, -700, 0.75, 0, 3, -4)

# ============================================================================================ CIERRE
z = "cierre"
sello_en(P_POLY, "0 PRUEBAS", ww(z, 0, "prueba") + 0.1, 0, -40, -7, 84, color=(1.0, 0.30, 0.25), op=1.0)
N_INV = Pz(T.nota("una INVENCIÓN (y de las mejores)", 290, px=44), 720, -330, 6, t_in=ww(z, 1, "invencion") - 0.2, chinchetas=((0, None, None),), entrada="aparece",
           dur=0.25)

TX(N("0 PRUEBAS", W / 2, 190, 150, ww(z, 0, "prueba"), (0.95, 1.0, 0.1)), ww(z, 0, "prueba"), FIN(z, 0) + 0.2, False)
TX(R(pk(z, 1, "una", "internet", 1), cy=170, px=80), ww(z, 1, "una", 1), FIN(z, 1) + 0.2, False)
TX(R(pk(z, 2, "pero", "pregunta"), cy=900, px=100), INI(z, 2), FIN(z, 2) + 0.2)
TX(Q([[("¿Por", ww(z, 4, "por")), ("qué", ww(z, 4, "que")), ("seguimos", ww(z, 4, "seguimos"))], [("buscando", ww(z, 4, "buscando")), ("esa", ww(z, 4, "esa")),
                                                                                                ("máquina", ww(z, 4, "maquina"))]],
     ww(z, 4, "por"), cy=H * 0.80, px=90), ww(z, 4, "por"), FIN(z, 4) + 1.2)


def _penumbra(t, a=INI(z, 2) - 0.1, b=INI(z, 3) + 1.2):
    """La lámpara baja antes de la última pregunta."""
    if t < a:
        return 1.0
    if t < b:
        return 1 - 0.55 * T.sm(T.pr(t, a, a + 0.8))
    return 0.45 + 0.55 * T.sm(T.pr(t, b, b + 0.6))


T.LUZ_FX.append(_penumbra)

K(INI(z, 0) + 0.3, -400, 100, 0.55, 0, 5, 0)
K(ww(z, 0, "prueba") + 0.4, 0, 250, 0.24, 0, 7, 0, modo="suave")
K(FIN(z, 0) + 0.2, 300, 300, 0.2, 0, 7, 2)
K(ww(z, 1, "invencion") + 0.4, 640, -250, 1.15, 3, 2, -3)
K(FIN(z, 1) + 0.1, 520, -200, 1.0, 0, 2, 0)
K(FIN(z, 2) + 0.1, 0, 180, 0.85, -1.5, 0, 0, modo="suave")
DENTRO(P_POLY, INI(z, 3) + 0.2, ww(z, 3, "fabrico"), FIN(z, 4) + 1.6)

# ============================================================================================ CRÉDITOS (sobre el almacén a oscuras)
_T_CR = FIN(z, 4) + 2.0


def _oscurece(lz, t):
    lz *= 1.0 - 0.72 * T.sm(T.pr(t, _T_CR - 0.3, _T_CR + 0.7))


TX(_oscurece, _T_CR - 0.3, TOTAL + 1.0, False)
TX(CREDITOS("Polybius: el videojuego que nunca existió", [
    "Fuentes: Wikipedia («Polybius (urban legend)») · Skeptoid (Brian Dunning) · Inverse · prensa de Oregón de 1981",
    "Fotos (Wikimedia Commons): Steve Morgan · Joho345 · Piotrus · Manfred Werner (Tsui) · Atari · US Army",
    "No existe ninguna foto de una máquina Polybius de 1981: aquí no se muestra ninguna.",
    "Las pantallas, la página web y los periódicos que aparecen son recreaciones dibujadas, no documentos reales.",
    "Animaciones y gráficos: producción propia · Música: Lyria"], _T_CR),
   _T_CR, TOTAL + 1.0, False)
