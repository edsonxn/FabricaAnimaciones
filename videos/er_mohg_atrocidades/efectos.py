# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Mohg QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 10-nov-2026).
Fórmula de Morgott/Radahn (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS) con el kit de
Elden Ring (nucleo/mg_er.py) y los estilos de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS reales de eldenring.fandom.com (bajar_pegatinas.py; identidad comprobada en previews/pegatinas_check.jpg).
- COMENTARIOS reales (≤ 10 días, _tarjetas.py): Zohary (pidió el tema), Justin ×2, Dany e Isaac (agradecen), Jonathan (corrige),
  Nikova (la crítica, con burla disfrazada), José Luis, David, Eternalack y Escuadrón (cierre).
- FICHAS solo con citas del guion (verificadas en _investigacion/).
- MG NUEVOS (mg_er): `cuenta_atras` (Tres/Duo/Unus/Nihil), `reclutamiento` (la escalera de Varré, 3 apariciones) y `dinastia`
  (organigrama; la sangre sube a la Madre Informe, 4 apariciones). Además `cien`, `mensaje` y `puesto` del kit.
- MAPAS (mundo): Necrolimbo, Iglesia de la Rosa, Ruinas de Sanguifuria, las tres doncellas, el norte, el portal.
- PISTAS voz=True: las 5 líneas originales del juego (sfx/s_*.mp3) con la voz callada (`post` en guion.py).
  python fab.py er_mohg_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
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


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None),
             en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + nombre, ver=1.6)
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


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)



C_ZOHARY, C_JUSTIN1, C_JUSTIN2 = "UgzQzkzQm8Hgtqtjn4V4AaABAg", "UgwZNOqIbIepAyMYwcF4AaABAg", "Ugwwr2Qj8QL7rlGZMfd4AaABAg"
C_DANY, C_ISAAC, C_JONATHAN = "Ugx8DJiYZSnW7fEi4FZ4AaABAg", "Ugw1bm9aV6wukwm3RZZ4AaABAg", "UgzvfipRMhMbWKhpEa14AaABAg"
C_NIKOVA, C_JOSE, C_DAVID = "UgwYiYKsYsRQ1IFZUp14AaABAg", "Ugz8dOeV0BvZ8fzrW5x4AaABAg", "UgztGOwx19tTZK-XWsV4AaABAg"
C_ETERNAL, C_ESCUADRON = "Ugxbkmo3yYrzzhvuEdh4AaABAg", "Ugy3J9g_I8ZqBY_rauV4AaABAg"
PASOS = [("Varré", "el Rostro Alabastrado"), ("Dedo infestado", "invade tres veces"), ("El paño", "sangre de una doncella"),
         ("La medalla", "caballero de sangre pura")]
RAMAS = [("Dedos Sangrientos", "cazan Sinluz"), ("Caballeros", "de sangre pura"), ("Nobles sanguinos", "su corte"),
         ("Cirujanos", "raptados"), ("Albináuricos", "con cuernos")]

