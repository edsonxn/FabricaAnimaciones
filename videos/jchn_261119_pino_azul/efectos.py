# -*- coding: utf-8 -*-
"""Capa de EFECTOS del primer reel diario de «Noticias de Juchipila» (vertical 1080x1920). Kit propio kit_nj.py (colores del logo).
SUBTÍTULOS grandes con la palabra que suena en amarillo = EXCEPCIÓN a R13 solo para esta página (Edson, 19-nov-2026).
Zona segura de Facebook Reels: nada importante debajo de y≈.78 (pie y nombre) ni pegado a la derecha en la mitad baja (botones).
  python fab.py <v> fx --seco   ·   python fab.py <v> fx   ·   python fab.py <v> fx hoja
"""
import json
import re
import kit_nj as K

W, H = K.W, K.H
PALETA = {"amarillo": (255, 204, 0), "crema": (241, 240, 230), "marino": (13, 24, 41), "rojo": (200, 35, 29)}
F = "fuente/fotos/"
PEG = "E:/PaginaFace/paginas/noticias_jch/arte/pegatinas/"

# ------------------------------------------------------------------ créditos de cada foto (arriba a la derecha)
PINIDAE = "Foto: pinidae / Wikimedia Commons, CC BY-SA 4.0"
CREDITOS = {
    "scene-001": PINIDAE, "scene-002": PINIDAE, "scene-005": PINIDAE, "scene-006": PINIDAE, "scene-007": PINIDAE,
    "scene-009": PINIDAE, "scene-010": PINIDAE, "scene-011": PINIDAE, "scene-013": PINIDAE, "scene-014": PINIDAE,
    "scene-003": "Foto: Ruff tuff cream puff / Commons, CC0 · ejemplar cultivado",
    "scene-008": "Foto: ferbio_dgo / Commons, CC BY-SA 4.0 · piña de Durango",
}


def _creditos():
    out = []
    for b, txt in CREDITOS.items():
        fn = K.credito(txt)
        w, h = fn(0, 1, []).shape[1::-1]
        out.append(dict(tipo="mg", fn=fn, de=b, a=f"{b}:fin", x=(W - 24 - w / 2) / W, y=(150 + h / 2) / H, sale=.05,
                        nombre="crédito " + b))
    return out


# ------------------------------------------------------------------ subtítulos (de timeline.json, palabra por palabra)
NUMEROS = [("mil novecientos sesenta y cuatro", "1964"), ("dos mil quinientos", "2 500"), ("dos mil diez", "2010"),
           ("dos mil", "2 000"), ("doscientos veinte", "220"), ("cuarenta", "40")]
SUB_HASTA = 50.0          # desde la pregunta final manda la tarjeta de cierre (ya trae la pregunta escrita)


def _palabras():
    tl = json.load(open("timeline.json", encoding="utf-8"))
    ws = [[w["w"], w["s"], w["e"]] for e in tl["escenas"] for f in e["frases"] for w in f["words"]]
    out, i = [], 0
    while i < len(ws):
        for frase, cifra in NUMEROS:          # cifras en número, como se leen más rápido
            n = len(frase.split())
            if " ".join(re.sub(r"[^\wáéíóúñ]", "", w[0].lower()) for w in ws[i:i + n]) == frase:
                fin = re.sub(r"[\wáéíóúñ]+$", "", ws[i + n - 1][0])
                out.append([cifra + re.sub(r"^[\wáéíóúÁÉÍÓÚñÑ]+", "", ws[i + n - 1][0]), ws[i][1], ws[i + n - 1][2]])
                i += n
                break
        else:
            out.append(list(ws[i]))
            i += 1
    return out


def _subtitulos():
    pal = [p for p in _palabras() if p[1] < SUB_HASTA]
    grupos, g = [], []
    for p in pal:
        g.append(p)
        largo = sum(len(x[0]) + 1 for x in g)
        if len(g) >= 4 or largo > 20 or p[0][-1] in ".,?!:" or p is pal[-1]:
            grupos.append(g)
            g = []
    out = []
    for k, g in enumerate(grupos):
        de = g[0][1] - .04
        a = grupos[k + 1][0][1] - .04 if k + 1 < len(grupos) and grupos[k + 1][0][1] - g[-1][2] < .6 else g[-1][2] + .35
        fn = K.subtitulo([(t, s - de, e - de) for t, s, e in g])
        out.append(dict(tipo="mg", fn=fn, de=round(de, 3), a=round(min(a, SUB_HASTA), 3), x=.5, y=.705, sale=.0,
                        nombre="sub " + " ".join(t for t, _, _ in g)))
    return out


