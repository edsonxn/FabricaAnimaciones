# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 15 enemigos ocultos de Fallout» (SECUENCIA YT, Radio Yermo, 3.er video, 23-nov-2026).
REGLA DE ORO (tes_secretos_40) con la receta de Tamriel: kit Pip-Boy `nucleo/mg_fo.py` (puesto, ficha, objetivo, vats, enemigo,
botin, aviso, contador, radio, terminal), pegatinas `pv()` con el rotador + peg_estilos (tema "fo"), muro del cierre y MAPAS REALES
del juego de cada puesto (coords = marcadores del mapa interactivo de la wiki, `mapas/_coords.json`, hoja `previews/_coords_check.jpg`).
Datos: `_investigacion_A.md` / `_B.md`. Copiado de `videos/fo_nunca_f4/efectos.py` y `videos/fo_refugios_25/efectos.py`.
    python fab.py fo_enemigos_ocultos fx --seco      FAB_FX_FINAL=1 python fab.py fo_enemigos_ocultos fx hoja
"""
import json
import os

import mg_fo as F
import peg_estilos as PE

CAMARA = {}
FUNDIDO = {}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_PEG = "fo"
TEMA_MAPA = "fo"
_FX, _FY = .76, .30
C = {j: {k: tuple(v["xy"]) for k, v in d.items()}
     for j, d in json.load(open(os.path.join(_MAP, "_coords.json"), encoding="utf-8")).items()}


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.18, y=.60, tam=380, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6, xs=(.14, .32, .50, .68, .86)):
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return dict(tipo="mg", fn=PR.muro([(P(s), n) for s, n in fotos], tema=TEMA_PEG, destaca=destaca, titulo=titulo), de=de, a=a,
                marcas=list(marcas), x=.5, y=.5, sale=.06, nombre="muro", ver=4.0)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco, tema=TEMA_PEG), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def mg(fn, de, a, marcas, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def pu(en, n, titulo, sub, y=.26):
    """Entrada de cada puesto (DATOS > MISIONES del Pip-Boy)."""
    return mg_en(F.puesto(n, titulo, sub, cab="ENEMIGO OCULTO"), en, 3.8, f"puesto {n}", y=y)


def fi(en, nombre, filas, texto=None, cab=None, dur=4.4, x=_FX, y=_FY):
    return mg_en(F.ficha(nombre, filas, texto, cab), en, dur, "ficha " + nombre, x=x, y=y)


def ob(en, texto, sub=None, hecho=False, dur=3.6, x=.30, y=.20, marca=1.4):
    fn = F.objetivo(texto, sub, hecho=hecho)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG objetivo " + texto, ver=1.0,
                **({"marcas": [(en, marca)]} if hecho else {}))


def av(en, texto, sub=None, icono=None, dur=3.2, x=.30, y=.13):
    return mg_en(F.aviso(texto, sub, icono=icono), en, dur, "aviso " + texto, x=x, y=y)


def cont(en, valor, unidad, titulo, desde=0, dur=3.4, x=.76, y=.30):
    return mg_en(F.contador(valor, unidad, titulo, desde=desde), en, dur, "contador " + titulo, x=x, y=y)


def ene(en, nombre, vida=1.0, a=None, sub=None, dur=4.0, y=.22):
    return mg_en(F.enemigo(nombre, vida, a, sub), en, dur, "enemigo " + nombre, y=y)


def _recorta(puntos, lado):
    xs, ys = [p[0] for p in puntos], [p[1] for p in puntos]
    L = max(lado, max(xs) - min(xs) + .14, max(ys) - min(ys) + .14)
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    x0, y0 = min(max(0.0, cx - L / 2), 1 - L), min(max(0.0, cy - L / 2), 1 - L)
    nue = [((p[0] - x0) / L, (p[1] - y0) / L) + tuple(p[2:]) for p in puntos]
    return (x0, y0, x0 + L, y0 + L), nue


def _recorte_disco(juego, rec):
    from PIL import Image
    d = os.path.join(_MAP, "_cache"); os.makedirs(d, exist_ok=True)
    f = os.path.join(d, f"{juego}_{'_'.join(f'{v:.4f}' for v in rec)}.png")
    if not os.path.exists(f):
        im = Image.open(os.path.join(_MAP, juego + ".png")).convert("RGB")
        W, H = im.size
        im = im.crop((int(rec[0] * W), int(rec[1] * H), int(rec[2] * W), int(rec[3] * H)))
        im.thumbnail((1600, 1600)); im.save(f)
    return f


def mapa(juego, titulo, puntos, de, a, marcas, sub, x=.70, y=.45, lado=.34, ancho=860, **kw):
    """Mapa REAL del juego en ventana, con el lugar marcado (y su foto)."""
    import mg_mapa as MP
    rec, puntos = _recorta(puntos, lado)
    fn = MP.mapa(_recorte_disco(juego, rec), puntos, TEMA_MAPA, titulo=titulo, sub=sub, recorte=None, modo="ventana",
                 ancho=ancho, **kw)
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)


def pt(juego, slug, nombre, tipo="meta", foto=None):
    x, y = C[juego][slug]
    return (x, y, nombre, tipo) + ((P(foto),) if foto else ())


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_AQUI, "pantallas", slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


FX = [
    # ================= GANCHO: un elemento por frase
    mg(F.radio(["Radio Yermo"], 0, "Transmitiendo desde una cueva que no sale en el mapa"), "Buenos días, Yermo",
       ("que no sale en el mapa|fin", .2), [], "radio saludo", y=.46),
    mg_en(F.terminal(["> CARGAR LISTA", "Los 15 enemigos *ocultos*", "Fallout 3 · New Vegas · Fallout 4"]), "Hoy, los quince enemigos",
          5.4, "terminal título", y=.80),
    pv("Una osa de circo", "e12_poster", "Ruzka, la osa maravilla", dur=3.2, x=.18, y=.60, tam=360),
    pv("Un perro gigante", "e8_gabe", "Gabe", dur=3.2, x=.80, y=.60, tam=360),
    pv("Un monstruo marino legendario", "e13_red", "Red Death", dur=3.4, x=.20, y=.60, tam=360),
    pv("Y un alienígena herido", "e7_alien", "El alienígena", dur=3.4, x=.80, y=.60, tam=360),
    ob("Todo comprobado en el juego", "Todo comprobado en el juego", hecho=True, dur=3.0),
    rel("y resulta que es una mosca", "e1_tamano", "El n.º 1", "Es una mosca", dur=4.0, x=.76, y=.52, tam=480),

    # ================= 15 · EL QUINTETO DE LA REINA (FO3)
    pu("Número quince", 15, "El Quinteto de la Reina", "Fallout 3 · bajo la estación Marigold"),
    mapa("yermo_capital", "Yermo Capital", [pt("yermo_capital", "marigold", "Estación Marigold", "poder", "e15_marigold")],
         "Bajo la estación de metro Marigold", ("fueran más pequeñas|fin", .2), ["Bajo la estación de metro Marigold"],
         "Estación Marigold", entrada="foco"),
    cam("un científico, el doctor Lesko", "e15_lesko", "Doctor Lesko", dur=3.6, x=.16, y=.64, tam=300),
    av("Le salió al revés", "Experimento fallido", "Mutágeno en la reina", dur=3.0),
    pv("escupiendo fuego", "e15_guardian", "Guardián del hormiguero", dur=3.8, x=.80, y=.60, tam=380),
    cont("Solo existen esos cinco", 5, "guardianes", "EN TODO EL JUEGO", dur=3.4),
    fi("Cada uno con doscientos veinticinco", "Guardián del hormiguero", [("PS", "225"), ("Resist. al fuego", "85 %")],
       "Solo *cinco* en todo el juego", "CRIATURA", dur=5.4),
    rel("Detrás está la reina de Marigold", "e15_reina", "Reina de Marigold", "1 000 PS", dur=4.6, x=.76, y=.52, tam=500),
    av("Ella no escupe fuego", "No escupe fuego", "Solo afectó a sus huevos", dur=3.4, y=.86),

    # ================= 14 · CAZADOR LEGENDARIO (FNV)
    pu("Número catorce", 14, "El cazador legendario", "New Vegas · mina de Silver Peak"),
    mapa("mojave", "Mojave", [pt("mojave", "jacobstown", "Jacobstown", "inicio"),
                              pt("mojave", "silver_peak", "Mina de Silver Peak", "peligro", "e14_exterior")],
         "En la mina de Silver Peak", ("Ya eso es mala idea|fin", .2), ["En la mina de Silver Peak", "en el camino a Jacobstown"],
         "Silver Peak", entrada="foco"),
    pv("sale el único cazador legendario", "e14_cazador_rec", "Cazador legendario", dur=4.0, x=.80, y=.58, tam=400),
    fi("Nivel veinticinco", "Cazador legendario", [("Nivel", "25"), ("PS", "400 (×2)"), ("Veneno", "8 /s · 30 s")],
       "El *único* de su especie", "CRIATURA", dur=6.0),
    cont("durante treinta segundos", 240, "PS", "VENENO EN TOTAL", dur=3.2, x=.30, y=.30),
    av("murió un soldado del Enclave", "Soldado del Enclave", "Huyó de Navarro", dur=3.6),
    ob("Por un cazador, o por el cazador", "Sobrevive a la mina", "Silver Peak", dur=3.6),

    # ================= 13 · RED DEATH (FO4 Far Harbor)
    pu("Número trece", 13, "El Red Death", "Far Harbor · isla sin marcador"),
    av("Los pescadores de Far Harbor", "Leyenda de Far Harbor", "Un monstruo hunde barcos", dur=3.6),
    ob("Solo lo ves si haces la gran cacería", "La gran cacería", "Con una vieja capitana", dur=4.4),
    pv("Llegas a una isla sin marcador", "e13_isla", "Isla sin marcador", dur=3.8, x=.80, y=.58, tam=400),
    pant("e13_red", "Y ahí está", ("con los ojos rojos brillantes|fin", .3), zoom=(1.0, 1.25)),
    av("Ni siquiera es hostil", "No es hostil", "Más pequeño que una tochomosca", dur=3.4, y=.86),
    ene("Sus ojos brillan a través", "Red Death", 1.0, sub="Hombre pinza · nivel 1", dur=4.4),
    ob("Igual tienes que matarlo", "Mata al Red Death", "La gran cacería", hecho=True, dur=3.6, marca=1.2),

    # ================= 12 · RUZKA (FO3 Point Lookout)
    pu("Número doce", 12, "Ruzka, la osa maravilla", "Point Lookout · guarida sin marcador"),
    mapa("punto_lookout", "Point Lookout", [pt("punto_lookout", "jet", "Avión estrellado", "inicio"),
                                             pt("punto_lookout", "ruzka", "Guarida de Ruzka", "peligro", "e12_ruzka")],
         "En el rincón noroeste de Point Lookout", ("de toda la expansión|fin", .2), ["En el rincón noroeste", "vive el único yao guai"],
         "Guarida de Ruzka", lado=.40, entrada="foco"),
    rel("era Ruzka, la osa maravilla", "e12_poster", "Ruzka", "La osa maravilla", dur=5.0, x=.76, y=.52, tam=480),
    fi("veinte por ciento más grande", "Ruzka", [("Nivel", "7"), ("PS", "220"), ("Tamaño", "+20 %")], "El *único* yao guai del DLC",
       "CRIATURA", dur=5.0),
    pv("jugando con una enorme pelota roja", "e12_ruzka", "Su pelota roja", dur=3.8, x=.20, y=.60, tam=380),
    av("la ventaja de amigo de los animales", "Amigo de los animales", "Sin esta ventaja, es hostil", dur=3.6),

    # ================= 11 · STRIPE (FNV OWB)
    pu("Número once", 11, "Stripe", "Old World Blues · solo con Wild Wasteland"),
    av("Solo aparece si elegiste el rasgo", "Rasgo: Wild Wasteland", "Requisito", icono="ok", dur=3.2),
    mapa("big_mt", "Big MT", [pt("big_mt", "higgs", "Higgs Village", "peligro", "e11_higgs")], "En Higgs Village",
         ("una pata de pollo delante|fin", .2), ["En Higgs Village"], "Higgs Village", entrada="foco"),
    pant("e11_stripe", "Te acercas, y sale", ("al tamaño de un perro|fin", .4), zoom=(1.0, 1.18)),
    fi("Pequeño, sí", "Stripe", [("Nivel", "30"), ("PS", "850"), ("Daño", "250")], "Un sanguinario *alfa* de bolsillo", "CRIATURA",
       dur=5.4),
    av("Es un homenaje a Stripe", "Homenaje", "El líder de los Gremlins", dur=3.6, y=.86),
    ob("No lo mojes", "No lo mojes", "Ni le des de comer de noche", dur=4.0),

    # ================= 10 · REINA NUKALURK (FO4 Nuka-World)
    pu("Número diez", 10, "La reina Nukalurk", "Nuka-World · el estanque de la planta"),
    pv("Detrás de la planta embotelladora", "e10_planta", "Planta embotelladora", dur=3.8, x=.80, y=.58, tam=400),
    pant("e10_noche", "Y en ese estanque", ("azul y brillante|fin", .3), zoom=(1.0, 1.15)),
    av("Brilla por el estroncio", "Estroncio", "El isótopo de la Nuka-Cola Quantum", dur=3.8),
    fi("Nivel sesenta y cuatro", "Reina Nukalurk", [("Nivel", "64"), ("PS", "1 500"), ("Radiación / veneno", "Inmune")],
       "*Única* en todo el juego", "CRIATURA", dur=6.0),
    mg_en(F.botin("Reina Nukalurk", ["Carne de reina Nukalurk ×5"]), "suelta cinco piezas de carne", 4.0, "botín reina", x=.72, y=.50),

    # ================= 9 · MADRE CURIE III (FO3 Broken Steel)
    pu("Número nueve", 9, "Madre Curie III", "Fallout 3 · Broken Steel"),
    cam("la Madre Curie predica", "e9_humana_rec", "Madre Curie", dur=4.4, x=.16, y=.64, tam=320),
    ob("si empiezas su misión", "Empieza su misión", hecho=True, dur=3.0, marca=.8),
    mapa("yermo_capital", "Yermo Capital", [pt("yermo_capital", "megaton", "Megatón", "peligro", "e9_megaton")],
         "haces estallar la bomba de Megatón", ("ella estaba predicando allí|fin", .4), ["haces estallar la bomba"], "Megatón",
         entrada="foco"),
    pant("e9_bomba", "Y vuelve", ("de la peor clase|fin", .2), zoom=(1.0, 1.12)),
    rel("mil cien puntos de vida", "e9_necrofaga", "Madre Curie III", "Necrófaga salvaje", dur=5.6, x=.76, y=.52, tam=500),
    cont("mil cien puntos de vida", 1100, "PS", "LA NUEVA MADRE CURIE", dur=3.6, x=.30, y=.30),
    av("El hermano Gerard también", "Hermano Gerard", "También se transforma", dur=3.2, y=.86),

    # ================= 8 · GABE (FNV OWB)
    pu("Número ocho", 8, "Gabe", "Old World Blues · el ciberperro gigante"),
    mapa("big_mt", "Big MT", [pt("big_mt", "x8", "Centro de investigación X-8", "peligro", "e8_guarida")],
         "En la instalación de pruebas del X-ocho", ("Un ciberperro|fin", .3), ["En la instalación de pruebas"], "X-8", entrada="foco"),
    cam("el doctor Borous", "e8_borous", "Doctor Borous", dur=3.4, x=.16, y=.64, tam=300),
    fi("Nivel treinta y cinco", "Gabe", [("Nivel", "35"), ("PS", "375"), ("Arma", "Ladrido sónico")], "Percepción: *0*", "CRIATURA",
       dur=6.0),
    ob("Puedes pasar a su lado en sigilo", "Pasa a su lado en sigilo", "Percepción 0", hecho=True, dur=3.6, marca=1.2),
    mg_en(F.contador(0, "", "DETONACIÓN EN", desde=5), "con una cuenta atrás", 3.6, "cuenta atrás Gabe", x=.76, y=.30),
    rel("Gabe se llama así", "e8_gabe", "Gabe", "Por el perro de una diseñadora", dur=6.0, x=.76, y=.52, tam=480),

    # ================= 7 · EL ALIENÍGENA (FO4)
    pu("Número siete", 7, "El alienígena del OVNI", "Fallout 4 · cueva sin marcar"),
    pant("e7_cayendo", "a veces ves pasar algo", ("entre los árboles|fin", .3), zoom=(1.0, 1.2)),
    mapa("commonwealth", "Commonwealth", [pt("commonwealth", "oberland", "Estación Oberland · el OVNI cae al este", "peligro", "e7_ovni")],
         "Al este de la estación Oberland", ("baja a una cueva sin marcar|fin", .2), ["Al este de la estación Oberland"], "Oberland",
         entrada="foco"),
    ene("Ahí dentro está el único alienígena", "Alienígena", .7, sub="Pierna lisiada · 50 PS", dur=4.4),
    rel("Lo matas, y la pistola alienígena", "e7_blaster_rec", "Pistola blaster alienígena", "Y cientos de balas", dur=5.0, x=.76,
        y=.52, tam=480),
    av("Cruzó la galaxia", "Ubicación descubierta", "Boston", dur=3.4, y=.86),

    # ================= 6 · SANGUINARIO LEGENDARIO (FNV)
    pu("Número seis", 6, "El sanguinario legendario", "New Vegas · caverna Dead Wind"),
    mapa("mojave", "Mojave", [pt("mojave", "repconn", "Centro de pruebas de REPCONN", "inicio"),
                              pt("mojave", "dead_wind", "Caverna Dead Wind", "peligro", "e6_cueva")],
         "La caverna Dead Wind", ("está llena de sanguinarios|fin", .3), ["La caverna Dead Wind", "al sur del centro de pruebas"],
         "Dead Wind", entrada="foco"),
    av("El único de la cueva que no vuelve", "No reaparece", "El único de la cueva", dur=3.4),
    fi("Nivel treinta, mil puntos", "Sanguinario legendario", [("Nivel", "30"), ("PS", "1 000"), ("Daño", "250 (×2)")],
       "Escoltado por *dos*", "CRIATURA", dur=6.0),
    mg_en(F.botin("Soldado de la Hermandad", ["Mercy"]), "A su lado hay un soldado", 5.4, "botín Mercy", x=.72, y=.50),

    # ================= 5 · MUTASCORPIO ALBINO (FO3 Broken Steel)
    pu("Número cinco", 5, "El mutascorpio albino", "Fallout 3 · Broken Steel"),
    mapa("yermo_capital", "Yermo Capital", [pt("yermo_capital", "reguladores", "Cuartel de los Reguladores", "peligro", "e5_reguladores")],
         "como la granja junto al cuartel", ("de los Reguladores|fin", .6), ["como la granja"], "Reguladores", entrada="foco"),
    pv("Mil quinientos puntos de vida#2", "e5_albino", "Mutascorpio albino", dur=4.0, x=.20, y=.60, tam=400),
    cont("Mil quinientos puntos de vida#2", 1500, "PS", "MUTASCORPIO ALBINO", dur=3.4),
    cam("y el general Jingwei", "e5_jingwei_rec", "General Jingwei", dur=3.4, x=.80, y=.64, tam=300),
    fi("Pega cien por pinchazo", "Mutascorpio albino", [("Daño", "100"), ("Veneno", "25 /s · 4 s"), ("Velocidad", "Más rápido")],
       None, "CRIATURA", dur=5.4),
    av("se cura poco a poco con la luz del sol", "Se cura al sol", "Y es albino", dur=3.8, y=.86),

    # ================= PAUSA · SUSCRIPCIÓN (sin cifra)
    mg(F.radio(["Radio Yermo"], 0, "Cada suscripción, un watt más de señal"), "Una pausa en la transmisión",
       ("un watt más de señal en el Yermo|fin", .3), [], "radio suscripción", y=.46),
    ob("suscríbete y activa la campana", "Suscríbete y activa la campana", "Radio Yermo", hecho=True, dur=5.0, marca=2.0),

    # ================= 4 · CAMALEÓN Y MÍTICO (FO4)
    pu("Número cuatro", 4, "Los sanguinarios camaleón y mítico", "Fallout 4 · solo a nivel altísimo"),
    av("solo aparecen cuando tu personaje", "Nivel requerido", "81 · 91", dur=3.6),
    pant("e4_camaleon", "El sanguinario camaleón sale", ("se queda con el último|fin", .3), zoom=(1.0, 1.15)),
    rel("El mítico, a partir del nivel", "e4_mitico", "Sanguinario mítico", "Nivel 91", dur=5.0, x=.76, y=.52, tam=500),
    fi("Mil trescientos sesenta puntos", "Sanguinario mítico", [("PS", "1 360+"), ("Golpe fuerte", "350")],
       "Los no legendarios más *fuertes*", "CRIATURA", x=.28, dur=5.4),
    mg_en(F.botin("Sanguinario mítico", ["Mano de sanguinario", "Cigarrillo", "Carne de sanguinario"], elegido=1),
          "entre su botín hay un cigarrillo", 4.4, "botín cigarrillo", x=.72, y=.50),

    # ================= 3 · RAWR (FNV Lonesome Road)
    pu("Número tres", 3, "Rawr", "Lonesome Road · la Divisoria"),
    mapa("divisoria", "La Divisoria", [pt("divisoria", "boxwood", "Azotea del hotel Boxwood", "peligro", "e3_azotea")],
         "En la Divisoria, pasando la azotea", ("te quedas encerrado con él|fin", .2), ["En la Divisoria"], "Boxwood", entrada="foco"),
    pant("e3_rawr", "Rawr es un sanguinario único", ("No se le puede derribar|fin", .3), zoom=(1.0, 1.15)),
    fi("Nivel cuarenta y cinco", "Rawr", [("Nivel", "45"), ("PS", "900"), ("Daño", "350")], "No se le puede *derribar*", "CRIATURA",
       dur=5.0),
    mg_en(F.special([10, 10, 10, 7, 5, 10, 10]), "Y sus atributos rozan el máximo", 5.6, "special Rawr", x=.30, y=.48),
    rel("Rawr huye de las bengalas", "e3_bengala_rec", "Pistola de bengalas", "Lo único que lo espanta", dur=4.4, x=.76, y=.52, tam=440),

    # ================= 2 · HUNDEBARCOS (FO4 Far Harbor)
    pu("Número dos", 2, "Hundebarcos", "Far Harbor · una señal de radio"),
    mg(F.radio(["Frecuencia de Hundebarcos"], 0, "Una señal que interfiere con las demás"), "a veces tu Pip-Boy capta",
       ("Es ella|fin", .3), [], "radio Hundebarcos", y=.46),
    pv("Un reptador de la Niebla legendario", "e2_hundebarcos", "Hundebarcos", dur=4.2, x=.80, y=.58, tam=420),
    cam("El Viejo Longfellow lleva años", "e2_longfellow_rec", "El Viejo Longfellow", dur=3.6, x=.16, y=.64, tam=300),
    fi("Tiene como mínimo dos mil doscientos", "Hundebarcos", [("Nivel", "75+"), ("PS", "2 200+"), ("Resist. física", "4 000")],
       None, "CRIATURA", dur=5.4),
    cont("Cuatro mil#3", 4000, "", "RESISTENCIA FÍSICA", dur=3.0, x=.30, y=.30),
    rel("Longfellow te da un arpón único", "e2_arpon_rec", "Arpón único", "La recompensa", dur=4.4, x=.70, y=.52, tam=520),

    # ================= 1 · TOCHOMOSCA LEGENDARIA (FNV OWB)
    pu("Número uno#3", 1, "La tochomosca legendaria", "Old World Blues · cueva misteriosa", y=.80),
    mapa("big_mt", "Big MT", [pt("big_mt", "tunel_norte", "Túnel norte de Big MT", "inicio"),
                              pt("big_mt", "cueva_misteriosa", "Cueva misteriosa", "peligro", "e1_entrada")],
         "En el noreste de Big MT", ("espera ella|fin", .3), ["En el noreste de Big MT", "hay una cueva misteriosa"],
         "Cueva misteriosa", entrada="foco"),
    rel("Es la criatura más poderosa", "e1_tamano", "Tochomosca legendaria", "Junto a un humano", dur=5.0, x=.74, y=.52, tam=540),
    fi("Nivel cincuenta. Dos mil", "Tochomosca legendaria", [("Nivel", "50"), ("PS", "2 000"), ("Cuerpo a cuerpo", "450"),
                                                            ("Plasma", "300")], "Explota al morir: *225*", "CRIATURA", dur=8.0),
    mg_en(F.botin("Tochomosca legendaria", ["Carne de tochomosca ×50", "Psycho ×20", "Buffout ×20"]), "suelta cincuenta pedazos",
          5.0, "botín tochomosca", x=.72, y=.50),
    av("Y nació de una broma", "Idea de un foro", "Un jugador la pidió", dur=4.0),

    # ================= CIERRE
    muro([("e12_ruzka", "Ruzka"), ("e11_stripe", "Stripe"), ("e7_alien", "El alienígena"), ("e8_gabe", "Gabe"), ("e1_tochomosca", "La tochomosca")],
         "Esos son los quince", ("y no se lo contó a nadie|fin", .6),
         ["Esos son los quince", "cuántos encontraste tú", "alguien vio a Stripe"], destaca=1, titulo="¿Cuántos encontraste?"),
    mg(F.radio(["Radio Yermo"], 0, "Todos los comentarios se leen"), "Todos los comentarios se leen", ("próxima transmisión|fin", .3),
       [], "radio comentarios", y=.46),
    mg(F.radio(["Radio Yermo"], 0, "Esto fue Radio Yermo. No entres a una cueva sin marcador."), "Esto fue Radio Yermo",
       ("también muerde|fin", 1.0), [], "radio despedida", y=.40),
    ob("Suscríbete, no entres", "Suscríbete a Radio Yermo", hecho=True, dur=4.0, x=.70, y=.88, marca=1.0),
]

# ---- EXTRA: un apoyo más donde la voz nombra algo concreto (relleno de huecos > 4 s tras `fx --seco`)
EXTRA = [
    pv("de Fallout tres, New Vegas y Fallout cuatro", "gen_pipboy3000_rec", "Pip-Boy", dur=3.0, x=.80, y=.62, tam=300),
    zoom("Le salió al revés", ("y la reina quedó custodiada|fin", .2), 1.12),
    pv("con mil puntos de vida", "e15_grupo", "Los guardianes", dur=3.4, x=.20, y=.60, tam=360),
    pv("hay una mina llena de cazadores", "e14_mina", "Mina de Silver Peak", dur=3.6, x=.20, y=.60, tam=360),
    zoom("Pero al fondo, desde un túnel", ("del juego|fin", .2), 1.14),
    pv("rodeada de barcos hundidos", "e13_marcador", "La isla en el mapa", dur=3.4, x=.20, y=.60, tam=340),
    zoom("Años de leyenda", ("cabe en una cubeta|fin", .3), 1.12),
    pv("rodeada de esqueletos", "e12_guarida", "La guarida", dur=3.6, x=.80, y=.58, tam=380),
    pv("hay una caseta de perro", "e11_higgs", "La caseta de Gabe", dur=3.2, x=.20, y=.60, tam=340),
    pv("Y el techo y el estanque", "e10_reina", "Reina Nukalurk", dur=3.6, x=.20, y=.60, tam=380),
    pv("No sale en la historia", "e10_carga", "Nuka-World", dur=3.6, x=.80, y=.58, tam=380),
    zoom("se arranca pedazos radiactivos", ("también se transforma|fin", .2), 1.14),
    dict(tipo="temblor", en="el cuerpo se vuelve atómico", amp=40),
    dict(tipo="destello", en="el cuerpo se vuelve atómico"),
    pv("Tantos estimulantes le dieron", "e1_psycho_rec", "Psycho", dur=3.0, x=.80, y=.62, tam=280),
    pv("Te dispara en cuanto te ve", "e7_alien", "El alienígena", dur=3.4, x=.20, y=.60, tam=360),
    pv("Y en el rincón más profundo", "e6_sanguinario", "Sanguinario legendario", dur=4.0, x=.80, y=.58, tam=400),
    zoom("El soldado llevó la misericordia", ("El sanguinario, no|fin", .4), 1.12),
    zoom("se cura poco a poco", ("sentido del humor|fin", .3), 1.12),
    pv("Están en el juego desde el principio", "e4_mitico", "Sanguinario mítico", dur=3.4, x=.20, y=.60, tam=360),
    rel("Noventa y un niveles de esfuerzo", "e4_cigarrillo_rec", "Cigarrillo", "La recompensa", dur=4.4, x=.76, y=.52, tam=440),
    av("Su última víctima", "Baliza de socorro", "Soldado Gleeson · RNC", dur=3.6),
    zoom("Un sanguinario más listo", ("miedo a una bengala|fin", .3), 1.12),
    zoom("Longfellow dice que preferiría", ("eso es romántico|fin", .3), 1.12),
    pv("Vuela alto, brilla en verde", "e1_tochomosca", "La tochomosca legendaria", dur=4.0, x=.80, y=.58, tam=400),
    dict(tipo="destello", en="y al morir explota"),
    pv("veinte Psycho y veinte Buffout", "e1_buffout_rec", "Buffout", dur=3.0, x=.20, y=.62, tam=260),
    zoom("Sanguinarios, cazadores", ("es una mosca#2|fin", .4), 1.15),
    rel("el canal hermano es Crónicas", "tamriel_canal", "Crónicas de Tamriel", "El canal hermano", dur=5.0, x=.74, y=.50, tam=480),
]
FX = FX + EXTRA

# ---- EXTRA 2 (chequeo 23-nov: pegatinas 2,7/min contra 3,6 del canal; frases que nombran algo sin apoyo)
EXTRA2 = [
    pv("junto a Grayditch", "e15_marigold", "Estación Marigold", dur=3.0, x=.80, y=.62, tam=340),
    rel("En el Mojave hay dos formas", "e14_cazador", "Cazador legendario", "Silver Peak", dur=4.4, x=.76, y=.52, tam=460),
    pv("Lo llaman Red Death", "e13_red", "Red Death", dur=3.4, x=.80, y=.60, tam=360),
    pv("El espectáculo continúa", "e12_ruzka", "Ruzka", dur=3.4, x=.20, y=.60, tam=380),
    pv("Te persigue hasta la fuente", "e11_higgs", "La fuente de Higgs Village", dur=3.4, x=.80, y=.60, tam=360),
    pv("Brilla en la oscuridad", "e10_noche", "Reina Nukalurk", dur=3.6, x=.20, y=.60, tam=380),
    pv("Casi nadie la ve así", "e9_necrofaga", "Madre Curie III", dur=3.6, x=.80, y=.60, tam=360),
    cam("Predicaba la paz del Átomo", "e9_humana_rec", "Madre Curie", dur=3.4, x=.16, y=.64, tam=300),
    pv("Un ciberperro", "e8_gabe", "Gabe", dur=3.2, x=.80, y=.62, tam=360),
    pv("Lo único sensato es correr", "e8_ladra", "Gabe", dur=3.2, x=.20, y=.60, tam=340),
    pv("está llena de sanguinarios", "e6_interior", "Caverna Dead Wind", dur=3.4, x=.20, y=.60, tam=360),
    av("Solo existe con Broken Steel", "Requiere Broken Steel", "Y nivel alto", dur=3.6),
    pv("Y aun así le tiene miedo", "e3_bengala_rec", "Una bengala", dur=3.2, x=.20, y=.62, tam=300),
    cam("Si la matas, Longfellow", "e2_longfellow_rec", "El Viejo Longfellow", dur=3.6, x=.16, y=.64, tam=300),
    pv("A la izquierda de la entrada", "e1_interior", "Cueva misteriosa", dur=3.4, x=.20, y=.60, tam=360),
    pv("Su última víctima", "e3_azotea", "La Divisoria", dur=3.4, x=.80, y=.60, tam=340),
]
FX = FX + EXTRA2

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/fallout4/ → sfx/*.mp3), solo en momentos clave (como fo_nunca_f4)
_NUM = ["quince", "catorce", "trece", "doce", "once", "diez", "nueve", "ocho", "siete", "seis", "cinco", "cuatro", "tres", "dos"]
PISTAS = [dict(sfx="pipboy", en="Número " + n, vol=.30) for n in _NUM]
PISTAS += [dict(sfx="subir_nivel", en="Número uno#3", vol=.26), dict(sfx="mision_completada", en="Esos son los quince", vol=.24),
           dict(sfx="lugar_descubierto", en="Bajo la estación de metro Marigold", vol=.22),
           dict(sfx="lugar_descubierto", en="En el noreste de Big MT", vol=.22),
           dict(sfx="vats", en="Te dispara en cuanto te ve", vol=.36),
           dict(sfx="geiger", en="Brilla por el estroncio", vol=.30), dict(sfx="geiger", en="se arranca pedazos radiactivos", vol=.30),
           dict(sfx="terminal", en="Hoy, los quince enemigos", vol=.30), dict(sfx="mision_completada", en="Igual tienes que matarlo", vol=.22)]
