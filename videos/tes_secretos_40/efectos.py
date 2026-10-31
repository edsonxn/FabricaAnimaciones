# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Los 40 SECRETOS de Skyrim que nadie te contó» (SECUENCIA YT, Crónicas de Tamriel, 30-oct-2026).
Todo con el kit de interfaz de Skyrim por código (nucleo/mg_tes.py), anclado a palabras de la voz:
- 41 avisos (título del top + uno por puesto), arriba al centro.
- Fichas estilo inventario SOLO con cifras verificadas en UESP (`_investigacion_*.md`), arriba a la derecha.
- Pegatinas con la imagen REAL (Fandom/UESP) de cada personaje u objeto que se nombra; los clave, GRANDES.
- Comentarios REALES (reglas 27/28-oct-2026): gancho @ericmarticorena3842, corrección @stazmadness3910 (29), n.º 1 @Knox8386 y
  agradecimientos @Senpai.13 (30), @AnormalProject (20), @OFSUAREZL + @daybengamers8298 (10), @franciscobarqueromunoz1218 (cierre).
- MG NUEVOS de este guion (regla 19-oct-2026): aguante (sopa, 31) · informe thalmor (7 y 6) · cordura (Cicerón, 2) · nombre
  (Paar-Thur-Nax, 1).
- Mapas reales (tema tes) con FOTO y ruta en 14 puestos: 40, 35, 29, 28, 23, 21, 18, 17, 16, 10, 9, 7, 4 y 3. Coordenadas de la
  base de datos del mapa de UESP calibradas sobre el mapa de papel (`_coords_uesp.py`).
- REHECHO con la revisión del usuario (30-oct-2026): lo anterior SIGUE y se SUMA: MG desde el gancho (rejillas, barras, barra_vida,
  deteccion, semana, estrellas, versiones, vela, soldados, cronologia, cadena, misiones), fichas ≥ 1,6/min, lo que dice la voz se ve
  (Torre Blanca a pantalla completa, Montaña Roja, nave, Martinet, Ramati, Oblivion…), pegatinas variadas (`nucleo/peg_estilos.py`:
  silueta sin fondo a media pantalla, reliquia, banda, camafeo, legajo, abanico), críticas contestadas (cr1, cr2) y campaña de subs.
  python fab.py tes_secretos_40 fx --seco   tiempos      python fab.py tes_secretos_40 fx hoja   previews/fx_NN.jpg
  python fab.py tes_secretos_40 chequeo     densidad contra el canal y narración ↔ imagen
"""
import os

import mg_tes as T
import mg_wow as W
import peg_estilos as PE

CAMARA = {}
FUNDIDO = {}

_FX, _FY = .76, .30            # fichas: arriba a la derecha (no tapan el centro del clip)
_PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pegatinas")   # imágenes reales de la wiki
_MAP = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mapas")
TEMA_MAPA = "tes"


def P(slug):
    return os.path.join(_PEG, slug + ".png")


def J(slug):
    return os.path.join(_PEG, slug + ".jpg")


def ficha(en, nombre, efecto, origen=None, dur=5.0, rojo=False, x=_FX, y=_FY):
    return dict(tipo="mg", fn=T.objeto(nombre, efecto, origen=origen, rojo=rojo), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="ficha " + nombre, ver=1.2)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, giro=-6.0):
    """Pegatina con la imagen REAL de lo que nombra la voz (regla de canal): abajo a la izquierda."""
    return dict(tipo="mg", fn=T.pegatina(P(slug), titulo, tam, giro=giro), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, dur=4.5, x=.25, tam=640):
    """Pegatina GRANDE (media pantalla): los personajes y objetos clave."""
    return peg(en, slug, titulo, dur=dur, x=x, y=.52, tam=tam)


# ---- estilos nuevos de pegatina (el usuario, 30-oct-2026: «que no se sienta que todas son iguales»)
def sil(en, slug, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara bien visible y el video corriendo detrás."""
    fn = PE.silueta(P(slug), nombre, sub, alto=alto, encuadre=encuadre, lado=lado)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    """Objeto sin fondo flotando sobre un círculo de runas."""
    return dict(tipo="mg", fn=PE.reliquia(P(slug), nombre, sub, tam), en=en, dur=dur, x=x, y=y, sale=.35, nombre="pegatina " + slug, ver=1.2)