def cifra(num, etiqueta, de, a, sub=None, desde=0, y=.42, miles=True):
    return dict(tipo="mg", fn=K.cifra(num, etiqueta, sub, desde, miles=miles), de=de, a=a, x=.5, y=y, sale=.05,
                nombre=f"cifra {num} {etiqueta.lower()}")


def pegatina(nombre, en, a, x, y, ancho=290):
    return dict(tipo="imagen", ruta=PEG + nombre + ".png", de=en, a=a, x=x, y=y, ancho=ancho, anim="fade", entra=.25, sale=.2)


CAMARA = {
    "scene-001": dict(a=(1.0, 0, 0), b=(1.12, .1, -.1)),
    "scene-002": dict(a=(1.15, 0, .1), b=(1.0, 0, 0)),
    "scene-005": dict(a=(1.0, 0, 0), b=(1.18, 0, -.1)),
    "scene-008": dict(a=(1.0, 0, .1), b=(1.12, 0, -.1)),
    "scene-011": dict(a=(1.0, 0, .2), b=(1.16, 0, -.2)),
    "scene-014": dict(a=(1.12, 0, 0), b=(1.0, 0, 0)),
}
FUNDIDO = {"scene-002": 0, "scene-008": 0, "scene-014": 0}

FX = _creditos() + [
    dict(tipo="abre", en=0, dur=.5),
    # logo de la página en la esquina todo el reel (la tarjeta final lo trae grande)
    dict(tipo="imagen", ruta="arte/logo_esquina.png", de=0, a="scene-015", x=.105, y=.07, ancho=182, entra=.4),
    # ---------------- gancho
    dict(tipo="destello", en="ningún otro lugar", fuerza=.45),
    # ---------------- contexto
    dict(tipo="pantalla", fn=K.mapa_sierra(F + "Pinus_maximartinezii_Sierra_de_Morones_Juchipila_Zacatecas_1.jpg"),
         de=("Vive en", -.1), a="scene-004:fin", marcas=["Cerro de Piñones"], entra=.3, sale=.3, nombre="mapa sierra"),
    dict(tipo="vineta", de="scene-006", a="scene-007:fin", fuerza=.45),
    # ---------------- lo jugoso
    cifra(2500, "ÁRBOLES ADULTOS", ("dos mil", -.05), "scene-010:fin", sub="se calculan entre 2 000 y 2 500", desde=2000, y=.40),
    cifra(220, "AÑOS", "doscientos veinte", "scene-011:fin", sub="los árboles más altos, de más de 9 metros", miles=False, y=.40),
    dict(tipo="pantalla", fn=K.mapa_region(), de="scene-012", a="scene-012:fin", entra=.3, sale=.3, nombre="mapa durango"),
    dict(tipo="mg", fn=K.comparativa([("SIERRA DE MORONES", "2 000 – 2 500", 2500, K.AMAR),
                                      ("DURANGO", "MÁS DE 900", 900, K.CREMA)], "ÁRBOLES ADULTOS"),
         de="el de aquí", a="scene-013:fin", x=.5, y=.47, sale=.05, nombre="comparativa"),
    # ---------------- cierre
    dict(tipo="desaturar", de="scene-014", a="scene-014:fin", k=.6, entra=.4),
    dict(tipo="vineta", de="scene-014", a="scene-014:fin", color="rojo", fuerza=.25),
    dict(tipo="mg", fn=K.sello("EN PELIGRO", "DE EXTINCIÓN · NOM-059 · UICN"), de="peligro", a="scene-014:fin", x=.5, y=.30,
         sale=.05, nombre="sello peligro"),
    pegatina("fuego", "fuego", "scene-014:fin", .3, .5),
    pegatina("vaca", "ganado", "scene-014:fin", .7, .5),
    dict(tipo="pantalla", fn=K.cierre("¿Usted ya / lo conocía?", ["Fuentes: Acta Botánica Mexicana (2011) · RBGE",
                                                                 "Fotos: Wikimedia Commons · Mapas: © OpenStreetMap"]),
         de="scene-015", a="scene-016:fin", entra=.4, sale=0, nombre="tarjeta cierre"),
    dict(tipo="cierra", en=("scene-016:fin", -.5), dur=.5),
] + _subtitulos()


def _ajusta(rotulos, maxw=960):
    """«A / B» = dos líneas; cada línea se achica hasta caber en `maxw` px (Poppins Black)."""
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
                if x1 - x0 + (tam * 1.4 if r.get("caja") else 0) <= maxw:
                    break
                tam -= 4
        paso = tam * 1.15 / H if not r.get("caja") else tam * 2.0 / H
        y0 = r.get("y", .5) - paso * (len(lineas) - 1) / 2
        for i, l in enumerate(lineas):
            out.append(dict(r, texto=l, tam=tam, y=round(y0 + i * paso, 4)))
    return out


