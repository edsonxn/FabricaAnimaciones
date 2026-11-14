# -*- coding: utf-8 -*-
"""Capa de EFECTOS del reel jch_gorditas (vertical 1080x1920): kit_gor.py (mapa «te queda de paso», pizarra de fonda, sello,
tacómetro, cartel) + kit_jch.py (fichas, cifras, créditos), fotos REALES de Facebook (Gorditas Doña Chenda / Doña Yolis) como
pantalla o pegatina con su crédito, rótulos de énfasis y SFX anclados a la voz.
Zona segura de Facebook Reels: nada importante debajo de y≈.78 (pie y nombre) ni pegado a la derecha en la mitad baja (botones).
  python fab.py <v> fx --seco   ·   python fab.py <v> fx   ·   FAB_FX_FINAL=1 python fab.py <v> fx hoja
"""
import os
import cv2
import numpy as np
from PIL import Image, ImageFilter
import kit_jch as K
import kit_gor as G

W, H = K.W, K.H
AQ = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(AQ, "pegatinas")
_PAN = os.path.join(AQ, "pantallas")
TEMA_PEG = "plasti"      # cálido: amarillo, rojo y papel

# ------------------------------------------------------------------ créditos de cada clip (arriba a la derecha)
CANAL = {
    "1VxwdPaFuoo": "Caxcán Online", "5A-tV6-F0zI": "Rosy Rosy", "5bNZspnZTIE": "Vicky Cocina y Jardín", "7DzxoV41Hik": "CASTA HRC",
    "9nQiFRaa_Bs": "SanMykol", "CZKb0xKPyIU": "Rosy Rosy", "HOanpy2EGo8": "Las Rutas Del Chris Motos",
    "J6vZRk1-f9M": "Bien Chulo Zacatecas", "b8ADq8B7kqo": "Las riquezas de nuestro lindo México", "d-OqU-t6pME": "Rosy Rosy",
    "myMD6B4wx8A": "Daniel RC", "pu6amlAuHvk": "Periódico Mi Tierra", "tVovSCNRmuE": "chico bolero publicitario",
}
SIN_CREDITO = {"scene-005", "scene-006", "scene-007", "scene-008",      # bajo el mapa a pantalla completa
               "scene-013", "scene-015", "scene-024", "scene-049"}                                # bajo una foto a pantalla completa (lleva la suya)
CHENDA, YOLIS = "Foto: Gorditas Doña Chenda (Facebook)", "Foto: Gorditas Doña Yolis (Facebook)"


def _creditos():
    import json
    fu = json.load(open(os.path.join(AQ, "fuentes.json"), encoding="utf-8"))
    bs = json.load(open(os.path.join(AQ, "busquedas.json"), encoding="utf-8"))
    out = []
    for i in range(1, 53):
        b = f"scene-{i:03d}"
        if b in SIN_CREDITO:
            continue
        vid = (fu.get(b) or {}).get("video") or (bs.get(b) or {}).get("url", "")[-11:]
        out.append(credito("Video: " + CANAL.get(vid, "YouTube"), b, f"{b}:fin"))
    return out


def credito(txt, de, a, lado="der"):
    fn = K.credito(txt)
    w, h = fn(0, 1, []).shape[1::-1]
    x = (W - 28 - w / 2) / W if lado == "der" else (28 + w / 2) / W
    y = (112 + h / 2) / H if lado == "der" else (170 + h / 2) / H
    return dict(tipo="mg", fn=fn, de=de, a=a, x=x, y=y, sale=.05, nombre=f"crédito {de} {txt[:18]}")


