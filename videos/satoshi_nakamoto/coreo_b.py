# -*- coding: utf-8 -*-
"""Coreografía B: DORIAN, HAL, SZABO, WRIGHT, TODD, BACK, CIERRE.
Zonas: Dorian a la izquierda (-4300, 250) · Hal entre Dorian y el centro (-2350, -600) · Szabo abajo-centro (-900, 2000) ·
Wright abajo (1500, 2200) · Todd abajo-derecha (4100, 2150) · Back a la derecha (3800, 120)."""
import tablero as T
import piezas as PZ
import piezas2 as P2
from coreo_comun import *  # noqa: F401,F403
from coreo_a import (Pz, pol, portal_pz, ROJA, AZUL, AMAR, VERDE, P_SAT, P_BOVEDA, P_BACK, F_BACK, F_CORREO, P_WP, P_HAL, F_TX, P_PRUEBA,
                     P_LLAVE, Q_OTRAS)

# ============================================================================================ DORIAN
d = "dorian"
P_REV = Pz(P2.revista(), -4950, -150, -5, 0.95, t_in=ww("perfil", 8, "titular") - 0.2, dur=0.6)
F_NW = Pz(T.ficha("6-MAR-2014 · Newsweek (Leah McGrath Goodman) dice haber encontrado a Satoshi", 540, 300, titulo="LA PORTADA", px=30),
          -4300, -500, 3, t_in=ww(d, 0, "revista"))
P_DORIAN = Pz(T.silueta_card("DORIAN NAKAMOTO", "SIN FOTO LIBRE"), -4250, 280, 3, 1.05, t_in=INI(d, 1) - 0.3)
P_TEMPLE = Pz(pol("temple_city", "TEMPLE CITY, CALIFORNIA", 520, 1.4, (0.5, 0.5)), -5100, 560, -4, t_in=ww(d, 1, "vive"))
F_DOR = Pz(T.ficha("Físico · trabajó en proyectos militares clasificados · nombre de nacimiento: Satoshi Nakamoto", 560, 330,
                   titulo="DORIAN P. S. NAKAMOTO", px=30), -3600, 640, 2, t_in=ww(d, 1, "fisico") - 0.2)
subraya(F_DOR, ww(d, 1, "literalmente"), -240, 240, 120)
P_PUERTA = portal_pz("puerta", "LA PREGUNTA EN LA PUERTA", -4850, 1000, 3, INI(d, 2) - 0.4)
Q_DOR = Pz(PZ.tarjeta_cita("Ya no estoy involucrado en eso. Se lo entregaron a otras personas.",
                           "Dorian Nakamoto a Newsweek, 2014 (después dijo que entendió mal la pregunta)", 720, 36), -3900, 1060, -2,
           t_in=INI(d, 3) + 0.1)
P_PERSEC = portal_pz("persecucion", "REPORTEROS EN LOS ÁNGELES", -5150, -650, -3, INI(d, 4) - 0.4)
sello_en(P_DORIAN, "LO NIEGA", ww(d, 5, "niega"), 0, 60, -10, 72)
F_P2P = Pz(PZ.tarjeta_cita("No soy Dorian Nakamoto.", "Cuenta de Satoshi en P2P Foundation, 6-mar-2014 · «I am not Dorian Nakamoto.»", 640, 46),
           -3700, -230, -3, t_in=ww(d, 6, "frase") - 0.2)
T.Punteada(P_SAT, F_P2P, ww(d, 6, "cuenta"), color=(0.85, 0.92, 1.0), curva=0.15, paquetes=2, vel=0.6)
sello_en(F_P2P, "¿HACKEADA?", ww(d, 7, "hackeada"), 120, 60, 8, 60)
H_DOR = rojo(P_DORIAN, P_SAT, ww(d, 1, "literalmente") + 0.2, 1.4, corte=ww(d, 7, "prueba"))
P_CUADRAS = portal_pz("cuadras", "A UNAS CUADRAS · ESQUEMA", -3800, -830, 4, INI(d, 8) - 0.3)

TX(S([("Newsweek", ww(d, 0, "niusuik")), ("·", ww(d, 0, "portada")), ("Marzo", ww(d, 0, "portada")), ("2014", ww(d, 0, "portada") + 0.2)], W / 2, 170, 96),
   ww(d, 0, "niusuik"), FIN(d, 0), False)
TX(S([("Dorian", INI(d, 1)), ("Satoshi", INI(d, 1) + 0.15), ("Nakamoto", INI(d, 1) + 0.3)], W / 2, 900, 100), INI(d, 1), ww(d, 1, "fisico"))
TX(R(pk(d, 3, "ya", "personas"), cy=880, px=78), INI(d, 3), FIN(d, 3) + 0.3)
TX(R(pk(d, 6, "no", "nakamoto"), cy=880, px=86), ww(d, 6, "soy") - 0.25, FIN(d, 6) + 0.4)
FOTO_CRED("temple_city", ww(d, 1, "vive"), ww(d, 1, "fisico"))