ROTULOS = _ajusta([
    dict(texto="SIERRA DE MORONES · JUCHIPILA", en=.5, a="scene-001:fin", tam=46, color="marino", caja="amarillo", y=.22, pop=0),
    dict(texto="CASI EN NINGÚN / OTRO LUGAR / DEL MUNDO", en="ningún otro lugar", a="scene-002:fin", tam=120, color="crema", y=.32),
    dict(texto="PINO AZUL", en="pino azul", a=("Vive en", -.1), tam=170, color="amarillo", y=.30),
    dict(texto="Pinus maximartinezii", en=("pino azul", .3), a=("Vive en", -.1), tam=56, color="crema", fuente="semi", y=.385, pop=0),
    dict(texto="1964", en="mil novecientos", a="scene-005:fin", tam=260, color="amarillo", y=.27),
    dict(texto="LO DESCRIBIÓ EL BOTÁNICO J. RZEDOWSKI", en=("mil novecientos", .4), a="scene-005:fin", tam=40, color="marino",
         caja="crema", y=.38, pop=0),
    dict(texto="CON ÁRBOLES DEL CERRO DE PIÑONES", en="ese cerro", a=("Y por", -.05), tam=40, color="marino", caja="amarillo",
         y=.25, pop=0),
    dict(texto="MÁS DE 40 AÑOS", en="cuarenta", a="scene-007:fin", tam=130, color="crema", y=.30),
    dict(texto="SE CREÍA QUE / SOLO EXISTÍA AQUÍ", en="solo existía", a="scene-007:fin", tam=96, color="amarillo", y=.42),
    dict(texto="LAS PIÑAS / MÁS GRANDES", en="más grandes", a="scene-008:fin", tam=130, color="amarillo", y=.27),
    dict(texto="DE TODOS LOS PINOS PIÑONEROS DEL MUNDO", en="pinos piñoneros", a="scene-008:fin", tam=40, color="marino",
         caja="crema", y=.39, pop=0),
    dict(texto="EL MÁS GRANDE / ESTÁ AQUÍ", en="el de aquí", a="scene-013:fin", tam=120, color="amarillo", y=.24),
])

SFX = {
    "nj_viento": ("Gentle mountain wind through pine needles, distant birds chirping, calm natural ambience, no music", 22),
    "nj_cama": ("Calm warm acoustic documentary background music, soft nylon guitar arpeggios and light strings, "
                "gentle and hopeful, seamless loop, instrumental", 22),
    "nj_tension": ("Low dark cinematic drone with a slow tense pulse, ominous, no melody", 6),
    "nj_golpe": ("Deep soft cinematic boom hit, short warm low impact", 2),
    "nj_whoosh": ("Quick soft airy whoosh transition, clean", 1.2),
    "nj_pop": ("Small soft UI pop click, clean, subtle", 0.6),
    "nj_sello": ("Rubber stamp slammed hard on paper on a wooden desk, single thud", 1.2),
    "nj_contador": ("Fast soft mechanical counter ticking, numbers rolling, short", 1.5),
    "nj_fuego": ("Crackling brush fire flames, short", 2),
    "nj_vaca": ("A single cow mooing in an open field, distant, realistic", 2),
}
PISTAS = [
    dict(sfx="nj_cama", de=0, a="scene-013:fin", vol=.17),
    dict(sfx="nj_viento", de=0, a="scene-003", vol=.30),
    dict(sfx="nj_golpe", en="ningún otro lugar", vol=.55),
    dict(sfx="nj_pop", en="pino azul", vol=.4),
    dict(sfx="nj_whoosh", en=("Vive en", -.1), vol=.45),
    dict(sfx="nj_pop", en="Cerro de Piñones", vol=.4),
    dict(sfx="nj_golpe", en="mil novecientos", vol=.45),
    dict(sfx="nj_pop", en="cuarenta", vol=.35),
    dict(sfx="nj_whoosh", en="scene-008", vol=.4),
    dict(sfx="nj_pop", en="más grandes", vol=.4),
    dict(sfx="nj_contador", en="dos mil", vol=.35),
    dict(sfx="nj_contador", en="doscientos veinte", vol=.35),
    dict(sfx="nj_whoosh", en="scene-012", vol=.45),
    dict(sfx="nj_pop", en="el de aquí", vol=.4),
    dict(sfx="nj_tension", de="scene-014", a="scene-014:fin", vol=.30),
    dict(sfx="nj_sello", en="peligro", vol=.6),
    dict(sfx="nj_fuego", en="fuego", vol=.35),
    dict(sfx="nj_vaca", en="ganado", vol=.30),
    dict(sfx="nj_cama", de="scene-015", a="scene-016:fin", vol=.17),
    dict(sfx="nj_golpe", en="scene-015", vol=.4),
]
