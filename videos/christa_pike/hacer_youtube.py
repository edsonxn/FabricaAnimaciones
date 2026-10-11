# -*- coding: utf-8 -*-
"""Genera youtube.json (título, descripción con capítulos reales del timeline, fuentes, etiquetas) a partir de timeline.json."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
CAP = {
    "gancho": "La noche del 30 de septiembre", "quien": "Quién es Christa Pike", "colleen": "Colleen Slemmer", "crimen": "12 de enero de 1995",
    "juicio": "Juicio y sentencia", "corredor": "Casi 30 años en el corredor de la muerte", "debate": "Un caso que divide",
    "camino": "La cuenta atrás", "noche": "Minuto a minuto: la ejecución", "despues": "Después: hospital, revisión y renuncia",
    "historial": "Tennessee y sus ejecuciones", "precedente": "Un caso casi sin precedentes", "cierre": "Lo que queda",
}


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


caps = "\n".join(f"{mmss(0 if i == 0 else e['t0'])} {CAP.get(e['id'], e['id'])}" for i, e in enumerate(TL["escenas"]))
desc = f"""El miércoles 30 de septiembre de 2026, Tennessee intentó ejecutar a Christa Pike con dos dosis de pentobarbital. Sobrevivió. Tres días después, el director de prisiones del estado renunció. Este es el caso completo: quién es Christa Pike, el asesinato de Colleen Slemmer en 1995, el juicio, casi treinta años en el corredor de la muerte, la noche de la ejecución minuto a minuto y lo que se sabe hasta ahora.

⏱️ CAPÍTULOS
{caps}

📚 FUENTES
• Renuncia de Frank Strada y estado de Pike (Associated Press, 3-oct-2026): https://abc7news.com/post/tennessees-prisons-chief-is-resigning-failed-execution-attempt-christa-pike/19904806/
• Al Jazeera (3-oct-2026): https://www.aljazeera.com/news/2026/10/3/tennessee-prisons-official-resigns-after-christa-pikes-failed-us-execution
• Newsweek (3-oct-2026), historial de ejecuciones fallidas y opiniones de expertos: https://www.newsweek.com/tennessee-prisons-chief-resigns-after-christa-pike-execution-failure-12520776
• Fox 9 (AP): https://www.fox9.com/news/christa-pike-latest-tennessee-prisons-chief-resigns-after-failed-execution
• CBS News, el caso y la fecha de ejecución: https://www.cbsnews.com/amp/news/tennessee-christa-gail-pike-execution-woman-death-row
• NBC News, crónica de la noche del 30 de septiembre: https://www.nbcnews.com/news/us-news/-was-mess-tennessee-fails-execute-inmate-2-lethal-injections-rcna600863
• ABC News, la madre de Colleen Slemmer: https://abcnews.com/US/mother-christa-pikes-victim-speaks-botched-execution-broke/story?id=136950906
• Cronología del caso, apelaciones y ejecución: https://en.wikipedia.org/wiki/Christa_Pike

ℹ️ La información está al 3 de octubre de 2026 y la historia sigue abierta: Pike seguía hospitalizada, en estado crítico, y una revisión independiente investiga lo ocurrido. Las afirmaciones sobre las vías intravenosas y el fármaco son las de sus abogados, no conclusiones oficiales. Hay descripciones de violencia (sin imágenes gráficas). Las animaciones, el esquema de la vena y la recreación de la ventana son gráficos explicativos, no imágenes reales; la miniatura es una ilustración generada con IA, no una imagen de la ejecución.

🎞️ Imágenes de archivo y de noticias de WBIR (Knoxville), France 24, NBC News, ABC News y NewsChannel 5, usadas con fines informativos y de comentario y con su crédito en pantalla. Fotos: Wikimedia Commons (Kaldari, Cessna86, Jon698, Warren LeMay, Joe Ravi, Lynn Freeny, Quintin Soloviev, Bill Allen / AP). Foto de ficha: Tennessee Department of Correction. Mapa de relieve: elevación AWS Terrain y límites Natural Earth (dominio público). Animaciones y gráficos: producción propia. Música: Lyria.

¿Qué opinas: debe Tennessee intentarlo otra vez? Te leo en los comentarios 👇

#ChristaPike #PenaDeMuerte #CrimenReal"""
datos = {
    "titulo": "Christa Pike: la ejecución que no terminó",
    "titulos_alternativos": ["Christa Pike sobrevivió a su ejecución: qué pasó", "Christa Pike: dos dosis y sigue viva"],
    "descripcion": desc,
    "etiquetas": ["christa pike", "christa pike ejecución", "christa pike execution", "ejecución fallida", "tennessee", "pena de muerte", "colleen slemmer",
                  "inyección letal", "pentobarbital", "frank strada", "bill lee tennessee", "corredor de la muerte", "crimen real", "caso real",
                  "documental", "documental de crimen", "job corps knoxville", "ejecución fallida tennessee", "estados unidos", "justicia",
                  "noticias", "caso christa pike", "mujer en el corredor de la muerte"],
    "categoria": 27,
    "idioma": "es", "idioma_audio": "es", "para_ninos": False,
    "miniatura": "salida/christa_pike_mini_final.jpg",
    "subtitulos": "salida/christa_pike.srt",
}
json.dump(datos, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("youtube.json listo; etiquetas:", sum(len(e) + 1 for e in datos["etiquetas"]), "caracteres; título", len(datos["titulo"]))
print(caps)