# cámara DORIAN
K(ww("perfil", 8, "prensa"), -2600, 1300, 0.55, 0, 5, 5)
LATIGO(ww("perfil", 8, "titular") - 0.3, ww("perfil", 8, "titular") + 0.35, -4900, -100, 1.15, -4, 0, 0)
K(FIN("perfil", 8) + 0.3, -4950, -150, 1.35, -5, 0, 0)
K(ww(d, 0, "revista"), -4600, -320, 1.2, 0, 3, 4)
K(FIN(d, 0), -4400, -420, 1.35, 2, 0, 0)
K(INI(d, 1) + 0.4, -4250, 280, 1.25, 3, -2, 3)
K(ww(d, 1, "vive") + 0.5, -4800, 450, 1.15, -2, 3, -3)
K(ww(d, 1, "fisico") + 0.3, -3700, 620, 1.4, 2, 0, 3)
K(FIN(d, 1), -3650, 680, 1.65, 2, 0, 0)
DENTRO(P_PUERTA, INI(d, 2) + 0.2, ww(d, 2, "pregunta"), FIN(d, 3) - 1.0)
K(FIN(d, 3) + 0.1, -3900, 1060, 1.45, -2, 0, 0)
DENTRO(P_PERSEC, INI(d, 4) + 0.3, ww(d, 4, "persiguen"), FIN(d, 4) + 0.1)
K(INI(d, 5) + 0.6, -4250, 280, 1.3, 2, 3, -3)
K(FIN(d, 5), -4250, 300, 1.5, 3, 0, 0)
K(ww(d, 6, "cuenta"), -150, 0, 1.0, -1, 3, 3)
K(ww(d, 6, "frase") + 0.2, -3700, -230, 1.4, -3, 0, -2, modo="suave")
K(FIN(d, 6), -3700, -230, 1.65, -3, 0, 0)
K(ww(d, 7, "hackeada") + 0.4, -3500, -150, 1.2, -1, 2, 2)
K(ww(d, 7, "prueba") + 0.6, -2400, 140, 0.7, 0, 3, 3)
DENTRO(P_CUADRAS, INI(d, 8) + 0.2, ww(d, 8, "cuadras"), ww(d, 8, "interesante") - 0.4)

# ============================================================================================ HAL
h = "hal"
F_PGP = Pz(T.ficha("Trabajó años en PGP Corporation (cifrado de correo) hasta 2011.", 480, 260, titulo="PIONERO DEL CIFRADO", px=30), -3050, -480, -3,
           t_in=ww(h, 1, "empresa") - 0.3)
F_RPOW = Pz(T.ficha("2004 · RPOW: prueba de trabajo reutilizable, antecesor de bitcoin.", 480, 260, titulo="RPOW", px=30), -2950, -60, 3,
            t_in=ww(h, 2, "cuatro"))
F_FORBES = Pz(T.ficha("Forbes (2014): un análisis de estilo lo halla el más parecido a Satoshi.", 520, 280, titulo="ESTILO", px=30), -2900, -1500, -2,
              t_in=ww(h, 3, "analisis"))
