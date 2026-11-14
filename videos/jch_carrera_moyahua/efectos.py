# -*- coding: utf-8 -*-
"""Capa de EFECTOS del reel jch_carrera_moyahua (vertical 1080x1920): kit propio kit_jch.py (mapa real con la ruta, cintillo de
POSTURA, fichas, cifras, balanza neutral, créditos), rótulos de énfasis y SFX anclados a la voz.
NEUTRALIDAD (Edson, 10-nov-2026): el narrador no toma postura; las fichas dicen de quién es cada dato («según…»), los cintillos
«POSTURA» salen solo mientras hablan esas voces y la balanza oscila sin decidirse.
Zona segura de Facebook Reels: nada importante debajo de y≈.78 (pie y nombre) ni pegado a la derecha en la mitad baja (botones).
  python fab.py <v> fx --seco   ·   python fab.py <v> fx   ·   python fab.py <v> fx hoja
"""
import kit_jch as K

W, H = K.W, K.H

# ------------------------------------------------------------------ créditos de cada clip (arriba a la derecha)
CANAL = {
    "9nQiFRaa_Bs": "SanMykol", "_2HqpvYxpQ0": "Alice Reyes 97", "iEVShIFfAxQ": "Las Rutas Del Chris Motos",
    "HOanpy2EGo8": "Las Rutas Del Chris Motos", "QlVO3wmW0co": "DD ON THE ROAD", "7DzxoV41Hik": "CASTA HRC",
    "QtKiqBaPpcs": "INFO TV 9", "rCZEUvXwl8Y": "Paul Desing Cain", "BtEGl7aYdiU": "CAIN Road Race OFICIAL",
    "bE9qxBdOQtk": "Natanael DUKE790", "d-OqU-t6pME": "Rosy Rosy",
}
ARCHIVO_CAIDA = {"scene-019", "scene-034"}          # caídas reales de otro domingo: NO son las del piloto de la nota
SIN_CREDITO = {"scene-007", "scene-008"}             # bajo el mapa a pantalla completa (el mapa lleva su propio crédito)


def _creditos():
    import json
    fu = json.load(open("fuentes.json", encoding="utf-8"))
    out = []
    for i in range(1, 40):
        b = f"scene-{i:03d}"
        if b in SIN_CREDITO or b not in fu:
            continue
        txt = "Video: " + CANAL.get(fu[b]["video"], "YouTube")
        if b in ARCHIVO_CAIDA:
            txt += " · imagen de archivo"
        fn = K.credito(txt)
        w, h = fn(0, 1, []).shape[1::-1]
        out.append(dict(tipo="mg", fn=fn, de=b, a=f"{b}:fin", x=(W - 28 - w / 2) / W, y=(112 + h / 2) / H, sale=.05,
                        nombre="crédito " + b))
    return out


def postura(lado, de, a):
    fn = K.postura(lado)
    w = fn(2, 5, []).shape[1]
    return dict(tipo="mg", fn=fn, de=de, a=a, x=(24 + w / 2) / W, y=.165, sale=.05, nombre="postura " + lado)


def ficha(titulo, items, de, a, marcas, color=K.AMAR, y=.60):
    return dict(tipo="mg", fn=K.ficha(titulo, items, color), de=de, a=a, marcas=marcas, x=.5, y=y, sale=.05,
                nombre="ficha " + titulo.lower())


def cifra(num, texto, de, a, color=K.AMAR, sub=None, y=.42, desde=0):
    return dict(tipo="mg", fn=K.cifra(num, texto, color, sub, desde), de=de, a=a, x=.5, y=y, sale=.05,
                nombre=f"cifra {num} {texto.lower()}")


def mapa(de, a, marcas, nombre="mapa ruta"):
    return dict(tipo="pantalla", fn=K.mapa_ruta(), de=de, a=a, marcas=marcas, entra=.35, sale=.35, nombre=nombre)


CAMARA = {
    "scene-001": dict(a=(1.0, 0, 0), b=(1.10, 0, .1)),
    "scene-011": dict(a=(1.0, 0, 0), b=(1.14, 0, 0)),
    "scene-019": dict(a=(1.0, 0, 0), b=(1.18, 0, .1)),
    "scene-029": dict(a=(1.0, 0, 0), b=(1.12, 0, 0)),
    "scene-039": dict(a=(1.0, 0, 0), b=(1.10, 0, 0)),
}
FUNDIDO = {"scene-003": 0, "scene-012": 0, "scene-019": 0}

