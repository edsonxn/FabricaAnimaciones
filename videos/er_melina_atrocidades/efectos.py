# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Melina QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 27-oct-2026).
Fórmula de Miquella/Malenia (docs/estilo_secuencia_yt.md § PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS REALES CON RUTA) con el
kit de Elden Ring (nucleo/mg_er.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de eldenring.fandom.com en pegatinas/, bajar_pegatinas.py),
  chicas abajo a la izquierda, en fila cuando la voz enumera, y algunas GRANDES (media pantalla).
- PANTALLAS a cuadro entero (pantallas/) donde el clip no enseña lo que hace falta ver (la Forja, el árbol en llamas, el ojo).
- fichas de descripción SOLO con citas verificadas (docstring de guion.py), arriba a la derecha; rótulo de puesto por atrocidad.
- MG NUEVOS de este guion: `acuerdo` (el trato; vuelve en el n.º 1 con la letra pequeña en rojo y el sello «Deber»), `ecos`
  (las palabras de «una desconocida» que resulta ser su madre), `arbol_arde` (de la llama al pie a la capital de ceniza) y
  `muerte_suelta` (la Runa de la Muerte presa en eslabones que saltan; «indiscriminada» tacha a todos).
- MAPAS: el viaje del acuerdo (Necrolimbo → Leyndell) y el de la llama (Leyndell → Forja de los gigantes), a pantalla; dónde
  está la Hoja de la invocación (ventana, Tierras Prohibidas).
  python fab.py er_melina_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_melina_atrocidades fx         audio/fx.wav
