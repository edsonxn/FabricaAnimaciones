# -*- coding: utf-8 -*-
"""Guía de estudio en video para la entrevista de Consejeras y Consejeros Distritales y Municipales del IEEZ (PEL 2026-2027).
Video personal del usuario (sin canal, no va a YouTube). ~12 min, 16:9, fichas y diagramas por código (escenas.py).

Técnicas de estudio aplicadas: preguntas de práctica con reloj (recuperación activa: el usuario contesta antes de ver la
respuesta), casos hipotéticos como los que anuncia la guía, mnemotecnias (iniciales, verbos), bloques cortos con título y
barra de avance (fragmentación), palabra clave en pantalla sincronizada con la voz (código dual) y simulacro final
intercalado de todos los temas.

FUENTE ÚNICA: la guía del IEEZ (Descargas/GUIA DE ESTUDIO PAG WEB.pdf, entrevistas del 12 al 30-oct-2026) y el texto
oficial de las leyes que enlaza, descargadas el 21-oct-2026: CPEUM (2-jun-2026) art. 41; Constitución de Zacatecas (8-abr-2026)
art. 38; LGIPE (2-jun-2026) arts. 82, 104, 120-125, 207-208, 217, 225, 273-274, 278, 285, 288-291, 298-299, 304;
Reglamento de Elecciones arts. 186-189; Ley Electoral de Zacatecas (15-feb-2025) arts. 30, 122-129, 254-272;
Ley Orgánica del IEEZ (31-may-2023) arts. 4-6, 10-11, 13, 30-32, 61-71.
Campos propios por escena (los lee escenas.py): "bloque" (n.º de bloque) y "vis" (qué se dibuja).
"""
import json
import os

TITULO = "Guía de estudio: entrevista de Consejos Distritales y Municipales IEEZ 2026-2027"
ARCHIVO = "guia_ieez_entrevista"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 480                        # sin música procedural: solo afina la cuantización de escenas a 0,5 s
FPS = 24                         # fichas: 24 fps bastan y el render sale antes
GAP = 0.32
SUBTITULOS = False
MEZCLA = dict(musica=-30.0, sfx=-26.0, fx=0.0)      # música muy por debajo: es para estudiar; fx = tic-tac y campana (fx_audio.py)
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

BLOQUES = {0: "Cómo te evalúan", 1: "Principios rectores", 2: "INE vs Instituto local", 3: "Atribuciones especiales",
           4: "El IEEZ y sus consejos", 5: "Proceso electoral", 6: "Jornada electoral", 7: "Cómputos",
           8: "Observación electoral", 9: "Competencias STAR", 10: "Simulacro final"}

P_LARGA, P_CORTA = 4.5, 3.0      # segundos de reloj para contestar


def pregunta(id_, bloque, texto, frase, caso=False, pausa=P_LARGA):
    return {"id": id_, "bloque": bloque, "post": pausa + 0.4, "frases": [frase],
            "vis": dict(tipo="pregunta", texto=texto, caso=caso, cuenta=pausa)}


def respuesta(id_, bloque, texto, frases, fuente=""):
    return {"id": id_, "bloque": bloque, "frases": frases, "vis": dict(tipo="respuesta", texto=texto, fuente=fuente)}


