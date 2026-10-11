# -*- coding: utf-8 -*-
"""Anclas de tiempo (palabras de la narración) y fases del plano secuencia."""
import types

from mundo_comun import T, INI, FIN, ESC0, ESC1, TOTAL

A = types.SimpleNamespace(
    # intro
    apaga=T("intro", "apaga"), desaparece=T("intro", "desaparece"), gravedad_i=T("intro", "gravedad"),
    cuanto=T("intro", "Cuánto"), vida_q=T("intro", "vida"), sobrevivir_q=T("intro", "sobrevivir"),
    imposible=T("intro", "imposible"), sol_i=T("intro", "Sol", frase=4),
    # sol
    millon=T("sol", "millón"), tierras=T("sol", "Tierras"), noventa=T("sol", "noventa"),
    superficie=T("sol", "superficie"), nucleo_s=T("sol", "núcleo"), segundo=T("sol", "segundo"),
    seiscientos=T("sol", "seiscientos"), cuatro=T("sol", "cuatro"), energia=T("sol", "energía", frase=4),
    luz_s=T("sol", "luz", frase=5), tierra_s=T("sol", "Tierra", frase=5), hora=T("sol", "hora"),
    humanidad=T("sol", "humanidad"),
    # ocho
    ahora=T("ocho", "ahora"), ocho=T("ocho", "ocho", frase=1), nada=T("ocho", "nada"), hace=T("ocho", "hace"),
    burbuja=T("ocho", "burbuja"), mercurio=T("ocho", "Mercurio"), venus=T("ocho", "Venus"),
    grav_o=T("ocho", "gravedad"), diecisiete=T("ocho", "diecisiete"), choque=T("ocho", "choque"),
    vez=T("ocho", "vez"),
    # deriva
    alcanza=T("deriva", "alcanza"), disparada=T("deriva", "disparada"), tiron=T("deriva", "tirón"),
    luna_d=T("deriva", "Luna"), jupiter=T("deriva", "Júpiter"), neptuno=T("deriva", "Neptuno"),
    jupiter2=T("deriva", "Júpiter", frase=4), reflejo=T("deriva", "reflejo"), escapan=T("deriva", "escapan"),
    collar=T("deriva", "collar"),
    # errante
    treinta=T("errante", "treinta"), mil_km=T("errante", "mil"), estrella=T("errante", "estrella"),
    cuarenta=T("errante", "cuarenta"), galaxia=T("errante", "galaxia"), chocar=T("errante", "Chocar"),
    gigantesco=T("errante", "gigantesco"), errante=T("errante", "errante"), solos=T("errante", "solos"),
    lactea=T("errante", "Láctea"),
    # primer día
    aqui=T("primer_dia", "aquí"), cielo=T("primer_dia", "cielo"), negro=T("primer_dia", "negro"),
    estrellas=T("primer_dia", "estrellas"), mediodia=T("primer_dia", "mediodía"), luna_p=T("primer_dia", "Luna"),
    mareas=T("primer_dia", "mareas"), frio_p=T("primer_dia", "frío"), oceanos_p=T("primer_dia", "océanos"),
    semana=T("primer_dia", "semana"), cero1=T("primer_dia", "cero", fin=True),
    # vida en la superficie
    foto=T("vida_sup", "fotosíntesis"), plantas=T("vida_sup", "plantas"), arboles=T("vida_sup", "árboles"),
    decadas=T("vida_sup", "décadas"), animales=T("vida_sup", "animales"), despues=T("vida_sup", "después"),
    cadena=T("vida_sup", "cadena"), fito=T("vida_sup", "fitoplancton"), asfixia=T("vida_sup", "asfixiaríamos"),
    oxigeno=T("vida_sup", "oxígeno", frase=6),
    # frío
    ano=T("frio", "año"), cero2=T("frio", "cero", frase=0, fin=True), tiempo_atm=T("frio", "tiempo"),
    viento=T("frio", "viento"), oceanos_f=T("frio", "océanos"), manta=T("frio", "manta"),
    debajo=T("frio", "Debajo"), cientos=T("frio", "cientos"), dioxido=T("frio", "dióxido"), nieve=T("frio", "nieve"),
    millones_f=T("frio", "millones"), nitrogeno=T("frio", "nitrógeno"), aire_f=T("frio", "aire", frase=6),
    suelo_f=T("frio", "suelo"),
    # humanos
    nosotros=T("humanos", "nosotros"), calor_h=T("humanos", "calor"), poquisimo=T("humanos", "poquísimo"),
    tres=T("humanos", "tres"), islandia=T("humanos", "Islandia"), nueve=T("humanos", "nueve"),
    paneles=T("humanos", "paneles"), nucleares=T("humanos", "nucleares"), geotermica=T("humanos", "geotérmica"),
    cultivos=T("humanos", "cultivos"), oscura=T("humanos", "oscura"),
    # profundidades
    verdaderos=T("profundidades", "verdaderos"), fondo_p=T("profundidades", "fondo"),
    hidro=T("profundidades", "hidrotermales"), quimica=T("profundidades", "química"),
    gusanos=T("profundidades", "gusanos"), pies=T("profundidades", "pies"),
    kilometros=T("profundidades", "kilómetros"), setenta_p=T("profundidades", "setenta"),
    noticia=T("profundidades", "noticia"),
    # realidad
    suerte=T("realidad", "suerte"), materia=T("realidad", "materia"), interruptor=T("realidad", "interruptor"),
    luz_r=T("realidad", "luz"), nucleo_r=T("realidad", "núcleo"), rebotando=T("realidad", "rebotando"),
    detuviera=T("realidad", "detuviera"), millones_r=T("realidad", "millones"), neutrinos=T("realidad", "neutrinos"),
    # futuro
    cambiara=T("futuro", "cambiará"), mil_f=T("futuro", "mil"), oceanos_fu=T("futuro", "océanos"),
    cinco_f=T("futuro", "cinco"), gigante=T("futuro", "gigante"), tierra_f=T("futuro", "Tierra"),
    calcinada=T("futuro", "calcinada"), enana=T("futuro", "enana"), billones=T("futuro", "billones"),
    # cierre
    amanecer_c=T("cierre", "amanecer"), comida=T("cierre", "comida"), aire_c=T("cierre", "aire"),
    clima=T("cierre", "clima"), luz_c=T("cierre", "luz"), manana=T("cierre", "mañana"), salga=T("cierre", "salga"),
    gracias=T("cierre", "gracias", frase=2), fin=FIN("cierre"),
)

# ---- fases del plano secuencia
D1 = (A.aqui - 1.6, A.cielo + 0.25)                   # zoom desde la galaxia hasta la superficie oscura
B0 = FIN("profundidades") + 0.9                        # el calor del interior crece...
BM = B0 + 1.5                                          # ... llena la pantalla: es el Sol
B1 = BM + 2.2                                          # el Sol ya se ve entero
D2 = (INI("cierre", 1) - 0.7, INI("cierre", 1) + 1.4)  # inmersión por la línea del amanecer
TOTAL = TOTAL
