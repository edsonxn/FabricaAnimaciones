# -*- coding: utf-8 -*-
"""Anclas de tiempo (palabras de la narración, tiempo GLOBAL) del plano secuencia «dos lunas»."""
import types

from mundo_comun import T, INI, FIN, ESC0, ESC1, TOTAL

A = types.SimpleNamespace(
    # ---------------------------------------------------------------- 1. intro (0:00-0:22)
    tierra_i=T("intro", "Tierra", frase=0), sola=T("intro", "sola", frase=0), dos0=T("intro", "dos", frase=0),
    piedrita=T("intro", "piedrita"), enorme=T("intro", "enorme"), junto=T("intro", "junto"),
    donde1=T("intro", "dónde", frase=2, n=0), saldria=T("intro", "saldría"), donde2=T("intro", "dónde", frase=2, n=1),
    vivir=T("intro", "vivir"), que_i=T("intro", "qué", frase=2), planeta=T("intro", "planeta"),
    mareas_i=T("intro", "mareas"), locura=T("intro", "locura"),
    final_i=T("intro", "final"), quizas=T("intro", "quizás"), dos_f=T("intro", "dos", frase=4),
    # ---------------------------------------------------------------- 2. hoy
    luna_h=T("hoy", "Luna", frase=0), conocemos=T("hoy", "conocemos"),
    cuatro=T("hoy", "cuatrocientos"), km=T("hoy", "kilómetros"), pesa=T("hoy", "pesa"), ochenta=T("hoy", "ochenta"),
    tierra_h=T("hoy", "Tierra", frase=1), menos=T("hoy", "menos"),
    poca=T("hoy", "poca"), oceanos=T("hoy", "océanos"), dos_veces=T("hoy", "dos veces"), dia=T("hoy", "día"),
    marea=T("hoy", "marea"), tira=T("hoy", "tira"), cercano=T("hoy", "cercano"), lejano=T("hoy", "lejano"),
    estira=T("hoy", "estira"), agua=T("hoy", "agua"),
    # ---------------------------------------------------------------- 3. origen
    primera=T("origen", "Primera"), otra_o=T("origen", "otra"),
    uno=T("origen", "uno"), capturarla=T("origen", "capturarla"), asteroide=T("origen", "asteroide", frase=1),
    pasa=T("origen", "pasa", frase=1), atrapa=T("origen", "atrapa"),
    neptuno=T("origen", "Neptuno"), triton=T("origen", "Tritón"), viajera=T("origen", "viajera"), fuera=T("origen", "fuera"),
    dificilisimo=T("origen", "dificilísimo"), casi=T("origen", "casi", frase=3), largo=T("origen", "largo"),
    y2024=T("origen", "veinticuatro"), once=T("origen", "once"), dos_meses=T("origen", "dos meses"), mini=T("origen", "mini"),
    se_fue=T("origen", "fue", frase=5),
    fabricarla=T("origen", "fabricarla"), choque1=T("origen", "choque", frase=6), lanza=T("origen", "lanza"),
    junta=T("origen", "junta"), luna_o=T("origen", "luna", frase=6),
    nacio=T("origen", "nació"), cuatro_mil=T("origen", "cuatro", frase=7), anos=T("origen", "años", frase=7),
    distinto=T("origen", "distinto"), salido=T("origen", "salido"), dos_o=T("origen", "dos", frase=8),
    # ---------------------------------------------------------------- 4. orbita
    segunda=T("orbita", "Segunda"), donde_o=T("orbita", "dónde"), sitio=T("orbita", "sitio"),
    gravedad=T("orbita", "gravedad", frase=1), hasta=T("orbita", "hasta"), millon=T("orbita", "millón"),
    mas_alla=T("orbita", "Más"), sol_o=T("orbita", "Sol"), lleva=T("orbita", "lleva"),
    seguras=T("orbita", "seguras"), mitad=T("orbita", "mitad"),
    lunas_o=T("orbita", "lunas", frase=3), estorban=T("orbita", "estorban"), tira_o=T("orbita", "tira"),
    chocan=T("orbita", "chocan", frase=3), disparada=T("orbita", "disparada"),
    excepcion=T("orbita", "excepción"), jano=T("orbita", "Jano"), epimeteo=T("orbita", "Epimeteo"),
    saturno=T("orbita", "Saturno"), comparten=T("orbita", "comparten"),
    alcanza=T("orbita", "alcanza"), no_chocan=T("orbita", "chocan", frase=5), intercambian=T("orbita", "intercambian"),
    cuatro_anos=T("orbita", "cuatro", frase=5),
    escondite=T("orbita", "escondite"), equilibrio=T("orbita", "equilibrio"), sesenta=T("orbita", "sesenta"),
    delante=T("orbita", "delante"), detras=T("orbita", "detrás"), luna_o2=T("orbita", "Luna", frase=6),
    ahi=T("orbita", "Ahí"), compensan=T("orbita", "compensan"), segunda_luna=T("orbita", "segunda", frase=7),
    persiguiendo=T("orbita", "persiguiendo"), jamas=T("orbita", "jamás"),
    # ---------------------------------------------------------------- 5. cielo
    imagina=T("cielo", "Imagina"), abajo=T("cielo", "abajo"),
    dos_c=T("cielo", "Dos"), separadas=T("cielo", "separadas"), seis=T("cielo", "seis"), punos=T("cielo", "puños"),
    cielo_c=T("cielo", "cielo", frase=1),
    fases=T("cielo", "fases"), creciente=T("cielo", "creciente"), otra_c=T("cielo", "otra"), menguando=T("cielo", "menguando"),
    velocidad=T("cielo", "velocidad"), repetiria=T("cielo", "repetiría"), cinco=T("cielo", "cinco"),
    dias=T("cielo", "días"), diferencia=T("cielo", "diferencia"),
    noches=T("cielo", "noches"), claras=T("cielo", "claras"), animales=T("cielo", "animales"),
    corales=T("cielo", "corales"), llena=T("cielo", "llena"), sabrian=T("cielo", "sabrían"), obedecer=T("cielo", "obedecer"),
    bonito=T("cielo", "Bonito"), tranquila=T("cielo", "tranquila"), cosa=T("cielo", "cosa"), vamos=T("cielo", "vamos"),
    ponerla=T("cielo", "ponerla"), cerca=T("cielo", "cerca"),
    # ---------------------------------------------------------------- 6. mareas (163,6-202,9)
    mitad_m=T("mareas", "mitad", frase=0), ciento=T("mareas", "ciento"), km_m=T("mareas", "kilómetros"),
    tiron_m=T("mareas", "tirón"), cubo=T("mareas", "cubo"), cercania=T("mareas", "cercanía"),
    mitad_m2=T("mareas", "mitad", frase=2), ocho=T("mareas", "ocho"), fuerte=T("mareas", "fuerte"),
    oceanos_m=T("mareas", "océanos"), metros_m=T("mareas", "metros", frase=3), dos_veces_m=T("mareas", "dos veces"),
    costas=T("mareas", "costas", frase=3),
    record=T("mareas", "récord"), diecis=T("mareas", "dieciséis"), fundy=T("mareas", "Fundy"), canada=T("mareas", "Canadá"),
    esa_luna=T("mareas", "esa Luna"), normal=T("mareas", "normal"),
    dos_lunas_m=T("mareas", "dos Lunas"), alinearan=T("mareas", "alinearan"), tirones=T("mareas", "tirones"),
    sumarian=T("mareas", "sumarían"), levantaria=T("mareas", "levantaría"), todavia=T("mareas", "todavía"),
    costa_m=T("mareas", "costa", frase=6), estable=T("mareas", "estable"), ola_m=T("mareas", "ola"),
    gigante_m=T("mareas", "gigante"), termina=T("mareas", "termina"),
    # ---------------------------------------------------------------- 7. calor (202,9-229,1)
    roca_c=T("calor", "roca"), sube=T("calor", "sube"), baja=T("calor", "baja"), decenas=T("calor", "decenas"),
    cm_c=T("calor", "centímetros"), vaiven=T("calor", "vaivén"), frotaria=T("calor", "frotaría"),
    interior=T("calor", "interior"), parar=T("calor", "parar"),
    friccion=T("calor", "fricción"), calor_w=T("calor", "calor", frase=3), io=T("calor", "Ío"), jupiter=T("calor", "Júpiter"),
    estirada=T("calor", "estirada"), cuatrocientos=T("calor", "cuatrocientos"), volcanes=T("calor", "volcanes", frase=3),
    activos=T("calor", "activos"), tierra_c=T("calor", "Tierra", frase=4), terremotos=T("calor", "terremotos"),
    volcanes2=T("calor", "volcanes", frase=4),
    # ---------------------------------------------------------------- 8. caída (229,1-281,5)
    lunas_c=T("caida", "lunas"), no_quedan=T("caida", "no se"), dejas=T("caida", "dejas"),
    aleja=T("caida", "aleja"), cuatro_c=T("caida", "cuatro"), cm_cc=T("caida", "centímetros"), marea_c=T("caida", "marea"),
    empuja=T("caida", "empuja"), delante_c=T("caida", "delante"),
    reves=T("caida", "revés"), rapido=T("caida", "rápido"), contrario=T("caida", "contrario"), acerca_c=T("caida", "acerca"),
    fobos=T("caida", "Fobos"), marte=T("caida", "Marte"), baja_f=T("caida", "baja"), dos_m=T("caida", "dos metros"),
    siglo=T("caida", "siglo"),
    cerca_c=T("caida", "cerca", frase=4), tiron_c=T("caida", "tirón"), cruzar=T("caida", "cruzar"),
    frontera=T("caida", "frontera"), limite=T("caida", "límite", frase=4), roche=T("caida", "Roche", frase=4),
    dentro=T("caida", "Dentro"), estira_c=T("caida", "estira", frase=5), propia=T("caida", "propia"),
    mantiene=T("caida", "mantiene"), unida=T("caida", "unida"),
    nueve=T("caida", "nueve"), dieciocho=T("caida", "dieciocho"), km_c=T("caida", "kilómetros", frase=6),
    centro=T("caida", "centro"),
    cruzarlo=T("caida", "cruzarlo"), estira7=T("caida", "estira", frase=7), parte=T("caida", "parte"),
    pedazos=T("caida", "pedazos"), reparten=T("caida", "reparten"), anillo_c=T("caida", "anillo"),
    anillos=T("caida", "anillos"), saturno_c=T("caida", "Saturno"), preciosos=T("caida", "preciosos"),
    brillantes=T("caida", "brillantes"), peligrosos=T("caida", "peligrosos"), lloverian=T("caida", "lloverían"),
    rocas=T("caida", "rocas"), sobre_t=T("caida", "Tierra", frase=8),
    # ---------------------------------------------------------------- 9. choque (281,5-331,6)
    otro_final=T("choque", "final"), dos_x=T("choque", "dos", frase=0), choquen=T("choque", "choquen"),
    ya_paso=T("choque", "ya"), pasado=T("choque", "pasado"),
    caras=T("choque", "caras"), vemos=T("choque", "vemos"), lisa=T("choque", "lisa"), mares_x=T("choque", "mares"),
    oculta=T("choque", "oculta", frase=3), montanas=T("choque", "montañas"), crateres=T("choque", "cráteres"),
    corteza=T("choque", "corteza"), gruesa=T("choque", "gruesa"),
    y2011=T("choque", "dos mil"), cientificos=T("choque", "científicos"), segunda_x=T("choque", "segunda"),
    mil_x=T("choque", "mil", frase=4, n=1), doscientos=T("choque", "doscientos"), km_x=T("choque", "kilómetros", frase=4),
    nacio_x=T("choque", "Nació"), choque_g=T("choque", "choque", frase=5), puntos=T("choque", "puntos"),
    equilibrio_x=T("choque", "equilibrio", frase=5),
    pasaron=T("choque", "Pasaron"), millones=T("choque", "millones"), orbita_x=T("choque", "órbita"),
    cambio=T("choque", "cambió"), equilibrio_x2=T("choque", "equilibrio", frase=6), rompio=T("choque", "rompió"),
    chocaron=T("choque", "chocaron"), despacio=T("choque", "despacio"), crater_x=T("choque", "cráter", frase=7),
    aplasto=T("choque", "aplastó"), panqueque=T("choque", "panqueque"), oculta2=T("choque", "oculta", frase=7),
    hipotesis=T("choque", "hipótesis"), encaja=T("choque", "encaja"), vemos2=T("choque", "vemos", frase=8),
    quizas_x=T("choque", "quizás"), dos_lunas_x=T("choque", "dos Lunas", frase=9), pegada=T("choque", "pegada"),
    # ---------------------------------------------------------------- 10. cierre (331,6-350,2)
    hoy_f=T("cierre", "Hoy"), sola_f=T("cierre", "sola"), mejor=T("cierre", "mejor"),
    estable_f=T("cierre", "estable"), mareas_f=T("cierre", "mareas"), noches_f=T("cierre", "noches"),
    estrellas_f=T("cierre", "estrellas"), con_dos=T("cierre", "dos"), estorban_f=T("cierre", "estorban"),
    estrellan=T("cierre", "estrellan"), destrozan=T("cierre", "destrozan"), mira=T("cierre", "mira"),
    luna_f=T("cierre", "Luna", frase=3), unica=T("cierre", "única"), quedo=T("cierre", "quedó"),
)

# escenas del guion (límites)
E_HOY = ESC0("hoy")
E_ORIGEN = ESC0("origen")
E_ORBITA = ESC0("orbita")
E_CIELO = ESC0("cielo")
E_MAREAS = ESC0("mareas")
E_CALOR = ESC0("calor")
E_CAIDA = ESC0("caida")
E_CHOQUE = ESC0("choque")
E_CIERRE = ESC0("cierre")