"""
import os

import mg_er as E
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .74, .30     # fichas: arriba a la derecha
TEMA_MAPA = "er"

CAMARA = {   # planos casi quietos (Melina sentada en la gracia): acercamiento lento en vez de rehacer
    **{f"scene-{n:03d}": dict(a=(1.0, 0, 0), b=(1.16, 0, -.05)) for n in (69, 77)},
}
FUNDIDO = {}


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_PEG, slug + ".png"), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=680):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=.50, tam=tam)


def fila(en, items, y=.64, tam=340, dur=4.6):
    """Varias pegatinas en fila; items = [(slug, titulo, ancla o None = la misma)]."""
    xs = (.12, .29, .46, .63, .80)
    return [peg(a or en, s, t, dur=dur, x=xs[i], y=y, tam=tam) for i, (s, t, a) in enumerate(items)]


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0):
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(os.path.join(_PAN, slug + ".jpg"), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=os.path.join(_PEG, icono + ".png") if icono else None),
             en=en, x=_FX, y=_FY, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


def mg(fn, de, a, marcas, nombre, y=.50):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + slug, ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + slug, ver=4.0)


_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")
REGALOS = ["Tus runas, en poder", "Torrentera", "La Mesa Redonda"]
LLEVAR = "Llevarla al pie del Árbol Áureo"
ETAPAS = ["La llama de los gigantes", "La yesca: Melina", "El Árbol Áureo arde", "Leyndell, capital de ceniza"]
TODOS = ["Los semidioses", "Los dioses", "Los Sinluz", "Tú"]

FX = [
    # ================================================================ GANCHO
    peg("Te da el caballo", "torrentera", "Torrentera", tam=420),
    peg("te sube de nivel", "melina_wiki", "Melina", tam=360, x=.80, y=.62),
    peg("te lleva a la Mesa Redonda", "mesa_redonda", "La Mesa Redonda", tam=440),
    grande("Melina. La chica de la capucha", "melina", "Melina", lado="der", dur=5.6, tam=640),
    pant("melina_capa", ("Bueno. Casi nada raro", -.2), ("Casi nada raro|fin", .6), zoom=(1.0, 1.12)),
    pant("forja1", ("Porque el día que por fin te dice lo que quiere", -.2), ("para cometer un pecado capital|fin", .4),
         zoom=(1.0, 1.12), pan=(0, 0, 0, -.05)),
    ficha("te lo pregunta así", "Melina, en la Forja", "¿Estás preparado para cometer *un pecado capital*?",
          tipo="Lo que te pregunta", a=("para cometer un pecado capital|fin", .8)),
    ficha("Lo dice ella misma", "Melina", "Lo sé. *Te estoy pidiendo que cometas un pecado capital*.", tipo="Lo que te dice",
          a=("sé que te estoy pidiendo que cometas un pecado capital|fin", .8)),
    peg("En el video de Ranni", "ranni", "Ranni", tam=380),
    peg("Hoy toca la otra favorita", "melina_media", "Melina", tam=420, x=.80, y=.60),
    puesto("Así que van las cinco peores atrocidades de Melina", "Las 5 peores atrocidades de", "Melina", dur=4.2),
    peg("la número uno es una amenaza", "hoja_invocacion", "Hoja de la invocación", tam=400),
    peg("fíjate bien en lo que te dice mientras te toca el hombro", "melina_capucha", "La mano en el hombro", tam=440),

    # ================================================================ 5 · TE ELIGIÓ PORQUE NO TENÍAS A NADIE
    puesto("Número cinco. Te eligió porque no tenías a nadie", "Atrocidad número 5", "Te eligió por estar solo"),
    peg("Cuando despiertas en el cementerio del principio", "cementerio", "El cementerio del principio", tam=460),
    peg("montada en Torrentera", "torrentera", "Torrentera", tam=400, x=.80, y=.62),
    ficha("Tranquilo, Torrentera, la suerte está de su lado", "Melina, en el cementerio",
          "Tranquilo, Torrentera, la suerte está de su lado. Lo encontramos aquí, después de todo. *Alguien de su clase seguro "
          "que buscará el Círculo de Elden*.", tipo="Lo que dice de ti", a=("seguro que buscará el Círculo de Elden|fin", .6)),
    ficha("Y entonces añade, en voz bajita", "Melina, en el cementerio", "*Aunque vaya en contra del Orden Áureo*.",
          tipo="Lo que añade", a=("Y que le conviene|fin", .4)),
    peg("aunque vaya en contra del Orden Áureo", "orden_aureo", "El Orden Áureo", tam=380),
    peg("las doncellas del Dedo, las que guían a los Sinluz", "hyetta", "Una doncella del Dedo", tam=400),
    ficha("pero a ti, me temo, no te acompaña ninguna", "Melina",
          "¿Has oído hablar de las doncellas del Dedo? Sirven a los Dos Dedos y guían a los Sinluz. *Pero a ti, me temo, no te "
          "acompaña ninguna*.", tipo="El acuerdo", a=("Por eso viene|fin", .4)),
    mg(E.acuerdo(REGALOS[:1], LLEVAR, titulo="El acuerdo"), ("Yo puedo hacer el papel de doncella", -.2),
       ("Ella pone el viaje gratis hasta su casa|fin", .8), ["Convertiré tus runas en poder", "Solo tienes que llevarme contigo"],
       "acuerdo 1"),
    peg("te regala un anillo con un silbato", "silbato", "Silbato de corcel espectral", tam=420),
    ficha("Torrentera te ha elegido, te dice", "Silbato de corcel espectral",
          "Invoca a un corcel espectral llamado Torrentera. *Torrentera te ha elegido. Trátalo con respeto*.",
          tipo="Lo que te dice", icono="silbato", a=("Trátalo con respeto|fin", .8)),
    grande("Al caballo le pide respeto para él", "torrentera", "Torrentera", lado="izq", dur=4.0, tam=600),
    peg("Tú ya estás contratado", "melina_media", "Melina", tam=400, x=.80, y=.60),

    # ---- 5b · solo fingía
    pant("melina_revela", ("Melina te espera en un lugar de gracia y te pide perdón", -.2), ("y te pide perdón|fin", .8),
         zoom=(1.0, 1.10), pan=(0, 0, .06, 0)),
    ficha("Perdóname. Te he estado poniendo a prueba", "Melina",
          "Perdóname. *Te he estado poniendo a prueba*. Para ver si la gracia de verdad te guía, y si eres apto para el desafío.",
          tipo="Lo que te confiesa", a=("el desafío que eso supone|fin", .4)),
    ficha("y remata con la frase más sincera", "Melina", "Torrentera te tomó la medida desde el principio. *Yo, en cambio, "
          "solo fingía*.", tipo="Lo que te confiesa", a=("Yo, en cambio, solo fingía|fin", 1.2)),
    peg("Y el que te aprobó fue el caballo", "torrentera", "Torrentera, el examinador", tam=420),
    mg(E.mensaje(["Deja que pose mi mano sobre ti.", "Compártelos conmigo:", "tus pensamientos, tus ambiciones."]),
       ("deja que pose mi mano sobre ti, solo un momento", -.2), ("Los principios que seguirías|fin", 1.0),
       ["deja que pose mi mano sobre ti", "compártelos conmigo", "Tus pensamientos. Tus ambiciones"], "mano", y=.76),
    peg("Ochenta, cien, ciento cincuenta veces", "melina_capucha", "Cada nivel, su mano", tam=420),
    ficha("Lo admite: te he servido", "Melina", "Te he servido como doncella del Dedo, pero no puedo ofrecerte guía. *No soy "
          "ninguna doncella*. Mi propósito se perdió hace mucho.", tipo="Lo que admite", a=("Mi propósito se perdió hace mucho|fin", .5)),
    mapa("mundo", [(.395, .735, "Necrolimbo", "inicio", _G("cementerio")), (.36, .715), (.33, .69), (.30, .64), (.27, .57),
                   (.25, .50), (.28, .43), (.33, .37), (.39, .35), (.44, .37), (.48, .40, "Leyndell", "meta", _P("capital"))],
         ("Y en cuanto llegas a la capital", -.3), ("el acuerdo queda cumplido|fin", 1.2),
         ["Y en cuanto llegas a la capital", "lo dice sin rodeos"], titulo="Las Tierras Intermedias", sub="El viaje del acuerdo",
         traza=99),
    peg("Te dejo a Torrentera y el poder de las runas", "torrentera", "Torrentera", tam=380),
    peg("como quien se baja de un taxi", "melina_media", "Melina, se va", tam=400, x=.80, y=.60),
    ficha("Y entonces te saluda así", "Melina", "*Hola de nuevo, viejo amigo*.", tipo="Cuando vuelve", a=("hola de nuevo, viejo amigo|fin", 1.0)),

    # ================================================================ 4 · LA HIJA QUE NO TE DIJO DE QUIÉN ERA HIJA
    puesto("Número cuatro. La hija que no te dijo", "Atrocidad número 4", "La hija secreta"),
    ficha("Te dice que busca el propósito que le dio su madre", "Melina", "Busco mi propósito, el que me dio *mi madre*, dentro "
          "del Árbol Áureo, hace mucho. Nací al pie del Árbol Áureo, *donde mi madre me dio ese propósito*.",
          tipo="Lo que cuenta de sí misma", a=("donde su madre le dio ese propósito|fin", .6)),
    pant("arbol", ("Lo que nunca te dice es cómo se llama su madre", -.2), ("Ni una vez en todo el juego|fin", .4), zoom=(1.0, 1.10)),
    ficha("el nombre interno de Melina es", "Archivos del juego", "Nombre interno del personaje: *MaricaOfDaughter*. Hija de Márika.",
          tipo="Lo que esconde el juego", a=("hija de Márika|fin", 1.2)),
    peg("el nombre interno de Melina es, literalmente, hija de Márika", "marika", "Márika", tam=400),
    grande("Cuando matas a Mésmer el Empalador", "messmer_jefe", "Mésmer el Empalador", lado="izq", dur=4.4, tam=620),
    ficha("te llevas su yesca, y su descripción dice", "Yesca de Messmer",
          "La yesca que ardía dentro de Mésmer el Empalador. *Mésmer, al igual que su hermana menor, tenía una visión del fuego*.",
          tipo="Objeto clave", icono="yesca_messmer", a=("tenía una visión del fuego|fin", 1.0)),
    *fila("O sea que la chica de la capucha es hija de la reina Márika", [
        ("marika", "Márika, su madre", None),
        ("messmer", "Mésmer, su hermano", "y hermana pequeña de Mésmer"),
        ("melina", "Melina", "y hermana pequeña de Mésmer")], dur=5.0),
    peg("Melina se ofrece a contarte los ecos de la reina Márika", "tercera_iglesia", "Iglesias de Márika", tam=440),
    mg(E.ecos(["Os despojo a cada uno de vuestra gracia.", "Con los ojos apagados, seréis expulsados de las Tierras Intermedias.",
               "Haréis la guerra en una tierra lejana, donde viviréis y moriréis."], titulo="Eco de Márika · Tercera Iglesia"),
       ("Os despojo a cada uno de vuestra gracia", -.3), ("la que te desterró es su madre|fin", .8),
       ["Os despojo a cada uno de vuestra gracia", "Con los ojos apagados", "Haréis la guerra en una tierra lejana",
        "Sin decirte que la que te desterró es su madre"], "ecos 1"),

    # ---- 4b · las madres de los demás y el fuego de la familia
    mg(E.ecos(["Escuchadme, semidioses, mis hijos amados.", "Si no llegáis a ser nada en absoluto, seréis abandonados.",
               "Y no seréis más que sacrificios."], titulo="Eco de Márika · a las afueras de la capital", firma="Márika",
              revela="de ella"),
       ("escuchadme, semidioses, mis hijos amados", -.3), ("Y te lo lee sin que le tiemble la voz|fin", .6),
       ["escuchadme, semidioses, mis hijos amados", "Pero si no llegáis a ser nada", "Y no seréis más que sacrificios",
        "De ella. Hijo que no sirve"], "ecos 2"),
    grande("Cuando le preguntas por Boc, el costurero", "boc", "Boc, el costurero", lado="izq", dur=5.0, tam=560),
    ficha("Cuando le preguntas por Boc", "Melina", "A veces lo veo llorar. Creo que echa de menos a su madre. *¿Nacer de una "
          "madre significa comportarse así?*", tipo="Lo que dice de Boc", a=("significa comportarse así|fin", 1.0)),
    peg("A los dos su madre les dio un propósito", "messmer_jefe", "Mésmer", tam=420),
    ficha("El de Mésmer lo dice él mismo", "Mésmer el Empalador", "Mi propósito sigue siendo el mismo: *todos los despojados de "
          "la gracia del oro hallarán la muerte*, en el abrazo de la llama de Mésmer.", tipo="Lo que dice",
          a=("en el abrazo de la llama de Mésmer|fin", .8)),
    ficha("Y su orbe cuenta que Mésmer despreciaba", "Orbe de Mésmer", "Mésmer despreciaba su propio fuego. *Una y otra vez quiso "
          "librarse de él, pero siempre ardía*.", tipo="Encantamiento", a=("pero siempre ardía|fin", .8)),
    *fila("La hermana pequeña tenía la misma visión", [
        ("yesca_messmer", "La visión de Mésmer", None),
        ("mariposa", "La visión de Melina", "La diferencia es que ella no la desprecia")], dur=5.4),
    peg("Si invocas a Melina contra Morgott", "morgott", "Morgott, rey de los Augurios", tam=420),
    pant("invocada", ("ella lanza un encantamiento secreto de la reina Márika", -.3), ("que cura a los aliados|fin", .4),
         zoom=(1.0, 1.10)),
    ficha("Su descripción dice: solo la bondad del oro", "Árbol Áureo menor",
          "Encantamiento secreto de la reina Márika. *Solo la bondad del oro, sin el Orden*. Márika bañó en oro la aldea de su "
          "hogar, *sabiendo perfectamente que no quedaba nadie a quien curar*.", tipo="Encantamiento", icono="arbol_menor",
          a=("curar cuando ya no queda nadie|fin", .6)),
    peg("Márika bañó en oro la aldea de su hogar", "aldea_chamanes", "La aldea de Márika", tam=440, x=.17, y=.66),

    # ================================================================ 3 · EL PECADO CAPITAL
    puesto("Número tres. El pecado capital", "Atrocidad número 3", "El pecado capital"),
    peg("Cuando por fin matas a Morgott", "morgott", "Morgott", tam=400),
    pant("espinas", ("Un muro de espinas cierra el paso", -.2), ("Y entonces reaparece Melina|fin", .4), zoom=(1.0, 1.12)),
    ficha("No pudiste entrar en el Árbol Áureo", "Melina", "No pudiste entrar en el Árbol Áureo, ¿verdad? Las espinas son "
          "impenetrables. *La única forma de convertirte en Señor del Círculo es atravesarlas*.", tipo="Lo que te dice",
          a=("es atravesarlas|fin", .4)),
    peg("muy por encima de las nubes, en los picos nevados de los gigantes", "picos_gigantes", "Los Picos de los gigantes",
        tam=520, y=.66),
    ficha("Así podré prenderle fuego al Árbol Áureo", "Melina", "Quiero que emprendas un nuevo viaje conmigo, hasta la llama de la "
          "perdición. *Así podré prenderle fuego al Árbol Áureo*.", tipo="Lo que te pide",
          a=("Así podré prenderle fuego al Árbol Áureo|fin", 1.0)),
    pant("arbol", ("El árbol que gobierna la vida de todo el mundo", -.2), ("El árbol a cuyo pie ella misma nació|fin", .4),
         zoom=(1.12, 1.0)),
    peg("Un encantamiento lo explica", "llama_surge", "¡Surge, oh llama!", tam=380),
    ficha("Un encantamiento lo explica", "¡Surge, oh llama!", "La llama de los gigantes es la llama de la perdición, *capaz de "
          "quemar el Árbol Áureo*. Por eso, tras la guerra contra los gigantes, su fuego fue sellado y vigilado.",
          tipo="Encantamiento", icono="llama_surge", a=("su fuego fue sellado y vigilado|fin", .6)),
    mg(E.ecos(["Pasad a los gigantes por la espada, y confinad la llama en lo alto del monte.",
               "Que empiece una nueva época, una época resplandeciente de vida."], titulo="Eco de Márika · Primera Iglesia",
              firma="Márika", revela="y su hija la enciende"),
       ("pasad a los gigantes por la espada", -.3), ("a encenderlo otra vez|fin", .8),
       ["pasad a los gigantes por la espada", "Que empiece una nueva época", "Y la hija te lleva de la mano"], "ecos 3"),
    peg("te lo explica Enia, la lectora de dedos", "enia", "Enia, lectora de dedos", tam=420),
    ficha("para que la llama queme el Árbol Áureo, se necesita un sacrificio", "Enia, lectora de dedos",
          "Para que la llama queme el Árbol Áureo, se necesita un sacrificio. *El de alguien que tenga una visión de la llama*, y "
          "que pueda guiarte hasta la Runa de la Muerte.", tipo="Lo que dice", a=("hasta la Runa de la Muerte|fin", .5)),
    peg("Ya sabes quién es", "mariposa", "Una visión de la llama", tam=380, x=.80, y=.62),
    ficha("no te preocupes por la yesca", "Melina", "*No te preocupes por la yesca. Yo me encargo de eso*.", tipo="Lo que te dice",
          a=("Yo me encargo de eso|fin", .8)),
    ficha("y luego te pide perdón por adelantado", "Melina", "Lo sé. Te estoy pidiendo que cometas un pecado capital. *Pero debe "
          "hacerse para llegar al camino de más allá*.", tipo="Lo que te dice", a=("el camino que yo quiero recorrer|fin", .5)),

    # ---- 3b · la Forja y la capital de ceniza
    ficha("Mi propósito me lo dio mi madre. Pero ahora", "Melina, en el valle nevado", "Mi propósito me lo dio mi madre. Pero ahora "
          "actúo por voluntad propia. *Sin importar los designios de mi madre*.", tipo="Lo que te dice",
          a=("sin importar los designios de mi madre|fin", .6)),
    mg(E.mensaje(["No permitiré que nadie hable mal de eso.", "Ni siquiera tú."]), ("no permitiré que nadie hable mal", -.2),
       ("tu opinión no entra en el acuerdo|fin", .6), ["no permitiré que nadie hable mal", "Ni siquiera tú"], "ni siquiera tú", y=.76),
    pant("forja1", ("Cuando por fin llegas a la Forja de los gigantes", -.2), ("¿Estás preparado para cometer un pecado capital?#2|fin", .3),
         zoom=(1.0, 1.10)),
    ficha("He observado las Tierras Intermedias", "Melina, en la Forja", "He observado las Tierras Intermedias durante mucho tiempo. "
          "Este mundo necesita ser reparado. *Y la muerte, indiscriminada*.", tipo="Lo que te dice",
          a=("¿Estás preparado para cometer un pecado capital?#2|fin", .5)),
    pant("forja2", ("Y entonces te toma de la mano", -.2), ("Ni siquiera te deja verlo|fin", .4), zoom=(1.0, 1.12), pan=(0, 0, .08, 0)),
    pant("forja3", ("Mientras duermes, ella se convierte en la yesca", -.2), ("Gracias por traerme hasta aquí|fin", .2),
         zoom=(1.0, 1.10)),
    mg(E.arbol_arde(ETAPAS), ("Oh, Árbol Áureo, arderás", -.3), ("Otra vez sin doncella|fin", .6),
       ["Oh, Árbol Áureo, arderás", "Arde por el nuevo señor", "Gracias por traerme hasta aquí", "Y despiertas en Farum Azula"],
       "árbol arde 1"),
    pant("forja4", ("Quien camina junto a la llama algún día", -.2), ("Quien camina junto a la llama algún día se encontrará con el camino de la muerte destinada|fin", .8),
         zoom=(1.0, 1.10)),
    peg("Y despiertas en Farum Azula", "farum_azula", "Farum Azula, la ciudad en ruinas", tam=460),
    pant("capital_ceniza", ("Leyndell, la capital de ceniza", -.2), ("solo asoman los edificios más altos|fin", .5),
         zoom=(1.0, 1.12), pan=(0, 0, 0, .05)),
    ficha("Enia lo resume sin dramatismo", "Enia, lectora de dedos", "La Runa de la Muerte ha sido liberada, y las Tierras "
          "Intermedias están cubiertas *por el oscuro destino de la Muerte*.", tipo="Lo que dice",
          a=("cubiertas por el oscuro destino de la Muerte|fin", .6)),
    mg(E.arbol_arde(ETAPAS, titulo="Lo que quemó"), ("Melina quemó el árbol de su madre", -.3), ("es la número tres|fin", .6),
       [("Melina quemó el árbol de su madre", -2.0), ("Melina quemó el árbol de su madre", -1.5), ("Melina quemó el árbol de su madre", -1.0),
        "enterró su ciudad natal en ceniza"], "árbol arde 2"),

    # ================================================================ 2 · MUERTE PARA TODOS
    puesto("Número dos. Muerte para todos", "Atrocidad número 2", "Muerte para todos"),
    mg(E.mensaje(["Este mundo necesita ser reparado.", "Y la muerte, indiscriminada."]),
       ("este mundo necesita ser reparado. Y la muerte, indiscriminada#2", -.2), ("Eso es lo que Melina quiere devolverle al mundo|fin", .4),
       ["este mundo necesita ser reparado. Y la muerte, indiscriminada#2", "Y la muerte, indiscriminada#2"], "indiscriminada", y=.76),
    peg("hay que saber qué es la Runa de la Muerte", "runa_muerte", "Runa de la Muerte", tam=420),
    ficha("Enia lo cuenta así: la Runa de la Muerte tiene dos nombres", "Enia, lectora de dedos",
          "La Runa de la Muerte tiene dos nombres. El otro es *muerte destinada*. La sombra prohibida, *arrancada del Orden Áureo "
          "en su creación*.", tipo="Lo que dice", a=("arrancada del Orden Áureo en su creación|fin", .8)),
    mg(E.muerte_suelta(TODOS), ("Melina no quiere un fragmento", -1.2), ("alguien tiene que matar a Maliketh|fin", .8),
       [("Melina no quiere un fragmento", -.6), "Quiere la runa entera", "para todo el mundo"], "muerte suelta 1"),
    peg("Y se la dio a guardar a Maliketh", "maliketh_jefe", "Maliketh, la Hoja Negra", tam=440, x=.80, y=.62),
    peg("En el video de Ranni vimos lo que pasó", "godwyn", "Godwyn", tam=380),
    peg("el semidiós más querido del mundo murió", "cuchillo_negro", "Un fragmento de muerte", tam=360, x=.80, y=.62),
    grande("Adivina quién", "maliketh_jefe", "Maliketh, la Hoja Negra", lado="izq", dur=5.4, tam=620),
    peg("El que tiene que recorrerla", "farum_azula", "Farum Azula", tam=420, x=.80, y=.60),
    *fila("Con Godrick, con Morgott", [
        ("godrick", "Godrick", None),
        ("morgott", "Morgott", "con Morgott"),
        ("maliketh", "Maliketh", "y ahora con el guardián de la muerte")], dur=5.2),
    peg("La sombra que guarda esa espada", "espada_maliketh", "La Hoja Negra", tam=420),

    # ---- 2b · la Hoja de la invocación
    mapa("mundo", [(.54, .37, "Tierras Prohibidas", "meta", _G("hoja_invocacion"))],
         ("Es una daga que puedes encontrar escondida", -.2), ("y se llama la Hoja de la invocación|fin", .8),
         ["Es una daga que puedes encontrar escondida"], titulo="¿Dónde está?", ventana=True),
    pant("cuarto_secreto", ("Su descripción dice: daga entregada", -.3), ("la doncella enyescada, aún se nota|fin", .5),
         zoom=(1.0, 1.10)),
    ficha("Su descripción dice: daga entregada", "Hoja de la invocación", "Daga entregada a quien partió hace mucho para cumplir con "
          "su deber. *El poder de su antigua dueña, la doncella enyescada, aún se nota*.", tipo="Daga", icono="hoja_invocacion",
          a=("la doncella enyescada, aún se nota|fin", .8)),
    mg(E.mensaje(["Quien camina junto a la llama", "algún día se encontrará", "con el camino de la muerte destinada."]),
       ("Y debajo, otra vez, la misma frase", -.1), ("el camino de la muerte destinada#2|fin", .8),
       ["Quien camina junto a la llama#2", "algún día se encontrará#2", "con el camino de la muerte destinada#2"], "frase daga", y=.76),
    grande("No buscaba un compañero", "melina", "Melina", lado="der", dur=5.0, tam=600),
    peg("La misma hoja la lleva Poliána", "valquirias", "Las hermanas de Millicent", tam=460),
    peg("Si viste el video de Malenia", "millicent", "Millicent", tam=380, x=.80, y=.60),
    peg("Ahora, para ser justos", "melina_wiki", "Melina", tam=360),
    ficha("te suplica: la vida perdura", "Melina", "*La vida perdura. Los nacimientos continúan*. ¿No hay belleza en eso?",
          tipo="Lo que te suplica", a=("¿No hay belleza en eso?|fin", .8)),
    mg(E.muerte_suelta(TODOS, titulo="Que todo nazca, y que todo muera"), ("Que todo nazca, y que todo muera", -.3),
       ("Pero es un mundo que decide ella|fin", .6),
       [("Que todo nazca, y que todo muera", -2.0), ("Que todo nazca, y que todo muera", -1.0), "Y que nadie se libre"],
       "muerte suelta 2"),
    peg("deja de ser tu compañera", "olla_frenetica", "La llama frenética", tam=380),

    # ================================================================ 1 · LA PROMESA DE MATARTE
    puesto("Número uno. La promesa de matarte", "Atrocidad número 1", "La promesa de matarte"),
    pant("tres_dedos", ("hay una puerta sellada que lleva a los Tres Dedos", -.2), ("la que lo quema todo|fin", .4), zoom=(1.0, 1.12)),
    ficha("Si pretendes reclamar esa llama", "Melina", "Si pretendes reclamar la llama frenética, te pido que desistas. "
          "*Es el caos, que devora la vida y el pensamiento sin fin*.", tipo="Lo que te pide", a=("deja en paz la llama frenética|fin", .5)),
    ficha("yo me encargo de la yesca. Es un propósito", "Melina", "Yo me encargo de la yesca. *Es un propósito que elijo cumplir*.",
          tipo="Lo que se le escapa", a=("antes que dejarte esa llama a ti|fin", .4)),
    peg("te arrodillas ante los Tres Dedos y aceptas la llama", "llama_frenetica", "La llama frenética", tam=420),
    pant("melina_capa", ("Melina aparece por última vez", -.2), ("Nuestro acuerdo termina aquí|fin", .5), zoom=(1.0, 1.12)),
    ficha("Has heredado la llama frenética", "Melina", "Has heredado la llama frenética. Qué lástima. *Ya no eres digno*. Nuestro "
          "acuerdo termina aquí.", tipo="Lo que te dice", a=("Nuestro acuerdo termina aquí|fin", .8)),
    mg(E.mensaje(["Si te alzas como Señor del Caos,", "te mataré."]), ("Si te alzas como Señor del Caos", -.2),
       ("como que la noche sigue al día|fin", .6), ["Si te alzas como Señor del Caos", "te mataré"], "te mataré", y=.76),
    mg(E.acuerdo(REGALOS, LLEVAR, letra="Si te alzas como Señor del Caos, te mataré. Ese es mi deber, por haberte concedido el poder "
                 "de las runas.", titulo="La letra pequeña del acuerdo"),
       ("y la frase siguiente es la que lo cambia todo", -.3), ("te lo cobraba con tu vida|fin", .8),
       [("y la frase siguiente es la que lo cambia todo", 0), ("y la frase siguiente es la que lo cambia todo", .4),
        ("y la frase siguiente es la que lo cambia todo", .8), ("y la frase siguiente es la que lo cambia todo", 1.2),
        "ese es mi deber, por haberte concedido", "Era un préstamo"], "acuerdo 2"),
    *fila("Adiós, mi compañero", [
        ("melina_media", "Melina", None),
        ("torrentera", "Torrentera", "Adiós, Torrentera")], dur=4.2),

    # ---- 1b · la escena tras los créditos
    pant("frenesi1", ("Todo es ceniza", -.2), ("ha ardido con todo lo demás|fin", .4), zoom=(1.0, 1.10)),
    peg("el anillo del silbato", "silbato", "Silbato de corcel espectral", tam=400),
    pant("melina_render6", ("Y por primera vez abre el ojo izquierdo", -.2), ("con un sello encima|fin", .4), zoom=(1.0, 1.14)),
    pant("frenesi_final", ("Y es de color violeta", -.2), ("La muerte destinada#3|fin", .8), zoom=(1.0, 1.12), pan=(0, -.05, 0, -.1)),
    ficha("Y te dice: Señor de la Llama Frenética", "Melina", "Señor de la Llama Frenética. Te buscaré, tan lejos como viajes. "
          "*Para darte lo que es tuyo. La muerte destinada*.", tipo="Lo que te promete", a=("La muerte destinada#3|fin", 1.0)),
    mg(E.mensaje(["Quien camina junto a la llama", "algún día se encontrará", "con el camino de la muerte destinada."]),
       ("Ahora vuelve a la frase de su daga", -.1), ("Y la muerte que te espera, es Melina|fin", .8),
       ["Quien camina junto a la llama#3", "En el final normal", "En este final, el que camina con la llama eres tú"],
       "frase daga 2", y=.76),
    grande("la Reina del Ojo Velado", "reina_ojo", "Los apóstoles de la Reina del Ojo Velado", lado="izq", dur=5.6, tam=600),
    peg("hasta que Maliketh la derrotó", "maliketh_jefe", "Maliketh", tam=380, x=.80, y=.62),
    peg("Y tenía un ojo especial", "ojo_sello", "El ojo sellado de Melina", tam=420, x=.80, y=.40),
    *fila("una hija de Márika con un ojo sellado", [
        ("marika", "Hija de Márika", None),
        ("ojo_sello", "Un ojo sellado", "con un ojo sellado"),
        ("runa_muerte", "La muerte destinada", "que acaba con el poder")], dur=5.4),
    grande("guardaba debajo de la capucha la cara de la muerte", "melina", "Melina", lado="der", dur=5.0, tam=620),
    peg("Es para ti. Y es una promesa", "hoja_invocacion", "La promesa", tam=420),

    # ================================================================ CIERRE
    *fila("La compañera perfecta te eligió", [
        ("cementerio", "Te eligió sola", None),
        ("tercera_iglesia", "Te ocultó a su madre", "te ocultó de quién era hija"),
        ("forja", "Quemó el árbol", "quemó el árbol de su madre#2"),
        ("runa_muerte", "Soltó la muerte", "le devolvió la muerte"),
        ("hoja_invocacion", "Te prometió matarte", "y te prometió matarte")], tam=300, dur=7.0),
    peg("Melina es la única que nunca te mintió", "melina_wiki", "Melina", tam=380),
    *fila("quién fue peor de las dos favoritas", [
        ("ranni", "Ranni", None),
        ("melina", "Melina", "o Melina, que te usó")], dur=6.0),
    puesto("en el canal tienes las atrocidades de Márika", "Ya en el canal",
           "Toda la familia", dur=5.4),
    peg("Sobre todo para quemar cosas", "yesca_messmer", "Cosas de familia", tam=380),
    peg("Y qué piensa quemar al llegar", "melina_fuego", "Melina", tam=440, x=.80, y=.60),
]
ROTULOS = []
SFX = {   # uno distinto por momento y distintos de Miquella/Ranni/Malenia (regla: nada de SFX repetidos ante el canal)
    "silbido": ("A soft ghostly whistle echoing in an empty misty graveyard, dark fantasy, eerie and gentle", 3),
    "mano": ("A gentle hand resting on a cloth shoulder with a faint warm golden shimmer, intimate and quiet", 2),
    "sello_deber": ("A heavy wax seal stamped hard onto thick parchment, deep thud, a cracking wax snap", 2),
    "ignicion": ("A colossal ancient flame igniting with a deep roar and rushing wind, a giant tree catching fire, dark fantasy", 5),
    "cadenas": ("Heavy golden chains snapping and shattering link by link, metallic and ominous", 3),
    "coro": ("A choir of faint whistles in the wind over ashes, haunting and sad, dark fantasy", 4),
}
PISTAS = [
    dict(sfx="silbido", en="te regala un anillo con un silbato", vol=.4),
    dict(sfx="mano", en="deja que pose mi mano sobre ti, solo un momento", vol=.4),
    dict(sfx="ignicion", en="Oh, Árbol Áureo, arderás", vol=.5),
    dict(sfx="cadenas", en="Quiere la runa entera", vol=.45),
    dict(sfx="sello_deber", en="Era un préstamo", vol=.5),
    dict(sfx="coro", en="Se oye un coro de silbidos", vol=.4),
]
