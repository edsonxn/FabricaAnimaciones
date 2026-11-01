# -*- coding: utf-8 -*-
"""Cuestionario exprés de 50 preguntas para la entrevista de Consejos Distritales y Municipales del IEEZ (PEL 2026-2027).
Video personal del usuario (sin canal, no va a YouTube). Segunda parte de `videos/guia_ieez/` (misma fuente, mismas escenas).
Formato: pregunta → reloj con tic-tac (contestar en voz alta) → respuesta con campana y fundamento. 7 temas con portadilla.

FUENTE ÚNICA: texto oficial de las leyes que enlaza la guía del IEEZ, descargadas el 21-oct-2026: CPEUM (2-jun-2026) art. 41;
Constitución de Zacatecas (8-abr-2026) art. 38; LGIPE (2-jun-2026) arts. 120-125, 217, 273-274, 285, 288-291, 299;
Reglamento de Elecciones arts. 187 y 189; Ley Electoral de Zacatecas (15-feb-2025) arts. 30, 123-129, 254-271;
Ley Orgánica del IEEZ (31-may-2023) arts. 4, 6, 10, 11, 61-69.
"""
import json
import os

TITULO = "Cuestionario de 50 preguntas: entrevista de Consejos Distritales y Municipales IEEZ 2026-2027"
ARCHIVO = "guia_ieez_50_preguntas"
ESTILO_VISUAL = "documental"
DURACION = None
BPM = 480                        # sin música procedural: solo afina la cuantización de escenas a 0,5 s
FPS = 24
GAP = 0.32
SUBTITULOS = False
MEZCLA = dict(musica=-30.0, sfx=-26.0, fx=0.0)      # fx = tic-tac y campana (fx_audio.py)
VOZ = dict(motor="elevenlabs", voice_id="sKgg4MPUDBy69X7iv3fA", modelo="eleven_v4", idioma="es", tomas=1, stability=0.5)

BLOQUES = {0: "50 preguntas", 1: "Principios e instituciones", 2: "Tu consejo", 3: "INE y atribuciones especiales",
           4: "Proceso electoral", 5: "Jornada electoral", 6: "Cómputos y recuentos", 7: "Observación y resultados"}
PAUSA = 4.0                      # segundos de reloj para contestar
TOTAL_P = 50
_U = ["", "uno", "dos", "tres", "cuatro", "cinco", "seis", "siete", "ocho", "nueve", "diez", "once", "doce", "trece", "catorce",
      "quince", "dieciséis", "diecisiete", "dieciocho", "diecinueve", "veinte", "veintiuno", "veintidós", "veintitrés",
      "veinticuatro", "veinticinco", "veintiséis", "veintisiete", "veintiocho", "veintinueve"]
_D = {3: "treinta", 4: "cuarenta", 5: "cincuenta"}


def palabra(n):
    if n < 30:
        return _U[n]
    d, u = divmod(n, 10)
    return _D[d] + (" y " + _U[u] if u else "")