FX = _creditos() + [
    dict(tipo="abre", en=0, dur=.6),
    # ---------------- gancho
    ficha("DOMINGO 15 DE NOVIEMBRE", [("Carretera federal 23 cerrada", "x"), ("De 3 a 4 horas", "·")], de="scene-001",
          a="scene-002:fin", marcas=["cerrada", "Tres o cuatro"], color=K.ROJO, y=.58),
    dict(tipo="temblor", en="pleito", amp=26),
    dict(tipo="destello", en="Para una carrera"),
    # ---------------- qué es
    ficha("CAIN ROAD RACE MÉXICO 2026", [("Evento: 13 al 15 de noviembre", "·"), ("Carrera: domingo 15", "·"),
                                         ("Salidas desde el mediodía", "·")],
          de="scene-005", a="scene-006:fin", marcas=["trece", "domingo quince", "mediodía"], y=.60),
    mapa("scene-007", ("scene-008:fin", .1), ["desde la caseta", "ciento cinco"]),
    cifra(100, "PILOTOS", "cien pilotos", "Salen uno", sub="de 16 estados", y=.44),
    cifra(30, "SEGUNDOS", "cada treinta", "scene-010:fin", sub="entre una salida y otra · contra el reloj", y=.44),
    dict(tipo="destello", en="pueblo se divide"),
    dict(tipo="vineta", de="scene-011", a="scene-011:fin", fuerza=.6),
    # ---------------- postura EN CONTRA
    postura("contra", "scene-012", "scene-012:fin"),
    ficha("PROTECCIÓN CIVIL", [("Moyahua", "·"), ("Juchipila", "·"), ("Apozol", "·"),
                               ("«El Estado no nos incluyó en la planeación»", "x")],
          de="Protección Civil", a="scene-013:fin", marcas=[("Protección Civil", .6), "Juchipila", ("Juchipila", .7), "no los había"],
          color=K.ROJO, y=.58),
    cifra(4, "AMBULANCIAS", "cuatro ambulancias", "scene-014:fin", color=K.ROJO, sub="entre los tres municipios", y=.62),
    ficha("HOSPITAL DE JUCHIPILA", [("Cirujano", "x"), ("Anestesiólogo", "x"), ("Equipo de trauma", "x")],
          de="scene-015", a=("trauma|fin", .5), marcas=["cirujano", "anestesiólogo", "equipo de trauma"], color=K.ROJO, y=.56),
    cifra(10, "ACCIDENTES", "Calculan", "scene-016:fin", color=K.ROJO, sub="calculados por Protección Civil durante la carrera",
          y=.42),
    cifra(3, "ACCIDENTES DE MOTO", "scene-017", ("semana|fin", .4), color=K.ROJO, sub="a la semana en Moyahua, sin carrera",
          y=.42),
    dict(tipo="temblor", en="se cayó", amp=34),
    postura("contra", "scene-020", ("esperen|fin", .25)),
    ficha("SE DETIENEN 3-4 HORAS", [("Taxis a Guadalajara", "x"), ("Taxis a Zacatecas", "x")],
          de="los taxis", a=("esperen|fin", .25), marcas=["Guadalajara#2", ("Guadalajara#2", .9)], color=K.ROJO, y=.58),
    # ---------------- postura A FAVOR
    postura("favor", "A ver", "scene-021:fin"),
    ficha("SEGÚN LOS ORGANIZADORES", [("50 marshals", "v"), ("Ambulancias", "v"), ("Protección Civil", "v"),
                                      ("Guardia Nacional", "v")],
          de="Lo que dicen", a="scene-023:fin", marcas=["cincuenta", "ambulancias Protección", "Protección Civil y",
                                                       "Guardia Nacional"], color=K.VERDE, y=.60),
    ficha("REVISIÓN A CADA PILOTO", [("Traje de cuero completo", "v"), ("Casco certificado", "v"), ("Seguro", "v")],
          de="scene-024", a=("seguro|fin", .5), marcas=["traje de cuero", "casco", "seguro"], color=K.VERDE, y=.60),
    cifra(15000, "ESPECTADORES", "quince mil", "scene-026:fin", color=K.VERDE, sub="en una sola edición en Concordia, Sinaloa",
          y=.42, desde=1000),
    postura("favor", "los burritos", "scene-030:fin"),
    postura("favor", "Si sale bien", ("queda en el mapa", -.1)),
    mapa("queda en el mapa", ("carreras|fin", .4), [0.0, .9], nombre="mapa ruta (en el mapa)"),
    # ---------------- balanza (el narrador no decide)
    dict(tipo="mg", fn=K.balanza(), de="Las dos cosas", a="scene-034:fin", x=.5, y=.47, sale=.05, nombre="balanza"),
    # ---------------- consejos
    ficha("SI VAS EL DOMINGO 15", [("Si viajas, sal temprano", "·"), ("Entrada gratis", "v"), ("Llega antes de las 10", "·"),
                                   ("No te pares en la salida de las curvas", "x"), ("No cruces la carretera", "x")],
          de="scene-035", a="scene-037:fin", marcas=["sal temprano", "gratis", "antes de las diez", "no te pares", "no cruces"],
          y=.55),
    dict(tipo="cierra", en=("scene-039:fin", -.6), dur=.6),
]