sello_en(P_HAL, "LO NEGÓ", ww(h, 4, "nego"), 0, 90, -8, 70)
P_SOBRE = Pz(P2.icono_card("sobre", 240), -1820, -470, 5, t_in=ww(h, 4, "correos") - 0.1)
N_COART = Pz(T.nota("¿COARTADA?", 260), -2850, 330, -5, t_in=ww(h, 5, "coartada") - 0.1, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
P_CARRERA = portal_pz("carrera", "SANTA BÁRBARA · 18-ABR-2009", -3320, 620, 2, INI(h, 6) - 0.3)
F_ALIBI = Pz(T.ficha("8:00 salida\n9:16 correo de Satoshi\n9:18 Hal cruza la meta", 480, 300, titulo="18-ABR-2009", px=32), -2450, 470, -2,
             t_in=ww(h, 7, "minutos") - 0.2)
resalta(F_ALIBI, ww(h, 7, "minutos") + 0.4, -200, 200, -5)
F_ELA = Pz(T.ficha("2009 · diagnóstico: ELA\n28-AGO-2014 · muere", 480, 260, titulo="HAL FINNEY", px=32), -1950, 1000, 3,
           t_in=ww(h, 8, "diagnosticaron") - 0.2)
P_CRIO = portal_pz("crio", "CRIOPRESERVADO", -2620, 1150, -3, INI(h, 9) - 0.3)
H_HAL = T.Hilo(P_HAL, P_SAT, INI(h, 0) + 0.4, 1.0, "rojo", etiqueta=T.ficha("1.ª TRANSACCIÓN", 260, 80, rayada=False, px=24))
T.Hilo(N_COART, P_HAL, ww(h, 5, "coartada") + 0.3, 0.6, "amarillo")
T.Hilo(F_ALIBI, P_CARRERA, ww(h, 7, "meta"), 0.6, "amarillo")

TX(S([("Hal", INI(h, 0)), ("Finney", INI(h, 0) + 0.25)], W / 2, 900, 120), INI(h, 0), FIN(h, 0))
TX(S([("9:16", ww(h, 7, "enviaba")), ("·", ww(h, 7, "minutos")), ("9:18", ww(h, 7, "meta"))], W / 2, 170, 110), ww(h, 7, "enviaba"), FIN(h, 7) + 0.3, False)
TX(R(pk(h, 5, "algo", "coartada"), cy=880, px=88), ww(h, 5, "algo"), FIN(h, 5) + 0.3)
FOTO_CRED("hal_finney", INI(h, 0), FIN(h, 0))

# cámara HAL
K(ww(d, 8, "interesante") + 0.6, -2350, -600, 0.9, -2, 4, -4)
K(FIN(h, 0), -2350, -600, 1.35, -3, 0, 0)
K(ww(h, 1, "empresa"), -2950, -450, 1.35, -3, 2, 3)
K(ww(h, 2, "cuatro") + 0.3, -2950, -100, 1.35, 3, -2, 3)
K(ww(h, 3, "analisis") + 0.3, -2880, -1460, 1.3, -2, 3, -3)
K(FIN(h, 3), -2900, -1500, 1.5, -2, 0, 0)
K(ww(h, 4, "nego") + 0.2, -2350, -550, 1.45, -3, 0, 0, modo="suave")
K(ww(h, 4, "correos") + 0.3, -1950, -500, 1.35, 2, 2, -3)
K(INI(h, 5) + 0.3, -2700, 150, 1.2, -3, 3, 3)
DENTRO(P_CARRERA, INI(h, 6) + 0.3, ww(h, 6, "carrera") + 0.2, ww(h, 7, "minutos"))
K(ww(h, 7, "meta") + 0.2, -2450, 470, 1.5, -2, 0, 0)
K(FIN(h, 7) + 0.2, -2450, 480, 1.7, -2, 0, 0)
K(ww(h, 8, "diagnosticaron") + 0.2, -1950, 1000, 1.4, 3, 2, -3)
DENTRO(P_CRIO, INI(h, 9) + 0.1, ww(h, 9, "criopreservado") + 0.5, FIN(h, 9) + 0.2)

# ============================================================================================ SZABO
z_ = "szabo"
P_SZABO = Pz(pol("szabo_capa", "NICK SZABO", 480, 1.05, (0.58, 0.42)), -1000, 1800, -3, 1.05, t_in=INI(z_, 0) - 0.2)
H_SZ = rojo(P_SZABO, P_SAT, ww(z_, 0, "nik") + 0.3, 1.0)
P_BITGOLD = portal_pz("bitgold", "BIT GOLD · 1998", -300, 2420, 2, ww(z_, 1, "llamado") - 0.6)
F_BG = Pz(T.ficha("BIT GOLD\n(1998)", 340, 210, px=40, rayada=False), -760, 1300, -4, t_in=INI(z_, 2) + 0.1, chinchetas=((0, None, AMAR),))
F_BTC = Pz(T.ficha("BITCOIN\n(2008)", 340, 210, px=40, rayada=False), -260, 1310, 3, t_in=INI(z_, 2) + 0.5, chinchetas=((0, None, AMAR),))
T.Cinta(-510, 1300, -8, INI(z_, 2) + 1.0, 200, 50)
F_ASTON = Pz(T.ficha("2014 · estudiantes de lingüística forense (sin revisión por pares): su estilo, el más cercano.", 520, 300, titulo="UNIVERSIDAD DE ASTON", px=28),
             -1000, 2470, 2, t_in=ww(z_, 3, "estudiantes") - 0.2)
P_REFS = Pz(T.hoja_img("whitepaper", 640, (0.755, 0.785, 0.985, 0.955)), -150, 1850, -2, t_in=ww(z_, 4, "documento") - 0.2)
resalta(P_REFS, ww(z_, 4, "uei"), -280, 280, -190, grosor=26)
resalta(P_REFS, ww(z_, 4, "adam"), -280, 280, 128, grosor=26)
N_BG = Pz(T.nota("¿Y BIT GOLD?", 250, (0.95, 0.55, 0.60)), 330, 1650, 6, t_in=ww(z_, 4, "menciona"), chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
Q_SZ = Pz(PZ.tarjeta_cita("Te equivocaste al señalarme como Satoshi, pero ya estoy acostumbrado.", "Nick Szabo a Dominic Frisby, 2014", 720, 36),
          -1750, 2950, 2, t_in=INI(z_, 6) + 0.2)
sello_en(P_SZABO, "LO NIEGA", ww(z_, 6, "nego"), 0, 80, -8, 70)

TX(S([("Nick", INI(z_, 0) + 0.5), ("Szabo", INI(z_, 0) + 0.7)], W / 2, 900, 120), INI(z_, 0) + 0.5, FIN(z_, 0) + 0.6)
TX(Q([[("¿Un", ww(z_, 5, "descuido") - 0.2), ("descuido", ww(z_, 5, "descuido"))], [("¿O", ww(z_, 5, "alguien") - 0.2), ("algo", ww(z_, 5, "alguien")),
       ("más", ww(z_, 5, "alguien") + 0.2)]], ww(z_, 5, "descuido") - 0.2, cy=H * 0.80, px=78), INI(z_, 5), FIN(z_, 5) + 0.3)
FOTO_CRED("szabo_capa", INI(z_, 0), FIN(z_, 0) + 0.6)

# cámara SZABO
K(INI(z_, 0) + 0.2, -1400, 1500, 0.8, 0, 4, 4)
K(FIN(z_, 0) + 0.3, -1000, 1800, 1.3, -3, 0, 0)
DENTRO(P_BITGOLD, ww(z_, 1, "llamado") - 0.2, ww(z_, 1, "oro"), FIN(z_, 1) + 0.1)
K(INI(z_, 2) + 0.5, -510, 1300, 1.4, -1, 3, 3)
K(FIN(z_, 2), -510, 1310, 1.6, 0, 0, 0)
K(ww(z_, 3, "estudiantes") + 0.3, -1000, 2450, 1.35, 2, -2, 3)
K(ww(z_, 4, "documento"), -300, 1900, 1.15, -2, 3, -3)
K(ww(z_, 4, "uei"), -150, 1680, 1.75, -2, 0, 0, modo="suave")
K(ww(z_, 4, "adam") + 0.2, -150, 1960, 1.75, -2, 0, 0)
K(ww(z_, 4, "menciona") + 0.2, 150, 1750, 1.4, 3, 0, 0)
K(FIN(z_, 5), -200, 1900, 1.0, 0, 4, 4)
K(INI(z_, 6) + 0.6, -1750, 2900, 1.35, 2, 0, -3)
K(FIN(z_, 6), -1700, 2850, 1.5, 2, 0, 0)

# ============================================================================================ WRIGHT
w_ = "wright"
P_WRIGHT = Pz(T.silueta_card("CRAIG WRIGHT", "SIN FOTO LIBRE"), 1100, 1750, 3, 1.05, t_in=ww(w_, 0, "contrario") - 0.3)
H_WR = rojo(P_WRIGHT, P_SAT, ww(w_, 0, "contrario") + 0.4, 1.0, corte=ww(w_, 10, "desacato"))
F_FILTR = Pz(T.ficha("8-DIC-2015 · Wired y Gizmodo publican documentos filtrados que lo señalan.", 520, 280, titulo="LA FILTRACIÓN", px=29), 1750, 1350, -3,
             t_in=ww(w_, 1, "diciembre") - 0.2)
P_ESCEN = portal_pz("escenario", "MAYO 2016 · «YO SOY SATOSHI»", 2350, 1720, 2, INI(w_, 2) - 0.3)
P_F16 = Pz(P2.hoja_firma("FIRMA DE SU «PRUEBA» (2016)", "publicada en base64; aquí convertida a hex"), 700, 2450, -2, t_in=ww(w_, 3, "firma") - 0.2)
P_F09 = Pz(P2.hoja_firma("FIRMA DE LA TX DEL BLOQUE 170", "12-ene-2009 · de Satoshi a Hal Finney", seed=40), 1450, 2620, 3, t_in=ww(w_, 4, "transaccion") - 0.3,
           chinchetas=((0, None, (0.95, 0.55, 0.1)),))
N_IDENT = Pz(T.nota("IDÉNTICAS", 230, (0.95, 0.55, 0.60), 50), 1080, 2950, -5, t_in=ww(w_, 4, "jal") + 0.2, chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
T.Cinta(1080, 2540, 15, ww(w_, 4, "jal"), 220, 54)
T.Hilo(P_F09, F_TX, ww(w_, 4, "jal") + 0.4, 1.4, "amarillo")
P_FOTOC = portal_pz("fotocopia", "COMO FOTOCOPIAR UNA FIRMA", 2250, 2450, -3, INI(w_, 5) - 0.3)
DEM = [Pz(PZ.recorte("DEMANDA", 380, 50 + k, False, 44), 2850 + 150 * k, 1250 + 140 * k, [-6, 4, -3][k], t_in=ww(w_, 6, "demando") + 0.25 * k, dur=0.4)
       for k in range(3)]
for k in range(3):
    sello_en(DEM[k], "DEMANDA", ww(w_, 6, "demando") + 0.25 * k + 0.45, 0, 30, -12, 48)
P_ROLLS = Pz(pol("rolls_building", "ROLLS BUILDING · LONDRES", 520, 1.45, (0.5, 0.5)), 2950, 2300, 3, t_in=ww(w_, 7, "alianza") - 0.2)
P_TRIB = portal_pz("tribunal", "14-MAR-2024 · EL FALLO", 2150, 2950, -2, INI(w_, 8) - 0.3)
sello_en(P_WRIGHT, "NO ES EL AUTOR", ww(w_, 8, "autor"), 0, -120, -9, 44)
sello_en(P_WRIGHT, "NO ES SATOSHI", ww(w_, 8, "satoshi"), 0, 0, 7, 48)
sello_en(P_WRIGHT, "NO CREÓ BITCOIN", ww(w_, 8, "creo"), 0, 120, -6, 44)
sello_en(P_F16, "FALSIFICACIONES", ww(w_, 9, "falsificaciones"), 0, 30, -10, 56)
F_DESAC = Pz(T.ficha("19-DIC-2024 · desacato: 1 año de prisión, pena suspendida.", 520, 260, titulo="CONDENA", px=30), 1450, 3150, -3,
             t_in=ww(w_, 10, "condenaron") - 0.2)

TX(S([("Craig", ww(w_, 1, "kreig")), ("Wright", ww(w_, 1, "kreig") + 0.25)], W / 2, 900, 120), ww(w_, 1, "kreig"), ww(w_, 1, "diciembre"))
TX(R(pk(w_, 3, "una", "cadena", 1), cy=880, px=80), ww(w_, 3, "una", 1), FIN(w_, 3) + 0.2)
TX(S([("Juez", ww(w_, 8, "juez")), ("James", ww(w_, 8, "juez") + 0.2), ("Mellor", ww(w_, 8, "juez") + 0.4)], W / 2, 170, 96), ww(w_, 8, "juez"),
   ww(w_, 8, "tajante") + 0.8, False)
TX(R(pk(w_, 9, "habia", "repetida"), cy=880, px=80), ww(w_, 9, "habia"), FIN(w_, 9) + 0.3)
FOTO_CRED("rolls_building", ww(w_, 7, "alianza"), FIN(w_, 7))

# cámara WRIGHT
K(INI(w_, 0) + 0.4, 200, 2300, 0.7, 0, 4, 4)
K(ww(w_, 0, "contrario") + 0.3, 1100, 1750, 1.3, 3, 0, 0, modo="suave")
K(ww(w_, 1, "diciembre") + 0.3, 1600, 1450, 1.25, -2, 3, -3)
K(FIN(w_, 1), 1750, 1380, 1.45, -3, 0, 0)
DENTRO(P_ESCEN, INI(w_, 2) + 0.1, ww(w_, 2, "anuncio") + 0.3, FIN(w_, 2) + 0.2)
K(ww(w_, 3, "firma") + 0.3, 900, 2400, 1.2, -2, 3, 3)
K(ww(w_, 3, "vieja"), 700, 2450, 1.55, -2, 0, 0)
K(ww(w_, 4, "transaccion") + 0.2, 1100, 2550, 1.1, 0, 2, -3)
K(FIN(w_, 4) + 0.2, 1080, 2650, 1.25, 0, 0, 0)
DENTRO(P_FOTOC, INI(w_, 5), ww(w_, 5, "fotocopiar") + 0.2, FIN(w_, 5) + 0.1)
K(ww(w_, 6, "demando") + 0.3, 3000, 1400, 1.2, -2, 3, 4)
K(FIN(w_, 6), 3100, 1450, 1.35, 0, 0, 0)
K(ww(w_, 7, "alianza") + 0.2, 2950, 2300, 1.3, 3, -2, -3)
DENTRO(P_TRIB, INI(w_, 8) + 0.1, ww(w_, 8, "tajante") - 0.2, ww(w_, 8, "tajante") + 0.9)
K(ww(w_, 8, "autor") + 0.1, 1100, 1750, 1.35, 3, 0, 0, modo="suave")
K(FIN(w_, 8) + 0.2, 1100, 1760, 1.45, 3, 0, 0)
K(ww(w_, 9, "mentido"), 800, 2300, 1.0, 0, 3, -3)
K(ww(w_, 9, "falsificaciones") + 0.2, 700, 2450, 1.5, -2, 0, 0)
K(ww(w_, 10, "condenaron") + 0.2, 1450, 3100, 1.3, -3, 2, 3)
K(ww(w_, 10, "desacato"), 700, 1000, 0.62, 0, 4, 0)
K(FIN(w_, 10) + 0.4, 900, 1300, 0.8, 0, 2, 2)
tache(P_WRIGHT, FIN(w_, 10) - 0.2, 0.6)

# ============================================================================================ TODD
t_ = "todd"
P_TELE = portal_pz("tele", "OCT-2024 · DOCUMENTAL DE HBO", 3600, 2050, -2, INI(t_, 1) - 0.3)
P_TODD = Pz(T.silueta_card("PETER TODD", "SIN FOTO LIBRE"), 4450, 1800, 3, 1.05, t_in=ww(t_, 1, "canadiense"))
H_TODD = rojo(P_TODD, P_SAT, ww(t_, 1, "piter") + 0.3, 1.2, color="azul")
P_FORO = portal_pz("foro_hora", "2010 · UNA HORA DESPUÉS", 4300, 2650, 2, INI(t_, 2) - 0.3)
N_MISMA = Pz(T.nota("¿LA MISMA PERSONA?", 270), 5050, 2350, 5, t_in=ww(t_, 3, "terminara"), chinchetas=((0, None, None),), entrada="aparece", dur=0.25)
sello_en(P_TODD, "LO NIEGA", ww(t_, 4, "ridiculo"), 0, 80, -8, 70)
F_FIND = Pz(T.ficha("ABR-2026 · documental «Finding Satoshi»: ¿Hal Finney + Len Sassaman?", 520, 300, titulo="OTRA TEORÍA", px=29), 3500, 2950, -3,
            t_in=INI(t_, 5) + 0.2)
P_LEN = Pz(pol("len_sassaman", "LEN SASSAMAN", 460, 0.85, (0.5, 0.3)), -1750, 60, 4, 1.0, t_in=ww(t_, 6, "len") - 0.3)
T.Hilo(P_HAL, P_LEN, ww(t_, 6, "len") + 0.3, 0.8, "azul", etiqueta=T.ficha("¿DOS PERSONAS?", 260, 80, rayada=False, px=24))
T.Hilo(P_LEN, P_SAT, ww(t_, 6, "len") + 0.9, 0.8, "azul")
F_LEN = Pz(T.ficha("3-JUL-2011 · muere Len Sassaman\n68 días después del último correo de Satoshi", 520, 280, titulo="LEN SASSAMAN", px=29), -1750, 560, -2,
           t_in=ww(t_, 7, "murio") - 0.1)
P_HOMEN = portal_pz("homenaje", "UN HOMENAJE EN LA CADENA", -1300, 1250, 3, INI(t_, 8) - 0.3)
N_Q1 = Pz(T.nota("?", 170, (0.98, 0.86, 0.25), 90), -2050, -950, -8, t_in=ww(t_, 9, "negarla"), chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
N_Q2 = Pz(T.nota("?", 170, (0.98, 0.86, 0.25), 90), -1450, -250, 7, t_in=ww(t_, 9, "confirmarla"), chinchetas=((0, None, None),), entrada="aparece", dur=0.2)

TX(S([("Peter", ww(t_, 1, "piter")), ("Todd", ww(t_, 1, "piter") + 0.25)], W / 2, 170, 120), ww(t_, 1, "piter"), FIN(t_, 1) + 0.6, False)
TX(R(pk(t_, 3, "como", "cuenta"), cy=880, px=78), ww(t_, 3, "como"), FIN(t_, 3) + 0.3)
TX(N("68 DÍAS", W / 2, 880, 140, ww(t_, 7, "meses"), (0.95, 1.0, 0.1)), ww(t_, 7, "meses"), FIN(t_, 7) + 0.3)
FOTO_CRED("len_sassaman", ww(t_, 6, "len"), FIN(t_, 6) + 1.0)

# cámara TODD
K(INI(t_, 0) + 0.3, 2300, 2400, 0.62, 0, 4, 4)
K(FIN(t_, 0), 3300, 2200, 0.9, -2, 2, 3)
DENTRO(P_TELE, INI(t_, 1) + 0.1, ww(t_, 1, "documental") + 0.3, ww(t_, 1, "canadiense") - 0.2)
K(ww(t_, 1, "piter") + 0.2, 4450, 1800, 1.35, 3, 0, 0, modo="suave")
DENTRO(P_FORO, INI(t_, 2) + 0.2, ww(t_, 2, "corrigio"), FIN(t_, 2) + 0.1)
K(ww(t_, 3, "terminara"), 4800, 2300, 1.25, 4, 2, -3)
K(INI(t_, 4) + 0.3, 4450, 1850, 1.35, 3, 0, 0)
K(FIN(t_, 4), 4450, 1850, 1.5, 3, 0, 0)
K(INI(t_, 5) + 0.6, 3500, 2900, 1.3, -3, 2, 3)
LATIGO(ww(t_, 5, "dos", 1) - 0.1, ww(t_, 5, "dos", 1) + 0.7, -2100, -300, 0.95, 0, 0, 0)
K(ww(t_, 6, "len") + 0.6, -1850, -200, 1.15, 2, 2, -3)
K(ww(t_, 7, "murio") + 0.3, -1750, 450, 1.35, -2, 0, 0)
K(FIN(t_, 7), -1750, 520, 1.5, -2, 0, 0)
DENTRO(P_HOMEN, INI(t_, 8) + 0.1, ww(t_, 8, "homenaje"), FIN(t_, 8) + 0.2)
K(INI(t_, 9) + 0.6, -1900, -500, 0.9, 0, 3, 3)
K(FIN(t_, 9), -1850, -450, 1.05, 0, 0, 0)

# ============================================================================================ BACK
b_ = "back"
P_HASH = portal_pz("hashcash", "HASHCASH · 1997", 4700, -480, 3, ww(b_, 1, "invento") - 0.4)
F_REF = Pz(T.ficha("[6] A. Back, «Hashcash - a denial of service counter-measure», 2002.", 560, 280, titulo="CITADO EN EL WHITE PAPER", px=28), 2900, -250, -2,
           t_in=ww(b_, 2, "citado") - 0.2)
T.Hilo(P_WP, P_BACK, ww(b_, 2, "documento"), 1.6, "rojo", grosor=3.6)
F_RESP = Pz(T.ficha("21-AGO-2008 · Back le responde: lee b-money, de Wei Dai.", 520, 260, titulo="LA RESPUESTA", px=29), 4500, 650, 3,
            t_in=ww(b_, 3, "escribio") + 0.1)
T.Punteada(P_BACK, F_CORREO, ww(b_, 3, "respondio"), color=(1.0, 0.85, 0.45), curva=-0.06, dur=1.4, paquetes=4, vel=0.3)
P_CARR = Pz(pol("carreyrou", "JOHN CARREYROU", 440, 0.85, (0.5, 0.35)), 5200, 420, -4, t_in=ww(b_, 4, "yon") - 0.2)
F_NYT = Pz(T.ficha("8-ABR-2026 · The New York Times: 18 meses de investigación. Back, el candidato más fuerte.", 540, 300, titulo="LA INVESTIGACIÓN", px=28),
           5250, 980, 3, t_in=ww(b_, 4, "niu") - 0.2)
P_IA = portal_pz("ia", "MILES DE MENSAJES · IA", 4400, 1150, -2, INI(b_, 5) - 0.3)
F_MANIAS = Pz(T.ficha("«proof of work» sin guiones · confunde «its» / «it's»", 520, 260, titulo="MANÍAS AL ESCRIBIR", px=30), 2900, 1000, -3,
              t_in=ww(b_, 6, "manias") - 0.1)
P_ACT = Pz(P2.esquema_actividad(), 5350, 1580, 2, t_in=ww(b_, 7, "callado") - 0.3)
P_ELSAL = portal_pz("el_salvador", "EL SALVADOR · «NO»", 2650, 300, 3, INI(b_, 8) - 0.3)
Q_NOSOY = Pz(PZ.tarjeta_cita("No soy Satoshi.", "Adam Back en X, 8-abr-2026 · «i'm not satoshi»", 620, 52), 2950, -700, -3, t_in=ww(b_, 9, "soy") - 0.3)
sello_en(P_BACK, "LO NIEGA", ww(b_, 9, "soy"), 0, 110, -8, 70)
P_CASI = Pz(P2.casillas("¿PRUEBA DIRECTA?", ("Una firma", "Una moneda movida", "Una prueba directa"), 520, px=32), 3450, 1020, 2, t_in=INI(b_, 10) + 0.1)
H_BACK = T.Hilo(P_BACK, P_SAT, ww(b_, 6, "bak") + 0.2, 1.4, "rojo", grosor=5.0)

TX(S([("Adam", ww(b_, 1, "adam")), ("Back", ww(b_, 1, "adam") + 0.25)], W / 2, 170, 120), ww(b_, 1, "adam"), ww(b_, 1, "invento"), False)
TX(N("18 MESES", W / 2, 880, 140, ww(b_, 4, "dieciocho"), (0.95, 1.0, 0.1)), ww(b_, 4, "dieciocho"), FIN(b_, 4) + 0.3)
TX(R(pk(b_, 6, "el", "bak"), cy=880, px=86), ww(b_, 6, "el"), FIN(b_, 6) + 0.3)
TX(R(pk(b_, 9, "no", "satoshi"), cy=880, px=110), ww(b_, 9, "no"), ww(b_, 9, "coincidencia"))
TX(R(pk(b_, 10, "no", "directa"), cy=880, px=80), ww(b_, 10, "no"), FIN(b_, 10) + 0.4)
FOTO_CRED("adam_back", ww(b_, 1, "adam"), ww(b_, 1, "invento"))
FOTO_CRED("carreyrou", ww(b_, 4, "yon"), FIN(b_, 4))

# cámara BACK: sigue la línea del primer correo de vuelta hasta Back
K(INI(b_, 0) + 0.2, -1500, -700, 0.9, 0, 2, 2)
K(ww(b_, 0, "mismo"), 1200, -400, 0.55, 0, 6, 0)
K(FIN(b_, 0), 3800, 120, 1.25, 4, 0, 0, modo="suave")
DENTRO(P_HASH, ww(b_, 1, "invento") - 0.3, ww(b_, 1, "jashcash"), FIN(b_, 1) + 0.1)
K(ww(b_, 2, "citado"), 2900, -250, 1.35, -2, 3, 3)
K(ww(b_, 2, "documento") + 0.5, 300, -1100, 0.38, 0, 6, 0)
K(INI(b_, 3) + 0.4, 3800, 150, 1.3, 4, 0, 0)
K(ww(b_, 3, "escribio") + 0.2, 3820, 170, 1.42, 4, 0, 0)
K(ww(b_, 3, "respondio") + 0.3, 4500, 650, 1.35, 3, 0, 0)
K(ww(b_, 3, "uei"), 4300, 400, 1.1, 2, 2, 3)
K(ww(b_, 4, "yon") + 0.3, 5200, 420, 1.35, -4, 0, 0)
K(ww(b_, 4, "niu") + 0.2, 5250, 950, 1.35, 3, 2, -3)
DENTRO(P_IA, INI(b_, 5) + 0.2, ww(b_, 5, "inteligencia"), FIN(b_, 5) + 0.1)
K(ww(b_, 6, "manias") + 0.3, 2900, 1000, 1.35, -3, 3, 3)
K(ww(b_, 6, "candidatos"), 3500, 500, 0.85, 0, 2, -2)
K(ww(b_, 6, "bak") + 0.3, 3800, 140, 1.4, 4, 0, 0, modo="suave")
K(ww(b_, 7, "callado") + 0.2, 5350, 1580, 1.25, 2, 2, -3)
K(FIN(b_, 7), 5350, 1600, 1.45, 2, 0, 0)
DENTRO(P_ELSAL, INI(b_, 8) + 0.2, ww(b_, 8, "persona"), FIN(b_, 8) + 0.1)
K(ww(b_, 9, "soy") + 0.2, 2950, -700, 1.4, -3, 0, 0)
K(ww(b_, 9, "coincidencia") + 0.3, 3800, 120, 1.25, 4, 2, -3)
K(INI(b_, 10) + 0.5, 3450, 1000, 1.35, 2, 0, 0)
K(FIN(b_, 10) + 0.4, 3000, 700, 0.9, 0, 3, 3)
circulo(P_BACK, ww(b_, 6, "bak"), 0.7, seed=4)

# ============================================================================================ CIERRE
c = "cierre"
N_M1 = Pz(T.nota("¿MURIÓ?", 240), -700, 380, -6, t_in=ww(c, 4, "murio") - 0.1, chinchetas=((0, None, None),), entrada="aparece", dur=0.2)
N_M2 = Pz(T.nota("¿PERDIÓ LAS LLAVES?", 260, (0.55, 0.85, 0.95)), 720, 300, 5, t_in=ww(c, 4, "perdio") - 0.1, chinchetas=((0, None, None),),
          entrada="aparece", dur=0.2)
N_M3 = Pz(T.nota("¿NOS ESTÁ VIENDO?", 260, (0.95, 0.55, 0.60)), 0, 650, -3, t_in=ww(c, 4, "viendo") - 0.1, chinchetas=((0, None, None),),
          entrada="aparece", dur=0.2)
P_ESTAT = portal_pz("estatua", "LUGANO · LA ESTATUA QUE DESAPARECE", -150, -1000, 2, INI(c, 5) - 0.4)

TX(R(pk(c, 5, "o", "diseno"), cy=880, px=86), INI(c, 5), FIN(c, 5) + 0.4)
TX(R(pk(c, 6, "bitcoin", "nadie", 0, 1), cy=960, px=86), ww(c, 6, "bitcoin"), FIN(c, 6) + 1.2)
FOTO_CRED("estatua_lugano", INI(c, 5), FIN(c, 5))


T.Linterna([(ww(c, 6, "nadie"), W / 2, H / 2, 900), (FIN(c, 6) + 1.0, W / 2, H / 2 - 40, 520), (TOTAL, W / 2, H / 2 - 40, 480)],
           ww(c, 6, "nadie"), TOTAL + 5, amb=0.16)

# cámara CIERRE: gran retroceso, saltos por los sospechosos, vuelta al centro
K(INI(c, 0) + 0.2, 1800, 600, 0.6, 0, 4, 2)
K(FIN(c, 0) + 0.2, 0, 150, 0.17, 0, 6, 0, modo="suave")
for k, (palabra, pz_) in enumerate((("hombre", P_DORIAN), ("corria", P_HAL), ("imagino", P_SZABO))):
    LATIGO(ww(c, 1, palabra) - 0.25, ww(c, 1, palabra) + 0.35, pz_.x, pz_.y, 1.05, pz_.rot * 0.6, 0, 0)
    K(ww(c, 1, palabra) + 1.6, pz_.x, pz_.y + 20, 1.25, pz_.rot * 0.6, 0, 0)
for k, (palabra, pz_) in enumerate((("proclamo", P_WRIGHT), ("corrigio", P_TODD), ("recibio", P_BACK))):
    LATIGO(ww(c, 2, palabra) - 0.25, ww(c, 2, palabra) + 0.35, pz_.x, pz_.y, 1.05, pz_.rot * 0.6, 0, 0)
    K(ww(c, 2, palabra) + 1.4, pz_.x, pz_.y + 20, 1.25, pz_.rot * 0.6, 0, 0)
LATIGO(INI(c, 3) - 0.1, INI(c, 3) + 0.6, 0, 100, 0.75, 0, 0, 0)
K(ww(c, 3, "llave"), 400, 600, 0.95, 0, 3, 3)
K(INI(c, 4) + 0.2, 0, 200, 0.85, 0, 0, 0)
K(FIN(c, 4), 0, 250, 1.0, 0, 0, 0)
DENTRO(P_ESTAT, INI(c, 5) + 0.1, ww(c, 5, "desaparecer") + 0.3, FIN(c, 5) + 0.1)
K(INI(c, 6) + 0.6, 0, 130, 0.82, -1, 3, 3)
K(FIN(c, 6) + 1.0, 0, 110, 0.92, -1.5, 0, 0, modo="suave")
K(TOTAL, 0, 100, 1.0, -1.5, 0, 0)
