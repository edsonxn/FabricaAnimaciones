# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «El Carpintero que lo Perdió Todo… e Inventó LEGO» (secuencia Flow, Plastitube, 3-nov-2026).
Pedido del usuario (3-nov): sobre los 3 min de CLIPS, capa LIGERA («que el video siga siendo protagonista»: ~1 cada 30-40 s,
1/3-1/2 de pantalla); en la parte de SOLO IMÁGENES, MÁS densa (pegatinas, fotos, MG, rótulos) para hacerla dinámica.
- Fotos REALES de Wikimedia Commons en pegatinas/ (Ole Kirk 1957, su familia, su casa de 1924, Godtfred, la patente US3005282,
  ladrillos Kiddicraft y Bri-Plax de Hilary Page, Legoland 1968, la minifigura de 1978, un 2x4, juguetes de madera originales
  de la colección de LEGO House: «History Collection of Lego House 02/03»).
- MG propios del canal: nucleo/mg_plasti.py (línea de los 3 incendios, contadores, pirámide de ladrillos).
- Estilos de pegatina variados: nucleo/peg_estilos.py con tema "plasti".
  python fab.py lego_carpintero fx --seco   tiempos      python fab.py lego_carpintero fx hoja   previews/fx_NN.jpg
"""
import os

import mg_plasti as K
import mg_tes as T
import mg_wow as W
import peg_estilos as PE

VIVO_AUTO = 12   # parallax suave en todas las imágenes sin FX vivo

CAMARA = {}
FUNDIDO = {}
PALETA = {"amarillo": (255, 205, 0), "crema": (250, 244, 228), "rojo": (214, 32, 40)}

_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")


def P(nombre):
    return os.path.join(_PEG, nombre)


def peg(en, img, titulo, dur=4.5, x=.18, y=.60, tam=420, giro=-6.0):
    """Pegatina clásica (foto real con borde blanco), abajo a la izquierda por defecto."""
    return dict(tipo="mg", fn=T.pegatina(P(img), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + img, ver=1.0)


def cam(en, img, nombre=None, dur=4.5, x=.16, y=.68, tam=320, foco=(.5, .25, 2.0)):
    """Medallón redondo para las personas reales."""
    return dict(tipo="mg", fn=PE.camafeo(P(img), nombre, tam, foco, tema="plasti"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + img, ver=1.0)


def ban(en, img, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=5.0, y=.5, lado="der"):
    """Tira de cine a todo lo ancho con el rostro en primer plano."""
    return dict(tipo="mg", fn=PE.banda(P(img), nombre, sub, foco, lado=lado, tema="plasti"), en=en, dur=dur, x=.5, y=y,
                sale=.35, nombre="pegatina " + img, ver=1.2)


def leg(img, titulo, lineas, de, a, marcas=(), sello=None, x=.22, y=.52, ancho=520, giro=3.5):
    """Expediente en papel con la foto en sepia, datos y sello."""
    return dict(tipo="mg", fn=PE.legajo(P(img), titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema="plasti"), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="pegatina " + img, ver=1.2)


def pant(img, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    """Foto REAL a cuadro entero (Legoland desde el aire)."""
    return dict(tipo="pantalla", fn=W.pantalla(P(img), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla " + img, ver=2.0)


def mg(fn, de, a, nombre, marcas=(), x=.5, y=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def rot(texto, en, tam=110, color="amarillo", y=.18):
    return dict(texto=texto, en=en, tam=tam, color=color, y=y)


INCENDIOS = [(1924, "El taller y la casa"), (1942, "La fábrica y los planos"), (1960, "Los juguetes de madera")]

FX = [
    # ======== ZONA DE CLIPS (0-3 min): ligera, ~1 cada 30-40 s, sin tapar el centro
    mg(K.contador(1140, "piezas por segundo", "Hoy se fabrican", w=760), "Cada segundo", "Cada segundo|fin", "piezas por segundo",
       x=.78, y=.24),
    mg(K.linea("Tres incendios", INCENDIOS, icono="fuego"), "Esta es una historia de tres incendios",
       "De un pato de madera", "tres incendios", marcas=["tres incendios", ("tres incendios", .6), ("tres incendios", 1.2)], y=.70),
    cam("Esta es la historia de LEGO", "ole_1957.jpg", "Ole Kirk Christiansen", dur=5.0, x=.83, y=.68),
    peg("Tiene cuatro hijos", "ole_familia.png", "La familia, años 30", dur=5.0, x=.80, y=.60, giro=5.0),
    peg("Levanta un taller más grande", "ole_hus.jpg", "Su casa de 1924, hoy museo", dur=5.0, x=.20, y=.62),
    dict(tipo="temblor", en="el fuego se come el taller entero", amp=18),

    # ======== ZONA DE IMÁGENES (desde ~3 min): más densa
    peg("empieza a hacer juguetes baratos", "juguetes_madera.jpg", "Juguetes LEGO de madera, años 30", dur=5.0, x=.78, y=.60, tam=460, giro=5.0),
    peg("Si la gente no puede comprar una mesa", "trenes_madera.jpg", "Trenes de madera (LEGO House)", dur=4.0, x=.22, y=.62, tam=420),
    dict(tipo="destello", en="el nombre de su marca", color="amarillo", fuerza=.5),
    peg("Su juguete estrella es un pato", "ole.png", "Ole Kirk en su oficina", dur=4.0, x=.80, y=.30, tam=360, giro=4.0),
    ban("Un día, su hijo Godtfred", "godtfred.jpg", "Godtfred", "el hijo · ayudaba desde los 12 años", foco=(.5, .22, 2.4), y=.78),
    dict(tipo="temblor", en="un cortocircuito incendia la fábrica", amp=22),
    dict(tipo="tinte", de="un cortocircuito incendia la fábrica", a="Es el segundo incendio|fin", color="rojo", k=.12),
    peg("unos ladrillos de plástico ingleses", "kiddicraft_4x2.jpg", "Kiddicraft, 1947", dur=4.5, x=.80, y=.58, tam=440),
    leg("briplax_1939.jpg", "Hilary Page", ["Juguetero inglés", "Primeros bloques: 1939", "Marca: Kiddicraft"],
        "Los inventó un juguetero", "En mil novecientos cuarenta y nueve, LEGO saca", x=.22),
    peg("LEGO saca sus propios ladrillos", "kiddicraft_lego.jpg", "Kiddicraft y LEGO, lado a lado", dur=5.0, x=.76, y=.56, tam=480),
    dict(tipo="desaturar", de="Y son un fracaso", a="Para muchos, es un capricho|fin", k=.45),
    mg(K.contador(1955, "", "Sistema de juego", desde=1950, w=620, color=K.AZUL), "presentan el Sistema de Juego",
       "Son un mundo|fin", "1955", x=.80, y=.24),
    peg("registran la patente", "patente_p1.png", "Patente: 28 de enero de 1958", dur=6.0, x=.24, y=.52, tam=560, giro=-4.0),
    cam("Ole Kirk llega a verlo", "ole_1957.jpg", "1891 - 1958", dur=7.5, x=.80, y=.62, tam=360),
    cam("Hilary Page no vio nada de esto", "briplax_1939.jpg", "Hilary Page", dur=5.0, x=.18, y=.66, foco=(.5, .55, 1.6)),
    mg(K.linea("Tres incendios", INCENDIOS, icono="fuego"), "En febrero de mil novecientos sesenta",
       "Al día siguiente", "tres incendios (2)", marcas=[("En febrero de mil novecientos sesenta", .2), ("En febrero de mil novecientos sesenta", .7), "el fuego destruye el almacén"], y=.72),
    cam("Godtfred les compra su parte", "godtfred.jpg", "Godtfred, al frente", dur=4.5, x=.82, y=.66, foco=(.5, .2, 2.4)),
    pant("legoland_aereo_1968.jpg", "abre Legoland", "Un parque con ciudades|fin", zoom=(1.0, 1.15)),
    peg("Un parque con ciudades", "legoland_miniland_1968.jpg", "Legoland, 1968", dur=5.0, x=.76, y=.58, tam=520),
    peg("llegan los muñequitos de plástico", "minifig_patente.png", "La minifigura (1978)", dur=4.5, x=.20, y=.56, tam=440),
    peg("las minifiguras", "lego_town_588.jpg", "Sets de 1978", dur=4.0, x=.80, y=.62, tam=420, giro=5.0),
    dict(tipo="desaturar", de="En dos mil cuatro, la empresa pierde", a="Venden los parques|fin", k=.5),
    mg(K.contador(36000000000, "piezas al año", "Cada año se fabrican"), "Fabrica unos treinta y seis mil millones",
       "Y con solo seis ladrillos", "36 mil millones", y=.30),
    mg(K.ladrillos(6, "Seis ladrillos de 2x4", "915 millones de combinaciones"), "Y con solo seis ladrillos",
       "Y una buena parte|fin", "combinaciones", y=.48),
    mg(K.contador(7000, "trabajadores", "Nuevo León · desde 2008", w=760, color=K.ROJO), "con más de siete mil trabajadores",
       "Solo en dos mil veinticinco|fin", "7 000 trabajadores", x=.78, y=.26),
    mg(K.contador(149000000, "cajas en 2025", "Salieron de Nuevo León"), "Solo en dos mil veinticinco",
       "Y en septiembre de dos mil veintiséis|fin", "149 millones", x=.5, y=.30),
    mg(K.linea("Tres incendios", INCENDIOS, icono="fuego"), "Que vio arder su trabajo tres veces",
       "Y que, cuando su familia|fin", "tres incendios (3)", marcas=[("Que vio arder su trabajo", .1), ("Que vio arder su trabajo", .6), "tres veces"], y=.72),
    # imágenes vivas (4-nov, hojas previews/vivo_0N.jpg mirándolas: fuera 026/039/049/051/067/078/087, el recorte arrastraba mesa, barco o cubierta)
    dict(tipo="vivo", beat="scene-021", anim="respira", capa=[0]),
    dict(tipo="vivo", beat="scene-034", anim="respira", capa=[1]),
    dict(tipo="vivo", beat="scene-045", anim="respira"),
    dict(tipo="vivo", beat="scene-058", anim="flota", capa=[0]),
    dict(tipo="vivo", beat="scene-071", anim="balanceo", capa=[1]),
    dict(tipo="vivo", beat="scene-073", anim="respira", capa=[0]),
    dict(tipo="vivo", beat="scene-081", anim="respira"),
    dict(tipo="vivo", beat="scene-091", anim="balanceo"),
]

ROTULOS = [
    rot("LEG GODT", "Junta dos palabras danesas", tam=140, y=.20),
    rot("= JUEGA BIEN", "que significan juega bien", tam=96, color="crema", y=.32),
    rot("LEGO = «YO ARMO»", "en latín, lego quiere decir", tam=96, y=.20),
    rot("3 CAPAS DE BARNIZ", "Cada pato lleva tres capas de barniz", tam=100, y=.18),
    rot("«SOLO LO MEJOR ES", "solo lo mejor es suficientemente bueno", tam=84, y=.16),
    rot("SUFICIENTEMENTE BUENO»", "solo lo mejor es suficientemente bueno", tam=84, y=.26),
    rot("MÁS DEL DOBLE", "Le cuesta más del doble", tam=120, y=.18),
    rot("DE LO QUE GANÓ EL AÑO ANTERIOR", "Le cuesta más del doble", tam=64, color="crema", y=.28),
    rot("«NUNCA»", "el plástico nunca va a reemplazar", tam=170, color="rojo", y=.22),
    rot("FALTA UN SISTEMA", "a los juguetes les falta un sistema", tam=110, y=.18),
    rot("1981", "En mil novecientos ochenta y uno", tam=150, y=.20),
    rot("SOLO PLÁSTICO", "Solo ladrillos de plástico", tam=120, y=.18),
    rot("2004: CASI EN QUIEBRA", "estuvo casi en quiebra", tam=96, color="rojo", y=.18),
    rot("+400 MILLONES DE DÓLARES", "cuatrocientos millones de dólares", tam=84, y=.20),
]

SFX = {}
PISTAS = []
