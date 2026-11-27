# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «15 FARMEOS de ORO del 30 al 50 en WoW Forever» (SECUENCIA YT, Crónicas de Warcraft; subagente C, 26-nov-2026).
Modelo: videos/wow_ruta_profesiones/efectos.py (helpers, kit de 4 estilos, tooltips de Wowhead y bloque Overgear).
- KIT DE 4 ESTILOS con los CAMBIOS DEL USUARIO del 25-nov: mapas SIEMPRE el original (E.mapa_e rota original → oro → madera →
  v1 → v2) con ÍCONO en cada punto (5.º campo: lo que se farmea, la cara del PNJ o su lugar; puntos de _coords.md, Wowhead
  Forever); tarjetas de criatura con su CARA (Fc → caras/); objetos con su TOOLTIP REAL de Wowhead al lado (tarj +
  _wowhead_ids.json) y foto equipado (hueso de oso, El pacificador); nada de letra negra chica sobre amarillo.
- Cada puesto: tarjeta de capítulo O.puesto (barra de nivel 30-50 con su tramo) + mapas + tarjetas + pegatinas + rótulos y, en
  la pausa "post" de 6,5 s, la FICHA DEL FARMEO (O.ficha_farmeo: nivel, zona, lo que se lleva con su precio de vendedor, oro,
  dónde venden la Horda y la Alianza; datos de videos/_investigacion_wow_oro_30_50.md y _coords.md, nada inventado).
- MG NUEVOS de este guion (nucleo/mg_oro.py, 26-nov): cuenta (montura 100 + doble esp. 50 = 150; 4 platas × 100 muertes),
  cronometro (coyotes 30 min = 6 o 84 p → 13-14/h; buitres 30 min = 21 o → ~41/h), etiquetas (vendedor contra subasta:
  colmillo, carne de cangrejo, glándula, perla de oro, carne de lobo tierna, el consejo final), probabilidad (1 de 3 fragmentos,
  4 de 10 cangrejos, 1 de 10 tierra elemental, 4 de 10 mollejas), encoge (huevos: de 1 oro a 15 platas en una semana), tope
  (5 mazmorras por hora), tabla_oro (el oro por hora que CRECE puesto a puesto), reparto (6 mollejas = la mitad), columnas
  (15 contra 40 valijas), puesto y ficha_farmeo. Prueba: python nucleo/mg_oro.py nuevos.
- Comentarios (≤ 10 días, ninguno repetido; ids en ESTADO.md): gancho @mfhm5700 y Azazel · reglas Carlo · burla0 Lalo ·
  burla1 Pkponcho · gracias1 Alexander, David, Rolazabal · gracias2 Lunatic, BiNWinslou.
- Overgear (escena overgear, 272,5-350 s): fondo de marca DEBAJO de reseñas, packshot y código; logo; capturas de la página de
  coaching (pantallas/og_coaching_*.jpg, 25-nov); pros, leveling, reseñas, packshot y CRONICAS10. Nada contra comprar oro.
- Flow (recreaciones con ingredientes del juego, marcadas RECREACIÓN): restos flotantes, cuatro valijas (todo el beat 140), cueva
  de Alterac, jaula de Rizz, esqueletos de Tanaris y, a pantalla completa en los beats sin clip real, reptadores (066) y jaguar (111).
  python fab.py wow_oro_30_50 fx --seco | python _revisa.py | FAB_FX_FINAL=1 python fab.py wow_oro_30_50 fx hoja
