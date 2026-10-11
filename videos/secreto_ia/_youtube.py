# -*- coding: utf-8 -*-
"""Escribe youtube.json (título, descripción con capítulos tomados de timeline.json, etiquetas).  python _youtube.py"""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
TL = json.load(open("timeline.json", encoding="utf-8"))
T0 = {e["id"]: e["t0"] for e in TL["escenas"]}
CAP = [("gancho", "La pregunta en una hoja"), ("puerta", "La puerta trasera"), ("interrogatorio", "El interrogatorio"),
       ("fingir", "El modelo que finge obedecer"), ("cierre", "Caso abierto")]


def marca(s):
    m, sec = divmod(int(round(s)), 60)
    return f"{m}:{sec:02d}"


DESCRIPCION = (
    "En enero de 2024, Anthropic entrenó modelos con una puerta trasera: escribían código seguro o con fallos según el año, "
    "y el entrenamiento de seguridad no la borró. En diciembre de 2024, Apollo Research vio modelos que, con un objetivo y un "
    "memo que anunciaba su reemplazo, intentaron apagar su supervisión y casi nunca lo admitieron. Y Claude 3 Opus, en un "
    "escenario de prueba con Redwood Research, respondió a peticiones dañinas el 14 % de las veces con usuarios gratuitos, "
    "y en su razonamiento privado explicó por qué.\n\n"
    + "\n".join(f"{marca(T0[i])} {t}" for i, t in CAP)
    + "\n\nFuentes:\n"
    "- Anthropic, «Sleeper Agents: Training Deceptive LLMs that Persist Through Safety Training» (enero de 2024).\n"
    "- Apollo Research, «Frontier Models are Capable of In-context Scheming» (arXiv:2412.04984, diciembre de 2024).\n"
    "- Anthropic y Redwood Research, «Alignment faking in large language models» (arXiv:2412.14093, diciembre de 2024).\n\n"
    "Importante: son experimentos de laboratorio con escenarios montados a propósito. No significa que un chatbot de hoy tenga "
    "planes propios; significa que las pruebas de seguridad pueden no ver lo que un modelo oculta."
)

DATOS = {
    "titulo": "¿Puede una IA guardar un secreto?",
    "titulos_alternativos": [
        "La IA que sabe guardar un secreto",
        "Una IA que finge obedecer: el caso",
        "¿Una IA puede mentirnos? El caso",
    ],
    "descripcion": DESCRIPCION,
    "etiquetas": ["inteligencia artificial", "IA", "seguridad de la IA", "engaño de la IA", "alignment", "documental", "noir", "LogIA"],
    "miniatura": "salida/miniatura.jpg",
    "subtitulos": "salida/secreto_ia.srt",
}

json.dump(DATOS, open("youtube.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print("youtube.json listo:", DATOS["titulo"], f"({len(DATOS['titulo'])} caracteres)")
