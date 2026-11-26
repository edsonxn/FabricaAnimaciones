# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (SECUENCIA YT, Crónicas de Warcraft, 25-nov-2026).
Modelos: videos/wow_errores_60/efectos.py (helpers y bloque Overgear) y videos/wow_ruta_forever/efectos.py (formato ruta).
- KIT DE 4 ESTILOS (regla del usuario 22-nov; PRIMER video que lo usa): TODOS los mapas, y parte de las fichas, tarjetas, rótulos y
  pegatinas, con nucleo/mg_wow_estilos.py (E.mapa_e / E.ficha_e / E.tarjeta_e / E.rotulo_e / E.peg_e) en rotación
  original → pergamino → oro → holograma; mezclados con los helpers originales (pv, rel, cam, aba, pant, APOYOS de interfaz).
- Cada parada: tarjeta de capítulo P.habilidad (barra 1-300 con los 4 rangos y sus tramos) + mapas reales con ruta de `_coords.md`
  (Wowhead Forever; paso k en la marca de la frase que lo nombra) + pegatinas (pegatinas/_creditos.json) + fichas + objetos de campamento.
- MG NUEVOS de este guion (nucleo/mg_prof.py): habilidad (12 tarjetas de parada), rangos (coste 10 c / 5 p / 50 p / 5 o y nivel
  10/20/35), barras (500 → 1200 barras de torio), telar (la trampa 300 ⇄ 300 y sus dos salidas), campamento (hoguera 3/5/10),
  legado (6 × 3 = 18 puntos), flujo (hierba → alquimia → tintes → sastrería/peletería; minería → herrería/ingeniería), traspaso
  (las pociones de sanación se mudan de la alquimia a primeros auxilios), bolsas (6/8/12/14 casillas).
- Comentarios (≤ 10 días, ninguno repetido): julsi Julsikakku · gracias1 Jesús, Óscar, Barón Rata, Steven · burla0 Goca ·
  burla1 Crisis · burla2 SoyoyoS (tarjetas en pegatinas/_comentarios.txt).
- Overgear (escena overgear, 140-215 s): fondo de marca DEBAJO de reseñas, packshot y código; logo blanco; capturas FRESCAS de la página
  de coaching (25-nov: pantallas/og_coaching_hero.jpg «Voice or text», og_coaching_precio.jpg «Save 5 %» + «Cashback from 1 %»).
  python fab.py wow_ruta_profesiones fx --seco | FAB_FX_FINAL=1 python fab.py wow_ruta_profesiones fx hoja | fx
