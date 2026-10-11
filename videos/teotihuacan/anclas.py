# -*- coding: utf-8 -*-
"""Anclas de tiempo (palabras de la narración) del plano secuencia de Teotihuacán."""
import types

from escena_base import TL, Escena

_ESC = {e["id"]: e for e in TL["escenas"]}
TOTAL = TL["total"]


def T(eid, texto, **kw):
    return Escena.w(types.SimpleNamespace(fr=_ESC[eid]["frases"], id=eid), texto, **kw)


def INI(eid, i=0):
    return _ESC[eid]["frases"][i]["t0"]


def FIN(eid, i=-1):
    return _ESC[eid]["frases"][i]["t1"]


A = types.SimpleNamespace(
    # intro
    hace=T("intro", "Hace"), cien=T("intro", "cien"), pir=T("intro", "pirámides"), regla=T("intro", "regla"),
    siglos=T("intro", "siglos"), ruinas=T("intro", "ruinas"), nadie=T("intro", "nadie"), ni=T("intro", "Ni"),
    esta=T("intro", "Esta"), teo=T("intro", "Teotihuacán", frase=4), nombre_i=T("intro", "nombre", frase=4),
    # valle
    cuarenta=T("valle", "cuarenta"), ciudad_v=T("valle", "Ciudad"), cuenca=T("valle", "cuenca"),
    lagos=T("valle", "lagos"), montanas=T("valle", "montañas"), pobladores=T("valle", "pobladores"),
    dosmil=T("valle", "dos", frase=2), veinte=T("valle", "veinte"), mexicas_v=T("valle", "mexicas"),
    dioses_v=T("valle", "dioses"), sabemos=T("valle", "sabemos"),
    # trazo
    azar=T("trazo", "azar"), cuadr=T("trazo", "cuadrículas"), km=T("trazo", "kilómetros"),
    calzada=T("trazo", "Calzada"), tumbas=T("trazo", "tumbas"), templos=T("trazo", "templos"),
    luna=T("trazo", "Luna"), sol_t=T("trazo", "Sol"), sesenta=T("trazo", "sesenta"),
    animales=T("trazo", "animales"), gente_t=T("trazo", "gente"),
    # gente
    cien_g=T("gente", "cien"), conjuntos=T("gente", "conjuntos"), murales=T("gente", "murales"),
    jaguares=T("gente", "jaguares"), extranj=T("gente", "extranjeros"), oaxaca=T("gente", "Oaxaca"),
    talleres=T("gente", "talleres"), obsidiana=T("gente", "obsidiana"),
    # comercio
    navajas=T("comercio", "navajas"), pachuca=T("comercio", "Pachuca"), mayas=T("comercio", "mayas"),
    tikal=T("comercio", "Tikal"), tres78=T("comercio", "trescientos"), guerrero=T("comercio", "guerrero"),
    rey=T("comercio", "rey"), trono=T("comercio", "trono"), conquista=T("comercio", "conquista"),
    alianza=T("comercio", "alianza"), mezcla=T("comercio", "mezcla"), lejos=T("comercio", "lejos"),
    # tunel
    bajo=T("tunel", "tierra"), dos2003=T("tunel", "dos", frase=1), tormenta=T("tunel", "tormenta"),
    hueco=T("tunel", "hueco"), tunel=T("tunel", "túnel", frase=2), cien_u=T("tunel", "cien"),
    sellado=T("tunel", "sellado"), camaras=T("tunel", "cámaras"), objetos=T("tunel", "objetos"),
    conchas=T("tunel", "conchas"), jade=T("tunel", "jade"), esferas=T("tunel", "esferas"),
    paisaje=T("tunel", "paisaje"), mercurio=T("tunel", "mercurio"), tumba=T("tunel", "tumba"),
    todavia=T("tunel", "Todavía"),
    # fuego
    arder=T("fuego", "arder"), quinientos=T("fuego", "quinientos"), calzada_f=T("fuego", "Calzada"),
    elite=T("fuego", "élite"), escult=T("fuego", "esculturas"), destroz=T("fuego", "destrozadas"),
    casas=T("fuego", "casas"), salvaron=T("fuego", "salvaron"), quien=T("fuego", "Quién"),
    rebelo=T("fuego", "rebeló"), ataque=T("fuego", "ataque"), clima=T("fuego", "clima"),
    sequias=T("fuego", "sequías"), varias=T("fuego", "varias"),
    # silencio
    marchando=T("silencio", "marchando"), dispersaron=T("silencio", "dispersaron"), simbolos=T("silencio", "símbolos"),
    texto=T("silencio", "texto"), lluvia=T("silencio", "lluvia"), maleza=T("silencio", "maleza"),
    siglos_s=T("silencio", "siglos"), nombre_s=T("silencio", "nombre"),
    # mexicas
    catorce=T("mexicas", "Siglos"), llegaron=T("mexicas", "llegaron"), dioses_m=T("mexicas", "dioses", frase=1),
    oscuridad=T("mexicas", "oscuridad"), nuevo_sol=T("mexicas", "Sol", frase=2), rico=T("mexicas", "rico"),
    pobre=T("mexicas", "pobre"), dudo=T("mexicas", "dudó"), cuatro=T("mexicas", "cuatro"),
    salto=T("mexicas", "saltó"), nacio=T("mexicas", "nació"), conocemos=T("mexicas", "conocemos"),
    # hoy
    patrim=T("hoy", "Patrimonio"), siete=T("hoy", "siete"), millon=T("hoy", "millón"), primavera=T("hoy", "primavera"),
    suben=T("hoy", "suben"), luz_h=T("hoy", "luz"), bajo_h=T("hoy", "Bajo"), tuneles=T("hoy", "túneles"),
    murales_h=T("hoy", "murales", frase=3), tumbas_h=T("hoy", "tumbas", frase=3),
    # cierre
    enorme=T("cierre", "enorme"), misterio=T("cierre", "misterio"), fascina=T("cierre", "fascinando"),
    bitacora=T("cierre", "Bitácora"), proxima=T("cierre", "próxima"),
)
