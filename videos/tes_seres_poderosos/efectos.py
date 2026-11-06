# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 20 seres más PODEROSOS de Tamriel» (SECUENCIA YT, Crónicas de Tamriel, 5-nov-2026).
REGLA DE ORO (tes_secretos_40) + «sin tramos vacíos» + KITS NUEVOS del 5-nov-2026 (pedido expreso del usuario):
- pegatinas casi todas con `pv()` (rotador de peg_anim + peg_anim_mas: pergamino, vitral, naipe, estampilla…), más estilos de
  peg_estilos (silueta, reliquia, camafeo, banda, abanico) para variar tamaños;
- PRESENTACIONES (nucleo/presenta.py), una de cada: tier list del gancho, versus Alduin–Sangre de Dragón, carrusel de príncipes
  daédricos, muro de los Nueve con Talos, tablero del Corazón de Lorkhan, podio final;
- MAPAS con `entrada=` rotando (desenrolla, foco, mesa, pliegue), `territorios` (Solstheim, la Plaga, las provincias de Talos,
  Estivalia, Cyrodiil) y puntos `"poder"`;
- MG NUEVOS de este guion en mg_tes: `escalera` (escala de poder que sube con la lista) y `cosmologia` (anillos del universo);
- 20 avisos de puesto, fichas de inventario con datos de UESP (`_investigacion_ranking.md`), comentarios reales (≤ 10 días).
  python fab.py tes_seres_poderosos fx --seco      python fab.py tes_seres_poderosos fx hoja