# (tema, texto en pantalla, pregunta dicha, respuesta en pantalla, respuesta dicha, fundamento)
P = [
    (1, "¿Cuáles son los principios rectores de la función electoral?", "¿Cuáles son los principios rectores de la función electoral?",
     "Certeza · legalidad · independencia · imparcialidad · máxima publicidad · objetividad",
     "Certeza, legalidad, independencia, imparcialidad, máxima publicidad y objetividad.", "CPEUM art. 41 · Const. Zacatecas art. 38"),
    (1, "¿Qué es el Instituto Electoral del Estado de Zacatecas?", "¿Qué es el Instituto Electoral del Estado de Zacatecas?",
     "El organismo público local electoral: permanente, con personalidad jurídica y patrimonio propios",
     "Es el organismo público local electoral, permanente, con personalidad jurídica y patrimonio propios, autónomo e independiente.", "Ley Orgánica IEEZ art. 4"),
    (1, "¿A quiénes corresponde organizar las elecciones?", "¿A quiénes corresponde organizar las elecciones?",
     "Al INE y a los organismos públicos locales", "Es una función del Estado que realizan el INE y los organismos públicos locales.", "CPEUM art. 41, base V"),
    (1, "¿Cómo se integra el Consejo General del IEEZ?", "¿Cómo se integra el Consejo General del Instituto Electoral de Zacatecas?",
     "1 consejero presidente + 6 consejeros electorales", "Un consejero presidente y seis consejeros electorales, con voz y voto.", "Const. Zacatecas art. 38-III"),
    (1, "¿Cuánto duran y quién designa a los consejeros del Consejo General del IEEZ?", "¿Cuánto duran y quién designa a los consejeros del Consejo General del Instituto?",
     "7 años, sin reelección · los designa el Consejo General del INE", "Siete años, sin reelección, y los designa el Consejo General del INE.", "Const. Zacatecas art. 38-III y IV"),
    (1, "¿Cuáles son los órganos electorales del IEEZ?", "¿Cuáles son los órganos electorales del Instituto?",
     "Consejos distritales · consejos municipales · mesas directivas de casilla", "Los consejos distritales, los consejos municipales y las mesas directivas de casilla.", "Ley Orgánica IEEZ art. 10"),
    (1, "¿Cuándo funcionan esos órganos electorales?", "¿Cuándo funcionan esos órganos electorales?",
     "Solo durante el proceso electoral", "Únicamente durante el proceso electoral.", "Ley Orgánica IEEZ art. 11"),

    (2, "¿Cómo se integra un consejo distrital o municipal?", "¿Cómo se integra un consejo distrital o municipal?",
     "Presidente · secretario ejecutivo · 4 consejeros electorales con suplentes", "Un consejero presidente, un secretario ejecutivo y cuatro consejeros electorales con sus suplentes.", "Ley Orgánica IEEZ art. 61"),
    (2, "¿Quién designa a sus integrantes y con qué votación?", "¿Quién designa a sus integrantes, y con qué votación?",
     "El Consejo General del IEEZ, por 2/3", "El Consejo General del Instituto, por el voto de las dos terceras partes.", "Ley Orgánica IEEZ art. 61"),
    (2, "En el consejo, ¿quiénes tienen solo voz?", "En el consejo, ¿quiénes tienen solo voz, sin voto?",
     "El secretario y los representantes de partidos e independientes", "El secretario y los representantes de partidos y candidaturas independientes.", "Ley Orgánica IEEZ art. 61"),
    (2, "¿Cuándo se instalan los consejos distritales?", "¿Cuándo se instalan los consejos distritales?",
     "A más tardar en la 1.ª semana de enero del año de la elección", "A más tardar en la primera semana de enero del año de la elección.", "Ley Orgánica IEEZ art. 64"),
    (2, "¿Cuándo se instalan los consejos municipales?", "¿Y cuándo se instalan los consejos municipales?",
     "En la 1.ª semana de febrero del año de la elección", "En la primera semana de febrero del año de la elección.", "Ley Orgánica IEEZ art. 67"),
    (2, "¿Con qué frecuencia sesionan los consejos distritales y municipales?", "¿Con qué frecuencia sesionan los consejos distritales y municipales?",
     "Al menos 2 veces al mes", "Por lo menos dos veces al mes.", "Ley Orgánica IEEZ arts. 64 y 67"),
    (2, "¿Qué quórum necesita el consejo para sesionar?", "¿Qué quórum necesita el consejo para sesionar?",
     "Mitad + 1 de quienes tienen voto, incluido el presidente", "La mitad más uno de sus integrantes con voto, entre ellos el presidente.", "Ley Orgánica IEEZ art. 62"),
    (2, "Si no hay quórum, ¿qué pasa?", "Si no hay quórum, ¿qué pasa?",
     "Se sesiona dentro de las 24 horas siguientes", "La sesión se realiza dentro de las veinticuatro horas siguientes, con quienes asistan.", "Ley Orgánica IEEZ art. 62"),
    (2, "¿Qué pasa si hay empate en una votación del consejo?", "¿Qué pasa si hay empate en una votación del consejo?",
     "El presidente tiene voto de calidad", "El presidente del consejo tiene voto de calidad.", "Ley Orgánica IEEZ art. 62"),
    (2, "Si falta el presidente a la sesión, ¿qué hacen los consejeros?", "Si falta el presidente a la sesión, ¿qué hacen los consejeros?",
     "Designan entre ellos, por mayoría simple, a quien presida", "Por mayoría simple designan entre ellos a quien presida esa sesión.", "Ley Orgánica IEEZ art. 62"),
    (2, "¿Quién ejerce la oficialía electoral en el consejo?", "¿Quién ejerce la oficialía electoral en el consejo?",
     "El secretario del consejo (puede delegarla por escrito)", "El secretario del consejo, que puede delegarla por escrito para cada caso.", "Ley Orgánica IEEZ arts. 66 y 69"),
    (2, "¿Qué cómputos realiza el consejo distrital?", "¿Qué cómputos realiza el consejo distrital?",
     "Gobernador y diputados por ambos principios", "Los de gobernador y de diputados por ambos principios.", "Ley Orgánica IEEZ art. 65"),
    (2, "¿Qué registros recibe el consejo municipal?", "¿Qué registros recibe el consejo municipal?",
     "Planillas de ayuntamiento por mayoría relativa", "Las planillas de candidatos a integrar el ayuntamiento por mayoría relativa.", "Ley Orgánica IEEZ art. 68"),

    (3, "¿A quién corresponde la capacitación electoral y designar funcionarios de casilla?", "¿A quién corresponde la capacitación electoral y designar a los funcionarios de casilla?",
     "Al INE (también en elecciones locales)", "Al INE, en elecciones federales y locales.", "CPEUM art. 41, base V, apartado B"),
    (3, "¿Quién fiscaliza los recursos de partidos y candidatos?", "¿Quién fiscaliza los recursos de partidos y candidatos?",
     "El Consejo General del INE", "El Consejo General del INE.", "CPEUM art. 41, base V, apartado B"),
    (3, "En la elección local, ¿quién imprime las boletas y produce los materiales?", "En la elección local, ¿quién imprime las boletas y produce los materiales?",
     "El IEEZ, con los lineamientos del INE", "El Instituto local, con los lineamientos que emite el INE.", "LGIPE art. 104 · Ley Orgánica IEEZ art. 6"),
    (3, "¿Qué es la atracción?", "¿Qué es la facultad de atracción?",
     "El INE atrae un asunto local por su trascendencia o para sentar criterio", "El INE atrae un asunto local, por su trascendencia o para sentar un criterio de interpretación.", "LGIPE art. 120"),
    (3, "¿Qué es la asunción?", "¿Qué es la asunción?",
     "El INE asume las actividades del organismo local: total o parcial", "El INE asume directamente las actividades del organismo local, de forma total o parcial.", "LGIPE arts. 120 y 123"),
    (3, "¿Qué es la delegación?", "¿Qué es la delegación?",
     "El INE delega en el organismo local una función propia (excepcional)", "El INE delega en el organismo local una función suya, de forma excepcional y antes de iniciar el proceso.", "LGIPE art. 125"),
    (3, "¿Cuántos votos del Consejo General del INE requieren esas atribuciones?", "¿Cuántos votos del Consejo General del INE requieren esas atribuciones?",
     "Al menos 8 votos", "Al menos ocho votos.", "LGIPE arts. 121, 124 y 125"),
    (3, "¿Hasta cuándo puede pedirse la asunción total de una elección local?", "¿Hasta cuándo puede pedirse la asunción total de una elección local?",
     "Antes de que inicie el proceso electoral", "Solo antes de que inicie el proceso electoral local.", "LGIPE art. 121"),

    (4, "¿Cuándo inicia el proceso electoral local en Zacatecas?", "¿Cuándo inicia el proceso electoral local en Zacatecas?",
     "El 20 de noviembre del año previo a la elección", "El veinte de noviembre del año previo a la elección.", "Ley Electoral de Zacatecas art. 124"),
    (4, "¿Cuáles son las etapas del proceso electoral?", "¿Cuáles son las etapas del proceso electoral?",
     "Preparación · jornada · resultados y validez · dictamen de gobernador", "Preparación, jornada electoral, resultados y declaraciones de validez, y dictamen de gobernador.", "Ley Electoral de Zacatecas art. 125"),
    (4, "¿Cuándo empieza y cuándo termina la jornada electoral?", "¿Cuándo empieza y cuándo termina la jornada electoral?",
     "8:00 h del 1.er domingo de junio → clausura de la casilla", "Empieza a las ocho de la mañana del primer domingo de junio y termina con la clausura de la casilla.", "Ley Electoral de Zacatecas art. 127"),
    (4, "¿Cuándo inicia la etapa de resultados y declaraciones de validez?", "¿Cuándo inicia la etapa de resultados y declaraciones de validez?",
     "Con la remisión de los paquetes a los consejos distritales y municipales", "Con la remisión de la documentación y expedientes electorales a los consejos distritales y municipales.", "Ley Electoral de Zacatecas art. 128"),
    (4, "¿Quién declara al gobernador electo?", "¿Quién declara al gobernador electo?",
     "El Tribunal de Justicia Electoral del Estado", "El Tribunal de Justicia Electoral del Estado.", "Ley Electoral de Zacatecas art. 129"),
    (4, "¿Cada cuánto se elige a diputados, ayuntamientos y gobernador?", "¿Cada cuánto se elige a diputados, ayuntamientos y gobernador?",
     "Diputados y ayuntamientos: 3 años · gobernador: 6 años", "Diputados y ayuntamientos cada tres años; gobernador, cada seis.", "Ley Electoral de Zacatecas art. 30"),
    (4, "¿Cuántos diputados y ayuntamientos se eligen en Zacatecas?", "¿Cuántos diputados y ayuntamientos se eligen en Zacatecas?",
     "18 de mayoría + 12 plurinominales · 58 ayuntamientos", "Dieciocho diputados de mayoría, doce plurinominales y cincuenta y ocho ayuntamientos.", "Ley Electoral de Zacatecas art. 123"),

    (5, "¿A qué hora se presentan los funcionarios a instalar la casilla?", "¿A qué hora se presentan los funcionarios a instalar la casilla?",
     "A las 7:30 h", "A las siete y media de la mañana.", "LGIPE art. 273"),
    (5, "8:15 h: no llegó la presidenta, pero sí el secretario. ¿Qué pasa?", "Son las ocho y cuarto, no llegó la presidenta pero sí el secretario. ¿Qué pasa?",
     "El secretario asume la presidencia e integra la mesa", "El secretario asume la presidencia e integra la mesa con propietarios, suplentes y, si faltan, electores de la fila.", "LGIPE art. 274"),
    (5, "¿Se puede nombrar funcionario de casilla a un representante de partido?", "¿Se puede nombrar funcionario de casilla a un representante de partido?",
     "No, en ningún caso", "No, en ningún caso.", "LGIPE art. 274"),
    (5, "¿A qué hora cierra la votación y cuándo puede ser distinto?", "¿A qué hora cierra la votación, y cuándo puede ser distinto?",
     "18:00 h · después solo si hay electores formados · antes si votó toda la lista", "A las seis de la tarde. Después, solo si hay electores formados; antes, solo si ya votó toda la lista nominal.", "LGIPE art. 285"),
    (5, "¿Cuándo es nulo un voto?", "¿Cuándo es nulo un voto?",
     "Boleta sin marcar · o 2 o más cuadros marcados sin coalición", "Cuando la boleta no tiene marca, o tiene dos o más cuadros marcados sin coalición entre esos partidos.", "LGIPE art. 288"),
    (5, "¿Quién cuenta las boletas sobrantes y cómo las inutiliza?", "¿Quién cuenta las boletas sobrantes, y cómo las inutiliza?",
     "El secretario · con 2 rayas diagonales", "El secretario de la mesa, con dos rayas diagonales de tinta.", "LGIPE art. 290"),
    (5, "¿Plazos para entregar el paquete electoral al consejo?", "¿Qué plazos hay para entregar el paquete electoral al consejo?",
     "Inmediato en la cabecera · 12 h urbana · 24 h rural", "Inmediato en la cabecera, hasta doce horas si es urbana y hasta veinticuatro si es rural.", "LGIPE art. 299"),

    (6, "¿Cuándo empiezan los cómputos distritales y municipales?", "¿Cuándo empiezan los cómputos distritales y municipales?",
     "Miércoles siguiente a la elección, 9:00 h", "A las nueve de la mañana del miércoles siguiente a la elección.", "Ley Electoral de Zacatecas arts. 258 y 265"),
    (6, "¿En qué orden se hacen los cómputos en el consejo distrital?", "¿En qué orden se hacen los cómputos en el consejo distrital?",
     "1.º gobernador · 2.º diputados", "Primero gobernador y después diputados.", "Ley Electoral de Zacatecas art. 258"),
    (6, "Menciona dos causas para volver a contar una casilla", "Menciona dos causas para volver a contar una casilla.",
     "Falta el acta · no coincide · errores evidentes · nulos > diferencia · todos los votos a uno",
     "Por ejemplo: falta el acta, no coincide con la del presidente, o los votos nulos superan la diferencia entre primero y segundo.", "Ley Electoral de Zacatecas art. 259"),
    (6, "¿Cuándo procede el recuento total en el consejo?", "¿Cuándo procede el recuento total en el consejo?",
     "Diferencia ≤ 1 % entre 1.º y 2.º + petición expresa del 2.º lugar", "Si la diferencia entre primero y segundo es de un punto porcentual o menos, y lo pide el representante del segundo lugar.", "Ley Electoral de Zacatecas art. 259"),
    (6, "¿Las casillas recontadas en el consejo pueden recontarse en el tribunal?", "¿Las casillas recontadas en el consejo pueden recontarse en el tribunal?",
     "No, en ningún caso", "No. En ningún caso puede pedirse al tribunal.", "Ley Electoral de Zacatecas art. 259"),
    (6, "¿Cuándo hace el Consejo General los cómputos estatales?", "¿Cuándo hace el Consejo General los cómputos estatales?",
     "El domingo siguiente a la jornada", "El domingo siguiente a la jornada electoral.", "Ley Electoral de Zacatecas art. 271"),

    (7, "¿Quién acredita a los observadores y hasta cuándo se solicita?", "¿Quién acredita a los observadores, y hasta cuándo se solicita?",
     "El INE · del inicio del proceso al 30 de abril", "El INE, y se solicita desde el inicio del proceso hasta el treinta de abril.", "LGIPE art. 217 · Reglamento de Elecciones art. 187"),
    (7, "¿El PREP da resultados definitivos?", "¿El PREP da resultados definitivos?",
     "No: son preliminares y solo informativos", "No. Sus resultados son preliminares y de carácter estrictamente informativo.", "Ley Electoral de Zacatecas art. 256"),
]
assert len(P) == TOTAL_P, len(P)

