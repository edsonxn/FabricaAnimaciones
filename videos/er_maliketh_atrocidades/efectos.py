# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «5 atrocidades de Maliketh que el juego te ESCONDIÓ» (SECUENCIA YT, Runa Caída, 27-nov-2026).
Molde: videos/er_messmer_atrocidades/efectos.py · plan: _fx_plan.md · reglas: docs/estilo_secuencia_yt.md § REGLA DE ORO y
§ Runa Caída. Kit nucleo/mg_er.py + peg_estilos/peg_anim (tema «er»).
- FICHAS = solo citas en español verificadas (_investigacion/dossier.md § 1-3, [EG]); lo que solo existe en inglés (líneas de
  Maliketh salvo «Oh, Muerte…», TODO Gurranq y D, el diálogo RECORTADO, la narración del tráiler) va PARAFRASEADO en rótulos
  `puesto` (arriba y=.10 `top()`, o abajo `ban_p()`) o dentro de un MG, nunca entre comillas en una ficha. La «Garra de la
  bestia Gurranq» (p3) tampoco va en ficha: el dossier solo tiene un fragmento y de «Garra de bestia».
- HILO DEL VIDEO: `expediente` de la fiscalía (abre en introb «la fiscalía trae cinco pruebas»; un cargo por puesto; sello
  PROBADO en el cierre «Esa es la lista»).
- MG NUEVOS (mg_er, 27-nov): retal (avance en introb; completo en p5b) · recambio (p4b: Gurranq ← D ← Tú) · nombre_bestia
  (p3: «Muerte de los Semidioses») · jaula_orden (p3b, 3 marcas; vuelve en cierrec con la 4.ª: la Muerte, libre) · pruebas
  (p1b: Aojo, Armadura de Cuchillo Negro, Recuerdo → «¿Márika?», SOLO como pregunta) · dos_muertes (cierrec, sin comillas).
  Reusados con datos nuevos: sombra (gancho y p1b), domino (adipocira), balanza ×2 (p5b, p2b), recibo (el trato de las
  raíces), muerte_suelta (p3b), estandartes (p2), estandarte_caido (p2b), cien + acuerdo (subs), cadena (p1), triada (p1d).
- MAPAS (mapas/mundo.jpg, coordenadas del dossier § 4; los NO MEDIDOS —catacumbas, Tierras prohibidas, Necrolimbo— NO se
  usan): intro Farum Azula · p5 Montedrago → Santuario de la bestia · p4 Árbol Áureo → Santuario · p3 Farum Azula · p2
  Santuario → Torre Sagrada de Caelid · p1b Santuario · cierrec Farum Azula → Leyndell.
- PISTAS voz=True (cortes en sfx/, `post` en guion.py): s_espada (intro), s_enganaste (p1b), s_recortado (p1c), s_necio
  (cierre), s_perdon (cierreb); durante cada una SOLO el rótulo de lo que se oye, traducido, abajo (y=.80).
- Maliketh con CARA = pegatinas/maliketh_cara.png (recorte de miniatura/ing_maliketh.png); maliketh*.png/clerigo.png son la
  Bestia Clériga agachada (sin cara): solo como «el clérigo del santuario».
  FAB_FX_FINAL=1 python fab.py er_maliketh_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALAS TODAS)
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


CON_CARA = {"gurranq", "clerigo", "marika", "ranni", "rykard", "bayle", "asesina_cuchillo", "pielesdivinas", "godwyn",
            "ave_muerte_cerca"}   # el vitral las vuelve ilegibles


def peg(en, slug, titulo, dur=4.0, x=.17, y=.62, tam=400, **fijo):
    """Pegatina con animación de presentación variada (nucleo/peg_anim.py, regla del 5-nov-2026); los comentarios, tarjeta fija."""
    if slug.startswith("com_"):
        return dict(tipo="mg", fn=T.pegatina(_G(slug), titulo, tam), en=en, dur=dur, x=x, y=y, sale=.3,
                    nombre="pegatina " + slug, ver=1.0)
    import peg_anim as PA
    if (slug.endswith("_cara") or slug in CON_CARA) and "marco" not in fijo:   # vitral y cristal tapan la cara (25-nov)
        rec = PA.es_recorte(_G(slug))
        rot = PA.rotador(PA._video_de(_G(slug)), TEMA)
        fijo["marco"] = rot._saca("marco" + ("R" if rec else ""), [m for m in PA.MARCOS_TODOS if rec or m != "aura"],
                                  lambda o: o not in ("cristal", "vitral"), ult="marco")
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


# Comentarios (ESTADO.md, leídos el 27-nov; tarjetas en pegatinas/com_<id>.png). Cada uno UNA vez (Diego: crítica en introb y
# su remate en p1d, mismo comentario y misma persona, dentro de este video).
C_AYLAN, C_BAUTI, C_PISO = "UgySmUGdjRfjJxkBcX94AaABAg", "UgxoCYU4dtPLXve5bl14AaABAg", "UgzBDd9Lo8N3FkUbdBd4AaABAg"
C_DIEGO, C_EDGAR, C_DARK = "Ugyq6VrXBUyp9nIRFVx4AaABAg", "UgyB1EoWLW8OFtGeOMh4AaABAg", "UgwSM-kZWs4crUYmDih4AaABAg"
C_JONATAN, C_NOVIA = "UgzctI4k2oDTuBdFzuR4AaABAg", "UgxPfvjIQIZU-ZQM8_94AaABAg"
C_BRYAN, C_ALBERTO = "UgyIXFYc9OQgyjwcpfB4AaABAg", "UgypNy1lYYyWaXbJoit4AaABAg"
C_ASTORA, C_LISSOM = "UgzGKL5gZgOIwF1SwsN4AaABAg", "UgwqsA6iIqCgJqVSd754AaABAg"

# Coordenadas (fracción de mapas/mundo.jpg = mundo_rejilla.jpg; dossier § 4). NO MEDIDOS (no se usan): catacumbas de los
# Cuchillos Negros, Tierras prohibidas, Aldea de Aguainvocante/Necrolimbo, arena exacta de Maliketh.
M_SANT = (.617, .600)        # Santuario de la bestia (✅ por forma: planta cuadrada con círculo, punta norte de Montedrago)
M_PUENTE_N = (.638, .61)     # puente largo hacia el sur (paso de la ruta)
M_MONTEDRAGO = (.638, .66)   # extremo sur del puente, dentro de la región Montedrago (≈ .62–.66, .60–.66)
M_TORRE = (.518, .637)       # Torre Sagrada de Caelid (⚠ por forma: torre redonda en un islote)
M_FARUM = (.886, .493)       # Farum Azula, la ciudad en ruinas (⚠ el remolino del este; Rykard .87 .48)
M_LEYNDELL = (.45, .39)      # Leyndell, capital del Reino (⚠ por forma; Rykard .44 .37)
M_ARBOL = (.49, .42)         # Árbol Áureo (✅ el dibujo dorado)

CARGOS = ["Guardias remendados con muertos", "Un cazador para el trabajo sucio", "Se llamaba Muerte de los Semidioses",
          "Selló el poder de los recién nacidos", "Dejó robar la Muerte"]


def expe(k, frase, dur=2.6):
    """Ficha de la fiscalía al abrir el puesto k (0 = n.º 5): escribe el cargo k (el sello PROBADO cae en el cierre)."""
    return mg(E.expediente(acusado="Maliketh, la Hoja Negra", sub="sombra de Márika, guardián de la Runa de la Muerte",
                           cargos=CARGOS[:k + 1], ya=k, sello=None, titulo="La fiscalía contra la Hoja Negra",
                           ritmo=.015, tmin=.3),
              (frase + "|fin", -.4), (frase + "|fin", dur), [(frase + "|fin", -.3)], f"expediente {k + 1}")


# Los 5 sonidos ORIGINALES con la voz callada (regla del 31-oct-2026 y regla 10; cortes en sfx/, `post` en guion.py)
P_ESPADA = "le habla a la muerte. Escúchalo|fin"
P_ENGANASTE = "son para ella. Escúchalo|fin"
P_RECORTADO = "a esta historia. Escúchalo|fin"
P_NECIO = "te desprecia. Escúchalo|fin"
P_PERDON = "último aliento cambia. Escúchalo|fin"
PISTAS = [
    dict(sfx="s_espada", en=P_ESPADA, vol=1.0, voz=True),
    dict(sfx="s_enganaste", en=P_ENGANASTE, vol=1.0, voz=True),
    dict(sfx="s_recortado", en=P_RECORTADO, vol=1.0, voz=True),
    dict(sfx="s_necio", en=P_NECIO, vol=1.0, voz=True),
    dict(sfx="s_perdon", en=P_PERDON, vol=1.0, voz=True),
]

