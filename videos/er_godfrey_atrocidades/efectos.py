# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Godfrey QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 19-nov-2026).
Molde: videos/er_sinluz_atrocidades/efectos.py (docs/estilo_secuencia_yt.md § REGLA DE ORO · PEGATINAS · MOTION GRAPHICS
NUEVOS · MAPAS) con el kit de Elden Ring (nucleo/mg_er.py) y los estilos de nucleo/peg_estilos.py (tema «er»):
- PEGATINAS reales (bajar_pegatinas.py; hoja previews/pegatinas_hoja.jpg). `godfrey` = `hoarah_loux` (misma imagen del Trono);
  `serosh` borroso → solo en camafeo chico; a pantalla, la captura `pantallas/serosh_carne.jpg` si existe.
  `rykard` y `zampaheces` copiadas de er_sinluz_atrocidades/pegatinas (mismas fuentes).
- COMENTARIOS reales (≤ 10 días): Ryans e Isaac (pidieron el tema) · críticas con contraburla: zzzz (Miquella), Moreno (la
  aguja), Nibald («con IA») · agradecen: Antonio, Esteban, Marcelo, Ulices, Ghost, Auren.
- FICHAS solo con citas en español verificadas (_investigacion/dossier.md: [EG]/[ES-wiki]). Los diálogos de Godfrey que solo
  están verificados en inglés NO van entre comillas: rótulos `puesto` con lo que dice la voz.
- MG NUEVOS (mg_er, 19-nov): `estandartes` (reinos tachados: p5, p5b, cierre), `gracia_perdida` (p5b ×2), `contencion`
  (Serosh = el freno: p1 ×2, p1b, p1c). Reusados: expediente (un cargo por puesto, sello en el n.º 1), linaje (p3 sin injertos;
  cierre con Godrick), subsuelo, cadena (grillete; Serosh cargándolo), acuerdo (la promesa de Márika, ×2, cabeceras nuevas),
  ecos (los tres ecos de Márika), domino (×3), triada, cien.
- MAPAS (mundo): Velo Tormentoso · Morne · Iglesia en llamas (ruta de conquistas) · Tercera iglesia → exilio por el mar ·
  Iglesia de la peregrinación · Picos (Primera iglesia → Forja) · prisión de Godefroy · Trono de Elden.
- PISTAS voz=True: «It's been a long while, Morgott» (p3b, post 4 s) y «Now I fight as Hoarah Loux! Warrior!» (p1b, post 7 s).
  FAB_FX_FINAL=1 python fab.py er_godfrey_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALAS TODAS)
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
FALTAN = []             # pantallas pedidas que aún no existen (se cubren con su alternativa)


def _hay(slug):
    return os.path.exists(_P(slug))


def _foto(*cands):
    """Primera imagen que exista: 'p:<pantalla>' o '<pegatina>'."""
    for c in cands:
        r = _P(c[2:]) if c.startswith("p:") else _G(c)
        if os.path.exists(r):
            return r
    return None


def pto(xy, nombre, foto=None, tipo=None):
    return (xy[0], xy[1], nombre, tipo, foto) if foto else (xy[0], xy[1], nombre, tipo)


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


def com(en, cid, dur=6.0, x=.30, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def sil(en, ruta, nombre=None, sub=None, dur=5.0, lado="izq", alto=880, encuadre=(0, .62)):
    """Personaje SIN FONDO a media pantalla, saliendo del borde, con la cara visible y el video corriendo detrás."""
    fn = PE.silueta(ruta, nombre, sub, alto=alto, encuadre=encuadre, lado=lado, tema=TEMA)
    x, y = PE.pos_silueta(fn, lado)
    return dict(tipo="mg", fn=fn, en=en, dur=dur, x=x, y=y, sale=.35, nombre="silueta " + os.path.basename(ruta), ver=1.4)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.24, y=.52, tam=520):
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


def aba(fotos, de, a, marcas, nombre, x=.50, y=.62, tam=290):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(slug, etiqueta ≤ 12 letras)]."""
    return dict(tipo="mg", fn=PE.abanico([(_G(s), t) for s, t in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="abanico " + nombre, ver=2.0)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0, alt=None):
    """Imagen REAL a pantalla completa (mg_wow.pantalla); si `slug` aún no existe, `alt` (otra pantalla que sí exista)."""
    if not _hay(slug):
        FALTAN.append(slug)
        slug = alt
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def pant_o(slug, de, a, otro, **kw):
    """Pantalla `slug` si existe; si no, el FX `otro` (pegatina/banda del mismo sujeto)."""
    if _hay(slug):
        return pant(slug, de, a, **kw)
    FALTAN.append(slug)
    return otro


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


def ban_p(de, a, arriba, titulo, nombre):
    """Rótulo `puesto` con inicio y fin anclados."""
    return mg(E.puesto(arriba, titulo), de, a, [], nombre, y=.80)


def mg(fn, de, a, marcas, nombre, y=.50, x=.5):
    return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.4, nombre="MG " + nombre, ver=5.0)


def msg(lineas, de, a, marcas, nombre, y=.76):
    """Mensaje del suelo (texto ámbar), para citas en español que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=y)


def cortado(de, a, sub, nombre):
    """Rótulo «CONTENIDO CORTADO» arriba (lo que no llegó al juego final se dice como tal y se marca en pantalla)."""
    return mg(E.puesto("Contenido cortado", sub), de, a, [], "cortado " + nombre, y=.10)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + (titulo or slug), ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + (titulo or slug), ver=4.0)


C_RYANS, C_ISAAC = "Ugzwx-gw60PNRP2_vWd4AaABAg", "UgxZoUME6H9uJQS-fNF4AaABAg"
C_ZZZZ, C_MORENO, C_NIBALD = "UgyXtVyD2QTVWCIUXV54AaABAg", "Ugx7sQm0LZRNNLTzeOd4AaABAg", "UgzFiKsLJKQSG1QpuBN4AaABAg"
C_ANTONIO, C_ESTEBAN = "UgzKl6SecxBZ18QuK2B4AaABAg", "Ugx0MBJdm3nLbTgw8R94AaABAg"
C_MARCELO, C_ULICES = "UgwnPzSkn0bVH27o1V14AaABAg", "UgwxGpGF9Z0ZX5q_gC14AaABAg"
C_GHOST, C_AUREN = "UgwdyniiCUm5KeFoVWZ4AaABAg", "UgwVQZoM7jzDuYINd7p4AaABAg"

# Coordenadas (fracción de mapas/mundo.jpg). Del molde (Godrick/Sinluz): Leyndell, Velo, Caelid, Picos. Medidas el 19-nov en
# recortes de mundo.jpg con rejilla, con la ubicación de la wiki inglesa (eldenring.fandom.com, API): Morne «southernmost point»
# · Iglesia de la peregrinación «northernmost point of the Weeping Peninsula» · Tercera iglesia «eastern Limgrave, just north
# of Mistwood» · Iglesia en llamas «border between Limgrave and Caelid» · Primera iglesia «northeastern Mountaintops,
# southeast of the Freezing Lake» · Forja «easternmost summit» (caldero rojo con cadenas) · prisión de Godefroy (Golden
# Lineage Evergaol) «south-westernmost point of Altus Plateau» (círculo de piedra al suroeste de la capital).
M_LEYND, M_VELO, M_CAEL, M_PICOS = (.48, .41), (.36, .70), (.60, .73), (.62, .23)
M_MORNE, M_PEREG, M_TERC, M_LLAMAS = (.413, .945), (.393, .843), (.457, .712), (.498, .710)
M_PRIMERA, M_FORJA, M_GODEF = (.700, .257), (.694, .325), (.406, .442)
M_PUENTE = (.432, .800)          # paso de Necrolimbo a la Península (Puente del Sacrificio)
M_FUERA = (.19, .965)            # flecha al borde: la Tierra Baldía y la guerra lejana están FUERA del mapa (dossier § 4)

CARGOS = ["Coleccionista de reinos", "Mandó a su pueblo a morir", "Padre ausente", "Acabó con los gigantes",
          "Rompió el cuello de Serosh"]


def expe(k, titulo_frase, dur=3.2):
    """Ficha del acusado al abrir el puesto k (0 = n.º 5): escribe el cargo k; en el n.º 1 cae el sello CULPABLE."""
    fin = (titulo_frase + "|fin", dur + (1.2 if k == 4 else 0))
    marcas = [(titulo_frase + "|fin", -.2)] + ([(titulo_frase + "|fin", 2.4)] if k == 4 else [])
    return mg(E.expediente(acusado="Godfrey", sub="primer Señor del Círculo", cargos=CARGOS[:k + 1], ya=k,
                           sello="CULPABLE" if k == 4 else None, titulo="Expediente del acusado"),
              (titulo_frase + "|fin", -.4), fin, marcas, f"expediente {k + 1}")


