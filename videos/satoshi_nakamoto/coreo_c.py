# -*- coding: utf-8 -*-
"""Coreografía C: LE ROUX (entre Todd y Back), ARCHIVO del gobierno y ESPEJO de Budapest (antes del cierre), y el GANCHO:
un «flash-forward» a oscuras con linterna sobre el tablero ya resuelto (piezas y hilos en modo `teaser`), que termina en el título."""
import tablero as T
import piezas as PZ
import piezas2 as P2
from coreo_comun import *  # noqa: F401,F403
from kit import CREDITOS
from coreo_a import (Pz, pol, portal_pz, ROJA, AZUL, AMAR, VERDE, P_SAT, P_BOVEDA, P_BACK, P_WP, P_HEX, P_HAL, Q_OTRAS, F_CORREO, P_TIMES,
                     P_GRAF, RAFAGA)
from coreo_b import (P_REV, P_DORIAN, P_SZABO, P_WRIGHT, P_TODD, P_TELE, P_ROLLS, P_LEN, P_F16, P_CARR, Q_DOR, P_ESTAT)

# ============================================================================================ LE ROUX
lr = "leroux"
P_LEROUX = Pz(pol("le_roux", "PAUL LE ROUX", 440, 0.8, (0.45, 0.30)), 2150, 650, 3, 1.0, t_in=ww(lr, 1, "pol") - 0.3)
F_LR = Pz(T.ficha("Creó un programa de cifrado (E4M). Después, jefe de una red criminal. Arrestado en 2012; 25 años de prisión (2020).", 540, 320,
                  titulo="PAUL LE ROUX", px=28), 1620, 980, -2, t_in=ww(lr, 1, "programador"))
F_PASAP = Pz(T.ficha("5-AGO-2008 · pasaporte diplomático del Congo a nombre de «Paul SOLOTSHI Calder Le Roux»", 540, 300, titulo="EL PASAPORTE", px=28),
             1700, 420, 2, t_in=ww(lr, 2, "pasaporte") - 0.3, chinchetas=((0, None, AMAR),))
