# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 ERRORES del nivel 30 al 60 en WoW Forever» (SECUENCIA YT, Crónicas de Warcraft, 11-nov-2026).
Modelo: videos/wow_secretos_primeros_niveles/efectos.py (helpers y bloque Overgear, enlace /CRONICAS/5).
- Cada puesto: reliquia/pegatina real al decir «Número N» + MAPA REAL con ruta (zamimg Classic eses, 1 % = coordenada) en 14 de 20
  + MG nuevos de este guion (curva 12/88, las 15 páginas, misión gris, doble spec, subasta, llavero, ruta de la Llave esqueleto,
  calendario de Onyxia, muro de los 50).
- Comentarios en pantalla (≤ 10 días, ninguno repetido): Tod, Rubén (gracias1) · Zanafer, Gregory, Matías (gracias2) ·
  críticas Marcos (burla0), Warr (burla1), Alberto ×2 (burla2).
  python fab.py wow_errores_30_60 fx --seco | fx hoja | fx
"""
import os

import mg_tes as T
import mg_wow as M
import peg_estilos as PE

_D = os.path.dirname(os.path.abspath(__file__))
_PEG, _PAN, _MAP = (os.path.join(_D, c) for c in ("pegatinas", "pantallas", "mapas"))
OG = r"medios\_overgear" + "\\"
OGF = OG + "forever\\"
CREATIVO = OG + "CRONICAS10_forever.mp4"
CODIGO = ("Usa el código CRONICAS10", 0.9)
TEMA_PEG = "wow"
AMAR, ROJO, VERDE, BLANCO, NAR = (255, 255, 160), (255, 70, 60), (40, 210, 90), (240, 240, 240), (255, 150, 60)
V, GR, RJ = "verde", "gris", "#ff3b3b"


def F(slug):
    return os.path.join(_PEG, slug + ".png")


def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    if slug.startswith("o_"):
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PA.variado(F(slug), titulo, tam, tema=TEMA_PEG, **anim), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def filav(en, items, y=.64, tam=320, dur=4.6):
    xs = (.14, .32, .50, .68, .86)
    return [pv(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, id_, dur=5.4, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(F("com_" + id_), "", tam), en=en, dur=dur, x=x, y=y, sale=.3, nombre="comentario " + id_, ver=1.0)


def rel(en, slug, nombre=None, sub=None, dur=4.2, x=.76, y=.52, tam=500):
    if slug.startswith("o_"):   # íconos de 56 px: más chicos, que no se vean borrosos (regla 10-nov)
        tam = min(tam, 340)
    return dict(tipo="mg", fn=PE.reliquia(F(slug), nombre, sub, tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .3, 1.4)):
    return dict(tipo="mg", fn=PE.camafeo(F(slug), nombre, tam, foco, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def ban(en, slug, nombre, sub=None, dur=4.0, x=.5, y=.78, tam=420):
    return dict(tipo="mg", fn=PE.banda(F(slug), nombre, sub, alto=tam, tema="wow"), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def sil(en, slug, nombre, sub=None, dur=4.4, lado="izq", alto=820, marco="museo"):
    # PERSONAS REALES = OPACAS (el usuario, 10-nov-2026): PE.silueta recortaba con rembg y la foto de Michel Koiter salía
    # translúcida, fundida con el gameplay. Ahora retrato con marco opaco a media pantalla (antes PE.silueta).
    return pv(en, slug, nombre, dur=dur, x=(.25 if lado == "izq" else .75), y=.50, tam=640,
              marco=marco, estancia="kenburns")


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(F(s), e) for s, e in fotos], tam, tema="wow"), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="abanico " + nombre, ver=1.2)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mapa(nom, puntos, de, a, marcas, titulo, sub=None, objeto=None, zmax=1.5, zmin=1.0):
    return dict(tipo="pantalla", fn=M.ruta(os.path.join(_MAP, nom + ".jpg"), puntos, titulo, sub, zmax=zmax, zmin=zmin, objeto=objeto),
                de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + titulo, ver=1.0)


def mg(fn, de, a, marcas, nombre, y=.60, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel([(F(s), n) for s, n in fotos], tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus((F(a_[0]), a_[1]), (F(b_[0]), b_[1]), ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def P(x, y, rot, sub=None, foto=None):
    return (x, y, rot, sub, F(foto) if foto else None)


CAMARA = {}
FUNDIDO = {}
EXP = "inv_misc_book_11"   # ícono de experiencia
FX = [
    # =========================================================== gancho: MG desde el primer segundo
    mg(M.tiempos("LA EXPERIENCIA DE TODO EL JUEGO", [("1 → 30 · 12 %", 12, VERDE), ("30 → 60 · 88 %", 88, ROJO)],
                 "4 084 700 puntos para llegar al 60"),
       ("Llegaste al nivel treinta", -.2), ("Y ahí es donde la gente pierde semanas|fin", .4),
       ["Pues no. Vas por el doce", "Para llegar al sesenta, más de cuatro millones", "el ochenta y ocho por ciento"], "curva 12/88", y=.55),
    ban("Y hay otro detalle que casi nadie sabe", "tuercespina", "LA BETA ACABABA EN EL 30", "del 31 al 60, nadie lo había jugado", dur=5.0),
    dict(tipo="mg", fn=PE.banda(F("expedicion"), "20 ERRORES DEL 30 AL 60", "del 20 al 1 · y cómo arreglarlos", alto=380, tema="wow"),
         en=("Hoy te traigo veinte errores", -.2), dur=4.4, x=.5, y=.80, sale=.3, nombre="banda 20", ver=1.0),
    # =========================================================== 20 páginas
    rel("Número veinte. Cargar veintisiete", "o_pagina", "Las verdes colinas", "de Tuercespina · 15 de 27 sirven"),
    mapa("tuercespina", [P(35.6, 10.6, "Expedición de Nesingwary", "Barnil Jarropetra", "barnil"), P(27, 77, "Bahía del Botín", "subasta", "bahia")],
         ("En el norte de la Vega de Tuercespina", -.2), ("Barnil Jarropetra te pide|fin", .2),
         ["En el norte de la Vega", "Barnil Jarropetra"], "VEGA DE TUERCESPINA", "nivel 30-45"),
    mg(M.filas("LAS 15 PÁGINAS QUE SÍ SIRVEN", [("Capítulo I · 1, 4, 6, 8", 4, ["inv_misc_note_01"] * 4), ("Capítulo II · 10, 11, 14, 16", 4, ["inv_misc_note_01"] * 4),
                                               ("Capítulo III · 18, 20, 21, 24", 4, ["inv_misc_note_01"] * 4), ("Capítulo IV · 25, 26, 27", 3, ["inv_misc_note_01"] * 3)]),
       ("Capítulo uno: la uno", -.3), ("Capítulo tres: dieciocho|fin", .5),
       ["Capítulo uno", "Capítulo dos", "Capítulo tres", "Y el capítulo cuatro"], "15 páginas", y=.58),
    sil("Hemet Nesingwary es un homenaje a Ernest Hemingway", "hemingway", "Ernest Hemingway", "«Las verdes colinas de África»", dur=5.6, lado="der"),
    # =========================================================== 19 misiones grises
    mg(M.contadores("UNA MISIÓN QUE GUARDASTE «PARA LUEGO»", [(EXP, "En su nivel", 4700, None, 0), (EXP, "6 niveles tarde", 1100, 1, 2)],
                    ("YA CASI NO DA NADA", 2)),
       ("Y desde ahí, pierde entre un diez", -.2), ("Esa misión que guardabas para luego, ya casi no da nada|fin", .4),
       ["pierde entre un diez", "por cada nivel de más", "ya casi no da nada"], "misión gris", y=.58),
    mapa("desolace", [P(56, 60, "Desolace", "misiones de nivel 30-40")], ("misiones de Desolace, de Arathi", -.3), ("seis u ocho niveles tarde|fin", .2),
         ["misiones de Desolace"], "DESOLACE", "seis u ocho niveles tarde"),
    # =========================================================== Overgear (hacia el minuto 4) + fondo de marca SIEMPRE
    dict(tipo="video", ruta=OG + r"background\Background.mp4", bucle=True, de="Una guía te explica la clase en general", a=("Y ya que hablamos del patrocinador", -.1),
         entra=.3, nombre="og fondo marca"),
    dict(tipo="video", ruta=OGF + "white-og-small-logo.mp4", croma=True, bucle=True,
         de="Este video lo patrocina Overgear", a="El enlace está en la descripción, y por el lanzamiento", entra=.3, sale=.3, nombre="og logo esquina"),
    dict(tipo="video", ruta=OGF + "2 pair_green_wow-forever.mp4", croma=True, en="un profesional verificado", dur=4.0, sale=.25, nombre="og pros"),
    dict(tipo="video", ruta=OGF + "cards-1-coaching_green-screen_wow-forever.mp4", croma=True, en="Talentos, rotación", dur=4.0, sale=.25, nombre="og coaching"),
    dict(tipo="video", ruta=OGF + "Reviews_v3_redscreen_march_wow-forever.mp4", croma="rojo", en="tú eliges, y pagas", dur=4.0, sale=.25, nombre="og reseñas"),
    dict(tipo="video", ruta=OGF + "packshot-text_greenscreen_wow-forever.mp4", croma=True, en="El enlace está en la descripción, y por el lanzamiento",
         a=CODIGO, entra=.2, nombre="og packshot", ver=2.5),
    dict(tipo="video", ruta=CREATIVO, croma=True, de=CODIGO, a=("Y ya que hablamos del patrocinador", -.1), entra=.15, nombre="og CODIGO", ver=3.0),
    # =========================================================== burla0 (Marcos)
    com("Marcos escribió: quién puede", "UgyJulOqxoNMH6lpv2V4AaABAg", dur=6.0, x=.32, y=.30),
    # =========================================================== 18 ángel
    rel("Número dieciocho. Resucitar con el Ángel", "angel", "Ángel de la Resurrección", "Dolencia de resurrección · 10 min"),
    mapa("tanaris_eses", [P(51.6, 27.8, "Gadgetzan", "cementerio"), P(39, 21, "Zul'Farrak", "tu cadáver", "zulfarrak_peg")],
         ("como Tanaris, Silithus o Desolace", -.3), ("nadie quiere correr de vuelta|fin", .3), ["como Tanaris"], "TANARIS", "el cementerio queda lejos"),
    # =========================================================== 17 vuelos
    rel("Número diecisiete. No activar los vuelos", "o_hogar", "Piedra de hogar", "1 hora de reutilización"),
    carr([("gadgetzan_peg", "Gadgetzan"), ("bahia", "Bahía del Botín"), ("kargath", "Kargath"), ("capilla", "Capilla de la Esperanza"), ("vista_eterna", "Vista Eterna")],
         "Los centros buenos de esta franja", ("la Capilla de la Esperanza de la Luz y Vista Eterna|fin", .3),
         ["Bahía del Botín", "Kargath para la Horda", "la Capilla de la Esperanza", "Vista Eterna"], titulo="DÓNDE ATAR LA PIEDRA"),
    pv("el Baluarte, en las Tierras de la Peste del Oeste", "baluarte", "El Baluarte · sin maestro de vuelo", dur=4.6, x=.72, y=.50, tam=640),
    # =========================================================== 16 JcJ
    mapa("tuercespina", [P(35.6, 10.6, "Expedición de Nesingwary"), P(32.5, 29, "Grom'gol", "zepelín de la Horda", "gromgol"), P(27, 77, "Bahía del Botín")],
         ("Horda y Alianza se cruzan en la Expedición", -.2), ("el zepelín de la Horda|fin", .3),
         ["en Bahía del Botín", "en el camino a Grom'gol"], "VEGA DE TUERCESPINA", "donde se cruzan las facciones"),
    # =========================================================== 15 Frondavil
    rel("Número quince. Pelear sin los curativos", "o_tuberculo", "Tubérculo de blancoria", "cura 1239-1592 · no comparte espera"),
    mapa("frondavil_eses", [P(51, 82, "Santuario Esmeralda", "Ungüento de planta Cenarion", "o_unguento")],
         ("En Frondavil, con el Ungüento", -.2), ("limpiar plantas corruptas del bosque|fin", .3), ["En Frondavil"], "FRONDAVIL", "nivel 45+"),
    filav("De las mismas plantas sale el Aliento", [("o_aliento", "Aliento de Dragón nocturno", None), ("o_tuberculo", "Tubérculo de blancoria", None)], y=.66, tam=320, dur=5.0),
    # =========================================================== gracias1
    com("Tod escribió que fue el mejor video", "UgwW592JD8G_KYBL2p94AaABAg", dur=5.6, x=.30, y=.30),
    com("Y Rubén lo resume en una línea", "Ugx36EufcukvuvbCH6R4AaABAg", dur=5.6, x=.66, y=.34),
    # =========================================================== 14 entrenador
    rel("Número catorce. Llegar al cuarenta y no pasar", "o_manoplas", "Manoplas del Maestro de filos", "en Forever: de +7 a +1"),
    pv("Y empieza en uno. Así que con tu arma", "o_devastador", "Habilidad de arma: 1", dur=4.4, x=.24, y=.56, tam=460),
    # =========================================================== 13 primeros auxilios
    rel("Número trece. Dejar los primeros auxilios", "o_pocion", "Poción de curación sublime", "Primeros auxilios 275-300"),
    mapa("arathi", [P(73.8, 32.6, "Sentencia", "Doctor Gregory Víctor", "gregory")], ("La Horda la hace con el doctor Gregory", -.2),
         ("con el doctor Gustaf VanHowzen, en Theramore|fin", -.9), ["La Horda la hace"], "TIERRAS ALTAS DE ARATHI", "Atenciones médicas · nivel 35"),
    mapa("marjal_eses", [P(66.4, 45.4, "Theramore", "Doctor Gustaf VanHowzen", "gustaf")], ("con el doctor Gustaf VanHowzen, en Theramore|fin", -.9),
         ("los más graves primero|fin", .2), ["Tienes que salvar a quince heridos"], "MARJAL REVOLCAFANGO", "la Alianza"),
    filav("guarda la seda y la tela de paño mágico", [("o_seda", "Tela de seda", None), ("o_panomagico", "Tela de paño mágico", None)], y=.66, tam=300, dur=4.6),
    # =========================================================== 12 doble especialización
    mg(M.contadores("DEL 40 AL 60", [("inv_misc_coin_01", "Reasignaciones de Classic", 40, None, 0), ("inv_misc_coin_01", "Doble especialización", 10, 1, 2)],
                    ("UNA SOLA COMPRA", 2)),
       ("En Forever, al nivel cuarenta, el entrenador", -.2), ("ya lo tenías resuelto|fin", .3),
       ["unas diez de oro", "Cambiar entre las dos es gratis", "con una sola compra"], "doble spec", y=.58, x=.34),
    pv("tanquear o curar en Zul'Farrak", "zulfarrak_peg", "Zul'Farrak · nivel 44-54", dur=4.4, x=.80, y=.50, tam=520),
    # =========================================================== 11 materiales
    rel("Vamos con el número once", "o_mitril", "Mineral de mitril", "a la subasta, no al vendedor"),
    mg(M.subasta("LO QUE VENDES AL VENDEDOR", [("inv_misc_leatherscrap_08", "Cuero grueso", "subasta", VERDE), ("inv_ore_mithril_02", "Mineral de mitril", "subasta", VERDE),
                                              ("inv_fabric_mageweave_01", "Tela de paño mágico", "subasta", VERDE)], ("MONTURA: UNAS 100 DE ORO", 3)),
       ("El cuero grueso de las bestias", -.2), ("en la subasta vale oro|fin", .3),
       ["el mineral de mitril", "y la tela de paño mágico", "Cada vez que pulsas vender todo"], "subasta", y=.58),
    # =========================================================== burla1 (Warr)
    com("Warr escribió: esto empieza", "UgyKh3_LChFmC2kdeXB4AaABAg", dur=6.4, x=.32, y=.30),
    pv("Cargar doce páginas que no sirven", "o_pagina", "12 páginas que no sirven", dur=4.0, x=.74, y=.56, tam=420),
    # =========================================================== 10 BiS
    vs(("herod", "Herod · el Devastador"), ("melenablanca", "Melenablanca · su Sombrero"), ("Los veteranos suben buscando", -.2),
       ("o el Sombrero de Melenablanca de la Catedral|fin", .4), ["el Devastador de Herod", "o el Sombrero de Melenablanca"], titulo="LA LISTA DE 2019"),
    mapa("tirisfal", [P(84.5, 31, "Monasterio Escarlata", "Armería y Catedral", "monasterio")], ("Pero Forever rehízo los objetos", -.2),
         ("distancia y hechizos|fin", .3), ["Pero Forever rehízo"], "CLAROS DE TIRISFAL", "Monasterio Escarlata"),
    # =========================================================== 9 llaves
    rel("Número nueve. Entrar a las mazmorras", "o_llave_escarlata", "La llave Escarlata", "cofre del Arcanista Doan"),
    carr([("o_llave_escarlata", "Llave Escarlata"), ("o_llave_sombra", "Llave Sombratiniebla"), ("o_marra", "Marra sacra")],
         ("Media franja del treinta al sesenta va con llavero", -.2), ("una puerta cerrada|fin", .3),
         ["la llave Escarlata salía", "Si empiezas por la Armería"], titulo="EL LLAVERO DEL 30 AL 60"),
    pv("Te la da Franclorn Forjador, un fantasma", "franclorn", "Franclorn Forjador · solo estando muerto", dur=5.0, x=.72, y=.50, tam=640),
    mapa("interior", [P(49, 68, "Altar de Zul", "Marra sacra"), P(61, 75, "Jintha'Alor", "se transforma la Marra", "o_marra")],
         ("Se transforma en la cima de Jintha'Alor", -.3), ("se invoca a Gahz'rilla|fin", .2), ["Se transforma en la cima"], "TIERRAS DEL INTERIOR", "la Marra de Zul'Farrak"),
    pv("Gahz'rilla soltaba la Zanahoria", "gahzrilla_juego", "Gahz'rilla", dur=4.4, x=.24, y=.52, tam=520),
    pv("Gahz'rilla soltaba la Zanahoria|fin", "o_zanahoria", "Zanahoria pinchada en un palo", dur=3.6, x=.74, y=.52, tam=420),
    # =========================================================== 8 cadenas
    rel("Número ocho. Abandonar a la mitad", "linken", "Linken", "La leyenda de Zelda en WoW"),
    mapa("ungoro", [P(63.1, 68.5, "Balsa naufragada", "Linken"), P(43.6, 8.4, "Refugio de los Mariscales", "J.D. Collie", "jdcollie")],
         ("Empieza en una balsa naufragada", -.2), ("y a Tanaris|fin", .3), ["pasa por J.D. Collie"], "CRÁTER DE UN'GORO", "la cadena de Linken"),
    filav("Al final te dan la Espada de maestría", [("o_espada_linken", "Espada de maestría", None), ("o_bumeran", "Bumerán de Linken", None)], y=.64, tam=330, dur=5.0),
    pv("Con el Templo Sumergido pasa igual", "templo", "Templo de Atal'Hakkar", dur=4.6, x=.72, y=.50, tam=620),
    # =========================================================== 7 Fauces de Madera
    rel("Número siete. Llegar a Cuna del Invierno", "timbermaw", "Bastión de los Fauces de Madera", "solo pasan sus aliados"),
    mapa("frondavil_eses", [P(62, 24, "Muertobosque", "furbolgs", "muertobosque"), P(64.6, 8, "Túnel", "Fauces de Madera", "grazle")],
         ("La reputación sube matando", -.2), ("se llevan a Grazle y a Nafien, dentro del bastión|fin", .3),
         ["Las Plumas de penacho", "se llevan a Grazle"], "FRONDAVIL", "los furbolgs Muertobosque"),
    filav("Las Plumas de penacho Muertobosque y las Cuentas", [("o_pluma", "Pluma de penacho", None), ("o_cuentas", "Cuentas de Espíritu", None)], y=.70, tam=280, dur=4.6),
    # =========================================================== gracias2
    com("Zanafer escribió que se enteró", "UgxQndttdPhEGM-GcWZ4AaABAg", dur=4.8, x=.28, y=.26),
    com("Y Gregory dice que el guion", "UgwT2OG4UHOgNNKY1HZ4AaABAg", dur=4.4, x=.70, y=.66),
    com("Y Matías lo deja claro", "UgzPWIDRQMH0N0zYubR4AaABAg", dur=5.0, x=.32, y=.32),
    # =========================================================== 6 Alba Argenta
    rel("Número seis. Matar no-muertos", "o_comision", "Comisión del Alba Argenta", "sin ella, no cae ni una"),
    filav("sueltan Piedras de la Plaga", [("o_piedra_plaga", "Piedra de la Plaga", None), ("o_muestra", "Muestra de valor", None)], y=.66, tam=320, dur=5.0),
    mapa("tdp_este_eses", [P(81.5, 59.5, "Capilla de la Esperanza de la Luz", "Duque Nicolás Zverenhoff", "zverenhoff")],
         ("Las piedras se entregan en la Capilla", -.2), ("a cambio de Muestras de valor del Alba Argenta|fin", .3), ["al duque Nicolás"], "TIERRAS DE LA PESTE DEL ESTE", "Alba Argenta"),
    # =========================================================== 5 misiones de clase
    rel("Número cinco. Saltarte las misiones de clase", "templo", "Templo de Atal'Hakkar", "misiones de clase del nivel 50"),
    mapa("azshara", [P(29, 40, "Archimago Xylem", "mago y pícaro", "xylem"), P(42, 43, "Ogtinc", "cazador y sacerdote", "ogtinc")],
         ("El mago y el pícaro la recogen", -.3), ("también en Azshara|fin", .3), ["El cazador y el sacerdote"], "AZSHARA", "nadie te avisa"),
    carr([("diblis", "Brujo · Diblis"), ("heroe", "Guerrero · Héroe caído"), ("ashlam", "Paladín · Peste del Oeste")],
         "El brujo, de un diablillo", ("en la entrada de Un'Goro|fin", .3),
         ["Y el guerrero", "El paladín la busca"], titulo="¿QUIÉN TE LA DA?"),
    # =========================================================== burla2 (Alberto)
    com("Alberto escribió: no sé quién", "UgyZ2txk2XtDDyYmmH54AaABAg", dur=6.0, x=.32, y=.30),
    com("Alberto también escribió que le gusta más Spoken", "Ugy9TIGrQnN4nmAAlR54AaABAg", dur=6.0, x=.66, y=.34),
    # =========================================================== 4 muro de los 50
    mg(M.contadores("CADA NIVEL DEL 50 AL 55", [(EXP, "Experiencia por nivel", 147500, None, 0), ("inv_misc_note_01", "Misiones que quedan", 0, 1, 1)],
                    ("EL MURO DE LOS 50", 2)),
       ("En Classic, entre el cincuenta y el cincuenta y cinco", -.2), ("puntos de experiencia o más|fin", .3), ["Y cada nivel pide", "puntos de experiencia o más"], "muro 50", y=.58),
    mapa("estepas", [P(84, 68, "Vigilia de Morgan"), P(29, 38, "Montaña Roca Negra", "mazmorras llenas de misiones", "montana")],
         ("La salida de siempre era la Montaña Roca Negra", -.2), ("más Un'Goro, Frondavil y Cuna del Invierno|fin", .2), ["con sus mazmorras"], "LAS ESTEPAS ARDIENTES", "la salida de siempre"),
    mapa("marjal_eses", [P(76, 18, "Alcaz Island Prison", "nivel 48-55 · nueva", "alcaz")], ("Pero Forever añade huecos nuevos", -.2),
         ("para el cuarenta y ocho al cincuenta y cinco|fin", .3), ["Alcaz Island Prison"], "MARJAL REVOLCAFANGO", "mazmorra nueva de Forever"),
    pv("Y Blackmaw Hold, en el norte de Azshara", "blackmaw", "Blackmaw Hold · 55-60", dur=4.6, x=.72, y=.50, tam=620),
    # =========================================================== 3 Llave esqueleto
    rel("Número tres. Llegar al cincuenta y ocho", "o_llave_esqueleto", "Llave esqueleto", "Scholomance"),
    mapa("peste_oeste", [P(42.9, 84.5, "Campamento del Orvallo", "Alianza · Ashlam", "ashlam"), P(80, 68, "El Baluarte", "Horda", "baluarte")],
         ("Empieza en las Tierras de la Peste del Oeste", -.2), ("y la Horda, en el Baluarte|fin", .3), ["y la Horda, en el Baluarte"], "TIERRAS DE LA PESTE DEL OESTE", "empieza la cadena"),
    mg(M.cadena("LA RUTA DE LA LLAVE ESQUELETO", [(F("o_fragmento"), "15 fragmentos", "Tierras de la Peste", False), (F("krinkle"), "Krinkle Buenacero", "Gadgetzan · 15 de oro", False),
                                                 (F("o_torio"), "2 lingotes de torio", "lava de Un'Goro", False), (F("araj"), "Araj el Invocador", "Andorhal", True)],
                ("LA PUERTA SE ABRE", 4)),
       ("Te piden quince fragmentos esqueléticos", -.2), ("matas a Araj el Invocador, en Andorhal|fin", .4),
       ["Te piden quince", "Krinkle Buenacero", "con dos lingotes", "matas a Araj", "Araj el Invocador, en Andorhal|fin"], "cadena llave", y=.58),
    # =========================================================== 2 ruta de Classic
    rel("Número dos. Subir del treinta al sesenta", "riverglades_peg", "Riverglades", "zona nueva · 35-45"),
    carr([("drowned_peg", "The Drowned City"), ("kroldok_peg", "Krol'dok Stronghold"), ("shendralas_peg", "Shen'dralas")],
         ("Está también Shen'dralas", -.2), ("Krol'dok Stronghold, en Riverglades|fin", .3), ["The Drowned City", "y Krol'dok"], titulo="LO NUEVO DE FOREVER"),
    # =========================================================== 1 Onyxia
    rel("Número uno. Llegar al sesenta el nueve", "o_amuleto", "Amuleto de Pirodraco", "personal · no de cuenta"),
    mg(M.tiempos("CINCO SEMANAS PARA ONYXIA", [("4 nov · Forever", 7, VERDE), ("5 semanas para subir y sintonizar", 20, AMAR), ("9 dic · bandas", 7, ROJO)],
                 "¿empezaste la sintonización?"),
       ("Del cuatro de noviembre al nueve de diciembre", -.2), ("mirando el portal|fin", .4), ["Del cuatro de noviembre", "hay cinco semanas", "El que empieza tarde"], "calendario", y=.58),
    pv("Y en medio está la más temida", "windsor", "Alguacil Windsor · si muere, se falla", dur=5.0, x=.72, y=.50, tam=640),
    mapa("inhospitas", [P(3, 47, "Kargath", "Señor de la guerra Dientegore · SIN «!»", "dientegore")], ("El que te da la primera, el Señor", -.2),
         ("ahí empieza Onyxia|fin", .3), ["no tiene el signo"], "TIERRAS INHÓSPITAS", "la trampa de la Horda"),
    carr([("rexxar", "Rexxar"), ("brasaliza", "Brasaliza"), ("thrall", "Thrall")], ("Luego te toca la Cumbre de Roca Negra", -.2),
         ("repartidas por el mundo|fin", .3), ["Rexxar en Desolace", "Brasaliza en el Marjal"], titulo="LA SINTONIZACIÓN DE LA HORDA"),
    pv("matando al general Drakkisath", "drakkisath", "General Drakkisath", dur=4.6, x=.72, y=.50, tam=600),
    pv("la misión del Lacre de Ascensión", "o_lacre", "Lacre de Ascensión · ¿hace falta?", dur=5.0, x=.26, y=.52, tam=480),
    pv("abren las bandas. Barrow Deeps", "guarida", "Guarida de Onyxia", dur=4.6, x=.74, y=.50, tam=600),
    # =========================================================== cierre
]
FX = [d for x in FX for d in (x if isinstance(x, list) else [x])]

ROTULOS = [   # solo para énfasis (regla del 30-sep: nada de subtítulos)
    dict(texto="12 %", en="Vas por el doce por ciento", dur=2.4, tam=170, color="rojo", y=.2),
    dict(texto="88 %", en="el ochenta y ocho por ciento", dur=2.4, tam=170, color="amarillo", y=.2),
    dict(texto="15 DE 27", en="solo piden quince páginas concretas", dur=2.4, tam=150, color="amarillo", y=.2),
    dict(texto="-10 a -20 % POR NIVEL", en="pierde entre un diez y un veinte", dur=2.6, tam=110, color="rojo", y=.2),
    dict(texto="SIN «!»", en="no tiene el signo de misión sobre la cabeza", dur=2.6, tam=150, color="rojo", y=.2),
    dict(texto="9 DE DICIEMBRE", en="El nueve de diciembre abren las bandas", dur=2.6, tam=130, color="amarillo", y=.2),
    dict(texto="HABLA CON ÉL", en="habla con Dientegore aunque no tenga signo", dur=2.4, tam=130, color="amarillo", y=.2),
]
SFX = {}
PISTAS = [dict(sfx="mision_aceptada", en=e, vol=.28) for e in ("Número veinte.", "Número quince", "Número diez", "Número cinco")]
PISTAS += [dict(sfx="subir_nivel", en=e, vol=.24) for e in ("Hoy te traigo veinte errores", "Número uno. Llegar al sesenta")]

APOYOS = [
    dict(en="Las páginas del libro caen de casi todos", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Las verdes colinas", calidad="amarillo",
         icono="inv_misc_note_01", lineas=["27 páginas", dict(t="La misión usa 15", c=V), dict(t="Las otras 12: a la subasta", c=GR)])),
    dict(en="Si resucitas con el ángel", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Dolencia de resurrección", calidad=RJ,
         icono="spell_holy_resurrection", lineas=["10 minutos", dict(t="Classic: −25 % de durabilidad extra", c=RJ)])),
    dict(en="Y aquí está el truco: tienen su propio tiempo", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Tubérculo de blancoria", calidad="verde",
         icono="inv_misc_food_55", lineas=["Cura 1239-1592", "Nivel 45", dict(t="No comparte espera con pociones", c=V)])),
    dict(en="En Classic, al nivel cuarenta, el guerrero", dur=5.4, x=.72, size=.50, tarjeta=dict(titulo="Nivel 40", calidad="amarillo",
         icono="inv_chest_plate01", lineas=["Guerrero y paladín: placas", "Cazador y chamán: malla", dict(t="En tu entrenador", c=V)])),
    dict(en="Para pasar de doscientos veinticinco", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Atenciones médicas", calidad="amarillo",
         icono="spell_holy_sealofsacrifice", lineas=["Primeros auxilios 225", "Nivel 35", dict(t="15 heridos, los graves primero", c=V)])),
    dict(en="El equipo que sumaba habilidad de arma", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Objetos de Forever", calidad="morado",
         icono="inv_misc_questionmark", lineas=["Aciertos y críticos iguales", "Llega la pericia", dict(t="Sanación con poder con hechizos", c=V)])),
    dict(en="Pero solo caen si llevas equipada", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Comisión del Alba Argenta", calidad="verde",
         icono="inv_jewelry_talisman_07", lineas=["Abalorio de misión", dict(t="Equipada: caen piedras", c=V), dict(t="Sin ella: ni una", c=RJ)])),
    dict(en="Y una trampa: en las Tierras de la Peste del Oeste", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Ojo al 50", calidad=RJ,
         icono="inv_misc_note_01", lineas=["Misión de enlace del nivel 50", dict(t="Sin ella no se abre la zona", c=RJ)])),
    dict(en="Pero la Guarida de Onyxia, de cuarenta", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Amuleto de Pirodraco", calidad="azul",
         icono="inv_jewelry_talisman_11", lineas=["Guarida de Onyxia · 40", dict(t="Personal, no de cuenta", c=RJ)])),
    dict(en="La Alianza tiene dieciséis misiones", dur=5.0, x=.72, size=.50, tarjeta=dict(titulo="Sintonización", calidad="amarillo",
         icono="inv_misc_head_dragon_black", lineas=["Alianza: 16 misiones · desde el 48", dict(t="Horda: 15 misiones · nivel 55", c=GR)])),
]