FX = [
    # ================================================================ GANCHO
    grande(("Maliketh, la Hoja Negra. La", 0), "maliketh_cara", "Maliketh, la Hoja Negra", lado="izq", dur=2.1, tam=560,
           y=.46),
    mg(E.sombra(ama="Márika", sombra_="Maliketh", amos="Los Dos Dedos", titulo="La sombra de la reina"),
       ("La sombra de la reina Márika", -.2), ("el guardián de la Runa", -.1),
       [("La sombra de la reina Márika", 0), ("de la reina Márika", .3)], "sombra gancho"),
    rel(("el guardián de la Runa", 0), "runa_muerte", "Runa de la Muerte", "su guardián", dur=3.2, x=.24, y=.44, tam=440),
    mapa("mundo", [pto(M_FARUM, "Farum Azula", _P("farum_wiki"), "poder")],
         ("y el jefe que te espera", -.2), ("con una espada hecha de", -.15), [("al final de Farum Azula", 0)],
         titulo="Farum Azula", sub="La ciudad en ruinas", ventana=True, x=.66, y=.42, entrada="foco"),
    rel(("con una espada hecha de", 0), "espada_maliketh", "Hoja negra de Maliketh", dur=2.6, x=.24, y=.44, tam=460),
    pant("hoja_negra_sale_del_cuerpo", ("cosida a su propia carne", -.2), ("levanta esa espada y le", -.1), zoom=(1.0, 1.08)),
    ban_p(("A mitad del combate, levanta", -.1), ("No te habla a ti", -.2), "A mitad del combate", "Levanta la espada",
          "mitad combate"),
    pant("maliketh_revelado_hoja", ("No te habla a ti", -.2), (P_ESPADA, -.05), zoom=(1.0, 1.06)),
    ban_p(("No te habla a ti", -.1), (P_ESPADA, -.05), "No te habla a ti", "Le habla a la Muerte", "habla muerte"),
    # ---- PISTA 1: s_espada (4,65 s) — solo el rótulo de lo que se oye (frase verificada en español, [ES-wiki])
    ban_p((P_ESPADA, .1), (P_ESPADA, 4.75), "Maliketh · en inglés", "Oh, Muerte. Conviértete en mi espada una vez más",
          "pista espada"),

    # ---- introb · la frase, la versión de siempre, el avance y los pedidos
    msg(["Oh, Muerte.", "Conviértete en mi espada una vez más."], ("Oh, Muerte. Conviértete", -.2),
        ("en mi espada una vez más|fin", .9), [("Oh, Muerte. Conviértete", 0), ("Conviértete en mi espada", 0)], "oh muerte"),
    cam(("Y lo que dice es esto: Oh", 0), "maliketh_cara", "Maliketh", dur=6.6, x=.84, y=.36, foco=(.5, .5, 1.1)),
    puesto(("Casi todo el mundo cree que Maliketh", 0), "Lo que todos creen", "Maliketh, la víctima", dur=3.4),
    peg(("El perro fiel de Márika", 0), "maliketh_cara", "El perro fiel de Márika", dur=3.0, x=.80, y=.40, tam=360),
    cam(("al que le robaron la muerte", 0), "runa_muerte", "Le robaron la Muerte", dur=2.6, x=.17, y=.46, foco=(.5, .5, 1.0)),
    grande(("y que acabó escondido en", 0), "clerigo", "Escondido, comiendo raíces", lado="der", dur=3.6, tam=560, y=.46),
    ban_p(("Y algo de eso es verdad", -.1), ("Y algo de eso es verdad|fin", .9), "Y algo de eso", "Es verdad", "verdad"),
    puesto(("Pero el juego esconde otra cosa", 0), "Pero el juego", "Esconde otra cosa", dur=2.6),
    mg(E.retal(remate=""), ("Unos guardias remendados con", -.2), ("Un cazador que hacía el", -.2),
       [("Unos guardias remendados con", 0), ("con grasa de muertos", 0)], "retal avance"),
    aba([("d_cazador", "Un cazador"), ("piedra_gurranq", "Un nombre"), ("mano_cuchilla", "Una reina"),
         ("maliketh_cara", "Una frase")],
        ("Un cazador que hacía el", -.2), ("y luego quitó del juego|fin", .8),
        ["Un cazador que hacía el", "Un nombre que hacía temblar", "Una reina que acunaba recién",
         "Y en el número uno, una"], "avance", y=.56, tam=280),
    puesto(("Este video lo pidieron ustedes", 0), "Lo pidieron ustedes", "Y aquí está", dur=2.4),
    com(("Aylan escribió que lo esperaba", 0), C_AYLAN, dur=3.55),
    com(("Bauti, que este semidiós tiene", 0), C_BAUTI, dur=3.25, x=.72, y=.36),
    com(("Y Piso Papas ya gritaba", 0), C_PISO, dur=4.6),
    com(("Y luego está Diego, que", 0), C_DIEGO, dur=11.4),
    peg(("servir a una tirana", 0), "marika", "¿La tirana?", dur=3.2, x=.80, y=.46, tam=360),
    ban_p(("Diego, la defensa ya habló", -.1), ("Y la fiscalía trae cinco", -.3), "La defensa ya habló",
          "Ahora, la fiscalía", "fiscalia"),
    mg(E.expediente(acusado="Maliketh, la Hoja Negra", sub="sombra de Márika, guardián de la Runa de la Muerte", cargos=(),
                    ya=0, sello=None, titulo="La fiscalía contra la Hoja Negra"),
       ("Y la fiscalía trae cinco", -.2), ("trae cinco pruebas|fin", 1.4), [], "expediente apertura", y=.42),

    # ================================================================ 5 · GUARDIAS HECHOS DE CAMPEONES MUERTOS
    puesto("Número cinco", "Prueba número 5", "Guardias de muertos", dur=3.4),
    expe(0, "Guardias hechos de campeones muertos", dur=1.2),
    grande(("Antes de conocer a Gurranq", .3), "gurranq", "Gurranq, el clérigo bestia", lado="der", dur=3.4, tam=520, y=.46,
           marco="museo"),
    mapa("mundo", [pto(M_MONTEDRAGO, "Montedrago", _P("caelid_wiki"), "inicio"), M_PUENTE_N,
                   pto(M_SANT, "Santuario de la bestia", _G("clerigo"), "poder")],
         ("tienes que cruzar Montedrago", -.3), ("Y en la puerta te espera", -.2),
         [("tienes que cruzar Montedrago", 0), ("Su refugio es el Santuario", 0)], titulo="Montedrago",
         sub="Al norte de Caelid", entrada="desenrolla", traza=2.4),
    ban_p(("Y en la puerta te espera", -.1), ("El juego la llama el Fiel", -.2), "En la puerta te espera",
          "Una gárgola negra, con alas de piedra", "gargola"),
    puesto(("El juego la llama el Fiel", 0), "Jefe", "Fiel de la Hoja Negra", dur=3.2),
    ban_p(("Casi todo el mundo la mata", -.1), ("El arma se llama Hoja", -.2), "Casi todo el mundo", "La mata y sigue",
          "la mata"),
    puesto(("El arma se llama Hoja", 0), "Su arma", "Hoja negra de gárgola", dur=3.6),
    ficha(("Espadón de bronce que portaban", 0), "Hoja negra de gárgola", "Espadón de bronce que portaban las gárgolas "
          "denodadas, *arreglada con adipocira ennegrecida*. […] *Esa es la marca de quienes sirven a Maliketh, la Hoja "
          "Negra.*", tipo="Arma", a=("de quienes sirven a Maliketh, la Hoja Negra|fin", .6)),
    cam(("Esa es la marca de quienes", 0), "maliketh_cara", "A quienes sirven", dur=3.6, x=.17, y=.44, foco=(.5, .5, 1.1)),
    puesto(("Y adipocira es una palabra", 0), "Adipocira", "¿Qué es?", dur=3.4),
    mg(E.domino(["Grasa de cadáver", "Bajo tierra", "Se vuelve cera", "Cera de muerto"], titulo="Adipocira, en la vida real",
                w=1600),
       ("En la vida real es la", -.2), ("Cera de muerto|fin", 1.0),
       [("En la vida real es la", 0), ("que se convierte en cera", 0), ("en cera bajo tierra", .2), ("Cera de muerto", 0)],
       "adipocira"),
    ban_p(("Y el propio juego te dice", -.1), ("En otra arma de gárgola", -.2), "El propio juego", "Te dice de dónde sale",
          "de donde"),
    ficha(("En otra arma de gárgola", 0), "Espadón de gárgola", "Tal y como le pasaba a su portador, las piezas que faltan "
          "fueron arregladas con adipocira, *el retal de los campeones*.", tipo="Arma",
          a=("con adipocira, el retal de los campeones|fin", .6)),
    cam(("el Espadón de gárgola, se", 0), "maliketh_cara", "Gárgolas de Maliketh", dur=4.0, x=.17, y=.44,
        foco=(.5, .5, 1.1)),

    # ---- 5b · el retal, el casco y la otra gárgola
    mg(E.retal(remate="A los campeones de otros"), ("retal de los campeones#2", -.2), ("a los campeones de otros|fin", .9),
       [("retal de los campeones#2", 0), ("y se remiendan con lo que", 0), ("la llevan ennegrecida", 0),
        ("a los campeones de otros", 0)], "retal"),
    rel(("Y el casco de Maliketh tiene", 0), "casco_maliketh", "Casco de Maliketh", dur=12.4),
    ficha(("Los campeones sabían lo que", -.3), "Casco de Maliketh", "[…] *Los campeones sabían lo que estaba en juego y, por "
          "eso mismo, eran campeones.*", tipo="Yelmo", icono="casco_maliketh", a=("por eso mismo, eran campeones|fin", .6)),
    mg(E.balanza("Dice", "No dice",
                 [("d", "De quién era cada pedazo"), ("i", "La cera, en sus guardias"), ("i", "El miedo, en su casco")],
                 remate="Unirlas es cosa nuestra", titulo="Ojo: lo que dice el juego"),
       ("Ojo: unir esas dos frases", -.2), ("los campeones en su casco|fin", 1.2),
       [("El juego no dice de quién", 0), ("Solo pone la cera de", 0), ("y el miedo de los campeones", 0),
        ("los campeones en su casco|fin", .1)], "ojo"),
    ban_p(("Y no es la única", -.1), ("y la misma cera de muerto|fin", .4), "No es la única · Tierras prohibidas",
          "Otra gárgola con su marca", "tierras prohibidas"),
    peg(("el camino que sube a las", 0), "maliketh_cara", "La misma marca negra", dur=4.0, x=.20, y=.42, tam=360,
        marco="museo"),
    peg(("Así que el perro fiel", 0), "clerigo", "El perro fiel de Márika", dur=4.2, x=.22, y=.46, tam=440),
    ban_p(("tenía la puerta vigilada por", -.1), ("Y eso es lo más suave", -.2), "La puerta vigilada",
          "Estatuas remendadas con muertos", "puerta"),
    ban_p(("Y eso es lo más suave", -.1), ("lo más suave de la lista|fin", .6), "Y eso", "Es lo más suave de la lista",
          "suave"),

    # ================================================================ 4 · EL CAZADOR QUE TRABAJABA PARA ÉL
    puesto("Número cuatro", "Prueba número 4", "El cazador a sueldo", dur=3.2),
    expe(1, "El cazador que trabajaba para él", dur=1.4),
    peg(("Si has pasado por el santuario", .7), "clerigo", "El santuario", dur=3.2, x=.20, y=.46, tam=400),
    rel(("raíces mortuorias. Tú se", -.3), "raiz_muerte", "Raíz mortuoria", dur=3.0, x=.80, y=.44, tam=420),
    mg(E.recibo("Raíces mortuorias", "Gurranq", "Tú", "Encantamientos de bestia", sello=None, titulo="El trato del santuario",
                etiquetas=("Las llevas", "Se las come", "Qué", "Te paga con")),
       ("Tú se las llevas", -.2), ("y a cambio te paga|fin", .05),
       [("Tú se las llevas", 0), ("él se las come", 0), ("él se las come", .6), ("y a cambio te paga", -.4)], "trato"),
    ban_p(("En el video de tus atrocidades", -.1), ("Hoy va el porqué", -.2), "Ya lo contamos",
          "En tus atrocidades", "tus atrocidades"),
    puesto(("Hoy va el porqué", 0), "Hoy", "Va el porqué", dur=2.4),
    rel(("Qué es una raíz mortuoria", 0), "raiz_muerte", "Raíz mortuoria", dur=8.6),
    ficha(("Su descripción empieza así", 0), "Raíz mortuoria", "*Una fuente que despierta a quienes viven en la muerte.* […]",
          tipo="Objeto clave", icono="raiz_muerte", a=("a quienes viven en la muerte|fin", 1.0)),
    grande(("Los muertos que caminan", 0), "ave_muerte_cerca", "Quienes viven en la muerte", lado="izq", dur=3.0, tam=560, y=.46),
    ban_p(("Los esqueletos que se levantan", -.1), ("una y otra vez|fin", .6), "Los muertos que caminan",
          "Se levantan una y otra vez", "esqueletos"),
    ficha(("Y termina con esto", 0), "Raíz mortuoria", "[…] *En la noche del complot, la Runa de la Muerte robada permitió la "
          "primera muerte de un semidiós.* Posteriormente, la Runa de la Muerte se extendió por las Tierras Intermedias a "
          "través de las raíces subterráneas del gran árbol, *emergiendo en forma de raíz mortuoria*.", tipo="Objeto clave",
          icono="raiz_muerte", a=("emergiendo en forma de raíz mortuoria|fin", .6)),
    peg(("permitió la primera muerte de", 0), "godwyn", "La primera muerte de un semidiós", dur=5.0, x=.22, y=.50, tam=440),
    rel(("se extendió por las Tierras", 0), "raiz_muerte", "Por las raíces del gran árbol", dur=8.0, x=.22, y=.46),
    ban_p(("Léelo despacio", -.1), ("se coló por las raíces", -.3), "Léelo despacio", "Le robaron la Muerte", "despacio"),
    cam(("La muerte que le robaron", 0), "maliketh_cara", "Su guardián", dur=3.4, x=.17, y=.44, foco=(.5, .5, 1.1)),
    mapa("mundo", [pto(M_ARBOL, "Árbol Áureo", None, "inicio"), pto(M_SANT, "Santuario de la bestia", _G("clerigo"), "meta")],
         ("se coló por las raíces", -.3), ("Y su forma de arreglarlo", -.2),
         [("se coló por las raíces", 0), ("Y por donde salía", .4)], titulo="Por las raíces",
         sub=None, ventana=True, x=.66, y=.40, margen=.21, entrada="pliegue", traza=99),
    peg(("los muertos dejaban de estar", 0), "pajaro_muerte", "Muertos que no se quedan muertos", dur=4.0, x=.20, y=.50,
        tam=420),
    ban_p(("Cada esqueleto que se te", -.1), ("es el fallo de un solo", -.2), "Cada esqueleto", "Cada tumba que se abre",
          "cada esqueleto"),
    ban_p(("es el fallo de un solo", -.1), ("Y su forma de arreglarlo", -.2), "El fallo", "De un solo guardián", "fallo"),
    grande(("Y su forma de arreglarlo", 0), "clerigo", "Su arreglo: comérselo", lado="der", dur=3.6, tam=560, y=.46),

    # ---- 4b · D, el encargo y el recambio
    ban_p(("Pero no lo arreglaba él", -.1), ("me conocen como D", -.2), "No lo arreglaba él solo",
          "Necrolimbo: un caballero dorado", "el solo"),
    leg("d_cazador", "D", ["Cazador de los muertos", "Armadura dorada", "Arranca raíces"],
        ("En Necrolimbo te cruzas", -.1), ("te pasa el encargo|fin", .4),
        [("un caballero de armadura dorada", .3), ("un caballero de armadura dorada", 1.0), ("y arranco sus raíces", 0)],
        y=.42),
    ban_p(("me conocen como D", -.1), ("y arranco sus raíces|fin", .6), "D · en inglés",
          "Caza a los que viven en la muerte", "d caza"),
    ban_p(("Y cuando le hablas de", -.1), ("Te dice que la propia", -.3), "D", "Te pasa el encargo", "encargo"),
    mg(E.recambio(iconos=(_G("gurranq"), _G("d_cazador"), None)), ("Te dice que la propia", -.2),
       ("El recambio eras tú|fin", 1.2),
       [("Te dice que la propia", 0), ("D trabajaba para él", 0), ("El recambio eras tú", 0)], "recambio"),
    rel(("Con la cuarta raíz nota", 0), "raiz_muerte", "La cuarta raíz", dur=4.0),
    top(("Dice que hay algo más", -.1), ("Y aun así, la muerte le", -.2), "Gurranq · en inglés",
        "Qué raro… hay algo más, mezclado", "mezclado"),
    top(("Y aun así, la muerte le", -.1), ("El juego nunca explica qué", -.2), "Gurranq · en inglés",
        "Aun así, la Muerte le calma el hambre", "hambre"),
    peg(("Y aun así, la muerte le", 0), "gurranq", "Gurranq", dur=3.4, x=.20, y=.50, tam=380),
    ban_p(("El juego nunca explica qué", -.1), ("Y tú se la diste igual", -.2), "El juego nunca explica",
          "Qué llevaba esa raíz", "nunca explica"),
    ban_p(("Y tú se la diste igual", -.1), ("Y tú se la diste igual|fin", .7), "Y tú", "Se la diste igual", "diste igual"),
    peg(("Y Gurranq sabía lo que", 0), "gurranq", "Sabía lo que comía", dur=3.0, x=.80, y=.42, tam=360),
    top(("Con la quinta raíz dice", -.1), ("Pero la tocaba la tuya", -.2), "Gurranq, quinta raíz · en inglés",
        "La Muerte es mi pecado: no la toque el hombre", "pecado"),
    rel(("Con la quinta raíz dice", 0), "raiz_muerte", "La quinta raíz", dur=4.2),
    ban_p(("Pero la tocaba la tuya", -.1), ("Él mismo te la pedía|fin", .6), "Pero la tocaba", "La tuya", "la tuya"),
    rel(("Su Ojo de bestia, el", 0), "ojo_bestia", "Ojo de bestia", dur=12.4),
    ficha(("Su Ojo de bestia, el", .4), "Ojo de bestia", "Se dice que tiembla cuando se encuentra cerca de la raíz mortuoria. "
          "[…] *\"No estoy saciado... Aliméntame... con más Muerte...\"*", tipo="Objeto clave", icono="ojo_bestia",
          a=("Con más Muerte|fin", .9)),

    # ---- 4c · Dark Shooter, Jonatan y el suscriptor nuevo
    puesto(("Y aquí va una respuesta", 0), "Una respuesta", "Con corrección incluida", dur=2.4),
    com(("Dark Shooter nos corrigió lo", 0), C_DARK, dur=8.6),
    ban_p(("Tienes razón, Dark", -.1), ("te pide que guardes el", -.2), "Tienes razón", "Dark", "razon"),
    peg(("Después de lanzarse contra ti", 0), "gurranq", "Gurranq", dur=4.0, x=.20, y=.46, tam=380),
    top(("te pide que guardes el", -.1), ("Ese basta era para tu", -.2), "Gurranq · en inglés",
        "Guarda el arma… no lo olvidaré… basta", "basta"),
    ban_p(("Ese basta era para tu", -.1), ("no para las raíces|fin", .5), "Ese «basta»", "Era para tu espada", "espada"),
    puesto(("Anotado", 0), "Anotado", "La quinta raíz, igual", dur=4.4),
    puesto(("Y dos comentarios más", 0), "Dos comentarios más", "Y valen oro", dur=2.2),
    com(("Jonatan escribe que estos", 0), C_JONATAN, dur=10.4),
    ban_p(("Jonatan, la rueda no te", -.1), ("el que te juzga es Rykard", -.1), "Jonatan", "La rueda no te juzga", "rueda"),
    peg(("el que te juzga es Rykard", 0), "rykard", "El que te juzga", dur=3.0, x=.80, y=.42, tam=380),
    com(("Y un suscriptor nuevo nos", 0), C_NOVIA, dur=6.4),
    ban_p(("Saludos a ella", -.1), ("de los que lo juegan|fin", .6), "Saludos a ella", "Ya sabe más que la mitad",
          "saludos"),

    # ================================================================ 3 · EL NOMBRE QUE ASUSTABA A LOS DIOSES
    puesto("Número tres", "Prueba número 3", "Un nombre que asusta", dur=3.2),
    expe(2, "El nombre que asustaba a los dioses", dur=2.2),
    grande(("Gurranq no siempre fue un", 1.4), "gurranq", "Gurranq", lado="izq", dur=3.0, tam=520, y=.46),
    ban_p(("Y su nombre no siempre", -.1), ("Debajo de su santuario hay", -.2), "Su nombre", "No siempre fue solo un nombre",
          "solo un nombre"),
    ban_p(("Debajo de su santuario hay", -.1), ("Su descripción dice que se", -.2), "Bajo su santuario",
          "Una daga: la Cinquedea", "cinquedea"),
    pant("farum_wiki", ("Su descripción dice que se", -.3), ("Una ciudad de bestias con", -.3), zoom=(1.0, 1.10)),
    ficha(("Su descripción dice que se", 0), "Cinquedea", "Espada corta cedida a los *clérigos de alta jerarquía de Farum "
          "Azula*. […] El diseño rinde homenaje a los cinco dedos de una bestia, *símbolo de la inteligencia que se otorgó "
          "antaño a los suyos*.", tipo="Daga", a=("se otorgó antaño a los suyos|fin", .6)),
    mapa("mundo", [pto(M_FARUM, "Farum Azula", _P("farum_wiki"), "poder")], ("Una ciudad de bestias con", -.3),
         ("Cuando le llevas la sexta", -.2), [("Una ciudad de bestias con", 0)], titulo="Farum Azula",
         sub="Una ciudad de bestias", ventana=True, x=.66, y=.42, entrada="mesa"),
    cam(("una que no rezaba precisamente", 0), "maliketh_cara", "No rezaba", dur=2.8, x=.17, y=.44, foco=(.5, .5, 1.1)),
    ban_p(("Cuando le llevas la sexta", -.1), ("la Piedra de Gurranq. Y", -.1), "La sexta raíz", "Te regala un milagro",
          "sexta"),
    rel(("la Piedra de Gurranq. Y", 0), "piedra_gurranq", "Piedra de Gurranq", dur=12.6),
    ficha(("Y su descripción dice: antaño", 0), "Piedra de Gurranq", "[…] *Antaño, Gurranq era una bestia tan "
          "terroríficamente feroz que su nombre significaba \"Muerte de los Semidioses\".*", tipo="Encantamiento",
          icono="piedra_gurranq", a=("significaba Muerte de los Semidioses|fin", .6)),
    mg(E.nombre_bestia(remate="Mucho antes de la Devastación"), ("Muerte de los Semidioses. Ese era", -.3),
       ("que se llamaba así|fin", 1.0),
       [("Muerte de los Semidioses. Ese era", -.2), ("Ese era su nombre", 0), ("antes de la Devastación", 0),
        ("ya había una bestia que", 0)], "nombre bestia"),
    rel(("Y su casco lo confirma", 0), "casco_maliketh", "Casco de Maliketh", dur=12.6),
    ficha(("Y su casco lo confirma", .3), "Casco de Maliketh", "*Maliketh, fiel hermanastro de la Reina Márika*, empuñaba un "
          "filo bañado en Muerte Escrita. *No había ni un solo semidiós que no lo temiese.* […]", tipo="Yelmo",
          icono="casco_maliketh", a=("que no lo temiese|fin", .7)),
    aba([("godrick", "Godrick"), ("rykard", "Rykard"), ("radahn", "Radahn"), ("morgott", "Morgott"), ("malenia", "Malenia"),
         ("mohg_cara", "Mohg")],
        ("Ni uno. Todos los", -.1), ("al mismo perro|fin", .7),
        [("Ni uno. Todos los", 0), ("Todos los semidioses que han", .3), ("que han pasado por este", 0),
         ("que han pasado por este", .4), ("por este canal le tenían", 0), ("le tenían miedo al mismo", 0)],
        "semidioses", y=.54, tam=240),
    rel(("La Garra de la bestia Gurranq", 0), "garra_gurranq", "Garra de la bestia Gurranq", dur=8.4),
    top(("habla de su furia, una", -.1), ("Un clérigo que, cuando se", -.3), "Garra de la bestia Gurranq",
        "Su furia de bestia… y su desasosiego", "furia"),
    ban_p(("Y los milagros que te", -.1), ("La Garra de la bestia Gurranq", -.2), "Sus milagros",
          "Lo dejan ver bajo el disfraz", "disfraz"),
    pant("gurranq_arrodillado_farum", ("Un clérigo que, cuando se", -.2), ("vuelve a ser lo que era", -.15),
         zoom=(1.0, 1.06)),
    pant("maliketh_revelado_cuerpo", ("vuelve a ser lo que era", -.2), ("vuelve a ser lo que era|fin", 1.6),
         zoom=(1.0, 1.08)),

    # ---- 3b · la jaula de la Orden Dorada
    puesto(("Y ahora la parte que", 0), "La parte que", "Casi nadie conecta", dur=3.0),
    rel(("La Muerte Escrita, la que", 0), "espada_maliketh", "Muerte Escrita", "en su espada", dur=3.6),
    mg(E.muerte_suelta(("Su sombra: Maliketh",), titulo="La Runa de la Muerte", remate="",
                   origen=("sacada del", "Círculo de Elden")),
       ("es la propia Runa de la", -.2), ("a guardar a su sombra|fin", .8), [("Márika la sacó del Círculo", 0)],
       "runa sacada"),
    rel(("Y la Runa reparadora del", 0), "runa_muerte", "Runa reparadora del Príncipe de la Muerte", dur=8.6),
    ficha(("Y la Runa reparadora del", .3), "Runa reparadora del Príncipe de la Muerte", "*La Orden Dorada se creó tras "
          "confinar a la Muerte Escrita*, por lo que esta nueva Orden equivaldrá a la restauración de la Muerte.",
          tipo="Objeto clave", a=("tras confinar a la Muerte Escrita|fin", 1.0)),
    mg(E.jaula_orden(), ("La Orden Dorada. La edad", -.2), ("Y el carcelero era él|fin", 1.2),
       [("La Orden Dorada. La edad", 0), ("el Árbol Áureo brillando", 0), ("Y el carcelero era él", 0)], "jaula"),
    rel(("Para que nadie pudiera volver", 0), "espada_maliketh", "Hoja negra de Maliketh", dur=6.0),
    ficha(("Para que nadie pudiera volver", .3), "Hoja negra de Maliketh", "[…] *Maliketh vinculó la espada a su propia "
          "carne* para que nadie pudiese volver a hurtar a la muerte.", tipo="Arma", icono="espada_maliketh",
          a=("Y en la cinemática de", -.1)),
    pant("hoja_negra_sale_del_cuerpo", ("Y en la cinemática de", -.3), ("la hoja le sale del cuerpo|fin", 1.0),
         zoom=(1.0, 1.10)),
    ban_p(("Y en la cinemática de", -.1), ("la hoja le sale del cuerpo|fin", .8), "En la cinemática de Farum Azula",
          "La hoja le sale del cuerpo", "cinematica"),
    ban_p(("Mientras él guardó esa jaula", -.1), ("Lo decidió Márika", -.2), "Mientras guardó la jaula",
          "La muerte de verdad no existió", "no existio"),
    peg(("Lo decidió Márika", 0), "marika", "Lo decidió Márika", dur=3.0, x=.20, y=.44, tam=380),
    peg(("Y lo hizo cumplir la", 0), "maliketh_cara", "La bestia que daba miedo", dur=4.0, x=.80, y=.42, tam=400),

    # ---- 3c · Edgar
    puesto(("Y antes del número dos", 0), "Antes del número dos", "Un comentario", dur=2.4),
    com(("Edgar nos pidió que habláramos", 0), C_EDGAR, dur=8.4),
    puesto(("Hola, Edgar", 0), "Hola, Edgar", "Saludo entregado", dur=2.4),
    ban_p(("en Latinoamérica, a este semidiós", -.1), ("Aquí le decimos la Hoja", -.2), "En Latinoamérica",
          "La Espada Negra", "latam"),
    ban_p(("Aquí le decimos la Hoja", -.1), ("Mismo perro, distinta correa", -.2), "Aquí", "La Hoja Negra", "aqui"),
    peg(("Aquí le decimos la Hoja", 0), "maliketh_cara", "Mismo perro", dur=4.6, x=.20, y=.44, tam=380),
    puesto(("Mismo perro, distinta correa", 0), "Mismo perro", "Distinta correa", dur=2.6),
    ban_p(("Lo de hablar latino lo", -.1), ("El Profeta solo tiene un", -.2), "Hablar latino", "Otro día", "otro dia"),
    puesto(("El Profeta solo tiene un", 0), "El Profeta", "Acento de profecía", dur=3.4),

    # ================================================================ 2 · LA REINA QUE ACUNABA A LOS RECIÉN NACIDOS
    puesto("Número dos#2", "Prueba número 2", "La reina de las cunas", dur=3.0),
    expe(3, "La reina que acunaba a los recién nacidos", dur=1.2),
    ban_p(("Antes de ser carcelero, Maliketh", .5), ("En Montedrago, cerca del", -.3), "Antes de ser carcelero",
          "El arma de Márika", "arma marika"),
    cam(("el arma de Márika contra", 0), "marika", "Márika", dur=2.6, x=.17, y=.44, foco=(.5, .35, 1.3)),
    mapa("mundo", [pto(M_SANT, "Santuario de la bestia", _G("clerigo"), "inicio"),
                   pto(M_TORRE, "Torre Sagrada de Caelid", _G("pielesdivinas"), "meta")],
         ("En Montedrago, cerca del", -.3), ("Arriba, después de pelear", -.2),
         [("En Montedrago, cerca del", 0), ("la Torre Sagrada de Caelid", 0)], titulo="Torre Sagrada de Caelid",
         sub="En un islote de Montedrago", entrada="pliegue", traza=2.0, margen=.26),
    grande(("contra un apóstol sacrodermo", 0), "pielesdivinas", "Apóstol sacrodermo", lado="izq", dur=2.6, tam=520, y=.46),
    rel(("el Espadón del exterminador de", 0), "mano_cuchilla", "Espadón del exterminador de dioses", dur=13.6),
    ficha(("Su descripción: espada sagrada", 0), "Espadón del exterminador de dioses", "Espada sagrada de la *Reina del Ojo "
          "Velado*, que controlaba a los apóstoles sacrodermos *antes de sucumbir ante Maliketh*.", tipo="Arma",
          icono="mano_cuchilla", a=("sucumbir ante Maliketh, la Hoja Negra|fin", .6)),
    cam(("En el video de Melina la", 0), "melina", "En el video de Melina", dur=3.0, x=.17, y=.44, foco=(.5, .3, 1.4)),
    ban_p(("Hoy toca contarla desde el", -.1), ("El Ritual de la llama", -.2), "Hoy", "Desde el otro lado", "otro lado"),
    ficha(("El Ritual de la llama", 0), "Ritual de la llama negra", "*La Reina del Ojo Velado dirigió a los apóstoles.* Se dice "
          "que era *una empírea elegida por los Dedos*.", tipo="Encantamiento", a=("una empírea elegida por los Dedos|fin", .7)),
    peg(("dirigió a los apóstoles", 0), "pielesdivinas", "Sus apóstoles", dur=4.0, x=.20, y=.48, tam=400),
    mg(E.estandartes(["La Reina del Ojo Velado"], remate="Quitada de en medio", titulo="La otra empírea", w=900),
       ("Una empírea. Lo mismo que", -.2), ("la quitó de en medio|fin", 1.0),
       [("la quitó de en medio", 0), ("la quitó de en medio|fin", .2)], "otra empirea", y=.46),
    cam(("Lo mismo que Márika: el", 0), "marika", "Márika, empírea", dur=4.4, x=.14, y=.40, foco=(.5, .35, 1.3)),
    peg(("el propio Recuerdo de esta", 0), "recuerdo_espada_negra", "Recuerdo de la Hoja Negra", dur=4.6, x=.86, y=.42,
        tam=320),
    cam(("Y la sombra de Márika la", 0), "maliketh_cara", "La sombra de Márika", dur=3.2, x=.86, y=.42, foco=(.5, .5, 1.1)),

    # ---- 2b · los apóstoles, la llama negra y el paño
    grande(("Y quiénes eran sus apóstoles", 0), "pielesdivinas", "Los apóstoles sacrodermos", lado="izq", dur=5.2, tam=520,
           y=.46),
    ban_p(("Gente que empuñaba la llama", -.1), ("La Llama negra rastreadora lo", -.2), "La llama negra",
          "La que mataba dioses", "llama negra"),
    ficha(("La Llama negra rastreadora lo", 0), "Llama negra rastreadora", "*Hace un tiempo la llama negra era capaz de matar "
          "dioses.* Sin embargo, *cuando Maliketh selló la Muerte Escrita, el verdadero poder de la llama negra se perdió*.",
          tipo="Encantamiento", a=("de la llama negra se perdió|fin", .7)),
    cam(("cuando Maliketh selló la Muerte", 0), "maliketh_cara", "La selló Maliketh", dur=4.0, x=.17, y=.44,
        foco=(.5, .5, 1.1)),
    ficha(("Y la túnica de los apóstoles", 0), "Túnica de apóstol sacrodermo", "Los apóstoles, que se dice que sirvieron a la "
          "Muerte Escrita, empuñan la llama negra exterminadora de dioses. Pero, *tras su derrota ante Maliketh, la Hoja "
          "Negra, la fuente de su poder fue sellada*.", tipo="Armadura", a=("la fuente de su poder fue sellada|fin", .7)),
    peg(("Y la túnica de los apóstoles", .2), "pielesdivinas", "Su túnica", dur=8.0, x=.20, y=.50, tam=400),
    puesto(("Pero el objeto que casi", 0), "Lo que casi nadie lee", "Empañadura sacroderma", dur=4.4),
    ficha(("La Reina del Ojo Velado acuna", 0), "Empañadura sacroderma", "*La Reina del Ojo Velado acuna a los apóstoles "
          "recién nacidos envueltos en este paño.* Pronto crecerán y se convertirán en la fatalidad de los dioses.",
          tipo="Talismán", a=("en la fatalidad de los dioses|fin", .7)),
    peg(("a los apóstoles recién nacidos", 0), "pielesdivinas", "Pronto crecerán", dur=6.0, x=.20, y=.50, tam=380),
    mg(E.estandarte_caido(emblema="Llama negra", quien="el poder con el que nacían", remate="Crecieron sin él",
                          titulo="Recién nacidos"),
       ("Una reina acunando recién nacidos", -.2), ("los hacía peligrosos|fin", .9),
       [("Una reina acunando recién nacidos", .3), ("que llega y sella el", 0), ("Esos niños crecieron sin", 0)],
       "recien nacidos"),
    ban_p(("Ojo, que aquí tampoco hay", -.1), ("Sacrodermo quiere decir piel", -.2), "Ojo", "Aquí tampoco hay santos",
          "santos"),
    ban_p(("Sacrodermo quiere decir piel", -.1), ("Y el juego dice que la", -.3), "Sacrodermo", "Piel de dios",
          "piel de dios"),
    peg(("Los apóstoles desollaban dioses", 0), "pielesdivinas", "Llevan la piel encima", dur=3.8, x=.20, y=.46, tam=400),
    mg(E.balanza("Dice", "No dice", [("i", "Sucumbió"), ("i", "Fue derrotada"), ("d", "Que la matara")],
                 remate="Derrotada sí; muerta, no", titulo="La Reina del Ojo Velado, según el juego"),
       ("Y el juego dice que la", -.2), ("No dice que la matara|fin", 1.2),
       [("la reina sucumbió y fue", 0), ("y fue derrotada", 0), ("No dice que la matara", 0),
        ("No dice que la matara|fin", .2)], "derrota"),
    ban_p(("Pero sí deja claro quién", -.1), ("Y en tu inventario se", -.2), "Pero sí deja claro", "Quién ganó", "gano"),
    rel(("En la torre queda su", 0), "mano_cuchilla", "Su espada, en la torre", dur=3.4),
    ban_p(("Y en tu inventario se", -.1), ("el paño de los recién nacidos|fin", .7), "En tu inventario",
          "El paño de los recién nacidos", "inventario"),

    # ================================================================ COMENTARIOS Y CAMPAÑA
    puesto(("Antes del número uno, varios", 0), "Antes del número uno", "Comentarios que se lo ganaron", dur=2.8),
    com(("Bryan dice que ha visto", 0), C_BRYAN, dur=8.6),
    com(("Y Alberto, que son de", 0), C_ALBERTO, dur=4.4, x=.72, y=.36),
    com(("Astora lo resume mejor que", 0), C_ASTORA, dur=7.4),
    peg(("atrocidades de estos enfermos", 0), "maliketh_cara", "Uno de los enfermos", dur=3.2, x=.80, y=.42, tam=360),
    com(("Y Lissom escribió: toca pasarse", 0), C_LISSOM, dur=5.6),
    puesto(("Gracias, Lissom", 0), "Gracias, Lissom", "Justo lo que pedimos", dur=3.6),
    ban_p(("A día de hoy somos", -.1), ("Aun así, de cada cien", -.25), "Runa Caída", "1 380 suscriptores", "mil trescientos"),
    mg(E.cien("De cada 100 vistas, las de suscriptores", 8, remate=("Siguiente objetivo: 2 000", 2)),
       ("Aun así, de cada cien", -.2), ("El siguiente objetivo son dos mil|fin", .8),
       ["Aun así, de cada cien", "menos de nueve son de", "El siguiente objetivo son"], "cien", y=.46),
    mg(E.acuerdo(["Coserse la Muerte a la carne"], "Que nadie se la lleve", letra="Aquí basta con un botón",
                 titulo="Guardar lo tuyo", remate="Suscríbete", cab=("A Maliketh le costó", "Para")),
       ("A Maliketh le hizo falta", -.2), ("basta con apretar un botón|fin", 1.0),
       [("A Maliketh le hizo falta", 0), ("para que nadie se la", 0), ("Aquí, en cambio, basta con", 0),
        ("basta con apretar un botón|fin", .1)], "boton"),
    puesto(("Y todos los comentarios se", 0), "Todos los comentarios", "Se leen, uno por uno", dur=3.6),

    # ================================================================ 1 · LA NOCHE QUE DEJÓ ROBAR LA MUERTE
    puesto("Número uno#3", "Prueba número 1", "La noche del robo", dur=3.0),
    expe(4, "La noche que dejó robar la Muerte", dur=1.0),
    ban_p(("Esta es la parte que todo", .25), ("Rogier te la cuenta en", -.2), "La parte que todo el mundo",
          "Cree conocer", "cree conocer"),
    pant("mesa_redonda", ("Rogier te la cuenta en", -.3), ("y Ranni la narra en", -.1)),
    ban_p(("Rogier te la cuenta en", -.1), ("y Ranni la narra en", -.2), "Rogier", "En la Mesa Redonda", "rogier"),
    peg(("y Ranni la narra en", 0), "ranni", "Ranni, en el tráiler", dur=3.0, x=.78, y=.42, tam=380),
    pant("trailer_noche_niebla", ("en una noche de niebla", -.3), ("El primero, Godwyn, el Dorado", -.2), zoom=(1.36, 1.42)),
    top(("en una noche de niebla", -.1), ("Y los semidioses empezaron a", -.2), "Tráiler oficial · Ranni",
        "Una noche de niebla invernal", "niebla"),
    top(("Y los semidioses empezaron a", -.1), ("El primero, Godwyn, el Dorado", -.2), "Tráiler oficial · Ranni",
        "Los semidioses empezaron a caer", "caer"),
    pant("trailer_godwyn_cadaver", ("El primero, Godwyn, el Dorado", -.3), ("Esa noche tiene nombre oficial", -.2),
         zoom=(1.36, 1.42)),
    ban_p(("El primero, Godwyn, el Dorado", -.1), ("Esa noche tiene nombre oficial", -.3), "El primero",
          "Godwyn, el Dorado", "godwyn"),
    puesto(("Esa noche tiene nombre oficial", 0), "Nombre oficial", "Noche de los Puñales Negros", dur=4.2),
    mg(E.cadena(["Falló", "Se cosió la espada", "Se escondió"], preso="Maliketh", amo="La noche del robo",
                remate="Comiendo raíces", titulo="Por eso"),
       ("Y pasó porque el guardián", -.2), ("Por eso acabó escondido|fin", 2.0),
       [("Y pasó porque el guardián", 0), ("Por eso se cosió la", 0), ("Por eso acabó escondido", 0),
        ("Por eso acabó escondido|fin", .6)], "por eso"),
    grande(("Y la asesina que lo", 0), "asesina_cuchillo", "Asesina de los Cuchillos Negros", lado="izq", dur=3.0, tam=520,
           y=.46),
    rel(("Tiche, la Cuchillo Negro", 0), "tiche", "Tiche, la Cuchillo Negro", dur=12.4),
    ficha(("Su ceniza de espíritu dice", 0), "Tiche, la Cuchillo Negro", "[…] durante la noche del complot, *imbuyó su puñal "
          "negro en la Runa de la Muerte para dar muerte a Godwyn, el Dorado*. […]", tipo="Cenizas de espíritu",
          icono="tiche", a=("para dar muerte a Godwyn, el Dorado|fin", .6)),
    peg(("imbuyó su puñal negro en", 0), "cuchillo_negro", "Su puñal negro", dur=3.6, x=.80, y=.70, tam=300),
    ban_p(("Y esa ceniza la invocas", -.1), ("para que pelee a tu lado|fin", .6), "Y esa ceniza", "La invocas tú",
          "invocas"),
    ficha(("El Sello maldito de la", 0), "Sello maldito de la Muerte", "[…] *Dos semidioses murieron al mismo tiempo.* […] "
          "Ranni fue la primera semidiosa en ver cómo su carne moría, mientras que, en el caso del Príncipe de la Muerte, "
          "*tan solo su alma falleció*.", tipo="Objeto clave", a=("solo murió su alma|fin", .8)),
    peg(("dos semidioses murieron al mismo", 0), "godwyn", "Dos semidioses", dur=3.6, x=.20, y=.50, tam=400),
    peg(("Ranni fue la primera en", 0), "ranni", "Ranni: su carne", dur=4.0, x=.20, y=.46, tam=380),
    peg(("Y en el caso del Príncipe", 0), "godwyn", "Godwyn: solo su alma", dur=4.4, x=.20, y=.50, tam=400),
    ban_p(("Hasta aquí, la versión de", -.1), ("Ahora, lo que el juego", -.2), "Hasta aquí", "La versión de siempre",
          "version"),
    puesto(("Ahora, lo que el juego", 0), "Tres objetos", "En tres sitios distintos", dur=4.6),
    pant("catacumbas_cuchillo", ("en unas catacumbas de Liurnia", -.3), ("Durante la Noche de los Puñales", 1.2)),
    ban_p(("El primero es el Aojo", -.1), ("Durante la Noche de los Puñales", -.1), "En unas catacumbas de Liurnia",
          "Aojo de puñal negro", "aojo"),
    ficha(("Durante la Noche de los Puñales", 0), "Aojo de puñal negro", "Durante la Noche de los Puñales Negros, *alguien "
          "robó un fragmento de la Runa de la Muerte a Maliketh, la Hoja Negra*, e imbuyó las dagas de los asesinos con su "
          "poder. Esta marca es una prueba del ritual y *oculta la verdad de la conspiración*.", tipo="Objeto clave",
          a=("Oculta la verdad. El juego", -.1)),
    cam(("alguien robó un fragmento de", 0), "maliketh_cara", "Se lo robaron", dur=4.0, x=.17, y=.44, foco=(.5, .5, 1.1)),
    peg(("e imbuyó las dagas de", 0), "cuchillo_negro", "Las dagas de las asesinas", dur=4.4, x=.20, y=.50, tam=380),
    puesto(("Oculta la verdad. El juego", 0), "Oculta la verdad", "Con esas palabras", dur=3.6),
    ban_p(("que lo que te han contado", -.1), ("no es todo|fin", .6), "Lo que te han contado", "No es todo", "no es todo"),
    rel(("El segundo, la armadura de", 0), "armadura_cuchillo", "Armadura de Cuchillo Negro", dur=17.0),
    ficha(("Las asesinas que llevaron a", 0), "Armadura de Cuchillo Negro", "*Las asesinas que llevaron a cabo las hazañas de "
          "la Noche de los Puñales Negros eran todas mujeres* y, según los rumores, *eran númenes estrechamente vinculadas a "
          "la propia Márika*.", tipo="Armadura", icono="armadura_cuchillo", a=("vinculadas a la propia Márika|fin", .7)),
    peg(("Las asesinas eran de la", 0), "asesina_cuchillo", "Las asesinas", dur=3.2, x=.20, y=.46, tam=380),
    peg(("de la gente de Márika", 0), "marika", "La gente de Márika", dur=3.0, x=.80, y=.44, tam=360),
    ban_p(("Y el tercer objeto es", -.1), ("es el que lo une todo|fin", .5), "El tercer objeto", "Lo une todo", "tercer"),

    # ---- 1b · el Recuerdo, la pregunta y Gurranq al morir
    rel(("Es el Recuerdo de la", 0), "recuerdo_espada_negra", "Recuerdo de la Hoja Negra", dur=19.0),
    ficha(("Maliketh era una bestia ligada", 0), "Recuerdo de la Hoja Negra", "Maliketh era una bestia ligada a la sombra de "
          "su empírea. El ansia de Márika por disponer de su sombra actuaba como un baluarte contra la Muerte Escrita. *Aun "
          "así, ella lo traicionó.*", tipo="Recuerdo", icono="recuerdo_espada_negra",
          a=("Aun así, ella lo traicionó|fin", 1.0)),
    mg(E.sombra(ama="Márika", sombra_="Maliketh", amos="Los Dos Dedos", titulo="Solo un recipiente"),
       ("En inglés y en japonés es", -.2), ("Y aun así, lo traicionó|fin", 1.0),
       [("En inglés y en japonés es", 0), ("Márika solo lo quería como", 0), ("Y aun así, lo traicionó", 0)],
       "recipiente", y=.56),
    top(("Márika solo lo quería como", -.1), ("Y aun así, lo traicionó|fin", .9), "En inglés y en japonés",
        "Solo lo quería como recipiente", "recipiente"),
    mg(E.pruebas(objetos=(("Aojo de puñal negro", "oculta la verdad de la conspiración", None),
                          ("Armadura de Cuchillo Negro", "númenes vinculadas a la propia Márika", _G("armadura_cuchillo")),
                          ("Recuerdo de la Hoja Negra", "Aun así, ella lo traicionó", _G("recuerdo_espada_negra")))),
       ("Así que la pregunta es", -.2), ("se la hizo robar su propia reina|fin", .5),
       [("Así que la pregunta es", 0), ("Así que la pregunta es", .6), ("y ojo, que el juego", 0),
        ("le robaron la Muerte a Maliketh", 0), ("o se la hizo robar", 0)], "pruebas"),
    ban_p(("Hay alguien que parece tener", .15), ("El propio Maliketh. Pero", -.1), "Alguien parece",
          "Tener la respuesta", "respuesta"),
    peg(("El propio Maliketh. Pero", 0), "maliketh_cara", "El propio Maliketh", dur=3.4, x=.20, y=.44, tam=400),
    mapa("mundo", [pto(M_SANT, "Su santuario", _G("gurranq"), "poder")], ("atacar a Gurranq en su", -.3),
         ("Sus últimas palabras son para", -.2), [("atacar a Gurranq en su", 0)], titulo="Santuario de la bestia",
         sub="Casi nadie lo ataca", ventana=True, x=.66, y=.42, entrada="foco"),
    peg(("Si lo matas, el clérigo", 0), "gurranq", "El clérigo bestia", dur=3.6, x=.20, y=.46, tam=380, marco="museo"),
    ban_p(("Sus últimas palabras son para", -.1), (P_ENGANASTE, -.05), "Sus últimas palabras", "Son para ella",
          "ultimas"),
    # ---- PISTA 2: s_enganaste (15,23 s) — Gurranq al morir (solo en inglés: traducción, no cita)
    ban_p((P_ENGANASTE, .1), (P_ENGANASTE, 7.6), "Gurranq, al morir · en inglés", "Márika… ¿por qué me engañaste?",
          "pista enganaste 1"),
    ban_p((P_ENGANASTE, 7.7), (P_ENGANASTE, 15.3), "Gurranq, al morir · en inglés", "¿Por qué… lo rompiste?",
          "pista enganaste 2"),

    # ---- 1c · romper; el diálogo recortado
    top(("Y lo que dice es esto: por", -.1), ("En japonés el verbo es", -.2), "Traducido del inglés",
        "¿Por qué me engañaste? ¿Por qué lo rompiste?", "engañaste"),
    peg(("me engañaste, Márika", 0), "marika", "Márika", dur=3.4, x=.80, y=.46, tam=360),
    ban_p(("En japonés el verbo es", -.1), ("El guardián de la muerte, muriendo", -.2), "En japonés",
          "El verbo es «romper»", "romper"),
    cam(("El guardián de la muerte, muriendo", 0), "gurranq", "El guardián, muriendo", dur=4.2, x=.17, y=.44,
        foco=(.5, .4, 1.2)),
    ban_p(("El Círculo de Elden se", -.1), ("Y el que lo pregunta", -.2), "El Círculo de Elden", "Se rompió", "circulo"),
    peg(("Y el que lo pregunta", 0), "maliketh_cara", "Su sombra", dur=3.0, x=.20, y=.44, tam=380),
    puesto(("Y todavía hay más. FromSoftware", 0), "Y todavía hay más", "Un diálogo recortado", dur=3.4),
    pant("maliketh_revelado_hoja", ("el final del combate contra", -.3), ("Lo quitó del juego", -.1), zoom=(1.06, 1.12)),
    ban_p(("Lo quitó del juego, pero", -.1), ("Y es la confesión que", -.2), "Lo quitó del juego",
          "Sigue en los archivos", "archivos"),
    ban_p(("Y es la confesión que", -.1), (P_RECORTADO, -.05), "La confesión", "Que le faltaba a esta historia",
          "confesion"),
    # ---- PISTA 3: s_recortado (13,84 s) — DIÁLOGO RECORTADO (en los archivos, no en el juego)
    ban_p((P_RECORTADO, .1), (P_RECORTADO, 5.6), "DIÁLOGO RECORTADO · Maliketh, en inglés", "Oh, Márika… ¿qué pasó?",
          "pista recortado 1"),
    ban_p((P_RECORTADO, 5.7), (P_RECORTADO, 13.9), "DIÁLOGO RECORTADO · Maliketh, en inglés",
          "¿Fui yo el necio… o me engañaste tú?", "pista recortado 2"),

    # ---- 1d · el necio y Diego
    top(("Oh, Márika. Qué pasó", -.1), ("En ese mismo diálogo recortado", -.2), "Diálogo recortado · traducido",
        "¿Fui yo el necio, o me engañaste tú?", "necio"),
    peg(("Oh, Márika. Qué pasó", 0), "maliketh_cara", "Maliketh", dur=5.4, x=.20, y=.46, tam=400),
    top(("la bestia promete muerte a", -.1), ("Y te dice que, armado", -.2), "Diálogo recortado · traducido",
        "Muerte a los ladrones de la Muerte", "ladrones"),
    top(("Y te dice que, armado", -.1), ("el trono que desees|fin", .6), "Diálogo recortado · traducido",
        "Armado con la muerte, elige tu trono", "trono"),
    cam(("armado con la muerte, puedes", 0), "runa_muerte", "Armado con la muerte", dur=3.6, x=.17, y=.44,
        foco=(.5, .5, 1.0)),
    mg(E.triada([("Acusarla a ella", "sin más"), ("Preguntarse", "si el necio fue él")], titulo="Lo que no hace", w=1300),
       ("Fíjate en lo que no", -.2), ("Se pregunta si el necio fue él|fin", 1.0),
       [("no la acusa a ella sin", 0), ("Se pregunta si el necio", 0)], "no hace"),
    ban_p(("Y FromSoftware decidió que esa", -.1), ("no la oyera nadie|fin", .6), "Y FromSoftware decidió",
          "Que nadie la oyera", "nadie"),
    puesto(("Así que volvamos con Diego", 0), "Volvamos con Diego", "¿Solo servía a una tirana?", dur=6.0),   # R46: su tarjeta ya salió en introb
    peg(("Puede que la tirana existiera", 0), "marika", "La tirana", dur=3.0, x=.80, y=.44, tam=360),
    ban_p(("Pero antes de servirla, su", -.1), ("Y después, mandaba a otros", -.2), "Antes de servirla",
          "Se llamaba Muerte de los Semidioses", "antes de servirla"),
    ban_p(("Y después, mandaba a otros", -.1), ("arrancar raíces por él|fin", .7), "Y después",
          "Mandaba a otros por raíces", "despues"),
    cam(("Y después, mandaba a otros", 0), "d_cazador", "D", dur=3.6, x=.17, y=.44, foco=(.5, .3, 1.3)),

    # ================================================================ CIERRE
    mg(E.expediente(acusado="Maliketh, la Hoja Negra", sub="sombra de Márika, guardián de la Runa de la Muerte",
                    cargos=CARGOS, ya=0, sello="PROBADO", titulo="La fiscalía contra la Hoja Negra"),
       ("Esa es la lista", -.2), ("si lo habían engañado|fin", 1.0),
       [("Guardias remendados con la grasa", 0), ("Un cazador que arrancaba raíces", 0), ("Un nombre que significaba Muerte", 0),
        ("Una reina que acunaba recién#2", 0), ("Y una noche en la", 0), ("si lo habían engañado|fin", .1)],
       "expediente cierre"),
    puesto(("Y queda una última cosa", 0), "Una última cosa", "Dos formas de morir", dur=3.4),
    ban_p(("Maliketh tiene dos formas de", -.1), ("y cada jugador solo oyó una|fin", .6), "Cada jugador",
          "Solo oyó una", "solo una"),
    pant("maliketh_revelado_perfil", ("Si nunca le llevaste raíces", -.3), (P_NECIO, -.05), zoom=(1.0, 1.06)),
    ban_p(("Si nunca le llevaste raíces", -.1), (P_NECIO, -.05), "Si nunca le diste raíces", "Cuando cae, te desprecia",
          "desprecia"),
    # ---- PISTA 4: s_necio (7,94 s)
    ban_p((P_NECIO, .1), (P_NECIO, 4.4), "Maliketh, al caer · en inglés", "Sinluz necio… ¿para qué codicias la Muerte Escrita?",
          "pista necio 1"),
    ban_p((P_NECIO, 4.5), (P_NECIO, 8.0), "Maliketh, al caer · en inglés", "¿Para matar a quién?", "pista necio 2"),

    # ---- cierreb · la otra muerte
    top(("Sinluz necio. Para qué codicias", -.1), ("Pero si terminaste su misión", -.2), "Traducido del inglés",
        "¿Para qué codicias la Muerte Escrita?", "codicias"),
    peg(("Sinluz necio. Para qué codicias", 0), "maliketh_cara", "Te desprecia", dur=5.4, x=.20, y=.46, tam=400),
    rel(("si le diste de comer hasta", 0), "raiz_muerte", "Hasta la última raíz", dur=3.4, x=.22, y=.46, tam=420),
    ban_p(("Pero si terminaste su misión", -.1), (P_PERDON, -.05), "Si le diste de comer", "Su último aliento cambia",
          "cambia"),
    # ---- PISTA 5: s_perdon (11,34 s)
    ban_p((P_PERDON, .1), (P_PERDON, 4.9), "Maliketh, al caer · en inglés", "Perdóname, Márika…", "pista perdon 1"),
    ban_p((P_PERDON, 5.0), (P_PERDON, 11.4), "Maliketh, al caer · en inglés", "La Orden Dorada… ya no puede restaurarse",
          "pista perdon 2"),

    # ---- cierrec · las dos muertes, la jaula abierta, los próximos y la colección
    top(("Perdóname, Márika. La Orden", -.1), ("Al que nunca le dio", -.2), "Traducido del inglés",
        "Perdóname, Márika: la Orden no se restaura", "perdoname"),
    peg(("Perdóname, Márika. La Orden", 0), "marika", "A ella", dur=4.6, x=.80, y=.46, tam=380),
    mg(E.dos_muertes(izq=("Si nunca le diste raíces", "Te pregunta para matar a quién", "te desprecia"),
                     der=("Si terminaste su misión", "Le pide perdón a Márika", "y a ti no te dice nada"),
                     remate="Hasta el último aliento, solo a Márika"),
       ("Al que nunca le dio", -.2), ("y a nadie más|fin", 1.0),
       [("Al que nunca le dio", 0), ("Al que le dio de comer", 0), ("Hasta el último aliento, Maliketh", 0)],
       "dos muertes"),
    puesto(("Hasta su entrada cambia", 0), "Hasta su entrada", "Cambia", dur=3.0),
    pant("maliketh_revelado_cuerpo", ("cuando llegas a su arena", -.3), ("Y luego jura que la", -.1), zoom=(1.04, 1.12)),
    ban_p(("no te recibe como a", -.1), ("Y luego jura que la", -.2), "No te recibe", "Como a un ladrón", "ladron"),
    top(("Te pregunta por qué. Duda", -.1), ("Y luego jura que la", -.2), "Maliketh · en inglés", "Sinluz… ¿por qué…?",
        "por que"),
    top(("Y luego jura que la", -.1), ("no volverá a ser robada|fin", .6), "Maliketh · en inglés",
        "Juro que no volverán a robarla", "jura"),
    peg(("Y luego jura que la", 0), "maliketh_cara", "Lo jura", dur=4.0, x=.20, y=.46, tam=400),
    pant("runa_muerte_hoja_flotando", ("Y entonces lo vences", -.3), ("La Runa de la Muerte queda", 1.0)),
    mapa("mundo", [pto(M_FARUM, "Farum Azula", _P("runa_muerte_altar"), "inicio"),
                   pto(M_LEYNDELL, "Leyndell, la capital", _P("leyndell_wiki"), "meta")],
         ("La Runa de la Muerte queda", 1.0), ("El carcelero cae, y la", -.1),
         [("La Runa de la Muerte queda", 1.1), ("y la capital del reino", 0)], titulo="La Muerte, libre",
         sub="De Farum Azula a la capital", entrada="desenrolla", traza=1.6, margen=.26),
    mg(E.jaula_orden(), ("El carcelero cae, y la", -.2), ("sale de la jaula|fin", 1.4),
       [("El carcelero cae, y la", 0), ("El carcelero cae, y la", .3), ("El carcelero cae, y la", .6),
        ("y la muerte sale de", 0)], "jaula abierta"),
    peg(("no fue ninguna asesina de", 0), "asesina_cuchillo", "Ninguna asesina", dur=3.0, x=.20, y=.46, tam=380),
    puesto(("Fuiste tú#2", 0), "La puerta la abriste", "Tú", dur=3.0),
    grande(("a Bayle el Temible", 0), "bayle", "Bayle el Temible", lado="der", dur=2.6, tam=540, y=.46),
    aba([("rennala", "Rennala"), ("parches", "Parches"), ("zampaheces", "Zampaheces"), ("gideon", "Gideon")],
        ("a Rennala y a Rellana", -.1), ("Dinos cuál quieres|fin", .7),
        ["a Rennala y a Rellana", "a Parches, y al", "y al Zampaheces con", "con Gideon. Dinos"], "proximos", tam=260),
    aba([("marika", "Márika"), ("radagon_cara", "Radagon"), ("miquella", "Miquella"), ("malenia", "Malenia")],
        ("En el canal tienes las", -.2), ("Ranni, Melina, Radahn", -.2),
        ["de Márika y Radagon", ("de Márika y Radagon", .5), "de Miquella, Malenia", ("de Miquella, Malenia", .5)],
        "coleccion 1", tam=260),
    aba([("ranni", "Ranni"), ("melina", "Melina"), ("radahn", "Radahn"), ("morgott", "Morgott"), ("mohg_cara", "Mohg"),
         ("godrick", "Godrick")],
        ("Ranni, Melina, Radahn", -.1), ("Godfrey, Rykard, Messmer", -.15),
        ["Ranni, Melina, Radahn", "Melina, Radahn, Morgott", "Radahn, Morgott, Mohg", ("Radahn, Morgott, Mohg", .7),
         ("Radahn, Morgott, Mohg", 1.4), ("Radahn, Morgott, Mohg", 2.1)], "coleccion 2", tam=240),
    aba([("godfrey", "Godfrey"), ("rykard", "Rykard"), ("messmer", "Messmer")],
        ("Godfrey, Rykard, Messmer", -.1), ("y las tuyas|fin", .6),
        ["Godfrey, Rykard, Messmer", "Rykard, Messmer, y las", ("Rykard, Messmer, y las", .5)], "coleccion 3", tam=260),
    puesto(("Suscríbete, que vamos por", 0), "Suscríbete", "Rumbo a los 2 000", dur=3.4),
    cam(("Y si te gustan los", 0), "marika", "Manos sucias", dur=3.6, x=.16, y=.40, foco=(.5, .35, 1.3)),
    ban_p(("Crónicas de Tamriel, nuestro canal", -.3), ("Te lo dejo aquí al final|fin", .9), "Nuestro canal hermano",
          "Crónicas de Tamriel · Skyrim", "tamriel"),
    grande(("Y la próxima vez que", 0), "gurranq", "Una bestia que pide muerte", lado="izq", dur=4.4, tam=460, y=.42),
    ban_p(("pregúntate primero quién la dejó", -.1), ("A lo mejor la bestia", -.3), "Pregúntate primero",
          "Quién la dejó escapar", "escapar"),
    grande(("A lo mejor la bestia", 0), "maliketh_cara", "Maliketh, la Hoja Negra", lado="der", dur=4.6, tam=560, y=.46,
           marco="museo"),
    ban_p(("A lo mejor la bestia", -.1), ("la bestia ya lo sabe|fin", 1.2), "A lo mejor", "La bestia ya lo sabe",
          "ya lo sabe"),
]

FX = [d for d in FX if d]
if FALTAN:
    print("efectos.py: pantallas que aún no existen (cubiertas con su alternativa):", " ".join(sorted(set(FALTAN))))
