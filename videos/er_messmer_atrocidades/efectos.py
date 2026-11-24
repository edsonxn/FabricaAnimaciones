# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Messmer QUE IGNORASTE» (SECUENCIA YT, Runa Caída, 24-nov-2026).
Molde: videos/er_rykard_atrocidades/efectos.py (copia en _efectos_rykard_molde.py) · plan: _fx_plan.md · reglas:
docs/estilo_secuencia_yt.md § REGLA DE ORO y § Runa Caída. Kit nucleo/mg_er.py + peg_estilos/peg_anim (tema «er»).
- FICHAS = solo citas en español verificadas (_investigacion/dossier.md § 3, [EG]/[ES-wiki]); los diálogos que solo existen
  en inglés (Anciana, Cornamentado, Leda, Queelign, almas estancadas) y la Bendición de Márika (EN/JP) van PARAFRASEADOS en
  rótulos `puesto` (arriba, y=.10, `top()`) o dentro de un MG, nunca entre comillas en una ficha.
- MG NUEVOS (mg_er, 24-nov): medalla (avance en introb; completo en p1b «Léelo otra vez»), tumba (p5b, en 2 apariciones),
  empalados (p3, «Las destripaban, las colgaban y después las quemaban»: la cita de p3_5 va en ficha), sopa (p2), despojados
  (avance en introb sin tachar; completo en p1c). Reusados: expediente (un cargo por puesto; sello CULPABLE en el cierre),
  linaje (gancho y p5), estandarte_caido, dos_nombres, balanza ×2, estandartes, cadena, triada, domino, cien, acuerdo, ecos.
- MAPAS (mapas/sombras.jpg, coordenadas MEDIDAS del dossier § 4): introb Reino → Fortaleza · p4 Fortaleza → Rauh · p3 Belurat
  y la torre · p2 Belurat (ventana) · p2c Llanura de las Tumbas → Ruinas calcinadas · p1b Belurat → Fortaleza (su sala).
- PISTAS voz=True (cortes en sfx/, `post` en guion.py): s_despojados (intro), s_cornamentado (p2b), s_madre_sanciona (p1b),
  s_maldicion (cierre); durante cada una SOLO el rótulo de lo que se oye, abajo (y=.80), sin tapar la cara de quien habla.
  FAB_FX_FINAL=1 python fab.py er_messmer_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALAS TODAS)