def _ajusta(rotulos, maxw=960):
    """Rótulos en vertical: «A / B» = dos líneas; cada línea se achica hasta caber en `maxw` px (fuente Poppins Black)."""
    import os
    from PIL import ImageFont
    ruta = next((p for p in (os.path.join(os.environ.get("LOCALAPPDATA", ""), "Microsoft", "Windows", "Fonts", "Poppins-Black.ttf"),
                             "C:/Windows/Fonts/Poppins-Black.ttf", "C:/Windows/Fonts/seguibl.ttf") if os.path.exists(p)))
    out = []
    for r in rotulos:
        lineas = [l.strip() for l in r["texto"].split(" / ")]
        tam = r.get("tam", 150)
        for l in lineas:
            while tam > 40:
                x0, _, x1, _ = ImageFont.truetype(ruta, tam).getbbox(l)
                if x1 - x0 <= maxw:
                    break
                tam -= 4
        paso = tam * 1.12 / H
        y0 = r.get("y", .5) - paso * (len(lineas) - 1) / 2
        for i, l in enumerate(lineas):
            out.append(dict(r, texto=l, tam=tam, y=round(y0 + i * paso, 4)))
    return out


ROTULOS = _ajusta([
    dict(texto="CERRADA", en="cerrada", a="scene-001:fin", tam=190, color="rojo", y=.36),
    dict(texto="¿PARA QUÉ?", en="Para qué", a="scene-002:fin", tam=150, color="amarillo", y=.30),
    dict(texto="UNA CARRERA / DE MOTOS", en="Para una carrera", a="pleito", tam=110, color="amarillo", y=.30),
    dict(texto="Y YA HAY PLEITO", en="pleito", a="scene-003:fin", tam=130, color="rojo", y=.40),
    dict(texto="CAIN ROAD RACE", en="Caín Road Race", a="primera vez", tam=140, color="amarillo", y=.34),
    dict(texto="1.ª VEZ EN ZACATECAS", en="primera vez", a="scene-004:fin", tam=110, color="crema", y=.34),
    dict(texto="EL PUEBLO / SE DIVIDE", en="pueblo se divide", a="scene-011:fin", tam=130, color="crema", y=.40),
    dict(texto="¿POR DÓNDE / LO SACAMOS?", en="Por dónde", a="scene-012:fin", tam=100, color="crema", y=.45),
    dict(texto="YA SE CAYÓ / UN PILOTO", en="se cayó", a="scene-019:fin", tam=110, color="rojo", y=.42),
    dict(texto="SIN REGLAS / SIN AMBULANCIAS", en="Sin reglas", a="scene-021:fin", tam=90, color="crema", y=.45),
    dict(texto="CONCORDIA, SINALOA", en="Concordia", a=("dos mil dieciséis", -.1), tam=110, color="crema", y=.40),
    dict(texto="DESDE 2016", en="dos mil dieciséis", a="quince mil", tam=110, color="crema", y=.40),
    dict(texto="COME", en="que come", a="scene-027:fin", tam=120, color="amarillo", y=.32),
    dict(texto="DUERME", en="que duerme", a="scene-027:fin", tam=120, color="amarillo", y=.40),
    dict(texto="CARGA GASOLINA", en="que carga", a="scene-027:fin", tam=120, color="amarillo", y=.48),
    dict(texto="HOTEL SEDE / EN APOZOL", en="El hotel sede", a="los burritos", tam=100, color="crema", y=.40),
    dict(texto="LOS BURRITOS / DE MOYAHUA", en="los burritos", a="scene-028:fin", tam=100, color="amarillo", y=.42),
    dict(texto="¿NUEVO LEÓN?", en="Nuevo León", a="scene-029:fin", tam=120, color="crema", y=.42),
    dict(texto="¿YUCATÁN?", en="Yucatán", a="scene-030:fin", tam=130, color="crema", y=.42),
    dict(texto="MAYO 2027", en="mayo de", a="scene-031:fin", tam=150, color="amarillo", y=.40),
    dict(texto="LAS DOS COSAS / SON CIERTAS", en="Las dos cosas", a="scene-032:fin", tam=96, color="crema", y=.15),
    dict(texto="¿DE QUÉ LADO / ESTÁS?", en="de qué lado", a="scene-039:fin", tam=120, color="amarillo", y=.36),
    dict(texto="TE LEO EN / LOS COMENTARIOS", en="Te leo", a="scene-038:fin", tam=100, color="crema", y=.50),
    dict(texto="CON RESPETO: / AQUÍ TODOS / SOMOS VECINOS", en="Con respeto", a="scene-039:fin", tam=100, color="crema", y=.61),
])

