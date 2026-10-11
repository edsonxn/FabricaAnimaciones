# -*- coding: utf-8 -*-
"""Escribe youtube.json (título, descripción con capítulos tomados de timeline.json, etiquetas).  python _youtube.py"""
import json, os
AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
TL = json.load(open("timeline.json", encoding="utf-8"))
T0 = {e["id"]: e["t0"] for e in TL["escenas"]}
CAP = [("gancho", "El hombre que no firmó"), ("cliente", "Quién es Daniel Kokotajlo"), ("profecia", "La predicción de 2021"),
       ("renuncia", "La renuncia a OpenAI"), ("precio", "El precio del silencio: 85 % de su patrimonio"),
       ("escandalo", "El escándalo y el 70 %"), ("expediente", "«AI 2027»: el expediente"), ("agentes", "La máquina que construye máquinas"),
       ("robo", "Febrero de 2027: el robo"), ("ejercito", "200 000 copias"), ("afuera", "Lo que se ve desde la calle"),
       ("mentira", "La máquina que miente"), ("filtracion", "La filtración"), ("voto", "Seis contra cuatro"),
       ("carrera", "Primer final: la carrera"), ("freno", "Segundo final: el freno"), ("dudas", "Las críticas"),
       ("marcador", "¿Se está cumpliendo?"), ("plan", "Lo que propone: esperar hasta 2040"), ("cierre", "Caso abierto")]


def mmss(t):
    t = int(t)
    return f"{t // 60}:{t % 60:02d}"


caps = "\n".join(f"{mmss(0 if k == 0 else T0[i])} {s}" for k, (i, s) in enumerate(CAP))
desc = f"""En 2024, un investigador de OpenAI renunció y se negó a firmar el acuerdo que le prohibía hablar mal de la empresa, aunque eso ponía en riesgo acciones que valían cerca del 85 % del patrimonio de su familia. Un año después publicó «AI 2027»: un pronóstico, mes a mes, de cómo podría llegar una inteligencia artificial que nos supere en todo. Un detective abre el expediente: quién es Daniel Kokotajlo, qué predijo, en qué acertó, en qué falló, los dos finales que escribió… y por qué su fecha se ha movido.

{caps}

Importante: «AI 2027» es un ESCENARIO, no un hecho. La empresa «OpenBrain», el robo de febrero de 2027, las 200 000 copias, la votación 6-4 y los dos finales son ficción escrita por sus autores para ilustrar un pronóstico. Sus propios autores dicen que 2027 era el año más probable, no uno seguro, y han revisado sus fechas varias veces.

Fuentes:
• AI Futures Project, «AI 2027» (3 de abril de 2025), por Daniel Kokotajlo, Scott Alexander, Thomas Larsen, Eli Lifland y Romeo Dean: ai-2027.com
• Daniel Kokotajlo, «What 2026 Looks Like» (6 de agosto de 2021)
• Vox (Kelsey Piper, mayo de 2024) sobre los acuerdos de salida de OpenAI; OpenAI retiró la cláusula y Kokotajlo conservó sus acciones
• Carta abierta «A Right to Warn about Advanced AI» (4 de junio de 2024), 13 firmantes
• The New York Times (junio de 2024 y abril de 2025): su estimación del 70 % y el perfil de Kevin Roose
• AI Futures Project, «Grading AI 2027's 2025 Predictions» (12 de febrero de 2026) y «Q2.5 2026 Timelines Update» (16 de agosto de 2026): la realidad avanza a ~75 % del ritmo del escenario; mediana de Kokotajlo para la superinteligencia: 2029
• AI Futures Project, «AI 2040: Plan A» (julio de 2026)
• Crítica de Ali Farhadi (Allen Institute for AI): el escenario no está suficientemente fundamentado en evidencia científica

Narración con voz sintética. Animación dibujada por código, cuadro a cuadro, en tinta y aguada. Los personajes dibujados son recreaciones genéricas: no son retratos de personas reales.

Míralo también:
• Deepfake: la videollamada donde NADIE era real → https://youtu.be/SNmr4gh5PkY
• Por qué la IA podría DESTRUIR a la humanidad → https://youtu.be/eZlZRGf3VC0

#InteligenciaArtificial #AI2027 #OpenAI"""
J = {
    "titulo": "Qué pasará con la IA en 2027: la advertencia del que renunció a OpenAI",
    "titulos_alternativos": [
        "Renunció a OpenAI para avisarnos: qué pasará en 2027",
        "AI 2027: el expediente del informante de OpenAI",
        "El informante de OpenAI que le puso FECHA al final",
    ],
    "descripcion": desc,
    "etiquetas": ["ai 2027", "inteligencia artificial", "openai", "daniel kokotajlo", "superinteligencia", "futuro de la inteligencia artificial",
                  "que pasara con la ia", "informante openai", "riesgos de la inteligencia artificial", "agi", "ia 2027", "chatgpt",
                  "carrera de la ia", "china ia", "alineamiento ia", "documental ia", "peligros de la inteligencia artificial", "cine negro",
                  "noir", "logia"],
    "categoria": 28, "idioma": "es", "idioma_audio": "es", "para_ninos": False,
    "miniatura": "salida/miniatura.jpg", "subtitulos": "salida/informante_2027.srt",
}
assert len(J["titulo"]) <= 100 and len(desc) < 5000, (len(J["titulo"]), len(desc))
json.dump(J, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(len(J["titulo"]), "car. título;", len(desc), "car. descripción")
print(caps)
