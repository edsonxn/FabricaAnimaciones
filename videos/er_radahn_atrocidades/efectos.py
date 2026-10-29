# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Radahn QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 28-oct-2026).
Fórmula de Melina/Miquella/Malenia (docs/estilo_secuencia_yt.md § PEGATINAS · MOTION GRAPHICS NUEVOS · MAPAS REALES CON RUTA)
con el kit de Elden Ring (nucleo/mg_er.py):
- PEGATINAS de cada personaje/objeto que nombra la voz (imagen real de eldenring.fandom.com en pegatinas/, bajar_pegatinas.py),
  chicas abajo a la izquierda, en fila cuando la voz enumera, y algunas GRANDES (media pantalla).
- COMENTARIOS reales (regla del 27/28-oct-2026): la tarjeta `com_<id>` sale cuando la voz menciona el comentario (gancho,
  Conker Lord, Mister Jesús Pain, Dinobot) y ≥ 4 de agradecimiento en el cierre (Pipo, Héctor, Jimmy, Barial, Maknarth).
- PANTALLAS a cuadro entero (pantallas/) donde el clip no enseña lo que hace falta ver (Aeonia, el consorte, los cuernos).
- fichas de descripción SOLO con citas verificadas (investigacion.md), arriba a la derecha; rótulo de puesto por atrocidad.
- MG NUEVOS de este guion: `lanzas` (las lanzas de los Imputrescibles vuelven como flechas contra ti), `cielo_sujeto` (los
  destinos que su victoria congeló; al caer, el cielo gira y cae la estrella), `balanza` (¿aceptó ser consorte?, el
  comentario de Dinobot) y `espejo` (Radagon y Radahn: consortes de un dios; el ídolo Godfrey tachado).
- MAPAS: Caelid (Sellia → Aeonia → Castillo de la Melena Roja) y la estrella que cae en Necrolimbo (mundo).
  python fab.py er_radahn_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_radahn_atrocidades fx         audio/fx.wav
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

CAMARA = {}
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