ESCENAS = [
    {"id": "intro", "bloque": 0, "pre": 0.6,
     "vis": dict(tipo="portada", titulo="50 preguntas", sub="Entrevista IEEZ · Consejos Distritales y Municipales · contesta antes de que acabe el reloj"),
     "frases": ["[warmly] Cuestionario exprés: cincuenta preguntas para tu entrevista del Instituto Electoral.",
                "Cuando suene el reloj, contesta en voz alta antes de ver la respuesta."]},
]
_tema = None
for _k, (_t, _q, _qv, _r, _rv, _f) in enumerate(P, 1):
    if _t != _tema:
        _tema = _t
        ESCENAS.append({"id": f"tema{_t}", "bloque": _t, "vis": dict(tipo="portada", titulo=BLOQUES[_t], sub=f"Tema {_t} de 7"),
                        "frases": [f"Tema {['', 'uno', 'dos', 'tres', 'cuatro', 'cinco', 'seis', 'siete'][_t]}: {BLOQUES[_t].lower()}."]})
    ESCENAS.append({"id": f"p{_k}q", "bloque": _t, "post": PAUSA + 0.4, "frases": [f"{palabra(_k).capitalize()}. {_qv}"],
                    "vis": dict(tipo="pregunta", texto=_q, caso=False, cuenta=PAUSA, num=_k, de=TOTAL_P)})
    ESCENAS.append({"id": f"p{_k}a", "bloque": _t, "frases": [_rv], "vis": dict(tipo="respuesta", texto=_r, fuente=_f)})