# Las 5 líneas ORIGINALES del juego, con la voz callada (regla del 31-oct-2026; cortes en sfx/, verificados con Whisper)
PISTAS = [
    dict(sfx="s_maidenless", en="Así suena en inglés|fin", vol=1.0, voz=True),
    dict(sfx="s_scream", en="Escúchalo de su boca|fin", vol=1.0, voz=True),
    dict(sfx="s_welcome", en="Así lo dice él|fin", vol=1.0, voz=True),
    dict(sfx="s_nihil", en="Escúchalo.#2|fin", vol=1.0, voz=True),
    dict(sfx="s_mohgwyn", en="el nombre de su casa|fin", vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    com("En el video de Morgott, Zohary nos dejó este comentario", C_ZOHARY, dur=7.0),
    mg(E.cuenta_atras(titulo="Como lo firmaría Mohg", remate="Así lo firmó Zohary"), ("Y lo firmó como lo firmaría", -.2),
       ("Nihil, Nihil, Nihil|fin", .8), ["Y lo firmó", "en su pelea", "Nihil, Nihil", "Nihil, Nihil, Nihil"], "nihil gancho"),
    com("Ese mismo día, Justin nos lo pidió dos veces", C_JUSTIN1, dur=4.0, x=.30, y=.30),
    com("Así que aquí lo tienes, Zohary", C_JUSTIN2, dur=3.6, x=.70, y=.36),
    grande("Tu patrón, con palacio, tridente", "mohg", "Mohg, Señor de la Sangre", lado="der", dur=5.0, tam=620),
    *fila("El gemelo de Morgott, con cuernos", [
        ("morgott_icono", "Morgott", None),
        ("mohg", "Mohg", "con cuernos, alas negras")], dur=5.0, tam=360),
    pant("palacio", ("un pantano rojo en el sótano del mundo", -.6), ("Nadie necesita un video para saber que es malo|fin", .3),
         zoom=(1.0, 1.10)),
    cam("En el video de Miquella vimos que lo tenían encantado", "miquella", "Miquella", dur=4.0, x=.80, y=.66),
    peg("su cuerpo acabó siendo el recipiente de Radahn", "radahn", "Radahn", tam=400),
    aba([(_G("icono_dedos"), "A quién recluta"), (_G("pano_rojo"), "Qué les pide"), (_G("mascara_blanca"), "Qué les hace"),
         (_G("dios_exterior"), "Con quién habló")],
        ("No explica a quién recluta", -.2), ("mucho antes de que Miquella apareciera en su vida|fin", .6),
        ["a quién recluta", "qué les pide", "qué les hace", "con quién habló allá abajo"], "no explica", x=.50, y=.62),
    puesto("Así que van las cinco peores atrocidades", "Las 5 peores atrocidades de", "Mohg", dur=4.4),
    rel("la madre de la verdad desea una herida", "rios", "Ríos de Sangre", dur=4.6),
    msg(["La madre de la verdad", "desea una herida."], ("guárdate esta frase para el final", -.1),
        ("la madre de la verdad desea una herida|fin", 1.0), ["la madre de la verdad", "desea una herida"], "frase final"),

    # ================================================================ 5 · TE CONVIERTE EN CAZADOR DE LOS TUYOS
    puesto("Número cinco. Te convierte en cazador", "Atrocidad número 5", "Cazador de los tuyos"),
    mapa("mundo", [(.395, .735, "La primera gracia", "Necrolimbo", _G("varre"))],
         ("Sales de la cueva del principio", -.3), ("das tres pasos por Necrolimbo|fin", 1.4),
         ["das tres pasos por Necrolimbo"], titulo="Necrolimbo", sub="El primer paso", ventana=True, traza=99),
    sil("Varré, el Rostro Alabastrado", _G("varre"), "Varré", "el Rostro Alabastrado", dur=5.0, lado="der", encuadre=(0, .5)),
    ficha("Por desgracia para ti, no tienes doncella", "Varré", "Por desgracia para ti, *no tienes doncella*. Sin guía, sin la "
          "fuerza de las runas y sin invitación a la Mesa Redonda. Tu destino, al parecer, es morir en el anonimato.",
          tipo="Lo que te dice", a=("es morir en el anonimato|fin", .4)),
    mg(E.puesto("Así suena", "Maidenless"), ("Así suena en inglés|fin", .0), ("Así suena en inglés|fin", 5.8), [], "maidenless",
       y=.80),

    # ---- 5b · los Dedos Sangrientos
    cam("a por Godrick y su Gran Runa", "godrick", "Godrick", dur=3.8, x=.80, y=.66),
    msg(["¡Bravo!"], ("Hasta te deja un mensaje en el suelo", -.1), ("el gesto de bravo|fin", 1.0), ["el gesto de bravo"], "bravo"),
    mapa("mundo", [(.395, .735, "Necrolimbo", "el primer paso"), (.33, .66), (.25, .60),
                   (.17, .56, "Iglesia de la Rosa", "Liurnia", _G("varre_cara"))],
         ("Hasta que lo encuentras en Liurnia", -.3), ("en la puerta de la Iglesia de la Rosa|fin", 1.2),
         ["en Liurnia", "en la puerta de la Iglesia de la Rosa"], titulo="Liurnia de los Lagos", sub="La segunda cita", traza=99),
    peg("los Dos Dedos, los dioses que guían a los Sinluz", "dos_dedos", "Los Dos Dedos", tam=420, x=.80, y=.60),
    ficha("Si le dices que te parecieron extraños", "Varré", "Las palabras de los Dos Dedos no son de fiar. Desvaríos seniles. "
          "Y lo peor de todo: *los Dedos no sienten ningún amor por los nuestros*.", tipo="Lo que te dice",
          a=("ningún amor por los nuestros|fin", .8)),
    rel("Cinco Dedos Sangrientos Infestados", "dedo_infestado", "Dedo Sangriento Infestado", dur=5.0, x=.24, y=.52),
    ficha("Un objeto para invadir el mundo de otros Sinluz", "Dedo Sangriento Infestado", "Para invadir el mundo de otros "
          "Sinluz. *Y matarlos*.", tipo="Herramienta", icono="dedo_infestado", a=("Y matarlos|fin", .8)),
    msg(["Fueron despreciados por la gracia,", "abandonados por los Dos Dedos."], ("No hay razón para dudar", -.1),
        ("abandonados por los Dos Dedos|fin", .6), ["despreciados por la gracia", "abandonados por los Dos Dedos"], "dudar"),
    mapa("mundo", [(.17, .56, "Iglesia de la Rosa", "Varré"), (.24, .48), (.30, .42),
                   (.355, .375, "Ruinas de Sanguifuria", "Magnus", _G("magnus"))],
         ("El encargo es invadir tres veces", -.3), ("en el altiplano|fin", .8),
         ["al pobre Magnus", "en las Ruinas de Sanguifuria", "en el altiplano"], titulo="Meseta de Altus", sub="La invasión",
         ventana=True, traza=99),
    peg("al pobre Magnus, la Garra de la Bestia", "magnus", "Magnus, la Garra de la Bestia", tam=420, x=.20, y=.62),
    ficha("Cuando vuelves, Varré está encantado", "Varré", "Me alegra que disfrutes de mi regalo. Lo supe desde el principio. "
          "*Tienes gusto por la sangre noble*.", tipo="Lo que te dice", a=("Tienes gusto por la sangre noble|fin", .8)),
    mg(E.dinastia(filas=RAMAS[:1], titulo="La Dinastía Mohgwyn", remate=""), ("Ese es el primer oficio de la dinastía", -.2),
       ("Los Dedos Sangrientos|fin", 1.0), ["Ese es el primer oficio", "Sinluz cazando Sinluz"], "dinastia 1"),
    # suscripción ANTES DEL MINUTO 5 (el usuario, 10-nov-2026)
    mg(E.puesto("Suscríbete", "650 → 1 000"), ("si llegaste por Mohg y te está gustando, suscríbete", -.1),
       ("y la meta es mil|fin", .8), [], "suscripcion 1", y=.80),
    rel("sin dedos infestados", "dedo_infestado", "Sin dedos infestados", dur=3.6, x=.80, y=.50),
    cam("Tú eres de la Mesa Redonda buena", "icono_pureblood", "Mesa Redonda buena", dur=3.8, x=.16, y=.66),
    sil("Yura, el cazador que te echa una mano", _G("yura"), "Yura", "cazador de Dedos Sangrientos", dur=5.0, lado="izq",
        encuadre=(0, .5)),
    ficha("los describe sin rodeos", "Yura", "Sinluz esclavizados por la sangre. Fanáticos que acechan a los suyos. Su locura "
          "impide cualquier parentesco. *Que tus emociones no detengan tu espada*.", tipo="Lo que te dice",
          a=("Que tus emociones no detengan tu espada|fin", .8)),
    pant("nerijus_full", ("El primero que te sale en Necrolimbo", -.2), ("bajo el puente donde patrulla la Caballería nocturna|fin", .4),
         zoom=(1.0, 1.10)),
    cam("es un Dedo Sangriento al que Yura conocía", "nerijus", "Nerijus", dur=3.8, x=.80, y=.66),
    sil("Eleonora, la Dedo Sangriento Violeta", _G("eleonora"), "Eleonora", "Dedo Sangriento Violeta", dur=5.0, lado="der",
        encuadre=(0, .45)),
    rel("su ataque se comparaba con un torbellino", "guja_eleonora", "Guja de Eleonora", dur=4.6, x=.24, y=.52),
    ficha("dice su arma, su leyenda está manchada", "Guja de Eleonora", "Su ataque se comparaba con un torbellino. *Ahora su leyenda "
          "está manchada de sangre maldita*.", tipo="Arma", icono="guja_eleonora", a=("manchada de sangre maldita|fin", .8)),
    rel("Ríos de Sangre, la katana de Okina", "rios", "Ríos de Sangre", dur=5.0, x=.76, y=.52),
    pant("okina_rios", ("Su descripción cuenta que", -.1), ("le hizo una propuesta|fin", .3), zoom=(1.0, 1.10)),
    ficha("una vida de demonio", "Ríos de Sangre", "Mohg, el Señor de la Sangre, sintió en su propia carne la espada y la locura "
          "de Okina, y le hizo una propuesta: *una vida de demonio. Una sed que nunca se sacia*.", tipo="Arma", icono="rios",
          a=("Una sed que nunca se sacia|fin", 1.0)),
    mg(E.puesto("Recluta", "asesinos de su propia gente"), ("Recluta asesinos de su propia gente", -.1),
       ("Recluta asesinos de su propia gente|fin", 1.2), [], "asesinos", y=.80),
    sil("el primero al que le ofrece el trabajo", _G("varre"), "Varré", "el reclutador", dur=4.4, lado="izq", encuadre=(0, .5)),

    # ================================================================ 4 · TE PIDE LA SANGRE DE UNA DONCELLA
    puesto("Número cuatro. Te pide la sangre", "Atrocidad número 4", "La sangre de una doncella"),
    ficha("Quiero ungirte como caballero", "Varré", "Un caballero al servicio del *Corifeo Mohg, el Señor de la Sangre*, para "
          "fundar una nueva dinastía. El Corifeo tiene fuerza, visión y, por supuesto, amor.", tipo="Lo que te dice",
          a=("y, por supuesto, amor|fin", .8)),
    msg(["Te dará un día o dos", "para que se te destapen los oídos."], ("Si le dices que no, no se enfada", -.1),
        ("para que se te destapen los oídos|fin", .8), ["a lo mejor lo oíste mal", "para que se te destapen los oídos"], "oidos"),
    rel("te entrega un paño de juramento blanco", "pano_limpio", "Favor del Señor de la Sangre", dur=5.0, x=.76, y=.52),
    mg(E.reclutamiento(PASOS[:3], remate=""), ("Y la prueba final", -.2), ("empapa el paño con la sangre de una doncella|fin", 1.0),
       ["Y la prueba final", "Y la prueba final", "empapa el paño"], "reclutamiento 1"),
    ficha("Y lo explica con toda la calma del mundo", "Varré", "Normalmente, este ritual implicaría *matar a tu propia doncella* y "
          "renegar de la sabiduría de los Dos Dedos. Pero como no tienes doncella, sirve la sangre de la doncella de cualquiera.",
          tipo="Lo que te dice", a=("sirve la sangre de la doncella de cualquiera|fin", .6)),
    grande("mataban a la doncella que los guiaba", "melina", "Una doncella: la que te guía", lado="der", dur=5.0, tam=560),
    mapa("mundo", [(.395, .735, "Capilla de la Espera", "tu doncella"), (.29, .42, "Iglesia de la Inhibición", "la de Vyke",
                                                                          _G("doncella_vyke")),
                   (.40, .82, "Puente del Sacrificio", "Irina", _G("irina"))],
         ("El juego te da tres caminos", -.3), ("la chica ciega del Puente del Sacrificio, en la Península Llorosa|fin", .6),
         ["El cadáver de tu propia doncella", "O la doncella de Vyke", "Matar a Irina"],
         titulo="Las Tierras Intermedias", sub="Tres doncellas", traza=99),
    *fila("La que solo te pide que le lleves una carta", [
        ("irina", "Irina", None),
        ("carta_irina", "Su carta", None),
        ("hyetta", "Hyetta", "sirve Hyetta")], dur=5.4, tam=330),
    mg(E.puesto("Para Varré", "Mientras sangre"), ("Para Varré, da igual cuál", -.1), ("Mientras sangre|fin", 1.0), [],
       "mientras sangre", y=.80),
    rel("el paño cambia de descripción", "pano_rojo", "Favor del Señor de la Sangre", dur=5.0, x=.24, y=.52),
    ficha("Paño de juramento completamente enrojecido", "Favor del Señor de la Sangre", "Paño de juramento completamente "
          "enrojecido, *teñido con la sangre de una doncella*. La prueba final ha terminado.", tipo="Objeto clave",
          icono="pano_rojo", a=("como un caballero que pondrá los cimientos de su dinastía|fin", .6)),

    # ---- 4b · la ceremonia
    ficha("Varré te pide el dedo", "Varré", "Esta sangre noble será *una insignia de honor inmutable*, en cuanto se asiente. "
          "Dentro de ti.", tipo="La ceremonia", a=("Dentro de ti|fin", .8)),
    msg(["Ay, cielos.", "Aprieta los dientes, o algo."], ("Ay, cielos", -.1), ("Aprieta los dientes, o algo|fin", .6),
        ["Ay, cielos", "Aprieta los dientes"], "dientes"),
    ficha("Nunca olvides esa sensación de agonía", "Varré", "Nunca olvides esa sensación de agonía. Porque es lo que te une al "
          "Corifeo Mohg, *a todos nosotros*.", tipo="La ceremonia", a=("a todos nosotros|fin", .6)),
    mg(E.puesto("Tienes el grito más dulce", "mi corderito"), ("Escúchalo de su boca|fin", .0), ("Escúchalo de su boca|fin", 5.8),
       [], "grito", y=.80),

    # ---- 4c · la medalla y el final de Varré
    rel("Luego te da la Medalla", "medalla", "Medalla de caballero de sangre pura", dur=5.0, x=.76, y=.52),
    mg(E.reclutamiento(PASOS, remate="Solo que aún no es el momento"), ("Prueba de que eres un glorioso caballero", -.2),
       ("Solo que aún no es el momento|fin", 1.0),
       ["Prueba de que eres", "Prueba de que eres", "Prueba de que eres", "Úsala para tener audiencia", "Solo que aún no"],
       "reclutamiento 2"),
    msg(["Ten paciencia.", "La nueva dinastía está cerca."], ("Porque Mohg aún duerme junto a la Divinidad", -.1),
        ("La nueva dinastía está cerca|fin", .8), ["Ten paciencia", "La nueva dinastía está cerca"], "paciencia"),
    cam("Y Varré lleva mucho tiempo cobrándola", "varre", "Varré", dur=3.8, x=.80, y=.66),
    rel("eres tú quien lo invade a él", "varre_ramo", "Ramo de Varré", dur=4.4, x=.24, y=.52),
    ficha("se arrastra y le reza a su señor", "Varré", "Oh, Corifeo Mohg, por favor, concédeme la fuerza que me prometiste. "
          "*Lo he dado todo*. Por favor, mi señor.", tipo="Al morir", a=("Por favor, mi señor|fin", .6)),
    mg(E.reclutamiento(PASOS, remate="Y su señor no responde"), ("Respóndeme, Corifeo Mohg", -.2),
       ("no responde|fin", 1.2), ["Respóndeme", "Respóndeme", "Respóndeme", "Respóndeme", "no responde"], "reclutamiento 3"),
    com("Dany nos escribió en el de Morgott", C_DANY, dur=6.0),
    mg(E.puesto("Aquí no se papea a nadie", "Se contesta con cariño"), ("aunque aquí no se papea a nadie", -.1),
       ("Mucho cariño|fin", 1.0), [], "carino", y=.80),
    com("E Isaac nos dejó esto", C_ISAAC, dur=7.5, x=.50, y=.32),
    cam("a diferencia de Varré, aquí sí cumplimos", "varre_cara", "No como Varré", dur=3.8, x=.80, y=.66),

    # ================================================================ 3 · RAPTA Y CORROMPE A LOS QUE CURABAN
    puesto("Número tres. Rapta y corrompe", "Atrocidad número 3", "Rapta a los que curaban"),
    grande("Las Máscaras Blancas sin nombre", "mascara_blanca", "Máscaras Blancas sin nombre", lado="der", dur=4.6, tam=520),
    rel("Su túnica cuenta quiénes eran", "tunica_cirujano", "Túnica de cirujano de guerra", dur=5.0, x=.24, y=.52),
    ficha("Cirujanos de guerra, que en la práctica", "Túnica de cirujano de guerra", "Cirujanos de guerra que en la práctica eran "
          "*verdugos piadosos*: daban el golpe de gracia a los heridos que ya no tenían salvación.", tipo="Armadura",
          icono="tunica_cirujano", a=("para que dejaran de sufrir|fin", .6)),
    ficha("De los cirujanos que raptó el Señor de la Sangre", "Túnica de cirujano de guerra", "De los cirujanos que *raptó* el "
          "Señor de la Sangre, ninguno logró domar la sangre maldita. Ninguno salvo Varré.", tipo="Armadura",
          icono="tunica_cirujano", a=("aunque él era una excepción|fin", .6)),
    mg(E.puesto("Raptó", "No los invitó"), ("Raptó. No los invitó", -.1), ("Raptó. No los invitó|fin", 1.0), [], "rapto", y=.80),
    rel("Y su máscara, la que te quedas", "mascara_blanca", "Máscara blanca", dur=5.0, x=.76, y=.52),
    ficha("la maldición del Señor de la Sangre anima", "Máscara blanca", "La maldición del Señor de la Sangre *anima a quien la "
          "lleva cuando hay derramamiento de sangre*.", tipo="Casco", icono="mascara_blanca", a=("ahora cobran vida con él|fin", .6)),
    *fila("Albináuricos. Los seres pálidos", [
        ("albinaurico", "Albináurico", None),
        ("albinaurico_rojo", "Albináurico de Mohgwyn", "Aquí abajo ya no son pálidos")], dur=6.0, tam=380),
    mapa("mundo", [(.57, .06, "Árbol Hierático", "Miquella"), (.56, .16), (.55, .23, "Campo sacroníveo", None)],
         ("En el norte, camino del Árbol Hierático", -.3), ("brillan con luz sagrada|fin", .6),
         ["camino del Árbol Hierático", "los albináuricos brillan con luz sagrada"], titulo="El norte", sub="El árbol de Miquella",
         ventana=True, traza=99),
    mg(E.puesto("Cuernos de augurio", "un don de la Madre Informe"), ("Cuernos de augurio", -.1), ("Cuernos de augurio|fin", 1.4), [],
       "cuernos", y=.80),
    ficha("La wiki lo resume así", "Albináuricos de Mohgwyn", "Recibieron un don de *la Madre Informe* a través de la sangre de "
          "augurio de Mohg, el Señor de la Sangre.", tipo="Según la wiki", a=("a través de la sangre de augurio|fin", 2.0)),
    mg(E.dinastia(filas=RAMAS[:1] + RAMAS[3:], titulo="La Dinastía Mohgwyn", remate=""), ("A él lo encerraron de niño", -.2),
       ("Y ahora es él quien se los hace crecer a otros|fin", .8), ["A él lo encerraron", "Y ahora#3", "se los hace crecer",
                                                                     "a otros"], "dinastia 2"),

    # ---- 3b · la corte
    sil("Los nobles sanguinos", _G("noble"), "Noble sanguino", None, dur=4.6, lado="izq", encuadre=(0, .5)),
    rel("Las hombreras de metal, dice la túnica", "tunica_noble", "Túnica de noble sanguino", dur=5.0, x=.76, y=.52),
    ficha("son la señal del rango noble", "Túnica de noble sanguino", "Las hombreras de metal son la señal del rango noble *que "
          "piensan reclamar cuando llegue la nueva dinastía*.", tipo="Armadura", icono="tunica_noble",
          a=("cuando llegue la nueva dinastía|fin", .6)),
    rel("Su arma, la Hélice sangrienta", "helice", "Hélice sangrienta", dur=5.0, x=.24, y=.52),
    ficha("la sangre extraída, dice la descripción", "Hélice sangrienta", "Diseñada para perforar la carne. La sangre extraída "
          "*resbala con elegancia* por la hoja.", tipo="Arma", icono="helice", a=("Con elegancia.#2|fin", .8)),
    rel("Impuesto de sangre", "blood_tax", "Impuesto de sangre", dur=5.0, x=.76, y=.52),
    pant("noble_ruinas", ("Uno de esos nobles te espera debajo", -.2), ("donde invades a Magnus por encargo de Varré|fin", .4),
         zoom=(1.0, 1.10)),
    mapa("mundo", [(.355, .375, "Ruinas de Sanguifuria", "un noble"), (.40, .38), (.46, .40, "Leyndell", "Esgar, abajo",
                                                                                      _G("esgar"))],
         ("Y uno de sus sacerdotes está metido", -.3), ("con dos perros que te hacen sangrar|fin", .4),
         ["en el corazón de la capital", "Esgar, Sacerdote de la Sangre"], titulo="Hasta la capital", sub="La corte de Mohg",
         ventana=True, traza=99),
    peg("Esgar, Sacerdote de la Sangre", "esgar", "Esgar, Sacerdote de la Sangre", tam=440, x=.20, y=.62),
    pant("palacio", ("Todo eso sale de un palacio levantado sobre una tumba", -.2), ("El mapa lo dice|fin", .3), zoom=(1.0, 1.12)),
    msg(["En las más tenebrosas profundidades", "yace la tumba de una antigua civilización."], ("El mapa lo dice", .2),
        ("está construyendo un panteón para albergar a su futura dinastía|fin", .4),
        ["en las más tenebrosas profundidades", "yace la tumba"], "mapa del palacio"),
    pant("estatua", ("Los dioses barbudos de piedra", -.2), ("mirando un altar empapado de sangre|fin", .3), zoom=(1.0, 1.10)),
    rel("el encantamiento Enjambre de moscas te lo dice", "moscas", "Enjambre de moscas", dur=5.0, x=.24, y=.52),
    ficha("el nuevo palacio del Señor de la Sangre", "Enjambre de moscas", "El nuevo palacio del Señor de la Sangre está en un "
          "pantano de *sangre putrefacta*, y estas moscas nacen del excremento de esa tierra.", tipo="Encantamiento",
          icono="moscas", a=("nacen del excremento de esa tierra|fin", .6)),
    ficha("El Excremento manchado de sangre", "Excremento manchado de sangre", "Carne a medio digerir y colonias de huevos "
          "diminutos, de origen desconocido. *Pero sin duda repugnante*.", tipo="Material", icono="excremento",
          a=("pero sin duda repugnante|fin", 1.0)),
    com("Por cierto, Jonathan nos corrigió", C_JONATHAN, dur=6.5),
    *fila("Y su gemelo también lo era", [
        ("morgott_icono", "Omen King", "en inglés es Omen King"),
        ("mohg_icono", "El gemelo", "Y su gemelo también lo era")], dur=6.0, tam=360),

    # ================================================================ 2 · ROBA UN DIOS DORMIDO
    puesto("Número dos. Roba un dios dormido", "Atrocidad número 2", "Roba un dios dormido"),
    mapa("mundo", [(.46, .40, "Leyndell", None), (.52, .30), (.55, .23, "Campo sacroníveo", None), (.56, .14),
                   (.57, .06, "Árbol Hierático", "un cascarón")],
         ("Al norte del mundo", -.3), ("ya no es más que un cascarón|fin", .4),
         ["más allá del Campo sacroníveo", "está el Árbol Hierático"], titulo="Al norte del mundo", sub="El Árbol Hierático",
         traza=99),
    cam("Gideon, el Omnisciente de la Mesa Redonda", "gideon_cara", "Gideon", dur=4.0, x=.80, y=.66),
    ficha("Se rumoreaba que Miquella se había incrustado", "Gideon", "Se rumoreaba que Miquella se había incrustado en el árbol. "
          "Pero antes de que pudiera terminar, *alguien abrió el árbol y huyó con su forma infante*.", tipo="Lo que dice",
          a=("huyó con su forma infante|fin", .8)),
    grande("Ese alguien es Mohg", "mohg_modelo", "Mohg: el que huyó con él", lado="der", dur=5.0, tam=600),
    *fila("Malenia, su hermana gemela", [
        ("malenia", "Malenia", None),
        ("miquella", "Miquella", "a un hermano que ya no estaba")], dur=6.0, tam=360),
    mapa("mundo", [(.55, .23, "Campo sacroníveo", "el portal", _G("mohg")), (.55, .30), (.54, .45, "Palacio de Mohgwyn",
                                                                                         "bajo tierra")],
         ("Fíjate en el camino", -.3), ("En el camino al Árbol Hierático|fin", .8),
         ["un portal escondido", "En el camino al Árbol Hierático"], titulo="El camino", sub="Del portal al palacio",
         ventana=True, traza=99),
    rel("Su recuerdo lo cuenta", "recuerdo_mohg", "Recuerdo del Señor de la Sangre", dur=5.0, x=.24, y=.52),
    ficha("con el deseo de convertir a Miquella", "Recuerdo del Señor de la Sangre", "Con el deseo de convertir a Miquella en una "
          "deidad de pleno derecho, Mohg trató de convertirse en su consorte. Sin embargo, por más que trató de compartir con él "
          "su alcoba, *jamás recibió respuesta del joven empíreo*.", tipo="Recuerdo", icono="recuerdo_mohg",
          a=("jamás recibió respuesta del joven empíreo|fin", .8)),
    ficha("En inglés hay una palabra que la traducción se calla", "Recuerdo del Señor de la Sangre · en inglés",
          "No es su alcoba. Es su *alcoba sangrienta*. En japonés, *su lecho de sangre*.", tipo="Lo que se calla",
          a=("En japonés, su lecho de sangre|fin", .8)),
    msg(["Miquella es mío,", "y solo mío."], ("Entre sus frases hay una que lo resume todo", -.1), ("y solo mío|fin", .6),
        ["Miquella es mío", "y solo mío"], "mio"),
    ficha("en otra que el juego nunca llegó a usar", "Mohg · diálogo sin usar", "Nadie más te llevará. *Nunca más, lo juro*.",
          tipo="Cortado del juego", a=("Nunca más, lo juro|fin", .8)),
    mg(E.puesto("Bienvenido", "invitado de honor"), ("Así lo dice él|fin", .0), ("Así lo dice él|fin", 9.8), [], "welcome",
       y=.80),

    # ---- 2b · el lago de sangre
    rel("El talismán Exaltación del Señor de la Sangre", "exaltacion", "Exaltación del Señor de la Sangre", dur=5.0, x=.76, y=.52),
    ficha("rendid vuestras ofrendas de sangre", "Exaltación del Señor de la Sangre", "Rendid vuestras ofrendas de sangre a vuestro "
          "señor. Empapad la alcoba de mi consorte. Saciad la sed de su crisálida. *Su despertar anunciará el alba de nuestra "
          "dinastía*.", tipo="Talismán", icono="exaltacion", a=("el alba de nuestra dinastía|fin", .8)),
    mg(E.dinastia(filas=RAMAS, titulo="De dónde sale tanta sangre", remate=""), ("Ofrendas de sangre#2", -.2),
       ("de cada Sinluz al que invaden|fin", .8),
       ["Ofrendas de sangre#2", "De los Dedos Sangrientos", "de los caballeros#2", "Y no hace falta", "Y no hace falta",
        "de cada Sinluz"], "dinastia 3"),
    pant("capullo_arte", ("Su sala es eso", -.2), ("y alrededor, sangre|fin", .4), zoom=(1.0, 1.12), oscuro=.1),
    peg("Ansbach, su antiguo comandante", "ansbach", "Ansbach", tam=420, x=.80, y=.60),
    com("Nikova nos escribió en el de Radahn", C_NIKOVA, dur=6.5),
    aba([(_G("icono_mohgwyn"), "Plan"), (_G("icono_pureblood"), "Escudo de armas"), (_G("tunica_noble"), "Uniforme"),
         (_G("dedo_infestado"), "Reclutamiento")],
        ("Por eso hoy elegimos a uno con la cabeza perfectamente en su sitio", -.2), ("departamento de reclutamiento|fin", .8),
        ["Con plan", "con escudo de armas", "con uniforme", "departamento de reclutamiento"], "cabeza en su sitio", x=.50, y=.62),
    mg(E.puesto("Con cariño, Nikova", "Mohg no estaba loco"), ("Y la peor de todas, la número uno", -.1),
       ("mucho antes#2|fin", 1.0), [], "nikova", y=.80),
    mg(E.cien("De cada 100 que ven Runa Caída", 4, remate=("Solo unas 4 están suscritas", 2)),
       ("Antes del número uno, el dato de siempre", -.3), ("y la meta es mil#2|fin", 1.4),
       ["De cada cien personas", "solo unas cuatro están suscritas"], "cien"),
    mg(E.puesto("Basta con un botón", "650 → 1 000"), ("Aquí basta con un botón", -.1), ("en el siguiente video|fin", 1.0), [],
       "boton", y=.80),

    # ================================================================ 1 · SU DIOS DESEA UNA HERIDA
    puesto("Número uno. Su dios desea una herida", "Atrocidad número 1", "Su dios desea una herida"),
    rel("Lo dice el Grillete de Mohg", "grillete_mohg", "Grillete de Mohg", dur=5.0, x=.24, y=.52),
    ficha("estos se hicieron para mantener", "Grillete de Mohg", "Estos se hicieron para mantener *a un augurio concreto* bajo el "
          "más estricto encierro.", tipo="Herramienta", icono="grillete_mohg", a=("bajo el más estricto encierro|fin", .8)),
    rel("El encantamiento Favor sanguino lo cuenta", "bloodboon", "Favor sanguino", dur=5.0, x=.76, y=.52),
    ficha("la madre de la verdad desea heridas", "Favor sanguino", "La madre de la verdad desea heridas. Cuando Mohg se encontró "
          "ante ella, su sangre maldita estalló en llamas. *Y quedó prendado de la impureza con la que había nacido*.",
          tipo="Encantamiento", icono="bloodboon", a=("con la que había nacido|fin", .8)),
    *fila("Su gemelo hizo justo lo contrario", [
        ("morgott_icono", "Morgott: la encerró", None),
        ("mohg_icono", "Mohg: la adoró", "Mohg, en cambio, la encendió")], dur=6.0, tam=360),
    mg(E.dinastia(filas=RAMAS, titulo="La Dinastía Mohgwyn", remate="Lo único que pide: heridas"), ("La Madre Informe. Un dios", -.3),
       ("lo único que pide es eso|fin", 1.0), ["La Madre Informe. Un dios"] * 6 + ["Un dios exterior", "lo único que pide es eso"], "dinastia 4"),
    rel("Su tridente, la Lanza sagrada de Mohgwyn", "lanza", "Lanza sagrada de Mohgwyn", dur=5.0, x=.24, y=.52),
    ficha("Es un instrumento de comunión", "Lanza sagrada de Mohgwyn", "Un instrumento de comunión con un dios exterior que "
          "concede poder a la sangre maldita. *La madre de la verdad desea una herida*.", tipo="Arma", icono="lanza",
          a=("la madre de la verdad desea una herida#2|fin", .8)),
    ficha("meter el brazo dentro del cuerpo", "Favor sanguino · la técnica", "Meter el brazo dentro del cuerpo de la Madre Informe "
          "y esparcir su hemofuego. *Hasta tres veces*.", tipo="Encantamiento", icono="bloodboon", a=("Hasta tres veces|fin", .8)),
    mg(E.cuenta_atras(remate=""), ("Ahí está la cuenta atrás", -.3), ("un anillo rojo se cierra a tu alrededor|fin", .6),
       ["Tres.#7", "Dos.#11", "Uno.#10", "un anillo rojo se cierra"], "cuenta atras"),

    # ---- 1b · Nihil
    mg(E.cuenta_atras(remate="Te arranca la vida a ti, y se la devuelve a él"), ("Nihil. Nada, en latín", -.6),
       ("y se la devuelve a él|fin", 1.0), ["Nihil#4"] * 4 + ["y se la devuelve a él"], "nihil"),
    rel("La Lágrima cristalina purificadora", "lagrima", "Lágrima cristalina purificadora", dur=5.0, x=.76, y=.52),
    ficha("purifica la maldición del terrible ritual", "Lágrima cristalina purificadora", "Purifica la maldición del terrible "
          "ritual de sangre de Mohg. En japonés la llama *la maldición que cuenta*.", tipo="Lágrima", icono="lagrima",
          a=("la maldición que cuenta|fin", .8)),
    mg(E.puesto("No es un ataque", "Es un sacrificio"), ("No es un ataque. Es un sacrificio", -.1),
       ("para la madre de la verdad|fin", .8), [], "sacrificio", y=.80),
    aba([(_G("garras"), "Garras de hemofuego"), (_G("hoja_hemofuego"), "Hoja de hemofuego"), (_G("moscas"), "Enjambre de moscas")],
        ("Ahora piensa en todo lo que usaste", -.2), ("concedido por el Señor de la Sangre|fin", .8),
        ["Garras de hemofuego", "Hoja de hemofuego", "Enjambre de moscas#2"], "hechizos", x=.50, y=.62),
    ficha("Todos dicen lo mismo", "Encantamientos de sangre", "Un encantamiento de *juramento de sangre*, concedido por el Señor "
          "de la Sangre.", tipo="Encantamiento", dur=5.0),
    rel("Y la Gran Runa de Mohg", "runa_mohg", "Gran Runa de Mohg", dur=5.4, x=.24, y=.52),
    ficha("Da una bendición de sangre", "Gran Runa de Mohg", "Da una *bendición de sangre* a los espíritus que invocas, y Grandes "
          "Runas espectrales cuando invades a otro jugador.", tipo="Gran Runa", icono="runa_mohg",
          a=("cuando invades a otro jugador|fin", .8)),
    msg(["La madre de la verdad", "desea una herida. Cada una."], ("Todo el poder de Mohg", -.1), ("Cada una.|fin", 1.0),
        ["Para que haya heridas", "Cada una"], "cada una"),
    mg(E.dinastia(filas=[("Un dios niño", "despertado con sangre"), ("Un rey consorte", "con cuernos")],
                  titulo="El plan de la Dinastía Mohgwyn", remate="Que el mundo sangre"),
       ("Ese era el plan de la Dinastía Mohgwyn", -.2), ("una diosa sin forma que solo quiere que el mundo sangre|fin", 1.0),
       ["Ese era el plan", "Un dios niño", "un rey consorte", "una diosa sin forma", "que el mundo sangre"], "plan"),
    aba([(_G("godrick"), "Un trono"), (_G("ranni"), "Las estrellas"), (_G("radahn"), "Un orden nuevo"),
         (_G("mohg"), "Heridas")],
        ("Sus hermanos querían un trono", -.2), ("a una diosa que se alimenta de heridas|fin", .8),
        ["Sus hermanos querían un trono", "una era de las estrellas", "un orden nuevo", "Mohg, en cambio#2"], "hermanos",
        x=.50, y=.62),
    rel("con la Ríos de Sangre de Okina", "rios", "Ríos de Sangre", dur=4.4, x=.76, y=.52),
    mg(E.puesto("Sin saberlo", "Dedos Sangrientos fieles"), ("Sin saberlo, fuimos los Dedos Sangrientos", -.1),
       ("Sin saberlo, fuimos los Dedos Sangrientos|fin", .4), [], "fieles", y=.80),
    ficha("grita su visión", "Mohg · al morir", "¡Ah, lo veo, tan claro como el día! *¡La llegada de nuestra dinastía!*",
          tipo="Al morir", a=("el nombre de su casa|fin", 3.0)),

    # ---- 1c
    *fila("el Radahn consorte te roba el corazón", [
        ("mohg", "Mohg, al morir", "de rodillas#2"),
        ("radahn", "El consorte", "te roba el corazón")], dur=5.4, tam=360),
    msg(["El lago de sangre", "lo llenó él."], ("Estaba encantado hasta el último segundo", -.1), ("lo llenó él|fin", 1.2),
        ["Pero el lago de sangre", "lo llenó él"], "lago"),

    # ================================================================ CIERRE
    aba([(_G("dedo_infestado"), "Caza a los tuyos"), (_G("pano_rojo"), "Una doncella"), (_G("mascara_blanca"), "Los que curaban"),
         (_P("mohg_miquella"), "Un dios dormido"), (_G("dios_exterior"), "La madre de la verdad")],
        ("Esa es la lista", -.2), ("a una diosa que desea heridas|fin", .8),
        ["Te recluta desde el primer paso", "te pide la sangre de una doncella#2", "rapta a los que curaban",
         "roba un dios dormido#2", "y le ofrece el mundo entero"], "lista", x=.50, y=.62, tam=270),
    rel("Su Gran Runa lo dice", "runa_mohg", "Gran Runa de Mohg", dur=4.6, x=.24, y=.52),
    ficha("amaba el lodazal en el que nació", "Gran Runa de Mohg", "*Amaba el lodazal* en el que nació.", tipo="Gran Runa",
          icono="runa_mohg", a=("tanta sangre ajena|fin", .6)),
    com("José Luis nos contó", C_JOSE, dur=6.5),
    com("David ya lleva unos siete videos", C_DAVID, dur=4.6, x=.30, y=.30),
    com("Y Eternalack lo resumió", C_ETERNAL, dur=4.4, x=.70, y=.36),
    com("Y Escuadrón preguntó", C_ESCUADRON, dur=6.0),
    mg(E.puesto("Atrocidad n.º 1 de Torrentera", "Te deja tirado en la mazmorra"), ("Por ahora solo tenemos una", -.1),
       ("te deja tirado en cuanto entras a una mazmorra|fin", 1.0), [], "torrentera", y=.80),
    aba([(_P("rykard"), "Rykard"), (_G("godwyn"), "Godwyn"), (_P("maliketh"), "Maliketh")],
        ("Por eso ya están apuntados Rykard", -.2), ("y Maliketh, que pide Justin|fin", .8),
        ["Rykard", "Godwyn", "Maliketh"], "apuntados", x=.50, y=.62),
    msg(["¿Villano de verdad,", "o el primer encantado de Miquella?"], ("Ahora te toca a ti", -.1),
        ("el primer encantado de Miquella|fin", 1.0), ["un villano de verdad", "el primer encantado"], "pregunta"),
    cam("Y Zohary, espero que tu patrón", "mohg_icono", "Para Zohary", dur=3.8, x=.80, y=.66),
    aba([(_G("marika"), "Márika y Radagon"), (_G("miquella"), "Miquella"), (_G("malenia"), "Malenia"), (_G("ranni"), "Ranni"),
         (_G("melina"), "Melina"), (_G("radahn"), "Radahn"), (_G("morgott_icono"), "Morgott")],
        ("en el canal tienes las atrocidades de Márika", -.2), ("y Morgott, su gemelo|fin", .8),
        ["de Márika y Radagon", "de Miquella#6", "Malenia#2", "Ranni", "Melina", "Radahn#4", "y Morgott#2"], "en el canal",
        x=.50, y=.62, tam=260),
    mg(E.puesto("Suscríbete", "Rumbo a los 1 000"), ("Y si te suscribes", -.1), ("nos acercas a los mil|fin", .8), [],
       "suscribete", y=.80),
    rel("la próxima vez que un Dedo Sangriento te invada", "dedo_infestado", "Dedo Sangriento", dur=4.4, x=.24, y=.52),
    grande("Para la madre de la verdad#2", "mohg", "Mohg, Señor de la Sangre", lado="der", dur=4.6, tam=600),
]