"""
import os

import mg_oro as O
import mg_prof as P
import mg_tes as T
import mg_wow as M
import mg_wow_estilos as E
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
_PEG60 = os.path.join(_D, "..", "wow_errores_60", "pegatinas")     # Guarida de Onyxia (la nombra el patrocinio)
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", -0.4)   # el código del creativo sale ~3 s después de entrar: así coincide con la voz
FIN_OG = ("Parada uno. Minería", -.4)
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
AZUL = (70, 140, 255)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    if slug.startswith("o_"):
        tam = min(tam, 340)
        if "marco" not in anim:   # el marco «vitral» parte el ícono en vidrieras y no se reconoce (hoja fx 22-nov): otro marco
            anim["marco"] = ("polaroid", "carta", "estampilla", "naipe", "museo", "clasico")[sum(map(ord, slug)) % 6]
    ruta = slug if os.path.exists(slug) else F(slug)
    return dict(tipo="mg", fn=PA.variado(ruta, titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + os.path.basename(slug), ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6, xs=(.14, .32, .50, .68, .86)):
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    if slug.startswith("o_"):
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    if slug.startswith("o_"):
        foco = (.5, .5, 1.0)
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def Fc(slug):
    """Retrato de PNJ recortado a cara y hombros (caras/<slug>.png, hecho de la pegatina): los marcos de oro y holograma
    cortaban la cabeza de los modelos de cuerpo entero (regla 9 del 11-nov: toda tarjeta con personaje enseña su CARA)."""
    c = os.path.join(_D, "caras", slug + ".png")
    return c if os.path.exists(c) else slug


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, estilo=None, zmax=1.5):
    """Mapa del KIT DE 4 ESTILOS (rota solo). puntos = [(x, y, rótulo, sub, slug_foto|None)] de `_coords.md`."""
    return E.mapa_e(nom, [E.P(x, y, r, sb, Fc(f) if f else None) for x, y, r, sb, f in puntos], de, a, marcas, titulo, sub,
                    estilo=estilo, zmax=zmax)


def tarj(en, slug, *a, **k):
    """E.tarjeta_e con el retrato recortado a la cara."""
    return E.tarjeta_e(en, Fc(slug), *a, **k)


def mg(fn, de, a, marcas, nombre, y=.56, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def par(n, nombre, slug, tramos, en, a, nota=None, nota_en=None):
    """Tarjeta de capítulo de la parada n (barra de habilidad 1-300 con sus tramos) al decir «Parada…»."""
    marcas = [(en, .2)] + [(en, .8 + .45 * k) for k in range(len(tramos))] + ([nota_en] if nota_en else [])
    return mg(P.habilidad(n, nombre, F(slug), tramos, nota), (en, -.2), a, marcas, f"parada {n}", y=.42)


def fav(ico, prof, n, en, a=None, remate=None):
    """Contador de recetas de Favor de comerciante de esa profesión (vuelve en cada parada de fabricación)."""
    a = a or (en, 3.0)
    return mg(M.contadores("RECETAS DE FAVOR DE COMERCIANTE", [(ico, prof, n, 0, 1)], (remate, 2) if remate else None),
              (en, -.2), a, [(en, .1), (en, 1.6), (en, 2.4)], f"favor {prof}", y=.50)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def muro(fotos, de, a, marcas, titulo=None, cols=6, alto=560):
    import presenta as PR
    return _pres(PR.muro([(F(s), n) for s, n in fotos], cols=cols, tema=TEMA_PEG, alto=alto, titulo=titulo), de, a, marcas, "muro") | dict(y=.53)


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel([(F(s), n) for s, n in fotos], tam=400, tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel") | dict(y=.54)


def tar(en, titulo, icono, lineas, calidad="amarillo", dur=5.0, x=.70, size=.50):
    """Ficha de interfaz (tooltip del juego) a la derecha. icono = nombre de Wowhead o slug de pegatina."""
    if os.path.exists(F(icono)):
        icono = _ICONO.get(icono, icono)
    return dict(en=en, dur=dur, x=x, size=size, tarjeta=dict(titulo=titulo, calidad=calidad, icono=icono, lineas=lineas))


import json as _json
_ICONO = {k: v["icono"] for k, v in _json.load(open(os.path.join(_PEG, "_creditos.json"), encoding="utf-8")).items() if v.get("icono")}

PROFS12 = [("o_prof_mineria", "Minería"), ("o_prof_herreria", "Herrería"), ("o_prof_ingenieria", "Ingeniería"),
           ("o_prof_herboristeria", "Herboristería"), ("o_prof_alquimia", "Alquimia"), ("o_prof_desuello", "Desuello"),
           ("o_prof_peleteria", "Peletería"), ("o_prof_sastreria", "Sastrería"), ("o_prof_encantamiento", "Encantamiento"),
           ("o_prof_cocina", "Cocina"), ("o_prof_pesca", "Pesca"), ("o_prof_primeros_auxilios", "Primeros auxilios")]
PREG = "inv_misc_questionmark"

CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== OVERGEAR: fondo de marca PRIMERO (debajo de reseñas, packshot y código)
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="Si reservas dos horas", a=FIN_OG,
         entra=.3, nombre="og fondo marca"),
    # =========================================================== GANCHO (0-68 s): un elemento cada 2-3 s, MG desde el segundo 0
    mg(P.traspaso("LAS POCIONES DE SANACIÓN", F("o_pocion_sanacion"), (F("o_prof_alquimia"), "ALQUIMIA"),
                  (PREG, "¿QUIÉN LAS HACE AHORA?"), "la profesión que casi todos dejan para el final"),
       .1, ("dejan para el final. Hay una|fin", -1.2),
       [("el alquimista ya no hace", .1), "Ahora las puede hacer cualquiera", "con la profesión que casi"], "traspaso gancho", y=.50),
    E.peg_e(("Hay una mena nueva en Monte", .1), "o_mena_torio_pesada", "Mena de torio pesada", dur=3.9, x=.17, y=.62),
    pv(("en Monte Hyjal que no se puede", -.3), "monte_hyjal", "Monte Hyjal", dur=3.7, x=.76, y=.46, tam=540),
    mg(P.telar("UNA PROFESIÓN CON TRAMPA", F("o_telar"), ("PARA LLEGAR AL 300", "TE PIDE UN TELAR"), ("EL TELAR", "SOLO SE FABRICA CON 300")),
       ("Y una profesión que, para llegar", -.2), ("solo se fabrica con trescientos|fin", .1),
       [("Y una profesión que, para llegar", .2), "que solo se fabrica con trescientos"], "telar gancho", y=.50),
    mg(M.contadores("LA PRIMERA SEMANA DE FOREVER", [("inv_misc_note_01", "millones de objetos de campamento", 28, 0, 1)],
                    ("SIN CAMPAMENTO, TE FALTAN ESTACIONES", 2)),
       ("trescientos En la primera semana", .3), ("Y sin campamento, te faltan", -.2),
       [("trescientos En la primera semana", 2.0), ("de objetos de campamento. Y sin", 0), ("Y sin campamento, te faltan", -.4)],
       "28 millones gancho", y=.52),
    pant("campamento", ("Y sin campamento, te faltan", -.2), ("media lista de recetas|fin", .4), zoom=(1.0, 1.12)),
    mg(M.tiempos("DOS RUTAS", [("NIVEL 1 A 60", 10, AZUL), ("PROFESIONES 1 A 300", 12, AMAR)], "las dos, al mismo tiempo"),
       ("Hace unos días hicimos la ruta", -.2), ("la de las profesiones|fin", .5),
       [("hicimos la ruta del uno al sesenta", .3), "Hoy toca la otra ruta", "la que vas subiendo al mismo tiempo"], "dos rutas", y=.50),
    muro(PROFS12, ("Son doce profesiones, y cada", -.2), ("en cuatro tramos|fin", .6),
         [("Son doce profesiones, y cada", .2 + .3 * k) for k in range(12)], "12 PROFESIONES · DEL 1 AL 300"),
    mapa("mundo", [(22.0, 43.5, "Hgarth", "Horda · dónde entrenar", "hgarth"), (73.5, 76.8, "Kitta Vientofuego", "Alianza · dónde entrenar", "kitta")],
         ("Para la Alianza y para la", -.2), ("dónde entrenar y dónde recoger|fin", .4),
         [("Para la Alianza y para la", .2), "con el mapa de dónde entrenar"], "AZEROTH", "dónde entrenar y dónde recoger", zmax=1.2),
] + filav("recetas nuevas, materiales nuevos, y", [("o_diseno_peto_bendecidas", "Recetas nuevas", None),
                                                 ("o_pecblenda", "Materiales nuevos", "materiales nuevos, y lo que")], y=.62, tam=320, dur=4.2, xs=(.14, .36)) + [
    E.ficha_e("PRIMERO, LA RECOLECCIÓN", ["o_prof_mineria", "o_prof_herboristeria", "o_prof_desuello"],
              ("Empezamos por lo que alimenta", -.2), ("Te adelanto que no es", -.1),
              [("Empezamos por lo que alimenta", .3), "a todas las demás", "la recolección, y terminamos"],
              etiquetas=["minería", "hierbas", "desuello"]),
    # =========================================================== REGLAS (70-139 s)
    mg(P.flujo("12 PROFESIONES · 9 + 3", [(c, 0, F(s), n) for c, (s, n) in enumerate(PROFS12[:5])]
               + [(c, 1, F(s), n) for c, (s, n) in enumerate(PROFS12[5:9])]
               + [(c, 2, F(s), n) for c, (s, n) in enumerate(PROFS12[9:])], [], ("SON EXACTAMENTE 12", 12), cols=5, filas=3),
       ("Primero, las reglas del juego", -.2), ("son exactamente doce|fin", .3),
       [("Hay nueve profesiones principales", .2 + .2 * k) for k in range(9)] + [("y tres secundarias", .1 + .2 * k) for k in range(3)]
       + ["son exactamente doce"], "9 + 3", y=.52),
    E.ficha_e("POR PERSONAJE: 2 + 3", ["o_prof_mineria", "o_prof_herreria", "o_prof_cocina", "o_prof_pesca", "o_prof_primeros_auxilios"],
              ("Puedes llevar dos principales", -.2), ("y esas no se pueden olvidar|fin", .3),
              [("Puedes llevar dos principales", .3), ("Puedes llevar dos principales", .8), ("Las tres secundarias, cocina", .6),
               ("pesca y primeros auxilios, van", 0), ("primeros auxilios, van aparte", 0)],
              etiquetas=["principal", "principal", "cocina", "pesca", "1.os auxilios"], estilo="original"),
    mg(P.rangos("ENTRENAR CADA RANGO", [(10, "cobre"), (5, "plata"), (50, "plata"), (5, "oro")], "unas 5 de oro y media por profesión",
                [None, 10, 20, 35]),
       ("Entrenar cuesta diez de cobre", -.2), ("el de artesano nivel treinta y cinco|fin", .8),
       ["Entrenar cuesta diez de cobre", "cinco de plata el segundo", "cincuenta de plata el tercero", "y cinco de oro el de artesano",
        "Unas cinco de oro y media", "El rango de oficial pide nivel", "el de experto nivel veinte", "el de artesano nivel treinta"],
       "rangos y coste", y=.52),
    E.rotulo_e(("Y el artesano no te lo enseña", 0), "El artesano: muchas veces, de viaje", sello="!", dur=5.0),
    pv(("muchas veces hay que viajar", -.4), "gadgetzan", "Gadgetzan · el artesano de ingeniería", dur=3.6, x=.76, y=.46, tam=520),
    mapa("durotar", [(40.5, 68.1, "Norzsh", "entrenador júnior de minería", "norzsh")],
         ("Novedad de Forever: cada zona", -.2), ("y desuello, que te enseñan", 0),
         [("tiene entrenadores júnior de minería", .2)], "DUROTAR", "entrenadores júnior · hasta el 75"),
    mapa("elwynn", [(47.2, 32.2, "Kelsey Fargo", "entrenadora júnior de minería", "kelsey_fargo")],
         ("y desuello, que te enseñan", 0), ("sin pisar la capital|fin", .5),
         [("y desuello, que te enseñan", .4)], "BOSQUE DE ELWYNN", "hasta el 75 sin pisar la capital"),
    E.ficha_e("LA MOCHILA · 5 RANURAS", ["inv_misc_bag_07", "inv_misc_bag_08", "inv_misc_bag_09", "inv_misc_bag_10", "o_bolsa_componentes_lino"],
              ("Y la mochila tiene una quinta", -.2), ("solo para la bolsa de componentes|fin", .6),
              [("Y la mochila tiene una quinta", .2), ("Y la mochila tiene una quinta", .5), ("Y la mochila tiene una quinta", .8),
               ("Y la mochila tiene una quinta", 1.1), "solo para la bolsa de componentes"],
              etiquetas=[None, None, None, None, "componentes"], estilo="original"),
    pv(("Y ninguna profesión da un", -.2), "o_hoguera_basica", "Hoguera de campamento", dur=4.0, x=.17, y=.62),
    pant("campamento_2", ("y en algo nuevo que vas", -.2), ("vas a ver en cada parada: el campamento|fin", .6), zoom=(1.0, 1.10)),
    # =========================================================== OVERGEAR (140-215 s) — logo, coaching, captura, pros, reseñas, captura precio, packshot, código
    aba([("o_prof_herreria", "Herrería"), ("o_prof_alquimia", "Alquimia"), ("o_prof_encantamiento", "Encantamiento")],
        ("algo que ninguna profesión te", -.3), ("cómo sacarle más a tu|fin", .6),
        [("algo que ninguna profesión te", .1), ("algo que ninguna profesión te", .5), ("algo que ninguna profesión te", .9)],
        "ninguna profesión", x=.30, y=.62),
    dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, "og_coaching_hero.jpg"), (1.0, 1.07), (0, 0, -.02, .05)),
         de=("Son sesiones individuales por horas", -.2), a="Un coach mira tus talentos", entra=.4, sale=.3, nombre="og captura coaching", ver=2.0),
    dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, "og_coaching_precio.jpg"), (1.0, 1.06)), de=("ahorras un cinco por ciento", -.3),
         a="Y lo que aprendes se queda", entra=.4, sale=.3, nombre="og captura precio", ver=2.0),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción, y hay", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en=("Este video lo patrocina Overgear", .3),
         dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="Un coach mira tus talentos", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-2_green-screen_wow-forever.mp4", croma=True, en="Y si todavía vas camino del", dur=3.6, sale=.25,
         nombre="og leveling"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="Y lo que aprendes se queda", dur=4.0,
         sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción, y hay",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=FIN_OG, entra=.15, nombre="og CODIGO", ver=3.0),
    pv(("resistencia al fuego para la", -.3), os.path.join(_PEG60, "guarida_onyxia.png"), "Guarida de Onyxia", dur=4.4, x=.76, y=.42, tam=480),
    pv(("consumibles, y qué equipo previo", -.2), os.path.join(_PEG60, "o_pocion_fuego.png"), "Consumibles", dur=3.6, x=.17, y=.62),
] + filav("Muchos de esos consumibles, por", [("o_prof_alquimia", "Alquimia", None), ("o_prof_cocina", "Cocina", ("Muchos de esos consumibles, por", .5)),
                                            ("o_prof_primeros_auxilios", "Primeros auxilios", ("Muchos de esos consumibles, por", 1.0))],
          y=.62, tam=300, dur=4.4, xs=(.14, .37, .60)) + [
    # =========================================================== P01 · MINERÍA (215-348 s)
    par(1, "MINERÍA", "o_prof_mineria", [(1, 65, "cobre"), (65, 125, "estaño y plata"), (125, 175, "hierro y oro"),
                                         (175, 245, "mitril y veraplata"), (245, 300, "torio")],
        "Parada uno. Minería", ("Del uno al sesenta y cinco, cobre", -.2), "alimenta a la herrería y a la ingeniería", "que alimenta a la herrería"),
    mapa("durotar", [(53.1, 25.5, "Cobre", "1-65", "o_mena_cobre"), (43.8, 64.7, "Vetas de cobre pobres", "Valle de los Retos", "o_mena_cobre")],
         ("Del uno al sesenta y cinco, cobre", -.2), ("y un entrenador júnior en cada uno|fin", .4),
         [("cobre, en cualquier zona inicial", .1), "hay vetas de cobre pobres"], "DUROTAR", "minería · del 1 al 65"),
    mapa("teldrassil", [(56.9, 27.6, "Fragmentos de ámbar", "dan mena de cobre", None), (53.0, 51.1, "Fragmentos de ámbar grandes", "solo hasta 20", None)],
         ("Los elfos de la noche, que", -.2), ("suben la habilidad hasta veinte|fin", .4),
         [("ahora pican fragmentos de ámbar", .1), ("Dan mena de cobre, aunque", .3)], "TELDRASSIL", "elfos de la noche · sin cobre"),
    mapa("mulgore", [(56.7, 53.4, "Cueva de cobre", "5 vetas · reaparecen rápido", "o_mena_cobre"),
                     (34.6, 53.2, "Excavación de Bael'dun", "la forja más cerca", None)],
         ("En Mulgore hay una cueva", -.2), ("está en la Excavación de Bael'dun|fin", .4),
         [("En Mulgore hay una cueva", .3), "La forja más cerca está"], "MULGORE", "una cueva con cinco vetas"),
    mapa("humedales", [(47.3, 62.2, "Cueva de estaño", "Alianza · 65-125", "o_mena_estano")],
         ("Del sesenta y cinco al ciento veinticinco", -.2), ("y la Horda, en el Bosque", -.2),
         [("La Alianza, en una cueva", .2)], "LOS HUMEDALES", "Alianza · estaño y plata"),
    pv(("estaño y plata. La Alianza", -.3), "o_mena_plata", "Mena de plata", dur=3.4, x=.17, y=.70),
    mapa("argenteos", [(58.1, 72.8, "Cueva de estaño", "Horda · 65-125", "o_mena_estano")],
         ("y la Horda, en el Bosque", -.2), ("Del ciento veinticinco al ciento setenta", -.2),
         [("y la Horda, en el Bosque", .2)], "BOSQUE DE ARGÉNTEOS", "Horda · o en Laderas de Trabalomas"),
    mapa("arathi", [(54.4, 76.0, "Hierro", "125-175", "o_mena_hierro"), (84.5, 32.8, "Oro", "155-175", "o_mena_oro")],
         ("Del ciento veinticinco al ciento setenta", -.5), ("o en Las Mil Agujas", .8),
         [("hierro y oro, en las Tierras", .1), ("hierro y oro, en las Tierras", 1.2)], "TIERRAS ALTAS DE ARATHI", "hierro y oro · 125-175"),
    mapa("mil_agujas", [(12.7, 34.8, "Hierro", "125-175", "o_mena_hierro"), (43.3, 35.5, "Hierro", None, "o_mena_hierro")],
         ("o en Las Mil Agujas", .8), ("tiene más vetas de hierro que", 0), [("o en Las Mil Agujas", .9), ("o en Las Mil Agujas", 1.6)],
         "LAS MIL AGUJAS", "hierro · 125-175"),
    mapa("riverglades", [(55.5, 44.7, "Hierro: unas 130 vetas", "la zona con más hierro", "o_mena_hierro")],
         ("tiene más vetas de hierro que", 0), ("unas ciento treinta|fin", .5),
         [("tiene más vetas de hierro que", .2)], "CLAROS DEL RÍO", "zona nueva de Forever"),
    mapa("interior", [(56.7, 43.9, "Mitril y veraplata", "175-245", "o_mena_mitril")],
         ("Del ciento setenta y cinco al doscientos cuarenta y cinco, mitril", -.2), "o en Tanaris. Aprende",
         [("mitril y veraplata, en Tierras", .1)], "TIERRAS DEL INTERIOR", "mitril y veraplata · 175-245"),
    pv(("mitril y veraplata, en Tierras", .4), "o_mena_veraplata", "Mena de veraplata", dur=3.6, x=.17, y=.70),
    mapa("tanaris", [(33.5, 44.6, "Mitril y veraplata", "175-245", "o_mena_mitril"), (55.1, 74.6, "Mitril y veraplata", None, "o_mena_mitril")],
         "o en Tanaris. Aprende", ("Y para cerrar, torio pequeño", -.3), [("o en Tanaris. Aprende", .1), ("o en Tanaris. Aprende", 1.1)],
         "TANARIS", "mitril y veraplata · 175-245"),
    E.rotulo_e(("Aprende el rango de artesano antes de salir", 0), "Aprende el artesano antes de salir", sello="!", dur=3.6),
] + filav("Y para cerrar, torio pequeño", [("o_mena_torio", "Torio pequeño", None), ("o_mena_torio", "Torio rico", ("y torio rico en Cuna", 0))],
          y=.64, tam=300, dur=5.0, xs=(.14, .34)) + [
    tar(("Y para cerrar, torio pequeño", .4), "Torio: del 245 al 300", "o_mena_torio",
        ["Torio pequeño: Un'Goro o Frondavil", dict(t="Torio rico: Cuna del Invierno", c=V), dict(t="Peste del Este · Estepas Ardientes", c=V)],
        dur=7.4),
    E.ficha_e("MENA DE LA SUBASTA: HASTA EL 105", ["o_mena_cobre", "o_mena_estano"], ("Si vas con prisa, existe", -.2),
              ("te llevan hasta el ciento cinco|fin", .6), [("unas ciento cuarenta de cobre", .2), ("y setenta de estaño", .1)],
              cuentas=[140, 70], total=105, etiquetas=["×140", "×70"]),
    E.rotulo_e(("la mena se apila de veinte", -.2), "La mena se apila de 20 en 20", sello="20", dur=3.6),
] + filav("pirita, bauxita y pecblenda", [("o_pirita", "Pirita", None), ("o_bauxita", "Bauxita", ("bauxita y pecblenda. Con", 0)),
                                          ("o_pecblenda", "Pecblenda", ("y pecblenda. Con la", 0))], y=.62, tam=300, dur=4.4) + [
    tarj(("Con la pecblenda se funde", .2), "o_barra_azerotio", "Barra de azerotio", "se funde con la pecblenda", dur=3.0, x=.74, tam=420),
    mapa("hyjal", [(35.6, 83.3, "Torio pesado", "la mena nueva", "o_mena_torio_pesada"), (35.8, 47.6, "Torio pesado", None, None),
                   (64.5, 86.0, "Torio pesado", "unas 120 vetas", None)],
         ("Y en Monte Hyjal está la", -.2), ("Pero esa no se funde", -.1),
         [("Y en Monte Hyjal está la", .4), "la mena de torio pesada, en", "en unas ciento veinte vetas"], "MONTE HYJAL", "la única mena nueva"),
    E.rotulo_e(("Pero esa no se funde", 0), "No se funde en ninguna forja de Azeroth", sello="!", dur=3.4),
    tarj(("necesitas una fundición de magma", -.2), "o_fundicion_magma", "Fundición de magma", "objeto de campamento", dur=3.4, x=.74, tam=420),
    mapa("estepas", [(27.9, 40.2, "Embajador Latifuego", "Profundidades de Roca Negra", "embajador_latifuego")],
         ("cuyo plano suelta el Embajador", -.2), ("el Embajador Latifuego, en Profundidades de Roca Negra|fin", .6),
         [("cuyo plano suelta el Embajador", .4)], "LAS ESTEPAS ARDIENTES", "el plano de la fundición"),
    E.ficha_e("CAMPAMENTO DEL MINERO", ["o_fundicion_magma", "o_magnetita", "o_jardin_rocoso"], ("Los otros dos objetos de campamento del", -.2),
              ("que hace crecer una veta|fin", .6), [("Los otros dos objetos de campamento del", .3), "son la magnetita, que da",
                                                    "y el jardín rocoso, que"], etiquetas=["magma", "ataque", "veta"]),
    mapa("hyjal", [(63.6, 86.7, "Torio rico", "más de 100 vetas", "o_mena_torio"), (76.3, 75.4, "Torio rico", "los últimos puntos", None)],
         ("Y un dato para el final", -.2), ("es el sitio|fin", .6),
         [("Monte Hyjal tiene, además, más", .3), "Para los últimos puntos"], "MONTE HYJAL", "torio rico · del 275 al 300"),
    # =========================================================== P02 · HERRERÍA (350-486 s)
    par(2, "HERRERÍA", "o_prof_herreria", [(1, 75, "piedras de afilar"), (75, 140, "bronce"), (140, 210, "hierro verde y mitril"),
                                           (270, 300, "torio")],
        "Parada dos. Herrería", ("Del uno al setenta y cinco, piedras", -.2), "se come casi todo lo que pica el minero", "la que se come casi"),
    pv(("piedras de afilar y piedras de", -.2), "o_piedra_pulir_burda", "Piedra de pulir burda", dur=4.0, x=.17, y=.62),
    tar("Y un ajuste del diez de noviembre", "Piedra de pulir burda", "o_piedra_pulir_burda",
        ["Ajuste del 10 de noviembre", dict(t="Ahora da puntos hasta el 90", c=V)], calidad="blanco", dur=5.2),
    tarj(("Calcula unas trescientas barras de", -.2), "o_barra_bronce", "Barra de bronce", "unas 300 hasta el 150", dur=4.6, x=.74, tam=420),
    pv(("bronce: varas de plata, leotardos", -.2), "o_prof_herreria", "Bronce · del 75 al 140", dur=3.6, x=.17, y=.62),
    mapa("orgrimmar", [(82.3, 23.0, "Saru Steelfury", "herrería · experto (H)", "saru_steelfury")],
         ("Para el rango de experto vas", -.2), ("y en Forjaz, un enano", -.1),
         [("en Orgrimmar lo enseña Saru", .2)], "ORGRIMMAR", "el experto de la Horda"),
    mapa("forjaz", [(52.4, 41.2, "Bengus Deepforge", "junto a la gran fragua (A)", "bengus_deepforge")],
         ("y en Forjaz, un enano", -.1), ("Y la Alianza tiene una opción", -.2),
         [("y en Forjaz, un enano", .4)], "FORJAZ", "el experto de la Alianza"),
    mapa("alterac", [(16.7, 68.8, "Ciudad de Dalaran", None, None), (19.7, 63.4, "Alard Schmied", "herrería hasta el 225 (A)", None)],
         ("Y la Alianza tiene una opción", -.2), ("En Darnassus, en cambio, no", -.1),
         [("Y la Alianza tiene una opción", .5), ("Alard Schmied, en Dalaran, enseña", .2)], "MONTAÑAS DE ALTERAC", "Dalaran · opción nueva"),
    E.rotulo_e(("En Darnassus, en cambio, no", 0), "Darnassus: sin herrero · los elfos, a Auberdine", sello="!", dur=4.2),
    pv(("cuarenta brazales de hierro verde", -.2), "o_brazales_hierro_verde", "Brazales de hierro verde ×40", dur=3.4, x=.17, y=.62),
    E.rotulo_e(("y pantalones de placas de mitril", -.4), "Del 140 al 210: brazales y placas de mitril", sello="40", dur=3.4),
    mapa("tuercespina", [(29.0, 75.4, "Brikk Finoficio", "Bahía del Botín · los dos bandos", "brikk")],
         ("El rango de artesano lo enseña Brikk", -.2), ("Y en Tanaris, Derotain Sorbelodo", -.1),
         [("El rango de artesano lo enseña Brikk", .5)], "VEGA DE TUERCESPINA", "el artesano de herrería"),
    mapa("tanaris", [(51.2, 27.5, "Derotain Sorbelodo", "Gadgetzan · piezas imperiales", "derotain")],
         ("Y en Tanaris, Derotain Sorbelodo", -.1), ("de piezas imperiales|fin", .5),
         [("Y en Tanaris, Derotain Sorbelodo", .4)], "TANARIS", "misiones de piezas imperiales"),
    mg(P.barras("HERRERÍA · DEL 270 AL 300", F("o_barra_torio"), 500, 1200, "barras de torio", "la diferencia: un par de planos"),
       ("Y aquí viene el golpe", -.2), ("o no un par de planos|fin", .8),
       ["calcula entre quinientas", "y mil doscientas barras de torio", "La diferencia es si encuentras"], "barras de torio", y=.52),
    E.rotulo_e(("ocho planos de placas bendecidas", -.2), "8 planos de placas bendecidas · del 240 al 300", sello="8", dur=4.4),
    tarj(("El peto, de unas arpías", -.2), "o_diseno_peto_bendecidas", "Plano: peto de placas bendecidas", "arpías de Monte Hyjal",
                dur=3.8, x=.74, tam=420),
    pv(("El peto, de unas arpías", .2), "monte_hyjal_2", "Monte Hyjal", dur=3.8, x=.20, y=.50, tam=460),
    tarj(("Y aquí entra el Favor", -.2), "o_cajon_arrebatado", "Favor de comerciante", "el sistema nuevo más grande", dur=4.0, x=.74, tam=420),
    pv(("Se gana llenando cajones de", -.2), "o_cajon_arrebatado", "Cajones de materiales", dur=4.0, x=.17, y=.62),
    tar(("Se gana llenando cajones de", .1), "Favor de comerciante", "o_cajon_arrebatado",
        ["Se gana llenando cajones de materiales", "Para dos campamentos de mercaderes", dict(t="El sistema nuevo más grande", c=V)], dur=4.6),
    mapa("mundo", [(29.2, 49.1, "Campamento de Favor (H)", "Los Baldíos · al oeste de El Cruce", "o_cajon_arrebatado"),
                   (76.2, 77.0, "Campamento de Favor (A)", "Tres Caminos · Crestagrana", "o_cajon_arrebatado")],
         ("La Horda lo tiene al oeste", -.2), ("venden las mismas recetas|fin", .4),
         [("La Horda lo tiene al oeste", .3), "y la Alianza en Tres Caminos"], "AZEROTH", "los dos campamentos de mercaderes", zmax=1.2),
    fav("trade_blacksmithing", "herrería · malla y placas", 61, "Para la herrería hay sesenta", ("y de placas para cada papel del grupo|fin", .5)),
    E.ficha_e("CAMPAMENTO DEL HERRERO", ["o_rueda_afilar", "o_yunque", "o_forja_maestra"], ("En el campamento, el herrero", -.2),
              ("que piden muchas recetas|fin", .6), ["pone una rueda de afilar", "Luego un yunque", "la forja maestra, que piden"],
              etiquetas=["fuerza", "yunque", "forja · 300"]),
    mapa("paramos", [(38.2, 77.5, "Gilnid", "Las Minas de la Muerte · plano del yunque", "gilnid")],
         ("El plano del yunque lo", -.2), ("el Señor gólem Argelmach", -.3),
         [("El plano del yunque lo", .5)], "PÁRAMOS DE PONIENTE", "Las Minas de la Muerte"),
    tarj(("el Señor gólem Argelmach", -.3), "argelmach", "Señor gólem Argelmach", "plano de la forja maestra", dur=4.4, x=.74),
    pv(("en Profundidades de Roca Negra. Y", -.4), "profundidades_roca_negra", "Profundidades de Roca Negra", dur=3.6, x=.22, y=.62, tam=420),
    tar("Y un detalle de combate", "Piedras de afilar en Forever", "inv_stone_sharpeningstone_02",
        [dict(t="Se acumulan con los venenos", c=V), dict(t="Y con Viento Furioso", c=V)], calidad="blanco", dur=5.8),
    # =========================================================== JULSI (488-511 s)
    com(("Y aquí va un espectador de", -.1), "julsikakku", dur=6.0, x=.32, y=.30),
    mg(M.contadores("JULSIKAKKU · EN CINCO DÍAS", [("trade_mining", "minería", 145, 0, 1), ("trade_blacksmithing", "herrería", 120, 1, 2)],
                    ("2 o 3 horas al día", 2)),
       ("llevaba minería ciento cuarenta y", -.3), ("A su ritmo, sin correr", .4),
       ["llevaba minería ciento cuarenta y", "y herrería ciento veinte", "en cinco días|fin"], "julsi contadores", y=.52),
    E.rotulo_e(("A su ritmo, sin correr", .3), "A su ritmo, sin correr", sello="36", dur=4.0),
    pv(("rumbo a la zona nueva", -.3), "claros_del_rio", "Claros del Río · la zona nueva", dur=4.4, x=.74, y=.46, tam=540),
    # =========================================================== P03 · INGENIERÍA (513-620 s)
    par(3, "INGENIERÍA", "o_prof_ingenieria", [(1, 56, "polvo y tornillos"), (56, 150, "bombas y dinamita"), (150, 200, "granadas y ovejas")],
        "Parada tres. Ingeniería", ("Del uno al cincuenta y seis", -.2), "el final: trastos y tubos de torio", ("Parada tres. Ingeniería", 2.2)),
    E.ficha_e("DEL 1 AL 56", ["o_polvo_explosivo_tosco", "inv_misc_gear_06", "o_llave_arco_voltaico"], ("Del uno al cincuenta y seis", -.2),
              ("Empieza en Orgrimmar o en", -.2), ["polvo explosivo tosco y tornillos", "y tornillos de cobre, y", "la llave inglesa de arco"],
              etiquetas=["polvo", "tornillos", "llave"]),
    E.rotulo_e(("Empieza en Orgrimmar o en", 0), "Empieza en Orgrimmar o en Forjaz", sello="!", dur=4.0),
    E.ficha_e("DEL 56 AL 150", ["inv_misc_bomb_09", "inv_misc_bomb_06", "inv_gizmo_pipe_01", "inv_gizmo_02"], ("Del cincuenta y seis al ciento", -.2),
              ("y cacharros zumbones|fin", .8), ["bombas de cobre, dinamita", "dinamita, tubos de bronce", "tubos de bronce y cacharros",
                                                 "y cacharros zumbones"], etiquetas=["bombas", "dinamita", "tubos", "cacharros"]),
    mapa("orgrimmar", [(76.0, 25.1, "Roxxik", "ingeniería · experto (H)", "roxxik")],
         ("Del ciento cincuenta al doscientos, con Roxxik", -.2), ("o con Springspindle en Forjaz", -.1),
         [("con Roxxik en Orgrimmar o", .1)], "ORGRIMMAR", "del 150 al 200"),
    mapa("forjaz", [(68.5, 43.5, "Springspindle", "Ciudad Manitas · experto (A)", "springspindle")],
         ("o con Springspindle en Forjaz", -.1), ("y quince ovejas explosivas", -.2),
         [("o con Springspindle en Forjaz", .3)], "FORJAZ", "del 150 al 200"),
    pv(("y quince ovejas explosivas", -.5), "o_oveja_explosiva", "Oveja explosiva ×15", dur=3.0, x=.17, y=.62),
    mapa("tanaris", [(51.2, 27.5, "Buzzek Giracorchete", "Gadgetzan · los dos bandos", "gadgetzan")],
         ("El rango de artesano lo enseña, en", -.2), ("también Kayleena Encantaflores, en", -.4),
         [("en el pueblo goblin de Gadgetzan", .2)], "TANARIS", "el artesano de ingeniería"),
    mapa("hyjal", [(60.2, 61.4, "Kayleena Encantaflores", "artesano · novedad de Forever", "kayleena")],
         ("también Kayleena Encantaflores, en", -.4), ("Y para el final, trastos", -.1),
         [("también Kayleena Encantaflores, en", .2)], "MONTE HYJAL", "el otro artesano"),
    tarj(("Y para el final, trastos", 0), "o_tubo_torio", "Tubo de torio", "unas 186 barras de torio", dur=4.6, x=.74, tam=420),
    pv(("unas ciento ochenta y seis barras", -.9), "o_barra_torio", "Barra de torio ×186", dur=3.0, x=.17, y=.62),
    mapa("cuna_invierno", [(61.2, 38.2, "Vista Eterna", "esquema del tubo de torio", None)],
         ("El esquema del tubo se compra", -.6), ("o con Kor'gar, en Claros", .2),
         [("El esquema del tubo se compra", -.1)], "CUNA DEL INVIERNO", "el esquema del tubo"),
    mapa("riverglades", [(77.6, 50.8, "Kor'gar", "esquema del tubo de torio", None)],
         ("o con Kor'gar, en Claros", .2), ("en Cima del Trueno no hay", 0),
         [("o con Kor'gar, en Claros", .5)], "CLAROS DEL RÍO", "o con Kor'gar"),
    E.rotulo_e(("en Cima del Trueno no hay", 0), "Cima del Trueno y Darnassus: sin ingeniero", sello="0", dur=5.6),
    E.peg_e(("en Cima del Trueno no hay", .3), "o_prof_ingenieria", "Sin ingeniero", dur=5.0, x=.76, y=.46, tam=340),
    tar("el gnomo ya no recibe sus", "Gnomos en Forever", "achievement_character_gnome_male",
        [dict(t="Sin los 15 puntos gratis de ingeniería", c=RJ), dict(t="Sus cacharros fallan menos", c=V)], dur=6.6),
    fav("trade_engineering", "ingeniería", 26, "Hay veintiséis recetas de Favor", None),
    tarj(("la versión segura de los explosivos", .5), "o_dinamita_saft", "Versión segura de los explosivos",
                "la lanza quien no es ingeniero", dur=4.6, x=.74, tam=420),
    pv(("una bolsa de bombas que", -.2), "o_bolsa_bombas_cobre", "Bolsa de bombas · sin munición", dur=4.0, x=.17, y=.62),
    tarj(("el parapente goblin ultraliviano", -.6), "o_parapente_goblin", "Parapente goblin ultraliviano", "al 300", dur=3.0, x=.74, tam=420),
    E.ficha_e("CAMPAMENTO DEL INGENIERO · SERVICIOS", ["o_robot_componentes", "o_robot_reparacion"], ("Y sus objetos de campamento son", -.2),
              ("y un robot de reparación|fin", .5), ["un robot que vende componentes", "y un robot de reparación"],
              etiquetas=["vende", "repara"]),
    mapa("paramos", [(38.2, 77.5, "Sneed", "Las Minas de la Muerte · robot de reparación", "sneed")],
         ("El plano del robot de reparación", -.2), ("Y al trescientos, el banco", -.1),
         [("lo suelta Sneed, en Las", .1)], "PÁRAMOS DE PONIENTE", "Las Minas de la Muerte"),
    mapa("peste_este", [(26.1, 10.4, "Ezra Grimm", "Stratholme · banco de anarquista", "ezra_grimm")],
         ("Y al trescientos, el banco", -.1), ("que suelta Ezra Grimm en Stratholme|fin", .7),
         [("que suelta Ezra Grimm en", .1)], "TIERRAS DE LA PESTE DEL ESTE", "Stratholme"),
    # =========================================================== BURLA0 · Goca (623-654 s)
    com(("Y antes de seguir, un comentario", 0), "goca912", dur=11.0, x=.32, y=.32),
    E.peg_e(("un lingote de cobre de", -.2), "o_barra_cobre", "Barra de cobre · Alianza", dur=5.0, x=.26, y=.52, tam=340),
    E.peg_e(("lo mismo que uno de la Horda", -.2), "o_barra_cobre", "Barra de cobre · Horda", dur=4.0, x=.74, y=.52, tam=340),
    mapa("mundo", [(71.8, 77.3, "Elwynn", "Alianza", None), (34.3, 44.1, "Durotar", "Horda", None)],
         ("te lo digo separado y", -.2), ("por lo menos ya sabes dónde", 0),
         [("te lo digo separado y", .3), "con el mapa de cada bando"], "AZEROTH", "cada bando, su mapa", zmax=1.2),
    pv(("ya sabes dónde comprar vendas", -.3), "o_venda_lino", "Venda de lino", dur=4.0, x=.76, y=.50, tam=340),
    # =========================================================== GRACIAS1 (655-689 s): uno a la vez, nunca encimados
    com(("Jesús, que juega desde dos", -.3), "jesus_izquierdo", dur=8.8, x=.32, y=.30),
    com(("Óscar volvió al juego después", -.2), "oscar_anv", dur=6.6, x=.66, y=.34),
    com(("Y Barón Rata ya va", -.2), "baron_rata", dur=3.2, x=.32, y=.30),
    com(("Y un espectador, Steven, que", 0), "steven", dur=6.4, x=.66, y=.34),
    E.rotulo_e(("Gracias a los cuatro", 0), "Todos los comentarios se leen", sello="4", dur=4.4),
    # =========================================================== P04 · HERBORISTERÍA (690-794 s)
    par(4, "HERBORISTERÍA", "o_prof_herboristeria", [(1, 70, "flor de paz y hojaplata"), (70, 115, "marregal y brezospina"),
                                                     (115, 170, "cardenal y sangrerregia"), (170, 205, "espina de oro"), (205, 230, "Tanaris")],
        "Parada cuatro. Herboristería", ("Del uno al setenta, flor", -.2), "alimenta a la alquimia y a los primeros auxilios",
        "la que alimenta a la alquimia"),
] + filav("Del uno al setenta, flor", [("o_flor_paz", "Flor de paz", ("flor de paz y hojaplata en", 0)),
                                       ("o_hojaplata", "Hojaplata", ("y hojaplata en cualquier zona", 0))], y=.58, tam=320, dur=3.4, xs=(.15, .35)) + [
    tar(("Ahí hay también versiones marchitas", -.2), "Herboristería del 1 al 70", "o_flor_paz",
        ["Flor de paz y hojaplata", "Versiones marchitas y atrofiadas", dict(t="Entrenador júnior en la zona", c=V)], calidad="blanco", dur=5.2),
    E.rotulo_e(("Ahí hay también versiones marchitas", .5), "Versiones marchitas y atrofiadas · entrenador júnior", sello="!", dur=4.0),
    mapa("argenteos", [(54.6, 27.0, "Marregal", "70-115", "o_marregal"), (54.5, 76.6, "Brezospina", "70-115", "o_brezospina")],
         ("Del setenta al ciento quince", -.2), ("Del ciento quince al ciento setenta", -.2),
         [("marregal y brezospina en el", .1), ("marregal y brezospina en el", .9)], "BOSQUE DE ARGÉNTEOS", "o Loch Modan, o Costa Oscura"),
    mapa("laderas", [(36.5, 56.1, "Sangrerregia", "115-170", "o_sangrerregia")],
         ("Del ciento quince al ciento setenta", -.2), ("o Sierra Espolón: hierba cardenal", .4),
         [("Del ciento quince al ciento setenta", 1.0)], "LADERAS DE TRABALOMAS", "115-170"),
    mapa("sierra_espolon", [(35.0, 64.2, "Hierba cardenal", "115-170", None)],
         ("o Sierra Espolón: hierba cardenal", .4), ("Del ciento setenta al doscientos cinco", -.2),
         [("o Sierra Espolón: hierba cardenal", .8)], "SIERRA ESPOLÓN", "hierba cardenal, acérita salvaje"),
    mapa("tuercespina", [(35.1, 15.2, "Mostacho de Khadgar", "170-205", "o_mostacho_khadgar"), (45.7, 35.9, "Espina de oro", "170-205", None)],
         ("Del ciento setenta al doscientos cinco", -.2), ("Y Claros del Río es una", -.1),
         [("la Vega de Tuercespina o Arathi", .2), ("pálida, espina de oro y", .3)], "VEGA DE TUERCESPINA", "o Arathi"),
    pv(("Y Claros del Río es una", -.1), "claros_del_rio_2", "Claros del Río · llena de espina de oro", dur=4.2, x=.74, y=.46, tam=540),
    mapa("tanaris", [(44.9, 34.7, "Flor de fuego", "205-230", None), (46.9, 65.5, "Loto cárdeno", "205-230", None)],
         ("Del doscientos cinco al doscientos treinta", -.2), ("Aprende el rango de artesano antes de ir", -.1),
         [("Tanaris o La Garganta de", .1), ("Tanaris o La Garganta de", 1.1)], "TANARIS", "o La Garganta de Fuego"),
    E.rotulo_e(("Aprende el rango de artesano antes de ir", 0), "El artesano, antes de ir: allí no hay entrenador", sello="!", dur=4.2),
    mapa("interior", [(65.4, 47.4, "Solea", "230-270", "o_solea"), (57.6, 42.6, "Champiñón fantasma", "cueva · 230-270", "o_champinon_fantasma")],
         ("Y al final, Tierras del", -.2), ("y Frondavil, con hojasueño", .6),
         [("Tierras del Interior con solea", .3), "y champiñón fantasma"], "TIERRAS DEL INTERIOR", "solea y champiñón fantasma"),
    mapa("frondavil", [(53.6, 14.9, "Hojasueño", "270-300", "o_hojasueno"), (42.9, 43.6, "Flor de plaga", "270-300", None)],
         ("y Frondavil, con hojasueño", .6), ("Lo nuevo de Forever: en Monte", -.1),
         [("y Frondavil, con hojasueño", .8), "y flor de plaga, hasta"], "FRONDAVIL", "hasta el 300"),
    mapa("hyjal", [(44.3, 75.2, "Hojapesadilla", "hierba nueva", "o_hojapesadilla"), (45.2, 86.8, "Salvia demoníaca", "hierba nueva", "o_salvia_demoniaca")],
         ("Lo nuevo de Forever: en Monte", -.1), ("El loto de la muerte no", -.2),
         [("la hojapesadilla, la salvia", 0), ("la salvia demoníaca y el", 0)], "MONTE HYJAL", "tres hierbas nuevas"),
    pv(("y el loto de la muerte", -.1), "o_loto_muerte", "Loto de la muerte", dur=3.4, x=.17, y=.70),
    E.peg_e(("sale de cualquier hierba de", -.3), "monte_hyjal", "Cualquier hierba de Hyjal", dur=4.4, x=.24, y=.56, tam=420),
    tar("El loto de la muerte no", "Loto de la muerte", "o_loto_muerte",
        [dict(t="No sale en el mapa", c=GR), "Sale de cualquier hierba de Hyjal", dict(t="Solo con un encantamiento en los guantes", c=V)],
        calidad="verde", dur=6.8),
    pv(("Y algo que nunca habíamos tenido", -.2), "o_semillas", "Semillas", dur=3.4, x=.17, y=.62),
    E.rotulo_e(("semillas de cuatro rangos", .5), "Semillas de 4 rangos", sello="4", dur=3.6),
    tarj(("que se plantan en un invernadero", -.3), "o_invernadero", "Invernadero", "aquí se plantan las semillas", dur=3.4, x=.74, tam=420),
    pv(("Hay también un injertador de semillas", .2), "o_injertador", "Injertador de semillas", dur=4.6, x=.17, y=.62),
    tar("Hay también un injertador de semillas", "Injertador de semillas", "o_injertador",
        ["Volvió el 19 de noviembre", dict(t="Ahora puede fallar", c=RJ), dict(t="Ya no acepta semillas escasas", c=RJ)], dur=7.6, x=.62),
    dict(tipo="oscurecer", de=("Hay también un injertador de semillas", -.1), a=("Hay también un injertador de semillas", 7.6), k=.55,
         entra=.3, sale=.3),
    tarj(("El primer objeto de campamento del herbolario", -.2), "o_vela_incienso", "Vela de incienso", "da intelecto", dur=4.6, x=.74, tam=420),
    mapa("humedales", [(38.5, 60.5, "Shadetooth", "Sitio de Excavación · plano del invernadero", "excavacion_humedales")],
         ("Y el plano del invernadero lo", -.2), ("lo suelta Shadetooth, en Los Humedales|fin", .6),
         [("lo suelta Shadetooth, en Los", .1)], "LOS HUMEDALES", "el plano del invernadero"),
    # =========================================================== P05 · ALQUIMIA (795-911 s)
    par(5, "ALQUIMIA", "o_prof_alquimia", [(1, 55, "elixires menores"), (55, 150, "maná, entereza y sabiduría"),
                                           (150, 225, "fuego y protección"), (225, 300, "transmutaciones y defensa")],
        "Parada cinco, la alquimia", ("Del uno al cincuenta y cinco, una", -.2), "aquí empieza el cambio más grande del video",
        "Y aquí empieza el cambio"),
    tar(("una receta nueva de Forever, el", -.2), "Elixir de fuerza menor", "o_elixir_fuerza_menor",
        [dict(t="Receta nueva de Forever", c=V), "Del 1 al 55", "Después: elixir de defensa menor"], calidad="blanco", dur=5.6),
] + filav("el elixir de fuerza menor", [("o_elixir_fuerza_menor", "Elixir de fuerza menor · nuevo", None),
                                        ("o_elixir_defensa_menor", "Elixir de defensa menor", "y después el elixir de defensa")],
          y=.62, tam=320, dur=3.6, xs=(.13, .33)) + [
    E.ficha_e("DEL 55 AL 150", ["inv_potion_70", "inv_potion_43", "inv_potion_06", "inv_potion_38"], ("Del cincuenta y cinco al ciento cincuenta, pociones", .5),
              ("y aceite de fuego|fin", .6), ["pociones de maná menores, elixires", "elixires de entereza y de", "y de sabiduría, y aceite",
                                              "y aceite de fuego"], etiquetas=["maná", "entereza", "sabiduría", "fuego"]),
    E.ficha_e("DEL 150 AL 225", ["inv_potion_33", "inv_potion_72", "inv_potion_06"], ("Del ciento cincuenta al doscientos veinticinco, elixir", -.2),
              ("Esa receta se compra en", -.2), ["elixir de poder de fuego", "pociones de maná y pociones", "protección contra la naturaleza. Esa"],
              etiquetas=["fuego", "maná", "natural"]),
    tar("Esa receta se compra en", "Receta: Poción de protección contra la Naturaleza", "inv_potion_06",
        ["Se compra en Feralas", "En Tuercespina", "O en Tanaris"], calidad="verde", dur=5.0),
    tar("Del doscientos veinticinco al trescientos, más", "Del 225 al 300", "trade_alchemy",
        ["Protección contra la naturaleza", "Transmutaciones de paso", "Aceite escama pétrea", dict(t="Elixir de defensa superior", c=V)], dur=8.4),
    mg(M.contadores("ALQUIMIA DEL 1 AL 300", [("trade_herbalism", "hierbas, más o menos", 1000, 0, 1)], ("POR ESO, CON HERBORISTERÍA", 2)),
       ("En total, del uno al", -.2), ("combina con la herboristería|fin", .6),
       [("alrededor de mil hierbas", 0), ("alrededor de mil hierbas|fin", 0), "Por eso tanta gente la"], "mil hierbas", y=.52),
    mapa("pantano", [(48.5, 55.8, "Rogvar", "alquimia · artesano (H)", "rogvar")],
         ("El rango de artesano lo enseñan Rogvar", -.2), ("y Kylanna, en Feralas, para", -.1),
         [("lo enseñan Rogvar, en el", .1)], "PANTANO DE LAS PENAS", "la Horda"),
    mapa("feralas", [(32.6, 43.8, "Kylanna", "alquimia · artesano (A)", "kylanna")],
         ("y Kylanna, en Feralas, para", -.1), ("Y hay un tercero para los", -.1),
         [("y Kylanna, en Feralas, para", .3)], "FERALAS", "la Alianza"),
    mapa("frondavil", [(50.9, 81.3, "Santuario Esmeralda", None, None),
                       (51.5, 82.0, "Maestro micólogo Shurome", "del 1 al 300 · los dos bandos", "shurome")],
         ("Y hay un tercero para los", -.1), ("Y por ahora te deja", -.1),
         [("Y hay un tercero para los", .4), ("Shurome, en el Santuario Esmeralda", .2)], "FRONDAVIL", "un tercero, para los dos bandos"),
    E.rotulo_e(("Y por ahora te deja", 0), "Por ahora, el artesano sin pedirte 200", sello="!", dur=4.0),
    pv(("las pociones de sanación ya no son del alquimista. Se", -.3), "o_pocion_sanacion", "Poción de sanación", dur=5.4, x=.76, y=.48, tam=340),
    E.rotulo_e(("Se fueron a otra profesión", -.1), "Se fueron a otra profesión: al final del video", sello="?", dur=3.8),
    mg(P.flujo("EL ALQUIMISTA AHORA HACE TINTES", [(0, 1, F("o_prof_alquimia"), "Alquimia"), (1, 0, F("o_tinte_ceruleo"), "Tinte cerúleo"),
                                                   (1, 1, F("o_tinte_magenta"), "Tinte magenta"), (1, 2, F("o_tinte_esmeralda"), "Verde esmeralda"),
                                                   (2, 0, F("o_prof_sastreria"), "Sastrería"), (2, 2, F("o_prof_peleteria"), "Peletería")],
               [(0, 1), (0, 2), (0, 3), (1, 4), (2, 4), (3, 5)], ("CLIENTES NUEVOS", 6), ancho=1500),
       ("Lo que ganó a cambio son", -.2), ("tiene clientes nuevos|fin", .7),
       [("Lo que ganó a cambio son", .2), "tinte cerúleo, magenta y", ("magenta y verde esmeralda", 0), ("y verde esmeralda, que", .2),
        "que piden la sastrería y", ("la sastrería y la peletería", .6), "El alquimista tiene clientes"], "tintes", y=.52),
    fav("trade_alchemy", "alquimia", 28, "Y veintiocho recetas de Favor", None),
    tarj(("hasta el elixir del oso pardo", -.2), "o_elixir_oso_pardo", "Elixir del oso pardo", "pide 300 y reputación honorable",
                dur=4.4, x=.74, tam=420),
    E.ficha_e("CAMPAMENTO DEL ALQUIMISTA", ["o_pozo_mana", "o_fermentador", "o_laboratorio_alquimia"], ("En el campamento, el alquimista", -.2),
              ("un laboratorio de alquimia|fin", .6), ["pone un pozo de maná", "luego un fermentador", "un laboratorio de alquimia"],
              etiquetas=None),
    pant("scholomance", ("Con el laboratorio, los frascos", -.2), ("se hacen junto a la hoguera|fin", .3), zoom=(1.0, 1.12)),
    pv(("Su plano lo suelta allí", .2), "o_laboratorio_alquimia", "Laboratorio de alquimia", dur=4.4, x=.20, y=.62),
    tarj(("Su plano lo suelta allí", -.2), "ras_levescarcha", "Ras Levescarcha", "plano del laboratorio · Scholomance", dur=5.4, x=.74),
    # =========================================================== BURLA1 · Crisis (913-939 s)
    com(("Y otro comentario, porque nos", 0), "crisisx94", dur=11.6, x=.32, y=.32),
    pv(("pero una veta de torio libre", -.3), "o_mena_torio", "Una veta de torio libre", dur=3.6, x=.76, y=.50, tam=340),
    mg(M.tiempos("EL PLAN", [("CON CALMA", 10, VERDE), ("¡CORRE A LA VETA!", 10, ROJO)], "antes de que llegue otro"),
       ("Así que tómatelo con calma", -.2), ("antes de que llegue otro|fin", .6),
       [("Así que tómatelo con calma", .2), "y luego corre a la veta", "antes de que llegue otro"], "calma y corre", y=.52),
    # =========================================================== P06 · DESUELLO (940-1046 s)
    par(6, "DESUELLO", "o_prof_desuello", [(1, 75, "zonas iniciales"), (75, 150, "Baldíos · Loch Modan"), (150, 225, "yetis y huargos"),
                                           (225, 280, "Feralas"), (280, 300, "Un'Goro")],
        "Parada número seis, el desuello", ("Uno de nivel treinta pide", -.2), "va pegada a la peletería", "la recolección que va pegada"),
    mg(M.contadores("LA REGLA: CINCO VECES SU NIVEL", [("inv_misc_pelt_wolf_01", "nivel del bicho", 30, 0, 1),
                                                       ("inv_misc_armorkit_17", "desuello que pide (×5)", 150, 1, 2)]),
       ("Uno de nivel treinta pide", -.2), ("Y en Forever, los bichos", -.1),
       ["Uno de nivel treinta pide", "pide ciento cincuenta", ("pide ciento cincuenta|fin", .3)], "regla ×5", y=.52),
    mapa("mundo", [(33.1, 43.8, "Durotar", "jabalíes · 1-75 (H)", "o_prof_desuello"), (72.0, 76.8, "Bosque de Elwynn", "lobos · 1-75 (A)", "o_prof_desuello")],
         ("Y en Forever, los bichos", -.1), ("Para el tramo del setenta", -.1),
         ["jabalíes en Durotar", "o lobos en el Bosque"], "AZEROTH", "desuello · hasta el 75", zmax=1.2),
    mapa("baldios", [(60.2, 33.8, "Zancudos", "75-150 (H)", "o_prof_desuello"), (61.2, 54.7, "Fuerte del Norte", "raptores al oeste", None)],
         ("Para el tramo del setenta", -.1), ("Y la Alianza, a Loch", .5),
         [("la Horda va a Los", .2), ("al oeste de Fuerte del", .2)], "LOS BALDÍOS", "la Horda · 75-150"),
    mapa("loch_modan", [(63.2, 40.8, "Cocodrilos, osos y jabalíes", "75-130 (A)", "o_prof_desuello")],
         ("Y la Alianza, a Loch", .5), ("Del ciento cincuenta al doscientos veinticinco, la", -.2),
         [("Y la Alianza, a Loch", .7)], "LOCH MODAN", "la Alianza · 75-130 · y luego Los Humedales"),
    mapa("alterac", [(36.5, 85.9, "Cueva de yetis", "150-225 · entrada desde Laderas", "o_prof_desuello")],
         ("Del ciento cincuenta al doscientos veinticinco, la", -.2), ("O los huargos del Bosque", -.5),
         [("la cueva de yetis de Laderas", .1)], "MONTAÑAS DE ALTERAC", "la cueva de yetis"),
    mapa("bosque_ocaso", [(62.8, 68.2, "Huargos", "150-225", "o_prof_desuello"), (64.6, 35.6, "Huargos", None, None)],
         ("O los huargos del Bosque", -.5), ("Del doscientos veinticinco al doscientos ochenta", .3),
         [("O los huargos del Bosque", .4), ("O los huargos del Bosque", 1.4)], "BOSQUE DEL OCASO", "los huargos"),
    mapa("feralas", [(54.6, 56.5, "Vega Cicatriz Feral", "yetis · 225-280", "o_cuero_grueso")],
         ("Del doscientos veinticinco al doscientos ochenta", .3), ("Y el final, los diemetradones", -.1),
         [("los yetis de la Vega", .1)], "FERALAS", "225-280"),
    mapa("ungoro", [(36.0, 35.2, "Diemetradones y pterrordáctilos", "280-300", "o_cuero_basto"), (35.5, 46.0, "Diemetradones", None, None)],
         ("Y el final, los diemetradones", -.1), ("Y la Horda tiene un regalo", -.1),
         [("Y el final, los diemetradones", .5), ("y pterrordáctilos de Un'Goro", .2)], "CRÁTER DE UN'GORO", "280-300"),
    tarj(("el cuchillo para desollar afilado", -.3), "o_cuchillo_afilado", "Cuchillo para desollar afilado",
                "+3 · misión en Los Baldíos (H)", dur=5.4, x=.74, tam=420),
    E.peg_e(("cada criatura se desuella una", .2), "o_prof_desuello", "Una sola vez", dur=4.6, x=.20, y=.60),
    tar("cada criatura se desuella una", "Desuello en Forever", "inv_misc_pelt_wolf_01",
        [dict(t="Una sola vez por criatura", c=RJ), dict(t="Lo que otro mata y no desuella: tuyo", c=V)], dur=7.6),
] + filav("cuero prístino, pellejo prístino y", [("o_cuero_pristino", "Cuero prístino", None),
                                                ("o_pellejo_pristino", "Pellejo prístino", ("pellejo prístino y escama", 0)),
                                                ("o_escama_pristina", "Escama prístina", ("y escama prístina. En", 0))], y=.62, tam=300, dur=3.0, xs=(.14, .37, .60)) + [
    mg(O.desplome("CUERO PRÍSTINO", [("en la beta", 100), ("1.ª semana", 5)], "de más de 1 de oro a unas 5 platas"),
       ("En la beta, el cuero", 1.9), ("bajó a unas cinco platas|fin", .8),
       [("En la beta, el cuero", 2.1), "en la primera semana bajó", "bajó a unas cinco platas"], "cuero prístino precio", y=.52),
    mapa("riverglades", [(65.2, 53.1, "Cuero pesado", "bestias de las llanuras", "o_cuero_pesado")],
         ("Claros del Río también sirve", -.2), ("Y en Monte Hyjal, cuero", .3),
         [("tiene bestias que dan mucho", .2)], "CLAROS DEL RÍO", "mucho cuero pesado"),
    mapa("hyjal", [(74.3, 36.6, "Cuero basto", None, "o_cuero_basto")],
         ("Y en Monte Hyjal, cuero", .3), ("En el campamento, el desollador", .4),
         [("Y en Monte Hyjal, cuero", .6)], "MONTE HYJAL", "cuero basto"),
    E.ficha_e("CAMPAMENTO DEL DESOLLADOR", ["o_silla_campamento", "o_guia_campo"], ("En el campamento, el desollador", .4),
              ("aprende a rastrear bestias|fin", .5), ["pone una silla de campamento", "una guía de campo con"],
              etiquetas=["crítico", "rastrear"]),
    tarj(("El plano de la guía lo", -.2), "lady_anacondra", "Lady Anacondra", "plano de la guía de campo", dur=4.2, x=.74),
    pv(("en las Cuevas de los Lamentos. Y al", -.3), "cuevas_lamentos", "Cuevas de los Lamentos", dur=3.6, x=.22, y=.62, tam=420),
    pv(("al trescientos llega un banco", -.2), "o_banco_trampero", "Banco de trabajo de trampero · 300", dur=4.0, x=.76, y=.50, tam=340),
    # =========================================================== P07 · PELETERÍA (1048-1159 s)
    par(7, "PELETERÍA", "o_prof_peleteria", [(1, 60, "cuero ligero"), (60, 130, "cuero oscuro"), (130, 205, "hombreras bárbaras"),
                                             (205, 300, "cuero grueso y basto")],
        "Parada siete. Peletería", ("Del uno al sesenta, cuero", -.2), "el objeto que más agradece quien sube de nivel",
        "el objeto de campamento que más"),
    pv(("Del uno al sesenta, cuero", .4), "o_cuero_ligero", "Cuero ligero", dur=4.0, x=.17, y=.62),
    tar(("y guantes de cuero repujado", -.4), "Peletería del 1 al 130", "inv_misc_armorkit_17",
        ["Pellejo ligero curtido", "Guantes de cuero repujado", "60-130: pantalones y cinturones", dict(t="Pellejo medio curtido", c=V)], dur=7.0),
] + filav("lo enseñan Una en Cima", [(Fc("una"), "Una · Cima del Trueno", None), (Fc("telonis"), "Telonis · Darnassus", "Telonis en Darnassus, o")],
          y=.56, tam=380, dur=3.0, xs=(.18, .42)) + [
    mapa("shendralas", [(42.6, 78.1, "Jarael", "peletería · experto", None)],
         ("o Jarael en Shen'dralas, la", -1.6), ("Del ciento treinta al doscientos cinco", .4),
         [("o Jarael en Shen'dralas, la", .3)], "SHEN'DRALAS", "zona nueva, casi de la Horda"),
    E.rotulo_e(("Del ciento treinta al doscientos cinco", .4), "Del 130 al 205", sello="!", dur=4.4),
    tar(("hombreras bárbaras, guantes de guardián", -.3), "Peletería del 130 al 205", "inv_misc_armorkit_17",
        ["Hombreras bárbaras", "Guantes de guardián", dict(t="Y cintas", c=V)], dur=4.6),
    mapa("mundo", [(23.2, 64.7, "Hahrana Pielférrea", "Feralas · artesano (H)", "hahrana"), (76.6, 37.9, "Drakk Stonehand", "Tierras del Interior · artesano (A)", "drakk")],
         ("El artesano está fuera de", -.2), ("para la Alianza. Del doscientos cinco", .2),
         [("Hahrana Pielférrea, en Feralas, para", .1), ("y Drakk Stonehand, en Tierras", .1)], "AZEROTH", "el artesano, fuera de las capitales", zmax=1.2),
    mg(M.contadores("PELETERÍA DEL 205 AL 300", [("inv_misc_leatherscrap_08", "cueros gruesos · el primer tramo", 500, 0, 1)],
                    ("Y LUEGO, CIENTOS DE CUEROS BASTOS", 2)),
       ("unos quinientos cueros gruesos", -.4), ("y paño rúnico|fin", .3),
       ["unos quinientos cueros gruesos", "solo para el primer tramo", "y luego cientos de cueros"], "500 cueros", y=.52),
    pv(("Y hay un patrón nuevo con", -.2), "o_patron_zapatos_gamuza", "Patrón nuevo", dur=4.2, x=.17, y=.62),
    tarj(("los zapatos de gamuza azul", -.3), "o_zapatos_gamuza", "Zapatos de gamuza azul", "del 235 al 265", dur=5.4, x=.74, tam=420),
    E.rotulo_e(("Hay también brazales y un", 0), "Gamuza azul: brazales y sombrero", sello="!", dur=3.6),
    pv(("necesita una máquina de coser", -.3), "o_maquina_coser", "Máquina de coser", dur=3.6, x=.76, y=.50, tam=340),
    fav("inv_misc_armorkit_17", "peletería · cuero y malla", 81, "ochenta y una recetas de"),
    tarj(("Muchas recetas piden un expositor", -.2), "o_expositor_curtido", "Expositor de curtido", "desde el 6-nov: con 125",
                dur=6.6, x=.74, tam=420),
    tarj(("Y aquí está la joya", -.2), "o_tienda_campamento", "Tienda de campamento", "descanso: hasta 5 % de un nivel, 1 vez por hora",
                dur=7.8, x=.74, tam=460),
    pv(("Y aquí está la joya", .4), "o_prof_peleteria", "La joya del peletero", dur=4.0, x=.17, y=.62),
    pant("campamento", ("Por eso la peletería es", -.2), ("el peletero siempre es bienvenido|fin", .4), zoom=(1.12, 1.0), pan=(.04, 0, -.04, 0)),
    tarj(("La máquina de coser, al", -.2), "vectus", "Vectus", "máquina de coser · Scholomance", dur=5.0, x=.74),
    pv(("la suelta Vectus, en Scholomance", .3), "scholomance", "Scholomance", dur=3.8, x=.22, y=.60, tam=420),
    # =========================================================== P08 · SASTRERÍA (1160-1286 s)
    par(8, "SASTRERÍA", "o_prof_sastreria", [(1, 55, "lino"), (55, 140, "lana y seda"), (140, 200, "tejido mágico"),
                                             (200, 225, "bolsas rojas"), (250, 280, "puños rúnicos")],
        "Parada ocho. Sastrería", ("Del uno al cincuenta y cinco, madejas", -.2), "no necesita recolección: la tela te cae",
        "la tela te cae de"),
    E.ficha_e("DEL 1 AL 140", ["inv_fabric_linen_02", "inv_fabric_wool_01", "inv_fabric_silk_01"], ("Del uno al cincuenta y cinco, madejas", -.2),
              ("capuchas y mochilas pequeñas|fin", .5), ["madejas de lino y cinturones", "lana y seda: capas", ("lana y seda: capas", .5)],
              etiquetas=["lino", "lana", "seda"]),
    pv(("lo enseñan Josef Gregorian en", -.2), Fc("josef_gregorian"), "Josef Gregorian · Entrañas", dur=3.6, x=.20, y=.52, tam=440),
    mapa("ventormenta", [(53.3, 81.5, "Georgio Bolero", "sastrería · experto (A)", "georgio_bolero")],
         ("y Georgio Bolero en Ventormenta", -.3), ("y en Shen'dralas está Melanori", -.8),
         [("y Georgio Bolero en Ventormenta", .3)], "VENTORMENTA", "el experto de la Alianza"),
    E.rotulo_e(("La Alianza tiene además a Charles", 0), "Alianza: también Charles Worth, en Dalaran", sello="!", dur=3.0),
    mapa("shendralas", [(43.4, 77.8, "Melanori", "sastrería · experto", None)],
         ("y en Shen'dralas está Melanori", -.8), ("Del ciento cuarenta al doscientos, tejido", .3),
         [("y en Shen'dralas está Melanori", .4)], "SHEN'DRALAS", "y Melanori"),
    pv(("Del ciento cuarenta al doscientos, tejido", .3), "o_tejido_magico", "Tejido mágico · del 140 al 200", dur=4.6, x=.17, y=.62),
    tar(("y chalecos y pantalones de", -.4), "Sastrería del 140 al 200", "inv_fabric_mageweave_01",
        ["Tejido mágico", "Chalecos de seda carmesí", dict(t="Pantalones de seda carmesí", c=V)], calidad="blanco", dur=4.4),
    mapa("laderas", [(63.7, 20.8, "Daryl Stack", "Molino Tarren · artesano (H)", "daryl_stack")],
         ("El artesano: Daryl Stack, en", -.2), ("y Timothy Worthington, en Theramore", -.2),
         [("El artesano: Daryl Stack, en", .4)], "LADERAS DE TRABALOMAS", "el artesano de la Horda"),
    mapa("marjal", [(65.0, 47.1, "Theramore", None, None), (66.2, 51.8, "Timothy Worthington", "artesano (A)", "timothy_worthington")],
         ("y Timothy Worthington, en Theramore", -.2), ("Compra el hilo rúnico antes", -.1),
         [("y Timothy Worthington, en Theramore", .2), ("y Timothy Worthington, en Theramore", 1.0)], "MARJAL REVOLCAFANGO", "el artesano de la Alianza"),
    pv(("Compra el hilo rúnico antes", -.1), "o_hilo_runico", "Hilo rúnico · cómpralo antes", dur=3.2, x=.17, y=.62),
    mg(P.bolsas("DEL 200 AL 225", [(F("o_bolsa_tejido_magico_roja"), "Bolsa de tejido mágico roja ×17", 14)], "en Forever, de 14 casillas",
                ancho=900),
       ("Entre el doscientos y el doscientos veinticinco", .5), ("ya son de catorce casillas|fin", .7),
       ["diecisiete bolsas de tejido mágico", "ya son de catorce casillas"], "bolsas rojas", y=.50),
    pv(("un patrón nuevo, los puños", -.2), "o_patron_punos_runicos", "Patrón: puños de paño rúnico", dur=4.4, x=.17, y=.62),
    mapa("hyjal", [(48.2, 33.6, "Pexmit", "patrón de los puños · 10 de oro", "pexmit"), (13.6, 53.0, "Kal'tinzan", "misión de la Horda", None)],
         ("Lo vende Pexmit, en Monte Hyjal, por diez", -.2), ("Calcula unos mil cuatrocientos paños", -.1),
         [("Lo vende Pexmit, en Monte Hyjal, por diez", .3), "o la Horda lo saca"], "MONTE HYJAL", "los puños de paño rúnico"),
    mg(M.contadores("SOLO DEL 250 AL 280", [("inv_fabric_purplefire_01", "paños rúnicos", 1400, 0, 1)], ("LA SASTRERÍA SE PAGA EN TELA", 2)),
       ("Calcula unos mil cuatrocientos paños", -.1), ("se paga en tela|fin", .7),
       ["unos mil cuatrocientos paños", "solo para ese tramo", "La sastrería se paga"], "1400 paños", y=.52),
    mg(P.bolsas("BOLSAS DE COMPONENTES · LA QUINTA RANURA", [(F("o_bolsa_componentes_lino"), "De lino", 6), (F("o_bolsa_componentes_lino"), "De lana", 8),
                                                         (F("o_bolsa_componentes_lino"), "Grande", 12), (F("o_bolsa_componentes_lino"), "Grande", 14)],
                "las grandes, con Favor"),
       ("Lo nuevo de Forever: las bolsas de componentes", -.2), ("Y la de lana pide tinte", .4),
       ["De lino de seis casillas", "de lana de ocho", "y las grandes de doce", "y catorce, con Favor", ("y catorce, con Favor", .6)],
       "bolsas de componentes", y=.50),
    mg(P.flujo("LA BOLSA DE LANA", [(0, 0, F("o_prof_alquimia"), "Alquimia"), (1, 0, F("o_tinte_ceruleo"), "Tinte cerúleo"),
                                               (2, 0, F("o_bolsa_componentes_lino"), "Bolsa de lana")], [(0, 1), (1, 2)],
               ("DE LA PARADA 5 A LA PARADA 8", 3), ancho=1300),
       ("Y la de lana pide tinte", .4), ("con la parada ocho|fin", .7),
       [("Y la de lana pide tinte", .6), "pide tinte cerúleo, que hace", ("pide tinte cerúleo, que hace", .8), "Aquí se conecta la parada"],
       "parada 5 a 8", y=.50),
    fav("trade_tailoring", "sastrería · tela", 67, "Hay sesenta y siete recetas", None),
    tarj(("el sastre pone un estandarte", -.2), "o_estandarte_faccion", "Estandarte de su facción", "da espíritu", dur=4.4, x=.74, tam=420),
    pv(("Al ciento cuarenta, una rueca", -.2), "o_rueca", "Rueca · 140", dur=4.0, x=.17, y=.62),
    mapa("alterac", [(16.7, 68.8, "Ciudad de Dalaran", "centinela inestable · plano de la rueca", "ciudad_dalaran")],
         ("Su plano lo suelta un centinela", -.2), ("Y la trampa: las recetas", -.1),
         [("lo suelta un centinela inestable", .1)], "MONTAÑAS DE ALTERAC", "la rueca"),
    mg(P.telar("LA TRAMPA DEL TELAR", F("o_telar"), ("LAS RECETAS 285-300", "PIDEN UN TELAR"), ("EL TELAR", "SOLO LO FABRICA QUIEN TIENE 300"),
               ["el telar de otro sastre", "otro camino"]),
       ("Y la trampa: las recetas", -.2), ("subes esos últimos puntos por otro camino|fin", .1),
       ["piden un telar. Y el", "Y el telar solo lo", "O encuentras un campamento donde", "o subes esos últimos puntos"], "telar", y=.50),
    tarj(("El plano del telar es", -.2), "baronesa_anastari", "Baronesa Anastari", "plano del telar · Stratholme", dur=4.8, x=.74),
    # =========================================================== P09 · ENCANTAMIENTO (1288-1399 s)
    par(9, "ENCANTAMIENTO", "o_prof_encantamiento", [(1, 70, "mota de magia"), (70, 150, "polvo extraño"), (225, 300, "vara de arcanita")],
        "Parada nueve. Encantamiento", ("Del uno al setenta, con un", -.2), "desencanta todo lo que cose el sastre", "que desencanta todo lo que"),
    tarj(("la mota de magia", -.2), "o_mota_magia", "Mota de magia", "reactivo nuevo de vendedor", dur=4.6, x=.74, tam=420),
    E.rotulo_e(("Forever añadió recetas de nivel", 0), "Recetas nuevas de nivel bajo: más baratas", sello="70", dur=4.2),
    pv(("Hay hasta una varita de", -.2), "o_varita_novato", "Varita de práctica de novato", dur=4.0, x=.76, y=.50, tam=340),
    tar(("absorción menor, vara de plata", -.3), "Encantamiento del 70 al 150", "inv_enchant_duststrange",
        ["Absorción menor", "Vara de plata rúnica", dict(t="Y varitas", c=V)], calidad="blanco", dur=4.4),
] + filav("con polvo extraño o esencia", [("o_polvo_extrano", "Polvo extraño", None),
                                          ("o_esencia_magica_inferior", "Esencia mágica inferior", "o esencia mágica inferior")],
          y=.62, tam=320, dur=5.2, xs=(.16, .36)) + [
    mapa("sierra_espolon", [(49.2, 57.2, "Hgarth", "experto (H) · en un risco", "hgarth"), (47.8, 60.8, "Refugio Roca del Sol", None, "refugio_roca_sol")],
         ("El rango de experto tiene un", -.2), ("Y Kitta Vientofuego, en lo", -.1),
         [("Hgarth, en un risco sobre", .1), ("sobre el Refugio Roca del", .2)], "SIERRA ESPOLÓN", "el experto de la Horda, escondido"),
    mapa("elwynn", [(65.8, 68.1, "Torre de Azora", None, "torre_azora"), (64.8, 70.6, "Kitta Vientofuego", "experto (A) · en lo alto", "kitta")],
         ("Y Kitta Vientofuego, en lo", -.1), ("La Alianza tiene además a Vanessa", -.1),
         [("en lo alto de la Torre", .2), ("Y Kitta Vientofuego, en lo", 2.2)], "BOSQUE DE ELWYNN", "la Torre de Azora"),
    mapa("alterac", [(16.8, 62.3, "Vanessa Sellers", "encantamiento (A) · Dalaran", None)],
         ("La Alianza tiene además a Vanessa", -.1), ("El artesano, para los dos bandos", -.1),
         [("La Alianza tiene además a Vanessa", .5)], "MONTAÑAS DE ALTERAC", "Dalaran"),
    mapa("inhospitas", [(44.2, 12.2, "Annora", "Uldaman · artesano, los dos bandos", "annora")],
         ("El artesano, para los dos bandos", -.1), ("Y aparece cuando limpias todo", -.1),
         [("solo lo enseña Annora, en", .2)], "TIERRAS INHÓSPITAS", "Uldaman"),
    E.rotulo_e(("Y aparece cuando limpias todo", 0), "Annora aparece al limpiar todo a su alrededor", sello="!", dur=3.8),
    E.ficha_e("DEL 225 AL 300", ["inv_potion_100", "inv_potion_104", "inv_wand_09"], ("Del doscientos veinticinco al trescientos, guantes", -.2),
              ("de arcanita para cerrar|fin", .6), ["aceites de maná y de", "y de zahorí, y la", "la vara rúnica de arcanita"],
              etiquetas=["maná", "zahorí", "arcanita"]),
    tarj(("los collares por fin se encantan", -.2), "o_encantar_collar", "Encantar collar", "la fórmula, solo con Favor", dur=4.0, x=.74, tam=420),
    fav("trade_engraving", "encantamiento", 39, "entre treinta y nueve recetas", None),
    tar(("También hay encantamientos de arma", .5), "Lo nuevo del encantador", "trade_engraving",
        ["Encantamientos de arma nuevos", "Reliquias", dict(t="Bastones y orbes para lanzadores", c=V)], dur=5.8),
    E.ficha_e("CAMPAMENTO DEL ENCANTADOR", ["o_laud_encantado", "o_recuperador_arcano"], ("En el campamento, el encantador", -.2),
              ("lo que sacas al desencantar|fin", .5), ["pone un laúd encantado", "un recuperador arcano, que"],
              etiquetas=None),
    pv(("El plano del recuperador lo", -.2), "ciudad_dalaran", "Sombra del archimago · Ciudad de Dalaran", dur=4.4, x=.24, y=.58, tam=460),
    tarj(("Y la forja arcana, al", -.2), "o_forja_arcana", "Forja arcana", "al 300 · la suelta Nanaya", dur=5.4, x=.74, tam=420),
    pv(("en el Bancal del Creador", -.4), "bancal_creador", "Bancal del Creador", dur=3.0, x=.24, y=.58, tam=460),
    E.peg_e(("Y un aviso para las bandas", .6), "o_prof_encantamiento", "Lleva un encantador", dur=5.0, x=.22, y=.50, tam=360),
    tarj(("la esencia maleable de la naturaleza", -.2), "o_esencia_maleable", "Esencia maleable",
                "de la naturaleza · solo desencantando", dur=6.0, x=.74, tam=420),
    # =========================================================== LEGADO (1400-1431 s)
    mg(P.legado("LEGADO DE PROFESIONES", [(F(s), n) for s, n in (PROFS12[1], PROFS12[2], PROFS12[4], PROFS12[6], PROFS12[7], PROFS12[8])],
                ceros=[F(s) for s, _ in (PROFS12[0], PROFS12[3], PROFS12[5], PROFS12[9], PROFS12[10], PROFS12[11])]),
       ("Y con el encantamiento cerramos", -.2), ("que un alternativo suba la fabricación|fin", .6),
       ["al llegar a ciento cincuenta", "a doscientos veinticinco y a", "y a trescientos", "Son dieciocho puntos en total",
        "La recolección y las secundarias"], "legado", y=.52),
    tar("Y en el árbol de Legado", "Árbol de Legado de profesiones", "inv_misc_book_09",
        [dict(t="Horas extra: más probabilidad de puntos", c=V), dict(t="Cosecha abundante: más materiales escasos", c=V)], dur=8.6),
    # =========================================================== BURLA2 · SoyoyoS (1433-1462 s)
    com(("Y un último comentario, con", 0), "soyoyos", dur=10.8, x=.32, y=.32),
    E.rotulo_e(("Fíjate qué educación", 0), "Nos llamó basura, pero se despidió", sello="!", dur=4.0),
    tar("si ves una imprecisión, dinos", "Correcciones", "inv_misc_note_01",
        ["Dinos el minuto", "Y el dato", dict(t="Las justas salen en el siguiente video", c=V)], dur=6.4),
    # =========================================================== P10 · COCINA (1463-1578 s)
    par(10, "COCINA", "o_prof_cocina", [(1, 50, "pececitos o caballa"), (50, 150, "pargo, atún y siluro"), (225, 300, "serviolas y branquirrojos")],
        "Parada diez. Cocina, la primera", ("Porque la cocina ya no", -.2), "la que enciende el campamento", "la que enciende el campamento"),
    pv(("una hoguera que llevas en", -.3), "o_hoguera_basica", "Una hoguera en la mochila", dur=3.4, x=.17, y=.62),
    tarj(("La hoguera básica se aprende", -.2), "o_hoguera_basica", "Hoguera básica", "cocina 1 · madera simple", dur=4.6, x=.74, tam=420),
    pv(("y se hace con madera", -.4), "o_madera_simple", "Madera simple", dur=3.0, x=.17, y=.62),
    mg(P.campamento("EL CAMPAMENTO", [("BÁSICA", 3), ("DE OFICIAL", 5), ("DE EXPERTO", 10)],
                    [F(s) for s in ("o_rueda_afilar", "o_vela_incienso", "o_pozo_mana", "o_silla_campamento", "o_tienda_campamento",
                                    "o_estandarte_faccion", "o_laud_encantado", "o_magnetita", "o_cuenco_pescado", "o_equipo_primeros_auxilios")],
                    "28 millones de objetos en la primera semana"),
       ("Y aquí te explico el campamento", .4), ("de objetos de campamento. La ruta", -.2),
       ["Alguien enciende la hoguera", "y cada jugador alrededor pone", "la de oficial cinco", "y la de experto diez",
        "jugadores pusieron más de veintiocho millones de objetos de campamento. La"], "campamento", y=.55),
    tar("Del uno al cincuenta, pececitos", "Cocina del 1 al 150", "inv_misc_fish_07",
        ["1-50: pececitos luminosos o caballa", "50-150: pargo de lodo, atún blanco", dict(t="Y el siluro mostacherizo", c=V)], dur=9.6),
    mapa("desolace", [(26.2, 69.8, "Wulan", "Aldea Cazasombras · libro de cocina (H)", "wulan")],
         ("El experto es un libro: lo vende Wulan", -.2), ("y Shandrina en el Lago", -.1),
         [("El experto es un libro: lo vende Wulan", .5)], "DESOLACE", "el libro de la Horda"),
    mapa("vallefresno", [(51.7, 73.4, "Lago Mystral", None, None), (49.4, 67.0, "Shandrina", "libro de cocina de experto (A)", "shandrina")],
         ("y Shandrina en el Lago", -.1), ("Y el artesano es una misión en Gadgetzan", -.1),
         [("y Shandrina en el Lago", .5), ("en Vallefresno, para la Alianza", 0)], "VALLEFRESNO", "el libro de la Alianza"),
] + filav("doce huevos gigantes, diez carnes", [("o_huevo_gigante", "12 huevos gigantes", None),
                                                ("o_carne_almeja", "10 carnes de almeja sabrosa", "diez carnes de almeja sabrosa"),
                                                ("o_queso_alterac", "20 quesos curados de Alterac", "y veinte quesos curados")], y=.62, tam=300, dur=4.2) + [
    pv(("Y el artesano es una misión en Gadgetzan", .2), "gadgetzan", "Gadgetzan · la misión de artesano", dur=3.8, x=.76, y=.40, tam=460),
    E.ficha_e("DEL 225 AL 300", ["inv_misc_fish_01", "inv_misc_fish_06", "inv_drink_17"], ("serviolas moteadas o branquirrojos", .2),
              ("pargo nocturno para terminar|fin", .6), ["serviolas moteadas o branquirrojos", "o branquirrojos, y la", "la sopa de pargo"],
              etiquetas=None),
    E.rotulo_e(("la comida cocinada da un", -.2), "Comida cocinada: +5 % de experiencia por muertes", sello="5", dur=4.0),
    E.peg_e(("la comida cocinada da un", -.4), "o_prof_cocina", "Comida cocinada · +5 %", dur=4.0, x=.76, y=.48),
    fav("inv_misc_food_15", "cocina · batidos de espíritu", 6, "Y hay seis recetas de", None),
    mapa("crestagrana", [(67.1, 69.9, "Descarrioaleta", "solo se pesca en Crestagrana", "o_whimsyfin")],
         ("Y la receta más rara", -.2), ("Y su descripción dice, literalmente", -.2),
         [("la descarrioaleta, que solo se", 0)], "MONTAÑAS CRESTAGRANA", "un pez nuevo"),
    tarj(("Y su descripción dice, literalmente", -.2), "o_delicia_whimsyfin", "Plato de descarrioaleta", "«Cómeme»", dur=4.0, x=.74, tam=420),
    pv(("La hoguera de oficial sale", -.2), "lord_serpentis", "Lord Serpentis · hoguera de oficial", dur=4.0, x=.76, y=.48, tam=520),
    tarj(("y el festín de Cocinitas", -.2), "cocinitas", "Cocinitas", "Las Minas de la Muerte · su festín", dur=4.8, x=.74),
    pv(("y el festín de Cocinitas", .3), "o_festin_cocinitas", "Festín de Cocinitas", dur=4.0, x=.20, y=.62),
    E.peg_e(("Y Cocinitas suelta también una", -.1), "o_varilla_cocinitas", "Varilla de remover · 25 % más rápido", dur=4.8, x=.24, y=.58),
    # =========================================================== P11 · PESCA (1580-1677 s)
    par(11, "PESCA", "o_prof_pesca", [(1, 75, "zonas iniciales"), (75, 150, "capitales y Baldíos")],
        "Parada número once, la pesca", ("Del uno al setenta y cinco, en", -.2), "no ocupa hueco · cofres en mar abierto", "la pesca, que no ocupa hueco"),
    pv(("con un adorno lustroso", -.3), "o_adorno_lustroso", "Adorno lustroso", dur=3.6, x=.17, y=.62),
    mapa("elwynn", [(52.4, 62.4, "Lago de Cristal", "pesca 1-75 · junto al agua", "o_cana_pescar")],
         ("Todos los entrenadores de inicio", -.2), ("Del setenta y cinco al ciento cincuenta, en las", -.1),
         [("Todos los entrenadores de inicio", .4)], "BOSQUE DE ELWYNN", "junto al agua"),
    E.peg_e(("en las capitales o en", -.2), "o_prof_pesca", "Pesca · del 75 al 150", dur=4.4, x=.20, y=.60),
    tar("Del setenta y cinco al ciento cincuenta, en las", "Pesca del 75 al 150", "trade_fishing",
        ["Las capitales", "Los Baldíos · Costa Oscura", dict(t="Loch Modan · Páramos de Poniente", c=V)], dur=7.0),
    mapa("tuercespina", [(27.4, 77.0, "Viejo Heming", "Bahía del Botín · libro de experto", "viejo_heming")],
         ("El experto es un libro que vende el Viejo", -.2), ("Con adornos brillantes, pescas", -.1),
         [("que vende el Viejo Heming", .3)], "VEGA DE TUERCESPINA", "el libro de experto"),
    pv(("Con adornos brillantes, pescas", -.1), "o_adornos_brillantes", "Adornos brillantes · Marjal Revolcafango", dur=4.2, x=.17, y=.62),
    mapa("marjal", [(58.4, 60.0, "Nat Pagle", "la misión de artesano", "nat_pagle")],
         ("El artesano es la misión de Nat", -.2), ("cuatro peces en cuatro costas", .4),
         [("la misión de Nat Pagle", .2)], "MARJAL REVOLCAFANGO", "la misión de Nat Pagle"),
    tar(("cuatro peces en cuatro costas", .3), "Nat Pagle: cuatro peces, cuatro costas", "trade_fishing",
        ["Tuercespina", "Desolace", "El Pantano de las Penas", dict(t="El Río Verdantis, en Feralas", c=V)], dur=6.6),
    pv(("cuatro peces en cuatro costas", .3), Fc("nat_pagle"), "Nat Pagle", dur=6.0, x=.20, y=.52, tam=440),
    tar("Y para cerrar, Frondavil, Feralas", "Pesca: hasta el 300", "trade_fishing",
        ["Frondavil · Feralas", "Tierras del Interior", dict(t="Tanaris · Un'Goro", c=V)], dur=6.4),
    tarj(("es una pecera", -.4), "o_cuenco_pescado", "Pecera", "+8 % a todas las estadísticas", dur=6.4, x=.74, tam=420),
    pv(("Al ciento cuarenta, un expositor de pesca", -.2), "o_expositor_pesca", "Expositor de pesca · señuelos", dur=4.4, x=.17, y=.62),
    mapa("vallefresno", [(16.5, 11.0, "Gelihast", "Cavernas de Brazanegra · expositor de pesca", "gelihast")],
         ("Su plano lo suelta Gelihast", -.2), ("Y al trescientos, una cabaña", -.1),
         [("Su plano lo suelta Gelihast", .4)], "VALLEFRESNO", "Cavernas de Brazanegra"),
    mapa("pantano", [(70.0, 52.9, "Profeta Jammal'an", "Templo Sumergido · cabaña de pesca", "jammalan")],
         ("Y al trescientos, una cabaña", -.1), ("Hay peces poco comunes y", -.1),
         [("que suelta el profeta Jammal'an", .1)], "PANTANO DE LAS PENAS", "el Templo Sumergido"),
    E.rotulo_e(("Hay peces poco comunes y", 0), "Peces poco comunes y raros nuevos", sello="!", dur=3.8),
    pv(("Y el concurso de pesca", .2), "o_cana_pescar", "Concurso de pesca · Tuercespina", dur=4.6, x=.17, y=.62),
    tar("Y el concurso de pesca", "Concurso de pesca de Tuercespina", "trade_fishing",
        ["Desde el 13 de noviembre", dict(t="Muchos más ganadores", c=V)], dur=5.6),
    mapa("azshara", [(58.3, 56.3, "Almejas de boca grande", "y langostas pinza oscura", "o_almeja_bocazas")],
         ("Y en la costa de Azshara", -.2), ("ahí está la siguiente parada|fin", .5),
         [("almejas de boca grande y", 0)], "AZSHARA", "más de 350 bancos"),
    pv(("langostas pinza oscura", -.2), "o_langosta_garraoscura", "Langostas pinza oscura", dur=4.2, x=.17, y=.64, tam=320),
    # =========================================================== P12 · PRIMEROS AUXILIOS (1678-1794 s)
    par(12, "PRIMEROS AUXILIOS", "o_prof_primeros_auxilios", [(1, 75, "lino o pociones menores"), (75, 150, "lana o cataplasma"),
                                                              (150, 225, "seda y tejido mágico"), (275, 300, "pociones sublimes")],
        "Parada número doce, los primeros", ("Porque aquí está la sorpresa", -.2), "la que más cambió en Forever", "y la que más cambió"),
    mg(P.traspaso("LA SORPRESA DE LA PARADA 5", F("o_pocion_sanacion"), (F("o_prof_alquimia"), "ALQUIMIA"),
                  (F("o_prof_primeros_auxilios"), "PRIMEROS AUXILIOS"), "esta la puede subir cualquier personaje"),
       ("Porque aquí está la sorpresa", -.2), ("la puede subir cualquier personaje|fin", .8),
       [("Porque aquí está la sorpresa", .3), "Ahora son de primeros auxilios", "y esa la puede subir"], "traspaso revelación", y=.50),
] + filav("dos caminos: vendas de lino", [("o_venda_lino", "Vendas de lino", ("vendas de lino, u ochenta", 0)),
                                          ("o_pocion_sanacion_menor", "86 pociones de sanación menores", "u ochenta y seis pociones"),
                                          ("o_flor_paz", "Flor de paz · especias · viales", "con flor de paz, especias")], y=.62, tam=300, dur=3.0, xs=(.16, .38, .60)) + [
    E.ficha_e("DEL 75 AL 150", ["inv_misc_bandage_14", "o_cataplasma_simple", "o_pocion_sanacion"], ("Del setenta y cinco al ciento cincuenta, vendas", .9),
              ("treinta y una pociones de sanación|fin", .6), ["vendas de lana, o un", "la cataplasma simple, y", "treinta y una pociones de"],
              etiquetas=["lana", "cataplasma", "×31"]),
    mapa("arathi", [(27.0, 58.8, "Deneb Camino", "libro de experto (A)", "deneb")],
         ("El experto es un libro: lo vende Deneb", -.2), ("y Balai Lok'Wein en el", -.1),
         [("lo vende Deneb Camino en", .3)], "TIERRAS ALTAS DE ARATHI", "el libro de la Alianza"),
    mapa("marjal", [(36.4, 30.4, "Balai Lok'Wein", "libro de experto (H)", "balai")],
         ("y Balai Lok'Wein en el", -.1), ("Del ciento cincuenta al doscientos veinticinco, vendas", 1.0),
         [("y Balai Lok'Wein en el", .3)], "MARJAL REVOLCAFANGO", "el libro de la Horda"),
    tar(("Del ciento cincuenta al doscientos veinticinco, vendas", .9), "Del 150 al 225", "inv_misc_bandage_01",
        ["Vendas de seda", dict(t="Vendas de tejido mágico", c=V)], calidad="blanco", dur=4.0),
    mapa("mundo", [(79.7, 43.2, "Doctor Gregory Victor", "Sentencia, Arathi (H)", "gregory_victor"),
                   (33.5, 62.1, "Doctor Gustaf VanHowzen", "Theramore (A)", "vanhowzen")],
         ("Y el artesano es la misión de atenciones", -.2), ("Salvas a quince heridos", -.1),
         [("el doctor Gregory Victor en", .2), ("o el doctor Gustaf VanHowzen", .3)], "AZEROTH", "Atenciones médicas", zmax=1.2),
    mg(M.contadores("ATENCIONES MÉDICAS", [("spell_holy_sealofsacrifice", "heridos salvados", 15, 0, 1)], ("¡ENTRÉGALA EN CUANTO LLEGUES!", 2)),
       ("Salvas a quince heridos", -.1), ("No te quedes a ver qué pasa|fin", .5),
       ["Salvas a quince heridos", "los críticos primero", "y la entregas en cuanto"], "15 heridos", y=.52),
    E.rotulo_e(("Luego, vendas de tejido mágico", -.1), "Luego, vendas de tejido mágico y de paño rúnico", sello="!", dur=3.8),
    tarj(("pociones de sanación sublimes. El", -.6), "o_pocion_sanacion_sublime", "Poción de sanación sublime", "la alternativa nueva · 275-300",
                dur=3.2, x=.74, tam=420),
    mapa("hyjal", [(48.2, 33.6, "Pexmit", "el manual · 8 de oro", "pexmit"), (13.0, 52.8, "Ortak Lomgok", "Flora Antigua · misión (H)", "ortak")],
         ("El manual lo vende Pexmit", -.2), ("Además hay curativos nuevos", -.1),
         [("El manual lo vende Pexmit", .4), ("una misión de Ortak Lomgok", .2)], "MONTE HYJAL", "el manual de las pociones sublimes"),
    tarj(("un torniquete de lana para", -.3), "o_torniquete_lana", "Torniquete de lana", "contra los sangrados", dur=4.8, x=.74, tam=420),
    E.ficha_e("CAMPAMENTO DEL SANADOR", ["o_equipo_primeros_auxilios", "o_estudio_toxinas", "o_laboratorio_peste"], ("En el campamento, el sanador", -.2),
              ("médico de la peste|fin", .6), ["equipo de primeros auxilios que", "Luego un estudio de toxinas", "el laboratorio de médico de"],
              etiquetas=["aguante", "toxinas", "peste"]),
    E.peg_e(("Piénsalo así: la profesión", -.1), "o_prof_primeros_auxilios", "Primeros auxilios · no ocupa hueco", dur=4.6, x=.24, y=.58),
    pv(("ahora fabrica pociones de sanación sublimes", -.4), "o_pocion_sanacion_sublime", "Poción de sanación sublime", dur=3.4, x=.76, y=.50, tam=340),
    pv(("Si tu personaje no tiene", -.1), "o_pocion_sanacion", "Tus pociones, para la banda", dur=5.6, x=.76, y=.50, tam=340),
    # =========================================================== COMBOS (1795-1843 s)
    carr([("o_prof_mineria", "Minería"), ("o_prof_herboristeria", "Herboristería"), ("o_prof_desuello", "Desuello"),
          ("o_prof_sastreria", "Sastrería"), ("o_prof_cocina", "Las secundarias")],
         ("Y antes de despedirnos", -.2), ("parejas que tienen sentido en Forever|fin", .4),
         [("la pregunta de siempre", .2), ("qué dos profesiones llevo", .2), ("No hay una respuesta única", .2), "pero sí parejas",
          ("pero sí parejas", 1.2)], "¿QUÉ DOS PROFESIONES LLEVO?"),
    mg(P.flujo("MINERÍA + HERRERÍA O INGENIERÍA", [(0, 0, F("o_prof_mineria"), "Minería"), (1, 0, F("o_barra_torio"), "Barras de torio"),
                                                   (2, 0, F("o_prof_herreria"), "Herrería"), (2, 1, F("o_prof_ingenieria"), "Ingeniería")],
               [(0, 1), (1, 2), (1, 3)], None, ancho=1400),
       ("Minería con herrería o con", -.2), ("salen de la minería|fin", .5),
       ["Minería con herrería o con", "cientos de barras de torio", ("Minería con herrería o con", .7), ("Minería con herrería o con", 1.4)],
       "combo minería", y=.50),
    E.ficha_e("HERBORISTERÍA + ALQUIMIA", ["o_prof_herboristeria", "o_prof_alquimia"], ("Herboristería con alquimia, porque", -.2),
              ("a sastres y peleteros|fin", .4), [("Herboristería con alquimia, porque", .1), ("Herboristería con alquimia, porque", .7)],
              etiquetas=["~1000 hierbas", "tintes"]),
    E.ficha_e("DESUELLO + PELETERÍA", ["o_prof_desuello", "o_prof_peleteria", "o_tienda_campamento"], ("Desuello con peletería, por", -.2),
              ("da descanso a todo el campamento|fin", .4), [("Desuello con peletería, por", .1), ("Desuello con peletería, por", .7), "por esa tienda que da"],
              etiquetas=["desuello", "peletería", "tienda"]),
    E.ficha_e("SASTRERÍA + ENCANTAMIENTO", ["o_prof_sastreria", "o_prof_encantamiento", "o_bolsa_componentes_lino"], ("Sastrería con encantamiento, porque", -.2),
              ("Y las tres secundarias, para", -.4), [("Sastrería con encantamiento, porque", .1), ("Sastrería con encantamiento, porque", .7),
                                                          "te hace las bolsas de"], etiquetas=["coses", "desencantas", "bolsas"]),
    E.ficha_e("LAS TRES SECUNDARIAS, PARA TODOS", ["o_prof_cocina", "o_prof_pesca", "o_prof_primeros_auxilios"], ("Y las tres secundarias, para", -.2),
              ("y otra ya hace tus pociones|fin", .6), [("Y las tres secundarias, para", .3), "una enciende el campamento", "y otra ya hace tus pociones"],
              etiquetas=["enciende", "pesca", "tus pociones"]),
    # =========================================================== CIERRE (1845-1876 s)
    E.rotulo_e(("Y esa es la ruta de profesiones", 0), "La ruta de profesiones, del 1 al 300", sello="12", dur=4.6),
    pv(("de la mena que no se funde", -.2), "o_mena_torio_pesada", "La mena que no se funde", dur=4.2, x=.20, y=.60),
    pv(("a la poción que ya no es", -.2), "o_pocion_sanacion_sublime", "La poción que ya no es del alquimista", dur=4.0, x=.76, y=.50, tam=340),
    E.rotulo_e(("Ahora cuéntame en los comentarios", 0), "¿Qué dos profesiones llevas?", sello="?", dur=4.6),
    E.peg_e(("Y si tu hermandad no", -.2), "o_prof_encantamiento", "¿Tu hermandad no tiene encantador?", dur=4.6, x=.76, y=.50),
    E.rotulo_e(("Nos vemos en la próxima crónica", 0), "Nos vemos en Azeroth", sello="!", dur=3.6),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]
_TAR = [d for d in FX if "tarjeta" in d and "tipo" not in d]      # las fichas de interfaz (tar) van a APOYOS
FX = [d for d in FX if not ("tarjeta" in d and "tipo" not in d)]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos); colores de la paleta (amarillo/rojo)
    dict(texto="NO ES LA QUE IMAGINAS", en="Te adelanto que no es", dur=3.0, tam=110, color="rojo", y=.16),
    dict(texto="NO SE FUNDE", en="que no se puede fundir en", dur=3.0, tam=130, color="rojo", y=.16),
    dict(texto="SIN JOYERÍA NI INSCRIPCIÓN", en="y no hay joyería ni", dur=3.0, tam=96, color="rojo", y=.90),
    dict(texto="NO SE PUEDEN OLVIDAR", en="y esas no se pueden olvidar", dur=3.0, tam=110, color="amarillo", y=.14),
    dict(texto="SIN BONUS PASIVO", en="Y ninguna profesión da un", dur=3.0, tam=130, color="rojo", y=.16),
    dict(texto="SACARLE MÁS EN COMBATE", en="cómo sacarle más a tu", dur=3.0, tam=110, color="amarillo", y=.16),
    dict(texto="LAS GUÍAS NO SIEMPRE VAN AL DÍA", en="Porque las guías no siempre", dur=3.0, tam=80, color="rojo", y=.16),
    dict(texto="9 DE DICIEMBRE", en="Y para las bandas del nueve", dur=3.0, tam=130, color="amarillo", y=.86),
    dict(texto="EL GOLPE", en="Y aquí viene el golpe", dur=2.4 + .6, tam=150, color="rojo", y=.14),
    dict(texto="SE ACUMULAN", en="ya se acumulan con los", dur=3.0, tam=130, color="amarillo", y=.16),
    dict(texto="GRACIAS, JULSIKAKKU", en="Gracias por enseñarnos que la", dur=3.0, tam=110, color="amarillo", y=.86),
    dict(texto="SIN 15 PUNTOS GRATIS", en="el gnomo ya no recibe sus", dur=3.0, tam=110, color="rojo", y=.14),
    dict(texto="BUENAS NOTICIAS", en="Pues hoy, Goca, tengo buenas", dur=3.0, tam=130, color="amarillo", y=.16),
    dict(texto="MISMO PESO", en="pesa exactamente lo mismo que", dur=3.0, tam=150, color="amarillo", y=.86),
    dict(texto="GRACIAS", en="Y gracias a quienes nos", dur=3.0, tam=160, color="amarillo", y=.80),
    dict(texto="SEMILLAS", en="Y algo que nunca habíamos tenido", dur=3.0, tam=150, color="amarillo", y=.16),
    dict(texto="EL CAMBIO MÁS GRANDE", en="Ahora viene el cambio de", dur=3.0, tam=120, color="rojo", y=.16),
    dict(texto="HOY VA A SER PEOR", en="y te aviso que hoy", dur=3.0, tam=130, color="rojo", y=.16),
    dict(texto="UNA SOLA VEZ", en="cada criatura se desuella una", dur=3.0, tam=140, color="rojo", y=.16),
    dict(texto="+3", en="que suma tres puntos", dur=3.0, tam=170, color="amarillo", y=.16),
    dict(texto="SIN RESISTENCIAS", en="Y las especializaciones ya no dan", dur=3.0, tam=130, color="rojo", y=.16),
    dict(texto="LA JOYA", en="Y aquí está la joya", dur=3.0, tam=160, color="amarillo", y=.16),
    dict(texto="SOLO CON 300", en="solo se coloca con trescientos", dur=3.0, tam=150, color="rojo", y=.16),
    dict(texto="DESENCANTAR TAMBIÉN DA PUNTOS", en="Y desencantar también da puntos", dur=3.0, tam=84, color="amarillo", y=.16),
    dict(texto="18 PUNTOS", en="Son dieciocho puntos en total", dur=3.0, tam=110, color="amarillo", y=.12),
    dict(texto="NIVEL EMBAJADOR", en="eso ya es nivel de embajador", dur=3.0, tam=130, color="amarillo", y=.16),
    dict(texto="SALUDOS", en="El saludo, te lo devolvemos", dur=3.0, tam=160, color="amarillo", y=.16),
    dict(texto="1 MINUTO = 1 HORA", en="Te sientas un minuto y", dur=3.4, tam=110, color="amarillo", y=.12),
    dict(texto="«CÓMEME»", en="literalmente, cómeme", dur=3.0, tam=150, color="amarillo", y=.16),
    dict(texto="+25 % MÁS RÁPIDO", en="cocinar un veinticinco por ciento", dur=3.0, tam=120, color="amarillo", y=.16),
    dict(texto="MÁS GANADORES", en="tiene muchos más ganadores", dur=3.0, tam=130, color="amarillo", y=.16),
    dict(texto="NO TE QUEDES", en="No te quedes a ver", dur=3.0, tam=150, color="rojo", y=.16),
    dict(texto="SIN EXCUSA", en="ya no tiene excusa", dur=3.0, tam=150, color="rojo", y=.16),
    dict(texto="NO OCUPA HUECO", en="la profesión que no ocupa hueco", dur=3.0, tam=130, color="amarillo", y=.16),
    dict(texto="SUSCRÍBETE", en="Si este video te sirvió", dur=3.0, tam=150, color="amarillo", y=.16),
]
SFX = {}
PISTAS = []

APOYOS = [
    tar(("Las profesiones tienen ventana propia", -.1), "Ventana de profesiones", "inv_misc_book_09",
        ["Tecla K", "Buscador y filtros", dict(t="Botón «Crear todo»", c=V)], dur=5.0),
    tar("Una rama de talentos escrita", "Rama de talentos de una guía", "inv_misc_book_09",
        ["Escrita antes del último ajuste", dict(t="Puede estar desfasada", c=RJ), dict(t="El coach mira la versión de hoy", c=V)], dur=5.6),
] + _TAR