# ------------------------------------------------------------------ fotos reales
def _pantalla_v(ruta, zoom=(1.0, 1.07)):
    """Foto a cuadro entero en VERTICAL: entera (cabe en .94 W × .66 H) sobre ella misma desenfocada y oscurecida, con un
    acercamiento lento. Para fotos de redes que no son 9:16."""
    zm = max(zoom)
    bw, bh = int(W * zm), int(H * zm)
    im = Image.open(ruta).convert("RGB")
    e = max(bw / im.width, bh / im.height)
    base = im.resize((int(im.width * e) + 1, int(im.height * e) + 1), Image.LANCZOS)
    base = base.crop(((base.width - bw) // 2, (base.height - bh) // 2, (base.width - bw) // 2 + bw, (base.height - bh) // 2 + bh))
    base = base.filter(ImageFilter.GaussianBlur(30)).point(lambda v: int(v * .40))
    f = min(bw * .94 / im.width, bh * .66 / im.height)
    fg = im.resize((int(im.width * f), int(im.height * f)), Image.LANCZOS)
    x, y = (bw - fg.width) // 2, int(bh * .47 - fg.height / 2)
    sombra = Image.new("L", base.size, 0)
    sombra.paste(200, (x + 16, y + 24, x + fg.width + 16, y + fg.height + 24))
    base.paste((0, 0, 0), (0, 0), sombra.filter(ImageFilter.GaussianBlur(26)))
    base.paste(fg, (x, y))
    arr = np.array(base)[..., ::-1].copy()

    def fn(dt, dur, marcas):
        u = min(1.0, max(0.0, dt / max(dur, .1)))
        u = u * u * (3 - 2 * u)
        s = (zoom[0] + (zoom[1] - zoom[0]) * u) / zm
        M = np.float32([[s, 0, W / 2 - s * bw / 2], [0, s, H / 2 - s * bh / 2]])
        fr = cv2.warpAffine(arr, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return np.dstack([fr, np.full((H, W), 255, np.uint8)])
    return fn


def pant(slug, de, a, cred):
    return [dict(tipo="pantalla", fn=_pantalla_v(os.path.join(_PAN, slug + ".jpg")), de=de, a=a, entra=.3, sale=.3,
                 nombre="pantalla " + slug, ver=2.0),
            credito(cred, de, a, lado="izq")]


def pv(en, slug, titulo, dur=4.0, x=.5, y=.5, tam=480, cred=None, **anim):
    import peg_anim as PA
    fn = PA.variado(os.path.join(_PEG, slug + ".png"), titulo, tam, tema=TEMA_PEG, **anim)
    out = [dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)]
    if cred:
        out.append(credito(cred, en, (en, dur), lado="izq"))
    return out


def ficha(titulo, items, de, a, marcas, color=K.AMAR, y=.58):
    return dict(tipo="mg", fn=K.ficha(titulo, items, color), de=de, a=a, marcas=marcas, x=.5, y=y, sale=.05,
                nombre="ficha " + titulo.lower())


def cifra(num, texto, de, a, color=K.AMAR, sub=None, y=.34, desde=0):
    return dict(tipo="mg", fn=K.cifra(num, texto, color, sub, desde), de=de, a=a, x=.5, y=y, sale=.05,
                nombre=f"cifra {num} {texto.lower()}")


CAMARA = {
    "scene-001": dict(a=(1.0, 0, 0), b=(1.10, 0, .1)),
    "scene-011": dict(a=(1.0, 0, 0), b=(1.12, 0, 0)),
    "scene-012": dict(a=(1.04, 0, 0), b=(1.16, 0, 0)),
    "scene-030": dict(a=(1.0, 0, 0), b=(1.10, 0, -.1)),
    # scene-048 y scene-050 (v2; antes 043/045): el dron trae subtítulos quemados abajo → medios/ recortados al 84 % por arriba con ffmpeg (12-nov)
}
FUNDIDO = {"scene-005": 0, "scene-011": 0, "scene-026": 0, "scene-050": 0}

FX = _creditos() + [
    dict(tipo="abre", en=0, dur=.6),
    # ---------------- gancho: desde el primer segundo, Juchipila y la carrera
    dict(tipo="mg", fn=G.cartel("BIENVENIDOS A", "JUCHIPILA", "ZACATECAS"), de="scene-001", a="scene-002:fin", x=.5, y=.29,
         sale=.05, nombre="cartel bienvenidos"),
    ficha("CAIN ROAD RACE MÉXICO 2026", [("Evento: 13 al 15 de noviembre", "·"), ("Carrera: domingo 15", "·")],
          de="Caín Road Race", a="scene-003:fin", marcas=[("Caín Road Race", .6), "ya vienes"], y=.60),
    dict(tipo="destello", en="entra a Juchipila"),
    # ---------------- dónde queda
    dict(tipo="pantalla", fn=G.mapa_paso(), de="scene-005", a="scene-008:fin", marcas=["diecisiete", "Apozol"], entra=.35,
         sale=.35, nombre="mapa te queda de paso"),
    # ---------------- gorditas FRITAS (Edson, 12-nov: solo las planas fritas con el lomo ENCIMA; las rellenas van aparte)
    dict(tipo="destello", en="lo importante"),
    dict(tipo="mg", fn=G.sello("IMPRESCINDIBLE"), de="sin probar", a="scene-011:fin", marcas=[.15], x=.5, y=.30, sale=.05,
         nombre="sello imprescindible"),
    *pant("yolis_02", "scene-013", "scene-013:fin", YOLIS),
    dict(tipo="mg", fn=G.pizarra("GORDITAS DE JUCHIPILA", ["De lomo", "De rajas", "De queso", "De chorizo",
                                                          "+ salsa verde", "+ queso fresco y cebolla"]),
         de="Y encima", a=("y su cebolla", 1.0), marcas=["lomo", "rajas", "queso o", "chorizo", "salsa verde", "queso fresco"],
         x=.5, y=.42, sale=.05, nombre="pizarra gorditas"),
    *pant("chenda_02", "scene-015", "scene-015:fin", CHENDA),
    *pv("Una no alcanza", "yolis_03", "NADIE PIDE UNA", dur=3.0, x=.5, y=.50, tam=900, cred=YOLIS),
    cifra(40, "AÑOS", "cuarenta", "scene-018:fin", sub="friendo gorditas en el callejón", y=.30),
    *pant("chenda_01", "scene-020", ("Y si te gustan", -.05), CHENDA),
    # ---------------- acompañar: la coca de vidrio = el combo perfecto
    *pant("chenda_03", "scene-024", "scene-024:fin", CHENDA),
    *pv("la coca bien helada", "coca", "COCA DE VIDRIO", dur=2.4, x=.5, y=.62, tam=560, cred="Video: Daniel RC"),
    dict(tipo="mg", fn=G.sello("EL COMBO PERFECTO"), de="combo perfecto", a="scene-025:fin", marcas=[.1], x=.5, y=.30, sale=.05,
         nombre="sello combo perfecto"),
    # ---------------- la broma
    dict(tipo="mg", fn=G.tacometro(), de="advertimos", a=("Las motos que", -.1), marcas=["pero vas a volver"], x=.5, y=.44,
         sale=.05, nombre="tacómetro carrera o gorditas"),
    dict(tipo="temblor", en=("pero vas a volver", .5), amp=28),
    # ---------------- más antojos
    *pv("churros", "churros", "CHURROS", dur=2.6, x=.30, y=.56, tam=580, cred="Video: Caxcán Online"),
    *pv("pan del pueblo", "pan", "PAN DEL PUEBLO", dur=2.3, x=.68, y=.40, tam=560),
    credito("Video: Emiliano JUCHIPILA", "pan del pueblo", ("pan del pueblo", 2.3), lado="izq"),
    # ---------------- caminar
    *pv("templo", "templo", "TEMPLO DE SAN FRANCISCO", dur=3.0, x=.5, y=.52, tam=760, cred="Video: Caxcán Online"),
    *pv("las letras", "letras", "LAS LETRAS", dur=3.6, x=.5, y=.42, tam=1000, marco="clasico"),
    # ---------------- consejos
    ficha("A LOS BIKERS", [("Deja la moto", "v"), ("Quítate el casco", "v"), ("Date la vuelta a pie", "v")],
          de="A los bikers", a="scene-040:fin", marcas=["deja la moto", "quítate el casco", "vuelta a pie"], y=.55),
    ficha("SI VAS A LA CARRERA", [("Llega antes de las 10", "·"), ("Almuerza temprano en Juchipila", "v"),
                                  ("¿Cierran la carretera? Aquí, comiendo", "v"), ("Trae efectivo", "·")],
          de="si vas a ver", a=("se paga así", .9), marcas=["antes de las diez", "almuerza temprano", "se cierra", "efectivo"],
          y=.55),
    # ---------------- se queda en Juchipila
    *pant("yolis_00", "scene-049", "scene-049:fin", YOLIS),
    # ---------------- cierre
    dict(tipo="mg", fn=G.cartel("ZACATECAS", "JUCHIPILA", "TE ESPERAMOS"), de="scene-050", a=("Compártelo", -.1), x=.5, y=.38,
         sale=.05, nombre="cartel te esperamos"),
    dict(tipo="cierra", en=("scene-052:fin", -.6), dur=.6),
]


def _ajusta(rotulos, maxw=960):
    """Rótulos en vertical: «A / B» = dos líneas; cada línea se achica hasta caber en `maxw` px (fuente Poppins Black)."""
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
    dict(texto="ENTRA A / JUCHIPILA", en="entra a Juchipila", a="Y ven", tam=130, color="amarillo", y=.30),
    dict(texto="VEN CON / MUCHA HAMBRE", en="mucha hambre", a="scene-004:fin", tam=120, color="rojo", y=.32),
    dict(texto="EL CORAZÓN / DEL CAÑÓN", en="corazón", a="scene-009:fin", tam=120, color="crema", y=.28),
    dict(texto="LO IMPORTANTE", en="lo importante", a="scene-010:fin", tam=140, color="amarillo", y=.40),
    dict(texto="GORDITAS / DE JUCHIPILA", en="las gorditas de", a="scene-011:fin", tam=120, color="amarillo", y=.60),
    dict(texto="FRITA EN ACEITE", en="se fríe", a="queda dorada", tam=120, color="amarillo", y=.30),
    dict(texto="DORADA Y / CRUJIENTE", en="queda dorada", a="Y encima", tam=130, color="amarillo", y=.20),
    dict(texto="SIÉNTATE", en="Siéntate", a=("Siéntate", 1.6), tam=150, color="amarillo", y=.30),
    dict(texto="¡QUE TRUENE!", en="que truene", a="scene-016:fin", tam=140, color="rojo", y=.24),
    dict(texto="CALLEJÓN DE / LOS JAMBADOS", en="Callejón", a=("cuarenta", -.1), tam=110, color="amarillo", y=.26),
    dict(texto="DESDE TEMPRANO", en="desde temprano", a="cuando se acaban", tam=110, color="crema", y=.15),
    dict(texto="¡Y SE ACABAN!", en="cuando se acaban", a=("Y si te gustan", -.05), tam=120, color="rojo", y=.15),
    dict(texto="¿TE GUSTAN / RELLENAS?", en="te gustan rellenas", a="de las que se abren", tam=120, color="crema", y=.26),
    dict(texto="TAMBIÉN LAS HAY", en="también las hay", a="de las que se abren", tam=110, color="amarillo", y=.43),
    dict(texto="OTRA OPCIÓN MÁS", en="Otra opción", a="scene-021:fin", tam=120, color="amarillo", y=.26),
    dict(texto="HORCHATA", en="horchata", a=("coca de vidrio", -.05), tam=120, color="crema", y=.22),
    dict(texto="CAFECITO", en="cafecito", a=("coca de vidrio", -.05), tam=120, color="crema", y=.30),
    dict(texto="LO QUE NO / PUEDE FALTAR", en="no puede faltar", a=("coca de vidrio", -.05), tam=110, color="amarillo", y=.42),
    dict(texto="COCA DE VIDRIO / BIEN FRÍA", en="coca de vidrio", a="scene-023:fin", tam=120, color="rojo", y=.20),
    dict(texto="LOMO, QUESO, / CEBOLLA Y CHILE", en="Gordita frita de lomo", a="la coca bien helada", tam=110, color="amarillo", y=.14),
    dict(texto="+ LA COCA / BIEN HELADA", en="la coca bien helada", a="scene-024:fin", tam=120, color="rojo", y=.14),
    dict(texto="LAS MOTOS QUE / NOS PERDONEN", en="Las motos que", a="scene-027:fin", tam=110, color="crema", y=.36),
    dict(texto="¿A QUÉ HORA / SALE LA CARRERA?", en="a qué hora sale", a=("a qué hora sale", 2.4), tam=100, color="crema", y=.30),
    dict(texto="¿A QUÉ HORA / ABREN?", en="a qué hora abren", a="scene-029:fin", tam=120, color="amarillo", y=.30),
    dict(texto="BIRRIA TATEMADA", en="birria tatemada", a="de chivo", tam=120, color="amarillo", y=.24),
    dict(texto="DE CHIVO / Y DE BORREGO", en="de chivo", a="Para el antojo", tam=100, color="amarillo", y=.26),
    dict(texto="CHICHARRONES", en="chicharrones", a="scene-031:fin", tam=110, color="amarillo", y=.20),
    dict(texto="LLÉVATE FRUTA", en="llévate fruta", a="scene-032:fin", tam=120, color="crema", y=.15),
    dict(texto="GUAYABA / DEL CAÑÓN", en="guayaba", a="scene-033:fin", tam=130, color="amarillo", y=.28),
    dict(texto="PREGÚNTALE / A LA GENTE", en="Pregúntale", a=("lugar favorito", -.05), tam=110, color="crema", y=.26),
    dict(texto="TODOS TIENEN / SU FAVORITO", en="lugar favorito", a="Ya comiste", tam=110, color="amarillo", y=.26),
    dict(texto="YA COMISTE.", en="Ya comiste", a="Ahora camina", tam=130, color="crema", y=.40),
    dict(texto="AHORA, CAMINA", en="Ahora camina", a="scene-035:fin", tam=130, color="amarillo", y=.30),
    dict(texto="EL JARDÍN", en="jardín", a="templo", tam=130, color="crema", y=.24),
    dict(texto="SUS CALLEJONES", en="callejones", a="Date una vuelta", tam=110, color="amarillo", y=.24),
    dict(texto="EL MERCADO", en="mercado", a="scene-037:fin", tam=130, color="crema", y=.24),
    dict(texto="¡TÓMATE LA FOTO!", en="dónde estuviste", a="A los bikers", tam=110, color="amarillo", y=.66),
    dict(texto="SIN CURVAS…", en="no hay curvas", a="pero hay sabor", tam=130, color="crema", y=.30),
    dict(texto="…PERO CON SABOR", en="pero hay sabor", a="si vas a ver", tam=120, color="amarillo", y=.30),
    dict(texto="CADA GORDITA", en="Cada gordita", a=("se queda en", -.05), tam=110, color="crema", y=.22),
    dict(texto="CADA PLATO DE BIRRIA", en="cada plato", a=("se queda en", -.05), tam=110, color="crema", y=.30),
    dict(texto="CADA BOLSA DE GUAYABA", en="cada bolsa", a=("se queda en", -.05), tam=110, color="crema", y=.38),
    dict(texto="SE QUEDA EN / JUCHIPILA", en="se queda en", a="scene-046:fin", tam=130, color="amarillo", y=.30),
    dict(texto="MAYO 2027", en="mayo del", a="scene-047:fin", tam=170, color="amarillo", y=.32),
    dict(texto="LA CARRERA / QUIERE VOLVER", en="mayo del", a="scene-047:fin", tam=90, color="crema", y=.42),
    dict(texto="QUEREMOS / QUE VUELVAS", en="queremos que", a="Aunque ya", tam=130, color="amarillo", y=.32),
    dict(texto="VAS A VOLVER / POR LAS GORDITAS", en="Aunque ya", a="scene-049:fin", tam=110, color="amarillo", y=.13),
    dict(texto="COMPÁRTELO CON / TU GRUPO DE RODADA", en="Compártelo", a="dinos en los", tam=100, color="amarillo", y=.30),
    dict(texto="DINOS EN LOS / COMENTARIOS", en="dinos en los", a=("de rajas", -.6), tam=110, color="crema", y=.30),
    dict(texto="¿LOMO, RAJAS / O CHORIZO?", en=("de rajas", -.6), a="scene-052:fin", tam=130, color="amarillo", y=.32),
])