# Los 2 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026; cortes en sfx/, `post` en guion.py)
PISTAS = [
    dict(sfx="s_morgott", en="Es para su hijo. Escúchalo|fin", vol=1.0, voz=True),
    dict(sfx="s_hoarah", en="grita el nombre que tenía antes de ser rey. Escúchalo|fin", vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    sil("Primer Señor del Círculo", _G("godfrey"), "Godfrey", "primer Señor del Círculo", dur=4.8, lado="der",
        encuadre=(0, .55)),
    cam("Marido de la reina Márika", "marika", "Márika", dur=3.4, x=.16, y=.66),
    cam("padre de Godwyn", "godwyn", "Godwyn", dur=3.0, x=.16, y=.30, foco=(.5, .35, 1.6)),
    aba([("godrick", "Godrick"), ("godefroy", "Godefroy"), ("morgott", "Morgott"), ("mohg", "Mohg")],
        ("y abuelo de casi toda la familia", -.2), ("te pasaste el juego matando|fin", 1.0),
        [("y abuelo de casi toda la familia", 0), ("y abuelo de casi toda la familia", .5),
         ("que te pasaste el juego", 0), ("te pasaste el juego matando", .4)], "familia", tam=270),
    ban("el gran guerrero que vuelve a casa", _G("godfrey"), "Godfrey", "el que vuelve a casa", foco=(.5, .3, 2.0), dur=4.4),
    puesto("El que te llama valiente", "El que te llama", "Valiente", dur=3.4),
    rel(("en las descripciones de sus propias armas", -.4), "hacha_godfrey", "Hacha de Godfrey", dur=2.2),
    aba([("espadon_injertado", "Un clan"), ("talisman_hacha", "Un pueblo"), ("grillete_mohg", "Dos hijos"),
         ("recuerdo_gigante", "Una especie")],
        ("hay un clan entero borrado", -.2), ("una especie entera que ya no existe|fin", .8),
        ["hay un clan entero borrado", "un pueblo mandado a morir lejos", "dos hijos encerrados", "y una especie entera que"],
        "lo que esconden", tam=280),
    puesto("Y la número uno la comete delante", "La número uno", "Delante de ti", dur=3.2),
    pant("trono_elden", ("en el último combate del juego", -.3), ("en el último combate del juego|fin", 3.6),
         alt="leyndell_ceniza", zoom=(1.0, 1.12)),
    cam("esquivando el hacha", "hacha_godfrey", "El hacha", dur=3.6, x=.84, y=.66, foco=(.66, .25, 2.0)),   # la hoja, no el mango
    com("Ryans lo pidió en un comentario", C_RYANS, dur=6.4),
    com("E Isaac pidió la tragedia de Godwyn", C_ISAAC, dur=6.4, x=.70, y=.36),
    grande("Godwyn tendrá su turno", "godwyn", "Godwyn el Dorado", lado="izq", dur=4.0, tam=600),
    ban_p(("Hoy toca el padre", -.1), ("mucho más que esconder|fin", 1.0), "Hoy toca el padre", "Mucho más que esconder",
          "el padre"),
    puesto("Antes de empezar, una corrección", "Antes de empezar", "Una corrección", dur=2.8),
    com("En el video de Miquella alguien escribió", C_ZZZZ, dur=6.6),
    cam("la mejor waifu del gaming", "miquella", "Miquella", dur=3.6, x=.84, y=.66),
    puesto("Ella es él", "Miquella", "Es un chico", dur=4.0),
    ban("es justo su poder, el encanto", _G("miquella"), "Miquella", "el encanto", foco=(.45, .50, 1.2), dur=4.4),   # la silueta perdía la cara
    ban_p(("Te alcanzó a ti también", -.1), ("a través de la pantalla|fin", 1.0), "Te alcanzó", "A través de la pantalla",
          "pantalla"),

    # ================================================================ 5 · EL COLECCIONISTA DE REINOS
    puesto("Número cinco", "Atrocidad número 5", "El coleccionista de reinos"),
    expe(0, "El coleccionista de reinos", dur=2.6),
    cam(("se acuerda de Godrick", 1.0), "godrick", "Godrick", dur=3.0, x=.16, y=.66),   # tras el expediente (no encima)
    mapa("mundo", [pto(M_VELO, "Velo Tormentoso", _foto("p:velo"), "meta")],
         ("en el Castillo de Velo Tormentoso", -.3), ("el primer gran castillo del juego|fin", .6),
         ["en el Castillo de Velo Tormentoso"], titulo="Colina Tormentosa", sub="Castillo de Velo Tormentoso", ventana=True,
         x=.70, y=.40, entrada="desenrolla", traza=99),
    ban_p(("Lo que nadie se pregunta", -.1), ("antes de que llegaran los dorados|fin", 1.0), "De quién era",
          "Antes de los dorados", "de quien era"),
    rel("La corona de Godfrey lo cuenta", "corona_senor", "Corona de Señor del Círculo", dur=5.0),
    ficha("La corona de Godfrey lo cuenta", "Corona de Señor del Círculo", "La era del Árbol Áureo empezó en mitad de un "
          "enfrentamiento, cuando Godfrey era el señor de la Batalla. […] *Se enfrentó solo al señor de la Tormenta*.",
          tipo="Yelmo", icono="corona_senor", a=("Se enfrentó solo al señor de la Tormenta|fin", 1.0)),
    mg(E.estandartes(["Su nombre", "Su cara", "Su tumba"], remate="Solo se sabe quién lo venció",
                     titulo="Lo que queda del señor de la Tormenta"),
       ("Del señor de la Tormenta no queda nada", -.2), ("es quién lo venció|fin", 1.2),
       ["no queda su nombre", "no queda su cara", "ni siquiera una tumba", "Lo único que se sabe de él"], "nada"),
    pant("retrato_velo", ("todavía cuelga un retrato enorme", -.3), ("encima de la chimenea|fin", .5), alt="velo",
         zoom=(1.0, 1.12)),
    cam("con el león Serosh a la espalda", "serosh", "Serosh", dur=4.0, x=.84, y=.40, foco=(.5, .4, 1.4)),
    ban_p(("Es como entrar en la casa de alguien", -.1), ("encima de la chimenea|fin", .4), "Encima de la chimenea",
          "El retrato del invasor", "chimenea"),
    rel("Hasta los halcones lo recuerdan", "cenizas_halcon_rey", "Cenizas de un halcón", "venerado como soberano", dur=5.4),
    ban_p(("los vientos de Velo Tormentoso todavía", -.1), ("rugían como ningún otro|fin", 1.0), "Velo Tormentoso",
          "Vientos que rugían", "vientos"),
    mg(E.estandartes(["Velo Tormentoso", "Señor de la Tormenta"], remate="El único que se le enfrentó lleva corona",
                     titulo="Reinos conquistados"),
       ("Hoy esos vientos ya no rugen", -1.2), ("lleva corona|fin", 1.4),
       ["Hoy esos vientos ya no rugen", "quién calló la tormenta", "lleva corona"], "reinos 1"),

    # ---- 5b · Morne y la gracia
    mapa("mundo", [pto(M_VELO, "Velo Tormentoso", None, "inicio"), M_PUENTE,
                   pto(M_MORNE, "Castillo de Morne", _foto("p:morne"), "meta")],
         ("Y luego está la Península del Llanto", -.3), ("con una espada clavada|fin", .6),
         ["Y luego está la Península", "Al sur, el Castillo de Morne"], titulo="Península del Llanto",
         sub="Castillo de Morne", entrada="mesa", traza=99),
    pant("monumento_morne", ("Su inscripción dice así", -.3), ("en manos del señor Godfrey|fin", .6), alt="morne",
         zoom=(1.42, 1.48), pan=(0, -1, .2, -1)),          # recorta el texto en inglés del mensaje (abajo)
    ficha("Su inscripción dice así", "Monumento de espada", "El asedio al castillo de Morne: un héroe solitario lucha en "
          "busca de venganza, *solo para terminar en manos del señor Godfrey*.", tipo="Castillo de Morne",
          a=("en manos del señor Godfrey|fin", 1.0)),
    puesto("Venganza de qué", "¿Venganza", "De qué?", dur=3.4),
    rel("en la espada más famosa de Morne", "espadon_injertado", "Espadón de hoja injertada", dur=5.6),
    ficha("Arma de vengador que carga", "Espadón de hoja injertada", "La famosa espada del Castillo de Morne. Arma de "
          "vengador que carga con océanos de ira y arrepentimiento. […] Un solitario campeón, superviviente de un país "
          "desaparecido, mostró tal determinación a la hora de seguir luchando que *reclamó las espadas de todo un clan de "
          "guerreros*.", tipo="Espadón", icono="espadon_injertado", a=("de todo un clan de guerreros|fin", 1.0)),
    mg(E.estandartes(["Velo Tormentoso", "Señor de la Tormenta", "País de Morne", "Clan de guerreros"], ya=2,
                     remate="En manos del señor Godfrey", titulo="Reinos conquistados"),
       ("Un país que desapareció", -.4), ("terminó en manos del señor Godfrey|fin", 1.4),
       ["Un país que desapareció", "y un clan entero de guerreros", "terminó en manos del señor Godfrey"], "reinos 2"),
    sil("la empuña el Bastardo leonino", _G("bastardo_leonino"), "Bastardo leonino", "el jefe del castillo", dur=5.2,
        lado="izq", encuadre=(0, .5)),
    puesto("se llama Juramento de venganza", "Habilidad del arma", "Juramento de venganza", dur=2.6),
    ban_p(("El juramento sigue en pie", -.1), ("El clan, no|fin", 1.4), "El juramento sigue en pie", "El clan, no", "clan no"),
    mg(E.gracia_perdida(["Señor de la Tormenta", "El clan de Morne", "Su último enemigo"],
                        remate="Se desvaneció el color de sus ojos"),
       ("Y aquí está lo que casi nadie lee", -.2), ("se desvaneció el color de sus ojos|fin", 1.4),
       ["Cuándo pierde Godfrey la gracia", "Su corona lo dice", "cayó su último enemigo", "Fue en ese instante",
        "se desvaneció el color de sus ojos"], "gracia 1"),
    mapa("mundo", [pto(M_VELO, "Velo Tormentoso", None, "inicio"), M_PUENTE, pto(M_MORNE, "Castillo de Morne"), M_PUENTE,
                   pto(M_LLAMAS, "Iglesia en llamas", _foto("p:monumento_caelid"), "meta")],
         ("No la pierde por una derrota", -.3), ("Un monumento en la frontera de Caelid lo confirma|fin", .3),
         ["No la pierde por una derrota", ("No la pierde por una derrota|fin", .2), "Un monumento en la frontera de Caelid"],
         titulo="El fin de la campaña", sub="Frontera de Caelid", entrada="foco", traza=99),
    msg(["Sus ejércitos dorados permanecen", "invencibles e incólumes."], ("sus ejércitos dorados permanecen", -.1),
        ("permanecen invencibles e incólumes|fin", 1.6), ["sus ejércitos dorados", "invencibles e incólumes"], "incolumes"),
    mg(E.gracia_perdida(["Señor de la Tormenta", "El clan de Morne", "Su último enemigo"],
                        remate="Ya no le queda nadie a quien matar", titulo="La gracia en sus ojos"),
       ("La pierde cuando ya no le queda", -.3), ("nadie a quien matar|fin", 1.6),
       [("La pierde cuando ya no le queda", -.3)] * 3 + [("La pierde cuando ya no le queda", .2), "nadie a quien matar"],
       "gracia 2"),
    rel("llevaban en la frente la Cinta de campeón", "cinta_campeon", "Cinta de campeón", dur=4.6),
    ficha("Prueba de que el portador", "Cinta de campeón", "Cinta reservada para los más valientes de Tierra Baldía. *Prueba "
          "de que el portador ha asesinado a innumerables enemigos*. Siguiendo el ejemplo de su líder, Hoarah Loux, los "
          "valientes guerreros de Tierra Baldía evitan cualquier adorno adicional.", tipo="Yelmo", icono="cinta_campeon",
          a=("su líder, Hoarah Loux|fin", .8)),
    cam("su líder, Hoarah Loux", "hoarah_loux", "Hoarah Loux", dur=3.6, x=.16, y=.66),
    ban_p(("El ejemplo era él", -.1), ("El ejemplo era él|fin", 1.2), "El ejemplo", "Era él", "ejemplo"),
    msg(["Intenta suscribirte."], ("Si te sorprendió que el primer rey", -.1),
        ("por quedarse sin víctimas, suscríbete|fin", .6), ["Si te sorprendió"], "suscribete 1"),
    puesto("Lo que viene después es peor", "Lo que viene", "Es peor", dur=3.4),

    # ================================================================ 4 · LA LARGA MARCHA
    puesto("Número cuatro", "Atrocidad número 4", "La Larga Marcha"),
    expe(1, "La Larga Marcha de los Sinluz", dur=2.0),
    mg(E.triada([("Sin gracia", "por qué no la tienes"), ("Sinluz", "por qué te llaman así"),
                 ("Vuelves", "cada vez que mueres")], titulo="¿Por qué eres un Sinluz?"),
       ("Alguna vez te preguntaste por qué", 1.4), ("cada vez que mueres|fin", 1.0),
       ["Por qué no tienes la gracia", "por qué te llaman así", "y por qué vuelves cada vez"], "por que sinluz"),
    cam("pregúntale a Godfrey", "godfrey", "Godfrey", dur=3.8, x=.84, y=.66),
    mapa("mundo", [pto(M_TERC, "Tercera iglesia de Márika", _foto("p:tercera_iglesia"), "meta")],
         ("En Necrolimbo, en la Tercera iglesia", -.3), ("Melina te deja oír un eco", -.3),
         ["en la Tercera iglesia de Márika"], titulo="Necrolimbo", sub="Tercera iglesia de Márika", ventana=True,
         x=.30, y=.40, entrada="pliegue", traza=99),
    sil("Melina te deja oír un eco", _G("melina"), "Melina", "la voz de los ecos", dur=5.0, lado="der", encuadre=(0, .5)),
    mg(E.ecos(["Mi señor. Os despojo a ti y a tus hombres de la Gracia.",
               "Con la mirada teñida de oscuro, seréis expulsados de las Tierras Intermedias.",
               "Guerrearéis en una tierra lejana,", "donde viviréis y moriréis."], firma="la reina Márika",
              titulo="Eco de la Tercera iglesia", h=700),
       ("Mi señor. Os despojo", -.3), ("donde viviréis y moriréis|fin", 1.4),
       ["Mi señor. Os despojo", "Con la mirada teñida de oscuro", "Guerrearéis en una tierra lejana",
        "donde viviréis y moriréis"], "eco destierro"),
    puesto("No es solo él", "No es solo él", "Son él y sus hombres", dur=3.8),
    rel("El Recuerdo de Hoarah Loux lo confirma", "recuerdo_hoarah", "Recuerdo de Hoarah Loux", dur=5.0),
    ficha("El Recuerdo de Hoarah Loux lo confirma", "Recuerdo de Hoarah Loux", "Cuando Godfrey, primer Señor del Círculo, "
          "fue despojado de su Gracia y se transformó en un Sinluz, *abandonó las Tierras Intermedias en compañía de los "
          "suyos*.", tipo="Recuerdo", icono="recuerdo_hoarah", a=("en compañía de los suyos|fin", 1.0)),
    puesto("Y los suyos lo siguieron sin una queja", "Los suyos", "Sin una queja", dur=3.0),
    peg("El Talismán con hacha cuenta", "talisman_hacha", "Talismán con hacha", dur=4.8, x=.20, y=.60, tam=420),
    ficha("El Talismán con hacha cuenta", "Talismán con hacha", "El señor que lideró la Larga Marcha portaba un hacha *y sus "
          "leales guerreros le rindieron homenaje portando una ellos también*…", tipo="Talismán", icono="talisman_hacha",
          a=("portando una ellos también|fin", 1.0)),
    mapa("mundo", [pto(M_TERC, "Tercera iglesia de Márika", None, "inicio"), (.40, .86), (.30, .93),
                   pto(M_FUERA, "Una tierra lejana", None, "meta")],
         ("Un pueblo entero que se va", -.3), ("nadie a quien matar en esta|fin", .5),
         ["Un pueblo entero que se va", "a morir allí"], titulo="La Larga Marcha", sub="Más allá del mar",
         entrada="foco", traza=99),
    ban_p(("Y a ellos nadie les preguntó", -.1), ("nadie les preguntó nada|fin", 1.4), "Y a ellos",
          "Nadie les preguntó nada", "nadie pregunto"),

    # ---- 4b · la promesa
    mapa("mundo", [pto(M_TERC, "Tercera iglesia", None, "inicio"), M_PUENTE,
                   pto(M_PEREG, "Iglesia de la peregrinación", _foto("p:iglesia_peregrinacion"), "meta")],
         ("Pero el eco tiene una segunda parte", -.3), ("Márika les hace una promesa|fin", .6),
         ["Pero el eco tiene una segunda parte", "En la Iglesia de la peregrinación"], titulo="Península del Llanto",
         sub="Iglesia de la peregrinación", ventana=True, x=.70, y=.40, entrada="desenrolla", traza=99),
    mg(E.ecos(["Tras vuestra muerte, os devolveré lo que un día quise para mí.",
               "Regresaréis a las Tierras Intermedias, guerrearéis y blandiréis el Círculo de Elden.",
               "Fortaleceos ante la amenaza de la muerte, guerreros de mi señor Godfrey."], firma="la reina Márika",
              titulo="Eco de la Iglesia de la peregrinación", h=700),
       ("Tras vuestra muerte", -.3), ("guerreros de mi señor Godfrey|fin", 1.2),
       ["Tras vuestra muerte", "Regresaréis a las Tierras Intermedias", "Fortaleceos ante la amenaza"], "eco promesa"),
    mg(E.acuerdo(["Volver tras la muerte", "Blandir el Círculo de Elden"], "Morir, volver y pelear otra vez",
                 letra="Un contrato de guerra sin fecha de fin", titulo="La promesa de Márika", remate="Sin fin",
                 cab=("Ella os da", "Vosotros pagáis")),
       ("Léelo otra vez", -.3), ("sin fecha de fin|fin", .3),
       [("Léelo otra vez", 0), ("Léelo otra vez|fin", .4), "Primero morís", "Eso no es un premio", "sin fecha de fin"],
       "promesa"),
    rel("Hasta el Ancla oxidada guarda", "ancla_oxidada", "Ancla oxidada", dur=5.0),
    ficha("Hasta el Ancla oxidada guarda", "Ancla oxidada", "Cuando los Sinluz salieron de las Tierras Intermedias con su "
          "señor, *dicen que solo quedó un único barco*.", tipo="Gran martillo", icono="ancla_oxidada",
          a=("solo quedó un único barco|fin", 1.0)),
    peg("Su hacha se rompió en la batalla", "hacha_godfrey", "Hacha de Godfrey", dur=4.6, x=.20, y=.60, tam=420),
    ficha("Su hacha se rompió en la batalla", "Hacha de Godfrey", "Arma de Godfrey, Señor del Círculo. *Se rompió en el "
          "curso de la batalla que libró como líder de los Sinluz durante la Larga Marcha*.", tipo="Gran hacha",
          icono="hacha_godfrey", a=("como líder de los Sinluz|fin", .8)),
    cam("renunció a la corona", "corona_senor", "La corona", dur=4.2, x=.16, y=.30, foco=(.5, .5, 1.3)),
    ban_p(("renunció a la corona", -.1), ("un simple guerrero|fin", 1.2), "Renunció a la corona", "Un simple guerrero",
          "simple guerrero"),
    pant_o("intro_hoarah", ("la intro lo nombra entre los muertos", -.3), ("entre los muertos que vuelven|fin", .2),
           ban("la intro lo nombra entre los muertos", _G("hoarah_loux"), "Hoarah Loux", "en la intro del juego",
               foco=(.5, .3, 2.0), dur=4.6)),
    puesto("Hoarah Loux, el caudillo", "Hoarah Loux", "Caudillo de la Tierra Baldía", dur=3.6),
    msg(["Alzaos, Sinluz, es el momento.", "Vosotros que habéis muerto,", "pero vivís."], ("Alzaos, Sinluz", -.1),
        ("pero vivís|fin", .3), ["Alzaos, Sinluz", "Vosotros que habéis muerto", "pero vivís"], "alzaos", y=.66),
    mg(E.acuerdo(["Volver tras la muerte", "Blandir el Círculo de Elden"], "Morir, volver y pelear",
                 letra="Un contrato de guerra sin fecha de fin", titulo="Tu parte del trato", remate="Para siempre",
                 cab=("Ella os da", "Vosotros pagáis")),
       ("Ahí está la atrocidad que ignoraste", -.2), ("Para siempre|fin", 1.4),
       [("Ahí está la atrocidad que ignoraste", 0), ("Ahí está la atrocidad que ignoraste", .2),
        ("Ahí está la atrocidad que ignoraste", .4), "Tú eres parte de ese trato", "Morir, volver y pelear"], "tu parte"),
    com("Antonio escribió que está suscrito", C_ANTONIO, dur=3.8),
    com("Y Esteban dice que le encanta", C_ESTEBAN, dur=6.4, x=.70, y=.36),
    ban_p(("Todos se leen, uno por uno", -.1), ("se decide lo que viene|fin", 1.0), "Todos se leen", "Uno por uno",
          "uno por uno"),

    # ================================================================ 3 · PADRE DEL AÑO
    puesto("Número tres", "Atrocidad número 3", "Padre del año"),
    expe(2, "Padre del año", dur=2.0),
    mg(E.linaje(raiz=("Godfrey y Márika", "el rey y la reina"), hijos=(("Godwyn", "el Dorado"), ("Morgott", "gemelo"),
                                                                        ("Mohg", "gemelo")),
                medio="sus hijos", remate="Los gemelos nacieron augurios: malditos", titulo="Los hijos del rey",
                injertos=()),
       ("Godfrey y Márika tuvieron hijos", 1.8), ("nacer augurio es nacer maldito|fin", 1.0),
       ["Godfrey y Márika tuvieron hijos", ("Godfrey y Márika tuvieron hijos|fin", .2), "Godwyn el Dorado",
        "dos gemelos, Morgott", ("dos gemelos, Morgott y Mohg|fin", -.2), "Los gemelos nacieron augurios"], "hijos"),
    pant("subsuelo", ("Un muñeco que encuentras en el Subsuelo", -.3), ("lo explica sin rodeos|fin", .4), alt="subsuelo_wiki"),
    rel("Un muñeco que encuentras en el Subsuelo", "parvulo", "Párvulo maldito", dur=5.0),
    ficha("A los hijos de los augurios se les", "Párvulo maldito", "A los hijos de los augurios se les extirpan los cuernos, "
          "*por lo que la mayoría perecen*. Estos amuletos se confeccionan en su recuerdo.", tipo="Objeto",
          icono="parvulo", a=("por lo que la mayoría perecen|fin", 1.2)),
    msg(["Por favor, te ruego", "que no me odies ni me maldigas."], ("la súplica de un niño", -.1),
        ("ni me maldigas|fin", .2), ["por favor, te ruego", "que no me odies"], "no me odies"),
    ban_p(("Pero los gemelos no eran hijos", -.1), ("Eran hijos del rey|fin", 1.0), "No eran hijos de cualquiera",
          "Eran hijos del rey", "hijos del rey"),
    rel("el Párvulo maldito de la realeza", "parvulo_realeza", "Párvulo maldito de la realeza", dur=5.0),
    ficha("A los hijos de augurios nacidos en la realeza", "Párvulo maldito de la realeza", "A los hijos de augurios nacidos "
          "en la realeza no se les extirpan los cuernos, sino que *se los oculta bajo tierra* sin que nadie lo sepa, "
          "*encarcelados para toda la eternidad*.", tipo="Objeto", icono="parvulo_realeza",
          a=("encarcelados para toda la eternidad|fin", .8)),
    mg(E.subsuelo(arriba="Leyndell, capital del Reino", abajo="Subsuelo de los marginados", sello="Para toda la eternidad",
                  remate="Bajo el trono de su padre", titulo="Lo que hay debajo del trono"),
       ("Bajo la capital. Bajo el trono", -.3), ("Bajo el trono de su padre|fin", .1),
       [("Bajo la capital. Bajo el trono", -.2), ("Bajo la capital. Bajo el trono", .4), "Bajo el trono de su padre",
        ("Bajo el trono de su padre|fin", 0)], "debajo del trono"),
    peg("Y el Grillete de Mohg dice", "grillete_mohg", "Grillete de Mohg", dur=4.4, x=.12, y=.16, tam=300),
    mg(E.cadena(["Un amuleto", "Bañado en magia dorada", "Confinamiento muy estricto"], preso="Mohg",
                amo="La familia dorada", remate="Magia dorada: el color de la familia", titulo="El Grillete de Mohg"),
       ("Y el Grillete de Mohg dice|fin", .1), ("El color de la familia|fin", 1.4),
       ["un amuleto bañado", "bañado en magia dorada", "un confinamiento muy estricto", "El color de la familia"],
       "grillete", y=.56),

    # ---- 3b · dónde estaba el padre
    puesto("quién firmó esa orden", "El juego no dice", "Quién firmó la orden", dur=3.8),
    cam("Ni Godfrey ni Márika aparecen", "godfrey", "Godfrey", dur=4.4, x=.16, y=.40),
    cam("ni Márika aparecen con la pluma", "marika", "Márika", dur=4.0, x=.84, y=.40),
    puesto("dónde estaba el padre", "Lo que sí se sabe", "Dónde estaba el padre", dur=3.6),
    mg(E.domino(["De campaña", "En el exilio", "Sus hijos, en las cloacas"], titulo="Dónde estaba el padre"),
       ("De campaña, matando", -.2), ("de su propia capital|fin", 1.0),
       ["De campaña, matando", "en el exilio, al otro lado", "Mientras sus hijos crecían"], "donde estaba"),
    sil("Morgott salió de ahí abajo", _G("morgott"), "Morgott", "rey de los augurios", dur=5.4, lado="der", encuadre=(0, .5)),
    pant("leyndell", ("Defendió el Árbol Áureo y la capital", -.3), ("toda la ausencia de su padre|fin", .3)),
    rel("Su recuerdo lo dice: jamás", "recuerdo_augurios", "Recuerdo del rey de los Augurios", dur=4.8),
    ficha("Su recuerdo lo dice: jamás", "Recuerdo del rey de los Augurios", "Pese a haber nacido como un augurio más sin la "
          "Gracia, Morgott decidió convertirse en el protector del Árbol Áureo. *Jamás recibió ninguna muestra de afecto por "
          "ello, pero aun así, él amó*.", tipo="Recuerdo", icono="recuerdo_augurios", a=("pero aun así, él amó|fin", 1.2)),
    ban_p(("Y a quién mataba Morgott", -.1), ("A los Sinluz que volvían|fin", .6), "A quién mataba Morgott",
          "A los Sinluz que volvían", "mataba morgott"),
    cam("La gente de su padre", "godfrey", "Su padre", dur=3.8, x=.84, y=.40),
    puesto("La gente de su padre", "Eran", "La gente de su padre", dur=2.0),      # antes de la silueta de Mohg
    sil("Su gemelo Mohg tomó el otro camino", _G("mohg"), "Mohg", "Señor de la Sangre", dur=2.6, lado="izq",
        encuadre=(0, .5)),
    rel("Su Gran Runa lo dice", "runa_mohg", "Gran Runa de Mohg", dur=5.0),
    ficha("Su Gran Runa lo dice", "Gran Runa de Mohg", "Mohg y Morgott eran gemelos, por lo que sus grandes runas son "
          "similares. No obstante, *la runa de Mohg está empapada en sangre maldita*, desde su devoción por el condenado "
          "lodazal en el que nació…", tipo="Gran Runa", icono="runa_mohg", a=("el condenado lodazal en el que nació|fin", .6)),
    aba([("morgott", "El reino"), ("mohg", "La sangre")], ("Uno amó al reino", -.2), ("a adorar la sangre|fin", 1.2),
        ["Uno amó al reino", "El otro se fue"], "gemelos", tam=330),
    pant("trono_elden", ("Cuando Godfrey por fin regresa", -.3), ("Lo mataste tú|fin", .3),    # 19-nov: la cinemática real
         alt="leyndell_ceniza", zoom=(1.0, 1.12)),                                                # (083-084) queda a la vista
    cam("Morgott ya está muerto", "morgott", "Morgott", dur=3.6, x=.16, y=.40),
    puesto("Lo mataste tú", "Morgott ya está muerto", "Lo mataste tú", dur=3.4),
    cam("no es para Márika", "marika", "Márika", dur=3.0, x=.84, y=.66),
    puesto("Es para su hijo. Escúchalo|fin", "Su primera frase", "Para Morgott", dur=4.4),

    # ---- 3c · ni un perdón; la aguja
    ban("Hace mucho tiempo, Morgott", _G("godfrey"), "Godfrey", "de vuelta en el trono", foco=(.5, .3, 2.0), dur=3.6),
    ban_p(("Eso es todo. Ni un perdón", -.1), ("por guardarle la casa|fin", 1.0), "Ni un perdón", "Ni un gracias", "perdon"),
    cortado(("En los archivos del juego quedó", -.1), ("La cortaron|fin", 1.2), "Perdóname, Morgott", "perdoname"),
    cam("que nunca llegó a la versión final", "morgott", "Morgott", dur=4.4, x=.16, y=.66),
    puesto("también está la Llama Frenética", "Bajo la capital", "La Llama Frenética", dur=3.8),
    com("Moreno nos corrigió", C_MORENO, dur=7.6),
    ban_p(("Moreno, en una cosa sí tienes", -.1), ("No se puede en cualquier sitio|fin", 1.0), "Tienes razón",
          "No en cualquier sitio", "cualquier sitio"),
    rel("La Aguja de Miquella solo funciona", "aguja_miquella", "Aguja de Miquella", "en Farum Azula", dur=6.0),
    ban_p(("Ahí, sí se puede", -.1), ("Ahí, sí se puede|fin", 1.4), "En Farum Azula", "Sí se puede", "si se puede"),
    ban_p(("Lo sabe todo el que la usó", -.1), ("tienen los ojos amarillos|fin", 1.2), "Los demás",
          "Siguen con ojos amarillos", "ojos amarillos"),

    # ================================================================ 2 · ACABA CON LOS GIGANTES
    puesto("Número dos", "Atrocidad número 2", "Acaba con los gigantes"),
    expe(3, "Acaba con los gigantes"),
    pant("picos", ("Al noreste del mapa, en los Picos", -.3), ("los dueños ya no están|fin", .4), zoom=(1.0, 1.14)),
    puesto("Es porque los dueños ya no están", "Los Picos de los gigantes", "Sin sus dueños", dur=3.6),
    mapa("mundo", [pto(M_PRIMERA, "Primera iglesia de Márika", _foto("p:primera_iglesia"), "meta")],
         ("En la Primera iglesia de Márika", -.3), ("Esta vez es una orden|fin", .4), ["En la Primera iglesia de Márika"],
         titulo="Picos de los gigantes", sub="Primera iglesia de Márika", ventana=True, x=.70, y=.40, entrada="mesa",
         traza=99),
    mg(E.ecos(["Recuérdalo, mi señor Godfrey. Elogiamos tus actos.",
               "Acaba con los gigantes con tu espada",
               "y confina la llama en lo alto de la montaña.",
               "Permite que empiece una nueva era.", "Una era rebosante de vida."], firma="la reina Márika",
              titulo="Eco de la Primera iglesia", h=720),
       ("Recuérdalo, mi señor Godfrey", -.3), ("Una era rebosante de vida|fin", 1.0),
       ["Recuérdalo, mi señor Godfrey", "Acaba con los gigantes con tu espada", "y confina la llama",
        "Permite que empiece", "Una era rebosante de vida"], "eco gigantes"),
    ban_p(("que empieza acabando con una especie", -.1), ("que empieza acabando con una especie entera|fin", 1.0),
          "Una era rebosante de vida", "Acabando con una especie", "especie"),
    rel("Su corona lo resume en una línea", "corona_senor", "Corona de Señor del Círculo", dur=5.0),
    ficha("Su corona lo resume en una línea", "Corona de Señor del Círculo", "La era del Árbol Áureo empezó en mitad de un "
          "enfrentamiento, cuando Godfrey era el señor de la Batalla. *Lideró la guerra contra los gigantes*.",
          tipo="Yelmo", icono="corona_senor", a=("lideró la guerra contra los gigantes|fin", 1.2)),
    rel("El Medallón de rugido dice", "medallon_rugido", "Medallón de rugido", dur=5.0),
    ficha("El Medallón de rugido dice", "Medallón de rugido", "En la antigüedad, *los gigantes eran enemigos mortales del "
          "Árbol Áureo*. Sus bramidos desolaban la naturaleza, provocaban avalanchas y azuzaban tormentas de fuego.",
          tipo="Talismán", icono="medallon_rugido", a=("enemigos mortales del Árbol Áureo|fin", .5)),
    peg("Y el Aplastagigantes, un martillo", "aplastagigantes", "Aplastagigantes", dur=5.0, x=.20, y=.60, tam=440),
    ficha("Y el Aplastagigantes, un martillo", "Aplastagigantes", "Gran martillo fabricado a partir de un pedrusco y usado en "
          "la guerra contra los gigantes. […] *Después de que los gigantes desaparecieran* para dar paso a las guerras de "
          "los hombres, esta arma cayó en el olvido.", tipo="Gran martillo", icono="aplastagigantes",
          a=("para dar paso a las guerras de los hombres|fin", .8)),
    ban_p(("Desaparecieran#2", -.1), ("Esa es la palabra que eligió el juego|fin", 1.0), "La palabra que eligió el juego",
          "Desaparecieran", "desaparecieran"),
    pant_o("zamor", ("Los caballeros de Zamor fueron", -.3), ("enemigos jurados de los gigantes de fuego|fin", .4), None,
           zoom=(1.08, 1.0)),                               # si no hay captura de las ruinas, solo la reliquia
    rel("Los caballeros de Zamor fueron", "armadura_zamor", "Armadura de Zamor", dur=5.0),
    puesto("enemigos jurados de los gigantes", "Caballeros de Zamor", "Enemigos de los gigantes", dur=3.6),
    rel("hasta un escudo con un rostro espantoso", "escudo_rostro", "Escudo de rostro", dur=5.2),
    ficha("hasta un escudo con un rostro espantoso", "Escudo de rostro", "El espantoso rostro y las llamas ardientes tienen "
          "como objetivo *recordar el horror que supone enfrentarse a un gigante de fuego*. De cierta forma, este escudo "
          "tiene una función instructiva.", tipo="Escudo", icono="escudo_rostro",
          a=("por qué había que exterminarlos|fin", .6)),
    pant("gigantes_empalados", ("Cuando subes hacia la Forja", -.3), ("atravesados por estacas|fin", .8), alt="picos",
         zoom=(1.12, 1.0)),
    mapa("mundo", [pto(M_PRIMERA, "Primera iglesia de Márika", None, "inicio"), (.70, .29),
                   pto(M_FORJA, "Forja de los gigantes", _foto("p:forja_gigantes", "gigante_fuego"), "meta")],
         ("Nadie te dice quién los clavó", -.3), ("quién dirigía esa guerra|fin", 1.2),
         ["Nadie te dice quién los clavó", "Pero ya sabes quién dirigía"], titulo="Contra los gigantes",
         sub=None, entrada="pliegue", traza=99),

    # ---- 2b · el último gigante; los troles
    grande("El Gigante de fuego, el jefe", "gigante_fuego", "Gigante de fuego", lado="der", dur=5.0, tam=620),
    rel("Su recuerdo dice que es un superviviente", "recuerdo_gigante", "Recuerdo del gigante de fuego", dur=5.0),
    ficha("Su recuerdo dice que es un superviviente", "Recuerdo del gigante de fuego", "*El gigante de fuego es un "
          "superviviente de la guerra contra los gigantes*. Al constatar que las llamas de su forja jamás podrían "
          "extinguirse, la reina Márika lo maldijo.", tipo="Recuerdo", icono="recuerdo_gigante",
          a=("la reina Márika lo maldijo|fin", .6)),
    msg(["Oh, insignificante gigante,", "deberás custodiar tu llama", "por toda la eternidad."],
        ("Oh, insignificante gigante", -.1), ("custodiar tu llama por toda la eternidad|fin", 1.4),
        ["Oh, insignificante gigante", "deberás custodiar tu llama", "por toda la eternidad"], "custodiar", y=.66),
    mg(E.domino(["Mataron a su pueblo", "Al último, de guardia", "Subes y lo matas", "Su llama quema el Árbol"],
                titulo="Ni eso le dejaron"),
       ("Mataron a su pueblo", -.2), ("Ni eso le dejaron|fin", 1.2),
       ["Mataron a su pueblo", "y al último lo dejaron vivo", "Y luego subes tú", "y usas su llama"], "ni eso"),
    pant("monumento_gigantes", ("Y dentro de esa guerra hubo otra", -.3), ("empieza la era del Árbol Áureo|fin", 1.2),
         alt="gigantes_empalados", zoom=(1.0, 1.10)),
    puesto("Junto a la Tumba del héroe matagigantes", "Picos de los gigantes", "Un monumento con espada", dur=4.0),
    mg(E.domino(["Los campeones combaten", "Los troles traicionan", "El fuego es vencido", "Empieza la era del Árbol"],
                titulo="La guerra contra los gigantes, en tres líneas"),
       ("los campeones combaten", -.3), ("empieza la era del Árbol Áureo|fin", 1.2),
       ["los campeones combaten", "los troles traicionan", "el fuego es vencido", "y empieza la era del Árbol"],
       "tres lineas"),
    sil("Los troles descienden de los gigantes", _G("troll"), "Trol", "gigante menor", dur=5.0, lado="izq", encuadre=(0, .5)),
    rel("la Espada dorada de trol", "espada_trol", "Espada dorada de trol", dur=5.0),
    ficha("Espada entregada a los gigantes menores", "Espada dorada de trol", "Espada entregada a los gigantes menores que "
          "lucharon por el Árbol Áureo durante la guerra contra los gigantes. Aunque hayan perdido la cordura, en ningún "
          "momento se separan de sus espadas, cuyo estado actual es lamentable *al haberse desconchado su chapado en oro*.",
          tipo="Espada colosal", icono="espada_trol", a=("su chapado en oro|fin", .8)),
    ban_p(("Chapado en oro. Ni siquiera", -.1), ("Ni siquiera era oro de verdad|fin", 1.0), "Chapado en oro",
          "Ni siquiera era oro", "oro"),
    cam("por una espada con baño dorado", "espada_trol", "Baño dorado", dur=4.0, x=.84, y=.40, foco=(.5, .5, 1.3)),
    ban_p(("vagan por los caminos sin cordura", -.1), ("sin cordura, sin soltarla|fin", 1.4), "Sin cordura",
          "Sin soltarla", "sin soltarla"),

    # ================================================================ COMENTARIOS Y CAMPAÑA
    puesto("cuatro comentarios que se ganaron", "Antes del número uno", "Cuatro comentarios", dur=3.2),
    com("Marcelo escribió que estos videos", C_MARCELO, dur=6.0),
    com("Ulices dice que le gustan", C_ULICES, dur=6.6, x=.70, y=.36),
    com("Ghost los escucha como un pódcast", C_GHOST, dur=5.4),
    com("Y Auren dejó una reflexión", C_AUREN, dur=9.4, x=.70, y=.36),
    cam("Godfrey te da la razón", "godfrey", "Godfrey", dur=3.4, x=.16, y=.66),
    ban_p(("Runa Caída pasó los mil", -.1), ("Runa Caída pasó los mil suscriptores|fin", 2.0), "Runa Caída",
          "1 000 suscriptores", "mil"),
    msg(["Gracias."], ("Gracias a cada uno de ustedes", -.1), ("Gracias a cada uno de ustedes|fin", 1.2),
        ["Gracias a cada uno"], "gracias"),
    mg(E.cien("De cada 100 que ven Runa Caída", 6, remate=("Solo 6 están suscritos", 1)), ("Aun así, de cada cien", -.2),
       ("solo seis están suscritos|fin", .2), ["de cada cien que ven", "solo seis están suscritos"], "cien", y=.44),
    puesto("El siguiente objetivo son dos mil", "Siguiente objetivo", "2 000 suscriptores", dur=2.0),
    msg(["Intenta suscribirte."], ("Si llevas cuatro atrocidades", -.1), ("que vas a hacer hoy|fin", 1.4),
        ["Si llevas cuatro atrocidades"], "suscribete 2"),

    # ================================================================ 1 · EL FINIQUITO DE SEROSH
    puesto(("El finiquito de Serosh", -1.6), "Atrocidad número 1", "El finiquito de Serosh", dur=2.8),
    expe(4, "El finiquito de Serosh", dur=1.4),
    aba([("espadon_injertado", "Enemigos"), ("talisman_hacha", "Su pueblo"), ("grillete_mohg", "Sus hijos"),
         ("recuerdo_gigante", "Una especie")],
        ("contra su pueblo, contra sus hijos", .1), ("contra una especie entera|fin", 1.0),
        [("contra su pueblo, contra sus hijos", -.4), "contra su pueblo, contra sus hijos", "contra sus hijos y contra",
         "y contra una especie entera"], "las otras cuatro", tam=280),
    cam("contra el único que lo aguantó", "serosh", "Serosh", dur=4.4, x=.84, y=.66, foco=(.5, .4, 1.4)),
    ban_p(("Y encima la comete delante de ti", -.1), ("en tu propia cara|fin", 1.0), "Delante de ti", "En tu propia cara",
          "en tu cara"),
    grande("El león que Godfrey lleva", "godfrey", "Godfrey y Serosh", lado="der", dur=5.0, tam=640),
    ban_p(("Su título es Serosh", -.1), ("Y no estaba ahí de adorno|fin", .8), "Serosh", "Señor de las Bestias", "titulo"),
    rel("El Icono de Godfrey lo explica", "icono_godfrey", "Icono de Godfrey", dur=5.0),
    ficha("El Icono de Godfrey lo explica", "Icono de Godfrey", "Godfrey era un feroz guerrero. Cuando juró sus votos para "
          "convertirse en Señor, comenzó a llevar a la bestia regente Serosh a sus espaldas, *con el fin de calmar el "
          "incesante deseo de batalla que ardía en su interior*.", tipo="Talismán", icono="icono_godfrey",
          a=("que ardía en su interior|fin", .6)),
    mg(E.contencion(barra="Deseo de batalla", freno="Serosh", grito="Hoarah Loux", icono=_G("icono_godfrey")),
       ("con el fin de calmar el incesante", -.2), ("que ardía en su interior|fin", .4),
       [("con el fin de calmar el incesante", .3)], "contencion 1", y=.74),
    sil("Y ese icono lo guarda Godefroy", _G("godefroy"), "Godefroy", "el Injertado", dur=3.0, lado="der", encuadre=(0, .5)),
    mapa("mundo", [pto(M_LEYND, "Leyndell", None, "inicio"), pto(M_GODEF, "Prisión eterna", _foto("godefroy"), "meta")],
         ("en una prisión eterna de la Meseta", -.3), ("cosido con brazos ajenos como Godrick|fin", .4),
         ["en una prisión eterna", ("en una prisión eterna de la Meseta Altus|fin", 0)], titulo="Meseta Altus",
         sub="Prisión eterna", ventana=True, x=.30, y=.40, entrada="foco", traza=99),
    cam("como Godrick", "godrick", "Godrick", dur=3.6, x=.84, y=.40),
    ban_p(("Hasta para contarte quién era su abuelo", -.1), ("lo hace con miembros robados|fin", 1.0), "La familia",
          "Con miembros robados", "miembros"),
    mg(E.contencion(barra="Deseo de batalla", freno="Serosh", grito="Hoarah Loux", icono=_G("icono_godfrey")),
       ("Serosh era su freno", -.3), ("Serosh era su freno|fin", 1.4), [("Serosh era su freno", -.3)], "contencion 2",
       y=.50),
    rel(("El Gran martillo de garras bestiales", 1.4), "martillo_garras", "Gran martillo de garras bestiales", dur=4.0),
    cam("el que te da Gurranq", "gurranq", "Gurranq", dur=3.6, x=.84, y=.70),
    ficha(("El Gran martillo de garras bestiales", 1.4), "Gran martillo de garras bestiales", "Dicen que las uñas negras que "
          "sobresalen de la piel dorada representan a Serosh, Señor de las Bestias, *que se convertiría en regente del rey "
          "Godfrey*.", tipo="Gran martillo", icono="martillo_garras", a=("lo llama regente del rey Godfrey|fin", .3)),
    rel("Y un escudo con su blasón", "escudo_apuntado", "Escudo apuntado con blasón de bestia", dur=5.2),
    ficha("Y un escudo con su blasón", "Escudo apuntado con blasón de bestia", "En su blasón presenta una bestia, la cual "
          "recuerda a los guerreros que no han de sucumbir a la agitación del combate. *Lucha con pasión, pero no seas su "
          "prisionero*.", tipo="Escudo", icono="escudo_apuntado", a=("pero no seas su prisionero|fin", 1.4)),
    ban_p(("Ese león dorado con su jinete", -.1), ("el símbolo de toda una época|fin", 1.0), "El león y su jinete",
          "Toda una época", "epoca"),
    rel("La Armadura leonina de Radahn", "armadura_radahn", "Armadura leonina de Radahn", dur=5.0),
    ficha("La Armadura leonina de Radahn", "Armadura leonina de Radahn", "Se dice que el león dorado simboliza a Godfrey, el "
          "primer Señor del Círculo, y a su bestia regente, Serosh. *Desde su juventud, Radahn quedó naturalmente "
          "fascinado por el Señor de la Batalla*.", tipo="Armadura", icono="armadura_radahn",
          a=("fascinado por el Señor de la Batalla|fin", .6)),
    sil("Un niño que creció admirando", _G("radahn"), "Radahn", "creció admirándolos", dur=3.2, lado="izq", encuadre=(0, .5)),
    mg(E.cadena(["Desde que fue rey", "Sin la gracia", "La Larga Marcha", "El exilio", "La muerte"], preso="Godfrey",
                amo="Serosh", remate="Una vida entera, y otra después", titulo="Lo que cargó Serosh"),
       ("Lo cargó desde que fue rey", -.2), ("pelear contra todo el mundo|fin", 1.0),
       ["Lo cargó desde que fue rey", "Lo acompañó cuando le quitaron", "Lo siguió en la Larga Marcha",
        "al exilio, a la guerra lejana", "y a la muerte", "Una vida entera, y otra después"], "lo cargo"),
    mapa("mundo", [pto(M_LEYND, "Trono de Elden", _foto("p:trono_elden", "p:leyndell_ceniza"), "poder")],
         ("Y en el Trono de Elden", -.3), ("por fin lo ves|fin", .5), ["Y en el Trono de Elden"],
         titulo="Leyndell, capital cinérea", sub="Trono de Elden", ventana=True, x=.30, y=.40, entrada="mesa", traza=99),
    pant("leyndell_ceniza", ("en la capital hecha ceniza", -.3), ("por fin lo ves|fin", .3),   # 19-nov: luego, Godfrey en
         zoom=(1.0, 1.12)),                                                                     # movimiento (clips 139-140)
    sil("Godfrey vuelve con Serosh a la espalda", _G("godfrey"), "Godfrey", "con Serosh a la espalda", dur=4.6, lado="der",
        encuadre=(0, .55)),
    msg(["Por desgracia, aquí estoy de nuevo", "para reclamarlo una vez más.", "Yo, Godfrey,", "¡el primer Señor del Círculo!"],
        ("Por desgracia, aquí estoy", -.1), ("Yo, Godfrey, el primer Señor del Círculo|fin", 1.2),
        ["Por desgracia, aquí estoy", "para reclamarlo una vez más", "Yo, Godfrey", "el primer Señor del Círculo"],
        "aqui estoy", y=.60),

    # ---- 1b · Serosh se vuelve de carne
    puesto("pasa algo que casi nadie mira", "Fíjate", "Casi nadie lo mira", dur=4.0),
    ban("Deja de ser un espíritu", _P("serosh_carne"), "Serosh", "se vuelve de carne", foco=(.80, .40, 1.3), dur=5.0, lado="izq",
        y=.20),                                  # 19-nov: banda arriba; la escena (clip 142, Serosh materializándose) se ve
    ban_p(("Por primera vez en eras", -.2), ("Por primera vez en eras|fin", 1.4), "Serosh", "Por primera vez en eras",
          "primera vez"),
    mg(E.contencion(barra="Deseo de batalla", freno="Serosh", grito="Hoarah Loux", icono=_G("icono_godfrey")),
       ("Y le rompe el cuello", 1.0), ("dar la cara por él|fin", .4),             # 19-nov: DESPUÉS del crujido; la escena
       [("Y le rompe el cuello", 1.0), ("Y le rompe el cuello", 1.4), ("Y le rompe el cuello", 2.0)],   # (143-145) queda libre
       "contencion 3", y=.42),
    ban_p(("Al león que lo cuidó durante eras", -.1), ("dar la cara por él|fin", 1.0), "Al león que lo cuidó",
          "A punto de dar la cara", "dar la cara"),
    ban_p(("En japonés la frase es todavía peor", -.1), ("fingir buenos modales|fin", .8), "En japonés",
          "Se acabó fingir", "japones"),
    cam("Serosh era los buenos modales", "serosh", "Serosh", dur=4.0, x=.84, y=.52, foco=(.5, .4, 1.4)),
    puesto("Serosh era los buenos modales", "Serosh", "Era los buenos modales", dur=3.8),
    ban("Bañado en la sangre de su regente", _P("hoarah_loux"), "Hoarah Loux", "bañado en sangre", foco=(.47, .26, 1.1),
        dur=4.4, y=.20),                         # 19-nov: banda arriba; la transformación y el grito (clips 147-148) se ven
    cam("tira el hacha y grita", "hacha_godfrey", "El hacha", dur=3.6, x=.16, y=.66, foco=(.5, .5, 1.3)),
    puesto(("antes de ser rey. Escúchalo|fin", .2), "Ahora pelea como", "Hoarah Loux", dur=6.4),

    # ---- 1c · sin freno
    mg(E.contencion(barra="Deseo de batalla", freno="Serosh", grito="Hoarah Loux", remate="Sin freno, sin corona",
                    icono=_G("icono_godfrey")),
       ("Ahora pelea como Hoarah Loux", -.3), ("llevaba eras evitando|fin", 1.0),
       [("Ahora pelea como Hoarah Loux", -.6), ("Ahora pelea como Hoarah Loux", -.5), ("Ahora pelea como Hoarah Loux", -.4),
        "Sin freno, sin corona"], "contencion 4", y=.50),
    rel("Y la expansión ya te había avisado", "atuendo_altiplanos", "Atuendo de los altiplanos", dur=5.0),
    ficha("Los guerreros de los altiplanos, su gente", "Atuendo de los altiplanos", "*Los guerreros de los altiplanos son "
          "famosos como cazadores de osos*; para ellos, no hay acto más glorioso que subyugar a una bestia salvaje.",
          tipo="Armadura", icono="atuendo_altiplanos", a=("subyugar a una bestia salvaje|fin", .6)),
    ban_p(("Serosh era la bestia", -.1), ("llevaba toda la vida encima de él|fin", .8), "Serosh", "Era la bestia", "bestia"),
    com("Nibald nos escribió", C_NIBALD, dur=7.4),
    puesto("flojo de verdad es Godfrey", "Flojo de verdad", "Godfrey", dur=3.6),
    cam("Tuvo un consejero durante eras", "serosh", "Su consejero", dur=4.2, x=.84, y=.66, foco=(.5, .4, 1.4)),
    puesto("lo despidió de un crujido", "Lo despidió", "De un crujido", dur=3.4),
    aba([("corona_senor", "Corona"), ("icono_godfrey", "Icono"), ("hacha_godfrey", "Hacha"), ("espadon_injertado", "Espadón")],
        ("seguimos leyendo cada descripción", -.2), ("para que no tengas que hacerlo tú|fin", .8),
        [("seguimos leyendo cada descripción", 0), ("seguimos leyendo cada descripción", .5),
         "de cada arma", ("de cada arma|fin", .3)], "descripciones", tam=280),
    sil("Y lo mejor es lo que dice cuando", _G("hoarah_loux"), "Hoarah Loux", "cuando por fin cae", dur=4.6, lado="der",
        encuadre=(0, .55)),
    puesto("tu fuerza es digna de una corona", "Al caer", "Digna de una corona", dur=4.0),
    puesto("la corona se gana con la fuerza", "Si te mata", "Se gana con la fuerza", dur=4.0),
    rel("El Hacha de Godfrey ya lo había", "hacha_godfrey", "Hacha de Godfrey", dur=5.0),
    ficha("El Hacha de Godfrey ya lo había", "Hacha de Godfrey", "Esta arma simboliza la promesa de Godfrey de actuar como un "
          "señor y, más adelante, se convirtió en el emblema del linaje dorado. *Antaño, la corona se afianzaba mediante la "
          "fuerza*.", tipo="Gran hacha", icono="hacha_godfrey", a=("se afianzaba mediante la fuerza|fin", 1.0)),
    puesto("todo su programa de gobierno", "En una sola frase", "Su programa de gobierno", dur=2.2),
    puesto("Y tú se lo acabas de confirmar", "Y tú", "Se lo acabas de confirmar", dur=3.6),

    # ================================================================ CIERRE
    mg(E.estandartes(["Señor de la Tormenta", "País de Morne", "Su pueblo", "Sus hijos", "Los gigantes", "Serosh"],
                     remate="Todo, en manos del señor Godfrey", titulo="La lista de Godfrey"),
       ("Esa es la lista", -.2), ("y al que le rompió el cuello|fin", .2),
       ["Un señor de la Tormenta del que", "y un país desaparecido", "Un pueblo mandado a morir lejos, del",
        "Dos hijos bajo tierra", "Una especie borrada", "Y un león que se volvió", "y al que le rompió el cuello"],
       "lista"),
    mg(E.linaje(raiz=("Godfrey", "primer Señor del Círculo"), hijos=(("Godrick", "el Injertado"),),
                medio="la sangre, cada vez más diluida", remate="Cosiéndose brazos en Velo Tormentoso",
                titulo="El linaje dorado"),
       ("Y su legado fue el linaje dorado", -.2), ("el mismo castillo que su abuelo conquistó|fin", 1.0),
       ["Y su legado fue el linaje dorado", ("Y su legado fue el linaje dorado|fin", .2), "Que acabó en Godrick",
        "cosiéndose brazos en Velo"], "linaje"),
    sil("Y cuando Godrick te mata", _G("godrick"), "Godrick", "pregunta si lo ha visto", dur=5.0, lado="izq",
        encuadre=(0, .5)),
    ban_p(("Sí, Godrick. Lo vio todo", -.1), ("Lo empezó todo|fin", 1.2), "Lo vio todo", "Lo empezó todo", "lo empezo"),
    pant("fortaleza_sombria", ("La expansión lo remata", -.3), ("sin atisbo de vacilación|fin", .4), alt="leyndell",
         zoom=(1.0, 1.10)),
    rel("con un talismán en la Fortaleza sombría", "talisman_dadiva", "Talismán de la dádiva del señor", dur=5.0),
    ficha("Godfrey recibiendo la savia del Árbol", "Talismán de la dádiva del señor", "Talismán que muestra a Godfrey, "
          "primer Señor del Círculo, mientras recibe la preciada savia. […] El Señor del Árbol Áureo aceptó la savia "
          "estoicamente, sin atisbo de vacilación. *¡No debe sorprender que proyecte una larga sombra sobre las tierras!*",
          tipo="Talismán", icono="talisman_dadiva", a=("una larga sombra sobre las tierras|fin", .6)),
    puesto(("No sorprende", -1.0), "Una larga sombra", "No sorprende", dur=3.4),
    msg(["Los comentarios se leen todos."], ("Los comentarios se leen todos", -.1), ("se decide cada video|fin", .4),
        ["Los comentarios se leen todos"], "se leen"),
    aba([("rykard", "Rykard"), ("zampaheces", "Zampaheces"), ("gideon", "Gideon"), ("rennala", "Rennala"),
         ("messmer", "Messmer")],
        ("Ya están apuntados Rykard", -.2), ("y hasta la Voluntad Mayor|fin", .6),
        ["Ya están apuntados Rykard", "el Zampaheces con Gideon", ("el Zampaheces con Gideon|fin", 0), "Rennala, Messmer",
         ("Rennala, Messmer|fin", 0)], "apuntados", y=.46, tam=260),
    ban_p(("Bayle y hasta la Voluntad Mayor", -.1), ("cuál quieres que sea el siguiente|fin", 1.0), "Y hasta",
          "Bayle y la Voluntad Mayor", "bayle"),
    aba([("marika", "Márika"), ("miquella", "Miquella"), ("malenia", "Malenia"), ("ranni", "Ranni"), ("melina", "Melina")],
        ("En el canal tienes las atrocidades", -.2), ("Melina, Radahn", .4),
        ["de Márika y Radagon", "de Miquella#3", "Malenia, Ranni", ("Malenia, Ranni|fin", 0), "Melina, Radahn"], "canal 1",
        tam=260),
    aba([("radahn", "Radahn"), ("morgott", "Morgott"), ("mohg", "Mohg"), ("godrick", "Godrick")],
        ("Radahn, Morgott, Mohg", .3), ("y las tuyas|fin", .6),
        [("Radahn, Morgott, Mohg", -.4), "Morgott, Mohg", "Mohg, Godrick", "Godrick, y las tuyas"], "canal 2", tam=260),
    puesto("Suscríbete, que vamos por los dos mil", "Suscríbete", "Vamos por los 2 000", dur=3.8),
    ban_p(("Crónicas de Tamriel, nuestro canal hermano", -.3), ("Te lo dejo aquí al final|fin", 1.0), "Canal hermano",
          "Crónicas de Tamriel", "tamriel"),
    ban("Y la próxima vez que llegues", _G("godfrey"), "Godfrey", "te llamará valiente", foco=(.5, .3, 2.0), dur=4.6),
    cam("fíjate en el león", "serosh", "Serosh", dur=4.6, x=.84, y=.40, foco=(.5, .4, 1.4)),
    ban_p(("Él ya sabe cómo acaba", -.2), ("Él ya sabe cómo acaba|fin", 2.6), "Serosh", "Ya sabe cómo acaba", "como acaba"),
]

# ---- 19-nov-2026 (revisión previa al render): bloques nuevos AL FINAL para no mover índices
FX += [
    # el monumento de espada REAL de la frontera de Caelid (Lore Turtle, cuadro limpio sin su rótulo)
    pant("monumento_caelid_espada", ("Un monumento en la frontera de Caelid lo confirma|fin", .1),
         ("permanecen invencibles e incólumes|fin", .5), zoom=(1.0, 1.10)),
]

FX = [d for d in FX if d]
if FALTAN:
    print("efectos.py: pantallas que aún no existen (cubiertas con su alternativa):", " ".join(sorted(set(FALTAN))))
