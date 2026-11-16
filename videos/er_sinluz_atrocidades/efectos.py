# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades que COMETISTE tú (el Sinluz) QUE IGNORASTE» (SECUENCIA YT, Runa Caída,
16-nov-2026). Molde: videos/er_godrick_atrocidades/efectos.py (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS ·
MOTION GRAPHICS NUEVOS · MAPAS) con el kit de Elden Ring (nucleo/mg_er.py) y los estilos de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS reales (bajar_pegatinas.py; identidad en previews/pegatinas_check.jpg). `maliketh*` y `mausoleo` NO (paisajes).
- COMENTARIOS reales (≤ 10 días, `yt comentario`): @wsefsd-n1v y Amand (pidieron el tema), Alexander y Amand (voto),
  Franko, Oswaldo, Karlos, Isaac (agradecen); contraburla: Jonathan, Cristian (Loquendo), Arturo, KingInsect.
- FICHAS solo con citas del guion (verificadas en _investigacion/dossier.md).
- MG NUEVOS (mg_er, 16-nov): `expediente` (ficha del acusado, un cargo por puesto + sentencia en el cierre), `audiencia`
  (campeones a las fauces; tú el siguiente), `uvas` (uvas que son ojos), `paciencia` (las 9 raíces de Gurranq).
  Reusados: marionetas, injerto (callback de Godrick), cielo_sujeto, acuerdo, arbol_arde, balanza, votacion, cien.
- MAPAS (mundo): Mansión del Volcán, los 3 encargos, Academia, Caelid, la estrella a Necrolimbo, Santuario de la bestia, la Forja.
- PISTAS voz=True: Hyetta ardiendo y Melina en la Forja (sfx/s_*.mp3) con la voz callada (`post` en guion.py).
  FAB_FX_FINAL=1 python fab.py er_sinluz_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALAS TODAS)
