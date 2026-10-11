# -*- coding: utf-8 -*-
"""Genera youtube.json (título, descripción con capítulos reales del timeline, fuentes, créditos, etiquetas) a partir de timeline.json."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
CAP = {
    "gancho": "Un millón de bitcoins sin dueño", "origen": "2008: la primera pista", "genesis": "El bloque génesis y su mensaje",
    "fantasma": "Un fantasma en los foros", "fortuna": "La única prueba", "perfil": "Cómo escribe Satoshi (análisis propio)",
    "dorian": "Sospechoso 1: Dorian Nakamoto", "hal": "Sospechoso 2: Hal Finney", "szabo": "Sospechoso 3: Nick Szabo",
    "wright": "Sospechoso 4: Craig Wright y el juicio de Londres", "todd": "Sospechoso 5: Peter Todd y la teoría de los dos",
    "leroux": "Paul Le Roux: la teoría que volvió", "back": "Sospechoso 6: Adam Back y la investigación del NYT",
    "archivo": "Lo que podría saber el gobierno", "espejo": "Todos somos Satoshi", "cierre": "El tablero completo",
}


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


caps = "\n".join(f"{mmss(0 if i == 0 else e['t0'])} {CAP.get(e['id'], e['id'])}" for i, e in enumerate(TL["escenas"]))
cr = json.load(open(os.path.join(AQUI, "imagenes", "creditos.json"), encoding="utf-8"))
USADAS = ["hal_finney", "running_bitcoin", "szabo_capa", "adam_back", "len_sassaman", "busto_budapest", "estatua_lugano", "whitepaper", "genesis_periodico",
          "lehman_dia", "rolls_building", "temple_city", "carreyrou", "le_roux", "pizza_day", "darling_2009"]
fotos = []
for k in USADAS:
    for n, v in cr.items():
        if n.startswith(k + "."):
            fotos.append(f"{v['autor'].split(chr(10))[0][:50]} ({v['licencia']})")
desc = f"""Hay más de un millón de bitcoins que nadie ha tocado desde hace más de quince años. Su dueño creó la primera criptomoneda del mundo y desapareció en 2011. Periodistas, programadores, documentales y hasta un tribunal de Londres han intentado ponerle cara. Este es el tablero completo de la investigación: las pistas (el bloque génesis, la ortografía, los horarios, el primer correo) y los sospechosos, de Dorian Nakamoto a Adam Back, señalado por The New York Times en 2026.

⏱️ CAPÍTULOS
{caps}

📚 FUENTES
• Satoshi Nakamoto (cronología, características y candidatos): https://en.wikipedia.org/wiki/Satoshi_Nakamoto
• The New York Times y Adam Back (TechCrunch, 8-abr-2026): https://techcrunch.com/2026/04/08/british-cryptographer-adam-back-denies-nyt-report-that-he-is-bitcoin-creator-satoshi-nakamoto/
• Resumen de la investigación de John Carreyrou (Coin360): https://coin360.com/news/adam-back-satoshi-nakamoto-nyt-investigation
• Fallo del Tribunal Superior de Londres sobre Craig Wright: https://en.wikipedia.org/wiki/Craig_Steven_Wright
• Documental de HBO «Money Electric» y Peter Todd: https://en.wikipedia.org/wiki/Money_Electric:_The_Bitcoin_Mystery
• Hal Finney: https://en.wikipedia.org/wiki/Hal_Finney_(computer_scientist)
• Hal Finney y la carrera del 18-abr-2009 (análisis de Jameson Lopp): https://coingape.com/jameson-lopp-busts-the-myth-about-hal-finney-being-bitcoin-creator-satoshi-nakamoto/
• Universidad de Aston y Nick Szabo (2014): https://www.sciencedaily.com/releases/2014/04/140417090547.htm
• Paul Le Roux y el pasaporte «Solotshi» (The Crypto Times, 28-sep-2026): https://cryptotimes.io/2026/09/28/is-paul-le-roux-really-satoshi-nakamoto-what-the-record-actually-shows
• Carteras de Satoshi y su valor (Arkham, vía The Crypto Times y FinanceFeeds): https://financefeeds.com/satoshi-nakamoto-identity-2026-suspects-and-the-85b-question/
• Demanda FOIA contra el Departamento de Seguridad Nacional (2025): https://www.fxstreet.com/cryptocurrencies/news/who-is-satoshi-crypto-lawyer-sues-dhs-to-reveal-satoshi-nakamotos-identity-202504081158
• Busto de Budapest «We are all Satoshi»: https://news.bitcoin.com/we-are-all-satoshi-statue-bitcoin-creator-satoshi-nakamoto-hungary/
• Mensajes de Satoshi (archivo usado para la gráfica de horarios): https://satoshi.nakamotoinstitute.org/
• Bloque génesis y transacción del bloque 170 (datos de la cadena): https://blockstream.info/

🔎 Análisis propio: la gráfica de horarios cuenta los 543 mensajes de Satoshi en foros del archivo del Satoshi Nakamoto Institute, por hora UTC (solo 7 entre las 5:00 y las 11:59). El código mostrado es el original de Bitcoin v0.1 (licencia MIT) y el volcado hexadecimal y la firma son los datos reales de la cadena.

ℹ️ Información al 3 de octubre de 2026. Ninguno de los señalados ha sido probado como Satoshi y todos los vivos lo niegan; un tribunal británico dictaminó en 2024 que Craig Wright no lo es. Las escenas dibujadas, los esquemas y la revista son ilustraciones, no documentos reales. Los sospechosos sin foto con licencia libre aparecen como silueta.

📷 Fotos (Wikimedia Commons): {"; ".join(fotos)}. Mapa: Natural Earth (dominio público). Animaciones y gráficos: producción propia. Música: Lyria.

¿Quién crees que es Satoshi? Deja tu sospechoso en los comentarios 👇

#SatoshiNakamoto #Bitcoin #Misterio"""
datos = {
    "titulo": "¿Quién es Satoshi Nakamoto? El tablero completo",
    "titulos_alternativos": ["Satoshi Nakamoto: los 7 sospechosos del creador de Bitcoin", "El creador de Bitcoin desapareció con 1 millón de BTC"],
    "descripcion": desc,
    "etiquetas": ["satoshi nakamoto", "quien es satoshi nakamoto", "creador de bitcoin", "bitcoin", "adam back", "hal finney", "nick szabo",
                  "craig wright", "dorian nakamoto", "peter todd", "len sassaman", "paul le roux", "misterio de bitcoin", "documental bitcoin",
                  "new york times satoshi", "bloque genesis", "criptomonedas", "misterios de internet", "documental", "historia de bitcoin",
                  "money electric", "finding satoshi"],
    "categoria": 27,
    "idioma": "es", "idioma_audio": "es", "para_ninos": False,
    "miniatura": "salida/satoshi_nakamoto_mini_final.jpg",
    "subtitulos": "salida/satoshi_nakamoto.srt",
}
json.dump(datos, open(os.path.join(AQUI, "youtube.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("youtube.json listo; etiquetas:", sum(len(e) + 1 for e in datos["etiquetas"]), "caracteres; título", len(datos["titulo"]), "; descripción", len(desc))
print(caps)