subraya(F_PASAP, ww(lr, 2, "solochi"), -120, 120, 70)
N_SOL = Pz(T.nota("¿SOLOTSHI = SATOSHI?", 270), 1150, 300, -6, t_in=ww(lr, 2, "solochi") + 0.4, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
P_CARCEL = portal_pz("carcel", "PRESO DESDE 2012", 2500, 1200, -3, INI(lr, 3) - 0.3)
sello_en(F_LR, "SIN VÍNCULO DIRECTO", ww(lr, 4, "vinculo"), 0, 40, -8, 44)
I_COD1 = Pz(P2.icono_card("documento", 220), 1100, 1250, -5, t_in=INI(lr, 5) + 0.2)
I_COD2 = Pz(P2.icono_card("documento", 220), 1450, 1300, 4, t_in=INI(lr, 5) + 0.5)
N_DIST = Pz(T.nota("≠", 150, (0.95, 0.55, 0.60), 110), 1275, 1050, 3, t_in=ww(lr, 5, "parecen") - 0.2, chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
T.Hilo(P_LEROUX, P_SAT, ww(lr, 1, "pol") + 0.3, 1.0, "verde", etiqueta=T.ficha("¿?", 120, 80, rayada=False, px=40))
T.Hilo(F_PASAP, F_CORREO, ww(lr, 2, "correo") - 0.2, 1.6, "amarillo", etiqueta=T.ficha("15 DÍAS ANTES", 230, 80, rayada=False, px=24))

TX(R(pk(lr, 0, "la", "crecer"), cy=880, px=90), ww(lr, 0, "la"), FIN(lr, 0) - 2.0)
TX(S([("Paul", ww(lr, 1, "pol")), ("Le", ww(lr, 1, "pol") + 0.15), ("Roux", ww(lr, 1, "pol") + 0.3)], W / 2, 900, 120), ww(lr, 1, "pol"), ww(lr, 1, "programador") + 1.0)
TX(S([("«Solotshi»", ww(lr, 2, "solochi"))], W / 2, 170, 120), ww(lr, 2, "solochi"), FIN(lr, 2) + 0.5, False)
FOTO_CRED("le_roux", ww(lr, 1, "pol"), FIN(lr, 1))

K(INI(lr, 0) + 0.2, -600, 300, 0.55, 0, 5, 4)
K(FIN(lr, 0), 1500, 650, 0.8, 0, 3, 3)
K(ww(lr, 1, "pol") + 0.2, 2150, 650, 1.35, 3, 0, 0, modo="suave")
K(ww(lr, 1, "programador") + 0.6, 1700, 950, 1.3, -2, 2, 3)
K(FIN(lr, 1), 1650, 980, 1.5, -2, 0, 0)
K(ww(lr, 2, "agosto"), 1750, 500, 1.2, 2, 3, -3)
K(ww(lr, 2, "correo"), -800, -400, 0.38, 0, 6, 0)
K(ww(lr, 2, "pasaporte") + 0.2, 1700, 430, 1.35, 2, 0, 0)
K(ww(lr, 2, "solochi") + 0.2, 1650, 500, 1.85, 2, 0, 0, modo="suave")
DENTRO(P_CARCEL, INI(lr, 3) + 0.2, ww(lr, 3, "prision"), FIN(lr, 3) + 0.1)
K(ww(lr, 4, "vinculo") + 0.2, 1620, 980, 1.45, -2, 0, 0)
K(INI(lr, 5) + 0.4, 1275, 1150, 1.25, 0, 3, 3)
K(FIN(lr, 5) + 0.2, 1275, 1150, 1.45, 0, 0, 0)

# ============================================================================================ ARCHIVO
ar = "archivo"
P_ARCH = portal_pz("archivo", "UN ARCHIVO DEL GOBIERNO DE EE. UU.", 5200, 2950, 2, INI(ar, 0) - 0.3)
F_DHS = Pz(T.ficha("Según la demanda: en 2019, una agente de Seguridad Nacional dijo que su equipo entrevistó en California a 4 personas.", 560, 330,
                   titulo="2019 · CALIFORNIA", px=27), 4450, 3200, -3, t_in=ww(ar, 1, "demanda") - 0.2)
PERS = [Pz(P2.icono_card("testigo", 220, 60 + k), 3900 + k * 260, 3650 + (k % 2) * 30, [-5, 3, -2, 6][k], t_in=ww(ar, 2, "cuatro") + 0.18 * k, dur=0.4,
           sonido=(k == 0)) for k in range(4)]
F_FOIA = Pz(T.ficha("ABR-2025 · un abogado demanda al gobierno para obtener las notas de esas entrevistas.", 540, 300, titulo="LA DEMANDA", px=28),
            5650, 3500, 3, t_in=INI(ar, 3) + 0.1)
sello_en(F_FOIA, "SIN PUBLICAR", ww(ar, 3, "ninguna") - 0.2, 0, 50, -9, 60)
T.Hilo(F_DHS, P_SAT, ww(ar, 2, "creacion"), 1.6, "blanco")

TX(N("4", W / 2, 860, 220, ww(ar, 2, "cuatro"), (0.95, 1.0, 0.1)), ww(ar, 2, "cuatro"), FIN(ar, 2) + 0.3)
TX(R(pk(ar, 3, "hasta", "ninguna"), cy=880, px=84), ww(ar, 3, "hasta"), FIN(ar, 3) + 0.5)

K(INI(ar, 0) + 0.4, 4600, 1800, 0.6, 0, 4, -4)
DENTRO(P_ARCH, INI(ar, 0) + 1.2, ww(ar, 0, "archivo"), FIN(ar, 0) + 0.2)
K(ww(ar, 1, "agente"), 4450, 3200, 1.35, -3, 2, 3)
K(FIN(ar, 1), 4450, 3220, 1.55, -3, 0, 0)
K(ww(ar, 2, "cuatro") + 0.3, 4300, 3600, 1.2, 0, 3, -3)
K(FIN(ar, 2), 4300, 3620, 1.35, 0, 0, 0)
K(INI(ar, 3) + 0.4, 5650, 3500, 1.35, 3, 0, 0)
K(FIN(ar, 3) + 0.2, 5600, 3450, 1.55, 3, 0, 0)

# ============================================================================================ ESPEJO
es = "espejo"
P_BUSTO = portal_pz("busto", "BUDAPEST · «TODOS SOMOS SATOSHI»", -500, -1020, -2, INI(es, 0) - 0.4)
TX(R(pk(es, 2, "todos", "satoshi"), cy=880, px=110), ww(es, 2, "todos"), FIN(es, 2) + 0.6)
FOTO_CRED("busto_budapest", INI(es, 0), FIN(es, 2))
K(INI(es, 0) - 0.2, 1500, 400, 0.4, 0, 6, 0)
DENTRO(P_BUSTO, INI(es, 0) + 0.4, ww(es, 0, "busto"), FIN(es, 2) + 0.2)

# ============================================================================================ GANCHO (flash-forward a oscuras)
g0 = "gancho"
TS = (INI(g0, 2) - 0.6, FIN(g0, 7) + 0.6)            # ventana en la que se ve el tablero «del futuro»
for pz_ in (P_REV, P_DORIAN, P_HAL, P_SZABO, P_WRIGHT, P_TODD, P_BACK, P_LEN, P_TELE, P_ROLLS, Q_OTRAS, P_WP, P_HEX, P_TIMES, P_F16, P_CARR,
            Q_DOR, P_GRAF, P_LEROUX) + tuple(RAFAGA[:12]):
    pz_.teaser = TS
for pz_ in (P_DORIAN, P_HAL, P_SZABO, P_WRIGHT, P_TODD, P_BACK, P_LEROUX):
    T.Hilo(pz_, P_SAT, 1e9, 1.0, "rojo", sonido=False, teaser=(ww(g0, 5, "cada") + 0.2, TS[1]))
P_BOVEDA.teaser = (0.0, TS[1])

T.Linterna([(INI(g0, 1) + 0.5, W / 2, H / 2, 1300), (INI(g0, 2), W / 2, H / 2, 620), (ww(g0, 4, "tribunal"), W / 2 + 60, H / 2, 560),
            (ww(g0, 6, "tablero"), W / 2, H / 2, 1500), (ww(g0, 6, "sospechosos"), W / 2, H / 2, 700), (FIN(g0, 7), W / 2, H / 2 - 30, 560)],
           INI(g0, 1) + 0.6, FIN(g0, 7) + 0.3, amb=0.13)


def _apagon(t, a=FIN(g0, 7) + 0.35, b=INI("origen", 0) - 0.05):
    """Negro entre el gancho y el inicio de la historia; la lámpara se enciende con un parpadeo."""
    if t < a or t > b + 1.2:
        return 1.0
    if t < b:
        return 1 - 0.78 * T.sm(T.pr(t, a, a + 0.35))
    e = t - b
    parp = 0.25 if (0.15 < e < 0.25 or 0.42 < e < 0.5) else 1.0
    return (0.22 + 0.78 * T.sm(T.pr(e, 0, 0.6))) * parp


T.LUZ_FX.append(_apagon)
snd(INI("origen", 0) - 0.05, "match", 0.4)

TX(S([("≈", ww(g0, 0, "millon")), ("1.100.000", ww(g0, 0, "millon")), ("BTC", ww(g0, 0, "bitcoins"))], W / 2, 900, 120), ww(g0, 0, "millon"), FIN(g0, 0) + 0.3)
TX(N("≈ 90.000 MILLONES USD", W / 2, 880, 110, ww(g0, 1, "noventa"), (0.95, 1.0, 0.1)), ww(g0, 1, "noventa"), FIN(g0, 1) + 0.2)
TX(CRED("Valor estimado con datos de Arkham Intelligence al 28-sep-2026", ww(g0, 1, "noventa"), FIN(g0, 1) + 0.2), ww(g0, 1, "noventa"), FIN(g0, 1) + 0.2,
   False)
TX(R(pk(g0, 3, "se", "cosas"), cy=880, px=86), ww(g0, 3, "se"), FIN(g0, 3) + 0.2)
TX(R(pk(g0, 6, "este", "sospechosos"), cy=880, px=86), INI(g0, 6), FIN(g0, 6) + 0.2)
TX(Q([[("¿Quién", ww(g0, 7, "quien")), ("es", ww(g0, 7, "quien") + 0.2)], [("Satoshi", ww(g0, 7, "satoshi")), ("Nakamoto", ww(g0, 7, "satoshi") + 0.3)]],
     ww(g0, 7, "quien"), cy=H * 0.78, px=96), ww(g0, 7, "quien"), FIN(g0, 7) + 0.3)

# cámara GANCHO: empieza DENTRO de la bóveda, sale al tablero oscuro y lo recorre con la linterna
_cx, _cy = T.centro_ventana(P_BOVEDA)
_zf = T.zoom_lleno(P_BOVEDA)
K(0.0, _cx, _cy, _zf * 1.08, P_BOVEDA.rot, 0, 0, modo="suave")
K(FIN(g0, 0) - 0.4, _cx, _cy, _zf * 1.01, P_BOVEDA.rot, 0, 0, modo="suave")
K(FIN(g0, 1) - 0.2, _cx, _cy + 40, 1.25, -2, 4, -5)
K(ww(g0, 2, "criptomoneda"), 0, 0, 1.15, -1, 2, 3, modo="suave")
K(FIN(g0, 2), 0, -60, 1.3, -1, 0, 0)
LATIGO(INI(g0, 3) - 0.1, INI(g0, 3) + 0.6, Q_OTRAS.x, Q_OTRAS.y, 1.3, 2, 0, 0)
K(FIN(g0, 3), Q_OTRAS.x, Q_OTRAS.y, 1.7, 2, 0, 0)
for palabra, pz_ in (("periodistas", P_REV), ("programadores", P_HAL), ("television", P_TELE), ("tribunal", P_ROLLS)):
    LATIGO(ww(g0, 4, palabra) - 0.3, ww(g0, 4, palabra) + 0.25, pz_.x, pz_.y, 1.15, pz_.rot * 0.6, 0, 0)
K(FIN(g0, 4), P_ROLLS.x - 100, P_ROLLS.y, 1.3, 2, 0, 0)
K(FIN(g0, 5), 0, 300, 0.32, 0, 6, 0)
K(ww(g0, 6, "tablero") + 0.3, 0, 300, 0.2, 0, 6, 0, modo="suave")
K(ww(g0, 6, "pistas") + 0.3, -1200, -1500, 0.55, -2, 4, 4)
K(ww(g0, 6, "sospechosos"), 1500, 1000, 0.5, 2, 3, -3)
K(FIN(g0, 6) + 0.2, 300, 200, 0.75, 0, 2, 2)
K(ww(g0, 7, "quien"), 0, 0, 1.25, -1.5, 0, 0, modo="suave")
K(FIN(g0, 7) + 0.4, 0, 0, 1.6, -1.5, 0, 0)
K(INI("origen", 0) - 0.3, -4500, -2300, 0.75, -3, 6, 8)


# ============================================================================================ CRÉDITOS (sobre el tablero a oscuras)
_T_CR = FIN("cierre", 6) + 1.4


def _oscurece(lz, t):
    lz *= 1.0 - 0.6 * T.sm(T.pr(t, _T_CR - 0.3, _T_CR + 0.7))


TX(_oscurece, _T_CR - 0.3, TOTAL + 1.0, False)
TX(CREDITOS("¿Quién es Satoshi Nakamoto?", [
    "Fuentes: The New York Times (vía TechCrunch y Coin360) · Wikipedia",
    "The Crypto Times · FinanceFeeds · FXStreet · Bitcoin.com · ScienceDaily · Coingape",
    "Datos: Satoshi Nakamoto Institute (análisis propio) · blockstream.info · Bitcoin v0.1 (MIT)",
    "Fotos (Wikimedia Commons): Joi Ito · Daily News-Post · Alexander Klink · Sheep0001 · Robert Scoble",
    "Kowtko21 · Roger Green · peter boy12qq12 · kellywritershouse · DEA · Sanjev Rajaram",
    "IMF / Stephen Jaffe · Fekist · Valentina Picozzi",
    "Animaciones y gráficos: producción propia · Música: Lyria",
    "Información al 3 de octubre de 2026. Nadie ha demostrado con pruebas ser Satoshi Nakamoto."], _T_CR),
   _T_CR, TOTAL + 1.0, False)