def ban(en, ruta, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    """Tira de cine a todo lo ancho con el rostro en primer plano."""
    return dict(tipo="mg", fn=PE.banda(ruta, nombre, sub, foco, lado=lado), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="pegatina " + os.path.basename(ruta), ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(P(slug), nombre, tam, foco), en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def leg(slug, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(P(slug), titulo, lineas, sello=sello, ancho=ancho, giro=giro), de=de, a=a, marcas=list(marcas), x=x, y=y,
                sale=.35, nombre="pegatina " + slug, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(slug, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico([(P(s), e) for s, e in fotos], tam), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="pegatina " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    """Imagen REAL a cuadro entero, cuando el clip no enseña lo que la voz dice (la Torre Blanca vista desde Skyrim)."""
    return dict(tipo="pantalla", fn=W.pantalla(P(slug), zoom, pan, oscuro=oscuro), de=de, a=a, entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def mis(en, arriba, titulo, dur=4.0, y=.30):
    """Aviso de misión de Skyrim como remate de un chiste."""
    return dict(tipo="mg", fn=T.mision(arriba, titulo), en=en, dur=dur, y=y, sale=.4, nombre="MG misión " + titulo, ver=1.4)


def com(en, cid, dur=6.0, x=.30, y=.30):
    """Comentario REAL del canal (tarjeta de `fab.py yt comentario`)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=760)


def aviso(en, n, titulo, dur=3.6):
    return dict(tipo="mg", fn=T.mision(f"Secreto · número {n}", titulo), en=en, dur=dur, y=.13, sale=.4, nombre="aviso " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.52, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=1.0)


def mapa(puntos, de, a, marcas, sub, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    fn = MP.mapa(os.path.join(_MAP, "skyrim.jpg"), puntos, TEMA_MAPA, titulo="Skyrim", sub=sub,
                 modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + sub, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + sub, ver=4.0)


# ---- los MG nuevos (solo datos del guion)
def _aguante():
    return T.aguante("Ataques sin fin", (P("sopa"), "Sopa de verduras"), 12, remate=("Por 5 monedas", 1))


def _informe_esbern():
    return T.informe("Informe thalmor · Esbern", (P("esbern"), "Esbern"),
                     [("Dragones", "No entienden por qué han vuelto", 0),
                      ("Rango", "Nunca fue un simple archivero", 1),
                      ("Funcionario que lo descartó", "Enviado a Alinor a ser reeducado", 2)])


def _informe_ulfric():
    return T.informe("Informe thalmor · Ulfric", (P("ulfric"), "Ulfric"),
                     [("Interrogado por", "Elenwen, en la Gran Guerra", 0),
                      ("Le hicieron creer", "Que su confesión entregó la ciudad", 1),
                      ("En realidad", "La ciudad ya había caído", 2)],
                     sello=("Recurso", 3))


def _cordura():
    return T.cordura("Diario de Cicerón", P("cicero"),
                     [("Asesino cuerdo y metódico", 0), ("Guardián de la Madre Noche", 1), ("Último trabajo: matar a un bufón", 2),
                      ("Lava el cadáver cada semana", 3), ("Ella nunca le habla", 4), ("Oye la risa de aquel bufón", 5)],
                     final=("Cicerón el hombre ha muerto", 6))


def _nombre():
    return T.nombre("Lo que significa su nombre", P("paarthurnax"),
                    [("Paar", "Ambición", 0), ("Thur", "Señor supremo", 1), ("Nax", "Crueldad", 2)])


# ---- MG nuevos del rehecho (30-oct-2026)
def _barras_razas():
    return T.barras("Velocidad por raza", [(P("alto_elfo"), "Altos elfos", 1.08, 0, T.ORO), (None, "Orcos", 1.045, 0, T.HUESO),
                                           (None, "Nórdicos", 1.03, 0, T.HUESO), (P("bretona"), "Bretonas", .95, 1, T.SANGRE),
                                           (P("khajiit"), "Khajiit", .95, 2, T.SANGRE)])


def _semana():
    return T.semana("Una semana para crear lo que quisieran",
                    [("Rieklings", P("riekling"), 0), ("Arvak", P("arvak"), 1), ("Señor de los vampiros", P("senor_vampiro"), 2),
                     ("La adopción", None, 3), ("Construir tu casa", None, 4)], tachada=("Mayordomo esqueleto", 5))


def _estrellas():
    escorpio = [(.40, .10), (.43, .22), (.44, .34), (.36, .28), (.33, .37), (.30, .45), (.28, .54), (.27, .63), (.25, .72), (.20, .79),
                (.13, .79), (.08, .72), (.09, .64), (.14, .58)]
    cruz = [(.75, .08), (.73, .72), (.62, .32), (.85, .42)]
    return T.estrellas("Polo sur de la Tierra",
                       [("Escorpio", escorpio, [(0, 3), (1, 3), (2, 3)] + [(k, k + 1) for k in range(3, 13)], 0),
                        ("Cruz del Sur", cruz, [(0, 1), (2, 3)], 1)], ancho=1040)


def _neloth():
    return T.versiones("El mismo personaje", (P("neloth"), "Morrowind", ["Maestro Telvanni", "Secuestraba a hijas Redoran", "Una misión: matarlo"], 0),
                       (P("neloth_sr"), "Skyrim", ["Sobrevivió"], 1), pie=None)


def _cronologia_erik():
    return T.cronologia("Erik West", [("2009", "Sarcoma de Ewing", 0), ("Make-A-Wish", "Lo lleva a Bethesda", 1),
                                      ("11 mayo 2011", "Erik muere", 2), ("11 nov 2011", "Sale Skyrim", 3)])


def _cadena_brand():
    return T.cadena("Brand-Shei", [("Invasión argoniana", None), ("Lo adopta una familia argoniana", P("brand_shei")),
                                   ("Vendedor en Riften", None), ("Tú le metes un anillo", P("anillo_madesi"))])


FX = [
    # ---- gancho
    com("nos dejó este comentario", "UgxVZpFHGH6mmk1_9kd4AaABAg", dur=7.0),
    rel("mejorar un amuleto de Talos", "amuleto_talos", dur=3.4, x=.82, y=.60, tam=420),
    ficha("Una cárcel donde peleabas", "La cárcel de la arena", "Peleabas por tu *libertad.*", origen="Contenido cortado", dur=2.6),
    cam("Un vendedor de Riften", "brand_shei", "Brand-Shei", dur=2.8, x=.15, y=.66, foco=(.5, .16, 2.4)),
    rel("una sopa de cinco monedas", "sopa", dur=3.6, x=.80, y=.60, tam=420),
    aviso("cuarenta secretos", "40", "Secretos que nadie te contó", dur=4.5),
    mg(T.rejilla("Cuarenta secretos", 40, 40, ("Todos comprobados", 2)), ("Hoy te traigo", -.2), ("en la descripción|fin", .4),
       ["Hoy te traigo", "cuarenta secretos", "todos comprobados"], "rejilla cuarenta", y=.58),
    ban("alguien en quien confías", P("paarthurnax"), foco=(.80, .26, 1.7), dur=4.2, y=.60),

    # ---- 40
    aviso("Número cuarenta", 40, "La poción del arquero"),
    ficha("sube el daño de todas", "Reforzar arquería", "Sube *todas* las armas, y los *puños.*", origen="Error del juego", rojo=True, dur=6.0),
    mapa([(.56, .21, "Lucero del Alba", "inicio", None), (.554, .326, "Fuerte Dunstad · la letrina", "meta", P("pocion_arqueria"))],
         de="Y en una letrina", a=("sobre apuntar bien|fin", .5), marcas=["Y en una letrina", "del Fuerte Dunstad"], sub="La poción del arquero", ajuste=.6),

    # ---- 39
    aviso("En el treinta y nueve", 39, "Las vacas del más allá"),
    peg("catorce cascarones plantados", "cascaron", "Cascarón de alma", dur=4.5),
    mg(T.rejilla("Cosecha del más allá", 14, 14, ("14 cascarones", 2), cols=7, ancho=560), ("Labra una parcela", -.2), ("cascarones plantados|fin", .7),
       ["Labra una parcela", "con catorce", "cascarones plantados"], "rejilla cascarones", x=.76, y=.62),
    grande("dos almas de vaca", "vaca", "", dur=4.0, x=.25, tam=480),
    ficha("Nadie explica", "Recordatorio de las Almas", "Dos almas de vaca. *Sin explicación.*", dur=3.6),

    # ---- 38
    aviso("Número treinta y ocho", 38, "Tu raza decide lo rápido que corres"),
    ficha("La velocidad depende de la altura", "Velocidad por raza", "Depende de la *altura.* El juego no te lo dice.", origen="Datos del juego", dur=1.9),
    mg(_barras_razas(), ("Los altos elfos son", -.1), ("Sin este ajuste", -.1), ["Los altos elfos son", "las bretonas", "las khajiit"], "barras razas"),

    # ---- 37
    aviso("En el treinta y siete", 37, "Castlevania"),
    ficha("En el Castillo de Volkihar", "Vitrina de Volkihar", "Garra, ojo, corazón, caja torácica y *anillo.*", dur=6.0),
    aba([("garra", "Garra"), ("ojo_sable", "Ojo"), ("corazon_daedra", "Corazón")], ("una garra", -.1), ("Son las partes de Drácula", .2),
        ["una garra", "un ojo", "un corazón"], "abanico vitrina"),
    grande("Son las partes de Drácula", "castlevania2", "Castlevania II", dur=5.5, x=.75, tam=560),

    # ---- 36
    aviso("Número treinta y seis", 36, "Los guardias te leen la mochila"),
    rel("Con la Estrella de Azura", "estrella_azura", "Estrella de Azura", dur=4.2, x=.25, y=.50, tam=500),
    peg("Con el Anillo de Namira", "anillo_namira", "Anillo de Namira", dur=3.5, x=.78, y=.62, tam=340),
    ficha("Y si eres hombre lobo", "Hombre lobo", "Pelo en las *orejas* y olor a *perro mojado.*", origen="Los guardias lo notan", dur=4.2),

    # ---- 35
    aviso("En el treinta y cinco", 35, "El mamut congelado"),
    mapa([(.73, .20, "Hibernalia", "inicio", None), (.692, .239, "Saarthal", "paso", None), (.665, .235, "El mamut congelado", "meta", P("mamut"))],
         de="Al oeste de Saarthal", a=("un virote de balista dwemer|fin", .3), marcas=["Al oeste de Saarthal", "hay un mamut atrapado"], sub="El mamut congelado", ajuste=.6),
    peg("Lleva clavadas cinco flechas", "flecha_enana", "Flecha enana", dur=4.0, x=.85, y=.60),
    ficha("Alguien lo estaba cazando", "Mamut congelado", "*5* flechas enanas y *1* virote de balista.", origen="Sin marcador en el mapa", dur=3.8),

    # ---- 34
    aviso("Número treinta y cuatro", 34, "Rezar a Arkay te puede matar"),
    ficha("Son veinticinco de salud", "Bendición de Arkay", "*+25* de salud · *8* horas. Si te queda menos al acabar, mueres.", origen="Santuario de Arkay", rojo=True, dur=7.0),
    mg(T.barra_vida("Cuando se acaba el efecto", ("Reforzar salud", "Te deja 1 punto"), ("Bendición de Arkay", "Mueres"), ancho=1000),
       ("Cuando se acaba un efecto", -.2), ("cobrando al contado|fin", .3), ["te deja con un punto de vida", "La Bendición de Arkay no", "mueres"], "barra de vida", x=.29, y=.62),

    # ---- 33
    aviso("En el treinta y tres", 33, "El gigante que pudo ser tu aliado"),
    grande("un gigante, Goldar", "gigante", "Goldar · misión cortada", dur=4.5, x=.25, tam=560),
    peg("una vaca pintada", "vaca", "Vaca pintada", dur=3.5, x=.80, y=.40, tam=320, giro=5.0),
    ficha("fabricantes de leche débil", "Goldar", "Las vacas son *fabricantes de leche débil.*", origen="Diálogo cortado", dur=4.5),

    # ---- 32
    aviso("Número treinta y dos", 32, "La turista de Markarth"),
    leg("margret", "Margret", ["Compra un colgante"], ("contra Margret", -.2), ("agente del general Tullius|fin", 1.0), ["agente del general Tullius"], sello=("Agente", 0)),
    sil("agente del general Tullius", "tullius_sil", "General Tullius", dur=2.8, lado="der", encuadre=(0, .60)),
    ficha("Si tardas", "Si tardas", "Muere delante de ti. Solo queda su *diario.*", dur=4.0),

    # ---- 31
    aviso("En el treinta y uno", 31, "La sopa de verduras"),
    mg(_aguante(), ("La sopa de verduras te devuelve", -.2), ("Por cinco monedas|fin", .6), ["La sopa de verduras te devuelve", "Por cinco monedas"], "aguante sopa"),

    # ---- 30
    com("nos dijo que el video le pareció", "Ugx90MHBC389cXU7AoF4AaABAg", dur=7.5),
    aviso("Hacerte vampiro te cambia", 30, "Hacerte vampiro te cambia de raza"),
    ficha("Para el juego, un vampiro", "Vampirismo", "Para el juego, *otra raza distinta.*", dur=4.5),
    cam("Bolund, en Falkreath", "bolund", "Bolund", dur=4.0, x=.15, y=.64, tam=340),
    cam("Y Galathil", "galathil", "Galathil", dur=4.5, x=.15, y=.64, tam=340),

    # ---- 29
    aviso("En el veintinueve", 29, "Un error nuestro"),
    ficha("velocidad cero coma seis", "Corrección", "Dijimos *0,6* para todos los martillos. No es verdad.", origen="Video de las armas", rojo=True, dur=6.0),
    mapa([(.105, .49, "Markarth", "inicio", None), (.239, .357, "Retiro del Mentiroso", "meta", P("martillo_largo"))],
         de="En el Retiro del Mentiroso", a=("Velocidad cero coma ocho|fin", .2), marcas=["En el Retiro del Mentiroso", "un cadáver sujeta"], sub="El Martillo largo", ajuste=.6),
    ficha("A herrería máxima", "Martillo largo", "*24,8* de daño por segundo · Volendrung *24,5*", origen="A herrería máxima", dur=5.0),
    rel("A herrería máxima", "martillo_largo", "Martillo largo", dur=5.0, x=.24, y=.52, tam=500),
    com("nos dijo que Clarividencia", "UgyQPJkz1TMvyu2as4l4AaABAg", dur=7.5),
    peg("la brújula no dice", "clarividencia", "Clarividencia", dur=3.5, x=.78, y=.66, tam=320),

    # ---- 28
    aviso("Número veintiocho", 28, "El hombre que sigue esperando un barco"),
    mapa([(.73, .20, "Hibernalia", "inicio", None), (.671, .185, "Campamento de Trius", "paso", None), (.671, .165, "Zanja del Peregrino", "meta", None)],
         de="En la costa de Hibernalia", a=("de la Zanja del Peregrino|fin", .5), marcas=["En la costa de Hibernalia", "bajo el agua"], sub="Para Shelly", ajuste=.6),

    # ---- 27
    aviso("En el veintisiete", 27, "Tu seguidor es mejor ladrón que tú"),
    sil("Si le mandas abrir", "lydia", dur=5.5, lado="izq", encuadre=(0, .60)),
    ficha("Si le mandas abrir", "Tu seguidor", "Cualquier cerradura con *0* ganzúas.", dur=5.0),
    ficha("un arco de caza", "Inventario oculto", "Arco de caza y *12* flechas de hierro.", origen="No sale en su inventario", dur=4.5),

    # ---- 26
    aviso("Número veintiséis", 26, "La maga de la corte de Soledad"),
    leg("sybille", "Sybille Stentor", ["Maga de la corte de Soledad"], ("Sybille Stentor dice", -.2), ("Detectar vida no la marca", -.3), x=.20, y=.52),
    mg(T.deteccion("Sybille Stentor", P("sybille"), ("Detectar vida", "No la marca"), ("Detectar muerte", "Sí la marca"), ancho=1100),
       ("Detectar vida no la marca", -.2), ("Detectar muerte, sí|fin", 1.0), ["Detectar vida no la marca", "Detectar muerte, sí"], "detección sybille"),
    peg("El verdugo cuenta", "ahtar", "Ahtar", dur=4.0, x=.78, y=.62, tam=340),

    # ---- crítica 1: kyrim (burla disfrazada, docs/estilo_secuencia_yt.md § COMENTARIOS 2c)
    com("nos escribió que se nota que kyrim", "UgzJYFZJk-eBnw3xQoB4AaABAg", dur=6.0),
    mis("De kyrim no sabemos nada", "Objetivo fallido", "Saber de Kyrim", dur=4.4),

    # ---- 25
    aviso("En el veinticinco", 25, "La nave de los rieklings"),
    peg("los rieklings acampan", "riekling", "Riekling", dur=5.0, x=.17),
    ficha("con el interior boca abajo", "La nave", "Volcada, con el interior *boca abajo.*", dur=4.0),
    grande("En Bloodmoon", "nave_extrana", "Solstheim", dur=6.0, x=.72, tam=620),

    # ---- 24 (las pegatinas de lo que salió de esa semana van dentro del MG)
    aviso("Número veinticuatro", 24, "La semana libre que creó las expansiones"),
    mg(_semana(), ("una semana para crear", -.2), ("Que yo habría contratado|fin", .3),
       ["De ahí salieron los rieklings", "Arvak", "el Señor de los vampiros", "la adopción", "y construir tu casa", "un mayordomo esqueleto"], "semana libre", y=.55),

    # ---- 23
    aviso("En el veintitrés", 23, "La capilla que aparece sola"),
    mapa([(.241, .523, "Viejo Hroldan", "inicio", None), (.226, .50, "El campamento · capilla de Mara", "meta", P("capilla_mara"))],
         de="Cerca del Viejo Hroldan", a=("con el diario de Karan al lado|fin", .4), marcas=["Cerca del Viejo Hroldan", "el campamento desaparece"], sub="Karan y Talvur", ajuste=.8),
    peg("con el diario de Karan", "karan_diario", "Diario de Karan", dur=3.4, x=.82, y=.60, tam=320, giro=5.0),

    # ---- 22
    aviso("Número veintidós", 22, "El Pergamino Antiguo esconde nuestras estrellas"),
    peg("Su fondo no es inventado", "pergamino", "Pergamino Antiguo", dur=6.0, x=.20, y=.66, tam=560),
    mg(_estrellas(), ("Es un mapa estelar", -.2), ("y la Cruz del Sur|fin", .4), ["con Escorpio", "y la Cruz del Sur"], "estrellas", x=.70, y=.56),
    ficha("Y leerlo te borra", "Pergamino Antiguo", "Borra *todos* tus efectos activos.", dur=4.5),
    rel("con el Arco de Auriel", "auriel", "Arco de Auriel", dur=3.6, x=.24, y=.52, tam=500),

    # ---- 21
    aviso("En el veintiuno", 21, "Desde Skyrim se ve Morrowind"),
    grande("desde Skyrim se ve Morrowind", "montana_roja", "Montaña Roja", dur=3.0, x=.25, tam=560),
    mapa([(.744, .183, "Colegio de Hibernalia · azotea", "inicio", None), (.86, .23), (.96, .28, "Morrowind", "meta", P("montana_roja"))],
         de="Desde la azotea", a=("se ve Morrowind#2|fin", .4), marcas=["Desde la azotea", "más allá de la frontera"], sub="Mirar fuera del mapa", ajuste=.6),
    pant("torre_skyrim", ("Y al sur, en un día despejado", -.1), ("de Cyrodiil|fin", .8), zoom=(1.0, 1.14), pan=(0, .3, 0, -.2)),

    # ---- 20
    com("nos dijo que a veces la música", "UgwjxU2XdFokls27Pnp4AaABAg", dur=7.5),
    aviso("Número veinte", 20, "Neloth ya era un cretino en Morrowind"),
    mg(_neloth(), ("Es el mismo personaje", -.2), ("Sobrevivió|fin", .9), ["Es el mismo personaje", "y una misión te mandaba matarlo"], "versiones neloth"),
    sil("Y hoy te dice con desdén", "neloth_sr", "Neloth", "Maestro Telvanni", dur=5.5, lado="izq"),
    ficha("Y hoy te dice con desdén", "Neloth", "Muy joven para acordarte del *Nerevarino.*", dur=5.0),

    # ---- 19
    aviso("En el diecinueve", 19, "El capitán que no se quedó muerto"),
    peg("está Falx Cario", "falx", "Falx Cario", dur=6.0, x=.17),
    ficha("murió hace unos doscientos años", "Falx Cario", "Muerto hace unos *200 años.*", origen="Personaje de Bloodmoon", dur=4.5),
    cam("Ildari lo reanimó", "ildari", "Ildari", dur=4.0, x=.82, y=.62, tam=320),

    # ---- 18
    aviso("Número dieciocho", 18, "El local de skooma que es una granja de sangre"),
    mapa([(.89, .78, "Riften", "inicio", None), (.802, .723, "Guarida de Aguas Rojas", "meta", P("skooma"))],
         de="La Guarida de Aguas Rojas", a=("te venden skooma|fin", .3), marcas=["La Guarida de Aguas Rojas", "Bajo una trampilla"], sub="Aguas Rojas", ajuste=.6),
    ficha("Si bebes la muestra gratis", "Muestra gratis", "Despiertas encerrado entre *vampiros.*", rojo=True, dur=5.0),

    # ---- 17
    aviso("En el diecisiete", 17, "Los cuatro aprendices que nadie buscó"),
    cam("Phinis Gestor menciona", "phinis", "Phinis Gestor", dur=4.0, x=.16, y=.64, tam=340),
    mapa([(.744, .183, "Colegio de Hibernalia", "inicio", P("phinis")), (.62, .20, "Yisra · la playa", "peligro", None),
          (.79, .225, "Rundi · runas de escarcha", "peligro", None), (.783, .273, "Borvir · Rincón del viajero", "peligro", None),
          (.718, .127, "Ilas-Tei · capilla de Talos", "meta", None)],
         de="repartidos por la comarca", a=("con un pergamino de Furia al lado|fin", .4),
         marcas=["repartidos por la comarca", "Yisra está calcinada", "Rundi yace", "Borvir, con tres", "E Ilas-Tei aparece"], sub="Los cuatro aprendices", ajuste=.9),
    ficha("La misión se cortó", "Misión cortada", "Llevarle sus objetos a Phinis *no hace nada.*", dur=4.5),

    # ---- 16
    aviso("Número dieciséis", 16, "El héroe del libro es el jefe que mataste"),
    peg("Sangre inmortal es un libro", "sangre_inmortal", "Sangre inmortal", dur=5.0, x=.20, y=.66, tam=480),
    mg(T.vela("Sangre inmortal", "El sacerdote", "Era el vampiro"), ("Al final, el sacerdote acerca", -.2), ("El sacerdote era el vampiro|fin", .3),
       ["el sacerdote acerca la vela", "El sacerdote era el vampiro"], "vela sacerdote"),
    mapa([(.42, .31, "Morthal", "inicio", None), (.418, .281, "Guarida de Movarth", "meta", P("movarth"))],
         de="Y el señor vampiro", a=("ese mismo Movarth|fin", .5), marcas=["Y el señor vampiro", "de la cueva de Morthal"], sub="Movarth Piquine", ajuste=.5),

    # ---- 15
    aviso("En el quince", 15, "La arena de Ventalia"),
    ficha("Si te encerraban", "La cárcel de la arena", "Peleabas ante el público. Si *ganabas*, salías *libre.*", origen="Contenido cortado", dur=6.0),

    # ---- 14
    aviso("Número catorce", 14, "El gran maestro tiene ficha de novato"),
    ficha("Paarthurnax es nivel diez", "Paarthurnax", "Nivel *10* · *905* de salud. Igual que el dragón más básico.", origen="Datos del juego", dur=6.5),
    peg("Paarthurnax es nivel diez", "paarthurnax", "Paarthurnax", dur=6.0, x=.20, y=.60, tam=460, giro=4.0),
    peg("lo interpreta Charles Martinet", "martinet", "Charles Martinet", dur=4.2, x=.18, y=.58, tam=420, giro=5.0),
    grande("Acuérdate de este dragón", "paarthurnax", "", dur=3.5, x=.75, tam=560),

    # ---- 13
    aviso("En el trece", 13, "Los libros que nadie lee"),
    peg("cuatro libros en alfabeto falmer", "tomo_falmer", "Libro falmer", dur=4.0, x=.17),
    ficha("te paga mil monedas", "Cuatro libros falmer", "*1 000* monedas por cada uno.", origen="Urag gro-Shub", dur=4.5),
    cam("Urag gro-Shub", "urag", "Urag gro-Shub", dur=4.5, x=.80, y=.66, tam=320),

    # ---- 12
    aviso("Número doce", 12, "Nunca absorbiste el alma de Alduin"),
    grande("Al matarlo no absorbes", "alduin", "Alduin", dur=4.2, x=.75, tam=560),
    cam("Arngeir te explica", "arngeir", "Arngeir", dur=5.0, x=.16, y=.62, tam=340),
    ficha("quizá se le permita volver", "Alduin", "Quizá *vuelva* al final de los tiempos.", dur=5.0),
    mis("Felicidades por salvar el mundo", "Misión completada", "Salvar el mundo, de momento", dur=4.0),

    # ---- 11
    aviso("En el once", 11, "El cura de Falkreath"),
    peg("En el once", "sala_falkreath", "Falkreath", dur=3.0, x=.80, y=.60, tam=420, giro=4.0),
    sil("Runil, el anciano sacerdote", "runil_b", "Runil", "Sacerdote de Arkay", dur=7.5, lado="izq"),
    ficha("En su diario anota un sueño", "Diario de Runil", "Una sombra, un rugido y un *desconocido* en un funeral.", dur=6.0),

    # ---- 10
    com("tremendo video", "UgyyK-18w979imO7POB4AaABAg", dur=4.0, x=.30, y=.24),
    com("le encantan estos videos", "Ugz_K8Ode87ZNHZb7FR4AaABAg", dur=3.6, x=.30, y=.42),
    aviso("Número diez", 10, "El pozo de la Hueste de Forel"),
    peg("Las tropas de Skorm", "diario_skorm", "Diario de Skorm", dur=4.5, x=.17, tam=340),
    ficha("Pero habían dejado cubos", "Los cubos", "Ya llenos, junto a un pozo *envenenado.*", rojo=True, dur=4.0),
    mapa([(.89, .78, "Riften", "inicio", None), (.913, .832, "Hueste de Forel · el pozo", "meta", None)],
         de="Al día siguiente, cuarenta", a=("tienes que bajar|fin", .4), marcas=["Al día siguiente, cuarenta", "Y ese pozo"], sub="La Hueste de Forel", ajuste=.5),
    mg(T.soldados("Cuarenta soldados", 40, ("Bebieron", 1), cols=10, ancho=760), ("cuarenta soldados bebieron", -.1), ("Y ese pozo", .2),
       ["cuarenta soldados bebieron", "antes de que pudieran pararlos"], "soldados", x=.26, y=.60),

    # ---- 9
    aviso("En el nueve", 9, "El faro que se tragó a una familia"),
    mapa([(.56, .21, "Lucero del Alba", "inicio", None), (.631, .248, "Faro del Flujo Helado", "meta", None)],
         de="Una familia redguard", a=("un agujero en el sótano|fin", .3), marcas=["Una familia redguard", "el Faro del Flujo Helado"], sub="El faro", ajuste=.5),
    peg("Encuentras a Ramati muerta", "ramati", "Ramati", dur=4.5, x=.74, y=.58, tam=460, giro=4.0),
    peg("Y los restos del padre", "segador", "Segador de chaurus", dur=4.0, x=.17),
    peg("Si los subes al brasero", "restos_habd", "Restos de Habd", dur=3.5, x=.78, y=.62, tam=340),

    # ---- crítica 2: «no eres digno» (burla disfrazada)
    com("nos dijo que no somos dignos", "Ugw36BCPJX6pZT5glDh4AaABAg", dur=6.0),
    mis("Seguimos esperando a que nos llamen", "Misión en curso", "Esperar a que nos llamen los Barbas Grises", dur=4.6),

    # ---- 8
    aviso("Número ocho", 8, "Los Barbas Grises nacieron de una humillación"),
    peg("Jurgen Llamador del Viento", "jurgen", "Jurgen Llamador del Viento", dur=6.0, x=.17),
    ficha("diecisiete lo atacaron", "Jurgen contra todos", "*17* contra *1* · *3* días tragándose sus gritos.", origen="Tablillas de Alto Hrothgar", dur=6.0, x=.84),
    mg(T.soldados("Diecisiete contra uno", 17, ("Cayeron agotados", 1), cols=17, ancho=1180), ("diecisiete lo atacaron", -.1), ("hasta que cayeron agotados|fin", 1.0),
       ["diecisiete lo atacaron", "hasta que cayeron agotados"], "diecisiete", x=.36, y=.72),

    # ---- 7
    aviso("En el siete", 7, "Lo que dicen los archivos thalmor"),
    mg(_informe_esbern(), ("En su informe sobre Esbern", -.2), ("a ser reeducado|fin", .7),
       ["que no entienden la vuelta", "nunca fue un simple archivero", "Al funcionario que lo descartó"], "informe esbern"),
    ban("Y el informe de Delphine", J("f_delphine"), "Delphine", "Antigua Cuchilla", foco=(.31, .31, 2.4), dur=6.0, y=.64),
    ficha("esquivó tres atentados", "Delphine", "*3* atentados esquivados.", origen="Informe thalmor", dur=4.4),

    # ---- campaña de suscripción (docs/estilo_secuencia_yt.md § CAMPAÑA): cifra real de `yt metricas`
    mg(T.rejilla("De cada 100 que ven este canal", 100, 14, ("Solo 14 están suscritos", 2)), ("De cada cien que ven", -.2), ("Queremos llegar a siete mil", -.2),
       ["De cada cien que ven", "catorce están suscritos", "catorce están suscritos"], "rejilla suscritos", y=.56),
    mis("Queremos llegar a siete mil", "Siguiente objetivo", "7 000 suscriptores", dur=3.8, y=.20),
    mis("Si llevas treinta y cuatro secretos", "Misión nueva", "Suscríbete a Crónicas de Tamriel", dur=4.8, y=.20),

    # ---- 6
    aviso("Número seis", 6, "Ulfric cree que entregó la Ciudad Imperial"),
    sil("Ulfric cree que entregó", "ulfric", dur=3.4, lado="der", encuadre=(0, .52)),
    mg(_informe_ulfric(), ("Los thalmor lo capturaron", -.2), ("figura como un recurso|fin", .9),
       ["Los thalmor lo capturaron", "le hicieron creer", "La ciudad ya había caído", "figura como un recurso"], "informe ulfric"),

    # ---- 5 (sin sarcasmo: solo lo necesario)
    aviso("Erik el Asesino existió", 5, "Erik el Asesino existió", dur=4.5),
    sil("El granjero de Paraje de Rorik", "erik", "Erik el Asesino", dur=6.5, lado="der"),
    mg(_cronologia_erik(), ("Le diagnosticaron", -.2), ("antes de que saliera Skyrim|fin", .6),
       ["Le diagnosticaron", "Make-A-Wish", "Murió el once de mayo", "seis meses antes"], "cronología erik", y=.60),

    # ---- 4
    aviso("Número cuatro", 4, "El vendedor de Riften"),
    grande("Brand-Shei es un elfo oscuro", "brand_shei", "Brand-Shei", dur=5.0, x=.25, tam=560),
    ficha("con nombre argoniano", "Brand-Shei", "Elfo oscuro con nombre *argoniano.*", dur=4.0),
    mapa([(.89, .78, "Riften · Brand-Shei", "inicio", P("brand_shei")), (.84, .45), (.793, .195, "Naufragio del Orgullo de Tel Vos", "meta", None)],
         de="En el naufragio del Orgullo", a=("Lo llama su único heredero|fin", .4), marcas=["En el naufragio del Orgullo", "un diario de su padre"], sub="El vendedor de Riften", ajuste=.7),
    mg(_cadena_brand(), ("lo criaron los del pueblo", -.5), ("para mandarlo a la cárcel|fin", .5),
       [("lo criaron los del pueblo", -.4), "lo criaron los del pueblo", "Y en el Gremio de Ladrones", "tú le metes un anillo", "para mandarlo a la cárcel"], "cadena brand-shei"),

    # ---- 3
    aviso("En el tres", 3, "El ataúd del carro"),
    peg("la Madre Noche estaba", "madre_noche_ob", "Madre Noche", dur=4.4, x=.17),
    peg("la Oyente Alisanne Dupre", "alisanne", "Alisanne Dupre", dur=3.0, x=.16, y=.58, tam=380, giro=4.0),
    peg("y Garnag huyó", "garnag", "Garnag", dur=3.4, x=.82, y=.58, tam=380, giro=-4.0),
    mapa([(.565, .429, "Granja de Loreio · el carro", "inicio", P("madre_noche")), (.50, .60), (.409, .745, "Santuario de Falkreath", "meta", P("cicero"))],
         de="Es el mismo ataúd", a=("la caída de la Hermandad|fin", .5), marcas=["Es el mismo ataúd", "Trece años huyendo"], sub="El ataúd del carro", ajuste=.5),
    ficha("Trece años huyendo", "El ataúd", "*13* años huyendo.", origen="Diario de Cicerón", dur=3.6, x=.24, y=.40),

    # ---- 2
    aviso("Número dos", 2, "Cicerón no nació loco"),
    sil("Cicerón no nació loco", "cicero", dur=3.2, lado="der"),
    mg(_cordura(), ("Sus diarios empiezan", -.2), ("es su última víctima|fin", .8),
       ["Sus diarios empiezan", "Lo nombran Guardián", "Matar a un bufón", "Lava el cadáver", "Ella nunca le habla", "empieza a oír la risa", "Cicerón el hombre ha muerto"],
       "cordura cicerón"),

    # ---- 1
    aviso("Y llegamos al número uno", 1, "El que te enseñó a confiar", dur=3.0),
    com("nos escribió que tras muchísimos", "UgzXyBrJs7uH5lwToEV4AaABAg", dur=8.5),
    mg(_nombre(), ("Su nombre se separa", -.2), ("Crueldad|fin", 2.0), ["Paar, Thur", "Señor supremo", "Crueldad"], "nombre paarthurnax"),
    peg("la mano derecha de Alduin", "alduin", "Alduin", dur=4.5, x=.78, y=.62, tam=380),
    grande("Y lo más fuerte lo dice él", "paarthurnax", "Paarthurnax", dur=9.0, x=.25, tam=640),

    # ---- cierre
    com("nos dio las gracias", "UgzGF3olyXy2g-JageF4AaABAg", dur=6.0),
    ficha("Cuántos de estos cuarenta", "¿Cuántos sabías?", "Déjalo en los *comentarios.*", dur=5.0),
    mis("Vamos por los siete mil", "Siguiente objetivo", "7 000 suscriptores", dur=4.0, y=.20),
]


# ---- SFX del JUEGO (regla 29-oct-2026; banco nucleo/datos/sfx_juego/skyrim/), solo en momentos clave para no repetirlos (regla de SFX)
PISTAS = [dict(sfx="mision_completada", en=e, vol=.20) for e in ("Número cuarenta", "Hacerte vampiro te cambia", "Número veinte", "Número diez", "En el tres", "Número dos")]
PISTAS += [dict(sfx="lugar_descubierto", en=e, vol=.20) for e in ("repartidos por la comarca", "Al día siguiente, cuarenta", "En su informe sobre Esbern", "En el naufragio del Orgullo")]
PISTAS += [dict(sfx="monedas", en=e, vol=.30) for e in ("Por cinco monedas", "paga mil monedas", "un anillo en el bolsillo")]
PISTAS += [dict(sfx="mision_iniciada", en=e, vol=.20) for e in ("De kyrim no sabemos nada", "Seguimos esperando a que nos llamen", "Si llevas treinta y cuatro secretos")]
PISTAS += [dict(sfx="subir_nivel", en="Y llegamos al número uno", vol=.24), dict(sfx="subir_nivel", en="Hoy te traigo cuarenta secretos", vol=.18),
           dict(sfx="mision_completada", en="Esa es mi lista", vol=.22)]