def com(en, cid, dur=6.0, x=.30, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


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
C_ZOHARY, C_CONKER, C_DINO, C_JESUS = "Ugzu17To_1EODNw3Ul94AaABAg", "Ugyh3XMSDrJ1xal_SDV4AaABAg", "UgyEonguQmG1rgVuVJh4AaABAg", "UgxmNyuD4WUxeo_uVHV4AaABAg"
C_PIPO, C_HECTOR, C_BARIAL, C_JIMMY, C_MAK = ("UgyvRw49fRF8kg6S0yJ4AaABAg", "Ugy1i1VPh1ZkrsRtSNR4AaABAg", "UgyAiQT45T97W4XVSPR4AaABAg",
                                              "UgxQScFrbg2feB1d3GZ4AaABAg", "Ugx03qCvSMiDP8Jg2F14AaABAg")
ATADOS = ["El destino de Ranni", "La familia real Caria", "La inmortalidad de Sellen", "La promesa de Jerren"]
PESOS = [("i", "Un juramento «con» él"), ("i", "«El juramento se cumplirá»"), ("i", "Lucha a su lado"),
         ("d", "Nunca vemos su respuesta"), ("d", "En Aeonia, a muerte"), ("d", "Miquella encanta al que se resiste"),
         ("d", "Su voz, cortada del juego")]

FX = [
    # ================================================================ GANCHO
    com("En el video de Miquella, alguien nos dejó este comentario", C_ZOHARY, dur=8.5),
    grande("Pues ese día es hoy", "radahn_render", "Radahn", lado="der", dur=4.4, tam=640),
    com("Conker Lord también nos pidió a Radahn", C_CONKER, dur=5.4),
    peg("El general que detuvo las estrellas", "reliquia_azote", "El Azote Estelar", tam=380),
    peg("El que aguantó a Malenia hasta el final", "malenia", "Malenia", tam=380, x=.80, y=.62),
    pant("radahn_festival", ("El que tiene un festival entero en su honor", -.2), ("a despedirlo como se merece|fin", .4),
         zoom=(1.0, 1.10)),
    pant("miquella_sobre", ("Y luego volvió en la expansión", -.2), ("con Miquella a su lado|fin", .6), zoom=(1.0, 1.12)),
    *fila("su mejor amigo, su caballera más fiel", [
        ("jerren", "Jerren, su amigo", None),
        ("freyja", "Freyja, su caballera", "su caballera más fiel"),
        ("iji", "Iji, el herrero", "el herrero que lo admiraba")], dur=4.6),
    puesto("Así que van las cinco peores atrocidades de Radahn", "Las 5 peores atrocidades de", "Radahn", dur=4.2),
    *fila("un par de ellas ya las rozamos en los videos de Malenia", [
        ("malenia", "Malenia", None),
        ("miquella", "Miquella", "y de Miquella")], dur=4.4),
    peg("fíjate bien de qué está hecha", "lanza_radahn", "Lanza de Radahn", tam=420),

    # ================================================================ 5 · EL BANQUETE DEL GENERAL
    puesto("Número cinco. El banquete del general", "Atrocidad número 5", "El banquete del general"),
    pant("castillo", ("tienes que pasar por el Castillo de la Melena Roja", -.2), ("al sur de Caelid|fin", .2), zoom=(1.0, 1.10)),
    grande("Ahí te recibe Jerren", "jerren_npc", "Jerren, el castellano", lado="izq", dur=4.6, tam=560),
    ficha("El general Radahn está condenado a vagar", "Jerren", "El general Radahn está condenado a vagar para siempre. La "
          "putrefacción escarlata de Malenia lo devora por dentro, y *hace mucho que perdió el juicio*.", tipo="Lo que te cuenta",
          a=("hace mucho que perdió el juicio|fin", .6)),
    ficha("ahora reúne los cadáveres de antiguos amigos", "Jerren", "Ahora reúne los cadáveres de antiguos amigos y enemigos, y "
          "*se atiborra de ellos como un perro*. Aullándole al cielo.", tipo="Lo que te cuenta",
          a=("Aullándole al cielo|fin", 1.0)),
    peg("Como un perro. Lo dice su mejor amigo", "jerren", "Su mejor amigo", tam=380),
    *fila("los Melena Roja, que eran sus propios soldados", [
        ("armadura_melena", "Los Melena Roja", None),
        ("cleanrot", "Caballeros de Malenia", "y los caballeros de Malenia")], dur=4.6),
    peg("Se come a los dos", "radahn_icono", "Radahn", tam=440, x=.80, y=.60),
    com("Mister Jesús Pain bromeaba", C_JESUS, dur=7.5),
    peg("Esa caballera, Finlay", "finlay", "Finlay", tam=420, x=.80, y=.60),
    peg("Pero a muchos de sus caballeros nadie los cargó", "cleanrot", "Los que no volvieron", tam=380),
    ficha("Si recoges una de la arena", "Lanza de Radahn", "Flechas grandes que usó el general Radahn durante el festival del "
          "combate. *En realidad, son las muchas lanzas con las que lo atravesaron los Caballeros Imputrescibles*.",
          tipo="Munición", icono="lanza_radahn", a=("los Caballeros Imputrescibles|fin", .8)),
    mg(E.lanzas(), ("O sea, los caballeros de Malenia lo llenaron de lanzas", -.2), ("a los que intentaron matarlo|fin", 1.0),
       ["lo llenaron de lanzas", "y él te las dispara a ti"], "lanzas"),
    pant("radahn_dunas", ("Y si te fijas en sus pies", -.2), ("buscando qué comer|fin", .4), zoom=(1.0, 1.14), pan=(0, 0, 0, .05)),

    # ---- 5b · el festival
    peg("Jerren tiene la respuesta: con una fiesta", "jerren_npc", "Jerren", tam=400),
    ficha("Esta fortaleza solo alberga a los vencidos", "Jerren", "Esta fortaleza solo alberga a los vencidos. *Pero cuando las "
          "estrellas se alinean, celebramos*.", tipo="Lo que te dice", a=("se declara el festival|fin", .6)),
    peg("ya sabes dónde acabaron", "radahn", "En las dunas", tam=420),
    ficha("Su capucha lo cuenta", "Capucha del excéntrico", "Jerren sirvió al general Radahn como comandante invitado, y se dice "
          "que *se juraron mutuamente una muerte honorable*.", tipo="Capucha", icono="capucha_jerren",
          a=("una muerte honorable|fin", 1.0)),
    peg("Su armadura añade", "armadura_jerren", "Armadura del excéntrico", tam=400),
    peg("Atado a matar a su amigo", "jerren", "Jerren", tam=380, x=.80, y=.62),
    pant("fuerte_gael", ("En el Fuerte Gael, al oeste de Caelid", -.2), ("el espíritu de un soldado muerto|fin", .3), zoom=(1.0, 1.10)),
    mg(E.mensaje(["Convoquen el festival de la guerra.", "Honren al general Radahn", "con la gloria de un guerrero.",
                  "Está en tus manos, Sir Jerren."]),
       ("Su último deseo es este", -.1), ("Está en tus manos, Sir Jerren|fin", .6),
       ["convoquen el festival de la guerra", "Honren al general Radahn", "con la gloria de un guerrero",
        "Está en tus manos, Sir Jerren"], "alma Gael", y=.76),
    peg("Eso te dice todo de cómo estaba Radahn", "cenizas_soldado", "Sus soldados", tam=400),
    ficha("Jerren lo despide así en la versión en inglés", "Jerren · en inglés", "Pudriéndose, y lisiado por la locura, *todo lo "
          "que quería era una muerte honorable*.", tipo="Lo que dice", a=("todo lo que quería era una muerte honorable|fin", .6)),
    ficha("Pero en el japonés original no dice eso", "Jerren · en japonés", "Fue, sin duda, *un final mucho más honorable* que "
          "pudrirse y enloquecer.", tipo="Lo que dice en realidad", a=("Es lo que su amigo decidió que era mejor para él|fin", .6)),
    peg("Es el único portador de una Gran Runa", "runa_radahn", "Gran Runa de Radahn", tam=420),
    grande("Y Blaidd, que pelea a tu lado en el festival", "blaidd_cara", "Blaidd", lado="izq", dur=4.4, tam=520),
    ficha("qué forma tan enferma de pelear", "Blaidd", "Qué forma tan enferma de pelear, ¿eh? *La gloria del choque se la "
          "reparten Radahn y tú*.", tipo="Lo que dice", a=("Bonito festival|fin", .4)),

    # ================================================================ 4 · SALVÓ SELLIA. Y LUEGO LA PUDRIÓ
    puesto("Número cuatro. Salvó Sellia", "Atrocidad número 4", "Salvó Sellia y la pudrió"),
    ficha("Su recuerdo cuenta que el general", "Recuerdo del Azote de las Estrellas", "El general conocido como el León Rojo poseía "
          "poderes gravitacionales aprendidos en Sellia durante su juventud. *Todo para no tener que abandonar nunca a su querido "
          "aunque escuálido corcel*.", tipo="Recuerdo", icono="recuerdo_azote", a=("aunque escuálido, corcel|fin", .8)),
    grande("El caballo se llama Leonard", "leonard", "Leonard", lado="izq", dur=4.8, tam=620),
    peg("sin partirle la espalda", "radahn_render", "Radahn y Leonard", tam=420, x=.80, y=.60),
    peg("el talismán del gato de cola larga", "gato", "Talismán del gato de cola larga", tam=420),
    peg("Al semidiós más fuerte le borraron el gato", "gato", "Ya no es suyo", tam=360, x=.80, y=.62),
    *fila("Con él estudiaba también Gaius", [
        ("gaius_peg", "Gaius", None),
        ("radahn_retrato", "Radahn", "Gaius y Radahn fueron buenos rivales")], dur=4.4),
    peg("Uno de sus hechizos lo dice", "hojas_piedra", "Hojas de piedra", tam=380, x=.80, y=.40),
    ficha("y uno de los hechizos de Radahn guarda una frase", "Estrellas en colapso", "Técnica gravitatoria que dominó el joven "
          "Radahn. *«Te agradezco tu tutela, maestro, porque ahora puedo desafiar a las estrellas»*.", tipo="Hechizo",
          icono="estrellas_colapso", a=("ahora puedo desafiar a las estrellas|fin", .8)),
    pant("gran_puente", ("Junto a un puente de Caelid hay un monumento", -.2), ("con una espada clavada que dice|fin", .3),
         zoom=(1.0, 1.10)),
    mg(E.mensaje(["El conflicto del Azote de las Estrellas.", "Radahn mantiene Sellia segura.", "Un hombre que se alza",
                  "para hacer pedazos las estrellas."]),
       ("el conflicto del Azote de las Estrellas", -.1), ("Por eso lo llaman el Azote Estelar|fin", .4),
       ["el conflicto del Azote de las Estrellas", "Radahn mantiene Sellia segura", "Un hombre que se alza",
        "para hacer pedazos las estrellas"], "monumento 1", y=.76),
    pant("sellia", ("Las estrellas caían sobre Sellia", -.2), ("Por eso lo llaman el Azote Estelar|fin", .3), zoom=(1.0, 1.10)),
    mg(E.mensaje(["La batalla de Aeonia.", "Radahn y Malenia en punto muerto.", "Y entonces florece",
                  "la putrefacción escarlata."]),
       ("Ahora busca otro monumento", -.1), ("Y entonces florece la putrefacción escarlata|fin", .6),
       ["la batalla de Aeonia", "Radahn y Malenia en punto muerto", "Y entonces florece", "la putrefacción escarlata#2"],
       "monumento 2", y=.76),
    pant("aeonia_trailer", ("Y abre el mapa de Caelid y lee la descripción", -.2), ("han quedado devastadas por la putrefacción|fin", .4),
         zoom=(1.0, 1.10), pan=(0, 0, -.05, 0)),
    ficha("Y abre el mapa de Caelid", "Mapa: Caelid", "Las vastas tierras de Caelid, *conocidas por haber sido escenario del "
          "último combate entre el general Radahn y Malenia*, han quedado devastadas por la putrefacción.", tipo="Fragmento de mapa",
          a=("han quedado devastadas por la putrefacción|fin", .6)),

    # ---- 4b · el pueblo, el ejército y Freyja
    mapa("caelid", [(.51, .52, "Sellia", "inicio", _P("sellia")), (.47, .56), (.43, .60, "Pantano de Aeonia", "peligro", _P("pantano")),
                    (.50, .66), (.58, .71), (.65, .77, "Castillo de la Melena Roja", "meta", _P("castillo"))],
         ("Mira el mapa", -.4), ("está a un paso del pueblo que él había salvado|fin", 1.2),
         ["Mira el mapa", "donde floreció la flor de Malenia", "está a un paso del pueblo"], titulo="Caelid",
         sub="Lo que salvó y lo que se pudrió", traza=99),
    mg(E.mensaje(["Se pudre. Todo se pudre de escarlata.", "Y Sellia, el pueblo de la hechicería.", "El fin está cerca, para todos."]),
       ("Un alma varada de Caelid lo cuenta como puede", -.1), ("El fin está cerca, para todos|fin", .6),
       ["se pudre. Todo se pudre de escarlata", "y Sellia, el pueblo de la hechicería", "El fin está cerca"], "alma Sellia", y=.76),
    grande("Millicent lo dice de Malenia", "millicent", "Millicent", lado="izq", dur=4.6, tam=560),
    ficha("Millicent lo dice de Malenia", "Millicent", "Debo devolverle a Malenia su voluntad. *El orgullo que abandonó para "
          "estar a la altura de Radahn*.", tipo="Lo que dice", a=("Él la empujó hasta ahí|fin", .6)),
    pant("aeonia_t16", ("Para igualarlo, Malenia tuvo que soltar la flor", -.2), ("Él la empujó hasta ahí|fin", .3), zoom=(1.0, 1.10)),
    ficha("La armadura lo explica", "Armadura de caballero Melena Roja", "Cuando la putrefacción de Malenia los derrotó, *los "
          "caballeros quemaron el blasón del pecho izquierdo* para mostrar su determinación. «Ay, mi hogar, no volveré a verte. "
          "Nuestro deber es quedarnos aquí, como un baluarte contra la plaga.»", tipo="Armadura", icono="armadura_melena",
          a=("como un baluarte contra la plaga|fin", 1.0)),
    peg("Esos soldados con antorchas", "cenizas_soldado", "Los soldados de Radahn", tam=420),
    peg("quemando una enfermedad que nunca se acaba", "sobreveste_melena", "El blasón quemado", tam=380, x=.80, y=.62),
    ficha("te lo dice aliviado", "Jerren", "*Por fin, mi trabajo ha terminado*. Ya no estoy atado a esta fortaleza.",
          tipo="Cuando lo matas", a=("Ya no estoy atado a esta fortaleza|fin", .8)),
    grande("Y luego está Freyja", "freyja_render", "Freyja, Melena Roja", lado="der", dur=5.0, tam=640),
    peg("a la que él mismo reclutó", "armadura_freyja", "Armadura de Freyja", tam=380),
    ficha("Hace mucho, la putrefacción escarlata me alcanzó", "Freyja", "Hace mucho, la putrefacción escarlata me alcanzó en el "
          "pantano de Aeonia. Inmóvil, con fiebre y con mucho dolor, me resigné a morir. *Me dejaron atrás*. Y solo Miquella el "
          "Bondadoso fue capaz de venir a buscarme.", tipo="Lo que te cuenta", a=("fue capaz de venir a buscarme|fin", .8)),
    pant("pantano", ("Me dejaron atrás. Su general no volvió por ella", -.2), ("con la gente que recoge del suelo|fin", .3),
         zoom=(1.0, 1.10)),
    peg("El que volvió fue Miquella", "miquella_nino", "Miquella", tam=420, x=.80, y=.60),

    # ================================================================ 3 · CONGELÓ EL DESTINO DE TODOS
    puesto("Número tres. Congeló el destino de todos", "Atrocidad número 3", "Congeló el destino de todos"),
    ficha("la reliquia del Azote de las Estrellas", "Reliquia del Azote de las Estrellas", "El más poderoso de los héroes semidioses "
          "se enfrentó solo a las estrellas que caían, y las aplastó. *Su conquista selló el destino mismo de las estrellas*.",
          tipo="Talismán", icono="reliquia_azote", a=("selló el destino mismo de las estrellas|fin", .8)),
    pant("radahn_arte", ("Selló el destino de las estrellas. Suena a hazaña", -.2), ("Son el destino de una familia entera. La suya|fin", .3),
         zoom=(1.0, 1.12), pan=(0, 0, 0, -.06)),
    grande("Iji, el herrero gigante de Liurnia", "iji_cara", "Iji", lado="izq", dur=4.6, tam=540),
    ficha("Iji, el herrero gigante de Liurnia", "Iji", "El destino de la familia real Caria lo guían las estrellas. Igual que el de "
          "la señora Ranni. Pero el general Radahn es el conquistador de las estrellas: *detuvo su movimiento con una victoria "
          "aplastante*.", tipo="Lo que te explica", a=("con una victoria aplastante|fin", .6)),
    ficha("si el general Radahn fuera derrotado", "Iji", "Si el general Radahn fuera derrotado, las estrellas volverían a moverse. "
          "*Y también el destino de la señora Ranni*.", tipo="Lo que te explica", a=("Y también el destino de la señora Ranni|fin", .8)),
    *fila("Ranni es su hermana", [
        ("ranni_cuadro", "Ranni", None),
        ("rennala", "Rennala", "Rennala, la reina de la Luna Llena"),
        ("radagon", "Radagon", "y Radagon"),
        ("radahn_retrato", "Radahn", "el destino de su hermana estuvo congelado")], dur=6.0, tam=320),
    peg("Blaidd, la sombra de Ranni", "blaidd", "Blaidd", tam=420, x=.80, y=.62),
    mg(E.cielo_sujeto(["El destino de Ranni"], remate="Alguien tiene que soltarlo"),
       ("¿Lo hizo a propósito?", -.2), ("Ese alguien eres tú|fin", 1.2),
       ["Lo único que consta es el efecto", "Ese alguien eres tú"], "cielo sujeto 1"),
    ficha("Blaidd lo ve en directo", "Blaidd", "¡Una estrella cayendo, ante nuestros ojos! *No me explico cómo Radahn sujetaba algo "
          "de esa escala*.", tipo="Lo que ve", a=("algo de esa escala|fin", .8)),
    mapa("mundo", [(.558, .735, "Caelid", "inicio", _P("radahn_dunas")), (.53, .70), (.50, .71),
                   (.47, .735, "Necrolimbo", "meta", _G("nokron"))],
         ("Una estrella entera se estrella en Necrolimbo", -.3), ("y el camino hacia el destino de Ranni|fin", 1.0),
         ["Una estrella entera se estrella en Necrolimbo", "Y debajo está Nokron"], titulo="Las Tierras Intermedias",
         sub="La estrella que sujetaba", traza=99),

    # ---- 3b · Sellen inmortal y la promesa de Jerren
    ficha("Cuando matas a Radahn, Iji te dice esto", "Iji", "Con las estrellas del destino otra vez en marcha, *cierta hechicera "
          "pierde su inmortalidad*. Por fin podremos librarnos de una vieja mala hierba de los Caria.", tipo="Lo que te dice",
          a=("una vieja mala hierba de los Caria|fin", .8)),
    grande("Esa hechicera es Sellen", "sellen", "Sellen", lado="izq", dur=5.0, tam=560),
    ficha("Obsesionada por la corriente primigenia", "Jerren, sobre Sellen", "Obsesionada por la corriente primigenia, *incontables "
          "hechiceros cayeron por su mano*. La maga más peligrosa de toda la historia de la academia de Raya Lucaria.",
          tipo="Lo que cuenta", a=("de la academia de Raya Lucaria|fin", .8)),
    *fila("Y mientras Radahn tuviera las estrellas quietas", [
        ("radahn_retrato", "Radahn", None),
        ("sellen", "Sellen, inmortal", "Sellen no podía morir")], dur=4.8),
    ficha("ha llegado la hora de recordarle una vieja promesa", "Iji", "*Ha llegado la hora de recordarle una vieja promesa*.",
          tipo="Lo que te dice", a=("hasta que muriera su amigo|fin", .6)),
    pant("radahn_festival", ("En cuanto Radahn cae, el viejo deja el castillo", -.2), ("Es Jerren, el cazador de brujas|fin", .3),
         zoom=(1.0, 1.10), oscuro=.15),
    peg("a las ruinas de la Perdición de la Bruja", "ruinas_bruja", "Ruinas de la Perdición de la Bruja", tam=440, x=.80, y=.60),
    mg(E.cielo_sujeto(ATADOS), ("Piénsalo. Un solo hombre agarraba el cielo", -.2), ("Ni qué más tenía agarrado|fin", .8),
       ["agarraba a su hermana", "a toda una familia real", "a una asesina inmortal", "y al juramento de su mejor amigo",
        "Y cuando lo sueltas"], "cielo sujeto 2"),
    peg("Ya contamos en el video de Ranni", "ranni", "Ranni", tam=420),
    peg("matando a su hermano en una fiesta", "radahn", "Radahn", tam=400, x=.80, y=.62),

    # ================================================================ 2 · EL JURAMENTO
    puesto("Número dos. El juramento", "Atrocidad número 2", "El juramento"),
    peg("En el video de Miquella vimos la propuesta", "miquella", "Miquella", tam=420),
    ficha("El recuerdo de la expansión lo cuenta así", "Recuerdo de un dios y un señor", "En su infancia, Miquella ya veía en Radahn "
          "a un señor. Su fuerza y su bondad contrastaban con su alma afligida. *Y así Miquella formuló su más sincero deseo: que "
          "Radahn fuera algún día su rey consorte*.", tipo="Recuerdo", icono="recuerdo_dios", a=("su rey consorte|fin", .6)),
    mg(E.mensaje(["…私の王に、なってください", "Por favor, sé mi rey."]), ("En japonés, esa última línea", -.1),
       ("por favor, sé mi rey|fin", .8), ["Es un ruego", "por favor, sé mi rey"], "japonés", y=.76),
    pant("puerta_divinidad", ("Y en la Puerta de la Divinidad", -.2), ("prométeme que serás mi consorte|fin", .4), zoom=(1.0, 1.10)),
    *fila("Nuestra parte. En plural", [
        ("miquella_nino", "Miquella", None),
        ("malenia", "La Espada de Miquella", "Su hermana. La que el juego llama")], dur=5.4),
    pant("aeonia_t23", ("Y fue justo ella la que fue a buscar a Radahn", -.2), ("que ya contamos en el video de Miquella|fin", .3),
         zoom=(1.0, 1.10)),
    peg("el famoso mensaje del consorte prometido", "yelmo_leon", "Yelmo del joven león", tam=400, x=.80, y=.60),
    ficha("Freyja confirma que el juramento existía", "Freyja", "Miquella el Bondadoso me habló del juramento que hizo una vez *con "
          "el general Radahn*. Y es aquí donde se cumplirá. Soy una Melena Roja. Debo saber la naturaleza de ese juramento.",
          tipo="Lo que dice", a=("Debo saber la naturaleza de ese juramento|fin", .6)),
    peg("Ni siquiera su caballera más fiel sabía", "freyja", "Freyja", tam=400),
    peg("Tuvo que ir hasta la Fortaleza Sombría", "fortaleza_sombria", "La Fortaleza Sombría", tam=460, x=.80, y=.60),
    ficha("Y en esa misma fortaleza está el pergamino", "Pergamino del rito secreto", "*Un señor anunciará el regreso de un dios*, y "
          "el alma del señor requerirá un recipiente.", tipo="Objeto clave", icono="pergamino",
          a=("y el alma del señor requerirá un recipiente|fin", .8)),
    peg("Radahn tenía que estar muerto", "runa_radahn2", "Gran Runa de Radahn", tam=400),

    # ---- 2b · las dos posturas
    pant("consorte_puerta", ("Cuando empieza la pelea final de la expansión", -.2), ("Para que pueda ser mi consorte|fin", .3),
         zoom=(1.0, 1.12)),
    ficha("Cuando empieza la pelea final de la expansión", "Miquella", "*Mi leal espada. Y campeón del festival*. Las hazañas de "
          "ambos se cantarán por siempre. Ahora el juramento se cumplirá, y el alma de mi hermano mayor volverá.", tipo="Lo que dice",
          a=("Para que pueda ser mi consorte|fin", .6)),
    *fila("Le da las gracias a dos personas", [
        ("malenia", "Su leal espada", "A su leal espada"),
        ("radahn_icono", "Radahn", "la que pudrió a Radahn"),
        ("runa_radahn", "El campeón: tú", "Y al campeón del festival")], dur=5.4),
    com("aquí entra un comentario que nos dejó Dinobot", C_DINO, dur=8.0),
    mg(E.balanza("Aceptó", "No aceptó", PESOS, remate="Nunca lo dice", titulo="¿Aceptó ser el consorte?"),
       ("Primera postura: aceptó", -.2), ("Ni para aceptar, ni para negarse|fin", 1.0),
       ["Freyja habla de un juramento hecho con él", "Miquella dice que el juramento se cumplirá", "Radahn lucha a su lado",
        "Segunda postura: nunca aceptó", "En Aeonia pelearon a muerte", "Miquella el Bondadoso es un monstruo",
        "Lo quitaron", "Ni para aceptar, ni para negarse"], "balanza"),
    peg("Ansbach lo resume así", "ansbach_npc", "Ansbach", tam=420, x=.20, y=.80),
    ficha("En un texto que se quedó sin usar", "Archivos del juego · texto cortado", "Soy Radahn. Hijo de Radagon de la melena roja, "
          "y de Rennala de la Luna Llena. *Un león criado para la batalla*.", tipo="Lo que iba a decir",
          a=("Un león criado para la batalla|fin", .8)),
    pant("consorte_cara", ("Así que esto es lo firme", -.2), ("y dentro de otro cuerpo|fin", .5), zoom=(1.0, 1.14)),
    peg("Si aceptó, prometió su alma", "miquella_perfil", "Miquella", tam=420),
    peg("lo usaron como a un muñeco", "radahn_concepto", "Radahn", tam=420, x=.80, y=.60),

    # ================================================================ 1 · VOLVIÓ EN EL CUERPO DE MOHG
    puesto("Número uno. Volvió en el cuerpo de Mohg", "Atrocidad número 1", "Volvió en el cuerpo de Mohg"),
    ficha("su reacción es esta: a mí me parece bien", "Freyja", "A mí me parece bien. Sé que al viejo Jerren le dolería, pero *la "
          "guerra siempre le sentó mejor al general Radahn*. Mucho mejor que cualquier muerte honorable.", tipo="Lo que dice",
          a=("para avivar el alma|fin", .6)),
    *fila("Todo lo que Jerren organizó", [
        ("jerren", "El festival", None),
        ("capucha_jerren", "El juramento", "el juramento de muerte honorable"),
        ("cenizas_soldado", "El último deseo", "el último deseo de los soldados")], dur=5.0),
    peg("lo tira a la basura en una frase", "freyja", "Freyja", tam=400, x=.80, y=.60),
    peg("Ansbach, el viejo caballero de Mohg", "ansbach", "Ansbach", tam=460),
    ficha("Usar a lord Mohg para entrar en la Tierra Sombría", "Ansbach", "Usar a lord Mohg para entrar en la Tierra Sombría ya era "
          "bastante. Pero además *planea usar su cadáver como recipiente para su rey consorte*. Solo desea su cáscara vacía.",
          tipo="Lo que descubre", a=("Solo desea su cáscara vacía|fin", .8)),
    grande("El cuerpo que ves en la pelea final es el de Mohg", "mohg", "Mohg, el señor de la sangre", lado="izq", dur=4.4, tam=560),
    pant("cuernos", ("Mira sus brazos", -.2), ("Las de Mohg|fin", .4), zoom=(1.0, 1.14)),
    ficha("Y si invocas a Ansbach para esa pelea", "Ansbach, contra el consorte", "General Radahn. Un placer verte después de tanto "
          "tiempo. *Pero esos restos no te pertenecen*. Lord Mohg tendrá su dignidad.", tipo="Lo que le dice",
          a=("Lord Mohg tendrá su dignidad|fin", .8)),
    mg(E.mensaje(["Esos restos no te pertenecen."]),
       ("Esos restos no te pertenecen. El héroe", -.1), ("Ni una palabra para defenderse|fin", .4),
       ["Esos restos no te pertenecen#2"], "restos", y=.76),
    *fila("Fue Mohg el que secuestró a Miquella", [
        ("mohg", "Mohg", None),
        ("miquella_nino", "Miquella", "Y ahora Miquella le roba el cadáver"),
        ("radahn_icono", "Radahn", "y mete dentro a su hermano")], dur=5.4),
    pant("miquella_sobre", ("Y en la segunda fase, Miquella aparece", -.2), ("y a mi consorte prometido, Radahn|fin", .4),
         zoom=(1.0, 1.12)),
    ficha("Y en la segunda fase, Miquella aparece", "Miquella", "Sinluz. Aspirante a señor del viejo orden. Si has conocido el "
          "pecado, si sufres por este mundo, cédenos el camino. *A mí, Miquella, y a mi consorte prometido, Radahn*.",
          tipo="Lo que te dice", a=("y a mi consorte prometido, Radahn|fin", .6)),

    # ---- 1b · el agarre, los parches, Freyja y el espejo
    mg(E.mensaje(["Que tus pensamientos", "sean solo de amor."]), ("Te susurra", -.1), ("que tus pensamientos sean solo de amor|fin", .8),
       ["que tus pensamientos", "sean solo de amor"], "amor", y=.76),
    peg("El juego lo llama corazón robado", "runa_miquella", "Gran Runa de Miquella", tam=400, x=.80, y=.62),
    ficha("el parche uno punto catorce", "Notas del parche 1.14 · 11-sep-2024", "Se han realizado los siguientes ajustes *al jefe "
          "final de SHADOW OF THE ERDTREE*: menos daño en algunos ataques, menos alcance y efectos más visibles.",
          tipo="Parche oficial", a=("Solo, jefe final|fin", .6)),
    ficha("En marzo de dos mil veintidós", "Parche 1.03.3 · 4-abr-2022", "Corregido un error en el ajuste del jefe «Radahn, Azote "
          "de las Estrellas» de la 1.03: *el poder de algunos ataques se redujo sin querer*.", tipo="Parche oficial",
          a=("Ni los parches saben qué hacer con él|fin", .4)),
    peg("En Enir-Ilim, al final de todo", "leda", "Leda y los suyos", tam=420),
    mg(E.mensaje(["Ofrezco este combate", "a Miquella el Bondadoso. Y a Rada…"]), ("Y en esa pelea dice", -.1),
       ("Y a Rada|fin", 1.2), ["ofrezco este combate", "Y a Rada"], "Rada", y=.76),
    pant("enir_ilim", ("No le da tiempo a terminar el nombre", -.2), ("ni siquiera está ahí para oírla|fin", .4), zoom=(1.0, 1.10)),
    ficha("Su armadura dice que, desde muy pequeño", "Armadura leonina de Radahn", "*Desde muy pequeño, Radahn quedó cautivado por "
          "el Señor del Campo de Batalla*.", tipo="Armadura", icono="armadura_leon", a=("Su ídolo de niño|fin", .6)),
    grande("Por Godfrey", "godfrey_jefe", "Godfrey, primer Señor del Círculo", lado="izq", dur=4.6, tam=560),
    mg(E.espejo(), ("Godfrey fue el rey al que su propio padre", -.2), ("En un cuerpo prestado. Sin voz|fin", 1.4),
       ["Radagon dejó a Rennala", "Y eso es exactamente en lo que acabó Radahn", "Consorte de un dios"], "espejo"),
    ficha("es el recuerdo de esa promesa entre los dos", "Recuerdo de un dios y un señor", "El recuerdo del consorte prometido. "
          "*Un dios y un señor*.", tipo="Recuerdo", icono="recuerdo_dios2", a=("Primero, el dios|fin", .8)),

    # ================================================================ CIERRE
    *fila("Esa es la lista. El héroe de Caelid", [
        ("lanza_radahn", "Se come a sus muertos", None),
        ("aeonia", "Pudrió Sellia", "salvó un pueblo y luego lo pudrió"),
        ("reliquia_azote", "Congeló el destino", "congeló el destino de su hermana"),
        ("recuerdo_dios", "Prometió su alma", "prometió su alma a un niño#2"),
        ("mohg", "Robó un cadáver", "y volvió dentro del cadáver")], tam=290, dur=9.0),
    pant("consorte", ("Y lo más triste es que", -.2), ("Y él solo ruge|fin", .6), zoom=(1.0, 1.12)),
    com("Antes de irme, gracias", C_PIPO, dur=5.0, x=.30, y=.30, tam=700),
    com("a Héctor", C_HECTOR, dur=5.0, x=.70, y=.36, tam=700),
    com("a Jimmy", C_JIMMY, dur=5.0, x=.32, y=.62, tam=700),
    com("Barial nos contó", C_BARIAL, dur=7.0, x=.66, y=.66, tam=740),
    com("Y Maknarth decía que le gustó el formato largo", C_MAK, dur=5.0, x=.30, y=.34, tam=700),
    peg("lo leímos, y lo cuidamos en este", "miquella", "Miquella", tam=360),
    peg("lo leímos, y lo cuidamos en este", "mohg", "Mohg", tam=360, x=.80, y=.62),
    *fila("¿Radahn aceptó ser el consorte", [
        ("radahn_icono", "Aceptó", None),
        ("radahn_concepto", "Lo usaron", "o lo usaron")], dur=4.4),
    com("Morgott ya está en la lista", C_CONKER, dur=4.2, x=.70, y=.32, tam=700),
    puesto("en el canal tienes las atrocidades de Márika", "Ya en el canal", "Toda la familia", dur=5.4),
    peg("Sobre todo para usarse unos a otros", "radagon", "Cosas de familia", tam=380),
    peg("ya se la clavaron a él", "lanza_radahn", "Lanza de Radahn", tam=440, x=.80, y=.60),
]
ROTULOS = []
SFX = {   # uno distinto por momento y distintos de Melina/Miquella/Ranni/Malenia (regla: nada de SFX repetidos ante el canal)
    "lanzas": ("A volley of heavy spears whooshing and thudding into armor, then a deep gravitational hum, dark fantasy", 3),
    "aullido": ("A distant monstrous howl echoing over a windy desert of red sand, grief and madness, dark fantasy", 4),
    "estrella": ("A huge meteor streaking across the sky and crashing far away, deep rumble and shockwave, dark fantasy", 5),
    "cadenas_luz": ("Taut glowing threads of energy snapping one after another with a crystalline twang, cosmic", 3),
    "balanza": ("An old brass balance scale creaking and tilting, small weights clinking onto metal pans", 3),
    "cuernos": ("Wet flesh and bone cracking as horns push out of skin, low and unsettling, dark fantasy", 3),
}
PISTAS = [
    dict(sfx="aullido", en="Aullándole al cielo", vol=.4),
    dict(sfx="lanzas", en="lo llenaron de lanzas", vol=.45),
    dict(sfx="estrella", en="Una estrella entera se estrella en Necrolimbo", vol=.5),
    dict(sfx="cadenas_luz", en="Y cuando lo sueltas", vol=.45),
    dict(sfx="balanza", en="Primera postura: aceptó", vol=.4),
    dict(sfx="cuernos", en="Mira sus brazos", vol=.45),
]