ESCENAS.append({"id": "cierre", "bloque": 7, "post": 2.5,
                "vis": dict(tipo="portada", titulo="¡Mucho éxito!", sub="Repite las que fallaste · responde con la ley que la sostiene"),
                "frases": ["Listo: cincuenta preguntas. Repite las que fallaste, y cuando contestes, cita la ley que te respalda.",
                           "[warmly] Mucho éxito en tu entrevista."]})

TRANSICIONES = [("continua", 0.4)] * (len(ESCENAS) - 1)
# Whisper escribe los números con cifras («12.», «8:15»): no es error de la voz
CER_MAX_POR_FRASE = {f"p{k}q_0": 0.35 for k in range(1, TOTAL_P + 1)}
CER_MAX_POR_FRASE.update({f"p{k}a_0": 0.35 for k in range(1, TOTAL_P + 1)})
CER_MAX_POR_FRASE["intro_0"] = 0.2


def _tramos():
    ruta = os.path.join(os.path.dirname(os.path.abspath(__file__)), "timeline.json")
    durs = {}
    if os.path.exists(ruta):
        for e in json.load(open(ruta, encoding="utf-8"))["escenas"]:
            durs[e["id"]] = e["t1"] - e["t0"]
    grupos, actual, acum = [], [], 0.0
    for e in ESCENAS:
        d = durs.get(e["id"], 4.0 + 5.5 * len(e["frases"]))
        if actual and acum + d > 150.0:
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