SFX = {
    "moto_pasa": ("A sport motorcycle passing by fast on a mountain road, loud engine roar doppler, realistic", 3),
    "sirena": ("Short distant ambulance siren wail, two cycles, realistic, outdoors", 3),
    "tic": ("Stopwatch ticking fast, crisp clock ticks, dry", 3),
    "balanza": ("Old metal balance scale creaking and swinging gently, small metallic squeaks", 4),
    "caida": ("Motorcycle sliding and crashing on asphalt, metal scraping, short, realistic", 3),
}
PISTAS = [
    dict(sfx="golpe", en="cerrada", vol=.55),
    dict(sfx="whoosh", en="Para qué", vol=.45),
    dict(sfx="moto_pasa", en="Para una carrera", vol=.5),
    dict(sfx="golpe", en="pleito", vol=.6),
    dict(sfx="sello", en="Caín Road Race", vol=.45),
    dict(sfx="pop", en="trece", vol=.4),
    dict(sfx="pop", en="domingo quince", vol=.4),
    dict(sfx="whoosh", en="scene-007", vol=.45),
    dict(sfx="datos", en="Noventa y siete", vol=.45),
    dict(sfx="pop", en="cien pilotos", vol=.45),
    dict(sfx="tic", en="cada treinta", vol=.35),
    dict(sfx="golpe", en="pueblo se divide", vol=.6),
    dict(sfx="whoosh", en="scene-012", vol=.45),
    dict(sfx="pop", en="Juchipila", vol=.35),
    dict(sfx="sirena", en="cuatro ambulancias", vol=.28),
    dict(sfx="pop", en="cirujano", vol=.35),
    dict(sfx="pop", en="anestesiólogo", vol=.35),
    dict(sfx="pop", en="equipo de trauma", vol=.35),
    dict(sfx="caida", en=("se cayó", -.25), vol=.4),
    dict(sfx="whoosh", en="A ver", vol=.45),
    dict(sfx="pop", en="cincuenta", vol=.4),
    dict(sfx="pop", en="traje de cuero", vol=.35),
    dict(sfx="datos", en="quince mil", vol=.4),
    dict(sfx="moto_pasa", en="mayo de", vol=.35),
    dict(sfx="balanza", en="Las dos cosas", vol=.4),
    dict(sfx="pop", en="gratis", vol=.35),
    dict(sfx="whoosh", en="de qué lado", vol=.45),
]