ESCENAS = [
    # ------------------------------------------------------------------ 0. cómo te evalúan
    {"id": "intro", "bloque": 0, "pre": 0.6,
     "vis": dict(tipo="portada", titulo="Entrevista IEEZ", sub="Consejos Distritales y Municipales · Proceso Electoral Local 2026-2027"),
     "frases": ["[warmly] Esta es tu guía exprés para la entrevista de consejero distrital o municipal del Instituto Electoral del Estado de Zacatecas."]},
    {"id": "evalua", "bloque": 0,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="Así te califican", items=[
         ["tres", "3 preguntas", "una sola respuesta correcta"],
         ["diez", "10 · 5 · 0", "correcta · regular · incorrecta"],
         ["treinta", "30 % + 10 %", "entrevista + curso de inducción = 40 %"],
         ["cinco", "5 competencias", "método STAR · 20 %"],
         ["entiendas", "Entender · aplicar · argumentar", "no memorizar artículos"],
         ["reloj", "Reloj = contesta en voz alta", "antes de ver la respuesta"]]),
     "frases": [
         "Te harán tres preguntas de conocimientos electorales, cada una con una sola respuesta correcta.",
         "Cada una vale diez si es correcta, cinco si es regular y cero si es incorrecta: treinta por ciento, más diez del curso de inducción.",
         "Y cinco competencias, con el método STAR, valen otro veinte.",
         "No buscan que recites artículos: buscan que entiendas, apliques y argumentes.",
         "Cuando aparezca el reloj, contesta en voz alta antes de ver la respuesta."]},

    # ------------------------------------------------------------------ 1. principios
    {"id": "principios", "bloque": 1,
     "vis": dict(tipo="tarjetas", layout="letras", titulo="Los 6 principios rectores", nota="CPEUM art. 41 · Const. Zacatecas art. 38 · Ley Orgánica IEEZ art. 4",
                 items=[["certeza", "C", "Certeza"], ["legalidad", "L", "Legalidad"], ["independencia", "I", "Independencia"],
                        ["imparcialidad", "I", "Imparcialidad"], ["máxima", "M", "Máxima publicidad"], ["objetividad", "O", "Objetividad"]]),
     "frases": [
         "Bloque uno: los principios rectores, la pregunta de ejemplo de la guía.",
         "Son seis: certeza, legalidad, independencia, imparcialidad, máxima publicidad y objetividad.",
         "Están en el artículo cuarenta y uno constitucional y en el treinta y ocho de la Constitución de Zacatecas.",
         "En un caso práctico, justifica tu decisión con uno de ellos."]},

    # ------------------------------------------------------------------ 2. INE vs Instituto local
    {"id": "quien", "bloque": 2,
     "vis": dict(tipo="tarjetas", layout="tabla", titulo="¿Quién hace qué?", cols=["INE", "IEEZ (organismo local)"],
                 nota="CPEUM art. 41, base V · LGIPE art. 104 · Ley Orgánica IEEZ art. 6",
                 items=[["capacitación", 0, "Capacitación electoral"], ["geografía", 0, "Geografía electoral"],
                        ["padrón", 0, "Padrón y lista de electores"], ["ubicar", 0, "Ubicar casillas y designar funcionarios"],
                        ["fiscalización", 0, "Fiscalización de partidos y candidatos"],
                        ["reglas", 0, "Reglas: PREP, encuestas, observación, conteos rápidos, materiales"],
                        ["prerrogativas", 1, "Prerrogativas de partidos y candidatos"], ["educación", 1, "Educación cívica"],
                        ["preparar", 1, "Preparar la jornada electoral"], ["imprimir", 1, "Imprimir documentos y producir materiales"],
                        ["escrutinios", 1, "Escrutinios, cómputos y constancias"], ["gobernador", 1, "Cómputo de la elección de gobernador"],
                        ["opera", 1, "Opera el PREP local · participación ciudadana"], ["oficialía", 1, "Oficialía electoral (fe pública)"]]),
     "frases": [
         "Bloque dos: quién hace qué. Las elecciones las organizan el INE y el organismo local, el Instituto Electoral de Zacatecas. Distinguirlos es justo lo que van a medir.",
         "Al INE le toca, en federales y locales: capacitación, geografía electoral, padrón y lista de electores, ubicar casillas y designar a sus funcionarios, y la fiscalización de partidos y candidatos.",
         "Y pone las reglas de resultados preliminares, encuestas, observación, conteos rápidos y materiales.",
         "Al Instituto local: prerrogativas de partidos y candidatos, educación cívica, preparar la jornada, e imprimir documentos y materiales.",
         "Además, escrutinios y cómputos, constancias, y el cómputo de gobernador.",
         "Y opera el PREP local, organiza la participación ciudadana y ejerce la oficialía electoral.",
         "Regla de oro: el INE pone las reglas nacionales; el Instituto local las aplica y organiza la elección local."]},
    pregunta("q_obs", 2, "¿A qué autoridad le corresponde acreditar a las y los observadores electorales?",
             "Pregunta de la guía: ¿a qué autoridad le corresponde acreditar a los observadores electorales?"),
    respuesta("a_obs", 2, "Al INE", [
        "Al INE. La solicitud se puede presentar en línea, ante el consejo local o distrital del INE, o ante el Instituto local, desde el inicio del proceso y hasta el treinta de abril del año de la elección."],
        "LGIPE art. 217 · Reglamento de Elecciones arts. 187 y 189"),

    # ------------------------------------------------------------------ 3. atribuciones especiales
    {"id": "especiales", "bloque": 3,
     "vis": dict(tipo="tarjetas", layout="grid3", titulo="Atribuciones especiales del INE", nota="LGIPE arts. 120 a 125 · Ley Electoral de Zacatecas arts. 377 a 380",
                 items=[["Asunción", "ASUNCIÓN", "El INE HACE las actividades del organismo local (total o parcial)"],
                        ["Atracción", "ATRACCIÓN", "El INE RESUELVE un asunto local: por trascendencia o para sentar criterio"],
                        ["Delegación", "DELEGACIÓN", "El INE ENCARGA al organismo local una función suya (excepcional)"],
                        ["ocho", "≥ 8 votos", "del Consejo General del INE"],
                        ["cuatro", "Lo piden", "4 consejeros del INE o la mayoría del consejo local"],
                        ["antes", "Asunción total", "solo antes de que inicie el proceso"]]),
     "frases": [
         "Bloque tres: las atribuciones especiales del INE. Son tres: asunción, atracción y delegación.",
         "Asunción: el INE asume las actividades del organismo local, total o parcialmente.",
         "Atracción: atrae un asunto local, por su trascendencia o para sentar un criterio.",
         "Delegación: le encarga al organismo local una función suya, de forma excepcional.",
         "Todas requieren al menos ocho votos del Consejo General del INE.",
         "Las piden cuatro consejeros del INE o la mayoría del consejo local; la asunción total, solo antes de que inicie el proceso.",
         "Truco: tres verbos. Asumir es hacer, atraer es resolver, delegar es encargar."]},
    pregunta("q_esp", 3, "Mencione una de las 3 atribuciones especiales del INE.",
             "Pregunta de la guía: menciona una de las tres atribuciones especiales del INE."),
    respuesta("a_esp", 3, "Atracción · Asunción · Delegación", [
        "Basta con una: atracción, asunción o delegación. Y si te piden más, explica la diferencia con los tres verbos."],
        "LGIPE art. 120 · respuesta de ejemplo de la guía: «Atracción»"),

    # ------------------------------------------------------------------ 4. el IEEZ y sus consejos
    {"id": "ieez", "bloque": 4,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="El Instituto Electoral del Estado de Zacatecas", nota="Const. Zacatecas art. 38 · Ley Orgánica IEEZ arts. 10 y 11 · Ley Electoral art. 123",
                 items=[["presidente", "Consejo General", "1 presidente + 6 consejeros · 7 años · los designa el INE"],
                        ["tres", "3 órganos electorales", "consejos distritales · consejos municipales · mesas de casilla"],
                        ["solo", "Temporales", "solo funcionan durante el proceso electoral"],
                        ["dieciocho", "18 distritos", "diputados de mayoría relativa"],
                        ["cincuenta", "58 ayuntamientos", "un consejo municipal en cada uno"],
                        ["doce", "12 diputados RP", "una sola circunscripción"]]),
     "frases": [
         "Bloque cuatro: el Instituto. Su Consejo General: un presidente y seis consejeros, designados por el INE por siete años.",
         "Sus tres órganos electorales: consejos distritales, consejos municipales y mesas directivas de casilla. Solo funcionan durante el proceso.",
         "Hay dieciocho distritos, cincuenta y ocho ayuntamientos y doce diputados plurinominales."]},
    {"id": "consejo", "bloque": 4,
     "vis": dict(tipo="tarjetas", layout="mesa", titulo="Tu consejo distrital o municipal", nota="Ley Orgánica IEEZ arts. 61 a 69 · Const. Zacatecas art. 38-VIII",
                 items=[["presidente", "Presidente", "voz y voto"], ["cuatro", "4 consejeros", "voz y voto · con suplentes"],
                        ["secretario", "Secretario", "solo voz"], ["representantes", "Representantes", "partidos e independientes · solo voz"],
                        ["enero", "Distritales", "instalados a más tardar 1.ª semana de enero"],
                        ["febrero", "Municipales", "instalados 1.ª semana de febrero"],
                        ["dos veces", "Sesionan", "al menos 2 veces al mes"],
                        ["mitad", "Quórum", "mitad + 1 con voto, con el presidente"],
                        ["empate", "Empate", "voto de calidad del presidente"]]),
     "frases": [
         "Cada consejo distrital o municipal tiene un consejero presidente, cuatro consejeros electorales con sus suplentes y un secretario ejecutivo.",
         "Los designa el Consejo General por dos terceras partes. Presidente y consejeros: voz y voto. Secretario y representantes: solo voz.",
         "Los distritales se instalan en la primera semana de enero, los municipales en la de febrero, y sesionan al menos dos veces al mes.",
         "Quórum: la mitad más uno con voto, incluido el presidente; si no hay, se sesiona dentro de veinticuatro horas. En empate, voto de calidad del presidente."]},
    {"id": "funciones", "bloque": 4,
     "vis": dict(tipo="tarjetas", layout="tabla", titulo="¿Qué hace cada consejo?", cols=["Consejo distrital", "Consejo municipal"],
                 nota="Ley Orgánica IEEZ arts. 65, 66, 68 y 69",
                 items=[["diputados", 0, "Registra fórmulas de diputados de mayoría relativa"],
                        ["cómputos", 0, "Cómputo de gobernador y de diputados"],
                        ["constancia", 0, "Valida y entrega constancia de diputado MR"],
                        ["planillas", 1, "Registra planillas de ayuntamiento"],
                        ["municipal", 1, "Cómputo municipal y validez"],
                        ["recuento", 0, "Califica y realiza recuentos"], ["recuento", 1, "Califica y realiza recuentos"],
                        ["oficialía", 0, "Secretario: oficialía electoral"], ["oficialía", 1, "Secretario: oficialía electoral"]]),
     "frases": [
         "El distrital registra a los diputados de mayoría, hace los cómputos de gobernador y diputados, y entrega su constancia.",
         "El municipal registra las planillas de ayuntamiento y hace el cómputo municipal.",
         "Ambos califican los recuentos, y su secretario ejerce la oficialía electoral: la fe pública."]},
    pregunta("q_cons", 4, "Caso: el presidente del consejo no llega a la sesión, pero están los 4 consejeros electorales. ¿Qué hacen?",
             "Caso práctico: el presidente del consejo no llega a la sesión, pero sí los cuatro consejeros electorales. ¿Qué hacen?", caso=True),
    respuesta("a_cons", 4, "Designan entre ellos, por mayoría simple, a quien presida esa sesión", [
        "Los consejeros, por mayoría simple, designan entre ellos a quien presida esa sesión.",
        "Si el que falta es el secretario, igual: un consejero lo suple, y no pierde su voto."],
        "Ley Orgánica IEEZ art. 62"),

    # ------------------------------------------------------------------ 5. proceso electoral
    {"id": "proceso", "bloque": 5,
     "vis": dict(tipo="tarjetas", layout="linea", titulo="Proceso electoral: 4 etapas", nota="Ley Electoral de Zacatecas arts. 122 a 129 · LGIPE arts. 207, 208 y 225",
                 items=[["preparación", "1 · Preparación", "20 de noviembre del año previo → inicio de la jornada"],
                        ["dos,", "2 · Jornada", "8:00 h del 1.er domingo de junio → clausura de casilla"],
                        ["resultados", "3 · Resultados y validez", "llegada de paquetes → cómputos y declaraciones"],
                        ["dictamen", "4 · Dictamen gobernador", "Tribunal de Justicia Electoral: cómputo final y gobernador electo"]]),
     "frases": [
         "Bloque cinco: el proceso electoral. En Zacatecas inicia el veinte de noviembre del año previo a la elección, con sesión del Consejo General.",
         "Tiene cuatro etapas. Uno, preparación de la elección; dos, jornada electoral; tres, resultados y declaraciones de validez; y cuatro, dictamen y declaración de validez de la elección de gobernador.",
         "La preparación dura hasta que inicia la jornada. La jornada empieza a las ocho de la mañana del primer domingo de junio y termina con la clausura de la casilla.",
         "Los resultados van de la llegada de paquetes a los consejos hasta los cómputos. Y la última etapa es del Tribunal de Justicia Electoral: gobernador electo.",
         "Recuérdalo así: preparo, voto, cuento y califico."]},
    pregunta("q_etapas", 5, "¿Cuáles son las etapas del proceso electoral? ¿Cuándo empieza y termina la jornada?",
             "Pregunta: ¿cuáles son las etapas del proceso electoral, y cuándo empieza y termina la jornada?"),
    respuesta("a_etapas", 5, "Preparación · Jornada · Resultados y validez · Dictamen de gobernador", [
        "Preparación, jornada, resultados y declaraciones de validez, y dictamen de gobernador.",
        "La jornada empieza a las ocho de la mañana del primer domingo de junio y termina con la clausura de la casilla."],
        "Ley Electoral de Zacatecas arts. 125 y 127"),

    # ------------------------------------------------------------------ 6. jornada electoral
    {"id": "jornada", "bloque": 6,
     "vis": dict(tipo="tarjetas", layout="reloj", titulo="La jornada, hora por hora", nota="LGIPE arts. 273, 274 y 285",
                 items=[["siete", "7:30", "llegan los funcionarios a instalar"],
                        ["ocho en punto", "8:00", "inicia la votación, nunca antes"],
                        ["ocho y cuarto", "8:15", "si no se instaló: se corre el orden"],
                        ["diez", "10:00", "sin apoyo por distancia: designan los representantes"],
                        ["seis de la tarde", "18:00", "cierra la votación"]]),
     "frases": [
         "Bloque seis: la jornada electoral, hora por hora.",
         "Siete y media: llegan los funcionarios a instalar la casilla, frente a los representantes.",
         "Ocho en punto: empieza a recibirse la votación, nunca antes.",
         "Ocho y cuarto: si no se ha instalado, se corre el orden. El presidente completa la mesa con propietarios, suplentes y, si faltan, electores de la fila.",
         "Si no está el presidente, asume el secretario; si tampoco, un escrutador; y si solo hay suplentes, uno de ellos preside.",
         "Si no llega nadie, actúa el consejo distrital. Y a las diez, si la distancia lo impidió, los representantes designan funcionarios entre los electores.",
         "Ojo: nunca se nombra funcionario a un representante de partido.",
         "Seis de la tarde: cierra la votación, salvo que haya gente formada; antes, solo si ya votó toda la lista."]},
    {"id": "casilla", "bloque": 6,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="Mesa directiva y escrutinio", nota="LGIPE arts. 82, 288, 290, 291 y 299 · Ley Orgánica IEEZ art. 70",
                 items=[["presidente", "Mesa directiva", "presidente · secretario · 2 escrutadores · suplentes"],
                        ["coincide", "Casilla única", "elección concurrente: + 1 secretario y + 1 escrutador"],
                        ["sobrantes", "Secretario", "cuenta sobrantes y las cruza con 2 rayas"],
                        ["primer escrutador", "1.er escrutador", "cuenta 2 veces quiénes votaron"],
                        ["urna", "Presidente → 2.º escrutador", "abre la urna · cuenta las boletas"],
                        ["nulo", "Voto nulo", "sin marca · o 2+ cuadros sin coalición"]]),
     "frases": [
         "La mesa: presidente, secretario, dos escrutadores y suplentes. Si la elección coincide con la federal, como en dos mil veintisiete, hay casilla única, con un secretario y un escrutador extra.",
         "En el escrutinio, el secretario cuenta las boletas sobrantes y las cruza con dos rayas.",
         "El primer escrutador cuenta dos veces a quienes votaron según la lista nominal.",
         "El presidente abre la urna, el segundo escrutador cuenta las boletas, y ambos las clasifican.",
         "Voto nulo: la boleta sin marcar, o marcada en dos o más cuadros sin coalición entre esos partidos."]},
    {"id": "paquete", "bloque": 6,
     "vis": dict(tipo="tarjetas", layout="grid3", titulo="Entrega del paquete al consejo", nota="LGIPE art. 299",
                 items=[["inmedia", "Inmediato", "casilla en la cabecera"], ["doce", "Hasta 12 h", "urbana fuera de la cabecera"],
                        ["veinticuatro", "Hasta 24 h", "casilla rural"]]),
     "frases": [
         "Entrega del paquete: inmediata en la cabecera, hasta doce horas si es urbana, y hasta veinticuatro si es rural."]},
    pregunta("q_ocho", 6, "Caso: son las 8:15, no llegó la presidenta de la casilla, pero sí el secretario. ¿Qué pasa?",
             "Caso práctico: son las ocho y cuarto, no ha llegado la presidenta de la casilla, pero sí el secretario. ¿Qué pasa?", caso=True),
    respuesta("a_ocho", 6, "El secretario asume la presidencia e integra la mesa", [
        "El secretario asume la presidencia y completa la mesa: primero recorre a los propietarios presentes, luego habilita a los suplentes y, si faltan, nombra a electores de la fila de esa sección."],
        "LGIPE art. 274"),

    # ------------------------------------------------------------------ 7. cómputos
    {"id": "recepcion", "bloque": 7,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="Llegan los paquetes al consejo", nota="Ley Electoral de Zacatecas arts. 254 a 256 · LGIPE art. 304",
                 items=[["orden", "Recibo", "en el orden en que llegan, con día y hora"],
                        ["numérico", "Bodega", "orden numérico · especiales aparte · puertas selladas"],
                        ["custodia", "Presidente", "responde por su custodia"],
                        ["acta", "Secretario", "acta circunstanciada de todo"],
                        ["preliminares", "Resultados preliminares", "lectura en voz alta y se fijan afuera"],
                        ["informativo", "PREP", "solo informativo, no definitivo"]]),
     "frases": [
         "Bloque siete, lo que más te toca como consejero: recibir paquetes y hacer los cómputos.",
         "Se reciben en el orden en que llegan, con recibo de día y hora, y se guardan en orden numérico en una bodega sellada frente a los representantes.",
         "El presidente responde por su custodia, y el secretario levanta acta circunstanciada de todo.",
         "Se suman resultados preliminares y se fijan afuera. El PREP es solo informativo, no definitivo."]},
    {"id": "computo", "bloque": 7,
     "vis": dict(tipo="tarjetas", layout="linea", titulo="Calendario de cómputos", nota="Ley Electoral de Zacatecas arts. 258, 259, 265 y 271",
                 items=[["elección", "Domingo", "jornada electoral"],
                        ["miércoles", "Miércoles 9:00", "cómputos distritales y municipales · sesión ininterrumpida"],
                        ["gobernador", "Distrital", "1.º gobernador · 2.º diputados"],
                        ["ayuntamiento", "Municipal", "1.º mayoría relativa · 2.º regidores RP"],
                        ["domingo siguiente", "Domingo siguiente", "Consejo General: cómputos estatales"]]),
     "frases": [
         "Los cómputos distritales y municipales empiezan a las nueve de la mañana del miércoles siguiente a la elección, en sesión ininterrumpida.",
         "El distrital: primero gobernador, luego diputados. El municipal: primero el ayuntamiento de mayoría relativa, luego regidores plurinominales.",
         "Y el domingo siguiente a la jornada, el Consejo General hace los cómputos estatales."]},
    {"id": "recuento", "bloque": 7,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="¿Cuándo se vuelve a contar?", nota="Ley Electoral de Zacatecas art. 259",
                 items=[["falta", "Por casilla", "falta el acta · no coincide · errores evidentes"],
                        ["nulos", "Por casilla", "nulos > diferencia entre 1.º y 2.º · todos los votos a uno"],
                        ["punto porcentual", "Recuento total", "diferencia ≤ 1 % + petición expresa del 2.º lugar"],
                        ["grupos", "Grupos de trabajo", "presididos por consejeros · antes del domingo siguiente"],
                        ["tribunal", "Definitivo", "lo recontado no se recuenta en el tribunal"],
                        ["constancia", "Al final", "validez · constancia de mayoría · cédula afuera"]]),
     "frases": [
         "Una casilla se recuenta si falta el acta, si no coincide con la del presidente o si hay errores evidentes.",
         "También si los votos nulos superan la diferencia entre primero y segundo lugar, o si todos los votos fueron para un solo partido.",
         "Recuento total: si la diferencia entre primero y segundo lugar es de un punto porcentual o menos, y el representante del segundo lugar lo pide expresamente.",
         "Se hace en grupos de trabajo presididos por consejeros, y debe terminar antes del domingo siguiente.",
         "Lo que se recontó en el consejo ya no se puede recontar en el tribunal.",
         "Al final: declaración de validez, constancia de mayoría, y cédula de resultados afuera."]},
    pregunta("q_recuento", 7, "Caso: el 1.er lugar gana por 0.8 % y, al iniciar la sesión, el representante del 2.º lugar pide recuento. ¿Qué procede?",
             "Caso práctico: en tu distrito el primer lugar gana por cero punto ocho por ciento, y al iniciar la sesión el representante del segundo lugar pide recuento. ¿Qué procede?", caso=True),
    respuesta("a_recuento", 7, "Recuento total de votos en todas las casillas", [
        "Recuento total en todas las casillas: la diferencia es de un punto o menos y hay petición expresa.",
        "Se forman grupos de trabajo presididos por consejeros, y debe concluir antes del domingo siguiente."],
        "Ley Electoral de Zacatecas art. 259, numerales 3 a 5"),

    # ------------------------------------------------------------------ 8. observación
    {"id": "observa", "bloque": 8,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="Observadoras y observadores", nota="LGIPE art. 217 · Reglamento de Elecciones arts. 186 a 189",
                 items=[["acredita", "Acredita el INE", "el Instituto local garantiza el derecho"],
                        ["tres años", "Requisitos", "sin dirigencia ni candidatura en 3 años · curso"],
                        ["instalación", "Pueden observar", "instalación · votación · escrutinio · clausura"],
                        ["nunca", "Nunca", "declarar triunfos · hacer proselitismo · sustituir autoridades"]]),
     "frases": [
         "Bloque ocho, observación electoral. La acreditación la da el INE, y el Instituto local garantiza ese derecho en el estado.",
         "Requisitos: sin dirigencia partidista ni candidatura en los tres años anteriores, y tomar el curso.",
         "Observan la instalación, la votación, el escrutinio y la clausura, pero nunca declaran triunfos ni hacen proselitismo."]},

    # ------------------------------------------------------------------ 9. STAR
    {"id": "star", "bloque": 9,
     "vis": dict(tipo="tarjetas", layout="letras", titulo="Competencias: método STAR", nota="Guía IEEZ, factor 2 (20 %)",
                 items=[["Situación", "S", "Situación: qué pasaba"], ["Tarea", "T", "Tarea: qué te tocaba"],
                        ["Acción", "A", "Acción: qué hiciste TÚ"], ["Resultado", "R", "Resultado: cómo terminó (con un dato)"]]),
     "frases": [
         "Bloque nueve: competencias. Te preguntarán por tu formación, tus trabajos y cómo has actuado.",
         "Responde con el método STAR. Situación: qué pasaba. Tarea: qué te tocaba. Acción: qué hiciste tú. Resultado: cómo terminó, con un dato si puedes."]},
    {"id": "competencias", "bloque": 9,
     "vis": dict(tipo="tarjetas", layout="grid", titulo="Una historia real para cada una", nota="Escala: excelente 10 · bueno 5 · regular 3",
                 items=[["liderazgo", "1 · Liderazgo", "profesionalismo e integridad"], ["negociación", "2 · Negociación", "y comunicación"],
                        ["equipo", "3 · Trabajo en equipo", "y bajo presión"], ["imparcialidad", "4 · Imparcialidad", "trato igual a todos"],
                        ["independencia", "5 · Independencia", "decidir sin presiones"], ["primera", "Yo hice · yo decidí", "primera persona, en pasado"]]),
     "frases": [
         "Las cinco son: liderazgo, profesionalismo e integridad; negociación y comunicación; trabajo en equipo y bajo presión; imparcialidad; e independencia.",
         "Lleva una historia real para cada una; para imparcialidad e independencia, una en la que seguiste las reglas aunque te presionaran.",
         "Lo que hiciste antes predice lo que harás: habla en primera persona y en pasado. Yo hice, yo decidí."]},

    # ------------------------------------------------------------------ 10. simulacro
    {"id": "simulacro", "bloque": 10,
     "vis": dict(tipo="portada", titulo="Simulacro final", sub="10 preguntas rápidas · contesta antes de que acabe el reloj"),
     "frases": ["Simulacro final: diez preguntas rápidas de todos los temas. Contesta antes de que se acabe el reloj."]},
]

