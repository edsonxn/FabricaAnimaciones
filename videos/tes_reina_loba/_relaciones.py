# -*- coding: utf-8 -*-
"""Redes de RELACIONES E INTENCIONES de «La Reina Loba» (mg_tes.red), una por capítulo donde la historia se enreda.
El usuario (13-nov-2026): «se pierde el hilo de la historia, sobre todo de los personajes, de saber quién es quién y las
intenciones de cada quien». Todas las intenciones, rótulos y notas salen del guion (guion.py / beats.json), sin lore
inventado; quien no tiene imagen real (Lord Thone, el embajador, el espía, el duque Mentin, el prometido, Orgnum) va con
busto en sombra. Dónde va cada una (anclas, duración y qué FX quitar): previews/relaciones_plan.md.
Uso en efectos.py:
    from _relaciones import red_cap1
    mg(red_cap1([dict(ver=[...]), ...]), "ancla de", ("ancla a", .1), ["marca 0", "marca 1", ...], "red cap 1", y=.5)
Cada red_capN(pasos=None) devuelve la función del MG; sin pasos usa PASOS_CAPN (los de la propuesta).
    python _relaciones.py      imprime los avisos de geometría de cada red (deben salir vacíos)
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
import mg_tes as T  # noqa: E402
from _arbol import PERSONAS as _A  # noqa: E402  (mismos retratos y encuadres que el árbol genealógico)


def _p(s):
    return os.path.join(AQUI, "pegatinas", s + ".png")


def _de(k, **kw):
    """Persona del árbol con su retrato y encuadre; kw cambia nombre/subtítulo/posición/intención."""
    a = _A[k]
    d = dict(n=a["n"], s=a["s"], img=a["img"], foco=a.get("foco"))
    d.update(kw)
    return d


def _sombra(n, s, **kw):
    return dict(n=n, s=s, img=None, **kw)


GEMA = (_p("gema_lobo"), (.5, .5, 1.25))
ANCIANA = (.53, .44, 3.0)           # cara de la anciana en flow_anciana_gema (1920x1072)


# =========================================================== 1 · El contrato robado (año 80)
P1 = {
    "pelagio2": _de("pelagio2", n="Pelagio", s="Hijo del emperador, padre de Potema", x=0.0, y=0.0),
    "uriel2": dict(n="Uriel II", s="Emperador, el abuelo", img=_p("uriel_ii"), foco=(.38, .2, 2.1), x=.40, y=0.0,
                   q=("NO CUMPLE", "ni la boda ni el oro")),
    "emb": _sombra("El embajador", "De Soledad", x=1.0, y=0.0, q=("EXIGE", "la boda prometida o el oro")),
    "potema": _de("potema", n="Potema", s="12 años", x=.40, y=1.0, q=("LE INTERESA", "abrir lo que está cerrado")),
    "mantiarco": _de("mantiarco", s="Rey de Soledad, 62 años", x=1.0, y=1.0),
}
N1 = [
    dict(a="uriel2", b="pelagio2", t="alianza", r="Padre e hijo"),
    dict(id="amenaza", a="emb", b="uriel2", t="rivalidad", r="Amenaza con el contrato", icono="contrato",
         rota="Sin contrato no hay amenaza"),
    dict(id="robo", a="potema", b="emb", t="hecho", r="Le roba el contrato", icono="contrato"),
    dict(id="ofrece", a="uriel2", b="potema", t="manipula", r="La ofrece a cambio"),
    dict(id="boda", a="potema", b="mantiarco", t="matrimonio", r="Boda a los 14"),
]
# 1.ª aparición: el trato roto, mientras Potema escucha detrás del tapiz
PASOS_CAP1A = [
    dict(ver=["uriel2", "pelagio2"]),
    dict(ver=["emb"]),
    dict(foco=["uriel2", "pelagio2"], zoom=1.0, nota="La boda prometida no va a ocurrir. El oro, tampoco"),
    dict(ver=["amenaza"], foco=["emb", "uriel2"]),
    dict(ver=["potema"], foco=["potema"], nota="Y detrás del tapiz, Potema escucha"),
]
# 2.ª aparición: el contrato ya no está y el emperador paga con su nieta
PASOS_CAP1B = [
    dict(ver=["uriel2", "pelagio2", "emb", "potema", "amenaza"]),
    dict(ver=["robo"], rompe=["amenaza"], cambia={"potema": ("TIENE", "el contrato robado")}, foco=["potema", "emb"]),
    dict(foco=["uriel2"], zoom=1.0, nota="Sin contrato, el emperador tiene que ofrecer otra cosa"),
    dict(ver=["ofrece"], foco=["uriel2", "potema"], zoom=1.0),
    dict(foco=[]),
    dict(ver=["mantiarco", "boda"], foco=["potema", "mantiarco"], nota="Ella, trece años. Él, sesenta y dos"),
]


def red_cap1(pasos=None):
    return T.red("El contrato robado", P1, N1, pasos or PASOS_CAP1B)


# =========================================================== 2 · El heredero que estorba (Soledad, año 97)
P2 = {
    "vhokken": _sombra("Lord Vhokken", "Su mano derecha", x=0.0, y=0.0),
    "potema": _de("potema", s="Reina de Soledad", x=.42, y=0.0, q=("QUIERE", "quitar de en medio al heredero")),
    "mantiarco": _de("mantiarco", s="Rey de Soledad", x=1.0, y=0.0, q=("NECESITA", "un heredero")),
    "thone": _sombra("Lord Thone", "Jefe guerrero del rey", x=.10, y=1.0),
    "bathorgh": _de("bathorgh", s="Hijo del primer matrimonio", x=.72, y=1.0, q=("ES", "el heredero legítimo")),
}
N2 = [
    dict(a="vhokken", b="potema", t="lealtad", r="A sus órdenes"),
    dict(a="potema", b="mantiarco", t="matrimonio", r="Esposa"),
    dict(a="mantiarco", b="bathorgh", t="lealtad", r="Su hijo y heredero"),
    dict(id="acusa_thone", a="potema", b="thone", t="traicion", r="Pruebas falsas de traición"),
    dict(id="cartas", a="potema", b="bathorgh", t="traicion", r="Cartas de amor falsas", icono="carta"),
    dict(id="padre", a="thone", b="bathorgh", t="hecho", r="¿Su padre?", punteado=True),
]
PASOS_CAP2 = [
    dict(ver=["potema", "vhokken", "mantiarco", "bathorgh"]),
    dict(ver=["thone", "acusa_thone"], foco=["potema", "thone"]),
    dict(foco=[]),
    dict(ver=["cartas", "padre"], foco=["bathorgh", "thone", "potema"], zoom=1.0),
    dict(foco=["bathorgh", "thone"], nota="Fechadas justo cuando nació Bathorgh"),
]


def red_cap2(pasos=None):
    return T.red("El heredero que estorba", P2, N2, pasos or PASOS_CAP2)


# =========================================================== 3 · La gema del lobo (año 98)
P3 = {
    "quintila": _de("quintila", s="Su madre, moribunda", x=0.0, y=0.0, q=("LE PREDICE", "su muerte y la de Mantiarco")),
    "espia": _sombra("El espía", "Maestro de espías de Antíoco", x=.55, y=0.0, q=("VIGILA A", "Potema")),
    "potema": _de("potema", s="Reina de Soledad", x=.12, y=1.0, q=("QUIERE", "que Antíoco renuncie al trono")),
    "antioco": _de("antioco", s="El heredero, 43 años", x=.88, y=1.0, q=("QUIERE", "ser coronado")),
}
N3 = [
    dict(a="quintila", b="potema", t="hecho", r="Le regala la gema", icono=GEMA),
    dict(id="vigila", a="espia", b="potema", t="hecho", r="La vigila"),
    dict(id="hechizo", a="potema", b="espia", t="manipula", r="La gema lo hechiza", rota="El encanto dura poco"),
    dict(id="falsa", a="potema", b="antioco", t="traicion", r="Carta falsa: «hijo del mayordomo»", icono="carta"),
    dict(id="sueldo", a="antioco", b="espia", t="lealtad", r="Le paga un buen sueldo", icono="moneda"),
    dict(id="acusa", a="antioco", b="potema", t="rivalidad", r="La acusa: las cartas de Soledad", curva=-.12),
]
PASOS_CAP3 = [
    dict(ver=["quintila", "potema", "antioco", "espia", "vigila"]),
    dict(ver=["hechizo"], foco=["potema", "espia"]),
    dict(ver=["falsa"], foco=["potema", "antioco"], zoom=1.0),
    dict(foco=[], nota="O renuncia al trono, o el escándalo"),
    dict(rompe=["hechizo"], foco=["espia", "potema"]),
    dict(ver=["sueldo"], foco=["antioco", "espia"]),
    dict(ver=["acusa"], foco=["antioco", "potema"], zoom=1.0),
    dict(cambia={"antioco": ("SERÁ", "emperador")}, foco=["antioco"]),
    dict(cambia={"potema": ("QUIERE", "que no reine mucho tiempo")}, foco=["potema", "antioco"], zoom=1.0,
         nota="«Sí, lo serás, hermano. Pero no por mucho tiempo»"),
]


def red_cap3(pasos=None):
    return T.red("La gema del lobo", P3, N3, pasos or PASOS_CAP3)


# =========================================================== 4 · Los elfos del mar (año 110)
P4 = {
    "psijic": dict(n="Los psijic", s="Monjes de Artaeum", img=_p("psijic_quaranir"), foco=(.47, .2, 3.2), x=0.0, y=0.0,
                   q=("PEDÍAN", "50 millones")),
    "antioco": _de("antioco", s="Emperador", x=1.0, y=0.0, q=("QUIERE", "defender la costa")),
    "orgnum": _sombra("Orgnum", "Rey de los maormer", x=0.0, y=1.0, q=("BUSCA", "aliados contra el Imperio")),
    "potema": _de("potema", s="Regente de Soledad", x=.55, y=1.0, q=("NO PROMETE", "nada a nadie")),
}
N4 = [
    dict(id="oferta", a="antioco", b="psijic", t="hecho", r="Les ofrece 12 millones", icono="moneda"),
    dict(id="finge", a="potema", b="psijic", t="manipula", r="Finge aliarse con los maormer"),
    dict(id="cobra", a="potema", b="antioco", t="traicion", r="Le cobra 12, paga 8"),
    dict(id="noche", a="orgnum", b="potema", t="alianza", r="Esa noche, juntos", icono=(_p("maormer"), (.5, .17, 3.0))),
]
PASOS_CAP4 = [
    dict(ver=["psijic", "antioco", "potema", "orgnum", "oferta", "finge"]),
    dict(cambia={"psijic": ("COBRAN", "8 millones")}, foco=["psijic"]),
    dict(ver=["cobra"], foco=["potema", "antioco"]),
    dict(ver=["noche"], foco=["orgnum", "potema"]),
    dict(foco=["potema"], zoom=1.0, nota="Su capacidad para mentir funcionaba en muchas culturas"),
    dict(cambia={"potema": ("SE QUEDA", "4 millones")}, foco=[], nota="A veces, hacer que la gente te odie es como se gana dinero"),
]


def red_cap4(pasos=None):
    return T.red("El negocio de la regente", P4, N4, pasos or PASOS_CAP4)


# =========================================================== 5 · La trampa de La Cañada (año 120)
P5 = {
    "potema": _de("potema", s="La tía desterrada", x=0.0, y=0.0, q=("DESTERRADA", "por Kintyra")),
    "prometido": _sombra("Su prometido", "Sale con un segundo ejército", x=1.0, y=0.0),
    "mentin": _sombra("Duque Mentin", "De La Cañada", x=0.0, y=1.0, q=("TRAICIONA", "al Imperio")),
    "kintyra": _de("kintyra", s="Emperatriz, 15 años", x=.55, y=1.0, q=("VA EN PERSONA", "a ayudar al duque")),
}
N5 = [
    dict(id="carta", a="kintyra", b="prometido", t="lealtad", r="Su prometido", icono="carta",
         rota="Una carta que ella nunca escribió"),
    dict(a="potema", b="kintyra", t="rivalidad", r="La sobrina contra la tía"),
    dict(id="trampa", a="mentin", b="kintyra", t="traicion", r="Le pide auxilio: la trampa"),
    dict(id="oro", a="potema", b="mentin", t="alianza", r="Miedo… y oro", icono="moneda"),
]
PASOS_CAP5 = [
    dict(ver=["kintyra", "prometido", "carta", "mentin", "trampa"]),
    dict(rompe=["carta"], foco=["kintyra", "prometido"], nota="Kintyra nunca escribió esa carta"),
    dict(foco=["mentin", "kintyra"]),
    dict(ver=["potema", "oro"], cambia={"mentin": ("POR", "miedo… y oro")}, foco=["mentin", "potema"]),
    dict(foco=["potema"], nota="El ejército de muertos: un rumor que ella misma fomenta"),
    dict(foco=["potema"], cambia={"potema": ("SU ARMA", "el miedo")}, zoom=1.0),
]


def red_cap5(pasos=None):
    return T.red("La trampa de La Cañada", P5, N5, pasos or PASOS_CAP5)


# =========================================================== 6 · La guerra del Diamante Rojo (año 127)
P6 = {
    "uriel": _de("uriel", s="Hijo de Potema", x=0.0, y=0.0, q=("SE CORONA", "con el apellido Septim")),
    "potema": _de("potema", s="La Reina Loba, 60 años", x=0.0, y=1.0, q=("PELEA", "bajo el Diamante Rojo")),
    "cefor": _de("cefor", s="Rey de Gilane", x=1.0, y=0.0, q=("RECUPERA", "el oeste de Roca Alta")),
    "magnus": _de("magnus", s="Rey de Lilmoth", x=1.0, y=1.0, q=("LLEVA", "un ejército de argonianos")),
}
N6 = [
    dict(a="potema", b="uriel", t="alianza", r="Madre e hijo"),
    dict(a="cefor", b="magnus", t="alianza", r="Hermanos"),
    dict(id="ichidag", a="cefor", b="uriel", t="rivalidad", r="Lo derrota en Ichidag"),
    dict(id="halcon", a="potema", b="magnus", t="rivalidad", r="Estrella del Halcón"),
]
PASOS_CAP6 = [
    dict(ver=["uriel", "potema", "cefor", "magnus", "ichidag"], tacha=["uriel"]),
    dict(cambia={"cefor": ("ES", "emperador")}, foco=["cefor"]),
    dict(ver=["halcon"], foco=["potema", "magnus"], zoom=1.0),
    dict(cambia={"potema": ("GANA", "la batalla. Pierde a su hijo")}, foco=["potema"]),
    dict(foco=["potema", "uriel"], nota="Ella no mira a nadie"),
]


def red_cap6(pasos=None):
    return T.red("Dos ramas, un diamante", P6, N6, pasos or PASOS_CAP6)


# =========================================================== 7 · La gema y el anillo (años 137-140)
P7 = {
    "magnus": _de("magnus", s="Padre de Pel", x=0.0, y=0.0),
    "potema": dict(n="Potema", s="La anciana, 70 años", img=_p("flow_anciana_gema"), foco=ANCIANA, x=.55, y=0.0,
                   q=("DEJA", "una gema maldita y un anillo")),
    "pel": dict(n="Pel", s="Hijo de Magnus", img=_p("pelagio_nino"), foco=(.51, .29, 3.3), x=0.0, y=1.0,
                q=("SERÁ", "el emperador Pelagio III")),
    "cefor": _de("cefor", s="Emperador Céforo I", x=1.0, y=1.0, q=("RECIBE", "un anillo «de levitación»")),
}
N7 = [
    dict(a="magnus", b="pel", t="lealtad", r="Su hijo"),
    dict(id="gema", a="potema", b="pel", t="manipula", r="Le cuelga la gema maldita", icono=GEMA),
    dict(id="anillo", a="potema", b="cefor", t="traicion", r="Resistencia al fuego, no levitación", icono="anillo"),
]
PASOS_CAP7 = [
    dict(ver=["magnus", "potema", "pel", "cefor", "gema", "anillo"], tacha=["potema"]),
    dict(tacha=["cefor"], foco=["cefor"]),
    dict(foco=["anillo", "potema", "cefor"], zoom=1.0, nota="¿Llevaba puesto el anillo?"),
    dict(foco=["gema", "potema", "pel"], zoom=1.0, nota="Y Pel lleva la gema al cuello"),
]


def red_cap7(pasos=None):
    return T.red("Lo que dejó la anciana", P7, N7, pasos or PASOS_CAP7)


REDES = [("cap1a", lambda: red_cap1(PASOS_CAP1A), PASOS_CAP1A), ("cap1b", red_cap1, PASOS_CAP1B), ("cap2", red_cap2, PASOS_CAP2),
         ("cap3", red_cap3, PASOS_CAP3), ("cap4", red_cap4, PASOS_CAP4), ("cap5", red_cap5, PASOS_CAP5),
         ("cap6", red_cap6, PASOS_CAP6), ("cap7", red_cap7, PASOS_CAP7)]

if __name__ == "__main__":
    for nombre, f, _ in REDES:
        fn = f()
        print(nombre, "OK" if not fn.avisos else fn.avisos)