"""
import os

import mg_er as E
import mg_tes as T
import peg_estilos as PE

_AQUI = os.path.dirname(os.path.abspath(__file__))
_PEG = os.path.join(_AQUI, "pegatinas")
_PAN = os.path.join(_AQUI, "pantallas")
_MAP = os.path.join(_AQUI, "mapas")
_FX, _FY = .70, .32     # fichas: arriba a la derecha (caja real ~980 px → borde derecho a ~4,5 %)
TEMA_MAPA = "er"
TEMA = "er"

CAMARA = {}
FUNDIDO = {}

_P = lambda s: os.path.join(_PAN, s + ".jpg")
_G = lambda s: os.path.join(_PEG, s + ".png")
FALTAN = []             # pantallas pedidas que aún no existen (se cubren con su alternativa)


def _hay(slug):
    return os.path.exists(_P(slug))


def pto(xy, nombre, foto=None, tipo=None):
    return (xy[0], xy[1], nombre, tipo, foto) if foto else (xy[0], xy[1], nombre, tipo)


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **fijo):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    return dict(tipo="mg", fn=PA.variado(_G(slug), titulo, tam, tema=TEMA, **fijo), en=en, dur=dur, x=x, y=y, sale=.06,
                nombre="pegatina " + slug, ver=1.0)


def grande(en, slug, titulo, lado="izq", dur=4.6, tam=600, y=.48, **fijo):
    return peg(en, slug, titulo, dur=dur, x=.25 if lado == "izq" else .75, y=y, tam=tam, **fijo)


def com(en, cid, dur=6.0, x=.28, y=.32, tam=760):
    """Tarjeta del comentario REAL (nucleo/comentarios.tarjeta → pegatinas/com_<id>.png)."""
    return peg(en, "com_" + cid, "", dur=dur, x=x, y=y, tam=tam)


def rel(en, slug, nombre=None, sub=None, dur=4.5, x=.24, y=.44, tam=500):
    """Objeto flotando sobre un círculo de runas."""
    return dict(tipo="mg", fn=PE.reliquia(_G(slug), nombre, sub, tam, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.35,
                nombre="reliquia " + slug, ver=1.2)


def cam(en, slug, nombre=None, dur=3.8, x=.16, y=.66, tam=300, foco=(.5, .2, 2.0)):
    """Medallón para las menciones rápidas."""
    return dict(tipo="mg", fn=PE.camafeo(_G(slug), nombre, tam, foco, tema=TEMA), en=en, dur=dur, x=x, y=y, sale=.3,
                nombre="camafeo " + slug, ver=1.0)


def aba(fotos, de, a, marcas, nombre, x=.50, y=.58, tam=290):
    """Cartas que se abren en abanico cuando la voz enumera. fotos = [(slug, etiqueta ≤ 12 letras)]."""
    return dict(tipo="mg", fn=PE.abanico([(_G(s), t) for s, t in fotos], tam, tema=TEMA), de=de, a=a, marcas=list(marcas),
                x=x, y=y, sale=.35, nombre="abanico " + nombre, ver=2.0)


def leg(slug, titulo, lineas, de, a, marcas, sello=None, x=.22, y=.45, ancho=400):
    """Expediente de pergamino con retrato en sepia; `sello` = (texto, i_marca) se estampa con la voz."""
    return dict(tipo="mg", fn=PE.legajo(_G(slug), titulo, lineas, sello=sello, ancho=ancho, tema=TEMA), de=de, a=a,
                marcas=list(marcas), x=x, y=y, sale=.35, nombre="legajo " + slug, ver=1.6)


def pant(slug, de, a, zoom=(1.0, 1.10), pan=(0, 0, 0, 0), oscuro=0.0, alt=None):
    """Imagen REAL a pantalla completa (mg_wow.pantalla); si `slug` aún no existe, `alt` (otra pantalla que sí exista)."""
    if not _hay(slug):
        FALTAN.append(slug)
        slug = alt
    import mg_wow as M
    return dict(tipo="pantalla", fn=M.pantalla(_P(slug), zoom, pan, oscuro=oscuro), de=de, a=a,
                entra=.5, sale=.5, nombre="pantalla " + slug, ver=2.0)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, a=None, y=None):
    """Ficha del inventario con la cita VERIFICADA. Sin `y`, se baja lo justo para que su borde de arriba quede ≥ 4 %."""
    fn = E.descripcion(nombre, texto, tipo=tipo, icono=_G(icono) if icono else None)
    if y is None:
        y = _FY
        try:
            y = max(_FY, (fn(30.0, 60.0, []).shape[0] / 2 + 46) / 1080)
        except Exception:            # stubs de _anclas.py
            pass
    d = dict(tipo="mg", fn=fn, en=en, x=_FX, y=y, sale=.35, nombre="ficha " + nombre, ver=1.6)
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


def ban_p(de, a, arriba, titulo, nombre):
    """Rótulo `puesto` abajo con inicio y fin anclados."""
    return mg(E.puesto(arriba, titulo), de, a, [], nombre, y=.80)


def top(de, a, arriba, titulo, nombre):
    """Rótulo `puesto` ARRIBA (y=.10): diálogos que solo existen en inglés, PARAFRASEADOS (nunca entre comillas)."""
    return mg(E.puesto(arriba, titulo), de, a, [], "arriba " + nombre, y=.10)


def msg(lineas, de, a, marcas, nombre, y=.76):
    """Mensaje del suelo (texto ámbar), para citas en español que la voz lee."""
    return mg(E.mensaje(lineas), de, a, marcas, "mensaje " + nombre, y=y)


def mapa(slug, puntos, de, a, marcas, titulo=None, sub=None, ventana=False, x=.70, y=.42, **kw):
    import mg_mapa as MP
    ruta = next((os.path.join(_MAP, slug + e) for e in (".jpg", ".png") if os.path.exists(os.path.join(_MAP, slug + e))),
                os.path.join(_MAP, slug + ".jpg"))
    fn = MP.mapa(ruta, puntos, TEMA_MAPA, titulo=titulo, sub=sub, modo="ventana" if ventana else "pantalla", **kw)
    if ventana:
        return dict(tipo="mg", fn=fn, de=de, a=a, marcas=marcas, x=x, y=y, sale=.35, nombre="mapa " + (titulo or slug), ver=3.0)
    return dict(tipo="pantalla", fn=fn, de=de, a=a, marcas=marcas, entra=.5, sale=.5, nombre="mapa " + (titulo or slug), ver=4.0)


# Comentarios (ESTADO.md, leídos el 24-nov; tarjetas en pegatinas/com_<id>.png). NO usar com_UgwJSlXBno3eEYwuI_x4AaABAg.
C_STORMY, C_SERGIO, C_LUIS = "UgxHbdhbvsllIKdpd-Z4AaABAg", "UgyS_O2n-x-GKqkxjtl4AaABAg", "UgzTki3VLPQeOEt1BKF4AaABAg"
C_RICK, C_RICO = "UgxRBIoWmEnn48Wv8DB4AaABAg", "UgzQ8NGWpzIzJX7yDax4AaABAg"
C_DAVID, C_QUIXI = "UgxdHxlNVRMXvaRRqad4AaABAg", "UgzbX3DCRGfAJ_JaDGJ4AaABAg"
C_QUAERENS, C_PASCUAL = "UgzgImyRyHKjdjBkCQx4AaABAg", "Ugxz7Dc9NCilg0P8Lmt4AaABAg"
C_SHIRO, C_ULISES, C_DANIEL = "UgzTQ0w2ZJwz6Nh3Pgh4AaABAg", "UgwOrheEVgtPhGGmRbN4AaABAg", "UgzyUmjrE2l-sir6F9d4AaABAg"
C_RETOS, C_SANTIAGO = "UgyPJ2Ulc5FuS9MJVAx4AaABAg", "Ugz7NLq2H8saxbXlFO14AaABAg"

# Coordenadas MEDIDAS (fracción de mapas/sombras.jpg; dossier § 4). Los lugares «NO MEDIDOS» allí NO se usan.
M_FORT = (.49, .43)          # Fortaleza sombría (por forma + Mapa: Altiplano Sombrío)
M_RAUH = (.283, .490)        # Antiguas ruinas de Rauh (gólem)
M_BELURAT = (.245, .60)      # Belurat, asentamiento de la torre
M_TORRE = (.225, .555)       # la torre de los cornamentados (Enir-Ilim en su cima)
M_LLANURA = (.40, .68)       # Llanura de las Tumbas (rótulo de región)
M_CALCIN = (.390, .693)      # Ruinas calcinadas (gólem)

CARGOS = ["Encerró a los suyos en una tumba", "Su sabio quemó más que nadie", "Colgó a sus dioses",
          "Enfrió la sopa de una familia", "Te puso la medalla"]


def expe(k, frase, dur=2.6):
    """Ficha del acusado al abrir el puesto k (0 = n.º 5): escribe el cargo k (el sello CULPABLE cae en el cierre)."""
    return mg(E.expediente(acusado="Messmer el Empalador", sub="hijo de Márika, señor del Reino de las Sombras",
                           cargos=CARGOS[:k + 1], ya=k, sello=None, titulo="El Empalador, juzgado"),
              (frase + "|fin", -.4), (frase + "|fin", dur), [(frase + "|fin", -.2)], f"expediente {k + 1}")


# Los 4 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026 y regla 10; cortes en sfx/, `post` en guion.py)
P_DESPOJ = "no se olvida. Escúchalo|fin"
P_CORNA = "diciéndole esto. Escúchalo|fin"
P_MADRE = "despojado de luz. Escúchalo|fin"
P_MALDI = "Es para ella. Escúchalo|fin"
PISTAS = [
    dict(sfx="s_despojados", en=P_DESPOJ, vol=1.0, voz=True),
    dict(sfx="s_cornamentado", en=P_CORNA, vol=1.0, voz=True),
    dict(sfx="s_madre_sanciona", en=P_MADRE, vol=1.0, voz=True),
    dict(sfx="s_maldicion", en=P_MALDI, vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    grande(("Messmer el Empalador", 0), "messmer", "Messmer el Empalador", lado="izq", dur=2.1, tam=560, y=.46),
    mg(E.linaje(raiz=("Márika", "la reina"), hijos=(("Messmer", "el Empalador"),), medio="su hijo",
                remate="Señor del Reino de las Sombras", titulo="El hijo de la reina", injertos=()),
       ("Hijo de la reina Márika", 0), ("y el jefe que te espera", -.25),
       [("Hijo de la reina Márika", 0), ("Hijo de la reina Márika", .5), ("Hijo de la reina Márika|fin", .1),
        "señor del Reino de las Sombras"], "linaje gancho"),
    pant("fortaleza_sombria_exterior", ("y el jefe que te espera", -.2), ("con una lanza en llamas", -.1), zoom=(1.0, 1.10)),
    ban_p(("en lo más alto de la Fortaleza", -.1), ("con una lanza en llamas", -.2), "Lo más alto de", "La Fortaleza sombría",
          "fortaleza"),
    rel(("con una lanza en llamas", 0), "lanza_empalador", "Lanza del Empalador", dur=2.4, x=.22, y=.44, tam=460),
    pant("messmer_fase2_cubre_rostro", ("y una serpiente dentro", -.2), ("te mira desde arriba", -.1), zoom=(1.0, 1.08)),
    pant("trailer_messmer_lanza_llamas", ("te mira desde arriba", -.2), ("una frase que resume", -.1), zoom=(1.36, 1.42)),
    puesto(("una frase que resume su vida", -.1), "Una sola frase", "Resume su vida entera", dur=3.2),
    peg(("La dice en inglés", 0), "messmer", "Messmer", dur=4.0, x=.80, y=.40, tam=360),
    ban_p(("con esa voz que no se olvida", -.1), (P_DESPOJ, -.05), "En inglés", "Con esa voz que no se olvida", "voz"),
    # ---- PISTA 1: s_despojados (11,44 s) — solo el rótulo de lo que se oye
    ban_p((P_DESPOJ, .15), (P_DESPOJ, 6.0), "Messmer: Those stripped of the Grace of Gold", "…shall all meet death",
          "pista despojados 1"),
    ban_p((P_DESPOJ, 6.1), (P_DESPOJ, 11.5), "Messmer", "In the embrace of Messmer's flame", "pista despojados 2"),

    # ---- introb · la frase, lo que todos saben y lo que viene
    mg(E.despojados(remate=None), ("En español: quienes se ven", -.3), ("En el abrazo de", -.15),
       [("En español: quienes se ven", .2)], "despojados avance"),
    msg(["En el abrazo de la llama de Messmer."], ("En el abrazo de", -.1), ("En el abrazo de la llama de Messmer|fin", 1.0),
        [("En el abrazo de", 0)], "abrazo"),
    puesto(("Casi todo el mundo cree", 0), "Lo que todos saben", "Quemó a un pueblo entero", dur=3.6),
    grande(("pueblo entero, los cornamentados", 0), "cornamentado", "Los cornamentados", lado="der", dur=3.7, tam=540, y=.44),
    mapa("sombras", [pto(M_FORT, "Fortaleza sombría", _P("fortaleza_sombria_exterior"), "poder")],
         ("El propio juego lo anuncia", -.3), ("y calcinado por la llama", -.3), [("El propio juego lo anuncia", 0)],
         titulo="Reino de las Sombras", sub="Un reino purgado en una batalla olvidada", entrada="desenrolla", traza=99),
    pant("reino_sombras", ("y calcinado por la llama", -.35), ("y calcinado por la llama de Messmer|fin", 1.4)),
    msg(["Un reino purgado en una batalla olvidada.", "Y calcinado por la llama de Messmer."],
        ("y calcinado por la llama", -.3), ("y calcinado por la llama de Messmer|fin", 1.3),
        [("y calcinado por la llama", -.3), ("y calcinado por la llama", 0)], "reino calcinado"),
    puesto(("Pero eso ya lo sabe", 0), "Eso ya se sabe", "Hoy va lo otro", dur=3.0),
    aba([("caballero_negro", "Caballeros"), ("leon", "Sus dioses"), ("potaje", "Una sopa"), ("insignia", "La medalla")],
        ("Lo que les hizo a sus", -.2), ("también estabas tú|fin", .7),
        ["Lo que les hizo a sus", "caballeros. Lo que hizo con", "otro pueblo. Una sopa fría", "Y en el número uno, una"],
        "avance", y=.56, tam=280),
    puesto(("Este video lo pidieron ustedes", 0), "Lo pidieron ustedes", "Y con ganas", dur=2.4),
    com("Stormy escribió que", C_STORMY, dur=5.8),
    com("Sergio las pidió dos", C_SERGIO, dur=4.0, x=.72, y=.36),
    com("Y Luis lo dijo claro", C_LUIS, dur=6.0),
    com("Rick dice que es", C_RICK, dur=3.6, x=.72, y=.36),
    ban_p(("Y Santiago y Alphonse", -.1), ("lo pidieron hace semanas|fin", .3), "Santiago y Alphonse",
          "Lo pidieron hace semanas", "santiago"),
    peg(("cuando aquí todavía íbamos", 0), "godrick", "Godrick", dur=3.0, x=.20, y=.40, tam=360),
    puesto("Stormy, ya puedes", "Stormy", "Recupera la cordura", dur=3.0),
    grande("Aunque después de este video", "messmer_jefe", "No te la garantizo", lado="der", dur=3.8, tam=520, y=.44),
    puesto("Y antes de empezar, un comentario", "Antes de empezar", "Un comentario", dur=3.0),
    com("Rico nos preguntó", C_RICO, dur=6.6),
    ban_p(("No todo el mundo lo ignoró", -.1), ("Algunos lo disfrutaron|fin", .5), "No todo el mundo lo ignoró",
          "Algunos lo disfrutaron", "disfrutaron"),
    mg(E.medalla(_G("insignia"), remate=None), ("Para ellos, el ejército", -.2), ("Sale en el número uno|fin", .8),
       [("Para ellos, el ejército", 0), "mandó hacer una medalla", ("mandó hacer una medalla", .8), "Sale en el número uno"],
       "medalla avance"),

    # ================================================================ 5 · SU PROPIA GENTE, A LA TUMBA
    puesto("Número cinco", "Atrocidad número 5", "Su gente, a la tumba", dur=3.4),
    expe(0, "Su propia gente, a la tumba", dur=3.0),
    ban_p(("ya había quemado lo de dentro", -.1), ("ya había quemado lo de dentro|fin", .8), "Antes que a nadie de fuera",
          "Quemó lo de dentro", "lo de dentro"),
    peg(("Empecemos por sus caballeros", 0), "armadura_fuego", "La armadura roja", dur=3.4, x=.20, y=.56, tam=420),
    grande(("armadura roja: los Caballeros", 0), "caballero_fuego", "Caballeros de Fuego", lado="der", dur=4.4, tam=560,
           y=.46),
    rel("Su casco lo cuenta", "casco_fuego", "Casco de Caballero de Fuego", dur=15.9),
    ficha("Su casco lo cuenta", "Casco de Caballero de Fuego", "Todos los caballeros provenían de alguna importante familia "
          "de los niveles superiores del Árbol Áureo, pero *fueron marginados, perseguidos y expulsados de sus hogares tras "
          "jurar lealtad a Messmer* como su señor.", tipo="Yelmo", icono="casco_fuego",
          a=("Messmer como su señor|fin", .3)),
    mg(E.estandarte_caido(emblema="Caballeros de Fuego", quien="familias de lo alto del Árbol Áureo",
                          remate="Jurarle lealtad te costaba la casa", titulo="Expulsados de sus hogares"),
       ("Jurarle lealtad te costaba", -.3), ("lo que recibían a cambio", -.25),
       [("Jurarle lealtad te costaba", -.1), ("te costaba la casa", .2), ("te costaba la casa|fin", 0)], "estandarte fuego"),
    rel(("lo que recibían a cambio", -.1), "armadura_fuego", "Armadura de Caballero de Fuego", dur=8.8),
    ficha(("lo que recibían a cambio", -.1), "Armadura de Caballero de Fuego", "*Solo ellos llegaron a conocer de verdad a "
          "Messmer*. Sus llamas son como serpientes. […]", tipo="Armadura", icono="armadura_fuego",
          a=("Sus llamas son como serpientes|fin", .6)),
    pant("messmer_cinematica_serpientes_lanza", ("Ese era el secreto del ejército", -.3), ("Su Recuerdo lo dice", -.2)),
    ban_p(("Su señor llevaba una serpiente", -.1), ("Su Recuerdo lo dice", -.3), "El secreto del ejército",
          "Una serpiente dentro", "secreto"),
    rel("Su Recuerdo lo dice sin rodeos", "recuerdo_empalador", "Recuerdo del Empalador", dur=12.2),
    ficha("Su Recuerdo lo dice sin rodeos", "Recuerdo del Empalador", "Una serpiente malévola se retorcía dentro de Messmer, "
          "por lo que *su madre le arrancó el ojo y lo sustituyó por un sello de Gracia*. […]", tipo="Recuerdo",
          icono="recuerdo_empalador", a=("un sello de Gracia|fin", .4)),
    mg(E.linaje(raiz=("Márika", "la reina, su madre"), hijos=(("Messmer", "el ojo sellado"),), medio="le arrancó el ojo",
                remate="Y lo puso al frente de una guerra", titulo="La madre y el hijo", injertos=()),
       ("Y aun así, con eso dentro", -.2), ("al frente de una guerra|fin", 1.0),
       [("Y aun así, con eso dentro", 0), ("Y aun así, con eso dentro", .6), "su madre lo puso al",
        "al frente de una guerra"], "madre e hijo"),
    peg("El Escudo con blasón", "escudo_serpiente", "Escudo con blasón de serpiente", dur=8.8, x=.22, y=.46, tam=440),
    ficha("El Escudo con blasón", "Escudo con blasón de serpiente", "Se dice que se forjó para conmemorar los inicios de la "
          "cruzada iniciada por *Messmer, hijo de Márika*.", tipo="Escudo", icono="escudo_serpiente",
          a=("iniciada por Messmer, hijo de Márika|fin", .7)),
    peg(("Un ojo arrancado y un sello", 0), "casco_messmer", "Casco de Messmer", dur=3.0, x=.20, y=.50, tam=420),
    cam(("Un ojo arrancado y un sello", .2), "marika", "Su madre", dur=2.8, x=.84, y=.40, foco=(.5, .35, 1.3)),
    puesto("Y no todos sus hombres", "No todos sus hombres", "Lo aceptaron", dur=3.8),

    # ---- 5b · Andreas, Huw y el batallón penitenciario
    grande("Los Caballeros Negros eran", "caballero_negro", "Caballeros Negros", lado="izq", dur=4.2, tam=540, y=.46),
    ficha("Los Caballeros Negros eran", "Andreas, comandante de los Caballeros Negros", "*Los Caballeros Negros eran la "
          "fuerza principal del ejército de Messmer*. […] Aunque tras su huida del Árbol Áureo siguió siendo un devoto "
          "seguidor de Messmer, […]", tipo="Cenizas de espíritu", icono="cenizas_andreas",
          a=("Hasta que se enteró|fin", .3)),
    leg("cenizas_andreas", "Andreas", ["Comandante de los Caballeros Negros", "Siguió a su señor desde el Árbol Áureo",
                                       "Devoto"],
        ("Su comandante, Andreas", -.1), ("Hasta que se enteró|fin", .3),
        [("Su comandante, Andreas", .3), "había seguido a su señor", "y le era devoto", "Hasta que se enteró"],
        sello=("SE ENTERÓ", 3)),
    ficha(("Su ceniza de espíritu lo", 0), "Andreas, comandante de los Caballeros Negros", "[…] Se rebeló tras conocer la "
          "*naturaleza reptiliana de su señor*. Por ello, *fue encarcelado en una tumba subterránea*.",
          tipo="Cenizas de espíritu", icono="cenizas_andreas", a=("Por ello, fue encarcelado en una tumba|fin", .5)),
    cam(("Su ceniza de espíritu lo", 0), "cenizas_andreas", "Andreas", dur=3.8, x=.17, y=.44, foco=(.5, .5, 1.0)),
    cam(("conocer la naturaleza reptiliana", 0), "messmer_serpiente", "Naturaleza reptiliana", dur=4.2, x=.17, y=.44,
        foco=(.5, .4, 1.2)),
    rel(("Y no fue solo. Su hijo", 0), "cenizas_huw", "Huw", "capitán de los Caballeros Negros", dur=12.0),
    ficha(("Y no fue solo. Su hijo", 0), "Huw, capitán de los Caballeros Negros", "[…] *Siguió a su padre, Andreas, en la "
          "rebelión contra Messmer*, y al igual que él, fue encarcelado en una tumba subterránea. […]",
          tipo="Cenizas de espíritu", icono="cenizas_huw", a=("al igual que él, fue encarcelado|fin", 2.0)),
    mg(E.tumba(), ("Un padre y un hijo", -.2), ("Y la descripción de Huw", -.3),
       [("Un padre y un hijo", 0), ("Un padre y un hijo", .6), "encerrados bajo tierra por descubrir"], "tumba 1"),
    ficha(("Y la descripción de Huw", 0), "Huw, capitán de los Caballeros Negros", "[…] Y al igual que él, fue encarcelado "
          "en una tumba subterránea. *Messmer lloró la pérdida de un hermano de armas.*", tipo="Cenizas de espíritu",
          icono="cenizas_huw", a=("un hermano de armas|fin", .6)),
    peg("Messmer lloró la pérdida", "messmer", "Messmer lloró", dur=3.8, x=.20, y=.44, tam=360),
    mg(E.tumba(), ("Lloró. Pero no lo sacó", -.2), ("Los sacaste tú", -.1),
       [("Lloró. Pero no lo sacó", -.2), ("Lloró. Pero no lo sacó", -.2), ("Lloró. Pero no lo sacó", -.2),
        ("Lloró. Pero no lo sacó", 0), "Pero no lo sacó de la tumba"], "tumba 2"),
    aba([("cenizas_andreas", "Andreas"), ("cenizas_huw", "Huw")], ("Los sacaste tú", 0), ("a pelear por ti|fin", .6),
        ["Los sacaste tú", "Sus cenizas son invocaciones"], "cenizas", tam=320),
    puesto("Los soldados rasos lo tenían", "Los soldados rasos", "Lo tenían peor", dur=2.5),
    peg(("Las Cenizas de soldado", 0), "cenizas_soldado", "Cenizas de soldado de Messmer", dur=10.4, x=.22, y=.46, tam=440),
    ficha(("Las Cenizas de soldado", 0), "Cenizas de soldado de Messmer", "Estos soldados pertenecían al *vil batallón "
          "penitenciario* y fueron enterrados *fuera de la vista del Árbol Umbrío*.", tipo="Cenizas de espíritu",
          icono="cenizas_soldado", a=("la vista del Árbol Umbrío|fin", .5)),
    rel(("Su armadura lleva un grabado", 0), "armadura_soldado", "Armadura de soldado de Messmer", dur=9.0),
    ficha(("Su armadura lleva un grabado", 0), "Armadura de soldado de Messmer", "Aunque la pechera luce un motivo del Árbol "
          "Umbrío, *se ha usado oro para su grabado*. Una pequeña consolación para quienes están obligados a *combatir sin "
          "gracia ni honor*.", tipo="Armadura", icono="armadura_soldado", a=("a combatir sin gracia ni honor|fin", .4)),
    rel(("Y el casco de los Caballeros Negros", 0), "casco_negro", "Casco de Caballero Negro", dur=10.4),
    ficha(("Y el casco de los Caballeros Negros", 0), "Casco de Caballero Negro", "[…] Desprende un persistente hedor a "
          "podrido. El olor podría proceder de la sangre contaminada que lo salpicó. O quien sabe si la causante es la propia "
          "*alma ennegrecida del portador tras una matanza sin fin*.", tipo="Yelmo", icono="casco_negro",
          a=("tras una matanza sin fin|fin", .5)),
    pant("llanura_wiki", ("Por el Reino de las Sombras quedan", -.3), ("Y le pregunta cuánto más", -.1)),
    peg(("quedan almas de esos soldados", 0), "soldado_messmer", "Almas de soldados", dur=3.4, x=.20, y=.52, tam=400),
    peg(("soldados, rezándole a Márika", .3), "marika", "Márika", dur=3.4, x=.80, y=.42, tam=360),
    top(("Una le pide a la reina", -.1), ("Y le pregunta cuánto más", -.2), "Alma de un soldado",
        "Abraza a tu hijo y mándanos una señal", "alma senal"),
    top(("Y le pregunta cuánto más", -.1), ("esta guerra santa|fin", .7), "Alma de un soldado",
        "¿Cuánto más durará esta guerra santa?", "alma guerra"),
    puesto("Nadie le contestó", "Nadie le contestó", "Ni la madre, ni el hijo", dur=3.8),

    # ================================================================ 4 · EL SABIO QUE QUEMÓ MÁS QUE NADIE
    puesto("Número cuatro", "Atrocidad número 4", "El sabio incendiario", dur=3.2),
    expe(1, "El sabio que quemó más que nadie", dur=2.6),
    grande("Se llamaba Salza", "capucha_salza", "Salza", lado="izq", dur=4.8, tam=460, y=.44),
    ban_p(("era discípulo del sabio Wego", -.1), ("Un hombre de libros", -.2), "Salza", "Discípulo del sabio Wego", "wego"),
    puesto("Un hombre de libros", "Un hombre de libros", "En un ejército de antorchas", dur=3.6),
    rel("Su hechizo, la Lluvia", "lluvia_fuego", "Lluvia de fuego", dur=15.4),
    ficha("Su hechizo, la Lluvia", "Lluvia de fuego", "Salza siempre mantuvo su desdén al barbarismo, *incluso a pesar de "
          "quemar más aldeas y calcinar más tierras que nadie*.", tipo="Encantamiento", icono="lluvia_fuego",
          a=("calcinar más tierras que nadie|fin", .6)),
    puesto(("Más que nadie en todo", 0), "Más que nadie", "En todo su ejército", dur=2.4),
    mg(E.dos_nombres(a=("El que más quemó", "más aldeas que nadie", "en el ejército del Empalador"),
                     b=("El que despreciaba", "la barbarie", "el sabio Salza"), remate="Eran el mismo hombre",
                     titulo="En el ejército del Empalador"),
       ("En el ejército del Empalador, el", -.2), ("Imagina cómo eran los demás|fin", 1.0),
       ["el que más quemó fue", "fue el que despreciaba", "Imagina cómo eran los demás"], "el mismo hombre"),
    puesto(("Porque en el Árbol Áureo", 0), "En el Árbol Áureo", "El fuego estaba prohibido", dur=3.4),
    rel(("La Chispa aromática lo recuerda", 0), "chispa_aromatica", "Chispa aromática", dur=11.4),
    ficha(("La Chispa aromática lo recuerda", 0), "Chispa aromática", "Aunque el fuego estaba prohibido entre aquellos que "
          "servían al Árbol Áureo, *con el avance de la guerra esta regla fue dejándose de lado*.",
          icono="chispa_aromatica", a=("fue dejándose de lado|fin", .5)),
    peg(("La Grasa de fuego de", 0), "grasa_messmer", "Grasa de fuego de Messmer", dur=9.0, x=.22, y=.50, tam=420),
    ficha(("La Grasa de fuego de", 0), "Grasa de fuego de Messmer", "[…] *El fuego era un símbolo de la cruzada*, e incluso "
          "los soldados rasos de Messmer lo usaban.", icono="grasa_messmer", a=("de Messmer lo usaban|fin", .4)),
    peg(("Y la Botella de perfume", 0), "botella_perfume", "Botella de perfume ígneo", dur=10.6, x=.22, y=.46, tam=440),
    ficha(("Y la Botella de perfume", 0), "Botella de perfume ígneo", "[…] *La cruzada fue una purga violenta en la que "
          "participaron como guerreros*.", tipo="Botella de perfume", icono="botella_perfume",
          a=("participaron como guerreros|fin", .5)),
    puesto(("Y aun así, hubo una cosa", 0), "Una cosa", "Que no quiso quemar", dur=3.4),
    rel(("Su capucha lo cuenta", 0), "capucha_salza", "Capucha de Salza", dur=8.2),
    ficha(("Su capucha lo cuenta", 0), "Capucha de Salza", "Discípulo del sabio Wego, *se negó a quemar unas ruinas antiguas, "
          "incluso a pesar de jugarse la vida*.", tipo="Yelmo", icono="capucha_salza",
          a=("a pesar de jugarse la vida|fin", .6)),
    mg(E.balanza("Lo que se deduce", "Lo que dice el juego",
                 [("i", "Alguien las quería en ceniza"), ("i", "Negarse costaba la cabeza"), ("d", "No dice quién lo ordenó"),
                  ("d", "Salza quemaba para Messmer")],
                 remate="Saca tus conclusiones", titulo="Las ruinas antiguas"),
       ("Alguien quería esas ruinas", -.3), ("Salza las aldeas|fin", 1.6),
       ["Alguien quería esas ruinas", "y decir que no podía", "El juego no dice quién", "Dice para quién quemaba",
        ("Salza las aldeas|fin", .2)], "ruinas"),
    pant("rauh_wiki", ("Las ruinas más famosas del", -.3), ("Y la llama de Messmer acabó", -.2)),
    ficha(("son las Antiguas ruinas de Rauh", -.2), "Mapa: Ruinas de Rauh", "*Estas gigantescas ruinas están inundadas*, "
          "arrasadas por la naturaleza y *divididas en dos por un abismo*. […]", tipo="Objeto clave",
          a=("en dos por un abismo|fin", .5)),
    mapa("sombras", [pto(M_FORT, "Fortaleza sombría", None, "inicio"),
                     pto(M_RAUH, "Antiguas ruinas de Rauh", _P("rauh_wiki"), "meta")],
         ("Y la llama de Messmer acabó", -.3), ("La Yesca de Messmer, la", -.1),
         [("Y la llama de Messmer acabó", -.3), ("acabó llegando a ellas igual", .3)], titulo="La llama llegó",
         sub="De la Fortaleza sombría a Rauh", entrada="mesa", traza=99),
    rel(("La Yesca de Messmer, la", 0), "yesca", "Yesca de Messmer", dur=11.4),
    ficha(("La Yesca de Messmer, la", 0), "Yesca de Messmer", "La llama que arde en el interior de Messmer. […] *Quema el "
          "árbol sellado que se dice que se encuentra en las antiguas ruinas de Rauh*.", tipo="Objeto clave", icono="yesca",
          a=("se encuentra en las antiguas ruinas de Rauh|fin", .3)),
    puesto(("Y quién le prendió fuego", 0), "¿Quién le prendió fuego?", "Tú", dur=3.0),

    # ---- 4b · Hilde, el almacén y la iglesia; David y Quixilero
    puesto("Salza no estaba solo", "Salza", "No estaba solo", dur=2.4),
    cam("Salza no estaba solo", "capucha_salza", "Salza", dur=2.0, x=.84, y=.40, foco=(.5, .5, 1.0)),
    rel(("La Caballera de Fuego Hilde", 0), "hilde", "Caballera de Fuego Hilde", dur=13.0),
    ficha(("La Caballera de Fuego Hilde", 0), "Caballera de Fuego Hilde", "Hilde era una gran amiga del sabio Salza y *se unió "
          "a quienes insistieron en preservar los especímenes*. Las cenizas de Hilde se consagraron como amuleto para "
          "proteger el almacén.", tipo="Cenizas de espíritu", icono="hilde", a=("para proteger el almacén|fin", .5)),
    pant("almacen_wiki", ("Ese almacén es el Almacén", -.3), ("Unos caballeros tuvieron que", -.2)),
    ban_p(("Ese almacén es el Almacén", 0), ("Unos caballeros tuvieron que", -.3), "Dentro de la Fortaleza sombría",
          "Almacén de especímenes", "almacen"),
    pant("almacen_especimenes_interior", ("Unos caballeros tuvieron que", -.3), ("no acabara en la hoguera|fin", .5)),
    ban_p(("Unos caballeros tuvieron que", -.1), ("no acabara en la hoguera|fin", .4), "Unos caballeros",
          "Tuvieron que insistir", "insistir"),
    pant("iglesia_brote", ("Hasta una iglesia acabó", -.3), ("La santa del brote, Romina", -.1)),
    grande(("La santa del brote, Romina", 0), "romina", "Romina, la santa del brote", lado="izq", dur=2.4, tam=540, y=.46),
    peg(("alzó una vez el brote", .5), "hoja_brote", "Hoja enastada del Brote", dur=4.6, x=.22, y=.46, tam=440),
    ficha(("alzó una vez el brote", .5), "Hoja enastada del Brote", "[…] *Una vez, en una iglesia en llamas, Romina alzó el "
          "brote en silencio*.", tipo="Arma", icono="hoja_brote", a=("en una iglesia que ardía|fin", .6)),
    peg(("Ojo: el juego no dice quién quemó", .3), "recuerdo_brote", "Recuerdo de la santa del brote", dur=4.6, x=.20, y=.50,
        tam=420),
    ban_p(("Ojo: el juego no dice quién quemó", -.1), ("quién quemó esa iglesia|fin", .8), "Ojo",
          "No dice quién la quemó", "quien quemo"),
    msg(["Un reino purgado en una batalla olvidada.", "Y calcinado por la llama de Messmer."],
        ("según el propio juego, fue", -.2), ("fue calcinado por la llama de Messmer|fin", 1.2),
        [("según el propio juego, fue", -.2), ("fue calcinado por la llama", 0)], "calcinado 2"),
    puesto("Y antes de seguir, dos", "Antes de seguir", "Dos comentarios", dur=2.2),
    com("David escribe que", C_DAVID, dur=13.6),
    com("Y Quixilero dice que diez", C_QUIXI, dur=7.6, x=.72, y=.36),
    puesto("David, para eso estamos", "Nosotros leemos las descripciones", "Tú, las responsabilidades", dur=4.4),
    puesto(("Y Quixilero, eso no", 0), "Quixilero", "No se lo digas a Miyazaki", dur=3.6),
    peg(("cierta sopa de escorpión", 0), "potaje", "Potaje de escorpión", dur=3.8, x=.70, y=.50, tam=360),

    # ================================================================ 3 · LOS DIOSES COLGADOS DE SUS LANZAS
    puesto("Número tres", "Atrocidad número 3", "Dioses en sus lanzas", dur=3.2),
    expe(2, "Los dioses colgados de sus lanzas", dur=2.3),
    com(("Messmer tenía que haber mucho", -.2), C_QUAERENS, dur=6.3),
    puesto(("Y casi nadie sabe de dónde", 0), "El apodo", "¿De dónde sale?", dur=3.4),
    ban_p(("No sale de empalar soldados", -.1), ("En el tráiler de la expansión", -.3), "No sale de empalar soldados",
          "Sale de los dioses ajenos", "apodo"),
    peg(("Sale de lo que hizo", 0), "leon", "Una bestia divina", dur=3.4, x=.80, y=.40, tam=360),
    pant("trailer_criatura_atravesada_lanzas", ("En el tráiler de la expansión", -.3),
         ("La tiranía de la llama de Messmer|fin", 1.0), zoom=(1.36, 1.42)),
    top(("En el tráiler de la expansión", -.1), ("una purga sin Gracia", -.3), "Tráiler oficial", "Leda lo resume así",
        "trailer leda"),
    peg(("Leda lo resume así", 0), "leda", "Leda", dur=3.0, x=.80, y=.40, tam=360),
    msg(["Una purga sin Gracia ni honor.", "La tiranía de la llama de Messmer."], ("una purga sin Gracia", -.2),
        ("La tiranía de la llama de Messmer|fin", 1.0), [("una purga sin Gracia", -.2), "La tiranía de la llama"],
        "purga leda"),
    peg(("Los cornamentados tenían bestias", 0), "cornamentado", "Los cornamentados", dur=3.4, x=.20, y=.50, tam=400),
    ban_p(("Los cornamentados tenían bestias", .8), ("Y en Belurat, el asentamiento", -.35), "Bestias divinas",
          "Mensajeras de los cielos", "bestias"),
    mapa("sombras", [pto(M_BELURAT, "Belurat", _P("belurat_plaza_fuente"), "inicio"),
                     pto(M_TORRE, "La torre", None, "meta")],
         ("Y en Belurat, el asentamiento", -.3), ("La Bestia divina León Danzante", -.2),
         ["Y en Belurat, el asentamiento", "de la torre, todavía queda"], titulo="Belurat", sub="Asentamiento de la torre",
         ventana=True, x=.66, y=.42, entrada="foco", traza=99),
    grande(("La Bestia divina León Danzante", 0), "leon", "León Danzante", lado="izq", dur=3.4, tam=600, y=.46),
    puesto(("Cuando la vences, te deja", 0), "Al vencerla", "Te deja un hechizo", dur=2.6),
    rel(("el Tornado de bestia divina", 0), "tornado_bestia", "Tornado de bestia divina", dur=12.0),
    ficha(("Y la descripción de ese hechizo", 0), "Tornado de bestia divina", "*La mayoría de las bestias divinas fueron "
          "destripadas y colgadas en las lanzas de Messmer, antes de ser calcinadas en sus llamas.* Quienes lo vieron lo "
          "comparan con una pira funeraria para la propia torre.", tipo="Encantamiento", icono="tornado_bestia",
          a=("funeraria para la propia torre|fin", .5)),
    peg(("Quienes lo vieron lo comparan", 0), "leon", "Bestia divina", dur=5.4, x=.20, y=.52, tam=400),
    mg(E.empalados(), ("Las destripaban, las colgaban", -.2), ("Y en japonés, el verbo", -.15),
       [("Las destripaban, las colgaban", 0), ("Las destripaban, las colgaban", .5), ("las colgaban y después", 0),
        ("las colgaban y después", .4), ("las colgaban y después", .8), "después las quemaban"], "empalados"),
    ban_p(("Y en japonés, el verbo", -.1), ("el mismo de su título|fin", .5), "En japonés", "El verbo es «empalar»",
          "japones"),
    peg(("es empalar, el mismo de", 0), "lanza_empalador", "Lanza del Empalador", dur=3.0, x=.20, y=.50, tam=400),
    mg(E.triada([("Sus enemigos", "no le dieron el título"), ("Dioses ajenos", "colgados de sus lanzas")],
                titulo="Por qué es el Empalador"),
       ("Messmer no es el Empalador", -.2), ("por los dioses de los demás|fin", 1.0),
       ["Messmer no es el Empalador", "Es el Empalador por los dioses"], "por que empalador"),

    # ---- 3b · el León Danzante y la anciana
    puesto("El León que tú mataste", "El León que mataste", "Fue de los que quedaron", dur=2.8),
    rel(("Su Recuerdo lo cuenta: al asaltar", 0), "recuerdo_leon", "Recuerdo del León Danzante", dur=9.8),
    ficha(("Su Recuerdo lo cuenta: al asaltar", 0), "Recuerdo del León Danzante", "Al asaltar la torre el ejército del "
          "Empalador, *el ritual de la danza del león tomó tintes marciales* […]", tipo="Recuerdo", icono="recuerdo_leon",
          a=("tomó tintes marciales|fin", .5)),
    puesto(("Una danza sagrada que tuvo", 0), "Una danza sagrada", "Que aprendió a pelear", dur=3.4),
    grande(("Antes del combate, una anciana", 0), "anciana", "Anciana cornamentada", lado="izq", dur=5.0, tam=500, y=.48),
    top(("Le pide que eche raíces", -.1), ("Que baile, y que limpie", -.2), "Canto de la anciana",
        "Echa raíces en los guardianes", "canto 1"),
    cam(("en los guardianes esculpidos", 0), "cabeza_bestia", "Guardianes esculpidos", dur=3.0, x=.84, y=.48,
        foco=(.5, .5, 1.0)),
    top(("Que baile, y que limpie", -.1), ("Que limpie a la vil progenie", -.2), "Canto de la anciana",
        "Baila y limpia la torre", "canto 2"),
    peg(("Que baile, y que limpie", 0), "leon", "La danza del león", dur=3.6, x=.20, y=.54, tam=380),
    top(("Que limpie a la vil progenie", -.1), ("de la ramera|fin", .6), "Canto de la anciana",
        "Limpia a la vil progenie", "canto 3"),
    grande(("La ramera es Márika", 0), "marika", "Márika", lado="der", dur=2.0, tam=560, y=.48),
    aba([("messmer", "Messmer"), ("miquella", "Miquella"), ("malenia", "Malenia"), ("morgott", "Morgott"), ("mohg", "Mohg")],
        ("Y su progenie, los hijos", .3), ("La bestia que te tocó", .5),
        [("Y su progenie, los hijos", .35), ("Y su progenie, los hijos", .4), ("los hijos de Márika", 0),
         ("los hijos de Márika", .4), ("los hijos de Márika|fin", 0)], "progenie", tam=240),
    ban_p(("La bestia que te tocó", .7), ("contra el Empalador|fin", .5), "La bestia que mataste",
          "Una plegaria contra él", "plegaria"),
    peg(("te tocó matar era la plegaria", 0), "leon", "León Danzante", dur=3.4, x=.20, y=.40, tam=360),
    rel(("Y cuando te llevas su máscara", 0), "cabeza_bestia", "Cabeza de bestia divina", dur=10.0),
    ficha(("Y cuando te llevas su máscara", 0), "Cabeza de bestia divina", "Máscara ritual con forma de la cabeza de una "
          "bestia divina capaz de llevar a cabo la danza del león. Usada por los mejores guardianes esculpidos. *Ya no "
          "responde a las sinceras plegarias de la anciana.*", tipo="Yelmo", icono="cabeza_bestia",
          a=("sinceras plegarias de la anciana|fin", .6)),
    ban_p(("Messmer colgó a sus dioses", -.1), ("Y tú te llevaste la cabeza", -.2), "Messmer", "Colgó a sus dioses",
          "colgo"),
    peg(("Y tú te llevaste la cabeza", 0), "cabeza_bestia", "La cabeza del último", dur=3.6, x=.76, y=.46, tam=420),
    ban_p(("Y tú te llevaste la cabeza", -.1), ("la cabeza del último|fin", .5), "Y tú", "Te llevaste su cabeza", "cabeza"),

    # ---- 3c · Pascual y la IA
    puesto(("Y hablando de cosas que", 0), "Un comentario", "Que no es lo que parece", dur=3.0),
    com("Pascual nos escribió", C_PASCUAL, dur=9.6),
    ban_p(("En este canal hay inteligencia", -.1), ("Y lo de los ejemplos modernos", -.25), "Pascual",
          "Aquí hay inteligencia artificial", "ia"),
    ban_p(("Y lo de los ejemplos modernos", -.1), ("comparaciones de este siglo|fin", .6), "Desde hoy",
          "Nada de este siglo", "este siglo"),
    leg("messmer", "Messmer", ["Cargo: señor feudal", "Plantilla: Caballeros Negros", "Recursos humanos: subterráneos"],
        ("Así que no diremos que", -.1), ("muy subterránea|fin", 1.0),
        [("Así que no diremos que", .3), "Diremos que era un señor", "una política de recursos humanos", "muy subterránea"],
        sello=("BAJO TIERRA", 3), y=.40),
    ban_p(("Así que no diremos que", -.1), ("con su plantilla|fin", .3), "Nada de", "«Jefe tóxico»", "toxico"),
    ban_p(("Diremos que era un señor", -.1), ("muy subterránea|fin", .9), "Señor feudal",
          "Recursos humanos subterráneos", "rrhh"),

    # ================================================================ 2 · LA SOPA FRÍA DE LA ABUELA
    puesto("Número dos", "Atrocidad número 2", "La sopa fría", dur=2.7),
    expe(3, "La sopa fría de la abuela", dur=2.4),
    ban_p(("el juego solo te deja hablar", -.1), ("con una víctima|fin", .4), "De todo un pueblo", "Una sola víctima con voz",
          "victima"),
    leg("anciana", "Anciana cornamentada", ["La del canto al León", "Encerrada en un almacén", "Belurat"],
        ("Es la anciana del canto", -.2), ("en un almacén de Belurat|fin", .3),
        [("Es la anciana del canto", .2), "Y la encuentras encerrada", "almacén de Belurat"]),
    mapa("sombras", [pto(M_BELURAT, "Belurat", _P("belurat_plaza_fuente"), "meta")],
         ("Y la encuentras encerrada", -.2), ("en un almacén de Belurat|fin", .3), ["almacén de Belurat"],
         titulo="Belurat", sub="Donde la encierran", ventana=True, x=.66, y=.42, entrada="foco"),
    pant("anciana_cornamentada_almacen_CONSUBTITULO", ("Cuando entras, te confunde", -.3),
         ("de sus viejos huesos|fin", .5), zoom=(1.30, 1.36), pan=(0, -1, 0, -1)),     # recorta el subtítulo en inglés (abajo)
    top(("Por tu aspecto, cree que", -.1), ("Te pregunta si los tuyos", -.2), "La anciana", "Te cree otro peón de Messmer",
        "peon"),
    top(("Te pregunta si los tuyos", -.1), ("de sus viejos huesos|fin", .5), "La anciana",
        "¿Qué os fascina de mis viejos huesos?", "huesos"),
    mg(E.estandartes(["Sus tierras", "Su torre", "Todo lo suyo"], remate="¿No os habéis regodeado bastante?",
                     titulo="Lo que te echa en cara", w=1500),
       ("Y luego lo suelta todo", -.2), ("regodeado ya bastante|fin", 1.0),
       ["Que sus tierras fueron", "Que su torre quedó", "Que vinisteis a robarlo", "Y que si no os habéis"], "echa en cara"),
    puesto(("Por esa ciudad encuentras", 0), "Por la ciudad", "Un objeto de comida", dur=2.3),
    peg(("El Potaje de escorpión: escorpión", 0), "potaje", "Potaje de escorpión", dur=10.6, x=.22, y=.46, tam=440),
    ficha(("El Potaje de escorpión: escorpión", 0), "Potaje de escorpión", "Escorpión cocido en una sopa negra. Receta típica "
          "de los cornamentados. […] *Antaño la preparaban con mimo las abuelas de la familia. Al haberse enfriado hace "
          "tiempo, esta sopa desprende un olor rancio y agrio.*", icono="potaje", a=("un olor rancio y agrio|fin", .6)),
    peg(("Antaño la preparaban con mimo", 0), "anciana", "Las abuelas de la familia", dur=5.0, x=.20, y=.50, tam=420),
    mg(E.sopa(icono=_G("potaje")), ("Una sopa que alguien hizo", -.2), ("No le hace falta|fin", 1.0),
       ["Una sopa que alguien hizo", "Y que se enfrió hace", "No le hace falta"], "sopa"),

    # ---- 2b · el Cornamentado
    peg(("La anciana tenía un hijo", 0), "anciana", "La anciana", dur=2.2, x=.80, y=.42, tam=360),
    grande(("Es el Cornamentado, el guerrero", 0), "cornamentado", "El Cornamentado", lado="izq", dur=4.6, tam=540, y=.46),
    peg(("del grupo de Miquella", 0), "miquella", "Miquella", dur=3.0, x=.80, y=.40, tam=360),
    ban_p(("En aquel video le llamamos", -.1), ("Se llama el Cornamentado", -.25), "En aquel video", "«Cornudo»: mal",
          "cornudo"),
    ban_p(("Se llama el Cornamentado", -.1), ("lo único que busca es venganza|fin", .5), "Se llama",
          "El Cornamentado", "nombre"),
    top(("La anciana te pide que", -.1), ("de Messmer y de los suyos|fin", .5), "La anciana",
        "Que su hijo vaya contigo y te vengues", "venganza"),
    peg(("La anciana te pide que", 0), "anciana", "La anciana", dur=3.6, x=.20, y=.44, tam=360),
    peg(("Y si ayudas al Cornamentado", 0), "cornamentado", "Hasta la arena de Messmer", dur=3.6, x=.76, y=.46, tam=420),
    ban_p(("entra en la arena diciéndole", -.1), (P_CORNA, -.05), "En la arena", "Se lo dice a Messmer", "arena"),
    # ---- PISTA 2: s_cornamentado (7,84 s)
    ban_p((P_CORNA, .1), (P_CORNA, 3.9), "El Cornamentado", "Messmer, foe of my beloved people", "pista cornamentado 1"),
    ban_p((P_CORNA, 4.0), (P_CORNA, 7.9), "El Cornamentado", "In vengeance for the flames, my blade I wield",
          "pista cornamentado 2"),

    # ---- 2c · su venganza, las almas, Leda, el mayal y la túnica
    top(("Messmer, enemigo de mi amado", -.1), ("empuño mi espada|fin", .6), "En español",
        "Enemigo de mi pueblo: empuño mi espada", "traduccion"),
    peg(("Messmer, enemigo de mi amado", 0), "cornamentado", "El Cornamentado", dur=3.4, x=.20, y=.46, tam=360),
    peg(("En venganza por las llamas", 0), "messmer", "Messmer", dur=3.0, x=.80, y=.46, tam=360),
    mg(E.cadena(["Su clan", "Su dolor", "Lo que sintieron"], preso="Messmer", amo="El Cornamentado", remate="«Tu fealdad»",
                titulo="¿Lo entiendes ahora?"),
       ("Y en plena pelea le", -.2), ("Tu fealdad, le dice|fin", 1.0),
       ["el sufrimiento de su clan", "su dolor, todo lo", "todo lo que sintieron", "Tu fealdad, le dice"], "fealdad"),
    pant("messmer_fase2_cubre_rostro", ("Cuando Messmer cae, el Cornamentado", -.3), ("una maraña de serpientes|fin", .6)),
    top(("te cuenta que le vio", -.1), ("Y que cómo se atrevió", -.25), "El Cornamentado",
        "Le vio la cara: una maraña de serpientes", "marana"),
    top(("Y que cómo se atrevió", -.1), ("el más vil de todos|fin", .5), "El Cornamentado",
        "¿Salvajes? Él era el más vil", "salvajes"),
    peg(("Y que cómo se atrevió", 0), "cornamentado", "El Cornamentado", dur=3.4, x=.20, y=.46, tam=360),
    ban_p(("En japonés no dice salvajes", -.1), ("Dice inmundicia|fin", .7), "En japonés", "No «salvajes»: «inmundicia»",
          "inmundicia"),
    cam(("Y si no llega a vengarse", 0), "cornamentado", "Sin venganza", dur=3.0, x=.84, y=.46, foco=(.5, .25, 1.6)),
    top(("sus últimas palabras son para", -.1), ("amadísima esposa e hijo|fin", .7), "Sus últimas palabras",
        "Oh madre, oh esposa, oh hijo", "ultimas"),
    peg(("para su familia: oh madre", 0), "anciana", "Su madre", dur=3.4, x=.20, y=.46, tam=360),
    mapa("sombras", [pto(M_LLANURA, "Llanura de las Tumbas", None, "inicio"),
                     pto(M_CALCIN, "Ruinas calcinadas", _P("ruinas_calcinadas"), "meta")],
         ("En la Llanura de las Tumbas", -.3), ("Dice que todos ardieron", -.3),
         ["En la Llanura de las Tumbas", "junto a las Ruinas calcinadas"], titulo="Llanura de las Tumbas",
         sub="Ruinas calcinadas", entrada="desenrolla", traza=1.7),
    pant("ruinas_calcinadas", ("Dice que todos ardieron", -.35), ("vivían su vida en paz|fin", .5)),
    top(("Dice que todos ardieron", -.1), ("Que qué hicieron para", -.2), "Un alma de la llanura",
        "Nos quemaron Messmer y los suyos", "alma quemados"),
    top(("Que qué hicieron para", -.1), ("vivían su vida en paz|fin", .5), "Un alma de la llanura",
        "¿Qué hicimos? Vivíamos en paz", "alma paz"),
    ban_p(("Ojo, que aquí no hay", -.3), ("La caballera Leda te", 0), "Ojo", "Aquí no hay santos", "santos"),
    grande(("La caballera Leda te", 0), "leda", "Leda", lado="izq", dur=4.4, tam=520, y=.50),
    top(("fue la reina Márika la", -.1), ("una limpieza por fuego|fin", .6), "Según Leda",
        "Márika ordenó purgar la torre", "leda marika"),
    peg(("fue la reina Márika la", .2), "marika", "Márika", dur=3.4, x=.80, y=.46, tam=360),
    mg(E.balanza("Un alma de la llanura", "Leda", [("i", "Vivían en paz"), ("d", "Nunca fueron santos"),
                                                   ("d", "Del lado perdedor")],
                 remate="Aun así, la sopa se enfrió", titulo="¿Eran inocentes?"),
       ("Pero también te dice", -.2), ("Aun así, la sopa se enfrió|fin", .8),
       [("Pero también te dice", 0), "nunca fueron santos", "del lado perdedor de una", "Aun así, la sopa se enfrió"],
       "leda"),
    rel(("Y el Mayal de serpiente", .7), "mayal", "Mayal de serpiente", dur=13.6),
    ficha(("un arma de su ejército, deja", 0), "Mayal de serpiente", "El fuego ruge en el interior de los cuerpos de las "
          "serpientes, infligiendo terribles quemaduras. Algunos del ejército de Messmer usaron estos mayales para *quemar a "
          "los cornamentados y marcarlos con agonía y miedo*.", tipo="Mayal", icono="mayal",
          a=("con agonía y miedo|fin", .6)),
    rel(("la Túnica de cordón trenzado", 0), "tunica_cordon", "Túnica de cordón trenzado", dur=13.0),
    ficha(("la Túnica de cordón trenzado", 0), "Túnica de cordón trenzado", "Atavío de los cornamentados en busca de "
          "venganza. *El cordón trenzado une el juramento del vengador al rencor de las víctimas. Jamás debe deshacerse.*",
          tipo="Armadura", icono="tunica_cordon", a=("Jamás debe deshacerse|fin", .7)),

    # ================================================================ COMENTARIOS Y CAMPAÑA
    puesto(("Antes del número uno, varios", 0), "Antes del número uno", "Varios comentarios", dur=2.8),
    com("Shiro buscaba algo que", C_SHIRO, dur=8.7),
    puesto("Shiro, tu jefe no se", "Shiro", "Tu jefe no se va a enterar", dur=3.3),
    com("Ulises entró a escuchar", C_ULISES, dur=5.4, x=.72, y=.36),
    com("Y Daniel nos sigue", C_DANIEL, dur=4.4),
    ban_p(("A día de hoy ya somos", -.1), ("Gracias de corazón|fin", .3), "Runa Caída", "1 300 suscriptores",
          "mil trescientos"),
    mg(E.cien("De cada 100 vistas de Runa Caída", 8, remate=("Meta: 2 000", 2)), ("Aun así, de cada cien", -.2),
       ("objetivo son dos mil|fin", .8), ["Aun así, de cada cien", "menos de nueve son de gente", "El siguiente objetivo son"],
       "cien", y=.46),
    mg(E.acuerdo(["Ser Caballero de Fuego"], "Te costaba la casa", letra="Aquí solo es un botón", titulo="Jurar lealtad",
                 remate="Suscríbete", cab=("Messmer te da", "Tú pones")),
       ("A los Caballeros de Fuego, jurarle", -.2), ("Aquí solo es un botón|fin", .6),
       ["A los Caballeros de Fuego, jurarle", "les costó la casa", ("Aquí solo es un botón", -.3),
        ("Aquí solo es un botón", .3)], "oferta"),
    msg(["Intenta suscribirte."], ("Aquí solo es un botón|fin", .7), ("se leen, uno por uno|fin", .2),
        [("Aquí solo es un botón|fin", .8)], "suscribete"),
    puesto("con ellos se decide lo que", "Los comentarios", "Deciden lo que viene", dur=3.0),

    # ================================================================ 1 · LA MEDALLA QUE LLEVASTE COLGADA
    puesto("Número uno#4", "Atrocidad número 1", "La medalla colgada", dur=2.8),
    expe(4, "La medalla que llevaste colgada", dur=2.6),
    ban_p(("Esta la llevaste tú", .1), ("Esta la llevaste tú|fin", .7), "Las otras cuatro las hizo él",
          "Esta la llevaste tú", "llevaste"),
    pant("belurat_plaza_fuente", ("En Belurat, la misma ciudad", -.3), ("te invade un espíritu rojo|fin", .6)),
    ban_p(("En Belurat, la misma ciudad", -.1), ("el Caballero de Fuego Queelign", -.2), "Belurat",
          "La ciudad de la anciana", "belurat"),
    grande(("el Caballero de Fuego Queelign", 0), "queelign", "Caballero de Fuego Queelign", lado="izq", dur=4.2, tam=560,
           y=.50),
    top(("le grita a la reina Márika", -.1), ("cáncer de su alegría|fin", .5), "Queelign",
        "Mira, reina: otro cáncer extirpado", "cancer"),
    peg(("le grita a la reina Márika", .3), "marika", "Márika", dur=3.4, x=.80, y=.46, tam=360),
    ban_p(("El cáncer eras tú", -.1), ("El cáncer eras tú|fin", .7), "El cáncer", "Eras tú", "cancer tu"),
    peg(("Queelign quería ser como", 0), "espadon_queelign", "Espadón de Queelign", dur=10.0, x=.22, y=.46, tam=440),
    ficha(("Queelign quería ser como", 0), "Espadón de Queelign", "Queelign se volcó en su cruzada y reforjó este espadón "
          "con la forma de la lanza de su soberano, *con la esperanza de ser un segundo empalador*", tipo="Espadón",
          icono="espadon_queelign", a=("ser un segundo empalador|fin", .5)),
    cam(("Iris de la Gracia, te", 0), "iris_gracia", "Iris de la Gracia", dur=3.8, x=.17, y=.44, foco=(.5, .5, 1.0)),
    ficha(("te regala sus cenizas de", 0), "Caballero de Fuego Queelign", "Blande un espadón en forma de lanza que *empala al "
          "enemigo en fuego para alejar a la bella madre Márika de la impureza*. […] Y una vez salvado, lo único que le "
          "quedaba era la guerra.", tipo="Cenizas de espíritu", icono="queelign", a=("le quedaba era la guerra|fin", .6)),
    peg(("para alejar a la bella madre", 0), "marika", "La bella madre Márika", dur=4.4, x=.20, y=.50, tam=400),
    puesto(("Cuando lo vences, te deja", 0), "Al vencerlo", "Te deja un talismán", dur=2.4),
    ban_p(("Casi todo el mundo se lo puso", -.1), ("el efecto es muy bueno|fin", .3), "Casi todo el mundo",
          "Se lo puso sin leerlo", "sin leerlo"),
    grande(("La Insignia de cruzada. Talismán", 0), "insignia", "Insignia de cruzada", lado="izq", dur=2.6, tam=520, y=.46),
    rel(("Talismán con una lanza alzada", 0), "insignia", "Insignia de cruzada", dur=12.2),
    ficha(("Talismán con una lanza alzada", 0), "Insignia de cruzada", "Talismán con una lanza alzada sobre un fondo "
          "llameante, en recuerdo de los caídos en la cruzada sagrada liderada por Messmer. *Aumenta la potencia de ataque "
          "tras derrotar a un enemigo.* […]", tipo="Talismán", icono="insignia", a=("Y sigue. Los cruzados", -.15)),
    ficha(("Y sigue. Los cruzados", 0), "Insignia de cruzada", "[…] Los cruzados olvidaron el honor y la piedad para *empalar "
          "y quemar sin misericordia a quienes consideraban impuros*. *Quienes se sentían estimulados por los gritos de "
          "muerte eran los mismos que abogaban por la santidad de la campaña.*", tipo="Talismán", icono="insignia",
          a=("la santidad de la campaña|fin", .5)),
    peg(("Y sigue. Los cruzados", .2), "soldado_messmer", "Los cruzados", dur=6.0, x=.20, y=.52, tam=420),
    peg(("Quienes se sentían estimulados", 0), "messmer", "Messmer", dur=5.2, x=.20, y=.44, tam=360),

    # ---- 1b · la medalla, otra vez; despojado de luz
    mg(E.medalla(_G("insignia")), ("Léelo otra vez", -.2), ("Rico, esta era la medalla|fin", .9),
       ["Léelo otra vez", "Aumenta el ataque tras derrotar", "cada vez que matas", "Como a ellos con los gritos",
        "Rico, esta era la medalla"], "medalla"),
    mapa("sombras", [pto(M_BELURAT, "Belurat", _G("insignia"), "inicio"),
                     pto(M_FORT, "Fortaleza sombría", _G("messmer"), "meta")],
         ("Y ahora la pregunta importante", .3), ("en cuanto entras en su sala|fin", 1.0),
         [("Y ahora la pregunta importante", .3), "en cuanto entras en su sala"], titulo="La sala de Messmer",
         sub="De Belurat a la Fortaleza sombría", entrada="pliegue", traza=99),
    msg(["Intruso sarnoso. Eres un Sinluz, según parece.", "Madre, ¿acaso tu verdadero señorío sanciona",
         "a alguien tan despojado de luz?"],
        ("Te llama intruso sarnoso", -.1), (P_MADRE, -.6),
        ["Te llama intruso sarnoso", "Y le pregunta a su madre", "señorío sanciona a alguien"], "sarnoso"),
    peg(("Te llama intruso sarnoso", 0), "messmer_jefe", "Messmer", dur=4.2, x=.80, y=.36, tam=360),
    # ---- PISTA 3: s_madre_sanciona (8,54 s)
    ban_p((P_MADRE, .1), (P_MADRE, 4.4), "Messmer", "Mother, wouldst thou truly Lordship sanction", "pista madre 1"),
    ban_p((P_MADRE, 4.5), (P_MADRE, 8.8), "Messmer", "in one so bereft of light?", "pista madre 2"),

    # ---- 1c · la cruzada contra ti; Runa de Márika; Retos
    ban_p(("Te llama despojado de luz", -.1), ("Y ahora vuelve a la frase", -.3), "Te llama", "Despojado de luz",
          "despojado"),
    mg(E.despojados(remate="Una cruzada que existía para matarte"), ("Y ahora vuelve a la frase", -.2),
       ("que existía para matarte|fin", 1.0),
       ["quienes se ven despojados#2", "contra un pueblo. Era", "Era contra todo el que", "no tuviera la gracia del oro",
        "la definición exacta", "que existía para matarte"], "despojados"),
    puesto(("Y para rematarlo", .2), "Y para rematarlo", "La Runa de Márika", dur=3.2),
    rel(("recoges la Runa de Márika", 0), "runa_marika", "Runa de Márika", dur=14.0),
    ficha(("recoges la Runa de Márika", 0), "Runa de Márika", "Restos dorados de la Gracia concedida personalmente por la "
          "reina Márika a *los héroes que se unieron a la cruzada por ella*. Úsalos para obtener 80.000 runas.",
          icono="runa_marika", a=("cobrar ochenta mil runas|fin", .6)),
    rel(("Messmer lo dejó escrito en", 0), "armadura_messmer", "Armadura de Messmer", dur=12.0),
    ficha(("Messmer lo dejó escrito en", 0), "Armadura de Messmer", "Por deseo de su madre, Messmer se convirtió en un "
          "símbolo aterrador para llevar a cabo la cruzada purificadora que ella ansiaba. *\"Centra en mí, y solo en mí, tus "
          "maldiciones, tu ira y tu pesar\".*", tipo="Armadura", icono="armadura_messmer",
          a=("tu ira y tu pesar|fin", .6)),
    peg(("una frase entre comillas", 0), "messmer", "Messmer", dur=5.6, x=.20, y=.44, tam=360),
    puesto(("Y aquí va el último comentario", 0), "El último comentario", "De hoy", dur=2.2),
    com("Retos nos escribió", C_RETOS, dur=9.0),
    ban_p(("Coincidimos en lo importante", -.1), ("Para todo lo demás", -.25), "Coincidimos", "El lore está bien", "lore"),
    ban_p(("Para todo lo demás", -.1), ("nosotros por ti|fin", .4), "Para todo lo demás", "Ya lo jugamos por ti",
          "jugamos"),
    grande(("Y Messmer te daría la razón", 0), "messmer_jefe", "Messmer", lado="der", dur=5.9, tam=520, y=.46),

    # ================================================================ CIERRE
    mg(E.expediente(acusado="Messmer el Empalador", sub="hijo de Márika, señor del Reino de las Sombras", cargos=CARGOS,
                    ya=0, sello="CULPABLE", titulo="El Empalador, juzgado"),
       ("Esa es la lista", -.2), ("que te colgaste tú|fin", .8),
       ["Sus propios caballeros, encerrados", "Un sabio que quemó más", "Los dioses de otro pueblo, colgados",
        "Una sopa que se enfrió", "Y una medalla para los", "que te colgaste tú"], "expediente cierre"),
    puesto(("Pero hay una última cosa", .1), "Una última cosa", "En tu inventario", dur=3.4),
    rel(("La Bendición de Márika: una", 0), "bendicion_marika", "Bendición de Márika", dur=16.2),
    ban_p(("una medicina especial bendecida", -.1), ("te cura todo de golpe|fin", .4), "Bendición de Márika",
          "Te cura todo de golpe", "bendicion"),
    top(("En inglés y en japonés", -.1), ("Y nunca más|fin", .9), "En inglés y en japonés",
        "Hizo varias para Messmer… y nunca más", "nunca mas"),
    peg(("Márika hizo varias de estas", 0), "marika", "Márika", dur=3.6, x=.80, y=.46, tam=360),
    mg(E.domino(["Le arrancó el ojo", "Lo escondió", "Le hizo medicinas", "Nunca más"], titulo="Lo que hizo su madre",
                w=1560),
       ("La madre que le arrancó", -.2), ("Y te las bebiste tú", -.15),
       ["La madre que le arrancó", "y lo escondió en el", "le hizo medicinas una", "nunca más volvió a hacerlo"], "madre"),
    peg(("Y te las bebiste tú", 0), "bendicion_marika", "Te las bebiste tú", dur=2.5, x=.20, y=.50, tam=400),
    peg(("Su Recuerdo lo cierra así", .1), "recuerdo_empalador", "Recuerdo del Empalador", dur=7.0, x=.22, y=.46, tam=440),
    ficha(("Su Recuerdo lo cierra así", .1), "Recuerdo del Empalador", "[…] Sin embargo, su miedo la obligó luego a esconder a "
          "su hijo en el Reino de las Sombras. *Oculto junto al pecado original, su odio fue creciendo.*", tipo="Recuerdo",
          icono="recuerdo_empalador", a=("su odio fue creciendo|fin", .6)),
    pant("messmer_fase2_mano", ("Y cuando por fin lo vences", -.3), (P_MALDI, -.1)),
    ban_p(("su último aliento no es", -.1), (P_MALDI, -.05), "Su último aliento", "No es para ti", "aliento"),
    # ---- PISTA 4: s_maldicion (7,73 s)
    ban_p((P_MALDI, .1), (P_MALDI, 7.8), "Messmer", "Mother… Marika… A curse upon thee", "pista maldicion"),

    # ---- cierreb · la maldición, los próximos y la colección
    mg(E.ecos(["Madre...", "Márika...", "Una maldición... caerá sobre ti..."], firma="a su madre",
              revela="a Márika, por su nombre", titulo="Su último aliento"),
       ("Madre. Márika. Una maldición", -.2), ("Messmer quemó un reino entero", -.2),
       ["Madre. Márika. Una maldición", ("Madre. Márika. Una maldición", .7), "Una maldición caerá sobre",
        "Es la única vez en todo"], "ecos maldicion"),
    peg(("Messmer quemó un reino entero", 0), "marika", "Su madre", dur=4.0, x=.20, y=.42, tam=360),
    ban_p(("Messmer quemó un reino entero", -.1), ("Y lo último que le dejó", -.25), "Por su madre",
          "Quemó un reino entero", "quemo reino"),
    ban_p(("Y lo último que le dejó", -.1), ("fue una maldición|fin", .5), "Y lo último que le dejó", "Una maldición",
          "maldicion"),
    com("Santiago, que nos pidió", C_SANTIAGO, dur=5.2),
    grande(("Bayle el Temible", 0), "bayle", "Bayle el Temible", lado="der", dur=3.2, tam=560, y=.46),
    aba([("rennala", "Rennala"), ("maliketh", "Maliketh"), ("parches", "Parches"), ("zampaheces", "Zampaheces"),
         ("gideon", "Gideon")],
        ("Y en los comentarios siguen", -.1), ("Dinos cuál quieres|fin", .7),
        ["siguen Rennala, Maliketh", ("Rennala, Maliketh, Parches", .5), ("Maliketh, Parches", .5), "y el Zampaheces",
         "con Gideon"], "proximos", tam=250),
    aba([("marika", "Márika"), ("radagon", "Radagon"), ("miquella", "Miquella"), ("malenia", "Malenia"), ("ranni", "Ranni"),
         ("melina", "Melina")],
        ("En el canal tienes las", -.2), ("Radahn, Morgott, Mohg", -.25),
        ["de Márika y Radagon", ("de Márika y Radagon|fin", -.2), "de Miquella, Malenia", ("de Miquella, Malenia|fin", -.1),
         "Ranni, Melina", ("Ranni, Melina", .4)], "canal 1", tam=240),
    aba([("radahn", "Radahn"), ("morgott", "Morgott"), ("mohg", "Mohg"), ("godrick", "Godrick"), ("godfrey", "Godfrey"),
         ("rykard", "Rykard")],
        ("Radahn, Morgott, Mohg", -.1), ("y las tuyas|fin", .5),
        ["Radahn, Morgott, Mohg", ("Radahn, Morgott, Mohg", .5), ("Morgott, Mohg, Godrick", .5), "Godrick, Godfrey",
         ("Godrick, Godfrey", .5), "Rykard, y las tuyas"], "canal 2", tam=240),
    puesto(("Suscríbete, que vamos por", 0), "Suscríbete", "Vamos por los 2 000", dur=3.4),
    cam(("Y si te gustan los mundos", 0), "radagon", "Hasta los dioses", dur=3.4, x=.16, y=.40, foco=(.5, .35, 1.3)),
    ban_p(("Crónicas de Tamriel, nuestro canal", -.3), ("Te lo dejo aquí al final|fin", .9), "Canal hermano",
          "Crónicas de Tamriel", "tamriel"),
    rel(("Y la próxima vez que un talismán", 0), "insignia", "Insignia de cruzada", "léela antes de ponértela", dur=7.4),
    ban_p(("léelo antes de ponértelo", -.1), ("A lo mejor la medalla", -.25), "Antes de ponértelo", "Léelo", "leelo"),
    grande(("A lo mejor la medalla", 0), "messmer", "Messmer", lado="der", dur=4.8, tam=540, y=.46),
    ban_p(("A lo mejor la medalla", -.1), ("estaban buscando|fin", 1.2), "A lo mejor la medalla",
          "Es de los que te buscaban", "te buscaban"),
]

FX = [d for d in FX if d]
if FALTAN:
    print("efectos.py: pantallas que aún no existen (cubiertas con su alternativa):", " ".join(sorted(set(FALTAN))))