"""
import json as _json
import os

import mg_oro as O
import mg_tes as T
import mg_wow as M
import mg_wow_estilos as E
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
_PEG60 = os.path.join(_D, "..", "wow_errores_60", "pegatinas")     # poción de fuego (la nombra el patrocinio)
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", -0.4)   # el código del creativo sale ~3 s después de entrar: así coincide con la voz
FIN_OG = ("Número trece. Los gorilas", -.4)
TEMA_PEG = "wow"
V, RJ = "verde", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def Fc(slug):
    """Retrato recortado a cara y hombros (caras/<slug>.png): toda tarjeta de personaje enseña su CARA (regla 25-nov)."""
    c = os.path.join(_D, "caras", slug + ".png")
    return c if os.path.exists(c) else slug


def R(slug):
    """Cara si existe; si no, la pegatina."""
    c = Fc(slug)
    return c if os.path.exists(c) else F(slug)


_MARCO_ICO = ("polaroid", "carta", "estampilla", "naipe", "museo", "clasico")
_MARCO_FOTO = ("polaroid", "museo", "carta", "rasgado", "naipe", "estampilla", "cristal", "clasico", "pergamino")
_rot_marco = dict(ico=0, foto=0)


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    base = os.path.basename(str(slug))
    if "marco" not in anim:   # el «vitral» parte el ícono y la CARA en vidrieras (hojas 22 y 26-nov): marcos en rotación sin él
        k = "ico" if base.startswith("o_") else "foto"
        lista = _MARCO_ICO if k == "ico" else _MARCO_FOTO
        anim["marco"] = lista[_rot_marco[k] % len(lista)]
        _rot_marco[k] += 1
    if base.startswith("o_"):
        tam = min(tam, 340)
    ruta = slug if os.path.exists(slug) else F(slug)
    return dict(tipo="mg", fn=PA.variado(ruta, titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + os.path.basename(slug), ver=1.0)


def filav(en, items, y=.64, tam=300, dur=4.4, xs=(.13, .30, .47, .64, .81)):
    """Fila de pegatinas; items = [(slug o ruta, título, ancla o None = la misma[, dict(entrada=…, salida=…)])]."""
    return [pv(it[2] or en, it[0], it[1], dur=dur, x=xs[i], y=y, tam=tam, **(it[3] if len(it) > 3 else {}))
            for i, it in enumerate(items)]


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    """Pila de fotos que se reparte (una por marca de la voz); fotos = [(ruta, etiqueta)]."""
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila(list(fotos), tam, TEMA_PEG, marco), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.06,
                nombre="pegatina pila " + nombre, ver=2.0)


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + id_, ver=1.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0, ruta=None):
    r = ruta or os.path.join(_PAN, slug + ".jpg")
    return dict(tipo="pantalla", fn=M.pantalla(r, zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5,
                nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, estilo=None, zmax=1.5):
    """Mapa del KIT (rota solo; siempre el mapa ORIGINAL). puntos = [(x, y, rótulo, sub, slug_ícono)] de `_coords.md`."""
    return E.mapa_e(nom, [E.P(x, y, r, sb, Fc(f) if f and not str(f).startswith("ico:") else f) for x, y, r, sb, f in puntos],
                    de, a, marcas, titulo, sub, estilo=estilo, zmax=zmax)


_WH = _json.load(open(os.path.join(_D, "_wowhead_ids.json"), encoding="utf-8"))
_TIPS = []


def tarj(en, slug, *a, **k):
    """E.tarjeta_e con la cara (personajes) o el ícono (objetos). Si es un objeto/hechizo con ID de Wowhead Forever
    (_wowhead_ids.json), al otro lado sale su TOOLTIP REAL (APOYO wowhead) y, si se equipa, la foto «Así se ve puesto»."""
    k.setdefault("x", .74)
    k.setdefault("tam", 420)
    out = [E.tarjeta_e(en, Fc(slug), *a, **k)]
    w = _WH.get(slug) or {}
    if w.get("ref"):
        ref = w["ref"]
        if w.get("tipo") == "spell":                       # forever/33388 → forever/spell/33388
            pre, n = ref.rsplit("/", 1)
            ref = f"{pre}/spell/{n}"
        lado = .43 if k["x"] > .5 else .57                 # junto a la tarjeta, fuera del sitio de las pegatinas (x .07-.27)
        _TIPS.append(dict(en=en, wowhead=ref, dur=k.get("dur", 5.0), x=lado, y=.46, size=.28))
        if w.get("equipado"):
            out.append(pv(en, os.path.join(_PEG, "eq_" + slug + ".jpg"), "Así se ve puesto", dur=k.get("dur", 5.0),
                          x=.12 if lado < .5 else .88, y=.27, tam=290))
    return out


def tarjc(en, slug, titulo, sub=None, dur=4.4, x=.76, y=.50, tam=480):
    """Tarjeta de criatura o PNJ con su CARA (kit de 4 estilos en rotación)."""
    return E.tarjeta_e(en, Fc(slug), titulo, sub, dur=dur, x=x, y=y, tam=tam)


def rot(en, texto, sello=None, dur=4.5):
    """Rótulo inferior del kit (rota estilos): borde izquierdo a 150 px y y=.85 (los de pergamino y madera se salían del 4 %)."""
    return E.rotulo_e(en, texto, sello=sello, dur=dur, izq=150, y=.85)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def tar(en, titulo, icono, lineas, calidad="amarillo", dur=5.0, x=.72, size=.46):
    """Ficha de interfaz (tooltip del juego) a la derecha. icono = nombre de Wowhead o slug de pegatina."""
    if os.path.exists(F(icono)):
        icono = _ICONO.get(icono, icono)
    return dict(en=en, dur=dur, x=x, size=size, tarjeta=dict(titulo=titulo, calidad=calidad, icono=icono, lineas=lineas))


_ICONO = {k: v["icono"] for k, v in _json.load(open(os.path.join(_PEG, "_creditos.json"), encoding="utf-8")).items() if v.get("icono")}


def muro(fotos, de, a, marcas, titulo=None, cols=5, alto=560):
    import presenta as PR
    return dict(tipo="mg", fn=PR.muro(list(fotos), cols=cols, tema=TEMA_PEG, alto=alto, titulo=titulo), de=de, a=a,
                marcas=list(marcas), x=.5, y=.53, sale=.06, nombre="muro", ver=4.0)


_ROT_FLOW = []


def flow(slug, de, a, respaldo=(), zoom=(1.0, 1.08)):
    """Imagen de Flow (pegatinas/flow_<slug>.png, RECREACIÓN con ingredientes del juego) a cuadro entero, con acercamiento lento
    y la marca «RECREACIÓN»; si el archivo faltara, va el respaldo (lista de FX)."""
    r = os.path.join(_PEG, f"flow_{slug}.png")
    if not os.path.exists(r):
        return list(respaldo)
    _ROT_FLOW.append(dict(texto="RECREACIÓN", en=de, dur=3.0, tam=54, color="blanco", x=.86, y=.07))
    return [pant("flow_" + slug, de, a, zoom=zoom, ruta=r)]


# ---------------------------------------------------------------- tarjeta de capítulo y FICHA DEL FARMEO de cada puesto
def puesto(n, nombre, cara, zona, rangos, de, a, marcas):
    img = cara if os.path.exists(str(cara)) else Fc(cara)
    return mg(O.puesto(n, nombre, img, zona, rangos), de, a, marcas, f"puesto {n}", y=.44)


H, A, N = "Horda", "Alianza", "Los dos"
FICHAS = {   # n: (nombre, cara, nivel, zona, objetos [(slug|ícono, nombre, precio vendedor)], oro, venta, ancla de cierre)
    15: ("Centauros Magram", "retador_magram", "33-38", "Desolace · Poblado Magram",
         [("o_pano_seda", "Paño de seda", "1p 50c"), ("o_tejido_magico", "Paño de tejido mágico", "2p 50c"),
          ("inv_misc_coin_02", "Monedas", None)],
         "Sin medir todavía: reaparecen más rápido desde el 25-nov",
         [(H, "Campamento del Espíritu Errante"), (A, "Punta de Nijel")], "y cuando la bolsa se llena, sales a vender"),
    14: ("Arañas Niebla Negra", "arana_niebla_negra", "35-38", "Marjal Revolcafango · Cueva Niebla Negra",
         [("o_seda_arana_espesa", "Seda de araña espesa", "7p 50c"), ("o_seda_sombras", "Seda de las Sombras", "10p"),
          ("o_mandibula_arana", "Mandíbula de araña chorreando", "5p 83c"), ("o_punta_pata_arana", "Punta de pata de araña dura", "4p 91c")],
         "Las sedas, mejor para los sastres",
         [(H, "Poblado Murohelecho"), (A, "Isla Theramore")], "La Alianza, en la Isla Theramore"),
    13: ("Gorilas Velo de Bruma", "gorila_velo_bruma", "32-35 · ancianos 40", "Vega de Tuercespina · oeste del Lago Nazferiti",
         [("o_colmillo_gorila", "Colmillo de gorila · la subasta paga más", "67c"), ("o_pelo_gorila_burdo", "Pelo de gorila", None)],
         "5-6o/h (precios del 12-nov)",
         [(H, "Campamento Grom'Gol"), (A, "Asentamiento Rebelde"), (N, "Bahía del Botín")], "Y si llega alguien más, baja a los ancianos"),
    12: ("Tortugas brillavalva", "tortuga_brillavalva", "30-36", "Las Mil Agujas · El Desierto de Sal",
         [("o_fragmento_caparazon", "Fragmento de caparazón moteado", "9p 3c"), ("o_cola_escamosa", "Cola escamosa espesa", "1p 55c"),
          ("o_carne_tortuga", "Carne de tortuga · mejor a la subasta", "87c")],
         "~4o/h de botín, más las monedas",
         [(N, "Circuito del Espejismo")], "a unas seis platas por muerte"),
    11: ("Reptadores de arena", "reptador_arena", "36-41", "Claros del Río · sur del Puerto Polvomecha",
         [("o_carne_cangrejo", "Carne de cangrejo tierna", "1p 12c"), ("o_almeja_boca_grande", "Almeja de boca grande (sur de Tuercespina)", "46c")],
         "Carne de cangrejo: 14p en la subasta (12-nov)",
         [(N, "Puerto Polvomecha")], "Y dentro de las almejas hay perlas"),
    10: ("Crías del Barranco Lethlor", "cria_lethlor", "40-44", "Tierras Inhóspitas · este de la zona",
         [("o_glandula_llamas", "Glándula de llamas pequeña", "2p 50c"), ("o_vastago_oscuro", "Vástago oscuro (mascota)", "25p"),
          ("inv_misc_coin_02", "Monedas", None), ("o_corazon_draco", "Corazón de draco negro (misión)", None)],
         "Sin cifra: oro y unos 30 000 de experiencia por hora",
         [(H, "Kargath"), (A, "campamentos goblin del centro")], "las crías se farmean por los bordes"),
    9: ("Múrlocs del Pantano", "murloc_marisma", "41-45", "Pantano de las Penas · playa del sureste",
        [("o_almeja_boca_grande", "Almeja de boca grande", "46c"), ("o_perla_oro", "Perla de oro", "1o"),
         ("o_perla_negra", "Perla negra", "10p"), ("o_carne_almeja", "Carne de almeja sabrosa", "50c")],
        "Perla de oro: 1o 30p en la subasta (22-nov)",
        [(H, "Rocal"), (N, "El Puerto")], "que ahí hay demasiados juntos"),
    8: ("Hienas Llagapata", "hiena_llagapata", "44-46", "Tanaris · Arenas Abisales",
        [("o_melena_espesa", "Melena espesa", "8p 12c"), ("o_pata_trofeo", "Pata de trofeo grande", "9p 37c"),
         ("o_carne_lobo_tierna", "Carne de lobo tierna · mejor a la subasta", "1p 50c"), ("o_huevo_gigante", "Huevo gigante (rocs)", "1p 50c")],
        "Carne de lobo tierna: casi 1o el montón (23-nov)",
        [(N, "Gadgetzan")], "ya sabes dónde más buscarla"),
    7: ("Gorilas y osos de Feralas", "tronador_groddoc", "47-50 · centro 41-43", "Feralas · Los Dos Colosos",
        [("o_hueso_oso", "Hueso de oso grande", "14p 84c"), ("o_mechon_gorila", "Mechón de pelo de gorila", "11p 31c"),
         ("o_mandibula_oso", "Mandíbula de oso", "8p 98c"), ("o_garra_oso", "Garra de oso indómito", "5p 78c")],
        "Sin profesión: grises que paga el vendedor",
        [(H, "Campamento Mojache"), (A, "Bastión Plumaluna")], "y la Alianza en el Bastión Plumaluna"),
    6: ("Jaguares del pantano", "jaguar_pantano", "36-39", "Pantano de las Penas · plan B: Claros del Río",
        [("o_cola_blanda", "Cola blanda larga", "8p 6c"), ("o_bigote_cerdas", "Bigote de cerdas", "7p 33c"),
         ("o_cuero_pesado", "Cuero pesado (con desuello)", "1p 50c")],
        "+10o/h",
        [(H, "Rocal · y Rog'mar en Claros del Río"), (N, "El Puerto")], "Y si una zona está llena, vas a la otra"),
    5: ("Elementales de roca", "elemental_roca", "37-44", "Tierras Inhóspitas · tres franjas",
        [("o_piedra_lisa", "Trozo de piedra lisa", "5p 30c"), ("o_piedra_dentada", "Trozo de piedra dentado", "4p 11c"),
         ("o_piedra_inerte", "Piedra inerte", "3p 60c"), ("o_tierra_elemental", "Tierra elemental · guárdala", "4p")],
        "~10o/h solo en grises",
        [(H, "Kargath"), (A, "campamentos goblin del centro")], "mira qué precio tiene"),
    4: ("Coyotes de Claros del Río", "coyote_llanuras", "36-40", "Claros del Río · sur del Cortijo de Wheeler",
        [("o_cola_tupida", "Cola tupida suave", "7p 45c"), ("o_melena_espesa", "Melena espesa", "8p 12c"),
         ("o_carne_lobo_rojo", "Carne de lobo rojo", "87c"), ("o_colmillo_grande", "Colmillo grande", "75c")],
        "13-14o/h (medido el 20-nov)",
        [(N, "Fortaleza de Farholde")], "a los elementales del número cinco"),
    3: ("Pesca de valijas", "o_valija_mitril", "cualquier nivel · pesca 150", "Vega de Tuercespina · costa oeste",
        [("o_valija_mitril", "Valija reforzada con mitril · se abre", None), ("o_anguila_petrea", "Anguila escama pétrea", "10p"),
         ("o_luremaster", "Maestro del cebo (talento de Legado)", None), ("o_jarabe_agua", "Jarabe de caminar sobre el agua", None)],
        "170o en 3 h 30 con el talento",
        [(H, "Campamento Grom'Gol (buzón)"), (N, "Bahía del Botín")], "y todo va al buzón"),
    2: ("Cuevas de ogros", "ogro_aplastacresta", "34-38", "Montañas de Alterac · Dominios de los Aplastacresta",
        [("o_mena_oro", "Mena de oro", "5p"), ("o_mena_veraplata", "Mena de veraplata", "5p"),
         ("o_mena_mitril", "Mena de mitril", "2p 50c"), ("o_pano_seda", "Paño de seda", "1p 50c")],
        "~30o/h (20-25 sin montura ni botas)",
        [(N, "Rizz Tornillosuelto, en su jaula")], "Quédate en las cuevas"),
    1: ("Destripadores negros", "destripador_negro", "46-50", "Las Tierras Devastadas · Alto de los Rapiñadores",
        [("o_molleja_buitre", "Molleja de buitre · subasta +2o", None), ("o_papada_hiena", "Papada de hiena risitas", None),
         ("o_pinza_scorpok", "Pinza de scorpok", None), ("inv_misc_coin_02", "Monedas", None)],
        "~41o/h (17 sin mollejas)",
        [(A, "Castillo de Nethergarde (vuelo)"), (H, "vuelo desde Rocal")], "desde el vuelo del Pantano de las Penas"),
}


def ficha(n):
    nom, cara, nivel, zona, objs, oro, venta, fin = FICHAS[n]
    img = Fc(cara) if os.path.exists(Fc(cara)) else F(cara)
    objs = [(F(s) if os.path.exists(F(s)) else s, t, p) for s, t, p in objs]
    return dict(tipo="mg", fn=O.ficha_farmeo(n, nom, img, nivel, zona, objs, oro, venta), de=(fin + "|fin", .25),
                a=(fin + "|fin", 6.4), marcas=[], x=.5, y=.5, sale=.4, nombre=f"ficha del farmeo {n}", ver=1.0)


def tabla(filas, nueva, de, a, marca, nota=None):
    fil = [(Fc(c) if c else None, r, v, t) for c, r, v, t in filas]
    return mg(O.tabla_oro("ORO POR HORA · LO QUE MIDIERON LOS JUGADORES", fil, nueva, nota), de, a, [marca], "tabla de oro", y=.50)


T_CENT = ("retador_magram", "Centauros · Desolace", None, "sin medir")
T_GOR = ("gorila_velo_bruma", "Gorilas · Tuercespina", 5.5, "5-6o/h")
T_JAG = ("jaguar_pantano", "Jaguares y cazadoras", 10.3, "+10o/h")
T_ELE = ("elemental_roca", "Elementales de roca", 10, "~10o/h")
T_COY = ("coyote_llanuras", "Coyotes · Claros del Río", 13.5, "13-14o/h")
T_ALT = ("ogro_aplastacresta", "Cuevas de Alterac", 30, "~30o/h")
T_BUI = ("destripador_negro", "Buitres · Tierras Devastadas", 41, "~41o/h")
T_BUI0 = ("destripador_negro", "Buitres, sin ninguna molleja", 17, "~17o/h")

CAMARA = {}
FUNDIDO = {}
FX = [
    # =========================================================== OVERGEAR: fondo de marca PRIMERO (debajo de reseñas, packshot y código)
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="Si reservas dos horas", a=FIN_OG,
         entra=.3, nombre="og fondo marca"),
    # Beats SIN clip real (subagente A, 26-nov): la recreación de Flow ocupa TODO el beat, con acercamiento lento; los mapas y MG
    # del puesto van encima. scene-066 = reptadores de arena en la playa de Claros del Río · scene-111 = jaguar del pantano.
    *flow("reptadores_playa", "scene-066", "scene-066:fin", zoom=(1.0, 1.14)),
    *flow("jaguar_pantano", "scene-111", "scene-111:fin", zoom=(1.0, 1.14)),
    # =========================================================== INTRO (0-60 s): un elemento cada 2-4 s, MG desde el segundo 0
    tarj(("Llegas al nivel cuarenta en", -.3), "o_equitacion", "Aprendiz jinete", "lo enseña el instructor de equitación", dur=5.4),
    E.peg_e("corres al instructor de equitación", "o_oro", "Abres la bolsa", dur=2.9, x=.17, y=.62),
    mg(O.cuenta("LO QUE CUESTA EL NIVEL 40", [(F("o_equitacion"), "Montura", "100o"), ("txt:×2", "Doble especialización", "50o")],
                ("En el mismo nivel", "150o", "DE GOLPE")),
       ("La montura cuesta cien de oro", -.3), ("en el mismo nivel|fin", .6),
       ["La montura cuesta cien de oro", "son otros cincuenta", "Ciento cincuenta de oro, de golpe"], "cuenta 150", y=.48),
    rot(("llegó al treinta y nueve con", -.2), "Nivel 39 · 67 de oro", sello="39", dur=4.2),
    E.peg_e(("y se puso a probar farmeos", -.2), "o_ico_reloj", "Media hora cada uno", dur=3.4, x=.76, y=.46, tam=320),
    mapa("devastadas", [(48.0, 29.1, "Alto de los Rapiñadores", "cráteres negros", "alto_rapinadores"),
                        (56.2, 36.5, "Destripadores negros", "un buitre cada pocos minutos", "o_molleja_buitre")],
         ("Mientras tanto, en un cráter", -.2), ("un buitre que deja, en promedio", -.1),
         ["en un cráter negro de Las", "aparece cada pocos minutos un"], "LAS TIERRAS DEVASTADAS", "un cráter negro"),
    tarjc(("un buitre que deja, en promedio", -.2), "destripador_negro", "Destripador negro", "casi 1 de oro por muerte", dur=4.4),
    pv(("casi una moneda de oro por", -.3), "o_molleja_buitre", "Molleja de buitre", dur=3.2, x=.17, y=.62),
    mapa("alterac", [(52.8, 47.1, "Vetas de cinco minerales", "ninguna guía de subida pisa aquí", "o_mena_oro"),
                     (47.3, 35.3, "Rizz Tornillosuelto", "un vendedor en una jaula", "rizz")],
         ("Y en una cueva de Alterac", -.2), ("y un vendedor encerrado en una jaula|fin", .3),
         ["hay vetas de cinco minerales", "y un vendedor encerrado en"], "MONTAÑAS DE ALTERAC", "una cueva que nadie pisa"),
    muro([(R(c), f"{n} · {t}") for n, c, t in ((15, "retador_magram", "Centauros"), (14, "arana_niebla_negra", "Arañas"),
                                                 (13, "gorila_velo_bruma", "Gorilas"), (12, "tortuga_brillavalva", "Tortugas"),
                                                 (11, "reptador_arena", "Cangrejos"), (10, "cria_lethlor", "Crías"),
                                                 (9, "murloc_marisma", "Múrlocs"), (8, "hiena_llagapata", "Hienas"),
                                                 (7, "tronador_groddoc", "Gorilas y osos"), (6, "jaguar_pantano", "Jaguares"),
                                                 (5, "elemental_roca", "Elementales"), (4, "coyote_llanuras", "Coyotes"),
                                                 (3, "o_valija_mitril", "Valijas"), (2, "ogro_aplastacresta", "Ogros y vetas"),
                                                 (1, "o_ico_pregunta", "¿?"))],
         ("Hoy van quince farmeos de", -.2), ("qué matar, dónde", -.3),
         [("Hoy van quince farmeos de", .2 + .19 * k) for k in range(15)], "15 FARMEOS · DEL 30 AL 50"),
    E.ficha_e("CADA FARMEO", ["inv_sword_04", "inv_misc_map_01", "inv_misc_coin_02", "inv_misc_bag_10"],
              ("qué matar, dónde", -.3), ("y a quién vendérselo|fin", .7),
              [("qué matar, dónde", .1), ("qué matar, dónde", .6), "cuánto da y a", "y a quién vendérselo"],
              etiquetas=["qué matar", "dónde", "cuánto da", "a quién"]),
    rot(("Del que menos rinde al", 0), "Del que menos rinde al que más", sello="15", dur=3.6),
    E.peg_e(("Y el número uno, te adelanto", -.1), "o_ico_pregunta", "El número uno", dur=4.2, x=.76, y=.46, tam=320),
    # =========================================================== REGLAS (60-145 s)
    rot(("Antes, dos comentarios que nos", 0), "Dos comentarios nos dieron la idea", sello="2", dur=3.6),
    com(("un espectador nos contó que llegó", -.4), "UgzdmIz1PYiEJip9Cgp4AaABAg", dur=5.0, x=.30, y=.30),
    mg(M.contadores("SU BOLSA", [("inv_misc_coin_02", "Al 40, con montura y doble esp.", 3, 0, 1),
                                 ("inv_misc_coin_01", "Ahora, en el 48", 100, 2, 3)], ("YA TIENEN DUEÑO", 4), ancho=1300),
       ("Y se quedó con tres de", -.2), ("entrenamientos y profesiones|fin", .2),
       [("Y se quedó con tres de", 0), ("Y se quedó con tres de", .9), "Ahora va en el cuarenta y ocho", "con cien de oro, y esos",
        "y esos cien ya tienen dueño"], "su bolsa 3 → 100", y=.56),
    com(("Y otro espectador, Azazel", .1), "Ugz7CYQY4fp_-Ygst7B4AaABAg", dur=6.0, x=.30, y=.30),
    rot(("va en el treinta y tres con", -.2), "Nivel 33 · 300 de oro · un solo objeto", sello="33", dur=4.6),
    E.peg_e(("No nos dijo cuál", -.1), "o_ico_pregunta", "¿Cuál es el suyo?", dur=3.0, x=.17, y=.60),
    rot(("y si el suyo está en la", -.3), "¿Está en la lista? Que nos avise", sello="?", dur=3.6),
    mg(O.tope("REGLA 1 · DESDE EL 20 DE NOVIEMBRE", "achievement_dungeon_gloryofthehero", 5, "CADA MAZMORRA: 5 POR HORA", "TOPE",
              "El oro del 30 al 50: en el mundo abierto"),
       ("Tres reglas antes de empezar", -.2), ("está en el mundo abierto|fin", .2),
       ["cada mazmorra se puede reiniciar", "como mucho cinco veces por hora", "El oro del treinta al cincuenta"], "tope mazmorras", y=.50),
    mg(O.encoge("REGLA 2 · LO QUE TODOS FARMEAN SE HUNDE", F("o_huevo_gigante"), "Huevo gigante", "1o", "15p", "EN UNA SEMANA", 7),
       ("Segunda: lo que todos farmean", -.1), ("unas quince platas en una semana|fin", .5),
       ["Los huevos gigantes pasaron de un oro a unas", ("de un oro a unas quince", -.4)], "huevos se hunden", y=.50),
    com(("Y aquí un espectador, Carlo", -.1), "UgyZCobf2UUSu8EF4k54AaABAg", dur=6.4, x=.30, y=.30),
    rot(("Tiene razón, y por eso en", 0), "Primero, lo que paga el vendedor", sello="1", dur=4.4),
    mg(M.grupos("REGLA 3 · CUALQUIER CLASE", [(1, f"classicon_{c}", " ", (255, 255, 255)) for c in
                                               ("warrior", "paladin", "hunter", "rogue", "priest", "shaman", "mage", "warlock", "druid")],
                ancho=1180),
       ("Y tercera regla: cualquier clase", -.2), ("pero el buitre no pregunta qué", -.4),
       [("cualquier clase puede hacer los", .1 + .22 * k) for k in range(9)], "cualquier clase", y=.50),
    tarjc(("pero el buitre no pregunta qué", -.3), "destripador_negro", "El buitre", "no pregunta qué eres", dur=3.3),
    mg(O.ficha_farmeo("15 al 1", "Cada farmeo", F("o_ico_pregunta"), "del 30 al 50", "dónde está",
                      [(F("o_ico_bolsa"), "lo que se lleva y lo que paga el vendedor", None)], "cuánto da",
                      [(H, "dónde vende la Horda"), (A, "dónde vende la Alianza")]),
       ("Y al final de cada farmeo vas", .3), ("cuánto da y dónde venderlo|fin", .7),
       ["el nivel, la zona", "la zona, lo que se", "lo que se lleva, cuánto", "cuánto da y dónde", "y dónde venderlo"], "ficha modelo", y=.50),
    # =========================================================== P15 · CENTAUROS MAGRAM (145-210 s)
    puesto(15, "CENTAUROS MAGRAM", "retador_magram", "Desolace · Poblado Magram", [(33, 38, "33-38")],
           ("Número quince. Los centauros", -.2), ("del treinta y tres al treinta y ocho|fin", .3),
           [("Número quince. Los centauros", 0), "del treinta y tres al treinta y ocho"]),
    mapa("desolace", [(70.8, 76.8, "Poblado Magram", "33-38 · campamento grande", "o_pano_seda"),
                      (67.6, 72.5, "Cazavientos y retadores", "33-34", "o_pano_seda"),
                      (72.5, 67.6, "Retadores y cazavientos", "otro grupo", "o_tejido_magico")],
         ("Es un campamento grande de", -.2), ("al sureste de la zona|fin", .3),
         [("Es un campamento grande de", .3), "con retadores, cazavientos y", "repartidos en varios grupos"], "DESOLACE", "Poblado Magram"),
    pv(("Y está en la lista por", -.1), "poblado_magram", "Poblado Magram", dur=3.4, x=.20, y=.56, tam=440),
    tar(("el veinticinco de noviembre, Blizzard", -.2), "Revisión del 25 de noviembre", "inv_misc_note_02",
        ["Poblado Magram · Desolace", dict(t="Los centauros reaparecen más rápido", c=V)], dur=5.6),
    tarjc(("Más centauros por hora para", -.2), "retador_magram", "Retador Magram", "reaparece más rápido", dur=3.8),
    tabla([T_CENT], 0, ("Todavía nadie ha medido cuánto", -.2), ("así que serías de los primeros|fin", .2),
          ("nadie ha medido cuánto oro", 0), "Todavía nadie lo ha medido"),
    pv(("Son humanoides, así que sueltan", -.1), Fc("cazavientos_magram"), "Cazavientos Magram", dur=3.6, x=.17, y=.58, tam=420),
] + tarj(("sueltan monedas y paño de seda", -.1), "o_pano_seda", "Paño de seda", "vendedor: 1 plata y media", dur=4.2) \
  + tarj(("empieza a caer el tejido mágico", -.4), "o_tejido_magico", "Paño de tejido mágico", "hacia el nivel 35", dur=2.8) + [
    tarjc(("las Zarpósea, que ya son", -.3), "zarposea_magram", "Zarpósea Magram", "hienas · ya son del 37", dur=4.0),
    rot(("quédate en los grupos del borde", -.3), "Si vas justo: los grupos del borde", sello="!", dur=3.2),
    mapa("desolace", [(70.8, 76.8, "Poblado Magram", "entras y matas", "o_pano_seda"),
                      (55.5, 55.9, "Campamento del Espíritu Errante", "vende la Horda", "o_oro"),
                      (65.1, 8.3, "Punta de Nijel", "vende la Alianza", "o_oro")],
         ("No pide profesión ni ruta", -.2), ("sales a vender|fin", .1),
         ["entras al poblado, matas", "y cuando la bolsa se llena", "sales a vender"], "DESOLACE", "a vender"),
    ficha(15),
    # =========================================================== P14 · ARAÑAS NIEBLA NEGRA (210-272 s)
    puesto(14, "ARAÑAS NIEBLA NEGRA", "arana_niebla_negra", "Marjal Revolcafango · Cueva Niebla Negra", [(35, 38, "35-38")],
           ("Número catorce. Las arañas", -.2), ("del treinta y cinco al treinta y ocho|fin", .3),
           [("Número catorce. Las arañas", 0), "del treinta y cinco al treinta y ocho"]),
    mapa("marjal", [(33.3, 22.8, "Cueva Niebla Negra", "35-38 · arañas dentro y fuera", "o_seda_sombras")],
         ("Están fuera y dentro de", -.2), ("muy juntas y sin pegar fuerte|fin", .2),
         [("Están fuera y dentro de", .3)], "MARJAL REVOLCAFANGO", "al norte del marjal"),
] + filav(("arañas Niebla Negra y ermitañas", -.3), [(Fc("arana_niebla_negra"), "Araña Niebla Negra", None),
                                                   (Fc("ermitana_niebla_negra"), "Ermitaña Niebla Negra", ("y ermitañas Niebla Negra", -.2))],
          y=.60, tam=300, dur=3.6, xs=(.14, .33)) \
  + tarj(("la mandíbula de araña chorreando", -.2), "o_mandibula_arana", "Mandíbula de araña chorreando", "vendedor: casi 6 platas", dur=3.2) \
  + tarj(("y la punta de pata de", -.1), "o_punta_pata_arana", "Pata de araña dura", "la punta · vendedor: casi 5 platas", dur=3.2) \
  + tarj(("La seda de araña espesa, a", -.2), "o_seda_arana_espesa", "Seda de araña espesa", "vendedor: 7 platas y media", dur=3.6) \
  + tarj(("y la seda de las Sombras", -.2), "o_seda_sombras", "Seda de las Sombras", "vendedor: 10 platas", dur=3.0) + [
    E.ficha_e("NO AL VENDEDOR: PARA LOS SASTRES", ["o_seda_arana_espesa", "o_seda_sombras"],
              ("Y esas dos mejor no las", -.1), ("con daño de las Sombras|fin", .4),
              ["las piden los sastres para", "y para piezas con daño"], etiquetas=["para subir", "daño de Sombras"]),
    rot(("Hay pocas apariciones, unas cuarenta", 0), "Pocas apariciones: unas 40", sello="40", dur=3.8),
    pant("cueva_niebla_negra", ("métete a la cueva, que dentro", -.4), ("que suelta un verde|fin", .3), zoom=(1.0, 1.12)),
    mapa("marjal", [(33.3, 22.8, "Cueva Niebla Negra", None, "o_seda_sombras"),
                    (36.3, 31.4, "Poblado Murohelecho", "vende la Horda", "o_oro"),
                    (65.0, 47.1, "Isla Theramore", "vende la Alianza", "o_oro")],
         ("La Horda vende al lado", -.2), ("en la Isla Theramore|fin", .2),
         [("La Horda vende al lado", .2), "en el Poblado Murohelecho", "La Alianza, en la Isla"], "MARJAL REVOLCAFANGO", "a vender"),
    ficha(14),
    # =========================================================== OVERGEAR (272,5-350 s) — logo, coaching, captura, pros, reseñas, captura precio, packshot, código
    pv(("algo que ningún buitre suelta", -.3), "o_molleja_buitre", "Esto no lo suelta ningún buitre", dur=3.6, x=.17, y=.62),
    rot(("para matar más rápido y", -.2), "Matar más rápido y morir menos", sello="!", dur=3.6),
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
    pv(("resistencia al fuego para la", -.3), "guarida_onyxia", "Guarida de Onyxia", dur=4.4, x=.76, y=.42, tam=480),
    pv(("consumibles, y qué equipo previo", -.2), os.path.join(_PEG60, "o_pocion_fuego.png"), "Consumibles", dur=3.6, x=.17, y=.62),
    rot(("cuanto más rápido matas, más", -.2), "Más rápido matas, más oro por hora", sello="+", dur=4.6),
    pv(("más oro por hora te deja", -.3), "o_oro", "Más oro por hora", dur=3.4, x=.76, y=.46, tam=320),
    # =========================================================== P13 · GORILAS VELO DE BRUMA (350-420 s)
    puesto(13, "GORILAS VELO DE BRUMA", "gorila_velo_bruma", "Vega de Tuercespina", [(32, 35, "32-35"), (40, 41, "ancianos 40")],
           ("Número trece. Los gorilas", -.2), ("y sus ancianos al cuarenta|fin", .3),
           [("Número trece. Los gorilas", 0), "del treinta y dos al treinta", "y sus ancianos al cuarenta"]),
    tarjc(("Tienen una ventaja que casi", -.1), "gorila_velo_bruma", "Gorila Velo de Bruma", "nadie los tiene de misión", dur=4.4),
    rot(("no hay misión de matarlos", -.2), "Sin misión: ni Alianza ni Horda", sello="0", dur=4.2),
    pv(("Así que casi siempre están", -.2), Fc("gorila_velo_bruma_anciano"), "Siempre vivos, sin nadie alrededor", dur=3.4, x=.76, y=.46, tam=420),
    mapa("tuercespina", [(37.7, 17.1, "Gorilas Velo de Bruma", "oeste del Lago Nazferiti · 32-33", "o_colmillo_gorila"),
                         (32.5, 66.8, "Gorilas ancianos", "Valle del Velo de Bruma · 40-41", "gorila_velo_bruma_anciano")],
         ("Los jóvenes viven al oeste", -.2), ("más al sur|fin", .3),
         [("Los jóvenes viven al oeste", .3), "Los ancianos, en el Valle"], "VEGA DE TUERCESPINA", "jóvenes al norte, ancianos al sur"),
    pv(("Sueltan pelo de gorila para", -.6), "o_pelo_gorila_burdo", "Pelo de gorila · al vendedor", dur=2.5, x=.17, y=.62),
    mg(O.etiquetas("¿VENDEDOR O SUBASTA?", F("o_colmillo_gorila"), "Colmillo de gorila", ("VENDEDOR", "67c"), ("SUBASTA", "bastante más"),
                   (1, "A LA SUBASTA")),
       ("y el colmillo de gorila, que", 0), ("Pero la subasta paga bastante más|fin", .5),
       ["que el vendedor te paga a", "Pero la subasta paga bastante", ("Pero la subasta paga bastante más|fin", 0)], "colmillo", y=.50),
    tarjc(("Porque una misión, La fiebre", -.1), "unbagwa", "Médico brujo Unbagwa", "La fiebre de Tuercespina", dur=3.8),
    pv(("para invocar a Mokk el", -.2), Fc("mokk"), "Mokk el Salvaje · en oleadas", dur=3.0, x=.17, y=.56, tam=440),
] + tarj(("y vuelve a comprarlos", -.8), "o_colmillo_gorila", "Colmillo de gorila", "quien falla, vuelve a comprarlos", dur=2.6) + [
    tabla([T_GOR, T_CENT], 0, ("A un jugador le salieron entre", -.2), ("con los precios del doce de noviembre|fin", .4),
          ("entre cinco y seis de oro", 0), "Precios del 12 de noviembre"),
    mapa("tuercespina", [(37.7, 17.1, "Gorilas del norte", "solo unas 14 apariciones", "o_colmillo_gorila"),
                         (32.5, 66.8, "Gorilas ancianos", "si llega alguien más", "gorila_velo_bruma_anciano")],
         ("Un aviso: los gorilas del", -.2), ("baja a los ancianos|fin", .2),
         ["los gorilas del norte son pocos", "Y si llega alguien más, baja"], "VEGA DE TUERCESPINA", "rinde si estás solo"),
    ficha(13),
    # =========================================================== BURLA0 · Lalo (420-450 s)
    rot(("Y aquí va un comentario", 0), "Un comentario", sello="!", dur=3.4),
    com(("un espectador, Lalo, nos escribió", -.3), "Ugzjswg1zuqvW8-qwA54AaABAg", dur=5.8, x=.30, y=.30),
] + tarj(("Por eso los huevos gigantes pasaron", -.2), "o_huevo_gigante", "Huevo gigante", "de 1 oro a 15 platas", dur=4.4) + [
    rot(("porque todos lo sabían", -.3), "Porque todos lo sabían", sello="15", dur=2.8),
    pil([(Fc("tortuga_brillavalva"), "Tortugas"), (Fc("reptador_arena"), "Cangrejos"), (Fc("cria_lethlor"), "Crías"),
         (Fc("hiena_llagapata"), "Hienas")],
        ("Así que hoy hicimos lo contrario", .3), ("Y si también te los sabes", -.1),
        [("quince lugares que casi nadie", .35 * k) for k in range(4)], "casi nadie farmea", y=.56, tam=280),
    rot(("Y si también te los sabes", -.1), "¿Te los sabes todos? Avísanos", sello="?", dur=3.6),
    # =========================================================== P12 · TORTUGAS BRILLAVALVA (450-520 s)
    puesto(12, "TORTUGAS BRILLAVALVA", "tortuga_brillavalva", "Las Mil Agujas · El Desierto de Sal", [(30, 36, "30-36")],
           ("Número doce. Las tortugas", -.2), ("del treinta al treinta y seis|fin", .3),
           [("Número doce. Las tortugas", 0), "del treinta al treinta y seis"]),
    tarjc(("Y no, no son las tortugas", -.1), "tortuga_brillavalva", "Tortuga brillavalva", "Las Mil Agujas · 30-31", dur=4.0),
    pv(("Y no, no son las tortugas", .2), "desierto_sal", "El Desierto de Sal", dur=3.4, x=.23, y=.52, tam=440),
    rot(("es otra zona, otro nivel", -.2), "Otra zona, otro nivel, otro objeto", sello="!", dur=3.8),
    pv(("Son lentas, no pegan fuerte", -.2), "tortuga_brillavalva", "Tortuga brillavalva · lenta", dur=6.0, x=.19, y=.54, tam=460,
       marco="museo"),
    mg(O.probabilidad("FRAGMENTO DE CAPARAZÓN MOTEADO", Fc("tortuga_brillavalva"), F("o_fragmento_caparazon"), 3, [1], "1 DE CADA 3",
                      ancho=1000),
       ("Son lentas, no pegan fuerte", -.2), ("El vendedor te lo paga a nueve", -.1),
       ["y en un tercio de las muertes"], "un tercio", y=.50, x=.64),
] + tarj(("El vendedor te lo paga a nueve", -.1), "o_fragmento_caparazon", "Fragmento de caparazón moteado", "vendedor: 9 platas", dur=2.6) \
  + filav(("Además caen carne de tortuga", -.1), [("o_carne_tortuga", "Carne de tortuga", None),
                                                ("o_cola_escamosa", "Cola escamosa espesa", ("y cola escamosa espesa", -.1))],
          y=.62, tam=300, dur=3.0, xs=(.14, .33)) \
  + tarj(("la compra la gente para una", 0), "o_carne_tortuga", "Carne de tortuga", "para una misión de cocina", dur=3.6) + [
    rot(("y en la subasta vale más", -.3), "Carne de tortuga: mejor a la subasta", sello="+", dur=3.4),
    mg(O.cuenta("EN PROMEDIO", [(Fc("tortuga_brillavalva"), "Por tortuga", "4p"), ("txt:100", "Muertes por hora", "100")],
                ("De botín por hora", "4o", "+ MONEDAS"), op="×"),
       ("En promedio son unas cuatro", -.2), ("más las monedas|fin", .5),
       ["En promedio son unas cuatro", "A unas cien muertes por hora", "cuatro de oro de botín"], "4 platas × 100", y=.50),
    mapa("mil_agujas", [(82.7, 56.2, "Mordedores brillavalva", "34-35", "o_fragmento_caparazon"),
                        (78.8, 62.5, "Cráter de la Comadreja", None, "o_cola_escamosa"),
                        (80.4, 77.5, "Circuito del Espejismo", "vende (los dos bandos)", "o_oro")],
         ("Los mordedores brillavalva están al", -.2), ("ahí mismo|fin", .3),
         [("Los mordedores brillavalva están al", .3), "junto al Cráter de la Comadreja", "Y para vender, el Circuito"],
         "LAS MIL AGUJAS", "al este de las salinas"),
    rot(("Un jugador lo resumió así", 0), "Unas cuantas tardes = la montura", sello="!", dur=4.6),
    pv(("unas cuantas tardes de tortugas", -.3), "o_equitacion", "Y tienes la montura", dur=3.6, x=.76, y=.46, tam=340),
    mapa("marjal", [(58.4, 61.7, "Cavapozos Fangorroca", "42-43 · unas 6 platas por muerte", "o_almeja_boca_grande")],
         ("Y si ya vas por el cuarenta y dos", -.2), ("a unas seis platas por muerte|fin", .2),
         [("la alternativa son los cavapozos", .3)], "MARJAL REVOLCAFANGO", "la alternativa del 42"),
    ficha(12),
    # =========================================================== GRACIAS1 · Alexander, David, Rolazabal (520-552 s)
    rot(("Y gracias a quienes nos", 0), "Gracias a quienes nos escriben", sello="3", dur=3.4),
    com(("un espectador, Alexander, nos dice", -.3), "Ugzj9p4ZzYxYAc-nIF94AaABAg", dur=5.4, x=.30, y=.30),
    com(("Otro, David, está seguro", -.2), "Ugw-mIbw-5QI2sOeQKZ4AaABAg", dur=5.4, x=.68, y=.34),
    com(("Y para otro, Rolazabal", -.2), "UgxK9QrEiweimquO5nx4AaABAg", dur=5.0, x=.32, y=.34),
    rot(("Todos los comentarios se leen", -.1), "Todos los comentarios se leen", sello="!", dur=4.0),
    pv(("Y si este te está sirviendo", -.1), "o_molleja_buitre", "Lo que viene paga más", dur=3.8, x=.76, y=.46, tam=320),
    # =========================================================== P11 · REPTADORES DE ARENA (552-617 s)
    puesto(11, "REPTADORES DE ARENA", "reptador_arena", "Claros del Río · la zona nueva", [(36, 41, "36-41")],
           ("Número once. Los reptadores", -.2), ("del treinta y seis al cuarenta y uno|fin", .3),
           [("Número once. Los reptadores", 0), "del treinta y seis al cuarenta y uno"]),
    mapa("riverglades", [(71.6, 67.5, "Reptadores de arena", "36-37 · la costa", "o_carne_cangrejo"),
                         (78.9, 55.2, "Puerto Polvomecha", "vende (los dos bandos)", "o_oro")],
         ("Son los cangrejos de la", -.2), ("Y sueltan carne de cangrejo", .1),
         ["Son los cangrejos de la", "al sur del Puerto Polvomecha"], "CLAROS DEL RÍO", "al sur del Puerto Polvomecha"),
    mg(O.probabilidad("CARNE DE CANGREJO TIERNA", Fc("reptador_arena"), F("o_carne_cangrejo"), 10, [1, 4, 6, 9], "4 DE CADA 10"),
       ("Y sueltan carne de cangrejo", .1), ("El vendedor te paga poco más", .5),
       [("Y sueltan carne de cangrejo", .5)], "4 de 10 cangrejos", y=.50),
    mg(O.etiquetas("¿VENDEDOR O SUBASTA?", F("o_carne_cangrejo"), "Carne de cangrejo tierna", ("VENDEDOR", "1p 12c"), ("SUBASTA", "14p"),
                   (1, "NO AL VENDEDOR"), "Subasta: precio del 12 de noviembre"),
       ("El vendedor te paga poco más", .5), ("Así que esta no va al vendedor|fin", .3),
       [("El vendedor te paga poco más", .7), "se vendía a catorce platas", "Así que esta no va al"], "cangrejo vendedor/subasta", y=.50),
] + tarj(("La compran los cocineros, que", -.1), "o_carne_cangrejo", "Carne de cangrejo tierna", "la compran los cocineros", dur=4.2) + [
    pv(("pasar la tarde en la playa", -.6), "claros_del_rio", "La playa de Claros del Río", dur=3.2, x=.15, y=.58, tam=360),
    rot(("Y si tienes la cocina en", -.1), "Cocina 200: guísala tú", sello="200", dur=3.6),
    pv(("unas veinticinco platas por cada guiso", -.4), "o_oro", "Unas 25 platas por guiso", dur=3.4, x=.76, y=.46, tam=320),
    mapa("riverglades", [(79.0, 54.2, "Fimbo Grasapuños", "misión: Sabores de mar", "fimbo")],
         ("De paso, en el mismo puerto", -.2), ("pide carne de reptador de arena", -.3),
         [("hay una misión con estos cangrejos", .2)], "CLAROS DEL RÍO", "Puerto Polvomecha"),
] + filav(("pide carne de reptador de arena", -.2), [("o_carne_reptador", "Carne de reptador de arena", None),
                                                    ("o_ojo_murloc", "Ojo de múrloc marino", ("y ojos de múrloc", -.2))],
          y=.62, tam=300, dur=3.6, xs=(.14, .33)) + [
    mapa("tuercespina", [(33.6, 76.3, "Reptadores de las arenas del sur", "40-41 · almejas", "o_almeja_boca_grande"),
                         (27.2, 75.6, "Bahía del Botín", None, "bahia_botin")],
         ("los reptadores del sur de Tuercespina", -.5), ("sueltan además almejas de boca", .1),
         ["los reptadores del sur de Tuercespina", "cerca de Bahía del Botín"], "VEGA DE TUERCESPINA", "si ya vas por el 40",
         estilo="original"),
] + tarj(("sueltan además almejas de boca", .1), "o_almeja_boca_grande", "Almeja de boca grande", "dentro hay perlas", dur=4.2) + [
    pv(("Y dentro de las almejas hay", -.5), "o_perla_oro", "Perlas", dur=2.8, x=.17, y=.62),
    ficha(11),
    # =========================================================== P10 · CRÍAS DEL BARRANCO LETHLOR (617-685 s)
    puesto(10, "CRÍAS DEL BARRANCO LETHLOR", "cria_lethlor", "Tierras Inhóspitas", [(40, 44, "40-44")],
           ("Número diez. Las crías del", -.2), ("del cuarenta al cuarenta y cuatro|fin", .3),
           [("Número diez. Las crías del", 0), "del cuarenta al cuarenta y cuatro"]),
    mapa("inhospitas", [(82.5, 32.2, "Crías del Barranco Lethlor", "41-43", "o_glandula_llamas"),
                        (79.2, 53.9, "Barranco Lethlor", None, "barranco_lethlor"),
                        (77.7, 62.8, "Crías del Barranco Lethlor", "también al sur", "o_vastago_oscuro")],
         ("Son crías de dragón que escupen", -.2), ("también sueltan monedas|fin", .2),
         ["Son crías de dragón que escupen", "al este de la zona, alrededor", "alrededor del barranco"], "TIERRAS INHÓSPITAS",
         "al este de la zona"),
] + tarj(("Sueltan la glándula de llamas", -.1), "o_glandula_llamas", "Glándula de llamas pequeña", "va en el ají aliento de dragón", dur=4.0) + [
    pv(("que va en el ají aliento", -.1), "o_aji_aliento", "Ají aliento de dragón", dur=4.2, x=.17, y=.55),
    rot(("muy usada en mazmorras", -.8), "Escupes fuego: muy usada en mazmorras", sello="!", dur=3.0),
    mg(O.etiquetas("¿VENDEDOR O SUBASTA?", F("o_glandula_llamas"), "Glándula de llamas pequeña", ("VENDEDOR", "2p 50c"), ("SUBASTA", "~10p"),
                   (1, "A LA SUBASTA"), "En la subasta llegó a valer unas 10 platas"),
       ("El vendedor te paga la glándula", -.2), ("llegó a valer unas diez|fin", .5),
       ["El vendedor te paga la glándula", "En la subasta llegó a valer", ("llegó a valer unas diez|fin", 0)], "glándula", y=.50),
] + tarj(("Y sueltan una mascota, el Vástago", -.1), "o_vastago_oscuro", "Vástago oscuro", "mascota · te sigue a todas partes", dur=4.6) + [
    pv(("una cría de dragón negro", -.2), Fc("cria_lethlor"), "Cría de dragón negro", dur=3.6, x=.17, y=.56, tam=420),
    rot(("El vendedor la paga a veinticinco", -.1), "Vendedor: 25 platas · la subasta, más", sello="25", dur=4.2),
] + tarj(("una misión pide el corazón de", -.2), "o_corazon_draco", "Corazón de draco negro", "cae muy poco", dur=3.0) + [
    mg(M.contadores("UN SOLO CORAZÓN DE DRACO NEGRO", [("inv_misc_organ_01", "crías muertas", 100, 0, 1)], ("MÁS DE 100", 2), ancho=1200),
       ("hay gente que mata más de", -.2), ("por un solo corazón|fin", .6),
       ["hay gente que mata más de", ("por un solo corazón|fin", -.3), ("por un solo corazón|fin", 0)], "100 crías", y=.52),
    mapa("inhospitas", [(82.5, 32.2, "Crías del Barranco Lethlor", "unos 30 000 de experiencia por hora", "cria_lethlor"),
                        (78.2, 46.2, "Vetas de mitril", "16 puntos en el este", "o_mena_mitril")],
         ("Y a un jugador le daban", -.2), ("con vetas de mitril alrededor|fin", .3),
         ["unos treinta mil puntos de experiencia", "con vetas de mitril alrededor"], "TIERRAS INHÓSPITAS", "oro y nivel a la vez"),
    rot(("Cuidado con los élites en", 0), "Élites en el centro: farmea los bordes", sello="!", dur=4.4),
    pv(("Cuidado con los élites en", .2), "barranco_lethlor", "Barranco Lethlor", dur=4.0, x=.73, y=.44, tam=480),
    ficha(10),
    # =========================================================== BURLA1 · Pkponcho (685-705 s)
    rot(("Y otro comentario. Un espectador", 0), "Otro comentario", sello="!", dur=2.8),
    com(("Un espectador, Pkponcho, nos escribió", -.3), "UgzeWmdKd0l3LgErJVB4AaABAg", dur=6.2, x=.30, y=.30),
    mg(M.contadores("CRÍTICAS CONTESTADAS EN ESTE VIDEO", [("inv_misc_note_02", "contestadas", 2, 0, 1)], ("TÚ ERES EL SEGUNDO", 2),
                    ancho=1200),
       ("en este video solo le contestamos", -.3), ("Tú eres el segundo|fin", .8),
       ["en este video solo le contestamos", "a dos. Tú eres", "Tú eres el segundo"], "críticas 2", y=.52),
    # =========================================================== P09 · MÚRLOCS DEL PANTANO (705-785 s)
    puesto(9, "MÚRLOCS DEL PANTANO", "murloc_marisma", "Pantano de las Penas", [(41, 45, "41-45")],
           ("Número nueve. Los múrlocs del", -.2), ("del cuarenta y uno al cuarenta y cinco|fin", .3),
           [("Número nueve. Los múrlocs del", 0), "del cuarenta y uno al cuarenta y cinco"]),
    mapa("pantano", [(82.4, 92.1, "Múrlocs de marisma", "la playa · 41-42", "o_almeja_boca_grande"),
                     (62.7, 87.2, "Oráculos y comecarnes", "grupo grande · 43-45", "o_receta_te_soleado"),
                     (66.1, 77.3, "Cueva Stagalbog", None, "o_perla_negra")],
         ("Hay cuatro tipos en la", -.2), ("múrlocs de marisma, vomitatintas", -.2),
         ["en la mitad sur de la", "y un grupo grande hacia", "hacia la Cueva Stagalbog"], "PANTANO DE LAS PENAS", "la playa del sur"),
] + [pv(("múrlocs de marisma, vomitatintas", -.2 + o), Fc(c), t, dur=4.4 - o, x=x, y=.60, tam=280)      # entran con la voz, se van juntos
       for o, c, t, x in ((0, "murloc_marisma", "Múrloc de marisma", .12), (.6, "vomitatintas_marisma", "Vomitatintas", .29),
                          (1.2, "comecarnes_marisma", "Comecarnes", .46), (1.7, "oraculo_marisma", "Oráculo", .63))] \
  + tarj(("Todos pueden soltar la almeja", .3), "o_almeja_boca_grande", "Almeja de boca grande", "se abre", dur=2.6) \
  + filav(("Al abrirla siempre salen de", .5), [("o_carne_almeja", "1 a 3 carnes de almeja sabrosa", None, dict(salida="funde")),
                                              ("o_perla_oro", "A veces, una perla", None)],
          y=.62, tam=300, dur=3.6, xs=(.14, .36)) \
  + tarj(("La perla buena es la perla", -.1), "o_perla_oro", "Perla de oro", "la perla buena", dur=3.2) + [
    pv(("La perla buena es la perla", .1), "o_perla_oro", "Perla de oro", dur=3.0, x=.17, y=.58, tam=340),
    mg(O.etiquetas("¿SUBASTA O VENDEDOR?", F("o_perla_oro"), "Perla de oro", ("SUBASTA", "1o 30p"), ("VENDEDOR", "1o"),
                   (0, "A LA SUBASTA"), "Subasta: 22 de noviembre"),
       ("un jugador la vendía a un", -.3), ("El vendedor solo te da un oro|fin", .4),
       [("un jugador la vendía a un", 0), "El vendedor solo te da un", ("El vendedor solo te da un oro|fin", 0)], "perla de oro", y=.50),
] + filav(("Las demás perlas valen menos", -.1), [("o_perla_negra", "Perla negra · unas 12 platas", ("la negra unas doce platas", -.2), dict(entrada="pop")),
                                             ("o_perla_iridiscente", "Perla iridiscente · unas 8", ("y la iridiscente unas ocho", -.2))],
          y=.58, tam=300, dur=3.6, xs=(.13, .40)) + [
    rot(("Pero se van sumando", -.2), "Pero se van sumando", sello="+", dur=2.6),
    E.ficha_e("Y ADEMÁS", ["inv_misc_coin_02", "o_serviola", "o_aceite_pescado"],
              ("Además sueltan monedas, serviola", 0), ("ligados al equiparse|fin", .4),
              ["Además sueltan monedas, serviola", "serviola moteada cruda, aceite", "aceite de pescado, y verdes"],
              etiquetas=["monedas", "serviola", "aceite"]),
    rot(("A ese jugador le cayeron", -.1), "Unas botas épicas: unos 13 de oro", sello="13", dur=4.6),
] + tarj(("Y los oráculos sueltan una receta", -.1), "o_receta_te_soleado", "Receta: té soleado", "nueva de Forever · cocina 200", dur=4.4) + [
    pv(("Y los oráculos sueltan una receta", .3), Fc("oraculo_marisma"), "Oráculo de marisma", dur=3.8, x=.17, y=.59, tam=400),
    pv(("Y la carne de almeja no", -.1), "o_carne_almeja", "Carne de almeja · no la tires", dur=3.6, x=.17, y=.62),
    tar(("desde el veintitrés de noviembre, sus", -.2), "Revisión del 23 de noviembre", "o_carne_almeja",
        ["Recetas con carne de almeja", dict(t="Cuentan como comida de aguante", c=V)], dur=5.0),
    mapa("pantano", [(81.5, 80.7, "Puesto Juncobruma", "empieza aquí al 40", "o_carne_almeja"),
                     (66.1, 77.3, "Cueva Stagalbog", "mejor más tarde: demasiados juntos", "o_perla_negra")],
         ("Empieza por la playa al cuarenta", -.2), ("que ahí hay demasiados juntos|fin", .2),
         ["junto al Puesto Juncobruma", "La parte de la cueva, mejor"], "PANTANO DE LAS PENAS", "por dónde empezar"),
    ficha(9),
    # =========================================================== P08 · HIENAS LLAGAPATA (785-860 s)
    puesto(8, "HIENAS LLAGAPATA", "hiena_llagapata", "Tanaris · Arenas Abisales", [(44, 46, "44-46")],
           ("Número ocho. Las hienas Llagapata", -.2), ("del cuarenta y cuatro al cuarenta y seis|fin", .3),
           [("Número ocho. Las hienas Llagapata", 0), "del cuarenta y cuatro al cuarenta y seis"]),
    mapa("tanaris", [(47.5, 36.9, "Rocs de fuego", "de misión · 43-45", "roc_fuego"),
                     (44.4, 38.7, "Hienas Llagapata", "44-45 · casi nadie las mata", "o_melena_espesa")],
         ("En las Arenas Abisales hay tantos", -.2), ("Y casi nadie mata a las hienas|fin", .3),
         ["hay tantos rocs de fuego", "como hienas"], "TANARIS", "las Arenas Abisales"),
] + tarj(("Sueltan la melena espesa, a ocho", -.1), "o_melena_espesa", "Melena espesa", "vendedor: 8 platas", dur=3.2) \
  + tarj(("y la pata de trofeo grande", .2), "o_pata_trofeo", "Pata de trofeo grande", "vendedor: 9 platas", dur=3.2) \
  + filav(("Además, cuero grueso, carne de", -.1), [("o_cuero_grueso", "Cuero grueso", None),
                                               ("o_carne_lobo_rojo", "Carne de lobo rojo", ("carne de lobo rojo y carne", 0)),
                                               ("o_carne_lobo_tierna", "Carne de lobo tierna", ("y carne de lobo tierna", 0))],
          y=.62, tam=280, dur=3.8, xs=(.12, .29, .46)) + [
    mg(O.etiquetas("¿SUBASTA O VENDEDOR?", F("o_carne_lobo_tierna"), "Carne de lobo tierna", ("SUBASTA", "casi 1o el montón"),
                   ("VENDEDOR", "17p"), (0, "A LA SUBASTA"), "Subasta: 23 de noviembre · la piden las guías de cocina"),
       ("Un jugador la vendía a casi", -.3), ("solo te da diecisiete platas|fin", .5),
       ["Un jugador la vendía a casi", "solo te da diecisiete platas", ("solo te da diecisiete platas|fin", 0)], "carne de lobo", y=.50),
] + flow("esqueletos_tanaris", ("La ruta es un triángulo por", -.2), ("Y si pasa un roc, mátalo", .1)) + [
    tarjc(("Y si pasa un roc, mátalo", -.1), "roc_fuego", "Roc de fuego", "suelta huevos gigantes", dur=4.2),
    pv(("que suelta huevos gigantes", -.3), "o_huevo_gigante", "Huevo gigante", dur=3.0, x=.17, y=.62),
    rot(("Ese mismo día, los huevos valían", 0), "Huevo gigante: poco más de 20 platas", sello="20", dur=4.4),
    pv(("Ya no es el farmeo de", -.1), Fc("roc"), "Pero de paso suma", dur=3.0, x=.76, y=.46, tam=400),
    mapa("tanaris", [(44.4, 38.7, "Arenas Abisales", "las dunas", "o_melena_espesa"),
                     (51.2, 27.5, "Gadgetzan", "neutral: los dos bandos", "o_oro")],
         ("Para vender, Gadgetzan, al norte", -.2), ("neutral para los dos bandos|fin", .3),
         [("Para vender, Gadgetzan, al norte", .3), "al norte de las dunas"], "TANARIS", "a vender"),
    mapa("mundo", [(26.7, 64.6, "Hienas · Tanaris", "melena espesa", "o_melena_espesa"),
                   (91.6, 62.1, "Coyotes · Claros del Río", "el número 4 · también la sueltan", "o_melena_espesa")],
         ("Y la melena espesa también la", -.2), ("ya sabes dónde más buscarla|fin", .1),
         ["Y la melena espesa también", "los coyotes del número cuatro"], "AZEROTH", "dónde más buscar la melena espesa", zmax=1.2),
    ficha(8),
    # =========================================================== GRACIAS2 · Lunatic, BiNWinslou (860-882 s)
    rot(("Y gracias también a Brasil", 0), "Gracias también a Brasil", sello="BR", dur=3.4),
    com(("un espectador, Lunatic, nos escribió", -.3), "UgxbfnjIWM1Jg6HlhPx4AaABAg", dur=5.8, x=.30, y=.30),
    com(("Y otro espectador, BiNWinslou", -.2), "UgzIW7D7uUzAMj4HC7h4AaABAg", dur=5.6, x=.66, y=.32),
    # =========================================================== P07 · GORILAS Y OSOS DE FERALAS (882-945 s)
    puesto(7, "GORILAS Y OSOS DE FERALAS", "tronador_groddoc", "norte de Feralas", [(47, 50, "47-50")],
           ("Número siete. Los gorilas y", -.2), ("del cuarenta y siete al cincuenta|fin", .3),
           [("Número siete. Los gorilas y", 0), "del cuarenta y siete al cincuenta"]),
    mapa("feralas", [(42.1, 21.9, "Tronadores Groddoc", "49-50 · Los Dos Colosos", "o_mechon_gorila"),
                     (47.8, 27.3, "Patriarcas Cueracero", "48-49", "o_hueso_oso")],
         ("Tronadores Groddoc y patriarcas Cueracero", -.2), ("alrededor de Los Dos Colosos|fin", .3),
         [("Tronadores Groddoc y patriarcas", .2), "y patriarcas Cueracero, en la"], "FERALAS", "alrededor de Los Dos Colosos"),
    rot(("Aquí no hace falta ninguna", 0), "Sin profesión: grises que paga el vendedor", sello="0", dur=4.6),
    tarjc(("Aquí no hace falta ninguna", .2), "tronador_groddoc", "Tronador Groddoc", "gorila · 49-50", dur=4.6),
    pv(("porque los grises que sueltan", -.2), Fc("patriarca_cueracero"), "Patriarca Cueracero", dur=3.4, x=.17, y=.50, tam=400, entrada="pop", salida="funde"),
] + tarj(("El hueso de oso grande, casi", -.1), "o_hueso_oso", "Hueso de oso grande", "casi 15 platas · ¡y es una maza!", dur=4.6) + [
    E.ficha_e("LOS GRISES DEL VENDEDOR", ["o_hueso_oso", "o_mechon_gorila", "o_mandibula_oso"],
              ("El mechón de pelo de gorila", -.3), ("La mandíbula de oso, casi nueve|fin", .5),
              [("El mechón de pelo de gorila", -.2), "El mechón de pelo de gorila", "La mandíbula de oso, casi"],
              etiquetas=["casi 15 p", "+11 p", "casi 9 p"]),
] + filav(("Y luego el pelo de gorila", -.1), [("o_pelo_gorila_burdo", "Pelo de gorila burdo", None, dict(entrada="pop", salida="funde")),
                                            ("o_garra_oso", "Garra de oso indómito", ("la garra de oso indómito", -.1)),
                                            ("o_costillar_oso", "Costillar de oso", ("y el costillar de oso", -.1))],
          y=.60, tam=240, dur=4.4, xs=(.115, .30, .50)) + [
    rot(("de cinco a seis platas cada", -.3), "De 5 a 6 platas cada uno", sello="6", dur=3.4),
    pv(("de la misión previa al Templo", -.3), "templo_sumergido", "Templo Sumergido", dur=4.2, x=.30, y=.44, tam=500),
    rot(("cuando hay gente haciéndola, reaparecen", -.2), "Con gente en la misión: reaparecen más rápido", sello="!", dur=3.8),
    mapa("feralas", [(57.8, 56.8, "Simios y osos del centro", "41-43 · sueltan casi lo mismo", "oso_cueracero")],
         ("Si vas por el cuarenta y uno", -.2), ("a menos nivel|fin", .3),
         [("los simios Groddoc y los", .2)], "FERALAS", "la opción del 41"),
    mapa("feralas", [(75.2, 43.8, "Campamento Mojache", "vende la Horda", "o_oro"),
                     (31.1, 44.6, "Bastión Plumaluna", "vende la Alianza", "o_oro")],
         ("La Horda vende en el Campamento", -.2), ("en el Bastión Plumaluna|fin", .3),
         ["en el Campamento Mojache, y", "y la Alianza en el Bastión"], "FERALAS", "a vender"),
    ficha(7),
    # =========================================================== P06 · JAGUARES DEL PANTANO (945-1002 s)
    puesto(6, "JAGUARES DEL PANTANO", "jaguar_pantano", "Pantano de las Penas", [(36, 39, "36-39")],
           ("Número seis. Los jaguares del", -.2), ("del treinta y seis al treinta y nueve|fin", .2),
           [("Número seis. Los jaguares del", 0), "del treinta y seis al treinta y nueve"]),
    rot(("Probablemente el farmeo de montura", 0), "El farmeo de montura más famoso", sello="1", dur=3.8),
    pv(("Sueltan colas y bigotes de felino", -.1), Fc("jaguar_pantano"), "Jaguar del pantano", dur=3.4, x=.17, y=.56, tam=420),
] + tarj(("la cola blanda larga, a ocho", -.1), "o_cola_blanda", "Cola blanda larga", "vendedor: 8 platas", dur=2.5) \
  + tarj(("y el bigote de cerdas, a", -.1), "o_bigote_cerdas", "Bigote de cerdas", "vendedor: más de 7 platas", dur=3.2) + [
    pv(("Y además, cuero y carne", -.1), "o_cuero_pesado", "Cuero y carne", dur=3.0, x=.17, y=.62),
    rot(("Con desuello rinde más", 0), "Con desuello rinde más", sello="+", dur=3.2),
    pv(("Con desuello rinde más", .3), "o_ico_desuello", "Desuello", dur=3.2, x=.76, y=.46, tam=320),
    pv(("hay quien aprovecha para subir la", -.3), "o_ico_herboristeria", "Y herboristería al mismo tiempo", dur=3.8, x=.17, y=.60),
    mapa("pantano", [(42.2, 42.4, "Jaguares del pantano", "36-37", "o_cola_blanda"),
                     (46.0, 53.8, "Rocal", "vende y vuela la Horda", "o_oro")],
         ("La Horda vende en Rocal", -.2), ("Y un aviso para la Alianza", .3),
         [("La Horda vende en Rocal", .1), "en Rocal, en medio del"], "PANTANO DE LAS PENAS", "a vender"),
    pant("rocal", ("por ahí patrullan guardias de", -.3), ("el combate entre jugadores|fin", .3), zoom=(1.0, 1.10)),
    rot(("Y un aviso para la Alianza", .3), "Alianza: guardias de la Horda te marcan JcJ", sello="!", dur=4.8),
    mapa("riverglades", [(58.7, 52.8, "Cazadoras llanagreste", "38-39 · sueltan lo mismo", "cazadora_llanagreste"),
                         (59.6, 45.9, "Rog'mar", "vende y vuela la Horda", "o_oro")],
         ("Si hay mucha gente, tienes el", -.2), ("sueltan lo mismo|fin", .3),
         ["las cazadoras llanagreste, al sur", "al sur de Rog'mar"], "CLAROS DEL RÍO", "el plan B"),
    tabla([T_JAG, T_GOR, T_CENT], 0, ("A un jugador le dejaban justo", -.2), ("vas a la otra|fin", .1),
          ("justo por encima de diez", 0)),
    ficha(6),
    # =========================================================== P05 · ELEMENTALES DE ROCA (1002-1082 s)
    puesto(5, "ELEMENTALES DE ROCA", "elemental_roca", "Tierras Inhóspitas", [(37, 44, "37-44")],
           ("Número cinco. Los elementales de", -.2), ("del treinta y siete al cuarenta y cuatro|fin", .3),
           [("Número cinco. Los elementales de", 0), "del treinta y siete al cuarenta y cuatro"]),
    rot(("El clásico de siempre para", 0), "El clásico de siempre para la montura", sello="!", dur=3.6),
    tar(("desde el trece de noviembre, los", -.2), "Revisión del 13 de noviembre", "inv_misc_note_02",
        ["Tierras Inhóspitas", dict(t="Más elementales de roca inferiores", c=V)], dur=5.2),
    pv(("los elementales de roca inferiores aparecen", -.2), Fc("elemental_roca_inferior"), "Elemental de roca inferior", dur=3.6,
       x=.17, y=.56, tam=420),
    mapa("inhospitas", [(17.6, 41.9, "Elementales inferiores", "37-39", "o_piedra_inerte"),
                        (4.3, 47.4, "Kargath", None, "kargath"),
                        (43.1, 82.4, "Elementales de roca", "al sur · Explanada del Espejismo", "o_tierra_elemental"),
                        (2.8, 82.0, "Elementales superiores", "del 42 · al suroeste", "o_sal_roca")],
         ("Hay tres franjas. Los inferiores", -.2), ("al suroeste|fin", .4),
         [("Los inferiores, del treinta y siete", .2), "junto a Kargath. Los normales", "Los normales, al sur, junto",
          "Y los superiores, del cuarenta"], "TIERRAS INHÓSPITAS", "tres franjas"),
    E.ficha_e("GRISES DE PIEDRA", ["o_piedra_lisa", "o_piedra_dentada", "o_piedra_inerte", "o_sal_roca"],
              ("Sueltan grises de piedra que", -.2), ("piedra inerte y sal de roca|fin", .6),
              ["trozos de piedra lisa y", "y dentada, piedra inerte", ("piedra inerte y sal de", 0), "y sal de roca"],
              etiquetas=["5 p 30 c", "4 p 11 c", "3 p 60 c", "2 p 50 c"]),
    mg(O.probabilidad("TIERRA ELEMENTAL", Fc("elemental_roca"), F("o_tierra_elemental"), 10, [6], "1 DE CADA 10"),
       ("Y tierra elemental, en una", -.2), ("cuando empiezan las bandas, la", -.3),
       [("Y tierra elemental, en una", .3)], "1 de 10 tierra", y=.50),
] + tarj(("cuando empiezan las bandas, la", -.2), "o_tierra_elemental", "Tierra elemental", "la piden las bandas", dur=4.6) + [
    tabla([T_JAG, T_ELE, T_GOR, T_CENT], 1, ("A un jugador le salían unos", -.2), ("solo en grises|fin", .6),
          ("unos diez de oro por hora", 0)),
    rot(("Otro dijo que con ellos", 0), "«Te garantizas la montura»", sello="!", dur=4.4),
    pv(("te garantizas la montura", -.2), "o_equitacion", "La montura", dur=3.4, x=.76, y=.46, tam=340),
    mapa("inhospitas", [(4.3, 47.4, "Kargath", "vende y vuela la Horda", "o_oro"),
                        (42.4, 52.6, "El centro de la zona", "vende la Alianza", "o_oro")],
         ("Para vender, la Horda tiene a", -.2), ("los campamentos goblin del centro|fin", .3),
         ["la Horda tiene a Kargath", "Y la Alianza, los campamentos"], "TIERRAS INHÓSPITAS", "a vender"),
    pv(("guarda la tierra elemental en el", -.2), "o_tierra_elemental", "Al banco", dur=3.4, x=.17, y=.62),
    rot(("Y el nueve de diciembre, mira", -.1), "9 de diciembre: mira su precio", sello="9", dur=3.2),
    ficha(5),
    # =========================================================== P04 · COYOTES DE CLAROS DEL RÍO (1082-1152 s)
    puesto(4, "COYOTES DE CLAROS DEL RÍO", "coyote_llanuras", "Claros del Río · la zona nueva", [(36, 40, "36-40")],
           ("Número cuatro. Los coyotes de", -.2), ("Los coyotes de Claros del Río, del treinta y seis al cuarenta|fin", .3),
           [("Número cuatro. Los coyotes de", 0), ("Los coyotes de Claros del Río, del", 1.0)]),
    mapa("riverglades", [(54.8, 75.8, "Cortijo de Wheeler", "Benjy Wheeler", "benjy_wheeler"),
                         (54.5, 86.9, "Coyotes de las llanuras", "siempre unos 4 vivos", "o_cola_tupida")],
         ("Están al sur del Cortijo de", -.2), ("y ya volvieron|fin", .2),
         [("Están al sur del Cortijo de", .3), "Y reaparecen a lo loco"], "CLAROS DEL RÍO", "al sur del Cortijo de Wheeler"),
    pv(("Sueltan la cola tupida suave", .2), Fc("coyote_llanuras"), "Coyote de las llanuras", dur=3.4, x=.15, y=.56, tam=330, marco="polaroid"),
] + tarj(("Sueltan la cola tupida suave", -.1), "o_cola_tupida", "Cola tupida suave", "vendedor: más de 7 platas", dur=3.2) \
  + tarj(("y la melena espesa, a ocho", -.1), "o_melena_espesa", "Melena espesa", "vendedor: 8 platas", dur=3.0) \
  + filav(("Además, colmillos, carne de lobo", -.1), [("o_colmillo_grande", "Colmillos", None),
                                                   ("o_carne_lobo_rojo", "Carne de lobo rojo", ("carne de lobo rojo y cuero", 0)),
                                                   ("o_cuero_pesado", "Cuero", ("y cuero|fin", -.4))],
          y=.62, tam=280, dur=3.6, xs=(.12, .29, .46)) + [
    pv(("Y la cola tupida suave tiene", -.1), "o_cola_tupida", "Segundo comprador", dur=3.4, x=.76, y=.46, tam=340),
    rot(("es uno de los objetos que", -.2), "Se canjea en la Feria de la Luna Negra", sello="2", dur=4.2),
    mg(O.cronometro("COYOTES DE CLAROS DEL RÍO · CON CRONÓMETRO", F("o_cola_tupida"), 30, "6o 84p",
                    ("inv_misc_pocketwatch_01", "Media hora, el 20 de noviembre"), "13-14o/h"),
       ("Un jugador lo midió con cronómetro", -.2), ("Entre trece y catorce de oro por hora|fin", .4),
       ["Un jugador lo midió con cronómetro", "seis de oro con ochenta y", "Entre trece y catorce de oro"], "cronómetro coyotes", y=.50),
    tabla([T_COY, T_JAG, T_ELE, T_GOR, T_CENT], 0, ("Era el jugador del treinta y", -.2), ("de los que más le dieron|fin", .3),
          ("Y de los farmeos que probó", 0)),
    mapa("riverglades", [(54.2, 84.0, "Sootfur", "coyote con nombre · 38", "sootfur"),
                         (54.8, 75.8, "Benjy Wheeler", "el granjero · su misión", "benjy_wheeler")],
         ("Hay un coyote con nombre", -.2), ("con el botín libre|fin", .3),
         ["Hay un coyote con nombre, Sootfur", "de una misión de Benjy"], "CLAROS DEL RÍO", "en grupo, con el botín libre"),
    mapa("mundo", [(91.6, 62.1, "Coyotes · Claros del Río", "36-40", "o_cola_tupida"),
                   (85.9, 48.6, "Elementales · Tierras Inhóspitas", "el número 5", "o_piedra_inerte")],
         ("Y desde ahí pasas directo a", -.2), ("a los elementales del número cinco|fin", .1),
         ["Y desde ahí pasas directo", "a los elementales del número"], "AZEROTH", "de Claros del Río a Tierras Inhóspitas", zmax=1.3),
    ficha(4),
    # =========================================================== P03 · PESCA DE VALIJAS (1152-1245 s)
    puesto(3, "PESCA DE VALIJAS", F("o_valija_mitril"), "la costa de Tuercespina", [(30, 50, "cualquier nivel")],
           ("Número tres. La pesca de", -.2), ("en la costa de Tuercespina|fin", .6),
           [("Número tres. La pesca de", 0), "en la costa de Tuercespina"]),
    rot(("ya hablamos de pescar en", -.4), "Ya lo contamos, pero cambió", sello="!", dur=4.2),
] + tarj(("Pero desde entonces cambiaron dos", -.1), "o_valija_mitril", "Valija reforzada con mitril", "dos cosas cambiaron", dur=4.6) \
  + flow("restos_flotantes", ("Las valijas reforzadas con mitril salen", -.2), ("y también de los bancos de", .1)) + [
    mapa("tuercespina", [(27.1, 42.9, "Anguila escama pétrea", "5 bancos", "o_anguila_petrea"),
                         (23.3, 57.2, "Anguila escama pétrea", "5 bancos", "o_anguila_petrea"),
                         (27.4, 83.4, "Anguila escama pétrea", "8 bancos", "o_anguila_petrea")],
         ("y también de los bancos de", .1), ("Dentro hay tejido mágico, cuero", .2),
         [("los bancos de anguila escama", .1), ("de anguila escama pétrea", .1), ("de anguila escama pétrea|fin", -.1)],
         "VEGA DE TUERCESPINA", "bancos de anguila escama pétrea"),
    E.ficha_e("DENTRO DE CADA VALIJA", ["o_tejido_magico", "o_cuero_grueso", "o_pano_runico", "inv_scroll_03"],
              ("Dentro hay tejido mágico, cuero", .2), ("bolsas de catorce casillas|fin", .4),
              [("Dentro hay tejido mágico, cuero", .4), "cuero, paño rúnico, objetos", "paño rúnico, objetos verdes", "alguna receta, y hasta"],
              etiquetas=["tejido mágico", "cuero", "paño rúnico", "recetas"]),
] + tarj(("el Maestro del cebo. Con", -.4), "o_luremaster", "Maestro del cebo", "talento de Legado · 2 rangos", dur=5.2) + [
    pv(("cada pez que sacas con señuelo", -.2), "o_adornos_brillantes", "Con señuelo", dur=3.2, x=.17, y=.54),
    rot(("tiene la mitad de probabilidad", -.2), "50 %: un pez extra · también valijas", sello="50", dur=4.2),
] + flow("cuatro_valijas", "scene-140", "scene-140:fin") + [
    rot(("Unos cuatro de oro por", -.1), "Unos 4 de oro por sacar un pez", sello="4", dur=2.6),
    mg(O.columnas("VALIJAS POR HORA", F("o_valija_mitril"), [("Sin el talento", 15, None), ("Con el Maestro del cebo", 40, None)],
                  "Cada valija: unas 70 platas de media"),
       ("Sin el talento sacaba unas quince", -.2), ("unas setenta platas|fin", .5),
       ["Sin el talento sacaba unas quince", "Con él, unas cuarenta", "Y cada valija vale, en promedio"], "15 contra 40", y=.50),
    mg(M.contadores("RESULTADO", [("inv_misc_coin_01", "de oro en 3 horas y media", 170, 0, 1),
                                  ("trade_fishing", "pesca: del 150 al", 225, 2, 3)], None, ancho=1240),
       ("Resultado: ciento setenta de oro", -.2), ("al doscientos veinticinco|fin", .6),
       [("Resultado: ciento setenta de oro", .2), "en tres horas y media", "mientras subía la pesca", "al doscientos veinticinco"],
       "170 oro", y=.52),
    rot(("Dos detalles más. Desde el", 0), "Dos detalles más", sello="2", dur=3.0),
] + tarj(("el expositor de pesca del campamento", -.3), "o_expositor_pesca", "Expositor de pesca", "desde el 16-nov: señuelos para todos",
         dur=3.6) + [
    pv(("da señuelos a todos", -.3), "o_adornos_brillantes", "Señuelos para todos", dur=3.0, x=.17, y=.62),
] + tarj(("Y el jarabe de caminar sobre", -.1), "o_jarabe_agua", "Jarabe de caminar sobre el agua", "pescas lejos de la orilla", dur=4.4) + [
    mapa("tuercespina", [(31.9, 28.4, "Campamento Grom'Gol", "salida · buzón", "o_valija_mitril"),
                         (27.1, 42.9, "Costa oeste", "bancos de anguila", "o_anguila_petrea"),
                         (23.3, 57.2, "Costa oeste", None, "o_anguila_petrea"),
                         (27.2, 75.6, "Bahía del Botín", "y vuelves", "o_oro")],
         ("La ruta: sales del Campamento", -.2), ("y todo va al buzón|fin", .2),
         ["sales del Campamento Grom'Gol", "bajas por toda la costa oeste", ("bajas por toda la costa oeste", 1.4),
          "hasta Bahía del Botín, y"], "VEGA DE TUERCESPINA", "la ruta de las valijas"),
    ficha(3),
    # =========================================================== P02 · CUEVAS DE OGROS DE ALTERAC (1245-1327 s)
    puesto(2, "CUEVAS DE OGROS", "ogro_aplastacresta", "Montañas de Alterac", [(34, 38, "34-38")],
           ("Número dos. Las cuevas de", -.2), ("del treinta y cuatro al treinta y ocho|fin", .3),
           [("Número dos. Las cuevas de", 0), "del treinta y cuatro al treinta y ocho"]),
    mapa("alterac", [(51.2, 42.0, "Dominios de los Aplastacresta", "la fortaleza (élite)", "dominios_aplastacresta"),
                     (47.9, 34.2, "Cuenca de la Matanza", "la cueva del norte", "o_mena_mitril"),
                     (47.4, 61.6, "Ogros del sur", "34-35", "o_pano_seda")],
         ("Junto a los Dominios de los", -.2), ("una al norte y otra al sur|fin", .3),
         [("Junto a los Dominios de los", .3), "una al norte y otra", "y otra al sur"], "MONTAÑAS DE ALTERAC", "dos cuevas",
         estilo="original"),
] + flow("cueva_alterac_vetas", ("Y dentro hay vetas de hierro", -.2), ("que reaparecen rápido|fin", .3)) \
  + filav(("Y dentro hay vetas de hierro", 0), [("o_mena_hierro", "Hierro", None), ("o_mena_mitril", "Mitril", ("de mitril, de veraplata", 0)),
                                            ("o_mena_veraplata", "Veraplata", ("de veraplata, de oro", 0)),
                                            ("o_mena_oro", "Oro", ("de oro y de plata", 0)), ("o_mena_plata", "Plata", ("y de plata, que", 0))],
          y=.66, tam=210, dur=4.6, xs=(.12, .30, .48, .66, .84)) + [
    rot(("Con minería, aquí subes casi", -.1), "Con minería: casi hasta el torio", sello="!", dur=3.8),
    mapa("alterac", [(52.8, 47.1, "38 vetas", "en un solo rincón", "o_mena_oro")],
         ("En un solo rincón del mapa", -.2), ("once de oro, ocho", .4),
         [("En un solo rincón del mapa", .4)], "MONTAÑAS DE ALTERAC", "un solo rincón"),
    E.ficha_e("38 VETAS EN UN RINCÓN", ["o_mena_oro", "o_mena_hierro", "o_mena_plata", "o_mena_mitril", "o_mena_veraplata"],
              ("once de oro, ocho", .4), ("y seis de veraplata|fin", .8),
              [("once de oro, ocho", .6), "ocho de hierro, siete", "siete de plata, seis", "seis de mitril y", "y seis de veraplata"],
              cuentas=[11, 8, 7, 6, 6], total=38),
    pv(("Los ogros sueltan plata, paño", -.1), Fc("ogro_aplastacresta"), "Ogro Aplastacresta", dur=3.6, x=.17, y=.60, tam=400),
] + tarj(("paño de seda, grises y verdes", -.2), "o_pano_seda", "Paño de seda", "vendedor: 1 plata y media", dur=3.4) + [
    mapa("alterac", [(47.3, 35.3, "Rizz Tornillosuelto", "en una jaula · junto a la cueva del norte", "rizz")],
         ("Y no hace falta irse a", -.2), ("Rizz Tornillosuelto, encerrado", -.2),
         [("cerca de la cueva del norte", .2)], "MONTAÑAS DE ALTERAC", "un vendedor sin salir de la zona", estilo="original"),
] + flow("jaula_rizz", ("Rizz Tornillosuelto, encerrado", -.2), ("ronda un raro, Lo'Grosh", -.3)) + [
    pv(("ronda un raro, Lo'Grosh", -.2), Fc("lo_grosh"), "Lo'Grosh · raro", dur=4.4, x=.17, y=.64, tam=380, marco="polaroid", entrada="sello", salida="funde"),
] + tarj(("que suelta una maza, El", -.2), "o_pacificador", "El pacificador", "en la subasta vale mucho", dur=4.4) + [
    rot(("Un jugador encontró las cuevas", 0), "Cuevas vacías: ninguna guía manda ahí", sello="0", dur=4.2),
    tabla([T_ALT, T_COY, T_JAG, T_ELE, T_GOR], 0, ("Con minería, montura y botas", -.2), ("unos treinta de oro por hora|fin", .6),
          ("le salieron unos treinta de", 0)),
    rot(("Sin montura ni botas, de", 0), "Sin montura ni botas: de 20 a 25 por hora", sello="20", dur=3.6),
    mapa("alterac", [(46.3, 47.1, "Aplastadores y magos", "élite · no te acerques", "aplastador_aplastacresta"),
                     (47.9, 34.2, "Las cuevas", "quédate aquí", "o_mena_mitril")],
         ("Un aviso: cerca de la fortaleza", -.2), ("Quédate en las cuevas|fin", .2),
         ["cerca de la fortaleza están los", "Quédate en las cuevas"], "MONTAÑAS DE ALTERAC", "cuidado con los élites"),
    ficha(2),
    # =========================================================== P01 · DESTRIPADORES NEGROS (1327-1415 s)
    puesto(1, "DESTRIPADORES NEGROS", "destripador_negro", "Las Tierras Devastadas", [(46, 50, "46-50")],
           ("Y número uno. Los destripadores", -.2), ("del cuarenta y seis al cincuenta|fin", .3),
           [("Y número uno. Los destripadores", 0), "del cuarenta y seis al cincuenta"]),
    mapa("devastadas", [(48.0, 29.1, "Alto de los Rapiñadores", None, "alto_rapinadores"),
                        (56.2, 36.5, "Destripadores negros", "46-48", "o_molleja_buitre"),
                        (63.9, 33.6, "Serpiente Enroscada", None, "o_molleja_buitre")],
         ("Son buitres carroñeros que viven", -.2), ("en un paisaje de cráteres negros|fin", .3),
         ["entre el Alto de los Rapiñadores", ("y la Serpiente Enroscada", -.7), "y la Serpiente Enroscada"],
         "LAS TIERRAS DEVASTADAS", "un paisaje de cráteres negros"),
] + tarj(("Y sueltan la molleja de buitre", -.1), "o_molleja_buitre", "Molleja de buitre", "la estrella del número uno", dur=2.6) + [
    mg(O.probabilidad("MOLLEJA DE BUITRE", Fc("destripador_negro"), F("o_molleja_buitre"), 10, [0, 3, 5, 8], "4 DE CADA 10",
                      "El 23 de noviembre se vendía a más de 2 de oro"),
       ("A un jugador le cayó en", .6), ("a más de dos de oro cada una|fin", .5),
       ["le cayó en cuatro de cada", "la vendía a más de dos"], "4 de 10 mollejas", y=.50),
    mapa("devastadas", [(50.6, 14.4, "Lynnore y Drazial", "dos misiones piden mollejas", "lynnore")],
         ("Tan cara porque la piden dos", -.2), ("El vigor del buitre, que", .3),
         [("la piden dos misiones de la", .1)], "LAS TIERRAS DEVASTADAS", "quién las pide", estilo="original"),
    tarjc(("El vigor del buitre, que", .3), "lynnore", "El vigor del buitre", "Maga sangrienta Lynnore · pide 10", dur=3.0),
    tarjc(("y El golpe decisivo, que", -.3), "drazial", "El golpe decisivo", "Mago sangriento Drazial · pide 2", dur=3.0, x=.26),
    mg(O.cronometro("DESTRIPADORES NEGROS · MEDIA HORA", F("o_molleja_buitre"), 30, "21o", ("inv_misc_bag_10", "92 objetos"), "~41o/h"),
       ("Ese jugador lo midió media hora", -.2), ("antes de la comisión de la subasta|fin", .4),
       ["Ese jugador lo midió media hora", "unos veintiún de oro", "Unos cuarenta y uno de oro"], "cronómetro buitres", y=.50),
    mg(O.reparto("30 MINUTOS · UNOS 21 DE ORO", "21o", [(F("o_molleja_buitre"), "6 mollejas: la mitad", .5),
                                                     ("inv_misc_bag_10", "Todo lo demás", .5)]),
       ("Seis mollejas fueron la mitad", -.2), ("Y sin ninguna molleja le", -.2),
       ["Seis mollejas fueron la mitad", ("Seis mollejas fueron la mitad", .9)], "mollejas la mitad", y=.50),
    tabla([T_BUI, T_ALT, T_BUI0, T_COY, T_JAG, T_ELE, T_GOR], 0, ("Y sin ninguna molleja le", -.2),
          ("más que casi toda la lista|fin", .4), ("Y sin ninguna molleja le", .3)),
    rot(("En promedio, casi noventa platas", 0), "Casi 90 platas por buitre", sello="90", dur=4.0),
    tarjc(("cada vez que matas un buitre", -.3), "destripador_negro", "Destripador negro", "casi 90 platas por muerte", dur=4.0),
    mapa("devastadas", [(56.2, 36.5, "Destripadores", "8 de los 32 puntos", "o_molleja_buitre"),
                        (62.4, 26.8, "Destripadores", "5 puntos", "o_molleja_buitre"),
                        (55.0, 44.0, "Destripadores", "5 puntos", "o_molleja_buitre"),
                        (46.5, 19.1, "Destripadores", "4 puntos", "o_molleja_buitre")],
         ("Dos avisos. Solo hay unos", -.2), ("y gana quien está encima|fin", .3),
         [("Solo hay unos treinta y dos", .1), ("Solo hay unos treinta y dos", .6), "puntos de aparición, así que",
          "así que hay competencia"], "LAS TIERRAS DEVASTADAS", "unos 32 puntos de aparición"),
    rot(("Y el precio de la molleja", -.1), "El precio puede caer como el de los huevos", sello="!", dur=4.4),
    pv(("como cayó el de los huevos", -.4), "o_huevo_gigante", "Como los huevos", dur=3.0, x=.76, y=.46, tam=320),
    mapa("devastadas", [(47.8, 18.1, "Aguijoneros Scorpok", "50-51 · desuello", "o_pinza_scorpok"),
                        (47.5, 22.2, "Hienas risitas famélicas", "45-46 · desuello", "o_papada_hiena")],
         ("De paso puedes desollar a", -.2), ("famélicas de la zona|fin", .3),
         ["los aguijoneros Scorpok y", "y a las hienas risitas"], "LAS TIERRAS DEVASTADAS", "de paso, desuello"),
    mapa("devastadas", [(56.2, 36.5, "Destripadores negros", None, "o_molleja_buitre"),
                        (65.9, 18.7, "Castillo de Nethergarde", "vuelo y venta de la Alianza", "ico:ability_mount_gryphon_01")],
         ("La Alianza llega volando al", -.2), ("Y la Horda, desde el vuelo", -.1),
         [("La Alianza llega volando al", .2), "al Castillo de Nethergarde"], "LAS TIERRAS DEVASTADAS", "cómo llegar"),
    mapa("mundo", [(88.1, 68.0, "Rocal", "vuelo de la Horda · Pantano de las Penas", "ico:ability_mount_wyvern_01"),
                   (87.6, 72.6, "Destripadores negros", "Las Tierras Devastadas", "o_molleja_buitre")],
         ("Y la Horda, desde el vuelo", -.2), ("desde el vuelo del Pantano de las Penas|fin", .1),
         ["Y la Horda, desde el vuelo", ("desde el vuelo del Pantano", .4)], "AZEROTH", "la Horda llega desde Rocal", zmax=1.8,
         estilo="original"),
    ficha(1),
    # =========================================================== RESUMEN · la ruta del oro por nivel (1415-1467 s)
    rot(("Y si los juntas, te queda", 0), "La ruta del oro por nivel", sello="50", dur=3.6),
    mapa("mundo", [(27.8, 54.6, "Tortugas · Desierto de Sal", "30-36", "o_fragmento_caparazon"),
                   (79.4, 75.1, "Gorilas · Tuercespina", "32-35", "o_colmillo_gorila"),
                   (14.5, 35.7, "Centauros · Desolace", "33-38", "o_pano_seda")],
         ("Del treinta al treinta y cinco", -.2), ("y los centauros de Desolace|fin", .4),
         ["las tortugas del Desierto de Sal", "los gorilas de Tuercespina", "y los centauros de Desolace"],
         "DEL 30 AL 35", "la ruta del oro por nivel", zmax=1.2, estilo="original"),
    mapa("mundo", [(25.1, 40.6, "Arañas · Marjal", "35-38", "o_seda_arana_espesa"),
                   (80.8, 12.7, "Cuevas · Alterac", "34-38", "o_mena_oro"),
                   (87.8, 67.0, "Jaguares · Pantano", "36-39", "o_cola_blanda"),
                   (91.6, 62.1, "Coyotes · Claros del Río", "36-40", "o_cola_tupida"),
                   (85.9, 48.6, "Elementales inferiores", "37-39", "o_piedra_inerte")],
         ("Del treinta y cinco al cuarenta", -.2), ("y los primeros elementales de roca|fin", .3),
         ["las arañas del marjal", "las cuevas de Alterac", "los jaguares del pantano, los coyotes",
          "los coyotes de Claros del Río y", "y los primeros elementales"], "DEL 35 AL 40", "la ruta del oro por nivel", zmax=1.2),
    mapa("mundo", [(90.5, 47.8, "Crías · Barranco Lethlor", "40-44", "o_glandula_llamas"),
                   (84.9, 52.0, "Elementales superiores", "42-44", "o_tierra_elemental"),
                   (78.7, 87.7, "Cangrejos · sur de Tuercespina", "40-41", "o_almeja_boca_grande"),
                   (90.4, 70.8, "Múrlocs · Pantano", "41-45", "o_perla_oro")],
         ("Del cuarenta al cuarenta y cinco", -.2), ("y los múrlocs del Pantano de las Penas|fin", .3),
         ["las crías del Barranco Lethlor, los", "los elementales superiores", "los cangrejos del sur de Tuercespina",
          "y los múrlocs del Pantano"], "DEL 40 AL 45", "la ruta del oro por nivel", zmax=1.2),
    mapa("mundo", [(26.7, 64.6, "Hienas · Tanaris", "44-46", "o_melena_espesa"),
                   (10.4, 43.3, "Gorilas y osos · Feralas", "47-50", "o_hueso_oso"),
                   (87.6, 72.6, "Buitres · Tierras Devastadas", "46-50", "o_molleja_buitre")],
         ("Y del cuarenta y cinco al", -.2), ("La pesca de valijas, en cualquier", -.1),
         ["las hienas de Tanaris", "los gorilas y osos de Feralas", "y los buitres de Las Tierras"],
         "DEL 45 AL 50", "la ruta del oro por nivel", zmax=1.2),
    pv(("La pesca de valijas, en cualquier", -.1), "o_valija_mitril", "Pesca de valijas · en cualquier momento", dur=3.4, x=.17, y=.60),
    mg(O.etiquetas("UN CONSEJO PARA TODOS", F("o_ico_bolsa"), "Antes de guardarlo para la subasta", ("A VECES", "2c"),
                   ("Y A VECES", "2o"), (1, "MIRA AL VENDEDOR"), "Mira primero lo que paga el vendedor"),
       ("Y un consejo para todos", -.2), ("y a veces son dos de oro|fin", .8),
       ["A veces la diferencia son dos", "y a veces son dos de oro", ("y a veces son dos de oro|fin", 0)], "consejo final", y=.50),
    # =========================================================== CIERRE (1467-1502 s)
    rot(("Y esos son los quince farmeos", 0), "15 farmeos de oro del 30 al 50", sello="15", dur=4.2),
    pv(("del centauro que Blizzard acaba", -.2), Fc("retador_magram"), "Del centauro", dur=3.4, x=.20, y=.50, tam=440),
    pv(("al buitre que deja casi", -.2), Fc("destripador_negro"), "al buitre", dur=3.6, x=.77, y=.52, tam=440),
    rot(("Ahora cuéntame en los comentarios", 0), "¿En qué nivel vas y cuánto oro llevas?", sello="?", dur=4.4),
    E.peg_e(("y cuál es tu farmeo secreto", -.2), "o_ico_pregunta", "Tu farmeo secreto", dur=3.6, x=.76, y=.46, tam=320),
    rot(("Y si alguien de tu hermandad", -.1), "¿Llegó al 40 sin montura? Mándaselo", sello="40", dur=4.6),
    pv(("llegó al cuarenta sin montura", -.3), "o_equitacion", "Sin montura", dur=3.6, x=.76, y=.46, tam=340),
    rot(("Nos vemos en la próxima crónica", 0), "Nos vemos en Azeroth", sello="!", dur=3.6),
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]
# Planos de ambiente casi quietos (nota del subagente A, 26-nov): acercamiento lento a lo largo del beat (FX zoom: solo el clip;
# pegatinas, MG y mapas van encima sin zoom), alternando el punto de fuga para que no se sientan iguales.
_BEATS = {b["id"]: b for b in _json.load(open(os.path.join(_D, "beats.json"), encoding="utf-8"))}


def acerca(i, cuanto=.12, cx=0.0, cy=0.0):
    b = _BEATS[i]
    return dict(tipo="zoom", beat=i, cuanto=cuanto, entra=max(.5, (b["t1"] - b["t0"]) * .95), sale=.01, cx=cx, cy=cy)


FX += [acerca(f"scene-{n:03d}", .10 + .03 * (k % 3), (-.3, 0.0, .3)[k % 3], (.1, -.1)[k % 2])
       for k, n in enumerate((7, 11, 41, 64, 65, 66, 67, 68, 69, 90, 114, 120, 125, 126, 164))]
_TAR = [d for d in FX if "tarjeta" in d and "tipo" not in d]      # las fichas de interfaz (tar) van a APOYOS
FX = [d for d in FX if not ("tarjeta" in d and "tipo" not in d)]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos); colores de la paleta (amarillo/rojo/blanco)
    dict(texto="SIN NINGUNA PROFESIÓN", en="no necesita ninguna profesión", dur=3.0, tam=110, color="rojo", y=.16),
    dict(texto="QUE NOS AVISE", en="que nos avise", dur=2.6, tam=120, color="amarillo", y=.16),
    dict(texto="TIENE RAZÓN", en="Tiene razón, y por eso", dur=2.6, tam=140, color="amarillo", y=.16),
    dict(texto="EL VENDEDOR NUNCA TE BAJA EL PRECIO", en="Porque el vendedor nunca te", dur=3.2, tam=80, color="amarillo", y=.16),
    dict(texto="OJO", en="Ojo con sus hienas", dur=2.4, tam=160, color="rojo", y=.16),
    dict(texto="UN RARO DENTRO", en="que dentro hay un raro", dur=2.6, tam=120, color="amarillo", y=.16),
    dict(texto="LAS GUÍAS NO SIEMPRE VAN AL DÍA", en="Porque las guías no siempre", dur=3.0, tam=80, color="rojo", y=.16),
    dict(texto="9 DE DICIEMBRE", en="Y para las bandas del nueve", dur=3.0, tam=130, color="amarillo", y=.86),
    dict(texto="TODOS LO SABEN", en="Tienes toda la razón, Lalo", dur=2.8, tam=130, color="amarillo", y=.16),
    dict(texto="TE CONTRATAMOS", en="que te contratamos", dur=2.6, tam=130, color="amarillo", y=.16),
    dict(texto="GRACIAS", en="Gracias a los tres", dur=2.8, tam=160, color="amarillo", y=.16),
    dict(texto="SUSCRÍBETE", en="suscríbete, que lo que viene", dur=3.0, tam=150, color="amarillo", y=.16),
    dict(texto="TODA LA RAZÓN", en="Tienes toda la razón, Pkponcho", dur=2.6, tam=130, color="amarillo", y=.16),
    dict(texto="UN ABRAZO, BRASIL", en="Un abrazo de vuelta para Lunatic", dur=3.0, tam=120, color="amarillo", y=.80),
    dict(texto="GRACIAS", en="Gracias, de verdad", dur=2.4, tam=160, color="amarillo", y=.80),
    dict(texto="EL PROBLEMA: LA GENTE", en="el único problema es la gente", dur=2.6, tam=100, color="rojo", y=.16),
    dict(texto="×2", en="cómo duplicarlo", dur=2.6, tam=170, color="amarillo", y=.16),
    dict(texto="BOLSAS DE 14", en="y hasta bolsas de catorce casillas", dur=2.6, tam=120, color="amarillo", y=.16),
    dict(texto="SIN PROFESIÓN", en="no hace falta ninguna profesión para", dur=2.6, tam=130, color="amarillo", y=.16),
    dict(texto="AZAZEL, NOS DEBES UNO", en="Azazel incluido, que nos debe", dur=2.8, tam=100, color="amarillo", y=.16),
    dict(texto="SUSCRÍBETE", en="suscríbete y compártelo con tu", dur=3.0, tam=150, color="amarillo", y=.16),
] + _ROT_FLOW
SFX = {}
PISTAS = []

APOYOS = [
    tar("Una rama de talentos escrita", "Rama de talentos de una guía", "inv_misc_book_09",
        ["Escrita antes del último ajuste", dict(t="Puede estar desfasada", c=RJ), dict(t="El coach mira la versión de hoy", c=V)], dur=5.6),
] + _TAR + _TIPS
