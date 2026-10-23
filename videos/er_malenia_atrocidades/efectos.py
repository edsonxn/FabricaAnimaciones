# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Malenia QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 23-oct-2026).
Fórmula de Miquella (docs/estilo_secuencia_yt.md § PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS REALES CON RUTA) con el kit de
Elden Ring (nucleo/mg_er.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de eldenring.fandom.com en pegatinas/), chicas abajo a la
  izquierda, en fila cuando la voz enumera, y algunas GRANDES (media pantalla).
- PANTALLAS a cuadro entero (pantallas/) donde el clip no enseña lo que hace falta ver.
- fichas de descripción SOLO con citas verificadas (docstring de guion.py), arriba a la derecha; rótulo de puesto por atrocidad.
- MG NUEVOS de este guion: `juramento` (el contrato de los caballeros, firmas que se pudren), `contagio` (lo que pudrió una flor,
  dos veces), `repudio` (Malenia y sus hijas; los hilos se parten con «como hizo tu madre») y `floraciones` (las tres flores).
- MAPAS: el viaje de Finlay (Aeonia → Árbol Sagrado, pantalla completa) y dónde está el pantano de Aeonia (ventana).
  python fab.py er_malenia_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_malenia_atrocidades fx         audio/fx.wav
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

CAMARA = {   # diálogos casi quietos (Gideon, Millicent, Gowry): acercamiento lento en vez de rehacer (cuentan justo esa escena)
    **{f"scene-{n:03d}": dict(a=(1.0, 0, 0), b=(1.16, 0, -.05)) for n in (20, 82, 83, 92, 99, 100, 104)},
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
HIJAS = [("Millicent", "la de la aguja"), ("Mary", None), ("Maureen", None), ("Amy", None), ("Polyanna", None)]

FX = [
    # ================================================================ GANCHO
    peg("Si viste el video de Miquella", "miquella_nino", "Miquella", y=.60),
    grande("Preguntó si Malenia también estaba hechizada", "malenia_jefa", "Malenia, espada de Miquella", lado="der", dur=5.4, tam=640),
    pant("estatua", ("Y es una buena pregunta", -.2), ("aun así siguió peleando|fin", .3), zoom=(1.0, 1.12), pan=(0, 0, .08, 0)),
    peg("La que te mató cuarenta veces", "mano_malenia", "Mano de Malenia", tam=440),
    ficha("en lo primero que te suelta cuando entras a su arena", "Malenia, espada de Miquella",
          "Cadáver tras cadáver *dejé a mi paso*, mientras esperaba *su regreso*.", tipo="Lo que te dice al entrar",
          a=("mientras esperaba su regreso|fin", .8)),
    puesto("hoy van las cinco peores atrocidades de Malenia", "Las 5 peores atrocidades de", "Malenia", dur=4.2),
    peg("Es la putrefacción", "aeonia", "La putrefacción escarlata", tam=440),

    # ================================================================ 5 · NUNCA CONOCIÓ LA DERROTA
    puesto("Número cinco. Nunca conoció la derrota", "Atrocidad número 5", "Nunca conoció la derrota"),
    ficha("soy Malenia, la espada de Miquella", "Malenia, espada de Miquella",
          "Soy Malenia, espada de Miquella. *Y nunca he conocido la derrota*.", tipo="Lo que te dice",
          a=("Te está informando|fin", .4)),
    peg("La hoja que lleva en su brazo de metal", "mano_malenia", "Mano de Malenia", tam=440),
    ficha("la prótesis de guerra de Malenia simbolizaba", "Mano de Malenia",
          "La prótesis de guerra de Malenia *simbolizaba sus victorias*. Algunos dicen haber visto alas al alzarla: *alas de una "
          "determinación feroz que jamás conocieron la derrota*.", tipo="Arma", icono="mano_malenia",
          a=("jamás conocieron la derrota|fin", .6)),
    grande("Godrick, el injertado", "godrick", "Godrick el Injertado", lado="izq", dur=5.0, tam=620),
    peg("Lo cuenta Kenneth Haight", "kenneth", "Kenneth Haight", tam=400, x=.80, y=.62),
    ficha("Según él, Godrick insultó a Malenia", "Kenneth Haight",
          "Insultó a Malenia, perdió contra ella en combate, y *en vez de morir como un hombre, le lamió las botas*.",
          tipo="Lo que dice de Godrick", a=("prefirió lamerle las botas|fin", 1.2)),
    peg("Un semidiós de la línea de Godfrey", "godfrey", "Godfrey, primer señor del Círculo", tam=420),
    pant("godrick_f2", ("Se pasó el resto de su vida", -.2), ("justo lo que le faltaba a ella|fin", .3), zoom=(1.0, 1.12)),
    peg("Gideon, el que todo lo sabe", "gideon", "Gideon el Omnisciente", tam=400),
    ficha("la describe en pocas palabras", "Gideon el Omnisciente", "Su gemela, *Malenia, la espadachina invicta*.",
          tipo="Lo que dice", a=("eso ya debería darte miedo|fin", .3)),

    # ---- 5b · cómo gana
    grande("cada vez que su espada te toca, ella se cura", "malenia_jefa", "Malenia", lado="izq", dur=5.4, tam=620),
    peg("Y su Gran Runa", "runa_malenia", "Gran Runa de Malenia", tam=420),
    ficha("reduce el poder curativo de tu frasco", "Gran Runa de Malenia",
          "La bendición de esta runa medio podrida *reduce el poder curativo del frasco de lágrimas carmesí*.", tipo="Gran Runa",
          icono="runa_malenia", a=("Hasta muerta te sigue quitando vida|fin", .4)),
    peg("de tu frasco de lágrimas carmesí", "frasco", "Frasco de lágrimas carmesí", tam=320),
    peg("En el video de Radagon", "radagon", "Radagon", tam=380),
    peg("Hay un talismán que la cuenta", "reliquia", "El talismán de su infancia", tam=400),
    ficha("aunque nació en la putrefacción maldita", "El talismán de su infancia",
          "Aunque nació en la putrefacción maldita, cuando la niña conoció a *su mentor y su espada fluida*, obtuvo *alas de una "
          "fuerza sin igual*.", tipo="Talismán", icono="reliquia", a=("alas de una fuerza sin igual|fin", .8)),
    peg("en manos de alguien que lleva dentro", "olla_podrida", "La putrefacción de un dios exterior", tam=360),
    peg("una sola persona a la que nadie consigue parar", "malenia_icono", "Malenia", tam=380),

    # ================================================================ 4 · LOS QUE SE PUDRIERON POR ELLA
    puesto("Número cuatro. Los que se pudrieron por ella", "Atrocidad número 4", "Los que se pudrieron por ella"),
    grande("caballeros de armadura dorada", "cleanrot", "Los caballeros de Malenia", lado="der", dur=5.0, tam=600),
    peg("Y la descripción de su armadura", "armadura_cleanrot", "Su armadura", tam=420),
    ficha("Los caballeros juraron pelear junto a Malenia", "Armadura de sus caballeros",
          "Los caballeros juraron pelear junto a Malenia, *a pesar de la inevitable, aunque gradual, putrefacción de su carne*.",
          tipo="Armadura", icono="armadura_cleanrot", a=("A pesar de la putrefacción de su carne|fin", .3)),
    mg(E.juramento(["Pelearé junto a Malenia.", "Acepto la putrefacción de mi carne: inevitable, aunque gradual."]),
       ("Es decir, todos sabían", -.3), ("Firme aquí, por favor|fin", 1.2),
       ["Es decir, todos sabían", "los iba a pudrir", "Y aun así firmaron", "Firme aquí"], "juramento"),
    peg("Se los llevó a Aeonia", "aeonia", "Aeonia", tam=400),
    pant("preparando", ("Allí, frente al ejército de Radahn", -.2), ("estaban a su lado cuando pasó|fin", .3),
         zoom=(1.0, 1.12), pan=(0, 0, .12, 0)),
    grande("es el comandante O'Neil", "oneil", "Comandante O'Neil", lado="izq", dur=5.0, tam=640),
    peg("Su estandarte lo describe", "estandarte", "Estandarte del comandante", tam=420),
    ficha("Su estandarte lo describe", "Estandarte del comandante",
          "El único veterano que recuerda esta batalla *con orgullo*, en la devastación del campo *comido por la putrefacción*.",
          tipo="Arma", icono="estandarte", a=("comido por la putrefacción|fin", 1.0)),
    peg("lo matas por una aguja rota", "aguja", "Aguja de oro puro, rota", tam=440),

    # ---- 4b · Finlay y los hijos no deseados
    grande("la historia más triste de ese ejército es la de Finlay", "cenizas_finlay", "Finlay", lado="der", dur=5.0, tam=560),
    ficha("Y su descripción cuenta", "Cenizas de Finlay",
          "Una de las pocas supervivientes de Aeonia. *Cargó sola a Malenia, dormida*, de vuelta al Árbol Sagrado, abriéndose "
          "paso contra sus enemigos.", tipo="Lo que cuenta su descripción", icono="cenizas_finlay",
          a=("Se quedó dormida después de florecer|fin", .3)),
    mapa("mundo", [(.558, .735, "Caelid", "inicio", _P("aeonia_pantano")), (.50, .71), (.42, .70), (.33, .66), (.27, .56),
                   (.29, .43), (.36, .34), (.45, .37), (.53, .36), (.62, .30), (.63, .20), (.60, .12),
                   (.565, .08, "Árbol Sagrado", "meta", _P("haligtree"))],
         ("Y Finlay la cargó ella sola", -.3), ("hasta el Árbol Sagrado|fin", 1.5),   # MASTER 1: 3,9 s quieto tras llegar la ruta
         ["desde Caelid", "hasta el Árbol Sagrado"], titulo="Las Tierras Intermedias", sub="El viaje de Finlay"),
    peg("Con una diosa de la putrefacción dormida al hombro", "cenizas_finlay", "Finlay", tam=380),
    peg("Malenia siguió durmiendo bajo el árbol", "malenia_icono", "Malenia, dormida", tam=360),
    peg("Se llaman los parientes de la putrefacción", "cenizas_parientes", "Los parientes de la putrefacción", tam=420),
    ficha("Sus cenizas dicen", "Cenizas de los parientes",
          "Siervos de la diosa de la putrefacción. *Siervos que fueron abandonados*.", tipo="Cenizas", icono="cenizas_parientes",
          a=("Siervos que fueron abandonados|fin", .8)),
    peg("viene con una oración", "exultacion", "Su encantamiento", tam=380),
    mg(E.mensaje(["Putrefacción para la diosa escarlata.", "Oh, flores escarlata, floreced en tierras lejanas,",
                  "y volved a nosotros, los hijos no deseados."]),
       ("putrefacción para la diosa escarlata", -.2), ("volved a nosotros, los hijos no deseados|fin", 1.4),
       ["putrefacción para la diosa escarlata", "Oh, flores escarlata", "y volved a nosotros"], "oración", y=.76),
    *fila("Malenia tenía un ejército que se pudrió", [
        ("cleanrot", "Sus caballeros", None),
        ("cenizas_finlay", "Finlay", "una caballera que la cargó"),
        ("cenizas_parientes", "Los parientes", "una colonia de bichos")], dur=7.0),

    # ================================================================ 3 · CAELID
    puesto("Número tres. Caelid", "Atrocidad número 3", "Caelid"),
    pant("caelid", "Porque Caelid no siempre fue", ("con una ciudad de hechiceros, Sellia|fin", .2), zoom=(1.12, 1.0), pan=(.12, 0, 0, 0)),
    pant("sellia", ("Tanto, que el propio Radahn", -.2), ("estaba flaquísimo|fin", .3), zoom=(1.0, 1.10)),
    peg("el propio Radahn fue a estudiar", "radahn", "Radahn", tam=420),
    ficha("la magia de la gravedad", "Recuerdo del Azote Estelar",
          "Aprendió la magia de la gravedad en Sellia *para no tener que abandonar nunca a su amado, aunque esmirriado, corcel*.",
          tipo="Recuerdo", a=("estaba flaquísimo|fin", .6)),
    mg(E.mensaje(["La batalla de Aeonia.", "Radahn y Malenia, en un punto muerto.", "Y entonces, la putrefacción escarlata florece."]),
       ("Hay un monumento con una espada", -.1), ("Y entonces, la putrefacción escarlata florece|fin", 1.2),
       ["la batalla de Aeonia", "Radahn y Malenia, en un punto muerto", "Y entonces, la putrefacción escarlata florece"],
       "monumento", y=.76),
    grande("Estaba empatando", "malenia_jefa", "Malenia", lado="izq", dur=4.4, tam=600),
    peg("la Aeonia escarlata: crea", "aeonia", "Aeonia escarlata", tam=440),
    ficha("Esta es la descripción de su técnica", "Aeonia escarlata",
          "Técnica de Malenia, la diosa de la putrefacción. *Crea una flor gigantesca que florece en una explosión de "
          "putrefacción escarlata*.", tipo="Encantamiento", icono="aeonia", a=("donde vivía gente|fin", .3)),
    mapa("caelid", [(.42, .61, "Pantano de Aeonia", "peligro", _G("aeonia"))],
         ("Y el pantano que te encuentras hoy", -.2), ("donde se abrió aquella flor|fin", .6),
         ["Y el pantano que te encuentras hoy"], titulo="Caelid", ventana=True),
    mg(E.mensaje(["Aquí mismo floreció la primera flor de Aeonia.", "Malenia, que florezcas como una diosa."]),
       ("Hay un mensaje de un espíritu", -.1), ("Le reza a la que los mató|fin", .6),
       ["aquí mismo floreció la primera flor", "Malenia, que florezcas como una diosa"], "espíritu", y=.76),

    # ---- 3b · el ejército que no deja de pelear
    pant("castillo_radahn", ("Y el ejército de Radahn, qué pasó", -.2), ("Pues que nunca dejó de pelear|fin", .3), zoom=(1.0, 1.10)),
    peg("Gideon lo cuenta así", "gideon", "Gideon", tam=380),
    ficha("he oído que los supervivientes", "Gideon el Omnisciente",
          "He oído que los supervivientes del ejército de Radahn siguen en las tierras salvajes, *conteniendo la putrefacción "
          "con fuego*.", tipo="Lo que dice", a=("siguen quemando lo que se pudre para que no avance|fin", .2)),
    peg("Hasta la Gran Runa de Radahn", "runa_radahn", "Gran Runa de Radahn", tam=420),
    ficha("Su descripción dice: la Gran Runa arde", "Gran Runa de Radahn",
          "La Gran Runa *arde para resistir el avance* de la putrefacción escarlata.", tipo="Gran Runa", icono="runa_radahn",
          a=("ardiendo para no pudrirse|fin", .4)),
    grande("Jerren, el cazador de brujas", "jerren", "Jerren, cazador de brujas", lado="izq", dur=5.0, tam=560),
    ficha("Jerren dice que el general", "Jerren, cazador de brujas",
          "El general Radahn está maldito a vagar para siempre. *Comido por dentro por la putrefacción escarlata de Malenia*, hace "
          "mucho que perdió el juicio.", tipo="Lo que dice", a=("como un perro|fin", .5)),
    ficha("enfermo de putrefacción y lisiado", "Jerren, cazador de brujas",
          "Enfermo de putrefacción y lisiado por la locura, *todo lo que quería era una muerte honorable*.", tipo="Lo que dice",
          a=("Por eso existe el festival|fin", .3)),
    peg("Es un funeral que necesita invitados", "radahn", "El festival de Radahn", tam=420),
    mg(E.contagio(["Radahn", "su ejército", "la tierra entera"], centro="La primera flor"),
       ("Malenia pudrió a Radahn", -.4), ("limpiar el desastre, fuiste tú|fin", .8),
       ["Malenia pudrió a Radahn", "Pudrió a su ejército", "Pudrió la tierra entera"], "contagio 1"),

    # ================================================================ 2 · LAS HIJAS QUE NUNCA QUISO
    puesto("Número dos. Las hijas que nunca quiso", "Atrocidad número 2", "Las hijas que nunca quiso"),
    pant("iglesia_plaga", ("tirada en una iglesia", -.3), ("consumida por la putrefacción|fin", .4), zoom=(1.0, 1.10)),
    grande("Millicent es una chica", "millicent", "Millicent", lado="izq", dur=5.0, tam=600),
    ficha("mi carne se retuerce con putrefacción escarlata", "Millicent",
          "Mi carne se retuerce con putrefacción escarlata. *Soy de la sangre de Malenia*.", tipo="Lo que te dice",
          a=("Soy de la sangre de Malenia|fin", .8)),
    peg("A ella la encontró Gowry", "gowry", "Gowry", tam=420),
    pant("choza_gowry", ("un viejo sabio que vive en una choza", -.2), ("Un simple bebé, en el pantano de Aeonia|fin", .3),
         zoom=(1.0, 1.10)),
    ficha("fui yo quien la encontró", "Gowry", "Fui yo quien la encontró. *Un simple bebé, en el pantano de Aeonia*.",
          tipo="Lo que dice", a=("Un bebé en el pantano de Aeonia|fin", .5)),
    mg(E.repudio("Malenia", HIJAS), ("Tiene hermanas", -.2), ("valquirias que sirven a la diosa de la putrefacción|fin", .5),
       ["Tiene hermanas"], "repudio 1"),
    peg("convertida en una valquiria escarlata", "insignia", "Insignia de las valquirias", tam=380),
    ficha("Gowry tiene un plan", "Gowry",
          "Cuando Malenia ascienda a la divinidad, *Millicent también renacerá. Como valquiria escarlata*.", tipo="Lo que dice",
          a=("convertida en una valquiria escarlata|fin", .5)),
    ficha("alimentada por la traición, su capullo", "Gowry", "Alimentada por la traición, *su capullo florecerá con más intensidad*.",
          tipo="Lo que dice", a=("Hay que traicionarla para que florezca|fin", .5)),
    mg(E.mensaje(["Te lo ruego, mátala.", "Con tus propias manos."]), ("te lo ruego, mátala", -.2),
       ("Con tus propias manos|fin", 1.0), ["te lo ruego, mátala", "Con tus propias manos"], "mátala", y=.76),
    peg("mi pequeño capullo, el más prometedor", "millicent", "Millicent", tam=380),
    mg(E.repudio("Malenia", HIJAS), ("tú también nos repudiarás", -.3), ("su madre las repudió|fin", .6),
       ["tú también nos repudiarás", "como hizo tu madre"], "repudio 2"),

    # ---- 2b · la aguja
    peg("Una aguja de oro puro clavada en la carne", "aguja_reparada", "Aguja de oro puro", tam=440),
    ficha("de las que Miquella forjó", "Aguja de Miquella",
          "Una de las agujas de oro puro que Miquella forjó *para alejar la intromisión de los dioses exteriores*.",
          tipo="Objeto clave", icono="aguja_miquella", a=("de los dioses exteriores|fin", .8)),
    peg("la aguja rota que le quitaste al comandante", "oneil", "Comandante O'Neil", tam=400, dur=2.6),
    *fila("Pues esa es", [
        ("aguja", "Rota", None),
        ("aguja_reparada", "Reparada", "Gowry la repara")], dur=5.0),
    peg("te ayuda en las peleas", "millicent", "Millicent", tam=380),
    ficha("ahora sigo el camino que tomó Malenia", "Millicent",
          "Ahora sigo el camino que tomó Malenia, tras desatar el poder de la putrefacción escarlata. *Tengo algo que devolverle*.",
          tipo="Lo que dice", a=("Tengo algo que devolverle|fin", .8)),
    pant("haligtree", ("cuando por fin llega al final de su camino", -.3), ("Millicent elige|fin", .4), zoom=(1.0, 1.12)),
    ficha("Se arranca la aguja ella misma", "Millicent",
          "Me quité la aguja yo misma. *Prefiero pudrirme hasta la nada, tal como soy*.", tipo="Sus últimas palabras",
          a=("prefiero pudrirme hasta la nada, tal como soy|fin", 1.0)),
    peg("Una hija repudiada", "protesis_millicent", "Prótesis de Millicent", tam=380),
    peg("el juego te da a cambio la aguja de Miquella", "aguja_miquella", "Aguja de Miquella", tam=440),
    peg("Sigue soñando con su hermano", "malenia_icono", "Malenia", tam=360),
    mg(E.repudio("Malenia", HIJAS, remate="Ni siquiera llegó a verla"), ("Lo más cerca que Millicent estuvo", -.2),
       ("ni siquiera llegó a verla|fin", .6),
       ["Lo más cerca que Millicent estuvo", "Lo más cerca que Millicent estuvo", "esa aguja que tú le llevaste"], "repudio 3"),

    # ================================================================ 1 · LA TERCERA FLOR
    puesto("Número uno. La tercera flor", "Atrocidad número 1", "La tercera flor"),
    mg(E.contagio(["Caelid", "Radahn", "su ejército", "los caballeros", "las hijas"], centro="Una sola flor"),
       ("Todo lo que te he contado hasta ahora", -.2), ("la primera vez que Malenia floreció|fin", .6),
       ["Caelid, Radahn, su ejército", "Radahn, su ejército, los caballeros", "su ejército, los caballeros",
        "los caballeros, las hijas", "las hijas. Todo eso"], "contagio 2"),
    peg("en la descripción de la Aeonia escarlata", "aeonia", "Aeonia escarlata", tam=420),
    ficha("cada vez que la flor escarlata florece", "Aeonia escarlata",
          "Cada vez que la flor escarlata florece, la putrefacción de Malenia avanza. *Con la tercera flor, se convertirá en una "
          "diosa verdadera*.", tipo="Encantamiento", icono="aeonia", a=("cuántas lleva ya|fin", .3)),
    mg(E.floraciones(["Aeonia, contra Radahn", "Tu pelea"]), ("La primera fue en Aeonia", -.4), ("Fue en tu pelea|fin", 1.2),
       ["La primera fue en Aeonia", "Fue en tu pelea"], "floraciones 1"),
    ficha("Malenia se detiene, y te dice", "Malenia, diosa de la putrefacción", "Espera. *La flor escarlata florece una vez más*.",
          tipo="Lo que te dice", a=("Esa es la segunda flor|fin", .3)),
    pant("malenia_f2", ("Lo que ves en la segunda fase", -.2), ("no es un cambio de fase para lucirse|fin", .3), zoom=(1.0, 1.12)),
    mg(E.floraciones(["Aeonia, contra Radahn", "Tu pelea"]), ("Es Malenia a una sola flor", -.3), ("Ahora, púdrete|fin", .8),
       ["Es Malenia a una sola flor", "Es Malenia a una sola flor", "de convertirse en diosa"], "floraciones 2"),
    ficha("lo último que oyes es", "Malenia, diosa de la putrefacción",
          "Que tu carne sea consumida. *Por la putrefacción escarlata*.", tipo="Si te mata",
          a=("que tu carne sea consumida por la putrefacción escarlata|fin", .8)),
    pant("aeonia_pantano", ("Si con una sola flor", -.2), ("qué habría pasado con la tercera|fin", .3), zoom=(1.0, 1.12)),
    peg("Una descripción de objeto lo explica", "olla_podrida", "Olla de putrefacción", tam=380),
    ficha("Una descripción de objeto lo explica", "Olla de putrefacción",
          "La putrefacción es uno de los elementos divinos de los dioses exteriores, y *devora la vida como una plaga feroz*.",
          tipo="Objeto", icono="olla_podrida", a=("como una plaga feroz|fin", .6)),
    grande("La plaga misma, con alas", "malenia_jefa", "Malenia", lado="der", dur=4.6, tam=620),

    # ---- 1b · el hechizo
    *fila("Y hay gente esperándolo", [
        ("aeonia", "El espíritu del pantano", "El espíritu del pantano"),
        ("cenizas_parientes", "Los hijos no deseados", "Los hijos no deseados que le piden"),
        ("gowry", "Gowry", "Gowry, que quiere")], dur=8.0),
    peg("Tú, con tus frascos medio podridos", "frasco", "Tus frascos medio podridos", tam=340),
    peg("Su armadura entera", "armadura_malenia", "Armadura de Malenia", tam=420),
    ficha("lleva la misma frase en su voz", "Armadura de Malenia",
          "Mi hermano cumplirá su promesa. Posee la sabiduría y el encanto de un dios. *Es el más temible de todos los Empíreos*.",
          tipo="Armadura", icono="armadura_malenia", a=("Es el más temible de todos los Empíreos|fin", 1.0)),
    grande("Los hechizados de Miquella hablan de su bondad", "miquella", "Miquella el Bondadoso", lado="izq", dur=5.0, tam=600),
    mg(E.mensaje(["No estaba hechizada.", "Estaba de acuerdo."]), ("no hay nada en el juego que diga", -.2),
       ("Estaba de acuerdo|fin", 1.4), ["no hay nada en el juego que diga", "Estaba de acuerdo"], "de acuerdo", y=.76),
    *fila("Él ponía el encanto", [
        ("miquella_nino", "El encanto", None),
        ("mano_malenia", "La espada", "ella ponía la espada")], dur=6.0),
    ficha("sus últimas palabras no son para sus caballeros", "Malenia, al morir",
          "Oh, querido Miquella, mi hermano... *Lo siento. Por fin encontré a mi rival*.", tipo="Sus últimas palabras",
          a=("Ni al final se acordó de los suyos|fin", .4)),

    # ================================================================ CIERRE
    *fila("dejó atrás una tierra podrida", [
        ("aeonia", "Una tierra podrida", None),
        ("cleanrot", "Sus caballeros", "unos caballeros que se deshicieron"),
        ("millicent", "Sus hijas", "y unas hijas que prefirieron")], dur=5.6),
    *fila("quién fue peor de los gemelos", [
        ("miquella_nino", "Miquella", None),
        ("malenia_icono", "Malenia", "o Malenia, que estuvo")], dur=6.0),
    puesto("en el canal tienes las atrocidades de Miquella", "Ya en el canal · Miquella, Radagon, Márika y Ranni", "Toda la familia",
           dur=5.4),
    peg("Pregúntale qué hizo cuando iba empatando", "malenia_jefa", "La invicta", tam=440),
]
ROTULOS = []
SFX = {   # uno distinto por momento y distintos de Miquella/Ranni (regla: nada de SFX repetidos ante el canal)
    "flor": ("A giant crimson flower bursting open with a wet organic bloom and a deep rumbling explosion, dark fantasy", 4),
    "sello": ("A heavy wax seal stamp slammed onto old parchment, sharp thud with a paper rustle", 2),
    "fuego": ("Crackling torches and a large bonfire burning in a windy red wasteland, distant soldiers, dark fantasy", 4),
    "aguja": ("A thin golden needle slowly pulled out of flesh with a delicate metallic ring, quiet and eerie", 3),
    "alas": ("Huge crimson wings unfurling with a fleshy whoosh and petals scattering in the air, dark fantasy", 3),
}
PISTAS = [
    dict(sfx="sello", en="Firme aquí", vol=.5),
    dict(sfx="flor", en="Y entonces, la putrefacción escarlata florece", vol=.5),
    dict(sfx="fuego", en="conteniendo la putrefacción con fuego", vol=.35),
    dict(sfx="aguja", en="Se arranca la aguja ella misma", vol=.45),
    dict(sfx="alas", en="La flor escarlata florece una vez más", vol=.45),
]