SFX = {
    "moto_pasa": ("A sport motorcycle passing by fast on a mountain road, loud engine roar doppler, realistic", 3),
    "fritura": ("Corn dough frying in a pot of hot oil, strong crackling sizzle, close up, realistic kitchen", 4),
    "cruje": ("Biting into a crispy fried tortilla, loud satisfying crunch, close up", 1.5),
    "motor_acelera": ("Motorcycle engine revving up hard to the red line, two revs, realistic", 3),
    "campana": ("Small Mexican town church bell ringing twice in the distance, outdoor", 3),
    # genéricos NUEVOS (no los mismos del reel de la carrera, que vio el mismo público)
    "whoosh": ("Quick airy swoosh transition, soft and clean, short", 1),
    "pop": ("Light wooden spoon tap on a clay pot, short bright pop", 1),
    "golpe": ("Deep warm drum hit with a short wooden knock, punchy impact", 1.5),
    "sello": ("Heavy rubber stamp slammed on a wooden table, single thump", 1),
    "datos": ("Old mechanical counter flipping numbers quickly, short ratchet clicks", 1.5),
}
PISTAS = [
    dict(sfx="moto_pasa", en="scene-001", vol=.5),
    dict(sfx="whoosh", en="Caín Road Race", vol=.45),
    dict(sfx="golpe", en="entra a Juchipila", vol=.55),
    dict(sfx="pop", en="mucha hambre", vol=.45),
    dict(sfx="whoosh", en="scene-005", vol=.45),
    dict(sfx="pop", en="diecisiete", vol=.4),
    dict(sfx="pop", en="Apozol", vol=.4),
    dict(sfx="golpe", en="lo importante", vol=.55),
    dict(sfx="sello", en=("sin probar", .15), vol=.55),
    dict(sfx="fritura", en="se fríe", vol=.45),
    dict(sfx="pop", en="lomo", vol=.35),
    dict(sfx="pop", en="rajas", vol=.35),
    dict(sfx="pop", en="queso o", vol=.35),
    dict(sfx="pop", en="chorizo", vol=.35),
    dict(sfx="whoosh", en="te gustan rellenas", vol=.4),
    dict(sfx="pop", en="coca de vidrio", vol=.45),
    dict(sfx="sello", en=("combo perfecto", .1), vol=.55),
    dict(sfx="cruje", en="que truene", vol=.6),
    dict(sfx="pop", en="Una no alcanza", vol=.4),
    dict(sfx="datos", en="cuarenta", vol=.4),
    dict(sfx="motor_acelera", en="advertimos", vol=.4),
    dict(sfx="golpe", en=("pero vas a volver", .5), vol=.6),
    dict(sfx="pop", en="a qué hora abren", vol=.45),
    dict(sfx="whoosh", en="birria tatemada", vol=.4),
    dict(sfx="pop", en="churros", vol=.4),
    dict(sfx="pop", en="pan del pueblo", vol=.4),
    dict(sfx="campana", en="templo", vol=.3),
    dict(sfx="pop", en="las letras", vol=.4),
    dict(sfx="pop", en="deja la moto", vol=.35),
    dict(sfx="pop", en="antes de las diez", vol=.35),
    dict(sfx="pop", en="efectivo", vol=.35),
    dict(sfx="datos", en="mayo del", vol=.4),
    dict(sfx="moto_pasa", en="scene-050", vol=.3),
    dict(sfx="whoosh", en=("de rajas", -.6), vol=.4),
]
