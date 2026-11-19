# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 20 ARMADURAS más poderosas de Skyrim» (SECUENCIA YT, Crónicas de Tamriel, 18-nov-2026).
REGLA DE ORO (tes_secretos_40) + kits del 5-nov: pegatinas `pv()` con el rotador, estilos de peg_estilos (reliquia, camafeo,
abanico), presentaciones (carrusel en el gancho, podio final), mapas con ruta y `entrada=` (coordenadas UESP de
`_coords.txt`, corregidas el 18-nov), fichas de inventario con las cifras del guion (investigacion.md) y MG NUEVOS de este
video: `mg_tes.tope` (el tope de armadura, la gema) y `mg_tes.conjunto` (conjunto pieza a pieza).
Cada puesto: aviso → ficha de la pieza → pegatinas de PNJ/objeto/lugar en su segundo → MG o mapa.
    python fab.py tes_armaduras_poderosas fx --seco      FAB_FX_FINAL=1 python fab.py tes_armaduras_poderosas fx hoja
"""
import os

import mg_tes as T
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


# ---------------------------------------------------------------- helpers (de tes_builds_rotas)
def pv(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **anim):
    import peg_anim as PA
    fn = PA.variado(P(slug), titulo, tam, tema=TEMA_PEG, **anim)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.06, nombre="pegatina " + slug, ver=1.0)


def _pres(fn, de, a, marcas, nombre):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=.5, y=.5, sale=.06, nombre=nombre, ver=4.0)


def _f(fotos):
    return [(P(s), n) for s, n in fotos]


def carr(fotos, de, a, marcas, titulo=None, marco="carta"):
    import presenta as PR
    return _pres(PR.carrusel(_f(fotos), tema=TEMA_PEG, marco=marco, titulo=titulo), de, a, marcas, "carrusel")


def podi(tres, de, a, marcas, titulo=None):
    import presenta as PR
    return _pres(PR.podio(_f(tres), titulo, TEMA_PEG), de, a, marcas, "podio")


def ficha(en, nombre, efecto, origen=None, dur=4.5, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def rel(en, slug, nombre=None, sub=None, dur=4.0, x=.24, y=.52, tam=460):
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.0, x=.16, y=.70, tam=280, foco=(.5, .25, 1.6)):
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.30, y=.66, tam=300):
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def mis(en, arriba, titulo, dur=3.0, y=.30):
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30, tam=760):
    return dict(tipo="mg", fn=T.pegatina(P("com_" + cid), "", tam, giro=-3.0), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina com_" + cid, ver=1.0)


def aviso(en, n, titulo, dur=3.4):
    return dict(tipo="mg", fn=T.mision(f"Armadura número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


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


# ---------------------------------------------------------------- coordenadas UESP (mapas/skyrim.jpg, `_coords.txt`)
FALKREATH, HAEMAR, CARRERA = (.434, .753), (.622, .739), (.539, .525)
YSGRAMOR, BLOATED, SOLEDAD = (.696, .156), (.414, .610), (.342, .202)
VOLKIHAR, DARKFALL, VALLE = (.090, .078), (.146, .294), (.079, .287)
RIFTEN, RATONERA, NIGHTINGALE = (.887, .783), (.886, .785), (.887, .814)
DEEPWOOD, HAGS = (.193, .272), (.213, .273)
MARKARTH, PERYITE, BTHARDAMZ = (.108, .488), (.169, .389), (.127, .371)
HIBERNALIA, COLEGIO, LABERINTIA = (.729, .208), (.744, .183), (.450, .382)
VALTHUME, SHEARPOINT, RAGNVALD, FORELHOST = (.242, .594), (.648, .448), (.107, .426), (.913, .832)
HIGHGATE, VOLSKYGGE = (.444, .198), (.198, .237)
VENTALIA, SACELLUM, KNIFEPOINT = (.792, .402), (.852, .428), (.344, .697)
RORIK, AKATOSH, JORRVASKR = (.307, .484), (.306, .459), (.557, .516)

# ---------------------------------------------------------------- comentarios (≤ 10 días, ninguno usado antes; ESTADO.md)
C_RELATOR, C_ZAARON, C_REYES = "Ugxy5ePb3AWRBPD8xJB4AaABAg", "Ugzyn__lkzP15KqZ4QB4AaABAg", "Ugwtnk34PMzxein1fUp4AaABAg"
C_IVAN, C_CARLOS = "UgxhEFq1wjJsRFr5vE14AaABAg", "UgzbKO5gwFnTM7bLC8V4AaABAg"
C_FRANK, C_LAGARTIJA, C_STRATOS = "UgzKyDTDkWHZ4-kJW5F4AaABAg", "UgzLa-TRUXRuUqlewCd4AaABAg", "UgzGy_AVtPT252GZ43t4AaABAg"

FX = [
    # ================= GANCHO: un elemento nuevo cada 2-3 s
    zoom(0.0, "Hoy, las veinte armaduras", 1.12),
    pv("Una máscara que, cuando estás", "konahrik", "Konahrik", dur=2.8, x=.80, y=.58, tam=380, entrada="tinta"),
    rel("Una coraza que solo te dan", "cota_ebano", "Cota de ébano", "Precio: tu seguidor", dur=3.0, x=.22, y=.52, tam=440),
    pv("Y un casco que escupe vapor", "mzund", "Semblante de Mzund", dur=2.6, x=.80, y=.58, tam=340, entrada="cristal"),
    pv("Un pirata que enterró", "haknir", "Haknir Estigma Mortal", dur=2.8, x=.20, y=.60, tam=340, marco="polaroid"),
    pv("Y una túnica que hace brotar", "miraak_tunica", "Túnica de Miraak", dur=2.6, x=.80, y=.58, tam=340, entrada="ceniza"),
    mis("Hoy, las veinte armaduras", "Crónicas de Tamriel", "Las 20 ARMADURAS más poderosas", dur=3.0, y=.30),
    carr([("mzund", "Cascos"), ("anulador", "Escudos"), ("archimago", "Túnicas"), ("ruisenor", "Conjuntos")],
         "Cascos, escudos, túnicas", ("la trampa de cada una", .3), ["Cascos", "escudos", "túnicas", "y conjuntos enteros"],
         titulo="Lo que entra en el top"),
    aba([("hierro", "Hierro"), ("daedrica", "La mejor")], "una armadura de hierro puede", ("la mejor del juego", .8),
        ["una armadura de hierro", "la mejor del juego"], "hierro y daedrica", x=.28),
    ficha("exactamente igual que la mejor", "Armadura de hierro", "Protege *igual* que la mejor", "Te lo demuestro al final", dur=3.6),

    # ================= 20 · SEMBLANTE DE MZUND
    aviso("Número veinte", 20, "Semblante de Mzund"),
    ficha("Un casco dwemer de Drágon-born", "Semblante de Mzund", "*24* de armadura · *12* de peso · *+60* de aguante",
          "Casco dwemer · Dragonborn", dur=4.6),
    rel("Pero lo importante es su poder", "mzund", "Semblante de Mzund", "Aliento de Nchuak", dur=4.4),
    ficha("Una ráfaga de vapor abrasador", "Aliento de Nchuak", "Vapor: *15* de daño por segundo", "Poder del casco", dur=4.0),
    mis("Una tetera con cuernos", "Física dwemer", "Una tetera con cuernos", dur=3.0, y=.30),
    pv("Está en el Gran Salón de Fahlbtharz", "fahlbtharz", "Gran Salón de Fahlbtharz", dur=3.6, x=.20, y=.60, tam=420, marco="museo"),
    mg(T.contadores("Gran Salón de Fahlbtharz", [("Accionadores con núcleo dinamo", 3, None, 0), ("Centuriones guardianes", 2, 0, 1)],
                    remate=("Y TRAS LA REJA, EL CASCO", 2)),
       "Primero el puzle de la caldera", ("directo a la nieve", .4), ["Luego llenas tres accionadores", "despiertan dos centuriones",
                                                                      "Tras la reja, el casco"], "contador fahlbtharz", y=.36, x=.70),

    # ================= 19 · MÁSCARA DE CLAVICUS VILE
    aviso("Número diecinueve", 19, "Máscara de Clavicus Vile"),
    ficha("Veintitrés de armadura y solo siete", "Máscara de Clavicus Vile", "*23* de armadura · *7* de peso · precios *20 %* mejores",
          "Persuasión · regeneración de magia", dur=4.6),
    rel("Para tenerla, la misión", "clavicus_mascara", "Máscara de Clavicus Vile", "El mejor amigo de un daedra", dur=4.0),
    pv("El perro habla", "barbas", "Barbas", dur=3.4, x=.80, y=.60, tam=380, entrada="vuela"),
    mapa("skyrim.jpg", "Falkreath", [pt(FALKREATH, "Falkreath", "inicio", "barbas"), pt(HAEMAR, "Vergüenza de Haemar", "meta", "clavicus")],
         "Barbas te lleva a Vergüenza", ("el Hacha pesarosa", 1.0), ["Barbas te lleva", "el santuario de Clávicus"],
         "Vergüenza de Haemar", entrada="foco"),
    ficha("Y al final te da a elegir", "El trato", "*La máscara* y Barbas vive · o el *hacha*", "Las dos cosas, no", dur=5.0),
    mis("Es un daedra del trato", "Clavicus Vile", "No es una tienda de descuentos", dur=3.2, y=.30),
    aba([("clavicus_mascara", "Máscara"), ("cota_ebano", "Cota de ébano")], "si te la pones con la Cota", ("pero con descuento", .5),
        ["si te la pones", "con la Cota de ébano"], "mascara y cota", x=.28),
    ficha("le puede desaparecer la cabeza", "Error visual", "Tu cabeza: *invisible*", "Máscara + Cota de ébano", dur=4.0, rojo=True),

    # ================= 18 · ESCUDO DE YSGRAMOR
    aviso("Número dieciocho", 18, "Escudo de Ysgramor"),
    rel("El Escudo de Ísgramor", "ysgramor_escudo", "Escudo de Ysgramor", "Final de los Compañeros", dur=4.4),
    ficha("Treinta de armadura. Un veinte", "Escudo de Ysgramor", "*30* de armadura · *20 %* resistencia a la magia · *+20* de salud",
          "Escudo pesado", dur=4.6),
    pv("Éorlund Melena Gris repara", "eorlund", "Eorlund Melena Gris", dur=3.0, x=.14, y=.62, tam=340),
    pv("el hacha Úuzrad", "wuuthrad", "Wuuthrad", dur=3.0, x=.33, y=.62, tam=300, marco="museo"),
    mapa("skyrim.jpg", "Carrera Blanca", [pt(CARRERA, "Forja del Cielo", "inicio", "eorlund"), pt(YSGRAMOR, "Tumba de Ysgramor", "meta", "ysgramor")],
         "en la Forja del Cielo", ("Solo aparece durante la misión", .5), ["en la Forja del Cielo", "hasta la Tumba de Ísgramor"],
         "Tumba de Ysgramor", ventana=True, ancho=880, x=.70, y=.45),
    ficha("el cofre estará vacío", "Cofre del jefe", "Fuera de la misión: *vacío*", "Solo durante La gloria de los muertos", dur=4.0,
          rojo=True, x=.26),
    mis("Y de ver lo que te ataca", "Primera persona", "Un tercio de la pantalla", dur=3.0, y=.30),

    # ================= CORREO 1 (críticas con contraburla: las voces)
    com("Un momento, que hay correo", C_FRANK, dur=7.0, x=.32, y=.34, tam=820),
    com("Y Lagartija Vaquera", C_LAGARTIJA, dur=5.0, x=.66, y=.62, tam=700),
    mg(T.contadores("Voces en este video", [("Voces distintas", 1, None, 0), ("Cambios de voz", 0, None, None)],
                    remate=("UNA SOLA: EL PROFETA", 1)),
       "Mensaje recibido. Hoy la voz", ("La mala noticia", .2), ["Hoy la voz no cambia", "Una sola, de principio"], "voces", y=.36, x=.70),
    mis("La mala noticia es que es la mía", "Mensaje recibido", "Narra el Profeta", dur=3.2, y=.72),
    pv("Ponte una de estas armaduras", "daedrica", "Protección anti-Profeta", dur=3.6, x=.22, y=.60, tam=400, entrada="sello"),

    # ================= 17 · PIEL DEL SALVADOR
    aviso("Número diecisiete", 17, "Piel del salvador"),
    ficha("Una coraza ligera de Írsin", "Piel del salvador", "*26* de armadura · *6* de peso · *15 %* resistencia a la magia · veneno a la *mitad*",
          "Artefacto de Hircine", dur=5.0),
    pv("conoces a Síndin", "sinding", "Sinding", dur=3.4, x=.20, y=.60, tam=380, marco="polaroid"),
    pv("y Írsin te da su reto", "hircine", "Hircine", dur=3.4, x=.80, y=.58, tam=400, marco="aura"),
    mapa("skyrim.jpg", "Falkreath", [pt(FALKREATH, "Falkreath", "inicio", "sinding"), pt(BLOATED, "Gruta del Hombre Hinchado", "meta", "hircine")],
         "En la Gruta del Hombre Hinchado", ("el Anillo de Írsin", .8), ["En la Gruta del Hombre", "si matas y desuellas"],
         "Gruta del Hombre Hinchado", entrada="pliegue"),
    rel("la Piel del salvador es, literalmente", "salvador", "Piel del salvador", "Piel de hombre lobo", dur=4.4, x=.76, y=.52),
    mis("Moda sostenible", "Moda de Tamriel", "Moda sostenible", dur=2.8, y=.30),
    mg(T.cadena("El truco de Hircine", [("Perdona a Sinding", P("sinding")), ("Matad a los cazadores", None), ("Recibe el anillo", None),
                                      ("Mátalo después", P("sinding")), ("Hircine te da la Piel", P("salvador"))]),
       "Y el truco: perdona a Síndin", ("no lleva la cuenta", .4),
       ["perdona a Síndin", "mata a los cazadores", "recibe el anillo", "Después, mátalo", "Írsin te da también"], "truco hircine", y=.48),

    # ================= 16 · ARMADURA REAL DE VAMPIRO
    aviso("Número dieciséis", 16, "Armadura real de vampiro"),
    ficha("Treinta de armadura, nueve de peso", "Armadura real de vampiro", "*30* de armadura · *9* de peso · magia *+125 %* más rápido",
          "Dawnguard", dur=5.0),
    rel("un solo encantamiento que lo dice todo", "vampiro_real", "Armadura real de vampiro", "Regeneración +125 %", dur=4.4),
    mapa("skyrim.jpg", "Mar de Fantasmas", [pt(SOLEDAD, "Soledad", "inicio"), pt(VOLKIHAR, "Ruinas de Volkihar", "meta", "vampiro_real")],
         "Está en el Castillo Vólkijar", ("junto a una espada de plata", .5), ["Está en el Castillo Vólkijar", "en las Ruinas de Vólkijar"],
         "Castillo Volkihar", entrada="desenrolla"),
    cam("con Serana", "serana", "Serana", dur=3.0, x=.16, y=.72),
    ficha("Y esa sala es la única fuente", "Fuente que reaparece", "Si se pierde, *vuelve* a la sala", "Sala de los ataúdes", dur=4.2),
    pv("la del Señor vampiro", "harkon", "Harkon · Señor vampiro", dur=3.6, x=.20, y=.60, tam=400, marco="carta"),
    mis("el invitado que recoge cosas", "Castillo Volkihar", "El invitado que recoge cosas", dur=3.2, y=.30),

    # ================= 15 · ESCUDO DE AURIEL
    aviso("Número quince", 15, "Escudo de Auriel"),
    rel("El Escudo de Áuriel", "auriel_escudo", "Escudo de Auriel", "Guarda cada golpe", dur=4.4),
    ficha("Treinta y dos de armadura. Y no tiene", "Escudo de Auriel", "*32* de armadura · guarda la energía de *cada bloqueo*",
          "Dawnguard", dur=4.6),
    mg(T.contadores("Carga del Escudo de Auriel", [("Bloqueos", 15, None, 1)], remate=("ONDA: FUERZA IMPLACABLE", 2)),
       "A los cinco bloqueos", ("al grito Fuerza implacable", .5), ["A los cinco bloqueos", "A los quince está cargado", "suelta una onda"],
       "carga auriel", y=.36, x=.70),
    mapa("skyrim.jpg", "Dawnguard", [pt(DARKFALL, "Cueva Darkfall", "inicio"), pt(VALLE, "Valle Olvidado", "meta", "auriel_escudo")],
         "Se consigue en el Valle Olvidado", ("abres el portal", .8), ["Se consigue en el Valle", "Le quitas el Modelo"],
         "Valle Olvidado", entrada="mesa"),
    cam("el Modelo de perfección de rubí", "rubi", "Modelo de perfección", dur=3.0, x=.16, y=.72, foco=(.5, .5, 1.0)),
    pv("un Belígero falmer pelea", "falmer_beligero", "Belígero falmer", dur=3.6, x=.20, y=.60, tam=400),
    ficha("si usas la onda cargada", "Pelea a puñetazos", "La onda cuenta como *agresión*", "Recompensa por pegar bien", dur=4.2, rojo=True),

    # ================= 14 · RELIQUIAS DE AHZIDAL
    aviso("Número catorce", 14, "Reliquias de Ahzidal"),
    pv("Siete piezas de un antiguo", "ahzidal_armadura", "Reliquias de Ahzidal", dur=3.6, x=.80, y=.58, tam=440, marco="museo"),
    mg(T.conjunto("Reliquias de Ahzidal", [("coraza", "Armadura · parálisis 5 %", P("ahzidal_armadura")), ("botas", "Botas · andar sobre el agua", None),
                                          ("guanteletes", "Guanteletes · absorben 50 %", None), ("casco", "Máscara · más fuego", None)],
                  bonus=("4 RELIQUIAS: +10 A ENCANTAMIENTO", 4)),
       "La armadura de castigo", ("Un genio con problemas", .4),
       ["La armadura de castigo", "Las botas: caminar", "Los guanteletes: absorben", "Y la máscara de Azídal", "Con cuatro reliquias puestas"],
       "conjunto ahzidal", y=.50),
    mis("Con cinco se apaga", "Genio de Ahzidal", "Con cinco se apaga", dur=3.0, y=.30),
    pv("de Rális Sedáris", "ralis", "Ralis Sedarys", dur=3.4, x=.20, y=.60, tam=380),
    mg(T.contadores("La excavación de Ralis", [("Primer pago", 1000, None, 0), ("Segundo pago", 2000, 0, 1), ("Tercer pago", 3000, 1, 2),
                                               ("Cuarto pago", 5000, 2, 3)], remate=("11 000 DE ORO", 4)),
       "en cuatro pagos", ("Once mil de oro en total", 1.0), ["en cuatro pagos", "dos mil, tres mil", "tres mil y cinco", "y cinco mil",
                                                              "Once mil de oro"], "pagos ralis", y=.36, x=.70),
    pv("el propio Azídal sale a pelear", "ahzidal", "Ahzidal", dur=3.8, x=.78, y=.58, tam=440, marco="aura"),
    mis("Inversión segura", "Arqueología", "Inversión segura", dur=3.0, y=.30),
    ficha("Ah, y con las botas", "Botas de Ahzidal", "Salto *más alto* sobre el agua · *peces* a mano", "Reliquia", dur=4.4),

    # ================= AGRADECIMIENTOS (5)
    com("Antes del top trece", C_ZAARON, dur=6.0, x=.30, y=.30, tam=740),
    com("@Reyes3019", C_REYES, dur=5.0, x=.70, y=.32, tam=680),
    com("Con este video ya sé", C_IVAN, dur=4.6, x=.30, y=.68, tam=640),
    com("@RelatorNoctambulo, con diez likes", C_RELATOR, dur=6.0, x=.32, y=.34, tam=760),
    ficha("nos dejó su build antimagia", "Build de @RelatorNoctambulo", "Bretón · piedra del *Señor* · *piel de dragón*",
          "Armadura pesada con resistencias", dur=4.6, x=.72, y=.68),
    com("El profeta tiene mucha aura", C_CARLOS, dur=5.0, x=.66, y=.34, tam=700),
    mis("Pero gracias por decirlo", "Aura del Profeta", "Confirmada", dur=3.0, y=.72),

    # ================= 13 · MAESTRE DEL GREMIO
    aviso("Número trece", 13, "Armadura de maestre del gremio"),
    ficha("Cuatro piezas de cuero", "Maestre del gremio", "*76* de armadura · *17* de peso", "Cuero · 4 piezas", dur=4.4),
    mg(T.conjunto("Maestre del gremio", [("coraza", "Armadura · +50 de carga", P("maestre")), ("botas", "Botas · carterista", None),
                                         ("guanteletes", "Guantes · ganzúas", None), ("casco", "Capucha · precios 20 %", None)]),
       "La armadura: más cincuenta", ("Te la entrega Tonília", -.1), ["La armadura: más cincuenta", "Botas: carterista",
                                                                            "Guantes: ganzúas", "Y la capucha"], "conjunto maestre", y=.50),
    pv("Te la entrega Tonília", "tonilia", "Tonilia", dur=3.6, x=.20, y=.60, tam=380),
    mapa("skyrim.jpg", "La Grieta", [pt(RATONERA, "Riften · La Ratonera", "meta", "maestre")],
         "Te la entrega Tonília", ("bajo Ríften", .8), ["en la Ratonera bajo Ríften"], "Ratonera", ventana=True, ancho=820, x=.70, y=.45,
         entrada="foco"),
    mis("Si tu oficina es la casa de otro", "Trabajo de oficina", "En casa ajena", dur=3.0, y=.30),
    pv("Mercer Frey llevaba una versión", "mercer", "Mercer Frey", dur=4.0, x=.80, y=.58, tam=400, marco="carta"),
    ficha("Mercer siempre se quedaba", "Versión de Mercer", "Más armadura · *sin encantar*", "No te la puedes poner", dur=4.0, x=.26),

    # ================= 12 · ARMADURA ETÉREA ANTIGUA
    aviso("Número doce", 12, "Armadura etérea antigua"),
    rel("La de la Hermandad Oscura", "eterea", "Armadura etérea antigua", "La buena", dur=4.0),
    mg(T.barras("Peso del conjunto entero", [(P("eterea"), "Etérea antigua", 7.5, 1, T.ORO), (P("maestre"), "Maestre del gremio", 17, 0, T.HUESO),
                                             (P("ruisenor"), "Ruiseñor", 18, 0, T.HUESO)], unidad="", remate=("LA MÁS LIGERA DEL TOP", 1)),
       "Setenta y dos de armadura y apenas", ("el conjunto más ligero de esta lista", .8), ["Setenta y dos de armadura", "el conjunto más ligero"],
       "peso etérea", y=.42),
    ficha("Inmunidad total al veneno", "Etérea antigua", "Veneno: *inmune* · botas *silenciosas*", "Coraza y botas", dur=3.2),
    ficha("La capucha, un treinta y cinco", "Capucha y guantes", "Arco *+35 %* · furtivo a una mano *×2*", "Capucha y guantes", dur=4.4),
    pv("Gabriella te da la Ficha", "gabriella", "Gabriella", dur=3.0, x=.20, y=.60, tam=360),
    mapa("skyrim.jpg", "La Marca", [pt(CARRERA, "Carrera Blanca", "inicio", "olava"), pt(DEEPWOOD, "Reducto de Bosque Profundo", "paso"),
                                    pt(HAGS, "Punta de la Arpía", "meta", "eterea")],
         "Olava la Débil te lee", ("una palanca que antes no existía", .8), ["Olava la Débil", "detrás del trono", "aparece una palanca"],
         "Punta de la Arpía", entrada="desenrolla"),
    mis("hasta la arquitectura se cree", "Skyrim", "La arquitectura cree en el horóscopo", dur=3.4, y=.30),

    # ================= CORREO 2 (crítica con contraburla: la recompensa del 3:33)
    com("Otro correo", C_STRATOS, dur=8.0, x=.32, y=.34, tam=820),
    ficha("El veneno no es crimen", "El veneno", "*No* es crimen", "Crimen: que te vean", dur=4.0, x=.72, y=.30),
    pv("Era un aficionado", "maestre", "Profesional: maestre del gremio", dur=4.4, x=.78, y=.58, tam=400, entrada="sello"),

    # ================= 11 · ANULADOR DE HECHIZOS
    aviso("Número once", 11, "Anulador de hechizos"),
    rel("El escudo de Périait", "anulador", "Anulador de hechizos", "Escudo de Peryite", dur=4.4),
    ficha("Treinta y ocho de armadura. Y al bloquear", "Anulador de hechizos", "*38* de armadura · custodia de *50* de daño mágico",
          "Sin gemas · sin magia", dur=5.0),
    mapa("skyrim.jpg", "La Marca", [pt(MARKARTH, "Markarth", "inicio"), pt(PERYITE, "Capilla de Peryite", "paso", "peryite"),
                                    pt(BTHARDAMZ, "Bthardamz", "meta", "anulador")],
         "La misión es La única cura", ("a matar a Órkendor", .8), ["La misión es La única cura", "En la Capilla de Périait",
                                                                    "a la ruina dwemer"], "Btardamz", entrada="pliegue"),
    cam("Kesh el Aseado te pide", "kesh", "Kesh el Aseado", dur=3.4, x=.16, y=.72),
    mis("la custodia es cóncava", "Detalle oculto", "La custodia es cóncava", dur=3.4, y=.30),
    ficha("Contra un mago muy fuerte", "Límite", "Mago fuerte: la custodia *se rompe*", "Y te tambaleas", dur=4.0, rojo=True),

    # ================= MENCIONES DE HONOR
    mis("dos menciones de honor", "Menciones de honor", "Se quedaron fuera por poco", dur=3.4, y=.30),
    rel("La Corona dentada", "corona_dentada", "Corona dentada", "Ranura del pelo", dur=4.6),
    aba([("corona_dentada", "Corona"), ("konahrik", "Máscara")], "la puedes llevar a la vez", ("Dos cascos en una cabeza", .8),
        ["la puedes llevar a la vez", "Dos cascos"], "corona y mascara", x=.72),
    pv("la armadura falmer pesada", "falmer_pesada", "Falmer pesada", dur=3.6, x=.24, y=.60, tam=400),
    pv("con el casco de cascarudo", "cascarudo", "Casco de cascarudo", dur=3.0, x=.40, y=.64, tam=300, marco="museo"),
    ficha("noventa y siete de armadura", "Falmer pesada + cascarudo", "*97* de armadura · *53* de peso", "Supera al ébano en las dos",
          dur=4.6),

    # ================= 10 · TÚNICA DE ARCHIMAGO
    aviso("Número diez", 10, "Túnica de archimago"),
    rel("No tiene armadura. Pesa uno", "archimago", "Túnica de archimago", "Peso: 1", dur=4.0),
    mg(T.contadores("Túnica de archimago", [("Hechizos de 5 escuelas: % más baratos", 15, None, 0), ("Magia extra", 50, 0, 1),
                                            ("Regeneración de magia: % más rápida", 100, 1, 2)], remate=("SIN ARMADURA · EN EL TOP", 2)),
       "Todos los hechizos de cinco", ("Es tu premio al terminar", 0), ["Todos los hechizos de cinco", "más cincuenta de magia",
                                                                        "se regenera el doble"], "stats archimago", y=.36, x=.70),
    mapa("skyrim.jpg", "Hibernalia", [pt(HIBERNALIA, "Hibernalia", "inicio"), pt(COLEGIO, "Colegio de Hibernalia", "meta", "savos")],
         "El Ojo de Magnus en el Colegio", ("te nombran archimago", .8), ["El Ojo de Magnus en el Colegio", "Derrotas a Ancáno"],
         "Colegio de Hibernalia", ventana=True, ancho=860, x=.70, y=.45),
    pv("Derrotas a Ancáno", "ancano", "Ancano", dur=3.4, x=.20, y=.60, tam=400, entrada="glitch"),
    aba([("archimago", "Túnica"), ("morokei", "Morokei")], "puedes llevarla con una máscara", ("otro cien por ciento", .8),
        ["puedes llevarla con una máscara", "Con Morokéi"], "tunica y morokei", x=.28),
    ficha("Con Morokéi, otro cien", "Túnica + Morokei", "Regeneración *+100 %* y otro *+100 %*", "Fallo de ranura · vale oro", dur=4.4),
    mis("Lo intenté", "Sovngarde", "No se la puedes robar", dur=3.0, y=.30),

    # ================= 9 · ARMADURA DE RUISEÑOR
    aviso("Número nueve", 9, "Armadura de Ruiseñor"),
    pv("Cuero negro y morado", "ruisenor", "Armadura de Ruiseñor", dur=4.0, x=.20, y=.58, tam=440, marco="aura"),
    ficha("Sesenta y nueve de armadura", "Armadura de Ruiseñor", "*69* de armadura · *18* de peso · *+25* con las 4 piezas",
          "Cuero · Nocturnal", dur=4.4),
    mg(T.conjunto("Armadura de Ruiseñor", [("coraza", "Aguante · escarcha", P("ruisenor")), ("botas", "Botas silenciosas", None),
                                           ("guanteletes", "Ganzúa · una mano", None), ("casco", "Ilusión más barata", None)],
                  bonus=("CONJUNTO: +25 DE ARMADURA", 3)),
       "Aguante y resistencia a la escarcha", ("Ilusión más barata en la capucha", .8),
       ["Aguante y resistencia", "botas silenciosas#2", "ganzúa y más daño", "e Ilusión más barata"], "conjunto ruisenor", y=.50),
    mapa("skyrim.jpg", "La Grieta", [pt(RIFTEN, "Riften", "inicio", "brynjolf"), pt(NIGHTINGALE, "Salón de los Ruiseñores", "meta", "nocturnal")],
         "La recibes en La vuelta", ("le juras lealtad a Nocturnal", .8), ["La recibes en La vuelta", "en el Salón de los Ruiseñores"],
         "Salón de los Ruiseñores", entrada="pliegue"),
    cam("con Kárlia y Brynjolf", "karliah", "Karliah", dur=3.0, x=.16, y=.72),
    ficha("se fija con tu nivel", "La trampa", "La versión se fija al *EMPEZAR* la misión", "No al recibirla", dur=4.4, rojo=True),
    ficha("Si la empiezas antes del nivel", "Antes del nivel 32", "Versión débil *para siempre*", "Ruiseñor", dur=4.0, rojo=True, x=.26),
    pv("Nocturnal, diosa de la suerte", "nocturnal", "Nocturnal", dur=3.6, x=.78, y=.58, tam=420, marco="aura"),

    # ================= 8 · KONAHRIK
    aviso("Número ocho", 8, "Konahrik"),
    rel("La máscara del Señor de la guerra", "konahrik", "Konahrik", "Señor de la guerra", dur=4.4),
    ficha("Veinticuatro de armadura: el casco", "Konahrik", "*24* de armadura base: el casco *más alto* del juego original",
          "Despierta con salud bajo el *15 %*", dur=5.0),
    mg(T.barras("Si tu salud baja del 15 %", [(None, "Explosión · llamas · gran curación", 15, 0, T.HUESO),
                                              (None, "Sacerdote dragón espectral · 60 s", 3, 1, T.ORO)], unidad=" %"),
       "Con un quince por ciento de probabilidad", ("durante sesenta segundos", .6),
       ["Con un quince por ciento de probabilidad", "Y con un tres por ciento"], "probabilidades konahrik", y=.42),
    mapa("skyrim.jpg", "Las ocho máscaras", [pt(VALTHUME, "Hevnoraak", "paso"), pt(SHEARPOINT, "Krosis", "paso"), pt(LABERINTIA, "Morokei", "paso", "morokei"),
                                             pt(RAGNVALD, "Otar", "paso"), pt(FORELHOST, "Rahgot", "paso"), pt(HIGHGATE, "Vokun", "paso"),
                                             pt(VOLSKYGGE, "Volsung", "paso"), pt(LABERINTIA, "Santuario de Bromjunaar", "meta", "mascara_madera")],
         "reúnes las ocho máscaras", ("y colocas las ocho en sus bustos", .6), [], "ocho mascaras", entrada="mesa"),
    pv("La máscara de Nákrin solo", "nahkriin", "Nahkriin", dur=3.6, x=.20, y=.60, tam=400, marco="cristal"),
    ficha("solo se consigue en Skúldafn", "Máscara de Nahkriin", "Solo en *Skuldafn*: sin segunda oportunidad", "Misión principal", dur=4.4,
          rojo=True),
    mis("Konájrik, imposible", "Konahrik", "Imposible", dur=2.8, y=.30),
    ficha("borra el templado que les hayas hecho", "Los bustos", "Borran *todo* el templado", "Herrería a la basura", dur=4.0, rojo=True),
    ficha("Y si vendes cualquiera de las ocho", "Vender una máscara", "También *pierde* el templado", "A cualquier mercader", dur=4.0,
          rojo=True, x=.26),
    pv("el Santuario de Bromyúnar iba a ser", "mascara_madera", "Máscara de madera", dur=4.4, x=.20, y=.60, tam=380),
    ficha("iba a ser una casa para el jugador", "Contenido cortado", "Bromjunaar iba a ser *tu casa*", "No llegó a tiempo", dur=4.4),

    # ================= 7 · EQUIPO DE MIRAAK
    aviso("Número siete", 7, "El equipo de Miraak"),
    pv("El equipo de Mirák", "miraak", "Miraak", dur=3.6, x=.80, y=.58, tam=440, marco="aura"),
    mg(T.barras("Absorción de hechizos", [(P("miraak_tunica"), "Túnica de Miraak", 15, 0, T.HUESO), (None, "Botas", 5, 1, T.HUESO),
                                          (None, "Guantes", 5, 1, T.HUESO)], unidad=" %", remate=("25 % EN TOTAL", 2)),
       "La túnica absorbe el quince", ("Un veinticinco por ciento en total", 1.0),
       ["La túnica absorbe", "Las botas y los guantes", "Un veinticinco por ciento en total"], "absorcion miraak", y=.42),
    ficha("brotan del suelo los tentáculos", "Tentáculos de Apócrifa", "Explotan: *100* de daño de veneno", "Al recibir golpes", dur=4.6),
    rel("Su máscara es nivelada", "miraak_mascara", "Máscara de Miraak", "27 a nivel 60", dur=4.4),
    ficha("A nivel sesenta llega", "Máscara de Miraak", "*27* de armadura a nivel *60*", "El casco más protector del juego", dur=4.4),
    mg(T.cadena("En la cima de Apócrifa", [("Los libros negros", None), ("Los capítulos", None), ("Doblegas a Sahrotaar", P("sahrotaar")),
                                          ("La cima: Miraak", P("miraak"))]),
       "Lo consigues matando a Mirák", ("y subes a la cima", 3.2),
       ["Lees los libros negros", "cruzas los capítulos", "doblegas a Sajrotár", "y subes a la cima", ("y subes a la cima", 1.6)],
       "cadena apocrifa", y=.48),
    ficha("llegas al cien por ciento de absorción", "Absorción", "*100 %*: inmune a los hechizos", "Túnica + piedra y ventaja Atronach",
          dur=4.4),
    mis("Inmune, pero con tentáculos", "Miraak", "Inmune, pero con tentáculos", dur=3.0, y=.30),

    # ================= 6 · ESTIGMA MORTAL
    aviso("Número seis", 6, "Armadura de Estigma Mortal"),
    rel("Ligera, de stáljrim", "estigma", "Estigma Mortal", "Stalhrim ligero", dur=4.4),
    ficha("Setenta y ocho y medio de armadura, trece", "Estigma Mortal", "*78,5* de armadura · *13* de peso", "Crece con cada pieza", dur=4.4),
    mg(T.conjunto("Estigma Mortal", [("coraza", "Aguante", P("estigma")), ("botas", "Carga", None), ("guanteletes", "Dos armas a la vez", None),
                                     ("casco", "Respirar bajo el agua", None)], bonus=("4 PIEZAS: +100 DE ARMADURA", 4)),
       "Aguante, carga", ("Más que toda la armadura", 2.0),
       ["Aguante, carga", "carga, y daño", "y daño con dos armas", "Y el yelmo: respiras", "con las cuatro piezas, más cien"],
       "conjunto estigma", y=.50),
    pv("El pirata Jáknir Estigma Mortal", "haknir", "Haknir Estigma Mortal", dur=3.8, x=.80, y=.58, tam=420, marco="aura"),
    pv("hay que leer el mapa del tesoro", "estigma_mapa", "Mapa del tesoro", dur=4.6, x=.26, y=.52, tam=600, marco="polaroid"),
    pv("Otro junto a Tel Mithryn", "estigma_tel", "Cofre junto a Tel Mithryn", dur=3.4, x=.74, y=.53, tam=500, marco="carta"),
    ficha("Y el último cofre trae la llave", "Túmulo de Gyldenhul", "*80* montones de oro · el fantasma de *Haknir*", "Isla de los horkers",
          dur=4.6),
    mg(T.contadores("El tesoro de Haknir", [("Monedas de oro", 6400, None, 1)], remate=("Y DOS CIMITARRAS ÚNICAS", 1)),
       "Con sus dos cimitarras únicas", ("cuatrocientas monedas de oro", 1.6), ["Con sus dos cimitarras", "cuatrocientas monedas"],
       "tesoro haknir", y=.36, x=.70),
    mis("Yo también grito", "Moda póstuma", "La ropa de un muerto", dur=3.0, y=.30),

    # ================= 5 · COTA DE ÉBANO
    aviso("Número cinco", 5, "Cota de ébano"),
    rel("Una coraza pesada de Boétia", "cota_ebano", "Cota de ébano", "Artefacto de Boethiah", dur=4.0),
    mg(T.barras("Coraza pesada: armadura y peso", [(P("cota_ebano"), "Cota de ébano · armadura", 45, 0, T.ORO),
                                                   (P("daedrica"), "Coraza daédrica · armadura", 48, 1, T.HUESO),
                                                   (P("cota_ebano"), "Cota de ébano · peso", 28, 0, T.ORO),
                                                   (P("daedrica"), "Coraza daédrica · peso", 50, 2, T.SANGRE)],
                remate=("3 DE ARMADURA POR 22 DE PESO", 2)),
       "Cuarenta y cinco de armadura y veintiocho", ("y pesa veintidós más", 2.4),
       ["Cuarenta y cinco de armadura y veintiocho", "La daédrica protege solo tres", "y pesa veintidós más"], "ebano contra daedrica", y=.42),
    ficha("Te mueves en silencio, y todo enemigo", "Cota de ébano", "Silencio · *5* de veneno por segundo a quien se acerque",
          "Sombra negra con humo verde", dur=5.0),
    mis("Y hasta funciona como radar", "Radar daédrico", "El humo avisa", dur=3.0, y=.30),
    mapa("skyrim.jpg", "Marca Oriental", [pt(VENTALIA, "Ventalia", "inicio"), pt(SACELLUM, "Próstilo de Boethiah", "paso", "boethiah"),
                                          pt(KNIFEPOINT, "Cresta de Punta del Cuchillo", "meta", "campeon_boethiah")],
         "El precio: La llamada de Boétia", ("que la lleva puesta", .8),
         ["El precio: La llamada", "En el Próstilo de Boétia", "en la Cresta de Punta del Cuchillo"], "Punta del Cuchillo", entrada="desenrolla"),
    pv("la yarla Elisif", "elisif", "Elisif", dur=3.6, x=.80, y=.58, tam=400, marco="polaroid"),
    ficha("una segunda misión que se cortó", "Contenido cortado", "Matar a la jarla *Elisif*", "Restos en los archivos", dur=4.4, x=.26),
    mis("Tu seguidor te cargó la mochila", "Seguidor", "200 horas de mochila", dur=3.2, y=.30),

    # ================= CAMPAÑA (~75 %)
    mg(T.rejilla("De cada cien que ven el canal", n=100, encendidas=13, remate=("Solo 13 suscritos", 1)),
       "De cada cien que ven", ("están suscritos", .6), ["De cada cien que ven", "solo trece están suscritos"], "rejilla suscritos", y=.44),
    mg(T.contadores("Meta del canal", [("Suscriptores", 6930, None, 0), ("La gran meta", 10000, 0, 1)]),
       "Somos casi siete mil", ("sacrificado en un altar", .6), ["Somos casi siete mil", "camino de diez mil"], "meta subs", y=.36, x=.70),
    mis("Un botón", "Misión nueva", "Suscríbete a Crónicas de Tamriel", dur=3.4, y=.72),

    # ================= 4 · STALHRIM
    aviso("Número cuatro", 4, "Armadura de stalhrim"),
    aba([("stalhrim_pesada", "Pesada"), ("stalhrim_ligera", "Ligera")], "La Armadura de stáljrim. Pesada", ("es hielo nórdico encantado", .8),
        ["La Armadura de stáljrim", "Pesada y ligera"], "stalhrim dos", x=.72),
    ficha("El stáljrim es hielo nórdico", "Stalhrim", "Hielo nórdico *encantado*", "Solstheim", dur=3.6, x=.26),
    mg(T.barras("Pesada: armadura y peso", [(P("stalhrim_pesada"), "Stalhrim pesada · armadura", 102, 0, T.ORO),
                                            (P("placas"), "Placas de dragón · armadura", 102, 0, T.HUESO),
                                            (P("stalhrim_pesada"), "Stalhrim pesada · peso", 59, 1, T.ORO),
                                            (P("placas"), "Placas de dragón · peso", 64, 1, T.HUESO)],
                remate=("LA QUE MÁS PROTEGE POR PESO", 2)),
       "La pesada: ciento dos", ("por cada unidad de peso", .8), ["La pesada: ciento dos", "con cinco menos de peso", "Es la armadura forjable"],
       "stalhrim contra placas", y=.42),
    rel("La ligera: setenta y ocho", "stalhrim_ligera", "Stalhrim ligera", "78,5 · peso 13", dur=4.4),
    ficha("los encantamientos de escarcha son", "Sobre stalhrim", "Escarcha *+25 %* más fuerte", "Encantamientos", dur=4.0),
    mg(T.cadena("Un nuevo yacimiento de stalhrim", [("Herrería de ébano", None), ("Déor Tallador", P("deor")), ("Baldor Hierro Forjado", P("baldor")),
                                                   ("Pico nórdico antiguo", None)]),
       "Para forjarla necesitas", ("con el pico nórdico antiguo", 1.0),
       ["Para forjarla necesitas", "Déor Tallador, en la Aldea", "al herrero Baldor", "con el pico nórdico"], "cadena stalhrim", y=.48),
    ficha("si Déor Tallador muere", "Déor Tallador", "Si muere antes: *nunca* podrás forjar stalhrim", "Para siempre", dur=4.4, rojo=True),
    cam("si Déor Tallador muere", "deor", "Déor Tallador", dur=4.0, x=.20, y=.66),
    mis("Toda una isla de hielo", "Solstheim", "Depende de un anciano", dur=3.6, y=.30),
    ficha("stál hrím, en islandés", "Stalhrim", "*Escarcha de acero* en islandés", "stál · hrím", dur=4.0),

    # ================= 3 · ESCAMAS DE DRAGÓN
    aviso("Número tres", 3, "Armadura de escamas de dragón"),
    rel("La mejor armadura ligera del juego original", "escamas", "Escamas de dragón", "La mejor ligera", dur=4.4),
    ficha("Ochenta y dos de armadura y solo veinte", "Escamas de dragón", "*82* de armadura · *20* de peso · con escudo *111*",
          "Armadura ligera", dur=4.6),
    ficha("la ventaja Armadura de dragón", "Armadura de dragón", "Herrería *100* + toda una rama", "Ventaja de herrería", dur=4.0, x=.26),
    mg(T.tope("Escamas de dragón · sin escudo", [("Ligera al máximo + ventajas", 362, "55 %"), ("Templada con herrería", 667, "80 %")],
              tope_=567, maximo=800, remate=("LA ÚNICA LIGERA AL TOPE SIN ESCUDO", 1)),
       "Con Armadura ligera al máximo y todas", ("al tope sin escudo|fin", 1.0), ["Con Armadura ligera al máximo", "Y templada, es la única"],
       "tope escamas", y=.46),
    mapa("skyrim.jpg", "Paraje de Rorik", [pt(RORIK, "Paraje de Rorik", "inicio"), pt(AKATOSH, "Santuario de Akatosh", "meta", "escamas")],
         "En una colina al noreste", ("cada diez días", .8), ["En una colina al noreste", "hay un santuario de Akatosh"],
         "santuario de Akatosh", ventana=True, ancho=860, x=.70, y=.45, entrada="foco"),
    mis("Es la única suscripción", "Akatosh", "La suscripción gratis", dur=3.2, y=.30),

    # ================= 2 · PLACAS DE DRAGÓN
    aviso("Número dos", 2, "Armadura de placas de dragón"),
    rel("Placas de hueso, y un yelmo", "placas", "Placas de dragón", "Yelmo de cráneo", dur=4.4),
    ficha("Ciento dos de armadura y sesenta y cuatro", "Placas de dragón", "*102* de armadura · *64* de peso · con escudo *136*",
          "Armadura pesada", dur=4.6),
    ficha("Se forja con huesos y escamas", "Forja", "*Huesos* y *escamas* de dragón", "Templado: hueso de dragón", dur=4.4, x=.26),
    mg(T.tope("Placas de dragón · con escudo", [("Todo al máximo · sin herrería", 525, "78 %")], tope_=542, maximo=800,
              remate=("A 2 PUNTOS DEL 80 %", 1)),
       "Con todo al máximo, sin tocar", ("del máximo del juego", 1.0), ["Con todo al máximo, sin tocar", "A dos puntos del máximo"],
       "tope placas", y=.46),
    mg(T.barras("Ya en el tope: lo que pesa", [(P("placas"), "Placas de dragón", 79, 0, T.ORO), (P("daedrica"), "Daédrica", 96, 0, T.HUESO)],
                unidad=""),
       "Y una vez templada, llega", ("más fáciles de juntar", .6), ["Setenta y nueve contra noventa"], "peso placas", y=.42),
    pv("en el laboratorio de Valérica", "valerica", "Valerica", dur=3.6, x=.20, y=.60, tam=380),
    ficha("Y con Don-gard hay un hueso", "Laboratorio de Valerica", "Un *hueso de dragón* antes de los dragones", "Dawnguard", dur=4.2),
    mis("te pones su cráneo de sombrero", "Moda nórdica", "Cráneo de sombrero", dur=3.0, y=.30),

    # ================= 1 · DAÉDRICA
    aviso("Número uno", 1, "Armadura daédrica", dur=3.8),
    pv("Negra, con vetas rojas", "daedrica", "Armadura daédrica", dur=4.4, x=.22, y=.54, tam=520, marco="museo"),
    ficha("Ciento ocho de armadura y ochenta y uno", "Armadura daédrica", "*108* de armadura · *81* de peso · con escudo *144*",
          "La pesada más fuerte del juego", dur=4.8),
    rel("Cada pieza lleva un corazón", "corazon_daedra", "Corazón de daedra", "Uno por pieza", dur=4.0, x=.24, y=.52, tam=400),
    mapa("skyrim.jpg", "Skyrim", [pt(JORRVASKR, "Jorrvaskr", "inicio", "corazon_daedra"), pt(VOLKIHAR, "Ruinas de Volkihar", "paso", "corazon_daedra"),
                                  pt(COLEGIO, "Fragua del atronach", "meta", "fragua_atronach")],
         "hay algunos fijos", ("una gema de alma negra", .8), ["uno en Jorrvaskr", "otro en las Ruinas", "la Fragua del atronach"],
         "corazones y fragua", entrada="mesa"),
    cam("Lo sueltan los drémora", "dremora", "Drémora", dur=3.0, x=.16, y=.72),
    ficha("Menos las botas sin encantar", "Fragua del atronach", "Todas las piezas… *menos las botas* sin encantar", "Porque sí",
          dur=4.0, rojo=True),
    mg(T.tope("Armadura daédrica · con su escudo", [("Pesada al máximo + ventajas · sin herrería", 560, "80 %")], tope_=542, maximo=800,
              remate=("EL MÁXIMO: 80 % MENOS DE DAÑO", 1)),
       "Y la razón del número uno", ("ochenta por ciento menos de daño", 1.0), ["Con Armadura pesada al máximo", "Y eso ya es el máximo"],
       "tope daedrica", y=.46),
    mis("Es la única armadura del juego que llega", "Número uno", "Al tope solo con ventajas", dur=3.6, y=.30),
    ficha("no te dejan saquearla", "Drémora", "Te dan el *corazón*. La armadura, *no*", "Botín", dur=4.0),
    ficha("las botas, los guanteletes de mujer", "Fallo de siempre", "Botas, guanteletes de mujer y escudo: *sin brillo rojo*",
          "Desde 2011", dur=4.6, rojo=True),
    mis("se le olvidó enchufar los pies", "Bethesda", "Se le olvidó enchufar los pies", dur=3.2, y=.30),

    # ================= GEMA: el hierro protege igual
    mis("Y ahora, lo que prometí", "Lo prometido", "Hierro contra daédrica", dur=3.4, y=.30),
    ficha("Cada punto de armadura reduce", "Armadura", "Solo daño *físico* · tope *80 %*", "Contra la magia: nada", dur=4.6),
    ficha("armadura oculta, que el menú", "Armadura oculta", "*Cada pieza* suma lo que el menú no enseña", "Con escudo bastan *542*",
          dur=4.6, x=.26),
    mg(T.tope("Con escudo · herrería al máximo", [("Daédrica · sin forja", 560, "80 %"), ("Hierro · templado", 547, "80 %")],
              tope_=542, maximo=800, remate=("EL MISMO 80 %", 2)),
       "Ahora la sorpresa", ("ochenta por ciento que la daédrica.|fin", .3), ["cualquier armadura pesada templada", "Hasta la de hierro", "El mismo ochenta"],
       "tope hierro", y=.46),
    mg(T.tope("Lo que pasa del tope", [("Escamas templada · sin escudo", 667, "80 %")], tope_=567, maximo=800,
              remate=("DESPERDICIO", 0)),
       "Y todo lo que pasa del tope", ("Es desperdicio", .8), ["no te sirve de nada"], "tope desperdicio", y=.46),
    ficha("las armas que atraviesan armadura", "Armas que atraviesan", "Harían falta *más de 2 000*", "Ballestas · mazas · martillos",
          dur=4.4),
    ficha("con la ventaja Condicionamiento", "Condicionamiento", "La armadura pesada *no pesa*", "Armadura pesada", dur=4.4),
    mis("la armadura que elijas es pura moda", "En el tope", "La armadura es pura moda", dur=3.2, y=.30),
    aba([("daedrica", "Daédrica"), ("hierro", "Hierro")], "hasta el hierro te salva igual", ("bien en la foto", .6),
        ["hasta el hierro te salva", "para verte bien"], "foto final", x=.28),

    # ================= CIERRE
    podi([("daedrica", "Daédrica"), ("placas", "Placas de dragón"), ("escamas", "Escamas de dragón")], "Este es el top",
         ("al máximo del juego", 1.2), ["Este es el top", "De un casco que escupe", "al conjunto que llega solo"], "El podio de las armaduras"),
    mis("Ahora te toca a ti", "Te toca", "¿Cuál falta?", dur=3.6, y=.30),
    mis("Y suscríbete, que vamos", "Camino de diez mil", "Suscríbete", dur=3.2, y=.30),
    pv("Radio Yermo, nuestro canal hermano", "radio_yermo", "Radio Yermo · canal hermano", dur=6.0, x=.72, y=.50, tam=520, marco="monitor"),
    ficha("es todo Fallout", "Radio Yermo", "Todo *Fallout*", "Canal hermano · enlace en la descripción", dur=4.4, x=.26),
    mis("Nos vemos en Tamriel", "Crónicas de Tamriel", "Nos vemos en Tamriel", dur=3.0, y=.30),
]

# ---- SFX del JUEGO (banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in (
    "Número veinte", "Número diecinueve", "Número dieciocho", "Número diecisiete", "Número dieciséis", "Número quince", "Número catorce",
    "Número trece", "Número doce", "Número once", "Número diez", "Número nueve", "Número ocho", "Número siete", "Número seis",
    "Número cinco", "Número cuatro", "Número tres", "Número dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.22) for e in (
    "el santuario de Clávicus", "hasta la Tumba de Ísgramor", "En la Gruta del Hombre", "en las Ruinas de Vólkijar", "Le quitas el Modelo",
    "en la Ratonera bajo Ríften", "aparece una palanca", "a la ruina dwemer", "en el Salón de los Ruiseñores", "en la Cresta de Punta del Cuchillo",
    "hay un santuario de Akatosh", "la Fragua del atronach")]
PISTAS += [dict(sfx="monedas", en="Once mil de oro", vol=.30), dict(sfx="monedas", en="cuatrocientas monedas", vol=.30),
           dict(sfx="subir_nivel", en="Número uno", vol=.24), dict(sfx="mision_completada", en="Este es el top", vol=.22),
           dict(sfx="mision_iniciada", en="Y ahora, lo que prometí", vol=.22),
           dict(sfx="grito_bajio", en=("se le oye en el bajío.|fin", .05), vol=.55),   # R17: «aún se le oye» = se oye
           dict(sfx="radio_yermo", en=("escucho esa radio.|fin", .05), vol=.30)]   # R17: «escucho esa radio»
SFX = {"grito_bajio": ("Distant ghostly man screaming in terror, echoing over a cold icy sea shore, eerie wind, no music", 3),
       "radio_yermo": ("Old 1950s tube radio tuning static crackle, brief swing music fragment through static, no vocals", 2)}

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
