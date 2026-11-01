# -*- coding: utf-8 -*-
"""Anclas de tiempo (palabras de la narración) y fases del plano secuencia «gravedad 5 s»."""
import types

from mundo_comun import T, INI, FIN, ESC0, ESC1, TOTAL

A = types.SimpleNamespace(
    # intro
    salto=T("intro", "salto"), pequeno=T("intro", "pequeño"),
    vuelves=T("intro", "vuelves"), suelo=T("intro", "suelo"),
    imagina=T("intro", "imagina"), gravedad_i=T("intro", "gravedad", frase=2),
    desaparece=T("intro", "desaparece"), cinco_i=T("intro", "cinco"),
    creen=T("intro", "creen"), volando=T("intro", "volando"), cohetes=T("intro", "cohetes"),
    rara=T("intro", "rara"), depende=T("intro", "depende"), apagues=T("intro", "apagues"),
    # version_a
    suave=T("version_a", "suave"), peso_a=T("version_a", "peso"), superficie=T("version_a", "superficie"),
    cero_a=T("version_a", "cero"), quieto=T("version_a", "quieto"), casa=T("version_a", "casa"),
    flotas=T("version_a", "flotas"), piso_a=T("version_a", "piso"),
    caminando=T("version_a", "caminando"), impulso=T("version_a", "impulso"), arriba_a=T("version_a", "arriba"),
    metro=T("version_a", "metro"), techo=T("version_a", "techo"), arbol=T("version_a", "árbol"),
    parque=T("version_a", "parque"),
    perros=T("version_a", "perros"), bicicletas=T("version_a", "bicicletas"), tazas=T("version_a", "tazas"),
    lenta=T("version_a", "lenta"),
    divertido=T("version_a", "divertido"), aire_a=T("version_a", "aire"),
    # viento_mar
    dos_v=T("viento_mar", "dos"), atmosfera=T("viento_mar", "atmósfera"), aplasta=T("viento_mar", "aplasta"),
    rebota_v=T("viento_mar", "rebota"), resorte=T("viento_mar", "resorte"),
    presion=T("viento_mar", "presión"), golpe_v=T("viento_mar", "golpe", frase=1),
    oidos=T("viento_mar", "oídos"), viento=T("viento_mar", "viento"),
    coches_v=T("viento_mar", "coches"), olas=T("viento_mar", "olas"), burbujas=T("viento_mar", "burbujas"),
    gira=T("viento_mar", "gira"), moverse=T("viento_mar", "moverse"), recta_v=T("viento_mar", "recta"),
    # caida_a
    cinco_ca=T("caida_a", "cinco", frase=0), regresa=T("caida_a", "regresa"),
    flotaba=T("caida_a", "flotaba"), diez=T("caida_a", "diez"), cae_ca=T("caida_a", "cae"),
    coches_ca=T("caida_a", "Coches"), golpean=T("caida_a", "golpean"),
    durisimo=T("caida_a", "durísimo"), humanidad=T("caida_a", "humanidad"),
    sobreviviria=T("caida_a", "sobreviviría"),
    # version_b
    total=T("version_b", "total"), apaga_b=T("version_b", "apaga", frase=0), universo=T("version_b", "universo"),
    cero_b=T("version_b", "cero"), interior=T("version_b", "interior"),
    brutal=T("version_b", "brutal"), roca=T("version_b", "roca"),
    soltar=T("version_b", "soltar"), rebota_b=T("version_b", "rebota"),
    rompe=T("version_b", "rompe"), lava=T("version_b", "lava"),
    tres_b=T("version_b", "tres"), luna=T("version_b", "Luna"),
    orbita=T("version_b", "órbita"), espacio_b=T("version_b", "espacio"),
    sol_b=T("version_b", "Sol", frase=4), nucleo=T("version_b", "núcleo"),
    hincha=T("version_b", "hincha"), fusion=T("version_b", "fusión"), nuclear=T("version_b", "nuclear"),
    cinco_b=T("version_b", "cinco"), volver_b=T("version_b", "volver"),
    desploma=T("version_b", "desploma"), funde=T("version_b", "funde"),
    # cierre
    suerte=T("cierre", "suerte"), interruptor=T("cierre", "interruptor"),
    cable=T("cierre", "cable"), forma=T("cierre", "forma"),
    doblada=T("cierre", "doblada"), materia=T("cierre", "materia"),
    proxima=T("cierre", "próxima"), caiga=T("cierre", "caiga"),
    piso_c=T("cierre", "piso"), enojes=T("cierre", "enojes"),
    tiron=T("cierre", "tirón"), unidos=T("cierre", "unidos"),
    mar_c=T("cierre", "mar"), estrellas=T("cierre", "estrellas"),
    fin=FIN("cierre"),
)

# ---- fases del plano secuencia (tiempos globales)
Z1 = (A.imagina - 0.1, A.desaparece + 0.6)            # del parque a la Tierra en el espacio (intro)
Z2 = (A.suave - 0.35, A.superficie + 0.55)            # del espacio a la casa/parque (versión A)
Z3 = (A.total - 0.35, A.universo + 0.65)              # del paisaje al espacio (versión B + principio del cierre)
Z4 = (A.proxima - 0.45, A.caiga + 0.15)               # vuelta al parque para el cierre
B0 = A.total - 0.35                                   # inicio de la versión B
TOTAL = TOTAL