SIMULACRO = [
    ("¿Cuántos consejeros electorales tiene un consejo municipal, además del presidente?",
     "Uno: ¿cuántos consejeros electorales tiene un consejo municipal, además del presidente?",
     "Cuatro, con sus suplentes", "Cuatro, con sus suplentes."),
    ("¿A qué hora empiezan los cómputos distritales y municipales?",
     "Dos: ¿a qué hora empiezan los cómputos distritales y municipales?",
     "9:00 h del miércoles siguiente a la elección", "A las nueve de la mañana del miércoles siguiente a la elección."),
    ("¿Quién designa a los consejeros distritales y municipales?",
     "Tres: ¿quién designa a los consejeros distritales y municipales?",
     "El Consejo General del IEEZ, por 2/3", "El Consejo General del Instituto Electoral, por dos terceras partes."),
    ("¿Cuándo inicia el proceso electoral local en Zacatecas?",
     "Cuatro: ¿cuándo inicia el proceso electoral local en Zacatecas?",
     "El 20 de noviembre del año previo", "El veinte de noviembre del año previo a la elección."),
    ("¿A qué hora cierra la votación?", "Cinco: ¿a qué hora cierra la votación?",
     "18:00 h, salvo electores formados", "A las seis de la tarde, salvo que haya electores formados."),
    ("¿Quién ubica las casillas y designa a sus funcionarios?", "Seis: ¿quién ubica las casillas y designa a sus funcionarios?",
     "El INE (salvo delegación)", "El INE, salvo que lo delegue."),
    ("¿Plazo para entregar el paquete de una casilla rural?", "Siete: ¿qué plazo hay para entregar el paquete de una casilla rural?",
     "Hasta 24 horas después de la clausura", "Hasta veinticuatro horas después de la clausura."),
    ("¿Quién ejerce la oficialía electoral en un consejo distrital?", "Ocho: ¿quién ejerce la oficialía electoral en un consejo distrital?",
     "El secretario del consejo", "El secretario del consejo."),
    ("¿Cuántos votos necesita el INE para atraer un asunto local?", "Nueve: ¿cuántos votos necesita el INE para atraer un asunto local?",
     "Al menos 8 de su Consejo General", "Al menos ocho votos de su Consejo General."),
    ("¿Qué principio aplicas al tratar igual a todos los partidos?", "Diez: ¿qué principio aplicas al tratar igual a todos los partidos?",
     "Imparcialidad", "Imparcialidad."),
]
for _k, (_q, _qv, _r, _rv) in enumerate(SIMULACRO, 1):
    _e = pregunta(f"s{_k}q", 10, _q, _qv, pausa=P_CORTA)
    _e["vis"]["num"] = _k
    ESCENAS.append(_e)
    ESCENAS.append(respuesta(f"s{_k}a", 10, _r, [_rv]))