"""
import os

import mg_er as E
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .30     # fichas: arriba a la derecha
TEMA_MAPA = "er"
TEMA = "er"

CAMARA = {}
FUNDIDO = {}

_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_G(slug), titulo, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=680):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.50, tam=tam)


def fila(en, items, y=.64, tam=340, dur=4.6):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def com(en, cid, dur=6.0, x=.30, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def sil(en, ruta, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara visible y el video corriendo detrás."""
    fn = PE.silueta(ruta, nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="silueta " + os.path.basename(ruta), ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.76, y=.52, tam=520):
    """Objeto flotando sobre un círculo de runas."""
    return dict(tipo="mg", fn=PE.reliquia(_G(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="reliquia " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(_G(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="camafeo " + slug, ver=1.0)


def ban(en, ruta, nombre=None, sub=None, foco=(.5, .3, 2.0), dur=4.5, y=.5, lado="der"):
    """Tira de cine a todo lo ancho con el rostro en primer plano."""
    return dict(tipo="mg", fn=PE.banda(ruta, nombre, sub, foco, lado=lado, tema=TEMA), en=en, dur=dur, x=.5, y=y, sale=.35,
                nombre="banda " + os.path.basename(ruta), ver=1.2)


def leg(ruta, titulo, lineas, de, a, marcas=(), sello=None, x=.21, y=.52, ancho=500, giro=3.5):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca)."""
    return dict(tipo="mg", fn=PE.legajo(ruta, titulo, lineas, sello=sello, ancho=ancho, giro=giro, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + titulo, ver=1.2)


def aba(fotos, de, a, marcas, nombre, x=.31, y=.66, tam=300):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(ruta, etiqueta)]."""
    return dict(tipo="mg", fn=PE.abanico(list(fotos), tam, tema=TEMA), de=de, a=a, marcas=list(marcas), x=x, y=y, sale=.35,
                nombre="abanico " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None, y=_FY):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None),
             en=en, x=_FX, y=y, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def msg(lineas, de, a, marcas, nombre):
    """Mensaje del suelo (texto ámbar) abajo, para citas que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=.76)


def cortado(de, a, sub, nombre):
    """Rótulo «CONTENIDO CORTADO» arriba (lo que no llegó al juego final se dice como tal y se marca en pantalla)."""
    return mg(E.puesto("Contenido cortado", sub), de, a, [], "cortado " + nombre, y=.10)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


C_WSEF, C_AMAND_PED = "Ugw1Hz8V7_0hYXmx1Sp4AaABAg", "Ugx-R_4o1YZyT3fLaBV4AaABAg"
C_ALEX, C_AMAND_VOTO, C_JONATHAN = "Ugy_4ZKdyNtLcxrmC6N4AaABAg", "Ugyb89M7sIZ96b-hAjN4AaABAg", "UgxMYDWt3wqEsjkbV5Z4AaABAg"
C_CRIS, C_ARTURO, C_KING = "UgxjDiYpkLFMHBQ3ldd4AaABAg", "Ugw3Dhf4bQQVsNFwIKN4AaABAg", "UgyauS4JeF5lBMFh4E54AaABAg"
C_OSWALDO, C_FRANKO, C_KARLOS, C_ISAAC = ("UgxSa4cFFYZs6Ig117x4AaABAg", "UgwZr8GUIJl-9aH-W7Z4AaABAg", "Ugx2vjkpC2P7Q9K_dTN4AaABAg",
                                          "UgxJ3axQRP9wFW24Vsd4AaABAg")

# Coordenadas (fracción de la imagen; medidas en mapas/mundo_rejilla.jpg el 16-nov; Leyndell/Altus/Liurnia/Caelid de Godrick)
M_VOLCAN, M_LEYND, M_ALTUS, M_LIUR = (.23, .325), (.48, .41), (.36, .36), (.17, .60)
M_ACAD, M_CAEL, M_BESTIA, M_VELO = (.197, .534), (.60, .73), (.615, .595), (.36, .70)
M_COLINA, M_PICOS, M_NECRO = (.375, .735), (.62, .23), (.40, .79)

CARGOS = ["Coleccionista de personas", "Sicario de un caníbal", "Ladrón de almas", "Le diste de comer ojos",
          "La que no pudiste evitar"]
RUNAS = [("Godrick", "Gran Runa"), ("Radahn", "Gran Runa"), ("Rykard", "Gran Runa"), ("Morgott", "Gran Runa"),
         ("Mohg", "Gran Runa")]


def expe(k, titulo_frase, dur=3.2):
    """Ficha del acusado al abrir el puesto k (0 = n.º 5): escribe el cargo k; en el n.º 1 cae el sello CULPABLE."""
    fin = (titulo_frase + "|fin", dur)
    marcas = [(titulo_frase + "|fin", -.2)] + ([(titulo_frase + "|fin", 2.6)] if k == 4 else [])
    return mg(E.expediente(cargos=CARGOS[:k + 1], ya=k, sello="CULPABLE" if k == 4 else None, titulo="Expediente del acusado"),
              (titulo_frase + "|fin", -.4), fin, marcas, f"expediente {k + 1}")


# Los 2 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026; cortes en sfx/, −18 LUFS)
PISTAS = [
    dict(sfx="s_hyetta", en="porque por fin pudo tocarlos Escúchala|fin", vol=1.0, voz=True),
    dict(sfx="s_melina", en="Y se despide Escúchala|fin", vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    aba([(_G("marika"), "Márika y Radagon"), (_G("miquella"), "Miquella y Malenia"), (_G("ranni"), "Ranni y Melina"),
         (_G("radahn"), "Radahn y Morgott"), (_G("mohg"), "Mohg y Godrick")],
        ("Llevamos diez videos contando", -.2), ("había alguien más en la escena|fin", .4),
        ["Llevamos diez videos", "contando las atrocidades", "de los semidioses", "desde la reina Márika", "hasta el pobre Godrick"],
        "diez videos",
        x=.50, y=.62, tam=260),
    msg(["Entró sin llamar.", "Los mató uno por uno."], ("Alguien que entró en sus casas", -.1), ("lo que tenían dentro|fin", .8),
        ["entró en sus casas", "Que los mató uno por uno"], "sin llamar"),
    com("Un comentario lo dijo en ocho palabras", C_WSEF, dur=5.6),
    com("Y Amand lo remató", C_AMAND_PED, dur=5.2, x=.70, y=.36),
    puesto("Así que hoy no hay semidiós", "Las 5 peores atrocidades de", "el Sinluz", dur=3.6),
    mg(E.expediente(cargos=["Drogó a una guerrera", "Sicario de un caníbal", "Dio de comer ojos a una ciega",
                            "Prendió fuego al mundo"], sello="CULPABLE", titulo="Expediente del acusado"),
       ("El que drogó a una guerrera", -.2), ("ya la cometiste|fin", 1.4),
       ["drogó a una guerrera", "sicario para un caníbal", "le dio de comer ojos", "prendió fuego al mundo", "ya la cometiste"],
       "expediente gancho"),

    # ================================================================ VOTACIÓN (resultado)
    mg(E.votacion(titulo="Narrador anterior o nuevo profeta", caja="Contamos los comentarios uno por uno",
                  remate="El profeta se queda"), ("En el video de Godrick preguntamos", -.2), ("Así que me quedo|fin", 1.0),
       ["narrador anterior, o", "nuevo profeta", "Contamos los comentarios", "Así que me quedo"], "votacion resultado"),
    com("Alexander lo resumió mejor que nadie", C_ALEX, dur=5.0),
    com("Y Amand escribió que se me escucha", C_AMAND_VOTO, dur=6.4, x=.70, y=.36),
    com("Jonathan votó por el anterior", C_JONATHAN, dur=6.0),
    cam("Sigue en el video de Mohg", "mohg", "Mohg", dur=3.8, x=.84, y=.66),
    com("Y Cristian preguntó quién es el degenerado", C_CRIS, dur=6.6),
    mg(E.puesto("Loquendo", "Cero votos"), ("Loquendo no se presentó a la votación", -.1), ("No sacó ni un voto|fin", .8), [],
       "loquendo", y=.80),
    mg(E.puesto("El protagonista de la lista", "Eres tú"), ("Hoy el protagonista de la lista", -.1),
       ("de la lista eres tú|fin", 1.4), [], "protagonista", y=.80),

    # ================================================================ 5 · EL COLECCIONISTA DE PERSONAS
    puesto("Número cinco", "Atrocidad número 5", "El coleccionista de personas"),
    expe(0, "El coleccionista de personas"),
    cam("la bruja de la torre", "ranni", "Ranni", dur=3.6, x=.84, y=.66),
    pant("tres_hermanas", ("subes a la Torre de Seluvis", -.3), ("al oeste de Liurnia|fin", .4), zoom=(1.0, 1.10)),
    sil("Seluvis es su preceptor", _G("seluvis"), "Seluvis", "el preceptor de Ranni", dur=5.4, lado="der", encuadre=(0, .55)),
    rel("Un frasquito", "pocion_seluvis", "Poción de Seluvis", dur=4.6, x=.24, y=.52),
    ficha("Su descripción es corta", "Poción de Seluvis", "Pequeño vial que contiene un *turbio tónico de un color negro "
          "azulado*.", tipo="Objeto clave", icono="pocion_seluvis", a=("de un color negro azulado|fin", .6)),
    msg(["Encuentra a Nepheli", "y haz que se beba esto."], ("Y debajo, la orden", -.1), ("haz que se beba esto|fin", 1.0),
        ["Encuentra a Nepheli", "haz que se beba esto"], "orden"),
    grande("La guerrera Nepheli Loux pertenece", "nepheli", "Nepheli Loux", lado="izq", dur=4.8, tam=600),
    cam("pertenece a la Mesa Redonda", "mesa_redonda", "Mesa Redonda", foco=(.5, .45, 1.4), dur=3.4, x=.84, y=.30),
    aba([(_G("nepheli"), "A Nepheli"), (_G("zampaheces"), "Al Zampaheces"), (_G("gideon"), "A Gideon")],
        ("Y el juego te deja elegir", -.2), ("sin que Seluvis se entere|fin", .6),
        ["dársela a ella", "dársela al Zampaheces", "o dársela a Gideon"], "elegir", x=.50, y=.62, tam=300),
    ban("Deja de ser la guerrera", _G("nepheli"), "Nepheli Loux", "la guerrera que conociste", foco=(.5, .25, 2.0), dur=4.4),
    cam("Seluvis, cuando se entera", "seluvis", "Seluvis", dur=3.4, x=.16, y=.66),
    mg(E.marionetas(titiritero="Seluvis", munecos=("Nepheli", "Tú"), dueno="Seluvis", titulo="Su cómplice", remate=""),
       ("Te dice que ahora eres su cómplice", -.2), ("una marioneta propia|fin", 1.2),
       ["ahora eres su cómplice", "Te dice que ahora", "y te pregunta si"], "complice"),

    # ---- 5b · el sótano de marionetas
    mg(E.puesto("Bajo unas ruinas", "Un sótano"), ("Porque debajo de unas ruinas", -.1), ("Seluvis tiene un sótano|fin", .6), [],
       "sotano", y=.80),
    msg(["Marioneta de Seluvis.", "No tocar."], ("En la entrada, un mensaje", -.1), ("No tocar|fin", 1.2),
        ["Marioneta de Seluvis", "No tocar"], "no tocar"),
    aba([(_G("marioneta_nepheli"), "Nepheli"), (_G("marioneta_zampaheces"), "Zampaheces"),
         (_G("marioneta_jarwight"), "Jarróntropo"), (_G("marioneta_therolina"), "Therolina")],
        ("Te deja elegir una gratis", -.2), ("para que mueran por ti|fin", .6),
        ["Te deja elegir una gratis", "Las demás te las vende", "cenizas de espíritu", "para que mueran por ti"],
        "marionetas", x=.50, y=.62, tam=290),
    rel("La Marioneta de Nepheli Loux", "marioneta_nepheli", "Marioneta de Nepheli Loux", dur=5.0, x=.24, y=.52),
    ficha("tiene su propia descripción", "Marioneta de Nepheli Loux", "La marioneta de una guerrera *traicionada por la "
          "pureza de su corazón*.", tipo="Cenizas de espíritu", icono="marioneta_nepheli", a=("la pureza de su corazón|fin", 1.0)),
    cam("Y ese alguien llevaba el frasquito", "pocion_seluvis", "El frasquito", foco=(.5, .5, 1.4), dur=3.4, x=.84, y=.66),
    ficha("La del Zampaheces es, dice", "Marioneta del Zampaheces", "El espíritu de un hombre que *asesinó a miles de "
          "personas* y profanó sus cadáveres.", tipo="Cenizas de espíritu", icono="marioneta_zampaheces",
          a=("y profanó sus cadáveres|fin", .4)),
    peg("La del Zampaheces es", "zampaheces", "El Zampaheces", tam=380, x=.20, y=.62),
    ficha("La del jarróntropo", "Marioneta del jarróntropo", "El espíritu de un hombre ansioso por ser parte de las *entrañas "
          "de un tarro viviente*.", tipo="Cenizas de espíritu", icono="marioneta_jarwight",
          a=("de un tarro viviente|fin", .8)),
    rel("Y la de Therolina", "marioneta_therolina", "Marioneta de Therolina", dur=5.4, x=.24, y=.52),
    ficha("termina con una frase que pesa", "Marioneta de Therolina", "Un Sinluz sin su doncella, una doncella sin su Sinluz, "
          "*y nada ni nadie que vaya a reunirlos*.", tipo="Cenizas de espíritu", icono="marioneta_therolina",
          a=("vaya a reunirlos|fin", .8)),
    sil("La de Sellen, tu maestra", _G("sellen"), "Sellen", "tu maestra de hechicería", dur=5.0, lado="der", encuadre=(0, .55)),
    mg(E.puesto("Seluvis colecciona", "A la gente que conoces"), ("Colecciona a la gente que conoces", -.1),
       ("Colecciona a la gente que conoces|fin", 1.4), [], "conoces", y=.80),
    rel("Te pide el Ámbar de luz estelar", "ambar_estelar", "Ámbar de luz estelar", dur=5.2, x=.24, y=.52),
    ficha("según su descripción, puede comandar", "Ámbar de luz estelar", "Un mineral que *puede comandar los destinos de los "
          "dioses*.", tipo="Objeto clave", icono="ambar_estelar", a=("los destinos de los dioses|fin", .8)),
    mg(E.marionetas(titiritero="Seluvis", munecos=("Nepheli", "Sellen", "Ranni"), dueno="Ranni", titulo="La mejor marioneta",
                    remate="La única que te paró"),
       ("Con él prepara un Brebaje ámbar", -.2), ("la decencia de pararte|fin", 1.0),
       ["Con él prepara", "un Brebaje ámbar", "La orden", "haz que Ranni se lo beba", "Lo único que te detiene es Ranni"],
       "mejor marioneta"),
    peg("Con él prepara un Brebaje ámbar", "brebaje", "Brebaje ámbar", tam=320, x=.13, y=.80),
    com("Arturo escribió que quería las cinco atrocidades", C_ARTURO, dur=6.6),
    mg(E.puesto("A Nepheli", "Nadie le pidió perdón"), ("A Nepheli, en cambio, nadie le pidió perdón", -.1),
       ("nadie le pidió perdón nunca|fin", 1.6), [], "perdon", y=.80),

    # ================================================================ 4 · SICARIO DE UN CANÍBAL
    puesto("Número cuatro", "Atrocidad número 4", "Sicario de un caníbal"),
    expe(1, "Sicario de un caníbal"),
    mapa("mundo", [(M_ALTUS[0], M_ALTUS[1], "Meseta Altus"), (.29, .33),
                   (M_VOLCAN[0], M_VOLCAN[1], "Mansión del Volcán", "Monte Gelmir", _P("mansion_volcan"))],
         ("entre ríos de lava", -.3), ("La Mansión del Volcán|fin", .6), ["En la cima del Monte Gelmir", "La Mansión del Volcán"],
         titulo="Monte Gelmir", sub="La Mansión del Volcán", entrada="desenrolla", traza=99),
    sil("Te recibe una mujer con máscara", _G("tanith"), "Tanith", "la señora de la casa", dur=5.4, lado="der", encuadre=(0, .5)),
    mg(E.puesto("Te ofrece", "Una familia"), ("Una familia", -.1), ("Una familia|fin", 1.6), [], "familia", y=.80),
    mg(E.puesto("El trabajito", "Cartas con nombres"), ("cartas con nombres", -.2), ("merece morir|fin", .6), [], "cartas", y=.80),
    mapa("mundo", [(M_VOLCAN[0], M_VOLCAN[1], "Mansión del Volcán"), (M_COLINA[0], M_COLINA[1], "Istvan", "Colina Tormentosa",
                    _G("istvan")), (M_ALTUS[0], M_ALTUS[1] + .02, "Rileigh", "Meseta Altus", _G("rileigh")),
                   (M_PICOS[0], M_PICOS[1], "Juno Hoslow", "Picos de los gigantes", _G("juno"))],
         ("El primero, el viejo caballero Istvan", -.3), ("de los Picos de los gigantes|fin", 1.0),
         ["El primero, el viejo caballero Istvan", "El segundo, Rileigh", "El tercero, Juno Hoslow"],
         titulo="Los encargos", sub="Tres Sinluz", entrada="mesa", traza=99),
    aba([(_G("disparo_magma"), "Disparo de magma"), (_G("hoja_serpiente"), "Hoja de hueso de serpiente"),
         (_G("camafeo"), "Camafeo del megalómano")],
        ("Y Tanith te paga", -.2), ("el Camafeo del megalómano|fin", .6),
        ["Un hechizo de magma", "Una espada de hueso de serpiente", "el Camafeo del megalómano"], "pago", x=.50, y=.62, tam=300),
    rel("Su descripción es la filosofía de la casa", "camafeo", "Camafeo del megalómano", dur=5.0, x=.24, y=.52),
    ficha("Su descripción es la filosofía de la casa", "Camafeo del megalómano", "Cuando Rykard sucumbió a la herejía, tomar por "
          "la fuerza se convirtió en norma. *Después de todo, los propios dioses lo hacían*.", tipo="Talismán", icono="camafeo",
          a=("los propios dioses lo hacían|fin", 1.0)),
    msg(["No hay sitio para los débiles,", "ni para las manos limpias."], ("Tanith también te avisa", -.1),
        ("te tienes que ir|fin", .6), ["no hay sitio para los débiles", "conservar las manos limpias"], "manos limpias"),
    mg(E.puesto("Y tú", "Te quedaste"), ("Y tú te quedaste", -.1), ("Y tú te quedaste|fin", 1.6), [], "quedaste", y=.80),

    # ---- 4b · la audiencia
    sil("Una audiencia con el señor de la casa", _G("rykard"), "Rykard", "señor de la Blasfemia", dur=5.4, lado="izq",
        encuadre=(0, .5)),
    rel("el Rencor de Rykard", "rencor_rykard", "Rencor de Rykard", dur=5.0, x=.24, y=.52),
    ficha("el Rencor de Rykard", "Rencor de Rykard", "El señor les concedió audiencia, *tras la cual fueron recibidos por las "
          "fauces de la gran serpiente*.", tipo="Hechizo", icono="rencor_rykard", a=("las fauces de la gran serpiente|fin", 1.0)),
    mg(E.audiencia(), ("La audiencia era el plato", -.2), ("Eras el siguiente menú|fin", 1.4),
       ["Los campeones de la mansión", "el mismo trabajo que tú", "terminaban en el estómago", "Eras el siguiente menú"],
       "audiencia"),
    peg("la Serpiente devoradioses", "serpiente", "Serpiente devoradioses", tam=360, x=.15, y=.22),
    aba([(_G("istvan"), "Istvan"), (_G("rileigh"), "Rileigh"), (_G("juno"), "Juno Hoslow")],
        ("Pero los tres que mataste", -.2), ("cazados por encargo|fin", .4),
        ["los tres que mataste", "Eran Sinluz como tú", "cazados por encargo"], "tres", x=.50, y=.62, tam=300),
    rel("runa incluida", "runa_rykard", "Gran Runa de Rykard", dur=4.6, x=.76, y=.50),
    grande("ahí está Tanith", "tanith", "Tanith", lado="izq", dur=4.6, tam=600),
    mg(E.puesto("Tanith", "Comiéndose a su señor"), ("Comiéndoselo", -.1), ("no se acaba rápido|fin", .4), [], "comiendo", y=.80),
    rel("Un tónico para borrarle la memoria", "tonico", "Tónico del olvido", dur=4.6, x=.76, y=.52),
    cam("a Rya, su hija adoptiva", "rya", "Rya", dur=3.8, x=.16, y=.66),
    mg(E.puesto("Y tú", "Eras de la familia"), ("Y tú eras de la familia", -.1), ("Y tú eras de la familia|fin", 1.6), [],
       "familia 2", y=.80),
    sil("aceptaste el juramento de Varré", _G("varre"), "Varré", "el de la máscara blanca", dur=5.0, lado="der",
        encuadre=(0, .5)),
    rel("Te da el Favor del Señor de la Sangre", "favor_sangre", "Favor del Señor de la Sangre", dur=5.0, x=.24, y=.52),
    ficha("lo dice con un desprecio muy suyo", "Favor del Señor de la Sangre", "Bastará con la sangre de la doncella de cualquier "
          "otro, *ya que después de todo, no sirves a ninguna*.", tipo="Objeto clave", icono="favor_sangre",
          a=("no sirves a ninguna|fin", 1.0)),
    mg(E.puesto("El rito exige", "Matar a tu propia doncella"), ("el rito exige matar a tu propia doncella", -.1),
       ("Tú solo tienes que usar la de otro|fin", .6), [], "rito", y=.80),
    pant("iglesia_inhibicion", ("Puedes mancharla en el cadáver", -.3), ("que todavía esté viva|fin", .4),
         zoom=(1.0, 1.10), oscuro=.05),
    mg(E.puesto("Guarda ese detalle", "Vuelve en el número dos"), ("Guarda ese detalle", -.1), ("Vuelve en el número dos|fin", 1.2),
       [], "detalle", y=.80),

    # ================================================================ 3 · EL LADRÓN DE ALMAS
    puesto("Número tres", "Atrocidad número 3", "El ladrón de almas"),
    expe(2, "El ladrón de almas"),
    rel("Y su recuerdo lo describe así", "recuerdo_injertado", "Recuerdo del Injertado", dur=5.4, x=.24, y=.52),
    ficha("Y su recuerdo lo describe así", "Recuerdo del Injertado", "Un hombre débil que ansiaba adquirir poder *mediante la "
          "grotesca práctica de la realización de injertos*.", tipo="Recuerdo", icono="recuerdo_injertado",
          a=("la realización de injertos|fin", .8)),
    cam("En el video de Godrick te contamos", "godrick", "Godrick", dur=3.6, x=.84, y=.66),
    mg(E.injerto(centro="Tú", sub_centro="el Sinluz", miembros=RUNAS, titulo="Tu inventario", remate="Tú te cosiste almas"),
       ("Ahora mira tu inventario", -.2), ("Tú te cosiste almas|fin", .3),
       ["Y saliste con las Grandes Runas", "de cinco semidioses", "sus recuerdos", "sus armas", "y sus hechizos",
        "Tú te cosiste almas"], "injerto inventario"),
    mapa("mundo", [(M_ACAD[0], M_ACAD[1], "Academia de Raya Lucaria", "Liurnia", _P("academia"))],
         ("Empieza por la Academia de Raya Lucaria", .5), ("En lo alto de la Gran Biblioteca|fin", .4),
         ["Empieza por la Academia"], titulo="Liurnia de los Lagos", sub="La Academia", ventana=True, x=.30, y=.40, traza=99),
    grande("está Rennala, la Reina de la Luna Llena", "rennala", "Rennala", lado="der", dur=5.0, tam=620),
    cam("Su marido, Radagon", "radagon", "Radagon", dur=3.4, x=.16, y=.66),
    cam("para casarse con Márika", "marika", "Márika", dur=3.4, x=.84, y=.66),
    mg(E.puesto("Su academia", "La encerró en su biblioteca"), ("La academia que ella había conquistado", -.1),
       ("en su propia biblioteca|fin", 1.0), [], "biblioteca", y=.80),
    rel("te llevas la Gran Runa de los Nonatos", "runa_nonatos", "Gran Runa de los Nonatos", dur=5.0, x=.24, y=.52),
    ficha("Su descripción: los hijos renacidos", "Gran Runa de los Nonatos", "Los hijos renacidos de Rennala fueron todos frágiles "
          "y su vida efímera. *Seres imperfectos, cada uno de ellos*.", tipo="Gran Runa", icono="runa_nonatos",
          a=("cada uno de ellos|fin", .8)),
    mg(E.puesto("Rennala", "Ni siquiera es semidiosa"), ("Lo curioso es que Rennala", -.1), ("ni siquiera es semidiosa|fin", 1.2),
       [], "no semidiosa", y=.80),
    sil("Gideon te lo comenta", _G("gideon"), "Gideon Ofnir", "el Omnisciente", dur=5.0, lado="der", encuadre=(0, .5)),
    rel("con unas lágrimas en la mano", "lagrima_larval", "Lágrima larval", dur=4.4, x=.76, y=.52),
    ban("convertida en tu estilista", _G("rennala"), "La Reina de la Luna Llena", "convertida en tu estilista",
        foco=(.5, .3, 2.0), dur=3.0),

    # ---- 3b · Radahn y los mausoleos
    mapa("mundo", [(M_CAEL[0], M_CAEL[1], "Caelid", "Radahn", _G("radahn"))], ("Luego está Radahn, en Caelid", .6),
         ("El Azote de las Estrellas|fin", 1.0), ["Luego está Radahn, en Caelid"], titulo="Caelid", sub="Radahn",
         ventana=True, x=.30, y=.40, traza=99),
    rel("según su recuerdo, aprendió la magia de gravedad", "recuerdo_azote", "Recuerdo del Azote de las Estrellas", dur=5.0,
        x=.76, y=.56),
    ficha("según su recuerdo, aprendió la magia de gravedad", "Recuerdo del Azote de las Estrellas", "Aprendió la magia de "
          "gravedad en su juventud. Todo para no tener que abandonar nunca a su *querido aunque escuálido corcel*.",
          tipo="Recuerdo", icono="recuerdo_azote", a=("aunque escuálido corcel|fin", .8), y=.28),
    sil("Ahora es un gigante podrido", _G("radahn"), "Radahn", "el Azote de las Estrellas", dur=5.4, lado="izq", encuadre=(0, .5)),
    rel("La Gran Runa arde", "runa_radahn", "Gran Runa de Radahn", dur=4.4, x=.76, y=.52),
    mg(E.cielo_sujeto(["Sus estrellas", "El destino"], quien="Radahn", remate="Una cae en Necrolimbo"),
       ("mientras Radahn vivía, sus estrellas", -.2), ("abre un cráter enorme|fin", 1.0),
       ["sus estrellas se quedaban quietas", "en el cielo", "Cuando lo matas"], "cielo"),
    mapa("mundo", [(M_CAEL[0], M_CAEL[1], "Caelid", "Radahn cae"), (.50, .78), (M_NECRO[0], M_NECRO[1], "Necrolimbo", "el cráter",
                    _G("estrellas"))], ("Tú le quitaste el tapón al cielo", -.3), ("en una ciudad subterránea|fin", .2),
         ["Tú le quitaste el tapón", "Y la grieta que dejó la estrella"], titulo="La estrella", sub="Necrolimbo",
         ventana=True, x=.70, y=.40, traza=99),
    peg("para bajar a robar en una ciudad subterránea", "nokron", "Nokron, la ciudad eterna", tam=440, x=.22, y=.60),
    mg(E.puesto("Tumbas que caminan", "Los Mausoleos errantes"), ("Los Mausoleos errantes", -.1),
       ("Los Mausoleos errantes|fin", 1.6), [], "mausoleos", y=.80),
    rel("Y el sobretodo que llevan", "sobretodo_mausoleo", "Sobretodo de soldado del mausoleo", dur=5.4, x=.24, y=.52),
    ficha("Y el sobretodo que llevan lo dice así", "Sobretodo de soldado del mausoleo", "La campana del mausoleo tañe en "
          "constante pesar *por los semidioses sin alma*.", tipo="Armadura", icono="sobretodo_mausoleo",
          a=("los semidioses sin alma|fin", 1.0)),
    mg(E.puesto("Una tumba sagrada", "Usada de fotocopiadora"), ("Una tumba sagrada", -.1),
       ("usada de fotocopiadora|fin", 1.4), [], "fotocopiadora", y=.80),

    # ---- 3c · Gurranq
    mapa("mundo", [(M_CAEL[0], M_CAEL[1], "Caelid"), (M_BESTIA[0], M_BESTIA[1], "Santuario de la bestia", "Montedrago",
                                                     _P("santuario_bestia"))],
         ("En el Santuario de la bestia", -.3), ("al norte de Caelid|fin", .6), ["En el Santuario de la bestia"],
         titulo="Montedrago", sub="Al norte de Caelid", ventana=True, x=.30, y=.40, traza=99),
    sil("vive Gurranq, el clérigo bestia", _G("gurranq"), "Gurranq", "el clérigo bestia", dur=5.6, lado="der", encuadre=(0, .5)),
    rel("Te pide Raíz mortuoria", "raiz_mortuoria", "Raíz mortuoria", dur=5.0, x=.24, y=.52),
    ficha("según su descripción, despierta", "Raíz mortuoria", "Una raíz que *despierta a quienes viven en la muerte*.",
          tipo="Objeto clave", icono="raiz_mortuoria", a=("te paga|fin", .4)),
    mg(E.paciencia(icono=_G("raiz_mortuoria")), ("Al principio la acepta con hambre", -.2),
       ("Con el hambre como única compañía|fin", 1.0),
       ["Al principio la acepta", "Que por favor, basta", "Y tú vuelves", "Con el hambre como única compañía"], "paciencia",
       y=.70),
    rel("el que guardaba la Runa de la Muerte", "runa_muerte", "Runa de la Muerte", dur=4.4, x=.76, y=.52),
    cam("Gurranq es Maliketh", "gurranq", "Maliketh, la Hoja Negra", dur=3.8, x=.16, y=.66),
    com("Y KingInsect le dio voz", C_KING, dur=6.2),
    mg(E.puesto("Márika le rompió el corazón", "Tú le rompiste la dieta"), ("Márika le rompió el corazón", -.1),
       ("Tú le rompiste la dieta|fin", 1.6), [], "dieta", y=.80),
    aba([(_G("rennala"), "Rennala"), (_G("radahn"), "Radahn"), (_G("gurranq"), "Gurranq"), (_G("sobretodo_mausoleo"), "Cada tumba")],
        ("Rennala, Radahn, Gurranq", -.2), ("Mataste para coleccionar|fin", .6),
        ["Rennala, Radahn", "Gurranq y cada tumba", "No mataste para defenderte", "Mataste para coleccionar"], "coleccion",
        x=.50, y=.62, tam=280),
    com("Y Oswaldo nos pidió", C_OSWALDO, dur=6.4),
    mg(E.puesto("Todos acaban mal", "Por culpa tuya"), ("Todos acaban mal", -.1), ("acaban mal por culpa tuya|fin", 1.4), [],
       "por ti", y=.80),

    # ================================================================ 2 · LE DISTE DE COMER OJOS
    puesto("Número dos Le diste", "Atrocidad número 2", "Le diste de comer ojos"),
    expe(3, "Le diste de comer ojos"),
    cam("la chica ciega del Puente del Sacrificio", "irina", "Irina", dur=3.8, x=.16, y=.66),
    aba([(_G("irina"), "La misma cara"), (_G("hyetta"), "La misma ropa")], ("Es ciega, tiene la misma cara", -.2), ("Se llama Hyetta|fin", .6),
        ["tiene la misma cara", "la misma ropa"], "misma cara", x=.50, y=.60, tam=360),
    grande("Te pide ayuda", "hyetta", "Hyetta", lado="der", dur=5.0, tam=600),
    rel("La Uva Shabriri", "uva_shabriri", "Uva Shabriri", dur=5.0, x=.24, y=.52),
    ficha("Ahora lee la descripción de la uva", "Uva Shabriri", "Un globo ocular amarillento y supurante de lo enfermizo. Por "
          "fuera está reseco y su interior es blando, como una gran uva demasiado madura. *Dáselo a la doncella ciega para "
          "guiarla hasta la luz distante*.", tipo="Objeto clave", icono="uva_shabriri", a=("hasta la luz distante|fin", 1.0),
          y=.36),
    mg(E.uvas(remate="Es un ojo"), ("Lo que acabas de darle es un ojo", -.1), ("Y la tercera|fin", .8), ["acabas de darle es un ojo", "Le estás dando de comer"],
       "uvas ojo"),
    sil("La tercera la llevaba encima Edgar", _G("edgar"), "Edgar", "el vengador", dur=5.6, lado="izq", encuadre=(0, .5)),
    mg(E.puesto("Para dársela", "A la chica idéntica a su hija"), ("Para dársela a la chica idéntica", -.1),
       ("idéntica a su hija|fin", .3), [], "identica", y=.80),
    mg(E.uvas([("Un espíritu en Velo Tormentoso", 1)], remate="Tú solo haces el reparto"), ("Y de dónde salen las uvas", -.2),
       ("Tú solo haces el reparto|fin", 1.2), ["Y de dónde salen las uvas", "hay un espíritu sentado", "Tú solo haces el reparto"],
       "uvas reparto"),

    # ---- 2b · la verdad y la llama
    mg(E.puesto("La verdad", "Son ojos humanos"), ("lo que se ha estado comiendo", -.1), ("son ojos humanos|fin", 1.4), [],
       "verdad", y=.80),
    ban("Ella no se lo cree", _G("hyetta"), "Hyetta", "no se lo cree", foco=(.5, .3, 2.0), dur=4.6),
    sil("El del caballero Vyke", _G("vyke"), "Vyke", "caballero de la Mesa Redonda", dur=5.4, lado="der", encuadre=(0, .5)),
    ficha("Su descripción: globo ocular del caballero Vyke", "Uva dactilograma", "Globo ocular del caballero Vyke, *inflamado y "
          "amarillento*.", tipo="Objeto clave", icono="uva_dactilograma", a=("le sacas el ojo|fin", .6)),
    pant("subsuelo", ("Debajo de Leyndell, en el Subsuelo", -.3), ("hay una puerta sellada|fin", .4), zoom=(1.0, 1.10)),
    peg("La Cámara de la llama frenética", "camara_frenetica", "Cámara de la llama frenética", tam=440, x=.22, y=.60),
    peg("Los Tres Dedos", "tres_dedos", "Los Tres Dedos", tam=460, x=.78, y=.56),
    rel("Te dan la llama del caos", "llama_frenetica", "Llama frenética", dur=4.6, x=.24, y=.52),

    # ---- 2c · las gracias
    aba([(_G("sello_frenetico"), "Un sello"), (_G("piedra_frenetica"), "Piedras de la llama frenética")],
        ("Lo único que queda en el suelo", -.2), ("unas piedras de la llama frenética|fin", .8),
        ["es un sello", "unas piedras de la llama"], "restos", x=.50, y=.62, tam=320),
    mg(E.puesto("Y ella", "Te dio las gracias"), ("Y ella te dio las gracias", -.1), ("Y ella te dio las gracias|fin", 1.6), [],
       "gracias", y=.80),
    rel("recuerda la bandera blanca", "favor_sangre", "Favor del Señor de la Sangre", dur=4.6, x=.76, y=.52),
    cam("Hyetta es una de las doncellas", "hyetta", "Hyetta", dur=3.6, x=.16, y=.66),
    aba([(_G("irina"), "Irina"), (_G("hyetta"), "Hyetta")], ("Hay quien dice que Hyetta es Irina", -.2),
        ("El juego nunca lo confirma|fin", .6), ["Hay quien dice", "la hija de Edgar"], "irina hyetta", x=.50, y=.60, tam=360),
    cam("el ojo que llevaba su propio padre", "edgar", "Edgar", dur=3.6, x=.84, y=.66),
    com("Franko escribió que los problemas de pronunciación", C_FRANKO, dur=6.4),
    mg(E.cien("De cada 100 que ven el canal", 5, remate=("Unas cinco, suscritas", 1)), ("De cada cien personas", -.2),
       ("y la meta es mil|fin", .6), ["De cada cien personas", "unas cinco están suscritas"], "cien", y=.46),
    com("Karlos escribió que poco a poco", C_KARLOS, dur=5.2),
    mg(E.puesto("Suscribirte", "No te pide ningún ojo"), ("Suscribirte no te pide ningún ojo", -.1),
       ("Suscribirte no te pide ningún ojo|fin", 1.6), [], "ningun ojo", y=.80),

    # ================================================================ 1 · LA QUE NO PUDISTE EVITAR
    puesto("llegamos al número uno", "Atrocidad número 1", "La que no pudiste evitar"),
    expe(4, "La atrocidad que no pudiste evitar de ninguna manera"),
    aba([(_G("pocion_seluvis"), "El frasquito"), (_G("tanith"), "Los encargos"), (_G("uva_shabriri"), "Las uvas"),
         (_G("raiz_mortuoria"), "Las raíces")],
        ("Podías no beber del frasquito", -.2), ("no volver con más raíces|fin", .6),
        ["no beber del frasquito", "no aceptar los encargos", "no dar las uvas", "no volver con más raíces"], "opcionales",
        x=.50, y=.62, tam=280),
    sil("Cuando conoces a Melina", _G("melina"), "Melina", "tu doncella", dur=2.6, lado="der", encuadre=(0, .5)),
    mg(E.acuerdo(["Ser tu doncella", "Runas en poder", "Buscar el Círculo de Elden"], "Llevarla al pie del Árbol Áureo",
                 titulo="El trato", remate="Trato"),
       ("ella te ofrece ser tu doncella", -.2), ("hasta el pie del Árbol Áureo|fin", 1.2),
       ["ser tu doncella", "Convertir tus runas en poder", "buscar el Círculo de Elden", "Solo hace falta que me lleves"],
       "trato"),
    cam("Matas a Morgott en Leyndell", "morgott", "Morgott", dur=3.6, x=.16, y=.66),
    mapa("mundo", [(M_LEYND[0], M_LEYND[1], "Leyndell", "el Árbol cerrado"), (.54, .30),
                   (M_PICOS[0], M_PICOS[1], "Picos de los gigantes", "la Forja", _G("forja"))],
         ("Pero está cerrado por espinas", -.3), ("En la Forja de los gigantes|fin", 1.0),
         ["Pero está cerrado por espinas", "En la Forja de los gigantes"], titulo="Lo más alto del mundo", sub="La Forja",
         ventana=True, x=.70, y=.40, traza=99),
    peg("Matas al último Gigante de fuego", "gigante_fuego", "Gigante de fuego", tam=440, x=.22, y=.60),
    mg(E.puesto("Melina te pregunta", "¿Preparado para un pecado capital?"), ("Melina te pregunta si estás preparado", -.1),
       ("cometer un pecado capital|fin", 1.4), [], "pecado", y=.80),

    # ---- 1b · la yesca
    mg(E.arbol_arde(["La llama llega", "Trepa por el tronco", "La yesca era ella", "Ceniza"], titulo="El pecado capital"),
       ("La yesca era ella", -.2), ("La llevaste a la hoguera|fin", 1.2),
       ["La yesca era ella", "hacía falta un sacrificio", "Melina se lanzó al fuego", "La llevaste a la hoguera"], "arbol arde"),
    sil("Hasta Shabriri te lo restriega", _G("shabriri"), "Shabriri", "el de la llama frenética", dur=5.4, lado="izq",
        encuadre=(0, .5)),
    rel("Que heredes la llama frenética", "llama_frenetica", "Llama frenética", dur=4.4, x=.76, y=.52),
    cam("la de Hyetta", "hyetta", "Hyetta", dur=3.4, x=.16, y=.66),
    peg("se despide de ti y de Torrentera", "torrentera", "Torrentera", tam=400, x=.78, y=.60),
    msg(["Te buscaré, por muy lejos que vayas.", "Para darte lo que mereces."], ("Te buscaré, por muy lejos", -.1),
        ("la Muerte que está escrita|fin", 1.0), ["Te buscaré", "Para darte lo que mereces"], "te buscare"),
    mg(E.balanza("Quemar a Melina", "Quemar el mundo", [("i", "La chica que te ayudó"), ("d", "Y que te jure la muerte")],
                 remate="Todos elegimos", titulo="Tus dos opciones"),
       ("Esas eran tus dos opciones", -.2), ("Todos elegimos|fin", 1.4),
       ["Quemar a la chica que te ayudó", "o quemar el mundo", "Y elegiste"], "dos opciones"),

    # ---- 1c · la ceniza
    peg("cuando bajas de Farum Azula", "farum_azula", "Farum Azula", tam=420, x=.78, y=.58),
    pant("capital_cinerea", ("se llama ahora Leyndell, capital cinérea", -.3), ("Todo gris|fin", .8), zoom=(1.0, 1.12)),
    sil("El del Zampaheces, el asesino del sótano", _G("zampaheces"), "El Zampaheces", "el asesino del sótano", dur=5.4,
        lado="der", encuadre=(0, .5)),
    rel("Le entregas cinco Maldiciones del semillero", "maldicion_semillero", "Maldición del semillero", dur=5.0, x=.24, y=.52),
    ficha("Su descripción: la maldición vilipendiada", "Runa reparadora de la maldición vilipendiada", "La maldición "
          "vilipendiada durará eternamente, y los hijos del mundo, sus nietos y todas las generaciones venideras *serán sus "
          "pústulas*.", tipo="Runa reparadora", icono="runa_reparadora", a=("serán sus pústulas|fin", 1.0)),
    mg(E.puesto("La doncella, o el mundo", "Se queman contigo"), ("La doncella, o el mundo", -.1), ("Se queman contigo|fin", 1.6), [],
       "se queman", y=.80),
    com("Isaac escribió que cada video", C_ISAAC, dur=6.0),

    # ================================================================ CIERRE
    mg(E.expediente(cargos=["Drogaste a una guerrera", "Mataste por encargo", "Robaste almas y raíces",
                            "Diste ojos y quemaste", "Prendiste fuego al Árbol"], sello="CULPABLE", titulo="Sentencia"),
       ("Esa es la lista", -.2), ("con tu doncella de yesca|fin", 1.6),
       ["Drogaste a una guerrera", "Mataste por encargo", "Le robaste el alma", "Le diste de comer ojos#2",
        "Y prendiste fuego al Árbol", "con tu doncella de yesca"], "sentencia"),
    cam("Godrick quería coserse el poder", "godrick", "Godrick", dur=3.6, x=.16, y=.66),
    mg(E.puesto("A ti te llaman", "Señor del Círculo"), ("Por eso a ti te llaman", -.1), ("y a él, el Injertado|fin", 1.0), [],
       "senor", y=.80),
    msg(["Los comentarios se leen todos."], ("Los comentarios se leen todos", -.1), ("se decide cada video|fin", .6),
        ["Los comentarios se leen todos"], "se leen"),
    com("dos personas pidieron que el acusado", C_WSEF, dur=4.4, x=.28, y=.30, tam=640),
    com("pidieron que el acusado fueras tú", C_AMAND_PED, dur=4.0, x=.72, y=.40, tam=640),
    aba([(_G("rykard"), "Rykard"), (_G("godfrey"), "Godfrey y Godwyn"), (_G("gurranq"), "Maliketh"), (_G("rennala"), "Rennala"),
         (_G("zampaheces"), "Zampaheces y Gideon")],
        ("Ya están apuntados Rykard", -.2), ("y hasta Bayle el Temible", -.3),
        ["Ya están apuntados Rykard", "Godfrey y Godwyn", "Maliketh, Rennala", "el Zampaheces con Gideon", "Midra"],
        "apuntados", x=.50, y=.62, tam=260),
    mg(E.puesto("Y hasta", "Bayle el Temible"), ("y hasta Bayle el Temible", -.1), ("cuál quieres que sea el siguiente|fin", .6),
       [], "bayle", y=.80),
    aba([(_G("marika"), "Márika y Radagon"), (_G("miquella"), "Miquella"), (_G("malenia"), "Malenia"), (_G("ranni"), "Ranni"),
         (_G("radahn"), "Radahn"), (_G("mohg"), "Mohg")],
        ("En el canal tienes las atrocidades", -.2), ("Mohg y Godrick|fin", .6),
        ["de Márika y Radagon", "de Miquella", "Malenia, Ranni", "Melina, Radahn", "Mohg y Godrick"], "en el canal",
        x=.50, y=.62, tam=260),
    mg(E.puesto("Suscríbete", "Rumbo a los 1 000"), ("Y si te suscribes", -.1), ("nos acercas a los mil|fin", .8), [],
       "suscribete", y=.80),
    mg(E.puesto("Ellos", "Sí se acuerdan"), ("Ellos sí se acuerdan", -.1), ("Ellos sí se acuerdan|fin", 2.4), [], "se acuerdan",
       y=.80),
]


# ================================================================ ESCENAS NUEVAS (+5 min, 16-nov relevo 1)
_FX_EXTRA = [
    # ---- 5c · la marioneta de Nepheli
    sil("su sirviente Pidia acaban muertos", _G("pidia"), "Pidia", "el sirviente de Seluvis", dur=5.0, lado="izq",
        encuadre=(0, .5)),
    rel("encuentras la Marioneta de Nepheli Loux", "marioneta_nepheli", "Marioneta de Nepheli Loux", dur=5.0, x=.76, y=.52),
    mg(E.puesto("No se vende", "Solo la tiene quien la drogó"), ("No se vende en la tienda", -.1),
       ("Solo la tiene quien la drogó|fin", 1.2), [], "quien la drogo", y=.80),
    ficha("era una de las marionetas favoritas", "Marioneta de Nepheli Loux", "Los diamantes en bruto merecen un trato especial "
          "*para que su preciado interior no se eche a perder*.", tipo="Cenizas de espíritu", icono="marioneta_nepheli",
          a=("no se eche a perder|fin", .8)),
    mg(E.puesto("Nepheli Loux", "Era"), ("era una guerrera hecha y derecha", -.1), ("hecha y derecha Era|fin", 1.4), [],
       "era", y=.80),
    cam("La guerrera que peleó contigo en Velo", "nepheli", "Nepheli", dur=3.8, x=.84, y=.66),
    mg(E.puesto("Una herramienta", "Más"), ("Como una herramienta más", -.1), ("Como una herramienta más|fin", 1.4), [],
       "herramienta", y=.80),
    sil("Si elegiste al Zampaheces", _G("zampaheces"), "El Zampaheces", "drogado", dur=5.4, lado="der", encuadre=(0, .5)),
    rel("Su marioneta acaba en la tienda", "marioneta_zampaheces", "Marioneta del Zampaheces", dur=4.4, x=.24, y=.52),
    mg(E.puesto("Final perdido", "Bendición de la desesperación"), ("pierdes un final entero del juego", -.1),
       ("la Bendición de la desesperación|fin", 1.0), [], "final perdido", y=.80),
    cam("dársela a Gideon", "gideon", "Gideon", dur=3.8, x=.16, y=.66),
    mg(E.puesto("El juego no premia la decencia", "Premia el frasquito"), ("El juego no premia la decencia", -.1),
       ("Premia el frasquito|fin", 1.4), [], "premia", y=.80),
    mg(E.marionetas(titiritero="Seluvis", munecos=("Nepheli", "Zampaheces", "Ranni"), dueno="Tú", titulo="Todo un titiritero",
                    remate="Eres igual que él"),
       ("Mientras tanto, Seluvis te va tomando cariño", -.2), ("Que eres igual que él|fin", 1.2),
       ["te va tomando cariño", "es como un hijo", "y aun así te las vende", "vas resultando todo un titiritero",
        "Que eres igual que él"], "titiritero"),

    # ---- 4c · tres detalles de la casa
    rel("el tónico que Tanith te dio", "tonico", "Tónico del olvido", dur=5.0, x=.24, y=.52),
    ficha("Su descripción: un regalo del blasfemo", "Tónico del olvido", "Un regalo del blasfemo Rykard para Lady Tanith, quien "
          "por desgracia no pudo darle uso. *Mi señor, no podría haber mayor angustia que olvidarte*.", tipo="Objeto clave",
          icono="tonico", a=("mayor angustia que olvidarte|fin", 1.0)),
    sil("borrarle la memoria a Rya", _G("rya"), "Rya", "su hija adoptiva", dur=5.0, lado="der", encuadre=(0, .5)),
    rel("te pagan con el mismo talismán", "pesar_daedicar", "Pesar de Daedicar", dur=5.0, x=.24, y=.52),
    ficha("Su descripción habla de una mujer", "Pesar de Daedicar", "Una mujer que se entregó a todos los tipos imaginables de "
          "adulterio y placer impío, *dando a luz a una infinidad de grotescos hijos*.", tipo="Talismán", icono="pesar_daedicar",
          a=("decidas lo que decidas|fin", .6)),
    rel("El segundo detalle es la Máscara de consorte", "mascara_consorte", "Máscara de consorte", dur=5.4, x=.24, y=.52),
    ficha("Su descripción cuenta que Tanith", "Máscara de consorte", "Fue la única humana que permaneció a su lado cuando se "
          "transformó en la serpiente blasfema. *Fue entonces cuando quedó cautivada por él*.", tipo="Yelmo",
          icono="mascara_consorte", a=("quedó cautivada por él|fin", .8)),
    mg(E.puesto("A ella", "Las escamas"), ("A unas les gustan las flores", -.1), ("las escamas|fin", 1.4), [], "escamas", y=.80),
    sil("te invade el Caballero de Tanith", _G("caballero_tanith"), "Caballero de Tanith", "te invade", dur=5.0, lado="izq",
        encuadre=(0, .5)),
    pant("elphael", ("en Elphael, tutor del Árbol Hierático", -.3), ("hay dos signos en el suelo|fin", .6), zoom=(1.0, 1.10)),
    grande("El signo dorado te lleva a ayudar a Millicent", "millicent", "Millicent", lado="der", dur=5.0, tam=560),
    rel("la Prótesis de Millicent", "protesis_millicent", "Prótesis de Millicent", dur=4.6, x=.24, y=.52),
    mg(E.puesto("Ya ni hace falta carta", "Basta con un signo rojo"), ("Ya ni hace falta carta", -.1),
       ("Basta con un signo rojo|fin", 1.4), [], "signo rojo", y=.80),

    # ---- 3d · Rennala en la pelea
    ban("Te habla con ternura", _G("rennala"), "Rennala", "te quiere de hijo", foco=(.5, .3, 2.0), dur=4.6),
    mg(E.puesto("Tú vienes a robarle", "Y ella te quiere de hijo"), ("Tú vienes a robarle", -.1),
       ("y ella te quiere de hijo|fin", 1.2), [], "de hijo", y=.80),
    cam("Su pequeña Ranni", "ranni", "Ranni", dur=4.0, x=.84, y=.66),
    rel("Y el huevo que abraza todo el tiempo", "runa_nonatos", "Gran Runa de los Nonatos", dur=5.0, x=.24, y=.52),
    ficha("Su descripción: huevo ámbar custodiado", "Gran Runa de los Nonatos", "Huevo ámbar custodiado por Rennala, la Reina de "
          "la Luna Llena. *Gran Runa de semidioses sin nacer*.", tipo="Gran Runa", icono="runa_nonatos",
          a=("se lo quitaste de los brazos|fin", .6)),
    sil("Ranni lo dejó dicho así", _G("ranni"), "Ranni", "la hija de Rennala", dur=5.0, lado="der", encuadre=(0, .5)),
    msg(["Maldito intruso. Haz que corra la voz.", "De la última reina de Caria."], ("llamándote maldito intruso", -.1),
        ("la magnificencia de la noche que conjuró|fin", .6), ["llamándote maldito intruso", "de la última reina de Caria"], "corre la voz"),

    # ---- 3e · campanas, Enia y el eco de Márika
    mg(E.puesto("Siete mausoleos", "Hasta la fotocopiadora tiene límite"), ("Hasta la fotocopiadora tiene límite", -.1),
       ("Hasta la fotocopiadora tiene límite|fin", 1.4), [], "limite", y=.80),
    sil("vas con la Lectora de Dedos Enia", _G("enia"), "Enia", "Lectora de Dedos", dur=5.0, lado="izq", encuadre=(0, .55)),
    msg(["El poder de su homónimo puede ser", "liberado por la Lectora de Dedos."], ("Cada recuerdo lo anuncia", -.1),
        ("liberado por la Lectora de Dedos|fin", .8), ["el poder de su homónimo", "liberado por la Lectora"], "homonimo"),
    rel("Así sacaste el Rencor de Rykard", "rencor_rykard", "Rencor de Rykard", dur=4.6, x=.76, y=.52),
    cam("Márika ya se lo había advertido", "marika", "Márika", dur=4.4, x=.16, y=.66),
    mg(E.puesto("Si no llegan a ser nada", "Solo quedarán como sacrificios"), ("Que solo quedarán como sacrificios", -.2),
       ("Que solo quedarán como sacrificios|fin", 1.4), [], "sacrificios", y=.80),
    mg(E.puesto("Márika escribió la regla", "Tú la aplicaste"), ("Márika escribió la regla", -.1),
       ("semidiós por semidiós|fin", 1.2), [], "regla", y=.80),

    # ---- 2d · como desees
    mg(E.puesto("Gesto", "Como desees"), ("Se llama Como desees", -.1), ("Muy apropiado|fin", 1.0), [], "como desees", y=.80),
    msg(["Manos temblorosas.", "Aúllan sin palabras."], ("Le ponen encima sus manos temblorosas", -.1),
        ("le acarician los ojos con suavidad|fin", .8), ["sus manos temblorosas", "Aúllan sin palabras"], "manos"),
    sil("aparece Shabriri, metido en el cuerpo de Yura", _G("yura"), "Yura", "con Shabriri dentro", dur=5.4, lado="der",
        encuadre=(0, .5)),
    rel("el Pesar de Shabriri", "pesar_shabriri", "Pesar de Shabriri", dur=5.0, x=.24, y=.52),
    ficha("Se dice que a este hombre", "Pesar de Shabriri", "Le arrancaron los ojos como castigo por sus calumnias y, con el "
          "tiempo, *la plaga de la llama de la locura llegó a habitar sus cuencas vacías*.", tipo="Talismán",
          icono="pesar_shabriri", a=("sus cuencas vacías|fin", .8)),
    aba([(_G("shabriri"), "Un hombre sin ojos"), (_G("uva_shabriri"), "Una uva que es un ojo"), (_G("hyetta"), "Una chica ciega")],
        ("Un hombre sin ojos", -.2), ("que se los come|fin", 1.0),
        ["Un hombre sin ojos", "Una uva que es un ojo", "Y una chica ciega"], "tres ojos", x=.50, y=.62, tam=300),
    grande("Y Hyetta tiene muy claro", "hyetta", "Hyetta", lado="izq", dur=5.0, tam=560),
    mg(E.puesto("No te pidió que la salvaras", "Te pidió que acabaras con todo"), ("No te pidió que la salvaras", -.1),
       ("Te pidió que acabaras con todo|fin", 1.0), [], "acabar", y=.80),

    # ---- 1d · la yesca con contrato
    sil("Y Melina te lo había dicho", _G("melina"), "Melina", "no era tu doncella", dur=5.4, lado="der", encuadre=(0, .5)),
    msg(["No soy ninguna doncella."], ("No soy ninguna doncella", -.1), ("No soy ninguna doncella|fin", 1.6),
        ["No soy ninguna doncella"], "ninguna doncella"),
    mg(E.puesto("No era tu doncella", "Era tu yesca, con contrato"), ("No era tu doncella", -.1),
       ("Era tu yesca, con contrato|fin", 1.4), [], "yesca contrato", y=.80),
    cam("Enia, la Lectora de Dedos", "enia", "Enia", dur=4.4, x=.16, y=.66),
    rel("La Aguja de Miquella", "aguja_miquella", "Aguja de Miquella", dur=5.0, x=.24, y=.52),
    peg("la arena del Señor dragón Placidusax", "placidusax", "Señor dragón Placidusax", tam=420, x=.78, y=.58),
    ficha("Su descripción: capaz de subyugar", "Aguja de Miquella", "Capaz de subyugar a la llama frenética una vez heredada, "
          "*lo cual permite engañar al destino*.", tipo="Objeto clave", icono="aguja_miquella", a=("engañar al destino|fin", 1.0)),
    mg(E.puesto("Engañar al destino, sí", "Al Árbol, no"), ("Engañar al destino, sí", -.1),
       ("El incendio se queda donde estaba|fin", .8), [], "al arbol no", y=.80),
    mg(E.triada([("Era de fragilidad", "Era de los nacidos en la oscuridad"), ("Era del orden", "Bendición de la desesperación"),
                 ("Señor de la Llama Frenética", "Era estelar")], titulo="Seis finales"),
       ("Y eso vale para todos", -.2), ("el Árbol ya ardió|fin", 1.2),
       ["Era de fragilidad", "Era del orden", "Señor de la Llama Frenética. Era estelar"], "seis finales"),
]

_FX_EXTRA = [
    # ---- 5c · Dolores
    rel("La Marioneta de Dolores, la Flecha Durmiente", "marioneta_dolores", "Marioneta de Dolores", dur=5.0, x=.24, y=.52),
    ficha("donde fue crítica a la par que amiga", "Marioneta de Dolores", "Perteneció en su día a la Mesa Redonda, donde fue "
          "crítica a la par que amiga de Gideon el Omnisciente. *Ella fue la causante de la enemistad entre este último y "
          "Seluvis*.", tipo="Cenizas de espíritu", icono="marioneta_dolores", a=("la enemistad entre este último y Seluvis|fin", 1.0)),
    aba([(_G("gideon"), "Gideon"), (_G("marioneta_dolores"), "Dolores"), (_G("seluvis"), "Seluvis")],
        ("Dos viejos de la Mesa Redonda", -.2), ("la acabó metiendo en un frasco|fin", .6),
        ["Dos viejos", "por la misma mujer", "la acabó metiendo en un frasco"], "dolores", x=.50, y=.62, tam=300),
    mg(E.puesto("Tú", "Solo pasas por caja"), ("Tú solo tienes que pasar por caja", -.1),
       ("Tú solo tienes que pasar por caja|fin", 1.4), [], "caja", y=.80),
    # ---- 3f · el Rencor por dentro
    rel("su descripción no termina en las fauces", "rencor_rykard", "Rencor de Rykard", dur=5.0, x=.24, y=.52),
    ficha("Estos espíritus se manifiestan", "Rencor de Rykard", "Estos espíritus se manifiestan a partir del rencor de los "
          "héroes que sufrieron un final violento. *Y en el interior de las entrañas de la serpiente, se convirtieron en sus "
          "semejantes*.", tipo="Hechizo", icono="rencor_rykard", a=("se convirtieron en sus semejantes|fin", 1.0)),
    mg(E.audiencia(titulo="Dentro de la serpiente", remate="Tú llegaste con más hambre"), ("Cada vez que lo lanzas", -.2),
       ("con más hambre que la serpiente|fin", 1.4),
       ["lanzas a los que fueron", "antes que tú", "a esa audiencia", "con más hambre que la serpiente"], "audiencia 2"),
    mg(E.puesto("Otra vez trabajando para alguien", "Ahora, para ti"), ("Otra vez trabajando para alguien", -.1),
       ("Ahora, para ti|fin", 1.2), [], "para ti", y=.80),
]
