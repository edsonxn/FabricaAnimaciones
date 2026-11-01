# -*- coding: utf-8 -*-
"""Anclas de tiempo (palabras de la narración) y fases del plano secuencia «oxígeno 5 s»."""
import types

from mundo_comun import T, INI, FIN, ESC0, ESC1, TOTAL

A = types.SimpleNamespace(
    # intro
    respira=T("intro", "Respira"), imagina=T("intro", "imagina"), instante=T("intro", "instante"),
    tierra_i=T("intro", "Tierra"), desaparece=T("intro", "desaparece"), siempre=T("intro", "siempre"),
    cinco_i=T("intro", "cinco", frase=2), parece=T("intro", "parece"), respirar_i=T("intro", "respirar"),
    sitios=T("intro", "sitios"), crees=T("intro", "crees"), mundo_i=T("intro", "mundo"),
    muchisimo=T("intro", "muchísimo"),
    # reglas
    reglas=T("reglas", "reglas"), deja=T("reglas", "deja"), vuelve_r=T("reglas", "vuelve"),
    exactamente=T("reglas", "exactamente"), dos_formas=T("reglas", "dos"), primera=T("reglas", "primera"),
    respiramos=T("reglas", "respiramos"), gas_r=T("reglas", "gas"), segunda=T("reglas", "segunda"),
    ultimo=T("reglas", "último"), facil=T("reglas", "fácil"),
    # aire
    cero_a=T("aire", "cero"), cada_cinco=T("aire", "cinco"), esfuma=T("aire", "esfuma"),
    ligero=T("aire", "ligero"), presion=T("aire", "presión"), quinta=T("aire", "quinta"),
    montana=T("aire", "montaña"), dos_mil=T("aire", "dos"), oidos=T("aire", "oídos"),
    golpe=T("aire", "golpe", frase=3), despegar=T("aire", "despegar"), timpanos=T("aire", "tímpanos"),
    demasiado=T("aire", "demasiado"), cielo=T("aire", "cielo"), azul=T("aire", "azul"),
    nitrogeno=T("aire", "nitrógeno"), sigue_ahi=T("aire", "ahí"),
    # fuego
    uno_f=T("fuego", "uno"), fuegos=T("fuego", "fuegos"), apagan=T("fuego", "apagan"),
    velas=T("fuego", "Velas"), fogones=T("fuego", "fogones"), incendios=T("fuego", "incendios"),
    arder=T("fuego", "arder"), coches=T("fuego", "coches"), rodando=T("fuego", "rodando"),
    aviones=T("fuego", "aviones"), apagan_av=T("fuego", "apagan", frase=3), piedra=T("fuego", "piedra"),
    planea=T("fuego", "planea"), y1982=T("fuego", "mil", frase=5), jumbo=T("fuego", "jumbo"),
    cuatro_m=T("fuego", "cuatro"), ceniza=T("fuego", "ceniza"), planeo=T("fuego", "Planeó"),
    siete=T("fuego", "siete"), encender=T("fuego", "encender"), aterrizo=T("fuego", "aterrizó"),
    victima=T("fuego", "víctima"), centrales=T("fuego", "centrales"), sesenta=T("fuego", "sesenta"),
    quemar=T("fuego", "quemar"), llama=T("fuego", "llama"), seguridad=T("fuego", "seguridad"),
    apagones=T("fuego", "apagones"), sol_f=T("fuego", "Sol", frase=9), brillando=T("fuego", "brillando"),
    no_es_fuego=T("fuego", "fuego", frase=9), fusion=T("fuego", "fusión"), necesita=T("fuego", "necesita"),
    # cuerpo
    dos_c=T("cuerpo", "dos"), dentro=T("cuerpo", "dentro"), sangre=T("cuerpo", "sangre"),
    desaparece_c=T("cuerpo", "desaparece"), celulas=T("cuerpo", "células"), comida=T("cuerpo", "comida"),
    energia=T("cuerpo", "energía"), cerebro=T("cuerpo", "cerebro"), organo=T("cuerpo", "órgano"),
    y1943=T("cuerpo", "mil"), medicos=T("cuerpo", "médicos"), aguanta=T("cuerpo", "aguanta"),
    cortan=T("cuerpo", "cortan"), respuesta=T("cuerpo", "respuesta"), seis=T("cuerpo", "seis"),
    cinco_c=T("cuerpo", "Cinco"), borde=T("cuerpo", "borde"), mareo=T("cuerpo", "mareo"),
    tunel=T("cuerpo", "túnel"), desmayarse=T("cuerpo", "desmayarse"),
    # regreso A
    cinco_ra=T("regreso_a", "cinco"), vuelve_ra=T("regreso_a", "vuelve"), sube=T("regreso_a", "sube"),
    otro_golpe=T("regreso_a", "golpe"), contrario=T("regreso_a", "contrario"), brasas=T("regreso_a", "brasas"),
    pilotos=T("regreso_a", "pilotos"), motores_ra=T("regreso_a", "motores"), choques=T("regreso_a", "choques"),
    susto=T("regreso_a", "susto"), sobreviviriamos=T("regreso_a", "sobreviviríamos"),
    version_facil=T("regreso_a", "versión"),
    # atomos
    dificil=T("atomos", "difícil"), cada_atomo=T("atomos", "átomo"), sorpresa=T("atomos", "sorpresa"),
    gas_at=T("atomos", "gas"), mitad_at=T("atomos", "mitad"), rocas_at=T("atomos", "rocas"),
    agua_at=T("atomos", "agua"), noventa=T("atomos", "noventa"), cuerpo_at=T("atomos", "cuerpo"),
    dos_terceras=T("atomos", "dos"), pegamento=T("atomos", "pegamento"), tocas=T("atomos", "tocas"),
    # suelo
    cero_s=T("suelo", "cero"), rocas_s=T("suelo", "rocas"), concreto=T("suelo", "concreto"),
    mitad_s=T("suelo", "mitad"), solidos=T("suelo", "sólidos"), edificios=T("suelo", "edificios"),
    polvo=T("suelo", "polvo"), carreteras=T("suelo", "carreteras"), hunde=T("suelo", "hunde"),
    metales=T("suelo", "metales"), oxido=T("suelo", "óxido"), piezas=T("suelo", "piezas"),
    tocan=T("suelo", "tocan"), pegar=T("suelo", "pegar"), soldado=T("suelo", "soldado"),
    invento=T("suelo", "invento"), soldadura=T("suelo", "soldadura"), naves=T("suelo", "naves"),
    # agua
    uno_ag=T("agua", "uno"), deja_ag=T("agua", "deja"), molecula=T("agua", "molécula"),
    hidrogeno_ag=T("agua", "hidrógeno"), ligero_ag=T("agua", "ligero"), oceanos=T("agua", "océanos"),
    rios=T("agua", "ríos"), nubes=T("agua", "nubes"), convierte=T("agua", "convierte"),
    fondo_ag=T("agua", "fondo"), aplastado=T("agua", "aplastado"), kilometros=T("agua", "kilómetros"),
    expandiria=T("agua", "expandiría"), brutal=T("agua", "brutal"), treinta=T("agua", "treinta"),
    atmosfera=T("agua", "atmósfera"),
    # nosotros
    nosotros=T("nosotros", "nosotros"), terceras_n=T("nosotros", "terceras"), sobrevivir=T("nosotros", "sobrevivir"),
    agua_n=T("nosotros", "agua"), proteinas=T("nosotros", "proteínas"), genetico=T("nosotros", "genético"),
    llevan=T("nosotros", "llevan"), version_n=T("nosotros", "versión"), segundo_n=T("nosotros", "segundo"),
    ser_vivo=T("nosotros", "vivo"), superficie_n=T("nosotros", "superficie"),
    # regreso B
    cinco_rb=T("regreso_b", "cinco"), vuelve_rb=T("regreso_b", "vuelve"), revuelto=T("regreso_b", "revuelto"),
    movido=T("regreso_b", "movido"), mezclado=T("regreso_b", "mezclado"), combustible=T("regreso_b", "combustible"),
    cohetes=T("regreso_b", "cohetes"), exactamente_b=T("regreso_b", "exactamente"), calcular=T("regreso_b", "calcular"),
    bonito=T("regreso_b", "bonito"),
    # realidad
    suerte=T("realidad", "suerte"), interruptor=T("realidad", "interruptor"), siempre_r=T("realidad", "siempre"),
    millones_r=T("realidad", "millones"), casi_no=T("realidad", "tenía"), fabricaron=T("realidad", "fabricaron"),
    bacterias=T("realidad", "bacterias"), luz_r=T("realidad", "luz"), hoy=T("realidad", "Hoy"),
    mitad_r=T("realidad", "mitad"), oceano_r=T("realidad", "océano"), pequenos=T("realidad", "pequeños"),
    # cierre
    proxima=T("cierre", "próxima"), hondo_c=T("cierre", "hondo"), recuerda=T("cierre", "recuerda"),
    aire_c=T("cierre", "aire"), miles=T("cierre", "miles"), existir=T("cierre", "existir"),
    planeta_c=T("cierre", "planeta"), regala=T("cierre", "regala"), pocos=T("cierre", "pocos"),
    fin=FIN("cierre"),
)

# ---- fases del plano secuencia (tiempos globales)
Z1 = (A.imagina - 0.1, A.desaparece - 0.25)          # el paisaje se aleja hasta la Tierra en el espacio
Z2 = (A.facil - 0.55, FIN("reglas") + 0.95)           # vuelta al paisaje (versión A)
PORTAL_IN = (A.dentro - 0.35, A.dentro + 0.75)       # el pecho se abre: dentro del cuerpo
PORTAL_OUT = (A.mareo - 1.15, A.mareo - 0.15)        # salimos por la cabeza de vuelta al parque
Z3 = (A.calcular - 0.6, A.bonito + 0.2)              # el paisaje se aleja hasta la Tierra (fin de la versión B)
Z4 = (A.proxima - 0.45, A.recuerda + 0.15)           # bajamos al parque para el cierre
B0 = A.dificil - 0.3                                  # empieza la versión B (paleta y reglas)
TOTAL = TOTAL