ESCENAS.append({"id": "cierre", "bloque": 10, "post": 2.5,
                "vis": dict(tipo="portada", titulo="¡Mucho éxito!", sub="Responde · cita la ley · da un ejemplo"),
                "frases": ["Último consejo: di la respuesta y, si la sabes, la ley que la sostiene. Eso demuestra que entiendes, que es lo que buscan.",
                           "[warmly] Respira, habla claro y con ejemplos. Mucho éxito en tu entrevista."]})

TRANSICIONES = [("continua", 0.4)] * (len(ESCENAS) - 1)      # plano continuo: los cambios los dibuja escenas.py


def _tramos():
    """Agrupa escenas seguidas en tramos de música de <= 165 s (con los tiempos reales si ya hay timeline.json)."""
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timeline.json")
    durs = {}
    if os.path.exists(ruta):
        for e in json.load(open(ruta, encoding="utf-8"))["escenas"]:
            durs[e["id"]] = e["t1"] - e["t0"]
    grupos, actual, acum = [], [], 0.0
    for e in ESCENAS:
        d = durs.get(e["id"], 4.0 + 5.5 * len(e["frases"]))
        if actual and acum + d > 165.0:
            grupos.append(actual)
            actual, acum = [], 0.0
        actual.append(e["id"])
        acum += d
    grupos.append(actual)
    notas = ["Begin softly from silence, calm and focused."] + ["Continue the same calm focused groove."] * (len(grupos) - 2) \
        + ["Continue, then resolve warmly to a clean ending."]
    return [(g, notas[i] if len(grupos) > 1 else "Begin softly and end cleanly.") for i, g in enumerate(grupos)]


LYRIA = dict(
    estilo="Calm lo-fi study music: soft felt piano, warm electric piano chords, gentle brushed drums, mellow bass, "
           "steady and unobtrusive, focused and encouraging, 80 BPM, instrumental only, no vocals.",
    escenas={},
    tramos=_tramos())

# Whisper escribe los números con cifras («0.8 %», «4. Con sus suplentes»): no es error de la voz (revisado el 21-oct-2026)
CER_MAX_POR_FRASE = {k: 0.35 for k in ["q_recuento_0", "s1a_0"] + [f"s{n}q_0" for n in range(1, 11)]}