"""
import os

import mg_tes as T
import mg_wow as W
import peg_estilos as PE

CAMARA = {}
FUNDIDO = {}

_AQUI = os.path.dirname(os.path.abspath(__file__))
_FX, _FY = .76, .30
_PEG = os.path.join(_AQUI, "pegatinas")
_MAP = os.path.join(_AQUI, "mapas")
TEMA_PEG = "tes"
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


# ---------------------------------------------------------------- helpers (plantilla actual + tes_dwemer_desaparicion)
def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def pil(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=300, marco="polaroid"):
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.pila([(P(s), e) for s, e in fotos], tam, TEMA_PEG, marco), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.06, nombre="pegatina pila " + nombre, ver=2.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def tier(items, de, a, marcas, titulo=None, filas=("S", "A", "B", "C", "D")):
    import presenta as PR
    return _pres(PR.tierlist([(P(s), n, f) for s, n, f in items], filas, titulo, TEMA_PEG), de, a, marcas, "tier list")


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def tabl(fotos, hilos, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.tablero(_f(fotos), hilos, titulo, TEMA_PEG), de, a, marcas, "tablero")


def vs(a_, b_, de, a, marcas, ganador=None, titulo=None):
    import presenta as PR
    return _pres(PR.versus(_f([a_])[0], _f([b_])[0], ganador, TEMA_PEG, titulo), de, a, marcas, "versus")


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


def muro(fotos, de, a, marcas, destaca=None, titulo=None):
    import presenta as PR
    return _pres(PR.muro(_f(fotos), tema=TEMA_PEG, destaca=destaca, titulo=titulo), de, a, marcas, "muro")


def ficha(en, nombre, efecto, origen=None, dur=4.5, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def sil(en, slug, nombre=None, sub=None, dur=4.5, lado="izq", alto=880, encuadre=(0, .62)):
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.76, y=.52, tam=520):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, slug, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.0, y=.5, lado="der"):
    return dict(tipo="mg", fn=PE.banda(P(slug), nombre, sub, foco, lado=lado), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def mis(en, arriba, titulo, dur=3.0, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(P("com_" + cid), "", tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def aviso(en, n, titulo, dur=3.4):
    return dict(tipo="mg", fn=T.mision(f"Puesto número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mg_en(fn, en, dur, nombre, x=.5, y=.5):
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mapa(img, titulo, puntos, de, a, marcas, sub, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, img), puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    e = .05 if kw.get("entrada") else .5
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=list(marcas), entra=e, sale=e, nombre="mapa " + sub, ver=4.0)


def zoom(de, a, cuanto=1.15, cx=0.0, cy=0.0):
    return dict(tipo="zoom", de=de, a=a, cuanto=cuanto, entra=.6, sale=.4, cx=cx, cy=cy)


def pt(xy, nombre, tipo, foto=None):
    return (xy[0], xy[1], nombre, tipo) + ((P(foto),) if foto else ())


# ---------------------------------------------------------------- MG nuevos de este guion
PELDANOS = ["Mortal", "Ascendido", "Dios vivo", "Príncipe daédrico", "Aedra", "Fuerza primordial", "El Soñador"]


def escala(en, k, dur=4.0, x=.19, y=.40):
    """Escala de poder: el rombo sube hasta el peldaño k (marca 0 = peldaño anterior, marca 1 = k)."""
    fn = T.escalera("Escala de poder", PELDANOS)

    def f(dt, d, marcas, _k=k):
        return fn(dt, d, [0.0] * _k + [0.6])
    return dict(tipo="mg", fn=f, en=en, dur=dur, x=x, y=y, sale=.4, nombre="MG escala " + str(k), ver=1.0)


# ---------------------------------------------------------------- coordenadas
# mapas/tamriel.jpg (Fandom «Tamriel Map», rotulado): a ojo sobre la rejilla (previews/_tamriel_rejilla.jpg)
IMPERIAL, KVATCH, BRUMA = (.545, .49), (.367, .586), (.515, .374)
SOLEDAD_T, VENTALIA_T, SOLSTHEIM_T = (.42, .058), (.545, .155), (.695, .053)
ROJA_T, VIVEC_T, ALINOR = (.76, .28), (.762, .393), (.059, .869)
SENTINEL_T, DAGGERFALL_T, ELSWEYR_T, BMARSH_T, VALEN_T = (.107, .369), (.035, .355), (.52, .78), (.78, .78), (.36, .80)
ALDRUIN_T, CHEYD_T = (.76, .28), (.63, .45)
# polígonos de provincias (tamriel.jpg)
SKYRIM_P = [(.31, .10), (.40, .05), (.60, .06), (.62, .12), (.66, .30), (.58, .33), (.45, .32), (.40, .30), (.33, .22)]
CYRO_P = [(.40, .31), (.58, .33), (.66, .31), (.69, .45), (.66, .60), (.60, .68), (.50, .62), (.40, .62), (.30, .58), (.36, .45)]
HAMMER_P = [(.08, .33), (.20, .30), (.30, .22), (.40, .29), (.38, .45), (.30, .50), (.20, .42), (.08, .45)]
HROCK_P = [(.03, .30), (.08, .12), (.20, .08), (.33, .10), (.30, .20), (.20, .28), (.08, .33)]
MORRO_P = [(.62, .12), (.70, .12), (.70, .30), (.78, .38), (.92, .30), (.94, .45), (.88, .58), (.72, .60), (.66, .45), (.66, .30)]
BMARSH_P = [(.65, .65), (.75, .60), (.88, .62), (.92, .72), (.90, .95), (.70, .97), (.65, .85)]
ELSW_P = [(.44, .65), (.55, .62), (.60, .68), (.60, .95), (.50, .92), (.44, .80)]
VALEN_P = [(.28, .65), (.44, .62), (.45, .82), (.42, .92), (.30, .90), (.26, .78)]
SUMMER_P = [(.02, .75), (.10, .69), (.20, .70), (.21, .90), (.10, .95), (.02, .90)]
SOLST_P = [(.65, .02), (.75, .02), (.76, .09), (.67, .10)]
# mapas/skyrim.jpg (UESP, `_coords_uesp.py`)
HELGEN, GARGANTA, CARRERA = (.541, .733), (.624, .644), (.539, .525)
COLEGIO, LABY, SOLEDAD = (.744, .183), (.450, .382), (.342, .202)
MARKARTH, SANT_DAGON, SEPTIMUS = (.108, .488), (.489, .355), (.740, .097)
# mapas/morrowind.jpg (provincia, ESO; a ojo)
MONTANA, TELFYR = (.436, .379), (.61, .45)
PLAGA_P = [(.36, .30), (.44, .27), (.52, .31), (.53, .40), (.46, .46), (.37, .44)]

# ---------------------------------------------------------------- comentarios (≤ 10 días, ninguno usado antes)
C_POSH, C_EDWIN, C_PIERO, C_ENKI = "Ugw5rXxxWM7ippFxXIJ4AaABAg", "Ugy149apA3szXN_0_j14AaABAg", "UgxT1xnqFlyixkNeMOB4AaABAg", "Ugzut-Cllfuhd81NA4h4AaABAg"
C_RAIF, C_POKEGO, C_KRIS = "Ugwo8fhA1yu1g_Gh6WZ4AaABAg", "UgxEbIkzm3c6JwExwLl4AaABAg", "Ugz17eRkfS38nbESxRF4AaABAg"
C_SAIDA, C_AMADEO, C_ALLEYVA = "Ugyr9VQAN8wvcTVR7nx4AaABAg", "Ugwvca2j-mjRLiq_hoF4AaABAg", "UgwqwWBo_xwa7E8WAT54AaABAg"

FX = [
    # ================= GANCHO: un elemento nuevo cada 2-3 s
    zoom(0.0, "Un príncipe que te cambia la cara", 1.12),
    pv("Un nigromante que quiso ser dios", "mannimarco", "Mannimarco", dur=2.4, x=.17, y=.60, tam=380, entrada="tinta"),
    pv("Un dragón que se come el mundo", "alduin", "Alduin", dur=2.4, x=.80, y=.58, tam=420, marco="naipe"),
    rel("Un gólem de latón", "numidium", "Numidium", "Conquistó un continente", dur=2.6, x=.24, y=.52, tam=440),
    pv("te cambia la cara por un queso", "queso", "Sheogorath", dur=2.4, x=.78, y=.60, tam=340, entrada="aplasta"),
    pv("y un dios que ve el tiempo", "akatosh", "Akatosh", dur=2.8, x=.18, y=.58, tam=380, marco="vitral"),
    mis("la pregunta que más pelea", "Crónicas de Tamriel", "¿Quién es el más poderoso?", dur=3.4, y=.30),
    ficha("Todo comprobado en UESP", "Fuentes", "Cada dato con su enlace de *UESP*", "En la descripción", dur=3.2),
    mis("lo hemos hecho entre siete", "Siete voces", "Una sola lista", dur=3.0, y=.30),
    tier([("mannimarco", "Mannimarco", "D"), ("miraak", "Miraak", "C"), ("alduin", "Alduin", "B"), ("talos", "Talos", "B"),
          ("molag_bal", "Molag Bal", "A"), ("hermaeus", "Hermaeus Mora", "A"), ("akatosh", "Akatosh", "S")],
         "Esta es la tabla", ("Depende de quién esté soñando", .3),
         ["Esta es la tabla", "salió de la pelea", "quédate hasta el número uno", "porque no es un dios", "O sí. Depende", "Depende de quién",
          "esté soñando"], "La tabla de la pelea"),

    # ================= RECUENTO DE VOTOS (Sentinel, cerrada)
    mg(T.barras("Votación de Sentinel · cerrada", [(None, "Hope", 2, 0, T.HUESO), (None, "MariCarmen", 2, 1, T.HUESO),
                                                   (None, "Johnny", 2, 2, T.HUESO), (None, "Edoardo · José · Mario", 0, 3, T.SANGRE),
                                                   (None, "El Profeta", 8, 4, T.ORO)], unidad=" votos", remate=("OCHO", 5)),
       "Primero, el marcador", ("y un largo etcétera", .4),
       ["Hope, dos votos", "MariCarmen, dos", "Yo, Johnny, dos", "Edoardo, José y Mario", "Y el Profeta", "Ocho votos"], "recuento", y=.42),
    com("@saidavalera403", C_SAIDA, dur=2.6, x=.18, y=.20, tam=520),
    com("@amadeoamaya7606", C_AMADEO, dur=2.6, x=.82, y=.20, tam=520),
    com("@alleyva", C_ALLEYVA, dur=2.6, x=.18, y=.84, tam=520),
    mis("se lleva los seis primeros", "El ganador", "Del seis al uno: el Profeta", dur=3.4, y=.30),
    mg_en(T.escalera("Escala de poder", PELDANOS), "Yo soy el Profeta", 4.4, "escala presentación", x=.20, y=.42),

    # ================= 20 · MANNIMARCO (Johnny)
    aviso("Número veinte", 20, "Mannimarco"),
    sil("el Rey de los Gusanos", "mannimarco_eso", "Mannimarco", "El Rey de los Gusanos", dur=4.6, lado="der", alto=900),
    pv("en la isla de Artaeum", "artaeum", "Artaeum", dur=3.6, x=.20, y=.60, tam=420, marco="estampilla"),
    ficha("lo expulsaron por practicar nigromancia", "Expulsado de Artaeum", "Por practicar *nigromancia*", "Segunda era, 230", dur=4.4),
    pv("Allí conoció a Vanus Galerion", "galerion", "Vanus Galerion", dur=3.6, x=.80, y=.60, tam=360),
    mg(T.balanza("Dos alumnos de Artaeum", ("Galerion · una escuela", P("galerion")), [("Mannimarco · un culto a la muerte", P("mannimarco"))]),
       "Galerion acabó fundando", ("un culto a la muerte", 1.0), ["Galerion acabó fundando", "un culto a la muerte"], "balanza alumnos", y=.40),
    rel("gemas de alma negras", "gema_negra", "Gema de alma negra", "Atrapa almas de personas", dur=4.0, x=.76, y=.52, tam=440),
    pv("el aliado de Molag Bal", "molag_eso", "Molag Bal", dur=3.4, x=.18, y=.60, tam=380),
    mis("ascendió y se convirtió en un dios", "Distorsión del Oeste", "El Dios de los Gusanos", dur=3.8, y=.30),
    escala("Un mortal que se hace dios", 1),

    # ================= 19 · DIVAYTH FYR (Johnny)
    aviso("el mago que más ha vivido", 19, "Divayth Fyr"),
    pv("Un mago telvanni", "divayth", "Divayth Fyr", dur=3.6, x=.80, y=.58, tam=420, marco="museo"),
    mg_en(T.contadores("Divayth Fyr", [("Años", 4000, None, None), ("Nivel en Morrowind", 65, None, None)], remate=("EL MÁS VIEJO", 0)),
          "con más de cuatro mil años", 4.6, "edad divayth", x=.70, y=.34),
    mapa("morrowind.jpg", "Morrowind", [pt(TELFYR, "Tel Fyr", "poder", "tel_fyr")], "sigue en su torre", ("como si nada", .6),
         ["sigue en su torre"], "Tel Fyr", ventana=True, ancho=900, x=.30, y=.45),
    pv("el Corprusarium", "corprusarium", "Corprusarium", dur=3.4, x=.80, y=.60, tam=400),
    ficha("encontró la cura", "Cura del corprus", "La única de *Morrowind*", "Divayth Fyr", dur=4.4),
    aba([("divayth", "Alfe"), ("divayth", "Beyte"), ("divayth", "Delte"), ("divayth", "Uupse")], "Vive con cuatro mujeres",
        ("de él mismo", .5), ["Alfe, Beyte", "Delte y Uupse", "no son sus hijas"], "hijas clones", x=.34),
    mis("Son clones de él mismo", "«Hechas con mi propia carne»", "Clones", dur=3.6, y=.30),

    # ================= 18 · MIRAAK (Edoardo)
    aviso("Número dieciocho", 18, "Miraak"),
    sil("el primer Sangre de Dragón", "miraak_db", "Miraak", "El primer Sangre de Dragón", dur=4.6, lado="izq", alto=900),
    mapa("tamriel.jpg", "Solstheim", [pt(VENTALIA_T, "Ventalia", "inicio"), pt(SOLSTHEIM_T, "Solstheim", "poder", "templo_miraak")],
         "Miraak era un sacerdote dragón", ("Y los traicionó", .8), ["Miraak era un sacerdote", "en Solstheim"], "Solstheim",
         entrada="desenrolla", territorios=[dict(poli=SOLST_P, nombre="Solstheim", en=1)]),
    ficha("Doblegar Voluntad", "Doblegar Voluntad", "Hasta un *dragón* le obedece", "Grito de Miraak", dur=4.4),
    pv("pasó miles de años en Apocrypha", "apocrypha", "Apocrypha", dur=3.8, x=.20, y=.60, tam=440, entrada="portal"),
    pv("levantar su templo en trance", "templo_miraak", "Templo de Miraak", dur=3.6, x=.80, y=.60, tam=420),
    pv("lo atraviesa con un tentáculo", "hermaeus", "Hermaeus Mora", dur=3.8, x=.235, y=.58, tam=400, estancia="pulso"),
    mis("no lo pienses en voz alta", "Lección", "Mora lo sabe todo", dur=3.4, y=.30),
    escala("cuando te vas a traicionar", 1, dur=3.4),

    # ================= 17 · PELINAL (Edoardo)
    aviso("el caballero que cayó de las estrellas", 17, "Pelinal Whitestrake"),
    pv("Pelinal Whitestrake", "pelinal", "Pelinal Whitestrake", dur=3.8, x=.80, y=.58, tam=420, marco="vitral"),
    pv("Es el campeón de Alessia", "alessia", "Alessia", dur=3.4, x=.18, y=.60, tam=380, marco="pergamino"),
    ficha("Mató en duelo a reyes hechiceros", "Pelinal", "Mató reyes-hechiceros *en duelo*", "UESP", dur=4.4),
    ficha("venía del futuro", "Reliquias del Cruzado", "Venían *del futuro*", "Canción de Pelinal", dur=4.0, y=.62),
    aba([("pelinal", "Pelinal"), ("umaril", "Umaril")], "Su gran enemigo fue Umaril", ("en ocho pedazos", .5),
        ["Su gran enemigo fue Umaril", "un hechicero ayleid"], "duelo Torre Oro Blanco", x=.50, y=.60),   # s3: era un 2.º vs (máx. 1)
    # 6-nov: quitada, la estatua de Oblivion no es Morihaus comprobado (regla identidad)
    # pv("Y su cabeza siguió viva", "morihaus", "Morihaus", dur=3.6, x=.20, y=.60, tam=380, estancia="vela"),
    pv("Los Caballeros de los Nueve", "pelinal", "Cruzado Divino", dur=3.4, x=.80, y=.60, tam=380, entrada="sello"),
    mis("un avatar de Shezarr", "Teoría", "Shezarr, el dios perdido", dur=3.6, y=.30),

    # ================= CORREO · crítica con burla (posh)
    mis("Una pausa, que hay correo", "Correo", "Crítica de la semana", dur=2.8, y=.22),
    com("@ebre1976 nos escribió", C_POSH, dur=7.0, x=.50, y=.42, tam=1000),
    ficha("Yo tengo hache", "Hope", "Con *hache*", dur=2.6, y=.62),
    ficha("Yo amenazo, no pronuncio", "MariCarmen", "Amenaza, no pronuncia", dur=2.6, y=.62),
    mis("Si Ebre paró el video", "Edoardo", "Posh confeso", dur=4.4, y=.30),

    # ================= 16 · DAGOTH UR (José)
    aviso("José. Número dieciséis", 16, "Dagoth Ur"),
    sil("el dios que salió de una montaña", "dagoth_ur", "Dagoth Ur", "El Sharmat", dur=4.6, lado="der", alto=900),
    pv("el mejor amigo de Nerevar", "nerevar", "Nerevar", dur=3.4, x=.18, y=.60, tam=380),
    rel("se quedó a solas con el Corazón", "corazon_lorkhan", "Corazón de Lorkhan", "Lo hizo dios", dur=4.2, x=.76, y=.52, tam=440),
    mapa("morrowind.jpg", "Vvardenfell", [pt(MONTANA, "Montaña Roja", "poder", "montana_roja")], "envió la plaga a todo Vvardenfell",
         ("durante siglos", .6), ["envió la plaga"], "La Plaga", entrada="foco",
         territorios=[dict(poli=PLAGA_P, nombre="La Plaga", en=0)]),
    pv("la Valla Fantasma", "valla_fantasma", "Valla Fantasma", dur=3.6, x=.80, y=.60, tam=420),
    pv("su propio dios de latón, Akulakhan", "akulakhan", "Akulakhan", dur=3.8, x=.20, y=.58, tam=420, entrada="ceniza"),
    mis("bienvenido, Luna y Estrella", "Dagoth Ur", "«Bienvenido, Luna y Estrella»", dur=3.4, y=.30),

    # ================= 15 · VIVEC (José)
    aviso("el dios poeta", 15, "Vivec"),
    pil([("vivec", "Vivec"), ("almalexia", "Almalexia"), ("sotha_sil", "Sotha Sil")], "Vivec es uno de los tres dioses",
        ("el mismo Corazón de Lorkhan", .6), ["Vivec es uno", "junto a Almalexia", "y Sotha Sil"], "tribunal"),
    mapa("tamriel.jpg", "Morrowind", [pt(VIVEC_T, "Vivec", "poder", "ministerio")], "Su ciudad tiene su nombre", ("durante siglos#2", .8),
         ["Su ciudad tiene"], "Vivec", ventana=True, ancho=900, x=.30, y=.45),
    rel("el Ministerio de la Verdad", "ministerio", "Ministerio de la Verdad", "Un pedazo de luna", dur=4.6, x=.76, y=.52, tam=480),
    ficha("Y Vivec lo detuvo en el aire", "Baar Dau", "Detenido *en el aire*", "Vivec", dur=4.0),
    rel("te entrega el guantelete", "wraithguard", "Wraithguard", "Tocar el Corazón sin morir", dur=4.0, x=.24, y=.52, tam=420),
    pv("los Treinta y Seis Sermones", "sermones", "36 Sermones", dur=3.8, x=.80, y=.565, tam=380, marco="pergamino"),
    escala("Cuando el Corazón se destruyó", 2, dur=3.6),

    # ================= 14 · ALDUIN (Mario)
    aviso("Número catorce", 14, "Alduin"),
    sil("el Devorador del Mundo", "alduin", "Alduin", "El Devorador del Mundo", dur=4.4, lado="der", alto=860, encuadre=(0, .7)),
    pv("primogénito de Akatosh", "akatosh", "Akatosh", dur=3.4, x=.18, y=.60, tam=360),
    pv("con un Pergamino Antiguo", "pergamino_sr", "Pergamino Antiguo", dur=3.6, x=.80, y=.60, tam=400, entrada="desenrolla"),
    mapa("skyrim.jpg", "Skyrim", [pt(HELGEN, "Helgen", "inicio", "helgen"), pt(GARGANTA, "Garganta del Mundo", "poder", "garganta")],
         "Solo lo mandaron al futuro", ("cortar la cabeza", .5), ["Solo lo mandaron", "En Helgen"], "Helgen",
         entrada="mesa"),
    pv("en Sovngarde se come las almas", "sovngarde", "Sovngarde", dur=3.6, x=.20, y=.60, tam=420),
    mis("el que se come el mundo", "Profecía", "El Devorador del Mundo", dur=3.6, y=.30),

    # ================= 13 · EL SANGRE DE DRAGÓN (Mario)
    aviso("Y en el trece", 13, "El último Sangre de Dragón"),
    vs(("alduin", "Alduin"), ("dovahkiin", "Sangre de Dragón"), "Te pongo por encima de Alduin", ("así de simples", .4),
       ["Te pongo por encima", "cuando pelean", "ganas tú"], ganador=1, titulo="¿Quién gana?"),
    ficha("Absorbes el alma de cada dragón", "Alma de dragón", "Un grito nuevo por *cada alma*", dur=4.4),
    pv("Barbas Grises", "arngeir", "Barbas Grises", dur=3.2, x=.21, y=.58, tam=360),
    pv("junto a tres héroes nórdicos", "sovngarde", "Sovngarde", dur=3.4, x=.80, y=.60, tam=380),
    pv("vences a Miraak", "miraak", "Miraak", dur=3.2, x=.20, y=.58, tam=360, entrada="cristal"),
    mg_en(T.contadores("Lo que puedes hacer", [("Gremios a la vez", 6, None, None), ("Cucharas robadas", 999, None, None)],
                       remate=("TODAS", 0)), "al frente de todos los gremios", 5.0, "gremios", x=.70, y=.34),
    pv("cuarenta quesos en el bolsillo", "queso", "40 quesos", dur=3.4, x=.80, y=.60, tam=320, entrada="aplasta"),
    escala("El ser más poderoso de Skyrim", 0, dur=3.6),

    # ================= AGRADECIMIENTOS
    mis("Y ahora, gracias", "Comentarios", "Gracias", dur=2.4, y=.22),
    com("@EdwinRpoc dice", C_EDWIN, dur=4.4, x=.50, y=.40, tam=900),
    com("@pierodelgadomontes1568", C_PIERO, dur=6.0, x=.30, y=.30, tam=760),
    com("@Enki-11", C_ENKI, dur=4.0, x=.70, y=.66, tam=700),
    com("@raif5729", C_RAIF, dur=3.4, x=.30, y=.70, tam=640),
    com("@PokeGoDLegacy", C_POKEGO, dur=4.0, x=.70, y=.30, tam=700),
    mis("Los leemos todos", "Crónicas de Tamriel", "Todos se leen", dur=4.4, y=.30),

    # ================= EL DATO del Humano tras el Telón
    com("@krisstianblackgao1726", C_KRIS, dur=7.0, x=.50, y=.42, tam=1000),
    mis("Pero un dato sí", "El Humano tras el Telón", "Un dato. Uno solo", dur=3.0, y=.22),
    pv("un hombre de carne y hueso", "tiber", "Tiber Septim", dur=4.0, x=.80, y=.58, tam=420, marco="museo"),
    pv("en el Imperio está prohibido", "amuleto_talos", "Amuleto de Talos", dur=3.6, x=.18, y=.60, tam=360, entrada="sello"),

    # ================= 12 · TALOS (Hope)
    aviso("Número doce", 12, "Talos"),
    sil("Antes de ser dios, fue Tiber Septim", "tiber", "Tiber Septim", "Fundador del tercer Imperio", dur=4.6, lado="izq", alto=900),
    mapa("tamriel.jpg", "Tamriel", [pt(HAMMER_P[2], "Roca Alta", "inicio"), pt(SENTINEL_T, "Páramo del Martillo", "paso"),
                                    pt(VENTALIA_T, "Skyrim", "paso"), pt(ROJA_T, "Morrowind", "paso"),
                                    pt(BMARSH_T, "Pantano Negro", "paso"), pt(ELSWEYR_T, "Elsweyr", "paso"),
                                    pt(VALEN_T, "Bosque Valen", "paso"), pt(IMPERIAL, "Ciudad Imperial", "poder", "talos")],
         "Terminó la segunda era", ("un solo hombre gobernaba Tamriel", 1.2),
         ["Terminó la segunda era", "desde Roca Alta", "conquistándolo todo", "hasta el Pantano Negro", "hasta el Pantano Negro#",
          "Por primera vez", "un solo hombre", "gobernaba Tamriel"], "Conquista de Talos", entrada="pliegue", traza=1.0,
         territorios=[dict(poli=HROCK_P, nombre="Roca Alta", en=0), dict(poli=HAMMER_P, nombre="Páramo del Martillo", en=1),
                      dict(poli=SKYRIM_P, nombre="Skyrim", en=2), dict(poli=MORRO_P, nombre="Morrowind", en=3),
                      dict(poli=BMARSH_P, nombre="Pantano Negro", en=4), dict(poli=ELSW_P, nombre="Elsweyr", en=5),
                      dict(poli=VALEN_P, nombre="Bosque Valen", en=6), dict(poli=CYRO_P, nombre="Cyrodiil", en=7)]),
    mis("se convirtió en el noveno Divino", "Los Nueve Divinos", "Ocho dioses y un mortal", dur=4.4, y=.30),
    pv("los altos elfos del Thalmor", "elenwen", "Thalmor", dur=3.6, x=.80, y=.60, tam=380),
    ficha("exigieron prohibir su culto", "Concordato de Oro Blanco", "Culto a Talos *prohibido*", "Tratado con el Thalmor", dur=4.6, rojo=True),
    ficha("te da un descanso en tus gritos", "Bendición de Talos", "Espera entre gritos *−20 %*", "Santuario de Talos", dur=4.4),
    pv("los Capas de la Tormenta", "ulfric", "Ulfric Capa de la Tormenta", dur=3.6, x=.18, y=.60, tam=380),
    escala("Talos está por encima de todos los mortales", 1, dur=4.0),

    # ================= 11 · NUMIDIUM (Hope)
    aviso("En el once", 11, "El Numidium"),
    rel("Un gólem gigante de latón", "numidium", "Numidium", "El dios de latón", dur=4.4, x=.76, y=.52, tam=500),
    pv("con la Mantella como corazón", "mantella", "Mantella", dur=3.6, x=.20, y=.60, tam=380, estancia="brillo"),
    mapa("tamriel.jpg", "Estivalia", [pt(IMPERIAL, "Ciudad Imperial", "inicio"), pt(ALINOR, "Alinor", "poder", "numidium")],
         "lo lanzó contra las islas", ("En una hora", .6), ["lo lanzó contra", "su asalto a Alinor"], "Alinor", entrada="desenrolla",
         territorios=[dict(poli=SUMMER_P, nombre="Estivalia", en=1)]),
    mg(T.reloj("Asalto a Alinor", 60, remate=("MENOS DE UNA HORA", 1)), "Una isla entera de magos", ("En una hora", 2.4), ["Una isla entera", "En una hora"], "una hora", x=.72, y=.36),
    mis("el tiempo se rompió", "Tercera era, 417", "La Distorsión del Oeste", dur=4.0, y=.30),

    # ================= 10 · MOLAG BAL (Hope)
    aviso("el primero de los príncipes daédricos", 10, "Molag Bal"),
    carr([("molag_bal", "Molag Bal"), ("dagon", "Mehrunes Dagon"), ("sheogorath", "Sheogorath"), ("hermaeus", "Hermaeus Mora"),
          ("azura", "Azura"), ("boethiah", "Boethiah"), ("nocturnal", "Nocturnal")],
         "Los príncipes daédricos son dieciséis", ("su propio reino en Oblivion", .6),
         ["Los príncipes daédricos son", "son dieciséis", "no son dioses", "su propio reino"], "Príncipes daédricos"),
    pv("Coldharbour, un reflejo helado", "coldharbour", "Coldharbour", dur=3.8, x=.80, y=.60, tam=440, marco="cristal"),
    ficha("creó a los primeros vampiros", "Padre de los vampiros", "Creó a la *primera*", "Molag Bal", dur=4.0),
    pv("anclas oscuras", "ancla", "Ancla oscura", dur=3.6, x=.20, y=.60, tam=420, entrada="portal"),
    pv("una casa abandonada de Markarth", "casa_abandonada", "La casa abandonada", dur=3.4, x=.80, y=.60, tam=380),
    rel("te da su maza", "maza_molag", "Maza de Molag Bal", "Si le obedeces", dur=4.0, x=.24, y=.52, tam=420),
    escala("ni los demás príncipes lo soportan", 3, dur=4.0),

    # ================= 9 · MEHRUNES DAGON (MariCarmen)
    aviso("Número nueve", 9, "Mehrunes Dagon"),
    sil("el príncipe de la destrucción", "dagon", "Mehrunes Dagon", "Príncipe de la destrucción", dur=4.4, lado="der", alto=860),
    pv("el Alba Mítica", "alba_mitica", "Alba Mítica", dur=3.4, x=.18, y=.60, tam=360, marco="rasgado"),
    pv("Uriel Septim séptimo", "uriel", "Uriel Septim VII", dur=3.4, x=.80, y=.60, tam=360, estancia="vela"),
    mapa("tamriel.jpg", "Cyrodiil", [pt(KVATCH, "Kvatch", "inicio", "kvatch"), pt(BRUMA, "Bruma", "paso", "puerta_oblivion"),
                                     pt(IMPERIAL, "Ciudad Imperial", "poder", "dagon")],
         "se abrieron puertas de Oblivion", ("en persona en la Ciudad Imperial|fin", .4),
         ["se abrieron puertas", "La primera ciudad en caer", "en la Ciudad Imperial"], "Crisis de Oblivion", entrada="foco",
         territorios=[dict(poli=CYRO_P, nombre="Cyrodiil", en=0)]),
    pv("rompió el Amuleto de los Reyes", "amuleto_reyes", "Amuleto de los Reyes", dur=3.8, x=.22, y=.58, tam=420, entrada="cristal"),
    rel("la Navaja de Mehrunes", "cuchilla_mehrunes", "Navaja de Mehrunes", "Puede matar de un tajo", dur=4.2, x=.76, y=.52, tam=420),
    mis("pierde contra un dragón de fuego", "MariCarmen", "No se lo digáis", dur=3.4, y=.30),

    # ================= 8 · SHEOGORATH / JYGGALAG (MariCarmen)
    aviso("el príncipe de la locura", 8, "Sheogorath · Jyggalag"),
    pv("el loco simpático", "sheogorath", "Sheogorath", dur=3.6, x=.765, y=.58, tam=400, entrada="remolino"),
    rel("el Wabbajack", "wabbajack", "Wabbajack", "Locura en un bastón", dur=3.6, x=.24, y=.52, tam=400),
    pv("Sheogorath es una maldición", "jyggalag", "Jyggalag", dur=3.6, x=.80, y=.58, tam=400, entrada="glitch"),
    mg(T.versiones("Un mismo príncipe", (P("sheogorath"), "Sheogorath", ["Locura", "Queso", "Wabbajack"], 0),
                   (P("jyggalag"), "Jyggalag", ["Orden", "Lógica", "Marcha Gris"], 1), pie=None),
       "condenaron a Jyggalag", ("la Marcha Gris", .5), ["condenaron a Jyggalag", "el príncipe del orden"], "dos caras", y=.42),
    pv("te quedas con el trono", "islas", "Islas Temblorosas", dur=3.4, x=.18, y=.60, tam=400, marco="estampilla"),
    pv("la mente del emperador Pelagius", "pelagio", "Pelagius", dur=3.4, x=.80, y=.60, tam=360, estancia="balanceo"),
    mapa("skyrim.jpg", "Skyrim", [pt(SOLEDAD, "Palacio Azul", "poder", "sheogorath")], "sentado, tomando el té", ("el mismo héroe", .5),
         ["sentado, tomando"], "Soledad", ventana=True, ancho=880, x=.30, y=.45),

    # ================= 7 · HERMAEUS MORA (MariCarmen)
    aviso("el que lo sabe todo", 7, "Hermaeus Mora"),
    sil("Es el príncipe del conocimiento", "hermaeus", "Hermaeus Mora", "Príncipe del conocimiento", dur=4.4, lado="der", alto=860),
    pv("Sus Libros Negros", "libro_negro", "Libro Negro", dur=3.4, x=.18, y=.60, tam=360, entrada="origami"),
    rel("el Oghma Infinium", "oghma", "Oghma Infinium", "Un libro de poder", dur=4.0, x=.76, y=.52, tam=440),
    mapa("skyrim.jpg", "Skyrim", [pt(SEPTIMUS, "Puesto de Septimus", "poder", "septimus")], "Septimus Signus, el erudito",
         ("acaba hecho ceniza", .5), ["Septimus Signus"], "Septimus", ventana=True, ancho=880, x=.30, y=.45),
    ficha("los secretos de los Barbas Grises", "Precio de Mora", "Los secretos de *los Barbas Grises*", "Dragonborn", dur=4.4, rojo=True),
    mis("Mora ya sabía", "MariCarmen", "Mora ya lo sabía", dur=3.4, y=.30),
    escala("Eres su nuevo campeón", 3, dur=3.4),

    # ================= CAMPAÑA DE SUSCRIPCIÓN (~75 %)
    mg(T.rejilla("De cada cien que ven el canal", 100, 44, remate=("NO ESTÁN SUSCRITOS", 1)), "Antes del top seis", ("no están suscritos", .8),
       ["De cada cien", "cuarenta y cuatro"], "campaña rejilla", y=.42),
    mg_en(T.contadores("Crónicas de Tamriel", [("Suscriptores", 6490, None, None), ("Meta", 10000, None, None)], remate=("SUSCRÍBETE", 0)),
          "Somos seis mil", 5.0, "meta subs", x=.70, y=.34),

    # ================= 6 · MAGNUS (el Profeta)
    aviso("Llegamos al seis", 6, "Magnus"),
    mg_en(T.escalera("Escala de poder", PELDANOS), "El primero de los dioses", 4.0, "escala aedra", x=.20, y=.42),
    pv("el arquitecto de la creación", "magnus", "Magnus", dur=3.8, x=.80, y=.58, tam=420, estancia="orbita"),
    mg(T.estrellas("El cielo de Nirn", [("Magnus · el sol", [(.5, .3)], [], 0), ("Magna-Ge · las estrellas",
                                        [(.2, .6), (.3, .5), (.4, .65), (.6, .55), (.7, .7), (.8, .45)], [(0, 1), (1, 2), (3, 4), (4, 5)], 1)]),
       "abrió un agujero en el cielo", ("Esos agujeros son las estrellas", 1.0), ["Ese agujero es el sol", "Esos agujeros"], "cielo magnus", y=.42),
    mapa("skyrim.jpg", "Skyrim", [pt(COLEGIO, "Colegio de Hibernalia", "poder", "ojo_magnus"), pt(LABY, "Laberintia", "meta", "baculo_magnus")],
         "En el Colegio de Hibernalia encuentras", ("dejó las llaves puestas", .5), ["En el Colegio", "en Laberintia"], "Magnus",
         ventana=True, ancho=900, x=.30, y=.45),

    # ================= 5 · AKATOSH (el Profeta)
    aviso("En el cinco, el dios dragón", 5, "Akatosh"),
    pv("el principal de los Nueve", "akatosh", "Akatosh", dur=3.8, x=.80, y=.58, tam=380, marco="vitral"),
    ficha("lo llaman una ruptura de dragón", "Ruptura de dragón", "Cuando *el tiempo* se rompe", dur=4.4),
    pv("Akatosh baja en forma de dragón de fuego", "martin", "Martin Septim", dur=4.0, x=.18, y=.58, tam=400, entrada="ceniza"),
    aba([("alduin", "Alduin"), ("dagon", "Dagon"), ("dovahkiin", "Sangre de Dragón")], "Alduin, Dagon, el Sangre de Dragón",
        ("le deben algo a Akatosh", .5), ["Alduin, Dagon", "Dagon, el Sangre", "Tres de esta lista"], "deudores akatosh"),

    # ================= 4 · LORKHAN (el Profeta)
    aviso("el dios que nos engañó a todos", 4, "Lorkhan"),
    pv("Lorkhan. Él convenció", "lorkhan", "Lorkhan", dur=3.8, x=.80, y=.58, tam=400, estancia="pulso"),
    rel("Trinimac le arrancó el corazón", "corazon_lorkhan", "Corazón de Lorkhan", "Disparado por Auriel", dur=4.4, x=.24, y=.52, tam=440),
    pv("Donde cayó se formó la Montaña Roja", "montana_roja", "Montaña Roja", dur=3.6, x=.80, y=.60, tam=420, marco="estampilla"),
    tabl([("lorkhan", "Lorkhan"), ("sovngarde", "Shor"), ("pelinal", "Shezarr · Pelinal"), ("corazon_lorkhan", "El Corazón"),
          ("dagoth_ur", "Dagoth Ur"), ("vivec", "El Tribunal"), ("numidium", "Numidium")],
         [(0, 1), (0, 2), (0, 3), (3, 4), (3, 5), (3, 6)], "Cada pueblo lo llama", ("Por eso está en el cuatro", .4),
         ["Cada pueblo lo llama", "le dicen Shor", "le dicen Shezarr", "Y aquí todo encaja", "hizo dioses a Dagoth Ur", "y al Tribunal",
          "movió el Numidium"], "Todo encaja"),

    # ================= 3 · PADOMAY y 2 · ANU (el Profeta)
    aviso("En el tres", 3, "Padomay"),
    mg(T.cosmologia("El universo de Tamriel", [("Mundus", "Nirn y las lunas"), ("Oblivion", "Los reinos daédricos"),
                                               ("Aetherius", "Los dioses"), ("El vacío", "Anu y Padomay"), ("El Soñador", "¿El Godhead?")]),
       "Al principio de todo había", ("De la sangre de Padomay", -.2),
       ["Al principio de todo", "había dos fuerzas", "lo que se queda quieto", "y Padomay, lo que cambia", "lo que cambia"], "cosmología", y=.46),
    muro([("molag_bal", "Molag Bal"), ("dagon", "Mehrunes Dagon"), ("sheogorath", "Sheogorath"), ("hermaeus", "Hermaeus Mora")],
         "De la sangre de Padomay", ("Todos son hijos del cambio", .8),
         ["salieron los daedra", "Molag Bal, Dagon", "Dagon, Sheogorath", "Sheogorath, Hermaeus"], titulo="Hijos del cambio"),
    pv("Muchos lo identifican con Sithis", "sithis", "Sithis", dur=3.8, x=.80, y=.60, tam=380, marco="museo"),
    pv("oyes a la Madre Noche", "madre_noche", "Madre Noche", dur=3.4, x=.18, y=.60, tam=360, estancia="vela"),
    aviso("su eterno rival", 2, "Anu"),
    pv("Según el Anuad, los dos hermanos", "anu_padomay", "Anu y Padomay", dur=4.4, x=.80, y=.58, tam=460, entrada="portal"),

    # ================= 1 · EL SOÑADOR (el Profeta)
    aviso("Y el número uno", 1, "El que sueña"),
    mg_en(T.escalera("Escala de poder", PELDANOS), "es un sueño", 4.4, "escala soñador", x=.20, y=.42),
    ficha("su existencia está en disputa", "Godhead", "Existencia *en disputa*", "UESP", dur=4.4),
    mis("se llama CHIM", "CHIM", "«Yo soy»", dur=4.0, y=.30),
    pil([("talos", "Talos"), ("vivec", "Vivec")], "Se dice que Talos y Vivec", ("paró una luna", .5), ["Talos y Vivec", "el otro paró"],
        "chim", x=.30, y=.60),
    mis("no sale en ningún juego", "El número uno", "Fuera del juego", dur=4.4, y=.30),

    # ================= CIERRE
    podi([("anu_padomay", "El Soñador"), ("anu_padomay", "Anu"), ("sithis", "Padomay")], "Este es el podio", ("la pelea entre siete", .3),
         ["Este es el podio", "Anu, Padomay, y el que", "y el que sueña"], "El podio"),
    aba([("azura", "Azura"), ("boethiah", "Boethiah"), ("martin", "Héroe de Kvatch")], "¿Quién falta?", ("Déjalo en los comentarios", .5),
        ["Quién falta", "Azura, Boethiah", "Boethiah, el Héroe"], "faltan", x=.30, y=.62),
    mis("Suscríbete si aún no", "Crónicas de Tamriel", "Suscríbete", dur=6.0, y=.30),
]

# ---- SIETE VOCES: placa de quién narra en cada cambio de voz; papeleta de la votación en el cierre
VOCES = ["Johnny", "Edoardo", "Hope", "José", "Mario", "MariCarmen", "el Profeta"]
_LEMA = {"Johnny": "El veinte y el diecinueve", "Edoardo": "El dieciocho y el diecisiete", "Hope": "El doce, el once y el diez",
         "José": "El dieciséis y el quince", "Mario": "El catorce y el trece", "MariCarmen": "El nueve, el ocho y el siete",
         "el Profeta": "Del seis al uno · 8 votos"}
_HUMANO = "el Humano tras el Telón"


def narra(en, nombre, dur=4.0, lema=None):
    n = VOCES.index(nombre) + 1 if nombre in VOCES else None
    return dict(tipo="mg", fn=T.narrador(nombre, lema or _LEMA.get(nombre, "Crítico n.º 1 · un dato, uno solo"), n, 7 if n else None),
                en=en, dur=dur, x=.80, y=.83, sale=.35, nombre="placa narra " + nombre, ver=1.2)


NARRA = [
    narra("Primero, el marcador", "Johnny"),
    narra("Cero votos, y sigo siendo", "Edoardo"), narra("José. Dieciséis y quince", "José"), narra("Mario. Catorce y trece", "Mario"),
    narra("Hope. Doce, once", "Hope"), narra("MariCarmen. Nueve, ocho", "MariCarmen"), narra("Del seis al uno", "el Profeta"),
    narra("Y a mí me tocan los dos últimos", "Johnny"),
    narra("Gracias, Johnny. Ahora", "Edoardo"), narra("Yo no soy. Yo tengo", "Hope", dur=2.4), narra("Yo menos. Yo amenazo", "MariCarmen", dur=2.4),
    narra("Bueno. Si Ebre", "Edoardo"), narra("Gracias igualmente, Ebre", "Johnny", dur=3.0),
    narra("José. Número dieciséis", "José"), narra("Muy profundo, José", "Mario"),
    narra("Y a @PokeGoDLegacy", "Hope", dur=3.0), narra("Y este es para alguien especial", "Johnny", dur=3.0),
    narra("Gracias, Krisstian", _HUMANO, dur=6.0), narra("Un dato. Y ya", "Johnny", dur=2.6),
    narra("Gracias, señor del micrófono", "Hope"), narra("Gracias, Hope. Mi turno", "MariCarmen"),
    narra("Antes del top seis", "MariCarmen"), narra("Llegamos al seis", "el Profeta"),
    mg(T.votacion("¿Qué voz se queda?", VOCES, "Un nombre en los comentarios"), "Y vota otra vez", ("Me los dan", .4),
       ["Johnny, Edoardo, Hope", "Edoardo. Posh", "Hope. Con hache. Y con", "José. Dos dioses", "Mario. Corrí", "MariCarmen. Tres príncipes",
        "Yo no pido votos", "Un nombre, y listo"], "votación", y=.45),
]
# ---- RELLENO de los tramos vacíos > 6 s (`_huecos.py`, s3 6-nov): una pegatina, ficha o abanico donde la voz nombra algo
EXTRA = [
    ficha("Spoiler: no nos pusimos", "Acuerdo entre las voces", "Grado de acuerdo: *0 %*", "Siete voces, una lista", dur=4.0),
    cam("Edoardo. El dieciocho y", "miraak", "Miraak", dur=3.2, x=.16, y=.66),
    cam("y el diecisiete. Cero", "pelinal", "Pelinal", dur=3.2, x=.84, y=.66),
    ban("En Oblivion lo tienes al final de la misión", "mannimarco", "Mannimarco", "El final del Gremio de Magos", dur=4.2),
    ficha("en Daggerfall, la leyenda dice", "El Rey de los Gusanos", "Asciende en la *Distorsión del Oeste*", "The Elder Scrolls II: Daggerfall",
          dur=4.6),
    pv("el Nerevarine, para que puedas", "nerevar", "El Nerevarine", dur=4.0, x=.80, y=.62, tam=380, marco="polaroid"),
    ficha("Cuatro mil años, la cura", "Divayth Fyr", "Más de *4 000* años · cura el *Corprus* · *4* clones", "Puesto 19", dur=5.0),
    pv("En el contenido Dragonborn, vuelve", "solstheim", "Solstheim", dur=4.2, x=.80, y=.60, tam=400, marco="estampilla"),
    pv("Umaril no estaba muerto", "umaril", "Umaril el Desplumado", dur=4.4, x=.80, y=.60, tam=400),
    ficha("reliquia a reliquia", "Reliquias del Cruzado", "*8* piezas: yelmo, coraza, espada, maza…", "Oblivion · Los Caballeros de los Nueve",
          dur=4.4),
    ficha("Y pronuncio Whitestrake", "Pronunciación de Whitestrake", "Nivel: *perfecto*", "Fuente: el propio Edoardo", dur=4.0),
    cam("te recibe como a un viejo amigo", "dagoth_ur", "Dagoth Ur", dur=4.0, x=.84, y=.64, tam=320),
    ficha("Y años después, la roca cayó", "Baar Dau", "Cae sobre Vivec en el *Año Rojo*", "Cuarta Era, año 5", rojo=True, dur=4.4),
    pv("Los antiguos nórdicos se rebelaron", "pergamino_sr", "Pergamino Antiguo", dur=4.4, x=.80, y=.60, tam=380, marco="pergamino"),
    pv("Lo contamos en el video de los dwemer", "numidium", "Numidium", dur=4.2, x=.80, y=.60, tam=420, marco="naipe"),
    ficha("Y no llega al top diez", "Numidium", "Puesto *11*. Sí, *once*.", "Lo dejamos ahí", rojo=True, dur=4.0),
    zoom("Un robot que conquista", ("no llega al top diez", 1.5), 1.10),
    ficha("intentó lo imposible: el Planemeld", "El Planemeld", "Fundir *Nirn* con *Coldharbour*", "The Elder Scrolls Online", dur=5.0),
    aba([("sheogorath", "Sheogorath"), ("jyggalag", "Jyggalag")], "así que en este puesto hay dos príncipes",
        ("uno de ellos. En el siete", -.3), ["así que en este puesto", "hay dos príncipes"], "dos principes"),
    sil("No tiene cara: es una masa", "hermaeus", "Hermaeus Mora", "Ojos y tentáculos", dur=4.6, lado="der"),
    cam("el señor de Miraak", "miraak_db", "Miraak", dur=3.4, x=.16, y=.66),
    cam("Dagon destruye", "dagon", "Mehrunes Dagon", dur=3.0, x=.16, y=.66),
    cam("y Sheogorath enloquece", "sheogorath", "Sheogorath", dur=3.0, x=.84, y=.66),
    ficha("dibujó los planos de Mundus", "Magnus", "Arquitecto de *Mundus*", "Aedra · el ojo que huyó", dur=4.6),
    cam("los magos de Tamriel lo veneran", "galerion", "Los magos", dur=3.4, x=.16, y=.66),
    ficha("Cada vez que miras el sol", "El Sol", "El agujero que dejó *Magnus*", "Skyrim", dur=4.6),
    zoom("Esos agujeros son las estrellas", ("Cada vez que miras el sol", 3.0), 1.12),
    pv("Alduin incluido", "alduin", "Alduin", dur=3.6, x=.80, y=.60, tam=380, marco="estampilla"),
    pv("se enfrenta a Mehrunes Dagon en plena", "dagon", "Mehrunes Dagon", dur=4.4, x=.80, y=.58, tam=420, marco="carta"),
    pv("el alma de dragón del Sangre", "dovahkiin", "El Sangre de Dragón", dur=4.4, x=.18, y=.60, tam=400, marco="vitral"),
    ficha("Todo lo que gritas", "Thu'um", "Un regalo de *Akatosh*", "Según la tradición", dur=3.8),
    ficha("una trampa que los atrapaba", "Lorkhan", "Estado: *muerto*. Más o menos.", "Puesto 4", rojo=True, dur=4.4),
    cam("el padre al que reza", "sithis", "Sithis", dur=3.6, x=.84, y=.64),
    pv("Anu es la quietud", "anu_padomay", "Anu", dur=4.0, x=.80, y=.60, tam=400, marco="vitral"),
    aba([("akatosh", "Akatosh"), ("magnus", "Magnus"), ("talos", "Los Nueve")], "Akatosh, Magnus, los Nueve",
        ("todos le deben su existencia", 1.5), ["Akatosh, Magnus", "Magnus, los Nueve", "los Nueve: todos"], "hijos de Anu"),
    ficha("con los restos de aquella pelea", "Nirn", "Hecho de los *restos* de la pelea", "Según el Anuad", dur=4.4),
    pv("Y de la sangre de los dos", "auriel", "Los dioses", dur=3.8, x=.18, y=.60, tam=380, marco="vitral"),
    zoom("Tamriel, Skyrim, tú", ("Por eso Anu está por encima", 1.0), 1.12),
    cam("Tamriel, Skyrim, tú", "dovahkiin", "Tú", dur=3.0, x=.84, y=.66),
    ficha("Por eso Anu está por encima", "Anu contra Padomay", "Gana *Anu*. Por *muy poco*.", "Puesto 2 y 3", dur=5.0),
    ficha("Según una de las ideas más famosas", "El Soñador", "El *Godhead* sueña el universo", "Según el lore", dur=4.6),
    cam("Todos estaríais dentro", "dovahkiin", "Tú también", dur=3.4, x=.16, y=.66),
    ficha("Y hay una forma de saberlo", "CHIM", "Saber que *estás soñado* y decir: *yo soy*", "El secreto de Talos y Vivec", dur=4.6),
    pv("los secretos de los dwemer", "yagrum", "Los dwemer", dur=4.4, x=.80, y=.60, tam=380, marco="estampilla"),
]
FX = FX + EXTRA + NARRA
# ---- s3: fichas para llegar a la mediana del canal (chequeo 1,3 → 1,6/min); van DESPUÉS de NARRA para no mover los índices de _ajustes.json
EXTRA2 = [
    ficha("Un hombre que se hizo dios, un dios", "Puestos 12 · 11 · 10", "Un *dios*, un *gólem* y un *príncipe*", "Le tocan a Hope", dur=4.2),
    ficha("el gran héroe de los chimer", "Voryn Dagoth", "A solas con el *Corazón de Lorkhan*", "Batalla de la Montaña Roja", dur=4.2),
    ficha("Wraithguard, para que puedas", "Wraithguard", "Toca el *Corazón* sin morir", "Morrowind · te lo da Vivec", dur=4.2),
    ficha("Desde entonces resucita dragones", "Alduin", "Resucita *dragones* en sus túmulos", "Skyrim · 4E 201", dur=4.2),
    ficha("Un gigante de cuatro brazos", "Mehrunes Dagon", "En persona en la *Ciudad Imperial*", "Oblivion · 3E 433", dur=4.4),
    ficha("lo llaman una ruptura", "Ruptura de dragón", "El *tiempo* se rompe", "Akatosh es el tiempo", dur=4.2),
]
FX = FX + EXTRA2

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número veinte", "Número dieciocho", "Número dieciséis", "Número catorce",
                                                                 "Número doce", "Número nueve", "Llegamos al seis")]
PISTAS += [dict(sfx="mision_iniciada", en=e, vol=.20) for e in ("el mago que más ha vivido", "el caballero que cayó", "el dios poeta",
                                                                "Y en el trece", "En el once", "En el diez", "En el ocho", "En el siete",
                                                                "En el cinco", "En el cuatro", "En el tres", "En el dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in ("en Solstheim", "envió la plaga", "Solo lo mandaron", "lo lanzó contra",
                                                                  "se abrieron puertas", "En el Colegio de Hibernalia")]
PISTAS += [dict(sfx="subir_nivel", en="Y el número uno", vol=.24), dict(sfx="subir_nivel", en="Esta es la tabla", vol=.18),
           dict(sfx="mision_completada", en="Este es el podio", vol=.22), dict(sfx="grito", en="con el grito Abatir", vol=.22),
           dict(sfx="grito", en="era Doblegar Voluntad", vol=.20),
           dict(sfx="madre_noche", en=("dejó Padomay.|fin", .15), vol=.85)]   # «oyes a la Madre Noche» = se oye (DarkSagor _kRKQ9XYLwI, 32,2 s)

# ---- AJUSTES de `_desencimar.py` (índices de FX sin ajustar)
import json as _json  # noqa: E402

_AJ = os.path.join(_AQUI, "_ajustes.json")
if os.path.exists(_AJ) and not os.environ.get("FAB_SIN_AJUSTES"):
    for _k, _v in sorted(_json.load(open(_AJ, encoding="utf-8")).items(), key=lambda kv: -int(kv[0])):
        _d = FX[int(_k)]
        if _v.get("quitar"):
            FX.pop(int(_k))
            continue
        if "retraso" in _v:
            _e = _d["en"]
            _d["en"] = (_e[0], _e[1] + _v["retraso"]) if isinstance(_e, tuple) else (_e, _v["retraso"])
        if "dur" in _v:
            _d["dur"] = _v["dur"]
