# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «Las 5 peores atrocidades de Radagon QUE IGNORASTE» (SECUENCIA YT, Runa Caída).
Todo con el kit de interfaz de Elden Ring por código (nucleo/mg_er.py), anclado a palabras de la voz:
- rótulo «ENEMIGO ABATIDO» por puesto (título del top + uno por atrocidad), banda a lo ancho.
- fichas de descripción de objeto (icono real de la wiki en medios/_iconos/) SOLO con lo que dice el guion, arriba a la derecha.
- 3 motion graphics: el mensaje del suelo «Radagon es Márika», los gemelos «hijos de un solo dios» y los dos matrimonios.
  python fab.py er_radagon_atrocidades fx hoja    previews/fx_NN.jpg (MÍRALA)
  python fab.py er_radagon_atrocidades fx         audio/fx.wav
"""
import os

import mg_er as E

CAMARA = {}
FUNDIDO = {}

_IC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "medios", "_iconos")
_FX, _FY = .74, .30     # fichas: arriba a la derecha (no tapan el centro del clip)


def ficha(en, nombre, texto, tipo=None, icono=None, dur=6.0, x=_FX, y=_FY, a=None):
    d = dict(tipo="mg", fn=E.descripcion(nombre, texto, tipo=tipo, icono=os.path.join(_IC, icono + ".png") if icono else None),
             en=en, x=x, y=y, sale=.35, nombre="ficha " + nombre, ver=1.6)
    if a:
        d.pop("en")
        d.update(de=en, a=a)
    else:
        d["dur"] = dur
    return d


def puesto(en, arriba, titulo, dur=3.4):
    return dict(tipo="mg", fn=E.puesto(arriba, titulo), en=en, dur=dur, y=.80, sale=.45, nombre="puesto " + titulo, ver=1.4)


FX = [
    # ---- gancho: la estatua de Leyndell
    dict(tipo="mg", fn=E.mensaje(["Solo la regresión revela secretos", "Radagon es Márika"]),
         de=("solo la regresión revela secretos", -.2), a=("Dice que Radagon es Márika|fin", 2.6),
         marcas=["solo la regresión revela secretos", "Radagon es Márika"], y=.80, sale=.5, nombre="MG mensaje", ver=3.0),
    puesto("las cinco peores atrocidades de Radagon", "Las 5 peores atrocidades de", "Radagon", dur=4.2),

    # ---- 5 · invasión de Liurnia
    puesto("Número cinco. Antes de ser rey", "Atrocidad número 5", "La invasión de Liurnia"),
    ficha("Un monumento de esa primera guerra", "Monumento de la primera guerra de Liurnia",
          "La gloria de Radagon *arde roja como su pelo*.", tipo="Monumento de espada", dur=5.5),
    ficha("según cuenta Miriel", "Miriel, pastor de los votos",
          "Radagon se arrepintió de sus agresiones territoriales y *le juró amor a Rennala*.", tipo="Lo que cuenta", dur=6.5),
    ficha("La Trenza roja de gigante", "Trenza roja de gigante",
          "Todos los gigantes tienen el pelo rojo, y *Radagon despreciaba el suyo*. Quizá era una maldición de su especie.",
          tipo="Látigo", icono="trenza", a=("como quien suelta un chisme y se va|fin", .3)),
    ficha("se lo heredó a su hijo Radahn", "Casco de melena roja de Radahn",
          "Radahn heredó el pelo rojo, *furioso y llameante*, de su padre Radagon.", tipo="Armadura de cabeza",
          icono="casco_radahn", dur=6.0),

    # ---- 4 · la espada de la primera esposa
    puesto("Bajamos al cuatro", "Atrocidad número 4", "La espada de su ex"),
    ficha("te suelta el Espadón de la Orden Áurea", "Espadón de la Orden Áurea",
          "Forjado por el rey consorte Radagon para simbolizar los principios de la Orden Áurea.", tipo="Arma legendaria",
          icono="espadon", a=("los principios de la Orden Áurea|fin", .4)),
    ficha("Pero la descripción guarda una línea", "Espadón de la Orden Áurea",
          "Hay señales de que antes fue el espadón que le dejó *su primera esposa, Rennala*.", tipo="Arma legendaria",
          icono="espadon", a=("lo rehizo como trofeo de su matrimonio nuevo|fin", .3)),

    # ---- 3 · los gemelos
    puesto("Número tres, los gemelos", "Atrocidad número 3", "Los gemelos malditos"),
    dict(tipo="mg", fn=E.gemelos(), de=("los dos son hijos de un solo dios", -.3), a=("la misma persona dos veces|fin", .5),
         marcas=["hijos de un solo dios", "Uno quedó maldito", "infancia eterna", "La otra llevaba"],
         y=.50, sale=.4, nombre="MG gemelos", ver=5.0),
    ficha("La Gran Runa de Malenia", "Gran Runa de Malenia",
          "Malenia es hija de la reina Márika y de Radagon, y su Gran Runa *debió ser la más sagrada de todas*.",
          tipo="Gran Runa", icono="runa_malenia", dur=4.9),
    ficha("Radagon le regaló al pequeño Miquella", "Anillos de luz de Radagon",
          "Regalo de su padre, Radagon, al pequeño Miquella. Miquella abandonó esa fe: *no podía hacer nada contra la "
          "putrefacción de Malenia*.", tipo="Milagro", a=("la putrefacción maldita de su hermana|fin", .5)),

    # ---- 2 · Radagon es Márika
    puesto("Ya en el podio", "Atrocidad número 2", "Radagon es Márika"),
    dict(tipo="mg", fn=E.doble_vida(), de=("Mientras Márika estaba casada", -.3), a=("le aplaudió la boda|fin", .8),
         marcas=["Mientras Márika estaba casada", "Radagon estaba casado con Rennala", "Cuando Godfrey fue exiliado",
                 "la reina se casó consigo misma"], y=.50, sale=.4, nombre="MG doble vida", ver=5.0),
    ficha("Con ese martillo la reina", "Martillo de Márika",
          "Con él la reina Márika *rompió el Círculo de Elden*, y Radagon *intentó repararlo*.", tipo="Martillo",
          icono="martillo", a=("no comparten la misma voluntad|fin", .4)),

    # ---- 1 · el huevo de Rennala
    puesto("Y llegamos al número uno", "Atrocidad número 1", "El huevo de Rennala"),
    ficha("Según Gideon Ofnir", "Gideon Ofnir, el omnisciente",
          "Rennala no es más que la receptora de *un huevo de ámbar que le dio Radagon*.", tipo="Lo que dice", dur=6.5),
    ficha("Las ropas de la reina", "Ropas de la reina",
          "Cuando Rennala perdió a su marido Radagon, *su corazón se fue con él*.", tipo="Armadura",
          a=("no era ninguna campeona|fin", .4)),
    ficha("la Gran Runa de los no nacidos", "Gran Runa de los no nacidos",
          "Todos los que renacen de Rennala son *frágiles y de vida corta*. Imperfectos, cada uno de ellos.",
          tipo="Gran Runa", icono="runa_no_nacidos", a=("Imperfectos, cada uno de ellos|fin", .8)),

    # ---- cierre: puente al video de Márika
    puesto("tienes que ver el video de las cinco peores atrocidades de Márika", "Ya en el canal · Las 5 peores",
           "Atrocidades de Márika", dur=5.0),
]
ROTULOS = []
SFX = {   # uno distinto por momento (regla: nada de SFX repetidos)
    "revela": ("Ethereal golden shimmer with a low choir swell revealing a hidden secret, dark fantasy", 4),
    "campana": ("One deep ominous church bell toll with a long reverb tail, dark fantasy", 4),
    "martillo": ("Heavy stone hammer striking a golden ring that cracks, deep metallic ring with reverb", 3),
    "lobo": ("Distant giant wolf howl echoing through a vast stone library", 4),
}
PISTAS = [
    dict(sfx="revela", en="Radagon es Márika", vol=.5),
    dict(sfx="martillo", en="Con ese martillo la reina", vol=.45),
    dict(sfx="campana", en="Y llegamos al número uno", vol=.5),
    dict(sfx="lobo", en="ronda un lobo gigante", vol=.4),
]
